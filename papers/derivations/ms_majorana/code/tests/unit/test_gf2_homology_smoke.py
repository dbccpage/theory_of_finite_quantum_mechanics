"""Smoke test for decomposed homology/gf2_homology.py and gf2_matrix.py."""
import pytest
from omega_engine.crates.homology_theory.gf2_matrix import GF2Matrix
from omega_engine.crates.homology_theory.gf2_chain_complex import GF2ChainComplex
from omega_engine.crates.homology_theory.gf2_homology import compute_homology, HomologyResult


def test_gf2_matrix_and_homology_smoke():
    d0 = [[1, 0], [1, 1], [0, 1]]
    d1 = [[1, 1, 1]]
    res = compute_homology(d0, d1)
    assert isinstance(res, HomologyResult)
    assert res.dim_C1 == 3
    assert res.rank_D0 == 2


def test_old_coda_homology_import_deleted():
    with pytest.raises(ImportError):
        import omega_engine.crates.coda.homology
    with pytest.raises(ImportError):
        import omega_engine.crates.coda.gf2_matrix


