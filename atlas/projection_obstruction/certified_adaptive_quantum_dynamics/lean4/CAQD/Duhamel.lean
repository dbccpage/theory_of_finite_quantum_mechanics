import CAQD.Core

namespace CAQD

/-- A step-wise quantum trajectory with residuals and propagators. -/
structure DiscreteTrajectory (V : OperatorSpace) where
  steps : Nat
  residual : Nat → V.Carrier        -- R_k at each time step k
  propagator_adj : Nat → V.Carrier → V.Carrier -- T†_{K-1-k} adjoint propagator
  contractive : ∀ k, V.PropagatorContractive (propagator_adj k)
  holder : V.HolderProperty

/-- Sum of residual trace norms up to step n: ∑_{k=0}^{n-1} ||R_k||_1. -/
def sumResidualNorms (V : OperatorSpace) (traj : DiscreteTrajectory V) : Nat → Nat
  | 0 => 0
  | k + 1 => sumResidualNorms V traj k + V.trace_norm (traj.residual k)

/-- Cumulative observable error bound B_O(K) along the trajectory:
    B_O(K) = ||O||_∞ * ∑_{k=0}^{K-1} ||R_k||_1. -/
def cumulativeBound (V : OperatorSpace) (traj : DiscreteTrajectory V) (O : V.Carrier) : Nat :=
  V.op_norm O * sumResidualNorms V traj traj.steps

/-- Exact observable error accumulation across steps:
    Tr(O * Δ_n) = ∑_{k=0}^{n-1} Tr( T†_{K-1-k}(O) * R_k ). -/
def stepPairing (V : OperatorSpace) (traj : DiscreteTrajectory V) (O : V.Carrier) : Nat → Int
  | 0 => 0
  | k + 1 => stepPairing V traj O k + V.trace_pairing (traj.propagator_adj k O) (traj.residual k)

/-- Sum of absolute pairing contributions: ∑_{k=0}^{n-1} |Tr(T†(O) * R_k)|. -/
def sumAbsPairing (V : OperatorSpace) (traj : DiscreteTrajectory V) (O : V.Carrier) : Nat → Nat
  | 0 => 0
  | k + 1 => sumAbsPairing V traj O k + Int.natAbs (V.trace_pairing (traj.propagator_adj k O) (traj.residual k))

/-- Absolute value of step pairing is bounded by sum of absolute values. -/
theorem abs_stepPairing_le_sumAbs (V : OperatorSpace) (traj : DiscreteTrajectory V) (O : V.Carrier) (n : Nat) :
    Int.natAbs (stepPairing V traj O n) ≤ sumAbsPairing V traj O n := by
  induction n with
  | zero =>
    dsimp [stepPairing, sumAbsPairing]
    exact Nat.le_refl 0
  | succ n ih =>
    dsimp [stepPairing, sumAbsPairing]
    have h_tri := Int.natAbs_add_le
      (stepPairing V traj O n)
      (V.trace_pairing (traj.propagator_adj n O) (traj.residual n))
    omega

/-- Theorem: Each step contribution is bounded by ||O||_∞ * ||R_k||_1. -/
theorem single_step_holder_bound (V : OperatorSpace) (traj : DiscreteTrajectory V) (O : V.Carrier) (k : Nat) :
    Int.natAbs (V.trace_pairing (traj.propagator_adj k O) (traj.residual k)) ≤
    V.op_norm O * V.trace_norm (traj.residual k) := by
  have h_holder := traj.holder (traj.propagator_adj k O) (traj.residual k)
  have h_contr := traj.contractive k O
  have h_mul_mono : V.op_norm (traj.propagator_adj k O) * V.trace_norm (traj.residual k) ≤
                    V.op_norm O * V.trace_norm (traj.residual k) := by
    apply Nat.mul_le_mul_right
    exact h_contr
  omega

/-- Lemma: Sum of absolute values is bounded by ||O||_∞ * sum of residual trace norms. -/
theorem sumAbsPairing_le_bound (V : OperatorSpace) (traj : DiscreteTrajectory V) (O : V.Carrier) (n : Nat) :
    sumAbsPairing V traj O n ≤ V.op_norm O * sumResidualNorms V traj n := by
  induction n with
  | zero =>
    dsimp [sumAbsPairing, sumResidualNorms]
    exact Nat.le_refl 0
  | succ m ih =>
    dsimp [sumAbsPairing, sumResidualNorms]
    have h_step := single_step_holder_bound V traj O m
    rw [Nat.mul_add]
    omega

/-- Master Duhamel Upper Bound Theorem:
    The absolute observable expectation error |Tr(O * Δ_K)| is bounded by B_O(K). -/
theorem duhamel_observable_bound (V : OperatorSpace) (traj : DiscreteTrajectory V) (O : V.Carrier) :
    Int.natAbs (stepPairing V traj O traj.steps) ≤ cumulativeBound V traj O := by
  dsimp [cumulativeBound]
  have h_abs := abs_stepPairing_le_sumAbs V traj O traj.steps
  have h_sum := sumAbsPairing_le_bound V traj O traj.steps
  omega

end CAQD
