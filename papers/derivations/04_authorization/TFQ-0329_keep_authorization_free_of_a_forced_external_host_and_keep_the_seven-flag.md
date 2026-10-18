# [TFQ-0329] Keep authorization free of a forced external host, and keep the seven-flag

> **Stage**: `AUTHORIZATION` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `0c45bf3f-d7e3-56b1-a95c-4c3fb3c8e5d0`  
> **Parent Derivation**: [TFQ-0328](TFQ-0328_evaluate_a_proposal_against_a_reporting_alphabet_as_a_separate_measurement_with.md)

---

## 1. Abstract & Formal Statement

Chapter 03 is authorization without forced externality. The shelf why_here line says authorization is not treated as requiring an external host, and the book nonclaims repeat that sentence. The local Lean scaffold DescentAuthority.lean opens with the comment that seven boolean flags and their conjunction are not a 5-field descent packet, not CODA-FDA, and not an authorization theorem. HaltGuards carries g_acc, g_det, g_zero_res, g_skel, g_exh, g_no_lift, and g_no_ref. all_guards_required only restates that conjunction. S001-GAP-ATLAS-AND-NOT-FDA remains proposed against this file and halt_guards.py.

### Governing Obligation
Keep authorization free of a forced external host, and keep the seven-flag conjunction from being read as CODA-FDA.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory/lean4/AuthorizationIncompletenessTheory/DescentAuthority.lean`](../../code/lean4/)

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory/python/src/authorization_incompleteness/halt_guards.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory/python/tests_unit/test_halt_guards.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0330](TFQ-0330_terminalize_only_as_authorized_rejected_unresolved_refused_or_not_admitted_and_do.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`, `F000.S001`, `F000.S001:001_authorization_an_incompleteness_theory`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory/book/README.md`
  - `omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory/claims/proposed_gaps.yaml`
  - `omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory/lean4/AuthorizationIncompletenessTheory/DescentAuthority.lean`
