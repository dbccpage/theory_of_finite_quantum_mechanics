import UnionComponents

/-! An added graph edge admits a chain retraction fixing every old zero-chain
if and only if its endpoints were already connected. The positive direction
constructs an integral path chain; the negative direction uses actual homology. -/
namespace PreMssn.GraphRetraction
open GraphHomology GraphExtensions Homology FreeAbelian
open Lean.Grind AddCommMonoid AddCommGroup
universe u

theorem path_chain (G : Graph.{u}) {a b : G.Vertex} (h : Connected G a b) :
    ∃ z : Free G.Edge, boundary G z = gen b - gen a := by
  induction h with
  | refl v => exact ⟨0, by rw [(boundary G).map_zero, sub_self]⟩
  | edge e => exact ⟨gen e, boundary_gen G e⟩
  | symm h ih =>
    obtain ⟨z,hz⟩ := ih
    refine ⟨-z, ?_⟩
    rw [(boundary G).map_neg, hz, neg_sub]
  | @trans a b c h₁ h₂ ih₁ ih₂ =>
    obtain ⟨z,hz⟩ := ih₁
    obtain ⟨w,hw⟩ := ih₂
    refine ⟨z+w, ?_⟩
    rw [(boundary G).map_add, hz, hw]
    simp only [sub_eq_add_neg]
    rw [add_comm (gen b + -gen a) (gen c + -gen b),
      add_assoc (gen c) (-gen b), ← add_assoc (-gen b) (gen b),
      neg_add_cancel, zero_add]

def edgeInclusion (G : Graph.{u}) : AddHom (Free G.Edge) (Free (Sum G.Edge PUnit)) :=
  FreeAbelian.map Sum.inl

theorem inclusion_boundary (G : Graph.{u}) (a b : G.Vertex) (z : Free G.Edge) :
    boundary (addEdge G a b) (edgeInclusion G z) = boundary G z := by
  apply hom_ext ((boundary (addEdge G a b)).comp (edgeInclusion G)) (boundary G) _ z
  intro e
  change boundary (addEdge G a b) (gen (.inl e)) = boundary G (gen e)
  rfl

def inclusion (G : Graph.{u}) (a b : G.Vertex) :
    Morphism (complex G) (complex (addEdge G a b)) where
  upper := edgeInclusion G
  middle := AddHom.identity _
  lower := AddHom.identity _
  boundary_commutes z := (inclusion_boundary G a b z).symm
  differential_commutes _ := rfl

def vertexHomology (G : Graph.{u}) (a : G.Vertex) : Homology (complex G) :=
  quotientProjection (boundaryCycle (complex G)) (asCycle G (gen a))

theorem vertex_homology_eq_iff (G : Graph.{u}) (a b : G.Vertex) :
    vertexHomology G a = vertexHomology G b ↔ Connected G a b := by
  constructor
  · intro h
    exact (vertex_class_eq_iff_connected G a b).mp (congrArg (toH0 G) h)
  · intro h
    exact congrArg (fromH0 G) ((vertex_class_eq_iff_connected G a b).mpr h)

theorem inclusion_vertex (G : Graph.{u}) (a b v : G.Vertex) :
    homologyMap (inclusion G a b) (vertexHomology G v) =
      vertexHomology (addEdge G a b) v := rfl

def edgeRetraction (G : Graph.{u}) (z : Free G.Edge) :
    AddHom (Free (Sum G.Edge PUnit)) (Free G.Edge) :=
  extend (fun e => match e with | .inl e => gen e | .inr _ => z)

theorem retraction_boundary (G : Graph.{u}) (a b : G.Vertex) (z : Free G.Edge)
    (hz : boundary G z = gen b-gen a) (w : Free (Sum G.Edge PUnit)) :
    boundary G (edgeRetraction G z w) = boundary (addEdge G a b) w := by
  apply hom_ext ((boundary G).comp (edgeRetraction G z)) (boundary (addEdge G a b)) _ w
  intro e
  cases e with
  | inl e =>
    change boundary G (gen e) = boundary (addEdge G a b) (gen (.inl e))
    rfl
  | inr _ => exact hz

def retraction (G : Graph.{u}) (a b : G.Vertex) (z : Free G.Edge)
    (hz : boundary G z = gen b-gen a) :
    Morphism (complex (addEdge G a b)) (complex G) where
  upper := edgeRetraction G z
  middle := AddHom.identity _
  lower := AddHom.identity _
  boundary_commutes w := (retraction_boundary G a b z hz w).symm
  differential_commutes _ := rfl

/-- This equivalence gives both a constructive repair when the endpoints were
connected and an obstruction when the edge merges two old components. -/
theorem middle_retraction_iff_connected (G : Graph.{u}) (a b : G.Vertex) :
    (∃ r : Morphism (complex (addEdge G a b)) (complex G),
      ∀ z, r.middle ((inclusion G a b).middle z) = z) ↔ Connected G a b := by
  constructor
  · rintro ⟨r, fixes⟩
    apply (vertex_homology_eq_iff G a b).mp
    apply induced_homology_injective (inclusion G a b) r fixes
    rw [inclusion_vertex, inclusion_vertex]
    exact (vertex_homology_eq_iff (addEdge G a b) a b).mpr
      (Connected.edge (G := addEdge G a b) (.inr PUnit.unit))
  · intro h
    obtain ⟨z,hz⟩ := path_chain G h
    exact ⟨retraction G a b z hz, fun _ => rfl⟩

theorem edge_retraction_fixes_old (G : Graph.{u}) (z w : Free G.Edge) :
    edgeRetraction G z (edgeInclusion G w) = w :=
  hom_ext ((edgeRetraction G z).comp (edgeInclusion G)) (AddHom.identity _)
    (fun _ => rfl) w

/-- The positive construction fixes all three old chain groups, not merely the
middle group needed for the homology obstruction. -/
theorem chain_retraction_iff_connected (G : Graph.{u}) (a b : G.Vertex) :
    (∃ r : Morphism (complex (addEdge G a b)) (complex G),
      (∀ z, r.middle ((inclusion G a b).middle z) = z) ∧
      (∀ e, r.upper ((inclusion G a b).upper e) = e) ∧
      (∀ l, r.lower ((inclusion G a b).lower l) = l)) ↔ Connected G a b := by
  constructor
  · rintro ⟨r,hm,_,_⟩
    exact (middle_retraction_iff_connected G a b).mp ⟨r,hm⟩
  · intro h
    obtain ⟨z,hz⟩ := path_chain G h
    exact ⟨retraction G a b z hz, (fun _ => rfl), edge_retraction_fixes_old G z, (fun _ => rfl)⟩

end PreMssn.GraphRetraction
