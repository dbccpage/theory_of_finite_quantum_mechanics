/-
Exact algebraic model; AuthorityEffect: None.
Finite presentation sets and supplied observation lists define two explicit identity conventions. Supply preserves the observation list; profile equality matches SameProfile; profile-image cardinality is bounded by presentation cardinality; injective profiles make the conventions agree; unary-profile equality matches the imported Collapsed predicate. A closed fixture distinguishes the two conventions, so one Boolean evaluator cannot agree with both everywhere. This is model ambiguity, not a computability-theoretic undecidability theorem. The absent-convention query returns its tagged result even when its branch values agree. The trial-convention list is supplied data, not a checked transcription of trial files. The independent observation-family sweep uses carrier sizes 1 through 3, despite its introductory mention of 4; size 4 belongs to the separate unary-regime sweep.
Historical names are labels; their physical or operational interpretations require separate evidence.
-/

import Imported.PreGenesisToMssn.Observation
import GenesisComputation
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Image
import Mathlib.Data.List.Basic
import Mathlib.Tactic



namespace CampaignPgwIdentityConventionUndecidable

open GenesisComputation
open GenesisComputation.GenesisCopy
open PreMssn.Observation


structure PreGenesisRegime (α β : Type*) where
  presented : Finset α
  obs : List (α → β)


def supplyInscription {α β : Type*} [DecidableEq α]
    (R : PreGenesisRegime α β) (x : α) : PreGenesisRegime α β :=
  ⟨insert x R.presented, R.obs⟩


def obsProfile {α β : Type*} (R : PreGenesisRegime α β) (x : α) : List β :=
  R.obs.map (fun o => o x)


theorem supplyInscription_preserves_obs_and_enlarges_presentation
    {α β : Type*} [DecidableEq α] (R : PreGenesisRegime α β) (x : α)
    (hfresh : x ∉ R.presented) :
    (supplyInscription R x).obs = R.obs ∧
    obsProfile (supplyInscription R x) = obsProfile R ∧
    (supplyInscription R x).presented.card = R.presented.card + 1 := by
  refine ⟨rfl, rfl, ?_⟩
  simp [supplyInscription, Finset.card_insert_of_notMem hfresh]


def indexedObs {α β : Type*} (R : PreGenesisRegime α β) (i : Fin R.obs.length) (x : α) : β :=
  (R.obs.get i) x


theorem obsProfile_eq_iff_sameProfile_and_empty_obs_collapse
    {α β : Type*} (R : PreGenesisRegime α β) (x y : α) :
    (obsProfile R x = obsProfile R y ↔ SameProfile (indexedObs R) x y) ∧
    (R.obs = [] →
      obsProfile R x = [] ∧
      SameProfile (indexedObs R) x y ∧
      profileClass (indexedObs R) x = profileClass (indexedObs R) y) := by
  refine ⟨?_, ?_⟩
  · constructor
    · intro h i
      have hget := congrArg (fun l : List β => l[i.val]?) h
      simp [obsProfile] at hget
      exact hget
    · intro h
      apply List.ext_getElem
      · simp [obsProfile]
      · intro n hn1 hn2
        have hn : n < R.obs.length := by simpa [obsProfile] using hn1
        simpa [obsProfile, indexedObs] using h ⟨n, hn⟩
  · intro hempty
    have hpx : obsProfile R x = [] := by simp [obsProfile, hempty]
    have hsame : SameProfile (indexedObs R) x y := by
      intro ⟨i, hi⟩
      simp [hempty] at hi
    exact ⟨hpx, hsame, (profile_class_eq_iff (indexedObs R) x y).mpr hsame⟩


def isNewStateUnder {α β : Type*} [DecidableEq α] [DecidableEq β]
    (c : IdentityConvention) (R : PreGenesisRegime α β) (x : α) : Bool :=
  match c with
  | .opaqueConv => decide (obsProfile R x ∉ R.presented.image (obsProfile R))
  | .exactInscription => decide (x ∉ R.presented)


inductive ConventionVerdict
  | undecidableWithoutConvention (opaqueBranch exactBranch : Bool)
  | decided (isNew : Bool)
  deriving DecidableEq, Repr


def queryNewState {α β : Type*} [DecidableEq α] [DecidableEq β]
    (optConv : Option IdentityConvention) (R : PreGenesisRegime α β) (x : α) :
    ConventionVerdict :=
  match optConv with
  | none =>
      .undecidableWithoutConvention
        (isNewStateUnder .opaqueConv R x)
        (isNewStateUnder .exactInscription R x)
  | some c => .decided (isNewStateUnder c R x)


def stateCountUnder {α β : Type*} [DecidableEq α] [DecidableEq β]
    (c : IdentityConvention) (R : PreGenesisRegime α β) : Nat :=
  match c with
  | .opaqueConv => (R.presented.image (obsProfile R)).card
  | .exactInscription => R.presented.card


inductive PreGenesisToken
  | ground
  | markA
  | markB
  | markAB
  deriving DecidableEq, Repr


def initialRegime : PreGenesisRegime PreGenesisToken Bool :=
  ⟨{.ground}, []⟩


def afterSupplyRegime : PreGenesisRegime PreGenesisToken Bool :=
  supplyInscription initialRegime .markA


theorem supply_markA_after_ground_branch_divergence :
    PreGenesisToken.ground ≠ PreGenesisToken.markA ∧
    isNewStateUnder .opaqueConv initialRegime .markA = false ∧
    isNewStateUnder .exactInscription initialRegime .markA = true ∧
    isNewStateUnder .opaqueConv initialRegime .markA ≠
      isNewStateUnder .exactInscription initialRegime .markA ∧
    queryNewState none initialRegime .markA = .undecidableWithoutConvention false true ∧
    queryNewState (some .opaqueConv) initialRegime .markA = .decided false ∧
    queryNewState (some .exactInscription) initialRegime .markA = .decided true := by
  decide


theorem stateCount_supply_markA_delta_zero_vs_one :
    stateCountUnder .opaqueConv initialRegime = 1 ∧
    stateCountUnder .exactInscription initialRegime = 1 ∧
    stateCountUnder .opaqueConv afterSupplyRegime = 1 ∧
    stateCountUnder .exactInscription afterSupplyRegime = 2 ∧
    stateCountUnder .exactInscription afterSupplyRegime -
      stateCountUnder .opaqueConv afterSupplyRegime = 1 := by
  decide


theorem opaque_stateCount_le_exact_stateCount
    {α β : Type*} [DecidableEq α] [DecidableEq β] (R : PreGenesisRegime α β) :
    stateCountUnder .opaqueConv R ≤ stateCountUnder .exactInscription R := by
  simpa [stateCountUnder] using Finset.card_image_le (s := R.presented) (f := obsProfile R)


theorem conventions_agree_iff_fresh_profile
    {α β : Type*} [DecidableEq α] [DecidableEq β]
    (R : PreGenesisRegime α β) (x : α) (hfresh : x ∉ R.presented) :
    (isNewStateUnder .opaqueConv R x = isNewStateUnder .exactInscription R x) ↔
      obsProfile R x ∉ R.presented.image (obsProfile R) := by
  simp [isNewStateUnder, hfresh]


theorem injective_obsProfile_implies_conventions_coincide
    {α β : Type*} [DecidableEq α] [DecidableEq β]
    (R : PreGenesisRegime α β) (hinj : Function.Injective (obsProfile R)) (x : α) :
    isNewStateUnder .opaqueConv R x = isNewStateUnder .exactInscription R x ∧
    stateCountUnder .opaqueConv R = stateCountUnder .exactInscription R := by
  refine ⟨?_, ?_⟩
  · simp only [isNewStateUnder, Finset.mem_image]
    congr 1
    apply propext
    constructor
    · intro h hx
      exact h ⟨x, hx, rfl⟩
    · rintro h ⟨y, hy, heq⟩
      have hyx : y = x := hinj heq
      subst hyx
      exact h hy
  · simpa [stateCountUnder] using Finset.card_image_of_injective R.presented hinj


def genesisUnaryProfile (r : Regime) (i : Nat) : List Bool :=
  (List.range r.forms.length).map (fun f => decide (r.forms.getD f 0 = 1 ∧ (f, [i]) ∈ r.insts))


theorem genesisUnaryProfile_eq_iff_collapsed (r : Regime) (i j : Nat) :
    genesisUnaryProfile r i = genesisUnaryProfile r j ↔ Collapsed r i j := by
  constructor
  · intro heq
    have hpoint : ∀ f < r.forms.length,
        ((r.forms.getD f 0 = 1 ∧ (f, [i]) ∈ r.insts) ↔
         (r.forms.getD f 0 = 1 ∧ (f, [j]) ∈ r.insts)) := by
      intro f hf
      have hget := congrArg (fun l : List Bool => l[f]?) heq
      simp only [genesisUnaryProfile, List.getElem?_map, List.getElem?_range, hf,
        Option.map_some, Option.some.injEq, decide_eq_decide] at hget
      exact hget
    refine ⟨?_, ?_⟩
    · rintro ⟨f, hf, har, ⟨hi, hj⟩ | ⟨hj, hi⟩⟩
      · exact hj ((hpoint f hf).mp ⟨har, hi⟩).2
      · exact hi ((hpoint f hf).mpr ⟨har, hj⟩).2
    · rintro ⟨f, hf, har, ⟨hj, hi⟩ | ⟨hi, hj⟩⟩
      · exact hi ((hpoint f hf).mpr ⟨har, hj⟩).2
      · exact hj ((hpoint f hf).mp ⟨har, hi⟩).2
  · rintro ⟨hnot1, _⟩
    apply List.ext_getElem
    · simp [genesisUnaryProfile]
    · intro f hf1 _
      have hf : f < r.forms.length := by simpa [genesisUnaryProfile] using hf1
      simp only [genesisUnaryProfile, List.getElem_map, List.getElem_range, decide_eq_decide]
      constructor
      · rintro ⟨har, hi⟩
        refine ⟨har, ?_⟩
        by_contra hj
        exact hnot1 ⟨f, hf, har, Or.inl ⟨hi, hj⟩⟩
      · rintro ⟨har, hj⟩
        refine ⟨har, ?_⟩
        by_contra hi
        exact hnot1 ⟨f, hf, har, Or.inr ⟨hj, hi⟩⟩


theorem unformed_vs_firstSeparation_regime_convention_bridge :
    genesisUnaryProfile ⟨2, [], [], [], []⟩ 0 = genesisUnaryProfile ⟨2, [], [], [], []⟩ 1 ∧
    Collapsed ⟨2, [], [], [], []⟩ 0 1 ∧
    genesisUnaryProfile firstSeparationRegime 0 = [true] ∧
    genesisUnaryProfile firstSeparationRegime 1 = [false] ∧
    genesisUnaryProfile firstSeparationRegime 0 ≠ genesisUnaryProfile firstSeparationRegime 1 ∧
    ¬ Collapsed firstSeparationRegime 0 1 := by
  decide


theorem no_convention_free_evaluator_fence :
    ¬ ∃ eval : PreGenesisRegime PreGenesisToken Bool → PreGenesisToken → Bool,
      (∀ R x, eval R x = isNewStateUnder .opaqueConv R x) ∧
      (∀ R x, eval R x = isNewStateUnder .exactInscription R x) := by
  rintro ⟨eval, hop, hex⟩
  have h1 := hop initialRegime .markA
  have h2 := hex initialRegime .markA
  rw [h1] at h2
  revert h2
  decide


def prompt12TrialConventions : Fin 3 → IdentityConvention :=
  ![.opaqueConv, .opaqueConv, .exactInscription]


theorem trial_votes_do_not_determine_convention_fence :
    prompt12TrialConventions 0 = .opaqueConv ∧
    prompt12TrialConventions 1 = .opaqueConv ∧
    prompt12TrialConventions 2 = .exactInscription ∧
    isNewStateUnder (prompt12TrialConventions 0) initialRegime .markA = false ∧
    isNewStateUnder (prompt12TrialConventions 2) initialRegime .markA = true := by
  decide

end CampaignPgwIdentityConventionUndecidable

#print axioms CampaignPgwIdentityConventionUndecidable.supplyInscription_preserves_obs_and_enlarges_presentation
#print axioms CampaignPgwIdentityConventionUndecidable.obsProfile_eq_iff_sameProfile_and_empty_obs_collapse
#print axioms CampaignPgwIdentityConventionUndecidable.supply_markA_after_ground_branch_divergence
#print axioms CampaignPgwIdentityConventionUndecidable.stateCount_supply_markA_delta_zero_vs_one
#print axioms CampaignPgwIdentityConventionUndecidable.opaque_stateCount_le_exact_stateCount
#print axioms CampaignPgwIdentityConventionUndecidable.conventions_agree_iff_fresh_profile
#print axioms CampaignPgwIdentityConventionUndecidable.injective_obsProfile_implies_conventions_coincide
#print axioms CampaignPgwIdentityConventionUndecidable.genesisUnaryProfile_eq_iff_collapsed
#print axioms CampaignPgwIdentityConventionUndecidable.unformed_vs_firstSeparation_regime_convention_bridge
#print axioms CampaignPgwIdentityConventionUndecidable.no_convention_free_evaluator_fence
#print axioms CampaignPgwIdentityConventionUndecidable.trial_votes_do_not_determine_convention_fence
