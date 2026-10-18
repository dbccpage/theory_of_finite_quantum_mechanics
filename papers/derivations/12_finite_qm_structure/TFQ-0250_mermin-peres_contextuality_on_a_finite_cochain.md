# [TFQ-0250] Mermin-Peres contextuality on a finite cochain

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `2101fa9a-11bb-5615-9878-a7ea1f3b9a95`  
> **Parent Derivation**: [TFQ-0249](TFQ-0249_trace-zero_summaries_do_not_fix_commutation.md)

---

## 1. Abstract & Formal Statement

QM_120 obliges a Mermin-Peres parity obstruction as a cochain fact on a declared finite packet. DS-QM120-MERMIN-PERES-F2-OBSTRUCTION says the six signed contexts have no global plus-or-minus assignment, because the declared signs multiply to minus one while any global assignment multiplies to plus one, and that every single context and every five-context subset remains satisfiable. The incidence form is an F2 cochain obstruction. The node says this derives neither quantum mechanics nor a Hilbert space.

### Governing Obligation
Record the finite Mermin-Peres parity obstruction on its declared contexts, without deriving a Hilbert space from that packet.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `declared measurement scenarios and contexts (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean names in the ledger (QM.MerminPeres.*) differ from names on disk (see notes).

> [!WARNING]
> Scenario and second measurement context are admitted; the cochain construction does not derive them.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/ContextualityObstruction.lean::d0_of_global_section`](../../code/lean4/)
- [`lean4/quantum_mechanics/ContextualityObstruction.lean::differential_squares_to_zero`](../../code/lean4/)
- [`lean4/quantum_mechanics/ContextualityObstruction.lean::x1_has_no_global_section`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm120_mermin_peres_f2_no_global_section`](../../code/lean4/)
- [`lean4/quantum_mechanics/DualWitness.lean::mermin_peres_parity_obstruction`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/contextuality_obstruction.rs::construct_cabello_scenario`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/kochen_specker.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/parity_context_packet.rs::ParityAdmission`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)

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
