# [TFQ-0350] Assume d1 d0 = 0 only by a declared certificate or the

> **Stage**: `L1_EMERGENCE` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `1524c5dc-3b41-586b-a74d-7aeb9aee7131`  
> **Parent Derivation**: [TFQ-0349](tfq_0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md)

---

## 1. Abstract & Formal Statement

The 003_l1_obstruction_framework claim-ledger header says the obstruction regime is k = 1, truncated. C2 and d1 are not constructed. d1 composed with d0 equal to zero is assumed via declared presheaf functoriality, and it is trivial when section 4 sets C2 to zero. The header says that flatness is not established in that paper. Every cohomology class there denotes the quotient Q1 = C1/im(d0). DAG node L1-CHAIN-D1D0-AXIOM records the same assumption and says whether Genesis or WDP derives flatness is for those fragments to say.

### Governing Obligation
Assume d1 d0 = 0 only by a declared certificate or the simplicial nerve route; the l1 framework ledger does not establish flatness.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `presheaf functoriality / restriction system: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Whether the Genesis / WDP fragments derive flatness is for those fragments to say.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm093_cochain_d1_d0_zero`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/cochains.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0351](tfq_0351_accept_an_integer_finite_list_certificate_only_inside_its_capacity_circulation_feasibility.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-CHAIN-D1D0-AXIOM`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-CHAIN-D1D0-AXIOM` (`L1_EMERGENCE` / `ADMITTED_PRIMITIVE`)
- **Mined Operad Family (`M2`)**: `OP-L1_EMERGENCE-L1-CHAIN-D1D0-AXIOM`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [770, -1540, 1155]`, `chord_potential = 1155`, `holonomy_gamma2 = 1540`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-CHAIN-D1D0-AXIOM): 4*idx(77) + 3*stage_rank(5) + route_degree(6) == 329` ($\text{value} = 329$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-CHAIN-D1D0-AXIOM): R_raw(179) - G_cob(87) - S_decoy(5) == 87 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 87$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 8d6c561e922870346278d836adf7d73b3027fd3fe44655e2eb670a8ea2e1bd01`
