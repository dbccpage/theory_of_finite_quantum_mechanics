"""Origin: scripts/test_overclaim_scan.py
Claim: each rule of scripts/overclaim_scan.py fires on a small synthetic input and stays quiet on its honest twin, the findings are deterministic with line-free keys, --strict compares against a baseline, and the committed baseline covers the HIGH findings of a fresh scan
AuthorityEffect: None
Scope Fence: this file does not test that a finding is a real overclaim; it tests the mechanical rules only
Level: L5
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import overclaim_scan as oc  # noqa: E402

REAL_ROOT = Path(__file__).resolve().parent.parent


def node(node_id: str, status: str = "OPEN", statement: str = "A statement.", lean=None, **extra) -> dict:
    return {"id": node_id, "stage": "FINITE_QM_CORE", "status": status, "statement": statement, "bottleneck": "b",
            "source": ["x.md"], "lean": lean or [], "rust": [], **extra}


def make_repo(tmp_path: Path, nodes: list[dict], files: dict[str, str] | None = None, records: list[dict] | None = None) -> Path:
    (tmp_path / "dag").mkdir(parents=True, exist_ok=True)
    (tmp_path / "dag" / "derivation_dag.json").write_text(json.dumps({"nodes": nodes, "records": records or []}), encoding="utf-8")
    for rel, text in (files or {}).items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    return tmp_path


def rules(findings, rule: str):
    return [f for f in findings if f.rule == rule]


GOOD_LEAN = "theorem good (n : Nat) : n + 0 = n := by simp\n"


# ---- R1 ------------------------------------------------------------------------------------


def test_r1_flags_atlas_only_and_missing_symbol(tmp_path):
    root = make_repo(tmp_path, [
        node("N-ATLAS", "PROVED_LEAN", lean=["omega_engine_atlas/a/B.lean::thm"]),
        node("N-NOREF", "PROVED_LEAN"),
        node("N-SYMBOL", "PROVED_LEAN", lean=["lean4/A.lean::absent_symbol"]),
        node("N-OK", "PROVED_LEAN", lean=["lean4/A.lean::good"]),
        node("N-OPEN", "OPEN", lean=["omega_engine_atlas/a/B.lean::thm"]),
    ], {"lean4/A.lean": GOOD_LEAN})
    got = {f.subject: f for f in rules(oc.scan(root), "R1")}
    assert set(got) == {"N-ATLAS", "N-NOREF", "N-SYMBOL"}
    assert all(f.severity == "HIGH" for f in got.values())
    assert "atlas-only" in got["N-ATLAS"].evidence


# ---- R2 ------------------------------------------------------------------------------------


def test_r2_true_typed_or_universal_statement_over_only_closed_theorems(tmp_path):
    lean = (
        "theorem trivial_one : True := trivial\n"
        "theorem closed_eq : 2 + 2 = 4 := by decide\n"
        "theorem general (n : Nat) : n + 0 = n := by simp\n"
        "theorem quantified : ∀ n : Nat, n + 0 = n := by intro n; simp\n"
        "def helper : Nat := 3\n"
    )
    root = make_repo(tmp_path, [
        node("N-TRUE", "PROVED_LEAN", lean=["lean4/A.lean::trivial_one"]),
        node("N-CLOSED", "PROVED_LEAN", "Holds for every n.", lean=["lean4/A.lean::closed_eq"]),
        node("N-CLOSED-DEF", "PROVED_LEAN", "Holds for every n.", lean=["lean4/A.lean::closed_eq", "lean4/A.lean::helper"]),
        node("N-GENERAL", "PROVED_LEAN", "Holds for every n.", lean=["lean4/A.lean::general"]),
        node("N-FORALL", "PROVED_LEAN", "Holds for every n.", lean=["lean4/A.lean::quantified"]),
        node("N-ONE-GENERAL", "PROVED_LEAN", "Holds for every n.", lean=["lean4/A.lean::closed_eq", "lean4/A.lean::general"]),
        node("N-MIXED", "PROVED_LEAN", "Holds for every n.", lean=["lean4/A.lean::general", "lean4/A.lean::trivial_one"]),
        # A closed decide theorem behind a statement with no universal wording is a finite claim, not an R2 finding.
        node("N-BOOKKEEPING", "PROVED_LEAN", "The partition has 10 stages and 172 routes.", lean=["lean4/A.lean::closed_eq"]),
        # A cited symbol the reader cannot place: do not claim that every cited declaration is closed.
        node("N-UNPLACED", "PROVED_LEAN", "Holds for every n.", lean=["lean4/A.lean::closed_eq", "lean4/A.lean::not_there"]),
    ], {"lean4/A.lean": lean})
    got = {f.subject: f for f in rules(oc.scan(root), "R2")}
    assert set(got) == {"N-TRUE", "N-CLOSED", "N-CLOSED-DEF", "N-MIXED"}
    assert got["N-TRUE"].severity == "MEDIUM"
    assert "type True" in got["N-TRUE"].evidence
    assert "every cited theorem is closed" in got["N-CLOSED"].evidence
    assert "every cited theorem is closed" not in got["N-MIXED"].evidence


def test_lean_files_are_parsed_once(tmp_path):
    root = make_repo(tmp_path, [], {"lean4/A.lean": GOOD_LEAN})
    repo = oc.Repo(root)
    assert repo.decls("lean4/A.lean") is repo.decls("lean4/A.lean")
    assert repo.stripped("lean4/A.lean") is repo.stripped("lean4/A.lean")
    assert repo.decls("lean4/missing.lean") is None


# ---- R3 ------------------------------------------------------------------------------------


def test_r3_ignores_comments_strings_and_constructors(tmp_path):
    lean = (
        "-- sorry in a line comment\n"
        "/- block sorry\n  /- nested admit -/ axiom -/\n"
        'def msg : String := "sorry and native_decide and unsafe"\n'
        "inductive Op where\n  | mention\n  | admit\n"
        "theorem honest : 1 = 1 := rfl\n"
    )
    root = make_repo(tmp_path, [node("N", "PROVED_LEAN", lean=["lean4/A.lean::honest"])], {"lean4/A.lean": lean})
    assert rules(oc.scan(root), "R3") == []


def test_r3_flags_each_token_for_proved_and_conditional_only(tmp_path):
    lean = (
        "theorem a : 1 = 2 := by sorry\n"
        "theorem b : 1 = 2 := by admit\n"
        "axiom my_axiom : False\n"
        "theorem c : 1 = 1 := by native_decide\n"
        "unsafe def d : Nat := 0\n"
    )
    root = make_repo(tmp_path, [
        node("N-LEAN", "PROVED_LEAN", lean=["lean4/A.lean::a"]),
        node("N-COND", "CONDITIONAL", lean=["lean4/B.lean::a"]),
        node("N-OPEN", "OPEN", lean=["lean4/C.lean::a"]),
    ], {"lean4/A.lean": lean, "lean4/B.lean": "theorem a : 1 = 2 := by sorry\n", "lean4/C.lean": lean})
    found = rules(oc.scan(root), "R3")
    assert {f.subject for f in found} == {"lean4/A.lean", "lean4/B.lean"}
    toks = {f.evidence.split("`")[1] for f in found if f.subject == "lean4/A.lean"}
    assert toks == {"sorry", "admit", "axiom", "native_decide", "unsafe"}
    assert all(f.severity == "HIGH" for f in found)


def test_r3_key_has_no_line_number(tmp_path):
    body = "theorem a : 1 = 2 := by sorry\n"
    root = make_repo(tmp_path, [node("N", "PROVED_LEAN", lean=["lean4/A.lean::a"])], {"lean4/A.lean": body})
    first = rules(oc.scan(root), "R3")[0]
    (root / "lean4" / "A.lean").write_text("\n\n\n" + body, encoding="utf-8")
    second = rules(oc.scan(root), "R3")[0]
    assert first.line == 1 and second.line == 4
    assert first.key == second.key


# ---- R4 ------------------------------------------------------------------------------------


def receipt(source: str, sha: str, axioms: dict | None = None) -> str:
    entry = {"module": "A", "dag_node": "N", "source": source, "sha256": sha, "axioms": axioms or {"A.good": ["propext"]}}
    return json.dumps({"lean_replay": {"results": [entry]}})


def test_r4_sha_and_axioms(tmp_path):
    sha = hashlib.sha256(GOOD_LEAN.encode()).hexdigest()
    root = make_repo(tmp_path, [node("N", "PROVED_LEAN", lean=["lean4/A.lean::good"])], {
        "lean4/A.lean": GOOD_LEAN,
        "dag/research/ok_lean_replay.json": receipt("lean4/A.lean", sha),
        "dag/research/badsha_lean_replay.json": receipt("lean4/A.lean", "0" * 64),
        "dag/research/badax_lean_replay.json": receipt("lean4/A.lean", sha, {"A.good": ["propext", "Lean.ofReduceBool"]}),
        "dag/research/missing_lean_replay.json": receipt("lean4/Gone.lean", sha),
    })
    found = rules(oc.scan(root), "R4")
    assert {f.subject for f in found} == {
        "dag/research/badsha_lean_replay.json", "dag/research/badax_lean_replay.json", "dag/research/missing_lean_replay.json"}
    assert any("Lean.ofReduceBool" in f.evidence for f in found)
    assert all(f.severity == "HIGH" for f in found)


def test_r4_accepts_crlf_checkout_hash(tmp_path):
    crlf = GOOD_LEAN.replace("\n", "\r\n").encode()
    sha_lf = hashlib.sha256(GOOD_LEAN.encode()).hexdigest()
    root = make_repo(tmp_path, [node("N", "PROVED_LEAN", lean=["lean4/A.lean::good"])], {"dag/research/x_lean_replay.json": receipt("lean4/A.lean", sha_lf)})
    (root / "lean4").mkdir()
    (root / "lean4" / "A.lean").write_bytes(crlf)
    assert rules(oc.scan(root), "R4") == []


# ---- R5 ------------------------------------------------------------------------------------


def test_r5_unrecomputed_number(tmp_path):
    lean = "theorem good : 3418 = 3418 := rfl\n"
    root = make_repo(tmp_path, [
        node("N-HAS", "PROVED_LEAN", "There are 3,418 admissible tuples.", lean=["lean4/A.lean::good"]),
        node("N-LACKS", "PROVED_LEAN", "There are 13,691 admissible tuples and 3,418 others.", lean=["lean4/A.lean::good"]),
        node("N-OPEN", "OPEN", "There are 99999 tuples."),
        node("N-CHECK", "COMPUTATIONALLY_CHECKED", "There are 4242 tuples.", lean=[]),
    ], {"lean4/A.lean": lean, "checks/independent/n-check.py": "print(4242)\n"})
    got = {f.subject: f for f in rules(oc.scan(root), "R5")}
    assert set(got) == {"N-LACKS"}
    assert "13691" in got["N-LACKS"].evidence and "3418" not in got["N-LACKS"].evidence.split("numbers in no cited file:")[1]
    assert got["N-LACKS"].severity == "LOW"


def r5_subjects(tmp_path, statement: str, lean: str) -> dict:
    root = make_repo(tmp_path, [node("N", "PROVED_LEAN", statement, lean=["lean4/A.lean::t"])], {"lean4/A.lean": lean})
    return {f.subject: f for f in rules(oc.scan(root), "R5")}


def test_r5_fraction_needs_the_exact_signed_numeral(tmp_path):
    sign = r5_subjects(tmp_path / "a", "The entry is 1/2.", "theorem t : (-1/2 : Rat) = -1/2 := rfl\n")
    assert set(sign) == {"N"} and "1/2" in sign["N"].evidence
    apart = r5_subjects(tmp_path / "b", "The entry is 1/2.", "theorem t : 1 + 2 = 3 := rfl\n")
    assert set(apart) == {"N"}
    exact = r5_subjects(tmp_path / "c", "The entry is -1/2.", "theorem t : (-1/2 : Rat) = -1/2 := rfl\n")
    assert exact == {}
    unsigned = r5_subjects(tmp_path / "d", "The entry is 1/2.", "theorem t : (1/2 : Rat) = 1/2 := rfl\n")
    assert unsigned == {}
    wrong_sign = r5_subjects(tmp_path / "e", "The entry is -1/2 (minus sign U+2212: −1/2).", "theorem t : (1/2 : Rat) = 1/2 := rfl\n")
    assert set(wrong_sign) == {"N"} and "-1/2" in wrong_sign["N"].evidence
    subtraction = r5_subjects(tmp_path / "f", "The count is n-1/2.", "theorem t : (1/2 : Rat) = 1/2 := rfl\n")
    assert subtraction == {}  # a minus after a word character is subtraction, not a sign


def test_r5_integers_stay_exact_token_equality(tmp_path):
    assert r5_subjects(tmp_path / "a", "There are 3,418 tuples.", "theorem t : 3_418 = 3418 := rfl\n") == {}
    assert set(r5_subjects(tmp_path / "b", "There are 3,418 tuples.", "theorem t : 13418 = 13418 := rfl\n")) == {"N"}


def test_r5_derivation_note_and_readme(tmp_path):
    rec = [{"id": "TFQ-0001", "existing_derivation_dag_ids": ["N"]}]
    root = make_repo(tmp_path, [node("N", "PROVED_LEAN", "x", lean=["lean4/A.lean::good"])], {
        "lean4/A.lean": "theorem good : 777 = 777 := rfl\n",
        "dag/derivations/01/tfq_0001_n.md": "The count is 777 and also 888 in 2026-10-22 [link](https://x/12345).\n",
        "README.md": "Intro.\n| `N` | PROVED_LEAN | 777 and 555 |\n",
    }, rec)
    found = rules(oc.scan(root), "R5")
    note = [f for f in found if f.subject.endswith("tfq_0001_n.md")]
    readme = [f for f in found if f.subject == "README.md"]
    assert len(note) == 1 and "888" in note[0].evidence and "777" not in note[0].evidence.split("no cited file:")[1] and "12345" not in note[0].evidence
    assert len(readme) == 1 and "555" in readme[0].evidence and readme[0].line == 2


# ---- R6 ------------------------------------------------------------------------------------


def test_r6_prose_calls_open_node_proved(tmp_path):
    root = make_repo(tmp_path, [node("N-OPEN"), node("N-LEAN", "PROVED_LEAN", lean=["lean4/A.lean::good"]), node("N-IMP", "IMPORTED_ASSUMPTION")], {
        "lean4/A.lean": GOOD_LEAN,
        "README.md": (
            "We proved N-OPEN in the last release.\n"
            "N-OPEN is not proved.\n"
            "N-OPEN is OPEN, although the note says proved.\n"
            "The theorem for N-LEAN is proved.\n"
            "It shows that N-IMP holds.\n"
            "N-OPEN-EXTENDED is derived.\n"
        ),
        "docs/note.md": (
            "Lean establishes N-OPEN.\n"
            "Derived part (dag/results/N-OPEN/runs/2026): the sector form is diagonal. See ../nodes/N-OPEN.md for the node.\n"
            "N-IMP is imported; it is re-expressed rather than derived.\n"
        ),
        "dag/research/not_scanned.md": "N-OPEN is proved.\n",
    })
    found = rules(oc.scan(root), "R6")
    assert sorted((f.subject, f.line) for f in found) == [("README.md", 1), ("README.md", 5), ("docs/note.md", 1)]
    assert all(f.severity == "HIGH" for f in found)


# ---- R7 ------------------------------------------------------------------------------------


def test_r7_promotional_wording_and_negations(tmp_path):
    root = make_repo(tmp_path, [], {
        "README.md": (
            "This work derives quantum mechanics from nothing.\n\n"
            "The project does not claim to derive quantum mechanics.\n\n"
            "A revolutionary, first-ever result.\n\n"
            "It makes no assumptions beyond the primitive.\n\n"
            "The program never uses the phrase complete derivation.\n\n"
            "The note does not claim any of the following:\n- that it derives quantum mechanics;\n\n"
            "- but this bullet, a paragraph later, says it derives quantum mechanics.\n"
        ),
        "docs/overclaim/report.md": "revolutionary\n",
    })
    found = rules(oc.scan(root), "R7")
    got = sorted((f.line, f.evidence.split('"')[1]) for f in found)
    assert got == [(1, "derives quantum mechanics"), (5, "first-ever"), (5, "revolutionary"), (14, "derives quantum mechanics")]
    assert all(f.severity == "MEDIUM" for f in found)


def test_r7_phrase_list_is_a_constant():
    assert "derives quantum mechanics" in oc.PROMOTIONAL_PHRASES and "no assumptions" in oc.PROMOTIONAL_PHRASES


# ---- R8 ------------------------------------------------------------------------------------


def test_r8_status_line(tmp_path):
    root = make_repo(tmp_path, [], {
        "dag/derivations/independent/a.md": "Status: AI-drafted, awaiting human review.\n\n# A\n",
        "dag/derivations/independent/b.md": "Status: Reviewed by Ada Lovelace, 2026-10-22.\n",
        "dag/derivations/independent/c.md": "# C\nStatus: AI-drafted, awaiting human review.\n",
        "dag/derivations/independent/d.md": "Status: Reviewed by someone.\n",
        "dag/derivations/independent/e.md": "Status: AI-drafted, awaiting human review\n",
    })
    found = rules(oc.scan(root), "R8")
    assert sorted(Path(f.subject).name for f in found) == ["c.md", "d.md", "e.md"]
    assert all(f.severity == "MEDIUM" and f.line == 1 for f in found)


# ---- R9 (needs git) -------------------------------------------------------------------------

GIT = shutil.which("git")


def run_git(root: Path, *args: str) -> None:
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.org", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.org"}
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, env=env)


@pytest.mark.skipif(GIT is None, reason="git not available")
def test_r9_status_rise_needs_lean_ref_and_receipt(tmp_path):
    sha = hashlib.sha256(GOOD_LEAN.encode()).hexdigest()
    base_nodes = [node("N-NONE"), node("N-LEANONLY"), node("N-FULL"), node("N-LOWERED", "PROVED_LEAN", lean=["lean4/A.lean::good"])]
    root = make_repo(tmp_path, base_nodes, {"lean4/A.lean": GOOD_LEAN, "lean4/B.lean": GOOD_LEAN})
    run_git(root, "init", "-q", "-b", "main")
    run_git(root, "add", "-A")
    run_git(root, "commit", "-q", "-m", "base")
    new_nodes = [
        node("N-NONE", "PROVED_LEAN"),
        node("N-LEANONLY", "PROVED_LEAN", lean=["lean4/B.lean::good"]),
        node("N-FULL", "PROVED_LEAN", lean=["lean4/A.lean::good"]),
        node("N-LOWERED", "OPEN"),
        node("N-BRAND-NEW", "PROVED_LEAN"),
    ]
    make_repo(root, new_nodes)
    entry = {"module": "A", "dag_node": "N-FULL", "source": "lean4/A.lean", "sha256": sha, "axioms": {}}
    (root / "dag" / "research").mkdir(parents=True)
    (root / "dag" / "research" / "campaign_n-full_lean_replay.json").write_text(json.dumps({"lean_replay": {"results": [entry]}}), encoding="utf-8")
    diff = oc.load_diff(root, "main")
    found = rules(oc.scan(root, diff), "R9")
    assert {f.subject for f in found} == {"N-NONE", "N-LEANONLY", "N-BRAND-NEW"}
    assert all(f.severity == "HIGH" for f in found)
    assert "no new replay-receipt row" in [f for f in found if f.subject == "N-LEANONLY"][0].evidence


@pytest.mark.skipif(GIT is None, reason="git not available")
def test_r9_touching_an_old_receipt_is_not_a_new_receipt(tmp_path):
    """Status rise + one new Lean ref + a whitespace-only edit to an old receipt must still be HIGH."""
    sha_a = hashlib.sha256(GOOD_LEAN.encode()).hexdigest()
    old_entry = {"module": "A", "dag_node": "N-OLD", "source": "lean4/A.lean", "sha256": sha_a, "axioms": {}}
    receipt_path = Path("dag") / "research" / "old_lean_replay.json"
    files = {"lean4/A.lean": GOOD_LEAN, "lean4/B.lean": GOOD_LEAN, receipt_path.as_posix(): json.dumps({"lean_replay": {"results": [old_entry]}})}
    root = make_repo(tmp_path, [node("N-OLD", "PROVED_LEAN", lean=["lean4/A.lean::good"]), node("N-RISE")], files)
    run_git(root, "init", "-q", "-b", "main")
    run_git(root, "add", "-A")
    run_git(root, "commit", "-q", "-m", "base")
    make_repo(root, [node("N-OLD", "PROVED_LEAN", lean=["lean4/A.lean::good"]), node("N-RISE", "PROVED_LEAN", lean=["lean4/B.lean::good"])])
    (root / receipt_path).write_text(json.dumps({"lean_replay": {"results": [old_entry]}}, indent=2) + "\n", encoding="utf-8")  # whitespace only
    diff = oc.load_diff(root, "main")
    assert receipt_path.as_posix() in diff.changed_files
    got = rules(oc.scan(root, diff), "R9")
    assert [f.subject for f in got] == ["N-RISE"] and got[0].severity == "HIGH"
    # A row for N-RISE whose source is the new ref's module, absent from the base, DOES count.
    new_row = {"module": "B", "dag_node": "N-RISE", "source": "lean4/B.lean", "sha256": sha_a, "axioms": {}}
    (root / receipt_path).write_text(json.dumps({"lean_replay": {"results": [old_entry, new_row]}}), encoding="utf-8")
    assert rules(oc.scan(root, oc.load_diff(root, "main")), "R9") == []
    # A row for N-RISE whose source is some other module does not.
    other_row = {**new_row, "source": "lean4/A.lean"}
    (root / receipt_path).write_text(json.dumps({"lean_replay": {"results": [old_entry, other_row]}}), encoding="utf-8")
    assert [f.subject for f in rules(oc.scan(root, oc.load_diff(root, "main")), "R9")] == ["N-RISE"]


@pytest.mark.skipif(GIT is None, reason="git not available")
def test_r9_a_row_already_in_the_base_is_not_new(tmp_path):
    sha_b = hashlib.sha256(GOOD_LEAN.encode()).hexdigest()
    row = {"module": "B", "dag_node": "N-RISE", "source": "lean4/B.lean", "sha256": sha_b, "axioms": {}}
    receipt_path = Path("dag") / "research" / "early_lean_replay.json"
    files = {"lean4/B.lean": GOOD_LEAN, receipt_path.as_posix(): json.dumps({"lean_replay": {"results": [row]}})}
    root = make_repo(tmp_path, [node("N-RISE")], files)
    run_git(root, "init", "-q", "-b", "main")
    run_git(root, "add", "-A")
    run_git(root, "commit", "-q", "-m", "base: receipt row exists, node still OPEN")
    make_repo(root, [node("N-RISE", "PROVED_LEAN", lean=["lean4/B.lean::good"])])
    (root / receipt_path).write_text(json.dumps({"lean_replay": {"results": [row]}}, indent=1) + "\n", encoding="utf-8")
    got = rules(oc.scan(root, oc.load_diff(root, "main")), "R9")
    assert [f.subject for f in got] == ["N-RISE"]
    # Re-recording the row (new sha256) makes it a new row.
    (root / "lean4" / "B.lean").write_text(GOOD_LEAN + "-- edit\n", encoding="utf-8")
    new_sha = hashlib.sha256((GOOD_LEAN + "-- edit\n").encode()).hexdigest()
    (root / receipt_path).write_text(json.dumps({"lean_replay": {"results": [{**row, "sha256": new_sha}]}}), encoding="utf-8")
    assert rules(oc.scan(root, oc.load_diff(root, "main")), "R9") == []


@pytest.mark.skipif(GIT is None, reason="git not available")
def test_changed_since_restricts_scope(tmp_path):
    root = make_repo(tmp_path, [node("N-OLD", "PROVED_LEAN"), node("N-OTHER", "OPEN")], {"README.md": "ok\n"})
    run_git(root, "init", "-q", "-b", "main")
    run_git(root, "add", "-A")
    run_git(root, "commit", "-q", "-m", "base")
    full = oc.scan(root)
    assert any(f.subject == "N-OLD" for f in rules(full, "R1"))
    assert oc.scan(root, oc.load_diff(root, "main")) == []
    make_repo(root, [node("N-OLD", "PROVED_LEAN", statement="changed"), node("N-OTHER", "OPEN")])
    scoped = oc.scan(root, oc.load_diff(root, "main"))
    assert {f.subject for f in scoped if f.rule == "R1"} == {"N-OLD"}


# ---- driver --------------------------------------------------------------------------------


def test_findings_are_deterministic_and_sorted(tmp_path):
    root = make_repo(tmp_path, [node(f"N-{i}", "PROVED_LEAN") for i in (3, 1, 2)], {"README.md": "revolutionary\n"})
    a, b = oc.scan(root), oc.scan(root)
    assert a == b
    assert oc.render_json(a) == oc.render_json(b) and oc.render_md(a) == oc.render_md(b)
    assert [f.sort_key() for f in a] == sorted(f.sort_key() for f in a)
    assert a[0].severity == "HIGH"


def test_strict_fails_only_on_new_high(tmp_path):
    root = make_repo(tmp_path, [node("N-OLD", "PROVED_LEAN")])
    assert oc.main(["--repo-root", str(root), "--write-baseline"]) == 0
    assert oc.main(["--repo-root", str(root), "--strict"]) == 0
    make_repo(root, [node("N-OLD", "PROVED_LEAN"), node("N-NEW", "PROVED_LEAN")])
    assert oc.main(["--repo-root", str(root), "--strict"]) == 1
    assert oc.main(["--repo-root", str(root)]) == 0


def test_write_then_check_roundtrip_and_stale(tmp_path):
    root = make_repo(tmp_path, [node("N-OLD", "PROVED_LEAN")])
    assert oc.main(["--repo-root", str(root), "--check"]) == 1  # nothing committed yet
    assert oc.main(["--repo-root", str(root), "--write"]) == 0
    assert oc.main(["--repo-root", str(root), "--check"]) == 0
    make_repo(root, [node("N-OLD", "PROVED_LEAN"), node("N-NEW", "PROVED_LEAN")])
    assert oc.main(["--repo-root", str(root), "--check"]) == 1
    assert b"\r" not in (root / "docs" / "overclaim" / "report.md").read_bytes()


def test_write_refuses_changed_since(tmp_path):
    root = make_repo(tmp_path, [])
    assert oc.main(["--repo-root", str(root), "--write", "--changed-since", "main"]) == 2


def test_strip_lean_keeps_line_numbers():
    src = 'a /- x\n y -/ b "s\n t" c -- d\n e'
    out = oc.strip_lean(src)
    assert out.count("\n") == src.count("\n") and "x" not in out and "d" not in out.split("\n")[2]


def test_committed_baseline_is_consistent_with_a_fresh_scan():
    """Every HIGH finding of a fresh scan of this checkout is in docs/overclaim/baseline.json (the committed gate)."""
    known = oc.load_baseline(REAL_ROOT / oc.SELF_BASELINE)
    assert known, "docs/overclaim/baseline.json is missing or empty"
    fresh = {f.key for f in oc.scan(REAL_ROOT) if f.severity == "HIGH"}
    assert fresh <= known, "new HIGH findings not in the baseline: " + ", ".join(sorted(fresh - known)[:5])