import Mathlib.Topology.MetricSpace.Completion
import Mathlib.Topology.Instances.Rat
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic
namespace Coda.Q
open UniformSpace

theorem completion_complete (X : Type*) [MetricSpace X] : CompleteSpace (Completion X) :=
  inferInstance

theorem completion_dense (X : Type*) [MetricSpace X] :
    DenseRange ((↑) : X → Completion X) := Completion.denseRange_coe

theorem completion_isometry (X : Type*) [MetricSpace X] :
    Isometry ((↑) : X → Completion X) := Completion.coe_isometry

noncomputable def rationalCompletionToReal : Completion ℚ → ℝ :=
  Completion.extension ((↑) : ℚ → ℝ)

theorem rational_completion_coe (q : ℚ) : rationalCompletionToReal (q : Completion ℚ) = q :=
  Completion.extension_coe Rat.uniformContinuous_coe_real q

theorem rational_completion_isometry : Isometry rationalCompletionToReal := by
  have h : Isometry ((↑) : ℚ → ℝ) := Isometry.of_dist_eq (fun _ _ => rfl)
  exact h.completion_extension

theorem rational_completion_surjective : Function.Surjective rationalCompletionToReal := by
  have dense : DenseRange rationalCompletionToReal := by
    apply Rat.denseRange_cast.mono
    rintro _ ⟨q, rfl⟩
    exact ⟨(q : Completion ℚ), rational_completion_coe q⟩
  intro x
  have hx := dense x
  rw [rational_completion_isometry.isClosedEmbedding.isClosed_range.closure_eq] at hx
  exact hx

theorem rational_completion_bijective : Function.Bijective rationalCompletionToReal :=
  ⟨rational_completion_isometry.injective, rational_completion_surjective⟩

theorem extension_uniformly_continuous {X Y : Type*} [MetricSpace X] [MetricSpace Y]
    [CompleteSpace Y] (f : X → Y) : UniformContinuous (Completion.extension f) :=
  Completion.uniformContinuous_extension

theorem extension_agrees {X Y : Type*} [MetricSpace X] [MetricSpace Y] [CompleteSpace Y]
    (f : X → Y) (h : UniformContinuous f) (x : X) :
    Completion.extension f (x : Completion X) = f x := Completion.extension_coe h x

theorem enclosure_error (lo hi x : ℝ) (hl : lo ≤ x) (hh : x ≤ hi) :
    |x - (lo+hi)/2| ≤ (hi-lo)/2 := by
  rw [abs_le]; constructor <;> linarith

theorem extension_unique {X Y : Type*} [MetricSpace X] [MetricSpace Y] [CompleteSpace Y]
    (f : X → Y) (hf : UniformContinuous f) (g : Completion X → Y)
    (hg : UniformContinuous g) (agrees : ∀ x, f x = g (x : Completion X)) :
    Completion.extension f = g := Completion.extension_unique hf hg agrees

noncomputable def sqrtStep (lo hi : ℝ) : ℝ × ℝ :=
  let m := (lo+hi)/2
  if m*m ≤ 2 then (m,hi) else (lo,m)

theorem sqrt_step_enclosure (lo hi : ℝ) (h0 : 0 ≤ lo)
    (hl : lo ≤ Real.sqrt 2) (hh : Real.sqrt 2 ≤ hi) :
    0 ≤ (sqrtStep lo hi).1 ∧ (sqrtStep lo hi).1 ≤ Real.sqrt 2 ∧
    Real.sqrt 2 ≤ (sqrtStep lo hi).2 ∧
    (sqrtStep lo hi).2 - (sqrtStep lo hi).1 = (hi-lo)/2 := by
  have hs := Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num)
  have hp := Real.sqrt_nonneg (2:ℝ)
  have hm : 0 ≤ (lo+hi)/2 := by linarith
  unfold sqrtStep
  dsimp only
  split <;> dsimp
  · rename_i h
    refine ⟨hm,?_,hh,by ring⟩
    nlinarith
  · rename_i h
    refine ⟨h0,hl,?_,by ring⟩
    nlinarith
end Coda.Q

#print axioms Coda.Q.completion_complete
#print axioms Coda.Q.completion_dense
#print axioms Coda.Q.completion_isometry
#print axioms Coda.Q.rational_completion_coe
#print axioms Coda.Q.rational_completion_isometry
#print axioms Coda.Q.rational_completion_surjective
#print axioms Coda.Q.rational_completion_bijective
#print axioms Coda.Q.extension_uniformly_continuous
#print axioms Coda.Q.extension_agrees
#print axioms Coda.Q.extension_unique
#print axioms Coda.Q.enclosure_error
#print axioms Coda.Q.sqrt_step_enclosure
