


namespace FermionGinCore

structure SignedWeight where
  weight : Nat
  sign : Int
deriving Repr, DecidableEq

def is_exact_involution_partner (c1 c2 : SignedWeight) : Bool :=
  c1.weight == c2.weight ∧ c1.sign + c2.sign == 0

theorem involution_pair_cancels_sign (w : Nat) (s1 s2 : Int)
    (h_sign : s1 + s2 = 0) :
    (w : Int) * s1 + (w : Int) * s2 = 0 := by
  have h_distrib : (w : Int) * s1 + (w : Int) * s2 = (w : Int) * (s1 + s2) := by
    rw [← Int.mul_add]
  rw [h_distrib, h_sign, Int.mul_zero]

abbrev MajoranaIndex := Nat

structure MajoranaBond where
  u : MajoranaIndex
  v : MajoranaIndex
deriving Repr, DecidableEq

def is_bulk_kitaev_bond (L : Nat) (u v : Nat) : Prop :=
  ∃ j : Nat, 1 ≤ j ∧ j < L ∧ u = j + j ∧ v = j + j + 1

theorem edge_mode_1_not_in_bulk (L : Nat) (u v : Nat)
    (h_bulk : is_bulk_kitaev_bond L u v) :
    u ≠ 1 ∧ v ≠ 1 := by
  rcases h_bulk with ⟨j, hj1, _, rfl, rfl⟩
  constructor
  · intro h
    omega
  · intro h
    omega

theorem edge_mode_2L_not_in_bulk (L : Nat) (u v : Nat)
    (h_bulk : is_bulk_kitaev_bond L u v) :
    u ≠ L + L ∧ v ≠ L + L := by
  rcases h_bulk with ⟨j, _, hjL, rfl, rfl⟩
  constructor
  · intro h
    omega
  · intro h
    omega

inductive TerminalRoute : Type
  | Repair
  | SplitBrainRefusal
  | ClosureFailure
deriving Repr, DecidableEq

def evaluate_gin_fermion_recovery
    (is_valid_index : Bool)
    (uncancelled_sign_mass : Nat) : TerminalRoute :=
  if ¬is_valid_index then
    TerminalRoute.ClosureFailure
  else if uncancelled_sign_mass == 0 then
    TerminalRoute.Repair
  else
    TerminalRoute.SplitBrainRefusal

theorem exact_gin_cancellation_routes_to_repair :
    evaluate_gin_fermion_recovery true 0 = TerminalRoute.Repair := by
  rfl

theorem residual_sign_routes_to_refusal (mass : Nat) (h : mass > 0) :
    evaluate_gin_fermion_recovery true mass = TerminalRoute.SplitBrainRefusal := by
  unfold evaluate_gin_fermion_recovery
  have h_ne : (mass == 0) = false := by
    simp [Nat.ne_of_gt h]
  simp [h_ne]

theorem invalid_gin_routes_to_closure_failure (mass : Nat) :
    evaluate_gin_fermion_recovery false mass = TerminalRoute.ClosureFailure := by
  rfl

end FermionGinCore
