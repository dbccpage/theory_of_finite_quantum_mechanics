import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Worklist closure/soundness, adjacent-word inventory,
bounded charge and exact replay. Rust mode-specific certified edges, immutable
finite machine, BFS order, scratch/Rc and provider refinement are separate. -/
namespace TFQM.FiniteTrace

variable {V I C : Type}

inductive Reachable (edge : V → V → Prop) (root : V) : V → Prop where
  | start : Reachable edge root root
  | step {x y : V} : Reachable edge root x → edge x y → Reachable edge root y

theorem initial_sound (edge : V → V → Prop) (root x : V) (h : x = root) :
    Reachable edge root x := by subst x; exact .start

theorem fresh_sound (edge : V → V → Prop) (root parent fresh : V)
    (sound : Reachable edge root parent) (neighbor : edge parent fresh) :
    Reachable edge root fresh := .step sound neighbor

theorem insert_sound (edge : V → V → Prop) (root parent fresh : V) (seen : V → Prop)
    (sound : ∀ x, seen x → Reachable edge root x) (parentSeen : seen parent)
    (neighbor : edge parent fresh) :
    ∀ x, (seen x ∨ x = fresh) → Reachable edge root x := by
  intro x hx
  rcases hx with hx | rfl
  · exact sound x hx
  · exact .step (sound parent parentSeen) neighbor

theorem closed_contains_reachable (edge : V → V → Prop) (root : V) (seen : V → Prop)
    (rootSeen : seen root) (closed : ∀ x, seen x → ∀ y, edge x y → seen y)
    (x : V) (reachable : Reachable edge root x) : seen x := by
  induction reachable with
  | start => exact rootSeen
  | step _ neighbor ih => exact closed _ ih _ neighbor

theorem empty_frontier_closed (edge : V → V → Prop) (seen pending : V → Prop)
    (cover : ∀ x, seen x → pending x ∨ ∀ y, edge x y → seen y)
    (empty : ∀ x, ¬ pending x) : ∀ x, seen x → ∀ y, edge x y → seen y := by
  intro x hx
  rcases cover x hx with hp | hc
  · exact False.elim (empty x hp)
  · exact hc

theorem complete_component (edge : V → V → Prop) (root : V) (seen pending : V → Prop)
    (rootSeen : seen root) (sound : ∀ x, seen x → Reachable edge root x)
    (cover : ∀ x, seen x → pending x ∨ ∀ y, edge x y → seen y)
    (empty : ∀ x, ¬ pending x) : ∀ x, seen x ↔ Reachable edge root x := by
  intro x
  exact ⟨sound x, closed_contains_reachable edge root seen rootSeen
    (empty_frontier_closed edge seen pending cover empty) x⟩

theorem existing_self_edge (seen : V → Prop) (x : V) (hx : seen x) : seen x := hx

theorem adjacent_length (headWord tailWord : List I) (a b : I) :
    (headWord ++ a :: b :: tailWord).length = (headWord ++ b :: a :: tailWord).length := by simp

theorem adjacent_inventory [DecidableEq I] (headWord tailWord : List I) (a b c : I) :
    List.count c (headWord ++ a :: b :: tailWord) = List.count c (headWord ++ b :: a :: tailWord) := by
  simp only [List.count_append, List.count_cons]
  omega

def charge (checks limit : Nat) : Option Nat :=
  if checks < limit then some (checks + 1) else none

theorem charge_success (checks limit : Nat) (h : checks < limit) :
    charge checks limit = some (checks + 1) := by simp [charge, h]

theorem charge_refusal (checks limit : Nat) (h : limit ≤ checks) :
    charge checks limit = none := by simp [charge, Nat.not_lt.mpr h]

theorem charge_bounded (checks limit : Nat) (h : checks < limit) : checks + 1 ≤ limit := by omega

theorem charge_strict (checks : Nat) : checks < checks + 1 := by omega

theorem machine_increment_fits (checks limit maximum : Nat) (h : checks < limit)
    (bounded : limit ≤ maximum) : checks + 1 ≤ maximum := by omega

def replay [DecidableEq C] (expected supplied : C) : Bool := decide (expected = supplied)
theorem replay_complete [DecidableEq C] (expected supplied : C) :
    replay expected supplied = true ↔ expected = supplied := by simp [replay]

theorem replay_refuses_missing [DecidableEq C] (expected supplied : C) (ne : expected ≠ supplied) :
    replay expected supplied = false := by simp [replay, ne]

end TFQM.FiniteTrace

#print axioms TFQM.FiniteTrace.initial_sound
#print axioms TFQM.FiniteTrace.fresh_sound
#print axioms TFQM.FiniteTrace.insert_sound
#print axioms TFQM.FiniteTrace.closed_contains_reachable
#print axioms TFQM.FiniteTrace.empty_frontier_closed
#print axioms TFQM.FiniteTrace.complete_component
#print axioms TFQM.FiniteTrace.existing_self_edge
#print axioms TFQM.FiniteTrace.adjacent_length
#print axioms TFQM.FiniteTrace.adjacent_inventory
#print axioms TFQM.FiniteTrace.charge_success
#print axioms TFQM.FiniteTrace.charge_refusal
#print axioms TFQM.FiniteTrace.charge_bounded
#print axioms TFQM.FiniteTrace.charge_strict
#print axioms TFQM.FiniteTrace.machine_increment_fits
#print axioms TFQM.FiniteTrace.replay_complete
#print axioms TFQM.FiniteTrace.replay_refuses_missing
