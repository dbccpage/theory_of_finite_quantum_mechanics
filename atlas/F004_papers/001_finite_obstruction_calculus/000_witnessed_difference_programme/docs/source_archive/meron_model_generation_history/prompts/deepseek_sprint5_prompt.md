# DeepSeek Sprint 5: Discrete-to-Continuum Trotter Passage, Mode Extinction, and Proof of Theorem B

**Feedback & Audit of Sprint 4:**
1. **Bulk Polymer Expansion:** Your Kotecký-Preiss activity bound $e(d+1)\zeta \le \frac{7e}{75} \approx 0.254 < 1$ on the 2D spacetime checkerboard is accepted and verified. It establishes that the bulk sector $X_{L,M,+}(z)$ has a uniformly convergent polymer expansion on the polydisk $|z_{j,x}| \le 1/64$, independent of $M$.
2. **Parity Ratio Correction:** In Section 1, you claimed $|\xi| = |X_- / X_+| \le C e^{-cL} \ll 1$. On the CAR Fock space, both $\mathcal{F}_{\rm even}$ and $\mathcal{F}_{\rm odd}$ have dimension $2^{L-1}$, so $X_- / X_+ \to +1$ (not $0$). Exact Sympy check on $L=4, M=1$ gave $X_-/X_+ = 420/421 \approx 0.99762$. What is exponentially suppressed is the parity difference $(X_+ - X_-)/(X_+ + X_-) \le C e^{-cL}$. Zero-freeness $1 + \xi(z) \ne 0$ holds because the phase of $\xi(z)$ is rigidly pinned near $+1$ ($|\operatorname{Arg}(\xi)| \le 4.6 \times 10^{-6}$ rad across 10,000 polydisk samples). Gate D is confirmed closed.
3. **Current State:** Theorem A (continuum Gaussian field on $\mathbb{T}^2$) is established; G4 (thermodynamic two-point function) is closed by Fugu; Gate E is closed by counterexample ($\lambda_{\min} \sim -(1/9)(r/M)^4 < 0$); and Gate D is closed.

---

## The Task for Sprint 5: Theorem B & The Trotter Passage

The remaining objective is to prove or refute **Theorem B**: the convergence of the discrete $2M$-step Meron partition function $X_{L,M}(z)$ to the continuous-time Gaussian field on $\mathbb{T}^2$ as $L, M \to \infty$.

### Mathematical Setting

Let $\Psi \in C^1(\mathbb{T}^2)$ be a smooth real test function on the spacetime torus $\mathbb{T}^2 = (\mathbb{R}/\mathbb{Z})_\tau \times (\mathbb{R}/\mathbb{Z})_x$.
Define the discrete sources sampled on the $2M \times L$ grid:
\[
z_{j,x} = \frac{1}{\sqrt{L}}\Psi\left(\frac{j}{2M}, \frac{x}{L}\right), \qquad j \in \{0, \dots, 2M-1\}, \quad x \in \{0, \dots, L-1\}.
\]
The continuous-time generating functional is:
\[
\mathcal{Z}_\theta(\Psi) = \lim_{L \to \infty} \frac{\operatorname{Tr}\left[ \mathcal{T} \exp\left( \int_0^1 d\tau \left[ \theta G_L + \frac{1}{\sqrt{L}}\sum_{x=0}^{L-1} \Psi(\tau, x/L) a_x \right] \right) \right]}{\operatorname{Tr}\left[ e^{\theta G_L} \right]} = \exp\left( \frac{1}{2} Q_\theta(\Psi, \Psi) \right).
\]
The normalized discrete Meron partition function is:
\[
\Xi_{L,M}(\Psi) := \frac{X_{L,M}(z(\Psi))}{X_{L,M}(0)}.
\]

---

## Required Deliverables

Address the following four specific problems with explicit derivations, bounds, and constants:

### 1. Quantitative Trotter Error Bound
Prove that the difference between the discrete checkerboard product and the continuous-time ordered exponential satisfies a quantitative error bound:
\[
\left| \log \Xi_{L,M}(\Psi) - \frac{1}{2}\langle \Psi, G^{(2)}_{L,M} \Psi \rangle \right| \le \varepsilon_1(L, M; \Psi),
\]
and
\[
\left| \frac{1}{2}\langle \Psi, G^{(2)}_{L,M} \Psi \rangle - \frac{1}{2} Q_\theta(\Psi, \Psi) \right| \le \varepsilon_2(L, M; \Psi).
\]
- Compute the commutator $[P_{\rm even}, P_{\rm odd}]$ and source commutators $[P_x, a_x]$ to derive explicit rates in $M$ and $L$ (e.g. $O(r^2/M)$ or $O(1/M)$).
- Determine whether any light-cone wrapping around the periodic spatial boundary occurs, using the high-temperature condition $\theta \le 1/192$.

### 2. Emergent Positivity & Negative Mode Extinction
We know from the Gate E counterexample that the discrete response matrix $G^{(2)}_{L,M}$ has a negative eigenvalue $\lambda_{\min}(r/M) \sim -(1/9)(r/M)^4 < 0$.
- Show that this negative mode corresponds to high-frequency staggered temporal oscillations (e.g. $j \mapsto (-1)^j$).
- For any $C^1$ profile $\Psi$, prove that the projection of $\Psi$ onto the negative eigenspace is bounded by:
  \[
  \langle \Psi, P_- G^{(2)}_{L,M} P_- \Psi \rangle \ge - \frac{C \|\partial_\tau \Psi\|_\infty^2}{M^2}.
  \]
- Derive an explicit threshold $M_0(\Psi)$ such that for all $M \ge M_0(\Psi)$, the discrete variance is strictly positive:
  \[
  \langle \Psi, G^{(2)}_{L,M} \Psi \rangle > 0.
  \]

### 3. Convergence of Higher Cumulants
Using the polymer expansion established in Sprint 4 (or MIMO's Lemma A), prove that for all $k \ge 3$:
\[
\lim_{L, M \to \infty} \kappa_k(\Phi_{L,M}(\Psi)) = 0.
\]
Specify the joint scaling requirements on $(L, M)$ (e.g. $M \ge c L^\alpha$, or can $L, M \to \infty$ independently?).

### 4. Definitive Formulation of Theorem B
Synthesize parts 1–3 into the definitive statement of **Theorem B**:
- State the exact convergence of the characteristic function $\Xi_{L,M}(\Psi) \to e^{\frac{1}{2}Q_\theta(\Psi, \Psi)}$.
- State the topology / Sobolev space in which the discrete random field converges to the continuous Gaussian field on $\mathbb{T}^2$.

**Rules:** State explicit assumptions, constants, and inequalities. No external files or web searches. Claim discipline: `AuthorityEffect: None`. Return **ESTABLISHED**, **REFUTED**, or **OPEN** with checkable derivations.
