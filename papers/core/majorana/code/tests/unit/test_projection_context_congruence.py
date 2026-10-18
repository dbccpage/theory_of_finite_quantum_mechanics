"""Tests for PO-OE-CORE-001: Projection-Context Congruence & Partition Refinement."""

from omega_engine.crates.representation.projection_context_congruence import (
    ProjectionContextCongruenceEngine,
)


def test_dfa_minimization_returning_witness():
    """Test classic 3-state system where S0 and S1 look identical under initial observation,

    but input 'a' transitions S0 -> S2 and S1 -> S0, separating them on step 2.
    """
    states = ["S0", "S1", "S2"]

    # Action generators
    generators = {
        "a": lambda s: {"S0": "S2", "S1": "S0", "S2": "S2"}[s],
        "b": lambda s: {"S0": "S1", "S1": "S1", "S2": "S2"}[s],
    }

    # Protected observation: S0 and S1 emit 0, S2 emits 1
    def obs(s):
        return 0 if s in ("S0", "S1") else 1

    engine = ProjectionContextCongruenceEngine(states, generators, obs)
    result = engine.compute_core_c()

    # Initial blocks: [S0, S1] and [S2]
    assert len(result.initial_blocks) == 2
    # Final blocks: [S0], [S1], [S2] because 'a' separates S0 and S1
    assert len(result.final_blocks) == 3
    assert result.splits_count == 1
    assert len(result.witnesses) == 1

    witness = result.witnesses[0]
    assert witness.state_x == "S0"
    assert witness.state_y == "S1"
    assert witness.context_word == ("a",)
    assert witness.obs_x_after == "1"  # S0 -> S2 emits 1
    assert witness.obs_y_after == "0"  # S1 -> S0 emits 0


def test_no_genesis_boundary_constant_observation():
    """Test Theorem Obligation 8: Core_C(T) = T.

    A constant protected observation produces a single one-class behavioral quotient
    regardless of hidden dynamics. Actions alone cannot recover distinctions after total erasure.
    """
    states = ["x1", "x2", "x3", "x4"]
    generators = {
        "rotate": lambda s: {"x1": "x2", "x2": "x3", "x3": "x4", "x4": "x1"}[s]
    }

    # Constant observation: everything emits 42
    def constant_obs(s):
        return 42

    engine = ProjectionContextCongruenceEngine(states, generators, constant_obs)
    result = engine.compute_core_c()

    assert len(result.initial_blocks) == 1
    assert len(result.final_blocks) == 1
    assert result.splits_count == 0
    assert result.is_invariant is True


def test_partition_refinement_idempotency():
    """Test Theorem Obligation 3: Core_C is idempotent on equivalence relations."""
    states = ["A", "B", "C", "D"]
    generators = {"step": lambda s: {"A": "B", "B": "C", "C": "D", "D": "D"}[s]}

    def obs(s):
        return "even" if s in ("A", "C") else "odd"

    # Pass 1
    engine1 = ProjectionContextCongruenceEngine(states, generators, obs)
    res1 = engine1.compute_core_c()

    # Pass 2 using final blocks as new initial observation mapping
    block_map = {}
    for idx, blk in enumerate(res1.final_blocks):
        for member in blk:
            block_map[member] = idx

    engine2 = ProjectionContextCongruenceEngine(
        states, generators, lambda s: block_map[s]
    )
    res2 = engine2.compute_core_c()

    assert res2.splits_count == 0
    assert len(res2.final_blocks) == len(res1.final_blocks)
    assert res2.is_invariant is True


def test_calculus_discrete_integration_congruence():
    """User prompt test case: calculus problem / integration of function x from 0 to 10.

    Partitioning real line grid points into equivalence classes under shift action.
    """
    # Grid x in 0..10
    grid = list(range(11))
    generators = {
        "dx": lambda x: min(10, x + 1),  # Forward Euler shift
    }

    # Observation: total integrated sum modulo 5
    def total_area_obs(x):
        return (x * (x + 1) // 2) % 5

    engine = ProjectionContextCongruenceEngine(
        grid, generators, total_area_obs, state_id_fn=lambda x: f"x={x}"
    )
    result = engine.compute_core_c()

    assert result.receipt_hash is not None
    assert result.to_dict()["authority_effect"] == "None"


