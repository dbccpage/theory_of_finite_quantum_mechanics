"""Synchronize the application-branch fragment into the DAG and two master indices.

Only the fragment-owned suffix is generated; pre-existing derivation papers and
records are preserved. --check detects stale generated data without writing.
AuthorityEffect: None. Synchronization does not establish a mathematical claim.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARKER = '<!-- application-branches: generated from fragments/application_branches.json -->'


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


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
    dag = json.loads((folder / 'derivation_dag.json').read_text(encoding='utf-8'))
    # Reject accidental capture of a node not previously owned by this fragment.
    for n in dag['nodes']:
        if n['id'] in ids and 'application-branch' not in n['tags']:
            raise ValueError('application node collides with existing node: ' + n['id'])
    dag['nodes'] = [n for n in dag['nodes'] if n['id'] not in ids] + nodes
    route_ids = {r['id'] for r in routes}
    dag['routes'] = [r for r in dag['routes'] if r['id'] not in route_ids] + routes
    for stage in fragment['stages']:
        if stage not in dag['stages']:
            dag['stages'].append(stage)
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

    # Preserve upstream records byte-for-byte, including their line endings.
    old_lines = (folder / 'theory_of_finite_qm.jsonl').read_bytes().decode('utf-8').splitlines(keepends=True)
    old_records = [json.loads(line) for line in old_lines]
    retained_lines = [line for line, r in zip(old_lines, old_records) if r['id'] not in record_ids]
    newline = '\r\n' if old_lines and old_lines[0].endswith('\r\n') else '\n'
    for r in old_records:
        if r['id'] in record_ids and r.get('source_slice') != 'application_branches':
            raise ValueError('application record collides with existing record: ' + r['id'])
    all_records = [r for r in old_records if r['id'] not in record_ids] + records
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

    index = strip_suffix((folder / 'derivations/README.md').read_text(encoding='utf-8'))
    index += '\n' + MARKER + '\n\n## Application and composition derivation branches\n\n'
    index += ('These branches attach to existing finite carriers. A proved theorem has its stated hypotheses; '
              'an open research target remains open. See the [branch fragment](../fragments/application_branches.json) '
              'and the [initial application receipt](../research/application_branches_validation.json). '
              'The [tensor receipt](../research/tensor_composition_validation.json) is the historical prose/kernel snapshot; '
              'the [formalization receipt](../research/tensor_formalization_validation.json) records the verified tomography and Schmidt extension. '
              'The [measurement receipt](../research/tensor_measurement_validation.json) records the effect cone, binary interval and finite POVMs with explicit saturation premises.\n')
    master = strip_suffix((folder / 'theory_of_finite_qm.md').read_text(encoding='utf-8'))
    master = re.sub(r'Nodes: \d+\.', f'Nodes: {len(all_records)}.', master, count=1)
    for stage in fragment['stages']:
        master = re.sub(r'^\| `' + stage + r'` \| \d+ \|\n', '', master, flags=re.M)
    stage_rows = ''.join(f'| `{stage}` | {sum(r["stage"] == stage for r in records)} |\n' for stage in fragment['stages'])
    heading = master.index('## Coda atlas packages')
    master = master[:heading].rstrip() + '\n' + stage_rows + '\n' + master[heading:]
    master += '\n' + MARKER + '\n'
    for stage in fragment['stages']:
        stage_records = [r for r in records if r['stage'] == stage]
        index += f'\n### {stage} ({len(stage_records)} derivations)\n\n'
        index += '| ID | Name | Status | Parent | DAG node |\n|---|---|---|---|---|\n'
        master += f'\n## {stage}\n'
        for r in stage_records:
            paper = paper_paths[r['id']].removeprefix('dag/derivations/')
            parent = paper_paths[r['parent_id']].removeprefix('dag/derivations/')
            node_id = r['existing_derivation_dag_ids'][0]
            index += f'| [{r["id"]}](./{paper}) | {r["name"]} | `{r["record_status"]}` | [{r["parent_id"]}](./{parent}) | `{node_id}` |\n'
            master += (f'\n### {r["id"]} {r["name"]}\n\n'
                       f'- UUID: `{r["uuid"]}`\n- Parent: `{r["parent_id"]}`\n'
                       f'- Status: `{r["record_status"]}`\n- DAG node: `{node_id}`\n'
                       f'- Paper: [derivation](derivations/{paper})\n\n'
                       f'{r["summary"]}\n\nObligation: {r["obligation"]}\n')
    return {
        folder / 'derivation_dag.json': json_text(dag),
        folder / 'theory_of_finite_qm.jsonl': ''.join(retained_lines) + ''.join(
            json.dumps(r, ensure_ascii=False, sort_keys=True) + newline for r in records),
        folder / 'theory_of_finite_qm.md': master,
        folder / 'derivations/README.md': index,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    differences = []
    for path, expected in generated_files(HERE.parent).items():
        if path.read_bytes() != expected.encode('utf-8'):
            differences.append(path.name)
            if not args.check:
                path.write_bytes(expected.encode('utf-8'))
    print('stale=' + ','.join(differences) if differences else 'application branches synchronized')
    return int(bool(differences) and args.check)


if __name__ == '__main__':
    raise SystemExit(main())
