Status: AI-drafted, awaiting human review.

# Finite combinatorial shadow of Genesis admission

AuthorityEffect: None.

The question is whether the Genesis admission structure determines a finite semi-simplicial set, a finite simplicial set, or a finite globular set. It does not. The largest finite object it does determine is the tuple shadow of a regime. This note says what that shadow is, which finite complexes were compared with it, and which comparisons are not theorems.

## The admitted state

The in-repo event semantics are `GenesisComputation.GenesisCopy`, cited there as a copy of `19L57G1:lean4/Derivation/Basic.lean`. A regime has five fields:

- `data`, a count of admitted data, whose internal names are the indices `0, …, data - 1`;
- `forms`, a list of judgment-form arities, each at least 1 when the admission step accepts the form;
- `insts`, a duplicate-free list of pairs `(form index, argument tuple)`;
- `rules`, a duplicate-free list of form indices carrying a uniform rule;
- `reqs`, a duplicate-free list of imposed pairs `(i, j)` with `i < j`.

Supply is the identity step. Replaying a list of events from the empty regime is therefore insensitive to supply events. The predicate `regimeWf` in the Lean module is the well-formedness predicate `Regime.wf` from that 19L57G1 file, restated because the in-repo copy does not contain it. It is not a new axiom.

`InertDiamond` is the three-event fragment: supply, admit a token, admit a form arity. Its state is a token list and an arity list. It has no argument tuples. `AdmissionFloor.ExhibitedCut` is a relation with two related endpoints and an irreflexivity law. `CellGrammar.ChainGrammar` is a two-step chain whose boundary maps are fields of the structure. `FiniteCochain` is one fixed triangle, with three integer edge slots, whose coboundary square is zero.

None of these sources says that a judgment form is a simplex, that an argument tuple is a list of faces, or that an imposed pair is a globe.

## What the regime determines

Define the tuple shadow of a regime to be the five-tuple `(data, forms, insts, rules, reqs)`. This is a function of the regime, and equal shadows come from equal regimes, because the shadow keeps every field. Concrete replays:

- Supply twice from the empty regime stays empty.
- The first-separation history (two data, one unary form, the instance `(0, [0])`, the requirement `(0, 1)`) ends at carrier 2, arities `[1]`, tuples `[(0, [0])]`, no rules, requirements `[(0, 1)]`. Every tuple has length 1, so none has length 2. The regime satisfies `regimeWf`.
- Admitting two data, one binary form, and the instance `(0, [0, 1])` ends at tuples `[(0, [0, 1])]`. The same history with arguments `[1, 0]` ends at tuples `[(0, [1, 0])]`. The two regimes have the same carrier and the same arity list, and both satisfy `regimeWf`. Their tuples differ.
- The fragment history “admit 0, admit 1, admit a form of arity 2” ends at token list `[0, 1]` and arity list `[2]`. That one state is the image of both binary regimes. The fragment does not store which order the arguments had.

So the six-operation regime determines ordered tuples. The three-event fragment does not. Neither record stores a face index, a source, a target, or a degeneracy.

## Finite complexes that were not determined

A degree-at-most-1 semi-simplicial set, in this note, is a pair of finite cardinalities and two face maps from the 1-simplices to the 0-simplices. There is no identity to impose in degree 1. A degree-at-most-1 globular set is the same data read as source and target. A degree-at-most-1 simplicial set adds a degeneracy section `s0` such that both faces of `s0(v)` are `v`. These are finite carriers. They are not presheaves, and this note does not call them Kan complexes.

On the binary edge regime the underlying ordered tuple is `(0, 1)` on a 2-element carrier, with one 1-cell if one chooses to read that tuple as a 1-cell. There are 4 maps `Fin 2 → Fin 1 → Fin 2`. Exactly 2 of them send the unique 1-simplex to the endpoint pair `{0, 1}`, namely face values `(1, 0)` and `(0, 1)`. Both readings are exhibited. The regime’s list stores the order `[0, 1]`, but it does not say which position is face 0. The same count holds for source and target: 4 pairs of maps `Fin 1 → Fin 2`, of which 2 swap the endpoints.

That endpoint reading is an import. It is used only to state the non-uniqueness. It is not derived from the admission step.

Even after the forward reading is chosen (face 0 has value 1, face 1 has value 0), a degeneracy is not in the regime. Two extensions satisfy `face i (s0 v) = v`:

- three 1-simplices: the edge, one loop at 0, one loop at 1, with `s0` selecting the loops;
- four 1-simplices: the same, plus a second loop at 0 which is not the value of `s0`.

The cardinalities 3 and 4 are different, so the extensions are different. The regime has no loop instance.

On that same forward 1-skeleton the three degree-2 face identities for a single 2-simplex fail for every choice of three (necessarily equal) 1-face indices, because the only edge has distinct endpoints and the identity `d0 d2 = d1 d0` would force those endpoints to agree. The empty extension in degree 2 is not the point of the theorem; the theorem is that no 2-simplex exists on that chosen skeleton. The regime did not choose the skeleton.

On the forward globe, both an empty set of 2-cells and a single 2-cell with equal source and target satisfy the globular identities. Their 2-cell counts are 0 and 1. Again this is after a source/target convention has been chosen.

The first-separation requirement is the single pair `(0, 1)`. Two irreflexive relations on `Fin 2` both relate 0 to 1: the one-way relation, and the symmetric relation. Both are exhibited cuts in the sense of `AdmissionFloor.ExhibitedCut`. The requirement list does not say which relation it is. Separately, `CellGrammar` admits at least two chain grammars on carriers `Fin 2`, `Fin 1`, and `Empty`, with boundary square vacuous and with different degree-1 boundaries (constant 0 and constant 1). `FiniteCochain.d1_d0_zero` is the nilpotence identity for the fixed three-edge triangle; the edge regime has one tuple, not three. That identity is not a shadow of the regime.

## Counts recomputed outside Lean

`checks/independent/genesis_hott_shadow.py` replays the same histories and enumerates the same finite maps. It does not import this repository. The counts it checks are: empty replay after two supplies; the first-separation shadow and the unary length; the two binary shadows; fragment state `([0, 1], [2])`; 4 face maps and 2 endpoint orientations; 4 globular pairs and 2 orientations; degeneracy equations for the extensions of sizes 3 and 4; failure of the three 2-simplex identities on the constant face map `Fin 3 → Fin 1`; the two cut relations; the triangle evaluation `d1(d0(0,1,2)) = 0`.

## Statement versus theorem

| Claim | Lean declaration | Verdict |
| --- | --- | --- |
| A regime and its tuple shadow determine each other. | `shadow_eq_iff` | FULL |
| Supply does not change a regime or its shadow. | `supply_preserves_shadow`, `replay_cons_supply`, `supply_history_stays_empty` | FULL |
| The first-separation history determines the unary shadow above, with no binary tuple, and the regime is well-formed. | `first_separation_shadow`, `first_separation_shadow_of_replay`, `first_separation_tuples_are_unary`, `first_separation_no_binary_tuple`, `first_separation_wf` | FULL |
| The two binary histories determine two well-formed regimes with the same carrier and arities and different tuples. | `edge_replay`, `reverse_edge_replay`, `edge_wf`, `reverse_edge_wf`, `edge_and_reverse_differ` | FULL |
| The three-event fragment does not store that argument order. | `fragment_replay`, `fragment_does_not_store_argument_order` | FULL |
| The binary edge regime determines a unique degree-≤1 semi-simplicial set. | not proved. The negative is `edge_regime_does_not_determine_semisimplicial1`, with `face_map_card` = 4 and `recovers_fun_card` = 2 | NOT PROVED. The negative is FULL |
| The binary edge regime determines a unique degree-≤1 globular set. | not proved. The negative is `edge_regime_does_not_determine_globular1`, with `globular_pair_card` = 4 and `globular_orientation_count` = 2 | NOT PROVED. The negative is FULL |
| The forward edge extends uniquely by a degeneracy. | not proved. `faceA_s0`, `faceB_s0`, `simplicial_extensions_not_unique` give two extensions, of sizes 3 and 4 | NARROWED to a chosen reading. Determination is NOT PROVED |
| That forward 1-skeleton carries a 2-simplex. | `no_simplex2_on_forward_edge` | NARROWED. The non-existence is FULL for that skeleton only |
| The forward globe extends uniquely by 2-cells. | `globe2_not_unique` | NARROWED. The negative is FULL for that globe only |
| The requirement `(0, 1)` determines one exhibited cut. | not proved. `requirement_does_not_determine_cut` | NOT PROVED. The negative is FULL |
| The edge shadow determines a `ChainGrammar` boundary, or is the `FiniteCochain` triangle. | not proved. `chain_boundaries_differ` and `triangle_nilpotence_not_edge_tuple` separate those existing objects from the shadow | NOT PROVED |
| The regime determines an object of Mathlib `SSet`, a semi-simplicial presheaf, or a globular set in every degree. | not proved | NOT PROVED |
| Horn fillers exist for any of these finite carriers. | not proved | NOT PROVED |

## What is proved

The tuple shadow is a function of the regime and determines it. Supply is inert for replay. The first-separation regime and the two binary regimes are the replays of the histories above and satisfy the restated well-formedness predicate. The three-event fragment collapses the two argument orders. Relative to the imported endpoint reading, the binary regime does not select a unique degree-≤1 face assignment or a unique source and target assignment: there are 4 candidates and 2 endpoint-preserving ones in each case. After one face convention is chosen, degeneracy extensions of sizes 3 and 4 both satisfy the degree-1 degeneracy equations, no 2-simplex satisfies the three face identities, and both 0 and 1 two-cells satisfy the globular identities on the forward globe. The requirement `(0, 1)` is shared by two different exhibited cuts. Two chain grammars differ, and the triangle nilpotence identity is not the one-tuple edge shadow.

## What is assumed

The event step is the cited `GenesisCopy.stepE`. `regimeWf` is the cited 19L57G1 predicate, copied rather than imported. The endpoint reading, the face-index convention (omit vertex `i`, as for `SimplexCategory.δ`), and the names “semi-simplicial”, “simplicial”, and “globular” for these finite carriers are imports. No equivalence with Mathlib `SSet` is assumed or proved. The kernel axioms used by the module are among `propext`, `Classical.choice`, and `Quot.sound`.

## What is open

No derivation produces a face map, a source, a target, or a degeneracy from a regime. The passage from the tuple shadow to a Mathlib simplicial set, to a semi-simplicial presheaf, or to a globular set in unbound degree is not proved. Horn filling is not proved. The three-event fragment does not determine the ordered tuples that the six-operation regime does determine. Nothing here identifies a finite carrier with an ∞-groupoid.
