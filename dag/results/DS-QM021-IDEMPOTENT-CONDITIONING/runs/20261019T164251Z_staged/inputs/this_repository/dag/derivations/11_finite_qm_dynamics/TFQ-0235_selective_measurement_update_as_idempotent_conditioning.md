# [TFQ-0235] Selective measurement update as idempotent conditioning

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `116f663d-e501-5cd1-a2b4-41eee276a094`  
> **Parent Derivation**: [TFQ-0234](../10_finite_qm_core/TFQ-0234_supplied_hilbert_carrier_after_the_conditional_lift.md)

---

## 1. Abstract & Formal Statement

QM_021, absorbed into Finite Quantum Mechanics as a redirect, obliges a finite conditioning step on nonnegative weights. For a declared sector S with positive mass, the update renormalizes the in-sector weights, is supported on S, and is idempotent, and compatible sectors compose by intersection. Zero sector mass leaves the update undefined; no missing state is manufactured. Ledger group SRC-021 records this as finite Bayesian conditioning on diagonal weights, not as the projection postulate and not as a measurement-problem result. Incompatible non-commuting measurements stay out of scope.

### Governing Obligation
Keep selective update as idempotent conditioning on a declared positive-mass sector, with zero mass left undefined.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `declared outcome partition (observer-relative) (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean mechanization targeted, not delivered (PL-QM037-1); incompatible measurements out of scope (C9).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm021_idempotent_conditioning_and_order_sensitivity`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/measurement.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0236](TFQ-0236_declared_instruments_and_conditional_record_updates.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM021-IDEMPOTENT-CONDITIONING`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM021-IDEMPOTENT-CONDITIONING` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM021-IDEMPOTENT-CONDITIONING`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1430, -2860, 2145]`, `chord_potential = 2145`, `holonomy_gamma2 = 2860`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM021-IDEMPOTENT-CONDITIONING): 4*idx(143) + 3*stage_rank(8) + route_degree(4) == 600` ($\text{value} = 600$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM021-IDEMPOTENT-CONDITIONING): R_raw(326) - G_cob(159) - S_decoy(8) == 159 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 159$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = d06231b338c2fe47154c4ea35cffc0349f5ff779fb83fb45e8b869d61739a1e6`
