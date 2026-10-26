# Complete typed observer adapter criteria

## Domain and theorem

The source and target have declared sorts, surjective maps between those sorts,
partial operation symbols, and truth-valued predicate symbols. An operation's
input is a typed tuple of source sorts; its result is either undefined or an
element of its declared output sort. Every field has its actual signature.
An omitted layer is not a zero-valued operation, an empty comparison, a default
terminalizer, or a policy inferred from another layer.

If each coordinate sort map is onto, its induced map on input tuples is onto.
Choosing a preimage independently in each coordinate proves this, including
the nullary tuple. Write an operation's input map as `q:A→B`, its output map
as `p:S→T`, and its source table as `f:A→Option S`. A unique target operation
`g:B→Option T` satisfying

`g(q(a)) = Option.map p (f(a))`

exists **if and only if** equal-`q` input tuples have either both undefined
source outputs, or both defined source outputs with equal-`p` results.

Necessity follows by evaluating `g` on the common target tuple. For sufficiency,
choose a preimage of each target tuple and use its mapped source output;
the fiber condition makes that choice immaterial. Surjectivity gives uniqueness.
`Option.map p value = none` holds exactly when `value = none`, so the equation
preserves **and reflects** definedness. A forward-preserving partial map which
hides a defined operation as undefined does not satisfy this criterion.

A predicate with Boolean truth value descends uniquely exactly when its truth
is constant on input fibers. This proves preservation and reflection of truth,
not only preservation of positive instances. Total reports obey the same
fiber-constancy criterion. Indexed-family theorems establish simultaneous
existence and uniqueness for all declared symbols, with heterogeneous input
and output types. Consequently these tests are necessary and sufficient for
the entire declared many-sorted signature, rather than separate sufficient
heuristics for selected fields.

The algebraic proofs have no finiteness assumption. Finite tables allow their
conditions to be decided exhaustively by the native many-sorted implementation.
For an infinite input type the same theorem remains valid, but finite sampling
does not verify its universally quantified hypotheses.

## Faithful completion and missing-layer recovery

For any onto presentation `q:X→P` and desired semantic field `s:X→L`, a unique
report adapter `P→L` exists exactly when `ker(q) ⊆ ker(s)`. Recovering the
complete original packet requires `s = identity`, and hence requires `q` to
be injective. Semantic recovery can demand less than complete reconstruction;
these claims must not be conflated.

If a presentation loses a required field, the joint report `x↦(q(x),s(x))`
has kernel `ker(q) ∩ ker(s)`. Use its **actual image** as the completion carrier,
rather than the full product with possibly unrealized pairs. This completion
is onto and recovers both fields by projection. An arbitrary onto completion
`c:X→C` recovers both fields exactly when its fibers respect that joint report.
Equivalently, there is a unique map `C→image(q,s)` commuting with the source
reports. This is the complete minimality property of the joint-image completion.
It is a data-preservation construction, not an inference of new source semantics.

The no-recovery statement permits source regularity constraints explicitly.
Let two **admitted** complete packets have identical visible projection but
different missing semantics. Then no function of the visible packet can recover
the missing semantics for every admitted completion: it would give equal
values on the identical projection and unequal values on those two packets.
This does not claim that every constrained missing field necessarily has two
admitted possibilities. A law which uniquely determines a field can remove
the obstruction; such a law must be supplied and verified.

The formal development supplies seven independent finite countermodels:

1. A collapsed Boolean input has undefined and defined singleton outputs.
   The output sort cannot itself cause an output-fiber mismatch here.
2. Both Boolean inputs are defined, but their Boolean outputs differ after
   the declared identity output map. Equal definedness alone is insufficient.
3. All operation data may be retained while a collapsed predicate has two
   different truth values. Operation descent does not imply predicate descent.
4. A non-surjective presentation permits two different extensions on an
   unused target input, while both agree on every source input. Uniqueness
   therefore needs surjectivity or restriction to the actual image.
5. Identity and negating updates on a two-state memory are different actual
   total update functions, indistinguishable when the update field is omitted.
6. Two constant terminalizer functions differ although visible presentation
   data agrees. Their choices are typed data; no assertion that both satisfy
   an arbitrary external certification law is made.
7. Constant `store` and `emit` status-to-action functions are different policies
   with the same retained fields. Policy cannot be recovered from a status
   alone without a declared status-to-action rule.

The generic admitted-completion theorem, rather than the toy finite output
alphabets, is the source-independent result. It specializes to actual source
fields once the allowed domain and its two witnesses are established.

## Recovered original sources and archival scope

Exact original-byte recovery is now successful; the previous custody and
unknown-vocabulary barriers are obsolete. The authoritative recovery report
is [`source_recovery_report.md`](source_recovery_report.md). The original
Genesis observer at source part 001 lines 983–1004 is `(M,U,p,rho,G,T)`, not
the education tuple `(C,p,~,W,V,tau)`. It has an initial memory state and
`rho:C×D*→D*`, where histories have unbounded length. The normalized nine-field
observer and the operational/self-observer source also retain their distinct
actual types. No identification is inferred from tuple arity.

The universal theorem handles these histories algebraically because its input
types are unrestricted. A finite-table executable adapter covers only its
declared finite domain. A claim to execute every original history context
requires an actual history program/transducer and its laws, or a separately
declared finite partial domain; finitely many tested histories do not supply
that proof. The theorem alone also does not prove that each recovered source
family has been instantiated with the correct signature. That is an additional
source-specific audit, separate from generic adapter completeness.

One historical target needs a mathematical disposition rather than a custody
warning. Original part 001 lines 1114 onward proposes that all six components
can independently change O1/O2 classification. The original itself predicts
that grammar `G` and terminalizer `T` are jointly eliminable from this
classification. Its O1/O2 targets depend on `p∘U*` and `rho`, hence holding
those fixed while changing only `G` or `T` cannot change those predicates.
Faithful adaptation may preserve `G,T` as independent interface fields, but
must not promote the stronger six-field **classification-independence** target.
It must instead be refuted/weakened to the stated four-component classification
core with two interface fields. This archival disposition does not obstruct
construction of faithful semantic adapters.

## Formal verification

`lean4/WitnessedDifference/ObserverAdapterCompleteness.lean` compiles standalone
under Lean 4.33.1 with exit code 0. It contains **27 theorem proofs** and a
source-bound explicit declaration census in
`lean4/observer_adapter_completeness_axioms.txt` covering **34** declarations
and constructors. Dependency union is exactly
`{Classical.choice, Quot.sound, propext}`; no custom axiom or admitted proof is
used. The seven concrete countermodels compile as proofs, rather than being
reported solely as numerical examples.

This receipt establishes the new core-only module, not a fresh build of the
older Mathlib-dependent package. Its central root import, claim map, and
canonical claim disposition are handled separately.

## General linear sensing is a distinct adapter

The absorbed PO035 `ObserverHarness` declares arbitrary shaped linear sensing Q; it does **not** require Q d0=0. FOC008's R0=(Pi_fact,Q,kappa) combines joint-law assumptions with a sensing map whose repair blindspot is im(d0) intersect ker(Q). Accordingly `LinearSensingPresentation` in the functional owner retains the actual report matrix R and admissible repair matrix d0 and computes R delta on the full rational defect vector space. It supplies no norm, cost, joint law, tensor decomposition, terminalizer, or repair invariance. Those remain separate source fields. Unlike a finite lookup table, a finite rational matrix defines its linear function for every rational vector, so this is a symbolic exact adapter of an infinite carrier. Real-valued inputs require a separately declared coefficient/number-domain representation; a rational implementation does not silently certify arbitrary floating source values.

**Linear criterion.** Over any field, the sensing map R:E->P induces a function on E/im(d0) exactly when R d0=0. Necessity: 0 and d0 a are in the same class, so their reports must agree; hence R d0 a=0 for every a. Sufficiency: if delta'-delta=d0 a, then R delta'-R delta=R d0 a=0. The induced function is unique because the quotient projection is onto. A report on E is nevertheless well-defined without this condition. Thus the general adapter accepts a visible repair and its separate `try_quotient` request refuses it.

**Supplied blindspot criterion.** Given actual repair parameters a, let h=d0 a and z=R h. Then h is in im(d0) intersect ker(R) exactly when z=0. A *nontrivial* blindspot additionally needs h!=0; nonzero a alone is insufficient when d0 has a kernel. The witness stores the actual parameters, actual h and actual z; verification recomputes both matrix products and both flags. This tests a concrete witness, not a completeness claim about a nullspace basis or the source's real recovery modulus.

The independent countermodel is d0=I_2 and R=(1,0). The source report of (3,7) is 3; visible repair a=(3,0) changes the report, so no quotient report exists. Meanwhile a=(0,7) gives a nonzero blindspot h=(0,7). Both phenomena coexist. The zero repair is blind but not nontrivial. Conversely R=(1,-1), d0=(1,1)^T satisfies R d0=0 and strengthens to the existing exact quotient presentation. These witnesses prevent wrongly treating every general harness as a repair-blind quotient observer.

Native arithmetic and shape checks delegate to `linear_algebra` matrix product. The functional owner independently validates exact rational denominators and canonicalizes coefficients; malformed vectors or matrices receive typed refusals. `adapt_linear_sensing` in the legacy WDP adapter retains this distinct owner object and custody annotations, leaves its quotient-presentation field empty, and preserves all absent layers. Python uses a separately checked exact rational sensing object and exposes the same strengthening and supplied-witness replay. Neither adapter infers archival identity or authority.

Production sensing verification passes: functional `linear_observer_presentation::sensing_tests` **3/3**, WDP `--test linear_sensing_adapter` **1/1**, and the existing functional `--test linear_observer_presentation` quotient regressions **2/2**. Independent Python sensing tests pass **2/2**, and existing semantic legacy adapter regressions pass **8/8**. Ruff checks, rustfmt and scoped diff checks pass.
