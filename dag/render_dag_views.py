"""Render the two read-only views of dag/derivation_dag.json: theory_of_finite_qm.jsonl and .md.

derivation_dag.json (schema derivation_dag.v2) is the single source of the derivation graph: its
nodes and routes, its TFQ records (top-level key records) and the hand-authored text of the
Markdown index (top-level key index_document). The two files rendered here are views of it:

- dag/theory_of_finite_qm.jsonl: one line per record, in the order of records, each line the record
  as JSON with sorted keys and non-ASCII characters kept, ended by CRLF;
- dag/theory_of_finite_qm.md: the header, the stage index (record count per stage), the Coda atlas
  package table, the record-to-node crosswalk and one section per stage listing its records.

Never edit the views by hand: edit derivation_dag.json (or the fragment a sync script owns) and run
the syncs, which call this renderer. Run order: sync_pfp_results.py, sync_unified_dag.py,
sync_application_branches.py, sync_pregenesis_to_wdp.py, sync_frontier_branches.py,
sync_genesis_to_higher.py, sync_foc035_observer_presheaf.py; each of them writes
derivation_dag.json and then the views. Run this script alone after a hand edit of derivation_dag.json.

    python -I -X utf8 dag/render_dag_views.py --check   # exit 1 when a view on disk differs
    python -I -X utf8 dag/render_dag_views.py --write   # rewrite the views that differ

AuthorityEffect: None. Rendering does not establish a mathematical claim.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DAG_PATH = 'dag/derivation_dag.json'
JSONL_PATH = 'dag/theory_of_finite_qm.jsonl'
MD_PATH = 'dag/theory_of_finite_qm.md'
JSONL_NEWLINE = '\r\n'
SCHEMA_VERSION = 'derivation_dag.v2'
APP_MARKER = '<!-- application-branches: generated from fragments/application_branches.json -->'
XWALK_BEGIN = '<!-- unified-dag:crosswalk:begin -->'
XWALK_END = '<!-- unified-dag:crosswalk:end -->'
# Stage sections that list every non-application record in the plain layout (the stages whose
# sections dag/sync_pregenesis_to_wdp.py owned). Other trunk stages list their unified_dag records
# in a delimited block after the other records.
PLAIN_STAGES = ('PREGENESIS', 'GENESIS', 'AUTHORIZATION', 'MSSN_SN', 'WDP')
UNIFIED_SLICE = 'unified_dag'
APP_SLICE = 'application_branches'
FRONTIER_SLICE = 'frontier_branches'
FRONTIER_MARKER = '<!-- frontier-branches: generated from fragments/frontier_branches.json -->'
GTH_SLICE = 'genesis_to_higher'
GTH_MARKER = '<!-- genesis-to-higher: generated from fragments/genesis_to_higher.json -->'
GTH_TAG = 'genesis-to-higher'
GTH_ROUTE_PREFIX = 'GTH-R-'
GTH_STAGE = 'GENESIS_TO_HIGHER'
OPS_SLICE = 'foc035_observer_presheaf'
OPS_MARKER = '<!-- foc035-observer-presheaf: generated from fragments/foc035_observer_presheaf.json -->'
OPS_TAG = 'foc035-observer-presheaf'
OPS_ROUTE_PREFIX = 'OPS-R-'
OPS_STAGE = 'OBSERVER_PRESHEAF'
# Records of these slices are listed after APP_MARKER, one section per application stage.
APP_SLICES = (APP_SLICE, FRONTIER_SLICE, GTH_SLICE, OPS_SLICE)
PGW_SLICE = 'pregenesis_to_wdp'
DOMAIN_TAG = 'source-corpus'


def json_text(value) -> str:
    """The byte layout of derivation_dag.json and the fragment files."""
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def record_line(record: dict) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True) + JSONL_NEWLINE


def canonical_record(record: dict) -> dict:
    """A record as stored in derivation_dag.json: keys sorted, as in its JSONL line."""
    return dict(sorted(record.items()))


def load_dag(root: Path = ROOT) -> dict:
    return json.loads((Path(root) / DAG_PATH).read_text(encoding='utf-8'))


def records_of(root: Path = ROOT) -> list[dict]:
    """The TFQ records of the single source (read-only consumers may also read the JSONL view)."""
    return load_dag(root)['records']


# ---------------------------------------------------------------------------------------------
# JSONL view.

def render_jsonl(dag: dict) -> str:
    return ''.join(record_line(r) for r in dag['records'])


# ---------------------------------------------------------------------------------------------
# Markdown view.

def _plain_block(r: dict) -> str:
    head = [f'### {r["id"]} {r["name"]}', '', f'- UUID: `{r["uuid"]}`',
            f'- Parent: `{r["parent_id"] or "root"}`', f'- Status: `{r["record_status"]}`']
    if r['coda_atlas_ids']:
        head.append('- Coda atlas: ' + ', '.join(f'`{x}`' for x in r['coda_atlas_ids']))
    if r['coda_atlas_paths']:
        head += ['- Atlas paths:', *[f'  - `{x}`' for x in r['coda_atlas_paths']]]
    return '\n'.join(head) + '\n\n' + r['summary'] + '\n\nObligation: ' + r['obligation'] + '\n'


def _unified_block(r: dict, node: dict) -> str:
    return (f'\n### {r["id"]} {r["name"]}\n\n- UUID: `{r["uuid"]}`\n- Parent: `{r["parent_id"]}`\n'
            f'- Status: `{r["record_status"]}`\n- DAG node: `{node["id"]}` (`{node["status"]}`)\n\n'
            f'{r["summary"]}\n\nObligation: {r["obligation"]}\n')


def _application_block(r: dict) -> str:
    paper = r['f004_refs'][0].removeprefix('dag/derivations/')
    return (f'\n### {r["id"]} {r["name"]}\n\n'
            f'- UUID: `{r["uuid"]}`\n- Parent: `{r["parent_id"]}`\n'
            f'- Status: `{r["record_status"]}`\n- DAG node: `{r["existing_derivation_dag_ids"][0]}`\n'
            f'- Paper: [derivation](derivations/{paper})\n\n'
            f'{r["summary"]}\n\nObligation: {r["obligation"]}\n')


def _crosswalk(dag: dict, records: list[dict]) -> str:
    doc = dag['index_document']
    status = {n['id']: n['status'] for n in dag['nodes']}
    review_of = {n['id']: n['pfp_review'] for n in dag['nodes'] if 'pfp_review' in n}
    domain = sum(1 for n in dag['nodes'] if DOMAIN_TAG in n.get('tags', []))
    aliases = doc.get('source_corpus_restatements', [])
    rows = []
    for r in records:
        ids = [x for x in r['existing_derivation_dag_ids'] if x in status]
        if r['source_slice'] == PGW_SLICE and not ids:
            ids = ['PGW-' + r['name'].upper()]
        cells = ', '.join(f'`{x}` ({status.get(x, "?")})' for x in ids)
        reviewed = [x for x in ids if x in review_of]

        def label(x):
            return f'{review_of[x]["verdict"]} / {review_of[x]["scope_effect"]}'
        review_cell = '; '.join(label(x) if len(reviewed) == 1 else f'`{x}`: {label(x)}' for x in reviewed) or '-'
        rows.append(f'| `{r["id"]}` | `{r["stage"]}` | `{r["record_status"]}` | {cells} | {review_cell} |')
    out = [XWALK_BEGIN, '## Unified derivation graph', '',
           'Generated by `dag/sync_unified_dag.py`. `derivation_dag.json`, this file and '
           '`theory_of_finite_qm.jsonl` describe one graph: every record names at least one DAG node and every '
           'DAG node is named by at least one record. A record that named no node has a node with its own id '
           '(tag `unified-dag`); a node that no record named has a record from `TFQ-1000` upward. '
           f'Records: {len(records)}. DAG nodes: {len(status)}. '
           f'Source-corpus records folded in: {domain} new, {len(aliases)} trunk restatements.', '',
           'The Review column names the verdict and scope effect of the PFP review of each reviewed node '
           '(`dag/fragments/pfp_review_decisions.json`, written by `dag/sync_pfp_results.py`); the node status '
           'in the previous column is the status after that review.', '',
           '### Record to node crosswalk', '',
           '| Record | Stage | Record status | DAG node (status) | Review |',
           '|---|---|---|---|---|', *rows, '']
    if aliases:
        out += ['### Source-corpus trunk restatements', '',
                'These source records restate a trunk step; the trunk node carries an `alias:` tag.', '',
                '| Source record | Corpus | Trunk node or record | Note |', '|---|---|---|---|',
                *[f'| `{a["source_id"]}` | `{a["corpus"]}` | `{a["alias_of"]}` | '
                  f'{a.get("alias_note", "").replace("|", chr(92) + "|")} |' for a in aliases], '']
    out.append(XWALK_END)
    return '\n'.join(out) + '\n'


def _trunk_section(stage: str, records: list[dict], nodes: dict) -> str:
    mine = [r for r in records if r['stage'] == stage and r['source_slice'] not in APP_SLICES]
    if stage in PLAIN_STAGES:
        return f'## {stage}\n\n' + '\n'.join(_plain_block(r) for r in mine)
    plain = [r for r in mine if r['source_slice'] != UNIFIED_SLICE]
    unified = [r for r in mine if r['source_slice'] == UNIFIED_SLICE]
    text = f'## {stage}\n\n' + '\n'.join(_plain_block(r) for r in plain)
    if unified:
        # A unified_dag record was made for a node that no record named; it names that node first.
        body = ''.join(_unified_block(r, nodes[r['existing_derivation_dag_ids'][0]]) for r in unified)
        text = (text.rstrip('\n') + '\n' + f'\n<!-- unified-dag:rows:{stage}:begin -->{body}'
                f'<!-- unified-dag:rows:{stage}:end -->\n')
    return text


def render_md(dag: dict) -> str:
    doc = dag['index_document']
    records = dag['records']
    nodes = {n['id']: n for n in dag['nodes']}
    trunk = doc['stage_index']
    app = doc['application_stages']
    sectioned = set(trunk) | set(app)
    unplaced = sorted({r['id'] for r in records if r['stage'] not in sectioned})
    if unplaced:
        raise ValueError('records whose stage has no section in index_document: ' + ', '.join(unplaced[:12]))
    misplaced = sorted(r['id'] for r in records if (r['source_slice'] in APP_SLICES) != (r['stage'] in app))
    if misplaced:
        raise ValueError('application records outside an application stage, or the reverse: ' + ', '.join(misplaced[:12]))
    count = {s: sum(1 for r in records if r['stage'] == s) for s in [*trunk, *app]}
    coda = doc['coda_atlas_packages']
    out = [doc['header_markdown'],
           f'Nodes: {len(records)}. {doc["record_count_note"]}\n\n',
           '## Stage index\n\n| Stage | Steps |\n| --- | ---: |\n',
           ''.join(f'| `{s}` | {count[s]} |\n' for s in [*trunk, *app]), '\n',
           f'## {coda["heading"]}\n\n| Floor | Shelf | Package | Path |\n| --- | --- | --- | --- |\n',
           ''.join(f'| {p["floor"]} | {p["shelf"]} | {p["package"]} | `{p["path"]}` |\n' for p in coda['rows']), '\n',
           _crosswalk(dag, records), '\n',
           '\n'.join(_trunk_section(s, records, nodes) for s in trunk),
           '\n' + APP_MARKER + '\n']
    for stage in app:
        out.append(f'\n## {stage}\n')
        out += [_application_block(r) for r in records if r['stage'] == stage]
    return ''.join(out)


# ---------------------------------------------------------------------------------------------
# Files.

def views(dag: dict, root: Path = ROOT) -> dict[Path, bytes]:
    root = Path(root)
    if dag.get('schema_version') != SCHEMA_VERSION:
        raise ValueError(f'{DAG_PATH}: schema_version {dag.get("schema_version")!r} is not {SCHEMA_VERSION}')
    return {root / JSONL_PATH: render_jsonl(dag).encode('utf-8'),
            root / MD_PATH: render_md(dag).encode('utf-8')}


def outputs(dag: dict, root: Path = ROOT) -> dict[Path, bytes]:
    """derivation_dag.json and both views, as a sync script writes them."""
    root = Path(root)
    return {root / DAG_PATH: json_text(dag).encode('utf-8'), **views(dag, root)}


def stale_views(root: Path = ROOT) -> list[str]:
    root = Path(root)
    return [path.relative_to(root).as_posix() for path, data in views(load_dag(root), root).items()
            if not path.is_file() or path.read_bytes() != data]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='report views that differ from derivation_dag.json')
    mode.add_argument('--write', action='store_true', help='rewrite the views that differ')
    parser.add_argument('--repo-root', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.repo_root
    differences = []
    for path, data in views(load_dag(root), root).items():
        if not path.is_file() or path.read_bytes() != data:
            differences.append(path.relative_to(root).as_posix())
            if args.write:
                path.write_bytes(data)
    print('stale=' + ','.join(differences) if differences else 'views match derivation_dag.json')
    return int(bool(differences) and args.check)


if __name__ == '__main__':
    raise SystemExit(main())
