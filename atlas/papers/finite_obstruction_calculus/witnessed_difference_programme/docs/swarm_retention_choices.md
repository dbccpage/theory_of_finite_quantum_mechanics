# Typed retention extensions and arbitrary comparison

This extends the relational classification in
[`swarm_relational_retention.md`](swarm_relational_retention.md). Its target is
the actual Chapter 3 packet `(M,u,r,comparison)`, rather than independence of
newly introduced witness predicates. It also records which hypotheses are
needed before an arbitrary report tolerance can yield a quotient.

## Complete typed extension space

Fix finite sets `M`, `I`, and `O` of cardinalities `n > 0`, `k ≥ 0`, and
`m ≥ 0`. A total update has type `I × M → M`; a readout has type `M → O`;
a comparison is a binary relation on `O`. Without additional laws, the
complete packet extension space is precisely

`M^(I × M) × O^M × P(O × O)`.

The bijection takes a packet to its three fields, and the inverse assembles
any independent triple. Both composites are identities. Thus fixing **any**
two typed fields imposes no additional restriction on choices for the third.
This is a statement conditional on the fixed types, not an assertion that a
function is independent of its own domain. In particular, an explicitly typed
`u` or `r` already mentions `M`, and every realized report must belong to `O`.
The original carrier component and its typing dependencies remain visible.

Choosing an image value independently at each function argument, and choosing
independently whether each ordered report pair belongs to the comparison,
gives exact counts:

| Named data or regularity | Number of choices |
| --- | --- |
| All total updates | `n^(nk)` |
| All readouts | `m^n` |
| All comparisons | `2^(m²)` |
| All typed packets | `n^(nk) m^n 2^(m²)` |
| Reflexive comparisons | `2^(m(m−1))` |
| Symmetric comparisons | `2^(m(m+1)/2)` |
| Reflexive symmetric comparisons | `2^(m(m−1)/2)` |
| Equivalence comparisons | Bell number `B_m` |
| Per-label bijective updates | `(n!)^k` |
| Injective readouts | `m!/(m−n)!` if `m ≥ n`, otherwise `0` |
| Surjective readouts | `Σ_{j=0}^m (−1)^j binom(m,j)(m−j)^n` |

For reflexivity, diagonal membership is forced; for symmetry, one choice is
made per unordered pair including its diagonal; for reflexive symmetry,
only distinct unordered pairs remain free. Equivalence relations correspond
bijectively to partitions of `O`. The injective count chooses successive
distinct outputs. The surjective count excludes missing-output subsets by
inclusion–exclusion. These arguments are proofs of the counts, not numerical
fits to enumerated examples.

With no input labels, the update field is uniquely the empty function.
With no reports and nonempty memory, there is no readout and no complete
packet. A singleton report alphabet has a unique readout. A singleton memory
carrier has a unique total update. Under a reflexive symmetric comparison,
zero or one report has a unique comparison. These cardinality degeneracies
are genuine forced choices and must not be described as independent degrees
of freedom that do not exist.

The native constructor decodes independent mixed-radix codes for the three
fields and checks that each code lies in its own range. Counts use checked
`u128` arithmetic and return `CardinalityOverflow` outside that representable
range; no wrapped value is treated as an exact count. The Python research
witness uses arbitrary-size integers, including `2^144` comparisons on twelve
reports. Neither enumeration establishes a primitive selection rule.

## Natural choices and named coupling

There **are** canonical component choices: identity updates for every label,
the diagonal comparison, and the universal comparison are preserved by
relabeling. Therefore “no canonical choice whatsoever” would be false. What
the product theorem establishes is that typing does not force a unique full
packet, or create a law relating its fields.

There is a precise readout-selection obstruction. If the report alphabet has
a fixed-point-free symmetry and memory is nonempty, a readout invariant under
that output symmetry cannot exist: evaluating at any memory point produces a
fixed report, a contradiction. In particular, when source and output
permutations are independent and `m ≥ 2`, full output-permutation symmetry
does not permit selection of a total readout. This is not asserted when a
distinguished output, an identification `M ≅ O`, or another symmetry-breaking
structure has already been supplied. The Lean theorem states its actual
fixed-point-free hypothesis explicitly.

Regularity laws may impose new coupling. For example, report-congruence
requires `r(x)=r(y) → r(u_i(x))=r(u_i(y))`. On three states with reports
`(0,0,1)`, identity updates satisfy this law, but the total update
`(0,2,2)` does not: the two states reporting `0` evolve to distinct reports.
Both updates are fully valid typed fields. The law, rather than typing,
removes one of them. Bijectivity or injectivity restrictions constrain their
own factors; compatibility laws mentioning multiple fields constrain the
corresponding product. No general logical independence is asserted after
arbitrary extra laws have been imposed.

## Greatest forward relation for arbitrary report comparison

For a declared packet, call `R ⊆ M × M` forward-compatible when every related
pair has compared reports and every declared input takes it to another related
pair. This requires neither symmetry nor transitivity. Define

`W(x,y) ⇔ for every finite input word w, comparison(r(u_w(x)),r(u_w(y)))`.

The empty word supplies immediate report comparison, and prepending a label
proves forward compatibility. Conversely, induction on the word length proves
that every forward-compatible relation lies in `W`. Thus `W` is the greatest
such relation. This proof does not close the comparison transitively, choose
an equivalence subrelation, or strengthen it to equality.

For finite computation begin with all immediately compared state pairs and
delete a pair whenever one of its labelled successors is no longer related.
The descending sequence retains every forward-compatible relation by induction.
A stationary round is itself compatible, hence equals `W`. At most `n²`
strict deletion rounds occur because at least one state pair is removed at
each strict round. If comparison is reflexive symmetric, reflexivity and
symmetry persist, and each strict round removes at least one unordered
distinct pair, giving the stronger bound `n(n−1)/2`. The numerical bounds
are proved here by finite counting; the Lean module proves the greatestness,
word characterization, and actual-chain fixed-point correctness.

For reflexive symmetric report tolerance, `W` is reflexive symmetric. It is
an equivalence **if and only if its own transitivity holds**. Transitivity of
the report comparison suffices by composing each word's comparison, but is
not necessary: future inputs can separate some tolerated pairs, and bad
report triples may be unrealized. The native criterion checks transitivity
of the computed state relation itself.

The smallest standard obstruction uses three reports `a,b,c`, reflexive
comparison, `a~b` and `b~c`, but not `a~c`, with identity updates and identity
readout. Then `W` is exactly that nontransitive tolerance. It cannot be used
as equality classes of a state quotient. This countermodel is proved in
Lean and independently executed in Rust and Python. Transitive closure would
introduce the forbidden pair `(a,c)` and would cease to respect the declared
comparison; it is not a repair.

Even an equivalence state relation has another boundary. Deterministic
updates descend because forward compatibility preserves its classes, but
the literal readout `r : M → O` descends to `M/W → O` **if and only if** it
is constant on every class. With universal comparison and distinct identity
reports on two static states, `W` is universal and hence an equivalence,
while the raw readout fails to descend. Choosing a representative report or
changing the report target introduces extra data. The native adapter exposes
separate state-quotient and literal-report-quotient admissibility checks; the
Lean theorem proves the separate necessary-and-sufficient readout condition.

## Native ownership, actual packet adapter, and executed validation

- `omega_category_theory/src/finite_retention_choices.rs` owns the typed
  extension counts/construction and arbitrary-comparison forward refinement.
  `cargo test --locked --offline -p omega_category_theory --lib
  finite_retention_choices::tests -- --nocapture`: **4 passed**. The complete
  256 two-state/one-label/two-report packets are enumerated without duplicates.
  For each, all sixteen state relations are checked; the computed relation
  equals the union of every forward-compatible relation. Tests also cover
  nontransitive tolerance, raw-readout refusal, regularity coupling, empty
  report alphabets, empty input alphabets, and overflow refusal.
- `omega_wdp/src/tolerance_retention.rs` converts the **actual** existing
  `RetentionPacket` plus an explicit full report alphabet to that owner. It
  permits unrealized reports and never closes the comparison. Its focused
  test covers the actual three-state nontransitive-tolerance packet.
  `cargo test --locked --offline -p omega_wdp --lib
  tolerance_retention::tests -- --nocapture`: **1 passed**.
- `code/witnessed_difference/retention_choices.py` is an independent hermetic
  finite research witness. `PYTHONPATH=code python -m pytest
  code/unit_tests/test_retention_choices.py -q --no-cov -n0`:
  **12 passed**, including all 256 typed packets/all sixteen candidate
  relations, the full three-report comparison space, accidental state
  equivalence after refinement, exact regularity counts, and output symmetry.
- `lean4/WitnessedDifference/RetentionChoices.lean` compiles standalone with
  Lean **4.33.1**. Its **17 theorem proofs** establish structural recombination,
  greatest forward compatibility, conditional equivalence, well-defined
  quotient updates, exact raw-readout descent, fixed-point correctness,
  output-selection obstruction, and the explicit nontransitive countermodel.
  `lean4/retention_choices_axioms.txt` records source SHA-256 and **34** explicit
  declarations/constructors/fields; axiom union is `{propext, Quot.sound}`.

These results classify typed extension choices and their dependence under
named additional laws. They do not assert that arbitrary predicates about
retention, arbitrary untyped realizations, or physical memory mechanisms are
independent. They assign no HoTT equivalence, Kan condition, chronology, or
physical authority to a tolerance relation.
