# [TFQ-0385] rule-can-erase-separation

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `9fb0a8eb-90af-5459-9ec5-6a157e3e6260`  
> **Parent Derivation**: [TFQ-0384](tfq_0384_cumulative_count_no_return.md)

---

## 1. Abstract & Formal Statement

Ledger row WDP-P000-017 records a counterexample: adding an admitted uniform rule can erase a prior separation. The row names two data, one unary instance on the first, then AdmitRuleAll of index 0, and says raw admission does not enforce requirement-preserving acceptance. The reproducing test was not opened. Genesis paper.md section 8 is the heading for closure. The finite statement still required is that this two-data history remains a visible counterexample beside the no-return count, so a later admission API cannot treat every admitted rule as separation-preserving.

### Governing Obligation
Admitting a uniform rule on two data can erase a prior separation, so raw admission is not requirement-preserving acceptance.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignTfq0385RuleErasesSeparation.lean`](../../../lean4/CampaignTfq0385RuleErasesSeparation.lean) records two data, one unary instance on datum 0, and the class count falling from 2 to 1 when the uniform rule on form 0 is added. The node stays OPEN.
- The opened fragments Inertia.lean and Run.lean are not cited for this counterexample.

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/imposition.rs`](../../code/rust/src/)
- [`absent: missing obligation: imposition.rs must be able to show a rule that drops a prior separation`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py`](../../code/python/)
- [`absent: missing obligation: replay the two-data AdmitRuleAll counterexample from ledger row WDP-P000-017`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch06_residuals_non_factorization_and_authorization_boundaries.md`
