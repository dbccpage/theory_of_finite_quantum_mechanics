# WDP-O12-REAL-TIME

Goal id: WDP-O12-REAL-TIME

Selected scope for WDP-O12-REAL-TIME is recorded in this note.

The plan row is open. Its `depends_on` list is empty and it names no fence. Its statement is that real-time or spectral-density claims for the Euclidean row-sum covariance are not supplied. O.12 lists those claims under what is not proved, and the thermodynamic-limit scope sentence supplies none. This note does not fill that absence. It records only the infinite-temperature atomic moments of one finite staggered row-sum. No Python, Rust, or Lean kernel was run. The arithmetic below is the normalized trace already used in EP-9, rewritten in the integer scaling stored by `car.ring`.

## Selected scope

Labelled carrier: periodic full-Fock CAR ring of even length \(L=4\) (dimension 16), with \(K_L\) and staggered row-sum \(A_L=\sum_x a_x\) as in TL-0. The same three rationals hold for every even \(L\ge 4\) by the edge-trace argument below, not by copying the \(L=4\) integers onto a larger ring. State: infinite-temperature normalized trace. Real time: \(A(t)=\exp(it K_L) A_L \exp(-it K_L)\). Atomic spectral measure

\[
\mu_L=(L\,2^L)^{-1}\sum_{\alpha,\beta}\lvert\langle\alpha\rvert A_L\rvert\beta\rangle\rvert^2\,\delta_{E_\beta-E_\alpha}.
\]

Excluded: \(\theta>0\), any Lebesgue spectral density, \(L\to\infty\), and the section 20.12 four-site Trotter covariance.

## Hypotheses

H1. \(L\) is even and at least 4. The carrier is the full \(2^L\)-dimensional periodic CAR ring of TL-0, with the physical Jordan–Wigner sign on the wrapping bond. The labelled ring is \(L=4\), dimension 16. Nothing below passes to an infinite volume.

H2. \(P_x\), \(K_L=\sum_x(I/4-P_x)\) and \(a_x=(-1)^x(n_x-1/2)\) are the TL-0 data. In the occupation basis \(K_L\) is real symmetric and each \(a_x\) is real diagonal, as EP-1 records. Set \(A_L=\sum_x a_x\).

H3. The state is the normalized trace \(\tau=2^{-L}\operatorname{Tr}\). This is the \(\theta=0\) case of TL-0, not a positive-temperature Gibbs state \(\rho=\exp(-\theta K_L)/\operatorname{Tr}\exp(-\theta K_L)\).

H4. Real time is the unitary group of this same \(K_L\). Write \(A(t)=\exp(it K_L)A_L\exp(-it K_L)\) and \(s_L(t)=L^{-1}\tau(A(t)A_L)\). In a real eigenbasis of \(K_L\), with energies \(E_\alpha\), \(s_L\) is the Fourier transform of the atomic measure \(\mu_L\) displayed above. The Boltzmann weights of EP-4 are not used.

H5. Let \(j_x=c_x^*c_{x+1}-c_{x+1}^*c_x\), indices modulo \(L\). The density part of each \(P_x\) commutes with every \(n_z\), hence with \(A_L\). EP-9 records the identity \([K_L,A_L]=\sum_x(-1)^x j_x\).

H6. The Euclidean kernel \(C^L_{xy}(u)=\operatorname{Tr}(\rho\, a_x(u)a_y)\) with \(a_x(u)=\exp(u\theta K_L)a_x\exp(-u\theta K_L)\) stays an imaginary-time correlation. EP-2 says it is not real-time dynamics. The circle coefficients \(\widehat k_{L,\theta}(m)\) are not re-read as a density on the line.

## Derivation

### 1. Equal-time mass

Since \(n_x^2=n_x\), \(a_x^2=I/4\). For \(x\neq y\),

\[
\tau\bigl((n_x-\tfrac12)(n_y-\tfrac12)\bigr)
=\tau(n_xn_y)-\tfrac12\tau(n_x)-\tfrac12\tau(n_y)+\tfrac14
=\tfrac14-\tfrac14-\tfrac14+\tfrac14=0,
\]

because \(\tau(n_x)=1/2\) and distinct number operators factorize under \(\tau\). The cross terms in \(A_L^2\) therefore drop, and \(\tau(A_L^2)=L/4\). Hence \(s_L(0)=1/4\), which is the total mass of \(\mu_L\).

At \(\theta=0\), TL-5 and the sentence after EP-8 give \(C^L_{0y}=\delta_{0y}/4\), so the Euclidean row-sum is the constant \(k_{L,0}(u)=1/4\). Translation sends \(a_x\) to \(-a_{x+1}\) and preserves \(\tau\), so

\[
k_{L,0}(u)=L^{-1}\tau(A_L^2)=s_L(0).
\]

That common number is the equal-time value of this one row-sum. It is not a spatial continuum sum and not a sum over a second time index.

### 2. The commutator

Write \(h_x=c_x^*c_{x+1}+c_{x+1}^*c_x\), so the hopping part of \(P_x\) is \(h_x/2\). Only \(a_x\) and \(a_{x+1}\) fail to commute with \(h_x\). With \(s=(-1)^x\),

\[
a_x+a_{x+1}=s(n_x-n_{x+1}).
\]

The CAR identities \([n_x,h_x]=j_x\) and \([n_{x+1},h_x]=-j_x\) give \([h_x,n_x-n_{x+1}]=-2j_x\), hence \([h_x,a_x+a_{x+1}]=-2s\,j_x\). The density terms contribute nothing, and

\[
[K_L,A_L]=-\sum_x\tfrac12[h_x,A_L]=\sum_x(-1)^x j_x,
\]

which is the identity EP-9 records.

### 3. Odd moment

\(K_L\) and \(A_L\) are Hermitian, and a real eigenbasis exists because \(K_L\) is real symmetric. Swapping \(\alpha\) and \(\beta\) sends \(\omega=E_\beta-E_\alpha\) to \(-\omega\) and preserves \(\lvert\langle\alpha\rvert A_L\rvert\beta\rangle\rvert^2\). The infinite-temperature weight \(2^{-L}\) does not prefer either side. Thus \(\mu_L\) is even, \(\int\omega\,d\mu_L=0\), and \(s_L'(0)=0\).

Cyclicity gives the same vanishing without the eigenbasis. \(\operatorname{Tr}(A_LKA_L)=\operatorname{Tr}(KA_L^2)\), so \(\operatorname{Tr}(A_L[K_L,A_L])=0\). In the real eigenbasis that trace is \(\sum_{\alpha,\beta}(E_\beta-E_\alpha)\lvert A_{\alpha\beta}\rvert^2\), which is \(L\,2^L\) times the first moment.

### 4. Second moment

Let \(c=c_x\) and \(d=c_{x+1}\) on distinct modes, and set \(j=c^*d-d^*c\). Then \(j^*=-j\), and the two middle words in \(j^*j\) each contain \(c^2\) or \(d^2\) after one anticommutation, so they vanish. The remaining words are

\[
d^*cc^*d=n_d-n_cn_d,\qquad c^*dd^*c=n_c-n_cn_d.
\]

Hence \(j_x^*j_x=n_x+n_{x+1}-2n_xn_{x+1}\). Under \(\tau\) this expectation is \(1/2+1/2-2\cdot(1/4)=1/2\). EP-9 calls this the squared trace of one edge hop.

For \(x\neq y\) the same normalized trace vanishes. Each monomial in \(j_x^*j_y\) is a product of one hop on edge \(x\) and one hop on edge \(y\). If the edges are disjoint, four distinct modes each appear once, so the occupation basis has an empty diagonal. If the edges share a site, three modes appear and at least one of them has unequal creator and annihilator count, so the diagonal is empty again. The only extra Kronecker in the four-point formula

\[
\tau(c_p^*c_qc_r^*c_s)=\tfrac14\bigl(\delta_{pq}\delta_{rs}+\delta_{ps}\delta_{qr}\bigr)
\]

that could see the same two sites from two bond indices requires \(y=x+1\) and \(y+1\equiv x\pmod L\), hence \(L=2\). The ring hypothesis \(L\ge 4\) excludes it. Therefore \(\tau(j_x^*j_y)=0\) for \(x\neq y\).

The signs \((-1)^{x+y}\) equal \(1\) on the diagonal, so

\[
\tau\bigl([K_L,A_L]^*[K_L,A_L]\bigr)=\sum_x\tau(j_x^*j_x)=L/2.
\]

The matrix element \(\langle\beta\rvert[K_L,A_L]\rvert\alpha\rangle=(E_\beta-E_\alpha)\langle\beta\rvert A_L\rvert\alpha\rangle\) converts the left side into the second moment:

\[
\int\omega^2\,d\mu_L=L^{-1}\tau\bigl([K_L,A_L]^*[K_L,A_L]\bigr)=\tfrac12.
\]

Since \(\mu_L\) is even, \(s_L(t)=\int\cos(t\omega)\,d\mu_L\), and \(s_L''(0)=-1/2\).

EP-9 uses this same trace as the coefficient of the Euclidean small-\(\theta\) expansion,

\[
\widehat k_{L,\theta}(m)=\frac{\theta^2}{L\,2^L\omega_m^2}\operatorname{Tr}([K_L,A_L]^*[K_L,A_L])+O_L(\theta^3)=\frac{\theta^2}{2\omega_m^2}+O_L(\theta^3),
\]

for each fixed even \(L\) and \(m\neq 0\). That is an imaginary-time circle coefficient. It is not a value of \(s_L\) and not a density \(\rho(\omega)\).

### 5. Integers on the labelled ring, and the traces for general even \(L\)

The unnormalized traces are \(\operatorname{Tr}(A_L^2)=L\,2^{L-2}\) and \(\operatorname{Tr}([K_L,A_L]^*[K_L,A_L])=L\,2^{L-1}\), with \(\operatorname{Tr}(A_L[K_L,A_L])=0\). Dividing by \(L\,2^L\) returns the moments \(1/4\), \(0\) and \(1/2\) for every even \(L\ge 4\).

`car.ring` stores the integer matrices \(K_4=4K_L\) and \(2a_x\). On \(L=4\) set \(A_2=\sum_x 2a_x=2A_L\). Then \([K_4,A_2]=8[K_L,A_L]\). The unscaled traces are \(16\), \(0\) and \(32\). The scaled traces are

\[
\operatorname{Tr}(A_2^2)=4\cdot 16=64,
\]

\[
\operatorname{Tr}(A_2[K_4,A_2])=0,
\]

\[
\operatorname{Tr}([K_4,A_2]^{\mathsf T}[K_4,A_2])=64\cdot 32=2048.
\]

The transpose is the adjoint because these matrices are real. For a general even \(L\) the unscaled traces are the \(L\)-dependent integers above. At \(L=6\) they are \(96\), \(0\) and \(192\), not \(16\), \(0\) and \(32\), and not the scaled triple \(64\), \(0\), \(2048\). Those three integers stay on the labelled ring.

### 6. What stays obstructed

At \(\theta=0\) the Euclidean evolution \(\exp(u\theta K_L)\) is the identity, so \(k_{L,0}\) is the constant \(1/4\). Its circle derivatives vanish. That constant does not display \(s_L''(0)=-1/2\).

O.12, after the Euclidean limit and the window bound \(\widehat k_\theta(m)\ge\theta^2/(36\pi^2 m^2)>0\) for \(m\neq 0\) and \(0<\theta\le 1/192\), still lists as not proved: anything for \(\theta>1/128\); real-time or spectral-density statements; the \(X_{LM}\) comparison; the joint spacetime schedule and the distribution topology. The scope sentence of `docs/meron_euclidean_thermodynamic_limit.md` says the same for real-time spectral density. The window-positivity section extends only the Euclidean nonzero-mode bound. It does not add a real-time statement.

\(\mu_L\) is a finite sum of atoms on the eigenvalue differences of one \(2^L\times 2^L\) matrix. It is not a Lebesgue density on the line. It is not the section 20.12 four-site continuous-time covariance of the Trotter response, and GEN-WDP-57 says neither four spectra nor that fixed carrier's time limit closes the spatial continuum programme. O.9's refusal of real-time CCR dynamics belongs to the spatial Gaussian closure and is a different query.

The open sentence of the goal remains the non-supply. These three rationals do not provide a \(\theta>0\) real-time density or an infinite-volume spectral density. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Claims this note does not make

- It does not claim that O.12, TL-0 through TL-12, or the window bound \(\theta^2/(36\pi^2 m^2)\) supplies a real-time evolution, a real-frequency spectral density, or a thermodynamic-limit real-time law. Those sentences say the opposite.
- It does not treat \(\widehat k_{L,\theta}(m)\), the limit mode \(\widehat k_\theta(m)\), or the bounds \(\theta^2/(16\pi^2 m^2)\) and \(\theta^2/(36\pi^2 m^2)\) as a density \(\rho(\omega)\). `series.fourier` integrates a rational theta-series on the Euclidean circle for integer \(m\). It does not compute \(s_L\).
- It does not replace \(\tau\) by a Gibbs state at \(\theta>0\), and it does not assert the moments \(1/4\), \(0\), \(1/2\) for that state.
- It does not call \(\mu_L\) a Lebesgue density, an infinite-volume spectral measure, a continuum limit, or the section 20.12 covariance.
- It does not copy the labelled integers \(64\), \(0\) and \(2048\) onto a larger ring. The \(L\)-independent statement is the triple of normalized moments only.
- It does not read \([K_L,A_L]\neq 0\) as identification of the Euclidean row-sum spectral weight. ARCH-R2-49 refuses that reading. EP-8 uses the commutator only as a finite-volume criterion for strictly positive Euclidean modes at \(\theta>0\).
- It does not revive the historical full-frequency commutator density. ARCH-R2-46 records that density as odd and negative at negative frequency, hence not a nonnegative measure on the line. Nonnegative mass here comes only from \(\lvert A_{\alpha\beta}\rvert^2\) at \(\theta=0\).
- It does not treat Wick rotation, a real-time Kubo formula, or Lehmann reconstruction of \(\widehat k(m)\) as a theorem of this carrier. It does not claim the \(X_{LM}\) comparison, a statement for \(\theta>1/128\), a Lean proof of the analytic estimates, or probability status for finite signed SQL histories.
- It does not use floating-point spectra at \(L=4,6,8,10\) as evidence. TL-7 marks those row sums as diagnostics.
- It does not assert that no later real-time estimate could exist. It asserts that this finite atomic measure is not that estimate, and that the goal remains the open non-supply the two source sentences record.
- A finite model on this carrier does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.
