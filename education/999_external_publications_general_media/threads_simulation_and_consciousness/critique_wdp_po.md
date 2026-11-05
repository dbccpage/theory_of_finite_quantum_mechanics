# Holographic Brain Theory, audited with the Witnessed Difference Programme and Projection Obstruction

Date: 2026-11-05. Target: Nishiyama, Tanaka, Tuszynski, Tsenkova, *Holographic Brain Theory: Super-Radiance, Memory Capacity and Control Theory*, IJMS 25(4):2399 (2024). Equation numbers refer to [ijms-25-02399.md](ijms-25-02399.md). Every number and every symbolic step below is replayed by [code/critique_checks.py](code/critique_checks.py) (checks 1 to 11). Two results are taken from the sibling review [adversarial_review.md](adversarial_review.md) (PR #513) and not redone: Gauss's law in Appendix C is broken exactly by the $M^2$, $\gamma$ and $v$ terms, and one-year retention at 310 K needs a barrier of about 1.2 eV while the paper's own water scale, 4 meV, gives about 1 ps.

Tags, as in [claims_ledger.md](claims_ledger.md): **Witnessed** (the paper's text or figure), **Derived** (follows by the steps shown), **Supplied** (put in by someone, named), **Cited** (standard result, not re-derived), **Open** (needs information the paper does not give). The sources and claim ids behind each tool used here are in the companion section at the end, so the body can be read without them.

The rule of the audit: attack the mathematics as a colleague would, so a reader can repeat it. Nothing here is about the authors.

A second rule, because three reviews now exist (ChatGPT's, PR #513, this one): agreement between reviewers is not evidence. No claim below rests on how many reviews share it. Each claim names what it rests on: a check number (an equation replayed by the script in this folder), a paper location (witnessed text or figure), a standard reference (cited), or "another review" (say-so, not redone here). PR #513's script was re-run in this folder on 2026-11-05 and its printed results reproduce, so its two results are replayed, not say-so. ChatGPT's points are treated in §8.5 as claims to break, not as support.

---

## 0. One screen

**The paper, in five lines.** (1) Appendix A: non-relativistic scalar QED, two-level water states, rotating-wave and dipole approximations, a loss term added by hand, and the standard super-radiant sech pulse comes out. (2) Section 3: a volume-hologram capacity bound with $\lambda = 500$ nm, $n_r = 1.3$, $d = 2$ mm, 2500 cm², giving 2.5 PB. (3) Appendix B: a static reference field, a density supplied to be $|r+o|^2$, and the Gabor reconstruction term appears. (4) Appendix C and Section 4: the classical (mean-field) sector of the model in Madelung form, a Proca mass and an Ohmic damping put in for a dropped self-energy, five identical layers, an open-loop static inversion, one rectangular density dip of 21 % on a 128² lattice. (5) Section 5: a "quantum mind" that registers, deciphers, decides and encodes; "one-to-one correspondence" between holograms and subjective experiences.

**The audit, in five lines.** (1) The gauge pair $A^0 = 0$, $\nabla\!\cdot\!\mathbf A = 0$ is not a gauge: with charge present it freezes the density, which kills the coherence that drives the pulse (§2). (2) Everything computed lives in the sector the paper discards as "quantum": $\Delta$, $D^{11}$ and $\Gamma_2$ are set to zero, and the one surviving $\hbar$ term is reported as a distortion to be damped away (§5). (3) The mean-field run is a product retraction with an unpaid budget: the normal rate $\nu$, the incident norm $g$ and the certified window are never computed, though they are computable (§6). (4) Memory is written and never read: of the retention packet $(M, u, r, \approx)$ the paper supplies $M$ and $u$ only, and its own Figure 6 shows the write decaying (§7). (5) The observer is the one part no equation touches: delete every sentence containing "mind" or "subjective experience" and no equation changes (§8).

**Two tests that decide most of it.**

| Test | Do this | Result |
|---|---|---|
| $\hbar \to 0$ | Drop the Bohm term $-\nabla^2\lvert\bar\varphi\rvert/(2me\lvert\bar\varphi\rvert)$ from (A70), (A81), (A87) | Sections 3, 4 and Appendices B, C are unchanged in kind: classical charged fluid + Maxwell + Proca + Ohmic damping. The paper calls this term a distortion (Section 5). **Derived**, check 3. |
| mind $\to 0$ | Delete every sentence of the paper that contains "mind", "consciousness" or "subjective experience" | No equation, figure, number or simulation changes. The mind clauses carry no authority over any result. **Witnessed**: Sections 1, 5, 6 are the only places those words occur. |

---

## 1. The paper as a chain of projections

Every step of the paper is a projection that throws information away, followed in words by a retraction that is never computed. Written as maps:

$$
\underbrace{\rho_{\text{QED}}}_{\text{state}}
\;\xrightarrow{\ \Pi_{\text{coh}}\ }\;
\underbrace{(\bar\varphi,\,A_\mu)}_{\text{mean field}}
\;\xrightarrow{\ \text{Madelung}\ }\;
\underbrace{(\lvert\bar\varphi\rvert,\,\beta,\,A_\mu)}_{\text{fluid}}
\;\xrightarrow{\ \lvert\cdot\rvert^2\ }\;
\underbrace{\lvert\bar\varphi\rvert^2}_{\text{density}}
\;\xrightarrow{\ \text{threshold}\ }\;
\underbrace{\{\text{high},\text{low}\}}_{\text{binary cell}}
\;\xrightarrow{\ ?\ }\;
\underbrace{\text{“subjective experience”}}_{\text{prose}}
$$

| Projection | What is thrown away | Where the paper does it | Retraction promised | Retraction computed? |
|---|---|---|---|---|
| $\Pi_{\text{coh}}$: state $\mapsto$ expectation values | all connected correlations: $\Delta$, $D$, $\Gamma_2$ | (A69)–(A71): "neglect", "set to zero" | none | no; the budget is §6 |
| Madelung | nothing (a change of variables) | (A69)–(A70) | — | exact, check 3 |
| $\lvert\cdot\rvert^2$ | the phase $\beta$ | (A76)–(A87): "we omit terms $-\partial_\mu\beta/e$" | none | no |
| threshold | the 1.3 %–21 % contrast | Section 4, "step-function-like" | Lohmann reconstruction (6)–(9) | no; one cell, no image |
| ? | everything | Section 5, 6 | "one-to-one correspondence" | no map is given |

The first projection is the one Projection Obstruction prices (§6). The last is the one the Witnessed Difference Programme prices (§8). The middle three are where the paper's own words "quantum" and "hologram" are spent (§4, §5).

---

## 2. The gauge pair is a constraint on the matter, not a gauge (Appendices A and B)

**2.1 The constraint.** In the temporal gauge $A^0 = 0$ the scalar potential is gone, and with it the Lagrange multiplier that enforces Gauss's law. Gauss's law then has to be imposed on the initial data and is preserved by current conservation. The paper's (A7) is exactly that statement, integrated once in time:

$$
\partial^\nu F_{\nu 0} = J_0 + c(\mathbf x), \qquad J_0 = -e\lvert\varphi\rvert^2 .
$$

With $A^0 = 0$, $F_{\nu 0} = -\partial_0 A_\nu$, so the left side is $\mp\,\partial_0(\nabla\!\cdot\!\mathbf A)$ (the sign is a metric convention and does not matter). Hence

$$
\boxed{\ \pm\,\partial_0\big(\nabla\!\cdot\!\mathbf A\big) = -e\lvert\varphi\rvert^2 + c(\mathbf x)\ }
$$

and the second condition $\nabla\!\cdot\!\mathbf A \equiv 0$ forces $\partial_0\lvert\varphi\rvert^2 = 0$ at every point. The paper sets $c = 0$ ("boundary conditions are set to be zero"), which then forces $\lvert\varphi\rvert^2 = 0$; keeping $c$ (the sibling review's static background) only allows a *static* density. **Derived** (check 1).

**2.2 What that does to the pulse.** The two-level state (A8), (A12) has density

$$
\lvert\varphi\rvert^2 = \lvert\chi_0\rvert^2\lvert\phi_0\rvert^2 + \lvert\chi_1\rvert^2\lvert\phi_1\rvert^2 + \big(e^{-i\Omega x^0}\chi_0^*\chi_1\,\phi_0^*\phi_1 + \text{c.c.}\big),
$$

so $\partial_0\lvert\varphi\rvert^2 = 0$ pointwise, with $\phi_0^*\phi_1 \neq 0$ (needed for $J_{01}\neq 0$ in (A27)), forces the coherence $R = 2\chi_0^*\chi_1$ to vanish. But $R$ is the whole right-hand side of (A38): $\partial_0\mathcal A = (g\Omega/4\pi L_3)R$. With $R = 0$ the field is constant and there is no super-radiant pulse. The gauge pair used to derive the pulse is incompatible with the pulse. **Derived** (check 1). The oscillating cross term is the dipole that radiates; its longitudinal Coulomb field is what a real Coulomb-gauge calculation keeps as $A^0 = \nabla^{-2}J^0$, the dipole–dipole near field the sibling review already flags. **Cited**.

**2.3 Appendix B makes it worse.** (A48) adds a Proca term $M^2 A_i$. Taking the divergence of the Proca equation with a conserved current gives $M^2\partial_\mu A^\mu = 0$, so $A^0 = 0$ *forces* $\nabla\!\cdot\!\mathbf A = 0$ at all times, and then 2.1 forces $\lvert\varphi\rvert^2 = 0$. In Appendix B the hologram medium has to be empty. **Derived** from a standard identity (**Cited**), check 1.

**2.4 Status.** The radiation gauge $A^0 = 0$, $\nabla\!\cdot\!\mathbf A = 0$ is a gauge only in the source-free theory. In the injection ledger it is not a convention but a supplied physical constraint: it deletes the longitudinal sector and freezes the charge. Appendix C does not make this choice (it keeps $A_0$ through (A87)), so the Section 4 simulations are not touched by 2.1–2.3; they are touched by the Gauss-law breakage of the sibling review instead.

---

## 3. Super-radiance: the standard pendulum, with its quantum part supplied (Appendix A)

**3.1 What the derivation is.** (A33)–(A35) are the Maxwell–Bloch equations for one resonant mode coupled to a two-level ensemble in the dipole and rotating-wave approximations. With $Z = N\cos\theta$, $R = N\sin\theta$ they are the Bloch pendulum, $\dot\theta = 2g\mathcal A$ (A40). The loss term $\mathcal A/L_3$ in (A42) is added by hand ("setting the length $L_3$ for release of radiation"); in the limit $\partial_0 \ll 1/L_3$ the field is slaved to the matter, $\mathcal A = (g\Omega N/4\pi)\sin\theta$, and the pendulum becomes overdamped:

$$
\dot\theta = \frac{\sin\theta}{\tau_R},\qquad \tau_R = \frac{2\pi}{g^2\Omega N},\qquad
\tan\frac{\theta}{2} = \tan\frac{\theta_0}{2}\,e^{x^0/\tau_R},\qquad
\mathcal A = \frac{g\Omega N}{4\pi}\,\mathrm{sech}\frac{x^0-\tau_0}{\tau_R}.
$$

This is the bad-cavity mean-field super-radiance of Dicke, Bonifacio and Lugiato, Gross and Haroche. **Cited**. Check 2 integrates (A36)–(A38) with the loss term and recovers (A45) to 1 % as $L_3 \to 0$; at $L_3 = 0.5/\Omega$ the error is 24 %, so "the solution" is the limit, not the equations. **Derived**.

**3.2 What is supplied.** $\theta_0$ is free. The one genuinely quantum element of super-radiance, the initiation of the pulse by vacuum fluctuations, enters only through $\theta_0 \approx 2/\sqrt N$ (**Cited**, Gross and Haroche), which with the paper's own $\tau_0 = -\tau_R\ln\tan(\theta_0/2)$ gives the delay $\tau_0 \approx \tfrac12\tau_R\ln N$. The paper neither derives nor uses it. Also supplied: real $J_{01} = J_{10}$, real $\mathcal A$, the resonant-shell measure (A29), $A_1 = A_2 = 0$, and the loss length $L_3$. Not checked: $\tau_R < T_2$ (dephasing of water conformational states at 310 K; the Discussion names the problem and gives no $T_2$), the cooperation condition $L_3 < c\,\tau_R$, and $\Omega \ge e^2\lvert\bar\varphi\rvert^2/m$ (needs $e$, $m$, $N/V$, none given). **Open**.

**3.3 No number comes out.** $\tau_R$ needs $g$, $\Omega$, $N$; $E_3$ needs the same and $L_3$. None has a value, so Appendix A predicts no wavelength, no intensity and no time. The $\lambda = 500$ nm of Section 3 is therefore supplied, not derived from $\Omega$; the paper says so ("for visible light", "as an example"). **Witnessed**.

**3.4 Where the light goes.** (A10) puts the vibration along $x^3$, (A13) expands $A_3$ in modes with $\mathbf k = (k^1, k^2, 0)$, and $A_1 = A_2 = 0$. So the emitted field is polarized along the microtubule axis and propagates in the plane perpendicular to it; a dipole along $x^3$ radiates as $\sin^2\theta$ and nothing along the axis. Figure 1 draws rings of light leaving the two ends, and Section 5 needs light guided along the lumen. Both are supplied against (A13). **Derived** (check 7).

**3.5 The waveguide sentence.** "Single mode waveguides with a cutoff wavelength 21 nm, in brief they should be able to guide light from strong ultra-violet to near-infrared." The 21 nm follows from the conducting-pipe formula $\lambda_c = 1.706\,d$ with $d \approx 12$ nm (the lumen). Under that model only $\lambda < \lambda_c$ propagates: 500 nm, 1500 nm and the whole UV-to-NIR band are below cutoff, evanescent. The inequality is backwards. Under the model that actually fits a protein cylinder in water (dielectric, no cutoff), confinement is set by $V = (\pi d/\lambda)\sqrt{n_1^2 - n_2^2} \approx 0.11$ at 500 nm, far below 1: the mode is essentially unconfined. **Derived** from textbook formulas (**Cited**: Jackson; Snyder and Love), check 6.

---

## 4. The hologram is classical, and its medium is supplied (Appendix B, Section 3)

**4.1 What (A48)–(A52) say.** With the Proca mass, the response to a static reference field $\tilde A_i = r(x^1, x^2)$ is

$$
A_i = \frac{M^2}{M^2 + e^2\lvert\varphi\rvert^2/m}\, r \;\approx\; \Big(1 - \frac{e^2\lvert\varphi\rvert^2}{M^2 m}\Big) r .
$$

The density modulates the field by London screening. Then (A51) **supplies** $\lvert\varphi\rvert^2 \propto \lvert r+o\rvert^2$; nothing in the dynamics produces it, and the object wave $o$ has no source anywhere in the model. Substituting gives (A52), $r(\lvert r\rvert^2 + \lvert o\rvert^2 + r^*o + ro^*)$, the Gabor reconstruction with the image term $\lvert r\rvert^2 o$. This is classical amplitude holography: an intensity $\lvert r+o\rvert^2$ written into a transmittance, read by $r$. The phase of $\varphi$ plays no role; only $\lvert\varphi\rvert^2$ enters. **Derived**.

**4.2 Depth.** With the Section 4 parameters ($e = 0.3$, $\lvert\varphi\rvert^2 = 1$, $M^2 = 2m^2$, lattice $ma_s = 1$) the modulation depth is $e^2\lvert\varphi\rvert^2/(M^2 m) = 0.045$: the image term carries 4.5 % of the reference amplitude, a diffraction efficiency of about $2\times10^{-3}$. The expansion (A49) is valid only when this number is small, so a strong reconstruction and a valid expansion exclude each other. **Derived** (check 5).

**4.3 The capacity is a product of supplied factors.** (3)–(5) multiply $4/\lambda^2$ by $n_r d/\lambda$ and by an area. The arithmetic holds (sibling review). Each factor is supplied: $\lambda = 500$ nm (not derived, 3.3), $n_r = 1.3$, $d = 2$ mm, 2500 cm². The bound is the volume-hologram bound for a transparent medium read by a coherent reference beam through its full thickness. Cortex at 500 nm is not that medium: the scattering coefficient of grey matter is of order 10–20 mm⁻¹ (**Cited**, tissue-optics compilations such as Jacques 2013; order of magnitude only), so a 2 mm path is 20–40 scattering lengths and a reference wave arrives as speckle. The number is also not a memory: a capacity is a count of distinguishable states, and without a readout map and a report grammar it bounds nothing an observer can use (§8.3).

**4.4 "Binary".** The Lohmann hologram of (6)–(9) is an array of cells, each with a hole whose width encodes an amplitude and whose offset encodes a phase. Section 4 produces one rectangular dip (60 × 40 cells, N₁ = 30, N₂ = 20) with contrast rising from 1.3 % to 21 % and never reaching two levels. "Binary" is supplied; no multi-cell pattern is formed and no image is reconstructed. Appendix A's super-radiant wave is never used as the $r$ of Appendix B, and Appendix B's $\lvert r+o\rvert^2$ is never produced by Appendix C. The three parts do not connect. **Witnessed**.

---

## 5. Appendix C is the classical sector of a quantum model

**5.1 The truncation.** The 2PI effective action (A56) carries the quantum content of the model in three objects: the boson propagator $\Delta$ (A60)–(A61), the photon propagator $D$ (A59), and the 2PI vertex functional $\Gamma_2$. The equations of motion (A62)–(A64) keep them. Then: $\Gamma_2 \to 0$ ("higher order"), $D^{11}_{ii}(x,x) \to 0$ ("neglected"), $\Delta^{11} \to 0$ (absent from (A69)–(A71)). What remains is the classical action's Euler–Lagrange equations for $(\bar\varphi, A_\mu)$. Every sentence in Section 5 about superposition, coherence, entanglement or decoherence refers to the three dropped objects. **Witnessed**.

**5.2 Madelung.** Check 3 verifies symbolically that (A63) with $\Gamma_2 = D^{11} = 0$ and $\bar\varphi = \lvert\bar\varphi\rvert e^{i\beta}$ is exactly

$$
\partial_0\lvert\bar\varphi\rvert^2 = \frac{e}{m}\nabla\!\cdot\!\Big[\lvert\bar\varphi\rvert^2\Big(\mathbf A - \frac{\nabla\beta}{e}\Big)\Big],\qquad
A_0 - \frac{\partial_0\beta}{e} = -\frac{\nabla^2\lvert\bar\varphi\rvert}{2me\lvert\bar\varphi\rvert} + \frac{e}{2m}\Big(\mathbf A - \frac{\nabla\beta}{e}\Big)^2 ,
$$

a charged superfluid: continuity plus a Bernoulli constraint with the Bohm (quantum-pressure) term. **Derived**. Printed-sign finding: (A70) carries $-\tfrac{e}{2m}(\mathbf A - \nabla\beta/e)^2$; the derivation and the simulated equations (A81), (A87) carry $+$. The simulation has the right sign. **Derived** (check 3).

**5.3 The only $\hbar$.** Restore units and the single term with $\hbar^2$ is the Bohm term. The paper's Discussion traces the "slight distortions" of the step function in Figure 6f to exactly this term and says they "do not seriously affect" the result. So the one quantum term in the computed sector is the one being damped away. With the Section 4 numbers (21 % dip, $e = 0.3$, $A \approx 0.1$) the Bohm term at the dip's edge is 0.2 m for a one-cell edge, 0.008 m for a five-cell edge, against $eA^2/2m = 0.0015\,m$: wherever the step is sharp, the "distortion" is the largest term in $A_0$. The actual edge width is not reported. **Derived** for the orders of magnitude, **Open** for the simulated ratio (check 4).

**5.4 The memory kernel replaced by a local operator.** (A75) writes the dropped self-energy as a memory integral $\int^{x^0}\!\Sigma_\rho(x^0, y^0)\,A_i(y^0)\,dy^0$ and then **supplies** $\Sigma_\rho \simeq -M^2 - \gamma\,\partial_0$, "factors dependent on temperature and charge" with no formula. This is projection-induced memory in the exact sense: a non-Markovian kernel is replaced by a Markovian one, and whether the projected dynamics descends (same coarse data now $\Rightarrow$ same coarse data later) is never checked. Two physical consequences are already on record: a photon mass in a charged condensate is the London term $e^2\lvert\bar\varphi\rvert^2/m$ that (A82) already contains, so $M^2$ double-counts the Meissner effect with a free value; and a conserved current gives a transverse self-energy by the Ward identity, so a constant $M^2$ and a $\gamma\partial_0$ acting on all of $\mathbf A$ break charge conservation, which is the sibling review's $-M^2\nabla\!\cdot\!\mathbf A - \gamma\,\partial_0\nabla\!\cdot\!\mathbf A + v\nabla\!\cdot\!\mathbf A^{(n\pm1)}$. **Cited** (PR #513).

**5.5 The hierarchy.** Scalp, skull, dura, cerebrospinal fluid and neocortex are five copies of the same equation with the same $e$, $m$, $M^2$, $\gamma$, coupled by one nearest-neighbour number $v$ ("transmittance"). No permittivity, conductivity, thickness or Fresnel coefficient distinguishes bone from fluid. **Witnessed**. The inputs are obtained by static inversion (A88)–(A89), dropping the time derivatives and the matter term; the inverse amplifies by $0.1\,(M^2/m^2)^N/v^N = 3.9$ (the text says "approximately 3"), check 11. The run is open loop: the output "approaches the target function due to damping" and then decays with the input ($e^{-\gamma_2 x^0}$); no error measure, no feedback, no trained readout, so "morphological computation" and "reservoir" are names, not operations. The conserved quantity reported, number to $10^{-6}$ %, is the discrete continuity equation (A86) holding; it says nothing about Gauss's law (broken, sibling review) or energy (A74, never reported). No lattice or time-step convergence is shown, so Figure 6 has an approximation order and no error bar. **Witnessed**.

**5.6 No scale.** Every quantity in Section 4 is in units of $m$ ($ma_s = 1$), and $m$ is never chosen. Two readings, check 9: with the paper's water scale $m = 4$ meV, $a_s = 49$ µm, the dip is 1.5 mm across, the box is 6 mm, and $mx^0 = 200$ is 33 ps; a millimetre cell is not an optical hologram at 500 nm. With $m$ chosen so that $a_s = 100$ nm resolves 500 nm fringes, $m = 2$ eV, the Meissner mass is 2.8 eV and the damping $\gamma = 0.4$ eV, a rate of $6\times10^{14}$ s⁻¹, in water. Either Section 3 and Section 4 are about different objects, or the parameters are not biological. **Derived**; which reading the authors intend is **Open**.

---

## 6. Mean field without a budget (Projection Obstruction)

**6.1 What a mean-field run is.** Keeping $(\bar\varphi, A_\mu)$ and dropping $\Delta$, $D$, $\Gamma_2$ is the product (coherent-state) retraction $\Pi$: the true state is replaced at every instant by the product of its one-mode marginals, and the dynamics is projected onto the tangent space of the product manifold, $\dot{\tilde\rho} = P_{\tilde\rho}\,\mathcal L\tilde\rho$. The residual $R(s) = Q_{\tilde\rho}\mathcal L\tilde\rho$ is what the true flow does that the product cannot follow. Projection Obstruction gives the price. From a product initial state, for every pair of coupled degrees of freedom $e$,

$$
D_e(t) := \big\lVert \rho_e(t) - \rho_a(t)\otimes\rho_b(t)\big\rVert_1 \;\ge\; \nu_e\,t - 24\,g^2 t^2,
\qquad \nu_e = \lVert Q_e\dot\rho_e(0)\rVert_1 ,
$$

with $g$ the incident interaction norm; for pure endpoint states $\nu_e = 2\lVert\chi\rVert$ with $\chi$ the centred interaction applied to the product, which is Yang's entanglement timescale, $\nu_e = 2/T_{\text{ent}}$. With damping (a Lindblad bath) the same bound holds with $6\Lambda_*^2$ in place of $24g^2$. The observable error of the mean-field run then obeys the edge-decomposed Duhamel bound: $\lvert\langle O\rangle_{\rho(t)} - \langle O\rangle_{\tilde\rho(t)}\rvert \le \lVert O\rVert_\infty\lVert\delta\rho_0\rVert_1 + \sum_e\int_0^t w_{O,e}(t-s)\,\nu_e(s)\,ds$. **Cited** (PO-000 §5; the Lean-mechanized parts are listed in the companion).

**6.2 Applied to Appendix C.** The paper's couplings are the current term $(e/m)\,\bar\varphi^*\nabla\bar\varphi\cdot\mathbf A$ and the seagull $e^2\lvert\bar\varphi\rvert^2\mathbf A^2/2m$: cubic and quartic, so $\nu_e \neq 0$ generically and the product manifold is left at first order in $t$. Check 10 runs the structure on a two-mode toy, $H_{\text{int}} = g\,(b^\dagger b)(a + a^\dagger)$ from coherent states $\lvert\alpha\rangle\lvert\beta\rangle$: the normal rate is $\nu = 2g\,\Delta(b^\dagger b)\,\Delta(a+a^\dagger) = 2g\lvert\beta\rvert$, numerically $0.150000$ against the formula $0.150000$, and the exact defect follows $D(t) \approx \nu t$ out to $t \sim 1/g$ ($D(1) = 0.153$, $\nu t = 0.150$). The certified quadratic window is tiny for bosons because the incident norm depends on the Fock truncation (12.6 at 28 levels); the first-order rate does not. **Derived** on a **Supplied** toy.

**6.3 What the paper owes.** For its own $e$, $m$, $N$ and lattice: $\nu_e$ per coupled pair, $\Lambda_*$ for the damped version, the window $t \le \nu_e/48g^2$ (or $\nu_e/12\Lambda_*^2$), and the Duhamel error of the one observable it reports, $\lvert\bar\varphi\rvert^2$ in Figure 6. Until then the run has the status the Projection Obstruction ledger gives such results: a heuristic trajectory, uncertified. The Section 5 sentence "we should investigate the balance of decoherence and error corrections" names the right object and supplies none of its inputs: the budget $h_{\text{safe}} = \min\{H, (\varepsilon - e - j)/r\}$ needs a target $\varepsilon$, a current error $e$, a defect rate $r$ and a jump allowance $j$. The paper has no $\varepsilon$ (no tolerance anywhere), no $e$, no $r$, no code. **Open**.

**6.4 The deeper point.** The paper computes the classical sector and claims the quantum one. The claims (superposition, coherence over the whole brain, entanglement in tubulin) are about $D_e(t)$ being large; the computation assumes $D_e(t) = 0$ for all $t$. The two cannot both be kept. **Derived** from 5.1 and 6.1.

---

## 7. Memory written, never read (Witnessed Difference Programme, retention)

**7.1 The packet.** A memory is a retention packet $(M, u, r, \approx)$: a store, an update, a readout, and a rule for when a readout matches what was written. Without $r$ nothing can be recalled; without $\approx$ no recall can be right or wrong. The paper:

| Component | Paper | Tag |
|---|---|---|
| $M$ | the density $\lvert\bar\varphi^{(N)}\rvert^2$ on the output layer | Supplied |
| $u$ | the control write, (A82)–(A91), Figure 6 | Derived, uncertified (§6) |
| $r$ | the reconstruction (A52), Appendix B only; never applied to the Appendix C density, which is a step, not $\lvert r+o\rvert^2$ | absent for the simulated memory |
| $\approx$ | none: no tolerance, no comparison, no norm anywhere in the paper | absent |

**7.2 The paper's own evidence.** Figure 5: $A_1^{(N)}$ reaches the target at $mx^0 = 20$ and is zero by $mx^0 = 200$. Figure 6: the dip grows to 21 % and is "slightly distorted" at the last reported time; the Discussion says bosons "will collect into the peripheral regions" unless the input is damped, and that the Bohm term "can gradually become comparable to damping over time". So within the window shown, the deterministic dynamics already begin to erase the write, with no thermal noise in the matter sector at all. The lifetime of the record is never computed. **Witnessed**. The sibling review's threshold stands: one year at 310 K needs about 1.2 eV; the paper's 4 meV gives about 1 ps. **Cited** (PR #513).

**7.3 Classification.** This is the "witness without retention" countermodel: a trace is written (level: registration) and nothing later reads it or compares it. In database terms, a row is inserted and no query ever runs; calling the table a memory is a name for the insert. The right question is not "how many bits fit" but "what is $r$, what is $\approx$, and what does $r(M_{\text{now}})$ return after the Figure 6 decay".

---

## 8. Section 5: the observer is the one part not supplied (Witnessed Difference Programme)

**8.1 The mind $\to 0$ test (from the One screen).** No equation depends on the mind clauses. In the ledger's terms the authority effect of the Section 5 prose on every result is none. This is not a criticism of speculation; it is the statement that the paper's results and its claim share no variable.

**8.2 The four operations are the rungs of the observation ladder.** Section 5 lists what a quantum mind "would have to" do. Each is a named rung, and each needs a declared carrier before it can fail or succeed:

| Section 5 operation | Ladder rung | What must be declared | In the paper |
|---|---|---|---|
| "register quantum level changes in neurons" | 2, registration | a carrier $M$ and a write $u$ with a stated capacity | $M$, $u$ supplied (§7) |
| "decipher ... translate into high-level concepts" | 3–4, typed witness and re-comparison | a readout $r$, a type for what is read, a second record to compare with | none |
| "make a decision" | 5, evaluator acceptance | a defect $J$, a tolerance, repairs, a status | none; no tolerance anywhere |
| "encode that decision back ... macroscopic effect" | policy | a rule from status to action | none; the controller is open loop |

The paper's model reaches rung 1 (interaction: the field writes the density) and, generously, rung 2. The Discussion then uses rung-5 language ("decision", "experience") with nothing in between. The ladder's failure modes name which rung fails; here none can fail because none is declared.

**8.3 "One-to-one correspondence" is a bijection with no map.** The sentence "we find one-to-one correspondence between holograms induced by external input functions and our subjective experiences" asserts a bijection $H \leftrightarrow E$ between a set of field configurations and a set of experiences. A bijection needs both sets and a map. The paper gives $H$ (densities on a lattice), no $E$, and no $q: H \to P$ into any report channel. Three facts then apply before any physics: (i) a finite report channel with $\lvert P\rvert < \lvert H\rvert$ must merge distinct holograms (pigeonhole), so "one-to-one" is false for any report an experiment could record unless $P$ is as large as $H$, which no self-report is; (ii) two configurations with the same report get the same verdict from every evaluator downstream, so differences that never reach the report cannot be evidence of anything (the blind spot); (iii) a self-report does not certify the experience it reports (the awareness firewall), so the headset experiment proposed in Section 5 can establish a map from input fields to *reports*, never to experiences. Under those terms the experiment is the right kind of move and should be run; its result will be a declared $q$ and a measured confusion structure on $P$, which is worth having. **Derived** from definitions.

**8.4 Authority.** The paper's honest sentence, "how a quantum mind could perceive the macro-world is yet another mystery altogether", is correct and should be kept. Prose carries no authority over results, and the model's evaluator, if there were one, could not authorize its own outputs; authority sits outside the observer, with whoever declares the packet and the test. The paper proposes; nothing in it evaluates.

**8.5 Five points from a second reviewer, broken and recovered.** Jeremy forwarded a review of Section 5 by ChatGPT (five numbered problems, a table of undefined terms, a proposed question for the authors). Each point is right in its physics; each stops one step short, and one proposes a repair of the wrong shape.

| # | As stated | Right | Breaks | Recovered |
|---|---|---|---|---|
| 1 | A "mind sector" is introduced without identity; a model would need $H_{\text{tot}} = H_{\text{brain}} + H_{\text{mind}} + H_{\text{int}}$ | nothing identifies the sector | the proposed repair is the wrong shape: a Hamiltonian term adds dynamics, and the paper already has dynamics; what is missing is an observer, which is not a Hamiltonian but a packet (presentation, memory, evaluator, policy) plus a place for authority. $H_{\text{mind}}$ would reproduce the blind spot: a sector cannot certify its own evaluator from inside | owed: $q: X \to P$, $(M, u, r, \approx)$, $(J, \text{tolerance}, \text{repairs}, \text{status})$, a policy, and where authority sits. None is a term in $H$ |
| 2 | superposition is confused with physical occupancy; a many-body wavefunction lives on configuration space | correct physics | aimed at prose; the paper's computations contain no many-body wavefunction: Appendix C evolves $\bar\varphi(\mathbf x)$, $A_\mu(\mathbf x)$ on 3-space, so "occupy multiple states simultaneously" has no object in any equation | the "quantum" sentences refer to $\Delta$, $D^{11}$, $\Gamma_2$, which the paper sets to zero (§5.1); apply the mind $\to 0$ test |
| 3 | decoherence is conflated with collapse; decoherence selects no outcome | correct (Schlosshauer, RMP 76, 1267) | generic; the paper's model has no bath (the $\gamma$ of (A75) is a supplied constant), no outcome rule, and the sentence "balance of decoherence and error corrections" has no inputs | owed: $h_{\text{safe}} = \min\{H, (\varepsilon - e - j)/r\}$ with its four inputs (§6.3). Selection of an outcome needs a declared rule; normalization never selects |
| 4 | uncertainty relations are turned into unknowability | correct | generic; the sentence in the paper is motivation, not a step in any argument | a measurement packet declares measurand, carrier, unit, calibration, uncertainty, traceability; "never completely knowable" is a sentence about an undeclared packet, and $\Delta x\,\Delta p \ge \hbar/2$ is a statement about two declared spreads |
| 5 | the four operations are the explanandum, not the explanation | correct | stops at "they require explanation" | they are rungs 2–5 plus policy (§8.2); each needs a declared carrier; the paper's model stops at rung 1–2 |

The reviewer's table of seven undefined terms maps one-to-one onto declared objects: mind $\to$ the four-layer packet; consciousness $\to$ the firewall (no derivation from self-report; needs a declared report channel and $\approx$); observer $\to$ the packet; perception $\to$ the ladder; information $\to$ $(M, u, r, \approx)$ with a measurement packet; measurement $\to$ the measurement packet; quantum mind $\to$ the mind $\to 0$ test. The reviewer's closing question, "which result requires the existence of a mind", is the right one; its sharp form is the test: delete the word, see what changes. The reviewer's "one important correction", that the field has made real progress, is agreed; it fits a rule of evidence: refuting Tegmark's estimate (Section 5) moves no evidence to the alternative, since the weight of a hypothesis rises only with its own witnessed tests, never with a rival's failure.

**8.6 The five questions, applied to the headline claim.** What is compared? Nothing: a hologram is written, no second record is produced. What is the defect? Undefined: no $J$, no norm. Which repairs are allowed? None are named. What residual is accepted? None is named. Which rule decides? None. A claim with those five answers is not false; it is not yet a claim.

---

## 9. What survives

- The super-radiant sech pulse, given $\theta_0$, $g$, $\Omega$, $N$, $L_3$ and the gauge repair of §2 (it is the standard result; the paper's algebra (A33)–(A47) is right, with the misprints already logged in the ledger).
- The Madelung reduction (A69)–(A70): exact, with the printed sign in (A70) corrected to that of (A81)/(A87).
- The Gabor reconstruction term (A52), given a supplied $\lvert r+o\rvert^2$.
- The capacity arithmetic (3)–(5) as arithmetic.
- The number-conservation check of the integrator.
- The sentence "yet another mystery altogether".
- The proposal to run a headset experiment, read as a test of input fields against *reports* with a declared $q$.

---

## 10. What the paper owes

Each question names a quantity the authors can compute or declare.

1. **Gauge (§2).** In Appendix A, replace $A^0 = 0$ by $A^0 = \nabla^{-2}J^0$ and keep $\nabla\!\cdot\!\mathbf A = 0$. What is the dipole–dipole shift and dephasing it adds to (A36)–(A38), and is $\tau_R$ still shorter than it?
2. **Numbers (§3).** Values of $\Omega$, $g$, $N$, $L_3$ for water in a microtubule lumen; the resulting $\tau_R$, $\tau_0$ and wavelength. Is $\lambda = 500$ nm derived or chosen?
3. **Direction (§3.4–3.5).** Under (A13) the light leaves sideways with axial polarization. Which equation produces the end emission of Figure 1, and under which model does a 12 nm lumen guide 500 nm light?
4. **Scale (§5.6).** The value of $m$, and therefore $a_s$, $M$, $\gamma$ in SI units. Which of the two readings in check 9 is intended?
5. **Budget (§6).** $\nu_e$, $\Lambda_*$, the window, and the Duhamel error on $\lvert\bar\varphi\rvert^2$ for the Figure 6 run.
6. **Charge (sibling review).** Does $\nabla\!\cdot\!\mathbf E = J^0 + e$ hold along the Figure 6 run, and what is the Coulomb energy of the 21 % dip?
7. **Retention (§7, sibling review).** The barrier between two record states and the retention time at 310 K; and $r(M)$ after $mx^0 = 200$.
8. **Readout (§7).** Apply (A52) to the Appendix C density: what image is reconstructed from one 21 % dip?
9. **Observer (§8).** For the headset experiment: the report channel $P$, the map $q$, the tolerance $\approx$, and who evaluates. Which result of Sections 2–4 changes if the word "mind" is deleted?
10. **Convergence (§5.5).** Figure 6 at two lattice spacings and two time steps, with the energy (A74) reported.

---

## 11. Ledgers

**11.1 Claims.**

The "rests on" column is the support, never the number of reviewers who agree.

| Claim in the paper | Where | Status | Rests on | Note |
|---|---|---|---|---|
| super-radiance follows from (A1) in the "Coulomb gauge" | App. A | **Refuted as stated** | check 1; (A6)–(A8), (A12), (A38) | the gauge pair freezes the density and kills the pulse; survives only with $A^0 \neq 0$ |
| the sech pulse (A45)–(A47) | App. A | **Derived, conditional** | check 2; cited (Gross–Haroche) | bad-cavity limit of mean-field Maxwell–Bloch; all inputs supplied; no number |
| light leaves the microtubule ends and is guided | Fig. 1, §5 | **Refuted as stated** | checks 6, 7; (A10), (A13); cited (Jackson; Snyder–Love) | (A13) gives sideways, axially polarized emission; 21 nm cutoff excludes 500 nm |
| capacity 2.5 PB | §3 | **Derived from supplied factors** | PR #513 check 3, replayed here; cited (tissue optics) | $\lambda$, $n_r$, $d$, area supplied; medium assumption fails in cortex; not a memory without $r$, $\approx$ |
| the model records a hologram | App. B | **Supplied** | check 5; (A48)–(A52) | $\lvert r+o\rvert^2$ put in; $o$ has no source; depth 4.5 % |
| Appendix C is QED | App. C | **Narrowed** | check 3; (A56), (A69)–(A71) | it is the classical sector; $\Delta$, $D^{11}$, $\Gamma_2$ set to zero; the one $\hbar$ term is damped away |
| (A70) | App. C | **Misprint** | check 3 | sign of the $V^2$ term; (A81)/(A87) correct |
| $M^2$, $\gamma$ from the self-energy | (A75) | **Supplied** | (A75) text; PR #513 check 1a, replayed here; cited (Ward identity) | no formula; double-counts London; breaks the Ward identity |
| five tissue layers | §4 | **Supplied** | (A82) text | identical equations and parameters |
| control achieves binary holograms | §4 | **Narrowed** | §4 text and Fig. 5–6; check 11; §6 | one dip, 1.3–21 % contrast, open loop, decays; no image; no convergence; uncertified |
| number conservation $<10^{-6}$ % | §4 | **Witnessed** | §4 text | integrator check of (A86) only |
| Gauss's law along the run | §4 | **Open** | PR #513 check 1a, replayed here | broken by $M^2$, $\gamma$, $v$ terms; size along the run needs a rerun |
| information recorded with no thermal degradation | §5 | **Narrowed** | PR #513 check 2, replayed here; cited (Arrhenius) | write is thermally clean; retention needs ~1.2 eV, paper has 4 meV |
| Tegmark's estimate is wrong | §5 | **Open** | §5 text | even if so, no evidence moves to the alternative |
| "balance of decoherence and error corrections" | §5 | **Open** | §5 text; PO §5.18 | $h_{\text{safe}}$ with no inputs (§6.3) |
| a quantum mind registers, deciphers, decides, encodes | §5 | **Not a claim yet** | §5 text; definitions (§8.2) | rungs 2–5 with no carrier declared |
| one-to-one correspondence holograms $\leftrightarrow$ experiences | §5 | **Not a claim yet** | §5 text; definitions (§8.3) | bijection with no map; pigeonhole, blind spot, firewall |
| "how a quantum mind could perceive ... is yet another mystery" | §5 | **Witnessed, correct** | §5 text | keep it |

**11.2 Injection ledger.** Every asymmetry put in by hand, in order of appearance. A result is only as strong as the weakest row it rests on.

| Injection | Where | Needed for | Declared by the paper? |
|---|---|---|---|
| $A^0 = 0$ and $\nabla\!\cdot\!\mathbf A = 0$ with charge present | A, B | everything in App. A, B | called a gauge |
| two-level truncation, vibration along $x^3$ | (A10)–(A12) | pulse | yes |
| $A_1 = A_2 = 0$; $\mathbf k \perp x^3$ | (A13) | pulse | yes, consequences not drawn |
| rotating-wave, dipole approximations | (A16), (A24) | pulse | yes |
| resonant-shell measure $\Omega^2/4\pi$ | (A29) | $g$ | yes |
| real $J_{01} = J_{10}$, real $\mathcal A$ | after (A32) | (A33)–(A35) | yes |
| loss $\mathcal A/L_3$ | (A42) | sech | "setting the length" |
| $\partial_0 \ll 1/L_3$ | (A43) | sech | yes |
| $\theta_0$ | (A44) | $\tau_0$ | free |
| $\lambda = 500$ nm, $n_r = 1.3$, $d = 2$ mm, 2500 cm² | §3 | 2.5 PB | "as an example" |
| 1 bit per synapse, $2.5\times10^{14}$ synapses | §3 | 30 TB | yes |
| $M^2 A_i$ "for the Meissner effect" | (A48) | hologram | "we have added" |
| static $\tilde A_i = r(x^1,x^2)$ | (A50) | hologram | yes |
| $\lvert\varphi\rvert^2 \propto \lvert r+o\rvert^2$; object wave $o$ | (A51) | reconstruction | "consider the case"; $o$ has no source |
| $a^0 = 0$, $\xi = 1$ on the fluctuation | (A55) | 2PI | yes |
| $\Gamma_2 \to 0$, $D^{11} \to 0$, $\Delta^{11} \to 0$ | (A69)–(A71) | classical sector | "neglect" |
| $\Sigma_\rho \to -M^2 - \gamma\partial_0$ | (A75) | damping, mass | "factors dependent on $T$ and $e$" |
| $A_3 = 0$, homogeneity in $x^3$, $\beta \to 0$ | before (A76) | 2D run | "we omit" |
| five identical layers, coupling $v$ | (A82) | hierarchy | yes |
| static inversion, drop $\partial_0$ and the matter term | (A88)–(A89) | inputs | yes |
| $e^{-\gamma_2 x^0}$ on the input | (A90) | convergence | yes, reason given in §5 |
| targets $\pm0.1$ polygonal, $N_1 = 30$, $N_2 = 20$ | (10)–(11) | Fig. 5, 6 | yes |
| $128^2$ periodic, $ma_s = 1$, $a_t/a_s = 10^{-3}$, $e = 0.3$, $v/m^2 = 0.8$, $\gamma/m = 0.2$, $M^2 = 2m^2$, $\gamma_2/m = 0.01$ | §4 | Fig. 5, 6 | yes; $m$ never fixed |
| "binary" | §4 | Lohmann cells | 1.3–21 % contrast |
| 4 meV water scale; open system; "error corrections" | §5 | Tegmark reply | no inputs |
| end emission; 21 nm single-mode guide | Fig. 1, §5 | capacity, delivery | against (A13) |
| "one-to-one correspondence" | §5 | the headline | no map |

---

## 12. Where projection and retraction would enter

A sketch, not a derivation. If the paper's chain (§1) were taken seriously as a chain of projections $\pi_k$ with retractions $\sigma_k$, then each stage has a defect $\delta_k(x) = \lVert x - \sigma_k\pi_k x\rVert$ in a declared norm, and three of them are already computable with the paper's own objects:

- $\delta_1$: the product-retraction defect $D_e(t)$ of §6, with its rate $\nu_e$ and window; this is the price of calling a mean field "quantum".
- $\delta_3$: the phase defect of $\lvert\cdot\rvert^2$: two configurations $\bar\varphi$, $\bar\varphi e^{i\beta}$ have the same density; whether the dropped $\beta$ matters is the descent question $q(x) = q(y) \Rightarrow q(Tx) = q(Ty)$ for the map $q = \lvert\cdot\rvert^2$ under the flow $T$ of (A76)–(A87), decidable by one computation the paper omits (it "omits terms $-\partial_\mu\beta/e$").
- $\delta_4$: the threshold defect: the distance between the 21 % dip and the two-level cell it is called.

The last arrow is where a theory of experience would have to live, and it is not a projection of a field. In the programme's terms an experience report is the output of an evaluator after a re-comparison: a second record is produced (a readout $r(M)$), compared with a first under a declared $\approx$, and a status is returned. What the subject reports is the status, and what an experiment can measure is the confusion structure of $q$ on the report channel $P$. That gives an exact meaning to "one-to-one correspondence": the induced map $H/\!\approx\; \to P$ is injective. It is testable, it needs no new physics, and the headset experiment could test it once $P$, $q$ and $\approx$ are declared. Whether anything more than that can be said about experience is outside what this audit, or the paper, can derive.

---

## Companion: sources, claim ids and files

*Witnessed Difference Programme* (monograph, `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`): admitted cut CH01-D01; injection ledger §3.2; retention packet and countermodels CM1–CM5, "witness without retention", §3.3–3.6, CH03-N01; normalization nonselection CH09-P01; four-layer observer CH10-D01..D04 (presentation $(X,P,q,C)$, memory, evaluator, policy), tolerance belongs to the evaluator CH10-N01; observation ladder CH12-D01 and failure modes; observation $\neq$ authorization CH12-P01; measurement packet CH13-D01; blind spot CH14-P01; capacity and pigeonhole §14.4; awareness firewall CH14-N01/N02; target-separating report obstruction CH14-T01; authority packet CH15-D01, four separations §15.2, prose carries no authority CH15-P04; descent criterion and projection-induced memory CH16-P01; consolidated nonclaims §21.7; evidence monotonicity §21.9; editorial tests §21.13; continuum enclosure App. M.3–M.4; the five questions App. R.

*Projection Obstruction* (PO-000 v6.9.20, `atlas/projection_obstruction/projection_obstruction_paper/projection_obstruction.md`): product retraction $\Pi$, tangent and normal projectors $P_e$, $Q_e$ (§3); RE1–RE5 and the $\ell^1$ selection (Theorem 4.2; Lean `ReplicaHierarchy.unweighted_sum_of_replicaAdditive_of_singleton_calibration`); Theorem 5.1 $D_e(t) \ge \nu_e t - 24g^2t^2$, Lemma 5.3, pure-state rate $\nu_e = 2\lVert\chi\rVert$ (§5.3.1), Lindblad extension $D \ge \nu t - 6\Lambda_*^2t^2$ (§5.4.1), projection transfer (Lean `ProjectionTransfer.transfer`); Theorem 5.10.A (edge-decomposed TDVP Duhamel bound); declared Born weights §5.12; residual uncertainty and $h_{\text{safe}}$ §5.18; induced cochain versus quotient obstruction §7.2; phase information discarded by weights, Theorem 7.5; "approximation orders, not validated error bars" §7.9. Siblings: PO-033 (Duhamel bound and the HEURISTIC_UNCERTIFIED status), PO-034 §7.2 (stop rules are policies), PO-006 (reported numbers depend on the declared gauge).

*Standard physics cited, not re-derived:* Dicke 1954; Bonifacio and Lugiato 1975; Gross and Haroche, Phys. Rep. 93, 301 (1982) for $\theta_0 \approx 2/\sqrt N$, $\tau_R < T_2$ and the cooperation length; Madelung 1927; Cornwall, Jackiw and Tomboulis 1974 for the 2PI action; the Ward identity; the Proca divergence identity; Jackson for $\lambda_c = 1.706\,d$; Snyder and Love for the $V$-number; Jacques, Phys. Med. Biol. 58, R37 (2013) for tissue scattering, order of magnitude; Schlosshauer, Rev. Mod. Phys. 76, 1267 (2004) for decoherence versus collapse; Landauer 1961 and Bennett 1982 via PR #513.

*Files in this folder:* [ijms-25-02399.md](ijms-25-02399.md) (the paper, all 91 equations); [claims_ledger.md](claims_ledger.md) (definitions, printed typos); [adversarial_review.md](adversarial_review.md) and [code/adversarial_review_checks.py](code/adversarial_review_checks.py) (PR #513: Gauss's law, Landauer); [adversary_of_chatgpt.md](adversary_of_chatgpt.md) (round 1 and 2); [code/critique_checks.py](code/critique_checks.py) (this audit's eleven checks).
