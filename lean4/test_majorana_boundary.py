"""Falsification harness for the Majorana Lean boundary and its exact oracle.

Origin: papers/derivations/ms_majorana/lean4/MajoranaCore.lean
Claim: urn:omega:fqm:majorana:maj-c2-f2-trichotomy:v1
AuthorityEffect: None
Scope Fence: The harness falsifies computable shadows of the Lean modules. It does not promote a reflexivity lemma into a hardware theorem.
Mutation-Kills: 3 non-equivalent source mutants, executed by papers/derivations/ms_majorana/lean4/test_majorana_boundary.py.
Gate 5 measurement: radon 6.0.1 cyclomatic max 9; lizard 1.24.1 cyclomatic max 9; AST cognitive max 8; nesting max 2.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import warnings
from collections.abc import Callable
from pathlib import Path

import pytest

_DIR = Path(__file__).resolve().parent
if str(_DIR) not in sys.path:
    sys.path.insert(0, str(_DIR))

import majorana_claim_oracle as oracle

_CORE = _DIR / "MajoranaCore.lean"
_GIN = _DIR / "MajoranaGinCore.lean"
_ORACLE = _DIR / "majorana_claim_oracle.py"
_LEAN = Path.home() / ".elan" / "bin" / "lean.exe"
_EXPECTED_SNAPSHOT = (0, 1, 2, 0, 1, 2, 6, 8, 8, 0, 4, 0, 1, 2, 2, 0, 1, 2, 2)

_ORACLE_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("float check bypassed", "if isinstance(value, float):", "if isinstance(value, float) and False:"),
    ("boolean check bypassed", "if isinstance(value, bool):", "if isinstance(value, bool) and False:"),
    ("negative natural admitted", "if value < 0:", "if False and value < 0:"),
    ("cycle count drops the component", "return edge_count - vertex_count + 1", "return edge_count - vertex_count + 0"),
    ("repair route renamed", 'return "Repair"', 'return "Refused"'),
    ("involution sum flipped", "return scale * first + scale * second", "return scale * first - scale * second"),
    ("crosstalk divisor widened", "return count * (count - 1) // 2", "return count * (count - 1) // 1"),
    ("field addition cleared", "mixed.append((left[index] + right[index]) & 1)", "mixed.append((left[index] + right[index]) & 0)"),
    ("cubic counter frozen", "        count += 1\n        cursor += 1", "        count += 0\n        cursor += 1"),
    ("float tag renamed", 'if tag == "float":', 'if tag == "floats":'),
    ("surface arm retargeted", '"SurfaceTopology." + name + " => "', '"SurfaceTopology." + name + " -> "'),
)

_CORE_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("float tag bypassed", 'tag == "float"', 'tag == "floats"'),
    ("bool tag bypassed", 'tag == "bool"', 'tag == "boolean"'),
    ("torus Betti collapsed", "SurfaceTopology.Torus => 2", "SurfaceTopology.Torus => 0"),
    ("toric distance maximized", "def toric_distance (rows cols : Nat) : Nat := min rows cols", "def toric_distance (rows cols : Nat) : Nat := max rows cols"),
    ("sigma dimension inflated", "| IsingAnyon.Sigma => 2", "| IsingAnyon.Sigma => 4"),
    ("cubic product shortened", "def gaussian_elimination_ops (n : Nat) : Nat := n * n * n", "def gaussian_elimination_ops (n : Nat) : Nat := n * n"),
    ("xor replaced by conjunction", "def f2_add (a b : Bool) : Bool := xor a b", "def f2_add (a b : Bool) : Bool := a && b"),
    ("conjunction replaced by disjunction", "def f2_mul (a b : Bool) : Bool := a && b", "def f2_mul (a b : Bool) : Bool := a || b"),
)

_GIN_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("float tag bypassed", 'tag == "float"', 'tag == "floats"'),
    ("bool tag bypassed", 'tag == "bool"', 'tag == "boolean"'),
    ("cancellation mass shifted", "uncancelled_sign_mass == 0", "uncancelled_sign_mass == 1"),
    ("invalid index polarity flipped", "if \u00acis_valid_index then", "if is_valid_index then"),
    ("partner sign test shifted", "c1.sign + c2.sign == 0", "c1.sign + c2.sign == 1"),
)

def surface_mutants() -> tuple[tuple[str, str, str], ...]:
    disk_old = "if name == " + '"Disk":\n        return ' + "0"
    disk_new = "if name == " + '"Disk":\n        return ' + "1"
    torus_old = "if name == " + '"Torus":\n        return ' + "2"
    torus_new = "if name == " + '"Torus":\n        return ' + "3"
    refused = "raise oracle.BoundaryRefusal(" + '"surface name is not admitted", {"received": name})'
    return (
        ("disk Betti inflated", disk_old, disk_new),
        ("torus Betti inflated", torus_old, torus_new),
        ("unknown surface admitted", refused, "return 4"),
    )


def expected_surface_betti(name: str) -> int:
    if name == "Disk":
        return 0
    if name == "Cylinder":
        return 1
    if name == "Torus":
        return 2
    raise oracle.BoundaryRefusal("surface name is not admitted", {"received": name})


def replace_once(source: str, old: str, new: str) -> str:
    count = source.count(old)
    if count != 1:
        raise oracle.BoundaryRefusal(
            "mutant site is not unique",
            {"role": "mutant", "received": str(count)},
        )
    return source.replace(old, new, 1)


def header_kill_count(source: str) -> int:
    needle = "Mutation-Kills: "
    start = source.find(needle)
    if start < 0:
        raise oracle.BoundaryRefusal(
            "mutation kill record is missing",
            {"role": "header", "received": "absent"},
        )
    rest = source[start + len(needle) :]
    digits: list[str] = []
    for char in rest:
        if char.isdigit():
            digits.append(char)
        else:
            break
    if not digits:
        raise oracle.BoundaryRefusal(
            "mutation kill record is not an integer",
            {"role": "header", "received": "absent"},
        )
    return int("".join(digits))


def lean_accepts(source: str, folder: Path) -> bool:
    if not _LEAN.is_file():
        raise oracle.BoundaryRefusal(
            "lean executable is missing",
            {"role": "lean", "received": str(_LEAN)},
        )
    path = folder / "MutantCheck.lean"
    path.write_text(source, encoding="utf-8", newline="\n")
    try:
        completed = subprocess.run(
            [str(_LEAN), str(path)],
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False
    except OSError:
        return False
    return completed.returncode == 0


def killed_lean_mutants(source: str, mutants: tuple[tuple[str, str, str], ...]) -> int:
    killed = 0
    with tempfile.TemporaryDirectory(prefix="majlean") as tmp:
        folder = Path(tmp)
        if not lean_accepts(source, folder):
            raise oracle.BoundaryRefusal(
                "baseline lean module was refused",
                {"role": "lean", "received": "baseline"},
            )
        for name, old, new in mutants:
            mutated = replace_once(source, old, new)
            if lean_accepts(mutated, folder):
                raise oracle.BoundaryRefusal(
                    "non-equivalent mutant survived",
                    {"role": "mutant", "received": name},
                )
            killed += 1
    return killed


def _load_source(source: str, name: str, file_path: Path) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise oracle.BoundaryRefusal("module spec is missing", {"role": "module", "received": name})
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(file_path)
    sys.modules[name] = module
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="__package__ != __spec__.parent",
            category=DeprecationWarning,
        )
        exec(compile(source, str(file_path), "exec"), module.__dict__)
    return dict(module.__dict__)


def _refusal_type(namespace: dict[str, object]) -> type[BaseException] | None:
    found = namespace.get("BoundaryRefusal")
    if isinstance(found, type) and issubclass(found, BaseException):
        return found
    return None


def _raises(probe: object, error: type[BaseException], invariant: str) -> bool:
    if not callable(probe):
        return False
    try:
        probe()
    except error as refusal:
        text = getattr(refusal, "invariant", None)
        return text == invariant
    return False


def _snapshot_holds(namespace: dict[str, object]) -> bool:
    function = namespace.get("claim_snapshot")
    error = _refusal_type(namespace)
    if not callable(function) or error is None:
        return False
    try:
        found = function()
    except error:
        return False
    return bool(found == _EXPECTED_SNAPSHOT)


def _numeric_refusals(namespace: dict[str, object], error: type[BaseException]) -> bool:
    require_nat = namespace.get("require_nat")
    require_int = namespace.get("require_int")
    if not callable(require_nat) or not callable(require_int):
        return False
    if not _raises(lambda: require_nat(1.0, "bound"), error, "float refused at the public boundary"):
        return False
    if not _raises(lambda: require_nat(True, "bound"), error, "boolean refused where an exact integer was required"):
        return False
    if not _raises(lambda: require_nat(-1, "bound"), error, "natural number is negative"):
        return False
    if not _raises(lambda: require_int(1.0, "left"), error, "float refused at the public boundary"):
        return False
    return _raises(lambda: require_int(True, "left"), error, "boolean refused where an exact integer was required")


def _tag_refusals(namespace: dict[str, object], error: type[BaseException]) -> bool:
    admit_tag = namespace.get("admit_tag")
    crosstalk = namespace.get("crosstalk_channels")
    cycles = namespace.get("cycle_count")
    if not callable(admit_tag) or not callable(crosstalk) or not callable(cycles):
        return False
    if not _raises(lambda: admit_tag("float"), error, "float refused at the public boundary"):
        return False
    if not _raises(lambda: admit_tag("bool"), error, "boolean refused where an exact integer was required"):
        return False
    if not _raises(lambda: admit_tag("set"), error, "tag is not an admitted exact scalar"):
        return False
    if not _raises(lambda: admit_tag(1), error, "tag is not an exact scalar name"):
        return False
    if not _raises(lambda: crosstalk(3), error, "multi-terminal hypothesis requires at least four terminals"):
        return False
    return _raises(lambda: cycles(0, 0), error, "connected graph has no vertices")


def _graph_refusals(namespace: dict[str, object], error: type[BaseException]) -> bool:
    dimension = namespace.get("cycle_dimension")
    route = namespace.get("gin_route")
    if not callable(dimension) or not callable(route):
        return False
    if not _raises(lambda: dimension(((True, 1),)), error, "boolean refused where an exact integer was required"):
        return False
    return _raises(lambda: route(1, 0), error, "validity flag is not a boolean")


def _call_text(function: object, argument: str, error: type[BaseException]) -> str | None:
    if not callable(function):
        return None
    try:
        found = function(argument)
    except error:
        return None
    if not isinstance(found, str):
        return None
    return found


def _tags_admitted(namespace: dict[str, object]) -> bool:
    admit_tag = namespace.get("admit_tag")
    error = _refusal_type(namespace)
    if not callable(admit_tag) or error is None:
        return False
    nat_tag = _call_text(admit_tag, "nat", error)
    int_tag = _call_text(admit_tag, "int", error)
    return nat_tag == "nat" and int_tag == "int"


def _oracle_holds(namespace: dict[str, object]) -> bool:
    error = _refusal_type(namespace)
    if error is None:
        return False
    if not _snapshot_holds(namespace):
        return False
    if not _numeric_refusals(namespace, error):
        return False
    if not _tag_refusals(namespace, error):
        return False
    if not _graph_refusals(namespace, error):
        return False
    return _tags_admitted(namespace)


def _mutant_survived(
    source: str,
    name: str,
    file_path: Path,
    oracle_fn: Callable[[dict[str, object]], bool],
) -> bool:
    try:
        namespace = _load_source(source, name, file_path)
    except Exception:
        return False
    try:
        return bool(oracle_fn(namespace))
    except Exception:
        return False


def _forget(names: list[str]) -> None:
    for name in names:
        sys.modules.pop(name, None)


def kill_python_mutants(
    source: str,
    mutants: tuple[tuple[str, str, str], ...],
    module_name: str,
    file_path: Path,
    oracle_fn: Callable[[dict[str, object]], bool],
) -> int:
    loaded: list[str] = []
    try:
        baseline_name = module_name + "_baseline"
        loaded.append(baseline_name)
        baseline = _load_source(source, baseline_name, file_path)
        if not oracle_fn(baseline):
            raise oracle.BoundaryRefusal(
                "baseline python module was refused",
                {"role": "mutant", "received": module_name},
            )
        killed = 0
        index = 0
        for name, old, new in mutants:
            mutated = replace_once(source, old, new)
            mutant_name = module_name + "_mutant_" + str(index)
            loaded.append(mutant_name)
            if _mutant_survived(mutated, mutant_name, file_path, oracle_fn):
                raise oracle.BoundaryRefusal(
                    "non-equivalent mutant survived",
                    {"role": "mutant", "received": name},
                )
            killed += 1
            index += 1
        return killed
    finally:
        _forget(loaded)


def _surface_matches(disk: object, cylinder: object, torus: object) -> bool:
    if disk != oracle.cycle_dimension(oracle.disk_incidence()):
        return False
    if cylinder != oracle.cycle_dimension(oracle.cylinder_incidence()):
        return False
    if torus != oracle.cycle_dimension(oracle.torus_incidence()):
        return False
    return True


def _surface_oracle(namespace: dict[str, object]) -> bool:
    function = namespace.get("expected_surface_betti")
    if not callable(function):
        return False
    try:
        disk = function("Disk")
        cylinder = function("Cylinder")
        torus = function("Torus")
    except oracle.BoundaryRefusal:
        return False
    if not _surface_matches(disk, cylinder, torus):
        return False
    try:
        function("Annulus")
    except oracle.BoundaryRefusal as refusal:
        return refusal.invariant == "surface name is not admitted"
    return False


def test_exact_cycle_and_cubic_counts() -> None:
    assert oracle.claim_snapshot() == _EXPECTED_SNAPSHOT
    assert oracle.cycle_dimension(oracle.disk_incidence()) == 0
    assert oracle.cylinder_rank() == 2
    assert oracle.cycle_dimension(()) == 0
    assert oracle.counted_cubic(0) == 0
    assert oracle.polynomial_cubic(0) == 0
    assert oracle.counted_cubic(3) == 27
    assert oracle.polynomial_cubic(3) == 27


def test_exact_routes_tags_and_mass() -> None:
    assert oracle.signed_mass(2, 1, -1) == 0
    assert oracle.gin_route(True, 0) == "Repair"
    assert oracle.gin_route(True, 2) == "SplitBrainRefusal"
    assert oracle.gin_route(False, 4) == "ClosureFailure"
    assert oracle.admit_tag("nat") == "nat"
    assert oracle.admit_tag("int") == "int"
    assert expected_surface_betti("Cylinder") == 1


def test_negative_numeric_boundary() -> None:
    with pytest.raises(oracle.BoundaryRefusal) as floated:
        oracle.require_nat(1.0, "bound")
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "bound"
    assert floated.value.parameters["received"] == "float"
    with pytest.raises(oracle.BoundaryRefusal) as boolean:
        oracle.require_nat(True, "bound")
    assert boolean.value.invariant == "boolean refused where an exact integer was required"
    assert boolean.value.parameters["received"] == "bool"
    with pytest.raises(oracle.BoundaryRefusal) as negative:
        oracle.require_nat(-1, "bound")
    assert negative.value.invariant == "natural number is negative"
    assert negative.value.parameters["received"] == "-1"


def test_negative_tag_boundary() -> None:
    with pytest.raises(oracle.BoundaryRefusal) as textual:
        oracle.require_int("1", "left")
    assert textual.value.invariant == "value is not an exact integer"
    with pytest.raises(oracle.BoundaryRefusal) as tag_float:
        oracle.admit_tag("float")
    assert tag_float.value.invariant == "float refused at the public boundary"
    with pytest.raises(oracle.BoundaryRefusal) as tag_bool:
        oracle.admit_tag("bool")
    assert tag_bool.value.invariant == "boolean refused where an exact integer was required"
    with pytest.raises(oracle.BoundaryRefusal) as tag_other:
        oracle.admit_tag("set")
    assert tag_other.value.invariant == "tag is not an admitted exact scalar"
    assert tag_other.value.parameters["received"] == "set"


def test_negative_graph_and_route_boundary() -> None:
    with pytest.raises(oracle.BoundaryRefusal) as tag_number:
        oracle.admit_tag(1)
    assert tag_number.value.invariant == "tag is not an exact scalar name"
    with pytest.raises(oracle.BoundaryRefusal) as binary:
        oracle.admit_tag(1.0)
    assert binary.value.invariant == "float refused at the public boundary"
    with pytest.raises(oracle.BoundaryRefusal) as flag:
        oracle.admit_tag(True)
    assert flag.value.invariant == "boolean refused where an exact integer was required"
    with pytest.raises(oracle.BoundaryRefusal) as terminals:
        oracle.crosstalk_channels(3)
    assert terminals.value.invariant == "multi-terminal hypothesis requires at least four terminals"


def test_negative_incidence_and_surface_boundary() -> None:
    with pytest.raises(oracle.BoundaryRefusal) as empty:
        oracle.cycle_count(0, 0)
    assert empty.value.invariant == "connected graph has no vertices"
    with pytest.raises(oracle.BoundaryRefusal) as bit:
        oracle.cycle_dimension(((True, 1),))
    assert bit.value.invariant == "boolean refused where an exact integer was required"
    assert bit.value.parameters["role"] == "bit"
    with pytest.raises(oracle.BoundaryRefusal) as width:
        oracle.cycle_dimension(((1, 0), (1,)))
    assert width.value.invariant == "incidence rows do not have equal width"
    with pytest.raises(oracle.BoundaryRefusal) as outside:
        oracle.cycle_dimension(((2, 0),))
    assert outside.value.invariant == "bit is outside the field F2"


def test_negative_route_and_missing_surface() -> None:
    with pytest.raises(oracle.BoundaryRefusal) as route:
        oracle.gin_route(1, 0)
    assert route.value.invariant == "validity flag is not a boolean"
    with pytest.raises(oracle.BoundaryRefusal) as surface:
        expected_surface_betti("Annulus")
    assert surface.value.invariant == "surface name is not admitted"
    with pytest.raises(oracle.BoundaryRefusal) as missing:
        oracle.surface_betti("def unused : Nat := 0\n", "Torus")
    assert missing.value.invariant == "surface arm is missing"


def test_integration_surface_and_channels() -> None:
    source = _CORE.read_text(encoding="utf-8")
    assert oracle.surface_betti(source, "Disk") == oracle.cycle_dimension(oracle.disk_incidence())
    assert oracle.surface_betti(source, "Cylinder") == oracle.cycle_count(3, 3)
    assert oracle.surface_betti(source, "Torus") == oracle.cycle_count(1, 2)
    assert oracle.crosstalk_channels(4) == 6
    assert oracle.crosstalk_channels(5) == 10


def test_integration_routes_mass_and_cubic() -> None:
    source = _CORE.read_text(encoding="utf-8")
    assert oracle.counted_cubic(2) == oracle.polynomial_cubic(2)
    assert oracle.gf2_rank(((1, 1), (1, 0))) == 2
    assert oracle.signed_mass(3, -1, 1) == 0
    assert oracle.gin_route(False, 0) == "ClosureFailure"
    assert expected_surface_betti("Torus") == oracle.surface_betti(source, "Torus")


def test_end_to_end_origin_resolves() -> None:
    repo = Path(__file__).resolve().parents[4]
    manuscript = (repo / "papers" / "derivations" / "ms_majorana" / "the_majorana_problem.md").read_text(encoding="utf-8")
    provenance = (_DIR / "PROVENANCE.md").read_text(encoding="utf-8")
    core = _CORE.read_text(encoding="utf-8")
    gin = _GIN.read_text(encoding="utf-8")
    assert "MAJ-C2" in manuscript
    assert "Theorem 4.1" in manuscript
    assert "GIN-C3" in provenance
    assert "exact_gin_cancellation_routes_to_repair" in provenance
    assert "Origin: papers/derivations/ms_majorana/the_majorana_problem.md" in core
    assert "Claim: urn:omega:fqm:majorana:maj-c2-f2-trichotomy:v1" in core
    assert "AuthorityEffect: None" in core


def test_end_to_end_lean_modules_compile() -> None:
    core = _CORE.read_text(encoding="utf-8")
    gin = _GIN.read_text(encoding="utf-8")
    assert "Origin: papers/derivations/ms_majorana/lean4/PROVENANCE.md" in gin
    assert "Claim: urn:omega:fqm:majorana:gin-c3-terminal-route:v1" in gin
    assert "AuthorityEffect: None" in gin
    with tempfile.TemporaryDirectory(prefix="maje2e") as tmp:
        folder = Path(tmp)
        assert lean_accepts(core, folder) is True
        assert lean_accepts(gin, folder) is True


def test_oracle_mutants_are_killed() -> None:
    source = _ORACLE.read_text(encoding="utf-8")
    killed = kill_python_mutants(source, _ORACLE_MUTANTS, "majorana_oracle_mutant", _ORACLE, _oracle_holds)
    assert killed == len(_ORACLE_MUTANTS)
    assert header_kill_count(source) == killed


def test_surface_mutants_are_killed() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    mutants = surface_mutants()
    killed = kill_python_mutants(source, mutants, "majorana_surface_mutant", Path(__file__), _surface_oracle)
    assert killed == len(mutants)
    assert header_kill_count(source) == killed


def test_core_lean_mutants_are_killed() -> None:
    source = _CORE.read_text(encoding="utf-8")
    killed = killed_lean_mutants(source, _CORE_MUTANTS)
    assert killed == len(_CORE_MUTANTS)
    assert header_kill_count(source) == killed


def test_gin_lean_mutants_are_killed() -> None:
    source = _GIN.read_text(encoding="utf-8")
    killed = killed_lean_mutants(source, _GIN_MUTANTS)
    assert killed == len(_GIN_MUTANTS)
    assert header_kill_count(source) == killed
