Status: AI-drafted, awaiting human review.

# Complete finite Genesis context decisions

AuthorityEffect: None. Target: PGW-CONTEXT-DECISION-PROCEDURE / TFQ-0497.
Provisional campaign outcome: Narrowed. The finite context decision theorem is
derived for arbitrary finite regimes; the node's first-count, uniformity and
implementation-refinement obligations remain open.

## Source and scope

The existing `GenesisComputation.GenesisCopy.Regime` is the admitted carrier:
a natural datum count, a list of form arities, a list of instances, a list of
uniformly ruled forms, and a list of requirements. No new regime semantics is
introduced. The earlier `GenesisComputation.UnarySep` sees unary hole-only
contexts and ignores uniform-rule coverage. It cannot implement the full
observation relation of this target.

The source `continuation.txt`, definitions in section two and its open register,
and `code/derivation/observe.py` specify the relation used here:

- a context is an admitted form and an arity-matched tuple of holes or admitted
  fixed data, with at least one hole;
- plugging replaces every hole by the same datum;
- a plugging is derivable when the instance is admitted or the form has a
  uniform all-tuples rule;
- collapse means equal derivability in every well-formed context; separation
  means a distinguishing well-formed context exists;
- holding two means some admitted pair is separable;
- an exhausted form reads every admitted pair alike in every context on it.

This is a finite slot language. It contains multiple-hole contexts and arbitrary
admitted arities. No bound on arity or datum count occurs in the Lean theorem.
It does not decide an arbitrary recursively generated term language, word
rewriting system or a language with additional inference rules.

## Enumeration and completeness

For datum count n, define the slot alphabet as hole followed by the datum indices
in increasing order. Define `slotTuples n 0` as the singleton empty tuple, and
form the next tuple list by prefixing each alphabet slot to each previous tuple.
This has the source order: first coordinate varies slowest, last fastest.

Induction on arity gives `mem_slotTuples`: membership is equivalent to the
declared length and every fixed slot being below n. For each admitted form,
filter its tuple list to retain a hole and attach the form index.
`mem_contexts` then states, for every raw context c,

```
c is in contexts(r) iff c is well formed in r.
```

Thus the search is complete over the whole finite context language, including
all hole multiplicities. An empty form list produces no contexts. A context
with an invalid form, wrong arity, no hole or an out-of-range fixed datum is
excluded by the characterization. Zero admitted data are also covered: there
are no datum pairs or observational classes.

## Collapse and separating witnesses

Evaluate the Boolean equality of the two derivability bits at every enumerated
context. `collapseTest_correct` identifies the all-true result with the
universally quantified definition of collapse. This gives a computable
`Decidable` instance for that definition, and the negated test decides
separability through `separable_iff_not_collapsed`.

The witness function uses `List.find?` on the same ordered list.
`witness_sound` proves that every returned context is well formed and
distinguishes the pair. `witness_none_iff` proves that it returns none exactly
for collapsed pairs. Completeness is therefore a theorem about the complete
context language, rather than a search receipt at a fixed arity.

The independent checker deliberately distinguishes two assertions. Filtering to
unary contexts loses binary separation. Filtering to one-hole contexts can
change the first witness when a multiple-hole witness comes first. No claim
is made that the family of all one-hole contexts is insufficient to decide
collapse; that would require a different argument and is not established here.

## Profiles and the class count

For each admitted datum, compute the finite set of contexts whose plugging is
derivable. `mem_profile` relates set membership to well-formed derivability;
`profile_eq_iff` identifies equality of these finite sets with collapse.
Taking the finite image of the admitted datum range yields `classes`; its
cardinality is the executable `classCount`.

The semantic quotient is defined independently by collapse over all well-formed
contexts on `Fin r.data`. `quotientProfile_injective` shows that mapping its
classes to computed profiles is injective. Every computed profile is occupied
by an admitted datum, and every quotient representative has one of those
profiles. The image of this injection is exactly `classes`. Consequently
`classCount_eq_quotient_card` states

```
classCount r = Nat.card (Quotient (observationSetoid r)).
```

The quotient's relation is the universal context predicate `Collapsed`, not a
new relation stipulated to have the desired cardinality. `holdsTwo_iff_classCount`
also identifies holding two with a class count of at least two.

## Exhaustion and uniform rules

Filter the complete context list to the selected form, then test every admitted
datum pair. `exhaustionTest_correct` identifies that Boolean with the source's
universal exhaustion predicate. A uniformly ruled form makes both derivability
bits true, so `uniform_rule_exhausted` applies to every such form and regime.
This establishes sufficiency. It does not establish the historical necessity
claim Y-2, which concerns histories and the declared reading of that claim.

## Independent exact checks

`checks/independent/pgw-context-decision-procedure.py` imports no repository code.
Its primary route enumerates Cartesian slot tuples. Its second route chooses
nonempty hole masks and independently assigns the remaining fixed positions;
it constructs ground tuples and derivability bits without calling the primary
plugging or context helpers. It also constructs quotient groups independently
from these truth vectors.

The checker exhausts all fact and rule subsets for datum counts zero through
two, with form signatures empty, unary, binary, ternary, and unary plus binary:
849 regimes. It checks every admitted pair, witness completeness, profiles,
class counts, holding two, and form exhaustion. The observed class-count
histogram is 11 with zero classes, 420 with one, and 418 with two.
An additional three-datum arity-four fixture checks the larger context language.
SymPy integer powers independently recompute each context count from
`sum_f ((n+1)^arity_f - n^arity_f)`.

The concrete Lean witnesses include a binary form separating the data through
`(hole,1)`, an initial multiple-hole witness `(hole,hole)`, and a uniform-rule
admission changing the class count from two to one. Four semantic mutations
are detected: unary-only search, changed first-witness order under one-hole
filtering, ignored uniform rules, and counting data instead of distinct
profiles. Seven malformed-input probes are rejected. Normal and optimized
Python outputs agree; the CLI's executable envelope is explicit and independent
of the generality of the Lean theorem.

Enumeration can be exponential in compact arity. Its cost is output-sensitive
in the slot universe; no efficient polynomial algorithm in compact regime size
is claimed. The Python entry boundary limits datum count, arity and total slot
enumeration and uses immutable tuple/frozenset fields.

## Replay and claim boundary

Build `lake build CampaignGenesisContextDecision` in its non-default library.
It imports the unchanged legacy `GenesisComputation` module; the replay records
which modules compiled and retains the existing dependency warnings. The new
module uses the compatible legacy import mode. Every terminal theorem audit
must contain only propext, Classical.choice and Quot.sound. The receipt binds
committed LF source blobs, including the unchanged carrier dependency.

No Python-to-Lean compiler or operational replay refinement is claimed. The
source observation definition is mirrored explicitly in the existing carrier;
an independent executable check does not prove equality of external programs.

## What is proved

Complete context enumeration, a correct general collapse decision procedure,
sound and complete separating-witness search, profile/collapse equivalence,
the computed cardinality of the semantic observational quotient, the holding-two
criterion, and a correct general form-exhaustion procedure with uniform-rule
sufficiency. These results cover arbitrary finite regimes and arities in the
stated source model, with no unary-only restriction.

## What is assumed

The admitted finite regime carrier and the declared slot/derivability language.
Uniform rules here are exactly all-tuples rules; no further inference closure
is silently supplied. Datum indices remain the declared internal identities.

## What is open

The original node also asks for first-count existence and the history-level
necessity statement Y-2. Those require their declared history predicates and
separate theorems. A refinement to the sealed Python/Rust implementations and
their driver remains outside this result. The full bundled node stays OPEN;
its finite context, class-count and exhaustion clauses now have local Lean
evidence. Outcome classification awaits human review.
