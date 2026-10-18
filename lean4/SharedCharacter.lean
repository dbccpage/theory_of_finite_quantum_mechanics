
import Std






namespace OvernightSharedCharacter


def oneThird : Rat := Rat.divInt 1 3

theorem oneThird_num_den : oneThird.num = 1 ∧ oneThird.den = 3 := by
  have nz : (3 : Nat) ≠ 0 := by decide
  have hdiv : oneThird = mkRat 1 3 := Rat.divInt_ofNat 1 3
  have hnorm : Rat.normalize 1 3 nz = mkRat 1 3 := Rat.normalize_eq_mkRat nz
  have hg : (1 : Int).natAbs.gcd 3 = 1 := by decide
  have hnum := Rat.num_normalize (num := 1) (den := 3) nz
  have hden := Rat.den_normalize (num := 1) (den := 3) nz
  constructor
  · rw [hdiv, ← hnorm, hnum, hg]
    exact Int.ediv_one 1
  · rw [hdiv, ← hnorm, hden, hg]

theorem divInt_n_over_n {n : Nat} (hn : n ≠ 0) : Rat.divInt n n = 1 := by
  have hdiv : Rat.divInt (↑n) ↑n = mkRat (↑n) n := Rat.divInt_ofNat (↑n) n
  have hnorm : Rat.normalize (↑n) n hn = mkRat (↑n) n := Rat.normalize_eq_mkRat hn
  have habs : (n : Int).natAbs = n := Int.natAbs_natCast n
  have hg : (n : Int).natAbs.gcd n = n := by
    rw [habs, Nat.gcd_self]
  have hnI : (n : Int) ≠ 0 := by
    intro h
    exact hn (Int.natCast_eq_zero.mp h)
  have hpos : 0 < n := Nat.pos_of_ne_zero hn
  have hnum : (Rat.normalize (↑n) n hn).num = 1 := by
    have h := Rat.num_normalize (num := (↑n : Int)) (den := n) hn
    rw [h, hg, Int.ediv_self hnI]
  have hden : (Rat.normalize (↑n) n hn).den = 1 := by
    have h := Rat.den_normalize (num := (↑n : Int)) (den := n) hn
    rw [h, hg, Nat.div_self hpos]
  have hr : Rat.normalize (↑n) n hn = 1 :=
    Rat.ext hnum (by
      have : (1 : Rat).den = 1 := Rat.den_natCast 1
      simpa [this] using hden)
  calc
    Rat.divInt n n = mkRat (↑n) n := hdiv
    _ = Rat.normalize (↑n) n hn := hnorm.symm
    _ = 1 := hr

theorem two_thirds_as_divInt :
    Rat.divInt 1 3 + Rat.divInt 1 3 = Rat.divInt 6 9 := by
  have z : (3 : Int) ≠ 0 := by decide
  exact Rat.divInt_add_divInt (n₁ := 1) (n₂ := 1) (d₁ := (3 : Int)) (d₂ := (3 : Int)) z z

theorem three_thirds_as_divInt :
    Rat.divInt 6 9 + Rat.divInt 1 3 = Rat.divInt 27 27 := by
  have z9 : (9 : Int) ≠ 0 := by decide
  have z3 : (3 : Int) ≠ 0 := by decide
  exact Rat.divInt_add_divInt (n₁ := 6) (n₂ := 1) (d₁ := (9 : Int)) (d₂ := (3 : Int)) z9 z3

theorem pairing_three_thirds : oneThird + oneThird + oneThird = 1 := by
  have h27 : (27 : Nat) ≠ 0 := by decide
  calc
    oneThird + oneThird + oneThird
        = Rat.divInt 1 3 + Rat.divInt 1 3 + Rat.divInt 1 3 := rfl
    _ = Rat.divInt 6 9 + Rat.divInt 1 3 := by rw [two_thirds_as_divInt]
    _ = Rat.divInt 27 27 := three_thirds_as_divInt
    _ = 1 := divInt_n_over_n h27

theorem pairing_ne_oneThird : (1 : Rat) ≠ oneThird := by
  intro h
  have hiff := (Rat.eq_iff_mul_eq_mul (p := (1 : Rat)) (q := oneThird)).mp h
  have hn1 : (1 : Rat).num = 1 := Rat.num_natCast 1
  have hd1 : (1 : Rat).den = 1 := Rat.den_natCast 1
  have ⟨hnum, hden⟩ := oneThird_num_den
  have hmul : (1 : Int) * 3 = 1 * 1 := by
    rw [hn1, hd1, hnum, hden] at hiff
    exact hiff
  exact (by decide : (3 : Int) ≠ 1) hmul

def IsIntegerRat (q : Rat) : Prop := q.den = 1

theorem pairing_is_integer : IsIntegerRat (1 : Rat) := rfl

theorem oneThird_not_integer : ¬ IsIntegerRat oneThird := by
  intro h
  have ⟨_, hden⟩ := oneThird_num_den
  have : (3 : Nat) = 1 := hden.symm.trans h
  exact (by decide : (3 : Nat) ≠ 1) this


def charEval (n k g : Nat) : Nat := (k * g) % n

theorem chi_one_at_one : charEval 3 1 1 = 1 := by decide

theorem chi_one_at_three : charEval 3 1 3 = 0 := by decide

theorem charEval_add (n k a b : Nat) :
    charEval n k (a + b) = (charEval n k a + charEval n k b) % n := by
  simp [charEval, Nat.mul_add, Nat.add_mod]

theorem charEval_killed_by_n {n k : Nat} (_hn : 0 < n) :
    charEval n k n = 0 := by
  simp [charEval]

theorem three_remainder_characters : List.length [0, 1, 2] = 3 := rfl


structure ScopeBoundary where
  pairingIsOne : Bool
  chiAtOneIsOneThird : Bool
  pairingEqualsChi : Bool
  znSoldAsU1 : Bool
  circleImportedForMu : Bool
  piFromExactQ : Bool
  authorityEffectNone : Bool
deriving DecidableEq, Repr

def scopeBoundary : ScopeBoundary :=
  { pairingIsOne := true
    chiAtOneIsOneThird := true
    pairingEqualsChi := false
    znSoldAsU1 := false
    circleImportedForMu := true
    piFromExactQ := false
    authorityEffectNone := true }

theorem scope_boundary_refuses_kills :
    scopeBoundary.pairingIsOne = true ∧
      scopeBoundary.chiAtOneIsOneThird = true ∧
      scopeBoundary.pairingEqualsChi = false ∧
      scopeBoundary.znSoldAsU1 = false ∧
      scopeBoundary.circleImportedForMu = true ∧
      scopeBoundary.piFromExactQ = false ∧
      scopeBoundary.authorityEffectNone = true := by
  decide

#print axioms pairing_three_thirds
#print axioms pairing_ne_oneThird
#print axioms oneThird_not_integer
#print axioms chi_one_at_one
#print axioms charEval_add
#print axioms scope_boundary_refuses_kills

end OvernightSharedCharacter

private def l5aProvenance : String :=
  "Origin: lean4/SharedCharacter.lean Claim: oneThird_num_den AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
