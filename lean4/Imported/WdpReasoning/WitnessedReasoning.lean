/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/wdp_reasoning/WitnessedReasoning.lean
   Original sha256: f063fd17bccdcfe8d5fea07a0032a3bc171c35b2a4dae76879fbf0b14c71eda0 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.WdpReasoning.WitnessedReasoning
   Reason         : WDP
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Init

namespace WitnessedReasoning

structure Rule (Atom : Type) where
  premises : List Atom
  conclusion : Atom

structure Theory (Atom : Type) where
  fact : Atom → Prop
  rule : Rule Atom → Prop

inductive Derivable {Atom : Type} (T : Theory Atom) : Atom → Prop where
  | fact (a) : T.fact a → Derivable T a
  | fire (r) : T.rule r →
      (∀ a, a ∈ r.premises → Derivable T a) → Derivable T r.conclusion

def Models {Atom : Type} (T : Theory Atom) (v : Atom → Prop) : Prop :=
  (∀ a, T.fact a → v a) ∧
  (∀ r, T.rule r → (∀ a, a ∈ r.premises → v a) → v r.conclusion)

theorem derivation_sound {Atom : Type} {T : Theory Atom} {a : Atom}
    (d : Derivable T a) {v : Atom → Prop} (hv : Models T v) : v a := by
  induction d with
  | fact a h => exact hv.1 a h
  | fire r h _ ih => exact hv.2 r h ih

theorem derivable_is_model {Atom : Type} (T : Theory Atom) :
    Models T (Derivable T) := by
  constructor
  · intro a h
    exact Derivable.fact a h
  · intro r h hp
    exact Derivable.fire r h hp

theorem derivable_iff_entailed {Atom : Type} (T : Theory Atom) (a : Atom) :
    Derivable T a ↔ ∀ v, Models T v → v a := by
  constructor
  · intro d v hv
    exact derivation_sound d hv
  · intro h
    exact h (Derivable T) (derivable_is_model T)

theorem countermodel_excludes_derivation {Atom : Type} {T : Theory Atom}
    {a : Atom} {v : Atom → Prop} (hv : Models T v) (ha : ¬v a) :
    ¬Derivable T a := by
  intro d
  exact ha (derivation_sound d hv)

def EmptyTheory (Atom : Type) : Theory Atom := ⟨fun _ => False, fun _ => False⟩

theorem inert_seed_derives_nothing {Atom : Type} (a : Atom) :
    ¬Derivable (EmptyTheory Atom) a := by
  apply countermodel_excludes_derivation (v := fun _ => False)
  · constructor
    · intro _ h; exact h
    · intro _ h; exact h.elim
  · exact id

def Justified {Atom : Type} (T : Theory Atom) (known : List Atom) (a : Atom) : Prop :=
  T.fact a ∨ ∃ r, T.rule r ∧ r.conclusion = a ∧ ∀ p, p ∈ r.premises → p ∈ known

inductive CheckedTrace {Atom : Type} (T : Theory Atom) : List Atom → Prop where
  | empty : CheckedTrace T []
  | step {known a} : CheckedTrace T known → Justified T known a →
      CheckedTrace T (a :: known)

theorem checked_trace_derivable {Atom : Type} {T : Theory Atom} {trace : List Atom}
    (h : CheckedTrace T trace) : ∀ a, a ∈ trace → Derivable T a := by
  induction h with
  | empty => intro a ha; cases ha
  | @step known b _ justified ih =>
    intro a ha
    cases ha with
    | head =>
      cases justified with
      | inl hf => exact Derivable.fact b hf
      | inr hr =>
        obtain ⟨r, hr, eq, hp⟩ := hr
        rw [← eq]
        exact Derivable.fire r hr (fun p hm => ih p (hp p hm))
    | tail _ ht => exact ih a ht

theorem checked_trace_sound {Atom : Type} {T : Theory Atom} {trace : List Atom}
    (ht : CheckedTrace T trace) {v : Atom → Prop} (hv : Models T v)
    {a : Atom} (ha : a ∈ trace) : v a :=
  derivation_sound (checked_trace_derivable ht a ha) hv

theorem learned_rule_conservative {Atom : Type} {T : Theory Atom} {a : Atom}
    (ha : Derivable T a) :
    ∀ b, Derivable (Theory.mk (fun x => T.fact x ∨ x = a) T.rule) b →
      Derivable T b := by
  intro b hb
  apply derivation_sound hb
  constructor
  · intro x hx
    cases hx with
    | inl hf => exact Derivable.fact x hf
    | inr he => exact he ▸ ha
  · intro r hr hp
    exact Derivable.fire r hr hp

theorem interpreted_claim_sound {Atom World : Type} {T : Theory Atom}
    (meaning : World → Atom → Prop) (admitted : World → Prop)
    (rules_sound : ∀ w, admitted w → Models T (meaning w))
    {a : Atom} (d : Derivable T a) : ∀ w, admitted w → meaning w a := by
  intro w hw
  exact derivation_sound d (rules_sound w hw)

theorem derivation_substitution {Atom Target : Type} {T : Theory Atom}
    {U : Theory Target} (encode : Atom → Target)
    (facts : ∀ a, T.fact a → Derivable U (encode a))
    (rules : ∀ r, T.rule r →
      (∀ a, a ∈ r.premises → Derivable U (encode a)) →
        Derivable U (encode r.conclusion))
    {a : Atom} (d : Derivable T a) : Derivable U (encode a) :=
  derivation_sound d ⟨facts, rules⟩

theorem theory_weakening {Atom : Type} {T U : Theory Atom}
    (facts : ∀ a, T.fact a → U.fact a)
    (rules : ∀ r, T.rule r → U.rule r)
    {a : Atom} (d : Derivable T a) : Derivable U a := by
  apply derivation_substitution id (fun a h => Derivable.fact a (facts a h)) _ d
  intro r h hp
  exact Derivable.fire r (rules r h) hp

theorem report_collision {World Report Answer : Type}
    (E : World → Report) (q : World → Answer) {w w' : World}
    (same : E w = E w') (different : q w ≠ q w') :
    ¬∃ decode : Report → Answer, ∀ x, decode (E x) = q x := by
  rintro ⟨decode, correct⟩
  apply different
  calc
    q w = decode (E w) := (correct w).symm
    _ = decode (E w') := congrArg decode same
    _ = q w' := correct w'

theorem processing_preserves_collision {World Report Result : Type}
    (E : World → Report) (compute : Report → Result) {w w' : World}
    (same : E w = E w') : compute (E w) = compute (E w') :=
  congrArg compute same

def run {State Action : Type} (step : State → Action → State) :
    State → List Action → State
  | s, [] => s
  | s, a :: rest => run step (step s a) rest

def Indistinguishable {State Action Report : Type}
    (step : State → Action → State) (observe : State → Report) (s t : State) : Prop :=
  ∀ actions, observe (run step s actions) = observe (run step t actions)

theorem history_collision {State Action Report Answer : Type}
    (step : State → Action → State) (observe : State → Report)
    (q : State → Answer) {s t : State}
    (same : Indistinguishable step observe s t) (different : q s ≠ q t) :
    ¬∃ decode : (List Action → Report) → Answer,
      ∀ x, decode (fun actions => observe (run step x actions)) = q x := by
  apply report_collision (fun x actions => observe (run step x actions)) q
  · exact funext same
  · exact different

theorem constant_question_needs_no_injective_report {World Report Answer : Type}
    (E : World → Report) (answer : Answer) :
    ∃ decode : Report → Answer, ∀ w, decode (E w) = answer :=
  ⟨fun _ => answer, fun _ => rfl⟩

end WitnessedReasoning
