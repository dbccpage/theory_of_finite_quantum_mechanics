
import Std





namespace OvernightT2

theorem add_eq_add_self_implies_zero {x : Int} (h : x = x + x) : x = 0 := by
  omega

theorem additive_zero (f : Int → Int)
    (hadd : ∀ a b, f (a + b) = f a + f b) : f 0 = 0 := by
  have h := hadd 0 0
  have : f 0 = f 0 + f 0 := by simpa using h
  exact add_eq_add_self_implies_zero this

theorem additive_succ (f : Int → Int)
    (hadd : ∀ a b, f (a + b) = f a + f b) (n : Nat) :
    f (n + 1) = f n + f 1 := by
  simpa using hadd (n : Int) 1

theorem additive_on_nat (f : Int → Int)
    (hadd : ∀ a b, f (a + b) = f a + f b) :
    ∀ n : Nat, f n = n * f 1 := by
  intro n
  induction n with
  | zero =>
      have hz := additive_zero f hadd
      simpa using hz
  | succ n ih =>
      have hs := additive_succ f hadd n
      have hcast : ((n + 1 : Nat) : Int) = (n : Int) + 1 := by
        simp
      have hmul : ((n + 1 : Nat) : Int) * f 1 = (n : Int) * f 1 + f 1 := by
        simp [Int.natCast_succ, Int.add_mul]
      calc
        f (n + 1) = f n + f 1 := hs
        _ = n * f 1 + f 1 := by simpa [ih]
        _ = (n + 1) * f 1 := by
          simpa [hcast] using hmul.symm

theorem additive_neg (f : Int → Int)
    (hadd : ∀ a b, f (a + b) = f a + f b) (n : Int) :
    f (-n) = -f n := by
  have hsum := hadd (-n) n
  have hz := additive_zero f hadd
  have hzn : -n + n = (0 : Int) := by omega
  rw [hzn, hz] at hsum
  omega

theorem unique_additive_from_int (f : Int → Int)
    (hadd : ∀ a b, f (a + b) = f a + f b) :
    ∀ n : Int, f n = n * f 1 := by
  intro n
  match n with
  | Int.ofNat k =>
      exact additive_on_nat f hadd k
  | Int.negSucc k =>
      have hn : Int.negSucc k = -((k + 1 : Nat) : Int) := rfl
      rw [hn]
      have hneg := additive_neg f hadd ((k + 1 : Nat) : Int)
      rw [hneg]
      have hpos := additive_on_nat f hadd (k + 1)
      rw [hpos, Int.neg_mul]

def markedLift (g n : Int) : Int := n * g

theorem markedLift_one (g : Int) : markedLift g 1 = g := by
  simp [markedLift]

theorem markedLift_add (g a b : Int) :
    markedLift g (a + b) = markedLift g a + markedLift g b := by
  simp [markedLift, Int.add_mul]

theorem markedLift_is_the_unique_additive (g : Int) (f : Int → Int)
    (hadd : ∀ a b, f (a + b) = f a + f b) (h1 : f 1 = g) :
    ∀ n, f n = markedLift g n := by
  intro n
  have h := unique_additive_from_int f hadd n
  simpa [markedLift, h1] using h

theorem emod_eq_zero_iff_dvd (n : Int) {m : Int} (_hm : 0 < m) :
    n % m = 0 ↔ m ∣ n :=
  Int.dvd_iff_emod_eq_zero.symm

theorem no_nonzero_int_killed_by_n {n g : Int} (hn : 1 < n) :
    n * g = 0 → g = 0 := by
  intro h
  have hn0 : n ≠ 0 := by omega
  rcases Int.mul_eq_zero.mp h with h | h
  · exact absurd h hn0
  · exact h

structure ScopeBoundary where
  uniqueLiftOnInt : Bool
  residualForcesFreeZ : Bool
  piFromExactQ : Bool
  u1FromL1Mass : Bool
  znSoldAsU1 : Bool
  authorityEffectNone : Bool
deriving DecidableEq, Repr

def scopeBoundary : ScopeBoundary :=
  { uniqueLiftOnInt := true
    residualForcesFreeZ := false
    piFromExactQ := false
    u1FromL1Mass := false
    znSoldAsU1 := false
    authorityEffectNone := true }

theorem scope_boundary_refuses_kills :
    scopeBoundary.uniqueLiftOnInt = true ∧
      scopeBoundary.residualForcesFreeZ = false ∧
      scopeBoundary.piFromExactQ = false ∧
      scopeBoundary.u1FromL1Mass = false ∧
      scopeBoundary.znSoldAsU1 = false ∧
      scopeBoundary.authorityEffectNone = true := by
  decide

#print axioms unique_additive_from_int
#print axioms markedLift_is_the_unique_additive
#print axioms no_nonzero_int_killed_by_n
#print axioms scope_boundary_refuses_kills

end OvernightT2

private def l5aProvenance : String :=
  "Origin: lean4/T2MarkedFreeLift.lean Claim: add_eq_add_self_implies_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
