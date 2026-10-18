/-
  H033PythagoreanPellTsirelsonConvergence.lean
  AuthorityEffect: None.

  Finite claim only. The Pell convergent (119, 120, 169) gives an integer
  CHSH witness: orthonormal measurement vectors, a value above the classical
  bound `2 * 169`, and a square strictly below `8 * 169^2`. No real square
  root and no continuum Tsirelson theorem are used.
-/

namespace FableHilbertWalk20260819.H033

structure Vec2 where
  x : Int
  y : Int
  deriving DecidableEq, Repr

def dot (u v : Vec2) : Int := u.x * v.x + u.y * v.y

def normSq (u : Vec2) : Int := dot u u

def iabs (z : Int) : Int := if z < 0 then -z else z

def pellX : Int := 119
def pellY : Int := 120
def pellZ : Int := 169

/-- Bob's scaled vectors `(-119, 120)` and `(120, 119)`. -/
def bob1 : Vec2 := ⟨-pellX, pellY⟩
def bob2 : Vec2 := ⟨pellY, pellX⟩

/-- Sum of the four absolute components, the integer CHSH numerator. -/
def bellSum (b1 b2 : Vec2) : Int :=
  iabs b1.y + iabs b1.x + iabs b2.x + iabs b2.y

def classicalBound (scale : Int) : Int := 2 * scale

def tsirelsonSq (scale : Int) : Int := 8 * (scale * scale)

theorem pell_triple_pythagorean :
    pellX * pellX + pellY * pellY = pellZ * pellZ := by decide

theorem pell_basis_orthonormal :
    dot bob1 bob2 = 0 ∧
      normSq bob1 = pellZ * pellZ ∧
      normSq bob2 = pellZ * pellZ := by decide

theorem pell_bell_sum_eval :
    bellSum bob1 bob2 = 478 := by decide

theorem pell_bell_violates_classical :
    bellSum bob1 bob2 > classicalBound pellZ ∧
      bellSum bob1 bob2 - classicalBound pellZ = 140 := by decide

theorem pell_strictly_below_tsirelson :
    bellSum bob1 bob2 * bellSum bob1 bob2 < tsirelsonSq pellZ ∧
      tsirelsonSq pellZ - bellSum bob1 bob2 * bellSum bob1 bob2 = 4 := by decide

#print axioms pell_triple_pythagorean
#print axioms pell_basis_orthonormal
#print axioms pell_bell_sum_eval
#print axioms pell_bell_violates_classical
#print axioms pell_strictly_below_tsirelson

end FableHilbertWalk20260819.H033
