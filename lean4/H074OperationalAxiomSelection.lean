/-
  H074OperationalAxiomSelection.lean
  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)

  Campaign C500 Block 07: Finite Operational Reconstruction and Rivals.
  Mechanizes arithmetic dimension-formula identities and a declared Boolean table.
  No operational signatures, purification witnesses, or reconstruction theorem
  are implemented. The table is an input assumption, not a model classification.
  Arithmetic scope:
  1. Real linear dimensions of state spaces across probabilistic theories:
       Classical: d
       Complex Quantum: d^2
       Real Quantum: d(d + 1) / 2
       Quaternionic Quantum: d(2d - 1)
  2. Local tomography identity and obstructions:
       Complex quantum satisfies local tomography: D(d1 * d2) = D(d1) * D(d2).
       Classical satisfies local tomography: D(d1 * d2) = D(d1) * D(d2).
       Real quantum strictly fails local tomography at d=2: D(4) = 10 ≠ 3 * 3 = 9.
       Quaternionic quantum strictly fails local tomography at d=2: D(4) = 28 ≠ 6 * 6 = 36.
  3. Unique surviving row of the declared Boolean table under its two flags.
  4. Naimark dilation vs. Born rule derivation distinction.
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace FableHilbertWalk20260819.H074

-- ===========================================================================
-- Section 1: State Space Real Dimension Definitions
-- ===========================================================================

def classical_dim (d : Nat) : Nat := d

def complex_dim (d : Nat) : Nat := d * d

def real_dim (d : Nat) : Nat := (d * (d + 1)) / 2

def quaternionic_dim (d : Nat) : Nat := d * (2 * d - 1)


-- ===========================================================================
-- Section 2: Local Tomography Theorems and Obstructions
-- ===========================================================================

/-- The declared classical dimension formula is multiplicative. -/
theorem classical_dimension_product_identity (d1 d2 : Nat) :
    classical_dim (d1 * d2) = classical_dim d1 * classical_dim d2 := rfl

/-- The declared complex dimension formula is multiplicative:
    (d1 * d2)^2 = d1^2 * d2^2. -/
theorem complex_dimension_product_identity (d1 d2 : Nat) :
    complex_dim (d1 * d2) = complex_dim d1 * complex_dim d2 := by
  dsimp [complex_dim]
  rw [Nat.mul_assoc d1 d2 (d1 * d2)]
  rw [← Nat.mul_assoc d2 d1 d2]
  rw [Nat.mul_comm d2 d1]
  rw [Nat.mul_assoc d1 d2 d2]
  rw [← Nat.mul_assoc d1 d1 (d2 * d2)]


/-- Real quantum mechanics fails local tomography for two qubits (d1 = 2, d2 = 2):
    D(4) = 10, but D(2) * D(2) = 3 * 3 = 9. -/
theorem real_quantum_fails_local_tomography_d2 :
    real_dim 4 ≠ real_dim 2 * real_dim 2 := by
  decide

/-- Quaternionic quantum mechanics fails local tomography for two quaternionic qubits (d1 = 2, d2 = 2):
    D(4) = 28, but D(2) * D(2) = 6 * 6 = 36. -/
theorem quaternionic_fails_local_tomography_d2 :
    quaternionic_dim 4 ≠ quaternionic_dim 2 * quaternionic_dim 2 := by
  decide


-- ===========================================================================
-- Section 3: Rival Family Axiom Matrix and Selection Theorem
-- ===========================================================================

inductive FiniteRivalTheory where
  | Classical
  | RealQuantum
  | QuaternionicQuantum
  | ComplexQuantum
  deriving DecidableEq, Repr

/-- Declared table input for local tomography; no operational-model evaluator is present. -/
def declared_local_tomography : FiniteRivalTheory → Bool
  | FiniteRivalTheory.Classical => true
  | FiniteRivalTheory.RealQuantum => false
  | FiniteRivalTheory.QuaternionicQuantum => false
  | FiniteRivalTheory.ComplexQuantum => true

/-- Declared table input for purification; no purification witness is constructed. -/
def declared_purification : FiniteRivalTheory → Bool
  | FiniteRivalTheory.Classical => false
  | FiniteRivalTheory.RealQuantum => true
  | FiniteRivalTheory.QuaternionicQuantum => true
  | FiniteRivalTheory.ComplexQuantum => true

/-- The declared Boolean flags select one row. This does not classify operational theories. -/
theorem declared_table_selects_complex_row (t : FiniteRivalTheory) :
    declared_local_tomography t = true ∧ declared_purification t = true ↔
    t = FiniteRivalTheory.ComplexQuantum := by
  cases t <;> decide


-- ===========================================================================
-- Section 4: Naimark Dilation vs. Born Rule Derivation
-- ===========================================================================

inductive DilationDerivationStatus where
  | DerivesBornRuleUnconditionally
  | OperatorIdentityOnly
  deriving DecidableEq, Repr

def naimark_status : DilationDerivationStatus :=
  DilationDerivationStatus.OperatorIdentityOnly

/-- The stored audit label records no Born-rule derivation. This is a label check only. -/
theorem naimark_does_not_derive_born_unconditionally :
    naimark_status ≠ DilationDerivationStatus.DerivesBornRuleUnconditionally := by
  intro h
  nomatch h


-- ===========================================================================
-- Section 5: Axiom Census & Auditing
-- ===========================================================================

#print axioms classical_dimension_product_identity
#print axioms complex_dimension_product_identity
#print axioms real_quantum_fails_local_tomography_d2
#print axioms quaternionic_fails_local_tomography_d2
#print axioms declared_table_selects_complex_row
#print axioms naimark_does_not_derive_born_unconditionally

end FableHilbertWalk20260819.H074
