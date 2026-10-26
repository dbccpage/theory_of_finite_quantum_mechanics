# A common thermodynamic target for the actual finite Meron chain

AuthorityEffect: None. These are written finite-matrix and limit proofs for
the declared periodic spinless U=t chain. They do not derive that Hamiltonian
from the primitive mark, identify a Gross-Neveu model, prove a spatial-mesh
field-theory limit, or formalize these analytic arguments in Lean.

## 1. Bind the actual source and its temperature

The source is `meron_transfer_trace`
at the inspected main checkpoint `199a4d18714263d0b207e8a31ab5b7bb2281feda`. It
sums the full 2^L occupation basis, with an even periodic chain L>=4, M
checkerboard repetitions and rational q>=1. The source's four-time-slice
fixture has L=4, M=2, q=3 and unscaled partition 912. The physical
dimensionless temperature parameter is theta=beta*t=M*log(q). Increasing M
at fixed q changes theta. It is not a fixed-temperature refinement.

On the admitted fermionic Fock carrier, let c_x be the CAR lowering
operators, n_x=c_x^*c_x and y=x+1 modulo L. Define

$$
P_x=\tfrac12(n_x+n_y-2n_xn_y+c_x^*c_y+c_y^*c_x),\qquad
H_L/t=\sum_x(\tfrac14 I-P_x).
$$

On the equal-occupation two-mode sectors P_x is zero. On each mixed sector,
including spectator occupations, it has matrix [[1,s],[s,1]]/2 with s the
CAR hopping sign. Thus P_x is a Hermitian projection, and h_x=I/4-P_x has
norm 3/4. In the source basis, s is minus one precisely when the occupied
modes strictly between the two endpoints have odd parity. This includes the
periodic bond; replacing it by an always-positive hop changes the model.

The source local transfer block is exactly I+(q-1)P_x=exp(log(q)P_x).
Disjoint even CAR polynomials commute: moving the two factors of one even
monomial through a disjoint even monomial gives an even number of sign
changes. Hence all even bonds commute with one another, and so do all odd
bonds. Write A=sum_even P_x, B=sum_odd P_x and G=A+B. Then
0<=G<=L I and ||A||,||B||<=L/2. Only neighboring opposite-parity bonds can
fail to commute, so ||[A,B]||<=2L by the triangle inequality and
||[P_x,P_y]||<=2. These statements hold at every finite even L>=4.

The source returns

$$
Z_{L,M}(q)=\operatorname{Tr}(e^{hB}e^{hA})^M,\quad h=\log q.
$$

It has removed the positive scalar q^(-LM/4). The physical log partition
density is therefore log(Z_{L,M})/L-M*log(q)/4. The target at theta is
ell_L(theta)=log Tr exp(-theta H_L/t)/L. Neither is the conventional free
energy without its additional factor -1/beta. No fixed-number projection
or chemical-potential term is inserted.

## 2. A bound on the actual time slicing

Set S_h=e^(hA/2)e^(hB)e^(hA/2). It is similar to e^(hB)e^(hA), is Hermitian
and satisfies S_h>=I. Thus Z_{L,M}=Tr exp(M log S_h), and Z_{L,M}>=2^L.

For F(s)=e^(sA/2)e^(sB)e^(sA/2), differentiation gives

$$
F'(s)-GF(s)=[e^{sA/2},B]e^{sB}e^{sA/2}+[F(s),A/2].
$$

The integral identity for [e^(sA),B] bounds the right side by
s*||[A,B]||*exp(s(||A||+||B||)). Integrating the defect against
e^((h-s)G) gives ||S_h-e^(hG)||<=h^2*||[A,B]||*exp(hL)/2.

For positive Hermitian S,T>=I, the resolvent integral for log gives
||log S-log T||<=||S-T||: the integrand norm is at most
||S-T||/(1+u)^2, whose integral is ||S-T||. Also K->log Tr exp K is
1-Lipschitz on Hermitian matrices in operator norm. Along a segment its
derivative is Tr(D exp K)/Tr exp K, bounded by ||D||; cyclicity justifies
this derivative even when K and D do not commute. Consequently

$$
\left|\frac{\log Z_{L,M}(q)}L-
\frac{\log\operatorname{Tr}e^{MhG}}L\right|
\le M h^2 q^L. \tag{MT}
$$

This argument uses the logarithm of a positive similar product; it does not
assert that the original checkerboard product itself is Hermitian. Its
growth factor q^L belongs to one time slice, rather than the entire evolution.
The norm defect method is standard product-formula analysis; see
[Childs et al., A Theory of Trotter Error](https://arxiv.org/abs/1912.08854v3).
The constants above are derived here for these declared matrices.

## 3. An entirely rational refinement family

Supply a common target theta in [r-rho,r+rho], with r>=rho>=0. Put
q=1+r/M. The effective source parameter is theta_hat=M log(1+r/M).
Integrating u/(1+u)<=u proves

$$0\le r-\widehat\theta\le r^2/(2M),\qquad
|\widehat\theta-\theta|\le d:=r^2/(2M)+\rho.$$

The unscaled target log Tr exp(theta G)/L has derivative in [0,1]. The
physical density ell_L has derivative in [-1/4,3/4], because every eigenvalue
of H_L/t lies in [-3L/4,L/4]. It is therefore 3/4-Lipschitz. Combining
these bounds with MT and h<=r/M gives rational errors

$$
b_{\rm raw}=\frac{r^2q^L}{M}+d,\qquad
b_{\rm time}=\frac{r^2q^L}{M}+\frac34d. \tag{ME}
$$

Apply the first to the source's unscaled density. Apply the second after
subtracting M log(q)/4. Certified rational logarithm intervals add their
own displayed widths; those widths are not counted as zero.

At the canonical temperature theta=2 log(3), the existing exact logarithm
series supplies rational intervals for theta. Their midpoints r and radii
rho define this family without irrational q inputs. Refining the logarithm
order must refine that same parameter, rather than declare independent
temperatures whose intervals happen to overlap.

## 4. Prove the spatial-volume target instead of assuming a scaling polynomial

Let H_n^o be the open-chain sum of its n-1 bond Hamiltonians, for every
n>=1, and let a_n=log Tr exp(-theta H_n^o/t). Splitting the occupation
carrier into two consecutive blocks identifies all internal even operators
with their tensor-factor operators. Connecting the blocks adds one bond of
norm 3/4. The log-trace Lipschitz inequality therefore gives

$$|a_{n+m}-a_n-a_m|\le c:=3\theta/4.$$

The sequence a_n+c is subadditive and a_n-c is superadditive. Both have
linear upper and lower bounds, since ||H_n^o/t||<=3(n-1)/4 and the carrier
has dimension 2^n. Fekete's argument gives the same finite limit f(theta)
for their densities, as they differ by 2c/n. Its infimum/supremum
characterization gives |a_n/n-f(theta)|<=c/n. Equivalently, dividing the
near-additive inequalities over blocks of a fixed size proves these bounds
directly; real completeness supplies the limit.

The periodic chain differs from the open chain by one more bond, even though
the periodic bond has a Jordan-Wigner string in the occupation writing.
Its norm is still 3/4. Thus

$$|\ell_L(\theta)-f(\theta)|\le\frac{3\theta}{2L}. \tag{MV}$$

This proves a thermodynamic target for this full-Fock U=t chain. It assumes
no quadratic finite-size scaling law and does not justify the existing
three-size Neville interpolation as a target enclosure.

## 5. The common-target enclosure and growing-volume time control

For the parameter interval in Section 3, the corrected finite sample has
error at most

$$
b_{\rm total}=\frac{r^2q^L}{M}
+\frac34\left(\frac{r^2}{2M}+\rho\right)
+\frac{3(r+\rho)}{2L} \tag{MC}
$$

against the single target f(theta). Expanding its rational logarithm
interval by this radius is a sound target enclosure under the declared
model and common-parameter premise.

For bounded r<=R, M>=L gives q^L<=(1+R/M)^M<=exp(R). Therefore MC tends
to zero along even L->infinity, M>=L and rho->0, with logarithm widths also
tending to zero. This is actual joint time/volume control for this query;
it does not assume interchange of arbitrary limits. Independent error
intervals at fixed M, unrelated theta values or a fixed q do not meet it.

The functions ell_L are all 3/4-Lipschitz in theta. Passing to their proven
limits makes f 3/4-Lipschitz too. Its restriction to nonnegative rational
theta therefore extends uniquely to the completion R_>=0 in the admitted
Archimedean metric, as in [PC-1](cs_q_presentation_completion.md). The
direct real-parameter limit and that completion route agree. This closes a
selected scalar observable presentation, not the complete infinite operator
algebra or a spatial-mesh continuum field theory.

## 6. Native and source execution scopes

The mathematical owner is `omega_quantum_physics::meron_time_refinement`.
It builds projectors from the existing exact `FockCarrier`, computes actual
transfer traces and rational ME/MC bounds. WDP only retains the owner's plan
and trace through `meron_time_adapter`, with AuthorityEffect None.

The existing native Fock ceiling admits four-site even chains. It refuses
six sites; no global resource ceiling was silently increased. The bound
object supports bounded even sizes up to 256, time counts up to 256 and
256-bit input rationals. A declared bound object is not a trace evaluation
on a carrier the native owner cannot allocate.

The Python companion calls the unchanged original transfer routine, rather
than the canonical-value cache. It limits source work, time counts, rational
inputs and logarithm order before execution. Finite source traces and the
four-site independent generator-series comparisons have finite scopes.
The universal MT–MC proofs are written; no new Lean credit is asserted for
matrix logarithms, the model Hamiltonian, near-additivity or these limits.

Full sign-character/orbit and observable-numerator identities remain separate
from transfer multiplication. The protected query here is the corrected full
partition log density. Extending susceptibility or another estimator requires
its actual source numerator and its own transport bound. No general fermion
sign solution, sampling complexity improvement, field-theory identification
or operational authorization follows from this selected closure.


The [native owner](../../../../../../omega_engine/crates_rs/omega_quantum_physics/src/meron_time_refinement.rs),
[WDP adapter](../../../../../../omega_engine/crates_rs/omega_wdp/src/meron_time_adapter.rs)
and [source companion](../../../../../../omega_engine_projects/finite_to_continuum/code/meron_time_refinement.py)
have distinct roles. Nineteen Python checks pass, including actual transfer
samples at rational parameters and at enclosures of the canonical temperature,
and independent finite-generator Taylor comparisons. Three native physics
checks pass, covering 1,024 source-bond matrix entries, periodic CAR signs,
the original trace 912 and typed domain/resource refusals. Two WDP adapter
checks pass. These counts refer to this source checkpoint; no earlier suite
is relabeled as freshly replayed.

```sh
py -3.12 -B -m pytest -q -o addopts= -p no:cacheprovider omega_engine_projects/finite_to_continuum/tests/time_refinement/test_meron_time_refinement.py
cargo test --offline --locked -j1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_quantum_physics --test meron_time_refinement
cargo test --offline --locked -j1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_wdp --test meron_time_adapter
```

## 7. Retain the actual spin sectors and numerator

The [spin/observable supplement](meron_spin_and_observable_transport.md)
now derives the odd-periodic/even-twisted spin map and the raw SQL staggered
numerator's transfer identity. Its normalized query has a written Kubo
time limit at fixed volume. A growing-volume correlation bound, spatial
scaling and general Meron sign-character theorem remain separate from this
partition-density limit.
