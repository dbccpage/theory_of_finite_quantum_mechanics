import GenesisComputation
import AdmissionFloor
import InertDiamond
import CellGrammar
import FiniteCochain

/-!
# Finite combinatorial shadow of Genesis admission

AuthorityEffect: None.

## What is cited

* `GenesisComputation.GenesisCopy.Regime`, `Event`, `stepE`, `replayE`,
  `emptyRegime`, `firstSeparationHistory`, `firstSeparationRegime`,
  `first_separation_replay`. The in-repo copy says it follows
  `19L57G1:lean4/Derivation/Basic.lean::Regime`, `::Event` and `::stepE`.
  Those declarations were read: a regime is a datum count, a list of
  judgment-form arities, a list of judgment instances `(form index, argument
  tuple)`, a list of ruled forms, and a list of imposed pairs. A form is not
  a simplex and an instance is not a face operator.
* `19L57G1:lean4/Derivation/Basic.lean::Regime.wf` is restated below as
  `regimeWf` because `GenesisCopy` does not contain that predicate.
* `InertDiamond.St`, `Ev`, `step`, `replay`, `init`. The three-event fragment
  stores admitted tokens and form arities. It has no instance arguments.
  `InertDiamond.inscription_does_not_determine_coproduct` is the existing
  independence result; it is not re-proved here.
* `AdmissionFloor.ExhibitedCut`.
* `OmegaCore.CellGrammar.ChainGrammar`.
* `FiniteCochain.d0`, `FiniteCochain.d1`, `FiniteCochain.d1_d0_zero`.
* `PregenConstructive.recon` and `ChainRetraction` were read and are not
  imported. The first reconstructs a listed report. The second is a chain-map
  retraction obstruction. Neither produces face maps or source and target maps.

## Imports (named, not axioms)

* Reading a length-2 argument tuple as the two faces of a 1-simplex, or as the
  source and target of a 1-globe, is not stated by the regime. `recoversEdge`
  and `recoversGlobe` are that reading, used only to show it is not unique.
* Face index `i` omits vertex `i`, the indexing of Mathlib
  `SimplexCategory.δ` (`Mathlib.AlgebraicTopology.SimplexCategory.Basic`).
  This file does not import `SSet`
  (`Mathlib.AlgebraicTopology.SimplicialSet.Basic`, the abbrev
  `SimplicialObject (Type u)`) and does not construct a presheaf, a truncation
  equivalence, or a horn filler.
* A degeneracy `s0` with both faces the identity is the degree-1 shadow of
  `SimplexCategory.σ`. Higher simplicial identities are not proved.
* The degree-2 source and target equations are the globular identities. No
  globular-set definition was found in this checkout's Lean sources to reuse.

The determination claim is not proved. The object the regime does determine
is `AdmissionTupleShadow`.
-/

namespace GenesisHottShadow

open GenesisComputation GenesisComputation.GenesisCopy

/-- The finite data of a regime, with no face or source/target choice. -/
structure AdmissionTupleShadow where
  carrierCard : Nat
  arities : List Nat
  tuples : List (Nat × List Nat)
  rules : List Nat
  reqs : List (Nat × Nat)
  deriving DecidableEq, Repr

def shadowOf (r : Regime) : AdmissionTupleShadow :=
  ⟨r.data, r.forms, r.insts, r.rules, r.reqs⟩

/-- Restatement of `19L57G1:lean4/Derivation/Basic.lean::Regime.wf`. -/
def regimeWf (r : Regime) : Prop :=
  (∀ p ∈ r.insts,
      p.1 < r.forms.length ∧ p.2.length = r.forms.getD p.1 0 ∧ ∀ a ∈ p.2, a < r.data) ∧
    (∀ f ∈ r.rules, f < r.forms.length) ∧
    (∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data) ∧
    (∀ a ∈ r.forms, 1 ≤ a)

theorem supply_preserves_shadow (r : Regime) (token : Nat) :
    (stepE r (.supply token)).map shadowOf = some (shadowOf r) := by
  rfl

theorem replay_cons_supply (es : List Event) (r : Regime) (t : Nat) :
    replayE (Event.supply t :: es) r = replayE es r := by
  simp [replayE, stepE]

theorem shadow_eq_iff (r r' : Regime) : shadowOf r = shadowOf r' ↔ r = r' := by
  constructor
  · intro h
    have h1 := congrArg AdmissionTupleShadow.carrierCard h
    have h2 := congrArg AdmissionTupleShadow.arities h
    have h3 := congrArg AdmissionTupleShadow.tuples h
    have h4 := congrArg AdmissionTupleShadow.rules h
    have h5 := congrArg AdmissionTupleShadow.reqs h
    cases r
    cases r'
    simp [shadowOf] at h1 h2 h3 h4 h5
    simp [h1, h2, h3, h4, h5]
  · intro h
    subst h
    rfl

theorem supply_history_stays_empty :
    replayE [Event.supply 0, Event.supply 1] emptyRegime = some emptyRegime := by
  decide

theorem first_separation_shadow :
    shadowOf firstSeparationRegime = ⟨2, [1], [(0, [0])], [], [(0, 1)]⟩ := rfl

theorem first_separation_shadow_of_replay :
    (replayE firstSeparationHistory emptyRegime).map shadowOf =
      some (shadowOf firstSeparationRegime) := by
  rw [first_separation_replay]
  rfl

theorem first_separation_tuples_are_unary :
    ∀ p ∈ (shadowOf firstSeparationRegime).tuples, p.2.length = 1 := by
  intro p hp
  simp [shadowOf, firstSeparationRegime] at hp
  subst hp
  rfl

theorem first_separation_no_binary_tuple :
    ∀ p ∈ (shadowOf firstSeparationRegime).tuples, p.2.length ≠ 2 := by
  intro p hp
  have hlen := first_separation_tuples_are_unary p hp
  omega

def edgeHistory : List Event :=
  [.admitDatum, .admitDatum, .admitForm 2, .admitInst 0 [0, 1]]

def edgeRegime : Regime := ⟨2, [2], [(0, [0, 1])], [], []⟩

def reverseEdgeHistory : List Event :=
  [.admitDatum, .admitDatum, .admitForm 2, .admitInst 0 [1, 0]]

def reverseEdgeRegime : Regime := ⟨2, [2], [(0, [1, 0])], [], []⟩

theorem edge_replay : replayE edgeHistory emptyRegime = some edgeRegime := by
  decide

theorem reverse_edge_replay :
    replayE reverseEdgeHistory emptyRegime = some reverseEdgeRegime := by
  decide

theorem edge_shadow :
    shadowOf edgeRegime = ⟨2, [2], [(0, [0, 1])], [], []⟩ := rfl

theorem reverse_shadow :
    shadowOf reverseEdgeRegime = ⟨2, [2], [(0, [1, 0])], [], []⟩ := rfl

theorem edge_and_reverse_differ :
    (shadowOf edgeRegime).carrierCard = (shadowOf reverseEdgeRegime).carrierCard ∧
      (shadowOf edgeRegime).arities = (shadowOf reverseEdgeRegime).arities ∧
      (shadowOf edgeRegime).tuples ≠ (shadowOf reverseEdgeRegime).tuples := by
  refine ⟨rfl, rfl, ?_⟩
  decide

theorem empty_wf : regimeWf emptyRegime := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> intro x hx <;> cases hx

theorem edge_wf : regimeWf edgeRegime := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro p hp
    simp [edgeRegime] at hp
    subst hp
    decide
  · intro f hf
    simp [edgeRegime] at hf
  · intro q hq
    simp [edgeRegime] at hq
  · intro a ha
    simp [edgeRegime] at ha
    subst ha
    decide

theorem reverse_edge_wf : regimeWf reverseEdgeRegime := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro p hp
    simp [reverseEdgeRegime] at hp
    subst hp
    decide
  · intro f hf
    simp [reverseEdgeRegime] at hf
  · intro q hq
    simp [reverseEdgeRegime] at hq
  · intro a ha
    simp [reverseEdgeRegime] at ha
    subst ha
    decide

theorem first_separation_wf : regimeWf firstSeparationRegime := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro p hp
    simp [firstSeparationRegime] at hp
    subst hp
    decide
  · intro f hf
    simp [firstSeparationRegime] at hf
  · intro q hq
    simp [firstSeparationRegime] at hq
    subst hq
    decide
  · intro a ha
    simp [firstSeparationRegime] at ha
    subst ha
    decide

theorem fragment_replay :
    InertDiamond.replay
        [InertDiamond.Ev.admit (0 : Fin 2), .admit 1, .form 2]
        (InertDiamond.init : InertDiamond.St (Fin 2)) =
      some ⟨[0, 1], [2]⟩ := by
  decide

theorem fragment_does_not_store_argument_order :
    (shadowOf edgeRegime).arities = [2] ∧
      (shadowOf reverseEdgeRegime).arities = [2] ∧
      (shadowOf edgeRegime).tuples ≠ (shadowOf reverseEdgeRegime).tuples ∧
      InertDiamond.replay
          [InertDiamond.Ev.admit (0 : Fin 2), .admit 1, .form 2]
          (InertDiamond.init : InertDiamond.St (Fin 2)) =
        some ⟨[0, 1], [2]⟩ := by
  refine ⟨rfl, rfl, ?_, fragment_replay⟩
  decide

/-! ## Degree at most 1 -/

/-- Two face maps on finite sets of 0-simplices and 1-simplices.
No identity is required in this degree. -/
structure FinSemiSimplicial1 where
  n0 : Nat
  n1 : Nat
  face : Fin 2 → Fin n1 → Fin n0

/-- Source and target on finite sets of 0-cells and 1-cells. -/
structure FinGlobular1 where
  n0 : Nat
  n1 : Nat
  src : Fin n1 → Fin n0
  tgt : Fin n1 → Fin n0

/-- Faces plus one degeneracy section. Not a horn-filling statement. -/
structure FinSimplicial1 where
  n0 : Nat
  n1 : Nat
  face : Fin 2 → Fin n1 → Fin n0
  s0 : Fin n0 → Fin n1
  face_s0 : ∀ v i, face i (s0 v) = v

def forwardReading : FinSemiSimplicial1 where
  n0 := 2
  n1 := 1
  face := fun i _ => if i = 0 then 1 else 0

def backwardReading : FinSemiSimplicial1 where
  n0 := 2
  n1 := 1
  face := fun i _ => if i = 0 then 0 else 1

/-- Either assignment of the ordered pair `(0, 1)` to the two face indices. -/
def recoversEdge (X : FinSemiSimplicial1) : Prop :=
  X.n0 = 2 ∧ X.n1 = 1 ∧
    ∃ e : Fin X.n1, e.val = 0 ∧
      (((X.face 0 e).val = 1 ∧ (X.face 1 e).val = 0) ∨
        ((X.face 0 e).val = 0 ∧ (X.face 1 e).val = 1))

def edgeIndex (X : FinSemiSimplicial1) (h : X.n1 = 1) : Fin X.n1 :=
  ⟨0, h.symm ▸ Nat.zero_lt_one⟩

theorem forward_recovers : recoversEdge forwardReading := by
  refine ⟨rfl, rfl, edgeIndex forwardReading rfl, rfl, Or.inl ?_⟩
  decide

theorem backward_recovers : recoversEdge backwardReading := by
  refine ⟨rfl, rfl, edgeIndex backwardReading rfl, rfl, Or.inr ?_⟩
  decide

/-- First face of the unique 1-simplex, or `99` when that simplex is absent. -/
def edgeFace0 (X : FinSemiSimplicial1) : Nat :=
  if h : X.n1 = 1 then (X.face (0 : Fin 2) (edgeIndex X h)).val else 99

theorem edgeFace0_forward : edgeFace0 forwardReading = 1 := by
  decide

theorem edgeFace0_backward : edgeFace0 backwardReading = 0 := by
  decide

theorem forward_ne_backward : forwardReading ≠ backwardReading := by
  intro h
  have := congrArg edgeFace0 h
  rw [edgeFace0_forward, edgeFace0_backward] at this
  exact absurd this (by decide)

theorem edge_regime_does_not_determine_semisimplicial1 :
    shadowOf edgeRegime = ⟨2, [2], [(0, [0, 1])], [], []⟩ ∧
      recoversEdge forwardReading ∧ recoversEdge backwardReading ∧
      forwardReading ≠ backwardReading :=
  ⟨edge_shadow, forward_recovers, backward_recovers, forward_ne_backward⟩

def recoversFun (f : Fin 2 → Fin 1 → Fin 2) : Prop :=
  (f 0 0 = 1 ∧ f 1 0 = 0) ∨ (f 0 0 = 0 ∧ f 1 0 = 1)

def recoversFunB (f : Fin 2 → Fin 1 → Fin 2) : Bool :=
  ((f 0 0 == 1) && (f 1 0 == 0)) || ((f 0 0 == 0) && (f 1 0 == 1))

theorem face_map_card : Fintype.card (Fin 2 → Fin 1 → Fin 2) = 4 := by
  decide

theorem recovers_fun_card :
    Fintype.card {f : Fin 2 → Fin 1 → Fin 2 // recoversFunB f = true} = 2 := by
  decide

theorem forward_fun_recovers : recoversFun forwardReading.face :=
  Or.inl ⟨rfl, rfl⟩

theorem backward_fun_recovers : recoversFun backwardReading.face :=
  Or.inr ⟨rfl, rfl⟩

def globeForward : FinGlobular1 where
  n0 := 2
  n1 := 1
  src := fun _ => 0
  tgt := fun _ => 1

def globeBackward : FinGlobular1 where
  n0 := 2
  n1 := 1
  src := fun _ => 1
  tgt := fun _ => 0

def recoversGlobe (G : FinGlobular1) : Prop :=
  G.n0 = 2 ∧ G.n1 = 1 ∧
    ∃ e : Fin G.n1, e.val = 0 ∧
      (((G.src e).val = 0 ∧ (G.tgt e).val = 1) ∨
        ((G.src e).val = 1 ∧ (G.tgt e).val = 0))

def globeIndex (G : FinGlobular1) (h : G.n1 = 1) : Fin G.n1 :=
  ⟨0, h.symm ▸ Nat.zero_lt_one⟩

theorem globe_forward_recovers : recoversGlobe globeForward := by
  refine ⟨rfl, rfl, globeIndex globeForward rfl, rfl, Or.inl ?_⟩
  decide

theorem globe_backward_recovers : recoversGlobe globeBackward := by
  refine ⟨rfl, rfl, globeIndex globeBackward rfl, rfl, Or.inr ?_⟩
  decide

def globeSrc0 (G : FinGlobular1) : Nat :=
  if h : G.n1 = 1 then (G.src (globeIndex G h)).val else 99

theorem globeSrc0_forward : globeSrc0 globeForward = 0 := by
  decide

theorem globeSrc0_backward : globeSrc0 globeBackward = 1 := by
  decide

theorem globe_forward_ne_backward : globeForward ≠ globeBackward := by
  intro h
  have := congrArg globeSrc0 h
  rw [globeSrc0_forward, globeSrc0_backward] at this
  exact absurd this (by decide)

theorem edge_regime_does_not_determine_globular1 :
    shadowOf edgeRegime = ⟨2, [2], [(0, [0, 1])], [], []⟩ ∧
      recoversGlobe globeForward ∧ recoversGlobe globeBackward ∧
      globeForward ≠ globeBackward :=
  ⟨edge_shadow, globe_forward_recovers, globe_backward_recovers, globe_forward_ne_backward⟩

def recoversGlobeFun (s t : Fin 1 → Fin 2) : Prop :=
  (s 0 = 0 ∧ t 0 = 1) ∨ (s 0 = 1 ∧ t 0 = 0)

def recoversGlobeB (s t : Fin 1 → Fin 2) : Bool :=
  ((s 0 == 0) && (t 0 == 1)) || ((s 0 == 1) && (t 0 == 0))

theorem globular_pair_card :
    Fintype.card ((Fin 1 → Fin 2) × (Fin 1 → Fin 2)) = 4 := by
  decide

theorem globular_orientation_count :
    Fintype.card {p : (Fin 1 → Fin 2) × (Fin 1 → Fin 2) // recoversGlobeB p.1 p.2 = true} = 2 := by
  decide

def faceA (i : Fin 2) (e : Fin 3) : Fin 2 :=
  if e = 0 then
    if i = 0 then 1 else 0
  else if e = 1 then
    0
  else
    1

def s0A (v : Fin 2) : Fin 3 :=
  if v = 0 then 1 else 2

theorem faceA_s0 : ∀ v i : Fin 2, faceA i (s0A v) = v := by
  decide

def simpA : FinSimplicial1 where
  n0 := 2
  n1 := 3
  face := faceA
  s0 := s0A
  face_s0 := faceA_s0

def faceB (i : Fin 2) (e : Fin 4) : Fin 2 :=
  if e = 0 then
    if i = 0 then 1 else 0
  else if e = 3 then
    1
  else
    0

def s0B (v : Fin 2) : Fin 4 :=
  if v = 0 then 1 else 3

theorem faceB_s0 : ∀ v i : Fin 2, faceB i (s0B v) = v := by
  decide

def simpB : FinSimplicial1 where
  n0 := 2
  n1 := 4
  face := faceB
  s0 := s0B
  face_s0 := faceB_s0

theorem simpA_contains_forward_edge :
    simpA.n0 = 2 ∧ faceA 0 0 = 1 ∧ faceA 1 0 = 0 ∧ simpA.face = faceA := by
  refine ⟨rfl, ?_, ?_, rfl⟩ <;> decide

theorem simpB_contains_forward_edge :
    simpB.n0 = 2 ∧ faceB 0 0 = 1 ∧ faceB 1 0 = 0 ∧ simpB.face = faceB := by
  refine ⟨rfl, ?_, ?_, rfl⟩ <;> decide

theorem simplicial_extensions_not_unique :
    simpA.n1 = 3 ∧ simpB.n1 = 4 ∧ simpA.face_s0 = simpA.face_s0 ∧ simpA ≠ simpB := by
  refine ⟨rfl, rfl, rfl, ?_⟩
  intro h
  have := congrArg FinSimplicial1.n1 h
  simp [simpA, simpB] at this

/-! ## One extra dimension, after a reading has been chosen -/

structure FinGlobular2 where
  base : FinGlobular1
  n2 : Nat
  src2 : Fin n2 → Fin base.n1
  tgt2 : Fin n2 → Fin base.n1
  globular_src : ∀ σ, base.src (src2 σ) = base.src (tgt2 σ)
  globular_tgt : ∀ σ, base.tgt (src2 σ) = base.tgt (tgt2 σ)

def globe2empty : FinGlobular2 where
  base := globeForward
  n2 := 0
  src2 := fun σ => σ.elim0
  tgt2 := fun σ => σ.elim0
  globular_src := by intro σ; exact σ.elim0
  globular_tgt := by intro σ; exact σ.elim0

def globe2loop : FinGlobular2 where
  base := globeForward
  n2 := 1
  src2 := fun _ => ⟨0, by decide⟩
  tgt2 := fun _ => ⟨0, by decide⟩
  globular_src := fun _ => rfl
  globular_tgt := fun _ => rfl

theorem globe2_not_unique :
    globe2empty.n2 = 0 ∧ globe2loop.n2 = 1 ∧
      globe2empty.base = globeForward ∧ globe2loop.base = globeForward ∧
      globe2empty ≠ globe2loop := by
  refine ⟨rfl, rfl, rfl, rfl, ?_⟩
  intro h
  have := congrArg FinGlobular2.n2 h
  simp [globe2empty, globe2loop] at this

/-- The three degree-2 semi-simplicial identities on a single 2-simplex,
with face index `i` omitting vertex `i`. -/
def simplex2Identities (face1 : Fin 2 → Fin 1 → Fin 2) (face2 : Fin 3 → Fin 1) : Prop :=
  face1 0 (face2 1) = face1 0 (face2 0) ∧
    face1 0 (face2 2) = face1 1 (face2 0) ∧
    face1 1 (face2 2) = face1 1 (face2 1)

theorem no_simplex2_on_forward_edge :
    ¬ ∃ face2 : Fin 3 → Fin 1, simplex2Identities forwardReading.face face2 := by
  intro ⟨face2, _h01, h02, _h12⟩
  simp [forwardReading] at h02

theorem forward_face_values :
    (forwardReading.face (0 : Fin 2) (edgeIndex forwardReading rfl)).val = 1 ∧
      (forwardReading.face (1 : Fin 2) (edgeIndex forwardReading rfl)).val = 0 := by
  constructor <;> decide

/-! ## Cuts and the existing chain and cochain data -/

def cutOneWay : AdmissionFloor.ExhibitedCut (Fin 2) where
  relation := fun x y => x = 0 ∧ y = 1
  first := 0
  second := 1
  exhibited := ⟨rfl, rfl⟩
  protectedLaw := by
    intro x hx
    rcases hx with ⟨hx0, hx1⟩
    exact absurd (hx0.symm.trans hx1) (by decide : (0 : Fin 2) ≠ 1)

def cutSymmetric : AdmissionFloor.ExhibitedCut (Fin 2) where
  relation := fun x y => (x = 0 ∧ y = 1) ∨ (x = 1 ∧ y = 0)
  first := 0
  second := 1
  exhibited := Or.inl ⟨rfl, rfl⟩
  protectedLaw := by
    intro x hx
    rcases hx with ⟨hx0, hx1⟩ | ⟨hx0, hx1⟩
    · exact absurd (hx0.symm.trans hx1) (by decide : (0 : Fin 2) ≠ 1)
    · exact absurd (hx1.symm.trans hx0) (by decide : (0 : Fin 2) ≠ 1)

theorem cuts_exhibit_requirement :
    cutOneWay.relation 0 1 ∧ cutSymmetric.relation 0 1 ∧
      (shadowOf firstSeparationRegime).reqs = [(0, 1)] := by
  refine ⟨⟨rfl, rfl⟩, Or.inl ⟨rfl, rfl⟩, rfl⟩

theorem cuts_differ : cutOneWay.relation ≠ cutSymmetric.relation := by
  intro h
  have := congrFun (congrFun h (1 : Fin 2)) (0 : Fin 2)
  simp [cutOneWay, cutSymmetric] at this

theorem requirement_does_not_determine_cut :
    (shadowOf firstSeparationRegime).reqs = [(0, 1)] ∧
      cutOneWay.relation ≠ cutSymmetric.relation :=
  ⟨rfl, cuts_differ⟩

def chainToZero : OmegaCore.CellGrammar.ChainGrammar (Fin 2) (Fin 1) Empty where
  zero0 := 0
  boundary1 := fun _ => 0
  boundary2 := Empty.elim
  boundarySquare := fun face => nomatch face

def chainToOne : OmegaCore.CellGrammar.ChainGrammar (Fin 2) (Fin 1) Empty where
  zero0 := 0
  boundary1 := fun _ => 1
  boundary2 := Empty.elim
  boundarySquare := fun face => nomatch face

theorem chain_boundaries_differ : chainToZero.boundary1 ≠ chainToOne.boundary1 := by
  intro h
  have := congrFun h (0 : Fin 1)
  simp [chainToZero, chainToOne] at this

theorem triangle_nilpotence_not_edge_tuple :
    FiniteCochain.d1 (FiniteCochain.d0 ⟨0, 1, 2⟩) = ⟨0⟩ ∧
      (shadowOf edgeRegime).tuples.length = 1 ∧
      (shadowOf edgeRegime).tuples.length ≠ 3 := by
  refine ⟨FiniteCochain.d1_d0_zero _, rfl, ?_⟩
  decide

#print axioms supply_preserves_shadow
#print axioms replay_cons_supply
#print axioms shadow_eq_iff
#print axioms supply_history_stays_empty
#print axioms first_separation_shadow
#print axioms first_separation_shadow_of_replay
#print axioms first_separation_tuples_are_unary
#print axioms first_separation_no_binary_tuple
#print axioms edge_replay
#print axioms reverse_edge_replay
#print axioms edge_shadow
#print axioms reverse_shadow
#print axioms edge_and_reverse_differ
#print axioms empty_wf
#print axioms edge_wf
#print axioms reverse_edge_wf
#print axioms first_separation_wf
#print axioms fragment_replay
#print axioms fragment_does_not_store_argument_order
#print axioms forward_recovers
#print axioms backward_recovers
#print axioms edgeFace0_forward
#print axioms edgeFace0_backward
#print axioms forward_ne_backward
#print axioms edge_regime_does_not_determine_semisimplicial1
#print axioms face_map_card
#print axioms recovers_fun_card
#print axioms forward_fun_recovers
#print axioms backward_fun_recovers
#print axioms globe_forward_recovers
#print axioms globe_backward_recovers
#print axioms globeSrc0_forward
#print axioms globeSrc0_backward
#print axioms globe_forward_ne_backward
#print axioms edge_regime_does_not_determine_globular1
#print axioms globular_pair_card
#print axioms globular_orientation_count
#print axioms faceA_s0
#print axioms faceB_s0
#print axioms simpA_contains_forward_edge
#print axioms simpB_contains_forward_edge
#print axioms simplicial_extensions_not_unique
#print axioms globe2_not_unique
#print axioms no_simplex2_on_forward_edge
#print axioms forward_face_values
#print axioms cuts_exhibit_requirement
#print axioms cuts_differ
#print axioms requirement_does_not_determine_cut
#print axioms chain_boundaries_differ
#print axioms triangle_nilpotence_not_edge_tuple

end GenesisHottShadow

private def l5aProvenance : String :=
  "Origin: lean4/GenesisHottShadow.lean Claim: edge_regime_does_not_determine_semisimplicial1 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
