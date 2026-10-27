# [TFQ-0160] Import finite maps QM-207 to QM-215

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `512fb3b6-86bd-59d7-954b-da1426928162`  
> **Parent Derivation**: [TFQ-0131](tfq_0131_density_operators_over_q_i.md)

---

## 1. Abstract & Formal Statement

Covers quantum_import_finite_maps.rs, quantum_import_finite_maps/algebraic_bound_state_spectra.rs, and quantum_import_finite_maps/foundational_derivation_closure.rs. The facade states exact finite-map controls for QM-207 through QM-215. algebraic_bound_state_spectra.rs is the QM-217 Kravchuk and so(4) hydrogen finite spectra. foundational_derivation_closure.rs is the 5 by 5 import-independence countermodel matrix and the Z[zeta_12] Sorkin readout class. Electroweak, QCD, and continuum-named siblings stay outside this node. A Python replay and a Lean 4 declaration would still have to match that 5 by 5 matrix.

### Governing Obligation
Match the 5 by 5 single-system import-independence countermodel matrix in the QM-219 closure.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579`](../../code/rust/src/)
- [`external:sha256:a10da92df13ef926419410d2e5c98c7366f31aa5dd28fa48718916ad8f904b62`](../../code/rust/src/)
- [`external:sha256:73ff1307c7f46b2f7648dd055f2db749abcaa4b8ab76c43fa35099fb1cd20ed4`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/algebraic_bound_state_spectra_control.py`](../../code/python/)
- [`sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/foundational_derivation_closure_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0161](tfq_0161_finite_expressibility_and_measurement.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-QM207-231-FINITE-MAP-CONTROLS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-QM207-231-FINITE-MAP-CONTROLS` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-FQ-QM207-231-FINITE-MAP-CONTROLS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1300, -2600, 1950]`, `chord_potential = 1950`, `holonomy_gamma2 = 2600`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-QM207-231-FINITE-MAP-CONTROLS): 4*idx(130) + 3*stage_rank(8) + route_degree(2) == 546` ($\text{value} = 546$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-QM207-231-FINITE-MAP-CONTROLS): R_raw(300) - G_cob(146) - S_decoy(8) == 146 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 146$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_qm207_231_finite_map_controls_master_certificate`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 4f03f564f1675dc7abe1226c9a7fadf62df0aed935938099aec0db828e3eec7b`
