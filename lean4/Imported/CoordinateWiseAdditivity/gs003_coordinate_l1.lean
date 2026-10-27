/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 167995fc4b15e64d0b383d40798c44fa5bdb858ba1ff86cbb20fc7e0195e3d8c (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.CoordinateWiseAdditivity.gs003_coordinate_l1
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Real.Basic
import Imported.CoordinateWiseAdditivity.primitive_difference

/-!
# Paper 004 — Coordinate-Wise Additivity and the L1 Norm

Lean4 mechanization of finite LGGR/EPK consequences from
"Coordinate-Wise Additivity and the L1 Norm on Finite Graph Cochains"
(Carroll, 2026).

## Main results

* `lggr_edgewise_uniformity_obstruction` — one-edge LGGR corollary:
  edgewise ℓ¹ diagnostics descend through the local quotient, while
  diagnostic-plus-weight data need not descend.

* `lggr_edgewise_uniformity_obstruction_succ` — the same LGGR obstruction on
  every nonempty finite edge set.

* `ce1_quadratic_not_l1_scalar`, `ce2_weighted_l1_not_uniform`,
  `ce3_cross_edge_coupling_not_edge_local`,
  `ce4_orbit_weighted_not_unweighted`, and `ce5_lp_not_homogeneous` —
  concrete arithmetic witnesses for the independence of Paper 004 hypotheses.

* `edge_uniformity_collapses_two_edge_l1` and
  `edge_uniformity_collapses_finite_l1` — arithmetic cores of Theorem 3:
  uniform weights collapse weighted ℓ¹ sums to scalar unweighted ℓ¹ sums.

* `coord_nat_l1_weighted_sum` and `coord_nat_l1_scalar_sum_succ` — positive
  finite-coordinate cores of Theorem 1: disjoint-coordinate additivity plus
  one-coordinate homogeneity gives the weighted coordinatewise ℓ¹ sum, and
  coordinate symmetry collapses it to a scalar ℓ¹ form on nonempty coordinate
  sets.

* `coord_real_l1_weighted_sum`, `coord_real_l1_scalar_sum_succ`,
  `coord_real_l1_exists_scalar_succ`, and
  `coord_real_l1_norm_scalar_positive_succ` — real finite-coordinate cores of
  Theorem 1 with absolute values, a nonnegative scalar witness, and the
  norm-strengthened positive-scalar refinement.

* `orbit_weight_eq_of_isometric_single_edge_invariance`,
  `orbit_weighted_l1_aggregation`, and `orbit_uniform_l1_collapse` — finite
  declared-orbit cores of Theorems 2 and 3: isometric single-edge invariance
  forces equal edge weights, orbit-indexed weights aggregate the global gauge,
  and orbit-uniform weights collapse to one scalar ℓ¹ total.

* `epk_local_kernel_does_not_determine_weighted_total` — the local diagnostic
  quotient does not determine the weighted global total.

* `diagnostic_and_weighted_total_do_not_factor_through_local_kernel_succ` —
  the coarse local kernel cannot factor the joint diagnostic-plus-weighted-total
  payload on any nonempty finite edge set.

* `epk_weighted_total_factors_when_kernel_declares_weights` and
  `diagnostic_and_weighted_total_factor_when_kernel_declares_weights` — the
  refined-kernel repair: once weights are declared in the kernel, the weighted
  total and the joint diagnostic-plus-total payload factor through the refined
  quotient.

* `weighted_quotient_projects_to_local_quotient` and
  `local_quotient_does_not_lift_to_weighted_quotient_succ` — the quotient
  refinement boundary: the refined diagnostic+weight quotient projects to the
  local diagnostic quotient, but the local quotient cannot reconstruct the
  refined quotient on nonempty edge sets.

* `scalar_total_lggr_obstruction_succ` — the scalar aggregate LGGR form:
  the unweighted diagnostic total factors through the local quotient, while
  the paired unweighted/weighted scalar totals do not.

* `uniform_weighted_total_factors_through_local_kernel` and
  `uniform_scalar_pair_factors_through_local_kernel` — the positive repair
  boundary: once the scalar weight is explicitly declared uniform, the induced
  weighted aggregate, alone or paired with the unweighted total, again factors
  through the local quotient.

* `cochainTotalPD`, `total_quotient_projects_to_local_quotient`,
  `weighted_quotient_projects_to_total_quotient`, and the corresponding
  non-lift theorems — the intermediate EPK ladder: declaring only the weighted
  scalar total is strictly finer than the local diagnostic quotient and
  strictly coarser than declaring the full weight profile.

The full Lean formalization of Paper 004 Theorems 1–3 over real cochains
remains PL-004-2. This file mechanizes finite arithmetic cores and the
primitive-difference quotient boundary used by the paper and encyclopedia.
-/

namespace PaperGS003

open Finset BigOperators

/-!
## Section 1: Theorem 1 Axiom Structure (Documentation)
-/

/-- The axiom bundle for Theorem 1. A function `ν` on a finite coordinate
    space satisfying seminorm absolute homogeneity, coordinate permutation
    symmetry, and disjoint-coordinate additivity is forced to be w·‖x‖₁. -/
structure CoordL1Axioms (k : Nat) where
  /-- The seminorm function on ℝ^k (abstract finite proxy). -/
  ν : (Fin k → Int) → Int
  /-- Non-negativity. -/
  nonneg : ∀ x : Fin k → Int, 0 ≤ ν x
  /-- ν(0) = 0. -/
  map_zero : ν (fun _ => 0) = 0
  /-- All standard basis vectors have equal ν by coordinate symmetry. -/
  basis_equal : ∀ i j : Fin k,
    ν (fun m => if m = i then 1 else 0) =
      ν (fun m => if m = j then 1 else 0)

/-- Standard positive-coordinate basis vector used by the finite arithmetic
    core of Theorem 1. -/
def natBasis {k : Nat} (i : Fin k) : Fin k → Nat :=
  fun j => if j = i then 1 else 0

/-- Restrict a finite coordinate vector to a finite coordinate set. -/
def natRestrict {k : Nat} (x : Fin k → Nat) (s : Finset (Fin k)) :
    Fin k → Nat :=
  fun i => if i ∈ s then x i else 0

/-- Positive-coordinate finite proxy for the hypotheses of Theorem 1.

This bundle is deliberately weaker than a full real seminorm formalization:
it captures the finite decomposition step used by the paper, while PL-004-2
keeps the remaining real/sign/orbit bridge open. -/
structure CoordNatL1Axioms (k : Nat) where
  /-- The finite positive-coordinate gauge. -/
  ν : (Fin k → Nat) → Nat
  /-- Zero vector has zero gauge. -/
  map_zero : ν (fun _ => 0) = 0
  /-- Additivity over vectors with disjoint coordinate support. -/
  disjoint_add : ∀ x y : Fin k → Nat,
    (∀ i, x i = 0 ∨ y i = 0) →
      ν (fun i => x i + y i) = ν x + ν y
  /-- Positive-coordinate homogeneity on a single coordinate axis. -/
  coord_hom : ∀ (i : Fin k) (n : Nat),
    ν (fun j => if j = i then n else 0) = n * ν (natBasis i)
  /-- Coordinate symmetry makes all basis weights equal. -/
  basis_equal : ∀ i j : Fin k, ν (natBasis i) = ν (natBasis j)

/-- **Theorem 1 positive-coordinate core.** Under finite disjoint-coordinate
    additivity and one-coordinate homogeneity, the gauge decomposes as the
    weighted coordinatewise ℓ¹ sum. -/
theorem coord_nat_l1_weighted_sum {k : Nat}
    (A : CoordNatL1Axioms k) (x : Fin k → Nat) :
    A.ν x = ∑ i : Fin k, x i * A.ν (natBasis i) := by
  have hrestrict :
      ∀ s : Finset (Fin k),
        A.ν (natRestrict x s) =
          s.sum (fun i => x i * A.ν (natBasis i)) := by
    intro s
    refine Finset.induction_on s ?base ?step
    · have hzero : natRestrict x ∅ = fun _ => 0 := by
        funext i
        simp [natRestrict]
      rw [hzero, A.map_zero]
      simp
    · intro a s ha ih
      have hdecomp :
          natRestrict x (insert a s) =
            fun i => natRestrict x s i + (if i = a then x a else 0) := by
        funext i
        by_cases hia : i = a
        · subst i
          simp [natRestrict, ha]
        · simp [natRestrict, hia]
      rw [hdecomp]
      have hdisj :
          ∀ i : Fin k, natRestrict x s i = 0 ∨
            (if i = a then x a else 0) = 0 := by
        intro i
        by_cases hia : i = a
        · subst i
          left
          simp [natRestrict, ha]
        · right
          simp [hia]
      rw [A.disjoint_add (natRestrict x s)
        (fun i => if i = a then x a else 0) hdisj]
      rw [ih]
      rw [A.coord_hom a (x a)]
      rw [Finset.sum_insert ha]
      exact Nat.add_comm _ _
  have hfull : natRestrict x Finset.univ = x := by
    funext i
    simp [natRestrict]
  simpa [hfull] using hrestrict Finset.univ

/-- **Theorem 1 scalar positive-coordinate core.** On a nonempty finite
    coordinate set, coordinate symmetry collapses the weighted decomposition
    to a scalar multiple of the positive-coordinate ℓ¹ sum. -/
theorem coord_nat_l1_scalar_sum_succ (n : Nat)
    (A : CoordNatL1Axioms (Nat.succ n))
    (x : Fin (Nat.succ n) → Nat) :
    A.ν x =
      A.ν (natBasis ⟨0, Nat.succ_pos n⟩) * (∑ i : Fin (Nat.succ n), x i) := by
  rw [coord_nat_l1_weighted_sum A x]
  have hweights :
      ∀ i : Fin (Nat.succ n),
        A.ν (natBasis i) = A.ν (natBasis ⟨0, Nat.succ_pos n⟩) := by
    intro i
    exact A.basis_equal i ⟨0, Nat.succ_pos n⟩
  simp_rw [hweights]
  rw [show
      (∑ i : Fin (Nat.succ n), x i * A.ν (natBasis ⟨0, Nat.succ_pos n⟩)) =
        ∑ i : Fin (Nat.succ n), A.ν (natBasis ⟨0, Nat.succ_pos n⟩) * x i by
    apply Finset.sum_congr rfl
    intro i _hi
    exact Nat.mul_comm (x i) (A.ν (natBasis ⟨0, Nat.succ_pos n⟩))]
  rw [← Finset.mul_sum]

/-- Standard real-coordinate basis vector used by the finite real core of
    Theorem 1. -/
def realBasis {k : Nat} (i : Fin k) : Fin k → ℝ :=
  fun j => if j = i then 1 else 0

/-- Restrict a finite real coordinate vector to a finite coordinate set. -/
def realRestrict {k : Nat} (x : Fin k → ℝ) (s : Finset (Fin k)) :
    Fin k → ℝ :=
  fun i => if i ∈ s then x i else 0

/-- Real finite-coordinate hypotheses for the local Theorem 1 proof.

This is the direct finite real-cochain core: disjoint-coordinate additivity plus
one-axis absolute homogeneity gives the weighted ℓ¹ decomposition. -/
structure CoordRealL1Axioms (k : Nat) where
  /-- The finite real-coordinate gauge. -/
  ν : (Fin k → ℝ) → ℝ
  /-- Non-negativity. -/
  nonneg : ∀ x : Fin k → ℝ, 0 ≤ ν x
  /-- Zero vector has zero gauge. -/
  map_zero : ν (fun _ => 0) = 0
  /-- Additivity over vectors with disjoint coordinate support. -/
  disjoint_add : ∀ x y : Fin k → ℝ,
    (∀ i, x i = 0 ∨ y i = 0) →
      ν (fun i => x i + y i) = ν x + ν y
  /-- Absolute homogeneity on each coordinate axis. -/
  coord_hom : ∀ (i : Fin k) (r : ℝ),
    ν (fun j => if j = i then r else 0) = |r| * ν (realBasis i)
  /-- Coordinate symmetry makes all basis weights equal. -/
  basis_equal : ∀ i j : Fin k, ν (realBasis i) = ν (realBasis j)

/-- **Theorem 1 real finite-coordinate core.** Under finite disjoint-coordinate
    additivity and coordinate-axis absolute homogeneity, the gauge decomposes
    as the weighted coordinatewise ℓ¹ sum. -/
theorem coord_real_l1_weighted_sum {k : Nat}
    (A : CoordRealL1Axioms k) (x : Fin k → ℝ) :
    A.ν x = ∑ i : Fin k, |x i| * A.ν (realBasis i) := by
  have hrestrict :
      ∀ s : Finset (Fin k),
        A.ν (realRestrict x s) =
          s.sum (fun i => |x i| * A.ν (realBasis i)) := by
    intro s
    refine Finset.induction_on s ?base ?step
    · have hzero : realRestrict x ∅ = fun _ => 0 := by
        funext i
        simp [realRestrict]
      rw [hzero, A.map_zero]
      simp
    · intro a s ha ih
      have hdecomp :
          realRestrict x (insert a s) =
            fun i => realRestrict x s i + (if i = a then x a else 0) := by
        funext i
        by_cases hia : i = a
        · subst i
          simp [realRestrict, ha]
        · simp [realRestrict, hia]
      rw [hdecomp]
      have hdisj :
          ∀ i : Fin k, realRestrict x s i = 0 ∨
            (if i = a then x a else 0) = 0 := by
        intro i
        by_cases hia : i = a
        · subst i
          left
          simp [realRestrict, ha]
        · right
          simp [hia]
      rw [A.disjoint_add (realRestrict x s)
        (fun i => if i = a then x a else 0) hdisj]
      rw [ih]
      rw [A.coord_hom a (x a)]
      rw [Finset.sum_insert ha]
      exact add_comm _ _
  have hfull : realRestrict x Finset.univ = x := by
    funext i
    simp [realRestrict]
  simpa [hfull] using hrestrict Finset.univ

/-- **Theorem 1 real scalar finite-coordinate core.** On a nonempty finite
    coordinate set, coordinate symmetry collapses the weighted real
    decomposition to a scalar multiple of the finite ℓ¹ sum. -/
theorem coord_real_l1_scalar_sum_succ (n : Nat)
    (A : CoordRealL1Axioms (Nat.succ n))
    (x : Fin (Nat.succ n) → ℝ) :
    A.ν x =
      A.ν (realBasis ⟨0, Nat.succ_pos n⟩) *
        (∑ i : Fin (Nat.succ n), |x i|) := by
  rw [coord_real_l1_weighted_sum A x]
  have hweights :
      ∀ i : Fin (Nat.succ n),
        A.ν (realBasis i) = A.ν (realBasis ⟨0, Nat.succ_pos n⟩) := by
    intro i
    exact A.basis_equal i ⟨0, Nat.succ_pos n⟩
  simp_rw [hweights]
  rw [show
      (∑ i : Fin (Nat.succ n), |x i| *
        A.ν (realBasis ⟨0, Nat.succ_pos n⟩)) =
        ∑ i : Fin (Nat.succ n),
          A.ν (realBasis ⟨0, Nat.succ_pos n⟩) * |x i| by
    apply Finset.sum_congr rfl
    intro i _hi
    exact mul_comm (|x i|) (A.ν (realBasis ⟨0, Nat.succ_pos n⟩))]
  rw [← Finset.mul_sum]

/-- **Theorem 1 nonnegative-scalar witness.** On a nonempty finite coordinate
    set, the real finite-coordinate core yields a nonnegative scalar `w` such
    that the gauge is `w` times the coordinatewise ℓ¹ sum. -/
theorem coord_real_l1_exists_scalar_succ (n : Nat)
    (A : CoordRealL1Axioms (Nat.succ n)) :
    ∃ w : ℝ, 0 ≤ w ∧
      ∀ x : Fin (Nat.succ n) → ℝ,
        A.ν x = w * (∑ i : Fin (Nat.succ n), |x i|) := by
  refine ⟨A.ν (realBasis ⟨0, Nat.succ_pos n⟩), ?_, ?_⟩
  · exact A.nonneg (realBasis ⟨0, Nat.succ_pos n⟩)
  · intro x
    exact coord_real_l1_scalar_sum_succ n A x

/-- Norm-strengthened real finite-coordinate hypotheses for the strict
    positivity refinement in Theorem 1. -/
structure CoordRealNormL1Axioms (k : Nat) extends CoordRealL1Axioms k where
  /-- A norm is strictly positive on nonzero vectors. -/
  positive_of_nonzero : ∀ x : Fin k → ℝ, x ≠ (fun _ => 0) → 0 < ν x

/-- **Theorem 1 norm-strengthened scalar witness.** If the real finite core is
    a norm, then the scalar witness is strictly positive. -/
theorem coord_real_l1_norm_scalar_positive_succ (n : Nat)
    (A : CoordRealNormL1Axioms (Nat.succ n)) :
    ∃ w : ℝ, 0 < w ∧
      ∀ x : Fin (Nat.succ n) → ℝ,
        A.ν x = w * (∑ i : Fin (Nat.succ n), |x i|) := by
  refine ⟨A.ν (realBasis ⟨0, Nat.succ_pos n⟩), ?_, ?_⟩
  · exact A.positive_of_nonzero (realBasis ⟨0, Nat.succ_pos n⟩) (by
      intro h
      have h0 := congrFun h ⟨0, Nat.succ_pos n⟩
      simp [realBasis] at h0)
  · intro x
    exact coord_real_l1_scalar_sum_succ n A.toCoordRealL1Axioms x

/-- Finite coordinate ℓ¹ norm used by the Paper 004 edge-aggregation theorems. -/
def edgeL1 {k : Nat} (x : Fin k → ℝ) : ℝ :=
  ∑ i : Fin k, |x i|

/-- Edge-weighted finite global ℓ¹ total. -/
def edgeWeightedL1Total {E : Type} [Fintype E] {k : Nat}
    (edgeWeight : E → ℝ) (δ : E → Fin k → ℝ) : ℝ :=
  ∑ e : E, edgeWeight e * edgeL1 (δ e)

/-- Orbit-weighted finite global ℓ¹ total, represented by a declared orbit
    classifier `orbit : E → O` and one scalar weight for each orbit label. -/
def orbitWeightedL1Total {E O : Type} [Fintype E] {k : Nat}
    (orbit : E → O) (orbitWeight : O → ℝ) (δ : E → Fin k → ℝ) : ℝ :=
  ∑ e : E, orbitWeight (orbit e) * edgeL1 (δ e)

/-- A cochain supported on a single edge. -/
def singleEdgeCochain {E : Type} [DecidableEq E] {k : Nat}
    (e : E) (u : Fin k → ℝ) : E → Fin k → ℝ :=
  fun f => if f = e then u else fun _ => 0

/-- The weighted total of a single-edge cochain is the edge weight times the
    coordinate ℓ¹ norm of the edge payload. -/
theorem single_edge_weighted_l1_total {E : Type} [Fintype E] [DecidableEq E]
    {k : Nat} (edgeWeight : E → ℝ) (e : E) (u : Fin k → ℝ) :
    edgeWeightedL1Total edgeWeight (singleEdgeCochain e u) =
      edgeWeight e * edgeL1 u := by
  unfold edgeWeightedL1Total singleEdgeCochain
  rw [Finset.sum_eq_single e]
  · simp [edgeL1]
  · intro b _hb hbe
    simp [hbe, edgeL1]
  · intro hnot
    exact False.elim (hnot (Finset.mem_univ e))

/-- **Theorem 2 edge-weight equality core.** If two single-edge probes are
    identified by the declared graph action and the fiber transport preserves
    the coordinate ℓ¹ norm, then the corresponding edge weights are equal. -/
theorem orbit_weight_eq_of_isometric_single_edge_invariance
    {E : Type} [Fintype E] [DecidableEq E] {k : Nat}
    (edgeWeight : E → ℝ) (e e' : E) (u v : Fin k → ℝ)
    (hiso : edgeL1 v = edgeL1 u)
    (hu : edgeL1 u ≠ 0)
    (hinv :
      edgeWeightedL1Total edgeWeight (singleEdgeCochain e u) =
        edgeWeightedL1Total edgeWeight (singleEdgeCochain e' v)) :
    edgeWeight e = edgeWeight e' := by
  rw [single_edge_weighted_l1_total edgeWeight e u,
    single_edge_weighted_l1_total edgeWeight e' v] at hinv
  rw [hiso] at hinv
  exact mul_right_cancel₀ hu hinv

/-- **Theorem 2 orbit aggregation core.** If edge weights factor through the
    declared orbit classifier, the global weighted ℓ¹ total is the
    orbit-weighted aggregation. -/
theorem orbit_weighted_l1_aggregation {E O : Type} [Fintype E] {k : Nat}
    (edgeWeight : E → ℝ) (orbit : E → O) (orbitWeight : O → ℝ)
    (δ : E → Fin k → ℝ)
    (hfactor : ∀ e : E, edgeWeight e = orbitWeight (orbit e)) :
    edgeWeightedL1Total edgeWeight δ =
      orbitWeightedL1Total orbit orbitWeight δ := by
  unfold edgeWeightedL1Total orbitWeightedL1Total
  apply Finset.sum_congr rfl
  intro e _he
  rw [hfactor e]

/-- **Theorem 3 orbit-uniform bridge.** If the declared orbit weights are all
    one scalar `α`, the orbit-weighted aggregation collapses to `α` times the
    unweighted finite ℓ¹ total over all edges. -/
theorem orbit_uniform_l1_collapse {E O : Type} [Fintype E] {k : Nat}
    (orbit : E → O) (orbitWeight : O → ℝ) (α : ℝ)
    (δ : E → Fin k → ℝ)
    (huniform : ∀ e : E, orbitWeight (orbit e) = α) :
    orbitWeightedL1Total orbit orbitWeight δ =
      α * (∑ e : E, edgeL1 (δ e)) := by
  unfold orbitWeightedL1Total
  simp_rw [huniform]
  rw [← Finset.mul_sum]

/-- **Theorem 3 edge-uniform bridge.** If the edge weights themselves are all
    one scalar `α`, the edge-weighted aggregation collapses to `α` times the
    unweighted finite ℓ¹ total over all edges. -/
theorem edge_uniform_l1_collapse {E : Type} [Fintype E] {k : Nat}
    (edgeWeight : E → ℝ) (α : ℝ) (δ : E → Fin k → ℝ)
    (huniform : ∀ e : E, edgeWeight e = α) :
    edgeWeightedL1Total edgeWeight δ =
      α * (∑ e : E, edgeL1 (δ e)) := by
  unfold edgeWeightedL1Total
  simp_rw [huniform]
  rw [← Finset.mul_sum]

/-!
## Section 2: Counterexamples and Arithmetic Cores
-/

/-- **Counterexample 1 arithmetic core.** A quadratic, ℓ²-style gauge is not
    a scalar multiple of the coordinatewise ℓ¹ gauge. -/
theorem ce1_quadratic_not_l1_scalar :
    ¬ (∃ w : Nat, ∀ x y : Nat, x ^ 2 + y ^ 2 = w * (x + y)) := by
  intro h
  rcases h with ⟨w, hw⟩
  have h10 := hw 1 0
  have h20 := hw 2 0
  omega

/-- **Counterexample 2 arithmetic core.** Removing coordinate symmetry permits
    weighted coordinate ℓ¹ gauges. -/
theorem ce2_weighted_l1_not_uniform :
    ¬ (∃ w : Nat, ∀ x y : Nat, x + 2 * y = w * (x + y)) := by
  intro h
  rcases h with ⟨w, hw⟩
  have h10 := hw 1 0
  have h01 := hw 0 1
  omega

/-- **Counterexample 3 arithmetic core.** Removing edge locality permits
    cross-edge coupling. -/
theorem ce3_cross_edge_coupling_not_edge_local :
    ¬ (∃ f g : Nat → Nat, ∀ a b : Nat, a + b + a * b = f a + g b) := by
  intro h
  rcases h with ⟨f, g, hfg⟩
  have h00 := hfg 0 0
  have h10 := hfg 1 0
  have h01 := hfg 0 1
  have h11 := hfg 1 1
  omega

/-- **Counterexample 4 arithmetic core.** Orbit-weighted ℓ¹ need not reduce
    to unweighted global ℓ¹ without edge-uniformity. -/
theorem ce4_orbit_weighted_not_unweighted :
    ¬ (∃ w : Nat, ∀ x y : Nat, x + 2 * y = w * (x + y)) := by
  exact ce2_weighted_l1_not_uniform

/-- **Theorem 3 two-edge arithmetic core.** Uniform weights collapse a two-edge
    weighted ℓ¹ expression to one scalar times the unweighted expression. -/
theorem edge_uniformity_collapses_two_edge_l1 (w x y : Nat) :
    w * x + w * y = w * (x + y) := by
  exact (Nat.mul_add w x y).symm

/-- **Theorem 3 finite arithmetic core.** On any finite edge type, if all edge
    weights are equal to `w`, then the weighted finite ℓ¹ sum collapses to
    `w` times the unweighted finite ℓ¹ sum. -/
theorem edge_uniformity_collapses_finite_l1 {E : Type} [Fintype E]
    (weight x : E → Nat) (w : Nat) (hw : ∀ e, weight e = w) :
    (∑ e : E, weight e * x e) = w * (∑ e : E, x e) := by
  simp_rw [hw]
  rw [← Finset.mul_sum]

/-- **Counterexample 5.** For p=2, the gauge Φ(x)=Σ|xᵢ|² is not absolutely
    homogeneous. Concrete witness: `(2*1)^2 ≠ 2*1^2`. -/
theorem ce5_lp_not_homogeneous :
    ¬ (∀ c x : Nat, (c * x) ^ 2 = c * x ^ 2) := by
  intro h
  have := h 2 1
  simp at this

/-!
## Section 3: LGGR / EPK Corollaries
-/

/-- A cochain diagnostic record with a fixed number of edges. -/
structure CochainDiag (n : Nat) where
  /-- Per-edge ℓ¹ diagnostic value. -/
  diag : Fin n → Nat
  /-- Per-edge weight from the local coordinatewise theorem. -/
  weight : Fin n → Nat

/-- Two cochains are zero-related when their per-edge diagnostics agree. -/
def cochainPD (n : Nat) : ObstructionCore.PrimitiveDifference (CochainDiag n) Prop where
  δ := fun c1 c2 => c1.diag = c2.diag
  Zero := fun p => p
  zero_refl := by
    intro x
    rfl
  zero_symm := by
    intro x y hxy
    exact hxy.symm
  zero_trans := by
    intro x y z hxy hyz
    exact hxy.trans hyz

/-- The per-edge diagnostic function. -/
def diagMap (n : Nat) : CochainDiag n → (Fin n → Nat) :=
  fun c => c.diag

/-- The per-edge weight function. -/
def weightMap (n : Nat) : CochainDiag n → (Fin n → Nat) :=
  fun c => c.weight

/-- The finite weighted/global total determined by diagnostics and weights. -/
def weightedTotalMap (n : Nat) : CochainDiag n → Nat :=
  fun c => ∑ e : Fin n, c.weight e * c.diag e

/-- The finite unweighted diagnostic total. -/
def unweightedTotalMap (n : Nat) : CochainDiag n → Nat :=
  fun c => ∑ e : Fin n, c.diag e

/-- The intermediate primitive-difference relation that declares diagnostics and
    the weighted scalar total, but not the full weight profile. -/
def cochainTotalPD (n : Nat) :
    ObstructionCore.PrimitiveDifference (CochainDiag n) Prop where
  δ := fun c1 c2 =>
    c1.diag = c2.diag ∧ weightedTotalMap n c1 = weightedTotalMap n c2
  Zero := fun p => p
  zero_refl := by
    intro x
    exact ⟨rfl, rfl⟩
  zero_symm := by
    intro x y hxy
    exact ⟨hxy.1.symm, hxy.2.symm⟩
  zero_trans := by
    intro x y z hxy hyz
    exact ⟨hxy.1.trans hyz.1, hxy.2.trans hyz.2⟩

/-- The finer primitive-difference relation that declares both diagnostics and
    weights as kernel data. -/
def cochainWeightedPD (n : Nat) :
    ObstructionCore.PrimitiveDifference (CochainDiag n) Prop where
  δ := fun c1 c2 => c1.diag = c2.diag ∧ c1.weight = c2.weight
  Zero := fun p => p
  zero_refl := by
    intro x
    exact ⟨rfl, rfl⟩
  zero_symm := by
    intro x y hxy
    exact ⟨hxy.1.symm, hxy.2.symm⟩
  zero_trans := by
    intro x y z hxy hyz
    exact ⟨hxy.1.trans hyz.1, hxy.2.trans hyz.2⟩

/-- The per-edge diagnostic is invariant on zero-related cochains. -/
theorem diag_invariant (n : Nat) :
    (cochainPD n).InvariantCongruent (diagMap n) := by
  intro x y hxy
  exact hxy

/-- **Witness.** Two 1-edge cochains with the same diagnostic but different
    weights. -/
theorem weight_witness :
    ∃ x y : CochainDiag 1,
      (cochainPD 1).ZeroRel x y ∧
      weightMap 1 x ≠ weightMap 1 y := by
  refine ⟨⟨fun _ => 5, fun _ => 1⟩, ⟨fun _ => 5, fun _ => 2⟩, ?_, ?_⟩
  · rfl
  · simp [weightMap]
    intro h
    have := congrFun h ⟨0, by omega⟩
    omega

/-- **Parametric witness.** On every nonempty edge set, the local diagnostic
    quotient can identify records whose weight profiles differ. -/
theorem weight_witness_succ (n : Nat) :
    ∃ x y : CochainDiag (Nat.succ n),
      (cochainPD (Nat.succ n)).ZeroRel x y ∧
      weightMap (Nat.succ n) x ≠ weightMap (Nat.succ n) y := by
  refine ⟨⟨fun _ => 5, fun _ => 1⟩, ⟨fun _ => 5, fun _ => 2⟩, ?_, ?_⟩
  · rfl
  · simp [weightMap]
    intro h
    have := congrFun h ⟨0, Nat.succ_pos n⟩
    omega

/-- Weight profiles are not invariant under the local diagnostic quotient on
    any nonempty edge set. -/
theorem weight_not_invariant_succ (n : Nat) :
    ¬ (cochainPD (Nat.succ n)).InvariantCongruent
      (weightMap (Nat.succ n)) := by
  obtain ⟨x, y, hrel, hne⟩ := weight_witness_succ n
  exact ObstructionCore.PrimitiveDifference.not_invariantCongruent_of_zeroRel_ne
    (cochainPD (Nat.succ n))
    (weightMap (Nat.succ n))
    hrel
    hne

/-- **Weighted-total witness.** On every nonempty edge set, two locally
    zero-related records can have different weighted global totals. -/
theorem weighted_total_witness_succ (n : Nat) :
    ∃ x y : CochainDiag (Nat.succ n),
      (cochainPD (Nat.succ n)).ZeroRel x y ∧
      weightedTotalMap (Nat.succ n) x ≠ weightedTotalMap (Nat.succ n) y := by
  refine ⟨⟨fun _ => 5, fun _ => 1⟩, ⟨fun _ => 5, fun _ => 2⟩, ?_, ?_⟩
  · rfl
  · simp [weightedTotalMap]

/-- The weighted global total is not invariant under the local diagnostic
    quotient on any nonempty edge set. -/
theorem weighted_total_not_invariant_succ (n : Nat) :
    ¬ (cochainPD (Nat.succ n)).InvariantCongruent
      (weightedTotalMap (Nat.succ n)) := by
  obtain ⟨x, y, hrel, hne⟩ := weighted_total_witness_succ n
  exact ObstructionCore.PrimitiveDifference.not_invariantCongruent_of_zeroRel_ne
    (cochainPD (Nat.succ n))
    (weightedTotalMap (Nat.succ n))
    hrel
    hne

/-- The unweighted diagnostic total is invariant under the local diagnostic
    quotient. -/
theorem unweighted_total_invariant (n : Nat) :
    (cochainPD n).InvariantCongruent (unweightedTotalMap n) := by
  intro x y hxy
  unfold unweightedTotalMap
  rw [hxy]

/-- The unweighted diagnostic total factors through the local diagnostic
    quotient. -/
theorem unweighted_total_factors_through_local_kernel (n : Nat) :
    ∃ F : (cochainPD n).ResidualQuotient → Nat,
      ∀ c : CochainDiag n,
        F ((cochainPD n).classOf c) = unweightedTotalMap n c := by
  exact
    (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      (cochainPD n)
      (unweightedTotalMap n)).mpr
      (unweighted_total_invariant n)

/-- **Scalar aggregate LGGR.** On every nonempty edge set, the unweighted
    diagnostic total factors through the local quotient, but the paired
    unweighted/weighted scalar totals do not. -/
theorem scalar_total_lggr_obstruction_succ (n : Nat) :
    (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient → Nat,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          unweightedTotalMap (Nat.succ n) c) ∧
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient → Nat × Nat,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          (unweightedTotalMap (Nat.succ n) c,
            weightedTotalMap (Nat.succ n) c)) := by
  constructor
  · exact unweighted_total_factors_through_local_kernel (Nat.succ n)
  · exact ObstructionCore.PrimitiveDifference.invariantPair_no_factor_of_right_not_invariant
      (cochainPD (Nat.succ n))
      (unweightedTotalMap (Nat.succ n))
      (weightedTotalMap (Nat.succ n))
      (weighted_total_not_invariant_succ n)

/-- Uniformly weighted aggregate induced by a declared scalar weight. -/
def uniformWeightedTotalMap (n w : Nat) : CochainDiag n → Nat :=
  fun c => w * unweightedTotalMap n c

/-- Declared uniform scalar weights are invariant under the coarse local
    diagnostic kernel. -/
theorem uniform_weighted_total_invariant (n w : Nat) :
    (cochainPD n).InvariantCongruent (uniformWeightedTotalMap n w) := by
  intro x y hxy
  unfold uniformWeightedTotalMap
  rw [unweighted_total_invariant n x y hxy]

/-- A declared uniform scalar weighted aggregate factors through the coarse
    local diagnostic quotient. -/
theorem uniform_weighted_total_factors_through_local_kernel (n w : Nat) :
    ∃ F : (cochainPD n).ResidualQuotient → Nat,
      ∀ c : CochainDiag n,
        F ((cochainPD n).classOf c) = uniformWeightedTotalMap n w c := by
  exact
    (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      (cochainPD n)
      (uniformWeightedTotalMap n w)).mpr
      (uniform_weighted_total_invariant n w)

/-- The paired unweighted total and declared-uniform weighted total factor
    through the coarse local diagnostic quotient. -/
theorem uniform_scalar_pair_factors_through_local_kernel (n w : Nat) :
    ∃ F : (cochainPD n).ResidualQuotient → Nat × Nat,
      ∀ c : CochainDiag n,
        F ((cochainPD n).classOf c) =
          (unweightedTotalMap n c, uniformWeightedTotalMap n w c) := by
  exact
    (ObstructionCore.PrimitiveDifference.invariantFactor_pair_exists_iff
      (cochainPD n)
      (unweightedTotalMap n)
      (uniformWeightedTotalMap n w)).mpr
      ⟨unweighted_total_invariant n, uniform_weighted_total_invariant n w⟩

/-- If all weights in a cochain record are the same scalar `w`, then its
    weighted total is `w` times its unweighted diagnostic total. -/
theorem weighted_total_eq_scalar_unweighted_total_of_uniform_weights
    (n w : Nat) (c : CochainDiag n) (hw : ∀ e : Fin n, c.weight e = w) :
    weightedTotalMap n c = w * unweightedTotalMap n c := by
  simp [weightedTotalMap, unweightedTotalMap]
  simp_rw [hw]
  rw [← Finset.mul_sum]

/-- **LGGR Corollary for Paper 004.** The per-edge diagnostic descends through
    the quotient, but the paired diagnostic-plus-weight map does not. -/
theorem lggr_edgewise_uniformity_obstruction :
    (∃ F : (cochainPD 1).ResidualQuotient → (Fin 1 → Nat),
      ∀ c : CochainDiag 1,
        F ((cochainPD 1).classOf c) = diagMap 1 c) ∧
    ¬ (∃ F : (cochainPD 1).ResidualQuotient → (Fin 1 → Nat) × (Fin 1 → Nat),
      ∀ c : CochainDiag 1,
        F ((cochainPD 1).classOf c) = (diagMap 1 c, weightMap 1 c)) := by
  obtain ⟨x, y, hrel, hne⟩ := weight_witness
  exact ObstructionCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction_of_witness
    (cochainPD 1)
    (diagMap 1)
    (weightMap 1)
    (diag_invariant 1)
    hrel
    hne

/-- **Parametric LGGR Corollary for Paper 004.** The obstruction holds on
    every nonempty finite edge set. -/
theorem lggr_edgewise_uniformity_obstruction_succ (n : Nat) :
    (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient →
        (Fin (Nat.succ n) → Nat),
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          diagMap (Nat.succ n) c) ∧
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient →
        (Fin (Nat.succ n) → Nat) × (Fin (Nat.succ n) → Nat),
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          (diagMap (Nat.succ n) c, weightMap (Nat.succ n) c)) := by
  obtain ⟨x, y, hrel, hne⟩ := weight_witness_succ n
  exact ObstructionCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction_of_witness
    (cochainPD (Nat.succ n))
    (diagMap (Nat.succ n))
    (weightMap (Nat.succ n))
    (diag_invariant (Nat.succ n))
    hrel
    hne

/-- **EPK instance.** The local diagnostic kernel does not determine the
    weight profile on any nonempty edge set. -/
theorem epk_local_kernel_does_not_determine_weight_profile (n : Nat) :
    ¬ (∀ x y : CochainDiag (Nat.succ n),
      (cochainPD (Nat.succ n)).ZeroRel x y →
        weightMap (Nat.succ n) x = weightMap (Nat.succ n) y) := by
  exact weight_not_invariant_succ n

/-- **EPK weighted-total instance.** The local diagnostic quotient does not
    determine the weighted global total on any nonempty edge set. -/
theorem epk_local_kernel_does_not_determine_weighted_total (n : Nat) :
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient → Nat,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          weightedTotalMap (Nat.succ n) c) := by
  exact ObstructionCore.PrimitiveDifference.invariantFactor_no_factor_of_not_invariant
    (cochainPD (Nat.succ n))
    (weightedTotalMap (Nat.succ n))
    (weighted_total_not_invariant_succ n)

/-- **EPK joint obstruction.** On every nonempty edge set, the coarse local
    diagnostic kernel cannot factor the joint diagnostic-plus-weighted-total
    payload. -/
theorem diagnostic_and_weighted_total_do_not_factor_through_local_kernel_succ
    (n : Nat) :
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient →
        (Fin (Nat.succ n) → Nat) × Nat,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          (diagMap (Nat.succ n) c, weightedTotalMap (Nat.succ n) c)) := by
  exact ObstructionCore.PrimitiveDifference.invariantPair_no_factor_of_right_not_invariant
    (cochainPD (Nat.succ n))
    (diagMap (Nat.succ n))
    (weightedTotalMap (Nat.succ n))
    (weighted_total_not_invariant_succ n)

/-- The diagnostic+total kernel is finer than the local diagnostic kernel. -/
theorem total_kernel_refines_local_kernel (n : Nat) :
    ∀ x y : CochainDiag n,
      (cochainTotalPD n).ZeroRel x y → (cochainPD n).ZeroRel x y := by
  intro x y hxy
  exact hxy.1

/-- Under the diagnostic+total kernel, the weighted scalar total is invariant
    because it is declared kernel data. -/
theorem weighted_total_invariant_with_total_kernel (n : Nat) :
    (cochainTotalPD n).InvariantCongruent (weightedTotalMap n) := by
  intro x y hxy
  exact hxy.2

/-- Under the diagnostic+total kernel, the diagnostic profile remains
    invariant. -/
theorem diag_invariant_with_total_kernel (n : Nat) :
    (cochainTotalPD n).InvariantCongruent (diagMap n) := by
  intro x y hxy
  exact hxy.1

/-- The weighted global total factors through the quotient once the kernel
    declares the weighted total itself. -/
theorem epk_weighted_total_factors_when_kernel_declares_total (n : Nat) :
    ∃ F : (cochainTotalPD n).ResidualQuotient → Nat,
      ∀ c : CochainDiag n,
        F ((cochainTotalPD n).classOf c) = weightedTotalMap n c := by
  exact
    (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      (cochainTotalPD n)
      (weightedTotalMap n)).mpr
      (weighted_total_invariant_with_total_kernel n)

/-- Once the kernel declares diagnostics and weighted total, the combined
    diagnostic-plus-weighted-total payload factors through that quotient. -/
theorem diagnostic_and_weighted_total_factor_when_kernel_declares_total
    (n : Nat) :
    ∃ F : (cochainTotalPD n).ResidualQuotient → (Fin n → Nat) × Nat,
      ∀ c : CochainDiag n,
        F ((cochainTotalPD n).classOf c) =
          (diagMap n c, weightedTotalMap n c) := by
  exact
    (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      (cochainTotalPD n)
      (fun c : CochainDiag n => (diagMap n c, weightedTotalMap n c))).mpr
      (by
        intro x y hxy
        exact Prod.ext hxy.1 hxy.2)

/-- The diagnostic+total quotient projects to the local diagnostic quotient. -/
theorem total_quotient_projects_to_local_quotient (n : Nat) :
    ∃ F : (cochainTotalPD n).ResidualQuotient → (cochainPD n).ResidualQuotient,
      ∀ c : CochainDiag n,
        F ((cochainTotalPD n).classOf c) = (cochainPD n).classOf c := by
  refine ⟨Quotient.lift (fun c : CochainDiag n => (cochainPD n).classOf c) ?_, ?_⟩
  · intro x y hxy
    exact ObstructionCore.PrimitiveDifference.classOf_eq_of_zero
      (cochainPD n) (total_kernel_refines_local_kernel n x y hxy)
  · intro c
    rfl

/-- On a nonempty edge set, the local quotient cannot reconstruct the
    diagnostic+total quotient. -/
theorem local_quotient_does_not_lift_to_total_quotient_succ (n : Nat) :
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient →
        (cochainTotalPD (Nat.succ n)).ResidualQuotient,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          (cochainTotalPD (Nat.succ n)).classOf c) := by
  intro h
  rcases h with ⟨F, hF⟩
  obtain ⟨x, y, hrel, hne⟩ := weighted_total_witness_succ n
  have hclass : (cochainPD (Nat.succ n)).classOf x =
      (cochainPD (Nat.succ n)).classOf y :=
    ObstructionCore.PrimitiveDifference.classOf_eq_of_zero
      (cochainPD (Nat.succ n)) hrel
  have htotal : (cochainTotalPD (Nat.succ n)).classOf x =
      (cochainTotalPD (Nat.succ n)).classOf y := by
    calc
      (cochainTotalPD (Nat.succ n)).classOf x =
          F ((cochainPD (Nat.succ n)).classOf x) := (hF x).symm
      _ = F ((cochainPD (Nat.succ n)).classOf y) := by rw [hclass]
      _ = (cochainTotalPD (Nat.succ n)).classOf y := hF y
  have hzero : (cochainTotalPD (Nat.succ n)).ZeroRel x y :=
    Quotient.exact htotal
  exact hne hzero.2

/-- **EPK repair theorem.** If the declared kernel includes both diagnostics
    and weights, then the weighted global total is invariant under that kernel. -/
theorem weighted_total_invariant_with_weight_kernel (n : Nat) :
    (cochainWeightedPD n).InvariantCongruent (weightedTotalMap n) := by
  intro x y hxy
  rcases hxy with ⟨hdiag, hweight⟩
  simp [weightedTotalMap, hdiag, hweight]

/-- **EPK positive factorization.** The weighted global total factors through
    the quotient once the kernel declares weights along with diagnostics. -/
theorem epk_weighted_total_factors_when_kernel_declares_weights (n : Nat) :
    ∃ F : (cochainWeightedPD n).ResidualQuotient → Nat,
      ∀ c : CochainDiag n,
        F ((cochainWeightedPD n).classOf c) = weightedTotalMap n c := by
  exact
    (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      (cochainWeightedPD n)
      (weightedTotalMap n)).mpr
      (weighted_total_invariant_with_weight_kernel n)

/-- Under the refined kernel, the local diagnostic profile remains invariant. -/
theorem diag_invariant_with_weight_kernel (n : Nat) :
    (cochainWeightedPD n).InvariantCongruent (diagMap n) := by
  intro x y hxy
  exact hxy.1

/-- Under the refined kernel, the weight profile is invariant because it is
    declared as part of the kernel. -/
theorem weight_invariant_with_weight_kernel (n : Nat) :
    (cochainWeightedPD n).InvariantCongruent (weightMap n) := by
  intro x y hxy
  exact hxy.2

/-- **EPK joint repair theorem.** Once the kernel declares both diagnostics and
    weights, the combined local diagnostic plus weighted-total payload factors
    through the refined quotient. -/
theorem diagnostic_and_weighted_total_factor_when_kernel_declares_weights
    (n : Nat) :
    ∃ F : (cochainWeightedPD n).ResidualQuotient → (Fin n → Nat) × Nat,
      ∀ c : CochainDiag n,
        F ((cochainWeightedPD n).classOf c) =
          (diagMap n c, weightedTotalMap n c) := by
  exact
    (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      (cochainWeightedPD n)
      (fun c : CochainDiag n => (diagMap n c, weightedTotalMap n c))).mpr
      (by
        intro x y hxy
        exact Prod.ext hxy.1
          (weighted_total_invariant_with_weight_kernel n x y hxy))

/-- The refined diagnostic+weight kernel is finer than the local diagnostic
    kernel. -/
theorem weighted_kernel_refines_local_kernel (n : Nat) :
    ∀ x y : CochainDiag n,
      (cochainWeightedPD n).ZeroRel x y → (cochainPD n).ZeroRel x y := by
  intro x y hxy
  exact hxy.1

/-- The full diagnostic+weight kernel is finer than the diagnostic+total
    kernel. -/
theorem weighted_kernel_refines_total_kernel (n : Nat) :
    ∀ x y : CochainDiag n,
      (cochainWeightedPD n).ZeroRel x y → (cochainTotalPD n).ZeroRel x y := by
  intro x y hxy
  exact ⟨hxy.1, by simp [weightedTotalMap, hxy.1, hxy.2]⟩

/-- The refined diagnostic+weight quotient canonically projects to the local
    diagnostic quotient. -/
theorem weighted_quotient_projects_to_local_quotient (n : Nat) :
    ∃ F : (cochainWeightedPD n).ResidualQuotient → (cochainPD n).ResidualQuotient,
      ∀ c : CochainDiag n,
        F ((cochainWeightedPD n).classOf c) = (cochainPD n).classOf c := by
  refine ⟨Quotient.lift (fun c : CochainDiag n => (cochainPD n).classOf c) ?_, ?_⟩
  · intro x y hxy
    exact ObstructionCore.PrimitiveDifference.classOf_eq_of_zero
      (cochainPD n) (weighted_kernel_refines_local_kernel n x y hxy)
  · intro c
    rfl

/-- The refined diagnostic+weight quotient canonically projects to the
    diagnostic+total quotient. -/
theorem weighted_quotient_projects_to_total_quotient (n : Nat) :
    ∃ F : (cochainWeightedPD n).ResidualQuotient → (cochainTotalPD n).ResidualQuotient,
      ∀ c : CochainDiag n,
        F ((cochainWeightedPD n).classOf c) = (cochainTotalPD n).classOf c := by
  refine ⟨Quotient.lift (fun c : CochainDiag n => (cochainTotalPD n).classOf c) ?_, ?_⟩
  · intro x y hxy
    exact ObstructionCore.PrimitiveDifference.classOf_eq_of_zero
      (cochainTotalPD n) (weighted_kernel_refines_total_kernel n x y hxy)
  · intro c
    rfl

/-- **EPK quotient non-lift.** On a nonempty edge set, the local diagnostic
    quotient cannot reconstruct the refined diagnostic+weight quotient. -/
theorem local_quotient_does_not_lift_to_weighted_quotient_succ (n : Nat) :
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient →
        (cochainWeightedPD (Nat.succ n)).ResidualQuotient,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          (cochainWeightedPD (Nat.succ n)).classOf c) := by
  intro h
  rcases h with ⟨F, hF⟩
  obtain ⟨x, y, hrel, hne⟩ := weight_witness_succ n
  have hclass : (cochainPD (Nat.succ n)).classOf x =
      (cochainPD (Nat.succ n)).classOf y :=
    ObstructionCore.PrimitiveDifference.classOf_eq_of_zero
      (cochainPD (Nat.succ n)) hrel
  have hrefined : (cochainWeightedPD (Nat.succ n)).classOf x =
      (cochainWeightedPD (Nat.succ n)).classOf y := by
    calc
      (cochainWeightedPD (Nat.succ n)).classOf x =
          F ((cochainPD (Nat.succ n)).classOf x) := (hF x).symm
      _ = F ((cochainPD (Nat.succ n)).classOf y) := by rw [hclass]
      _ = (cochainWeightedPD (Nat.succ n)).classOf y := hF y
  have hzero : (cochainWeightedPD (Nat.succ n)).ZeroRel x y :=
    Quotient.exact hrefined
  exact hne hzero.2

/-- First two-edge record witnessing that diagnostic+total data need not
    determine the full weight profile. -/
def totalWeightSwapX : CochainDiag 2 where
  diag := fun _ => 1
  weight := fun e => if e = (0 : Fin 2) then 1 else 2

/-- Second two-edge record witnessing that diagnostic+total data need not
    determine the full weight profile. -/
def totalWeightSwapY : CochainDiag 2 where
  diag := fun _ => 1
  weight := fun e => if e = (0 : Fin 2) then 2 else 1

/-- **EPK quotient middle-layer non-lift.** The diagnostic+total quotient cannot
    reconstruct the full diagnostic+weight quotient, even on two edges. -/
theorem total_quotient_does_not_lift_to_weighted_quotient_two_edges :
    ¬ (∃ F : (cochainTotalPD 2).ResidualQuotient →
        (cochainWeightedPD 2).ResidualQuotient,
      ∀ c : CochainDiag 2,
        F ((cochainTotalPD 2).classOf c) =
          (cochainWeightedPD 2).classOf c) := by
  intro h
  rcases h with ⟨F, hF⟩
  have htotal : (cochainTotalPD 2).ZeroRel totalWeightSwapX totalWeightSwapY := by
    constructor
    · funext e
      rfl
    · decide
  have hclass : (cochainTotalPD 2).classOf totalWeightSwapX =
      (cochainTotalPD 2).classOf totalWeightSwapY :=
    ObstructionCore.PrimitiveDifference.classOf_eq_of_zero
      (cochainTotalPD 2) htotal
  have hrefined : (cochainWeightedPD 2).classOf totalWeightSwapX =
      (cochainWeightedPD 2).classOf totalWeightSwapY := by
    calc
      (cochainWeightedPD 2).classOf totalWeightSwapX =
          F ((cochainTotalPD 2).classOf totalWeightSwapX) :=
            (hF totalWeightSwapX).symm
      _ = F ((cochainTotalPD 2).classOf totalWeightSwapY) := by rw [hclass]
      _ = (cochainWeightedPD 2).classOf totalWeightSwapY := hF totalWeightSwapY
  have hzero : (cochainWeightedPD 2).ZeroRel totalWeightSwapX totalWeightSwapY :=
    Quotient.exact hrefined
  have hne : totalWeightSwapX.weight ≠ totalWeightSwapY.weight := by
    decide
  exact hne hzero.2

/-!
## Stable names for encyclopedia references
-/

namespace LGGR

theorem diag_invariant (n : Nat) :
    (cochainPD n).InvariantCongruent (diagMap n) :=
  PaperGS003.diag_invariant n

theorem weight_witness :
    ∃ x y : CochainDiag 1,
      (cochainPD 1).ZeroRel x y ∧
      weightMap 1 x ≠ weightMap 1 y :=
  PaperGS003.weight_witness

theorem weight_witness_succ (n : Nat) :
    ∃ x y : CochainDiag (Nat.succ n),
      (cochainPD (Nat.succ n)).ZeroRel x y ∧
      weightMap (Nat.succ n) x ≠ weightMap (Nat.succ n) y :=
  PaperGS003.weight_witness_succ n

theorem weight_not_invariant_succ (n : Nat) :
    ¬ (cochainPD (Nat.succ n)).InvariantCongruent
      (weightMap (Nat.succ n)) :=
  PaperGS003.weight_not_invariant_succ n

theorem weighted_total_witness_succ (n : Nat) :
    ∃ x y : CochainDiag (Nat.succ n),
      (cochainPD (Nat.succ n)).ZeroRel x y ∧
      weightedTotalMap (Nat.succ n) x ≠ weightedTotalMap (Nat.succ n) y :=
  PaperGS003.weighted_total_witness_succ n

theorem weighted_total_not_invariant_succ (n : Nat) :
    ¬ (cochainPD (Nat.succ n)).InvariantCongruent
      (weightedTotalMap (Nat.succ n)) :=
  PaperGS003.weighted_total_not_invariant_succ n

theorem unweighted_total_invariant (n : Nat) :
    (cochainPD n).InvariantCongruent (unweightedTotalMap n) :=
  PaperGS003.unweighted_total_invariant n

theorem unweighted_total_factors_through_local_kernel (n : Nat) :
    ∃ F : (cochainPD n).ResidualQuotient → Nat,
      ∀ c : CochainDiag n,
        F ((cochainPD n).classOf c) = unweightedTotalMap n c :=
  PaperGS003.unweighted_total_factors_through_local_kernel n

theorem scalar_total_lggr_obstruction_succ (n : Nat) :
    (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient → Nat,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          unweightedTotalMap (Nat.succ n) c) ∧
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient → Nat × Nat,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          (unweightedTotalMap (Nat.succ n) c,
            weightedTotalMap (Nat.succ n) c)) :=
  PaperGS003.scalar_total_lggr_obstruction_succ n

theorem uniform_weighted_total_invariant (n w : Nat) :
    (cochainPD n).InvariantCongruent (uniformWeightedTotalMap n w) :=
  PaperGS003.uniform_weighted_total_invariant n w

theorem uniform_weighted_total_factors_through_local_kernel (n w : Nat) :
    ∃ F : (cochainPD n).ResidualQuotient → Nat,
      ∀ c : CochainDiag n,
        F ((cochainPD n).classOf c) = uniformWeightedTotalMap n w c :=
  PaperGS003.uniform_weighted_total_factors_through_local_kernel n w

theorem uniform_scalar_pair_factors_through_local_kernel (n w : Nat) :
    ∃ F : (cochainPD n).ResidualQuotient → Nat × Nat,
      ∀ c : CochainDiag n,
        F ((cochainPD n).classOf c) =
          (unweightedTotalMap n c, uniformWeightedTotalMap n w c) :=
  PaperGS003.uniform_scalar_pair_factors_through_local_kernel n w

theorem weighted_total_eq_scalar_unweighted_total_of_uniform_weights
    (n w : Nat) (c : CochainDiag n) (hw : ∀ e : Fin n, c.weight e = w) :
    weightedTotalMap n c = w * unweightedTotalMap n c :=
  PaperGS003.weighted_total_eq_scalar_unweighted_total_of_uniform_weights n w c hw

theorem lggr_edgewise_uniformity_obstruction :
    (∃ F : (cochainPD 1).ResidualQuotient → (Fin 1 → Nat),
      ∀ c : CochainDiag 1,
        F ((cochainPD 1).classOf c) = diagMap 1 c) ∧
    ¬ (∃ F : (cochainPD 1).ResidualQuotient → (Fin 1 → Nat) × (Fin 1 → Nat),
      ∀ c : CochainDiag 1,
        F ((cochainPD 1).classOf c) = (diagMap 1 c, weightMap 1 c)) :=
  PaperGS003.lggr_edgewise_uniformity_obstruction

theorem lggr_edgewise_uniformity_obstruction_succ (n : Nat) :
    (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient →
        (Fin (Nat.succ n) → Nat),
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          diagMap (Nat.succ n) c) ∧
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient →
        (Fin (Nat.succ n) → Nat) × (Fin (Nat.succ n) → Nat),
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          (diagMap (Nat.succ n) c, weightMap (Nat.succ n) c)) :=
  PaperGS003.lggr_edgewise_uniformity_obstruction_succ n

theorem epk_local_kernel_does_not_determine_weight_profile (n : Nat) :
    ¬ (∀ x y : CochainDiag (Nat.succ n),
      (cochainPD (Nat.succ n)).ZeroRel x y →
        weightMap (Nat.succ n) x = weightMap (Nat.succ n) y) :=
  PaperGS003.epk_local_kernel_does_not_determine_weight_profile n

theorem epk_local_kernel_does_not_determine_weighted_total (n : Nat) :
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient → Nat,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          weightedTotalMap (Nat.succ n) c) :=
  PaperGS003.epk_local_kernel_does_not_determine_weighted_total n

theorem diagnostic_and_weighted_total_do_not_factor_through_local_kernel_succ
    (n : Nat) :
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient →
        (Fin (Nat.succ n) → Nat) × Nat,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          (diagMap (Nat.succ n) c, weightedTotalMap (Nat.succ n) c)) :=
  PaperGS003.diagnostic_and_weighted_total_do_not_factor_through_local_kernel_succ n

theorem total_kernel_refines_local_kernel (n : Nat) :
    ∀ x y : CochainDiag n,
      (cochainTotalPD n).ZeroRel x y → (cochainPD n).ZeroRel x y :=
  PaperGS003.total_kernel_refines_local_kernel n

theorem weighted_total_invariant_with_total_kernel (n : Nat) :
    (cochainTotalPD n).InvariantCongruent (weightedTotalMap n) :=
  PaperGS003.weighted_total_invariant_with_total_kernel n

theorem diag_invariant_with_total_kernel (n : Nat) :
    (cochainTotalPD n).InvariantCongruent (diagMap n) :=
  PaperGS003.diag_invariant_with_total_kernel n

theorem epk_weighted_total_factors_when_kernel_declares_total (n : Nat) :
    ∃ F : (cochainTotalPD n).ResidualQuotient → Nat,
      ∀ c : CochainDiag n,
        F ((cochainTotalPD n).classOf c) = weightedTotalMap n c :=
  PaperGS003.epk_weighted_total_factors_when_kernel_declares_total n

theorem diagnostic_and_weighted_total_factor_when_kernel_declares_total
    (n : Nat) :
    ∃ F : (cochainTotalPD n).ResidualQuotient → (Fin n → Nat) × Nat,
      ∀ c : CochainDiag n,
        F ((cochainTotalPD n).classOf c) =
          (diagMap n c, weightedTotalMap n c) :=
  PaperGS003.diagnostic_and_weighted_total_factor_when_kernel_declares_total n

theorem total_quotient_projects_to_local_quotient (n : Nat) :
    ∃ F : (cochainTotalPD n).ResidualQuotient → (cochainPD n).ResidualQuotient,
      ∀ c : CochainDiag n,
        F ((cochainTotalPD n).classOf c) = (cochainPD n).classOf c :=
  PaperGS003.total_quotient_projects_to_local_quotient n

theorem local_quotient_does_not_lift_to_total_quotient_succ (n : Nat) :
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient →
        (cochainTotalPD (Nat.succ n)).ResidualQuotient,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          (cochainTotalPD (Nat.succ n)).classOf c) :=
  PaperGS003.local_quotient_does_not_lift_to_total_quotient_succ n

theorem weighted_total_invariant_with_weight_kernel (n : Nat) :
    (cochainWeightedPD n).InvariantCongruent (weightedTotalMap n) :=
  PaperGS003.weighted_total_invariant_with_weight_kernel n

theorem epk_weighted_total_factors_when_kernel_declares_weights (n : Nat) :
    ∃ F : (cochainWeightedPD n).ResidualQuotient → Nat,
      ∀ c : CochainDiag n,
        F ((cochainWeightedPD n).classOf c) = weightedTotalMap n c :=
  PaperGS003.epk_weighted_total_factors_when_kernel_declares_weights n

theorem diag_invariant_with_weight_kernel (n : Nat) :
    (cochainWeightedPD n).InvariantCongruent (diagMap n) :=
  PaperGS003.diag_invariant_with_weight_kernel n

theorem weight_invariant_with_weight_kernel (n : Nat) :
    (cochainWeightedPD n).InvariantCongruent (weightMap n) :=
  PaperGS003.weight_invariant_with_weight_kernel n

theorem diagnostic_and_weighted_total_factor_when_kernel_declares_weights
    (n : Nat) :
    ∃ F : (cochainWeightedPD n).ResidualQuotient → (Fin n → Nat) × Nat,
      ∀ c : CochainDiag n,
        F ((cochainWeightedPD n).classOf c) =
          (diagMap n c, weightedTotalMap n c) :=
  PaperGS003.diagnostic_and_weighted_total_factor_when_kernel_declares_weights n

theorem weighted_kernel_refines_local_kernel (n : Nat) :
    ∀ x y : CochainDiag n,
      (cochainWeightedPD n).ZeroRel x y → (cochainPD n).ZeroRel x y :=
  PaperGS003.weighted_kernel_refines_local_kernel n

theorem weighted_kernel_refines_total_kernel (n : Nat) :
    ∀ x y : CochainDiag n,
      (cochainWeightedPD n).ZeroRel x y → (cochainTotalPD n).ZeroRel x y :=
  PaperGS003.weighted_kernel_refines_total_kernel n

theorem weighted_quotient_projects_to_local_quotient (n : Nat) :
    ∃ F : (cochainWeightedPD n).ResidualQuotient → (cochainPD n).ResidualQuotient,
      ∀ c : CochainDiag n,
        F ((cochainWeightedPD n).classOf c) = (cochainPD n).classOf c :=
  PaperGS003.weighted_quotient_projects_to_local_quotient n

theorem weighted_quotient_projects_to_total_quotient (n : Nat) :
    ∃ F : (cochainWeightedPD n).ResidualQuotient → (cochainTotalPD n).ResidualQuotient,
      ∀ c : CochainDiag n,
        F ((cochainWeightedPD n).classOf c) = (cochainTotalPD n).classOf c :=
  PaperGS003.weighted_quotient_projects_to_total_quotient n

theorem local_quotient_does_not_lift_to_weighted_quotient_succ (n : Nat) :
    ¬ (∃ F : (cochainPD (Nat.succ n)).ResidualQuotient →
        (cochainWeightedPD (Nat.succ n)).ResidualQuotient,
      ∀ c : CochainDiag (Nat.succ n),
        F ((cochainPD (Nat.succ n)).classOf c) =
          (cochainWeightedPD (Nat.succ n)).classOf c) :=
  PaperGS003.local_quotient_does_not_lift_to_weighted_quotient_succ n

theorem total_quotient_does_not_lift_to_weighted_quotient_two_edges :
    ¬ (∃ F : (cochainTotalPD 2).ResidualQuotient →
        (cochainWeightedPD 2).ResidualQuotient,
      ∀ c : CochainDiag 2,
        F ((cochainTotalPD 2).classOf c) =
          (cochainWeightedPD 2).classOf c) :=
  PaperGS003.total_quotient_does_not_lift_to_weighted_quotient_two_edges

end LGGR

end PaperGS003

/-! ## Axiom audit (paper promotion requirement)

`#print axioms` for the load-bearing results cited by the encyclopedia entries
(ENC-1082 / ENC-1085 counterexamples, ENC-0245 edge-uniformity collapse,
ENC-1081 LGGR obstruction, ENC-1084 EPK kernel boundary). All should resolve to
the standard Lean environment axioms only. -/

-- Counterexamples (ENC-1085, ENC-1082)
#print axioms PaperGS003.ce1_quadratic_not_l1_scalar
#print axioms PaperGS003.ce2_weighted_l1_not_uniform
#print axioms PaperGS003.ce3_cross_edge_coupling_not_edge_local
#print axioms PaperGS003.ce4_orbit_weighted_not_unweighted
#print axioms PaperGS003.ce5_lp_not_homogeneous

-- Theorem 1 positive-coordinate finite core (ENC-0243 / PL-004-2)
#print axioms PaperGS003.coord_nat_l1_weighted_sum
#print axioms PaperGS003.coord_nat_l1_scalar_sum_succ
#print axioms PaperGS003.coord_real_l1_weighted_sum
#print axioms PaperGS003.coord_real_l1_scalar_sum_succ
#print axioms PaperGS003.coord_real_l1_exists_scalar_succ
#print axioms PaperGS003.coord_real_l1_norm_scalar_positive_succ

-- Theorem 2/3 finite declared-orbit aggregation cores (ENC-0244 / ENC-0245)
#print axioms PaperGS003.single_edge_weighted_l1_total
#print axioms PaperGS003.orbit_weight_eq_of_isometric_single_edge_invariance
#print axioms PaperGS003.orbit_weighted_l1_aggregation
#print axioms PaperGS003.orbit_uniform_l1_collapse
#print axioms PaperGS003.edge_uniform_l1_collapse

-- Theorem 3 edge-uniformity collapse cores (ENC-0245)
#print axioms PaperGS003.edge_uniformity_collapses_two_edge_l1
#print axioms PaperGS003.edge_uniformity_collapses_finite_l1
#print axioms PaperGS003.weighted_total_eq_scalar_unweighted_total_of_uniform_weights
#print axioms PaperGS003.uniform_weighted_total_factors_through_local_kernel
#print axioms PaperGS003.uniform_scalar_pair_factors_through_local_kernel

-- LGGR edgewise-uniformity obstruction (ENC-1081)
#print axioms PaperGS003.lggr_edgewise_uniformity_obstruction
#print axioms PaperGS003.lggr_edgewise_uniformity_obstruction_succ
#print axioms PaperGS003.scalar_total_lggr_obstruction_succ

-- EPK kernel boundary (ENC-1084)
#print axioms PaperGS003.epk_local_kernel_does_not_determine_weight_profile
#print axioms PaperGS003.epk_local_kernel_does_not_determine_weighted_total
#print axioms PaperGS003.diagnostic_and_weighted_total_do_not_factor_through_local_kernel_succ
#print axioms PaperGS003.epk_weighted_total_factors_when_kernel_declares_weights
#print axioms PaperGS003.weighted_quotient_projects_to_local_quotient
#print axioms PaperGS003.local_quotient_does_not_lift_to_weighted_quotient_succ
