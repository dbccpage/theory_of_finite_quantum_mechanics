import GenesisFspBridge

/-!
# Finite horns on a declared semi-simplicial extension of a cut

AuthorityEffect: None.

The carrier below is a finite semi-simplicial set of dimension at most 2.
Its edge `e01` is packaged as a `GenesisFspBridge.CarrierCut`: an irreflexive
witnessed pair. `cut_endpoints_apart` is `GenesisFspBridge.cut_endpoints_distinct`
applied to that cut (`19L57G1:lean4/Derivation/Apartness.lean` is the same
irreflexivity shape, cited, not imported).

`19L57G1:lean4/Derivation/HigherStructure.lean` records that a witnessed binary
relation is a directed graph and that nothing above dimension 1 is forced
(`boundary_not_forced`). Its `shell2` admits a 2-cell only when all three
boundary edges are already present; `shell_guard_load_bearing` refuses a 2-cell
on an incomplete boundary; `filling_not_forced` says a horn does not fill
itself. Those declarations are not recompiled here.

The third vertex, the extra edges, and the unique 2-simplex are declared data.
They are not derived from the cut. The Genesis-determination claim is
NOT PROVED. Every horn lemma is a statement about this finite object only.

Horn shape, low dimension, no degeneracies. An inner 2-horn is a pair of
1-simplices `(d₀, d₂)` with `tgt d₂ = src d₀`. An outer 2-horn of index 0 is a
pair `(d₁, d₂)` with the same source and distinct targets. An outer 2-horn of
index 2 is a pair `(d₀, d₁)` with the same target. A filler is a 2-simplex with
those faces. Face convention: on an edge, `d₀` is the target and `d₁` is the
source; on `t012`, `d₀ = e12`, `d₁ = e02`, `d₂ = e01`.

This is the dimension-2 case of a horn missing one face. Mathlib's `SSet.horn`
(`Mathlib.AlgebraicTopology.SimplicialSet.Horn`, pin `56a005855ea17e0b0958f73ec801ae140b0a1679`)
is not imported and is not re-proved.

Verdicts for this object:
* inner horn `(d₀ = e12, d₂ = e01)` is filled by `t012`;
* inner horn `(d₀ = e01, d₂ = e20)` has no filler;
* outer horn of index 0, `(d₁ = e02, d₂ = e01)`, is filled by `t012`;
* outer horn of index 0, `(d₁ = e21, d₂ = e20)`, has no filler;
* outer horn of index 2, `(d₀ = e12, d₁ = e02)`, is filled by `t012`;
* every vertex is the source of some edge and the target of some edge;
* the cited full-boundary guard `shell2` rejects the two-edge inner horn.
-/

namespace GenesisHottHorns

inductive Vtx where
  | v0
  | v1
  | v2
  deriving DecidableEq, Repr

inductive Edge where
  | e01
  | e12
  | e02
  | e20
  | e21
  deriving DecidableEq, Repr

inductive Tri where
  | t012
  deriving DecidableEq, Repr

def src : Edge → Vtx
  | .e01 => .v0
  | .e12 => .v1
  | .e02 => .v0
  | .e20 => .v2
  | .e21 => .v2

def tgt : Edge → Vtx
  | .e01 => .v1
  | .e12 => .v2
  | .e02 => .v2
  | .e20 => .v0
  | .e21 => .v1

def d0e (e : Edge) : Vtx := tgt e

def d1e (e : Edge) : Vtx := src e

def d0t : Tri → Edge
  | .t012 => .e12

def d1t : Tri → Edge
  | .t012 => .e02

def d2t : Tri → Edge
  | .t012 => .e01

/-- The cut relation exhibited by `e01`. -/
def endpointRel : Vtx → Vtx → Prop
  | .v0, .v1 => True
  | _, _ => False

theorem endpointRel_irrefl (x : Vtx) : ¬ endpointRel x x := by
  cases x <;> intro h <;> exact h

def endpointCut : GenesisFspBridge.CarrierCut Vtx where
  r := endpointRel
  irrefl := endpointRel_irrefl

theorem cut_endpoints_apart : Vtx.v0 ≠ Vtx.v1 :=
  GenesisFspBridge.cut_endpoints_distinct endpointCut trivial

theorem cut_edge_no_loop : src .e01 ≠ tgt .e01 :=
  cut_endpoints_apart

theorem third_vertex_not_in_cut (x : Vtx) :
    ¬ endpointRel x .v2 ∧ ¬ endpointRel .v2 x := by
  cases x <;> constructor <;> intro h <;> exact h

theorem no_loop (e : Edge) : src e ≠ tgt e := by
  cases e <;> intro h <;> cases h

theorem face_face_01 (σ : Tri) : d0e (d1t σ) = d0e (d0t σ) := by
  cases σ
  rfl

theorem face_face_02 (σ : Tri) : d0e (d2t σ) = d1e (d0t σ) := by
  cases σ
  rfl

theorem face_face_12 (σ : Tri) : d1e (d2t σ) = d1e (d1t σ) := by
  cases σ
  rfl

theorem triangle_uses_third_vertex : tgt (d0t .t012) = .v2 := rfl

/-- Inner 2-horn: faces `d₀` and `d₂`, matched at the middle vertex. -/
structure InnerHorn where
  d0 : Edge
  d2 : Edge
  match1 : tgt d2 = src d0

def FillsInner (h : InnerHorn) (σ : Tri) : Prop :=
  d0t σ = h.d0 ∧ d2t σ = h.d2

/-- Outer 2-horn of index 0: faces `d₁` and `d₂`, same source, distinct targets. -/
structure OuterHornK0 where
  d1 : Edge
  d2 : Edge
  match0 : src d1 = src d2
  distinct : tgt d1 ≠ tgt d2

def FillsOuterK0 (h : OuterHornK0) (σ : Tri) : Prop :=
  d1t σ = h.d1 ∧ d2t σ = h.d2

/-- Outer 2-horn of index 2: faces `d₀` and `d₁`, same target. -/
structure OuterHornK2 where
  d0 : Edge
  d1 : Edge
  match2 : tgt d0 = tgt d1

def FillsOuterK2 (h : OuterHornK2) (σ : Tri) : Prop :=
  d0t σ = h.d0 ∧ d1t σ = h.d1

def innerFilled : InnerHorn where
  d0 := .e12
  d2 := .e01
  match1 := rfl

theorem inner_horn_filled : ∃ σ : Tri, FillsInner innerFilled σ :=
  ⟨.t012, ⟨rfl, rfl⟩⟩

def innerRefused : InnerHorn where
  d0 := .e01
  d2 := .e20
  match1 := rfl

theorem inner_horn_refused : ¬ ∃ σ : Tri, FillsInner innerRefused σ := by
  intro ⟨σ, _, h2⟩
  cases σ
  cases h2

def outerFilled : OuterHornK0 where
  d1 := .e02
  d2 := .e01
  match0 := rfl
  distinct := by intro h; cases h

theorem outer_horn_k0_filled : ∃ σ : Tri, FillsOuterK0 outerFilled σ :=
  ⟨.t012, ⟨rfl, rfl⟩⟩

def outerRefused : OuterHornK0 where
  d1 := .e21
  d2 := .e20
  match0 := rfl
  distinct := by intro h; cases h

theorem outer_horn_k0_refused : ¬ ∃ σ : Tri, FillsOuterK0 outerRefused σ := by
  intro ⟨σ, h1, _⟩
  cases σ
  cases h1

def outerFilledK2 : OuterHornK2 where
  d0 := .e12
  d1 := .e02
  match2 := rfl

theorem outer_horn_k2_filled : ∃ σ : Tri, FillsOuterK2 outerFilledK2 σ :=
  ⟨.t012, ⟨rfl, rfl⟩⟩

theorem not_all_inner_2_horns_fill :
    ¬ ∀ h : InnerHorn, ∃ σ : Tri, FillsInner h σ := by
  intro h
  exact inner_horn_refused (h innerRefused)

theorem not_all_outer_k0_horns_fill :
    ¬ ∀ h : OuterHornK0, ∃ σ : Tri, FillsOuterK0 h σ := by
  intro h
  exact outer_horn_k0_refused (h outerRefused)

theorem every_source_1horn_fills (v : Vtx) : ∃ e : Edge, src e = v := by
  cases v
  · exact ⟨.e01, rfl⟩
  · exact ⟨.e12, rfl⟩
  · exact ⟨.e20, rfl⟩

theorem every_target_1horn_fills (v : Vtx) : ∃ e : Edge, tgt e = v := by
  cases v
  · exact ⟨.e20, rfl⟩
  · exact ⟨.e01, rfl⟩
  · exact ⟨.e12, rfl⟩

/-- The three boundary edges of `(v0, v1, v2)`. This is the `shell2` shape:
all three edges, not a horn. -/
def boundaryEdges (present : Edge → Bool) : Bool :=
  present .e01 && present .e12 && present .e02

/-- Admit a 2-cell only for a complete absent face. Mirrors the cited guard. -/
def admitTriGuard (present : Edge → Bool) (triPresent : Bool) : Bool :=
  boundaryEdges present && !triPresent

def innerHornPresent (e : Edge) : Bool :=
  match e with
  | .e01 | .e12 => true
  | _ => false

def fullBoundaryPresent (e : Edge) : Bool :=
  match e with
  | .e01 | .e12 | .e02 => true
  | _ => false

theorem inner_horn_not_full_boundary :
    boundaryEdges innerHornPresent = false := rfl

theorem full_boundary_present :
    boundaryEdges fullBoundaryPresent = true := rfl

theorem inner_horn_guard_refuses :
    admitTriGuard innerHornPresent false = false := rfl

theorem full_boundary_guard_allows_declaration :
    admitTriGuard fullBoundaryPresent false = true := rfl

theorem shell2_stronger_than_inner_horn :
    boundaryEdges innerHornPresent = false ∧
      boundaryEdges fullBoundaryPresent = true ∧
        admitTriGuard innerHornPresent false = false :=
  ⟨rfl, rfl, rfl⟩

def edges : List Edge := [.e01, .e12, .e02, .e20, .e21]

theorem edges_complete (e : Edge) : e ∈ edges := by
  cases e <;> decide

def innerHornList : List (Edge × Edge) :=
  edges.flatMap fun d2 =>
    edges.filterMap fun d0 =>
      if decide (tgt d2 = src d0) then some (d0, d2) else none

theorem innerHornList_length : innerHornList.length = 8 := by
  decide

def innerFilledList : List (Edge × Edge) :=
  innerHornList.filter fun p =>
    decide (d0t .t012 = p.1 ∧ d2t .t012 = p.2)

theorem innerFilledList_length : innerFilledList.length = 1 := by
  decide

def outerK0List : List (Edge × Edge) :=
  edges.flatMap fun d2 =>
    edges.filterMap fun d1 =>
      if decide (src d1 = src d2 ∧ tgt d1 ≠ tgt d2) then some (d1, d2) else none

theorem outerK0List_length : outerK0List.length = 4 := by
  decide

def outerK0FilledList : List (Edge × Edge) :=
  outerK0List.filter fun p =>
    decide (d1t .t012 = p.1 ∧ d2t .t012 = p.2)

theorem outerK0FilledList_length : outerK0FilledList.length = 1 := by
  decide

theorem unique_inner_filler (d0 d2 : Edge)
    (hf : d0t .t012 = d0 ∧ d2t .t012 = d2) :
    d0 = .e12 ∧ d2 = .e01 := by
  rcases hf with ⟨h0, h2⟩
  subst h0
  subst h2
  exact ⟨rfl, rfl⟩

end GenesisHottHorns

#print axioms GenesisHottHorns.endpointRel_irrefl
#print axioms GenesisHottHorns.cut_endpoints_apart
#print axioms GenesisHottHorns.cut_edge_no_loop
#print axioms GenesisHottHorns.third_vertex_not_in_cut
#print axioms GenesisHottHorns.no_loop
#print axioms GenesisHottHorns.face_face_01
#print axioms GenesisHottHorns.face_face_02
#print axioms GenesisHottHorns.face_face_12
#print axioms GenesisHottHorns.triangle_uses_third_vertex
#print axioms GenesisHottHorns.inner_horn_filled
#print axioms GenesisHottHorns.inner_horn_refused
#print axioms GenesisHottHorns.outer_horn_k0_filled
#print axioms GenesisHottHorns.outer_horn_k0_refused
#print axioms GenesisHottHorns.outer_horn_k2_filled
#print axioms GenesisHottHorns.not_all_inner_2_horns_fill
#print axioms GenesisHottHorns.not_all_outer_k0_horns_fill
#print axioms GenesisHottHorns.every_source_1horn_fills
#print axioms GenesisHottHorns.every_target_1horn_fills
#print axioms GenesisHottHorns.inner_horn_not_full_boundary
#print axioms GenesisHottHorns.full_boundary_present
#print axioms GenesisHottHorns.inner_horn_guard_refuses
#print axioms GenesisHottHorns.full_boundary_guard_allows_declaration
#print axioms GenesisHottHorns.shell2_stronger_than_inner_horn
#print axioms GenesisHottHorns.edges_complete
#print axioms GenesisHottHorns.innerHornList_length
#print axioms GenesisHottHorns.innerFilledList_length
#print axioms GenesisHottHorns.outerK0List_length
#print axioms GenesisHottHorns.outerK0FilledList_length
#print axioms GenesisHottHorns.unique_inner_filler
