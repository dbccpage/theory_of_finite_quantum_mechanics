"""Custody and semantic-boundary checks for the source consolidation."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_added_route_is_present_and_open_questions_stay_open():
    dag = load("dag/derivation_dag.json")
    fragment = load("dag/fragments/computation_information_route.json")
    for kind in ("nodes", "routes", "records"):
        by_id = {item["id"]: item for item in dag[kind]}
        for item in fragment[kind]:
            assert by_id[item["id"]] == item
    nodes = {n["id"]: n for n in dag["nodes"]}
    for key in ("COMP-MARK-ADMISSION-GAP", "COMP-P-VS-NP-OPEN", "QC-NP-BQP-RELATION-OPEN", "QG-FULL-THEORY-COMPLETION-OPEN"):
        assert nodes[key]["status"] == "OPEN"
    assert nodes["COMP-UTM-CONDITIONAL-ROUTE"]["status"] == "CONDITIONAL"
    assert nodes["QI-MODEL-ADMISSION"]["status"] == "IMPORTED_ASSUMPTION"
    bqp_inputs = set(next(r for r in fragment["routes"] if r["output"] == "QC-UNIFORM-CIRCUITS-BQP")["inputs"])
    assert "QI-MODEL-ADMISSION" in bqp_inputs
    assert "COMP-COST-MODEL-IMPORT" in bqp_inputs
    assert "COMP-P-VS-NP-OPEN" not in bqp_inputs


def test_new_reading_spine_and_derivation_links_resolve():
    paths = [ROOT / r["f004_refs"][0] for r in load("dag/fragments/computation_information_route.json")["records"]]
    paths += [ROOT / "dag/derivations/first_mark_to_quantum_gravity.md"]
    for paper in paths:
        for ref in re.findall(r"\]\(([^\s()]+)\)", paper.read_text(encoding="utf-8")):
            if ref.startswith(("https://", "http://", "#")):
                continue
            assert (paper.parent / ref.split("#")[0]).resolve().exists(), (paper, ref)
