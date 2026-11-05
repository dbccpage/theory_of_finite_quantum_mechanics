import WitnessedDifference.PresentationCompletion
import Mathlib.Analysis.Complex.Circle
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.NumberTheory.Real.Irrational
import Mathlib.Topology.Algebra.GroupCompletion

/-!
# Circle characters and the completion of a metric presentation

The character extension below retains the additive homomorphism law. The
dyadic obstruction concerns the actual real subtype with its induced metric.
These results do not formalize Pontryagin duality or the compact-open topology.
-/

noncomputable section

namespace WitnessedDifference.PresentationDuality

open UniformSpace PresentationCompletion

universe u v

/-- Relative control for the unit circle, with its chordal metric. -/
def RelativeControlCircle {X : Type u} {P : Type v} [MetricSpace P]
    (p : X → P) (χ : X → Circle) : Prop := RelativeControl p χ

theorem character_pc_of_lipschitz {X : Type u} {P : Type v} [MetricSpace P]
    (p : X → P) (χ : X → Circle) (K : ℝ)
    (hK : ∀ x x', dist (χ x) (χ x') ≤ K * dist (p x) (p x')) :
    RelativeControl p χ := by
  intro ε hε
  have hpos : 0 < |K| + 1 := by positivity
  refine ⟨ε / (|K| + 1), div_pos hε hpos, ?_⟩
  intro x y hxy
  calc
    dist (χ x) (χ y) ≤ K * dist (p x) (p y) := hK x y
    _ ≤ (|K| + 1) * dist (p x) (p y) := by
      apply mul_le_mul_of_nonneg_right _ dist_nonneg
      linarith [le_abs_self K]
    _ < ε := (lt_div_iff₀' hpos).mp hxy

section CharacterExtension

variable {X : Type u} {P : Type v} [AddGroup X] [AddCommGroup P]
variable [MetricSpace P] [IsUniformAddGroup P]

/-- Fibre control descends a character to the actual presentation subgroup. -/
def imageCharacter (p : X →+ P) (χ : X →+ Additive Circle)
    (h : RelativeControl p χ) : p.range →+ Additive Circle where
  toFun := imageQuery p χ
  map_zero' := by
    have hp : imagePresentation p (0 : X) = (0 : p.range) := Subtype.ext p.map_zero
    rw [← hp, imageQuery_agrees p χ h, map_zero]
  map_add' s t := by
    obtain ⟨x, hx⟩ := s.property
    obtain ⟨y, hy⟩ := t.property
    have hs : imagePresentation p x = s := Subtype.ext hx
    have ht : imagePresentation p y = t := Subtype.ext hy
    have hst : imagePresentation p (x + y) = s + t := by
      apply Subtype.ext
      change p (x + y) = (s : P) + (t : P)
      rw [map_add, hx, hy]
    rw [← hst, ← hs, ← ht]
    simp only [imageQuery_agrees p χ h, map_add]

/-- Relative control gives a unique continuous homomorphic circle extension. -/
theorem unique_character_extension_to_completion (p : X →+ P)
    (χ : X →+ Additive Circle) (h : RelativeControl p χ) :
    ∃! g : Completion p.range →+ Additive Circle,
      Continuous g ∧ ∀ x,
        g ((p.rangeRestrict x : p.range) : Completion p.range) = χ x := by
  let f := imageCharacter p χ h
  have hf : UniformContinuous f := uniformContinuous_imageQuery p χ h
  refine ⟨f.extension hf.continuous, ⟨f.continuous_extension hf.continuous, ?_⟩, ?_⟩
  · intro x
    rw [f.extension_coe hf.continuous]
    exact imageQuery_agrees p χ h x
  · intro g hg
    have hu := (relativeControl_iff_unique_completion p χ).mp h
    have hgu : UniformContinuous (g : Completion p.range → Additive Circle) :=
      uniformContinuous_addMonoidHom_of_continuous hg.1
    have hfu : UniformContinuous (f.extension hf.continuous : Completion p.range → Additive Circle) :=
      uniformContinuous_addMonoidHom_of_continuous (f.continuous_extension hf.continuous)
    apply DFunLike.coe_injective
    exact hu.unique ⟨hgu, hg.2⟩
      ⟨hfu,
        fun x => (f.extension_coe hf.continuous _).trans (imageQuery_agrees p χ h x)⟩

end CharacterExtension

/-- Real dyadics, allowing integer exponents exactly as in the Lane E statement. -/
def RealDyadics : Set ℝ := {x | ∃ n k : ℤ, x = (k : ℝ) / (2 : ℝ) ^ n}

theorem sqrt_two_not_mem_realDyadics : Real.sqrt 2 ∉ RealDyadics := by
  rintro ⟨n, k, hk⟩
  apply irrational_sqrt_two
  refine ⟨(k : ℚ) / (2 : ℚ) ^ n, ?_⟩
  simpa only [Rat.cast_div, Rat.cast_intCast, Rat.cast_zpow, Rat.cast_ofNat] using hk.symm

/-- Dyadic floor approximations to sqrt(2) converge in the ambient real line. -/
theorem dyadic_sqrt_two_tendsto :
    Filter.Tendsto (fun n : ℕ => (⌊Real.sqrt 2 * (2 : ℝ) ^ n⌋₊ : ℝ) / (2 : ℝ) ^ n)
      Filter.atTop (nhds (Real.sqrt 2)) := by
  exact (tendsto_nat_floor_mul_div_atTop (Real.sqrt_nonneg 2)).comp
    (tendsto_pow_atTop_atTop_of_one_lt (by norm_num : (1 : ℝ) < 2))

/-- The induced real metric on the dyadic rationals is not complete. -/
theorem dyadic_subspace_not_complete : ¬ CompleteSpace RealDyadics := by
  intro h
  have hc : IsClosed RealDyadics := (completeSpace_coe_iff_isComplete.mp h).isClosed
  apply sqrt_two_not_mem_realDyadics
  apply hc.mem_of_tendsto dyadic_sqrt_two_tendsto
  exact Filter.Eventually.of_forall fun n =>
    ⟨(n : ℤ), (⌊Real.sqrt 2 * (2 : ℝ) ^ n⌋₊ : ℤ), by simp⟩

end WitnessedDifference.PresentationDuality
