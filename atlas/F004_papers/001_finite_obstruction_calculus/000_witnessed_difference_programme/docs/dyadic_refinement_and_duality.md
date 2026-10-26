# Dyadic refinement, character duals and the declared circle completion

AuthorityEffect: None. Reviewed 2026-10-03. This supplement advances
GEN-WDP-O03/O04 for a supplied cyclic tower. It does not choose that tower,
a topology or a physical continuum from the primitive mark.

The actual source is
`coda_inductive_presentation.py` at the PR 407 merge.
The [original-function oracle](../evidence/dyadic_source_oracle.json) binds
its bytes and those of `interval_calculus.py`. The following classification
is derived from its declared maps; the source does not construct these limits.
Background character terminology and the conventional circle/integer duals
are described by [Elkies](https://abel.math.harvard.edu/~elkies/M55b.02/pontrjagin.html).
[Conrad's finite character notes](https://kconrad.math.uconn.edu/blurbs/grouptheory/charthy.pdf)
provide the finite-group background. A named finite generator is part of
the presentation: its character-index parametrization uses that choice.

## 1. The algebraic direct limit

Write C_n=Z/(2^n) and i_n(k)=2k in C_(n+1), including C_0={0}.
Addition is preserved since 2(a+b) modulo 2N equals twice the residue
of a+b modulo N. The map is injective: two doubled residues agree
modulo 2N exactly when the original residues agree modulo N.

Map C_n to D=Z[1/2]/Z by k -> k/2^n modulo integers. Inclusion leaves
this coordinate unchanged. Every element of D has such a representative.
Two representatives have equal coordinates exactly when their images
at a common later level agree: use the denominator 2^max(n,m) and reduce
both numerators modulo it. Thus the algebraic direct limit is D, the
Prüfer 2-group, and not the full circle carrier.

This also proves the universal property. For compatible homomorphisms
f_n:C_n -> H, set f(k/2^n)=f_n(k). The common-level criterion makes this
well-defined; moving two summands to one level proves additivity.
Every coordinate comes from a level, so f is the unique such map.
No topology is required by this algebraic statement.

## 2. Exact finite pairing and restriction

After supplying complex roots, put
chi_(n,a)(k)=exp(2 pi i a k/2^n). Multiplication adds a modulo 2^n;
conjugation negates it. Pullback along i_n sends the higher index A to
A modulo 2^n, since A(2k)/2^(n+1)=Ak/2^n modulo integers.
Successive restrictions commute because reduction modulo a smaller
dividing order absorbs reduction modulo the larger order.

For N=2^n, the normalized inner product is

$$
\frac1N\sum_{k=0}^{N-1}\chi_a(k)\overline{\chi_b(k)}
=\begin{cases}1&a=b\pmod N,\\0&a\ne b\pmod N.\end{cases}
$$

If the difference is zero every term is one. Otherwise the ratio r is
an N-th root with r≠1; multiplying the geometric sum by 1-r gives
1-r^N=0, hence the sum is zero in the supplied complex field.
This written all-N proof is separate from the native finite evaluation.

The native `omega_number_theory::dyadic_presentation` implementation
actually adds N roots in the existing exact cyclotomic owner and divides
by N. It does not return a delta selected by comparing indices.
Caller term/conductor limits are checked before field-context construction;
the owner's conductor cap is 1024. Those limits do not bound arbitrary
BigInt bit complexity or count the cyclotomic cache as summation terms.
Level metadata additionally has the explicit native word-size bound.
WDP delegates arithmetic and retains the declared prefix and computed value.

## 3. The discrete topology gives a 2-adic dual

Equip D with the discrete topology. Every homomorphism D -> U(1) is
continuous. Its restriction to C_n is determined by an index a_n modulo
2^n, and compatibility is precisely a_(n+1) mod 2^n=a_n.
Conversely a compatible family defines a character at k/2^n by the
finite formula above; common-level equality proves independence of the
representative. These constructions are inverse group homomorphisms.

The compatible index families, with coordinatewise operations, are the
inverse limit Z_2 of the rings Z/(2^n), used here as an additive group.
The dual's compact-open topology agrees with its inverse-limit topology:
compact subsets of discrete D are finite; each such set lies in one
C_n; and each finite-stage restriction is determined by evaluation at
its generator. Each coordinate has a finite image of roots of unity,
so these conditions give exactly the same neighborhood basis.
The inverse limit is compact, being a closed subset of the product of
finite compact spaces, and its distinct points are separated by clopen
coordinate fibers. It is not the connected circle.

At every finite stage a_n has exactly two next-stage extensions,
a_n and a_n+2^n. Both lie below 2^(n+1), both reduce to a_n, and they
are distinct. Conversely a residue below 2^(n+1) is below 2^n or differs
from one below it by 2^n, so there are no other extensions.
Choosing either extension and then keeping that integer at later levels
already gives two different infinite compatible families. A finite
prefix cannot choose a unique infinite character.

## 4. The circle-subspace topology gives a different completion

Instead embed D in T=R/Z with its quotient metric
d(x,y)=min_(z in Z)|x-y-z| and give D the subspace topology.
For every x in [0,1), a dyadic grid point floor(2^n x)/2^n lies within
2^-n of x. Hence D is dense in the declared complete metric group T;
its metric completion is T by the universal property of completion.
The real carrier, metric and completeness are premises of this result.

A continuous homomorphism D -> T is uniformly continuous, since the
metrics are translation invariant and continuity at zero controls all
differences. It therefore extends uniquely to the completion T: use
limits of images of approximating dyadic sequences; uniform continuity
proves independence of the sequence and preservation of addition.

Every continuous character of T is x -> exp(2 pi i jx), j in Z.
For completeness, pull it back to R. Near zero its values lie in a small
circle arc and have a continuous real argument g with g(0)=0.
For sufficiently small s,t,s+t the difference g(s+t)-g(s)-g(t) is
integer-valued and continuous on a connected neighborhood of (0,0).
It is zero there, so g is locally additive. Continuity and rational
approximation make g(t)=alpha t locally; subdividing t and using the
homomorphism law gives the same formula on all R. Periodicity at one
forces alpha to be an integer. Uniqueness follows by evaluation on R.
Thus the continuous characters of subspace D are exactly the integer
families a_n=j modulo 2^n. The arbitrary 2-adic families from section 3
need not be continuous for this topology.

This dense proper subgroup is not locally compact, so no general locally
compact Pontryagin reflexivity theorem is being applied to subspace D.
The extension argument above proves the stated character classification.
In particular, algebraic refinement alone chooses neither topology.

## 5. A conditional Haar limit with an explicit error

Under the already supplied circle and its normalized length measure,
let F be continuous and periodic of period one. The finite uniform
average A_N=(1/N) sum F(k/N) converges to the circle integral as
N=2^n tends to infinity. If omega_F(delta) bounds |F(x)-F(y)| for
|x-y|≤delta, integrate on each cell [k/N,(k+1)/N] to obtain

$$
\left|A_N-\int_0^1F(x)\,dx\right|\le\omega_F(1/N).
$$

Uniform continuity on the compact circle gives convergence. For an
L-Lipschitz F the sharper integral of L(x-k/N) on each cell gives
L/(2N). This is a written conditional sampling bound. It neither
computes a Haar integral natively nor proves model-specific action,
fermion determinant, thermodynamic or time-mesh error estimates.

## 6. The actual enclosure flag has a retained counterexample

The original `is_cauchy_contractive` checks consecutive overlap and
nonincreasing widths. It does not check nesting, the stored contraction
rate, a common target or an infinite shrinking-width law.
Its original `lift_mark_to_continuum` sets `is_witness_verified=True`
when this finite flag is true and the mark is nonblank.

Use the four intervals [0,1], [1/2,3/2], [1,2], [3/2,5/2] with
declared rate 1/2. Consecutive intervals overlap and all widths equal
one, so both original flags are true. The first and last intervals
are disjoint: no common target exists. Widths do not contract by the
declared rate. The [oracle](../evidence/dyadic_source_oracle.json) retains
the actual source outputs rather than replacing those functions.

Even a checked finite nested prefix with smaller widths would not
establish an infinite convergence law or an error bound against a
particular physical target. Appendix M.3 states those further premises.
The source's zero-float and authority fields do not supply them.

## 7. Evidence scopes and replay

The [Lean module](../lean4/WitnessedDifference/DyadicPresentation.lean)
proves fifteen selected natural-number residue/refinement laws at every
natural level, including exact two-element fibers and nonunique adjacent
extension. Its [source-bound receipt](../lean4/dyadic_presentation_axioms.txt)
records actual elaboration. It does not formalize Q/Z, complex orthogonality,
the infinite dual, topology, completion or Haar integration.

Eight math-owner cases and one WDP case check finite arithmetic, exact
orthogonality, common-field pairing, malformed prefixes and resource
refusals. One math case compares 63 original inclusions/coordinates and
378 original character turns. The separate original tests are regression
evidence for their asserted behavior; they do not repair the counterexample.
The [native receipt](../evidence/dyadic_character_receipt.json) binds inputs,
commands, counts and scope. The historical Mathlib census is unchanged.

From the repository root:

```bash
cargo test --offline --locked --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_number_theory --test dyadic_presentation -p omega_wdp --test dyadic_character_adapter
```

From the paper directory:

```bash
python scripts/verify_finite_derivations.py --lean /path/to/lean-4.33.1
```

GEN-WDP-O03/O04 gain a specific refinement classification and a conditional
limit bound. All five enlarged obligations retain their full open scopes.
