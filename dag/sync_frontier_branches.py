"""Synchronize the frontier-branch fragment into derivation_dag.json, its papers and the derivation index.

dag/fragments/frontier_branches.json holds four branches that connect external programmes to the existing
graph: CONSTRUCTOR_THEORY, CAUSAL_QFT, ADS_CFT and LOOP_QUANTUM_GRAVITY. Every external result is a node with status
SOURCE_RECORD, IMPORTED_ASSUMPTION or OPEN (the two Lean anchors, the one definition, and the 14 finite targets read
repository files and carry PROVED_LEAN or DEFINITION). A route that no source derives is GAP_NO_DERIVATION. Finite
exact targets carry PROVED_LEAN on their declared finite domain.

derivation_dag.json (schema derivation_dag.v2) is the single source of the graph. This script owns:

- the fragment's nodes (tag frontier-branch), routes (id prefix FRO-R-) and records (source_slice frontier_branches),
  which come last in their lists, after the application block;
- index_document.application_stages: the application stages followed by the frontier stages;
- one generated derivation paper per record, under dag/derivations/30_constructor_theory, 31_causal_qft, 32_ads_cft
  and 33_loop_quantum_gravity;
- the frontier section of dag/derivations/README.md, after the line views.FRONTIER_MARKER.

Run order: sync_pfp_results.py, sync_unified_dag.py, sync_application_branches.py, sync_pregenesis_to_wdp.py, this
script, then dag/sync_genesis_to_higher.py. A genesis-to-higher block already in the graph (tag
genesis-to-higher, routes GTH-R-, records of source_slice genesis_to_higher, the README section after
views.GTH_MARKER) is kept after the frontier block. --check detects stale generated data without writing.
AuthorityEffect: None. Synchronization does not establish a mathematical claim.
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

SLICE = views.FRONTIER_SLICE
MARKER = views.FRONTIER_MARKER
TAG = 'frontier-branch'
ROUTE_PREFIX = 'FRO-R-'
FRAGMENT = 'dag/fragments/frontier_branches.json'
FOLDERS = {'CONSTRUCTOR_THEORY': '30_constructor_theory', 'CAUSAL_QFT': '31_causal_qft',
           'ADS_CFT': '32_ads_cft', 'LOOP_QUANTUM_GRAVITY': '33_loop_quantum_gravity'}
FORBIDDEN = ('proves', 'guarantees', 'mathematically verifies', 'fundamentally', 'true intelligence', 'impossible',
             'universal', 'flawless', 'perfectly', 'clearly', 'obviously', 'simply', 'merely', 'weaponized')
EXTERNAL = ('external:', 'pr:')
ALLOWED_STATUS = ('SOURCE_RECORD', 'IMPORTED_ASSUMPTION', 'OPEN', 'PROVED_LEAN', 'DEFINITION')
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


# The ownership and run-order notes of derivation_dag.json name every sync; this script adds itself to them.
NOTE_PATCHES = (
    ('source_slice unified_dag, application_branches and pregenesis_to_wdp,',
     'source_slice unified_dag, application_branches, pregenesis_to_wdp and frontier_branches,'),
    ('dag/sync_pregenesis_to_wdp.py and dag/sync_pfp_results.py from their fragments',
     'dag/sync_pregenesis_to_wdp.py, dag/sync_frontier_branches.py and dag/sync_pfp_results.py from their fragments'),
    ('index_document.application_stages is written by dag/sync_application_branches.py and ',
     'index_document.application_stages is written by dag/sync_application_branches.py (application stages) and '
     'dag/sync_frontier_branches.py (frontier stages), and '),
    ('sync_application_branches.py, sync_pregenesis_to_wdp.py; each writes',
     'sync_application_branches.py, sync_pregenesis_to_wdp.py, sync_frontier_branches.py; each writes'),
    ('pregenesis_to_wdp and frontier_branches,',
     'pregenesis_to_wdp, frontier_branches and genesis_to_higher,'),
    ('dag/sync_frontier_branches.py and dag/sync_pfp_results.py',
     'dag/sync_frontier_branches.py, dag/sync_genesis_to_higher.py and dag/sync_pfp_results.py'),
    ('dag/sync_frontier_branches.py (frontier stages), and ',
     'dag/sync_frontier_branches.py (frontier stages) and dag/sync_genesis_to_higher.py '
     '(the genesis-to-higher stage), and '),
    ('sync_frontier_branches.py; each writes',
     'sync_frontier_branches.py, sync_genesis_to_higher.py; each writes'),
)


def patch_schema_note(note: str) -> str:
    for old, new in NOTE_PATCHES:
        note = note.replace(old, new)
    return note


def validate(fragment: dict, dag: dict) -> list[str]:
    errs: list[str] = []
    nodes, routes, records = fragment['nodes'], fragment['routes'], fragment['records']
    ids = {n['id'] for n in nodes}
    others = {n['id'] for n in dag['nodes'] if TAG not in n.get('tags', [])}
    if len(ids) != len(nodes):
        errs.append('duplicate frontier node ids')
    if ids & others:
        errs.append('frontier node collides with an existing node: ' + ', '.join(sorted(ids & others)))
    if len({r['id'] for r in records}) != len(records):
        errs.append('duplicate frontier record ids')
    if len({r['id'] for r in routes}) != len(routes):
        errs.append('duplicate frontier route ids')
    known = ids | others
    for n in nodes:
        if n['stage'] not in fragment['stages']:
            errs.append(f'{n["id"]}: stage {n["stage"]} not in the fragment stages')
        if n['status'] not in ALLOWED_STATUS:
            errs.append(f'{n["id"]}: status {n["status"]} is not allowed in this fragment')
        if TAG not in n['tags']:
            errs.append(f'{n["id"]}: missing tag {TAG}')
        for ref in n['source']:
            if ref.startswith('external:') and ref not in {c['ref'] for c in fragment['citations'].values()}:
                errs.append(f'{n["id"]}: external source {ref} has no citation entry')
        if n['status'] in ('SOURCE_RECORD', 'IMPORTED_ASSUMPTION') and not any(
                ref.startswith('external:') for ref in n['source']):
            errs.append(f'{n["id"]}: an external result needs an external: source')
        if n['status'] == 'PROVED_LEAN' and not n['lean']:
            errs.append(f'{n["id"]}: PROVED_LEAN without a Lean reference')
    for r in routes:
        if not r['id'].startswith(ROUTE_PREFIX) or r['output'] not in known or any(i not in known for i in r['inputs']):
            errs.append(f'route {r["id"]}: bad id or endpoint')
        if r['output'] not in ids and r['output'] not in others:
            errs.append(f'route {r["id"]}: unknown output')
    for n in nodes:
        out_routes = [r for r in routes if r['output'] == n['id']]
        if not out_routes:
            errs.append(f'{n["id"]}: no incoming route')
        if n['status'] == 'OPEN' and any(r['status'] not in ('GAP_NO_DERIVATION',) for r in out_routes):
            errs.append(f'{n["id"]}: an OPEN node may only have gap routes')
    record_ids = {r['id'] for r in records}
    existing = {r['id'] for r in dag['records'] if r.get('source_slice') != SLICE}
    if record_ids & existing:
        errs.append('frontier record id collides with an existing record')
    for r in records:
        if r['source_slice'] != SLICE or r['parent_id'] not in (record_ids | existing):
            errs.append(f'{r["id"]}: bad slice or parent')
    named = {x for r in records for x in r['existing_derivation_dag_ids']}
    if named != ids:
        errs.append('records and nodes of the fragment do not name each other')
    blob = json.dumps(fragment, ensure_ascii=False)
    errs += [f'forbidden word in fragment: {w}' for w in forbidden_words(blob)]
    return errs


def render_paper(node: dict, record: dict, fragment: dict, paths: dict[str, str]) -> str:
    notes = fragment['paper_notes'][node['id']]
    cites = fragment['citations']
    me = paths[record['id']]
    parent = record['parent_id']
    routes_in = [r for r in fragment['routes'] if r['output'] == node['id']]
    routes_out = [r for r in fragment['routes'] if node['id'] in r['inputs'] and r['output'] not in
                  {n['id'] for n in fragment['nodes']}]
    kids = [r for r in fragment['records'] if r['parent_id'] == record['id']]
    out = [f'# [{record["id"]}] {record["name"]}', '',
           f'**Stage:** `{node["stage"]}` | **Status:** `{node["status"]}` | **AuthorityEffect:** None.', '',
           f'**Parent:** {link(me, paths[parent], parent)}  ',
           f'**DAG node:** `{node["id"]}`  ',
           f'**UUID:** `{record["uuid"]}`  ',
           f'**Required DAG inputs:** {", ".join("`" + i + "`" for i in node_inputs(node, fragment))}', '',
           '*Generated by `dag/sync_frontier_branches.py` from `dag/fragments/frontier_branches.json`; edit the '
           'fragment, not this paper.*', '', '## Statement', '', node['statement'], '',
           '## Governing obligation', '', node['bottleneck'], '',
           '## Source status', '', node['source_status'], '',
           '## What is imported', '']
    out += [f'- {x}' for x in notes['imports']] or [
        '- Nothing is imported by this node as a premise of a repository result.']
    if node['imported_structure']:
        out += ['', 'Declared imported structure:', *[f'- `{x}`' for x in node['imported_structure']]]
    out += ['', '## What is open', '']
    out += [f'- {x}' for x in notes['open']] or ['- No further obligation is recorded beyond the governing obligation.']
    if notes['target']:
        target_note = (
            'Checked in Lean 4 on the declared finite domain; see the Lean 4 declarations read below and '
            '`dag/research/frontier_targets_lean_replay.json`.'
            if node['status'] == 'PROVED_LEAN'
            else 'No check of this target is recorded in the repository. A run that mines or checks it must keep the '
                 'statement as written or narrow it.'
        )
        out += ['', '## Finite target (precise statement)', '', notes['target'], '', target_note]
    out += ['', '## Connections to this repository', '']
    for r in routes_in:
        out.append(f'- Route `{r["id"]}` (`{r["status"]}`) from {", ".join("`" + i + "`" for i in r["inputs"])}: '
                   f'{r["mechanism"]}')
    for r in routes_out:
        out.append(f'- Route `{r["id"]}` (`{r["status"]}`) from this node into `{r["output"]}`: {r["mechanism"]}')
    out += [f'- {x}' for x in notes['connections']]
    if node['see_also']:
        out += ['', 'See also: ' + ', '.join('`' + x + '`' for x in node['see_also']) + '.']
    out += ['', '## Non-claims', '']
    out += [f'- {x}' for x in notes['non_claims']] or ['- No statement of this node is a theorem of the repository '
                                                         'beyond what its status says.']
    out += ['', '## Sources', '']
    for key in notes['cites']:
        out.append(f'- `{cites[key]["ref"]}`: {cites[key]["text"]}')
    local = [x for x in node['source'][1:] if not x.startswith(EXTERNAL)]
    out += [f'- Repository: `{x}`' for x in local]
    if not notes['cites'] and not local:
        out.append('- No external source and no repository file beyond the parent nodes named above.')
    if node['lean']:
        out += ['', '## Lean 4 declarations read', *[f'- `{x}`' for x in node['lean']]]
    out += ['', '## Downstream derivations', '']
    out += [f'- {link(me, paths[k["id"]], k["id"])} {k["name"]}' for k in kids] or [
        '*None (leaf in the current tree)*']
    return '\n'.join(out) + '\n'


def node_inputs(node: dict, fragment: dict) -> list[str]:
    main = [r for r in fragment['routes'] if r['id'] == ROUTE_PREFIX + node['id']]
    return main[0]['inputs'] if main else []


def generated_files(root: Path) -> dict[Path, bytes]:
    fragment = json.loads((root / FRAGMENT).read_text(encoding='utf-8'))
    dag = views.load_dag(root)
    errs = validate(fragment, dag)
    if errs:
        raise ValueError('frontier fragment invalid:\n  ' + '\n  '.join(errs))
    nodes, routes, records = fragment['nodes'], fragment['routes'], fragment['records']
    ids = {n['id'] for n in nodes}
    route_ids = {r['id'] for r in routes}
    record_ids = {r['id'] for r in records}

    # sync_genesis_to_higher.py owns the block after this one. Keep it last.
    gth_nodes = [n for n in dag['nodes'] if views.GTH_TAG in n.get('tags', [])]
    gth_routes = [r for r in dag['routes'] if r['id'].startswith(views.GTH_ROUTE_PREFIX)]
    dag['nodes'] = [n for n in dag['nodes'] if TAG not in n.get('tags', []) and n['id'] not in ids
                    and views.GTH_TAG not in n.get('tags', [])] + nodes + gth_nodes
    dag['routes'] = [r for r in dag['routes'] if not r['id'].startswith(ROUTE_PREFIX) and r['id'] not in route_ids
                     and not r['id'].startswith(views.GTH_ROUTE_PREFIX)] + routes + gth_routes
    for stage in fragment['stages']:
        if stage not in dag['stages']:
            dag['stages'].append(stage)
    gth_records = [r for r in dag['records'] if r.get('source_slice') == views.GTH_SLICE]
    kept = [r for r in dag['records'] if r.get('source_slice') not in (SLICE, views.GTH_SLICE)
            and r['id'] not in record_ids]
    dag['records'] = [views.canonical_record(r) for r in kept + records + gth_records]
    doc = dag['index_document']
    had_gth_stage = views.GTH_STAGE in doc['application_stages']
    doc['application_stages'] = [s for s in doc['application_stages']
                                 if s not in fragment['stages'] and s != views.GTH_STAGE] + list(fragment['stages'])
    if had_gth_stage:
        doc['application_stages'].append(views.GTH_STAGE)
    dag['segment_notes'][SLICE] = [fragment['segment_note']]
    dag['schema_notes'] = [patch_schema_note(s) for s in dag['schema_notes']]

    paths = paper_paths(root)
    for r in records:
        paths[r['id']] = r['f004_refs'][0]
        if not r['f004_refs'][0].startswith('dag/derivations/' + FOLDERS[r['stage']] + '/tfq_' + r['id'][4:] + '_'):
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
        outputs[root / paths[r['id']]] = text.encode('utf-8')

    readme = (root / 'dag/derivations/README.md').read_text(encoding='utf-8')
    head = readme.partition(MARKER)[0].rstrip('\n')
    gth_at = readme.find(views.GTH_MARKER)
    gth_tail = readme[gth_at:] if gth_at >= 0 else ''
    section = '\n\n' + MARKER + '\n\n## Frontier derivation branches\n\n'
    section += ('These branches record external programmes and their candidate finite targets. A source record or an '
                'imported assumption is not a result of this repository; an open target stays open until a run '
                'checks it. A gap route marks a link that no source read for this change derives. See the '
                '[branch fragment](../fragments/frontier_branches.json).\n')
    for stage in fragment['stages']:
        stage_records = [r for r in records if r['stage'] == stage]
        section += f'\n### {stage} ({len(stage_records)} derivations)\n\n'
        section += '| ID | Name | Status | Parent | DAG node |\n|---|---|---|---|---|\n'
        for r in stage_records:
            paper = paths[r['id']].removeprefix('dag/derivations/')
            parent = paths[r['parent_id']].removeprefix('dag/derivations/')
            section += (f'| [{r["id"]}](./{paper}) | {r["name"]} | `{r["record_status"]}` | '
                        f'[{r["parent_id"]}](./{parent}) | `{r["existing_derivation_dag_ids"][0]}` |\n')
    readme_text = head + section
    if gth_tail:
        if not gth_tail.endswith('\n'):
            gth_tail += '\n'
        readme_text = readme_text.rstrip('\n') + '\n\n' + gth_tail
    outputs[root / 'dag/derivations/README.md'] = readme_text.encode('utf-8')
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
    print('stale=' + ','.join(differences) if differences else 'frontier branches synchronized')
    return int(bool(differences) and args.check)


if __name__ == '__main__':
    raise SystemExit(main())
