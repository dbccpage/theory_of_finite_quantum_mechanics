"""Check the FOC-035 observer-presheaf fragment: ledger coverage, honest statuses, custody and synchronization."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'dag'))
import sync_foc035_observer_presheaf as sync  # noqa: E402
import validate_derivation_dag as validator  # noqa: E402

LEDGER = ROOT / 'sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md'
NOTE = LEDGER.with_name('lggr_and_the_quantum_observer_presheaf.md')
EXPECTED_STATUS = {
    'DEFINITION': {'OPS-OBSERVER-TUPLE'},
    'PROVED_LEAN': {'OPS-PUSHFORWARD-FUNCTOR-LEAN', 'OPS-PARITY-HOLONOMY-LEAN'},
    'PROVED_PROSE': {'OPS-UNDERDETERMINATION', 'OPS-NCF-LHV-EQUIVALENCE', 'OPS-STRONG-CONTEXTUALITY-NCF-ZERO',
                     'OPS-MAXIMAL-COVER-DESCENT', 'OPS-NGE-NOT-CONTEXTUALITY', 'OPS-CECH-COBOUNDARY',
                     'OPS-ZERO-COCYCLE-BLIND'},
    'COMPUTATIONALLY_CHECKED': {'OPS-NOISY-PR-NCF', 'OPS-ARC-COVER-NGE-WITNESS', 'OPS-PARITY-CYCLE-DESCENT-NCF',
                                'OPS-VOROBEV-PATH-INSTANCE', 'OPS-TEST-482-REPAIR', 'OPS-THREE-ROLE-GATE',
                                'OPS-SELF-CERTIFICATION-PACKET'},
    'CONDITIONAL': {'OPS-OBSERVER-DECLARATION-REFUSAL', 'OPS-RUST-RECEIPTS-AND-LIMITS',
                    'OPS-AXIS3-RELABELING', 'OPS-REGRESS-COROLLARY'},
    'IMPORTED_ASSUMPTION': {'OPS-NO-SIGNALLING-SIGNED-SECTION', 'OPS-Z2-WITNESS-FALSE-NEGATIVES',
                            'OPS-VOROBEV-THEOREM', 'OPS-AXIS1-WELLFOUNDED-ADMISSION', 'OPS-AXIS2-META-CARRIER'},
    'OPEN': {'OPS-LEAN-GAP'},
    'REFUTED': {'OPS-REFUTED-AXIS3-WIDE', 'OPS-REFUTED-NB9', 'OPS-REFUTED-EARLIER-GATE', 'OPS-REFUTED-EARLIER-RUST'},
    'SOURCE_RECORD': {'OPS-AP-CARD-PROPOSAL', 'OPS-PR1050-ABSENCE'},
}


def fragment():
    return json.loads((ROOT / 'dag/fragments/foc035_observer_presheaf.json').read_text(encoding='utf-8'))


def test_generated_files_match_fragment():
    for path, expected in sync.generated_files(ROOT).items():
        assert path.read_bytes() == expected, path


def test_statuses_follow_the_evidence():
    f = fragment()
    assert f['stages'] == ['OBSERVER_PRESHEAF']
    by_id = {n['id']: n for n in f['nodes']}
    assert len(f['nodes']) == len(f['records']) == 33 and len(f['routes']) == 37
    for status, ids in EXPECTED_STATUS.items():
        assert {i for i, n in by_id.items() if n['status'] == status} == ids, status
    for nid, node in by_id.items():
        if node['status'] == 'PROVED_LEAN':
            assert node['lean'] and all(x.startswith('lean4/LggrFiniteResults.lean::') for x in node['lean'])
            receipt_path = 'dag/research/foc035_observer_presheaf_lean_replay.json'
            assert receipt_path in node['source']
            receipt = json.loads((ROOT / receipt_path).read_text(encoding='utf-8'))
            entry = next(e for e in receipt['lean_replay']['results'] if e['dag_node'] == nid)
            assert entry['sha256'] == hashlib.sha256((ROOT / entry['source']).read_bytes()).hexdigest()
            assert entry['exit_code'] == 0 and entry['axiom_audit_passed']
            assert set(entry['anchors']) == {ref.split('::')[1] for ref in node['lean']}
            assert all(set(report['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
                       for report in entry['axiom_reports'])
        elif nid == 'OPS-RUST-RECEIPTS-AND-LIMITS':
            assert node['lean'] and all(
                x.startswith('lean4/CampaignOpsRustReceiptsAndLimits.lean::') for x in node['lean'])
            receipt_path = 'dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json'
            assert receipt_path in node['source']
            receipt = json.loads((ROOT / receipt_path).read_text(encoding='utf-8'))
            entry = receipt['lean_replay']['results'][0]
            assert entry['dag_node'] == nid
            assert entry['source'] == sync.CAMPAIGN_CEILING
            expected_audit = set(entry['anchors']) | {
                'CampaignOpsRustReceiptsAndLimits.maxGlobal',
                'CampaignOpsRustReceiptsAndLimits.maxLp',
            }
            assert set(entry['axioms']) == expected_audit
            assert entry['sha256'] == hashlib.sha256((ROOT / entry['source']).read_bytes()).hexdigest()
            assert entry['exit_code'] == 0 and entry['axiom_audit_passed']
            assert set(entry['anchors']) == {ref.split('::')[1] for ref in node['lean']}
            assert all(not axioms for axioms in entry['axioms'].values())
        else:
            assert node['lean'] == [], nid
        if node['status'] == 'COMPUTATIONALLY_CHECKED':
            assert sync.INDEPENDENT in node['source'] or any(t in node['source'] for t in sync.PYTHON_TESTS), nid
        if node['status'] == 'CONDITIONAL' and nid in ('OPS-OBSERVER-DECLARATION-REFUSAL', 'OPS-RUST-RECEIPTS-AND-LIMITS'):
            assert 'omega_solvers' in node['bottleneck'] and 'not run here' in node['bottleneck'], nid
        if node['status'] == 'IMPORTED_ASSUMPTION':
            assert node['imported_structure'], nid
        assert node['stage'] == 'OBSERVER_PRESHEAF' and 'foc035-observer-presheaf' in node['tags']


def test_every_ledger_row_is_mapped_once_or_more():
    rows = set(re.findall(r'^\| (L035-[A-Z]\d+) \|', LEDGER.read_text(encoding='utf-8'), re.M))
    assert len(rows) == 40
    mapped = {r for n in fragment()['nodes'] for r in n['ledger_rows']}
    assert mapped == rows


def test_external_citations_are_the_verified_ones():
    f = fragment()
    cited = {c['ref'] for c in f['citations'].values()}
    assert cited == {'external:arXiv:1102.0264', 'external:arXiv:1111.3620', 'external:arXiv:1705.07918',
                     'external:doi:10.1137/1107014'}
    pattern = re.compile(r'external:(arXiv:\d{4}\.\d{4,5}|doi:10\.\S+)')
    assert all(pattern.fullmatch(ref) for ref in cited)
    used = {s for n in f['nodes'] for s in n['source'] if s.startswith('external:')}
    assert used <= cited


def test_routes_attach_without_a_return_edge_or_a_cycle():
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    assert validator.check(graph, None) == []
    f = fragment()
    mine = {n['id'] for n in f['nodes']}
    assert all(r['output'] in mine for r in f['routes'])
    assert any(set(r['inputs']) - mine for r in f['routes'])
    by_out = {}
    for r in f['routes']:
        by_out.setdefault(r['output'], []).append(r)
    assert set(by_out) == mine
    for nid in ('OPS-LEAN-GAP', 'OPS-NO-SIGNALLING-SIGNED-SECTION', 'OPS-VOROBEV-THEOREM', 'OPS-AXIS1-WELLFOUNDED-ADMISSION'):
        assert all(r['status'] == 'GAP_NO_DERIVATION' and 'source' not in r for r in by_out[nid]), nid
    assert any(r['status'] == 'DERIVED_LEAN' for r in by_out['OPS-PUSHFORWARD-FUNCTOR-LEAN'])
    graph['routes'].append(dict(id='mutation-back-edge', inputs=['OPS-REGRESS-COROLLARY'],
                                output='PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY', status='GAP_NO_DERIVATION'))
    assert any('cycle among nodes' in error for error in validator.check(graph, None))


def test_papers_and_forbidden_words():
    for r in fragment()['records']:
        text = (ROOT / r['f004_refs'][0]).read_text(encoding='utf-8')
        assert text.startswith(f'# [{r["id"]}] {r["name"]}\n'), r['id']
        assert '\r' not in text
        for heading in ('## Statement', '## Governing obligation', '## Source status', '## Routes',
                        '## Non-claims', '## Sources'):
            assert heading in text, (r['id'], heading)
        assert sync.forbidden_words(text) == [], r['id']


def test_source_copies_are_byte_identical_to_the_recorded_digests():
    prov = json.loads((ROOT / 'sources/atlas/PROVENANCE.json').read_text(encoding='utf-8'))
    entries = {entry['in_repo_path']: entry for entry in prov['files']}
    for path in (LEDGER, NOTE):
        entry = entries[path.relative_to(ROOT).as_posix()]
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == entry['sha256'] and len(data) == entry['size_bytes']
        assert b'\r' not in data


def test_independent_check_recomputes_the_numbers():
    script = ROOT / sync.INDEPENDENT
    done = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(script)], capture_output=True, text=True, timeout=600)
    assert done.returncode == 0, done.stdout[-800:] + done.stderr[-800:]
    assert '50 checks passed' in done.stdout


def test_ceiling_witness_cannot_promote_status_or_cover_another_node():
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    cases = (
        ('OPS-RUST-RECEIPTS-AND-LIMITS', 'OPEN', 'only PROVED_LEAN'),
        ('OPS-RUST-RECEIPTS-AND-LIMITS', 'PROVED_LEAN', 'PROVED_LEAN must cite'),
        ('OPS-REGRESS-COROLLARY', 'CONDITIONAL', 'only PROVED_LEAN'),
    )
    for node_id, status, expected in cases:
        data = fragment()
        ceiling = next(n for n in data['nodes'] if n['id'] == 'OPS-RUST-RECEIPTS-AND-LIMITS')
        target = next(n for n in data['nodes'] if n['id'] == node_id)
        target['status'] = status
        target['lean'] = list(ceiling['lean'])
        assert any(expected in error for error in sync.validate(data, graph, ROOT))


def test_ceiling_witness_rejects_a_valid_but_unrelated_lean_module():
    data = fragment()
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    ceiling = next(n for n in data['nodes'] if n['id'] == 'OPS-RUST-RECEIPTS-AND-LIMITS')
    unrelated = next(n for n in data['nodes'] if n['status'] == 'PROVED_LEAN')
    ceiling['lean'] = list(unrelated['lean'])
    assert any('ceiling narrowing must cite' in error for error in sync.validate(data, graph, ROOT))
