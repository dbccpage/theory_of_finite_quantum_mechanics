# Spatial Gaussian source closure on the completed circle

This advances the [analytic response theorem](meron_analytic_response.md)
to spatially varying sources on the [selected circle completion](cs_q_presentation_completion.md).
It proves convergence of the actual Meron source functional and its smeared
quadratic queries under an explicit fluctuation scaling. The result is a
static Gaussian field. Its scaling and topology are declared inputs, and it
does not select an interacting quantum field theory. These are written
infinite-family proofs, separate from bounded exact computation and Lean.

## 1. Retain the original Hamiltonian, source and time histories

Keep even L>=4, full periodic CAR, h_x=I/4-P_x and
a_x=(-1)^x(n_x-1/2). For independent local complex sources z_x, define

\[
 Z_L(\theta,\mathbf z)=\operatorname{Tr}
   \exp[-\theta\sum_xh_x+\sum_xz_xa_x].
\]

The actual time approximation is

\[
 X_{L,M}(\mathbf z)=q^{-LM/4}\operatorname{Tr}
 [T_{\rm odd}(q)D_{\mathbf z}T_{\rm even}(q)D_{\mathbf z}]^M,
 \quad D_{\mathbf z}=\exp[\sum_xz_xa_x/(2M)],\quad q=1+r/M.
\]

Declare a common theta in [r-rho,r+rho], with r>=rho>=0 and
r+rho<=Theta=1/192. Set R=1/64, C_0=1/19. Split each local source into
the same two labels as AR-2/AR-3. Their norm bounds are unchanged when
every |z_x|<=R. Thus the actual independent-source polydisk has an
analytic logarithm and

\[
 |\log Z_L-L\log2|,\ |\log X_{L,M}-L\log2|\le LC_0. \tag{SG-1}
\]

For the Hamiltonian representation this also holds at complex
|theta|<=Theta. Even-CAR trace factorization, the wrapping bond, both
parity sectors and the original ordered time product are retained.

Let F be a fixed real Lipschitz function on T=R/Z, with bounds
||F||_infinity<=N and Lip(F)<=K. The spatial mesh is a=1/L and x maps
to x/L in the declared circle. The smeared half-time query is

\[
 Q_F=\sum_{j=0}^{2M-1}\sum_x F(x/L)a_x({\rm state}_j),\qquad
 V_{L,M}(F)=\frac{\langle Q_F^2\rangle}{(2M)^2L}. \tag{SG-2}
\]

The brackets are the original normalized signed SQL history sum. They
are not reclassified as a probability law. The finite CAR automorphism
c_x ↦ (-1)^x c_x^* sends n_x to 1-n_x. Since adjacent sites have
opposite signs, it preserves every P_x, including the even-L wrapping bond,
and reverses every a_x. It preserves the full trace and each transfer layer.
Thus simultaneous reversal of all local sources leaves both partitions
unchanged, proving zero first moment for every real profile F and the
absence of odd source powers used below. The physical scalar
factor cancels from the normalized source functional but is retained in
its defining partition.

## 2. A spatial locality bound follows from the same polymers

Give each polymer activity the extra positive weight exp(|C|/4). Apply
the abstract Kotecky–Preiss criterion with a(C)=|C| to these majorants.
The [abstract polymer theorem](https://arxiv.org/pdf/math-ph/0605041v2),
section 2, equations (2.10), (2.14) and (2.15), supplies the pinned
expansion bound; [REF-MATH-012](references.md#ref-math-012--abstract-polymer-convergence) records its exact import scope.
All model-specific premises are derived here and in AR-2–AR-5.

Since exp(5/4)<4, replace e t_M in AR-4 by exp(5/4)t_M. The strict bound is

\[
 S_M^*\le\frac4{143M},\qquad
 \sum_{D\not\sim C}|w(D)|e^{5|D|/4}
          \le\frac{28}{143}|C|<|C|. \tag{SG-3}
\]

Indeed M exp(5/4)t_M<=4/255, so the geometric denominator is at least
143/255. To justify exp(5/4)<4, use e<3 and
exp(1/4)<sum_(n>=0)(1/4)^n=4/3.

For a specified source label, the absolute sum of log clusters containing
it is bounded by the sum of pinned expansions over polymers containing
that label. Marking such a polymer counts each qualifying cluster at
least once. SG-3 bounds this sum by S_M^*. There are two source labels
per site for Z, and 2M for X. Therefore the weighted absolute log-cluster
sum anchored at a specified physical source site is at most

\[
 C_A=8/143. \tag{SG-4}
\]

A log cluster containing source sites x and y has connected physical
support. If d_L(x,y) is their shortest circle-graph distance, its bond
labels include a path of at least that length. The sum of its polymer
cardinalities is at least d_L(x,y), including repeated labels. Removing
the extra weight thus gives an anchored absolute sum at most
C_A exp[-d_L(x,y)/4]. This uses actual CAR supports, including the
wrapping bond, rather than a tensor-support approximation.

Differentiate the independent-source logarithm at zero. Cauchy's formula
on the local source disks, with factorial two for a repeated site, yields
for either the exact or time-slice response kernel

\[
 |\kappa_{L,M}(x,y)|\le C_K e^{-d_L(x,y)/4},
 \quad \kappa_{L,M}(x,y)=
    \left.\partial_{z_x}\partial_{z_y}\log X_{L,M}\right|_0,
 \quad C_K=\frac{16}{143R^2}. \tag{SG-5}
\]

Terms lacking either source site have zero mixed derivative. Absolute
weighted convergence justifies differentiating the remaining cluster sum.
For Z_L the same proof defines kappa_L. These are source-response kernels;
finite signed time histories have not been assumed to have positive
covariance matrices.

## 3. Identify the continuum quadratic query

Translation of one CAR mode preserves the Hamiltonian. It exchanges the
two transfer layers and changes the sign of the shifted staggered source.
Cyclicity of Tr(AB)^M=Tr(BA)^M restores the transfer order. Consequently
both second-response kernels are translation invariant, even though the
individual checkerboard factors are not. Their row sums are

\[
 \sum_y\kappa_{L,M}(x,y)=\chi_{L,M},\qquad
 \chi_{L,M}=f_{L,M}''(0),
\]

independent of x. AR-9 bounds |chi_(L,M)-chi(theta)| by E, where
chi(theta)=p''(theta,0)>=0 for the common thermodynamic pressure.
The nonnegativity follows from convexity of the exact Hamiltonian pressure
and its proved derivative limit, not from positivity of every signed history.
Also Cauchy's formula gives |chi(theta)|<=C_chi=2C_0/R^2.

In SG-2 the normalized source Hessian gives
V_(L,M)(F)=a sum_(x,y)F_x F_y kappa_(L,M)(x,y). Replace F_y by F_x.
Since |F_y-F_x|<=K a d_L(x,y), SG-5 gives error at most
40 C_K N K a: exp(-1/4)<=4/5 and
2 sum_(d>=1)d(4/5)^d=40. The row sum then yields
chi_(L,M) a sum_x F_x^2. Finally F^2 is 2NK-Lipschitz, so the uniform
circle Riemann sum differs from its integral by at most NK a. Therefore

\[
 \left|V_{L,M}(F)-\chi(\theta)\int_T F^2\right|
 \le N^2 E+(40C_K+C_\chi)NK/L. \tag{SG-6}
\]

This estimate retains one fixed continuous profile F. Replacing it by
unrelated profiles at each level would not supply a common target. Exact
piecewise-linear circle profiles provide a bounded computational class
whose samples, supremum norm, Lipschitz constant and squared integral are
derived from immutable rational knots rather than supplied as unchecked flags.

## 4. The full normalized source functional has a Gaussian limit

Define the actual logarithmic source functional under fluctuation scaling:

\[
 \ell_{L,M}(u;F)=\log X_{L,M}
        (\{u\sqrt{a}\,F(x/L)\}_x)-\log X_{L,M}(\mathbf0).
\]

The equivalent signed SQL weights are exp[u sqrt(a) Q_F/(2M)]. This is
the same time-averaged query as SG-2, with the spatial factor sqrt(a).
For complex u with t=|u|N/(R sqrt(L))<1, SG-1 bounds its Taylor
coefficients by LC_0 times the inverse powers of R sqrt(L)/N.
Particle-hole symmetry makes all odd coefficients vanish. Thus

\[
 \left|\ell_{L,M}(u;F)-\tfrac12u^2V_{L,M}(F)\right|
 \le \frac{C_0|u|^4N^4}{LR^4(1-t^2)}=:T_{L,M}. \tag{SG-7}
\]

If N=0 the profile and both sides are zero. Combining SG-6 and SG-7 gives

\[
 \left|\ell_{L,M}(u;F)
        -\tfrac12u^2\chi(\theta)\int_TF^2\right|
 \le\tfrac12|u|^2[N^2E+(40C_K+C_\chi)NK/L]+T_{L,M}. \tag{SG-8}
\]

Take the same admitted common temperature and polynomial schedule as AR-9:
L=4k^4, M=L^2, epsilon=R/(4k), with rho=0 or admissible O(k^-4)
enclosures containing that theta. Then E=O(k^-2), the spatial variation
term is O(k^-4) and T is O(k^-4) on bounded u sets. The logarithmic and
exponentiated source functionals converge uniformly there. A finite set
of test profiles follows by taking their linear combinations; polarization
gives limiting mixed response chi(theta) integral F G.

At u=i v the limit is exp[-v^2 chi(theta) integral F^2/2]. This statement
is convergence of source functionals. It is not an invocation of weak
convergence of finite probability measures: those signed source sums have
not been proved positive definite. An equal-time measurement characteristic
function or real-time CCR fluctuation model is a different protected query.

## 5. Construct the resulting field on the completed circle

Use the integer characters supplied by the selected circle/Pontryagin
branch. Their real orthonormal basis is 1, sqrt(2)cos(2pi n x),
sqrt(2)sin(2pi n x), n>=1. With independent standard Gaussian coefficients
xi_j, define Phi(F)=sqrt(chi) sum_j xi_j <F,e_j>. Parseval's identity
makes the series Cauchy in mean square for each F in L^2(T). Its finite
collections have covariance chi integral F G and precisely the limiting
characteristic functional above.

For any s>1/2, the expected negative-Sobolev squared norm is
chi[1+2 sum_(n>=1)(1+n^2)^(-s)]<infinity. Hence it is finite almost surely
and defines a Gaussian random distribution on H^(-s)(T). This explicitly
constructs the static white-noise field target. It does not assert tightness
of a family of finite signed measures or an operator-valued quantum field.

The field is nontrivial at theta=0, where chi=1/4. There is also an explicit
positive-temperature nondegeneracy range. SG-1 for the exact Hamiltonian
extends to the joint complex theta/source polydisk. Its bounded analytic
thermodynamic continuation follows by the coefficient compactness and
identity argument used in AR-6. Cauchy bounds on its Taylor coefficients give

\[
 |\chi(\theta)-1/4|\le\frac{2C_0}{R^2}
                   \frac{\theta}{\Theta-\theta},\quad 0\le\theta<\Theta.
\]

At theta<=2^(-20) this is at most 24576/311239<1/8. Thus
1/8<=chi(theta)<=3/8 there. These conservative constants are sufficient,
not an optimal physical temperature window.

## 6. Scope, ownership and the remaining field-theory problem

The mesh x/L, fluctuation factor L^(-1/2), fixed temperature and selected
circle geometry are explicit parts of this profile. A physical coupling
renormalization, critical continuum limit, propagation law, nontrivial
spacetime correlations, or interacting field action has not been derived.
The original q=3,M=2 fixture remains outside the analytic domain.

The functional math owner constructs and evaluates exact periodic
piecewise-linear test profiles. Quantum physics owns spatial-source bounds
and actual weighted moments, reusing its CAR layers and the generic matrix
jet owner. WDP retains the profile, plan, moments and bounded readings.
Python independently checks the weighted moments against original SQL
histories. Work caps remain finite; code does not execute the infinite
schedule or sample the distribution-valued target.

This closes a stated spatial source-functional profile, including its
quadratic query, locality estimate, common target and limit schedule.
The broader field theory and five enlarged Genesis obligations remain open.
