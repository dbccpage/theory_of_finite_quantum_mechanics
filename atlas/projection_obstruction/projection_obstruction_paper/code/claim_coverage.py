"""Claim-to-executable-evidence matrix for PO-000.

Every claim-ledger identifier is dispositioned here. A disposition records the
strongest Python mechanism available and, separately, whether the general
paper theorem remains outside Python's proof authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from evidence import REQUIRED_CLAIM_IDS, EvidenceKind


class GeneralStatus(StrEnum):
    """Status of the universally quantified paper statement."""

    EXECUTABLE_FINITE = "executable_finite"
    INSTANCE_ONLY = "instance_only"
    PREMISES_ONLY = "premises_only"
    SCOPE_FENCE = "scope_fence"
    PROSE_OR_LEAN = "prose_or_lean"
    DEPENDENCY_ONLY = "dependency_only"


@dataclass(frozen=True)
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


PROSE_SUPPLEMENT_CLAIMS = {
    "E-LIMITS": "Theorem 5.7 and Corollary 5.8, §5.10",
    "V65-METRIC": "Theorem 5.9 and Proposition 5.10, §5.11",
    "V65-PURE": "Theorem 5.11, §5.12",
    "V65-SUPPORT": "Proposition 5.13, §5.14",
    "V65-CUMULANT": "Theorem 5.14, §5.14",
    "V65-DENSITY": "Theorem 5.15, §5.15",
    "V65-PHASE": "Theorem 7.5 and Proposition 7.6, §7.5",
    "V65-PREDICTION": "Theorems 7.7 and 7.8, §7.6",
    "V65-OBSERVABILITY": "Theorem 7.9, §7.7",
    "V65-EXTENSION": "Appendix D and Proposition D.1",
    "V66-ONSET": "Theorem 5.16, §5.16",
    "V66-APPLICATIONS": "Corollary 5.17, §5.16",
    "V68-CANCELLATION": "Theorem 5.18 and Proposition 5.19, §5.17",
    "V68-LOCAL-ZERO": "Proposition 5.20, §5.17",
    "V68-PHYSICAL": "Theorem 7.10 and Corollary 7.11, §7.8",
    "V69-JORDAN": "Lemmas E.1--E.3 and Theorem E.4, Appendix E",
    "V69-SELECTOR": "Theorem E.5 and channel reconstruction, Appendix E",
    "V6914-TRACE": "Proposition E.6, Appendix E; separate scoped Lean proof",
    "V6914-CENTER": "Proposition E.7, Appendix E",
}


CHART_PROSE_CLAIMS = (
    ("C4d", "Lemma 3.6 base-dependent shear; Example 3.6 is not a Python witness"),
    ("C4e", "Lemma 3.7 fiber displacement; Example 3.7 is not a Python witness"),
    ("C4f", "Lemma 3.8 parameter chart; Example 3.8 is not a Python witness"),
    ("C4g", "Lemma 3.9 two-chart transition; Example 3.9 is not a Python witness"),
    ("C4h", "Lemma 3.10 left-inverse construction; Example 3.10 is not a Python witness"),
    ("C4i", "Lemma 3.11 parameter-retraction obstruction; Example 3.11 is not a Python witness"),
    ("C4j", "Lemma 3.12 closed-range image retraction; Example 3.12 is not a Python witness"),
    ("C4k", "Lemma 3.13 non-closed range; Example 3.13 is not a Python witness"),
    ("C4l", "Lemma 3.14 linear modulus; Example 3.14 is not a Python witness"),
)


CLAIM_COVERAGE = (
    _claim(
        # 2026-09-03: was bound to "quantum lattice simulation bounds" with a
        # NUMERICAL_REPLAY kind, so a passing trajectory reported evidence for
        # a claim the ledger marks OUT OF SCOPE / NOT ESTABLISHED HERE with
        # evidence "None".  It is now the scope fence it actually is.
        "D8a",
        "repairable-mass R scope fence (R is not defined in this paper)",
        EvidenceKind.STATIC_SCOPE_FENCE,
        GeneralStatus.SCOPE_FENCE,
        "static disclaimer audit; no R theorem is claimed or checked here",
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
        "curved-graph counterexample to unqualified ambient-to-chart transfer",
        EvidenceKind.COUNTEREXAMPLE,
        GeneralStatus.INSTANCE_ONLY,
        "Proposition 3.C; the finite model is the counterexample, not a curved-embedding theorem",
    ),
    _claim(
        "C4a",
        "tangent-restricted affine-subspace chart transfer",
        EvidenceKind.EXACT_SYMBOLIC_INSTANCE,
        GeneralStatus.PROSE_OR_LEAN,
        "Lemma 3.3 is prose; the symbolic witness is Example 3.3 and Remark 3.3.1 only",
    ),
    _claim(
        "C4b",
        "vertical graph chart derivative and noncancellation test",
        EvidenceKind.EXACT_SYMBOLIC_INSTANCE,
        GeneralStatus.PROSE_OR_LEAN,
        "Lemma 3.4 is prose; the symbolic witness is Example 3.4 only",
    ),
    _claim(
        "C4c",
        "constant-shear graph chart derivative",
        EvidenceKind.EXACT_SYMBOLIC_INSTANCE,
        GeneralStatus.PROSE_OR_LEAN,
        "Lemma 3.5 is prose; the symbolic witness is Example 3.5 only",
    ),
    *(
        _claim(
            claim_id,
            mechanism,
            EvidenceKind.NOT_EXECUTABLE,
            GeneralStatus.PROSE_OR_LEAN,
            "Written proof; the recorded example is not a Python witness",
        )
        for claim_id, mechanism in CHART_PROSE_CLAIMS
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
    # 2026-09-03: H1 and H2 were swapped against both ledgers.  The ledger's
    # H1 is the §7.4.1 carrier family and watcher kernels; its H2 is the
    # §7.4.2 tallies, All-Green / Global Red, and visibility gap.  The code
    # had the tallies under H1 and family-nonemptiness under H2, so the
    # claim-to-mechanism mapping was wrong even though the replay happened to
    # exercise both.
    _claim(
        "H1",
        "local observer carrier family and edgewise watcher kernels",
        EvidenceKind.EXACT_FINITE,
        GeneralStatus.EXECUTABLE_FINITE,
        "finite declared observer carriers; nonempty index set validated",
    ),
    _claim(
        "H2",
        "raw, watched, and projection-loss tallies with the visibility gap",
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
    # 2026-09-03: added with the ledger-derived claim universe.  These four
    # rows exist in the markdown ledger and were absent from the hard-coded
    # 47-id tuple, so nothing in the rail had ever considered them.
    _claim(
        "E4-second",
        "Lean product-rule second-derivative assembly (Appendix B)",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.PROSE_OR_LEAN,
        "MECHANIZED-LOCAL in Lean; Python does not verify Lean proofs",
    ),
    _claim(
        "E4-commutator",
        "Lean arithmetic factors 2k and 4k(k+1) only (Appendix B)",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.PROSE_OR_LEAN,
        "arithmetic factors only; the commutator inequalities are paper-resident",
    ),
    _claim(
        "H8",
        "Lean coupled-carrier refutation of joint-kernel necessity (Prop 7.4.7-B)",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.PROSE_OR_LEAN,
        "Lean-mechanized; the manuscript's inline replay is not executed here",
    ),
    _claim(
        "H9",
        "Lean exact quotient witness Phi = 2 on the scalar coupled gauge (§7.4.10)",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.PROSE_OR_LEAN,
        "Lean-mechanized; omega is a declared test cochain, not a §5 residual",
    ),
    _claim(
        "P4-7",
        "minimum linear measurement counts for distinct realization and repair subspaces (Prop 4.7)",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.PROSE_OR_LEAN,
        "prose-proved linear algebra in §4.7",
    ),
    _claim(
        "E3-general",
        "general-order commutator and derivative bounds (Lemma 5.4)",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.PROSE_OR_LEAN,
        "prose-proved general-order commutator estimates in §5.8",
    ),
    _claim(
        "E4-general",
        "general-order short-time lower-bound certificate (Theorem 5.5)",
        EvidenceKind.NOT_EXECUTABLE,
        GeneralStatus.PROSE_OR_LEAN,
        "prose-proved general-order short-time lower bound in §5.8",
    ),
    *(
        _claim(
            claim_id,
            pointer,
            EvidenceKind.NOT_EXECUTABLE,
            GeneralStatus.PROSE_OR_LEAN,
            "Written general proof; exact finite examples do not establish the general claim.",
        )
        for claim_id, pointer in PROSE_SUPPLEMENT_CLAIMS.items()
    ),
)

