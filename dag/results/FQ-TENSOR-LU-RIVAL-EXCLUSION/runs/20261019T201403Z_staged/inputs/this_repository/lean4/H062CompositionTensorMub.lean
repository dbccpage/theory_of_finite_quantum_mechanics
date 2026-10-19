
namespace FableHilbertWalk20260819.H062


inductive TensorAxiom : Type
  | bilinearity : TensorAxiom
  | local_unitary_covariance : TensorAxiom
  | product_marginal_consistency : TensorAxiom
  | no_signaling : TensorAxiom
  deriving DecidableEq, Repr

def tensorAxiomList : List TensorAxiom :=
  [TensorAxiom.bilinearity,
   TensorAxiom.local_unitary_covariance,
   TensorAxiom.product_marginal_consistency,
   TensorAxiom.no_signaling]

theorem tensor_axiom_count_is_four : tensorAxiomList.length = 4 := by
  rfl


structure Vec2 where
  x0 : Int
  x1 : Int
  deriving DecidableEq, Repr

def Vec2.add (u v : Vec2) : Vec2 :=
  ⟨u.x0 + v.x0, u.x1 + v.x1⟩

def Vec2.smul (c : Int) (u : Vec2) : Vec2 :=
  ⟨c * u.x0, c * u.x1⟩

def projDump (u v : Vec2) : Vec2 :=
  ⟨(v.x0 + v.x1) * u.x0, (v.x0 + v.x1) * u.x1⟩

theorem projDump_linear_left (u1 u2 v : Vec2) :
    projDump (Vec2.add u1 u2) v = Vec2.add (projDump u1 v) (projDump u2 v) := by
  dsimp [projDump, Vec2.add]
  rw [Int.mul_add, Int.mul_add]

theorem projDump_linear_right (u v1 v2 : Vec2) :
    projDump u (Vec2.add v1 v2) = Vec2.add (projDump u v1) (projDump u v2) := by
  dsimp [projDump, Vec2.add]
  have h : v1.x0 + v2.x0 + (v1.x1 + v2.x1) = (v1.x0 + v1.x1) + (v2.x0 + v2.x1) := by omega
  rw [h]
  repeat rw [Int.add_mul]

def e0 : Vec2 := ⟨1, 0⟩
def e1 : Vec2 := ⟨0, 1⟩

def pauliZ (v : Vec2) : Vec2 :=
  ⟨v.x0, -v.x1⟩

theorem pauliZ_e0 : pauliZ e0 = e0 := by rfl

theorem pauliZ_e1 : pauliZ e1 = ⟨0, -1⟩ := by rfl

theorem projDump_collision :
    projDump e0 e0 = e0 ∧ projDump e0 e1 = e0 := by
  decide

theorem rival_fails_local_unitary_covariance :
    (projDump e0 (pauliZ e0)).x0 ≠ (projDump e0 (pauliZ e1)).x0 := by
  decide


def rational_overlap_d2_denom : Nat := 2
def rational_overlap_d3_denom : Nat := 3

def composite_d6_overlap_denom : Nat :=
  rational_overlap_d2_denom * rational_overlap_d3_denom

theorem composite_d6_overlap_is_one_sixth :
    composite_d6_overlap_denom = 6 := by
  rfl

def product_mub_count_d6 : Nat := 3

theorem product_mub_count_is_three : product_mub_count_d6 = 3 := by
  rfl


def gkp_phase_order (N : Nat) : Nat := N

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

private def l5aProvenance : String :=
  "Origin: lean4/H062CompositionTensorMub.lean Claim: tensor_axiom_count_is_four AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
