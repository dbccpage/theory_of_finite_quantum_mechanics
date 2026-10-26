# Exact Euclidean covariance positivity for the periodic Meron chain

Status: finite-volume theorem for every even size and positive temperature;
the high-temperature Hamiltonian volume limit is treated in the
[thermodynamic-limit supplement](meron_euclidean_thermodynamic_limit.md).
Comparison with the discrete transfer and a joint spacetime schedule remain open. AuthorityEffect: None.

This result concerns the exact Hamiltonian Gibbs trace, not a probability
interpretation of the signed SQL histories. It retains the same full periodic
CAR carrier and the same staggered source as the
[analytic response](meron_analytic_response.md) and
[time-labelled transfer](meron_time_dependent_analyticity.md).

## EP-1. Euclidean time and a real spectral basis

For even `L>=4`, let `c_x` be the CAR lowering operators, `n_x=c_x^*c_x`,
`y=x+1` modulo `L`, and

\[
 P_x=\tfrac12(n_x+n_y-2n_xn_y+c_x^*c_y+c_y^*c_x),\quad
 K_L=H_L/t=\sum_x(\tfrac14 I-P_x),\quad
 a_x=(-1)^x(n_x-\tfrac12),\quad A_L=\sum_xa_x. \tag{EP-1}
\]

Take `theta>0`, `Z=Tr exp(-theta K_L)`, and
`rho=exp(-theta K_L)/Z`. Normalized imaginary time lies on the circle
`u in R/Z`; for `0<=u<=1` define

\[
 a_x(u)=e^{u\theta K_L}a_xe^{-u\theta K_L},\qquad
 C_{xy}(u)=\operatorname{Tr}(\rho\,a_x(u)a_y)
       -\operatorname{Tr}(\rho a_x)\operatorname{Tr}(\rho a_y). \tag{EP-2}
\]

For two arbitrary time arguments, `C_(xy)(tau,sigma)` means the thermal
time-ordered kernel obtained from EP-2 at `u=tau-sigma mod 1`. Since the
equal-time density operators commute, the endpoint values agree and this
kernel is continuous on the time circle. This is an imaginary-time
correlation, not real-time dynamics.

In the ordered occupation basis, every `c_x` has entries `0,+1,-1`.
Consequently `K_L` is real symmetric, including the wrapping hopping
sign, and every `a_x` is real diagonal. Choose a real orthonormal
eigenbasis `|alpha>` of `K_L`, with energies `E_alpha`. Put
`p_alpha=exp(-theta E_alpha)/Z` and
`v_(alpha,beta)(x)=<alpha|a_x|beta> in R`.
The particle-hole CAR automorphism `c_x -> (-1)^x c_x^*` preserves each
`P_x` for even `L` and reverses each `a_x`. Trace invariance therefore
gives `Tr(rho a_x)=0` for every site. The centering term in EP-2 vanishes.

## EP-3. Positive Fourier coefficients

For integer `m`, set `omega_m=2 pi m` and
`C_hat_(xy)(m)=integral_0^1 exp(-i omega_m u) C_(xy)(u) du`.
The spectral expansion of EP-2 is

\[
 C_{xy}(u)=\sum_{\alpha,\beta}p_\alpha
  e^{-u\theta(E_\beta-E_\alpha)}
  v_{\alpha\beta}(x)v_{\alpha\beta}(y). \tag{EP-3}
\]

Pair the two ordered terms with distinct energies
`E_alpha<E_beta`. With `d=theta(E_beta-E_alpha)>0`, their time factor is
`p_alpha[exp(-du)+exp(-d(1-u))]`. Its integer-circle Fourier integral is
`2(p_alpha-p_beta)d/(d^2+omega_m^2)`. Equal-energy terms have only the
zero Fourier mode. Thus the exact coefficient matrix is

\[
 \widehat C_{xy}(m)=
 \sum_{E_\alpha<E_\beta}
 {2(p_\alpha-p_\beta)d_{\alpha\beta}
       \over d_{\alpha\beta}^2+\omega_m^2}
 v_{\alpha\beta}(x)v_{\alpha\beta}(y)
 +\mathbf1_{m=0}\sum_{E_\alpha=E_\beta}
 p_\alpha v_{\alpha\beta}(x)v_{\alpha\beta}(y),
 \quad d_{\alpha\beta}=\theta(E_\beta-E_\alpha). \tag{EP-4}
\]

The first sum takes one orientation of every unequal-energy eigenvector
pair; the second takes all ordered equal-energy pairs. All coefficients
are nonnegative. The real spectral basis makes each summand a positive
semidefinite outer product. Hence for any complex spatial vector `b`,

\[
 \sum_{x,y}\overline b_x\widehat C_{xy}(m)b_y\ge0. \tag{EP-5}
\]

The finite-dimensional kernel is continuous and its Fourier coefficients
decay as `O_L(m^-2)`. Parseval therefore proves, for every real or complex
square-integrable periodic spacetime profile `F`,

\[
 \sum_{x,y}\int_0^1\!\int_0^1
 \overline{F(\tau,x)}C_{xy}(\tau-\sigma)F(\sigma,y)
 \,d\tau\,d\sigma
 =\sum_{m\in\mathbb Z}\sum_{x,y}
 \overline{\widehat F_m(x)}\widehat C_{xy}(m)
 \widehat F_m(y)\ge0. \tag{EP-6}
\]

Thus the exact finite-volume Euclidean covariance is positive
semidefinite. It defines consistent finite-dimensional Gaussian laws for
test functions on this finite spatial carrier. EP-6 says nothing about
positivity of the finite signed transfer-history weights.

## EP-7. Staggered row sum and surviving finite-volume time modes

Translation by one physical CAR site preserves `K_L` and sends `a_x` to
`-a_(x+1)`. Accordingly `C_(x+1,y+1)=C_(xy)`, and every spatial row sum is

\[
 k_{L,\theta}(u)=\sum_yC_{0y}(u)
  ={1\over L}\operatorname{Tr}(\rho A_L(u)A_L),\qquad
 \widehat k_{L,\theta}(m)
  ={1\over L}\sum_{x,y}\widehat C_{xy}(m)\ge0. \tag{EP-7}
\]

The zero mode is exactly the static Kubo response already targeted in
AR-6--AR-9. Twice differentiating
`p_L(theta,z)=L^(-1)log Tr exp(-theta K_L+z A_L)` by the finite-dimensional
Duhamel formula, and using the vanishing first moment, gives

\[
 p_L''(\theta,0)={1\over L}\int_0^1
  \operatorname{Tr}(\rho A_L(u)A_L)\,du
 =\widehat k_{L,\theta}(0). \tag{EP-7a}
\]

Thus the established thermodynamic static susceptibility is the selected
zero-frequency limit of this Euclidean kernel. EP-7a does not identify
any nonzero-frequency volume limit.

For `m!=0`, EP-4 has no equal-energy term. Its strictly positive weights
show that `k_hat_(L,theta)(m)>0` for **every** nonzero integer `m` exactly
when `[K_L,A_L]!=0`. This commutator is nonzero in the one-particle
sector: the ordinary edge `0--1` has
`<1|K_L|0>=-1/2`, while `A_L|0>=|0>` and
`A_L|1>=-|1>`, so
`<1|[K_L,A_L]|0>=-1`. Therefore

\[
 \widehat k_{L,\theta}(m)>0
 \quad(L\ge4\text{ even},\ \theta>0,\ m\in\mathbb Z\setminus\{0\}).
 \tag{EP-8}
\]

The contrast with zero coupling is exact. At `theta=0`, the normalized
trace gives `C_(xy)(u)=delta_(xy)/4`, so `k_(L,0)=1/4` and every nonzero
time Fourier mode vanishes. For each **fixed** even `L`, expanding EP-4
at a nonzero mode also gives

\[
 \widehat k_{L,\theta}(m)
 = {\theta^2\over L\,2^L\omega_m^2}
   \operatorname{Tr}([K_L,A_L]^*[K_L,A_L])
   +O_L(\theta^3)
 = {\theta^2\over2\omega_m^2}+O_L(\theta^3). \tag{EP-9}
\]

For the last equality, the density terms commute with `A_L`, while
`[K_L,A_L]=sum_x(-1)^x(c_x^*c_(x+1)-c_(x+1)^*c_x)`.
Distinct physical edge-hop terms are orthogonal in the normalized
infinite-temperature trace when `L>=4`, and each has squared trace `1/2`.
The remainder in EP-9 is **fixed-volume**; no uniform-in-`L` lower
bound follows from this expansion.

## EP-10. Volume-uniform temporal control of the row sum

The same spectral formula gives a volume-uniform *upper* bound without
assuming that the nonzero modes have a common volume limit. Define the
thermal double-commutator expectation

\[
 D_{L,\theta}:=\operatorname{Tr}\rho[A_L,[K_L,A_L]]
 =2\sum_{E_\alpha<E_\beta}(p_\alpha-p_\beta)
    (E_\beta-E_\alpha)|\langle\alpha|A_L|\beta\rangle|^2.
 \tag{EP-10}
\]

It is nonnegative. EP-9's local commutator calculation gives
`[A_L,[K_L,A_L]]=2 sum_x(c_x^*c_(x+1)+c_(x+1)^*c_x)`.
Each edge hopping has operator norm one, including the wrapping CAR edge.
Hence `0<=D_(L,theta)<=2L` for every even `L>=4` and every `theta>0`.

For `0<=u<=1`, differentiate the paired time factor in EP-3. Its derivative
has magnitude at most `(p_alpha-p_beta)d_(alpha,beta)`, because
`|exp(-du)-exp(-d(1-u))|<=1-exp(-d)`. Consequently

\[
 |k'_{L,\theta}(u)|\le {\theta D_{L,\theta}\over2L}
 \le\theta. \tag{EP-11}
\]

The one-sided endpoint derivatives obey the same bound, so the periodic
kernel is `theta`-Lipschitz in circle distance. For `m!=0`, EP-4 and
`d^2+omega_m^2>=omega_m^2` give

\[
 0<\widehat k_{L,\theta}(m)
 \le {\theta D_{L,\theta}\over L\omega_m^2}
 \le {\theta\over2\pi^2m^2}. \tag{EP-12}
\]

The Fourier series is absolutely and uniformly convergent. Its
nonnegative coefficients, EP-7a and
`sum_(m!=0) 1/m^2=pi^2/3` imply

\[
 0\le k_{L,\theta}(0)-p_L''(\theta,0)\le\theta/6,
 \qquad |k_{L,\theta}(u)-p_L''(\theta,0)|\le\theta/6.
 \tag{EP-13}
\]

On the admitted analytic interval `0<=theta<=1/192`, AR-6 and Cauchy's
estimate give `0<=p_L''(theta,0)<=2/(19R^2)` with `R=1/64`, uniformly
in `L`. Thus EP-11 and EP-13 make the row-sum kernels uniformly bounded
and equicontinuous. Along every sequence of even volumes tending to
infinity, Arzela--Ascoli supplies a uniformly convergent subsequence.
Every such limit is a continuous positive-definite time-circle kernel;
its zero Fourier mode is the previously proved common
`chi(theta)=lim_L p_L''(theta,0)`, and its nonzero coefficients obey
EP-12. These statements do **not** prove that all subsequences share a
kernel or that a positive finite-volume nonzero coefficient stays
strictly positive in the limit.

## Boundary of the theorem

EP-4--EP-8 settle positivity and nontrivial temporal modes of the
**exact finite-volume Hamiltonian** kernel. EP-10 supplies subsequential
uniform limits of its spatial row sums in the high-temperature region,
but neither uniqueness nor an absolutely summable infinite-volume
site-pair kernel. Strict positivity of nonzero modes need not pass to a
subsequence limit without a uniform lower bound. The time-labelled
discrete transfer's pair derivatives still need an `M`-uniform spatial
bound and a quantitative comparison with EP-2. A joint `(L,M)` schedule,
spacetime distribution topology and finite signed-measure interpretation
are not supplied here.

The subsequent [thermodynamic-limit supplement](meron_euclidean_thermodynamic_limit.md)
proves uniqueness and an absolutely summable infinite-volume site-pair kernel
on its declared high-temperature region. Its window argument supplies a
uniform positive lower bound for nonzero time modes on `0<theta<=1/192`.
These later results resolve the volume-limit questions listed above for that
region. They do not establish the discrete-transfer comparison.
