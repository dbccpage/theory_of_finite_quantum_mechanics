# -*- coding: utf-8 -*-
"""
test_or_generate_figures.py: Tests figure generation for CODA-OR with isolated importlib loading.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_test_dir = Path(__file__).resolve().parent
_code_dir = _test_dir.parent
_pkg_root = _code_dir.parent

if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))


def _load_isolated_generate_figures():
    fig_py = _code_dir / "generate_figures.py"
    spec = importlib.util.spec_from_file_location("generate_figures_isolated", fig_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_figure_generation_output_and_semantic_invariants() -> None:
    """Verify figure generation output and assert semantic target-binding invariants."""
    mod = _load_isolated_generate_figures()
    out_file = mod.generate_fig1()
    assert out_file.exists(), f"Figure {out_file} was not created"
    assert out_file.stat().st_size > 1000, f"Figure {out_file} is suspiciously small ({out_file.stat().st_size} bytes)"

    # Verify that the module's semantic inputs enforce target binding
    import pytest
    from coda_or_core import (
        ComparisonObject,
        SupportArrow,
        SupportSieve,
        evaluate_comparison_authority,
    )

    # Certified fixture used in figure has exact target matching
    sieve_cert = SupportSieve(
        target_object_id="X_cert",
        arrows=(
            SupportArrow(
                source_regime_id="Reg_A1",
                target_object_id="X_cert",
                source_has_authority=True,
                certificate_id="chi_A1",
            ),
        ),
    )
    obj_cert = ComparisonObject(
        object_id="X_cert",
        weight_class="finite_bilimit",
        support_sieve=sieve_cert,
        descent_d="D_X",
        verifier_v="V_X",
        terminalizer_tau="tau_X",
    )
    res_cert = evaluate_comparison_authority(obj_cert)
    assert res_cert.inhabited is True
    assert res_cert.refusal_code is None

    # Mismatched target is strictly rejected
    with pytest.raises(ValueError, match="Arrow target 'X_other' does not match sieve target 'X_cert'"):
        SupportSieve(
            target_object_id="X_cert",
            arrows=(
                SupportArrow(
                    source_regime_id="Reg_A1",
                    target_object_id="X_other",
                    source_has_authority=True,
                    certificate_id="chi_A1",
                ),
            ),
        )
