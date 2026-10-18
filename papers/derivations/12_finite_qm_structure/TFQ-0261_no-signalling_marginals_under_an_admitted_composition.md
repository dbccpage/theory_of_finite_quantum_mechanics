# [TFQ-0261] No-signalling marginals under an admitted composition

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `62b54714-87e2-599f-b886-e8c81e65daff`  
> **Parent Derivation**: [TFQ-0259](TFQ-0259_finite_chsh_ceiling_on_one_global_joint_table.md)

---

## 1. Abstract & Formal Statement

QM_074 is an annex. Its opened text mints no independent public theorem and sends the load-bearing prose to the finite Bell paper. DS-QM074-NO-SIGNALING-MARGINAL, which was read in the derivation graph, states the finite obligation that remains: in a bipartite conditional distribution, the no-signalling marginal condition holds under an admitted composition rule, and local marginals do not force product factorization. The statement is about admitted tables. Relativistic causality is held aside.

### Governing Obligation
Check no-signalling only as a marginal identity under an admitted composition rule, on declared tables.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `admitted composition rule for subsystems (assumption)`
- **Admitted**: `input independence of remote setting (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> None (NoSignalling.lean, Entanglement.lean, and DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal build under QmCarrierTests).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal`](../../code/lean4/)
- [`lean4/quantum_mechanics/Entanglement.lean::non_signaling_under_local_b_flip`](../../code/lean4/)
- [`lean4/quantum_mechanics/NoSignalling.lean::no_signalling_under_admitted_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/no_signalling.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/no_signalling.rs::no_signalling`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
