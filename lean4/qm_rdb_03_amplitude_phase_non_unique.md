import «l010_01_born_redundancy»

/-!
RDB-03: amplitude/sign non-uniqueness.

Normalized residual weights do not determine phase/coherence data. This file
uses the finite PaperQF002 sign-flip witness: the local squared-probability
diagnostic is unchanged, while a mixing/coherence-sensitive diagnostic changes.
-/

namespace QM

namespace RDB03

noncomputable section

def unitPositivePhase : ℚ × ℚ :=
  ((1 : ℚ), (1 : ℚ))

def unitNegativePhase : ℚ × ℚ :=
  ((1 : ℚ), (-1 : ℚ))

theorem signPhase_same_sector_probabilities :
    PaperQF002.pairSquaredDirectProb unitPositivePhase =
      PaperQF002.pairSquaredDirectProb unitNegativePhase := by
  simpa [unitPositivePhase, unitNegativePhase] using
    PaperQF002.pairSquaredDirectProb_sign_flip 1 1

theorem signPhase_amplitudes_distinct :
    unitPositivePhase ≠ unitNegativePhase := by
  intro h
  have hsnd := congrArg Prod.snd h
  norm_num [unitPositivePhase, unitNegativePhase] at hsnd

/-- Same residual-sector weights do not determine the sign/phase witness. -/
theorem sectorProbabilities_do_not_determine_phase_sign :
    PaperQF002.pairSquaredDirectProb unitPositivePhase =
        PaperQF002.pairSquaredDirectProb unitNegativePhase ∧
      unitPositivePhase ≠ unitNegativePhase := by
  exact ⟨signPhase_same_sector_probabilities, signPhase_amplitudes_distinct⟩

/-- A coherence-sensitive mixing rule can distinguish sign/phase witnesses that
the sector-weight diagnostic identifies. -/
theorem sameWeights_but_mixing_changes_descended_weights :
    PaperQF002.phaseBlind₂ (1 : ℚ) 1 1 (-1) ∧
      PaperQF002.twoRowMixWeights 1 1 ≠ PaperQF002.twoRowMixWeights 1 (-1) := by
  simpa using
    PaperQF002.sign_phase_same_weights_but_mixing_changes_descended_weights

theorem mixing_outputs_explicitly_split :
    PaperQF002.twoRowMixWeights 1 1 = ((4 : ℚ), 0) ∧
      PaperQF002.twoRowMixWeights 1 (-1) = (0, (4 : ℚ)) := by
  simpa using PaperQF002.sign_phase_mixing_redistributes_weights

end

end RDB03

end QM

#print axioms QM.RDB03.sectorProbabilities_do_not_determine_phase_sign
#print axioms QM.RDB03.sameWeights_but_mixing_changes_descended_weights
