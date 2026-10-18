



import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring

namespace GR002.HodgeDiracSUSY

def d0_eval (alpha : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (-alpha.1 + alpha.2.1, -alpha.2.1 + alpha.2.2, -alpha.2.2 + alpha.1)

def d1_eval (omega : ℝ × ℝ × ℝ) : ℝ :=
  omega.1 + omega.2.1 + omega.2.2

theorem d1_d0_nilpotent (alpha : ℝ × ℝ × ℝ) :
    d1_eval (d0_eval alpha) = 0 := by
  dsimp [d1_eval, d0_eval]
  ring

def d0_adjoint_eval (w : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (-w.1 + w.2.2, w.1 - w.2.1, w.2.1 - w.2.2)

def d1_adjoint_eval (x : ℝ) : ℝ × ℝ × ℝ := (x, x, x)

def add3 (u v : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (u.1 + v.1, u.2.1 + v.2.1, u.2.2 + v.2.2)

def delta1_filled (w : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  add3 (d0_eval (d0_adjoint_eval w)) (d1_adjoint_eval (d1_eval w))

theorem delta1_is_3_identity (w : ℝ × ℝ × ℝ) :
    delta1_filled w = (3 * w.1, 3 * w.2.1, 3 * w.2.2) := by
  dsimp [delta1_filled, add3, d0_eval, d0_adjoint_eval,
    d1_adjoint_eval, d1_eval]
  apply Prod.ext
  · ring
  · apply Prod.ext <;> ring

#print axioms d1_d0_nilpotent
#print axioms delta1_is_3_identity

end GR002.HodgeDiracSUSY
