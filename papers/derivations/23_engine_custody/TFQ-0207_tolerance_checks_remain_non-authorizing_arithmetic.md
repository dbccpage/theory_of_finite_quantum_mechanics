# [TFQ-0207] Tolerance checks remain non-authorizing arithmetic

> **Stage**: `ENGINE_CUSTODY` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `2c9055ff-da7d-56db-aa85-a2375379a317`  
> **Parent Derivation**: [TFQ-0206](TFQ-0206_a_float_computation_cannot_authorize.md)

---

## 1. Abstract & Formal Statement

Tolerance arithmetic on the atlas shelves stays a recorded computation with a cutoff. is_valid_density_matrix compares a matrix with its conjugate transpose and compares its trace with one, using an absolute tolerance. born_probability returns a Python float from the real part of a trace. The finite-obstruction reference imports linprog, so a solver float is not an exact rational witness. F003 may store the call and the returned number in a side file. Custody does not promote that number into the rational carrier or into the Lean sentence compared later.

### Governing Obligation
Store tolerance traces as side logs and keep them out of the rational statement.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/lean4/FromPrimitiveDifferenceToQuantumMechanics/FiniteDensity.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/density_matrix.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/python/src/finite_obstruction.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/python/src/finite_quantum/density_matrix.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0208](TFQ-0208_python_names_the_finite_packet_statement.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000:001_from_primitive_difference_to_quantum_mechanics`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`, `F003.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime`
