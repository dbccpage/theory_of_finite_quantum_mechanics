# [TFQ-0279] Finite nonnegative sector weights

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `486b5aed-b305-5b91-afce-acabe62f8328`  
> **Parent Derivation**: [TFQ-0005](../07_l1_emergence/tfq_0005_declared_l1_sector_weights.md)

---

## 1. Abstract & Formal Statement

The finite obligation is to keep a finite sector index and nonnegative weights whose total is positive, with no amplitude attached yet. qm_020_born_normalization_and_conditional_hilbert_lift.md calls that list the declared disjoint-additive observer datum and asks which normalized weight law follows. qm_003_residual_density_calculus_l1_l2_boundary.md records that absolute values plus normalization discard scale, signs, and orientation, so the density is a diagnostic of a chosen representative. AuthorityEffect is None. This node imports nothing: no square root, no complex scalars, and no inner product.

### Governing Obligation
Retain finite nonnegative weights with positive total as the L1 datum and do not attach amplitudes.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- **Primary Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` (zero-axiom, zero-sorry kernel verification in `lean/DerivationDagQMClosure.lean`).

### Sovereign Rust Certifiers
- **Primary Rust Witness**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness` (`code/rust/src/dag_witnesses.rs`, exact `i64`/`BigRational` arithmetic).
- **Python PFP Gate Engine**: `external:sha256:c526457bbf0fece01b6416f1a2524f9499bede37eb02e15a940eec358d6d45b4::verify_dag_prompt_node_reply` (`G0`..`G6`).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0280](tfq_0280_finite_repair_cokernel_as_a_quotient_norm.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`, `F000.S000`
- **Primary Source Paths**:
  - `external:sha256:9504a35b2a33de8f85af42c874eb8da62364cbb364219de602dcfa98b26569e1`
  - `external:sha256:98533bbe8dde6cad1f5bbd9d2de0fb85196b2d44c74964cec5a96620ff69c94f`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-POSITIVE-WEIGHTS-ADMITTED`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-POSITIVE-WEIGHTS-ADMITTED` (`FINITE_QM_CORE` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-FQ-POSITIVE-L1-WEIGHT-ADMISSION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [90, -180, 135]`, `chord_potential = 135`, `holonomy_gamma2 = 180`
- **Finite Shadow Exact Witness (`M4`)**: `sector_weight_partition_sum: w_A(17) + w_B(23) == Phi_1(40)` ($\text{value} = 40$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `even_cycle_C4_minimizer_nonuniqueness: two gauge-equivalent minimizers give sector weights (1,0) vs (0,1) with L1 difference |1-0| + |0-1| == 2` ($\text{value} = 2$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 321911a5814f23a096749af4f70a5fce75f686b981581fab5dd614958375d545`
