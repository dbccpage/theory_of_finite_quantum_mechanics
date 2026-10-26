import Mathlib

/-!
# The classical corner of the §18.1 axiom package

This is the first `WitnessedDifference` module built on Mathlib. It imports
nothing from the core-only modules, so their notations (`ℚ`, `∅`, `∑`, `≃`)
never meet Mathlib's in one file.

It proves outcome (a) of `WDP-CH18-O01` for two strengthened readings of the
candidate package W1–W6 of §18.1 (W3 with pointwise nonnegativity; dynamics that
preserve the form of W5 over `ℤ[i]`), and it locates the point where the package
stops being classical.

* `WDP-CH18-P02` (positive form). Over a finite report carrier, a linear update
  that sends pointwise nonnegative rational weights of total mass `W > 0` to
  weights of the same kind is column-stochastic. If it also has an inverse of
  the same kind, it is a permutation matrix, and conversely. With pointwise
  nonnegativity added to W3, the content of W4 ("reversible updates are
  bijections of the carrier") is a theorem for linear updates that are
  reversible within the states. The preservation clauses of the permutation
  isometry of `QuantumImports` hold for every finite carrier, not only `Bool`.
* `WDP-CH18-P03` (signed countermodel). Without pointwise nonnegativity the
  conclusion fails: `!![2, 1; -1, 0]` preserves total mass, has a
  mass-preserving inverse, is not a permutation matrix, and sends `(1, 0)` to
  the signed weight `(2, -1)` of the §18.2 remark.
* `WDP-CH18-P04` (form-preserving form). Over the Gaussian integers every
  matrix with `Uᴴ * U = 1` is monomial: one nonzero entry per column, a unit
  `±1` or `±i`, in rows given by a permutation. The phase-blind readout
  `π(v)_q = N(v_q)` of W6 then moves by that same permutation, so no such `U`
  separates two vectors with equal readout. Every finite run of such updates
  has its readout fixed by the initial readout and one permutation
  (`gaussian_run_readout`, not bound to a ledger row).
* `WDP-CH18-P05` (where the corner ends). The unnormalized Hadamard matrix of
  `H010` satisfies `Hᴴ * H = 2`, so it is not a unitary over `ℤ[i]`, and
  `WDP-CH18-P04` alone shows that no unitary over `ℤ[i]` can do what it does.
  Unitaries that do separate readout fibres exist once the scalar ring is
  enlarged by a finite localization: the rotation `!![3/5, -4/5; 4/5, 3/5]`
  with entries in `ℤ[1/5]`, and `½ !![1+i, 1-i; 1-i, 1+i]` with entries in
  `ℤ[i][1/2]`. Their readouts are rational rather than integral. Neither needs
  the continuum field.

No declaration here derives quantum theory, the Born rule, a Hilbert space,
or the continuum field. Every statement is finite and exact.
-/

namespace WitnessedDifference.ClassicalCorner

open Matrix Finset

/-! ## `WDP-CH18-P02`: nonnegative weights force permutations -/

section Positive

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- A weight of total mass `W`: pointwise nonnegative rationals summing to `W`
(Axiom W3 with pointwise nonnegativity added). -/
def IsState (W : ℚ) (w : ι → ℚ) : Prop :=
  (∀ i, 0 ≤ w i) ∧ ∑ i, w i = W

/-- A linear update, given by its matrix, that sends every state of mass `W` to
a state of mass `W`. -/
def PreservesStates (W : ℚ) (T : Matrix ι ι ℚ) : Prop :=
  ∀ w, IsState W w → IsState W (T *ᵥ w)

/-- Column-stochastic: nonnegative entries and every column summing to one. -/
def IsStochastic (T : Matrix ι ι ℚ) : Prop :=
  (∀ i j, 0 ≤ T i j) ∧ ∀ j, ∑ i, T i j = 1

theorem mulVec_single_apply (T : Matrix ι ι ℚ) (j : ι) (W : ℚ) (i : ι) :
    (T *ᵥ Pi.single j W) i = T i j * W := by
  simp [mulVec, dotProduct, Pi.single_apply]

theorem stochastic_of_preservesStates {W : ℚ} (hW : 0 < W) {T : Matrix ι ι ℚ}
    (hT : PreservesStates W T) : IsStochastic T := by
  have key : ∀ j, IsState W (T *ᵥ Pi.single j W) := by
    intro j
    refine hT _ ⟨fun i => ?_, by simp⟩
    by_cases h : i = j
    · subst h
      simp [hW.le]
    · simp [h]
  refine ⟨fun i j => ?_, fun j => ?_⟩
  · have h := (key j).1 i
    rw [mulVec_single_apply] at h
    exact (mul_nonneg_iff_of_pos_right hW).mp h
  · have h := (key j).2
    simp only [mulVec_single_apply] at h
    rw [← Finset.sum_mul] at h
    have h2 : (∑ i, T i j - 1) * W = 0 := by rw [sub_mul]; linarith
    rcases mul_eq_zero.mp h2 with h3 | h3
    · linarith
    · exact absurd h3 hW.ne'

omit [DecidableEq ι] in
theorem preservesStates_of_stochastic {W : ℚ} {T : Matrix ι ι ℚ}
    (hT : IsStochastic T) : PreservesStates W T := by
  rintro w ⟨hw0, hwW⟩
  refine ⟨fun i => ?_, ?_⟩
  · simp only [mulVec, dotProduct]
    exact Finset.sum_nonneg fun j _ => mul_nonneg (hT.1 i j) (hw0 j)
  · simp only [mulVec, dotProduct]
    rw [Finset.sum_comm]
    simp_rw [← Finset.sum_mul, hT.2, one_mul]
    exact hwW

/-- For `W > 0`, preserving states of mass `W` is the same as being
column-stochastic. -/
theorem preservesStates_iff_stochastic {W : ℚ} (hW : 0 < W) (T : Matrix ι ι ℚ) :
    PreservesStates W T ↔ IsStochastic T :=
  ⟨stochastic_of_preservesStates hW, preservesStates_of_stochastic⟩

/-- If `S * T = 1` with both stochastic and `T k j > 0`, then column `k` of `S`
is the basis vector `e_j`. -/
theorem column_eq_single_of_pos {S T : Matrix ι ι ℚ} (hS : IsStochastic S)
    (hT : IsStochastic T) (hST : S * T = 1) {j k : ι} (hkj : 0 < T k j) :
    ∀ i, S i k = if i = j then 1 else 0 := by
  have hzero : ∀ i, i ≠ j → S i k = 0 := by
    intro i hij
    have h := congrFun (congrFun hST i) j
    rw [mul_apply, one_apply_ne hij] at h
    have hall := (Finset.sum_eq_zero_iff_of_nonneg
      (fun l _ => mul_nonneg (hS.1 i l) (hT.1 l j))).mp h k (Finset.mem_univ k)
    rcases mul_eq_zero.mp hall with h1 | h1
    · exact h1
    · exact absurd h1 hkj.ne'
  intro i
  split_ifs with hij
  · subst hij
    have hsum := hS.2 k
    rwa [Finset.sum_eq_single i (fun b _ hb => hzero b hb) (by simp)] at hsum
  · exact hzero i hij

/-- A column-stochastic matrix with a column-stochastic inverse is a
permutation matrix. -/
theorem perm_of_stochastic_inverse {S T : Matrix ι ι ℚ} (hS : IsStochastic S)
    (hT : IsStochastic T) (hST : S * T = 1) :
    ∃ σ : Equiv.Perm ι, T = σ.permMatrix ℚ := by
  have hTS : T * S = 1 := mul_eq_one_comm.mp hST
  have hpos : ∀ j, ∃ k, 0 < T k j := by
    intro j
    by_contra h
    push Not at h
    have : ∑ i, T i j ≤ 0 := Finset.sum_nonpos fun i _ => h i
    linarith [hT.2 j]
  choose f hf using hpos
  have hcol : ∀ i j, T i j = if i = f j then 1 else 0 := by
    intro i j
    have hSk := column_eq_single_of_pos hS hT hST (hf j)
    have h := congrFun (congrFun hTS i) (f j)
    rw [mul_apply, Finset.sum_eq_single j
      (fun b _ hb => by rw [hSk b, if_neg hb, mul_zero]) (by simp),
      hSk j, if_pos rfl, mul_one, one_apply] at h
    exact h
  have hinj : Function.Injective f := by
    intro j j' hjj'
    have h1 := column_eq_single_of_pos hS hT hST (hf j) j
    have h2 := column_eq_single_of_pos hS hT hST (hf j') j
    rw [hjj', h2] at h1
    by_contra hne
    rw [if_neg hne, if_pos rfl] at h1
    exact zero_ne_one h1
  let e := Equiv.ofBijective f hinj.bijective_of_finite
  refine ⟨e.symm, ?_⟩
  ext i j
  rw [hcol]
  simp [PEquiv.toMatrix_apply, Equiv.symm_apply_eq, e]

theorem permMatrix_isStochastic (σ : Equiv.Perm ι) :
    IsStochastic (σ.permMatrix ℚ) := by
  refine ⟨fun i j => ?_, fun j => ?_⟩
  · simp only [PEquiv.toMatrix_apply]
    split_ifs <;> norm_num
  · simp [PEquiv.toMatrix_apply, ← Equiv.eq_symm_apply]

/-- `WDP-CH18-P02`. For `W > 0`, an update is reversible within the states of
mass `W` exactly when it is a permutation matrix. -/
theorem reversible_iff_permutation {W : ℚ} (hW : 0 < W) (T : Matrix ι ι ℚ) :
    (PreservesStates W T ∧ ∃ S, PreservesStates W S ∧ S * T = 1) ↔
      ∃ σ : Equiv.Perm ι, T = σ.permMatrix ℚ := by
  constructor
  · rintro ⟨hT, S, hS, hST⟩
    exact perm_of_stochastic_inverse ((preservesStates_iff_stochastic hW S).mp hS)
      ((preservesStates_iff_stochastic hW T).mp hT) hST
  · rintro ⟨σ, rfl⟩
    refine ⟨preservesStates_of_stochastic (permMatrix_isStochastic σ),
      σ⁻¹.permMatrix ℚ, preservesStates_of_stochastic (permMatrix_isStochastic _), ?_⟩
    rw [← permMatrix_mul, mul_inv_cancel, permMatrix_one]

/-- `WDP-CH18-P02`, bundled: for `W > 0`, preserving states of mass `W` is
column-stochasticity, and reversibility within those states is being a
permutation matrix. -/
theorem nonnegative_weights_force_permutations {W : ℚ} (hW : 0 < W) (T : Matrix ι ι ℚ) :
    (PreservesStates W T ↔ IsStochastic T) ∧
      ((PreservesStates W T ∧ ∃ S, PreservesStates W S ∧ S * T = 1) ↔
        ∃ σ : Equiv.Perm ι, T = σ.permMatrix ℚ) :=
  ⟨preservesStates_iff_stochastic hW T, reversible_iff_permutation hW T⟩

/-- A permutation update relabels the weight: `(σ.permMatrix w)_q = w (σ q)`.
Mathlib's `σ.permMatrix` sends `e_q` to `e_{σ⁻¹ q}`, so it is the prose's
`P_{σ⁻¹}`. -/
theorem permutation_update_relabels (σ : Equiv.Perm ι) (w : ι → ℚ) :
    σ.permMatrix ℚ *ᵥ w = w ∘ σ :=
  permMatrix_mulVec σ

/-- The preservation clauses of the permutation isometry of `QuantumImports`,
on every finite carrier: a permutation matrix over `ℤ` preserves the standard
form, the total mass and the `ℓ¹` norm. -/
theorem permutation_isometry_int (σ : Equiv.Perm ι) (u v : ι → ℤ) :
    (σ.permMatrix ℤ *ᵥ u) ⬝ᵥ (σ.permMatrix ℤ *ᵥ v) = u ⬝ᵥ v ∧
      ∑ i, (σ.permMatrix ℤ *ᵥ u) i = ∑ i, u i ∧
      ∑ i, ((σ.permMatrix ℤ *ᵥ u) i).natAbs = ∑ i, (u i).natAbs := by
  simp only [permMatrix_mulVec, dotProduct, Function.comp]
  exact ⟨Equiv.sum_comp σ (fun i => u i * v i), Equiv.sum_comp σ u,
    Equiv.sum_comp σ (fun i => (u i).natAbs)⟩

end Positive

/-! ## `WDP-CH18-P03`: signed weights break the corner -/

section Signed

/-- A mass-preserving shear over `ℚ`. -/
def signedShear : Matrix (Fin 2) (Fin 2) ℚ := !![2, 1; -1, 0]

/-- Its inverse, also mass-preserving. -/
def signedShearInv : Matrix (Fin 2) (Fin 2) ℚ := !![0, -1; 1, 2]

/-- `WDP-CH18-P03`. With signed weights, total mass and invertibility do not
force a permutation: the shear and its inverse both preserve total mass, the
shear is not a permutation matrix, and it sends the basis weight `(1, 0)` to
the signed weight `(2, -1)`. -/
theorem signed_weights_break_the_corner :
    (∀ w : Fin 2 → ℚ, ∑ i, (signedShear *ᵥ w) i = ∑ i, w i) ∧
      (∀ w : Fin 2 → ℚ, ∑ i, (signedShearInv *ᵥ w) i = ∑ i, w i) ∧
      signedShearInv * signedShear = 1 ∧
      (∀ σ : Equiv.Perm (Fin 2), signedShear ≠ σ.permMatrix ℚ) ∧
      signedShear *ᵥ ![1, 0] = ![2, -1] := by
  refine ⟨fun w => ?_, fun w => ?_, ?_, fun σ h => ?_, ?_⟩
  · simp [signedShear, Fin.sum_univ_two, mulVec, dotProduct]
    ring
  · simp [signedShearInv, Fin.sum_univ_two, mulVec, dotProduct]
    ring
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [signedShear, signedShearInv, mul_apply, Fin.sum_univ_two]
  · have h00 := congrFun (congrFun h 0) 0
    simp only [signedShear, PEquiv.toMatrix_apply] at h00
    split_ifs at h00 <;> norm_num at h00
  · ext i
    fin_cases i <;> simp [signedShear, mulVec, dotProduct, Fin.sum_univ_two]

end Signed

/-! ## `WDP-CH18-P04`: unitaries over `ℤ[i]` are monomial -/

section Gaussian

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The phase-blind quadratic readout of Axiom W6 over `ℤ[i]`:
`π(v)_q = N(v_q) = |v_q|²`. -/
def readout (v : ι → GaussianInt) : ι → ℤ :=
  fun q => (v q).norm

theorem star_mul_self_eq_norm (z : GaussianInt) : star z * z = (z.norm : GaussianInt) := by
  rw [Zsqrtd.norm_eq_mul_conj, mul_comm]

theorem gaussian_norm_nonneg (z : GaussianInt) : 0 ≤ z.norm :=
  Zsqrtd.norm_nonneg (by norm_num) z

/-- The units of `ℤ[i]` are exactly `1`, `-1`, `i` and `-i`. -/
theorem gaussian_unit_cases {z : GaussianInt} (hz : IsUnit z) :
    z = 1 ∨ z = -1 ∨ z = ⟨0, 1⟩ ∨ z = ⟨0, -1⟩ := by
  have hn : z.norm = 1 := (Zsqrtd.norm_eq_one_iff' (by norm_num) z).mpr hz
  rw [Zsqrtd.norm_def] at hn
  have hre : -1 ≤ z.re ∧ z.re ≤ 1 := by constructor <;> nlinarith [sq_nonneg z.im]
  have him : -1 ≤ z.im ∧ z.im ≤ 1 := by constructor <;> nlinarith [sq_nonneg z.re]
  obtain ⟨re, im⟩ := z
  simp only at hn hre him ⊢
  obtain ⟨hre1, hre2⟩ := hre
  obtain ⟨him1, him2⟩ := him
  interval_cases re <;> interval_cases im <;> simp_all <;> decide

/-- Each column of a unitary over `ℤ[i]` has exactly one nonzero entry, and
that entry is a unit. -/
theorem unitary_column {U : Matrix ι ι GaussianInt} (hU : Uᴴ * U = 1) (j : ι) :
    ∃ k, IsUnit (U k j) ∧ ∀ i, i ≠ k → U i j = 0 := by
  have h := congrFun (congrFun hU j) j
  rw [mul_apply, one_apply_eq] at h
  simp only [conjTranspose_apply, star_mul_self_eq_norm] at h
  rw [← Int.cast_sum] at h
  have hsum : ∑ k, (U k j).norm = 1 := by exact_mod_cast h
  obtain ⟨k, hk⟩ : ∃ k, (U k j).norm ≠ 0 := by
    by_contra hne
    push Not at hne
    simp [hne] at hsum
  have hsplit := Finset.add_sum_erase Finset.univ (fun i => (U i j).norm) (Finset.mem_univ k)
  rw [hsum] at hsplit
  have hkpos : 0 < (U k j).norm := lt_of_le_of_ne (gaussian_norm_nonneg _) (Ne.symm hk)
  have hrest : 0 ≤ ∑ i ∈ Finset.univ.erase k, (U i j).norm :=
    Finset.sum_nonneg fun i _ => gaussian_norm_nonneg _
  have hzero : ∑ i ∈ Finset.univ.erase k, (U i j).norm = 0 := by omega
  have hone : (U k j).norm = 1 := by omega
  refine ⟨k, (Zsqrtd.norm_eq_one_iff' (by norm_num) _).mp hone, fun i hik => ?_⟩
  have hi := (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => gaussian_norm_nonneg (U i j))).mp
    hzero i (Finset.mem_erase.mpr ⟨hik, Finset.mem_univ i⟩)
  exact (Zsqrtd.norm_eq_zero_iff (by norm_num) _).mp hi

/-- `WDP-CH18-P04`. Every unitary over `ℤ[i]` is monomial: a permutation of
rows with a unit (`±1` or `±i`) in each column. -/
theorem gaussian_unitary_is_monomial {U : Matrix ι ι GaussianInt} (hU : Uᴴ * U = 1) :
    ∃ (σ : Equiv.Perm ι) (u : ι → GaussianInt), (∀ j, IsUnit (u j)) ∧
      ∀ i j, U i j = if i = σ j then u j else 0 := by
  choose f hunit hzero using unitary_column hU
  have hinj : Function.Injective f := by
    intro j j' hjj'
    by_contra hne
    have h := congrFun (congrFun hU j) j'
    rw [mul_apply, one_apply_ne hne,
      Finset.sum_eq_single (f j)
        (fun b _ hb => by simp [conjTranspose_apply, hzero j b hb]) (by simp)] at h
    simp only [conjTranspose_apply] at h
    have hunit' : IsUnit (U (f j) j') := hjj' ▸ hunit j'
    exact ((hunit j).star.mul hunit').ne_zero h
  let σ := Equiv.ofBijective f hinj.bijective_of_finite
  refine ⟨σ, fun j => U (f j) j, hunit, fun i j => ?_⟩
  simp only [σ, Equiv.ofBijective_apply]
  split_ifs with h
  · rw [h]
  · exact hzero j i h

/-- A monomial matrix with unit entries moves the readout by its permutation. -/
theorem readout_of_monomial {U : Matrix ι ι GaussianInt} {σ : Equiv.Perm ι}
    {u : ι → GaussianInt} (hu : ∀ j, IsUnit (u j))
    (hU' : ∀ i j, U i j = if i = σ j then u j else 0) (v : ι → GaussianInt) :
    readout (U *ᵥ v) = readout v ∘ σ.symm := by
  funext i
  have hentry : (U *ᵥ v) i = u (σ.symm i) * v (σ.symm i) := by
    simp only [mulVec, dotProduct, hU']
    rw [Finset.sum_eq_single (σ.symm i)]
    · simp
    · intro b _ hb
      rw [if_neg, zero_mul]
      intro h
      exact hb (by rw [h, Equiv.symm_apply_apply])
    · simp
  have hnorm : (u (σ.symm i)).norm = 1 :=
    (Zsqrtd.norm_eq_one_iff' (by norm_num) _).mpr (hu _)
  simp only [readout, Function.comp, hentry, Zsqrtd.norm_mul, hnorm, one_mul]

/-- A unitary over `ℤ[i]` moves the readout by a permutation. -/
theorem gaussian_unitary_readout {U : Matrix ι ι GaussianInt} (hU : Uᴴ * U = 1) :
    ∃ σ : Equiv.Perm ι, ∀ v, readout (U *ᵥ v) = readout v ∘ σ.symm := by
  obtain ⟨σ, u, hu, hU'⟩ := gaussian_unitary_is_monomial hU
  exact ⟨σ, readout_of_monomial hu hU'⟩

/-- No unitary over `ℤ[i]` separates two vectors with the same readout. -/
theorem gaussian_unitary_preserves_readout_fibres {U : Matrix ι ι GaussianInt}
    (hU : Uᴴ * U = 1) {v v' : ι → GaussianInt} (h : readout v = readout v') :
    readout (U *ᵥ v) = readout (U *ᵥ v') := by
  obtain ⟨σ, hσ⟩ := gaussian_unitary_readout hU
  rw [hσ, hσ, h]

/-- `WDP-CH18-P04`, bundled: a unitary over `ℤ[i]` is monomial with entries
`±1` or `±i` in the rows of one permutation `σ`, it moves the readout by that
same `σ`, and it separates no readout fibre. -/
theorem unitary_package_is_classical {U : Matrix ι ι GaussianInt} (hU : Uᴴ * U = 1) :
    ∃ (σ : Equiv.Perm ι) (u : ι → GaussianInt),
      (∀ j, u j = 1 ∨ u j = -1 ∨ u j = ⟨0, 1⟩ ∨ u j = ⟨0, -1⟩) ∧
      (∀ i j, U i j = if i = σ j then u j else 0) ∧
      (∀ v, readout (U *ᵥ v) = readout v ∘ σ.symm) ∧
      ∀ v v', readout v = readout v' → readout (U *ᵥ v) = readout (U *ᵥ v') := by
  obtain ⟨σ, u, hu, hU'⟩ := gaussian_unitary_is_monomial hU
  refine ⟨σ, u, fun j => gaussian_unit_cases (hu j), hU', readout_of_monomial hu hU',
    fun v v' h => ?_⟩
  rw [readout_of_monomial hu hU', readout_of_monomial hu hU', h]

/-- Along any finite run of unitary updates over `ℤ[i]`, the readout is the
initial readout relabelled by one permutation: the run is a deterministic
reversible classical model on the carrier. -/
theorem gaussian_run_readout (Us : List (Matrix ι ι GaussianInt))
    (hUs : ∀ U ∈ Us, Uᴴ * U = 1) :
    ∃ τ : Equiv.Perm ι, ∀ v, readout (Us.foldr (fun U w => U *ᵥ w) v) = readout v ∘ τ.symm := by
  induction Us with
  | nil => exact ⟨1, fun v => rfl⟩
  | cons U Us ih =>
    obtain ⟨τ, hτ⟩ := ih fun V hV => hUs V (List.mem_cons_of_mem U hV)
    obtain ⟨σ, hσ⟩ := gaussian_unitary_readout (hUs U List.mem_cons_self)
    refine ⟨σ * τ, fun v => ?_⟩
    rw [List.foldr_cons, hσ, hτ]
    rfl

end Gaussian

/-! ## `WDP-CH18-P05`: where the corner ends -/

section Boundary

/-- The unnormalized Hadamard matrix of `H010`, over `ℤ[i]`. -/
def hadamard : Matrix (Fin 2) (Fin 2) GaussianInt := !![1, 1; 1, -1]

theorem hadamard_similitude : hadamardᴴ * hadamard = !![2, 0; 0, 2] := by
  ext i j : 1
  fin_cases i <;> fin_cases j <;>
    simp [hadamard, mul_apply, Fin.sum_univ_two, conjTranspose_apply] <;> decide

theorem hadamard_separates_fibre :
    readout ![(1 : GaussianInt), 1] = readout ![1, -1] ∧
      readout (hadamard *ᵥ ![1, 1]) ≠ readout (hadamard *ᵥ ![1, -1]) := by
  refine ⟨?_, fun h => ?_⟩
  · ext i
    fin_cases i <;> simp [readout]
  · have h0 := congrFun h 0
    simp [readout, hadamard, mulVec, dotProduct, Fin.sum_univ_two] at h0

/-- The Hadamard mixer is not a unitary over `ℤ[i]`: by `WDP-CH18-P04` no
unitary separates a readout fibre, and `hadamard` does. -/
theorem hadamard_not_unitary : hadamardᴴ * hadamard ≠ 1 := fun h =>
  hadamard_separates_fibre.2
    (gaussian_unitary_preserves_readout_fibres h hadamard_separates_fibre.1)

/-- A rational rotation with entries in `ℤ[1/5]`. -/
def pythagoreanRotation : Matrix (Fin 2) (Fin 2) ℚ := !![3/5, -4/5; 4/5, 3/5]

/-- The squared readout over `ℚ`. -/
def squareReadout (v : Fin 2 → ℚ) : Fin 2 → ℚ := fun q => v q ^ 2

/-- Over `ℤ[1/5]` a genuine isometry separates the sign fibre that the
Hadamard similitude separates over `ℤ`. -/
theorem pythagorean_rotation_separates_fibre :
    pythagoreanRotationᵀ * pythagoreanRotation = 1 ∧
      (∀ i j, ∃ a : ℤ, pythagoreanRotation i j = a / 5) ∧
      squareReadout ![1, 1] = squareReadout ![1, -1] ∧
      squareReadout (pythagoreanRotation *ᵥ ![1, 1]) = ![1/25, 49/25] ∧
      squareReadout (pythagoreanRotation *ᵥ ![1, -1]) = ![49/25, 1/25] := by
  refine ⟨?_, fun i j => ?_, ?_, ?_, ?_⟩
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [pythagoreanRotation, mul_apply, Fin.sum_univ_two] <;> norm_num
  · fin_cases i <;> fin_cases j
    · exact ⟨3, by simp [pythagoreanRotation]⟩
    · exact ⟨-4, by simp [pythagoreanRotation]⟩
    · exact ⟨4, by simp [pythagoreanRotation]⟩
    · exact ⟨3, by simp [pythagoreanRotation]⟩
  · ext i
    fin_cases i <;> simp [squareReadout]
  · ext i
    fin_cases i <;>
      simp [squareReadout, pythagoreanRotation, mulVec, dotProduct, Fin.sum_univ_two] <;> norm_num
  · ext i
    fin_cases i <;>
      simp [squareReadout, pythagoreanRotation, mulVec, dotProduct, Fin.sum_univ_two] <;> norm_num

/-- The Gaussian rationals `ℚ(i)`, as `ℚ[ω]` with `ω² = -1`. -/
abbrev GaussRat := QuadraticAlgebra ℚ (-1) 0

/-- The readout `|z|² = re² + im²` over `ℚ(i)`. -/
def gaussRatReadout (v : Fin 2 → GaussRat) : Fin 2 → ℚ :=
  fun q => (v q).re ^ 2 + (v q).im ^ 2

/-- `½ !![1+i, 1-i; 1-i, 1+i]`. -/
def halfMixer : Matrix (Fin 2) (Fin 2) GaussRat :=
  !![⟨1/2, 1/2⟩, ⟨1/2, -1/2⟩; ⟨1/2, -1/2⟩, ⟨1/2, 1/2⟩]

/-- Over `ℤ[i][1/2]` a unitary separates the phase fibre of `(1, 1)` and
`(1, i)`. It is also a unitary square root of the toggle `!![0, 1; 1, 0]`,
which has no square root among report permutations (`import7_unforced`). -/
theorem half_mixer_separates_fibre :
    halfMixerᴴ * halfMixer = 1 ∧
      halfMixer * halfMixer = !![0, 1; 1, 0] ∧
      (∀ i j, ∃ a b : ℤ, halfMixer i j = ⟨a / 2, b / 2⟩) ∧
      gaussRatReadout ![1, 1] = gaussRatReadout ![1, ⟨0, 1⟩] ∧
      gaussRatReadout (halfMixer *ᵥ ![1, 1]) = ![1, 1] ∧
      gaussRatReadout (halfMixer *ᵥ ![1, ⟨0, 1⟩]) = ![2, 0] := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext i j : 1
    fin_cases i <;> fin_cases j <;>
      ext <;> simp [halfMixer, mul_apply, Fin.sum_univ_two, conjTranspose_apply,
        QuadraticAlgebra.re_one, QuadraticAlgebra.im_one] <;> norm_num
  · ext i j : 1
    fin_cases i <;> fin_cases j <;>
      ext <;> simp [halfMixer, mul_apply, Fin.sum_univ_two,
        QuadraticAlgebra.re_one, QuadraticAlgebra.im_one] <;> norm_num
  · intro i j
    fin_cases i <;> fin_cases j
    · exact ⟨1, 1, by simp [halfMixer]⟩
    · exact ⟨1, -1, by simp [halfMixer]⟩
    · exact ⟨1, -1, by simp [halfMixer]⟩
    · exact ⟨1, 1, by simp [halfMixer]⟩
  · ext i
    fin_cases i <;> simp [gaussRatReadout, QuadraticAlgebra.re_one, QuadraticAlgebra.im_one]
  · ext i
    fin_cases i <;>
      simp [gaussRatReadout, halfMixer, mulVec, dotProduct, Fin.sum_univ_two] <;> norm_num
  · ext i
    fin_cases i <;>
      simp [gaussRatReadout, halfMixer, mulVec, dotProduct, Fin.sum_univ_two] <;> norm_num

/-- `WDP-CH18-P05`, bundled: the Hadamard mixer is a similitude that separates a
readout fibre and is not a unitary over `ℤ[i]`, while unitaries over
`ℤ[1/5]` and `ℤ[i][1/2]` separate readout fibres; the second is also a unitary
square root of the toggle. -/
theorem classical_corner_ends :
    hadamardᴴ * hadamard = !![2, 0; 0, 2] ∧
      (readout ![(1 : GaussianInt), 1] = readout ![1, -1] ∧
        readout (hadamard *ᵥ ![1, 1]) ≠ readout (hadamard *ᵥ ![1, -1])) ∧
      hadamardᴴ * hadamard ≠ 1 ∧
      (pythagoreanRotationᵀ * pythagoreanRotation = 1 ∧
        (∀ i j, ∃ a : ℤ, pythagoreanRotation i j = a / 5) ∧
        squareReadout ![1, 1] = squareReadout ![1, -1] ∧
        squareReadout (pythagoreanRotation *ᵥ ![1, 1]) = ![1/25, 49/25] ∧
        squareReadout (pythagoreanRotation *ᵥ ![1, -1]) = ![49/25, 1/25]) ∧
      (halfMixerᴴ * halfMixer = 1 ∧
        halfMixer * halfMixer = !![0, 1; 1, 0] ∧
        (∀ i j, ∃ a b : ℤ, halfMixer i j = ⟨a / 2, b / 2⟩) ∧
        gaussRatReadout ![1, 1] = gaussRatReadout ![1, ⟨0, 1⟩] ∧
        gaussRatReadout (halfMixer *ᵥ ![1, 1]) = ![1, 1] ∧
        gaussRatReadout (halfMixer *ᵥ ![1, ⟨0, 1⟩]) = ![2, 0]) :=
  ⟨hadamard_similitude, hadamard_separates_fibre, hadamard_not_unitary,
    pythagorean_rotation_separates_fibre, half_mixer_separates_fibre⟩

end Boundary

end WitnessedDifference.ClassicalCorner
