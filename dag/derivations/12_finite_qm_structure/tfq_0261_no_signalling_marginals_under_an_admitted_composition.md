# [TFQ-0261] No-signalling marginals under an admitted composition

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `62b54714-87e2-599f-b886-e8c81e65daff`  
> **Parent Derivation**: [TFQ-0259](tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md)

---

## 1. Abstract & Formal Statement

QM_074 is an annex. Its opened text mints no independent public theorem and sends the load-bearing prose to the finite Bell paper. DS-QM074-NO-SIGNALING-MARGINAL, which was read in the derivation graph, states the finite obligation that remains: in a bipartite conditional distribution, the no-signalling marginal condition holds under an admitted composition rule, and local marginals do not force product factorization. The statement is about admitted tables. Relativistic causality is held aside.

### Governing Obligation
Check no-signalling only as a marginal identity under an admitted composition rule, on declared tables.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `admitted composition rule for subsystems (assumption)`
- **Admitted**: `input independence of remote setting (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> None (NoSignalling.lean, Entanglement.lean, and DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal build under QmCarrierTests).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal`](../../code/lean4/)
- [`lean4/quantum_mechanics/Entanglement.lean::non_signaling_under_local_b_flip`](../../code/lean4/)
- [`lean4/quantum_mechanics/NoSignalling.lean::no_signalling_under_admitted_composition`](../../code/lean4/)
- [`sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:e0f586ad94889080d74ad1297fadf59196e4e05cb5b399ef9b7f4d0ae2482c7c`](../../code/rust/src/)
- [`external:sha256:e0f586ad94889080d74ad1297fadf59196e4e05cb5b399ef9b7f4d0ae2482c7c::no_signalling`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`sources/atlas/papers/finite_quantum_mechanics/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM074-NO-SIGNALING-MARGINAL`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM074-NO-SIGNALING-MARGINAL` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM074-NO-SIGNALING-MARGINAL`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1550, -3100, 2325]`, `chord_potential = 2325`, `holonomy_gamma2 = 3100`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM074-NO-SIGNALING-MARGINAL): 4*idx(155) + 3*stage_rank(8) + route_degree(2) == 646` ($\text{value} = 646$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM074-NO-SIGNALING-MARGINAL): R_raw(350) - G_cob(171) - S_decoy(8) == 171 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 171$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = ee4f4c2e371082c9763112dac3e0d9e33f7c2e5d2ac5633fe642c35436860032`
