Status: AI-drafted, awaiting human review.

AuthorityEffect: None.

This is an explicitly declared language extension. It does not reconstruct the
sealed Alpha harness, replace its license protocol, or derive the desirability
of separating every collapsed pair from observations. The new policy field has
two constructors: halt and separateAll. The latter is an admitted goal choice.
Lexicographic order on the existing datum indices is its declared tie rule;
no equivariance under arbitrary reindexing is claimed for that choice.

The extension has instruction syntax SEEK, SOURCE(event), and SETPOLICY(policy).
Its interpreter retains the source's optional failure on SOURCE. SEEK computes
from the admitted regime and policy; its caller supplies no target pair. The
example program SETPOLICY(separateAll); SEEK records the pair in an initially
unconstrained two-datum regime. Thus the generator runs inside this declared
interpreter, rather than using a host-provided target argument.

To compute observations, enumerate every slot as either a hole or an admitted
datum, take all tuples of the admitted arity of each form, and retain tuples
with a hole. Structural induction proves that membership is equivalent to the
actual source wfCtx predicate, including forms of arbitrary arity and multiple
holes. Agreement over that finite list is equivalent to source collapse over
all well-formed contexts. Uniform rules are evaluated by the source's actual
derivability predicate; neither the visible token spelling nor a new datum is
used in the computation.

The agenda consists of ordered admitted pairs that collapse and have not yet
been recorded as requirements. Under separateAll, next chooses the first
member. Its soundness theorem gives all source impose guards and freshness.
Its empty-result theorem is exact: every ordered collapsed pair is already a
requirement. Each successful SEEK is precisely the existing source impose
event, increases the requirement-list length by one, preserves every observation
coordinate and the policy, and cannot immediately request the same pair again.
The instruction interpreter and source instruction agree on that event.

Recording a requirement does not satisfy it. Saturation here means that every
fresh agenda entry has been requested, not that any still-collapsed pair has
been separated. A responder, its search measure and authorization to admit a
response are separate interfaces. Neither repeated SEEK nor the source's
response-existence theorem establishes autonomous continued growth.

The two policies give different next results on the same admitted observations.
This explicit control prevents presenting the new goal choice as a consequence
of source observation alone. In the unconstrained two-datum fixture a single
SEEK saturates its fresh agenda. The actual reading-L regime already records
its target, so that fixture is deliberately not mislabeled as reading L.

The independent check covers all fact sets, uniform-rule sets and initial
requirement subsets for datum counts through three and the declared empty,
unary and binary signatures. A direct all-context agreement implementation and
a separately formed observation-profile implementation give identical agendas.
SymPy recomputes the complete census: 8,424 regimes. Repeated SEEK makes 6,517
fresh request steps and saturates every declared case. Three explicit mutants
ignore existing requirements, ignore HALT, or ignore a distinguishing
observation; each returns an incorrect pair on its stated control. Normal and
optimized runs agree and strict mypy passes. These bounded regressions are
separate from the general Lean membership and instruction theorems.

What is proved

A computable object-language generator in the declared extended interpreter,
complete source-context enumeration, sound fresh targets, exact empty-agenda
criterion, and a recorded source impose step for each generated target. All
seventeen exported theorem audits compile with permitted kernel axioms.

What is assumed

The admitted separateAll policy and index-order tie convention. The source
admission/observation semantics are imported from the pinned Basic module.
The source byte pin is checked in the receipt. Lean/checker author assessments
are L4D; declarative Lake configuration is L1C under the explicit configuration
exception. Assessments await human review.

What is open

Integrating this language extension with Alpha, response search and licensing;
selecting a policy from the frozen source without a new declaration; and an
unbounded continuation theorem. The original historical absence statement
remains accurate and its node stays OPEN. This is a provisional narrowed result.
