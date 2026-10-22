"""Check the frontier-branch fragment: custody, honesty of statuses, graph connection and synchronization."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'dag'))
import sync_frontier_branches as sync
import validate_derivation_dag as validator

EXTERNAL_STATUSES = {'SOURCE_RECORD', 'IMPORTED_ASSUMPTION', 'OPEN'}
LEAN_ANCHORS = {'CQFT-FINITE-STRICT-POSET-SPACELIKE', 'CQFT-NO-SIGNALLING-PRODUCT-LEAN'}


def fragment():
    return json.loads((ROOT / 'dag/fragments/frontier_branches.json').read_text(encoding='utf-8'))


def test_generated_files_match_fragment():
    for path, expected in sync.generated_files(ROOT).items():
        assert path.read_bytes() == expected, path


def test_fragment_counts_and_stages():
    f = fragment()
    assert f['stages'] == ['CONSTRUCTOR_THEORY', 'CAUSAL_QFT', 'ADS_CFT', 'LOOP_QUANTUM_GRAVITY']
    assert {n['stage'] for n in f['nodes']} == set(f['stages']) == {r['stage'] for r in f['records']}
    assert len(f['nodes']) == len(f['records']) == 58 and len(f['routes']) == 66
    assert all(r['source_slice'] == 'frontier_branches' for r in f['records'])


def test_external_results_are_never_derived_statuses():
    for n in fragment()['nodes']:
        if n['status'] in ('PROVED_LEAN', 'DEFINITION'):
            # Only repository declarations: the two Lean anchors, the finite causal-set definition, and the 14 finite targets.
            assert (n['id'] in LEAN_ANCHORS or n['id'] == 'CQFT-FINITE-CAUSET-IDENTIFICATION'
                    or 'finite-target' in n['tags']), n['id']
            assert not ({'external-source', 'external-import'} & set(n['tags'])), n['id']
            if n['id'] in LEAN_ANCHORS:
                assert not any(s.startswith('external:') for s in n['source'][1:])
        else:
            assert n['status'] in EXTERNAL_STATUSES, n['id']
        if n['status'] in ('SOURCE_RECORD', 'IMPORTED_ASSUMPTION'):
            assert any(s.startswith('external:') for s in n['source']), n['id']


def test_citations_resolve_and_use_identifier_spellings():
    f = fragment()
    refs = {c['ref'] for c in f['citations'].values()}
    pattern = re.compile(r'external:(arXiv:[a-z\-]*/?\d+(\.\d+)?|doi:10\.\S+|numdam:\S+|book:\S+|Nuovo-Cimento-\S+)')
    assert all(pattern.fullmatch(ref) for ref in refs), refs
    used = {s for n in f['nodes'] for s in n['source'] if s.startswith('external:')}
    assert used == refs
    # The arXiv identifiers were checked against the arXiv records on 2026-10-21.
    expected = {'1210.7439', '1405.5563', '1507.03287', '1608.02625', '1707.06036', '1707.06050', 'math-ph/9903028',
                'gr-qc/0309009', 'gr-qc/0207103', 'hep-th/9711200', 'hep-th/9802109', 'hep-th/9802150',
                'hep-th/0603001', '1411.7041', '1607.03901', '1503.06237', 'quant-ph/9602019', 'gr-qc/9505006',
                'gr-qc/9411005', 'gr-qc/9602046', 'math-ph/9812013', '0711.0146', '0708.1595', '1205.2019'}
    assert {r.removeprefix('external:arXiv:') for r in refs if r.startswith('external:arXiv:')} == expected


def test_open_nodes_have_only_gap_routes_and_targets_are_precise():
    f = fragment()
    for n in f['nodes']:
        incoming = [r for r in f['routes'] if r['output'] == n['id']]
        assert incoming, n['id']
        if n['status'] == 'OPEN':
            assert all(r['status'] == 'GAP_NO_DERIVATION' for r in incoming), n['id']
        if 'finite-target' in n['tags']:
            assert len(f['paper_notes'][n['id']]['target']) > 100, n['id']
    for stage in f['stages']:
        targets = [n for n in f['nodes'] if n['stage'] == stage and 'finite-target' in n['tags']]
        assert 2 <= len(targets) <= 4, (stage, len(targets))
    for r in f['routes']:
        if r['id'].startswith('FRO-R-BACK-'):
            assert r['status'] == 'GAP_NO_DERIVATION'


def test_routes_connect_each_stage_to_the_existing_graph_without_cycles():
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    assert validator.check(graph, None) == []
    f = fragment()
    mine = {n['id'] for n in f['nodes']}
    old_ids = {n['id'] for n in graph['nodes']} - mine
    for stage in f['stages']:
        branch = {n['id'] for n in f['nodes'] if n['stage'] == stage}
        assert any(r['output'] in branch and set(r['inputs']) & old_ids for r in f['routes']), stage
    graph['routes'].append(dict(id='mutation-back-edge', inputs=['CT-QUBIT-NO-CLONING-FINITE-TARGET'],
                                output='FQ-DECLARED-QUANTUM-INTERFACE', status='GAP_NO_DERIVATION'))
    assert any('cycle among nodes' in error for error in validator.check(graph, None))


def test_lean_anchors_cite_declarations_that_exist():
    f = fragment()
    for n in f['nodes']:
        if n['id'] in LEAN_ANCHORS or 'finite-target' in n['tags']:
            assert n['lean'] and n['status'] == 'PROVED_LEAN'
            for reference in n['lean']:
                path, _, symbol = reference.partition('::')
                leaf = symbol.split('.')[-1]
                text = (ROOT / path).read_text(encoding='utf-8')
                assert re.search(r'\b' + re.escape(leaf) + r'\b', text), reference
                assert not re.search(r'\b(sorry|admit)\b', re.sub(r'/\-.*?\-/|--[^\n]*', '', text, flags=re.S)), path


def test_papers_exist_and_do_not_use_forbidden_words():
    f = fragment()
    for r in f['records']:
        text = (ROOT / r['f004_refs'][0]).read_text(encoding='utf-8')
        assert text.startswith(f'# [{r["id"]}] {r["name"]}\n')
        assert '\r' not in text
        for heading in ('## Statement', '## What is imported', '## What is open', '## Non-claims', '## Sources'):
            assert heading in text, (r['id'], heading)
        assert sync.forbidden_words(text) == [], r['id']
