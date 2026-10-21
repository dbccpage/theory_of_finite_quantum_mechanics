import Mathlib.Basic.Real.Pointwise
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Algebra.Order.Archimedean.Basic
import Mathlib.Algebra.Order.BigOperators.Group.List
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

/-!
# Noisy unitary steps without fresh resources lose the input

Origin: dag/research/quantum_computation_self_obstruction.md (QCV-Q4)
Claim, general dimension (trace norm over `ℂ`): for the global depolarizing channel
`Δ_p ρ = (1 - p) ρ + p (tr ρ / d) 1` and two matrices of equal trace,
`‖Δ_p ρ - Δ_p σ‖₁ = (1 - p) ‖ρ - σ‖₁`.  Interleaved with arbitrary unitaries `V_i` and rates
`p_i ∈ [0, 1]`, a noisy history of length `t` satisfies
`‖ρ_t - σ_t‖₁ = (∏ (1 - p_i)) ‖ρ_0 - σ_0‖₁ ≤ (1 - p)^t ‖ρ_0 - σ_0‖₁` when every `p_i ≥ p`.
The trace norm is the variational norm `sup_U |tr (U X)|` over unitaries `U` (a definition here;
its equality with the sum of singular values is the cited standard fact, not re-derived).
Claim, qubit (`d = 2`, rational Bloch vectors): `Δ_p` scales the Bloch vector by `1 - p`, a unitary
acts by a rational rotation, and the squared Bloch distance of two histories contracts by
`∏ (1 - p_i)^2`; for the difference of two Bloch matrices `Z`, `Z² = (|r - s|² / 4) 1`.
AuthorityEffect: None
Scope Fence: the noise model is a *global* depolarizing channel after every step with rate at
least `p`, a declared input.  It is not a model of independent per-qubit noise, and it is not a
statement about any device.  The Aharonov-Ben-Or-Impagliazzo-Nisan (1996) theorem on noisy
reversible computation is cited as context, not imported as proof.
-/

open Matrix Pointwise

namespace QcSelfObstruction

section General

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The set of values `‖tr (U X)‖` over unitary `U`. -/
def pairingSet (X : Matrix n n ℂ) : Set ℝ :=
  {x | ∃ U ∈ Matrix.unitaryGroup n ℂ, x = ‖(U * X).trace‖}

/-- Trace norm of a complex matrix, as the variational maximum `sup_U |tr (U X)|` (definition). -/
noncomputable def tn (X : Matrix n n ℂ) : ℝ := sSup (pairingSet X)

theorem pairingSet_bddAbove (X : Matrix n n ℂ) : BddAbove (pairingSet X) := by
  refine ⟨∑ i, ∑ j, ‖X j i‖, ?_⟩
  rintro x ⟨U, hU, rfl⟩
  have hb : ∀ i j, ‖U i j‖ ≤ 1 := fun i j => entry_norm_bound_of_unitary hU i j
  calc ‖(U * X).trace‖ = ‖∑ i, ∑ j, U i j * X j i‖ := by
        simp [Matrix.trace, Matrix.mul_apply]
    _ ≤ ∑ i, ‖∑ j, U i j * X j i‖ := norm_sum_le _ _
    _ ≤ ∑ i, ∑ j, ‖U i j * X j i‖ := Finset.sum_le_sum (fun i _ => norm_sum_le _ _)
    _ ≤ ∑ i, ∑ j, ‖X j i‖ := by
        refine Finset.sum_le_sum (fun i _ => Finset.sum_le_sum (fun j _ => ?_))
        rw [norm_mul]
        calc ‖U i j‖ * ‖X j i‖ ≤ 1 * ‖X j i‖ :=
              mul_le_mul_of_nonneg_right (hb i j) (norm_nonneg _)
          _ = ‖X j i‖ := one_mul _

theorem tn_nonneg [Nonempty n] (X : Matrix n n ℂ) : 0 ≤ tn X := by
  apply Real.sSup_nonneg
  rintro x ⟨U, _, rfl⟩
  exact norm_nonneg _

/-- Sanity: the trace norm of the zero matrix is zero. -/
theorem tn_zero : tn (0 : Matrix n n ℂ) = 0 := by
  unfold tn pairingSet
  have : {x : ℝ | ∃ U ∈ Matrix.unitaryGroup n ℂ, x = ‖(U * (0 : Matrix n n ℂ)).trace‖} = {0} := by
    ext x
    simp only [Set.mem_ofPred_eq, Set.mem_singleton_iff, Matrix.mul_zero, Matrix.trace_zero,
      norm_zero]
    exact ⟨fun ⟨_, _, h⟩ => h, fun h => ⟨1, Submonoid.one_mem _, h⟩⟩
  rw [this, csSup_singleton]

/-- Homogeneity for nonnegative real scalars. -/
theorem tn_smul {a : ℝ} (ha : 0 ≤ a) (X : Matrix n n ℂ) : tn ((a : ℂ) • X) = a * tn X := by
  unfold tn
  have h : pairingSet ((a : ℂ) • X) = a • pairingSet X := by
    ext x
    simp only [pairingSet, Set.mem_ofPred_eq, Set.mem_smul_set, smul_eq_mul]
    constructor
    · rintro ⟨U, hU, rfl⟩
      refine ⟨‖(U * X).trace‖, ⟨U, hU, rfl⟩, ?_⟩
      rw [Matrix.mul_smul, Matrix.trace_smul, norm_smul, Complex.norm_real, Real.norm_of_nonneg ha]
    · rintro ⟨y, ⟨U, hU, rfl⟩, rfl⟩
      refine ⟨U, hU, ?_⟩
      rw [Matrix.mul_smul, Matrix.trace_smul, norm_smul, Complex.norm_real, Real.norm_of_nonneg ha]
  rw [h, Real.sSup_smul_of_nonneg ha]
  rfl

/-- Unitary invariance: `tn (V X V†) = tn X`. -/
theorem tn_conj {V : Matrix n n ℂ} (hV : V ∈ Matrix.unitaryGroup n ℂ) (X : Matrix n n ℂ) :
    tn (V * X * star V) = tn X := by
  unfold tn
  have hV' := Unitary.mem_iff.1 hV
  have key : ∀ U : Matrix n n ℂ, (U * (V * X * star V)).trace = ((star V * U * V) * X).trace := by
    intro U
    calc (U * (V * X * star V)).trace = (star V * (U * (V * X))).trace := by
          rw [← Matrix.mul_assoc, ← Matrix.mul_assoc, Matrix.trace_mul_comm (U * V * X)]
      _ = ((star V * U * V) * X).trace := by simp [Matrix.mul_assoc]
  have h : pairingSet (V * X * star V) = pairingSet X := by
    ext x
    simp only [pairingSet, Set.mem_ofPred_eq]
    constructor
    · rintro ⟨U, hU, rfl⟩
      refine ⟨star V * U * V, ?_, by rw [key]⟩
      exact Submonoid.mul_mem _ (Submonoid.mul_mem _ (Unitary.star_mem hV) hU) hV
    · rintro ⟨W, hW, rfl⟩
      refine ⟨V * W * star V, ?_, ?_⟩
      · exact Submonoid.mul_mem _ (Submonoid.mul_mem _ hV hW) (Unitary.star_mem hV)
      · rw [key]
        have : star V * (V * W * star V) * V = W := by
          calc star V * (V * W * star V) * V = (star V * V) * W * (star V * V) := by
                simp only [Matrix.mul_assoc]
            _ = W := by rw [hV'.1]; simp
        rw [this]
  rw [h]

/-- Global depolarizing channel `Δ_p ρ = (1 - p) ρ + p (tr ρ / d) 1`. -/
noncomputable def depol (p : ℝ) (ρ : Matrix n n ℂ) : Matrix n n ℂ :=
  ((1 - p : ℝ) : ℂ) • ρ + ((p : ℂ) * ρ.trace / (Fintype.card n : ℂ)) • (1 : Matrix n n ℂ)

/-- One noisy computational step: a unitary followed by global depolarizing noise. -/
noncomputable def noisyStep (p : ℝ) (V : Matrix n n ℂ) (ρ : Matrix n n ℂ) : Matrix n n ℂ :=
  depol p (V * ρ * star V)

theorem trace_conj {V : Matrix n n ℂ} (hV : V ∈ Matrix.unitaryGroup n ℂ) (X : Matrix n n ℂ) :
    (V * X * star V).trace = X.trace := by
  have hV' := Unitary.mem_iff.1 hV
  calc (V * X * star V).trace = (star V * (V * X)).trace := by
        rw [Matrix.trace_mul_comm]
    _ = X.trace := by rw [← Matrix.mul_assoc, hV'.1, Matrix.one_mul]

theorem trace_depol [Nonempty n] (p : ℝ) (ρ : Matrix n n ℂ) : (depol p ρ).trace = ρ.trace := by
  unfold depol
  have hd : (Fintype.card n : ℂ) ≠ 0 := by
    exact_mod_cast Fintype.card_ne_zero
  rw [Matrix.trace_add, Matrix.trace_smul, Matrix.trace_smul, Matrix.trace_one]
  simp only [smul_eq_mul, Complex.ofReal_sub, Complex.ofReal_one]
  field_simp
  ring

theorem trace_noisyStep [Nonempty n] {V : Matrix n n ℂ} (hV : V ∈ Matrix.unitaryGroup n ℂ) (p : ℝ)
    (ρ : Matrix n n ℂ) : (noisyStep p V ρ).trace = ρ.trace := by
  unfold noisyStep
  rw [trace_depol, trace_conj hV]

/-- Q4, one step: `Δ_p` contracts the trace distance of equal-trace inputs by exactly `1 - p`. -/
theorem depol_dist [Nonempty n] {p : ℝ} (hp : p ≤ 1) {ρ σ : Matrix n n ℂ}
    (htr : ρ.trace = σ.trace) : tn (depol p ρ - depol p σ) = (1 - p) * tn (ρ - σ) := by
  have h : depol p ρ - depol p σ = ((1 - p : ℝ) : ℂ) • (ρ - σ) := by
    unfold depol
    rw [htr, smul_sub]
    abel
  rw [h, tn_smul (by linarith)]

/-- One noisy step (any unitary) contracts the trace distance of equal-trace inputs by exactly
`1 - p`. -/
theorem noisyStep_dist [Nonempty n] {p : ℝ} (hp : p ≤ 1) {V : Matrix n n ℂ}
    (hV : V ∈ Matrix.unitaryGroup n ℂ) {ρ σ : Matrix n n ℂ} (htr : ρ.trace = σ.trace) :
    tn (noisyStep p V ρ - noisyStep p V σ) = (1 - p) * tn (ρ - σ) := by
  unfold noisyStep
  rw [depol_dist hp (by rw [trace_conj hV, trace_conj hV, htr])]
  congr 1
  have : V * ρ * star V - V * σ * star V = V * (ρ - σ) * star V := by
    rw [Matrix.mul_sub, Matrix.sub_mul]
  rw [this, tn_conj hV]

/-- A noisy history: a list of (noise rate, unitary) steps applied left to right. -/
noncomputable def run : List (ℝ × Matrix n n ℂ) → Matrix n n ℂ → Matrix n n ℂ
  | [], ρ => ρ
  | (p, V) :: L, ρ => run L (noisyStep p V ρ)

/-- Every step is a unitary with a rate in `[0, 1]`. -/
def Admissible (L : List (ℝ × Matrix n n ℂ)) : Prop :=
  ∀ s ∈ L, 0 ≤ s.1 ∧ s.1 ≤ 1 ∧ s.2 ∈ Matrix.unitaryGroup n ℂ

theorem trace_run [Nonempty n] (L : List (ℝ × Matrix n n ℂ)) (hL : Admissible L)
    (ρ : Matrix n n ℂ) : (run L ρ).trace = ρ.trace := by
  induction L generalizing ρ with
  | nil => rfl
  | cons s L ih =>
    obtain ⟨p, V⟩ := s
    have hs := hL (p, V) (List.mem_cons_self)
    have hL' : Admissible L := fun t ht => hL t (List.mem_cons_of_mem _ ht)
    simp only [run]
    rw [ih hL', trace_noisyStep hs.2.2]

/-- Q4 (exact, general dimension): along any noisy history the trace distance of two computations
that start with equal trace is multiplied by exactly `∏ (1 - p_i)`. -/
theorem run_dist [Nonempty n] (L : List (ℝ × Matrix n n ℂ)) (hL : Admissible L)
    {ρ σ : Matrix n n ℂ} (htr : ρ.trace = σ.trace) :
    tn (run L ρ - run L σ) = (L.map (fun s => 1 - s.1)).prod * tn (ρ - σ) := by
  induction L generalizing ρ σ with
  | nil => simp [run]
  | cons s L ih =>
    obtain ⟨p, V⟩ := s
    have hs := hL (p, V) (List.mem_cons_self)
    have hL' : Admissible L := fun t ht => hL t (List.mem_cons_of_mem _ ht)
    simp only [run, List.map_cons, List.prod_cons]
    rw [ih hL' (by rw [trace_noisyStep hs.2.2, trace_noisyStep hs.2.2, htr]),
      noisyStep_dist hs.2.1 hs.2.2 htr]
    ring

/-- Decay bound: if every step has rate at least `p` (and at most one), after `t` steps the trace
distance is at most `(1 - p)^t` times its initial value. -/
theorem run_dist_le [Nonempty n] {p : ℝ} (hp1 : p ≤ 1)
    (L : List (ℝ × Matrix n n ℂ)) (hL : Admissible L) (hrate : ∀ s ∈ L, p ≤ s.1)
    {ρ σ : Matrix n n ℂ} (htr : ρ.trace = σ.trace) :
    tn (run L ρ - run L σ) ≤ (1 - p) ^ L.length * tn (ρ - σ) := by
  rw [run_dist L hL htr]
  apply mul_le_mul_of_nonneg_right _ (tn_nonneg _)
  clear htr
  induction L with
  | nil => simp
  | cons s L ih =>
    have hs := hL s (List.mem_cons_self)
    have hL' : Admissible L := fun t ht => hL t (List.mem_cons_of_mem _ ht)
    have hr' : ∀ t ∈ L, p ≤ t.1 := fun t ht => hrate t (List.mem_cons_of_mem _ ht)
    simp only [List.map_cons, List.prod_cons, List.length_cons, pow_succ]
    have h1 := ih hL' hr'
    have h2 : 1 - s.1 ≤ 1 - p := by linarith [hrate s List.mem_cons_self]
    have h3 : 0 ≤ 1 - s.1 := by linarith [hs.2.1]
    have h4 : 0 ≤ (L.map (fun s => 1 - s.1)).prod := by
      apply List.prod_nonneg
      intro x hx
      obtain ⟨t, ht, rfl⟩ := List.mem_map.1 hx
      have := hL t (List.mem_cons_of_mem _ ht)
      linarith [this.2.1]
    nlinarith [pow_nonneg (sub_nonneg.2 hp1) L.length]

end General

/-- Rational form of the decay: `(1 - p)^t ≤ 1 / (1 + p t)` for `0 ≤ p ≤ 1`, so a depth
`t ≥ (1 / δ - 1) / p` noisy computation retains at most a fraction `δ` of the initial distance. -/
theorem decay_le_inv (p : ℚ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1) (t : ℕ) :
    (1 - p) ^ t ≤ 1 / (1 + p * t) := by
  have h1 : 1 + p * t ≤ (1 + p) ^ t := by
    have := one_add_mul_le_pow (a := p) (by linarith) t
    linarith
  have h2 : (1 - p) ^ t * (1 + p) ^ t ≤ 1 := by
    rw [← mul_pow]
    have : (1 - p) * (1 + p) ≤ 1 := by nlinarith
    exact pow_le_one₀ (by nlinarith) this
  have hpos : 0 < 1 + p * t := by positivity
  rw [le_div_iff₀ hpos]
  have h0 : 0 ≤ (1 - p) ^ t := pow_nonneg (by linarith) t
  calc (1 - p) ^ t * (1 + p * t) ≤ (1 - p) ^ t * (1 + p) ^ t := mul_le_mul_of_nonneg_left h1 h0
    _ ≤ 1 := h2

theorem decay_below {p δ : ℚ} (hp0 : 0 < p) (hp1 : p ≤ 1) (hδ : 0 < δ) {t : ℕ}
    (ht : (1 / δ - 1) / p ≤ t) : (1 - p) ^ t ≤ δ := by
  refine le_trans (decay_le_inv p hp0.le hp1 t) ?_
  have h1 : 1 / δ - 1 ≤ p * t := by
    rwa [div_le_iff₀ hp0, mul_comm] at ht
  rw [div_le_iff₀ (by positivity)]
  have : 1 ≤ δ * (1 + p * t) := by
    have h2 : 1 / δ ≤ 1 + p * t := by linarith
    rwa [div_le_iff₀ hδ, mul_comm] at h2
  linarith

/-! ## Qubit case: exact rational Bloch vectors -/

/-- Bloch vectors with rational coordinates. -/
abbrev Bloch := Fin 3 → ℚ

/-- Depolarizing channel on the Bloch vector: `r ↦ (1 - p) r`. -/
def depolB (p : ℚ) (r : Bloch) : Bloch := (1 - p) • r

/-- A rational rotation (`Rᵀ R = 1`) as the action of a qubit unitary on Bloch vectors. -/
structure RatRot where
  R : Matrix (Fin 3) (Fin 3) ℚ
  orth : R.transpose * R = 1

/-- Squared Bloch distance (squared qubit trace distance, see `blochMat_sq`). -/
def sqDist (r s : Bloch) : ℚ := (r - s) ⬝ᵥ (r - s)

theorem sqDist_nonneg (r s : Bloch) : 0 ≤ sqDist r s := by
  unfold sqDist
  simp only [dotProduct, Fin.sum_univ_three, Pi.sub_apply]
  nlinarith [mul_self_nonneg (r 0 - s 0), mul_self_nonneg (r 1 - s 1), mul_self_nonneg (r 2 - s 2)]

theorem rot_dot (Q : RatRot) (v : Bloch) : (Q.R *ᵥ v) ⬝ᵥ (Q.R *ᵥ v) = v ⬝ᵥ v := by
  have h1 : (Q.R *ᵥ v) = v ᵥ* Q.R.transpose := (Matrix.vecMul_transpose Q.R v).symm
  calc (Q.R *ᵥ v) ⬝ᵥ (Q.R *ᵥ v) = (v ᵥ* Q.R.transpose) ⬝ᵥ (Q.R *ᵥ v) := by rw [← h1]
    _ = v ⬝ᵥ (Q.R.transpose *ᵥ (Q.R *ᵥ v)) := (Matrix.dotProduct_mulVec _ _ _).symm
    _ = v ⬝ᵥ v := by rw [Matrix.mulVec_mulVec, Q.orth, Matrix.one_mulVec]

/-- One qubit step: rotate, then depolarize. -/
def stepB (p : ℚ) (Q : RatRot) (r : Bloch) : Bloch := depolB p (Q.R *ᵥ r)

theorem sqDist_stepB (p : ℚ) (Q : RatRot) (r s : Bloch) :
    sqDist (stepB p Q r) (stepB p Q s) = (1 - p) ^ 2 * sqDist r s := by
  unfold sqDist stepB depolB
  have h : (1 - p) • (Q.R *ᵥ r) - (1 - p) • (Q.R *ᵥ s) = (1 - p) • (Q.R *ᵥ (r - s)) := by
    rw [Matrix.mulVec_sub, smul_sub]
  rw [h, smul_dotProduct, dotProduct_smul, rot_dot]
  simp only [smul_eq_mul]
  ring

/-- A noisy qubit history. -/
def runB : List (ℚ × RatRot) → Bloch → Bloch
  | [], r => r
  | (p, Q) :: L, r => runB L (stepB p Q r)

/-- Q4 (exact, qubit, rational): the squared Bloch distance of two histories is multiplied by
`∏ (1 - p_i)^2`. -/
theorem sqDist_runB (L : List (ℚ × RatRot)) (r s : Bloch) :
    sqDist (runB L r) (runB L s) = (L.map (fun x => (1 - x.1) ^ 2)).prod * sqDist r s := by
  induction L generalizing r s with
  | nil => simp [runB]
  | cons x L ih =>
    obtain ⟨p, Q⟩ := x
    simp only [runB, List.map_cons, List.prod_cons]
    rw [ih, sqDist_stepB]
    ring

/-- Qubit decay bound: with every rate in `[p, 1]`, after `t` steps
`sqDist ≤ ((1 - p)^2)^t · sqDist`; distance itself is `(1 - p)^t` times the initial distance. -/
theorem sqDist_runB_le {p : ℚ} (L : List (ℚ × RatRot))
    (hrate : ∀ x ∈ L, p ≤ x.1 ∧ x.1 ≤ 1) (r s : Bloch) :
    sqDist (runB L r) (runB L s) ≤ ((1 - p) ^ 2) ^ L.length * sqDist r s := by
  rw [sqDist_runB]
  apply mul_le_mul_of_nonneg_right _ (sqDist_nonneg r s)
  induction L with
  | nil => simp
  | cons x L ih =>
    have hx := hrate x List.mem_cons_self
    have hr' : ∀ y ∈ L, p ≤ y.1 ∧ y.1 ≤ 1 := fun y hy => hrate y (List.mem_cons_of_mem _ hy)
    simp only [List.map_cons, List.prod_cons, List.length_cons]
    rw [pow_succ ((1 - p) ^ 2) L.length]
    have h1 := ih hr'
    have h2 : (1 - x.1) ^ 2 ≤ (1 - p) ^ 2 := by
      apply pow_le_pow_left₀ (by linarith [hx.2]) (by linarith [hx.1])
    have h4 : 0 ≤ (L.map (fun x => (1 - x.1) ^ 2)).prod := by
      apply List.prod_nonneg
      intro y hy
      obtain ⟨t, _, rfl⟩ := List.mem_map.1 hy
      positivity
    nlinarith [pow_nonneg (sq_nonneg (1 - p)) L.length]

/-- The Pauli part `v · σ` of a Bloch vector, as a complex `2 × 2` matrix. -/
noncomputable def blochMat (v : Bloch) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![(v 2 : ℂ), (v 0 : ℂ) - Complex.I * (v 1 : ℂ); (v 0 : ℂ) + Complex.I * (v 1 : ℂ), -(v 2 : ℂ)]

/-- `(v · σ)² = |v|² 1`: a difference of two qubit states `ρ(r) - ρ(s) = (r - s) · σ / 2` has
both singular values equal to `|r - s| / 2`, so its trace norm is `|r - s|` (the last step is the
cited eigenvalue fact for a Hermitian matrix). -/
theorem blochMat_sq (v : Bloch) : blochMat v * blochMat v = ((v ⬝ᵥ v : ℚ) : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [blochMat, Matrix.mul_apply, Fin.sum_univ_two, dotProduct, Fin.sum_univ_three,
      Complex.ext_iff] <;> ring_nf <;> simp

end QcSelfObstruction
