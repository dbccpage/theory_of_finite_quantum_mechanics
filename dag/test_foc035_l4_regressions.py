"""Regression support for fragment validation and unpublished-output boundaries."""
from __future__ import annotations
import copy
import json
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "dag"))
import sync_foc035_observer_presheaf as ops
import sync_frontier_branches as frontier
import sync_genesis_to_higher as genesis

MODULES = [ops, frontier, genesis]


def load(module):
    return json.loads((ROOT / module.FRAGMENT).read_text(encoding="utf-8"))


def errors(module, fragment):
    dag = json.loads((ROOT / "dag/derivation_dag.json").read_text(encoding="utf-8"))
    return module.validate(fragment, dag, ROOT) if module is ops else module.validate(fragment, dag)


@pytest.mark.parametrize("module", MODULES)
def test_valid_fragment_is_accepted(module):
    assert errors(module, load(module)) == []


@pytest.mark.parametrize("module", MODULES)
@pytest.mark.parametrize("fault,diagnostic", [
    ("duplicate_node", "duplicate"),
    ("unknown_status", "not allowed"),
    ("unknown_endpoint", "endpoint"),
    ("bad_record_parent", "parent"),
    ("unnamed_node", "name each other"),
])
def test_invalid_graph_is_refused(module, fault, diagnostic):
    fragment = copy.deepcopy(load(module))
    if fault == "duplicate_node":
        fragment["nodes"].append(copy.deepcopy(fragment["nodes"][0]))
    elif fault == "unknown_status":
        fragment["nodes"][0]["status"] = "FORGED"
    elif fault == "unknown_endpoint":
        fragment["routes"][0]["inputs"].append("NONEXISTENT-ENDPOINT")
    elif fault == "bad_record_parent":
        fragment["records"][0]["parent_id"] = "NONEXISTENT-RECORD"
    else:
        fragment["records"].pop()
    assert any(diagnostic in error for error in errors(module, fragment))


@pytest.mark.parametrize("fault,diagnostic", [
    ("proof_source", "PROVED_LEAN must cite"),
    ("compute_source", "COMPUTATIONALLY_CHECKED must cite"),
    ("import_premise", "needs imported_structure"),
    ("gap_source", "gap route carries no source"),
])
def test_observer_evidence_cannot_be_promoted_without_support(fault, diagnostic):
    fragment = load(ops)
    if fault == "gap_source":
        route = next(r for r in fragment["routes"] if r["status"] == "GAP_NO_DERIVATION")
        route["source"] = ["external:unsupported"]
    else:
        status = {"proof_source": "PROVED_LEAN", "compute_source": "COMPUTATIONALLY_CHECKED",
                  "import_premise": "IMPORTED_ASSUMPTION"}[fault]
        node = next(n for n in fragment["nodes"] if n["status"] == status)
        field = {"proof_source": "lean", "compute_source": "source", "import_premise": "imported_structure"}[fault]
        node[field] = []
    assert any(diagnostic in error for error in errors(ops, fragment))


def test_invalid_fragment_never_publishes(monkeypatch):
    fragment = load(ops)
    fragment["nodes"].append(copy.deepcopy(fragment["nodes"][0]))
    read = Path.read_text
    target = ROOT / ops.FRAGMENT
    def replacement(path, *args, **kwargs):
        return json.dumps(fragment) if path == target else read(path, *args, **kwargs)
    def forbidden(*args, **kwargs):
        raise AssertionError("invalid fragment attempted a write")
    monkeypatch.setattr(Path, "read_text", replacement)
    monkeypatch.setattr(Path, "write_bytes", forbidden)
    monkeypatch.setattr(Path, "write_text", forbidden)
    with pytest.raises(ValueError, match="duplicate"):
        ops.generated_files(ROOT)

