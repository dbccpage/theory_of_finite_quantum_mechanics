# Time-labelled Meron sources and higher connected responses

Status: selected finite-family theorem; spacetime covariance limit OPEN.
AuthorityEffect: None.

This extends [AR-3--AR-6](meron_analytic_response.md) from one repeated
source to independent half-step and site labels. It uses the actual even
periodic full-Fock `U=t` CAR chain. It is a written infinite-family proof,
not a new finite execution or Lean theorem. The labels below are an exact
source insertion on the native transfer product; the original SQLite rows
do not store these independent labels.

## TD-1. Exact time-labelled partition and its finite history expansion

Take even `L>=4`, integer `M>=1`, `0<=r<=1/192`, `q=1+r/M`, and `h=log q`.
Retain `h_x=I/4-P_x`, `a_x=(-1)^x(n_x-1/2)`, the two periodic checkerboard
layers `T_j` (`j` modulo two), and the full `2^L` occupation basis. For
independent complex labels `z_(j,x)` set

\[
 D_j(\mathbf z)=\exp\left[\frac1{2M}\sum_x z_{j,x}a_x\right],\qquad
 X_{L,M}(\mathbf z)=q^{-LM/4}
 \operatorname{Tr}\prod_{j=2M-1}^{0}\left[T_j(q)D_j(\mathbf z)\right]. \tag{TD-1}
\]

The rightmost factor acts first. Inserting the occupation resolution of
identity between factors gives, with `s_(2M)=s_0`,

\[
 X_{L,M}(\mathbf z)=q^{-LM/4}
 \sum_{s_0,\ldots,s_{2M-1}}
 \prod_{j=0}^{2M-1}\langle s_{j+1}|T_j(q)|s_j\rangle
 \exp\left[\frac1{2M}\sum_{j,x}z_{j,x}a_x(s_j)\right]. \tag{TD-2}
\]

The matrix elements retain the original periodic CAR hop sign; no
sign-stripped transfer is substituted. This identity is a basis expansion
of the specified transfer, including source insertion **before** each
layer. At zero source it is the earlier trace. Inside the original SQL
carrier ceiling the zero-source trace agrees with the original signed
partition; equation TD-2 does not assert that SQLite stores the added
time-labelled source columns. The scalar `q^(-LM/4)` remains on both sides.

At the exactly decoupled control `r=0`, all layers are identities and the
site factors commute. The formula reduces without a continuum argument to

\[
 X_{L,M}(\mathbf z)=\prod_{x=0}^{L-1}
 2\cosh\!\left({1\over4M}\sum_{j=0}^{2M-1}z_{j,x}\right). \tag{TD-2a}
\]

The staggered sign drops out because cosh is even. A constant source `z`
therefore gives `[2 cosh(z/2)]^L`, checking the half-step normalization.
At this control every nonzero temporal Fourier mode of the quadratic
response is zero; a positive-temperature temporal mode requires a separate
argument.

## TD-3. Uniform polydisk and logarithm bound

For **every** `|z_(j,x)|<=R=1/64`, the branch of `log X` fixed by the
zero-coupling, zero-source normalized trace exists and satisfies

\[
 \left|\log X_{L,M}(\mathbf z)-L\log2\right|
 \le C_0 L,\qquad C_0=1/19, \tag{TD-3}
\]

uniformly in even `L>=4`, integer `M>=1`, and all independently chosen
labels. In particular `X` has no zero in this polydisk.

Here are the premises of the abstract polymer step. Split each `D_j`
exactly into its commuting site factors, and distribute the physical
scalar `q^(-LM/4)` over the `LM` bond factors. The ordered normalized
trace is a product of `LM` factors `exp(-h h_x)` and `2ML` factors
`exp(z_(j,x)a_x/(2M))`, hence `3ML` labels. Every exponent is even and has
norm at most `1/(256M)`: for a bond use `h<=r/M` and `||h_x||=3/4`; for a
source use `||a_x||=1/2` and `R/(4M)=1/(256M)`. The wrapping bond has its
two *physical CAR sites* as support, despite its occupation-matrix parity
string. Disjoint even-CAR supports commute and their normalized full-Fock
trace factorizes.

Expand each factor as `I+V_i`. Connected selected label sets are hard-core
polymers, incompatible when physical supports overlap; disconnected
components commute and trace-factorize, preserving the order inside each
component. Thus their activities obey

\[
 |w(C)|\le t_M^{|C|},\qquad
 t_M=e^{1/(256M)}-1\le(256M-1)^{-1}. \tag{TD-4}
\]

Different values of `z_(j,x)` alter the activities, but not the support
graph or TD-4. A bond-copy label overlaps at most `3M-1` bond labels and
`4M` source labels; a source-copy label overlaps at most `2M` bond and
`2M-1` source labels. Hence the degree is at most `7M-1`. The connected
`k`-set count rooted at one label is at most `(4(7M-1))^(k-1)`. With
`a(C)=|C|`, the root sum and incompatibility sum are, exactly as in AR-4/5,

\[
 S_M:=\sum_{C\ni i}|w(C)|e^{|C|}
 \le\frac{e t_M}{1-28M e t_M}\le\frac1{57M},\qquad
 \sum_{D\not\sim C}|w(D)|e^{|D|}
 \le 7M|C|S_M\le\frac7{57}|C|<|C|. \tag{TD-5}
\]

The imported [Fernandez--Procacci polymer criterion](https://arxiv.org/pdf/math-ph/0605041v2),
equations (2.10), (2.14), and (2.15), now gives an absolutely convergent
log-cluster expansion and the zero-free branch. Integrating its pinned
majorant from zero activities bounds the absolute logarithm by the sum of
rooted polymer majorants. There are `3ML` labels, so TD-5 yields
`3ML/(57M)=L/19`, proving TD-3. This is the same AR margin applied to
independent time labels; it is not an assumption that static analyticity
implies time-dependent analyticity.

The even-`L` particle-hole CAR automorphism `c_x -> (-1)^x c_x^*`
preserves each `P_x` (including the periodic bond), hence each layer, and
reverses every `a_x`. Trace invariance gives
`X_(L,M)(z)=X_(L,M)(-z)` under simultaneous reversal of all labels.
All odd total connected responses at zero source therefore vanish.

## TD-6. Smeared mixed-cumulant bound

For a bounded real or complex spacetime array `Psi_(j,x)`, write
`N=||Psi||_infinity` and define the signed-history observable

\[
 \Phi_{L,M}(\Psi)=\frac1{2M\sqrt L}
 \sum_{j=0}^{2M-1}\sum_{x=0}^{L-1}\Psi_{j,x}a_x(s_j).
 \tag{TD-6}
\]

Its *connected response cumulants* are derivatives at zero of
`ell_(L,M)(u;Psi)=log[X_(L,M)(u Psi/sqrt L)/X_(L,M)(0)]`. The ratio is the
normalized signed history sum, not an asserted probability expectation.
For `N>0`, TD-3 bounds `|ell|<=2C_0 L` on the disk
`|u|<=R sqrt(L)/N`. Cauchy's formula gives, for every integer `n>=1`,

\[
 |\kappa_n(\Phi_{L,M}(\Psi))|
 \le 2C_0 n!\left(\frac NR\right)^n L^{1-n/2}.
 \tag{TD-7}
\]

The bound is uniform in `M`. Odd orders are exactly zero by the
particle-hole symmetry. For distinct bounded profiles `Psi_1,...,Psi_n`
with norms `N_i>0`, apply multivariable Cauchy on radii
`R sqrt(L)/(n N_i)` to obtain

\[
 |\kappa(\Phi(\Psi_1),\ldots,\Phi(\Psi_n))|
 \le 2C_0\frac{n^n}{R^n}L^{1-n/2}\prod_i N_i.
 \tag{TD-8}
\]

If any `N_i=0`, that mixed cumulant is zero. Thus the mixed second
responses are uniformly bounded, and every connected order `n>=3`
vanishes as `L` grows, independently of how `M` grows. In particular,
for `t=|u|N/(R sqrt L)<1`, the even Taylor series gives the explicit
quadratic remainder

\[
 \left|\ell_{L,M}(u;\Psi)
       -\frac{u^2}{2}\kappa_2(\Phi_{L,M}(\Psi))\right|
 \le \frac{2C_0 L t^4}{1-t^2}. \tag{TD-9}
\]

For fixed `u,N` this is `O(L^-1)` uniformly in `M`. If the quadratic
forms converge along a specified joint `(L,M)` schedule, TD-9 forces the
corresponding finite collections of source functionals to a quadratic
limit. A positive-semidefinite limiting form would then define Gaussian
finite-dimensional laws. Neither covariance convergence nor positivity of
that form follows from TD-3--TD-9.

## Boundary of the result

This closes the uniform time-labelled analytic-disk and smeared
higher-cumulant *subproblem* in the declared high-temperature region.
It does not bound individual non-equal-time site-pair correlations at their
natural `(2M)^2` rescaling, identify a spacetime covariance kernel or
topology, or give a joint error schedule for time-dependent test functions.
The [exact Hamiltonian Euclidean covariance](meron_euclidean_covariance_positivity.md)
is positive and has nonzero temporal modes at every finite even size and
positive temperature. The [thermodynamic-limit supplement](meron_euclidean_thermodynamic_limit.md)
establishes its high-temperature volume limit and positive nonzero time modes
on its stated region. Comparison with these discrete signed histories remains open. The `q=3` fixtures lie outside this
analytic disk.
