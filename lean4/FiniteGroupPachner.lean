import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Finset.Card
import Mathlib.Data.Rat.Defs
import Mathlib.Algebra.Field.Rat
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic.FieldSimp

/-! Untwisted finite-group gauge counting for the three 4-dimensional Pachner moves.
The local complexes are complementary collections of facets of a 5-simplex.
No Regge action, twisted amplitude, quantum group or fermion model is asserted.
AuthorityEffect: None.
-/
namespace FiniteGroupPachner

abbrev Vertex := Fin 6

def edgeOne (i j : Vertex) : Prop := i ≠ 0 ∧ j ≠ 0
def triangleOne (i j k : Vertex) : Prop := i ≠ 0 ∧ j ≠ 0 ∧ k ≠ 0
def edgeTwo (i j : Vertex) : Prop := ¬ ((i = 0 ∧ j = 1) ∨ (i = 1 ∧ j = 0))
def triangleTwo (i j k : Vertex) : Prop := edgeTwo i j ∧ edgeTwo j k ∧ edgeTwo i k

def triangleLeft (i j k : Vertex) : Prop := ({i,j,k} : Finset Vertex) ≠ {0,1,2}
def triangleRight (i j k : Vertex) : Prop := ({i,j,k} : Finset Vertex) ≠ {3,4,5}
def triangleBoundary (i j k : Vertex) : Prop := triangleLeft i j k ∧ triangleRight i j k

def facetFace (p : Nat) (left : Bool) (s : Finset Vertex) : Prop :=
  ∃ v : Vertex, (if left then v.val < p else p ≤ v.val) ∧ v ∉ s

instance facetFaceDecidable (p : Nat) (left : Bool) (s : Finset Vertex) :
    Decidable (facetFace p left s) := by unfold facetFace; infer_instance

macro "geometry" : tactic => `(tactic|
  (simp only [facetFace, edgeOne, triangleOne, edgeTwo, triangleTwo,
    triangleLeft, triangleRight, triangleBoundary]; decide))

theorem one_facet_edges : ∀ i j : Vertex,
    facetFace 1 true {i,j} ↔ edgeOne i j := by geometry
theorem one_facet_triangles : ∀ i j k : Vertex,
    facetFace 1 true {i,j,k} ↔ triangleOne i j k := by geometry
theorem five_facet_edges : ∀ i j : Vertex,
    facetFace 1 false {i,j} := by geometry
theorem five_facet_triangles : ∀ i j k : Vertex,
    facetFace 1 false {i,j,k} := by geometry
theorem two_facet_edges : ∀ i j : Vertex,
    facetFace 2 true {i,j} ↔ edgeTwo i j := by geometry
theorem two_facet_triangles : ∀ i j k : Vertex,
    facetFace 2 true {i,j,k} ↔ triangleTwo i j k := by geometry
theorem four_facet_edges : ∀ i j : Vertex,
    facetFace 2 false {i,j} := by geometry
theorem four_facet_triangles : ∀ i j k : Vertex,
    facetFace 2 false {i,j,k} := by geometry
theorem three_facet_edges : ∀ i j : Vertex,
    facetFace 3 true {i,j} ∧ facetFace 3 false {i,j} := by geometry
theorem three_facet_triangles : ∀ i j k : Vertex,
    (facetFace 3 true {i,j,k} ↔ triangleLeft i j k) ∧
    (facetFace 3 false {i,j,k} ↔ triangleRight i j k) := by geometry

/-- The common subcomplex has exactly the boundary skeleton used below. -/
theorem one_boundary_skeleton :
    (∀ i j : Vertex, (facetFace 1 true {i,j} ∧ facetFace 1 false {i,j}) ↔ edgeOne i j) ∧
    (∀ i j k : Vertex, (facetFace 1 true {i,j,k} ∧ facetFace 1 false {i,j,k}) ↔
      triangleOne i j k) := by geometry

theorem two_boundary_skeleton :
    (∀ i j : Vertex, (facetFace 2 true {i,j} ∧ facetFace 2 false {i,j}) ↔ edgeTwo i j) ∧
    (∀ i j k : Vertex, (facetFace 2 true {i,j,k} ∧ facetFace 2 false {i,j,k}) ↔
      triangleTwo i j k) := by geometry

theorem three_boundary_skeleton :
    (∀ i j : Vertex, facetFace 3 true {i,j} ∧ facetFace 3 false {i,j}) ∧
    (∀ i j k : Vertex, (facetFace 3 true {i,j,k} ∧ facetFace 3 false {i,j,k}) ↔
      triangleBoundary i j k) := by geometry

theorem one_root_triangle : ∀ i j : Vertex,
    edgeOne i j → triangleOne 1 i j := by geometry
theorem two_root_edges : ∀ i : Vertex, edgeTwo 2 i := by geometry
theorem two_root_triangle : ∀ i j : Vertex,
    edgeTwo i j → triangleTwo 2 i j := by geometry
theorem boundary_has_triangle_cone : ∀ i j k : Vertex,
    ∃ r : Vertex, triangleBoundary r i j ∧ triangleBoundary r j k ∧
      triangleBoundary r i k := by geometry

variable (G : Type*) [Group G]

@[ext] structure Connection where
  edge : Vertex → Vertex → G
  diagonal : ∀ i, edge i i = 1
  reverse : ∀ i j, edge j i = (edge i j)⁻¹

variable {G}

def FlatOn (T : Vertex → Vertex → Vertex → Prop) (c : Connection G) : Prop :=
  ∀ i j k, T i j k → c.edge i j * c.edge j k = c.edge i k

def Coloring (E : Vertex → Vertex → Prop) (T : Vertex → Vertex → Vertex → Prop) :=
  {c : Connection G // (∀ i j, ¬ E i j → c.edge i j = 1) ∧ FlatOn T c}

abbrev Complete := @Coloring G _ (fun _ _ => True) (fun _ _ _ => True)
abbrev BoundaryOne := @Coloring G _ edgeOne triangleOne
abbrev BoundaryTwo := @Coloring G _ edgeTwo triangleTwo
abbrev BoundaryThree := @Coloring G _ (fun _ _ => True) triangleBoundary
abbrev ThreeLeft := @Coloring G _ (fun _ _ => True) triangleLeft
abbrev ThreeRight := @Coloring G _ (fun _ _ => True) triangleRight

def pureConnection (p : Vertex → G) : Connection G where
  edge i j := (p i)⁻¹ * p j
  diagonal i := by simp
  reverse i j := by simp

def pureColoring (p : Vertex → G) : Complete (G := G) :=
  ⟨pureConnection p, (by simp), by intro i j k _; simp [pureConnection, mul_assoc]⟩

theorem edge_from_root (c : Connection G) (r i j : Vertex)
    (h : c.edge r i * c.edge i j = c.edge r j) :
    c.edge i j = (c.edge r i)⁻¹ * c.edge r j := by
  rw [← h]; simp

theorem complete_from_row (c : Complete (G := G)) (r : Vertex) :
    c = pureColoring (c.val.edge r) := by
  apply Subtype.ext
  apply Connection.ext
  funext i j
  exact edge_from_root c.val r i j (c.property.2 r i j trivial)

theorem triangle_from_cone (c : Connection G) (r i j k : Vertex)
    (hij : c.edge r i * c.edge i j = c.edge r j)
    (hjk : c.edge r j * c.edge j k = c.edge r k)
    (hik : c.edge r i * c.edge i k = c.edge r k) :
    c.edge i j * c.edge j k = c.edge i k := by
  apply mul_left_cancel (a := c.edge r i)
  rw [← mul_assoc, hij, hjk, hik]

theorem boundary_three_flat (b : BoundaryThree (G := G)) :
    FlatOn (fun _ _ _ => True) b.val := by
  intro i j k _
  obtain ⟨r, hij, hjk, hik⟩ := boundary_has_triangle_cone i j k
  exact triangle_from_cone b.val r i j k (b.property.2 r i j hij)
    (b.property.2 r j k hjk) (b.property.2 r i k hik)


/-- A boundary violation cannot be hidden by extending the field in the bulk. -/
theorem flat_boundary_of_matching
    (E : Vertex → Vertex → Prop) (T S : Vertex → Vertex → Vertex → Prop)
    (b c : Connection G)
    (hmatch : ∀ i j, E i j → c.edge i j = b.edge i j)
    (hflat : FlatOn S c)
    (hfaces : ∀ i j k, T i j k → S i j k ∧ E i j ∧ E j k ∧ E i k) :
    FlatOn T b := by
  intro i j k h
  obtain ⟨hs, hij, hjk, hik⟩ := hfaces i j k h
  have result := hflat i j k hs
  rw [hmatch i j hij, hmatch j k hjk, hmatch i k hik] at result
  exact result

theorem nonflat_boundary_has_no_extension
    (E : Vertex → Vertex → Prop) (T S : Vertex → Vertex → Vertex → Prop)
    (b : Connection G) (hbad : ¬ FlatOn T b)
    (hfaces : ∀ i j k, T i j k → S i j k ∧ E i j ∧ E j k ∧ E i k) :
    ¬ ∃ c : Connection G, FlatOn S c ∧
      (∀ i j, E i j → c.edge i j = b.edge i j) := by
  rintro ⟨c, hc, hm⟩
  exact hbad (flat_boundary_of_matching E T S b c hm hc hfaces)

noncomputable instance connectionFintype [Fintype G] : Fintype (Connection G) :=
  Fintype.ofInjective Connection.edge (by intro a b h; exact Connection.ext h)

noncomputable instance coloringFintype [Fintype G]
    (E : Vertex → Vertex → Prop) (T : Vertex → Vertex → Vertex → Prop) :
    Fintype (@Coloring G _ E T) := by
  classical
  unfold Coloring
  infer_instance

def Matches (E : Vertex → Vertex → Prop) (c b : Connection G) : Prop :=
  ∀ i j, E i j → c.edge i j = b.edge i j

def SelfFillings {E : Vertex → Vertex → Prop} {T : Vertex → Vertex → Vertex → Prop}
    (b : @Coloring G _ E T) := {c : @Coloring G _ E T // Matches E c.val b.val}

abbrev OneNew (b : BoundaryOne (G := G)) :=
  {c : Complete (G := G) // Matches edgeOne c.val b.val}
abbrev TwoNew (b : BoundaryTwo (G := G)) :=
  {c : Complete (G := G) // Matches edgeTwo c.val b.val}
abbrev ThreeOld (b : BoundaryThree (G := G)) :=
  {c : ThreeLeft (G := G) // Matches (fun _ _ => True) c.val b.val}
abbrev ThreeNew (b : BoundaryThree (G := G)) :=
  {c : ThreeRight (G := G) // Matches (fun _ _ => True) c.val b.val}

noncomputable instance selfFillingsFintype [Fintype G]
    {E : Vertex → Vertex → Prop} {T : Vertex → Vertex → Vertex → Prop}
    (b : @Coloring G _ E T) : Fintype (SelfFillings b) := by
  classical
  unfold SelfFillings
  infer_instance
noncomputable instance oneNewFintype [Fintype G] (b : BoundaryOne (G := G)) :
    Fintype (OneNew b) := Fintype.ofFinite _
noncomputable instance twoNewFintype [Fintype G] (b : BoundaryTwo (G := G)) :
    Fintype (TwoNew b) := Fintype.ofFinite _
noncomputable instance threeOldFintype [Fintype G] (b : BoundaryThree (G := G)) :
    Fintype (ThreeOld b) := Fintype.ofFinite _
noncomputable instance threeNewFintype [Fintype G] (b : BoundaryThree (G := G)) :
    Fintype (ThreeNew b) := Fintype.ofFinite _

def selfFilling {E : Vertex → Vertex → Prop} {T : Vertex → Vertex → Vertex → Prop}
    (b : @Coloring G _ E T) : SelfFillings b := ⟨b, by intro i j _; rfl⟩

theorem self_filling_unique {E : Vertex → Vertex → Prop}
    {T : Vertex → Vertex → Vertex → Prop} (b : @Coloring G _ E T)
    (c : SelfFillings b) : c = selfFilling b := by
  apply Subtype.ext
  apply Subtype.ext
  apply Connection.ext
  funext i j
  change c.val.val.edge i j = b.val.edge i j
  by_cases h : E i j
  · exact c.property i j h
  · rw [c.val.property.1 i j h, b.property.1 i j h]

theorem complete_eq_of_row (c d : Complete (G := G)) (r : Vertex)
    (h : ∀ i, c.val.edge r i = d.val.edge r i) : c = d := by
  calc c = pureColoring (c.val.edge r) := complete_from_row c r
       _ = pureColoring (d.val.edge r) := congrArg pureColoring (funext h)
       _ = d := (complete_from_row d r).symm

def onePotential (b : BoundaryOne (G := G)) (t : G) (i : Vertex) : G :=
  if i = 0 then t else b.val.edge 1 i

def fillOne (b : BoundaryOne (G := G)) (t : G) : OneNew b :=
  ⟨pureColoring (onePotential b t), by
    intro i j h
    simpa [pureColoring, pureConnection, onePotential, h.1, h.2] using
      (edge_from_root b.val 1 i j (b.property.2 1 i j (one_root_triangle i j h))).symm⟩

def oneParameter {b : BoundaryOne (G := G)} (c : OneNew b) : G := c.val.val.edge 1 0

theorem one_parameter_fill (b : BoundaryOne (G := G)) (t : G) :
    oneParameter (fillOne b t) = t := by
  simp [oneParameter, fillOne, pureColoring, pureConnection, onePotential, b.val.diagonal]

theorem fill_one_parameter (b : BoundaryOne (G := G)) (c : OneNew b) :
    fillOne b (oneParameter c) = c := by
  apply Subtype.ext
  apply complete_eq_of_row (r := 1)
  intro i
  by_cases hi : i = 0
  · subst i
    exact one_parameter_fill b (oneParameter c)
  · simpa [fillOne, pureColoring, pureConnection, onePotential, hi, b.val.diagonal]
      using (c.property 1 i ⟨by decide, hi⟩).symm

def oneFillingEquiv (b : BoundaryOne (G := G)) : OneNew b ≃ G where
  toFun := oneParameter
  invFun := fillOne b
  left_inv := fill_one_parameter b
  right_inv := one_parameter_fill b

def fillTwo (b : BoundaryTwo (G := G)) : TwoNew b :=
  ⟨pureColoring (b.val.edge 2), by
    intro i j h
    exact (edge_from_root b.val 2 i j
      (b.property.2 2 i j (two_root_triangle i j h))).symm⟩

theorem two_filling_unique (b : BoundaryTwo (G := G)) (c : TwoNew b) :
    c = fillTwo b := by
  apply Subtype.ext
  apply complete_eq_of_row (r := 2)
  intro i
  simpa [fillTwo, pureColoring, pureConnection, b.val.diagonal]
    using c.property 2 i (two_root_edges i)

def fillThreeOld (b : BoundaryThree (G := G)) : ThreeOld b :=
  ⟨⟨b.val, b.property.1, by intro i j k _; exact boundary_three_flat b i j k trivial⟩,
    by intro i j _; rfl⟩
def fillThreeNew (b : BoundaryThree (G := G)) : ThreeNew b :=
  ⟨⟨b.val, b.property.1, by intro i j k _; exact boundary_three_flat b i j k trivial⟩,
    by intro i j _; rfl⟩

theorem three_old_unique (b : BoundaryThree (G := G)) (c : ThreeOld b) :
    c = fillThreeOld b := by
  apply Subtype.ext; apply Subtype.ext; apply Connection.ext
  funext i j; exact c.property i j trivial

theorem three_new_unique (b : BoundaryThree (G := G)) (c : ThreeNew b) :
    c = fillThreeNew b := by
  apply Subtype.ext; apply Subtype.ext; apply Connection.ext
  funext i j; exact c.property i j trivial

theorem card_of_unique_witness {α : Type*} [Fintype α] (a : α) (h : ∀ x, x = a) :
    Fintype.card α = 1 := by
  let : Unique α := ⟨⟨a⟩, h⟩
  exact Fintype.card_unique

theorem self_filling_count [Fintype G] {E : Vertex → Vertex → Prop}
    {T : Vertex → Vertex → Vertex → Prop} (b : @Coloring G _ E T) :
    Fintype.card (SelfFillings b) = 1 :=
  card_of_unique_witness (selfFilling b) (self_filling_unique b)

theorem one_filling_count [Fintype G] (b : BoundaryOne (G := G)) :
    Fintype.card (OneNew b) = Fintype.card G := Fintype.card_congr (oneFillingEquiv b)

theorem two_filling_count [Fintype G] (b : BoundaryTwo (G := G)) :
    Fintype.card (TwoNew b) = 1 := card_of_unique_witness (fillTwo b) (two_filling_unique b)

theorem three_old_count [Fintype G] (b : BoundaryThree (G := G)) :
    Fintype.card (ThreeOld b) = 1 := card_of_unique_witness (fillThreeOld b) (three_old_unique b)

theorem three_new_count [Fintype G] (b : BoundaryThree (G := G)) :
    Fintype.card (ThreeNew b) = 1 := card_of_unique_witness (fillThreeNew b) (three_new_unique b)

theorem unnormalized_one_five_iff [Fintype G] (b : BoundaryOne (G := G)) :
    Fintype.card (SelfFillings b) = Fintype.card (OneNew b) ↔ Fintype.card G = 1 := by
  rw [self_filling_count, one_filling_count]
  exact eq_comm

/-- Interior vertices are faces of one local complex but not of the common boundary. -/
def interiorVertices (p : Nat) (left : Bool) : Finset Vertex :=
  Finset.univ.filter (fun i => facetFace p left {i} ∧ ¬ facetFace p (!left) {i})


def localFacets (p : Nat) (left : Bool) : Finset (Finset Vertex) :=
  (Finset.univ.filter (fun v : Vertex => if left then v.val < p else p ≤ v.val)).image
    (fun v => Finset.univ.erase v)

theorem face_is_in_a_facet (p : Nat) (left : Bool) (s : Finset Vertex) :
    facetFace p left s ↔ ∃ f ∈ localFacets p left, s ⊆ f := by
  simp [facetFace, localFacets, Finset.subset_erase]

theorem local_facets_have_five_vertices (p : Nat) (left : Bool)
    (s : Finset Vertex) (h : s ∈ localFacets p left) : s.card = 5 := by
  obtain ⟨v, _, rfl⟩ := Finset.mem_image.mp h
  simp

theorem facet_counts :
    (localFacets 1 true).card = 1 ∧ (localFacets 1 false).card = 5 ∧
    (localFacets 2 true).card = 2 ∧ (localFacets 2 false).card = 4 ∧
    (localFacets 3 true).card = 3 ∧ (localFacets 3 false).card = 3 := by decide

@[simp] theorem one_old_interior : (interiorVertices 1 true).card = 0 := by decide
@[simp] theorem one_new_interior : (interiorVertices 1 false).card = 1 := by decide
@[simp] theorem two_old_interior : (interiorVertices 2 true).card = 0 := by decide
@[simp] theorem two_new_interior : (interiorVertices 2 false).card = 0 := by decide
@[simp] theorem three_old_interior : (interiorVertices 3 true).card = 0 := by decide
@[simp] theorem three_new_interior : (interiorVertices 3 false).card = 0 := by decide

/-- Count flat fillings with fixed boundary, normalized per interior vertex. -/
noncomputable def localAmplitude [Fintype G] (α : Type*) [Fintype α] (interior : Nat) : ℚ :=
  (Fintype.card α : ℚ) / (Fintype.card G : ℚ) ^ interior

theorem group_order_ne_zero [Fintype G] : (Fintype.card G : ℚ) ≠ 0 :=
  Nat.cast_ne_zero.mpr Fintype.card_ne_zero

theorem pachner_one_five [Fintype G] (b : BoundaryOne (G := G)) :
    localAmplitude (G := G) (SelfFillings b) (interiorVertices 1 true).card =
    localAmplitude (G := G) (OneNew b) (interiorVertices 1 false).card := by
  simp [localAmplitude, self_filling_count, one_filling_count, group_order_ne_zero (G := G)]

theorem pachner_two_four [Fintype G] (b : BoundaryTwo (G := G)) :
    localAmplitude (G := G) (SelfFillings b) (interiorVertices 2 true).card =
    localAmplitude (G := G) (TwoNew b) (interiorVertices 2 false).card := by
  simp [localAmplitude, self_filling_count, two_filling_count]

theorem pachner_three_three [Fintype G] (b : BoundaryThree (G := G)) :
    localAmplitude (G := G) (ThreeOld b) (interiorVertices 3 true).card =
    localAmplitude (G := G) (ThreeNew b) (interiorVertices 3 false).card := by
  simp [localAmplitude, three_old_count, three_new_count]

/-- Each outside configuration supplies its boundary; gluing is a dependent pair.
The denominator counts all vertices, with the boundary already in `outsideVertices`.
-/
noncomputable def stateSum [Fintype G] {X : Type*} [Fintype X]
    (F : X → Type*) [∀ x, Fintype (F x)] (vertices : Nat) : ℚ :=
  (Fintype.card (Σ x, F x) : ℚ) / (Fintype.card G : ℚ) ^ vertices

theorem glued_one_five [Fintype G] {X : Type*} [Fintype X]
    (b : X → BoundaryOne (G := G)) (outsideVertices : Nat) :
    stateSum (G := G) (fun x => SelfFillings (b x))
      (outsideVertices + (interiorVertices 1 true).card) =
    stateSum (G := G) (fun x => OneNew (b x))
      (outsideVertices + (interiorVertices 1 false).card) := by
  simp only [stateSum, Fintype.card_sigma, self_filling_count, one_filling_count,
    one_old_interior, one_new_interior, Nat.add_zero]
  simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one, Nat.cast_mul, pow_succ]
  field_simp [group_order_ne_zero (G := G)]

theorem glued_two_four [Fintype G] {X : Type*} [Fintype X]
    (b : X → BoundaryTwo (G := G)) (outsideVertices : Nat) :
    stateSum (G := G) (fun x => SelfFillings (b x))
      (outsideVertices + (interiorVertices 2 true).card) =
    stateSum (G := G) (fun x => TwoNew (b x))
      (outsideVertices + (interiorVertices 2 false).card) := by
  simp [stateSum, Fintype.card_sigma, self_filling_count, two_filling_count]

theorem glued_three_three [Fintype G] {X : Type*} [Fintype X]
    (b : X → BoundaryThree (G := G)) (outsideVertices : Nat) :
    stateSum (G := G) (fun x => ThreeOld (b x))
      (outsideVertices + (interiorVertices 3 true).card) =
    stateSum (G := G) (fun x => ThreeNew (b x))
      (outsideVertices + (interiorVertices 3 false).card) := by
  simp [stateSum, Fintype.card_sigma, three_old_count, three_new_count]

#print axioms nonflat_boundary_has_no_extension
#print axioms unnormalized_one_five_iff
#print axioms oneFillingEquiv
#print axioms one_filling_count
#print axioms two_filling_count
#print axioms three_old_count
#print axioms three_new_count
#print axioms face_is_in_a_facet
#print axioms pachner_one_five
#print axioms pachner_two_four
#print axioms pachner_three_three
#print axioms glued_one_five
#print axioms glued_two_four
#print axioms glued_three_three
end FiniteGroupPachner
