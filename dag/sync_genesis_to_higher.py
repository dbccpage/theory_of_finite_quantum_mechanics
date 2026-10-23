"""Synchronize the genesis-to-higher fragment into derivation_dag.json, its papers and the derivation index.

dag/fragments/genesis_to_higher.json holds one stage, GENESIS_TO_HIGHER. It attaches to the Genesis
admission gate PGW-GO-ADMISSION-GATE. Open steps and the three infinite imports use GAP_NO_DERIVATION.
GTH-LANG-LIMITS is PROVED_PROSE for a limit that does not mention the unfinished language; its route is
RECORD_PARENT (reading order, not a derivation from the admission gate). No node is PROVED_LEAN.

derivation_dag.json (schema derivation_dag.v2) is the single source of the graph. This script owns:

- the fragment's nodes (tag genesis-to-higher), routes (id prefix GTH-R-) and records (source_slice
  genesis_to_higher), which come last, after the frontier block;
- the stage GENESIS_TO_HIGHER at the end of index_document.application_stages;
- one generated derivation paper per record, under dag/derivations/34_genesis_to_higher;
- the section of dag/derivations/README.md after the line views.GTH_MARKER.

Run order: sync_pfp_results.py, sync_unified_dag.py, sync_application_branches.py, sync_pregenesis_to_wdp.py,
sync_frontier_branches.py, this script. --check detects stale generated data without writing.
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

SLICE = views.GTH_SLICE
MARKER = views.GTH_MARKER
TAG = views.GTH_TAG
ROUTE_PREFIX = views.GTH_ROUTE_PREFIX
STAGE = views.GTH_STAGE
FRAGMENT = 'dag/fragments/genesis_to_higher.json'
FOLDER = '34_genesis_to_higher'
FORBIDDEN = ('proves', 'guarantees', 'mathematically verifies', 'fundamentally', 'true intelligence', 'impossible',
             'universal', 'flawless', 'perfectly', 'clearly', 'obviously', 'simply', 'merely', 'weaponized')
EXTERNAL = ('external:', 'pr:')
ALLOWED_STATUS = ('OPEN', 'IMPORTED_ASSUMPTION', 'PROVED_PROSE')
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


def validate(fragment: dict, dag: dict) -> list[str]:
    errs: list[str] = []
    nodes, routes, records = fragment['nodes'], fragment['routes'], fragment['records']
    ids = {n['id'] for n in nodes}
    others = {n['id'] for n in dag['nodes'] if TAG not in n.get('tags', [])}
    if fragment.get('stages') != [STAGE]:
        errs.append('fragment stages must be exactly GENESIS_TO_HIGHER')
    if len(ids) != len(nodes):
        errs.append('duplicate genesis-to-higher node ids')
    if ids & others:
        errs.append('node collides with an existing node: ' + ', '.join(sorted(ids & others)))
    if len({r['id'] for r in records}) != len(records):
        errs.append('duplicate record ids')
    if len({r['id'] for r in routes}) != len(routes):
        errs.append('duplicate route ids')
    known = ids | others
    cited = {c['ref'] for c in fragment['citations'].values()}
    for n in nodes:
        if n['stage'] != STAGE:
            errs.append(f'{n["id"]}: stage {n["stage"]} is not {STAGE}')
        if n['status'] not in ALLOWED_STATUS:
            errs.append(f'{n["id"]}: status {n["status"]} is not allowed in this fragment')
        if n['status'] == 'PROVED_LEAN' or n['lean']:
            errs.append(f'{n["id"]}: this stage has no Lean proof')
        if TAG not in n['tags']:
            errs.append(f'{n["id"]}: missing tag {TAG}')
        for ref in n['source']:
            if ref.startswith('external:') and ref not in cited:
                errs.append(f'{n["id"]}: external source {ref} has no citation entry')
        if n['status'] == 'IMPORTED_ASSUMPTION':
            if not n['imported_structure']:
                errs.append(f'{n["id"]}: an import needs imported_structure')
            if not any(ref.startswith('external:') for ref in n['source']):
                errs.append(f'{n["id"]}: an import needs an external: source')
        if not any(s.startswith('dag/derivations/independent/gth_') for s in n['source']):
            errs.append(f'{n["id"]}: source does not name an independent note')
    for r in routes:
        if not r['id'].startswith(ROUTE_PREFIX) or r['output'] not in known or any(i not in known for i in r['inputs']):
            errs.append(f'route {r["id"]}: bad id or endpoint')
        if r['status'] == 'GAP_NO_DERIVATION' and r.get('source'):
            errs.append(f'route {r["id"]}: a gap route carries no source')
        if r['status'] != 'GAP_NO_DERIVATION' and not r.get('source'):
            errs.append(f'route {r["id"]}: non-gap route without source')
    for n in nodes:
        incoming = [r for r in routes if r['output'] == n['id']]
        if not incoming:
            errs.append(f'{n["id"]}: no incoming route')
        if n['status'] == 'OPEN' and any(r['status'] != 'GAP_NO_DERIVATION' for r in incoming):
            errs.append(f'{n["id"]}: an OPEN node may only have gap routes')
        if n['status'] == 'PROVED_PROSE' and all(r['status'] == 'GAP_NO_DERIVATION' for r in incoming):
            errs.append(f'{n["id"]}: PROVED_PROSE but every incoming route is a gap')
    if not any(r['output'] == 'GTH-SHADOW' and 'PGW-GO-ADMISSION-GATE' in r['inputs']
               and r['status'] == 'GAP_NO_DERIVATION' for r in routes):
        errs.append('GTH-SHADOW has no gap route from PGW-GO-ADMISSION-GATE')
    record_ids = {r['id'] for r in records}
    existing = {r['id'] for r in dag['records'] if r.get('source_slice') != SLICE}
    if record_ids & existing:
        errs.append('record id collides with an existing record')
    for r in records:
        if r['source_slice'] != SLICE or r['stage'] != STAGE:
            errs.append(f'{r["id"]}: bad slice or stage')
        if r['parent_id'] not in (record_ids | existing):
            errs.append(f'{r["id"]}: bad parent')
        if r['existing_derivation_dag_ids'] != [r['local_id']]:
            errs.append(f'{r["id"]}: record does not name its node')
    named = {x for r in records for x in r['existing_derivation_dag_ids']}
    if named != ids:
        errs.append('records and nodes of the fragment do not name each other')
    blob = json.dumps(fragment, ensure_ascii=False)
    errs += [f'forbidden word in fragment: {w}' for w in forbidden_words(blob)]
    return errs


def render_paper(node: dict, record: dict, fragment: dict, paths: dict[str, str]) -> str:
    me = paths[record['id']]
    parent = record['parent_id']
    note = next(s for s in node['source'] if s.startswith('dag/derivations/independent/'))
    routes_in = [r for r in fragment['routes'] if r['output'] == node['id']]
    out = [f'# [{record["id"]}] {record["name"]}', '',
           f'**Stage:** `{node["stage"]}` | **Status:** `{node["status"]}` | **AuthorityEffect:** None.', '',
           f'**Parent:** {link(me, paths[parent], parent)}  ',
           f'**DAG node:** `{node["id"]}`  ',
           f'**UUID:** `{record["uuid"]}`  ',
           f'**Independent note:** {link(me, note, Path(note).name)}', '',
           '*Generated by `dag/sync_genesis_to_higher.py` from `dag/fragments/genesis_to_higher.json`; edit the '
           'fragment, not this paper.*', '',
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
            '- Nothing in this paper is a Lean declaration.',
            '- An imported assumption is not a result of this repository.',
            '- A gap route marks a link that no source derives.',
            '- A reading-order route does not derive its output from its input.',
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
    errs = validate(fragment, dag)
    if errs:
        raise ValueError('genesis-to-higher fragment invalid:\n  ' + '\n  '.join(errs))
    nodes, routes, records = fragment['nodes'], fragment['routes'], fragment['records']
    ids = {n['id'] for n in nodes}
    route_ids = {r['id'] for r in routes}
    record_ids = {r['id'] for r in records}

    # sync_foc035_observer_presheaf.py owns the block after this one. Keep it last.
    ops_nodes = [n for n in dag['nodes'] if views.OPS_TAG in n.get('tags', [])]
    ops_routes = [r for r in dag['routes'] if r['id'].startswith(views.OPS_ROUTE_PREFIX)]
    ops_records = [r for r in dag['records'] if r.get('source_slice') == views.OPS_SLICE]
    dag['nodes'] = [n for n in dag['nodes'] if TAG not in n.get('tags', []) and n['id'] not in ids
                    and views.OPS_TAG not in n.get('tags', [])] + nodes + ops_nodes
    dag['routes'] = [r for r in dag['routes'] if not r['id'].startswith(ROUTE_PREFIX) and r['id'] not in route_ids
                     and not r['id'].startswith(views.OPS_ROUTE_PREFIX)] + routes + ops_routes
    if STAGE not in dag['stages']:
        dag['stages'].append(STAGE)
    kept = [r for r in dag['records'] if r.get('source_slice') not in (SLICE, views.OPS_SLICE)
            and r['id'] not in record_ids]
    dag['records'] = [views.canonical_record(r) for r in kept + records + ops_records]
    doc = dag['index_document']
    had_ops_stage = views.OPS_STAGE in doc['application_stages']
    doc['application_stages'] = [s for s in doc['application_stages'] if s not in (STAGE, views.OPS_STAGE)] + [STAGE]
    if had_ops_stage:
        doc['application_stages'].append(views.OPS_STAGE)
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
    ops_at = readme.find(views.OPS_MARKER)  # the observer-presheaf section is owned by its own sync script
    ops_tail = readme[ops_at:] if ops_at >= 0 else ''
    section = '\n\n' + MARKER + '\n\n## Genesis to higher categories\n\n'
    section += ('This stage records open steps and named imports from the Genesis admission gate toward finite '
                'shadows, truncation, horn fillers, a finite identity-type model, three infinite imports, and a '
                'priced-import language. An imported assumption is not a result of this repository. A gap route '
                'marks a link that no source derives. The limit node states Gödel-Rosser and Tarski under hypotheses '
                'that do not mention the unfinished language; its route is reading order. See the '
                '[branch fragment](../fragments/genesis_to_higher.json).\n')
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
    readme_text = base + section
    if ops_tail:
        readme_text = readme_text.rstrip('\n') + '\n\n' + ops_tail
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
    print('stale=' + ','.join(differences) if differences else 'genesis-to-higher synchronized')
    return int(bool(differences) and args.check)


if __name__ == '__main__':
    raise SystemExit(main())
