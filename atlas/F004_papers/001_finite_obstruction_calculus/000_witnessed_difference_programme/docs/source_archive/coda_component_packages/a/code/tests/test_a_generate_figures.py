# -*- coding: utf-8 -*-
"""
test_a_generate_figures.py: Tests figure generation and semantic topology for CODA-A.
AuthorityEffect: None.
"""

import inspect
from pathlib import Path

import generate_figures
from generate_figures import generate_projection_cokernel_figure


def test_projection_cokernel_figure_generation(tmp_path: Path) -> None:
    target = tmp_path / "test_fig1_projection_cokernel.png"
    out = generate_projection_cokernel_figure(target)
    assert out.is_file()
    assert out.stat().st_size > 1000  # valid image file


def test_semantic_figure_arrow_topology() -> None:
    """
    Semantic test (Review M1): Asserts that quotient map q : V -> V/im(C) originates
    from the ambient V box (x <= 0.30) rather than im(C) (x in [0.42, 0.66]),
    and asserts presence of section s and inclusion i : ker(C) -> V.
    """
    source = inspect.getsource(generate_figures.generate_projection_cokernel_figure)

    # 1. Quotient map must originate from V (x <= 0.30), not im(C) (x = 0.66)
    assert "xytext=(0.25, 0.80)" in source, "Quotient map q must originate in ambient V box"
    assert "xy=(0.78, 0.80)" in source, "Quotient map q must land in cokernel box"
    assert "xytext=(0.66, 0.71)" not in source, "Quotient map q must NOT originate in im(C) box"
    assert r"Quotient $q : V \to V / \mathrm{im}(C)$" in source

    # 2. Section s must map from cokernel to kernel
    assert r"Section $s$" in source
    assert "xy=(0.66, 0.45)" in source  # ker(C) right edge
    assert "xytext=(0.76, 0.52)" in source  # cokernel left edge

    # 3. Inclusion i must map from ker(C) to ambient V
    assert r"\iota : \ker(C) \hookrightarrow V" in source
