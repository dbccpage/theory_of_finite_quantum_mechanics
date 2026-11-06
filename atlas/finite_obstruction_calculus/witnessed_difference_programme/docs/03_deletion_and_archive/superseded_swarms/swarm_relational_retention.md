# Relational retention, bisimulation, and the succession boundary

## Scope of the Chapter 6 obligation

CH06-O01 asks for a succession packet from an explicitly order-free retention
package, or a proof that a named additional order input is necessary. Chapter 3
now classifies total deterministic labelled packets. Bisimulation alone does
not settle the Chapter 6 question: it classifies admitted transitions rather
than selecting their direction. The results here therefore supply both a
broader finite relational classification and an explicit succession boundary.

The admitted packet is `(M, I, T, r, ≈)`, where `M` is finite and nonempty,
`I` is a finite label set, and `T_i ⊆ M × M` is a declared directed relation
for each label. Successor sets may be empty or branching; no total update map,
initial state, global chronology, or linear clock is required. Reports use
exact equality, or an explicitly checked report equivalence `≈` which is
quotiented before refinement. A merely reflexive symmetric tolerance is not
silently replaced by its transitive closure.

The directed relations `T_i` are the named additional directional input. The
construction does not derive them from the carrier or its reports. A carrier
index is an implementation identifier and is not constitutive succession.

## Greatest report-respecting strong bisimulation

A relation `R` is a report-respecting strong bisimulation if `x R y` entails
equal report classes and, for every label, every successor of `x` has an
`R`-related successor of `y`, and conversely. Empty successor sets are included
in both conditions. The existential matching concerns successor states rather
than numbers of duplicate edges; transitions are sets.

Let `B` be the union of every such bisimulation. Unions preserve the matching
property: each related pair has a witnessing constituent bisimulation, and
its successor matches lie in that constituent and hence in the union.
Identity is a bisimulation. Converses preserve bisimulation by exchanging
forth and back. Composites preserve bisimulation by composing the two
successor witnesses and their report equalities. These three facts prove that
`B` is reflexive, symmetric, and transitive. It is the greatest bisimulation,
not simply a greatest equivalence among a restricted search family.

For finite computation, begin at `R₀ = ker(r)` and iterate

`Rₖ₊₁ = Rₖ ∩ {pairs with two-sided successor matching into Rₖ}`.

Each round remains an equivalence: reflexivity matches a successor with itself;
symmetry exchanges matching directions; transitivity composes the matching
witnesses. The chain descends. Every bisimulation is contained in `R₀` and,
inductively, in every subsequent relation. A stationary round is itself a
bisimulation, and therefore equals `B`. For `n = |M|`, every strict round
splits at least one partition block. Starting with `b₀` blocks, at most
`n − b₀ ≤ n − 1` strict rounds occur. This is a mathematical termination proof;
the Lean fixed-point theorem and equivalence-preservation theorem formalize
its structural premises, while the numerical finite-block count is stated
and proved here rather than claimed as a Lean theorem.

The native implementation uses successor **block sets** as signatures, rather
than searching arbitrary relations. Equal signatures are exactly the two-sided
matching criterion for an equivalence partition. Signature enumeration can
rename blocks but cannot change the relation. The receipt verifier replays
the complete chain from the actual packet. A stable unnecessarily fine
partition, a truncated chain, or a forged quotient is refused.

## Quotient and behavioral classification

The quotient has report `r([x]) = r(x)` and a labelled edge `[x] → [y]` exactly
when a representative edge exists. Bisimulation's back condition proves that
every chosen source representative has a successor in every reported target
class. Thus the quotient transition is independent of representatives and
the quotient map is a surjective bounded morphism: the image of each source
successor set is exactly the corresponding target successor set.

For any other surjective report-preserving bounded morphism `f : M → N`, its
kernel is a bisimulation. Indeed, for `f(x)=f(y)`, the image of a successor of
`x` is a successor of `f(y)`; the back condition at `y` supplies a successor
with the same image. The converse direction is identical. Thus `ker(f) ⊆ B`,
and `[x]` defines a unique map `N → M/B` with `q = factor ∘ f`. Surjectivity of
`f` proves uniqueness. This map is again report-preserving and bounded by
lifting a target successor to a source successor and then projecting it.
The direction is from every finer quotient to the coarsest behavioral
quotient; this is not the constructor-increment initiality claim CH04-O01.

For two systems with common label interpretation and common report IDs,
compute greatest bisimulation on their disjoint union. They represent the
same unpointed behavior set exactly when each component represents the same
set of union classes. This is equivalent to report- and label-preserving
isomorphism of their minimal quotients: a matching class determines its unique
quotient state and the two-sided successor sets. No initial state is chosen.

Strong bisimilarity is stricter than equality of finite traces. The Python
witness compares `a.(b+c)` with `(a.b)+(a.c)`: both have the same complete
finite trace set in this depth-two acyclic instance, but their intermediate
branching states cannot be bisimulated. Forward edge-preserving maps are
also insufficient for the quotient theorem. A deadlocked state mapped to a
looping target preserves every existing edge vacuously, but fails the back
condition and is refused by the native factor verifier.

## Succession from the admitted relation, and necessity of directional input

Let `E = ⋃ᵢ T_i`. Nonempty directed reachability is transitive by path
concatenation. It is irreflexive exactly when `E` has no directed cycle.
Consequently a strict partial order containing **all** admitted edges exists
on the original memory carrier exactly when this graph is acyclic. In that
case nonempty reachability is its least such order. A cycle refutes every
irreflexive transitive extension containing those edges, not just one proposed
reachability implementation.

For a cyclic graph, mutual reflexive reachability defines SCC equivalence.
On the component carrier, define `A < B` by reachability between distinct
components. Representative independence follows by composing paths inside
the source and target SCCs. This order is irreflexive; a return path would
merge the components. It is transitive; if the first and third components
coincided, the intermediate component would merge with them. The SCC quotient
therefore constructs a succession packet on a **changed carrier**. Internal
cycle edges project to equality and are not claimed to be strict succession.
A strongly connected graph yields a one-component empty strict order, which
supplies no nontrivial succession. A fork supplies a partial order whose two
leaves remain incomparable; enumeration does not select an order between them.

For a bare finite memory carrier with constant reports and no directed
relation, every state permutation is an automorphism. If a putative strict
order is invariant under the transposition swapping `x` and `y`, then
`x < y` entails `y < x`, contradicting asymmetry. Applying this to every
distinct pair proves that a permutation-invariant strict order is empty.
Thus a directed transition relation, a report-order structure, or another
explicit symmetry-breaking input is necessary for nontrivial succession in
that fully symmetric input class. The Lean swap theorem proves the local
obstruction without presupposing a clock. For structured retention packets,
the relevant automorphism group may be smaller; no claim that every such
packet retains the full symmetric group is made.

This answers the finite relational construction/classification and the named
symmetry obstruction. It does not infer a unique transition relation from
arbitrary retention data, physical causal structure, continuum topology,
duration, or experienced passage. These are the original Chapter 6 scope
boundaries, and should not be removed by promoting the bisimulation theorem.
The quotient is an ordinary set-level quotient. It proves neither HoTT
equivalence, univalence, homotopy coherence, nor Kan fibrancy.

## Implementations and executed checks

- Native owner: `omega_category_theory/src/finite_relational.rs`.
  Production command: `cargo test -p omega_category_theory --lib
  finite_relational::tests -- --nocapture`: **5 passed**. Its exhaustive test
  checks all `8 × 512 = 4096` three-state one-label graphs with binary reports,
  against all five equivalence partitions, the refinement-round bound, SCC
  strict-order laws, and raw/behavioral-quotient acyclicity agreement.
- Thin WDP adapter: `omega_wdp/src/relational_retention.rs`.
  Production command: `cargo test -p omega_wdp --lib
  relational_retention::tests -- --nocapture`: **2 passed**. Tests cover
  branching fork succession and refusal of nontransitive report tolerance.
- Independent hermetic witness: `code/witnessed_difference/relational_retention.py`.
  Command: `PYTHONPATH=code python -m pytest
  code/unit_tests/test_relational_retention.py -q --no-cov -n0`:
  **12 passed**. Besides all 4096 three-state instances, it exhausts every
  arbitrary relation on all 64 two-state graph/report instances, verifies the
  union characterization, and tests relabelling, trace/bisimulation separation,
  cycles, deadlock, invalid data, empty alphabets, and forged receipts.
- Formal source: `lean4/WitnessedDifference/RelationalRetention.lean`.
  Standalone Lean **4.33.1** compilation exits **0**. Its 19 theorem proofs
  cover equivalence, greatestness, equivalence-preserving refinement,
  stabilized-approximation correctness, quotient representative independence,
  unique comparison, raw-cycle obstruction, and swapping-symmetry obstruction.
  The separate `lean4/relational_retention_axioms.txt` records the source
  SHA-256 and all 31 explicit declarations/constructors; dependency union is
  `{propext, Quot.sound}`. No admitted proof or custom axiom is used.

The standalone Lean module has not been represented as a freshly rebuilt
Mathlib-dependent package, and the historical package axiom receipt is left
intact. These test commands are targeted checks, not a whole-estate test sweep.
