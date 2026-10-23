# CODA mathematics inside the Witnessed Difference Programme

The shared mathematics of the CODA estate is developed in **Appendix P of
the [central manuscript](../witnessed_difference_programme.md)**. The nine
runtime stages are applications of six constructions, with additional
contracts at their interfaces. This decomposition makes those constructions
available together without treating a stage name as a mathematical theorem.

The source edition is Git revision
`c8328f651eb231a4c1ede77f160a3f0a2e3e6c64` in `dbccpage/the_symbol_game`.
Its CODA papers, formal sources and application sources are retained.
Their older deposit artifacts keep their original edition and meaning.
This is a consolidation of source mathematics, not a new deposit.
Operational authority of this WDP development remains None.

## The common language

Write `x` for a declared raw state, `p(x)` for a report, `q(x)` for a
protected query, `R` for an admitted linear repair space, and `F` for a
transport of raw states. These five objects have different jobs:

- a report loses distinctions according to its fibers;
- a query descends exactly when it is constant on those fibers;
- a repair quotient identifies states differing by an element of `R`;
- a transport acts on the quotient only when it carries `R` into the
  target repair space;
- a grant is an additional input interpreted by an admitted verifier.

The repair space, topology, verifier and grantor are supplied structures.
The witnessed cut of Chapter 1 supplies none of them by itself. A finite
menu of allowed edits need not be a subspace; in that case it is an edit
system, and the quotient-vector-space proofs do not apply automatically.

## Six reusable constructions

| Construction in Appendix P | Source components | What survives the compression |
| --- | --- | --- |
| Realized-image factorization, P.1 | CS, CS_Q, MUR, FDA, GTLA | One exact fiber criterion, refinement direction, collision countermodels and the separate approximate decoder bound. |
| Repair distance and certificates, P.2 | FOC, OR, FDA, stack | A full repair image, positive weights, primal–dual equality, two repair degrees, trichotomy and compatible transport bounds. |
| Quotient transport, P.3 | MUR, Genesis adapters | Commuting-square pasting, irreversible forgetting, and the new complete fiber-size criterion for actual pair aggregation. |
| Residual section, P.4 | A, FOC | A declared projection splits the repair quotient; equality of its image with the repair space is essential. |
| Compatible gluing and history, P.5 | OR, MUR, GTLA | Fiber products, span composition, additive declared prices and retained raw histories; global coherence is an additional obligation. |
| Completion and terminal standing, P.6 | Q, CS_Q, FDA, GTLA | Uniform extension of one admitted query, common-target enclosures, path/guard witnesses and conditional verifier/grant soundness. |

This organization separates mathematical dependency from operational order.
For example, a profile can be an image quotient without being a cohomology
class. A repair quotient can be represented by a residual section without
selecting an optimizer. A metric completion can close an observable without
extending a discontinuous authorization decision.

## What each primary source contributes

The entries below refer to the retained source edition, rather than to
mutable remote `main`. The companion Lean files are inspected proof sources;
this consolidation does not claim a new compilation of all nine estates.

| Retained primary text | Mathematical contribution and its exact boundary |
| --- | --- |
| [CODA stack](source_archive/coda_component_packages/coda/coda.md) | The witnessed, irreflexive cut and explicit admission discipline; combines the layers. The relation's irreflexivity and later structures are hypotheses. Its source archive and historical-byte refusals retain their custody roles. |
| [FOC](source_archive/coda_component_packages/foc/coda_foc.md) | Weighted finite-dimensional real quotient norms and their full dual feasible sets; a second repair quotient for closure, direct-sum additivity, positive-weight nullity independence and operator-norm transport bounds. Rational exact execution uses rational linear programming, not compactness of a rational ball. |
| [MUR](source_archive/coda_component_packages/mur/coda_mur.md) | Two commuting-square notations describe the same pasting proof. Collisions persist under lawful transport and post-processing; a noninjective collapse has no universal left inverse. Loss accounting and target standing require additional contracts. |
| [CS](source_archive/coda_component_packages/cs/coda_cs.md) | Exact decoding through the realized image iff fiber constancy; coarser constancy implies finer constancy. A decoder on unrealized profile values requires an additional extension choice. No continuum is manufactured. |
| [CS_Q](source_archive/coda_component_packages/cs_q/coda_cs_q_bridge.md) | An epsilon decoder bounds same-profile output distance by twice epsilon. Zero pseudometric distance requires separation before it implies equality. Input Lipschitz control is a different premise; finite sampling can miss an entire query. |
| [Q](source_archive/coda_component_packages/q/coda_q.md) | Metric completion, density, isometry and uniform extension; the actual `Algebra.lean` identifies the completion of the rationals with the reals and proves enclosure and square-root refinement results. Admission records elsewhere are policy wrappers. Neither interval order nor diameter establishes target membership. |
| [A](source_archive/coda_component_packages/a/coda_a.md) | `C²=C` gives the residual `L=I−C`, a quotient section and transport identity. The connection to FOC additionally requires `im C=im d0`. The former ontological A-T8 theorem label is withdrawn in its source; an ontology is not recovered by this compression. |
| [OR](source_archive/coda_component_packages/or/coda_or.md) | Two compatible overlapping pairs glue uniquely to a triple; incompatible overlaps do not. Exact repairs are closed. Support, target binding and terminalizer requirements are explicit standing predicates, not a general sheaf or bicategory theorem. |
| [FDA](source_archive/coda_component_packages/fda/coda_fda.md) | Operational standing is a terminal together with an actual path and seven derived guards. Regime standing is verification plus a recorded grant. Soundness follows under two additional universal soundness hypotheses; connecting these two standing models needs an explicit interpretation. |
| [GTLA](source_archive/coda_component_packages/coda_gtla/coda_gtla_monograph.md.txt) | Comparison spans compose by a fiber product. Declared composite cost is a sum; trace erasure forgets work. Terminal constructors are disjoint. The finite Boolean evaluator copies declared answers and does not prove the component theorems or general Master Normal Form. |

The [pinned source tree](https://github.com/dbccpage/the_symbol_game/tree/c8328f651eb231a4c1ede77f160a3f0a2e3e6c64/omega_engine_atlas/coda_atlas/F005_coda)
provides immutable retrieval of the same component paths.
The component packages remain the owners of their historical papers, proof
files, code and release records. WDP is the integrated mathematical reading
surface. There is no claim that deleting those originals is justified.

The formal scopes are narrower than the written synthesis in several places.
FOC's selected separator, diagonal-minimum and transport declarations do not
formalize the entire weighted linear-programming duality theorem. CS_Q's
Lipschitz declaration uses an abstract monotone scale, rather than constructing
a real metric instance. A's quotient core proves additive/function laws;
scalar linearity in P.4 is a written argument. FDA's operational and regime
standing records still need an interpretation between them. Q's
`Algebra.lean` does contain actual Mathlib completion results, whereas the
nearby admission records have different policy roles.

## Native owners and the finite application

The [Python application](../code/coda_application/README.md) begins
with supplied finite cochain data. It solves the unweighted rational repair
problem, checks selected layer conditions and enforces a local HMAC grant
contract. Its Rust bridge prepares payloads; it does not call a native solver.

Both primary Layer3 implementations only inspect fine tokens already present
in the supplied projection map; an unmapped fine token can escape that check.
They take no protected query argument and therefore cannot establish P.1's
query fiber criterion. Their successful diagnostic text must be read within
this partial profile-check scope. The independent WDP diagnostic/proposal
profile has its own explicit certificate replay contract.

| Native surface | Actual responsibility | Remaining mathematical or operational premise |
| --- | --- | --- |
| [omega_coda](../../../../../../omega_engine/crates_rs/omega_coda/src/lib.rs) | Owns the nine-stage finite pipeline and canonical Q modules. FOC checks exact certificates, closure-map shape and `d1 d0=0`; its next defect is `‖d1 x‖1`. | This pipeline has no arbitrary positive weight vector or second repair map `a2`. Supplied grant strings are untrusted; the FDA stage refuses them with `EXTERNAL_GRANT_VERIFIER_UNAVAILABLE`. |
| [CODA diagnostic routing](../../../../../../omega_engine/crates_rs/omega_coda/src/diagnostic_routing.rs) | Replays exact WDP-profile certificates and separates diagnosis from policy-scoped proposal. | It does not invoke the nine-stage operational authority pipeline. |
| [omega_coda::q](../../../../../../omega_engine/crates_rs/omega_coda/src/q/mod.rs) | Owns validated admission packets, finite-shadow fixtures, spectral membrane and the CS-to-Q adapter. | Public continuum-shadow strings, anti-collapse flags and transport DTOs are declarations until their particular evaluator checks them. They are not universal completion proofs. |
| [omega_q](../../../../../../omega_engine/crates_rs/omega_q/src/lib.rs) | Compatibility re-exports of `omega_coda::q`. | It is not a second implementation or independently constructed continuum. |
| [omega_wdp](../../../../../../omega_engine/crates_rs/omega_wdp/src/lib.rs) | Retains source-specific states, histories, observation assembly and thin owner adapters. | A WDP receipt has None authority. The broader all-source refinement and physical-model obligations remain open. |
| [Pair transport owner](../../../../../../omega_engine/crates_rs/omega_linear_algebra/src/gauge_pair_transport.rs) | Computes exact `P M Pᵀ`, classifies gradient descent and independently replays a cycle counterwitness. | The complete mathematical theorem is finite but unbounded in carrier size; this executable accepts at most 256 vertices per carrier. |
| [Genesis carrier adapter](../../../../../../omega_engine/crates_rs/omega_wdp/src/genesis_transport_descent.rs) | Checks actual AddTerm/Identify execution against that transport for both raw count tables; retains marks and both complete states. | The classification concerns fixed-writing gradients. It does not quotient raw cost, enabled removals, oriented filling constraints or future histories. |

No Rust modules are moved or split in this increment. Adding a generic
transport criterion and its source adapter does not complete the deferred
crate decomposition.

## A single worked route through the constructions

Take the source potential `g=(0,0,1,0)` and the directed table
`e(x,y)=g(x)−g(y)`. Its fixed-carrier repair class is zero. Identify source
vertices 0 and 1, retaining target vertices 0, 1, 2. Endpoint fiber sizes are
`m=(2,1,1)` and fiber sums are `s=(0,1,0)`. Actual count aggregation gives

    T(e)(0,1) = -2
    T(e)(1,2) =  1
    T(e)(2,0) =  0

The cycle is `−1`, so `T(e)` is not a target gradient. The zero source table
and `e` were repair-equivalent; their transported tables are not. Consequently
the quotient report fails the fiber criterion for this proposed transport.
No target quotient arrow can make its square commute on all representatives.

This is one obstruction appearing in three useful languages: failure of a
repair subspace to be preserved (FOC), failure of report factorization (CS),
and failure of a proposed descent square (MUR). It is one mathematical
failure, rather than three independent diagnostics. A projection section
cannot cure it: choosing representatives changes the operation and requires
its own declared preservation law.

For contrast, merge six vertices in three pairs. Then `m=(2,2,2)` and
`T(dg)=d(2s)` for every potential. Balanced aggregation descends, and balanced
maps compose. That positive result still says nothing about whether raw
history, source edit prices or institutional grants descend.

More precisely, the lawful total maps form a subcategory of finite sets, and
`X ↦ Z^(X×X)/{dg}` with fiber-sum arrows is a functor to abelian groups.
Identity and composition follow from the raw operators; quotient descent
follows from the repair-subspace criterion. This closes a selected finite
category. It does not turn the unrestricted Genesis edit graph into that
category or supply its missing higher overlap laws.

## Where the continuum and language work must focus

1. For a selected domain, preserve the protected query through the actual
   finite profile and prove relative uniform continuity on its image. Then
   use the complete target's extension theorem. Appendix O provides such
   selected presentation, Meron pressure/response and static Gaussian routes.
2. Retain common-target interval membership and a shrinking error modulus.
   Rational interval arithmetic alone supplies neither. General spacetime,
   interacting critical scaling and all-temperature response still need
   their model-specific estimates.
3. Supply coherent carrier-changing operations and higher overlap laws before
   claiming a general site, sheaf, cohomological language or HoTT semantics.
   The new fiber criterion closes one operation family, not this whole task.
4. Extend the existing AutoP normal-form contract around explicit report,
   query, repair, transport and certificate interfaces. Keep finite menus,
   linear quotients, approximate decoders and authorization predicates typed
   separately; one common syntax does not make their semantics interchangeable.
5. Bind grantor standing, jurisdiction and interpretation to the target
   regime. Mathematical completion and a successful local verifier cannot
   select those institutional premises.

This decomposition compresses the existing finite and conditional theory.
It leaves the full five enlarged Genesis obligations and a universal
domain-independent/continuum reconstruction as research obligations.

## Balance preservation is a separate dynamic question

[Appendix P.7](../witnessed_difference_programme.md#p7-complete-balance-preservation-rules-for-the-five-source-25-edits)
classifies all five canonical Source-25 edits for a fixed ordered carrier and
oriented face set. AddTerm always preserves old declared balances; assertion
addition/removal does so iff the directed arc occurs in no filled face;
Identify does so iff no surviving face touches the merged vertex; Fill does
so iff the new cycle row is implied by the old rows over Q.

These are balance rules on raw states, not an unrestricted quotient functor.
In particular, an individual zero-excess merge can remain balanced while a
different balanced input disproves its universal preservation. Three ordinary
tetrahedron faces do not imply the fourth on independent directed arcs; seven
directed face equations do imply the eighth. This provides an explicit local
coherence test without silently importing antisymmetry or a higher site.
