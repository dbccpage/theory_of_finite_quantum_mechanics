/-!
  MajoranaGinCore.lean — Generalized Inverted Index (GIN) Cochains for the Fermion Sign Problem
  and Majorana Zero Mode Boundaries

  AuthorityEffect: None
  Primary Reference: sealed-derivation-v1 (commit 3100c4e)
  Companion Contracts: nf.change.bqnf.yaml, fermion_sign_problem.md

  Formalizes:
  1. Involution sign cancellation: w_+ * (+1) + w_- * (-1) = 0 under GIN-indexed weight equality w_+ = w_-.
  2. Majorana Zero Mode (MZM) boundary decoupling: edge modes γ_1 and γ_{2L} are strictly disjoint from bulk pairing bonds.
  3. BQNF Terminal Routing for fermionic GIN cochains (Repair, SplitBrainRefusal, ClosureFailure).
-/

def ginProvenanceRecord : String :=
  "Origin: papers/derivations/ms_majorana/lean4/provenance.md\nClaim: urn:omega:fqm:majorana:gin-c3-terminal-route:v1\nAuthorityEffect: None\nMutation-Kills: 5 non-equivalent source mutants, executed by papers/derivations/ms_majorana/lean4/test_majorana_boundary.py.\n"

namespace MajoranaGinCore

/-- Representation of a signed configuration weight -/
structure SignedWeight where
  weight : Nat
  sign : Int -- +1 or -1
deriving Repr, DecidableEq

/-- Condition for exact sign-reversing involution partner -/
def is_exact_involution_partner (c1 c2 : SignedWeight) : Bool :=
  c1.weight == c2.weight ∧ c1.sign + c2.sign == 0

/-- THEOREM: Exactly paired configurations cancel in signed summation -/
theorem involution_pair_cancels_sign (w : Nat) (s1 s2 : Int)
    (h_sign : s1 + s2 = 0) :
    (w : Int) * s1 + (w : Int) * s2 = 0 := by
  have h_distrib : (w : Int) * s1 + (w : Int) * s2 = (w : Int) * (s1 + s2) := by
    rw [← Int.mul_add]
  rw [h_distrib, h_sign, Int.mul_zero]

/-- Majorana operator index in a 1D chain of length L (1 <= k <= 2L) -/
abbrev MajoranaIndex := Nat

/-- Bulk Majorana pairing bond (γ_u, γ_v) -/
structure MajoranaBond where
  u : MajoranaIndex
  v : MajoranaIndex
deriving Repr, DecidableEq

/-- The canonical sweet-spot Kitaev bulk bonds for chain of length L:
    bonds = {(2j, 2j+1) | 1 <= j < L}, expressed linearly as j + j and j + j + 1 -/
def is_bulk_kitaev_bond (L : Nat) (u v : Nat) : Prop :=
  ∃ j : Nat, 1 ≤ j ∧ j < L ∧ u = j + j ∧ v = j + j + 1

/-- THEOREM: Edge mode γ_1 is strictly disjoint from all bulk Kitaev bonds -/
theorem edge_mode_1_not_in_bulk (L : Nat) (u v : Nat)
    (h_bulk : is_bulk_kitaev_bond L u v) :
    u ≠ 1 ∧ v ≠ 1 := by
  rcases h_bulk with ⟨j, hj1, _, rfl, rfl⟩
  constructor
  · intro h
    omega
  · intro h
    omega

/-- THEOREM: Edge mode γ_{2L} is strictly disjoint from all bulk Kitaev bonds -/
theorem edge_mode_2L_not_in_bulk (L : Nat) (u v : Nat)
    (h_bulk : is_bulk_kitaev_bond L u v) :
    u ≠ L + L ∧ v ≠ L + L := by
  rcases h_bulk with ⟨j, _, hjL, rfl, rfl⟩
  constructor
  · intro h
    omega
  · intro h
    omega

/-- Canonical BQNF Terminal Routing for Fermionic GIN Cochains -/
inductive TerminalRoute : Type
  | Repair             -- Exact sign cancellation or certified topological zero-mode protection
  | SplitBrainRefusal  -- Uncancelled fermion sign residual mass in Q^1
  | ClosureFailure     -- Broken inverted index posting list or missing parity sector
deriving Repr, DecidableEq

/-- Decision rule for GIN-indexed Fermion Sign Problem recovery -/
def evaluate_gin_fermion_recovery
    (is_valid_index : Bool)
    (uncancelled_sign_mass : Nat) : TerminalRoute :=
  if ¬is_valid_index then
    TerminalRoute.ClosureFailure
  else if uncancelled_sign_mass == 0 then
    TerminalRoute.Repair
  else
    TerminalRoute.SplitBrainRefusal

/-- THEOREM: Complete GIN pairing (zero residual sign mass) routes to Repair -/
theorem exact_gin_cancellation_routes_to_repair :
    evaluate_gin_fermion_recovery true 0 = TerminalRoute.Repair := by
  rfl

/-- THEOREM: Non-zero residual sign mass routes to SplitBrainRefusal -/
theorem residual_sign_routes_to_refusal (mass : Nat) (h : mass > 0) :
    evaluate_gin_fermion_recovery true mass = TerminalRoute.SplitBrainRefusal := by
  unfold evaluate_gin_fermion_recovery
  have h_ne : (mass == 0) = false := by
    simp [Nat.ne_of_gt h]
  simp [h_ne]

/-- THEOREM: Invalid GIN posting structure routes to ClosureFailure -/
theorem invalid_gin_routes_to_closure_failure (mass : Nat) :
    evaluate_gin_fermion_recovery false mass = TerminalRoute.ClosureFailure := by
  rfl

inductive GinBoundaryError where
  | refused (invariant : String) (parameter : String)
  deriving DecidableEq, Repr

def admit_gin_tag (tag : String) : Except GinBoundaryError String :=
  if tag == "nat" then Except.ok "nat"
  else if tag == "int" then Except.ok "int"
  else if tag == "float" then
    Except.error (GinBoundaryError.refused "float refused at the public boundary" "float")
  else if tag == "bool" then
    Except.error (GinBoundaryError.refused "boolean refused where an exact integer was required" "bool")
  else
    Except.error (GinBoundaryError.refused "tag is not an admitted exact scalar" tag)

def gin_refusal_invariant (tag : String) : String :=
  match admit_gin_tag tag with
  | Except.ok _ => "admitted"
  | Except.error (GinBoundaryError.refused invariant _) => invariant

theorem gin_float_tag_refused :
    gin_refusal_invariant "float" = "float refused at the public boundary" := by rfl

theorem gin_bool_tag_refused :
    gin_refusal_invariant "bool" = "boolean refused where an exact integer was required" := by rfl

#guard is_exact_involution_partner ⟨1, 1⟩ ⟨1, -1⟩ == true
#guard gin_refusal_invariant "float" == "float refused at the public boundary"
#guard gin_refusal_invariant "bool" == "boolean refused where an exact integer was required"

end MajoranaGinCore
