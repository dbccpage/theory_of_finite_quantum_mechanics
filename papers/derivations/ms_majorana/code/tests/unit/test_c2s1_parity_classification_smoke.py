from __future__ import annotations
"""C2S1-005: Python twin parity classification smoke."""


from pathlib import Path

import pytest

import omega_engine_governance.contracts as omega_contracts
from omega_engine_governance.contracts import contract_corpus
from omega_engine_governance.contracts.build import RustPortPending, load_v1_contracts

PKG = Path(omega_contracts.__file__).resolve().parent
_REPO = Path(__file__).resolve().parents[2]
CLASSIFICATION = (
    _REPO
    / "omega_engine_product_planning_office"
    / "_project_anomalon_codename_woland"
    / "reviews"
    / "2026-09-04_python_contract_foundation_classification.md"
)


def test_package_importable() -> None:
    assert omega_contracts is not None
    assert hasattr(omega_contracts, "__file__")


def test_corpus_paths_nonempty() -> None:
    # Governance is authoritative; no alternate corpus may conceal empty scope.
    paths = contract_corpus.corpus_paths()
    assert paths and all(path.is_relative_to(PKG) for path in paths)


def test_known_stub_rust_port_pending() -> None:
    with pytest.raises(RustPortPending, match="Semantic Python port required for build.rs::load_v1_contracts"):
        load_v1_contracts()


def test_classification_doc_present() -> None:
    assert CLASSIFICATION.is_file()
    text = CLASSIFICATION.read_text(encoding="utf-8")
    assert "SEMANTIC" in text
    assert "STUB" in text
    assert "RustPortPending" in text
    assert "AuthorityEffect" in text


