/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/wdp_reasoning/ExecutableReasoning.lean
   Original sha256: 45e84a8230275c507a559e30a2321fa2a01614460d64dceb03f5c3772bce9206 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.WdpReasoning.ExecutableReasoning
   Reason         : WDP
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.WdpReasoning.WitnessedReasoning

namespace WitnessedReasoning.Executable

structure FiniteRule where
  premises : List Nat
  conclusion : Nat
  deriving DecidableEq, Repr

def FiniteRule.abstract (r : FiniteRule) : Rule Nat :=
  ⟨r.premises, r.conclusion⟩

structure FiniteTheory where
  atoms : List String
  facts : List Nat
  rules : List FiniteRule
  deriving DecidableEq, Repr

def FiniteTheory.abstract (T : FiniteTheory) : Theory Nat where
  fact a := a ∈ T.facts
  rule r := ∃ f, f ∈ T.rules ∧ r = f.abstract

def FiniteTheory.Valid (T : FiniteTheory) : Prop :=
  T.atoms.Pairwise (· ≠ ·) ∧ (∀ a ∈ T.atoms, a ≠ "") ∧
  (∀ a ∈ T.facts, a < T.atoms.length) ∧
  (∀ r ∈ T.rules, r.conclusion < T.atoms.length ∧
    ∀ a ∈ r.premises, a < T.atoms.length)

instance (T : FiniteTheory) : Decidable T.Valid := by
  unfold FiniteTheory.Valid
  infer_instance

structure IndexStep where
  conclusion : Nat
  rule : Option Nat
  premises : List Nat
  deriving DecidableEq, Repr

structure ProofCertificate where
  theory : FiniteTheory
  goal : Nat
  steps : List IndexStep
  deriving DecidableEq, Repr

structure ModelCertificate where
  theory : FiniteTheory
  goal : Nat
  values : List Bool
  deriving DecidableEq, Repr

def references (known : List Nat) : List Nat → List Nat → Bool
  | [], [] => true
  | i :: ids, a :: atoms => decide (known[i]? = some a) && references known ids atoms
  | _, _ => false

theorem references_sound {known ids atoms : List Nat}
    (h : references known ids atoms = true) : ∀ a ∈ atoms, a ∈ known := by
  induction ids generalizing atoms with
  | nil =>
    cases atoms with
    | nil => simp
    | cons a rest => simp [references] at h
  | cons i ids ih =>
    cases atoms with
    | nil => simp [references] at h
    | cons a rest =>
      simp only [references, Bool.and_eq_true, decide_eq_true_eq] at h
      intro x hx
      cases hx with
      | head => exact List.mem_of_getElem? h.1
      | tail _ hx => exact ih h.2 x hx

def checkStep (T : FiniteTheory) (known : List Nat) (s : IndexStep) : Bool :=
  decide (s.conclusion < T.atoms.length) &&
  match s.rule with
  | none => decide (s.conclusion ∈ T.facts ∧ s.premises = [])
  | some i => match T.rules[i]? with
    | none => false
    | some r => decide (s.conclusion = r.conclusion) && references known s.premises r.premises

def KnownSound (T : FiniteTheory) (known : List Nat) : Prop :=
  ∀ a ∈ known, Derivable T.abstract a

theorem checkStep_sound {T : FiniteTheory} {known : List Nat} {s : IndexStep}
    (hk : KnownSound T known) (h : checkStep T known s = true) :
    Derivable T.abstract s.conclusion := by
  simp only [checkStep, Bool.and_eq_true, decide_eq_true_eq] at h
  cases hr : s.rule with
  | none =>
    simp only [hr, decide_eq_true_eq] at h
    exact Derivable.fact _ h.2.1
  | some i =>
    cases he : T.rules[i]? with
    | none => simp [hr, he] at h
    | some r =>
      simp only [hr, he, Bool.and_eq_true, decide_eq_true_eq] at h
      rw [h.2.1]
      exact Derivable.fire r.abstract ⟨r, List.mem_of_getElem? he, rfl⟩
        (fun a ha => hk a (references_sound h.2.2 a ha))

def replay (T : FiniteTheory) : List Nat → List IndexStep → Option (List Nat)
  | known, [] => some known
  | known, s :: rest =>
    if checkStep T known s then replay T (known ++ [s.conclusion]) rest else none

theorem replay_sound {T : FiniteTheory} {steps : List IndexStep}
    {known result : List Nat} (hk : KnownSound T known)
    (h : replay T known steps = some result) : KnownSound T result := by
  induction steps generalizing known with
  | nil =>
    have eq : known = result := by simpa [replay] using h
    exact eq ▸ hk
  | cons s rest ih =>
    simp only [replay] at h
    split at h
    next hs =>
      apply ih _ h
      intro a ha
      rcases List.mem_append.mp ha with ha | ha
      · exact hk a ha
      · have eq : a = s.conclusion := by simpa using ha
        exact eq ▸ checkStep_sound hk hs
    next => contradiction

theorem checkStep_justified {T : FiniteTheory} {known : List Nat} {s : IndexStep}
    (h : checkStep T known s = true) : Justified T.abstract known s.conclusion := by
  simp only [checkStep, Bool.and_eq_true, decide_eq_true_eq] at h
  cases hr : s.rule with
  | none =>
    simp only [hr, decide_eq_true_eq] at h
    exact Or.inl h.2.1
  | some i =>
    cases he : T.rules[i]? with
    | none => simp [hr, he] at h
    | some r =>
      simp only [hr, he, Bool.and_eq_true, decide_eq_true_eq] at h
      exact Or.inr ⟨r.abstract, ⟨r, List.mem_of_getElem? he, rfl⟩,
        h.2.1.symm, references_sound h.2.2⟩

theorem replay_refines_trace {T : FiniteTheory} {steps : List IndexStep}
    {known result : List Nat} (hk : CheckedTrace T.abstract known.reverse)
    (h : replay T known steps = some result) : CheckedTrace T.abstract result.reverse := by
  induction steps generalizing known with
  | nil =>
    have eq : known = result := by simpa [replay] using h
    exact eq ▸ hk
  | cons s rest ih =>
    simp only [replay] at h
    split at h
    next hs =>
      apply ih _ h
      rw [List.reverse_append]
      apply CheckedTrace.step hk
      rcases checkStep_justified hs with hf | ⟨r, hr, hc, hp⟩
      · exact Or.inl hf
      · exact Or.inr ⟨r, hr, hc, fun a ha => by simpa using hp a ha⟩
    next => contradiction

def checkProof (T : FiniteTheory) (goal : Nat) (p : ProofCertificate) : Bool :=
  decide (T.Valid ∧ goal < T.atoms.length ∧ p.theory = T ∧ p.goal = goal) &&
  match replay T [] p.steps with
  | none => false
  | some known => decide (known.getLast? = some goal)

theorem checkProof_binding {T : FiniteTheory} {goal : Nat} {p : ProofCertificate}
    (h : checkProof T goal p = true) :
    T.Valid ∧ goal < T.atoms.length ∧ p.theory = T ∧ p.goal = goal := by
  simp only [checkProof, Bool.and_eq_true, decide_eq_true_eq] at h
  exact h.1

theorem checkProof_sound {T : FiniteTheory} {goal : Nat} {p : ProofCertificate}
    (h : checkProof T goal p = true) : Derivable T.abstract goal := by
  simp only [checkProof, Bool.and_eq_true, decide_eq_true_eq] at h
  cases hr : replay T [] p.steps with
  | none => simp [hr] at h
  | some known =>
    simp only [hr, decide_eq_true_eq] at h
    exact replay_sound (by intro a ha; cases ha) hr goal (List.mem_of_getLast? h.2)

def ModelValid (T : FiniteTheory) (goal : Nat) (values : List Bool) : Prop :=
  values.length = T.atoms.length ∧ values[goal]? = some false ∧
  (∀ a ∈ T.facts, values[a]? = some true) ∧
  (∀ r ∈ T.rules, (∀ a ∈ r.premises, values[a]? = some true) →
    values[r.conclusion]? = some true)

instance (T : FiniteTheory) (goal : Nat) (values : List Bool) :
    Decidable (ModelValid T goal values) := by
  unfold ModelValid
  infer_instance

def checkCountermodel (T : FiniteTheory) (goal : Nat) (m : ModelCertificate) : Bool :=
  decide (T.Valid ∧ goal < T.atoms.length ∧ m.theory = T ∧ m.goal = goal ∧
    ModelValid T goal m.values)

theorem checkCountermodel_binding {T : FiniteTheory} {goal : Nat} {m : ModelCertificate}
    (h : checkCountermodel T goal m = true) :
    T.Valid ∧ goal < T.atoms.length ∧ m.theory = T ∧ m.goal = goal := by
  have hm := of_decide_eq_true h
  exact ⟨hm.1, hm.2.1, hm.2.2.1, hm.2.2.2.1⟩

theorem checkCountermodel_models {T : FiniteTheory} {goal : Nat} {m : ModelCertificate}
    (h : checkCountermodel T goal m = true) :
    Models T.abstract (fun a => m.values[a]? = some true) := by
  have hm := (of_decide_eq_true h).2.2.2.2
  constructor
  · exact hm.2.2.1
  · intro r hr hp
    obtain ⟨f, hf, rfl⟩ := hr
    exact hm.2.2.2 f hf hp

theorem checkCountermodel_sound {T : FiniteTheory} {goal : Nat} {m : ModelCertificate}
    (h : checkCountermodel T goal m = true) : ¬Derivable T.abstract goal := by
  have hm := (of_decide_eq_true h).2.2.2.2
  apply countermodel_excludes_derivation (checkCountermodel_models h)
  intro hg
  rw [hm.2.1] at hg
  contradiction

theorem checked_verdicts_exclusive {T : FiniteTheory} {goal : Nat}
    {p : ProofCertificate} {m : ModelCertificate} (hp : checkProof T goal p = true) :
    checkCountermodel T goal m ≠ true := by
  intro hm
  exact checkCountermodel_sound hm (checkProof_sound hp)

theorem checked_interpretation {World : Type} {T : FiniteTheory} {goal : Nat}
    {p : ProofCertificate} (h : checkProof T goal p = true)
    (meaning : World → Nat → Prop) (admitted : World → Prop)
    (sound : ∀ w, admitted w → Models T.abstract (meaning w)) :
    ∀ w, admitted w → meaning w goal :=
  interpreted_claim_sound meaning admitted sound (checkProof_sound h)

def graphTheory (atoms : List String) (edges : List (Nat × Nat)) (start : Nat) :
    FiniteTheory :=
  ⟨atoms, [start], edges.map (fun e => ⟨[e.1], e.2⟩)⟩

inductive Reachable (edges : List (Nat × Nat)) (start : Nat) : Nat → Prop where
  | refl : Reachable edges start start
  | step {u v} : Reachable edges start u → (u, v) ∈ edges → Reachable edges start v

theorem graph_derivable_reachable {atoms : List String} {edges : List (Nat × Nat)}
    {start goal : Nat} (h : Derivable (graphTheory atoms edges start).abstract goal) :
    Reachable edges start goal := by
  apply derivation_sound h
  constructor
  · intro a ha
    have eq : a = start := by simpa [FiniteTheory.abstract, graphTheory] using ha
    exact eq ▸ Reachable.refl
  · intro r hr hp
    obtain ⟨f, hf, rfl⟩ := hr
    obtain ⟨e, he, rfl⟩ := List.mem_map.mp hf
    exact Reachable.step (hp e.1 (by simp [FiniteRule.abstract])) he

theorem graph_reachable_derivable {atoms : List String} {edges : List (Nat × Nat)}
    {start goal : Nat} (h : Reachable edges start goal) :
    Derivable (graphTheory atoms edges start).abstract goal := by
  induction h with
  | refl => exact Derivable.fact _ (by simp [FiniteTheory.abstract, graphTheory])
  | @step u v _ he ih =>
    apply Derivable.fire (Rule.mk [u] v)
    · exact ⟨⟨[u], v⟩, List.mem_map.mpr ⟨(u, v), he, rfl⟩, rfl⟩
    · intro a ha
      have eq : a = u := by simpa using ha
      exact eq ▸ ih

theorem graph_derivable_iff_reachable (atoms : List String) (edges : List (Nat × Nat))
    (start goal : Nat) :
    Derivable (graphTheory atoms edges start).abstract goal ↔ Reachable edges start goal :=
  ⟨graph_derivable_reachable, graph_reachable_derivable⟩

theorem checked_graph_proof {atoms : List String} {edges : List (Nat × Nat)}
    {start goal : Nat} {p : ProofCertificate}
    (h : checkProof (graphTheory atoms edges start) goal p = true) :
    Reachable edges start goal :=
  graph_derivable_reachable (checkProof_sound h)

theorem checked_graph_countermodel {atoms : List String} {edges : List (Nat × Nat)}
    {start goal : Nat} {m : ModelCertificate}
    (h : checkCountermodel (graphTheory atoms edges start) goal m = true) :
    ¬Reachable edges start goal := by
  intro path
  exact checkCountermodel_sound h (graph_reachable_derivable path)

end WitnessedReasoning.Executable
