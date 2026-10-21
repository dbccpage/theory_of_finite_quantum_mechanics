"""Check that the PFP reviews are incorporated into the DAG and the JSONL without status promotion.

AuthorityEffect: None. These tests check synchronization and custody of review text; they do not
check that any review or any node statement is true.
"""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'dag'))
import sync_pfp_results as pfp
import validate_derivation_dag as validator

REVIEW_FILES = ('final_delivery_review_result.json', 'delivery_review_result.json', 'review_result.json',
                'audit_results.json', 'findings.json')
GENERATED_SLICES = ('unified_dag', 'pregenesis_to_wdp', 'application_branches')


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def reviewed_folders():
    """Result folders that hold at least one review file; batches and custody are not nodes."""
    found = set()
    for folder in (ROOT / 'dag/results').iterdir():
        reviews = folder / 'reviews'
        if folder.name not in ('batches', 'custody') and reviews.is_dir() and any(
                (sub / name).exists() for sub in reviews.iterdir() if sub.is_dir() for name in REVIEW_FILES):
            found.add(folder.name)
    return found


def nodes_by_id():
    return {n['id']: n for n in load('dag/derivation_dag.json')['nodes']}


def test_review_synchronization_is_a_fixed_point():
    for path, expected in pfp.generated_files(ROOT).items():
        assert path.read_bytes() == expected, path


def test_applying_the_decisions_twice_changes_nothing():
    dag = load('dag/derivation_dag.json')
    before = copy.deepcopy(dag)
    assert pfp.apply_decisions(ROOT, dag, pfp.load_decisions(ROOT)) == []
    assert dag == before


def test_every_reviewed_node_has_a_pfp_review_and_only_those():
    nodes = nodes_by_id()
    reviewed = reviewed_folders()
    assert len(reviewed) >= 151  # 151 from the first nine batches, plus every later batch with a decision
    assert {i for i, n in nodes.items() if 'pfp_review' in n} == reviewed
    assert {e['node_id'] for e in pfp.load_decisions(ROOT)['decisions']} == reviewed


def test_no_status_is_promoted_relative_to_prior_status():
    for node_id, node in nodes_by_id().items():
        review = node.get('pfp_review')
        if review is None:
            continue
        rank = pfp.STATUS_RANK
        assert rank[node['status']] <= rank[review['prior_status']], node_id
        assert (node['status'] != review['prior_status']) == (review['scope_effect'] == 'status_lowered'), node_id
        if review['scope_effect'] == 'statement_narrowed':
            assert node['statement'] != review['prior_statement'], node_id


def test_decisions_cannot_raise_a_status():
    dag = load('dag/derivation_dag.json')
    decisions = pfp.load_decisions(ROOT)
    nodes = {n['id']: n for n in dag['nodes']}
    entry = next(e for e in decisions['decisions']
                 if e['scope_effect'] == 'consistent' and nodes[e['node_id']]['status'] == 'IMPORTED_ASSUMPTION')
    nodes[entry['node_id']].pop('pfp_review')
    entry['scope_effect'] = 'status_lowered'
    entry['status'] = 'PROVED_LEAN'
    errors = pfp.apply_decisions(ROOT, dag, decisions)
    assert len(errors) == 1 and 'raises IMPORTED_ASSUMPTION to PROVED_LEAN' in errors[0]


def test_review_sha256_values_match_the_review_files():
    for node_id, node in nodes_by_id().items():
        review = node.get('pfp_review')
        if review is None:
            continue
        data = (ROOT / review['review']).read_bytes()
        assert pfp.review_sha256(data) == review['review_sha256'], node_id
        assert validator.pfp_review_sha256(data) == review['review_sha256'], node_id
        assert review['review_refs'][-1] == review['review'], node_id
        for ref in review['review_refs'] + review['superseded_by']:
            assert (ROOT / ref).exists(), (node_id, ref)


def test_review_is_the_latest_review_file_of_its_folder():
    for node_id, node in nodes_by_id().items():
        review = node.get('pfp_review')
        if review is None:
            continue
        path = ROOT / review['review']
        folder = ROOT / 'dag/results' / node_id / 'reviews'
        assert path.parent.parent == folder, node_id
        latest = sorted(sub.name for sub in folder.iterdir() if sub.is_dir() and any((sub / f).exists() for f in REVIEW_FILES))[-1]
        assert path.parent.name == latest, node_id


def test_no_boilerplate_next_test_remains():
    boilerplate = set(pfp.load_decisions(ROOT)['boilerplate_next_test'])
    assert len(boilerplate) == 3
    for node_id, node in nodes_by_id().items():
        review = node.get('pfp_review')
        if review is None:
            continue
        assert review['next_test'] not in boilerplate, node_id
        assert review['next_test'] in (review['does_not_support'], review['next_test'])
        assert len(review['next_test']) > 20, node_id


def test_boilerplate_is_replaced_by_the_does_not_support_obligation():
    decisions = pfp.load_decisions(ROOT)
    boilerplate = decisions['boilerplate_next_test']
    replaced = 0
    for entry in decisions['decisions']:
        raw = pfp.find_text(json.loads((ROOT / entry['review']).read_text(encoding='utf-8')), 'next_test')
        review = nodes_by_id()[entry['node_id']]['pfp_review']
        if raw in boilerplate:
            assert review['next_test'] == review['does_not_support'], entry['node_id']
            replaced += 1
    assert replaced >= 130


def test_every_base_row_naming_a_reviewed_node_carries_review_refs():
    nodes = nodes_by_id()
    aliases = load('dag/fragments/unified_dag.json')['row_aliases']
    rows = [json.loads(x) for x in (ROOT / 'dag/theory_of_finite_qm.jsonl').read_text(encoding='utf-8').splitlines()]
    with_refs = 0
    for row in rows:
        ids = set(row['existing_derivation_dag_ids']) | set(aliases.get(row['id'], []))
        expected = sorted({ref for i in ids if 'pfp_review' in nodes.get(i, {}) for ref in nodes[i]['pfp_review']['review_refs']})
        if row['source_slice'] not in GENERATED_SLICES or row['source_slice'] == 'unified_dag':
            assert row.get('pfp_review_refs', []) == expected, row['id']
        with_refs += 'pfp_review_refs' in row
    assert with_refs > 100


def test_routes_into_a_lowered_node_are_not_stronger_than_the_node():
    graph = load('dag/derivation_dag.json')
    nodes = {n['id']: n for n in graph['nodes']}
    for route in graph['routes']:
        node = nodes[route['output']]
        review = node.get('pfp_review')
        if review is None or review['scope_effect'] != 'status_lowered':
            continue
        assert pfp.ROUTE_RANK[route['status']] <= pfp.ROUTE_RANK[pfp.ROUTE_FOR_STATUS[node['status']]], route['id']
        assert route['id'] in review['prior_route_status'] or route['status'] == pfp.ROUTE_FOR_STATUS[node['status']]


def test_packaged_graph_passes_the_validator_with_file_checks():
    graph = load('dag/derivation_dag.json')
    errors = validator.check({'nodes': [n for n in graph['nodes'] if 'pfp_review' in n], 'routes': []}, ROOT)
    assert [e for e in errors if 'pfp_review' in e] == []
