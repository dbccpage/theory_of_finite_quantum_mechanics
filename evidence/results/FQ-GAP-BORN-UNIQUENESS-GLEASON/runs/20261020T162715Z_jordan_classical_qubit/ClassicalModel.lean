import CatalogueGeometry
import Mathlib.Analysis.Convex.StdSimplex

/-! Classical models in fixed affine coordinates. The affine basis is selected using the proved
finite-dimensional basis-existence theorem; this is a noncomputable coordinate choice, not a
new physical assumption or an unproved state-space contract. -/
noncomputable section
namespace FiniteQM.ClassicalModel
open Set ReconstructionGeometry ClassicalExclusion CatalogueGeometry

/-- A fixed affine basis with n+1 vertices in real affine dimension n. -/
def basis (n : ℕ) : AffineBasis (Fin (n+1)) ℝ (Space n) :=
  Classical.choice (AffineBasis.exists_affineBasis_of_finiteDimensional
    (k := ℝ) (V := Space n) (P := Space n) (by simp))

def states (n : ℕ) : Set (Space n) := convexHull ℝ (range (basis n))

theorem coord_nonneg {n : ℕ} {x : Space n} (hx : x ∈ states n) (i : Fin (n+1)) :
    0 ≤ (basis n).coord i x := by
  rw [states, (basis n).convexHull_eq_nonneg_coord] at hx
  exact hx i

theorem coord_le_one {n : ℕ} {x : Space n} (hx : x ∈ states n) (i : Fin (n+1)) :
    (basis n).coord i x ≤ 1 := by
  have h := Finset.single_le_sum (fun j (_ : j ∈ Finset.univ) => coord_nonneg hx j)
    (Finset.mem_univ i)
  simpa only [(basis n).sum_coord_apply_eq_one] using h

/-- A simplex coordinate equal to one uniquely identifies its vertex. -/
theorem coord_one_unique {n : ℕ} {x : Space n} (hx : x ∈ states n) (i : Fin (n+1))
    (heq : (basis n).coord i x = 1) : x = basis n i := by
  apply (basis n).ext_elem
  intro j
  by_cases hji : j = i
  · subst j; simpa using heq
  · have hs := Finset.sum_erase_add Finset.univ (fun k => (basis n).coord k x) (Finset.mem_univ i)
    have hzero : ∑ k ∈ Finset.univ.erase i, (basis n).coord k x = 0 := by
      rw [heq, (basis n).sum_coord_apply_eq_one] at hs
      linarith
    have hz := (Finset.sum_eq_zero_iff_of_nonneg
      (fun k (_ : k ∈ Finset.univ.erase i) => coord_nonneg hx k)).mp hzero j (by simp [hji])
    simpa [AffineBasis.coord_apply, hji, Ne.symm hji] using hz

theorem vertex_mem (n : ℕ) (i : Fin (n+1)) : basis n i ∈ states n :=
  subset_convexHull ℝ _ ⟨i, rfl⟩

theorem vertex_extreme (n : ℕ) (i : Fin (n+1)) : basis n i ∈ (states n).extremePoints ℝ := by
  apply extreme_of_unique_affine_max (states n) ((basis n).coord i) (basis n i) (vertex_mem n i)
  · intro x hx
    simpa using coord_le_one hx i
  · intro x hx hv
    apply coord_one_unique hx i
    simpa using hv

def coordEffect (n : ℕ) (i : Fin (n+1)) : Effect (states n) where
  functional := (basis n).coord i
  nonnegative := fun _ hx => coord_nonneg hx i
  bounded := fun _ hx => coord_le_one hx i

theorem vertex_frame (n : ℕ) : Frame (states n) (basis n) := by
  refine ⟨(basis n).ind.injective, vertex_extreme n, ?_⟩
  exact ⟨coordEffect n, (fun x _ => (basis n).sum_coord_apply_eq_one x),
    (fun i j => (basis n).coord_apply i j)⟩

/-- Capacity is proved by injectivity into the finite set of extreme vertices. -/
theorem frame_bound {n m : ℕ} (f : Fin m → Space n) (hf : Frame (states n) f) : m ≤ n+1 := by
  have hv : ∀ i, ∃ j : Fin (n+1), basis n j = f i := by
    intro i
    change f i ∈ range (basis n)
    exact extremePoints_convexHull_subset (hf.pure i)
  choose g hg using hv
  have inj : Function.Injective g := by
    intro i j hij
    apply hf.distinct
    rw [← hg i, ← hg j, hij]
  simpa using Fintype.card_le_of_injective g inj

def system (n : ℕ) : System n where
  states := states n
  nonempty := ⟨basis n 0, vertex_mem n 0⟩
  convex := convex_convexHull ℝ _
  compact := (Set.finite_range (basis n)).isCompact_convexHull ℝ
  full := by rw [states, affineSpan_convexHull]; exact (basis n).tot
  rank := n+1
  rank_pos := Nat.succ_pos n
  frame_bound := fun _ f hf => frame_bound f hf
  frame_attained := ⟨basis n, vertex_frame n⟩

theorem rank_eq (n : ℕ) : (system n).rank = n+1 := rfl
theorem dim_eq (n : ℕ) : (system n).dim = n+1 := rfl
theorem finite_polytope (n : ℕ) : FinitePolytope (system n).states :=
  ⟨range (basis n), Set.finite_range _, rfl⟩

theorem spectral (n : ℕ) : (system n).Spectral := by
  intro x hx
  exact ⟨n+1, basis n, vertex_frame n, hx⟩

/-- Barycentric coordinates are nonnegative normalized classical probabilities. -/
theorem coords_probability {n : ℕ} {x : Space n} (hx : x ∈ (system n).states) :
    (basis n).coords x ∈ stdSimplex ℝ (Fin (n+1)) :=
  ⟨fun i => coord_nonneg hx i, (basis n).sum_coord_apply_eq_one x⟩

theorem coords_reconstruct (n : ℕ) (x : Space n) :
    ∑ i, ((basis n).coord i x) • basis n i = x := by
  exact (basis n).linear_combination_coord_eq_self x

theorem pure_eq_vertices (n : ℕ) : (states n).extremePoints ℝ = range (basis n) := by
  apply Set.Subset.antisymm extremePoints_convexHull_subset
  rintro x ⟨i, rfl⟩
  exact vertex_extreme n i

/-- Onto, not merely an inclusion: the state model is exactly the probability simplex. -/
theorem coords_image (n : ℕ) : (basis n).coords '' states n = stdSimplex ℝ (Fin (n+1)) := by
  rw [states, (basis n).coords.image_convexHull, ← Set.range_comp']
  have hc : (fun i => (basis n).coords (basis n i)) =
      (fun i j : Fin (n+1) => if i = j then (1 : ℝ) else 0) := by
    funext i j
    simp [AffineBasis.coord_apply, eq_comm]
  rw [hc]
  exact convexHull_basis_eq_stdSimplex ℝ (Fin (n+1))

#print axioms pure_eq_vertices
#print axioms coords_image
#print axioms basis
#print axioms coord_nonneg
#print axioms coord_le_one
#print axioms coord_one_unique
#print axioms vertex_extreme
#print axioms vertex_frame
#print axioms frame_bound
#print axioms system
#print axioms rank_eq
#print axioms dim_eq
#print axioms finite_polytope
#print axioms spectral
#print axioms coords_probability
#print axioms coords_reconstruct
end FiniteQM.ClassicalModel