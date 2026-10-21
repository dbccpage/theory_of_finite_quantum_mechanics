"""Join derivation_dag.json and theory_of_finite_qm.jsonl into one derivation graph.

The DAG (nodes and routes) and the TFQ tree (records joined by parent_id) were kept
apart: some records named no DAG node and some nodes had no record. The fragment
dag/fragments/unified_dag.json owns the join:

- every record that names no node of the other two fragments' or the base DAG gets a node
  with the record's id (tag unified-dag) and a route from the node of its parent record;
- every node that no record names gets a record TFQ-1000 upward (source_slice unified_dag)
  and a derivation paper;
- alias links append an existing node id to a base record that restates it;
- the master-ledger packet crosswalk is carried as packet: tags on the nodes;
- the audited source-corpus records (FSP, MUB6, Majorana, Dressing Field Method) are written
  into the application-branch fragment, with their papers, and their trunk restatements are
  carried as alias: tags on the trunk nodes.

Run order: sync_pfp_results.py, then this script, then sync_application_branches.py, then
sync_pregenesis_to_wdp.py; --check on all four is then clean. --check detects stale generated data
without writing. The pfp_review object that sync_pfp_results.py writes onto a base node is carried
through here: a record generated from such a node copies pfp_review_refs, and the crosswalk table has
a Review column.
AuthorityEffect: None. Synchronization does not establish a mathematical claim, and no
status is promoted: a record's status is mapped to the nearest DAG status, never upward.
"""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SLICE = 'unified_dag'
TAG = 'unified-dag'
DOMAIN_TAG = 'source-corpus'
ROUTE_PREFIX = 'UDG-R-'
DOMAIN_ROUTE_PREFIX = 'APP-R-'
OWNED_TAG_PREFIXES = ('alias:', 'packet:')
UUID_NAMESPACE = uuid.uuid5(
    uuid.NAMESPACE_URL,
    'https://github.com/dbccpage/theory_of_finite_quantum_mechanics/dag/theory_of_finite_qm.jsonl')
XWALK_BEGIN = '<!-- unified-dag:crosswalk:begin -->'
XWALK_END = '<!-- unified-dag:crosswalk:end -->'
APP_MARKER = '<!-- application-branches: generated from fragments/application_branches.json -->'
STAGE_FOLDERS = {
    'PREGENESIS': '01_pregenesis', 'GENESIS': '02_genesis', 'FINITE_OBSTRUCTION': '03_finite_obstruction',
    'AUTHORIZATION': '04_authorization', 'MSSN_SN': '05_mssn_sn', 'WDP': '06_wdp',
    'L1_EMERGENCE': '07_l1_emergence', 'L1_TO_L2': '08_l1_to_l2', 'FINITE_HILBERT': '09_finite_hilbert',
    'FINITE_QM_CORE': '10_finite_qm_core', 'FINITE_QM_DYNAMICS': '11_finite_qm_dynamics',
    'FINITE_QM_STRUCTURE': '12_finite_qm_structure', 'FINITE_QM_INFORMATION': '13_finite_qm_information',
    'FINITE_GAUGE': '14_finite_gauge', 'FINITE_QED': '15_finite_qed', 'FINITE_ELECTROWEAK': '16_finite_electroweak',
    'FINITE_QCD': '17_finite_qcd', 'FINITE_TOPOLOGICAL': '18_finite_topological', 'FINITE_QG': '19_finite_qg',
    'CONTINUUM_INTERFACE': '20_continuum_interface', 'IMPLEMENTATION_CORE': '21_implementation_core',
    'IMPLEMENTATION_SIBLING': '22_implementation_sibling', 'ENGINE_CUSTODY': '23_engine_custody',
    'DRESSING_FIELD': '24_dressing_field', 'MUTUALLY_UNBIASED_BASES': '25_mub', 'FERMION_SIGN': '26_fsp',
    'TENSOR_COMPOSITION': '27_tensor_composition', 'MAJORANA': '28_majorana',
    'COMPUTATION': '29_computation',
}
# DAG stage of a record of each TFQ stage, and TFQ stage of a node of each DAG stage.
DAG_STAGE = {stage: stage for stage in STAGE_FOLDERS}
RECORD_STAGE = {stage: stage for stage in STAGE_FOLDERS} | {'IMPLEMENTATION': 'IMPLEMENTATION_CORE'}
# TFQ record status -> DAG node status. Fence labels of a source slice carry no derivation status.
NODE_STATUS = {
    'DEFINITION': 'DEFINITION', 'PROVED_LEAN': 'PROVED_LEAN', 'PROVED_PROSE': 'PROVED_PROSE',
    'CONDITIONAL': 'CONDITIONAL', 'COMPUTATIONAL_CONTROL': 'COMPUTATIONALLY_CHECKED',
    'OPEN_OBLIGATION': 'OPEN', 'GAP': 'OPEN', 'OPEN_OBLIGATIONS': 'OPEN', 'OPEN_ADJOINING': 'OPEN',
    'OPEN_COMPLETION': 'OPEN', 'OPEN_BRIDGE': 'OPEN', 'OPEN_INTERFACE': 'OPEN',
    'IMPORTED_ASSUMPTION': 'IMPORTED_ASSUMPTION', 'ADMITTED_PRIMITIVE': 'ADMITTED_PRIMITIVE',
}
RECORD_STATUS = {
    'DEFINITION': 'DEFINITION', 'PROVED_LEAN': 'PROVED_LEAN', 'PROVED_PROSE': 'PROVED_PROSE',
    'CONDITIONAL': 'CONDITIONAL', 'COMPUTATIONALLY_CHECKED': 'COMPUTATIONAL_CONTROL', 'OPEN': 'OPEN_OBLIGATION',
    'IMPORTED_ASSUMPTION': 'IMPORTED_ASSUMPTION', 'ADMITTED_PRIMITIVE': 'ADMITTED_PRIMITIVE',
    'SOURCE_RECORD': 'SOURCE_RECORD', 'REFUTED': 'REFUTED',
}
ROUTE_STATUS = {
    'PROVED_LEAN': 'DERIVED_LEAN', 'PROVED_PROSE': 'DERIVED_PROSE', 'DEFINITION': 'DERIVED_PROSE',
    'REFUTED': 'DERIVED_PROSE', 'COMPUTATIONALLY_CHECKED': 'COMPUTED', 'CONDITIONAL': 'CONDITIONAL_ON_IMPORT',
    'IMPORTED_ASSUMPTION': 'CONDITIONAL_ON_IMPORT', 'ADMITTED_PRIMITIVE': 'RECORD_PARENT',
    'SOURCE_RECORD': 'RECORD_PARENT', 'OPEN': 'GAP_NO_DERIVATION',
}
NEW_STAGES = ('FINITE_OBSTRUCTION', 'AUTHORIZATION', 'FINITE_HILBERT', 'FINITE_QM_INFORMATION', 'FINITE_GAUGE',
              'FINITE_QED', 'FINITE_ELECTROWEAK', 'FINITE_QCD', 'FINITE_TOPOLOGICAL', 'FINITE_QG',
              'CONTINUUM_INTERFACE', 'IMPLEMENTATION_CORE', 'IMPLEMENTATION_SIBLING', 'ENGINE_CUSTODY', 'MAJORANA',
              'COMPUTATION')
FORBIDDEN = ('proves', 'guarantees', 'mathematically verifies', 'fundamentally', 'true intelligence',
             'impossible', 'universal', 'flawless', 'perfectly', 'clearly', 'obviously', 'simply',
             'merely', 'weaponized')
LEGEND_SOURCE_RECORD = ('a step the cited source records, or a fence label from a TFQ source slice; the DAG '
                        'assigns it no derivation status')
EDGE_RECORD_PARENT = ('RECORD_PARENT marks the TFQ tree link from a record to its parent record; it asserts '
                      'reading order, not a derivation.')


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def record_line(record, newline):
    return json.dumps(record, ensure_ascii=False, sort_keys=True) + newline


def record_uuid(record_id: str) -> str:
    return str(uuid.uuid5(UUID_NAMESPACE, record_id))


def slug(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')[:80]


def forbidden_words(text: str) -> list[str]:
    low = text.lower()
    return [w for w in FORBIDDEN if re.search(r'\b' + re.escape(w) + r'\b', low)]


def resolves(root: Path, ref: str) -> bool:
    """A local reference resolves when its path exists and its leaf symbol occurs in the file."""
    if ref.startswith(('external:', 'pr:', 'absent')):
        return True
    path, _, symbol = ref.partition('::')
    path = re.sub(r':\d+(?:[-,]\d+)*$', '', path.split('#', 1)[0])
    target = root / path
    if not target.exists():
        return False
    if not symbol or not target.is_file():
        return True
    leaf = symbol.split('::')[-1].split('.')[-1]
    return leaf in target.read_text(encoding='utf-8', errors='replace')


def paper_paths(root: Path) -> dict[str, str]:
    paths = {}
    for p in (root / 'dag/derivations').rglob('tfq_*.md'):
        key = re.match(r'tfq_(\d{4})_', p.name)
        if key:
            paths['TFQ-' + key[1]] = p.relative_to(root).as_posix()
    return paths


def link(from_paper: str, to_paper: str, label: str) -> str:
    return f'[{label}]({posixpath.relpath(to_paper, posixpath.dirname(from_paper))})'


# ---------------------------------------------------------------------------------------------
# Strip: remove everything this fragment owns, so generation starts from the other owners' data.

def strip_owned(dag, records, fragment, app):
    alias_ids = {rid: set(v) for rid, v in fragment['row_aliases'].items()}
    nodes = []
    for n in dag['nodes']:
        if TAG in n.get('tags', []):
            continue
        n = dict(n)
        n['tags'] = [t for t in n.get('tags', []) if not t.startswith(OWNED_TAG_PREFIXES)]
        nodes.append(n)
    dag['nodes'] = nodes
    dag['routes'] = [r for r in dag['routes'] if not r['id'].startswith(ROUTE_PREFIX)]
    owned_rows = {r['id'] for r in records if r.get('source_slice') == SLICE}
    owned_nodes = {r['id'] for r in records}  # unified nodes carry the record id
    kept = []
    for r in records:
        if r['id'] in owned_rows:
            continue
        ids = r['existing_derivation_dag_ids']
        drop = alias_ids.get(r['id'], set()) | ({r['id']} & owned_nodes)
        if any(x in drop for x in ids):
            r = dict(r, existing_derivation_dag_ids=[x for x in ids if x not in drop])
        kept.append(r)
    domain_nodes = {n['id'] for n in app['nodes'] if DOMAIN_TAG in n.get('tags', [])}
    app['nodes'] = [n for n in app['nodes'] if n['id'] not in domain_nodes]
    app['records'] = [r for r in app['records'] if r['existing_derivation_dag_ids'][0] not in domain_nodes]
    app['routes'] = [r for r in app['routes'] if r['output'] not in domain_nodes]
    app['stages'] = [s for s in app['stages'] if s not in fragment.get('domain_stages_added', [])]
    return kept


# ---------------------------------------------------------------------------------------------
# Generation.

def node_for_record(r, root, paths, parent_node):
    status = NODE_STATUS.get(r['record_status'], 'SOURCE_RECORD')
    lean = [x for x in r['lean4'] if not x.startswith('absent')]
    rust = [x for x in r['rust'] if not x.startswith('absent')]
    good_lean = [x for x in lean if resolves(root, x)]
    good_rust = [x for x in rust if resolves(root, x)]
    dropped = len(lean) + len(rust) - len(good_lean) - len(good_rust)
    paper = paths[r['id']]
    source = [paper] + [x for x in r.get('f004_refs', []) if x != paper and resolves(root, x)]
    source_status = f"TFQ record_status {r['record_status']} (source slice {r['source_slice']})"
    if status == 'SOURCE_RECORD' and r['record_status'] != 'SOURCE_RECORD':
        source_status += '; a fence label of that slice, carried without a derivation status'
    if dropped:
        source_status += f'; {dropped} cited witness path(s) do not resolve in this checkout and are not listed'
    node = {
        'id': r['id'], 'stage': DAG_STAGE[r['stage']], 'status': status, 'source_status': source_status,
        'statement': r['summary'], 'source': source, 'lean': good_lean, 'rust': good_rust,
        'imported_structure': [], 'bottleneck': r['obligation'], 'tags': [TAG, r['id'], r['stage'].lower()],
    }
    route = None
    if parent_node is not None:
        route = {'id': ROUTE_PREFIX + r['id'], 'inputs': [parent_node], 'output': r['id'],
                 'status': ROUTE_STATUS[status], 'source': [paper]}
    return node, route


def record_for_node(n, rid, parent_id, root):
    stage = RECORD_STAGE[n['stage']]
    local = [x for x in n['source'] if not x.startswith(('external:', 'pr:')) and resolves(root, x)]
    paper = f'dag/derivations/{STAGE_FOLDERS[stage]}/tfq_{rid[4:]}_{slug(n["id"])}.md'
    record = {
        'coda_atlas_ids': [], 'coda_atlas_paths': [], 'existing_derivation_dag_ids': [n['id']],
        'f004_refs': [paper] + [x for x in local if x != paper], 'id': rid, 'lean4': list(n['lean']),
        'local_id': n['id'], 'name': n['id'].lower(), 'obligation': n['bottleneck'], 'parent_id': parent_id,
        'python': [], 'record_status': RECORD_STATUS[n['status']], 'rust': list(n['rust']),
        'source_slice': SLICE, 'stage': stage, 'summary': n['statement'], 'uuid': record_uuid(rid),
    }
    refs = n.get('pfp_review', {}).get('review_refs')
    if refs:  # written onto the node by sync_pfp_results.py, which runs first
        record['pfp_review_refs'] = list(refs)
    return record, paper


def render_paper(r, n, paper, parent_paper, kids):
    out = [f'# [{r["id"]}] {n["id"]}', '',
           f'> **Stage**: `{r["stage"]}` | **Status**: `{r["record_status"]}` | **DAG node**: `{n["id"]}` (`{n["status"]}`)  ',
           f'> **UUID**: `{r["uuid"]}`  ',
           f'> **Parent Derivation**: {link(paper, parent_paper, r["parent_id"])}', '',
           '*Generated by `dag/sync_unified_dag.py` from the DAG node so that the node has a record in the '
           'TFQ tree; edit the node, not this paper.*', '', '---', '',
           '## 1. Abstract & Formal Statement', '', n['statement'], '', '### Governing Obligation',
           n['bottleneck'], '', '### Source Status', n['source_status'], '', '---', '',
           '## 2. Derivation Context', '']
    if n.get('imported_structure'):
        out += ['### Admitted Structural Imports', *[f'- **Admitted**: `{x}`' for x in n['imported_structure']], '']
    if n.get('see_also'):
        out += ['### See Also', *[f'- `{x}`' for x in n['see_also']], '']
    out += ['---', '', '## 3. Multi-Tier Code & Proof Witnesses', '', '### Lean 4 Theorems',
            *([f'- `{x}`' for x in n['lean']] or ['- *none cited*']), '', '### Rust Certifiers',
            *([f'- `{x}`' for x in n['rust']] or ['- *none cited*']), '', '---', '',
            '## 4. Downstream Derivations (Outgoing DAG Links)', '']
    out += [f'- `{k}`' for k in kids] or ['*None (Leaf or Terminal derivation in current tree)*']
    out += ['', '---', '', '## 5. Audit Trail & Primary Source Lineage', '', '- **Cited Sources**:',
            *[f'  - `{x}`' for x in n['source']]]
    return '\n'.join(out) + '\n'


def prose(text: str) -> str:
    """Mathematical text such as u_T[A](v) must not read as a Markdown link."""
    return text.replace('](', ']\\(')


def plain_path(ref: str) -> str:
    """A node source cites a file; line ranges stay in the paper and the record."""
    return re.sub(r':\d+(?:[-,]\d+)*$', '', ref.split('#', 1)[0])


def render_domain_paper(d, record, paper, parent_paper, kids):
    out = [f'# [{record["id"]}] {d["name"]}', '',
           f'> **Stage**: `{record["stage"]}` | **Status**: `{record["record_status"]}` | **DAG node**: `{d["node_id"]}`  ',
           f'> **UUID**: `{record["uuid"]}`  ',
           f'> **Parent Derivation**: {link(paper, parent_paper, record["parent_id"])}  ',
           f'> **Source record**: `{d["source_id"]}` in `{d["corpus"]}` (claimed status `{d.get("source_claimed_status") or "none"}`)',
           '', '*Generated by `dag/sync_unified_dag.py` from the audited corpus record in '
           '`dag/fragments/unified_dag.json`.*', '', '---', '',
           '## 1. Abstract & Formal Statement', '', prose(d['statement']), '', '### Governing Obligation',
           prose(d['obligation']), '', '### Witness Audit', prose(d.get('audit') or 'No audit note.'), '', '---', '',
           '## 2. Derivation Context', '']
    if d.get('imported_structure'):
        out += ['### Admitted Structural Imports', *[f'- **Admitted**: `{x}`' for x in d['imported_structure']], '']
    if len(d['parent_nodes']) > 1:
        out += ['### Further Prerequisites', *[f'- `{x}`' for x in d['parent_nodes'][1:]], '']
    if d.get('uses'):
        out += ['### Uses (trunk nodes this step dresses or feeds)', *[f'- `{x}`' for x in d['uses']], '']
    if d.get('see_also'):
        out += ['### See Also', *[f'- `{x}`' for x in d['see_also']], '']
    out += ['---', '', '## 3. Multi-Tier Code & Proof Witnesses', '']
    for key, head in (('lean', 'Lean 4 Theorems'), ('rust', 'Rust Certifiers'), ('python', 'Python Checks'),
                      ('external_witnesses', 'Cited by the source, not in this checkout')):
        out += [f'### {head}', *([f'- `{x}`' for x in d.get(key, [])] or ['- *none*']), '']
    out += ['---', '', '## 4. Downstream Derivations (Outgoing DAG Links)', '']
    out += [f'- {link(paper, kid_paper, kid)}' for kid, kid_paper in kids] or \
        ['*None (Leaf or Terminal derivation in current tree)*']
    out += ['', '---', '', '## 5. Audit Trail & Primary Source Lineage', '', '- **Cited Sources**:',
            *[f'  - `{x}`' for x in d['sources']]]
    return '\n'.join(out) + '\n'


def generated_files(root: Path = ROOT):
    folder = root / 'dag'
    fragment = json.loads((folder / 'fragments/unified_dag.json').read_text(encoding='utf-8'))
    app_path = folder / 'fragments/application_branches.json'
    app = json.loads(app_path.read_text(encoding='utf-8'))
    pgw_path = folder / 'fragments/pregenesis_to_wdp.json'
    pgw = json.loads(pgw_path.read_text(encoding='utf-8'))
    dag = json.loads((folder / 'derivation_dag.json').read_text(encoding='utf-8'))
    lines = (folder / 'theory_of_finite_qm.jsonl').read_bytes().decode('utf-8').splitlines(keepends=True)
    newline = '\r\n' if lines and lines[0].endswith('\r\n') else '\n'
    old_records = [json.loads(line) for line in lines]
    old_line = {r['id']: line for r, line in zip(old_records, lines)}
    records = strip_owned(dag, old_records, fragment, app)
    paths = {k: v for k, v in paper_paths(root).items()}
    errors = []

    # 0. Pre-genesis records without a node of their own get a unified node and reuse it there.
    reuse_set = set(fragment['pregenesis_reuse'])
    for rec in pgw['records']:
        if rec['id'] in reuse_set:
            rec['dag'] = {'reuse': rec['id']}

    node_ids = {n['id'] for n in dag['nodes']}
    app_node_ids = {n['id'] for n in app['nodes']}
    by_id = {r['id']: r for r in records}

    # 1. Alias links on base records.
    for rid, targets in fragment['row_aliases'].items():
        r = by_id[rid]
        for t in targets:
            if t not in node_ids:
                errors.append(f'alias target {t} of {rid} is not a DAG node')
        by_id[rid] = dict(r, existing_derivation_dag_ids=r['existing_derivation_dag_ids'] + list(targets))

    def real_ids(r):
        return [x for x in r['existing_derivation_dag_ids'] if x in node_ids or x in app_node_ids]

    # 2. A node for every base record that names none. Fragment-owned records (pre-genesis and
    #    application) get their node from their own fragment.
    fragment_slices = {'pregenesis_to_wdp', 'application_branches'}
    new_nodes, new_routes = [], []
    unified_node = {}
    for r in records:
        r = by_id[r['id']]
        if (r['source_slice'] in fragment_slices and r['id'] not in reuse_set) or real_ids(r):
            continue
        unified_node[r['id']] = r['id']

    def node_of(rid):
        r = by_id.get(rid)
        if r is None:
            return None
        if rid in unified_node:
            return rid
        ids = real_ids(r)
        if ids:
            return ids[0]
        if r['source_slice'] == 'pregenesis_to_wdp':
            return 'PGW-' + r['name'].upper()
        return None

    for r in records:
        rid = r['id']
        if rid not in unified_node:
            continue
        r = by_id[rid]
        parent = node_of(r['parent_id']) if r['parent_id'] else None
        node, route = node_for_record(r, root, paths, parent)
        new_nodes.append(node)
        if route:
            new_routes.append(route)
        by_id[rid] = dict(r, existing_derivation_dag_ids=r['existing_derivation_dag_ids'] + [rid])

    # 3. A record for every node that no record names (other fragments' records count).
    named = {x for r in by_id.values() for x in r['existing_derivation_dag_ids']}
    named |= {x for r in app['records'] for x in r['existing_derivation_dag_ids']}
    named |= {'PGW-' + r['name'].upper() for r in pgw['records'] if r.get('dag') and 'reuse' not in r['dag']}
    assigned = fragment['node_records']
    outputs: dict[Path, bytes] = {}
    node_rows = []
    nodes_by_id = {n['id']: n for n in dag['nodes']}
    incoming = {}
    for route in dag['routes']:
        incoming.setdefault(route['output'], []).append(route)
    first_record = {}
    for r in by_id.values():
        for x in r['existing_derivation_dag_ids']:
            first_record.setdefault(x, r['id'])
    for n in dag['nodes']:
        if n['id'] in named:
            continue
        if n['id'] not in assigned:
            errors.append(f'node {n["id"]} has no record; add it to node_records in unified_dag.json')
            continue
        first_record.setdefault(n['id'], assigned[n['id']]['id'])
    for nid, spec in assigned.items():
        if nid in named:
            errors.append(f'node_records entry {nid} is already named by a record')
            continue
        n = nodes_by_id.get(nid)
        if n is None:
            errors.append(f'node_records entry {nid} is not a DAG node')
            continue
        parent = spec.get('parent')
        if parent is None:
            for route in incoming.get(nid, []):
                for item in route['inputs']:
                    if item in first_record:
                        parent = first_record[item]
                        break
                if parent:
                    break
        if parent is None:
            errors.append(f'node {nid}: no parent record; give node_records.{nid}.parent')
            continue
        rec, paper = record_for_node(n, spec['id'], parent, root)
        node_rows.append((rec, n, paper))
    row_ids = {rec['id'] for rec, _, _ in node_rows}
    for rec, n, paper in node_rows:
        paths[rec['id']] = paper
    for rec, n, paper in node_rows:
        if rec['parent_id'] not in paths:
            errors.append(f'{rec["id"]}: parent {rec["parent_id"]} has no paper')
            continue
        kids = sorted(k['id'] for k, _, _ in node_rows if k['parent_id'] == rec['id'])
        outputs[root / paper] = render_paper(rec, n, paper, paths[rec['parent_id']], kids).encode('utf-8')
    if len(row_ids) != len(node_rows) or row_ids & set(by_id):
        errors.append('node_records ids collide')

    # 4. Source-corpus records into the application fragment.
    domain_nodes, domain_routes, domain_records = [], [], []
    alias_tags: dict[str, list[str]] = {}
    for a in fragment.get('domain_aliases', []):
        alias_tags.setdefault(a['alias_of'], []).append('alias:' + a['source_id'])
        if a['alias_of'] not in node_ids and a['alias_of'] not in by_id:
            errors.append(f'alias {a["source_id"]}: {a["alias_of"]} is neither a node nor a record')
    domain = fragment.get('domain_records', [])
    domain_record_of = {d['node_id']: d['record_id'] for d in domain}
    all_nodes = node_ids | app_node_ids | {d['node_id'] for d in domain} | {n['id'] for n in new_nodes}
    for d in domain:
        for text in (d['statement'], d['obligation'], d['name']):
            if forbidden_words(text):
                errors.append(f'{d["source_id"]}: forbidden word {forbidden_words(text)}')
        for p in d['parent_nodes']:
            if p not in all_nodes:
                errors.append(f'{d["source_id"]}: parent node {p} unknown')
        for ref in d.get('lean', []) + d.get('rust', []) + d.get('python', []) + d['sources']:
            if not resolves(root, ref):
                errors.append(f'{d["source_id"]}: reference does not resolve: {ref}')
        if d['status'] == 'PROVED_LEAN' and not d.get('lean'):
            errors.append(f'{d["source_id"]}: PROVED_LEAN without a local Lean reference')
        paper = f'dag/derivations/{STAGE_FOLDERS[d["stage"]]}/tfq_{d["record_id"][4:]}_{slug(d["slug"])}.md'
        paths[d['record_id']] = paper
    for d in domain:
        parent_record = d['parent_record']
        record = {
            'id': d['record_id'], 'uuid': record_uuid(d['record_id']), 'local_id': d['node_id'],
            'name': d['name'], 'stage': d['stage'], 'parent_id': parent_record,
            'record_status': RECORD_STATUS[d['status']], 'summary': d['statement'], 'obligation': d['obligation'],
            'source_slice': 'application_branches', 'existing_derivation_dag_ids': [d['node_id']],
            'coda_atlas_ids': [], 'coda_atlas_paths': [],
            'f004_refs': [paths[d['record_id']]] + [s for s in d['sources']],
            'python': list(d.get('python', [])), 'rust': list(d.get('rust', [])), 'lean4': list(d.get('lean', [])),
        }
        domain_records.append(record)
        node = {
            'id': d['node_id'], 'stage': d['stage'], 'status': d['status'],
            'source_status': (f'{d["corpus"]} record {d["source_id"]} claims '
                              f'{d.get("source_claimed_status") or "no status"}; audited status {d["status"]}'),
            'statement': d['statement'],
            'source': list(dict.fromkeys([paths[d['record_id']]] + [plain_path(s) for s in d['sources']])),
            'lean': list(d.get('lean', [])), 'rust': list(d.get('rust', [])),
            'imported_structure': list(d.get('imported_structure', [])), 'bottleneck': d['obligation'],
            'tags': ['application-branch', DOMAIN_TAG, d['record_id'], d['source_id']],
        }
        see = [x for x in d.get('see_also', []) + d.get('uses', []) if x in all_nodes and x != d['node_id']]
        if see:
            node['see_also'] = list(dict.fromkeys(see))
        domain_nodes.append(node)
        route_status = ROUTE_STATUS[d['status']]
        domain_routes.append({
            'id': DOMAIN_ROUTE_PREFIX + d['node_id'], 'inputs': list(d['parent_nodes']), 'output': d['node_id'],
            'status': route_status, 'mechanism': d['obligation'],
            'source': list(dict.fromkeys([paths[d['record_id']]] + [plain_path(s) for s in d['sources'][:2]])),
        })
    for d in domain:
        if d['parent_record'] not in paths:
            errors.append(f'{d["source_id"]}: parent record {d["parent_record"]} has no paper')
            continue
        kids = [(k['record_id'], paths[k['record_id']]) for k in domain if k['parent_record'] == d['record_id']]
        outputs[root / paths[d['record_id']]] = render_domain_paper(
            d, next(r for r in domain_records if r['id'] == d['record_id']), paths[d['record_id']],
            paths[d['parent_record']], kids).encode('utf-8')
    app['nodes'] += domain_nodes
    app['routes'] += domain_routes
    app['records'] += domain_records
    for stage in fragment.get('domain_stages_added', []):
        if stage not in app['stages']:
            app['stages'].append(stage)

    # 5. Packet crosswalk and alias tags on nodes.
    packet_tags: dict[str, list[str]] = {}
    for packet, rid in fragment['packet_crosswalk'].items():
        nid = node_of(rid)
        if nid is None:
            errors.append(f'packet {packet}: record {rid} has no node')
            continue
        packet_tags.setdefault(nid, []).append('packet:' + packet)
    for n in dag['nodes'] + new_nodes:
        if 'pregenesis-to-wdp' in n.get('tags', []):
            continue  # the pre-genesis sync owns these nodes; the crosswalk table carries their aliases
        extra = packet_tags.get(n['id'], []) + alias_tags.get(n['id'], [])
        if extra:
            n['tags'] = n.get('tags', []) + extra
    for n in app['nodes']:
        n['tags'] = [t for t in n.get('tags', []) if not t.startswith(OWNED_TAG_PREFIXES)]
        extra = packet_tags.get(n['id'], []) + alias_tags.get(n['id'], [])
        if extra:
            n['tags'] = n['tags'] + extra

    if errors:
        raise ValueError('unified DAG fragment invalid:\n  ' + '\n  '.join(errors))

    # 6. DAG: unified nodes and routes go before the pre-genesis block, which precedes the
    #    application block; both other syncs then leave them in place.
    nodes = dag['nodes']
    at = next((i for i, n in enumerate(nodes) if 'pregenesis-to-wdp' in n.get('tags', []) or
               'application-branch' in n.get('tags', [])), len(nodes))
    dag['nodes'] = nodes[:at] + new_nodes + nodes[at:]
    routes = dag['routes']
    at = next((i for i, x in enumerate(routes) if x['id'].startswith(('PGW-R-', 'APP-R-'))), len(routes))
    dag['routes'] = routes[:at] + new_routes + routes[at:]
    for stage in NEW_STAGES:
        if stage not in dag['stages']:
            dag['stages'].append(stage)
    dag['status_legend']['SOURCE_RECORD'] = LEGEND_SOURCE_RECORD
    if EDGE_RECORD_PARENT not in dag['edge_semantics']:
        dag['edge_semantics'].append(EDGE_RECORD_PARENT)
    dag['segment_notes'][SLICE] = [fragment['segment_note']]
    # Application nodes the application sync will append, so the counts below see the final graph.
    final_app_ids = {n['id'] for n in app['nodes']}

    # 7. JSONL: rewrite only changed base lines; unified records go before the pre-genesis block.
    out_lines = []
    for r in records:
        r2 = by_id[r['id']]
        line = old_line.get(r['id'])
        if line is None or json.loads(line) != r2:
            line = record_line(r2, newline)
        out_lines.append((r2, line))
    at = next((i for i, (r, _) in enumerate(out_lines) if r['source_slice'] in fragment_slices), len(out_lines))
    block = [(rec, record_line(rec, newline)) for rec, _, _ in node_rows]
    out_lines = out_lines[:at] + block + out_lines[at:]
    all_records = [r for r, _ in out_lines if r['source_slice'] != 'application_branches'] + app['records']

    # 8. Markdown master: per-stage sections for unified records, stage counts, node count, crosswalk.
    master = (folder / 'theory_of_finite_qm.md').read_text(encoding='utf-8')
    head, marker, tail = master.partition(APP_MARKER)
    head = re.sub(r'\n<!-- unified-dag:rows:[A-Z0-9_]+:begin -->.*?<!-- unified-dag:rows:[A-Z0-9_]+:end -->\n', '\n',
                  head, flags=re.S)
    by_stage: dict[str, list] = {}
    for rec, n, _ in node_rows:
        by_stage.setdefault(rec['stage'], []).append((rec, n))
    for stage, items in by_stage.items():
        start = head.index(f'\n## {stage}\n')
        nxt = head.find('\n## ', start + 1)
        nxt = len(head) if nxt < 0 else nxt
        body = ''.join(f'\n### {rec["id"]} {rec["name"]}\n\n- UUID: `{rec["uuid"]}`\n- Parent: `{rec["parent_id"]}`\n'
                       f'- Status: `{rec["record_status"]}`\n- DAG node: `{n["id"]}` (`{n["status"]}`)\n\n'
                       f'{rec["summary"]}\n\nObligation: {rec["obligation"]}\n' for rec, n in items)
        block_md = f'\n<!-- unified-dag:rows:{stage}:begin -->{body}<!-- unified-dag:rows:{stage}:end -->\n'
        head = head[:nxt].rstrip('\n') + '\n' + block_md + head[nxt:]
    app_stages = set(app['stages'])
    for stage in {r['stage'] for r in all_records} - app_stages:
        count = sum(1 for r in all_records if r['stage'] == stage)
        head = re.sub(r'^\| `' + stage + r'` \| \d+ \|$', f'| `{stage}` | {count} |', head, count=1, flags=re.M)
    head = re.sub(r'Nodes: \d+\.', f'Nodes: {len(all_records)}.', head, count=1)
    head = re.sub(re.escape(XWALK_BEGIN) + r'.*?' + re.escape(XWALK_END) + r'\n\n', '', head, flags=re.S)
    dag_status = {n['id']: n['status'] for n in dag['nodes'] + new_nodes + app['nodes']}
    for rec in pgw['records']:
        if rec.get('dag') and 'reuse' not in rec['dag']:
            dag_status['PGW-' + rec['name'].upper()] = rec['dag']['status']
    review_of = {n['id']: n['pfp_review'] for n in dag['nodes'] if 'pfp_review' in n}
    xrows = []
    for r in all_records:
        ids = [x for x in r['existing_derivation_dag_ids'] if x in dag_status]
        if r['source_slice'] == 'pregenesis_to_wdp' and not ids:
            spec = next(p for p in pgw['records'] if p['id'] == r['id'])
            ids = [spec['dag']['reuse']] if 'reuse' in spec.get('dag', {}) else ['PGW-' + r['name'].upper()]
        cells = ', '.join(f'`{x}` ({dag_status.get(x, "?")})' for x in ids)
        reviewed = [x for x in ids if x in review_of]
        label = lambda x: f'{review_of[x]["verdict"]} / {review_of[x]["scope_effect"]}'
        review_cell = '; '.join(label(x) if len(reviewed) == 1 else f'`{x}`: {label(x)}' for x in reviewed) or '-'
        xrows.append(f'| `{r["id"]}` | `{r["stage"]}` | `{r["record_status"]}` | {cells} | {review_cell} |')
    aliases = fragment.get('domain_aliases', [])
    xwalk = [XWALK_BEGIN, '## Unified derivation graph', '',
             'Generated by `dag/sync_unified_dag.py`. `derivation_dag.json`, this file and '
             '`theory_of_finite_qm.jsonl` describe one graph: every record names at least one DAG node and every '
             'DAG node is named by at least one record. A record that named no node has a node with its own id '
             '(tag `unified-dag`); a node that no record named has a record from `TFQ-1000` upward. '
             f'Records: {len(all_records)}. DAG nodes: {len(dag_status)}. '
             f'Source-corpus records folded in: {len(domain)} new, {len(aliases)} trunk restatements.', '',
             'The Review column names the verdict and scope effect of the PFP review of each reviewed node '
             '(`dag/fragments/pfp_review_decisions.json`, written by `dag/sync_pfp_results.py`); the node status '
             'in the previous column is the status after that review.', '',
             '### Record to node crosswalk', '',
             '| Record | Stage | Record status | DAG node (status) | Review |',
             '|---|---|---|---|---|', *xrows, '']
    if aliases:
        xwalk += ['### Source-corpus trunk restatements', '',
                  'These source records restate a trunk step; the trunk node carries an `alias:` tag.', '',
                  '| Source record | Corpus | Trunk node or record | Note |', '|---|---|---|---|',
                  *[f'| `{a["source_id"]}` | `{a["corpus"]}` | `{a["alias_of"]}` | '
                    f'{a.get("alias_note", "").replace("|", chr(92) + "|")} |'
                    for a in aliases], '']
    xwalk.append(XWALK_END)
    i = head.index('\n## PREGENESIS\n') + 1
    head = head[:i] + '\n'.join(xwalk) + '\n\n' + head[i:]
    master = head + marker + tail

    # 9. Derivation README: unified records in their stage tables.
    readme_path = folder / 'derivations/README.md'
    readme = readme_path.read_text(encoding='utf-8')
    rhead, rmarker, rtail = readme.partition(APP_MARKER)
    rhead = re.sub(r'^\| \[`(TFQ-1\d{3})`\].*\n', '', rhead, flags=re.M)
    for stage, items in by_stage.items():
        m = re.search(r'^### ' + stage + r' \((\d+) derivations\)\n', rhead, re.M)
        if m is None:
            continue
        start = m.end()
        nxt = rhead.find('\n### ', start)
        nxt = len(rhead) if nxt < 0 else nxt
        section = rhead[start:nxt].rstrip('\n')
        rows_md = ''.join(
            f'\n| [`{rec["id"]}`](./{paths[rec["id"]].removeprefix("dag/derivations/")}) | {rec["name"]} | '
            f'`{rec["record_status"]}` | [`{rec["parent_id"]}`](./{paths[rec["parent_id"]].removeprefix("dag/derivations/")}) |'
            for rec, _ in items)
        section += rows_md
        count = section.count('\n| [`TFQ-')
        rhead = rhead[:m.start()] + f'### {stage} ({count} derivations)\n' + section + '\n' + rhead[nxt:]
    readme = rhead + rmarker + rtail

    outputs[folder / 'derivation_dag.json'] = json_text(dag).encode('utf-8')
    outputs[folder / 'theory_of_finite_qm.jsonl'] = ''.join(line for _, line in out_lines).encode('utf-8')
    outputs[folder / 'theory_of_finite_qm.md'] = master.encode('utf-8')
    outputs[readme_path] = readme.encode('utf-8')
    outputs[app_path] = json_text(app).encode('utf-8')
    outputs[pgw_path] = json_text(pgw).encode('utf-8')
    return outputs


def invariant_errors(root: Path = ROOT) -> list[str]:
    """After all three syncs: one graph, records and nodes naming each other."""
    dag = json.loads((root / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    records = [json.loads(line) for line in (root / 'dag/theory_of_finite_qm.jsonl').read_text(encoding='utf-8').splitlines()]
    node_ids = {n['id'] for n in dag['nodes']}
    named = {x for r in records for x in r['existing_derivation_dag_ids']}
    errs = [f'record {r["id"]} names no DAG node' for r in records
            if not any(x in node_ids for x in r['existing_derivation_dag_ids'])]
    errs += [f'node {n} is named by no record' for n in sorted(node_ids - named)]
    papers = paper_paths(root)
    errs += [f'record {r["id"]} has no paper' for r in records if r['id'] not in papers]
    return errs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--invariants', action='store_true', help='check the joined graph; write nothing')
    args = parser.parse_args()
    if args.invariants:
        errs = invariant_errors(ROOT)
        for err in errs:
            print('FAIL', err)
        print(f'unified invariants failures={len(errs)}')
        return int(bool(errs))
    differences = []
    for path, expected in generated_files(ROOT).items():
        if not path.exists() or path.read_bytes() != expected:
            differences.append(path.relative_to(ROOT).as_posix())
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(expected)
    print('stale=' + ','.join(differences) if differences else 'unified DAG synchronized')
    return int(bool(differences) and args.check)


if __name__ == '__main__':
    raise SystemExit(main())
