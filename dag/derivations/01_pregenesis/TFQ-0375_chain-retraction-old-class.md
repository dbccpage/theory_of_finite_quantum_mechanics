# [TFQ-0375] chain-retraction-old-class

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `7c19c8d4-f9c3-52bc-8307-4a73628c5044`  
> **Parent Derivation**: [TFQ-0374](TFQ-0374_three-recovery-contracts.md)

---

## 1. Abstract & Formal Statement

PG-CHAIN-RETRACTION and ledger row WDP-P001-012 say that if chain maps i and r satisfy r composed with i equal to the identity, the induced homology map is injective, so an extension cannot kill an old class by such a retraction. Opened Paper.lean declares chain_retraction_cannot_kill. Homology.lean is listed. Pre-Genesis paper.md sections 13.1 through 13.3 name two isolated points and a triangle with an attached face as instances. The finite statement still required is those two instances inside a declared finite complex and a declared coefficient setting.

### Governing Obligation
A chain retraction cannot kill an old homology class; the two-point graph and the attached triangle stay the named finite instances.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Chain complex over a declared coefficient ring (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Statement is about declared finite complexes; it supplies the 'growth does not repair' direction used by WDP-CH04-N02.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: chain_retraction_cannot_kill on a declared ChainFragment`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Homology.lean::induced_homology_injective`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::chain_retraction_cannot_kill`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::homology_injective_of_chain_retraction`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::triangle_retraction_impossible`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::two_point_retraction_impossible`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: chain-retraction check for the two-point graph and the attached triangle in crate pre_mssn_preservation`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_homology/src/chain_map.rs::CertifiedChainMap`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_homology/src/integral_chain_equivalence.rs::CheckedChainEquivalence`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: graph_homology_ranks on the two named complexes, without a retraction that kills the old class`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0376](TFQ-0376_justified-lift-checklist.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch06_residuals_non_factorization_and_authorization_boundaries.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-CHAIN-RETRACTION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-CHAIN-RETRACTION` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-CHAIN-RETRACTION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [490, -980, 735]`, `chord_potential = 735`, `holonomy_gamma2 = 980`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-CHAIN-RETRACTION): 4*idx(49) + 3*stage_rank(1) + route_degree(3) == 202` ($\text{value} = 202$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-CHAIN-RETRACTION): R_raw(103) - G_cob(51) - S_decoy(1) == 51 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 51$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 08784bcc39c3506a05d523e6ae246d94b8c6e7ccd4077779c6ab872f250e90f1`
