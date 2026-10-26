import FreeGroup

/-! Reduced signed words classify the group-term quotient in `FreeGroup`.
The proof uses the action of generators on reduced words by cancellation.
This is an algebraic normal-form theorem; no topological comparison is used. -/
namespace PreMssn.FreeWord
open FreeGroup
universe u

theorem inv_mul {G : Type u} [Group G] (a : G) : inv a*a = 1 := Group.inverse_mul a
theorem mul_inv {G : Type u} [Group G] (a : G) : a*inv a = 1 := Group.mul_inverse a

theorem left_cancel {G : Type u} [Group G] (a b c : G) (h : a*b = a*c) : b=c := by
  have k := congrArg (fun x => inv a * x) h
  rw [← Group.mul_assoc, ← Group.mul_assoc, inv_mul,
    Group.one_mul, Group.one_mul] at k
  exact k

theorem inv_inv {G : Type u} [Group G] (a : G) : inv (inv a) = a := by
  apply left_cancel (inv a)
  rw [mul_inv, inv_mul]

theorem solve_left {G : Type u} [Group G] (a b c : G) (h : b = a*c) :
    c = inv a*b := by
  rw [h, ← Group.mul_assoc, inv_mul, Group.one_mul]

abbrev Letter (A : Type u) := A × Bool

def flip {A : Type u} (a : Letter A) : Letter A := (a.1, !a.2)

@[simp] theorem flip_flip {A : Type u} (a : Letter A) : flip (flip a) = a := by
  rcases a with ⟨a, b⟩
  cases b <;> rfl

theorem flip_ne_self {A : Type u} (a : Letter A) : flip a ≠ a := by
  rcases a with ⟨a, b⟩
  cases b <;> simp [flip]

inductive Reduced {A : Type u} : List (Letter A) → Prop where
  | nil : Reduced []
  | cons {a l} : Reduced l → (∀ b t, l = b::t → a ≠ flip b) → Reduced (a::l)

theorem reduced_tail {A : Type u} {a : Letter A} {l} (h : Reduced (a::l)) : Reduced l := by
  cases h with | cons ht _ => exact ht

def push {A : Type u} [DecidableEq A] (a : Letter A) : List (Letter A) → List (Letter A)
  | [] => [a]
  | b::l => if a = flip b then l else a::b::l

theorem push_reduced {A : Type u} [DecidableEq A] (a : Letter A) {l}
    (h : Reduced l) : Reduced (push a l) := by
  cases l with
  | nil => exact Reduced.cons Reduced.nil (by intros; contradiction)
  | cons b l =>
    simp only [push]
    split
    · exact reduced_tail h
    · apply Reduced.cons h
      intro c t he
      cases he
      assumption

theorem push_flip {A : Type u} [DecidableEq A] (a : Letter A) {l}
    (h : Reduced l) : push (flip a) (push a l) = l := by
  cases l with
  | nil => simp [push]
  | cons b l =>
    by_cases hab : a = flip b
    · have ha : flip a = b := by rw [hab, flip_flip]
      simp only [push, if_pos hab]
      cases l with
      | nil => simp [ha]
      | cons c t =>
        have hn : b ≠ flip c := by cases h with | cons _ hn => exact hn c t rfl
        simp [ha, hn]
    · simp [push, hab]

abbrev ReducedWord (A : Type u) := {l : List (Letter A) // Reduced l}

def pushWord {A : Type u} [DecidableEq A] (a : Letter A) (w : ReducedWord A) :
    ReducedWord A := ⟨push a w.val, push_reduced a w.property⟩

def letterPermutation {A : Type u} [DecidableEq A] (a : Letter A) : Perm (ReducedWord A) where
  forward := pushWord a
  backward := pushWord (flip a)
  left_inverse w := Subtype.ext (push_flip a w.property)
  right_inverse w := Subtype.ext (by
    change push a (push (flip a) w.val) = w.val
    have h := push_flip (flip a) w.property
    simpa only [flip_flip] using h)

def generatorAction {A : Type u} [DecidableEq A] (a : A) : Perm (ReducedWord A) :=
  letterPermutation (a, false)

def action {A : Type u} [DecidableEq A] : Hom (Free A) (Perm (ReducedWord A)) :=
  extend generatorAction

def letterValue {A : Type u} (a : Letter A) : Free A :=
  if a.2 then inv (gen a.1) else gen a.1

theorem flip_value {A : Type u} (a : Letter A) : letterValue (flip a) = inv (letterValue a) := by
  rcases a with ⟨a,b⟩
  cases b <;> simp [letterValue, flip, inv_inv]

def value {A : Type u} : List (Letter A) → Free A
  | [] => 1
  | a::l => letterValue a * value l

theorem push_value {A : Type u} [DecidableEq A] (a : Letter A) (l : List (Letter A)) :
    value (push a l) = letterValue a * value l := by
  cases l with
  | nil => rfl
  | cons b l =>
    simp only [push]
    split
    · rename_i h
      rw [h, flip_value, value, ← Group.mul_assoc, inv_mul, Group.one_mul]
    · rfl

theorem letter_action {A : Type u} [DecidableEq A] (a : Letter A) (w : ReducedWord A) :
    (action (letterValue a)).forward w = pushWord a w := by
  rcases a with ⟨a,b⟩
  cases b <;> rfl

theorem action_value {A : Type u} [DecidableEq A] (q : Free A) (w : ReducedWord A) :
    value ((action q).forward w).val = q * value w.val := by
  induction q using Quotient.inductionOn with
  | _ e =>
    induction e generalizing w with
    | one => exact (Group.one_mul (value w.val)).symm
    | gen a => exact push_value (a,false) w.val
    | mul e f ihe ihf =>
      change ∀ w : ReducedWord A,
        value ((action (ofExpr e)).forward w).val = ofExpr e * value w.val at ihe
      change ∀ w : ReducedWord A,
        value ((action (ofExpr f)).forward w).val = ofExpr f * value w.val at ihf
      change value ((action (ofExpr e * ofExpr f)).forward w).val =
        (ofExpr e * ofExpr f) * value w.val
      rw [action.map_mul]
      change value ((action (ofExpr e)).forward ((action (ofExpr f)).forward w)).val = _
      rw [ihe, ihf, Group.mul_assoc]
    | inv e ih =>
      change ∀ w : ReducedWord A,
        value ((action (ofExpr e)).forward w).val = ofExpr e * value w.val at ih
      change value ((action (inv (ofExpr e))).forward w).val = inv (ofExpr e) * value w.val
      rw [action.map_inv]
      have h := ih ((action (ofExpr e)).backward w)
      rw [(action (ofExpr e)).right_inverse] at h
      exact solve_left (ofExpr e) (value w.val)
        (value ((action (ofExpr e)).backward w).val) h

def emptyWord (A : Type u) : ReducedWord A := ⟨[], Reduced.nil⟩

def normalForm {A : Type u} [DecidableEq A] (q : Free A) : ReducedWord A :=
  (action q).forward (emptyWord A)

theorem normal_form_value {A : Type u} [DecidableEq A] (q : Free A) :
    value (normalForm q).val = q := by
  have h := action_value q (emptyWord A)
  exact h.trans (Group.mul_one q)

theorem reduced_value_normal_form {A : Type u} [DecidableEq A] (w : ReducedWord A) :
    normalForm (value w.val) = w := by
  rcases w with ⟨l,h⟩
  induction l with
  | nil => rfl
  | cons a l ih =>
    change (action (letterValue a * value l)).forward (emptyWord A) = ⟨a::l,h⟩
    rw [action.map_mul]
    change (action (letterValue a)).forward (normalForm (value l)) = _
    rw [ih (reduced_tail h), letter_action]
    apply Subtype.ext
    cases l with
    | nil => rfl
    | cons b t =>
      have hn : a ≠ flip b := by cases h with | cons _ hn => exact hn b t rfl
      exact if_neg hn

/-- Equality in the actual group-term quotient is exactly equality of the
computable reduced representatives. -/
theorem equality_iff_normal_form {A : Type u} [DecidableEq A] (p q : Free A) :
    p = q ↔ normalForm p = normalForm q := by
  constructor
  · exact congrArg normalForm
  · intro h
    have k := congrArg (fun w : ReducedWord A => value w.val) h
    simpa only [normal_form_value] using k

def reduce {A : Type u} [DecidableEq A] : List (Letter A) → List (Letter A)
  | [] => []
  | a::l => push a (reduce l)

theorem reduce_correct {A : Type u} [DecidableEq A] (l : List (Letter A)) :
    reduce l = (normalForm (value l)).val := by
  induction l with
  | nil => rfl
  | cons a l ih =>
    change push a (reduce l) = ((action (letterValue a * value l)).forward (emptyWord A)).val
    rw [action.map_mul]
    change push a (reduce l) = ((action (letterValue a)).forward (normalForm (value l))).val
    rw [letter_action]
    exact congrArg (push a) ih

theorem word_equality_iff_reduction {A : Type u} [DecidableEq A] (l m : List (Letter A)) :
    value l = value m ↔ reduce l = reduce m := by
  rw [equality_iff_normal_form, reduce_correct, reduce_correct]
  exact ⟨congrArg Subtype.val, Subtype.ext⟩

theorem reduce_idempotent {A : Type u} [DecidableEq A] (l : List (Letter A)) :
    reduce (reduce l) = reduce l := by
  rw [reduce_correct l, reduce_correct, normal_form_value]

end PreMssn.FreeWord
