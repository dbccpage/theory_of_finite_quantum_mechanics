
import Std





namespace OvernightT4

def charEval (r k m : Int) : Int := (k * r) % m

theorem charEval_add {r m : Int} (_hm : 0 < m) (a b : Int) :
    charEval r (a + b) m = (charEval r a m + charEval r b m) % m := by
  simp [charEval, Int.add_mul, Int.add_emod]

theorem factors_through_n {r n m : Int} (_hm : 0 < m) :
    charEval r n m = 0 ↔ m ∣ n * r := by
  simp [charEval]
  exact Int.dvd_iff_emod_eq_zero.symm

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

private def l5aProvenance : String :=
  "Origin: lean4/T4CharacterRemainder.lean Claim: charEval_add AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
