import BornGaussianRationalFrameObstruction
import Mathlib.Tactic.LinearCombination

/-!
# Frame functions on `ℚ(i)³`: the residue-modulo-`2` class ansatz is closed

AuthorityEffect: None.

`BornGaussianRationalFrameObstruction` shows that a frame function on `K³`, `K = ℚ(i)`, whose
value on Gaussian-integer vectors not divisible by `1 + i` depends only on the `(1+i)`-parity
class `((a+b)%2, (c+d)%2, (e+g)%2)` is the constant `1/3`.  Its docstring names residues modulo
`2` as the next untested ansatz.  This file closes it.

Setting.  `gv a b c d e g = (a+bi, c+di, e+gi)`.  A frame function `f` is *`2`-class determined*
(`Mod2Determined f col`) when `f (gv a b c d e g) = col (a%2) (b%2) (c%2) (d%2) (e%2) (g%2)`
for every Gaussian-integer vector with some component not divisible by `1 + i`.  There are
`4³ - 2³ = 56` such residue classes modulo `2`.

Main result.  `mod2_class_function_is_third`: every `2`-class determined frame function is
`1/3` on all those vectors.  The proof lists `56` explicit orthogonal frames of Gaussian-integer
vectors with coordinates of modulus at most `3`, whose `56 × 56` class-incidence matrix is
invertible over `ℚ`; each class value is the explicit rational combination of the frame
equations given by a row of the inverse (`linear_combination`).  The frames and the inverse
were found by an exact search (`checks/independent/fq-gap-born-uniqueness-gleason-mod2.py`)
and are re-verified here by the kernel.

This closes the modulo-`2` ansatz only.  Whether every frame function on `ℚ(i)³` rays is
quadratic remains undecided here; see `CampaignBornRationalRayObstruction` for the contrasting `ℚ³`
case.  Nothing here is a statement about physics.
-/

namespace BornFable.GaussianFrames

open BornFable

/-- `f` is determined by the residues modulo `2` of the six integer coordinates on
Gaussian-integer vectors not all of whose components are divisible by `1 + i`. -/
def Mod2Determined (f : GVec → ℚ) (col : ℤ → ℤ → ℤ → ℤ → ℤ → ℤ → ℚ) : Prop :=
  ∀ a b c d e g : ℤ, ¬ ((a + b) % 2 = 0 ∧ (c + d) % 2 = 0 ∧ (e + g) % 2 = 0) →
    f (gv a b c d e g) = col (a % 2) (b % 2) (c % 2) (d % 2) (e % 2) (g % 2)

theorem nonZero_of_x_im {v : GVec} (h : v.x.im ≠ 0) : v.NonZero :=
  Or.inl fun e => h (by simp [e])

theorem nonZero_of_y_im {v : GVec} (h : v.y.im ≠ 0) : v.NonZero :=
  Or.inr (Or.inl fun e => h (by simp [e]))

theorem nonZero_of_z_im {v : GVec} (h : v.z.im ≠ 0) : v.NonZero :=
  Or.inr (Or.inr fun e => h (by simp [e]))

/-- Class value of an explicit Gaussian-integer vector, in normalised form. -/
theorem class_value2 {f : GVec → ℚ} {col : ℤ → ℤ → ℤ → ℤ → ℤ → ℤ → ℚ} (hP : Mod2Determined f col)
    (a b c d e g p q r s t u : ℤ)
    (hne : ¬ ((a + b) % 2 = 0 ∧ (c + d) % 2 = 0 ∧ (e + g) % 2 = 0))
    (h1 : a % 2 = p) (h2 : b % 2 = q) (h3 : c % 2 = r) (h4 : d % 2 = s) (h5 : e % 2 = t)
    (h6 : g % 2 = u) :
    f (gv a b c d e g) = col p q r s t u := by
  rw [hP a b c d e g hne, h1, h2, h3, h4, h5, h6]

/-! ### Fifty-six explicit frames -/
theorem frame1 : IsFrame (gv (-1) 0 0 0 0 0) (gv 0 0 (-1) 0 0 0) (gv 0 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame2 : IsFrame (gv (-1) 0 0 0 0 0) (gv 0 0 0 (-1) 0 0) (gv 0 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y_im (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame3 : IsFrame (gv (-1) 0 0 0 0 0) (gv 0 0 0 0 0 (-1)) (gv 0 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_z_im (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame4 : IsFrame (gv 0 (-1) 0 0 0 0) (gv 0 0 (-1) 0 0 0) (gv 0 0 0 0 1 0) :=
  ⟨nonZero_of_x_im (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame5 : IsFrame (gv (-1) 0 (-1) 0 0 0) (gv (-1) 0 1 0 0 0) (gv 0 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame6 : IsFrame (gv (-1) 0 (-1) 0 0 0) (gv 0 (-1) 0 1 0 0) (gv 0 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame7 : IsFrame (gv (-1) 0 0 (-1) 0 0) (gv (-1) 0 0 1 0 0) (gv 0 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame8 : IsFrame (gv (-1) 0 0 (-1) 0 0) (gv 0 (-1) (-1) 0 0 0) (gv 0 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame9 : IsFrame (gv (-1) 0 0 0 (-1) 0) (gv (-1) 0 0 0 1 0) (gv 0 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame10 : IsFrame (gv (-1) 0 0 0 (-1) 0) (gv 0 (-1) 0 0 0 1) (gv 0 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame11 : IsFrame (gv (-1) 0 0 0 0 (-1)) (gv (-1) 0 0 0 0 1) (gv 0 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame12 : IsFrame (gv (-1) 0 0 0 0 (-1)) (gv 0 (-1) 0 0 (-1) 0) (gv 0 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame13 : IsFrame (gv (-1) 0 0 0 0 0) (gv 0 0 (-1) 0 (-1) 0) (gv 0 0 (-1) 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame14 : IsFrame (gv (-1) 0 0 0 0 0) (gv 0 0 (-1) 0 0 (-1)) (gv 0 0 0 1 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_y_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame15 : IsFrame (gv (-1) 0 0 0 0 0) (gv 0 0 0 (-1) (-1) 0) (gv 0 0 0 (-1) 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y_im (by norm_num [gv]), nonZero_of_y_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame16 : IsFrame (gv (-1) 0 0 0 0 0) (gv 0 0 0 (-1) 0 (-1)) (gv 0 0 (-1) 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y_im (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame17 : IsFrame (gv (-1) (-1) (-1) 0 0 0) (gv (-1) 0 1 (-1) 0 0) (gv 0 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame18 : IsFrame (gv (-1) (-1) (-1) 0 0 0) (gv 0 (-1) 1 1 0 0) (gv 0 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame19 : IsFrame (gv (-1) (-1) 0 (-1) 0 0) (gv (-1) 0 1 1 0 0) (gv 0 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame20 : IsFrame (gv (-1) (-1) 0 0 (-1) 0) (gv (-1) 0 0 0 1 (-1)) (gv 0 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame21 : IsFrame (gv (-1) (-1) 0 0 (-1) 0) (gv 0 (-1) 0 0 1 1) (gv 0 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame22 : IsFrame (gv (-1) (-1) 0 0 0 (-1)) (gv (-1) 0 0 0 1 1) (gv 0 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame23 : IsFrame (gv (-1) 0 0 0 0 0) (gv 0 0 (-1) (-1) (-1) 0) (gv 0 0 1 0 (-1) 1) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame24 : IsFrame (gv (-1) 0 0 0 0 0) (gv 0 0 (-1) (-1) 0 (-1)) (gv 0 0 1 0 (-1) (-1)) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame25 : IsFrame (gv (-1) 0 0 0 0 0) (gv 0 0 0 (-1) (-1) (-1)) (gv 0 0 (-1) (-1) 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y_im (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame26 : IsFrame (gv (-1) (-1) (-1) 0 (-1) 0) (gv (-1) (-1) 1 0 1 0) (gv 0 0 (-1) 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame27 : IsFrame (gv (-1) (-1) (-1) 0 (-1) 0) (gv (-1) 1 0 (-1) 0 (-1)) (gv 0 0 (-1) 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame28 : IsFrame (gv (-1) (-1) (-1) 0 0 (-1)) (gv (-1) (-1) 1 0 0 1) (gv 0 0 0 1 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame29 : IsFrame (gv (-1) (-1) (-1) 0 0 (-1)) (gv (-1) 1 0 (-1) 1 0) (gv 0 0 0 1 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame30 : IsFrame (gv (-1) 0 (-1) (-1) (-1) 0) (gv (-1) 0 1 1 (-1) 0) (gv (-1) 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame31 : IsFrame (gv (-1) 0 (-1) (-1) (-1) 0) (gv 0 (-1) (-1) 1 0 (-1)) (gv (-1) 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame32 : IsFrame (gv (-1) 0 (-1) (-1) 0 (-1)) (gv (-1) 0 1 1 0 (-1)) (gv 0 1 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame33 : IsFrame (gv (-1) 0 (-1) (-1) 0 (-1)) (gv 0 (-1) (-1) 1 1 0) (gv 0 1 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame34 : IsFrame (gv (-1) 0 (-1) 0 (-1) (-1)) (gv (-1) 0 (-1) 0 1 1) (gv (-1) 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame35 : IsFrame (gv (-1) 0 (-1) 0 (-1) (-1)) (gv 0 (-1) 0 (-1) (-1) 1) (gv (-1) 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame36 : IsFrame (gv (-1) 0 0 (-1) (-1) (-1)) (gv (-1) 0 0 (-1) 1 1) (gv 0 1 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame37 : IsFrame (gv (-1) 0 0 (-1) (-1) (-1)) (gv 0 (-1) 1 0 (-1) 1) (gv 0 1 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame38 : IsFrame (gv (-1) 0 (-1) 0 (-1) 0) (gv (-2) 0 1 0 1 0) (gv 0 0 (-1) 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame39 : IsFrame (gv (-1) 0 (-1) 0 (-1) 0) (gv (-1) 0 (-1) 0 2 0) (gv (-1) 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame40 : IsFrame (gv (-1) 0 (-1) 0 (-1) 0) (gv (-1) 0 2 0 (-1) 0) (gv (-1) 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame41 : IsFrame (gv (-1) 0 (-1) 0 0 (-1)) (gv (-2) 0 1 0 0 1) (gv 0 0 0 1 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame42 : IsFrame (gv (-1) 0 (-1) 0 0 0) (gv (-1) 0 1 0 0 (-2)) (gv 0 1 0 (-1) 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame43 : IsFrame (gv (-1) 0 (-1) 0 0 0) (gv 0 (-1) 0 1 0 (-1)) (gv (-1) 0 1 0 2 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame44 : IsFrame (gv (-1) 0 0 (-1) (-1) 0) (gv (-2) 0 0 1 1 0) (gv 0 0 0 (-1) 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame45 : IsFrame (gv (-1) 0 0 (-1) 0 (-1)) (gv (-2) 0 0 1 0 1) (gv 0 0 (-1) 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame46 : IsFrame (gv (-1) 0 0 (-1) 0 0) (gv (-1) 0 0 1 0 (-2)) (gv 0 1 1 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame47 : IsFrame (gv (-1) 0 0 (-1) 0 0) (gv 0 (-1) (-1) 0 0 (-1)) (gv 0 1 1 0 0 (-2)) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame48 : IsFrame (gv (-1) (-1) (-1) (-1) (-1) 0) (gv (-1) (-1) 0 1 1 (-1)) (gv 1 0 (-1) 1 (-1) (-1)) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame49 : IsFrame (gv (-1) (-1) (-1) (-1) (-1) 0) (gv (-1) (-1) 1 0 1 1) (gv 1 0 (-1) (-1) 1 1) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame50 : IsFrame (gv (-1) (-1) (-1) (-1) (-1) 0) (gv 0 (-1) (-1) 1 1 (-1)) (gv (-1) (-1) 1 0 1 1) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x_im (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame51 : IsFrame (gv (-1) (-1) (-1) (-1) 0 (-1)) (gv (-1) (-1) 0 1 1 1) (gv 1 0 (-1) 1 1 (-1)) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame52 : IsFrame (gv (-1) (-1) (-1) (-1) (-1) 0) (gv (-1) 0 (-1) 0 2 (-2)) (gv (-1) 0 1 0 0 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame53 : IsFrame (gv (-1) (-1) (-1) 0 (-1) (-1)) (gv (-1) 0 2 (-2) (-1) 0) (gv (-1) 0 0 0 1 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame54 : IsFrame (gv (-1) (-1) (-1) 0 0 0) (gv (-1) 0 1 (-1) (-1) 0) (gv 1 0 (-1) 1 (-3) 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame55 : IsFrame (gv (-1) (-1) 0 0 (-1) 0) (gv (-1) 0 (-1) 0 1 (-1)) (gv 1 0 (-3) 0 (-1) 1) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩
theorem frame56 : IsFrame (gv 0 0 (-1) (-1) (-1) 0) (gv (-1) 0 (-1) 0 1 (-1)) (gv (-3) 0 1 0 (-1) 1) :=
  ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

set_option maxHeartbeats 4000000 in
/-- **The residue-modulo-`2` ansatz gives only the constant `1/3`.** -/
theorem mod2_class_function_is_third (f : GVec → ℚ) (col : ℤ → ℤ → ℤ → ℤ → ℤ → ℤ → ℚ)
    (hF : IsFrameFunction f) (hP : Mod2Determined f col)
    (a b c d e g : ℤ) (hne : ¬ ((a + b) % 2 = 0 ∧ (c + d) % 2 = 0 ∧ (e + g) % 2 = 0)) :
    f (gv a b c d e g) = 1 / 3 := by
  have t1 : col 1 0 0 0 0 0 + col 0 0 1 0 0 0 + col 0 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame1
    rw [class_value2 hP (-1) 0 0 0 0 0 1 0 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) 0 0 0 0 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 1 0 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t2 : col 1 0 0 0 0 0 + col 0 0 0 1 0 0 + col 0 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame2
    rw [class_value2 hP (-1) 0 0 0 0 0 1 0 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 (-1) 0 0 0 0 0 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 1 0 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t3 : col 1 0 0 0 0 0 + col 0 0 0 0 0 1 + col 0 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame3
    rw [class_value2 hP (-1) 0 0 0 0 0 1 0 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 0 (-1) 0 0 0 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 1 0 0 0 0 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t4 : col 0 1 0 0 0 0 + col 0 0 1 0 0 0 + col 0 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame4
    rw [class_value2 hP 0 (-1) 0 0 0 0 0 1 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) 0 0 0 0 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 1 0 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t5 : col 1 0 1 0 0 0 + col 1 0 1 0 0 0 + col 0 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame5
    rw [class_value2 hP (-1) 0 (-1) 0 0 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 0 0 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 1 0 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t6 : col 1 0 1 0 0 0 + col 0 1 0 1 0 0 + col 0 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame6
    rw [class_value2 hP (-1) 0 (-1) 0 0 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) 0 1 0 0 0 1 0 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 1 0 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t7 : col 1 0 0 1 0 0 + col 1 0 0 1 0 0 + col 0 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame7
    rw [class_value2 hP (-1) 0 0 (-1) 0 0 1 0 0 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 1 0 0 1 0 0 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 1 0 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t8 : col 1 0 0 1 0 0 + col 0 1 1 0 0 0 + col 0 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame8
    rw [class_value2 hP (-1) 0 0 (-1) 0 0 1 0 0 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) (-1) 0 0 0 0 1 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 1 0 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t9 : col 1 0 0 0 1 0 + col 1 0 0 0 1 0 + col 0 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame9
    rw [class_value2 hP (-1) 0 0 0 (-1) 0 1 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 0 1 0 1 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 1 0 0 0 0 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t10 : col 1 0 0 0 1 0 + col 0 1 0 0 0 1 + col 0 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame10
    rw [class_value2 hP (-1) 0 0 0 (-1) 0 1 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) 0 0 0 1 0 1 0 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 1 0 0 0 0 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t11 : col 1 0 0 0 0 1 + col 1 0 0 0 0 1 + col 0 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame11
    rw [class_value2 hP (-1) 0 0 0 0 (-1) 1 0 0 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 0 0 1 1 0 0 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 1 0 0 0 0 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t12 : col 1 0 0 0 0 1 + col 0 1 0 0 1 0 + col 0 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame12
    rw [class_value2 hP (-1) 0 0 0 0 (-1) 1 0 0 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) 0 0 (-1) 0 0 1 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 1 0 0 0 0 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t13 : col 1 0 0 0 0 0 + col 0 0 1 0 1 0 + col 0 0 1 0 1 0 = 1 := by
    have h := hF _ _ _ frame13
    rw [class_value2 hP (-1) 0 0 0 0 0 1 0 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) 0 (-1) 0 0 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) 0 1 0 0 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t14 : col 1 0 0 0 0 0 + col 0 0 1 0 0 1 + col 0 0 0 1 1 0 = 1 := by
    have h := hF _ _ _ frame14
    rw [class_value2 hP (-1) 0 0 0 0 0 1 0 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) 0 0 (-1) 0 0 1 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 1 1 0 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t15 : col 1 0 0 0 0 0 + col 0 0 0 1 1 0 + col 0 0 0 1 1 0 = 1 := by
    have h := hF _ _ _ frame15
    rw [class_value2 hP (-1) 0 0 0 0 0 1 0 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 (-1) (-1) 0 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 (-1) 1 0 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t16 : col 1 0 0 0 0 0 + col 0 0 0 1 0 1 + col 0 0 1 0 1 0 = 1 := by
    have h := hF _ _ _ frame16
    rw [class_value2 hP (-1) 0 0 0 0 0 1 0 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 (-1) 0 (-1) 0 0 0 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) 0 1 0 0 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t17 : col 1 1 1 0 0 0 + col 1 0 1 1 0 0 + col 0 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame17
    rw [class_value2 hP (-1) (-1) (-1) 0 0 0 1 1 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 (-1) 0 0 1 0 1 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 1 0 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t18 : col 1 1 1 0 0 0 + col 0 1 1 1 0 0 + col 0 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame18
    rw [class_value2 hP (-1) (-1) (-1) 0 0 0 1 1 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) 1 1 0 0 0 1 1 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 1 0 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t19 : col 1 1 0 1 0 0 + col 1 0 1 1 0 0 + col 0 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame19
    rw [class_value2 hP (-1) (-1) 0 (-1) 0 0 1 1 0 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 1 0 0 1 0 1 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 0 1 0 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t20 : col 1 1 0 0 1 0 + col 1 0 0 0 1 1 + col 0 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame20
    rw [class_value2 hP (-1) (-1) 0 0 (-1) 0 1 1 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 0 1 (-1) 1 0 0 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 1 0 0 0 0 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t21 : col 1 1 0 0 1 0 + col 0 1 0 0 1 1 + col 0 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame21
    rw [class_value2 hP (-1) (-1) 0 0 (-1) 0 1 1 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) 0 0 1 1 0 1 0 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 1 0 0 0 0 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t22 : col 1 1 0 0 0 1 + col 1 0 0 0 1 1 + col 0 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame22
    rw [class_value2 hP (-1) (-1) 0 0 0 (-1) 1 1 0 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 0 1 1 1 0 0 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 1 0 0 0 0 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t23 : col 1 0 0 0 0 0 + col 0 0 1 1 1 0 + col 0 0 1 0 1 1 = 1 := by
    have h := hF _ _ _ frame23
    rw [class_value2 hP (-1) 0 0 0 0 0 1 0 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) (-1) (-1) 0 0 0 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 1 0 (-1) 1 0 0 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t24 : col 1 0 0 0 0 0 + col 0 0 1 1 0 1 + col 0 0 1 0 1 1 = 1 := by
    have h := hF _ _ _ frame24
    rw [class_value2 hP (-1) 0 0 0 0 0 1 0 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) (-1) 0 (-1) 0 0 1 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 1 0 (-1) (-1) 0 0 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t25 : col 1 0 0 0 0 0 + col 0 0 0 1 1 1 + col 0 0 1 1 1 0 = 1 := by
    have h := hF _ _ _ frame25
    rw [class_value2 hP (-1) 0 0 0 0 0 1 0 0 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 (-1) (-1) (-1) 0 0 0 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) (-1) 1 0 0 0 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t26 : col 1 1 1 0 1 0 + col 1 1 1 0 1 0 + col 0 0 1 0 1 0 = 1 := by
    have h := hF _ _ _ frame26
    rw [class_value2 hP (-1) (-1) (-1) 0 (-1) 0 1 1 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) (-1) 1 0 1 0 1 1 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) 0 1 0 0 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t27 : col 1 1 1 0 1 0 + col 1 1 0 1 0 1 + col 0 0 1 0 1 0 = 1 := by
    have h := hF _ _ _ frame27
    rw [class_value2 hP (-1) (-1) (-1) 0 (-1) 0 1 1 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 1 0 (-1) 0 (-1) 1 1 0 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) 0 1 0 0 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t28 : col 1 1 1 0 0 1 + col 1 1 1 0 0 1 + col 0 0 0 1 1 0 = 1 := by
    have h := hF _ _ _ frame28
    rw [class_value2 hP (-1) (-1) (-1) 0 0 (-1) 1 1 1 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) (-1) 1 0 0 1 1 1 1 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 1 1 0 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t29 : col 1 1 1 0 0 1 + col 1 1 0 1 1 0 + col 0 0 0 1 1 0 = 1 := by
    have h := hF _ _ _ frame29
    rw [class_value2 hP (-1) (-1) (-1) 0 0 (-1) 1 1 1 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 1 0 (-1) 1 0 1 1 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 1 1 0 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t30 : col 1 0 1 1 1 0 + col 1 0 1 1 1 0 + col 1 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame30
    rw [class_value2 hP (-1) 0 (-1) (-1) (-1) 0 1 0 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 1 (-1) 0 1 0 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 0 1 0 1 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t31 : col 1 0 1 1 1 0 + col 0 1 1 1 0 1 + col 1 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame31
    rw [class_value2 hP (-1) 0 (-1) (-1) (-1) 0 1 0 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) (-1) 1 0 (-1) 0 1 1 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 0 1 0 1 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t32 : col 1 0 1 1 0 1 + col 1 0 1 1 0 1 + col 0 1 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame32
    rw [class_value2 hP (-1) 0 (-1) (-1) 0 (-1) 1 0 1 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 1 0 (-1) 1 0 1 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 1 0 0 1 0 0 1 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t33 : col 1 0 1 1 0 1 + col 0 1 1 1 1 0 + col 0 1 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame33
    rw [class_value2 hP (-1) 0 (-1) (-1) 0 (-1) 1 0 1 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) (-1) 1 1 0 0 1 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 1 0 0 1 0 0 1 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t34 : col 1 0 1 0 1 1 + col 1 0 1 0 1 1 + col 1 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame34
    rw [class_value2 hP (-1) 0 (-1) 0 (-1) (-1) 1 0 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 (-1) 0 1 1 1 0 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 0 0 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t35 : col 1 0 1 0 1 1 + col 0 1 0 1 1 1 + col 1 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame35
    rw [class_value2 hP (-1) 0 (-1) 0 (-1) (-1) 1 0 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) 0 (-1) (-1) 1 0 1 0 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 0 0 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t36 : col 1 0 0 1 1 1 + col 1 0 0 1 1 1 + col 0 1 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame36
    rw [class_value2 hP (-1) 0 0 (-1) (-1) (-1) 1 0 0 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 (-1) 1 1 1 0 0 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 1 1 0 0 0 0 1 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t37 : col 1 0 0 1 1 1 + col 0 1 1 0 1 1 + col 0 1 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame37
    rw [class_value2 hP (-1) 0 0 (-1) (-1) (-1) 1 0 0 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) 1 0 (-1) 1 0 1 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 1 1 0 0 0 0 1 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t38 : col 1 0 1 0 1 0 + col 0 0 1 0 1 0 + col 0 0 1 0 1 0 = 1 := by
    have h := hF _ _ _ frame38
    rw [class_value2 hP (-1) 0 (-1) 0 (-1) 0 1 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-2) 0 1 0 1 0 0 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) 0 1 0 0 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t39 : col 1 0 1 0 1 0 + col 1 0 1 0 0 0 + col 1 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame39
    rw [class_value2 hP (-1) 0 (-1) 0 (-1) 0 1 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 (-1) 0 2 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 0 0 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t40 : col 1 0 1 0 1 0 + col 1 0 0 0 1 0 + col 1 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame40
    rw [class_value2 hP (-1) 0 (-1) 0 (-1) 0 1 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 2 0 (-1) 0 1 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 0 1 0 1 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t41 : col 1 0 1 0 0 1 + col 0 0 1 0 0 1 + col 0 0 0 1 1 0 = 1 := by
    have h := hF _ _ _ frame41
    rw [class_value2 hP (-1) 0 (-1) 0 0 (-1) 1 0 1 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-2) 0 1 0 0 1 0 0 1 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 1 1 0 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t42 : col 1 0 1 0 0 0 + col 1 0 1 0 0 0 + col 0 1 0 1 1 0 = 1 := by
    have h := hF _ _ _ frame42
    rw [class_value2 hP (-1) 0 (-1) 0 0 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 0 0 (-2) 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 1 0 (-1) 1 0 0 1 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t43 : col 1 0 1 0 0 0 + col 0 1 0 1 0 1 + col 1 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame43
    rw [class_value2 hP (-1) 0 (-1) 0 0 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) 0 1 0 (-1) 0 1 0 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 0 2 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t44 : col 1 0 0 1 1 0 + col 0 0 0 1 1 0 + col 0 0 0 1 1 0 = 1 := by
    have h := hF _ _ _ frame44
    rw [class_value2 hP (-1) 0 0 (-1) (-1) 0 1 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-2) 0 0 1 1 0 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 0 (-1) 1 0 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t45 : col 1 0 0 1 0 1 + col 0 0 0 1 0 1 + col 0 0 1 0 1 0 = 1 := by
    have h := hF _ _ _ frame45
    rw [class_value2 hP (-1) 0 0 (-1) 0 (-1) 1 0 0 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-2) 0 0 1 0 1 0 0 0 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 0 (-1) 0 1 0 0 0 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t46 : col 1 0 0 1 0 0 + col 1 0 0 1 0 0 + col 0 1 1 0 1 0 = 1 := by
    have h := hF _ _ _ frame46
    rw [class_value2 hP (-1) 0 0 (-1) 0 0 1 0 0 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 1 0 (-2) 1 0 0 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 1 1 0 1 0 0 1 1 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t47 : col 1 0 0 1 0 0 + col 0 1 1 0 0 1 + col 0 1 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame47
    rw [class_value2 hP (-1) 0 0 (-1) 0 0 1 0 0 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) (-1) 0 0 (-1) 0 1 1 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 1 1 0 0 (-2) 0 1 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t48 : col 1 1 1 1 1 0 + col 1 1 0 1 1 1 + col 1 0 1 1 1 1 = 1 := by
    have h := hF _ _ _ frame48
    rw [class_value2 hP (-1) (-1) (-1) (-1) (-1) 0 1 1 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) (-1) 0 1 1 (-1) 1 1 0 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 1 0 (-1) 1 (-1) (-1) 1 0 1 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t49 : col 1 1 1 1 1 0 + col 1 1 1 0 1 1 + col 1 0 1 1 1 1 = 1 := by
    have h := hF _ _ _ frame49
    rw [class_value2 hP (-1) (-1) (-1) (-1) (-1) 0 1 1 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) (-1) 1 0 1 1 1 1 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 1 0 (-1) (-1) 1 1 1 0 1 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t50 : col 1 1 1 1 1 0 + col 0 1 1 1 1 1 + col 1 1 1 0 1 1 = 1 := by
    have h := hF _ _ _ frame50
    rw [class_value2 hP (-1) (-1) (-1) (-1) (-1) 0 1 1 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 0 (-1) (-1) 1 1 (-1) 0 1 1 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) (-1) 1 0 1 1 1 1 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t51 : col 1 1 1 1 0 1 + col 1 1 0 1 1 1 + col 1 0 1 1 1 1 = 1 := by
    have h := hF _ _ _ frame51
    rw [class_value2 hP (-1) (-1) (-1) (-1) 0 (-1) 1 1 1 1 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) (-1) 0 1 1 1 1 1 0 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 1 0 (-1) 1 1 (-1) 1 0 1 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t52 : col 1 1 1 1 1 0 + col 1 0 1 0 0 0 + col 1 0 1 0 0 0 = 1 := by
    have h := hF _ _ _ frame52
    rw [class_value2 hP (-1) (-1) (-1) (-1) (-1) 0 1 1 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 (-1) 0 2 (-2) 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 0 0 0 1 0 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t53 : col 1 1 1 0 1 1 + col 1 0 0 0 1 0 + col 1 0 0 0 1 0 = 1 := by
    have h := hF _ _ _ frame53
    rw [class_value2 hP (-1) (-1) (-1) 0 (-1) (-1) 1 1 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 2 (-2) (-1) 0 1 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 0 0 1 0 1 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t54 : col 1 1 1 0 0 0 + col 1 0 1 1 1 0 + col 1 0 1 1 1 0 = 1 := by
    have h := hF _ _ _ frame54
    rw [class_value2 hP (-1) (-1) (-1) 0 0 0 1 1 1 0 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 1 (-1) (-1) 0 1 0 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 1 0 (-1) 1 (-3) 0 1 0 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t55 : col 1 1 0 0 1 0 + col 1 0 1 0 1 1 + col 1 0 1 0 1 1 = 1 := by
    have h := hF _ _ _ frame55
    rw [class_value2 hP (-1) (-1) 0 0 (-1) 0 1 1 0 0 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 (-1) 0 1 (-1) 1 0 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP 1 0 (-3) 0 (-1) 1 1 0 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have t56 : col 0 0 1 1 1 0 + col 1 0 1 0 1 1 + col 1 0 1 0 1 1 = 1 := by
    have h := hF _ _ _ frame56
    rw [class_value2 hP 0 0 (-1) (-1) (-1) 0 0 0 1 1 1 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-1) 0 (-1) 0 1 (-1) 1 0 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide), class_value2 hP (-3) 0 1 0 (-1) 1 1 0 1 0 1 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)] at h
    exact h
  have k1 : col 0 0 0 0 0 1 = 1 / 3 := by
    linear_combination (-2 / 3 : ℚ) * t1 + (1 : ℚ) * t3 + (2 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40
  have k2 : col 0 0 0 0 1 0 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (2 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40
  have k3 : col 0 0 0 1 0 0 = 1 / 3 := by
    linear_combination (-2 / 3 : ℚ) * t1 + (1 : ℚ) * t2 + (-1 / 3 : ℚ) * t5 + (2 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-2 / 3 : ℚ) * t40
  have k4 : col 0 0 0 1 0 1 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (-5 / 6 : ℚ) * t13 + (1 : ℚ) * t16 + (1 / 3 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k5 : col 0 0 0 1 1 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 2 : ℚ) * t15 + (1 / 3 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k6 : col 0 0 0 1 1 1 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (-5 / 6 : ℚ) * t13 + (1 : ℚ) * t25 + (1 : ℚ) * t34 + (5 / 6 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (-1 / 6 : ℚ) * t40 + (-1 : ℚ) * t56
  have k7 : col 0 0 1 0 0 0 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (2 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-2 / 3 : ℚ) * t40
  have k8 : col 0 0 1 0 0 1 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 : ℚ) * t14 + (-1 / 2 : ℚ) * t15 + (1 / 3 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k9 : col 0 0 1 0 1 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k10 : col 0 0 1 0 1 1 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (-5 / 6 : ℚ) * t13 + (1 : ℚ) * t23 + (1 : ℚ) * t34 + (5 / 6 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (-1 / 6 : ℚ) * t40 + (-1 : ℚ) * t56
  have k11 : col 0 0 1 1 0 1 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 : ℚ) * t23 + (1 : ℚ) * t24 + (-1 : ℚ) * t34 + (-1 / 6 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-1 / 6 : ℚ) * t40 + (1 : ℚ) * t56
  have k12 : col 0 0 1 1 1 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 : ℚ) * t34 + (-1 / 6 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-1 / 6 : ℚ) * t40 + (1 : ℚ) * t56
  have k13 : col 0 1 0 0 0 0 = 1 / 3 := by
    linear_combination (-2 / 3 : ℚ) * t1 + (1 : ℚ) * t4 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (2 / 3 : ℚ) * t13 + (-2 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40
  have k14 : col 0 1 0 0 0 1 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (-5 / 6 : ℚ) * t9 + (1 : ℚ) * t10 + (1 / 6 : ℚ) * t13 + (-1 / 6 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (1 / 3 : ℚ) * t40
  have k15 : col 0 1 0 0 1 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (-1 / 2 : ℚ) * t11 + (1 : ℚ) * t12 + (1 / 6 : ℚ) * t13 + (-1 / 6 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (1 / 3 : ℚ) * t40
  have k16 : col 0 1 0 0 1 1 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (-5 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (1 : ℚ) * t21 + (1 : ℚ) * t34 + (-1 / 6 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (5 / 6 : ℚ) * t40 + (-1 : ℚ) * t55
  have k17 : col 0 1 0 1 0 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (-5 / 6 : ℚ) * t5 + (1 : ℚ) * t6 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 / 6 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k18 : col 0 1 0 1 0 1 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t43
  have k19 : col 0 1 0 1 1 0 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t42
  have k20 : col 0 1 0 1 1 1 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (-1 / 12 : ℚ) * t5 + (-1 / 12 : ℚ) * t9 + (-1 / 12 : ℚ) * t13 + (-1 / 2 : ℚ) * t34 + (1 : ℚ) * t35 + (1 / 12 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (1 / 12 : ℚ) * t40
  have k21 : col 0 1 1 0 0 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 2 : ℚ) * t7 + (1 : ℚ) * t8 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 / 6 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k22 : col 0 1 1 0 0 1 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (2 / 3 : ℚ) * t5 + (-1 : ℚ) * t8 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t47
  have k23 : col 0 1 1 0 1 0 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (2 / 3 : ℚ) * t5 + (-1 : ℚ) * t7 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t46
  have k24 : col 0 1 1 0 1 1 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 4 : ℚ) * t7 + (-1 / 2 : ℚ) * t8 + (-1 / 12 : ℚ) * t9 + (-1 / 12 : ℚ) * t13 + (-1 / 2 : ℚ) * t36 + (1 : ℚ) * t37 + (1 / 12 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (1 / 12 : ℚ) * t40
  have k25 : col 0 1 1 1 0 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (-5 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (1 : ℚ) * t18 + (1 : ℚ) * t30 + (-1 / 6 : ℚ) * t38 + (5 / 6 : ℚ) * t39 + (-2 / 3 : ℚ) * t40 + (-1 : ℚ) * t54
  have k26 : col 0 1 1 1 0 1 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (-1 / 12 : ℚ) * t5 + (-1 / 12 : ℚ) * t9 + (-1 / 12 : ℚ) * t13 + (-1 / 2 : ℚ) * t30 + (1 : ℚ) * t31 + (1 / 12 : ℚ) * t38 + (1 / 12 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k27 : col 0 1 1 1 1 0 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (-1 / 12 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 4 : ℚ) * t11 + (-1 / 2 : ℚ) * t12 + (-1 / 12 : ℚ) * t13 + (-1 / 2 : ℚ) * t32 + (1 : ℚ) * t33 + (1 / 12 : ℚ) * t38 + (1 / 12 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k28 : col 0 1 1 1 1 1 = 1 / 3 := by
    linear_combination (-2 / 3 : ℚ) * t1 + (2 / 3 : ℚ) * t5 + (2 / 3 : ℚ) * t9 + (2 / 3 : ℚ) * t13 + (-2 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t50 + (-1 : ℚ) * t52 + (-1 : ℚ) * t53
  have k29 : col 1 0 0 0 0 0 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (2 / 3 : ℚ) * t13 + (-2 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40
  have k30 : col 1 0 0 0 0 1 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (1 / 2 : ℚ) * t11 + (1 / 6 : ℚ) * t13 + (-1 / 6 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (1 / 3 : ℚ) * t40
  have k31 : col 1 0 0 0 1 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 / 6 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (1 / 3 : ℚ) * t40
  have k32 : col 1 0 0 0 1 1 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (-5 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (1 : ℚ) * t20 + (1 : ℚ) * t34 + (-1 / 6 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (5 / 6 : ℚ) * t40 + (-1 : ℚ) * t55
  have k33 : col 1 0 0 1 0 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (1 / 2 : ℚ) * t7 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 / 6 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k34 : col 1 0 0 1 0 1 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (2 / 3 : ℚ) * t13 + (-1 : ℚ) * t16 + (-2 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t45
  have k35 : col 1 0 0 1 1 0 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (2 / 3 : ℚ) * t13 + (-1 : ℚ) * t15 + (-2 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t44
  have k36 : col 1 0 0 1 1 1 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 4 : ℚ) * t7 + (-1 / 2 : ℚ) * t8 + (-1 / 12 : ℚ) * t9 + (-1 / 12 : ℚ) * t13 + (1 / 2 : ℚ) * t36 + (1 / 12 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (1 / 12 : ℚ) * t40
  have k37 : col 1 0 1 0 0 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 / 6 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k38 : col 1 0 1 0 0 1 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (2 / 3 : ℚ) * t13 + (-1 : ℚ) * t14 + (-2 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t41
  have k39 : col 1 0 1 0 1 0 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40
  have k40 : col 1 0 1 0 1 1 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (-1 / 12 : ℚ) * t5 + (-1 / 12 : ℚ) * t9 + (-1 / 12 : ℚ) * t13 + (1 / 2 : ℚ) * t34 + (1 / 12 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (1 / 12 : ℚ) * t40
  have k41 : col 1 0 1 1 0 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (-5 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (1 : ℚ) * t17 + (1 : ℚ) * t30 + (-1 / 6 : ℚ) * t38 + (5 / 6 : ℚ) * t39 + (-2 / 3 : ℚ) * t40 + (-1 : ℚ) * t54
  have k42 : col 1 0 1 1 0 1 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (-1 / 12 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 4 : ℚ) * t11 + (-1 / 2 : ℚ) * t12 + (-1 / 12 : ℚ) * t13 + (1 / 2 : ℚ) * t32 + (1 / 12 : ℚ) * t38 + (1 / 12 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k43 : col 1 0 1 1 1 0 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (-1 / 12 : ℚ) * t5 + (-1 / 12 : ℚ) * t9 + (-1 / 12 : ℚ) * t13 + (1 / 2 : ℚ) * t30 + (1 / 12 : ℚ) * t38 + (1 / 12 : ℚ) * t39 + (-1 / 6 : ℚ) * t40
  have k44 : col 1 0 1 1 1 1 = 1 / 3 := by
    linear_combination (-2 / 3 : ℚ) * t1 + (2 / 3 : ℚ) * t5 + (2 / 3 : ℚ) * t9 + (2 / 3 : ℚ) * t13 + (-2 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t49 + (-1 : ℚ) * t52 + (-1 : ℚ) * t53
  have k45 : col 1 1 0 0 0 1 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 : ℚ) * t20 + (1 : ℚ) * t22 + (-1 : ℚ) * t34 + (-1 / 6 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-1 / 6 : ℚ) * t40 + (1 : ℚ) * t55
  have k46 : col 1 1 0 0 1 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 : ℚ) * t34 + (-1 / 6 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-1 / 6 : ℚ) * t40 + (1 : ℚ) * t55
  have k47 : col 1 1 0 1 0 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 : ℚ) * t17 + (1 : ℚ) * t19 + (-1 : ℚ) * t30 + (-1 / 6 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t54
  have k48 : col 1 1 0 1 0 1 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (-1 / 12 : ℚ) * t5 + (-1 / 12 : ℚ) * t9 + (-1 / 12 : ℚ) * t13 + (-1 / 2 : ℚ) * t26 + (1 : ℚ) * t27 + (-1 / 6 : ℚ) * t38 + (1 / 12 : ℚ) * t39 + (1 / 12 : ℚ) * t40
  have k49 : col 1 1 0 1 1 0 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (-1 / 12 : ℚ) * t5 + (-1 / 12 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 / 4 : ℚ) * t15 + (-1 / 2 : ℚ) * t28 + (1 : ℚ) * t29 + (-1 / 6 : ℚ) * t38 + (1 / 12 : ℚ) * t39 + (1 / 12 : ℚ) * t40
  have k50 : col 1 1 0 1 1 1 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-2 / 3 : ℚ) * t40 + (1 : ℚ) * t48 + (-1 : ℚ) * t49 + (1 : ℚ) * t53
  have k51 : col 1 1 1 0 0 0 = 1 / 3 := by
    linear_combination (-1 / 6 : ℚ) * t1 + (1 / 6 : ℚ) * t5 + (1 / 6 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 : ℚ) * t30 + (-1 / 6 : ℚ) * t38 + (-1 / 6 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t54
  have k52 : col 1 1 1 0 0 1 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (-1 / 12 : ℚ) * t5 + (-1 / 12 : ℚ) * t9 + (1 / 6 : ℚ) * t13 + (-1 / 4 : ℚ) * t15 + (1 / 2 : ℚ) * t28 + (-1 / 6 : ℚ) * t38 + (1 / 12 : ℚ) * t39 + (1 / 12 : ℚ) * t40
  have k53 : col 1 1 1 0 1 0 = 1 / 3 := by
    linear_combination (1 / 12 : ℚ) * t1 + (-1 / 12 : ℚ) * t5 + (-1 / 12 : ℚ) * t9 + (-1 / 12 : ℚ) * t13 + (1 / 2 : ℚ) * t26 + (-1 / 6 : ℚ) * t38 + (1 / 12 : ℚ) * t39 + (1 / 12 : ℚ) * t40
  have k54 : col 1 1 1 0 1 1 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (1 / 3 : ℚ) * t39 + (-2 / 3 : ℚ) * t40 + (1 : ℚ) * t53
  have k55 : col 1 1 1 1 0 1 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (-1 : ℚ) * t48 + (1 : ℚ) * t51 + (1 : ℚ) * t52
  have k56 : col 1 1 1 1 1 0 = 1 / 3 := by
    linear_combination (1 / 3 : ℚ) * t1 + (-1 / 3 : ℚ) * t5 + (-1 / 3 : ℚ) * t9 + (-1 / 3 : ℚ) * t13 + (1 / 3 : ℚ) * t38 + (-2 / 3 : ℚ) * t39 + (1 / 3 : ℚ) * t40 + (1 : ℚ) * t52
  rw [hP a b c d e g hne]
  have ha : a % 2 = 0 ∨ a % 2 = 1 := by omega
  have hb : b % 2 = 0 ∨ b % 2 = 1 := by omega
  have hc : c % 2 = 0 ∨ c % 2 = 1 := by omega
  have hd : d % 2 = 0 ∨ d % 2 = 1 := by omega
  have he : e % 2 = 0 ∨ e % 2 = 1 := by omega
  have hg : g % 2 = 0 ∨ g % 2 = 1 := by omega
  rcases ha with ha | ha <;> rcases hb with hb | hb <;> rcases hc with hc | hc <;>
    rcases hd with hd | hd <;> rcases he with he | he <;> rcases hg with hg | hg <;>
    simp only [ha, hb, hc, hd, he, hg] <;>
    first
    | exact absurd (by omega) hne
    | exact k1
    | exact k2
    | exact k3
    | exact k4
    | exact k5
    | exact k6
    | exact k7
    | exact k8
    | exact k9
    | exact k10
    | exact k11
    | exact k12
    | exact k13
    | exact k14
    | exact k15
    | exact k16
    | exact k17
    | exact k18
    | exact k19
    | exact k20
    | exact k21
    | exact k22
    | exact k23
    | exact k24
    | exact k25
    | exact k26
    | exact k27
    | exact k28
    | exact k29
    | exact k30
    | exact k31
    | exact k32
    | exact k33
    | exact k34
    | exact k35
    | exact k36
    | exact k37
    | exact k38
    | exact k39
    | exact k40
    | exact k41
    | exact k42
    | exact k43
    | exact k44
    | exact k45
    | exact k46
    | exact k47
    | exact k48
    | exact k49
    | exact k50
    | exact k51
    | exact k52
    | exact k53
    | exact k54
    | exact k55
    | exact k56

end BornFable.GaussianFrames

#print axioms BornFable.GaussianFrames.class_value2
#print axioms BornFable.GaussianFrames.mod2_class_function_is_third
