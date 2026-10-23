"""Synchronize the application-branch fragment into derivation_dag.json and the derivation index.

derivation_dag.json (schema derivation_dag.v2) is the single source of the derivation graph. Only
the fragment-owned suffix is generated: the fragment's nodes and routes are appended to the DAG, its
records (source_slice application_branches) replace the application block at the end of the records
of derivation_dag.json, and index_document.application_stages lists the fragment stages, in order,
for the application sections of the Markdown view. Pre-existing derivation papers and records are
preserved. The read-only views theory_of_finite_qm.jsonl and theory_of_finite_qm.md are then rendered
from derivation_dag.json by dag/render_dag_views.py.

Run order: sync_pfp_results.py, sync_unified_dag.py, this script, sync_pregenesis_to_wdp.py,
sync_frontier_branches.py, sync_genesis_to_higher.py. The frontier block (nodes tagged frontier-branch,
routes FRO-R-, records of source_slice frontier_branches, the frontier README section) is kept after the
application block, and the genesis-to-higher block is kept after the frontier block.
--check detects stale generated data without writing.
AuthorityEffect: None. Synchronization does not establish a mathematical claim.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import render_dag_views as views  # noqa: E402

MARKER = views.APP_MARKER
FRONTIER_TAG = 'frontier-branch'
FRONTIER_ROUTE_PREFIX = 'FRO-R-'
json_text = views.json_text


def strip_suffix(text):
    return text.split(MARKER, 1)[0].rstrip() + '\n'


def generated_files(root: Path):
    folder = root / 'dag'
    fragment = json.loads((folder / 'fragments/application_branches.json').read_text(encoding='utf-8'))
    nodes, routes, records = (fragment[k] for k in ('nodes', 'routes', 'records'))
    ids = {n['id'] for n in nodes}
    record_ids = {r['id'] for r in records}
    if len(ids) != len(nodes) or len(record_ids) != len(records):
        raise ValueError('duplicate fragment identifiers')
    dag = views.load_dag(root)
    # Reject accidental capture of a node not previously owned by this fragment.
    for n in dag['nodes']:
        if n['id'] in ids and 'application-branch' not in n['tags']:
            raise ValueError('application node collides with existing node: ' + n['id'])
    _replace_application_nodes_and_routes(dag, fragment, nodes, routes, ids)
    _update_named_applications(dag, fragment)

    # Records: upstream records are kept as they are; the fragment records form the final block.
    old_records = dag['records']
    for r in old_records:
        if r['id'] in record_ids and r.get('source_slice') != 'application_branches':
            raise ValueError('application record collides with existing record: ' + r['id'])
    frontier_records = [r for r in old_records if r.get('source_slice') == views.FRONTIER_SLICE]
    gth_records = [r for r in old_records if r.get('source_slice') == views.GTH_SLICE]
    ops_records = [r for r in old_records if r.get('source_slice') == views.OPS_SLICE]
    all_records = [r for r in old_records if r['id'] not in record_ids
                   and r.get('source_slice') not in (views.FRONTIER_SLICE, views.GTH_SLICE, views.OPS_SLICE)] \
        + records + frontier_records + gth_records + ops_records
    if len({r['id'] for r in all_records}) != len(all_records):
        raise ValueError('duplicate master record identifiers')
    paper_paths = {}
    for p in (folder / 'derivations').rglob('tfq_*.md'):
        key = re.match(r'tfq_(\d{4})_', p.name)
        if key:
            paper_id = 'TFQ-' + key[1]
            if paper_id in paper_paths:
                raise ValueError('duplicate derivation paper: ' + paper_id)
            paper_paths[paper_id] = p.relative_to(root).as_posix()
    if any(r['id'] not in paper_paths or r['parent_id'] not in paper_paths for r in records):
        raise ValueError('application paper or parent is missing')
    # The Markdown view links an application record's paper through its first f004 reference.
    for r in records:
        if r['f004_refs'][:1] != [paper_paths[r['id']]]:
            raise ValueError(f'{r["id"]}: f004_refs must start with its paper {paper_paths[r["id"]]}')
    dag['records'] = [views.canonical_record(r) for r in all_records]
    # Stages appended by sync_frontier_branches.py follow this fragment's stages.
    dag['index_document']['application_stages'] = list(fragment['stages']) + [
        s for s in dag['index_document']['application_stages'] if s not in fragment['stages']]

    index = _render_application_index(folder, fragment, records, paper_paths)
    return {
        **views.outputs(dag, root),  # derivation_dag.json and the two views rendered from it
        folder / 'derivations/README.md': index.encode('utf-8'),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    differences = []
    for path, expected in generated_files(HERE.parent).items():
        if path.read_bytes() != expected:
            differences.append(path.name)
            if not args.check:
                path.write_bytes(expected)
    print('stale=' + ','.join(differences) if differences else 'application branches synchronized')
    return int(bool(differences) and args.check)




def _update_named_applications(dag, fragment):
    nf = next(n for n in dag['nodes'] if n['id'] == 'IMPL-FSP-SWITCHING-NORMAL-FORM-NF002')
    nf['statement'] = fragment['nf002_statement']
    if fragment['nf002_source'] not in nf['source']:
        nf['source'].append(fragment['nf002_source'])
    if fragment['nf002_replay_source'] not in nf['source']:
        nf['source'].append(fragment['nf002_replay_source'])
    nf['source_status'] = fragment['nf002_source_status']
    for symbol in fragment['nf002_replay_symbols']:
        reference = fragment['nf002_replay_source'] + '::' + symbol
        if reference not in nf['lean']:
            nf['lean'].append(reference)

    tensor = next(n for n in dag['nodes'] if n['id'] == 'FQ-GAP-TENSOR-UNIQUENESS')
    update = fragment['tensor_uniqueness_update']
    for field in ('statement', 'source_status', 'bottleneck', 'imported_structure'):
        tensor[field] = update[field]
    for field in ('source', 'see_also'):
        for reference in update[field]:
            if reference not in tensor[field]:
                tensor[field].append(reference)


def _replace_application_nodes_and_routes(dag, fragment, nodes, routes, ids):
    # Frontier-branch nodes, routes and records (sync_frontier_branches.py) stay after the application block.
    # The genesis-to-higher block (sync_genesis_to_higher.py) stays after the frontier block.
    frontier_nodes = [n for n in dag['nodes'] if FRONTIER_TAG in n.get('tags', [])]
    # The FOC-035 observer-presheaf block (sync_foc035_observer_presheaf.py) stays last.
    gth_nodes = [n for n in dag['nodes'] if views.GTH_TAG in n.get('tags', [])]
    ops_nodes = [n for n in dag['nodes'] if views.OPS_TAG in n.get('tags', [])]
    dag['nodes'] = [n for n in dag['nodes'] if n['id'] not in ids and FRONTIER_TAG not in n.get('tags', [])
                    and views.GTH_TAG not in n.get('tags', [])
                    and views.OPS_TAG not in n.get('tags', [])] + nodes + frontier_nodes + gth_nodes + ops_nodes
    route_ids = {r['id'] for r in routes}
    frontier_routes = [r for r in dag['routes'] if r['id'].startswith(FRONTIER_ROUTE_PREFIX)]
    gth_routes = [r for r in dag['routes'] if r['id'].startswith(views.GTH_ROUTE_PREFIX)]
    ops_routes = [r for r in dag['routes'] if r['id'].startswith(views.OPS_ROUTE_PREFIX)]
    dag['routes'] = [r for r in dag['routes'] if r['id'] not in route_ids
                     and not r['id'].startswith(FRONTIER_ROUTE_PREFIX)
                     and not r['id'].startswith(views.GTH_ROUTE_PREFIX)
                     and not r['id'].startswith(views.OPS_ROUTE_PREFIX)] \
        + routes + frontier_routes + gth_routes + ops_routes
    for stage in fragment['stages']:
        if stage not in dag['stages']:
            dag['stages'].append(stage)


def _render_application_index(folder, fragment, records, paper_paths):
    readme_head, frontier_marker, frontier_tail = (folder / 'derivations/README.md').read_text(
        encoding='utf-8').partition(views.FRONTIER_MARKER)
    index = strip_suffix(readme_head)
    index += '\n' + MARKER + '\n\n## Application and composition derivation branches\n\n'
    index += ('These branches attach to existing finite carriers. A proved theorem has its stated hypotheses; '
              'an open research target remains open. See the [branch fragment](../fragments/application_branches.json) '
              'and the [initial application receipt](../research/application_branches_validation.json). '
              'The [tensor receipt](../research/tensor_composition_validation.json) is the historical prose/kernel snapshot; '
              'the [formalization receipt](../research/tensor_formalization_validation.json) records the verified tomography and Schmidt extension. '
              'The [measurement receipt](../research/tensor_measurement_validation.json) records the effect cone, binary interval and finite POVMs with explicit saturation premises. '
              'The [countermodel receipt](../research/tensor_countermodel_validation.json) verifies the TFQ-0413 hypothesis boundaries.\n')
    for stage in fragment['stages']:
        stage_records = [r for r in records if r['stage'] == stage]
        index += f'\n### {stage} ({len(stage_records)} derivations)\n\n'
        index += '| ID | Name | Status | Parent | DAG node |\n|---|---|---|---|---|\n'
        for r in stage_records:
            paper = paper_paths[r['id']].removeprefix('dag/derivations/')
            parent = paper_paths[r['parent_id']].removeprefix('dag/derivations/')
            node_id = r['existing_derivation_dag_ids'][0]
            index += f'| [{r["id"]}](./{paper}) | {r["name"]} | `{r["record_status"]}` | [{r["parent_id"]}](./{parent}) | `{node_id}` |\n'
    if frontier_marker:  # the frontier section is owned by sync_frontier_branches.py
        index = index.rstrip('\n') + '\n\n' + frontier_marker + frontier_tail
    return index


if __name__ == '__main__':
    raise SystemExit(main())
