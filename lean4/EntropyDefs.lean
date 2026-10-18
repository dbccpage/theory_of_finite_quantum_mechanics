

namespace FiniteQm.C750.B01

structure RatFrac where
  num : Int
  den : Nat
  den_pos : 0 < den
deriving Repr

namespace RatFrac

def zero : RatFrac := ⟨0, 1, Nat.zero_lt_one⟩

def one : RatFrac := ⟨1, 1, Nat.zero_lt_one⟩

def add (x y : RatFrac) : RatFrac :=
  ⟨x.num * (y.den : Int) + y.num * (x.den : Int), x.den * y.den, Nat.mul_pos x.den_pos y.den_pos⟩

def neg (x : RatFrac) : RatFrac :=
  ⟨-x.num, x.den, x.den_pos⟩

def sub (x y : RatFrac) : RatFrac :=
  add x (neg y)

def mul (x y : RatFrac) : RatFrac :=
  ⟨x.num * y.num, x.den * y.den, Nat.mul_pos x.den_pos y.den_pos⟩

def smul (c : Int) (x : RatFrac) : RatFrac :=
  ⟨c * x.num, x.den, x.den_pos⟩

def isZero (x : RatFrac) : Prop := x.num = 0

end RatFrac

structure RationalDensity (d : Nat) where
  dim_pos : 0 < d
  weights : List Nat
  length_eq : weights.length = d
  denom : Nat
  denom_pos : 0 < denom
  trace_eq : weights.sum = denom

namespace RationalDensity

def purity_num (rho : RationalDensity d) : Nat :=
  (rho.weights.map (fun w => w * w)).sum

def is_pure (rho : RationalDensity d) : Prop :=
  purity_num rho = rho.denom * rho.denom

def is_mixed (rho : RationalDensity d) : Prop :=
  ¬ is_pure rho

end RationalDensity

structure LinearFormInLogarithms where
  basis : List Nat
  coeffs : List RatFrac
  len_eq : basis.length = coeffs.length

namespace LinearFormInLogarithms

def is_nonvanishing (form : LinearFormInLogarithms) : Prop :=
  ∃ c ∈ form.coeffs, c.num ≠ 0

def is_zero (form : LinearFormInLogarithms) : Prop :=
  ∀ c ∈ form.coeffs, c.num = 0

end LinearFormInLogarithms

def removable_singularity_term (w : Nat) (log_val : RatFrac) : RatFrac :=
  if w = 0 then RatFrac.zero else RatFrac.mul ⟨(w : Int), 1, Nat.zero_lt_one⟩ log_val

theorem removable_singularity_zero (log_val : RatFrac) :
    removable_singularity_term 0 log_val = RatFrac.zero := by
  rfl

theorem removable_singularity_is_zero (log_val : RatFrac) :
    (removable_singularity_term 0 log_val).isZero := by
  rw [removable_singularity_zero]
  rfl

theorem ratFrac_add_comm (x y : RatFrac) :
    (RatFrac.add x y).num = (RatFrac.add y x).num ∧
      (RatFrac.add x y).den = (RatFrac.add y x).den := by
  cases x with
  | mk xn xd _ =>
    cases y with
    | mk yn yd _ =>
      refine ⟨?_, Nat.mul_comm xd yd⟩
      simp [RatFrac.add, Int.add_comm]

theorem ratFrac_sub_self_zero (x : RatFrac) : (RatFrac.sub x x).isZero := by
  cases x with
  | mk xn xd hx =>
    unfold RatFrac.isZero RatFrac.sub RatFrac.add RatFrac.neg
    rw [← Int.add_mul, Int.add_right_neg, Int.zero_mul]

def pureOne (d : Nat) (hd : 0 < d) : RationalDensity d where
  dim_pos := hd
  weights := d :: List.replicate (d - 1) 0
  length_eq := by
    rw [List.length_cons, List.length_replicate]
    omega
  denom := d
  denom_pos := hd
  trace_eq := by
    have hrep : ∀ n, (List.replicate n (0 : Nat)).sum = 0 := by
      intro n
      induction n with
      | zero => rfl
      | succ n ih =>
        rw [List.replicate_succ, List.sum_cons, ih]
    rw [List.sum_cons, hrep]
    omega

def mixedHalf : RationalDensity 2 where
  dim_pos := by decide
  weights := [1, 1]
  length_eq := by decide
  denom := 2
  denom_pos := by decide
  trace_eq := by decide

theorem pureOne_is_pure (d : Nat) (hd : 0 < d) : (pureOne d hd).is_pure := by
  unfold RationalDensity.is_pure RationalDensity.purity_num
  have hden : (pureOne d hd).denom = d := by rfl
  have hw : (pureOne d hd).weights = d :: List.replicate (d - 1) 0 := by rfl
  rw [hden, hw]
  have hmap : ∀ n, (List.replicate n (0 : Nat)).map (fun w => w * w) = List.replicate n 0 := by
    intro n
    induction n with
    | zero => rfl
    | succ n ih =>
      rw [List.replicate_succ, List.map_cons, ih]
  have hrep : ∀ n, (List.replicate n (0 : Nat)).sum = 0 := by
    intro n
    induction n with
    | zero => rfl
    | succ n ih =>
      rw [List.replicate_succ, List.sum_cons, ih]
  rw [List.map_cons, hmap, List.sum_cons, hrep]
  omega

theorem mixedHalf_is_mixed : mixedHalf.is_mixed := by
  unfold RationalDensity.is_mixed RationalDensity.is_pure RationalDensity.purity_num mixedHalf
  decide

end FiniteQm.C750.B01

private def l5aProvenance : String :=
  "Origin: lean4/EntropyDefs.lean Claim: removable_singularity_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
