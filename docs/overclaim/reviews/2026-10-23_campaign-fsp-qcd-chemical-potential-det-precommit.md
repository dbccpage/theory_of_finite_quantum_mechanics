Status: AI-drafted, awaiting human review.

# Pre-Commit Overclaim & Falsification Review: `FSP-QCD-CHEMICAL-POTENTIAL-DET` (`TFQ-1201`)

**Date:** 2026-10-23  
**Campaign Node:** `FSP-QCD-CHEMICAL-POTENTIAL-DET` (`TFQ-1201`, source ID `FSP-DERIV-037`, stage `FERMION_SIGN`)  
**Outcome:** `Narrowed` (`IMPORTED_ASSUMPTION` preserved; finite algebraic $\gamma_5$-chemical-potential intertwining, Hasenfratz–Karsch / Kogut–Susskind staggered operator identities, and explicit $SU(3)$ nonreal determinant witness formalized in Lean 4 and checked by an independent Python script)  
**AuthorityEffect:** `None`

---

## 1. Falsification & Boundary Audit

1. **Historical Fixture Replacement (`NonAbelianGaugeSigns.lean`)**:
   - The legacy file `lean4/Imported/Fsp/NonAbelianGaugeSigns.lean` did not contain `qcd_chemical_potential_complex_determinant`; its declarations were `rfl` on a constant lookup table (withdrawn in `GIN-C12`).
   - `lean4/CampaignFspQcdChemicalPotentialDet.lean` replaces that table lookup with the general $\gamma_5$-chemical-potential determinant conjugation theorem `gamma5_mu_intertwine_det_conj`, the Hasenfratz–Karsch and Kogut–Susskind staggered operator identities (`diracMu_det_conj`, `staggeredDiracMu_det_conj`), and the explicit $SU(3)$ clock-link operator `su3FugacityDirac`.

2. **Exact $\gamma_5$-Chemical-Potential Intertwining & Special Cases**:
   - `gamma5_mu_intertwine_det_conj` establishes that for any involutive $\Gamma_5$ ($\Gamma_5^2 = I_n$) and matrix family $D : \mathbb{C} \to M_n(\mathbb{C})$ satisfying $\Gamma_5 D(\mu) \Gamma_5 = D(-\mu^*)^\dagger$, $(\det D(\mu))^* = \det D(-\mu^*)$.
   - `gamma5_real_mu_det_conj`, `gamma5_zero_mu_det_im_zero`, and `gamma5_imag_mu_det_im_zero` specialize this identity to real $\mu \in \mathbb{R}$ ($(\det D(\mu))^* = \det D(-\mu)$), $\mu = 0$ ($\operatorname{Im}\det D(0) = 0$), and purely imaginary $\mu = i \mu_I$ ($\operatorname{Im}\det D(i \mu_I) = 0$).

3. **Explicit $SU(3)$ Complex Determinant Witness vs. $SU(2)$ Reality**:
   - `su3ClockLink` defines $U_{\text{SU3}} = \operatorname{diag}(i, i, -1) \in SU(3)$ and establishes unitarity (`su3ClockLink_unitary`), unimodularity (`su3ClockLink_det`), and nonreal trace $\operatorname{Im}\operatorname{Tr}(U_{\text{SU3}}) = 2 \neq 0$ (`su3ClockLink_trace_im_ne_zero`).
   - `su3FugacityDirac_det_at_two`, `su3FugacityDirac_det_at_half`, and `su3FugacityDirac_complex_det_witness` establish $\det D_{\text{SU3}}(2) = \frac{63}{8} - 27 i$ and $\det D_{\text{SU3}}(1/2) = \frac{63}{8} + 27 i$, showing $\operatorname{Im}\det D_{\text{SU3}}(2) = -27 \neq 0$ and $\det D_{\text{SU3}}(2) \neq \det D_{\text{SU3}}(1/2)$.
   - `su2DiagLink_block_det_im_zero` contrasts this with diagonal $SU(2)$ links $\operatorname{diag}(u, u^*)$ ($u u^* = 1$), where $\operatorname{Im}\det(I_2 - r\,\operatorname{diag}(u, u^*)) = 0$ for all $r \in \mathbb{R}$.

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - In `lean4/CampaignFspQcdChemicalPotentialDet.lean` (`L4D`), any matrix family $D(\mu)$ intertwined by an involution $\Gamma_5$ with $D(-\mu^*)^\dagger$ satisfies $(\det D(\mu))^* = \det D(-\mu^*)$ (with $\operatorname{Im}\det D(\mu) = 0$ at $\mu = 0$ and $\mu = i\mu_I$); Hasenfratz–Karsch and Kogut–Susskind staggered operators satisfy this intertwining; and the explicit $SU(3)$ clock link $U_{\text{SU3}} = \operatorname{diag}(i,i,-1)$ yields $\det D_{\text{SU3}}(2) = \frac{63}{8} - 27 i$ and $\det D_{\text{SU3}}(1/2) = \frac{63}{8} + 27 i$ with $\operatorname{Im}\det D_{\text{SU3}}(2) = -27 \neq 0$.
   - In `checks/independent/fsp-qcd-chemical-potential-det.py` (`L4D`), 79 exact symbolic and rational checks pass with 12 nonreal-determinant witnesses across the $6 \times 6$ chiral $SU(3)$ witness and $12 \times 12$ 1D/2D Kogut–Susskind staggered $SU(3)$ lattices.
2. **What it does not support**:
   - Full continuum or thermodynamic-limit 4D QCD path-integral construction, silver-blaze phase-transition dynamics, or asymptotic bounds on the finite-volume phase-quenched reweighting factor $\langle e^{i N_f \theta} \rangle_{\text{pq}} \sim e^{-V \Delta f}$.
3. **Narrowest defensible claim**:
   - Chemical-potential $\gamma_5$-intertwining $\Gamma_5 D(\mu) \Gamma_5 = D(-\mu^*)^\dagger$ forces $(\det D(\mu))^* = \det D(-\mu^*)$ (giving real determinants at $\mu = 0$ and purely imaginary $\mu = i \mu_I$), while at real $\mu \neq 0$ the explicit $SU(3)$ link $U_{\text{SU3}} = \operatorname{diag}(i,i,-1)$ produces $\det D_{\text{SU3}}(2) = \frac{63}{8} - 27 i \notin \mathbb{R}$.
4. **Next test needed**:
   - Proceed to the next available derivation in `dag/pfp/campaign/derivation_queue.json`.
