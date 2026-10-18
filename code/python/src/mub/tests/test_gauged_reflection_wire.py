"""Refuse malformed or unbound candidate-box reflection inputs."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

def _find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists() or (candidate / "pyproject.toml").exists():
            return candidate
    return start.parents[5]


ROOT = _find_repo_root(Path(__file__).resolve())
MUB6_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS = MUB6_DIR / "artifacts"
SCRIPT = MUB6_DIR / "scripts/reflect_szollosi_gauged.py"
NAMES = {
    "inspection": "mub_szollosi_gauged_native_inspection.json",
    "exclusion": "mub_szollosi_balance_exclusion_receipt.json",
    "coefficients": "mub_szollosi_gauged_lean_coefficients.json",
    "root-receipt": "mub_szollosi_gauged_root_receipt.json",
    "system": "mub_szollosi_gauged_executable_system.json",
    "request": "mub_szollosi_balance_exclusion_request.json",
}


def inputs(tmp_path):
    files = {key: tmp_path / name for key, name in NAMES.items()}
    for key, path in files.items():
        path.write_bytes((ARTIFACTS / NAMES[key]).read_bytes())
    return files


def run_formatter(files, output):
    args = [sys.executable, str(SCRIPT)]
    for key, path in files.items():
        args.extend(["--" + key, str(path)])
    return subprocess.run(
        args + ["--output", str(output)], cwd=ROOT, capture_output=True, text=True, check=False
    )


def test_formatter_reproduces_checked_candidate_box_source(tmp_path):
    files = inputs(tmp_path)
    output = tmp_path / "reflected.lean"
    result = run_formatter(files, output)
    assert result.returncode == 0, result.stderr
    assert (
        output.read_bytes()
        == (ROOT / "lean4/research_programs/mub6/SzollosiGaugedReflection.lean").read_bytes()
    )


@pytest.mark.parametrize(
    "case",
    [
        "boolean_dimension",
        "noncanonical_rational",
        "changed_coefficient",
        "missing_bound",
        "changed_candidate_bound",
        "missing_parent_bound",
        "runtime_scope_promotion",
        "duplicate_json_field",
        "tampered_system_bytes",
        "tampered_coefficient_bytes",
        "changed_parent_row_bound",
        "changed_original_prefix",
    ],
)
def test_formatter_refuses_malformed_or_unbound_input(tmp_path, case):
    files = inputs(tmp_path)
    leaf = json.loads(files["exclusion"].read_bytes())
    if case == "boolean_dimension":
        ast = json.loads(files["system"].read_bytes())
        ast["variable_count"] = True
        files["system"].write_bytes(json.dumps(ast).encode())
    elif case == "noncanonical_rational":
        leaf["images"][368]["hi"] = "34/4"
    elif case == "changed_coefficient":
        data = json.loads(files["inspection"].read_bytes())
        data["coefficients"][642]["terms"][0]["coefficient"] = "-5"
        files["inspection"].write_bytes(json.dumps(data).encode())
    elif case in ("missing_bound", "changed_candidate_bound"):
        if case == "missing_bound":
            leaf["request"]["bounds"].pop()
        else:
            leaf["request"]["bounds"][368]["hi"] = "1"
        raw = (json.dumps(leaf["request"], separators=(",", ":")) + "\n").encode()
        files["request"].write_bytes(raw)
        leaf["request_sha256"] = hashlib.sha256(raw).hexdigest()
    elif case == "missing_parent_bound":
        parent = json.loads(files["root-receipt"].read_bytes())
        parent["intersections"][0] = None
        files["root-receipt"].write_bytes(json.dumps(parent).encode())
    elif case == "changed_parent_row_bound":
        parent = json.loads(files["root-receipt"].read_bytes())
        parent["intersections"][368]["hi"] = "2"
        files["root-receipt"].write_bytes(json.dumps(parent).encode())
    elif case == "changed_original_prefix":
        reference = json.loads(files["coefficients"].read_bytes())
        reference[0]["terms"][0]["coefficient"] = "-2"
        raw = json.dumps(reference).encode()
        files["coefficients"].write_bytes(raw)
        sha = hashlib.sha256(raw).hexdigest()
        for key in ("inspection", "root-receipt"):
            receipt = json.loads(files[key].read_bytes())
            receipt["coefficient_reference_sha256"] = sha
            if key == "inspection":
                receipt["coefficients"] = reference
            files[key].write_bytes(json.dumps(receipt).encode())
        leaf["coefficient_reference_sha256"] = sha
    elif case == "runtime_scope_promotion":
        leaf["full_56_cell_and_cusp_calculation_complete"] = True
    elif case == "duplicate_json_field":
        files["inspection"].write_bytes(
            b'{"schema":"duplicate",' + files["inspection"].read_bytes()[1:]
        )
    elif case == "tampered_system_bytes":
        files["system"].write_bytes(files["system"].read_bytes() + b" ")
    elif case == "tampered_coefficient_bytes":
        files["coefficients"].write_bytes(files["coefficients"].read_bytes() + b" ")
    files["exclusion"].write_bytes(json.dumps(leaf).encode())
    output = tmp_path / "reflected.lean"
    assert run_formatter(files, output).returncode != 0
    assert not output.exists()


@pytest.mark.parametrize("key", list(NAMES))
def test_formatter_refuses_input_output_alias(tmp_path, key):
    files = inputs(tmp_path)
    before = {name: path.read_bytes() for name, path in files.items()}
    assert run_formatter(files, files[key]).returncode != 0
    assert before == {name: path.read_bytes() for name, path in files.items()}
