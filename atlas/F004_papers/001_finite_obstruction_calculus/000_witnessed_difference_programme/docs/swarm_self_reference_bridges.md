# CH14 follow-on: explicit self-state and partial protocol bridges

This extends `swarm_functional_classification.md` rather than replacing its
five-bit theorem. It addresses the missing R1/R2/R3 parameters from manuscript
§§14.1–14.2 with explicit finite maps, exact iff criteria, constructive witness
plans, and an actual accepted E-observation instance. All conclusions are
conditional on the declared finite tables and carry `AuthorityEffect: None`.

## 1. Parameters and meanings from the original obligation

Let X be a finite nonempty carrier of states of one identified observer O.
Declare accessible self-state `sigma:X→A` and its presentation `q:A→P`. Keep
these different: access to sigma can be richer than access to `q∘sigma`.
Declare an independent **partial report** `r:X⇀R`, a total context transport
`t:X→X`, a total later-state map `l:X→X`, and a partial later-state target
`b:X⇀R`. Every partial map has an explicit undefined value at every missing
point; absent table rows are malformed inputs, not undefined reports or default
identity transports.

Declare a finite generation relation `G⊆A×R`. This is an independent semantic
model of which reports can be generated from an accessible self-state. It is
not inferred from a hash, provenance claim, or the existence of r. G may be
functional or nondeterministic; that regularity is checked separately.

A candidate reflexive provenance link at x contains:

- source and target observer identities;
- captured and independently re-accessed accessible-state identities;
- the reported-value identity.

The model checks it against O, sigma(x), the **actual** r(x), and G. A checked
link must have both observer identities O, both accessible-state identities
sigma(x), its report equal to r(x), and `(sigma(x),r(x))∈G`. A supplied but stale,
foreign, mismatched, or unsupported record does not establish R1. This is finite
semantic provenance; actual retained-artifact custody and evaluator standing
are stronger prerequisites handled by the E-observation bridge in §5 below.

Finally declare a partial equality-comparison protocol: an identified evaluator
and finite domain `D⊆R×R`. The protocol is executable only on admitted pairs;
where executed, it compares exact report identities for equality. Its domain
and existence are independent of whether the values happen to agree. No
probability, confidence level, physical truth, or metrological traceability is
inferred from this declared comparator. Other comparator semantics require
another explicitly supplied comparison relation.

## 2. Exact eventwise criteria: availability versus success

At each x:

| Question | Exact criterion |
|---|---|
| A report exists | `r(x)` is defined |
| Linkage candidate provided | report and provenance candidate both exist |
| R1 linkage verified | the identity/state/report/generation checks above all hold |
| R2 comparison across context is available | `r(x)` and `r(t(x))` are defined |
| R2 report remains stable | availability holds and `r(x)=r(t(x))` |
| R3 later comparison is available | `r(x)=v`, `b(l(x))=w`, protocol exists, and `(v,w)∈D` |
| Later comparison succeeds | R3 availability holds and `v=w` |

These are independently replayed finite predicates. They are not promises
attached to an unchecked receipt. A target that is undefined cannot be a
successful comparison; two undefined reports do not count as an available
report event.

For the original R2 on the **domain of actual report events**, use

`E(t,r): ∀x,v, r(x)=v ⇒ r(t(x))=v`.

This is exposed as `report_events_preserved`. It does **not** require a report
at every state. For example, reports `(0,undefined)` under identity transport
preserve every actual report event, while universal comparison availability is
false. Sending the reporting state to the undefined state refutes E. Thus the
partial-report case is not silently converted to the earlier total-map class.
For total t, universal R2 availability is equivalent to report totality, and
universal successful stability is exactly `ReportTotal(r) ∧ E(t,r)`. Both
statements are kernel-checked in Lean.

### Complete aggregate classification

For the stronger all-declared-states diagnostic tuple

`(ReportTotal, LinkProvided, LinkVerified, StableSuccess, CompareAvailable, CompareSuccess)`

the exact realizability criterion is:

1. If ReportTotal is false, every other universal predicate is false.
2. If ReportTotal is true, LinkVerified implies LinkProvided, and CompareSuccess
   implies CompareAvailable; there are no other Boolean constraints.

There are exactly **19 signatures**: one partial-report signature, and
`3 linkage states × 2 stability states × 3 comparison states = 18` total-report
signatures. The native and Python constructors realize all permitted signatures
using two states. This theorem concerns the specified universal diagnostics;
it does not discard eventwise R1/R2/R3, which remain directly available at each
state and can be true at one state despite global unavailability elsewhere.

**Universal necessity.** Every verified link, every available stability test,
and every available later comparison contains an actual report. Each successful
comparison contains an available protocol run. These statements imply all
listed constraints without any bound on the number of states.

**Constructive sufficiency.** Use sigma(0)=0, sigma(1)=1, reports `(0,1)` and
G={(0,0),(1,1)}. Identity context gives stable success; swapping the two states
refutes it. Links are either absent, supplied with a foreign source observer,
or exactly reflexive, realizing all three linkage states. Always use the real
later-state swap l(0)=1, l(1)=0. A missing protocol gives comparison unavailability.
A protocol admitting all pairs and target table `(0,1)` makes comparison
available but unequal at both states. The same protocol with target `(1,0)`
makes both later comparisons succeed. These choices are independent. For the
partial-report signature, use `(0,undefined)`, absent links and absent protocol.
All outputs and negative cases are checked independently against their maps.

This supplies explicit refutations of R1⇒R2, R1⇒R3 availability, R2⇒R1,
R3 availability⇒R1, R3 availability⇒comparison success, and successful later
comparison⇒context stability. The failed draft ladder is not restored.

## 3. Determination and the exact later-state factorization bridges

### Rich self-state, provenance, and deterministic generation

A partial report factors through sigma **iff** its Option-valued table is
constant on every sigma-fiber. Undefined values are part of that table; one
undefined and one defined value in the same fiber block a partial decoder.
An explicit finite decoder is returned when the condition holds. The same
criterion applies to the coarser presentation `q∘sigma`.

Verified provenance alone does not imply deterministic report factorization.
For instance, take sigma constant and G={(a,0),(a,1)}; reports 0 and 1 can both
have valid reflexive origin evidence. If G is functional, however, verified
linkage at every state forces report fiber constancy: two equal sigma values
have reports admitted by the same functional G-row and hence equal reports.
That implication is kernel-checked. The functional-G hypothesis is sufficient. It is not necessary for a particular report r to factor: an unused second output in a G-row need not affect the actual reports.

A report linked to richer sigma can distinguish a collision of `q∘sigma`.
The named production fixture uses distinct accessible self-states but a constant
presentation, with successfully linked distinct reports. It satisfies the
original richer-access interpretation of R1 without contradicting the
presentation-only blind-spot proposition CH14-P01.

### Two different later-target questions, both with iff answers

1. A prescribed current-state target `y:X⇀R` can be realized as `k(l(x))` by a
   later-state target k **iff** y is constant on the fibers of l.
2. The actual later target `b(l(x))` can be inferred by a partial accessible-state
   decoder `h(sigma(x))` **iff** the composite `b∘l` is constant on sigma-fibers.

The native owner returns the finite factor map when possible. It refuses
incorrect shapes or out-of-carrier values; a well-typed fiber collision returns
no factor. Both iff results are Lean theorems, not conclusions from a bounded
search. For example, a constant later map cannot realize prescribed targets
0 and 1 at different current states; nor can it realize a defined target at
one state and an undefined target at the other. A constant sigma cannot infer
later targets that differ across its one fiber.

If verified linkage plus functional G makes r factor through sigma, and every
later comparison succeeds, then `r=b∘l`. Thus `b∘l` must factor through sigma.
A later-target collision on a sigma-fiber refutes the combination of those
hypotheses. This obstruction is separate from comparison-protocol unavailability.

## 4. Exact existence criterion under FIXED bridge data

The previous tests do not merely classify abstract predicate patterns. Native
`successful_linked_report_plan` and the named WDP
`plan_successful_self_reports` solve the following actual constructive problem:
keep sigma, G, t, l, b and D fixed; seek a new report table and provenance table
whose linkage verifies and whose later comparisons all succeed.

A solution exists **iff**, for every state x:

- `b(l(x))` is defined, with value v;
- `(sigma(x),v)∈G`;
- an executable protocol exists and `(v,v)∈D`.

If context stability is also required, add
`b(l(t(x)))=b(l(x))` at every state.

**Necessity.** Successful comparison forces `r(x)=b(l(x))`, a defined value.
Verified linkage then forces generation membership, and successful protocol
execution forces diagonal-domain membership. Stable reports force equality
of these composite target values under t.

**Sufficiency.** Set `r(x)=b(l(x))`; fill each provenance record with the same
observer identity, captured/re-accessed sigma(x), and that value. The listed
conditions verify linkage and admit the successful equality comparison. The
additional context equality gives report stability. The native owner constructs
this witness; the named adapter independently re-audits its complete packet.
Planning constructs finite candidate data, not an authorized modification of
an actual observer or proof of physical behavior.

`successful_linked_report_exists_iff` proves the non-stability version directly
in Lean. The stability addendum follows by the same forced-value substitution
and the separately checked stability-preservation theorem; its witness and
negative cases are implemented and tested natively and in Python.

Under functional G, sigma-fiber constancy of b∘l follows from generation
membership, as expected. With nondeterministic G, the linked-report plan can
exist even without such a decoder; the theorem does not add determinism for
free. Missing target, missing generation membership, missing comparator diagonal,
and unstable required context each have distinct checked countermodels.

## 5. Actual accepted self-witnessing event (CH14-D01)

The hermetic Python bridge goes beyond structural reports. It takes an actual
`AcceptedObservation`, revalidates its complete observation receipt, binds its
registration carrier to `self:<observer identity>`, and binds its retained mark
to a typed target payload naming the observer, state index, target component
`accessible_self_state`, accessible self-state, and report. It requires a verified
reflexive link in the finite model and verifies the witness against a **separately
supplied re-accessed mark**.

The tests build Registration→WitnessReceipt→ObservationReceipt→AcceptedObservation
using the paper's existing APIs and verify this reflexive target end to end.
A foreign observer target, changed re-accessed artifact, unavailable provenance,
or correctly hashed Boolean state index in place of an integer is refused.
Structural linkage by itself remains insufficient for an accepted self-witnessing
event: evaluator standing, accepted-observation provenance and artifact replay
are additional checked prerequisites. No phenomenological conclusion follows.

## 6. Files, proof status, and scoped verification

New production owner:
`omega_category_theory/src/finite_self_reference.rs`.
New named adapter: `omega_wdp/src/self_reference_adapter.rs`.
Focused native tests: owner `tests/finite_self_reference.rs` and WDP
`tests/self_reference_adapter.rs`.
Hermetic reference: `code/self_reference_bridges.py` and its targeted test file.
Lean: `lean4/WitnessedDifference/SelfReferenceBridges.lean`.

The Lean file has ten verified theorem declarations, with no `sorry` or custom
axioms. Six list no axioms; the partial-factor and its two later-map corollaries
use the standard `propext/Classical.choice/Quot.sound`, and the fixed-bridge
existence construction uses `Classical.choice`. Complete 19-signature aggregate
sufficiency has a universal proof plus explicit native/Python constructors;
it is not represented as a single Lean bit-enumeration theorem.

Scoped tests exercise all 64 aggregate candidates, all 19 positive witnesses,
negative constraints, per-event partiality, stale/foreign/mismatched provenance,
generation omission, protocol-domain omission, later-map factor collisions,
fixed-bridge planning and mandatory context-stability failures, richer sigma
access than presentation, missing rows, and forged audit flags. The Python
reference also independently enumerates all partial report/target tables, all
context/later maps on two states, and absent/empty/full protocol domains.

The earlier five-bit total-map theorem remains an explicitly named subclass.
This follow-on supplies the missing bridge parameters and exact finite answers
instead of treating the original vocabulary gap as a stopping point. What it
still does not derive is the choice or physical fidelity of sigma, G, transport,
later map, target, evaluator, or reporting protocol. Those are the admitted
parameters of the now-checkable original finite functional problem.
