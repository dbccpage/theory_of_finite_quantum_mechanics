"""Origin: scripts/auto/test_auto_checks.py
Claim: tests for the five scripts/auto modules; every scanner runs against small git fixture repositories built in tmp_path, never against the checkout
AuthorityEffect: None
Scope Fence: verification evidence for the scanners' stated rules only; a passing suite says nothing about the repository's mathematics

Run: python -m pytest scripts/auto/test_auto_checks.py -q -p no:cacheprovider
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable, NoReturn

import pytest

HERE = Path(__file__).resolve().parent
for entry in (HERE, HERE.parent):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

import anti_pattern_lint as apl  # noqa: E402
import auto_common as common  # noqa: E402
import estate_audit as estate  # noqa: E402
import obstruction_scan as obs  # noqa: E402
import symmetry_scan as sym  # noqa: E402
from auto_common import AuditError, Finding  # noqa: E402


# --------------------------------------------------------------------------------------------
# fixtures


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@example.org",
                           "-c", "core.autocrlf=false", *args], check=True, capture_output=True, text=True).stdout


def write(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def make_repo(root: Path, files: dict[str, str]) -> Path:
    write(root, files)
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    git(root, "tag", "base")
    return root


def rules(findings: Iterable[Finding]) -> list[str]:
    return sorted(f.rule for f in findings)


SCANNER_SRC = 'ALLOWED_AXIOMS = ("propext", "Classical.choice", "Quot.sound")\nLEAN_ADMISSION_TOKENS = ("sorry", "admit", "native_decide", "unsafe")\n'
VALIDATOR_SRC = ('PFP_STATUS_RANK = {"OPEN": 0, "IMPORTED_ASSUMPTION": 1, "CONDITIONAL": 2, "COMPUTATIONALLY_CHECKED": 3, '
                 '"PROVED_PROSE": 4, "PROVED_LEAN": 5}\nFORBIDDEN = ("proves", "obviously", "simply", "guarantees")\n')


def dag(nodes: dict[str, str], routes: list[tuple[str, str, list[str], str]]) -> str:
    return json.dumps({"nodes": [{"id": i, "status": s} for i, s in nodes.items()],
                       "routes": [{"id": r, "status": s, "inputs": ins, "output": out} for r, s, ins, out in routes]}, indent=1)


# --------------------------------------------------------------------------------------------
# auto_common


def test_finding_rejects_unknown_severity() -> None:
    with pytest.raises(AuditError):
        Finding("X", "CRITICAL", "a", 1, "m")


def test_finding_render_with_and_without_line() -> None:
    assert Finding("R", "LOW", "a.py", 3, "msg", "d").render() == "[LOW] R a.py:3: msg (d)"
    assert Finding("R", "HIGH", "a.py", 0, "msg").render() == "[HIGH] R a.py: msg"


def test_exit_status_thresholds() -> None:
    found = [Finding("R", "MEDIUM", "a", 1, "m")]
    assert common.exit_status(found, "HIGH") == 0
    assert common.exit_status(found, "MEDIUM") == 1
    assert common.exit_status(found, "LOW") == 1
    assert common.exit_status(found, "none") == 0
    assert common.exit_status([], "LOW") == 0


@pytest.mark.parametrize("text,ok,error", [
    ("---\nname: a\n---\nbody", True, ""),
    ("no front matter", False, "no opening"),
    ("---\nname: a\n", False, "no closing"),
    ("---\nname: [a\n---\n", False, "not valid YAML"),
    ("---\n- a\n---\n", False, "not a mapping"),
])
def test_parse_front_matter(text: str, ok: bool, error: str) -> None:
    meta, body, err = common.parse_front_matter(text)
    assert (meta is not None) == ok
    assert error in err
    if ok:
        assert meta == {"name": "a"} and body.strip() == "body"


def test_sentences_split_on_capital_after_stop() -> None:
    assert common.sentences("One thing. Two things; `three` here. e.g. lower") == ["One thing.", "Two things;", "`three` here. e.g. lower"]


def test_render_markdown_and_json_counts() -> None:
    found = [Finding("R", "HIGH", "a|b", 2, "m")]
    md = common.render_markdown("T", found, "scope")
    assert "1 HIGH, 0 MEDIUM, 0 LOW" in md and "a\\|b" not in md and "`a|b:2`" in md
    assert "No findings" in common.render_markdown("T", [], "scope")
    doc = json.loads(common.render_json("tool", found, "scope"))
    assert doc["counts"] == {"HIGH": 1, "MEDIUM": 0, "LOW": 0} and doc["findings"][0]["line"] == 2


def test_render_markdown_limit() -> None:
    found = [Finding("R", "LOW", "a", i, "m") for i in range(1, 6)]
    assert "3 more findings not shown." in common.render_markdown("T", found, "s", limit=2)


def test_git_helpers_on_fixture(tmp_path: Path) -> None:
    root = make_repo(tmp_path, {"a.txt": "one\ntwo\n", "keep.txt": "x\n"})
    write(root, {"a.txt": "one\nnew\ntwo\n", "b.txt": "fresh\nline\n"})
    assert common.changed_files(root, "base") == ["a.txt", "b.txt"]
    assert common.added_lines(root, "base", "a.txt") == {2}
    assert common.added_lines(root, "base", "b.txt") == {1, 2}
    assert common.tracked_files(root) == ["a.txt", "keep.txt"]
    assert common.tracked_files(root, untracked=True) == ["a.txt", "b.txt", "keep.txt"]
    assert common.show_at(root, "base", "a.txt") == "one\ntwo\n"
    assert common.show_at(root, "base", "missing.txt") is None


def test_git_error_is_audit_error(tmp_path: Path) -> None:
    root = make_repo(tmp_path, {"a.txt": "x\n"})
    with pytest.raises(AuditError):
        common.merge_base(root, "no-such-ref")


def test_run_main_maps_audit_error_to_exit_2(capsys: pytest.CaptureFixture[str]) -> None:
    def body() -> NoReturn:
        raise AuditError("boom")
    assert common.run_main("tool", body) == 2
    assert "tool: error: boom" in capsys.readouterr().err


def test_emit_writes_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    args = common.base_parser("d").parse_args(["--summary", str(tmp_path / "s.md"), "--fail-on", "LOW"])
    status = common.emit("tool", "Title", [Finding("R", "LOW", "a", 1, "m")], args, "scope")
    assert status == 1
    assert "## Title" in (tmp_path / "s.md").read_text(encoding="utf-8")
    assert "tool: 0 HIGH, 0 MEDIUM, 1 LOW (scope)" in capsys.readouterr().out


# --------------------------------------------------------------------------------------------
# anti_pattern_lint


LEAN = """theorem a : True := by
  sorry
-- sorry in a comment
/- admit in a block
   comment -/
def s := "native_decide in a string"
inductive Tok
  | admit (t : Nat)
axiom smuggled : False
theorem axiom_free : True := trivial
@[simp] private axiom other : True
  exact (by admit)
"""


def test_lean_findings_tokens_and_axioms() -> None:
    found = apl.lean_findings("m.lean", LEAN, None)
    assert [(f.rule, f.line) for f in found] == [("AP_LN_001", 2), ("AP_LN_004", 9), ("AP_LN_004", 11), ("AP_LN_001", 12)]


def test_lean_findings_only_added_lines() -> None:
    assert [f.line for f in apl.lean_findings("m.lean", LEAN, {9, 12})] == [9, 12]
    assert apl.lean_findings("m.lean", LEAN, set()) == []


def test_python_token_rules() -> None:
    code = 'x = 1  # type: ignore\ny = 2  # type: ignore[attr-defined]\np = "C:\\\\Users\\\\me\\\\x"\nq = "/home/me/x"\n# "C:\\\\Users\\\\me"\n'
    found = apl.python_token_findings("scripts/a.py", code)
    assert [(f.rule, f.line) for f in found] == [("AP_PY_001", 1), ("AP_PY_006", 3), ("AP_PY_006", 4)]
    assert rules(apl.python_token_findings("scripts/test_a.py", code)) == ["AP_PY_001"]


def test_float_literals_only_in_independent_checks() -> None:
    code = "a = 1.5\nb = 2\nc = 1e3\nd = 0x1e\ne = 2j\n"
    found = apl.python_token_findings("checks/independent/x.py", code)
    assert [f.line for f in found] == [1, 3]
    assert apl.python_token_findings("scripts/x.py", code) == []


def test_ast_rules_in_tests_and_independent_checks() -> None:
    test_code = ("import pytest\ndef test_a():\n    assert 2 % 2 == 0\n    assert True\n    assert f(1) == 1\n"
                 "    assert (1, 2) == (1, 2)\n    with pytest.raises(ValueError):\n        raise ValueError('x')\n"
                 "    with pytest.raises(ValueError):\n        f(0)\n")
    found = apl.python_ast_findings("scripts/test_a.py", test_code)
    assert [(f.rule, f.line) for f in found] == [("AP_PY_019", 3), ("AP_PY_019", 4), ("AP_PY_019", 6), ("AP_PY_019", 7)]
    assert apl.python_ast_findings("scripts/a.py", test_code) == []
    check = "import math\nx = float(3)\ny = math.sqrt(2)\nz = math.pi\nw = expr.evalf()\nv = abs(-2)\n"
    assert [f.line for f in apl.python_ast_findings("checks/independent/c.py", check)] == [2, 3, 4, 5]
    bad = apl.python_ast_findings("checks/independent/bad.py", "def (:\n")
    assert [(f.rule, f.severity, f.line) for f in bad] == [("UNPARSEABLE", "LOW", 1)]


def test_in_scope_and_test_file() -> None:
    assert not common.in_scope("dag/results/X/run.py") and not common.in_scope("lean4/.lake/x.lean")
    assert common.in_scope("lean4/A.lean")
    assert apl.is_test_file("code/python/tests/helper.py") and apl.is_test_file("a/test_b.py") and not apl.is_test_file("a/b.py")


def card(pid: str, dual: str) -> str:
    return f"---\npattern_id: {pid}\ndual_pattern: {dual}\n---\n# card\n"


def catalog(root: Path, extra: dict[str, str] | None = None) -> None:
    files = {f".agents/patterns/{side}/{slot}/.keep": "" for side in ("anti", "helpful") for slot in apl.REQUIRED_SLOTS}
    files[".agents/patterns/anti/python/AP_PY_001_a.md"] = card("AP_PY_001", "HP_PY_001_b")
    files[".agents/patterns/helpful/python/HP_PY_001_b.md"] = card("HP_PY_001", "AP_PY_001_a")
    files.update(extra or {})
    write(root, files)


def test_catalog_clean_and_defects(tmp_path: Path) -> None:
    catalog(tmp_path)
    assert apl.audit_catalog(tmp_path) == []
    catalog(tmp_path, {
        ".agents/patterns/anti/python/AP_PY_002_c.md": card("AP_PY_009", "HP_PY_001_b"),
        ".agents/patterns/anti/python/AP_PY_003_d.md": card("AP_PY_003", "HP_PY_003_missing"),
        ".agents/patterns/anti/python/AP_PY_004_e.md": "---\npattern_id: AP_PY_004\n---\n",
        ".agents/patterns/anti/python/HP_PY_005_f.md": card("HP_PY_005", "x"),
        ".agents/patterns/anti/python/AP_PY_006_g.md": "no front matter",
    })
    assert rules(apl.audit_catalog(tmp_path)) == ["CARD_FRONT_MATTER", "CARD_ID_MISMATCH", "CARD_NAME", "DUAL_FILE_MISSING",
                                                  "DUAL_MISSING", "DUAL_NOT_RECIPROCAL"]


def test_catalog_missing_and_slot(tmp_path: Path) -> None:
    assert rules(apl.audit_catalog(tmp_path)) == ["CATALOG_MISSING"]
    (tmp_path / ".agents/patterns/anti/lean4").mkdir(parents=True)
    assert len(apl.audit_catalog(tmp_path)) == 2 * len(apl.REQUIRED_SLOTS) - 1


def test_lint_cli_gates_only_added_lean_lines(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = make_repo(tmp_path, {"lean4/A.lean": "theorem a : True := by\n  sorry\n", "dag/results/x/B.lean": "x\n"})
    catalog(root)
    assert apl.main(["--repo-root", str(root), "--changed-since", "base"]) == 0
    write(root, {"lean4/A.lean": "theorem a : True := by\n  sorry\ntheorem b : True := by admit\n",
                 "dag/results/x/B.lean": "sorry\n", "lean4/New.lean": "axiom n : False\n"})
    assert apl.main(["--repo-root", str(root), "--changed-since", "base"]) == 1
    out = capsys.readouterr().out
    assert "lean4/A.lean:3" in out and "lean4/A.lean:2" not in out and "lean4/New.lean:1" in out and "dag/results" not in out
    assert apl.main(["--repo-root", str(root), "--fail-on", "none", "--json"]) == 0
    doc = json.loads(capsys.readouterr().out)
    # whole-checkout mode reads the git index: both A.lean lines, not the untracked New.lean
    assert [(f["path"], f["line"]) for f in doc["findings"] if f["severity"] == "HIGH"] == [("lean4/A.lean", 2), ("lean4/A.lean", 3)]


def test_lint_cli_not_a_checkout(tmp_path: Path) -> None:
    assert apl.main(["--repo-root", str(tmp_path)]) == 2


# --------------------------------------------------------------------------------------------
# obstruction_scan


def test_module_index_and_top_names() -> None:
    files = ["scripts/tool.py", "code/python/src/qm/__init__.py", "code/python/src/qm/core.py", "dag/my-hyphen.py"]
    index = obs.module_index(Path("."), files)
    assert index["tool"] == "scripts/tool.py" and index["qm"] == "code/python/src/qm/__init__.py"
    assert index["qm.core"] == "code/python/src/qm/core.py" and index["scripts.tool"] == "scripts/tool.py"
    assert "my-hyphen" not in index
    top = obs.repository_top_names(index)
    assert {"tool", "qm", "scripts"} <= top and "code" not in top  # `code` is also a standard-library module
    assert "json" not in obs.repository_top_names({"json": "x.py"})


def test_rule_o1() -> None:
    import ast
    tree = ast.parse("import sympy\nimport json\nfrom qm.core import f\nimport sys\nsys.path.insert(0, '.')\nfrom . import y\n")
    found = obs.rule_o1(Path("."), "checks/independent/c.py", tree, {"qm"})
    assert sorted((f.line, f.severity) for f in found) == [(3, "HIGH"), (5, "MEDIUM"), (6, "HIGH")]


def test_import_cycles_and_resolution(tmp_path: Path) -> None:
    files = {
        "scripts/a.py": "import b\n",
        "scripts/b.py": "from c import x\n",
        "scripts/c.py": "import a\n",
        "scripts/d.py": "import a\ndef f():\n    import d2\n",
        "scripts/d2.py": "import d\n",
        "code/python/src/pkg/__init__.py": "from . import m\n",
        "code/python/src/pkg/m.py": "from .n import thing\n",
        "code/python/src/pkg/n.py": "from pkg import m\n",
    }
    make_repo(tmp_path, files)
    found = obs.python_findings(tmp_path, {"O2"}, None)
    assert [f.detail for f in found] == ["code/python/src/pkg/__init__.py, code/python/src/pkg/m.py, code/python/src/pkg/n.py",
                                         "scripts/a.py, scripts/b.py, scripts/c.py"]
    focused = obs.python_findings(tmp_path, {"O2"}, {"scripts/d.py"})
    assert focused == []
    assert len(obs.python_findings(tmp_path, {"O2"}, {"scripts/b.py"})) == 1


def test_strongly_connected_ignores_tails_and_self_loops() -> None:
    graph = {"a": {"b"}, "b": {"a", "c"}, "c": {"c"}, "d": {"a"}}
    assert obs.strongly_connected(graph) == [["a", "b"]]


def test_resolve_relative_too_deep() -> None:
    import ast
    node = ast.parse("from .... import x").body[0]
    assert isinstance(node, ast.ImportFrom)
    assert obs.resolve_targets("a/b.py", node, {}, {"a/x.py"}) == set()


def test_rule_o3_and_changes() -> None:
    doc = json.loads(dag({"A": "OPEN", "B": "PROVED_LEAN", "C": "DEFINITION", "D": "PROVED_LEAN", "E": "REFUTED"},
                         [("R1", "DERIVED_LEAN", ["A", "C"], "B"), ("R2", "GAP_NO_DERIVATION", ["A"], "D"),
                          ("R3", "COMPUTED", ["E"], "D"), ("R4", "DERIVED_LEAN", ["C"], "D"), ("R5", "RECORD_PARENT", ["A"], "C")]))
    found = obs.rule_o3(doc, {"R1": 7}, None)
    assert [(f.line, f.message.split()[1]) for f in found] == [(7, "R1"), (0, "R3")]
    assert "no other derived route" in found[0].detail and found[1].detail.startswith("1 other")
    assert obs.rule_o3(doc, {}, {"Z"}) == [] and len(obs.rule_o3(doc, {}, {"C"})) == 1


def test_load_dag_errors() -> None:
    for text in (None, "{", "[]", '{"nodes": []}'):
        with pytest.raises(AuditError):
            obs.load_dag(text, "dag")


def test_id_lines_and_changed_ids() -> None:
    assert obs.id_lines('{\n "id": "A",\n  "id": "B"\n}') == {"A": 2, "B": 3}
    old = json.loads(dag({"A": "OPEN"}, []))
    new = json.loads(dag({"A": "PROVED_LEAN", "B": "OPEN"}, []))
    assert obs.changed_dag_ids(new, old) == {"A", "B"}


def test_obstruction_cli_changed_since(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    base = dag({"A": "OPEN", "B": "PROVED_LEAN", "C": "DEFINITION"}, [("R1", "DERIVED_LEAN", ["C"], "B")])
    root = make_repo(tmp_path, {"dag/derivation_dag.json": base, "checks/independent/c.py": "import fractions\n",
                                "scripts/tool.py": "x = 1\n"})
    assert obs.main(["--repo-root", str(root), "--changed-since", "base", "--fail-on", "LOW"]) == 0
    write(root, {"dag/derivation_dag.json": dag({"A": "OPEN", "B": "PROVED_LEAN", "C": "DEFINITION"},
                                                [("R1", "DERIVED_LEAN", ["C", "A"], "B")]),
                 "checks/independent/c.py": "import tool\n"})
    assert obs.main(["--repo-root", str(root), "--changed-since", "base"]) == 1
    out = capsys.readouterr().out
    assert "[HIGH] O1 checks/independent/c.py:1" in out and "route R1" in out
    assert obs.main(["--repo-root", str(root), "--only", "O3", "--fail-on", "none"]) == 0


def test_obstruction_cli_missing_dag(tmp_path: Path) -> None:
    root = make_repo(tmp_path, {"a.txt": "x\n"})
    assert obs.main(["--repo-root", str(root), "--only", "O3"]) == 2


# --------------------------------------------------------------------------------------------
# symmetry_scan


def sym_repo(root: Path, lint_tokens: str = '("sorry", "admit", "native_decide", "unsafe", "axiom")', extra: dict[str, str] | None = None) -> Path:
    files = {"scripts/overclaim_scan.py": SCANNER_SRC, "dag/validate_derivation_dag.py": VALIDATOR_SRC,
             "scripts/auto/anti_pattern_lint.py": f"LEAN_FORBIDDEN = {lint_tokens}\n"}
    files.update(extra or {})
    return make_repo(root, files)


def test_reference_and_token_drift(tmp_path: Path) -> None:
    ref, found = sym.load_reference(sym_repo(tmp_path))
    assert ref.axioms == {"propext", "Classical.choice", "Quot.sound"} and "axiom" in ref.tokens and found == []
    assert ref.ranks["PROVED_LEAN"] == 5 and "simply" in ref.forbidden
    _, drift = sym.load_reference(sym_repo(tmp_path / "b", '("sorry",)'))
    assert rules(drift) == ["SYM_TOKENS"] and drift[0].severity == "HIGH"


def test_literal_assignment_errors(tmp_path: Path) -> None:
    write(tmp_path, {"m.py": "X = f()\nY: int = 3\n", "bad.py": "def (:"})
    assert sym.literal_assignment(tmp_path, "m.py", "Y") == 3
    for rel, name in (("m.py", "X"), ("m.py", "Z"), ("bad.py", "X"), ("absent.py", "X")):
        with pytest.raises(AuditError):
            sym.literal_assignment(tmp_path, rel, name)


@pytest.fixture()
def reference() -> sym.Reference:
    return sym.Reference(frozenset({"propext", "Classical.choice", "Quot.sound"}),
                         frozenset({"sorry", "admit", "native_decide", "unsafe", "axiom"}),
                         {"OPEN": 0, "CONDITIONAL": 2, "PROVED_PROSE": 4, "PROVED_LEAN": 5}, frozenset({"proves", "simply"}))


def test_check_axioms(reference: sym.Reference) -> None:
    assert sym.check_axioms("f", 1, "It compiles with only propext, Classical.choice and Quot.sound.", reference) == []
    found = sym.check_axioms("f", 1, "Allowed: only propext, Classical.choice and funext.", reference)
    assert [(f.severity, f.message.split(":")[0]) for f in found] == [("HIGH", "DANGEROUS_DRIFT"), ("MEDIUM", "MISSING_PROPAGATION")]
    assert sym.check_axioms("f", 1, "propext and Classical.choice appear, with funext.", reference) == []


def test_check_tokens(reference: sym.Reference) -> None:
    assert sym.check_tokens("f", 1, "No sorry, admit, axiom, native_decide or unsafe.", reference) == []
    found = sym.check_tokens("f", 1, "No sorry, native_decide or extern.", reference)
    assert [f.severity for f in found] == ["LOW", "MEDIUM"]
    assert sym.check_tokens("f", 1, "sorry alone", reference) == []


def test_check_status_order(reference: sym.Reference) -> None:
    assert sym.check_status_order("f", 1, "OPEN < CONDITIONAL < PROVED_LEAN", reference) == []
    found = sym.check_status_order("f", 1, "OPEN < PROVED_LEAN < PROVED_PROSE and OPEN < WIBBLE < PROVED_LEAN", reference)
    assert [(f.severity, f.message.split(":")[0]) for f in found] == [("HIGH", "CONTRADICTION"), ("MEDIUM", "STALE_RULE")]


def test_check_forbidden_words(reference: sym.Reference) -> None:
    good = 'The validator refuses words: "proves", "simply" and "proves".'
    assert sym.check_forbidden_words("f", 1, good, reference) == []
    bad = 'The validator refuses `proves`, `simply`, `elegant`.'
    assert "elegant" in sym.check_forbidden_words("f", 1, bad, reference)[0].message
    assert sym.check_forbidden_words("f", 1, "`proves`, `simply`, `elegant` with no cue", reference) == []
    assert sym.quoted_runs('`a1x` then a long gap of more than thirty characters here `bbb`, `ccc`') == []
    assert sym.quoted_runs('"aaa", "bbb" and "ccc"') == [["aaa", "bbb", "ccc"]]


def test_paragraphs_skip_fences() -> None:
    text = "one\ntwo\n\n```\nOPEN < X < Y\n```\nthree\n"
    assert sym.paragraphs(text) == [(1, "one two"), (7, "three")]


def test_symmetry_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = sym_repo(tmp_path, extra={"CONTRIBUTING.md": "Lean must compile with only propext and Classical.choice.\n"})
    assert sym.main(["--repo-root", str(root)]) == 0
    assert "MISSING_PROPAGATION" in capsys.readouterr().out
    write(root, {"README.md": "Order: OPEN < PROVED_LEAN < CONDITIONAL.\n"})
    git(root, "add", "README.md")
    assert sym.main(["--repo-root", str(root), "--changed-since", "base"]) == 1
    out = capsys.readouterr().out
    assert "README.md" in out and "CONTRIBUTING.md" not in out
    assert sym.main(["--repo-root", str(tmp_path / "nope")]) == 2


# --------------------------------------------------------------------------------------------
# estate_audit


SKILL = "---\nname: good-skill\ndescription: Use when testing the estate audit; it checks names, links and wording.\n---\n# T\n\n## Steps\n\nSee [ref](ref.md).\n"


def test_manifest_findings() -> None:
    assert estate.manifest_findings("s", SKILL, "good-skill", "skill") == []
    assert rules(estate.manifest_findings("s", "no fm", "x", "skill")) == ["INVALID_FRONT_MATTER"]
    assert rules(estate.manifest_findings("s", SKILL, "other", "skill")) == ["NAME_PATH_MISMATCH"]
    bad = "---\nname: Bad_Name\ndescription: short\n---\nbody\n"
    assert rules(estate.manifest_findings("s", bad, "Bad_Name", "skill")) == ["DESCRIPTION_LENGTH", "NAME_FORMAT", "NO_SECTIONS"]
    assert rules(estate.manifest_findings("a", "---\nname: 3\n---\n", "a", "agent")) == ["MISSING_FIELD", "MISSING_FIELD"]


def test_link_findings(tmp_path: Path) -> None:
    write(tmp_path, {"d/ok.md": "x", "scripts/real.py": ""})
    text = ("[ok](ok.md) [anchor](ok.md#x) [web](https://x.org) [bad](gone.md) [tpl](<date>.md) ![img](no.png)\n"
            "`scripts/real.py` `scripts/missing.py` `docs/<date>_x.md` `scripts/real.py`.\n")
    found = estate.link_findings(tmp_path, "d/page.md", text)
    assert [(f.rule, f.line) for f in found] == [("BROKEN_LINK", 1), ("MISSING_PATH", 2)]


def test_wording_findings() -> None:
    text = ("Copy omega_engine_operads/skills here.\nAdapted from the_symbol_game omega_engine_operads/x.\n"
            "The agent may self-certify its output. Never self-certify.\nCheck for self-certifying tests.\n"
            "It raises the status when tests pass.\n"
            'Wording such as "self-certify" or `raise a status` is a mention.\n')
    assert [(f.rule, f.line) for f in estate.wording_findings("s.md", text)] == [
        ("FOREIGN_PATH", 1), ("AUTHORITY_UNSAFE", 3), ("AUTHORITY_UNSAFE", 5)]


def test_header_findings(tmp_path: Path) -> None:
    write(tmp_path, {"scripts/auto/a.py": '"""Origin: x\nClaim: y\nAuthorityEffect: None\nScope Fence: z\n"""\n',
                     "scripts/auto/b.py": '"""Origin: x"""\n'})
    assert estate.header_findings(tmp_path, "scripts/auto/a.py") == []
    assert "Claim:" in estate.header_findings(tmp_path, "scripts/auto/b.py")[0].message


def test_estate_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = make_repo(tmp_path, {".claude/skills/good-skill/SKILL.md": SKILL, ".claude/skills/good-skill/ref.md": "ok\n",
                                ".claude/skills/bad/SKILL.md": "---\nname: wrong\ndescription: d\n---\n",
                                ".agents/teamwork/t/BRIEFING.md": "You may approve your own work.\n",
                                ".claude/agents/helper.md": "---\nname: helper\ndescription: Helps with a narrow, named repository task.\n---\n",
                                "docs/a.md": "[x](missing.md)\n", "scripts/auto/new.py": "x = 1\n"})
    assert estate.main(["skills", "--repo-root", str(root)]) == 1
    assert "NAME_PATH_MISMATCH" in capsys.readouterr().out
    assert estate.main(["agents", "--repo-root", str(root), "--fail-on", "MEDIUM"]) == 1
    assert "approve your own" in capsys.readouterr().out
    assert estate.main(["docs", "--repo-root", str(root), "--paths", "docs", "--fail-on", "MEDIUM"]) == 1
    assert estate.main(["docs", "--repo-root", str(root), "--paths", "nowhere"]) == 2
    assert estate.main(["docs", "--repo-root", str(root), "--fail-on", "LOW"]) == 1
    assert "MISSING_HEADER" in capsys.readouterr().out
    write(root, {"docs/b.md": "[y](a.md)\n"})
    assert estate.main(["docs", "--repo-root", str(root), "--changed-since", "base", "--fail-on", "LOW"]) == 0


# --------------------------------------------------------------------------------------------
# Boundaries, severities and branch alternatives (each test below was added to kill a surviving mutant)


@pytest.mark.parametrize("script", ["anti_pattern_lint", "obstruction_scan", "symmetry_scan", "estate_audit"])
def test_scripts_run_under_isolated_python(script: str) -> None:
    """python -I does not put the script directory on sys.path; each script must add it itself."""
    done = subprocess.run([sys.executable, "-I", "-X", "utf8", str(HERE / f"{script}.py"), "--help"],
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0 and "--fail-on" in done.stdout


def test_fail_on_accepts_every_severity() -> None:
    parser = common.base_parser("d")
    for choice in common.FAIL_CHOICES:
        assert parser.parse_args(["--fail-on", choice]).fail_on == choice
    assert common.SEVERITIES == ("HIGH", "MEDIUM", "LOW")


def test_render_markdown_exact_limit_and_unicode() -> None:
    found = [Finding("R", "LOW", "a", i, "m") for i in range(1, 3)]
    assert "more findings" not in common.render_markdown("T", found, "s", limit=2)
    assert "ψ" in common.render_json("tool", [Finding("R", "LOW", "ψ.md", 1, "m")], "s")


def test_added_lines_for_a_file_dropped_from_the_index(tmp_path: Path) -> None:
    root = make_repo(tmp_path, {"a.txt": "one\ntwo\n"})
    git(root, "rm", "-q", "--cached", "a.txt")
    assert common.added_lines(root, "base", "a.txt") == {1, 2}


def test_in_scope() -> None:
    assert not common.in_scope("dag/results/X/run.py") and not common.in_scope("lean4/.lake/x.lean")
    assert not common.in_scope("atlas/x.md") and common.in_scope("lean4/A.lean")


def test_admit_identifier_is_not_the_tactic() -> None:
    lean = ("noncomputable def admit {n} (d : Nat) : Nat := d\n"
            "theorem t (h : admit d g = 1) : True := by\n"
            "  unfold admit at h\n"
            "  simp [admit]\n"
            "  · admit\n"
            "  admit <;> simp\n")
    assert [f.line for f in apl.lean_findings("m.lean", lean, None)] == [5, 6]
    assert [(f.rule, f.severity) for f in apl.lean_findings("m.lean", "sorry\naxiom a : False\n", None)] == [
        ("AP_LN_001", "HIGH"), ("AP_LN_004", "HIGH")]


def test_lint_severities_and_negatives() -> None:
    tokens = apl.python_token_findings("checks/independent/c.py", 'x = 1.0  # type: ignore\np = "/home/me/f"\n')
    assert sorted((f.rule, f.severity) for f in tokens) == [("AP_MATH_011", "MEDIUM"), ("AP_PY_001", "LOW"), ("AP_PY_006", "MEDIUM")]
    test_code = ("import pytest\ndef test_a(x):\n    assert x\n    assert 1 + x == 2\n    with open(x):\n        raise ValueError\n"
                 "    with pytest.warns(UserWarning):\n        raise ValueError\n    assert 2 % 2 == 0\n")
    found = apl.python_ast_findings("scripts/test_a.py", test_code)
    assert [(f.rule, f.severity, f.line) for f in found] == [("AP_PY_019", "MEDIUM", 9)]
    check = "import math\nother.sqrt(2)\nmath.floor(2)\n(lambda: 1)()\nmath.sqrt(2)\nnp.pi\n"
    assert [(f.severity, f.line) for f in apl.python_ast_findings("checks/independent/c.py", check)] == [("MEDIUM", 5)]


def test_lint_unreadable_file(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_bytes(b"\xff\xfe\x00")
    assert [(f.rule, f.severity) for f in apl.scan_file(tmp_path, "bad.py", None)] == [("UNREADABLE", "LOW")]
    assert apl.scan_file(tmp_path, "notes.txt", None) == []


def test_lint_scan_defaults_to_files_and_catalog(tmp_path: Path) -> None:
    root = make_repo(tmp_path, {"lean4/A.lean": "sorry\n"})
    catalog(root)
    found, scope = apl.scan(root, None)
    assert "AP_LN_001" in rules(found) and scope.startswith("whole checkout")
    found, scope = apl.scan(root, None, True)
    assert found == [] and scope == "pattern catalog"


def test_catalog_severities(tmp_path: Path) -> None:
    assert [f.severity for f in apl.audit_catalog(tmp_path)] == ["MEDIUM"]
    catalog(tmp_path, {".agents/patterns/anti/python/AP_PY_002_c.md": card("AP_PY_009", "HP_PY_404_none"),
                       ".agents/patterns/anti/python/AP_PY_004_e.md": "---\npattern_id: AP_PY_004\n---\n",
                       ".agents/patterns/anti/python/HP_PY_005_f.md": card("HP_PY_005", "x"),
                       ".agents/patterns/anti/python/AP_PY_006_g.md": "no front matter",
                       ".agents/patterns/anti/python/AP_PY_007_h.md": card("AP_PY_007", "HP_PY_001_b")})
    assert {f.severity for f in apl.audit_catalog(tmp_path)} == {"MEDIUM"}
    assert rules(apl.audit_catalog(tmp_path)) == ["CARD_FRONT_MATTER", "CARD_ID_MISMATCH", "CARD_NAME", "DUAL_FILE_MISSING",
                                                  "DUAL_MISSING", "DUAL_NOT_RECIPROCAL"]


def test_edits_sys_path_negatives() -> None:
    import ast
    tree = ast.parse("import sys, os\nsys.path.copy()\nos.path.insert(0)\nx.append(1)\npath.insert(0, 'a')\nsys.path.append('b')\n")
    found = obs.rule_o1(Path("."), "checks/independent/c.py", tree, set())
    assert [(f.line, f.severity) for f in found] == [(6, "MEDIUM")]


def test_relative_import_at_exact_depth() -> None:
    import ast
    node = ast.parse("from .. import x").body[0]
    assert isinstance(node, ast.ImportFrom)
    assert obs.resolve_targets("a/b.py", node, {}, {"x.py"}) == {"x.py"}


def test_cycle_detail_truncates_after_six() -> None:
    six = {f"m{i}": {f"m{(i + 1) % 6}"} for i in range(6)}
    seven = {f"m{i}": {f"m{(i + 1) % 7}"} for i in range(7)}
    assert "more" not in obs.rule_o2(six, None)[0].detail
    found = obs.rule_o2(seven, None)
    assert found[0].detail.endswith("and 1 more") and found[0].severity == "MEDIUM"
    assert obs.rule_o2(seven, {"elsewhere.py"}) == []


def test_id_lines_at_column_zero() -> None:
    assert obs.id_lines('"id": "A"\n') == {"A": 1}


def test_o3_gap_alternative_is_not_a_clean_route() -> None:
    doc = json.loads(dag({"A": "OPEN", "B": "PROVED_LEAN", "C": "DEFINITION"},
                         [("R1", "DERIVED_LEAN", ["A"], "B"), ("R2", "GAP_NO_DERIVATION", ["C"], "B")]))
    found = obs.rule_o3(doc, {}, None)
    assert found[0].detail.startswith("no other") and found[0].severity == "MEDIUM"


def test_python_files_focus_filters_scope(tmp_path: Path) -> None:
    root = make_repo(tmp_path, {"scripts/a.py": "x = 1\n"})
    write(root, {"other/b.py": "y = 2\n", "scripts/new.py": "z = 3\n"})
    assert obs.python_files(root, {"other/b.py", "scripts/new.py", "scripts/notes.md"}) == ["scripts/a.py", "scripts/new.py"]


def test_o1_respects_focus_and_reports_unparseable(tmp_path: Path) -> None:
    root = make_repo(tmp_path, {"scripts/tool.py": "x = 1\n", "checks/independent/c.py": "import tool\n",
                                "checks/independent/broken.py": "def (:\n"})
    assert obs.python_findings(root, {"O1"}, {"scripts/tool.py"}) == []
    found = obs.python_findings(root, {"O1"}, None)
    assert sorted((f.rule, f.severity, f.path) for f in found) == [
        ("O1", "HIGH", "checks/independent/c.py"), ("UNPARSEABLE", "LOW", "checks/independent/broken.py")]


def test_o3_when_the_dag_is_new_since_base(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = make_repo(tmp_path, {"a.txt": "x\n"})
    write(root, {"dag/derivation_dag.json": dag({"A": "OPEN", "B": "PROVED_LEAN"}, [("R1", "COMPUTED", ["A"], "B")])})
    assert obs.main(["--repo-root", str(root), "--changed-since", "base", "--only", "O3", "--json", "--fail-on", "none"]) == 0
    doc = json.loads(capsys.readouterr().out)
    assert [(f["rule"], f["line"] > 0) for f in doc["findings"]] == [("O3", True)]


def test_symmetry_exact_pair_equal_ranks_and_severities(reference: sym.Reference) -> None:
    found = sym.check_tokens("f", 1, "No sorry or native_decide.", reference)
    assert [(f.severity, f.message.split(":")[0]) for f in found] == [("MEDIUM", "MISSING_PROPAGATION")]
    ref = sym.Reference(reference.axioms, reference.tokens, {"OPEN": 0, "SOURCE_RECORD": 0, "PROVED_LEAN": 5}, reference.forbidden)
    assert [f.severity for f in sym.check_status_order("f", 1, "OPEN < SOURCE_RECORD < PROVED_LEAN", ref)] == ["HIGH"]
    stray = sym.check_forbidden_words("f", 1, 'The validator refuses "proves", "simply", "very much so".', reference)
    assert stray[0].severity == "MEDIUM" and "very much so" in stray[0].message


def test_quoted_runs_boundaries() -> None:
    exact_gap = "x" * 30
    assert sym.quoted_runs(f'"aaa"{exact_gap}"bbb", "ccc"') == [["aaa", "bbb", "ccc"]]
    assert sym.quoted_runs(f'"aaa"x{exact_gap}"bbb", "ccc"') == []
    assert sym.quoted_runs('"aaa", "bbb", "ccc" and then a gap that is far too long "ddd", "eee"') == [["aaa", "bbb", "ccc"]]
    assert sym.quoted_runs('"aaa", `x` "bbb", "ccc"') == []
    assert sym.quoted_runs('"aaa", "bbb"', min_len=2) == [["aaa", "bbb"]]


def test_reference_is_frozen(reference: sym.Reference) -> None:
    import dataclasses
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(reference, "axioms", frozenset())


def test_symmetry_unreadable_prose(tmp_path: Path) -> None:
    root = sym_repo(tmp_path, extra={"README.md": "ok\n"})
    (root / "README.md").write_bytes(b"\xff\xfe")
    found, _ = sym.scan(root, None)
    assert [(f.rule, f.severity) for f in found] == [("UNREADABLE", "LOW")]


def test_description_length_boundaries() -> None:
    def fm(desc: str) -> str:
        return f"---\nname: s\ndescription: {desc}\n---\n## A\n"
    assert estate.manifest_findings("s", fm("x" * 40), "s", "skill") == []
    assert estate.manifest_findings("s", fm("x" * 1024), "s", "skill") == []
    assert [f.severity for f in estate.manifest_findings("s", fm("x" * 1025), "s", "skill")] == ["MEDIUM"]
    agent = "---\nname: other\ndescription: An agent with a long enough description here.\n---\n"
    assert [(f.rule, f.severity) for f in estate.manifest_findings("a", agent, "helper", "agent")] == [("NAME_PATH_MISMATCH", "HIGH")]
    assert [(f.rule, f.severity) for f in estate.manifest_findings("s", "---\nname: s\n---\n## A\n", "s", "skill")] == [
        ("MISSING_FIELD", "HIGH")]


def test_estate_severities(tmp_path: Path) -> None:
    write(tmp_path, {"d/x.md": ""})
    found = estate.link_findings(tmp_path, "d/page.md", "[a](gone.md) `scripts/none.py`\n")
    assert [(f.rule, f.severity) for f in found] == [("BROKEN_LINK", "MEDIUM"), ("MISSING_PATH", "LOW")]
    wording = estate.wording_findings("s.md", "Copy omega_engine_operads/x.\nIt may self-certify.\n")
    assert [(f.rule, f.severity) for f in wording] == [("FOREIGN_PATH", "HIGH"), ("AUTHORITY_UNSAFE", "MEDIUM")]
    write(tmp_path, {"scripts/auto/b.py": "x = 1\n"})
    assert [f.severity for f in estate.header_findings(tmp_path, "scripts/auto/b.py")] == ["LOW"]
    (tmp_path / "bin.md").write_bytes(b"\xff\xfe")
    assert [(f.rule, f.severity) for f in estate.audit_document(tmp_path, "bin.md", "skill")] == [("UNREADABLE", "HIGH")]


def test_fenced_and_inline_code_are_not_links(tmp_path: Path) -> None:
    text = "```json\n[x](gone.md)\n```\n`[y](gone2.md)` and [z](gone3.md)\n"
    found = estate.link_findings(tmp_path, "page.md", text)
    assert [(f.line, f.message.split()[2]) for f in found] == [(4, "gone3.md")]


def test_skill_audit_reads_each_file_once(tmp_path: Path) -> None:
    write(tmp_path, {".claude/skills/good-skill/SKILL.md": SKILL.replace("[ref](ref.md)", "[gone](gone.md)"),
                     ".claude/skills/good-skill/ref.md": "[gone](gone.md)\n"})
    found, scope = estate.audit_skills(tmp_path)
    assert sorted(f.path for f in found) == [".claude/skills/good-skill/SKILL.md", ".claude/skills/good-skill/ref.md"]
    assert scope == "1 skills"


def test_docs_paths_scope(tmp_path: Path) -> None:
    write(tmp_path, {"scripts/x.py": "x = 1\n", "scripts/auto/y.py": "y = 1\n", "scripts/n.txt": "[a](b)\n",
                     "scripts/d.md": "[a](missing.md)\n"})
    assert sorted(estate._expand(tmp_path, "scripts")) == ["scripts/auto/y.py", "scripts/d.md", "scripts/x.py"]
    found, _ = estate.audit_docs(tmp_path, None, ["scripts"])
    assert sorted((f.rule, f.path) for f in found) == [("BROKEN_LINK", "scripts/d.md"), ("MISSING_HEADER", "scripts/auto/y.py")]
    (tmp_path / "scripts/bad.md").write_bytes(b"\xff\xfe")
    found, _ = estate.audit_docs(tmp_path, None, ["scripts/bad.md"])
    assert [(f.rule, f.severity) for f in found] == [("UNREADABLE", "LOW")]


@pytest.mark.parametrize("tactic", ["sorry", "admit", "native_decide"])
@pytest.mark.parametrize("prefix", ["theorem bad : True := by first | ", "  | "])
def test_tactic_alternatives_are_not_constructor_names(tactic: str, prefix: str) -> None:
    found = apl.lean_findings("m.lean", "theorem bad : True := by\n" + prefix + tactic + "\n", None)
    assert [(f.rule, f.severity, f.line) for f in found] == [("AP_LN_001", "HIGH", 2)]


def test_nullary_admit_constructor_and_match_arm_are_names() -> None:
    text = "inductive Token where\n  | admit\n  | other\ndef use (t : Token) := match t with\n  | admit => 0\n  | other => 1\n"
    assert apl.lean_findings("m.lean", text, None) == []
