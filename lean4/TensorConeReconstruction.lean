import Mathlib.Analysis.Matrix.Order

/-!
General finite-dimensional cone-selection kernel.

The operational derivation of coordinates and controlled-shift reachability is
in TFQ-0410 and TFQ-0412. This file checks the cone step for an arbitrary finite
complex matrix size, with reachability and transport as explicit hypotheses.
It does not assert that primitive difference supplies these hypotheses.
-/

open Matrix
open scoped BigOperators ComplexOrder MatrixOrder

namespace TensorConeReconstruction

variable {n : Type*} [Fintype n]

def rankOne (v : n → ℂ) : Matrix n n ℂ := vecMulVec v (star v)

def quadratic (A : Matrix n n ℂ) (v : n → ℂ) : ℂ :=
  star v ⬝ᵥ (A *ᵥ v)

/-- Every positive matrix is a finite sum of unnormalized rank-one matrices. -/
theorem positive_mem_of_rankOne
    (K : Set (Matrix n n ℂ)) (hz : 0 ∈ K)
    (ha : ∀ A ∈ K, ∀ B ∈ K, A + B ∈ K)
    (hr : ∀ v : n → ℂ, rankOne v ∈ K)
    {A : Matrix n n ℂ} (hA : A.PosSemidef) : A ∈ K := by
  classical
  obtain ⟨B, rfl⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hA.nonneg
  have hsum : star B * B = ∑ i : n, rankOne (fun j => star (B i j)) := by
    ext j k
    simp [Matrix.sum_apply, rankOne, Matrix.mul_apply, Matrix.star_apply,
      Matrix.vecMulVec_apply]
  rw [hsum]
  exact Finset.sum_induction _ _ (fun A B hA hB => ha A hA B hB) hz (fun i _ => hr _)

/-- Rank-one preparation and all vector tests identify the entire positive cone. -/
theorem cone_eq_positive
    (K : Set (Matrix n n ℂ)) (hz : 0 ∈ K)
    (ha : ∀ A ∈ K, ∀ B ∈ K, A + B ∈ K)
    (hh : ∀ A ∈ K, A.IsHermitian)
    (hr : ∀ v : n → ℂ, rankOne v ∈ K)
    (hp : ∀ A ∈ K, ∀ v : n → ℂ, 0 ≤ quadratic A v) :
    K = {A | A.PosSemidef} := by
  ext A
  constructor
  · intro hA
    exact Matrix.PosSemidef.of_dotProduct_mulVec_nonneg (hh A hA) (hp A hA)
  · exact positive_mem_of_rankOne K hz ha hr

/-- Enough operational data to transport seed preparations and seed tests.
`forward` prepares the orbit and `backward` pulls a seed test onto that orbit.
No positive cone is built into either map's type.
-/
structure OrbitData (K : Set (Matrix n n ℂ)) (G : Type*) where
  seeds : Set (n → ℂ)
  vector : G → (n → ℂ) → (n → ℂ)
  forward : G → Matrix n n ℂ → Matrix n n ℂ
  backward : G → Matrix n n ℂ → Matrix n n ℂ
  seed_preparation : ∀ s ∈ seeds, rankOne s ∈ K
  seed_positive : ∀ A ∈ K, ∀ s ∈ seeds, 0 ≤ quadratic A s
  forward_preserves : ∀ g, ∀ A ∈ K, forward g A ∈ K
  backward_preserves : ∀ g, ∀ A ∈ K, backward g A ∈ K
  preparation_transport : ∀ g s, forward g (rankOne s) = rankOne (vector g s)
  test_transport : ∀ g A s, quadratic (backward g A) s = quadratic A (vector g s)
  reachability : ∀ v : n → ℂ, ∃ g s, s ∈ seeds ∧ vector g s = v

/-- Seed positivity plus reversible orbit reachability forces PSD, in every
finite dimension. The lower inclusion uses all reachable preparations. -/
theorem operational_orbit_selects_positive
    (K : Set (Matrix n n ℂ)) (hz : 0 ∈ K)
    (ha : ∀ A ∈ K, ∀ B ∈ K, A + B ∈ K)
    (hh : ∀ A ∈ K, A.IsHermitian)
    {G : Type*} (D : OrbitData K G) :
    K = {A | A.PosSemidef} := by
  apply cone_eq_positive K hz ha hh
  · intro v
    obtain ⟨g, s, hs, rfl⟩ := D.reachability v
    rw [← D.preparation_transport]
    exact D.forward_preserves g _ (D.seed_preparation s hs)
  · intro A hA v
    obtain ⟨g, s, hs, rfl⟩ := D.reachability v
    rw [← D.test_transport]
    exact D.seed_positive _ (D.backward_preserves g A hA) s hs

#print axioms positive_mem_of_rankOne
#print axioms cone_eq_positive
#print axioms operational_orbit_selects_positive

end TensorConeReconstruction
