"""Unit tests for omega_engine/carrier/carrier.py conforming to carrier.contract.yaml."""

import pytest
from omega_engine.crates.carrier import (
    Carrier,
    CarrierArtifact,
    CheckedCarrierArtifact,
    verify_carrier_contract,
    CONTRACT_ID,
)


def test_carrier_contract_conformance():
    d0 = [[-1.0, 0.0], [1.0, -1.0], [0.0, 1.0]]
    d1 = [[1.0, 1.0, 1.0]]

    carrier = Carrier(
        c0_dim=2,
        c1_dim=3,
        c2_dim=1,
        d0=d0,
        d1=d1,
        carrier_kind="simplicial_complex",
    )

    assert carrier.c0_dim == 2
    assert carrier.c1_dim == 3
    assert carrier.c2_dim == 1
    assert carrier.verify_chain_law() is True

    artifact = carrier.to_artifact()
    assert isinstance(artifact, CarrierArtifact)
    assert artifact.authority_effect == "EvidenceOnly"
    assert artifact.carrier_kind == "simplicial_complex"

    checked = carrier.check_contract()
    assert isinstance(checked, CheckedCarrierArtifact)
    assert checked.authority_effect == "FactOnly"
    assert checked.is_valid_chain_law is True

    audit = verify_carrier_contract(carrier)
    assert audit["contract_id"] == CONTRACT_ID
    assert audit["is_valid_chain_law"] is True
    assert audit["authority_effect"] == "FactOnly"


def test_invalid_chain_law_rejection():
    d0 = [[1.0, 0.0], [0.0, 1.0]]
    d1 = [[1.0, 1.0]]

    carrier = Carrier(
        c0_dim=2,
        c1_dim=2,
        c2_dim=1,
        d0=d0,
        d1=d1,
    )

    assert carrier.verify_chain_law() is False
    artifact = carrier.to_artifact()
    assert artifact.authority_effect == "EvidenceOnly"
    assert artifact.chain_law_witness is None

    with pytest.raises(ValueError, match="violates chain law d1 ∘ d0 = 0"):
        carrier.check_contract()


