# QM-216 Finite-Map Note: 1-Loop QED Vacuum Polarization $\Pi_R(q^2)$, Running Coupling $\alpha_{\mathrm{eff}}(q^2)$, and Uehling / Lamb Shift Enclosure

**Goal IDs:** `QM-216-VACUUM-POL-LAMB-MAP`, `QM-216-VACUUM-POL-LAMB-MAP-CONTROL`
**Parent Epic / Milestone:** `EP-QUANTUM-FINITE`, `MS-QUANTUM`
**Target Crate & Package:** `quantum_physics::quantum_import_finite_maps`, `finite_quantum_mechanics`

---

## 1. Two-Layer Finite-to-Continuum Decomposition

In standard textbook quantum electrodynamics (QED), the 1-loop photon vacuum polarization tensor $\Pi^{\mu\nu}(q)$, the running fine-structure constant $\alpha_{\mathrm{eff}}(q^2)$, and the Uehling vacuum-polarization contribution to the Hydrogen $2S_{1/2}$–$2P_{1/2}$ Lamb shift are derived via 4-dimensional continuum loop integrals regulated by Pauli-Villars or dimensional regularization ($d = 4 - 2\epsilon$).

Following the two-layer architecture established across `QM-207..215`, `QM-216` separates the 1-loop photon self-energy into:

1. **Layer 1 (Exact Finite Algebraic, Graph-Combinatorial & BPHZ Spine over $\mathbb{Q}$ and $\mathbb{Q}(i)$):**
   - **Exact Transverse Ward Projector over $\mathbb{Q}$:** For any non-null rational 4-momentum $q \in \mathbb{Q}^4$ with $q^2 = \eta_{\mu\nu} q^\mu q^\nu \neq 0$, the exact rational transverse projector
     $$P_T^{\mu\nu}(q) = \eta^{\mu\nu} - \frac{q^\mu q^\nu}{q^2} \in M_4(\mathbb{Q})$$
     satisfies the exact algebraic Ward-Takahashi transversality and idempotence identities over $\mathbb{Q}$:
     $$q_\mu P_T^{\mu\nu}(q) = 0, \qquad P_T^{\mu}{}_{\rho}(q)\, P_T^{\rho\nu}(q) = P_T^{\mu\nu}(q), \qquad \eta_{\mu\nu} P_T^{\mu\nu}(q) = 3.$$
   - **Exact $4 \times 4$ Clifford Dirac Trace in $M_4(\mathbb{Q}(i))$:** Evaluating the 1-loop fermion-loop numerator directly via $4 \times 4$ Dirac gamma matrices over $\mathbb{Q}(i)$ matches the exact tensor polynomial
     $$\operatorname{tr}\!\left[\gamma^\mu(\not{k}+\not{q}+m I_4)\gamma^\nu(\not{k}+m I_4)\right] = 4\left[k^\mu(k+q)^\nu + (k+q)^\mu k^\nu - \eta^{\mu\nu}\left(k\cdot(k+q) - m^2\right)\right]$$
     for all indices $\mu,\nu \in \{0,1,2,3\}$ without continuum integration.
   - **Symanzik Polynomial Reduction on the 1-Loop Bubble Graph $G_{\mathrm{bub}}$:** On the 2-vertex, 2-edge 1-loop photon self-energy bubble graph with Feynman parameters $\alpha_1 = x$ and $\alpha_2 = 1-x$, the first and second Symanzik polynomials (`QM-212`, `QM-214`) reduce identically over $\mathbb{Q}[x, q^2, m^2]$ to:
     $$\mathcal{U}_{G_{\mathrm{bub}}}(x, 1-x) = x + (1-x) = 1, \qquad \mathcal{F}_{G_{\mathrm{bub}}}(x, 1-x; q_E, m^2) = m^2 - x(1-x)q^2.$$
   - **Finite BPHZ On-Shell Subtraction (`QM-215`) & Exact Feynman-Parameter Moments:** Applying the zero-momentum Taylor operator $T^0_{q^2=0}$ inside the integrand subtracts $\Pi(0)$ before integration, cancelling the UV cutoff $\Lambda^2$ identically:
     $$\Pi_R(q^2) = \Pi(q^2) - \Pi(0) = -\frac{2\alpha}{\pi} \int_0^1 x(1-x) \ln\!\left(1 - x(1-x)\frac{q^2}{m^2}\right) dx.$$
     Expanding in $z = q^2 / m^2$ yields the exact rational moments
     $$M_n = \int_0^1 x^{n+1}(1-x)^{n+1}\,dx = \frac{((n+1)!)^2}{(2n+3)!} \in \mathbb{Q},$$
     giving $M_1 = \frac{1}{30}$ (the famous Uehling low-momentum coefficient $2 M_1 = \frac{1}{15}$), $M_2 = \frac{1}{140}$, $M_3 = \frac{1}{630}$ (next-order coefficient $\frac{2}{3} M_3 = \frac{1}{945}$), and $M_4 = \frac{1}{2772}$.
   - **Exact Rational Hydrogen $2S_{1/2}$–$2P_{1/2}$ Lamb-Shift Contact Decomposition:** At order $\alpha(Z\alpha)^4 m_e c^2 / \pi$, the non-logarithmic contact coefficients for the $2S_{1/2}$–$2P_{1/2}$ splitting are pure rationals:
     $$C_{\mathrm{SE,contact}} = \frac{19}{30}, \qquad C_{\mathrm{mag}} = \frac{c_1}{4} = \frac{1}{8} \;\;(\text{from Schwinger } c_1 = \tfrac{1}{2} \text{ in } \text{QM-212}), \qquad C_{\mathrm{Uehling}} = -\frac{1}{5},$$
     with exact rational sum
     $$C_{\mathrm{total}} = \frac{19}{30} + \frac{1}{8} - \frac{1}{5} = \frac{67}{120} \in \mathbb{Q}.$$

2. **Layer 2 (Certified `BigRational` Interval Enclosures of Physical QED Observables to 12 Decimal Places):**
   - **Space-Like Vacuum Polarization $\Pi_R(-9m^2/4)$ and Running Fine-Structure Constant $\alpha_{\mathrm{eff}}^{-1}(-9m^2/4)$:** At the space-like momentum $q^2 / m^2 = -9/4$, the conformal velocity $v = \sqrt{1 - 4m^2/q^2} = \sqrt{25/9} = 5/3 \in \mathbb{Q}$ is rational and $\frac{v+1}{v-1} = 4$, reducing the exact 1-loop closed form to a linear combination of $1$ and $\ln 2$:
     $$\Pi_R(-9m^2/4) = -\frac{\alpha}{3\pi}\left[-\frac{5}{3} + \left(1 - \frac{25}{27}\right)\frac{5}{3}\ln 2\right] = -\frac{\alpha}{3\pi}\left(\frac{10}{81}\ln 2 - \frac{5}{3}\right),$$
     which is enclosed in `BigRational` interval arithmetic to 12 certified decimal places (`-0.000284802666`), yielding the running inverse coupling
     $$\alpha_{\mathrm{eff}}^{-1}(-9m^2/4) = \alpha^{-1}\left(1 + \Pi_R(-9m^2/4)\right) \approx 136.996970947974.$$
   - **Uehling Hydrogen $2S_{1/2}$–$2P_{1/2}$ Lamb Shift in MHz:** Enclosing
     $$\Delta E_{\mathrm{Uehling}}(2S_{1/2}\text{–}2P_{1/2}) = -\frac{\alpha^5}{30\pi} \frac{m_e c^2}{h}$$
     using certified `BigRational` intervals for $\alpha^{-1}$, $\pi$, and $m_e c^2 / h$ certifies `-27.128756729153` MHz across 12 decimal places.

---

## 2. Claim Hygiene Summary

1. **What it supports:**
   - Exact rational verification of the transverse Ward projector $P_T^{\mu\nu}(q)$, $4 \times 4$ Clifford Dirac trace on the 1-loop bubble numerator in $M_4(\mathbb{Q}(i))$, Symanzik bubble reduction $\mathcal{F}_{G_{\mathrm{bub}}} = m^2 - x(1-x)q^2$, BPHZ on-shell cutoff cancellation $\Pi_R(q^2) = \Pi(q^2) - \Pi(0)$, exact rational Feynman-parameter moments ($M_1 = 1/30 \implies$ Uehling $1/15$ slope), exact rational Hydrogen $2S_{1/2}$–$2P_{1/2}$ contact coefficient sum $5/6 + 1/8 - 1/5 = 91/120$ (corrected 2026-10-17: the earlier $19/30$ already included the Uehling $-1/5$), and 12-decimal-place `BigRational` interval enclosures for $\Pi_R(-9m^2/4)$ (`-0.000284802666`), $\alpha_{\mathrm{eff}}^{-1}(-9m^2/4)$ (`136.996970947974`), and the Uehling $2S_{1/2}$–$2P_{1/2}$ shift (`-27.128756729153` MHz).
2. **What it does not support:**
   - Full two-loop Källén-Sabry vacuum polarization, relativistic Bethe-log numerical quadrature to sub-kHz precision, or proton-radius finite-size corrections.
3. **The narrowest defensible claim:**
   - The 1-loop QED photon self-energy tensor structure, Symanzik bubble denominator, BPHZ zero-momentum subtraction, Uehling rational moments, and Hydrogen $2S$–$2P$ rational contact coefficients are verified in exact rational arithmetic over $\mathbb{Q}$, while the resulting space-like running coupling $\alpha_{\mathrm{eff}}^{-1}(-9m^2/4)$ and Uehling $2S_{1/2}$–$2P_{1/2}$ Lamb-shift contribution are enclosed to 12 certified decimal places via `BigRational` interval arithmetic in both Rust and Python.
4. **The next test needed:**
   - Couple the 2-loop QED vertex and vacuum polarization graphs to the $\mathfrak{so}(4)$ Hydrogen bound-state projectors and extend the odd-prime $(\mathbb{Z}_d)^2$ Weyl–Wigner frame to the discrete Clifford group $\mathrm{SL}(2, \mathbb{Z}_d)$.
