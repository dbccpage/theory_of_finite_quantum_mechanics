





import HWKernel
import FreeLinearization
import InnerProductAdmission
import BornPairingBoundary
import HilbertWalkSameContract

namespace HilbertWalk.Gleason

open HilbertWalk.HWKernel
open HilbertWalk.FreeLinearization (delta)
open HilbertWalk.InnerProductAdmission (sesq)
open HilbertWalk.BornPairingBoundary
  (hostSupplies UniquenessDischarged uniqueness_not_discharged)

def GleasonDimAtLeastThree {Q : Type} (E : Enum Q) : Prop :=
  3 ≤ E.elems.length

theorem enumBool_length_two : enumBool.elems.length = 2 :=
  rfl

#print axioms enumBool_length_two

theorem two_label_host_not_gleason_dimension :
    ¬ GleasonDimAtLeastThree enumBool := by
  intro h
  unfold GleasonDimAtLeastThree at h
  have hlen : enumBool.elems.length = 2 := enumBool_length_two
  rw [hlen] at h
  exact (by decide : ¬ ((3 : Nat) ≤ 2)) h

#print axioms two_label_host_not_gleason_dimension

theorem no_three_pairwise_distinct_reports :
    ¬ ∃ a b c : Bool, a ≠ b ∧ a ≠ c ∧ b ≠ c := by
  decide

#print axioms no_three_pairwise_distinct_reports

theorem no_three_orthonormal_report_deltas :
    ¬ ∃ a b c : Bool,
      a ≠ b ∧ a ≠ c ∧ b ≠ c ∧
        sesq gaussPack enumBool (delta gaussPack a) (delta gaussPack b) =
          gaussPack.zero ∧
        sesq gaussPack enumBool (delta gaussPack a) (delta gaussPack c) =
          gaussPack.zero ∧
        sesq gaussPack enumBool (delta gaussPack b) (delta gaussPack c) =
          gaussPack.zero := by
  intro h
  rcases h with ⟨a, b, c, hab, hac, hbc, _⟩
  exact no_three_pairwise_distinct_reports ⟨a, b, c, hab, hac, hbc⟩

#print axioms no_three_orthonormal_report_deltas

theorem gleason_pack_uniqueness_still_imported :
    ¬ GleasonDimAtLeastThree enumBool ∧
      hostSupplies.dimension_ge_three = false ∧
      hostSupplies.noncontextuality = false ∧
      hostSupplies.sigma_additivity = false ∧
      hostSupplies.continuity_of_measure = false ∧
      UniquenessDischarged hostSupplies = false :=
  ⟨two_label_host_not_gleason_dimension, rfl, rfl, rfl, rfl,
    uniqueness_not_discharged⟩

#print axioms gleason_pack_uniqueness_still_imported

theorem gleason_uniqueness_cannot_run_on_two_label_host :
    ¬ GleasonDimAtLeastThree enumBool ∧
      (¬ ∃ a b c : Bool, a ≠ b ∧ a ≠ c ∧ b ≠ c ∧
        sesq gaussPack enumBool (delta gaussPack a) (delta gaussPack b) =
          gaussPack.zero ∧
        sesq gaussPack enumBool (delta gaussPack a) (delta gaussPack c) =
          gaussPack.zero ∧
        sesq gaussPack enumBool (delta gaussPack b) (delta gaussPack c) =
          gaussPack.zero) ∧
      (HilbertWalk.SameContract.bornRule
          HilbertWalk.BornPairingBoundary.psi21
          (HilbertWalk.BornPairingBoundary.indicator false) ≠
        HilbertWalk.SameContract.swappedRule
          HilbertWalk.BornPairingBoundary.psi21
          (HilbertWalk.BornPairingBoundary.indicator false)) :=
  ⟨two_label_host_not_gleason_dimension,
    no_three_orthonormal_report_deltas,
    HilbertWalk.SameContract.two_effect_rules_share_unit_total_and_disagree.2.2.2.2⟩

#print axioms gleason_uniqueness_cannot_run_on_two_label_host

end HilbertWalk.Gleason

private def l5aProvenance : String :=
  "Origin: lean4/HilbertWalkGleason.lean Claim: enumBool_length_two AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
