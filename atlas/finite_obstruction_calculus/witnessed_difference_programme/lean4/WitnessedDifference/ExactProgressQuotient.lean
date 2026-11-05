import WitnessedDifference.BeliefGameQuotient

/-! Necessary and sufficient structural laws for an exact operation quotient.
    A finite surjection has a representative; the explicit representative here makes the
    construction independent of any successful search outcome. Report labels
    may include checked resolution IDs and independently supplied authorization. -/
namespace WitnessedDifference.ExactProgressQuotient

open WitnessedDifference.CertifiedProgress
open WitnessedDifference.BeliefGameQuotient

structure FiberExact {S Q A R} (G : Game S A) (q : S → Q) (report : S → R) : Prop where
  target : ∀ x y, q x = q y → (G.target x ↔ G.target y)
  enabled : ∀ x y a, q x = q y → (G.enabled x a ↔ G.enabled y a)
  price : ∀ x y a, q x = q y → G.enabled x a → G.cost x a = G.cost y a
  successors : ∀ x y a, q x = q y → G.enabled x a → ∀ z,
    (∃ t, t ∈ G.successors x a ∧ q t = z) ↔
    (∃ t, t ∈ G.successors y a ∧ q t = z)
  reports : ∀ x y, q x = q y → report x = report y

def quotient {S Q A} (G : Game S A) (q : S → Q) (representative : Q → S) : Game Q A where
  target z := G.target (representative z)
  enabled z a := G.enabled (representative z) a
  cost z a := G.cost (representative z) a
  successors z a := (G.successors (representative z) a).map q
  positive z a ha := G.positive (representative z) a ha
  nonempty z a ha := by
    obtain ⟨y, hy⟩ := G.nonempty (representative z) a ha
    exact ⟨q y, List.mem_map.mpr ⟨y, hy, rfl⟩⟩

theorem fiber_laws_construct_exact {S Q A R} (G : Game S A) (q : S → Q)
    (representative : Q → S) (hs : ∀ z, q (representative z) = z) (report : S → R)
    (h : FiberExact G q report) : TwoSided G (quotient G q representative) q := by
  have eq (x : S) : q x = q (representative (q x)) := (hs (q x)).symm
  refine ⟨fun x => h.target x _ (eq x), fun x a => h.enabled x _ a (eq x),
    fun x a ha => h.price x _ a (eq x) ha, ?_, ?_⟩
  · intro x a ha y hy
    obtain ⟨t, ht, he⟩ := (h.successors x _ a (eq x) ha (q y)).mp ⟨y, hy, rfl⟩
    exact List.mem_map.mpr ⟨t, ht, he⟩
  · intro x a ha z hz
    obtain ⟨t, ht, he⟩ := List.mem_map.mp hz
    exact (h.successors x _ a (eq x) ha z).mpr ⟨t, ht, he⟩

theorem exact_implies_fiber_laws {S Q A R} (G : Game S A) (H : Game Q A)
    (q : S → Q) (report : S → R) (coarseReport : Q → R)
    (h : TwoSided G H q) (hr : ∀ x, coarseReport (q x) = report x) :
    FiberExact G q report := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro x y he
    exact (h.target x).trans (he ▸ (h.target y).symm)
  · intro x y a he
    exact (h.enabled x a).trans (he ▸ (h.enabled y a).symm)
  · intro x y a he ha
    have hb := (h.enabled y a).mpr (he ▸ (h.enabled x a).mp ha)
    calc G.cost x a = H.cost (q x) a := h.price x a ha
         _ = H.cost (q y) a := congrArg (fun z => H.cost z a) he
         _ = G.cost y a := (h.price y a hb).symm
  · intro x y a he ha z
    have hb := (h.enabled y a).mpr (he ▸ (h.enabled x a).mp ha)
    constructor
    · rintro ⟨t, ht, rfl⟩
      exact h.backward y a hb (q t) (he ▸ h.forward x a ha t ht)
    · rintro ⟨t, ht, rfl⟩
      exact h.backward x a ha (q t) (he.symm ▸ h.forward y a hb t ht)
  · intro x y he
    rw [← hr x, ← hr y, he]

theorem exact_quotient_exists_iff {S Q A R} (G : Game S A) (q : S → Q)
    (representative : Q → S) (hs : ∀ z, q (representative z) = z) (report : S → R) :
    (∃ H : Game Q A, ∃ r : Q → R, TwoSided G H q ∧
      ∀ x, r (q x) = report x) ↔ FiberExact G q report := by
  constructor
  · rintro ⟨H, r, h, hr⟩
    exact exact_implies_fiber_laws G H q report r h hr
  · intro h
    refine ⟨quotient G q representative, fun z => report (representative z),
      fiber_laws_construct_exact G q representative hs report h, ?_⟩
    intro x
    exact h.reports _ x (hs (q x))

theorem exact_preserves_all_budgets {S Q A R} (G : Game S A) (q : S → Q)
    (representative : Q → S) (hs : ∀ z, q (representative z) = z) (report : S → R)
    (h : FiberExact G q report) (x : S) (budget : Rat) :
    (∃ n, BudgetReach G n budget x) ↔
      ∃ n, BudgetReach (quotient G q representative) n budget (q x) :=
  achievable_budgets_equal (fiber_laws_construct_exact G q representative hs report h) x budget

noncomputable def reportSeed {S R} (pairs : List (S × S)) (report : S → R) : List (S × S) := by
  classical
  exact pairs.filter (fun p => report p.1 = report p.2)

theorem stabilized_reports_preserved {S A R} (G : Game S A) (pairs : List (S × S))
    (report : S → R) (n : Nat) (x y : S)
    (h : (x,y) ∈ stabilize G n (reportSeed pairs report)) : report x = report y := by
  classical
  have hs := stabilized_subset G n (reportSeed pairs report) x y h
  exact of_decide_eq_true (List.mem_filter.mp hs).2

theorem coarsest_reported_refinement {S A R} (G : Game S A) (pairs : List (S × S))
    (report : S → R) (U : S → S → Prop)
    (stable : ∀ x y, U x y → Compatible G U x y)
    (labels : ∀ x y, U x y → report x = report y)
    (included : ∀ x y, U x y → (x,y) ∈ pairs) (n : Nat) :
    ∀ x y, U x y → (x,y) ∈ stabilize G n (reportSeed pairs report) := by
  classical
  apply stable_refinement_retained G U stable n (reportSeed pairs report)
  intro x y h
  exact List.mem_filter.mpr ⟨included x y h, by simp [labels x y h]⟩

theorem reported_refinement_fixed {S A R} (G : Game S A) (pairs : List (S × S))
    (report : S → R) :
    refinePairs G (stabilize G (reportSeed pairs report).length (reportSeed pairs report)) =
      stabilize G (reportSeed pairs report).length (reportSeed pairs report) :=
  stabilization_is_fixed G _ _ (Nat.le_refl _)

end WitnessedDifference.ExactProgressQuotient

#print axioms WitnessedDifference.ExactProgressQuotient.fiber_laws_construct_exact
#print axioms WitnessedDifference.ExactProgressQuotient.exact_implies_fiber_laws
#print axioms WitnessedDifference.ExactProgressQuotient.exact_quotient_exists_iff
#print axioms WitnessedDifference.ExactProgressQuotient.exact_preserves_all_budgets
#print axioms WitnessedDifference.ExactProgressQuotient.stabilized_reports_preserved
#print axioms WitnessedDifference.ExactProgressQuotient.coarsest_reported_refinement
#print axioms WitnessedDifference.ExactProgressQuotient.reported_refinement_fixed
