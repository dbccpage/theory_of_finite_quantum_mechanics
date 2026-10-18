# [TFQ-0374] three-recovery-contracts

> **Stage**: `PREGENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `1efaec4d-d31d-52bf-8033-b8d24ef93a4a`  
> **Parent Derivation**: [TFQ-0373](TFQ-0373_free-monoid-size-noniso.md)

---

## 1. Abstract & Formal Statement

Ledger row WDP-P001-009 says language restriction, partial word recovery, and total erasure have different types, with no Ext calculation. Pre-Genesis paper.md section 11.2 is the heading. Opened preservation.py defines recover_word, erase_word, and decimal_decode as separate functions, which does not by itself record that they differ on a new letter. The finite statement still required is a single finite witness, one new letter, on which the three contracts disagree, kept distinct from free-monoid size. WordRecovery.lean is listed in the package and was not opened, so its declarations stay unchecked here.

### Governing Obligation
Language restriction, partial word recovery, and total erasure are three different types, witnessed on one new letter, with no Ext calculation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`missing declaration obligation: three contracts differ on a new letter, file listed and not opened`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/WordRecovery.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: three recovery contracts in crate pre_mssn_preservation that disagree on one new letter`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: one new-letter witness where recover_word, erase_word, and a restriction map return different types`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0375](TFQ-0375_chain-retraction-old-class.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
