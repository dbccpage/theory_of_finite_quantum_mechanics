# [TFQ-0368] index-layer-separation

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `70fe2cf3-e83a-54a3-9e17-7a2c25739f36`  
> **Parent Derivation**: [TFQ-0367](TFQ-0367_listed-history-choice-free-summary.md)

---

## 1. Abstract & Formal Statement

Pre-Genesis paper.md section 6, which was opened, separates S(n), alphabet size k, grammar profile p, atlas target MSS-m, homology degree H_j, and coverage length. Ledger row WDP-P001-001 in 001_sn_mssn/paper_claim_ledger.md says native stages, alphabet indices, profiles, atlas rows, and homological degrees differ, and that the crosswalk does not derive every row. The finite statement still required is that a shared numeral, such as 2 in S(2) and MSS-2, does not identify those objects.

### Governing Obligation
S(n), alphabet size, grammar profile, MSS target, and homology degree remain different quantities even when their numerals coincide.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`missing declaration obligation: separate types for stage index and homology degree in 000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: distinct index newtypes in crate pre_mssn_preservation for stage, alphabet size, profile, and homological degree`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a layer tag on each row of 000_pre_genesis_to_mssn/code/grammar/mssn.ebnf checks so a numeral cannot alias S(n) with MSS-m`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0369](TFQ-0369_finite-demand-count.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch02_primitive_difference_and_finite_carrier.md`
