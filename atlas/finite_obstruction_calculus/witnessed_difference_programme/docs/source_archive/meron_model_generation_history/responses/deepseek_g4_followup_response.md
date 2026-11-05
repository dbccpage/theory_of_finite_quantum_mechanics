# DeepSeek Follow-Up Response: Correction and Dobrushin Reversal

**Boundary.** I inspected only the question text you supplied. No implementation files, commit hashes, or external repositories were provided in this conversation. All statements below are conditional on the CAR definitions given in the prompt. I do not claim to have read any absent file. AuthorityEffect: None.

**Important correction.** My earlier answer contained a serious error: I called \(P_x\) "quadratic" and \(T_j(q)\) a "Gaussian fermionic operator." That was wrong. \(P_x\) contains the quartic term \(-2n_x n_y\). I also wrote the kernel as the single-particle propagator \(\langle c_x c_y^\dagger\rangle\) when the source couples to the density \(a_x\). Both errors are corrected below. The Dobrushin audit also reverses my earlier pessimism.

---

## Question 1: Operator degrees and non-Gaussianity

**1.1 Expansion of \(P_x\).** With \(n_x = c_x^\dagger c_x\),

\[
P_x = \tfrac12\big(n_x + n_y - 2\,c_x^\dagger c_x c_y^\dagger c_y + c_x^\dagger c_y + c_y^\dagger c_x\big).
\]

The term \(-2n_x n_y = -2c_x^\dagger c_x c_y^\dagger c_y\) is **quartic**. The hopping terms are quadratic. So \(P_x\) is quadratic **plus** quartic. It is not Gaussian.

**1.2 \(a_x\) is quadratic.** \(a_x = (-1)^x(c_x^\dagger c_x - \tfrac12)\) is quadratic (number operator minus a constant). Correct.

**1.3 \(K_L\) is interacting.** \(K_L = \sum_x(\tfrac14 - P_x)\) contains the quartic \(n_x n_y\) term. Under Jordan–Wigner it maps to an XXZ exchange chain, not free fermions. Concretely, writing \(n_x = (1+\sigma_x^z)/2\),

\[
K_L = \tfrac14\sum_x\big(\sigma_x^z\sigma_{x+1}^z - \tfrac12(\sigma_x^x\sigma_{x+1}^x + \sigma_x^y\sigma_{x+1}^y)\big),
\]

an anisotropic exchange (XXZ with \(\Delta = -2\) relative to the XY coupling). It is **not** free fermions and **not** isotropic Heisenberg. The earlier "free-fermion quadratic Hamiltonian" claim is withdrawn.

**Consequence for the pair kernel.** Because \(K_L\) is interacting, the density–density correlator is not related to the single-particle propagator by Wick's theorem. The two are genuinely different objects.

---

## Question 2: Density–density vs. single-particle kernel

The source couples to \(a_x\), so the correct kernel is the connected **staggered density–density** correlation

\[
C_\theta(\tau,\sigma;x,y) = \langle T_\tau a_x(\tau)\,a_y(\sigma)\rangle_{\beta,c},
\]

not \(\langle c_x(\tau)c_y^\dagger(\sigma)\rangle\). My Section 4.1 was wrong.

**How the cluster expansion evaluates it.** Expand

\[
X_{L,M}(z) = q^{-LM/4}\operatorname{Tr}\prod_j T_j(q)\,e^{(1/2M)\sum_x z_{j,x}a_x}.
\]

Two derivatives \(\partial_{z_{j,x}}\partial_{z_{k,y}}\) bring down \(\frac{1}{(2M)^2}a_x(s_j)a_y(s_k)\). The cluster expansion of \(\log X\) then produces the connected density–density cumulant, with polymers built from the fluctuation factors \(T_j-1\) and \((e^{(1/2M)\sum z a}-1)\). The single-particle propagator never appears; it would require a source linear in \(c\), which is not what \(D_j(z)\) supplies.

**Why this matters for positivity.** Density–density correlators of a Hermitian operator are positive semidefinite by the spectral representation (Gate 1 of my earlier answer survives, but with \(a_x\) replacing \(c_x\)). The single-particle propagator is not positive semidefinite in the same sense.

---

## Question 3: Dobrushin / Shearer audit — reversal

The standard Kotecký–Preiss / Dobrushin criterion is: with factor norm \(\epsilon\) and overlap degree \(d\), convergence follows if

\[
e\,(d+1)\,\epsilon < 1.
\]

Plug in the prompt's numbers:

\[
e\,(7M)\,\frac{1}{256M} = \frac{7e}{256} \approx 0.0743 < 1.
\]

**The \(M\) cancels.** The factor norm's \(1/M\) is exactly compensated by the overlap degree's \(M\). The criterion is satisfied **uniformly in \(M\)**, with a margin of roughly a factor of 13.

**Correction to my earlier answer.** I claimed the temporal KP bound was "missing." That was wrong. Given the prompt's stated bounds — norm \(\le 1/(256M)\) and overlap degree \(\le 7M-1\) — the standard Dobrushin criterion **does** establish uniform polymer convergence directly. The temporal KP bound is not an open lemma; it is a consequence of the supplied bounds.

**Caveat.** The prompt states these bounds as inputs. If they are themselves unproved, the convergence is conditional on them. The prompt says "Audit this claim" — the audit is: **given** the bounds, convergence follows; **whether** the bounds hold requires separate verification against the actual \(T_j\) and \(D_j\).

**What convergence does and does not give.** Uniform convergence of the polymer expansion makes \(\log X\) analytic in the polydisk and bounds **all** cumulants, including the non-equal-time pair kernel. So the pair kernel **is** controlled by the same expansion. The prompt's warning that the static theorem "does not identify the non-equal-time pair kernel" is about **identification**, not **boundedness**. Boundedness follows from convergence; identification requires the explicit spectral representation (Question 5).

---

## Question 4: Spatial row sum vs. coincident point

Compute the variance of \(\Phi_{L,M}(\Psi)\) directly:

\[
\operatorname{Var}(\Phi) = \frac{1}{(2M)^2 L}\sum_{j,x}\sum_{k,y}\Psi\!\Big(\frac{j}{2M},\frac{x}{L}\Big)\Psi\!\Big(\frac{k}{2M},\frac{y}{L}\Big)\,C_\theta(s_j,s_k;x,y).
\]

Since \(\Psi\) is Lipschitz in the spatial argument, \(\Psi(x/L)\Psi(y/L) = |\Psi(x/L)|^2 + O(|x-y|/L)\). The leading term factorizes. Summing over \(x\) with \(y=x+u\):

\[
\sum_x |\Psi(x/L)|^2 \sum_u C_\theta(\tau,\sigma;0,u) \;\approx\; L\int dx\,|\Psi(x)|^2\;K_\theta(\tau,\sigma),
\]

where

\[
K_\theta(\tau,\sigma) = \sum_{u\in\mathbb{Z}} C_\theta(\tau,\sigma;0,u)
\]

is the **spatial row sum**. The single-point value \(C(0,0)\) would appear only if the test function were a delta at \(x=y\); for a Lipschitz profile the sum over \(u\) is what survives. The \(L\) in the prefactor cancels the \(L\) from the spatial integral, leaving the row sum.

**Correction to my earlier Section 5.2.** I wrote \(\int dx\,|\Psi|^2 K(\tau-\tau',0)\), sampling only \(x-y=0\). That was wrong: the correct object is the row sum \(\sum_u C(0,u)\), not the coincident point. The formula in the prompt is correct.

---

## Question 5: Nonzero temporal Fourier modes

The temporal kernel is \(K_\theta(\tau-\sigma) = \sum_u C_\theta(\tau,\sigma;0,u)\). Its Fourier coefficients are

\[
K_n = \int_0^1 d\tau\, K_\theta(\tau)\,e^{2\pi i n\tau}.
\]

**Spectral representation.** For a finite system,

\[
C_\theta(\tau,\sigma;x,y) = \frac{1}{Z}\sum_{m,n} e^{-\beta E_m}\langle m|a_x|n\rangle\langle n|a_y|m\rangle\, e^{(\tau-\sigma)(E_m-E_n)} - \langle a_x\rangle\langle a_y\rangle .
\]

The \(n\neq 0\) Fourier coefficients are determined by matrix elements \(\langle m|a_x|n\rangle\) with \(E_m\neq E_n\). These are nonzero whenever \(a_x\) does not commute with \(K_L\).

**Does \(a_x\) commute with \(K_L\)?** No. \(a_x = (-1)^x(n_x-\tfrac12)\) is the staggered density. The hopping term \(c_x^\dagger c_{x+1}+c_{x+1}^\dagger c_x\) changes the staggered occupation, so \([K_L,a_x]\neq 0\). Explicitly, at the level of a single bond,

\[
[K_L, a_x] \propto (-1)^x(c_x^\dagger c_{x+1} - c_{x+1}^\dagger c_x),
\]

which is nonzero. Therefore \(\langle m|a_x|n\rangle\neq 0\) for many pairs with \(E_m\neq E_n\), and \(K_n\neq 0\) for at least some \(n\neq 0\).

**Positive-temperature statement.** For \(0<\theta\le 1/192\), the thermal state is a mixed state with support on excited states. The spectral function of \(a_x\) has support at frequencies set by the charge gap \(\Delta_c\), which is nonzero for the U=t chain at half-filling. Therefore \(K_n\neq 0\) for \(n\) up to \(O(1/\Delta_c)\). The kernel does **not** collapse to a time-independent constant.

**The \(\theta=0\) case.** Even at \(\theta=0\), the ground-state correlator \(\langle 0|T_\tau a_x(\tau)a_y(0)|0\rangle_c\) has nonzero temporal Fourier modes, because \(a_x|0\rangle\) is not an eigenstate of \(K_L\). The prompt's statement "at \(\theta=0\) the source is time-constant and only the zero temporal mode remains" refers to the **classical source** \(z_{j,x}\) being \(j\)-independent, not to the quantum kernel. The quantum kernel retains nonzero modes at all temperatures.

**Cluster representation.** The polymer expansion of Question 3 gives an alternative route: the temporal decay of \(K_\theta(\tau-\sigma)\) is governed by the same exponential clustering that makes the KP sum converge. The Fourier coefficients \(K_n\) decay exponentially in \(|n|\) with a rate set by the temporal correlation length \(\xi_t = O(1/\Delta_c)\). This is consistent with the spectral representation.

**Correction to my earlier Section 4.1.** I identified the kernel with the single-particle propagator and wrote a free-fermion dispersion \(\epsilon(k)\). That was wrong for two reasons: the kernel is the density–density correlator, and the Hamiltonian is interacting. The correct identification is the staggered density–density kernel, with spectral weight at the charge gap.

---

## Summary of corrections

| Earlier claim | Correction |
|---|---|
| \(P_x\) is quadratic; \(T_j\) Gaussian | \(P_x\) is quadratic + quartic; \(K_L\) is interacting XXZ |
| Kernel = single-particle propagator | Kernel = connected staggered density–density correlator |
| Temporal KP bound is missing | Dobrushin criterion \(e(d+1)\epsilon\approx 0.0743<1\) gives uniform convergence |
| Variance samples \(C(0,0)\) | Variance samples the spatial row sum \(\sum_u C(0,u)\) |
| Free-fermion dispersion | Interacting spectral function with charge gap; nonzero temporal modes survive |

**Status of the target theorem.** With these corrections, the conditional theorem in my earlier answer survives, but its hypotheses change: the polymer convergence is **proved** by Dobrushin (given the stated bounds), the kernel is the density–density correlator, and the temporal modes are nonzero at all \(\theta\ge 0\). The remaining open gate is the **explicit identification** of the density–density kernel's continuum limit, not its boundedness.
