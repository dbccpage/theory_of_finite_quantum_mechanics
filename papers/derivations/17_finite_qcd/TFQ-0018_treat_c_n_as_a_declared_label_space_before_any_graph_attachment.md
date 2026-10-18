# [TFQ-0018] Treat C^N as a declared label space before any graph attachment

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `3c1d5da1-6681-5ca4-ae05-fc7d50cf23e2`  
> **Parent Derivation**: [TFQ-0017](TFQ-0017_do_not_promote_the_su_2_quaternion_shadow_to_su_3__c.md)

---

## 1. Abstract & Formal Statement

su_n.rs stores a generalized Gell-Mann family on a declared label space C^N for N from 2 through 8. Diagonal scales are irrational, so each generator is kept as sqrt(r_a) times an exact matrix M_a over Q(i), and the checked identities are rational: trace pairing 2 delta_ab and a Jacobi identity after the common square-root factor is removed. The file states that the label space is a separate declaration and is not built from a graph. For N=3 the generator count is eight, which is the algebra shadow used by the color control, not a finite group SU(3).

### Governing Obligation
Treat C^N as a declared label space before any graph attachment.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: the sqrt(r) M_a packaging is not the Lean Fierz slice`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_lie_theory/src/su_n.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: su_n Gell-Mann basis has no finite_qm use-case wrapper`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0019](TFQ-0019_keep_the_weighted_m_3_q_i_family_distinct_from_a_finite_subgroup_of_su_3.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
