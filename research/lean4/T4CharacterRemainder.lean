import Std

/-!
Overnight T4: character factorization on remainders, no Complex.

A character of `Z` with values in `Z/m` sending `1` to `r` is
`k ↦ (k * r) % m`. It factors through `Z/n` exactly when
`n * r ≡ 0 (mod m)`.

This is the remainder form of `z^n = 1`. Dual of `Z/n` stays
`Z/n`. Embedding into `U(1)` is not proved here.

AuthorityEffect: None.
-/

namespace OvernightT4

def charEval (r k m : Int) : Int := (k * r) % m

theorem charEval_add {r m : Int} (_hm : 0 < m) (a b : Int) :
    charEval r (a + b) m = (charEval r a m + charEval r b m) % m := by
  simp [charEval, Int.add_mul, Int.add_emod]

theorem factors_through_n {r n m : Int} (_hm : 0 < m) :
    charEval r n m = 0 ↔ m ∣ n * r := by
  simp [charEval]
  exact Int.dvd_iff_emod_eq_zero.symm

/-- For target `Z/n` and `r = 1`, the character factors at `n`. -/
theorem generator_killed_by_n {n : Int} (_hn : 0 < n) :
    charEval 1 n n = 0 := by
  simp [charEval]

theorem generator_not_killed_by_one {n : Int} (hn : 1 < n) :
    charEval 1 1 n ≠ 0 := by
  have h1 : (1 : Int) % n = 1 := Int.emod_eq_of_lt (by decide) hn
  simp [charEval, h1]

structure ScopeBoundary where
  remainderCharacters : Bool
  znSoldAsU1 : Bool
  piFromExactQ : Bool
  authorityEffectNone : Bool
deriving DecidableEq, Repr

def scopeBoundary : ScopeBoundary :=
  { remainderCharacters := true
    znSoldAsU1 := false
    piFromExactQ := false
    authorityEffectNone := true }

theorem scope_boundary_refuses_kills :
    scopeBoundary.remainderCharacters = true ∧
      scopeBoundary.znSoldAsU1 = false ∧
      scopeBoundary.piFromExactQ = false ∧
      scopeBoundary.authorityEffectNone = true := by
  decide

#print axioms charEval_add
#print axioms factors_through_n
#print axioms generator_killed_by_n
#print axioms scope_boundary_refuses_kills

end OvernightT4
