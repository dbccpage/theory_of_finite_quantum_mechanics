# [TFQ-0266] No derivation from stochastic kernels to complete positivity

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `GAP`  
> **UUID**: `bc4061e5-23b4-5fa2-8123-180d87317a10`  
> **Parent Derivation**: [TFQ-0265](tfq_0265_stochastic_population_shadow_of_a_channel.md)

---

## 1. Abstract & Formal Statement

The derivation-graph reading note says no source that was read derives completely positive maps from stochastic kernels. QM_082 records the opposite arrow and a fence: complete positivity, Kraus, Choi, and Stinespring form, and coherence transport, are not forced by the kernel. A positive trace-preserving map can share the identity kernel and still fail complete positivity. DS-CPTP-COMPLETE-POSITIVITY-IMPORT marks complete positivity, the tensor with identity, and the environment extension as assumptions. QM_083 is only the annex for that fence.

### Governing Obligation
Leave the passage from a stochastic kernel to a completely positive map underived, and keep coherence transport imported.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complete positivity (assumption)`
- **Admitted**: `environment extension (assumption)`
- **Admitted**: `tensor product with identity (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open upgrade row: when off-diagonal transport is admissible.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H063CptpChannelsStinespring.lean::stinespring_requires_extension_verified`](../../code/lean4/)
- [`sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:7ecaf8b5a2fd5a4428b83ca6f579e8bda5323dd5ca0b2d87b0138227eb0e5cf3`](../../code/rust/src/)
- [`external:sha256:19f735a77b55e8182884060c73a1c66ccc64e14b24e1c3d5a173d64f8fe5b024`](../../code/rust/src/)
- [`external:sha256:e17359f64c885efb596f3390cf43cc40c25011d24ded59d783982b1eb15318df`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0267](tfq_0267_completely_positive_import_annex.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-CPTP-COMPLETE-POSITIVITY-IMPORT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-CPTP-COMPLETE-POSITIVITY-IMPORT` (`FINITE_QM_STRUCTURE` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-DS-CPTP-CHOI-PARTIAL-TRANSPOSE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [160, -320, 240]`, `chord_potential = 240`, `holonomy_gamma2 = 320`
- **Finite Shadow Exact Witness (`M4`)**: `choi_transpose_trace: Tr(C_T) = 1 + 0 + 0 + 1 == 2` ($\text{value} = 2$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `partial_transpose_negative_minor_det: det([[0,1],[1,0]]) == -1 (positive map T fails complete positivity)` ($\text{value} = -1$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `3` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = ade1abc854da8d288b94131d3cd96e2457d8b706841217d4cac6917d5336c5dd`
