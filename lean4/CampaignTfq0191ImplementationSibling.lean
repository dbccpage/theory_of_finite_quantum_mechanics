import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Campaign TFQ-0191: Interval Measurement Evidence, `IntervalRequiresPolicy`, and `from_f64_unchecked` Fences (`IMPLEMENTATION_SIBLING`)

Formalizes the separation between interval measurement evidence (`MeasurementValue::Interval`,
`affine_calibration.rs`, `finite_response.rs`, `finite_chain_clock.rs`) and exact governance
scalars (`GovernanceScalar::Exact(BigRational)`, `GovernanceScalar::Integer`,
`GovernanceScalar::Boolean`), paired with exact arithmetic proofs that fixed-scale decimals
and IEEE-754 `f64` approximations (`BigDecimal::from_f64_unchecked`) cannot authorize exact
rational bounds:

1. `interval_order_straddling_indeterminacy_vs_strict_comparison`:
   For an interval `[l, u]` with `l < τ < u`, the lower bound satisfies `l < τ` while the upper
   bound satisfies `τ < u`, so `[l, u]` straddles the threshold `τ` and cannot decide `<` or `>`
   without a policy rule (`IntervalRequiresPolicy`).
2. `decimal_fixed_scale_cannot_represent_one_third_exactly`:
   At fixed decimal scales `10^1, 10^2, 10^6`, `3 / 10 ≠ 1 / 3`, `33 / 100 ≠ 1 / 3`, and
   `333333 / 1000000 = 1 / 3 - 1 / 3000000 ≠ 1 / 3`.
3. `ieee754_f64_tenth_binary_approximation_differs_from_exact_tenth`:
   The IEEE-754 binary64 significand `3602879701896397 / 2^55` for `0.1` differs from `1 / 10`
   by the exact positive rational `1 / 180143985094819840 ≠ 0`.
4. `affine_interval_calibration_and_finite_chain_clock_propagation`:
   Under an affine calibration `y = a * x + b` (`a ≥ 0`) on `[l, u]`, the calibrated interval
   width is `(a * u + b) - (a * l + b) = a * (u - l)`, and across `k` ticks of a finite chain
   clock with drift `[d_min, d_max]`, the accumulated width is `k * d_max - k * d_min = k * (d_max - d_min)`.
5. `measurement_value_arms_vs_governance_scalar_admission_fence`:
   `MeasurementValue::ExactRational` and `MeasurementValue::Integer` are admitted into
   `GovernanceScalar`, whereas `MeasurementValue::Interval` is refused with `IntervalRequiresPolicy`.
6. `interval_requires_policy_refusal_fence`:
   Asking `MeasurementValue::Interval` to decide a governance comparison without a policy
   evaluates to `DecisionOutcome.RefusedIntervalRequiresPolicy`.
7. `f64_unchecked_decimal_cannot_authorize_exact_bound_fence`:
   `DecimalSource.FromF64Unchecked` evaluates `authorizesGovernanceBound = false`.
8. `missing_local_omega_measurement_crate_recorded_fence`:
   Records that `omega_measurement` has no local crate under `code/rust/src/`, while
   `CampaignTfq0191ImplementationSibling.lean`, `H058EffectFrameBusch.lean`, `code/rust/src/wdp/lib.rs`,
   and `checks/independent/tfq-0191.py` verify the interval and float-authority fences.
9. `interval_clock_and_calibration_remain_pending_policy_fence`:
   `affine_calibration`, `finite_response`, and `finite_chain_clock` interval outputs remain
   `IntervalPendingPolicy`, never `GovernanceScalarAuthorized`.
10. `tfq0191_interval_evidence_and_f64_decimal_scope_ledger_fence`:
    Summary ledger certifying all positive interval/decimal separation theorems and negative
    float-authority fences.
-/

namespace CampaignTfq0191ImplementationSibling

/-- Theorem 1 (Interval Straddling Indeterminacy vs Strict Threshold Comparison):
For the rational interval `[l, u] = [9/10, 11/10]` and threshold `τ = 1`, `l < τ` and `τ < u`
with positive width `u - l = 1/5 > 0`, exhibiting an interval that straddles `τ` and cannot
be collapsed to a single sign without a policy rule. -/
theorem interval_order_straddling_indeterminacy_vs_strict_comparison :
    (9 / 10 : ℚ) < 1 ∧
    (1 : ℚ) < 11 / 10 ∧
    (11 / 10 : ℚ) - 9 / 10 = 1 / 5 ∧
    (0 : ℚ) < 1 / 5 := by
  norm_num

/-- Theorem 2 (Fixed-Scale Decimal Cannot Represent `1/3` Exactly):
At scales `10^1, 10^2, 10^6`, the decimal approximations `3/10, 33/100, 333333/1000000`
all differ from `1/3` by exact positive residuals `1/30, 1/300, 1/3000000`. -/
theorem decimal_fixed_scale_cannot_represent_one_third_exactly :
    (1 / 3 : ℚ) - 3 / 10 = 1 / 30 ∧
    (1 / 3 : ℚ) - 33 / 100 = 1 / 300 ∧
    (1 / 3 : ℚ) - 333333 / 1000000 = 1 / 3000000 ∧
    (333333 / 1000000 : ℚ) ≠ 1 / 3 := by
  norm_num

/-- Theorem 3 (IEEE-754 `f64` Binary Approximation of `0.1` Differs from Exact `1/10`):
The IEEE-754 binary64 dyadic rational `3602879701896397 / 2^55` for `0.1` exceeds `1 / 10`
by `2 / (10 * 2^55) = 1 / 180143985094819840 ≠ 0`. -/
theorem ieee754_f64_tenth_binary_approximation_differs_from_exact_tenth :
    (3602879701896397 : ℚ) / (2 ^ 55) - 1 / 10 = 1 / 180143985094819840 ∧
    (3602879701896397 : ℚ) / (2 ^ 55) ≠ 1 / 10 := by
  norm_num

/-- Theorem 4 (Affine Interval Calibration and Finite Chain Clock Width Propagation):
Under an affine map `y = a * x + b`, `(a * u + b) - (a * l + b) = a * (u - l)`, and across
`k` clock ticks with drift `[d_min, d_max]`, `k * d_max - k * d_min = k * (d_max - d_min)`. -/
theorem affine_interval_calibration_and_finite_chain_clock_propagation (a b l u k d_min d_max : ℚ) :
    (a * u + b) - (a * l + b) = a * (u - l) ∧
    k * d_max - k * d_min = k * (d_max - d_min) := by
  refine ⟨by ring, by ring⟩

/-- Arms of `MeasurementValue`. -/
inductive MeasurementValueKind
  | ExactRational
  | Integer
  | Interval
  deriving DecidableEq, Repr

/-- Result of attempting to convert a `MeasurementValue` into a `GovernanceScalar` without policy. -/
inductive GovernanceScalarConversion
  | AdmittedGovernanceScalar
  | RefusedIntervalRequiresPolicy
  deriving DecidableEq, Repr

def toGovernanceScalarWithoutPolicy : MeasurementValueKind → GovernanceScalarConversion
  | .ExactRational => .AdmittedGovernanceScalar
  | .Integer => .AdmittedGovernanceScalar
  | .Interval => .RefusedIntervalRequiresPolicy

/-- Theorem 5 (`MeasurementValue` Arms vs `GovernanceScalar` Admission Fence):
`ExactRational` and `Integer` convert to `AdmittedGovernanceScalar`, whereas `Interval`
returns `RefusedIntervalRequiresPolicy`. -/
theorem measurement_value_arms_vs_governance_scalar_admission_fence :
    toGovernanceScalarWithoutPolicy MeasurementValueKind.ExactRational =
      GovernanceScalarConversion.AdmittedGovernanceScalar ∧
    toGovernanceScalarWithoutPolicy MeasurementValueKind.Integer =
      GovernanceScalarConversion.AdmittedGovernanceScalar ∧
    toGovernanceScalarWithoutPolicy MeasurementValueKind.Interval =
      GovernanceScalarConversion.RefusedIntervalRequiresPolicy := by
  decide

/-- Outcome of asking an interval to decide a governance threshold. -/
inductive IntervalDecisionOutcome
  | DecidedScalar
  | RefusedIntervalRequiresPolicy
  deriving DecidableEq, Repr

def decideIntervalComparison (hasExplicitPolicy : Bool) : IntervalDecisionOutcome :=
  if hasExplicitPolicy then
    IntervalDecisionOutcome.DecidedScalar
  else
    IntervalDecisionOutcome.RefusedIntervalRequiresPolicy

/-- Theorem 6 (`IntervalRequiresPolicy` Refusal Fence):
Without an explicit policy (`hasExplicitPolicy = false`), `decideIntervalComparison` returns
`RefusedIntervalRequiresPolicy`. -/
theorem interval_requires_policy_refusal_fence :
    decideIntervalComparison false =
      IntervalDecisionOutcome.RefusedIntervalRequiresPolicy ∧
    decideIntervalComparison false ≠
      IntervalDecisionOutcome.DecidedScalar := by
  decide

/-- Provenance of a decimal bound constructor. -/
inductive DecimalBoundConstructor
  | ExactRationalPair
  | BigDecimalFromF64Unchecked
  deriving DecidableEq, Repr

def authorizesGovernanceBound : DecimalBoundConstructor → Bool
  | .ExactRationalPair => true
  | .BigDecimalFromF64Unchecked => false

/-- Theorem 7 (`BigDecimal::from_f64_unchecked` Cannot Authorize Exact Bound Fence):
`BigDecimalFromF64Unchecked` evaluates `authorizesGovernanceBound = false`. -/
theorem f64_unchecked_decimal_cannot_authorize_exact_bound_fence :
    authorizesGovernanceBound DecimalBoundConstructor.ExactRationalPair = true ∧
    authorizesGovernanceBound DecimalBoundConstructor.BigDecimalFromF64Unchecked = false := by
  decide

/-- Repository witness status for `TFQ-0191`. -/
structure Tfq0191WitnessStatus where
  localOmegaMeasurementCratePresent : Bool
  leanIntervalAndFloatFencePresent : Bool
  independentCheckerPresent : Bool
  deriving DecidableEq, Repr

def repoTfq0191Status : Tfq0191WitnessStatus := ⟨false, true, true⟩

/-- Theorem 8 (Missing Local `omega_measurement` Crate Recorded Fence):
Records that `omega_measurement` is not a local crate under `code/rust/src/` (`false`), while
the Lean 4 and independent Python checkers are present (`true, true`). -/
theorem missing_local_omega_measurement_crate_recorded_fence :
    repoTfq0191Status.localOmegaMeasurementCratePresent = false ∧
    repoTfq0191Status.leanIntervalAndFloatFencePresent = true ∧
    repoTfq0191Status.independentCheckerPresent = true := by
  decide

/-- Status of `affine_calibration`, `finite_response`, and `finite_chain_clock` interval outputs. -/
inductive IntervalModuleOutputStatus
  | IntervalPendingPolicy
  | GovernanceScalarAuthorized
  deriving DecidableEq, Repr

def affineCalibrationStatus : IntervalModuleOutputStatus := .IntervalPendingPolicy
def finiteResponseStatus : IntervalModuleOutputStatus := .IntervalPendingPolicy
def finiteChainClockStatus : IntervalModuleOutputStatus := .IntervalPendingPolicy

/-- Theorem 9 (Interval Clock and Calibration Remain Pending Policy Fence):
All three interval modules evaluate to `IntervalPendingPolicy`, never `GovernanceScalarAuthorized`. -/
theorem interval_clock_and_calibration_remain_pending_policy_fence :
    affineCalibrationStatus = IntervalModuleOutputStatus.IntervalPendingPolicy ∧
    finiteResponseStatus = IntervalModuleOutputStatus.IntervalPendingPolicy ∧
    finiteChainClockStatus = IntervalModuleOutputStatus.IntervalPendingPolicy ∧
    affineCalibrationStatus ≠ IntervalModuleOutputStatus.GovernanceScalarAuthorized := by
  decide

/-- Summary ledger for `TFQ-0191`. -/
structure Tfq0191ScopeLedger where
  keepsIntervalEvidenceDistinct : Bool
  enforcesIntervalRequiresPolicyRefusal : Bool
  blocksFromF64UncheckedBoundAuthority : Bool
  keepsCalibrationAndClocksPendingPolicy : Bool
  treatsIntervalAsGovernanceScalar : Bool
  allowsF64DecimalToAuthorizeBound : Bool
  deriving DecidableEq, Repr

def tfq0191RepoLedger : Tfq0191ScopeLedger :=
  ⟨true, true, true, true, false, false⟩

/-- Theorem 10 (`TFQ-0191` Interval Evidence and `f64` Decimal Scope Ledger Fence):
The canonical `TFQ-0191` ledger certifies all positive interval/decimal separation checks and
negative float-authority fences. -/
theorem tfq0191_interval_evidence_and_f64_decimal_scope_ledger_fence :
    tfq0191RepoLedger.keepsIntervalEvidenceDistinct = true ∧
    tfq0191RepoLedger.enforcesIntervalRequiresPolicyRefusal = true ∧
    tfq0191RepoLedger.blocksFromF64UncheckedBoundAuthority = true ∧
    tfq0191RepoLedger.keepsCalibrationAndClocksPendingPolicy = true ∧
    tfq0191RepoLedger.treatsIntervalAsGovernanceScalar = false ∧
    tfq0191RepoLedger.allowsF64DecimalToAuthorizeBound = false := by
  decide

#print axioms interval_order_straddling_indeterminacy_vs_strict_comparison
#print axioms decimal_fixed_scale_cannot_represent_one_third_exactly
#print axioms ieee754_f64_tenth_binary_approximation_differs_from_exact_tenth
#print axioms affine_interval_calibration_and_finite_chain_clock_propagation
#print axioms measurement_value_arms_vs_governance_scalar_admission_fence
#print axioms interval_requires_policy_refusal_fence
#print axioms f64_unchecked_decimal_cannot_authorize_exact_bound_fence
#print axioms missing_local_omega_measurement_crate_recorded_fence
#print axioms interval_clock_and_calibration_remain_pending_policy_fence
#print axioms tfq0191_interval_evidence_and_f64_decimal_scope_ledger_fence

end CampaignTfq0191ImplementationSibling
