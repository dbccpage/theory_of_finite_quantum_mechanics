"""Re-exporting DualWitnessCertifier from certificate crate (Certifier role)."""

from omega_engine.crates.certificate.cert_dual_witness import (
    DualWitnessCert,
    DualWitnessCertifier,
    verify_dual_witness_weak_duality,
    CONTRACT_ID,
)

__all__ = [
    "DualWitnessCert",
    "DualWitnessCertifier",
    "verify_dual_witness_weak_duality",
    "CONTRACT_ID",
]
