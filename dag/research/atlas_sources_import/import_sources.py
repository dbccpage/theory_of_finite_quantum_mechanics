"""Copy the cited files of the restored F004 families into sources/atlas and point the DAG at them.

AuthorityEffect: None. Reads the plan from plan_sources.py. Copies only files the plan marks `verified` whose bytes
match the sibling git history and that have no identical or newline-equivalent twin in the repository; every
other cited file is resolved to its existing twin. Writes sources/atlas/PROVENANCE.json and rewrites path text in
dag/derivation_dag.json and dag/fragments/*.json (keys source, lean, lean4, rust, python and structured `path`
entries; never `f004_refs`, `coda_atlas_paths`, `coda_atlas_ids`, never an `absent:` note). No status, statement or
route changes.

    python -I -X utf8 import_sources.py <repo> <plan.json>            # dry run
    python -I -X utf8 import_sources.py <repo> <plan.json> --write
"""
import argparse, collections, difflib, hashlib, json, re
from typing import Any
from pathlib import Path

COMMIT_PARENT = '3379759468^'
REWRITE_KEYS = {'source', 'lean', 'lean4', 'rust', 'python', 'path', 'witnesses', 'sources'}
SKIP_KEYS = {'f004_refs', 'coda_atlas_paths', 'coda_atlas_ids'}
DEST = 'sources/atlas/F004_papers'


def line_diff(a: bytes, b: bytes) -> dict:
    la = a.decode('utf-8', 'replace').splitlines()
    lb = b.decode('utf-8', 'replace').splitlines()
    if len(la) * len(lb) > 4_000_000 and abs(len(la) - len(lb)) > 0:
        return {'lines_atlas': len(la), 'lines_in_repo': len(lb)}
    sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
    return {'lines_atlas': len(la), 'lines_in_repo': len(lb), 'similarity': round(sm.ratio(), 4)}


def rewrite(obj, pattern, table, counter, ctx=''):
    if isinstance(obj, dict):
        out = {k: (v if k in SKIP_KEYS else rewrite(v, pattern, table, counter, k)) for k, v in obj.items()}
        if out.get('root') == 'symbol_game' and isinstance(out.get('path'), str) and out['path'] in set(table.values()):
            out['root'] = 'local'
            counter['root->local'] += 1
        return out
    if isinstance(obj, list):
        return [rewrite(v, pattern, table, counter, ctx) for v in obj]
    if isinstance(obj, str):
        if ctx not in REWRITE_KEYS or obj.startswith('absent'):
            return obj

        def sub(m):
            counter[ctx] += 1
            return table[m.group(0)]
        return pattern.sub(sub, obj)
    return obj


def inside(root: Path, relative: str) -> Path:
    """Resolve a planned repository path without allowing an escape."""
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f'invalid repository path: {relative!r}')
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()) or target == root.resolve():
        raise ValueError(f'path escapes repository: {relative}')
    return target


def preflight(root: Path, rows: Any) -> list[tuple[dict[str, Any], bytes, str, bytes]]:
    """Validate every row before writing; return the exact bytes that were checked."""
    if not isinstance(rows, list) or not rows:
        raise ValueError('plan must be a nonempty list')
    prepared = []
    seen: set[str] = set()
    destinations: set[Path] = set()
    for row in rows:
        if not isinstance(row, dict) or row.get('status') != 'verified':
            raise ValueError('every plan row must be verified')
        original = row.get('atlas_path')
        if not isinstance(original, str) or not original or original in seen:
            raise ValueError('missing or duplicate atlas path')
        seen.add(original)
        digest, size = row.get('git_sha256'), row.get('size')
        if not isinstance(digest, str) or re.fullmatch(r'[0-9a-f]{64}', digest) is None:
            raise ValueError(f'invalid source digest: {original}')
        if type(size) is not int or size < 0 or not isinstance(row.get('ana_path'), str):
            raise ValueError(f'invalid source metadata: {original}')
        data = Path(row['ana_path']).read_bytes()
        if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f'source changed since planning: {original}')
        twin = row.get('resolved_to_existing')
        if twin is not None:
            if not isinstance(twin, dict) or twin.get('match') not in ('identical', 'newline_equivalent'):
                raise ValueError(f'invalid twin match: {original}')
            dest = twin.get('path')
            target = inside(root, dest)
            target_data = target.read_bytes()
            normalise = lambda b: b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
            matches = target_data == data if twin['match'] == 'identical' else normalise(target_data) == normalise(data)
            if not matches:
                raise ValueError(f'existing twin changed since planning: {original}')
        else:
            family, relative = row.get('family'), row.get('rel')
            if not isinstance(family, str) or re.fullmatch(r'[A-Za-z0-9_-]+', family) is None:
                raise ValueError(f'invalid source family: {original}')
            family_root = inside(root, f'{DEST}/{family}')
            target = inside(family_root, relative)
            dest = target.relative_to(root.resolve()).as_posix()
            target_data = data
            if target in destinations:
                raise ValueError(f'duplicate copy destination: {dest}')
            destinations.add(target)
        for other in row.get('in_repo_same_name_different_content', [])[:3]:
            inside(root, other).read_bytes()
        prepared.append((row, data, dest, target_data))
    # A later copied row must not overwrite an earlier resolved twin.
    for row, _, dest, _ in prepared:
        if 'resolved_to_existing' in row and inside(root, dest) in destinations:
            raise ValueError(f'copy destination collides with an existing twin: {dest}')
    return prepared


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo')
    ap.add_argument('plan')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    root = Path(args.repo)
    rows = json.loads(Path(args.plan).read_text(encoding='utf-8'))
    try:
        prepared = preflight(root, rows)
    except (ValueError, OSError) as exc:
        ap.exit(1, f'refusing: {exc}\n')
    table, prov = {}, []
    for r, data, dest, target_data in prepared:
        entry = {'original_atlas_path': r['atlas_path'], 'ana_path': r['ana_path'], 'sha256': r['git_sha256'],
                 'size_bytes': r['size'], 'in_repo_sha256': hashlib.sha256(target_data).hexdigest(), 'git_commit': COMMIT_PARENT + ' (the_symbol_game)'}
        if 'resolved_to_existing' in r:
            entry['outcome'] = 'resolved_to_existing'
            entry['in_repo_path'] = r['resolved_to_existing']['path']
            entry['match'] = r['resolved_to_existing']['match']
            table[r['atlas_path']] = r['resolved_to_existing']['path']
        else:
            entry['outcome'] = 'copied'
            entry['in_repo_path'] = dest
            table[r['atlas_path']] = dest
            if args.write:
                target = inside(root, dest)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                if target.read_bytes() != data:
                    raise OSError(f'copy verification failed: {dest}')
            twins = r.get('in_repo_same_name_different_content')
            if twins:
                entry['edition_difference'] = {
                    'same_named_in_repo_files': twins,
                    'note': 'the in-repo file differs from the atlas file; references keep pointing at the atlas copy',
                    'diffs': {t: line_diff(data, inside(root, t).read_bytes()) for t in twins[:3]}}
        prov.append(entry)
    counts = collections.Counter(e['outcome'] for e in prov)
    print('outcomes', dict(counts), 'edition differences', sum(1 for e in prov if 'edition_difference' in e))
    if args.write:
        doc = {'schema_version': 'atlas_sources_provenance.v1', 'authority_effect': 'None',
               'source': 'the_symbol_game omega_engine_atlas/coda_atlas/F004_papers/{family}, deleted from the sibling working tree by commit 3379759468 and restored to --ana',
               'git_commit': COMMIT_PARENT, 'copied': counts['copied'], 'resolved_to_existing': counts['resolved_to_existing'],
               'files': sorted(prov, key=lambda e: e['original_atlas_path'])}
        (root / 'sources/atlas').mkdir(parents=True, exist_ok=True)
        (root / 'sources/atlas/PROVENANCE.json').write_text(json.dumps(doc, indent=1, ensure_ascii=False) + '\n',
                                                            encoding='utf-8', newline='\n')
    pattern = re.compile(r'(?<![\w/.\-])(?:' + '|'.join(re.escape(p) for p in sorted(table, key=len, reverse=True))
                         + r')(?![\w/])')
    total = 0
    for rel in ['dag/derivation_dag.json'] + sorted(p.relative_to(root).as_posix() for p in (root / 'dag/fragments').glob('*.json')):
        path = root / rel
        data = json.loads(path.read_bytes())
        counter = collections.Counter()
        new = rewrite(data, pattern, table, counter)
        n = sum(counter.values())
        total += n
        print(f'{rel}: {n} reference(s) rewritten {dict(counter)}')
        if args.write and n:
            path.write_bytes((json.dumps(new, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))
    print('total', total)


if __name__ == '__main__':
    main()
