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
