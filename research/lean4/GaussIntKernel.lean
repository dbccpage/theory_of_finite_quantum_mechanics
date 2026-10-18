/-
  GaussIntKernel.lean
  Core Gaussian integer arithmetic shared by the quotient-fiber and
  interference modules (retired papers QM_060 and QM_061).
  AuthorityEffect: None
  Zero Mathlib dependency.
-/

structure GaussInt where
  re : Int
  im : Int
  deriving DecidableEq, Repr

namespace GaussInt

def zero : GaussInt := ⟨0, 0⟩
def one : GaussInt := ⟨1, 0⟩
def i : GaussInt := ⟨0, 1⟩

def add (a b : GaussInt) : GaussInt := ⟨a.re + b.re, a.im + b.im⟩
def neg (a : GaussInt) : GaussInt := ⟨-a.re, -a.im⟩
def mul (a b : GaussInt) : GaussInt := ⟨a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re⟩
def conj (a : GaussInt) : GaussInt := ⟨a.re, -a.im⟩

def sqMod (a : GaussInt) : Int := a.re * a.re + a.im * a.im

theorem int_sq_nonneg (a : Int) : 0 ≤ a * a := by
  rcases Int.le_total 0 a with h | h
  · exact Int.mul_nonneg h h
  · rw [← Int.neg_mul_neg]
    exact Int.mul_nonneg (Int.neg_nonneg.mpr h) (Int.neg_nonneg.mpr h)

theorem sqMod_nonneg (a : GaussInt) : 0 ≤ sqMod a := by
  dsimp [sqMod]
  have h1 := int_sq_nonneg a.re
  have h2 := int_sq_nonneg a.im
  exact Int.add_nonneg h1 h2

theorem conj_mul_self_re (a : GaussInt) : (mul (conj a) a).re = sqMod a := by
  dsimp [mul, conj, sqMod]
  simp only [Int.neg_mul, Int.sub_neg]

theorem conj_mul_self_im (a : GaussInt) : (mul (conj a) a).im = 0 := by
  dsimp [mul, conj]
  simp only [Int.neg_mul]
  rw [Int.mul_comm a.im a.re]
  exact Int.add_right_neg (a.re * a.im)

end GaussInt

def Vec (K : Type) (Q : Type) := Q → K
