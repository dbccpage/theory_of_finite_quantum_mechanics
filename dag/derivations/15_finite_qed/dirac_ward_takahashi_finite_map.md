# AuthorityEffect: None.

# QM-215: Dirac / Kulish–Faddeev Dressed Matter Propagator & Exact Clifford Ward–Takahashi Identity $Z_1 = Z_2$

## 1. Purpose and Finite-to-Continuum Bridge Scope

Standard textbook presentations of Quantum Electrodynamics (QED) encounter three linked obstacles in the matter sector:
1. **Gauge dependence of bare fermion correlators:** Under a local vertex gauge transformation $g_v \in \mathrm{U}(1)$, the bare spinor field transforms as $\psi_v \mapsto g_v \psi_v$, so the two-point correlator $\langle \bar{\psi}_y, \psi_x \rangle$ is not gauge-invariant for $x \neq y$.
2. **Ultraviolet (UV) charge renormalization identity $Z_1 = Z_2$:** Textbook proofs of $Z_1 = Z_2$ often rely on formal manipulations of divergent continuum integrals ($\int d^4k$) where momentum shifts $k \mapsto k + q$ require regulator-dependent justification.
3. **Infrared (IR) soft-photon divergences:** Perturbative scattering amplitudes with bare external electrons diverge as the photon mass or IR cutoff $\lambda_{\mathrm{IR}} \to 0$.

`QM-215` resolves all three mechanisms on a finite, continuum-free algebraic spine over $\mathbb{Q}$ and $\mathbb{Q}(i)$ paired with certified `BigRational` / `RationalInterval` enclosures:
- **Layer 1 (Exact Algebraic & Cohomological Spine over $\mathbb{Q}(i)$):**
  - Represents the $4 \times 4$ Dirac Clifford algebra $C\ell_{1,3}(\mathbb{Q}(i))$ in the standard Dirac basis with exact Gaussian rational entries, checking $\{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu}I_4$, $\not{p}\not{p} = (p \cdot p)I_4$, and exact rational propagator inversion $S_F(p) S_F(p)^{-1} = I_4$ where $S_F(p)^{-1} = \not{p} - m I_4$ and $S_F(p) = (\not{p} + m I_4)/(p^2 - m^2)$.
  - Implements Dirac / Ravera spanning-tree fermion dressing $\Psi_v^{(T)} = u_T[U](v)^{-1}\psi_v$, where $u_T[U](v) = \prod_{e \in P_T(v_0 \to v)} U_e^{\pm 1} \in \mathrm{U}(1) \subset \mathbb{Q}(i)$ is the path holonomy along spanning tree $T$. Under any local vertex gauge transformation $U_{uv}^g = g_v U_{uv} g_u^{-1}$ and $\psi_v^g = g_v \psi_v$ (with $g_{v_0} = 1$), the dressed spinor $\Psi_v^{(T)}$ and two-point correlator $\langle \bar{\Psi}_y^{(T)}, \Psi_x^{(T)} \rangle$ are invariant across all $8$ spanning trees of the 4-vertex diamond graph, while changing spanning tree $T_a \to T_b$ shifts $\langle \bar{\Psi}_y^{(T)}, \Psi_x^{(T)} \rangle$ by a gauge-invariant fundamental-cycle holonomy factor.
  - Evaluates the 1-loop QED vertex integrand $\mathcal{I}_\Lambda^\mu(p', p; k)$ and fermion self-energy integrand $\mathcal{I}_\Sigma(p, k)$ in $M_4(\mathbb{Q}(i))$:
    $$\mathcal{I}_\Lambda^\mu(p', p; k) = \sum_{\nu=0}^3 \eta_{\nu\nu} \frac{\gamma^\nu S_F(p'-k)\gamma^\mu S_F(p-k)\gamma^\nu}{k^2 - \lambda_\gamma^2}, \qquad \mathcal{I}_\Sigma(p, k) = \sum_{\nu=0}^3 \eta_{\nu\nu} \frac{\gamma^\nu S_F(p-k)\gamma^\nu}{k^2 - \lambda_\gamma^2}.$$
    Contraction with external photon momentum $q_\mu$ satisfies the exact integrand-level 1-loop Ward–Takahashi identity
    $$q_\mu \mathcal{I}_\Lambda^\mu(p+q, p; k) = \mathcal{I}_\Sigma(p, k) - \mathcal{I}_\Sigma(p+q, k)$$
    at every rational loop momentum $k \in \mathbb{Q}^4$ before integration. Taking the exact analytical derivative with respect to $p_\mu$ at $q = 0$ yields the differential Ward identity
    $$\mathcal{I}_\Lambda^\mu(p, p; k) = -\frac{\partial \mathcal{I}_\Sigma(p, k)}{\partial p_\mu},$$
    which forces the BPHZ Taylor subtraction operators at $p = q = 0$ to coincide ($T^0_{p'=p=0}\mathcal{I}_\Lambda^\mu = -\partial_{p_\mu} T^1_{p=0}\mathcal{I}_\Sigma$) and yields $Z_1 = Z_2$ ($Z_1 / Z_2 = 1 \in \mathbb{Q}$).
- **Layer 2 (Kulish–Faddeev / Bloch–Nordsieck IR Soft-Photon Enclosure):**
  - Verifies exact algebraic cancellation of the fictitious IR cutoff $\lambda_{\mathrm{IR}}$ and Laurent pole $\varepsilon_{\mathrm{IR}}^{-1}$ between the virtual soft-photon exponent $B_{\mathrm{virt}}(\lambda_{\mathrm{IR}}) = -\frac{\alpha}{\pi} J(v)\ln(m/\lambda_{\mathrm{IR}})$ and the real soft-photon emission exponent $\tilde{B}_{\mathrm{real}}(\Delta E, \lambda_{\mathrm{IR}}) = +\frac{\alpha}{\pi} J(v)\ln(2\Delta E/\lambda_{\mathrm{IR}})$.
  - Encloses the resulting regulator-free Yennie–Frautschi–Suura / Kulish–Faddeev attenuation factor
    $$\mathcal{S}_{\mathrm{KF}}(v, \Delta E) = \exp\!\left(\frac{\alpha}{\pi} J(v) \ln\frac{2\Delta E}{m}\right), \qquad J(v) = \frac{1}{v}\ln\frac{1+v}{1-v} - 1,$$
    at rational cusp velocity $v = 3/5$ ($\frac{1+v}{1-v} = 4 \implies J(3/5) = \frac{10}{3}\ln 2 - 1$) and energy resolution ratio $2\Delta E / m = 1/2$ to 12 certified decimal digits (`0.997892261461`, interval width $< 10^{-14}$).

## 2. Executable Evidence and Parity

- **Rust Unit Control:** `quantum_physics::quantum_import_finite_maps::evaluate_qm215_dirac_ward_takahashi` and `test_qm215_dirac_ward_takahashi_control` in `external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579`.
- **Python Use-Case & E2E Suite:** `finite_qm.use_cases.dirac_ward_takahashi_control` and `tests/e2e/test_e2e_dirac_ward_takahashi_control.py` (`6 passed`).

## 3. Claim Hygiene Summary

1. **What it supports:**
   - Exact $4 \times 4$ Clifford algebra $C\ell_{1,3}(\mathbb{Q}(i))$ arithmetic, spanning-tree DFM fermion dressing gauge invariance across all $8$ spanning trees of the diamond graph, integrand-level 1-loop Ward–Takahashi and differential Ward identities in $M_4(\mathbb{Q}(i))$ implying $Z_1 / Z_2 = 1$, and 12-decimal `BigRational` / `RationalInterval` enclosure of the Kulish–Faddeev soft-photon attenuation factor (`0.997892261461`) at $v = 3/5$, $2\Delta E / m = 1/2$.
2. **What it does not support:**
   - All-orders non-perturbative confinement, chiral axial anomalies on curved manifolds, or multi-loop numerical integration over non-rational external kinematics.
3. **The narrowest defensible claim:**
   - In this finite algebraic and rational-interval model over $\mathbb{Q}$ and $\mathbb{Q}(i)$, spanning-tree DFM dressing renders two-point spinor correlators invariant under local $\mathrm{U}(1)$ vertex gauge transformations, the 1-loop QED vertex and self-energy integrands satisfy $q_\mu \mathcal{I}_\Lambda^\mu(p+q, p; k) = \mathcal{I}_\Sigma(p, k) - \mathcal{I}_\Sigma(p+q, k)$ and $\mathcal{I}_\Lambda^\mu(p, p; k) = -\partial \mathcal{I}_\Sigma(p, k)/\partial p_\mu$ identically in $M_4(\mathbb{Q}(i))$ so $Z_1 = Z_2$, and the Kulish–Faddeev soft-photon attenuation factor is enclosed to 12 certified digits (`0.997892261461`) after exact IR regulator cancellation.
4. **The next test needed:**
   - Execute Step 3 (`QM-216`: 1-Loop QED Vacuum Polarization $\Pi_R(q^2)$, Running Coupling $\alpha_{\mathrm{eff}}(q^2)$, and Uehling Potential / Hydrogen $2S_{1/2}$–$2P_{1/2}$ Lamb Shift Enclosure).
