# Finite observer descent: category, criterion, and constrained countermodel

AuthorityEffect: None. This note supplies a declared finite model for
`WDP-CH11-O01`; it does not assert gluing for every possible observer, partial
comparison map, empirical measurement scenario, or physical report family.
The canonical manuscript and claim ledger are unchanged by this note.

## 1. The site and its coverage

Fix a finite carrier X and a finite family B of subsets containing the empty
set and X and closed under binary intersection. Objects of C are U in B, with
one arrow V -> U exactly when V is a subset of U. Identity and composition are
ordinary inclusions, so C is a genuine finite category. A covering family of U
is a finite family (U_i -> U) whose union is U. This is a Grothendieck
pretopology:

1. The identity cover {U -> U} has union U.
2. Pulling a cover back along V -> U gives (U_i intersect V -> V). These
   objects exist by intersection closure, and their union is V.
3. Replacing each U_i by a cover (U_ij) gives a composite cover because the
   union over i,j is the union over i of U_i, namely U.

An empty family covers the empty object. The site need not contain every
subset of X, and it does not assume a temporal ordering of its carrier.

For each U, declare a finite report set F(U), possibly empty. For each inclusion
V subset U, declare a total transport/restriction map rho(U,V):F(U)->F(V).
Require rho(U,U)=id and rho(V,W) rho(U,V)=rho(U,W). These requirements make F
an actual contravariant functor C^op -> FinSet, hence a presheaf. They are
validated at every section in the native implementation. Missing, partially
defined, mistyped, or incoherent transports are typed refusals; they are not
silently completed or interpreted as a presheaf.

The observer-presentation category in this model is the above context category
with its declared finite report presentations and coherent transports. Its
category of elements is also explicit: objects are pairs (U,s), and an arrow
(V,t)->(U,s) exists exactly when V subset U and t=rho(U,V)(s). Transport
coherence proves composition and identity for this presentation category.

## 2. General finite descent criterion

For a cover (U_i) of U, its matching-family set is

M(F,(U_i)) = { (s_i) in product_i F(U_i) :
  rho(U_i,U_i intersect U_j)(s_i)
  = rho(U_j,U_i intersect U_j)(s_j) for all i,j }.

Functoriality ensures that the restriction map

R:F(U)->M(F,(U_i)),  s |-> (rho(U,U_i)(s))_i

is well-defined: both overlap restrictions of a global section equal
rho(U,U_i intersect U_j)(s). For a fixed supplied matching family m, all global
extensions are exactly the fiber R^-1(m). Therefore:

- Fiber size zero is an existence obstruction.
- Fiber size one gives existence and a unique global report.
- Fiber size greater than one gives existence with a typed ambiguity witness.

The presheaf is separated for this cover iff R is injective, has the existence
part of descent iff R is surjective, and satisfies the sheaf condition for this
cover iff R is bijective. These are equivalences, not sufficient conditions
whose converses are left open. In particular, the full site sheaf condition
requires this bijectivity for every covering family, including the empty cover
of the empty object.

**Proof.** Injectivity says two global reports restricting to the same matching
family are equal. Surjectivity says each matching family has a global
extension. Combining the two gives exactly one extension per family, and
exactly one extension per family implies both. The finite algorithm checks all
Cartesian-product tuples, retains precisely those passing all overlap tests,
and enumerates every section of F(U) in each fiber. Thus it decides all three
conditions without assuming a gluing law. An explicit Cartesian-product limit
is checked before enumeration. Exceeding it is a typed resource refusal,
never evidence of an empty fiber, separatedness, or a sheaf property.

This criterion also covers nonseparated presheaves. For example, take
F(empty)=F({x})=F({y})={*}, F({x,y})={g0,g1}, and let every proper restriction
be the unique map. The singleton cover has one matching family with two
global extensions. Identity and composition hold, so the ambiguity is real,
not a malformed diagram. The native owner includes this example.

## 3. Constrained observer charts and exact gluing membership

The WDP adapter specializes the criterion to constrained pointwise reports.
Each U has a finite family A_U of admissible functions U->D_U and an injective
decoding d_U:D_U->D into a shared value set. The decoding is defined on every
symbol appearing in an admissible report. Distinct reports must decode to
distinct functions. Let F(U) be the decoded admissible family in D^U.

For every V subset U, require the pointwise restriction of every member of
F(U) to belong to F(V). Transport in chart labels is consequently: decode in
U, restrict to V, then uniquely identify the report in V's declared family.
This transport is total. Identity holds because decoded reports are distinct;
composition holds because successive pointwise restrictions equal direct
restriction, and target decoding is injective. These facts are also checked
by the generic native presheaf constructor.

For a compatible fixed family (s_i), define g(x)=s_i(x) for any covering
context containing x. Compatibility makes this independent of i, and coverage
ensures every x in U receives a value. Then g restricts to every s_i. If h has
the same restrictions, choose a context containing x; h(x)=s_i(x)=g(x), so h=g.
Consequently the constrained presheaf is separated for every union cover, and

**A fixed compatible family glues in F(U) iff its unique pointwise union g
belongs to the declared admissible family F(U).**

This is the exact extra condition beyond the unconstrained function-sheaf
result. Equivalently, the sheaf condition for a cover holds iff F(U) equals the
compatible relational join of the declared local families F(U_i). Arbitrary
nonlocal global constraints need not satisfy that equality. Local
satisfiability alone, or existence of some compatible choices in a proper
subfamily, does not establish compatibility of the particular supplied
sections or admissibility of their pointwise union.

If the site contains all singleton objects with singleton covers of every
context, the all-cover sheaf condition further forces each F(U) to be precisely
the product of its singleton allowed-value families (with the unique empty
report). The present model does not assume that factorization.

## 4. Complete constrained countermodel and its classification

Let X={x,y} and B={empty,{x},{y},X}. Use these report families in shared values
{0,1}:

| Context | Admissible decoded reports |
| --- | --- |
| empty | the empty report |
| {x} | x=0; x=1 |
| {y} | y=0; y=1 |
| X | (x=0,y=0); (x=1,y=1) |

Every family is restriction closed. Global reports satisfy the nonlocal
constraint x=y. One chart may encode 0/1 as off/on, another as false/true, and
the global chart as zero/one; injective decoding into shared 0/1 yields coherent
transport despite distinct local spellings.

For the singleton cover, every pair is compatible because its overlap is empty
and both restrictions give the unique empty report. The fibers are:

| Fixed x-report | Fixed y-report | Global fiber |
| --- | --- | --- |
| 0 | 0 | unique 00 |
| 0 | 1 | empty: union violates x=y |
| 1 | 0 | empty: union violates x=y |
| 1 | 1 | unique 11 |

Thus this is a real finite presheaf, separated for the cover, with two exact
existence obstructions. It refutes unconditional gluing of compatible reports
in constrained observer families. Adding 01 and 10 to F(X) produces the full
function-family model and restores unique gluing for this cover.

All distinct-object union covers in this four-object countermodel are also
classified natively: there are 16 valid target/cover pairs. Exactly two fail
the existence part: the cover {{x},{y}} of X and that same cover with the empty
object added. Every cover containing X itself glues uniquely because it
already supplies a global report; covers of singleton or empty targets also
glue uniquely. Repeated members of a cover add only redundant identical
restrictions and do not change the criterion.

## 5. Implementation, replay binding, and checked evidence

Native mathematical owner:

- `omega_category_theory/src/finite_report_descent.rs` owns the finite site,
  total coherent restriction validation, matching families, all global fibers,
  separatedness/existence/sheaf-cover decisions and generic ambiguity model.
- Contexts use u64 subset masks (at most 64 named carrier points). Report sets
  use numbered sections. These implementation limits do not change the
  mathematical theorem; resource refusals remain explicit.

Thin WDP adapter:

- `omega_wdp/src/observer_site.rs` validates actual context domains, injective
  chart decoding, distinct admissible report families and restriction closure.
  It translates names into the generic owner and decodes the fixed compatible
  union. It preserves the declared global constraints.
- Replay takes the actual site, actual target, actual cover and actual local
  section indices as separate arguments and recomputes the complete receipt.
  Changing candidate constraints, a section, overlap data, a fiber, or the
  gluing outcome cannot transfer evidence to a different problem.
- All receipts carry AuthorityEffect::None. Physical observer adequacy and
  governance conclusions are not fields that arithmetic can establish.

Independent paper reference:

- `code/witnessed_difference/finite_observer_descent.py` checks constrained
  assignment families and independently enumerates their matching fibers.
- `code/unit_tests/test_finite_observer_descent.py` checks the two zero/two
  singleton fibers, restoration by all four assignments, empty-cover law,
  actual overlap disagreement, and refusal of non-restriction-closed families.

Core-only Lean evidence:

- `lean4/WitnessedDifference/ObserverDescent.lean` proves the general abstract
  sheaf iff existence-and-separated criterion, pointwise union restriction,
  uniqueness, constrained existence iff union admissibility, and compatibility
  plus nonexistence for the Boolean equality countermodel.
- An explicit cover-selector supplies membership witnesses, so no choice is
  required. Four theorem declarations are axiom-free. Pointwise-function
  uniqueness and constrained membership equivalence use only Quot.sound
  through function extensionality. No Classical.choice, sorry, axiom stub,
  finite-enumeration proof, or cohomological theorem is claimed.

Scoped production commands (run sequentially):

```text
cargo +stable test -p omega_category_theory --lib finite_report_descent::tests --offline -j 2
cargo +stable test -p omega_wdp --lib observer_site::tests --offline -j 2
python -m pytest -o addopts='' code/unit_tests/test_finite_observer_descent.py -q
lean lean4/WitnessedDifference/ObserverDescent.lean
```

Commands use the existing workspace Cargo manifest and pinned task toolchains.
The Python command uses the established repository virtual environment. Native
owner tests cover the generic failure/ambiguity/coherence/resource cases and
every distinct union cover of the countermodel; WDP tests cover chart transport,
actual constraints, restored gluing, malformed report families and forged
receipts. The Lean file can be checked standalone; registration in the central
Lean aggregator and claim maps is a separate root-owned packaging action.

## 6. Exact conclusion and remaining scope

For the declared finite site and presheaf, descent is fully classified by
fibers of the checked global restriction map. For constrained pointwise
observer charts, uniqueness is automatic and existence is exactly target
admissibility of the compatible union. The supplied countermodel disproves
the stronger unconditional gluing claim while the native classifier determines
precisely which covers fail.

No additive structure is assumed, so these typed obstructions are not identified
with a homology or Cech cohomology class. Such an identification needs a
declared linear/additive coefficient system and an additional comparison proof.
The result also neither extends partial transports nor derives report
constraints, physical calibration, a measurement scenario, empirical
contextuality, or observer authority from primitive difference.
