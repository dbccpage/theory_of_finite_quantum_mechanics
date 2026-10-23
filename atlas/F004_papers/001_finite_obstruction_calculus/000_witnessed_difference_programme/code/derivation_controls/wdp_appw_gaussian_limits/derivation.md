# WDP-APPW-GAUSSIAN-LIMITS

Goal id: WDP-APPW-GAUSSIAN-LIMITS

Selected scope for WDP-APPW-GAUSSIAN-LIMITS is recorded in this note.

The plan row is open. Its `depends_on` list is empty and it names no fence. Its statement is that Gaussian limits remain a separate obligation: the static Gaussian result and the bounded time-labelled cumulant result hold only under the hypotheses already stated for them, and they are not a joint spacetime field limit. This note checks that separation on one finite carrier. It does not construct a joint \((L,M)\) spacetime Gaussian field. No Python, Rust, or Lean kernel was run for this note.

## Selected scope

Labelled carrier \(L=4\), \(M=1\), \(r=0\) (inside \(0\le r\le 1/192\)), full 16-dimensional periodic CAR Fock space, half-steps \(j=0,1\) and sites \(x=0,1,2,3\). Hypotheses used are only TD-2a (layers are identities) and the TD-6 scaling of \(\Phi\). Exact rationals: constant profile \(\kappa_2=1/4\) and \(\kappa_4=-1/32\); alternating profile \(\Phi=0\), so every cumulant is \(0\). The static Gaussian input class (time-independent Lipschitz \(F\), amplitude \(L^{-1/2}\), schedule \(L=4k^4\), \(M=L^2\), law on \(H^{-s}(\mathbb T)\)) does not contain the alternating 8-label profile.

## Hypotheses

H1. TD-1/TD-2 keep even \(L\ge 4\), integer \(M\ge 1\), \(0\le r\le 1/192\), \(q=1+r/M\), the full \(2^L\) occupation basis, and the periodic checkerboard layers. At the decoupled control \(r=0\) every layer is the identity, the site factors commute, and TD-2a states, with no continuum argument,

\[
X_{L,M}(\mathbf z)=\prod_{x=0}^{L-1}2\cosh\Bigl(\frac1{4M}\sum_{j=0}^{2M-1}z_{j,x}\Bigr).
\]

The staggered sign drops because \(\cosh\) is even. The zero-source value is \(X_{L,M}(\mathbf 0)=2^L\).

H2. TD-6 scales a bounded array by the same square root of volume. The centred logarithm and the signed-history observable are

\[
\ell_{L,M}(u;\Psi)=\log\frac{X_{L,M}(u\Psi/\sqrt L)}{X_{L,M}(\mathbf 0)},
\qquad
\Phi_{L,M}(\Psi)=\frac1{2M\sqrt L}\sum_{j,x}\Psi_{j,x}a_x(s_j).
\]

The connected responses \(\kappa_n\) are the derivatives of \(\ell\) at \(u=0\). The ratio is a normalized signed history sum, not an asserted probability expectation. On this carrier \(\sqrt L=2\) and \(2M\sqrt L=4\).

H3. The static closure in SG and O.9 is a different input. One fixed real Lipschitz profile \(F\) on the circle is repeated in time, the mesh is \(a=1/L\), and the amplitude is \(\sqrt a\). The schedule taken from AR-9 is \(L=4k^4\), \(M=L^2\). Integer characters construct a Gaussian random distribution on \(H^{-s}(\mathbb T)\) for \(s>1/2\), with variance factor \(\chi(\theta)\). At \(\theta=0\), \(\chi=1/4\). SG §6 states that nontrivial spacetime correlations have not been derived. The point \((L,M)=(4,1)\) is not on that schedule: \(k=1\) would require \(M=L^2=16\).

H4. TD-7, printed as O-11, is only the Cauchy majorant on the disk \(|z_{j,x}|\le R=1/64\):

\[
|\kappa_n(\Phi_{L,M}(\Psi))|\le\frac2{19}\,n!\Bigl(\frac{\|\Psi\|_\infty}{R}\Bigr)^n L^{1-n/2},
\]

uniformly in \(M\). The paragraph after TD-9 states that neither covariance convergence nor positivity follows from TD-3 through TD-9. This note uses that printed bound at one integer point. It does not re-prove the polymer criterion.

H5. Appendix W copies the accepted Trotter argument and says that theorem closes a fixed finite spatial carrier's time limit and does not assert a joint infinite-volume/continuum limit or a Gaussian field law. W.8 says the static Gaussian and bounded time-labelled cumulant results remain under their stated hypotheses and are not a joint spacetime field limit, and that a finite signed generating function is not a probability characteristic function. Theorem T1 on this same \(L=4\) carrier is the bound \(|q_M-Q_\theta|\le A_\theta(B,D)/M\).

## Derivation

### 1. Constant profile: the finite law is not Gaussian

Specialize TD-2a to \(L=4\), \(M=1\), and insert the TD-6 labels \(z_{j,x}=u\Psi_{j,x}/\sqrt 4=u\Psi_{j,x}/2\). The argument of each \(\cosh\) is

\[
\frac1{4}\sum_{j=0}^{1}z_{j,x}=u\sigma_x,\qquad\sigma_x=\frac{\Psi_{0,x}+\Psi_{1,x}}{8}.
\]

Dividing by \(X(\mathbf 0)=16\) cancels the four factors of \(2\), so

\[
\ell(u;\Psi)=\sum_{x=0}^{3}\log\cosh(u\sigma_x).
\]

The function \(\log\cosh\) is even, so every odd derivative at \(0\) vanishes. Its second derivative at \(0\) is \(1\), and its fourth derivative at \(0\) is \(-2\): the expansion \(\log\cosh t=t^2/2-t^4/12+O(t^6)\) has fourth derivative \(-2\) at the origin. Therefore

\[
\kappa_2=\sum_{x=0}^{3}\sigma_x^2=\sum_{x=0}^{3}\frac{(\Psi_{0,x}+\Psi_{1,x})^2}{64},\qquad
\kappa_4=\sum_{x=0}^{3}(-2)\sigma_x^4.
\]

For the constant array \(\Psi_{j,x}=1\), each \(\sigma_x=1/4\). Then \(\sigma_x^2=1/16\) and \(\sigma_x^4=1/256\), hence

\[
\kappa_2=4\cdot\frac1{16}=\frac14,\qquad
\kappa_4=4\cdot(-2)\cdot\frac1{256}=-\frac1{32}.
\]

A Gaussian log characteristic function is quadratic, so its fourth derivative at the origin is \(0\). Here \(\kappa_4=-1/32\neq 0\). The finite constant-profile law on this carrier is not Gaussian. The equality \(\kappa_2=\chi(0)=1/4\) is equality of one rational with the static variance factor. It is not the \(H^{-s}(\mathbb T)\) field, and this \((L,M)\) is not the AR-9 point \(M=L^2\).

### 2. Alternating profile: every cumulant is zero

Take \(\Psi_{0,x}=1\) and \(\Psi_{1,x}=-1\), eight labels in all. Each time sum vanishes, so \(\sigma_x=0\), \(\ell=0\), and every derivative at \(u=0\) is \(0\).

The same conclusion is the occupation expansion. At \(r=0\), \(M=1\), TD-2 has identity layers and the trace is periodic, so a history has nonzero weight only when \(s_0=s_1\). TD-6 then gives the function

\[
\Phi=\frac14\sum_{x=0}^{3}\bigl(a_x(s_0)-a_x(s_1)\bigr)=0
\]

on every history with nonzero weight. Every cumulant of the zero function is \(0\).

The static theorem's \(\chi(0)=1/4\) equals the constant-profile \(\kappa_2\) of §1 and does not equal this alternating quadratic form. Reading \(\chi(0)\) as that 8-label value would reuse the static rational as a spacetime number. The exact form is \(0\), not \(1/4\). The static input class does not contain this profile: SG and O.9 take one time-independent Lipschitz circle profile, not a half-step sign flip.

### 3. The cumulant majorant does not identify either kernel

Apply the printed TD-7 bound at \(n=2\), \(\|\Psi\|_\infty=1\), \(R=1/64\), and \(L=4\):

\[
|\kappa_2|\le\frac2{19}\cdot 2!\cdot 64^2\cdot L^{0}=\frac{4}{19}\cdot 4096=\frac{16384}{19}.
\]

Both exact values sit strictly inside that interval: \(0<16384/19\) and \(1/4<16384/19\). The majorant is uniform in \(M\) and does not select a non-equal-time kernel, a cylinder topology, or a joint \((L,M)\) rate. TD-9 says that a positive-semidefinite limiting form would define Gaussian finite-dimensional laws only if the quadratic forms converge along a specified joint schedule, and that neither that convergence nor that positivity follows from TD-3 through TD-9.

### 4. What stays outside this carrier

Appendix W's opening and W.8 keep the static circle Gaussian and the time-labelled cumulant bound under their own hypotheses and refuse them as a joint spacetime field limit. Theorem T1 is a fixed-spatial time-continuum bound on the same four-site Fock space; it does not assert a Gaussian field law. The note `meron_spacetime_field_theorems.md` withdraws the earlier claim of a completed Gaussian spacetime field and of a joint discrete-to-continuum limit.

Gate E evaluates one response matrix at \(L=4\), \(M=1\), \(r=1/10\). The recorded quadratic value is \(v^{\mathsf T}Gv=-1/88305\), so that matrix is not positive semidefinite. Since \(1/10>1/192\), the point lies outside \(0\le r\le 1/192\). It is not an in-disk counterexample to TD-3 or TD-7. It only shows that dropping the temperature hypothesis can destroy positive semidefiniteness of one finite matrix. It is not a Gaussian field law.

No joint \((L,M)\) spacetime Gaussian field limit is claimed.

## Claims not made

- A joint spacetime Gaussian field, an \(H^{-s}\) law on a spacetime cylinder, or convergence of a non-equal-time covariance.
- Positivity of the finite signed histories as a probability law, or the reading of a finite signed generating function as a probability characteristic function.
- Finite-measure tightness, real-time CCR dynamics, coupling renormalization, an interacting quantum field, or an operator-valued limit.
- Identification of \(\chi(0)=1/4\), the constant-profile \(\kappa_2\), the O.12 row-sum kernel, Theorem T1, or the rank-one channel with a spacetime Gaussian target.
- An in-disk reading of the Gate E value \(-1/88305\). That point is \(r=1/10\), outside \(0\le r\le 1/192\).
- Execution of the schedule \(L=4k^4\), \(M=L^2\), or a sample of the static white-noise distribution. The comparisons \(e<3\) and the imported polymer criterion are not re-proved here.
- Any continuum limit, physical law, or closed theorem outside the selected carrier. A finite model on \(L=4\), \(M=1\), \(r=0\) does not establish one.
