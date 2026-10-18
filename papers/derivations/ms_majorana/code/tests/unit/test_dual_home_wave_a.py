"""Wave A: dual-home truth table + stub inventory honesty (path-scoped)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from omega_engine_governance.contracts.dual_home_stub_inventory import (
    DEFAULT_PACKAGES,
    scan_packages,
    summary_table,
)
from omega_engine.crates.functional.gamma2 import gamma2
from omega_engine.crates.functional.phi1 import residual_l1
from omega_engine.crates.linear_algebra_theory.basic_matrix import BasicMatrix
from omega_engine.crates.linear_algebra_theory.gram_schmidt_proto import (
    gram_schmidt_columns,
)


PLAYPEN = Path(__file__).resolve().parents[1]
DOCS = PLAYPEN / "omega_engine" / "contracts" / "_docs"
TRUTH = DOCS / "dual_home_truth_table.md"
ENGINE_INV = DOCS / "engine_role_inventory.md"
BASE_POLICY = DOCS / "base_contract_version_policy.md"

REQUIRED_SYMBOLS = (
    "residual_l1",
    "phi1",
    "gamma2",
    "xi",
    "matmul",
    "gram_schmidt",
    "solve_phi",
)

STUB_MIN = {
    "functional": 10,
    "linear_algebra": 15,
    "homology": 20,
    "solver": 40,
    "search": 15,
}
PROTO_MIN = {
    "functional": 8,
    "linear_algebra": 5,
    "homology": 10,
    "solver": 5,
    "search": 1,
}


def test_truth_table_doc_exists() -> None:
    assert TRUTH.is_file(), f"missing Wave A truth table: {TRUTH}"
    text = TRUTH.read_text(encoding="utf-8")
    assert "AuthorityEffect" in text
    assert "Dual-home" in text or "dual-home" in text
    assert "PROTO_LIVE" in text
    assert "STUB_MIRROR" in text


def test_truth_table_lists_required_symbols() -> None:
    text = TRUTH.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SYMBOLS if s not in text]
    assert missing == [], f"truth table missing symbols: {missing}"


def test_related_policy_docs_exist() -> None:
    assert ENGINE_INV.is_file()
    assert BASE_POLICY.is_file()
    policy = BASE_POLICY.read_text(encoding="utf-8")
    assert "Dual-home math law" in policy or "dual-home" in policy.lower()
    assert "urn:omega:execution:engine:v1.0.0" in policy


def test_residual_l1_proto_live() -> None:
    assert residual_l1([1.0, -2.0, 0.5]) == pytest.approx(3.5)
    assert residual_l1([]) == 0.0


def test_gamma2_proto_live() -> None:
    import numpy as np

    d1 = np.array([[1.0, -1.0], [0.0, 1.0]], dtype=float)
    h = np.array([1.0, 1.0], dtype=float)
    res = gamma2(d1, h, tolerance=1e-9)
    assert res.value == pytest.approx(1.0)
    assert res.is_closed is False


def test_matmul_and_gram_schmidt_proto_live() -> None:
    a = BasicMatrix(2, 2, [1.0, 0.0, 0.0, 1.0])
    b = BasicMatrix(2, 2, [2.0, 3.0, 4.0, 5.0])
    c = a.mul(b, zero=0.0)
    assert list(c.data) == [2.0, 3.0, 4.0, 5.0]

    q, path = gram_schmidt_columns([[1.0, 0.0], [1.0, 1.0]])
    assert len(q) == 2
    assert any("gram_schmidt_proto" in p for p in path)
    assert any("PROD_TODO" in p for p in path)


def test_stub_inventory_scanner_runs() -> None:
    reports = scan_packages(DEFAULT_PACKAGES)
    assert len(reports) == len(DEFAULT_PACKAGES)
    table = summary_table(reports)
    assert "functional" in table
    by_name = {r.package: r for r in reports}
    for pkg, min_stub in STUB_MIN.items():
        c = by_name[pkg].counts.get("STUB", 0)
        assert c >= min_stub, f"{pkg}: expected STUB>={min_stub}, got {c}"
    for pkg, min_proto in PROTO_MIN.items():
        c = by_name[pkg].counts.get("PROTO", 0)
        assert c >= min_proto, f"{pkg}: expected PROTO>={min_proto}, got {c}"


def test_truth_table_package_density_section_present() -> None:
    text = TRUTH.read_text(encoding="utf-8")
    assert "Package density" in text
    for pkg in DEFAULT_PACKAGES:
        assert pkg in text or f"`{pkg}" in text or pkg.rstrip("/") in text


def test_engine_must_not_own_residual_in_truth_table() -> None:
    text = TRUTH.read_text(encoding="utf-8")
    assert re.search(r"Engine.*forbids|forbids.*residual|never computes residual", text, re.I)


