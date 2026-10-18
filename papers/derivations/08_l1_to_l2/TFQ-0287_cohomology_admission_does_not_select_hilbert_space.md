# [TFQ-0287] Cohomology admission does not select Hilbert space

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `6e10f8d0-3251-5aa0-a882-62b26de020f7`  
> **Parent Derivation**: [TFQ-0286](TFQ-0286_descent_census_and_an_open_conjecture.md)

---

## 1. Abstract & Formal Statement

qm_010_hilbert_space_cochains_qm_cohomology.md defines a four-side adapter whose quantum side is an imported finite realization: Hilbert carrier, states, effects, POVMs, Born pairing, channels, and phase data. The finite obligation is admission of a declared cochain, including the complex law that the image of the first differential sits in the kernel of the next, once that law is part of the declaration. The status box says the note does not derive quantum mechanics, Hilbert space, or Born uniqueness. The claim ledger leaves a Lean discharge of that image-in-kernel step open. Cohomology here diagnoses exactness.

### Governing Obligation
Import the Hilbert side of the adapter and leave the cochain Lean discharge open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- **Primary Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` (zero-axiom, zero-sorry kernel verification in `lean/DerivationDagQMClosure.lean`).

### Sovereign Rust Certifiers
- **Primary Rust Witness**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness` (`code/rust/src/dag_witnesses.rs`, exact `i64`/`BigRational` arithmetic).
- **Python PFP Gate Engine**: `omega_engine_pfp/tests/demo_004/finite_qm_derivation_pfp/gates/gate_engine.py::verify_dag_prompt_node_reply` (`G0`..`G6`).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0288](TFQ-0288_pairing_audit_does_not_select_the_born_row.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-PRIM-TO-QM-SELECTION-OPEN`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-PRIM-TO-QM-SELECTION-OPEN` (`FINITE_QM_CORE` / `CONDITIONAL`)
- **Mined Operad Family (`M2`)**: `OP-FQ-PRIM-TO-QM-PARAMETER-GAP`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [100, -200, 150]`, `chord_potential = 150`, `holonomy_gamma2 = 200`
- **Finite Shadow Exact Witness (`M4`)**: `d3_parameter_hierarchy: diag_params(3-1=2) + rebit_params(3*4/2-1=5) + qubit_params(3^2-1=8) == 15` ($\text{value} = 15$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `d3_qubit_minus_diagonal_parameter_gap: (3^2 - 1) - (3 - 1) == 6 unfixed coherence parameters` ($\text{value} = 6$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = afcfb80d98f91d52fe05966a4b8f466848f83f0af6e760fe4672a846036d6192`
