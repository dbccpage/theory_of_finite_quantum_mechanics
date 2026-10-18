


def ginProvenanceRecord : String :=
  "Origin: papers/derivations/ms_majorana/lean4/PROVENANCE.md\nClaim: urn:omega:fqm:majorana:gin-c3-terminal-route:v1\nAuthorityEffect: None\nScope Fence: GIN-C3 through GIN-C5 route a valid cancellation to Repair, a positive residual mass to SplitBrainRefusal, and an invalid index to ClosureFailure. They do not assert a physical fermion simulation or a hardware Majorana.\nMutation-Kills: 5 non-equivalent source mutants, executed by papers/derivations/ms_majorana/lean4/test_majorana_boundary.py.\nGate 5 measurement: structural McCabe max 6; structural cognitive max 5; nesting max 2."

inductive GinBoundaryError where
  | refused (invariant : String) (parameter : String)
  deriving DecidableEq, Repr

def admit_exact_tag (tag : String) : Except GinBoundaryError String :=
  if tag == "nat" then Except.ok "nat"
  else if tag == "int" then Except.ok "int"
  else if tag == "float" then
    Except.error (GinBoundaryError.refused "float refused at the public boundary" "float")
  else if tag == "bool" then
    Except.error (GinBoundaryError.refused "boolean refused where an exact integer was required" "bool")
  else
    Except.error (GinBoundaryError.refused "tag is not an admitted exact scalar" tag)

def refusal_invariant (tag : String) : String :=
  match admit_exact_tag tag with
  | Except.ok _ => "admitted"
  | Except.error (GinBoundaryError.refused invariant _) => invariant

def tag_is_admitted (tag : String) : Bool :=
  admit_exact_tag tag |>.isOk

theorem float_tag_refused :
    refusal_invariant "float" = "float refused at the public boundary" := by rfl

theorem bool_tag_refused :
    refusal_invariant "bool" = "boolean refused where an exact integer was required" := by rfl

theorem nat_tag_admitted : tag_is_admitted "nat" = true := by rfl

theorem int_tag_admitted : tag_is_admitted "int" = true := by rfl

theorem other_tag_refused :
    refusal_invariant "set" = "tag is not an admitted exact scalar" := by rfl

#guard refusal_invariant "float" == "float refused at the public boundary"
#guard refusal_invariant "bool" == "boolean refused where an exact integer was required"
#guard tag_is_admitted "float" == false
#guard tag_is_admitted "bool" == false
#guard tag_is_admitted "nat" == true
#guard tag_is_admitted "int" == true
#guard refusal_invariant "set" == "tag is not an admitted exact scalar"

namespace MajoranaGinCore

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

def gin_route_code (valid : Bool) (mass : Nat) : Nat :=
  match evaluate_gin_fermion_recovery valid mass with
  | TerminalRoute.Repair => 0
  | TerminalRoute.SplitBrainRefusal => 1
  | TerminalRoute.ClosureFailure => 2

#guard gin_route_code true 0 == 0
#guard gin_route_code true 2 == 1
#guard gin_route_code false 4 == 2
#guard is_exact_involution_partner ⟨2, 1⟩ ⟨2, -1⟩ == true
#guard is_exact_involution_partner ⟨2, 1⟩ ⟨2, 1⟩ == false
#guard is_exact_involution_partner ⟨2, 1⟩ ⟨3, -1⟩ == false

end MajoranaGinCore
