# WDP-APPM-M4-REMAINDER

Goal id: WDP-APPM-M4-REMAINDER

Selected scope for WDP-APPM-M4-REMAINDER is recorded in this note.

## Selected scope

Labelled finite carrier only: full occupation traces at repetitions=2, q=3, L in {4,6,8}, so Z=(912,33012,973824) on the 2^L Fock space with no particle-number projection and no 2D/3D/4D reuse of 912. Nodes x=1/L^2 in {1/16,1/36,1/64}. The degree-at-most-2 Lagrange projector at x=0 is the three-point extrapolant of g(L)=ln Z(L)/L. The exact rational this carrier determines is the node gap H(0)=-1/36864 together with weights (4/15,-81/35,64/21) and moments (1,0,0). It is not a triple b_i and not a thermodynamic limit.

## Hypotheses

The hypotheses are taken from Appendix M.4 and Appendix O.4, and they are restricted to this carrier.

H1. One common triple (f, c1, c2) and remainders obey g(L_i)=f+c1 x_i+c2 x_i^2+r_i with |r_i|<=b_i.

H2. The verification record supplies the three integers Z and an arithmetic logarithm interval. It does not supply b_i.

H3. For the corrected full-Fock Hamiltonian density, |ell_L(theta)-f(theta)|<=3 theta/(2L). That estimate assumes no quadratic finite-size law.

H4. The fixture theta=2 ln 3 lies outside the disk theta<=1/192.

## Derivation

Appendix M.4 records the occupation-basis checkerboard transfer at repetitions=2 and q=3: Z(4)=912, Z(6)=33012, and Z(8)=973824. The trace sums all 2^L occupation states and does not project to a fixed particle number. Set g(L)=ln(Z(L))/L and x_i=1/L_i^2, so the nodes are 1/16, 1/36, and 1/64. The same appendix says that reading g as a thermodynamic free energy needs a separate temperature, sign, and normalization. The positive quantity ln(Z)/L is a log-partition density until those conventions are fixed. g(L) is not rational. A certified logarithm interval is arithmetic uncertainty, not a model remainder r_i.

The degree-at-most-2 Lagrange weights at x=0 are w_i=prod_{j≠i} x_j/(x_i-x_j).

For L=4, the numerator is (1/36)(1/64)=1/2304 and the denominator is (1/16-1/36)(1/16-1/64)=(5/144)(3/64)=15/9216, so w_4=9216/(2304·15)=4/15.

For L=6, the numerator is (1/16)(1/64)=1/1024 and the denominator is (1/36-1/16)(1/36-1/64)=(-5/144)(7/576)=-35/(144·576), so w_6=-144·576/(1024·35)=-81/35.

For L=8, the numerator is (1/16)(1/36)=1/576 and the denominator is (1/64-1/16)(1/64-1/36)=(-3/64)(-7/576)=21/(64·576), so w_8=64/21.

Thus w=(4/15,-81/35,64/21). On denominator 105, 4/15=28/105, -81/35=-243/105, and 64/21=320/105, so 28/105-243/105+320/105=105/105=1. On denominator 420, sum w_i x_i=7/420-27/420+20/420=0, because (4/15)(1/16)=1/60, (-81/35)(1/36)=-9/140, and (64/21)(1/64)=1/21. On denominator 6720, sum w_i x_i^2=7/6720-12/6720+5/6720=0, because (4/15)(1/256)=1/960, (-81/35)(1/1296)=-1/560, and (64/21)(1/4096)=1/1344. The three moments are (1,0,0). The sum of the absolute weights is 4/15+81/35+64/21=591/105=197/35. That constant is the triangle factor for the unit bounds b_i=1. It is not a Meron remainder.

Under H1 the two correction sums cancel, so fhat-f=sum w_i r_i and |fhat-f|<=B with B=sum |w_i| b_i=(4/15)b_4+(81/35)b_6+(64/21)b_8. Logarithm-interval endpoints expand by the same B. Signed weights also send a rational sample box to a tight rational image; B is a further enlargement of that image, not the image itself. This is a conditional triangle bound. The b_i are external inputs. H2 says the verification record does not provide them.

Three exact samples cannot produce those inputs. Set H(x)=(x-1/16)(x-1/36)(x-1/64). Then H vanishes at the three nodes, and H(0)=(-1/16)(-1/36)(-1/64)=-1/(16·36·64)=-1/36864. The zero function and H share the samples and the degree-at-most-2 interpolant 0, but not the value at 0. For every real t, g and g+t H(x(L)) share the three samples, so the quadratic projector is unchanged, while the value at x=0 moves by -t/36864. Any candidate radius B read off the samples is exceeded by large t, while the samples and the arithmetic width stay fixed. No function of the three samples is a correct uniform triple (b_4,b_6,b_8). A check on this carrier can compare the weights, the three moments, and H(0)=-1/36864. It cannot check a Meron b_i.

Appendix M.4 records an extrapolation near 1.6941183355 with arithmetic width below 10^{-19}, and states that the verification record carries no independently justified scaling remainder. That width encloses only the interpolation of certified logarithms. The continuum-bridge note records the same width and the same absence of a scaling-remainder input. The original extrapolator returns [0,0] on three zero samples, which is the interpolant of both zero and H, not a limit enclosure for H.

H3 does not fill the gap. The time/volume supplement and Appendix O.4 prove |ell_L(theta)-f(theta)|<=3 theta/(2L) for the corrected full-Fock density. The bound covers the whole density error, including every power of 1/L. Both texts say the argument assumes no quadratic finite-size polynomial and does not justify this three-point Neville enclosure. Feeding the unlicensed choice b_i=3 theta/(2 L_i) into the weights would give radius (3 theta/2)(1/15+27/70+8/21)=(3 theta/2)(5/6)=5 theta/4. That is 20/3 times the direct L=8 radius 3 theta/16, and it is still not a remainder after a fitted pair (c1,c2).

The checkerboard time majorant is different again. The supplement bounds the unscaled density against log Tr exp(M h G)/L by M h^2 q^L, with h=ln q. At q=3 and M=2 this is 2 (ln 3)^2 3^L. It grows with L, it is not rational, and it is not a 1/L scaling remainder after a quadratic fit.

H4 blocks the later analytic disk. Appendix O.8 proves a complex-source bound for 0<=theta<=1/192 and states that the q=3, M=2 fixture lies outside that region and receives no analytic certificate. Here theta=M ln q=2 ln 3. Since ln 3>1, this theta is larger than 1/192. The polymer/Cauchy disk, the Kubo jet, and the spatial Gaussian closure are not these b_i.

The Rust Neville recurrence states that neither the recurrence nor the separate Lagrange image supplies a function remainder or an asymptotic limit. The e2e weight check confirms 4/15, -81/35, and 64/21 and their sum 1. Its remainder check multiplies those weights by the caller-chosen fractions 1/100, 1/200, and 1/400 and compares the resulting sum with itself. Those fractions are not proved bounds for these three Meron logarithms. The Wilsonian and Meron-bridge docstrings name a thermodynamic free-energy limit; Appendix M.4 does not treat that naming, or the sub-10^{-19} width, as a model-error proof.

This finite case does not produce b_i binding one (f,c1,c2) to g(L)=ln Z(L)/L at L=4,6,8, q=3, and repetitions=2. It does not establish a continuum limit or a quadratic law for all even L.

## Claims this note does not make

- It does not supply nonnegative b_i for these three traces.
- It does not treat the arithmetic width below 10^{-19} as a scaling remainder.
- It does not treat 197/35, or the toy inputs 1/100, 1/200, and 1/400, as Meron remainders.
- It does not treat agreement on the three nodes as excluding every other scaling polynomial. Multiples of H preserve the samples and move the value at 0.
- It does not import |ell_L(theta)-f(theta)|<=3 theta/(2L) as these b_i or as validation of the quadratic fit.
- It does not import the checkerboard majorant M (ln q)^2 q^L, the disk theta<=1/192, a Kubo correlation, or a spatial Gaussian limit as these b_i.
- It does not read ln(Z)/L as free energy without temperature, sign, and normalization.
- It does not reuse Z=912 as a 2D, 3D, or 4D partition.
- It does not assert the quadratic scaling law for every even L.
- It does not identify a field theory, a Gross-Neveu model, or a spacetime limit.
- A finite model on this carrier does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.
