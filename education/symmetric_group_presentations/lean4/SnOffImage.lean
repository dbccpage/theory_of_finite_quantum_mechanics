import SnSyntax
import SnCarrier
import SnTheorems

/-!
# S(n) Off-Image Refusal Completeness (Lean 4)

AuthorityEffect: None. GenesisEffect: None.

`SnTheorems.old_image_base` is the positive half of the retraction law:
on the image of `sectionLift n`, `retractionDownMap n` is a left inverse.
This file supplies the domain restriction that the deposit ledger row
WDP-P001-019 names as open: `retractionDownMap n` accepts nothing except
section images, so `nonDescent` means exactly "off the image".

Scope: the pinned education `SnCarrier` model (`BasePresentation`,
`sectionLift`, `retractionDownMap`) and nothing else. Nothing here concerns
carrier cardinalities, OB-1, or any S(n) tower beyond the five base shapes.

Statements:
1. `accepted_only_from_section`: an accepted outcome exhibits a base
   presentation `b` with `p = sectionLift n b` and `q = b.toPresentation`.
2. `nonDescent_iff_off_image`: refusal exactly when `p` is no section image.
3. `sectionLift_injective`: the witness `b` is unique.
4. `retraction_stage_strict`: a lift at stage `m ≠ n` is refused by `r_n`.
5. `inImage_iff`: a `Bool` image test computed from the syntax alone.

Axiom note. `SnTheorems.old_image_base` depends on `Classical.choice`
through `Nat.instLawfulBEq` (reached by `beq_self_eq_true`). This file does
not reuse it: `old_image_base'` below re-derives the same statement through
`decide_eq_true`, and every theorem here stays within `{propext}`.
-/

namespace SnOffImage

open SnPresentation
open SnCarrier

/-- `n == n` on `Nat` is `decide (n = n)`; this proof avoids `Nat.instLawfulBEq`. -/
theorem nat_beq_self (n : Nat) : (n == n) = true := decide_eq_true rfl

/-- `if` with a true condition, by cases on the decision procedure. -/
theorem ite_true_of {α : Sort u} {c : Prop} [h : Decidable c] (hc : c) (t e : α) :
    (if c then t else e) = t := by
  cases h with
  | isTrue _ => rfl
  | isFalse hn => exact absurd hc hn

/-- `if` with a false condition, by cases on the decision procedure. -/
theorem ite_false_of {α : Sort u} {c : Prop} [h : Decidable c] (hc : ¬ c) (t e : α) :
    (if c then t else e) = e := by
  cases h with
  | isTrue hp => exact absurd hp hc
  | isFalse _ => rfl

/-- The old-image law of `SnTheorems.old_image_base`, re-proved without
    `Classical.choice`. Same statement, same model. -/
theorem old_image_base' (n : Nat) (b : BasePresentation) :
    retractionDownMap n (sectionLift n b) = .accepted b.toPresentation := by
  cases b with
  | ground g =>
    dsimp only [sectionLift, retractionDownMap, BasePresentation.toPresentation]
    rw [ite_true_of (nat_beq_self n)]
  | supplied s =>
    dsimp only [sectionLift, retractionDownMap, BasePresentation.toPresentation]
    rw [ite_true_of (nat_beq_self n)]
  | relation r =>
    cases r <;>
      (dsimp only [sectionLift, retractionDownMap, BasePresentation.toPresentation];
       rw [ite_true_of (nat_beq_self n)])

/-- Main theorem (off-image refusal completeness). Every accepted outcome of
    the retraction down-map comes from a section image, and the accepted
    payload is that base presentation read back as a presentation. -/
theorem accepted_only_from_section (n : Nat) (p : SnPresentation) (q : SnPresentation)
    (h : retractionDownMap n p = .accepted q) :
    ∃ b : BasePresentation, p = sectionLift n b ∧ q = b.toPresentation := by
  cases p with
  | ground g => cases h
  | supplied s => cases h
  | relation r => cases h
  | retraction r => cases h
  | nonDescent nd => cases h
  | lift l =>
    obtain ⟨s, body⟩ := l
    cases Nat.decEq s n with
    | isFalse hs =>
      dsimp only [retractionDownMap] at h
      rw [ite_false_of (fun hb => hs (eq_of_beq hb))] at h
      cases h
    | isTrue hs =>
      subst hs
      cases body with
      | arrow src tgt =>
        dsimp only [retractionDownMap] at h
        rw [ite_true_of (nat_beq_self s)] at h
        exact ⟨.relation (.cut ⟨src, tgt⟩), rfl, by cases h; rfl⟩
      | pair v0 v1 =>
        dsimp only [retractionDownMap] at h
        rw [ite_true_of (nat_beq_self s)] at h
        exact ⟨.relation (.simplex ⟨v0, v1⟩), rfl, by cases h; rfl⟩
      | glyphs gs =>
        cases gs with
        | nil =>
          dsimp only [retractionDownMap] at h
          rw [ite_true_of (nat_beq_self s)] at h
          exact ⟨.ground ⟨()⟩, rfl, by cases h; rfl⟩
        | cons a t =>
          cases t with
          | nil =>
            dsimp only [retractionDownMap] at h
            rw [ite_true_of (nat_beq_self s)] at h
            exact ⟨.supplied ⟨a⟩, rfl, by cases h; rfl⟩
          | cons b t' =>
            cases t' with
            | nil =>
              dsimp only [retractionDownMap] at h
              rw [ite_true_of (nat_beq_self s)] at h
              exact ⟨.relation (.pair ⟨a, b⟩), rfl, by cases h; rfl⟩
            | cons c t'' =>
              dsimp only [retractionDownMap] at h
              rw [ite_true_of (nat_beq_self s)] at h
              cases h

/-- Corollary 1: the retraction refuses exactly the presentations that are
    not section images at that stage. -/
theorem nonDescent_iff_off_image (n : Nat) (p : SnPresentation) :
    retractionDownMap n p = .nonDescent ↔ ∀ b : BasePresentation, p ≠ sectionLift n b := by
  constructor
  · intro h b hp
    subst hp
    rw [old_image_base'] at h
    cases h
  · intro h
    cases hr : retractionDownMap n p with
    | accepted q =>
      obtain ⟨b, hb, _⟩ := accepted_only_from_section n p q hr
      exact absurd hb (h b)
    | nonDescent => rfl

/-- Reading a base presentation back as a presentation is injective. -/
theorem toPresentation_injective {b b' : BasePresentation}
    (h : b.toPresentation = b'.toPresentation) : b = b' := by
  cases b <;> cases b' <;> cases h <;> rfl

/-- Corollary 2: the section is injective, so the witness of
    `accepted_only_from_section` is unique. The proof is the left-inverse
    argument through `old_image_base'`; the `ground` case rests on
    `GroundToken` having a single value, which `old_image_base'` uses when it
    reads `.ground ⟨()⟩` back as `.ground g`. -/
theorem sectionLift_injective (n : Nat) (b b' : BasePresentation)
    (h : sectionLift n b = sectionLift n b') : b = b' := by
  have h1 := old_image_base' n b
  have h2 := old_image_base' n b'
  rw [h] at h1
  rw [h1] at h2
  injection h2 with h3
  exact toPresentation_injective h3

/-- The stage index carried by a lift, or `none` for any other presentation. -/
def liftStage : SnPresentation → Option Nat
  | .lift l => some l.stage
  | _ => none

theorem liftStage_sectionLift (m : Nat) (b : BasePresentation) :
    liftStage (sectionLift m b) = some m := by
  cases b with
  | ground g => rfl
  | supplied s => rfl
  | relation r => cases r <;> rfl

/-- Corollary 3: the stage test is exact. A section image at stage `m` is
    refused by the retraction at any other stage `n`. -/
theorem retraction_stage_strict (n m : Nat) (b : BasePresentation) (hm : m ≠ n) :
    retractionDownMap n (sectionLift m b) = .nonDescent := by
  apply (nonDescent_iff_off_image n (sectionLift m b)).mpr
  intro b' hb
  apply hm
  have hst := congrArg liftStage hb
  rw [liftStage_sectionLift, liftStage_sectionLift] at hst
  injection hst

/-- Corollary 4: a decidable image test. It is computed from the syntax alone:
    `retractionDownMap` inspects only the constructor, the stage index and the
    body of its argument, and `inImage` reads off which outcome it produced. -/
def inImage (n : Nat) (p : SnPresentation) : Bool :=
  match retractionDownMap n p with
  | .accepted _ => true
  | .nonDescent => false

theorem inImage_iff (n : Nat) (p : SnPresentation) :
    inImage n p = true ↔ ∃ b : BasePresentation, p = sectionLift n b := by
  constructor
  · intro h
    unfold inImage at h
    cases hr : retractionDownMap n p with
    | accepted q =>
      obtain ⟨b, hb, _⟩ := accepted_only_from_section n p q hr
      exact ⟨b, hb⟩
    | nonDescent =>
      rw [hr] at h
      cases h
  · intro ⟨b, hb⟩
    subst hb
    unfold inImage
    rw [old_image_base']

/-- Instance checks: refusals (three-glyph body, wrong stage, non-lift
    presentations) and the five accepted shapes round-tripping. -/
example : retractionDownMap 2 (.lift ⟨2, .glyphs [.latin 0, .latin 1, .latin 2]⟩) = .nonDescent := by
  decide
example : inImage 2 (.lift ⟨2, .glyphs [.latin 0, .latin 1, .latin 2]⟩) = false := by
  decide
example : retractionDownMap 2 (.lift ⟨3, .glyphs [.latin 0]⟩) = .nonDescent := by
  decide
example : inImage 2 (.lift ⟨3, .glyphs [.latin 0]⟩) = false := by
  decide
example : retractionDownMap 2 (.supplied ⟨.latin 0⟩) = .nonDescent := by
  decide
example : retractionDownMap 2 (.retraction ⟨2, .glyphs []⟩) = .nonDescent := by
  decide
example : retractionDownMap 2 (.nonDescent ⟨()⟩) = .nonDescent := by
  decide
example : retractionDownMap 0 (sectionLift 0 (.ground ⟨()⟩)) = .accepted (.ground ⟨()⟩) := by
  decide
example : retractionDownMap 1 (sectionLift 1 (.supplied ⟨.latin 0⟩)) =
    .accepted (.supplied ⟨.latin 0⟩) := by
  decide
example : retractionDownMap 2 (sectionLift 2 (.relation (.pair ⟨.latin 0, .latin 1⟩))) =
    .accepted (.relation (.pair ⟨.latin 0, .latin 1⟩)) := by
  decide
example : retractionDownMap 3 (sectionLift 3 (.relation (.cut ⟨.latin 0, .latin 1⟩))) =
    .accepted (.relation (.cut ⟨.latin 0, .latin 1⟩)) := by
  decide
example : retractionDownMap 3 (sectionLift 3 (.relation (.simplex ⟨.latin 0, .digit 1⟩))) =
    .accepted (.relation (.simplex ⟨.latin 0, .digit 1⟩)) := by
  decide
example : inImage 3 (sectionLift 3 (.relation (.simplex ⟨.latin 0, .digit 1⟩))) = true := by
  decide

end SnOffImage

#print axioms SnOffImage.old_image_base'
#print axioms SnOffImage.accepted_only_from_section
#print axioms SnOffImage.nonDescent_iff_off_image
#print axioms SnOffImage.sectionLift_injective
#print axioms SnOffImage.retraction_stage_strict
#print axioms SnOffImage.inImage_iff
