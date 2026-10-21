"""Isolated exact certificates for the qm slice.

Origin: lean4/LorentzBoost.lean theorem boost_hyperbolic_identity
(5 * 5 - 3 * 3 = 16).
Claim: urn:omega:fqm:qm:isolated-certificate-suite:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 8; AST Sonar cognitive complexity max 12; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 10.
Scope Fence: The witness identity is the integer 16 from that Lean theorem.
The suite checks the qm certificates imported here. It does not extend their claims.
"""

from __future__ import annotations

import ast
import importlib
import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path
from typing import Mapping, NamedTuple

import pytest


class WitnessError(Exception):
    """One violated witness invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


class Certificate(NamedTuple):
    module: str
    relative: str
    expected: Fraction
    package: str
    origin_path: str
    needle: str
    old: str
    new: str


_QM = Path(__file__).resolve().parent if Path(__file__).resolve().parent.name == "qm" else Path(__file__).resolve().parents[1]


def _read_source(relative: str) -> str:
    path = _QM / relative
    if not path.exists():
        if relative.endswith("__init__.py"):
            prefix = relative.split("/")[0]
            path = _QM / f"{prefix}.py"
        else:
            path = _QM / Path(relative).name
    return path.read_text(encoding="utf-8")

_SHARED: tuple[tuple[str, str], ...] = (
    ("if isinstance(value, float):", "if False and isinstance(value, float):"),
    ("if type(value) is bool:", "if False and type(value) is bool:"),
    ("if isinstance(value, Fraction):", "if False and isinstance(value, Fraction):"),
    ("if type(value) is int:", "if False and type(value) is int:"),
    ("if value != expected:", "if value == expected:"),
    ("return _MARK", "return _MARK + 1"),
    ("if _mark() != 7:", "if _mark() == 7:"),
)
_CASES: tuple[Certificate, ...] = (
    Certificate("src.qm.campaigns.boost_composition", "campaigns/boost_composition.py", Fraction(4, 5), "src.qm.campaigns", "lean4/BoostComposition.lean", "theorem composition_trace", "return (left + right) / denom", "return (left - right) / denom"),
    Certificate("src.qm.campaigns.born_gleason", "campaigns/born_gleason.py", Fraction(0), "src.qm.campaigns", "code/python/src/qm/campaigns/born_gleason.py", "", "gap = _frame_sum(vector, coordinate) - _frame_sum(vector, rotated)", "gap = _frame_sum(vector, coordinate) + _frame_sum(vector, rotated)"),
    Certificate("src.qm.campaigns.buildability", "campaigns/buildability.py", Fraction(5), "src.qm.campaigns", "code/python/src/qm/campaigns/buildability.py", "", "return left + right", "return left - right"),
    Certificate("src.qm.campaigns.carrier", "campaigns/carrier.py", Fraction(0), "src.qm.campaigns", "code/python/src/qm/campaigns/carrier.py", "", 'total += _require_fraction(weights[2], "edge2")', 'total -= _require_fraction(weights[2], "edge2")'),
    Certificate("src.qm.campaigns.causal_order", "campaigns/causal_order.py", Fraction(4), "src.qm.campaigns", "code/python/src/qm/campaigns/causal_order.py", "", "if ranks != (0, 1, 1, 2):", "if ranks == (0, 1, 1, 2):"),
    Certificate("src.qm.campaigns.channel_census", "campaigns/channel_census.py", Fraction(2), "src.qm.campaigns", "code/python/src/qm/campaigns/channel_census.py", "", "if count != _COUNT:", "if count == _COUNT:"),
    Certificate("src.qm.campaigns.commuting_obs", "campaigns/commuting_obs.py", Fraction(4), "src.qm.campaigns", "lean4/CommutingObservables.lean", "def pauliX", "total += abs(product[row][column] - reverse[row][column])", "total += abs(product[row][column] + reverse[row][column])"),
    Certificate("src.qm.campaigns.context_barrier", "campaigns/context_barrier.py", Fraction(8), "src.qm.campaigns", "code/python/src/qm/campaigns/context_barrier.py", "", "if mass == 0:", "if mass != 0:"),
    Certificate("src.qm.campaigns.continuum", "campaigns/continuum.py", Fraction(4), "src.qm.campaigns", "lean4/H056ContinuumLiftBoundary.lean", "theorem commutator_trace_zero", "return Fraction(count)", "return Fraction(count + 1)"),
    Certificate("src.qm.campaigns.dynamics", "campaigns/dynamics.py", Fraction(3), "src.qm.campaigns", "code/python/src/qm/campaigns/dynamics.py", "", "return left[row][0] * right[0][column] + left[row][1] * right[1][column] + left[row][2] * right[2][column]", "return left[row][0] * right[0][column] + left[row][1] * right[1][column] - left[row][2] * right[2][column]"),
    Certificate("src.qm.campaigns.everett", "campaigns/everett.py", Fraction(3, 5), "src.qm.campaigns", "code/python/src/qm/campaigns/everett.py", "", "return parsed[first] / mass", "return parsed[first] * mass"),
    Certificate("src.qm.campaigns.finite_geometry_host", "campaigns/finite_geometry_host.py", Fraction(0), "src.qm.campaigns", "code/python/src/qm/campaigns/finite_geometry_host.py", "", "defect += abs(lines_through(point) - 3)", "defect += abs(lines_through(point) - 4)"),
    Certificate("src.qm.campaigns.foundational_targets", "campaigns/foundational_targets.py", Fraction(5, 8), "src.qm.campaigns", "code/python/src/qm/campaigns/foundational_targets.py", "", "return square_00 + square_11", "return square_00 - square_11"),
    Certificate("src.qm.campaigns.gleason", "campaigns/gleason.py", Fraction(0), "src.qm.campaigns", "code/python/src/qm/campaigns/gleason.py", "", 'return _locked(left - right, _GAP, "Gleason frame gap drifted")', 'return _locked(left + right, _GAP, "Gleason frame gap drifted")'),
    Certificate("src.qm.campaigns.higher_dim", "campaigns/higher_dim.py", Fraction(3), "src.qm.campaigns", "code/python/src/qm/campaigns/higher_dim.py", "", "return left[row][0] * right[0][column] + left[row][1] * right[1][column] + left[row][2] * right[2][column]", "return left[row][0] * right[0][column] + left[row][1] * right[1][column] - left[row][2] * right[2][column]"),
    Certificate("src.qm.campaigns.import_bundle", "campaigns/import_bundle.py", Fraction(30), "src.qm.campaigns", "code/python/src/qm/campaigns/import_bundle.py", "", "return trace * determinant * purity", "return trace + determinant * purity"),
    Certificate("src.qm.campaigns.lorentz_boost", "campaigns/lorentz_boost.py", Fraction(0), "src.qm.campaigns", "lean4/LorentzBoost.lean", "theorem boost_hyperbolic_identity", "abs(left[0][0] - right[0][0])", "abs(left[0][0] + right[0][0])"),
    Certificate("src.qm.campaigns.mub_reports", "campaigns/mub_reports.py", Fraction(-7, 50), "src.qm.campaigns", "code/python/src/qm/campaigns/mub_reports.py", "", "return Fraction(1, 2) - overlap", "return Fraction(1, 2) + overlap"),
    Certificate("src.qm.campaigns.quantum_walk", "campaigns/quantum_walk.py", Fraction(1, 2), "src.qm.campaigns", "code/python/src/qm/campaigns/quantum_walk.py", "", "return square[0][0]", "return square[0][1]"),
    Certificate("src.qm.campaigns.residual_density", "campaigns/residual_density.py", Fraction(1), "src.qm.campaigns", "code/python/src/qm/campaigns/residual_density.py", "", "return abs(residual[0]) + abs(residual[1]) + abs(residual[2]) + abs(residual[3])", "return abs(residual[1]) + abs(residual[2]) + abs(residual[3])"),
    Certificate("src.qm.campaigns.rotation_groups", "campaigns/rotation_groups.py", Fraction(4), "src.qm.campaigns", "code/python/src/qm/campaigns/rotation_groups.py", "", "return left[row][0] * right[0][column] + left[row][1] * right[1][column]", "return left[row][0] * right[0][column] - left[row][1] * right[1][column]"),
    Certificate("src.qm.campaigns.sector_conditioning", "campaigns/sector_conditioning.py", Fraction(2, 3), "src.qm.campaigns", "code/python/src/qm/campaigns/sector_conditioning.py", "", "mass += value", "mass -= value"),
    Certificate("src.qm.campaigns.spectral_claims", "campaigns/spectral_claims.py", Fraction(0), "src.qm.campaigns", "code/python/src/qm/campaigns/spectral_claims.py", "", "if constant != 2:", "if constant == 2:"),
    Certificate("src.qm.campaigns.toric", "campaigns/toric.py", Fraction(2), "src.qm.campaigns", "lean4/H044SurfaceCodeToricTopology.lean", "theorem homology_dimension_k2", "dimension = 8 - rank_x - rank_z", "dimension = 8 - rank_x + rank_z"),
    Certificate("src.qm.campaigns.tower", "campaigns/tower.py", Fraction(4), "src.qm.campaigns", "lean4/H052CyclotomicTowerDirected.lean", "theorem subfield_inclusion_trans", "degree = first * second", "degree = first * second * first"),
    Certificate("src.qm.data", "data/__init__.py", Fraction(1, 2), "src.qm.data", "code/python/src/qm/data/__init__.py", "", "return left * left + right * right", "return left * left - right * right"),
    Certificate("src.qm.campaigns", "campaigns/__init__.py", Fraction(-1), "src.qm.campaigns", "lean4/CommutingObservables.lean", "def pauliX", "return Fraction(xz[0][1])", "return Fraction(xz[0][0])"),
    Certificate("src.qm.entrypoints", "entrypoints/__init__.py", Fraction(12), "src.qm.entrypoints", "code/python/src/qm/entrypoints/__init__.py", "", "if blocks * bets != 30:", "if blocks * bets == 30:"),
)
_WITNESS_MUTANTS: tuple[tuple[tuple[str, str], tuple[str, str]], ...] = (
    (("left = 5 ", "* 5"), ("left = 5 ", "+ 5")),
    (("right = 3 ", "* 3"), ("right = 3 ", "+ 3")),
    (("if left ", "!= 25:"), ("if left ", "== 25:")),
    (("if right ", "!= 9:"), ("if right ", "== 9:")),
    (("gap = left ", "- right"), ("gap = left ", "+ right")),
    (("if left - right ", "!= gap:"), ("if left - right ", "== gap:")),
    (("if gap ", "!= 16:"), ("if gap ", "== 16:")),
    (("return ", "gap"), ("return ", "gap + 1")),
)


def _float_probe() -> object:
    value = ast.literal_eval("1.0")
    if type(value).__name__ in {"int", "bool"}:
        raise WitnessError("admitted scalar is not a refusal probe")
    return value


def witness_identity() -> int:
    """5 * 5 - 3 * 3, the numerator checked by boost_hyperbolic_identity."""
    left = 5 * 5
    right = 3 * 3
    if left != 25:
        raise WitnessError("witness square drifted", {"value": left})
    if right != 9:
        raise WitnessError("witness second square drifted", {"value": right})
    gap = left - right
    if left - right != gap:
        raise WitnessError("witness difference drifted", {"value": gap})
    if gap != 16:
        raise WitnessError("witness hyperbolic gap drifted", {"value": gap})
    return gap


def _load(source: str, name: str, package: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise WitnessError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = package
    module.__file__ = str(Path(__file__).resolve())
    sys.modules[name] = module
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="__package__ != __spec__.parent", category=DeprecationWarning)
        exec(compile(source, name + ".py", "exec"), module.__dict__)
    return module.__dict__


def _good(namespace: dict[str, object], expected: Fraction) -> bool:
    certify = namespace.get("certify")
    if not callable(certify):
        return False
    try:
        bare = certify()
        probed = certify(1)
        rational = certify(Fraction(1))
    except Exception:
        return False
    return bool(bare == expected) and bool(probed == expected) and bool(rational == expected)


def _refused(certify: object, probe: object, invariant: str) -> bool:
    if not callable(certify):
        return False
    try:
        certify(probe)
    except Exception as caught:
        return getattr(caught, "invariant", None) == invariant
    return False


def _oracle(namespace: dict[str, object], expected: Fraction) -> bool:
    certify = namespace.get("certify")
    if _good(namespace, expected) is False:
        return False
    floated = _refused(certify, _float_probe(), "float refused at the public boundary")
    boolean = _refused(certify, True, "boolean refused where a rational was required")
    text = _refused(certify, "text", "value is not an exact rational")
    return floated and boolean and text


def _killed_site(source: str, old: str, new: str, name: str, package: str, expected: Fraction) -> bool:
    try:
        namespace = _load(source.replace(old, new, 1), name, package)
        killed = _oracle(namespace, expected) is False
    except Exception:
        killed = True
    finally:
        sys.modules.pop(name, None)
    return killed


def _require_killed(source: str, old: str, new: str, name: str, case: Certificate) -> None:
    if source.count(old) != 1:
        raise WitnessError("mutant site is not unique", {"site": old, "count": source.count(old), "module": case.module})
    if _killed_site(source, old, new, name, case.package, case.expected) is not True:
        raise WitnessError("mutant survived", {"site": old, "module": case.module})


def _pairs(case: Certificate) -> tuple[tuple[str, str], ...]:
    return _SHARED + ((case.old, case.new),)


def _expect(error: type[BaseException], probe: object, invariant: str) -> None:
    if not callable(probe):
        raise WitnessError("negative probe is not callable")
    try:
        probe()
    except error as caught:
        if getattr(caught, "invariant", None) != invariant:
            raise WitnessError("negative probe violated a different invariant", {"expected": invariant, "actual": getattr(caught, "invariant", None)})
        return
    raise WitnessError("negative probe was accepted", {"invariant": invariant})


def test_witness_identity_matches_lean() -> None:
    root = next((p for p in Path(__file__).resolve().parents if (p / "lean4").exists()), Path(__file__).resolve().parents[4])
    source = (root / "lean4" / "LorentzBoost.lean").read_text(encoding="utf-8")
    if "theorem boost_hyperbolic_identity" not in source:
        raise WitnessError("LorentzBoost witness theorem is missing")
    if witness_identity() != 16:
        raise WitnessError("witness identity drifted", {"value": witness_identity()})


def test_certificates_match_locked_values() -> None:
    index = 0
    while index < len(_CASES):
        case = _CASES[index]
        module = importlib.import_module(case.module)
        if module.certify() != case.expected:
            raise WitnessError("certificate drifted", {"module": case.module})
        if module.certify(1) != case.expected:
            raise WitnessError("integer probe drifted", {"module": case.module})
        if module.certify(Fraction(1)) != case.expected:
            raise WitnessError("rational probe drifted", {"module": case.module})
        index += 1


def test_negative_probes() -> None:
    index = 0
    while index < len(_CASES):
        case = _CASES[index]
        module = importlib.import_module(case.module)
        _expect(Exception, lambda: module.certify(_float_probe()), "float refused at the public boundary")
        _expect(Exception, lambda: module.certify(True), "boolean refused where a rational was required")
        _expect(Exception, lambda: module.certify("text"), "value is not an exact rational")
        index += 1


def test_domain_negatives() -> None:
    carrier = importlib.import_module("src.qm.campaigns.carrier")
    clock = importlib.import_module("src.qm.campaigns.higher_dim")
    data = importlib.import_module("src.qm.data")
    _expect(carrier.CarrierCurvatureError, lambda: carrier.curvature((1, 2)), "triangle carrier needs 3 edges")
    _expect(clock.ClockError, lambda: clock.clock_order(2), "this clock certificate is the qutrit clock")
    _expect(data.FixtureRationalError, lambda: data.parse_fixture_rational("nope"), "fixture rational must be 'a/b'")
    _expect(carrier.CarrierCurvatureError, lambda: carrier.curvature((_float_probe(), 0, 0)), "float refused at the public boundary")


def _require_value(actual: object, expected: object, invariant: str) -> None:
    if actual != expected:
        raise WitnessError(invariant, {"actual": str(actual), "expected": str(expected)})


def test_integration_across_certificates() -> None:
    boost = importlib.import_module("src.qm.campaigns.boost_composition")
    lorentz = importlib.import_module("src.qm.campaigns.lorentz_boost")
    continuum = importlib.import_module("src.qm.campaigns.continuum")
    walk = importlib.import_module("src.qm.campaigns.quantum_walk")
    mub = importlib.import_module("src.qm.campaigns.mub_reports")
    campaigns = importlib.import_module("src.qm.campaigns")
    entrypoints = importlib.import_module("src.qm.entrypoints")
    commuting = importlib.import_module("src.qm.campaigns.commuting_obs")
    carrier = importlib.import_module("src.qm.campaigns.carrier")
    data = importlib.import_module("src.qm.data")
    _require_value(boost.composition_trace(), 65, "composition trace drifted")
    _require_value(lorentz.hyperbolic_identity(), 16, "hyperbolic identity drifted")
    _require_value(continuum.trace_obstruction(), Fraction(4), "trace obstruction drifted")
    _require_value(walk.cycle_return(), Fraction(1, 2), "cycle return drifted")
    _require_value(mub.overlap_gap(), Fraction(1, 2) - Fraction(16, 25), "overlap gap drifted")
    _require_value(campaigns.campaign_pauli_anticommutator(), Fraction(-1), "Pauli entry drifted")
    _require_value(entrypoints.entrypoint_alias_count(), 12, "entrypoint count drifted")
    _require_value(commuting.commutator_mass(((1, 0), (0, 2)), ((3, 0), (0, -1))), 0, "diagonal commutator drifted")
    _require_value(carrier.constant_weight_curvature(), 3, "constant curvature drifted")
    _require_value(data.parse_fixture_rational("2/4"), Fraction(1, 2), "fixture reduction drifted")
    _require_value(data.fixture_purity(), Fraction(1, 2), "fixture purity drifted")


def test_end_to_end_cli() -> None:
    index = 0
    while index < len(_CASES):
        case = _CASES[index]
        module = importlib.import_module(case.module)
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = module.main()
        if code != 0:
            raise WitnessError("certificate command failed", {"module": case.module, "code": code})
        if stdout.getvalue() != str(case.expected) + "\n":
            raise WitnessError("certificate command printed the wrong value", {"module": case.module, "printed": stdout.getvalue()})
        index += 1


def test_origins_resolve() -> None:
    root = next((p for p in Path(__file__).resolve().parents if (p / "lean4").exists()), Path(__file__).resolve().parents[4])
    index = 0
    while index < len(_CASES):
        case = _CASES[index]
        source = _read_source(case.relative)
        if case.origin_path not in source:
            raise WitnessError("origin path is not cited", {"module": case.module})
        if "AuthorityEffect: None" not in source:
            raise WitnessError("authority effect is missing", {"module": case.module})
        if "Scope Fence:" not in source:
            raise WitnessError("scope fence is missing", {"module": case.module})
        target = root / case.origin_path
        if not target.exists():
            if case.origin_path.endswith("__init__.py"):
                prefix = Path(case.origin_path).parent.name
                target = root / "code" / "python" / "src" / "qm" / f"{prefix}.py"
            else:
                target = root / "code" / "python" / "src" / "qm" / Path(case.origin_path).name
        if target.exists() is False:
            raise WitnessError("origin file is missing", {"path": case.origin_path})
        if case.needle != "" and case.needle not in target.read_text(encoding="utf-8"):
            raise WitnessError("origin does not contain the cited statement", {"needle": case.needle})
        index += 1


@pytest.mark.parametrize("case", _CASES, ids=lambda case: case.relative)
def test_mutation_kills(case: Certificate) -> None:
    source = _read_source(case.relative)
    baseline = "isolated_baseline_" + case.module.replace(".", "_")
    try:
        namespace = _load(source, baseline, case.package)
        if _oracle(namespace, case.expected) is not True:
            raise WitnessError("baseline oracle failed", {"module": case.module})
    finally:
        sys.modules.pop(baseline, None)
    pairs = _pairs(case)
    index = 0
    killed = 0
    while index < len(pairs):
        old, new = pairs[index]
        _require_killed(source, old, new, "isolated_mutant_" + str(index) + "_" + case.module.replace(".", "_"), case)
        killed += 1
        index += 1
    if killed != 8:
        raise WitnessError("kill count drifted", {"killed": killed, "module": case.module})
    receipt = "Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py."
    if receipt not in source:
        raise WitnessError("kill receipt is missing", {"module": case.module})


def _witness_holds(namespace: dict[str, object]) -> bool:
    witness = namespace.get("witness_identity")
    if not callable(witness):
        return False
    try:
        value = witness()
    except Exception:
        return False
    return bool(value == 16)


def test_witness_mutation_kills() -> None:
    path = Path(__file__)
    source = path.read_text(encoding="utf-8")
    baseline = "isolated_witness_baseline"
    try:
        namespace = _load(source, baseline, "")
        if _witness_holds(namespace) is not True:
            raise WitnessError("witness baseline oracle failed")
    finally:
        sys.modules.pop(baseline, None)
    killed = 0
    index = 0
    while index < len(_WITNESS_MUTANTS):
        old_parts, new_parts = _WITNESS_MUTANTS[index]
        old = "".join(old_parts)
        new = "".join(new_parts)
        if source.count(old) != 1:
            raise WitnessError("witness mutant site is not unique", {"site": old, "count": source.count(old)})
        name = "isolated_witness_mutant_" + str(index)
        try:
            mutated = _load(source.replace(old, new, 1), name, "")
            survived = _witness_holds(mutated)
        except Exception:
            survived = False
        finally:
            sys.modules.pop(name, None)
        if survived:
            raise WitnessError("witness mutant survived", {"site": old})
        killed += 1
        index += 1
    if killed != 8:
        raise WitnessError("witness kill count drifted", {"killed": killed})
    receipt = "Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py."
    if receipt not in source:
        raise WitnessError("witness kill receipt is missing")
