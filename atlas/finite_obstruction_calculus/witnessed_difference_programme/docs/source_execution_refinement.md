# Raw source execution, pair transport and paid histories

AuthorityEffect: None. This supplement connects the pinned seed-25 transition
rules to a native execution kernel. It supplies a universal algebraic proof,
a source-specific representation argument and finite differential evidence.
It advances O02 and the dynamic-carrier branch of O03; the other original
transition/admission systems and the full enlarged obligations remain open.

## Declared source domain

At Genesis Ongoing revision `5d9488324ce976817987bd83a28d901371cfc073`,
`twentyfifth.state.FState` consists of an unnamed carrier `0..n-1`, two
nonnegative integer multiplicity tables and sorted, distinct oriented filled
triples. A triple starts at its least vertex; reverse orientations remain
distinct. The selected dependency closure has unchanged
[source pins](../manifests/source_replay_inputs.json).

The native
[`Source25State`](../../../../../../omega_engine/crates_rs/omega_wdp/src/genesis_source_execution.rs)
uses canonical labels `t0..t(n-1)`, arbitrary `BigInt` counts and the
same canonical triples. Its checked constructor preserves every source
field. Decode the labels as positions and reconstruct the two row-major
tables and filled tuple to recover the source writing exactly. This is a
bijection on the declared unnamed integer states, subject to the native
carrier's addressable dimension and allocation limits. It does not include
arbitrary untyped Python objects: the Python constructor's annotations do
not, by themselves, exclude every noninteger object.

An event is one canonical descriptor in `twentyfifth.state.changes(state)`.
The kernel's `perform_enabled` matches membership in that list followed by
the source's `perform`. The original function also accepts some rotated
filling aliases and unused descriptor fields outside its canonical enabled
list. Those raw calls are not the selected legal-run interface.

## Preservation and reflection by the five edit cases

For a vertex map `q`, transport each relation table separately by

```text
T'(i,j) = sum of T(x,y) over q(x)=i and q(y)=j.
```

The source identification loops implement this sum. With incidence matrix
`P(i,x)=1` when `q(x)=i` and zero otherwise, the exact matrix owner
[`push_forward_square`](../../../../../../omega_engine/crates_rs/omega_linear_algebra/src/semiring_lumpability.rs)
computes `P T P^T`. Expanding the two matrix products, distributing the
finite sums and exchanging their order gives the displayed fiber sum.
This argument includes every loop and reverse arc, noninjective maps and
empty target fibers. It does not require a bound on natural multiplicities.

The core-only
[`Source25PairTransport.lean`](../lean4/WitnessedDifference/Source25PairTransport.lean)
compiles that equality for every finite vertex list, map and natural table.
Its declared edit model replaces source fiber loops by the actual matrix
product order. The resulting partial step and ordered execution agree at
every finite history length, retaining all intermediate states, occurrences
and the two addition prices. The
[source-bound axiom receipt](../lean4/source25_pair_transport_axioms.txt)
audits ten selected declarations and reports `propext` and `Quot.sound`;
there are no admitted proofs. Lean does not verify Python/Rust parsers,
sorting implementations, machine allocation or the other Genesis seeds.

The source correspondence is checked case by case:

| Event | Exact raw output and enabled condition | Addition price |
| --- | --- | --- |
| Identify x,y | Requires x<y<n. Use q(y)=x, q(k)=k-1 for k>y, otherwise q(k)=k. Sum both relation fibers; map each filled triple, drop degeneracies, rotate to its least vertex, deduplicate and sort. | (0,0) |
| Remove relation,x,y | Requires an in-range occupied coordinate. Subtract one from exactly that relation coordinate; preserve the carrier, other counts and marks. | (0,0) |
| Fill x,y,z | Requires three distinct in-range vertices in canonical orientation and an absent triple. Add that mark; preserve both assertion tables. | (0,0) |
| Add term | Zero-extend each table through the inclusion of old vertices; preserve every mark. New incident counts are zero. | (1,0) |
| Add assertion relation,x,y | Requires an in-range ordered pair; an existing assertion and a loop are both allowed. Add one to that coordinate alone. | (0,1) |

Every enabled descriptor belongs to one of these cases, and each predicate
is recovered from the full packet. The complete enabled ordering is
identifications in lexicographic order; occupied r coordinates then s;
absent oriented triples in lexicographic order; a term; all r additions
then all s additions. Removal appears once per occupied coordinate rather
than once per copy. These observations establish both preservation and
reflection at the declared source interface. Storage and ordering agreement
are also checked against original functions below.

## All finite legal runs and future questions

For an arbitrary legal event word, induct on its length. The empty word
retains the decoded initial state. If its first event is enabled, the five
cases above give the same complete successor and its addition price; apply
the induction hypothesis to the remaining word. If it is disabled, both
legal-run interfaces refuse at that prefix. A refusal adds no occurrence
and is not an admitted no-op.

The native `Source25Run` stores every raw intermediate, the exact ordered
event word and the sum of both addition-price coordinates. Composition
requires equality of the complete intermediate packet. Concatenating two
such runs retains one copy of that boundary state, concatenates occurrences
and adds prices. Empty runs are identities; list concatenation and integer
addition give associativity whenever the boundaries agree. A matching excess
table alone is insufficient to establish that boundary equality.

Injective raw-state encoding preserves every deterministic state question,
including the next enabled list, `n + sum(r+s)`, the seed-22 plain-state
price `n + sum(abs(r-s))`, marked diagnostics and source result marks.
Trace questions additionally use the retained history. Adding r(0,1) and
then removing it has the same final state as an empty run, but two more
occurrences and one more assertion addition. Final-state equality cannot
recover that difference.

These are written all-run arguments for the declared seed-25 semantics,
with the finite-sum kernel mechanized separately. They are not a
machine-verified refinement of every original executable or an all-source
completion of O02.

## Carrier changes and raising retain representatives

Zero and the gradient of potential (1,0) have the same two-term source
result. After zero-extending each to three terms, their result marks differ.
Similarly zero and the gradient of (0,0,0,1) agree on four terms; identifying
0 with 1 gives different three-term result marks. The pinned original
`result_mark` and `perform` verify both countermodels. Native execution
reproduces their raw outputs, and the fixed-carrier matrix owner verifies
repair equivalence before and its failure after each change. Thus these
operations do not define an automatic map on repair classes.

Actual source-23 raising by nonnegative counts g instead changes
`r(x,y)` by g(x) and `s(x,y)` by g(y) for x!=y. Loops and marks stay
unchanged. Its excess changes by g(x)-g(y), so marked cycle diagnostics are
preserved while raw states and available removals can change. Raising is
not one of the five seed-25 enabled changes.

## Independent execution evidence

The [new receipt](../evidence/source_execution_receipt.json) comes from
[`verify_source_execution.py`](../scripts/verify_source_execution.py),
which invokes the pinned original functions rather than a rewritten
Python transition algorithm. It binds:

- All 261 states with binary r/s tables and zero, one or two terms.
- Five explicit larger states, including both mark orientations, mark
  collapse/deduplication, loops and a count of 2^140.
- All 3,770 enabled transitions from those 266 states. A deterministic
  compact-JSON stream digest covers the complete enabled ordering, every
  raw output, both addition prices, raw sizes and plain-state costs.
- Three ordered histories, two raising cases and the two quotient
  countermodels. The native test checks every split of each retained history.

The verifier checks size, SHA-256, Git blob and regular-file custody for
all 24 pinned inputs. It rejects unbound imported source modules and
rehashes the source, control and verifier after original execution.
The native
[`source_execution_oracle.rs`](../../../../../../omega_engine/crates_rs/tests/omega_wdp/source_execution_oracle.rs)
binds the verifier/control hashes and independently rebuilds the same stream
using the Rust kernel. All three tests passed. The five additional native
kernel cases and three owner cases test malformed inputs, disabled changes,
unbounded counts, composition and general small vertex-map transports.
These are finite regression checks, separate from the universal formula proof.

From the repository root:

```powershell
py -3.12 omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/scripts/verify_source_execution.py --source-root <pinned-snapshots> --output <new-receipt.json>
cargo test --manifest-path omega_engine/crates_rs/Cargo.toml --locked --offline -j1 -p omega_wdp --test source_execution_oracle
cargo test --manifest-path omega_engine/crates_rs/Cargo.toml --locked --offline -j1 -p linear_algebra --test pair_table_transport
```

The source verifier refuses an existing output. Original pins and prior
receipts remain unchanged. The complete programme still needs each other
source-specific transition/admission map and the remaining primitive,
coherence, operational and institutional obligations recorded in the
[completion audit](programme_completion_audit.md).
