# [TFQ-0185] Record the K_{2,3} finite certificate as the pair 6 and 9/2, with

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `2d1328e4-0623-5d82-98f3-b10488b701d6`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

The trace-zero quotient on K_{2,3} is a finite numerical certificate of 6 versus 9/2, not a Lean theorem in this tree. The README titled Trace-Zero Repair Quotients on a Finite Graph says the program checks K_{2,3} and K_4 minus an edge, and that on both graphs the expected quotients are 6 and 9/2 with gap 3/2. claim_ledger.md row TZQ-4.1 states Theorem 4.1: for the qutrit defect on unit-weight K_{2,3}, Phi_0 is 6 and Phi_all is 9/2. The obligation is to cite those two values as the certificate pair. The same README says no Lean formalization is claimed.

### Governing Obligation
Record the K_{2,3} finite certificate as the pair 6 and 9/2, with gap 3/2.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Hermitian trace-zero defects on a declared graph (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> GAP-F001-S000-001: Lean DualWitness is a candidate mirror, not a duality certificate for QM_080 Theorems 5-6; the K_{2,3} certificates are exact computations in Rust/Python, no Lean theorem for them. Zenodo 20550459 carries a wrong centered trace-zero dual awaiting erratum.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: not located`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for external:sha256:268cb7c97325e28274aeeb256645a51550ea6e687fa42b12343e4c63215430ad`](../../code/python/)
- [`absent: no local python twin located for external:sha256:15a047e84ecf1f2b166b471588781c72f32ce161a9222455b4fa786878f364ed`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0186](tfq_0186_do_not_treat_tracezeroduality_lean_as_a_lean_formalization_of_the_k_2_3_quotients.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
