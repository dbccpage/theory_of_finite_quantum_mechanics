# [TFQ-0073] Each language must carry: isotony, locality and optional complement duality on a

> **Stage**: `FINITE_QED` | **Status**: `GAP`  
> **UUID**: `f25f3290-ec26-53ba-a375-805b00ca8c4d`  
> **Parent Derivation**: [TFQ-0072](tfq_0072_each_language_must_carry_channel_amplitude_optical_defect_finite_born_partial_sum.md)

---

## 1. Abstract & Formal Statement

algebraic_qft.rs checks a finite local net and refuses the continuum reading in its own header. try_new requires a declared algebra for every region of one common carrier, including the empty region and its complement. qubit_chain builds the subset net from Pauli supports and refuses more than four parties. defects records an isotony failure when a smaller region is not a subalgebra of a larger one, a locality failure when disjoint regions fail to commute, and, if requested, a duality failure when an algebra is not the commutant of its complement.

### Governing Obligation
Each language must carry: isotony, locality and optional complement duality on a declared finite subset net of at most four parties, and must state that this net is not continuum Haag duality.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex field C (assumption)`
- **Admitted**: `continuum Hilbert space (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Z[i] non-field obstruction and discriminant-5 spectral exit from Q(i) are mechanized; continuum Hilbert completion remains an explicit import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:2c3063603fd3462c580b0cbfda3f2af787a0b06292ac7ea296360d6330ce0139`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0074](tfq_0074_each_language_must_carry_klein_nishina_forward_value_1_thomson_shape_1_u_2_2_s_u.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
