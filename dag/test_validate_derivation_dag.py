"""Origin: dag/test_validate_derivation_dag.py
Claim: derivation DAG checks reject cycles, bad vocabulary, and forbidden words, and the packaged graph reports zero failures
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
    }
    killed = 0
    for name, (old, new) in mutants.items():
        if source.count(old) != 1:
            raise AssertionError(name)
        module = _load(source.replace(old, new, 1), f"dag_mut_{name}")
        if not _killed(module, name):
            raise AssertionError(name)
        killed += 1
    assert killed == 4
    assert "MutationKillCount: 4" in source


def _killed(module: object, name: str) -> bool:
    check = getattr(module, "check")
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
