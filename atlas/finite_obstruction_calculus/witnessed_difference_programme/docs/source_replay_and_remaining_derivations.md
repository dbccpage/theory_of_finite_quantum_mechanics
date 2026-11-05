# Source replay, context transport and the remaining derivations

AuthorityEffect: None. This supplement advances the five enlarged obligations
without converting finite examples into an end-to-end derivation of every source
system. Original source pins and the canonical 154 claims retain their scopes.

## 1. What was actually replayed

[Source inputs](../manifests/source_replay_inputs.json) pin 24 files, including
the dependency closure of the selected original functions, to Genesis revision
`f1d56c010e6ba10a3b9418bd7cc5953c067250f2` and Genesis Ongoing revision
`5d9488324ce976817987bd83a28d901371cfc073`. These supplement the historical
source manifest; they do not replace its bytes. The replay rejects changed
Git blobs, sizes, hashes, non-regular controls and unbound imported modules,
then checks the input and verifier bytes again after execution.

The [retained source receipt](../evidence/source_replay_receipt.json) contains:

- Three seven-event admission scenarios, with 20, 130 and 69 reached states.
- Every minimum response before isomorphism in the declared two-item,
  arity-at-most-two initial challenge: six for `mu1`, two for `mu2`.
- All 32 enabled one-step changes from three explicitly listed seed-25
  states, covering identification, removal, filling, term addition and
  assertion addition. The empty state and loops are included.
- One actual raising operation and separate seed-15 and seed-16 admission
  checks. These two admission operations have different protected meanings.

The native test
[`genesis_source_replay.rs`](../../../../../../omega_engine/crates_rs/tests/omega_wdp/genesis_source_replay.rs)
compares every before/after excess, marked diagnostic and balance flag against
these independently executed source cases. It also checks the source's chosen
seed-22 plain-state price and independently counts the enabled one-step
alternatives. It does not execute the original transition system in Rust.

The later [source execution refinement](source_execution_refinement.md)
adds a Rust kernel for all five canonical seed-25 changes. Its separate
oracle executes 3,770 original transitions from 266 complete raw states
and checks native outputs, ordering, histories and prices. A new universal
finite-sum proof justifies raw pair aggregation; its declared partial-run
model preserves every history length. This advances the selected seed-25
branch without closing the obligation for every original source system.

## 2. The initial challenge floor and its alternatives

The challenged source state has two admitted opaque data, no forms, no
instances, no rules, and a requirement that their observation profiles differ.
With no form, there is no context, so the empty response fails. One new datum
does not add a context. One bare form has no derivable instances. An instance
or rule cannot name an absent form. Thus no admissible response of at most
one item separates the profiles.

Two items suffice: admit one form of arity `k >= 1`, then one instance. A
context whose hole occupies any selected argument distinguishes the datum
appearing there from the other datum. Within the stated arity bound, the two
unary instances and four binary instances give exactly six responses. Every
other two-item shape either lacks an instance or adds a universal rule, which
gives both data the same profile. All six have raw item cost two. Lexicographic
cost `(item count, new-form arity sum)` retains the two unary responses.
The original fast checker and its naive response predicate both accept the
retained responses. The source enumeration, not a newly assigned constant,
supplies these frontiers.

This is an **observational separation** floor. Its binary alternatives include
diagonal instances; the model has not admitted a protected irreflexivity law.
It is therefore distinct from the floor for an exhibited irreflexive cut.
An opaque inscription, its repeated supply, and its deduplicated readmission
still do not produce a second datum, form, orientation or protected law.
The [admission theorem supplement](primitive_admission_and_transport.md)
states the additional cut hypotheses and proves their separation consequence.
No scalar price or admission discipline is selected by the inscription.

## 3. State, occurrences, cost and future observations

For the selected seed-25 source, the native packet retains all ordered term
positions, both nonnegative multiplicity tables and every oriented filled
triple. Serialization to that packet is injective on the source's unnamed,
fixed-writing `FState`: the source state is recovered by reconstructing its
two tables and filled tuple. Consequently every deterministic question on
that full state factors through the packet, including the enabled next-change
list and seed-22 plain-state price. This is a representation argument for
those source types; it does not claim a source-specific evaluator for every
future question or a complete execution refinement for every seed.

The repair quotient forgets more. Simultaneous `r`/`s` assertions can preserve
excess while changing removals available in the future. Raising can preserve
repair class while changing the plain-state price. A final packet also omits
the number and order of prior occurrences. Ordered occurrences and their
declared prices must therefore remain in a separate trace whenever they are
protected questions. The unbounded-history criteria in
[`OriginalGenesisObserver.lean`](../lean4/WitnessedDifference/OriginalGenesisObserver.lean)
give the corresponding extension-congruence and paid-descent conditions.

Seed 15's selected admission record preserves the underlying assertion state;
reaching a result leaves it not admitted. Seed 16's selected admission
consumes a recorded leftover and adds an assertion. The replay checks both
actual functions. Treating their shared word “admission” as one transition
would fail preservation of their declared source fields.

## 4. Actual subcontext restriction and lawful composition

`GenesisOngoingAdapter::restrict(vertices, marks)` selects distinct existing
vertices and existing marks contained in those vertices. It keeps loops and
independent reverse arcs, copies both actual multiplicity tables, and rotates
each oriented triple to its least target index before sorting. It returns
the actual target packet and a matrix-owner checked cochain map.

If `i` is the selected vertex injection, the maps are
`F0(g)(x)=g(i(x))`, `F1(h)(x,y)=h(i(x),i(y))`, and the corresponding selection
of marked diagnostic rows in degree two. Substitution gives both squares:

```text
F1 d0 = d0 F0
F2 D_source = D_target F1.
```

Two restrictions compose by composing their injections and mark selections.
The adapter binds the complete intermediate assertion packet, including raw
multiplicities; the matrix owner independently checks the resulting product.
A full permutation with its inverse gives both identities. A proper
restriction need not reflect classes: restricting to the empty context
forgets a loop obstruction. Tests check these cases and typed refusals for
unknown, duplicate or out-of-context selections.

This pullback does not turn term addition into a zero-extension cochain map,
or arbitrary identification into a quotient map. The source countermodels
remain. Explicit linear homotopies establish agreement on closed classes
under their equations; they do not supply general higher path constructors
or Kan fillers. A source site and all its restriction/coverage laws remain
additional data for a sheaf claim.

## 5. Operational reconstruction and its nonselection boundary

The selected operational target admits a complex Hilbert carrier, positive
density matrices of trace one, effects between zero and the identity, trace
pairing, and Kraus updates with their normalization and composition laws.
[Realification](genesis_qm_realification_bridge.md) preserves their exact
statistics when the doubled real representation retains the chosen complex
structure and scales states by one half. Four fresh native cases check
rectangular products/adjoints, imaginary coherence, conditional states,
sequential channels and the failure of unrestricted real models to be the
same image. The phase test separately checks telescoping and gauge invariance.

These are conditional operational realizations. Trace-one alone permits
`diag(2,-1)`, which yields a negative value for a positive basis effect.
Positivity is therefore required for this probability interpretation.
Phase invariance alone permits other normalized readouts and does not select
trace pairing or Born weights. A finite classical model and an unrestricted
real carrier remain countermodels to unconditional complex-Hilbert selection.
No source replay supplies undeclared positivity, scalar or composition axioms.

## 6. Actual policy enforcement and institutional limits

The current CODA authority boundary is
[`authority.py`](../code/coda_application/domain/authority.py): a keyring
configured with recognized grantors verifies a grant bound to a problem,
evidence, licensee and nonce; each nonce is spent once. Token minting checks
both verification and prior spending. The two fresh selected tests reject
internal token construction and fabricated/unspent grants. This verifies a
declared software rule; possessing or accepting a key does not prove external
institutional standing or a physical fact.

The actual Prime integration test
[`prime_rules_end_to_end.rs`](../../../../../../omega_engine/crates_rs/tests/omega_solvers/prime_rules_end_to_end.rs)
supplies native computed and replayed residual certificates to the DDC owner.
Its five fresh cases distinguish a paid loss from an unpaid increase, refuse
cross-carrier residual subtraction and admit the declared lawful decrease.
Budget, adequate detection, scoped continuation and execution permission
remain separate meanings. A routing terminal is not an authorization token.

An appeal additionally needs a declared challenger class, review jurisdiction,
admissible new evidence and revision rule. A record of denial cannot determine
those choices: two institutions can share all reports and disagree about
appeal rights. Likewise identical mathematical evidence with opposite
permissions defeats every evidence-only decoder. The already compiled
fiber-constancy theorem makes this a precise nonselection boundary. No general
institutional or all-source reconstruction is claimed here; O01–O05 remain
open at their full enlarged scopes in the completion audit.

## Replay commands

Run from this package, with exact snapshots located under the explicit root:

```powershell
py -3.12 scripts/verify_source_replays.py --source-root <snapshots> --output <new-receipt.json>
py -3.12 scripts/verify_finite_derivations.py --lean <Lean-4.33.1-binary>
```

The source verifier refuses an existing output. The committed source receipt
is an execution artifact; the script and pins are its reproducibility inputs.
The custody tests mutate temporary fixtures only, not original repositories
or historical receipts. Their eleven cases cover regular-file substitution,
directory controls, traversal errors and root-relative cache exclusions.
