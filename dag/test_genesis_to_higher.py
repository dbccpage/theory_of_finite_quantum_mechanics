"""Check the genesis-to-higher fragment: custody, honest statuses, and synchronization."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'dag'))
import sync_genesis_to_higher as sync
import validate_derivation_dag as validator

OPEN_IDS = {
    'GTH-SHADOW', 'GTH-TRUNC', 'GTH-HORNS', 'GTH-HOTT-MODEL',
    'GTH-LANG-CORE', 'GTH-LANG-REFLECT', 'GTH-LANG-INTERPRET', 'GTH-LANG-IMPORT',
}
IMPORT_IDS = {
    'GTH-IMPORT-UNIVALENT-UNIVERSE', 'GTH-IMPORT-INFTY-GROUPOID', 'GTH-IMPORT-INFTY-1-CATEGORY',
}
STATUS_LINE = 'Status: AI-drafted, awaiting human review.'


def fragment():
    return json.loads((ROOT / 'dag/fragments/genesis_to_higher.json').read_text(encoding='utf-8'))


def test_generated_files_match_fragment():
    for path, expected in sync.generated_files(ROOT).items():
        assert path.read_bytes() == expected, path


def test_counts_statuses_and_routes():
    f = fragment()
    assert f['stages'] == ['GENESIS_TO_HIGHER']
    assert len(f['nodes']) == len(f['records']) == len(f['routes']) == 12
    by_id = {n['id']: n for n in f['nodes']}
    assert set(by_id) == OPEN_IDS | IMPORT_IDS | {'GTH-LANG-LIMITS'}
    for nid in OPEN_IDS:
        assert by_id[nid]['status'] == 'OPEN' and by_id[nid]['lean'] == [], nid
    for nid in IMPORT_IDS:
        node = by_id[nid]
        assert node['status'] == 'IMPORTED_ASSUMPTION', nid
        assert node['imported_structure']
        assert any(s.startswith('external:') for s in node['source']), nid
    limits = by_id['GTH-LANG-LIMITS']
    assert limits['status'] == 'PROVED_PROSE' and limits['lean'] == []
    assert 'PROVED_LEAN' not in {n['status'] for n in f['nodes']}
    routes = {r['output']: r for r in f['routes']}
    assert set(routes) == set(by_id)
    shadow = routes['GTH-SHADOW']
    assert shadow['inputs'] == ['PGW-GO-ADMISSION-GATE'] and shadow['status'] == 'GAP_NO_DERIVATION'
    assert 'source' not in shadow
    core = routes['GTH-LANG-CORE']
    assert core['inputs'] == ['PGW-GO-ADMISSION-GATE', 'PG-GEN-REGIME-EVENTS', 'PGW-SN-TWO-BOXED-LAWS']
    assert core['status'] == 'GAP_NO_DERIVATION' and 'source' not in core
    for nid in OPEN_IDS:
        assert routes[nid]['status'] == 'GAP_NO_DERIVATION' and 'source' not in routes[nid], nid
    lim = routes['GTH-LANG-LIMITS']
    assert lim['status'] == 'RECORD_PARENT' and lim['inputs'] == ['GTH-LANG-IMPORT'] and lim['source']
    assert {r['id'] for r in f['records']} == {f'TFQ-{n}' for n in range(2400, 2412)}
    assert next(r['parent_id'] for r in f['records'] if r['id'] == 'TFQ-2400') == 'TFQ-0481'
    cited = {c['ref'] for c in f['citations'].values()}
    pattern = re.compile(r'external:(arXiv:[a-z\-]*/?\d+(\.\d+)?|doi:10\.\S+|book:\S+)')
    assert all(pattern.fullmatch(ref) for ref in cited), cited
    used = {s for n in f['nodes'] for s in n['source'] if s.startswith('external:')}
    assert used == cited


def test_graph_attaches_without_a_return_edge_or_a_cycle():
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    assert validator.check(graph, None) == []
    f = fragment()
    mine = {n['id'] for n in f['nodes']}
    assert all(r['output'] in mine for r in f['routes'])
    assert any(set(r['inputs']) - mine for r in f['routes'])
    graph['routes'].append(dict(id='mutation-back-edge', inputs=['GTH-LANG-LIMITS'],
                                output='PGW-GO-ADMISSION-GATE', status='GAP_NO_DERIVATION'))
    assert any('cycle among nodes' in error for error in validator.check(graph, None))


def test_papers_notes_and_forbidden_words():
    f = fragment()
    for r in f['records']:
        text = (ROOT / r['f004_refs'][0]).read_text(encoding='utf-8')
        assert text.startswith(f'# [{r["id"]}] {r["name"]}\n'), r['id']
        assert '\r' not in text
        for heading in ('## Statement', '## Governing obligation', '## Source status', '## Routes',
                        '## Non-claims', '## Sources'):
            assert heading in text, (r['id'], heading)
        assert sync.forbidden_words(text) == [], r['id']
    for n in f['nodes']:
        path = next(s for s in n['source'] if s.startswith('dag/derivations/independent/gth_'))
        assert not Path(path).name.startswith('tfq_')
        note = (ROOT / path).read_text(encoding='utf-8')
        assert note.startswith(STATUS_LINE + '\n'), path
        assert '\r' not in note
        for heading in ('## What is proved', '## What is assumed', '## What is open'):
            assert heading in note, path
        assert sync.forbidden_words(note) == [], path
        if n['id'] == 'GTH-LANG-LIMITS':
            assert 'Nothing in Lean.' in note
        elif n['id'] == 'GTH-SHADOW':
            assert 'CampaignGthShadow' in note
            assert 'lean list stays empty' in note
        else:
            assert 'Nothing in Lean.' in note.split('## What is proved', 1)[1].split('## What is assumed', 1)[0]
