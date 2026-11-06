"""Custody and semantic-boundary checks for the source consolidation."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_every_source_has_its_declared_surviving_bytes():
    manifest = load("dag/derivations/source_consolidation_manifest.json")
    destinations = set()
    for row in manifest["files"]:
        target = (ROOT / row["destination"]).resolve()
        assert target.is_relative_to(ROOT)
        assert target not in destinations
        destinations.add(target)
        assert target.is_file(), row
        assert hashlib.sha256(target.read_bytes()).hexdigest() == row.get("edited_sha256", row["sha256"])
    for old in manifest["retired_directories"]:
        assert not (ROOT / old).exists()


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
    paths += [ROOT / "dag/derivations/FIRST_MARK_TO_QUANTUM_GRAVITY.md", ROOT / "dag/derivations/SOURCE_CROSSWALK.md"]
    for paper in paths:
        for ref in re.findall(r"\]\(([^\s()]+)\)", paper.read_text(encoding="utf-8")):
            if ref.startswith(("https://", "http://", "#")):
                continue
            assert (paper.parent / ref.split("#")[0]).resolve().exists(), (paper, ref)
