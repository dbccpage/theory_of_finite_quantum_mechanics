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
- [`absent: no local rust twin located for external:sha256:70c158328f038a7c76fcacc04288b142250b1121803c1c0c511aa71943a83782`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`](../../code/python/)
- [`absent: no local python twin located for external:sha256:28bf40cf36c459316ada0e9f8d6862026535c3fee1455678793ce7af060af8c9`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0207](tfq_0207_tolerance_checks_remain_non_authorizing_arithmetic.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000`, `F001.S000`, `F000.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:git-tree:5d358f5062016c742016b891fa7891bb0f0e19ef`
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:6c3ddd228c139e91dd74dc2ea348d97cc54608a0`
  - `external:git-tree:aaf60017b237ab042d2a4f52cec36e21f4264b2f`
