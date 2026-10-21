"""
majorana_evaluator.py — Re-exporting façade for the modular Majorana evaluation engine.

Decomposed into:
- ``majorana_f2_trichotomy``: GF(2) matrix arithmetic, cochains, trichotomy, and Tetron carriers.
- ``majorana_mzm_ising``: Kitaev sweet-spot chain, Ising fusion algebra, and parity invariants.
- ``majorana_transfer_bounds``: Open-system Lindblad, non-Markovian bath, and cross-junction bounds.

AuthorityEffect: None.
"""

from __future__ import annotations

try:
    from .majorana_f2_trichotomy import (
        _CLASSIFY_BUDGET,
        F2CochainComplex,
        GF2Matrix,
        TetronCarrier,
        TrichotomyClass,
        _stored_bit,
        _vector_bits,
        build_tetron_carrier,
        classify_residual,
        compute_coset_weight,
        logical_representative,
        verify_norm_equivalence,
    )
    from .majorana_mzm_ising import (
        IsingFusionAlgebra,
        KitaevSweetSpotChain,
        ParityAlgebraModel,
        audit_legacy_carrier,
        compute_skew_pfaffian,
        pfaffian_z2_invariant,
    )
    from .majorana_transfer_bounds import (
        ContinuumCrossJunctionFemModel,
        DetectorAdequacyAudit,
        DetectorAdequacyReceipt,
        MultiTerminalTransferReceipt,
        NonMarkovianBosonicBathModel,
        NonMarkovianTransferReceipt,
        OpenSystemMajoranaBraidModel,
        TransferBoundReceipt,
    )
except (ImportError, ValueError):
    from majorana_f2_trichotomy import (
        _CLASSIFY_BUDGET,
        F2CochainComplex,
        GF2Matrix,
        TetronCarrier,
        TrichotomyClass,
        _stored_bit,
        _vector_bits,
        build_tetron_carrier,
        classify_residual,
        compute_coset_weight,
        logical_representative,
        verify_norm_equivalence,
    )
    from majorana_mzm_ising import (
        IsingFusionAlgebra,
        KitaevSweetSpotChain,
        ParityAlgebraModel,
        audit_legacy_carrier,
        compute_skew_pfaffian,
        pfaffian_z2_invariant,
    )
    from majorana_transfer_bounds import (
        ContinuumCrossJunctionFemModel,
        DetectorAdequacyAudit,
        DetectorAdequacyReceipt,
        MultiTerminalTransferReceipt,
        NonMarkovianBosonicBathModel,
        NonMarkovianTransferReceipt,
        OpenSystemMajoranaBraidModel,
        TransferBoundReceipt,
    )

__all__ = [
    "_CLASSIFY_BUDGET",
    "F2CochainComplex",
    "GF2Matrix",
    "TetronCarrier",
    "TrichotomyClass",
    "_stored_bit",
    "_vector_bits",
    "build_tetron_carrier",
    "classify_residual",
    "compute_coset_weight",
    "logical_representative",
    "verify_norm_equivalence",
    "KitaevSweetSpotChain",
    "IsingFusionAlgebra",
    "ParityAlgebraModel",
    "compute_skew_pfaffian",
    "pfaffian_z2_invariant",
    "audit_legacy_carrier",
    "TransferBoundReceipt",
    "OpenSystemMajoranaBraidModel",
    "DetectorAdequacyReceipt",
    "DetectorAdequacyAudit",
    "NonMarkovianTransferReceipt",
    "NonMarkovianBosonicBathModel",
    "MultiTerminalTransferReceipt",
    "ContinuumCrossJunctionFemModel",
]
