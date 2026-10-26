# Complete declared finite classifications for CH03-O02 and CH14-O01

Status: conditional mathematical results, `AuthorityEffect: None`. This note fixes
predicate meanings from the manuscript and existing native APIs before proving
implications. It does not claim that every interpretation of either open claim
has been resolved. No phenomenology, physical truth, stochastic independence,
clock, or component-selection principle is assumed or concluded.

## 1. Retention vocabulary and exact scope

The manuscript §3.3 defines **data** `(M,u,r,≈)`, with `u:M×I→M` and `r:M→O`.
Data components are not propositions. A question about their independence needs
specified predicates and regularity assumptions. We classify the existing
`RetentionPropertyVector` meanings, adding the active-update predicate used by
CM1. Assume a finite nonempty `M`, total deterministic updates, total readout,
and a comparison whose reflexive symmetric interpretation is an **equivalence
on realized reports**. Recognition is therefore represented by `e:O→P` on
realized reports; write `q=e∘r`. We make no equivalence claim for arbitrary
nontransitive tolerance. The existing native quotient rejects that case.

The six predicates are:

| Symbol | Exact predicate | Existing API |
|---|---|---|
| N | `|M|>1` | `is_nontrivial_carrier` |
| V | Every `u_i:M→M` is a permutation | `is_fully_reversible` |
| O | Raw readout `r` is injective | `is_observable` |
| T | Distinct realized raw reports are recognized together | `has_nontrivial_tolerance` |
| K | Distinct states have different readouts along some finite input word | `is_minimal` |
| A | Some `u_i(m)≠m` | Additional predicate capturing CM1 |

`K` uses the comparison quotient, not literal raw-report equality. This matters:
`O` alone does not force `K` when tolerance identifies distinct raw reports.
The input alphabet may be empty in an audited model; our existential witnesses
use one input. Cardinalities and alphabets are not fixed in advance. Fixed
carrier size or a mandated empty alphabet can impose additional restrictions.

### Complete necessity and sufficiency theorem

A six-bit signature occurs in this class **iff**:

1. If `¬N`, then `(V,O,T,K,A)=(1,1,0,1,0)`.
2. If `O∧¬T`, then `K`.
3. If `¬A`, then `V` and `K↔(O∧¬T)`.

These conditions allow exactly **19 signatures**: the singleton signature,
14 active signatures on nontrivial carriers, and four inactive signatures on
nontrivial carriers. Forgetting `A` yields exactly **15 five-bit signatures**.
Thus these conditions describe the complete Boolean implication theory of the
specified predicates, not just implications noticed in a bounded enumeration.

**Universal necessity proof.** On a singleton every total update is identity,
every report is injective, and no distinct realized raw reports exist. Its
behavioral quotient has one class. Next, `q` is injective iff `O∧¬T`: equality
of raw reports entails equality of recognized reports, and any identification
of different raw reports is precisely `T`. Immediate recognized injectivity
separates every distinct state using the empty input word, giving `K`. If `¬A`,
all updates are identities, so every word leaves each state unchanged. Behavioral
equality is then exactly equality of `q`, giving `K↔(O∧¬T)`; identities are
permutations. These arguments apply to arbitrary finite carrier sizes and all
finite input alphabets, rather than being inferred from enumerated examples.

**Constructive sufficiency proof.** The following rows fix raw and recognized
readouts. All labels are merely finite identifiers.

| Required O,T,K | Raw r | Recognized q |
|---|---|---|
| 1,0,1 | `01` | `01` |
| 0,0,1 | `001` | `001` |
| 1,1,1 | `012` | `001` |
| 0,1,1 | `0012` | `0001` |
| 1,1,0 | `01` | `00` |
| 0,0,0 | `00` | `00` |
| 0,1,0 | `001` | `000` |

For every permitted inactive signature, use identity updates. The constraints
allow only rows where recognized injectivity exactly matches `K`, so this works.
For active reversible signatures, use the cycle on the listed states. In a
`K=1` row, the recognized word `0…01` has distinct rotations; each state sees
its unique `1` at a distinct position, so all states are behaviorally distinct.
For active irreversible signatures with `K=1`, use `i↦min(i+1,n−1)`. Each state
first reports `1` after a different number of steps, proving minimality; the
last two states have the same successor, proving irreversibility. For active
irreversible signatures with `K=0`, reset every state to zero. In every `K=0`
row all recognized reports are constant, so no dynamics can distinguish states.
The singleton witness is the one-state identity model. These constructions
realize **every permitted signature**, with at most four states.

This proves, among other separations, that full reversibility need not imply
active updates, that faithful current readout need not imply reversibility,
and that noninjective immediate readouts can still give a minimal behavioral
system. Selection of `u`, `r`, or `≈` from primitive difference is not supplied.
The data-component independence question without these invariant definitions,
or with arbitrary tolerance, is still a different obligation.

## 2. Functional self-presentation: fix the bridges before classifying

Manuscript §14.2 states R1: report linked to accessible self-state; R2: report
stable under context transport; R3: evaluator can compare report with later
behavior or state. The existing native audit accepts `q:X→P`, `h:P→R`, optional
context `t`, and optional target table. It therefore **presumes** the report
`s=hq`; linkage is structural. Its `is_context_stable` flag checks **presentation
stability** `q∘t=q`, rather than the manuscript's report stability `s∘t=s`.
Its missing context entries default to identity and missing target entries to
the report itself. Those defaults cannot establish either open claim.

Our checked adapter requires complete context and target maps, refuses missing
or surplus entries and duplicate carrier names, and reports the two stability
predicates separately. It still interoperates with the existing audit after
these stronger input checks; it does not change that audit's historical meaning.

### Explicit general finite-map interpretation

Take a finite nonempty accessible state carrier `X` and total maps
`q:X→P`, **independently declared** report `s:X→R`, context `t:X→X`, and declared
state/behavior target `b:X→R`. Define:

- F: `s` factors through the realized presentation `q(X)`.
- P: `q(t(x))=q(x)` for every state (presentation stability).
- S: `s(t(x))=s(x)` for every state (the manuscript's report stability).
- C: `s(x)=b(x)` for every state (exact declared calibration success).
- B: `q` has a collision between distinct accessible states (presentation blind spot).

Factorization F is equivalent to `q(x)=q(y)⇒s(x)=s(y)`. Necessity follows by
applying the factor map. For sufficiency, define the factor at each realized
presentation by the report of any state in its fiber; fiber constancy makes
this well-defined. The native owner returns and checks that finite factor map.
The report alphabet need not be numeric: C is exact label comparison, not an
uncertainty estimate.

### Complete classification theorem

A five-bit `(F,P,S,C,B)` signature occurs **iff**

`¬B⇒F` and `F∧P⇒S`.

There are exactly **20 realizable signatures**. Forgetting the extra diagnostic
P leaves exactly **12 `(F,S,C,B)` signatures**, with the sole constraint
`¬B⇒F`. There is consequently no further universally valid Boolean constraint
among these specified predicates.

**Universal necessity.** If q is injective, every report is constant on its
singleton fibers and therefore factors. If `s=hq` and q is context-stable,
then `s(t(x))=h(q(t(x)))=h(q(x))=s(x)`. No premise about the target b occurs in
either argument.

**Constructive sufficiency.** Use `X={0,1}` with `q=01` if `¬B`, and
`X={0,1,2}` with `q=001` if `B`. Choose `(s,t)` from this complete table:

| B,F,P,S | s | t |
|---|---|---|
| 0,1,1,1 | `01` | `01` |
| 0,1,0,1 | `00` | `11` |
| 0,1,0,0 | `01` | `11` |
| 1,1,1,1 | `001` | `012` |
| 1,1,0,1 | `000` | `212` |
| 1,1,0,0 | `001` | `212` |
| 1,0,1,1 | `010` | `012` |
| 1,0,1,0 | `010` | `112` |
| 1,0,0,1 | `010` | `212` |
| 1,0,0,0 | `012` | `212` |

Every table entry is verified directly by fiber equality and the displayed
context map. For each row independently, set `b=s` to obtain C, or change `b(0)`
to a distinct report label to obtain `¬C`. Thus every permitted signature has
an explicit model of at most three states. This constructive argument proves
completeness across arbitrary finite sizes; tests of small models corroborate
necessity rather than substituting for its proof.

### Ambiguities and boundaries that cannot be hidden

1. **R1 is not defined as factorization through q in the manuscript.** It says
   linkage to accessible self-state. If access includes richer state than q,
   a report can distinguish q-collisions while still being linked to that richer
   state. F is the explicit *report-through-presentation* bridge; the existing
   `h:P→R` API embodies it. Neither the original broad R1 nor self-witnessing
   accepted E-observation provenance is established merely by these finite maps.
2. **R3 comparison ability is not C calibration success.** A checker can compare
   two different values and reject. In our class total b and exact comparison
   make comparison availability structural; C records its success. To classify
   failure of R3 availability, the evaluator/protocol and its admissible domain
   must be separately specified. Missing b is an untyped prerequisite, not a
   proof of `¬C`. The existing `max_calibration_error` counts report/target
   mismatches; it is not measurement uncertainty or physical truth.
3. **Later targets require a declared replay bridge.** A later target can be
   represented as `b=k∘t` only when that factorization is supplied. If that is
   mandated, the additional constraint can alter the classification. Our b is
   a total declared state/behavior target, matching the current ground-truth API.
4. **Blind spots are relative to q.** If F and B hold, the report shares a blind
   spot. An unlinked report may inspect additional state and distinguish it;
   this does not refute the presentation blind-spot proposition CH14-P01.
5. Exact calibration transfers factorization from report to target and back:
   `C⇒(F(s)↔F(b))`. Thus if a prescribed target separates a q-fiber, no linked
   report can be calibrated to that target. This extra hypothesis is not silently
   included in the five-bit theorem.
6. No awareness, evaluator standing, physical calibration traceability, or
   authority effect is inferred. Both original open claims retain these stated
   vocabulary/regularity boundaries; this is a complete *declared subclass*
   result, rather than an unqualified resolution of all readings.

## 3. Implementation, proof coverage, and reproducible checks

Production math owner:
`omega_category_theory/src/finite_functional_classification.rs`. It uses private
checked map carriers and delegates behavioral quotient mathematics to the
existing `finite_moore` owner. Production WDP adapter:
`omega_wdp/src/functional_classification.rs`. It round-trips all retention
signatures through the existing packet constructor and property-vector audit,
requires owner/legacy invariant agreement, and adapts the original functional
observer packet without missing-field defaults. No Python FFI facade or solver
fallback was introduced. The sovereign owner also exposes complete literal-
implication queries: `retention_implication_countermodel` and
`functional_implication_countermodel`. A failed implication returns a checked
actual finite model, rather than only a Boolean pattern. Absence of a witness
is justified by the complete universal classification above, including its
constructive sufficiency, rather than an assumed search-size bound. Invalid
property indices are refused; contradictory premises entail vacuously.

Hermetic executable reference: `code/functional_classification.py`, with
`code/unit_tests/test_functional_classification.py`. The Python retention witness
uses unary pair-orbit replay through at most `|M|²` pair states; it does not claim
to implement the production arbitrary-alphabet Moore quotient. Universal lemmas:
`lean4/WitnessedDifference/FunctionalClassification.lean`. Its 11 checked theorems
prove linking, stability transfer, calibrated-link transfer, inherited blind
spots, recognized injectivity, behavioral minimality, inactive behavior, and
singleton consequences. Two case-splitting lemmas use standard Lean
`propext/Classical.choice/Quot.sound`; the remaining nine list no axioms. No
`sorry`, custom axiom, external solver, or generated hash-as-proof occurs.
Constructive completeness is proved in this note and corroborated by both
native and Python witness checks; the full 19/20-signature sufficiency theorem
has not been encoded as a single Lean theorem.

Validated scoped commands:

```bash
cargo test -p omega_category_theory --test finite_functional_classification --locked --offline
cargo test -p omega_wdp --test functional_classification --locked --offline
python -m pytest -o addopts='' code/unit_tests/test_functional_classification.py -q
python -m ruff check --select F401,F841,I code/functional_classification.py code/unit_tests/test_functional_classification.py
```

Native results: five owner tests and four adapter tests passed. Python: five
scoped tests passed; targeted Ruff passed. The owner/Python checks cover all
64 retention signatures and all 32 functional signatures, verify every positive
constructor and every negative criterion, and independently audit all binary
presentation/report/target assignments and all total context maps on 1–3 states.
Native tests additionally reject incomplete domains, nontransitive comparison,
mutated packet tables, and report-on-presentation omissions.

Lean was compiled with the installed Lean 4.33.1 binary, first building the
unchanged `BehavioralQuotient` import to an external scratch directory, then
compiling this new module with that directory in `LEAN_PATH`. These two files
need no mathlib download. Central root imports and deposit census registration
are left to the parent integration task; no canonical manuscript, ledger,
education chapter, Cargo registration, or existing proof file is edited here.
