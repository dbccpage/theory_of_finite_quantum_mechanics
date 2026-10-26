# Actual primitive admission and persistent challenge floor

AuthorityEffect: None. This supplement advances GEN-WDP-O01/O02 for the
original `19L57G1` derivation model. The five enlarged obligations remain
open at their full scopes. The original revision is
`f1d56c010e6ba10a3b9418bd7cc5953c067250f2`; the four executable source files
are byte-bound in [the primitive input manifest](../manifests/primitive_execution_inputs.json).
The source's fast minimum routine and its full replay are distinct functions.

## Raw regime and six-event correspondence

A regime has ordered datum tokens, ordered positive form arities, admitted
instances, uniform rules and persistent separation requirements. The last
three components are sets. Tokens are opaque strings; empty strings,
Unicode and duplicate occurrence tokens are representable. An index denotes
an admitted occurrence. Token equality in the dedup reading is an external
convention, not a derivable identity law or a parsing of angle brackets.

Map each well-formed source regime componentwise to
`omega_wdp::genesis_primitive_execution::PrimitiveRegime`, preserving ordered
lists and replacing source frozensets by ordered finite sets. Every finite
well-formed source state whose sizes fit native indices has such an image.
The source dataclass also permits malformed direct constructions; these are
outside this checked native domain.

| Source event | Raw effect and acceptance condition |
| --- | --- |
| `Supply(token)` | Keeps every admitted component unchanged. Prior supply is not an admission precondition in this source. |
| `AdmitDatum(token)` | Dedup appends iff the token is absent. The occurrence reading always appends. |
| `AdmitForm(k)` | Appends a new form iff k is positive; equal arities do not identify forms. |
| `AdmitInst(f,args)` | Requires an existing form, its exact arity and existing datum indices; set insertion is idempotent. |
| `AdmitRuleAll(f)` | Requires an existing form and inserts its uniform rule. |
| `Impose(i,j)` | Requires i < j < n and inserts the requirement even when it is presently unsatisfied. |

Each case uses precisely the same condition and component update on both
sides. Thus the component map preserves successful steps and reflects
semantic refusal on this domain. Induction on a finite event word gives
the same raw state at every prefix, for either fixed reading. This is a
written correspondence proof; the concrete Python and Rust programs have
finite differential evidence rather than a machine-checked refinement theorem.

`PrimitiveRun` retains its reading, complete initial/intermediate/final
states and ordered events. Composition requires equality of the whole
intermediate state and reading. Replaying the suffix from that boundary
proves the append law. Neither a final-state summary nor a multiset of
events establishes this boundary. Raw events have no source price field;
canonical deltas carry the separate item and arity prices.

## Actual observation and candidate semantics

A context consists of an existing form and one slot per argument; at least
one slot is a hole and every non-hole slot is an existing datum index.
Plugging a datum fills every hole with that same datum. An instance is
derivable exactly when it is admitted or its form has a uniform rule.
A profile is the set of contexts derivable after that plug. Separation
means unequal profiles, and a witness is the first context in source
order that gives opposite judgments. A uniform rule may erase an earlier
separation; accepting a well-formed event does not establish satisfaction.

The native context list has the same form order and lexicographic slot
order, with the hole preceding datum 0. Its profile, collapsed-pair,
first-witness and requirement checks therefore preserve the source's
actual observations. Shared `omega_combinatorics::cartesian_words::CartesianWords`
owns the finite product, exact cardinality and resource refusal. Its
independent width ceiling is 4096. The caller supplies cumulative tuple
and candidate limits. A resource refusal yields no partial candidate list
and makes no claim of mathematical impossibility.

`full_deltas` implements the source's complete unpruned enumeration for
0, 1 and 2 items. It retains canonical multiset items, repeats and the
first-occurrence output order. In particular, cost 1 emits all missing
uniform rules before any instances; cost 2 uses the source's interleaved
universe order before canonicalizing each pair and replay-filtering it.
The original oracle found and corrected an initial native ordering error
for bases with multiple forms.

`minimum_responses_checked` checks actual replay, imposes the target and
tests every persistent requirement. It minimizes item count first, and
then new-form arity for `ItemsThenArity`, within the declared item/arity
bounds. It supports bases with uniform rules. A returned `None` means no
valid response in that complete bounded space; it does not rule out a
larger item count or arity.

## All-arity floor with persistent requirements

Let the initial regime have n admitted data, no forms and proper persistent
requirements Q. Let the new challenge be a proper pair (i,j). Form the
finite graph G with edges Q union {(i,j)}. A vertex cover C meets every
edge. Write tau(G) for its minimum size. The target ensures tau(G) >= 1.

No zero- or one-item delta separates the target: datum or form admission
alone supplies no derivable context, and an instance or rule without a
form is ill-formed. Classifying the two-item multisets leaves one possible
separating shape: a new positive-arity form followed by one instance on
that form. Two forms have no instances; datum/form pairs have no instance;
instance/rule-only pairs lack a form. A form plus a uniform rule gives
every datum the same profile.

For the remaining shape, let t be the admitted tuple and C its mentioned
data. A datum d has a nonempty profile iff d occurs in t. For the forward
direction, a hole plugged by d contributes an occurrence of d to t. For
the reverse direction, replace each occurrence of d in t by a hole and
leave the other entries fixed. That context recognizes d. If a context
recognized distinct a and b, a hole would equate a and b. Thus distinct
mentioned data have disjoint, nonempty profiles, while all unmentioned
data have the same empty profile. A pair is separated iff at least one
endpoint is in C. All requirements are satisfied iff C covers G.

This proves the following for every finite no-form regime, not only the
two-datum initial fixture:

1. With maximum form arity A, a two-item response exists iff tau(G) <= A.
2. When it exists, the item-count floor is 2. All minimum responses are
   form/instance pairs whose tuple length is at most A and whose mentioned
   data cover G. Repetition is permitted.
3. The lexicographic item/arity minimum is (2,tau(G)). At this arity, each
   tuple lists the members of a minimum vertex cover exactly once, in any
   order. A shorter tuple would give a smaller cover; conversely every
   minimum cover supplies a tuple of that length.

For a single target on two data, tau=1: there are two unary minima, and
with A=2 the item-only frontier also retains all four binary tuples.
For all three pair requirements on three data, tau=2 and the minimum
frontier has six ordered binary tuples. For all six pairs on four data,
tau=3 and there are twenty-four ordered ternary tuples. At A=2 no
two-item response satisfies those six requirements. A unary choice is
therefore insufficient once the persistent requirement graph needs a
larger cover.

The core-only [PrimitiveContextFloor module](../lean4/WitnessedDifference/PrimitiveContextFloor.lean)
proves eleven selected declarations, including profile inhabitation,
hole reflection, the pair criterion and the requirement-cover equivalence.
Its [source-bound receipt](../lean4/primitive_context_floor_axioms.txt)
uses `propext` and no admitted proof. The classification of item shapes,
minimum-cover optimization and concrete program correspondence are
written above; they are not additional formalized declarations.
These positive judgments also do not impose an irreflexivity law.

## Generated-token collision is a live boundary

The source translates `NewDatum` to token `w{n}` and increments its
prospective index. An arbitrary externally admitted token can already
have that name. For data `["w2","x"]` and one binary form, the delta
`NewDatum; NewInst(0,(0,2))` tries to admit `w2`. Dedup leaves only two
data, so index 2 is invalid. The source fast check accepts this delta;
the source naive replay raises `AdmissionError`.

The native raw translation retains the original collision and its replay
rejects the instance. It does not certify generated-token freshness from
an incremented counter. The checked minimum path validates full replay.
The pinned source is unchanged, and the independent fast result remains
visible in the receipt rather than being relabeled as a full-replay result.

## Reproducible evidence and limits

The [receipt](../evidence/primitive_execution_receipt.json) binds the
[verifier](../scripts/verify_primitive_execution.py) and four original source
files. It executes the original functions; it does not replace their
mathematics with a new Python implementation. The original/native digests
match 1,664 regimes, 72,954 event attempts, 25,408 semantic refusals and
582 complete candidate deltas in eleven declared bases. Both reading
histories retain every intermediate state and every prefix split. The
three oracle cases, seven focused native cases and two Cartesian owner
cases pass. This is finite program evidence in addition to the stated
unbounded mathematical proofs.

Six focused custody cases reject same-byte source/control symlinks, a
linked parent, directory controls and post-execution mutation. The
verifier checks regular entries, source sizes/digests/Git blobs and the
import closure, then rechecks the source/control bytes after execution.
Use a fresh output path:

```text
py -3.12 scripts/verify_primitive_execution.py \
  --source-root /path/to/pinned-source-snapshots \
  --output /path/to/new-primitive-receipt.json
py -3.12 -m pytest --no-cov -n 0 \
  code/tests/python/injection_tests/test_primitive_execution_custody.py
```

From the repository root, the native scope is:

```bash
cargo test --manifest-path omega_engine/crates_rs/Cargo.toml --offline --locked -j1 -p omega_kernel --test cartesian_words -p omega_wdp --test genesis_primitive_execution --test primitive_execution_oracle
```

This branch supplies actual primitive context and persistent-cost
correspondence. It leaves other source regimes, higher coherent
transport, operational reconstruction and institutional meanings under
the five open obligations in [the completion audit](programme_completion_audit.md).
