# [TFQ-0034] Keep the flavor GMO polynomial away from the color Casimir control; the

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `80563309-6644-5b99-a207-15559b120a73`  
> **Parent Derivation**: [TFQ-0033](tfq_0033_construct_an_explicit_three_index_color_contraction_before_using_a_baryon_singlet_label.md)

---

## 1. Abstract & Formal Statement

qed_weak_hadronic_finite_maps.rs and the Python twin implement a different su(3), the flavor mass operator M0 + M1*Y + M2*(I(I+1)-Y^2/4). gmo_octet_relation_coefficients returns the zero vector in all three slots, and Lean gmo_octet in FiniteQFTAndGravity.lean records the polynomial identity 2(M_N+M_Xi)=3 M_Lambda + M_Sigma for every coefficient triple. pdg_baryon_masses then imports decimal MeV values and forms a fractional residual. That imported residual is not an exact identity. A float or truncated reading of the PDG residual cannot authorize the finite color-channel statement in the other su(3) module.

### Governing Obligation
Keep the flavor GMO polynomial away from the color Casimir control; the PDG residual cannot authorize either finite identity.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/FiniteQFTAndGravity.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:b2756728a2444a8202ad7ab9078b63b94e2b41bb2addc311e7a2b1bebd8d9f44`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/qed_weak_hadronic_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0035](tfq_0035_quote_n_c_3_as_the_finite_color_factor_and_leave_the_ev_rate.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
