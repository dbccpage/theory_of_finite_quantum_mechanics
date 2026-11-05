# WDP-APPW-UNIFORM-VOLUME

Goal id: WDP-APPW-UNIFORM-VOLUME

Selected scope for WDP-APPW-UNIFORM-VOLUME is recorded in this note.

The plan row is open. Its `depends_on` list is empty and it names no fence. Its statement is that a uniform infinite-volume bound named by earlier model responses is unfinished and stays open. The row notes that O.12 later gives written uniform-in-\(L\) bounds for the row-sum covariance on \(0\le\theta\le 1/192\), and that whether that discharges this Appendix W obligation is not stated. This note records one finite identity on the fixed Appendix W carrier, together with the obstruction. It does not supply a uniform-in-\(L\) bound for the Trotter response. No Python, Rust, or Lean kernel was run for this note. The arithmetic below is exact rational comparison of the printed one-period formula.

## Selected scope

One-period staggered eigenvalue on the Appendix W carrier \(L=4\) (Fock dimension 16), not a volume family: \(\lambda_1(r)=-r^4/(4(r+2)(r^2+4r+8))\) at \(r=1/192\) equals \(-1/87426958080\). Theorem T1 controls only this fixed \(L\), with trace dimension 16 and \(\|H\|\le 4\). Not a supremum over \(L\) of the Trotter matrix \(G_M\) (order \(8M\)), and not the O.12 spatial row-sum.

## Hypotheses

H1. Appendix W copies the accepted Trotter argument as the canonical proof. The opening states that the theorem closes a fixed finite spatial carrier's time limit and does not assert a joint infinite-volume/continuum limit or a Gaussian field law. The same two sentences open `docs/meron_field_limit_derivations/trotter_cochain_extinction_derivation.md`.

H2. Section 1 fixes that carrier. There are \(L=4\) sites and the full 16-dimensional CAR Fock space. Indices are periodic. For \(0<\theta\le 1\) and an integer \(M\ge 1\), the step is \(r=\theta/M\) and \(N=2M\). The layers are \(T_0=(I+rP_0)(I+rP_2)\) and \(T_1=(I+rP_1)(I+rP_3)\). The response \(G_M=4 D_z^2\log Z_M(0)\) is symmetric of order \(LN=8M\). The declared quadratic is \(q_M(\psi)=\psi^T G_M\psi/(L N^2)\). The scalar \((1+r)^{-M}\) cancels from \(G\).

H3. Section 2 prints the one-period formula \(\lambda_1(r)=-r^4/(4(r+2)(r^2+4r+8))\) and the value \(\lambda_1(1/192)=-1/87426958080\). The same section says the four inertias at \(\theta=1/10\) and \(M=1,2,3,4\) verify four finite matrices and are not an all-\(M\) inertia theorem.

H4. Theorem T1 is stated for the supplied \(L=4\) carrier. Its proof uses trace dimension 16, \(\|H_i\|\le 2\), \(\|H\|\le 4\), and the factors \(e^{4\theta}\) and \(e^{16\theta}\). It states that no spatial quadrature is taken: the site indices remain the original four. A joint \((L,M)\) limit would need uniform spatial estimates and a spatial reconstruction map, which sampling on this fixed grid does not supply.

H5. Section 3 bounds each response entry by \((E+E^2)/4\), with \(E=e^{4\theta}\), from the same \(L=4\) norm. The text does not replace 4 by a variable length. The resulting rank-one bound is uniform in the time step \(M\) on this one volume.

H6. Section 7 lists uniform infinite-volume estimates as a separate obligation, beside all-\(M\) inertia and joint spatial reconstruction. W.8 says earlier model responses that proposed to close the uniform-volume obligation remain proposals, that the estimate they name and do not finish stays open, and that this appendix does not give that missing estimate a new name.

H7. O.12 and `docs/meron_euclidean_thermodynamic_limit.md` bound a different object: the continuous Euclidean kernel \(C^L_{0y}(u)\) and the spatial row-sum \(k_{L,\theta}(u)=\sum_y C^L_{0y}(u)\), not the discrete Hessian \(G_M\).

## Derivation

### 1. The finite identity

Appendix W §2, and the same formula in the live Trotter derivation §2, print

\[
\lambda_1(r)=\frac{-r^4}{4(r+2)(r^2+4r+8)}
\]

and state \(\lambda_1(1/192)=-1/87426958080\). The same paragraph says the denominator is the polynomial \(64+64r+24r^2+4r^3\).

Expand the rational denominator. \((r+2)(r^2+4r+8)=r^3+6r^2+16r+16\), and multiplication by 4 gives \(4r^3+24r^2+64r+64\). That is the printed polynomial.

Substitute \(r=1/192\). Then \(r+2=385/192\). Next,

\[
r^2+4r+8=\frac{1}{192^2}+\frac{4}{192}+8=\frac{1+768+8\cdot 36864}{36864}=\frac{295681}{36864},
\]

since \(192^2=36864\) and \(1+768+294912=295681\). Therefore

\[
4(r+2)(r^2+4r+8)=\frac{4\cdot 385\cdot 295681}{192^3}=\frac{455348740}{192^3},
\]

because \(4\cdot 385=1540\) and \(1540\cdot 295681=455348740\). Then \(r^4=1/192^4\), so

\[
\frac{r^4}{4(r+2)(r^2+4r+8)}=\frac{1/192^4}{455348740/192^3}=\frac{1}{192\cdot 455348740}.
\]

The product is \(192\cdot 455348740=87426958080\). Hence \(\lambda_1(1/192)=-1/87426958080\).

This is one rational value of the printed one-period formula. The same section's table at \(\theta=1/10\) and \(M=1,2,3,4\) is four finite matrices. It is not an all-\(M\) theorem, and the time-limit argument does not depend on extrapolating that table.

W.8's Gate E value is a different point. The verification record at \(L=4\), \(M=1\), \(r=1/10\) gives eigenvalue \(-1/706440\) and \(v^T G v=-1/88305\), with `is_positive_semidefinite` false. The point \(r=1/10\) lies outside the declared region \(r\le 1/192\). W.8 says one finite point does not establish an unrestricted finite-\(M\) claim or an asymptotic formula. That quadratic value is not a supremum over volumes.

### 2. What the fixed-carrier hypotheses do not give

Theorem T1 states \(|q_M-Q_\theta|\le A_\theta(B,D)/M\) for samples on the supplied \(L=4\) carrier. The envelope is

\[
A_\theta=L\bigl\{30(\theta+\theta^2)e^{16\theta}B^2+2\theta e^{4\theta}B^2+\tfrac12 e^{16\theta}BD\bigr\}.
\]

In the proof, \(H_0=P_0+P_2\) and \(H_1=P_1+P_3\) have norms at most two, and \(\|H\|\le 4\). The trace dimension is 16. The segment error is \(\varepsilon_M=6(\theta+\theta^2)e^{8\theta}/M\). The factor \(L\) in \(A_\theta\) is that site count: the last quadrature step sums the original four indices and divides by \(L\). The text does not replace the norm 4 by a variable length, and it says no spatial quadrature is taken.

Section 3 uses \(E=e^{4\theta}\) on the same carrier. Products of the layers have norm at most \(E\), each response entry has magnitude at most \((E+E^2)/4\), and \(|\lambda_v|\le 2M(E+E^2)\). The rank-one channel then satisfies \(|q_{v,M}|\le (E+E^2)D^2/(16M^2)\). That bound is uniform in \(M\) on this one volume. It is not a bound uniform in a spatial length.

Section 4 states the missing joint object and does not define it. A joint \((L,M)\) limit needs uniform spatial estimates and a spatial reconstruction map. Sampling on this fixed grid does not supply those hypotheses. No formula for a family of Trotter volumes, and no exact spatial error identity for \(G_M\) or \(q_M\), is given in Appendix W.

### 3. The obstruction

Section 7 says the written T1–T3 prove the fixed four-site time limit and its positive-margin case. It then lists general all-\(M\) inertia, uniform infinite-volume estimates, joint spatial reconstruction, cumulant control, Gaussian limits, and native physical repair bindings as separate obligations. It says this scope does not close the continuum.

W.8 repeats the cut. Neither compressed-channel extinction nor T1 is a spatial continuum theorem. Earlier model responses that proposed to close the uniform-volume obligation remain proposals. The estimate they name and do not finish, a uniform infinite-volume bound, stays open. The one-period value, and the Gate E point, are not that estimate. The appendix does not give the missing estimate a new name.

### 4. O.12 does not discharge the obligation

O.12 takes even \(L\ge 4\) and the continuous Euclidean kernel of the periodic Hamiltonian, with row-sum \(k_{L,\theta}(u)=\sum_y C^L_{0y}(u)\). On \(|\theta|\le 1/96\),

\[
|C^L_{0y}(u)|\le M_1(96|\theta|)^{d_L(0,y)},\qquad M_1=\frac{24576}{43},
\]

and the monograph sets \(S_1=3/43\). The thermodynamic-limit note writes the same constant as \(M_1=2S_1\cdot 64^2\). The arithmetic \(2\cdot(3/43)\cdot 64^2=24576/43\) matches those two printed expressions. It is a constant of that continuous kernel, not an entry bound for \(G_M\).

For \(q=96|\theta|e^\mu<1\), O.12 bounds the weighted spatial sum of those absolute values uniformly in even \(L\ge 4\). Display (O-15) states that the placed ring kernel converges to the line kernel in the stated \(\ell^1_\mu\) norm on \(0\le\theta\le 1/192\), with rate uniform on that interval, while the comparison \(\sup_u|k_{L,\theta}-k_\theta|\le 4 M_1 L(128\theta)^L\) is printed for \(0\le\theta<1/128\). O.12's own not-proved list includes anything for \(\theta>1/128\), the \(X_{LM}\) comparison, and the joint spacetime schedule. The thermodynamic-limit note later says TL-2 through TL-7 hold on \(0\le\theta\le 1/192\) except TL-5, which stays on \(0\le\theta<1/128\), and its dated note keeps "any statement for \(\theta>1/128\)" as it applies to the ring lemmas TL-4 and TL-5. This note does not decide that tension.

O.11 says the finite-volume Euclidean argument does not compare the kernel with the time-labelled discrete transfer, and that the joint continuum schedule remains open. O.10 records a different volume-uniform bound, \(|\log X_{L,M}(z)-L\log 2|\le L/19\) for \(|z_{j,x}|\le 1/64\), and says that cumulant bound does not identify the non-equal-time covariance or a joint spacetime limit. W.8 keeps the static Gaussian and the bounded time-labelled cumulant results under their own hypotheses and does not accept them as a joint spacetime field limit. Reusing those constants as the Trotter estimate would be the renaming W.8 refuses.

The row-sum \(k_{L,\theta}=\sum_y C^L_{0y}\) is one spatial sum of the continuous kernel. It is not used here as a sum over the spacetime index set of \(G_M\). The monograph does not say that O.12 closes Appendix W. The plan note says that discharge is not stated.

### 5. Conclusion

On this labelled carrier the checkable result is \(\lambda_1(1/192)=-1/87426958080\). A finite model does not establish a continuum limit, a uniform infinite-volume bound, or a closed theorem outside that identity. The Appendix W uniform infinite-volume bound for the Trotter response stays open.

## Claims this note does not make

- It does not claim a uniform infinite-volume bound for \(G_M\) or \(q_M\), a supremum over \(L\), a joint \((L,M)\) limit, a continuum limit, a Gaussian field law, or a physical law.
- It does not treat \(\lambda_1(1/192)=-1/87426958080\) as anything beyond the printed one-period formula on the fixed carrier. The series \(\lambda_1=-r^4/64+r^5/64-5r^6/512+O(r^7)\) is the source's expansion of that formula; it is not evaluated here as a volume limit.
- It does not treat the four inertias at \(\theta=1/10\) and \(M=1,2,3,4\) as an all-\(M\) inertia theorem.
- It does not treat the Gate E point \(L=4\), \(M=1\), \(r=1/10\), with \(v^T G v=-1/88305\), as a supremum over volumes or as an asymptotic formula. That point lies outside \(r\le 1/192\).
- It does not treat T1's envelope, the factor \(L\) in \(A_\theta\), the trace dimension 16, or \(\|H\|\le 4\) as uniform in a variable spatial length. The text does not replace 4 by a variable length.
- It does not treat the rank-one bound \(|q_{v,M}|\le(E+E^2)D^2/(16M^2)\), Theorem T2, or Corollary T3 as a volume bound. Those statements are uniform in the time step on this one volume, or are positivity statements on the fixed carrier.
- It does not treat O.12, the row-sum \(k_{L,\theta}\), the constant \(M_1=24576/43\), display (O-14), or display (O-15) as a bound on the discrete Hessian \(G_M\). It does not decide the printed tension between the \(\theta>1/128\) exclusion and the \(0\le\theta\le 1/192\) rate.
- It does not treat O.11's temporal bound, O.10's majorant \(|\log X_{L,M}-L\log 2|\le L/19\), or the \(X_{LM}\) comparison as the Appendix W uniform infinite-volume Trotter bound. O.12 lists the \(X_{LM}\) comparison as not proved. O.11 says the Euclidean argument does not compare the kernel with the time-labelled discrete transfer.
- It does not claim that a finite set of volumes for the Trotter response was stated, or that this identity witnesses the missing estimate. No such family is written. The uniform infinite-volume bound stays open.
