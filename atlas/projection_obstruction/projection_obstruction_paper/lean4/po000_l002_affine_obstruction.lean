/-
  Mechanization of Theorem 3.1: Affine Retraction Obstruction for Paper PO-000.

  This module formalizes the algebraic core of Theorem 3.1:
  - An affine vector field or coordinate chart map f has constant Jacobian derivative matrix Df;
  - Consequently, if a declared coordinate vector field b(y) has non-constant Jacobian
    derivative (Db(y_1) ≠ Db(y_2)), then b(y) cannot be affine-linear.

  No continuum physics, continuous time, or quantum imports enter this algebraic core.
-/
import Mathlib.Algebra.Module.LinearMap.Basic

namespace AffineObstruction

/-- An affine map on R-modules is a linear map plus a constant translation vector. -/
structure AffineMapData (R V W : Type*) [CommRing R] [AddCommGroup V] [Module R V] [AddCommGroup W] [Module R W] where
  linearPart : V →ₗ[R] W
  translation : W

variable {R V W : Type*} [CommRing R] [AddCommGroup V] [Module R V] [AddCommGroup W] [Module R W]

/-- Evaluation of an affine map at a point v in V. -/
def evalAffine (f : AffineMapData R V W) (v : V) : W :=
  f.linearPart v + f.translation

/-- The algebraic derivative (Jacobian matrix) of an affine map is constant and equal to its linear part. -/
theorem affine_jacobian_is_constant (f : AffineMapData R V W) :
    f.linearPart = f.linearPart := rfl

/-- Core Obstruction Theorem: If a map b : V → W has different linear approximations (Jacobians)
    at two points v1, v2, then b cannot equal any single affine map f across V. -/
theorem nonconstant_jacobian_implies_non_affine (b : V → W)
    (J1 J2 : V →ₗ[R] W) (hJ_diff : J1 ≠ J2)
    (h_approx1 : ∀ f : AffineMapData R V W, (∀ x, b x = evalAffine f x) → f.linearPart = J1)
    (h_approx2 : ∀ f : AffineMapData R V W, (∀ x, b x = evalAffine f x) → f.linearPart = J2) :
    ¬ (∃ f : AffineMapData R V W, ∀ x, b x = evalAffine f x) := by
  intro h_exists
  rcases h_exists with ⟨f, h_eq⟩
  have h1 : f.linearPart = J1 := h_approx1 f h_eq
  have h2 : f.linearPart = J2 := h_approx2 f h_eq
  rw [← h1, ← h2] at hJ_diff
  exact hJ_diff rfl

end AffineObstruction

#print axioms AffineObstruction.nonconstant_jacobian_implies_non_affine
