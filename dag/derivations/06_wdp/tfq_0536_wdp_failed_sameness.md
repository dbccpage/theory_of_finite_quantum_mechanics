# [TFQ-0536] wdp-failed-sameness

> **Stage**: `WDP` | **Status**: `SOURCE_RECORD`  
> **UUID**: `61c77f02-bd23-5f87-afe7-7d7010ba31b3`  
> **Parent Derivation**: [TFQ-0360](tfq_0360_supply_the_admitted_cut_x_e_tau_k_as_data_and_do.md)

---

## 1. Abstract & Formal Statement

WDP-CH01-P01: within a fixed comparison family K, a failed declared sameness comparison Same_K(p, q) = 0 exhibits that the two compared presentations are not interchangeable under that comparison. The statement is local: it does not say the presentations differ under every comparison, does not make the failure intrinsic to the tokens, and supplies no order. A failed comparison is a residual at the level of predicates; encoding it as p − q is a stronger step that presupposes subtraction, scalars and a zero.

### Governing Obligation
Report a failed declared comparison as non-interchangeability under that comparison only, and do not encode it as a difference p − q without first admitting a group or vector-space carrier.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared comparison family K and sameness predicate Same_K on presentations (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Local to the declared comparison; it orders nothing, says nothing about other comparisons, and the ledger binds it to prose plus the Python ground.py check with no Lean declaration.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: the claim map lists WDP-CH01-P01 as prose-only; no Lean declaration states it`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `external:sha256:39e988784c38613df38c5f88b06efee27f73f0a7a02b8069458d6e2168e498b8::primitive_difference` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py::test_primitive_difference_and_triangle_identity`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py)
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/ground.py::primitive_difference`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/ground.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0538](tfq_0538_wdp_quotient_defect_root_p.md)
- [TFQ-0540](tfq_0540_wdp_asymmetry_injection_ledger.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:420-432`
  - `external:sha256:b3182646c084a1d31b4c382572524489dcfa76f74bf74ee0863573424d048c65:111-123`
