"""Public boundary/lifecycle and independent rational controls for CLI adapters.

No physical constant, Lean theorem or delegated suite is certified by these tests.
"""
from contextlib import redirect_stderr, redirect_stdout
from fractions import Fraction
import importlib
import io
from itertools import product
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import src.bin as ray
from src.bin import entropy_cli as collision
from src.bin import finite_cli as trace
import src.finite_probability as mass


class HostileTuple(tuple):
    def __iter__(self):
        raise RuntimeError("must refuse before user iteration")

    def __len__(self):
        raise RuntimeError("must refuse before user length")


class OverridingInt(int):
    def __add__(self, other):
        return 0.5


class OverridingFraction(Fraction):
    def __mul__(self, other):
        return 0.5


class HostileString(str):
    def __len__(self):
        raise RuntimeError("must refuse before user string callbacks")


@pytest.mark.parametrize("operation, error, argument", [
    (ray.ray_power_two, ray.BinWitnessError, HostileTuple((1, 0, 0))),
    (collision.collision_probability, collision.ParityError, HostileTuple((1,))),
    (mass.integer_mass, mass.ScaledSimplexError, HostileTuple((1, 0))),
])
def test_hostile_container_callbacks_are_not_run(operation, error, argument):
    with pytest.raises(error, match="container subclass refused"):
        operation(argument)


@pytest.mark.parametrize("scalar", [OverridingInt(1), OverridingFraction(1)])
def test_closed_scalar_admission(scalar):
    with pytest.raises(ray.BinWitnessError, match="not an exact rational"):
        ray.ray_power_two((scalar, 0, 0))
    with pytest.raises(collision.ParityError, match="not an exact rational"):
        collision.collision_probability((scalar,))
    with pytest.raises(mass.ScaledSimplexError, match="not an integer"):
        mass.integer_mass((scalar, 0))
    with pytest.raises(trace.CliTraceError, match="not an integer"):
        trace.cli_identity_trace(scalar)


def test_declared_budgets_match_the_contract():
    assert ray.MAX_SCALAR_BITS == mass.MAX_WEIGHT_BITS == collision.MAX_SCALAR_BITS == 1024
    assert (collision.MAX_OUTCOMES, collision.MAX_WORK_BITS) == (4096, 8192)
    assert (trace.MAX_IDENTITY_DIMENSION, trace.MAX_ARGUMENTS, trace.MAX_ARGUMENT_CHARACTERS) == (256, 64, 4096)


def test_admitted_upper_bit_edge_and_refusal_without_big_integer_rendering():
    edge = (1 << 1024) - 1
    assert ray.ray_power_two((edge, 0, 0)) == Fraction(edge * edge)
    assert mass.integer_mass((edge, edge)) == 2 * edge
    rejected = [1 << 1024, -(1 << 20000), Fraction((1 << 1024) + 1, 2), Fraction(1, 1 << 1024)]
    for value in rejected:
        with pytest.raises(ray.BinWitnessError, match="bit budget exceeded"):
            ray.ray_power_two((value, 0, 0))
        with pytest.raises(collision.ParityError, match="bit budget exceeded"):
            collision.collision_probability((value,))
    for value in rejected[:2]:
        with pytest.raises(mass.ScaledSimplexError, match="bit budget exceeded"):
            mass.integer_mass((value, 0))
    with pytest.raises(trace.CliTraceError, match="dimension budget exceeded"):
        trace.cli_identity_trace(-(1 << 20000))


def test_vector_and_work_budgets(monkeypatch):
    assert collision.collision_probability((1,) + (0,) * 4095) == Fraction(1)
    with pytest.raises(collision.ParityError, match="vector budget exceeded"):
        collision.collision_probability((1,) + (0,) * 4096)
    monkeypatch.setattr(collision, "MAX_WORK_BITS", 2)
    # Mass totals fit 2 bits; the first squared denominator, 9, needs 4 bits.
    with pytest.raises(collision.ParityError, match="bit budget exceeded"):
        collision.collision_probability((Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)))
    # The running mass 1/2+1/3=5/6 needs 3 bits before collision work begins.
    with pytest.raises(collision.ParityError, match="bit budget exceeded"):
        collision.collision_probability((Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)))


def test_resource_refusal_precedes_identity_provider(monkeypatch):
    class MustNotAllocate:
        @staticmethod
        def identity(size):
            raise AssertionError("oversized request reached the allocator")
    monkeypatch.setattr(trace, "ExactMatrix", MustNotAllocate)
    with pytest.raises(trace.CliTraceError, match="dimension budget exceeded"):
        trace.cli_identity_trace(257)


def test_real_identity_provider_at_boundaries():
    for dimension in [0, 1, 2, 3, 16, 256]:
        result = trace.cli_identity_trace(dimension)
        assert type(result) is Fraction
        assert result == Fraction(dimension)


def test_provider_failure_has_typed_context(monkeypatch):
    from src.linear_algebra.matrix import MatrixFailure
    class RefusingProvider:
        @staticmethod
        def identity(size):
            raise MatrixFailure("provider fixture refusal")
    monkeypatch.setattr(trace, "ExactMatrix", RefusingProvider)
    with pytest.raises(trace.CliTraceError, match="identity matrix provider failed") as caught:
        trace.cli_identity_trace(1)
    assert isinstance(caught.value.__cause__, MatrixFailure)
    assert caught.value.parameters == {"provider_error": "MatrixFailure"}


def test_provider_cannot_supply_overriding_diagonal_scalars(monkeypatch):
    eye = trace.ExactMatrix.identity(1)
    eye.data[0] = OverridingFraction(1)
    class UnsafeProvider:
        @staticmethod
        def identity(size):
            return eye
    monkeypatch.setattr(trace, "ExactMatrix", UnsafeProvider)
    with pytest.raises(trace.CliTraceError, match="not an exact rational"):
        trace.cli_identity_trace(1)


def test_generated_exact_controls():
    for scale in range(1, 8):
        for a, b, c in product(range(-2, 3), repeat=3):
            result = ray.ray_power_two((Fraction(a, scale), Fraction(b, scale), Fraction(c, scale)))
            assert type(result) is Fraction
            assert result == Fraction(a * a + b * b + c * c, scale * scale)
        for a in range(scale + 1):
            result = collision.collision_probability((Fraction(a, scale), Fraction(scale - a, scale)))
            assert type(result) is Fraction
            assert result == Fraction(a * a + (scale - a) * (scale - a), scale * scale)
    for a, b in product(range(-16, 17), repeat=2):
        assert mass.integer_mass((a, b)) == a + b


@pytest.mark.parametrize("provider", [ray, collision, mass])
@pytest.mark.parametrize("error", [BrokenPipeError, ValueError])
def test_closed_or_broken_stdout_is_graceful(provider, error):
    class BrokenStream(io.StringIO):
        def write(self, text):
            raise error("output unavailable")
    with redirect_stdout(BrokenStream()):
        assert provider.main() == 2


def test_witness_output_remains_exact():
    for provider, expected in [(ray, "1\n"), (collision, "1/2\n"), (mass, "1\n")]:
        output = io.StringIO()
        with redirect_stdout(output):
            assert provider.main() == 0
        assert output.getvalue() == expected


@pytest.mark.parametrize("arguments", [HostileTuple(("list",)), "list", [True],
                                      [HostileString("list")], ["list"] * 65, ["x" * 4097]])
def test_bad_command_arguments_do_not_reach_dispatch(monkeypatch, arguments):
    def should_not_run(args):
        raise AssertionError("invalid argument reached dispatch")
    monkeypatch.setattr(trace, "_dispatch", should_not_run)
    assert trace.main(arguments) == 2


def test_adapter_detaches_arguments_and_checks_status(monkeypatch):
    arguments = ["list", "--json"]
    def mutating_dispatch(values):
        values.clear()
        return 0
    monkeypatch.setattr(trace, "_dispatch", mutating_dispatch)
    assert trace.main(arguments) == 0
    assert arguments == ["list", "--json"]
    for status in [None, True, "0", -1, 3]:
        monkeypatch.setattr(trace, "_dispatch", lambda args, status=status: status)
        assert trace.main(["list"]) == 2
    for status in [0, 1, 2]:
        monkeypatch.setattr(trace, "_dispatch", lambda args, status=status: status)
        assert trace.main(["list"]) == status


def test_parser_and_cli_composition():
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        assert trace.main(["--help"]) == 0
        assert trace.main([]) == 2
        assert trace.main(["unknown-command"]) == 2
        assert trace.main(["evidence", "check", "--project-root", str(Path.cwd())]) == 2
        output = io.StringIO()
        with redirect_stdout(output):
            assert trace.main(["list", "--json"]) == 0
        assert type(json.loads(output.getvalue())) is list


def test_module_exit_preserves_reported_failure():
    root = Path(__file__).resolve().parents[3]
    result = subprocess.run([sys.executable, "-B", "-m", "src.bin.finite_cli", "evidence", "check",
                             "--project-root", str(root)], cwd=root, capture_output=True, text=True,
                            env={**os.environ, "PYTHONPATH": str(root / "code/python")}, timeout=30)
    assert result.returncode == 2
    assert result.stderr.strip() == "SOURCE_MANIFEST_REQUIRED"
