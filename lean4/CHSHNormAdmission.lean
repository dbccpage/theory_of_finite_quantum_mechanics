import Mathlib.Analysis.InnerProductSpace.OfNorm
import Mathlib.Analysis.Normed.Lp.ProdLp
import Mathlib.Tactic

/-!
CHSH through a declared real norm and its dual unit ball.
AuthorityEffect: None. Real scalars, linear carrier, norm, full dual ball and
the unbiased binary probability rule are supplied. No composition theory is selected.
The sum/difference argument credits Bell/Quantum.lean in the external Bell package.
The reconstruction is Mathlib's Jordan-von Neumann theorem, not a new theorem.
-/
noncomputable section
open scoped ENNReal
namespace CHSHNormAdmission

variable {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]

/-- Exactly the contractivity condition for a linear functional in the dual unit ball. -/
def UnitEffect (f : X →ₗ[ℝ] ℝ) : Prop := ∀ x, |f x| ≤ ‖x‖

theorem unitEffect_iff_dual_bound (f : X →L[ℝ] ℝ) :
    UnitEffect f.toLinearMap ↔ ‖f‖ ≤ 1 := by
  constructor
  · intro h
    apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
    intro x
    simpa [Real.norm_eq_abs] using h x
  · intro h x
    have hb := f.le_opNorm x
    have hm := mul_le_mul_of_nonneg_right h (norm_nonneg x)
    simpa [Real.norm_eq_abs] using hb.trans hm

def continuousEffect (f : X →ₗ[ℝ] ℝ) (hf : UnitEffect f) : X →L[ℝ] ℝ :=
  f.mkContinuous 1 (fun x => by simpa [Real.norm_eq_abs] using hf x)

def chsh (f g : X →ₗ[ℝ] ℝ) (u v : X) : ℝ :=
  f u + f v + g u - g v

theorem correlator_bound (f : X →ₗ[ℝ] ℝ) (hf : UnitEffect f)
    (u : X) (hu : ‖u‖ ≤ 1) : |f u| ≤ 1 := (hf u).trans hu

theorem dual_sum_difference_bound (f g : X →ₗ[ℝ] ℝ)
    (hf : UnitEffect f) (hg : UnitEffect g) (u v : X) :
    |chsh f g u v| ≤ ‖u + v‖ + ‖u - v‖ := by
  have h : chsh f g u v = f (u + v) + g (u - v) := by
    simp only [chsh, map_add, map_sub]; ring
  rw [h]
  exact (abs_add_le _ _).trans (add_le_add (hf _) (hg _))

theorem algebraic_bound (f g : X →ₗ[ℝ] ℝ)
    (hf : UnitEffect f) (hg : UnitEffect g) (u v : X)
    (hu : ‖u‖ ≤ 1) (hv : ‖v‖ ≤ 1) : |chsh f g u v| ≤ 4 := by
  have h := dual_sum_difference_bound f g hf hg u v
  have h1 := norm_add_le u v
  have h2 := norm_sub_le u v
  linarith

/-- This law is an explicit additional premise, not a property of arbitrary norms. -/
def Parallelogram (X : Type*) [NormedAddCommGroup X] : Prop :=
  ∀ u v : X, ‖u + v‖ ^ 2 + ‖u - v‖ ^ 2 = 2 * (‖u‖ ^ 2 + ‖v‖ ^ 2)

theorem chsh_sq_le_eight (hP : Parallelogram X)
    (f g : X →ₗ[ℝ] ℝ) (hf : UnitEffect f) (hg : UnitEffect g)
    (u v : X) (hu : ‖u‖ ≤ 1) (hv : ‖v‖ ≤ 1) :
    |chsh f g u v| ^ 2 ≤ 8 := by
  have hb := dual_sum_difference_bound f g hf hg u v
  have hs := sq_le_sq₀ (abs_nonneg (chsh f g u v))
    (add_nonneg (norm_nonneg (u+v)) (norm_nonneg (u-v)))
  have hu2 : ‖u‖ ^ 2 ≤ 1 := by nlinarith [norm_nonneg u]
  have hv2 : ‖v‖ ^ 2 ≤ 1 := by nlinarith [norm_nonneg v]
  have hp := hP u v
  have ht := hs.mpr hb
  nlinarith [sq_nonneg (‖u+v‖ - ‖u-v‖)]

theorem chsh_le_two_sqrt_two (hP : Parallelogram X)
    (f g : X →ₗ[ℝ] ℝ) (hf : UnitEffect f) (hg : UnitEffect g)
    (u v : X) (hu : ‖u‖ ≤ 1) (hv : ‖v‖ ≤ 1) :
    |chsh f g u v| ≤ 2 * Real.sqrt 2 := by
  have h := chsh_sq_le_eight hP f g hf hg u v hu hv
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num), Real.sqrt_nonneg (2:ℝ)]

@[instance_reducible]
def reconstructedInnerProduct (hP : Parallelogram X) : InnerProductSpace ℝ X :=
  InnerProductSpace.ofNorm (𝕜 := ℝ) (fun u v => by simpa [pow_two] using hP u v)

theorem reconstructed_polarization (hP : Parallelogram X) (u v : X) :
    letI := reconstructedInnerProduct hP
    inner ℝ u v = (‖u+v‖^2 - ‖u-v‖^2) / 4 := by
  let := reconstructedInnerProduct hP
  have ha := norm_add_sq_real u v
  have hs := norm_sub_sq_real u v
  nlinarith

omit [NormedSpace ℝ X] in
theorem inner_product_implies_parallelogram [InnerProductSpace ℝ X] :
    Parallelogram X := by
  intro u v
  exact parallelogram_law_with_norm ℝ u v

/-- The binary probability prescription is an admission. -/
def probability (e a b : ℝ) : ℝ := (1 + a*b*e)/4
def Sign (a : ℝ) : Prop := a = 1 ∨ a = -1

theorem probability_nonnegative (e a b : ℝ) (he : |e| ≤ 1)
    (ha : Sign a) (hb : Sign b) : 0 ≤ probability e a b := by
  have he' := abs_le.mp he
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;>
    dsimp [probability] <;> linarith

theorem probability_normalized (e : ℝ) :
    probability e 1 1 + probability e 1 (-1) +
    probability e (-1) 1 + probability e (-1) (-1) = 1 := by
  unfold probability; ring

theorem marginal_alice (e a : ℝ) :
    probability e a 1 + probability e a (-1) = 1/2 := by
  unfold probability; ring

theorem marginal_bob (e b : ℝ) :
    probability e 1 b + probability e (-1) b = 1/2 := by
  unfold probability; ring

theorem probability_recovers_correlator (e : ℝ) :
    probability e 1 1 - probability e 1 (-1) -
    probability e (-1) 1 + probability e (-1) (-1) = e := by
  unfold probability; ring

theorem deterministic_local_bound (a b c d : ℝ)
    (ha : Sign a) (hb : Sign b) (hc : Sign c) (hd : Sign d) :
    |a*c+a*d+b*c-b*d| ≤ 2 := by
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;>
    rcases hc with rfl | rfl <;> rcases hd with rfl | rfl <;> norm_num

theorem positive_mixture_bound {I : Type*} [Fintype I] (w s : I → ℝ)
    (hw : ∀ i, 0 ≤ w i) (ht : ∑ i, w i = 1) (hs : ∀ i, |s i| ≤ 2) :
    |∑ i, w i * s i| ≤ 2 := by
  calc
    _ ≤ ∑ i, |w i * s i| := Finset.abs_sum_le_sum_abs _ _
    _ = ∑ i, w i * |s i| := by simp_rw [abs_mul, abs_of_nonneg (hw _)]
    _ ≤ ∑ i, w i * 2 := Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_left (hs i) (hw i)
    _ = 2 := by rw [← Finset.sum_mul, ht]; ring

abbrev Plane (p : ENNReal) := WithLp p (ℝ × ℝ)
def effect (p : ENNReal) (a b : ℝ) : Plane p →ₗ[ℝ] ℝ where
  toFun x := a*x.fst+b*x.snd
  map_add' x y := by simp; ring
  map_smul' c x := by simp; ring

theorem l1_effect_plus : UnitEffect (effect 1 1 1) := by
  intro x
  simpa [effect, WithLp.prod_norm_eq_of_L1, Real.norm_eq_abs] using abs_add_le x.fst x.snd

theorem l1_effect_minus : UnitEffect (effect 1 1 (-1)) := by
  intro x
  simpa [effect, WithLp.prod_norm_eq_of_L1, Real.norm_eq_abs, sub_eq_add_neg] using abs_sub x.fst x.snd

theorem l1_pr_witness :
    ‖(WithLp.toLp 1 (1,0) : Plane 1)‖ = 1 ∧
    ‖(WithLp.toLp 1 (0,1) : Plane 1)‖ = 1 ∧
    chsh (effect 1 1 1) (effect 1 1 (-1))
      (WithLp.toLp 1 (1,0)) (WithLp.toLp 1 (0,1)) = 4 := by
  norm_num [WithLp.prod_norm_eq_of_L1, effect, chsh]

theorem l1_fails_parallelogram : ¬ Parallelogram (Plane 1) := by
  intro hp
  have h := hp (WithLp.toLp 1 (1,0)) (WithLp.toLp 1 (0,1))
  norm_num [WithLp.prod_norm_eq_of_L1] at h

theorem linfty_effect_first : UnitEffect (effect ∞ 1 0) := by
  intro x
  simp [effect, WithLp.prod_norm_eq_sup, Real.norm_eq_abs]

theorem linfty_effect_second : UnitEffect (effect ∞ 0 1) := by
  intro x
  simp [effect, WithLp.prod_norm_eq_sup, Real.norm_eq_abs]

theorem linfty_pr_witness :
    ‖(WithLp.toLp ∞ (1,1) : Plane ∞)‖ = 1 ∧
    ‖(WithLp.toLp ∞ (1,-1) : Plane ∞)‖ = 1 ∧
    chsh (effect ∞ 1 0) (effect ∞ 0 1)
      (WithLp.toLp ∞ (1,1)) (WithLp.toLp ∞ (1,-1)) = 4 := by
  norm_num [WithLp.prod_norm_eq_sup, effect, chsh]

theorem l2_effect (a b : ℝ) (hab : a^2+b^2 ≤ 1) : UnitEffect (effect 2 a b) := by
  intro x
  have hcs : (a*x.fst+b*x.snd)^2 ≤ (a^2+b^2)*(x.fst^2+x.snd^2) := by
    nlinarith [sq_nonneg (a*x.snd-b*x.fst)]
  have hn : ‖x‖^2 = x.fst^2+x.snd^2 := by
    rw [WithLp.prod_norm_eq_of_L2, Real.sq_sqrt]
    · simp [Real.norm_eq_abs, sq_abs]
    · positivity
  have hm := mul_le_mul_of_nonneg_right hab (add_nonneg (sq_nonneg x.fst) (sq_nonneg x.snd))
  change |a*x.fst+b*x.snd| ≤ ‖x‖
  nlinarith [sq_abs (a*x.fst+b*x.snd), norm_nonneg x]

theorem l2_norm_sq (x : Plane 2) : ‖x‖^2 = x.fst^2+x.snd^2 := by
  rw [WithLp.prod_norm_eq_of_L2, Real.sq_sqrt]
  · simp [Real.norm_eq_abs, sq_abs]
  · positivity

theorem l2_parallelogram : Parallelogram (Plane 2) := by
  intro u v
  simp only [l2_norm_sq, WithLp.add_fst, WithLp.add_snd, WithLp.sub_fst, WithLp.sub_snd]
  ring

theorem l2_upper_bound (f g : Plane 2 →ₗ[ℝ] ℝ)
    (hf : UnitEffect f) (hg : UnitEffect g) (u v : Plane 2)
    (hu : ‖u‖ ≤ 1) (hv : ‖v‖ ≤ 1) : |chsh f g u v| ≤ 2 * Real.sqrt 2 :=
  chsh_le_two_sqrt_two l2_parallelogram f g hf hg u v hu hv

theorem l2_witness_effects :
    UnitEffect (effect 2 (Real.sqrt 2/2) (Real.sqrt 2/2)) ∧
    UnitEffect (effect 2 (Real.sqrt 2/2) (-Real.sqrt 2/2)) := by
  have h := Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num)
  constructor <;> apply l2_effect <;> nlinarith

theorem l2_attainment :
    ‖(WithLp.toLp 2 (1,0) : Plane 2)‖ = 1 ∧
    ‖(WithLp.toLp 2 (0,1) : Plane 2)‖ = 1 ∧
    chsh (effect 2 (Real.sqrt 2/2) (Real.sqrt 2/2))
      (effect 2 (Real.sqrt 2/2) (-Real.sqrt 2/2))
      (WithLp.toLp 2 (1,0)) (WithLp.toLp 2 (0,1)) = 2 * Real.sqrt 2 := by
  norm_num [WithLp.prod_norm_eq_of_L2, effect, chsh]
  ring

#print axioms unitEffect_iff_dual_bound
#print axioms correlator_bound
#print axioms dual_sum_difference_bound
#print axioms algebraic_bound
#print axioms chsh_sq_le_eight
#print axioms chsh_le_two_sqrt_two
#print axioms reconstructed_polarization
#print axioms inner_product_implies_parallelogram
#print axioms probability_nonnegative
#print axioms probability_normalized
#print axioms marginal_alice
#print axioms marginal_bob
#print axioms probability_recovers_correlator
#print axioms deterministic_local_bound
#print axioms positive_mixture_bound
#print axioms l1_effect_plus
#print axioms l1_effect_minus
#print axioms l1_pr_witness
#print axioms l1_fails_parallelogram
#print axioms linfty_effect_first
#print axioms linfty_effect_second
#print axioms linfty_pr_witness
#print axioms l2_effect
#print axioms l2_norm_sq
#print axioms l2_parallelogram
#print axioms l2_upper_bound
#print axioms l2_witness_effects
#print axioms l2_attainment

end CHSHNormAdmission
