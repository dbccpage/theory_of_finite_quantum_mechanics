/-
  H017Gleason -- a three-label cardinality surrogate fails on Bool.
  AuthorityEffect: None. Candidate only. Not PROVEN.

  QM_122 remaining job 7.2 / STACK Gleason item, scoped to this
  host. `GleasonDimAtLeastThree` is only `3 ≤ E.elems.length`. It
  is not H013's `GleasonPack.dimension_ge_three`, and this file
  proves no bridge to that pack's other flags (noncontextuality,
  σ-additivity, continuity of measure). R7 — Born uniqueness
  under the full Gleason package — stays imported.

  The walk's two-label report set Bool has enumeration length 2,
  so the cardinality surrogate is false, and there is no
  three-element orthonormal report-basis frame.

  The weaker same-contract disagreement
  `H013Contract.two_effect_rules_share_unit_total_and_disagree`
  already shows two effect pairings that share the unit-effect
  total and disagree. That is not Gleason.

  This file does not prove Gleason at any dimension, and it does
  not claim the Born square is non-unique under Gleason's
  hypotheses.

  AuthorityEffect: None
  Origin: papers/core/finite_quantum_mechanics.md
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

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

/-- Cardinality surrogate only: the enumerated report set has at
    least three labels. Not `GleasonPack.dimension_ge_three`, and
    not a Hilbert-space dimension hypothesis. -/
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

/-- The two-label host has no three pairwise distinct reports. -/
theorem no_three_pairwise_distinct_reports :
    ¬ ∃ a b c : Bool, a ≠ b ∧ a ≠ c ∧ b ≠ c := by
  decide

#print axioms no_three_pairwise_distinct_reports

/-- A three-element orthonormal report-basis frame would need three
    pairwise distinct labels. The two-label host has none. -/
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

/-- No bridge from the cardinality surrogate to `GleasonPack`.
    The surrogate fails on Bool; the pack's four Bool flags stay
    the hand-set `hostSupplies` metadata, all false. Uniqueness
    under that pack is not discharged. R7 remains imported. -/
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

/-- Punchline: the cardinality surrogate fails on the two-label
    host, and there is no three-element orthonormal report-basis
    frame. The weaker unit-effect contract already has two
    disagreeing pairings (cited, not re-proved). This is not a
    Gleason theorem, not a bridge to `GleasonPack`, and not
    discharge of R7. -/
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
