# [TFQ-0192] Keep diagnostic floats and display conversions out of governance and out of

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `3e798744-bc10-52c3-bfa6-b57153d314d2`  
> **Parent Derivation**: [TFQ-0189](tfq_0189_keep_exact_rational_measurement_evidence_distinct_and_free_of_float_authority.md)

---

## 1. Abstract & Formal Statement

Diagnostic floats are a fourth arm and are barred from governance even when a display conversion exists. MeasurementValue::DiagnosticFloat carries an f64 plus a DiagnosticPurpose limited to logging or visualization. MeasurementError variants RawF64ForbiddenInGovernance and DiagnosticFloatForbiddenInGovernance name the refusal. try_to_f64_for_display is documented as forbidden for governance decisions. The obligation is to leave that display path outside every licence, probability, and MUB certificate. FQ-IMPL-F64-GATING counts two measurement files in legacy_debt.

### Governing Obligation
Keep diagnostic floats and display conversions out of governance and out of exact certificates.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `floating point as diagnostic only (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Exact faces use BigRational/Q(i)/Q(zeta_n); f64 faces are legacy debt, not agreed use. Which quantum_physics results still route through f64 is not audited here.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:e7de14f3a7ac549411872b110b09968dc2178ab76ed8099b8871e949a9d69b7a`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:0d9d32875b0dda27f266bef37af470f35769ab924210bd90b9ed923958b2baf3`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:07e63c53da4b64ecfc4fa925a1544eccb27b590bfd3e257b35947c3c15a3ca73`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
