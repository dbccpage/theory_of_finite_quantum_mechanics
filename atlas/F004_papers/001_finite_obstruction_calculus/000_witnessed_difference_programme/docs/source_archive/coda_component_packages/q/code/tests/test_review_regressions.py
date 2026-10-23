"""Standalone exact-scalar and immutable-sample regressions."""

import runpy
import sys
from fractions import Fraction
from pathlib import Path

import generate_figures
import pytest
from coda_q_core import SampledSignal, reproduce_sqrt2_picture
from continuum import Enclosure, _validate_exact_rational, sqrt2_enclosure


@pytest.mark.parametrize("value", [True, 0.25, object(), "bad", "1/0"])
def test_continuum_rejects_inexact_or_invalid_scalars(value):
    with pytest.raises(TypeError):
        _validate_exact_rational(value, "endpoint")


@pytest.mark.parametrize("value", [1, "1", Fraction(1)])
def test_continuum_normalizes_exact_scalars(value):
    enclosure = Enclosure(value, "3/2")
    assert enclosure.lower == Fraction(1)
    assert enclosure.upper == Fraction(3, 2)
    assert enclosure.verifies_sqrt2()


def test_sample_storage_is_immutable_and_midpoint_label_is_explicit():
    samples = {0: 1}
    signal = SampledSignal("sample", samples)
    samples[0] = 2
    assert signal.evaluate_at(0) == 1
    with pytest.raises(TypeError):
        signal.samples[Fraction(0)] = 2
    picture = reproduce_sqrt2_picture()
    assert picture["midpoint_self_distance"] == 0
    assert "midpoint_error" not in picture
    assert picture["midpoint"] ** 2 != 2
    assert picture["error_bound"] == sqrt2_enclosure(5).error_bound


def test_figure_default_and_cli_paths_are_reproducible(tmp_path, monkeypatch):
    source = Path(generate_figures.__file__).resolve()
    monkeypatch.setattr(
        generate_figures, "__file__", str(tmp_path / "code" / "generate_figures.py")
    )
    default = generate_figures.generate_fig1()
    assert default.read_bytes().startswith(b"\x89PNG")
    output = tmp_path / "cli.png"
    monkeypatch.setattr(sys, "argv", [str(source), "--output", str(output)])
    runpy.run_path(str(source), run_name="__main__")
    assert output.read_bytes().startswith(b"\x89PNG")
