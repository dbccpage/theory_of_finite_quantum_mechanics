# Admission floors and lawful cochain transport

AuthorityEffect: None. These are additional derivations for the enlarged
Genesis-to-WDP programme. They do not alter the sealed Genesis source or the
154-row monograph register.

## The primitive floor

An exhibited cut consists of a carrier V, a relation R, two designated
elements a,b, the positive instance R(a,b), and the protected law
`forall x, not R(x,x)`. Substitution proves a differs from b: identifying
them turns the instance into a prohibited diagonal. Therefore a subsingleton
carrier cannot support the cut. Any transport preserving both the instance
and the law must preserve the separation of these endpoints.

The hypotheses are necessary in distinct ways. On a singleton, the full
relation has an instance and violates irreflexivity; the empty relation is
irreflexive and has no instance. On Bool, both the forward and reversed
single-edge cuts satisfy the conditions. The cut law selects neither
orientation. Admission of a carrier, form, instance and law remains explicit;
visible glyphs in the opaque inscription supply none of them.

[`PrimitiveAdmissionFloor.lean`](../lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean)
proves these statements for arbitrary types. Its final two declarations
compare *declared* prices of unary and binary responses. They do not prove
the original Genesis cost-floor theorem or that these two responses exhaust
every possible language. Those source results keep their original scope.

This supplies a precise admitted cut floor for GEN-WDP-O01. The obligation
to refine each original challenge generator and account for every permitted
minimum alternative remains in the enlarged programme.

## Maps between different cochain carriers

Write `dA0: A0 -> A1`, `dA1: A1 -> A2` and likewise for B, with
`dA1 dA0 = dB1 dB0 = 0`. A supplied linear triple F is a cochain map when

```text
F1 dA0 = dB0 F0
F2 dA1 = dB1 F1.
```

If y=x+dA0(r), linearity and the first square give
`F1(y)=F1(x)+dB0(F0(r))`. Thus F descends to the repair quotient
`A1/im(dA0) -> B1/im(dB0)`. The second square transports closedness, so F
also induces a map on `ker(dA1)/im(dA0)`. These are different quotients.
Neither equation establishes injectivity, surjectivity or norm preservation.
For example, doubling every degree of a hollow triangle is a commuting map
and doubles its nonzero L1 quotient value.

Identity maps and composition satisfy the same two equations. Composition
requires the entire intermediate differential presentation, including its
ordered coordinates, to agree. Matching dimension numbers alone is insufficient.
The owner `linear_algebra::finite_cochain_map` checks those conditions before
constructing a map. `identity` and `then` return checked maps; raw matrices
cannot bypass the constructor.

If a supplied down-map satisfies `down up = id` in every degree, applying down
to a repair between two up-images proves a repair between the original
representatives. This reflects quotient equality on the old image.
`up down = id` is a separate condition. Inclusion `(x -> (x,0))` and projection
`((x,y) -> x)` exhibit a retraction with a new direction that does not descend
back as an identity. A linear projection here is not MSS's typed
`NON_DESCENT` response on a novel syntactic term; that syntax policy remains
an additional contract.

## Supplied homotopies and their limit

A degree -1 homotopy H between F and G must supply both matrices H1 and H2:

```text
F0-G0 = H1 dA0
F1-G1 = dB0 H1 + H2 dA1
F2-G2 = dB1 H2.
```

For a *closed* x, the middle equation reduces to
`F1(x)-G1(x)=dB0(H1(x))`. Hence F and G agree on closed cohomology classes.
For arbitrary x the additional `H2 dA1(x)` term can survive. A homotopy does
not imply agreement on every raw repair-quotient class.

The exact countermodel is the rational complex with dimensions `(1,2,1)`,
`d0(t)=(t,0)` and `d1(a,b)=b`. The identity is homotopic to zero with
`H1(a,b)=a`, `H2(t)=(0,t)`. The nonclosed element `(0,1)` still has a nonzero
raw repair class. Conversely, two unequal maps of a zero-differential
complex cannot acquire a homotopy merely because both curvatures vanish.

`CochainHomotopy::try_new` checks all three equations and every coordinate.
Missing, incorrectly shaped, and altered matrices are refused.
[`CochainTransport.lean`](../lean4/WitnessedDifference/CochainTransport.lean)
proves repair transport, composite squares, retraction reflection and the
closed-class implication under explicit additive and square hypotheses.
These abstract theorems do not certify an arbitrary user scalar type's ring
laws; the native exact tests use BigRational.

This develops the linear branch of GEN-WDP-O03. Source-specific dynamic
carrier maps, restriction sites and actual higher cell fillers are still
required. An explicit cochain homotopy is not a general Kan-filling theorem.

## Native ownership and verification

The least reflexive/transitive closure of a finite relation now belongs to
`omega_category_theory::finite_relational::FinitePreorder`. WDP resolves
its declared labels and delegates the closure. Duplicate or empty labels,
absent edge endpoints and absent query endpoints return typed errors.
Public field mutation and unchecked deserialization no longer construct a
WDP preorder. The empty carrier remains valid. Cycles can yield a preorder
without yielding an antisymmetric order.

The focused category tests compare every one of the 512 three-state relations
with an independent path search and test leastness against every possible
reflexive/transitive superrelation. This is exhaustive only on that carrier
size. The matrix-owner tests check composition, exact context mismatch,
retractions, the homotopy countermodel and malformed fillers. The source-bound
Lean receipts audit eight new admission declarations and four transport
declarations; the enlarged standalone spine audits 311 selected declarations
across 22 modules. The historical 202-declaration Mathlib census is unchanged.

Run native tests sequentially from the canonical Cargo workspace, with the
configured shared target cache on Windows worktrees:

```text
cargo test --locked --offline -j 1 -p omega_category_theory --test finite_preorder
cargo test --locked --offline -j 1 -p linear_algebra --test finite_cochain_map
cargo test --locked --offline -j 1 -p omega_wdp --test evaluation_preorder
```

The [teaching lab](../../../../../../omega_engine_education/documentation/070_witnessed_difference_programme_wdp/curriculum/710_wdp_finite_obstruction/concepts/lesson_710_04_admission_and_transport.md)
walks through the distinction and the two quotient types. Executing its
finite arithmetic examples supplies an example replay, not a learner study
or an unrestricted reconstruction of the programme.
