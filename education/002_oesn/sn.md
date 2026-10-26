# S(n): presentations, declared continuations and finite obstructions

AuthorityEffect: None.

S(n) labels presentations in a staged continuation of Genesis. The source
begins with the literal opaque inscription `<>`; its executable model has an
empty admitted regime, and a supply event leaves that regime unchanged.
An explicit admission changes it. The mathematics below records the source
facts and the extra constructions used to carry them forward.

Read the [source correspondence](source_correspondence.md) before assigning a
source theorem to a stage label. The active combined manuscript is
[From Pre-Genesis to MSS-N](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md).
The [WDP construction](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/derivations/genesis_construction.md)
connects a recorded literal-root history to the canonical Rust primitives and
a declared finite simplicial interpretation.

## 1. Source, representation, application and checking

Keep four questions separate: which events were admitted; how they are
represented mathematically; what application the representation describes;
and which equations or records the checker actually verifies. A result in a
representation transfers to the admitted construction through an explicit
preservation or reflection theorem.

The historical “Two Boxed Laws” express design requirements for such work:
identify the unresolved demand and licensed response, and justify returning
claims from a mathematical representation to its source. They are not
independent theorems that force the next event. An external continuation
request and a choice of response grammar are legitimate recorded inputs.

## 2. From inscription to a separation challenge

| Label in this strand | Event or construction | Established scope |
| --- | --- | --- |
| S(0) | Supply the opaque whole `<>` | Empty admitted regime; no internal derivation |
| S(1) | Supply `<a>`; separately choose admission if required | Supply alone is a no-op |
| S(2) | Retain the opaque wholes `<a>` and `<ab>` in reading L | No instances implies observational collapse; F additionally retains `<>` |
| S(3) | Require the two indicated data to be separated | Cost-two minimum in the declared item grammar; arity price selects the unary minimum up to source isomorphism |
| S(4) | Apply a specified closure policy to remaining demands | Source closure results under that policy; no universal carrier size |
| S(5) | Issue a further continuation request | Recorded policy input |
| S(6) | Supply an extension and recover its old image | Later section/partial-inverse construction |

The initial `<>` occupies two ASCII bytes and one presentation-token slot.
Neither count is the number of admitted data. In the source, `<ab>` is opaque;
in `sn.ebnf`, the same bytes encode a pair. These are distinct parsers.
The pair interpretation cannot be read back into the original event history.

For a form-less and instance-less source regime, at most one admitted item
cannot distinguish two data. One form and one instance attain separation.
Under item count these tie across different arities. Under the lexicographic
pair (item count, new-form arity sum), a unary mark gives `(2,1)` and the
source proves the appropriate uniqueness up to isomorphism. This does not
identify the minimum with a binary directed edge.

## 3. Endpoints, observations and refinement

Let R be a supplied irreflexive relation. From R(a,b), equality a=b would
contradict irreflexivity, so the support of that pair has exactly two elements:

\[
R(a,b)\Longrightarrow a\ne b,\qquad |\{a,b\}|=2.
\]

This counts endpoints. A single occurrence can witness the relation, both
endpoints may already exist, and the cost of admitting a distinction depends
on the event grammar. For the pointed two-element directed graph D₂, mapping
its distinguished points to a,b determines a unique edge-preserving function.
This statement specifies relation-preserving maps; it does not identify every
possible notion of witness or morphism.

If q:A→O collapses a demanded pair, choose a tag t with t(a)=0 and t(b)=1.
On a finite decidable carrier such a tag is explicit. Set

\[
q'(x)=(q(x),t(x)),\qquad \operatorname{pr}_1q'=q.
\]

The old observation is retained and that pair is separated. Several demanded
pairs require a colouring of their conflict graph. The minimum tag alphabet
is the graph's chromatic number; it is a cost in this declared response class.
[Example E10](levels/level_10_spectral_epistemic_quarantine.md) gives a finite
calculation, independently of the source's form/instance item cost.

## 4. Exact recovery and future operations

For an injection u:A→B with decidable image and an explicit inverse on that
image, define

\[
\widehat r:B\to A\sqcup\{\mathrm{NON\_DESCENT}\},\qquad
\widehat r(u(x))=\mathrm{inl}(x).
\]

Outside the image return refusal. For u(x)=(x,0), test the second coordinate
before recovering x. A total projection (x,y)↦x is a different map, since it
forgets y without refusing. The typed composite above is not an ordinary
identity B→B, nor does it establish an adjunction. Preserving future admitted
events additionally requires the relevant transition squares to commute.

The local Lean proof is `old_image_base` on the explicitly declared flat base
syntax. Its source type excludes nested lifts, retractions and refusal terms.
The Python example uses the zero-new-coordinate image. Each proves or checks
its own construction; neither is silently substituted for a source replay.

The construction index n is also distinct from Postnikov depth j. For j≥0,
Postnikov truncations of a fixed space preserve π₀. An empty space followed by
a point cannot be two such truncations of one space. If a topological
realization is supplied, write P_j(ρ(S(n))) and state its own hypotheses.

## 5. Active demands, retained evidence and ordered history

Let W_n be a finite set of unresolved demand receipts, and set s_n=|W_n|.
Let D_{n+1}⊆W_n be discharged receipts and let B_{n+1} be new receipts,
disjoint from W_n minus D_{n+1}. Then

\[
W_{n+1}=(W_n\setminus D_{n+1})\sqcup B_{n+1},\qquad
s_{n+1}=s_n-|D_{n+1}|+|B_{n+1}|.
\]

The persistent receipt set H grows by union; the event history is an ordered
list and retains repetitions. The displayed sequence `(0,1,1,1,0,1,1)` is a
prescribed exercise history. Its “unconsumed mark”, “unclosed orbit” and
“descent gap” entries require actual issued demands; they do not follow from
a mark or a table of stage names. A completed separation of the only pair
leaves no separation demand unless another demand is supplied.

Lift size counts newly introduced operators under a specified cost convention.
It is independent of survivor change, endpoint count and witness multiplicity.
A homology class in an interpretation is an obstruction to the stated repair
problem, not automatically a receipt in W_n.

## 6. Continuing through finite mathematics

The [level index](levels/README.md) collects the source-oriented lessons and
finite examples. E10–E21 cover refinement, confluence, circulation, termination,
quantifiers, proof scope, partial descent, encodings, optimization, torsion,
observer completion and independent repairs. Their legacy filenames are kept
for links; the numbers are lesson identifiers, not derived Genesis stages.

For each extraction into a mathematics crate, retain the construction,
operations, equality convention and protected questions, and prove the
correspondence being used. A diagram, name or matching dimension does not
supply that correspondence. This is the concrete route from the admitted
primitives through WDP to reusable mathematics.

## 7. Verification entry points

See [code/README.md](code/README.md) for actual module scopes and commands.
`check_sn.py` checks grammar cases; `sn_audit.py` checks syntax, finite relation
examples and contract shape; the Lean files prove their stated elementary
syntax and image-recovery facts. The source's own derivation proofs remain
separate evidence. Passing grammar cases does not check a cochain calculation,
an authorization credential, or the contents of a continuation receipt.
