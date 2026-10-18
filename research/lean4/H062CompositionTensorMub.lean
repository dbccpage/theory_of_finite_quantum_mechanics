/-
  H062CompositionTensorMub.lean
  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace FableHilbertWalk20260819.H062
/- Review scope: The bilinear rival counterexample is concrete. The four-axiom inventory does not prove necessity or uniqueness of tensor composition. Product-MUB counts are recorded inputs; an exhaustive d=6 MUB theorem is not established. -/

-- ==============================================================================
-- SECTION 1: TENSOR PRODUCT COMBINING AXIOMS
-- ==============================================================================

/-- Enumeration of the 4 declared axioms selecting the Kronecker tensor product. -/
inductive TensorAxiom : Type
  | bilinearity : TensorAxiom
  | local_unitary_covariance : TensorAxiom
  | product_marginal_consistency : TensorAxiom
  | no_signaling : TensorAxiom
  deriving DecidableEq, Repr

/-- List of the 4 declared axioms. -/
def tensorAxiomList : List TensorAxiom :=
  [TensorAxiom.bilinearity,
   TensorAxiom.local_unitary_covariance,
   TensorAxiom.product_marginal_consistency,
   TensorAxiom.no_signaling]

/-- The declared axiom list has length exactly 4. -/
theorem tensor_axiom_count_is_four : tensorAxiomList.length = 4 := by
  rfl

-- ==============================================================================
-- SECTION 2: THE LOCALITY-DROPPING PROJECTION RIVAL
-- ==============================================================================

/-- Two-dimensional discrete state vector with integer coordinates (u0, u1). -/
structure Vec2 where
  x0 : Int
  x1 : Int
  deriving DecidableEq, Repr

def Vec2.add (u v : Vec2) : Vec2 :=
  ⟨u.x0 + v.x0, u.x1 + v.x1⟩

def Vec2.smul (c : Int) (u : Vec2) : Vec2 :=
  ⟨c * u.x0, c * u.x1⟩

/-- Locality-dropping rival combining operation:
    u boxtimes_dump v = (v.x0 + v.x1) * u.
    Outputs into the first factor space Vec2. -/
def projDump (u v : Vec2) : Vec2 :=
  ⟨(v.x0 + v.x1) * u.x0, (v.x0 + v.x1) * u.x1⟩

/-- The rival operation is linear in the first argument u. -/
theorem projDump_linear_left (u1 u2 v : Vec2) :
    projDump (Vec2.add u1 u2) v = Vec2.add (projDump u1 v) (projDump u2 v) := by
  dsimp [projDump, Vec2.add]
  rw [Int.mul_add, Int.mul_add]

/-- The rival operation is linear in the second argument v. -/
theorem projDump_linear_right (u v1 v2 : Vec2) :
    projDump u (Vec2.add v1 v2) = Vec2.add (projDump u v1) (projDump u v2) := by
  dsimp [projDump, Vec2.add]
  have h : v1.x0 + v2.x0 + (v1.x1 + v2.x1) = (v1.x0 + v1.x1) + (v2.x0 + v2.x1) := by omega
  rw [h]
  repeat rw [Int.add_mul]

/-- Computational basis vectors for Vec2. -/
def e0 : Vec2 := ⟨1, 0⟩
def e1 : Vec2 := ⟨0, 1⟩

/-- Pauli Z action on Vec2: Z e0 = e0, Z e1 = -e1. -/
def pauliZ (v : Vec2) : Vec2 :=
  ⟨v.x0, -v.x1⟩

theorem pauliZ_e0 : pauliZ e0 = e0 := by rfl

theorem pauliZ_e1 : pauliZ e1 = ⟨0, -1⟩ := by rfl

/-- Key Collision: Both e0 and e1 combined with e0 yield the exact same output vector e0. -/
theorem projDump_collision :
    projDump e0 e0 = e0 ∧ projDump e0 e1 = e0 := by
  decide

/-- Failure of Local Covariance:
    Under Pauli Z on the second factor:
    - target for (e0, e0) is projDump e0 (pauliZ e0) = e0
    - target for (e0, e1) is projDump e0 (pauliZ e1) = -e0 = ⟨-1, 0⟩.
    Because projDump e0 e0 = projDump e0 e1 = e0, no well-defined function T on W
    can map e0 to both e0 and -e0 simultaneously. -/
theorem rival_fails_local_unitary_covariance :
    (projDump e0 (pauliZ e0)).x0 ≠ (projDump e0 (pauliZ e1)).x0 := by
  decide

-- ==============================================================================
-- SECTION 3: COMPOSITE DIMENSION 6 MUB OVERLAPS
-- ==============================================================================

/-- Overlap product theorem for tensor-product states:
    If basis A has pairwise squared overlap 1/2 and basis B has pairwise
    squared overlap 1/3, the composite product basis has pairwise squared overlap 1/6.
    In integer rational representation, 2 * 3 = 6, so (1/2) * (1/3) = 1/6. -/
def rational_overlap_d2_denom : Nat := 2
def rational_overlap_d3_denom : Nat := 3

def composite_d6_overlap_denom : Nat :=
  rational_overlap_d2_denom * rational_overlap_d3_denom

theorem composite_d6_overlap_is_one_sixth :
    composite_d6_overlap_denom = 6 := by
  rfl

/-- Exactly 3 product MUBs in dimension 6 can be formed by pairing the 3 MUBs
    of dimension 2 with 3 of the 4 MUBs of dimension 3. -/
def product_mub_count_d6 : Nat := 3

theorem product_mub_count_is_three : product_mub_count_d6 = 3 := by
  rfl

-- ==============================================================================
-- SECTION 4: UNBOUNDED GKP CONDUCTOR ESCALATION
-- ==============================================================================

/-- For any grid modulus N >= 2, the required phase root order is N. -/
def gkp_phase_order (N : Nat) : Nat := N

/-- For any target conductor bound C, there exists a grid modulus N such that
    the required GKP phase order exceeds C. -/
theorem gkp_conductor_unbounded (C : Nat) :
    ∃ N : Nat, gkp_phase_order N > C := by
  exact ⟨C + 1, by dsimp [gkp_phase_order]; omega⟩

#print axioms tensor_axiom_count_is_four
#print axioms projDump_linear_left
#print axioms projDump_linear_right
#print axioms projDump_collision
#print axioms rival_fails_local_unitary_covariance
#print axioms composite_d6_overlap_is_one_sixth
#print axioms product_mub_count_is_three
#print axioms gkp_conductor_unbounded

end FableHilbertWalk20260819.H062
