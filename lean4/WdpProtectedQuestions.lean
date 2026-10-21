import Mathlib.Data.Fintype.Card
import Mathlib.Logic.Equiv.Fintype
import Mathlib.Data.Set.Card

/-!
# Symmetry price of selecting a point on an unstructured set (WDP-CH03-P01 / D01 / N01)

AuthorityEffect: None.  Scope: a bare type `X` with the full permutation action `Equiv.Perm X`.
A *declared input set* `S` is modelled as a subset whose points are fixed pointwise (the stabiliser of `S`);
this is the narrowest model of "declared input breaks the symmetry" and is a MODELLING CHOICE (the setwise
stabiliser, which only fixes `S` as a set, would give a different table): the ledger
definition WDP-CH03-D01 is relative to an implementation class and a dependency preorder, which are not
modelled here.  The singleton frontier below is a near-consequence of that choice: a declared point is fixed because it is declared
(first disjunct of `invariantUnder_iff`).  `Selecting`/`MinimalSelecting` is NOT ledger D01 (minimal input sets whose
removal restores a symmetry that moves the output); no equivariant-selection-function type is defined, `no_fully_invariant_point`
is its bare-set specialisation.  Everything below is symmetry-price bookkeeping only.  It does not say that retention,
dynamics or observers are impossible, and it does not port WDP-CH03-P03 (declare-then-assert grammar).
The source theorem `no_fully_invariant_point` is general (any type with two distinct points); the source
witness `pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` is unrelated fixed arithmetic.
-/

namespace WdpProtectedQuestions

variable {X : Type*}

/-- `σ` fixes the declared set `S` pointwise. -/
def FixesPointwise (S : Set X) (σ : Equiv.Perm X) : Prop := ∀ s ∈ S, σ s = s

/-- `x` is invariant under every symmetry that keeps the declared set `S` fixed pointwise. -/
def InvariantUnder (S : Set X) (x : X) : Prop := ∀ σ : Equiv.Perm X, FixesPointwise S σ → σ x = x

/-- `S` is *selecting*: some point is invariant under the stabiliser of `S`. -/
def Selecting (S : Set X) : Prop := ∃ x, InvariantUnder S x

/-- Inclusion-minimal selecting sets: the asymmetry-price frontier in this model. -/
def MinimalSelecting (S : Set X) : Prop := Selecting S ∧ ∀ T : Set X, T ⊂ S → ¬ Selecting T

/-- General source statement (Symmetry.lean `no_fully_invariant_point`): no point is fixed by all of Sym(X). -/
theorem no_fully_invariant_point [DecidableEq X] [Nontrivial X] :
    ¬ ∃ x : X, ∀ σ : Equiv.Perm X, σ x = x := by
  rintro ⟨x, hx⟩
  obtain ⟨y, hy⟩ := exists_ne x
  have h1 := hx (Equiv.swap x y)
  rw [Equiv.swap_apply_left] at h1
  exact hy h1

/-- The same, phrased with `2 ≤ card X`. -/
theorem no_fully_invariant_point_card [DecidableEq X] [Fintype X] (h : 2 ≤ Fintype.card X) :
    ¬ ∃ x : X, ∀ σ : Equiv.Perm X, σ x = x := by
  have : Nontrivial X := Fintype.one_lt_card_iff_nontrivial.mp h
  exact no_fully_invariant_point

/-- Exact characterisation of the points invariant under the stabiliser of `S`. -/
theorem invariantUnder_iff [DecidableEq X] (S : Set X) (x : X) :
    InvariantUnder S x ↔ x ∈ S ∨ ∀ y, y ∉ S → y = x := by
  constructor
  · intro hx
    by_cases hxS : x ∈ S
    · exact Or.inl hxS
    · refine Or.inr (fun y hyS => ?_)
      by_contra hne
      have hfix : FixesPointwise S (Equiv.swap x y) := by
        intro s hs
        have h1 : s ≠ x := fun h => hxS (h ▸ hs)
        have h2 : s ≠ y := fun h => hyS (h ▸ hs)
        exact Equiv.swap_apply_of_ne_of_ne h1 h2
      have := hx _ hfix
      rw [Equiv.swap_apply_left] at this
      exact hne this
  · rintro (hxS | hall) σ hσ
    · exact hσ x hxS
    · by_cases hxS : x ∈ S
      · exact hσ x hxS
      · have hσxS : σ x ∉ S := by
          intro hs
          have h1 : σ (σ x) = σ x := hσ _ hs
          exact hxS (by rw [← σ.injective h1]; exact hs)
        exact hall _ hσxS

/-- `S` selects a point iff it is nonempty or the carrier has exactly one point. -/
theorem selecting_iff [DecidableEq X] (S : Set X) :
    Selecting S ↔ S.Nonempty ∨ ∃ x : X, ∀ y : X, y = x := by
  constructor
  · rintro ⟨x, hx⟩
    rcases (invariantUnder_iff S x).mp hx with h | h
    · exact Or.inl ⟨x, h⟩
    · by_cases hne : S.Nonempty
      · exact Or.inl hne
      · refine Or.inr ⟨x, fun y => h y ?_⟩
        intro hy
        exact hne ⟨y, hy⟩
  · rintro (⟨s, hs⟩ | ⟨x, hx⟩)
    · exact ⟨s, (invariantUnder_iff S s).mpr (Or.inl hs)⟩
    · exact ⟨x, (invariantUnder_iff S x).mpr (Or.inr (fun y _ => hx y))⟩

/-- For a carrier with at least two points, selecting means nonempty: the price is at least one declared point. -/
theorem selecting_iff_nonempty [DecidableEq X] [Nontrivial X] (S : Set X) :
    Selecting S ↔ S.Nonempty := by
  rw [selecting_iff]
  constructor
  · rintro (h | ⟨x, hx⟩)
    · exact h
    · obtain ⟨a, b, hab⟩ := exists_pair_ne X
      exact absurd ((hx a).trans (hx b).symm) hab
  · exact Or.inl

/-- The frontier for at least two points is exactly the family of singletons. -/
theorem minimalSelecting_iff_singleton [DecidableEq X] [Nontrivial X] (S : Set X) :
    MinimalSelecting S ↔ ∃ x, S = {x} := by
  constructor
  · rintro ⟨hsel, hmin⟩
    obtain ⟨x, hx⟩ := (selecting_iff_nonempty S).mp hsel
    refine ⟨x, ?_⟩
    by_contra hne
    have hsub : ({x} : Set X) ⊂ S :=
      Set.ssubset_iff_subset_ne.mpr ⟨Set.singleton_subset_iff.mpr hx, fun h => hne h.symm⟩
    exact hmin _ hsub ((selecting_iff_nonempty _).mpr ⟨x, rfl⟩)
  · rintro ⟨x, rfl⟩
    refine ⟨(selecting_iff_nonempty _).mpr ⟨x, rfl⟩, fun T hT hTsel => ?_⟩
    obtain ⟨y, hy⟩ := (selecting_iff_nonempty T).mp hTsel
    have : y = x := hT.1 hy
    subst this
    exact hT.2 (Set.singleton_subset_iff.mpr hy)

/-- The frontier is in bijection with the carrier (at least two points); this carries the content for infinite
carriers, where a cardinality statement would read `0 = 0`. -/
noncomputable def frontierEquiv [DecidableEq X] [Nontrivial X] : X ≃ {S : Set X // MinimalSelecting S} :=
  Equiv.ofBijective (fun x => (⟨{x}, (minimalSelecting_iff_singleton _).mpr ⟨x, rfl⟩⟩ : {S : Set X // MinimalSelecting S}))
    ⟨fun a b hab => Set.singleton_eq_singleton_iff.mp (congrArg Subtype.val hab),
     fun ⟨S, hS⟩ => by
       obtain ⟨x, rfl⟩ := (minimalSelecting_iff_singleton S).mp hS
       exact ⟨x, rfl⟩⟩

/-- Cardinality form; informative only for finite carriers (`Nat.card` of an infinite type is `0`). -/
theorem frontier_card [DecidableEq X] [Nontrivial X] :
    Nat.card {S : Set X // MinimalSelecting S} = Nat.card X :=
  (Nat.card_congr frontierEquiv).symm

/-- Boundary (hypothesis dropped): on a one-point carrier the empty declaration already selects, price zero. -/
theorem one_point_empty_selects [DecidableEq X] [Subsingleton X] [Nonempty X] : Selecting (∅ : Set X) := by
  rw [selecting_iff]
  obtain ⟨x⟩ := ‹Nonempty X›
  exact Or.inr ⟨x, fun y => Subsingleton.elim y x⟩

/-- Boundary: on an empty carrier nothing is selected, whatever is declared. -/
theorem empty_carrier_no_selection [IsEmpty X] (S : Set X) : ¬ Selecting S := by
  rintro ⟨x, _⟩
  exact isEmptyElim x

/-- Instance (not the general statement): the two-point carrier `Bool`. -/
theorem bool_instance :
    ¬ Selecting (∅ : Set Bool) ∧ Selecting ({true} : Set Bool) ∧ MinimalSelecting ({false} : Set Bool) :=
  ⟨fun h => by simpa using (selecting_iff_nonempty (∅ : Set Bool)).mp h,
   (selecting_iff_nonempty _).mpr ⟨true, rfl⟩,
   (minimalSelecting_iff_singleton _).mpr ⟨false, rfl⟩⟩

end WdpProtectedQuestions

#print axioms WdpProtectedQuestions.no_fully_invariant_point
#print axioms WdpProtectedQuestions.no_fully_invariant_point_card
#print axioms WdpProtectedQuestions.invariantUnder_iff
#print axioms WdpProtectedQuestions.selecting_iff
#print axioms WdpProtectedQuestions.selecting_iff_nonempty
#print axioms WdpProtectedQuestions.minimalSelecting_iff_singleton
#print axioms WdpProtectedQuestions.frontierEquiv
#print axioms WdpProtectedQuestions.frontier_card
#print axioms WdpProtectedQuestions.one_point_empty_selects
#print axioms WdpProtectedQuestions.empty_carrier_no_selection
#print axioms WdpProtectedQuestions.bool_instance
