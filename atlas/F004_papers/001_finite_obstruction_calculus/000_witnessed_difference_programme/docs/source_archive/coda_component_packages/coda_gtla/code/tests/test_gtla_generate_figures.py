# -*- coding: utf-8 -*-
"""
test_generate_figures.py: Tests publication figure generation for CODA-GTLA.
Verifies file generation, non-trivial binary footprint, and valid image dimensions.

AuthorityEffect: None.
"""

import sys
from pathlib import Path

# Add parent code directory to sys.path
code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from generate_figures import generate_gtla_figure  # noqa: E402


def test_generate_gtla_figure():
    out_file = generate_gtla_figure()
    assert out_file.exists(), "fig1_authority_descent.png must be created"
    stat = out_file.stat()
    assert stat.st_size > 10000, (
        f"Figure file size {stat.st_size} must be substantial (non-trivial)"
    )

    # Verify image dimensions
    try:
        from PIL import Image

        with Image.open(out_file) as img:
            w, h = img.size
            assert w >= 1000, f"Expected width >= 1000, got {w}"
            assert h >= 600, f"Expected height >= 600, got {h}"
    except ImportError:
        pass
