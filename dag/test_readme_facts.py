"""Keep the README facts block generated and the README free of overclaiming words.

AuthorityEffect: None. The fast path reuses the contract/score row already in
README.md; `python -I -X utf8 scripts/build_readme_facts.py --check` runs the
full check, including `scripts/contract_scores.py check`.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'dag'))
import build_readme_facts as facts  # noqa: E402
import validate_derivation_dag as validator  # noqa: E402


def readme():
    return facts.README.read_text(encoding='utf-8')


def test_facts_block_is_current():
    current = readme()
    assert facts.splice(current, facts.render(skip_contracts=True)) == current, (
        'README facts are stale: run python -I -X utf8 scripts/build_readme_facts.py --write')


def test_facts_block_has_one_pair_of_markers():
    text = readme()
    assert text.count(facts.BEGIN) == 1 and text.count(facts.END) == 1
    assert text.index(facts.BEGIN) < text.index(facts.END)


def test_readme_avoids_forbidden_words():
    text = readme().lower()
    found = [w for w in validator.FORBIDDEN if re.search(r'\b' + re.escape(w) + r'\b', text)]
    assert found == []


def test_named_nodes_exist_in_the_dag():
    ids = {n['id'] for n in facts.load_json('dag/derivation_dag.json')['nodes']}
    assert [n for n in facts.NAMED_NODES if n not in ids] == []


def test_placeholder_scan_ignores_comments_and_strings():
    text = '-- sorry\n/- admit /- sorry -/ -/\ndef s := "sorry"\ntheorem t : True := by\n  admit\n'
    stripped = facts.strip_lean(text)
    assert 'sorry' not in stripped
    assert len(facts.ADMIT_TACTIC.findall(stripped)) == 1
