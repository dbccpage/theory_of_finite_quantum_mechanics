"""Check branch/source custody and synchronized graph/index integration."""
from pathlib import Path
import json
import re
import sys
import hashlib

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'dag'))
import sync_application_branches as sync
import validate_derivation_dag as validator


def fragment():
    return json.loads((ROOT / 'dag/fragments/application_branches.json').read_text(encoding='utf-8'))


def test_generated_indices_and_dag_match_fragment():
    for path, expected in sync.generated_files(ROOT).items():
        assert path.read_bytes() == expected, path


def test_branches_have_resolved_papers_parents_and_local_source_symbols():
    f = fragment()
    records = [json.loads(line) for line in (ROOT / 'dag/theory_of_finite_qm.jsonl').read_text(encoding='utf-8').splitlines()]
    ids = {r['id'] for r in records}
    pregenesis_to_wdp = json.loads((ROOT / 'dag/fragments/pregenesis_to_wdp.json').read_text(encoding='utf-8'))
    unified = json.loads((ROOT / 'dag/fragments/unified_dag.json').read_text(encoding='utf-8'))
    frontier = json.loads((ROOT / 'dag/fragments/frontier_branches.json').read_text(encoding='utf-8'))
    gth = json.loads((ROOT / 'dag/fragments/genesis_to_higher.json').read_text(encoding='utf-8'))
    assert len(ids) == len(records) == (397 + len(unified['node_records']) + len(pregenesis_to_wdp['records'])
                                        + len(f["records"]) + len(frontier['records']) + len(gth['records']))
    papers = list((ROOT / 'dag/derivations').rglob('tfq_*.md'))
    paper_ids = ['TFQ-' + re.match(r'tfq_(\d{4})_', p.name)[1] for p in papers]
    assert len(paper_ids) == len(set(paper_ids)) == len(records)
    assert set(paper_ids) == ids
    nodes = {n['id']: n for n in f['nodes']}
    for r in f['records']:
        assert r['parent_id'] in ids
        n = nodes[r['existing_derivation_dag_ids'][0]]
        assert r['stage'] == n['stage']
        assert (ROOT / n['source'][0]).is_file()
    for n in f['nodes']:
        for field in ('source', 'lean', 'rust'):
            for reference in n[field]:
                path, _, symbol = reference.partition('::')
                source = ROOT / path
                assert source.is_file(), reference
                if symbol:
                    # Same leaf rule as validate_derivation_dag.py: last segment after :: and after a dot.
                    leaf = symbol.split('::')[-1].split('.')[-1]
                    assert re.search(r'\b' + re.escape(leaf) + r'\b', source.read_text(encoding='utf-8')), reference
    assert {r['stage'] for r in f['records']} == set(f['stages'])


def test_application_routes_connect_to_existing_dag_without_cycles():
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    assert validator.check(graph, None) == []
    f = fragment()
    old_ids = {n['id'] for n in graph['nodes']} - {n['id'] for n in f['nodes']}
    for stage in f['stages']:
        branch_ids = {n['id'] for n in f['nodes'] if n['stage'] == stage}
        assert any(r['output'] in branch_ids and set(r['inputs']) & old_ids for r in f['routes'])
    # An accidental back-edge from the shared carrier into the new theorem is caught.
    graph['routes'].append(dict(id='mutation-back-edge',inputs=['DFM-GENERAL-GRAPH-DRESSING'],
        output='FQ-CARRIER-CONTRACT-V2',status='DERIVED_PROSE',source=['external:test']))
    assert any('cycle among nodes' in error for error in validator.check(graph, None))


def test_application_paper_and_index_links_resolve():
    files = [ROOT / n['source'][0] for n in fragment()['nodes']]
    index = ROOT / 'dag/derivations/README.md'
    # Earlier index text is outside this addition's custody.
    sections = [(p, p.read_text(encoding='utf-8')) for p in files]
    sections.append((index, index.read_text(encoding='utf-8').split(sync.MARKER)[1]))
    for paper, text in sections:
        for reference in re.findall(r'\]\(([^)]+)\)', text):
            if reference.startswith(('https://', 'http://')):
                continue
            assert (paper.parent / reference.split('#')[0]).is_file(), (paper, reference)


def test_nf002_count_is_current_and_global_obligations_stay_open():
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    nodes = {n['id']: n for n in graph['nodes']}
    nf = nodes['IMPL-FSP-SWITCHING-NORMAL-FORM-NF002']
    assert nf['statement'] == fragment()['nf002_statement']
    assert 'normalForms_length' in nf['statement']
    assert 'one residual' not in nf['statement'] and 'draft PR' not in nf['statement']
    for name in ('MUB6-GLOBAL-OBLIGATIONS', 'FSP-EFFICIENT-SAMPLING-OBLIGATIONS',
                 'DFM-HIERARCHICAL-BOREL', 'DFM-CONTINUUM-INTERFACE'):
        assert nodes[name]['status'] == 'OPEN'
    for name in ('DFM-GENERAL-GRAPH-DRESSING', 'DFM-TREE-CHANGE'):
        assert nodes[name]['status'] == 'PROVED_LEAN'
    lean = (ROOT / 'lean4/FiniteGraphDressing.lean').read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit|axiom)\b', lean)


def test_nf002_port_preserves_sealed_source_except_conditional_lemma_spellings():
    f = fragment()
    raw = (ROOT / f['nf002_source']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == f['nf002_sealed_sha256']
    expected = raw.decode('utf-8').replace('\r\n', '\n')
    substitutions = [
        (r'ite_eq_left_of_eq_true _ _ \(eq_true ([A-Za-z0-9_]+)\)', r'if_pos \1'),
        (r'ite_eq_right_of_eq_false _ _ \(eq_false ([A-Za-z0-9_]+)\)', r'if_neg \1'),
        (r'dite_eq_left_of_eq_true \(eq_true ⟨v, h⟩\)', r'dif_pos ⟨v, h⟩'),
        (r'dite_eq_right_of_eq_false \(eq_false e\.2\)', r'dif_neg e.2'),
    ]
    counts = []
    for pattern, replacement in substitutions:
        expected, count = re.subn(pattern, replacement, expected)
        counts.append(count)
    assert counts == [9, 8, 1, 1]
    port = (ROOT / f['nf002_replay_source']).read_text(encoding='utf-8')
    port = re.sub(r'\n/- Compatibility port of the sealed NF-002 source\..*?-/\n', '', port, count=1, flags=re.S)
    assert port == expected


def test_tensor_proof_boundaries_and_conditional_gap():
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    nodes = {n['id']: n for n in graph['nodes']}
    assert nodes['FQ-GAP-TENSOR-UNIQUENESS']['status'] == 'CONDITIONAL'
    assert nodes['TENSOR-CONE-ORBIT-KERNEL']['status'] == 'PROVED_LEAN'
    for name in ('TENSOR-TOMOGRAPHIC-COORDINATES',
                 'TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION'):
        assert nodes[name]['status'] == 'PROVED_LEAN'
    assert nodes['TENSOR-ASSUMPTION-COUNTERMODELS']['status'] == 'PROVED_LEAN'
    gap = nodes['FQ-GAP-TENSOR-UNIQUENESS']
    update = fragment()['tensor_uniqueness_update']
    for field in ('statement', 'source_status', 'bottleneck', 'imported_structure'):
        assert gap[field] == update[field]
    assert 'tensor composition (assumption)' not in gap['imported_structure']
    lean = (ROOT / 'lean4/TensorConeReconstruction.lean').read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit|axiom)\b', lean)
    assert 'reachability : ∀ v' in lean
    assert 'variable {n : Type*} [Fintype n]' in lean


def test_tensor_lean_replay_matches_sources_and_admission_policy():
    receipt = json.loads((ROOT / 'dag/research/tensor_formalization_validation.json').read_text(encoding='utf-8'))
    replay = receipt['lean_replay']
    modules = {'TensorConeReconstruction', 'TensorTomography', 'TensorCoordinates',
               'TensorSchmidt', 'TensorReachability', 'TensorOperationalCone', 'TensorComposition'}
    assert len(replay['results']) == len(modules)
    assert {r['module'] for r in replay['results']} == modules
    assert '4.35.0' in replay['lean_version']
    assert replay['mathlib_source_sha'] == '56a005855ea17e0b0958f73ec801ae140b0a1679'
    for result in replay['results']:
        raw = (ROOT / f"lean4/{result['module']}.lean").read_bytes()
        assert hashlib.sha256(raw).hexdigest() == result['sha256']
        code = re.sub(r'/\-.*?\-/|--[^\n]*', '', raw.decode('utf-8'), flags=re.S)
        assert not re.search(r'\b(sorry|admit|axiom|sorryAx|unsafe)\b', code)
        assert result['exit_code'] == 0 and result['axiom_audit_passed'] is True
        lists = re.findall(r'depends on axioms: \[([^]]*)\]', result['output'])
        assert lists
        assert all(set(names.split(', ')) <= {'propext', 'Classical.choice', 'Quot.sound'} for names in lists)
