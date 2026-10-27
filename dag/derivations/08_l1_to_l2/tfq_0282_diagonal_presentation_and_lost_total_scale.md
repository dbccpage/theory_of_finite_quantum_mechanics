# [TFQ-0282] Diagonal presentation and lost total scale

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `7ff6d204-33dc-5062-a195-8ba75befc1cc`  
> **Parent Derivation**: [TFQ-0281](tfq_0281_residual_mass_to_a_declared_diagonal.md)

---

## 1. Abstract & Formal Statement

The redirect stub qm_004_general_obstruction_management_calculus.md keeps the diagonal presentation of a finite nonnegative mass ledger and the scale identification of ledgers that differ by a positive factor. The finite obligation is that identification: normalization forgets the unnormalized total, and stochastic updates stay on the diagonal in the declared basis. The same stub states that this bookkeeping does not derive complex amplitudes, coherence, Born uniqueness, or physical quantum dynamics.

### Governing Obligation
Record scale-invariant diagonal weights without treating them as complex amplitudes or Born uniqueness.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- **Primary Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` (zero-axiom, zero-sorry kernel verification in `lean/DerivationDagQMClosure.lean`).

### Sovereign Rust Certifiers
- **Primary Rust Witness**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness` (`code/rust/src/dag_witnesses.rs`, exact `i64`/`BigRational` arithmetic).
- **Python PFP Gate Engine**: `external:sha256:c526457bbf0fece01b6416f1a2524f9499bede37eb02e15a940eec358d6d45b4::verify_dag_prompt_node_reply` (`G0`..`G6`).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0283](tfq_0283_finite_matrix_packet_imports_the_pairing.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`, `F000.S000`
- **Primary Source Paths**:
  - `external:sha256:9504a35b2a33de8f85af42c874eb8da62364cbb364219de602dcfa98b26569e1`
  - `external:sha256:98533bbe8dde6cad1f5bbd9d2de0fb85196b2d44c74964cec5a96620ff69c94f`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-OPERATOR-LIFT-TRACE-EMBED-013`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-OPERATOR-LIFT-TRACE-EMBED-013` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-OPERATOR-LIFT-TRACE-EMBED-013`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [780, -1560, 1170]`, `chord_potential = 1170`, `holonomy_gamma2 = 1560`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-OPERATOR-LIFT-TRACE-EMBED-013): 4*idx(78) + 3*stage_rank(6) + route_degree(2) == 332` ($\text{value} = 332$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-OPERATOR-LIFT-TRACE-EMBED-013): R_raw(186) - G_cob(90) - S_decoy(6) == 90 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 90$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 0face75857cc8223b8bce01b8fcb280a13ccdc4fc11ec98872c32bc388ad4b99`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM003-C17-COMPOSABLE-FACTORIZATION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM003-C17-COMPOSABLE-FACTORIZATION` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM003-C17-COMPOSABLE-FACTORIZATION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [960, -1920, 1440]`, `chord_potential = 1440`, `holonomy_gamma2 = 1920`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM003-C17-COMPOSABLE-FACTORIZATION): 4*idx(96) + 3*stage_rank(6) + route_degree(2) == 404` ($\text{value} = 404$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM003-C17-COMPOSABLE-FACTORIZATION): R_raw(222) - G_cob(108) - S_decoy(6) == 108 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 108$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm003_c17_off_diagonal_obstruction_to_diagonal_factorization`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 9a9563bc7afd0ad6ed316acf7626a3bf8fe86041c38d0d5a3428404fcf11b07f`
