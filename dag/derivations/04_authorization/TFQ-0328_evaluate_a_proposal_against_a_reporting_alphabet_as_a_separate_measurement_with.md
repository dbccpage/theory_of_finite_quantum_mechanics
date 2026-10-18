# [TFQ-0328] Evaluate a proposal against a reporting alphabet as a separate measurement, with

> **Stage**: `AUTHORIZATION` | **Status**: `SOURCE_RECORD`  
> **UUID**: `36f4588e-841a-5d15-aecf-b72a8d5b8487`  
> **Parent Derivation**: [TFQ-0327](TFQ-0327_keep_proposal_spaces_and_reporting_alphabets_separate_from_the_unjoined.md)

---

## 1. Abstract & Formal Statement

Chapter 02 of EA:000.001.001 is evaluation as a separate measurement from proposal. The shelf admission rule names proposal spaces, reporting alphabets, supplied validity bits, finite terminals, and replay packets. The exit contract asks for a typed claim ledger, source disposition, implementation inventory, local proposed gaps, and explicit P0 and walk nonclaims. Nothing in the opened shelf or book README collapses evaluation into authorization. A supplied validity bit is data for a later terminal, not itself a terminal. AuthorityEffect is None on the shelf header.

### Governing Obligation
Evaluate a proposal against a reporting alphabet as a separate measurement, with a supplied validity bit that is not yet a terminal.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory/lean4/AuthorizationIncompletenessTheory/ReportFactorization.lean`](../../code/lean4/)

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory/python/tests_unit/test_report_factorization.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0329](TFQ-0329_keep_authorization_free_of_a_forced_external_host_and_keep_the_seven-flag.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`, `F000.S001`, `F000.S001:001_authorization_an_incompleteness_theory`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory/book/README.md`
