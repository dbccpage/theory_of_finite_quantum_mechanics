"""Origin: research/quantum_to_classical_descent/test_check_exact.py
Claim: the Q(i) certificate rejects non-rational scalars, nonreal coordinates, and non-Hermitian arguments, and its four listed mutants change those results
AuthorityEffect: None
Scope Fence: this file does not claim analytic all-time proofs or hardware
Level: L5
MutationKillCount: 4
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

SCRIPT = Path(__file__).resolve().parent / "check_exact.py"
_PASS = (
    "cochain: rank D0=1; Phi(b)=0; Phi(w)=2; completed constants=1,1",
    "unitary fixture: derivatives +/-3/5; closure ranks=1,2,2; one new row",
    "open fixture: G=[[-2,1],[2,-1]]; stationary=(1/3,2/3)",
    "measurement: p=(9/25,16/25); D(rho,sigma)=12/25; SA defect=576/625",
    "Bell: S=14/5; dual transpose entries={0,4}; dual objective=-4/5",
    "other carriers: triangle raw=2, quotient=0; binary correction controls; odd star loop",
    "PASS: explicit finite certificates, using exact Q(i) arithmetic.",
    "Not checked by this program: analytic all-time proofs, Lieb-Robinson premises, hardware, or Lean.",
)


def _load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _call(module: ModuleType, name: str, *args: object) -> object:
    function: object = getattr(module, name)
    if not callable(function):
        raise RuntimeError(name)
    return function(*args)


def _raises(module: ModuleType, name: str, *args: object) -> bool:
    try:
        _call(module, name, *args)
    except Exception as error:
        return type(error).__name__ == "CertificateError"
    return False


def test_exact_guards_and_rank() -> None:
    module = _load(SCRIPT, "check_exact_unit")
    assert _raises(module, "c", True)
    assert _raises(module, "c", "nope")
    assert _raises(module, "real", getattr(module, "II"))
    assert _raises(module, "big_rational", 1, 0)
    bad = _call(module, "mat", [[0, 1], [0, 0]])
    assert _raises(module, "psd", bad)
    verification = _call(module, "verify_rank", 2, 2)
    assert getattr(verification, "holds") is True
    assert _call(module, "syndrome", (1, 0, 0)) == 1


def test_end_to_end_prints_the_certificate() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0
    for line in _PASS:
        assert line in result.stdout


def test_optimized_mode_is_refused() -> None:
    result = subprocess.run(
        [sys.executable, "-O", str(SCRIPT)],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode != 0


def _mutant(tmp_path: Path, label: str, old: str, new: str) -> ModuleType:
    text = SCRIPT.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise AssertionError(label)
    destination = tmp_path / f"{label}.py"
    destination.write_text(text.replace(old, new, 1), encoding="utf-8")
    return _load(destination, f"check_exact_{label}")


def test_mutation_kills(tmp_path: Path) -> None:
    killed = _kill_rank(tmp_path)
    killed = killed + _kill_real(tmp_path)
    killed = killed + _kill_psd(tmp_path)
    killed = killed + _kill_bool(tmp_path)
    assert killed == 4


def _kill_rank(tmp_path: Path) -> int:
    module = _mutant(tmp_path, "rank", "verify_rank(rank(d0), 1)", "verify_rank(rank(d0), 2)")
    if _raises(module, "run_cochain"):
        return 1
    return 0


def _kill_real(tmp_path: Path) -> int:
    module = _mutant(tmp_path, "real", "if value.im != 0:", "if False and value.im != 0:")
    if _raises(module, "real", getattr(module, "II")):
        return 0
    return 1


def _kill_psd(tmp_path: Path) -> int:
    module = _mutant(
        tmp_path,
        "psd",
        "if matrix != dag(matrix):",
        "if False and matrix != dag(matrix):",
    )
    bad = _call(module, "mat", [[0, 1], [0, 0]])
    if _raises(module, "psd", bad):
        return 0
    return 1


def _kill_bool(tmp_path: Path) -> int:
    module = _mutant(
        tmp_path,
        "bool",
        "if isinstance(value, bool) or not isinstance(value, int):",
        "if not isinstance(value, int):",
    )
    if _raises(module, "c", True):
        return 0
    return 1
