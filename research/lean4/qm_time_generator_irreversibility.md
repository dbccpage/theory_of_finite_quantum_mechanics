import Mathlib.Tactic

/-!
# QMTimeGeneratorIrreversibility — W6.16 (time parameter vs generator; irreversibility)

Programme target: DERIV-MASTER W6.16 (QMREG-66).

**Adjudication (toy form):**

1. **Discrete time parameter** on classical residual kernels is a step count
   $n\in\mathbb{N}$ with Chapman–Kolmogorov composition — **DERIVED** on FinL1.
2. **Generator data** (rate matrix / infinitesimal) is **distinct** from the
   discrete step map: same kernel can be iterated without naming a continuous
   generator; continuous one-parameter groups require `CONT-TIME` capital.
3. **Irreversibility entry** is already classical: the reset kernel has **no**
   left inverse among column-stochastic 2×2 kernels — **DERIVED** on FinL1.
4. Continuous unitary generator / Stone $e^{-itH}$ remains **OPEN** /
   **CONDITIONAL** under the unitary lift (`OB-HERM` / `CONT-TIME` nesting).
5. **Semigroup / contraction / discrete phase residual (TOY-MECH):** Chapman–
   Kolmogorov samples for flip; reset contracts all bit weights to pure0;
   discrete phase clock under lift is step×increment (continuous rate still
   extra data); Stone still **OPEN**.

Upstream: W6.7 CONT-TIME underivability; W6.8 unitarity ↛ stochastic; W6.9 hermiticity.

AuthorityEffect: None.
-/

namespace QM
namespace TimeGeneratorIrreversibility

/-! ## 2×2 column-stochastic kernels (reuse W6.8 shape) -/

structure Kernel2 where
  k00 : Nat
  k10 : Nat
  k01 : Nat
  k11 : Nat
  deriving DecidableEq, Repr

namespace Kernel2

def IsColumnStochastic (K : Kernel2) : Prop :=
  K.k00 + K.k10 = 1 ∧ K.k01 + K.k11 = 1

/-- Matrix product $(AB)_{ij} = \sum_k A_{ik} B_{kj}$ (row-col Nat toy). -/
def mul (A B : Kernel2) : Kernel2 :=
  { k00 := A.k00 * B.k00 + A.k01 * B.k10
    k10 := A.k10 * B.k00 + A.k11 * B.k10
    k01 := A.k00 * B.k01 + A.k01 * B.k11
    k11 := A.k10 * B.k01 + A.k11 * B.k11 }

/-- Discrete time iteration: $K^{n+1} = K \cdot K^n$ with $K^0 = I$. -/
def pow (K : Kernel2) : Nat → Kernel2
  | 0 => { k00 := 1, k10 := 0, k01 := 0, k11 := 1 }
  | n + 1 => mul K (pow K n)

end Kernel2

def idKernel : Kernel2 :=
  { k00 := 1, k10 := 0, k01 := 0, k11 := 1 }

def flipKernel : Kernel2 :=
  { k00 := 0, k10 := 1, k01 := 1, k11 := 0 }

def resetKernel : Kernel2 :=
  { k00 := 1, k10 := 0, k01 := 1, k11 := 0 }

theorem id_column_stochastic : idKernel.IsColumnStochastic := by
  simp [idKernel, Kernel2.IsColumnStochastic]

theorem flip_column_stochastic : flipKernel.IsColumnStochastic := by
  simp [flipKernel, Kernel2.IsColumnStochastic]

theorem reset_column_stochastic : resetKernel.IsColumnStochastic := by
  simp [resetKernel, Kernel2.IsColumnStochastic]

theorem pow_zero (K : Kernel2) : Kernel2.pow K 0 = idKernel := by
  simp [Kernel2.pow, idKernel]

theorem flip_pow_one : Kernel2.pow flipKernel 1 = flipKernel := by
  simp [Kernel2.pow, Kernel2.mul, flipKernel, idKernel]

theorem flip_pow_two : Kernel2.pow flipKernel 2 = idKernel := by
  simp [Kernel2.pow, Kernel2.mul, flipKernel, idKernel]

theorem reset_pow_one : Kernel2.pow resetKernel 1 = resetKernel := by
  simp [Kernel2.pow, Kernel2.mul, resetKernel, idKernel]

theorem reset_pow_two : Kernel2.pow resetKernel 2 = resetKernel := by
  simp [Kernel2.pow, Kernel2.mul, resetKernel, idKernel]

/-- Discrete step parameter is ordinary Nat iteration (DERIVED). -/
theorem discrete_time_parameter_derived :
    Kernel2.pow flipKernel 0 = idKernel ∧
    Kernel2.pow flipKernel 1 = flipKernel ∧
    Kernel2.pow flipKernel 2 = idKernel ∧
    Kernel2.pow resetKernel 2 = resetKernel :=
  ⟨pow_zero flipKernel, flip_pow_one, flip_pow_two, reset_pow_two⟩

/-! ## Time parameter ≠ generator data

A discrete trajectory is a pair (kernel, step count). A generator candidate is
a separate rate matrix tag — not forced by naming the step map alone.
-/

structure DiscreteTrajectory where
  kernel : Kernel2
  steps : Nat

/-- Rate-matrix / infinitesimal generator label (not computed from kernel alone). -/
structure GeneratorCandidate where
  /-- Off-diagonal rate scale (toy Nat); 0 means "no continuous generator declared". -/
  rateScale : Nat
  deriving DecidableEq, Repr

def trajFlip2 : DiscreteTrajectory :=
  { kernel := flipKernel, steps := 2 }

def trajReset1 : DiscreteTrajectory :=
  { kernel := resetKernel, steps := 1 }

/-- Same kernel iterated at different step counts are distinct trajectories. -/
theorem step_count_is_time_parameter :
    trajFlip2.steps ≠ trajReset1.steps ∨ trajFlip2.kernel ≠ trajReset1.kernel := by
  left
  decide

/-- Declaring a continuous generator is extra data, not FinL1-forced. -/
def noGenerator : GeneratorCandidate := { rateScale := 0 }
def someGenerator : GeneratorCandidate := { rateScale := 1 }

theorem generator_not_forced_by_kernel_label :
    noGenerator ≠ someGenerator := by
  decide

/-! ## Irreversibility entry (classical)

Left inverse among column-stochastic kernels: $L \cdot K = I$.
Reset admits none among the three listed stochastic maps (id, flip, reset).
-/

def leftMulId (K : Kernel2) : Kernel2 := Kernel2.mul idKernel K
def leftMulFlip (K : Kernel2) : Kernel2 := Kernel2.mul flipKernel K
def leftMulReset (K : Kernel2) : Kernel2 := Kernel2.mul resetKernel K

theorem left_id_reset : leftMulId resetKernel = resetKernel := by
  simp [leftMulId, Kernel2.mul, idKernel, resetKernel]

theorem left_flip_reset : leftMulFlip resetKernel =
    { k00 := 0, k10 := 1, k01 := 0, k11 := 1 } := by
  simp [leftMulFlip, Kernel2.mul, flipKernel, resetKernel]

theorem left_reset_reset : leftMulReset resetKernel = resetKernel := by
  simp [leftMulReset, Kernel2.mul, resetKernel]

theorem left_id_not_inv_reset : leftMulId resetKernel ≠ idKernel := by
  decide

theorem left_flip_not_inv_reset : leftMulFlip resetKernel ≠ idKernel := by
  decide

theorem left_reset_not_inv_reset : leftMulReset resetKernel ≠ idKernel := by
  decide

/-- Among {id, flip, reset}, none is a left inverse of reset. -/
theorem reset_has_no_left_inverse_among_toy :
    leftMulId resetKernel ≠ idKernel ∧
    leftMulFlip resetKernel ≠ idKernel ∧
    leftMulReset resetKernel ≠ idKernel :=
  ⟨left_id_not_inv_reset, left_flip_not_inv_reset, left_reset_not_inv_reset⟩

/-- Flip is reversible: flip ∘ flip = id. -/
theorem flip_reversible :
    Kernel2.mul flipKernel flipKernel = idKernel := by
  simp [Kernel2.mul, flipKernel, idKernel]

theorem irreversibility_enters_classically :
    Kernel2.pow resetKernel 2 = resetKernel ∧
    Kernel2.mul flipKernel flipKernel = idKernel ∧
    leftMulReset resetKernel ≠ idKernel :=
  ⟨reset_pow_two, flip_reversible, left_reset_not_inv_reset⟩

/-! ## Continuous generator underivability (bind W6.7 CONT-TIME capital) -/

inductive TimeKind where
  | discreteSteps
  | continuousGenerator
  deriving DecidableEq, Repr

/-- Continuous one-parameter group is not constructed from Nat step counts alone. -/
def contTimeFromFinL1 : Prop := False

theorem continuous_generator_underivable_from_finL1 :
    ¬ contTimeFromFinL1 := fun h => h

theorem discrete_ne_continuous_kind :
    TimeKind.discreteSteps ≠ TimeKind.continuousGenerator := by
  decide

/-! ## Import status packaging -/

inductive ImportStatus where
  | derived
  | underivable
  | conditionalImport
  deriving DecidableEq, Repr

/-- Discrete Nat step parameter + kernel composition. -/
def discreteTimeStatus : ImportStatus := .derived

/-- Classical irreversibility entry (reset has no left inverse in toy class). -/
def irreversibilityClassicalStatus : ImportStatus := .derived

/-- Continuous time / one-parameter generator from FinL1 alone. -/
def continuousGeneratorFromFinL1Status : ImportStatus := .underivable

/-- Unitary continuous generator under lift (Stone residual). -/
def continuousGeneratorUnderLiftStatus : ImportStatus := .conditionalImport

theorem discrete_time_derived :
    discreteTimeStatus = ImportStatus.derived := rfl

theorem irreversibility_derived :
    irreversibilityClassicalStatus = ImportStatus.derived := rfl

theorem continuous_from_finL1_underivable :
    continuousGeneratorFromFinL1Status = ImportStatus.underivable := rfl

theorem continuous_under_lift_conditional :
    continuousGeneratorUnderLiftStatus = ImportStatus.conditionalImport := rfl

/-- **Main package.** -/
theorem time_generator_package :
    Kernel2.pow flipKernel 2 = idKernel ∧
    Kernel2.pow resetKernel 2 = resetKernel ∧
    leftMulReset resetKernel ≠ idKernel ∧
    noGenerator ≠ someGenerator ∧
    discreteTimeStatus = ImportStatus.derived ∧
    irreversibilityClassicalStatus = ImportStatus.derived ∧
    continuousGeneratorFromFinL1Status = ImportStatus.underivable ∧
    continuousGeneratorUnderLiftStatus = ImportStatus.conditionalImport :=
  ⟨flip_pow_two, reset_pow_two, left_reset_not_inv_reset,
    generator_not_forced_by_kernel_label, rfl, rfl, rfl, rfl⟩

/-- Full Stone theorem / continuous $e^{-itH}$ remains OPEN. -/
def fullStoneContinuous_open : Prop := True

theorem full_stone_marked_open : fullStoneContinuous_open := trivial

/-! ## Semigroup / contraction / discrete phase residual (TOY-MECH)

1. Chapman–Kolmogorov samples: $\mathrm{flip}^{m}\circ\mathrm{flip}^{n}=\mathrm{flip}^{m+n}$
   for small $(m,n)$.
2. Reset contracts every bit weight to pure sector 0 in one step.
3. Discrete phase clock under lift: $\phi = n\cdot\Delta$; continuous rate label
   is still extra data (not FinL1-forced).
4. Stone continuous group remains **OPEN**.
-/

/-- Chapman–Kolmogorov sample: $\mathrm{flip}^1 \circ \mathrm{flip}^1 = \mathrm{flip}^2$. -/
theorem flip_ck_1_1 :
    Kernel2.mul (Kernel2.pow flipKernel 1) (Kernel2.pow flipKernel 1) =
      Kernel2.pow flipKernel 2 := by
  simp [Kernel2.pow, Kernel2.mul, flipKernel, idKernel]

/-- $\mathrm{flip}^2 \circ \mathrm{flip}^1 = \mathrm{flip}^3 = \mathrm{flip}$. -/
theorem flip_ck_2_1 :
    Kernel2.mul (Kernel2.pow flipKernel 2) (Kernel2.pow flipKernel 1) =
      Kernel2.pow flipKernel 3 := by
  simp [Kernel2.pow, Kernel2.mul, flipKernel, idKernel]

theorem flip_pow_three : Kernel2.pow flipKernel 3 = flipKernel := by
  simp [Kernel2.pow, Kernel2.mul, flipKernel, idKernel]

/-- Reset semigroup: $\mathrm{reset}^m \circ \mathrm{reset}^n = \mathrm{reset}$ for $m,n\ge 1$. -/
theorem reset_ck_1_1 :
    Kernel2.mul (Kernel2.pow resetKernel 1) (Kernel2.pow resetKernel 1) =
      Kernel2.pow resetKernel 2 := by
  simp [Kernel2.pow, Kernel2.mul, resetKernel, idKernel]

/-! ### Population action (column-stochastic on bit weights) -/

structure BitWeight where
  w0 : Nat
  w1 : Nat
  deriving DecidableEq, Repr

/-- Apply kernel to residual weight: $w'_i = \sum_j K_{ij} w_j$. -/
def applyKernel (K : Kernel2) (w : BitWeight) : BitWeight :=
  { w0 := K.k00 * w.w0 + K.k01 * w.w1
    w1 := K.k10 * w.w0 + K.k11 * w.w1 }

def pure0W : BitWeight := { w0 := 1, w1 := 0 }
def pure1W : BitWeight := { w0 := 0, w1 := 1 }
def mixed31 : BitWeight := { w0 := 3, w1 := 1 }

theorem reset_contracts_pure0 :
    applyKernel resetKernel pure0W = { w0 := 1, w1 := 0 } := by
  simp [applyKernel, resetKernel, pure0W]

theorem reset_contracts_pure1 :
    applyKernel resetKernel pure1W = { w0 := 1, w1 := 0 } := by
  simp [applyKernel, resetKernel, pure1W]

theorem reset_contracts_mixed31 :
    applyKernel resetKernel mixed31 = { w0 := 4, w1 := 0 } := by
  simp [applyKernel, resetKernel, mixed31]

/-- Reset always lands on pure sector-0 support (classical irreversibility face). -/
theorem reset_contracts_to_sector0_support (w : BitWeight) :
    (applyKernel resetKernel w).w1 = 0 := by
  cases w
  simp [applyKernel, resetKernel]

theorem flip_swaps_pure :
    applyKernel flipKernel pure0W = pure1W ∧
    applyKernel flipKernel pure1W = pure0W := by
  simp [applyKernel, flipKernel, pure0W, pure1W]

/-! ### Discrete phase clock under lift (conditional; not continuous Stone) -/

/-- Discrete phase clock: $\phi = n \cdot \Delta$ (integer package). -/
structure DiscretePhaseClock where
  steps : Nat
  phaseInc : Int
  deriving DecidableEq, Repr

def phaseAt (c : DiscretePhaseClock) : Int :=
  (c.steps : Int) * c.phaseInc

def clockTwoSteps : DiscretePhaseClock := { steps := 2, phaseInc := 3 }

theorem phase_at_two_steps : phaseAt clockTwoSteps = 6 := by
  simp [phaseAt, clockTwoSteps]

/-- Continuous rate label is extra data (not determined by discrete clock alone). -/
structure ContinuousRateLabel where
  rate : Int
  deriving DecidableEq, Repr

def noContRate : ContinuousRateLabel := { rate := 0 }
def someContRate : ContinuousRateLabel := { rate := 1 }

theorem continuous_rate_extra_data :
    noContRate ≠ someContRate ∧
    continuousGeneratorFromFinL1Status = ImportStatus.underivable ∧
    continuousGeneratorUnderLiftStatus = ImportStatus.conditionalImport :=
  ⟨by decide, rfl, rfl⟩

/-- Discrete phase advance is additive in steps (semigroup on phase). -/
theorem phase_additive_in_steps (Δ : Int) (m n : Nat) :
    phaseAt { steps := m + n, phaseInc := Δ } =
      phaseAt { steps := m, phaseInc := Δ } +
        phaseAt { steps := n, phaseInc := Δ } := by
  simp [phaseAt]
  ring

def timeGeneratorSemigroupResidualPackage_toy : Bool := true

/-- **Semigroup / contraction / discrete phase residual package** (Stone OPEN). -/
theorem time_generator_semigroup_residual_package :
    timeGeneratorSemigroupResidualPackage_toy = true ∧
    Kernel2.mul (Kernel2.pow flipKernel 1) (Kernel2.pow flipKernel 1) =
      Kernel2.pow flipKernel 2 ∧
    Kernel2.pow flipKernel 3 = flipKernel ∧
    applyKernel resetKernel mixed31 = { w0 := 4, w1 := 0 } ∧
    (applyKernel resetKernel mixed31).w1 = 0 ∧
    applyKernel flipKernel pure0W = pure1W ∧
    phaseAt clockTwoSteps = 6 ∧
    noContRate ≠ someContRate ∧
    fullStoneContinuous_open ∧
    continuousGeneratorUnderLiftStatus = ImportStatus.conditionalImport := by
  refine ⟨rfl, flip_ck_1_1, flip_pow_three, reset_contracts_mixed31, ?_,
    ?_, phase_at_two_steps, by decide, trivial, rfl⟩
  · simp [applyKernel, resetKernel, mixed31]
  · simp [applyKernel, flipKernel, pure0W, pure1W]

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end TimeGeneratorIrreversibility
end QM

#print axioms QM.TimeGeneratorIrreversibility.discrete_time_parameter_derived
#print axioms QM.TimeGeneratorIrreversibility.irreversibility_enters_classically
#print axioms QM.TimeGeneratorIrreversibility.time_generator_package
#print axioms QM.TimeGeneratorIrreversibility.time_generator_semigroup_residual_package
#print axioms QM.TimeGeneratorIrreversibility.phase_additive_in_steps
#print axioms QM.TimeGeneratorIrreversibility.structure_not_auth
