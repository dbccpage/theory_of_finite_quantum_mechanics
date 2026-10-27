# [TFQ-0337] Record homology injectivity under a chain-map retraction, and record that the two-point

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `3b76c446-671f-5473-9007-07bfd137f75f`  
> **Parent Derivation**: [TFQ-0336](tfq_0336_keep_unequal_finite_alphabets_from_a_free_monoid_isomorphism_and_keep_language_restriction.md)

---

## 1. Abstract & Formal Statement

WDP-P001-012 records that a chain-map retraction forces homology injectivity, and that the two-point edge and the filled triangle admit no chain-map retraction fixing the original complex. WDP-P001-011 records that on the two-point graph, H0 counts undirected components and loops do not lower that count. WDP-P001-013 is a definition: chains, cochains, homology, homotopy, and directed reachability are distinct, and a vanishing homology class is not a homotopy contraction. DAG node PG-CHAIN-RETRACTION cites Pre-Genesis lines 493-519 and the Paper001.lean homology symbols. AuthorityEffect is None.

### Governing Obligation
Record homology injectivity under a chain-map retraction, and record that the two-point edge and filled triangle do not retract onto the original complex.

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
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Homology.lean::induced_homology_injective`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Paper.lean::chain_retraction_cannot_kill`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean::homology_injective_of_chain_retraction`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean::triangle_retraction_impossible`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean::two_point_retraction_impossible`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:11c6f3bb8f50e1cc3ffb444f3699282bcbac16b6207a5ecfde9f1a590e26dc33::CertifiedChainMap`](../../code/rust/src/)
- [`external:sha256:f4806506294f8696a4a072d760952f5454185e22ba8ec6ae9eb5ef62d0b154b2::CheckedChainEquivalence`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/code/sn_mssn_checks.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0338](tfq_0338_descend_a_question_to_the_realized_report_image_exactly_when_it_is.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:

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
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 08784bcc39c3506a05d523e6ae246d94b8c6e7ccd4077779c6ab872f250e90f1`
