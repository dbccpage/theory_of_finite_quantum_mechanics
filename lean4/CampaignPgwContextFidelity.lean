/-!
# Campaign finite case for PGW-CONTEXT-FIDELITY

AuthorityEffect: None.

Two-value carrier only. `false` is the stale context and `true` is the context
after `designateA`. This is not the sealed Genesis grammar and not `certifies`.
-/

namespace CampaignPgwContextFidelity

abbrev State := Bool

inductive Event where
  | supplyDiamond
  | designateA
  deriving DecidableEq, Repr

inductive Step where
  | assertOnlyDiamond
  | assertHasA
  deriving DecidableEq, Repr

inductive Answer where
  | verified
  | retracted
  deriving DecidableEq, Repr

def replayStep (s : State) : Event → State
  | .supplyDiamond => s
  | .designateA => true

def replay (h : List Event) : State :=
  h.foldl replayStep false

def stepValid (s : State) : Step → Prop
  | .assertOnlyDiamond => s = false
  | .assertHasA => s = true

def validTrace (s : State) (τ : List Step) : Prop :=
  ∀ st ∈ τ, stepValid s st

def separatingStep (s' : State) : Step :=
  if s' then Step.assertHasA else Step.assertOnlyDiamond

def separatingTrace (s' : State) : List Step :=
  [separatingStep s']

theorem separatingStep_valid (s' : State) : stepValid s' (separatingStep s') := by
  cases s' <;> simp [separatingStep, stepValid]

theorem separatingStep_invalid {s s' : State} (hne : s ≠ s') :
    ¬ stepValid s (separatingStep s') := by
  cases s' <;> cases s <;> simp [separatingStep, stepValid] at hne ⊢

theorem stale_not_transferred (s s' : State) (hne : s ≠ s') :
    validTrace s' (separatingTrace s') ∧ ¬ validTrace s (separatingTrace s') := by
  constructor
  · intro st hmem
    simp [separatingTrace] at hmem
    subst hmem
    exact separatingStep_valid s'
  · intro hval
    exact separatingStep_invalid hne (hval (separatingStep s') (by simp [separatingTrace]))

def acceptEqual (c : State) (h : List Event) : Prop :=
  c = replay h

def ContractSound (accept : State → List Event → Prop) : Prop :=
  ∀ c h, accept c h → ∀ τ, validTrace c τ → validTrace (replay h) τ

theorem acceptEqual_sound : ContractSound acceptEqual := by
  intro c h heq τ hτ st hmem
  exact heq ▸ hτ st hmem

theorem sound_implies_equal {accept : State → List Event → Prop}
    (hs : ContractSound accept) {c : State} {h : List Event}
    (ha : accept c h) : c = replay h :=
  Classical.byContradiction fun hne =>
    let hsep := stale_not_transferred (replay h) c (Ne.symm hne)
    hsep.2 (hs c h ha (separatingTrace c) hsep.1)

theorem equal_implies_sound {accept : State → List Event → Prop}
    (hs : ∀ c h, accept c h → c = replay h) : ContractSound accept := by
  intro c h ha τ hτ st hmem
  simpa [hs c h ha] using hτ st hmem

theorem sound_iff_only_replay (accept : State → List Event → Prop) :
    ContractSound accept ↔ ∀ c h, accept c h → c = replay h :=
  ⟨fun hs _ _ ha => sound_implies_equal hs ha, equal_implies_sound⟩

def answerOnlyDiamond (h : List Event) : Answer :=
  if replay h = false then Answer.verified else Answer.retracted

theorem replay_supply : replay [Event.supplyDiamond] = false := rfl

theorem replay_full : replay [Event.supplyDiamond, Event.designateA] = true := rfl

theorem truncated_verified :
    answerOnlyDiamond [Event.supplyDiamond] = Answer.verified := by
  simp [answerOnlyDiamond, replay_supply]

theorem full_retracted :
    answerOnlyDiamond [Event.supplyDiamond, Event.designateA] = Answer.retracted := by
  simp [answerOnlyDiamond, replay_full]

theorem answers_follow_received_history :
    answerOnlyDiamond [Event.supplyDiamond] = Answer.verified ∧
      answerOnlyDiamond [Event.supplyDiamond, Event.designateA] = Answer.retracted ∧
      replay [Event.supplyDiamond] = false ∧
      replay [Event.supplyDiamond, Event.designateA] = true :=
  ⟨truncated_verified, full_retracted, replay_supply, replay_full⟩

def allStates : List State := [false, true]

def unequalPairs : List (State × State) :=
  allStates.flatMap fun s => (allStates.filter fun s' => s != s').map fun s' => (s, s')

theorem unequal_pair_count : unequalPairs.length = 2 := rfl

def shortEvents : List Event := [Event.supplyDiamond, Event.designateA]

def historiesAtMost2 : List (List Event) :=
  [[]] ++ shortEvents.map (fun e => [e]) ++
    (shortEvents.flatMap fun e1 => shortEvents.map fun e2 => [e1, e2])

theorem history_count : historiesAtMost2.length = 7 := rfl

end CampaignPgwContextFidelity

#print axioms CampaignPgwContextFidelity.separatingStep_valid
#print axioms CampaignPgwContextFidelity.separatingStep_invalid
#print axioms CampaignPgwContextFidelity.stale_not_transferred
#print axioms CampaignPgwContextFidelity.acceptEqual_sound
#print axioms CampaignPgwContextFidelity.sound_implies_equal
#print axioms CampaignPgwContextFidelity.equal_implies_sound
#print axioms CampaignPgwContextFidelity.sound_iff_only_replay
#print axioms CampaignPgwContextFidelity.replay_supply
#print axioms CampaignPgwContextFidelity.replay_full
#print axioms CampaignPgwContextFidelity.truncated_verified
#print axioms CampaignPgwContextFidelity.full_retracted
#print axioms CampaignPgwContextFidelity.answers_follow_received_history
#print axioms CampaignPgwContextFidelity.unequal_pair_count
#print axioms CampaignPgwContextFidelity.history_count
