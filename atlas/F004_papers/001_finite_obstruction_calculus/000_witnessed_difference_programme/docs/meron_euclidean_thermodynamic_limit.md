# The Euclidean thermodynamic limit of the periodic Meron row-sum covariance

Status: written theorem on `0<=theta<=1/192` with an imported polymer
criterion; strict positivity of every nonzero time mode is proved on the
whole window `0<theta<=1/192`, with the explicit bound `theta^2/(36 pi^2 m^2)`
(section "Window positivity", added 2026-10-07). TL-9's earlier bound
`theta^2/(16 pi^2 m^2)` on `0<theta<=theta_*` stands as written.

This continues the [finite-volume positivity theorem](meron_euclidean_covariance_positivity.md)
and closes the three items its boundary left open on the high-temperature
interval: uniqueness of the volume limit, an absolutely summable
infinite-volume site-pair kernel, and strict positivity of a nonzero limit
mode in an explicit window. It uses the polymer representation of the
[analytic response](meron_analytic_response.md) (AR-2 and the
Kotecký–Preiss criterion it imports), together with standard finite-dimensional
spectral theory, Gibbs variational inequalities, complex analysis, and
Fourier analysis. The model-specific estimates are proved below; the abstract
polymer criterion is an external theorem. The exact finite checks are in
`code/meron_thermodynamic_limit/` with tests in
`code/tests/test_meron_thermodynamic_limit.py` and
`code/tests/test_meron_positivity_window.py`; the rational constants are
also stated in `lean4/WitnessedDifference/MeronThermoLimitConstants.lean`. The analytic estimates
below are written proofs. They are not Lean theorems.

## TL-0. The exact object

Take even `L>=4`, the full `2^L`-dimensional CAR space with the physical
periodic hopping sign (the wrapping bond carries the Jordan–Wigner string;
nothing is erased), and

\[
 P_x={1\over2}\bigl(n_x+n_{x+1}-2n_xn_{x+1}+c_x^*c_{x+1}+c_{x+1}^*c_x\bigr),
 \qquad K_L=\sum_{x\in\mathbb Z_L}\bigl(I/4-P_x\bigr),
\]

\[
 a_x=(-1)^x(n_x-\tfrac12),\qquad
 \rho_{L,\theta}=e^{-\theta K_L}/\operatorname{Tr}e^{-\theta K_L},\qquad
 a_x(u)=e^{u\theta K_L}a_xe^{-u\theta K_L}.
\]

The Euclidean two-point function, its row sum and the time modes are

\[
 C^L_{xy}(u)=\operatorname{Tr}\rho_{L,\theta}\,a_x(u)a_y,\qquad
 k_{L,\theta}(u)=\sum_{y\in\mathbb Z_L}C^L_{0y}(u),\qquad
 \widehat k_{L,\theta}(m)=\int_0^1k_{L,\theta}(u)e^{-2\pi imu}\,du .
 \tag{TL-0}
\]

The CAR automorphism `c_x -> (-1)^x c_x^*` preserves `K_L` and the full
trace on an even ring, and sends every `a_x` to `-a_x`. Thus `Tr rho a_x=0`
for every admitted temperature, so `C` is already the connected function.
The finite series checks through order 5 for `L=4` and order 6 for `L=6`
are controls for this symmetry, not its all-temperature proof. On a bond's
two-mode occupation space, `P_x` is zero on the empty and doubly occupied
states and has block `[[1,1],[1,1]]/2` on the one-particle states. Hence
`P_x^2=P_x=P_x^*` in every CAR representation, including the wrapping bond.
It follows that `||I/4-P_x||=3/4` and `||a_x||=1/2`.

## TL-1. A two-segment polymer gas

Fix `0<=u<=1`, sites `0,y`, and complex `theta,z,w`. Write

\[
 \Xi(z,w)=2^{-L}\operatorname{Tr}\Bigl(e^{-(1-u)\theta K_L}e^{za_0}
          e^{-u\theta K_L}e^{wa_y}\Bigr).
\]

Its labels are the `2L` pairs (segment, bond) and the two sources. A bond
label of segment length `s<=1` has operator `-s theta(I/4-P_x)`, of norm at
most `(3/4)|theta|`; a source label has norm `|z|/2` or `|w|/2`. Expand each
segment exponential into words. Letters with disjoint supports are even CAR
operators and commute, also across the wrapping bond, so every word splits
into its connected label components and the normalized trace factorizes over
them (AR §2–3). The bounds below use exactly these premises: (i) every bond
term is `4` times a projector; (ii) for every word on pairwise disjoint label
components the normalized trace is the product of the traces of the
components; (iii) a bond term commutes with every local operator and every
source off its bond, and a source `a_z` commutes with every local operator
off `z`; (iv) the staggered source has vanishing mean, `Tr(K^n a_x)=0` for
all `n`, so `C` is the connected function; (v) on the physical ring, every
bond term and source is even, that is, commutes with the total parity. For
the physical ring the local operators are `c_z`, `c_z^*` and (i)–(v) are CAR
statements. For the sign-erased ring of TL-4 they are spin-language
statements: the erased wrap term is a projector on two sites of the tensor
product, and the local operators are the site Paulis.

*Locality lemma.* (ii) follows from (iii) and (v). On the physical ring, an
operator that commutes with `c_w`, `c_w^*` for every `w` outside a set `S` is
the sum of an even element of the CAR algebra of `S` and an odd element of it
times the parity of the complement; if it is also even, the second part
vanishes. Even elements of the CAR algebras of disjoint sets commute, and the
normalized trace of their product is the product of the traces. On the
erased ring, an operator commuting with every site Pauli off `S` acts only on
the tensor factor of `S`, and the trace of the tensor product factorizes.
*Vanishing mean on the erased ring.* The global spin flip `prod_z X_z` fixes
every bond term (it maps `n` to `1-n`, which fixes `n_x+n_y-2n_xn_y`, and it
swaps the two hopping terms) and maps `a_x` to `-a_x`, so
`Tr(K^n a_x)=-Tr(K^n a_x)=0`. The physical ring uses the particle-hole map in
the same way.

Exact check `bond_locality`, both rings, `L=4,6`: (i); trace factorization
for every set of pairwise disjoint units, a unit being one bond term or one
source (products of single units; the word-level statement (ii) is the
lemma); (iii); (iv) through `n=L`; (v); and that the `K` it uses is built
from those bond terms, `4K=L·I-Σ4P_x`. It rejects four mutations, each
of which passes the checks that came before it:
the nonlocal bond term `4P_(0,1)(I+Z_2···Z_{L-1})/2` (round-4
counterexample R4-CX-01), the source `a_{L/2}` dressed by the total parity
(round-5 counterexample R5-CX-01, which changes `C^6_{03}` at order `theta^2`),
and the odd bond term `2(I+(c_0+c_0^*)Z_2···Z_{L-1})` (round-5 objection
R5-OBJ-02), and `4K+4Z_0Z_{L/2}` with the bond terms unchanged (round-6
counterexample R6-CX-01, which changes `C^4_{02}` and `C^6_{03}` at order
`theta`). The binding check and this fourth mutation were added after the
run closed and were not reviewed by its critics. So
TL-1–TL-3 hold for the erased ring with the same constants. This is an
exact hard-core polymer gas whose weight obeys
AR-2, `|w(C)|<=prod_(i in C)(e^{||X_i||}-1)`. A label meets at most `Delta=7`
others. On

\[
 |\theta|\le1/96,\qquad |z|,|w|\le1/64
\]

every label norm is at most `1/128`. The connected-set count of AR §4, with
`e<3` and `e^x-1<=x/(1-x)`, gives the rooted majorant

\[
 S_1={3\,t\over1-28\cdot3t}\Big|_{t=1/127}={3\over43},
 \qquad (\Delta+1)S_1={24\over43}<1,
 \tag{TL-1}
\]

so the Kotecký–Preiss criterion imported in AR (Fernández–Procacci,
arXiv:math-ph/0605041v2, eqs. 2.10, 2.14, 2.15) holds uniformly in `L` and
`u`. `log Xi` is analytic on this polydisk. Its mixed difference
`f=log Xi(z,w)-log Xi(z,0)-log Xi(0,w)+log Xi(0,0)` keeps only clusters that
contain both source labels, and the pinned majorant bounds it by `2S_1`.
Since `C^L_{0y}(u)=partial_z partial_w log Xi(0,0)` (the means vanish),
Cauchy's estimate on the polydisk gives

\[
 |C^L_{0y}(u)|\le M_1:=2S_1\cdot64^2={24576\over43}
 \qquad(|\theta|\le1/96,\ 0\le u\le1,\ \text{all even }L).
 \tag{TL-2}
\]

## TL-2. Decay in the exact distance

Give each bond label its own coupling `theta_b`. A cluster that contains both
sources contains a connected chain of bond labels joining `0` to `y`, hence at
least `d_L(0,y)` distinct bonds. So `C^L_{0y}` is analytic on the disk and
vanishes to order `d=d_L(0,y)` at `theta=0`. Schwarz's lemma on
`|theta|<=1/96` gives

\[
 |C^L_{0y}(u)|\le M_1(96|\theta|)^{d_L(0,y)}.
 \tag{TL-3}
\]

The exact order is attained: for `L=6` and the chain `[-4,4]` the first
nonzero `theta`-coefficient of `C_{0y}` is at order `|y|` (ring distance on
the ring). Summing TL-3 over the two sites at each distance gives the uniform
tail. If `mu>=0` and `q=96 |theta| e^mu<1` then

\[
 \sup_{L}\sup_{0\le u\le1}\sum_{y}e^{\mu d_L(0,y)}|C^L_{0y}(u)|
 \le B(\theta):=M_1{1+q\over1-q}.
 \tag{TL-4}
\]

The magnitude is essential. At `theta=-1/96`, `mu=0`, a signed ratio would
give `q=-1` and a zero bound, while `a_0^2=I/4` implies `C^L_00(0)=1/4`.
The corrected ratio is `q=1`, so this endpoint is outside TL-4's domain.
This counterexample concerns the signed weighted bound, not the separate
positive-temperature theorem. TL-7 retains its explicit `q<1` restriction.

## TL-3. The infinite-volume two-point function

Let `C^R` be the same function on the open chain `[-R,R]` (no wrapping bond).
TL-1–TL-3 hold for it verbatim. `C^{R+1}_{0n}-C^R_{0n}` keeps only clusters
that touch a bond outside `[-R,R]` and contain the source at `0`; each has at
least `R+1` bonds, so

\[
 |C^{R+1}_{0n}(u)-C^R_{0n}(u)|\le2M_1(96|\theta|)^{R+1}.
\]

The same count gives more. Let `I` and `J` be any two finite intervals that
both contain `[-R,R]`, and let `C^I`, `C^J` be the open-chain functions on
them. `f_I-f_J` keeps only clusters that contain the source at `0` and touch a
bond outside `[-R,R]`. Such a cluster contains the bonds `(0,1),…,(R,R+1)` or
`(-R-1,-R),…,(-1,0)`, so it has at least `R+1` bond labels. The difference is
analytic on the TL-1 polydisk, bounded there by `2M_1` after the two source
derivatives, and vanishes to order `R+1` in `theta`, so Schwarz gives

\[
 |C^I_{0n}(u)-C^J_{0n}(u)|\le2M_1(96|\theta|)^{R+1}
 \qquad([-R,R]\subseteq I\cap J).
\]

Hence `C^infty_{0n}(u)=lim_R C^R_{0n}(u)` exists uniformly in `u` on
`|theta|<1/96`, is analytic there, inherits TL-3 with `d=|n|`, and is the
same along every exhausting sequence of intervals. It is translation
invariant: shifting an open chain by `x` relabels its CAR modes and maps
`a_x a_{x+n}` to `a_0a_n`, since the two staggering signs `(-1)^x` cancel. So
`C^I_{x,x+n}=C^{I-x}_{0n}`, `I-x` exhausts `Z` when `I` does, and
`C^infty_{x,x+n}=C^infty_{0n}`. It is the infinite-volume two-point
function. Its natural space is `ell^1_mu(Z;C[0,1])` with norm
`sum_n e^{mu|n|} sup_u|C(n,u)|`, finite for every `mu` with `q<1`.

## TL-4. The lift and the unique volume limit

Define the wrapped difference

\[
 D_y(u)=C^L_{0y}(u)-\sum_{n\equiv y\ (L)}C^\infty_{0n}(u).
\]

The model is fermion-periodic: the wrapping term is the CAR hopping
`c_{L-1}^*c_0+c_0^*c_{L-1}` (with `n_{L-1}`, `n_0`). It is even, supported on
the two modes `L-1` and `0`, and independent of the global parity. Every
cluster with fewer than `L` bond labels lies on an arc of at most `L` sites.
The site relabelling of that arc onto a segment of the line is injective. It
preserves which labels overlap, so the Ursell coefficients agree. It maps the
wrapping term onto the line hopping between the corresponding sites, so the
normalized traces agree. Therefore all `theta`-coefficients of `D_y` below
order `L` vanish. The argument uses only locality of the wrapping term. The
sign-erased model used below as a mutation is the spin-periodic chain: in
fermion language its wrapping term carries a parity string, but in spin
language it is a two-site term, and below order `L` no cluster reaches around
the ring. So the lift holds for it as well, and it is a different model, not
an exception to the argument (round-2 correction: round 1 called it outside
the lift). Since TL-1–TL-3 hold for it in spin language, the bound
`|D_y|<=4M_1(128|theta|)^L` below holds for it too. Exact check: for `L=4` and `L=6` the physical and erased kernels
`C_{0y}` agree site by site below order `L` and first differ at order `L`.
(Exact checks: for `L=6` and `L=8` the lift agrees through the computed
order 4; for `L=4` it agrees through order 3 and differs at order 4.)
On `|theta|<=1/128` the sum over `n` converges with ratio `3/4`, and
`|D_y|<=M_1(1+512/175)<4M_1`. Schwarz on that disk gives
`|D_y|<=4M_1(128|theta|)^L`. With `k_theta(u)=sum_n C^infty_{0n}(u)`,

\[
 \varepsilon_L(\theta):=\sup_{0\le u\le1}|k_{L,\theta}(u)-k_\theta(u)|
 \le4M_1L(128\theta)^L\longrightarrow0
 \qquad(0\le\theta<1/128),
 \tag{TL-5}
\]

\[
 \sup_u|k_{L,\theta}(u)-k_{L',\theta}(u)|\le\varepsilon_L(\theta)+\varepsilon_{L'}(\theta).
 \tag{TL-6}
\]

So every sequence of even volumes has the same limit, and EP-10's
subsequential limits all equal `k_theta`. The rate is uniform on
`0<=theta<=1/192`, where `128 theta<=2/3`.

The wrap sign does not reach the lift or the limit. It does reach the finite
kernel: erasing it changes the exact row-sum series first at order exactly
`L` (checked for `L=4` and `L=6`; for `L=6` the correct order-6 zero mode is
`3259/2580480`). That is the precise sense in which the sign matters.

**Embedding.** Put `E_L(n)=C^L_{0,n mod L}` for `-L/2<n<=L/2` and `0`
otherwise. For `0<=theta<=1/192`, `mu>=0` and `q<1`,

\[
 \|E_L-C^\infty\|_{\ell^1_\mu(\mathbb Z;C[0,1])}
 \le M_1q^{L/2}\Bigl(4L+{4\over1-q}\Bigr).
 \tag{TL-7}
\]

Proof. Write `r=96theta<=1/2` and `q=re^mu<1` with `mu>=0`. For a window site,
`E_L(n)-C^infty_{0n}=D_n+sum_{m≡n, m≠n}C^infty_{0m}`. First, by TL-4 and
`e^{mu|n|}<=e^{mu L/2}`,
`e^{mu|n|}|D_n|<=4M_1(128theta)^Le^{mu L/2}=4M_1q^{L/2}(128^2theta/96)^{L/2}`,
and `128^2theta/96<=8/9` for `theta<=1/192`; the `L` window sites give at most
`4M_1Lq^{L/2}`. Second, every wrapped image has `|m|>=L-|n|>=|n|`, so
`e^{mu|n|}|C^infty_{0m}|<=M_1e^{mu|n|}r^{|m|}<=M_1q^{|m|}`; each `m` outside
the window occurs for exactly one `n`, so these terms sum to at most
`2M_1q^{L/2}/(1-q)`. Third, the terms outside the window are bounded by the
same geometric sum. Adding the three parts gives (TL-7). The hypothesis
`mu>=0` is needed: for `mu` sufficiently negative the `n=0` window term does
not vanish while the right side tends to `0` (round-2 correction: the
statement had named it only in the proof).
The ring kernels therefore converge to the line kernel as site-pair kernels in
`ell^1_mu`, not only after summing over `y`.

## TL-5. Zero mode, symmetry and nonnegativity

- **Zero mode.** `int_0^1 k_{L,theta}=chi_L(theta)` (EP-7a) and TL-5 give
  `widehat k_theta(0)=chi(theta)`, the previously proved static
  susceptibility limit.
- **High-temperature value.** At `theta=0`, `C^L_{0y}=delta_{0y}/4`, so
  `k_0=1/4` for every `u` (exact). On the complex disk `|theta|<=1/192`,
  `q=1/2` and TL-4 give `|k_theta|<=3M_1`; Schwarz gives

  \[
   |k_\theta(u)-1/4|\le(3M_1+1/4)\,192\,\theta,
  \]

  so `k_theta(u)>0` for every `u` when `theta<43/56631360`.
- **Symmetry.** `k_theta(u)=k_theta(1-u)` (KMS and reflection; each exact
  coefficient polynomial is checked to satisfy it).
- **Nonnegativity.** `widehat k_{L,theta}(m)>=0` for every `m` (EP-7);
  uniform convergence passes it to `widehat k_theta(m)>=0`.

## TL-6. Strict positivity of the nonzero modes in a window

Let `omega=2 pi m`, `m!=0`. Integrate by parts twice over the time circle.
The KMS jump of `k'` is `theta/L Tr rho [A_L,[K_L,A_L]]=2 theta F_L`, with
`F_L=Tr rho h_0`, `h_0=c_0^*c_1+c_1^*c_0` (EP-9's commutator, checked
exactly), and `k''=theta^2 g_L`:

\[
 \omega^2\widehat k_{L,\theta}(m)=2\theta F_L(\theta)-\theta^2\widehat g_L(m),
 \qquad g_L(u)=\sum_y\operatorname{Tr}\rho\,B_0(u)a_y,
 \tag{TL-8}
\]

where `B_0=-[K_L,j_0]`, `j_0=c_1^*c_0-c_0^*c_1`, is supported on the four
sites `{-1,0,1,2}`. TL-8 is checked coefficientwise in `theta` (`L=4` through
order 5, `L=6` through order 4, modes 1 to 3), and `g_L=(1/L)Tr rho [K,[K,A]](u)A` is checked to equal the
local sum. An exact certificate gives `||B_0||^2<=3`: the integer matrix
`48I-(4B_0)^2` is positive semidefinite by exact symmetric elimination on the
four modes, and `32I-(4B_0)^2` is not. (A CAR polynomial's norm does not
depend on the representation.)

- `F`: one source `s h_0`, `|s|<=1/128`, same gas on `|theta|<=1/96`, gives
  `|F|<=128 S_1=384/43`. Exactly `F(0)=0`, `F'(0)=1/4`, so Schwarz gives
  `|F-theta/4|<=M_F(96theta)^2`, `M_F=384/43+1/384=147499/16512`.
- `g`: sources `z B_0`, `|z|<=1/576`, and `w a_y`, `|w|<=1/96`, bonds on
  `|theta|<=1/144`: label norm `1/192`, degree `11`,
  `S_g=3/59`, `|Tr rho B_0(u)a_y|<=M_g=2S_g·576·96=331776/59`, vanishing to
  the distance from `y` to the support. On `|theta|<=1/288` the sum over `y`
  is at most `6M_g`. Exactly `g(theta=0)=1/2` for every `u`, so its nonzero
  Fourier modes vanish at `theta=0`, and
  `|g-1/2|<=G·288theta`, `G=6M_g+1/2=3981371/118`.

These bounds are uniform in `L` and pass to the limit. Hence, for
`0<theta<=theta_*`,

\[
 \omega^2\widehat k_\theta(m)\ge\theta^2\Bigl({1\over2}-\theta(18432M_F+288G)\Bigr)
 \ge{\theta^2\over4},
 \qquad
 \theta_*={2537\over100281465600}\approx2.53\cdot10^{-8},
 \tag{TL-9}
\]

that is `widehat k_theta(m)>=theta^2/(16 pi^2 m^2)>0` for every `m!=0`, every
even `L` and the limit. The first inequality alone is strictly positive for
every `theta<1/(2(18432M_F+288G))=2theta_*=2537/50140732800`, so strict
positivity holds on `0<theta<2theta_*`; `theta_*` is only where the clean bound
`theta^2/4` stops. This matches EP-9's leading term
`theta^2/(2 omega^2)` up to the factor `1/2` spent on the error. It sits
below EP-12's upper bound `theta/(2 pi^2 m^2)`.

## TL-7. Audit

| Item | What was checked | How |
| --- | --- | --- |
| Normalization | `rho` divides by `Tr e^{-theta K}`, not by `2^L` | Exact: the unnormalized `theta^0` zero mode is `16`; dividing by `2^L` instead changes the series first at order 2 |
| Wrap sign | Kept in the model; the lift covers both the physical and the sign-erased ring; erasing the sign is a mutation that changes the finite kernel first at order `L` | Exact mutations and per-site comparison, `L=4,6`; the `L=6` series is recorded through order 6 |
| Embedding constant | The three parts of TL-7 add up to at most `M_1q^{L/2}(4L+4/(1-q))`, for `mu>=0` | Written; exact Fraction test for even `L=4..40` and three values of `e^mu>=1`; `e^mu<1` is rejected |
| Staggering and `P` scale | Removing `(-1)^x` or doubling `P` moves an exact coefficient | Exact mutations |
| Builders | Jordan–Wigner matrices and an independent bit builder agree | Exact, `L=4,6` |
| Interchange `L->infty` with `int du` and Fourier | TL-5 is uniform in `u` | Written |
| Interchange `sum_y` with limits | Absolute by TL-4 | Written |
| Series coefficients versus analytic functions | Cauchy and Schwarz on uniform polydisks; the `log` branch is the cluster series | Written |
| Integer arithmetic | `int64` products guarded; overflow raises | Exact test |

Floating-point row sums (`L=4,6,8,10`, `theta=1/192`, `u=1/3`) agree to
`1e-11`; they are
diagnostics, not evidence.

## Scope of the preceding estimates

TL-2–TL-7 hold on `0<=theta<=1/192` (TL-5 on `0<=theta<1/128`),
under the imported polymer criterion. TL-9 gives its stated quantitative
bound on `0<theta<=theta_*` and positivity on `0<theta<2theta_*`.
The next section extends strict positivity to `0<theta<=1/192` by an
open-chain argument; it does not require the previously proposed bound on
`sup_u|g-1/2|`. No statement for `theta>1/128`, real-time spectral density,
comparison with `X_LM`, or Lean proof of the analytic estimates is supplied.
`MeronThermoLimitConstants.lean` checks only rational constants.

## Window positivity on `0<theta<=1/192` (added 2026-10-07)

This section extends the strict-positivity range of TL-9. It does not bound
`sup_u|g-1/2|`, and it does not use TL-8. It works on even open chains,
where three exact facts hold, and passes to the limit through TL-3 and TL-4.
Code: `code/meron_thermodynamic_limit/positivity.py`; tests:
`code/tests/test_meron_positivity_window.py`.

**Open-chain kernel.** For the open chain `I` with `n` sites (even), let
`A=sum_{x in I}a_x`, `h_b=c_b^*c_{b+1}+c_{b+1}^*c_b`, and
`k^I(u)=(1/n)Tr rho A(u)A`. With `rho` and `K` diagonal, `p_i` the Gibbs
weights, `E_i` the levels and `Delta_ij=theta(E_j-E_i)`,

\[
 \widehat{k^I}(m)=\sum_{i,j}{w_{ij}\over\Delta_{ij}^2+\omega^2},\qquad
 w_{ij}={1\over n}|A_{ij}|^2(p_i-p_j)\Delta_{ij}\ge0 ,
\]
\[
 \sum w_{ij}=2\theta\bar F^I,\quad \bar F^I={1\over n}\sum_b\langle h_b\rangle;
 \qquad
 \sum w_{ij}\Delta_{ij}^2=\theta^3\bar W^I,\quad
 \bar W^I={1\over n}\sum_x\langle W_x\rangle,\quad W_x=[\mathrm{ad}_K^2a_x,\mathrm{ad}_KA].
 \tag{TL-10}
\]

The first is EP-9's commutator on the open chain, the second the same
computation one order up; `W_x` is Hermitian. Since
`1/(Delta^2+omega^2)>=1/omega^2-Delta^2/omega^4`,

\[
 \omega^2\widehat{k^I}(m)\ge2\theta\bar F^I-\theta^3\max_x\|W_x\|/\omega^2 .
 \tag{TL-11}
\]

**SU(2) on open chains.** With `sigma_x=J_xc_x`, `J_x=prod_{y<x}(I-2n_y)`,
the staggered lowering `G=sum_x(-1)^x sigma_x` commutes with `K` exactly.
Put `Q_b=D_b-P_b`, `D_b=n_b+n_{b+1}-2n_bn_{b+1}`, `T11_b=n_bn_{b+1}`,
`T00_b=(1-n_b)(1-n_{b+1})`, and
`Y_b=2(-1)^b(sigma_b^*n_{b+1}-n_b sigma_{b+1}^*)`,
`Y'_b=Y_b+2(-1)^b(sigma_{b+1}^*-sigma_b^*)`. Then
`[G,Y_b]=4(Q_b-T11_b)` and `[G,Y'_b]=4(Q_b-T00_b)`. Because
`Tr rho[G,Y]=Tr[rho,G]Y=0`, every Gibbs state of an open chain has
`<Q_b>=<T11_b>=<T00_b>`. The four projectors `P_b,Q_b,T00_b,T11_b` sum to
the identity on the bond and `h_b=P_b-Q_b`, so `<h_b>=(4<P_b>-1)/3`.
Exact on chains `n=2,4,6,8`; with the unstaggered `G` the commutator with
`K` is nonzero. (The ring lacks this at finite `L`: floating-point
diagnostics give `<Q>-<T00>` near `1e-6` at `L=4`, `theta=0.05`. That is
why the argument runs on open chains.)

**Bond energy.** Let `n=2N` and `Phi(theta)=log Tr e^{theta sum_b P_b}`, so
`Phi'=sum_b<P_b>`. Each `P_b` is a rank-one projector on its two sites, so
the dimer state `e^{theta sum_j P_{(2j,2j+1)}}` has `Tr=(e^theta+3)^N`, and
its exact expectations are `(1+s)/(4+s)` on dimer bonds and `1/4` on the
`N-1` bonds between dimers (`s=e^theta-1`; checked for three rational `s`).
The Gibbs variational inequality and convexity of `Phi` give
`sum_b<P_b> >= (Phi(theta)-Phi(0))/theta >= (N log((e^theta+3)/4)+(N-1)theta/4)/theta`.
With `<h_b>=(4<P_b>-1)/3`,

\[
 2\theta\bar F^I\ \ge\ {8\over3}\,g(\theta),\qquad
 g(\theta)={1\over2}\log{e^\theta+3\over4}-{\theta\over8}
 \ \ge\ {\theta^2\over64}\Bigl(3-\theta-{\theta^2\over4}\Bigr),
\]

exactly, for every even `n` and every `theta>0`. The last step uses
`e^theta>=1+theta+theta^2/2`, `log(1+y)>=y-y^2/2` and the polynomial identity
checked in the code (`y=theta/4+theta^2/8`; replacing the leading `3` by `4`
fails). Floating point gives `bar F^I` about three times `4g/(3theta)`
on open chains; that slack is not used.

**Second moment.** `W_x` is supported on `[x-4,x+4]` cut to the chain, so on
every even open chain it is one of the cases on chains of `2,4,6,8` sites or
`x<=4` on the 9-site chain, up to reflection (which either preserves the
staggered signs or reverses them all, according to the chain length; in both
cases `W_x` is unchanged). A CAR polynomial's norm does not depend on
the representation. For each case `256W_x` is an integer matrix that
conserves the particle number, and `1408^2 I-(256W_x)^2` is positive
semidefinite on every particle-number block by exact symmetric elimination.
So `||W_x||<=11/2`; with `5` in place of `11/2` the check fails (the
interior value is about `5.0234`).

**Finite volume.** With `omega^2>=4pi^2>39` (from `pi>3.14159`), TL-11 and
the two bounds give, for every even open chain,

\[
 \omega^2\widehat{k^I}(m)\ \ge\ \theta^2\Bigl({3-\theta-\theta^2/4\over24}
 -{11\theta\over78}\Bigr)\ \ge\ {\theta^2\over9}
 \qquad(0<\theta\le1/96).
 \tag{TL-12}
\]

The bracket is decreasing; it is `5706995/46006272` (about `0.1240`) at
`theta=1/192` and `1415795/11501568` (about `0.1231`) at `1/96`, both above
`1/9` (exact; `1/8` fails at `1/192`).

**Limit.** Let `q=96theta<=1/2` and `R_x=dist(x,Z\I)-1`, the largest radius whose symmetric lattice window
about `x` lies in `I`. TL-3 gives `|C^I_{x,x+d}-C^infty_{0d}|<=2M_1q^{R_x+1}` for
`|d|<=R_x`, and both functions are at most `M_1q^{|d|}`. Summing row `x`,
`|sum_y C^I_{xy}-k_theta|<=M_1(4R_x+10)q^{R_x+1}`; each value of `R_x`
occurs at most twice, so

\[
 \sup_u|k^I(u)-k_\theta(u)|\le{2M_1\over n}\sum_{R\ge0}(4R+10)q^{R+1}
 \le{28M_1\over n}.
\]

Hence `widehat{k^I}(m)->widehat k_theta(m)`, the same limit the rings reach
by TL-4 and TL-5, and TL-12 passes to it:

\[
 \widehat k_\theta(m)\ \ge\ {\theta^2\over36\pi^2m^2}>0
 \qquad(m\ne0,\ 0<\theta\le1/192).
\]

This replaces TL-9's `theta^2/(16pi^2m^2)` on `0<theta<=theta_*` by a
constant smaller by `4/9` and extends it to the whole window.

**What this does and does not settle.**

- Proved, with the imported polymer criterion (used only for the limit): strict positivity of
  every nonzero limit mode on `0<theta<=1/192`, and of every nonzero
  open-chain mode for every even `n` on `0<theta<=1/96` (finite volume needs
  no polymer input).
- Not proved, and no longer needed for positivity: an `L`-uniform bound
  `sup_u|g-1/2|<=c theta` with `c` of order one. It stays open as a
  statement about `g`.
- Not proved: the same lower bound on rings at finite `L` (the ring lacks
  exact SU(2); `ring_su2_defect_float` records the defect); anything about
  the limit for `theta>1/192` or about open chains for `theta>1/96`; a Lean
  proof. Floating-point diagnostics (Lehmann sum against quadrature, TL-10's
  two identities below `1e-17`, `||W_x||`) agree and prove nothing.

**Dated note to "Boundary of the theorem" (2026-10-07).** The sentences
"Not proved: strict positivity of a nonzero limit mode on
`2theta_*<=theta<=1/192`" and "The single missing estimate is a lower bound
... uniform in `L`" were true when written and are now superseded by this
section, which needs neither estimate. The rest of that paragraph stands,
including "any statement for `theta>1/128`" as it applies to the ring
lemmas TL-4 and TL-5.
