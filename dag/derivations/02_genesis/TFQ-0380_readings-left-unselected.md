# [TFQ-0380] readings-left-unselected

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `e50384e9-e0c7-5ba7-b5f5-3452fe47bb35`  
> **Parent Derivation**: [TFQ-0379](TFQ-0379_supply-does-not-admit.md)

---

## 1. Abstract & Formal Statement

Chapter 1 of the S000 book, opened, says two admission readings remain unselected and that the chapter does not select reading L or reading F. The DAG statement on PG-GEN-SUPPLY-NO-OP keeps both: Reading L leaves <> supplied and not admitted, while Reading F admits it as a datum. Genesis paper.md section 7 is the heading for what minimal must include. The finite statement still required is a pair of regimes, or an explicit open branch, rather than a single chosen reading. Selecting one reading would change which datum is present at the first separation, so the branch stays open.

### Governing Obligation
Reading L and Reading F both remain available; neither admission of <> nor its non-admission is selected.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> none.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`missing declaration obligation: both readings remain parameters of the first-separation statements`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::collapsed_of_no_insts`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::supply_no_op`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: reading.rs was listed and not opened; it must not collapse L and F if both are represented`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/reading.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: 000_genesis_19l57g1/code/derivation/model.py must be able to store both readings without a default choice`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0381](TFQ-0381_cost-two-first-separation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch01_genesis_of_difference.md`
