import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Tactic.Module

/-!
The algebraic and positive-representation bridge of Lemma E.1.

The hypotheses below are the complex-bilinear extensions of B1's displayed
identities. `star` is conjugation on the complexification; `inner_j` and
`inner_l` are the sesquilinear extensions of (E2). Associativity, the
anti-multiplicative involution, faithfulness and positive squares are conclusions,
not hypotheses. Finite-dimensional closedness, spectral square roots, the
reverse cone inclusion and E.2--E.5 are not asserted by this module.
-/

namespace Po000JordanLie

open Complex

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [StarAddMonoid E] [StarModule ℂ E]

structure Data (E : Type*) [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [StarAddMonoid E] [StarModule ℂ E] where
  j : E →ₗ[ℂ] E →ₗ[ℂ] E
  l : E →ₗ[ℂ] E →ₗ[ℂ] E
  one : E
  j_comm : ∀ a b, j a b = j b a
  l_anti : ∀ a b, l a b = -l b a
  j_unit : ∀ a, j one a = a
  l_unit : ∀ a, l one a = 0
  jacobi : ∀ a b c, l a (l b c) + l b (l c a) + l c (l a b) = 0
  derivation : ∀ a b c, l a (j b c) = j (l a b) c + j b (l a c)
  associator : ∀ a b c, j (j a b) c - j a (j b c) = l b (l c a)
  star_j : ∀ a b, star (j a b) = j (star a) (star b)
  star_l : ∀ a b, star (l a b) = l (star a) (star b)
  inner_j : ∀ a b c, inner ℂ (j a b) c = inner ℂ b (j (star a) c)
  inner_l : ∀ a b c, inner ℂ (l a b) c = -inner ℂ b (l (star a) c)

namespace Data

variable (d : Data E)

def product (a b : E) : E := d.j a b + I • d.l a b

def left (a : E) : E →ₗ[ℂ] E := d.j a + I • d.l a

@[simp] theorem left_apply (a b : E) : d.left a b = d.product a b := rfl

theorem real_associator (a b c : E) :
    d.j (d.j a b) c - d.j a (d.j b c) - d.l (d.l a b) c + d.l a (d.l b c) = 0 := by
  rw [d.associator, d.l_anti (d.l a b) c]
  calc
    _ = d.l a (d.l b c) + d.l b (d.l c a) + d.l c (d.l a b) := by module
    _ = 0 := d.jacobi a b c

theorem imaginary_associator (a b c : E) :
    d.j (d.l a b) c + d.l (d.j a b) c - d.j a (d.l b c) - d.l a (d.j b c) = 0 := by
  rw [d.l_anti (d.j a b) c, d.derivation c a b, d.derivation a b c,
    d.l_anti c a, d.l_anti c b]
  simp only [map_neg, LinearMap.neg_apply]
  rw [d.j_comm (d.l a c) b]
  module

theorem product_associative (a b c : E) :
    d.product (d.product a b) c = d.product a (d.product b c) := by
  apply sub_eq_zero.mp
  calc
    _ = (d.j (d.j a b) c - d.j a (d.j b c) - d.l (d.l a b) c + d.l a (d.l b c)) +
        I • (d.j (d.l a b) c + d.l (d.j a b) c - d.j a (d.l b c) - d.l a (d.j b c)) := by
      simp only [product, map_add, map_smul, LinearMap.add_apply, LinearMap.smul_apply,
        smul_add, smul_smul, I_mul_I, neg_one_smul]
      module
    _ = 0 := by rw [d.real_associator, d.imaginary_associator]; simp

@[simp] theorem one_product (a : E) : d.product d.one a = a := by
  simp [product, d.j_unit, d.l_unit]

@[simp] theorem product_one (a : E) : d.product a d.one = a := by
  simp [product, d.j_comm a d.one, d.l_anti a d.one, d.j_unit, d.l_unit]

theorem star_product (a b : E) :
    star (d.product a b) = d.product (star b) (star a) := by
  simp only [product, star_add, star_smul, d.star_j, d.star_l, star_def, conj_I]
  rw [d.j_comm (star a) (star b), d.l_anti (star a) (star b)]
  module

omit [InnerProductSpace ℂ E] [StarModule ℂ E] in
theorem product_involution (a : E) : star (star a) = a := star_star a

theorem left_multiplicative (a b : E) :
    d.left (d.product a b) = (d.left a).comp (d.left b) := by
  ext c
  exact d.product_associative a b c

theorem left_faithful : Function.Injective d.left := by
  intro a b h
  have h' := congrArg (fun f : E →ₗ[ℂ] E => f d.one) h
  simpa using h'

theorem left_adjoint (a b c : E) :
    inner ℂ (d.left a b) c = inner ℂ b (d.left (star a) c) := by
  simp [left_apply, product, inner_add_left, inner_add_right,
    inner_smul_left, inner_smul_right, d.inner_j, d.inner_l]

theorem square_pairing (a b : E) :
    (inner ℂ b (d.left (d.product (star a) a) b)).re = ‖d.left a b‖ ^ 2 := by
  rw [d.left_multiplicative, LinearMap.comp_apply, ← d.left_adjoint]
  exact (norm_sq_eq_re_inner (𝕜 := ℂ) _).symm

theorem positive_square (a b : E) :
    0 ≤ (inner ℂ b (d.left (d.product (star a) a) b)).re := by
  rw [d.square_pairing]
  exact sq_nonneg _

theorem positive_jordan_square (a b : E) (ha : star a = a) :
    0 ≤ (inner ℂ b (d.left (d.j a a) b)).re := by
  have hz : d.l a a = 0 := by
    have h := d.l_anti a a
    have hh : (2 : ℂ) • d.l a a = 0 := by
      calc
        _ = d.l a a + d.l a a := by module
        _ = 0 := (congrArg (fun x => x + d.l a a) h).trans (neg_add_cancel _)
    exact (smul_eq_zero.mp hh).resolve_left (by norm_num)
  have hp := d.positive_square a b
  simpa [ha, product, hz] using hp

end Data

/-- The complexification of the real scalar system witnesses consistency of
the displayed identity package. No bare domain axiom is introduced. -/
noncomputable def scalarData : Data ℂ where
  j := LinearMap.mul ℂ ℂ
  l := 0
  one := 1
  j_comm := by intro a b; exact mul_comm a b
  l_anti := by intros; simp
  j_unit := by intro a; exact one_mul a
  l_unit := by intros; rfl
  jacobi := by intros; simp
  derivation := by intros; simp
  associator := by intros; simp [mul_assoc]
  star_j := by intros; simp
  star_l := by intros; simp
  inner_j := by intros; simp [RCLike.inner_apply]; ring
  inner_l := by intros; simp

theorem scalar_product (a b : ℂ) : scalarData.product a b = a * b := by
  simp [Data.product, scalarData]

end Po000JordanLie

#print axioms Po000JordanLie.Data.product_associative
#print axioms Po000JordanLie.Data.star_product
#print axioms Po000JordanLie.Data.product_involution
#print axioms Po000JordanLie.Data.left_multiplicative
#print axioms Po000JordanLie.Data.left_faithful
#print axioms Po000JordanLie.Data.left_adjoint
#print axioms Po000JordanLie.Data.positive_square
#print axioms Po000JordanLie.Data.positive_jordan_square
#print axioms Po000JordanLie.scalarData
#print axioms Po000JordanLie.scalar_product
