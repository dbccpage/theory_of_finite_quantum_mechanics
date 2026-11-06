# -*- coding: utf-8 -*-
"""Test figure generation and coordinate correctness for CODA-FOC."""

from pathlib import Path

from generate_figures import generate_figure_1


def test_generate_figure_1(tmp_path: Path):
    target = tmp_path / "test_fig.png"
    out, coords = generate_figure_1(target)
    assert out.exists()
    assert out.stat().st_size > 5000

    # Panel 1: ExactRepair coordinates and arithmetic
    p1 = coords["ExactRepair"]
    assert p1["x"] == (1, 0)
    assert p1["d0_f"] == (-1, 0)
    # Check exact vector equality: r = x + d0 f
    assert p1["r"] == (p1["x"][0] + p1["d0_f"][0], p1["x"][1] + p1["d0_f"][1])
    assert p1["r"] == (0, 0)
    assert p1["phi1"] == 0
    assert p1["gamma2"] == 0

    # Panel 2: CoherentResidual coordinates and arithmetic
    p2 = coords["CoherentResidual"]
    assert p2["x"] == (0, 1)
    assert p2["d0_f"] == (0, 0)
    assert p2["r"] == (p2["x"][0] + p2["d0_f"][0], p2["x"][1] + p2["d0_f"][1])
    assert p2["r"] == (0, 1)
    assert p2["phi1"] == 1
    assert p2["gamma2"] == 0

    # Panel 3: NonclosedDefect coordinates and arithmetic
    p3 = coords["NonclosedDefect"]
    assert p3["x"] == (0, 1)
    assert p3["d0_f"] == (0, 0)
    assert p3["r"] == (p3["x"][0] + p3["d0_f"][0], p3["x"][1] + p3["d0_f"][1])
    assert p3["r"] == (0, 1)
    assert p3["d1_r"] == 1
    assert p3["phi1"] == 1
    assert p3["gamma2"] == 1

