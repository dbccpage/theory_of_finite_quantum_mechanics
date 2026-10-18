"""Claim-to-executable-evidence matrix for PO-000.

Every claim-ledger identifier is dispositioned here. A disposition records the
strongest Python mechanism available and, separately, whether the general
paper theorem remains outside Python's proof authority.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum

from omega_engine.crates.projection_obstruction.evidence import REQUIRED_CLAIM_IDS, EvidenceKind


class GeneralStatus(StrEnum):
    """Status of the universally quantified paper statement."""

    EXECUTABLE_FINITE = "executable_finite"
    INSTANCE_ONLY = "instance_only"
    PREMISES_ONLY = "premises_only"
    SCOPE_FENCE = "scope_fence"
    PROSE_OR_LEAN = "prose_or_lean"
    DEPENDENCY_ONLY = "dependency_only"


@dataclass
class ClaimMechanization:
    claim_id: str
    mechanism: str
    evidence_kind: EvidenceKind
    general_status: GeneralStatus
    limitation: str


def _claim(
    claim_id: str,
    mechanism: str,
    evidence_kind: EvidenceKind,
    general_status: GeneralStatus,
    limitation: str,
) -> ClaimMechanization:
    return ClaimMechanization(
        claim_id=claim_id,
        mechanism=mechanism,
        evidence_kind=evidence_kind,
        general_status=general_status,
        limitation=limitation,
    )


REQUIRED_LEDGER_CLAIM_IDS = REQUIRED_CLAIM_IDS


CLAIM_COVERAGE = (
    _claim(
        "D8a",
        "quantum lattice simulation bounds",
        EvidenceKind.NUMERICAL_REPLAY,
        GeneralStatus.INSTANCE_ONLY,
        "finite system numerical trajectory replay",
    ),

    _claim(
        "A1",
        "quantum residual and family receipts",
        EvidenceKind.PREMISE_CHECK,
        GeneralStatus.PROSE_OR_LEAN,
        "finite systems and sampled times only",
    ),
    _claim(
        "A2",
        "total observation presentation",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.EXECUTABLE_FINITE,
        "requires every observation map as input",
    ),
    _claim(
        "A3",
        "exact image membership",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.EXECUTABLE_FINITE,
        "finite rational matrices only",
    ),
    _claim(
        "A4",
        "authority field invariant",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.SCOPE_FENCE,
        "metadata invariant, not mathematics",
    ),
    _claim(
        "A5",
        "literal nonclaim regression",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.SCOPE_FENCE,
        "does not establish excluded claims",
    ),
    _claim(
        "A6",
        "host-assumption manifest",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.SCOPE_FENCE,
        "host theory remains imported",
    ),
    _claim(
        "A7",
        "Python evidence-ceiling contract",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.SCOPE_FENCE,
        "finite and numerical receipts are not formal proof",
    ),
    _claim(
        "B1",
        "covering-edge coboundary",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.EXECUTABLE_FINITE,
        "finite rational fibers",
    ),
    _claim(
        "B2",
        "raw l1 edge tally",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.EXECUTABLE_FINITE,
        "finite rational fibers",
    ),
    _claim(
        "B3",
        "projected semigroup counterexample",
        EvidenceKind.EXACT_SYMBOLIC_INSTANCE,
        GeneralStatus.INSTANCE_ONLY,
        "one exact graph-retraction instance",
    ),
    _claim(
        "B4",
        "typed d1 refusal",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.SCOPE_FENCE,
        "native covering-edge data has no C2",
    ),
    _claim(
        "C1",
        "declared chart derivative criterion",
        EvidenceKind.EXACT_SYMBOLIC_INSTANCE,
        GeneralStatus.PROSE_OR_LEAN,
        "instance does not prove Banach theorem",
    ),
    _claim(
        "C2",
        "flat-chart component sanity",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.PROSE_OR_LEAN,
        "general differential geometry is imported",
    ),
    _claim(
        "C3",
        "nonlinear-conjugacy nonclaim",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.SCOPE_FENCE,
        "only affine-coordinate linearity is excluded",
    ),
    _claim(
        "C4",
        "ambient-to-chart bridge refusal",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.PROSE_OR_LEAN,
        "S1 remains open; ambient derivative variation is not a chart criterion",
    ),
    _claim(
        "D1",
        "finite RE1-RE5 equation audit",
        EvidenceKind.FINITE_EXHAUSTIVE,
        GeneralStatus.PROSE_OR_LEAN,
        "exhaustive only on declared exact grid",
    ),
    _claim(
        "D2",
        "singleton decomposition identity",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.PROSE_OR_LEAN,
        "finite pointwise certificate",
    ),
    _claim(
        "D3",
        "weighted local-gauge form audit",
        EvidenceKind.FINITE_EXHAUSTIVE,
        GeneralStatus.PROSE_OR_LEAN,
        "finite declared diagnostic family",
    ),
    _claim(
        "D4",
        "type-orbit swap audit",
        EvidenceKind.FINITE_EXHAUSTIVE,
        GeneralStatus.PROSE_OR_LEAN,
        "finite declared permutation orbits",
    ),
    _claim(
        "D5",
        "unweighted calibration identity",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.PROSE_OR_LEAN,
        "finite pointwise certificate",
    ),
    _claim(
        "D6",
        "lp and scaled countermodels",
        EvidenceKind.COUNTEREXAMPLE,
        GeneralStatus.INSTANCE_ONLY,
        "exact p=2 and c=2 witnesses",
    ),
    _claim(
        "D7",
        "withdrawn-independence fence",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.SCOPE_FENCE,
        "prevents reintroduction of a withdrawn claim",
    ),
    _claim(
        "D8",
        "distinct raw/quotient/repair types",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.EXECUTABLE_FINITE,
        "finite rational presentation",
    ),
    _claim(
        "E1",
        "normalization arithmetic",
        EvidenceKind.EXACT_SYMBOLIC_INSTANCE,
        GeneralStatus.PREMISES_ONLY,
        "matrix norm inequalities remain imported",
    ),
    _claim(
        "E2",
        "support-tangency fixtures",
        EvidenceKind.NUMERICAL_REPLAY,
        GeneralStatus.PROSE_OR_LEAN,
        "finite small-matrix replay",
    ),
    _claim(
        "E3",
        "analytic double-commutator bound refusal",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.PROSE_OR_LEAN,
        "the finite-structural 8g^2 and 24g^2 estimates remain prose-proved",
    ),
    _claim(
        "E4",
        "signed short-time bound replay",
        EvidenceKind.NUMERICAL_REPLAY,
        GeneralStatus.PROSE_OR_LEAN,
        "sampled finite lattices and tolerances",
    ),
    _claim(
        "E5",
        "uniform-family arithmetic",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.PROSE_OR_LEAN,
        "finite prefix; infinite quantifier remains prose",
    ),
    _claim(
        "E6",
        "superseded-route fence",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.SCOPE_FENCE,
        "does not revive Lieb-Robinson route",
    ),
    _claim(
        "E7",
        "global-trace nonidentification",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.SCOPE_FENCE,
        "requires explicit reconstruction hypotheses",
    ),
    _claim(
        "E8",
        "reverse-triangle arithmetic",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.PROSE_OR_LEAN,
        "finite scalar/matrix instances",
    ),
    _claim(
        "E9",
        "uniform-family corollary arithmetic",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.PROSE_OR_LEAN,
        "finite supplied family; infinite quantifier remains prose",
    ),
    _claim(
        "F1",
        "two-qubit closed-form replay",
        EvidenceKind.NUMERICAL_REPLAY,
        GeneralStatus.INSTANCE_ONLY,
        "worked example only",
    ),
    _claim(
        "F2",
        "TFIM edge-rate replay",
        EvidenceKind.NUMERICAL_REPLAY,
        GeneralStatus.INSTANCE_ONLY,
        "finite worked example only",
    ),
    _claim(
        "F3",
        "TFIM incident-load count",
        EvidenceKind.PREMISE_CHECK,
        GeneralStatus.INSTANCE_ONLY,
        "finite declared interaction graph",
    ),
    _claim(
        "G1",
        "typed residual-to-coboundary pipeline",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.EXECUTABLE_FINITE,
        "requires declared observation maps",
    ),
    _claim(
        "G2",
        "higher-cell refusal",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.DEPENDENCY_ONLY,
        "owned by PO-001 and PO-003",
    ),
    _claim(
        "G3",
        "PO-004 dependency fence",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.DEPENDENCY_ONLY,
        "no correlation theorem duplicated here",
    ),
    _claim(
        "G4",
        "PO-005 dependency fence",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.DEPENDENCY_ONLY,
        "only one semigroup witness retained",
    ),
    _claim(
        "H1",
        "raw, watched, and projection-loss tallies",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.EXECUTABLE_FINITE,
        "finite declared observer carriers",
    ),
    _claim(
        "H2",
        "nonempty observer-family validation",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.EXECUTABLE_FINITE,
        "finite declared edge domains",
    ),
    _claim(
        "H3",
        "observer passivity certificate",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.PROSE_OR_LEAN,
        "exact finite instances only",
    ),
    _claim(
        "H4",
        "All-Green joint-kernel certificate",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.PROSE_OR_LEAN,
        "exact finite instances only",
    ),
    _claim(
        "H5",
        "three-patch Local-Green/Global-Red witness",
        EvidenceKind.COUNTEREXAMPLE,
        GeneralStatus.INSTANCE_ONLY,
        "one exact six-edge carrier",
    ),
    _claim(
        "H6",
        "positive rational scaling instances",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.PROSE_OR_LEAN,
        "finite list witnesses the formula, not an analytic modulus",
    ),
    _claim(
        "H7",
        "combined-watcher injectivity certificate",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.PROSE_OR_LEAN,
        "finite rank certificate per declared edge",
    ),
)





