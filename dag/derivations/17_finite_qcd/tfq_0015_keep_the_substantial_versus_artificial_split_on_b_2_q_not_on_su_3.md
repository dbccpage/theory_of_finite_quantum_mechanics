# [TFQ-0015] Keep the substantial-versus-artificial split on B_2(Q), not on SU(3)

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `774e8cb5-9b27-5790-bb8d-4e5fa538c906`  
> **Parent Derivation**: [TFQ-0014](tfq_0014_do_not_cite_the_m_2_packet_complex_or_the_groupoid_algebra_as.md)

---

## 1. Abstract & Formal Statement

hierarchical_nonabelian_dfm_finite_map.md, QM-213, separates an artificial Borel connection from a substantial one on a 4-vertex punctured diamond. Artificial data U_e = h(t)h(s)^{-1} has face and cycle holonomy I_2, and a single-valued vertex dressing neutralizes every edge. Substantial data keeps the triangular face flat while the punctured cycle carries a Borel matrix with trace 5/2 and determinant 1, so a dressing supported on a spanning tree is required. evaluate_qm213_nonabelian_dfm_control and run_qm213_nonabelian_dfm_control replay that split. The structure group in the map is B_2(Q), not SU(3).

### Governing Obligation
Keep the substantial-versus-artificial split on B_2(Q), not on SU(3).

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: QM-213 has no theorem block in FiniteQM.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/nonabelian_dfm_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0016](tfq_0016_add_a_lean_replay_of_the_two_stage_dressing_or_leave_qm_213_as.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
