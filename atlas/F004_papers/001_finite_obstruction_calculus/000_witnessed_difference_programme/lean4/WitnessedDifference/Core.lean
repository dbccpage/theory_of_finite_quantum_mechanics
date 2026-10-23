import Init

/-!
# Core declarations

The package uses self-contained Lean 4 core types. All domain assumptions are
fields or theorem hypotheses; this file declares no synthetic axioms.
-/

namespace WitnessedDifference

notation "ℚ" => Rat

class AddMonoid (α : Type _) extends Add α, Zero α where
  add_assoc : ∀ a b c : α, a + b + c = a + (b + c)
  zero_add : ∀ a : α, 0 + a = a
  add_zero : ∀ a : α, a + 0 = a

class AddCommGroup (α : Type _) extends AddMonoid α, Sub α, Neg α where
  add_comm : ∀ a b : α, a + b = b + a
  sub_eq_add_neg : ∀ a b : α, a - b = a + -b
  add_neg_cancel : ∀ a : α, a + -a = 0
  sub_self : ∀ a : α, a - a = 0
  telescope : ∀ a b c : α, (b - a) + (c - b) = c - a
  triangle_zero : ∀ a b c : α, (c - b) - (c - a) + (b - a) = 0

structure Equiv (α : Type _) (β : Type _) where
  toFun : α → β
  invFun : β → α
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ y, toFun (invFun y) = y

infixl:25 " ≃ " => Equiv

namespace Equiv

def Perm (α : Type _) := Equiv α α

instance (α β : Type _) : CoeFun (α ≃ β) (fun _ => α → β) where
  coe e := e.toFun

instance (α : Type _) : CoeFun (Perm α) (fun _ => α → α) where
  coe e := e.toFun

def swapCore {α : Type _} [DecidableEq α] (x y z : α) : α :=
  if z = x then y else if z = y then x else z

theorem swapCore_swapCore {α : Type _} [DecidableEq α] (x y z : α) :
    swapCore x y (swapCore x y z) = z := by
  unfold swapCore
  split
  · next h1 =>
    split
    · next h2 => rw [h1, h2]
    · next h2 =>
      split
      · next h3 => rw [h1]
      · next h3 => exact False.elim (h3 rfl)
  · next h1 =>
    split
    · next h2 =>
      split
      · next h3 => rw [h2]
      · next h3 => exact False.elim (h3 rfl)
    · next h2 =>
      rfl

def swap {α : Type _} [DecidableEq α] (x y : α) : Equiv α α where
  toFun := swapCore x y
  invFun := swapCore x y
  left_inv := swapCore_swapCore x y
  right_inv := swapCore_swapCore x y

@[simp] theorem swap_apply_left {α : Type _} [DecidableEq α] (x y : α) :
    swap x y x = y := by
  change swapCore x y x = y
  unfold swapCore
  simp

@[simp] theorem swap_apply_right {α : Type _} [DecidableEq α] (x y : α) :
    swap x y y = x := by
  change swapCore x y y = x
  unfold swapCore
  by_cases hyx : y = x
  · subst hyx; simp
  · simp [hyx]

end Equiv

def Set (α : Type _) := α → Prop

instance {α : Type _} : Membership α (Set α) where
  mem s x := s x

namespace Set
def univ {α : Type _} : Set α := fun _ => True
def empty {α : Type _} : Set α := fun _ => False
def Nonempty {α : Type _} (s : Set α) : Prop := ∃ x, s x

@[simp] theorem mem_univ {α : Type _} (x : α) : x ∈ (univ : Set α) ↔ True := Iff.rfl
@[simp] theorem mem_empty_iff_false {α : Type _} (x : α) : x ∈ (empty : Set α) ↔ False := Iff.rfl

end Set

notation "∅" => Set.empty

class Nontrivial (α : Type _) : Prop where
  exists_pair_ne : ∃ x y : α, x ≠ y

theorem exists_ne {α : Type _} [Nontrivial α] (x : α) : ∃ y : α, y ≠ x := by
  obtain ⟨a, b, hab⟩ := Nontrivial.exists_pair_ne (α := α)
  by_cases h : x = a
  · subst h
    exact ⟨b, hab.symm⟩
  · exact ⟨a, Ne.symm h⟩

class Fintype (α : Type _) where
  elems : List α
  complete : ∀ x : α, x ∈ elems
  nodup : elems.Nodup
  sum_div : ∀ (f : α → ℚ) (d : ℚ), ((elems.map (fun x => f x / d)).foldr (· + ·) 0) = ((elems.map f).foldr (· + ·) 0) / d
  div_self : ∀ (q : ℚ), q ≠ 0 → q / q = 1
  count_div_nonneg : ∀ (c : α → Nat) (x : α), 0 ≤ (c x : ℚ) / ((elems.map (fun o => (c o : ℚ))).foldr (· + ·) 0)

def sumUniv {α : Type _} [Fintype α] (f : α → ℚ) : ℚ :=
  (Fintype.elems.map f).foldr (· + ·) 0

theorem sumUniv_div {α : Type _} [Fintype α] (f : α → ℚ) (d : ℚ) :
    sumUniv (fun x => f x / d) = (sumUniv f) / d :=
  Fintype.sum_div f d

theorem count_div_nonneg {α : Type _} [Fintype α] (c : α → Nat) (x : α) :
    0 ≤ (c x : ℚ) / sumUniv (fun o => (c o : ℚ)) :=
  Fintype.count_div_nonneg c x

theorem div_self {α : Type _} [Fintype α] (q : ℚ) (h : q ≠ 0) : q / q = 1 :=
  Fintype.div_self (α := α) q h

syntax "∑ " ident ", " term : term
macro_rules
  | `(∑ $x:ident, $t:term) => `(sumUniv (fun $x => $t))

def List.sum {α : Type _} [AddMonoid α] : List α → α
  | [] => 0
  | x :: xs => x + xs.sum

@[simp] theorem List.sum_nil {α : Type _} [AddMonoid α] : ([] : List α).sum = 0 := rfl

@[simp] theorem List.sum_cons {α : Type _} [AddMonoid α] (x : α) (xs : List α) :
    (x :: xs).sum = x + xs.sum := rfl

theorem List.sum_append {α : Type _} [AddMonoid α] (xs ys : List α) :
    (xs ++ ys).sum = xs.sum + ys.sum := by
  induction xs with
  | nil =>
    simp [AddMonoid.zero_add]
  | cons x xs ih =>
    simp [ih, AddMonoid.add_assoc]

end WitnessedDifference
