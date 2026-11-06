# Exact spin-sector transport and the actual Meron observable

AuthorityEffect: None. The carrier, Hamiltonian, boundary condition and query
are the declared full-Fock periodic U=t chain of the
[time/volume derivation](meron_time_and_volume_refinement.md). The spin map and
finite-volume time limit below are written proofs. No spatial scaling limit,
general Meron character theorem or new Lean credit is asserted here.

## 1. Retain the periodic fermion boundary

Number sites x=0,...,L-1 with L even and L>=4. On the occupation tensor basis
define S_x^z=1/2-n_x and the single-site spin raising/lowering matrices, and
write E_xy=S_x^+S_y^-+S_x^-S_y^+. On adjacent interior sites, the CAR hopping
matrix is E_xy. On the periodic bond it is -Pi E_(L-1,0), where
Pi=(-1)^N and N=sum n_x: a nonzero hop has one occupied endpoint, so its
spectator parity is (-1)^(N-1)=-Pi. All these hopping operators preserve Pi.

The source bond Hamiltonian is

$$h_x=S_x^zS_y^z-\tfrac12(c_x^*c_y+c_y^*c_x).$$

Let D=(-1)^(sum_(x odd) n_x), a diagonal real unitary. Every nearest-neighbor
hop changes the odd-sublattice occupation by one, including the closing bond
because L is even. Thus D changes the sign of each hop, leaves n_x and Pi
fixed, and D^2=I. On the Pi=p sector,

$$
D(H_L/t)D=
\sum_{x=0}^{L-2}\boldsymbol S_x\cdot\boldsymbol S_{x+1}
+S_{L-1}^zS_0^z-\tfrac p2 E_{L-1,0}. \tag{SP}
$$

The odd sector p=-1 therefore has periodic antiferromagnetic Heisenberg
coupling. The even sector p=+1 has a pi twist in the closing XY coupling.
Each spin Hamiltonian must be restricted to its matching parity sector.
Taking two unrestricted spin traces doubles the carrier and loses the model.
Replacing both blocks by one unrestricted periodic spin chain changes it too.

Consequently the exact full partition identity is

$$
\operatorname{Tr}e^{-\theta H_L/t}=
\sum_{p=\pm1}\operatorname{Tr}_{\Pi=p}
e^{-\theta H^{\rm spin}_{-p}},
$$

with the twist indicated by the subscript. Spectral functions, states and
operators transport by D conjugation on these actual carriers. Diagonal
occupation observables are unchanged. A parity-changing operator needs its
cross-sector blocks as well; compressing it into one sector loses information.
Number is retained through S_tot^z=L/2-N. Half filling fixes this magnetization
but also fixes parity: $L\equiv 0\pmod 4$ and L=2 modulo 4 use different twists.

The boundary sign is a Jordan-Wigner issue, not an extra numerical convention;
see [Lamacraft's Jordan-Wigner lecture](https://austen.uk/courses/tqm/jordan-wigner/).
The formulas above derive it in this source's occupation and staggered-basis
conventions, rather than copying a boundary assignment from another model.

## 2. What the bulk identification does establish

Let H_per^spin be the unrestricted periodic antiferromagnetic spin chain.
The difference between it and D(H_L/t)D is one operator,
-(Pi+I)E_(L-1,0)/2, of norm at most one. The log-trace Lipschitz inequality
from the time/volume proof gives

$$
\left|\frac1L\log\operatorname{Tr}e^{-\theta H_L/t}
-\frac1L\log\operatorname{Tr}e^{-\theta H^{\rm spin}_{\rm per}}\right|
\le\theta/L.
$$

Therefore both full-carrier models have the same already-proved thermodynamic
log-density target f(theta) at fixed theta. This identifies a standard bulk
model for that query. It does not erase their finite sectors, establish a
correlation limit or identify their low-energy finite-size spectra. In a
scaling where theta grows proportionally to L, this bound does not vanish.

[Itoi's SU(2) WZW analysis](https://arxiv.org/abs/cond-mat/9804075) studies
marginal perturbations and logarithmic corrections for the Heisenberg
antiferromagnetic chain. It is a primary source for a candidate low-energy
profile to audit. Importing that profile here still needs the selected
ensemble, twist/charge sectors, scaling, observable normalizations and a
source-bound convergence argument. A shared bulk free energy is insufficient.

## 3. Identify the SQL observable by expanding the actual transfer

Let A=sum_x (-1)^x(n_x-1/2), and let T_t be the full matching-layer transfer
at time t. There are K=2M half layers. With an insertion before each layer,
put

$$F_{L,M}(\lambda)=\operatorname{Tr}
\prod_{t=K-1}^{0}(T_t e^{\lambda A}).$$

Expanding the trace in occupations gives the signed history weight multiplied
by exp(lambda Q), where Q=sum_t A(state_t). Thus F(0) is the original unscaled
partition, F'(0) its raw first numerator, and F''(0) its raw squared numerator.

The same expansion identifies the original SQL cluster query in its admitted
execution domain. The source constructor allows L=4 or 6 and L*M<=12; the
written identity for its declared local/graph construction holds at every
finite even L and M, independently of that executable ceiling. For one plaquette, the
vertical breakup has weight one and equal occupations on its vertical edges.
The horizontal breakup has weight w=(q-1)/2, opposite occupations on each
horizontal pair, and the CAR sign when a hop occurs. On a mixed diagonal
entry, the two breakups sum to 1+w=(q+1)/2. On a swapped entry, only the
horizontal breakup contributes w times the CAR sign. Equal occupations
permit only the vertical breakup. These are exactly the source local blocks.

Define sigma_(t,x)=(-1)^x(2n_(t,x)-1). It is constant along every vertical
or horizontal graph edge, since horizontal endpoints have opposite site
parities. Compatible occupations therefore correspond bijectively to
one independent sigma=+1 or -1 on each connected component. This is exactly
the SQL orientation-mask construction. The graph weight is w to its horizontal
breakup count. For each matching layer, disjoint interior hops preserve the
number of spectators inside the periodic Jordan-Wigner string; the SQL sign
computed from the before-layer occupations agrees with the multiplication
order. Summing all graph/orientation pairs reproduces every transfer history
with its multiplicity and CAR sign.

For a component C, a_C=|C|/2. Hence

$$Q=\tfrac12\sum_{t,x}\sigma_{t,x}
=\sum_C a_C(-1)^{\mathrm{mask}_C}.$$

This is the `meron_staggered` observable and proves the raw numerator identity
with F''(0). The improved zero/two-meron formula additionally needs the
declared sign-character law. Its finite source comparisons below establish
that law's consequence only in their inspected fixtures; the transfer
expansion does not silently promote a general character theorem.

At the canonical L=4,M=2,q=3 fixture, the unchanged original SQL gives
Z=912 and Q-square numerator 36864. The time-average square is
36864/(4^2*912)=48/19. The equal-time A-square numerator is 2384, with ratio
149/57. These differ by 5/57. The time-integrated query cannot be replaced
by an equal-time readout with the same name.

## 4. The actual finite-volume time-continuum target

For the time-average query use lambda/(2M) in each insertion. Write the
normalized generating trace as F_bar(lambda). Its second derivative is
F''(0)/(2M)^2. For q=1+r/M with a common theta in [r-rho,r+rho], put
theta_hat=M log q and d=r^2/(2M)+rho as in the earlier refinement proof.
At fixed finite L the limiting curve is

$$F_{L,\theta}(\lambda)=\operatorname{Tr}e^{\theta G+\lambda A},$$

or the same curve times exp(-theta L/4) in physical scalar normalization.
That positive scalar cancels from its normalized first and second readouts.
The limiting second readout is the dimensionless Kubo correlation

$$
K_L(\theta)=\frac1{\operatorname{Tr}e^{\theta G}}
\int_0^1\operatorname{Tr}
(e^{(1-s)\theta G}A e^{s\theta G}A)\,ds. \tag{KO}
$$

Differentiating the exponential by Duhamel's formula gives the ordered
two-insertion triangle with factor two; cyclicity and s <-> 1-s symmetry
give the integral displayed above. It is not the equal-time A^2 pairing
unless additional commutation or model information justifies that equality.
The occupation-complement involution commutes with every source projector
at even L and sends A to -A, so the first derivative is zero in both finite
and limiting curves. Accordingly K_L is also the second derivative of log F
at zero. A susceptibility with physical units requires its declared field,
beta and volume factors in addition to this dimensionless query.

The derivative limit needs a proof; uniform real function convergence alone
would not suffice. A finite matrix-jet lift supplies it explicitly. In the
three-by-three block carrier let J_(1,0)=1, J_(2,1)=2 and other entries zero,
let A_hat=J tensor A, and let D_X=diag(X,X,X). A second derivative triple
(V,V',V'') is represented by

$$\begin{pmatrix}V&0&0\\V'&V&0\\V''&2V'&V\end{pmatrix}.$$

Block multiplication gives the noncommuting Leibniz law exactly. The normalized
one-pair step is

$$
Q_M=e^{\widehat\theta D_B/M}e^{\widehat A/(2M)}
e^{\widehat\theta D_{A_e}/M}e^{\widehat A/(2M)},
$$

where A_e is the even-bond projector sum and B the odd-bond sum. The first
name differs from the diagonal observable A. Its M-th power carries precisely
the value and two normalized insertion derivatives. The target lift is
exp(theta D_G+A_hat).

Use the maximum block-row-sum operator norm. It is submultiplicative,
||D_G||<=L and ||A_hat||<=2||A||<=L. Set T=r+rho and S=L(T+1), bounding
the sum of the four generator norms and the target generator norm. Expanding
a one-pair product and its one-step target exponential around the same
linear term bounds their difference by (S/M)^2 exp(S/M): each nonlinear
remainder is at most half that quantity. Telescoping M steps bounds the
effective-parameter lift error by S^2 exp(S)/M. Duhamel's identity for the
theta_hat-to-theta drift contributes at most L*d*exp(S). Thus

$$\delta_L=e^S(S^2/M+Ld)$$

bounds the full lift difference, including its derivative blocks. Trace
differences are at most 2^L delta_L, and both unscaled partitions are at least
2^L. Spectral weighted arithmetic-geometric means give
0<=K_L<=||A||^2<=L^2/4: in an eigenbasis of theta G, bound
e^((1-s)k_i+s k_j) by (1-s)e^(k_i)+s e^(k_j), then sum |A_ij|^2 and integrate.
Consequently

$$
\left|\frac{F''_{L,M}(0)}{(2M)^2 Z_{L,M}}-K_L(\theta)\right|
\le(1+L^2/4)\delta_L. \tag{KT}
$$

For fixed L, bounded r, M tending to infinity and rho tending to zero, KT
vanishes. It proves the actual time-average numerator transport at fixed
volume. Its exponential-in-L bound does not close a growing-volume correlation
limit, supply an efficient sampling algorithm or prove spatial field scaling.

## 5. Native ownership and inspected execution

The exact derivative product belongs to
`linear_algebra::exact_field::second_order_jet`. It checks square compatible
shapes and has a whole-product budget preflight of 12n^3+4n^2+1 scalar calls
and n^2 elements per matrix allocation. These counts exclude scalar-internal
bit complexity; the number of simultaneous matrices is a fixed constant.
The field and its exactness contracts remain premises.

`omega_quantum_physics::meron_time_refinement` owns the actual CAR chain,
staggered unitary, twisted spin matrices, parity blocks and insertion moments.
It retains the four-site Fock ceiling and refuses parity-mixing compression.
The new observable query has its own sixteen-repetition ceiling; the existing
partition/time-plan ceiling stays at 256. WDP requests that owner's observable
for its retained plan and independently compares its partition with the
previously retained partition. No authorization is produced.

The Python block-matrix companion independently computes the occupation
transfer and compares it with the unchanged original SQL graph ensemble.
Thirteen checks include four source fixtures at four and six sites, first
and second numerators, the improved-query comparison and normalization/input
refusals. The native checks include three exact-jet cases, four spin/observable
cases and two WDP cases. Five affected earlier physics/WDP cases are also
replayed separately. These are finite execution scopes; SP, the graph
expansion and KO/KT are written proofs without newly claimed Lean bindings.

```sh
py -3.12 -B -m pytest -q -o addopts= -p no:cacheprovider omega_engine_projects/finite_to_continuum/tests/observable_transport/test_meron_observable_transport.py
cargo test --offline --locked -j1 --manifest-path omega_engine/crates_rs/Cargo.toml -p linear_algebra --test second_order_jet
cargo test --offline --locked -j1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_quantum_physics --test meron_spin_and_observable --test meron_time_refinement
cargo test --offline --locked -j1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_wdp --test meron_observable_adapter --test meron_time_adapter
```

The next missing continuum evidence is a compatible growing-volume/spatial
scaling of these actual correlations, with retained charge/twist sectors and
an identified physical field/readout profile. The presentation-completion
criterion can then be applied to that supplied profile; it cannot manufacture
the convergence hypotheses or erase source-specific observable distinctions.
