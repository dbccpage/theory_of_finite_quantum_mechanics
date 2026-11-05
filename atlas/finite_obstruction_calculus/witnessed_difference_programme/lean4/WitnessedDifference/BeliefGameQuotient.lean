import WitnessedDifference.CertifiedProgress
import Init.Data.List.Sublist

/-! Two-sided belief-arena transport and constructive finite relation refinement.
    These are game laws, not extraction of a physical observer or verification
    of the Python partition implementation. The finite relation algorithm uses
    classical decisions; the supplied Python tables provide effective decisions. -/
namespace WitnessedDifference.BeliefGameQuotient

open WitnessedDifference.CertifiedProgress

universe u v w

structure TwoSided {S : Type u} {Q : Type v} {A : Type w}
    (fine : Game S A) (coarse : Game Q A) (q : S → Q) : Prop where
  target : ∀ x, fine.target x ↔ coarse.target (q x)
  enabled : ∀ x a, fine.enabled x a ↔ coarse.enabled (q x) a
  price : ∀ x a, fine.enabled x a → fine.cost x a = coarse.cost (q x) a
  forward : ∀ x a, fine.enabled x a → ∀ y, y ∈ fine.successors x a →
    q y ∈ coarse.successors (q x) a
  backward : ∀ x a, fine.enabled x a → ∀ z, z ∈ coarse.successors (q x) a →
    ∃ y, y ∈ fine.successors x a ∧ q y = z

theorem reach_transport {S Q A} {fine : Game S A} {coarse : Game Q A} {q : S → Q}
    (sim : TwoSided fine coarse q) (n : Nat) :
    ∀ x, Reach fine n x ↔ Reach coarse n (q x) := by
  induction n with
  | zero => exact sim.target
  | succ n ih =>
    intro x
    constructor
    · rintro (ht | ⟨a, ha, hs⟩)
      · exact Or.inl ((sim.target x).mp ht)
      · refine Or.inr ⟨a, (sim.enabled x a).mp ha, ?_⟩
        intro z hz
        obtain ⟨y, hy, rfl⟩ := sim.backward x a ha z hz
        exact (ih y).mp (hs y hy)
    · rintro (ht | ⟨a, ha, hs⟩)
      · exact Or.inl ((sim.target x).mpr ht)
      · have hf := (sim.enabled x a).mpr ha
        exact Or.inr ⟨a, hf, fun y hy =>
          (ih y).mpr (hs (q y) (sim.forward x a hf y hy))⟩

theorem winning_transport {S Q A} {fine : Game S A} {coarse : Game Q A} {q : S → Q}
    (sim : TwoSided fine coarse q) (x : S) : Winning fine x ↔ Winning coarse (q x) := by
  constructor
  · rintro ⟨n, hn⟩
    exact ⟨n, (reach_transport sim n x).mp hn⟩
  · rintro ⟨n, hn⟩
    exact ⟨n, (reach_transport sim n x).mpr hn⟩

theorem budget_transport {S Q A} {fine : Game S A} {coarse : Game Q A} {q : S → Q}
    (sim : TwoSided fine coarse q) (n : Nat) :
    ∀ budget x, BudgetReach fine n budget x ↔ BudgetReach coarse n budget (q x) := by
  induction n with
  | zero =>
    intro budget x
    exact and_congr (sim.target x) Iff.rfl
  | succ n ih =>
    intro budget x
    constructor
    · rintro (⟨ht, hb⟩ | ⟨a, ha, hc, hs⟩)
      · exact Or.inl ⟨(sim.target x).mp ht, hb⟩
      · refine Or.inr ⟨a, (sim.enabled x a).mp ha, (sim.price x a ha) ▸ hc, ?_⟩
        intro z hz
        obtain ⟨y, hy, rfl⟩ := sim.backward x a ha z hz
        rw [← sim.price x a ha]
        exact (ih _ y).mp (hs y hy)
    · rintro (⟨ht, hb⟩ | ⟨a, ha, hc, hs⟩)
      · exact Or.inl ⟨(sim.target x).mpr ht, hb⟩
      · have hf := (sim.enabled x a).mpr ha
        refine Or.inr ⟨a, hf, (sim.price x a hf).symm ▸ hc, ?_⟩
        intro y hy
        apply (ih _ y).mpr
        rw [sim.price x a hf]
        exact hs (q y) (sim.forward x a hf y hy)

theorem achievable_budgets_equal {S Q A} {fine : Game S A} {coarse : Game Q A} {q : S → Q}
    (sim : TwoSided fine coarse q) (x : S) (budget : Rat) :
    (∃ n, BudgetReach fine n budget x) ↔ ∃ n, BudgetReach coarse n budget (q x) := by
  constructor
  · rintro ⟨n, hn⟩
    exact ⟨n, (budget_transport sim n budget x).mp hn⟩
  · rintro ⟨n, hn⟩
    exact ⟨n, (budget_transport sim n budget x).mpr hn⟩

structure OptionalExtension {S A} (old new : Game S A) : Prop where
  target : ∀ x, old.target x → new.target x
  enabled : ∀ x a, old.enabled x a → new.enabled x a
  price : ∀ x a, old.enabled x a → old.cost x a = new.cost x a
  successors : ∀ x a, old.enabled x a → ∀ y, y ∈ new.successors x a →
    y ∈ old.successors x a

theorem optional_actions_preserve_budget {S A} {old new : Game S A}
    (extension : OptionalExtension old new) (n : Nat) :
    ∀ budget x, BudgetReach old n budget x → BudgetReach new n budget x := by
  induction n with
  | zero => exact fun _ x h => ⟨extension.target x h.1, h.2⟩
  | succ n ih =>
    intro budget x h
    rcases h with ⟨ht, hb⟩ | ⟨a, ha, hc, hs⟩
    · exact Or.inl ⟨extension.target x ht, hb⟩
    · refine Or.inr ⟨a, extension.enabled x a ha, (extension.price x a ha) ▸ hc, ?_⟩
      intro y hy
      rw [← extension.price x a ha]
      exact ih _ y (hs y (extension.successors x a ha y hy))

def Compatible {S A} (G : Game S A) (R : S → S → Prop) (x y : S) : Prop :=
  (G.target x ↔ G.target y) ∧ ∀ a,
    (G.enabled x a ↔ G.enabled y a) ∧ (G.enabled x a →
      G.cost x a = G.cost y a ∧
      (∀ z, z ∈ G.successors x a → ∃ t, t ∈ G.successors y a ∧ R z t) ∧
      (∀ t, t ∈ G.successors y a → ∃ z, z ∈ G.successors x a ∧ R z t))

theorem compatible_mono {S A} (G : Game S A) {R U : S → S → Prop}
    (subset : ∀ x y, R x y → U x y) {x y : S} (h : Compatible G R x y) :
    Compatible G U x y := by
  refine ⟨h.1, ?_⟩
  intro a
  refine ⟨(h.2 a).1, ?_⟩
  intro ha
  obtain ⟨hc, hf, hb⟩ := (h.2 a).2 ha
  refine ⟨hc, ?_, ?_⟩
  · intro z hz
    obtain ⟨t, ht, hr⟩ := hf z hz
    exact ⟨t, ht, subset z t hr⟩
  · intro t ht
    obtain ⟨z, hz, hr⟩ := hb t ht
    exact ⟨z, hz, subset z t hr⟩

noncomputable def refinePairs {S A} (G : Game S A) (pairs : List (S × S)) : List (S × S) :=
  by
    classical
    exact pairs.filter (fun p => decide (Compatible G (fun x y => (x, y) ∈ pairs) p.1 p.2))

theorem mem_refinePairs {S A} (G : Game S A) (pairs : List (S × S)) (x y : S) :
    (x, y) ∈ refinePairs G pairs ↔
    (x, y) ∈ pairs ∧ Compatible G (fun z t => (z, t) ∈ pairs) x y := by
  classical
  simp [refinePairs]

theorem strict_refinement_decreases_length {S A} (G : Game S A)
    (pairs : List (S × S)) (h : refinePairs G pairs ≠ pairs) :
    (refinePairs G pairs).length < pairs.length := by
  classical
  have sub : List.Sublist (refinePairs G pairs) pairs := List.filter_sublist
  have le := sub.length_le
  have neq : (refinePairs G pairs).length ≠ pairs.length := fun he => h (sub.eq_of_length he)
  omega

noncomputable def stabilize {S A} (G : Game S A) : Nat → List (S × S) → List (S × S)
  | 0, pairs => pairs
  | n + 1, pairs => by
    classical
    exact if refinePairs G pairs = pairs then pairs else stabilize G n (refinePairs G pairs)

theorem stabilized_subset {S A} (G : Game S A) (n : Nat) (pairs : List (S × S)) :
    ∀ x y, (x, y) ∈ stabilize G n pairs → (x, y) ∈ pairs := by
  classical
  induction n generalizing pairs with
  | zero => exact fun _ _ h => h
  | succ n ih =>
    simp only [stabilize]
    split
    · exact fun _ _ h => h
    · exact fun x y h => ((mem_refinePairs G pairs x y).mp (ih _ x y h)).1

theorem stabilization_is_fixed {S A} (G : Game S A) (n : Nat)
    (pairs : List (S × S)) (bound : pairs.length ≤ n) :
    refinePairs G (stabilize G n pairs) = stabilize G n pairs := by
  classical
  induction n generalizing pairs with
  | zero =>
    have empty : pairs = [] := List.length_eq_zero_iff.mp (by omega)
    subst pairs
    simp [stabilize, refinePairs]
  | succ n ih =>
    simp only [stabilize]
    split
    · assumption
    · have lt := strict_refinement_decreases_length G pairs (by assumption)
      exact ih _ (by omega)

theorem stable_refinement_retained {S A} (G : Game S A) (R : S → S → Prop)
    (stable : ∀ x y, R x y → Compatible G R x y)
    (n : Nat) (pairs : List (S × S))
    (included : ∀ x y, R x y → (x, y) ∈ pairs) :
    ∀ x y, R x y → (x, y) ∈ stabilize G n pairs := by
  classical
  induction n generalizing pairs with
  | zero => exact included
  | succ n ih =>
    simp only [stabilize]
    split
    · exact included
    · apply ih
      intro x y hR
      exact (mem_refinePairs G pairs x y).mpr
        ⟨included x y hR, compatible_mono G included (stable x y hR)⟩

theorem coarsest_stable_relation {S A} (G : Game S A) (pairs : List (S × S)) :
    let result := stabilize G pairs.length pairs
    (∀ x y, (x, y) ∈ result → (x, y) ∈ pairs) ∧
    (∀ x y, (x, y) ∈ result → Compatible G (fun z t => (z, t) ∈ result) x y) ∧
    (∀ R : S → S → Prop, (∀ x y, R x y → (x, y) ∈ pairs) →
      (∀ x y, R x y → Compatible G R x y) → ∀ x y, R x y → (x, y) ∈ result) := by
  dsimp
  refine ⟨stabilized_subset G _ pairs, ?_, ?_⟩
  · intro x y h
    have fixed := stabilization_is_fixed G pairs.length pairs (Nat.le_refl _)
    have hr : (x, y) ∈ refinePairs G (stabilize G pairs.length pairs) := fixed.symm ▸ h
    exact ((mem_refinePairs G _ x y).mp hr).2
  · intro R included stable
    exact stable_refinement_retained G R stable pairs.length pairs included

theorem compatible_reflexive {S A} (G : Game S A) (x : S) :
    Compatible G (fun z t => z = t) x x := by
  refine ⟨Iff.rfl, ?_⟩
  intro a
  exact ⟨Iff.rfl, fun _ => ⟨rfl, fun z hz => ⟨z, hz, rfl⟩,
    fun t ht => ⟨t, ht, rfl⟩⟩⟩

theorem compatible_converse {S A} (G : Game S A) {R : S → S → Prop}
    {x y : S} (h : Compatible G R x y) :
    Compatible G (fun z t => R t z) y x := by
  refine ⟨h.1.symm, ?_⟩
  intro a
  refine ⟨(h.2 a).1.symm, ?_⟩
  intro ha
  obtain ⟨hc, hf, hb⟩ := (h.2 a).2 ((h.2 a).1.mpr ha)
  exact ⟨hc.symm, hb, hf⟩

theorem compatible_composition {S A} (G : Game S A) {R U : S → S → Prop}
    {x y z : S} (hxy : Compatible G R x y) (hyz : Compatible G U y z) :
    Compatible G (fun p q => ∃ m, R p m ∧ U m q) x z := by
  refine ⟨hxy.1.trans hyz.1, ?_⟩
  intro a
  refine ⟨(hxy.2 a).1.trans (hyz.2 a).1, ?_⟩
  intro ha
  obtain ⟨hcx, hfx, hbx⟩ := (hxy.2 a).2 ha
  obtain ⟨hcy, hfy, hby⟩ := (hyz.2 a).2 ((hxy.2 a).1.mp ha)
  refine ⟨hcx.trans hcy, ?_, ?_⟩
  · intro p hp
    obtain ⟨m, hm, hR⟩ := hfx p hp
    obtain ⟨q, hq, hU⟩ := hfy m hm
    exact ⟨q, hq, m, hR, hU⟩
  · intro q hq
    obtain ⟨m, hm, hU⟩ := hby q hq
    obtain ⟨p, hp, hR⟩ := hbx m hm
    exact ⟨p, hp, m, hR, hU⟩

theorem stable_seed_equivalence {S A} (G : Game S A) (pairs : List (S × S))
    (refl : ∀ x, (x, x) ∈ pairs)
    (symm : ∀ x y, (x, y) ∈ pairs → (y, x) ∈ pairs)
    (trans : ∀ x y z, (x, y) ∈ pairs → (y, z) ∈ pairs → (x, z) ∈ pairs) :
    let R := fun x y => (x, y) ∈ stabilize G pairs.length pairs
    (∀ x, R x x) ∧ (∀ x y, R x y → R y x) ∧
      (∀ x y z, R x y → R y z → R x z) := by
  dsimp
  obtain ⟨included, stable, greatest⟩ := coarsest_stable_relation G pairs
  let R := fun x y => (x, y) ∈ stabilize G pairs.length pairs
  refine ⟨?_, ?_, ?_⟩
  · intro x
    apply greatest (fun z t => z = t) (fun z t h => h ▸ refl z) _ x x rfl
    intro z t h
    subst t
    exact compatible_reflexive G z
  · have rev_included : ∀ x y, R y x → (x, y) ∈ pairs :=
      fun x y h => symm y x (included y x h)
    have rev_stable : ∀ x y, R y x → Compatible G (fun z t => R t z) x y :=
      fun x y h => compatible_converse G (stable y x h)
    intro x y h
    exact greatest (fun z t => R t z) rev_included rev_stable y x h
  · have comp_included : ∀ x z, (∃ y, R x y ∧ R y z) → (x, z) ∈ pairs := by
      rintro x z ⟨y, hxy, hyz⟩
      exact trans x y z (included x y hxy) (included y z hyz)
    have comp_stable : ∀ x z, (∃ y, R x y ∧ R y z) →
        Compatible G (fun p q => ∃ m, R p m ∧ R m q) x z := by
      rintro x z ⟨y, hxy, hyz⟩
      exact compatible_composition G (stable x y hxy) (stable y z hyz)
    intro x y z hxy hyz
    exact greatest (fun p q => ∃ m, R p m ∧ R m q) comp_included comp_stable
      x z ⟨y, hxy, hyz⟩

end WitnessedDifference.BeliefGameQuotient

#print axioms WitnessedDifference.BeliefGameQuotient.reach_transport
#print axioms WitnessedDifference.BeliefGameQuotient.winning_transport
#print axioms WitnessedDifference.BeliefGameQuotient.budget_transport
#print axioms WitnessedDifference.BeliefGameQuotient.achievable_budgets_equal
#print axioms WitnessedDifference.BeliefGameQuotient.optional_actions_preserve_budget
#print axioms WitnessedDifference.BeliefGameQuotient.compatible_mono
#print axioms WitnessedDifference.BeliefGameQuotient.mem_refinePairs
#print axioms WitnessedDifference.BeliefGameQuotient.strict_refinement_decreases_length
#print axioms WitnessedDifference.BeliefGameQuotient.stabilized_subset
#print axioms WitnessedDifference.BeliefGameQuotient.stabilization_is_fixed
#print axioms WitnessedDifference.BeliefGameQuotient.stable_refinement_retained
#print axioms WitnessedDifference.BeliefGameQuotient.coarsest_stable_relation
#print axioms WitnessedDifference.BeliefGameQuotient.compatible_reflexive
#print axioms WitnessedDifference.BeliefGameQuotient.compatible_converse
#print axioms WitnessedDifference.BeliefGameQuotient.compatible_composition
#print axioms WitnessedDifference.BeliefGameQuotient.stable_seed_equivalence
