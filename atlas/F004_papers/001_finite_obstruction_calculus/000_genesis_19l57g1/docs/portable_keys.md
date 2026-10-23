# Portable canonical keys, version 1

The frozen Python and current Rust refined local keys choose color-class
orders by different conventions. Their equality classifications can agree
while their labelled representatives and fingerprints differ. Local keys
are implementation-specific.

`portable_key_v1` minimizes the total structural tuple
`(n, forms, instances, rules, requirements)` over **all** datum and form
bijections, using structural lexicographic ordering. Form arities travel
with form indices. Instance and rule collections are sorted. Requirement
endpoints are sorted within each pair, and the pair collection is sorted.
Presentation labels are erased. The contract includes only well-formed regimes
whose encoded integers and collection lengths lie in `0..2**64-1`. Python
rejects invalid structure, non-integer values and overflow with `PortableKeyError`.

The byte encoding starts with ASCII `GENESIS-KEY`, a zero byte, and byte 1.
All subsequent integers are unsigned 64-bit big-endian words:

1. Datum count; form count; each form arity.
2. Instance count; for each instance, form index, argument count, argument indices.
3. Uniform-rule count; each form index.
4. Requirement count; each pair's lower and upper endpoint.

Collection lengths and fixed integer widths make this encoding injective on
the declared tuples. The empty regime encodes as the 13-byte prefix followed
by forty zero bytes. Hashes of these bytes must carry the protocol version
and hash-algorithm identifier; existing local fingerprints are not portable.

The caller declares a budget for `n! × number_of_forms!` candidates. Both
implementations refuse exhaustion before enumeration. The default is 100,000.
The protocol trades factorial runtime for an uncomplicated common convention;
it does not replace the faster historical refined algorithms.

The standalone replay compares complete bytes and every context observation
on all 1,436 regimes of its explicitly enumerated population. The concrete Lean
exhaustive-search theorem supplies a mathematical classification criterion. A general refinement
proof of these Python and Rust source programs remains an engineering question.

The companion theorem `GenesisPaper.serializedRelabel_sound` formalizes the
soundness of comparing sorted structural tuples after supplied datum and form
bijections, for well-formed regimes. It uses membership preservation of list
sorting and constructs the composed regime isomorphism.

`GenesisPaper.Wire.structuralWords_injective` formalizes recovery of the exact
five-field tuple from the length-prefixed word layout. `portableBytes_injective`
then establishes injectivity of the actual 13-byte prefix and unsigned 64-bit
big-endian encoding, under the explicit word-range hypothesis.
`portableBytes_sound` composes those results with regime-isomorphism soundness.
These are general Lean theorems. The additional `GenesisPaper.Search` module
constructs every finite bijection from its permutation table, proves that its
insertion enumerator contains exactly all permutations, and selects the least
five-field tuple. `canonicalKey_attained` proves attainment and leastness;
`canonicalKey_classification` proves equality exactly for isomorphic well-formed
regimes with duplicate-free collections. `canonicalBytes_classification`
extends the criterion to the wire encoding under the unsigned-word bounds.
No orbit-choice or invariance premise is supplied. General refinement of the
Python and Rust source programs remains a separate obligation.

`encode_structural_key_v1` and `decode_portable_key_v1` are available in both
languages. The decoder checks complete consumption, positive arities, all index
and argument bounds, ordered requirements and strictly sorted collections. It
rejects truncated input, oversized length declarations, trailing data and
duplicates. Acceptance does not establish that the labelled tuple is an orbit
minimum. Rust also rejects words outside the host's `usize` range; the replay
reported here uses a 64-bit host.

The native Lean executable evaluates the encoder defined in the proof module.
It agrees with Python on 1,439 tuples, including three boundary vectors.
The native proved Lean search also agrees on all 1,436 labelled regimes;
its inputs retain their original datum and form indices. Two further probes
exercise mixed arities and descending instance-list order. Its input validator
executes the well-formedness and duplicate-free predicates and rejects 17
malformed or over-budget cases. The native wrapper caps each dimension at eight
and the permutation-pair budget at 100,000 before enumeration. The theorems
apply to arbitrary finite dimensions and do not impose these runtime caps.
The largest admitted population, 80,640 permutation pairs, is also executed
and its minimum checked against the known empty-collection structural tuple.
Python and Rust agree on 72 explicit acceptance/rejection cases, including
all truncations of the empty key and maximum unsigned-word values. A budget
of zero refuses even the empty regime's single identity candidate. Budget
checking stops at the first exceeded bound, before constructing factorial-sized
candidate sets or an unbounded factorial integer.
