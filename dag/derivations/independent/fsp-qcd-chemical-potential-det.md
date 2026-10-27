Status: AI-drafted, awaiting human review.

# FSP-QCD-CHEMICAL-POTENTIAL-DET

AuthorityEffect: None.

The node `FSP-QCD-CHEMICAL-POTENTIAL-DET` (`TFQ-1201`) remains `IMPORTED_ASSUMPTION` (`Narrowed`), while its finite algebraic core—the general $\gamma_5$-chemical-potential intertwining identity $\Gamma_5 D(\mu) \Gamma_5 = D(-\mu^*)^\dagger$ and determinant conjugation law $(\det D(\mu))^* = \det D(-\mu^*)$, its specialization to real chemical potential $\mu \in \mathbb{R}$, $\mu = 0$, and purely imaginary $\mu = i \mu_I$, the Hasenfratz–Karsch and Kogut–Susskind staggered operator identities, the explicit $SU(3)$ clock link $U = \operatorname{diag}(i, i, -1) \in SU(3)$ with $\operatorname{Im}\operatorname{Tr}(U) = 2 \neq 0$, the exact $6 \times 6$ chiral $SU(3)$ Dirac determinant witness $\det D_{\text{SU3}}(2) = \frac{63}{8} - 27 i \notin \mathbb{R}$ and $\det D_{\text{SU3}}(1/2) = \frac{63}{8} + 27 i$, and the diagonal $SU(2)$ reality contrast—is formalized in `lean4/FermionSignQcdChemicalPotentialDet.lean` and checked in `checks/independent/fsp-qcd-chemical-potential-det.py`.

## Setting

1. **General $\gamma_5$-Chemical-Potential Intertwining (`gamma5_mu_intertwine_det_conj`, `gamma5_real_mu_det_conj`)**:
   For a finite index type $n$, an involutive matrix $\Gamma_5 \in M_n(\mathbb{C})$ ($\Gamma_5^2 = I_n$), and a family of matrices $D : \mathbb{C} \to M_n(\mathbb{C})$ satisfying $\Gamma_5 D(\mu) \Gamma_5 = D(-\mu^*)^\dagger$, taking determinants and complex conjugates yields
   $$\bigl(\det D(\mu)\bigr)^* = \det D(-\mu^*).$$
   - At real chemical potential $\mu \in \mathbb{R}$, $\mu^* = \mu$, so $(\det D(\mu))^* = \det D(-\mu)$, and $\det D(\mu)$ is real if and only if $\det D(\mu) = \det D(-\mu)$.
   - At $\mu = 0$ (`gamma5_zero_mu_det_im_zero`) and at purely imaginary $\mu = i \mu_I$ with $\mu_I \in \mathbb{R}$ (`gamma5_imag_mu_det_im_zero`), $-\mu^* = \mu$, forcing $\operatorname{Im}\det D(\mu) = 0$.

2. **Hasenfratz–Karsch & Kogut–Susskind Staggered Chemical-Potential Operators (`diracMu_det_conj`, `staggeredDiracMu_det_conj`)**:
   For $D(\mu) = M_0 + \exp(\mu)\, K_+ + \exp(-\mu)\, K_-$ with $\overline{\exp(z)} = \exp(\bar z)$, if $\Gamma_5 M_0 \Gamma_5 = M_0^\dagger$, $\Gamma_5 K_+ \Gamma_5 = K_-^\dagger$, and $\Gamma_5 K_- \Gamma_5 = K_+^\dagger$, then $\Gamma_5 D(\mu) \Gamma_5 = D(-\mu^*)^\dagger$ and $(\det D(\mu))^* = \det D(-\mu^*)$. In the Kogut–Susskind staggered discretization, $\Gamma_5$ is the Hermitian site-parity involution ($\Gamma_5^2 = I$, $\Gamma_5^\dagger = \Gamma_5$), $M_0 = m I$, $K_- = -K_+^\dagger$, and $\Gamma_5 K_+ \Gamma_5 = -K_+$.

3. **Explicit $SU(3)$ Complex Determinant Witness & $SU(2)$ Contrast (`su3FugacityDirac_complex_det_witness`, `su2DiagLink_block_det_im_zero`)**:
   - The diagonal Gaussian-integer matrix $U_{\text{SU3}} = \operatorname{diag}(i, i, -1)$ satisfies $U_{\text{SU3}} U_{\text{SU3}}^\dagger = I_3$, $\det U_{\text{SU3}} = 1$, and $\operatorname{Im}\operatorname{Tr}(U_{\text{SU3}}) = 2 \neq 0$.
   - For the $6 \times 6$ chiral operator $D_{\text{SU3}}(z) = \operatorname{diag}(I_3 - z U_{\text{SU3}}, I_3 - z^{-1} U_{\text{SU3}}^\dagger)$ intertwined by $\Gamma_5 = \begin{pmatrix} 0 & I_3 \\ I_3 & 0 \end{pmatrix}$, evaluating at real fugacity $z = 2$ ($\mu = \ln 2 > 0$) and $z = 1/2$ ($-\mu = -\ln 2 < 0$) gives
     $$\det D_{\text{SU3}}(2) = \frac{63}{8} - 27 i, \qquad \det D_{\text{SU3}}(1/2) = \frac{63}{8} + 27 i,$$
     so $\operatorname{Im}\det D_{\text{SU3}}(2) = -27 \neq 0$ and $\det D_{\text{SU3}}(2) \neq \det D_{\text{SU3}}(1/2)$.
   - By contrast, for any diagonal $SU(2)$ link $\operatorname{diag}(u, u^*)$ with $u u^* = 1$ and any real fugacity $r \in \mathbb{R}$, $\det(I_2 - r\,\operatorname{diag}(u, u^*)) = 1 - r(u + u^*) + r^2$ has zero imaginary part.

## Lean 4 Declarations (`lean4/FermionSignQcdChemicalPotentialDet.lean`)

Built via `cd lean4 && lake build FermionSignQcdChemicalPotentialDet` using only standard axioms (`propext`, `Classical.choice`, `Quot.sound`):
- `FermionSignQcdChemicalPotentialDet.det_conj_by_involution`
- `FermionSignQcdChemicalPotentialDet.gamma5_mu_intertwine_det_conj`
- `FermionSignQcdChemicalPotentialDet.gamma5_real_mu_det_conj`
- `FermionSignQcdChemicalPotentialDet.gamma5_zero_mu_det_im_zero`
- `FermionSignQcdChemicalPotentialDet.gamma5_imag_mu_det_im_zero`
- `FermionSignQcdChemicalPotentialDet.diracMu_gamma5_adjoint`
- `FermionSignQcdChemicalPotentialDet.diracMu_det_conj`
- `FermionSignQcdChemicalPotentialDet.staggeredDiracMu_gamma5_adjoint`
- `FermionSignQcdChemicalPotentialDet.staggeredDiracMu_det_conj`
- `FermionSignQcdChemicalPotentialDet.su3ClockLink_unitary`
- `FermionSignQcdChemicalPotentialDet.su3ClockLink_det`
- `FermionSignQcdChemicalPotentialDet.su3ClockLink_trace_im_ne_zero`
- `FermionSignQcdChemicalPotentialDet.su3FugacityDirac_gamma5_intertwine`
- `FermionSignQcdChemicalPotentialDet.su3FugacityDirac_det_at_two`
- `FermionSignQcdChemicalPotentialDet.su3FugacityDirac_det_at_half`
- `FermionSignQcdChemicalPotentialDet.su3FugacityDirac_complex_det_witness`
- `FermionSignQcdChemicalPotentialDet.su2DiagLink_block_det_im_zero`

## Independent Check (`checks/independent/fsp-qcd-chemical-potential-det.py`)

Imports no repository code. Uses Python `fractions.Fraction` and SymPy to check:
- Symbolic and exact rational fugacity evaluations of the $6 \times 6$ chiral $SU(3)$ clock-link operator $D_{\text{SU3}}(z)$, confirming $\det D_{\text{SU3}}(2) = 63/8 - 27 i$, $\det D_{\text{SU3}}(1/2) = 63/8 + 27 i$, unit-circle reality for purely imaginary $\mu$, and nonzero imaginary parts across rational real fugacities $z \neq 1$.
- $12 \times 12$ Kogut–Susskind staggered $SU(3)$ Dirac operators on 1D ($L=4$) and 2D ($2 \times 2$) periodic lattices with non-commuting $SU(3)$ links carrying complex Polyakov loop traces, confirming $\Gamma_5 D(\mu) \Gamma_5 = D(-\mu^*)^\dagger$, $(\det D(\mu))^* = \det D(-\mu^*)$, reality at $\mu = 0$ and imaginary $\mu$, and $\operatorname{Im}\det D(\mu) \neq 0$ at real $\mu \neq 0$.
- Contrast with $SU(2)$ fundamental links on the same $2 \times 2$ staggered lattice, where $\operatorname{Im}\det D(\mu) = 0$ and $\det D(\mu) > 0$ for all tested real fugacities.

## Scope Fence (What Is Not Claimed)

1. **What it supports**: The exact finite-dimensional $\gamma_5$-chemical-potential intertwining identity $\Gamma_5 D(\mu) \Gamma_5 = D(-\mu^*)^\dagger$ and determinant conjugation law $(\det D(\mu))^* = \det D(-\mu^*)$, reality at $\mu = 0$ and purely imaginary $\mu = i \mu_I$, the Hasenfratz–Karsch and Kogut–Susskind staggered operator identities, and explicit finite $SU(3)$ link witnesses where $\operatorname{Im}\det D(\mu) \neq 0$ at real $\mu \neq 0$.
2. **What it does not support**: Full continuum or thermodynamic-limit 4D QCD path-integral construction, silver-blaze phase-transition dynamics, or severity bounds for the finite-volume QCD phase-quenched reweighting factor $\langle e^{i N_f \theta} \rangle_{\text{pq}} \sim e^{-V \Delta f}$.
3. **Narrowest defensible claim**: In Lean 4 (`FermionSignQcdChemicalPotentialDet`), any matrix family $D(\mu)$ intertwined by an involution $\Gamma_5$ with $D(-\mu^*)^\dagger$ satisfies $(\det D(\mu))^* = \det D(-\mu^*)$ (with $\operatorname{Im}\det D(\mu) = 0$ at $\mu = 0$ and $\mu = i\mu_I$), the Hasenfratz–Karsch and Kogut–Susskind staggered operators satisfy this intertwining, and the explicit $SU(3)$ clock link $U = \operatorname{diag}(i,i,-1)$ gives $\det D_{\text{SU3}}(2) = \frac{63}{8} - 27 i$ and $\det D_{\text{SU3}}(1/2) = \frac{63}{8} + 27 i$ with $\operatorname{Im}\det D_{\text{SU3}}(2) = -27 \neq 0$.
