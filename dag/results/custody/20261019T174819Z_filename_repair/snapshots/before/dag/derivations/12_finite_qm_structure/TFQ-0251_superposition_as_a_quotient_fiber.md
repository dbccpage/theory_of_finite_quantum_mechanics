# [TFQ-0251] Superposition as a quotient fiber

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `c2791f94-d9a9-5862-8be4-e42de055171f`  
> **Parent Derivation**: [TFQ-0234](../10_finite_qm_core/TFQ-0234_supplied_hilbert_carrier_after_the_conditional_lift.md)

---

## 1. Abstract & Formal Statement

QM_060 obliges superposition to be read as the fiber of a phase-blind quotient, not as a new probability mass. Under a supplied lift that attaches a phase to a square root of a weight, the squared modulus repeats the weight, and the phase sits in the kernel of the population map. DS-QM060-SUPERPOSITION-QUOTIENT-FIBER records the finite witness that two opposite phases can share a quotient point and still differ in the fiber, so a later mixing step can see a cross term. The paper header calls this a component note of the ingredient ladder and says the fiber is observer-relative.

### Governing Obligation
Place relative phase in the fiber of the phase-blind quotient and do not count that fiber as extra probability mass.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Gaussian-integer/rational amplitude vectors (assumption)`
- **Admitted**: `U(1) phase carrier (assumption)`
- **Admitted**: `complex amplitude lift c_gamma with unit phases (lift)`
- **Admitted**: `finite phase group for fiber enumeration (assumption)`
- **Admitted**: `quadratic readout |.|^2 (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Reuse of upstream theorem; no new derivation of the lift.

> [!WARNING]
> Readout |c|^2 and amplitude vectors are declared; the fiber is a property of that readout, not derived from a bare difference.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm060_061_phase_fiber_and_interference_non_descent`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/H008PhaseBlindPresentation.lean::weight_nonneg`](../../code/lean4/)
- [`lean4/quantum_mechanics/H009PhaseFiber.lean::global_phase_in_fiber`](../../code/lean4/)
- [`lean4/quantum_mechanics/H009PhaseFiber.lean::phasePD_zeroRel_iff`](../../code/lean4/)
- [`lean4/quantum_mechanics/H009PhaseFiber.lean::phase_fiber`](../../code/lean4/)
- [`lean4/quantum_mechanics/H009PhaseFiber.lean::relative_phase_in_fiber`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs::averages_to_dephasing`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs::phase_blind_projection`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs::phase_equivalent`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0252](TFQ-0252_interference_as_a_resource_outside_l1_bookkeeping.md)
- [TFQ-0253](TFQ-0253_conditional_complex-carrier_selector.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM060-SUPERPOSITION-QUOTIENT-FIBER`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM060-SUPERPOSITION-QUOTIENT-FIBER` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM060-SUPERPOSITION-QUOTIENT-FIBER`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1440, -2880, 2160]`, `chord_potential = 2160`, `holonomy_gamma2 = 2880`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM060-SUPERPOSITION-QUOTIENT-FIBER): 4*idx(144) + 3*stage_rank(8) + route_degree(4) == 604` ($\text{value} = 604$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM060-SUPERPOSITION-QUOTIENT-FIBER): R_raw(328) - G_cob(160) - S_decoy(8) == 160 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 160$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm060_061_phase_fiber_and_interference_non_descent`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-chat-v3-0324` | `status = PASS` | `receipt_sha256 = eaa1b2c17f0c9b49d36d0f8789a561470d29530c6f7a51c889884a44b48d89ed`
