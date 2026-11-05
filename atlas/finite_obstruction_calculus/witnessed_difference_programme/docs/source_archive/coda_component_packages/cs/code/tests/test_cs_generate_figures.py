# -*- coding: utf-8 -*-
"""
test_generate_figures.py: Tests figure generation for CODA-CS.
AuthorityEffect: None.
"""

from __future__ import annotations

from generate_figures import generate_fig1


def test_figure_generation_output() -> None:
    """Verify that generate_fig1 generates an existing, non-empty PNG file."""
    out_file = generate_fig1()
    assert out_file.exists(), f"Figure {out_file} was not created"
    assert out_file.stat().st_size > 1000, f"Figure {out_file} is suspiciously small ({out_file.stat().st_size} bytes)"
