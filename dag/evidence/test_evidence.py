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
    assert be.receipt_results({"lean_replay": {"results": []}}) == ({"results": []}, [], None)
    assert be.receipt_results({"results": [], "lean_version": "4.35.0"})[1] is None
    assert be.receipt_results({"checks": "Lean ran"})[2] == "records Lean checks without per-module sha256"
    failed = {"lean_version": "4.35.0", "results": [{"exit_code": 1}]}
    assert "nonzero code" in be.receipt_results(failed)[2]


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


def test_scratch_commands_use_the_unique_current_receipt_namespace():
    builder = be.Builder()
    prefix = "lean4/CampaignAuthfCarrierAdmissionGate.lean::"
    bare = builder.make_item(prefix + "directCeilings", "test", True)
    qualified = builder.make_item(prefix + "CampaignAuthfCarrierAdmissionGate.directCeilings", "test", True)
    assert bare["canonical_symbol"] == qualified["canonical_symbol"] == "CampaignAuthfCarrierAdmissionGate.directCeilings"
    assert bare["command_note"] == qualified["command_note"]
    assert "#print axioms CampaignAuthfCarrierAdmissionGate.directCeilings" in bare["command_note"]
    ambiguous = builder.make_item("lean4/ChainRetraction.lean::cls_ne_zero", "test", True)
    assert ambiguous["canonical_symbol"] is None


def test_receipt_aliases_count_once_without_removing_audit_rows_or_changing_grade():
    rows = [item(symbol=s, canonical_symbol="Ns.t", cited_in=["node.lean"], decl_axioms=[], decl_ambiguous=False)
            for s in ("t", "Ns.t")]
    grade, facts = be.grade_node(rows, [])
    assert grade == "E3" and facts["lean_receipt_backed"] == 1
    assert facts["symbols_found"] == len(rows) == 2
    summary = be.lean_summary([{"items": rows, "status": "OPEN"}])
    assert summary["lean_declarations_in_repo"]["distinct"] == 1
    assert summary["lean_references_cited_in_node_lean_fields"] == {"present": 2}
    different = item(symbol="Other.t", canonical_symbol="Other.t", cited_in=["node.lean"])
    assert be.grade_node(rows + [different], [])[1]["lean_receipt_backed"] == 2


def test_indexed_replay_receipts_have_top_level_digest_custody():
    doc = document()
    for receipt in doc["receipts"]:
        path = receipt["receipt_file"]
        data = (ROOT / path).read_bytes()
        info = doc["files"][path]
        assert info["size"] == len(data)
        assert info["sha256"] == hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


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


def test_build_commands_use_unique_scoped_config_and_preserve_default_and_fallback():
    """Scoped roots need a selected Lake file; unknown or ambiguous roots do not."""
    builder = be.Builder.__new__(be.Builder)
    builder.roots = {"Default"}
    builder.scoped_configs = {"Default": ["lakefile.other.lean"],
                              "Scoped": ["lakefile.scoped.lean"],
                              "Ambiguous": ["lakefile.a.lean", "lakefile.b.lean"]}
    for module, expected in {
        "Default": "cd lean4 && lake build Default",
        "Scoped": "cd lean4 && lake --file=lakefile.scoped.lean build Scoped",
        "Ambiguous": "cd lean4 && lake build   # the library that contains lean4/Ambiguous.lean",
        "Unknown": "cd lean4 && lake build   # the library that contains lean4/Unknown.lean",
    }.items():
        command, note = builder._command(item(path=f"lean4/{module}.lean", symbol=f"{module}.t"))
        assert command == expected
        assert note == f"then, in a scratch file that imports {module}: #print axioms {module}.t"


def test_scoped_root_discovery_ignores_comments_and_unsafe_config_names(tmp_path, monkeypatch):
    """Only literal roots in a simple local Lake filename become commands."""
    monkeypatch.setattr(be, "ROOT", tmp_path)
    (tmp_path / "lean4").mkdir()
    (tmp_path / "lean4/lakefile.safe.lean").write_text(
        "-- roots := #[`Ignored]\nlean_lib Safe where\n  roots := #[`Scoped]\n", encoding="utf-8")
    (tmp_path / "lean4/lakefile.unsafe&name.lean").write_text(
        "roots := #[`Unsafe]\n", encoding="utf-8")
    monkeypatch.setattr(be, "load_json", lambda _: {"nodes": [], "records": []})
    builder = be.Builder()
    assert dict(builder.scoped_configs) == {"Scoped": ["lakefile.safe.lean"]}


def test_majorana_citations_are_qualified_unique_and_reproduce_the_scoped_build():
    """TFQ-1186 must not double-count bare aliases of the audited declarations."""
    row = rows()["FSP-MAJORANA-CLIFFORD-PARITY"]
    entries = [i for i in row["items"] if i["path"] == "lean4/CampaignMajoranaCliffordParity.lean"
               and i["symbol"] is not None]
    names = receipt_names("campaign_fsp-majorana-clifford-parity_lean_replay.json")
    assert len(entries) == len(set(names)) == 32
    assert {i["symbol"] for i in entries} == set(names)
    assert {i["command"] for i in entries} == {
        "cd lean4 && lake --file=lakefile.campaignMajorana.lean build CampaignMajoranaCliffordParity"}


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


def test_pgw_campaign_receipt_without_a_lean_replay_object_is_indexed():
    """The PGW campaign file itemises axioms at the top level. Indexing it does not change the node status."""
    rel = "dag/research/campaign_pgw-presentation-not-expressive-lift_lean_replay.json"
    data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    assert "lean_replay" not in data
    receipts = [r for r in document()["receipts"] if r["receipt_file"] == rel]
    assert len(receipts) == 1
    assert receipts[0]["module"] == "CampaignPgwPresentationLift"
    assert receipts[0]["dag_node"] == "PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT"
    assert receipts[0]["exit_code"] == 0
    assert receipts[0]["lean_version"]
    row = rows()["PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT"]
    assert row["status"] == "CONDITIONAL"
    current = hashlib.sha256((ROOT / "lean4/CampaignPgwPresentationLift.lean").read_bytes()).hexdigest()
    assert current == data["sha256"]
    assert at_least(row["grade"], "E3")
    skipped = {item["file"] for item in document()["receipts_not_indexed"]}
    assert "dag/research/tensor_countermodel_failed_replay.json" in skipped


def test_pfp_batch_nodes_are_credited_through_their_receipt():
    for entry in receipt_entries("pfp_batch01_lean_replay.json"):
        current = hashlib.sha256((ROOT / entry["source"]).read_bytes()).hexdigest()
        if current == entry["sha256"] and entry["exit_code"] == 0 and entry.get("axiom_audit_passed") is True:
            assert at_least(rows()[entry["dag_node"]]["grade"], "E3"), entry["dag_node"]


def test_node_without_in_repo_evidence_is_e0():
    # PG-GEN-SUPPLY-NO-OP was the live example until its Lean files were imported into lean4/Imported, so the
    # rule is tested on synthetic nodes; the live DAG is covered by the two completeness tests below.
    node = {"id": "SYNTH-EXTERNAL", "status": "PROVED_LEAN"}
    external = item(resolution="external_unresolved", counts=False, counted=False, cited_in=["node.lean"])
    grade, facts = be.grade_node([external], [])
    assert grade == "E0"
    kinds = {f["kind"] for f in be.node_flags(node, [external], grade, facts)}
    assert {"proved_lean_below_e3", "proved_lean_external_only"} <= kinds


def test_proved_lean_with_a_present_but_unreplayed_file_is_below_e3_but_not_external():
    node = {"id": "SYNTH-UNREPLAYED", "status": "PROVED_LEAN"}
    unreplayed = item(replay="none", cited_in=["node.lean"])
    grade, facts = be.grade_node([unreplayed], [])
    assert grade == "E2"
    kinds = {f["kind"] for f in be.node_flags(node, [unreplayed], grade, facts)}
    assert "proved_lean_below_e3" in kinds and "proved_lean_external_only" not in kinds


def test_proved_lean_with_a_verified_present_file_raises_neither_flag():
    node = {"id": "SYNTH-VERIFIED", "status": "PROVED_LEAN"}
    good = item(cited_in=["node.lean"])
    grade, facts = be.grade_node([good], [])
    assert grade == "E3"
    kinds = {f["kind"] for f in be.node_flags(node, [good], grade, facts)}
    assert "proved_lean_below_e3" not in kinds and "proved_lean_external_only" not in kinds


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
    # non-vacuous: the summary count agrees with the list, whatever its size
    assert document()["summary"]["mismatches_by_kind"].get("proved_lean_below_e3", 0) == len(below)


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


def test_uncited_module_flag_compares_files_not_declarations():
    node = {"status": "CONDITIONAL"}
    facts = {"runnable_tests": 0}

    def uncited(items: list[dict]) -> list[str]:
        return [f["detail"] for f in be.node_flags(node, items, "E3", facts)
                if f["kind"] == "receipt_names_uncited_module"]

    cited = item(path="lean4/A.lean", symbol="A.cited", cited_in=["node.lean", "receipt r.json (A)"])
    anchor_only = item(path="lean4/A.lean", symbol="A.anchor", cited_in=["receipt r.json (A)"])
    other_file = item(path="lean4/B.lean", symbol="B.anchor", cited_in=["receipt r.json (B)"])
    # a receipt anchor in a file where the node cites another declaration is not a citation gap
    assert uncited([cited, anchor_only]) == []
    # a file the receipt names and no node field cites at all is a gap, reported once per file
    gaps = uncited([cited, anchor_only, other_file, item(path="lean4/B.lean", symbol="B.two",
                                                       cited_in=["receipt r.json (B)"])])
    assert len(gaps) == 1 and "lean4/B.lean" in gaps[0]
    # a node-only citation is never a gap
    assert uncited([item(path="lean4/C.lean", cited_in=["node.lean"])]) == []


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


def test_all_replay_states_are_reported_in_the_evidence_summary():
    import copy
    import render_evidence as render

    doc = copy.deepcopy(document())
    counts = doc["summary"]["lean_declarations_in_repo"]
    assert counts["distinct"] == sum(counts[k] for k in
        ("replay_verified", "replay_stale", "replay_failed", "no_receipt"))
    # Exercise the failure bucket even when a checkout has no failed receipt.
    counts["replay_failed"] = 7
    text = render.readme_page(doc, doc["nodes"])
    assert "7 are in files whose current-hash receipt failed the build or axiom audit" in text


def test_generated_symbol_tables_have_a_blank_line_before_the_grade_list():
    for rel, text in outputs().items():
        if rel.endswith(".md"):
            assert not re.search(r"^\|.*\|\n- counts toward the grade:", text, re.M), rel
