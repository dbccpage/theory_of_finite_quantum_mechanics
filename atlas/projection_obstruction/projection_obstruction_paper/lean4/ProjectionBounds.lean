import Mathlib.Analysis.Normed.Operator.NormedSpace
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

noncomputable section
open scoped BigOperators
namespace ProjectionBounds

/-- A lower rate supported by a two-sided error enclosure. -/
def lowerRate (observed radius : ℝ) : ℝ := max 0 (observed - radius)

theorem lowerRate_le (actual observed radius : ℝ) (ha : 0 ≤ actual)
    (herr : |observed - actual| ≤ radius) : lowerRate observed radius ≤ actual := by
  apply max_le ha
  linarith [(abs_le.mp herr).2]

theorem uncertain_onset (defect actual observed radius curvature time : ℝ)
    (hd : 0 ≤ defect) (ha : 0 ≤ actual) (ht : 0 ≤ time)
    (herr : |observed - actual| ≤ radius)
    (honset : actual * time - curvature * time ^ 2 ≤ defect) :
    max 0 (lowerRate observed radius * time - curvature * time ^ 2) ≤ defect := by
  apply max_le hd
  have := mul_le_mul_of_nonneg_right (lowerRate_le actual observed radius ha herr) ht
  linarith

theorem half_slope_window (rate curvature time : ℝ) (hk : 0 < curvature)
    (ht : 0 ≤ time) (hwindow : time ≤ rate / (2 * curvature)) :
    rate * time / 2 ≤ rate * time - curvature * time ^ 2 := by
  have h := (le_div_iff₀ (by positivity : 0 < 2 * curvature)).mp hwindow
  nlinarith [mul_nonneg ht (by linarith : 0 ≤ rate - 2 * curvature * time)]

theorem zero_curvature (rate time : ℝ) : rate * time - 0 * time ^ 2 = rate * time := by ring

theorem uncertainty_explains_rate (observed radius : ℝ) (h : observed ≤ radius) :
    lowerRate observed radius = 0 := max_eq_left (sub_nonpos.mpr h)

/-- Exact algebraic characterization; the horizon is a separate premise. -/
theorem correction_window_iff (initial rate reserve tolerance time : ℝ) (hr : 0 < rate) :
    initial + rate * time + reserve ≤ tolerance ↔
      time ≤ (tolerance - initial - reserve) / rate := by
  rw [le_div_iff₀ hr]
  constructor <;> intro h <;> nlinarith

theorem zero_rate_window (initial reserve tolerance time : ℝ) :
    initial + 0 * time + reserve ≤ tolerance ↔ initial + reserve ≤ tolerance := by simp

theorem safe_horizon (initial rate reserve tolerance horizon time : ℝ)
    (hr : 0 < rate)
    (ht : time ≤ min horizon ((tolerance - initial - reserve) / rate)) :
    time ≤ horizon ∧ initial + rate * time + reserve ≤ tolerance := by
  exact ⟨(le_min_iff.mp ht).1,
    (correction_window_iff initial rate reserve tolerance time hr).mpr (le_min_iff.mp ht).2⟩

theorem exhausted_budget (initial rate reserve tolerance time : ℝ)
    (h : tolerance < initial + reserve) (hr : 0 ≤ rate) (ht : 0 ≤ time) :
    tolerance < initial + rate * time + reserve := by nlinarith [mul_nonneg hr ht]

section NormBounds
variable {E : Type*} [NormedAddCommGroup E]

/-- Finite transported correction jumps, with arbitrary normed carrier. The
continuous variation-of-constants identity is an explicit input, not an axiom. -/
theorem transported_jump_bound {I : Type*} [Fintype I]
    (error initial integral : E) (transport : I → E → E) (jump : I → E)
    (initialBound integralBound : ℝ)
    (hformula : error = initial + integral - ∑ i, transport i (jump i))
    (hinit : ‖initial‖ ≤ initialBound) (hint : ‖integral‖ ≤ integralBound)
    (hcontract : ∀ i x, ‖transport i x‖ ≤ ‖x‖) :
    ‖error‖ ≤ initialBound + integralBound + ∑ i, ‖jump i‖ := by
  rw [hformula]
  calc
    _ ≤ ‖initial + integral‖ + ‖∑ i, transport i (jump i)‖ := norm_sub_le _ _
    _ ≤ (‖initial‖ + ‖integral‖) + ∑ i, ‖transport i (jump i)‖ :=
      add_le_add (norm_add_le _ _) (norm_sum_le _ _)
    _ ≤ _ := add_le_add (add_le_add hinit hint) (Finset.sum_le_sum (fun i _ => hcontract i _))

/-- Actual update discrepancy plus a correction displacement; no renormalization
or cancellation is silently assumed. -/
theorem corrected_step (F : E → E) (exact approx next correction : E)
    (initial rate time integration jump : ℝ)
    (hcontract : ∀ x y, ‖F x - F y‖ ≤ ‖x - y‖)
    (hinit : ‖exact - approx‖ ≤ initial)
    (hres : ‖F approx - next‖ ≤ rate * time + integration)
    (hj : ‖correction‖ ≤ jump) :
    ‖F exact - (next + correction)‖ ≤ initial + rate * time + integration + jump := by
  have h1 := norm_sub_le_norm_sub_add_norm_sub (F exact) (F approx) next
  have h2 := norm_sub_le_norm_sub_add_norm_sub (F exact) next (next + correction)
  have hc : ‖next - (next + correction)‖ = ‖correction‖ := by simp
  rw [hc] at h2
  linarith [hcontract exact approx]

/-- Telescoping the factor-replacement path is the source of the k factor. -/
theorem path_bound (path : ℕ → E) (k : ℕ) :
    ‖path 0 - path k‖ ≤ ∑ i ∈ Finset.range k, ‖path i - path (i + 1)‖ := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [Finset.sum_range_succ]
    exact (norm_sub_le_norm_sub_add_norm_sub (path 0) (path k) (path (k+1))).trans (add_le_add ih le_rfl)

theorem factor_replacement_bound (path : ℕ → E) (k : ℕ) (ε : ℝ)
    (hstep : ∀ i < k, ‖path i - path (i + 1)‖ ≤ ε) :
    ‖path 0 - path k‖ ≤ k * ε := by
  apply (path_bound path k).trans
  calc
    _ ≤ ∑ _i ∈ Finset.range k, ε := Finset.sum_le_sum (fun i hi => hstep i (Finset.mem_range.mp hi))
    _ = _ := by simp

theorem defect_difference (x y px py : E) :
    |‖x - px‖ - ‖y - py‖| ≤ ‖x - y‖ + ‖px - py‖ := by
  have h := abs_norm_sub_norm_le (x - px) (y - py)
  have heq : x - px - (y - py) = (x - y) - (px - py) := by abel
  rw [heq] at h
  exact h.trans (norm_sub_le _ _)

/-- The path endpoints are the actual product retractions. Its step estimates
are precisely the tensor norm and partial trace obligations of an instantiation. -/
theorem product_defect_uncertainty (x y px py : E) (path : ℕ → E) (k : ℕ) (ε : ℝ)
    (hxy : ‖x - y‖ ≤ ε) (hfirst : path 0 = px) (hlast : path k = py)
    (hstep : ∀ i < k, ‖path i - path (i + 1)‖ ≤ ‖x - y‖) :
    |‖x - px‖ - ‖y - py‖| ≤ (k + 1 : ℝ) * ε := by
  have hp := factor_replacement_bound path k ‖x-y‖ hstep
  rw [hfirst, hlast] at hp
  calc
    _ ≤ ‖x-y‖ + ‖px-py‖ := defect_difference x y px py
    _ ≤ (k + 1 : ℝ) * ‖x-y‖ := by nlinarith
    _ ≤ _ := mul_le_mul_of_nonneg_left hxy (by positivity)

theorem observed_defect_interval (actual reference observed stateRadius evaluationRadius : ℝ)
    (ha : 0 ≤ actual) (hs : |actual - reference| ≤ stateRadius)
    (he : |observed - reference| ≤ evaluationRadius) :
    max 0 (observed - stateRadius - evaluationRadius) ≤ actual ∧
      actual ≤ observed + stateRadius + evaluationRadius := by
  have h1 := abs_le.mp hs
  have h2 := abs_le.mp he
  exact ⟨max_le ha (by linarith), by linarith⟩

/-- Covers a declared observation map without assuming it is a coboundary. -/
theorem observed_residual_bound {F : Type*} [NormedAddCommGroup F]
    (observe : E → F) (x y px py : E) (L ε : ℝ)
    (hL : 0 ≤ L) (hobs : ∀ a b, ‖observe a - observe b‖ ≤ L * ‖a-b‖)
    (hres : ‖(x-px)-(y-py)‖ ≤ ε) :
    ‖observe (x-px) - observe (y-py)‖ ≤ L * ε :=
  (hobs _ _).trans (mul_le_mul_of_nonneg_left hres hL)


/-- A finite sequence of certified updates preserves the accumulated envelope. -/
theorem accumulated_budget (error increment : ℕ → ℝ) (initial : ℝ)
    (h0 : error 0 ≤ initial) (hstep : ∀ n, error (n+1) ≤ error n + increment n)
    (n : ℕ) : error n ≤ initial + ∑ i ∈ Finset.range n, increment i := by
  induction n with
  | zero => simpa using h0
  | succ n ih =>
    rw [Finset.sum_range_succ]
    linarith [hstep n]

theorem residual_difference (x y px py : E) :
    ‖(x-px)-(y-py)‖ ≤ ‖x-y‖ + ‖px-py‖ := by
  have h : (x-px)-(y-py) = (x-y)-(px-py) := by abel
  rw [h]
  exact norm_sub_le _ _

theorem product_residual_uncertainty (x y px py : E) (path : ℕ → E) (k : ℕ) (ε : ℝ)
    (hxy : ‖x-y‖ ≤ ε) (hfirst : path 0 = px) (hlast : path k = py)
    (hstep : ∀ i < k, ‖path i-path (i+1)‖ ≤ ‖x-y‖) :
    ‖(x-px)-(y-py)‖ ≤ (k+1 : ℝ)*ε := by
  have hp := factor_replacement_bound path k ‖x-y‖ hstep
  rw [hfirst, hlast] at hp
  calc
    _ ≤ ‖x-y‖ + ‖px-py‖ := residual_difference x y px py
    _ ≤ (k+1 : ℝ)*‖x-y‖ := by nlinarith
    _ ≤ _ := mul_le_mul_of_nonneg_left hxy (by positivity)

example : (1/100 : ℝ) + (1/10)*(3/4) + 3/200 ≤ 1/10 := by norm_num
example : ¬ ((1/100 : ℝ) + (1/10)*1 + 3/200 ≤ 1/10) := by norm_num
example : lowerRate (1/50) (1/50) = 0 := by norm_num [lowerRate]

end NormBounds
end ProjectionBounds
