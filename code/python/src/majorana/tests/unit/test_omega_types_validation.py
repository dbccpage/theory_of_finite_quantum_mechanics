"""Narrow validation tests for patched omega_types carriers."""

import numpy as np
import pytest

from omega_engine.crates.type.finite_poset import FinitePoset
from omega_engine.crates.type.causal_poset import CausalPoset
from omega_engine.crates.type.banach_presheaf_types import (
    BanachPresheaf,
    BanachStalk,
    RestrictionMap,
)
from omega_engine.crates.type.gauge_types import (
    AnomalyCancellationMetadata,
    AnomalyCancellationResult,
    ConstraintCheckResult,
)
from omega_engine.crates.type.quantum_states import QuantumState


def test_finite_poset_rejects_unknown_edge_endpoint():
    with pytest.raises(ValueError):
        FinitePoset(["a", "b"], [("a", "c")])


def test_finite_poset_valid_and_has_cycle():
    p = FinitePoset(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")])
    assert p.has_cycle() is True
    acyclic = FinitePoset(["a", "b", "c"], [("a", "b"), ("b", "c")])
    assert acyclic.has_cycle() is False


def test_causal_poset_precedes_is_reachability():
    cp = CausalPoset({"a": (0, 0), "b": (1, 0), "c": (2, 0)}, [("a", "b"), ("b", "c")])
    assert cp.precedes("a", "c") is True
    assert cp.precedes("c", "a") is False
    assert cp.precedes("a", "a") is False
    assert cp.comparable("a", "c") is True


def test_banach_validate_shape_mismatch():
    stalks = {"a": BanachStalk(2, "a"), "b": BanachStalk(3, "b")}
    bad = RestrictionMap(np.eye(2), "b", "a")  # wrong shape: expected (2, 3)
    pre = BanachPresheaf(stalks, [("a", "b")], {("a", "b"): bad})
    with pytest.raises(ValueError):
        pre.validate()


def test_banach_validate_accepts_well_formed():
    stalks = {"a": BanachStalk(2, "a"), "b": BanachStalk(3, "b")}
    r = RestrictionMap(np.zeros((2, 3)), "b", "a")
    pre = BanachPresheaf(stalks, [("a", "b")], {("a", "b"): r})
    pre.validate()  # should not raise


def test_gauge_metadata_alias_is_same_container():
    assert AnomalyCancellationMetadata is ConstraintCheckResult
    assert AnomalyCancellationResult is ConstraintCheckResult


def test_quantum_state_rejects_non_finite():
    with pytest.raises(ValueError):
        QuantumState(np.array([1.0, np.inf]))
    QuantumState(np.array([1.0, 0.0]))  # finite is fine


