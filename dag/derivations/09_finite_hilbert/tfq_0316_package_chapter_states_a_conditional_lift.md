# [TFQ-0316] Package chapter states a conditional lift

> **Stage**: `FINITE_HILBERT` | **Status**: `SOURCE_RECORD`  
> **UUID**: `5961eb44-4f9e-5a02-8081-f9a5bf0e2293`  
> **Parent Derivation**: [TFQ-0315](tfq_0315_exact_density_ray_and_population_shadow.md)

---

## 1. Abstract & Formal Statement

The package README in 001_from_primitive_difference_to_quantum_mechanics says the book does not derive quantum mechanics from primitive difference and that a finite Gauss-integer matrix algebra is not ordinary matrix algebra over the complex numbers. Chapter 2 is titled as the conditional Hilbert lift and Born normalization. The finite obligation of this node is to match that floor: F001.S000 coordinates the lift, and the chapter is a consolidation record, not a new existence argument. The README classifies steps as formal finite results, source claims, candidate mirrors, continuum interfaces, or open bridges.

### Governing Obligation
Use the F001 package as the floor match for a conditional lift, with the continuum Hilbert step still open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/FiniteDensity.lean`](../../lean4/)
- [`lean4/DualWitness.lean`](../../lean4/)

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0317](tfq_0317_three_lean_files_stay_on_a_narrow_carrier.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`
  - `external:sha256:49250fc3940b574236fe8aeb8acabb9673af35fe28f17474e9deb52ecd18a713`
