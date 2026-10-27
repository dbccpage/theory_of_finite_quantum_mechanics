import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Sum
import Mathlib.Data.Fintype.Pi
import Mathlib.SetTheory.Cardinal.Finite
import Mathlib.Logic.Function.Iterate
import OldImageInjective
import Imported.OeSn.SnOffImage

/-!
# S(n) Protected Answer Transport and Commuting Transition Squares (`PGW-SN-PROTECTED-ANSWER-TRANSPORT`, `TFQ-0519`)

AuthorityEffect: None. GenesisEffect: None.

Formalizes the mathematical characterizations and explicit counterexamples for
`PGW-SN-PROTECTED-ANSWER-TRANSPORT` (`TFQ-0519`):

1. **Retraction-induced answer transport**:
   - Given a lift `u : A → B` and a typed recovery `r : B → A ⊕ E` obeying `OldImageLaw u r`
     (`∀ a, r (u a) = Sum.inl a`), any protected answer `F : A → Q` and off-image fallback
     `d : E → Q` yield a canonical target counterpart `retractionTransport r F d : B → Q`
     satisfying `AnswerTransport u F (retractionTransport r F d)` (`retraction_transport_law`).
   - Without choosing a fallback `d`, `typedRetractionTransport r F : B → Q ⊕ E` transports
     every old answer to `Sum.inl (F a)` on `im(u)` and preserves typed refusal `Sum.inr e`
     off `im(u)` (`typed_retraction_transport_law`, `typed_retraction_transport_refuses`).
2. **Image uniqueness and off-image non-uniqueness**:
   - Any two target counterparts `F₁', F₂' : B → Q` satisfying `AnswerTransport u F Fᵢ'`
     agree on `Set.range u` (`transport_unique_on_image`).
   - Whenever `b₀ ∉ Set.range u` and `q₀ ≠ q₁ : Q`, there exist two distinct target
     counterparts `F₀', F₁' : B → Q` both satisfying `AnswerTransport u F Fᵢ'` while
     `F₀' b₀ = q₀` and `F₁' b₀ = q₁` (`transport_off_image_underdetermined`).
   - On finite types with injective `u`, the number of target counterparts `F' : B → Q`
     satisfying `AnswerTransport u F F'` is `|Q| ^ (|B| - |A|)` (`transport_counterpart_card`).
3. **Commuting transition squares and multi-step preservation**:
   - `TransitionSquare u T T'` (`∀ a, T' (u a) = u (T a)`) implies `k`-step iterated
     commutation `TransitionSquare u (T^[k]) (T'^[k])` (`commuting_square_iterated`) and
     multi-step answer preservation `F' ((T'^[k]) (u a)) = F ((T^[k]) a)` for every
     transported answer `F'` (`commuting_square_preserves_transported_answer`).
   - Under `OldImageLaw u r`, any source transition `T : A → A` and off-image fallback
     `b_ref : B` induce a canonical target transition `canonicalTransitionLift u r T b_ref`
     satisfying `TransitionSquare u T (canonicalTransitionLift u r T b_ref)`
     (`canonical_transition_lift_commutes`).
   - Conversely, when `T' (u a)` lies in `Set.range u` and `OldImageLaw u r` holds, universal
     one-step preservation of Boolean answers via `retractionTransport` is equivalent to the
     commuting square equation `T' (u a) = u (T a)` at `a`
     (`commuting_square_iff_boolean_answers_preserved_on_image`).
   - `OldImageLaw u r` and `AnswerTransport u F F'` alone do not force `TransitionSquare u T T'`
     or one-step preservation `F' (T' (u a)) = F (T a)` for an arbitrary target transition `T'`
     (`transition_square_not_implied_general`).
4. **Concrete `SnCarrier` and `S6Descent` instantiations**:
   - In the pinned `SnCarrier` model (`BasePresentation`, `sectionLift`, `retractionDownMap`),
     `snRetract n : SnPresentation → BasePresentation ⊕ Unit` satisfies `OldImageLaw (sectionLift n) (snRetract n)`
     at every stage `n` (`snRetract_old_image_law`), providing canonical answer transport and
     canonical commuting transition lifts (`snCarrier_answer_transport`,
     `snCarrier_canonical_transition_square`), while the off-image presentation
     `.lift ⟨6, .glyphs [.latin 0, .latin 1, .latin 2]⟩` witnesses off-image non-uniqueness
     and transition failure without a commuting square (`snCarrier_off_image_underdetermined`,
     `snCarrier_transition_counterexample`).
   - In the integer `S6Descent` model `s6Lift x = (x, 0)` and `s6Retract (x, y)`,
     `OldImageLaw s6Lift s6Retract` holds (`s6Descent_old_image_law`), providing canonical
     answer transport and canonical transition squares (`s6Descent_answer_transport`,
     `s6Descent_canonical_transition_square`), while the vertical-shift transition
     `T' (x, y) = (x + 1, 1)` violates the commuting square and corrupts transported answers
     (`s6Descent_transition_counterexample`).
5. **Non-implication fences**:
   - Old-image recovery does not yield a conservative extension of universal target predicates
     off `im(u)` (`not_conservative_extension_off_image`).
   - Old-image recovery does not make `u` and a collapsed retraction a two-sided inverse when
     off-image points exist (`old_image_not_right_inverse`), nor does it induce a monotone
     Galois adjunction on a 2-into-3 finite preorder witness (`old_image_not_monotone_adjunction`).
   - Transporting an unresolved demand predicate `D : A → Prop` across `u` leaves `D' (u a₀)`
     unresolved (`unrelated_demand_not_resolved_by_lift`), and `activeObstructions 6 = 1` in
     `SnCarrier` records the stage-6 obligation table value (`snCarrier_s6_demand_active`).
-/

namespace ProtectedAnswerTransport

open OldImageInjective
open SnPresentation
open SnCarrier
open SnOffImage

/-! ## Section 1: Protected Answer Transport and Off-Image Freedom -/

/-- Target counterpart `F' : B → Q` transports a protected answer `F : A → Q` across `u : A → B`
when `F' (u a) = F a` for all `a : A`. -/
def AnswerTransport {A B Q : Type} (u : A → B) (F : A → Q) (F' : B → Q) : Prop :=
  ∀ a : A, F' (u a) = F a

/-- Canonical target counterpart constructed from a typed recovery `r : B → A ⊕ E`,
a protected answer `F : A → Q`, and an off-image fallback `d : E → Q`. -/
def retractionTransport {A B E Q : Type} (r : B → A ⊕ E) (F : A → Q) (d : E → Q) : B → Q :=
  fun b => Sum.elim F d (r b)

/-- Typed target counterpart `B → Q ⊕ E` that requires no fallback on `E`, returning
`Sum.inl (F a)` on accepted preimages and `Sum.inr e` on refused elements. -/
def typedRetractionTransport {A B E Q : Type} (r : B → A ⊕ E) (F : A → Q) : B → Q ⊕ E :=
  fun b => Sum.map F id (r b)

/-- Under `OldImageLaw u r`, `retractionTransport r F d` satisfies `AnswerTransport u F`
for every protected answer `F` and every off-image fallback `d`. -/
theorem retraction_transport_law {A B E Q : Type} (u : A → B) (r : B → A ⊕ E)
    (hr : OldImageLaw u r) (F : A → Q) (d : E → Q) :
    AnswerTransport u F (retractionTransport r F d) := by
  intro a
  unfold retractionTransport
  rw [hr a]
  rfl

/-- Under `OldImageLaw u r`, `typedRetractionTransport r F` transports `u a` to `Sum.inl (F a)`. -/
theorem typed_retraction_transport_law {A B E Q : Type} (u : A → B) (r : B → A ⊕ E)
    (hr : OldImageLaw u r) (F : A → Q) (a : A) :
    typedRetractionTransport r F (u a) = Sum.inl (F a) := by
  unfold typedRetractionTransport
  rw [hr a]
  rfl

/-- Whenever `r b = Sum.inr e`, `typedRetractionTransport r F b` preserves the refusal tag `e`. -/
theorem typed_retraction_transport_refuses {A B E Q : Type} (r : B → A ⊕ E) (F : A → Q)
    (b : B) (e : E) (hb : r b = Sum.inr e) :
    typedRetractionTransport r F b = Sum.inr e := by
  unfold typedRetractionTransport
  rw [hb]
  rfl

/-- Any two target counterparts `F₁', F₂' : B → Q` that transport the same protected answer `F`
across `u` agree at every point of `Set.range u`. -/
theorem transport_unique_on_image {A B Q : Type} (u : A → B) (F : A → Q) (F₁' F₂' : B → Q)
    (h₁ : AnswerTransport u F F₁') (h₂ : AnswerTransport u F F₂')
    (b : B) (hb : b ∈ Set.range u) :
    F₁' b = F₂' b := by
  rcases hb with ⟨a, rfl⟩
  rw [h₁ a, h₂ a]

/-- Off the lifted image, `AnswerTransport u F` leaves `F'` unconstrained: for any injective lift
`u : A → B` with an off-image point `b₀` (`∀ a, u a ≠ b₀`) and any two distinct values `q₀ ≠ q₁ : Q`,
there exist two distinct target counterparts `F₀', F₁' : B → Q` that both transport `F` while
taking values `q₀` and `q₁` at `b₀`. -/
theorem transport_off_image_underdetermined {A B Q : Type} (u : A → B) (hu : Function.Injective u)
    (F : A → Q) (b₀ : B) (hb₀ : ∀ a, u a ≠ b₀) (q₀ q₁ : Q) (hq : q₀ ≠ q₁) :
    ∃ F₀' F₁' : B → Q,
      AnswerTransport u F F₀' ∧ AnswerTransport u F F₁' ∧
        F₀' b₀ = q₀ ∧ F₁' b₀ = q₁ ∧ F₀' ≠ F₁' := by
  obtain ⟨r, hr, hrb₀⟩ := law_freedom_off_image (E := Unit) u hu (Sum.inr ())
  let F₀' := retractionTransport r F (fun _ => q₀)
  let F₁' := retractionTransport r F (fun _ => q₁)
  refine ⟨F₀', F₁', retraction_transport_law u r hr F _, retraction_transport_law u r hr F _,
    ?_, ?_, ?_⟩
  · show Sum.elim F (fun _ => q₀) (r b₀) = q₀
    rw [hrb₀ b₀ hb₀]
    rfl
  · show Sum.elim F (fun _ => q₁) (r b₀) = q₁
    rw [hrb₀ b₀ hb₀]
    rfl
  · intro heq
    have hval := congrFun heq b₀
    change Sum.elim F (fun _ => q₀) (r b₀) = Sum.elim F (fun _ => q₁) (r b₀) at hval
    rw [hrb₀ b₀ hb₀] at hval
    exact hq hval

/-- On finite types, for an injective lift `u : A → B` and a protected answer `F : A → Q`,
the number of target counterparts `F' : B → Q` satisfying `AnswerTransport u F F'` is
`|Q| ^ (|B| - |A|)`. -/
theorem transport_counterpart_card {A B Q : Type} [Fintype A] [Fintype B] [Fintype Q]
    (u : A → B) (hu : Function.Injective u) (F : A → Q) :
    Nat.card {F' : B → Q // AnswerTransport u F F'} =
      (Fintype.card Q) ^ (Fintype.card B - Fintype.card A) := by
  classical
  let φ : Set.range u → A := (Equiv.ofInjective u hu).symm
  have hφ : ∀ a (h : u a ∈ Set.range u), φ ⟨u a, h⟩ = a := fun a h =>
    (Equiv.symm_apply_eq _).mpr rfl
  let e : {F' : B → Q // AnswerTransport u F F'} ≃ ({b : B // b ∉ Set.range u} → Q) :=
    { toFun := fun F' s => F'.1 s.1
      invFun := fun g => ⟨fun b => if h : b ∈ Set.range u then F (φ ⟨b, h⟩) else g ⟨b, h⟩, by
        intro a
        have h : u a ∈ Set.range u := ⟨a, rfl⟩
        simp only [h, ↓reduceDIte, hφ]⟩
      left_inv := by
        rintro ⟨F', hF'⟩
        apply Subtype.ext
        funext b
        by_cases h : b ∈ Set.range u
        · rcases h with ⟨a, rfl⟩
          have h2 : u a ∈ Set.range u := ⟨a, rfl⟩
          simp only [h2, ↓reduceDIte, hφ]
          exact (hF' a).symm
        · simp only [h, ↓reduceDIte]
      right_inv := by
        intro g
        funext s
        simp only [s.2, ↓reduceDIte] }
  rw [Nat.card_congr e]
  have hS : Fintype.card {b : B // b ∉ Set.range u} = Fintype.card B - Fintype.card A := by
    have h1 := Fintype.card_subtype_compl (fun b : B => b ∈ Set.range u)
    have h2 : Fintype.card {b : B // b ∈ Set.range u} = Fintype.card A :=
      (Fintype.card_congr (Equiv.ofInjective u hu)).symm
    rw [h2] at h1
    convert h1
  rw [Nat.card_eq_fintype_card, Fintype.card_fun, hS]

/-! ## Section 2: Commuting Transition Squares and Multi-Step Preservation -/

/-- A target operation `T' : B → B` forms a commuting transition square with a source operation
`T : A → A` across `u : A → B` when `T' (u a) = u (T a)` for all `a : A`. -/
def TransitionSquare {A B : Type} (u : A → B) (T : A → A) (T' : B → B) : Prop :=
  ∀ a : A, T' (u a) = u (T a)

/-- If `(T, T')` forms a commuting square across `u`, then for every step count `k : Nat`,
the `k`-fold iterates `(T^[k], T'^[k])` also form a commuting square across `u`. -/
theorem commuting_square_iterated {A B : Type} (u : A → B) (T : A → A) (T' : B → B)
    (hT : TransitionSquare u T T') (k : Nat) :
    TransitionSquare u (T^[k]) (T'^[k]) := by
  induction k with
  | zero =>
    intro a
    rfl
  | succ k ih =>
    intro a
    rw [Function.iterate_succ_apply', Function.iterate_succ_apply', ih a, hT (T^[k] a)]

/-- If `F'` transports `F` across `u` and `(T, T')` forms a commuting transition square across `u`,
then `F'` preserves `F` along every `k`-step trajectory starting on the lifted image. -/
theorem commuting_square_preserves_transported_answer {A B Q : Type}
    (u : A → B) (F : A → Q) (F' : B → Q) (T : A → A) (T' : B → B)
    (hF : AnswerTransport u F F') (hT : TransitionSquare u T T')
    (k : Nat) (a : A) :
    F' ((T'^[k]) (u a)) = F ((T^[k]) a) := by
  rw [commuting_square_iterated u T T' hT k a, hF ((T^[k]) a)]

/-- Canonical target transition induced by a source transition `T : A → A`, a typed recovery
`r : B → A ⊕ E`, and an off-image fallback state `b_ref : B`. -/
def canonicalTransitionLift {A B E : Type} (u : A → B) (r : B → A ⊕ E)
    (T : A → A) (b_ref : B) : B → B :=
  fun b =>
    match r b with
    | Sum.inl a => u (T a)
    | Sum.inr _ => b_ref

/-- Under `OldImageLaw u r`, `canonicalTransitionLift u r T b_ref` satisfies the commuting
transition square for every `T : A → A` and every fallback `b_ref : B`. -/
theorem canonical_transition_lift_commutes {A B E : Type} (u : A → B) (r : B → A ⊕ E)
    (hr : OldImageLaw u r) (T : A → A) (b_ref : B) :
    TransitionSquare u T (canonicalTransitionLift u r T b_ref) := by
  intro a
  unfold canonicalTransitionLift
  rw [hr a]

/-- Pointwise characterization on the lifted image: if `OldImageLaw u r` holds and `T' (u a)` lies
in `Set.range u`, then `T' (u a) = u (T a)` if and only if every Boolean protected answer
`F : A → Bool` is preserved after one step under `retractionTransport`. -/
theorem commuting_square_iff_boolean_answers_preserved_on_image {A B E : Type} [DecidableEq A]
    (u : A → B) (r : B → A ⊕ E) (hr : OldImageLaw u r)
    (T : A → A) (T' : B → B) (a : A) (him : T' (u a) ∈ Set.range u) :
    T' (u a) = u (T a) ↔
      ∀ (F : A → Bool) (d : E → Bool),
        retractionTransport r F d (T' (u a)) = F (T a) := by
  constructor
  · intro hsq F d
    rw [hsq, retraction_transport_law u r hr F d (T a)]
  · intro hall
    rcases him with ⟨a', ha'⟩
    have hbool := hall (fun x => decide (x = T a)) (fun _ => false)
    rw [← ha'] at hbool
    rw [retraction_transport_law u r hr (fun x => decide (x = T a)) (fun _ => false) a'] at hbool
    dsimp only at hbool
    rw [decide_eq_true rfl] at hbool
    have heq : a' = T a := of_decide_eq_true hbool
    rw [← ha', heq]

/-- `OldImageLaw u r` and `AnswerTransport u F F'` do not imply `TransitionSquare u T T'` or
one-step answer preservation: whenever `F a₁ ≠ F (T a₀)`, the constant target map
`T' := fun _ => u a₁` violates both `TransitionSquare u T T'` and `F' (T' (u a₀)) = F (T a₀)`. -/
theorem transition_square_not_implied_general {A B E Q : Type}
    (u : A → B) (r : B → A ⊕ E) (hr : OldImageLaw u r)
    (F : A → Q) (F' : B → Q) (hF : AnswerTransport u F F')
    (T : A → A) (a₀ a₁ : A) (hne : F a₁ ≠ F (T a₀)) :
    ∃ T' : B → B,
      OldImageLaw u r ∧ AnswerTransport u F F' ∧
        ¬ TransitionSquare u T T' ∧ F' (T' (u a₀)) ≠ F (T a₀) := by
  refine ⟨fun _ => u a₁, hr, hF, ?_, ?_⟩
  · intro hsq
    have hstep := hsq a₀
    have hval := congrArg F' hstep
    rw [hF a₁, hF (T a₀)] at hval
    exact hne hval
  · dsimp only
    rw [hF a₁]
    exact hne

/-! ## Section 3: Concrete `SnCarrier` Instantiation (`BasePresentation`, `sectionLift`, `retractionDownMap`) -/

/-- Partial syntax decoder inverting `BasePresentation.toPresentation` on the three base constructors. -/
def decodeBase : SnPresentation → Option BasePresentation
  | .ground g => some (.ground g)
  | .supplied s => some (.supplied s)
  | .relation r => some (.relation r)
  | _ => none

theorem decodeBase_toPresentation (b : BasePresentation) :
    decodeBase b.toPresentation = some b := by
  cases b <;> rfl

/-- Typed recovery map for `SnCarrier` at stage `n`, returning `Sum.inl b` when `retractionDownMap n`
accepts a base presentation `b` and `Sum.inr ()` when `retractionDownMap n` refuses. -/
def snRetract (n : Nat) (p : SnPresentation) : BasePresentation ⊕ Unit :=
  match retractionDownMap n p with
  | .accepted q =>
    match decodeBase q with
    | some b => Sum.inl b
    | none => Sum.inr ()
  | .nonDescent => Sum.inr ()

/-- `snRetract n` obeys `OldImageLaw` with respect to `sectionLift n` at every stage `n : Nat`. -/
theorem snRetract_old_image_law (n : Nat) :
    OldImageLaw (sectionLift n) (snRetract n) := by
  intro b
  unfold snRetract
  rw [old_image_base' n b]
  dsimp only
  rw [decodeBase_toPresentation b]

/-- `snRetract n p` returns `Sum.inr ()` if and only if `retractionDownMap n p = .nonDescent`. -/
theorem snRetract_nonDescent_iff (n : Nat) (p : SnPresentation) :
    snRetract n p = Sum.inr () ↔ retractionDownMap n p = .nonDescent := by
  unfold snRetract
  cases hr : retractionDownMap n p with
  | nonDescent =>
    dsimp only
    exact ⟨fun _ => rfl, fun _ => rfl⟩
  | accepted q =>
    obtain ⟨b, _, hq⟩ := accepted_only_from_section n p q hr
    subst hq
    dsimp only
    rw [decodeBase_toPresentation b]
    dsimp only
    constructor
    · intro h
      cases h
    · intro h
      cases h

/-- Canonical answer transport for the pinned `SnCarrier` model at any stage `n`. -/
theorem snCarrier_answer_transport {Q : Type} (n : Nat)
    (F : BasePresentation → Q) (d : Unit → Q) :
    AnswerTransport (sectionLift n) F (retractionTransport (snRetract n) F d) :=
  retraction_transport_law (sectionLift n) (snRetract n) (snRetract_old_image_law n) F d

/-- Canonical commuting transition square for the pinned `SnCarrier` model at any stage `n`. -/
theorem snCarrier_canonical_transition_square (n : Nat) (T : BasePresentation → BasePresentation) :
    TransitionSquare (sectionLift n) T
      (canonicalTransitionLift (sectionLift n) (snRetract n) T (.nonDescent ⟨()⟩)) :=
  canonical_transition_lift_commutes (sectionLift n) (snRetract n)
    (snRetract_old_image_law n) T (.nonDescent ⟨()⟩)

/-- Off-image witness in `SnPresentation` at stage 6: a 3-glyph lift body is outside the 5 base shapes. -/
def snStage6OffImageWitness : SnPresentation :=
  .lift ⟨6, .glyphs [.latin 0, .latin 1, .latin 2]⟩

theorem snStage6OffImageWitness_refused :
    retractionDownMap 6 snStage6OffImageWitness = .nonDescent := by
  decide

theorem snStage6OffImageWitness_not_in_image (b : BasePresentation) :
    sectionLift 6 b ≠ snStage6OffImageWitness := by
  intro hb
  have h := (nonDescent_iff_off_image 6 snStage6OffImageWitness).mp snStage6OffImageWitness_refused b
  exact h hb.symm

/-- At stage 6 of `SnCarrier`, every base answer `F : BasePresentation → Nat` admits two distinct
target counterparts `F₀', F₁' : SnPresentation → Nat` that both satisfy
`AnswerTransport (sectionLift 6) F` while disagreeing on `snStage6OffImageWitness`. -/
theorem snCarrier_off_image_underdetermined (F : BasePresentation → Nat) :
    ∃ F₀' F₁' : SnPresentation → Nat,
      AnswerTransport (sectionLift 6) F F₀' ∧
        AnswerTransport (sectionLift 6) F F₁' ∧
        F₀' snStage6OffImageWitness = 0 ∧
        F₁' snStage6OffImageWitness = 1 ∧
        F₀' ≠ F₁' := by
  let F₀' := retractionTransport (snRetract 6) F (fun _ => 0)
  let F₁' := retractionTransport (snRetract 6) F (fun _ => 1)
  have href : snRetract 6 snStage6OffImageWitness = Sum.inr () :=
    (snRetract_nonDescent_iff 6 snStage6OffImageWitness).mpr snStage6OffImageWitness_refused
  refine ⟨F₀', F₁', snCarrier_answer_transport 6 F _, snCarrier_answer_transport 6 F _,
    ?_, ?_, ?_⟩
  · show Sum.elim F (fun _ => 0) (snRetract 6 snStage6OffImageWitness) = 0
    rw [href]
    rfl
  · show Sum.elim F (fun _ => 1) (snRetract 6 snStage6OffImageWitness) = 1
    rw [href]
    rfl
  · intro heq
    have hval := congrFun heq snStage6OffImageWitness
    change Sum.elim F (fun _ => 0) (snRetract 6 snStage6OffImageWitness) =
      Sum.elim F (fun _ => 1) (snRetract 6 snStage6OffImageWitness) at hval
    rw [href] at hval
    cases hval

/-- Concrete stage-6 transition counterexample in `SnCarrier`: `OldImageLaw` and `AnswerTransport`
hold, yet a target transition `T'` that emits `snStage6OffImageWitness` violates the commuting
square and fails to preserve the base answer after one step. -/
theorem snCarrier_transition_counterexample :
    let F : BasePresentation → Nat := fun _ => 1
    let F' : SnPresentation → Nat := retractionTransport (snRetract 6) F (fun _ => 0)
    let T : BasePresentation → BasePresentation := id
    let T' : SnPresentation → SnPresentation := fun _ => snStage6OffImageWitness
    let b₀ : BasePresentation := .ground ⟨()⟩
    OldImageLaw (sectionLift 6) (snRetract 6) ∧
      AnswerTransport (sectionLift 6) F F' ∧
      ¬ TransitionSquare (sectionLift 6) T T' ∧
      F' (T' (sectionLift 6 b₀)) ≠ F (T b₀) := by
  intro F F' T T' b₀
  have href : snRetract 6 snStage6OffImageWitness = Sum.inr () :=
    (snRetract_nonDescent_iff 6 snStage6OffImageWitness).mpr snStage6OffImageWitness_refused
  refine ⟨snRetract_old_image_law 6, snCarrier_answer_transport 6 F _, ?_, ?_⟩
  · intro hsq
    exact snStage6OffImageWitness_not_in_image (T b₀) (hsq b₀).symm
  · change Sum.elim F (fun _ => 0) (snRetract 6 snStage6OffImageWitness) ≠ 1
    rw [href]
    decide

/-! ## Section 4: Concrete `S6Descent` Integer Slice Model (`u(x) = (x, 0)`) -/

/-- Lift map `u(x) = (x, 0)` of the `S6Descent` integer model. -/
def s6Lift (x : Int) : Int × Int := (x, 0)

/-- Typed retraction `r(x, y)` of the `S6Descent` integer model: accepts `(x, 0)` as `Sum.inl x`
and refuses `(x, y)` for `y ≠ 0` as `Sum.inr ()`. -/
def s6Retract (p : Int × Int) : Int ⊕ Unit :=
  if p.2 = 0 then Sum.inl p.1 else Sum.inr ()

/-- `s6Retract` obeys `OldImageLaw` with respect to `s6Lift`. -/
theorem s6Descent_old_image_law : OldImageLaw s6Lift s6Retract := by
  intro x
  rfl

/-- `s6Retract (x, y) = Sum.inr ()` if and only if `y ≠ 0`. -/
theorem s6Retract_refuses_iff (x y : Int) :
    s6Retract (x, y) = Sum.inr () ↔ y ≠ 0 := by
  unfold s6Retract
  by_cases hy : y = 0
  · simp only [hy, ↓reduceIte, ne_eq, not_true_eq_false, reduceCtorEq]
  · simp only [hy, ↓reduceIte, ne_eq, not_false_eq_true]

/-- Canonical answer transport for the `S6Descent` model. -/
theorem s6Descent_answer_transport {Q : Type} (F : Int → Q) (d : Unit → Q) :
    AnswerTransport s6Lift F (retractionTransport s6Retract F d) :=
  retraction_transport_law s6Lift s6Retract s6Descent_old_image_law F d

/-- Canonical commuting transition square for the `S6Descent` model: `T'(x, 0) = (T x, 0)`. -/
theorem s6Descent_canonical_transition_square (T : Int → Int) :
    TransitionSquare s6Lift T (canonicalTransitionLift s6Lift s6Retract T (0, 1)) :=
  canonical_transition_lift_commutes s6Lift s6Retract s6Descent_old_image_law T (0, 1)

/-- Concrete counterexample in `S6Descent`: the off-slice step `T'(x, y) = (x + 1, 1)` shares the
first-coordinate increment with `T(x) = x + 1`, but steps off `y = 0`, violating both
`TransitionSquare s6Lift T T'` and one-step preservation of `F(x) = x`. -/
theorem s6Descent_transition_counterexample :
    let F : Int → Int := id
    let F' : Int × Int → Int := retractionTransport s6Retract F (fun _ => -1)
    let T : Int → Int := fun x => x + 1
    let T' : Int × Int → Int × Int := fun p => (p.1 + 1, 1)
    OldImageLaw s6Lift s6Retract ∧
      AnswerTransport s6Lift F F' ∧
      ¬ TransitionSquare s6Lift T T' ∧
      F' (T' (s6Lift 0)) ≠ F (T 0) := by
  intro F F' T T'
  refine ⟨s6Descent_old_image_law, s6Descent_answer_transport F _, ?_, ?_⟩
  · intro hsq
    have h0 := congrArg Prod.snd (hsq 0)
    revert h0
    decide
  · decide

/-! ## Section 5: Non-Implication Fences (No Conservative Extension, No Adjunction, No Demand Resolution) -/

/-- **No automatic conservative extension off the image**: for any lift `u : A → B` and off-image
point `b₀` (`∀ a, u a ≠ b₀`), the image-membership predicate `P' b := ∃ a, u a = b` holds for every
lifted old element `u a`, yet fails at `b₀`. Thus universal validity on `im(u)` (`∀ a, P' (u a)`)
does not imply universal validity on `B` (`∀ b, P' b`). -/
theorem not_conservative_extension_off_image {A B : Type} (u : A → B) (b₀ : B)
    (hb₀ : ∀ a, u a ≠ b₀) :
    ∃ P' : B → Prop, (∀ a : A, P' (u a)) ∧ ¬ (∀ b : B, P' b) := by
  refine ⟨fun b => ∃ a, u a = b, fun a => ⟨a, rfl⟩, ?_⟩
  intro hall
  rcases hall b₀ with ⟨a, ha⟩
  exact hb₀ a ha

/-- **No two-sided inverse / equivalence off the image**: whenever `b₀ : B` is outside `im(u)`,
no collapse `Sum.elim id g ∘ r : B → A` of any recovery `r : B → A ⊕ E` can satisfy
`u (Sum.elim id g (r b₀)) = b₀`. -/
theorem old_image_not_right_inverse {A B E : Type} (u : A → B) (r : B → A ⊕ E)
    (g : E → A) (b₀ : B) (hb₀ : ∀ a, u a ≠ b₀) :
    u (Sum.elim id g (r b₀)) ≠ b₀ :=
  hb₀ (Sum.elim id g (r b₀))

/-- Concrete finite preorder counterexample showing that `OldImageLaw` (even for an order-embedding
lift) does not induce a Galois adjunction `u a ≤ b ↔ a ≤ p b`: on `Fin 2 → Fin 3` with
`gapLift 0 = 1`, `gapLift 1 = 2`, the off-image element `b = 0` lies below the entire lifted image,
so at `a = 0, b = 0` we have `0 ≤ p 0` for every `p : Fin 3 → Fin 2` while `gapLift 0 = 1 ≤ 0` is false. -/
def gapLift : Fin 2 → Fin 3
  | ⟨0, _⟩ => ⟨1, by decide⟩
  | ⟨1, _⟩ => ⟨2, by decide⟩

def gapRetract : Fin 3 → Fin 2 ⊕ Unit
  | ⟨0, _⟩ => Sum.inr ()
  | ⟨1, _⟩ => Sum.inl ⟨0, by decide⟩
  | ⟨2, _⟩ => Sum.inl ⟨1, by decide⟩

theorem gap_old_image_law : OldImageLaw gapLift gapRetract := by
  unfold OldImageLaw
  decide

/-- No map `p : Fin 3 → Fin 2` satisfies the Galois adjunction law
`∀ a b, gapLift a ≤ b ↔ a ≤ p b`. -/
theorem old_image_not_left_galois_adjunction :
    ¬ ∃ p : Fin 3 → Fin 2, ∀ (a : Fin 2) (b : Fin 3), gapLift a ≤ b ↔ a ≤ p b := by
  rintro ⟨p, hp⟩
  have h0 : gapLift ⟨0, by decide⟩ ≤ ⟨0, by decide⟩ ↔ (⟨0, by decide⟩ : Fin 2) ≤ p ⟨0, by decide⟩ :=
    hp ⟨0, by decide⟩ ⟨0, by decide⟩
  revert h0
  generalize p ⟨0, by decide⟩ = x
  revert x
  decide

/-- **No resolution of an unrelated demand**: if `D' : B → Prop` transports a demand predicate
`D : A → Prop` across `u` (`AnswerTransport u D D'`), then any active demand `D a₀` remains active
at `u a₀` (`D' (u a₀)`). -/
theorem unrelated_demand_not_resolved_by_lift {A B : Type} (u : A → B)
    (D : A → Prop) (D' : B → Prop) (hD : AnswerTransport u D D')
    (a₀ : A) (ha₀ : D a₀) :
    D' (u a₀) := by
  rw [hD a₀]
  exact ha₀

/-- In `SnCarrier`, `activeObstructions 6 = 1` while `retractionDownMap 6` satisfies the old-image
law on all base presentations (`old_image_base' 6`), confirming that the stage-6 table records an
active descent-checking obligation alongside exact old-image recovery. -/
theorem snCarrier_s6_demand_active :
    activeObstructions 6 = 1 ∧
      (∀ b : BasePresentation,
        retractionDownMap 6 (sectionLift 6 b) = .accepted b.toPresentation) :=
  ⟨rfl, old_image_base' 6⟩

end ProtectedAnswerTransport

#print axioms ProtectedAnswerTransport.retraction_transport_law
#print axioms ProtectedAnswerTransport.typed_retraction_transport_law
#print axioms ProtectedAnswerTransport.typed_retraction_transport_refuses
#print axioms ProtectedAnswerTransport.transport_unique_on_image
#print axioms ProtectedAnswerTransport.transport_off_image_underdetermined
#print axioms ProtectedAnswerTransport.transport_counterpart_card
#print axioms ProtectedAnswerTransport.commuting_square_iterated
#print axioms ProtectedAnswerTransport.commuting_square_preserves_transported_answer
#print axioms ProtectedAnswerTransport.canonical_transition_lift_commutes
#print axioms ProtectedAnswerTransport.commuting_square_iff_boolean_answers_preserved_on_image
#print axioms ProtectedAnswerTransport.transition_square_not_implied_general
#print axioms ProtectedAnswerTransport.snRetract_old_image_law
#print axioms ProtectedAnswerTransport.snRetract_nonDescent_iff
#print axioms ProtectedAnswerTransport.snCarrier_answer_transport
#print axioms ProtectedAnswerTransport.snCarrier_canonical_transition_square
#print axioms ProtectedAnswerTransport.snCarrier_off_image_underdetermined
#print axioms ProtectedAnswerTransport.snCarrier_transition_counterexample
#print axioms ProtectedAnswerTransport.s6Descent_old_image_law
#print axioms ProtectedAnswerTransport.s6Descent_answer_transport
#print axioms ProtectedAnswerTransport.s6Descent_canonical_transition_square
#print axioms ProtectedAnswerTransport.s6Descent_transition_counterexample
#print axioms ProtectedAnswerTransport.not_conservative_extension_off_image
#print axioms ProtectedAnswerTransport.old_image_not_right_inverse
#print axioms ProtectedAnswerTransport.old_image_not_left_galois_adjunction
#print axioms ProtectedAnswerTransport.unrelated_demand_not_resolved_by_lift
#print axioms ProtectedAnswerTransport.snCarrier_s6_demand_active
