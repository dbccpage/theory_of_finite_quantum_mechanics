# [TFQ-0298] Bra-ket section remains non-canonical

> **Stage**: `FINITE_HILBERT` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `0caa67d2-2335-5565-bec4-226dc8799730`  
> **Parent Derivation**: [TFQ-0297](TFQ-0297_inner-product_admission_slot_is_still_a_stub.md)

---

## 1. Abstract & Formal Statement

qm_201_braket_section_admission.md titles the bra-ket section non-canonical. Its status box says the draft does not derive continuum quantum mechanics and mints no authority. The claim ledger marks QM_201-C0 as a reserved band slot with stub status. The finite obligation is a chosen section of the ray: a representative vector for each projective class, with the residual freedom written down. quantum_state.rs keeps an exact ray over Gaussian rationals that is not normalized, and computes scale-free ratios, which is a different choice from a unit-section convention. No file in this slice forces one section.

### Governing Obligation
Declare any bra-ket section explicitly and leave the QM_201 slot open while it is only a stub.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
*Formalization active. Proof obligations tracked under zero-sorry regime.*

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0299](../08_l1_to_l2/TFQ-0299_orthogonal_additivity_is_an_extra_frame_law.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-CABELLO-FRAME-POLYTOPE-146`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-CABELLO-FRAME-POLYTOPE-146` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-CABELLO-FRAME-POLYTOPE-146`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1080, -2160, 1620]`, `chord_potential = 1620`, `holonomy_gamma2 = 2160`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-CABELLO-FRAME-POLYTOPE-146): 4*idx(108) + 3*stage_rank(7) + route_degree(3) == 456` ($\text{value} = 456$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-CABELLO-FRAME-POLYTOPE-146): R_raw(251) - G_cob(122) - S_decoy(7) == 122 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 122$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 0d3f57a67ec5428c4b4f93b09aec1a15c11199f196fe9151b25da48e46cae569`
