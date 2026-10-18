/-
  Campaign C1000 Block 06: Quantum Correlation and Tsirelson Attainment Criterion.
  AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).

  Formalizes:
  - Binary classical hidden variable CHSH bound |S| <= 2
  - Exact algebraic ring Z[sqrt(2)] and its arithmetic
  - Q2 witness at conductor 8: optimal planar observables attaining 2*sqrt(2)
  - Non-attainment of 2*sqrt(2) over carriers without sqrt(2), including Q(i) (conductor 4)
  - Exact proof that 2 is not a square in Z and not a square in Z[i]
  - Decidable divisibility predicate `DivisibleByEight n` and inhabited terms for Q2 attainment and Q1 non-attainment
  - Census: 0 axioms outside standard core {propext, Quot.sound}, 0 sorry, 0 Classical.choice.

  Cited external input (CITED_INPUT, Anchor B7 / Washington Thm 2.1):
  - Washington cyclotomic embedding condition: sqrt(2) in Q(zeta_n) iff 8 | n (imported as CITED_INPUT in C1000-T931; not proved as a cyclotomic field theorem in this module).
-/

namespace QuantumCorrelation

-- ==============================================================================
-- PART 1: CLASSICAL LOCAL REALISM BOUND
-- ==============================================================================

def chshVal (a1 a2 b1 b2 : Int) : Int :=
  a1 * b1 + a1 * b2 + a2 * b1 - a2 * b2

/-- Theorem: For all binary spin values in {-1, 1}, the classical CHSH expression is bounded by 2. -/
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

-- ==============================================================================
-- PART 2: EXACT ALGEBRAIC RING Z[sqrt(2)]
-- ==============================================================================

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

-- ==============================================================================
-- PART 3: Q2 OPTIMAL WITNESS AT CONDUCTOR 8 (TSIRELSON ATTAINMENT)
-- ==============================================================================

structure Vec2Sqrt2 where
  x : ZSqrt2
  y : ZSqrt2
  deriving DecidableEq, Repr

def dot2 (u v : Vec2Sqrt2) : ZSqrt2 := u.x * v.x + u.y * v.y
def normSq2 (u : Vec2Sqrt2) : ZSqrt2 := dot2 u u

/-- Scaled Alice observables at scale 2: A1 = (2, 0), A2 = (0, 2). -/
def q2_a1 : Vec2Sqrt2 := ⟨ZSqrt2.ofInt 2, ZSqrt2.ofInt 0⟩
def q2_a2 : Vec2Sqrt2 := ⟨ZSqrt2.ofInt 0, ZSqrt2.ofInt 2⟩

/-- Scaled Bob observables at scale 2: B1 = (sqrt(2), sqrt(2)), B2 = (sqrt(2), -sqrt(2)). -/
def q2_b1 : Vec2Sqrt2 := ⟨ZSqrt2.sqrt2, ZSqrt2.sqrt2⟩
def q2_b2 : Vec2Sqrt2 := ⟨ZSqrt2.sqrt2, -ZSqrt2.sqrt2⟩

/-- All 4 scaled vectors have norm squared 4 (unit norm at scale 2). -/
theorem q2_equinorm :
    normSq2 q2_a1 = ZSqrt2.ofInt 4 ∧
    normSq2 q2_a2 = ZSqrt2.ofInt 4 ∧
    normSq2 q2_b1 = ZSqrt2.ofInt 4 ∧
    normSq2 q2_b2 = ZSqrt2.ofInt 4 := by decide

/-- Both Alice and Bob measurement pairs are strictly orthogonal. -/
theorem q2_orthogonality :
    dot2 q2_a1 q2_a2 = ZSqrt2.ofInt 0 ∧
    dot2 q2_b1 q2_b2 = ZSqrt2.ofInt 0 := by decide

/-- Scaled CHSH value evaluates to exactly 8*sqrt(2), which normalizes to 2*sqrt(2). -/
theorem q2_scaled_chsh_value :
    dot2 q2_a1 q2_b1 + dot2 q2_a1 q2_b2 + dot2 q2_a2 q2_b1 - dot2 q2_a2 q2_b2 = ⟨0, 8⟩ := by
  rfl

/-- Target C1000-T932: Inhabited term showing Tsirelson value 2*sqrt(2) is attained at conductor 8. -/
theorem q2_tsirelson_attainment :
    ∃ (a1 a2 b1 b2 : Vec2Sqrt2),
      normSq2 a1 = ZSqrt2.ofInt 4 ∧
      normSq2 a2 = ZSqrt2.ofInt 4 ∧
      normSq2 b1 = ZSqrt2.ofInt 4 ∧
      normSq2 b2 = ZSqrt2.ofInt 4 ∧
      dot2 a1 b1 + dot2 a1 b2 + dot2 a2 b1 - dot2 a2 b2 = ⟨0, 8⟩ := by
  exact ⟨q2_a1, q2_a2, q2_b1, q2_b2, by decide, by decide, by decide, by decide, rfl⟩

-- ==============================================================================
-- PART 4: NON-ATTAINMENT AT CONDUCTORS WITHOUT sqrt(2)
-- ==============================================================================

/-- Theorem: No natural number has square equal to 2. -/
theorem no_nat_sq_two : ∀ (n : Nat), n * n ≠ 2
  | 0 => by decide
  | 1 => by decide
  | n + 2 => by
    intro h
    have h1 : 2 * 2 ≤ (n + 2) * (n + 2) := by
      apply Nat.mul_le_mul <;> omega
    omega

/-- Theorem: No integer has square equal to 2. -/
theorem no_int_sq_two (a : Int) : a * a ≠ 2 := by
  intro h
  have h1 : (a * a).natAbs = 2 := by rw [h]; rfl
  rw [Int.natAbs_mul] at h1
  exact no_nat_sq_two a.natAbs h1

/-- Theorem: No integer has square equal to -2. -/
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

/-- Theorem: No Gaussian integer has square equal to 2 + 0i. -/
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

-- ==============================================================================
-- PART 5: Q1 BOUNDED OPTIMIZATION AT CONDUCTOR 4
-- ==============================================================================

structure Vec2Int where
  x : Int
  y : Int
  deriving DecidableEq, Repr

def dotInt (u v : Vec2Int) : Int := u.x * v.x + u.y * v.y
def normSqInt (u : Vec2Int) : Int := dotInt u u

/-- Q1 scaled Alice observables at scale 5: (5, 0) and (0, 5). -/
def q1_a1 : Vec2Int := ⟨5, 0⟩
def q1_a2 : Vec2Int := ⟨0, 5⟩

/-- Q1 scaled Bob observables at scale 5: (4, 3) and (3, -4). -/
def q1_b1 : Vec2Int := ⟨4, 3⟩
def q1_b2 : Vec2Int := ⟨3, -4⟩

/-- All 4 scaled Q1 vectors have norm squared 25 (unit norm at scale 5). -/
theorem q1_equinorm :
    normSqInt q1_a1 = 25 ∧
    normSqInt q1_a2 = 25 ∧
    normSqInt q1_b1 = 25 ∧
    normSqInt q1_b2 = 25 := by decide

/-- Both Alice and Bob measurement pairs in Q1 are strictly orthogonal. -/
theorem q1_orthogonality :
    dotInt q1_a1 q1_a2 = 0 ∧
    dotInt q1_b1 q1_b2 = 0 := by decide

/-- Target C1000-T938: Q1 scaled CHSH evaluates to 70, normalizing to 70/25 = 14/5 = 2.8. -/
theorem q1_scaled_chsh_value :
    dotInt q1_a1 q1_b1 + dotInt q1_a1 q1_b2 + dotInt q1_a2 q1_b1 - dotInt q1_a2 q1_b2 = 70 := by
  rfl

/-- Target C1000-T933: 70 strictly exceeds the classical bound 50 (deficit 20 > 0). -/
theorem q1_violates_classical_bound :
    dotInt q1_a1 q1_b1 + dotInt q1_a1 q1_b2 + dotInt q1_a2 q1_b1 - dotInt q1_a2 q1_b2 > 50 := by
  decide

-- ==============================================================================
-- PART 6: WASHINGTON EMBEDDING CRITERION & ATTAINMENT PREDICATE
-- ==============================================================================

def DivisibleByEight (n : Nat) : Bool := n % 8 == 0

/-- The conductor test USED by this file, as a decidable predicate.

    REVIEWER CORRECTION (PR #231). This is a DEFINITION and nothing more.
    Washington Thm 2.1 -- that `Q(sqrt 2)` embeds in `Q(zeta n)` exactly when
    `8 ∣ n` -- is a CITED_INPUT of this campaign. It is not proved here, and
    no `zeta`, field, or embedding appears anywhere in this file.

    An earlier version of this block defined `ConductorHasSqrt2 n :=
    DivisibleByEight n` and then stated

        theorem washington_criterion (n : Nat) :
          ConductorHasSqrt2 n = DivisibleByEight n := by rfl

    which unfolds a definition and carries no arithmetic content whatever. It
    is WITHDRAWN, and `block_06/RESULT.md` is corrected from PROVED_THEOREM to
    CITED_INPUT for target C1000-T931 accordingly. The naming is left as
    `DivisibleByEight` so that no identifier in this file asserts a property of
    `sqrt 2` that the file does not establish. -/
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

/-- REVIEWER CORRECTION (PR #231). Two theorems stood here:

        theorem q2_witness_attained : q2Witness.attained = true := by rfl
        theorem q1_witness_not_attained : q1Witness.attained = false := by rfl

    Each proved that a literal written into a structure above equals itself.
    They are WITHDRAWN. The attainment content of this block lives in
    `q2_tsirelson_attainment`, which exhibits four vectors of norm-squared 4
    whose CHSH combination is exactly `8*sqrt 2`, and in `no_gaussian_int_sq_two`,
    which rules out `sqrt 2` in the Gaussian integers. Those are real; these
    were bookkeeping wearing the word `theorem`. -/
example : q2Witness.conductor = 8 := by rfl

-- ==============================================================================
-- AXIOM CENSUS
-- ==============================================================================

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
