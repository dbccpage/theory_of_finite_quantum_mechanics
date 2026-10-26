"""Origin: dag/test_validate_derivation_dag.py
Claim: derivation DAG checks reject cycles, bad vocabulary, forbidden words, malformed or unlinked TFQ records and stale views, and the packaged graph reports zero failures
AuthorityEffect: None
Scope Fence: this file does not claim that a recorded statement is true
Level: L5
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate_derivation_dag as dag


def _node(node_id: str, stage: str = "DEFINITION", status: str = "DEFINITION") -> dict[str, object]:
    return {
        "id": node_id,
        "stage": stage,
        "status": status,
        "source_status": "recorded",
        "statement": "a finite record",
        "source": ["dag/derivation_dag.json"],
        "lean": [],
        "rust": [],
        "imported_structure": [],
        "bottleneck": "none",
        "tags": [],
        "see_also": [],
    }


def _route(route_id: str, output: str, inputs: list[str]) -> dict[str, object]:
    return {
        "id": route_id,
        "status": "DERIVED_PROSE",
        "output": output,
        "inputs": inputs,
        "source": ["dag/derivation_dag.json"],
    }


def test_exact_integer_and_ratio_guards() -> None:
    with pytest.raises(dag.DagContractError):
        dag.exact_int(True)
    with pytest.raises(dag.DagContractError):
        dag.big_rational(1, 0)
    assert dag.acyclic_ratio(2, 2) == dag.big_rational(1, 1)
    assert dag.verify_acyclic_ratio(1, 2).holds is False


def _graph(nodes: list[dict[str, object]], routes: list[dict[str, object]]) -> dict[str, object]:
    payload: dict[str, object] = {}
    payload["nodes"] = nodes
    payload["routes"] = routes
    return payload


def test_cycle_is_reported_and_chain_is_not() -> None:
    nodes = [_node("a", "PREGENESIS", "ADMITTED_PRIMITIVE"), _node("b", "GENESIS")]
    nodes[0]["source"] = []
    chain = _graph(nodes, [_route("r", "b", ["a"])])
    assert dag.check(chain, None) == []
    cyc = _graph(nodes, [_route("r1", "b", ["a"]), _route("r2", "a", ["b"])])
    assert any("cycle among nodes" in err for err in dag.check(cyc, None))


def test_negative_vocabulary_and_duplicate() -> None:
    bad = _node("a", stage="NOPE")
    errs = dag.check(_graph([bad, bad], []), None)
    assert any("bad stage" in err for err in errs)
    assert any("duplicate node id" in err for err in errs)
    route = _route("r", "missing", [])
    route_errs = dag.check(_graph([_node("a", "PREGENESIS", "ADMITTED_PRIMITIVE")], [route]), None)
    assert any("no inputs" in err for err in route_errs)
    hype = _node("a", status="ADMITTED_PRIMITIVE")
    hype["statement"] = "this is impossible"
    hype["source"] = []
    assert any("forbidden word" in err for err in dag.check(_graph([hype], []), None))


def test_file_reference_integration(tmp_path: Path) -> None:
    cited = tmp_path / "note.txt"
    cited.write_text("symbol_leaf\n", encoding="utf-8")
    node = _node("a", status="PROVED_LEAN")
    node["lean"] = ["note.txt::symbol_leaf"]
    node["source"] = ["note.txt"]
    missing = dag.check(_graph([node], [_route("r", "a", ["a"])]), tmp_path)
    assert any("output among its inputs" in err for err in missing)
    node["lean"] = ["note.txt::absent_symbol"]
    errs = dag.check(_graph([node], [_route("r", "a", ["z"])]), tmp_path)
    assert any("symbol" in err for err in errs)
    assert any("unknown input" in err for err in errs)


def _review(**changes: object) -> dict[str, object]:
    review: dict[str, object] = {
        "review": "dag/results/N/reviews/r/review_result.json",
        "review_sha256": "0" * 64,
        "review_refs": ["dag/results/N/reviews/r/review_result.json"],
        "verdict": "scoped_result_or_obstruction_reviewed",
        "narrowest_claim": "a finite witness",
        "does_not_support": "the general statement",
        "next_test": "prove the general statement",
        "scope_effect": "consistent",
        "reason": "stated within the witness",
        "prior_status": "DEFINITION",
        "prior_statement": "a finite record",
        "prior_bottleneck": "none",
        "superseded_by": [],
    }
    review.update(changes)
    return review


def _reviewed(**changes: object) -> dict[str, object]:
    node = _node("a", "PREGENESIS", "DEFINITION")
    node["pfp_review"] = _review(**changes)
    return node


def test_pfp_review_shape_is_checked() -> None:
    assert dag.check(_graph([_reviewed()], []), None) == []
    missing = _reviewed()
    del missing["pfp_review"]["next_test"]  # type: ignore[arg-type]
    assert any("is missing ['next_test']" in err for err in dag.check(_graph([missing], []), None))
    extra = _reviewed(unexpected="x")
    assert any("unknown keys ['unexpected']" in err for err in dag.check(_graph([extra], []), None))
    assert any("not a sha256" in err for err in dag.check(_graph([_reviewed(review_sha256="abc")], []), None))
    bad_refs = _reviewed(review_refs=["elsewhere.json"])
    assert any("must end with the review path" in err for err in dag.check(_graph([bad_refs], []), None))
    bad_effect = _reviewed(scope_effect="promoted")
    assert any("not in the vocabulary" in err for err in dag.check(_graph([bad_effect], []), None))
    not_object = _node("a")
    not_object["pfp_review"] = "text"
    assert any("must be an object" in err for err in dag.check(_graph([not_object], []), None))


def test_pfp_review_never_raises_a_status() -> None:
    raised = _node("a", status="DEFINITION")
    raised["pfp_review"] = _review(prior_status="OPEN", scope_effect="status_lowered")
    errs = dag.check(_graph([raised], []), None)
    assert any("is above pfp_review.prior_status OPEN" in err for err in errs)
    unmarked = _reviewed(prior_status="PROVED_LEAN", scope_effect="consistent")
    assert any("exactly when the status changed" in err for err in dag.check(_graph([unmarked], []), None))
    lowered = _reviewed(prior_status="PROVED_LEAN", scope_effect="status_lowered")
    assert not any("pfp_review" in err for err in dag.check(_graph([lowered], []), None))
    same = _reviewed(scope_effect="statement_narrowed")
    assert any("statement is the prior statement" in err for err in dag.check(_graph([same], []), None))


def test_open_node_keeps_its_target_statement() -> None:
    target = _node("a", "PREGENESIS", "OPEN")
    target["statement"] = "Continuous time is not constructed."
    assert not any("narrowed" in err for err in dag.check(_graph([target], []), None))
    for prefix in ("Narrowed boundary, status left OPEN. 3 * 3 + 4 * 4 = 5 * 5.", "Reviewed scope: 48 - 24 = 24."):
        slice_node = _node("a", "PREGENESIS", "OPEN")
        slice_node["statement"] = prefix
        assert any("narrowed slice, not the target" in err for err in dag.check(_graph([slice_node], []), None))
    narrowed = _node("a", "PREGENESIS", "CONDITIONAL")
    narrowed["pfp_review"] = _review(prior_status="CONDITIONAL", scope_effect="statement_narrowed",
                                     prior_statement="the target")
    assert any("keep the target statement" in err for err in dag.check(_graph([narrowed], []), None))
    proved = _reviewed(scope_effect="statement_narrowed", prior_statement="the target")
    assert not any("keep the target statement" in err for err in dag.check(_graph([proved], []), None))


def test_pfp_review_file_and_sha256_are_checked(tmp_path: Path) -> None:
    review_file = tmp_path / "dag" / "results" / "N" / "reviews" / "r" / "review_result.json"
    review_file.parent.mkdir(parents=True)
    review_file.write_bytes(b'{"status": "ok"}\r\n')
    digest = dag.pfp_review_sha256(b'{"status": "ok"}\n')
    assert dag.pfp_review_sha256(review_file.read_bytes()) == digest
    node = _reviewed(review_sha256=digest)
    node["source"] = ["dag/results/N/reviews/r/review_result.json"]
    assert dag.check(_graph([node], []), tmp_path) == []
    wrong = _reviewed()
    wrong["source"] = ["dag/results/N/reviews/r/review_result.json"]
    assert any("does not match" in err for err in dag.check(_graph([wrong], []), tmp_path))
    gone = _reviewed(review="dag/results/N/reviews/r/gone.json", review_refs=["dag/results/N/reviews/r/gone.json"])
    gone["source"] = ["dag/results/N/reviews/r/review_result.json"]
    assert any("file missing" in err for err in dag.check(_graph([gone], []), tmp_path))


def _record(rid: str, parent: str | None, names: list[str], stage: str = "PREGENESIS") -> dict[str, object]:
    return {
        "coda_atlas_ids": [],
        "coda_atlas_paths": [],
        "existing_derivation_dag_ids": names,
        "f004_refs": [],
        "id": rid,
        "lean4": [],
        "local_id": rid,
        "name": "step " + rid,
        "obligation": "keep the step finite",
        "parent_id": parent,
        "python": [],
        "record_status": "SOURCE_RECORD",
        "rust": [],
        "source_slice": "00",
        "stage": stage,
        "summary": "a finite step",
        "uuid": "00000000-0000-0000-0000-000000000000",
    }


def _v2(records: list[dict[str, object]] | None = None) -> dict[str, object]:
    nodes = [_node("a", "PREGENESIS", "ADMITTED_PRIMITIVE"), _node("b", "PREGENESIS")]
    nodes[0]["source"] = []
    return {
        "schema_version": dag.SCHEMA_VERSION,
        "stages": ["PREGENESIS"],
        "index_document": {
            "header_markdown": "# Tree\n\n",
            "record_count_note": "No atlas paths dropped.",
            "stage_index": ["PREGENESIS"],
            "application_stages": [],
            "coda_atlas_packages": {"heading": "Packages", "rows": [{"floor": "F0", "shelf": "S0", "package": "p", "path": "x/p"}]},
            "source_corpus_restatements": [],
        },
        "nodes": nodes,
        "routes": [_route("r", "b", ["a"])],
        "records": records if records is not None else [_record("TFQ-0000", None, ["a"]), _record("TFQ-0001", "TFQ-0000", ["b", "R-b"])],
    }


def _write_views(graph: dict[str, object], folder: Path) -> None:
    for path, data in dag.render_dag_views.views(graph, folder.parent).items():
        (folder / path.name).write_bytes(data)


def test_v2_records_and_views_pass(tmp_path: Path) -> None:
    graph = _v2()
    _write_views(graph, tmp_path)
    assert dag.check(graph, None, tmp_path) == []
    jsonl = (tmp_path / "theory_of_finite_qm.jsonl").read_bytes()
    assert jsonl.count(b"\r\n") == 2 and b'"id": "TFQ-0001"' in jsonl
    md = (tmp_path / "theory_of_finite_qm.md").read_text(encoding="utf-8")
    assert "Nodes: 2. No atlas paths dropped." in md and "| `PREGENESIS` | 2 |" in md


def test_v2_top_level_keys_are_checked() -> None:
    old = {**_v2(), "schema_version": "derivation_dag.v1"}
    assert any("is not derivation_dag.v2" in err for err in dag.check(old, None))
    missing = _v2()
    del missing["index_document"]
    assert any("missing top-level keys ['index_document']" in err for err in dag.check(missing, None))
    extra = {**_v2(), "notes": []}
    assert any("unknown top-level keys ['notes']" in err for err in dag.check(extra, None))
    bad_doc = _v2()
    bad_doc["index_document"]["stage_index"] = ["NOPE"]  # type: ignore[index]
    assert any("unknown stage NOPE" in err for err in dag.check(bad_doc, None))


def test_v2_records_are_checked() -> None:
    dup = _v2([_record("TFQ-0000", None, ["a"]), _record("TFQ-0000", None, ["b"])])
    assert any("duplicate record id TFQ-0000" in err for err in dag.check(dup, None))
    orphan = _v2([_record("TFQ-0000", None, ["a"]), _record("TFQ-0001", "TFQ-0009", ["b"])])
    assert any("parent_id TFQ-0009 is not another record" in err for err in dag.check(orphan, None))
    cycle = _v2([_record("TFQ-0000", None, ["a"]), _record("TFQ-0001", "TFQ-0002", ["b"]), _record("TFQ-0002", "TFQ-0001", ["b"])])
    assert any("parent_id chain is a cycle" in err for err in dag.check(cycle, None))
    nameless = _v2([_record("TFQ-0000", None, ["a"]), _record("TFQ-0001", "TFQ-0000", ["b"]), _record("TFQ-0002", "TFQ-0000", ["R-b"])])
    assert any("record TFQ-0002: names no DAG node" in err for err in dag.check(nameless, None))
    unnamed = _v2([_record("TFQ-0000", None, ["a"])])
    assert any("node b: named by no record" in err for err in dag.check(unnamed, None))
    shape = _record("TFQ-01", "TFQ-0000", ["b"])
    shape["extra"] = 1
    shape["lean4"] = "x.lean"
    errs = dag.check(_v2([_record("TFQ-0000", None, ["a"]), shape]), None)
    assert any("id is not TFQ-NNNN" in err for err in errs)
    assert any("unknown keys ['extra']" in err for err in errs)
    assert any("field lean4 must be a list of strings" in err for err in errs)


def test_v2_views_and_papers_are_checked(tmp_path: Path) -> None:
    graph = _v2()
    _write_views(graph, tmp_path)
    (tmp_path / "theory_of_finite_qm.md").write_text("hand edit\n", encoding="utf-8")
    assert any("view theory_of_finite_qm.md differs" in err for err in dag.check(graph, None, tmp_path))
    (tmp_path / "theory_of_finite_qm.jsonl").unlink()
    assert any("view theory_of_finite_qm.jsonl differs" in err for err in dag.check(graph, None, tmp_path))
    root = tmp_path / "repo"
    papers = root / "dag" / "derivations" / "01_pregenesis"
    papers.mkdir(parents=True)
    (root / "dag" / "derivation_dag.json").write_text("{}", encoding="utf-8")
    (papers / "tfq_0000_root.md").write_text("# root\n", encoding="utf-8")
    errs = dag.check(graph, root)
    assert any("record TFQ-0001: no derivation paper" in err for err in errs)
    assert not any("record TFQ-0000: no derivation paper" in err for err in errs)


def test_packaged_graph_end_to_end() -> None:
    root = HERE.parent
    result = subprocess.run(
        [sys.executable, str(HERE / "validate_derivation_dag.py"), "--no-files"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "failures=0" in result.stdout
    assert f"nodes={len(dag._load_dag(HERE / 'derivation_dag.json')['nodes'])}" in result.stdout


def _load(text: str, name: str) -> object:
    path = HERE / f"_mutant_{name}.py"
    path.write_text(text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    path.unlink()
    return module


def test_mutation_kills_are_recorded() -> None:
    source = (HERE / "validate_derivation_dag.py").read_text(encoding="utf-8")
    mutants = {
        "cycle": ("verify_acyclic_ratio(seen, len(ids)).holds", "True"),
        "stage": (
            'if _text(node, "stage") not in STAGES:',
            'if False and _text(node, "stage") not in STAGES:',
        ),
        "word": (
            'if re.search(r"\\b" + re.escape(word) + r"\\b", blob):',
            'if False and re.search(r"\\b" + re.escape(word) + r"\\b", blob):',
        ),
        "pfp": (
            "if PFP_STATUS_RANK[status] > PFP_STATUS_RANK[prior]:",
            "if False and PFP_STATUS_RANK[status] > PFP_STATUS_RANK[prior]:",
        ),
        "record_dup": ("if rid in seen_records:", "if False and rid in seen_records:"),
        "record_parent": (
            "if pid is not None and (pid not in seen_records or pid == rid):",
            "if False and pid is not None and (pid not in seen_records or pid == rid):",
        ),
        "record_node": ("if not any(x in ids for x in dag_ids):", "if False and not any(x in ids for x in dag_ids):"),
        "node_named": ("if node_id not in named:", "if False and node_id not in named:"),
        "views": (
            'if not path.is_file() or path.read_bytes() != text.encode("utf-8"):',
            'if False and (not path.is_file() or path.read_bytes() != text.encode("utf-8")):',
        ),
        "paper": ('for r in records if _text(r, "id") not in papers]', "for r in records if False]"),
    }
    killed = 0
    for name, (old, new) in mutants.items():
        if source.count(old) != 1:
            raise AssertionError(name)
        module = _load(source.replace(old, new, 1), f"dag_mut_{name}")
        if not _killed(module, name):
            raise AssertionError(name)
        killed += 1
    assert killed == 10
    assert "MutationKillCount: 10" in source


def _killed_v2(module: object, name: str) -> bool:
    """A v2 mutant is killed when the check it disables no longer reports the defect."""
    import tempfile

    check = getattr(module, "check")
    if name == "record_dup":
        graph = _v2([_record("TFQ-0000", None, ["a"]), _record("TFQ-0000", None, ["b"])])
        return not any("duplicate record id" in err for err in check(graph, None))
    if name == "record_parent":
        graph = _v2([_record("TFQ-0000", None, ["a"]), _record("TFQ-0001", "TFQ-0009", ["b"])])
        return not any("is not another record" in err for err in check(graph, None))
    if name == "record_node":
        graph = _v2([_record("TFQ-0000", None, ["a"]), _record("TFQ-0001", "TFQ-0000", ["b"]), _record("TFQ-0002", "TFQ-0000", ["x"])])
        return not any("names no DAG node" in err for err in check(graph, None))
    if name == "node_named":
        return not any("named by no record" in err for err in check(_v2([_record("TFQ-0000", None, ["a"])]), None))
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        graph = _v2()
        if name == "views":
            _write_views(graph, root)
            (root / "theory_of_finite_qm.md").write_text("hand edit\n", encoding="utf-8")
            return not any("differs" in err for err in check(graph, None, root))
        (root / "dag" / "derivations").mkdir(parents=True)
        (root / "dag" / "derivation_dag.json").write_text("{}", encoding="utf-8")
        return not any("no derivation paper" in err for err in check(graph, root))


def _killed(module: object, name: str) -> bool:
    check = getattr(module, "check")
    if name in ("record_dup", "record_parent", "record_node", "node_named", "views", "paper"):
        return _killed_v2(module, name)
    if name == "cycle":
        nodes = [_node("a", "PREGENESIS", "ADMITTED_PRIMITIVE"), _node("b", "GENESIS")]
        nodes[0]["source"] = []
        errs = check({"nodes": nodes, "routes": [_route("r1", "b", ["a"]), _route("r2", "a", ["b"])]}, None)
        return not any("cycle among nodes" in err for err in errs)
    if name == "stage":
        errs = check({"nodes": [_node("a", stage="NOPE")], "routes": []}, None)
        return not any("bad stage" in err for err in errs)
    if name == "pfp":
        raised = _node("a", status="DEFINITION")
        raised["pfp_review"] = _review(prior_status="OPEN", scope_effect="status_lowered")
        errs = check({"nodes": [raised], "routes": []}, None)
        return not any("is above pfp_review.prior_status" in err for err in errs)
    errs = check({"nodes": [_node("a", status="OPEN", stage="OPEN")], "routes": []}, None)
    text_errs = check(
        {"nodes": [{**_node("a", status="ADMITTED_PRIMITIVE"), "statement": "impossible", "source": []}], "routes": []},
        None,
    )
    return not any("forbidden word" in err for err in text_errs) and isinstance(errs, list)
