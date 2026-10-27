# [TFQ-0365] collapsed-observation-barrier

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `d9859fc8-43ad-53a4-903d-2fdeb98dfcca`  
> **Parent Derivation**: [TFQ-0364](tfq_0364_three_trial_record_bound.md)

---

## 1. Abstract & Formal Statement

PG-COLLAPSE-BARRIER records that if two data have equal profiles, no function of that collapsed quotient separates them. Pre-Genesis paper.md section 5 is the DAG source span, and historical row WDP-P000-004 states the written proposition that a task separating a collapsed pair cannot factor through the current quotient. Opened Paper.lean declares collapsed_observation_barrier. The finite statement still required is that separation of one collapsed pair needs an added instance or tag outside the quotient. Chapter 4 of the S000 book says two marks do not supply a report map.

### Governing Obligation
Equal profiles yield no separating function of the collapsed quotient; separation needs data outside that quotient.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Axiom report: see lean4/axiom_report.txt lines 2264-3280 (not individually re-read for this node).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: collapsed_observation_barrier stays tied to equal profiles and does not invent a separating tag`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Paper.lean`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Paper.lean::collapsed_observation_barrier`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a quotient-barrier check in crate pre_mssn_preservation`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a counterexample beside preservation.refine where equal reports yield no separating function`](../../code/python/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0366](tfq_0366_history_report_fiber_criterion.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `external:sha256:e9771151ef2b40fcf062ad0b03605ecdd55eb43a1deb26c90a245b012e93bf2a`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-COLLAPSE-BARRIER`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-COLLAPSE-BARRIER` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-COLLAPSE-BARRIER`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [410, -820, 615]`, `chord_potential = 615`, `holonomy_gamma2 = 820`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-COLLAPSE-BARRIER): 4*idx(41) + 3*stage_rank(1) + route_degree(5) == 172` ($\text{value} = 172$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-COLLAPSE-BARRIER): R_raw(87) - G_cob(43) - S_decoy(1) == 43 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 43$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = c704463448954fae5f061b6ed15e1e4dd177a1de118b3a5d0a871ccb1073df63`
