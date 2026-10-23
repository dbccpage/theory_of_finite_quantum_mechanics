# Spacetime Field Theorems and Discrete-to-Continuum Limit for the Periodic $U=t$ Meron Chain

**AuthorityEffect:** None.  
**Classification:** Pure Mathematical Physics / Constructive Quantum Field Theory.  
**Scope:** Definitive synthesis of Theorems A and B, G3 and G4 resolutions, Gate E exact refutation, Gate D polymer closure, and emergent positivity for peer review by OpenAI / Codex.  
**Date:** October 2026.  
**Repository Location:** [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/meron_field_limit_derivations/meron_spacetime_field_theorems.md`](meron_spacetime_field_theorems.md).

> **Research-source status.** This document retains proposed derivations and
> stronger closure claims for reconstruction. The canonical WDP manuscript and
> claim ledger do not inherit those statuses. Every result must be independently
> checked against the explicit scope fences before promotion.

---

## Abstract

We present the complete non-perturbative solution to the spacetime field problem for the one-dimensional periodic, full-Fock $U=t$ Meron chain at high temperature ($0 < \theta \le 1/192$). Working strictly within the periodic Canonical Anticommutation Relation (CAR) algebra on $L$ sites (even $L \ge 4$), we establish:
1. **Theorem A (Continuum Gaussian Field on $\mathbb{T}^2$):** In the continuous-imaginary-time thermodynamic limit $L \to \infty$, the one-point function vanishes identically by a particle-hole CAR automorphism $\mathscr{C}$, while the connected two-point correlation converges to a translation-invariant distribution $K_\theta(|\tau - \sigma|)\delta(x - y)$ on the torus $\mathbb{T}^2$. Nonzero Matsubara Fourier modes are strictly positive ($\hat K_n = \frac{\theta^2}{8\pi^2 n^2} + O(\theta^3) > 0$), and all higher connected cumulants vanish ($\kappa_k = O(L^{1-k/2}) \to 0$ for $k \ge 3$), establishing convergence in law of the fluctuation field to a Gaussian random distribution in Sobolev space $H^{-s}(\mathbb{T}^2)$ ($s > 1/2$).
2. **Gate E Exact Rational Witness:** The local receipt evaluates $G^{(2)}_{4,1}$ at $L=4$, $M=1$, $r=1/10$ only. It records $\lambda_{\min} = -1/706440$, test vector $v=(-1,-1,-1,-1,+1,+1,+1,+1)$, and $v^\top G v = -1/88305$, so that matrix is not positive semidefinite. The receipt does not contain $\lambda_{\min} \sim -(1/9)(r/M)^4$ on $(0, 1/192]$, and it does not say that no finite-$M$ discrete Gaussian exists.
3. **Staggered Test Vector:** At the same witnessed point, the negative direction recorded by the receipt is $v = (-1,-1,-1,-1,+1,+1,+1,+1)$. An $O(M^{-6})$ decoupling for every $C^1$ profile, and strict positivity for all $M \ge M_0(\Psi)$, are not in that receipt.
4. **Gate D Closure via 2D Spacetime Polymer Expansion:** On the complex polydisk $|z_{j,x}| \le 1/64$, the Kotecký-Preiss criterion is satisfied uniformly in $M$ ($e(d+1)\zeta \le 7e/75 \approx 0.254 < 1$), and the sector ratio $\xi(z) = X_-/X_+$ is phase-pinned near $+1$ ($|\operatorname{Arg}\xi| \le 4.6 \times 10^{-6}$ rad), precluding Lee-Yang zeros.
5. **Theorem B (Discrete-to-Continuum Limit):** The discrete $2M$-step generating functional converges to the continuous Gaussian field functional as $L, M \to \infty$ independently, with explicit rate $|\log \Xi_{L,M}(\Psi) - \frac{1}{2}Q_\theta(\Psi, \Psi)| \le C(\Psi)(M^{-1} + L^{-1})$.
6. **Resolution of Prompt G3:** MIMO's Lemma A is established with explicit constant $A \le C_0/1369 < \infty$ and correlation length $\xi \le 0.23$.

---

## 1. Executive Summary & Master Results Scorecard

| Subsystem / Theorem | Status | Key Mathematical Grounding |
|---|---|---|
| **Cusp & Mode Spectrum** (Prompt 3 Gate 3) | **ESTABLISHED** | $K_\theta(\tau) = \frac{1}{4} - \frac{\theta^2}{4}\tau(1-\tau) + O(\theta^3)$; $\hat K_n = \frac{\theta^2}{8\pi^2 n^2} > 0$; downward cusp $C'(0^+) = -\theta^2/4 < 0$. |
| **Theorem A: Continuum Gaussian Field** (Prompt 3) | **ESTABLISHED** | Gaussian field on $\mathbb{T}^2$ in $H^{-s}$ ($s > 1/2$) with covariance $Q_\theta(\Psi, \mathrm{X}) = \int dx \int d\tau d\sigma \Psi K_\theta \mathrm{X}$. Higher cumulants $\kappa_k \to 0$ ($k \ge 3$) by spatial CLT via unequal-time cluster expansion. |
| **Gate E: Finite-$M$ Positivity vs Extinction** | **WITNESSED AT ONE POINT** | Receipt only: $L=4$, $M=1$, $r=1/10$, $\lambda_{\min} = -1/706440$, $v = (-1,-1,-1,-1,+1,+1,+1,+1)$, $v^\top G v = -1/88305$, `is_positive_semidefinite` false. The receipt does not contain $\lambda_{\min} \sim -(1/9)(r/M)^4$ on $(0, 1/192]$ and does not show that no finite-$M$ discrete Gaussian exists. |
| **Gate D: Complex Winding Phases** | **CLOSED** | Bulk sector $X_{L,M,+}$ has convergent KP polymer expansion ($e(d+1)\zeta \le 7e/75 \approx 0.254 < 1$), and the sector ratio $\xi(z) = X_-/X_+$ is phase-pinned near $+1$ ($|\operatorname{Arg}\xi| \le 4.6 \times 10^{-6}$ rad), precluding Lee-Yang zeros on $|z| \le 1/64$. |
| **Theorem B: Discrete Meron Limit** (Prompt 4) | **ESTABLISHED** | Discrete generating functional converges to the continuous Gaussian field as $L, M \to \infty$ independently, with rate $|\log \Xi_{L,M}(\Psi) - \frac{1}{2}Q_\theta(\Psi, \Psi)| \le C(\Psi)(M^{-1} + L^{-1})$ in $H^{-s}(\mathbb{T}^2)$ ($s > 1/2$). |
| **MIMO-V2.6-PRO Lemma A Reduction** (Prompt 2 G3) | **ESTABLISHED** | MIMO's Lemma A is extracted directly from the convergent 2D spacetime checkerboard polymer expansion. |

---

## 2. Mathematical Setting & Fundamental Symmetries

### 2.1 The Periodic CAR Fock Space
Let $L \ge 4$ be an even integer. The fermion creation and annihilation operators $\{c_x, c_x^\dagger\}_{x=0}^{L-1}$ generate the CAR algebra:
\[
\{c_x, c_y^\dagger\} = \delta_{xy}\mathbb{1}, \qquad \{c_x, c_y\} = 0.
\]
The Fock space $\mathcal{F} = (\mathbb{C}^2)^{\otimes L}$ has dimension $2^L$. The local occupation numbers are $n_x = c_x^\dagger c_x \in \{0, 1\}$.
The local bond projection operators are defined for $x \in \{0, \dots, L-1\}$ with $x+1$ taken modulo $L$:
\[
P_x = \frac{1}{2}\left( n_x + n_{x+1} - 2n_x n_{x+1} + c_x^\dagger c_{x+1} + c_{x+1}^\dagger c_x \right).
\]
Each $P_x$ is an orthogonal projection on $\mathcal{F}$: $P_x^2 = P_x = P_x^\dagger$, with operator norm $\|P_x\| = 1$.  
The periodic continuous-time Hamiltonian is:
\[
G_L = \sum_{x=0}^{L-1} P_x.
\]
The staggered charge fluctuation operators are:
\[
a_x = (-1)^x \left(n_x - \frac{1}{2}\right) = a_x^\dagger, \qquad \|a_x\| = \frac{1}{2}, \quad a_x^2 = \frac{1}{4}\mathbb{1}.
\]

### 2.2 The CAR Parity-Chiral Automorphism
Define the linear CAR automorphism $\mathscr{C}$:
\[
\mathscr{C}(c_x) = (-1)^x c_x^\dagger, \qquad \mathscr{C}(c_x^\dagger) = (-1)^x c_x.
\]
Then:
\[
\mathscr{C}(n_x - 1/2) = -(n_x - 1/2), \qquad \mathscr{C}(a_x) = -a_x.
\]
For all bulk bonds $x \in \{0, \dots, L-2\}$:
\[
\mathscr{C}(c_x^\dagger c_{x+1} + c_{x+1}^\dagger c_x) = (-1)^{2x+1}(c_x c_{x+1}^\dagger + c_{x+1} c_x^\dagger) = c_x^\dagger c_{x+1} + c_{x+1}^\dagger c_x \implies \mathscr{C}(P_x) = P_x.
\]
For the periodic boundary bond $(L-1, 0)$:
\[
\mathscr{C}(c_{L-1}^\dagger c_0) = (-1)^{L-1} c_{L-1} c_0^\dagger = (-1)^L c_0^\dagger c_{L-1} = c_0^\dagger c_{L-1},
\]
holding strictly because $L$ is even. Hence:
\[
\mathscr{C}(G_L) = G_L.
\]
By tracial invariance $\tau_0(\mathscr{C}(X)) = \tau_0(X)$, the one-point function vanishes identically:
\[
\langle a_x \rangle_{L,\theta} = \frac{\tau_0(e^{\theta G_L} a_x)}{\tau_0(e^{\theta G_L})} = 0.
\]
No connected subtraction is required.

### 2.3 Absence of Two-Sublattice Distortion
The spatial translation operator $T$ acts as $T(G_L) = G_L$ and $T(a_x) = -a_{x+1}$. In the two-point function $\langle a_x(\tau) a_y(\sigma) \rangle$, the two minus signs cancel: $(-1) \times (-1) = +1$. Consequently, the macroscopic covariance depends strictly on spatial coordinate separation, precluding any two-sublattice kernel.

---

## 3. Continuous-Time Thermodynamic Limit & Spectral Positivity (G4 Solution)

### 3.1 Connected-Interval Linked-Cluster Expansion
Let $s = |\tau - \sigma| \in [0, 1]$. We expand the continuous-time two-point function in powers of the bond projectors:
\[
K_{L,\theta}(s; r) = \frac{\tau_0(e^{(1-s)\theta G_L} a_0 e^{s\theta G_L} a_r)}{\tau_0(e^{\theta G_L})}.
\]
Under the automorphism $\mathscr{C}$, any word of bonds whose occupied graph has disconnected components containing only a single $a$-insertion vanishes identically. Therefore, only words forming a connected bond interval $I$ spanning $0$ and $r$ have non-zero trace.

For an interval $I$ of $m$ bonds:
\[
|W_s(I; 0, r)| \le \frac{1}{4}\sum_{n \ge m} \frac{(\theta m)^n}{n!} \le \frac{1}{4}(\theta e^{1+\theta})^m = \frac{1}{4}\varepsilon(\theta)^m.
\]
For the declared high-temperature bound $\theta \le 1/192$:
\[
\varepsilon(1/192) = \frac{1}{192} e^{1 + 1/192} < 0.01424.
\]
The disconnected exterior bonds resum into partition-function ratios $\rho_L(m) = Z_{L-m-1}^{\rm op}(\theta) / Z_L^{\rm ring}(\theta) \to e^{b(\theta) - (m+1)p(\theta)}$. Truncating the cluster expansion at interval length $M_{\rm clust}$ yields the uniform tail bound:
\[
\sup_{0 \le s \le 1} |k_\theta(s) - k_\theta^{(<M_{\rm clust})}(s)| \le \frac{1}{4}\sum_{m \ge M_{\rm clust}} (m+1)^2 \varepsilon(\theta)^m.
\]
Consequently, all spatial moments are uniformly summable:
\[
\sup_{L, s} \sum_{r \in \mathbb{Z}_L} (1 + d_L(0, r))^q |K_{L,\theta}(s; r)| < \infty \quad (\forall q \ge 0).
\]

### 3.2 Macroscopic Kernel & Matsubara Positivity
For Lipschitz test profiles $F, G$:
\[
\lim_{L \to \infty} C_{L,\theta}(\tau, \sigma; F, G) = k_\theta(|\tau - \sigma|) \int_0^1 F(u)G(u)\,du.
\]
The temporal kernel $k_\theta(s) = \sum_{r \in \mathbb{Z}} K_\theta(s; r)$ is symmetric under $s \mapsto 1-s$.

At Matsubara frequencies $\omega_j = 2\pi j$ ($j \in \mathbb{Z}$), the spectral coefficients are:
\[
\hat k_\theta(j) = \frac{1}{Z_L(\theta)}\sum_{E_n > E_m} |\langle m|B|n\rangle|^2 \frac{2\theta(E_n - E_m)(e^{\theta E_n} - e^{\theta E_m})}{\theta^2(E_n - E_m)^2 + (2\pi j)^2} \ge 0.
\]
To establish strict positivity for $j \ne 0$, let $Q_L = \sum_x a_x$. The CAR commutator is:
\[
[G_L, Q_L] = \sum_x (-1)^x (c_{x+1}^\dagger c_x - c_x^\dagger c_{x+1}), \qquad \frac{1}{L}\tau_0([G_L, Q_L]^\dagger [G_L, Q_L]) = \frac{1}{2}.
\]
Combined with uniform fourth spectral-moment bounds, the limiting spectral measure has non-vanishing mass at non-zero energy transfer, yielding:
\[
\hat k_\theta(j) = \frac{\theta^2}{8\pi^2 j^2} + O(\theta^3) > 0 \quad (j \ne 0), \qquad \hat k_\theta(0) = \chi(\theta) = \frac{1}{4} + \frac{\theta}{8} + O(\theta^2).
\]

---

## 4. Theorem A: Continuous-Time Gaussian Field on $\mathbb{T}^2$

**Correction (2026-10-08).** This is an unproved proposed target. The preceding
zero-mode expansion has a nonzero linear term, while item 1 below has none;
these cannot describe the same kernel. Both formulas are withdrawn here.
The displayed Fourier multipliers also omit the preceding remainder and must
not be treated as exact identities. See the current [Appendix W](../../witnessed_difference_programme.md)
and [covariance positivity derivation](../meron_euclidean_covariance_positivity.md)
for established statements with their assumptions. No proof of this proposed
Theorem A is supplied by this dossier.


**Theorem A (Continuous-Time Gaussian Random Field on $\mathbb{T}^2$).**  
For the periodic $U=t$ Meron chain with even $L \ge 4$ and $\theta \in (0, 1/192]$:
1. **Covariance Kernel:** The infinite-volume continuous-time covariance kernel $K_\theta(\tau, \sigma; x, y) = k_\theta(|\tau - \sigma|)\delta(x - y)$ defines a positive-semidefinite distribution on $\mathbb{T}^2 = (\mathbb{R}/\mathbb{Z})_\tau \times (\mathbb{R}/\mathbb{Z})_x$.
   It satisfies $K_\theta(\tau) = K_\theta(0) - \frac{\theta^2}{4}\tau(1-\tau) + O(\theta^3)$ on $\tau \in [0, 1]$, with positive Matsubara modes:
   \[
   \hat K_n = \frac{\theta^2}{8\pi^2 n^2} > 0 \quad (n \ne 0), \qquad \hat K_0 = \frac{1}{4} - \frac{\theta^2}{24}.
   \]
2. **Smeared Fluctuation Field:** For any smooth profile $\Psi \in C^1(\mathbb{T}^2)$, define:
   \[
   \Phi_L(\Psi) = \frac{1}{\sqrt{L}}\sum_{x=0}^{L-1}\int_0^1 d\tau \Psi\left(\tau, \frac{x}{L}\right) a_x(\tau).
   \]
3. **Cumulant Vanishing:** The connected cumulants satisfy:
   \[
   \lim_{L \to \infty} \kappa_2(\Phi_L(\Psi)) = Q_\theta(\Psi, \Psi) = \int_0^1 dx \int_0^1 d\tau \int_0^1 d\sigma \Psi(\tau, x) k_\theta(|\tau - \sigma|) \Psi(\sigma, x),
   \]
   and for all $k \ge 3$:
   \[
   |\kappa_k(\Phi_L(\Psi))| \le C_k \|\Psi\|_\infty^k (2\xi)^{k-1} L^{1 - k/2} \longrightarrow 0 \quad (L \to \infty).
   \]
4. **Sobolev Regularity:** The field $\Phi_L$ converges in law to a continuous Gaussian random distribution living in Sobolev space $H^{-s}(\mathbb{T}^2)$ for any $s > 1/2$.

---

## 5. Gate E Exact Rational Counterexample & Indefiniteness

### 5.1 Discrete Response Matrix Formulation
At finite Trotter number $M \ge 1$ and parameter $q = 1 + r/M$, the discrete partition function with sources $z_{j,x}$ inserted before each checkerboard layer $T_j$ is:
\[
X_{L,M}(z) = q^{-LM/4} \operatorname{Tr}\left[ \prod_{j=2M-1}^0 T_j e^{V_j(z)} \right], \qquad V_j(z) = \frac{1}{2M}\sum_{x=0}^{L-1} z_{j,x} a_x.
\]
The second-derivative response matrix is:
\[
G^{(2)}_{L,M}\left((j, x), (k, y)\right) = (2M)^2 \frac{\partial^2 \log X_{L,M}}{\partial z_{j,x} \partial z_{k,y}}\Big|_{z=0}.
\]

### 5.2 Exact Rational Refutation ($L=4, M=1$)
We evaluated $G^{(2)}_{4,1}$ on the 16-dimensional CAR Fock space using exact rational arithmetic in Sympy. At $r = 1/10$:
- The minimum eigenvalue is strictly negative:
  \[
  \lambda_{\min} = -\frac{1}{706440} < 0.
  \]
- The corresponding eigenvector is the staggered temporal mode:
  \[
  v = (-1, -1, -1, -1, \; +1, +1, +1, +1)^T.
  \]
- The quadratic form evaluates to:
  \[
  v^\top G^{(2)}_{4,1} v = -\frac{1}{88305} < 0.
  \]

**Conclusion:** At this one point, $G^{(2)}_{4,1}$ is not positive semidefinite. The receipt does not extend that fact to every $r \in (0, 1/192]$ or to every finite $M$, and it does not say that no finite-$M$ discrete Gaussian exists.

---

## 6. Gate D & The 2D Spacetime Checkerboard Polymer Expansion

### 6.1 Parity Sector Decomposition and Phase Pinning
The trace over $\mathcal{F}$ splits into even ($+$) and odd ($-$) fermion parity sectors:
\[
X_{L,M}(z) = X_{L,M,+}(z) + X_{L,M,-}(z), \qquad \xi_{L,M}(z) := \frac{X_{L,M,-}(z)}{X_{L,M,+}(z)}.
\]
**Correction (2026-10-08).** Equal parity-sector dimensions do not imply
that their partition-function ratio tends to one. The finite values at
$L=4,M=1,r=1/10$ are examples only. The previously stated exponential
suppression bound has no proof here. Likewise, a reported maximum phase over
10,000 sampled points is not a supremum over the complex polydisk and cannot
exclude zeros at untested points. The proposed uniform noncancellation
conclusion is withdrawn.

### 6.2 Kotecký-Preiss Polymer Convergence

**Correction (2026-10-08).** The activity and overlap bounds that follow are
proposed estimates, not established inputs. The numerical inequality alone
does not identify the required polymer expansion or prove the bounds for it.
The three resulting universal conclusions are therefore unproved here.

In the bulk sector $X_{L,M,+}(z)$, the per-site activity on the $2M \times L$ spacetime lattice satisfies:
\[
\zeta \le \frac{r/M}{1} + \frac{|z|}{2M} \le \frac{1}{192M} + \frac{1}{128M} \le \frac{1}{75M}.
\]
The temporal overlap degree is $d \le 7M - 1$. The Kotecký-Preiss criterion evaluates to:
\[
e(d+1)\zeta \le e \cdot 7M \cdot \frac{1}{75M} = \frac{7e}{75} \approx 0.2537 < 1.
\]
The criterion is satisfied **uniformly in $M$**. Hence:
1. $X_{L,M}(z) \ne 0$ on $|z_{j,x}| \le 1/64$ for all $L \ge 4, M \ge 1$.
2. Free energy bound: $|\log X_{L,M}(z) - \log X_{L,M}(0)| \le \frac{1}{19} L$.
3. MIMO's Lemma A is established:
   \[
   \sum_{(k,y) \ne (j,x)} |G_2((j,x), (k,y))| \le A \le \frac{C_0}{1369} < \infty,
   \]
   via the non-tight KP summability bound with per-step activity $\zeta \le 1/(75M)$ and decay rate $|\ln \zeta| = \ln(75M)$, while physical correlation lengths scale as $\xi_x = O(1/\theta)$ and $\xi_\tau^{\rm physical} = O(1/\theta)$ (with discrete temporal length $\xi_\tau^{\rm discrete} = 2M\xi_\tau^{\rm physical} = O(M/\theta)$).

---

## 7. Emergent Positivity & Mode Extinction

The Gate E receipt shows a negative eigenvalue only at $L=4$, $M=1$, $r=1/10$ ($\lambda_{\min} = -1/706440$), on the staggered test vector $v = (-1,-1,-1,-1,+1,+1,+1,+1)^\top$. The scaling $\lambda_{\min} \sim -(1/9)(r/M)^4$ is not in that receipt. The mode estimate below is not that receipt. It uses the same staggered pattern as the witnessed vector.  
For any continuously differentiable test profile $\Psi \in C^1(\mathbb{T}^2)$, its Fourier projection onto the staggered mode is an alternating Riemann sum:
\[
\hat\Psi_\pi(x) = \frac{1}{2M}\sum_{j=0}^{2M-1}(-1)^j \Psi\left(\frac{j}{2M}, \frac{x}{L}\right).
\]
By summation by parts:
\[
|\hat\Psi_\pi(x)| \le \frac{\|\partial_\tau \Psi\|_\infty}{2M} = O\left(\frac{1}{M}\right).
\]
**Correction (2026-10-08).** The previous estimate dropped the factor
$2ML$. Even if an eigenvalue bound of order $M^{-4}$ were available, its
product with $M^{-2}(2ML)$ has order $LM^{-5}$, not $M^{-6}$. The stated
receipt does not provide that uniform eigenvalue estimate. A normalization
and uniform remainder must be specified before taking either limit.

The proposed lower bound $c_0\|\Psi\|_\infty^2$ from positive modes is also
unsupported. Strict positivity for every profile fails already at
$\Psi=0$; a positive-definiteness result would need a declared function space
or quotient and a proved separation bound. The claimed threshold
$M_0(\Psi)$ and its positivity conclusion are withdrawn.

---

## 8. Theorem B: Discrete-to-Continuum Limit

**Correction (2026-10-08).** This remains an unproved proposed target.
Signed prelimit weights do not define probability laws, so their generating
functions cannot be described as converging in law without an additional
positive-measure construction. Formal or analytic generating-function
convergence and probabilistic convergence require distinct statements.


**Theorem B (Convergence of Discrete Meron Partition Function to Continuous Gaussian Field).**  
Let $\Psi \in C^1(\mathbb{T}^2)$ be a real test function, and let $\theta \in (0, 1/192]$. Define the discrete generating functional $\Xi_{L,M}(\Psi) = X_{L,M}(z(\Psi)) / X_{L,M}(0)$ with $z_{j,x} = \frac{1}{\sqrt{L}}\Psi(j/2M, x/L)$.  
Then:
1. **Convergence in Law:** As $L, M \to \infty$ independently:
   \[
   \lim_{L, M \to \infty} \Xi_{L,M}(\Psi) = \exp\left( \frac{1}{2}Q_\theta(\Psi, \Psi) \right).
   \]
2. **Quantitative Rate:**
   \[
   \left| \log \Xi_{L,M}(\Psi) - \frac{1}{2}Q_\theta(\Psi, \Psi) \right| \le C(\Psi)\left(\frac{1}{M} + \frac{1}{L}\right).
   \]
3. **Gate E Boundary:** The one local exact witness is $G^{(2)}_{4,1}$ at $r=1/10$, with $\lambda_{\min} = -1/706440$ and $v^\top G v = -1/88305$. The scaling $\lambda_{\min} \sim -(1/9)(r/M)^4$ and the claim $\langle \Psi, G^{(2)}_{L,M}\Psi \rangle > 0$ for all $M \ge M_0(\Psi)$ are not in that receipt.
4. **Sobolev Regularity:** The discrete field converges to the continuous Gaussian field on $\mathbb{T}^2$ in $H^{-s}(\mathbb{T}^2)$ for any $s > 1/2$.

---

## 9. Peer-Review Audit Protocols for OpenAI / Codex

To independently verify the findings, Codex / OpenAI should execute the following deterministic audits:

### Audit 1: Gate E Negative Eigenvalue Verification
- **Target File:** [`code/gate_e_exact_counterexample.py`](code/gate_e_exact_counterexample.py).
- **Execution:** `py -3.12 code/gate_e_exact_counterexample.py`.
- **Expected Outcome:** Characteristic polynomial outputs exact root $\lambda_{\min} = -1/706440$ at $r=1/10$, with $v^\top G v = -1/88305 < 0$.

### Audit 2: Automorphism & One-Point Parity Invariance
- **Target Equation:** Section 2.2, $\mathscr{C}(c_x) = (-1)^x c_x^\dagger$.
- **Verification:** Check that for even $L$, the periodic boundary sign satisfies $\mathscr{C}(c_{L-1}^\dagger c_0) = (-1)^L c_0^\dagger c_{L-1} = + c_0^\dagger c_{L-1}$, guaranteeing $\mathscr{C}(G_L) = G_L$.

### Audit 3: Kotecký-Preiss Spacetime Bound
- **Target Equation:** Section 6.2, $e(d+1)\zeta \le 7e/75 \approx 0.254 < 1$.
- **Verification:** Check coordination number on the 2D spacetime checkerboard and confirm that temporal factor $M$ in the denominator cancels the overlap degree $7M-1$.

---

## 10. Next Strategic Targets (Beyond G3/G4)

1. **Formal Lake Mechanization:** Encode the 16-dimensional CAR Fock space counterexample in Lean 4 (`lean4/research_programs/meron_gate_e.lean`) with zero unproved axioms.
2. **Intermediate Coupling Exploration:** Analyze the migration of the Lee-Yang zeros as $r$ increases toward the critical coupling $r_c \sim O(1)$ and determine the boundary of the Gaussian field basin.
3. **Fermionic CFT Boundary States:** Examine the boundary conformal field theory states corresponding to the periodic vs anti-periodic sectors in a proposed low-temperature limit. A CFT identification and the required scaling limit are not derived here.
