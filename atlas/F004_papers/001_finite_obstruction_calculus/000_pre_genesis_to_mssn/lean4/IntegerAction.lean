import FreeAbelian

/-! Canonical integer multiples in an arbitrary additive abelian group.
This supplies the constructive coefficient operations needed for explicit
finite coordinates of the free abelian group; no scalar-action law is assumed. -/
namespace PreMssn.IntegerAction
open Lean.Grind
open AddCommMonoid AddCommGroup
open Homology
universe u v

def multiple {M : Type u} [AddCommGroup M] (k : Int) (a : M) : M :=
  match k with
  | .ofNat n => nsmulRec n a
  | .negSucc n => -(nsmulRec (n+1) a)

theorem multiple_zero {M : Type u} [AddCommGroup M] (a : M) : multiple 0 a = 0 := rfl
theorem multiple_one {M : Type u} [AddCommGroup M] (a : M) : multiple 1 a = a :=
  zero_add a

theorem multiple_succ {M : Type u} [AddCommGroup M] (k : Int) (a : M) :
    multiple (k+1) a = multiple k a + a := by
  cases k with
  | ofNat n =>
    rw [show Int.ofNat n + 1 = Int.ofNat (n+1) from rfl]
    rfl
  | negSucc n =>
    cases n with
    | zero =>
      change (0 : M) = -(0 + a) + a
      rw [zero_add, neg_add_cancel]
    | succ n =>
      rw [show Int.negSucc (n+1) + 1 = Int.negSucc n from by omega]
      change -(nsmulRec (n+1) a) = -(nsmulRec (n+1) a + a) + a
      rw [neg_add, add_assoc, neg_add_cancel, add_zero]

theorem multiple_pred {M : Type u} [AddCommGroup M] (k : Int) (a : M) :
    multiple (k-1) a = multiple k a - a := by
  apply (add_left_inj a).mp
  rw [← multiple_succ, show k-1+1 = k from by omega, sub_add_cancel]

theorem integer_induction {P : Int → Prop} (zero : P 0)
    (succ : ∀ k, P k → P (k+1)) (pred : ∀ k, P k → P (k-1)) (k : Int) : P k := by
  cases k with
  | ofNat n =>
    induction n with
    | zero => exact zero
    | succ n ih =>
      have h := succ (Int.ofNat n) ih
      exact (show Int.ofNat n + 1 = Int.ofNat (n+1) from rfl) ▸ h
  | negSucc n =>
    induction n with
    | zero => exact pred 0 zero
    | succ n ih =>
      have h := pred (Int.negSucc n) ih
      simpa only [show Int.negSucc n - 1 = Int.negSucc (n+1) from by omega] using h

theorem multiple_add {M : Type u} [AddCommGroup M] (k j : Int) (a : M) :
    multiple (k+j) a = multiple k a + multiple j a := by
  apply integer_induction (P := fun k => multiple (k+j) a = multiple k a + multiple j a)
  · rw [Int.zero_add, multiple_zero, zero_add]
  · intro k ih
    rw [show k+1+j = (k+j)+1 from by omega, multiple_succ, ih, multiple_succ]
    rw [add_assoc, add_comm (multiple j a) a, ← add_assoc]
  · intro k ih
    rw [show k-1+j = (k+j)-1 from by omega, multiple_pred, ih, multiple_pred]
    simp only [sub_eq_add_neg]
    rw [add_assoc, add_comm (multiple j a) (-a), ← add_assoc]

def fromInteger {M : Type u} [AddCommGroup M] (a : M) : AddHom Int M where
  toFun k := multiple k a
  map_zero := rfl
  map_add k j := multiple_add k j a

theorem hom_nsmul {M : Type u} {N : Type v} [AddCommGroup M] [AddCommGroup N]
    (f : AddHom M N) (n : Nat) (a : M) : f (nsmulRec n a) = nsmulRec n (f a) := by
  induction n with
  | zero => exact f.map_zero
  | succ n ih =>
    change f (nsmulRec n a + a) = nsmulRec n (f a) + f a
    rw [f.map_add, ih]

theorem hom_multiple {M : Type u} {N : Type v} [AddCommGroup M] [AddCommGroup N]
    (f : AddHom M N) (k : Int) (a : M) : f (multiple k a) = multiple k (f a) := by
  cases k with
  | ofNat n => exact hom_nsmul f n a
  | negSucc n =>
    change f (-nsmulRec (n+1) a) = -nsmulRec (n+1) (f a)
    rw [f.map_neg, hom_nsmul]

theorem nsmul_integer (n : Nat) (a : Int) : nsmulRec n a = (n : Int) * a := by
  induction n with
  | zero => simp [nsmulRec]
  | succ n ih =>
    change nsmulRec n a + a = ((n+1 : Nat) : Int) * a
    rw [ih, Int.natCast_add, Int.natCast_one, Int.add_mul, Int.one_mul]

theorem multiple_integer (k a : Int) : multiple k a = k * a := by
  cases k with
  | ofNat n => exact nsmul_integer n a
  | negSucc n =>
    change -nsmulRec (n+1) a = Int.negSucc n * a
    rw [nsmul_integer, show Int.negSucc n = -((n+1 : Nat) : Int) from rfl, Int.neg_mul]

end PreMssn.IntegerAction
