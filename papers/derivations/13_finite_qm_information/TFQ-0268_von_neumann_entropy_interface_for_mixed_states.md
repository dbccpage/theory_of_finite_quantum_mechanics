# [TFQ-0268] Von Neumann entropy interface for mixed states

> **Stage**: `FINITE_QM_INFORMATION` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `7b2bc254-f9f6-576e-a1a1-854169dbe824`  
> **Parent Derivation**: [TFQ-0262](../12_finite_qm_structure/TFQ-0262_cptp_class_recorded_as_a_definition.md)

---

## 1. Abstract & Formal Statement

Finite Quantum Mechanics section 5 lists the transcendental von Neumann entropy interface as an open boundary. For a non-pure density operator with an algebraic spectrum, the natural-log entropy is described as a nonzero algebraic linear combination of logarithms, and Baker's theorem is the cited reason for calling that value transcendental. The claim is unit-sensitive: the base-two entropy of the maximally mixed qubit state is the integer one, so the text does not extend the transcendental reading to every base. The declared external interface is a certified rational enclosure of stated width.

### Governing Obligation
Keep mixed-state natural-log entropy outside the cyclotomic field unless a Baker hypothesis and a rational enclosure are both declared.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Baker theorem on linear forms in logarithms (assumption)`
- **Admitted**: `real logarithm (lift)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> C750Purity.lean and polynomial Renyi-2 purity dichotomy build under QmCarrierTests; transcendence of mixed von Neumann entropy remains conditional on the Baker hypothesis.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/C750Purity.lean::mixed_entropy_is_transcendental`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_entropy_purity_and_ds_qm034_051_cayley_clifford_witness`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census`](../../code/lean4/)
- [`lean4/quantum_mechanics/EntropyDichotomy.lean::entropy_zero_iff_pure`](../../code/lean4/)
- [`lean4/quantum_mechanics/EntropyDichotomy.lean::mixed_entropy_positive`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/entropy.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_entropy.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_entropy.rs::CitedAnchor`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_entropy.rs::RationalSpectrum`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche8_tensor_stone_continuum_embedding_and_leftover_mnc_witness`](../../code/rust/src/)

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

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-ENTROPY-DICHOTOMY-BAKER`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-ENTROPY-DICHOTOMY-BAKER` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-ENTROPY-DICHOTOMY-BAKER`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1250, -2500, 1875]`, `chord_potential = 1875`, `holonomy_gamma2 = 2500`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-ENTROPY-DICHOTOMY-BAKER): 4*idx(125) + 3*stage_rank(7) + route_degree(2) == 523` ($\text{value} = 523$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-ENTROPY-DICHOTOMY-BAKER): R_raw(285) - G_cob(139) - S_decoy(7) == 139 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 139$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_embedding_relativity_and_entropy_baker_dichotomy_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4-flash` | `status = PASS` | `receipt_sha256 = 38df70300b0b3b490a97a0d11f5f42a379fc4d640287b3a5cb3757a64b369a54`
