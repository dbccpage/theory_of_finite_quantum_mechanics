import Init.Data.Rat
import Init.Grind.Ordered.Rat
import Lean

/-!
# Checked finite progress, losing traps, and rational optimality

This is a mathematical game model, not verification of the Python program.
Successor lists are finite and nonempty for enabled actions. The abstract
results do not assume an independently sound interpretation of target truth.
Finite-state stabilization and the producer's horizon construction are outside
this module. The kernel results below prove the certificate laws.
-/
namespace WitnessedDifference.CertifiedProgress

universe u v

structure Game (State : Type u) (Action : Type v) where
  target : State → Prop
  enabled : State → Action → Prop
  successors : State → Action → List State
  cost : State → Action → Rat
  nonempty : ∀ x a, enabled x a → ∃ y, y ∈ successors x a
  positive : ∀ x a, enabled x a → 0 < cost x a

def Reach {S A} (G : Game S A) : Nat → S → Prop
  | 0, x => G.target x
  | n + 1, x => G.target x ∨ ∃ a, G.enabled x a ∧
      ∀ y, y ∈ G.successors x a → Reach G n y

def Winning {S A} (G : Game S A) (x : S) : Prop := ∃ n, Reach G n x

theorem reach_target {S A} (G : Game S A) (n : Nat) (x : S) (h : G.target x) :
    Reach G n x := by
  cases n with
  | zero => exact h
  | succ n => exact Or.inl h

theorem reach_step {S A} (G : Game S A) (n : Nat) (x : S)
    (h : Reach G n x) : Reach G (n + 1) x := by
  induction n generalizing x with
  | zero => exact Or.inl h
  | succ n ih =>
    rcases h with ht | ⟨a, ha, hs⟩
    · exact Or.inl ht
    · exact Or.inr ⟨a, ha, fun y hy => ih y (hs y hy)⟩

theorem reach_mono {S A} (G : Game S A) {n m : Nat} (h : n ≤ m)
    (x : S) (hx : Reach G n x) : Reach G m x := by
  induction h with
  | refl => exact hx
  | step h ih => exact reach_step G _ x ih

theorem finite_successor_bound {S A} (G : Game S A) (xs : List S)
    (h : ∀ x, x ∈ xs → Winning G x) : ∃ n, ∀ x, x ∈ xs → Reach G n x := by
  induction xs with
  | nil => exact ⟨0, by simp⟩
  | cons x xs ih =>
    obtain ⟨n, hn⟩ := h x (by simp)
    obtain ⟨m, hm⟩ := ih (fun y hy => h y (by simp [hy]))
    refine ⟨n + m, ?_⟩
    intro y hy
    rcases List.mem_cons.mp hy with rfl | hy
    · exact reach_mono G (by omega) y hn
    · exact reach_mono G (by omega) y (hm y hy)

theorem winning_fixed_point {S A} (G : Game S A) (x : S) :
    Winning G x ↔ G.target x ∨ ∃ a, G.enabled x a ∧
      ∀ y, y ∈ G.successors x a → Winning G y := by
  constructor
  · rintro ⟨n, hn⟩
    cases n with
    | zero => exact Or.inl hn
    | succ n =>
      rcases hn with ht | ⟨a, ha, hs⟩
      · exact Or.inl ht
      · exact Or.inr ⟨a, ha, fun y hy => ⟨n, hs y hy⟩⟩
  · rintro (ht | ⟨a, ha, hs⟩)
    · exact ⟨0, ht⟩
    · obtain ⟨n, hn⟩ := finite_successor_bound G (G.successors x a) hs
      exact ⟨n + 1, Or.inr ⟨a, ha, hn⟩⟩

theorem least_closed_region {S A} (G : Game S A) (W : S → Prop)
    (targets : ∀ x, G.target x → W x)
    (predecessor : ∀ x a, G.enabled x a →
      (∀ y, y ∈ G.successors x a → W y) → W x) :
    ∀ x, Winning G x → W x := by
  intro x ⟨n, hn⟩
  induction n generalizing x with
  | zero => exact targets x hn
  | succ n ih =>
    rcases hn with ht | ⟨a, ha, hs⟩
    · exact targets x ht
    · exact predecessor x a ha (fun y hy => ih y (hs y hy))

structure Trap {S A} (G : Game S A) (L : S → Prop) : Prop where
  no_target : ∀ x, L x → ¬G.target x
  closure : ∀ x, L x → ∀ a, G.enabled x a →
    ∃ y, y ∈ G.successors x a ∧ L y

theorem trap_excludes_reach {S A} (G : Game S A) {L : S → Prop}
    (trap : Trap G L) (n : Nat) : ∀ x, L x → ¬Reach G n x := by
  induction n with
  | zero => exact trap.no_target
  | succ n ih =>
    intro x hx h
    rcases h with ht | ⟨a, ha, hs⟩
    · exact trap.no_target x hx ht
    · obtain ⟨y, hy, hL⟩ := trap.closure x hx a ha
      exact ih y hL (hs y hy)

theorem trap_excludes_winning {S A} (G : Game S A) {L : S → Prop}
    (trap : Trap G L) (x : S) (hx : L x) : ¬Winning G x := by
  rintro ⟨n, hn⟩
  exact trap_excludes_reach G trap n x hx hn

theorem losing_complement_is_trap {S A} (G : Game S A) :
    Trap G (fun x => ¬Winning G x) := by
  classical
  constructor
  · intro x hx ht
    exact hx ⟨0, ht⟩
  · intro x hx a ha
    apply Classical.byContradiction
    intro no_escape
    apply hx
    apply (winning_fixed_point G x).mpr
    right
    refine ⟨a, ha, ?_⟩
    intro y hy
    apply Classical.byContradiction
    intro not_winning
    exact no_escape ⟨y, hy, not_winning⟩

theorem loss_iff_trap_at_initial {S A} (G : Game S A) (x : S) :
    ¬Winning G x ↔ ∃ L, L x ∧ Trap G L := by
  constructor
  · intro hx
    exact ⟨fun y => ¬Winning G y, hx, losing_complement_is_trap G⟩
  · rintro ⟨L, hx, trap⟩
    exact trap_excludes_winning G trap x hx

theorem dead_end_is_losing_only_when_not_target {S A} (G : Game S A) (x : S)
    (not_target : ¬G.target x) (empty : ∀ a, ¬G.enabled x a) : ¬Winning G x := by
  apply trap_excludes_winning G (L := fun y => y = x) ?_ x rfl
  constructor
  · intro y hy
    simpa [hy] using not_target
  · intro y hy a ha
    exact False.elim (empty a (by simpa [hy] using ha))

structure Ranked {S A} (G : Game S A) (W : S → Prop) where
  rank : S → Nat
  terminal : ∀ x, G.target x → rank x = 0
  move : ∀ x, W x → ¬G.target x → ∃ a, G.enabled x a ∧
    ∀ y, y ∈ G.successors x a → W y ∧ rank y < rank x

theorem rank_certificate_sound {S A} (G : Game S A) {W : S → Prop}
    (cert : Ranked G W) : ∀ x, W x → Reach G (cert.rank x) x := by
  have bounded : ∀ n x, W x → cert.rank x ≤ n → Reach G n x := by
    intro n
    induction n with
    | zero =>
      intro x hx hr
      by_cases ht : G.target x
      · exact ht
      · obtain ⟨a, ha, hs⟩ := cert.move x hx ht
        obtain ⟨y, hy⟩ := G.nonempty x a ha
        have hlt := (hs y hy).2
        omega
    | succ n ih =>
      intro x hx hr
      by_cases ht : G.target x
      · exact Or.inl ht
      · obtain ⟨a, ha, hs⟩ := cert.move x hx ht
        refine Or.inr ⟨a, ha, ?_⟩
        intro y hy
        have hlt := (hs y hy).2
        exact ih y (hs y hy).1 (by omega)
  intro x hx
  exact bounded (cert.rank x) x hx (Nat.le_refl _)

theorem checked_partition_characterizes_winning {S A} (G : Game S A)
    {W L : S → Prop} (cert : Ranked G W) (trap : Trap G L)
    (cover : ∀ x, W x ∨ L x) (x : S) : Winning G x ↔ W x := by
  constructor
  · intro h
    rcases cover x with hw | hl
    · exact hw
    · exact False.elim (trap_excludes_winning G trap x hl h)
  · intro hw
    exact ⟨cert.rank x, rank_certificate_sound G cert x hw⟩

def BudgetReach {S A} (G : Game S A) : Nat → Rat → S → Prop
  | 0, budget, x => G.target x ∧ 0 ≤ budget
  | n + 1, budget, x => (G.target x ∧ 0 ≤ budget) ∨
      ∃ a, G.enabled x a ∧ G.cost x a ≤ budget ∧
        ∀ y, y ∈ G.successors x a → BudgetReach G n (budget - G.cost x a) y

theorem budget_forgets_cost {S A} (G : Game S A) (n : Nat) (budget : Rat) (x : S)
    (h : BudgetReach G n budget x) : Reach G n x := by
  induction n generalizing budget x with
  | zero => exact h.1
  | succ n ih =>
    rcases h with ht | ⟨a, ha, _, hs⟩
    · exact Or.inl ht.1
    · exact Or.inr ⟨a, ha, fun y hy => ih _ y (hs y hy)⟩

theorem budget_mono {S A} (G : Game S A) (n : Nat) {low high : Rat}
    (le : low ≤ high) (x : S) (h : BudgetReach G n low x) :
    BudgetReach G n high x := by
  induction n generalizing low high x with
  | zero => exact ⟨h.1, Rat.le_trans h.2 le⟩
  | succ n ih =>
    rcases h with ht | ⟨a, ha, hc, hs⟩
    · exact Or.inl ⟨ht.1, Rat.le_trans ht.2 le⟩
    · refine Or.inr ⟨a, ha, Rat.le_trans hc le, ?_⟩
      intro y hy
      exact ih (by grind) y (hs y hy)

structure OptimalCertificate {S A} (G : Game S A) where
  W : S → Prop
  L : S → Prop
  cover : ∀ x, W x ∨ L x
  losing : Trap G L
  rank : S → Nat
  value : S → Rat
  terminal_rank : ∀ x, G.target x → rank x = 0
  terminal_value : ∀ x, G.target x → value x = 0
  nonnegative : ∀ x, W x → 0 ≤ value x
  upper : ∀ x, W x → ¬G.target x → ∃ a, G.enabled x a ∧
    ∀ y, y ∈ G.successors x a →
      W y ∧ rank y < rank x ∧ G.cost x a + value y ≤ value x
  lower : ∀ x, W x → ¬G.target x → ∀ a, G.enabled x a →
    ∃ y, y ∈ G.successors x a ∧
      (L y ∨ (W y ∧ value x ≤ G.cost x a + value y))

def OptimalCertificate.ranked {S A} {G : Game S A} (cert : OptimalCertificate G) :
    Ranked G cert.W where
  rank := cert.rank
  terminal := cert.terminal_rank
  move := by
    intro x hx ht
    obtain ⟨a, ha, hs⟩ := cert.upper x hx ht
    exact ⟨a, ha, fun y hy => ⟨(hs y hy).1, (hs y hy).2.1⟩⟩

theorem optimal_upper_budget {S A} (G : Game S A) (cert : OptimalCertificate G) :
    ∀ x, cert.W x → BudgetReach G (cert.rank x) (cert.value x) x := by
  have bounded : ∀ n x, cert.W x → cert.rank x ≤ n →
      BudgetReach G n (cert.value x) x := by
    intro n
    induction n with
    | zero =>
      intro x hx hr
      by_cases ht : G.target x
      · exact ⟨ht, cert.nonnegative x hx⟩
      · obtain ⟨a, ha, hs⟩ := cert.upper x hx ht
        obtain ⟨y, hy⟩ := G.nonempty x a ha
        have hlt := (hs y hy).2.1
        omega
    | succ n ih =>
      intro x hx hr
      by_cases ht : G.target x
      · exact Or.inl ⟨ht, cert.nonnegative x hx⟩
      · obtain ⟨a, ha, hs⟩ := cert.upper x hx ht
        obtain ⟨z, hz⟩ := G.nonempty x a ha
        have hUpper := (hs z hz).2.2
        have hNonneg := cert.nonnegative z (hs z hz).1
        refine Or.inr ⟨a, ha, by grind, ?_⟩
        intro y hy
        have hlt := (hs y hy).2.1
        have hcost := (hs y hy).2.2
        exact budget_mono G n (by grind) y (ih y (hs y hy).1 (by omega))
  intro x hx
  exact bounded (cert.rank x) x hx (Nat.le_refl _)

theorem optimal_lower_budget {S A} (G : Game S A) (cert : OptimalCertificate G)
    (n : Nat) (budget : Rat) (x : S) (hx : cert.W x)
    (h : BudgetReach G n budget x) : cert.value x ≤ budget := by
  induction n generalizing budget x with
  | zero =>
    rw [cert.terminal_value x h.1]
    exact h.2
  | succ n ih =>
    by_cases ht : G.target x
    · rw [cert.terminal_value x ht]
      rcases h with hgoal | ⟨a, ha, hc, _⟩
      · exact hgoal.2
      · have hp := G.positive x a ha
        grind
    · rcases h with hgoal | ⟨a, ha, _, hs⟩
      · exact False.elim (ht hgoal.1)
      · obtain ⟨y, hy, hl | ⟨hw, hcost⟩⟩ := cert.lower x hx ht a ha
        · exact False.elim (trap_excludes_reach G cert.losing n y hl
            (budget_forgets_cost G n _ y (hs y hy)))
        · have hbound := ih _ y hw (hs y hy)
          grind

theorem certificate_exact_optimality {S A} (G : Game S A) (cert : OptimalCertificate G)
    (x : S) (hx : cert.W x) :
    (∃ n, BudgetReach G n (cert.value x) x) ∧
    ∀ n budget, BudgetReach G n budget x → cert.value x ≤ budget := by
  exact ⟨⟨cert.rank x, optimal_upper_budget G cert x hx⟩,
         fun n budget h => optimal_lower_budget G cert n budget x hx h⟩

theorem successful_terminal_cannot_be_stalled_loss {S A} (G : Game S A)
    {L : S → Prop} (trap : Trap G L) (x : S) (ht : G.target x) : ¬L x := by
  intro hL
  exact trap.no_target x hL ht

theorem positive_upper_step_decreases_value {S A} (G : Game S A)
    (cert : OptimalCertificate G) (x : S) (hx : cert.W x) (ht : ¬G.target x) :
    ∃ a, G.enabled x a ∧ ∀ y, y ∈ G.successors x a → cert.value y < cert.value x := by
  obtain ⟨a, ha, hs⟩ := cert.upper x hx ht
  refine ⟨a, ha, ?_⟩
  intro y hy
  have hpos := G.positive x a ha
  have hbound := (hs y hy).2.2
  grind

theorem terminal_boundary_blocks_constant_shift :
    (101 : Rat) = 1 + 100 ∧ (100 : Rat) ≠ 0 := by grind

theorem operating_savings_do_not_imply_setup_payback :
    (0 : Rat) < 5 - 2 ∧ ¬((4 : Rat) < 5 - 2) := by grind

end WitnessedDifference.CertifiedProgress

#print axioms WitnessedDifference.CertifiedProgress.reach_target
#print axioms WitnessedDifference.CertifiedProgress.reach_step
#print axioms WitnessedDifference.CertifiedProgress.reach_mono
#print axioms WitnessedDifference.CertifiedProgress.finite_successor_bound
#print axioms WitnessedDifference.CertifiedProgress.winning_fixed_point
#print axioms WitnessedDifference.CertifiedProgress.least_closed_region
#print axioms WitnessedDifference.CertifiedProgress.trap_excludes_reach
#print axioms WitnessedDifference.CertifiedProgress.trap_excludes_winning
#print axioms WitnessedDifference.CertifiedProgress.losing_complement_is_trap
#print axioms WitnessedDifference.CertifiedProgress.loss_iff_trap_at_initial
#print axioms WitnessedDifference.CertifiedProgress.dead_end_is_losing_only_when_not_target
#print axioms WitnessedDifference.CertifiedProgress.rank_certificate_sound
#print axioms WitnessedDifference.CertifiedProgress.checked_partition_characterizes_winning
#print axioms WitnessedDifference.CertifiedProgress.budget_forgets_cost
#print axioms WitnessedDifference.CertifiedProgress.budget_mono
#print axioms WitnessedDifference.CertifiedProgress.OptimalCertificate.ranked
#print axioms WitnessedDifference.CertifiedProgress.optimal_upper_budget
#print axioms WitnessedDifference.CertifiedProgress.optimal_lower_budget
#print axioms WitnessedDifference.CertifiedProgress.certificate_exact_optimality
#print axioms WitnessedDifference.CertifiedProgress.successful_terminal_cannot_be_stalled_loss
#print axioms WitnessedDifference.CertifiedProgress.positive_upper_step_decreases_value
#print axioms WitnessedDifference.CertifiedProgress.terminal_boundary_blocks_constant_shift
#print axioms WitnessedDifference.CertifiedProgress.operating_savings_do_not_imply_setup_payback
