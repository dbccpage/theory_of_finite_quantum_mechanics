
namespace FableHilbertWalk20260819.H063


def single_qubit_dimension : Nat := 2

def choi_dim_d2 : Nat := single_qubit_dimension * single_qubit_dimension

theorem choi_dimension_is_four : choi_dim_d2 = 4 := by
  rfl

def max_kraus_rank_d2 : Nat := 4

theorem kraus_rank_bound_is_four : max_kraus_rank_d2 = 4 := by
  rfl


structure Choi4 where
  d0 : Int
  d1 : Int
  d2 : Int
  d3 : Int
  deriving DecidableEq, Repr

def Choi4.isPsdDiag (c : Choi4) : Prop :=
  c.d0 ≥ 0 ∧ c.d1 ≥ 0 ∧ c.d2 ≥ 0 ∧ c.d3 ≥ 0

def depolChoiDiag1_3 : Choi4 := ⟨9, 1, 1, 1⟩

theorem depol_choi_1_3_psd : depolChoiDiag1_3.isPsdDiag := by
  dsimp [Choi4.isPsdDiag, depolChoiDiag1_3]
  decide

def depolChoiDiag1_7 : Choi4 := ⟨25, 1, 1, 1⟩

theorem depol_choi_1_7_psd : depolChoiDiag1_7.isPsdDiag := by
  dsimp [Choi4.isPsdDiag, depolChoiDiag1_7]
  decide


structure ChannelDilation where
  channel_id : String
  base_conductor : Nat
  choi_eigenvalue_squarefree_factor : Nat
  dilation_conductor : Nat
  requires_extension : Bool
  escalates_beyond_120 : Bool
  deriving DecidableEq, Repr

def depol_1_3 : ChannelDilation :=
  ⟨"depol_1_3", 1, 3, 12, true, false⟩

theorem depol_1_3_conductor_is_twelve : depol_1_3.dilation_conductor = 12 := by
  rfl

theorem depol_1_3_divides_120 : 120 % depol_1_3.dilation_conductor = 0 := by
  rfl

def depol_1_7 : ChannelDilation :=
  ⟨"depol_1_7", 1, 7, 28, true, true⟩

theorem depol_1_7_conductor_is_twenty_eight : depol_1_7.dilation_conductor = 28 := by
  rfl

theorem depol_1_7_not_divides_120 : 120 % depol_1_7.dilation_conductor ≠ 0 := by
  decide

theorem stinespring_requires_extension_verified :
    depol_1_3.requires_extension = true ∧ depol_1_7.requires_extension = true := by
  decide

theorem depol_1_7_escalates_beyond_120_verified :
    depol_1_7.escalates_beyond_120 = true := by
  decide


inductive TargetChannel : Type
  | ch_ident : TargetChannel
  | ch_bitflip : TargetChannel
  | ch_phaseflip : TargetChannel
  | ch_bitphase : TargetChannel
  | ch_depol_1_3 : TargetChannel
  | ch_depol_1_7 : TargetChannel
  | ch_meas : TargetChannel
  | ch_css_syndrome : TargetChannel
  deriving DecidableEq, Repr

def channelCensusList : List TargetChannel :=
  [TargetChannel.ch_ident,
   TargetChannel.ch_bitflip,
   TargetChannel.ch_phaseflip,
   TargetChannel.ch_bitphase,
   TargetChannel.ch_depol_1_3,
   TargetChannel.ch_depol_1_7,
   TargetChannel.ch_meas,
   TargetChannel.ch_css_syndrome]

theorem channels_censused_count_is_eight : channelCensusList.length = 8 := by
  rfl

#print axioms choi_dimension_is_four
#print axioms kraus_rank_bound_is_four
#print axioms depol_choi_1_3_psd
#print axioms depol_choi_1_7_psd
#print axioms depol_1_3_conductor_is_twelve
#print axioms depol_1_3_divides_120
#print axioms depol_1_7_conductor_is_twenty_eight
#print axioms depol_1_7_not_divides_120
#print axioms stinespring_requires_extension_verified
#print axioms depol_1_7_escalates_beyond_120_verified
#print axioms channels_censused_count_is_eight

theorem redundant_rational_weight (a b : Rat) (hb : b ≠ 0) :
    (a*b) * ((1/b)*(1/b)) = a/b := by
  grind

#print axioms redundant_rational_weight
end FableHilbertWalk20260819.H063

private def l5aProvenance : String :=
  "Origin: lean4/H063CptpChannelsStinespring.lean Claim: choi_dimension_is_four AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
