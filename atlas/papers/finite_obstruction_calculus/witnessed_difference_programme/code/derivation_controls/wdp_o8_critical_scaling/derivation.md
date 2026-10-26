# WDP-O8-CRITICAL-SCALING

Goal id: WDP-O8-CRITICAL-SCALING

Selected scope for WDP-O8-CRITICAL-SCALING is recorded in this note.

The plan row is open. Its `depends_on` list is empty and it names no fence. Its statement is that interacting spacetime, critical mesh, coupling scaling, and spatial field scaling of the Meron responses remain open. This note does not close that statement. It records the coefficient of \(\theta^1\) at \(\theta=0\) in the Euclidean kernel on one even ring, and the mesh exponent of that single coefficient. No Python, Rust, or Lean kernel was run for this note. The arithmetic is the normalized trace already fixed by EP-1 and by the integer bond matrices in `car.py`.

## Selected scope

Labelled carrier: the even periodic full-Fock ring \(L=4\), dimension \(16\), bonds \((x,x+1 \bmod 4)\), \(K_4=\sum_x(I/4-P_x)\), \(a_x=(-1)^x(n_x-1/2)\), and

\[
C_{0y}(u)=\operatorname{Tr}\bigl(e^{-(1-u)\theta K}a_0 e^{-u\theta K}a_y\bigr)\big/\operatorname{Tr}(e^{-\theta K}).
\]

Finite result: the coefficient of \(\theta^1\) at \(\theta=0\) is the \(u\)-constant tuple \((y=0,1,2,3)\mapsto(0,1/16,0,1/16)\). The same one-bond trace equals \(1/16\) on every even ring \(L\ge 4\), so the ratio of the \(L=6\) value to the \(L=4\) value is \(1\), and any one-power mesh ansatz for this coefficient has exponent \(0\).

Not selected: critical finite-size scaling, a temperature that grows with \(L\), coupling renormalization, the discrete kernel \(X_{L,M}\), or a joint spacetime field limit.

## Hypotheses

H1. EP-1 and TL-0, for even \(L\ge 4\): \(y=x+1\) modulo \(L\),

\[
P_x=\tfrac12\bigl(n_x+n_y-2n_xn_y+c_x^*c_y+c_y^*c_x\bigr),\qquad
K=\sum_x\bigl(I/4-P_x\bigr),\qquad
a_x=(-1)^x(n_x-\tfrac12).
\]

EP-2 writes \(a_x(u)=e^{u\theta K}a_x e^{-u\theta K}\) and \(C_{xy}(u)=\operatorname{Tr}(\rho\,a_x(u)a_y)\) after the centering term drops. The displayed split exponential is that trace. The particle-hole map \(c_x\mapsto(-1)^x c_x^*\) preserves each \(P_x\) for even \(L\) and reverses each \(a_x\), so \(\operatorname{Tr}(\rho a_x)=0\). Occupation gives \(n_x^2=n_x\), hence \(a_x^2=I/4\). O.12 records the consequence \(C^L_{00}(0)=1/4\). The code stores \(K_4=4K\) and \(2a_x\), with \(4P=2(n_x+n_y-2n_xn_y+c_x^*c_y+c_y^*c_x)\).

H2. At \(\theta=0\) the normalized trace is \(2^{-L}\operatorname{Tr}\), the uniform product state. AR §2 factorizes the normalized trace of even CAR operators on disjoint supports. The wrapping bond is included: its CAR support is the two endpoint modes, and a long occupation-basis parity string is a basis artifact of that reordering. TL-1 states the same factorization across the wrapping bond. Each \(P_x\) is a projector, since \((4P)^2=4(4P)\).

H3. The section headed TL-2 says that \(C^L_{0y}\) vanishes at \(\theta=0\) to order the ring distance \(d_L(0,y)\). The bound tagged TL-3 is \(|C^L_{0y}(u)|\le M_1(96|\theta|)^{d_L(0,y)}\) on \(|\theta|\le 1/96\). On the smaller interval \(0\le\theta\le 1/192\) one has \(96\theta\le 1/2\), and that base does not depend on \(L\). The sentence that the exact order is attained is stated for \(L=6\) and the chain \([-4,4]\), not as a new \(L=4\) computation.

H4. O.8 keeps interacting spacetime, critical mesh, and coupling scaling open, and assigns O.9 only a static spatial source functional. SG §6 states that the mesh \(x/L\), the factor \(L^{-1/2}\), fixed temperature, and the selected circle remain premises of that profile, and that coupling renormalization, a critical continuum limit, and an interacting field action are not derived. Analytic §7 says critical regimes, spatial mesh, and coupling rescaling still need their own estimates. Presentation §10 says that in critical finite-size scaling \(\theta\) may grow with \(L\). O.12 leaves the \(X_{LM}\) comparison and the joint spacetime schedule unproved. This jet is the Hamiltonian kernel at order \(\theta^1\), not that schedule.

## Derivation

### 1. The order-\(\theta\) trace

Expand \(e^{-s\theta K}=I-s\theta K+O(\theta^2)\). Then

\[
\begin{aligned}
N(u)&=\operatorname{Tr}\bigl(e^{-(1-u)\theta K}a_0 e^{-u\theta K}a_y\bigr)\\
&=\operatorname{Tr}(a_0 a_y)-\theta\bigl((1-u)\operatorname{Tr}(K a_0 a_y)+u\operatorname{Tr}(a_0 K a_y)\bigr)+O(\theta^2).
\end{aligned}
\]

H1 gives \(\operatorname{Tr}(K)=0\) once each bond has normalized trace \(1/4\), proved in the next section, so \(Z=\operatorname{Tr}(e^{-\theta K})=2^L+O(\theta^2)\). No order-\(\theta\) term in \(Z\) enters the quotient. Off site, \(\operatorname{Tr}(a_0 a_y)=0\), and the scalar summands \(I/4\) inside \(K\) drop with it. The coefficient of \(\theta\) is

\[
C_{0y}^{(1)}(u)=-(1-u)\langle K a_0 a_y\rangle-u\langle a_0 K a_y\rangle,
\]

with \(\langle\,\cdot\,\rangle=2^{-L}\operatorname{Tr}\).

### 2. Each bond has normalized trace \(1/4\)

On one bond the occupation basis \(|n_0 n_1\rangle=00,01,10,11\) represents the adjacent operators by

\[
4P=\begin{pmatrix}0&0&0&0\\0&2&2&0\\0&2&2&0\\0&0&0&0\end{pmatrix}.
\]

The diagonal block is \(2(n_0+n_1-2n_0 n_1)\). The off-diagonal block is \(2(c_0^*c_1+c_1^*c_0)\): the Jordan–Wigner sign on the ordered pair \((0,1)\) produces \(+|10\rangle\) from \(|01\rangle\) and \(+|01\rangle\) from \(|10\rangle\), and both doubly occupied and empty states are annihilated. The trace of this matrix is \(4\), so the two-site trace of \(P\) is \(1\) and the two-site normalized trace is \(1/4\). Eigenvalues of the middle block are \(0\) and \(4\), so \(P\) is a projector, in agreement with \((4P)^2=4(4P)\).

AR §2 moves any bond's two modes into one successive block by an occupation-basis permutation that preserves the trace. Unused modes contribute the factor \(1\) to the normalized trace. The wrapping bond is the same two-mode operator after that reordering. Therefore every bond, on every even \(L\ge 4\), has \(\langle P_x\rangle=1/4\) and \(\langle I/4-P_x\rangle=0\). Hence \(\operatorname{Tr}(K)=0\).

### 3. On site

\(\langle K a_0^2\rangle=\langle K\rangle/4=0\). Cyclicity gives \(\operatorname{Tr}(a_0 K a_0)=\operatorname{Tr}(K a_0^2)=0\). Thus \(C_{00}^{(1)}(u)=0\). The constant term remains \(C_{00}(0)=1/4\), which is not the coefficient of \(\theta\).

### 4. The bond \((0,1)\)

The same basis has \(2a_0=\operatorname{diag}(-1,-1,1,1)\) and \(2a_1=\operatorname{diag}(1,-1,1,-1)\), hence

\[
(2a_0)(2a_1)=\operatorname{diag}(-1,1,1,-1).
\]

Right-multiplication by that diagonal leaves \(4P\) unchanged, because the two nonzero columns already sit on the entries \(+1\). The trace is \(4\). Division by the bond dimension \(4\) gives the normalized expectation \(1\). Since \((2a_0)(2a_1)=4 a_0 a_1\),

\[
4P\,(2a_0)(2a_1)=16\,P a_0 a_1,
\]

and \(\langle P a_0 a_1\rangle=1/16\). Both insertions are diagonal, so they commute and \(\operatorname{Tr}(a_0 P a_1)=\operatorname{Tr}(P a_0 a_1)\). The scalar \(I/4\) drops because \(\operatorname{Tr}(a_0 a_1)=0\). Therefore the bond \((0,1)\) contributes

\[
\langle(I/4-P)a_0 a_1\rangle=\langle a_0(I/4-P)a_1\rangle=-1/16.
\]

Every other bond misses at least one of the sites \(0\) and \(1\). H2 factorizes that bond off the missed source, and the missed source has mean \(0\), so the bond drops. Hence \(\langle K a_0 a_1\rangle=\langle a_0 K a_1\rangle=-1/16\) and

\[
C_{01}^{(1)}(u)=(1-u)/16+u/16=1/16.
\]

The value does not depend on \(u\) or on \(L\). The spectator modes contribute the same factor to the numerator and to \(2^L\).

### 5. The other three sites on \(L=4\)

The bond \((3,0)\) is the other neighbour of site \(0\). Sites \(0\) and \(3\) carry opposite staggers, because \(L\) is even and \(3\) is odd. After the reordering in H2, its two-mode matrices are the matrices of section 4. The same trace gives \(\langle P a_0 a_3\rangle=1/16\), and every other bond misses at least one endpoint, so \(C_{0,3}^{(1)}(u)=1/16\).

Site \(2\) is at ring distance \(2\). No single bond meets both \(0\) and \(2\). The order-\(\theta\) formula contains only one factor of \(K\), so \(C_{02}^{(1)}(u)=0\). That is the distance vanishing named in H3, specialized to order \(1\); it does not use the Schwarz majorant.

The four coefficients are \(0\), \(1/16\), \(0\), \(1/16\). Their sum is the constant \(1/8\). In `checks.py` the recorded series is `ZERO_MODE` \(=[1/4,1/8,1/48,-1/96]\), and `test_wrap_sign_zero_modes_recorded` identifies that list with the physical zero-mode series on \(L=6\). The entry `ZERO_MODE[1]`\(=1/8\) therefore matches this spatial sum. The match checks the sum of four site values. It does not promote \(1/8\) to a spatial field, and it does not evaluate the later entries \(1/48\) and \(-1/96\).

### 6. Mesh exponent of this coefficient

Sections 4 and 5 use one bond and the mean-zero factorization. Both are uniform in even \(L\ge 4\). Thus

\[
\partial_\theta C_{01}\big|_{\theta=0}=1/16
\]

on \(L=4\) and on \(L=6\). Suppose one constant \(c\) and one exponent \(\alpha\) satisfied \(\partial_\theta C_{01}|_0=c L^\alpha\) at both lengths. The two values are equal and nonzero, so \((6/4)^\alpha=(3/2)^\alpha=1\), hence \(\alpha=0\). The \(\theta\)-linear nearest-neighbour coupling has mesh exponent \(0\).

### 7. What this identity does not close

Exponent \(0\) at \(\theta=0\) is not critical finite-size scaling. Presentation §10 requires a declared regime in which \(\theta\) may grow with \(L\). The proved window \(0\le\theta\le 1/192\) has decay base \(96\cdot(1/192)=1/2\), independent of \(L\) (the comparison recorded under TL-7). O.9's amplitude \(L^{-1/2}\) is the declared fluctuation premise \(\sqrt a\) at mesh \(a=1/L\), and SG §6 says that premise is not a derived coupling renormalization or an interacting field action. O.12 still lists the \(X_{LM}\) comparison and the joint spacetime schedule as not proved, so these rationals are not a discrete-history spacetime kernel.

A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the tuple \((0,1/16,0,1/16)\) and the exponent \(0\) of that one coefficient. The goal statement remains the open obligation named by O.8 and O.5.

## Claims this note does not make

- It does not claim interacting spacetime, a critical mesh, physical coupling renormalization, or spatial field scaling of the Meron responses. Those are the open statement of the goal. O.5's fixed-volume Kubo jet does not establish a growing-volume correlation or a spatial scaling limit.
- It does not treat \(a=1/L\) or the amplitude \(L^{-1/2}\) as derived critical or interacting scaling. O.9 and SG §6 keep them as premises of one static profile.
- It does not read the disk \(0\le\theta\le 1/192\), \(|z|\le 1/64\), the schedule \(L=4k^4\), \(M=L^2\), or the fixed-\(L\) transport bound as this exponent. The base \(1/2\) does not grow with \(L\).
- It does not claim an all-temperature susceptibility theorem. That is the neighbouring obligation.
- It does not compare this kernel with \(X_{L,M}\), and it does not supply a joint \((L,M)\) spacetime schedule or a field topology.
- It does not reuse the O.5 fixture rationals \(36864\), \(912\), \(48/19\), or \(149/57\). Those are fixed-volume one-dimensional values. It does not reuse `ZERO_MODE[1]`\(=1/8\), nor \(1/48\), nor \(-1/96\), as a site value or as a field.
- It does not claim a sign-problem algorithm, new Lean coverage, an operator-valued field, real-time CCR dynamics, or positivity of the finite signed histories.
