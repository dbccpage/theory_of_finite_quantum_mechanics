# [TFQ-0381] cost-two-first-separation

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `f39dea0e-e068-5840-846a-9de7b7c858cf`  
> **Parent Derivation**: [TFQ-0380](TFQ-0380_readings-left-unselected.md)

---

## 1. Abstract & Formal Statement

PG-GEN-COLLAPSE-AND-FIRST-SEPARATION and ledger row WDP-P000-007 say the first pair-separation task has minimum item cost two in readings L and F over the declared response grammar. Search found deltaU0_valid in Derivation/Minimality.lean. The ledger adds that the theorem has no form-arity bound and that changing the item grammar can change the cost. Genesis paper.md section 7 is the heading. The finite statement still required is that cost-two floor inside the declared grammar, with ties retained rather than removed by an extra judgment. It does not transfer to a different item grammar.

### Governing Obligation
Inside the declared response grammar, the first pair separation has item cost two in both readings, and ties stay.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared candidate space of one-step augmentations (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Minimality is relative to the declared finite candidate space; not a global minimality claim.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: deltaU0_valid inside the declared response grammar`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean::U0_separable`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean::deltaU0_valid`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: minima.rs must record item cost two without dropping ties`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a cost counter in 000_genesis_19l57g1/code/derivation/candidates.py, listed and not opened, scoped to the declared response grammar`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0382](TFQ-0382_refined-minimum-class.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch03_marks_presentations_and_declared_comparisons.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-GEN-COLLAPSE-AND-FIRST-SEPARATION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-GEN-COLLAPSE-AND-FIRST-SEPARATION` (`GENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-GENESIS-PG-GEN-COLLAPSE-AND-FIRST-SEPARATION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [540, -1080, 810]`, `chord_potential = 810`, `holonomy_gamma2 = 1080`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-GEN-COLLAPSE-AND-FIRST-SEPARATION): 4*idx(54) + 3*stage_rank(2) + route_degree(3) == 225` ($\text{value} = 225$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-GEN-COLLAPSE-AND-FIRST-SEPARATION): R_raw(118) - G_cob(58) - S_decoy(2) == 58 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 58$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean::deltaU0_valid`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = bf446d713f355a933f8f546e2219a75a7a2b7eb5307042f0d28c0adc1d773801`
