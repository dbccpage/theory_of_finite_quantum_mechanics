# A Schur-type reformulation of local tomography

Product preparation and factorized probabilities do not imply local tomography.
They do imply a calibrated observation map, which isolates the exact missing
subspace. Local tomography follows if an additional irreducible family of
admitted operations preserves observational indistinguishability. The latter
operational principle remains an assumption.

## The conditional kernel argument

Let K be any field, V a K-vector space of unnormalized states, and I and J finite
local frame index sets. Let p(i,j) be independent preparations and e(i,j) linear
product tests satisfying

    e(i,j)(p(k,l)) = delta(i,k) delta(j,l).

The dual frame elements may be signed linear combinations of physical
preparations and effects. They are coordinates in the supplied linear spans;
individual dual elements are not required to be positive or physically
admissible. No assertion that these tests separate V appears here. Define

    M(x)(i,j) = e(i,j)(x)
    R(c) = sum_(i,j) c(i,j) p(i,j).

The Lean constructions `ofDualFrame` and `ofProductFrame` prove MR = identity.
With H = identity - RM, the module proves MH = 0, HR = 0, H squared = H, and

    x = R(M(x)) + H(x).

Thus local tomography is equivalent to H = 0. In finite dimension,

    dim(V) = |I| |J| + dim(ker M).

Calibration supplies the lower bound and a reconstruction of visible coordinates;
it leaves every dimension of ker M unconstrained. The general dimension lemma
uses an arbitrary coordinate space C; `product_dimension` specializes to I x J
when injectivity has been established.

Suppose admitted linear operations T(g) and coordinate actions L(g) satisfy
M T(g) = L(g) M. This **observation descent** follows, for example, if every
pulled-back product test has a supplied finite expansion in the product tests.
`descent_of_test_pullback` verifies that implication, and `descent_comp` verifies
closure under sequential composition. It does not prove that a proposed physical
operation has such a pullback.

The kernel of M is then a common invariant subspace. Add the hypothesis that the
family T is **irreducible**: its only common invariant linear subspaces are zero
and V. Since M is nonzero, its kernel cannot be V; it must be zero. This proves
injectivity by a Schur-type argument. Once the operation family may be freely
chosen, existence of a descending irreducible family is equivalent to tomography;
it is not an independently weaker reconstruction premise. `calibrated_tomography`
obtains nonzero observation from calibration and a nontrivial coordinate space.

The main proof is field-neutral and does not choose real, complex, quaternionic,
or Hermitian state carriers. `OperationalFieldSelection.selected_parameter`
connects it to the previous dimension theorem: for the supplied same-family law
K(d,n) = n + d choose(n,2), d > 0 and the stated two-system dimension, it selects
d = 2. That selects a parameter within this law, not a classification of all
operational theories or a derivation of the law itself. The redundant nonzero
observation argument has been removed from `selected_parameter`.
`two_hypotheses_satisfiable` exhibits a rational 16-coordinate identity-calibrated
model with all matrix units at d = 2, discharging every headline hypothesis.
`selected_carrier` concludes c = .complex for the supplied real/complex/quaternion
catalogue. This selects a catalogue label; it does not identify the arbitrary
coefficient field K with the complex numbers.

## Why the extra assumptions matter

For a classical binary pair take C = Q^4 and V = C direct-sum C, with positive
cone given by nonnegative coordinates in both blocks. Set

    M(x,y) = x+y,     R(c) = (c/2,c/2),
    T(g)(x,y) = (A(g)x,A(g)y),     L(g) = A(g).

Here A(g) ranges over the 16 product matrix-unit outcome filters. Calibration,
product-probability factorization, positive preparations, normalization, positive
subnormalized filters, and observation descent all hold. Yet (c,0) and (0,c),
for any unit coordinate c, are distinct positive normalized states with identical
product statistics. The hidden anti-diagonal (h,-h) is a four-dimensional
invariant subspace, so irreducibility fails.

The global first-block normalization question distinguishes those states.
Quotienting by ker M removes that question. It constructs a tomographic quotient,
but does not prove tomography of the original theory or preserve its protected
questions. Lean now also defines `PairIndex = Fin 2 × Fin 2`, an eight-coordinate
doubled carrier, and its block-diagonal product filters. The theorems
`doubled_product_calibration`, `doubled_product_descent`,
`doubled_product_not_irreducible`, and `doubled_product_not_injective` verify the
binary-pair claims. The scalar doubled witness additionally proves failure of
descent of a protected first-block question. The existing `TensorHiddenCoordinates` supplies the stronger Hermitian
countermodel independently.

The finite controls also check the two converse mistakes:

| Model | Calibration | Descent | Irreducible | Tomography |
| --- | --- | --- | --- | --- |
| Classical product matrix units | yes | yes | yes | yes |
| Doubled product filters | yes | yes | no | no |
| Identity operations on Q^4 | yes | yes | no | yes |
| All matrix units on the doubled space | yes | no | yes | no |

For the last model irreducibility holds because every matrix unit is present;
`matrix_units_irreducible` proves this over any field. The identity-only model
has many invariant subspaces. Failure of full operator span alone is not treated
as proof of reducibility for an arbitrary family.

For a fixed prescribed operation family, tomography does not imply that family's
irreducibility: the identity-only family above is a counterexample. If the family
may instead be freely chosen, the statement is an equivalence:

    (exists ops, localOps, descent and Irreducible ops) <=> Injective observe.

`OperationalFilterFamily.exists_descending_irreducible_iff` proves this for a
calibrated finite nonempty coordinate space. Its reverse direction uses
`product_resets_irreducible_iff` from PR147 and the explicitly descending family
R E_ij M. Existence of such a family is therefore a Schur-type reformulation;
physical availability still needs an independent justification.
It also cannot be imposed on normalization-preserving dynamics alone when a
nonzero proper normalization kernel exists: that kernel is invariant. This is
`normalization_obstructs_irreducibility`. Individual outcome filters may decrease
normalization; the classical matrix units provide positive, subnormalized
examples, with both positivity and subnormalization proved in Lean. Their
availability in a different operational theory remains to be established.

## Assumptions still open

1. A field-linear state space, linear effects, and the relation of those objects
   to primitive difference are supplied. The theorem does not derive scalars,
   convexity, positivity, or a complete effect space.
2. Independent dual preparation/test frames and factorization are supplied.
3. Closure of pulled-back product tests under each admitted operation must be
   proved in the target theory. Arbitrary global operations need not descend.
4. An irreducible family of those operations must be justified independently of
   tomography. Postulating all global measure-and-prepare operations and then
   silently assuming their descent would import the missing separation claim.
5. The complex-selection bridge retains the same-family dimension law and d > 0.
   General classification, tensor-cone uniqueness, and primitive-to-QM closure
   remain open.

The next mathematical task is to justify an appropriate outcome-filter family
and its test-pullback identities from independently motivated operational rules,
or exhibit a further countermodel. Proving only reversibility or normalization preservation
cannot discharge this route's irreducibility premise.

## Verification and custody

The two Lean modules prove the universal conditional statements. Python Fraction
and Rust BigRational independently replay the same original JSON matrices.
The 277 mutation cases are fixture-integrity checks: they reject changes to the
fixed certificate, schema types, scope and premise list. Their rejection is not
evidence that every changed calibration is mathematically invalid. Separate
semantic tests accept alternative valid calibrations, show a descending reducible
family on a tomographic carrier, and test the effect-separation boundary. They
use the generic exact analyzer without the fixture identity validator. Optimized
Python retains its scope guard; neither type of finite check replaces Lean proofs.

Run `py -3.12 -X utf8 replay.py --output <new-directory>` from this run directory.
The replay checks the exact required source set before and after execution,
reconstructs the candidate, re-elaborates both Lean files, audits the declared
headline axioms, runs Python and Rust controls and the existing complex-selection
regressions, and checks typed composition records, DAG synchronization, contracts, and whitespace. It never
overwrites an earlier result directory. Local toolchain/path dependencies are
recorded in the receipt; Rust uses the repository's existing sibling-repository
dependencies and the pinned Cargo lockfile.

`p2/attempts` retains exploratory elaboration and typed-composition failures.
`p2/initial_verified` retains the first executable pass, before the operation
record repair; its pin envelope and changed source snapshots are preserved.
`p2/verified` holds the final command, axiom, mutation, and source receipts.
The canonical DAG and prior evidence are unchanged; `p5/proposed_dag_delta.json`
is only a proposal. This is one researcher's source review with independent
language checks, not a fabricated independent reviewer or provider panel.

Supported: a field-neutral Schur-type reformulation, its conditional dimension
consequence, explicit countermodels, and a conditional dimension-family bridge.
Not supported: unconditional local tomography from primitive difference or a
completed reconstruction of complex quantum theory. AuthorityEffect: None.


Follow-up custody: the requested text and proof corrections are validated in
`../../reviews/20261021T210045Z_claim_boundary_fixes/`. Earlier pin envelopes and
receipts retain their original bytes and apply to their historical commits; use
the follow-up replay for the current sources rather than resealing old receipts.
