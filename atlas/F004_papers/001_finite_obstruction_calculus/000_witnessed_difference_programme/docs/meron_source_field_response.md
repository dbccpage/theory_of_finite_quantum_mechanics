# Actual source-field pressure and response at finite resolution

This advances the [actual U=t chain](meron_time_and_volume_refinement.md)
and [staggered Kubo query](meron_spin_and_observable_transport.md). The
infinite-family arguments below are written proofs. Bounded exact traces
and tests have separate scopes; no new Lean coverage is claimed.

## 1. Preserve the actual ensemble and source

For even L>=4 retain the full periodic CAR carrier, both parity sectors,
G=sum_x P_x, H_L/t=L I/4-G, and
A_L=sum_x (-1)^x(n_x-1/2). Each P_x is the previously verified projection;
each physical bond has norm 3/4. We have ||A_L||=L/2 and integer occupation
eigenvalues. Declare theta>=0 and lambda in R, and protect

\[
p_L(\theta,\lambda)=L^{-1}\log\operatorname{Tr}
 \exp[-\theta H_L/t+\lambda A_L].
\]

The source is dimensionless in the exponent. It is not an undeclared
magnetic-field unit or a new physical ensemble. At lambda=0 this is the
earlier corrected log density. Differentiating the finite matrix exponential
by Duhamel's formula shows p_L is convex in lambda; its second derivative
is the connected Kubo covariance divided by L. Occupation complement with
the bipartite particle-hole transform preserves H_L and sends A_L to -A_L,
so the first derivative at zero vanishes. Consequently
p_L''(theta,0)=K_L(theta)/L for the earlier dimensionless Kubo readout.

For Hermitian X,Y, the eigenvalue min-max bound gives
|log Tr exp X-log Tr exp Y|<=||X-Y||. Thus p_L is 3/4-Lipschitz in theta
and 1/2-Lipschitz in lambda, uniformly in L. These are bounds for the
declared source function, not for its derivatives.

## 2. The same field has a thermodynamic pressure

Take open chains in even blocks of length 2n, and write a_n for their log
partition at the same theta,lambda. Internal CAR-even bond operators on
disjoint blocks tensorize, and the staggered source adds without a phase
change across an even block. Joining two blocks adds one bond of norm 3/4.
Therefore, with c=3theta/4,

\[
 |a_{n+m}-a_n-a_m|\le c.
\]

The sequences a_n+c and a_n-c are respectively subadditive and
superadditive. The per-site bound |p_L-log 2|<=3theta/4+|lambda|/2 keeps
these limits finite. Their normalized Fekete limits agree because 2c/n tends
to zero; their infimum/supremum characterizations give
|a_n-2n p(theta,lambda)|<=c. Closing the periodic CAR bond changes the
log partition by at most c, even though that bond has a parity string in
the occupation tensor basis. Hence the actual full-Fock periodic pressure
has the common target and uniform field bound

\[
 |p_L(\theta,\lambda)-p(\theta,\lambda)|
 \le\frac{3\theta}{2L}. \tag{SF-1}
\]

The target inherits convexity and both Lipschitz constants. Its rational
parameter presentation therefore completes uniquely to the admitted
parameter half-plane by [PC-1](cs_q_presentation_completion.md). This is
an infinite-volume thermodynamic function at the fixed lattice; it is not
yet a spatial-mesh field theory.

## 3. Bind nonzero-source SQL histories to transfer

Let h=log q>=0, d=log v with v>0, E=sum_(even x) P_x, B=sum_(odd x) P_x,
and D=exp(d A_L)=v^A_L. The actual generating trace is

\[
 Z_{L,M}(q,v)=\operatorname{Tr}(e^{hB}D e^{hE}D)^M.
\]

The earlier local-breakup/history bijection still applies: insert v^A at
each half-time state. Its diagonal factors multiply to v^Q, where
Q=sum_(half times) A(state_t). Therefore the original signed graph/orientation
sum with weight v^Q equals this trace. No new sign-character cancellation
law is assumed. The original SQLite connection already provides exact
`qpow`; the new tests query its actual histories, rather than a cached value.

The effective parameters are theta_hat=M log q and lambda_hat=2M log v.
The physical pressure sample is log Z/L-theta_hat/4. Holding q or v fixed
while increasing M changes these parameters and does not refine one target.
At q=1 the exact free trace is (v^M+v^-M)^L; at v=1 the earlier partition
trace, including Z_(4,2)(3,1)=912, is recovered.

## 4. A joint time/volume bound with a signed source

The pair is similar to the positive Hermitian matrix
S=e^(hB/2) D e^(hE) D e^(hB/2). Both S and exp(hG+2dA_L) have smallest
eigenvalue at least exp(-L|d|): use E,B>=0 and D^2>=exp(-L|d|)I.
In the five exponential factors of S the sum of operator norms is at
most T=L(h+|d|). Its linear term is hG+2dA_L. Bounding each exponential
series by its scalar norm series gives a nonlinear remainder at most
T^2 exp(T)/2 for each of S and the target exponential. Thus

\[
 \|S-e^{hG+2dA_L}\|\le T^2 e^T.
\]

For positive matrices with lower eigenvalue alpha, the resolvent formula
for log bounds its operator Lipschitz constant by
integral_0^infinity (alpha+s)^-2 ds=1/alpha. Apply this with
alpha=exp(-L|d|), then the log-trace exponential bound to M log S.
After division by L, the time error at the effective parameters is at most

\[
 M L(h+|d|)^2\exp[L(h+2|d|)].
\]

Declare common targets theta in [r-rho_theta,r+rho_theta], with r>=rho_theta>=0,
and lambda in [s-rho_lambda,s+rho_lambda], with s signed and rho_lambda>=0.
Choose exact rational q=1+r/M and
v=(1+|s|/(2M))^sign(s), taking v=1 at s=0. The scalar logarithm inequality
0<=x-log(1+x)<=x^2/2 gives target drifts

\[
 \delta_\theta=r^2/(2M)+\rho_\theta,\qquad
 \delta_\lambda=s^2/(4M)+\rho_\lambda.
\]

Combining these with SF-1 gives a total pressure radius

\[
 b=\frac L M(r+|s|/2)^2
       \exp\left[\frac L M(r+|s|)\right]
   +\frac34\delta_\theta+\frac12\delta_\lambda
   +\frac{3(r+\rho_\theta)}{2L}. \tag{SF-2}
\]

For bounded r,s, even L tending to infinity, M/L tending to infinity,
and both declared radii tending to zero, b tends to zero. M=L^2 is one
admissible infinite-family schedule. This field bound is coarser than the
earlier zero-source bound; it does not replace its M>=L result.

Native and Python bound objects replace exp(x) by the exact upper bound
3^ceil(x), since e<3 and x>=0. The majorant stays bounded along this
schedule, so it also yields vanishing error. Bounded execution admits at
most 256 sites/repetitions and exponent ceiling 64. Actual native CAR traces
retain the four-site carrier ceiling; source traces allow at most 16
repetitions. Python occupation traces use the existing bounded 4/6-site
work preflight. None of those finite caps is an execution of the infinite
family or a restriction on the written proof.

Certified rational logarithm intervals enclose log Z/L-theta_hat/4.
Widening them by the finite portion of SF-2 encloses p_L at the declared
targets; widening by all of SF-2 encloses the same thermodynamic p.

## 5. What response convergence actually follows

For fixed theta, convexity makes the distributional second derivative
mu_theta=d^2p(theta,lambda)/d lambda^2 a positive Radon measure. The
1/2-Lipschitz bound gives total mass at most one. At finite L the
corresponding measure is p_L''(theta,lambda)d lambda. For phi in C_c^2(R),
integration by parts and SF-1 give

\[
 \left|\int\phi p_L''\,d\lambda-\int\phi\,d\mu_\theta\right|
 \le\frac{3\theta}{2L}\|\phi''\|_{L^1}. \tag{SF-3}
\]

This establishes a quantitative weak response limit for the actual source
family. Uniform mass bounds extend convergence to compactly supported
continuous test functions by smooth approximation. It does not evaluate
a pointwise susceptibility at lambda=0.

At field center x and fixed resolution epsilon>0 protect

\[
 D_\epsilon p(x)=\frac{p(x+\epsilon)-2p(x)+p(x-\epsilon)}{\epsilon^2}
 =\int\frac{(\epsilon-|u|)_+}{\epsilon^2}\,d\mu_\theta(x+u).
\]

The equality follows by integrating the distributional second derivative
against the triangular kernel. It states precisely which smeared response
is computed. If the three pressure enclosures have radii b_minus,b_zero,
b_plus, their response radius is
(b_minus+2b_zero+b_plus)/epsilon^2. Each input radius already includes its
certified logarithm uncertainty. The sampler constructs all three points
at one supplied temperature.
For fixed epsilon the SF-2 schedule therefore closes this actual finite-
resolution response. If epsilon also shrinks, pressure/logarithm errors
must be o(epsilon^2), and a pointwise identification needs further evidence.

Conditional on a genuine bound |p'''|<=C on [x-epsilon,x+epsilon], the
triangular kernel's mean |u| is epsilon/3, giving
|D_epsilon p(x)-p''(x)|<=C epsilon/3. The measurement owner can propagate
a declared C; it does not verify function smoothness or derive C from a
flag. SF-1–SF-3 alone supply no such certificate. The later
[analytic-source theorem](meron_analytic_response.md) derives uniform
regularity in an explicit high-temperature region.

Even global uniform convergence of convex smooth Lipschitz functions is
insufficient. Let p(x)=log cosh(x)/2 and, for integers n>=1,
p_n(x)=(1-1/n)p(x)+log cosh(nx)/(2n^2). Both are convex and 1/2-Lipschitz.
Convexity and cosh(nx)<=2^(n-1)cosh(x)^n give
0<=p_n-p<=(n-1)log(2)/(2n^2) globally. Nevertheless p''(0)=1/2 and
p_n''(0)=1-1/(2n). This is a logical countermodel to differentiating a
pressure convergence claim, not a counterexample to this Hamiltonian.

## 6. Literature route and remaining physical obligations

[Bluhm, Capel and Perez-Hernandez, arXiv:2104.04419v2](https://arxiv.org/pdf/2104.04419v2)
prove uniform finite-interval clustering in Theorem 6.2 and local
indistinguishability in Proposition 7.1 for the stated one-dimensional
finite-range spin setting. Those results motivate an open-spin bulk route.
The [publisher abstract for Araki (1969)](https://link.springer.com/article/10.1007/BF01645134)
reports analytic free energy and local expectations; its full theorem was
not imported or audited here. Neither citation is credited with the
pointwise susceptibility claim for our periodic full-Fock ensemble.

Two-site blocking admits the staggered source as a translation-invariant
on-site term. A future import must still handle the actual parity-dependent
periodic boundary and prove uniform imaginary-time connected-correlation
control or another valid derivative argument. The one-bond pressure bound
does not automatically control second derivatives. A spatial continuum
profile also needs lattice spacing, coupling/temperature scaling, sectors,
smeared observables and an explicitly chosen convergence topology. Constants
valid at fixed theta need not remain uniform when theta grows with L.

Pontryagin character closure supplies the selected geometry, not these
dynamical estimates. SF-1–SF-3 add actual pressure and weak/finite-resolution
response control to that route. The later analytic-source theorem closes pointwise intensive Kubo
susceptibility in its stated high-temperature region. Outside that region,
and for spatial field scaling and the enlarged Genesis obligations, the
remaining obligations stay open.

## 7. Owners and reproducibility

`omega_quantum_physics::meron_source_field` owns the common-source bound
plan, and `meron_time_refinement::FiniteMeronChain` owns the actual trace.
It reuses CAR and generic matrix powers. `omega_measurement::finite_response`
reuses the existing bounded readings and kernel intervals for generic
response error propagation. WDP retains the source plan and owner trace;
it introduces no second field/interval solver. AuthorityEffect is None.

From the repository root, run the bounded companions:

```sh
py -3.12 -B -m pytest -q -o addopts= -p no:cacheprovider omega_engine_projects/finite_to_continuum/tests/source_response omega_engine_projects/finite_to_continuum/tests/observable_transport
cargo test --offline --locked -j1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_measurement --test finite_response
cargo test --offline --locked -j1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_quantum_physics -p omega_wdp --test meron_source_field --test meron_source_adapter
```

The new Python cases bind four actual source SQL traces, signed fields,
normalizations, the three-point sampler, and typed resource refusals.
Native cases cover model traces, bound arithmetic, interval transport and
the thin adapter. Analytic SF-1–SF-3 remain written results, not empirical
inferences from those tests or extensions of the metric Lean theorem.
