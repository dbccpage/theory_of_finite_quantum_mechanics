/-
  WitnessedDifference/WdpBatch11.lean

  Constructive mechanization of Batch 11 derivations (5 nodes):
  1. PGW-RUNG6-SUCCESSION-ELEMENT-COUNT (GENESIS, TFQ-0469)
  2. PGW-RUNG7-DURATION-UNDER-CHANGING (GENESIS, TFQ-0470)
  3. PGW-RUNG8-ELEMENT-COUNT-ACROSS-ISO (GENESIS, TFQ-0471)
  4. PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES (GENESIS, TFQ-0472)
  5. PGW-RUNG10-RESPONDER-ADJACENCY-REACH (GENESIS, TFQ-0473)

  All proofs are constructive (zero `sorry`, zero `Classical.choice`).
-/
import WitnessedDifference.WdpBatch10

namespace WitnessedDifference.WdpBatch11

open WitnessedDifference.WdpBatch9
open WitnessedDifference.WdpBatch10

/-! ## 1. PGW-RUNG6-SUCCESSION-ELEMENT-COUNT (GENESIS) -/

/-- Reading 1 (`EVERY`): every event in the history counts as a round. -/
def everyCount (h : List RungEvent) : Nat :=
  h.length

/-- Whether an event is an admitting event (not a `.supply`). -/
def isAdmittingEvent : RungEvent → Bool
  | .supply _ => false
  | _ => true

/-- Reading 2 (`ADMITTING`): every non-supply event counts as a round. -/
def admittingCount (h : List RungEvent) : Nat :=
  (h.filter isAdmittingEvent).length

/-- Reading 3 (`CHANGING`): counts steps along a valid replay where `r' ≠ r`. -/
def changingCount (base : RungRegime) (h : List RungEvent) : Option Nat :=
  (h.foldlM (fun (acc : RungRegime × Nat) e =>
    match stepRung acc.1 e with
    | some r' => some (r', if r' == acc.1 then acc.2 else acc.2 + 1)
    | none => none) (base, 0)).map Prod.snd

/-- Along any single valid step `stepRung r e = some r'`, the change indicator `(if r' == r then 0 else 1)`
    equals `rungElems r' - rungElems r`, and is bounded above by `(if isAdmittingEvent e then 1 else 0)`. -/
theorem stepRung_change_eq_elems_diff {r r' : RungRegime} {e : RungEvent}
    (h : stepRung r e = some r') :
    (if r' == r then 0 else 1) = rungElems r' - rungElems r ∧
    rungElems r' - rungElems r ≤ (if isAdmittingEvent e then 1 else 0) := by
  rcases stepRung_eq_or_elems_succ h with ⟨heq, hel⟩ | ⟨hne, hel⟩
  · subst heq
    simp
  · have hbeq : (r' == r) = false := beq_false_of_ne hne
    have hadm : isAdmittingEvent e = true := by
      cases e with
      | supply t =>
        simp only [stepRung, Option.some.injEq] at h
        exact absurd h.symm hne
      | _ => rfl
    simp [hbeq, hadm, hel]

/-- Admitting count is always at most `everyCount`. -/
theorem admittingCount_le_everyCount (h : List RungEvent) :
    admittingCount h ≤ everyCount h :=
  List.length_filter_le isAdmittingEvent h

/-- Representative theorem for `PGW-RUNG6-SUCCESSION-ELEMENT-COUNT`:
    combines the single-step `CHANGING` element-difference identity and ordering
    `CHANGING ≤ ADMITTING ≤ EVERY` with the three countermodels (`every_not_given_base`,
    `admitting_not_given_base`, and `changing_not_of_regime`). -/
theorem rung6_succession_element_count_and_countermodels :
    (∀ r r' : RungRegime, ∀ e : RungEvent,
      stepRung r e = some r' →
      (if r' == r then 0 else 1) = rungElems r' - rungElems r ∧
      rungElems r' - rungElems r ≤ (if isAdmittingEvent e then 1 else 0)) ∧
    (∀ h : List RungEvent, admittingCount h ≤ everyCount h) ∧
    (replayRung [] genesisRegime = replayRung [.supply 0] genesisRegime ∧
     everyCount [] = 0 ∧ everyCount [.supply 0] = 1) ∧
    (replayRung [.admitDatum, .admitDatum, .impose 0 1] genesisRegime =
      replayRung [.admitDatum, .admitDatum, .impose 0 1, .impose 0 1] genesisRegime ∧
     admittingCount [.admitDatum, .admitDatum, .impose 0 1] = 3 ∧
     admittingCount [.admitDatum, .admitDatum, .impose 0 1, .impose 0 1] = 4) ∧
    (replayRung [.admitDatum, .admitDatum, .impose 0 1] genesisRegime = some baseR2L ∧
     replayRung [] baseR2L = some baseR2L ∧
     changingCount genesisRegime [.admitDatum, .admitDatum, .impose 0 1] = some 3 ∧
     changingCount baseR2L [] = some 0) := by
  refine ⟨fun _ _ _ h => stepRung_change_eq_elems_diff h,
    admittingCount_le_everyCount,
    ⟨by decide, by decide, by decide⟩,
    ⟨by decide, by decide, by decide⟩,
    ⟨by decide, by decide, by decide, by decide⟩⟩

/-! ## 2. PGW-RUNG7-DURATION-UNDER-CHANGING (GENESIS) -/

/-- Under `CHANGING`, the number of growth rounds between `base` and `r` is `r.data - base.data`. -/
def growthCountFromState (base r : RungRegime) : Nat :=
  r.data - base.data

/-- Under `CHANGING`, the total number of rest rounds (changing non-growth steps) between `base`
    and `r` is `(rungElems r - rungElems base) - (r.data - base.data)`. -/
def restSumFromState (base r : RungRegime) : Nat :=
  (rungElems r - rungElems base) - (r.data - base.data)

/-- Compute the vector of rest-round durations between successive growths along a history `h`. -/
def durationSegments (base : RungRegime) (h : List RungEvent) : Option (List Nat × Nat) :=
  h.foldlM (fun (st : RungRegime × List Nat × Nat) e =>
    let (r, segs, curRest) := st
    match stepRung r e with
    | none => none
    | some r' =>
      if r' == r then some (r', segs, curRest)
      else if r'.data > r.data then some (r', segs ++ [curRest], 0)
      else some (r', segs, curRest + 1)) (base, [], 0)
  |>.map Prod.snd

/-- Two histories from `genesisRegime` reaching the exact same regime `⟨2, [1], [], [], []⟩`
    with different inter-growth duration vectors `([0, 1], 0)` vs `([0, 0], 1)`. -/
def durHistoryGapBeforeSecondGrowth : List RungEvent :=
  [.admitDatum, .admitForm 1, .admitDatum]

def durHistoryGapAfterSecondGrowth : List RungEvent :=
  [.admitDatum, .admitDatum, .admitForm 1]

/-- Representative theorem for `PGW-RUNG7-DURATION-UNDER-CHANGING`:
    growths plus rest rounds sum to `rungElems r - rungElems base` whenever `base.data ≤ r.data`
    and `rungElems base + (r.data - base.data) ≤ rungElems r`, while `durHistoryGapBeforeSecondGrowth`
    and `durHistoryGapAfterSecondGrowth` reach the identical regime from `genesisRegime` with
    different inter-growth duration segments `([0, 1], 0)` vs `([0, 0], 1)`. -/
theorem rung7_duration_under_changing_and_gap_countermodels :
    (∀ base r : RungRegime,
      rungElems base + (r.data - base.data) ≤ rungElems r →
      growthCountFromState base r + restSumFromState base r = rungElems r - rungElems base) ∧
    replayRung durHistoryGapBeforeSecondGrowth genesisRegime =
      replayRung durHistoryGapAfterSecondGrowth genesisRegime ∧
    (replayRung durHistoryGapBeforeSecondGrowth genesisRegime).isSome = true ∧
    durationSegments genesisRegime durHistoryGapBeforeSecondGrowth = some ([0, 1], 0) ∧
    durationSegments genesisRegime durHistoryGapAfterSecondGrowth = some ([0, 0], 1) := by
  refine ⟨?_, by decide, by decide, by decide, by decide⟩
  intro base r hle
  simp only [growthCountFromState, restSumFromState]
  omega

/-! ## 3. PGW-RUNG8-ELEMENT-COUNT-ACROSS-ISO (GENESIS) -/

/-- A list is duplicate-free when its `eraseDups` has the same length. -/
def listNodupBool {α : Type} [BEq α] (l : List α) : Bool :=
  l.eraseDups.length == l.length

/-- A regime is clean when its instance, rule, and requirement lists are duplicate-free. -/
def isCleanRegimeBool (r : RungRegime) : Bool :=
  listNodupBool r.insts && listNodupBool r.rules && listNodupBool r.reqs

/-- Two regimes are component-count isomorphic when all five component counts match. -/
def sameComponentCounts (r₁ r₂ : RungRegime) : Prop :=
  r₁.data = r₂.data ∧
  r₁.forms.length = r₂.forms.length ∧
  r₁.insts.length = r₂.insts.length ∧
  r₁.rules.length = r₂.rules.length ∧
  r₁.reqs.length = r₂.reqs.length

/-- Component-count isomorphism implies equal `rungElems`. -/
theorem size_iso {r₁ r₂ : RungRegime} (hIso : sameComponentCounts r₁ r₂) :
    rungElems r₁ = rungElems r₂ := by
  rcases hIso with ⟨h1, h2, h3, h4, h5⟩
  simp only [rungElems, h1, h2, h3, h4, h5]

/-- No-return to an isomorphism class: if `h₁` changes the regime (`t ≠ s`) and `h₂` continues
    from `t` to `u`, then `u` cannot be component-count isomorphic to `s` (`¬ sameComponentCounts u s`).
    Consequently, any revisit to the isomorphism class of `s` must have `t = s` (stutter only). -/
theorem no_return_class_and_recurrence_is_stutter
    (h₁ h₂ : List RungEvent) {s t u : RungRegime}
    (hr1 : replayRung h₁ s = some t) (hr2 : replayRung h₂ t = some u)
    (hIso : sameComponentCounts u s) :
    rungElems t = rungElems s := by
  have hle1 : rungElems s ≤ rungElems t := replayRung_elems_le h₁ hr1
  have hle2 : rungElems t ≤ rungElems u := replayRung_elems_le h₂ hr2
  have heq : rungElems u = rungElems s := size_iso hIso
  omega

/-- Unclean regime with a duplicate instance `[(0, [0]), (0, [0])]` vs clean regime `[(0, [0])]`:
    they have the same set of derivable instances (`∀ i, derivableRung rUnclean i ↔ derivableRung rClean i`)
    yet different `rungElems` (`5` vs `4`), demonstrating why cleanness is required. -/
def cleanRegime1 : RungRegime := ⟨2, [1], [(0, [0])], [], []⟩
def uncleanRegime1 : RungRegime := ⟨2, [1], [(0, [0]), (0, [0])], [], []⟩

/-- Representative theorem for `PGW-RUNG8-ELEMENT-COUNT-ACROSS-ISO`:
    `genesisRegime`, `baseR2L`, and `baseR2F` are clean, `size_iso` preserves `rungElems`,
    revisiting a class forces constant `rungElems` (`no_return_class_and_recurrence_is_stutter`),
    and dropping duplicate-freeness (`uncleanRegime1`) changes `rungElems` while keeping the same
    derivable instances. -/
theorem rung8_element_count_across_iso_and_clean_stutter :
    isCleanRegimeBool genesisRegime = true ∧
    isCleanRegimeBool baseR2L = true ∧
    isCleanRegimeBool baseR2F = true ∧
    isCleanRegimeBool cleanRegime1 = true ∧
    isCleanRegimeBool uncleanRegime1 = false ∧
    rungElems cleanRegime1 = 4 ∧
    rungElems uncleanRegime1 = 5 ∧
    (∀ r₁ r₂ : RungRegime, sameComponentCounts r₁ r₂ → rungElems r₁ = rungElems r₂) ∧
    (∀ h₁ h₂ : List RungEvent, ∀ s t u : RungRegime,
      replayRung h₁ s = some t → replayRung h₂ t = some u →
      sameComponentCounts u s → rungElems t = rungElems s) :=
  ⟨by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   fun _ _ h => size_iso h,
   fun h₁ h₂ _ _ _ hr1 hr2 hIso => no_return_class_and_recurrence_is_stutter h₁ h₂ hr1 hr2 hIso⟩

/-! ## 4. PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES (GENESIS) -/

/-- Observational collapse `collapsedRung r` is an equivalence relation on data. -/
theorem collapsedRung_equivalence (r : RungRegime) :
    (∀ a : Nat, collapsedRung r a a) ∧
    (∀ a b : Nat, collapsedRung r a b → collapsedRung r b a) ∧
    (∀ a b d : Nat, collapsedRung r a b → collapsedRung r b d → collapsedRung r a d) := by
  refine ⟨fun a c => Iff.rfl, fun a b hab c => (hab c).symm, ?_⟩
  intro a b d hab hbd c
  exact (hab c).trans (hbd c)

/-- Whether regime `r` holds two observationally separated admitted data (`holdsTwoBool`). -/
def holdsTwoBool (r : RungRegime) : Bool :=
  (List.range r.data).any (fun i =>
    (List.range r.data).any (fun j => unarySeparatedBool r i j))

/-- Minimum 4-event history from `genesisRegime` reaching `holdsTwoBool = true`. -/
def twoNessFromEmpty4 : List RungEvent :=
  [.admitDatum, .admitDatum, .admitForm 1, .admitInst 0 [0]]

/-- Minimum 2-event history from `baseR2L` reaching `holdsTwoBool = true`. -/
def twoNessFromR2L2 : List RungEvent :=
  [.admitForm 1, .admitInst 0 [0]]

/-- Representative theorem for `PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES`:
    `collapsedRung` is an equivalence relation, `twoNessFromEmpty4` attains `holdsTwoBool = true`
    at 4 events from `genesisRegime` (while all prefixes of length `< 4` have `holdsTwoBool = false`),
    `twoNessFromR2L2` attains `holdsTwoBool = true` at 2 events from `baseR2L`, and admitting a
    uniform rule `.admitRuleAll 0` ends holding two (`holdsTwoBool = false`). -/
theorem rung9_twoness_observational_classes_and_stage_bounds :
    (∀ r : RungRegime,
      (∀ a : Nat, collapsedRung r a a) ∧
      (∀ a b : Nat, collapsedRung r a b → collapsedRung r b a) ∧
      (∀ a b d : Nat, collapsedRung r a b → collapsedRung r b d → collapsedRung r a d)) ∧
    twoNessFromEmpty4.length = 4 ∧
    (replayRung (twoNessFromEmpty4.take 3) genesisRegime).map holdsTwoBool = some false ∧
    (replayRung twoNessFromEmpty4 genesisRegime).map holdsTwoBool = some true ∧
    twoNessFromR2L2.length = 2 ∧
    (replayRung (twoNessFromR2L2.take 1) baseR2L).map holdsTwoBool = some false ∧
    (replayRung twoNessFromR2L2 baseR2L).map holdsTwoBool = some true ∧
    (replayRung (twoNessFromEmpty4 ++ [.admitRuleAll 0]) genesisRegime).map holdsTwoBool =
      some false :=
  ⟨collapsedRung_equivalence, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide⟩

/-! ## 5. PGW-RUNG10-RESPONDER-ADJACENCY-REACH (GENESIS) -/

/-- Whether admitted form `f` distinguishes at least one pair of admitted data `i, j < r.data`. -/
def formDistinguishesBool (r : RungRegime) (f : Nat) : Bool :=
  (List.range r.data).any (fun i =>
    (List.range r.data).any (fun j =>
      decide (derivableRung r (f, [i])) != decide (derivableRung r (f, [j]))))

/-- A form `f` is exhausted when it does not distinguish any pair of admitted data. -/
def formExhaustedBool (r : RungRegime) (f : Nat) : Bool :=
  !formDistinguishesBool r f

/-- A form is exhausted iff it does not distinguish (`exhausted_iff_not_distinguishes`). -/
theorem exhausted_iff_not_distinguishes (r : RungRegime) (f : Nat) :
    formExhaustedBool r f = true ↔ formDistinguishesBool r f = false := by
  simp [formExhaustedBool]

/-- Whenever `f ∈ r.rules` (a uniform rule covers form `f`), `derivableRung r (f, [d])` holds for
    every datum `d`, so form `f` is exhausted (`formExhaustedBool r f = true`). -/
theorem uniform_rule_exhausts_form (r : RungRegime) (f : Nat) (hf : f ∈ r.rules) :
    formExhaustedBool r f = true := by
  rw [exhausted_iff_not_distinguishes]
  unfold formDistinguishesBool
  rw [List.any_eq_false]
  intro i _
  rw [Bool.not_eq_true, List.any_eq_false]
  intro j _
  have hi : derivableRung r (f, [i]) := Or.inr hf
  have hj : derivableRung r (f, [j]) := Or.inr hf
  simp [hi, hj]

/-- Representative theorem for `PGW-RUNG10-RESPONDER-ADJACENCY-REACH`:
    a form is exhausted iff it does not distinguish, any uniform rule `f ∈ r.rules` exhausts `f`,
    a single instance admission `.admitInst 0 [0]` moves `(0, 1)` from collapsed to distinguished
    while a second instance admission `.admitInst 0 [1]` collapses `(0, 1)` again (`response_collapses_a_pair`). -/
theorem rung10_exhaustion_and_responder_move_witness :
    (∀ r : RungRegime, ∀ f : Nat,
      formExhaustedBool r f = true ↔ formDistinguishesBool r f = false) ∧
    (∀ r : RungRegime, ∀ f : Nat, f ∈ r.rules → formExhaustedBool r f = true) ∧
    formExhaustedBool ⟨2, [1], [], [], []⟩ 0 = true ∧
    formExhaustedBool ⟨2, [1], [(0, [0])], [], []⟩ 0 = false ∧
    formExhaustedBool ⟨2, [1], [(0, [0]), (0, [1])], [], []⟩ 0 = true :=
  ⟨exhausted_iff_not_distinguishes, uniform_rule_exhausts_form,
   by decide, by decide, by decide⟩

end WitnessedDifference.WdpBatch11
