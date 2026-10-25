"""Synchronize the FOC-035 observer-presheaf fragment into derivation_dag.json, its papers and the derivation index.

dag/fragments/foc035_observer_presheaf.json holds one stage, OBSERVER_PRESHEAF. It maps the rows of the claim
ledger of FOC-035 ("Local Green, Global Red: the Observer Tuple, the Empirical Presheaf and the Three-Role Gate",
copied byte for byte under sources/atlas/) to nodes. A row keeps the status its evidence supports in this
repository, not the status it has in the source repository:

- PROVED_LEAN only for the declarations of lean4/LggrFiniteResults.lean, with the statement narrowed to them;
- COMPUTATIONALLY_CHECKED only where a check that runs here recomputes the instance values: the exact independent
  script checks/independent/foc035_observer_presheaf.py or the imported Python tests under code/python/tests;
- CONDITIONAL where the computing test is a Rust test that needs the external omega_solvers crate and is not run here;
- IMPORTED_ASSUMPTION for results the note cites by name and does not re-prove (external ids checked against the
  arXiv and DOI records);
- PROVED_PROSE for statements the note proves in prose only, REFUTED for the negative-evidence rows, OPEN for the
  Lean gap, SOURCE_RECORD and DEFINITION for names and definitions.

derivation_dag.json (schema derivation_dag.v2) is the single source of the graph. This script owns:

- the fragment's nodes (tag foc035-observer-presheaf), routes (id prefix OPS-R-) and records (source_slice
  foc035_observer_presheaf), which come last, after the genesis-to-higher block;
- the stage OBSERVER_PRESHEAF at the end of index_document.application_stages;
- one generated derivation paper per record, under dag/derivations/35_foc035_observer_presheaf;
- the section of dag/derivations/README.md after the line views.OPS_MARKER.

Run order: sync_pfp_results.py, sync_unified_dag.py, sync_application_branches.py, sync_pregenesis_to_wdp.py,
sync_frontier_branches.py, sync_genesis_to_higher.py, this script. --check detects stale generated data without
writing. AuthorityEffect: None. Synchronization does not establish a mathematical claim.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import render_dag_views as views  # noqa: E402

SLICE = views.OPS_SLICE
MARKER = views.OPS_MARKER
TAG = views.OPS_TAG
ROUTE_PREFIX = views.OPS_ROUTE_PREFIX
STAGE = views.OPS_STAGE
FRAGMENT = 'dag/fragments/foc035_observer_presheaf.json'
FOLDER = '35_foc035_observer_presheaf'
NODE_PREFIX = 'OPS-'
LEAN_FILE = 'lean4/LggrFiniteResults.lean'
CAMPAIGN_CEILING = 'lean4/CampaignOpsRustReceiptsAndLimits.lean'
INDEPENDENT = 'checks/independent/foc035_observer_presheaf.py'
PYTHON_TESTS = ('code/python/tests/test_three_role_gate.py',)
FORBIDDEN = ('proves', 'guarantees', 'mathematically verifies', 'fundamentally', 'true intelligence', 'impossible',
             'universal', 'flawless', 'perfectly', 'clearly', 'obviously', 'simply', 'merely', 'weaponized')
EXTERNAL = ('external:', 'pr:')
ALLOWED_STATUS = ('DEFINITION', 'PROVED_PROSE', 'PROVED_LEAN', 'COMPUTATIONALLY_CHECKED', 'CONDITIONAL',
                  'IMPORTED_ASSUMPTION', 'OPEN', 'REFUTED', 'SOURCE_RECORD')
RECORD_STATUS = {'DEFINITION': 'DEFINITION', 'PROVED_PROSE': 'PROVED_PROSE', 'PROVED_LEAN': 'PROVED_LEAN',
                 'COMPUTATIONALLY_CHECKED': 'COMPUTATIONAL_CONTROL', 'CONDITIONAL': 'CONDITIONAL',
                 'IMPORTED_ASSUMPTION': 'IMPORTED_ASSUMPTION', 'OPEN': 'OPEN_OBLIGATION', 'REFUTED': 'REFUTED',
                 'SOURCE_RECORD': 'SOURCE_RECORD'}
json_text = views.json_text


def forbidden_words(text: str) -> list[str]:
    low = text.lower()
    return [w for w in FORBIDDEN if re.search(r'\b' + re.escape(w) + r'\b', low)]


def paper_paths(root: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    for p in (root / 'dag' / 'derivations').rglob('tfq_*.md'):
        key = re.match(r'tfq_(\d{4})_', p.name)
        if key:
            found['TFQ-' + key[1]] = p.relative_to(root).as_posix()
    return found


def link(from_paper: str, to_paper: str, label: str) -> str:
    rel = os.path.relpath(to_paper, os.path.dirname(from_paper)).replace(os.sep, '/')
    return f'[{label}]({rel})'


def symbol_errors(root: Path, node_id: str, field: str, ref: str) -> list[str]:
    path, _, symbol = ref.partition('::')
    if not (root / path).is_file():
        return [f'{node_id}: {field} path missing: {path}']
    if symbol and symbol.split('::')[-1].split('.')[-1] not in (root / path).read_text(encoding='utf-8', errors='replace'):
        return [f'{node_id}: {field} symbol {symbol} not in {path}']
    return []


def validate(fragment: dict, dag: dict, root: Path) -> list[str]:
    errs: list[str] = []
    nodes, routes, records = fragment['nodes'], fragment['routes'], fragment['records']
    ids = {n['id'] for n in nodes}
    others = {n['id'] for n in dag['nodes'] if TAG not in n.get('tags', [])}
    if fragment.get('stages') != [STAGE]:
        errs.append('fragment stages must be exactly OBSERVER_PRESHEAF')
    if len(ids) != len(nodes):
        errs.append('duplicate foc035 node ids')
    if ids & others:
        errs.append('node collides with an existing node: ' + ', '.join(sorted(ids & others)))
    if len({r['id'] for r in records}) != len(records):
        errs.append('duplicate record ids')
    if len({r['id'] for r in routes}) != len(routes):
        errs.append('duplicate route ids')
    known = ids | others
    cited = {c['ref'] for c in fragment['citations'].values()}
    _validate_node_evidence(nodes, cited, root, errs)
    _validate_routes_and_statuses(nodes, routes, ids, others, known, errs, root)
    record_ids = {r['id'] for r in records}
    existing = {r['id'] for r in dag['records'] if r.get('source_slice') != SLICE}
    if record_ids & existing:
        errs.append('record id collides with an existing record')
    node_by_id = {n['id']: n for n in nodes}
    for r in records:
        if r['source_slice'] != SLICE or r['stage'] != STAGE:
            errs.append(f'{r["id"]}: bad slice or stage')
        if r['parent_id'] not in (record_ids | existing):
            errs.append(f'{r["id"]}: bad parent')
        if r['existing_derivation_dag_ids'] != [r['local_id']]:
            errs.append(f'{r["id"]}: record does not name its node')
        node = node_by_id.get(r['local_id'])
        if node is None or r['record_status'] != RECORD_STATUS.get(node['status']):
            errs.append(f'{r["id"]}: record status does not follow the node status')
    named = {x for r in records for x in r['existing_derivation_dag_ids']}
    if named != ids:
        errs.append('records and nodes of the fragment do not name each other')
    blob = json.dumps(fragment, ensure_ascii=False)
    errs += [f'forbidden word in fragment: {w}' for w in forbidden_words(blob)]
    return errs


def _validate_node_evidence(nodes, cited, root, errs):
    for n in nodes:
        nid = n['id']
        if not nid.startswith(NODE_PREFIX) or n['stage'] != STAGE:
            errs.append(f'{nid}: bad id prefix or stage')
        if n['status'] not in ALLOWED_STATUS:
            errs.append(f'{nid}: status {n["status"]} is not allowed in this fragment')
        if TAG not in n['tags']:
            errs.append(f'{nid}: missing tag {TAG}')
        _validate_node_references(n, nid, cited, root, errs)
        if n['status'] == 'IMPORTED_ASSUMPTION' and not n['imported_structure']:
            errs.append(f'{nid}: an import needs imported_structure')
        if n['status'] == 'PROVED_LEAN':
            if not n['lean'] or any(not x.startswith(LEAN_FILE + '::') for x in n['lean']):
                errs.append(f'{nid}: PROVED_LEAN must cite declarations of {LEAN_FILE}')
        elif n['id'] == 'OPS-RUST-RECEIPTS-AND-LIMITS':
            if not n['lean'] or any(not x.startswith(CAMPAIGN_CEILING + '::') for x in n['lean']):
                errs.append(f'{nid}: ceiling narrowing must cite declarations of {CAMPAIGN_CEILING}')
        elif n['lean']:
            errs.append(f'{nid}: only PROVED_LEAN nodes carry lean references')
        if n['status'] == 'COMPUTATIONALLY_CHECKED' and not (
                INDEPENDENT in n['source'] or any(t in n['source'] for t in PYTHON_TESTS)):
            errs.append(f'{nid}: COMPUTATIONALLY_CHECKED must cite the independent check or an imported Python test')
        if n['status'] == 'CONDITIONAL' and 'not run here' not in n['bottleneck'] and 'cited, not re-run' not in n['bottleneck']:
            errs.append(f'{nid}: a CONDITIONAL bottleneck must say what is not run here or not re-run')


def _validate_routes_and_statuses(nodes, routes, ids, others, known, errs, root):
    for r in routes:
        if not r['id'].startswith(ROUTE_PREFIX) or r['output'] not in ids or any(i not in known for i in r['inputs']):
            errs.append(f'route {r["id"]}: bad id or endpoint')
        if r['status'] == 'GAP_NO_DERIVATION' and r.get('source'):
            errs.append(f'route {r["id"]}: a gap route carries no source')
        if r['status'] != 'GAP_NO_DERIVATION' and not r.get('source'):
            errs.append(f'route {r["id"]}: non-gap route without source')
        for ref in r.get('source', []):
            if not ref.startswith(EXTERNAL) and not (root / ref.split('#', 1)[0]).is_file():
                errs.append(f'route {r["id"]}: source path missing: {ref}')
    for n in nodes:
        incoming = [r for r in routes if r['output'] == n['id']]
        if not incoming:
            errs.append(f'{n["id"]}: no incoming route')
        if n['status'] == 'OPEN' and any(r['status'] != 'GAP_NO_DERIVATION' for r in incoming):
            errs.append(f'{n["id"]}: an OPEN node may only have gap routes')
        if n['status'] in ('PROVED_PROSE', 'PROVED_LEAN') and all(r['status'] == 'GAP_NO_DERIVATION' for r in incoming):
            errs.append(f'{n["id"]}: {n["status"]} but every incoming route is a gap')
        if n['status'] == 'PROVED_LEAN' and not any(r['status'] == 'DERIVED_LEAN' for r in incoming):
            errs.append(f'{n["id"]}: PROVED_LEAN without a DERIVED_LEAN route')


def render_paper(node: dict, record: dict, fragment: dict, paths: dict[str, str]) -> str:
    me = paths[record['id']]
    parent = record['parent_id']
    routes_in = [r for r in fragment['routes'] if r['output'] == node['id']]
    out = [f'# [{record["id"]}] {record["name"]}', '',
           f'**Stage:** `{node["stage"]}` | **Status:** `{node["status"]}` | **AuthorityEffect:** None.', '',
           f'**Parent:** {link(me, paths[parent], parent)}  ',
           f'**DAG node:** `{node["id"]}`  ',
           f'**UUID:** `{record["uuid"]}`  ',
           f'**Ledger rows:** {", ".join(node["ledger_rows"]) if "ledger_rows" in node else ""}', '',
           '*Generated by `dag/sync_foc035_observer_presheaf.py` from `dag/fragments/foc035_observer_presheaf.json`; '
           'edit the fragment, not this paper.*', '',
           '## Statement', '', node['statement'], '',
           '## Governing obligation', '', node['bottleneck'], '',
           '## Source status', '', node['source_status'], '']
    if node['imported_structure']:
        out += ['## Imported structure', '', *[f'- `{x}`' for x in node['imported_structure']], '']
    out += ['## Routes', '']
    for r in routes_in:
        out.append(f'- Route `{r["id"]}` (`{r["status"]}`) from '
                   f'{", ".join("`" + i + "`" for i in r["inputs"])}: {r["mechanism"]}')
    if node['see_also']:
        out += ['', 'See also: ' + ', '.join('`' + x + '`' for x in node['see_also']) + '.']
    out += ['', '## Non-claims', '',
            '- The source note and its claim ledger are copies of FOC-035 from another repository; this paper restates '
            'one ledger row at the status its evidence supports here.',
            '- A Lean reference is listed only on a PROVED_LEAN node, and its statement is narrower than the ledger row '
            'where the node says so.',
            '- A Rust test of the source repository is not run in this repository.',
            '- An imported assumption is not a result of this repository.',
            '- A gap route marks a link that no source derives.',
            '', '## Sources', '']
    for key in fragment['paper_cites'].get(node['id'], []):
        cite = fragment['citations'][key]
        out.append(f'- `{cite["ref"]}`: {cite["text"]}')
    for ref in node['source']:
        if not ref.startswith(EXTERNAL):
            out.append(f'- Repository: `{ref}`')
    return '\n'.join(out) + '\n'


def generated_files(root: Path) -> dict[Path, bytes]:
    fragment = json.loads((root / FRAGMENT).read_text(encoding='utf-8'))
    dag = views.load_dag(root)
    errs = validate(fragment, dag, root)
    if errs:
        raise ValueError('foc035 observer-presheaf fragment invalid:\n  ' + '\n  '.join(errs))
    nodes, routes, records = fragment['nodes'], fragment['routes'], fragment['records']
    # ledger_rows is fragment metadata for the papers; it is not a node key of derivation_dag.json.
    graph_nodes = [{k: v for k, v in n.items() if k != 'ledger_rows'} for n in nodes]
    ids = {n['id'] for n in nodes}
    route_ids = {r['id'] for r in routes}
    record_ids = {r['id'] for r in records}

    dag['nodes'] = [n for n in dag['nodes'] if TAG not in n.get('tags', []) and n['id'] not in ids] + graph_nodes
    dag['routes'] = [r for r in dag['routes'] if not r['id'].startswith(ROUTE_PREFIX) and r['id'] not in route_ids] + routes
    if STAGE not in dag['stages']:
        dag['stages'].append(STAGE)
    kept = [r for r in dag['records'] if r.get('source_slice') != SLICE and r['id'] not in record_ids]
    dag['records'] = [views.canonical_record(r) for r in kept + records]
    doc = dag['index_document']
    doc['application_stages'] = [s for s in doc['application_stages'] if s != STAGE] + [STAGE]
    dag['segment_notes'][SLICE] = [fragment['segment_note']]

    paths = paper_paths(root)
    for r in records:
        paths[r['id']] = r['f004_refs'][0]
        prefix = 'dag/derivations/' + FOLDER + '/tfq_' + r['id'][4:] + '_'
        if not r['f004_refs'][0].startswith(prefix):
            raise ValueError(f'{r["id"]}: paper path does not follow the stage folder')
    missing = [r['parent_id'] for r in records if r['parent_id'] not in paths]
    if missing:
        raise ValueError('parent record without a paper: ' + ', '.join(sorted(set(missing))))
    node_by_id = {n['id']: n for n in nodes}
    outputs: dict[Path, bytes] = {}
    for r in records:
        text = render_paper(node_by_id[r['existing_derivation_dag_ids'][0]], r, fragment, paths)
        bad = forbidden_words(text)
        if bad:
            raise ValueError(f'{r["id"]}: forbidden word in paper: {bad}')
        if '\r' in text:
            raise ValueError(f'{r["id"]}: paper contains CR')
        outputs[root / paths[r['id']]] = text.encode('utf-8')

    readme = (root / 'dag/derivations/README.md').read_text(encoding='utf-8')
    base = readme.partition(MARKER)[0].rstrip('\n')
    section = '\n\n' + MARKER + '\n\n## FOC-035 observer presheaf\n\n'
    section += ('This stage maps the claim ledger of FOC-035 to nodes at the status the evidence supports in this '
                'repository. Lean-checked rows keep only the narrowed statements of `lean4/LggrFiniteResults.lean`. '
                'Rows computed by a Rust test stay conditional, because that test needs an external crate and is not '
                'run here. Instance values are recomputed by an exact independent script, and the Python gate and '
                'one repaired test run here. Cited results are imported assumptions. A gap route marks a link that no '
                'source derives. See the [branch fragment](../fragments/foc035_observer_presheaf.json).\n')
    section += f'\n### {STAGE} ({len(records)} derivations)\n\n'
    section += '| ID | Name | Status | Parent | DAG node |\n|---|---|---|---|---|\n'
    for r in records:
        paper = paths[r['id']].removeprefix('dag/derivations/')
        parent = paths[r['parent_id']].removeprefix('dag/derivations/')
        section += (f'| [{r["id"]}](./{paper}) | {r["name"]} | `{r["record_status"]}` | '
                    f'[{r["parent_id"]}](./{parent}) | `{r["existing_derivation_dag_ids"][0]}` |\n')
    bad = forbidden_words(section)
    if bad:
        raise ValueError(f'forbidden word in README section: {bad}')
    outputs[root / 'dag/derivations/README.md'] = (base + section).encode('utf-8')
    outputs.update(views.outputs(dag, root))
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = HERE.parent
    differences = []
    for path, expected in generated_files(root).items():
        if not path.exists() or path.read_bytes() != expected:
            differences.append(path.relative_to(root).as_posix())
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(expected)
    print('stale=' + ','.join(differences) if differences else 'foc035 observer presheaf synchronized')
    return int(bool(differences) and args.check)






def _validate_node_references(n, nid, cited, root, errs):
    for ref in n['source']:
        if ref.startswith('external:'):
            if ref not in cited:
                errs.append(f'{nid}: external source {ref} has no citation entry')
        elif not ref.startswith('dag/derivations/' + FOLDER + '/'):  # the generated paper is written below
            path = ref.split('#', 1)[0]
            if not (root / path).is_file():
                errs.append(f'{nid}: source path missing: {ref}')
    for field in ('lean', 'rust'):
        for ref in n[field]:
            errs += symbol_errors(root, nid, field, ref)


if __name__ == '__main__':
    raise SystemExit(main())
