import ClassicalExclusion
import ReconstructionArithmetic
import Mathlib.LinearAlgebra.AffineSpace.FiniteDimensional

/-!
A repaired geometric boundary for Row 8. The old bare System/global axioms are NOT imported.
Normalized states live in a compact convex full-affine-dimensional subset of real Euclidean space.
`dim` is the homogenized state dimension (affine dimension + 1), not a free label.
The catalogue/bridge below are explicit inputs. No catalogue instance or Jordan classification
proof is asserted. Numeric tags alone still do not define Jordan multiplication or a process theory.
-/
noncomputable section
namespace FiniteQM.ReconstructionGeometry
open Set ClassicalExclusion
open ReconstructionArithmetic

abbrev Space (n : ℕ) := EuclideanSpace ℝ (Fin n)

/-- An operational effect is an actual affine functional bounded by zero and one on states. -/
structure Effect {n : ℕ} (S : Set (Space n)) where
  functional : Space n →ᵃ[ℝ] ℝ
  nonnegative : ∀ x ∈ S, 0 ≤ functional x
  bounded : ∀ x ∈ S, functional x ≤ 1

/-- Ordered pure frames are perfectly distinguishable by a normalized measurement.
Injectivity prevents repeated-state capacity inflation. -/
structure Frame {n m : ℕ} (S : Set (Space n)) (f : Fin m → Space n) : Prop where
  distinct : Function.Injective f
  pure : ∀ i, f i ∈ S.extremePoints ℝ
  distinguishable : ∃ e : Fin m → Effect S,
    (∀ x ∈ S, ∑ i, (e i).functional x = 1) ∧
    (∀ i j, (e i).functional (f j) = if i = j then 1 else 0)

/-- Finite-dimensional normalized state space, with capacity witnessed by genuine frames. -/
structure System (n : ℕ) where
  states : Set (Space n)
  nonempty : states.Nonempty
  convex : Convex ℝ states
  compact : IsCompact states
  full : affineSpan ℝ states = ⊤
  rank : ℕ
  rank_pos : 0 < rank
  frame_bound : ∀ m (f : Fin m → Space n), Frame states f → m ≤ rank
  frame_attained : ∃ f : Fin rank → Space n, Frame states f

namespace System
/-- Dimension of the homogenized ordered state space. -/
def dim {n : ℕ} (_A : System n) : ℕ := n + 1
/-- Purity is derived from the actual state geometry. -/
def Pure {n : ℕ} (A : System n) (x : Space n) : Prop := x ∈ A.states.extremePoints ℝ

/-- Reversible transformations are affine automorphisms with state-preserving inverse. -/
structure Reversible {n : ℕ} (A : System n) where
  equivalence : Space n ≃ᵃ[ℝ] Space n
  image_states : equivalence '' A.states = A.states

/-- Identity, inverse, and composition inherit the laws of actual affine equivalences. -/
def Reversible.identity {n : ℕ} (A : System n) : Reversible A where
  equivalence := AffineEquiv.refl ℝ (Space n)
  image_states := by simp

def Reversible.inverse {n : ℕ} {A : System n} (r : Reversible A) : Reversible A where
  equivalence := r.equivalence.symm
  image_states := by
    calc
      r.equivalence.symm '' A.states = r.equivalence.symm '' (r.equivalence '' A.states) :=
        congrArg (fun S => r.equivalence.symm '' S) r.image_states.symm
      _ = A.states := by rw [Set.image_image]; simp

def Reversible.compose {n : ℕ} {A : System n} (r s : Reversible A) : Reversible A where
  equivalence := s.equivalence.trans r.equivalence
  image_states := by
    change (fun x => r.equivalence (s.equivalence x)) '' A.states = A.states
    rw [← Set.image_image, s.image_states, r.image_states]

/-- Spectrality uses genuine finite convex hulls of perfectly distinguishable pure frames. -/
def Spectral {n : ℕ} (A : System n) : Prop :=
  ∀ x ∈ A.states, ∃ m, ∃ f : Fin m → Space n, Frame A.states f ∧ x ∈ convexHull ℝ (range f)

/-- Strong symmetry is transitivity on ordered pure frames of each fixed size. -/
def StronglySymmetric {n : ℕ} (A : System n) : Prop :=
  ∀ m (f g : Fin m → Space n), Frame A.states f → Frame A.states g →
    ∃ r : Reversible A, ∀ i, r.equivalence (f i) = g i

theorem dim_pos {n : ℕ} (A : System n) : 0 < A.dim := Nat.succ_pos n
/-- A singleton state space has homogenized dimension one. This rules out the old
one-state/dimension-two phantom before any classification input is used. -/
theorem subsingleton_dim_one {n : ℕ} (A : System n) (h : A.states.Subsingleton) : A.dim = 1 := by
  let _ : Subsingleton (Space n) := AffineSubspace.subsingleton_of_subsingleton_span_eq_top h A.full
  have hn : n = 0 := by
    simpa using (Module.finrank_zero_of_subsingleton (R := ℝ) (M := Space n))
  simp [dim, hn]

/-- In a spectral capacity-one system, every state is extreme. -/
theorem rank_one_pure {n : ℕ} (A : System n) (hS : A.Spectral) (hr : A.rank = 1)
    {x : Space n} (hx : x ∈ A.states) : A.Pure x := by
  obtain ⟨m, f, hf, hxf⟩ := hS x hx
  have hm : m ≤ 1 := hr ▸ A.frame_bound m f hf
  have hmpos : 0 < m := by
    by_contra h
    have hmzero : m = 0 := by omega
    subst m
    simp at hxf
  have hmone : m = 1 := by omega
  subst m
  have h_range : range f = {f 0} := by
    ext y
    constructor
    · rintro ⟨i, rfl⟩
      have hi : i = 0 := Subsingleton.elim _ _
      simp [hi]
    · intro hy
      exact ⟨0, (Set.mem_singleton_iff.mp hy).symm⟩
  have hxeq : x = f 0 := by simpa [h_range] using hxf
  rw [hxeq]
  exact hf.pure 0

/-- The old phantom is impossible even as a spectral rank-one geometric system. -/
theorem rank_one_dim_one {n : ℕ} (A : System n) (hS : A.Spectral) (hr : A.rank = 1) :
    A.dim = 1 := by
  apply A.subsingleton_dim_one
  intro x hx y hy
  have hmid := A.convex.midpoint_mem hx hy
  have hp := A.rank_one_pure hS hr hmid
  have hxmid := hp.2 hx hy (midpoint_mem_openSegment x y)
  have hymid := hp.2 hy hx (by rw [midpoint_comm]; exact midpoint_mem_openSegment y x)
  exact hxmid.trans hymid.symm

end System

/-- Actual affine marginals and separately affine product preparations.
A product-effect/tensor theorem and rank multiplication are not silently assumed here. -/
structure Composite {a b c : ℕ} (A : System a) (B : System b) (AB : System c) where
  prod : Space a → Space b → Space c
  prod_mem : ∀ x ∈ A.states, ∀ y ∈ B.states, prod x y ∈ AB.states
  prod_left_affine : ∀ y ∈ B.states, ∃ f : Space a →ᵃ[ℝ] Space c, ∀ x, f x = prod x y
  prod_right_affine : ∀ x ∈ A.states, ∃ f : Space b →ᵃ[ℝ] Space c, ∀ y, f y = prod x y
  margA : Space c →ᵃ[ℝ] Space a
  margB : Space c →ᵃ[ℝ] Space b
  margA_mem : MapsTo margA AB.states A.states
  margB_mem : MapsTo margB AB.states B.states
  margA_prod : ∀ x ∈ A.states, ∀ y ∈ B.states, margA (prod x y) = x
  margB_prod : ∀ x ∈ A.states, ∀ y ∈ B.states, margB (prod x y) = y

namespace Composite
/-- RC-L2 at the System boundary: the fixed-state product section makes the marginal onto. -/
theorem marginal_image {a b c : ℕ} {A : System a} {B : System b} {AB : System c}
    (C : Composite A B AB) : C.margB '' AB.states = B.states := by
  obtain ⟨x, hx⟩ := A.nonempty
  exact image_eq_of_section C.margB C.margB_mem (C.prod x)
    (C.prod_mem x hx) (C.margB_prod x hx)

/-- Finite polytope composites have finite polytope marginals. -/
theorem marginal_finite_polytope {a b c : ℕ} {A : System a} {B : System b} {AB : System c}
    (C : Composite A B AB) (h : FinitePolytope AB.states) : FinitePolytope B.states := by
  rw [← C.marginal_image]
  exact affine_image_finite_polytope C.margB h

/-- RC-L5 for the repaired System: a marginal affinely equivalent to the ball excludes a
classical composite. This is stronger than simplex exclusion and needs no rank/dimension counts. -/
theorem no_polytope_composite_with_ball {a b c : ℕ}
    {A : System a} {B : System b} {AB : System c} (C : Composite A B AB)
    (e : Space b ≃ᵃ[ℝ] R3) (he : e '' B.states = ball3) : ¬ FinitePolytope AB.states := by
  intro h
  apply ball3_not_finite_polytope
  rw [← he]
  exact affine_image_finite_polytope e.toAffineMap (C.marginal_finite_polytope h)
end Composite

/-- A proof-bearing catalogue of real state models for the arithmetic classification tags.
This is an INPUT CONTRACT, not a construction of Jordan algebras from numeric labels.
Classical geometry and the qubit ball must be supplied, rather than inferred from dimensions. -/
structure JordanStateCatalogue where
  ambient : EJA → ℕ
  model : (J : EJA) → System (ambient J)
  model_dim : ∀ J, (model J).dim = J.dim
  model_rank : ∀ J, (model J).rank = J.rank
  classical_geometry : ∀ J, J.IsClassical → FinitePolytope (model J).states
  qubit_geometry : ∀ J s, J.summands = [s] → s.IsQubitAlgebra →
    ∃ e : Space (ambient J) ≃ᵃ[ℝ] R3, e '' (model J).states = ball3

/-- An actual affine representation in a supplied catalogue, preserving operational capacity. -/
structure Representation (catalogue : JordanStateCatalogue) {n : ℕ} (A : System n) where
  tag : EJA
  equivalence : Space n ≃ᵃ[ℝ] Space (catalogue.ambient tag)
  image_states : equivalence '' A.states = (catalogue.model tag).states
  rank_eq : A.rank = tag.rank

namespace Representation
/-- Dimension preservation is derived from the affine equivalence and catalogue calibration. -/
theorem dim_eq {catalogue : JordanStateCatalogue} {n : ℕ} {A : System n}
    (R : Representation catalogue A) : A.dim = R.tag.dim := by
  have hn := R.equivalence.linear.finrank_eq
  have hnm : n = catalogue.ambient R.tag := by simpa using hn
  rw [← catalogue.model_dim R.tag]
  exact congrArg (fun k => k + 1) hnm

theorem inverse_image_states {catalogue : JordanStateCatalogue} {n : ℕ} {A : System n}
    (R : Representation catalogue A) :
    R.equivalence.symm '' (catalogue.model R.tag).states = A.states := by
  rw [← R.image_states, Set.image_image]
  simp

/-- Classical tags imply actual finite convex generation only through supplied geometry. -/
theorem classical_polytope {catalogue : JordanStateCatalogue} {n : ℕ} {A : System n}
    (R : Representation catalogue A) (h : R.tag.IsClassical) : FinitePolytope A.states := by
  rw [← R.inverse_image_states]
  exact affine_image_finite_polytope R.equivalence.symm.toAffineMap
    (catalogue.classical_geometry R.tag h)

theorem qubit_ball {catalogue : JordanStateCatalogue} {n : ℕ} {A : System n}
    (R : Representation catalogue A) {s : SimpleEJA}
    (hs : R.tag.summands = [s]) (hq : s.IsQubitAlgebra) :
    ∃ e : Space n ≃ᵃ[ℝ] R3, e '' A.states = ball3 := by
  obtain ⟨e, he⟩ := catalogue.qubit_geometry R.tag s hs hq
  refine ⟨R.equivalence.trans e, ?_⟩
  change (fun x => e (R.equivalence x)) '' A.states = ball3
  rw [← Set.image_image, R.image_states, he]
end Representation

/-- Safe replacement for the unrestricted global Jordan axiom. The genuine geometric
hypotheses are required and the output is a real affine representation. No instance is asserted.
The simple-or-classical conclusion is also explicit rather than another global axiom. -/
structure JordanBridge (catalogue : JordanStateCatalogue) : Prop where
  classify : ∀ {n} (A : System n), A.Spectral → A.StronglySymmetric →
    ∃ R : Representation catalogue A, R.tag.IsSimple ∨ R.tag.IsClassical

/-- The former `AXIOM[elem]`, now proved from the affine models and marginal section.
The Jordan bridge itself is not needed once representations have been supplied. -/
theorem no_classical_composite_with_qubit {catalogue : JordanStateCatalogue}
    {a b c : ℕ} {A : System a} {B : System b} {AB : System c}
    (C : Composite A B AB) (RAB : Representation catalogue AB)
    (RB : Representation catalogue B) {s : SimpleEJA}
    (hs : RB.tag.summands = [s]) (hq : s.IsQubitAlgebra) : ¬ RAB.tag.IsClassical := by
  obtain ⟨e, he⟩ := RB.qubit_ball hs hq
  intro hc
  exact C.no_polytope_composite_with_ball e he (RAB.classical_polytope hc)

/-- Arithmetic qubit selection survives, with its geometric meaning supplied by the catalogue. -/
theorem rank_two_dim_four_ball {catalogue : JordanStateCatalogue} {n : ℕ} {A : System n}
    (R : Representation catalogue A) (hr : A.rank = 2) (hd : A.dim = 4) :
    ∃ e : Space n ≃ᵃ[ℝ] R3, e '' A.states = ball3 := by
  obtain ⟨s, hs, hq⟩ := qubit_algebra R.tag (R.rank_eq ▸ hr) (R.dim_eq ▸ hd)
  exact R.qubit_ball hs hq

/-- Full classical-factor exclusion combines the preserved counting lemma with the new
geometric exclusion. Dimension and rank composition laws are explicit hypotheses; they have
not been derived from a dimension-only surrogate for local tomography. -/
theorem no_classical_factor_with_qubit {catalogue : JordanStateCatalogue}
    {a b c : ℕ} {A : System a} {B : System b} {AB : System c}
    (C : Composite A B AB) (RA : Representation catalogue A)
    (RB : Representation catalogue B) (RAB : Representation catalogue AB)
    (dichotomy : RAB.tag.IsSimple ∨ RAB.tag.IsClassical)
    (dimension_mul : AB.dim = A.dim * B.dim)
    (rank_lower_bound : A.rank * B.rank ≤ AB.rank)
    (nontrivial : 2 ≤ A.rank) (qubit_rank : B.rank = 2) (qubit_dim : B.dim = 4) :
    ¬ RA.tag.IsClassical := by
  intro hc
  have ha : A.dim = A.rank := RA.dim_eq.trans
    ((EJA.classical_dim_eq_rank RA.tag hc).trans RA.rank_eq.symm)
  rcases dichotomy with hs | hs
  · obtain ⟨s, hsingle⟩ := hs
    have hw := RAB.tag.wf s (by simp [hsingle])
    have hd : s.dim = 4 * A.rank := by
      have h := RAB.dim_eq.symm.trans dimension_mul
      simpa [EJA.dim, hsingle, sumDim, ha, qubit_dim, Nat.mul_comm] using h
    have hr : 2 * A.rank ≤ s.rank := by
      have h := rank_lower_bound
      rw [qubit_rank, RAB.rank_eq] at h
      simpa [EJA.rank, hsingle, sumRank, Nat.mul_comm] using h
    exact no_simple_dim4m_rank2m A.rank nontrivial s hw hd hr
  · obtain ⟨e, he⟩ := rank_two_dim_four_ball RB qubit_rank qubit_dim
    exact C.no_polytope_composite_with_ball e he (RAB.classical_polytope hs)

#print axioms System.Reversible.identity
#print axioms System.Reversible.inverse
#print axioms System.Reversible.compose
#print axioms System.dim_pos
#print axioms System.subsingleton_dim_one
#print axioms System.rank_one_pure
#print axioms System.rank_one_dim_one
#print axioms Composite.marginal_image
#print axioms Composite.marginal_finite_polytope
#print axioms Composite.no_polytope_composite_with_ball
#print axioms Representation.dim_eq
#print axioms Representation.inverse_image_states
#print axioms Representation.classical_polytope
#print axioms Representation.qubit_ball
#print axioms no_classical_composite_with_qubit
#print axioms rank_two_dim_four_ball
#print axioms no_classical_factor_with_qubit
end FiniteQM.ReconstructionGeometry