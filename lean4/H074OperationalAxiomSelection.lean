

namespace FableHilbertWalk20260819.H074


def classical_dim (d : Nat) : Nat := d

def complex_dim (d : Nat) : Nat := d * d

def real_dim (d : Nat) : Nat := (d * (d + 1)) / 2

def quaternionic_dim (d : Nat) : Nat := d * (2 * d - 1)



theorem classical_dimension_product_identity (d1 d2 : Nat) :
    classical_dim (d1 * d2) = classical_dim d1 * classical_dim d2 := rfl

theorem complex_dimension_product_identity (d1 d2 : Nat) :
    complex_dim (d1 * d2) = complex_dim d1 * complex_dim d2 := by
  dsimp [complex_dim]
  rw [Nat.mul_assoc d1 d2 (d1 * d2)]
  rw [← Nat.mul_assoc d2 d1 d2]
  rw [Nat.mul_comm d2 d1]
  rw [Nat.mul_assoc d1 d2 d2]
  rw [← Nat.mul_assoc d1 d1 (d2 * d2)]


theorem real_quantum_fails_local_tomography_d2 :
    real_dim 4 ≠ real_dim 2 * real_dim 2 := by
  decide

theorem quaternionic_fails_local_tomography_d2 :
    quaternionic_dim 4 ≠ quaternionic_dim 2 * quaternionic_dim 2 := by
  decide



inductive FiniteRivalTheory where
  | Classical
  | RealQuantum
  | QuaternionicQuantum
  | ComplexQuantum
  deriving DecidableEq, Repr

def declared_local_tomography : FiniteRivalTheory → Bool
  | FiniteRivalTheory.Classical => true
  | FiniteRivalTheory.RealQuantum => false
  | FiniteRivalTheory.QuaternionicQuantum => false
  | FiniteRivalTheory.ComplexQuantum => true

def declared_purification : FiniteRivalTheory → Bool
  | FiniteRivalTheory.Classical => false
  | FiniteRivalTheory.RealQuantum => true
  | FiniteRivalTheory.QuaternionicQuantum => true
  | FiniteRivalTheory.ComplexQuantum => true

theorem declared_table_selects_complex_row (t : FiniteRivalTheory) :
    declared_local_tomography t = true ∧ declared_purification t = true ↔
    t = FiniteRivalTheory.ComplexQuantum := by
  cases t <;> decide



inductive DilationDerivationStatus where
  | DerivesBornRuleUnconditionally
  | OperatorIdentityOnly
  deriving DecidableEq, Repr

def naimark_status : DilationDerivationStatus :=
  DilationDerivationStatus.OperatorIdentityOnly

theorem naimark_does_not_derive_born_unconditionally :
    naimark_status ≠ DilationDerivationStatus.DerivesBornRuleUnconditionally := by
  intro h
  nomatch h



#print axioms classical_dimension_product_identity
#print axioms complex_dimension_product_identity
#print axioms real_quantum_fails_local_tomography_d2
#print axioms quaternionic_fails_local_tomography_d2
#print axioms declared_table_selects_complex_row
#print axioms naimark_does_not_derive_born_unconditionally

end FableHilbertWalk20260819.H074

private def l5aProvenance : String :=
  "Origin: lean4/H074OperationalAxiomSelection.lean Claim: classical_dimension_product_identity AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
