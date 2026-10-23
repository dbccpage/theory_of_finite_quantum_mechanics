import AdmissionFloor
import PregenConstructive
import Mathlib.Algebra.Group.TypeTags.Finite
import Mathlib.AlgebraicTopology.SimplicialSet.Basic
import Mathlib.AlgebraicTopology.SimplicialSet.Nerve
import Mathlib.CategoryTheory.Groupoid
import Mathlib.CategoryTheory.SingleObj
import Mathlib.Data.Fintype.Card
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.FinCases

/-!
# Finite truncated homotopy data

AuthorityEffect: None.

Finite objects built from cited primitives, not from a general Genesis-admission
theorem. Citations, not re-proofs:

* `theory_of_finite_quantum_mechanics:lean4/AdmissionFloor.lean::AdmissionFloor.ExhibitedCut`
* `theory_of_finite_quantum_mechanics:lean4/AdmissionFloor.lean::AdmissionFloor.endpoints_apart`
* `theory_of_finite_quantum_mechanics:lean4/PregenConstructive.lean::PregenConstructive.FiberConstantOn`
* `theory_of_finite_quantum_mechanics:lean4/PregenConstructive.lean::PregenConstructive.recon`
* `theory_of_finite_quantum_mechanics:lean4/ChainRetraction.lean::ChainRetraction.TwoPoints.cls`
  is cited and not used. Identification of that homology class with π₀ is NOT PROVED.
* Mathlib `SSet` (`Mathlib/AlgebraicTopology/SimplicialSet/Basic.lean`)
* Mathlib `CategoryTheory.nerve` (`Mathlib/AlgebraicTopology/SimplicialSet/Nerve.lean`)
* Mathlib `CategoryTheory.Groupoid` (`Mathlib/CategoryTheory/Groupoid.lean`)
* Mathlib `CategoryTheory.SingleObj.groupoid` (`Mathlib/CategoryTheory/SingleObj.lean`)

The cut-edge fundamental groupoid below is a 1-groupoid with finitely many arrows.
It is not an ∞-groupoid. The one-object groupoid `SingleObj (Multiplicative (ZMod 2))`
is one finite 1-type. `IsSSetTruncatedAt` is only Mathlib's truncation functor
applied to a simplicial set; it is not a presentation of a general n-type.
-/

open CategoryTheory

namespace GenesisHottTruncation

/-- Dimension 1. The cut-edge graph on three vertices: one undirected edge `{0,1}`. -/
def cutEdge (i j : Fin 3) : Bool :=
  (i == 0 && j == 1) || (i == 1 && j == 0)

/-- Dimension 1. The path graph `0—1—2`. -/
def pathEdge (i j : Fin 3) : Bool :=
  (i == 0 && j == 1) || (i == 1 && j == 0) || (i == 1 && j == 2) || (i == 2 && j == 1)

/-- Dimension 1, truncation level 0. Label of the cut-edge path-component. -/
def cutComponent (i : Fin 3) : Fin 2 :=
  if i = 2 then 1 else 0

/-- Dimension 1, truncation level 0. Walks of length at most 2 on `cutEdge`. -/
def walkCut (i j : Fin 3) : Bool :=
  i == j || cutEdge i j ||
    ((cutEdge i 0 && cutEdge 0 j) || (cutEdge i 1 && cutEdge 1 j) ||
      (cutEdge i 2 && cutEdge 2 j))

/-- Dimension 1, truncation level 0. Walks of length at most 2 on `pathEdge`. -/
def walkPath (i j : Fin 3) : Bool :=
  i == j || pathEdge i j ||
    ((pathEdge i 0 && pathEdge 0 j) || (pathEdge i 1 && pathEdge 1 j) ||
      (pathEdge i 2 && pathEdge 2 j))

/-- Dimension 1, truncation level 0.
`cutEdge` is symmetric. -/
theorem cut_edge_symmetric (i j : Fin 3) : cutEdge i j = cutEdge j i := by
  fin_cases i <;> fin_cases j <;> decide

/-- Dimension 1, truncation level 0.
`cutEdge` is irreflexive, so it can carry an exhibited-cut law. -/
theorem cut_edge_irreflexive (i : Fin 3) : cutEdge i i = false := by
  fin_cases i <;> decide

/-- Dimension 1, truncation level 0.
`pathEdge` is symmetric. -/
theorem path_edge_symmetric (i j : Fin 3) : pathEdge i j = pathEdge j i := by
  fin_cases i <;> fin_cases j <;> decide

/-- Dimension 1, truncation level 0.
`pathEdge` is irreflexive. -/
theorem path_edge_irreflexive (i : Fin 3) : pathEdge i i = false := by
  fin_cases i <;> decide

/-- Dimension 1, truncation level 0.
The cut-edge relation is an `AdmissionFloor.ExhibitedCut` on `Fin 3`. -/
def cutEdgeExhibited : AdmissionFloor.ExhibitedCut (Fin 3) where
  relation := fun i j => cutEdge i j = true
  first := 0
  second := 1
  exhibited := by decide
  protectedLaw := by
    intro x
    fin_cases x <;> decide

/-- Dimension 1, truncation level 0.
The path-edge relation is an `AdmissionFloor.ExhibitedCut` on `Fin 3`. -/
def pathEdgeExhibited : AdmissionFloor.ExhibitedCut (Fin 3) where
  relation := fun i j => pathEdge i j = true
  first := 0
  second := 1
  exhibited := by decide
  protectedLaw := by
    intro x
    fin_cases x <;> decide

/-- Dimension 1, truncation level 0.
The exhibited cut-edge endpoints are apart, by `AdmissionFloor.endpoints_apart`. -/
theorem cut_edge_endpoints_apart :
    cutEdgeExhibited.first ≠ cutEdgeExhibited.second :=
  AdmissionFloor.endpoints_apart cutEdgeExhibited

/-- Dimension 1, truncation level 0.
Length-at-most-2 walks on `cutEdge` are exactly equality of component labels. -/
theorem walkCut_iff_component (i j : Fin 3) :
    walkCut i j = true ↔ cutComponent i = cutComponent j := by
  fin_cases i <;> fin_cases j <;> decide

/-- Dimension 1, truncation level 0.
The cut-edge walk relation is reflexive. -/
theorem walkCut_refl (i : Fin 3) : walkCut i i = true := by
  fin_cases i <;> decide

/-- Dimension 1, truncation level 0.
The cut-edge walk relation is symmetric. -/
theorem walkCut_symm (i j : Fin 3) : walkCut i j = walkCut j i := by
  fin_cases i <;> fin_cases j <;> decide

/-- Dimension 1, truncation level 0.
The cut-edge walk relation is transitive on this three-vertex graph. -/
theorem walkCut_trans (i j k : Fin 3) (hij : walkCut i j = true) (hjk : walkCut j k = true) :
    walkCut i k = true := by
  fin_cases i <;> fin_cases j <;> fin_cases k <;> revert hij hjk <;> decide

/-- Dimension 1, truncation level 0.
An edge is a walk. -/
theorem cutEdge_implies_walk (i j : Fin 3) (h : cutEdge i j = true) : walkCut i j = true := by
  fin_cases i <;> fin_cases j <;> revert h <;> decide

/-- Dimension 1, truncation level 0.
Component labels attained on the cut-edge graph, with duplicates removed by hand. -/
def cutPi0 : List (Fin 2) := [0, 1]

/-- Dimension 1, truncation level 0.
Every vertex label lies in `cutPi0`, both labels occur, and the list has length 2. -/
theorem cut_edge_pi0_card :
    cutPi0.length = 2 ∧ cutPi0.Nodup ∧
      (∀ i : Fin 3, cutComponent i ∈ cutPi0) ∧
      (0 : Fin 2) ∈ cutPi0 ∧ (1 : Fin 2) ∈ cutPi0 := by
  refine ⟨rfl, ?_, ?_, ?_, ?_⟩
  · decide
  · intro i
    fin_cases i <;> decide
  · decide
  · decide

/-- Dimension 1, truncation level 0.
On the path graph every pair is joined by a walk of length at most 2. -/
theorem walkPath_all (i j : Fin 3) : walkPath i j = true := by
  fin_cases i <;> fin_cases j <;> decide

/-- Dimension 1, truncation level 0.
The path graph has one path-component label. -/
def pathPi0 : List (Fin 1) := [0]

/-- Dimension 1, truncation level 0.
`pathPi0` has length 1, and every vertex pair lies in that one component. -/
theorem path_edge_pi0_card :
    pathPi0.length = 1 ∧ (∀ i j : Fin 3, walkPath i j = true) :=
  ⟨rfl, walkPath_all⟩

/-- Dimension 1, truncation level 0.
Two exhibited cuts on `Fin 3` have path-component counts 2 and 1.
Existence of `AdmissionFloor.ExhibitedCut` does not determine π₀.
The claim that Genesis admission determines π₀ on every carrier is NOT PROVED. -/
theorem exhibited_cut_does_not_determine_pi0 :
    cutEdgeExhibited.relation cutEdgeExhibited.first cutEdgeExhibited.second ∧
      pathEdgeExhibited.relation pathEdgeExhibited.first pathEdgeExhibited.second ∧
      cutPi0.length = 2 ∧ pathPi0.length = 1 ∧ cutPi0.length ≠ pathPi0.length := by
  refine ⟨cutEdgeExhibited.exhibited, pathEdgeExhibited.exhibited, rfl, rfl, ?_⟩
  decide

/-- Dimension 1, truncation level 1.
Reduced paths on the cut-edge graph: a stay at one vertex, or the single edge
in either direction. Backtracking is not a constructor. -/
inductive RedLabel : Type where
  | stay0
  | stay1
  | stay2
  | edge01
  | edge10
deriving DecidableEq

/-- Dimension 1, truncation level 1. Source of a reduced path. -/
def redSrc : RedLabel → Fin 3
  | .stay0 => 0
  | .stay1 => 1
  | .stay2 => 2
  | .edge01 => 0
  | .edge10 => 1

/-- Dimension 1, truncation level 1. Target of a reduced path. -/
def redTgt : RedLabel → Fin 3
  | .stay0 => 0
  | .stay1 => 1
  | .stay2 => 2
  | .edge01 => 1
  | .edge10 => 0

/-- Dimension 1, truncation level 1.
The reduced path from `i` to `j`, if one exists. -/
def labelOf (i j : Fin 3) : Option RedLabel :=
  if i = 0 ∧ j = 0 then some .stay0
  else if i = 0 ∧ j = 1 then some .edge01
  else if i = 1 ∧ j = 0 then some .edge10
  else if i = 1 ∧ j = 1 then some .stay1
  else if i = 2 ∧ j = 2 then some .stay2
  else none

/-- Dimension 1, truncation level 1.
A chosen reduced path has the requested endpoints. -/
theorem labelOf_src_tgt (i j : Fin 3) (p : RedLabel) (h : labelOf i j = some p) :
    redSrc p = i ∧ redTgt p = j := by
  fin_cases i <;> fin_cases j <;> cases p <;> revert h <;> decide

/-- Dimension 1, truncation level 1.
A reduced path exists if and only if the vertices lie in one component. -/
theorem labelOf_some_iff_component (i j : Fin 3) :
    (labelOf i j).isSome = true ↔ cutComponent i = cutComponent j := by
  fin_cases i <;> fin_cases j <;> decide

/-- Dimension 1, truncation level 1.
There is no reduced path from `0` to `2`. -/
theorem labelOf_0_2 : labelOf 0 2 = none := by
  decide

/-- Dimension 1, truncation level 1.
At most one reduced-path label joins a given ordered pair. -/
theorem red_label_agrees (i j : Fin 3) (a b : RedLabel)
    (ha : labelOf i j = some a) (hb : labelOf i j = some b) : a = b :=
  Option.some_injective _ (ha.symm.trans hb)

/-- Dimension 1. Vertices of the cut-edge graph, tagged for the groupoid instance. -/
structure CutVertex where
  idx : Fin 3

/-- Dimension 1, truncation level 1.
The cut-edge graph has three vertices. -/
def cutVertexEquiv : CutVertex ≃ Fin 3 where
  toFun v := v.idx
  invFun i := ⟨i⟩
  left_inv _ := rfl
  right_inv _ := rfl

instance : Fintype CutVertex :=
  Fintype.ofEquiv (Fin 3) cutVertexEquiv.symm

/-- Dimension 1, truncation level 1.
Three vertices. -/
theorem cut_vertex_card : Fintype.card CutVertex = 3 := by
  rw [Fintype.card_congr cutVertexEquiv]
  exact Fintype.card_fin 3

/-- Dimension 1, truncation level 1.
An arrow exists precisely when the endpoints lie in one path-component.
`token` is the only element of `Fin 1`, so there is at most one arrow. -/
structure CutArrow (x y : CutVertex) : Type where
  same : cutComponent x.idx = cutComponent y.idx
  token : Fin 1

instance (x y : CutVertex) : Subsingleton (CutArrow x y) :=
  ⟨fun ⟨_, t1⟩ ⟨_, t2⟩ => by
    fin_cases t1
    fin_cases t2
    rfl⟩

/-- Dimension 1, truncation level 1.
Finite fundamental groupoid of the cut-edge forest: exactly one arrow along each
reduced path, and no arrow across components. Not an ∞-groupoid.
Endomorphisms are identities, so the homotopy type is 0-truncated. -/
instance : Groupoid CutVertex where
  Hom x y := CutArrow x y
  id x := ⟨Eq.refl (cutComponent x.idx), 0⟩
  comp f g := ⟨f.same.trans g.same, 0⟩
  id_comp _ := Subsingleton.elim _ _
  comp_id _ := Subsingleton.elim _ _
  assoc _ _ _ := Subsingleton.elim _ _
  inv f := ⟨f.same.symm, 0⟩
  inv_comp _ := Subsingleton.elim _ _
  comp_inv _ := Subsingleton.elim _ _

/-- Dimension 1, truncation level 1.
In the cut-edge groupoid, an inverse cancels on the left. Not an ∞-groupoid. -/
theorem cut_inv_cancels {x y : CutVertex} (f : x ⟶ y) :
    Groupoid.inv f ≫ f = 𝟙 y :=
  Groupoid.inv_comp f

/-- Dimension 1, truncation level 1.
An arrow exists if and only if the indices lie in one component. -/
theorem cut_arrow_nonempty_iff (i j : Fin 3) :
    Nonempty (CutArrow ⟨i⟩ ⟨j⟩) ↔ cutComponent i = cutComponent j := by
  constructor
  · rintro ⟨h, _⟩
    exact h
  · intro h
    exact ⟨⟨h, 0⟩⟩

/-- Dimension 1, truncation level 1.
An arrow exists if and only if a reduced-path label exists. -/
theorem cut_arrow_iff_label (i j : Fin 3) :
    Nonempty (CutArrow ⟨i⟩ ⟨j⟩) ↔ (labelOf i j).isSome = true := by
  rw [cut_arrow_nonempty_iff, labelOf_some_iff_component]

/-- Dimension 1, truncation level 1.
Ordered pairs that carry one cut-edge arrow. -/
def sameComponentPairs : List (Fin 3 × Fin 3) :=
  [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)]

/-- Dimension 1, truncation level 1.
Membership in `sameComponentPairs` is component equality. -/
theorem mem_sameComponentPairs (i j : Fin 3) :
    (i, j) ∈ sameComponentPairs ↔ cutComponent i = cutComponent j := by
  fin_cases i <;> fin_cases j <;> decide

/-- Dimension 1, truncation level 1.
The cut-edge fundamental groupoid has five arrows. Not an ∞-groupoid. -/
theorem cut_groupoid_morphism_count :
    sameComponentPairs.length = 5 ∧ sameComponentPairs.Nodup ∧
      (∀ i j : Fin 3,
        (i, j) ∈ sameComponentPairs ↔ Nonempty (CutArrow ⟨i⟩ ⟨j⟩)) := by
  refine ⟨rfl, ?_, ?_⟩
  · decide
  · intro i j
    rw [mem_sameComponentPairs, cut_arrow_nonempty_iff]

/-- Dimension 1, truncation level 0 as a homotopy type.
Every endomorphism of the cut-edge groupoid is the identity arrow. -/
theorem cut_endomorphism_trivial (v : CutVertex) (f : CutArrow v v) : f = ⟨rfl, 0⟩ := by
  cases f with
  | mk _ t =>
    fin_cases t
    rfl

/-- Dimension 0 report on a listed history, truncation level 0.
`PregenConstructive.recon` returns each cut-edge component label from `vertexList`.
This does not derive π₀ from the history-report criterion in general. -/
theorem recon_recovers_cut_components :
    PregenConstructive.recon cutComponent cutComponent (0 : Fin 2) [0, 1, 2] = some 0 ∧
      PregenConstructive.recon cutComponent cutComponent (1 : Fin 2) [0, 1, 2] = some 1 := by
  decide

/-- Dimension 0, truncation level 0.
The component label is fiber-constant for the report that is the label itself,
on the listed vertices. Scope is this list only. -/
theorem component_report_fiber_constant :
    PregenConstructive.FiberConstantOn ([0, 1, 2] : List (Fin 3)) cutComponent cutComponent := by
  intro _ _ _ _ hreport
  exact hreport

/-- Dimension 1, truncation level 1.
Finite presentation of one 1-type: one object and endomorphisms `ZMod 2`,
with the square of the generator equal to the identity.
Mathlib supplies the groupoid structure on `SingleObj`. Not an ∞-groupoid.
A general n-type is not presented. -/
theorem bz2_morphism_card :
    Fintype.card (Multiplicative (ZMod 2)) = 2 := by
  rw [Fintype.card_multiplicative]
  exact ZMod.card 2

/-- Dimension 1, truncation level 1.
The carrier of `SingleObj (Multiplicative (ZMod 2))` is a subsingleton.
Not an ∞-groupoid. -/
theorem bz2_object_subsingleton :
    Subsingleton (SingleObj (Multiplicative (ZMod 2))) :=
  inferInstance

/-- Dimension 1, truncation level 1.
The non-identity element of `ZMod 2` has order 2. -/
theorem bz2_generator_square :
    Multiplicative.ofAdd (1 : ZMod 2) ≠ 1 ∧
      Multiplicative.ofAdd (1 : ZMod 2) * Multiplicative.ofAdd (1 : ZMod 2) = 1 := by
  decide

/-- Dimension 1, truncation level 1.
`BZ2` has two endomorphisms and the cut-edge vertex `0` has only the identity
endomorphism, so this 1-type is not the cut-edge fundamental groupoid. -/
theorem bz2_is_not_cut_edge_groupoid :
    Fintype.card (Multiplicative (ZMod 2)) = 2 ∧
      (∀ f : CutArrow ⟨0⟩ ⟨0⟩, f = ⟨rfl, 0⟩) ∧
      Fintype.card CutVertex = 3 ∧
      sameComponentPairs.length = 5 := by
  refine ⟨bz2_morphism_card, ?_, cut_vertex_card, rfl⟩
  intro f
  exact Subsingleton.elim f ⟨rfl, 0⟩

/-- Truncation level `n`, simplex dimension at most `n`.
Mathlib's truncation functor has been applied. This predicate holds for every
simplicial set, so it does not present a general n-type. -/
def IsSSetTruncatedAt (n : ℕ) (X : SSet) : Prop :=
  ∃ Y : SSet.Truncated n, Y = (SSet.truncation n).obj X

/-- Truncation level `n`.
`IsSSetTruncatedAt` is not a presentation of a general n-type. -/
theorem sset_truncation_predicate_is_not_a_presentation (n : ℕ) (X : SSet) :
    IsSSetTruncatedAt n X :=
  ⟨(SSet.truncation n).obj X, rfl⟩

/-- Dimension 0 of the nerve, truncation level 1 of the 1-type.
Mathlib's `nerveEquiv` identifies 0-simplices of `nerve` with the objects
of `SingleObj (Multiplicative (ZMod 2))`. Not an ∞-groupoid. -/
theorem bz2_nerve_zero_simplices_equiv_objects :
    Nonempty (ComposableArrows (SingleObj (Multiplicative (ZMod 2))) 0 ≃
      SingleObj (Multiplicative (ZMod 2))) :=
  ⟨nerveEquiv⟩

/-- Dimension at most 1, truncation level 1.
The nerve of the finite 1-type satisfies the truncation predicate at level 1.
The predicate does not present a general n-type. -/
theorem bz2_nerve_satisfies_truncation_predicate :
    IsSSetTruncatedAt 1 (nerve (SingleObj (Multiplicative (ZMod 2)))) :=
  sset_truncation_predicate_is_not_a_presentation 1 _

end GenesisHottTruncation

#print axioms GenesisHottTruncation.cut_edge_symmetric
#print axioms GenesisHottTruncation.cut_edge_irreflexive
#print axioms GenesisHottTruncation.path_edge_symmetric
#print axioms GenesisHottTruncation.path_edge_irreflexive
#print axioms GenesisHottTruncation.cut_edge_endpoints_apart
#print axioms GenesisHottTruncation.walkCut_iff_component
#print axioms GenesisHottTruncation.walkCut_refl
#print axioms GenesisHottTruncation.walkCut_symm
#print axioms GenesisHottTruncation.walkCut_trans
#print axioms GenesisHottTruncation.cutEdge_implies_walk
#print axioms GenesisHottTruncation.cut_edge_pi0_card
#print axioms GenesisHottTruncation.walkPath_all
#print axioms GenesisHottTruncation.path_edge_pi0_card
#print axioms GenesisHottTruncation.exhibited_cut_does_not_determine_pi0
#print axioms GenesisHottTruncation.labelOf_src_tgt
#print axioms GenesisHottTruncation.labelOf_some_iff_component
#print axioms GenesisHottTruncation.labelOf_0_2
#print axioms GenesisHottTruncation.red_label_agrees
#print axioms GenesisHottTruncation.cut_vertex_card
#print axioms GenesisHottTruncation.cut_inv_cancels
#print axioms GenesisHottTruncation.cut_arrow_nonempty_iff
#print axioms GenesisHottTruncation.cut_arrow_iff_label
#print axioms GenesisHottTruncation.mem_sameComponentPairs
#print axioms GenesisHottTruncation.cut_groupoid_morphism_count
#print axioms GenesisHottTruncation.cut_endomorphism_trivial
#print axioms GenesisHottTruncation.recon_recovers_cut_components
#print axioms GenesisHottTruncation.component_report_fiber_constant
#print axioms GenesisHottTruncation.bz2_morphism_card
#print axioms GenesisHottTruncation.bz2_object_subsingleton
#print axioms GenesisHottTruncation.bz2_generator_square
#print axioms GenesisHottTruncation.bz2_is_not_cut_edge_groupoid
#print axioms GenesisHottTruncation.sset_truncation_predicate_is_not_a_presentation
#print axioms GenesisHottTruncation.bz2_nerve_zero_simplices_equiv_objects
#print axioms GenesisHottTruncation.bz2_nerve_satisfies_truncation_predicate
