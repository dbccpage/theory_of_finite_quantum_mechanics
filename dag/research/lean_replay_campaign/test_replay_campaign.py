"""Tests for replay_campaign.py: the Lean lexer behind the admission scan, the audit resolution rules, --only.

AuthorityEffect: None.

    python -I -X utf8 -m pytest dag/research/lean_replay_campaign/test_replay_campaign.py -q
"""
import importlib.util
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("replay_campaign", HERE / "replay_campaign.py")
rc = importlib.util.module_from_spec(_spec)
sys.modules["replay_campaign"] = rc
_spec.loader.exec_module(rc)


# ----------------------------------------------------------------- lexer / admission scan

def hits(src: str) -> list[str]:
    return rc.admission_scan(src)


def test_sorry_in_code_is_found():
    assert hits("theorem t : True := by\n  sorry\n")


def test_line_comment_hides_its_own_block_opener():
    # `-- /-` must not open a block comment that swallows the sorry below
    assert hits("-- see /- here\ntheorem t : True := by sorry\n")


def test_string_literal_hides_nothing_after_it():
    assert hits('def s := "/-"\ntheorem t : True := by sorry\n')


def test_sorry_inside_string_or_comment_is_not_code():
    assert not hits('def s := "sorry"\n-- sorry\n/- sorry -/\n')


def test_nested_block_comments():
    assert not hits("/- a /- b -/ sorry -/\ntheorem t : True := trivial\n")
    assert hits("/- a /- b -/ c -/ theorem t : True := by sorry\n")


def test_doc_comment_and_escaped_quote():
    assert not hits('/-- doc "unterminated -/\ndef s := "a\\"b sorry"\n')


def test_char_literal_quote_does_not_open_a_string():
    assert hits("def q := '\"'\ntheorem t : True := by sorry\n")


def test_apostrophe_in_identifier_is_not_a_char_literal():
    assert hits("theorem h' : True := by sorry\n")


def test_raw_string():
    assert not hits('def s := r#"sorry "quoted" -/"#\n')
    assert hits('def s := r"/-"\ntheorem t : True := by sorry\n')


def test_strip_keeps_line_structure():
    src = "/- a\nb -/\nimport Foo\n-- c\nimport Bar\n"
    out = rc.strip_comments(src)
    assert out.count("\n") == src.count("\n")
    assert [m.group(1) for m in rc.IMPORT.finditer(out)] == ["Foo", "Bar"]


# ----------------------------------------------------------------- audit resolution

def audit(lines: list[str], cited: list[str], done: bool = True):
    parsed = rc.parse_audit("\n".join(lines), cited)
    return rc.audit_decision(parsed, cited, done), parsed


def test_exact_and_suffix_match_resolve():
    (ok, axioms), parsed = audit(["AX\tfoo\tNS.foo\t[propext]", "AX\tNS.bar\tNS.bar\t[]"], ["foo", "NS.bar"])
    assert ok and set(axioms) == {"NS.foo", "NS.bar"}
    assert parsed["cited_resolution"] == {"foo": ["NS.foo"], "NS.bar": ["NS.bar"]}


def test_one_unresolved_symbol_denies_the_flag():
    (ok, _), parsed = audit(["AX\tfoo\tNS.foo\t[]", "UNRESOLVED\tbar"], ["foo", "bar"])
    assert not ok and parsed["unresolved_cited_symbols"] == ["bar"]


def test_whole_file_audit_never_sets_the_flag_when_a_cited_symbol_is_missing():
    lines = ["UNRESOLVED\tbar", "AX\t*\tNS.other\t[propext]"]
    (ok, axioms), parsed = audit(lines, ["bar"])
    assert not ok and axioms == {} and parsed["file_wide_axioms"] == {"NS.other": ["propext"]}


def test_all_symbols_unresolved_is_not_a_pass():
    (ok, _), _ = audit(["UNRESOLVED\ta", "UNRESOLVED\tb", "AX\t*\tNS.t\t[]"], ["a", "b"])
    assert not ok


def test_ambiguous_leaf_is_unresolved():
    lines = ["AX\tfoo\tA.foo\t[]", "AX\tfoo\tB.foo\t[]"]
    (ok, _), parsed = audit(lines, ["foo"])
    assert not ok and parsed["ambiguous_cited_symbols"] == {"foo": ["A.foo", "B.foo"]}


def test_exact_name_wins_over_other_suffix_matches():
    lines = ["AX\tA.foo\tA.foo\t[]", "AX\tA.foo\tB.A.foo\t[]"]
    (ok, axioms), _ = audit(lines, ["A.foo"])
    assert ok and set(axioms) == {"A.foo"}


def test_last_component_fallback_lines_are_ignored():
    # an older audit printed AXLC lines for a constant in another namespace; they must not resolve anything
    lines = ["AXLC\tU1.Cayley.homCayley_projMul\tU1.CayleyProjective.homCayley_projMul\t[]"]
    (ok, axioms), parsed = audit(lines, ["U1.Cayley.homCayley_projMul"])
    assert not ok and axioms == {} and parsed["unresolved_cited_symbols"] == ["U1.Cayley.homCayley_projMul"]


def test_symbol_that_was_never_audited_is_not_a_pass():
    (ok, _), parsed = audit(["AX\tfoo\tNS.foo\t[]"], ["foo", "baz"])
    assert not ok and not parsed["all_cited_audited"]


def test_nonstandard_axiom_denies_the_flag():
    (ok, _), _ = audit(["AX\tfoo\tNS.foo\t[propext, sorryAx]"], ["foo"])
    assert not ok


def test_file_cited_without_a_declaration_uses_the_whole_file_audit():
    (ok, axioms), _ = audit(["AX\t*\tNS.t\t[Classical.choice]"], [])
    assert ok and axioms == {"NS.t": ["Classical.choice"]}
    (ok2, _), _ = audit([], [])
    assert not ok2


def test_build_failure_denies_the_flag():
    (ok, _), _ = audit(["AX\tfoo\tNS.foo\t[]"], ["foo"], done=False)
    assert not ok


# ----------------------------------------------------------------- cache keys and --only

def test_keys_change_with_symbols_and_dependency_state():
    k = rc.Runner.keys
    base = k("a" * 64, {"M": "1"}, ["x"])
    assert k("a" * 64, {"M": "1"}, ["x"]) == base
    assert k("a" * 64, {"M": "2"}, ["x"])[0] != base[0]
    assert k("a" * 64, {"M": "1"}, ["x", "y"])[0] == base[0]
    assert k("a" * 64, {"M": "1"}, ["x", "y"])[1] != base[1]
    assert k("b" * 64, {"M": "1"}, ["x"])[0] != base[0]


class _Stub:
    plan = {"lean4/A.lean": {}, "papers/x/y/B.lean": {}}

    class graph:
        path_of = {"A": "lean4/A.lean", "Dep": "lean4/Dep.lean"}


def test_only_accepts_paths_and_module_names():
    paths, mods = rc.Runner.normalise_only(_Stub, ["lean4/A.lean", "Dep", "papers/x/y/B.lean"])
    assert paths == {"lean4/A.lean", "lean4/Dep.lean", "papers/x/y/B.lean"}
    assert mods == {"A", "Dep"}
    assert rc.Runner.normalise_only(_Stub, None) == (None, None)
    with pytest.raises(SystemExit):
        rc.Runner.normalise_only(_Stub, ["Nope"])
