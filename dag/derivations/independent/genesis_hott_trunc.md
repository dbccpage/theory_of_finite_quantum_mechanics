Status: AI-drafted, awaiting human review.

# Finite truncated homotopy data

**AuthorityEffect:** None.

**Lean module:** `lean4/GenesisHottTruncation.lean`

**Independent check:** `checks/independent/genesis_hott_trunc.py`

**Replay:** `dag/research/genesis_hott_trunc_lean_replay.json`

Citations used as declaration windows, not re-proved:

- `theory_of_finite_quantum_mechanics:lean4/AdmissionFloor.lean::AdmissionFloor.ExhibitedCut`
- `theory_of_finite_quantum_mechanics:lean4/AdmissionFloor.lean::AdmissionFloor.endpoints_apart`
- `theory_of_finite_quantum_mechanics:lean4/PregenConstructive.lean::PregenConstructive.recon`
- `theory_of_finite_quantum_mechanics:lean4/PregenConstructive.lean::PregenConstructive.FiberConstantOn`
- `theory_of_finite_quantum_mechanics:lean4/ChainRetraction.lean::ChainRetraction.TwoPoints.cls` (cited only)
- Mathlib `SSet`, `CategoryTheory.nerve`, `CategoryTheory.Groupoid`, `CategoryTheory.SingleObj.groupoid`

## Finite graphs

Vertices are `Fin 3`. Dimension 1.

The cut-edge graph has one undirected edge, `{0,1}`. Vertex `2` is isolated. The relation is symmetric and irreflexive, and it is an `AdmissionFloor.ExhibitedCut` with endpoints `0` and `1`. Those endpoints are apart by `AdmissionFloor.endpoints_apart`.

A walk of length at most 2 joins `i` and `j` if and only if they receive the same label: `0` and `1` receive label `0`, and `2` receives label `1`. The set of labels is `{0,1}`, so this graph has two path-components. Truncation level 0.

The path graph `0—1—2` is also an exhibited cut (it relates `0` and `1`, and it is irreflexive). Every pair of vertices is joined by a walk of length at most 2, so it has one path-component.

The two relations are both exhibited cuts and have different path-component counts, 2 and 1. Existence of an exhibited cut does not determine π₀. The claim that Genesis admission determines π₀ on every carrier is not proved.

## Fundamental groupoid of the cut-edge forest

Dimension 1. The data are a 1-groupoid, not an ∞-groupoid. Because every endomorphism is the identity arrow, the homotopy type is 0-truncated.

Reduced paths are five labels: stay at `0`, stay at `1`, stay at `2`, the edge `0→1`, and the edge `1→0`. There is no label from `0` to `2`. For each ordered pair there is at most one such label, and a label exists if and only if the endpoints lie in one path-component.

The groupoid has objects the three vertices and one arrow for each of those five pairs. Composition and inverses are the component-label operations: an inverse cancels. Mathlib's `Groupoid` class is instantiated; it is not re-proved. The arrow count is 5.

`PregenConstructive.recon`, applied to the list `[0,1,2]` with report and answer equal to the component label, returns `some 0` for label `0` and `some 1` for label `1`. The label is fiber-constant on that list. This does not derive path-components from the history-report criterion in general.

`ChainRetraction.TwoPoints.cls` is not identified with this π₀.

## One finite 1-type

Dimension 1, truncation level 1. Not an ∞-groupoid.

Mathlib's `SingleObj (Multiplicative (ZMod 2))` is a groupoid with a subsingleton of objects and two endomorphisms. The element `ofAdd 1` is not the identity, and its square is the identity. That is a finite presentation of one 1-type by the multiplication table of `ZMod 2`. It is not the cut-edge fundamental groupoid: the cut-edge vertex `0` has only the identity endomorphism, while this 1-type has two endomorphisms, and the cut-edge groupoid has three objects and five arrows.

A general n-type is not presented. `IsSSetTruncatedAt n X` says only that Mathlib's `SSet.truncation` produces an `n`-truncated simplicial set equal to the truncation of `X`. The predicate holds for every simplicial set and every `n`.

Mathlib's `nerveEquiv` identifies the 0-simplices of the nerve of this one-object groupoid with its objects. The nerve at truncation level 1 satisfies the truncation predicate. No Kan filler, no homotopy group above dimension 1, and no ∞-groupoid is constructed.

## What is proved

On the cut-edge graph: two path-components, five arrows in a finite fundamental groupoid, trivial endomorphisms, and agreement of arrows with reduced-path labels. On the path graph: one path-component. On `SingleObj (Multiplicative (ZMod 2))`: two endomorphisms and the relation `g * g = 1`. The truncation predicate holds for every simplicial set, including the nerve of that 1-type. Two exhibited cuts have different π₀ counts.

## What is assumed

Mathlib's category, groupoid, simplicial-set, nerve, and `ZMod` constructions, used as cited and not re-proved. The standard Lean axioms recorded by `#print axioms` are `propext`, `Classical.choice`, and `Quot.sound`. The edge relations and the group `ZMod 2` are supplied data. They are not derived from an exhibited cut alone.

## What is open

Genesis admission does not, in this file, determine π₀, the fundamental groupoid, or the 1-type. The identification of `ChainRetraction.TwoPoints.cls` with π₀ is open. A general presentation of n-types is open. Horn filling, a Kan complex, and any ∞-groupoid are open. The nerve is used only through `nerveEquiv` at dimension 0 and through the truncation predicate at level 1.

## Statement versus theorem

| Statement | Declaration | Verdict |
| --- | --- | --- |
| Cut-edge graph on `Fin 3` has two path-components (dimension 1, truncation level 0) | `GenesisHottTruncation.cut_edge_pi0_card`, `walkCut_iff_component` | FULL for this graph |
| Path graph `0—1—2` has one path-component (dimension 1, truncation level 0) | `GenesisHottTruncation.path_edge_pi0_card` | FULL for this graph |
| Finite fundamental groupoid of the cut-edge forest: 3 objects, 5 arrows, inverses cancel, endomorphisms are identities (dimension 1; 1-groupoid, homotopy truncation level 0; not an ∞-groupoid) | `cut_vertex_card`, `cut_groupoid_morphism_count`, `cut_inv_cancels`, `cut_endomorphism_trivial`, `cut_arrow_iff_label` | FULL for this graph |
| One finite 1-type with carrier a subsingleton and endomorphism group of order 2 (dimension 1, truncation level 1; not an ∞-groupoid) | `bz2_object_subsingleton`, `bz2_morphism_card`, `bz2_generator_square` | FULL for this one groupoid |
| That 1-type is not the cut-edge fundamental groupoid | `bz2_is_not_cut_edge_groupoid` | FULL |
| Exhibited-cut data determine π₀ | `exhibited_cut_does_not_determine_pi0` separates two cuts | NOT PROVED; the finite separation is proved |
| `ChainRetraction.TwoPoints.cls` is this π₀ | none | NOT PROVED |
| A general n-type is presented | `IsSSetTruncatedAt`, `sset_truncation_predicate_is_not_a_presentation` | NOT PROVED; the predicate holds for every `SSet` |
| The nerve is an ∞-groupoid or a Kan complex | `bz2_nerve_zero_simplices_equiv_objects`, `bz2_nerve_satisfies_truncation_predicate` | NARROWED to 0-simplices and the level-1 truncation predicate |
