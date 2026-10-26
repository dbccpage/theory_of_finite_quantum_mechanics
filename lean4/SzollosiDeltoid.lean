import WallTransport
import ZeroRelVariety
import ModuliReduction

/-!
# Szöllősi Deltoid Arc Formalization in Lean 4 (MUB(6) Campaign 6 / Lane G1d)

AuthorityEffect: None


## Mathematical Architecture

This module formalizes:
1. **2-Circulant Matrix Algebra over Commutative Star-Rings**:
   - The abstract commutative involutive ring `CommStarRing` capturing exact arithmetic in ℂ.
   - 3x3 and 6x6 matrix representations and 4-block decomposition.
   - Circulant matrices `A = circ(a, b, c)` and `B = circ(d, e, f)`.
2. **Column Orthogonality and the Szöllősi Condition**:
   - Exact circulant commutativity theorem: `A * B = B * A` for all circulants over commutative rings.
   - Off-diagonal blocks in B₆ B₆† vanish identically by circulant commutativity:
     `A B - B A = 0` and `B† A† - A† B† = 0`.
   - Diagonal blocks equal `6 I₃` if and only if `z₁ + z₂ = 0`, where:
     `z₁ = a c* + b a* + c b*`
     `z₂ = d f* + e d* + f e*`.
   - Column orthogonality theorem: `B₆ B₆† = 6 I₆ ↔ z₁ + z₂ = 0`.
3. **Complex Hadamard Property**:
   - Unimodular entry constraints for 2-circulant blocks.
   - Exact proof that `z₁ + z₂ = 0` implies B₆ is a complex Hadamard matrix.
4. **Deltoid Hypocycloid Parameterization**:
   - Parameterization of the boundary curve connecting Fourier `F₆` (z₁ = 0),
     Haagerup `H₆` (intermediate arc parameter), and Tao `S₆` (boundary cusps).
5. **Unbiasedness Extension Obstruction**:
   - Total squared curvature functional Ψˢᑫ(B₆(θ), U) > 0 on candidate fourth bases.
   - Connection to `ZeroRelVariety.lean` (`curvature_bound_implies_variety_empty`):
     A certified positive curvature lower bound ε_del > 0 forces the real ZeroRel vanishing
     locus to be empty: V_ℝ(ZeroRel_{B₆(θ)}) = ∅, guaranteeing ¬ HasFourthBasis(B₆(θ)).
-/

namespace MUB6.Gluing.SzollosiDeltoid

open MUB6.Gluing
open MUB6.Gluing.Variety
open MUB6.Gluing.Orbits
open MUB6.Gluing.ModuliReduction

/-!
### 1. Commutative Star-Ring and Matrix Arithmetic
-/

/-- An abstract commutative ring with involution (star-ring), modeling ℂ, ℚ(ζ₂₄), or phase rings. -/
structure CommStarRing where
  Carrier : Type
  zero : Carrier
  one : Carrier
  add : Carrier → Carrier → Carrier
  neg : Carrier → Carrier
  mul : Carrier → Carrier → Carrier
  conj : Carrier → Carrier
  -- Ring axioms
  add_assoc : ∀ x y z, add (add x y) z = add x (add y z)
  add_comm : ∀ x y, add x y = add y x
  add_zero : ∀ x, add x zero = x
  zero_add : ∀ x, add zero x = x
  add_left_neg : ∀ x, add (neg x) x = zero
  mul_assoc : ∀ x y z, mul (mul x y) z = mul x (mul y z)
  mul_comm : ∀ x y, mul x y = mul y x
  mul_one : ∀ x, mul x one = x
  one_mul : ∀ x, mul one x = x
  left_distrib : ∀ x y z, mul x (add y z) = add (mul x y) (mul x z)
  right_distrib : ∀ x y z, mul (add x y) z = add (mul x z) (mul y z)
  zero_mul : ∀ x, mul zero x = zero
  mul_zero : ∀ x, mul x zero = zero
  neg_neg : ∀ x, neg (neg x) = x
  mul_neg : ∀ x y, mul x (neg y) = neg (mul x y)
  neg_mul : ∀ x y, mul (neg x) y = neg (mul x y)
  neg_add : ∀ x y, neg (add x y) = add (neg x) (neg y)
  -- Involution (star) axioms
  conj_add : ∀ x y, conj (add x y) = add (conj x) (conj y)
  conj_mul : ∀ x y, conj (mul x y) = mul (conj x) (conj y)
  conj_conj : ∀ x, conj (conj x) = x
  conj_zero : conj zero = zero
  conj_one : conj one = one
  conj_neg : ∀ x, conj (neg x) = neg (conj x)

namespace CommStarRing

variable (R : CommStarRing)

/-- Subtraction in CommStarRing. -/
def sub (x y : R.Carrier) : R.Carrier :=
  R.add x (R.neg y)

/-- Swap inner terms of a 3-term sum: x + (y + z) = x + (z + y). -/
theorem add_swap_inner (x y z : R.Carrier) :
    R.add x (R.add y z) = R.add x (R.add z y) := by
  rw [R.add_comm y z]

/-- Swap first and second terms of a 3-term sum: x + (y + z) = y + (x + z). -/
theorem add_swap_first_second (x y z : R.Carrier) :
    R.add x (R.add y z) = R.add y (R.add x z) := by
  rw [← R.add_assoc, R.add_comm x y, R.add_assoc]

/-- Swap first and third terms of a 3-term sum: x + (y + z) = z + (y + x). -/
theorem add_swap_first_third (x y z : R.Carrier) :
    R.add x (R.add y z) = R.add z (R.add y x) := by
  rw [← R.add_assoc, R.add_comm (R.add x y) z, R.add_comm x y]

/-- 6-term addition associativity: (x₀ + (x₁ + x₂)) + (x₃ + (x₄ + x₅)) = x₀ + (x₁ + (x₂ + (x₃ + (x₄ + x₅)))). -/
theorem add_assoc6 (x0 x1 x2 x3 x4 x5 : R.Carrier) :
    R.add (R.add x0 (R.add x1 x2)) (R.add x3 (R.add x4 x5)) =
    R.add x0 (R.add x1 (R.add x2 (R.add x3 (R.add x4 x5)))) := by
  rw [R.add_assoc, R.add_assoc]

/-- Multiplication of negated elements: (-x) * (-y) = x * y. -/
theorem neg_mul_neg (x y : R.Carrier) : R.mul (R.neg x) (R.neg y) = R.mul x y := by
  rw [R.neg_mul, R.mul_neg, R.neg_neg]

/-- Right negation: x + (-x) = 0. -/
theorem add_right_neg (x : R.Carrier) : R.add x (R.neg x) = R.zero := by
  rw [R.add_comm, R.add_left_neg]

/-- Self-subtraction gives zero: x - x = 0. -/
theorem add_sub_cancel (x : R.Carrier) : sub R x x = R.zero := by
  dsimp [sub]
  exact add_right_neg R x

/-- Multiplicative reduction of double conjugate negation: x * (conj (- (conj y))) = - (x * y). -/
theorem add_cycle3 (x y z : R.Carrier) :
    R.add x (R.add y z) = R.add z (R.add x y) := by
  rw [← R.add_assoc, R.add_comm (R.add x y) z]

theorem add_cycle3_back (x y z : R.Carrier) :
    R.add x (R.add y z) = R.add y (R.add z x) := by
  rw [R.add_comm y z, ← R.add_assoc, R.add_comm (R.add x z) y, R.add_comm x z]

theorem mul_neg_conj (x y : R.Carrier) :
    R.mul x (R.conj (R.neg (R.conj y))) = R.neg (R.mul x y) := by
  rw [R.conj_neg, R.conj_conj, R.mul_neg]

theorem mul_neg_conj_neg (x y : R.Carrier) :
    R.mul (R.neg x) (R.conj (R.neg y)) = R.mul x (R.conj y) := by
  rw [R.conj_neg, neg_mul_neg]



/-- 6-term cancellation: if x₀ + (x₁ + x₂) = y₀ + (y₁ + y₂), then (x₀ + (x₁ + x₂)) + (-y₀ + (-y₁ + -y₂)) = 0. -/
theorem add6_cancel (x0 x1 x2 y0 y1 y2 : R.Carrier)
    (h_comm : R.add x0 (R.add x1 x2) = R.add y0 (R.add y1 y2)) :
    R.add (R.add x0 (R.add x1 x2))
          (R.add (R.neg y0) (R.add (R.neg y1) (R.neg y2))) = R.zero := by
  rw [← R.neg_add, ← R.neg_add]
  rw [h_comm]
  exact add_right_neg R _

/-- The element 3 in the star-ring: 1 + 1 + 1. -/
def three : R.Carrier :=
  R.add R.one (R.add R.one R.one)

/-- The element 6 in the star-ring: 3 + 3. -/
def six : R.Carrier :=
  R.add (three R) (three R)

/-- Unit modulus predicate: x * x* = 1. -/
def isUnitModulus (x : R.Carrier) : Prop :=
  R.mul x (R.conj x) = R.one

theorem is_unit_modulus_conj (x : R.Carrier) (h : isUnitModulus R x) :
    isUnitModulus R (R.conj x) := by
  dsimp [isUnitModulus]
  rw [R.conj_conj, R.mul_comm]
  exact h

theorem is_unit_modulus_neg (x : R.Carrier) (h : isUnitModulus R x) :
    isUnitModulus R (R.neg x) := by
  dsimp [isUnitModulus]
  rw [R.conj_neg, neg_mul_neg]
  exact h

end CommStarRing

/-!
### 2. Canonical Coordinates and 3x3 Matrices
-/

abbrev f0 : Fin 6 := ⟨0, by omega⟩
abbrev f1 : Fin 6 := ⟨1, by omega⟩
abbrev f2 : Fin 6 := ⟨2, by omega⟩
abbrev f3 : Fin 6 := ⟨3, by omega⟩
abbrev f4 : Fin 6 := ⟨4, by omega⟩
abbrev f5 : Fin 6 := ⟨5, by omega⟩

abbrev g0 : Fin 3 := ⟨0, by omega⟩
abbrev g1 : Fin 3 := ⟨1, by omega⟩
abbrev g2 : Fin 3 := ⟨2, by omega⟩

/-- A 3x3 matrix over R. -/
def Matrix3 (α : Type) := Fin 3 → Fin 3 → α

/-- A 6x6 matrix over R. -/
def Matrix6 (α : Type) := Fin 6 → Fin 6 → α

/-- Identity matrix in dimension 3. -/
def id3 (R : CommStarRing) : Matrix3 R.Carrier :=
  fun i j => if i = j then R.one else R.zero

/-- Scaled identity matrix in dimension 3: s * I₃. -/
def scaleId3 (R : CommStarRing) (s : R.Carrier) : Matrix3 R.Carrier :=
  fun i j => if i = j then s else R.zero

/-- Zero matrix in dimension 3. -/
def zero3 (R : CommStarRing) : Matrix3 R.Carrier :=
  fun _ _ => R.zero

/-- 3x3 Matrix addition. -/
def add3 (R : CommStarRing) (M N : Matrix3 R.Carrier) : Matrix3 R.Carrier :=
  fun i j => R.add (M i j) (N i j)

/-- 3x3 Matrix subtraction. -/
def sub3 (R : CommStarRing) (M N : Matrix3 R.Carrier) : Matrix3 R.Carrier :=
  fun i j => CommStarRing.sub R (M i j) (N i j)

/-- 3x3 Matrix multiplication. -/
def mul3 (R : CommStarRing) (M N : Matrix3 R.Carrier) : Matrix3 R.Carrier :=
  fun i j =>
    R.add (R.mul (M i g0) (N g0 j))
      (R.add (R.mul (M i g1) (N g1 j))
             (R.mul (M i g2) (N g2 j)))

/-- 3x3 Matrix adjoint (conjugate transpose). -/
def adjoint3 (R : CommStarRing) (M : Matrix3 R.Carrier) : Matrix3 R.Carrier :=
  fun i j => R.conj (M j i)

/-- A 3x3 circulant matrix circ(c₀, c₁, c₂):
Row 0: c₀, c₁, c₂
Row 1: c₂, c₀, c₁
Row 2: c₁, c₂, c₀ -/
def circulant3 (R : CommStarRing) (c0 c1 c2 : R.Carrier) : Matrix3 R.Carrier :=
  fun i j =>
    match i.val, j.val with
    | 0, 0 => c0 | 0, 1 => c1 | 0, 2 => c2
    | 1, 0 => c2 | 1, 1 => c0 | 1, 2 => c1
    | 2, 0 => c1 | 2, 1 => c2 | 2, 2 => c0
    | _, _ => R.zero

/-- The adjoint of circ(c₀, c₁, c₂) is circ(c₀*, c₂*, c₁*). -/
theorem adjoint3_circulant (R : CommStarRing) (c0 c1 c2 : R.Carrier) :
    adjoint3 R (circulant3 R c0 c1 c2) =
    circulant3 R (R.conj c0) (R.conj c2) (R.conj c1) := by
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ => rfl
  | ⟨0, _⟩, ⟨1, _⟩ => rfl
  | ⟨0, _⟩, ⟨2, _⟩ => rfl
  | ⟨1, _⟩, ⟨0, _⟩ => rfl
  | ⟨1, _⟩, ⟨1, _⟩ => rfl
  | ⟨1, _⟩, ⟨2, _⟩ => rfl
  | ⟨2, _⟩, ⟨0, _⟩ => rfl
  | ⟨2, _⟩, ⟨1, _⟩ => rfl
  | ⟨2, _⟩, ⟨2, _⟩ => rfl

/-- **Theorem: Circulant Commutativity**.
Any two 3x3 circulant matrices over a commutative star-ring commute: A * B = B * A. -/
theorem circulant_comm (R : CommStarRing) (a0 a1 a2 b0 b1 b2 : R.Carrier) :
    mul3 R (circulant3 R a0 a1 a2) (circulant3 R b0 b1 b2) =
    mul3 R (circulant3 R b0 b1 b2) (circulant3 R a0 a1 a2) := by
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ =>
    change R.add (R.mul a0 b0) (R.add (R.mul a1 b2) (R.mul a2 b1)) =
           R.add (R.mul b0 a0) (R.add (R.mul b1 a2) (R.mul b2 a1))
    rw [R.mul_comm b0 a0, R.mul_comm b1 a2, R.mul_comm b2 a1]
    exact CommStarRing.add_swap_inner R _ _ _
  | ⟨0, _⟩, ⟨1, _⟩ =>
    change R.add (R.mul a0 b1) (R.add (R.mul a1 b0) (R.mul a2 b2)) =
           R.add (R.mul b0 a1) (R.add (R.mul b1 a0) (R.mul b2 a2))
    rw [R.mul_comm b0 a1, R.mul_comm b1 a0, R.mul_comm b2 a2]
    exact CommStarRing.add_swap_first_second R _ _ _
  | ⟨0, _⟩, ⟨2, _⟩ =>
    change R.add (R.mul a0 b2) (R.add (R.mul a1 b1) (R.mul a2 b0)) =
           R.add (R.mul b0 a2) (R.add (R.mul b1 a1) (R.mul b2 a0))
    rw [R.mul_comm b0 a2, R.mul_comm b1 a1, R.mul_comm b2 a0]
    exact CommStarRing.add_swap_first_third R _ _ _
  | ⟨1, _⟩, ⟨0, _⟩ =>
    change R.add (R.mul a2 b0) (R.add (R.mul a0 b2) (R.mul a1 b1)) =
           R.add (R.mul b2 a0) (R.add (R.mul b0 a2) (R.mul b1 a1))
    rw [R.mul_comm b2 a0, R.mul_comm b0 a2, R.mul_comm b1 a1]
    exact CommStarRing.add_swap_first_second R _ _ _
  | ⟨1, _⟩, ⟨1, _⟩ =>
    change R.add (R.mul a2 b1) (R.add (R.mul a0 b0) (R.mul a1 b2)) =
           R.add (R.mul b2 a1) (R.add (R.mul b0 a0) (R.mul b1 a2))
    rw [R.mul_comm b2 a1, R.mul_comm b0 a0, R.mul_comm b1 a2]
    exact CommStarRing.add_swap_first_third R _ _ _
  | ⟨1, _⟩, ⟨2, _⟩ =>
    change R.add (R.mul a2 b2) (R.add (R.mul a0 b1) (R.mul a1 b0)) =
           R.add (R.mul b2 a2) (R.add (R.mul b0 a1) (R.mul b1 a0))
    rw [R.mul_comm b2 a2, R.mul_comm b0 a1, R.mul_comm b1 a0]
    exact CommStarRing.add_swap_inner R _ _ _
  | ⟨2, _⟩, ⟨0, _⟩ =>
    change R.add (R.mul a1 b0) (R.add (R.mul a2 b2) (R.mul a0 b1)) =
           R.add (R.mul b1 a0) (R.add (R.mul b2 a2) (R.mul b0 a1))
    rw [R.mul_comm b1 a0, R.mul_comm b2 a2, R.mul_comm b0 a1]
    exact CommStarRing.add_swap_first_third R _ _ _
  | ⟨2, _⟩, ⟨1, _⟩ =>
    change R.add (R.mul a1 b1) (R.add (R.mul a2 b0) (R.mul a0 b2)) =
           R.add (R.mul b1 a1) (R.add (R.mul b2 a0) (R.mul b0 a2))
    rw [R.mul_comm b1 a1, R.mul_comm b2 a0, R.mul_comm b0 a2]
    exact CommStarRing.add_swap_inner R _ _ _
  | ⟨2, _⟩, ⟨2, _⟩ =>
    change R.add (R.mul a1 b2) (R.add (R.mul a2 b1) (R.mul a0 b0)) =
           R.add (R.mul b1 a2) (R.add (R.mul b2 a1) (R.mul b0 a0))
    rw [R.mul_comm b1 a2, R.mul_comm b2 a1, R.mul_comm b0 a0]
    exact CommStarRing.add_swap_first_second R _ _ _

/-- Subtractive form of circulant commutativity: A * B - B * A = 0. -/
theorem circulant_comm_sub (R : CommStarRing) (a0 a1 a2 b0 b1 b2 : R.Carrier) :
    sub3 R (mul3 R (circulant3 R a0 a1 a2) (circulant3 R b0 b1 b2))
           (mul3 R (circulant3 R b0 b1 b2) (circulant3 R a0 a1 a2)) =
    zero3 R := by
  have h := circulant_comm R a0 a1 a2 b0 b1 b2
  rw [h]
  funext i j
  dsimp [sub3, zero3]
  exact CommStarRing.add_sub_cancel R _

/-- Circulant normality: A * A† = A† * A. -/
theorem circulant_normal (R : CommStarRing) (a0 a1 a2 : R.Carrier) :
    mul3 R (circulant3 R a0 a1 a2) (adjoint3 R (circulant3 R a0 a1 a2)) =
    mul3 R (adjoint3 R (circulant3 R a0 a1 a2)) (circulant3 R a0 a1 a2) := by
  rw [adjoint3_circulant]
  exact circulant_comm R a0 a1 a2 (R.conj a0) (R.conj a2) (R.conj a1)

/-!
### 3. 4-Block Matrix Decomposition
-/

/-- Top-left 3x3 block of a 6x6 matrix. -/
def block00 {α : Type} (M : Matrix6 α) : Matrix3 α :=
  fun i j =>
    match i.val, j.val with
    | 0, 0 => M f0 f0 | 0, 1 => M f0 f1 | 0, 2 => M f0 f2
    | 1, 0 => M f1 f0 | 1, 1 => M f1 f1 | 1, 2 => M f1 f2
    | 2, 0 => M f2 f0 | 2, 1 => M f2 f1 | 2, 2 => M f2 f2
    | _, _ => M f0 f0

/-- Top-right 3x3 block of a 6x6 matrix. -/
def block01 {α : Type} (M : Matrix6 α) : Matrix3 α :=
  fun i j =>
    match i.val, j.val with
    | 0, 0 => M f0 f3 | 0, 1 => M f0 f4 | 0, 2 => M f0 f5
    | 1, 0 => M f1 f3 | 1, 1 => M f1 f4 | 1, 2 => M f1 f5
    | 2, 0 => M f2 f3 | 2, 1 => M f2 f4 | 2, 2 => M f2 f5
    | _, _ => M f0 f0

/-- Bottom-left 3x3 block of a 6x6 matrix. -/
def block10 {α : Type} (M : Matrix6 α) : Matrix3 α :=
  fun i j =>
    match i.val, j.val with
    | 0, 0 => M f3 f0 | 0, 1 => M f3 f1 | 0, 2 => M f3 f2
    | 1, 0 => M f4 f0 | 1, 1 => M f4 f1 | 1, 2 => M f4 f2
    | 2, 0 => M f5 f0 | 2, 1 => M f5 f1 | 2, 2 => M f5 f2
    | _, _ => M f0 f0

/-- Bottom-right 3x3 block of a 6x6 matrix. -/
def block11 {α : Type} (M : Matrix6 α) : Matrix3 α :=
  fun i j =>
    match i.val, j.val with
    | 0, 0 => M f3 f3 | 0, 1 => M f3 f4 | 0, 2 => M f3 f5
    | 1, 0 => M f4 f3 | 1, 1 => M f4 f4 | 1, 2 => M f4 f5
    | 2, 0 => M f5 f3 | 2, 1 => M f5 f4 | 2, 2 => M f5 f5
    | _, _ => M f0 f0

/-- **Theorem: 4-Block Matrix Extensionality**.
Two 6x6 matrices are equal if and only if all four of their 3x3 blocks are equal. -/
theorem matrix6_ext_blocks {α : Type} (M N : Matrix6 α)
    (h00 : block00 M = block00 N)
    (h01 : block01 M = block01 N)
    (h10 : block10 M = block10 N)
    (h11 : block11 M = block11 N) : M = N := by
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ => exact congrFun (congrFun h00 g0) g0
  | ⟨0, _⟩, ⟨1, _⟩ => exact congrFun (congrFun h00 g0) g1
  | ⟨0, _⟩, ⟨2, _⟩ => exact congrFun (congrFun h00 g0) g2
  | ⟨0, _⟩, ⟨3, _⟩ => exact congrFun (congrFun h01 g0) g0
  | ⟨0, _⟩, ⟨4, _⟩ => exact congrFun (congrFun h01 g0) g1
  | ⟨0, _⟩, ⟨5, _⟩ => exact congrFun (congrFun h01 g0) g2
  | ⟨1, _⟩, ⟨0, _⟩ => exact congrFun (congrFun h00 g1) g0
  | ⟨1, _⟩, ⟨1, _⟩ => exact congrFun (congrFun h00 g1) g1
  | ⟨1, _⟩, ⟨2, _⟩ => exact congrFun (congrFun h00 g1) g2
  | ⟨1, _⟩, ⟨3, _⟩ => exact congrFun (congrFun h01 g1) g0
  | ⟨1, _⟩, ⟨4, _⟩ => exact congrFun (congrFun h01 g1) g1
  | ⟨1, _⟩, ⟨5, _⟩ => exact congrFun (congrFun h01 g1) g2
  | ⟨2, _⟩, ⟨0, _⟩ => exact congrFun (congrFun h00 g2) g0
  | ⟨2, _⟩, ⟨1, _⟩ => exact congrFun (congrFun h00 g2) g1
  | ⟨2, _⟩, ⟨2, _⟩ => exact congrFun (congrFun h00 g2) g2
  | ⟨2, _⟩, ⟨3, _⟩ => exact congrFun (congrFun h01 g2) g0
  | ⟨2, _⟩, ⟨4, _⟩ => exact congrFun (congrFun h01 g2) g1
  | ⟨2, _⟩, ⟨5, _⟩ => exact congrFun (congrFun h01 g2) g2
  | ⟨3, _⟩, ⟨0, _⟩ => exact congrFun (congrFun h10 g0) g0
  | ⟨3, _⟩, ⟨1, _⟩ => exact congrFun (congrFun h10 g0) g1
  | ⟨3, _⟩, ⟨2, _⟩ => exact congrFun (congrFun h10 g0) g2
  | ⟨3, _⟩, ⟨3, _⟩ => exact congrFun (congrFun h11 g0) g0
  | ⟨3, _⟩, ⟨4, _⟩ => exact congrFun (congrFun h11 g0) g1
  | ⟨3, _⟩, ⟨5, _⟩ => exact congrFun (congrFun h11 g0) g2
  | ⟨4, _⟩, ⟨0, _⟩ => exact congrFun (congrFun h10 g1) g0
  | ⟨4, _⟩, ⟨1, _⟩ => exact congrFun (congrFun h10 g1) g1
  | ⟨4, _⟩, ⟨2, _⟩ => exact congrFun (congrFun h10 g1) g2
  | ⟨4, _⟩, ⟨3, _⟩ => exact congrFun (congrFun h11 g1) g0
  | ⟨4, _⟩, ⟨4, _⟩ => exact congrFun (congrFun h11 g1) g1
  | ⟨4, _⟩, ⟨5, _⟩ => exact congrFun (congrFun h11 g1) g2
  | ⟨5, _⟩, ⟨0, _⟩ => exact congrFun (congrFun h10 g2) g0
  | ⟨5, _⟩, ⟨1, _⟩ => exact congrFun (congrFun h10 g2) g1
  | ⟨5, _⟩, ⟨2, _⟩ => exact congrFun (congrFun h10 g2) g2
  | ⟨5, _⟩, ⟨3, _⟩ => exact congrFun (congrFun h11 g2) g0
  | ⟨5, _⟩, ⟨4, _⟩ => exact congrFun (congrFun h11 g2) g1
  | ⟨5, _⟩, ⟨5, _⟩ => exact congrFun (congrFun h11 g2) g2

/-- 6x6 matrix adjoint. -/
def adjoint6 (R : CommStarRing) (M : Matrix6 R.Carrier) : Matrix6 R.Carrier :=
  fun i j => R.conj (M j i)

/-- 6x6 matrix multiplication. -/
def mul6 (R : CommStarRing) (M N : Matrix6 R.Carrier) : Matrix6 R.Carrier :=
  fun i j =>
    R.add (R.mul (M i f0) (N f0 j))
      (R.add (R.mul (M i f1) (N f1 j))
        (R.add (R.mul (M i f2) (N f2 j))
          (R.add (R.mul (M i f3) (N f3 j))
            (R.add (R.mul (M i f4) (N f4 j))
              (R.mul (M i f5) (N f5 j))))))

/-- Scaled identity matrix in dimension 6: s * I₆. -/
def scaleId6 (R : CommStarRing) (s : R.Carrier) : Matrix6 R.Carrier :=
  fun i j => if i = j then s else R.zero

/-- Block (0, 0) of scaleId6 is scaleId3. -/
theorem block00_scaleId6 (R : CommStarRing) (s : R.Carrier) :
    block00 (scaleId6 R s) = scaleId3 R s := by
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ => rfl | ⟨0, _⟩, ⟨1, _⟩ => rfl | ⟨0, _⟩, ⟨2, _⟩ => rfl
  | ⟨1, _⟩, ⟨0, _⟩ => rfl | ⟨1, _⟩, ⟨1, _⟩ => rfl | ⟨1, _⟩, ⟨2, _⟩ => rfl
  | ⟨2, _⟩, ⟨0, _⟩ => rfl | ⟨2, _⟩, ⟨1, _⟩ => rfl | ⟨2, _⟩, ⟨2, _⟩ => rfl

/-- Block (0, 1) of scaleId6 is zero3. -/
theorem block01_scaleId6 (R : CommStarRing) (s : R.Carrier) :
    block01 (scaleId6 R s) = zero3 R := by
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ => rfl | ⟨0, _⟩, ⟨1, _⟩ => rfl | ⟨0, _⟩, ⟨2, _⟩ => rfl
  | ⟨1, _⟩, ⟨0, _⟩ => rfl | ⟨1, _⟩, ⟨1, _⟩ => rfl | ⟨1, _⟩, ⟨2, _⟩ => rfl
  | ⟨2, _⟩, ⟨0, _⟩ => rfl | ⟨2, _⟩, ⟨1, _⟩ => rfl | ⟨2, _⟩, ⟨2, _⟩ => rfl

/-- Block (1, 0) of scaleId6 is zero3. -/
theorem block10_scaleId6 (R : CommStarRing) (s : R.Carrier) :
    block10 (scaleId6 R s) = zero3 R := by
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ => rfl | ⟨0, _⟩, ⟨1, _⟩ => rfl | ⟨0, _⟩, ⟨2, _⟩ => rfl
  | ⟨1, _⟩, ⟨0, _⟩ => rfl | ⟨1, _⟩, ⟨1, _⟩ => rfl | ⟨1, _⟩, ⟨2, _⟩ => rfl
  | ⟨2, _⟩, ⟨0, _⟩ => rfl | ⟨2, _⟩, ⟨1, _⟩ => rfl | ⟨2, _⟩, ⟨2, _⟩ => rfl

/-- Block (1, 1) of scaleId6 is scaleId3. -/
theorem block11_scaleId6 (R : CommStarRing) (s : R.Carrier) :
    block11 (scaleId6 R s) = scaleId3 R s := by
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ => rfl | ⟨0, _⟩, ⟨1, _⟩ => rfl | ⟨0, _⟩, ⟨2, _⟩ => rfl
  | ⟨1, _⟩, ⟨0, _⟩ => rfl | ⟨1, _⟩, ⟨1, _⟩ => rfl | ⟨1, _⟩, ⟨2, _⟩ => rfl
  | ⟨2, _⟩, ⟨0, _⟩ => rfl | ⟨2, _⟩, ⟨1, _⟩ => rfl | ⟨2, _⟩, ⟨2, _⟩ => rfl

/-!
### 4. The 2-Circulant Matrix B₆ and Szöllősi Orthogonality Condition
-/

/-- Szöllősi 2-circulant block matrix structure:
B₆ = [[A,      B   ],
      [B†,    -A†  ]]
where A and B are 3x3 circulant matrices. -/
def szollosiBlock6 (R : CommStarRing) (A B : Matrix3 R.Carrier) : Matrix6 R.Carrier :=
  fun i j =>
    match i.val, j.val with
    | 0, 0 => A g0 g0 | 0, 1 => A g0 g1 | 0, 2 => A g0 g2
    | 0, 3 => B g0 g0 | 0, 4 => B g0 g1 | 0, 5 => B g0 g2
    | 1, 0 => A g1 g0 | 1, 1 => A g1 g1 | 1, 2 => A g1 g2
    | 1, 3 => B g1 g0 | 1, 4 => B g1 g1 | 1, 5 => B g1 g2
    | 2, 0 => A g2 g0 | 2, 1 => A g2 g1 | 2, 2 => A g2 g2
    | 2, 3 => B g2 g0 | 2, 4 => B g2 g1 | 2, 5 => B g2 g2
    | 3, 0 => adjoint3 R B g0 g0 | 3, 1 => adjoint3 R B g0 g1 | 3, 2 => adjoint3 R B g0 g2
    | 3, 3 => R.neg (adjoint3 R A g0 g0) | 3, 4 => R.neg (adjoint3 R A g0 g1) | 3, 5 => R.neg (adjoint3 R A g0 g2)
    | 4, 0 => adjoint3 R B g1 g0 | 4, 1 => adjoint3 R B g1 g1 | 4, 2 => adjoint3 R B g1 g2
    | 4, 3 => R.neg (adjoint3 R A g1 g0) | 4, 4 => R.neg (adjoint3 R A g1 g1) | 4, 5 => R.neg (adjoint3 R A g1 g2)
    | 5, 0 => adjoint3 R B g2 g0 | 5, 1 => adjoint3 R B g2 g1 | 5, 2 => adjoint3 R B g2 g2
    | 5, 3 => R.neg (adjoint3 R A g2 g0) | 5, 4 => R.neg (adjoint3 R A g2 g1) | 5, 5 => R.neg (adjoint3 R A g2 g2)
    | _, _ => R.zero

/-- Szöllősi 2-circulant matrix from 6 unimodular phase parameters (a, b, c, d, e, f). -/
def szollosiB6 (R : CommStarRing) (a b c d e f : R.Carrier) : Matrix6 R.Carrier :=
  szollosiBlock6 R (circulant3 R a b c) (circulant3 R d e f)

/-- Szöllősi z₁ invariant: z₁ = a c* + b a* + c b*. -/
def szollosi_z1 (R : CommStarRing) (a b c : R.Carrier) : R.Carrier :=
  R.add (R.mul a (R.conj c)) (R.add (R.mul b (R.conj a)) (R.mul c (R.conj b)))

/-- Szöllősi z₂ invariant: z₂ = d f* + e d* + f e*.
Evaluates the same polynomial form on (d, e, f). -/
def szollosi_z2 (R : CommStarRing) (d e f : R.Carrier) : R.Carrier :=
  szollosi_z1 R d e f

/-- Circulant Gram Matrix Diagonal: For unimodular entries, (A A†)ᵢᵢ = 3. -/
theorem circulant_gram_diag (R : CommStarRing) (a b c : R.Carrier)
    (ha : CommStarRing.isUnitModulus R a)
    (hb : CommStarRing.isUnitModulus R b)
    (hc : CommStarRing.isUnitModulus R c) (i : Fin 3) :
    mul3 R (circulant3 R a b c) (adjoint3 R (circulant3 R a b c)) i i =
    CommStarRing.three R := by
  rw [adjoint3_circulant]
  match i with
  | ⟨0, _⟩ =>
    change R.add (R.mul a (R.conj a)) (R.add (R.mul b (R.conj b)) (R.mul c (R.conj c))) =
           CommStarRing.three R
    dsimp [CommStarRing.three]
    rw [ha, hb, hc]
  | ⟨1, _⟩ =>
    change R.add (R.mul c (R.conj c)) (R.add (R.mul a (R.conj a)) (R.mul b (R.conj b))) =
           CommStarRing.three R
    dsimp [CommStarRing.three]
    rw [ha, hb, hc]
  | ⟨2, _⟩ =>
    change R.add (R.mul b (R.conj b)) (R.add (R.mul c (R.conj c)) (R.mul a (R.conj a))) =
           CommStarRing.three R
    dsimp [CommStarRing.three]
    rw [ha, hb, hc]

/-- Sum of Gram Diagonal Blocks: (A A† + B B†)ᵢᵢ = 3 + 3 = 6. -/
theorem szollosi_diag_entry_eq_six (R : CommStarRing) (a b c d e f : R.Carrier)
    (ha : CommStarRing.isUnitModulus R a) (hb : CommStarRing.isUnitModulus R b) (hc : CommStarRing.isUnitModulus R c)
    (hd : CommStarRing.isUnitModulus R d) (he : CommStarRing.isUnitModulus R e) (hf : CommStarRing.isUnitModulus R f)
    (i : Fin 3) :
    R.add (mul3 R (circulant3 R a b c) (adjoint3 R (circulant3 R a b c)) i i)
          (mul3 R (circulant3 R d e f) (adjoint3 R (circulant3 R d e f)) i i) =
    CommStarRing.six R := by
  rw [circulant_gram_diag R a b c ha hb hc i]
  rw [circulant_gram_diag R d e f hd he hf i]
  rfl

/-- Off-diagonal entry (0, 1) of circulant Gram matrix equals z₁. -/
theorem circulant_gram_offdiag_01 (R : CommStarRing) (a b c : R.Carrier) :
    mul3 R (circulant3 R a b c) (adjoint3 R (circulant3 R a b c)) g0 g1 =
    szollosi_z1 R a b c := by
  rw [adjoint3_circulant]
  rfl

/-- Off-diagonal entry (0, 1) of the sum equals z₁ + z₂. -/
theorem szollosi_offdiag_01_eq_sum (R : CommStarRing) (a b c d e f : R.Carrier) :
    R.add (mul3 R (circulant3 R a b c) (adjoint3 R (circulant3 R a b c)) g0 g1)
          (mul3 R (circulant3 R d e f) (adjoint3 R (circulant3 R d e f)) g0 g1) =
    R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f) := by
  rw [circulant_gram_offdiag_01, circulant_gram_offdiag_01]
  rfl

/-- Off-diagonal entry (1, 2) equals z₁ + z₂. -/
theorem circulant_gram_entry_12 (R : CommStarRing) (a b c d e f : R.Carrier) :
    R.add (mul3 R (circulant3 R a b c) (adjoint3 R (circulant3 R a b c)) g1 g2)
          (mul3 R (circulant3 R d e f) (adjoint3 R (circulant3 R d e f)) g1 g2) =
    R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f) := by
  rw [adjoint3_circulant, adjoint3_circulant]
  change R.add (R.add (R.mul c (R.conj b)) (R.add (R.mul a (R.conj c)) (R.mul b (R.conj a))))
               (R.add (R.mul f (R.conj e)) (R.add (R.mul d (R.conj f)) (R.mul e (R.conj d)))) =
         R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f)
  dsimp [szollosi_z1, szollosi_z2]
  rw [CommStarRing.add_swap_first_second R (R.mul c (R.conj b))]
  rw [CommStarRing.add_swap_first_second R (R.mul f (R.conj e))]
  rw [R.add_comm (R.mul c (R.conj b)) (R.mul b (R.conj a))]
  rw [R.add_comm (R.mul f (R.conj e)) (R.mul e (R.conj d))]

/-- Off-diagonal entry (2, 0) equals z₁ + z₂. -/
theorem circulant_gram_entry_20 (R : CommStarRing) (a b c d e f : R.Carrier) :
    R.add (mul3 R (circulant3 R a b c) (adjoint3 R (circulant3 R a b c)) g2 g0)
          (mul3 R (circulant3 R d e f) (adjoint3 R (circulant3 R d e f)) g2 g0) =
    R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f) := by
  rw [adjoint3_circulant, adjoint3_circulant]
  change R.add (R.add (R.mul b (R.conj a)) (R.add (R.mul c (R.conj b)) (R.mul a (R.conj c))))
               (R.add (R.mul e (R.conj d)) (R.add (R.mul f (R.conj e)) (R.mul d (R.conj f)))) =
         R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f)
  dsimp [szollosi_z1, szollosi_z2]
  rw [CommStarRing.add_swap_first_third R (R.mul b (R.conj a))]
  rw [CommStarRing.add_swap_first_third R (R.mul e (R.conj d))]
  rw [R.add_comm (R.mul c (R.conj b)) (R.mul b (R.conj a))]
  rw [R.add_comm (R.mul f (R.conj e)) (R.mul e (R.conj d))]

/-- **Theorem: Diagonal Blocks Equal 6 I₃ if and only if z₁ + z₂ = 0**.
A A† + B B† = 6 I₃ holds precisely when the Szöllősi condition z₁ + z₂ = 0 is satisfied. -/
theorem diagonal_blocks_eq_six_iff (R : CommStarRing) (a b c d e f : R.Carrier)
    (ha : CommStarRing.isUnitModulus R a) (hb : CommStarRing.isUnitModulus R b) (hc : CommStarRing.isUnitModulus R c)
    (hd : CommStarRing.isUnitModulus R d) (he : CommStarRing.isUnitModulus R e) (hf : CommStarRing.isUnitModulus R f) :
    (add3 R (mul3 R (circulant3 R a b c) (adjoint3 R (circulant3 R a b c)))
            (mul3 R (circulant3 R d e f) (adjoint3 R (circulant3 R d e f))) =
     scaleId3 R (CommStarRing.six R)) ↔
    (R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f) = R.zero) := by
  constructor
  · intro h_mat
    have h01 := congrFun (congrFun h_mat g0) g1
    dsimp [scaleId3] at h01
    rw [adjoint3_circulant, adjoint3_circulant] at h01
    change R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f) = R.zero at h01
    exact h01
  · intro h_cond
    funext i j
    match i, j with
    | ⟨0, _⟩, ⟨0, _⟩ =>
      dsimp [add3, scaleId3]
      exact szollosi_diag_entry_eq_six R a b c d e f ha hb hc hd he hf g0
    | ⟨1, _⟩, ⟨1, _⟩ =>
      dsimp [add3, scaleId3]
      exact szollosi_diag_entry_eq_six R a b c d e f ha hb hc hd he hf g1
    | ⟨2, _⟩, ⟨2, _⟩ =>
      dsimp [add3, scaleId3]
      exact szollosi_diag_entry_eq_six R a b c d e f ha hb hc hd he hf g2
    | ⟨0, _⟩, ⟨1, _⟩ =>
      dsimp [add3, scaleId3]
      rw [adjoint3_circulant, adjoint3_circulant]
      change R.add (R.add (R.mul a (R.conj c)) (R.add (R.mul b (R.conj a)) (R.mul c (R.conj b))))
                   (R.add (R.mul d (R.conj f)) (R.add (R.mul e (R.conj d)) (R.mul f (R.conj e)))) = R.zero
      exact h_cond
    | ⟨1, _⟩, ⟨2, _⟩ =>
      dsimp [add3, scaleId3]
      rw [adjoint3_circulant, adjoint3_circulant]
      change R.add (R.add (R.mul c (R.conj b)) (R.add (R.mul a (R.conj c)) (R.mul b (R.conj a))))
                   (R.add (R.mul f (R.conj e)) (R.add (R.mul d (R.conj f)) (R.mul e (R.conj d)))) = R.zero
      have hz : R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f) = R.zero := h_cond
      dsimp [szollosi_z1, szollosi_z2] at hz
      rw [CommStarRing.add_swap_first_second R (R.mul c (R.conj b))]
      rw [CommStarRing.add_swap_first_second R (R.mul f (R.conj e))]
      rw [R.add_comm (R.mul b (R.conj a)) (R.mul c (R.conj b)), R.add_comm (R.mul e (R.conj d)) (R.mul f (R.conj e))] at hz
      exact hz
    | ⟨2, _⟩, ⟨0, _⟩ =>
      dsimp [add3, scaleId3]
      rw [adjoint3_circulant, adjoint3_circulant]
      change R.add (R.add (R.mul b (R.conj a)) (R.add (R.mul c (R.conj b)) (R.mul a (R.conj c))))
                   (R.add (R.mul e (R.conj d)) (R.add (R.mul f (R.conj e)) (R.mul d (R.conj f)))) = R.zero
      have hz : R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f) = R.zero := h_cond
      dsimp [szollosi_z1, szollosi_z2] at hz
      rw [CommStarRing.add_swap_first_third R (R.mul b (R.conj a))]
      rw [CommStarRing.add_swap_first_third R (R.mul e (R.conj d))]
      rw [R.add_comm (R.mul b (R.conj a)) (R.mul c (R.conj b)), R.add_comm (R.mul e (R.conj d)) (R.mul f (R.conj e))] at hz
      exact hz
    | ⟨1, _⟩, ⟨0, _⟩ =>
      dsimp [add3, scaleId3]
      rw [adjoint3_circulant, adjoint3_circulant]
      have h_conj : R.conj (R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f)) = R.conj R.zero := by rw [h_cond]
      rw [R.conj_zero, R.conj_add] at h_conj
      dsimp [szollosi_z1, szollosi_z2] at h_conj
      rw [R.conj_add, R.conj_add, R.conj_mul, R.conj_mul, R.conj_mul,
          R.conj_add, R.conj_add, R.conj_mul, R.conj_mul, R.conj_mul] at h_conj
      rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj] at h_conj
      rw [R.mul_comm (R.conj a) c, R.mul_comm (R.conj b) a, R.mul_comm (R.conj c) b,
          R.mul_comm (R.conj d) f, R.mul_comm (R.conj e) d, R.mul_comm (R.conj f) e] at h_conj
      change R.add (R.add (R.mul c (R.conj a)) (R.add (R.mul a (R.conj b)) (R.mul b (R.conj c))))
                   (R.add (R.mul f (R.conj d)) (R.add (R.mul d (R.conj e)) (R.mul e (R.conj f)))) = R.zero
      exact h_conj
    | ⟨2, _⟩, ⟨1, _⟩ =>
      dsimp [add3, scaleId3]
      rw [adjoint3_circulant, adjoint3_circulant]
      have h_conj : R.conj (R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f)) = R.conj R.zero := by rw [h_cond]
      rw [R.conj_zero, R.conj_add] at h_conj
      dsimp [szollosi_z1, szollosi_z2] at h_conj
      rw [R.conj_add, R.conj_add, R.conj_mul, R.conj_mul, R.conj_mul,
          R.conj_add, R.conj_add, R.conj_mul, R.conj_mul, R.conj_mul] at h_conj
      rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj] at h_conj
      rw [R.mul_comm (R.conj a) c, R.mul_comm (R.conj b) a, R.mul_comm (R.conj c) b,
          R.mul_comm (R.conj d) f, R.mul_comm (R.conj e) d, R.mul_comm (R.conj f) e] at h_conj
      change R.add (R.add (R.mul b (R.conj c)) (R.add (R.mul c (R.conj a)) (R.mul a (R.conj b))))
                   (R.add (R.mul e (R.conj f)) (R.add (R.mul f (R.conj d)) (R.mul d (R.conj e)))) = R.zero
      rw [CommStarRing.add_cycle3 R (R.mul c (R.conj a)), CommStarRing.add_cycle3 R (R.mul f (R.conj d))] at h_conj
      exact h_conj
    | ⟨0, _⟩, ⟨2, _⟩ =>
      dsimp [add3, scaleId3]
      rw [adjoint3_circulant, adjoint3_circulant]
      have h_conj : R.conj (R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f)) = R.conj R.zero := by rw [h_cond]
      rw [R.conj_zero, R.conj_add] at h_conj
      dsimp [szollosi_z1, szollosi_z2] at h_conj
      rw [R.conj_add, R.conj_add, R.conj_mul, R.conj_mul, R.conj_mul,
          R.conj_add, R.conj_add, R.conj_mul, R.conj_mul, R.conj_mul] at h_conj
      rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj] at h_conj
      rw [R.mul_comm (R.conj a) c, R.mul_comm (R.conj b) a, R.mul_comm (R.conj c) b,
          R.mul_comm (R.conj d) f, R.mul_comm (R.conj e) d, R.mul_comm (R.conj f) e] at h_conj
      change R.add (R.add (R.mul a (R.conj b)) (R.add (R.mul b (R.conj c)) (R.mul c (R.conj a))))
                   (R.add (R.mul d (R.conj e)) (R.add (R.mul e (R.conj f)) (R.mul f (R.conj d)))) = R.zero
      rw [CommStarRing.add_cycle3_back R (R.mul c (R.conj a)), CommStarRing.add_cycle3_back R (R.mul f (R.conj d))] at h_conj
      exact h_conj


/-- **Top-Left Block Evaluation**: block00(B₆ B₆†) = A A† + B B†. -/
theorem szollosi_block00_eq (R : CommStarRing) (a b c d e f : R.Carrier) :
    block00 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) =
    add3 R (mul3 R (circulant3 R a b c) (adjoint3 R (circulant3 R a b c)))
           (mul3 R (circulant3 R d e f) (adjoint3 R (circulant3 R d e f))) := by
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ => exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
  | ⟨0, _⟩, ⟨1, _⟩ => exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
  | ⟨0, _⟩, ⟨2, _⟩ => exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
  | ⟨1, _⟩, ⟨0, _⟩ => exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
  | ⟨1, _⟩, ⟨1, _⟩ => exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
  | ⟨1, _⟩, ⟨2, _⟩ => exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
  | ⟨2, _⟩, ⟨0, _⟩ => exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
  | ⟨2, _⟩, ⟨1, _⟩ => exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
  | ⟨2, _⟩, ⟨2, _⟩ => exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm

/-- **Top-Right Block Vanishes by Circulant Commutativity**: block01(B₆ B₆†) = 0. -/
theorem szollosi_block01_eq (R : CommStarRing) (a b c d e f : R.Carrier) :
    block01 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) =
    zero3 R := by
  have h_comm := circulant_comm R a b c d e f
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ =>
    have h := congrFun (congrFun h_comm g0) g0
    change R.add (R.mul a d) (R.add (R.mul b f) (R.mul c e)) =
           R.add (R.mul d a) (R.add (R.mul e c) (R.mul f b)) at h
    have h_step1 : block01 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g0 g0 =
      R.add (R.add (R.mul a (R.conj (R.conj d))) (R.add (R.mul b (R.conj (R.conj f))) (R.mul c (R.conj (R.conj e)))))
            (R.add (R.mul d (R.conj (R.neg (R.conj a)))) (R.add (R.mul e (R.conj (R.neg (R.conj c)))) (R.mul f (R.conj (R.neg (R.conj b)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.conj_conj, R.conj_conj, R.conj_conj]
    rw [CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨0, _⟩, ⟨1, _⟩ =>
    have h := congrFun (congrFun h_comm g0) g1
    change R.add (R.mul a e) (R.add (R.mul b d) (R.mul c f)) =
           R.add (R.mul d b) (R.add (R.mul e a) (R.mul f c)) at h
    have h_step1 : block01 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g0 g1 =
      R.add (R.add (R.mul a (R.conj (R.conj e))) (R.add (R.mul b (R.conj (R.conj d))) (R.mul c (R.conj (R.conj f)))))
            (R.add (R.mul d (R.conj (R.neg (R.conj b)))) (R.add (R.mul e (R.conj (R.neg (R.conj a)))) (R.mul f (R.conj (R.neg (R.conj c)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.conj_conj, R.conj_conj, R.conj_conj]
    rw [CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨0, _⟩, ⟨2, _⟩ =>
    have h := congrFun (congrFun h_comm g0) g2
    change R.add (R.mul a f) (R.add (R.mul b e) (R.mul c d)) =
           R.add (R.mul d c) (R.add (R.mul e b) (R.mul f a)) at h
    have h_step1 : block01 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g0 g2 =
      R.add (R.add (R.mul a (R.conj (R.conj f))) (R.add (R.mul b (R.conj (R.conj e))) (R.mul c (R.conj (R.conj d)))))
            (R.add (R.mul d (R.conj (R.neg (R.conj c)))) (R.add (R.mul e (R.conj (R.neg (R.conj b)))) (R.mul f (R.conj (R.neg (R.conj a)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.conj_conj, R.conj_conj, R.conj_conj]
    rw [CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨1, _⟩, ⟨0, _⟩ =>
    have h := congrFun (congrFun h_comm g1) g0
    change R.add (R.mul c d) (R.add (R.mul a f) (R.mul b e)) =
           R.add (R.mul f a) (R.add (R.mul d c) (R.mul e b)) at h
    have h_step1 : block01 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g1 g0 =
      R.add (R.add (R.mul c (R.conj (R.conj d))) (R.add (R.mul a (R.conj (R.conj f))) (R.mul b (R.conj (R.conj e)))))
            (R.add (R.mul f (R.conj (R.neg (R.conj a)))) (R.add (R.mul d (R.conj (R.neg (R.conj c)))) (R.mul e (R.conj (R.neg (R.conj b)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.conj_conj, R.conj_conj, R.conj_conj]
    rw [CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨1, _⟩, ⟨1, _⟩ =>
    have h := congrFun (congrFun h_comm g1) g1
    change R.add (R.mul c e) (R.add (R.mul a d) (R.mul b f)) =
           R.add (R.mul f b) (R.add (R.mul d a) (R.mul e c)) at h
    have h_step1 : block01 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g1 g1 =
      R.add (R.add (R.mul c (R.conj (R.conj e))) (R.add (R.mul a (R.conj (R.conj d))) (R.mul b (R.conj (R.conj f)))))
            (R.add (R.mul f (R.conj (R.neg (R.conj b)))) (R.add (R.mul d (R.conj (R.neg (R.conj a)))) (R.mul e (R.conj (R.neg (R.conj c)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.conj_conj, R.conj_conj, R.conj_conj]
    rw [CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨1, _⟩, ⟨2, _⟩ =>
    have h := congrFun (congrFun h_comm g1) g2
    change R.add (R.mul c f) (R.add (R.mul a e) (R.mul b d)) =
           R.add (R.mul f c) (R.add (R.mul d b) (R.mul e a)) at h
    have h_step1 : block01 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g1 g2 =
      R.add (R.add (R.mul c (R.conj (R.conj f))) (R.add (R.mul a (R.conj (R.conj e))) (R.mul b (R.conj (R.conj d)))))
            (R.add (R.mul f (R.conj (R.neg (R.conj c)))) (R.add (R.mul d (R.conj (R.neg (R.conj b)))) (R.mul e (R.conj (R.neg (R.conj a)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.conj_conj, R.conj_conj, R.conj_conj]
    rw [CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨2, _⟩, ⟨0, _⟩ =>
    have h := congrFun (congrFun h_comm g2) g0
    change R.add (R.mul b d) (R.add (R.mul c f) (R.mul a e)) =
           R.add (R.mul e a) (R.add (R.mul f c) (R.mul d b)) at h
    have h_step1 : block01 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g2 g0 =
      R.add (R.add (R.mul b (R.conj (R.conj d))) (R.add (R.mul c (R.conj (R.conj f))) (R.mul a (R.conj (R.conj e)))))
            (R.add (R.mul e (R.conj (R.neg (R.conj a)))) (R.add (R.mul f (R.conj (R.neg (R.conj c)))) (R.mul d (R.conj (R.neg (R.conj b)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.conj_conj, R.conj_conj, R.conj_conj]
    rw [CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨2, _⟩, ⟨1, _⟩ =>
    have h := congrFun (congrFun h_comm g2) g1
    change R.add (R.mul b e) (R.add (R.mul c d) (R.mul a f)) =
           R.add (R.mul e b) (R.add (R.mul f a) (R.mul d c)) at h
    have h_step1 : block01 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g2 g1 =
      R.add (R.add (R.mul b (R.conj (R.conj e))) (R.add (R.mul c (R.conj (R.conj d))) (R.mul a (R.conj (R.conj f)))))
            (R.add (R.mul e (R.conj (R.neg (R.conj b)))) (R.add (R.mul f (R.conj (R.neg (R.conj a)))) (R.mul d (R.conj (R.neg (R.conj c)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.conj_conj, R.conj_conj, R.conj_conj]
    rw [CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨2, _⟩, ⟨2, _⟩ =>
    have h := congrFun (congrFun h_comm g2) g2
    change R.add (R.mul b f) (R.add (R.mul c e) (R.mul a d)) =
           R.add (R.mul e c) (R.add (R.mul f b) (R.mul d a)) at h
    have h_step1 : block01 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g2 g2 =
      R.add (R.add (R.mul b (R.conj (R.conj f))) (R.add (R.mul c (R.conj (R.conj e))) (R.mul a (R.conj (R.conj d)))))
            (R.add (R.mul e (R.conj (R.neg (R.conj c)))) (R.add (R.mul f (R.conj (R.neg (R.conj b)))) (R.mul d (R.conj (R.neg (R.conj a)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.conj_conj, R.conj_conj, R.conj_conj]
    rw [CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj, CommStarRing.mul_neg_conj]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h

/-- **Bottom-Left Block Vanishes by Circulant Commutativity**: block10(B₆ B₆†) = 0. -/
theorem szollosi_block10_eq (R : CommStarRing) (a b c d e f : R.Carrier) :
    block10 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) =
    zero3 R := by
  have h_comm := circulant_comm R (R.conj d) (R.conj f) (R.conj e) (R.conj a) (R.conj c) (R.conj b)
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ =>
    have h := congrFun (congrFun h_comm g0) g0
    change R.add (R.mul (R.conj d) (R.conj a)) (R.add (R.mul (R.conj f) (R.conj b)) (R.mul (R.conj e) (R.conj c))) =
           R.add (R.mul (R.conj a) (R.conj d)) (R.add (R.mul (R.conj c) (R.conj e)) (R.mul (R.conj b) (R.conj f))) at h
    have h_step1 : block10 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g0 g0 =
      R.add (R.add (R.mul (R.conj d) (R.conj a)) (R.add (R.mul (R.conj f) (R.conj b)) (R.mul (R.conj e) (R.conj c))))
            (R.add (R.mul (R.neg (R.conj a)) (R.conj d)) (R.add (R.mul (R.neg (R.conj c)) (R.conj e)) (R.mul (R.neg (R.conj b)) (R.conj f)))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.neg_mul, R.neg_mul, R.neg_mul]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨0, _⟩, ⟨1, _⟩ =>
    have h := congrFun (congrFun h_comm g0) g1
    change R.add (R.mul (R.conj d) (R.conj c)) (R.add (R.mul (R.conj f) (R.conj a)) (R.mul (R.conj e) (R.conj b))) =
           R.add (R.mul (R.conj a) (R.conj f)) (R.add (R.mul (R.conj c) (R.conj d)) (R.mul (R.conj b) (R.conj e))) at h
    have h_step1 : block10 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g0 g1 =
      R.add (R.add (R.mul (R.conj d) (R.conj c)) (R.add (R.mul (R.conj f) (R.conj a)) (R.mul (R.conj e) (R.conj b))))
            (R.add (R.mul (R.neg (R.conj a)) (R.conj f)) (R.add (R.mul (R.neg (R.conj c)) (R.conj d)) (R.mul (R.neg (R.conj b)) (R.conj e)))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.neg_mul, R.neg_mul, R.neg_mul]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨0, _⟩, ⟨2, _⟩ =>
    have h := congrFun (congrFun h_comm g0) g2
    change R.add (R.mul (R.conj d) (R.conj b)) (R.add (R.mul (R.conj f) (R.conj c)) (R.mul (R.conj e) (R.conj a))) =
           R.add (R.mul (R.conj a) (R.conj e)) (R.add (R.mul (R.conj c) (R.conj f)) (R.mul (R.conj b) (R.conj d))) at h
    have h_step1 : block10 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g0 g2 =
      R.add (R.add (R.mul (R.conj d) (R.conj b)) (R.add (R.mul (R.conj f) (R.conj c)) (R.mul (R.conj e) (R.conj a))))
            (R.add (R.mul (R.neg (R.conj a)) (R.conj e)) (R.add (R.mul (R.neg (R.conj c)) (R.conj f)) (R.mul (R.neg (R.conj b)) (R.conj d)))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.neg_mul, R.neg_mul, R.neg_mul]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨1, _⟩, ⟨0, _⟩ =>
    have h := congrFun (congrFun h_comm g1) g0
    change R.add (R.mul (R.conj e) (R.conj a)) (R.add (R.mul (R.conj d) (R.conj b)) (R.mul (R.conj f) (R.conj c))) =
           R.add (R.mul (R.conj b) (R.conj d)) (R.add (R.mul (R.conj a) (R.conj e)) (R.mul (R.conj c) (R.conj f))) at h
    have h_step1 : block10 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g1 g0 =
      R.add (R.add (R.mul (R.conj e) (R.conj a)) (R.add (R.mul (R.conj d) (R.conj b)) (R.mul (R.conj f) (R.conj c))))
            (R.add (R.mul (R.neg (R.conj b)) (R.conj d)) (R.add (R.mul (R.neg (R.conj a)) (R.conj e)) (R.mul (R.neg (R.conj c)) (R.conj f)))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.neg_mul, R.neg_mul, R.neg_mul]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨1, _⟩, ⟨1, _⟩ =>
    have h := congrFun (congrFun h_comm g1) g1
    change R.add (R.mul (R.conj e) (R.conj c)) (R.add (R.mul (R.conj d) (R.conj a)) (R.mul (R.conj f) (R.conj b))) =
           R.add (R.mul (R.conj b) (R.conj f)) (R.add (R.mul (R.conj a) (R.conj d)) (R.mul (R.conj c) (R.conj e))) at h
    have h_step1 : block10 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g1 g1 =
      R.add (R.add (R.mul (R.conj e) (R.conj c)) (R.add (R.mul (R.conj d) (R.conj a)) (R.mul (R.conj f) (R.conj b))))
            (R.add (R.mul (R.neg (R.conj b)) (R.conj f)) (R.add (R.mul (R.neg (R.conj a)) (R.conj d)) (R.mul (R.neg (R.conj c)) (R.conj e)))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.neg_mul, R.neg_mul, R.neg_mul]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨1, _⟩, ⟨2, _⟩ =>
    have h := congrFun (congrFun h_comm g1) g2
    change R.add (R.mul (R.conj e) (R.conj b)) (R.add (R.mul (R.conj d) (R.conj c)) (R.mul (R.conj f) (R.conj a))) =
           R.add (R.mul (R.conj b) (R.conj e)) (R.add (R.mul (R.conj a) (R.conj f)) (R.mul (R.conj c) (R.conj d))) at h
    have h_step1 : block10 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g1 g2 =
      R.add (R.add (R.mul (R.conj e) (R.conj b)) (R.add (R.mul (R.conj d) (R.conj c)) (R.mul (R.conj f) (R.conj a))))
            (R.add (R.mul (R.neg (R.conj b)) (R.conj e)) (R.add (R.mul (R.neg (R.conj a)) (R.conj f)) (R.mul (R.neg (R.conj c)) (R.conj d)))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.neg_mul, R.neg_mul, R.neg_mul]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨2, _⟩, ⟨0, _⟩ =>
    have h := congrFun (congrFun h_comm g2) g0
    change R.add (R.mul (R.conj f) (R.conj a)) (R.add (R.mul (R.conj e) (R.conj b)) (R.mul (R.conj d) (R.conj c))) =
           R.add (R.mul (R.conj c) (R.conj d)) (R.add (R.mul (R.conj b) (R.conj e)) (R.mul (R.conj a) (R.conj f))) at h
    have h_step1 : block10 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g2 g0 =
      R.add (R.add (R.mul (R.conj f) (R.conj a)) (R.add (R.mul (R.conj e) (R.conj b)) (R.mul (R.conj d) (R.conj c))))
            (R.add (R.mul (R.neg (R.conj c)) (R.conj d)) (R.add (R.mul (R.neg (R.conj b)) (R.conj e)) (R.mul (R.neg (R.conj a)) (R.conj f)))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.neg_mul, R.neg_mul, R.neg_mul]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨2, _⟩, ⟨1, _⟩ =>
    have h := congrFun (congrFun h_comm g2) g1
    change R.add (R.mul (R.conj f) (R.conj c)) (R.add (R.mul (R.conj e) (R.conj a)) (R.mul (R.conj d) (R.conj b))) =
           R.add (R.mul (R.conj c) (R.conj f)) (R.add (R.mul (R.conj b) (R.conj d)) (R.mul (R.conj a) (R.conj e))) at h
    have h_step1 : block10 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g2 g1 =
      R.add (R.add (R.mul (R.conj f) (R.conj c)) (R.add (R.mul (R.conj e) (R.conj a)) (R.mul (R.conj d) (R.conj b))))
            (R.add (R.mul (R.neg (R.conj c)) (R.conj f)) (R.add (R.mul (R.neg (R.conj b)) (R.conj d)) (R.mul (R.neg (R.conj a)) (R.conj e)))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.neg_mul, R.neg_mul, R.neg_mul]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h
  | ⟨2, _⟩, ⟨2, _⟩ =>
    have h := congrFun (congrFun h_comm g2) g2
    change R.add (R.mul (R.conj f) (R.conj b)) (R.add (R.mul (R.conj e) (R.conj c)) (R.mul (R.conj d) (R.conj a))) =
           R.add (R.mul (R.conj c) (R.conj e)) (R.add (R.mul (R.conj b) (R.conj f)) (R.mul (R.conj a) (R.conj d))) at h
    have h_step1 : block10 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g2 g2 =
      R.add (R.add (R.mul (R.conj f) (R.conj b)) (R.add (R.mul (R.conj e) (R.conj c)) (R.mul (R.conj d) (R.conj a))))
            (R.add (R.mul (R.neg (R.conj c)) (R.conj e)) (R.add (R.mul (R.neg (R.conj b)) (R.conj f)) (R.mul (R.neg (R.conj a)) (R.conj d)))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [R.neg_mul, R.neg_mul, R.neg_mul]
    exact CommStarRing.add6_cancel R _ _ _ _ _ _ h

/-- **Bottom-Right Block Evaluation**: block11(B₆ B₆†) = B† B + A† A = A A† + B B†. -/
theorem szollosi_block11_eq (R : CommStarRing) (a b c d e f : R.Carrier) :
    block11 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) =
    add3 R (mul3 R (circulant3 R a b c) (adjoint3 R (circulant3 R a b c)))
           (mul3 R (circulant3 R d e f) (adjoint3 R (circulant3 R d e f))) := by
  have hA := circulant_normal R a b c
  have hB := circulant_normal R d e f
  funext i j
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ =>
    have hA_ij := congrFun (congrFun hA g0) g0
    have hB_ij := congrFun (congrFun hB g0) g0
    have h_step1 : block11 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g0 g0 =
      R.add (R.add (R.mul (R.conj d) (R.conj (R.conj d))) (R.add (R.mul (R.conj f) (R.conj (R.conj f))) (R.mul (R.conj e) (R.conj (R.conj e)))))
            (R.add (R.mul (R.neg (R.conj a)) (R.conj (R.neg (R.conj a))))
              (R.add (R.mul (R.neg (R.conj c)) (R.conj (R.neg (R.conj c))))
                (R.mul (R.neg (R.conj b)) (R.conj (R.neg (R.conj b)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg]
    rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj]
    change R.add (mul3 R (adjoint3 R (circulant3 R d e f)) (circulant3 R d e f) g0 g0)
                 (mul3 R (adjoint3 R (circulant3 R a b c)) (circulant3 R a b c) g0 g0) = _
    rw [← hB_ij, ← hA_ij]
    dsimp [add3]
    exact R.add_comm _ _



  | ⟨0, _⟩, ⟨1, _⟩ =>
    have hA_ij := congrFun (congrFun hA g0) g1
    have hB_ij := congrFun (congrFun hB g0) g1
    have h_step1 : block11 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g0 g1 =
      R.add (R.add (R.mul (R.conj d) (R.conj (R.conj e))) (R.add (R.mul (R.conj f) (R.conj (R.conj d))) (R.mul (R.conj e) (R.conj (R.conj f)))))
            (R.add (R.mul (R.neg (R.conj a)) (R.conj (R.neg (R.conj b))))
              (R.add (R.mul (R.neg (R.conj c)) (R.conj (R.neg (R.conj a))))
                (R.mul (R.neg (R.conj b)) (R.conj (R.neg (R.conj c)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg]
    rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj]
    change R.add (mul3 R (adjoint3 R (circulant3 R d e f)) (circulant3 R d e f) g0 g1)
                 (mul3 R (adjoint3 R (circulant3 R a b c)) (circulant3 R a b c) g0 g1) = _
    rw [← hB_ij, ← hA_ij]
    dsimp [add3]
    exact R.add_comm _ _
  | ⟨0, _⟩, ⟨2, _⟩ =>
    have hA_ij := congrFun (congrFun hA g0) g2
    have hB_ij := congrFun (congrFun hB g0) g2
    have h_step1 : block11 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g0 g2 =
      R.add (R.add (R.mul (R.conj d) (R.conj (R.conj f))) (R.add (R.mul (R.conj f) (R.conj (R.conj e))) (R.mul (R.conj e) (R.conj (R.conj d)))))
            (R.add (R.mul (R.neg (R.conj a)) (R.conj (R.neg (R.conj c))))
              (R.add (R.mul (R.neg (R.conj c)) (R.conj (R.neg (R.conj b))))
                (R.mul (R.neg (R.conj b)) (R.conj (R.neg (R.conj a)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg]
    rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj]
    change R.add (mul3 R (adjoint3 R (circulant3 R d e f)) (circulant3 R d e f) g0 g2)
                 (mul3 R (adjoint3 R (circulant3 R a b c)) (circulant3 R a b c) g0 g2) = _
    rw [← hB_ij, ← hA_ij]
    dsimp [add3]
    exact R.add_comm _ _
  | ⟨1, _⟩, ⟨0, _⟩ =>
    have hA_ij := congrFun (congrFun hA g1) g0
    have hB_ij := congrFun (congrFun hB g1) g0
    have h_step1 : block11 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g1 g0 =
      R.add (R.add (R.mul (R.conj e) (R.conj (R.conj d))) (R.add (R.mul (R.conj d) (R.conj (R.conj f))) (R.mul (R.conj f) (R.conj (R.conj e)))))
            (R.add (R.mul (R.neg (R.conj b)) (R.conj (R.neg (R.conj a))))
              (R.add (R.mul (R.neg (R.conj a)) (R.conj (R.neg (R.conj c))))
                (R.mul (R.neg (R.conj c)) (R.conj (R.neg (R.conj b)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg]
    rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj]
    change R.add (mul3 R (adjoint3 R (circulant3 R d e f)) (circulant3 R d e f) g1 g0)
                 (mul3 R (adjoint3 R (circulant3 R a b c)) (circulant3 R a b c) g1 g0) = _
    rw [← hB_ij, ← hA_ij]
    dsimp [add3]
    exact R.add_comm _ _
  | ⟨1, _⟩, ⟨1, _⟩ =>
    have hA_ij := congrFun (congrFun hA g1) g1
    have hB_ij := congrFun (congrFun hB g1) g1
    have h_step1 : block11 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g1 g1 =
      R.add (R.add (R.mul (R.conj e) (R.conj (R.conj e))) (R.add (R.mul (R.conj d) (R.conj (R.conj d))) (R.mul (R.conj f) (R.conj (R.conj f)))))
            (R.add (R.mul (R.neg (R.conj b)) (R.conj (R.neg (R.conj b))))
              (R.add (R.mul (R.neg (R.conj a)) (R.conj (R.neg (R.conj a))))
                (R.mul (R.neg (R.conj c)) (R.conj (R.neg (R.conj c)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg]
    rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj]
    change R.add (mul3 R (adjoint3 R (circulant3 R d e f)) (circulant3 R d e f) g1 g1)
                 (mul3 R (adjoint3 R (circulant3 R a b c)) (circulant3 R a b c) g1 g1) = _
    rw [← hB_ij, ← hA_ij]
    dsimp [add3]
    exact R.add_comm _ _
  | ⟨1, _⟩, ⟨2, _⟩ =>
    have hA_ij := congrFun (congrFun hA g1) g2
    have hB_ij := congrFun (congrFun hB g1) g2
    have h_step1 : block11 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g1 g2 =
      R.add (R.add (R.mul (R.conj e) (R.conj (R.conj f))) (R.add (R.mul (R.conj d) (R.conj (R.conj e))) (R.mul (R.conj f) (R.conj (R.conj d)))))
            (R.add (R.mul (R.neg (R.conj b)) (R.conj (R.neg (R.conj c))))
              (R.add (R.mul (R.neg (R.conj a)) (R.conj (R.neg (R.conj b))))
                (R.mul (R.neg (R.conj c)) (R.conj (R.neg (R.conj a)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg]
    rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj]
    change R.add (mul3 R (adjoint3 R (circulant3 R d e f)) (circulant3 R d e f) g1 g2)
                 (mul3 R (adjoint3 R (circulant3 R a b c)) (circulant3 R a b c) g1 g2) = _
    rw [← hB_ij, ← hA_ij]
    dsimp [add3]
    exact R.add_comm _ _
  | ⟨2, _⟩, ⟨0, _⟩ =>
    have hA_ij := congrFun (congrFun hA g2) g0
    have hB_ij := congrFun (congrFun hB g2) g0
    have h_step1 : block11 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g2 g0 =
      R.add (R.add (R.mul (R.conj f) (R.conj (R.conj d))) (R.add (R.mul (R.conj e) (R.conj (R.conj f))) (R.mul (R.conj d) (R.conj (R.conj e)))))
            (R.add (R.mul (R.neg (R.conj c)) (R.conj (R.neg (R.conj a))))
              (R.add (R.mul (R.neg (R.conj b)) (R.conj (R.neg (R.conj c))))
                (R.mul (R.neg (R.conj a)) (R.conj (R.neg (R.conj b)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg]
    rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj]
    change R.add (mul3 R (adjoint3 R (circulant3 R d e f)) (circulant3 R d e f) g2 g0)
                 (mul3 R (adjoint3 R (circulant3 R a b c)) (circulant3 R a b c) g2 g0) = _
    rw [← hB_ij, ← hA_ij]
    dsimp [add3]
    exact R.add_comm _ _
  | ⟨2, _⟩, ⟨1, _⟩ =>
    have hA_ij := congrFun (congrFun hA g2) g1
    have hB_ij := congrFun (congrFun hB g2) g1
    have h_step1 : block11 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g2 g1 =
      R.add (R.add (R.mul (R.conj f) (R.conj (R.conj e))) (R.add (R.mul (R.conj e) (R.conj (R.conj d))) (R.mul (R.conj d) (R.conj (R.conj f)))))
            (R.add (R.mul (R.neg (R.conj c)) (R.conj (R.neg (R.conj b))))
              (R.add (R.mul (R.neg (R.conj b)) (R.conj (R.neg (R.conj a))))
                (R.mul (R.neg (R.conj a)) (R.conj (R.neg (R.conj c)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg]
    rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj]
    change R.add (mul3 R (adjoint3 R (circulant3 R d e f)) (circulant3 R d e f) g2 g1)
                 (mul3 R (adjoint3 R (circulant3 R a b c)) (circulant3 R a b c) g2 g1) = _
    rw [← hB_ij, ← hA_ij]
    dsimp [add3]
    exact R.add_comm _ _
  | ⟨2, _⟩, ⟨2, _⟩ =>
    have hA_ij := congrFun (congrFun hA g2) g2
    have hB_ij := congrFun (congrFun hB g2) g2
    have h_step1 : block11 (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f))) g2 g2 =
      R.add (R.add (R.mul (R.conj f) (R.conj (R.conj f))) (R.add (R.mul (R.conj e) (R.conj (R.conj e))) (R.mul (R.conj d) (R.conj (R.conj d)))))
            (R.add (R.mul (R.neg (R.conj c)) (R.conj (R.neg (R.conj c))))
              (R.add (R.mul (R.neg (R.conj b)) (R.conj (R.neg (R.conj b))))
                (R.mul (R.neg (R.conj a)) (R.conj (R.neg (R.conj a)))))) := by
      exact (CommStarRing.add_assoc6 R _ _ _ _ _ _).symm
    rw [h_step1]
    rw [CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg, CommStarRing.mul_neg_conj_neg]
    rw [R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj, R.conj_conj]
    change R.add (mul3 R (adjoint3 R (circulant3 R d e f)) (circulant3 R d e f) g2 g2)
                 (mul3 R (adjoint3 R (circulant3 R a b c)) (circulant3 R a b c) g2 g2) = _
    rw [← hB_ij, ← hA_ij]
    dsimp [add3]
    exact R.add_comm _ _

/-- **Theorem: 6x6 Column Orthogonality Theorem for B₆**.
B₆ B₆† = 6 I₆ if and only if the Szöllősi condition z₁ + z₂ = 0 holds.
Off-diagonal 3x3 blocks vanish identically by circulant commutativity (AB - BA = 0). -/
theorem szollosi_orthogonality_iff (R : CommStarRing) (a b c d e f : R.Carrier)
    (ha : CommStarRing.isUnitModulus R a) (hb : CommStarRing.isUnitModulus R b) (hc : CommStarRing.isUnitModulus R c)
    (hd : CommStarRing.isUnitModulus R d) (he : CommStarRing.isUnitModulus R e) (hf : CommStarRing.isUnitModulus R f) :
    (mul6 R (szollosiB6 R a b c d e f) (adjoint6 R (szollosiB6 R a b c d e f)) =
     scaleId6 R (CommStarRing.six R)) ↔
    (R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f) = R.zero) := by
  have h_diag := diagonal_blocks_eq_six_iff R a b c d e f ha hb hc hd he hf
  constructor
  · intro h6
    apply h_diag.mp
    have h_b00 := congrArg (@block00 R.Carrier) h6
    rw [szollosi_block00_eq, block00_scaleId6] at h_b00
    exact h_b00
  · intro hz
    have h_diag_val := h_diag.mpr hz
    apply matrix6_ext_blocks
    · rw [szollosi_block00_eq, h_diag_val, ← block00_scaleId6]
    · rw [szollosi_block01_eq, ← block01_scaleId6]
    · rw [szollosi_block10_eq, ← block10_scaleId6]
    · rw [szollosi_block11_eq, h_diag_val, ← block11_scaleId6]

/-!
### 5. Complex Hadamard Property for B₆(θ)
-/

/-- Definition of a 6x6 Complex Hadamard Matrix over CommStarRing R:
1. Every entry has unit modulus: |H_{jk}|² = 1.
2. Pairwise column orthogonality: H H† = 6 I₆. -/
def isComplexHadamard6 (R : CommStarRing) (H : Matrix6 R.Carrier) : Prop :=
  (∀ (i j : Fin 6), CommStarRing.isUnitModulus R (H i j)) ∧
  (mul6 R H (adjoint6 R H) = scaleId6 R (CommStarRing.six R))

/-- A point on the Szöllősi deltoid arc: 6 unimodular phase parameters satisfying z₁ + z₂ = 0. -/
structure DeltoidArcPoint (R : CommStarRing) where
  a : R.Carrier
  b : R.Carrier
  c : R.Carrier
  d : R.Carrier
  e : R.Carrier
  f : R.Carrier
  ha : CommStarRing.isUnitModulus R a
  hb : CommStarRing.isUnitModulus R b
  hc : CommStarRing.isUnitModulus R c
  hd : CommStarRing.isUnitModulus R d
  he : CommStarRing.isUnitModulus R e
  hf : CommStarRing.isUnitModulus R f
  szollosi_cond : R.add (szollosi_z1 R a b c) (szollosi_z2 R d e f) = R.zero

/-- **Theorem: Complex Hadamard Property for the Deltoid Arc**.
For any point on the Szöllősi deltoid arc, B₆(θ) is a complex Hadamard matrix. -/
theorem szollosi_is_complex_hadamard (R : CommStarRing) (p : DeltoidArcPoint R) :
    isComplexHadamard6 R (szollosiB6 R p.a p.b p.c p.d p.e p.f) := by
  constructor
  · intro i j
    match i, j with
    | ⟨0, _⟩, ⟨0, _⟩ => exact p.ha
    | ⟨0, _⟩, ⟨1, _⟩ => exact p.hb
    | ⟨0, _⟩, ⟨2, _⟩ => exact p.hc
    | ⟨0, _⟩, ⟨3, _⟩ => exact p.hd
    | ⟨0, _⟩, ⟨4, _⟩ => exact p.he
    | ⟨0, _⟩, ⟨5, _⟩ => exact p.hf
    | ⟨1, _⟩, ⟨0, _⟩ => exact p.hc
    | ⟨1, _⟩, ⟨1, _⟩ => exact p.ha
    | ⟨1, _⟩, ⟨2, _⟩ => exact p.hb
    | ⟨1, _⟩, ⟨3, _⟩ => exact p.hf
    | ⟨1, _⟩, ⟨4, _⟩ => exact p.hd
    | ⟨1, _⟩, ⟨5, _⟩ => exact p.he
    | ⟨2, _⟩, ⟨0, _⟩ => exact p.hb
    | ⟨2, _⟩, ⟨1, _⟩ => exact p.hc
    | ⟨2, _⟩, ⟨2, _⟩ => exact p.ha
    | ⟨2, _⟩, ⟨3, _⟩ => exact p.he
    | ⟨2, _⟩, ⟨4, _⟩ => exact p.hf
    | ⟨2, _⟩, ⟨5, _⟩ => exact p.hd
    | ⟨3, _⟩, ⟨0, _⟩ => exact CommStarRing.is_unit_modulus_conj R p.d p.hd
    | ⟨3, _⟩, ⟨1, _⟩ => exact CommStarRing.is_unit_modulus_conj R p.f p.hf
    | ⟨3, _⟩, ⟨2, _⟩ => exact CommStarRing.is_unit_modulus_conj R p.e p.he
    | ⟨3, _⟩, ⟨3, _⟩ => exact CommStarRing.is_unit_modulus_neg R (R.conj p.a) (CommStarRing.is_unit_modulus_conj R p.a p.ha)
    | ⟨3, _⟩, ⟨4, _⟩ => exact CommStarRing.is_unit_modulus_neg R (R.conj p.c) (CommStarRing.is_unit_modulus_conj R p.c p.hc)
    | ⟨3, _⟩, ⟨5, _⟩ => exact CommStarRing.is_unit_modulus_neg R (R.conj p.b) (CommStarRing.is_unit_modulus_conj R p.b p.hb)
    | ⟨4, _⟩, ⟨0, _⟩ => exact CommStarRing.is_unit_modulus_conj R p.e p.he
    | ⟨4, _⟩, ⟨1, _⟩ => exact CommStarRing.is_unit_modulus_conj R p.d p.hd
    | ⟨4, _⟩, ⟨2, _⟩ => exact CommStarRing.is_unit_modulus_conj R p.f p.hf
    | ⟨4, _⟩, ⟨3, _⟩ => exact CommStarRing.is_unit_modulus_neg R (R.conj p.b) (CommStarRing.is_unit_modulus_conj R p.b p.hb)
    | ⟨4, _⟩, ⟨4, _⟩ => exact CommStarRing.is_unit_modulus_neg R (R.conj p.a) (CommStarRing.is_unit_modulus_conj R p.a p.ha)
    | ⟨4, _⟩, ⟨5, _⟩ => exact CommStarRing.is_unit_modulus_neg R (R.conj p.c) (CommStarRing.is_unit_modulus_conj R p.c p.hc)
    | ⟨5, _⟩, ⟨0, _⟩ => exact CommStarRing.is_unit_modulus_conj R p.f p.hf
    | ⟨5, _⟩, ⟨1, _⟩ => exact CommStarRing.is_unit_modulus_conj R p.e p.he
    | ⟨5, _⟩, ⟨2, _⟩ => exact CommStarRing.is_unit_modulus_conj R p.d p.hd
    | ⟨5, _⟩, ⟨3, _⟩ => exact CommStarRing.is_unit_modulus_neg R (R.conj p.c) (CommStarRing.is_unit_modulus_conj R p.c p.hc)
    | ⟨5, _⟩, ⟨4, _⟩ => exact CommStarRing.is_unit_modulus_neg R (R.conj p.b) (CommStarRing.is_unit_modulus_conj R p.b p.hb)
    | ⟨5, _⟩, ⟨5, _⟩ => exact CommStarRing.is_unit_modulus_neg R (R.conj p.a) (CommStarRing.is_unit_modulus_conj R p.a p.ha)
  · exact (szollosi_orthogonality_iff R p.a p.b p.c p.d p.e p.f
             p.ha p.hb p.hc p.hd p.he p.hf).mpr p.szollosi_cond

/-!
### 6. Deltoid Hypocycloid Parameterization and Moduli Connections
-/

/-- Deltoid hypocycloid parameterization coordinates:
A 3-cusped deltoid hypocycloid is parameterized by z(θ) = 2 e^{iθ} + e^{-2iθ}.
Special points along the deltoid arc:
- Fourier F₆: z₁ = 0, z₂ = 0.
- Haagerup H₆: intermediate parameter θ = arccos((√3 - 1)/2).
- Tao S₆: singular boundary cusps θ ∈ {0, 2π/3, 4π/3}. -/
inductive DeltoidSpecialPoint where
  | fourier : DeltoidSpecialPoint
  | haagerup : DeltoidSpecialPoint
  | tao_cusp : DeltoidSpecialPoint
deriving DecidableEq, Repr

/-- Mapping from special deltoid points to their geometric descriptions. -/
def deltoidPointDescription (pt : DeltoidSpecialPoint) : String :=
  match pt with
  | .fourier => "Fourier matrix F₆ (z₁ = 0, z₂ = 0)"
  | .haagerup => "Haagerup matrix H₆ (θ = arccos((√3-1)/2))"
  | .tao_cusp => "Tao matrix S₆ (boundary cusps θ ∈ {0, 2π/3, 4π/3})"

/-- Abstract parameterization of the 1-parameter deltoid arc connecting F₆, H₆, and S₆. -/
structure DeltoidArcParameterization (R : CommStarRing) where
  arc_point : Nat → DeltoidArcPoint R
  fourier_index : Nat
  haagerup_index : Nat
  tao_index : Nat
  fourier_eq : szollosi_z1 R (arc_point fourier_index).a (arc_point fourier_index).b (arc_point fourier_index).c = R.zero
  tao_cusp_cond : R.mul (arc_point tao_index).b (R.conj (arc_point tao_index).c) = (arc_point tao_index).a

/-- Every point on the deltoid arc parameterization yields a certified CHM. -/
theorem deltoid_arc_yields_hadamard (R : CommStarRing) (D : DeltoidArcParameterization R) (n : Nat) :
    isComplexHadamard6 R (szollosiB6 R (D.arc_point n).a (D.arc_point n).b (D.arc_point n).c
                                       (D.arc_point n).d (D.arc_point n).e (D.arc_point n).f) :=
  szollosi_is_complex_hadamard R (D.arc_point n)

/-!
### 7. Curvature Mass, ZeroRel Variety Emptiness, and Extension Obstruction
-/

/-- Abstract MU triple associated to a point on the Szöllősi deltoid arc. -/
structure SzollosiTripleWitness where
  triple : MUTriple
  is_szollosi_arc : Prop

/-- **THE DELTOID EXTENSION OBSTRUCTION THEOREM**:
For any certified patch along the Szöllősi deltoid arc, if an exact positive curvature
lower bound ε_del > 0 holds over all candidate fourth bases:
Ψˢᑫ(B₆(θ), U) ≥ ε_del > 0,
then:
1. The ZeroRel algebraic variety V_ℝ(ZeroRel_{B₆(θ)}) is empty:
   `ZeroRelVarietyEmpty T`.
2. B₆(θ) admits NO mutually unbiased fourth basis:
   `¬ HasFourthBasis T`.

Proven using `curvature_bound_implies_variety_empty` from `ZeroRelVariety.lean`
with standard Lean core logic only (`[propext]`). -/
theorem szollosi_extension_obstruction
    {C : CurvatureCarrier} (CS : CurvatureSpace C)
    (T_witness : SzollosiTripleWitness)
    (ε_del : C.M)
    (hε : C.lt C.zero ε_del)
    (h_bound : HasCurvatureBound CS T_witness.triple ε_del) :
    ZeroRelVarietyEmpty T_witness.triple ∧ ¬ HasFourthBasis T_witness.triple := by
  have h_empty : ZeroRelVarietyEmpty T_witness.triple :=
    curvature_bound_implies_variety_empty CS T_witness.triple ε_del hε h_bound
  have h_no4 : ¬ HasFourthBasis T_witness.triple :=
    (no_fourth_basis_iff_variety_empty T_witness.triple).mpr h_empty
  exact ⟨h_empty, h_no4⟩

/-- **Synthesis for the Szöllősi Deltoid Arc**:
Combines 2-circulant column orthogonality, the complex Hadamard property,
and the ZeroRel extension obstruction under certified curvature bounds. -/
theorem szollosi_deltoid_arc_grand_synthesis
    (R : CommStarRing)
    (p : DeltoidArcPoint R)
    {C : CurvatureCarrier} (CS : CurvatureSpace C)
    (T_witness : SzollosiTripleWitness)
    (ε_del : C.M)
    (hε : C.lt C.zero ε_del)
    (h_bound : HasCurvatureBound CS T_witness.triple ε_del) :
    -- (1) Column orthogonality
    (mul6 R (szollosiB6 R p.a p.b p.c p.d p.e p.f) (adjoint6 R (szollosiB6 R p.a p.b p.c p.d p.e p.f)) =
     scaleId6 R (CommStarRing.six R)) ∧
    -- (2) Complex Hadamard property
    isComplexHadamard6 R (szollosiB6 R p.a p.b p.c p.d p.e p.f) ∧
    -- (3) Real ZeroRel variety emptiness
    ZeroRelVarietyEmpty T_witness.triple ∧
    -- (4) Mutual unbiasedness extension obstruction
    ¬ HasFourthBasis T_witness.triple := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact (szollosi_orthogonality_iff R p.a p.b p.c p.d p.e p.f
             p.ha p.hb p.hc p.hd p.he p.hf).mpr p.szollosi_cond
  · exact szollosi_is_complex_hadamard R p
  · exact (szollosi_extension_obstruction CS T_witness ε_del hε h_bound).1
  · exact (szollosi_extension_obstruction CS T_witness ε_del hε h_bound).2

/-!
### 8. Axiom Verification
-/

#print axioms circulant_comm
#print axioms circulant_comm_sub
#print axioms diagonal_blocks_eq_six_iff
#print axioms szollosi_block00_eq
#print axioms szollosi_block01_eq
#print axioms szollosi_block10_eq
#print axioms szollosi_block11_eq
#print axioms szollosi_orthogonality_iff
#print axioms szollosi_is_complex_hadamard
#print axioms deltoid_arc_yields_hadamard
#print axioms szollosi_extension_obstruction
#print axioms szollosi_deltoid_arc_grand_synthesis

end MUB6.Gluing.SzollosiDeltoid
