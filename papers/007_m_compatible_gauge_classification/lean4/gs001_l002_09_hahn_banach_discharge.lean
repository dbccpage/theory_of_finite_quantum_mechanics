/-
Paper 002, Tier 9: Hahn-Banach discharge.

The Tier-1 maximal-symmetry theorem isolates the only analytic dependency as a
norming-functional hypothesis. Mathlib's Hahn-Banach corollary
`exists_dual_vector` supplies exactly that hypothesis for every unit vector, so
the direction-independence and proportionality theorems no longer need a
user-supplied norming-functional package.
-/

import «gs001_l002_06_maximal_symmetry»
import Mathlib.Analysis.Normed.Module.HahnBanach

namespace PaperGS001

noncomputable section

variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]

theorem norming_functional_from_hahn_banach
    (u : V) (hu : ‖u‖ = 1) :
    ∃ f : V →L[ℝ] ℝ, ‖f‖ = 1 ∧ f u = 1 := by
  have hne : ‖u‖ ≠ 0 := by
    rw [hu]
    norm_num
  rcases exists_dual_vector ℝ u hne with ⟨f, hf_norm, hf_u⟩
  exact ⟨f, hf_norm, by simpa [hu] using hf_u⟩

theorem direction_independence_hahn_banach
    (G : MaximalGauge V)
    {u v : V} (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    G.j u = G.j v := by
  exact
    MaximalGauge.direction_independence_tier1 G
      norming_functional_from_hahn_banach hu hv

theorem gauge_proportional_hahn_banach
    (G : MaximalGauge V)
    (hV : ∃ x : V, x ≠ 0) :
    ∃ c : ℝ, 0 < c ∧ ∀ x : V, G.j x = c * ‖x‖ := by
  exact
    MaximalGauge.gauge_proportional_tier1 G
      norming_functional_from_hahn_banach hV

#print axioms PaperGS001.norming_functional_from_hahn_banach
#print axioms PaperGS001.direction_independence_hahn_banach
#print axioms PaperGS001.gauge_proportional_hahn_banach

end

end PaperGS001
