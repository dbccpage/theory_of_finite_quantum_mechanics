# [TFQ-0072] Each language must carry: channel amplitude, optical defect, finite Born partial sum,

> **Stage**: `FINITE_QED` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `71a03090-acf5-5d96-a175-0d1d6908deb8`  
> **Parent Derivation**: [TFQ-0071](tfq_0071_each_language_must_carry_hermitian_k_yields_a_unitary_cayley_s_on.md)

---

## 1. Abstract & Formal Statement

scattering_amplitude.rs takes the finite S from s_matrix and forms channel amplitudes at a declared energy. amplitude and probability read incoming and outgoing channels and refuse an index outside the carrier. optical_theorem_defect computes the matrix defect of T - T dagger against 2 i T dagger T. A declared H0 and V give a free resolvent, a full resolvent, and a T matrix. born_series sums V (G0 V)^k through a declared order. lippmann_schwinger_defect and resolvent_identity_defect expose the finite residuals.

### Governing Obligation
Each language must carry: channel amplitude, optical defect, finite Born partial sum, Lippmann-Schwinger residual, and an explicit statement that no on-shell limit is taken.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `continuum path category (assumption)`
- **Admitted**: `declared discrete Lagrangian and weights (assumption)`
- **Admitted**: `refinement system and convergence certificate (assumption)`
- **Admitted**: `time slicing (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean file for ENC-1072 not verified by me.

> [!WARNING]
> Forward-Euler norm growth 1 + e^2 > 1 vs Cayley norm preservation is mechanized; continuum path-integral convergence remains conditional.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:a4ca67769f0cdeae91bce65233c44b0a2b18deb921c5d4e4fabd22880ee84034`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0073](tfq_0073_each_language_must_carry_isotony_locality_and_optional_complement_duality_on_a.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
