---
title: "Charged Scalar Matter Coupled to Light: Superradiance, Holographic Storage and Driven Density Patterns, as Theorems"
subtitle: "The holographic brain paper, rewritten as mathematics"
date: 2026-11-05
---

**Source.** Nishiyama, Tanaka, Tuszynski, Tsenkova, *Holographic Brain Theory: Super-Radiance, Memory Capacity and Control Theory*, Int. J. Mol. Sci. **25**, 2399 (2024). Equation labels of the form (A$n$) refer to its appendices; labels of the form ($k.n$) are ours.

**What this is.** The same model, the same four calculations, written so that every assumption is a numbered hypothesis, every result is a proposition with a proof, every misprint is corrected, and every number is derived. Nothing is claimed that is not proved. Section 6 states, as mathematics, what the model does not contain.

---

## 0. Conventions

Units $\hbar = c = 1$. Coordinates $x = (x^0,\mathbf{x})$, $\partial_0 = \partial/\partial x^0$, $\nabla = (\partial_1,\partial_2,\partial_3)$. All fields are smooth and either decay at spatial infinity or are periodic on a box $V = L_1L_2L_3$; all integrals are over that box.

Fields: a complex scalar $\varphi$; a scalar potential $A^0$; a vector potential $\mathbf{A} = (A_1,A_2,A_3)$, the covariant spatial components as in the source. The electric field is
$$\mathbf{E} \equiv \partial_0\mathbf{A} - \nabla A^0 ,$$
and $-\tfrac14 F_{\mu\nu}F^{\mu\nu} = \tfrac12(\mathbf{E}^2 - (\nabla\times\mathbf{A})^2)$.

Polar form: $\varphi = \sqrt{\rho}\,e^{i\beta}$ with $\rho = |\varphi|^2 \ge 0$. The quanta of $\varphi$ carry charge $-e$. Velocity field:
$$\boldsymbol{\mathcal V} \equiv \frac{\nabla\beta - e\mathbf{A}}{m}. \qquad (0.1)$$
Constants: $m > 0$ (mass), $e > 0$ (coupling), $U(\mathbf{x})$ a real potential, $\rho_b(\mathbf{x}) \ge 0$ a fixed background charge density. The source takes $\rho_b \equiv 0$; we keep it as a parameter because several results turn on it.

Notation for the plasma frequency: for a mean number density $\bar n = N/V$,
$$\omega_p^2 \equiv \frac{e^2 \bar n}{m}. \qquad (0.2)$$

---

## 1. The model

**Definition 1.1 (Lagrangian).**
$$\mathcal L = \tfrac12\left(\mathbf{E}^2 - (\nabla\times\mathbf{A})^2\right) - \rho_b A^0 + \varphi^*\left(i\partial_0 + eA^0\right)\varphi - \frac{1}{2m}\left|(\nabla - ie\mathbf{A})\varphi\right|^2 - U|\varphi|^2 . \qquad (1.1)$$
With $\rho_b = 0$ this is (A1) up to a total derivative.

**Proposition 1.2 (Field equations).** The Euler–Lagrange equations of (1.1) are
$$\text{(M)}\quad (i\partial_0 + eA^0)\varphi = -\frac{1}{2m}(\nabla - ie\mathbf{A})^2\varphi + U\varphi ,$$
$$\text{(G)}\quad \nabla\cdot\mathbf{E} = \rho_b - e\rho ,$$
$$\text{(A)}\quad \partial_0\mathbf{E} = \nabla^2\mathbf{A} - \nabla(\nabla\cdot\mathbf{A}) + e\rho\,\boldsymbol{\mathcal V} .$$
Every solution of (M) satisfies the continuity equation
$$\text{(C)}\quad \partial_0\rho = -\nabla\cdot(\rho\,\boldsymbol{\mathcal V}).$$

*Proof.* Variation in $\varphi^*$ gives (M). Variation in $A^0$: $\partial\mathcal L/\partial A^0 = -\rho_b + e\rho$ and $\partial\mathcal L/\partial(\partial_iA^0) = -E_i$, so $\nabla\cdot\mathbf{E} = \rho_b - e\rho$. Variation in $A_i$: $\partial\mathcal L/\partial A_i = \frac{e}{m}\rho(\partial_i\beta - eA_i) = e\rho\mathcal V_i$ (expand $|(\nabla - ie\mathbf{A})\varphi|^2$ and use $\operatorname{Im}(\varphi^*\partial_i\varphi) = \rho\,\partial_i\beta$), $\partial\mathcal L/\partial(\partial_0A_i) = E_i$, $\partial\mathcal L/\partial(\partial_jA_i) = -(\partial_jA_i - \partial_iA_j)$; the Euler–Lagrange equation is $\partial_0E_i - \partial_j(\partial_jA_i - \partial_iA_j) = e\rho\mathcal V_i$, which is (A). For (C), multiply (M) by $\varphi^*$, subtract the conjugate, and take the imaginary part; the computation is the imaginary part of Theorem 4.1. $\blacksquare$

**Theorem 1.3 (Gauss's law propagates).** Let $G \equiv \nabla\cdot\mathbf{E} - \rho_b + e\rho$. For every solution of (M) and (A), $\partial_0 G = 0$. Hence (G) holds for all times if it holds at one time.

*Proof.* $\partial_0\nabla\cdot\mathbf{E} = \nabla\cdot\left(\nabla^2\mathbf{A} - \nabla\nabla\cdot\mathbf{A}\right) + e\nabla\cdot(\rho\boldsymbol{\mathcal V}) = 0 - e\,\partial_0\rho$ by (C). $\blacksquare$

This is the content of (A5)–(A7). The source then sets the "time-independent term" to zero, which is the choice of imposing (G) at $x^0 = 0$.

**Theorem 1.4 (The pair $A^0 = 0$, $\nabla\cdot\mathbf{A} = 0$ freezes the density).** Suppose $A^0 \equiv 0$ and $\nabla\cdot\mathbf{A} \equiv 0$. Then $\nabla\cdot\mathbf{E} \equiv 0$, hence
$$\partial_0\rho \equiv 0 ,$$
and if (G) holds, $e\rho \equiv \rho_b$. In particular, with $\rho_b = 0$ and (G), $\varphi \equiv 0$.

*Proof.* $\nabla\cdot\mathbf{E} = \partial_0\nabla\cdot\mathbf{A} - \nabla^2A^0 = 0$. Theorem 1.3 gives $\partial_0(e\rho) = -\partial_0 G = 0$. $\blacksquare$

The source calls this pair "the Coulomb gauge" (before (A2)). It is not a gauge: a gauge choice removes one function, and this pair removes two. It is a restriction on solutions, and Theorem 1.4 says which: those with time-independent density.

**Theorem 1.5 (Coulomb gauge, consistent form).** On $\mathbb{R}^3$ with decaying fields impose $\nabla\cdot\mathbf{A} = 0$ and define $A^0$ by the Poisson equation
$$-\nabla^2A^0 = \rho_b - e\rho , \qquad A^0 = \frac{1}{4\pi}\int\frac{\rho_b(\mathbf{y}) - e\rho(\mathbf{y})}{|\mathbf{x}-\mathbf{y}|}\,d^3y . \qquad (1.2)$$
Then (G) holds identically, the longitudinal part of (A) is equivalent to (C), and the transverse part of (A) is
$$\partial_0^2\mathbf{A} = \nabla^2\mathbf{A} + \left(e\rho\,\boldsymbol{\mathcal V}\right)_T , \qquad (1.3)$$
where $(\cdot)_T$ is the divergence-free projection. The system (M), (1.2), (1.3) is the model with no restriction on solutions.

*Proof.* With $\nabla\cdot\mathbf{A} = 0$, $\nabla\cdot\mathbf{E} = -\nabla^2A^0$, so (1.2) is (G). Take the divergence of (A): $-\partial_0\nabla^2A^0 = e\nabla\cdot(\rho\boldsymbol{\mathcal V})$, which by (1.2) is $\partial_0(\rho_b - e\rho) = e\nabla\cdot(\rho\boldsymbol{\mathcal V})$, i.e. (C). The transverse part of (A) with $\mathbf{E} = \partial_0\mathbf{A} - \nabla A^0$ is (1.3). $\blacksquare$

On a periodic box, (1.2) is solvable only if $\int(\rho_b - e\rho) = 0$: the box must be neutral. With $\rho_b = 0$ this forces $N = 0$. A neutralizing background is therefore not optional on a torus.

**Proposition 1.6 (The price of the repair).** Under Theorem 1.5, equation (M) carries the term $eA^0$ with $A^0$ given by (1.2). Let $\delta \equiv \sup|\rho_b - e\rho|$ on the support.

(a) Slab: if $\rho_b - e\rho$ depends on $x^3$ only and vanishes outside $|x^3| \le L_3/2$, then $A^0$, normalized to vanish on the two faces, satisfies $\sup|A^0| \le \delta L_3^2/8$.

(b) Ball: if it vanishes outside a ball of radius $a$, then $\sup|A^0| \le \delta a^2/2$.

An additive constant in $A^0$ shifts every level equally; the oscillation of $A^0$ over the support is what shifts them differently, and it is bounded by the same numbers. Consequently the single-particle levels used in Section 2 are shifted relative to one another by at most $e\sup|A^0|$, and the two-level reduction there requires
$$e\sup|A^0| \ll \Omega . \qquad (1.4)$$
With $\rho_b = 0$ (the source) and $\rho \approx \bar n$, (a) reads $e^2\bar n L_3^2/8 = m\,\omega_p^2 L_3^2/8 \ll \Omega$.

*Proof.* (a) The one-dimensional problem $-f'' = q$ on $[-L/2, L/2]$ with $|q| \le \delta$ and $f(\pm L/2) = 0$ satisfies $|f| \le \delta(L^2/4 - x^2)/2 \le \delta L^2/8$ by comparison with $q \equiv \pm\delta$. (b) $|A^0(\mathbf{x})| \le \frac{\delta}{4\pi}\int_{|\mathbf{y}|\le a}\frac{d^3y}{|\mathbf{x}-\mathbf{y}|} \le \frac{\delta}{4\pi}\int_{|\mathbf{y}|\le a}\frac{d^3y}{|\mathbf{y}|} = \delta a^2/2$ (the integral is maximal at the centre). $\blacksquare$

---

## 2. Two-level emitter and the pulse

**Hypotheses.**

- **H2.1 (two levels).** $-\nabla^2/2m + U$ has real normalized eigenfunctions $\phi_0, \phi_1$ with eigenvalues $E_0 < E_1$; $\Omega \equiv E_1 - E_0$; and $\varphi(x) = \sum_{n=0,1} e^{-iE_nx^0}\chi_n(x^0)\phi_n(\mathbf{x})$ with $|\chi_0|^2 + |\chi_1|^2 = N$. On a set where $\phi_0 \ne 0$, the ratio $\phi_1/\phi_0$ takes at least three values.
- **H2.2 (emission geometry).** $\mathbf{A} = A_3(x^0,x^1,x^2)\,\hat{\mathbf{e}}_3$ and $A^0 = 0$. (This is the pair of Theorem 1.4; see Theorem 2.9.)
- **H2.3 (resonant shell).** $A_3 = \int\frac{d^2k}{(2\pi)^2}\,\tfrac12\left[\alpha_{\mathbf{k}}e^{-i(\omega_kx^0 - \mathbf{k}\cdot\mathbf{x})} + \text{c.c.}\right]$ with $\mathbf{k} = (k^1,k^2,0)$ and $\omega_k^2 = |\mathbf{k}|^2 + \omega_p^2$; only the modes with $\omega_k = \Omega$ are kept. This requires
$$\Omega^2 \ge \omega_p^2 . \qquad (2.0)$$
The shell measure is $\Omega^2/4\pi$ (this is (A29)); $\mathcal A \equiv \int_{\omega_k = \Omega}\alpha_{\mathbf{k}}$, made real by a constant phase.
- **H2.4 (slow envelopes).** $|\partial_0\chi_n| \le \varepsilon\,\Omega\,|\chi_n|$ with $\varepsilon < \tfrac12$, and $|\partial_0\alpha_{\mathbf k}| \ll \Omega|\alpha_{\mathbf k}|$.
- **H2.5 (dipole).** $e^{i\mathbf{k}\cdot\mathbf{x}} \simeq 1$ on the support of $\phi_n$: $L_1, L_2 \ll 2\pi/\sqrt{\Omega^2 - \omega_p^2}$.

The source states (2.0) as $\Omega \ge e^2|\bar\varphi|^2/m$ (after (A29) and (A47)); the two sides have different dimensions, and (2.0) is the condition under which the shell in (A29) exists.

**Definition 2.2 (Reduced model).** Let $d \equiv \frac1m\int\phi_0\,\partial_3\phi_1 \in \mathbb{R}$, $g \equiv ed/2$, $\kappa \equiv \dfrac{g\Omega}{4\pi L_3}$. The reduced model is
$$\dot\chi_0 = g\mathcal A\chi_1, \qquad \dot\chi_1 = -g\mathcal A\chi_0, \qquad \dot{\mathcal A} = \kappa R, \qquad R \equiv 2\operatorname{Re}(\chi_0^*\chi_1). \qquad (2.1)$$

Under H2.1–H2.5, equations (M) and (A) reduce to (2.1); this is (A14)–(A35) with the misprint in (A31) ($\chi_1$ for $\chi_0$) corrected and the phase of $\mathcal A$ fixed. We take (2.1) as the definition and prove everything below from it.

**Proposition 2.3 (Invariants).** Along (2.1), with $Z \equiv |\chi_1|^2 - |\chi_0|^2$,
$$N = |\chi_0|^2 + |\chi_1|^2, \qquad I \equiv \operatorname{Im}(\chi_0^*\chi_1), \qquad \mathcal E \equiv \tfrac12\mathcal A^2 + \frac{\Omega}{8\pi L_3}Z$$
are constant, and $Z^2 + R^2 = N^2 - 4I^2$.

*Proof.* $\dot Z = -2g\mathcal A R$, $\dot R = 2g\mathcal A Z$, $\frac{d}{dt}(\chi_0^*\chi_1) = g\mathcal A(|\chi_1|^2 - |\chi_0|^2) = g\mathcal A Z$ is real, so $\dot I = 0$; $\dot N = 2\operatorname{Re}(\chi_0^*\dot\chi_0 + \chi_1^*\dot\chi_1) = 2g\mathcal A\operatorname{Re}(\chi_0^*\chi_1 - \chi_1^*\chi_0) = 0$; $\dot{\mathcal E} = \kappa\mathcal A R - \frac{\Omega}{8\pi L_3}2g\mathcal AR = 0$. Finally $R^2 + 4I^2 = 4|\chi_0|^2|\chi_1|^2$ and $Z^2 + 4|\chi_0|^2|\chi_1|^2 = N^2$. $\blacksquare$

Put $N' \equiv \sqrt{N^2 - 4I^2}$ and, for $N' > 0$, define $\theta$ by $Z = N'\cos\theta$, $R = N'\sin\theta$. Then $\dot\theta = 2g\mathcal A$, which is (A40). For real initial data $I = 0$ and $N' = N$.

**Theorem 2.4 (Pendulum).** $\theta$ obeys
$$\ddot\theta = \omega_c^2\sin\theta, \qquad \omega_c^2 \equiv 2g\kappa N' = \frac{g^2\Omega N'}{2\pi L_3}. \qquad (2.2)$$
Equivalently $\psi \equiv \theta - \pi$ is a pendulum, $\ddot\psi = -\omega_c^2\sin\psi$. The state $\theta = 0$ (all quanta in the upper level, $Z = N'$) is the unstable equilibrium; $\theta = \pi$ is the stable one.

*Proof.* $\ddot\theta = 2g\dot{\mathcal A} = 2g\kappa R = 2g\kappa N'\sin\theta$. $\blacksquare$

**Theorem 2.5 (Lossless dynamics: no emission, a periodic train).** Let $\mathcal A(0) = 0$ and $\theta(0) = \theta_0 \in (0,\pi)$. Then

(i) $\theta$ oscillates between $\theta_0$ and $2\pi - \theta_0$ with period
$$T(\theta_0) = \frac{4}{\omega_c}K\!\left(\cos\tfrac{\theta_0}{2}\right), \qquad K(k) = \int_0^{\pi/2}\frac{d\phi}{\sqrt{1 - k^2\sin^2\phi}}; \qquad (2.3)$$

(ii) $\mathcal A(t) = \dfrac{\dot\theta}{2g}$ satisfies $|\mathcal A| \le \dfrac{\omega_c}{g}\cos\dfrac{\theta_0}{2}$, with equality at $\theta = \pi$, and $\mathcal A$ returns to $0$ every half period;

(iii) as $\theta_0 \downarrow 0$, $T(\theta_0) = \dfrac{4}{\omega_c}\ln\dfrac{8}{\theta_0} + o(1) \to \infty$, and each pulse of the train converges to
$$\mathcal A(t) = \frac{\omega_c}{g}\operatorname{sech}\!\big(\omega_c(t - t_1)\big). \qquad (2.4)$$

*Proof.* Multiply (2.2) by $\dot\theta$: $\tfrac12\dot\theta^2 + \omega_c^2\cos\theta = \omega_c^2\cos\theta_0$. The potential $\omega_c^2\cos\theta$ has its maximum $\omega_c^2$ at $\theta = 0$, so the orbit is a libration about $\theta = \pi$ with turning points where $\cos\theta = \cos\theta_0$, i.e. $\theta_0$ and $2\pi - \theta_0$. In the variable $\psi = \theta - \pi$ this is the pendulum of amplitude $\pi - \theta_0$, whose period is $\frac{4}{\omega_c}K(\sin\frac{\pi - \theta_0}{2}) = \frac{4}{\omega_c}K(\cos\frac{\theta_0}{2})$. At $\theta = \pi$, $\dot\theta^2 = 2\omega_c^2(1 + \cos\theta_0) = 4\omega_c^2\cos^2\frac{\theta_0}{2}$, giving (ii). For (iii), $K(k) = \ln\frac{4}{\sqrt{1-k^2}} + o(1)$ as $k \uparrow 1$ and $\sqrt{1 - \cos^2\frac{\theta_0}{2}} = \sin\frac{\theta_0}{2}$; on the separatrix ($\theta_0 = 0$) the energy integral reads $\dot\theta = 2\omega_c\sin\frac{\theta}{2}$, whose solution is $\tan\frac{\theta}{4} = e^{\omega_c(t - t_1)}$, and $\sin\frac{\theta}{2} = \operatorname{sech}\,\omega_c(t - t_1)$. $\blacksquare$

So the lossless reduced model has a hyperbolic-secant pulse, but as the limit of a periodic train whose period diverges logarithmically in the seed; and $\mathcal E$ is conserved, so nothing is emitted: the field returns its energy to the matter every half period. A single emitted pulse requires an energy sink.

**H2.6 (loss).** Radiation leaves the slab at rate $1/L_3$:
$$\dot{\mathcal A} = \kappa R - \frac{\mathcal A}{L_3}. \qquad (2.5)$$
This is (A42). It is a model of escape, not a consequence of (1.1).

**Theorem 2.6 (Overdamped limit: the single pulse).** Put $\tau_R \equiv \dfrac{2\pi}{g^2\Omega N'}$, so that $\omega_c^2 = \dfrac{1}{\tau_R L_3}$. If
$$L_3 \ll \tau_R , \qquad (2.6)$$
then on times $x^0 \gg L_3$ the solution of (2.1) with (2.5) is, to leading order in $L_3/\tau_R$,
$$\mathcal A = \kappa L_3 N'\sin\theta, \qquad \dot\theta = \frac{\sin\theta}{\tau_R}, \qquad \theta(x^0) = 2\arctan\!\Big(e^{x^0/\tau_R}\tan\frac{\theta_0}{2}\Big), \qquad (2.7)$$
$$\mathcal A(x^0) = \frac{g\Omega N'}{4\pi}\operatorname{sech}\frac{x^0 - \tau_0}{\tau_R}, \qquad \tau_0 = -\tau_R\ln\tan\frac{\theta_0}{2}. \qquad (2.8)$$
Here $\theta$ increases monotonically from $\theta_0$ to $\pi$: the pulse is emitted once and the energy $\mathcal E$ decreases by the amount that leaves through the loss term.

*Proof.* With $\dot{\mathcal A} = O(\mathcal A/\tau_R)$ and $1/L_3 \gg 1/\tau_R$, (2.5) gives $\mathcal A = \kappa L_3 N'\sin\theta\,(1 + O(L_3/\tau_R))$. Then $\dot\theta = 2g\mathcal A = 2g\kappa L_3 N'\sin\theta = \sin\theta/\tau_R$, which integrates to (2.7); differentiating, $\mathcal A = \dot\theta/2g = \frac{1}{2g\tau_R}\sin\theta$ and $\sin\theta = \operatorname{sech}((x^0 - \tau_0)/\tau_R)$ with $\tau_0$ as stated. Monotonicity: $\sin\theta > 0$ on $(0,\pi)$. $\blacksquare$

(2.8) is (A45)–(A47). The width $\tau_R$ is independent of $L_3$ only inside the regime (2.6); outside it the width is $1/\omega_c = \sqrt{\tau_R L_3}$ of Theorem 2.5. Both regimes have the shape $\operatorname{sech}$; the shape does not identify the regime, the width does.

**Corollary 2.7 (Every pulse needs a seed).** $\theta_0 = 0$, $\mathcal A = 0$ is a stationary solution of (2.1), of (2.1)+(2.5), and of (2.7). The delay $\tau_0 \to +\infty$ and the period $T \to \infty$ as $\theta_0 \downarrow 0$. No equation of Sections 1–2 produces $\theta_0 \ne 0$; it is a hypothesis.

**H2.7 (seed).** $\theta_0 \in (0,\pi)$ is given.

The source uses $\theta_0$ in (A41), (A44), (A47) and writes "definition of $\theta_0$ is in Appendix A"; no definition is there.

**Proposition 2.8 (A frozen density has no coherence).** Assume H2.1 and H2.4. If $\partial_0\rho \equiv 0$, then $\chi_0^*\chi_1 \equiv 0$; hence $R \equiv 0$, $\mathcal A$ is constant, and no pulse exists.

*Proof.* With real $\phi_n$,
$$\rho = |\chi_0|^2\phi_0^2 + |\chi_1|^2\phi_1^2 + 2\phi_0\phi_1\operatorname{Re}\!\left(\chi_0^*\chi_1 e^{-i\Omega x^0}\right).$$
Dividing by $\phi_0^2$ on the set of H2.1, $\rho/\phi_0^2$ is a quadratic polynomial in $s = \phi_1/\phi_0$ with coefficients $|\chi_0|^2$, $2\operatorname{Re}(\chi_0^*\chi_1e^{-i\Omega x^0})$, $|\chi_1|^2$; a quadratic constant in time at three values of $s$ has time-independent coefficients. So $|\chi_0|$, $|\chi_1|$ are constant and $\operatorname{Re}(c\,e^{-i\Omega x^0})$ is constant, where $c \equiv \chi_0^*\chi_1$ has constant modulus. If $c \ne 0$ write $c = |c|e^{i\eta}$: $\cos(\eta - \Omega x^0)$ constant forces $\dot\eta = \Omega$, so $|\dot c| = \Omega|c|$. But $|\dot c| \le |\dot\chi_0||\chi_1| + |\chi_0||\dot\chi_1| \le 2\varepsilon\Omega|c| < \Omega|c|$ by H2.4. Hence $c = 0$. $\blacksquare$

**Theorem 2.9 (Appendix A, as written, has no pulse; the repair and its price).** H2.2 places the system under Theorem 1.4 with $\rho_b = 0$: the density is frozen. By Proposition 2.8 the coherence vanishes and (2.8) cannot occur. The pulse (2.8) is a theorem of the reduced model (2.1)+(2.5)+H2.7. The reduced model follows from (1.1) only after replacing H2.2 by Theorem 1.5 (Coulomb gauge with $A^0$ from (1.2)), and then only under the smallness condition (1.4), which with $\rho_b = 0$ is $e^2\bar nL_3^2/8 \ll \Omega$.

*Proof.* Theorems 1.4, 1.5, Propositions 1.6, 2.8. $\blacksquare$

**Proposition 2.10 (Transverse current).** H2.2 also sets the $x^1, x^2$ components of (A) to zero, which by (A) requires $\rho\,\partial_{1,2}\beta = 0$. Under H2.1 and H2.4, if $\phi_1/\phi_0$ depends on $x^1$ or $x^2$, this forces $\chi_0^*\chi_1 = 0$.

*Proof.* With $s = \phi_1/\phi_0$ and $w = e^{-i\Omega x^0}$, $\beta = -E_0x^0 + \arg(\chi_0 + w\chi_1 s)$ up to a constant, so $\partial_{1,2}\beta = \operatorname{Im}(w\chi_0^*\chi_1)\,\partial_{1,2}s/|\chi_0 + w\chi_1s|^2$. If $\partial_{1,2}s \ne 0$ somewhere, $\operatorname{Im}(e^{-i\Omega x^0}\chi_0^*\chi_1) \equiv 0$ there, and the argument of Proposition 2.8 gives $\chi_0^*\chi_1 = 0$. $\blacksquare$

The source's hypothesis that $\nabla_3$ dominates ((A10)) is the case $\phi_1/\phi_0 = f(x^3)$, in which the transverse current vanishes identically and only Theorem 2.9 remains.

**Proposition 2.11 (What decides whether a pulse occurs).** The reduced model has the parameters $g, \Omega, N', L_3, \theta_0$ and, for the pulse to be observed before the phases of the $N'$ emitters randomize, a dephasing time $T_2$ with
$$\tau_R = \frac{2\pi}{g^2\Omega N'} < T_2 , \qquad L_3 \ll \tau_R , \qquad \Omega^2 \ge \omega_p^2 , \qquad e^2\bar nL_3^2 \ll 8\Omega . \qquad (2.9)$$
The source gives no values for $g, N', L_3, \theta_0$ or $T_2$, and for $\Omega$ only the order of magnitude of a water rotational spacing ($4$ meV, its Section 1). Whether (2.9) holds in any medium is therefore open, and the source's own discussion ("the balance of decoherence and error corrections … in the open system") names the computation it does not perform.

---

## 3. Screened waves, holographic readout, capacity

**Hypotheses.**

- **H3.1 (static neutral medium).** $\rho = \rho(\mathbf{x})$, $\boldsymbol{\mathcal V} \equiv 0$, $\rho_b = e\rho$. Then Theorem 1.4 permits $A^0 = 0$, $\nabla\cdot\mathbf{A} = 0$ consistently: a static medium is the one case in which the pair of H2.2 is harmless.
- **H3.2 (screening and source).** Equation (A) acquires a term $-M^2\mathbf{A}$ with a supplied constant $M^2 \ge 0$, and a supplied external field enters as $M^2\tilde{\mathbf{A}}$.
- **H3.3 (polarization).** $\mathbf{A} = A_3\hat{\mathbf{e}}_3$, $\tilde{\mathbf{A}} = \tilde A_3\hat{\mathbf{e}}_3$, both independent of $x^3$, so $\nabla\cdot\mathbf{A} = 0$.

**Definition 3.1 (Screened wave equation).**
$$\left[\partial_0^2 - \nabla^2 + \omega_p^2(\mathbf{x}) + M^2\right]A_3 = M^2\tilde A_3, \qquad \omega_p^2(\mathbf{x}) \equiv \frac{e^2\rho(\mathbf{x})}{m}. \qquad (3.1)$$
This is (A48) with its remainder $O(\partial\varphi)$ equal to zero under H3.1.

**Theorem 3.2 (Transmittance).** Let $\tilde A_3 = b\,e^{i(k^0x^0 - \mathbf{k}\cdot\mathbf{x})}$ with $k^0 = |\mathbf{k}|$ and $\mathbf{k}\perp\hat{\mathbf{e}}_3$. Put
$$T(\mathbf{x}) \equiv \frac{M^2}{M^2 + \omega_p^2(\mathbf{x})}. \qquad (3.2)$$
Then $A_3 = T\tilde A_3$ satisfies (3.1) with the source replaced by $M^2\tilde A_3 + \mathcal R$, where
$$\mathcal R = \left(2i\,\mathbf{k}\cdot\nabla T - \nabla^2T\right)\tilde A_3 . \qquad (3.3)$$

*Proof.* $(\partial_0^2 - \nabla^2)(T\tilde A_3) = T(-k_0^2 + |\mathbf{k}|^2)\tilde A_3 - 2\nabla T\cdot\nabla\tilde A_3 - (\nabla^2T)\tilde A_3 = 2i(\mathbf{k}\cdot\nabla T)\tilde A_3 - (\nabla^2T)\tilde A_3$, and $(\omega_p^2 + M^2)T = M^2$. $\blacksquare$

$\mathcal R$ is small when $T$ varies slowly on the scale $1/|\mathbf{k}|$; (A49) is Theorem 3.2 with $\mathcal R$ dropped.

**Corollary 3.3 (The medium is seen only through $s$).** With $s(\mathbf{x}) \equiv \omega_p^2(\mathbf{x})/M^2$: if $M^2 = 0$ then $T \equiv 0$ and $\mathcal R \equiv 0$, so the external wave does not enter the medium at all; as $M^2 \to \infty$, $T \to 1$; and for $s < 1$,
$$T = 1 - s + s^2 - \cdots . \qquad (3.4)$$

**H3.4 (recorded pattern).** On the recording plane, $\rho(x^1,x^2) = c\,|r(x^1,x^2) + o(x^1,x^2)|^2$ with $c > 0$, $r$ a reference wave and $o$ an object wave, and $\tilde A_3 = r$.

**Theorem 3.4 (Reconstruction identity).** Under H3.1–H3.4, to first order in $s$,
$$A_3 - \tilde A_3 = -\sigma\Big[(|r|^2 + |o|^2)\,r \;+\; |r|^2\,o \;+\; r^2\,o^*\Big] + O(s^2), \qquad \sigma \equiv \frac{c\,e^2}{mM^2}. \qquad (3.5)$$
The third term is the object wave multiplied by $|r|^2$; the fourth is its conjugate (the twin image); and the third has amplitude at most $s_r|o|$ with $s_r \equiv \sigma\sup|r|^2$.

*Proof.* (3.4) gives $A_3 - \tilde A_3 = -s\,r + O(s^2)$ with $s = \sigma|r + o|^2 = \sigma(|r|^2 + |o|^2 + r^*o + ro^*)$; multiply by $r$. $\blacksquare$

This is (A52), which prints $\tilde A_i$ on the left for $A_i$. Nothing selects the third term over the fourth; that is the ordinary twin-image problem of in-line holography.

**Corollary 3.5 (Numbers).** At the source's Section 4 values, $e = 0.3$, $\rho = m^3$ (its $|\bar\varphi|^2 = 1$ in units of $m$) and $M^2 = 2m^2$: $s = e^2\rho/(mM^2) = 0.045$. The reconstructed object wave carries at most $s_r \approx 0.045$ of the object's amplitude: $4.5\%$, at the only parameter values the source gives.

**Remark 3.6 (No write).** In Definition 3.1 the density $\rho$ is data. No equation of Sections 1–3 changes $\rho$ (H3.1 sets $\boldsymbol{\mathcal V} = 0$), and no equation contains $o$ except through H3.4. The pattern $|r + o|^2$ is assumed, not produced, and $o$ has no source.

**Lemma 3.7 (Cell count).** Partition a region of area $S$ and thickness $d$ into cells of lateral side $\ell_\parallel$ and depth $\ell_\perp$. The number of cells is
$$C = \frac{S\,d}{\ell_\parallel^2\,\ell_\perp}. \qquad (3.6)$$
With the convention $\ell_\parallel = \lambda/2$, $\ell_\perp = \lambda/n_r$ (the source's, after its reference for the $2$-dimensional limit $4/\lambda^2$), $C_3 = 4n_rSd/\lambda^3$, and the surface alone holds $C_2 = 4S/\lambda^2$; their ratio is
$$\frac{C_3}{C_2} = \frac{n_r d}{\lambda}. \qquad (3.7)$$

**Proposition 3.8 (The petabyte is the thickness factor).** With $n_r = 1.3$, $d = 2\,\mathrm{mm}$, $\lambda = 500\,\mathrm{nm}$, $S = 2500\,\mathrm{cm}^2$:
$$C_2 = 4.0\times10^{12} \;(0.5\ \mathrm{TB}), \qquad \frac{n_rd}{\lambda} = 5200, \qquad C_3 = 2.08\times10^{16}\;(2.6\ \mathrm{PB}).$$
At $\lambda = 1500\,\mathrm{nm}$, $C_3 = 0.096\ \mathrm{PB}$; at $\lambda = 310\,\mu\mathrm{m}$ (the wavelength of the $4\ \mathrm{meV}$ scale the source quotes for water), $C_3 = 8.7\times10^7$ bits (11 MB). The comparison figure $250\times10^{12}$ synapses $\times\,1$ bit is $31$ TB; at $4.7$ bits per synapse it is $147$ TB.

One cell is one bit only under the hypothesis **H3.5**: a write and a read exist that set and recover one bit per cell. Neither is given (Remark 3.6).

**Lemma 3.9 (Erasure bound versus retention).** The Landauer bound $k_BT\ln2$ is a lower bound on the heat released by one logically irreversible erasure. It is not a bound on how long a stored value persists. For a two-state cell separated by a barrier $\Delta E$ with attempt time $\tau_a$, the Arrhenius lifetime is $\tau = \tau_a e^{\Delta E/k_BT}$, so retention for a time $\tau_{\rm ret}$ needs
$$\Delta E \ge k_BT\ln\frac{\tau_{\rm ret}}{\tau_a}. \qquad (3.8)$$

**Proposition 3.10 (Numbers).** At $T = 310\,\mathrm{K}$, $k_BT = 26.7\ \mathrm{meV}$ and $k_BT\ln2 = 18.5\ \mathrm{meV}$ (the source rounds to 20). With $\tau_a = 1\ \mathrm{ps}$: $\tau_{\rm ret} = 1\ \mathrm{s}$ needs $\Delta E \ge 0.74\ \mathrm{eV}$; $1$ hour, $0.96\ \mathrm{eV}$; $1$ year, $1.20\ \mathrm{eV}$. The photon energy $2.4\ \mathrm{eV}$ at $500\,\mathrm{nm}$ is not a barrier of the medium; no barrier is given. The "maximum wavelength $60\ \mu\mathrm{m}$" is $hc/(k_BT\ln2)$: $67\ \mu\mathrm{m}$, or $62\ \mu\mathrm{m}$ with the rounded $20$ meV. It is a conversion of units, not a property of the medium.

---

## 4. Driven density patterns: the classical sector

**Theorem 4.1 (Polar form).** On any region where $\rho > 0$, equation (M) is equivalent to the pair
$$\text{(C)}\quad \partial_0\rho = -\nabla\cdot(\rho\boldsymbol{\mathcal V}), \qquad \text{(B)}\quad eA^0 - \partial_0\beta = -\frac{\nabla^2\sqrt\rho}{2m\sqrt\rho} + \frac{m}{2}\boldsymbol{\mathcal V}^2 + U .$$

*Proof.* With $D \equiv \nabla - ie\mathbf{A}$ and $\varphi = \sqrt\rho e^{i\beta}$: $D\varphi = e^{i\beta}(\nabla\sqrt\rho + im\sqrt\rho\,\boldsymbol{\mathcal V})$ and
$$D^2\varphi = e^{i\beta}\left[\nabla^2\sqrt\rho - m^2\boldsymbol{\mathcal V}^2\sqrt\rho + im\left(\nabla\cdot(\sqrt\rho\,\boldsymbol{\mathcal V}) + \boldsymbol{\mathcal V}\cdot\nabla\sqrt\rho\right)\right].$$
(M) reads $e^{i\beta}[i\partial_0\sqrt\rho - \sqrt\rho\,\partial_0\beta + eA^0\sqrt\rho] = -\frac{1}{2m}D^2\varphi + U\sqrt\rho e^{i\beta}$. The imaginary part is $\partial_0\sqrt\rho = -\frac12(\nabla\cdot(\sqrt\rho\boldsymbol{\mathcal V}) + \boldsymbol{\mathcal V}\cdot\nabla\sqrt\rho)$, which times $2\sqrt\rho$ is (C). The real part divided by $\sqrt\rho$ is (B). $\blacksquare$

(B) is (A70) with the sign of the $\boldsymbol{\mathcal V}^2$ term corrected: the source prints $-\frac{e}{2m}(A_i - \partial_i\beta/e)^2$, while (A81) and (A87), and the derivation, carry $+$. A free plane wave satisfies (B) and not the printed form.

**Lemma 4.2 (Unitary gauge).** If $\rho > 0$ everywhere, the gauge transformation $\varphi \to e^{-i\beta}\varphi$, $A^0 \to A^0 - \partial_0\beta/e$, $\mathbf{A} \to \mathbf{A} - \nabla\beta/e$ sets $\beta \equiv 0$. In this gauge $\boldsymbol{\mathcal V} = -e\mathbf{A}/m$ and (B) determines $A^0$:
$$eA^0 = -\frac{\nabla^2\sqrt\rho}{2m\sqrt\rho} + \frac{e^2}{2m}\mathbf{A}^2 + U . \qquad (4.1)$$

This is the source's "we omit terms $-\partial_\mu\beta/e$" (after (A81)); it is not an approximation but a gauge choice, and it is incompatible with any further condition on $A^0$ or $\nabla\cdot\mathbf{A}$. (4.1) with $U = 0$ is (A87).

**Hypotheses.**

- **H4.1 (planar).** $A_3 = 0$, nothing depends on $x^3$, $U = 0$.
- **H4.2 (supplied response).** The matter's back-reaction beyond mean field is replaced by $-M^2\mathbf{A} - \gamma\,\partial_0\mathbf{A}$ with supplied constants $M^2 \ge 0$, $\gamma \ge 0$. (This is (A75); the derivation from the self-energy is not reproduced here, and the constants are taken as data.)
- **H4.3 (layers).** Copies $n = 1,\dots,N$ of the fields, coupled by $v(\mathbf{A}^{(n-1)} + \mathbf{A}^{(n+1)})$ with a supplied constant $v$, a supplied drive $\mathbf{A}^{(0)}$, and $\mathbf{A}^{(N+1)} \equiv 0$.
- **H4.4 (constraint).** $A^{0(n)}$ is given by (4.1); equation (G) is not imposed.

**Definition 4.3 (Layer system).** For $n = 1,\dots,N$, with $E_i^{(n)} \equiv \partial_0A_i^{(n)} - \partial_iA^{0(n)}$:
$$\partial_0E_1^{(n)} = \partial_2^2A_1^{(n)} - \partial_1\partial_2A_2^{(n)} - \frac{e^2\rho^{(n)}}{m}A_1^{(n)} - M^2A_1^{(n)} - \gamma\,\partial_0A_1^{(n)} + v\big(A_1^{(n-1)} + A_1^{(n+1)}\big),$$
$$\partial_0E_2^{(n)} = \partial_1^2A_2^{(n)} - \partial_1\partial_2A_1^{(n)} - \frac{e^2\rho^{(n)}}{m}A_2^{(n)} - M^2A_2^{(n)} - \gamma\,\partial_0A_2^{(n)} + v\big(A_2^{(n-1)} + A_2^{(n+1)}\big),$$
$$\partial_0\rho^{(n)} = \frac{e}{m}\nabla\cdot\big(\rho^{(n)}\mathbf{A}^{(n)}\big), \qquad eA^{0(n)} = -\frac{\nabla^2\sqrt{\rho^{(n)}}}{2m\sqrt{\rho^{(n)}}} + \frac{e^2}{2m}\big(\mathbf{A}^{(n)}\big)^2 . \qquad (4.2)$$
This is (A82)–(A87). The source prints $e\rho/m$ for $e^2\rho/m$ in (A76) and (A78).

**Proposition 4.4 (The one quantum term).** Restoring $\hbar$, (4.1) reads $eA^0 = -\dfrac{\hbar^2\nabla^2\sqrt\rho}{2m\sqrt\rho} + \dfrac{e^2}{2m}\mathbf{A}^2$. Every other term of (4.2) is independent of $\hbar$. Setting that term to zero leaves a classical charged fluid: continuity, Ampère's law with the supplied $M^2, \gamma, v$, and the constraint $eA^0 = e^2\mathbf{A}^2/2m$.

*Proof.* Dimensional restoration of (B): $\boldsymbol{\mathcal V} = (\hbar\nabla\beta - e\mathbf{A})/m$ and the quantum pressure carries $\hbar^2$; in the unitary gauge no other $\hbar$ remains. $\blacksquare$

The source reports that this term produces "slight distortions" of Figure 6f and "does not seriously affect" the result. That is a statement that the simulation is insensitive to its only quantum term.

**Theorem 4.5 (Gauss's law drifts).** For a solution of (4.2) put $G^{(n)} \equiv \nabla\cdot\mathbf{E}^{(n)} - \rho_b + e\rho^{(n)}$. Then
$$\partial_0G^{(n)} = -\left(M^2 + \gamma\,\partial_0\right)\nabla\cdot\mathbf{A}^{(n)} + v\,\nabla\cdot\big(\mathbf{A}^{(n-1)} + \mathbf{A}^{(n+1)}\big). \qquad (4.3)$$
In particular $G^{(n)}$ is conserved if and only if the right side vanishes; for $M^2 = \gamma = v = 0$ it is conserved (Theorem 1.3).

*Proof.* Take the divergence of the first two equations of (4.2): $\nabla\cdot(\nabla^2\mathbf{A} - \nabla\nabla\cdot\mathbf{A}) = 0$; $-\frac{e^2}{m}\nabla\cdot(\rho\mathbf{A}) = -e\,\partial_0\rho$ by the third; $\nabla\cdot(\partial_0\mathbf{A}) = \partial_0\nabla\cdot\mathbf{A}$; the rest is (4.3). $\blacksquare$

For the targets (4.5) below, $\nabla\cdot\mathbf{A}_{\rm tgt} \ne 0$ on the interior, so $G^{(N)}$ drifts. A rerun of the simulation at the source's parameters (reported in the companion checks of this folder, not replayed here) finds $|\partial_0G^{(N)}|$ between $1.1$ and $2.3$ times $|\partial_0(e\rho^{(N)})|$ over the run: the quantity the simulation reports as the hologram and the violation of Gauss's law are of the same size. The source reports conservation of $\int\rho^{(N)}$ to $10^{-6}\,\%$; that is the third equation of (4.2) on a periodic box and is unrelated to (4.3).

**Theorem 4.6 (Inverse design is a Chebyshev recursion).** Drop time derivatives and the $e^2\rho/m$ term in (4.2) (as the source does), write $u^{(n)}$ for the static fields, and impose $u^{(N)} = \mathbf{A}_{\rm tgt}$, $u^{(N+1)} = 0$. Then
$$u_1^{(n-1)} = \frac{M^2u_1^{(n)} - \partial_2^2u_1^{(n)} + \partial_1\partial_2u_2^{(n)}}{v} - u_1^{(n+1)}, \qquad u_2^{(n-1)} = \frac{M^2u_2^{(n)} - \partial_1^2u_2^{(n)} + \partial_1\partial_2u_1^{(n)}}{v} - u_2^{(n+1)}. \qquad (4.4)$$
If $u_1^{(N)} = u_1(x^1)$ and $u_2^{(N)} = u_2(x^2)$, all derivative terms vanish and
$$u^{(N-J)} = U_J(c)\,u^{(N)}, \qquad c \equiv \frac{M^2}{2v}, \qquad U_0 = 1,\ U_1 = 2c,\ U_{J+1} = 2cU_J - U_{J-1}, \qquad (4.5)$$
with $U_J$ the Chebyshev polynomial of the second kind; for $c > 1$, $U_J(c) = \dfrac{\sinh((J+1)\eta)}{\sinh\eta}$, $c = \cosh\eta$.

*Proof.* The static, drive-free first equation of (4.2) at layer $n$ is $0 = \partial_2^2u_1^{(n)} - \partial_1\partial_2u_2^{(n)} - M^2u_1^{(n)} + v(u_1^{(n-1)} + u_1^{(n+1)})$; solve for $u_1^{(n-1)}$. For separable targets the recursion is $u^{(n-1)} + u^{(n+1)} = 2c\,u^{(n)}$ with $u^{(N+1)} = 0$, which is the defining recursion of $U_J$ in $J = N - n$. The closed form is the standard one. $\blacksquare$

The source's (A88) prints $-\partial_1^2u_1$ where (4.4) has $-\partial_2^2u_1$ (and symmetrically in (A89)); for its targets the difference is invisible because both vanish.

**Corollary 4.7 (The input amplitude).** With $N = 4$, $M^2/v = 2.5$ ($c = 1.25$) and target amplitude $0.1$: $U_4(1.25) = 21.3125$, so $\max|u^{(0)}| = 2.13$. The source's "$0.1\times(M^2/m^2)^4/v^N = 3.9$" is the recursion without the term $-u^{(n+1)}$; its Figure 4 shows "approximately 3". Keeping the $e^2\rho/m$ term, $c = (M^2 + \omega_p^2)/2v = 1.30625$, $U_4 = 27.11$ and $\max|u^{(0)}| = 2.71$.

**Targets** (the source's (10)–(11), in lattice units $x^i = n^ia_s$, $ma_s = 1$, $N_s = 64$, $N_1 = 30$, $N_2 = 20$):
$$A_{1,\rm tgt} = 0.1\,m\begin{cases}\dfrac{n^1 + N_s}{N_s - N_1} & n^1 \le -N_1\\[4pt] -\dfrac{n^1}{N_1} & |n^1| < N_1\\[4pt] \dfrac{n^1 - N_s}{N_s - N_1} & n^1 \ge N_1\end{cases}, \qquad A_{2,\rm tgt} \text{ likewise in } n^2 \text{ with } N_2 . \qquad (4.6)$$

**Theorem 4.8 (Linear response reproduces the reported depression).** Suppose the output layer field has fixed shape and a time-dependent amplitude, $\mathbf{A}^{(N)}(x^0,\mathbf{x}) = a(x^0)\,\mathbf{A}_{\rm tgt}(\mathbf{x})$, and write $\rho^{(N)} = \bar n(1 + \delta)$. To first order in $\delta$ and $\mathbf{A}$,
$$\delta(x^0,\mathbf{x}) = \frac{e}{m}\,\nabla\cdot\mathbf{A}_{\rm tgt}(\mathbf{x})\int_0^{x^0}a . \qquad (4.7)$$
For (4.6) on the central rectangle $|n^1| < N_1$, $|n^2| < N_2$, $\nabla\cdot\mathbf{A}_{\rm tgt} = -0.1\,m^2\left(\frac{1}{N_1} + \frac{1}{N_2}\right)$. With $a(x^0) = e^{-\gamma_2x^0}$ and the source's $e = 0.3$, $\gamma_2 = 0.01\,m$:
$$\delta_{\rm centre}(x^0) = -0.25\left(1 - e^{-0.01\,mx^0}\right). \qquad (4.8)$$

| $mx^0$ | 5 | 20 | 40 | 100 | 200 |
|---|---|---|---|---|---|
| (4.8) | $-1.2\%$ | $-4.5\%$ | $-8.2\%$ | $-15.8\%$ | $-21.6\%$ |
| source, Figure 6 | $-1.3\%$ | $-4.5\%$ | $-9.1\%$ | $-16\%$ | $-21\%$ |

*Proof.* Linearize the third equation of (4.2): $\partial_0\delta = \frac{e}{m}\nabla\cdot\mathbf{A}^{(N)} = \frac{e}{m}a(x^0)\nabla\cdot\mathbf{A}_{\rm tgt}$; integrate. On the central rectangle $\partial_1A_{1,\rm tgt} = -0.1m^2/N_1$, $\partial_2A_{2,\rm tgt} = -0.1m^2/N_2$. Then $\frac{e}{m}\cdot(-0.1m^2)(\tfrac1{30} + \tfrac1{20})\cdot\frac{1 - e^{-\gamma_2x^0}}{\gamma_2} = -\frac{0.3\cdot0.1}{12}\cdot100\,(1 - e^{-0.01mx^0})$. $\blacksquare$

**Corollary 4.9 (What the depression is).** By (4.7) the recorded quantity is the time integral of the divergence of the drive: the fluid moves with velocity $-e\mathbf{A}/m$ (Lemma 4.2) and the density follows. It is first order in $e$ and vanishes with the coupling. It is not binary: it is the continuous number (4.8). It does not stop; it slows because the drive decays, and the drive is still at $e^{-1} = 0.37$ of its initial amplitude at $mx^0 = 100$. Nothing in (4.2) restores or holds the pattern; the source's own remark that the velocity "is nonzero at later times" and that "charged bosons will collect into the peripheral regions" is the nonlinear continuation of (4.7).

A rerun of the simulation with the corrected input amplitude $2.13$ (reported in the companion checks of this folder) gives at $mx^0 = 20$ a central dip of $3.5\%$ at $e = 0.3$, $2.1\%$ at $e = 0.15$ and $1.1\%$ at $e = 0.075$: halving $e$ divides the dip by $1.7$ and then $1.9$, as first order in $e$ predicts once the relative size $\delta$ of the nonlinear terms is allowed for; a second-order dependence would divide it by $4$.

**Theorem 4.10 (Conservation on the box).** For (4.2) on a periodic box, $\int\rho^{(n)}$ is constant, and for (4.7), $\int\delta = 0$: the central depression is balanced by a rise outside. For (4.6) the rise in the corner region $|n^1| > N_1$, $|n^2| > N_2$ is $+0.156\,(1 - e^{-0.01mx^0})$, i.e. $+13.5\%$ at $mx^0 = 200$.

*Proof.* The third equation of (4.2) is a divergence; so is (4.7). On the corners $\nabla\cdot\mathbf{A}_{\rm tgt} = 0.1m^2(\frac{1}{N_s - N_1} + \frac{1}{N_s - N_2})$. $\blacksquare$

---

## 5. What the model establishes

**Theorem 5.1.** Under the hypotheses named, the model (1.1) yields exactly the following.

(i) *(Pulse.)* Under H2.1–H2.7 with H2.2 replaced by Theorem 1.5 and (1.4), the reduced model (2.1)+(2.5) emits one pulse $\mathcal A = \frac{g\Omega N'}{4\pi}\operatorname{sech}\frac{x^0 - \tau_0}{\tau_R}$, $\tau_R = 2\pi/(g^2\Omega N')$, provided $L_3 \ll \tau_R$; without the loss term it exchanges energy periodically with period (2.3); without the seed $\theta_0$ nothing happens. The parameters $g, \Omega, N', L_3, \theta_0, T_2$ are not specified.

(ii) *(Readout.)* Under H3.1–H3.4, a static neutral medium whose density is $c|r + o|^2$ transmits a reference wave $r$ with the object wave present at amplitude at most $s_r = \sigma\sup|r|^2 \approx \omega_p^2/M^2$ times the object's ($0.045$ at the source's values), together with the twin image. The density pattern is assumed; no write exists.

(iii) *(Count.)* A $2\,\mathrm{mm}$ slab of index $1.3$ and area $2500\,\mathrm{cm}^2$ has $2.08\times10^{16}$ cells of size $(\lambda/2)^2(\lambda/n_r)$ at $\lambda = 500\,\mathrm{nm}$; its surface has $4\times10^{12}$; the ratio is the thickness in units of $\lambda/n_r$. Cells are not bits until a write and a read are given.

(iv) *(Simulation.)* Under H4.1–H4.4, a classical charged fluid with one quantum-pressure term, driven through four identical layers by an input computed by the Chebyshev recursion (4.5) (amplitude $2.13$, not $3.9$), develops the density change (4.7), whose central value (4.8) matches the reported Figure 6 to within $1\%$ of density at every sampled time. The layer system does not preserve Gauss's law (4.3).

*Proof.* Sections 1–4. $\blacksquare$

---

## 6. What the model does not contain

Let $\Sigma$ be the state space of the model: triples $(\varphi, A^0, \mathbf{A})$ on the box (Section 1), or $(\rho^{(n)}, \mathbf{A}^{(n)}, \mathbf{E}^{(n)})_{n=1}^N$ (Section 4), with the flow $\Phi_t$ defined by the field equations and the supplied drive.

**Definition 6.1 (Memory).** A memory over an object set $\mathcal O$ consists of a write $W: \mathcal O\times\Sigma \to \Sigma$, a hold time $\tau_{\rm ret}$ with $\|\Phi_t W(o,\sigma) - W(o,\sigma)\| \le \epsilon$ in a norm on $\Sigma$ for $0 \le t \le \tau_{\rm ret}$, and a read $R: \Sigma \to \mathcal O$ with $R(\Phi_tW(o,\sigma)) = o$ for all $t \le \tau_{\rm ret}$ except on a set of error rate $p$.

**Proposition 6.2.** In Sections 1–4: the only input to $\Sigma$ is the supplied drive $\mathbf{A}^{(0)}$ (Section 4) or the supplied pattern (H3.4), neither of which is a map from an object set; no read $R$ is defined; no hold time follows from the equations (Corollary 4.9, Lemma 3.9); and no map from $\Sigma$ to any set other than $\Sigma$ itself appears. Hence no statement of the form "the pattern is recalled", "holograms correspond one-to-one to $X$", or "$X$ is manipulated", for any $X$ outside $\Sigma$, is a proposition about the model: it has no referent in $\Sigma$. $\blacksquare$

**Open problems.** Each is a theorem that would have to be proved, or a number that would have to be supplied, before Theorem 5.1 says anything about a medium.

- **O1.** Values of $g, \Omega, N', L_3, \theta_0, T_2$ for a stated medium, and a proof of (2.9).
- **O2.** A bound on the Coulomb term (1.4) for that medium, or a proof that the background $\rho_b$ neutralizes it.
- **O3.** A write: an equation whose solution has $\rho \propto |r + o|^2$ with $o$ an input, from (1.1) or a stated extension.
- **O4.** A read: a map $R$ on $\Sigma$ with a proved error rate.
- **O5.** A hold: a barrier $\Delta E$ for the pattern, from the equations, with (3.8) evaluated.
- **O6.** The ablation: the solution of (4.2) with the $\hbar^2$ term removed, compared with Figures 5–6; and the solution with (G) imposed, compared with (4.3).

---

## Appendix A. Hypothesis ledger

| Label | Statement | Where used | Status |
|---|---|---|---|
| $\rho_b$ | background charge density | §1, §3 | supplied; $0$ in the source; required $\ne 0$ on a torus (Thm 1.5) |
| H2.1 | two real levels, $\Omega = E_1 - E_0$ | §2 | supplied |
| H2.2 | $A^0 = 0$, $\mathbf{A} \parallel \hat{\mathbf e}_3$ | §2 | supplied; contradicts a changing density (Thm 1.4, Thm 2.9) |
| H2.3 | resonant shell, $\Omega^2 \ge \omega_p^2$ | §2 | supplied; threshold corrected from the source |
| H2.4 | slow envelopes, $\varepsilon < \frac12$ | Prop 2.8 | supplied (rotating-wave approximation) |
| H2.5 | dipole, $L_{1,2} \ll 2\pi/\sqrt{\Omega^2 - \omega_p^2}$ | §2 | supplied; fails for any emitting region larger than the wavelength, such as the $2500$ cm$^2$ slab of §3 at $500$ nm |
| H2.6 | loss $-\mathcal A/L_3$ | Thm 2.6 | supplied model |
| H2.7 | seed $\theta_0 \ne 0$ | Cor 2.7 | supplied; undefined in the source |
| (1.4) | $e\sup\lvert A^0\rvert \ll \Omega$ | Thm 2.9 | derived condition; not evaluated by the source |
| (2.6) | $L_3 \ll \tau_R$ | Thm 2.6 | derived condition; not evaluated |
| H3.1 | static neutral medium | §3 | supplied; the one consistent use of H2.2 |
| H3.2 | screening $M^2$, source $M^2\tilde{\mathbf A}$ | §3 | supplied constants |
| H3.3 | polarization $\hat{\mathbf e}_3$ | §3 | supplied |
| H3.4 | $\rho = c\lvert r + o\rvert^2$ | Thm 3.4 | supplied; no write (Rem 3.6); $o$ has no source |
| H3.5 | one cell = one bit | Prop 3.8 | supplied; needs a write and a read |
| H4.1 | planar, $U = 0$ | §4 | supplied |
| H4.2 | $M^2$, $\gamma$ replace the self-energy | §4 | supplied constants (2 and 0.2 in units of $m$) |
| H4.3 | four identical layers, coupling $v$, drive $\mathbf A^{(0)}$ | §4 | supplied; drive computed from the target |
| H4.4 | (G) not imposed | Thm 4.5 | consequence of the unitary gauge; breaks Gauss's law |
| (4.6) | targets | §4 | supplied by the authors |
| $m$ | the mass scale | §4 | never given; at $4$ meV the lattice cell is $49\ \mu$m, at the mass of a water molecule $10^{-17}$ m |

## Appendix B. Corrections to the source

| Location | As printed | Corrected |
|---|---|---|
| before (A2) | "Coulomb gauge, namely $A^0 = 0$ and $\nabla_iA_i = 0$" | two conditions, not a gauge; freezes $\rho$ (Thm 1.4); Coulomb gauge is Thm 1.5 |
| (A31) | $\chi_1$ on the right | $\chi_0$ |
| after (A29), after (A47) | $\Omega \ge e^2\lvert\bar\varphi\rvert^2/m$ | $\Omega^2 \ge e^2\bar n/m$ |
| §2 | "definition of $\theta_0$ is in Appendix A" | $\theta_0$ is a hypothesis (H2.7) |
| (A52) | $\tilde A_i \propto \cdots$ | $A_i - \tilde A_i = -\sigma[\cdots]$, (3.5) |
| §3 | $k_BT\ln2$ bounds thermal degradation | it bounds erasure heat; retention needs (3.8) |
| (A70) | $-\frac{e}{2m}(A_i - \partial_i\beta/e)^2$ | $+$, as in (A81), (A87) and (B) |
| (A76), (A78) | $e\lvert\bar\varphi\rvert^2/m$ | $e^2\lvert\bar\varphi\rvert^2/m$ |
| (A88), (A89) | $-\partial_1^2u_1$, $-\partial_2^2u_2$ | $-\partial_2^2u_1$, $-\partial_1^2u_2$, (4.4) |
| §4 | input maximum $0.1\times2^4/0.8^4 = 3.9$ | $0.1\,U_4(1.25) = 2.13$ (Cor 4.7) |
| §4 | "distributions … stop evolving" | (4.8): they stop because the drive decays |
| §5 | "one-to-one correspondence" | no second set exists (Prop 6.2) |

## Appendix C. Numbers

| Quantity | Value | From |
|---|---|---|
| $k_BT$ at $310$ K | $26.71$ meV | Prop 3.10 |
| $hc/(k_BT\ln 2)$ | $67\ \mu$m | Prop 3.10 |
| $k_BT\ln 2$ | $18.52$ meV | Prop 3.10 |
| barrier for $1$ s, $1$ h, $1$ yr ($\tau_a = 1$ ps) | $0.74$, $0.96$, $1.20$ eV | (3.8) |
| $C_2$, $n_rd/\lambda$, $C_3$ at $500$ nm | $4.0\times10^{12}$, $5200$, $2.08\times10^{16}$ | Prop 3.8 |
| $C_3$ at $1500$ nm, at $310\ \mu$m | $7.7\times10^{14}$, $8.7\times10^7$ | Prop 3.8 |
| $s = \omega_p^2/M^2$ at the Section 4 values | $0.045$ | Cor 3.5 |
| $U_4(1.25)$, $0.1\,U_4$ | $21.3125$, $2.13$ | Cor 4.7 |
| $U_4(1.30625)$, $0.1\,U_4$ | $27.11$, $2.71$ | Cor 4.7 |
| $\delta_{\rm centre}$ at $mx^0 = 5, 20, 40, 100, 200$ | $-1.2, -4.5, -8.2, -15.8, -21.6\ \%$ | (4.8) |
| $\delta_{\rm corner}$ at $mx^0 = 200$ | $+13.5\ \%$ | Thm 4.10 |
| $T(\theta_0)$ for $\theta_0 = 0.1$ | $4.38\times(4/\omega_c)$ | (2.3) |

## Appendix D. Verification map

Every result below is recomputed from scratch by the companion script `7_paper_rewritten_checks.py` (numpy and sympy only; it prints PASS or FAIL per line and exits with status 1 on any failure). Symbolic checks prove an identity for arbitrary functions; numerical checks integrate the stated equations and compare with the stated closed forms.

| Result | Check line | Method |
|---|---|---|
| Prop 1.2 | Prop 1.2 | symbolic: kinetic-term expansion and $\partial\mathcal L/\partial A_i = e\rho\mathcal V_i$ |
| Thm 1.3 | Thm 1.3 | symbolic: $\nabla\cdot(\nabla^2\mathbf A - \nabla\nabla\cdot\mathbf A) = 0$ |
| Prop 1.6 | Prop 1.6 | numerical: slab comparison bound; ball integral $2\pi a^2$ |
| Prop 2.3 | Prop 2.3 | numerical: invariants along (2.1) to $10^{-13}$ |
| Thm 2.4, 2.5 (i)–(ii) | Thm 2.4/2.5 | numerical: pendulum equation, period (2.3), peak, turning points |
| Thm 2.5 (iii) | Thm 2.5(iii) | numerical: sech limit (2.4), logarithmic period |
| Thm 2.6 | Thm 2.6 | numerical: (2.5) at $L_3/\tau_R = 0.005$ against (2.8) |
| Cor 2.7 | Cor 2.7 | numerical: fixed point |
| Prop 2.8 | Prop 2.8 | symbolic: density expansion |
| Thm 3.2 | Thm 3.2 | symbolic: residual (3.3) |
| Thm 3.4, Cor 3.5 | Thm 3.4 | symbolic: (3.5); $s = 0.045$ |
| Prop 3.8 | Prop 3.8 | arithmetic |
| Prop 3.10 | Prop 3.10 | arithmetic |
| Thm 4.1 | Thm 4.1 | symbolic: (C) and (B); printed (A70) sign fails on a plane wave |
| Thm 4.5 | Thm 4.5 | symbolic: (4.3) |
| Thm 4.6, Cor 4.7 | Thm 4.6/Cor 4.7, Thm 4.6 (lattice) | recursion, closed form, forward solve; derivative terms on the lattice |
| Thm 4.8 | Thm 4.8 | lattice divergence of (4.6), table against Figure 6 |
| Thm 4.10 | Thm 4.10 | lattice sum, corner rise |
| Appendix A, C | App. A/C | arithmetic |

Not replayed by the script: the Gauss-residual ratio quoted after Theorem 4.5 and the three rerun dips quoted after Corollary 4.9, which come from reruns of the source's full simulation reported elsewhere in this folder.
