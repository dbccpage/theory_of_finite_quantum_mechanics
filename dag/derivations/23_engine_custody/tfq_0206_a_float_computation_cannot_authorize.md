# [TFQ-0206] A float computation cannot authorize

> **Stage**: `ENGINE_CUSTODY` | **Status**: `SOURCE_RECORD`  
> **UUID**: `ecfd3068-698f-554b-914e-e2c686af8937`  
> **Parent Derivation**: [TFQ-0205](tfq_0205_exact_rational_carriers_cross_the_wire_as_text.md)

---

## 1. Abstract & Formal Statement

A float computation cannot authorize. The kernel names approximate as the only sanctioned lossy read of an Exact value and returns None when the value does not fit in a finite f64. That function is a named loss, not a second carrier. On the quantum shelf, density_matrix.py takes a NumPy array and a tolerance and returns a Python float, so those results stay diagnostic. Level18 records a zero-float law whose gap is an integer difference of scaled objectives. The prime runtime may keep a float trace in a side log. It must not copy that float into the carrier or treat a tolerance match as the finite statement.

### Governing Obligation
Bar every float or tolerance result from the authorizing carrier.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for lean4/Level18ZeroFloatLaw.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_kernel/src/exact.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`](../../code/python/)
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/python/src/finite_obstruction.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0207](tfq_0207_tolerance_checks_remain_non_authorizing_arithmetic.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000`, `F001.S000`, `F000.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics`
