import BornEffectValuation
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Matrix.Basis
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.DotProduct
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.Ring.Unbundled.Basic
import Mathlib.Algebra.Order.Floor.Semiring
import Mathlib.Data.Rat.Floor
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Abel

/-
Matrix carrier for the effect-valuation interface `BornFinite.OrderedQUnit`.  AuthorityEffect: None.

Carrier.  V := Matrix (Fin n) (Fin n) ℚ, all n×n rational matrices (symmetry is NOT imposed).
Quadratic form qf A x := x ⬝ᵥ (A *ᵥ x).  Order: le A B := ∀ x, 0 ≤ qf (B - A) x, i.e. B - A is
positive semidefinite on rational points (`PsdQ`).  Unit: u := 1.

The order is a preorder (reflexive, transitive, translation- and scaling-compatible) but NOT a
partial order: a skew matrix A (Aᵀ = -A) has qf A x = 0 for every x, hence A ≤ 0 and 0 ≤ A while
A ≠ 0 in general (`skew_le_zero_and_ge`).  `OrderedQUnit` asks only for reflexivity and
transitivity, so `space n` is an honest instance of that interface.

Nothing physical is claimed.  The matrix algebra, its order, the order-unit bound, the rank-one
effects, and the trace representation of ℚ-linear functionals are supplied (standard finite linear
algebra over ℚ), not derived from any physical postulate.  No Born rule and no Gleason-type
uniqueness is proved here.  Everything is exact over ℚ; no real numbers, limits, or continuity.
-/

namespace BornFinite.MatrixCarrier

open Matrix

variable {n : ℕ}

/-! ### The quadratic form and its algebraic rules -/

/-- The quadratic form of `A` evaluated at the rational vector `x`. -/
def qf (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) : ℚ := x ⬝ᵥ (A *ᵥ x)

theorem qf_add (A B : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    qf (A + B) x = qf A x + qf B x := by
  unfold qf
  rw [Matrix.add_mulVec, dotProduct_add]

theorem qf_sub (A B : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    qf (A - B) x = qf A x - qf B x := by
  unfold qf
  rw [Matrix.sub_mulVec, dotProduct_sub]

theorem qf_neg (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) : qf (-A) x = -qf A x := by
  unfold qf
  rw [Matrix.neg_mulVec, dotProduct_neg]

theorem qf_smul (q : ℚ) (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    qf (q • A) x = q * qf A x := by
  unfold qf
  rw [Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul]

theorem qf_zero (x : Fin n → ℚ) : qf (0 : Matrix (Fin n) (Fin n) ℚ) x = 0 := by
  unfold qf
  rw [Matrix.zero_mulVec, dotProduct_zero]

theorem qf_one (x : Fin n → ℚ) : qf (1 : Matrix (Fin n) (Fin n) ℚ) x = x ⬝ᵥ x := by
  unfold qf
  rw [Matrix.one_mulVec]

theorem qf_eq_sum_sum (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    qf A x = ∑ i, ∑ j, x i * (A i j * x j) := by
  unfold qf
  simp only [dotProduct, Matrix.mulVec_apply_eq_sum, Finset.mul_sum]

theorem dot_self_nonneg (x : Fin n → ℚ) : 0 ≤ x ⬝ᵥ x := by
  unfold dotProduct
  exact Finset.sum_nonneg (fun i _ => mul_self_nonneg (x i))

theorem dot_self_pos {x : Fin n → ℚ} (hx : x ≠ 0) : 0 < x ⬝ᵥ x := by
  rcases (dot_self_nonneg x).lt_or_eq with h | h
  · exact h
  · exact absurd (dotProduct_self_eq_zero.mp h.symm) hx

theorem dot_self_eq_sum_sq (x : Fin n → ℚ) : x ⬝ᵥ x = ∑ i, x i ^ 2 := by
  unfold dotProduct
  simp only [sq]

/-! ### Positive semidefiniteness over rational points, and the ordered unit space -/

/-- Positive semidefinite on rational vectors: the exact finite notion used throughout. -/
def PsdQ (A : Matrix (Fin n) (Fin n) ℚ) : Prop := ∀ x, 0 ≤ qf A x

/-- The matrix carrier as an `OrderedQUnit`: `le A B` iff `B - A` is `PsdQ`, unit `1`. -/
def space (n : ℕ) : OrderedQUnit (Matrix (Fin n) (Fin n) ℚ) where
  le A B := PsdQ (B - A)
  le_refl A := by
    intro x
    rw [sub_self, qf_zero]
  le_trans A B C hAB hBC := by
    intro x
    have e : C - A = (C - B) + (B - A) := by abel
    rw [e, qf_add]
    exact add_nonneg (hBC x) (hAB x)
  add_le_add_right A B C h := by
    intro x
    have e : B + C - (A + C) = B - A := by abel
    rw [e]
    exact h x
  smul_nonneg q A hq hA := by
    intro x
    rw [sub_zero, qf_smul]
    have h := hA x
    rw [sub_zero] at h
    exact mul_nonneg hq h
  u := 1
  u_nonneg := by
    intro x
    rw [sub_zero, qf_one]
    exact dot_self_nonneg x

theorem space_le (A B : Matrix (Fin n) (Fin n) ℚ) : (space n).le A B ↔ PsdQ (B - A) := Iff.rfl

theorem space_u : (space n).u = 1 := rfl

theorem effect_iff (E : Matrix (Fin n) (Fin n) ℚ) :
    (space n).Effect E ↔ PsdQ E ∧ PsdQ (1 - E) := by
  show PsdQ (E - 0) ∧ PsdQ (1 - E) ↔ PsdQ E ∧ PsdQ (1 - E)
  rw [sub_zero]

theorem effect_iff' (E : Matrix (Fin n) (Fin n) ℚ) :
    (space n).Effect E ↔ ∀ x, 0 ≤ qf E x ∧ qf E x ≤ x ⬝ᵥ x := by
  rw [effect_iff]
  constructor
  · rintro ⟨h1, h2⟩ x
    refine ⟨h1 x, ?_⟩
    have h := h2 x
    rw [qf_sub, qf_one] at h
    linarith
  · intro h
    refine ⟨fun x => (h x).1, fun x => ?_⟩
    rw [qf_sub, qf_one]
    linarith [(h x).2]

/-! ### Order-unit bound: every matrix lies between `-k • 1` and `k • 1` -/

theorem sq_le_dot (x : Fin n → ℚ) (i : Fin n) : x i * x i ≤ x ⬝ᵥ x := by
  unfold dotProduct
  exact Finset.single_le_sum (f := fun j => x j * x j) (fun j _ => mul_self_nonneg (x j))
    (Finset.mem_univ i)

theorem abs_mul_le_dot (x : Fin n → ℚ) (i j : Fin n) : |x i * x j| ≤ x ⬝ᵥ x := by
  have hi := sq_le_dot x i
  have hj := sq_le_dot x j
  rw [abs_le]
  constructor
  · nlinarith [mul_self_nonneg (x i + x j)]
  · nlinarith [mul_self_nonneg (x i - x j)]

theorem abs_qf_le (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    |qf A x| ≤ (∑ i, ∑ j, |A i j|) * (x ⬝ᵥ x) := by
  rw [qf_eq_sum_sum, Finset.sum_mul]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun i _ => ?_)
  rw [Finset.sum_mul]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun j _ => ?_)
  calc |x i * (A i j * x j)| = |A i j| * |x i * x j| := by
        rw [← abs_mul]
        congr 1
        ring
    _ ≤ |A i j| * (x ⬝ᵥ x) := mul_le_mul_of_nonneg_left (abs_mul_le_dot x i j) (abs_nonneg _)

theorem order_unit (A : Matrix (Fin n) (Fin n) ℚ) :
    ∃ k : ℕ, (space n).le (-((k : ℚ) • (1 : Matrix (Fin n) (Fin n) ℚ))) A ∧
      (space n).le A ((k : ℚ) • (1 : Matrix (Fin n) (Fin n) ℚ)) := by
  obtain ⟨c, hc⟩ : ∃ c : ℚ, c = ∑ i, ∑ j, |A i j| := ⟨_, rfl⟩
  have hk : c ≤ (⌈c⌉₊ : ℚ) := Nat.le_ceil c
  refine ⟨⌈c⌉₊, ?_, ?_⟩
  · intro x
    have h := abs_qf_le A x
    rw [← hc] at h
    have hS := dot_self_nonneg x
    have hcS : c * (x ⬝ᵥ x) ≤ (⌈c⌉₊ : ℚ) * (x ⬝ᵥ x) := mul_le_mul_of_nonneg_right hk hS
    rw [sub_neg_eq_add, qf_add, qf_smul, qf_one]
    linarith [(abs_le.mp h).1]
  · intro x
    have h := abs_qf_le A x
    rw [← hc] at h
    have hS := dot_self_nonneg x
    have hcS : c * (x ⬝ᵥ x) ≤ (⌈c⌉₊ : ℚ) * (x ⬝ᵥ x) := mul_le_mul_of_nonneg_right hk hS
    rw [qf_sub, qf_smul, qf_one]
    linarith [(abs_le.mp h).2]

/-! ### Rank-one effects -/

theorem cauchy_schwarz (x y : Fin n → ℚ) : (x ⬝ᵥ y) ^ 2 ≤ (x ⬝ᵥ x) * (y ⬝ᵥ y) := by
  rw [dot_self_eq_sum_sq x, dot_self_eq_sum_sq y]
  unfold dotProduct
  exact Finset.sum_mul_sq_le_sq_mul_sq Finset.univ x y

/-- The rank-one matrix `(1 / (x ⬝ᵥ x)) • vecMulVec x x` (a projector when `x ≠ 0`). -/
def P (x : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ := (1 / (x ⬝ᵥ x)) • vecMulVec x x

theorem qf_vecMulVec (x y : Fin n → ℚ) : qf (vecMulVec x x) y = (x ⬝ᵥ y) ^ 2 := by
  rw [qf_eq_sum_sum, sq]
  unfold dotProduct
  rw [Finset.sum_mul_sum]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  rw [vecMulVec_apply]
  ring

theorem qf_rankOne (x y : Fin n → ℚ) : qf (P x) y = (x ⬝ᵥ y) ^ 2 / (x ⬝ᵥ x) := by
  unfold P
  rw [qf_smul, qf_vecMulVec, one_div_mul_eq_div]

theorem rankOne_effect {x : Fin n → ℚ} (hx : x ≠ 0) : (space n).Effect (P x) := by
  rw [effect_iff']
  intro y
  rw [qf_rankOne]
  have hpos := dot_self_pos hx
  constructor
  · exact div_nonneg (sq_nonneg _) hpos.le
  · rw [div_le_iff₀ hpos]
    calc (x ⬝ᵥ y) ^ 2 ≤ (x ⬝ᵥ x) * (y ⬝ᵥ y) := cauchy_schwarz x y
      _ = (y ⬝ᵥ y) * (x ⬝ᵥ x) := mul_comm _ _

/-! ### Trace representation of ℚ-linear functionals -/

/-- The matrix representing a linear functional `L`: `repMatrix L i j = L (single j i 1)`. -/
def repMatrix (L : Matrix (Fin n) (Fin n) ℚ →ₗ[ℚ] ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  Matrix.of fun i j => L (Matrix.single j i 1)

theorem repMatrix_apply (L : Matrix (Fin n) (Fin n) ℚ →ₗ[ℚ] ℚ) (i j : Fin n) :
    repMatrix L i j = L (Matrix.single j i 1) := rfl

theorem trace_mul_eq_sum (ρ A : Matrix (Fin n) (Fin n) ℚ) :
    Matrix.trace (ρ * A) = ∑ i, ∑ j, ρ i j * A j i := by
  simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply]

theorem trace_rep (L : Matrix (Fin n) (Fin n) ℚ →ₗ[ℚ] ℚ) (A : Matrix (Fin n) (Fin n) ℚ) :
    L A = Matrix.trace (repMatrix L * A) := by
  have hsingle : ∀ i j : Fin n,
      Matrix.single i j (A i j) = A i j • Matrix.single i j (1 : ℚ) := by
    intro i j
    rw [Matrix.smul_single, smul_eq_mul, mul_one]
  calc L A = L (∑ i, ∑ j, Matrix.single i j (A i j)) :=
        congrArg L (Matrix.matrix_eq_sum_single A)
    _ = ∑ i, ∑ j, A i j * L (Matrix.single i j (1 : ℚ)) := by
        rw [map_sum]
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [map_sum]
        refine Finset.sum_congr rfl fun j _ => ?_
        rw [hsingle, LinearMap.map_smul, smul_eq_mul]
    _ = ∑ i, ∑ j, repMatrix L j i * A i j := by
        refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
        rw [repMatrix_apply, mul_comm]
    _ = ∑ j, ∑ i, repMatrix L j i * A i j := Finset.sum_comm
    _ = Matrix.trace (repMatrix L * A) := (trace_mul_eq_sum _ _).symm

theorem rep_unique (ρ ρ' : Matrix (Fin n) (Fin n) ℚ)
    (h : ∀ A, Matrix.trace (ρ * A) = Matrix.trace (ρ' * A)) : ρ = ρ' := by
  ext i j
  have hij := h (Matrix.single j i 1)
  simpa [Matrix.trace_mul_single] using hij

theorem qf_eq_trace (ρ : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    x ⬝ᵥ (ρ *ᵥ x) = Matrix.trace (ρ * vecMulVec x x) := by
  rw [Matrix.mul_vecMulVec, Matrix.trace_vecMulVec, dotProduct_comm]

theorem qf_eq_trace' (ρ : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) :
    qf ρ x = Matrix.trace (ρ * vecMulVec x x) :=
  qf_eq_trace ρ x

/-! ### Non-antisymmetry: skew matrices are both `≤ 0` and `≥ 0` -/

theorem qf_eq_zero_of_skew {A : Matrix (Fin n) (Fin n) ℚ} (hA : Aᵀ = -A) (x : Fin n → ℚ) :
    qf A x = 0 := by
  have h : qf A x = -qf A x := by
    unfold qf
    calc x ⬝ᵥ (A *ᵥ x) = (x ᵥ* A) ⬝ᵥ x := dotProduct_mulVec x A x
      _ = (Aᵀ *ᵥ x) ⬝ᵥ x := by rw [Matrix.mulVec_transpose]
      _ = ((-A) *ᵥ x) ⬝ᵥ x := by rw [hA]
      _ = -(x ⬝ᵥ (A *ᵥ x)) := by rw [Matrix.neg_mulVec, neg_dotProduct, dotProduct_comm]
  linarith

theorem skew_le_zero_and_ge {A : Matrix (Fin n) (Fin n) ℚ} (hA : Aᵀ = -A) :
    (space n).le A 0 ∧ (space n).le 0 A := by
  constructor
  · intro x
    rw [zero_sub, qf_neg, qf_eq_zero_of_skew hA, neg_zero]
  · intro x
    rw [sub_zero, qf_eq_zero_of_skew hA]

end BornFinite.MatrixCarrier

#print axioms BornFinite.MatrixCarrier.qf
#print axioms BornFinite.MatrixCarrier.qf_add
#print axioms BornFinite.MatrixCarrier.qf_sub
#print axioms BornFinite.MatrixCarrier.qf_neg
#print axioms BornFinite.MatrixCarrier.qf_smul
#print axioms BornFinite.MatrixCarrier.qf_zero
#print axioms BornFinite.MatrixCarrier.qf_one
#print axioms BornFinite.MatrixCarrier.qf_eq_sum_sum
#print axioms BornFinite.MatrixCarrier.dot_self_nonneg
#print axioms BornFinite.MatrixCarrier.dot_self_pos
#print axioms BornFinite.MatrixCarrier.dot_self_eq_sum_sq
#print axioms BornFinite.MatrixCarrier.PsdQ
#print axioms BornFinite.MatrixCarrier.space
#print axioms BornFinite.MatrixCarrier.space_le
#print axioms BornFinite.MatrixCarrier.space_u
#print axioms BornFinite.MatrixCarrier.effect_iff
#print axioms BornFinite.MatrixCarrier.effect_iff'
#print axioms BornFinite.MatrixCarrier.sq_le_dot
#print axioms BornFinite.MatrixCarrier.abs_mul_le_dot
#print axioms BornFinite.MatrixCarrier.abs_qf_le
#print axioms BornFinite.MatrixCarrier.order_unit
#print axioms BornFinite.MatrixCarrier.cauchy_schwarz
#print axioms BornFinite.MatrixCarrier.P
#print axioms BornFinite.MatrixCarrier.qf_vecMulVec
#print axioms BornFinite.MatrixCarrier.qf_rankOne
#print axioms BornFinite.MatrixCarrier.rankOne_effect
#print axioms BornFinite.MatrixCarrier.repMatrix
#print axioms BornFinite.MatrixCarrier.repMatrix_apply
#print axioms BornFinite.MatrixCarrier.trace_mul_eq_sum
#print axioms BornFinite.MatrixCarrier.trace_rep
#print axioms BornFinite.MatrixCarrier.rep_unique
#print axioms BornFinite.MatrixCarrier.qf_eq_trace
#print axioms BornFinite.MatrixCarrier.qf_eq_trace'
#print axioms BornFinite.MatrixCarrier.qf_eq_zero_of_skew
#print axioms BornFinite.MatrixCarrier.skew_le_zero_and_ge
