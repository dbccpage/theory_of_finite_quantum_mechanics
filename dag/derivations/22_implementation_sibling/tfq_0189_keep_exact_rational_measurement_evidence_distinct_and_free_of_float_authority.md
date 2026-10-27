# [TFQ-0189] Keep exact rational measurement evidence distinct and free of float authority

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `16ee6e37-dc8c-5905-bed2-39c93fc2df96`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

Exact measurement evidence is the ExactRational and Integer arms of MeasurementValue, and it stays distinct from the other arms. src/measurement_kernel.rs documents that no governance-critical decision may depend on raw f64, and GovernanceScalar accepts Exact of BigRational, Integer, and Boolean only. EffectFrameBusch.lean, AuthorityEffect None, works in Rat and says its squeeze lemma is not a density or completion theorem. The obligation is to let an exact rational measurement authorize a finite comparison only as that rational, not by passing through a display float.

### Governing Obligation
Keep exact rational measurement evidence distinct and free of float authority.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/EffectFrameBusch.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:e7de14f3a7ac549411872b110b09968dc2178ab76ed8099b8871e949a9d69b7a`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0190](tfq_0190_keep_symbolic_measurement_references_distinct_from_exact_rationals_and_from_intervals.md)
- [TFQ-0191](tfq_0191_keep_interval_measurement_evidence_distinct_and_do_not_let_an_f64_built_decimal.md)
- [TFQ-0192](tfq_0192_keep_diagnostic_floats_and_display_conversions_out_of_governance_and_out_of.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
