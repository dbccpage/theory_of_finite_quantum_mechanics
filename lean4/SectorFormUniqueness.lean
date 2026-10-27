import BornMatrixCarrier
import Mathlib.Data.Fin.VecNotation
import Mathlib.Logic.Equiv.Basic
import Mathlib.Tactic.FinCases

/-
Uniqueness of the inner product on the sector carrier (rational case).  AuthorityEffect: None.

Carrier.  V := Fin n → ℚ, the free ℚ-linearization of n report sectors (FreeLinearization); a candidate inner
product is a symmetric Gram matrix G with pairing `pair G x y = x ⬝ᵥ (G *ᵥ y)` and quadratic readout
`qf G x = x ⬝ᵥ (G *ᵥ x)` — the same `qf` that `BornMatrixCarrier` uses to order effects, imported
unchanged.

Two hypotheses are put on the readout, and nothing else:

* `SectorAdditive G`: `qf G (u + v) = qf G u + qf G v` whenever `u` and `v` have disjoint sector
  supports.  This is the quadratic transcription of edgewise l1 additivity (the l1 sector weight
  satisfies exactly this law on disjoint supports, `l1_disjoint_additive`; cf. L1-GS000-EDGEWISE-L1
  and the D1 additivity defect of QM_020 Thm 2a).
* `Invariant G σ` for every sector permutation σ in a set S whose generated group acts
  transitively on sectors (`Generated`, `invariant_of_generated`): the readout does not see a
  relabelling of sectors (the permutation isometry envelope of PermutationUnitary).

Results.
1. `offdiag_eq_zero` / `eq_diagonal_of_sectorAdditive`: sector additivity forces every off-diagonal
   Gram entry to vanish, i.e. the sector basis is orthogonal for every sector-additive form.  This
   is the content of L1-IMP-ORTHOGONAL-ADDITIVITY, derived from the additivity law alone.
   `qf_eq_sum_diag_sq_of_sectorAdditive` gives the readout `Σ G i i · x i ^ 2` without assuming
   symmetry (the skew part of G is invisible to the readout, `qf_eq_zero_of_skew`).
2. `diag_const_of_transitive` / `eq_smul_one` / `eq_smul_one_generated`: transitive permutation
   invariance collapses the diagonal to a constant, so `G = c • 1` with `c = G i₀ i₀`;
   `scale_pos` gives `c > 0` for a
   positive-definite form; `pair_eq_scale_dot` identifies the pairing with `c · (x ⬝ᵥ y)`.
3. `unique_of_normalized`, `unique_up_to_scale`: any two such forms agree once one diagonal entry is
   matched; in general they are proportional.  `one_sectorAdditive`, `one_invariant` show that the
   standard dot product (the `qf 1` of the Born carrier) satisfies the hypotheses, so the selection is
   consistent and nonvacuous.
4. Countermodels, each hypothesis used: `diag12 = diag(1, 2)` (the InnerProductAdmission `gram_not_unique` form) is
   symmetric, positive definite and sector additive but not invariant under the sector swap and not a
   scalar multiple of 1; `unif12 = 1 + (all ones)` is symmetric, positive definite and invariant under
   every permutation of two sectors but not sector additive and not a scalar multiple of 1.

What is not claimed.  Nothing derives the carrier V, the scalar field ℚ, or the quadratic shape of
the readout from primitives; the two laws above are hypotheses, and the scale c is a unit choice.
Everything is exact over ℚ; no real numbers, limits or continuity.
-/

namespace InnerProductFinite.SectorForm

open Matrix BornFinite.MatrixCarrier

variable {n : ℕ}

/-! ### Pairing, disjoint supports, sector additivity -/

/-- The bilinear pairing of the Gram matrix `G`. -/
def pair (G : Matrix (Fin n) (Fin n) ℚ) (x y : Fin n → ℚ) : ℚ := x ⬝ᵥ (G *ᵥ y)

theorem pair_self (G : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) : pair G x x = qf G x := rfl

/-- Two carrier vectors have disjoint sector supports: no sector carries both. -/
def DisjointSupport (u v : Fin n → ℚ) : Prop := ∀ k, u k = 0 ∨ v k = 0

/-- Sector additivity of the quadratic readout on disjointly supported vectors. -/
def SectorAdditive (G : Matrix (Fin n) (Fin n) ℚ) : Prop :=
  ∀ u v, DisjointSupport u v → qf G (u + v) = qf G u + qf G v

/-- The l1 sector weight is additive on disjoint supports: the law `SectorAdditive` transcribes. -/
theorem l1_disjoint_additive (u v : Fin n → ℚ) (h : DisjointSupport u v) :
    ∑ i, |u i + v i| = ∑ i, |u i| + ∑ i, |v i| := by
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rcases h i with hu | hv
  · rw [hu, zero_add, abs_zero, zero_add]
  · rw [hv, add_zero, abs_zero, add_zero]

theorem qf_add_vec (G : Matrix (Fin n) (Fin n) ℚ) (u v : Fin n → ℚ) :
    qf G (u + v) = qf G u + pair G u v + pair G v u + qf G v := by
  simp only [qf, pair, mulVec_add, dotProduct_add, add_dotProduct]
  ring

theorem mulVec_single_one' (G : Matrix (Fin n) (Fin n) ℚ) (j : Fin n) :
    G *ᵥ Pi.single j 1 = fun i => G i j := by
  funext i
  simp [Matrix.mulVec, dotProduct_single]

theorem pair_single_single (G : Matrix (Fin n) (Fin n) ℚ) (i j : Fin n) :
    pair G (Pi.single i 1) (Pi.single j 1) = G i j := by
  rw [pair, mulVec_single_one', single_dotProduct, one_mul]

theorem qf_single (G : Matrix (Fin n) (Fin n) ℚ) (i : Fin n) : qf G (Pi.single i 1) = G i i :=
  pair_single_single G i i

theorem disjoint_single_single {i j : Fin n} (h : i ≠ j) :
    DisjointSupport (Pi.single i (1 : ℚ)) (Pi.single j 1) := by
  intro k
  by_cases hk : k = i
  · right
    subst hk
    exact Pi.single_eq_of_ne h 1
  · left
    exact Pi.single_eq_of_ne hk 1

theorem single_ne_zero (i : Fin n) : (Pi.single i (1 : ℚ) : Fin n → ℚ) ≠ 0 := by
  intro h
  have := congrFun h i
  simp at this

/-! ### 1. Sector additivity forces an orthogonal sector basis -/

/-- The symmetric part of every off-diagonal pair vanishes (no symmetry of `G` assumed). -/
theorem offdiag_pair_sum_eq_zero {G : Matrix (Fin n) (Fin n) ℚ} (hG : SectorAdditive G)
    {i j : Fin n} (h : i ≠ j) : G i j + G j i = 0 := by
  have := hG _ _ (disjoint_single_single h)
  rw [qf_add_vec, pair_single_single, pair_single_single] at this
  linarith

theorem transpose_entry {G : Matrix (Fin n) (Fin n) ℚ} (hs : Gᵀ = G) (i j : Fin n) :
    G i j = G j i := by
  simpa [Matrix.transpose_apply] using congrFun (congrFun hs j) i

/-- For a symmetric sector-additive form every off-diagonal entry is zero. -/
theorem offdiag_eq_zero {G : Matrix (Fin n) (Fin n) ℚ} (hs : Gᵀ = G) (hG : SectorAdditive G)
    {i j : Fin n} (h : i ≠ j) : G i j = 0 := by
  have h1 := offdiag_pair_sum_eq_zero hG h
  have h2 := transpose_entry hs i j
  linarith

theorem eq_diagonal_of_sectorAdditive {G : Matrix (Fin n) (Fin n) ℚ} (hs : Gᵀ = G)
    (hG : SectorAdditive G) : G = Matrix.diagonal (fun i => G i i) := by
  ext i j
  by_cases h : i = j
  · subst h
    simp
  · rw [Matrix.diagonal_apply_ne _ h]
    exact offdiag_eq_zero hs hG h

theorem qf_diagonal (d : Fin n → ℚ) (x : Fin n → ℚ) :
    qf (Matrix.diagonal d) x = ∑ i, d i * x i ^ 2 := by
  simp only [qf, dotProduct, mulVec_diagonal]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  ring

theorem qf_transpose (G : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) : qf Gᵀ x = qf G x := by
  unfold qf
  rw [Matrix.mulVec_transpose, dotProduct_comm, ← dotProduct_mulVec]

/-- Half the symmetric part of `G`; its readout agrees with that of `G`. -/
def symmPart (G : Matrix (Fin n) (Fin n) ℚ) : Matrix (Fin n) (Fin n) ℚ := (1 / 2 : ℚ) • (G + Gᵀ)

theorem symmPart_transpose (G : Matrix (Fin n) (Fin n) ℚ) : (symmPart G)ᵀ = symmPart G := by
  unfold symmPart
  rw [Matrix.transpose_smul, Matrix.transpose_add, Matrix.transpose_transpose, add_comm]

theorem symmPart_apply (G : Matrix (Fin n) (Fin n) ℚ) (i j : Fin n) :
    symmPart G i j = (1 / 2) * (G i j + G j i) := by
  simp [symmPart, Matrix.smul_apply, Matrix.add_apply, Matrix.transpose_apply]

theorem qf_symmPart (G : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) : qf (symmPart G) x = qf G x := by
  unfold symmPart
  rw [qf_smul, qf_add, qf_transpose]
  ring

theorem sectorAdditive_symmPart {G : Matrix (Fin n) (Fin n) ℚ} (hG : SectorAdditive G) :
    SectorAdditive (symmPart G) := by
  intro u v h
  rw [qf_symmPart, qf_symmPart, qf_symmPart]
  exact hG u v h

/-- The readout of any sector-additive form is the diagonal sum `Σ G i i · x i ^ 2`. -/
theorem qf_eq_sum_diag_sq_of_sectorAdditive {G : Matrix (Fin n) (Fin n) ℚ} (hG : SectorAdditive G)
    (x : Fin n → ℚ) : qf G x = ∑ i, G i i * x i ^ 2 := by
  have hd := eq_diagonal_of_sectorAdditive (symmPart_transpose G) (sectorAdditive_symmPart hG)
  rw [← qf_symmPart, hd, qf_diagonal]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rw [symmPart_apply]
  ring

/-! ### 2. Transitive sector symmetry collapses the diagonal -/

/-- Coordinate action of a sector permutation, `(permute σ x) i = x (σ.symm i)` (the convention of
PermutationUnitary `permU`), so that `permute σ (Pi.single j 1) = Pi.single (σ j) 1`. -/
def permute (σ : Equiv.Perm (Fin n)) (x : Fin n → ℚ) : Fin n → ℚ := fun i => x (σ.symm i)

theorem permute_single (σ : Equiv.Perm (Fin n)) (j : Fin n) :
    permute σ (Pi.single j (1 : ℚ)) = Pi.single (σ j) 1 := by
  funext i
  simp only [permute, Pi.single_apply, Equiv.symm_apply_eq]

/-- `G` is invariant under the sector permutation `σ` when its readout is. -/
def Invariant (G : Matrix (Fin n) (Fin n) ℚ) (σ : Equiv.Perm (Fin n)) : Prop :=
  ∀ x, qf G (permute σ x) = qf G x

/-- A set of sector permutations acts transitively on sectors: any two distinct sectors are
exchanged by some member. -/
def TransitiveOn (S : Set (Equiv.Perm (Fin n))) : Prop := ∀ i j : Fin n, i ≠ j → ∃ σ ∈ S, σ i = j

theorem diag_eq_of_invariant {G : Matrix (Fin n) (Fin n) ℚ} {σ : Equiv.Perm (Fin n)}
    (h : Invariant G σ) (j : Fin n) : G (σ j) (σ j) = G j j := by
  have := h (Pi.single j 1)
  rwa [permute_single, qf_single, qf_single] at this

theorem diag_const_of_transitive {G : Matrix (Fin n) (Fin n) ℚ} {S : Set (Equiv.Perm (Fin n))}
    (hS : ∀ σ ∈ S, Invariant G σ) (hT : TransitiveOn S) (i j : Fin n) : G i i = G j j := by
  by_cases hij : i = j
  · rw [hij]
  · obtain ⟨σ, hσ, rfl⟩ := hT i j hij
    exact (diag_eq_of_invariant (hS σ hσ) i).symm

/-! Invariance is closed under the group operations, so the symmetry hypothesis may be stated for
generators: the group they generate is recorded as an inductive predicate. -/

/-- The group generated by a set of sector permutations. -/
inductive Generated (S : Set (Equiv.Perm (Fin n))) : Equiv.Perm (Fin n) → Prop
  | of {σ : Equiv.Perm (Fin n)} (h : σ ∈ S) : Generated S σ
  | one : Generated S 1
  | mul {σ τ : Equiv.Perm (Fin n)} (hσ : Generated S σ) (hτ : Generated S τ) : Generated S (σ * τ)
  | inv {σ : Equiv.Perm (Fin n)} (hσ : Generated S σ) : Generated S σ⁻¹

theorem permute_one (x : Fin n → ℚ) : permute (1 : Equiv.Perm (Fin n)) x = x := by
  funext i
  rfl

theorem permute_mul (σ τ : Equiv.Perm (Fin n)) (x : Fin n → ℚ) :
    permute (σ * τ) x = permute σ (permute τ x) := by
  funext i
  simp only [permute, Equiv.Perm.mul_def, Equiv.symm_trans_apply]

theorem permute_inv_left (σ : Equiv.Perm (Fin n)) (x : Fin n → ℚ) :
    permute σ⁻¹ (permute σ x) = x := by
  funext i
  simp only [permute, Equiv.Perm.inv_def, Equiv.symm_symm, Equiv.symm_apply_apply]

theorem permute_inv_right (σ : Equiv.Perm (Fin n)) (x : Fin n → ℚ) :
    permute σ (permute σ⁻¹ x) = x := by
  have := permute_inv_left σ⁻¹ x
  rwa [inv_inv] at this

theorem invariant_one (G : Matrix (Fin n) (Fin n) ℚ) : Invariant G 1 := fun x => by
  rw [permute_one]

theorem invariant_mul {G : Matrix (Fin n) (Fin n) ℚ} {σ τ : Equiv.Perm (Fin n)}
    (hσ : Invariant G σ) (hτ : Invariant G τ) : Invariant G (σ * τ) := fun x => by
  rw [permute_mul, hσ, hτ]

theorem invariant_inv {G : Matrix (Fin n) (Fin n) ℚ} {σ : Equiv.Perm (Fin n)}
    (hσ : Invariant G σ) : Invariant G σ⁻¹ := fun x => by
  have h := hσ (permute σ⁻¹ x)
  rw [permute_inv_right] at h
  exact h.symm

theorem invariant_of_generated {G : Matrix (Fin n) (Fin n) ℚ} {S : Set (Equiv.Perm (Fin n))}
    (hS : ∀ σ ∈ S, Invariant G σ) {σ : Equiv.Perm (Fin n)} (h : Generated S σ) : Invariant G σ := by
  induction h with
  | of hm => exact hS _ hm
  | one => exact invariant_one G
  | mul _ _ ih₁ ih₂ => exact invariant_mul ih₁ ih₂
  | inv _ ih => exact invariant_inv ih

/-- Main theorem: a symmetric, sector-additive form invariant under a transitive set of sector
permutations is a scalar multiple of the identity, the scalar being any diagonal entry. -/
theorem eq_smul_one {G : Matrix (Fin n) (Fin n) ℚ} {S : Set (Equiv.Perm (Fin n))} (hs : Gᵀ = G)
    (hA : SectorAdditive G) (hS : ∀ σ ∈ S, Invariant G σ) (hT : TransitiveOn S) (i₀ : Fin n) :
    G = G i₀ i₀ • (1 : Matrix (Fin n) (Fin n) ℚ) := by
  ext i j
  by_cases h : i = j
  · subst h
    rw [Matrix.smul_apply, Matrix.one_apply_eq, smul_eq_mul, mul_one]
    exact diag_const_of_transitive hS hT i i₀
  · rw [Matrix.smul_apply, Matrix.one_apply_ne h, smul_zero]
    exact offdiag_eq_zero hs hA h

/-- The main theorem with the symmetry hypothesis on generators only: invariance under a set `S`
whose generated group acts transitively. -/
theorem eq_smul_one_generated {G : Matrix (Fin n) (Fin n) ℚ} {S : Set (Equiv.Perm (Fin n))}
    (hs : Gᵀ = G) (hA : SectorAdditive G) (hS : ∀ σ ∈ S, Invariant G σ)
    (hT : TransitiveOn (Generated S)) (i₀ : Fin n) :
    G = G i₀ i₀ • (1 : Matrix (Fin n) (Fin n) ℚ) :=
  eq_smul_one hs hA (fun _ hσ => invariant_of_generated hS hσ) hT i₀

theorem qf_eq_scale_dot {G : Matrix (Fin n) (Fin n) ℚ} {S : Set (Equiv.Perm (Fin n))} (hs : Gᵀ = G)
    (hA : SectorAdditive G) (hS : ∀ σ ∈ S, Invariant G σ) (hT : TransitiveOn S) (i₀ : Fin n)
    (x : Fin n → ℚ) : qf G x = G i₀ i₀ * (x ⬝ᵥ x) := by
  have hG := eq_smul_one hs hA hS hT i₀
  calc qf G x = qf (G i₀ i₀ • (1 : Matrix (Fin n) (Fin n) ℚ)) x := by rw [← hG]
    _ = G i₀ i₀ * (x ⬝ᵥ x) := by rw [qf_smul, qf_one]

theorem pair_smul_one (c : ℚ) (x y : Fin n → ℚ) :
    pair (c • (1 : Matrix (Fin n) (Fin n) ℚ)) x y = c * (x ⬝ᵥ y) := by
  rw [pair, Matrix.smul_mulVec, Matrix.one_mulVec, dotProduct_smul, smul_eq_mul]

theorem pair_eq_scale_dot {G : Matrix (Fin n) (Fin n) ℚ} {S : Set (Equiv.Perm (Fin n))} (hs : Gᵀ = G)
    (hA : SectorAdditive G) (hS : ∀ σ ∈ S, Invariant G σ) (hT : TransitiveOn S) (i₀ : Fin n)
    (x y : Fin n → ℚ) : pair G x y = G i₀ i₀ * (x ⬝ᵥ y) := by
  have hG := eq_smul_one hs hA hS hT i₀
  calc pair G x y = pair (G i₀ i₀ • (1 : Matrix (Fin n) (Fin n) ℚ)) x y := by rw [← hG]
    _ = G i₀ i₀ * (x ⬝ᵥ y) := pair_smul_one _ x y

/-- Positive definiteness of the readout makes the scale positive. -/
theorem scale_pos {G : Matrix (Fin n) (Fin n) ℚ} (hpos : ∀ x, x ≠ 0 → 0 < qf G x) (i₀ : Fin n) :
    0 < G i₀ i₀ := by
  have := hpos _ (single_ne_zero i₀)
  rwa [qf_single] at this

/-! ### 3. Uniqueness and nonvacuity -/

theorem unique_of_normalized {G G' : Matrix (Fin n) (Fin n) ℚ} {S : Set (Equiv.Perm (Fin n))}
    (hs : Gᵀ = G) (hA : SectorAdditive G) (hS : ∀ σ ∈ S, Invariant G σ)
    (hs' : G'ᵀ = G') (hA' : SectorAdditive G') (hS' : ∀ σ ∈ S, Invariant G' σ)
    (hT : TransitiveOn S) (i₀ : Fin n) (hnorm : G i₀ i₀ = G' i₀ i₀) : G = G' := by
  rw [eq_smul_one hs hA hS hT i₀, eq_smul_one hs' hA' hS' hT i₀, hnorm]

theorem unique_up_to_scale {G G' : Matrix (Fin n) (Fin n) ℚ} {S : Set (Equiv.Perm (Fin n))}
    (hs : Gᵀ = G) (hA : SectorAdditive G) (hS : ∀ σ ∈ S, Invariant G σ)
    (hs' : G'ᵀ = G') (hA' : SectorAdditive G') (hS' : ∀ σ ∈ S, Invariant G' σ)
    (hT : TransitiveOn S) (i₀ : Fin n) (h0 : G i₀ i₀ ≠ 0) :
    G' = (G' i₀ i₀ / G i₀ i₀) • G := by
  have hG := eq_smul_one hs hA hS hT i₀
  have hG' := eq_smul_one hs' hA' hS' hT i₀
  calc G' = G' i₀ i₀ • (1 : Matrix (Fin n) (Fin n) ℚ) := hG'
    _ = (G' i₀ i₀ / G i₀ i₀) • (G i₀ i₀ • (1 : Matrix (Fin n) (Fin n) ℚ)) := by
        rw [smul_smul, div_mul_cancel₀ _ h0]
    _ = (G' i₀ i₀ / G i₀ i₀) • G := by rw [← hG]

theorem pair_diagonal_eq_zero_of_disjoint (d : Fin n → ℚ) {u v : Fin n → ℚ}
    (h : DisjointSupport u v) : pair (Matrix.diagonal d) u v = 0 := by
  simp only [pair, dotProduct, mulVec_diagonal]
  refine Finset.sum_eq_zero (fun i _ => ?_)
  rcases h i with hu | hv
  · rw [hu, zero_mul]
  · rw [hv, mul_zero, mul_zero]

/-- Every diagonal form is sector additive. -/
theorem diagonal_sectorAdditive (d : Fin n → ℚ) : SectorAdditive (Matrix.diagonal d) := by
  intro u v h
  rw [qf_add_vec, pair_diagonal_eq_zero_of_disjoint d h,
    pair_diagonal_eq_zero_of_disjoint d (fun k => (h k).symm)]
  ring

theorem one_sectorAdditive : SectorAdditive (1 : Matrix (Fin n) (Fin n) ℚ) := by
  rw [← Matrix.diagonal_one]
  exact diagonal_sectorAdditive _

theorem dot_permute (σ : Equiv.Perm (Fin n)) (x : Fin n → ℚ) :
    permute σ x ⬝ᵥ permute σ x = x ⬝ᵥ x := by
  unfold dotProduct permute
  exact Equiv.sum_comp σ.symm (fun i => x i * x i)

/-- The standard form is invariant under every sector permutation. -/
theorem one_invariant (σ : Equiv.Perm (Fin n)) : Invariant (1 : Matrix (Fin n) (Fin n) ℚ) σ := by
  intro x
  rw [qf_one, qf_one, dot_permute]

theorem one_posdef (x : Fin n → ℚ) (hx : x ≠ 0) : 0 < qf (1 : Matrix (Fin n) (Fin n) ℚ) x := by
  rw [qf_one]
  exact dot_self_pos hx

/-- The selected form is the Born carrier's standard form: with the unit normalisation
`G i₀ i₀ = 1` the hypotheses pin `G = 1`, whose readout is the `qf 1` of `BornMatrixCarrier`. -/
theorem eq_one_of_normalized {G : Matrix (Fin n) (Fin n) ℚ} {S : Set (Equiv.Perm (Fin n))}
    (hs : Gᵀ = G) (hA : SectorAdditive G) (hS : ∀ σ ∈ S, Invariant G σ) (hT : TransitiveOn S)
    (i₀ : Fin n) (hnorm : G i₀ i₀ = 1) : G = 1 := by
  rw [eq_smul_one hs hA hS hT i₀, hnorm, one_smul]

/-! ### 4. Countermodels: each hypothesis is used -/

/-- The InnerProductAdmission form `diag(1, 2)`. -/
def diag12 : Matrix (Fin 2) (Fin 2) ℚ := Matrix.diagonal ![1, 2]

theorem diag12_transpose : diag12ᵀ = diag12 := Matrix.diagonal_transpose _

theorem diag12_sectorAdditive : SectorAdditive diag12 := diagonal_sectorAdditive _

theorem diag12_qf (x : Fin 2 → ℚ) : qf diag12 x = x 0 * x 0 + 2 * (x 1 * x 1) := by
  rw [diag12, qf_diagonal, Fin.sum_univ_two]
  simp
  ring

theorem diag12_posdef (x : Fin 2 → ℚ) (hx : x ≠ 0) : 0 < qf diag12 x := by
  rw [diag12_qf]
  have h0 := mul_self_nonneg (x 0)
  have h1 := mul_self_nonneg (x 1)
  by_cases hx0 : x 0 = 0
  · have hx1 : x 1 ≠ 0 := by
      intro hx1
      apply hx
      funext i
      fin_cases i
      · exact hx0
      · exact hx1
    have := mul_self_pos.mpr hx1
    linarith
  · have := mul_self_pos.mpr hx0
    linarith

/-- `diag(1, 2)` is not invariant under the sector swap. -/
theorem diag12_not_invariant_swap : ¬ Invariant diag12 (Equiv.swap 0 1) := by
  intro h
  have := diag_eq_of_invariant h 0
  rw [Equiv.swap_apply_left] at this
  simp [diag12] at this

theorem diag12_not_scalar (c : ℚ) : diag12 ≠ c • (1 : Matrix (Fin 2) (Fin 2) ℚ) := by
  intro h
  have h0 := congrFun (congrFun h 0) 0
  have h1 := congrFun (congrFun h 1) 1
  simp [diag12] at h0 h1
  linarith

/-- `1 + (all ones)` on two sectors. -/
def unif12 : Matrix (Fin 2) (Fin 2) ℚ := 1 + Matrix.of (fun _ _ => (1 : ℚ))

theorem unif12_apply (i j : Fin 2) : unif12 i j = (if i = j then 1 else 0) + 1 := by
  simp [unif12, Matrix.add_apply, Matrix.one_apply]

theorem unif12_transpose : unif12ᵀ = unif12 := by
  ext i j
  rw [Matrix.transpose_apply, unif12_apply, unif12_apply]
  by_cases h : i = j
  · subst h
    rfl
  · rw [if_neg h, if_neg (Ne.symm h)]

theorem unif12_qf (x : Fin 2 → ℚ) :
    qf unif12 x = x 0 * x 0 + x 1 * x 1 + (x 0 + x 1) * (x 0 + x 1) := by
  rw [qf_eq_sum_sum, Fin.sum_univ_two, Fin.sum_univ_two, Fin.sum_univ_two]
  simp only [unif12_apply]
  norm_num
  ring

theorem unif12_posdef (x : Fin 2 → ℚ) (hx : x ≠ 0) : 0 < qf unif12 x := by
  rw [unif12_qf]
  have h0 := mul_self_nonneg (x 0)
  have h1 := mul_self_nonneg (x 1)
  have h2 := mul_self_nonneg (x 0 + x 1)
  by_cases hx0 : x 0 = 0
  · have hx1 : x 1 ≠ 0 := by
      intro hx1
      apply hx
      funext i
      fin_cases i
      · exact hx0
      · exact hx1
    have := mul_self_pos.mpr hx1
    linarith
  · have := mul_self_pos.mpr hx0
    linarith

theorem permute_swap_zero (x : Fin 2 → ℚ) : permute (Equiv.swap 0 1) x 0 = x 1 := by
  simp [permute, Equiv.symm_swap, Equiv.swap_apply_left]

theorem permute_swap_one (x : Fin 2 → ℚ) : permute (Equiv.swap 0 1) x 1 = x 0 := by
  simp [permute, Equiv.symm_swap, Equiv.swap_apply_right]

/-- The two-sector symmetry set `{swap}`. -/
def S₂ : Set (Equiv.Perm (Fin 2)) := {Equiv.swap 0 1}

theorem S₂_transitive : TransitiveOn S₂ := by
  intro i j hij
  fin_cases i <;> fin_cases j
  · exact absurd rfl hij
  · exact ⟨Equiv.swap 0 1, rfl, Equiv.swap_apply_left 0 1⟩
  · exact ⟨Equiv.swap 0 1, rfl, Equiv.swap_apply_right 0 1⟩
  · exact absurd rfl hij

theorem unif12_invariant : ∀ σ ∈ S₂, Invariant unif12 σ := by
  intro σ hσ x
  have h : σ = Equiv.swap 0 1 := hσ
  subst h
  rw [unif12_qf, unif12_qf, permute_swap_zero, permute_swap_one]
  ring

/-- `1 + (all ones)` is not sector additive: the two sectors interfere. -/
theorem unif12_not_sectorAdditive : ¬ SectorAdditive unif12 := by
  intro h
  have := h _ _ (disjoint_single_single (show (0 : Fin 2) ≠ 1 by decide))
  rw [qf_add_vec, pair_single_single, pair_single_single, qf_single, qf_single] at this
  simp [unif12_apply] at this

theorem unif12_not_scalar (c : ℚ) : unif12 ≠ c • (1 : Matrix (Fin 2) (Fin 2) ℚ) := by
  intro h
  have h01 := congrFun (congrFun h 0) 1
  simp [unif12_apply] at h01

end InnerProductFinite.SectorForm

#print axioms InnerProductFinite.SectorForm.pair
#print axioms InnerProductFinite.SectorForm.pair_self
#print axioms InnerProductFinite.SectorForm.DisjointSupport
#print axioms InnerProductFinite.SectorForm.SectorAdditive
#print axioms InnerProductFinite.SectorForm.l1_disjoint_additive
#print axioms InnerProductFinite.SectorForm.qf_add_vec
#print axioms InnerProductFinite.SectorForm.mulVec_single_one'
#print axioms InnerProductFinite.SectorForm.pair_single_single
#print axioms InnerProductFinite.SectorForm.qf_single
#print axioms InnerProductFinite.SectorForm.disjoint_single_single
#print axioms InnerProductFinite.SectorForm.single_ne_zero
#print axioms InnerProductFinite.SectorForm.offdiag_pair_sum_eq_zero
#print axioms InnerProductFinite.SectorForm.transpose_entry
#print axioms InnerProductFinite.SectorForm.offdiag_eq_zero
#print axioms InnerProductFinite.SectorForm.eq_diagonal_of_sectorAdditive
#print axioms InnerProductFinite.SectorForm.qf_diagonal
#print axioms InnerProductFinite.SectorForm.qf_transpose
#print axioms InnerProductFinite.SectorForm.symmPart
#print axioms InnerProductFinite.SectorForm.symmPart_transpose
#print axioms InnerProductFinite.SectorForm.symmPart_apply
#print axioms InnerProductFinite.SectorForm.qf_symmPart
#print axioms InnerProductFinite.SectorForm.sectorAdditive_symmPart
#print axioms InnerProductFinite.SectorForm.qf_eq_sum_diag_sq_of_sectorAdditive
#print axioms InnerProductFinite.SectorForm.permute
#print axioms InnerProductFinite.SectorForm.permute_single
#print axioms InnerProductFinite.SectorForm.Invariant
#print axioms InnerProductFinite.SectorForm.TransitiveOn
#print axioms InnerProductFinite.SectorForm.diag_eq_of_invariant
#print axioms InnerProductFinite.SectorForm.diag_const_of_transitive
#print axioms InnerProductFinite.SectorForm.Generated
#print axioms InnerProductFinite.SectorForm.permute_one
#print axioms InnerProductFinite.SectorForm.permute_mul
#print axioms InnerProductFinite.SectorForm.permute_inv_left
#print axioms InnerProductFinite.SectorForm.permute_inv_right
#print axioms InnerProductFinite.SectorForm.invariant_one
#print axioms InnerProductFinite.SectorForm.invariant_mul
#print axioms InnerProductFinite.SectorForm.invariant_inv
#print axioms InnerProductFinite.SectorForm.invariant_of_generated
#print axioms InnerProductFinite.SectorForm.eq_smul_one
#print axioms InnerProductFinite.SectorForm.eq_smul_one_generated
#print axioms InnerProductFinite.SectorForm.qf_eq_scale_dot
#print axioms InnerProductFinite.SectorForm.pair_smul_one
#print axioms InnerProductFinite.SectorForm.pair_eq_scale_dot
#print axioms InnerProductFinite.SectorForm.scale_pos
#print axioms InnerProductFinite.SectorForm.unique_of_normalized
#print axioms InnerProductFinite.SectorForm.unique_up_to_scale
#print axioms InnerProductFinite.SectorForm.pair_diagonal_eq_zero_of_disjoint
#print axioms InnerProductFinite.SectorForm.diagonal_sectorAdditive
#print axioms InnerProductFinite.SectorForm.one_sectorAdditive
#print axioms InnerProductFinite.SectorForm.dot_permute
#print axioms InnerProductFinite.SectorForm.one_invariant
#print axioms InnerProductFinite.SectorForm.one_posdef
#print axioms InnerProductFinite.SectorForm.eq_one_of_normalized
#print axioms InnerProductFinite.SectorForm.diag12
#print axioms InnerProductFinite.SectorForm.diag12_transpose
#print axioms InnerProductFinite.SectorForm.diag12_sectorAdditive
#print axioms InnerProductFinite.SectorForm.diag12_qf
#print axioms InnerProductFinite.SectorForm.diag12_posdef
#print axioms InnerProductFinite.SectorForm.diag12_not_invariant_swap
#print axioms InnerProductFinite.SectorForm.diag12_not_scalar
#print axioms InnerProductFinite.SectorForm.unif12
#print axioms InnerProductFinite.SectorForm.unif12_apply
#print axioms InnerProductFinite.SectorForm.unif12_transpose
#print axioms InnerProductFinite.SectorForm.unif12_qf
#print axioms InnerProductFinite.SectorForm.unif12_posdef
#print axioms InnerProductFinite.SectorForm.permute_swap_zero
#print axioms InnerProductFinite.SectorForm.permute_swap_one
#print axioms InnerProductFinite.SectorForm.S₂
#print axioms InnerProductFinite.SectorForm.S₂_transitive
#print axioms InnerProductFinite.SectorForm.unif12_invariant
#print axioms InnerProductFinite.SectorForm.unif12_not_sectorAdditive
#print axioms InnerProductFinite.SectorForm.unif12_not_scalar
