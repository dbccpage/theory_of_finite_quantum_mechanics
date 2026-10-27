import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Analysis.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# FermionSignQcdChemicalPotentialDet (`FSP-QCD-CHEMICAL-POTENTIAL-DET` / `TFQ-1201`)

Formalizes the finite-dimensional linear-algebraic core of **FSP-DERIV-037**
(`FSP-QCD-CHEMICAL-POTENTIAL-DET`, record `TFQ-1201`):

1. **General $\gamma_5$-Chemical-Potential Intertwining & Determinant Conjugation Law**:
   For any involutive matrix $\Gamma_5 \in M_n(\mathbb{C})$ ($\Gamma_5^2 = I_n$) and any family of
   matrices $D : \mathbb{C} \to M_n(\mathbb{C})$ satisfying the chemical-potential $\gamma_5$-hermiticity
   relation
   $$\Gamma_5 D(\mu) \Gamma_5 = D(-\mu^*)^\dagger,$$
   the determinant obeys the exact complex conjugation law
   $$\bigl(\det D(\mu)\bigr)^* = \det D(-\mu^*).$$
   - At real chemical potential $\mu \in \mathbb{R}$ ($\mu^* = \mu$), this yields
     $\bigl(\det D(\mu)\bigr)^* = \det D(-\mu)$, so $\det D(\mu) \in \mathbb{R}$ holds if and only if
     $\det D(\mu) = \det D(-\mu)$.
   - At $\mu = 0$ or purely imaginary chemical potential $\mu = i \mu_I$ ($\mu_I \in \mathbb{R}$),
     $-\mu^* = \mu$, forcing $\operatorname{Im}\det D(\mu) = 0$.

2. **Hasenfratz–Karsch Exponential Chemical-Potential Structure & Staggered Fermions**:
   For a lattice Dirac operator decomposed into $\mu$-independent mass/spatial hopping $M_0$,
   forward temporal hopping $K_+$, and backward temporal hopping $K_-$ weighted by a
   chemical-potential fugacity map $\exp(\pm \mu)$ satisfying Schwarz reflection
   $\overline{\exp(z)} = \exp(\bar z)$,
   $$D(\mu) = M_0 + \exp(\mu)\, K_+ + \exp(-\mu)\, K_-,$$
   if $\Gamma_5 M_0 \Gamma_5 = M_0^\dagger$, $\Gamma_5 K_+ \Gamma_5 = K_-^\dagger$, and
   $\Gamma_5 K_- \Gamma_5 = K_+^\dagger$ (which holds in particular for Kogut–Susskind staggered
   fermions where $\Gamma_5 = \varepsilon$ is the site-parity involution, $M_0 = m I$,
   $K_- = -K_+^\dagger$, and $\varepsilon K_+ \varepsilon = -K_+$), then
   $$\Gamma_5 D(\mu) \Gamma_5 = D(-\mu^*)^\dagger \quad\text{and}\quad
     \bigl(\det D(\mu)\bigr)^* = \det D(-\mu^*).$$

3. **Explicit $SU(3)$ Link Witness & Strict Complex Determinant at Real $\mu \neq 0$**:
   Because the fundamental representation $\mathbf{3}$ of $SU(3)$ is complex ($\mathbf{3} \not\simeq \bar{\mathbf{3}}$),
   $SU(3)$ contains elements with nonreal trace. We exhibit the explicit diagonal $SU(3)$ clock link
   $$U_{\text{SU3}} = \operatorname{diag}(i, i, -1) \in SU(3), \qquad
     U_{\text{SU3}} U_{\text{SU3}}^\dagger = I_3, \qquad
     \det U_{\text{SU3}} = 1, \qquad
     \operatorname{Tr}(U_{\text{SU3}}) = -1 + 2i,$$
   and the $6 \times 6$ chiral two-time-slice / $\gamma_0$-diagonal Dirac operator at fugacity $z = e^\mu$:
   $$D_{\text{SU3}}(z) = \begin{pmatrix} I_3 - z U_{\text{SU3}} & 0 \\ 0 & I_3 - z^{-1} U_{\text{SU3}}^\dagger \end{pmatrix}.$$
   We prove that $\Gamma_5 = \begin{pmatrix} 0 & I_3 \\ I_3 & 0 \end{pmatrix}$ intertwines
   $D_{\text{SU3}}(z)$ with $D_{\text{SU3}}((z^*)^{-1})^\dagger$, and that at real positive fugacity
   $z = 2$ ($\mu = \ln 2 > 0$) and its inverse $z = 1/2$ ($-\mu = -\ln 2 < 0$),
   $$\det D_{\text{SU3}}(2) = \frac{63}{8} - 27 i, \qquad
     \det D_{\text{SU3}}(1/2) = \frac{63}{8} + 27 i = \bigl(\det D_{\text{SU3}}(2)\bigr)^*,$$
   with $\operatorname{Im}\det D_{\text{SU3}}(2) = -27 \neq 0$ and
   $\det D_{\text{SU3}}(2) \neq \det D_{\text{SU3}}(1/2)$.
   By contrast, for any diagonal $SU(2)$ link $\operatorname{diag}(u, u^*)$ with $|u|^2 = 1$ and
   any real fugacity $r \in \mathbb{R}$, $\operatorname{Im}\det(I_2 - r\,\operatorname{diag}(u, u^*)) = 0$.
-/

namespace FermionSignQcdChemicalPotentialDet

open Matrix Complex

noncomputable section

/-! ## Part I: General $\gamma_5$-Chemical-Potential Intertwining & Determinant Conjugation -/

/-- Conjugating any square matrix `M` by an involution `Γ5` (`Γ5 * Γ5 = 1`) preserves `det`. -/
theorem det_conj_by_involution {n : Type*} [Fintype n] [DecidableEq n]
    {R : Type*} [CommRing R] (Γ5 M : Matrix n n R) (hΓ : Γ5 * Γ5 = 1) :
    (Γ5 * M * Γ5).det = M.det := by
  calc
    (Γ5 * M * Γ5).det = Γ5.det * M.det * Γ5.det := by
      rw [det_mul, det_mul]
    _ = (Γ5.det * Γ5.det) * M.det := by ring
    _ = (Γ5 * Γ5).det * M.det := by rw [← det_mul]
    _ = M.det := by rw [hΓ, det_one, one_mul]

/-- **General $\gamma_5$-Chemical-Potential Determinant Conjugation Identity**:
If `Γ5 * Γ5 = 1` and `Γ5 * D μ * Γ5 = (D (-star μ))ᴴ`, then
`star (D μ).det = (D (-star μ)).det`. -/
theorem gamma5_mu_intertwine_det_conj {n : Type*} [Fintype n] [DecidableEq n]
    (Γ5 : Matrix n n ℂ) (D : ℂ → Matrix n n ℂ) (μ : ℂ)
    (hΓ : Γ5 * Γ5 = 1)
    (h_int : Γ5 * D μ * Γ5 = (D (-star μ))ᴴ) :
    star (D μ).det = (D (-star μ)).det := by
  have h1 : (Γ5 * D μ * Γ5).det = ((D (-star μ))ᴴ).det := congrArg Matrix.det h_int
  rw [det_conj_by_involution Γ5 (D μ) hΓ, det_conjTranspose] at h1
  have h2 := congrArg star h1
  simpa only [star_star] using h2

/-- Specialization to real chemical potential `μ : ℝ`:
`star (D (μ : ℂ)).det = (D (-(μ : ℂ))).det`. -/
theorem gamma5_real_mu_det_conj {n : Type*} [Fintype n] [DecidableEq n]
    (Γ5 : Matrix n n ℂ) (D : ℂ → Matrix n n ℂ) (μ : ℝ)
    (hΓ : Γ5 * Γ5 = 1)
    (h_int : ∀ z : ℂ, Γ5 * D z * Γ5 = (D (-star z))ᴴ) :
    star (D (μ : ℂ)).det = (D (-(μ : ℂ))).det := by
  have h := gamma5_mu_intertwine_det_conj Γ5 D (μ : ℂ) hΓ (h_int (μ : ℂ))
  simpa only [star_def, conj_ofReal] using h

/-- At zero chemical potential `μ = 0`, `-star 0 = 0`, so `(D 0).det` is equal to its own
complex conjugate and therefore has zero imaginary part. -/
theorem gamma5_zero_mu_det_im_zero {n : Type*} [Fintype n] [DecidableEq n]
    (Γ5 : Matrix n n ℂ) (D : ℂ → Matrix n n ℂ)
    (hΓ : Γ5 * Γ5 = 1)
    (h_int : ∀ z : ℂ, Γ5 * D z * Γ5 = (D (-star z))ᴴ) :
    ((D 0).det).im = 0 := by
  have h := gamma5_mu_intertwine_det_conj Γ5 D 0 hΓ (h_int 0)
  simp only [star_zero, neg_zero] at h
  exact conj_eq_iff_im.mp (by simpa only [star_def] using h)

/-- At purely imaginary chemical potential `μ = I * (μI : ℂ)` (`μI : ℝ`), `-star μ = μ`,
so `(D (I * μI)).det` is real (`im = 0`). -/
theorem gamma5_imag_mu_det_im_zero {n : Type*} [Fintype n] [DecidableEq n]
    (Γ5 : Matrix n n ℂ) (D : ℂ → Matrix n n ℂ) (μI : ℝ)
    (hΓ : Γ5 * Γ5 = 1)
    (h_int : ∀ z : ℂ, Γ5 * D z * Γ5 = (D (-star z))ᴴ) :
    ((D (I * (μI : ℂ))).det).im = 0 := by
  have h := gamma5_mu_intertwine_det_conj Γ5 D (I * (μI : ℂ)) hΓ (h_int (I * (μI : ℂ)))
  have hfixed : -star (I * (μI : ℂ)) = I * (μI : ℂ) := by
    simp [star_mul, conj_I, conj_ofReal, mul_comm]
  rw [hfixed] at h
  exact conj_eq_iff_im.mp (by simpa only [star_def] using h)

/-! ## Part II: Hasenfratz-Karsch Exponential Chemical-Potential Operator & Staggered Fermions -/

/-- Lattice Dirac operator with Hasenfratz-Karsch chemical potential `μ ∈ ℂ` weighted by a
chemical-potential exponential map `expMap : ℂ → ℂ`:
forward temporal hopping `Kpos` is weighted by `expMap(μ)` and backward temporal hopping `Kneg`
is weighted by `expMap(-μ)`. -/
def diracMu {n : Type*} (expMap : ℂ → ℂ) (M0 Kpos Kneg : Matrix n n ℂ) (μ : ℂ) : Matrix n n ℂ :=
  M0 + expMap μ • Kpos + expMap (-μ) • Kneg

lemma star_expMap_neg_star (expMap : ℂ → ℂ) (hexp : ∀ z : ℂ, star (expMap z) = expMap (star z))
    (μ : ℂ) : star (expMap (-star μ)) = expMap (-μ) := by
  rw [hexp, star_neg, star_star]

lemma star_expMap_star (expMap : ℂ → ℂ) (hexp : ∀ z : ℂ, star (expMap z) = expMap (star z))
    (μ : ℂ) : star (expMap (star μ)) = expMap μ := by
  rw [hexp, star_star]

/-- **Hasenfratz-Karsch γ₅-Hermiticity Identity**:
If `expMap` commutes with complex conjugation (`star (expMap z) = expMap (star z)`), and `Γ5`
intertwines the spatial/mass part `M0` with `M0ᴴ` and swaps `Kpos, Kneg` with `Knegᴴ, Kposᴴ`,
then `Γ5 * diracMu expMap M0 Kpos Kneg μ * Γ5 = (diracMu expMap M0 Kpos Kneg (-star μ))ᴴ`
for every complex chemical potential `μ ∈ ℂ`. -/
theorem diracMu_gamma5_adjoint {n : Type*} [Fintype n] [DecidableEq n]
    (expMap : ℂ → ℂ) (hexp : ∀ z : ℂ, star (expMap z) = expMap (star z))
    (Γ5 M0 Kpos Kneg : Matrix n n ℂ)
    (hM0 : Γ5 * M0 * Γ5 = M0ᴴ)
    (hKpos : Γ5 * Kpos * Γ5 = Knegᴴ)
    (hKneg : Γ5 * Kneg * Γ5 = Kposᴴ)
    (μ : ℂ) :
    Γ5 * diracMu expMap M0 Kpos Kneg μ * Γ5 =
      (diracMu expMap M0 Kpos Kneg (-star μ))ᴴ := by
  unfold diracMu
  rw [mul_add, mul_add, add_mul, add_mul]
  rw [Matrix.mul_smul, Matrix.smul_mul, Matrix.mul_smul, Matrix.smul_mul]
  rw [hM0, hKpos, hKneg]
  rw [conjTranspose_add, conjTranspose_add, conjTranspose_smul, conjTranspose_smul, neg_neg]
  rw [star_expMap_neg_star expMap hexp μ, star_expMap_star expMap hexp μ]
  abel

/-- **Hasenfratz-Karsch Determinant Conjugation Theorem**:
Under the hypotheses of `diracMu_gamma5_adjoint` and `Γ5 * Γ5 = 1`,
`star (diracMu expMap M0 Kpos Kneg μ).det = (diracMu expMap M0 Kpos Kneg (-star μ)).det`. -/
theorem diracMu_det_conj {n : Type*} [Fintype n] [DecidableEq n]
    (expMap : ℂ → ℂ) (hexp : ∀ z : ℂ, star (expMap z) = expMap (star z))
    (Γ5 M0 Kpos Kneg : Matrix n n ℂ)
    (hΓ : Γ5 * Γ5 = 1)
    (hM0 : Γ5 * M0 * Γ5 = M0ᴴ)
    (hKpos : Γ5 * Kpos * Γ5 = Knegᴴ)
    (hKneg : Γ5 * Kneg * Γ5 = Kposᴴ)
    (μ : ℂ) :
    star (diracMu expMap M0 Kpos Kneg μ).det =
      (diracMu expMap M0 Kpos Kneg (-star μ)).det :=
  gamma5_mu_intertwine_det_conj Γ5 (diracMu expMap M0 Kpos Kneg) μ hΓ
    (diracMu_gamma5_adjoint expMap hexp Γ5 M0 Kpos Kneg hM0 hKpos hKneg μ)

/-- **Kogut-Susskind Staggered Dirac Operator with Chemical Potential**:
Given a staggered site-parity involution `Γ5` (`Γ5 * Γ5 = 1`, `Γ5ᴴ = Γ5`), real quark mass `m`,
and forward temporal hopping `Tpos` that anticommutes with `Γ5` (`Γ5 * Tpos * Γ5 = -Tpos`),
the staggered operator `D_stag(μ) = m I + expMap(μ) Tpos - expMap(-μ) Tposᴴ` satisfies
`Γ5 * D_stag(μ) * Γ5 = (D_stag(-star μ))ᴴ` and `star (det D_stag(μ)) = det D_stag(-star μ)`. -/
def staggeredDiracMu {n : Type*} [DecidableEq n]
    (expMap : ℂ → ℂ) (m : ℝ) (Tpos : Matrix n n ℂ) (μ : ℂ) : Matrix n n ℂ :=
  diracMu expMap ((m : ℂ) • 1) Tpos (-Tposᴴ) μ

theorem staggeredDiracMu_gamma5_adjoint {n : Type*} [Fintype n] [DecidableEq n]
    (expMap : ℂ → ℂ) (hexp : ∀ z : ℂ, star (expMap z) = expMap (star z))
    (Γ5 Tpos : Matrix n n ℂ) (m : ℝ)
    (hΓ_sq : Γ5 * Γ5 = 1)
    (hΓ_herm : Γ5ᴴ = Γ5)
    (hT_anti : Γ5 * Tpos * Γ5 = -Tpos)
    (μ : ℂ) :
    Γ5 * staggeredDiracMu expMap m Tpos μ * Γ5 =
      (staggeredDiracMu expMap m Tpos (-star μ))ᴴ := by
  apply diracMu_gamma5_adjoint expMap hexp
  · rw [Matrix.mul_smul, Matrix.smul_mul, mul_one, hΓ_sq, conjTranspose_smul, conjTranspose_one]
    simp
  · rw [hT_anti, conjTranspose_neg, conjTranspose_conjTranspose]
  · calc
      Γ5 * (-Tposᴴ) * Γ5 = -(Γ5 * Tposᴴ * Γ5) := by simp
      _ = -(Γ5ᴴ * Tposᴴ * Γ5ᴴ) := by rw [hΓ_herm]
      _ = -((Γ5 * Tpos * Γ5)ᴴ) := by
        rw [← conjTranspose_mul, ← conjTranspose_mul, mul_assoc]
      _ = -((-Tpos)ᴴ) := by rw [hT_anti]
      _ = Tposᴴ := by rw [conjTranspose_neg, neg_neg]

theorem staggeredDiracMu_det_conj {n : Type*} [Fintype n] [DecidableEq n]
    (expMap : ℂ → ℂ) (hexp : ∀ z : ℂ, star (expMap z) = expMap (star z))
    (Γ5 Tpos : Matrix n n ℂ) (m : ℝ)
    (hΓ_sq : Γ5 * Γ5 = 1)
    (hΓ_herm : Γ5ᴴ = Γ5)
    (hT_anti : Γ5 * Tpos * Γ5 = -Tpos)
    (μ : ℂ) :
    star (staggeredDiracMu expMap m Tpos μ).det =
      (staggeredDiracMu expMap m Tpos (-star μ)).det :=
  gamma5_mu_intertwine_det_conj Γ5 (staggeredDiracMu expMap m Tpos) μ hΓ_sq
    (staggeredDiracMu_gamma5_adjoint expMap hexp Γ5 Tpos m hΓ_sq hΓ_herm hT_anti μ)

/-! ## Part III: Explicit SU(3) Link Witness & Nonreal Determinant at Real Chemical Potential -/

/-- Explicit diagonal `SU(3)` link matrix `U = diag(I, I, -1)` with Gaussian-integer entries.
Its eigenvalues are `i, i, -1`, whose product is `i * i * (-1) = 1` and whose trace is `2i - 1`. -/
def su3ClockLink : Matrix (Fin 3) (Fin 3) ℂ :=
  !![I, 0, 0;
     0, I, 0;
     0, 0, -1]

/-- `su3ClockLink` is unitary: `U * Uᴴ = I_3`. -/
theorem su3ClockLink_unitary : su3ClockLink * su3ClockLinkᴴ = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [su3ClockLink, mul_apply, Fin.sum_univ_three, conjTranspose_apply, one_apply]

/-- `det(su3ClockLink) = 1`, confirming `su3ClockLink ∈ SU(3)`. -/
theorem su3ClockLink_det : su3ClockLink.det = 1 := by
  simp [su3ClockLink, det_fin_three, I_mul_I]

/-- Unlike `SU(2)`, where every group element has real trace, `su3ClockLink ∈ SU(3)` has
nonreal trace `Tr(U) = -1 + 2i` (`Im Tr(U) = 2 ≠ 0`), reflecting the complex `3 ≇ 3̄` representation. -/
theorem su3ClockLink_trace_im_ne_zero :
    (su3ClockLink.trace).im = 2 ∧ (su3ClockLink.trace).im ≠ 0 := by
  constructor
  · simp [su3ClockLink, trace, Fin.sum_univ_three]
    norm_num
  · simp [su3ClockLink, trace, Fin.sum_univ_three]

/-- Chiral / γ₀-diagonal 6x6 `SU(3)` lattice Dirac operator at fugacity `z = e^μ ∈ ℂ`:
`D_SU3(z) = diag(I_3 - z U, I_3 - z⁻¹ Uᴴ)` on `Fin 3 ⊕ Fin 3`. -/
def su3FugacityDirac (z : ℂ) : Matrix (Fin 3 ⊕ Fin 3) (Fin 3 ⊕ Fin 3) ℂ :=
  fromBlocks (1 - z • su3ClockLink) 0 0 (1 - z⁻¹ • su3ClockLinkᴴ)

/-- Chiral involution `Γ5 = [[0, I_3], [I_3, 0]]` swapping forward and backward chiral blocks. -/
def gamma5Chiral3 : Matrix (Fin 3 ⊕ Fin 3) (Fin 3 ⊕ Fin 3) ℂ :=
  fromBlocks 0 1 1 0

theorem gamma5Chiral3_sq : gamma5Chiral3 * gamma5Chiral3 = 1 := by
  simp [gamma5Chiral3, fromBlocks_multiply, fromBlocks_one]

/-- `gamma5Chiral3` intertwines `su3FugacityDirac z` with `(su3FugacityDirac (star z)⁻¹)ᴴ`. -/
theorem su3FugacityDirac_gamma5_intertwine (z : ℂ) :
    gamma5Chiral3 * su3FugacityDirac z * gamma5Chiral3 =
      (su3FugacityDirac (star z)⁻¹)ᴴ := by
  simp [gamma5Chiral3, su3FugacityDirac, fromBlocks_multiply, fromBlocks_conjTranspose,
    conjTranspose_sub, conjTranspose_smul, conjTranspose_conjTranspose]

/-- At real positive fugacity `z = 2` (`μ = ln 2 > 0`), the exact `SU(3)` Dirac determinant is
`(su3FugacityDirac 2).det = 63 / 8 - 27 * I`. -/
theorem su3FugacityDirac_det_at_two :
    (su3FugacityDirac 2).det = (63 / 8 : ℂ) - 27 * I := by
  rw [su3FugacityDirac, det_fromBlocks_zero₂₁]
  simp only [su3ClockLink, det_fin_three, Matrix.sub_apply, Matrix.smul_apply]
  norm_num [Complex.ext_iff, mul_re, mul_im, I_re, I_im]

/-- At the inverse real fugacity `z = 1/2` (`-μ = -ln 2 < 0`), the exact `SU(3)` Dirac
determinant is the complex conjugate `(su3FugacityDirac (1/2)).det = 63 / 8 + 27 * I`. -/
theorem su3FugacityDirac_det_at_half :
    (su3FugacityDirac (1 / 2 : ℂ)).det = (63 / 8 : ℂ) + 27 * I := by
  rw [su3FugacityDirac, det_fromBlocks_zero₂₁]
  simp only [su3ClockLink, det_fin_three, Matrix.sub_apply, Matrix.smul_apply]
  norm_num [Complex.ext_iff, mul_re, mul_im, I_re, I_im]

/-- **Complex Quark Determinant Witness at Real Chemical Potential**:
At real fugacity `z = 2` (`μ = ln 2 ≠ 0`), `(su3FugacityDirac 2).det` has strictly nonzero
imaginary part `-27 ≠ 0`, and its complex conjugate equals `(su3FugacityDirac (1/2)).det`
while `(su3FugacityDirac 2).det ≠ (su3FugacityDirac (1/2)).det`. -/
theorem su3FugacityDirac_complex_det_witness :
    ((su3FugacityDirac 2).det).im = -27 ∧
    ((su3FugacityDirac 2).det).im ≠ 0 ∧
    star (su3FugacityDirac 2).det = (su3FugacityDirac (1 / 2 : ℂ)).det ∧
    (su3FugacityDirac 2).det ≠ (su3FugacityDirac (1 / 2 : ℂ)).det := by
  rw [su3FugacityDirac_det_at_two, su3FugacityDirac_det_at_half]
  refine ⟨?_, ?_, ?_, ?_⟩
  · norm_num
  · norm_num
  · norm_num [Complex.ext_iff]
  · intro h
    have him := congrArg Complex.im h
    norm_num at him

/-- Contrast with `SU(2)`: for any diagonal `SU(2)` link `diag(u, star u)` with `u * star u = 1`
and any real fugacity `r : ℝ`, the forward block determinant `(1 - r • diag(u, star u)).det`
equals `1 - r * (u + star u) + r^2`, which has zero imaginary part for all `r ∈ ℝ`. -/
def su2DiagLink (u : ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![u, 0; 0, star u]

theorem su2DiagLink_block_det_im_zero (u : ℂ) (hu : u * star u = 1) (r : ℝ) :
    (((1 : Matrix (Fin 2) (Fin 2) ℂ) - (r : ℂ) • su2DiagLink u).det).im = 0 := by
  have hu' : u * (starRingEnd ℂ) u = 1 := by simpa only [star_def] using hu
  have hdet : ((1 : Matrix (Fin 2) (Fin 2) ℂ) - (r : ℂ) • su2DiagLink u).det =
      1 - (r : ℂ) * (u + (starRingEnd ℂ) u) + (r : ℂ) * (r : ℂ) := by
    simp [su2DiagLink, det_fin_two]
    linear_combination (r : ℂ) ^ 2 * hu'
  rw [hdet]
  simp

end

end FermionSignQcdChemicalPotentialDet

#print axioms FermionSignQcdChemicalPotentialDet.det_conj_by_involution
#print axioms FermionSignQcdChemicalPotentialDet.gamma5_mu_intertwine_det_conj
#print axioms FermionSignQcdChemicalPotentialDet.gamma5_real_mu_det_conj
#print axioms FermionSignQcdChemicalPotentialDet.gamma5_zero_mu_det_im_zero
#print axioms FermionSignQcdChemicalPotentialDet.gamma5_imag_mu_det_im_zero
#print axioms FermionSignQcdChemicalPotentialDet.diracMu_gamma5_adjoint
#print axioms FermionSignQcdChemicalPotentialDet.diracMu_det_conj
#print axioms FermionSignQcdChemicalPotentialDet.staggeredDiracMu_gamma5_adjoint
#print axioms FermionSignQcdChemicalPotentialDet.staggeredDiracMu_det_conj
#print axioms FermionSignQcdChemicalPotentialDet.su3ClockLink_unitary
#print axioms FermionSignQcdChemicalPotentialDet.su3ClockLink_det
#print axioms FermionSignQcdChemicalPotentialDet.su3ClockLink_trace_im_ne_zero
#print axioms FermionSignQcdChemicalPotentialDet.su3FugacityDirac_gamma5_intertwine
#print axioms FermionSignQcdChemicalPotentialDet.su3FugacityDirac_det_at_two
#print axioms FermionSignQcdChemicalPotentialDet.su3FugacityDirac_det_at_half
#print axioms FermionSignQcdChemicalPotentialDet.su3FugacityDirac_complex_det_witness
#print axioms FermionSignQcdChemicalPotentialDet.su2DiagLink_block_det_im_zero
