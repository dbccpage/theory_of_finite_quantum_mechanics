# [TFQ-0347] Keep ExactClass, ClosedResidual, and ActiveClosureFailure off the routing terminal, and leave

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `f76090bf-5bc9-5734-bf24-755ac0709657`  
> **Parent Derivation**: [TFQ-0345](TFQ-0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md)

---

## 1. Abstract & Formal Statement

WDP-CH04-N01 says a diagnostic class, a signature value, or a certificate is not a routing terminal, a repair action, a stabilization receipt, or authority. ExactClass is not ExactRepair, and ClosedResidual is not StabilizedSurvivor. WDP-CH04-O01 is conditional: under a declared terminal, lift, and guarded-change policy, independently verified diagnostics feed checked finite routing receipts, and the diagnostic does not select its policy. The ledger binding for O01 is partial. DAG node PG-WDP-DIAGNOSTIC-NOT-ROUTING and route PG-R-DIAG-NOT-ROUTING record that separation.

### Governing Obligation
Keep ExactClass, ClosedResidual, and ActiveClosureFailure off the routing terminal, and leave WDP-CH04-O01 conditional on a declared policy.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Separation is a definitional discipline; WDP-CH04-O01 (diagnostics feed checked finite routing receipts under a declared terminal, lift and guarded-change policy) is CONDITIONAL and only partially ported.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Routing.lean::outside_profile_ne_refuted`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Routing.lean::route`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_types/src/ceiling.rs::EvidenceCeiling`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_types/src/fda.rs::GuardEvidence`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_types/src/routing.rs::RoutingTerminal`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/authority_gap.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/wdp_kernel_check.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`, `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch07_finite_obstruction_calculus.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-WDP-DIAGNOSTIC-NOT-ROUTING`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-WDP-DIAGNOSTIC-NOT-ROUTING` (`WDP` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-WDP-PG-WDP-DIAGNOSTIC-NOT-ROUTING`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [670, -1340, 1005]`, `chord_potential = 1005`, `holonomy_gamma2 = 1340`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-WDP-DIAGNOSTIC-NOT-ROUTING): 4*idx(67) + 3*stage_rank(4) + route_degree(2) == 282` ($\text{value} = 282$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-WDP-DIAGNOSTIC-NOT-ROUTING): R_raw(154) - G_cob(75) - S_decoy(4) == 75 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 75$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = a2b690f493369995c5a6f1294002a9659c048e36233332df40e9a234d316db23`
