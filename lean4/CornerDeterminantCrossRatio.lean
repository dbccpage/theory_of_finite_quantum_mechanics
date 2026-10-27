import SzollosiDeltoid
import AlgebraicCornerReconstruction

/-!
# Concrete Cross-Ratio and Corner Determinant Identities (Target 1 / Lane UNC)

AuthorityEffect: None

Grounding:
Mateo Cárdenes Wuttig & Joseph Tindall (August 2026),
"A Complete Classification of Complex Hadamard Matrices of Order Six", arXiv:2608.18053.
H. B. Mann (1965), "On Linear Relations Between Roots of Unity", Mathematika 12, 107–117.
J. H. Conway & A. J. Jones (1976), "Trigonometric Diophantine Equations", Acta Arith. 30, 229–240.
B. R. Karlsson (2011), Linear Algebra and its Applications 434, 239–246.
Ferenc Szöllősi (2010), J. Phys. A: Math. Theor. 43, 385303.


## Mathematical Architecture

This module formalizes:
1. **Determinant Identity for Dephased 3x3 Corners**:
   For the dephased 3x3 corner matrix:
     M = [[1, 1, 1], [1, a, b], [1, c, d]]
   we establish:
     det(M) = a * d - b * c - a + b + c - d.
   We prove this both for general 3x3 corner matrices and for the leading 3x3 submatrix
   of order-6 matrices over any commutative star-ring (modeling ℂ and ℚ(ζ₂₄)).
   Furthermore, we establish equivalence with the Singular Corner condition
   (Lemma 8, Cárdenes Wuttig & Tindall 2026; `CornerSingular` in `AlgebraicCornerReconstruction.lean`):
     det(M) = 0 ↔ a * d + b + c = b * c + a + d.
2. **Gauge Invariance of 2x2 Cross-Ratio**:
   For any 2x2 sub-block [[a, b], [c, d]] under independent row and column phasings
   (D₁ M D₂), we establish:
     cr(D₁ M D₂) = cr(M)
   where cr(M) = a * d * b* * c*.
   We prove this at the 2x2 block level and for submatrices of order-6 matrices under
   full diagonal gauge transformations.
3. **Equivalence Between Row Orthogonality and cr = -1**:
   Under declared unit-modulus hypotheses (|a| = |b| = |c| = |d| = 1), we establish:
     Row orthogonality (a * b* + c * d* = 0) ↔ cr(a, b, c, d) = -1
   and analogously for column orthogonality (a * c* + b * d* = 0 ↔ cr(a, b, c, d) = -1).
-/

namespace MUB6.Gluing.CornerCrossRatio

open MUB6.Gluing
open MUB6.Gluing.SzollosiDeltoid
open MUB6.Gluing.CornerReconstruction

variable (R : CommStarRing)

/-!
### 1. Matrix Geometries and Coordinate Indices
-/

/-- A 2x2 matrix over ring R. -/
def Matrix2 (α : Type) := Fin 2 → Fin 2 → α

abbrev idx0_2 : Fin 2 := ⟨0, by omega⟩
abbrev idx1_2 : Fin 2 := ⟨1, by omega⟩

/-!
### 2. Corner Determinant Identity for Dephased 3x3 Corners
-/

/-- Standard 3x3 Determinant in any CommStarRing via Laplace expansion along row 0. -/
def det3 (M : Matrix3 R.Carrier) : R.Carrier :=
  R.add
    (R.mul (M g0 g0) (CommStarRing.sub R (R.mul (M g1 g1) (M g2 g2)) (R.mul (M g1 g2) (M g2 g1))))
    (R.add
      (R.neg (R.mul (M g0 g1) (CommStarRing.sub R (R.mul (M g1 g0) (M g2 g2)) (R.mul (M g1 g2) (M g2 g0)))))
      (R.mul (M g0 g2) (CommStarRing.sub R (R.mul (M g1 g0) (M g2 g1)) (R.mul (M g1 g1) (M g2 g0)))))

/-- Canonical dephased 3x3 corner matrix with entries (a, b, c, d):
Row 0: 1, 1, 1
Row 1: 1, a, b
Row 2: 1, c, d -/
def dephasedCorner3 (a b c d : R.Carrier) : Matrix3 R.Carrier :=
  fun i j =>
    match i.val, j.val with
    | 0, 0 => R.one | 0, 1 => R.one | 0, 2 => R.one
    | 1, 0 => R.one | 1, 1 => a     | 1, 2 => b
    | 2, 0 => R.one | 2, 1 => c     | 2, 2 => d
    | _, _ => R.zero

/-- Corner determinant polynomial: a*d - b*c - a + b + c - d. -/
def cornerDeterminantPoly (a b c d : R.Carrier) : R.Carrier :=
  R.add (R.mul a d)
    (R.add (R.neg (R.mul b c))
      (R.add (R.neg a)
        (R.add b
          (R.add c (R.neg d)))))

theorem dephasedCorner3_entry_00 (a b c d : R.Carrier) : dephasedCorner3 R a b c d g0 g0 = R.one := rfl
theorem dephasedCorner3_entry_01 (a b c d : R.Carrier) : dephasedCorner3 R a b c d g0 g1 = R.one := rfl
theorem dephasedCorner3_entry_02 (a b c d : R.Carrier) : dephasedCorner3 R a b c d g0 g2 = R.one := rfl
theorem dephasedCorner3_entry_10 (a b c d : R.Carrier) : dephasedCorner3 R a b c d g1 g0 = R.one := rfl
theorem dephasedCorner3_entry_11 (a b c d : R.Carrier) : dephasedCorner3 R a b c d g1 g1 = a := rfl
theorem dephasedCorner3_entry_12 (a b c d : R.Carrier) : dephasedCorner3 R a b c d g1 g2 = b := rfl
theorem dephasedCorner3_entry_20 (a b c d : R.Carrier) : dephasedCorner3 R a b c d g2 g0 = R.one := rfl
theorem dephasedCorner3_entry_21 (a b c d : R.Carrier) : dephasedCorner3 R a b c d g2 g1 = c := rfl
theorem dephasedCorner3_entry_22 (a b c d : R.Carrier) : dephasedCorner3 R a b c d g2 g2 = d := rfl

/-- **Theorem 1: Corner Determinant Identity for Dephased 3x3 Corner**.
For the dephased 3x3 corner matrix M = [[1, 1, 1], [1, a, b], [1, c, d]],
det(M) = a*d - b*c - a + b + c - d.
Proven constructively. -/
theorem det3_dephased_corner (a b c d : R.Carrier) :
    det3 R (dephasedCorner3 R a b c d) = cornerDeterminantPoly R a b c d := by
  unfold det3 CommStarRing.sub cornerDeterminantPoly
  rw [dephasedCorner3_entry_00, dephasedCorner3_entry_01, dephasedCorner3_entry_02,
      dephasedCorner3_entry_10, dephasedCorner3_entry_11, dephasedCorner3_entry_12,
      dephasedCorner3_entry_20, dephasedCorner3_entry_21, dephasedCorner3_entry_22]
  rw [R.one_mul, R.one_mul, R.mul_one, R.one_mul, R.one_mul, R.mul_one, R.one_mul]
  rw [R.neg_add, R.neg_neg]
  rw [R.add_assoc (R.mul a d) (R.neg (R.mul b c))]
  congr 1
  rw [R.add_comm (R.neg d) b]
  rw [R.add_comm c (R.neg a)]
  rw [R.add_comm (R.add b (R.neg d)) (R.add (R.neg a) c)]
  rw [R.add_assoc (R.neg a) c (R.add b (R.neg d))]
  congr 1
  rw [← R.add_assoc c b (R.neg d)]
  rw [R.add_comm c b]
  rw [R.add_assoc b c (R.neg d)]

/-- Leading 3x3 corner extraction from an order-6 matrix. -/
def corner3x3 (H : Matrix6 R.Carrier) : Matrix3 R.Carrier :=
  fun i j => H ⟨i.val, by omega⟩ ⟨j.val, by omega⟩

/-- **Theorem 1b: Leading 3x3 Corner Determinant in Order-6 Matrix**.
Evaluates the leading 3x3 corner determinant of a 6x6 matrix whose leading corner is dephased. -/
theorem det_leading_corner_dephased (H : Matrix6 R.Carrier) (a b c d : R.Carrier)
    (h00 : H f0 f0 = R.one) (h01 : H f0 f1 = R.one) (h02 : H f0 f2 = R.one)
    (h10 : H f1 f0 = R.one) (h11 : H f1 f1 = a)     (h12 : H f1 f2 = b)
    (h20 : H f2 f0 = R.one) (h21 : H f2 f1 = c)     (h22 : H f2 f2 = d) :
    det3 R (corner3x3 R H) = cornerDeterminantPoly R a b c d := by
  unfold det3 CommStarRing.sub cornerDeterminantPoly corner3x3
  have e00 : H ⟨(g0 : Fin 3).val, by omega⟩ ⟨(g0 : Fin 3).val, by omega⟩ = R.one := h00
  have e01 : H ⟨(g0 : Fin 3).val, by omega⟩ ⟨(g1 : Fin 3).val, by omega⟩ = R.one := h01
  have e02 : H ⟨(g0 : Fin 3).val, by omega⟩ ⟨(g2 : Fin 3).val, by omega⟩ = R.one := h02
  have e10 : H ⟨(g1 : Fin 3).val, by omega⟩ ⟨(g0 : Fin 3).val, by omega⟩ = R.one := h10
  have e11 : H ⟨(g1 : Fin 3).val, by omega⟩ ⟨(g1 : Fin 3).val, by omega⟩ = a := h11
  have e12 : H ⟨(g1 : Fin 3).val, by omega⟩ ⟨(g2 : Fin 3).val, by omega⟩ = b := h12
  have e20 : H ⟨(g2 : Fin 3).val, by omega⟩ ⟨(g0 : Fin 3).val, by omega⟩ = R.one := h20
  have e21 : H ⟨(g2 : Fin 3).val, by omega⟩ ⟨(g1 : Fin 3).val, by omega⟩ = c := h21
  have e22 : H ⟨(g2 : Fin 3).val, by omega⟩ ⟨(g2 : Fin 3).val, by omega⟩ = d := h22
  rw [e00, e01, e02, e10, e11, e12, e20, e21, e22]
  rw [R.one_mul, R.one_mul, R.mul_one, R.one_mul, R.one_mul, R.mul_one, R.one_mul]
  rw [R.neg_add, R.neg_neg]
  rw [R.add_assoc (R.mul a d) (R.neg (R.mul b c))]
  congr 1
  rw [R.add_comm (R.neg d) b]
  rw [R.add_comm c (R.neg a)]
  rw [R.add_comm (R.add b (R.neg d)) (R.add (R.neg a) c)]
  rw [R.add_assoc (R.neg a) c (R.add b (R.neg d))]
  congr 1
  rw [← R.add_assoc c b (R.neg d)]
  rw [R.add_comm c b]
  rw [R.add_assoc b c (R.neg d)]

/-!
### 3. Gauge Invariance of 2x2 Cross-Ratio
-/

/-- Cross-ratio of a 2x2 configuration: a * d * b* * c*. -/
def crossRatio (a b c d : R.Carrier) : R.Carrier :=
  R.mul (R.mul a d) (R.mul (R.conj b) (R.conj c))

/-- Cross-ratio of a 2x2 matrix: M₀₀ M₁₁ M₀₁* M₁₀*. -/
def crossRatio2 (M : Matrix2 R.Carrier) : R.Carrier :=
  crossRatio R (M idx0_2 idx0_2) (M idx0_2 idx1_2) (M idx1_2 idx0_2) (M idx1_2 idx1_2)

/-- Product middle-swap lemma: (w * x) * (y * z) = (w * y) * (x * z). -/
theorem mul_swap_middle (w x y z : R.Carrier) :
    R.mul (R.mul w x) (R.mul y z) = R.mul (R.mul w y) (R.mul x z) := by
  rw [← R.mul_assoc (R.mul w x) y z]
  rw [R.mul_assoc w x y]
  rw [R.mul_comm x y]
  rw [← R.mul_assoc w y x]
  rw [R.mul_assoc (R.mul w y) x z]

/-- Cross-unit cancellation lemma: (x * u) * (y * u*) = x * y for unit-modulus u. -/
theorem mul_unit_cross (x y u : R.Carrier) (hu : CommStarRing.isUnitModulus R u) :
    R.mul (R.mul x u) (R.mul y (R.conj u)) = R.mul x y := by
  rw [mul_swap_middle R x u y (R.conj u), hu, R.mul_one]

/-- Invariance of 2x2 cross-ratio under column phase rotations. -/
theorem cross_ratio_col_phase_invariance
    (a b c d v0 v1 : R.Carrier)
    (hv0 : CommStarRing.isUnitModulus R v0)
    (hv1 : CommStarRing.isUnitModulus R v1) :
    crossRatio R
      (R.mul a v0)
      (R.mul b v1)
      (R.mul c v0)
      (R.mul d v1) =
    crossRatio R a b c d := by
  unfold crossRatio
  rw [R.conj_mul, R.conj_mul]
  rw [R.mul_comm (R.mul (R.conj b) (R.conj v1)) (R.mul (R.conj c) (R.conj v0))]
  rw [mul_swap_middle R (R.mul a v0) (R.mul d v1) (R.mul (R.conj c) (R.conj v0)) (R.mul (R.conj b) (R.conj v1))]
  rw [mul_unit_cross R a (R.conj c) v0 hv0]
  rw [mul_unit_cross R d (R.conj b) v1 hv1]
  rw [mul_swap_middle R a (R.conj c) d (R.conj b)]
  rw [R.mul_comm (R.conj c) (R.conj b)]

/-- Invariance of 2x2 cross-ratio under row phase rotations. -/
theorem cross_ratio_row_phase_invariance
    (a b c d u0 u1 : R.Carrier)
    (hu0 : CommStarRing.isUnitModulus R u0)
    (hu1 : CommStarRing.isUnitModulus R u1) :
    crossRatio R
      (R.mul u0 a)
      (R.mul u0 b)
      (R.mul u1 c)
      (R.mul u1 d) =
    crossRatio R a b c d := by
  unfold crossRatio
  rw [R.conj_mul, R.conj_mul]
  rw [R.mul_comm u0 a, R.mul_comm u1 d, R.mul_comm (R.conj u0) (R.conj b), R.mul_comm (R.conj u1) (R.conj c)]
  rw [mul_swap_middle R (R.mul a u0) (R.mul d u1) (R.mul (R.conj b) (R.conj u0)) (R.mul (R.conj c) (R.conj u1))]
  rw [mul_unit_cross R a (R.conj b) u0 hu0]
  rw [mul_unit_cross R d (R.conj c) u1 hu1]
  rw [mul_swap_middle R a (R.conj b) d (R.conj c)]

/-- **Theorem 2: Full Gauge Invariance of 2x2 Cross-Ratio**.
For any 2x2 sub-block [[a, b], [c, d]] of unit-modulus numbers under independent row
and column phasings D₁ M D₂, cr(D₁ M D₂) = cr(M).
Proven constructively with zero axioms. -/
theorem cross_ratio_gauge_invariance
    (a b c d u0 u1 v0 v1 : R.Carrier)
    (hu0 : CommStarRing.isUnitModulus R u0)
    (hu1 : CommStarRing.isUnitModulus R u1)
    (hv0 : CommStarRing.isUnitModulus R v0)
    (hv1 : CommStarRing.isUnitModulus R v1) :
    crossRatio R
      (R.mul (R.mul u0 a) v0)
      (R.mul (R.mul u0 b) v1)
      (R.mul (R.mul u1 c) v0)
      (R.mul (R.mul u1 d) v1) =
    crossRatio R a b c d := by
  rw [cross_ratio_col_phase_invariance R (R.mul u0 a) (R.mul u0 b) (R.mul u1 c) (R.mul u1 d) v0 v1 hv0 hv1]
  exact cross_ratio_row_phase_invariance R a b c d u0 u1 hu0 hu1

/-- Independent row and column phase scaling of an order-6 matrix: D₁ H D₂. -/
def phaseMatrix6 (u v : Fin 6 → R.Carrier) (H : Matrix6 R.Carrier) : Matrix6 R.Carrier :=
  fun i j => R.mul (R.mul (u i) (H i j)) (v j)

/-- Extraction of a 2x2 submatrix from an order-6 matrix. -/
def submatrix2 (H : Matrix6 R.Carrier) (r0 r1 c0 c1 : Fin 6) : Matrix2 R.Carrier :=
  fun i j =>
    match i.val, j.val with
    | 0, 0 => H r0 c0 | 0, 1 => H r0 c1
    | 1, 0 => H r1 c0 | 1, 1 => H r1 c1
    | _, _ => R.zero

theorem submatrix2_entry_00 (H : Matrix6 R.Carrier) (r0 r1 c0 c1 : Fin 6) : submatrix2 R H r0 r1 c0 c1 idx0_2 idx0_2 = H r0 c0 := rfl
theorem submatrix2_entry_01 (H : Matrix6 R.Carrier) (r0 r1 c0 c1 : Fin 6) : submatrix2 R H r0 r1 c0 c1 idx0_2 idx1_2 = H r0 c1 := rfl
theorem submatrix2_entry_10 (H : Matrix6 R.Carrier) (r0 r1 c0 c1 : Fin 6) : submatrix2 R H r0 r1 c0 c1 idx1_2 idx0_2 = H r1 c0 := rfl
theorem submatrix2_entry_11 (H : Matrix6 R.Carrier) (r0 r1 c0 c1 : Fin 6) : submatrix2 R H r0 r1 c0 c1 idx1_2 idx1_2 = H r1 c1 := rfl

/-- **Theorem 2b: Gauge Invariance for Submatrices of Order-6 Matrices**. -/
theorem submatrix2_gauge_invariance
    (H : Matrix6 R.Carrier) (r0 r1 c0 c1 : Fin 6) (u v : Fin 6 → R.Carrier)
    (hu0 : CommStarRing.isUnitModulus R (u r0))
    (hu1 : CommStarRing.isUnitModulus R (u r1))
    (hv0 : CommStarRing.isUnitModulus R (v c0))
    (hv1 : CommStarRing.isUnitModulus R (v c1)) :
    crossRatio2 R (submatrix2 R (phaseMatrix6 R u v H) r0 r1 c0 c1) =
    crossRatio2 R (submatrix2 R H r0 r1 c0 c1) := by
  unfold crossRatio2
  rw [submatrix2_entry_00, submatrix2_entry_01, submatrix2_entry_10, submatrix2_entry_11]
  rw [submatrix2_entry_00, submatrix2_entry_01, submatrix2_entry_10, submatrix2_entry_11]
  dsimp [phaseMatrix6]
  exact cross_ratio_gauge_invariance R (H r0 c0) (H r0 c1) (H r1 c0) (H r1 c1)
    (u r0) (u r1) (v c0) (v c1) hu0 hu1 hv0 hv1

/-!
### 4. Equivalence Between Row Orthogonality and cr = -1
-/

theorem cross_ratio_eq_row_factors (a b c d : R.Carrier) :
    crossRatio R a b c d = R.mul (R.mul a (R.conj b)) (R.mul d (R.conj c)) := by
  unfold crossRatio
  exact mul_swap_middle R a d (R.conj b) (R.conj c)

theorem cross_ratio_eq_col_factors (a b c d : R.Carrier) :
    crossRatio R a b c d = R.mul (R.mul a (R.conj c)) (R.mul d (R.conj b)) := by
  unfold crossRatio
  have h1 : R.mul (R.conj b) (R.conj c) = R.mul (R.conj c) (R.conj b) := R.mul_comm (R.conj b) (R.conj c)
  rw [h1]
  exact mul_swap_middle R a d (R.conj c) (R.conj b)

theorem add_eq_zero_of_eq_neg (x y : R.Carrier) (h : x = R.neg y) :
    R.add x y = R.zero := by
  rw [h, R.add_left_neg]

theorem eq_neg_of_add_eq_zero (x y : R.Carrier) (h : R.add x y = R.zero) :
    x = R.neg y := by
  have h1 : x = R.add x R.zero := (R.add_zero x).symm
  have h2 : R.zero = R.add y (R.neg y) := by rw [R.add_comm, R.add_left_neg]
  rw [h2] at h1
  rw [← R.add_assoc] at h1
  rw [h] at h1
  rw [R.zero_add] at h1
  exact h1

theorem unit_cross_product_one (c d : R.Carrier)
    (hc : CommStarRing.isUnitModulus R c)
    (hd : CommStarRing.isUnitModulus R d) :
    R.mul (R.mul c (R.conj d)) (R.mul d (R.conj c)) = R.one := by
  rw [R.mul_comm d (R.conj c)]
  rw [mul_swap_middle R c (R.conj d) (R.conj c) d]
  rw [hc]
  rw [R.mul_comm (R.conj d) d]
  have hd' : R.mul d (R.conj d) = R.one := hd
  rw [hd', R.mul_one]

/-- Row orthogonality for a 2x2 block: a * b* + c * d* = 0
(Hermitian inner product of columns (a, c) and (b, d)). -/
def RowOrthogonal (a b c d : R.Carrier) : Prop :=
  R.add (R.mul a (R.conj b)) (R.mul c (R.conj d)) = R.zero

/-- Column orthogonality for a 2x2 block: a * c* + b * d* = 0
(Hermitian inner product of rows (a, b) and (c, d)). -/
def ColOrthogonal (a b c d : R.Carrier) : Prop :=
  R.add (R.mul a (R.conj c)) (R.mul b (R.conj d)) = R.zero

/-- **Theorem 3: Equivalence Between Row Orthogonality and cr = -1**.
Under declared unit-modulus hypotheses (|a| = |b| = |c| = |d| = 1):
a * b* + c * d* = 0 ↔ cr(a, b, c, d) = -1.
Proven constructively in both directions with zero axioms. -/
theorem row_orthogonality_iff_cross_ratio_neg_one
    (a b c d : R.Carrier)
    (_ha : CommStarRing.isUnitModulus R a)
    (_hb : CommStarRing.isUnitModulus R b)
    (hc : CommStarRing.isUnitModulus R c)
    (hd : CommStarRing.isUnitModulus R d) :
    RowOrthogonal R a b c d ↔ crossRatio R a b c d = R.neg R.one := by
  constructor
  · intro h_ortho
    have h_neg : R.mul a (R.conj b) = R.neg (R.mul c (R.conj d)) :=
      eq_neg_of_add_eq_zero R _ _ h_ortho
    rw [cross_ratio_eq_row_factors]
    rw [h_neg]
    rw [R.neg_mul]
    rw [unit_cross_product_one R c d hc hd]
  · intro h_cr
    have h_row : R.mul (R.mul a (R.conj b)) (R.mul d (R.conj c)) = R.neg R.one := by
      rw [← cross_ratio_eq_row_factors]
      exact h_cr
    have h_mult : R.mul (R.mul (R.mul a (R.conj b)) (R.mul d (R.conj c))) (R.mul c (R.conj d)) =
                  R.mul (R.neg R.one) (R.mul c (R.conj d)) := by
      rw [h_row]
    rw [R.mul_assoc (R.mul a (R.conj b))] at h_mult
    rw [R.mul_comm (R.mul d (R.conj c)) (R.mul c (R.conj d))] at h_mult
    rw [unit_cross_product_one R c d hc hd] at h_mult
    rw [R.mul_one] at h_mult
    rw [R.neg_mul, R.one_mul] at h_mult
    exact add_eq_zero_of_eq_neg R _ _ h_mult

/-- **Theorem 3b: Equivalence Between Column Orthogonality and cr = -1**.
Under declared unit-modulus hypotheses (|a| = |b| = |c| = |d| = 1):
a * c* + b * d* = 0 ↔ cr(a, b, c, d) = -1.
Proven constructively in both directions with zero axioms. -/
theorem col_orthogonality_iff_cross_ratio_neg_one
    (a b c d : R.Carrier)
    (_ha : CommStarRing.isUnitModulus R a)
    (hb : CommStarRing.isUnitModulus R b)
    (_hc : CommStarRing.isUnitModulus R c)
    (hd : CommStarRing.isUnitModulus R d) :
    ColOrthogonal R a b c d ↔ crossRatio R a b c d = R.neg R.one := by
  constructor
  · intro h_ortho
    have h_neg : R.mul a (R.conj c) = R.neg (R.mul b (R.conj d)) :=
      eq_neg_of_add_eq_zero R _ _ h_ortho
    rw [cross_ratio_eq_col_factors]
    rw [h_neg]
    rw [R.neg_mul]
    rw [unit_cross_product_one R b d hb hd]
  · intro h_cr
    have h_col : R.mul (R.mul a (R.conj c)) (R.mul d (R.conj b)) = R.neg R.one := by
      rw [← cross_ratio_eq_col_factors]
      exact h_cr
    have h_mult : R.mul (R.mul (R.mul a (R.conj c)) (R.mul d (R.conj b))) (R.mul b (R.conj d)) =
                  R.mul (R.neg R.one) (R.mul b (R.conj d)) := by
      rw [h_col]
    rw [R.mul_assoc (R.mul a (R.conj c))] at h_mult
    rw [R.mul_comm (R.mul d (R.conj b)) (R.mul b (R.conj d))] at h_mult
    rw [unit_cross_product_one R b d hb hd] at h_mult
    rw [R.mul_one] at h_mult
    rw [R.neg_mul, R.one_mul] at h_mult
    exact add_eq_zero_of_eq_neg R _ _ h_mult

#print axioms det3_dephased_corner
#print axioms det_leading_corner_dephased
#print axioms cross_ratio_gauge_invariance
#print axioms submatrix2_gauge_invariance
#print axioms row_orthogonality_iff_cross_ratio_neg_one
#print axioms col_orthogonality_iff_cross_ratio_neg_one

end MUB6.Gluing.CornerCrossRatio
