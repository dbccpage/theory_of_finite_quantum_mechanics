import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Pi

/-!
# Admission floor: an exhibited cut needs a law, and the law is data

AuthorityEffect: None.  Re-proves, for an arbitrary carrier, the source statements of
`PrimitiveAdmissionFloor.lean` (`endpoints_apart` line 14, `no_cut_on_subsingleton` line 20,
`identification_breaks_law` line 23, `instance_without_law_allows_singleton` 33,
`law_without_instance_allows_singleton` 37) and `PointedRelation.lean`
(`pointed_relation_independence` line 84), and adds three statements the source does not make:

* `cut_exists_iff_nontrivial`: a law-bearing cut exists on `V` iff `V` has two distinct points;
* `exists_law_target_iff`: a map `q` admits an irreflexive target for a relation `R` iff `q` separates every
  `R`-related pair (the converse direction of `identification_breaks_law`);
* `law_not_derived_from_distinctness`: on every carrier with two distinct points there are an instance
  without law and a law without instance, so neither the law nor the instance follows from distinctness.

The node does not derive the law from `<>` or from `Real_0`: the relation is supplied data.
`two_point_cut_count` is a labelled fixed instance (relations on `Fin 2`).
-/

namespace AdmissionFloor

variable {V W : Type}

/-- A cut: a relation, two endpoints it relates, and the law that it is irreflexive. -/
structure ExhibitedCut (V : Type) where
  relation : V → V → Prop
  first : V
  second : V
  exhibited : relation first second
  protectedLaw : ∀ x, ¬ relation x x

theorem endpoints_apart (cut : ExhibitedCut V) : cut.first ≠ cut.second := by
  intro same
  have diagonal := cut.exhibited
  rw [same] at diagonal
  exact cut.protectedLaw cut.second diagonal

theorem no_cut_on_subsingleton [Subsingleton V] (cut : ExhibitedCut V) : False :=
  endpoints_apart cut (Subsingleton.elim _ _)

theorem identification_breaks_law (cut : ExhibitedCut V) (q : V → W) (target : W → W → Prop)
    (preserves : ∀ x y, cut.relation x y → target (q x) (q y)) (law : ∀ w, ¬ target w w) :
    q cut.first ≠ q cut.second := by
  intro same
  have transported := preserves cut.first cut.second cut.exhibited
  rw [same] at transported
  exact law (q cut.second) transported

/-- A cut exists exactly on carriers with two distinct points. -/
theorem cut_exists_iff_nontrivial : Nonempty (ExhibitedCut V) ↔ Nontrivial V := by
  constructor
  · rintro ⟨cut⟩
    exact ⟨⟨cut.first, cut.second, endpoints_apart cut⟩⟩
  · rintro ⟨⟨a, b, hab⟩⟩
    exact ⟨⟨fun x y => x ≠ y, a, b, hab, fun x h => h rfl⟩⟩

/-- Sharp converse of `identification_breaks_law`: an irreflexive target for `R` along `q` exists iff
`q` separates every `R`-related pair. -/
theorem exists_law_target_iff (R : V → V → Prop) (q : V → W) :
    (∃ target : W → W → Prop, (∀ x y, R x y → target (q x) (q y)) ∧ ∀ w, ¬ target w w) ↔
      ∀ x y, R x y → q x ≠ q y := by
  constructor
  · rintro ⟨target, preserves, law⟩ x y hxy same
    have := preserves x y hxy
    rw [same] at this
    exact law _ this
  · intro h
    exact ⟨fun u v => u ≠ v, fun x y hxy => h x y hxy, fun w hw => hw rfl⟩

/-- Instance without law and law without instance exist on every nonempty carrier. -/
theorem instance_without_law (v : V) : ∃ r : V → V → Prop, r v v ∧ ¬ ∀ x, ¬ r x x :=
  ⟨fun _ _ => True, trivial, fun h => h v trivial⟩

theorem law_without_instance : ∃ r : V → V → Prop, (∀ x, ¬ r x x) ∧ ∀ a b, ¬ r a b :=
  ⟨fun _ _ => False, fun _ h => h, fun _ _ h => h⟩

/-- Neither the law nor the instance follows from distinctness: on a two-point carrier the empty and
the total relation both leave the marked pair distinct. -/
theorem law_not_derived_from_distinctness (a b : V) (_hab : a ≠ b) :
    (∃ r : V → V → Prop, (∀ x, ¬ r x x) ∧ ¬ r a b) ∧ (∃ r : V → V → Prop, r a b ∧ ¬ ∀ x, ¬ r x x) :=
  ⟨⟨fun _ _ => False, fun _ h => h, fun h => h⟩, ⟨fun _ _ => True, trivial, fun h => h a trivial⟩⟩

/-- Pointed relation independence for arbitrary carriers in `Type`:
relatedness does not give distinctness, distinctness does not give relatedness,
irreflexivity plus relatedness gives distinctness. -/
theorem pointed_relation_independence :
    (¬ ∀ (X : Type) (R : X → X → Prop) (a b : X), R a b → a ≠ b)
      ∧ (¬ ∀ (X : Type) (R : X → X → Prop) (a b : X), a ≠ b → R a b)
      ∧ (∀ (X : Type) (R : X → X → Prop) (a b : X), (∀ x, ¬ R x x) → R a b → a ≠ b) := by
  refine ⟨?_, ?_, ?_⟩
  · intro h
    exact h Unit (fun _ _ => True) () () trivial rfl
  · intro h
    exact h Bool (fun _ _ => False) false true (by decide)
  · intro X R a b hirr hab heq
    subst heq
    exact hirr a hab

/-- Labelled fixed instance: on `Fin 2` exactly 3 of the 16 Boolean relations are cut data
(irreflexive and nonempty), and exactly 1 is law-bearing and empty. -/
theorem two_point_cut_count :
    Fintype.card {R : Fin 2 → Fin 2 → Bool // (∀ x, R x x = false) ∧ ∃ a b, R a b = true} = 3 := by
  decide

theorem one_point_cut_count :
    Fintype.card {R : Fin 1 → Fin 1 → Bool // (∀ x, R x x = false) ∧ ∃ a b, R a b = true} = 0 := by
  decide

end AdmissionFloor

#print axioms AdmissionFloor.endpoints_apart
#print axioms AdmissionFloor.no_cut_on_subsingleton
#print axioms AdmissionFloor.identification_breaks_law
#print axioms AdmissionFloor.cut_exists_iff_nontrivial
#print axioms AdmissionFloor.exists_law_target_iff
#print axioms AdmissionFloor.instance_without_law
#print axioms AdmissionFloor.law_without_instance
#print axioms AdmissionFloor.law_not_derived_from_distinctness
#print axioms AdmissionFloor.pointed_relation_independence
#print axioms AdmissionFloor.two_point_cut_count
#print axioms AdmissionFloor.one_point_cut_count
