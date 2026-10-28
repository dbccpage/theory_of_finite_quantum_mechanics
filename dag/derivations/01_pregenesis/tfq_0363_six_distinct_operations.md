# [TFQ-0363] six-distinct-operations

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `23f3688a-199b-57d1-8e40-0385eb4c71d2`  
> **Parent Derivation**: [TFQ-0362](tfq_0362_four_host_conditions.md)

---

## 1. Abstract & Formal Statement

PG-SIX-OPERATIONS and historical ledger row WDP-P000-003 require Mention, Supply, Designate, Admit, Retain, and Operate to stay six operations. Opened Pre-Genesis paper.md section 3 and Genesis paper.md section 3 are the cited headings. The DAG statement says only Admit changes admitted state, and that conflating supply with admission is the source of the later Reading L and Reading F split. The finite statement still required is six separately typed operations, with a check that Supply and Designate do not write the admitted regime. No single enum in the opened Python preservation module carries those six names.

### Governing Obligation
Mention, Supply, Designate, Admit, Retain, and Operate stay six operations, and only Admit changes admitted state.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Definitional separation; no theorem is attached to the list itself. The one Lean-checked consequence is supply_no_op (PG-GEN-SUPPLY-NO-OP).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_six_operations_and_primdiff_admission_gate`](../../code/lean4/)
- [`missing declaration obligation: six operation names beside supply_no_op in Derivation/Inertia.lean`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/genesis/lean4/Derivation/Inertia.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: six named operations in wire_primitives rather than one event enum that merges them`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/event.rs`](../../code/rust/src/)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/supply.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: six operation constructors in 000_genesis_19l57g1/code/derivation/model.py, listed but not opened, kept distinct from one another`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0364](tfq_0364_three_trial_record_bound.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`
- **Primary Source Paths**:
  - `external:sha256:9504a35b2a33de8f85af42c874eb8da62364cbb364219de602dcfa98b26569e1`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-SIX-OPERATIONS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-SIX-OPERATIONS` (`PREGENESIS` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-SIX-OPERATIONS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [380, -760, 570]`, `chord_potential = 570`, `holonomy_gamma2 = 760`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-SIX-OPERATIONS): 4*idx(38) + 3*stage_rank(1) + route_degree(3) == 158` ($\text{value} = 158$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-SIX-OPERATIONS): R_raw(81) - G_cob(40) - S_decoy(1) == 40 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 40$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 38fed40f2d484f26814153a4003f9895e1b9a72c3402cfd2f6e78923355036bf`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-GEN-SUPPLY-NO-OP`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-GEN-SUPPLY-NO-OP` (`GENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-GENESIS-PG-GEN-SUPPLY-NO-OP`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [520, -1040, 780]`, `chord_potential = 780`, `holonomy_gamma2 = 1040`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-GEN-SUPPLY-NO-OP): 4*idx(52) + 3*stage_rank(2) + route_degree(4) == 218` ($\text{value} = 218$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-GEN-SUPPLY-NO-OP): R_raw(114) - G_cob(56) - S_decoy(2) == 56 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 56$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `atlas/papers/finite_obstruction_calculus/genesis/lean4/Derivation/Inertia.lean::collapsed_of_no_insts`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = cf82bee9927d85f6ff0f891f4c3a6e49695997befe22c52c4a9c07949462bd0b`
