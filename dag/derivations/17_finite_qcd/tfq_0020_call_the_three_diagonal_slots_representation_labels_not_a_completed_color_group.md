# [TFQ-0020] Call the three diagonal slots representation labels, not a completed color group

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `866d89c4-decb-5c59-9352-52cf31158727`  
> **Parent Derivation**: [TFQ-0019](tfq_0019_keep_the_weighted_m_3_q_i_family_distinct_from_a_finite_subgroup_of_su_3.md)

---

## 1. Abstract & Formal Statement

On those weighted generators the same Rust report records the fundamental Casimir sum as (4/3) times the 3 by 3 identity and the adjoint action sum as 3 times each basis element. Lean FiniteQM.lean names the same rationals in su3_casimir_and_channel_identities: C_F(3)=4/3 and C_A(3)=3. The three diagonal slots of T_3 and T-tilde_8 are representation labels for a declared three-dimensional carrier. su_n.rs still treats the carrier dimension as an input. The obligation is to call these labels a finite representation shadow for three colors, not a completed color group.

### Governing Obligation
Call the three diagonal slots representation labels, not a completed color group.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_lie_theory/src/su_n.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/qcd_beta0_wilson_confinement_control.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qcd_beta0_wilson_confinement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0021](tfq_0021_record_channel_factors_as_casimir_arithmetic_not_as_composites.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
