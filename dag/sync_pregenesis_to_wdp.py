"""Synchronize the pre-genesis to WDP fragment into papers, derivation_dag.json and the derivation index.

The fragment dag/fragments/pregenesis_to_wdp.json owns records TFQ-0417 upward:
their papers, their records in derivation_dag.json (source_slice pregenesis_to_wdp,
spliced before the application-branch block), their DAG nodes and routes (spliced
before the application-branch block), the five stage sections of
dag/derivations/README.md that list them, and the appended child bullets in section 4
of unpinned parent papers. Custody-pinned papers (dag/operads/*.yaml paper_source_pins)
are never written.

derivation_dag.json (schema derivation_dag.v2) is the single source of the derivation
graph. The read-only views theory_of_finite_qm.jsonl and theory_of_finite_qm.md are
rendered from it by dag/render_dag_views.py, which this script calls; the renderer lists
every non-application record of the five stages PREGENESIS, GENESIS, AUTHORIZATION,
MSSN_SN and WDP in the plain layout of their Markdown sections.

Run order: sync_pfp_results.py, sync_unified_dag.py, sync_application_branches.py, this
script; --check on all four is then clean. --check detects stale generated data without
writing.
AuthorityEffect: None. Synchronization does not establish a mathematical claim.
"""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import render_dag_views as views  # noqa: E402
FRAGMENT = HERE / 'fragments/pregenesis_to_wdp.json'
SLICE = 'pregenesis_to_wdp'
TAG = 'pregenesis-to-wdp'
NODE_PREFIX = 'PGW-'
ROUTE_PREFIX = 'PGW-R-'
APP_MARKER = '<!-- application-branches: generated from fragments/application_branches.json -->'
PINNED_BEGIN = '<!-- pregenesis-to-wdp:pinned-children:begin -->'
PINNED_END = '<!-- pregenesis-to-wdp:pinned-children:end -->'
UUID_NAMESPACE = uuid.uuid5(
    uuid.NAMESPACE_URL,
    'https://github.com/dbccpage/theory_of_finite_quantum_mechanics/dag/theory_of_finite_qm.jsonl')
OWNED_STAGES = ('PREGENESIS', 'GENESIS', 'AUTHORIZATION', 'MSSN_SN', 'WDP')
STAGE_FOLDERS = {
    'PREGENESIS': '01_pregenesis', 'GENESIS': '02_genesis', 'AUTHORIZATION': '04_authorization',
    'MSSN_SN': '05_mssn_sn', 'WDP': '06_wdp',
}
DAG_STAGE = {'PREGENESIS': 'PREGENESIS', 'GENESIS': 'GENESIS', 'AUTHORIZATION': 'IMPLEMENTATION',
             'MSSN_SN': 'MSSN_SN', 'WDP': 'WDP'}
RECORD_STATUSES = ('DEFINITION', 'SOURCE_RECORD', 'PROVED_LEAN', 'OPEN_OBLIGATION', 'GAP', 'CONDITIONAL')
# Paper status -> DAG node statuses it may be recorded with.
STATUS_PAIRS = {
    'DEFINITION': {'DEFINITION'},
    'PROVED_LEAN': {'PROVED_LEAN'},
    'SOURCE_RECORD': {'PROVED_LEAN', 'PROVED_PROSE', 'DEFINITION', 'COMPUTATIONALLY_CHECKED',
                      'CONDITIONAL', 'REFUTED'},
    'OPEN_OBLIGATION': {'OPEN', 'CONDITIONAL'},
    'GAP': {'OPEN'},
    'CONDITIONAL': {'CONDITIONAL'},
}
ROUTE_STATUS = {
    'PROVED_LEAN': 'DERIVED_LEAN', 'PROVED_PROSE': 'DERIVED_PROSE', 'DEFINITION': 'DERIVED_PROSE',
    'REFUTED': 'DERIVED_PROSE', 'COMPUTATIONALLY_CHECKED': 'COMPUTED',
    'CONDITIONAL': 'CONDITIONAL_ON_IMPORT', 'OPEN': 'GAP_NO_DERIVATION',
}
ROOTS = ('local', 'symbol_game', 'github19l')
TIERS = (('lean', 'Lean 4 Theorems'),
         ('rust', 'Sovereign Rust Certifiers (Exact Rational Arithmetic)'),
         ('python', 'Python Oracles & Numerical Evaluators'))
JSONL_TIER = {'lean': 'lean4', 'rust': 'rust', 'python': 'python'}
NAME_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
FORBIDDEN = ('proves', 'guarantees', 'mathematically verifies', 'fundamentally', 'true intelligence',
             'impossible', 'universal', 'flawless', 'perfectly', 'clearly', 'obviously', 'simply',
             'merely', 'weaponized')
CONTEXT = ('In accordance with strict constructive principles:\n'
           '- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer '
           'combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / '
           'Gaussian integer arithmetic).\n'
           '- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be '
           'assumed prior to their explicit constructive descent.\n')


json_text = views.json_text


def load_manifest(root: Path = ROOT):
    return json.loads((root / 'dag/fragments/pregenesis_to_wdp.json').read_text(encoding='utf-8'))


def pinned_papers(root: Path) -> set[str]:
    """Repo-relative paths of papers whose bytes an operad record pins."""
    pinned = set()
    for path in sorted((root / 'dag/operads').glob('*.yaml')):
        in_pins = False
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.strip() == 'paper_source_pins:':
                in_pins = True
                continue
            if in_pins:
                item = re.match(r'^\s*- path: (dag/derivations/\S+\.md)\s*$', line)
                if item:
                    pinned.add(item.group(1))
                elif not re.match(r'^\s+(sha256: \S+)?$', line):
                    in_pins = False
    return pinned


def read_records(root: Path) -> list[dict]:
    """The TFQ records of derivation_dag.json, in order."""
    return views.load_dag(root)['records']


def paper_paths(root: Path) -> dict[str, str]:
    paths = {}
    for p in (root / 'dag/derivations').rglob('tfq_*.md'):
        key = re.match(r'tfq_(\d{4})_', p.name)
        if key:
            paths['TFQ-' + key[1]] = p.relative_to(root).as_posix()
    return paths


def record_uuid(record_id: str) -> str:
    return str(uuid.uuid5(UUID_NAMESPACE, record_id))


def slug(name: str) -> str:
    return name.replace('-', '_')


def new_paper_path(r) -> str:
    return f'dag/derivations/{STAGE_FOLDERS[r["stage"]]}/tfq_{r["id"][4:]}_{slug(r["name"])}.md'


def node_id(r) -> str:
    return NODE_PREFIX + r['name'].upper()


def ref_string(entry, manifest, jsonl: bool = False) -> str:
    """The DAG spelling of one witness or source reference; jsonl=True gives the JSONL spelling.

    DAG references to the_symbol_game are unprefixed, as in the existing PG nodes (the validator
    resolves them against that checkout). JSONL witnesses outside this checkout carry an
    external: prefix, because the JSONL path check resolves unprefixed paths in this repository.
    """
    if 'absent' in entry:
        return 'absent: ' + entry['absent']
    path = entry['path']
    if entry['root'] == 'github19l':
        path = f'external:github.com/dbccpage/19L57G1@{manifest["external_roots"]["github19l"]["commit"]}/{path}'
    elif entry['root'] == 'symbol_game' and jsonl:
        path = 'external:the_symbol_game/' + path
    if entry.get('symbol'):
        return path + '::' + entry['symbol']
    if entry.get('lines'):
        return path + ':' + entry['lines']
    return path


def ref_url(entry, manifest, paper: str) -> str | None:
    if 'absent' in entry:
        return None
    if entry['root'] == 'local':
        return posixpath.relpath(entry['path'], posixpath.dirname(paper))
    if entry['root'] == 'symbol_game':
        commit = manifest['external_roots']['symbol_game']['commit']
        return f'https://github.com/dbccpage/the_symbol_game/blob/{commit}/{entry["path"]}'
    commit = manifest['external_roots']['github19l']['commit']
    return f'https://github.com/dbccpage/19L57G1/blob/{commit}/{entry["path"]}'


def ref_label(entry, manifest) -> str:
    if 'absent' in entry:
        return entry['absent']
    if entry['root'] == 'github19l':
        commit = manifest['external_roots']['github19l']['commit'][:9]
        label = f'github:dbccpage/19L57G1@{commit}/{entry["path"]}'
    else:
        label = entry['path']
    if entry.get('symbol'):
        label += '::' + entry['symbol']
    if entry.get('lines'):
        label += ':' + entry['lines']
    return label


def prose_fields(r):
    yield r['summary']
    yield r['obligation']
    yield r['fence']
    yield from r.get('imports', [])
    if r.get('dag') and 'status' in r['dag']:
        yield r['dag'].get('source_status', '')


def validate_manifest(manifest, records_by_id, pinned, paths, lint_range=None) -> list[str]:
    """Schema and ordering checks; lint_range=(lo, hi) relaxes contiguity for a partial batch
    and accepts references to ids in [lo, hi] that other batches will supply."""
    errs = []
    recs = manifest['records']
    first = int(manifest['first_id'][4:])
    manifest_ids = [r['id'] for r in recs]
    if lint_range is None and manifest_ids != [f'TFQ-{first + i:04d}' for i in range(len(recs))]:
        errs.append('manifest ids must run contiguously from first_id')
    if len(set(manifest_ids)) != len(manifest_ids):
        errs.append('duplicate manifest ids')
    by_id = {r['id']: r for r in recs}
    names = set()
    rank = {s: i for i, s in enumerate(('PREGENESIS', 'GENESIS', 'FINITE_OBSTRUCTION', 'AUTHORIZATION',
                                         'MSSN_SN', 'WDP'))}
    for r in recs:
        rid = r['id']
        old = records_by_id.get(rid)
        if old is not None and old.get('source_slice') != SLICE:
            errs.append(f'{rid}: collides with a record of slice {old.get("source_slice")}')
        if not NAME_RE.match(r['name']) or len(r['name']) > 40:
            errs.append(f'{rid}: name must be kebab-case and at most 40 characters')
        if r['name'] in names:
            errs.append(f'{rid}: duplicate name {r["name"]}')
        names.add(r['name'])
        if r['stage'] not in OWNED_STAGES:
            errs.append(f'{rid}: stage {r["stage"]} is not owned by this fragment')
        if r.get('group') not in (None, 'S(n)', 'MSS-N') or (r.get('group') and r['stage'] != 'MSSN_SN'):
            errs.append(f'{rid}: bad group {r.get("group")}')
        if r['record_status'] not in RECORD_STATUSES:
            errs.append(f'{rid}: bad record_status {r["record_status"]}')
        for key in ('summary', 'obligation', 'fence'):
            if not r.get(key) or '\n' in r[key] or '<!--' in r[key]:
                errs.append(f'{rid}: {key} must be one non-empty line')
        for text in prose_fields(r):
            for word in FORBIDDEN:
                if re.search(r'\b' + re.escape(word) + r'\b', text.lower()):
                    errs.append(f'{rid}: forbidden word {word!r}')
        refs = [r['parent_id'], *r.get('prerequisites', [])]
        for ref in refs:
            if ref in by_id:
                if int(ref[4:]) >= int(rid[4:]):
                    errs.append(f'{rid}: {ref} must precede it')
                ref_stage = by_id[ref]['stage']
            elif ref in records_by_id and records_by_id[ref].get('source_slice') != SLICE:
                ref_stage = records_by_id[ref]['stage']
            elif lint_range and lint_range[0] <= int(ref[4:]) <= lint_range[1] and int(ref[4:]) < int(rid[4:]):
                continue
            else:
                errs.append(f'{rid}: unknown reference {ref}')
                continue
            if ref_stage in rank and r['stage'] in rank and rank[ref_stage] > rank[r['stage']]:
                errs.append(f'{rid}: {ref} sits in a later stage ({ref_stage})')
        parent_pinned = paths.get(r['parent_id']) in pinned
        if parent_pinned != bool(r.get('pinned_parent')):
            errs.append(f'{rid}: pinned_parent must be {parent_pinned} for {r["parent_id"]}')
        if len(set(r.get('prerequisites', []))) != len(r.get('prerequisites', [])) or \
                r['parent_id'] in r.get('prerequisites', []):
            errs.append(f'{rid}: prerequisites repeat a reference')
        for tier, _ in TIERS:
            entries = r['witnesses'].get(tier, [])
            if not entries:
                errs.append(f'{rid}: witness tier {tier} is empty; use an absent entry')
            for e in entries:
                if 'absent' not in e and (e.get('root') not in ROOTS or not e.get('path')):
                    errs.append(f'{rid}: bad {tier} witness {e}')
        if not r.get('sources'):
            errs.append(f'{rid}: no cited source')
        for s in r.get('sources', []):
            if s.get('root') not in ROOTS or not s.get('path') or not re.match(r'^\d+(-\d+)?$', s.get('lines', '')) \
                    or not s.get('quote'):
                errs.append(f'{rid}: bad source {s}')
        dag = r.get('dag')
        if dag is not None and 'reuse' not in dag:
            status = dag.get('status')
            if status not in STATUS_PAIRS.get(r['record_status'], set()):
                errs.append(f'{rid}: paper status {r["record_status"]} cannot pair with node status {status}')
            local_lean = [e for e in r['witnesses']['lean'] if 'absent' not in e and e['root'] != 'github19l']
            if status == 'PROVED_LEAN' and not local_lean:
                errs.append(f'{rid}: PROVED_LEAN needs a Lean witness in this checkout or the_symbol_game')
            if status == 'CONDITIONAL' and not r.get('imports'):
                errs.append(f'{rid}: CONDITIONAL needs a named import')
            if not dag.get('source_status'):
                errs.append(f'{rid}: dag.source_status missing')
    return errs


def dag_node_of(record_id, by_id, records_by_id, node_ids, depth=0) -> list[str]:
    """DAG nodes standing for a record; an unmapped record stands in for its nearest mapped ancestor."""
    if depth > 600 or record_id is None:
        return []
    if record_id in by_id:
        r = by_id[record_id]
        dag = r.get('dag')
        if dag is not None:
            return [dag['reuse']] if 'reuse' in dag else [node_id(r)]
        return dag_node_of(r['parent_id'], by_id, records_by_id, node_ids, depth + 1)
    old = records_by_id.get(record_id)
    if old is None:
        return []
    mapped = [x for x in old.get('existing_derivation_dag_ids', []) if x in node_ids]
    if mapped:
        return mapped[:1]
    return dag_node_of(old.get('parent_id'), by_id, records_by_id, node_ids, depth + 1)


def render_jsonl_record(r, manifest, by_id, records_by_id, node_ids):
    dag = r.get('dag')
    if dag is None:
        dag_ids = []
    elif 'reuse' in dag:
        dag_ids = [dag['reuse']]
    else:
        dag_ids = [node_id(r), ROUTE_PREFIX + r['name'].upper()]
    f004 = sorted({e['path'] for e in [*r['sources'], *[w for t, _ in TIERS for w in r['witnesses'][t]]]
                   if 'absent' not in e and e['root'] == 'symbol_game' and 'F004_papers' in e['path']})
    record = {
        'coda_atlas_ids': r.get('coda_atlas_ids', []),
        'coda_atlas_paths': r.get('coda_atlas_paths', []),
        'existing_derivation_dag_ids': dag_ids,
        'f004_refs': f004,
        'id': r['id'],
        'lean4': [ref_string(e, manifest, jsonl=True) for e in r['witnesses']['lean']],
        'local_id': node_id(r) if dag_ids and dag_ids[0] == node_id(r) else NODE_PREFIX + r['id'][4:],
        'name': r['name'],
        'obligation': r['obligation'],
        'parent_id': r['parent_id'],
        'python': [ref_string(e, manifest, jsonl=True) for e in r['witnesses']['python']],
        'record_status': r['record_status'],
        'rust': [ref_string(e, manifest, jsonl=True) for e in r['witnesses']['rust']],
        'source_slice': SLICE,
        'stage': r['stage'],
        'summary': r['summary'],
        'uuid': record_uuid(r['id']),
    }
    return record


def link(from_paper: str, to_paper: str, label: str) -> str:
    return f'[{label}]({posixpath.relpath(to_paper, posixpath.dirname(from_paper))})'


def render_paper(r, manifest, all_paths, children, names):
    paper = all_paths[r['id']]
    parent = r['parent_id']
    out = [f'# [{r["id"]}] {r["name"]}', '',
           f'> **Stage**: `{r["stage"]}` | **Status**: `{r["record_status"]}`  ',
           f'> **UUID**: `{record_uuid(r["id"])}`  ',
           f'> **Parent Derivation**: {link(paper, all_paths[parent], parent)}', '', '---', '',
           '## 1. Abstract & Formal Statement', '', r['summary'], '', '### Governing Obligation',
           r['obligation'], '', '---', '', '## 2. Derivation Context & Mathematical Grounding', '',
           CONTEXT.rstrip('\n'), '']
    if r.get('imports'):
        out += ['### Admitted Structural Imports', *[f'- **Admitted**: `{x}`' for x in r['imports']], '']
    if r.get('prerequisites'):
        out += ['### Further Prerequisites',
                *[f'- {link(paper, all_paths[p], p)} {names[p]}' for p in r['prerequisites']], '']
    out += ['### Epistemic Bottlenecks & Falsification Fences', '> [!WARNING]', f'> {r["fence"]}', '', '---', '',
            '## 3. Multi-Tier Code & Proof Witnesses', '']
    for tier, heading in TIERS:
        items = []
        for e in r['witnesses'][tier]:
            url = ref_url(e, manifest, paper)
            label = ref_label(e, manifest)
            items.append(f'- [`{label}`]({url})' if url else f'- `missing obligation: {label}`')
        out += [f'### {heading}', *sorted(items), '']
    out += ['---', '', '## 4. Downstream Derivations (Outgoing DAG Links)', '']
    kids = children.get(r['id'], [])
    out += [f'- {link(paper, all_paths[k], k)}' for k in kids] or \
        ['*None (Leaf or Terminal derivation in current tree)*']
    out += ['', '---', '', '## 5. Audit Trail & Primary Source Lineage', '']
    if r.get('coda_atlas_ids'):
        out.append('- **Atlas Lineage**: ' + ', '.join(f'`{x}`' for x in r['coda_atlas_ids']))
    if r.get('coda_atlas_paths'):
        out += ['- **Primary Source Paths**:', *[f'  - `{x}`' for x in r['coda_atlas_paths']]]
    out += ['- **Cited Source Lines**:', *[f'  - `{ref_label(s, manifest)}`' for s in r['sources']]]
    return '\n'.join(out) + '\n'


SECTION4 = re.compile(r'(## 4\. Downstream Derivations \(Outgoing DAG Links\)(?:\r?\n))(.*?)((?:\r?\n)---(?:\r?\n))',
                      re.S)


def patch_section4(text: str, paper: str, owned_ids: set[str], kids: list[str], all_paths) -> str:
    """Rebuild section 4 of an unpinned parent: its own bullets, then this fragment's children."""
    match = SECTION4.search(text)
    if match is None:
        raise ValueError('section 4 not found in ' + paper)
    # Some papers mix endings; section 4 keeps the ending of its own heading line.
    eol = '\r\n' if match.group(1).endswith('\r\n') else '\n'
    lines = [ln for ln in match.group(2).splitlines() if ln.strip()]
    kept = [ln for ln in lines if not ln.startswith('*None') and
            not any(f'[{k}]' in ln for k in owned_ids)]
    bullets = kept + [f'- {link(paper, all_paths[k], k)}' for k in kids]
    body = eol + eol.join(bullets or ['*None (Leaf or Terminal derivation in current tree)*']) + eol
    return text[:match.start(2)] + body + text[match.end(2):]


def render_dag_node(r, manifest):
    dag = r['dag']
    paper = new_paper_path(r)
    source = [paper, *[ref_string(s, manifest) for s in r['sources']]]
    node = {
        'id': node_id(r),
        'stage': DAG_STAGE[r['stage']],
        'status': dag['status'],
        'source_status': dag['source_status'],
        'statement': r['summary'],
        'source': source,
        'lean': [ref_string(e, manifest) for e in r['witnesses']['lean'] if 'absent' not in e],
        'rust': [ref_string(e, manifest) for e in r['witnesses']['rust'] if 'absent' not in e],
        'imported_structure': list(r.get('imports', [])),
        'bottleneck': r['fence'],
        'tags': [TAG, r['id'], r['stage'].lower()],
    }
    if any(e.get('root') == 'github19l' for e in r['witnesses']['lean']):
        node['tags'].append('external-lean-github')
    return node


def render_route(r, manifest, inputs):
    return {
        'id': ROUTE_PREFIX + r['name'].upper(),
        'inputs': inputs,
        'output': node_id(r),
        'status': ROUTE_STATUS[r['dag']['status']],
        'source': [new_paper_path(r), *[ref_string(s, manifest) for s in r['sources'][:2]]],
    }


def readme_section(stage, records, all_paths):
    folder = STAGE_FOLDERS[stage]
    rows = []
    for r in records:
        paper = all_paths[r['id']].removeprefix('dag/derivations/')
        if r['parent_id'] is None:
            parent = '`root`'
        else:
            parent = f'[`{r["parent_id"]}`](./{all_paths[r["parent_id"]].removeprefix("dag/derivations/")})'
        rows.append(f'| [`{r["id"]}`](./{paper}) | {r["name"]} | `{r["record_status"]}` | {parent} |')
    return (f'### {stage} ({len(records)} derivations)\n\nFolder: [`{folder}/`](./{folder}/)\n\n'
            '| ID | Name | Status | Parent |\n|---|---|---|---|\n' + '\n'.join(rows) + '\n')


ROUTE_STAGES = ('PREGENESIS', 'GENESIS', 'FINITE_OBSTRUCTION', 'AUTHORIZATION', 'MSSN_SN', 'WDP')
ROUTE_FILE = 'dag/derivations/PREGENESIS_TO_WDP_ROUTE.md'


def route_index(all_records, all_paths, owned: set[str]) -> str:
    """Reading order: a depth-first walk of the parent tree from TFQ-0000 over the route stages."""
    by_id = {r['id']: r for r in all_records}
    kids: dict[str, list[str]] = {}
    for r in all_records:
        if r['parent_id'] and r['stage'] in ROUTE_STAGES:
            kids.setdefault(r['parent_id'], []).append(r['id'])
    order, stack = [], ['TFQ-0000']
    while stack:
        cur = stack.pop()
        order.append(cur)
        stack.extend(sorted(kids.get(cur, []), reverse=True))
    missed = sorted(r['id'] for r in all_records if r['stage'] in ROUTE_STAGES and r['id'] not in set(order))
    # A parent's stage never ranks after its child's, so a stable sort by stage keeps parents first.
    order.sort(key=lambda rid: ROUTE_STAGES.index(by_id[rid]['stage']))

    def row(i, rid):
        r = by_id[rid]
        paper = all_paths[rid].removeprefix('dag/derivations/')
        parent = r['parent_id'] or 'root'
        mark = ' (new)' if rid in owned else ''
        return f'| {i} | [`{rid}`](./{paper}){mark} | {r["name"]} | `{r["stage"]}` | `{r["record_status"]}` | `{parent}` |'

    counts = ''.join(
        f'| `{s}` | {sum(1 for x in order if by_id[x]["stage"] == s and x not in owned)} | '
        f'{sum(1 for x in order if by_id[x]["stage"] == s and x in owned)} |\n' for s in ROUTE_STAGES)
    text = ('# Route: pre-genesis to WDP\n\n'
            '**AuthorityEffect:** None. Generated by `dag/sync_pregenesis_to_wdp.py` from '
            '`dag/theory_of_finite_qm.jsonl`; do not edit by hand.\n\n'
            'Every derivation paper on the route from the inert inscription `<>` (`TFQ-0000`) through Genesis, '
            'its expansion past the `dbccpage/19L57G1` freeze, S(n), MSS-N and WDP, in reading order: stage '
            'by stage (PREGENESIS, GENESIS, FINITE_OBSTRUCTION, AUTHORIZATION, MSSN_SN, WDP), and within a '
            'stage a depth-first walk of the parent tree from `TFQ-0000`, children in id order, so every '
            'parent precedes its children. A paper\'s further '
            'prerequisites are listed in its section 2. Records marked (new) come from '
            '[`fragments/pregenesis_to_wdp.json`](../fragments/pregenesis_to_wdp.json). A status records what '
            'the cited source establishes; OPEN_OBLIGATION and GAP rows are open.\n\n'
            '| Stage | Existing papers | New papers |\n|---|---|---|\n' + counts + '\n'
            '| # | ID | Name | Stage | Status | Parent |\n|---|---|---|---|---|---|\n' +
            '\n'.join(row(i + 1, rid) for i, rid in enumerate(order)) + '\n')
    if missed:
        text += ('\n## Route-stage papers not reached from TFQ-0000 by parent links\n\n'
                 '| # | ID | Name | Stage | Status | Parent |\n|---|---|---|---|---|---|\n' +
                 '\n'.join(row(i + 1, rid) for i, rid in enumerate(missed)) + '\n')
    return text


def generated_files(root: Path = ROOT):
    manifest = load_manifest(root)
    recs = manifest['records']
    by_id = {r['id']: r for r in recs}
    dag = views.load_dag(root)
    old_records = dag['records']
    records_by_id = {r['id']: r for r in old_records}
    pinned = pinned_papers(root)
    disk_paths = paper_paths(root)
    errs = validate_manifest(manifest, records_by_id, pinned, disk_paths)
    if errs:
        raise ValueError('manifest invalid:\n  ' + '\n  '.join(errs))

    all_paths = {k: v for k, v in disk_paths.items() if k not in by_id}
    for r in recs:
        all_paths[r['id']] = new_paper_path(r)
    names = {r['id']: r['name'] for r in old_records} | {r['id']: r['name'] for r in recs}
    children: dict[str, list[str]] = {}
    for r in recs:
        children.setdefault(r['parent_id'], []).append(r['id'])

    old_node_ids = {n['id'] for n in dag['nodes'] if TAG not in n.get('tags', [])}
    new_ids = {node_id(r) for r in recs if r.get('dag') and 'reuse' not in r['dag']}
    if old_node_ids & new_ids:
        raise ValueError('new node collides with an existing node: ' + ', '.join(sorted(old_node_ids & new_ids)))
    node_ids = old_node_ids | new_ids
    for r in recs:
        if r.get('dag') and 'reuse' in r['dag'] and r['dag']['reuse'] not in old_node_ids:
            raise ValueError(f'{r["id"]}: reused node {r["dag"]["reuse"]} is not in the DAG')

    # Records: drop this slice, splice its block before the application block.
    new_records = [render_jsonl_record(r, manifest, by_id, records_by_id, node_ids) for r in recs]
    kept = [r for r in old_records if r.get('source_slice') != SLICE]
    at = next((i for i, r in enumerate(kept) if r.get('source_slice') == 'application_branches'), len(kept))
    all_records = kept[:at] + new_records + kept[at:]
    dag['records'] = [views.canonical_record(r) for r in all_records]

    # DAG: drop this fragment's nodes and routes, splice new blocks before the application blocks.
    nodes = [n for n in dag['nodes'] if TAG not in n.get('tags', [])]
    routes = [x for x in dag['routes'] if not x['id'].startswith(ROUTE_PREFIX)]
    new_nodes, new_routes = [], []
    for r in recs:
        if not r.get('dag') or 'reuse' in r['dag']:
            continue
        inputs = []
        for ref in [r['parent_id'], *r.get('prerequisites', [])]:
            for n in dag_node_of(ref, by_id, records_by_id, node_ids):
                if n not in inputs and n != node_id(r):
                    inputs.append(n)
        if not inputs:
            inputs = ['PG-INERT-DIAMOND']
        new_nodes.append(render_dag_node(r, manifest))
        new_routes.append(render_route(r, manifest, inputs))
    ni = next((i for i, n in enumerate(nodes) if 'application-branch' in n.get('tags', [])), len(nodes))
    ri = next((i for i, x in enumerate(routes) if x['id'].startswith('APP-R-')), len(routes))
    dag['nodes'] = nodes[:ni] + new_nodes + nodes[ni:]
    dag['routes'] = routes[:ri] + new_routes + routes[ri:]
    dag['segment_notes'][SLICE] = [manifest['segment_note']]

    # Papers: render new ones; rebuild section 4 of unpinned parents.
    outputs: dict[Path, bytes] = {}
    for r in recs:
        outputs[root / all_paths[r['id']]] = render_paper(r, manifest, all_paths, children, names).encode('utf-8')
    owned = set(by_id)
    for parent, kids in sorted(children.items()):
        if parent in by_id:
            continue
        path = disk_paths[parent]
        if path in pinned:
            continue
        text = (root / path).read_bytes().decode('utf-8')
        outputs[root / path] = patch_section4(text, path, owned, kids, all_paths).encode('utf-8')
    # An unpinned parent that lost all its fragment children returns to its own bullets.
    for rid, path in disk_paths.items():
        if rid in by_id or rid in children or path in pinned:
            continue
        text = (root / path).read_bytes().decode('utf-8')
        if any(f'[{k}]' in text.split('## 4. Downstream', 1)[-1].split('## 5.', 1)[0] for k in owned):
            outputs[root / path] = patch_section4(text, path, owned, [], all_paths).encode('utf-8')

    # README: regenerate the five owned stage sections and the pinned-children block.
    readme = (root / 'dag/derivations/README.md').read_text(encoding='utf-8')
    order = ['PREGENESIS', 'GENESIS', 'FINITE_OBSTRUCTION', 'AUTHORIZATION', 'MSSN_SN', 'WDP', 'L1_EMERGENCE']
    for stage in OWNED_STAGES:
        stage_records = [r for r in all_records if r['stage'] == stage and r.get('source_slice') != 'application_branches']
        start = re.search(r'^### ' + stage + r' \(\d+ derivations\)\n', readme, re.M).group(0)
        nxt = order[order.index(stage) + 1]
        i = readme.index(start)
        j = readme.index(f'\n### {nxt} (', i) + 1
        readme = readme[:i] + readme_section(stage, stage_records, all_paths) + '\n' + readme[j:]
    head, marker, tail = readme.partition(APP_MARKER)
    if PINNED_BEGIN in head:
        head = head[:head.index(PINNED_BEGIN)]
    head = head.rstrip() + '\n'
    pinned_rows = [(r['parent_id'], r['id']) for r in recs if r.get('pinned_parent')]
    if recs:
        head += ('\n' + PINNED_BEGIN + '\n\n### Pre-genesis to WDP route\n\n'
                 'The [route index](./PREGENESIS_TO_WDP_ROUTE.md) lists every paper from `<>` through Genesis, '
                 'its expansion, S(n), MSS-N and WDP in reading order.\n')
        if pinned_rows:
            head += ('\n### Children recorded for custody-pinned papers\n\n'
                     'Section 4 of a custody-pinned paper is not rewritten. These children name it as parent.\n\n'
                     '| Pinned parent | Child |\n|---|---|\n' +
                     ''.join(f'| [`{p}`](./{all_paths[p].removeprefix("dag/derivations/")}) | '
                             f'[`{c}`](./{all_paths[c].removeprefix("dag/derivations/")}) |\n'
                             for p, c in pinned_rows))
        head += '\n' + PINNED_END + '\n'
    readme = head + ('\n' + marker + tail if marker else '')

    # theory_of_finite_qm.md: the renderer lists the owned stages (views.PLAIN_STAGES) in the plain layout.
    if tuple(OWNED_STAGES) != views.PLAIN_STAGES:
        raise ValueError('render_dag_views.PLAIN_STAGES must be the stages this sync owns')

    outputs[root / ROUTE_FILE] = route_index(all_records, all_paths, owned).encode('utf-8')
    outputs.update(views.outputs(dag, root))  # derivation_dag.json and the two views rendered from it
    outputs[root / 'dag/derivations/README.md'] = readme.encode('utf-8')
    return outputs


def lint(parts: list[Path], root: Path = ROOT) -> list[str]:
    """Validate partial batches together with the manifest's records, without writing."""
    manifest = load_manifest(root)
    old_records = read_records(root)
    records = list(manifest['records'])
    for part in parts:
        records += json.loads(part.read_text(encoding='utf-8'))['records']
    records.sort(key=lambda r: r['id'])
    merged = dict(manifest, records=records)
    planned = (int(manifest['first_id'][4:]), int(manifest.get('planned_last_id', 'TFQ-9999')[4:]))
    return validate_manifest(merged, {r['id']: r for r in old_records}, pinned_papers(root),
                             paper_paths(root), lint_range=planned)


def merge(parts: list[Path], root: Path = ROOT) -> int:
    """Fold batch files into the manifest (replacing records with the same id) and write it."""
    manifest = load_manifest(root)
    records = {r['id']: r for r in manifest['records']}
    for part in parts:
        for r in json.loads(part.read_text(encoding='utf-8'))['records']:
            records[r['id']] = r
    manifest['records'] = [records[k] for k in sorted(records)]
    (root / 'dag/fragments/pregenesis_to_wdp.json').write_bytes(json_text(manifest).encode('utf-8'))
    return len(manifest['records'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--lint', type=Path, nargs='+', help='validate partial batch files; write nothing')
    parser.add_argument('--merge', type=Path, nargs='+', help='fold batch files into the manifest')
    args = parser.parse_args()
    if args.merge:
        print(f'manifest records={merge(args.merge)}')
        return 0
    if args.lint:
        errs = lint(args.lint)
        for err in errs:
            print('FAIL', err)
        print(f'lint failures={len(errs)}')
        return int(bool(errs))
    differences = []
    for path, expected in generated_files(ROOT).items():
        if not path.exists() or path.read_bytes() != expected:
            differences.append(path.relative_to(ROOT).as_posix())
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(expected)
    print('stale=' + ','.join(differences) if differences else 'pregenesis-to-wdp fragment synchronized')
    return int(bool(differences) and args.check)


if __name__ == '__main__':
    raise SystemExit(main())
