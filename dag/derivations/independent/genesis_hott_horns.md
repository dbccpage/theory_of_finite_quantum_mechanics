Status: AI-drafted, awaiting human review.

# Finite horns and a 0-truncated identity fragment

AuthorityEffect: None.

The finite object is a semi-simplicial set with vertices `v0`, `v1`, `v2`, directed edges `e01 : v0 → v1`, `e12 : v1 → v2`, `e02 : v0 → v2`, `e20 : v2 → v0`, `e21 : v2 → v1`, and one 2-simplex `t012` whose faces are `d0 = e12`, `d1 = e02`, `d2 = e01`. On an edge, `d0` is the target and `d1` is the source. There are no degeneracy operators.

An inner 2-horn is a pair of edges `(d0, d2)` with `tgt d2 = src d0`. An outer 2-horn of index 0 is a pair `(d1, d2)` with the same source and distinct targets. An outer 2-horn of index 2 is a pair `(d0, d1)` with the same target. A filler is a 2-simplex with those faces. These are the dimension-2 horns that omit one face. Mathlib's `SSet.horn` is the general notion; it is not imported.

The edge `e01` is the witnessed pair of a `GenesisFspBridge.CarrierCut`: the relation holds only for `(v0, v1)` and is irreflexive, so `GenesisFspBridge.cut_endpoints_distinct` gives `v0 ≠ v1`. The third vertex is not related to anything by that relation. The other edges and `t012` are declared. They are not derived from the cut.

## Statement versus theorem

| Claim | Declaration | Verdict |
| --- | --- | --- |
| Genesis admission determines this simplicial object and its horn fillers | none | NOT PROVED |
| `e01` is an irreflexive witnessed pair and its endpoints are apart | `cut_endpoints_apart`, `cut_edge_no_loop` | NARROWED to that pair |
| `v2` is not in the cut relation | `third_vertex_not_in_cut` | FULL for this relation |
| No edge is a loop | `no_loop` | FULL for these five edges |
| Face-face identities on `t012` | `face_face_01`, `face_face_02`, `face_face_12` | FULL for this 2-simplex |
| Inner horn `(d0 = e12, d2 = e01)` has a filler | `inner_horn_filled` | FULL |
| Inner horn `(d0 = e01, d2 = e20)` has no filler | `inner_horn_refused` | FULL |
| Not every inner 2-horn fills | `not_all_inner_2_horns_fill` | FULL for this object |
| There are 8 inner horns and 1 filled inner horn | `innerHornList_length`, `innerFilledList_length` | FULL |
| The filled inner horn is exactly `(e12, e01)` | `unique_inner_filler` | FULL |
| Outer index-0 horn `(d1 = e02, d2 = e01)` has a filler | `outer_horn_k0_filled` | FULL |
| Outer index-0 horn `(d1 = e21, d2 = e20)` has no filler | `outer_horn_k0_refused` | FULL |
| Not every outer index-0 horn fills | `not_all_outer_k0_horns_fill` | FULL for this object |
| There are 4 outer index-0 horns and 1 filled | `outerK0List_length`, `outerK0FilledList_length` | FULL |
| Outer index-2 horn `(d0 = e12, d1 = e02)` has a filler | `outer_horn_k2_filled` | FULL |
| Every vertex is a source and a target | `every_source_1horn_fills`, `every_target_1horn_fills` | FULL for these three vertices |
| The full-boundary guard is strictly stronger than the inner-horn edge set | `shell2_stronger_than_inner_horn` | FULL for this guard |
| Every derivation of the identity fragment fits its type | `soundness` | FULL for the fragment below |
| Vertex path induction into `Sort u` | `vertex_id_elim` | NARROWED to equalities of `Vtx` |
| Vertex path induction into `Prop` | `vertex_id_elim_prop` | NARROWED to equalities of `Vtx` |
| Vertex equalities are subsingletons | `identity_zero_truncated` | FULL |
| Transport along `refl` is the identity | `transport_refl` | FULL |
| Reading edges as identity proofs refutes reflexivity | `edge_reading_refutes_refl` | FULL |
| No semantic value fits `Id(v0, v1)` | `no_path_between_cut_endpoints`, `id_cut_endpoints_uninhabited` | FULL |
| Two singleton carriers with distinct codes are not a univalent universe | `code_univalence_fails` | FULL for `BaseCode`; not a disproof of univalence |
| Object-language `J` for arbitrary types | none | NOT PROVED |
| Object-language function extensionality | none | NOT PROVED |
| Univalent universes | named import below | imported, NOT PROVED |
| ∞-groupoids | named import below | imported, NOT PROVED |
| (∞,1)-categories | named import below | imported, NOT PROVED |

## The carrier

Order the vertices of `t012` as `(v0, v1, v2)`. Deleting one vertex leaves an edge:

- delete `v0` and the remaining edge is `v1 → v2`, which is `e12`;
- delete `v1` and the remaining edge is `v0 → v2`, which is `e02`;
- delete `v2` and the remaining edge is `v0 → v1`, which is `e01`.

The three simplicial identities on a 2-simplex are the agreements of those endpoints. Each one is a direct comparison:

- `d0 d1 = d0 d0` sends both composite faces to `v2`;
- `d0 d2 = d1 d0` sends both to `v1`;
- `d1 d2 = d1 d1` sends both to `v0`.

The independent enumeration lists every ordered pair of the five edges. Eight pairs satisfy `tgt d2 = src d0`. Exactly one of them is `(e12, e01)`, the pair of faces of `t012`, so exactly one inner horn is filled and seven are refused. Four pairs have the same source and distinct targets. Exactly one of them is `(e02, e01)`, so exactly one outer index-0 horn is filled and three are refused. The index-2 pair `(e12, e02)` shares the target `v2` and is the remaining pair of faces of `t012`.

The refused inner horn is the composable pair `e20` then `e01` (`v2 → v0 → v1`). The only 2-simplex has `d2 = e01`, not `e20`. The refused outer horn is the pair `e21`, `e20`, both leaving `v2`, with targets `v1` and `v0`. Neither face list is the face list of `t012`.

Every vertex occurs as a source and as a target, so both kinds of 1-dimensional outer horn, which ask only for an edge with a prescribed source or target, are filled. That does not extend to dimension 2.

## What the cited guard does

`19L57G1:lean4/Derivation/HigherStructure.lean::shell2` is true when the three boundary edges of a triple are present and the 2-cell is absent. `shell_guard_load_bearing` refuses a 2-cell when that test fails. `ladder_dim2` says that if the test passes, the declared step adds the 2-cell. `filling_not_forced` says a complete horn does not create its filler by itself. `boundary_not_forced` gives two distinct boundary conventions on the same cell, both with vanishing composite boundary, so the boundary assignment is declared.

On this carrier the same shape is `boundaryEdges`: it demands `e01`, `e12`, and `e02` together. The inner-horn edge set `{e01, e12}` fails that test, so the guard does not admit a 2-cell. The full boundary `{e01, e12, e02}` passes, and the guard then allows a declaration. Allowing a declaration is not the presence of the 2-simplex. The simplex `t012` is still declared data.

This is why the cited calculus is not an inner-horn filling condition. An inner 2-horn specifies two edges. The cited guard requires three.

## The identity fragment

The syntax has constants `cst v` for the three vertices, one variable `bvar`, `refl`, `lam`, and `app`. Types are `vtx`, `Id(t1, t2)`, and `Π (_ : vtx), B`. A `Π` body may mention `bvar` inside an identity. Contexts are empty or one vertex variable. The derivation rules are the constant rule, the variable rule, reflexivity, lambda, application with substitution of a closed vertex term, and weakening of a closed judgment. There is no `J` constructor.

Substitution replaces free occurrences of `bvar` and does not enter a nested `lam`. A closed term does not use `bvar`, and its interpretation does not depend on the environment (`interp_closed`).

The interpretation takes values in vertices, formal paths `pth a b`, or functions `Vtx → Sem`. `cst v` denotes that vertex. `bvar` denotes the environment vertex. `refl t` denotes `pth v v` when `t` denotes `v`. `lam` denotes the function which interprets the body at each vertex. `app` denotes evaluation. `fits` says that a vertex value fits `vtx`, that `pth a b` fits `Id(t1, t2)` only when `a` and `b` are the denoted endpoints and `a = b`, and that a function fits a `Π` when every value fits the body.

`soundness` is the statement that every derivation, at every vertex environment, is interpreted by a value that fits its type. The checked fragment is exactly the six rules above.

`Id(v0, v1)` has no fitting semantic value, because a fitting path would force `v0 = v1`, contradicting the cut. Therefore no derivation of that type exists.

Reflexivity, transport along reflexivity, and path induction are available for equalities of vertices. `vertex_id_elim` is the ambient eliminator of Lean equality, at every universe level, with motive `C : (x : Vtx) → v0 = x → Sort u` or with any basepoint. `transport_refl` is the computation rule `Eq.rec c rfl = c`. `identity_zero_truncated` says there is at most one proof of `a = b`. In that sense the vertex type is 0-truncated and its identity types are mere propositions. The 2-simplex is not used as a 2-path.

The edge reading is not a model of identity. For every vertex there is no edge with that vertex as both source and target (`no_loop`, and for `e01` also the cut). A loop would be required for reflexivity if a 1-simplex were an identity proof.

`BaseCode` has two codes, `unitC` and `reflC`. `Unit` and the equality `v0 = v0` are singletons, with mutually inverse maps `u ↦ rfl` and `p ↦ ()`. The codes are not equal. So "identity of codes is bijection of carriers" fails for this two-code set. That is a fact about `BaseCode`. It is not a theorem about a univalent universe, and it is not an axiom denying univalence.

## Named imports

These are prose imports. They are not Lean axioms and they are not proved.

1. Univalent universes. Assume a universe `U` in which identity of types is equivalence of types. This would extend the finite code set `BaseCode`, where two codes with bijective singleton carriers are not equal. The finite set is an approximation of a universe of codes, not that universe. Status: imported, not proved.

2. ∞-groupoids. Assume a Kan complex: every horn, inner or outer, has a filler, in every dimension. This would extend the finite semi-simplicial set above, which refuses the inner horn `(e01, e20)` and the outer horn `(e21, e20)`. The finite set is not an ∞-groupoid. Status: imported, not proved.

3. (∞,1)-categories. Assume a quasi-category: every inner horn has a filler. This would extend the same finite set, which refuses an inner 2-horn. The finite set is not an (∞,1)-category. Status: imported, not proved.

## What is proved

On this finite semi-simplicial set, the face-face identities hold for `t012`. The inner horn of `(e01, e12)` and the outer horns of `(e01, e02)` are filled by `t012`. The inner horn of `(e20, e01)` and the outer horn of `(e20, e21)` are not filled. Of the 8 inner horns, 1 is filled. Of the 4 outer index-0 horns, 1 is filled. Every 1-dimensional source or target horn is filled. The full-boundary guard rejects the two-edge inner horn. The cut on `e01` has distinct endpoints, and `v2` lies outside that relation.

In the deep embedding, every derivation of the stated fragment interprets as a value of its type. Identity of the cut endpoints is empty. Vertex identity types are subsingletons. Path induction along those equalities holds for `Sort u` motives. Transport along reflexivity computes as the identity. The edge set does not interpret reflexivity.

## What is assumed

The carrier, its five edges, and `t012` are declared. The cut law used in Lean is irreflexivity of `endpointRel`, through `GenesisFspBridge.CarrierCut`. The ambient logic is Lean's, so the printed axioms are only `propext` where a proof uses propositional extensionality, and no axioms where it does not. No use of `Classical.choice` or `Quot.sound` appears in the printed lists.

The three named imports above are assumed only as labels for structures this finite object does not provide. Nothing in the Lean files postulates them.

Cited and not recompiled: `19L57G1:lean4/Derivation/HigherStructure.lean::shell2`, `::ladder_dim2`, `::shell_guard_load_bearing`, `::filling_not_forced`, and `::boundary_not_forced`. The local guard `admitTriGuard` repeats the shell shape on these five edges. It does not replay the passage history of that file.

## What is open

Genesis-determination of the simplicial object is not proved. A witnessed irreflexive pair does not supply `v2`, the extra edges, or `t012`.

Object-language identity elimination is not a rule of the fragment. `vertex_id_elim` does not add it. Function extensionality is not a rule of the fragment. There is no syntax of 2-paths, no higher inductive type, and no interpretation of `t012` as a homotopy. The sound model is 0-truncated. It is not claimed to be an ∞-groupoid, a univalent universe, or an (∞,1)-category.

Horn filling in dimensions above 2 is not stated. The Kan condition and the inner-horn condition fail in dimension 2 for this object; that does not classify any larger complex.
