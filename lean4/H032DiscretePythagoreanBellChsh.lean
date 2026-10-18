

namespace FableHilbertWalk20260819.H032


def chsh_val (a1 a2 b1 b2 : Int) : Int :=
  a1 * b1 + a1 * b2 + a2 * b1 - a2 * b2

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

theorem pythagorean_equinorm :
    normSq a1 = 25 ∧ normSq a2 = 25 ∧
    normSq b1 = 25 ∧ normSq b2 = 25 := by decide

theorem pythagorean_orthogonality :
    dot a1 a2 = 0 ∧ dot b1 b2 = 0 := by decide


structure Vec4 where
  w0 : Int
  w1 : Int
  w2 : Int
  w3 : Int
  deriving DecidableEq, Repr

def dot4 (x y : Vec4) : Int :=
  x.w0 * y.w0 + x.w1 * y.w1 + x.w2 * y.w2 + x.w3 * y.w3

def psi_minus : Vec4 := ⟨0, 1, -1, 0⟩

theorem psi_minus_norm_sq : dot4 psi_minus psi_minus = 2 := by decide

def apply_obs_tensor (u v : Vec2) : Vec4 :=
  ⟨u.y * v.x - u.x * v.y,
   - (u.x * v.x + u.y * v.y),
   u.x * v.x + u.y * v.y,
   u.y * v.x - u.x * v.y⟩

theorem singlet_expectation_derivation (u v : Vec2) :
    dot4 psi_minus (apply_obs_tensor u v) = -2 * dot u v := by
  dsimp [dot4, psi_minus, apply_obs_tensor, dot]
  have h1 : (0 : Int) * (u.y * v.x - u.x * v.y) = 0 := Int.zero_mul _
  have h2 : (1 : Int) * -(u.x * v.x + u.y * v.y) = -(u.x * v.x + u.y * v.y) := Int.one_mul _
  have h3 : (-1 : Int) * (u.x * v.x + u.y * v.y) = -(u.x * v.x + u.y * v.y) := by omega
  rw [h1, h2, h3]
  omega

def E (u v : Vec2) : Int := - dot u v

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

theorem pythagorean_chsh_quantum_sum :
    E a1 b1 + E a1 b2 - E a2 b1 + E a2 b2 = -70 := by decide

def classical_scaled_bound : Int := 2 * 25

theorem pythagorean_bell_violation :
    (- (E a1 b1 + E a1 b2 - E a2 b1 + E a2 b2)) > classical_scaled_bound ∧
    (- (E a1 b1 + E a1 b2 - E a2 b1 + E a2 b2)) - classical_scaled_bound = 20 := by decide

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

private def l5aProvenance : String :=
  "Origin: lean4/H032DiscretePythagoreanBellChsh.lean Claim: classical_chsh_bound AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
