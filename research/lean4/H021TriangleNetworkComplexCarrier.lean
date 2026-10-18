



namespace FableHilbertWalk20260819.H021


namespace CyclotomicRing12

structure Cyclo12 where
  a0 : Int
  a1 : Int
  a2 : Int
  a3 : Int
  deriving DecidableEq, Repr

def zero : Cyclo12 := ⟨0, 0, 0, 0⟩
def one : Cyclo12 := ⟨1, 0, 0, 0⟩

def add (p q : Cyclo12) : Cyclo12 :=
  ⟨p.a0 + q.a0, p.a1 + q.a1, p.a2 + q.a2, p.a3 + q.a3⟩

def neg (p : Cyclo12) : Cyclo12 :=
  ⟨-p.a0, -p.a1, -p.a2, -p.a3⟩

def sub (p q : Cyclo12) : Cyclo12 :=
  ⟨p.a0 - q.a0, p.a1 - q.a1, p.a2 - q.a2, p.a3 - q.a3⟩

def mulX (p : Cyclo12) : Cyclo12 :=
  ⟨-p.a3, p.a0, p.a1 + p.a3, p.a2⟩

def mulX2 (p : Cyclo12) : Cyclo12 := mulX (mulX p)
def mulX3 (p : Cyclo12) : Cyclo12 := mulX (mulX2 p)

def smul (c : Int) (p : Cyclo12) : Cyclo12 :=
  ⟨c * p.a0, c * p.a1, c * p.a2, c * p.a3⟩

def mul (p q : Cyclo12) : Cyclo12 :=
  add (smul p.a0 q)
    (add (smul p.a1 (mulX q))
      (add (smul p.a2 (mulX2 q))
           (smul p.a3 (mulX3 q))))

def conj (p : Cyclo12) : Cyclo12 :=
  ⟨p.a0 + p.a2, p.a1, -p.a2, -p.a1 - p.a3⟩

instance : Zero Cyclo12 := ⟨zero⟩
instance : One Cyclo12 := ⟨one⟩
instance : Add Cyclo12 := ⟨add⟩
instance : Neg Cyclo12 := ⟨neg⟩
instance : Sub Cyclo12 := ⟨sub⟩
instance : Mul Cyclo12 := ⟨mul⟩

def zeta12 : Cyclo12 := ⟨0, 1, 0, 0⟩
def i_unit : Cyclo12 := ⟨0, 0, 0, 1⟩
def zeta3  : Cyclo12 := ⟨-1, 0, 1, 0⟩

theorem i_unit_squared : i_unit * i_unit = -1 := by rfl

theorem i_unit_fourth : i_unit * i_unit * i_unit * i_unit = 1 := by rfl

theorem zeta3_cubed : zeta3 * zeta3 * zeta3 = 1 := by rfl

theorem zeta3_cyclotomic : 1 + zeta3 + zeta3 * zeta3 = 0 := by rfl

theorem zeta12_fourth_is_zeta3 : zeta12 * zeta12 * zeta12 * zeta12 = zeta3 := by rfl

theorem zeta12_minimal_poly :
    zeta12 * zeta12 * zeta12 * zeta12 - zeta12 * zeta12 + 1 = 0 := by rfl

theorem zeta12_twelfth_is_one :
    zeta12 * zeta12 * zeta12 * zeta12 * zeta12 * zeta12 *
    zeta12 * zeta12 * zeta12 * zeta12 * zeta12 * zeta12 = 1 := by rfl

theorem composite_generator_zeta12 : -i_unit * zeta3 = zeta12 := by rfl

def rho_J : Cyclo12 := i_unit
def rho_tau : Cyclo12 := zeta3

theorem declared_holonomy_generator_identities :
    rho_J * rho_J = -1 ∧
    rho_J * rho_J * rho_J * rho_J = 1 ∧
    rho_tau * rho_tau * rho_tau = 1 ∧
    1 + rho_tau + rho_tau * rho_tau = 0 ∧
    -rho_J * rho_tau = zeta12 ∧
    zeta12 * zeta12 * zeta12 = rho_J ∧
    zeta12 * zeta12 * zeta12 * zeta12 = rho_tau ∧
    zeta12 * zeta12 * zeta12 * zeta12 - zeta12 * zeta12 + 1 = 0 := by
  refine ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

end CyclotomicRing12


namespace SimplicialDiamondComplex

structure Chain1 where
  e01 : Int
  e13 : Int
  e32 : Int
  e20 : Int
  e12 : Int
  deriving DecidableEq, Repr

def zero1 : Chain1 := ⟨0, 0, 0, 0, 0⟩

def add1 (c d : Chain1) : Chain1 :=
  ⟨c.e01 + d.e01, c.e13 + d.e13, c.e32 + d.e32, c.e20 + d.e20, c.e12 + d.e12⟩

def sub1 (c d : Chain1) : Chain1 :=
  ⟨c.e01 - d.e01, c.e13 - d.e13, c.e32 - d.e32, c.e20 - d.e20, c.e12 - d.e12⟩

def smul1 (n : Int) (c : Chain1) : Chain1 :=
  ⟨n * c.e01, n * c.e13, n * c.e32, n * c.e20, n * c.e12⟩

instance : Zero Chain1 := ⟨zero1⟩
instance : Add Chain1 := ⟨add1⟩
instance : Sub Chain1 := ⟨sub1⟩

structure Chain2 where
  fA : Int
  fB : Int
  deriving DecidableEq, Repr

def d2 (c : Chain2) : Chain1 :=
  ⟨c.fA, c.fB, c.fB, c.fA, c.fA - c.fB⟩

def cycle_C4 : Chain1 := ⟨1, 1, 1, 1, 0⟩

theorem stokes_diamond_boundary_cancellation :
    d2 ⟨1, 1⟩ = cycle_C4 := by rfl

structure Diag2 where
  d1 : Int
  d2 : Int
  deriving DecidableEq, Repr

def J_op (v : Diag2) : Diag2 :=
  ⟨v.d2, -v.d1⟩

theorem J_squared_is_neg_I (v : Diag2) :
    J_op (J_op v) = ⟨-v.d1, -v.d2⟩ := by
  obtain ⟨d1, d2⟩ := v
  dsimp [J_op]

theorem J_fourth_is_I (v : Diag2) :
    J_op (J_op (J_op (J_op v))) = v := by
  obtain ⟨d1, d2⟩ := v
  dsimp [J_op]
  rw [Int.neg_neg, Int.neg_neg]

structure Bary3 where
  b1 : Int
  b2 : Int
  deriving DecidableEq, Repr

def tau_op (v : Bary3) : Bary3 :=
  ⟨v.b2 - v.b1, -v.b1⟩

theorem tau_cubed_is_I (v : Bary3) :
    tau_op (tau_op (tau_op v)) = v := by
  obtain ⟨b1, b2⟩ := v
  dsimp [tau_op]
  have h1 : -b1 - (b2 - b1) = -b2 := by omega
  have h2 : -(b2 - b1) - -b2 = b1 := by omega
  have h3 : - -b2 = b2 := by omega
  rw [h1, h2, h3]

theorem tau_cyclotomic_relation (v : Bary3) :
    (tau_op (tau_op v)).b1 + (tau_op v).b1 + v.b1 = 0 ∧
    (tau_op (tau_op v)).b2 + (tau_op v).b2 + v.b2 = 0 := by
  obtain ⟨b1, b2⟩ := v
  dsimp [tau_op]
  constructor <;> omega

end SimplicialDiamondComplex


namespace EvaluationAndSorkin

open SimplicialDiamondComplex

structure Cochain1 where
  w01 : Int
  w13 : Int
  w32 : Int
  w20 : Int
  w12 : Int
  deriving DecidableEq, Repr

def add_cochain (p q : Cochain1) : Cochain1 :=
  ⟨p.w01 + q.w01, p.w13 + q.w13, p.w32 + q.w32, p.w20 + q.w20, p.w12 + q.w12⟩

def eval_pairing (c : Chain1) (phi : Cochain1) : Int :=
  c.e01 * phi.w01 + c.e13 * phi.w13 + c.e32 * phi.w32 + c.e20 * phi.w20 + c.e12 * phi.w12

theorem eval_pairing_left_additive
    (c1 c2 : Chain1) (phi : Cochain1) :
    eval_pairing (add1 c1 c2) phi =
    eval_pairing c1 phi + eval_pairing c2 phi := by
  obtain ⟨a1, a2, a3, a4, a5⟩ := c1
  obtain ⟨b1, b2, b3, b4, b5⟩ := c2
  obtain ⟨w1, w2, w3, w4, w5⟩ := phi
  dsimp [eval_pairing, add1]
  repeat rw [Int.add_mul]
  omega

theorem eval_pairing_right_additive
    (c : Chain1) (phi1 phi2 : Cochain1) :
    eval_pairing c (add_cochain phi1 phi2) =
    eval_pairing c phi1 + eval_pairing c phi2 := by
  obtain ⟨a1, a2, a3, a4, a5⟩ := c
  obtain ⟨w1, w2, w3, w4, w5⟩ := phi1
  obtain ⟨u1, u2, u3, u4, u5⟩ := phi2
  dsimp [eval_pairing, add_cochain]
  repeat rw [Int.mul_add]
  omega

structure DetectorTensor where
  g : Chain1 → Chain1 → Int
  h_bilin_left  : ∀ c1 c2 d, g (add1 c1 c2) d = g c1 d + g c2 d
  h_bilin_right : ∀ c d1 d2, g c (add1 d1 d2) = g c d1 + g c d2
  h_symm        : ∀ c d, g c d = g d c

def readout (E : DetectorTensor) (c : Chain1) : Int :=
  E.g c c

def I2 (E : DetectorTensor) (A B : Chain1) : Int :=
  readout E (add1 A B) - readout E A - readout E B

theorem I2_formula (E : DetectorTensor) (A B : Chain1) :
    I2 E A B = 2 * E.g A B := by
  dsimp [I2, readout]
  rw [E.h_bilin_left, E.h_bilin_right, E.h_bilin_right]
  rw [E.h_symm B A]
  omega

def I3 (E : DetectorTensor) (A B C : Chain1) : Int :=
  readout E (add1 (add1 A B) C)
  - readout E (add1 A B)
  - readout E (add1 B C)
  - readout E (add1 A C)
  + readout E A + readout E B + readout E C

theorem sorkin_third_order_identically_zero
    (E : DetectorTensor) (A B C : Chain1) :
    I3 E A B C = 0 := by
  dsimp [I3, readout]
  have h_exp3 : E.g (add1 (add1 A B) C) (add1 (add1 A B) C) =
                E.g A A + E.g B B + E.g C C +
                2 * E.g A B + 2 * E.g B C + 2 * E.g A C := by
    repeat rw [E.h_bilin_left]
    repeat rw [E.h_bilin_right]
    rw [E.h_symm B A, E.h_symm C A, E.h_symm C B]
    omega
  have h_expAB : E.g (add1 A B) (add1 A B) =
                 E.g A A + E.g B B + 2 * E.g A B := by
    rw [E.h_bilin_left, E.h_bilin_right, E.h_bilin_right]
    rw [E.h_symm B A]
    omega
  have h_expBC : E.g (add1 B C) (add1 B C) =
                 E.g B B + E.g C C + 2 * E.g B C := by
    rw [E.h_bilin_left, E.h_bilin_right, E.h_bilin_right]
    rw [E.h_symm C B]
    omega
  have h_expAC : E.g (add1 A C) (add1 A C) =
                 E.g A A + E.g C C + 2 * E.g A C := by
    rw [E.h_bilin_left, E.h_bilin_right, E.h_bilin_right]
    rw [E.h_symm C A]
    omega
  rw [h_exp3, h_expAB, h_expBC, h_expAC]
  omega

def metric_E (c d : Chain1) : Int :=
  c.e01 * d.e01 + c.e13 * d.e13 + c.e01 * d.e13 + c.e13 * d.e01 +
  c.e32 * d.e32 + c.e20 * d.e20 + c.e12 * d.e12

theorem metric_E_bilin_left (c1 c2 d : Chain1) :
    metric_E (add1 c1 c2) d = metric_E c1 d + metric_E c2 d := by
  obtain ⟨a1, a2, a3, a4, a5⟩ := c1
  obtain ⟨b1, b2, b3, b4, b5⟩ := c2
  obtain ⟨d1, d2, d3, d4, d5⟩ := d
  dsimp [metric_E, add1]
  repeat rw [Int.add_mul]
  omega

theorem metric_E_bilin_right (c d1 d2 : Chain1) :
    metric_E c (add1 d1 d2) = metric_E c d1 + metric_E c d2 := by
  obtain ⟨c1, c2, c3, c4, c5⟩ := c
  obtain ⟨a1, a2, a3, a4, a5⟩ := d1
  obtain ⟨b1, b2, b3, b4, b5⟩ := d2
  dsimp [metric_E, add1]
  repeat rw [Int.mul_add]
  omega

theorem metric_E_symm (c d : Chain1) :
    metric_E c d = metric_E d c := by
  obtain ⟨c1, c2, c3, c4, c5⟩ := c
  obtain ⟨d1, d2, d3, d4, d5⟩ := d
  dsimp [metric_E]
  repeat rw [Int.mul_comm c1]
  repeat rw [Int.mul_comm c2]
  repeat rw [Int.mul_comm c3]
  repeat rw [Int.mul_comm c4]
  repeat rw [Int.mul_comm c5]
  omega

def standardDetector : DetectorTensor where
  g := metric_E
  h_bilin_left := metric_E_bilin_left
  h_bilin_right := metric_E_bilin_right
  h_symm := metric_E_symm

def slitA : Chain1 := ⟨1, 0, 0, 0, 0⟩
def slitB : Chain1 := ⟨0, 1, 0, 0, 0⟩
def slitC : Chain1 := ⟨0, 0, 1, 0, 0⟩

theorem concrete_I2_nonzero :
    I2 standardDetector slitA slitB = 2 := by
  rw [I2_formula]
  dsimp [standardDetector, metric_E, slitA, slitB]

theorem concrete_I3_zero :
    I3 standardDetector slitA slitB slitC = 0 := by
  apply sorkin_third_order_identically_zero

def cubic_readout (c : Chain1) : Int :=
  (c.e01 + c.e13 + c.e32) * (c.e01 + c.e13 + c.e32) * (c.e01 + c.e13 + c.e32)

def I3_cubic (A B C : Chain1) : Int :=
  cubic_readout (add1 (add1 A B) C)
  - cubic_readout (add1 A B)
  - cubic_readout (add1 B C)
  - cubic_readout (add1 A C)
  + cubic_readout A + cubic_readout B + cubic_readout C

theorem cubic_valuation_violates_sorkin :
    I3_cubic slitA slitB slitC = 6 := by
  dsimp [I3_cubic, cubic_readout, slitA, slitB, slitC, add1]

end EvaluationAndSorkin


namespace SignedPermutationAndResidue

structure Vec3 where
  x0 : Int
  x1 : Int
  x2 : Int
  deriving DecidableEq, Repr

def Vec3.l1_norm (v : Vec3) : Nat :=
  v.x0.natAbs + v.x1.natAbs + v.x2.natAbs

def Vec3.l2_norm_sq (v : Vec3) : Int :=
  v.x0 * v.x0 + v.x1 * v.x1 + v.x2 * v.x2

def Vec3.inner (u v : Vec3) : Int :=
  u.x0 * v.x0 + u.x1 * v.x1 + u.x2 * v.x2

def signed_perm_B3 (v : Vec3) : Vec3 :=
  ⟨-v.x1, v.x0, -v.x2⟩

theorem signed_perm_preserves_l1 (v : Vec3) :
    Vec3.l1_norm (signed_perm_B3 v) = Vec3.l1_norm v := by
  dsimp [signed_perm_B3, Vec3.l1_norm]
  have h0 : (-v.x1).natAbs = v.x1.natAbs := Int.natAbs_neg v.x1
  have h2 : (-v.x2).natAbs = v.x2.natAbs := Int.natAbs_neg v.x2
  rw [h0, h2]
  omega

theorem signed_perm_preserves_inner (u v : Vec3) :
    Vec3.inner (signed_perm_B3 u) (signed_perm_B3 v) = Vec3.inner u v := by
  dsimp [signed_perm_B3, Vec3.inner]
  have h1 : -u.x1 * -v.x1 = u.x1 * v.x1 := Int.neg_mul_neg u.x1 v.x1
  have h2 : -u.x2 * -v.x2 = u.x2 * v.x2 := Int.neg_mul_neg u.x2 v.x2
  rw [h1, h2]
  rw [Int.add_comm (u.x1 * v.x1) (u.x0 * v.x0)]

theorem signed_perm_preserves_l2_norm_sq (v : Vec3) :
    Vec3.l2_norm_sq (signed_perm_B3 v) = Vec3.l2_norm_sq v := by
  dsimp [signed_perm_B3, Vec3.l2_norm_sq]
  have h1 : -v.x1 * -v.x1 = v.x1 * v.x1 := Int.neg_mul_neg v.x1 v.x1
  have h2 : -v.x2 * -v.x2 = v.x2 * v.x2 := Int.neg_mul_neg v.x2 v.x2
  rw [h1, h2]
  rw [Int.add_comm (v.x1 * v.x1) (v.x0 * v.x0)]

def proj_admission (v : Vec3) : Vec3 :=
  ⟨v.x0, v.x1, 0⟩

def irreversible_residue_l1 (v : Vec3) : Nat :=
  Vec3.l1_norm v - Vec3.l1_norm (proj_admission v)

theorem irreversible_residue_positive_witness :
    let v : Vec3 := ⟨1, 2, 5⟩
    irreversible_residue_l1 v = 5 := by
  decide

end SignedPermutationAndResidue


#print axioms CyclotomicRing12.i_unit_squared
#print axioms CyclotomicRing12.zeta3_cubed
#print axioms CyclotomicRing12.zeta12_minimal_poly
#print axioms CyclotomicRing12.composite_generator_zeta12
#print axioms CyclotomicRing12.declared_holonomy_generator_identities
#print axioms SimplicialDiamondComplex.stokes_diamond_boundary_cancellation
#print axioms SimplicialDiamondComplex.J_squared_is_neg_I
#print axioms SimplicialDiamondComplex.tau_cubed_is_I
#print axioms EvaluationAndSorkin.sorkin_third_order_identically_zero
#print axioms EvaluationAndSorkin.concrete_I2_nonzero
#print axioms EvaluationAndSorkin.cubic_valuation_violates_sorkin
#print axioms SignedPermutationAndResidue.signed_perm_preserves_l1
#print axioms SignedPermutationAndResidue.signed_perm_preserves_inner
#print axioms SignedPermutationAndResidue.irreversible_residue_positive_witness

end FableHilbertWalk20260819.H021

private def l5aProvenance : String :=
  "Origin: lean4/H021TriangleNetworkComplexCarrier.lean Claim: i_unit_squared AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
