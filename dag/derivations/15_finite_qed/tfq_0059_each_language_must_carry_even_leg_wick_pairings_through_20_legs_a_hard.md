# [TFQ-0059] Each language must carry: even-leg Wick pairings through 20 legs, a hard

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `dd01fb4a-c925-5b27-809d-65c24f0c45cc`  
> **Parent Derivation**: [TFQ-0058](tfq_0058_each_language_must_carry_u_g_equals_the_scaled_principal_minor_of_the.md)

---

## 1. Abstract & Formal Statement

feynman_diagram.rs computes finite Wick contractions and vacuum-multigraph symmetry factors. wick_pairing_count and wick_pairings require an even number of legs, at most 20, and refuse when the materialized pairing or permutation count exceeds the budget. MAX_WICK_PAIRINGS is 1<<16. A contraction keeps half-edges, loops and parallel edges. symmetry_factor uses vertex automorphisms, parallel-edge permutations and loop reversals. phi4_vacuum_diagrams classifies canonical phi-four vacuum multigraphs through three vertices and returns a computed factor.

### Governing Obligation
Each language must carry: even-leg Wick pairings through 20 legs, a hard budget refusal, and a symmetry factor from automorphisms, parallel edges and loop reversals, with no loop integral.

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
- [`absent: no local rust twin located for external:sha256:5750c8892fd61b580168841520e2dbb88c42dc9a2870654a5b5a13df5a7e3be1`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0060](tfq_0060_each_language_must_carry_c1_1_2_exactly_and_higher_coefficients_only.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
