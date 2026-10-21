"""Check that derivation_dag.json and theory_of_finite_qm.jsonl stay one graph without status promotion."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'dag'))
import sync_unified_dag as sync

# Lower rank is weaker evidence. A corpus record's audited status never ranks above its claim.
RANK = {'OPEN': 0, 'SOURCE_RECORD': 0, 'IMPORTED_ASSUMPTION': 1, 'ADMITTED_PRIMITIVE': 1, 'CONDITIONAL': 1,
        'DEFINITION': 2, 'COMPUTATIONALLY_CHECKED': 2, 'PROVED_PROSE': 3, 'PROVED_LEAN': 4, 'REFUTED': 4}


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def test_generated_files_are_current():
    for path, expected in sync.generated_files(ROOT).items():
        assert path.read_bytes() == expected, path


def test_every_record_names_a_node_and_every_node_a_record():
    assert sync.invariant_errors(ROOT) == []


def test_record_statuses_map_to_nodes_without_promotion():
    graph = load('dag/derivation_dag.json')
    nodes = {n['id']: n for n in graph['nodes']}
    records = [json.loads(x) for x in (ROOT / 'dag/theory_of_finite_qm.jsonl').read_text(encoding='utf-8').splitlines()]
    for r in records:
        node = nodes.get(r['id'])
        if node is None or sync.TAG not in node['tags']:
            continue
        assert node['status'] == sync.NODE_STATUS.get(r['record_status'], 'SOURCE_RECORD'), r['id']
        assert node['status'] != 'PROVED_LEAN' or node['lean'], r['id']


def test_corpus_records_are_audited_at_or_below_their_claim():
    fragment = load('dag/fragments/unified_dag.json')
    for d in fragment['domain_records']:
        claimed = d.get('source_claimed_status')
        if claimed in RANK:
            assert RANK[d['status']] <= RANK[claimed] or d['status'] == 'PROVED_PROSE', d['source_id']
        if d['status'] == 'PROVED_LEAN':
            assert d['lean'], d['source_id']
            for ref in d['lean']:
                path = ROOT / ref.split('::')[0]
                code = re.sub(r'/-.*?-/|--[^\n]*', '', path.read_text(encoding='utf-8'), flags=re.S)
                assert not re.search(r'\b(sorry|admit)\b|^\s*axiom\b', code, flags=re.M), ref


def test_known_open_problems_stay_open():
    graph = load('dag/derivation_dag.json')
    for n in graph['nodes']:
        text = (n['statement'] + ' ' + n['id']).lower()
        if n['stage'] == 'MUTUALLY_UNBIASED_BASES' and ('quartet' in text or 'max_mub' in text or 'maximal' in text):
            assert n['status'] != 'PROVED_LEAN', n['id']
        if n['stage'] == 'FERMION_SIGN' and 'master' in text:
            assert n['status'] != 'PROVED_LEAN', n['id']


def test_unified_record_ids_leave_room_for_the_pregenesis_fragment():
    fragment = load('dag/fragments/unified_dag.json')
    ids = [s['id'] for s in fragment['node_records'].values()] + [d['record_id'] for d in fragment['domain_records']]
    assert len(ids) == len(set(ids))
    assert all(int(x[4:]) >= 1000 for x in ids)
