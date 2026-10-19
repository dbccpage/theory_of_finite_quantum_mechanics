# [TFQ-0132] Trace-norm certificates

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `e5fcbadd-ef0c-58de-be5c-7c8bdbadb584`  
> **Parent Derivation**: [TFQ-0131](tfq_0131_density_operators_over_q_i.md)

---

## 1. Abstract & Formal Statement

Covers trace_norm_certificate.rs, trace_distance_quotient.rs, trace_observer_certificate.rs, and projective_preservers.rs. trace_norm_certificate.rs pins the trace norm of a Hermitian Q(i) matrix by a primal split H = P - N and a dual witness with zero duality gap, refusing an undeclared irrational spectrum. The other files treat trace-zero edge defects on a finite digraph, supplied observer witnesses, and conditional preservers. A Python replay and a Lean 4 declaration would still have to match the zero-gap trace-norm witness.

### Governing Obligation
Match a zero duality gap between the primal split H = P - N and the dual witness, and the refusal of an undeclared irrational spectrum.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/projective_preservers.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/trace_distance_quotient.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/trace_observer_certificate.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for trace_norm_certificate.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM080-IMPORT-FREE-TRACE-NORM-CORE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM080-IMPORT-FREE-TRACE-NORM-CORE` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM080-IMPORT-FREE-TRACE-NORM-CORE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1560, -3120, 2340]`, `chord_potential = 2340`, `holonomy_gamma2 = 3120`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM080-IMPORT-FREE-TRACE-NORM-CORE): 4*idx(156) + 3*stage_rank(8) + route_degree(2) == 650` ($\text{value} = 650$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM080-IMPORT-FREE-TRACE-NORM-CORE): R_raw(352) - G_cob(172) - S_decoy(8) == 172 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 172$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 973e86eed2afbe0161c84f92c4ff28648ad4e792a11449b1f338360b552dc318`
