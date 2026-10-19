

namespace FableHilbertWalk20260819.H013QuarticSeparation

structure Vec2 where
  x : Int
  y : Int

def dot (u v : Vec2) : Int :=
  u.x * v.x + u.y * v.y

def normSq (u : Vec2) : Int :=
  dot u u

def quadReadout (u v : Vec2) : Int :=
  (dot u v) ^ 2

def quartReadout (u v : Vec2) : Int :=
  (dot u v) ^ 4

def e1 : Vec2 := ⟨5, 0⟩
def e2 : Vec2 := ⟨0, 5⟩

def p1 : Vec2 := ⟨3, 4⟩
def p2 : Vec2 := ⟨-4, 3⟩

def psi : Vec2 := ⟨5, 0⟩

theorem frames_equinorm :
    normSq e1 = 25 ∧ normSq e2 = 25 ∧
    normSq p1 = 25 ∧ normSq p2 = 25 := by
  decide

theorem frames_orthogonal :
    dot e1 e2 = 0 ∧ dot p1 p2 = 0 := by
  decide

theorem quadratic_frame_additivity :
    quadReadout e1 psi + quadReadout e2 psi = 625 ∧
    quadReadout p1 psi + quadReadout p2 psi = 625 := by
  decide

theorem quartic_frame_values :
    quartReadout e1 psi + quartReadout e2 psi = 390625 ∧
    quartReadout p1 psi + quartReadout p2 psi = 210625 := by
  decide

theorem quartic_frame_deficit :
    (quartReadout e1 psi + quartReadout e2 psi) -
    (quartReadout p1 psi + quartReadout p2 psi) = 180000 := by
  decide

theorem quartic_rival_fails_frame_additivity :
    quartReadout e1 psi + quartReadout e2 psi ≠
    quartReadout p1 psi + quartReadout p2 psi := by
  decide

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

private def l5aProvenance : String :=
  "Origin: lean4/H013QuarticRivalSeparation.lean Claim: frames_equinorm AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
