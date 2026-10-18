/-
  H041PrimePWignerPhaseSpace.lean
  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)

  Shows in this model under exact integer arithmetic that:
  1. For prime dimension p = 5 on discrete phase space F_5 x F_5, the parity reflection
     operator P on Z^5 reflects coordinates j |-> (-j) mod 5:
       P(v0, v1, v2, v3, v4) = (v0, v4, v3, v2, v1), satisfying P^2 = I.
  2. The stabilizer state |0> = (1, 0, 0, 0, 0) is a +1 eigenstate of P:
       P |0> = |0>, yielding positive parity expectation <0| P |0> = 1 > 0.
  3. The uniform stabilizer state |+> = (1, 1, 1, 1, 1) is also a +1 eigenstate:
       P |+> = |+>, yielding positive parity expectation <+| P |+> = 5 > 0.
  4. The magic state |M> = (0, 1, 0, 0, -1) is a -1 eigenstate of P:
       P |M> = -|M|, with unnormalized parity expectation <M| P |M> = -2 < 0.
  5. This establishes the point negativity witness <M| P |M> = - <M| M> = -2 < 0
     in the discrete Gross Wigner representation.
  6. Gross phase space covariance holds: the cyclic translation X satisfies
       P X P = X^{-1}, confirming that phase space reflection inverts translations.
-/

namespace FableHilbertWalk20260819.H041

structure Vec5 where
  v0 : Int
  v1 : Int
  v2 : Int
  v3 : Int
  v4 : Int
  deriving DecidableEq, Repr

def dot5 (u v : Vec5) : Int :=
  u.v0 * v.v0 + u.v1 * v.v1 + u.v2 * v.v2 + u.v3 * v.v3 + u.v4 * v.v4

def normSq5 (u : Vec5) : Int := dot5 u u

/-- Discrete phase space parity operator P in dimension p = 5:
    j |-> (-j) mod 5, mapping (v0, v1, v2, v3, v4) |-> (v0, v4, v3, v2, v1). -/
def P_op (v : Vec5) : Vec5 :=
  ⟨v.v0, v.v4, v.v3, v.v2, v.v1⟩

/-- Parity is an involution: P^2 = I. -/
theorem parity_is_involution (v : Vec5) : P_op (P_op v) = v := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := v
  rfl

/-- Standard computational basis stabilizer state |0> = (1, 0, 0, 0, 0). -/
def psi_stabilizer : Vec5 := ⟨1, 0, 0, 0, 0⟩

/-- Uniform superposition stabilizer state |+> = (1, 1, 1, 1, 1). -/
def psi_plus : Vec5 := ⟨1, 1, 1, 1, 1⟩

/-- Magic state |M> = (0, 1, 0, 0, -1). -/
def psi_magic : Vec5 := ⟨0, 1, 0, 0, -1⟩

/-- Stabilizer state |0> is a +1 eigenstate of P. -/
theorem stabilizer_zero_parity_eigenstate :
    P_op psi_stabilizer = psi_stabilizer := by rfl

/-- Stabilizer state |0> has positive parity expectation +1. -/
theorem stabilizer_zero_positive_expectation :
    dot5 psi_stabilizer (P_op psi_stabilizer) = 1 := by rfl

/-- Uniform stabilizer state |+> is a +1 eigenstate of P. -/
theorem stabilizer_plus_parity_eigenstate :
    P_op psi_plus = psi_plus := by rfl

/-- Uniform stabilizer state |+> has positive parity expectation +5. -/
theorem stabilizer_plus_positive_expectation :
    dot5 psi_plus (P_op psi_plus) = 5 := by rfl

/-- Magic state |M> is an exact -1 eigenstate of P: P |M> = -|M|. -/
theorem magic_parity_eigenstate :
    P_op psi_magic = ⟨-psi_magic.v0, -psi_magic.v1, -psi_magic.v2, -psi_magic.v3, -psi_magic.v4⟩ := by rfl

/-- Magic state norm squared is 2. -/
theorem magic_norm_sq : normSq5 psi_magic = 2 := by rfl

/-- Magic state unnormalized parity expectation is -2. -/
theorem magic_parity_inner_product :
    dot5 psi_magic (P_op psi_magic) = -2 := by rfl

/-- Strict Wigner point negativity witness:
    <M| P |M> = - <M| M> = -2 < 0. -/
theorem magic_wigner_negativity_witness :
    dot5 psi_magic (P_op psi_magic) < 0 ∧
    dot5 psi_magic (P_op psi_magic) = - (normSq5 psi_magic) := by decide

/-- Cyclic translation operator X (position shift j |-> j + 1 mod 5). -/
def X_shift (v : Vec5) : Vec5 :=
  ⟨v.v4, v.v0, v.v1, v.v2, v.v3⟩

/-- Inverse translation operator X^{-1} (position shift j |-> j - 1 mod 5). -/
def X_inv (v : Vec5) : Vec5 :=
  ⟨v.v1, v.v2, v.v3, v.v4, v.v0⟩

/-- Translation has order 5: X^5 = I. -/
theorem x_shift_order_five (v : Vec5) :
    X_shift (X_shift (X_shift (X_shift (X_shift v)))) = v := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := v
  rfl

/-- X_inv is the exact inverse of X_shift. -/
theorem x_shift_inverse (v : Vec5) : X_inv (X_shift v) = v := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := v
  rfl

/-- Gross covariance: conjugation of translation by parity inverts the shift:
    P X P = X^{-1}. -/
theorem gross_parity_covariance (v : Vec5) :
    P_op (X_shift (P_op v)) = X_inv v := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := v
  rfl

/-- Dual commutation formulation of Gross covariance: P X = X^{-1} P. -/
theorem gross_parity_commutation (v : Vec5) :
    P_op (X_shift v) = X_inv (P_op v) := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := v
  rfl

#print axioms parity_is_involution
#print axioms stabilizer_zero_parity_eigenstate
#print axioms stabilizer_zero_positive_expectation
#print axioms stabilizer_plus_parity_eigenstate
#print axioms stabilizer_plus_positive_expectation
#print axioms magic_parity_eigenstate
#print axioms magic_norm_sq
#print axioms magic_parity_inner_product
#print axioms magic_wigner_negativity_witness
#print axioms x_shift_order_five
#print axioms x_shift_inverse
#print axioms gross_parity_covariance
#print axioms gross_parity_commutation

end FableHilbertWalk20260819.H041
