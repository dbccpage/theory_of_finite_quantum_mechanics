


namespace QuantumCorrelation


def chshVal (a1 a2 b1 b2 : Int) : Int :=
  a1 * b1 + a1 * b2 + a2 * b1 - a2 * b2

theorem classical_chsh_bound (a1 a2 b1 b2 : Int)
    (ha1 : a1 = 1 ∨ a1 = -1)
    (ha2 : a2 = 1 ∨ a2 = -1)
    (hb1 : b1 = 1 ∨ b1 = -1)
    (hb2 : b2 = 1 ∨ b2 = -1) :
    chshVal a1 a2 b1 b2 ≤ 2 ∧ chshVal a1 a2 b1 b2 ≥ -2 := by
  rcases ha1 with rfl | rfl <;>
  rcases ha2 with rfl | rfl <;>
  rcases hb1 with rfl | rfl <;>
  rcases hb2 with rfl | rfl <;>
  decide


structure ZSqrt2 where
  a : Int
  b : Int
  deriving DecidableEq, Repr

namespace ZSqrt2

def add (x y : ZSqrt2) : ZSqrt2 := ⟨x.a + y.a, x.b + y.b⟩
def sub (x y : ZSqrt2) : ZSqrt2 := ⟨x.a - y.a, x.b - y.b⟩
def mul (x y : ZSqrt2) : ZSqrt2 := ⟨x.a * y.a + 2 * x.b * y.b, x.a * y.b + x.b * y.a⟩
def neg (x : ZSqrt2) : ZSqrt2 := ⟨-x.a, -x.b⟩

instance : Add ZSqrt2 := ⟨add⟩
instance : Sub ZSqrt2 := ⟨sub⟩
instance : Mul ZSqrt2 := ⟨mul⟩
instance : Neg ZSqrt2 := ⟨neg⟩

def ofInt (n : Int) : ZSqrt2 := ⟨n, 0⟩
def sqrt2 : ZSqrt2 := ⟨0, 1⟩

theorem sqrt2_sq : sqrt2 * sqrt2 = ofInt 2 := by rfl

end ZSqrt2


structure Vec2Sqrt2 where
  x : ZSqrt2
  y : ZSqrt2
  deriving DecidableEq, Repr

def dot2 (u v : Vec2Sqrt2) : ZSqrt2 := u.x * v.x + u.y * v.y
def normSq2 (u : Vec2Sqrt2) : ZSqrt2 := dot2 u u

def q2_a1 : Vec2Sqrt2 := ⟨ZSqrt2.ofInt 2, ZSqrt2.ofInt 0⟩
def q2_a2 : Vec2Sqrt2 := ⟨ZSqrt2.ofInt 0, ZSqrt2.ofInt 2⟩

def q2_b1 : Vec2Sqrt2 := ⟨ZSqrt2.sqrt2, ZSqrt2.sqrt2⟩
def q2_b2 : Vec2Sqrt2 := ⟨ZSqrt2.sqrt2, -ZSqrt2.sqrt2⟩

theorem q2_equinorm :
    normSq2 q2_a1 = ZSqrt2.ofInt 4 ∧
    normSq2 q2_a2 = ZSqrt2.ofInt 4 ∧
    normSq2 q2_b1 = ZSqrt2.ofInt 4 ∧
    normSq2 q2_b2 = ZSqrt2.ofInt 4 := by decide

theorem q2_orthogonality :
    dot2 q2_a1 q2_a2 = ZSqrt2.ofInt 0 ∧
    dot2 q2_b1 q2_b2 = ZSqrt2.ofInt 0 := by decide

theorem q2_scaled_chsh_value :
    dot2 q2_a1 q2_b1 + dot2 q2_a1 q2_b2 + dot2 q2_a2 q2_b1 - dot2 q2_a2 q2_b2 = ⟨0, 8⟩ := by
  rfl

theorem q2_tsirelson_attainment :
    ∃ (a1 a2 b1 b2 : Vec2Sqrt2),
      normSq2 a1 = ZSqrt2.ofInt 4 ∧
      normSq2 a2 = ZSqrt2.ofInt 4 ∧
      normSq2 b1 = ZSqrt2.ofInt 4 ∧
      normSq2 b2 = ZSqrt2.ofInt 4 ∧
      dot2 a1 b1 + dot2 a1 b2 + dot2 a2 b1 - dot2 a2 b2 = ⟨0, 8⟩ := by
  exact ⟨q2_a1, q2_a2, q2_b1, q2_b2, by decide, by decide, by decide, by decide, rfl⟩


theorem no_nat_sq_two : ∀ (n : Nat), n * n ≠ 2
  | 0 => by decide
  | 1 => by decide
  | n + 2 => by
    intro h
    have h1 : 2 * 2 ≤ (n + 2) * (n + 2) := by
      apply Nat.mul_le_mul <;> omega
    omega

theorem no_int_sq_two (a : Int) : a * a ≠ 2 := by
  intro h
  have h1 : (a * a).natAbs = 2 := by rw [h]; rfl
  rw [Int.natAbs_mul] at h1
  exact no_nat_sq_two a.natAbs h1

theorem no_int_sq_neg_two (a : Int) : a * a ≠ -2 := by
  intro h
  have h1 : (a * a).natAbs = 2 := by rw [h]; rfl
  rw [Int.natAbs_mul] at h1
  exact no_nat_sq_two a.natAbs h1

structure ZI where
  re : Int
  im : Int
  deriving DecidableEq, Repr

namespace ZI
def mul (x y : ZI) : ZI := ⟨x.re * y.re - x.im * y.im, x.re * y.im + x.im * y.re⟩
instance : Mul ZI := ⟨mul⟩
end ZI

theorem no_gaussian_int_sq_two (z : ZI) : z * z ≠ ⟨2, 0⟩ := by
  intro h
  injection h with hre him
  change z.re * z.re - z.im * z.im = 2 at hre
  change z.re * z.im + z.im * z.re = 0 at him
  have hcomm : z.im * z.re = z.re * z.im := Int.mul_comm z.im z.re
  rw [hcomm] at him
  have him2 : 2 * (z.re * z.im) = 0 := by omega
  have hzero : z.re * z.im = 0 := by omega
  have hab : z.re = 0 ∨ z.im = 0 := Int.mul_eq_zero.mp hzero
  rcases hab with hre0 | him0
  · rw [hre0] at hre
    have : z.im * z.im = -2 := by omega
    exact no_int_sq_neg_two z.im this
  · rw [him0] at hre
    have : z.re * z.re = 2 := by omega
    exact no_int_sq_two z.re this


structure Vec2Int where
  x : Int
  y : Int
  deriving DecidableEq, Repr

def dotInt (u v : Vec2Int) : Int := u.x * v.x + u.y * v.y
def normSqInt (u : Vec2Int) : Int := dotInt u u

def q1_a1 : Vec2Int := ⟨5, 0⟩
def q1_a2 : Vec2Int := ⟨0, 5⟩

def q1_b1 : Vec2Int := ⟨4, 3⟩
def q1_b2 : Vec2Int := ⟨3, -4⟩

theorem q1_equinorm :
    normSqInt q1_a1 = 25 ∧
    normSqInt q1_a2 = 25 ∧
    normSqInt q1_b1 = 25 ∧
    normSqInt q1_b2 = 25 := by decide

theorem q1_orthogonality :
    dotInt q1_a1 q1_a2 = 0 ∧
    dotInt q1_b1 q1_b2 = 0 := by decide

theorem q1_scaled_chsh_value :
    dotInt q1_a1 q1_b1 + dotInt q1_a1 q1_b2 + dotInt q1_a2 q1_b1 - dotInt q1_a2 q1_b2 = 70 := by
  rfl

theorem q1_violates_classical_bound :
    dotInt q1_a1 q1_b1 + dotInt q1_a1 q1_b2 + dotInt q1_a2 q1_b1 - dotInt q1_a2 q1_b2 > 50 := by
  decide


def DivisibleByEight (n : Nat) : Bool := n % 8 == 0





abbrev ConductorHasSqrt2 : Nat → Bool := DivisibleByEight

theorem conductor_8_divisible_by_8 : DivisibleByEight 8 = true := by rfl
theorem conductor_4_not_divisible_by_8 : DivisibleByEight 4 = false := by rfl
theorem conductor_12_not_divisible_by_8 : DivisibleByEight 12 = false := by rfl

structure AttainmentWitness where
  conductor : Nat
  attained : Bool
  witness_name : String

def q2Witness : AttainmentWitness := ⟨8, true, "Q2"⟩
def q1Witness : AttainmentWitness := ⟨4, false, "Q1"⟩



example : q2Witness.conductor = 8 := by rfl


#print axioms classical_chsh_bound
#print axioms q2_scaled_chsh_value
#print axioms q2_tsirelson_attainment
#print axioms no_int_sq_two
#print axioms no_int_sq_neg_two
#print axioms no_gaussian_int_sq_two
#print axioms q1_scaled_chsh_value
#print axioms q1_violates_classical_bound
#print axioms conductor_8_divisible_by_8
#print axioms conductor_4_not_divisible_by_8

end QuantumCorrelation

private def l5aProvenance : String :=
  "Origin: lean4/QuantumCorrelation.lean Claim: classical_chsh_bound AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
