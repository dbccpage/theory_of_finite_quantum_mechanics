import Std

/-!
Overnight T1: scalar period subgroup.

Reduced classes `a/b` in `Q/Z` generate a cyclic group of order
`n = lcm(denominators)`. The algebraic core recorded here is:

- `Z/n` modelled as remainders; residue `1` has order `n`.
- Coefficients of `1/a` and `1/b` inside `Z/lcm(a,b)` are coprime.
- Bézout: those coefficients integer-combine to `1`, so they
  generate the whole remainder group `Z/n`.

Vector periods need not be cyclic. `Z/2 × Z/2` (Klein) is the
fence: four elements, every element 2-torsion, no generator of
order 4. Dual of `Z/n` remains `Z/n`, not free `U(1)`.

AuthorityEffect: None.
-/

namespace OvernightT1

/-! ## Remainders: order of 1 in `Z/n`. -/

theorem residue_one_killed_by_n {n : Nat} (_hn : 0 < n) :
    (n * 1) % n = 0 := by
  simp [Nat.mod_self]

theorem residue_one_not_killed_below {n k : Nat}
    (hk : 0 < k) (hkn : k < n) :
    (k * 1) % n ≠ 0 := by
  simp [Nat.mul_one, Nat.mod_eq_of_lt hkn]
  exact Nat.ne_of_gt hk

/-! ## Bézout for `Nat.gcd`. -/

theorem mul_reassoc (x q m : Int) : x * (q * m) = m * (x * q) := by
  calc
    x * (q * m) = (x * q) * m := (Int.mul_assoc x q m).symm
    _ = m * (x * q) := Int.mul_comm (x * q) m

theorem bezout_step_identity (x y q m r : Int) :
    (y - x * q) * m + x * (m * q + r) = x * r + y * m := by
  have hre := mul_reassoc x q m
  simp [Int.mul_add, Int.mul_comm, Int.sub_eq_add_neg, Int.add_assoc,
    Int.add_left_comm, Int.add_comm, Int.mul_neg, hre]
  rw [Int.add_right_neg, Int.add_zero]

theorem gcd_bezout (m n : Nat) :
    ∃ x y : Int, x * (m : Int) + y * (n : Int) = (m.gcd n : Int) := by
  let P : Nat → Nat → Prop := fun m n =>
    ∃ x y : Int, x * (m : Int) + y * (n : Int) = (m.gcd n : Int)
  refine Nat.gcd.induction (P := P) m n ?base ?step
  · intro n
    refine ⟨0, 1, ?_⟩
    simp [Nat.gcd_zero_left]
  · intro m n hm ih
    rcases ih with ⟨x, y, hx⟩
    let q : Int := ↑(n / m)
    let r : Int := ↑(n % m)
    refine ⟨y - x * q, x, ?_⟩
    have hsplit : (n : Int) = (m : Int) * q + r := by
      have hnat : m * (n / m) + n % m = n := Nat.div_add_mod n m
      calc
        (n : Int) = ↑(m * (n / m) + n % m) := by rw [hnat]
        _ = ↑(m * (n / m)) + ↑(n % m) := Int.natCast_add _ _
        _ = ↑m * ↑(n / m) + ↑(n % m) := by rw [Int.natCast_mul]
    have hrec : m.gcd n = (n % m).gcd m := Nat.gcd_rec m n
    have hid := bezout_step_identity x y q (↑m) r
    calc
      (y - x * q) * (m : Int) + x * (n : Int)
          = (y - x * q) * (m : Int) + x * ((m : Int) * q + r) := by rw [hsplit]
      _ = x * r + y * (m : Int) := hid
      _ = ((n % m).gcd m : Int) := hx
      _ = (m.gcd n : Int) := by rw [hrec]

theorem coprime_bezout {a b : Nat} (h : a.gcd b = 1) :
    ∃ u v : Int, u * (a : Int) + v * (b : Int) = 1 := by
  rcases gcd_bezout a b with ⟨u, v, huv⟩
  refine ⟨u, v, ?_⟩
  simpa [h] using huv

/-! ## Coefficient identity: `gcd(n/a, n/b) = n / lcm(a,b)`. -/

theorem gcd_div_self_eq_one {a b : Nat} (ha : 0 < a) (_hb : 0 < b) :
    (a / a.gcd b).gcd (b / a.gcd b) = 1 := by
  have hg : 0 < a.gcd b := Nat.gcd_pos_of_pos_left b ha
  have hdiv := Nat.gcd_div (Nat.gcd_dvd_left a b) (Nat.gcd_dvd_right a b)
  have hself : a.gcd b / a.gcd b = 1 := Nat.div_self hg
  simpa [hself] using hdiv

theorem lcm_div_left {a b : Nat} (ha : 0 < a) (_hb : 0 < b) :
    a.lcm b / a = b / a.gcd b := by
  have hposg : 0 < a.gcd b := Nat.gcd_pos_of_pos_left b ha
  have ha_lcm : a ∣ a.lcm b := Nat.dvd_lcm_left a b
  have hprod : a.gcd b * a.lcm b = a * b := Nat.gcd_mul_lcm a b
  have hcancel : a.gcd b * (a.lcm b / a) = b := by
    calc
      a.gcd b * (a.lcm b / a)
          = a.gcd b * a.lcm b / a := (Nat.mul_div_assoc (a.gcd b) ha_lcm).symm
      _ = a * b / a := by rw [hprod]
      _ = b := Nat.mul_div_cancel_left b ha
  have hother : a.gcd b * (b / a.gcd b) = b :=
    Nat.mul_div_cancel' (Nat.gcd_dvd_right a b)
  exact Nat.mul_left_cancel hposg (hcancel.trans hother.symm)

theorem n_div_a_factor {a n L : Nat}
    (hL : L ∣ n) (haL : a ∣ L) :
    n / a = (n / L) * (L / a) := by
  calc
    n / a = (n / L * L) / a := by rw [Nat.div_mul_cancel hL]
    _ = (n / L) * (L / a) := Nat.mul_div_assoc _ haL

theorem gcd_of_embedded_coeffs {a b n : Nat}
    (ha : 0 < a) (hb : 0 < b) (_hn : 0 < n)
    (hadv : a ∣ n) (hbdv : b ∣ n) :
    (n / a).gcd (n / b) = n / a.lcm b := by
  have hl : a.lcm b ∣ n := Nat.lcm_dvd hadv hbdv
  have h1 : n / a = (n / a.lcm b) * (a.lcm b / a) :=
    n_div_a_factor hl (Nat.dvd_lcm_left a b)
  have h2 : n / b = (n / a.lcm b) * (a.lcm b / b) :=
    n_div_a_factor hl (Nat.dvd_lcm_right a b)
  have h3 :
      (n / a).gcd (n / b) =
        (n / a.lcm b) * ((a.lcm b / a).gcd (a.lcm b / b)) := by
    rw [h1, h2, Nat.gcd_mul_left]
  have hcop : (a.lcm b / a).gcd (a.lcm b / b) = 1 := by
    have ha' : a.lcm b / a = b / a.gcd b := lcm_div_left ha hb
    have hb' : a.lcm b / b = a / a.gcd b := by
      have h := lcm_div_left hb ha
      rw [Nat.lcm_comm b a] at h
      rw [Nat.gcd_comm b a] at h
      exact h
    rw [ha', hb', Nat.gcd_comm]
    exact gcd_div_self_eq_one ha hb
  simpa [hcop] using h3

/-- Inside `Z/lcm(a,b)`, the residues of `1/a` and `1/b` are coprime. -/
theorem embedded_coeffs_coprime {a b : Nat} (ha : 0 < a) (hb : 0 < b) :
    (a.lcm b / a).gcd (a.lcm b / b) = 1 := by
  have hn : 0 < a.lcm b := Nat.lcm_pos ha hb
  have h :=
    gcd_of_embedded_coeffs ha hb hn (Nat.dvd_lcm_left a b) (Nat.dvd_lcm_right a b)
  simpa [Nat.div_self hn] using h

/-- Those residues integer-combine to `1`, so they generate `Z/n`. -/
theorem lcm_coeffs_generate_one {a b : Nat} (ha : 0 < a) (hb : 0 < b) :
    ∃ u v : Int,
      u * ((a.lcm b / a) : Int) + v * ((a.lcm b / b) : Int) = 1 :=
  coprime_bezout (embedded_coeffs_coprime ha hb)

/-- Concrete witness used by the Python twin: `1/2` and `1/3` generate `1/6`. -/
theorem one_half_one_third_coeffs :
    (Nat.lcm 2 3 / 2) = 3 ∧ (Nat.lcm 2 3 / 3) = 2 ∧ (3 : Nat).gcd 2 = 1 := by
  decide

theorem two_times_one_third_minus_one_half_is_one_sixth :
    (2 : Int) * 2 + (-1 : Int) * 3 = 1 := by
  decide

/-! ## Vector fence: Klein four-group is not cyclic. -/

def Klein := Bool × Bool

def kadd : Klein → Klein → Klein
  | (a, b), (c, d) => (a.xor c, b.xor d)

def kzero : Klein := (false, false)

theorem kadd_self (p : Klein) : kadd p p = kzero := by
  rcases p with ⟨x, y⟩
  cases x <;> cases y <;> rfl

theorem klein_four_distinct :
    ((false, false) : Klein) ≠ (true, false) ∧
      ((false, false) : Klein) ≠ (false, true) ∧
      ((false, false) : Klein) ≠ (true, true) ∧
      ((true, false) : Klein) ≠ (false, true) ∧
      ((true, false) : Klein) ≠ (true, true) ∧
      ((false, true) : Klein) ≠ (true, true) := by
  decide

/-- No element of Klein has additive order 4: double is always zero. -/
theorem klein_no_order_four (p : Klein) : kadd p p = kzero :=
  kadd_self p

/-! ## Scope fence. -/

structure ScopeBoundary where
  scalarLcmGeneratesZn : Bool
  vectorNeedNotCyclic : Bool
  znSoldAsU1 : Bool
  piFromExactQ : Bool
  freeZForcedByResidual : Bool
  authorityEffectNone : Bool
deriving DecidableEq, Repr

def scopeBoundary : ScopeBoundary :=
  { scalarLcmGeneratesZn := true
    vectorNeedNotCyclic := true
    znSoldAsU1 := false
    piFromExactQ := false
    freeZForcedByResidual := false
    authorityEffectNone := true }

theorem scope_boundary_refuses_kills :
    scopeBoundary.scalarLcmGeneratesZn = true ∧
      scopeBoundary.vectorNeedNotCyclic = true ∧
      scopeBoundary.znSoldAsU1 = false ∧
      scopeBoundary.piFromExactQ = false ∧
      scopeBoundary.freeZForcedByResidual = false ∧
      scopeBoundary.authorityEffectNone = true := by
  decide

#print axioms gcd_bezout
#print axioms embedded_coeffs_coprime
#print axioms lcm_coeffs_generate_one
#print axioms residue_one_not_killed_below
#print axioms klein_no_order_four
#print axioms scope_boundary_refuses_kills

end OvernightT1
