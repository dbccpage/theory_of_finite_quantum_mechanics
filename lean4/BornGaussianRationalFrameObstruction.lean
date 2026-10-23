import BornGaussRat
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Frame functions on `ℚ(i)³`: the `(1+i)`-parity route is closed

AuthorityEffect: None.

Setting.  `GVec` is `K³` for `K = ℚ(i)` (`BornFable.GaussRat`), with the Hermitian form
`inner u v = Σ conj(uₖ) vₖ`.  A frame is a triple of nonzero pairwise orthogonal vectors; a frame
function is `f : GVec → ℚ` summing to `1` on every frame.  (`BornGaussianFrameRays` shows such an
`f` is automatically constant on rays.)

For a Gaussian integer `a + b i`, `(1+i) ∣ a + b i ⇔ a ≡ b (mod 2)`; the `(1+i)`-parity class of a
Gaussian-integer vector `gv a b c d e g = (a+bi, c+di, e+gi)` is `((a+b)%2, (c+d)%2, (e+g)%2)`.

Main results:
* `frame_tri_110` (and `frame_tri_101`, `frame_tri_011`): the non-real orthogonal frame
  `(1,1,0), (1,-1,1+i), (1,-1,-1-i)` all of whose members lie in the parity class `(1,1,0)`.
  (A claim that no such frame exists over `ℤ³` was made in a companion file,
  `BornRationalPlaneObstruction`, that failed to compile and is not part of this build; it is
  neither used nor established here.)
* `parity_class_function_is_third`: a frame function on `K³` whose value on every Gaussian-integer
  vector not divisible by `1+i` depends only on the parity class is `1/3` on all of those vectors
  (`1/3` is the value of the Born function of `ρ = I/3`; that is not a theorem here).  So a frame
  function of this `(1+i)`-parity form is not a non-quadratic one.  Parity-type constructions
  with other classes (for example residues modulo `2`) are not covered.

This file does **not** decide whether every frame function on `ℚ(i)³` rays is quadratic.
Nothing here is a statement about physics.
-/

namespace BornFable.GaussianFrames

open BornFable

/-- A vector in `K³`, `K = ℚ(i)`. -/
structure GVec where
  x : GaussRat
  y : GaussRat
  z : GaussRat

namespace GVec

/-- The Hermitian inner product `⟨u, v⟩ = Σ conj(uₖ) vₖ` (conjugate-linear in `u`). -/
def inner (u v : GVec) : GaussRat := star u.x * v.x + star u.y * v.y + star u.z * v.z

/-- `v ≠ 0`. -/
def NonZero (v : GVec) : Prop := v.x ≠ 0 ∨ v.y ≠ 0 ∨ v.z ≠ 0

/-- Scalar multiplication. -/
def smul (l : GaussRat) (v : GVec) : GVec := ⟨l * v.x, l * v.y, l * v.z⟩

end GVec

/-- An orthogonal frame: three nonzero pairwise orthogonal vectors. -/
def IsFrame (u v w : GVec) : Prop :=
  u.NonZero ∧ v.NonZero ∧ w.NonZero ∧ u.inner v = 0 ∧ u.inner w = 0 ∧ v.inner w = 0

/-- A frame function: sums to `1` on every orthogonal frame. -/
def IsFrameFunction (f : GVec → ℚ) : Prop :=
  ∀ u v w : GVec, IsFrame u v w → f u + f v + f w = 1

/-- The Gaussian-integer vector `(a + b i, c + d i, e + g i)`. -/
def gv (a b c d e g : ℤ) : GVec :=
  ⟨⟨(a : ℚ), (b : ℚ)⟩, ⟨(c : ℚ), (d : ℚ)⟩, ⟨(e : ℚ), (g : ℚ)⟩⟩

/-- `f` is determined by the `(1+i)`-parity class on `(1+i)`-primitive Gaussian-integer
vectors: there is `col` with `f (gv a b c d e g) = col ((a+b)%2) ((c+d)%2) ((e+g)%2)` whenever
not all three components are divisible by `1 + i`. -/
def ParityDetermined (f : GVec → ℚ) (col : ℤ → ℤ → ℤ → ℚ) : Prop :=
  ∀ a b c d e g : ℤ, ¬ ((a + b) % 2 = 0 ∧ (c + d) % 2 = 0 ∧ (e + g) % 2 = 0) →
    f (gv a b c d e g) = col ((a + b) % 2) ((c + d) % 2) ((e + g) % 2)

/-! ### Nonzero-ness helpers -/

theorem nonZero_of_x {v : GVec} (h : v.x.re ≠ 0) : v.NonZero :=
  Or.inl fun e => h (by simp [e])

theorem nonZero_of_y {v : GVec} (h : v.y.re ≠ 0) : v.NonZero :=
  Or.inr (Or.inl fun e => h (by simp [e]))

theorem nonZero_of_z {v : GVec} (h : v.z.re ≠ 0) : v.NonZero :=
  Or.inr (Or.inr fun e => h (by simp [e]))

/-- Verify an explicit Gaussian-rational inner-product identity componentwise. -/
macro "gauss_arith" : tactic =>
  `(tactic| first
      | (ext <;> simp [GVec.inner, gv] <;> norm_num)
      | norm_num [GVec.inner, gv, GaussRat.ext_iff])

/-! ### Seven explicit frames -/

/-- Real frame `e₃, (1,1,0), (1,-1,0)`. -/
theorem frame_e3_110 : IsFrame (gv 0 0 0 0 1 0) (gv 1 0 1 0 0 0) (gv 1 0 (-1) 0 0 0) :=
  ⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- Real frame `e₁, (0,1,1), (0,1,-1)`. -/
theorem frame_e1_011 : IsFrame (gv 1 0 0 0 0 0) (gv 0 0 1 0 1 0) (gv 0 0 1 0 (-1) 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]),
    nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- Real frame `e₂, (1,0,1), (1,0,-1)`. -/
theorem frame_e2_101 : IsFrame (gv 0 0 1 0 0 0) (gv 1 0 0 0 1 0) (gv 1 0 0 0 (-1) 0) :=
  ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- Real frame `(1,1,1), (1,-1,0), (1,1,-2)`. -/
theorem frame_111_110 : IsFrame (gv 1 0 1 0 1 0) (gv 1 0 (-1) 0 0 0) (gv 1 0 1 0 (-2) 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- The non-real triangle `(1,1,0), (1,-1,1+i), (1,-1,-1-i)`: all three members have
`(1+i)`-parity class `(1,1,0)`. -/
theorem frame_tri_110 :
    IsFrame (gv 1 0 1 0 0 0) (gv 1 0 (-1) 0 1 1) (gv 1 0 (-1) 0 (-1) (-1)) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- The permuted triangle `(1,0,1), (1,1+i,-1), (1,-1-i,-1)`, class `(1,0,1)`. -/
theorem frame_tri_101 :
    IsFrame (gv 1 0 0 0 1 0) (gv 1 0 1 1 (-1) 0) (gv 1 0 (-1) (-1) (-1) 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- The permuted triangle `(0,1,1), (1+i,1,-1), (-1-i,1,-1)`, class `(0,1,1)`. -/
theorem frame_tri_011 :
    IsFrame (gv 0 0 1 0 1 0) (gv 1 1 1 0 (-1) 0) (gv (-1) (-1) 1 0 (-1) 0) :=
  ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-! ### The parity route is closed -/

/-- Class value of an explicit Gaussian-integer vector, in normalised form. -/
theorem class_value {f : GVec → ℚ} {col : ℤ → ℤ → ℤ → ℚ} (hP : ParityDetermined f col)
    (a b c d e g p q r : ℤ)
    (hne : ¬ ((a + b) % 2 = 0 ∧ (c + d) % 2 = 0 ∧ (e + g) % 2 = 0))
    (h1 : (a + b) % 2 = p) (h2 : (c + d) % 2 = q) (h3 : (e + g) % 2 = r) :
    f (gv a b c d e g) = col p q r := by
  rw [hP a b c d e g hne, h1, h2, h3]

/-- **The `(1+i)`-parity ansatz gives only the constant `1/3`.**  A frame function on `K³` whose
values on Gaussian-integer vectors not divisible by `1+i` depend only on the class
`((a+b)%2, (c+d)%2, (e+g)%2)` equals `1/3` on all such vectors.  This does not cover other parity
classes, and it is not stated for vectors outside this domain. -/
theorem parity_class_function_is_third (f : GVec → ℚ) (col : ℤ → ℤ → ℤ → ℚ)
    (hF : IsFrameFunction f) (hP : ParityDetermined f col)
    (a b c d e g : ℤ) (hne : ¬ ((a + b) % 2 = 0 ∧ (c + d) % 2 = 0 ∧ (e + g) % 2 = 0)) :
    f (gv a b c d e g) = 1 / 3 := by
  -- class values of the seventeen explicit vectors
  have k100 := class_value hP 1 0 0 0 0 0 1 0 0 (by decide) (by decide) (by decide) (by decide)
  have k010 := class_value hP 0 0 1 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide)
  have k001 := class_value hP 0 0 0 0 1 0 0 0 1 (by decide) (by decide) (by decide) (by decide)
  have kP := class_value hP 1 0 1 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide)
  have kM := class_value hP 1 0 (-1) 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide)
  have kQ := class_value hP 0 0 1 0 1 0 0 1 1 (by decide) (by decide) (by decide) (by decide)
  have kQm := class_value hP 0 0 1 0 (-1) 0 0 1 1 (by decide) (by decide) (by decide) (by decide)
  have kR := class_value hP 1 0 0 0 1 0 1 0 1 (by decide) (by decide) (by decide) (by decide)
  have kRm := class_value hP 1 0 0 0 (-1) 0 1 0 1 (by decide) (by decide) (by decide) (by decide)
  have kT := class_value hP 1 0 1 0 1 0 1 1 1 (by decide) (by decide) (by decide) (by decide)
  have kS := class_value hP 1 0 1 0 (-2) 0 1 1 0 (by decide) (by decide) (by decide) (by decide)
  have kA := class_value hP 1 0 (-1) 0 1 1 1 1 0 (by decide) (by decide) (by decide) (by decide)
  have kB := class_value hP 1 0 (-1) 0 (-1) (-1) 1 1 0
    (by decide) (by decide) (by decide) (by decide)
  have kC := class_value hP 1 0 1 1 (-1) 0 1 0 1 (by decide) (by decide) (by decide) (by decide)
  have kD := class_value hP 1 0 (-1) (-1) (-1) 0 1 0 1
    (by decide) (by decide) (by decide) (by decide)
  have kF := class_value hP 1 1 1 0 (-1) 0 0 1 1 (by decide) (by decide) (by decide) (by decide)
  have kG := class_value hP (-1) (-1) 1 0 (-1) 0 0 1 1
    (by decide) (by decide) (by decide) (by decide)
  -- the seven frame equations
  have t1 := hF _ _ _ frame_e3_110
  have t2 := hF _ _ _ frame_e1_011
  have t3 := hF _ _ _ frame_e2_101
  have t4 := hF _ _ _ frame_111_110
  have t5 := hF _ _ _ frame_tri_110
  have t6 := hF _ _ _ frame_tri_101
  have t7 := hF _ _ _ frame_tri_011
  -- the class of the given vector is one of the seven nonzero ones
  have ha : (a + b) % 2 = 0 ∨ (a + b) % 2 = 1 := by omega
  have hc : (c + d) % 2 = 0 ∨ (c + d) % 2 = 1 := by omega
  have he : (e + g) % 2 = 0 ∨ (e + g) % 2 = 1 := by omega
  rcases ha with ha | ha <;> rcases hc with hc | hc <;> rcases he with he | he <;>
    first
    | exact absurd (And.intro ha (And.intro hc he)) hne
    | (have key := class_value hP a b c d e g _ _ _ hne ha hc he; linarith)

end BornFable.GaussianFrames

#print axioms BornFable.GaussianFrames.frame_e3_110
#print axioms BornFable.GaussianFrames.frame_e1_011
#print axioms BornFable.GaussianFrames.frame_e2_101
#print axioms BornFable.GaussianFrames.frame_111_110
#print axioms BornFable.GaussianFrames.frame_tri_110
#print axioms BornFable.GaussianFrames.frame_tri_101
#print axioms BornFable.GaussianFrames.frame_tri_011
#print axioms BornFable.GaussianFrames.class_value
#print axioms BornFable.GaussianFrames.parity_class_function_is_third
