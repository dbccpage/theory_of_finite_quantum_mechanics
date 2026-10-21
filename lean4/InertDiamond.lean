import Mathlib.Logic.Function.Basic

/-!
# The inert inscription `<>`: a finite admission model, inertness, and independence from the coproduct root

AuthorityEffect: None.  Scope: a finite event model in the style of the Genesis construction
(`GenesisConstruction.lean`, `genesis_construction.rs`): an event is a SUPPLY of a token (mention), an
ADMISSION of a token as a datum, or an ADMISSION of a form of a given arity (the three-event fragment of the
six-operation alphabet; instance, rule and imposition events are NOT modelled).  `root` is the distinguished
literal `<>`, any token type `Tok` with decidable equality.

The DAG node PG-INERT-DIAMOND is a DEFINITION ("`<>` is a literal inscription, supplied or mentioned but
carrying no object-language meaning until an admission event; it is not defined as the root
`Real_0 = Difference ⊔ Structure`").  A definition has no proof obligation, so this file proves the honest
substitute: (1) the model's rule "supply never changes the admitted state" yields inertness of the inscription
for every function of the admitted state in the UNROOTED replay, whatever the number or position of mentions
(in the ROOTED replay, which mirrors the Rust gate, the first supply of `<>` is an admission precondition and
only later supplies are inert); (2) the same
definition is consistent with, and independent of, the MODEL PREDICATE `HasCoproduct` (an admitted Difference-classified and an
admitted Structure-classified datum), not of the identification itself, which is not modelled: some histories that inscribe
`<>` have no coproduct structure, some that have coproduct structure inscribe nothing (unrooted model only), and a history that only
supplies or only admits `<>` has none for any classification of tokens; (3) the inertness is a RULE of the model,
not a consequence of the spelling `<>` (a rival step rule that admits on supply is exhibited).  Nothing here
derives or refutes the root identification in any other model, and nothing is physical.
-/

namespace InertDiamond

variable {Tok : Type} [DecidableEq Tok]

/-- The three-event fragment of the six-operation alphabet. -/
inductive Ev (Tok : Type) where
  | supply (t : Tok)
  | admit (t : Tok)
  | form (arity : Nat)
  deriving DecidableEq

/-- Admitted state: the admitted data (no duplicates) and the admitted form arities. -/
@[ext]
structure St (Tok : Type) where
  data : List Tok
  forms : List Nat
  deriving DecidableEq

/-- The empty (pre-Genesis) state. -/
def init : St Tok := ⟨[], []⟩

/-- One event.  Supply is the identity; re-admission of a datum designates (no duplicate); arity 0 is refused. -/
def step (s : St Tok) : Ev Tok → Option (St Tok)
  | .supply _ => some s
  | .admit t => if t ∈ s.data then some s else some ⟨s.data ++ [t], s.forms⟩
  | .form n => if 1 ≤ n then some ⟨s.data, s.forms ++ [n]⟩ else none

/-- Replay of a finite event list from a state. -/
def replay : List (Ev Tok) → St Tok → Option (St Tok)
  | [], s => some s
  | e :: es, s =>
    match step s e with
    | none => none
    | some s' => replay es s'

/-- Admission-class event: anything but a supply. -/
def isAdmission : Ev Tok → Bool
  | .supply _ => false
  | _ => true

theorem step_supply (s : St Tok) (t : Tok) : step s (Ev.supply t) = some s := rfl

theorem replay_supply_cons (t : Tok) (es : List (Ev Tok)) (s : St Tok) :
    replay (Ev.supply t :: es) s = replay es s := rfl

/-- Inertness: deleting every supply event from a history changes neither the outcome nor a refusal. -/
theorem replay_filter_supply (es : List (Ev Tok)) :
    ∀ s : St Tok, replay (es.filter isAdmission) s = replay es s := by
  induction es with
  | nil => intro s; rfl
  | cons e es ih =>
    intro s
    cases e with
    | supply t => exact ih s
    | admit t =>
      show replay (Ev.admit t :: es.filter isAdmission) s = replay (Ev.admit t :: es) s
      show (match step s (Ev.admit t) with | none => none | some s' => replay (es.filter isAdmission) s') =
        (match step s (Ev.admit t) with | none => none | some s' => replay es s')
      cases step s (Ev.admit t) with
      | none => rfl
      | some s' => exact ih s'
    | form n =>
      show (match step s (Ev.form n) with | none => none | some s' => replay (es.filter isAdmission) s') =
        (match step s (Ev.form n) with | none => none | some s' => replay es s')
      cases step s (Ev.form n) with
      | none => rfl
      | some s' => exact ih s'

/-- Two histories with the same admission-class subsequence have the same outcome: how many times, and where,
`<>` (or any token) is merely supplied is invisible to every function of the replay outcome. -/
theorem replay_eq_of_same_admissions (es fs : List (Ev Tok))
    (h : es.filter isAdmission = fs.filter isAdmission) (s : St Tok) :
    replay es s = replay fs s := by
  rw [← replay_filter_supply es s, ← replay_filter_supply fs s, h]

/-- Any function of the admitted outcome is independent of the number of mentions of `<>`. -/
theorem mention_count_irrelevant {X : Type} (φ : Option (St Tok) → X) (root : Tok) (k : Nat)
    (es : List (Ev Tok)) (s : St Tok) :
    φ (replay (List.replicate k (Ev.supply root) ++ es) s) = φ (replay es s) := by
  induction k with
  | zero => rfl
  | succ k ih => exact ih

/-- A history made only of supplies leaves the state untouched. -/
theorem replay_all_supplies (ts : List Tok) (s : St Tok) :
    replay (ts.map Ev.supply) s = some s := by
  induction ts with
  | nil => rfl
  | cons t ts ih => exact ih

/-- Only admission-class events change the state (converse of inertness). -/
theorem step_changes_only_by_admission (s s' : St Tok) (e : Ev Tok) (h : step s e = some s') (hne : s' ≠ s) :
    isAdmission e = true := by
  cases e with
  | supply t => exact absurd (Option.some.inj h).symm hne
  | admit t => rfl
  | form n => rfl

/-- Admitting a token that is not yet a datum DOES change the state. -/
theorem admit_changes_state (s : St Tok) (t : Tok) (ht : t ∉ s.data) :
    ∃ s', step s (Ev.admit t) = some s' ∧ s' ≠ s := by
  refine ⟨⟨s.data ++ [t], s.forms⟩, ?_, ?_⟩
  · show (if t ∈ s.data then some s else some ⟨s.data ++ [t], s.forms⟩) = _
    split
    · contradiction
    · rfl
  · intro heq
    have this : s.data ++ [t] = s.data := congrArg St.data heq
    have hlen := congrArg List.length this
    have h2 : (s.data ++ [t]).length = s.data.length + 1 := List.length_append
    omega

/-- Supplying the root leaves the empty state; admitting it afterwards produces a different state. -/
theorem supply_then_admit_root (root : Tok) :
    replay [Ev.supply root] (init : St Tok) = some init ∧
    replay [Ev.supply root, Ev.admit root] (init : St Tok) = some ⟨[root], []⟩ ∧
    (some init : Option (St Tok)) ≠ some ⟨[root], []⟩ := by
  refine ⟨rfl, ?_, ?_⟩
  · show (if root ∈ ([] : List Tok) then some init else some ⟨[] ++ [root], []⟩) = _
    split
    · contradiction
    · rfl
  · intro h
    have := congrArg St.data (Option.some.inj h)
    exact List.cons_ne_nil root [] (this.symm)

/-! ## Rooted replay, as in the Rust construction: the first event must be the supply of `<>` -/

def replayRooted (root : Tok) : List (Ev Tok) → Option (St Tok)
  | Ev.supply t :: es => if t = root then replay es init else none
  | _ => none

theorem rooted_refuses_without_root (root d : Tok) (hd : d ≠ root) (es : List (Ev Tok)) :
    replayRooted root (Ev.admit d :: es) = none ∧ replayRooted root ([] : List (Ev Tok)) = none ∧
      replayRooted root (Ev.supply d :: es) = none := by
  refine ⟨rfl, rfl, ?_⟩
  show (if d = root then replay es init else none) = none
  split
  · contradiction
  · rfl

/-- In the rooted replay the FIRST supply of the literal is an admission precondition: dropping it from an
accepted history turns acceptance into refusal.  (Contrast `replay_filter_supply`, which concerns the unrooted replay.) -/
theorem rooted_root_supply_is_precondition (root : Tok) (u : List (Ev Tok)) (hu : ∀ t, u.head? ≠ some (Ev.supply t)) :
    replayRooted root u = none ∧ replayRooted root (Ev.supply root :: u) = replay u init := by
  refine ⟨?_, ?_⟩
  · cases u with
    | nil => rfl
    | cons e es =>
      cases e with
      | supply t => exact absurd rfl (hu t)
      | admit t => rfl
      | form n => rfl
  · show (if root = root then replay u init else none) = _
    split
    · rfl
    · contradiction

/-- In the rooted replay every supply AFTER the first event is inert: deleting them changes nothing. -/
theorem rooted_later_supply_inert (root : Tok) (es : List (Ev Tok)) :
    replayRooted root (Ev.supply root :: es.filter isAdmission) = replayRooted root (Ev.supply root :: es) := by
  show (if root = root then replay (es.filter isAdmission) init else none) = (if root = root then replay es init else none)
  rw [replay_filter_supply es init]

theorem rooted_inscription_alone (root : Tok) : replayRooted root [Ev.supply root] = some (init : St Tok) := by
  show (if root = root then replay [] init else none) = _
  split
  · rfl
  · contradiction

/-! ## The coproduct identification is not derivable from the inscription -/

inductive Chan where
  | diff
  | struct
  deriving DecidableEq

/-- The two-channel structure of a state, relative to a classification of tokens into channels:
both a Difference datum and a Structure datum are admitted. -/
def HasCoproduct (cls : Tok → Option Chan) (s : St Tok) : Prop :=
  (∃ t ∈ s.data, cls t = some Chan.diff) ∧ (∃ t ∈ s.data, cls t = some Chan.struct)

omit [DecidableEq Tok] in
theorem no_coproduct_init (cls : Tok → Option Chan) : ¬ HasCoproduct cls (init : St Tok) := by
  rintro ⟨⟨t, ht, _⟩, _⟩
  cases ht

omit [DecidableEq Tok] in
/-- One admitted token cannot carry two channels, whatever the classification. -/
theorem no_coproduct_of_single_token (cls : Tok → Option Chan) (root : Tok) (s : St Tok)
    (hs : ∀ x ∈ s.data, x = root) : ¬ HasCoproduct cls s := by
  rintro ⟨⟨t, ht, ht'⟩, ⟨u, hu, hu'⟩⟩
  have e1 := hs t ht
  have e2 := hs u hu
  rw [e1] at ht'
  rw [e2] at hu'
  rw [ht'] at hu'
  exact Chan.noConfusion (Option.some.inj hu')

/-- A history that only supplies and admits `<>` stays inside `{<>}`, hence never has coproduct structure. -/
theorem root_only_no_coproduct (cls : Tok → Option Chan) (root : Tok) :
    ∀ (es : List (Ev Tok)) (s : St Tok), (∀ x ∈ s.data, x = root) →
      (∀ e ∈ es, e = Ev.supply root ∨ e = Ev.admit root) →
      ∀ s', replay es s = some s' → ¬ HasCoproduct cls s' := by
  intro es
  induction es with
  | nil =>
    intro s hs _ s' h
    have : s = s' := Option.some.inj h
    subst this
    exact no_coproduct_of_single_token cls root s hs
  | cons e es ih =>
    intro s hs hes s' h
    have he := hes e (List.mem_cons_self)
    have hes' : ∀ e' ∈ es, e' = Ev.supply root ∨ e' = Ev.admit root :=
      fun e' he' => hes e' (List.mem_cons_of_mem e he')
    rcases he with rfl | rfl
    · exact ih s hs hes' s' h
    · by_cases hm : root ∈ s.data
      · have hstep : step s (Ev.admit root) = some s := by
          show (if root ∈ s.data then some s else some ⟨s.data ++ [root], s.forms⟩) = _
          split
          · rfl
          · contradiction
        have h' : replay es s = some s' := by
          have : replay (Ev.admit root :: es) s = replay es s := by
            show (match step s (Ev.admit root) with | none => none | some s'' => replay es s'') = _
            rw [hstep]
          rw [← this]; exact h
        exact ih s hs hes' s' h'
      · have hstep : step s (Ev.admit root) = some ⟨s.data ++ [root], s.forms⟩ := by
          show (if root ∈ s.data then some s else some ⟨s.data ++ [root], s.forms⟩) = _
          split
          · contradiction
          · rfl
        have h' : replay es ⟨s.data ++ [root], s.forms⟩ = some s' := by
          have : replay (Ev.admit root :: es) s = replay es ⟨s.data ++ [root], s.forms⟩ := by
            show (match step s (Ev.admit root) with | none => none | some s'' => replay es s'') = _
            rw [hstep]
          rw [← this]; exact h
        refine ih ⟨s.data ++ [root], s.forms⟩ ?_ hes' s' h'
        intro x hx
        cases List.mem_append.mp hx with
        | inl hx => exact hs x hx
        | inr hx => simpa using hx

/-- Instance: tokens `0 = <>`, `1` (a Difference datum), `2` (a Structure datum). -/
def cls3 : Fin 3 → Option Chan
  | 0 => none
  | 1 => some Chan.diff
  | 2 => some Chan.struct

/-- Instance: a history that inscribes `<>` and reaches coproduct structure only by admitting the two channels. -/
theorem rooted_with_coproduct :
    ∃ s, replayRooted (0 : Fin 3) [Ev.supply 0, Ev.admit 1, Ev.admit 2] = some s ∧ HasCoproduct cls3 s := by
  refine ⟨⟨[1, 2], []⟩, rfl, ?_⟩
  refine ⟨⟨1, by simp, rfl⟩, ⟨2, by simp, rfl⟩⟩

/-- Instance: coproduct structure with NO inscription in the unrooted model (the rooted replay refuses it). -/
theorem coproduct_without_inscription :
    (∃ s, replay [Ev.admit (1 : Fin 3), Ev.admit 2] init = some s ∧ HasCoproduct cls3 s) ∧
    replayRooted (0 : Fin 3) [Ev.admit 1, Ev.admit 2] = none := by
  refine ⟨⟨⟨[1, 2], []⟩, rfl, ?_⟩, rfl⟩
  refine ⟨⟨1, by simp, rfl⟩, ⟨2, by simp, rfl⟩⟩

/-- Instance: inscription (supply, then admission of `<>` itself) without coproduct structure. -/
theorem inscription_without_coproduct :
    ∃ s, replayRooted (0 : Fin 3) [Ev.supply 0, Ev.admit 0] = some s ∧ ¬ HasCoproduct cls3 s :=
  ⟨⟨[0], []⟩, rfl, no_coproduct_of_single_token cls3 0 _ (by intro x hx; simpa using hx)⟩

/-- Same supply subsequence, different admitted structure: the inscription does not determine the coproduct. -/
theorem inscription_does_not_determine_coproduct :
    ∃ es fs : List (Ev (Fin 3)), (es.filter (fun e => !isAdmission e) = fs.filter (fun e => !isAdmission e)) ∧
      (∃ s, replayRooted 0 es = some s ∧ ¬ HasCoproduct cls3 s) ∧
      (∃ s, replayRooted 0 fs = some s ∧ HasCoproduct cls3 s) := by
  refine ⟨[Ev.supply 0], [Ev.supply 0, Ev.admit 1, Ev.admit 2], rfl, ?_, ?_⟩
  · exact ⟨init, rfl, no_coproduct_init cls3⟩
  · exact rooted_with_coproduct

/-! ## Inertness is a rule of the model, not of the spelling -/

/-- A rival step rule that admits on supply: under it the supplied token DOES become a datum. -/
def stepAdmitting (s : St Tok) : Ev Tok → Option (St Tok)
  | .supply t => step s (.admit t)
  | e => step s e

theorem rival_supply_not_inert (root : Tok) :
    stepAdmitting (init : St Tok) (Ev.supply root) ≠ some init ∧ step (init : St Tok) (Ev.supply root) = some init := by
  refine ⟨?_, rfl⟩
  intro h
  have h1 : stepAdmitting (init : St Tok) (Ev.supply root) = some ⟨[root], []⟩ := by
    show (if root ∈ ([] : List Tok) then some init else some ⟨[] ++ [root], []⟩) = _
    split
    · contradiction
    · rfl
  rw [h1] at h
  have := congrArg St.data (Option.some.inj h)
  exact List.cons_ne_nil root [] this

end InertDiamond

#print axioms InertDiamond.replay_filter_supply
#print axioms InertDiamond.replay_eq_of_same_admissions
#print axioms InertDiamond.mention_count_irrelevant
#print axioms InertDiamond.step_changes_only_by_admission
#print axioms InertDiamond.admit_changes_state
#print axioms InertDiamond.supply_then_admit_root
#print axioms InertDiamond.rooted_refuses_without_root
#print axioms InertDiamond.rooted_root_supply_is_precondition
#print axioms InertDiamond.rooted_later_supply_inert
#print axioms InertDiamond.no_coproduct_of_single_token
#print axioms InertDiamond.root_only_no_coproduct
#print axioms InertDiamond.rooted_with_coproduct
#print axioms InertDiamond.coproduct_without_inscription
#print axioms InertDiamond.inscription_without_coproduct
#print axioms InertDiamond.inscription_does_not_determine_coproduct
#print axioms InertDiamond.rival_supply_not_inert
