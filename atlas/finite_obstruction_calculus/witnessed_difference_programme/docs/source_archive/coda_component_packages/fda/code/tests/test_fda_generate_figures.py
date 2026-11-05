# -*- coding: utf-8 -*-
"""Test figure generation for CODA-FDA.
AuthorityEffect: None.
"""

from __future__ import annotations

from generate_figures import generate_fig1


def test_generate_fig1():
    """Ensure schematic figure 1 generates properly and exists on disk."""
    out_path = generate_fig1()
    assert out_path.is_file()
    assert out_path.stat().st_size > 0
