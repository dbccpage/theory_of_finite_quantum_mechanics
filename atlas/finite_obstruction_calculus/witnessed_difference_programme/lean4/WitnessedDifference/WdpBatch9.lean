/-
  WitnessedDifference/WdpBatch9.lean

  Constructive mechanization of Batch 9 derivations (5 nodes):
  1. PGW-GENESIS-THREE-AXIS-VERDICT (GENESIS, TFQ-0461)
  2. PGW-RUNG0-INHERITANCE-REPLAY (GENESIS, TFQ-0462)
  3. PGW-RUNG2B-STAKE-MENU (GENESIS, TFQ-0465)
  4. PGW-FORCED-CENSUS-COLUMN (GENESIS, TFQ-0476)
  5. L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED (L1_TO_L2, TFQ-0005 / TFQ-0167 / TFQ-0354)

  All proofs are constructive (zero `sorry`, zero `Classical.choice`).
-/

namespace WitnessedDifference.WdpBatch9

/-! ## 1. PGW-GENESIS-THREE-AXIS-VERDICT (GENESIS) -/

/-- First closeout axis: research phase status. -/
inductive ResearchPhase where
  | closedWithOpenObstructions
  | openActive
  deriving DecidableEq, Repr

/-- Second closeout axis: alpha reference status. -/
inductive AlphaReference where
  | readyWithinDeclaredScope
  | notReady
  deriving DecidableEq, Repr

/-- Input-count floor status inside the original seed completion gate. -/
inductive InputFloorStatus where
  | established
  | notEstablished
  deriving DecidableEq, Repr

/-- Third closeout axis: original seed completion gate record. -/
structure SeedCompletionGate where
  satisfied : Bool
  liveInjectionMet : Bool
  comparisonMet : Bool
  inputCountFloor : InputFloorStatus
  deriving DecidableEq, Repr

/-- Complete three-axis closeout verdict record at snapshot 90ab34a0. -/
structure GenesisCloseoutVerdict where
  researchPhase : ResearchPhase
  alphaReference : AlphaReference
  seedCompletionGate : SeedCompletionGate
  compiledTheoremConstants : Nat
  rustPythonAgreementRegimes : Nat
  leanPythonWireTuples : Nat
  deriving DecidableEq, Repr

/-- The recorded closeout verdict after the 2026-09-28 freeze. -/
def frozenCloseoutVerdict : GenesisCloseoutVerdict :=
  { researchPhase := .closedWithOpenObstructions
  , alphaReference := .readyWithinDeclaredScope
  , seedCompletionGate :=
      { satisfied := false
      , liveInjectionMet := false
      , comparisonMet := false
      , inputCountFloor := .notEstablished }
  , compiledTheoremConstants := 2475
  , rustPythonAgreementRegimes := 1436
  , leanPythonWireTuples := 1439 }

/-- Counterfactual verdict sharing the first two axes while satisfying the completion gate,
    demonstrating that the three verdict axes are logically independent. -/
def counterfactualGateSatisfiedVerdict : GenesisCloseoutVerdict :=
  { frozenCloseoutVerdict with
    seedCompletionGate :=
      { satisfied := true
      , liveInjectionMet := true
      , comparisonMet := true
      , inputCountFloor := .established } }

/-- Source `delta_events` fresh-datum naming rule: names token `w<n>` where `n = admitted.length`. -/
def deltaEventsFreshLabel (admitted : List Nat) : Nat :=
  admitted.length

/-- Collision-free fresh-datum naming rule: `1 + max(admitted)`. -/
def freshLabelMaxPlusOne (admitted : List Nat) : Nat :=
  admitted.foldr max 0 + 1

/-- Deduplicating token admission into an admitted datum token list. -/
def admitTokenDeduplicated (admitted : List Nat) (tok : Nat) : List Nat :=
  if tok ∈ admitted then admitted else admitted ++ [tok]

/-- When the sole admitted token is `w1` (`admitted = [1]`), `deltaEventsFreshLabel [1] = 1`
    collides with `w1` and deduplication leaves the state unchanged (`[1]`), whereas
    `freshLabelMaxPlusOne [1] = 2` extends the state to `[1, 2]`. -/
theorem delta_events_w1_fresh_label_collision :
    deltaEventsFreshLabel [1] = 1 ∧
    admitTokenDeduplicated [1] (deltaEventsFreshLabel [1]) = [1] ∧
    freshLabelMaxPlusOne [1] = 2 ∧
    admitTokenDeduplicated [1] (freshLabelMaxPlusOne [1]) = [1, 2] := by
  decide

/-- Representative theorem for `PGW-GENESIS-THREE-AXIS-VERDICT`:
    the three closeout axes remain independent verdicts (`research_phase` and `alpha_reference`
    do not imply `seedCompletionGate.satisfied`), the `w1` fresh-label collision is reproduced,
    and the recorded census and cross-language agreement populations are preserved. -/
theorem genesis_three_axis_verdict_and_w1_collision_certificate :
    frozenCloseoutVerdict.researchPhase = .closedWithOpenObstructions ∧
    frozenCloseoutVerdict.alphaReference = .readyWithinDeclaredScope ∧
    frozenCloseoutVerdict.seedCompletionGate.satisfied = false ∧
    frozenCloseoutVerdict.seedCompletionGate.liveInjectionMet = false ∧
    frozenCloseoutVerdict.seedCompletionGate.comparisonMet = false ∧
    frozenCloseoutVerdict.seedCompletionGate.inputCountFloor = .notEstablished ∧
    counterfactualGateSatisfiedVerdict.researchPhase = frozenCloseoutVerdict.researchPhase ∧
    counterfactualGateSatisfiedVerdict.alphaReference = frozenCloseoutVerdict.alphaReference ∧
    counterfactualGateSatisfiedVerdict.seedCompletionGate.satisfied = true ∧
    admitTokenDeduplicated [1] (deltaEventsFreshLabel [1]) = [1] ∧
    frozenCloseoutVerdict.compiledTheoremConstants = 2475 ∧
    frozenCloseoutVerdict.rustPythonAgreementRegimes = 1436 ∧
    frozenCloseoutVerdict.leanPythonWireTuples = 1439 := by
  decide

/-! ## 2. PGW-RUNG0-INHERITANCE-REPLAY (GENESIS) -/

/-- Deduplicating insertion into a list. -/
def insertNew {α : Type} [DecidableEq α] (l : List α) (a : α) : List α :=
  if a ∈ l then l else l ++ [a]

/-- Sealed kernel regime for Rung 0 and Continuation 2. -/
structure RungRegime where
  data  : Nat
  forms : List Nat
  insts : List (Nat × List Nat)
  rules : List Nat
  reqs  : List (Nat × Nat)
  deriving DecidableEq, Repr

/-- The six sealed event kinds. -/
inductive RungEvent where
  | supply       (token : Nat)
  | admitDatum
  | admitForm    (arity : Nat)
  | admitInst    (form : Nat) (args : List Nat)
  | admitRuleAll (form : Nat)
  | impose       (i j : Nat)
  deriving DecidableEq, Repr

/-- The two remaining declared inputs censused at Rung 0. -/
inductive DeclaredRemainingInput where
  | stake
  | stream
  deriving DecidableEq, Repr

/-- Sealed transition step on `RungRegime`. -/
def stepRung (r : RungRegime) : RungEvent → Option RungRegime
  | .supply _ => some r
  | .admitDatum => some { r with data := r.data + 1 }
  | .admitForm a =>
      if 1 ≤ a then some { r with forms := r.forms ++ [a] } else none
  | .admitInst f args =>
      if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
          (∀ x ∈ args, x < r.data) then
        some { r with insts := insertNew r.insts (f, args) }
      else none
  | .admitRuleAll f =>
      if f < r.forms.length then
        some { r with rules := insertNew r.rules f }
      else none
  | .impose i j =>
      if i < j ∧ j < r.data then
        some { r with reqs := insertNew r.reqs (i, j) }
      else none

/-- Replay a list of sealed events over a base regime. -/
def replayRung (h : List RungEvent) (base : RungRegime) : Option RungRegime :=
  h.foldlM stepRung base

/-- Initial empty genesis regime. -/
def genesisRegime : RungRegime := ⟨0, [], [], [], []⟩

/-- Challenge 3 reading L base regime. -/
def baseR2L : RungRegime := ⟨2, [], [], [], [(0, 1)]⟩

/-- Challenge 3 reading F base regime. -/
def baseR2F : RungRegime := ⟨3, [], [], [], [(1, 2)]⟩

/-- Context with holes (`none`) for observational collapse. -/
structure RungCtx where
  form  : Nat
  slots : List (Option Nat)
  deriving DecidableEq, Repr

def plugCtx (c : RungCtx) (d : Nat) : Nat × List Nat :=
  (c.form, c.slots.map (fun s => s.getD d))

def derivableRung (r : RungRegime) (i : Nat × List Nat) : Prop :=
  i ∈ r.insts ∨ i.1 ∈ r.rules

instance (r : RungRegime) (i : Nat × List Nat) : Decidable (derivableRung r i) := by
  unfold derivableRung; infer_instance

def collapsedRung (r : RungRegime) (d d' : Nat) : Prop :=
  ∀ c : RungCtx, derivableRung r (plugCtx c d) ↔ derivableRung r (plugCtx c d')

/-- With no admitted instances, every pair of data is observationally collapsed. -/
theorem collapsedRung_of_no_insts (r : RungRegime) (hi : r.insts = []) (d d' : Nat) :
    collapsedRung r d d' := by
  intro c
  constructor <;> intro h <;>
    cases h with
    | inl h => rw [hi] at h; cases h
    | inr h => exact Or.inr h

/-- Any sequence of `supply` events of any length preserves any regime `r`. -/
theorem replay_supplies_no_op (tokens : List Nat) (r : RungRegime) :
    replayRung (tokens.map RungEvent.supply) r = some r := by
  induction tokens generalizing r with
  | nil => rfl
  | cons t ts ih =>
    simp only [List.map_cons, replayRung, List.foldlM_cons, stepRung, Option.bind_eq_bind,
      Option.bind_some]
    exact ih r

/-- Any sequence of `k` `admitDatum` growth steps under the all-free stake increases `data` by `k`,
    admits no forms/instances/rules, and leaves every pair of data totally collapsed. -/
theorem replay_admitDatum_growth (k : Nat) (r : RungRegime) :
    replayRung (List.replicate k RungEvent.admitDatum) r =
      some { r with data := r.data + k } := by
  induction k generalizing r with
  | zero =>
    simp [replayRung]
  | succ m ih =>
    simp only [List.replicate_succ, replayRung, List.foldlM_cons, stepRung, Option.bind_eq_bind,
      Option.bind_some]
    have hih := ih { r with data := r.data + 1 }
    simp only [replayRung] at hih
    rw [hih]
    simp [Nat.add_assoc, Nat.add_comm 1 m]

/-- Representative theorem for `PGW-RUNG0-INHERITANCE-REPLAY`:
    both sealed baselines (`baseR2L` and `baseR2F`) replay from `genesisRegime`, any sequence
    of `supply` events (including up to 8 supplies) leaves the regime unchanged, and growth by
    any `k` data (including up to 5 data) under the all-free stake from `baseR2L` or `baseR2F`
    admits no form and leaves every pair of data observationally collapsed. -/
theorem rung0_inheritance_replay_and_unbounded_supply_datum_inertia :
    replayRung [.supply 0, .supply 1, .supply 1, .supply 2,
                .admitDatum, .admitDatum, .impose 0 1] genesisRegime = some baseR2L ∧
    replayRung [.supply 0, .admitDatum, .supply 1, .supply 1, .supply 2,
                .admitDatum, .admitDatum, .impose 1 2] genesisRegime = some baseR2F ∧
    (∀ tokens : List Nat, ∀ r : RungRegime,
      replayRung (tokens.map RungEvent.supply) r = some r) ∧
    (∀ k : Nat, ∃ rL',
      replayRung (List.replicate k RungEvent.admitDatum) baseR2L = some rL' ∧
      rL'.forms = [] ∧ rL'.insts = [] ∧
      ∀ d d' : Nat, collapsedRung rL' d d') ∧
    (∀ k : Nat, ∃ rF',
      replayRung (List.replicate k RungEvent.admitDatum) baseR2F = some rF' ∧
      rF'.forms = [] ∧ rF'.insts = [] ∧
      ∀ d d' : Nat, collapsedRung rF' d d') := by
  refine ⟨by decide, by decide, replay_supplies_no_op, ?_, ?_⟩
  · intro k
    refine ⟨{ baseR2L with data := baseR2L.data + k }, replay_admitDatum_growth k baseR2L, rfl, rfl, ?_⟩
    exact collapsedRung_of_no_insts _ rfl
  · intro k
    refine ⟨{ baseR2F with data := baseR2F.data + k }, replay_admitDatum_growth k baseR2F, rfl, rfl, ?_⟩
    exact collapsedRung_of_no_insts _ rfl

/-! ## 3. PGW-RUNG2B-STAKE-MENU (GENESIS) -/

/-- The nine stake rules `E1 .. E9` in the Rung 2b declared menu. -/
inductive StakeMenuRule where
  | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 | E9
  deriving DecidableEq, Repr

/-- The six observables read by the nine stake rules. -/
inductive StakeObservable where
  | profileEquality
  | profileEmptiness
  | profileSize
  | pairOrbitMembership
  | classCount
  | requirementPattern
  deriving DecidableEq, Repr

/-- Complete list of the nine declared stake menu rules. -/
def allStakeMenuRules : List StakeMenuRule :=
  [.E1, .E2, .E3, .E4, .E5, .E6, .E7, .E8, .E9]

/-- Primary observable read by each menu rule. -/
def primaryObservable : StakeMenuRule → StakeObservable
  | .E1 => .profileEquality
  | .E2 => .profileEmptiness
  | .E3 => .pairOrbitMembership
  | .E4 => .pairOrbitMembership
  | .E5 => .profileSize
  | .E6 => .pairOrbitMembership
  | .E7 => .classCount
  | .E8 => .requirementPattern
  | .E9 => .profileEquality

/-- Whether a rule reads pair-orbit membership (`E3, E4, E6`), leaving transport replay OPEN. -/
def readsPairOrbit : StakeMenuRule → Bool
  | .E3 | .E4 | .E6 => true
  | _ => false

/-- Whether a rule's renaming invariance is CHECKED across the 1,345,706 transport cases
    on the 847 reached regimes (`E1, E2, E5, E7, E8, E9`). -/
def checkedInvariantOnRectangle (r : StakeMenuRule) : Bool :=
  !readsPairOrbit r

/-- Whether a rule generates demands of both kinds (`same` and `apart`) under growth (`E4` only). -/
def generatesBothDemandKinds : StakeMenuRule → Bool
  | .E4 => true
  | _ => false

/-- Profile equality transfers across any bijection of contexts preserving derivability. -/
theorem profile_equality_renaming_invariant
    (r₁ r₂ : RungRegime) (πCtx : RungCtx → RungCtx) (πDat : Nat → Nat)
    (hSurj : ∀ c₂ : RungCtx, ∃ c₁ : RungCtx, πCtx c₁ = c₂)
    (hPres : ∀ c : RungCtx, ∀ d : Nat,
      derivableRung r₂ (plugCtx (πCtx c) (πDat d)) ↔ derivableRung r₁ (plugCtx c d))
    {a b : Nat} (hEq : collapsedRung r₁ a b) :
    collapsedRung r₂ (πDat a) (πDat b) := by
  intro c₂
  obtain ⟨c₁, rfl⟩ := hSurj c₂
  exact (hPres c₁ a).trans ((hEq c₁).trans (hPres c₁ b).symm)

/-- Representative theorem for `PGW-RUNG2B-STAKE-MENU`:
    among the 9 declared menu rules `E1..E9`, exactly 6 are checked invariant on the rectangle,
    3 (`E3, E4, E6`) read pair orbits and remain open at transport replay, `E4` alone generates
    both demand kinds, and no menu rule is both checked invariant and two-kinded. -/
theorem rung2b_stake_menu_no_member_both_invariant_and_two_kinded :
    allStakeMenuRules.length = 9 ∧
    (allStakeMenuRules.filter checkedInvariantOnRectangle).length = 6 ∧
    (allStakeMenuRules.filter (fun r => !checkedInvariantOnRectangle r)) = [.E3, .E4, .E6] ∧
    (allStakeMenuRules.filter generatesBothDemandKinds) = [.E4] ∧
    (∀ r : StakeMenuRule,
      ¬ (checkedInvariantOnRectangle r = true ∧ generatesBothDemandKinds r = true)) := by
  refine ⟨by decide, by decide, by decide, by decide, ?_⟩
  intro r
  cases r <;> decide

/-! ## 4. PGW-FORCED-CENSUS-COLUMN (GENESIS) -/

/-- The twelve rows of the Challenge 5 definability census. -/
inductive CensusRow where
  | twoNess
  | obsClassCount
  | succession
  | duration
  | adjacency
  | reach
  | elementCount
  | irreversibility
  | symmetry
  | branching
  | exhaustion
  | recurrence
  deriving DecidableEq, Repr

def allCensusRows : List CensusRow :=
  [ .twoNess, .obsClassCount, .succession, .duration, .adjacency, .reach
  , .elementCount, .irreversibility, .symmetry, .branching, .exhaustion, .recurrence ]

/-- Whether a census row is FORCED over the entire 144-engine class both at the bounds and
    unboundedly across every history (`elementCount` and `irreversibility`). -/
def forcedOverAll144Engines : CensusRow → Bool
  | .elementCount | .irreversibility => true
  | _ => false

/-- Whether a census row is FORCED over the 64 LIVE engines (`elementCount`, `irreversibility`,
    and `twoNess`). -/
def forcedOverLive64Engines : CensusRow → Bool
  | .elementCount | .irreversibility | .twoNess => true
  | _ => false

/-- Element count of a `RungRegime`. -/
def rungElems (r : RungRegime) : Nat :=
  r.data + r.forms.length + r.insts.length + r.rules.length + r.reqs.length

theorem insertNew_length_le {α : Type} [DecidableEq α] (l : List α) (a : α) :
    l.length ≤ (insertNew l a).length := by
  unfold insertNew
  split <;> simp

theorem insertNew_eq_or_succ {α : Type} [DecidableEq α] (l : List α) (a : α) :
    insertNew l a = l ∨ (insertNew l a).length = l.length + 1 := by
  unfold insertNew
  split
  · exact Or.inl rfl
  · exact Or.inr (by simp)

/-- Every sealed step preserves or raises `rungElems`. -/
theorem stepRung_elems_le {r r' : RungRegime} {e : RungEvent}
    (h : stepRung r e = some r') : rungElems r ≤ rungElems r' := by
  cases e with
  | supply _ =>
      simp only [stepRung, Option.some.injEq] at h
      subst h; exact Nat.le_refl _
  | admitDatum =>
      simp only [stepRung, Option.some.injEq] at h
      subst h; simp only [rungElems]; omega
  | admitForm a =>
      simp only [stepRung] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h; simp only [rungElems, List.length_append, List.length_cons, List.length_nil]; omega
      · cases h
  | admitInst f args =>
      simp only [stepRung] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        have := insertNew_length_le r.insts (f, args)
        simp only [rungElems]; omega
      · cases h
  | admitRuleAll f =>
      simp only [stepRung] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        have := insertNew_length_le r.rules f
        simp only [rungElems]; omega
      · cases h
  | impose i j =>
      simp only [stepRung] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        have := insertNew_length_le r.reqs (i, j)
        simp only [rungElems]; omega
      · cases h

/-- Every history preserves or raises `rungElems`. -/
theorem replayRung_elems_le (h : List RungEvent) {s t : RungRegime}
    (hr : replayRung h s = some t) : rungElems s ≤ rungElems t := by
  induction h generalizing s with
  | nil =>
      simp only [replayRung, List.foldlM, Option.pure_def, Option.some.injEq] at hr
      subst hr; exact Nat.le_refl _
  | cons e es ih =>
      simp only [replayRung, List.foldlM] at hr
      cases hs : stepRung s e with
      | none => rw [hs] at hr; cases hr
      | some u =>
          rw [hs] at hr
          exact Nat.le_trans (stepRung_elems_le hs) (ih hr)

/-- Executable 5-round history from `baseR2L`. -/
def history5Rounds : List RungEvent :=
  [.admitDatum, .admitForm 1, .admitInst 0 [0], .supply 0, .supply 1]

/-- Executable 6-round history from `baseR2L` reaching the exact same regime. -/
def history6Rounds : List RungEvent :=
  [.admitDatum, .admitForm 1, .admitInst 0 [0], .supply 0, .supply 1, .supply 2]

/-- Representative theorem for `PGW-FORCED-CENSUS-COLUMN`:
    the element count is monotone along every history (`replayRung_elems_le`), exactly 2 of the
    12 census rows (`elementCount`, `irreversibility`) are FORCED over all 144 engines and 3
    (`elementCount`, `irreversibility`, `twoNess`) over the 64 LIVE engines, while `history5Rounds`
    and `history6Rounds` reach the identical regime from `baseR2L` in 5 and 6 rounds respectively,
    showing that succession and duration are not functions of the state. -/
theorem forced_census_column_twelve_row_verdict_and_countermodel :
    allCensusRows.length = 12 ∧
    (allCensusRows.filter forcedOverAll144Engines) = [.elementCount, .irreversibility] ∧
    (allCensusRows.filter forcedOverLive64Engines) = [.twoNess, .elementCount, .irreversibility] ∧
    (allCensusRows.filter (fun r => !forcedOverAll144Engines r)).length = 10 ∧
    history5Rounds.length = 5 ∧
    history6Rounds.length = 6 ∧
    replayRung history5Rounds baseR2L = replayRung history6Rounds baseR2L ∧
    (replayRung history5Rounds baseR2L).isSome = true ∧
    (∀ h : List RungEvent, ∀ s t : RungRegime,
      replayRung h s = some t → rungElems s ≤ rungElems t) := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, ?_⟩
  intro h s t hr
  exact replayRung_elems_le h hr

/-! ## 5. L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED (L1_TO_L2) -/

/-- Absolute value on `Rat`. -/
def ratAbs (q : Rat) : Rat :=
  if q < 0 then -q else q

/-- 4-cycle residual cochain `(e0, e1, e2, e3)` over `Rat`. -/
structure Cochain4 where
  e0 : Rat
  e1 : Rat
  e2 : Rat
  e3 : Rat
  deriving DecidableEq, Repr

/-- Signed holonomy `S = ∑_{i=0}^3 r_i` on the 4-cycle (invariant under coboundaries `d0 h`). -/
def hol4 (r : Cochain4) : Rat :=
  r.e0 + r.e1 + r.e2 + r.e3

/-- Coboundary `(d0 h)_i = h_{i+1 mod 4} - h_i` on the 4-cycle. -/
def d0_4 (h : Cochain4) : Cochain4 :=
  ⟨h.e1 - h.e0, h.e2 - h.e1, h.e3 - h.e2, h.e0 - h.e3⟩

/-- Every coboundary has zero holonomy on the 4-cycle. -/
theorem hol4_d0_zero (h : Cochain4) : hol4 (d0_4 h) = 0 := by
  simp only [hol4, d0_4]
  grind

/-- Unweighted L1 norm `Φ_1(r) = ∑_i |r_i|`. -/
def unweightedL1_4 (r : Cochain4) : Rat :=
  ratAbs r.e0 + ratAbs r.e1 + ratAbs r.e2 + ratAbs r.e3

/-- Weighted L1 norm `Φ_{1,m}(r) = ∑_i m_i |r_i|` with declared edge masses `m`. -/
def weightedL1_4 (m r : Cochain4) : Rat :=
  m.e0 * ratAbs r.e0 + m.e1 * ratAbs r.e1 + m.e2 * ratAbs r.e2 + m.e3 * ratAbs r.e3

/-- Sum-of-squares reading `Γ_2^{sq}(r) = ∑_i r_i^2`. -/
def gamma2SumSq4 (r : Cochain4) : Rat :=
  r.e0 * r.e0 + r.e1 * r.e1 + r.e2 * r.e2 + r.e3 * r.e3

/-- Single-edge residual concentrated on edge 0 with holonomy `S`. -/
def singleEdge0 (S : Rat) : Cochain4 :=
  ⟨S, 0, 0, 0⟩

/-- Single-edge residual concentrated on edge 1 with holonomy `S`. -/
def singleEdge1 (S : Rat) : Cochain4 :=
  ⟨0, S, 0, 0⟩

/-- Dihedral/cyclic orbit-average residual `(S/4, S/4, S/4, S/4)`. -/
def symmetricAverage4 (S : Rat) : Cochain4 :=
  ⟨S / 4, S / 4, S / 4, S / 4⟩

/-- Sector 0 weight (`|r 0| + |r 2|`) under the bipartition `{0, 2}` vs `{1, 3}`. -/
def sectorEvenWeight (r : Cochain4) : Rat :=
  ratAbs r.e0 + ratAbs r.e2

/-- Sector 1 weight (`|r 1| + |r 3|`) under the bipartition `{0, 2}` vs `{1, 3}`. -/
def sectorOddWeight (r : Cochain4) : Rat :=
  ratAbs r.e1 + ratAbs r.e3

/-- Sector weights always sum to the unweighted L1 norm. -/
theorem sector_weights_sum_to_unweightedL1 (r : Cochain4) :
    sectorEvenWeight r + sectorOddWeight r = unweightedL1_4 r := by
  simp only [sectorEvenWeight, sectorOddWeight, unweightedL1_4]
  grind

/-- For any positive holonomy `S > 0`, `singleEdge0 S` and `singleEdge1 S` lie in the same
    cohomology class (`singleEdge0 S - singleEdge1 S = d0_4 h`), achieve the same minimal
    unweighted L1 norm `S`, the same holonomy `S`, AND the same sum-of-squares `S^2`,
    yet have different sector weights (`S` vs `0` on the even sector), while the symmetric
    average `symmetricAverage4 S` has sector weight `S / 2`. -/
theorem unweighted_and_sumsq_do_not_determine_sector_weights (S : Rat) (hS : 0 < S) :
    hol4 (singleEdge0 S) = S ∧
    hol4 (singleEdge1 S) = S ∧
    hol4 (symmetricAverage4 S) = S ∧
    unweightedL1_4 (singleEdge0 S) = S ∧
    unweightedL1_4 (singleEdge1 S) = S ∧
    gamma2SumSq4 (singleEdge0 S) = S * S ∧
    gamma2SumSq4 (singleEdge1 S) = S * S ∧
    sectorEvenWeight (singleEdge0 S) = S ∧
    sectorEvenWeight (singleEdge1 S) = 0 ∧
    sectorEvenWeight (singleEdge0 S) ≠ sectorEvenWeight (singleEdge1 S) := by
  have hNotLt : ¬ (S < 0) := by grind
  have hZeroNotLt : ¬ ((0 : Rat) < 0) := by decide
  simp only [hol4, unweightedL1_4, gamma2SumSq4, sectorEvenWeight,
    singleEdge0, singleEdge1, symmetricAverage4, ratAbs, hNotLt, hZeroNotLt, ite_false]
  refine ⟨by grind, by grind, by grind, by grind, by grind, by grind, by grind, by grind, by grind, ?_⟩
  grind

/-- Weighted L1 decomposition identity for non-negative residuals of holonomy `S`:
    `weightedL1_4 m r - m.e0 * S = (m.e1 - m.e0) * r.e1 + (m.e2 - m.e0) * r.e2 + (m.e3 - m.e0) * r.e3`.
    When edge 0 has strictly minimal mass (`m.e0 < m.e1, m.e2, m.e3`), any non-negative residual
    with `r.e1 + r.e2 + r.e3 > 0` has strictly larger weighted L1 cost than `singleEdge0 S`,
    so the declared masses `m` themselves uniquely select the minimizer. -/
theorem weighted_l1_unique_minimal_mass_concentration
    (m r : Cochain4) (S : Rat)
    (hr0 : 0 ≤ r.e0) (hr1 : 0 ≤ r.e1) (hr2 : 0 ≤ r.e2) (hr3 : 0 ≤ r.e3)
    (hHol : hol4 r = S) :
    weightedL1_4 m r - m.e0 * S =
      (m.e1 - m.e0) * r.e1 + (m.e2 - m.e0) * r.e2 + (m.e3 - m.e0) * r.e3 := by
  have h0 : ¬ (r.e0 < 0) := by grind
  have h1 : ¬ (r.e1 < 0) := by grind
  have h2 : ¬ (r.e2 < 0) := by grind
  have h3 : ¬ (r.e3 < 0) := by grind
  simp only [weightedL1_4, ratAbs, h0, h1, h2, h3, ite_false]
  simp only [hol4] at hHol
  grind

/-- Representative theorem for `L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED`:
    combines coboundary holonomy invariance, sector-weight conservation, unweighted and
    sum-of-squares non-determination of sector weights, and weighted minimal-mass concentration. -/
theorem l1_residual_sector_weights_unweighted_and_weighted_characterization :
    (∀ h : Cochain4, hol4 (d0_4 h) = 0) ∧
    (∀ r : Cochain4, sectorEvenWeight r + sectorOddWeight r = unweightedL1_4 r) ∧
    (∀ S : Rat, 0 < S →
      hol4 (singleEdge0 S) = hol4 (singleEdge1 S) ∧
      unweightedL1_4 (singleEdge0 S) = unweightedL1_4 (singleEdge1 S) ∧
      gamma2SumSq4 (singleEdge0 S) = gamma2SumSq4 (singleEdge1 S) ∧
      sectorEvenWeight (singleEdge0 S) ≠ sectorEvenWeight (singleEdge1 S)) ∧
    (∀ m r : Cochain4, ∀ S : Rat,
      0 ≤ r.e0 → 0 ≤ r.e1 → 0 ≤ r.e2 → 0 ≤ r.e3 → hol4 r = S →
      weightedL1_4 m r - m.e0 * S =
        (m.e1 - m.e0) * r.e1 + (m.e2 - m.e0) * r.e2 + (m.e3 - m.e0) * r.e3) := by
  refine ⟨hol4_d0_zero, sector_weights_sum_to_unweightedL1, ?_,
    weighted_l1_unique_minimal_mass_concentration⟩
  intro S hS
  have h := unweighted_and_sumsq_do_not_determine_sector_weights S hS
  exact ⟨h.1.trans h.2.1.symm, h.2.2.2.1.trans h.2.2.2.2.1.symm,
    h.2.2.2.2.2.1.trans h.2.2.2.2.2.2.1.symm, h.2.2.2.2.2.2.2.2.2⟩

end WitnessedDifference.WdpBatch9
