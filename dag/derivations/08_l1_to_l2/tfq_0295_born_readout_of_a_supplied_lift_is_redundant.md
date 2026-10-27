# [TFQ-0295] Born readout of a supplied lift is redundant

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `b29fa125-ae52-5496-bfac-bea4ad609d47`  
> **Parent Derivation**: [TFQ-0294](tfq_0294_circle_phases_as_an_imported_unit_group.md)

---

## 1. Abstract & Formal Statement

qm_020_born_normalization_and_conditional_hilbert_lift.md does not derive quantum mechanics. Its opening says the question is the normalized weight law and an optional encoding, given additive weights. The section labeled Theorem 4 states that if a lift is supplied with squared modulus equal to the weight, the Born normalization of that lift matches direct l1 normalization. The finite obligation is that equality for a supplied lift, not existence of the lift. Square roots, complex scalars, and unit phases are imports, already separated in the gap nodes.

### Governing Obligation
Match Born normalization to the l1 profile only for a supplied lift, without deriving quantum mechanics.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Born/quadratic readout (assumption)`
- **Admitted**: `complex scalars with modulus: lift`
- **Admitted**: `square root field: lift`
- **Admitted**: `unit phases: lift`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No Lean theorem for |c|^2 normalization over C found; BornNormalization.lean treats discrete 2x2 density / POVM. Rust exact_amplitudes returns None unless every p_j is a rational square.

> [!WARNING]
> The cited declarations live in lean4/original_lean_20260809/qm_l010_01_born_redundancy.lean (2,215 lines, Mathlib.Tactic import); repo-level lean4/quantum_mechanics copy is Mathlib-free but this extraction did not run a build. Zenodo 20683775 needs the narrowing erratum.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/BornNormalization.lean`](../../lean4/)
- [`lean4/BornRedundancy.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:2367d7d43e194cf155298ace7054041ae444c67ab6cd71f51cc12cfacda6f3d4`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:d58eb2c1f4ae2ac65cc7145554cd2a5c955e096776c1f6d9daafb2065b14450e`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py`](../../code/python/)
- [`absent: no local python twin located for external:unlocated`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0296](tfq_0296_hilbert_inner_product_is_admitted_structure.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`
  - `external:sha256:eb788c5f48e4cc2ea2d3abdd7c4c0aaebe0b2b2edd084d6daf463e27df848c8b`
