# [TFQ-0191] Keep interval measurement evidence distinct, and do not let an f64-built decimal

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `a0cc0796-08ba-5bc0-8bcf-baa4803f1a66`  
> **Parent Derivation**: [TFQ-0189](tfq_0189_keep_exact_rational_measurement_evidence_distinct_and_free_of_float_authority.md)

---

## 1. Abstract & Formal Statement

Interval evidence is a third kind and is not yet a governance scalar. MeasurementValue::Interval stores lower and upper BigDecimal bounds, and MeasurementError::IntervalRequiresPolicy is the refusal when an interval is asked to decide. BigDecimal::from_f64_unchecked builds a decimal from an f64 with a fixed scale, which is not an exact rational. affine_calibration.rs, finite_response.rs, and finite_chain_clock.rs add further interval clocks and calibrations. The obligation is to keep interval evidence pending a policy decision and to stop that unchecked f64 constructor from authorizing a bound.

### Governing Obligation
Keep interval measurement evidence distinct, and do not let an f64-built decimal authorize a bound.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Interval Evidence vs Governance Scalar (`IntervalRequiresPolicy`)**: `MeasurementValue::Interval` represents a pair of bounds $[l, u]$ ($l \le u$) and is distinct from `GovernanceScalar` (`ExactRational`, `Integer`, `Boolean`). When $[l, u]$ straddles a threshold $\tau$ ($l < \tau < u$) or is asked to decide without an explicit policy rule, conversion refuses with `MeasurementError::IntervalRequiresPolicy`.
- **Fixed-Scale Decimal & IEEE-754 `f64` Discrepancy (`BigDecimal::from_f64_unchecked`)**: A fixed-scale decimal $m / 10^s$ cannot represent non-dyadic-decimal rationals such as $1/3$ ($10^s \equiv 1 \pmod 3$), and IEEE-754 binary64 approximates $1/10$ by $3602879701896397 / 2^{55} = 1/10 + 1/180143985094819840 \ne 1/10$, so `BigDecimal::from_f64_unchecked` cannot authorize an exact rational bound.
- **Interval Clocks & Calibrations Pending Policy**: Affine calibrations ($y = a x + b$, width $a(u - l)$), finite response intervals, and $k$-tick finite chain clock intervals ($[k d_{\min}, k d_{\max}]$, width $k(d_{\max} - d_{\min})$) remain interval evidence pending policy.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `lean4/CampaignTfq0191ImplementationSibling.lean`:
  - `CampaignTfq0191ImplementationSibling.interval_order_straddling_indeterminacy_vs_strict_comparison`
  - `CampaignTfq0191ImplementationSibling.decimal_fixed_scale_cannot_represent_one_third_exactly`
  - `CampaignTfq0191ImplementationSibling.ieee754_f64_tenth_binary_approximation_differs_from_exact_tenth`
  - `CampaignTfq0191ImplementationSibling.affine_interval_calibration_and_finite_chain_clock_propagation`
  - `CampaignTfq0191ImplementationSibling.measurement_value_arms_vs_governance_scalar_admission_fence`
  - `CampaignTfq0191ImplementationSibling.interval_requires_policy_refusal_fence`
  - `CampaignTfq0191ImplementationSibling.f64_unchecked_decimal_cannot_authorize_exact_bound_fence`
  - `CampaignTfq0191ImplementationSibling.missing_local_omega_measurement_crate_recorded_fence`
  - `CampaignTfq0191ImplementationSibling.interval_clock_and_calibration_remain_pending_policy_fence`
  - `CampaignTfq0191ImplementationSibling.tfq0191_interval_evidence_and_f64_decimal_scope_ledger_fence`
- `lean4/H058EffectFrameBusch.lean`:
  - `FableHilbertWalk20260819.H058.rat_add_le_add`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `code/rust/src/wdp/lib.rs`:
  - `evaluate_exactness_fraud_criterion`

### Independent Python Verification
- `checks/independent/tfq-0191.py`:
  - `run_all_checks`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `lean4/CampaignTfq0191ImplementationSibling.lean`
  - `lean4/H058EffectFrameBusch.lean`
  - `code/rust/src/wdp/lib.rs`
  - `checks/independent/tfq-0191.py`
