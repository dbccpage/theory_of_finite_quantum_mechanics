# [TFQ-0117] GAP-F002-S001-001 remains open. Finite cyclic dual is not sold as a circle

> **Stage**: `CONTINUUM_INTERFACE` | **Status**: `OPEN_ADJOINING`  
> **UUID**: `ff0ea4fe-c64e-54d1-a76e-00b085d050a7`  
> **Parent Derivation**: [TFQ-0111](../19_finite_qg/tfq_0111_the_interface_stays_open_gap_f000_f002_001_and_gap_f002_s001_001_are_not_discharged.md)

---

## 1. Abstract & Formal Statement

named_adjoining.yaml refuses several promotions. Pi is not minted from an exact rational residual. A circle group is not obtained from l1 mass. The dual of a finite cyclic group is that same finite cyclic group, not a circle. Free integers are not forced by an N equals 3 leftover. Pontryagin duality is not derived in the file, and Haar uniqueness does not select the factor two pi. What is finite is the described rational leftover and the refusal list. What is not discharged is a derived circle gauge group and the continuum limit. The gap stays open, and the Einstein equation is not discharged.

### Governing Obligation
GAP-F002-S001-001 remains open. Finite cyclic dual is not sold as a circle group.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F004_papers/007_finite_to_continuum/lean4/CharacterOrthogonality.lean`](../../code/lean4/)

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/007_finite_to_continuum/code/coda_2d_pontryagin.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F002.S001`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F002_continuum/S001_continuum_finite_shadow_bridge`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`GP-IMPORT-CIRCLE-U1`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `GP-IMPORT-CIRCLE-U1` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-GP-CIRCLE-U1-IMPORT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [200, -400, 300]`, `chord_potential = 300`, `holonomy_gamma2 = 400`
- **Finite Shadow Exact Witness (`M4`)**: `sign_fiber_destructive_cancellation: (1 + (-1))^2 == 0 vs (1 + 1)^2 == 4 (gap 4)` ($\text{value} = 4$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `non_exponent_two_satisfied_by_Z3: |Z/3Z| == 3 (finite group of order 3 is not exponent-2 yet is not the circle U(1))` ($\text{value} = 3$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 7c35753fa4028aabc0abad1200143bd785e3fa2d2f5fa1d396f4d05eba145d01`
