/-!
Two-label slice of GP-IMPORT-GLEASON.
AuthorityEffect: None.
The module has no import. It records the dimension failure on two labels
and the two readout pairings at amplitudes 2 and 1. It does not discharge
Born uniqueness under Gleason hypotheses.
-/

namespace CampaignGpImportGleason

def weight (a : Int) : Int := a * a

def amp : Bool → Int
  | false => 2
  | true => 1

def unitEffect : Bool → Int
  | _ => 1

def falseIndicator : Bool → Int
  | false => 1
  | true => 0

def swapEffect (e : Bool → Int) : Bool → Int :=
  fun q => e (!q)

def pair (w e : Bool → Int) : Int :=
  w false * e false + w true * e true

def born (e : Bool → Int) : Int :=
  pair (fun q => weight (amp q)) e

def swapped (e : Bool → Int) : Int :=
  pair (fun q => weight (amp q)) (swapEffect e)

theorem twoLabelsBelowThree : (2 : Nat) < 3 := by decide

theorem dimensionExtraFails : ¬ ((3 : Nat) ≤ 2) := by decide

theorem noThreeDistinctLabels :
    ¬ ∃ a b c : Bool, a ≠ b ∧ a ≠ c ∧ b ≠ c := by decide

theorem squaredWeights :
    weight (amp false) = 4 ∧ weight (amp true) = 1 := by decide

theorem unitPairingsAgree :
    born unitEffect = 5 ∧ swapped unitEffect = 5 := by decide

theorem falseIndicatorDisagrees :
    born falseIndicator = 4 ∧
      swapped falseIndicator = 1 ∧
      born falseIndicator ≠ swapped falseIndicator := by decide

#print axioms twoLabelsBelowThree
#print axioms dimensionExtraFails
#print axioms noThreeDistinctLabels
#print axioms squaredWeights
#print axioms unitPairingsAgree
#print axioms falseIndicatorDisagrees

end CampaignGpImportGleason
