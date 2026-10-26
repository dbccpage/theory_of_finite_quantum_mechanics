Status: AI-drafted, awaiting human review.

# Controlled refinement limits of group transport

AuthorityEffect: None.

This result advances `DFM-CONTINUUM-INTERFACE` from a finite non-locality
witness to an actual convergence theorem for a supplied binary refinement
family. It does not construct that family from gauge dynamics or assert a
smooth field. The full node and its physical bridge remain OPEN.

The checkout was synchronized to remote main at
`948f4e7102e67661381afce3fd9ad3742b719536`. Among open continuum-related
nodes without a reserved pull request, this target had impact rank 32.
Its earlier finite witnesses remain intact; they do not already establish
this refinement-limit result. The companion target is
`LQG-CONTINUUM-LIMIT-GAP` (rank 47). Impact is the campaign's ordering rule,
not a measure of mathematical difficulty.

## Supplied structure

Let G be a group with a complete metric and compatible topological-group
structure. Assume the multiplication estimate

    d(ab, cd) <= d(a,c) + d(b,d).

This is the explicit metric hypothesis used in the proof. It holds for
bi-invariant metrics; the theorem does not construct a preferred metric.
For every finite binary word p, supply an edge label U_p. Its two children
are false::p and true::p. Later path factors act on the left, matching the
repository's transport convention. Define

    T_0(p) = U_p,
    T_(n+1)(p) = T_n(true::p) T_n(false::p).

Supply C >= 0 and q >= 0 with 2q < 1, and require, for every word p,

    d(U_p, U_(true::p) U_(false::p)) <= C q^|p|.

Thus the proof does not assume the refined transports already converge.
It assumes a local split-error estimate, from which convergence follows.
The type `Controlled` packages the labels and these quantitative conditions.

## Accumulation over the refinement tree

At depth zero the consecutive-transport estimate is exactly the split
hypothesis. At the next depth the multiplication estimate bounds the error
by the errors in the two children. Applying the induction hypothesis to
each child gives

    d(T_n(p), T_(n+1)(p)) <= C q^|p| (2q)^n.

The factor two is essential: the number of leaves doubles at each step.
`step_bound` proves this for every depth, word and admitted group, without
commutativity. This is an induction over the actual recursive transport.

## Completion, rate and compatibility

The geometric majorant is summable because 2q < 1. The transports form a
Cauchy sequence. Completeness supplies a limit L_p, uniqueness follows from
the metric topology, and summing the error tail gives

    d(T_n(p), L_p) <= C q^|p| (2q)^n / (1 - 2q).

These are `Controlled.exists_limit`, `Controlled.limit_unique` and
`Controlled.error_bound`. The use of real bounds, completeness and the
usual convergence theory is explicit, not derived from finite primitives.
Taking limits in the recursion, using continuity of multiplication, gives

    L_p = L_(true::p) L_(false::p).

`Controlled.limit_split` therefore produces exactly compatible limiting
labels from approximately compatible finite labels.

## Endpoint gauges and continuous parameters

An `EndpointGauge` supplies start and finish gauges for every word. Its
fields require preservation of the old outer endpoints and equality at
the shared midpoint. The dressed edge is

    U'_p = finish(p)^(-1) U_p start(p).

At each finite depth, the two midpoint factors cancel in the prescribed
order. Induction proves

    T'_n(p) = finish(p)^(-1) T_n(p) start(p).

`transport_dress` establishes this algebraically for any group, without a
metric. `Controlled.dressed_tendsto` passes the identity to the limit by
continuity. It does not assume that the dressed tower has separately been
registered as a `Controlled` object.

Now let labels depend on x in any supplied topological parameter space X.
If every finite edge map x -> U_p(x) is continuous and the same C and q work
for every x, the tail estimate is uniform in x. The real geometric bound
tends to zero, so `uniform_refinement_limit` proves uniform convergence and
`continuous_refinement_limit` proves continuity of x -> L_p(x). Pointwise
control with constants depending arbitrarily on x is not asserted to give
this continuity conclusion. No differentiability follows from this result.

## Why the strict decay hypothesis matters

In the additive real group, use the edge value |p| / 2^|p|. Its split defect
has absolute value (1/2)^|p|. Nevertheless the depth-n transport at the
root is n. `critical_transport`, `critical_split_defect` and
`critical_no_limit` prove these facts and nonconvergence in Lean. Shrinking
individual errors at the excluded threshold q = 1/2 are insufficient.

## Independent controls and replay

`checks/independent/dfm-continuum-refinement-limit.py` imports no repository
code. It sums a flattened leaf list rather than using the Lean recursion.
For rational slopes a, offsets b and q in {0, 1/8, 1/4, 3/8}, it checks

    U_p = a/2^|p| + b q^|p|,
    T_n(p) = a/2^|p| + b q^|p| (2q)^n,
    L_p = a/2^|p|.

The tail bound is attained when C = |b|(1-2q). It also checks varying-sign
perturbations, zero offsets, a nonconstant rational endpoint gauge,
noncommutative S3 endpoint cancellation and exactly compatible S3 towers.
Negative controls detect reversed product order, a missing inverse, an
omitted binary factor and the critical decay threshold. The example q=1/4,
a=0, b=1 has root transports 1, 1/2, 1/4, 1/8, 1/16, 1/32, 1/64 and limit
zero. All displayed values are recomputed using exact fractions.

These bounded computations are controls, not a computational proof of
completeness, convergence or continuity. Those statements are kernel-checked
in `lean4/CampaignDfmRefinementLimit.lean`. The source-bound replay receipt
records the exact build, all explicit declarations' axiom reports and
independent output. Only the standard axioms propext, Classical.choice and
Quot.sound are admitted. The full repository Lean workspace is not built.

## What is proved

Convergence with a quantitative rate for every admitted controlled binary
tower; uniqueness and exact compatibility of limiting labels; endpoint
gauge covariance; uniform convergence and continuity for parameterized
families with a common bound; and failure at the stated threshold example.

## What is assumed

The group, complete metric, multiplication estimate, compatible group
topology, binary family, local decay bound, and any parameter topology,
continuous edge maps and compatible endpoint gauges.

## What is open

Deriving these inputs from the existing finite gauge models; arbitrary
triangulation refinements; smoothness, patching and physical locality;
continuum gauge dynamics or a Standard Model identification. This result
supplies a conditional mathematical limit, not those physical bridges.
