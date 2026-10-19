import Mathlib.CategoryTheory.PathCategory.Basic

/-! AuthorityEffect: None. Actual Mathlib quiver paths/category and universal
extension,chronological edge words and strict-rank finite length. Rust graph
admission,Kahn rank,complete bounded enumeration/table/certificate refinement
separate;the mathematical lift is not a newly implemented Rust lift API. -/
namespace TFQM.FinitePath
open CategoryTheory

universe u v w
variable {V : Type u} [Quiver.{v} V] {a b c d : V}

theorem identity_comp (p : Quiver.Path a b) : Quiver.Path.nil.comp p = p :=
  Quiver.Path.nil_comp p

theorem comp_identity (p : Quiver.Path a b) : p.comp Quiver.Path.nil = p :=
  Quiver.Path.comp_nil p

theorem comp_associative (p : Quiver.Path a b) (q : Quiver.Path b c) (r : Quiver.Path c d) :
    (p.comp q).comp r = p.comp (q.comp r) := Quiver.Path.comp_assoc p q r

theorem length_identity (a : V) : (Quiver.Path.nil : Quiver.Path a a).length = 0 := rfl

theorem length_composition (p : Quiver.Path a b) (q : Quiver.Path b c) :
    (p.comp q).length = p.length + q.length := Quiver.Path.length_comp p q

def edgeWord {E : Type w} (label : ∀ {x y : V}, (x ⟶ y) → E) {a : V} :
    ∀ {b : V}, Quiver.Path a b → List E
  | _, .nil => []
  | _, .cons p e => edgeWord label p ++ [label e]

theorem word_identity {E : Type w} (label : ∀ {x y : V}, (x ⟶ y) → E) (a : V) :
    edgeWord label (Quiver.Path.nil : Quiver.Path a a) = [] := rfl

theorem word_composition {E : Type w} (label : ∀ {x y : V}, (x ⟶ y) → E)
    (p : Quiver.Path a b) (q : Quiver.Path b c) :
    edgeWord label (p.comp q) = edgeWord label p ++ edgeWord label q := by
  induction q with
  | nil => simp only [Quiver.Path.comp_nil, edgeWord, List.append_nil]
  | cons q e ih => simp only [Quiver.Path.comp_cons, edgeWord, ih, List.append_assoc]

theorem word_length {E : Type w} (label : ∀ {x y : V}, (x ⟶ y) → E) (p : Quiver.Path a b) :
    (edgeWord label p).length = p.length := by
  induction p with
  | nil => rfl
  | cons p e ih => simp only [edgeWord, List.length_append, List.length_singleton, Quiver.Path.length_cons, ih]

theorem rank_length (rank : V → Nat) (strict : ∀ {x y : V}, (x ⟶ y) → rank x < rank y)
    (p : Quiver.Path a b) : rank a + p.length ≤ rank b := by
  induction p with
  | nil => simp
  | cons p e ih =>
    have step := strict e
    simp only [Quiver.Path.length_cons]
    omega

theorem rank_bound (rank : V → Nat) (strict : ∀ {x y : V}, (x ⟶ y) → rank x < rank y)
    (vertices : Nat) (bounded : ∀ x, rank x < vertices) (p : Quiver.Path a b) :
    p.length < vertices := by
  have lengthBound := rank_length rank strict p
  have endpointBound := bounded b
  omega

theorem rank_no_cycle (rank : V → Nat) (strict : ∀ {x y : V}, (x ⟶ y) → rank x < rank y)
    (p : Quiver.Path a a) : p = Quiver.Path.nil := by
  apply Quiver.Path.eq_nil_of_length_zero
  have lengthBound := rank_length rank strict p
  omega

variable {C : Type w} [Category C]

theorem lift_identity (assignment : V ⥤q C) (x : V) :
    (Paths.lift assignment).map (Quiver.Path.nil : Quiver.Path x x) = 𝟙 (assignment.obj x) :=
  Paths.lift_nil assignment x

theorem lift_edge (assignment : V ⥤q C) (edge : a ⟶ b) :
    (Paths.lift assignment).map edge.toPath = assignment.map edge := Paths.lift_toPath assignment edge

theorem lift_composition (assignment : V ⥤q C) (p : Quiver.Path a b) (q : Quiver.Path b c) :
    (Paths.lift assignment).map (p.comp q) =
      (Paths.lift assignment).map p ≫ (Paths.lift assignment).map q :=
  (Paths.lift assignment).map_comp p q

theorem lift_unique (assignment : V ⥤q C) (extension : Paths V ⥤ C)
    (onGenerators : Paths.of V ⋙q extension.toPrefunctor = assignment) :
    extension = Paths.lift assignment := Paths.lift_unique assignment extension onGenerators

theorem bounded_fresh (count budget : Nat) (within : count ≤ budget) (notFull : count ≠ budget) :
    count + 1 ≤ budget := by omega

theorem bounded_count (count budget : Nat) (within : count ≤ budget) (cap : budget ≤ 64) :
    count ≤ 64 := Nat.le_trans within cap

end TFQM.FinitePath

#print axioms TFQM.FinitePath.identity_comp
#print axioms TFQM.FinitePath.comp_identity
#print axioms TFQM.FinitePath.comp_associative
#print axioms TFQM.FinitePath.length_identity
#print axioms TFQM.FinitePath.length_composition
#print axioms TFQM.FinitePath.edgeWord
#print axioms TFQM.FinitePath.word_identity
#print axioms TFQM.FinitePath.word_composition
#print axioms TFQM.FinitePath.word_length
#print axioms TFQM.FinitePath.rank_length
#print axioms TFQM.FinitePath.rank_bound
#print axioms TFQM.FinitePath.rank_no_cycle
#print axioms TFQM.FinitePath.lift_identity
#print axioms TFQM.FinitePath.lift_edge
#print axioms TFQM.FinitePath.lift_composition
#print axioms TFQM.FinitePath.lift_unique
#print axioms TFQM.FinitePath.bounded_fresh
#print axioms TFQM.FinitePath.bounded_count
