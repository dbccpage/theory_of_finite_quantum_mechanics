"""Unit tests for the 6-site lattice scaling and GIN involution synthesis.

AuthorityEffect: None.
"""

from __future__ import annotations

from symbol_game_pfp import verify_6site_scaling_gin


def test_6site_lattice_ddc_and_gin_involution():
    """Verify 6-site lattice scaling reproduces exact ground truth and GIN involution."""
    res = verify_6site_scaling_gin()
    assert res["subgraphs"] == 4096
    assert res["configurations"] == 33396
    assert res["cancelling_subgraphs"] == 72
    assert res["surviving_subgraphs"] == 4024
    assert res["meron_distribution"] == {0: 4024, 2: 72}
    assert res["exact_partition_z"] == "33012"
    assert res["transfer_matrix_trace"] == "33012"
    assert res["total_cancelling_pairs"] == 192
    assert res["verified"] is True
