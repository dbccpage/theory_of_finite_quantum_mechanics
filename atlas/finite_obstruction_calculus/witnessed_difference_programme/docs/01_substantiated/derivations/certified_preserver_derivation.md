# From certified separation to reversible transformations

This supplement derives the corrected R12 preserver rung and the algebraic
R13 generator rung. Its field, positive Hermitian form, probability readout
and allowed operations are supplied inputs. For dimension at least two the
rational ray space is countably infinite; in dimension one it has one ray.
The preserver classifications below quantify over the whole ray carrier.
Bounded graph pockets are examples of the theorem's hypotheses and boundaries,
not exhaustive checks of that carrier.

**Status: written derivation with separately scoped executable and Lean evidence.**
The central statements are integrated in
[Chapter 19A](../../witnessed_difference_programme.md#chapter-19a). The written
derivations now have a [Python certificate reference](../../code/certified_preservers/),
submitted-witness replay examples, native Rust norm and preserver checkers,
and an [executed notebook](../../jupyter_notebooks/supplements/110_certified_preservers.ipynb).
The registered core-only Lean modules
[CertifiedPreservers](../../lean4/WitnessedDifference/CertifiedPreservers.lean)
[RationalUnitaryReachability](../../lean4/WitnessedDifference/RationalUnitaryReachability.lean)
and [ProjectiveFrameRigidity](../../lean4/WitnessedDifference/ProjectiveFrameRigidity.lean)
formalize separation, rational phases, rank-one projection and constructive
unitary reachability, together with the coordinate-frame uniqueness steps.
They do not formalize the entire preserver
classification or the R13 inner-derivation theorem; the arithmetic parity
corollary retains the two-squares equivalence as an explicit premise.

The [supplement ledger](../../witnessed_difference_programme_claim_ledger.md#preserver-and-generator-supplement-r12r13)
and [evidence guide](../derivation_evidence.md#certified-preservers-and-algebraic-generators)
bind the written, mechanized and executable scopes individually.
Section 10's observation-completion row refers to the existing linear
completion machinery; it is not a newly implemented bicommutant solver.
Full-paper publication readiness is a separate validation claim.

## 1. Inputs, conventions and corrections

Let \(K=\mathbb Q(i)\), with its declared conjugation and
\(N(z)=\bar z z\). Let \(V=K^d\), \(d\ge1\), and let
\[
h(x,y)=x^*Hy,\qquad H=H^*>0.
\]
The form is conjugate-linear in its first argument. In R9, positive
semidefiniteness was already proved from the observer Gram form; trivial radical
then makes it positive definite. Nondegeneracy alone, without that preceding
positivity hypothesis, would not suffice: \(\operatorname{diag}(1,-1)\)
has zero radical and isotropic nonzero vectors.

A ray is \(K^\times f\), \(f\ne0\). Put
\[
r_f=h(f,f)\in\mathbb Q_{>0},\qquad
\tau_f([y])=\frac{N(h(f,y))}{r_f r_y}.
\]
Write \(x\perp y\) for \(h(x,y)=0\). For an operator,
\(A^\dagger=H^{-1}A^*H\); it is ordinary conjugate transpose only in a
standard Gram basis. A semilinear map has the form \(U=M\sigma\), where
\(\sigma\) acts coordinatewise.

The submitted proposal needs the following corrections.

| Proposed claim | Correct statement or rejection |
| --- | --- |
| All unit-norm Gaussian rationals are \(\mu_4\) | The group \(K^1=\{z:N(z)=1\}\) is infinite; only its torsion subgroup is \(\mu_4\). |
| Same ray action forces a unit-norm scalar | The scalar is in \(K^\times\); it has norm one when the two similarity multipliers agree. |
| All separation preservers are R11 unitary processes | They are projective semisimilarities. A similarity can be normalized to a unitary exactly when its multiplier is a Gaussian norm. |
| Root-free Gram–Schmidt gives equal complementary Gram frames | Orthogonalizing two frames does not make their diagonal entries equal. Section 5 gives a direct isometry instead. |
| Lüders conversion gives a complete irreversible-cost classification | A supplied postselected projection has a specified success probability. Other allowed instruments or intermediate projections can change reachability and cost. |
| Informational completeness is equivalent to a residual branch group | Completeness forces the projective pointwise stabilizer to be trivial. The converse fails. |
| The full-probability qubit case is open | Section 7 gives a finite-frame proof over \(K\), including a general positive Hermitian form. |
| Inner derivations give a topology-free Stone theorem | They give \(\delta=-i[H_0,\cdot]\), with \(H_0\) Hermitian, under the stated linearity and dagger law. No time evolution or exponentiation follows. |

## 2. The pure-state table separates rays

**WDP-R12-P01 (finite-dimensional proposition).** The table is well defined
on rays, lies in \(\mathbb Q\cap[0,1]\), and
\[
\tau_f=\tau_g\quad\Longleftrightarrow\quad [f]=[g].
\]
In fact \(d^2\) explicitly specified probe rays suffice.

**Proof.** Rescaling \(f,y\) by \(a,b\ne0\) multiplies both numerator and
denominator by \(N(a)N(b)\). Every term is rational. If
\(\alpha=h(f,y)/r_f\), direct expansion gives
\[
r_f h(y-\alpha f,y-\alpha f)=r_f r_y-N(h(f,y)).
\tag{2.1}
\]
Positivity proves the probability bounds. Equality \(\tau_f([g])=1\)
holds exactly when \(g=\alpha f\). If the two entire tables agree, evaluate
at \([f]\); both give one, so \([f]=[g]\). The converse follows from
representative independence.

For a finite reconstruction use the coordinate vectors \(e_j\) and,
for \(j<k\), \(e_j+e_k\) and \(e_j+i e_k\). All are nonzero. Multiplying
their readouts by their known squared lengths gives evaluations of the
Hermitian quadratic form
\[
q_f(y)=y^{*}A_f y,\qquad A_f=Hff^*H/r_f.
\]
Its diagonal entries come from \(q_f(e_j)\). Its off-diagonal real and
imaginary parts come from
\[
\begin{aligned}
2\operatorname{Re}(A_f)_{jk}
 &=q_f(e_j+e_k)-q_f(e_j)-q_f(e_k),\\
-2\operatorname{Im}(A_f)_{jk}
 &=q_f(e_j+i e_k)-q_f(e_j)-q_f(e_k).
\end{aligned}
\]
Thus the \(d+2\binom d2=d^2\) probes determine \(A_f\). Since \(H\) is
invertible, equality determines \(ff^*/r_f=gg^*/r_g\), whose images are
the original rays. These \(d^2\) probes are a sufficient linear
tomography menu, not a claimed minimal pure-state menu. \(\square\)

## 3. Separation preservers and their exact scope

**WDP-R12-O01 (preserver theorem).** For \(d\ge3\), a bijection \(T\) of
the entire ray space preserves orthogonality in both directions exactly
when it is induced by a semilinear similarity
\[
U=M\sigma,\qquad
M^*HM=c\,\sigma(H),\qquad c\in\mathbb Q_{>0},
\quad \sigma\in\{\mathrm{id},\mathrm{conj}\}.
\tag{3.1}
\]
Such a map preserves the entire probability table. Its branch and its
matrix up to a nonzero scalar are unique.

The general projective semilinearity step belongs to classical algebraic
preserver theory. A related primary reference is Rodman and Šemrl,
*Orthogonality preserving bijective maps on finite dimensional projective
spaces over division rings*, Linear and Multilinear Algebra 56 (2008),
647–664, DOI
[10.1080/03081080701395772](https://doi.org/10.1080/03081080701395772).
The publisher metadata and abstract were checked; the full text was not
audited. REF-PRES-001 is therefore positioning, not a proof import.
The coordinate argument below discharges the requested native written-proof
fallback for a bijection on **all** one-dimensional subspaces of a positive
Hermitian space of vector dimension at least three, preserving orthogonality
in both directions. It supplies no finite-pocket extension theorem,
probability law, unitary normalization over \(K\), or physical authorization.
The proof does not import a complex-continuum Wigner theorem.

**Reduction and proof.** Orthogonality reconstructs
the projective lines:
\[
\mathbb P(\operatorname{span}(x,y))
 =\bigl(\{[x],[y]\}^{\perp}\bigr)^{\perp}.
\]
Nondegeneracy gives the double-perpendicular equality, and bijectivity
allows \(T\) to commute with both perpendicular operations. Thus \(T\)
is a projective collineation. Here is the coordinate proof of the needed
fundamental theorem, so the written result can be read independently
of that import.

A collineation preserves projective spans by iterating lines. It
therefore preserves independence and hyperplanes. Postcompose with a
linear projectivity sending the images of a coordinate basis to that
basis. Each ray \([e_0+e_j]\) then maps to \([e_0+a_j e_j]\) with
\(a_j\ne0\). Postcompose with the diagonal matrix of entries
\(1,a_1^{-1},\ldots,a_{d-1}^{-1}\).
The normalized map fixes every coordinate ray and every
\([e_0+e_j]\).

Its affine chart \([e_0+\sum x_j e_j]\) is \(K^{d-1}\). The hyperplane
at infinity is preserved, so parallel lines and parallel hyperplanes
are preserved. The coordinate hyperplane \(x_j=t\) is spanned by
\([e_0+t e_j]\) and the other coordinate directions at infinity.
Intersecting these hyperplanes shows that the affine action is
\[
(x_1,\ldots,x_{d-1})\longmapsto
(\phi_1(x_1),\ldots,\phi_{d-1}(x_{d-1})),
\]
where each \(\phi_j\) is a bijection fixing 0 and 1. In any two
coordinate directions the diagonal line through 0 and \((1,1)\)
is fixed, so \(\phi_j(t)=\phi_k(t)\) for all \(t\).
Call the common map \(\phi\). The availability of two affine
directions is exactly the condition \(d\ge3\).

The line \(y=x+b\) is parallel to that diagonal and contains
\((0,b)\). Its image is \(y=x+\phi(b)\); evaluating at
\((a,a+b)\) gives \(\phi(a+b)=\phi(a)+\phi(b)\).
The line \(y=ax\) contains 0 and \((1,a)\); its image has slope
\(\phi(a)\). Evaluating at \((b,ab)\) gives
\(\phi(ab)=\phi(a)\phi(b)\). Hence \(\phi\) is a field
automorphism. Points at infinity are the directions of these
affine lines, so their action is also coordinatewise \(\phi\).
Undoing the linear normalizations proves the required \(M\sigma\).

An automorphism of \(K\) fixes its prime field \(\mathbb Q\) and sends
\(i\) to a root of \(X^2+1\). In a field these roots are \(i,-i\).
Hence it is identity or conjugation, and commutes with conjugation.

Let \(h'(x,y)=\sigma^{-1}(h(Ux,Uy))\). The forms \(h,h'\) have exactly
the same zero relation. For fixed \(x\ne0\), their nonzero linear
functionals in \(y\) have the same kernel, so one is a scalar multiple
of the other. For independent \(x,z\), the two original functionals
are independent by nondegeneracy. Applying the identity to \(x+z\)
forces their two scalar multiples to agree. Connecting dependent
vectors through an independent one makes the multiple global.
Conjugate symmetry makes it rational, and positivity makes it positive.
This proves (3.1). Conversely (3.1) directly preserves zero and cancels
the factor \(c^2\) in the normalized probability.

For uniqueness, divide two representatives to obtain a semilinear
map \(F\) fixing every ray. On a basis \(F e_j=a_j e_j\).
Fixing \(e_j+e_k\) forces every \(a_j\) equal to one nonzero \(a\).
Fixing \(e_1+t e_2\) for every \(t\in K\) forces its field
automorphism to fix every \(t\). Thus \(F=aI\) and the branches agree.
This argument needs \(d\ge2\). \(\square\)

Write \(\mathrm{PSim}(h)=\mathrm{Sim}(h)/K^\times\) and
\(\mathrm{P\Gamma Sim}(h)\) for the semilinear group. There is an exact
sequence
\[
1\longrightarrow\mathrm{PSim}(h)\longrightarrow
\mathrm{P\Gamma Sim}(h)\longrightarrow C_2\longrightarrow1.
\]
It splits after choosing an \(h\)-orthogonal \(K\)-basis: its Gram
matrix is positive rational diagonal, so coordinate conjugation in
that basis is an involutive anti-isometry. In an arbitrary basis,
bare coordinate conjugation need not preserve \(h\). Writing a second
\(\rtimes C_2\) after a notation already containing both semilinear
branches would count them twice.

The conjugate branch is related to the scalar involution. It is not
the dagger operation on operators: a field automorphism, an
antilinear state map and an adjoint map have different types.

## 4. Phases, norms and normalization

**WDP-R12-P02 (corrected phase proposition).** If \(U'=aU\), its
multiplier is \(c'=N(a)c\). Equal multipliers leave precisely the
phase group
\[
K^1=\{-1\}\ \cup\
\left\{\frac{1-t^2+2it}{1+t^2}:t\in\mathbb Q\right\}.
\tag{4.1}
\]
The parameter is unique away from \(-1\), with inverse
\(t=\operatorname{Im}(z)/(1+\operatorname{Re}(z))\).
The torsion subgroup of \(K^1\) is \(\mu_4\).

**Proof.** The multiplier law follows by substitution. Squaring the two
coordinates in (4.1) gives one. Conversely \(a^2+b^2=1\), \(a\ne-1\),
and \(t=b/(1+a)\) give the displayed parametrization by elementary
fraction arithmetic. Distinct rational parameters give distinct
phases, so the group is infinite.

For the torsion assertion, if \(z^n=1\), then \(s=z+z^{-1}=2a\)
is a rational algebraic integer: the recurrence
\(P_0=2,P_1=X,P_{k+1}=XP_k-P_{k-1}\) gives the monic relation
\(P_n(s)=2\). The rational-root argument gives \(s\in\mathbb Z\).
Since \(|a|\le1\), \(s\in\{-2,-1,0,1,2\}\). The cases
\(a=\pm1/2\) require \(b^2=3/4\), impossible for rational \(b\).
The other cases give \(1,-1,i,-i\). \(\square\)

In particular \(z=(3+4i)/5\) refutes the original phase claim. Clearing
denominators produces \(m^2+n^2=q^2\), not \(m^2+n^2=4\).
The paper's existing rational-phase boundary already proves this
specific phase has infinite order and lacks a rational half-step.

A projective representation with chosen **unitary** lifts has cocycle
values in \(K^1\); they need not lie in \(\mu_4\). For \(C_2\) acting by
the swap ray map, choose \(U_s=zX\), \(U_1=I\). Then
\(U_s^2=z^2I\), and \(z^2=(-7+24i)/25\notin\mu_4\).
Arbitrary similarity lifts instead have scalars in \(K^\times\).
The Gaussian-integer theorem in Chapter 18 still has exactly four
unit phases because its scalar ring is \(\mathbb Z[i]\).
Chapter 5's cubic root \(\omega\) requires its declared cyclotomic
extension; it cannot be identified with a Gaussian-rational phase.

**WDP-R12-P03 (norm realization).** For \(r>0\) rational,
\[
r=N(z),\ z\in K^\times
\quad\Longleftrightarrow\quad
v_p(r)\text{ is even for every prime }p\equiv3\pmod4.
\tag{4.2}
\]
Consequently
\[
\mathbb Q_{>0}/N(K^\times)
 \simeq\bigoplus_{p\equiv3\ (4)}\mathbb Z/2,
\qquad r\longmapsto (v_p(r)\bmod2)_p.
\tag{4.3}
\]
Negative valuations are included; each vector has finite support.

**Proof.** Write \(r=m/n\) in lowest terms. If \(r=a^2+b^2\) with
rational \(a,b\), clear a common denominator. For \(p\equiv3\pmod4\),
\(p\mid A^2+B^2\) implies \(p\mid A,B\): otherwise \(-1\) would be a
square modulo \(p\). Removing common powers shows that the valuation
of a sum of two integer squares is even. Subtracting the even
denominator valuation proves necessity.

For sufficiency use the integer two-squares theorem
[REF-NORM-001, Theorems 9.6 and 9.10](../references.md#ref-norm-001--gaussian-integers-and-two-squares):
2 is the norm
of \(1+i\), a prime \(p\equiv1\pmod4\) is a Gaussian norm, and an even
power of a \(3\bmod4\) prime is a square. Multiplication of Gaussian
integers combines these witnesses into \(z_m,z_n\) with norms \(m,n\).
Then \(z_m/z_n\) has norm \(r\). The integer theorem follows from the
Euclidean algorithm in \(\mathbb Z[i]\): a square root \(t\) of
\(-1\bmod p\) exists for \(p\equiv1\pmod4\), and
\(\gcd(p,t+i)\) has norm \(p\). These are standard number-theoretic
inputs, not a new WDP prime theorem. The parity homomorphism has this
kernel and hits every finite parity vector by multiplying its
corresponding primes, which proves (4.3). \(\square\)

A terminating, unbounded arithmetic procedure factors the numerator
and denominator by trial division, tests these parities, then finds
the required integer pairs by finite square search. A practical
bounded implementation returns exhaustion separately from an odd-prime
obstruction. A positive certificate is the two rational coordinates;
a negative one identifies a verified prime and its odd valuation.

For the proposed gate,
\[
B=\frac{1+i}{2}
\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\qquad B^*B=I,\qquad B^2=iI.
\tag{4.4}
\]
This implements the usual Hadamard **ray action** within \(K\), even
though its conventional real \(1/\sqrt2\) matrix is not over \(K\).
There is no Gaussian scalar of norm \(1/3\). Moreover the Fourier
matrix of order three also needs a primitive cubic root unavailable
in \(K\). These are two separate scalar obstructions. Formula (4.4)
does not supply the conventional \(T\) ray action, whose nontrivial
eigenvalue ratio is outside \(K\).

## 5. Unitary reachability and the similarity boundary

**WDP-R12-O02 (complete unitary ray criterion).** For nonzero \(f,g\),
there is an \(h\)-unitary \(U\) with \([Uf]=[g]\) if and only if
\[
r_f/r_g\in N(K^\times).
\tag{5.1}
\]
Allowing antiunitaries does not enlarge these orbits. The ambient
obstruction group is (4.3); a particular form realizes the norm
classes of its own nonzero vectors.

**Proof and construction.** Necessity follows from \(Uf=a g\):
\(r_f=N(a)r_g\). The same equation holds for an antiunitary because
\(\sigma\) fixes rational diagonal values.

Conversely, exhibit \(a\) with \(N(a)=r_f/r_g\), and put \(v=ag\).
Then \(r_v=r_f=r\). If \(v=f\), choose \(U=I\). Otherwise let
\[
w=f-v,\quad \beta=h(w,f),\qquad
Ux=x-w\,h(w,x)/\beta.
\tag{5.2}
\]
Here \(h(w,w)=\beta+\bar\beta\). If \(\beta=0\), positivity forces
\(w=0\), contrary to the case assumption. Thus every coefficient
in (5.2) lies in \(K\), and \(Uf=v\). Expanding \(h(Ux,Uy)\), the
coefficient of \(h(x,w)h(w,y)\) is
\[
-1/\beta-1/\bar\beta+
(\beta+\bar\beta)/(\bar\beta\beta)=0.
\]
Hence \(U\) is an isometry. It is injective, and finite dimension
makes it invertible. This is a constructed equal-length extension;
no square root or unproved equality of complementary frames is used.
\(\square\)

**Similarity normalization.** A similarity with multiplier \(c\)
can be multiplied by a scalar to become unitary exactly when
\(c\in N(K^\times)\). Taking determinants in (3.1) for the identity
branch gives
\[
N(\det M)=c^d.
\]
The same conclusion holds for the conjugate branch since
\(\det H\in\mathbb Q_{>0}\). For odd \(d\), the parity group (4.3)
therefore forces \(c\) to be a norm. In even dimension this fails.
For the standard form in dimension four, the rational matrix
\[
M=\begin{pmatrix}
1&-1&-1&0\\
1&1&0&1\\
1&0&1&-1\\
0&-1&1&1
\end{pmatrix}
\quad\text{satisfies}\quad M^*M=3I.
\tag{5.3}
\]
It preserves all ray probabilities, sends \(e_1\) to \((1,1,1,0)\),
and cannot be normalized over \(K\), since \(v_3(3)\) is odd.
These two rays occupy different unitary norm classes. Thus R12's linear
similarity branch and R11's one-factor unitary processes agree projectively
in odd dimension, but not in every even dimension. The conjugate branch
normalizes to an antiunitary in odd dimension and remains a distinct branch.

For all ray similarities, the orbit obstruction is the unitary
norm class modulo the multiplier subgroup actually realized by
\(\mathrm{Sim}(h)\). Equivalently, \([f]\) reaches \([g]\) precisely
when \(r_f/r_g\in N(K^\times)\Gamma(h)\), where
\(\Gamma(h)=\{c:\exists M,\ M^*HM=cH\}\).
To prove sufficiency write \(r_f/r_g=n\gamma\), where
\(n\in N(K^\times)\) and \(\gamma\in\Gamma(h)\). Apply a similarity
of multiplier \(\gamma^{-1}\) to \(f\), then apply (5.1).
Anti-isometries do not change norms.
No independent classification of \(\Gamma(h)\) for arbitrary forms
is silently asserted.

## 6. Exact postselection and what its probability means

**WDP-R12-P04 (Lüders branch).** The submitted operator
\[
\Pi_g=\frac{g\,g^*H}{r_g}
\]
is an \(h\)-selfadjoint idempotent. The two factors
\(\Pi_g,I-\Pi_g\) resolve the identity under \(h\)-adjoint.
For input \(f\ne0\), the first branch has probability
\[
\frac{h(\Pi_g f,\Pi_g f)}{r_f}=\tau_f([g]).
\tag{6.1}
\]
Its conditional ray is \([g]\) exactly when that probability is
positive. At zero probability its vector is zero; no conditional
state exists.

**Proof.** The scalar \(g^*Hg=r_g\) proves idempotence by direct
multiplication. The adjoint definition proves selfadjointness, and
orthogonality of the two projections proves completeness. Finally,
\(\Pi_g f=g\,h(g,f)/r_g\); taking its squared length proves (6.1).
\(\square\)

For a declared policy that first seeks a unitary certificate and,
if none exists, tries this one projection, the three reports are:
unitary witness; positive-probability postselection witness; or a
zero-probability refusal of that branch. If a score is explicitly
defined as failure probability, the first two scores are \(0\) and
\(1-\tau\). They are not operation costs or an optimal-control
theorem.

For \(f=e_1,g=(1,1,1)\), the unitary obstruction is prime 3 and the
direct postselection succeeds with probability \(1/3\). For
\(f=e_1,g=e_2\), direct postselection has zero probability but a
unitary swap succeeds. Even when both obstructions occur, other
postselections can help: in dimension four set
\(g=(0,1,1,1)\), \(a=f+g\). The sequence projecting first to
\([a]\), then to \([g]\), succeeds with probability
\((1/4)(3/4)=3/16\), despite \(\tau_f([g])=0\) and a nonzero
unitary norm obstruction. The allowed operation menu is essential.

## 7. Both dimension-two boundaries

**CM-W1 (orthogonality does not suffice).** In the standard two-dimensional
space each ray has exactly one orthogonal ray. Define a permutation on
six rays by swapping the axes, exchanging the pair
\(\{[1,1],[1,-1]\}\) with
\(\{[1,2],[2,-1]\}\) in the displayed order in both directions,
and fixing every other ray. The six-ray set is closed under
orthogonal complement, so this extends to an orthogonality-preserving
bijection of the entire rational ray space.

It is not a semisimilarity. A semisimilarity swapping the two
coordinate axes has columns on those axes with equal squared
length. Its image of \([1,1]\) therefore has equal-modulus
coordinates, whereas \([1,2]\) does not. Its probabilities also
change: \(1/2=\tau_{e_1}([1,1])\), but
\(\tau_{e_2}([1,2])=4/5\). Merely mapping the first pair to the
second while fixing the second pair would not be a bijection.

**WDP-R12-P05 (full-probability qubit theorem).** For \(d=2\), every
bijection preserving the entire transition-probability table is
induced by a unique projective semisimilarity with branch identity
or conjugation. Thus the proposed conjecture is settled by the
following elementary argument.

Choose an \(h\)-orthogonal \(K\)-basis \(e_1,e_2\) with squared
lengths \(r_1,r_2>0\), using root-free orthogonalization. Represent
their image rays by \(u,v\). They are orthogonal. Write a
representative of \(T[e_1+e_2]\) as \(\alpha u+\beta v\).
Both coefficients are nonzero since its transition probabilities
with the axes are strictly between zero and one.
Probability preservation gives
\[
\frac{N(\alpha)r_u}{N(\alpha)r_u+N(\beta)r_v}
 =\frac{r_1}{r_1+r_2}.
\]
Replace \(v\) by \((\beta/\alpha)v\). Then the map \(M\) with
columns \(u,v\) satisfies \(M^*HM=cH\) in these coordinates,
\(c=r_u/r_1\), and sends the plus ray correctly.

Compose \(T\) with \(M^{-1}\). It now fixes the two axes and the
plus ray. The image of \([e_1+i e_2]\) can be written
\([e_1+z e_2]\). Its axis probabilities force \(N(z)=1\), and its
plus-ray probability forces \(\operatorname{Re}z=0\); hence
\(z=i\) or \(-i\). Compose with coordinate conjugation if needed.

The resulting map fixes four reference rays. For every
\([e_1+t e_2]\), its probabilities against those four rays determine
successively \(N(t)\), \(\operatorname{Re}t\) and
\(\operatorname{Im}t\). Thus it fixes every ray, including the
remaining coordinate axis. This supplies the representative and
branch. Uniqueness is the frame argument of Section 3. \(\square\)

## 8. Observation stabilizers, bicommutants and sharp counts

Let \(X=\mathbb P(V)\), and let \(\mathcal F\) be a declared set of
rational readout functions on \(X\). Let \(\mathcal G\) be the
declared group of projective semisimilarities acting on \(X\).
For \(E\subseteq\mathcal F\) and \(G\subseteq\mathcal G\), define
\[
G_E=\{u:\forall e\in E,\ e\circ u=e\},\qquad
\operatorname{Fix}(G)=\{e:\forall u\in G,\ e\circ u=e\}.
\]

**WDP-R12-O03(a) (Galois connection).**
\[
E\subseteq\operatorname{Fix}(G)\quad\Longleftrightarrow\quad
G\subseteq G_E.
\tag{8.1}
\]
Both maps reverse inclusion. The two composites are extensive,
monotone and idempotent. **Proof:** expand the same quantified
equation \(e(ux)=e(x)\); the closure laws follow from that
equivalence. This assertion is about pointwise preservation of
the named readouts, not permutations of an unlabelled menu.

For an operator algebra \(A\subseteq\operatorname{End}_K(V)\), write
\(A'=\{B:Ba=aB\text{ for every }a\in A\}\).
In the next assertion, \(A\) is a unital
\(K\)-subalgebra closed under \(h\)-adjoint.

**WDP-R12-O03(b) (finite algebraic bicommutant).**
\[
A''=A,\qquad
\operatorname{Fix}_{\operatorname{End}_K(V)}
   \bigl(\text{conjugation by }U(A')\bigr)=A.
\tag{8.2}
\]
On Hermitian operators the fixed set is \(A\cap\{B:B^\dagger=B\}\),
not the entire complex algebra.

**Proof without topological closure.** An \(A\)-invariant subspace
has an \(A\)-invariant orthogonal complement because \(A\) is
dagger-closed. Its orthogonal projection has coefficients in \(K\):
for a basis matrix \(F\), it is
\(F(F^*HF)^{-1}F^*H\). The Gram inverse exists by positivity.

For \(B\in A''\), amplify the representation diagonally to \(V^d\)
with the direct-sum form. Let
\(v=(e_1,\ldots,e_d)\) and
\(W=\{(ae_1,\ldots,ae_d):a\in A\}\).
The subspace \(W\) and its orthogonal complement are invariant under
diagonal \(A\); its projection \(P=(P_{jk})\) therefore commutes
with diagonal \(A\), so \(P_{jk}\in A'\). Diagonal \(B\) commutes
with \(P\). Since \(I\in A\), \(v\in W\); hence
\((Be_1,\ldots,Be_d)\in W\), so \(B\) equals one member of \(A\).
This proves \(A''=A\).

For any finite dagger-closed algebra \(D\), its unitary commutant
equals \(D'\). Indeed, a Hermitian \(a\in D\) has the rational
Cayley unitary
\[
C=(I+ia)(I-ia)^{-1}\in D.
\]
The inverse exists: \((I-ia)x=0\) would imply
\(0=h(x,x)+h(ax,ax)\). Its membership in \(D\) follows from
Cayley–Hamilton, or solving the polynomial inverse. Since
\(C+I=2(I-ia)^{-1}\), an operator commuting with \(C\) also
commutes with \(a=(C-I)(i(C+I))^{-1}\).
Every member of \(D\) is \(a+ib\) with \(a,b\) Hermitian.
Thus commuting with all its unitaries is equivalent to commuting
with \(D\). Apply this to \(D=A'\) and the first equality. \(\square\)

**Information completeness is stronger than a trivial stabilizer.**
For \(d\ge2\), if the menu separates rays, every member of \(G_E\) fixes every ray;
projective uniqueness makes \(G_E=\{1\}\). Conjugation is not a
universal residual symmetry: an imaginary cross-term probe detects
it. Conversely a trivial stabilizer need not make the menu injective.

The dimension hypothesis matters when the group retains semilinear
representatives modulo scalar. In dimension one, identity and conjugation
are distinct projective semilinear classes but act identically on the
single ray. Every menu separates that singleton, while both classes remain
in its stabilizer. Passing instead to the faithful image in the ray
permutation group removes this kernel. The Galois connection itself needs
no faithfulness hypothesis, and the bicommutant law also holds in dimension one.

Here is an exact three-dimensional counterexample for the standard
form. Take the two effects
\[
D=\operatorname{diag}(0,1/2,1),\quad
B=\tfrac12I+\tfrac1{10}
\begin{pmatrix}0&1&i\\1&0&1\\-i&1&0\end{pmatrix}.
\tag{8.3}
\]
The off-diagonal row-sum bound gives \(0<B<I\).
The rays \(f=(1,0,1)\), \(g=(1,0,-1)\) both report \(1/2\) for
both effects, so the menu is not even pure-state complete.

Nevertheless its projective semisimilarity stabilizer is trivial.
Equality of all expectation values for a Hermitian operator implies
operator equality by the finite polarization argument of Section 2.
Fixing \(D\), which has three distinct rational eigenvalues, forces
a semilinear representative to have diagonal matrix. In the identity
branch, fixing the three nonzero off-diagonal entries of \(B\)
forces its diagonal scalars equal. In the conjugate branch the
real 12 and 23 entries again force equality, while the imaginary
13 entry forces their ratio to be \(-1\), a contradiction.
Thus no nonidentity projective representative fixes both readouts.

**WDP-R12-O03(c) (typed completion count).** Let \(R\) be an explicitly
declared finite rational **linear** space of Hermitian trace-zero
state defects, and let
\[
Q_E(D)=(\operatorname{tr}(eD))_{e\in E}.
\]
With arbitrary additional rational linear observations, the minimum
number needed to make the combined report injective on \(R\) is
\[
k=\dim_{\mathbb Q}(R\cap\ker Q_E).
\tag{8.4}
\]
**Proof:** each additional row lowers the residual kernel dimension
by at most one. Conversely choose a basis of the residual kernel,
take its dual functionals, and extend them to the ambient rational
space. Their joint restriction is injective on that kernel.
This is the injectivity instance of Appendix T's linear completion
argument. Quotient detection, recovery of an original carrier, and
restricted menus retain their separate Appendix T hypotheses.

For the standard form \(H=I\), the constructed rows on Hermitian
state defects may also be realized as positive effects. The trace pairing on Hermitian matrices is
nondegenerate over \(\mathbb Q\); represent a row by a Hermitian
matrix \(A\). Choose a positive rational bound \(c\) larger than
every row sum of \(|\operatorname{Re}A_{jk}|+
|\operatorname{Im}A_{jk}|\). Then
\(E=(I+A/c)/2\) satisfies \(0<E<I\), and on trace-zero defects
\(\operatorname{tr}(ED)=\operatorname{tr}(AD)/(2c)\).
Thus the scaled rows retain the matching count if arbitrary such
effects are allowed. A supplied instrument shelf or its costs need
a separate realization and optimization argument.

For transformation defects one must first declare a rational linear
carrier and its linear observations, for example differences of
the induced linear maps on Hermitian matrices. A nonlinear set of
unitaries, branches or pure-state differences does not automatically
inherit (8.4). Applying the count to its declared linear span gives
that span's count, not a proof of minimality on the nonlinear set.

## 9. R13: inner generators with the correct adjoint law

**WDP-R13-P01 (algebraic generator theorem).** Let
\(\delta:M_d(K)\to M_d(K)\) be \(K\)-linear and satisfy the Leibniz
law. There is \(S\in M_d(K)\) with \(\delta(A)=[S,A]\). If also
\(\delta(A^\dagger)=\delta(A)^\dagger\), then one may choose
\(S^\dagger=-S\). Equivalently,
\[
\delta(A)=-i[H_0,A],\qquad H_0^\dagger=H_0,
\tag{9.1}
\]
where \(H_0\) is unique modulo a rational scalar matrix.

**Constructive proof.** In any coordinate basis, with matrix units
\(E_{jk}\), set
\[
S=\sum_j\delta(E_{j1})E_{1j}.
\tag{9.2}
\]
The identity \(E_{kl}E_{j1}=\delta_{lj}E_{k1}\), differentiated and
multiplied on the right by \(E_{1j}\), gives
\[
E_{kl}S=\delta(E_{k1})E_{1l}-\delta(E_{kl}).
\]
Also \(SE_{kl}=\delta(E_{k1})E_{1l}\), so
\([S,E_{kl}]=\delta(E_{kl})\). Linearity extends this to every
matrix. Two such generators differ by an operator commuting with
every matrix unit; it is a scalar matrix.

The dagger law implies \([S+S^\dagger,A]=0\) for every \(A\).
Thus \(S+S^\dagger=tI\); selfadjointness makes \(t\in\mathbb Q\).
Replace \(S\) by \(S-tI/2=(S-S^\dagger)/2\), preserving its
commutator and making it skew-adjoint. Set \(H_0=iS\) to obtain
(9.1). The difference of two Hermitian generators is a real
element of \(K\), hence rational, times \(I\). \(\square\)

This is the inner-derivation theorem with an explicit matrix-unit
certificate. Skolem–Noether concerns algebra automorphisms, and
Stone's theorem needs a topological one-parameter group; neither
name turns (9.1) into a supplied dynamics. A certificate for the
finite table \(\delta(E_{jk})\) checks linear extension, every
matrix-unit Leibniz identity, the dagger law and (9.2).
No matrix exponential, time parameter or physical Hamiltonian is
selected. The existing rational-phase half-step obstruction remains.

## 10. Certificates, verification and consolidation

| Certificate | Independently checked data | Scope |
| --- | --- | --- |
| Hermitian carrier | Exact \(H\), invertibility/positive Gram evidence, dimension | Admits the specified form, not an inferred physical carrier |
| Preserver | Branch, exact \(M,c\), complete identity \(M^*HM=c\sigma(H)\) | Certifies the induced global map; sampled action agreement cannot certify an unrelated black-box map |
| Reachability | Original \(H,f,g\), scalar \(a\), matrix \(U\) and \(Uf=ag\) | Replays that original source/target pair and unitary law |
| Norm obstruction | Positive rational input, prime, primality evidence and exact odd valuation | Refuses only the named norm/unitary obligation |
| Lüders branch | Original \(H,f,g\), submitted projection, probability and branch vector | Zero branch is retained as zero, never normalized |
| Generator | Exact matrix-unit table and submitted \(S,H_0\) | Full finite basis obligations, without an invented flow |
| Observation completion | Declared rational defect carrier, menu rows, added rows and lower-bound kernel basis | Linear recovery count with the actual operation menu stated separately |

All certificate bindings include the original problem and coefficients;
a checker replays the submitted witness. Malformed data, a false witness,
a true norm obstruction and budget exhaustion are different results.
Authorization is independently supplied.

R12 strengthens R2/R3 with an injective pure-state table; uses the scalar
involution and declared orientation from R8/R9; takes the R10 probability
rule as input; and identifies the arithmetic gap between R11 unitary
processes and the whole projective preserver group. It corrects rather
than absorbs Chapter 5's cyclotomic phases into \(\mu_4\), and retains
Chapter 18's Gaussian-integer restriction. Its Galois statement and
Appendix T application keep their types and hypotheses explicit.

There is no derivation of the Born rule, no selected branch, no universal
gate set, no topology, no continuum phase group, no physical measurement
model and no granted authority in these results. R13 adds an algebraic
generator classification and preserves all those boundaries.
