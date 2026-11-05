"""Tests for coupling CAQD adaptive cluster updates with the Lieb-Robinson causal envelope.

AuthorityEffect: None.
"""

from __future__ import annotations

import numpy as np
import pytest
from caqd.adaptive import (
    compute_edge_hop_distance,
    evaluate_causal_envelope_metrics,
    evolve_adaptive,
    is_edge_in_causal_cone,
)
from caqd.spin_chains import (
    TFIMChain,
    XXZChain,
    partial_trace,
    trace_norm,
)

RHO0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
RHO_PLUS = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)


def test_compute_edge_hop_distance_open_and_periodic():
    """Hop distance from edges to source sites on open and periodic chains."""
    # Open chain N=5: edges (0, 1), (1, 2), (2, 3), (3, 4)
    model_open = TFIMChain(num_sites=5, periodic=False)

    # Source at site 0
    assert compute_edge_hop_distance(model_open, (0, 1), [0]) == 0
    assert compute_edge_hop_distance(model_open, (1, 2), [0]) == 1
    assert compute_edge_hop_distance(model_open, (2, 3), [0]) == 2
    assert compute_edge_hop_distance(model_open, (3, 4), [0]) == 3

    # Source at site 2
    assert compute_edge_hop_distance(model_open, (0, 1), [2]) == 1
    assert compute_edge_hop_distance(model_open, (1, 2), [2]) == 0
    assert compute_edge_hop_distance(model_open, (2, 3), [2]) == 0
    assert compute_edge_hop_distance(model_open, (3, 4), [2]) == 1

    # Empty source returns 0
    assert compute_edge_hop_distance(model_open, (0, 1), []) == 0

    # Periodic chain N=5: edge (4, 0) connects 4 and 0
    model_periodic = TFIMChain(num_sites=5, periodic=True)
    assert compute_edge_hop_distance(model_periodic, (4, 0), [0]) == 0
    assert compute_edge_hop_distance(model_periodic, (2, 3), [0]) == 2


def test_is_edge_in_causal_cone_predicates():
    """Edge causal classification under light-cone velocity v_LR."""
    model = TFIMChain(num_sites=5, periodic=False)
    v_lr = 2.0
    sources = [0]

    # At t = 0.0: radius = 0.0
    assert is_edge_in_causal_cone(model, (0, 1), sources, current_time=0.0, v_lr=v_lr) is True
    assert is_edge_in_causal_cone(model, (1, 2), sources, current_time=0.0, v_lr=v_lr) is False
    assert is_edge_in_causal_cone(model, (3, 4), sources, current_time=0.0, v_lr=v_lr) is False

    # At t = 0.5: radius = 1.0
    assert is_edge_in_causal_cone(model, (0, 1), sources, current_time=0.5, v_lr=v_lr) is True
    assert is_edge_in_causal_cone(model, (1, 2), sources, current_time=0.5, v_lr=v_lr) is True
    assert is_edge_in_causal_cone(model, (2, 3), sources, current_time=0.5, v_lr=v_lr) is False

    # At t = 1.5: radius = 3.0
    assert is_edge_in_causal_cone(model, (3, 4), sources, current_time=1.5, v_lr=v_lr) is True

    # Empty source is always in cone
    assert is_edge_in_causal_cone(model, (3, 4), [], current_time=0.0, v_lr=v_lr) is True


def test_causal_adaptive_simulation_prevents_acausal_merging():
    """CAQD with causal envelope bounds prevents cluster merging outside the forward light cone."""
    model = XXZChain(num_sites=4, J=1.0, delta=1.0, h=0.2, periodic=False)
    # Localized excitation at site 0, ground-like state at sites 1, 2, 3
    rho0 = [RHO_PLUS, RHO0, RHO0, RHO0]
    t_span = [0.0, 0.05, 0.1, 0.25]
    v_lr = 2.0

    res = evolve_adaptive(
        model=model,
        rho0=rho0,
        t_span=t_span,
        tol=0.01,
        refine_threshold=0.01,
        v_lr=v_lr,
        source_sites=[0],
    )

    assert res.metadata["causal_filtering_active"] is True
    assert res.metadata["v_lr"] == 2.0
    assert res.metadata["source_sites"] == [0]

    # Evaluate causal envelope metrics
    audit = evaluate_causal_envelope_metrics(res, model, source_sites=[0], v_lr=v_lr)
    assert audit["spacelike_merges_count"] == 0
    assert audit["causal_purity_verified"] is True


def test_unmerged_clusters_outside_causal_cone_retain_marginal_invariance():
    """Distant sites outside the causal cone undergo zero local change, matching Cycle 007 no-signalling."""
    model = TFIMChain(num_sites=4, J=1.0, h=0.0, periodic=False)
    # Perturbation solely at site 0
    rho0 = [RHO_PLUS, RHO0, RHO0, RHO0]
    t_span = [0.0, 0.05, 0.1]
    v_lr = 2.0

    res = evolve_adaptive(
        model=model,
        rho0=rho0,
        t_span=t_span,
        tol=0.05,
        refine_threshold=0.05,
        v_lr=v_lr,
        source_sites=[0],
    )

    # Initial marginals
    init_rho3 = RHO0
    # Site 3 is at distance 3 from site 0. At t = 0.1, v_lr * t = 0.2 < 3.0.
    final_state = res.states[-1]
    final_rho3 = partial_trace(final_state, [3], 4)

    # Local single-site state on site 3 remains undisturbed to high precision
    diff = trace_norm(final_rho3 - init_rho3)
    assert diff == pytest.approx(0.0, abs=1e-8)


def test_causal_input_guards_fail_closed():
    """Causal functions reject non-physical or malformed velocities, times, and sites."""
    model = TFIMChain(num_sites=4, periodic=False)

    # Invalid v_lr
    with pytest.raises(ValueError, match="v_lr must be a positive finite real"):
        is_edge_in_causal_cone(model, (0, 1), [0], 0.1, v_lr=0.0)

    with pytest.raises(ValueError, match="v_lr must be a positive finite real"):
        is_edge_in_causal_cone(model, (0, 1), [0], 0.1, v_lr=-1.5)

    with pytest.raises(ValueError, match="v_lr must be a positive finite real"):
        is_edge_in_causal_cone(model, (0, 1), [0], 0.1, v_lr=True)

    with pytest.raises(ValueError, match="v_lr must be a positive finite real"):
        is_edge_in_causal_cone(model, (0, 1), [0], 0.1, v_lr=float("inf"))

    # Invalid current_time
    with pytest.raises(ValueError, match="current_time must be a nonnegative finite real"):
        is_edge_in_causal_cone(model, (0, 1), [0], current_time=-0.1, v_lr=1.0)

    with pytest.raises(ValueError, match="current_time must be a nonnegative finite real"):
        is_edge_in_causal_cone(model, (0, 1), [0], current_time=True, v_lr=1.0)

    # Invalid causal_margin
    with pytest.raises(ValueError, match="causal_margin must be a nonnegative finite real"):
        is_edge_in_causal_cone(model, (0, 1), [0], 0.1, v_lr=1.0, causal_margin=-0.5)

    # Invalid source_sites in evolve_adaptive
    with pytest.raises(ValueError, match="source_sites must be integers in range"):
        evolve_adaptive(model, [RHO0] * 4, v_lr=1.0, source_sites=[99])

    with pytest.raises(ValueError, match="source_sites must be integers in range"):
        evolve_adaptive(model, [RHO0] * 4, v_lr=1.0, source_sites=[True])

    # Default call without v_lr remains 100% backward compatible
    res_default = evolve_adaptive(model, [RHO0] * 4, t_span=[0.0, 0.1])
    assert res_default.metadata["causal_filtering_active"] is False
    assert res_default.metadata["v_lr"] is None
