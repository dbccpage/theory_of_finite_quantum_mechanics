# [TFQ-0019] Keep the weighted M_3(Q(i)) family distinct from a finite subgroup of SU(3)

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `45bea6fc-1760-5308-bac3-5e3c3c7a3667`  
> **Parent Derivation**: [TFQ-0018](TFQ-0018_treat_c_n_as_a_declared_label_space_before_any_graph_attachment.md)

---

## 1. Abstract & Formal Statement

qcd_beta0_wilson_confinement_control.rs, QM-221, builds eight weighted generators in M_3(Q(i)). The first seven are half the usual off-diagonal and Cartan patterns with weight 1, and T-tilde_8 is (1/2) diag(1,1,-2) with weight 1/3, avoiding a bare sqrt(3) in the matrix entries. The Rust report asks each generator to be Hermitian and traceless, the weighted trace pairing to equal (1/2) delta_ab on all 64 pairs, and the Jacobi sum to vanish on all 512 ordered triples. Python su3_weighted_generators repeats that arithmetic with fractions. This is a finite matrix control. It does not define a lattice link in SU(3).

### Governing Obligation
Keep the weighted M_3(Q(i)) family distinct from a finite subgroup of SU(3).

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/qcd_beta0_wilson_confinement_control.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qcd_beta0_wilson_confinement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0020](TFQ-0020_call_the_three_diagonal_slots_representation_labels_not_a_completed_color_group.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
