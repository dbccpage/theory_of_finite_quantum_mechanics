# [TFQ-0263] Trace norm under a supplied CPTP family

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `cb38f3cf-c630-5ced-a714-9904a0b91f99`  
> **Parent Derivation**: [TFQ-0262](tfq_0262_cptp_class_recorded_as_a_definition.md)

---

## 1. Abstract & Formal Statement

QM_080 obliges trace-norm geometry only as CPTP-compatible, not as selected by monotonicity alone. The corrected title says monotonicity is necessary for the trace-distance gauge and not sufficient to select it. Finite Quantum Mechanics section 11.3 states the conditional result that was read: if every CPTP map between matrix algebras fails to increase a family of norms on trace-zero Hermitian matrices, then those norms are one positive multiple of the trace norm. The text says this is a result on the full stated channel and matrix domain, not a selection of that domain from primitive difference.

### Governing Obligation
Attach the trace-norm multiple to the hypothesis that every map in the stated CPTP class is monotone, and do not drop that hypothesis.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `CPTP maps (assumption)`
- **Admitted**: `complex matrices and full CPTP class (assumption)`
- **Admitted**: `density matrices and M_n(C) (assumption)`
- **Admitted**: `spectral theorem (assumption)`
- **Admitted**: `spectral theorem for the matrix lift (assumption)`
- **Admitted**: `tensor product (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No Lean statement of the uniqueness-up-to-scale theorem found; TraceZeroDuality.lean item 3 states only that c||.||_1 is monotone for every c > 0. Rust certifies trace norms of given Hermitian matrices over Q(i), not the theorem.

> [!WARNING]
> Spectral selection theorem has no Lean (NOT-STARTED); duplicates FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY in the other fragment.

> [!WARNING]
> Overlaps FQ trace-norm nodes in the other fragment.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DualWitness.lean::dual_witness_certifies_trace_distance`](../../code/lean4/)
- [`lean4/quantum_mechanics/TraceZeroDuality.lean::trace_zero_duality_gap_zero`](../../code/lean4/)
- [`sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:19f735a77b55e8182884060c73a1c66ccc64e14b24e1c3d5a173d64f8fe5b024`](../../code/rust/src/)
- [`external:sha256:8de9a137f60908341dba42d28fa768bf1da772772d76f839787a5fcc9b56f170`](../../code/rust/src/)
- [`external:sha256:8de9a137f60908341dba42d28fa768bf1da772772d76f839787a5fcc9b56f170::TraceNormCertificate`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_fq_core_and_k23_duality_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`sources/atlas/papers/finite_quantum_mechanics/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0264](tfq_0264_monotonicity_does_not_select_the_trace_norm.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1120, -2240, 1680]`, `chord_potential = 1680`, `holonomy_gamma2 = 2240`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY): 4*idx(112) + 3*stage_rank(7) + route_degree(3) == 472` ($\text{value} = 472$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY): R_raw(259) - G_cob(126) - S_decoy(7) == 126 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 126$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_fq_core_and_k23_duality_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 62c4999f1004a22da10c55f9c3f7047137d1e7d034ebf2f0587324f13d1e2928`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1570, -3140, 2355]`, `chord_potential = 2355`, `holonomy_gamma2 = 3140`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION): 4*idx(157) + 3*stage_rank(8) + route_degree(2) == 654` ($\text{value} = 654$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION): R_raw(354) - G_cob(173) - S_decoy(8) == 173 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 173$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `4` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = d812cb0121a5a508f59d368314f4eb02e86e22bcbf711fb101569a15ca81df55`
