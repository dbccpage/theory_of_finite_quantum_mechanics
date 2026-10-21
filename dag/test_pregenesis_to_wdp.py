"""Check the pre-genesis to WDP fragment: generated files, layout, custody, links and the chain."""
from pathlib import Path
import json
import re
import sys
import uuid

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'dag'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import sync_application_branches as app_sync
import sync_pregenesis_to_wdp as pgw
import validate_derivation_dag as validator
import verify_pregenesis_to_wdp_citations as citations

STAGE_RANK = {s: i for i, s in enumerate(('PREGENESIS', 'GENESIS', 'FINITE_OBSTRUCTION', 'AUTHORIZATION',
                                          'MSSN_SN', 'WDP'))}
DAG_ROOTS = {'PG-INERT-DIAMOND', 'PG-SIX-OPERATIONS', 'PG-PRIMDIFF-AXIOMS', 'PG-ROOT-DIFF-STRUCTURE'}


def manifest():
    return pgw.load_manifest(ROOT)


def records():
    return [json.loads(line) for line in (ROOT / 'dag/theory_of_finite_qm.jsonl').read_text(encoding='utf-8').splitlines()]


def test_generated_files_match_disk_for_both_generators():
    for path, expected in pgw.generated_files(ROOT).items():
        assert path.read_bytes() == expected, path
    for path, expected in app_sync.generated_files(ROOT).items():
        assert path.read_bytes().decode('utf-8') == expected, path


def test_manifest_schema_and_uuid_namespace():
    m = manifest()
    _, old = pgw.read_jsonl(ROOT)
    errs = pgw.validate_manifest(m, {r['id']: r for r in old}, pgw.pinned_papers(ROOT), pgw.paper_paths(ROOT))
    assert errs == []
    ns = uuid.uuid5(uuid.NAMESPACE_URL,
                    'https://github.com/dbccpage/theory_of_finite_quantum_mechanics/dag/theory_of_finite_qm.jsonl')
    assert str(ns) == m['uuid_namespace']['value'] == str(pgw.UUID_NAMESPACE)
    by_id = {r['id']: r for r in records()}
    for r in m['records']:
        assert by_id[r['id']]['uuid'] == str(uuid.uuid5(ns, r['id']))
    groups = [r['group'] for r in m['records'] if r['stage'] == 'MSSN_SN']
    assert groups == sorted(groups, key=lambda g: (g != 'S(n)', g))


def test_jsonl_layout_keeps_upstream_lines_and_orders_blocks():
    raw = (ROOT / 'dag/theory_of_finite_qm.jsonl').read_bytes().decode('utf-8')
    lines = raw.splitlines(keepends=True)
    assert all(line.endswith('\r\n') for line in lines)
    slices = [json.loads(line)['source_slice'] for line in lines]
    owned = [i for i, s in enumerate(slices) if s == pgw.SLICE]
    app = [i for i, s in enumerate(slices) if s == 'application_branches']
    assert owned == list(range(owned[0], owned[0] + len(owned)))
    assert max(owned) < min(app)
    assert all(s not in (pgw.SLICE, 'application_branches') for s in slices[:owned[0]])
    keys = set(json.loads(lines[0]))
    for i in owned:
        r = json.loads(lines[i])
        assert set(r) == keys
        assert lines[i] == json.dumps(r, ensure_ascii=False, sort_keys=True) + '\r\n'


def test_new_papers_have_five_sections_and_no_pfp_receipt():
    for r in manifest()['records']:
        text = (ROOT / pgw.new_paper_path(r)).read_text(encoding='utf-8')
        assert '\r' not in text
        for heading in ('## 1. Abstract', '## 2. Derivation Context', '## 3. Multi-Tier', '## 4. Downstream',
                        '## 5. Audit Trail'):
            assert heading in text, (r['id'], heading)
        assert '## 6.' not in text
        assert text.startswith(f'# [{r["id"]}] {r["name"]}\n')


def _links(path: Path, text: str):
    for reference in re.findall(r'\]\(([^)]+)\)', text):
        if reference.startswith(('https://', 'http://')):
            continue
        yield reference


def test_links_resolve_in_new_papers_owned_indices_and_patched_parents():
    m = manifest()
    owned = {r['id'] for r in m['records']}
    parents = {r['parent_id'] for r in m['records'] if r['parent_id'] not in owned and not r.get('pinned_parent')}
    paths = pgw.paper_paths(ROOT)
    sections = [(ROOT / pgw.new_paper_path(r), (ROOT / pgw.new_paper_path(r)).read_text(encoding='utf-8'))
                for r in m['records']]
    # In an existing parent only section 4 is written by the generator; older placeholder links stay as found.
    for p in parents:
        f = ROOT / paths[p]
        sections.append((f, f.read_text(encoding='utf-8').split('## 4. Downstream', 1)[1].split('## 5.', 1)[0]))
    for f, text in sections:
        for reference in _links(f, text):
            assert (f.parent / reference.split('#')[0]).is_file(), (f, reference)
    index = ROOT / 'dag/derivations/README.md'
    text = index.read_text(encoding='utf-8').split(app_sync.MARKER)[0]
    for stage in pgw.OWNED_STAGES:
        section = re.search(r'^### ' + stage + r' \(\d+ derivations\)\n.*?(?=^### |\Z)', text, re.S | re.M).group(0)
        for reference in _links(index, section):
            assert (index.parent / reference).is_file() or (index.parent / reference).is_dir(), reference


def test_section4_lists_children_of_new_and_unpinned_parents():
    m = manifest()
    paths = pgw.paper_paths(ROOT)
    children = {}
    for r in m['records']:
        children.setdefault(r['parent_id'], []).append(r['id'])
    pinned = pgw.pinned_papers(ROOT)
    readme = (ROOT / 'dag/derivations/README.md').read_text(encoding='utf-8')
    for parent, kids in children.items():
        text = (ROOT / paths[parent]).read_text(encoding='utf-8')
        section = text.split('## 4. Downstream', 1)[1].split('## 5.', 1)[0]
        if paths[parent] in pinned:
            for kid in kids:
                assert re.search(r'\| \[`' + parent + r'`\]\([^)]+\) \| \[`' + kid + r'`\]', readme), (parent, kid)
            continue
        listed = re.findall(r'\[(TFQ-\d{4})\]', section)
        assert listed[-len(kids):] == kids, (parent, listed, kids)


def test_pinned_papers_unchanged():
    import validate_prompts
    report = validate_prompts.validate()
    errors = report['errors'] if isinstance(report, dict) else report
    assert not [e for e in errors if 'paper source pin changed' in e]


def test_chain_reaches_root_and_dag_stays_valid():
    by_id = {r['id']: r for r in records()}
    m = manifest()
    for r in m['records']:
        seen, cur = set(), r['id']
        while by_id[cur]['parent_id'] is not None:
            parent = by_id[cur]['parent_id']
            assert STAGE_RANK.get(by_id[parent]['stage'], 99) <= STAGE_RANK.get(by_id[cur]['stage'], 99) or \
                by_id[parent]['stage'] not in STAGE_RANK
            assert cur not in seen
            seen.add(cur)
            cur = parent
        assert cur == 'TFQ-0000', r['id']
    assert any(r.get('terminal') for r in m['records'])
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    assert validator.check(graph, None) == []
    preds = {}
    for route in graph['routes']:
        preds.setdefault(route['output'], set()).update(route['inputs'])
    for node in graph['nodes']:
        if pgw.TAG not in node['tags']:
            continue
        stack, seen = [node['id']], set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(preds.get(cur, ()))
        assert seen & DAG_ROOTS, node['id']


def test_citations_resolve_offline():
    if citations.symbol_game_root() is None:
        pytest.skip('the_symbol_game checkout not found; set TFQ_SYMBOL_GAME_ROOT')
    files = citations.Files(network=False, commit=manifest()['external_roots']['github19l']['commit'])
    errs, _ = citations.check(manifest(), files)
    assert errs == []
