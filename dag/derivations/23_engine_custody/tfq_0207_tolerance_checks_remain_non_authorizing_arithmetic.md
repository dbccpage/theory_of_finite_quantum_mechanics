# [TFQ-0207] Tolerance checks remain non-authorizing arithmetic

> **Stage**: `ENGINE_CUSTODY` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `2c9055ff-da7d-56db-aa85-a2375379a317`  
> **Parent Derivation**: [TFQ-0206](tfq_0206_a_float_computation_cannot_authorize.md)

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
- [`lean4/FiniteDensity.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/qm/campaigns/density_matrix.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`](../../code/python/)
- [`absent: no local python twin located for external:sha256:28bf40cf36c459316ada0e9f8d6862026535c3fee1455678793ce7af060af8c9`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0208](tfq_0208_python_names_the_finite_packet_statement.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000:001_from_primitive_difference_to_quantum_mechanics`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`, `F003.S000`
- **Primary Source Paths**:
  - `external:git-tree:aaf60017b237ab042d2a4f52cec36e21f4264b2f`
  - `external:git-tree:825506e48afab1825c9431562935d4f0fcadc33f`
  - `external:git-tree:5d358f5062016c742016b891fa7891bb0f0e19ef`
