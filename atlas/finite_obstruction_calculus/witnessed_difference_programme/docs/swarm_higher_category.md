# CH04-O01: typed routing and a precisely scoped contextual reflector

AuthorityEffect: None. This note supplies a finite mathematical routing interface,
an actual comma-category universal property, and an exact obstruction to the
stronger profile-reflecting completion. It does not grant operational authority,
select a physical observer, identify profiles with consciousness, or reconstruct
quantum theory. The mathematical results do not depend on packaging status.

## The category and its full congruent subcategory

Fix a context alphabet C. An object is S=(X,R,a), where X is a nonempty finite
carrier, R is an equivalence relation (the kernel of a declared profile), and
for each c in C, a_c:X→X is a total operation. Native context labels are fixed
indices; their identities are preserved by every arrow. The Python and Rust
constructors check finite carrier typing and total actions. Lean proves the
algebraic universal property for arbitrary carriers.

A morphism f:S→T is a function f:X→Y satisfying both:

1. x R y implies f(x) R_T f(y);
2. f(a_c(x))=a^T_c(f(x)) for every c and x.

Identity and ordinary function composition satisfy both equations. Arrow
endpoints are part of the checked native type, and composition rejects unmatched
endpoints. Equality of arrows is equality of underlying functions; Lean's
`hom_ext` proves that the proof fields do not introduce extra arrow identities.
These are ordinary categorical laws, rather than a record containing category
labels.

Cong is the full subcategory consisting of those objects for which R is stable
under every context: x R y implies a_c(x) R a_c(y). Profiles need not distinguish
all points. Stability is the intended contextual congruence condition.

## A genuine conditional completion, with its unit and universal property

Let R* be the least equivalence relation containing R and stable under every
context. It exists: the indiscrete relation is such a relation, and intersections
preserve all of these properties. Equivalently, generate R* from R using
reflexivity, symmetry, transitivity, and the rule

    x R* y ⇒ a_c(x) R* a_c(y).

Define L(S)=(X,R*,a), with the *same carrier and operations*. The unit η_S:S→L(S)
is the identity function on X. It is a morphism because R is contained in R*.
L(S) belongs to Cong by construction.

The executable table algorithm additionally requires a finite context alphabet C. The abstract reflector below permits arbitrary C. The native algorithm starts with the declared profile partition. At each round
it merges the successor blocks of every currently related pair under every
context, then closes the partition equivalence and canonicalizes block labels.
Every changed round merges at least two blocks. Hence there are at most |X|-1
strict rounds. At its fixed point the partition is stable. Conversely, every
stable equivalence containing R contains each merge and each equivalence closure
by induction on rounds; therefore the computed relation is exactly R*. The
algorithm does not split blocks or modify context actions.

Now take **any object of the comma category S↓Cong**: a congruent system T and a
morphism f:S→T. We claim there is exactly one morphism g:L(S)→T such that

    g ∘ η_S = f.

Existence is proved by induction on the generation of R*. The base relation is
preserved because f is a morphism. Reflexivity, symmetry and transitivity are
preserved because T's relation is an equivalence. For the context-generation
step, equivariance of f and congruence of T give

    f(a_c(x)) = a^T_c(f(x)) R_T a^T_c(f(y)) = f(a_c(y)).

Consequently the same function f preserves R* and defines g. Equivariance is
unchanged. Uniqueness follows from the triangle and the identity carrier unit:
for every x, g(x)=g(η_S(x))=f(x). This proves **initiality of (L(S),η_S) in
S↓Cong**, with actual typed morphisms and a universal quantifier over all
congruent targets. It is not just a successful finite example or a constructor
disjointness argument.

For an arrow f:S→T, L(f) is the same underlying function between completed
systems. Apply the preceding factorization to η_T∘f. Identity and composition
are preserved, and the units are natural:

    L(f) ∘ η_S = η_T ∘ f.

Thus this construction is a reflector onto Cong. The native tests check the
comma triangles and all candidate factors in declared finite targets, while
Lean proves the general universal property and functor laws.

**Scope that matters:** this reflector coarsens profile equivalence. It may make
formerly distinguishable profiles equivalent. It is not a refinement preserving
or reflecting original reports. Its existence must not be cited as a proof of
the historical minimal-constructor-refinement lemma.

## The stronger profile-reflecting completion is impossible

Suppose a proposed unit η:S→T is a morphism, T is congruent, and η reflects
profiles:

    η(x) R_T η(y) ⇒ x R y.

If x R y, preservation gives η(x) R_T η(y). T's congruence and η's action
commutation give

    η(a_c(x)) R_T η(a_c(y)).

Reflection gives a_c(x) R a_c(y). Therefore S was already congruent.

The contrapositive is an exact no-go theorem: **a noncongruent S has no
profile-reflecting morphism into any congruent T**. In the comma category whose
objects require such reflecting units there are no objects at all, so it has
no initial object. This addresses an actual universal-property claim, without
mistaking a failed factorization example for general categorical nonexistence.

A concrete finite countermodel has X={0,1,2}, profiles p=(0,0,1), one context,
and action a=(0,2,2). We have 0 R 1 but a(0)=0 and a(1)=2 are not related. Thus
no congruent completion with an equivariant, profile-preserving and
profile-reflecting unit exists, irrespective of target size or constructors.
The relation-coarsening reflector instead produces the indiscrete partition.
The distinction between these two unit contracts is essential.

This no-go theorem requires all of its stated arrow conditions. Changing arrow
direction, weakening reflection, or changing the relation notion gives a different
category and requires a different theorem. A profile-splitting behavioral
quotient is not identified with this coarsening reflector.

## Diagnostic-to-routing adapter and guarded changes

`omega_wdp::diagnostic_routing` accepts a declared context system, a submitted
exact Phi1 primal/dual certificate, and a declared d1. It delegates Phi1 replay,
chain-law checking, Gamma2 computation and exact trichotomy classification to
`omega_functional`; the WDP layer does not implement competing optimization.
The context system and cochain complex are independently declared data. A
positive defect does not imply a critical context witness; zero Phi1 does not
rule one out. The tests exhibit routing for all three diagnostic classes under
the same independently checked context witness.

A `RoutingRequest` and `ProposalPolicy` are separate inputs. The typed finite
outcomes are mathematical proposals/refusals:

- Hold retains the diagnostic without making a change.
- A profile-reflecting completion returns identity when the system is already
  congruent, or refuses with an exact critical-context witness by the no-go theorem.
- A relation-coarsening completion requires declared permission and rechecks the
  critical witness before constructing the reflector. It does not reduce Phi1
  by assertion and does not pretend to preserve distinguishable reports.
- A value-edit candidate requires declared edit permission, unchanged d0 and
  weights, the same d1 and context system, fresh certificate replay, and strict
  exact Phi1 decrease. The allowed move changes omega; it does not hide a change
  of weights or the repair operator. Forged certificates and changed contracts
  are errors, and a verified candidate without strict decrease is refused.

The `RoutingReceipt` binds the full diagnostic, policy, request and resulting
proposal. Its replay method recomputes the diagnostics and routing guards. Its
fields are private. No enum submitted by a caller is accepted as proof of a
routing decision, and no receipt carries authority.

For the fixed optimization problem, changing only its repair parameter cannot
strictly lower the *optimal* Phi1: every valid exact certificate of that same
problem has the same primal/dual optimum. Therefore a strict-descent policy
needs a declared change to input values, weights, deletion or admissible repairs.
The implementation selects the finite value-edit contract. It does not claim
pure graph growth evades CH04-P09 or replace operational lift admission.

## Evidence and remaining boundary

New production mathematics lives in
`omega_category_theory/src/context_reflection.rs`, reusing its existing
`finite_moore` carrier checker. WDP naming, policies and diagnostic adaptation live
in `omega_wdp/src/diagnostic_routing.rs`. The paper's hermetic Python reference
is `code/witnessed_difference/context_reflection.py`.

The new core-only Lean file `lean4/WitnessedDifference/ContextReflection.lean`
proves category identities/associativity, generated-congruence preservation,
actual comma initiality, reflector identity/composition and unit naturality,
and the general reflecting-unit no-go plus its three-state countermodel. The
six printed principal theorem axiom reports in
`lean4/context_reflection_axioms.txt` all report **no axioms**. These are fresh
elaboration observations, not claims about all repository proofs.

Targeted validation completed:

- Native category owner: 5 tests passed, including all 135 three-state profile/action systems checked against every stable super-equivalence.
- Native WDP diagnostic routing: 4 tests passed.
- Hermetic Python reference: 3 tests passed; Ruff passed.
- Core-only Lean: successful elaboration; no admissions or extra axioms.

This supplies a typed finite mathematical interface, a valid conditional
completion, and an exact obstruction to the stronger reflecting-unit contract.
It leaves constructor refinements with different morphisms, arbitrary guarded
operational policies, and the CODA authority-bearing terminalizer outside this
proved scope. It does not claim the monograph's broad interface row has no
remaining work.

## Concrete finite terminal/lift/closure routing supplement

`omega_wdp::finite_routing` completes the selected finite terminal/lift interface while preserving `diagnostic_routing`. TerminalPolicy is an explicit three-row partial table indexed by the independently replayed exact/closed/active diagnostic class. Missing policy or row gives typed refusal. A certified terminal must agree with its class; Hold is always permitted. These are mathematical terminals with AuthorityEffect None, not licenses. StabilizedSurvivor requires a separately declared complete finite deterministic update table, source packet binding and actual next(s)=s. ClosedResidual alone is insufficient. A two-state toggle carrying identical diagnostic packets is refused. For a fixed point, induction proves next^n(s)=s for all n in the declared mathematical dynamics; this says nothing about physical stability or an infinite decreasing-run limit.

The generic linear-algebra owner `finite_cochain_map` uses the existing BasicMatrix/Semiring/product owners. A cochain window contains declared dimensions C0,C1,C2 and actual d0,d1 satisfying d1 d0=0. A typed source→target map has actual matrices F0,F1,F2 and is accepted iff e0 F0=F1 d0 and e1 F1=F2 d1. Necessity is the definition of a cochain map; sufficiency transports boundaries and closed vectors, since F1(d0 a)=e0(F0 a) and e1(F1 z)=F2(d1 z)=0 when d1 z=0. Therefore it induces a quotient map on degree-one cohomology over the rational field. No injectivity, surjectivity or norm preservation follows. The WDP lift adapter additionally binds both actual diagnostic windows, independently replays their certificates and checks target omega=F1(source omega). If coordinate inclusion is required, every matrix column must be a distinct standard basis vector. A scaling map is a valid commuting lift but fails inclusion and can double Phi1; both countermodels are executable.

The closure guard requires common context/d0/d1/weights, independently certified before/after defects, strict Phi1 decrease and Gamma_after−Gamma_before ≤ declared nonnegative damage budget. A change from defect (3,0) to (1,1), with zero d0 and d1=(0,1), decreases Phi1 from3 to2 but raises Gamma from0 to1. Budget0 refuses; budget1 accepts. This is an actual closure-damage check; no unstated ratio guard is inferred. Pure repair-potential changes cannot decrease Phi1 of a fixed quotient problem. For any accepted finite sequence, summing its checked inequalities yields Gamma_N ≤ Gamma_0 + sum damage_budget_i, and strict Phi1 descent holds at each step. This finite statement does not prove termination, convergence to zero, stabilization or an infinite-run limit.

Focused evidence: native generic cochain-map test1/1 and WDP routing tests3/3 pass with --locked --offline; Python corresponding routing tests3/3 pass. Core-only `WitnessedDifference/FiniteRouting.lean` proves closed-vector transport, repair transport and declared fixed-point stationarity. `finite_routing_axioms.txt` records principal theorem axioms. The original historical policies are not retrospectively credited: these declared finite contracts are concrete executable completions of the requested interface, with missing inputs refused explicitly.
