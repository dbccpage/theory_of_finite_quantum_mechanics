import HilbertWalkGleason
import QuarticRivalSeparation
import Mathlib.Tactic.NormNum

/- Finite contract insufficiency and a fixed three-dimensional quartic rival.
   No universal Gleason uniqueness theorem is imported as a proved conclusion.
   AuthorityEffect: None. -/
namespace QuantumMechanics.PromptBornGap
theorem two_label_dimension_refusal :
    ¬ HilbertWalk.Gleason.GleasonDimAtLeastThree
      HilbertWalk.HWKernel.enumBool :=
  HilbertWalk.Gleason.two_label_host_not_gleason_dimension
theorem no_three_distinct_bool_labels :
    ¬ ∃ a b c : Bool, a ≠ b ∧ a ≠ c ∧ b ≠ c :=
  HilbertWalk.Gleason.no_three_pairwise_distinct_reports
theorem actual_weak_source_disagreement :
    HilbertWalk.SameContract.bornRule
      HilbertWalk.BornPairingBoundary.psi21
      (HilbertWalk.BornPairingBoundary.indicator false) = 4 ∧
    HilbertWalk.SameContract.swappedRule
      HilbertWalk.BornPairingBoundary.psi21
      (HilbertWalk.BornPairingBoundary.indicator false) = 1 :=
  HilbertWalk.SameContract.disagree_on_false_indicator
theorem source_quartic_deficit :
    (HilbertWalk.QuarticRivalSeparation.quartReadout
      HilbertWalk.QuarticRivalSeparation.e1
      HilbertWalk.QuarticRivalSeparation.psi +
     HilbertWalk.QuarticRivalSeparation.quartReadout
      HilbertWalk.QuarticRivalSeparation.e2
      HilbertWalk.QuarticRivalSeparation.psi) -
    (HilbertWalk.QuarticRivalSeparation.quartReadout
      HilbertWalk.QuarticRivalSeparation.p1
      HilbertWalk.QuarticRivalSeparation.psi +
     HilbertWalk.QuarticRivalSeparation.quartReadout
      HilbertWalk.QuarticRivalSeparation.p2
      HilbertWalk.QuarticRivalSeparation.psi) = 180000 :=
  HilbertWalk.QuarticRivalSeparation.quartic_frame_deficit
theorem normalized_three_coordinate_counterexample :
    (9/25 : ℚ)+(16/25)+0=1 ∧
    (9/25 : ℚ)^2+(16/25)^2+0=337/625 ∧
    (1 : ℚ)-337/625=288/625 ∧ (288/625 : ℚ)>0 := by norm_num
end QuantumMechanics.PromptBornGap
#print axioms QuantumMechanics.PromptBornGap.two_label_dimension_refusal
#print axioms QuantumMechanics.PromptBornGap.no_three_distinct_bool_labels
#print axioms QuantumMechanics.PromptBornGap.actual_weak_source_disagreement
#print axioms QuantumMechanics.PromptBornGap.source_quartic_deficit
#print axioms QuantumMechanics.PromptBornGap.normalized_three_coordinate_counterexample
