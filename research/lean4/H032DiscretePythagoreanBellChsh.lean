/-
  H032DiscretePythagoreanBellChsh.lean
  AuthorityEffect: None.

  Shows in this model under exact integer arithmetic that:
  1. For all 16 deterministic local hidden variable assignments in {-1, 1}^4,
     the classical Bell-CHSH value satisfies |a1*b1 + a1*b2 + a2*b1 - a2*b2| <= 2.
  2. The discrete Pythagorean (3, 4, 5) basis vectors at scale 5 are strictly orthogonal
     and equinormed with norm squared 25:
     a1 = (0, 5), a2 = (5, 0), b1 = (-3, 4), b2 = (4, 3).
  3. The quantum singlet correlation is derived from the state vector |psi^-> = (0, 1, -1, 0)
     and observable tensor product (A(u) ⊗ B(v)), yielding <psi^- | A ⊗ B | psi^-> = -2 * dot(u, v),
     which normalizes by ||psi^-||^2 = 2 to exact E(u, v) = - dot(u, v).
  4. The quantum correlation values evaluate to exact integers at scale 25:
     E11 = -20, E12 = -15, E21 = +15, E22 = -20.
  5. The discrete Bell-CHSH expression evaluates to:
     |E11 + E12 - E21 + E22| = 70.
  6. Since the classical local realism bound at scale 25 is 2 * 25 = 50,
     the discrete quantum value 70 strictly violates the classical bound (deficit 70 - 50 = 20),
     achieving normalized S = 14/5 = 2.8 > 2 without continuous angle imports.
-/

namespace FableHilbertWalk20260819.H032

-- ==============================================================================
-- PART 1: CLASSICAL LOCAL REALISM BOUND (16 ASSIGNMENTS)
-- ==============================================================================

def chsh_val (a1 a2 b1 b2 : Int) : Int :=
  a1 * b1 + a1 * b2 + a2 * b1 - a2 * b2

/-- Theorem: For all binary spin values in {-1, 1}, the classical CHSH expression is bounded by 2. -/
theorem classical_chsh_bound (a1 a2 b1 b2 : Int)
    (ha1 : a1 = 1 ∨ a1 = -1)
    (ha2 : a2 = 1 ∨ a2 = -1)
    (hb1 : b1 = 1 ∨ b1 = -1)
    (hb2 : b2 = 1 ∨ b2 = -1) :
    chsh_val a1 a2 b1 b2 ≤ 2 ∧ chsh_val a1 a2 b1 b2 ≥ -2 := by
  rcases ha1 with rfl | rfl <;>
  rcases ha2 with rfl | rfl <;>
  rcases hb1 with rfl | rfl <;>
  rcases hb2 with rfl | rfl <;>
  decide

-- ==============================================================================
-- PART 2: DISCRETE PYTHAGOREAN ORTHONORMAL BASES AT SCALE 5
-- ==============================================================================

structure Vec2 where
  x : Int
  y : Int
  deriving DecidableEq, Repr

def dot (u v : Vec2) : Int := u.x * v.x + u.y * v.y
def normSq (u : Vec2) : Int := dot u u

def a1 : Vec2 := ⟨0, 5⟩
def a2 : Vec2 := ⟨5, 0⟩
def b1 : Vec2 := ⟨-3, 4⟩
def b2 : Vec2 := ⟨4, 3⟩

/-- All 4 vectors have norm squared 25 (unit norm at scale 5). -/
theorem pythagorean_equinorm :
    normSq a1 = 25 ∧ normSq a2 = 25 ∧
    normSq b1 = 25 ∧ normSq b2 = 25 := by decide

/-- Both Alice's and Bob's measurement pairs are strictly orthogonal. -/
theorem pythagorean_orthogonality :
    dot a1 a2 = 0 ∧ dot b1 b2 = 0 := by decide

-- ==============================================================================
-- PART 3: SINGLET STATE DERIVATION & QUANTUM CORRELATIONS
-- ==============================================================================

structure Vec4 where
  w0 : Int
  w1 : Int
  w2 : Int
  w3 : Int
  deriving DecidableEq, Repr

def dot4 (x y : Vec4) : Int :=
  x.w0 * y.w0 + x.w1 * y.w1 + x.w2 * y.w2 + x.w3 * y.w3

/-- Singlet state vector in Z^4: |psi^-> = |01> - |10> = (0, 1, -1, 0). -/
def psi_minus : Vec4 := ⟨0, 1, -1, 0⟩

/-- Norm squared of the discrete singlet state vector is 2. -/
theorem psi_minus_norm_sq : dot4 psi_minus psi_minus = 2 := by decide

/-- Action of observable tensor product (A(u) ⊗ B(v)) on the singlet state vector |psi^->:
    Row 0: u.y * v.x - u.x * v.y
    Row 1: - (u.x * v.x + u.y * v.y)
    Row 2: u.x * v.x + u.y * v.y
    Row 3: u.y * v.x - u.x * v.y -/
def apply_obs_tensor (u v : Vec2) : Vec4 :=
  ⟨u.y * v.x - u.x * v.y,
   - (u.x * v.x + u.y * v.y),
   u.x * v.x + u.y * v.y,
   u.y * v.x - u.x * v.y⟩

/-- Matrix-vector expectation value of (A(u) ⊗ B(v)) on singlet state |psi^->:
    <psi^- | (A(u) ⊗ B(v)) | psi^-> = -2 * dot(u, v). -/
theorem singlet_expectation_derivation (u v : Vec2) :
    dot4 psi_minus (apply_obs_tensor u v) = -2 * dot u v := by
  dsimp [dot4, psi_minus, apply_obs_tensor, dot]
  have h1 : (0 : Int) * (u.y * v.x - u.x * v.y) = 0 := Int.zero_mul _
  have h2 : (1 : Int) * -(u.x * v.x + u.y * v.y) = -(u.x * v.x + u.y * v.y) := Int.one_mul _
  have h3 : (-1 : Int) * (u.x * v.x + u.y * v.y) = -(u.x * v.x + u.y * v.y) := by omega
  rw [h1, h2, h3]
  omega

/-- Scaled quantum singlet correlation: E(u, v) = - dot(u, v). -/
def E (u v : Vec2) : Int := - dot u v

/-- Normalizing by singlet norm squared (2) yields the exact correlation E(u, v) = - dot(u, v):
    <psi | (A ⊗ B) | psi> = normSq(psi) * E(u, v). -/
theorem singlet_correlation_normalized (u v : Vec2) :
    dot4 psi_minus (apply_obs_tensor u v) = 2 * E u v := by
  have h := singlet_expectation_derivation u v
  dsimp [E]
  omega

theorem pythagorean_correlations :
    E a1 b1 = -20 ∧
    E a1 b2 = -15 ∧
    E a2 b1 = 15 ∧
    E a2 b2 = -20 := by decide

/-- Scaled CHSH quantum operator value:
    E(a1, b1) + E(a1, b2) - E(a2, b1) + E(a2, b2) = -70. -/
theorem pythagorean_chsh_quantum_sum :
    E a1 b1 + E a1 b2 - E a2 b1 + E a2 b2 = -70 := by decide

/-- Scaled classical bound at scale 25 is 50. -/
def classical_scaled_bound : Int := 2 * 25

/-- Strict violation of the classical local realism bound:
    |-70| = 70 > 50, with exact quantum surplus of 20. -/
theorem pythagorean_bell_violation :
    (- (E a1 b1 + E a1 b2 - E a2 b1 + E a2 b2)) > classical_scaled_bound ∧
    (- (E a1 b1 + E a1 b2 - E a2 b1 + E a2 b2)) - classical_scaled_bound = 20 := by decide

/-- Ratio 70 / 25 corresponds to 14/5 in exact reduced fraction:
    70 * 1 = 14 * 5. -/
theorem pythagorean_rational_ratio : (70 : Int) * 1 = 14 * 5 := by decide

#print axioms classical_chsh_bound
#print axioms pythagorean_equinorm
#print axioms pythagorean_orthogonality
#print axioms psi_minus_norm_sq
#print axioms singlet_expectation_derivation
#print axioms singlet_correlation_normalized
#print axioms pythagorean_correlations
#print axioms pythagorean_chsh_quantum_sum
#print axioms pythagorean_bell_violation
#print axioms pythagorean_rational_ratio

end FableHilbertWalk20260819.H032
