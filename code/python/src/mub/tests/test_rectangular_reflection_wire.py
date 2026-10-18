"""Adversarial wire-boundary checks; mathematical checks run in Lean."""

import copy
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
SCRIPT = MUB6_DIR / "scripts/reflect_szollosi_rectangular.py"


def inputs(tmp_path):
    names = {
        "receipt": "mub_szollosi_rectangular_native_receipt.json",
        "system": "mub_szollosi_executable_system.json",
        "coefficients": "mub_szollosi_lean_coefficients.json",
        "request": "mub_szollosi_rectangular_request.json",
    }
    result = {}
    for key, name in names.items():
        result[key] = tmp_path / name
        result[key].write_bytes((ARTIFACTS / name).read_bytes())
    return result


def run_formatter(files, output):
    args = [sys.executable, str(SCRIPT)]
    for key, path in files.items():
        args.extend(["--" + key, str(path)])
    return subprocess.run(
        args + ["--output", str(output)], cwd=ROOT, capture_output=True, text=True, check=False
    )


def test_formatter_reproduces_the_kernel_checked_source(tmp_path):
    files = inputs(tmp_path)
    output = tmp_path / "reflected.lean"
    result = run_formatter(files, output)
    assert result.returncode == 0, result.stderr
    assert (
        output.read_bytes()
        == (ROOT / "lean4/research_programs/mub6/SzollosiRectangularReflection.lean").read_bytes()
    )

    for path in (ROOT / "lean4/research_programs/mub6").glob("SzollosiRectangularJacobian*.lean"):
        assert (tmp_path / path.name).read_bytes() == path.read_bytes()


@pytest.mark.parametrize(
    "case",
    [
        "boolean_dimension",
        "noncanonical_rational",
        "duplicate_preconditioner",
        "missing_jacobian_row",
        "runtime_scope_promotion",
        "unexpected_field",
        "tampered_system_bytes",
        "duplicate_json_field",
    ],
)
def test_formatter_refuses_malformed_or_unbound_input(tmp_path, case):
    files = inputs(tmp_path)
    data = json.loads(files["receipt"].read_bytes())
    request = copy.deepcopy(data["request"])
    if case == "boolean_dimension":
        request["variable_count"] = True
    elif case == "noncanonical_rational":
        data["images"][0]["lo"] = "-2/2"
    elif case == "duplicate_preconditioner":
        row = next(row for row in request["preconditioner"] if row["entries"])
        row["entries"].append(copy.deepcopy(row["entries"][0]))
    elif case == "missing_jacobian_row":
        data["jacobian"].pop()
    elif case == "runtime_scope_promotion":
        data["root_existence_claimed"] = True
    elif case == "unexpected_field":
        data["extra"] = 1
    elif case == "tampered_system_bytes":
        files["system"].write_bytes(files["system"].read_bytes() + b" ")
    elif case == "duplicate_json_field":
        files["receipt"].write_bytes(b'{"schema":"duplicate",' + files["receipt"].read_bytes()[1:])
        output = tmp_path / "reflected.lean"
        assert run_formatter(files, output).returncode != 0
        assert not output.exists()
        return
    if request != data["request"]:
        raw = json.dumps(request, separators=(",", ":")).encode()
        files["request"].write_bytes(raw)
        data["request"] = request
        data["request_sha256"] = hashlib.sha256(raw).hexdigest()
    files["receipt"].write_bytes(json.dumps(data).encode())
    output = tmp_path / "reflected.lean"
    result = run_formatter(files, output)
    assert result.returncode != 0
    assert not output.exists()


@pytest.mark.parametrize("key", ["receipt", "system", "coefficients", "request"])
def test_formatter_refuses_input_output_alias(tmp_path, key):
    files = inputs(tmp_path)
    before = {name: path.read_bytes() for name, path in files.items()}
    assert run_formatter(files, files[key]).returncode != 0
    assert before == {name: path.read_bytes() for name, path in files.items()}
