# Mathematical constructions and executable contracts

The standalone companion uses Lean 4.33.0 and its standard library. Group laws,
quotient maps, inverse equations and normal-form classification below have proof
terms. They are not supplied as conclusions in structure fields. Structures for
input chain complexes, chain maps, groups and distributions carry their defining
laws; each displayed concrete model supplies those laws by proof.

## Core statements

| Manuscript claim | Lean construction | Quantification and scope |
| --- | --- | --- |
| Report reconstruction and uniqueness | `PreMssn.history_report_criterion`, `history_factor_unique` in `Paper.lean` | Arbitrary carriers; factorization is on the actual report image |
| Observational identification and task descent | `Observation.profileSetoid`, `task_descent_iff`, `collapsed_quotient_barrier` | Heterogeneous observation families and their actual quotient |
| Finite demand accounting | `PreMssn.demand_accounting`, `demand_register_nodup` in `Paper.lean` | Finite distinct registers, discharge membership and disjoint births |
| Typed recovery | `PreMssn.old_image_injective` in `Paper.lean`, `SnTheorems.old_image_base` | General recovery law; all imported base constructors and stages |
| Free-monoid nonisomorphism | `PreMssn.word_iso_alphabet_bijection`, `unequal_finite_alphabets_not_iso` in `Paper.lean` | Actual list monoids and two-sided homomorphism inverses |
| Discrete-category obstruction | `DiscreteCategory.equivalence_object_bijection`, `two_and_twenty_six_not_equivalent` | Equality morphisms, functors and natural isomorphisms |
| Constructed homology and chain-retraction obstruction | `Homology.homologyMap`, `induced_homology_injective` | Actual cycle subgroup and quotient by boundary image in a three-degree fragment |
| Integral class encoding and torsion | `Homology.integer_class_eq_iff`, remainder classification and order-two lemmas | Every integer modulus, including zero and negative values |

## Graphs and finite coordinates

[FreeAbelian.lean](../lean4/FreeAbelian.lean) constructs the free abelian group
from an additive-term congruence, including interpretation and universal
extension/uniqueness. [GraphHomology.lean](../lean4/GraphHomology.lean) constructs
the boundary quotient and its isomorphism with the free abelian group on actual
connected components. `vertex_class_eq_iff_connected` identifies precisely when
two vertex classes coincide. Vertices and edges have separate carriers, allowing
empty graphs, loops and parallel edges.

[FiniteCoordinates.lean](../lean4/FiniteCoordinates.lean) constructs
`freeFiniteIso`, `graphH0Iso` and `graphReducedH0Iso`. The reduced group is the
augmentation kernel, with explicit inverse coordinates. An enumeration of the
component quotient is an explicit parameter; its correctness is not assumed
from an executable union-find result.

[UnionComponents.lean](../lean4/UnionComponents.lean) proves the component
algorithm's correspondence separately. `labels_eq_iff_connected` and
`labels_eq_iff_h0` characterize its computed fibers for arbitrary vertex types.
`canonical_eq_iff_h0` connects selected representatives with actual H0 classes;
`natural_root_minimum` proves the least-vertex convention. `computedH0Iso`
constructs a basis from these representatives when the enumeration covers the
vertex carrier. The bounded replay now calls this component algorithm.

[GraphExtensions.lean](../lean4/GraphExtensions.lean) proves finite component
count changes, the maximal count criterion and nonzero loop classes.
[GraphRetraction.lean](../lean4/GraphRetraction.lean) constructs path chains and
proves `chain_retraction_iff_connected`: an added edge admits a chain retraction
fixing old zero-chains exactly when its endpoints were already connected.

[TriangleHomology.lean](../lean4/TriangleHomology.lean) proves the unique
diagonal coordinate of every integral cycle, constructs `unfilledH1Iso` with
the integers and `filledH1Iso` with the trivial group, and proves that attachment
has no chain retraction. Its class encoder refuses exactly the noncycles.
[TriangleDegree.lean](../lean4/TriangleDegree.lean) extends this to every integer
face degree m: actual inverse homology maps identify the group with Z/(m Z).
The class encoder is proved complete for these classes, including m=0 and
negative m, and the degree-two cycle is proved nonzero with double zero.

## Words, duality and probability

[WordRecovery.lean](../lean4/WordRecovery.lean) proves the fixed-width decimal
roundtrip and injectivity, failure of surjectivity onto all binary words,
language restriction/retraction, exact old-word refusal, erasure homomorphism,
renaming inverse criterion and directed-edge multiset preservation under trace
reversal. [Observation.lean](../lean4/Observation.lean) also proves uniqueness of
the pointed D2 relation map. That statement concerns a vertex map preserving a
relation; it does not assert uniqueness of chosen edge identities in a
multigraph with parallel edges.

[Cochain.lean](../lean4/Cochain.lean) constructs the additive-homomorphism dual
and proves that precomposition gives square-zero coboundaries. It identifies
the concrete triangle face cochain coordinate with the general construction.
It also constructs contravariant pullback and proves the split surjection on
cohomology induced by a chain retraction, for arbitrary coefficient groups.
`triangle_repair_invariant` and `triangle_repair_exact_iff` supply the concrete
WDP handoff: circulation is unchanged by integral vertex-potential repairs and
is zero exactly when such a repair exists.
[ChainHomotopy.lean](../lean4/ChainHomotopy.lean) proves homology functor laws,
equality of maps induced by a chain homotopy, and injectivity for a retraction
up to homotopy. The filled triangle admits no such homotopy retraction.

[FreeGroup.lean](../lean4/FreeGroup.lean) constructs the nonabelian group-term
quotient, its universal property and abelianization factorization/uniqueness.
A three-point permutation interpretation detects the nontrivial commutator.
[FreeWord.lean](../lean4/FreeWord.lean) proves complete normal-form
classification: `word_equality_iff_reduction` concerns equality in the actual
group quotient, and `reduce_idempotent` establishes the canonical convention.
[WedgeHomology.lean](../lean4/WedgeHomology.lean) constructs the two-loop graph's
actual H1 group and identifies its zero commutator class.

[BellPair.lean](../lean4/BellPair.lean) constructs normalized rational pair
distributions with uniform marginals and correlations (1,1,-1,1). It bridges
Boolean parity to arbitrary integer sign assignments.
[BellMixture.lean](../lean4/BellMixture.lean) proves the oriented CHSH bound for
every normalized nonnegative rational distribution on the sixteen deterministic
assignments. `target_has_no_joint_distribution` excludes the displayed target
in this model. The runtime constructor checks the laws of the very distribution
used by the theorem. No claim about physical realization follows.

## Shared finite wire conventions

Replay records use `v1`, an operation name and fields separated by ASCII tabs.
Integer lists use ASCII commas and canonical decimal spellings: no leading
zero, plus sign, negative zero or non-ASCII digits. Each input integer has
magnitude at most 1,000,000. Malformed records return `REFUSE`.

| Operation | Additional convention | Result |
| --- | --- | --- |
| `triangle` | Flag 0/1 and three integral edge coefficients | Unfilled diagonal coordinate or filled zero; noncycles refused |
| `triangle_degree` | Integer degree and three integral edge coefficients | Canonical class modulo the degree; zero degree retains the integer |
| `cochain` | Three integral edge-cochain coefficients | Sum on the oriented face boundary |
| `bellpair` | Flag 0/1 selects correlation +1/-1 | Four numerators with denominator 2, ordered (++,+-,-+,--) |
| `decimal` / `decimal_decode` | At most 16 ASCII digits / 64 bits; four most-significant-first bits per digit | Exact coding; incomplete or nondecimal nibbles refused |
| `recover` / `erase` | At most 64 letters in `abc`, old alphabet `ab` | Recovery returns `NON_DESCENT` on a new letter; erasure deletes new letters |
| `rename` | Mapping list at most 8 entries; word at most 64 source indices | Mapped indices, with out-of-carrier indices refused |
| `trace` | At most 16 triples (first, direction 0/1, last) | Reverse order, swap endpoints and flip every direction |
| `freeword` | At most 64 letters in `abAB`; capitals denote inverses | Reduced word in the same alphabet, with the empty string for identity |
| `bellmix` | Sixteen nonnegative integer masses, positive total | Four correlations then oriented score, as reduced rational strings |

Joint-assignment order is lexicographic in (a0,a1,b0,b1), with Boolean false
(sign +1) before true (sign -1). Rational strings use a signed numerator and
positive denominator, omit `/1`, and represent zero as `0`. These explicit
conventions, rather than each language's generic object ordering, define the
exchanged representatives.

The original report, demand, boundary, component, cyclic-class, code-collision
and CHSH operations retain their prior conventions. Carrier/history size is at
most eight and graphs have at most sixteen edge occurrences. Component output
lists pairs (least vertex, total coefficient), in increasing representative
order, retaining zero totals for present components.

## Remaining formal and publication limits

The identification between the constructed free group and continuous based
loops modulo homotopy in a topological two-circle wedge remains open. Neither
the algebraic quotient nor the cellular chain complex supplies this comparison
by definition. The manuscript cites the standard topology while keeping this
formal obligation explicit.

Agreement of the three native runtimes is bounded executable evidence; it is
not a general source/compiler refinement proof. The compiled census counts all
package-local constants, including generated declarations, rather than distinct
theorems. Independent mathematical review, author decisions and public deposit
remain separate from local compilation and package verification.
