Status: AI-drafted, awaiting human review.

# Exact Genesis replay representation

AuthorityEffect: None. Campaign target: PG-GEN-SUPPLY-ERASURE. This also
supplies the representation needed by PG-GEN-SUPPLY-NO-OP and the one-step
potential premise of PG-GEN-NO-RETURN. Outcome classification awaits review.

## Source custody and the objects being compared

The source interpreter is `Derivation.stepE` and `Derivation.replayE` in
`atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Basic.lean`.
The file's Git blob is exactly `610d8fc982853807eb892eaaf683fc4eb2959cc1`,
the file fetched from `dbccpage/19L57G1` at the sealed commit
`3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`. The receipt records both the
committed local bytes and this external source pin. The atlas source is
compiled in place, without editing the archive.

There are three representations. The existing `GenesisComputation.GenesisCopy`
uses lists. The source uses a separate Lean structure with the same fields.
The new `ArrayRegime` uses a natural datum count and arrays for the form,
instance, uniform-rule and requirement stores. An instance's argument tuple
is a list of natural indices. No field is omitted or represented merely by
its count. Order is preserved; the theorem does not identify arbitrary
permutations of stores.

The map `decode` takes each array to its list, and `encode` performs the
reverse conversion. Both composites are the identity, so this is a
representation isomorphism. The maps between the existing copy and the
source are also inverses. The event maps preserve every constructor and
every argument.

## Every guarded transition

The array interpreter is defined by array operations, independently of the
source transition function. Supply returns the input unchanged. Datum
admission increments the count. Form admission checks positive arity and
pushes the arity. Instance admission checks the form index, argument length
and every datum index; it inserts the instance only if absent. Uniform-rule
admission checks its form and inserts only if absent. Requirement admission
checks the ordered pair of datum indices and inserts only if absent.

The representation theorem splits on these constructors and their guards.
The guards have exactly the same truth values after decoding. On success,
array push becomes list append and deduplicating array insertion becomes
the source's `insertNew`. On failure, both results are `none`. Consequently,
for every array regime and every source event,

```
map decode (arrayStep r e) = stepE (decode r) e.
```

This is not an agreement theorem restricted to the tested events or states.
It quantifies over every natural coordinate and every finite argument list.

## Every finite history, including failures

Both replays sequence partial steps with `Option.bind`. Induction on the
history proves that decoding commutes with replay. In the inductive case,
a failed first step poisons both replays. A successful first step gives the
same decoded successor, to which the induction hypothesis applies.

The inverse representation map gives both directions of success and
failure reflection:

```
arrayReplay h r = some (encode s) iff replayE h (decode r) = some s;
arrayReplay h r = none iff replayE h (decode r) = none.
```

The earlier copy-to-source replay theorem is proved independently in the
same way. It therefore connects the actual existing copy, rather than a
newly substituted count-only abstraction, to the source interpreter.

## Supply erasure and the token-aware model

A supply step is the identity in the source for every regime. Induction on
the history proves that filtering supply events preserves the entire
partial replay result. On a non-supply event the proof retains its guard
and failure branch. The representation isomorphism transports this equality
to array replay. Reading L and Reading F are both exhibited with their full
requirement stores.

Token erasure requires an additional distinction. The source token-aware
interpreter deduplicates datum admission by token identity, whereas the
erased datum-admission constructor always increments its count. The
source's `eraseEvent` translates a duplicate admission into supply, relative
to the current token store. Its `eraseHistory` threads that state and stops
after the first invalid event. The compiled source theorem `erase_replay`,
combined with the array replay representation, gives `token_array_replay`.
A context-free replacement of every token admission by an erased increment
would fail on two admissions of the same token.

## Potential and the exact source transition

The potential is the datum count plus the lengths of the other four stores.
A separate field-and-event map connects the source interpreter to the
actual `SecondRun.Sealed` interpreter. Transporting its source theorems shows
that every successful source step weakly increases this potential and every
successful step that changes the regime strictly increases it. This
statement concerns equality of all fields, rather than a comparison of
two independently supplied counts.

## Independent audit

`checks/independent/pg-gen-supply-erasure.py` imports no repository code. It
compares an immutable tuple interpreter with separately written mutable
array-coordinate operations. It enumerates every history through the
printed length bound over a printed alphabet, from the empty regime and
both challenge readings. It compares every successful coordinate and
partial failure, filters supplies, checks state-dependent token erasure,
and challenges incorrect supply admission, failure recovery, duplicate
insertion, unordered requirements, token erasure and missing rule fields.
SymPy independently counts the history universe and evaluates the
potential. Its JSON receipt gives the exact counts and every mutant's
reference and incorrect result. The Lean proof has no history-length bound.

## What is proved

The existing list copy and the new array model represent the actual sealed
source regime and transition interpreter exactly. This includes all fields,
all event arguments, success, guard failure, every finite replay, supply
erasure, both readings and the source's state-dependent token-erasure
simulation. Successful real source changes strictly raise the source
potential.

## What is assumed

The declared source event grammar, internal datum indices, deduplicating
collection semantics and optional failure semantics. The historical tag
binding is cryptographic source custody in the receipt; a tag name alone
is not a mathematical premise.

## What is open

This is not a proof of the CPython or Rust runtime, a verified compiler, or
an operational refinement of the Alpha responder and its license protocol.
Those are distinct from representation of the mathematical interpreter.
The demand-policy extension, finite-obstruction carrier bridge and
whole-process comparison-class questions are separate campaign units.
