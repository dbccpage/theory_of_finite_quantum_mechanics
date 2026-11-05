"""Regression controls for witness admission and source-bound Lean evidence."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("projection_replay", ROOT / "tools/replay_projection_bounds.py")
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


def test_census_covers_all_twenty_named_theorems():
    assert len(replay.expected_names(ROOT)) == 20


def test_multiline_axiom_report():
    text = "'ProjectionBounds.example' depends on axioms: [propext,\n Classical.choice, Quot.sound]\n"
    assert replay.parse_axioms(text, ["ProjectionBounds.example"]) == {
        "ProjectionBounds.example": ["Classical.choice", "Quot.sound", "propext"]}


@pytest.mark.parametrize("text", [
    "", "'ProjectionBounds.example' depends on axioms: [sorryAx]\n",
    "'ProjectionBounds.example' depends on axioms: [propext,\n",
    "'ProjectionBounds.wrong' does not depend on any axioms\n",
    "'ProjectionBounds.example' does not depend on any axioms\n" * 2,
])
def test_census_refuses_missing_wrong_truncated_and_duplicate_reports(text):
    with pytest.raises(ValueError):
        replay.parse_axioms(text, ["ProjectionBounds.example"])


@pytest.mark.parametrize("optimized", [False, True])
@pytest.mark.parametrize("mutation", ["none", "wrong_verdict", "integer_verdict", "float_duration", "negative", "extra_input"])
def test_witness_refusals_survive_optimization(tmp_path, optimized, mutation):
    folder = tmp_path / "docs/residual_error_budget"
    shutil.copytree(ROOT / "docs/residual_error_budget", folder)
    (tmp_path / "code").mkdir()
    shutil.copyfile(ROOT / "code/residual_error_budget.py", tmp_path / "code/residual_error_budget.py")
    path = folder / "witness_near_miss.json"
    witness = json.loads(path.read_text())
    if mutation == "wrong_verdict":
        witness["expected_within_budget"] = True
    elif mutation == "integer_verdict":
        witness["expected_within_budget"] = 0
    elif mutation == "float_duration":
        witness["duration"] = 0.5
    elif mutation == "negative":
        witness["duration"] = "-1"
    elif mutation == "extra_input":
        with (folder / "input.yaml").open("a") as stream:
            stream.write('\nundeclared: "1"\n')
    path.write_text(json.dumps(witness), encoding="utf-8")
    command = [sys.executable, "-I", "-B"] + (["-O"] if optimized else []) + [str(folder / "checker.py")]
    result = subprocess.run(command, capture_output=True, text=True, timeout=20)
    assert (result.returncode == 0) == (mutation == "none"), result.stdout + result.stderr


@pytest.mark.parametrize("target", ["source", "report", "pin", "count", "flag"])
def test_recorded_evidence_refuses_drift(tmp_path, target):
    for name in [*replay.SOURCES, "lean4/projection_axiom_report.txt", "lean4/projection_axiom_census.json"]:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, path)
    if target in {"source", "report", "pin"}:
        name = {"source": replay.SOURCES[0], "report": "lean4/projection_axiom_report.txt", "pin": replay.SOURCES[2]}[target]
        with (tmp_path / name).open("a", encoding="utf-8") as stream:
            stream.write("\n")
    else:
        path = tmp_path / "lean4/projection_axiom_census.json"
        data = json.loads(path.read_text())
        data["count" if target == "count" else "fresh_compilation"] = 1
        path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError):
        replay.verify_receipt(tmp_path)


def test_stored_census_binds_current_sources():
    assert replay.verify_receipt(ROOT)["count"] == 20


def test_fresh_replay_requires_prepared_cache():
    result = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "tools/replay_projection_bounds.py"),
                             "--mathlib", str(ROOT / "nonexistent-mathlib")],
                            capture_output=True, text=True, timeout=20)
    assert result.returncode == 1
    assert "prepare clean dependency" in result.stdout
