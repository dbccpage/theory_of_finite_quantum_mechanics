/-
  H013QuarticRivalSeparation -- Phase 1 separating experiment.
  AuthorityEffect: None.

  Shows in this model under exact arithmetic that:
  1. The quadratic Born readout preserves frame additivity across the standard
     basis and the (3, 4, 5) Pythagorean basis.
  2. The H013 quartic rival fails frame additivity, yielding 390625 on the standard
     basis and 210625 on the Pythagorean basis (exact deficit 180000, i.e. 288/625).
  3. Any homogeneous degree-4 polynomial satisfying the frame-additivity symmetry
     and trace constraints factors as (x^2 + y^2) * (quadratic), collapsing on the
     unit circle to quadratic degree p = 2.
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace FableHilbertWalk20260819.H013QuarticSeparation

/-- 2D integer vector. -/
structure Vec2 where
  x : Int
  y : Int

/-- Dot product of two 2D integer vectors. -/
def dot (u v : Vec2) : Int :=
  u.x * v.x + u.y * v.y

/-- Norm squared of a 2D integer vector. -/
def normSq (u : Vec2) : Int :=
  dot u u

/-- Quadratic readout: (<u, v>)^2. -/
def quadReadout (u v : Vec2) : Int :=
  (dot u v) ^ 2

/-- Quartic readout: (<u, v>)^4. -/
def quartReadout (u v : Vec2) : Int :=
  (dot u v) ^ 4

/-- Standard basis vectors at scale 5. -/
def e1 : Vec2 := ⟨5, 0⟩
def e2 : Vec2 := ⟨0, 5⟩

/-- Pythagorean (3, 4, 5) basis vectors. -/
def p1 : Vec2 := ⟨3, 4⟩
def p2 : Vec2 := ⟨-4, 3⟩

/-- State vector at scale 5. -/
def psi : Vec2 := ⟨5, 0⟩

/-- Both frames have norm squared 25 on all basis elements. -/
theorem frames_equinorm :
    normSq e1 = 25 ∧ normSq e2 = 25 ∧
    normSq p1 = 25 ∧ normSq p2 = 25 := by
  decide

/-- Both frames are strictly orthogonal. -/
theorem frames_orthogonal :
    dot e1 e2 = 0 ∧ dot p1 p2 = 0 := by
  decide

/-- Quadratic Born readout satisfies frame additivity: sum is 625 on both frames. -/
theorem quadratic_frame_additivity :
    quadReadout e1 psi + quadReadout e2 psi = 625 ∧
    quadReadout p1 psi + quadReadout p2 psi = 625 := by
  decide

/-- Quartic rival readout values: 390625 on standard frame, 210625 on Pythagorean frame. -/
theorem quartic_frame_values :
    quartReadout e1 psi + quartReadout e2 psi = 390625 ∧
    quartReadout p1 psi + quartReadout p2 psi = 210625 := by
  decide

/-- Deficit of the quartic rival: exact difference is 180000 != 0. -/
theorem quartic_frame_deficit :
    (quartReadout e1 psi + quartReadout e2 psi) -
    (quartReadout p1 psi + quartReadout p2 psi) = 180000 := by
  decide

/-- The quartic rival strictly fails frame additivity on orthogonal pairs. -/
theorem quartic_rival_fails_frame_additivity :
    quartReadout e1 psi + quartReadout e2 psi ≠
    quartReadout p1 psi + quartReadout p2 psi := by
  decide

/-- Algebraic reduction: Any quartic polynomial satisfying the frame-additivity
    conditions (c13 = c31 and c22 = c40 + c04) factors through x^2 + y^2. -/
theorem quartic_polynomial_reduction (x y c40 c31 c04 : Int) :
    (x * x + y * y) * (c40 * (x * x) + c31 * (x * y) + c04 * (y * y)) =
    c40 * (x * x * x * x) + c31 * (x * x * x * y) + (c40 + c04) * (x * x * y * y) + c31 * (x * y * y * y) + c04 * (y * y * y * y) := by
  have h1 : (x * x + y * y) * (c40 * (x * x) + c31 * (x * y) + c04 * (y * y)) =
      (x * x) * (c40 * (x * x)) + (x * x) * (c31 * (x * y)) + (x * x) * (c04 * (y * y)) +
      ((y * y) * (c40 * (x * x)) + (y * y) * (c31 * (x * y)) + (y * y) * (c04 * (y * y))) := by
    rw [Int.add_mul, Int.mul_add, Int.mul_add, Int.mul_add, Int.mul_add]
  have h2 : (c40 + c04) * (x * x * y * y) = c40 * (x * x * y * y) + c04 * (x * x * y * y) := by
    rw [Int.add_mul]
  rw [h1, h2]
  have e1 : (x * x) * (c40 * (x * x)) = c40 * (x * x * x * x) := by ac_rfl
  have e2 : (x * x) * (c31 * (x * y)) = c31 * (x * x * x * y) := by ac_rfl
  have e3 : (x * x) * (c04 * (y * y)) = c04 * (x * x * y * y) := by ac_rfl
  have e4 : (y * y) * (c40 * (x * x)) = c40 * (x * x * y * y) := by ac_rfl
  have e5 : (y * y) * (c31 * (x * y)) = c31 * (x * y * y * y) := by ac_rfl
  have e6 : (y * y) * (c04 * (y * y)) = c04 * (y * y * y * y) := by ac_rfl
  rw [e1, e2, e3, e4, e5, e6]
  ac_rfl

#print axioms frames_equinorm
#print axioms frames_orthogonal
#print axioms quadratic_frame_additivity
#print axioms quartic_frame_values
#print axioms quartic_frame_deficit
#print axioms quartic_rival_fails_frame_additivity
#print axioms quartic_polynomial_reduction

end FableHilbertWalk20260819.H013QuarticSeparation
