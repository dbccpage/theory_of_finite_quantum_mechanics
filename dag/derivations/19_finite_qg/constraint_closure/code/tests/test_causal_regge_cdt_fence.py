"""Tests for the declared quadratic spike-suppression fixture.

AuthorityEffect: None.
"""

import sys
import os

import numpy as np
import pytest

from causal_regge_cdt_fence import (
    bare_action_density,
    effective_causal_action,
    compare_action_profiles,
    mcmc_causal_comparison,
)


class TestCausalReggeCDT:
    def test_bare_action_plunges(self):
        """Bare action plunged for large k."""
        assert bare_action_density(20) < bare_action_density(6)

    def test_causal_action_stabilizes_minimum_at_6(self):
        """With the supplied penalty, S_eff(k) is minimal at k=6 on [3, 20]."""
        S_6 = effective_causal_action(6)
        for k in range(3, 21):
            if k != 6:
                assert effective_causal_action(k) > S_6, (
                    f"S_eff({k}) = {effective_causal_action(k)} <= S_eff(6) = {S_6}"
                )

    def test_compare_action_profiles(self):
        result = compare_action_profiles(k_max=20)
        assert result["bare_minimum_k"] == 20
        assert result["causal_minimum_k"] == 6
        assert result["causal_stabilized"]

    def test_mcmc_spike_suppression(self):
        result = mcmc_causal_comparison(n_steps=50_000, k_range=(3, 20))
        assert result["unconstrained_k6_fraction"] < 0.05
        assert result["unconstrained_runaway_fraction"] > 0.90
        assert result["causal_k6_fraction"] > 0.70
        assert result["causal_runaway_fraction"] < 0.05
        assert result["spike_suppressed"]
        assert result["runaway_eliminated"]
