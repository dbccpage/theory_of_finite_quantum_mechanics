"""Tests for dag/evidence/build_evidence.py.

AuthorityEffect: None. The generated evidence map and pages must be current, every
node must carry a grade, and the grades must follow the stated rules. Several checks
recompute their answer from the raw DAG and receipt files, not from the builder.

    python -m pytest dag/evidence/test_evidence.py
"""
from __future__ import annotations

import functools
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "dag"))
import build_evidence as be  # noqa: E402
import validate_derivation_dag as validator  # noqa: E402

LINK = re.compile(r"(?<!\\)\]\(([^)#\s]+)(?:#[^)]*)?\)")


@functools.lru_cache(maxsize=1)
def outputs() -> dict[str, str]:
    return be.render_all()


@functools.lru_cache(maxsize=1)
def document() -> dict:
    return json.loads(outputs()[be.MAP_REL])


@functools.lru_cache(maxsize=1)
def dag() -> dict:
    return json.loads((ROOT / be.DAG_REL).read_text(encoding="utf-8"))


def rows() -> dict[str, dict]:
    return {r["id"]: r for r in document()["nodes"]}


def flagged(node: str, kind: str) -> bool:
    return any(m["node"] == node and m["kind"] == kind for m in document()["mismatches"])


def at_least(grade: str, floor: str) -> bool:
    return be.GRADES.index(grade) >= be.GRADES.index(floor)


# ------------------------------------------------------------------ generated files

def test_generated_files_are_current():
    assert be.stale(outputs()) == [], "run python -I -X utf8 dag/evidence/build_evidence.py --write"


def test_every_node_has_a_grade_and_pages():
    nodes = dag()["nodes"]
    table = rows()
    assert len(table) == len(nodes) == document()["summary"]["nodes"]
    for node in nodes:
        row = table[node["id"]]
        assert row["grade"] in be.GRADES
        assert row["status"] == node["status"], "the map must not change a status"
        assert f"{be.DOCS_REL}/nodes/{node['id']}.md" in outputs()
        assert node["id"] in outputs()[f"{be.DOCS_REL}/stages/{node['stage']}.md"]


def test_summary_counts_add_up():
    summary = document()["summary"]
    assert sum(summary["by_grade"].values()) == summary["nodes"]
    assert sum(summary["by_status"].values()) == summary["nodes"]
    for status, grades in summary["status_by_grade"].items():
        assert sum(grades.values()) == summary["by_status"].get(status, 0)
    assert summary["mismatches_total"] == len(document()["mismatches"])


def prose_of(text: str) -> str:
    """Markdown without code spans, fenced blocks and link targets: identifiers are not prose."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    return re.sub(r"\]\([^)]*\)", "]", text)


def test_generated_pages_avoid_forbidden_words():
    for rel, text in outputs().items():
        if not rel.endswith(".md"):
            continue
        lowered = prose_of(text).lower()
        found = [w for w in validator.FORBIDDEN if re.search(r"\b" + re.escape(w) + r"\b", lowered)]
        assert found == [], f"{rel}: {found}"


def test_relative_links_resolve():
    for rel, text in outputs().items():
        if not rel.endswith(".md"):
            continue
        base = (ROOT / rel).parent
        for target in LINK.findall(text):
            if re.match(r"[a-z]+:", target):
                continue
            assert (base / target).resolve().exists() or ((base / target).as_posix() in
                                                          {(ROOT / k).as_posix() for k in outputs()}), f"{rel}: {target}"


def test_readme_links_to_the_evidence_page():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/evidence/README.md" in readme


# ------------------------------------------------------------------ grading rules

def item(**kw) -> dict:
    base = {"kind": "lean_decl", "path": "lean4/X.lean", "symbol": "X.t", "counted": True, "counts": True,
            "generated": False, "resolution": "present", "symbol_exists": True, "symbol_declared": True,
            "replay": "verified", "decl_listed": False}
    base.update(kw)
    return base


def review(qualifies: bool = True) -> dict:
    return {"qualifies": qualifies}


def test_grade_rules_on_synthetic_evidence():
    grade = lambda items, reviews=(): be.grade_node(items, list(reviews))[0]  # noqa: E731
    assert grade([]) == "E0"
    assert grade([item(resolution="external_unresolved", counts=False)]) == "E0"
    assert grade([item(kind="paper", symbol=None, counts=False, generated=True)]) == "E0"
    assert grade([item(kind="paper", symbol=None, replay="n/a")]) == "E1"
    assert grade([item(symbol=None, replay="none")]) == "E1"
    assert grade([item(symbol_exists=False, replay="none")]) == "E1"
    assert grade([item(replay="none")]) == "E2"
    assert grade([item(replay="stale")]) == "E2"
    assert grade([item(replay="failed")]) == "E2"
    assert grade([item()]) == "E3"
    assert grade([item(symbol_declared=False)]) == "E2"
    assert grade([item(symbol_declared=False, decl_listed=True)]) == "E3"
    test = item(kind="python_test", path="code/python/tests/test_x.py", symbol="test_x", replay="n/a")
    assert grade([item(), test]) == "E3"
    assert grade([item()], [review()]) == "E3"
    assert grade([item(), test], [review(False)]) == "E3"
    assert grade([item(), test], [review()]) == "E4"
    assert grade([item(replay="none"), test], [review()]) == "E2"


def test_receipt_acceptance_rules():
    base = {"exit_code": 0, "axiom_audit_passed": True, "axioms_standard": True}
    assert be.receipt_ok(base, True)
    assert not be.receipt_ok(base, False)
    assert not be.receipt_ok({**base, "exit_code": 1}, True)
    assert not be.receipt_ok({**base, "axiom_audit_passed": False}, True)
    assert not be.receipt_ok({**base, "axioms_standard": False}, True)
    # an absent audit flag is not a pass
    assert not be.receipt_ok({**base, "axiom_audit_passed": None}, True)
    assert not be.receipt_ok({"exit_code": 0, "axioms_standard": True}, True)
    assert be.parse_axiom_output("'A.b' depends on axioms: [propext,\n Quot.sound]\n'A.c' does not depend on any axioms") == {
        "A.b": ["Quot.sound", "propext"], "A.c": []}


def test_every_indexed_receipt_records_a_passed_axiom_audit_or_is_not_credited():
    builder = be.Builder()
    for receipt in builder.receipts:
        if receipt["axiom_audit_passed"] is not True:
            assert not be.receipt_ok(receipt, True), receipt["id"]


def test_declaration_names_match_in_one_direction_and_ambiguity_is_recorded():
    pair = ["ChainRetraction.TwoPoints.cls_ne_zero", "ChainRetraction.Triangle.cls_ne_zero"]
    assert be.matching_names("ChainRetraction.TwoPoints.cls_ne_zero", pair) == ["ChainRetraction.TwoPoints.cls_ne_zero"]
    assert be.matching_names("ChainRetraction.Triangle.cls_ne_zero", pair) == ["ChainRetraction.Triangle.cls_ne_zero"]
    assert be.matching_names("cls_ne_zero", pair) == sorted(pair)  # two hits: ambiguous
    assert be.matching_names("Ns.A.b", ["A.b"]) == []  # the receipt name may not be the longer-prefix fragment
    assert be.matching_names("A.b", ["Ns.A.b", "A.c"]) == ["Ns.A.b"]
    # the real receipt holds both declarations
    names = set(receipt_names("pfp_batch01_lean_replay.json"))
    assert set(pair) <= names
    builder = be.Builder()
    unique = builder.make_item("lean4/ChainRetraction.lean::ChainRetraction.TwoPoints.cls_ne_zero", "test", True)
    ambiguous = builder.make_item("lean4/ChainRetraction.lean::cls_ne_zero", "test", True)
    assert unique["decl_listed"] and not unique["decl_ambiguous"] and unique["decl_axioms"] is not None
    assert ambiguous["decl_ambiguous"] and not ambiguous["decl_listed"] and ambiguous["decl_axioms"] is None


def test_descendant_counts_are_unique_and_survive_a_cycle():
    nodes = {n: {} for n in "abcd"}
    routes = [{"inputs": ["a"], "output": "b"}, {"inputs": ["a", "b"], "output": "c"},
              {"inputs": ["b"], "output": "c"}, {"inputs": ["c"], "output": "d"}]
    assert be.descendant_counts(nodes, routes) == {"a": 3, "b": 2, "c": 1, "d": 0}
    cyclic = routes + [{"inputs": ["d"], "output": "a"}]
    assert set(be.descendant_counts(nodes, cyclic)) == set(nodes)  # no crash; validate_derivation_dag.py rejects cycles


def test_the_validator_owns_citation_parsing():
    assert validator.symbol_leaf("Ns.Mod.name") == "name"
    assert validator.symbol_leaf("x::y.z") == "z"
    assert be.split_citation("lean4/X.lean::Ns.t") == ("lean4/X.lean", "Ns.t", None)
    assert be.split_citation("papers/a.md:1-45") == ("papers/a.md", None, "1-45")
    assert be.split_citation("dag/a.md#ANCHOR-1") == ("dag/a.md", None, "ANCHOR-1")
    assert be.split_citation("external:arXiv:1503.06237") == ("external:arXiv:1503.06237", None, None)
    assert not hasattr(be, "parse_ref") and not hasattr(be, "leaf_of")


def test_the_renderer_is_pure():
    import builtins
    import pathlib
    import render_evidence as render
    statements = {n["id"]: n for n in dag()["nodes"]}
    banned = ("open", "read_text", "read_bytes")
    saved = {name: getattr(pathlib.Path, name) for name in banned[1:]}
    saved_open = builtins.open

    def refuse(*a, **k):
        raise AssertionError("the renderer must not read files")

    builtins.open = refuse
    for name in banned[1:]:
        setattr(pathlib.Path, name, refuse)
    try:
        pages = render.render_pages(document(), statements)
    finally:
        builtins.open = saved_open
        for name, fn in saved.items():
            setattr(pathlib.Path, name, fn)
    assert {k: v for k, v in outputs().items() if k != be.MAP_REL} == pages


def test_module_sizes_stay_under_the_limit():
    for name in ("build_evidence.py", "render_evidence.py"):
        assert len((HERE / name).read_text(encoding="utf-8").splitlines()) < 1000, name


# ------------------------------------------------------------------ chosen nodes, checked independently

def receipt_entries(name: str) -> list[dict]:
    data = json.loads((ROOT / "dag/research" / name).read_text(encoding="utf-8"))
    return data["lean_replay"]["results"]


def receipt_names(name: str) -> list[str]:
    names: list[str] = []
    for entry in receipt_entries(name):
        names += list(entry.get("axioms", {})) + list(entry.get("anchors", []))
    return names


def test_frontier_nodes_follow_their_receipt():
    for entry in receipt_entries("frontier_targets_lean_replay.json"):
        node = entry["dag_node"]
        current = hashlib.sha256((ROOT / entry["source"]).read_bytes()).hexdigest()
        row = rows()[node]
        if current == entry["sha256"] and entry["exit_code"] == 0 and entry["axiom_audit_passed"]:
            assert at_least(row["grade"], "E3"), node
        else:
            assert flagged(node, "receipt_not_current"), node


def test_five_qubit_perfect_tensor_is_e3_or_higher():
    row = rows()["ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET"]
    entry = next(e for e in receipt_entries("frontier_targets_lean_replay.json")
                 if e["dag_node"] == "ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET")
    assert hashlib.sha256((ROOT / entry["source"]).read_bytes()).hexdigest() == entry["sha256"]
    assert at_least(row["grade"], "E3")
    assert row["facts"]["lean_receipt_backed"] >= 4
    assert row["facts"]["qualifying_reviews"] == 1


def test_pfp_batch_nodes_are_credited_through_their_receipt():
    for entry in receipt_entries("pfp_batch01_lean_replay.json"):
        current = hashlib.sha256((ROOT / entry["source"]).read_bytes()).hexdigest()
        if current == entry["sha256"] and entry["exit_code"] == 0 and entry.get("axiom_audit_passed") is True:
            assert at_least(rows()[entry["dag_node"]]["grade"], "E3"), entry["dag_node"]


def test_node_without_in_repo_evidence_is_e0():
    row = rows()["PG-GEN-SUPPLY-NO-OP"]
    assert row["grade"] == "E0"
    assert flagged("PG-GEN-SUPPLY-NO-OP", "proved_lean_below_e3")
    assert flagged("PG-GEN-SUPPLY-NO-OP", "proved_lean_external_only")


def test_e4_needs_both_a_test_and_a_review():
    for row in rows().values():
        if row["grade"] == "E4":
            assert row["facts"]["runnable_tests"] and row["facts"]["qualifying_reviews"]
            assert row["facts"]["lean_receipt_backed"]


# ------------------------------------------------------------------ the mismatch list is complete

def test_every_proved_lean_node_below_e3_is_in_the_mismatch_list():
    below = {r["id"] for r in rows().values()
             if r["status"] == "PROVED_LEAN" and not at_least(r["grade"], "E3")}
    listed = {m["node"] for m in document()["mismatches"] if m["kind"] == "proved_lean_below_e3"}
    assert below == listed
    assert below, "the DAG currently has PROVED_LEAN nodes below E3; the list must show them"


def test_proved_lean_with_only_external_lean_is_flagged():
    root = ROOT
    expected = set()
    for node in dag()["nodes"]:
        if node["status"] != "PROVED_LEAN" or not node["lean"]:
            continue
        in_repo = [r for r in node["lean"]
                   if not r.startswith(be.EXTERNAL_PREFIXES) and (root / validator.split_ref(r)[0]).exists()]
        if not in_repo:
            expected.add(node["id"])
    listed = {m["node"] for m in document()["mismatches"] if m["kind"] == "proved_lean_external_only"}
    assert expected == listed


def test_computationally_checked_without_a_test_is_flagged():
    for row in rows().values():
        if row["status"] == "COMPUTATIONALLY_CHECKED" and not row["facts"]["runnable_tests"]:
            assert flagged(row["id"], "computational_no_runnable_test"), row["id"]
        if row["status"] == "COMPUTATIONALLY_CHECKED" and row["facts"]["runnable_tests"]:
            assert not flagged(row["id"], "computational_no_runnable_test"), row["id"]


def test_no_mismatch_without_a_node_and_page():
    ids = set(rows())
    for m in document()["mismatches"]:
        assert m["node"] in ids
        assert m["kind"] in be.MISMATCH_ORDER


def test_external_paths_are_never_called_present():
    for row in document()["nodes"]:
        for it in row["items"]:
            if it["resolution"] in ("external", "external_unresolved"):
                assert not it["file_exists"] and not it["counts"]
            if it["resolution"] == "present":
                assert (ROOT / it["path"]).exists()
