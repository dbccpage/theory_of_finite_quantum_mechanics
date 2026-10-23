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
import argparse, collections, difflib, json, re, shutil
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo')
    ap.add_argument('plan')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    root = Path(args.repo)
    rows = json.loads(Path(args.plan).read_text(encoding='utf-8'))
    bad = [r for r in rows if r['status'] != 'verified']
    if bad:
        raise SystemExit('refusing: %d files are not verified against the sibling git history: %s'
                         % (len(bad), [(r['atlas_path'], r['status']) for r in bad[:5]]))
    table, prov = {}, []
    for r in rows:
        entry = {'original_atlas_path': r['atlas_path'], 'ana_path': r['ana_path'], 'sha256': r['git_sha256'],
                 'size_bytes': r['size'], 'git_commit': COMMIT_PARENT + ' (the_symbol_game)'}
        if 'resolved_to_existing' in r:
            entry['outcome'] = 'resolved_to_existing'
            entry['in_repo_path'] = r['resolved_to_existing']['path']
            entry['match'] = r['resolved_to_existing']['match']
            table[r['atlas_path']] = r['resolved_to_existing']['path']
        else:
            dest = f"{DEST}/{r['family']}/{r['rel']}"
            entry['outcome'] = 'copied'
            entry['in_repo_path'] = dest
            table[r['atlas_path']] = dest
            if args.write:
                src = Path(r['ana_path'])
                data = src.read_bytes()
                target = root / dest
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                assert target.read_bytes() == data
            twins = r.get('in_repo_same_name_different_content')
            if twins:
                entry['edition_difference'] = {
                    'same_named_in_repo_files': twins,
                    'note': 'the in-repo file differs from the atlas file; references keep pointing at the atlas copy',
                    'diffs': {t: line_diff(Path(r['ana_path']).read_bytes(), (root / t).read_bytes()) for t in twins[:3]}}
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
