





import HWKernel
import H004FreeLinearization
import H005InnerProductAdmission
import H013BornPairingBoundary
import H013SameContract

namespace FableHilbertWalk20260819.H017Gleason

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004 (delta)
open FableHilbertWalk20260819.H005 (sesq)
open FableHilbertWalk20260819.H013
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
      (FableHilbertWalk20260819.H013Contract.bornRule
          FableHilbertWalk20260819.H013.psi21
          (FableHilbertWalk20260819.H013.indicator false) ≠
        FableHilbertWalk20260819.H013Contract.swappedRule
          FableHilbertWalk20260819.H013.psi21
          (FableHilbertWalk20260819.H013.indicator false)) :=
  ⟨two_label_host_not_gleason_dimension,
    no_three_orthonormal_report_deltas,
    FableHilbertWalk20260819.H013Contract.two_effect_rules_share_unit_total_and_disagree.2.2.2.2⟩

#print axioms gleason_uniqueness_cannot_run_on_two_label_host

end FableHilbertWalk20260819.H017Gleason

private def l5aProvenance : String :=
  "Origin: lean4/H017Gleason.lean Claim: enumBool_length_two AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
