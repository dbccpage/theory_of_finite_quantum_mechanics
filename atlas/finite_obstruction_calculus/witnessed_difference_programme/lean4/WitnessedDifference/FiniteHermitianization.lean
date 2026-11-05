import Init.Data.Rat
import Init.Grind.Ordered.Rat
import WitnessedDifference.DaggerObserverPairing

/-!
# Finite rational Hermitianization from a supplied complex structure

The previous finite spine constructs signed additive carriers, an algebraic
tensor, a declared dagger and observer-induced positive forms.  Those data do
not choose complex scalars.  This file starts only after a rational carrier and
a checked endomorphism `J` with `J² = -I` have been supplied.

It constructs the Gaussian-rational scalar action and the Hermitian form

`h(x,y) = g(x,y) + i g(Jx,y)`

from a symmetric rational bilinear form for which `J` is skew-adjoint.  It
proves conjugate symmetry, sesquilinearity, positivity on the diagonal, and
equality of the real and Hermitian radicals.  A concrete rational plane proves
the hypotheses are inhabited.  Reversing the orientation of `J` retains the
same positive real form but changes the Hermitian form, so positivity does not
select the complex orientation.

This is finite algebraic Hermitianization.  It does not construct a norm
completion, probabilities, states, dynamics, or a physical interpretation.
Lean core only.
-/

namespace WitnessedDifference.FiniteHermitianization

set_option linter.checkUnivs false
set_option linter.unusedSimpArgs false

universe u

/-! ## Exact Gaussian-rational scalars -/

/-- A self-contained presentation of `ℚ(i)`. -/
structure GaussianRat where
  re : Rat
  im : Rat
  deriving DecidableEq

theorem gaussian_ext {z w : GaussianRat} (hre : z.re = w.re)
    (him : z.im = w.im) : z = w := by
  cases z
  cases w
  simp only [GaussianRat.mk.injEq] at hre him ⊢
  exact ⟨hre, him⟩

def gzero : GaussianRat := ⟨0, 0⟩
def gone : GaussianRat := ⟨1, 0⟩
def gi : GaussianRat := ⟨0, 1⟩
def gadd (z w : GaussianRat) : GaussianRat := ⟨z.re + w.re, z.im + w.im⟩
def gneg (z : GaussianRat) : GaussianRat := ⟨-z.re, -z.im⟩
def gmul (z w : GaussianRat) : GaussianRat :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
def gconj (z : GaussianRat) : GaussianRat := ⟨z.re, -z.im⟩
def gnorm (z : GaussianRat) : Rat := z.re * z.re + z.im * z.im

theorem gmul_assoc (x y z : GaussianRat) :
    gmul (gmul x y) z = gmul x (gmul y z) := by
  cases x
  cases y
  cases z
  simp only [gmul, GaussianRat.mk.injEq]
  constructor <;>
    simp only [Rat.sub_eq_add_neg, Rat.neg_mul, Rat.mul_neg, Rat.neg_add,
      Rat.add_mul, Rat.mul_add, Rat.mul_assoc] <;> ac_rfl

theorem gone_mul (z : GaussianRat) : gmul gone z = z := by
  cases z
  apply gaussian_ext <;> simp only [gmul, gone] <;> grind

theorem gmul_one (z : GaussianRat) : gmul z gone = z := by
  cases z
  apply gaussian_ext <;> simp only [gmul, gone] <;> grind

theorem gi_square : gmul gi gi = gneg gone := by
  apply gaussian_ext <;> simp only [gmul, gi, gneg, gone] <;> grind

theorem gconj_involutive (z : GaussianRat) : gconj (gconj z) = z := by
  cases z
  simp [gconj]

theorem gconj_mul (z w : GaussianRat) :
    gconj (gmul z w) = gmul (gconj z) (gconj w) := by
  cases z
  cases w
  apply gaussian_ext
  · simp only [gconj, gmul, Rat.neg_mul, Rat.mul_neg, Rat.neg_neg]
  · simp only [gconj, gmul, Rat.neg_add, Rat.neg_mul, Rat.mul_neg]

theorem rat_square_nonnegative (x : Rat) : 0 ≤ x * x := by
  rcases (Rat.le_total : (0 : Rat) ≤ x ∨ x ≤ 0) with hx | hx
  · exact Rat.mul_nonneg hx hx
  · have hn : 0 ≤ -x := by grind
    have hp := Rat.mul_nonneg hn hn
    simpa [Rat.neg_mul, Rat.mul_neg] using hp

theorem rat_two_squares_zero (x y : Rat) (h : x * x + y * y = 0) :
    x = 0 ∧ y = 0 := by
  have hx := rat_square_nonnegative x
  have hy := rat_square_nonnegative y
  have hx0 : x * x = 0 := by grind
  have hy0 : y * y = 0 := by grind
  exact ⟨(Rat.mul_eq_zero.mp hx0).elim id id,
    (Rat.mul_eq_zero.mp hy0).elim id id⟩

theorem gnorm_nonnegative (z : GaussianRat) : 0 ≤ gnorm z :=
  Rat.add_nonneg (rat_square_nonnegative z.re) (rat_square_nonnegative z.im)

theorem gnorm_eq_zero_iff (z : GaussianRat) : gnorm z = 0 ↔ z = gzero := by
  constructor
  · intro h
    rcases rat_two_squares_zero z.re z.im h with ⟨hre, him⟩
    cases z
    simp only [gzero, GaussianRat.mk.injEq]
    exact ⟨hre, him⟩
  · intro h
    rw [h]
    simp only [gnorm, gzero]
    grind

theorem gnorm_mul (z w : GaussianRat) :
    gnorm (gmul z w) = gnorm z * gnorm w := by
  rcases z with ⟨a, b⟩
  rcases w with ⟨c, d⟩
  simp only [gnorm, gmul]
  grind

/-! ## A supplied rational complex structure -/

abbrev QVec (ι : Type u) := ι → Rat

def vzero {ι : Type u} : QVec ι := fun _ => 0
def vadd {ι : Type u} (x y : QVec ι) : QVec ι := fun i => x i + y i
def vneg {ι : Type u} (x : QVec ι) : QVec ι := fun i => -x i
def vsmul {ι : Type u} (r : Rat) (x : QVec ι) : QVec ι := fun i => r * x i

/-- The extra datum needed to pass from a rational carrier to a complex one. -/
structure ComplexStructure (ι : Type u) where
  J : QVec ι → QVec ι
  map_add : ∀ x y, J (vadd x y) = vadd (J x) (J y)
  map_smul : ∀ r x, J (vsmul r x) = vsmul r (J x)
  square : ∀ x, J (J x) = vneg x

/-- Scalar multiplication by `a+ib` is `aI+bJ`. -/
def complexSmul {ι : Type u} (C : ComplexStructure ι)
    (z : GaussianRat) (x : QVec ι) : QVec ι :=
  vadd (vsmul z.re x) (vsmul z.im (C.J x))

theorem complexSmul_one {ι : Type u} (C : ComplexStructure ι) (x : QVec ι) :
    complexSmul C gone x = x := by
  funext i
  simp only [complexSmul, gone, vadd, vsmul]
  grind

theorem complexSmul_i {ι : Type u} (C : ComplexStructure ι) (x : QVec ι) :
    complexSmul C gi x = C.J x := by
  funext i
  simp only [complexSmul, gi, vadd, vsmul]
  grind

theorem complexSmul_add_scalar {ι : Type u} (C : ComplexStructure ι)
    (z w : GaussianRat) (x : QVec ι) :
    complexSmul C (gadd z w) x =
      vadd (complexSmul C z x) (complexSmul C w x) := by
  funext i
  simp only [complexSmul, gadd, vadd, vsmul, Rat.add_mul]
  ac_rfl

theorem complexSmul_add_vector {ι : Type u} (C : ComplexStructure ι)
    (z : GaussianRat) (x y : QVec ι) :
    complexSmul C z (vadd x y) =
      vadd (complexSmul C z x) (complexSmul C z y) := by
  rw [complexSmul, C.map_add]
  funext i
  simp only [complexSmul, vadd, vsmul, Rat.mul_add]
  ac_rfl

theorem complexSmul_mul {ι : Type u} (C : ComplexStructure ι)
    (z w : GaussianRat) (x : QVec ι) :
    complexSmul C (gmul z w) x =
      complexSmul C z (complexSmul C w x) := by
  simp only [complexSmul]
  rw [C.map_add, C.map_smul, C.map_smul, C.square]
  funext i
  simp only [gmul, complexSmul, vadd, vsmul, vneg,
    Rat.sub_eq_add_neg, Rat.mul_add, Rat.add_mul, Rat.mul_neg,
    Rat.neg_mul, Rat.neg_add, Rat.mul_assoc]
  ac_rfl

/-! ## Compatible real forms and Hermitianization -/

/-- A positive-semidefinite real rational form compatible with `J`. -/
structure CompatibleForm {ι : Type u} (C : ComplexStructure ι) where
  form : QVec ι → QVec ι → Rat
  add_left : ∀ x y z, form (vadd x y) z = form x z + form y z
  smul_left : ∀ r x y, form (vsmul r x) y = r * form x y
  symmetric : ∀ x y, form x y = form y x
  J_skew : ∀ x y, form (C.J x) y = -form x (C.J y)
  nonnegative : ∀ x, 0 ≤ form x x

theorem form_add_right {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y z : QVec ι) :
    F.form x (vadd y z) = F.form x y + F.form x z := by
  calc
    F.form x (vadd y z) = F.form (vadd y z) x := F.symmetric _ _
    _ = F.form y x + F.form z x := F.add_left _ _ _
    _ = F.form x y + F.form x z := by rw [F.symmetric y x, F.symmetric z x]

theorem form_smul_right {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (r : Rat) (x y : QVec ι) :
    F.form x (vsmul r y) = r * F.form x y := by
  calc
    F.form x (vsmul r y) = F.form (vsmul r y) x := F.symmetric _ _
    _ = r * F.form y x := F.smul_left _ _ _
    _ = r * F.form x y := by rw [F.symmetric y x]

theorem form_neg_left {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) :
    F.form (vneg x) y = -F.form x y := by
  have hv : vneg x = vsmul (-1) x := by
    funext i
    simp only [vneg, vsmul]
    grind
  rw [hv, F.smul_left]
  grind

theorem form_neg_right {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) :
    F.form x (vneg y) = -F.form x y := by
  have hv : vneg y = vsmul (-1) y := by
    funext i
    simp only [vneg, vsmul]
    grind
  rw [hv, form_smul_right]
  grind

/-- Skew-adjointness plus `J²=-I` makes `J` an isometry. -/
theorem form_J_isometry {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) :
    F.form (C.J x) (C.J y) = F.form x y := by
  rw [F.J_skew, C.square, form_neg_right]
  exact Rat.neg_neg _

/-- The Hermitian form with real part `g` and imaginary part `g(J-, -)`. -/
def hermitian {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) : GaussianRat :=
  ⟨F.form x y, F.form (C.J x) y⟩

theorem hermitian_conjugate_symmetry {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) :
    hermitian F y x = gconj (hermitian F x y) := by
  apply gaussian_ext
  · exact F.symmetric y x
  · simp only [hermitian, gconj]
    have hs := F.J_skew x y
    have hxy := F.symmetric (C.J y) x
    have hyx := F.symmetric x (C.J y)
    grind

theorem hermitian_add_left {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y z : QVec ι) :
    hermitian F (vadd x y) z = gadd (hermitian F x z) (hermitian F y z) := by
  apply gaussian_ext
  · exact F.add_left x y z
  · simp only [hermitian, gadd]
    rw [C.map_add, F.add_left]

theorem hermitian_add_right {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y z : QVec ι) :
    hermitian F x (vadd y z) = gadd (hermitian F x y) (hermitian F x z) := by
  apply gaussian_ext
  · exact form_add_right F x y z
  · exact form_add_right F (C.J x) y z

/-- The first slot is conjugate linear. -/
theorem hermitian_smul_left {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (z : GaussianRat) (x y : QVec ι) :
    hermitian F (complexSmul C z x) y =
      gmul (gconj z) (hermitian F x y) := by
  apply gaussian_ext
  · simp only [hermitian, complexSmul, gmul, gconj]
    rw [F.add_left, F.smul_left, F.smul_left]
    simp only [Rat.sub_eq_add_neg, Rat.neg_mul, Rat.mul_neg]
    grind
  · simp only [hermitian, complexSmul, gmul, gconj]
    rw [C.map_add, C.map_smul, C.map_smul, C.square,
      F.add_left, F.smul_left, F.smul_left, form_neg_left]
    simp only [Rat.sub_eq_add_neg, Rat.neg_mul, Rat.mul_neg, Rat.neg_neg]

/-- The second slot is linear. -/
theorem hermitian_smul_right {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (z : GaussianRat) (x y : QVec ι) :
    hermitian F x (complexSmul C z y) =
      gmul z (hermitian F x y) := by
  apply gaussian_ext
  · simp only [hermitian, complexSmul, gmul]
    have hskew := F.J_skew x y
    have hright : F.form x (C.J y) = -F.form (C.J x) y := by grind
    rw [form_add_right, form_smul_right, form_smul_right, hright]
    simp only [Rat.sub_eq_add_neg, Rat.neg_mul, Rat.mul_neg, Rat.neg_neg]
  · simp only [hermitian, complexSmul, gmul]
    rw [form_add_right, form_smul_right, form_smul_right, form_J_isometry]

theorem hermitian_self_im_zero {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x : QVec ι) : (hermitian F x x).im = 0 := by
  simp only [hermitian]
  have hs := F.J_skew x x
  have hsym := F.symmetric (C.J x) x
  grind

theorem hermitian_self {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x : QVec ι) :
    hermitian F x x = ⟨F.form x x, 0⟩ := by
  apply gaussian_ext
  · rfl
  · exact hermitian_self_im_zero F x

theorem hermitian_self_nonnegative {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x : QVec ι) :
    0 ≤ (hermitian F x x).re := F.nonnegative x

theorem hermitian_self_zero_iff_form_self_zero {ι : Type u}
    {C : ComplexStructure ι} (F : CompatibleForm C) (x : QVec ι) :
    hermitian F x x = gzero ↔ F.form x x = 0 := by
  rw [hermitian_self]
  constructor
  · intro h
    exact congrArg GaussianRat.re h
  · intro h
    simp [gzero, h]

def FormRadical {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x : QVec ι) : Prop :=
  ∀ y, F.form x y = 0

def HermitianRadical {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x : QVec ι) : Prop :=
  ∀ y, hermitian F x y = gzero

/-- Hermitianization changes scalars but does not change the radical. -/
theorem hermitian_radical_iff_form_radical {ι : Type u}
    {C : ComplexStructure ι} (F : CompatibleForm C) (x : QVec ι) :
    HermitianRadical F x ↔ FormRadical F x := by
  constructor
  · intro h y
    exact congrArg GaussianRat.re (h y)
  · intro h y
    apply gaussian_ext
    · exact h y
    · simp only [hermitian, gzero]
      rw [F.J_skew, h (C.J y), Rat.neg_zero]

/-! ## A constructive finite model and the orientation counterexample -/

abbrev Plane := QVec Bool

def planeJ (x : Plane) : Plane
  | false => -x true
  | true => x false

def oppositePlaneJ (x : Plane) : Plane
  | false => x true
  | true => -x false

def planeComplex : ComplexStructure Bool where
  J := planeJ
  map_add := by
    intro x y
    funext i
    cases i <;> simp [planeJ, vadd, Rat.neg_add]
  map_smul := by
    intro r x
    funext i
    cases i <;> simp [planeJ, vsmul, Rat.mul_neg, Rat.neg_mul, Rat.mul_comm]
  square := by
    intro x
    funext i
    cases i <;> simp [planeJ, vneg]

def oppositePlaneComplex : ComplexStructure Bool where
  J := oppositePlaneJ
  map_add := by
    intro x y
    funext i
    cases i <;> simp [oppositePlaneJ, vadd, Rat.neg_add]
  map_smul := by
    intro r x
    funext i
    cases i <;> simp [oppositePlaneJ, vsmul, Rat.mul_neg, Rat.neg_mul, Rat.mul_comm]
  square := by
    intro x
    funext i
    cases i <;> simp [oppositePlaneJ, vneg]

def planeForm (x y : Plane) : Rat :=
  x false * y false + x true * y true

def planeCompatible : CompatibleForm planeComplex where
  form := planeForm
  add_left := by
    intro x y z
    simp only [planeForm, vadd, Rat.add_mul]
    ac_rfl
  smul_left := by
    intro r x y
    simp only [planeForm, vsmul, Rat.mul_assoc, Rat.mul_add]
  symmetric := by
    intro x y
    simp only [planeForm]
    rw [Rat.mul_comm (x false) (y false), Rat.mul_comm (x true) (y true)]
  J_skew := by
    intro x y
    simp only [planeForm, planeComplex, planeJ, Rat.neg_mul, Rat.neg_add,
      Rat.mul_neg]
    grind
  nonnegative := by
    intro x
    exact Rat.add_nonneg (rat_square_nonnegative (x false))
      (rat_square_nonnegative (x true))

def oppositePlaneCompatible : CompatibleForm oppositePlaneComplex where
  form := planeForm
  add_left := planeCompatible.add_left
  smul_left := planeCompatible.smul_left
  symmetric := planeCompatible.symmetric
  J_skew := by
    intro x y
    simp only [planeForm, oppositePlaneComplex, oppositePlaneJ, Rat.neg_mul,
      Rat.neg_add, Rat.mul_neg]
    grind
  nonnegative := planeCompatible.nonnegative

theorem plane_form_zero_iff_vector_zero (x : Plane) :
    planeForm x x = 0 ↔ x = vzero := by
  constructor
  · intro h
    rcases rat_two_squares_zero (x false) (x true) h with ⟨hfalse, htrue⟩
    funext i
    cases i <;> simp [vzero, hfalse, htrue]
  · intro h
    rw [h]
    simp only [planeForm, vzero]
    grind

def planeToGaussian (x : Plane) : GaussianRat := ⟨x false, x true⟩

theorem plane_complex_action_is_multiplication (z : GaussianRat) (x : Plane) :
    planeToGaussian (complexSmul planeComplex z x) =
      gmul z (planeToGaussian x) := by
  apply gaussian_ext <;>
    simp only [planeToGaussian, complexSmul, planeComplex, planeJ, gmul,
      vadd, vsmul] <;> grind

theorem plane_hermitian_is_standard (x y : Plane) :
    hermitian planeCompatible x y =
      gmul (gconj (planeToGaussian x)) (planeToGaussian y) := by
  apply gaussian_ext
  · simp only [hermitian, planeCompatible, planeForm, gmul, gconj,
      planeToGaussian, planeComplex, planeJ, Rat.mul_neg, Rat.neg_mul,
      Rat.sub_eq_add_neg, Rat.neg_neg]
  · simp only [hermitian, planeCompatible, planeForm, gmul, gconj,
      planeToGaussian, planeComplex, planeJ, Rat.mul_neg, Rat.neg_mul]
    ac_rfl

def realBasis : Plane
  | false => 1
  | true => 0

def imaginaryBasis : Plane
  | false => 0
  | true => 1

/-- The same positive real form admits opposite complex orientations, and the
resulting Hermitian pairings differ.  Positivity does not choose `J`. -/
theorem positive_form_does_not_select_complex_orientation :
    planeForm realBasis realBasis = 1 ∧
      planeForm imaginaryBasis imaginaryBasis = 1 ∧
      hermitian planeCompatible realBasis imaginaryBasis = gi ∧
      hermitian oppositePlaneCompatible realBasis imaginaryBasis = gneg gi ∧
      hermitian planeCompatible realBasis imaginaryBasis ≠
        hermitian oppositePlaneCompatible realBasis imaginaryBasis := by
  constructor
  · simp only [planeForm, realBasis]
    grind
  constructor
  · simp only [planeForm, imaginaryBasis]
    grind
  constructor
  · apply gaussian_ext <;>
      simp only [hermitian, planeCompatible, planeForm, realBasis,
        imaginaryBasis, planeComplex, planeJ, gi] <;> grind
  constructor
  · apply gaussian_ext <;>
      simp only [hermitian, oppositePlaneCompatible, planeForm, realBasis,
        imaginaryBasis, oppositePlaneComplex, oppositePlaneJ, gneg, gi] <;> grind
  · intro h
    have him := congrArg GaussianRat.im h
    simp only [hermitian, planeCompatible, oppositePlaneCompatible, planeForm,
      realBasis, imaginaryBasis, planeComplex, oppositePlaneComplex, planeJ,
      oppositePlaneJ] at him
    grind

end WitnessedDifference.FiniteHermitianization

#print axioms WitnessedDifference.FiniteHermitianization.gmul_assoc
#print axioms WitnessedDifference.FiniteHermitianization.gconj_mul
#print axioms WitnessedDifference.FiniteHermitianization.gnorm_mul
#print axioms WitnessedDifference.FiniteHermitianization.complexSmul_mul
#print axioms WitnessedDifference.FiniteHermitianization.form_J_isometry
#print axioms WitnessedDifference.FiniteHermitianization.hermitian_conjugate_symmetry
#print axioms WitnessedDifference.FiniteHermitianization.hermitian_add_left
#print axioms WitnessedDifference.FiniteHermitianization.hermitian_add_right
#print axioms WitnessedDifference.FiniteHermitianization.hermitian_smul_left
#print axioms WitnessedDifference.FiniteHermitianization.hermitian_smul_right
#print axioms WitnessedDifference.FiniteHermitianization.hermitian_self_nonnegative
#print axioms WitnessedDifference.FiniteHermitianization.hermitian_self_zero_iff_form_self_zero
#print axioms WitnessedDifference.FiniteHermitianization.hermitian_radical_iff_form_radical
#print axioms WitnessedDifference.FiniteHermitianization.plane_form_zero_iff_vector_zero
#print axioms WitnessedDifference.FiniteHermitianization.plane_complex_action_is_multiplication
#print axioms WitnessedDifference.FiniteHermitianization.plane_hermitian_is_standard
#print axioms WitnessedDifference.FiniteHermitianization.positive_form_does_not_select_complex_orientation
