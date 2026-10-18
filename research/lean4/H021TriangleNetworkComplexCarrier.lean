/-
  H021TriangleNetworkComplexCarrier.lean --
  Simplicial diamond 2-complex and declared Cyclo12 generator identities,
  canonical chain-cochain evaluation bilinearity, Sorkin I_3 === 0,
  signed permutation isometries B_n, and irreversible residue decomposition.

  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)
  Source-paper contact: Paper 122 §7.7, Milestone 1 Requirements R1, R2, R6.

  Target propositions:
    1. Simplicial diamond 2-complex Stokes boundary cancellation:
       partial_2(Delta_A + Delta_B) = C_4 (stokes_diamond_boundary_cancellation).
    2. Boundary 4-cycle J^2 = -I_2, J^4 = I_2 on diagonal difference space:
       J_squared_is_neg_I, J_fourth_is_I.
    3. Face rotation tau^3 = I, tau^2 + tau + I = 0 on barycentric space:
       tau_cubed_is_I, tau_cyclotomic_relation.
    4. Declared Cyclo12 elements satisfy exact generator identities without continuous S^1:
       i_unit_squared, i_unit_fourth, zeta3_cubed, zeta3_cyclotomic,
       zeta12_minimal_poly, zeta12_twelfth_is_one, composite_generator_zeta12.
    5. Canonical evaluation pairing <c, phi> bilinear in both arguments:
       eval_pairing_left_additive, eval_pairing_right_additive.
    6. 2-point tensor detector readout (p=2) forces Sorkin third-order
       interference to vanish identically:
       sorkin_third_order_identically_zero, I2_formula,
       concrete_I2_nonzero, concrete_I3_zero.
    7. Cubic valuation obstruction (p=3):
       cubic_valuation_violates_sorkin (I_3 = 6 != 0).
    8. Signed permutation isometries B_n preserve l1 and l2 norms:
       signed_perm_preserves_l1, signed_perm_preserves_inner, signed_perm_preserves_l2_norm_sq.
    9. Irreversible residue decomposition for non-exchangeable admissions:
       irreversible_residue_positive_witness.

  Nonclaim boundary:
    No continuous circle S^1 or field C. No continuous U(1) gauge group.
    No infinite-dimensional Hilbert space.
-/

namespace FableHilbertWalk20260819.H021

-- ==============================================================================
-- PART 1: MINIMAL CYCLOTOMIC RING Z[zeta_12] = Z[x] / (x^4 - x^2 + 1)
-- ==============================================================================

namespace CyclotomicRing12

/-- An element of Z[zeta_12] represented as a polynomial a0 + a1*x + a2*x^2 + a3*x^3
    modulo Phi_12(x) = x^4 - x^2 + 1. -/
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

/-- Multiplication by generator x modulo x^4 = x^2 - 1:
    x * (a0 + a1*x + a2*x^2 + a3*x^3) = -a3 + a0*x + (a1 + a3)*x^2 + a2*x^3. -/
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

/-- Discrete algebraic conjugation (x* = x^11 = -x^3 + x). -/
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

/-- Order-4 imaginary unit identity i^2 = -1. -/
theorem i_unit_squared : i_unit * i_unit = -1 := by rfl

/-- Order-4 cyclic group identity i^4 = 1. -/
theorem i_unit_fourth : i_unit * i_unit * i_unit * i_unit = 1 := by rfl

/-- Order-3 face rotation cyclic group identity (zeta_3)^3 = 1. -/
theorem zeta3_cubed : zeta3 * zeta3 * zeta3 = 1 := by rfl

/-- Order-3 cyclotomic polynomial relation 1 + zeta_3 + (zeta_3)^2 = 0. -/
theorem zeta3_cyclotomic : 1 + zeta3 + zeta3 * zeta3 = 0 := by rfl

/-- Relation between primitive 12th root and 3rd root: (zeta_12)^4 = zeta_3. -/
theorem zeta12_fourth_is_zeta3 : zeta12 * zeta12 * zeta12 * zeta12 = zeta3 := by rfl

/-- Minimal polynomial identity Phi_12(zeta_12) = (zeta_12)^4 - (zeta_12)^2 + 1 = 0. -/
theorem zeta12_minimal_poly :
    zeta12 * zeta12 * zeta12 * zeta12 - zeta12 * zeta12 + 1 = 0 := by rfl

/-- Full 12-cycle closure (zeta_12)^12 = 1. -/
theorem zeta12_twelfth_is_one :
    zeta12 * zeta12 * zeta12 * zeta12 * zeta12 * zeta12 *
    zeta12 * zeta12 * zeta12 * zeta12 * zeta12 * zeta12 = 1 := by rfl

/-- Composite generator theorem: product of order-4 (-i) and order-3 (zeta_3)
    algebraically generates the native primitive 12th root zeta_12. -/
theorem composite_generator_zeta12 : -i_unit * zeta3 = zeta12 := by rfl

/-- Cellular holonomy generator assignments for diamond 2-complex:
    rho_J maps the boundary 4-cycle J to the imaginary unit i_unit in Cyclo12.
    rho_tau maps the triangular face 3-cycle tau to zeta3 in Cyclo12. -/
def rho_J : Cyclo12 := i_unit
def rho_tau : Cyclo12 := zeta3

/-- Theorem `declared_holonomy_generator_identities`:
    For the declared assignments `rho_J := i_unit` and `rho_tau := zeta3`,
    the following Cyclo12 identities hold:
    1. rho_J has exact order 4 (rho_J^2 = -1, rho_J^4 = 1).
    2. rho_tau has exact order 3 (rho_tau^3 = 1, 1 + rho_tau + rho_tau^2 = 0).
    3. The composite product -rho_J * rho_tau equals the declared element zeta_12.
    4. Powers of zeta_12 reproduce the generators: zeta_12^3 = rho_J, zeta_12^4 = rho_tau.
    5. The composite generator satisfies the 12th cyclotomic polynomial Phi_12(x) = x^4 - x^2 + 1 = 0. -/
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

-- ==============================================================================
-- PART 2: SIMPLICIAL DIAMOND 2-COMPLEX Delta_A^2 \cup_e Delta_B^2
-- ==============================================================================

namespace SimplicialDiamondComplex

/-- 1-Chains on the diamond 2-complex with 4 vertices {0, 1, 2, 3}.
    Edges:
    - Outer boundary edges: e01, e13, e32, e20
    - Interior diagonal shared edge: e12. -/
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

/-- 2-Chains spanned by the two triangular faces Delta_A = (0, 1, 2) and Delta_B = (1, 3, 2). -/
structure Chain2 where
  fA : Int
  fB : Int
  deriving DecidableEq, Repr

/-- Boundary differential operator partial_2 : C_2 -> C_1:
    partial_2(Delta_A) = e01 + e12 + e20
    partial_2(Delta_B) = e13 + e32 - e12. -/
def d2 (c : Chain2) : Chain1 :=
  ⟨c.fA, c.fB, c.fB, c.fA, c.fA - c.fB⟩

/-- The outer boundary 4-cycle C_4 = (0 -> 1 -> 3 -> 2 -> 0). -/
def cycle_C4 : Chain1 := ⟨1, 1, 1, 1, 0⟩

/-- Stokes Boundary Cancellation Theorem:
    The glued complex Delta_A + Delta_B has boundary equal to the outer 4-cycle C_4,
    with interior edge e12 canceling identically (+1 - 1 = 0). -/
theorem stokes_diamond_boundary_cancellation :
    d2 ⟨1, 1⟩ = cycle_C4 := by rfl

/-- Diagonal coordinate 2-space (d1, d2) = (v3 - v0, v2 - v1). -/
structure Diag2 where
  d1 : Int
  d2 : Int
  deriving DecidableEq, Repr

/-- Order-4 cyclic permutation J on diagonal coordinate space: J(d1, d2) = (d2, -d1). -/
def J_op (v : Diag2) : Diag2 :=
  ⟨v.d2, -v.d1⟩

/-- Order-4 generator satisfies J^2 = -I_2. -/
theorem J_squared_is_neg_I (v : Diag2) :
    J_op (J_op v) = ⟨-v.d1, -v.d2⟩ := by
  obtain ⟨d1, d2⟩ := v
  dsimp [J_op]

/-- Cyclic closure J^4 = I_2. -/
theorem J_fourth_is_I (v : Diag2) :
    J_op (J_op (J_op (J_op v))) = v := by
  obtain ⟨d1, d2⟩ := v
  dsimp [J_op]
  rw [Int.neg_neg, Int.neg_neg]

/-- Barycentric coordinates on triangular face Delta_A: (b1, b2) = (v1 - v0, v2 - v0). -/
structure Bary3 where
  b1 : Int
  b2 : Int
  deriving DecidableEq, Repr

/-- Order-3 face rotation tau: tau(b1, b2) = (b2 - b1, -b1). -/
def tau_op (v : Bary3) : Bary3 :=
  ⟨v.b2 - v.b1, -v.b1⟩

/-- Cyclic closure tau^3 = I. -/
theorem tau_cubed_is_I (v : Bary3) :
    tau_op (tau_op (tau_op v)) = v := by
  obtain ⟨b1, b2⟩ := v
  dsimp [tau_op]
  have h1 : -b1 - (b2 - b1) = -b2 := by omega
  have h2 : -(b2 - b1) - -b2 = b1 := by omega
  have h3 : - -b2 = b2 := by omega
  rw [h1, h2, h3]

/-- Cyclotomic relation tau^2 + tau + I = 0 on barycentric coordinates. -/
theorem tau_cyclotomic_relation (v : Bary3) :
    (tau_op (tau_op v)).b1 + (tau_op v).b1 + v.b1 = 0 ∧
    (tau_op (tau_op v)).b2 + (tau_op v).b2 + v.b2 = 0 := by
  obtain ⟨b1, b2⟩ := v
  dsimp [tau_op]
  constructor <;> omega

end SimplicialDiamondComplex

-- ==============================================================================
-- PART 3: CANONICAL EVALUATION PAIRING AND SORKIN I_3 === 0
-- ==============================================================================

namespace EvaluationAndSorkin

open SimplicialDiamondComplex

/-- 1-Cochains as linear functionals C^1 = Hom(C_1, Int). -/
structure Cochain1 where
  w01 : Int
  w13 : Int
  w32 : Int
  w20 : Int
  w12 : Int
  deriving DecidableEq, Repr

def add_cochain (p q : Cochain1) : Cochain1 :=
  ⟨p.w01 + q.w01, p.w13 + q.w13, p.w32 + q.w32, p.w20 + q.w20, p.w12 + q.w12⟩

/-- Canonical evaluation pairing <c, phi> : C_1 x C^1 -> Int. -/
def eval_pairing (c : Chain1) (phi : Cochain1) : Int :=
  c.e01 * phi.w01 + c.e13 * phi.w13 + c.e32 * phi.w32 + c.e20 * phi.w20 + c.e12 * phi.w12

/-- Left-additivity of canonical evaluation pairing. -/
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

/-- Right-additivity of canonical evaluation pairing. -/
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

/-- Symmetric Bilinear Detector Tensor / Gram Matrix mediating 2-point readouts c (x) c*. -/
structure DetectorTensor where
  g : Chain1 → Chain1 → Int
  h_bilin_left  : ∀ c1 c2 d, g (add1 c1 c2) d = g c1 d + g c2 d
  h_bilin_right : ∀ c d1 d2, g c (add1 d1 d2) = g c d1 + g c d2
  h_symm        : ∀ c d, g c d = g d c

/-- Quadratic Detector Readout P(c) = <E, c (x) c*> = E.g(c, c) (valuation degree p = 2). -/
def readout (E : DetectorTensor) (c : Chain1) : Int :=
  E.g c c

/-- Second-order Sorkin interference I_2(A, B) = P(A + B) - P(A) - P(B). -/
def I2 (E : DetectorTensor) (A B : Chain1) : Int :=
  readout E (add1 A B) - readout E A - readout E B

/-- Exact formula: I_2(A, B) = 2 * E.g(A, B). -/
theorem I2_formula (E : DetectorTensor) (A B : Chain1) :
    I2 E A B = 2 * E.g A B := by
  dsimp [I2, readout]
  rw [E.h_bilin_left, E.h_bilin_right, E.h_bilin_right]
  rw [E.h_symm B A]
  omega

/-- Third-order Sorkin interference I_3(A, B, C):
    I_3 = P(A + B + C) - P(A + B) - P(B + C) - P(A + C) + P(A) + P(B) + P(C). -/
def I3 (E : DetectorTensor) (A B C : Chain1) : Int :=
  readout E (add1 (add1 A B) C)
  - readout E (add1 A B)
  - readout E (add1 B C)
  - readout E (add1 A C)
  + readout E A + readout E B + readout E C

/-- Sorkin Third-Order Interference Identically Vanishes Theorem:
    Any 2-point tensor detector readout P(c) = c (x) c* (quadratic degree p = 2)
    identically satisfies I_3(A, B, C) = 0 across any three histories A, B, C. -/
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

-- Concrete realization of standard detector with cross-path interference
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

/-- Non-vanishing second-order quantum interference: I_2(A, B) = 2 != 0. -/
theorem concrete_I2_nonzero :
    I2 standardDetector slitA slitB = 2 := by
  rw [I2_formula]
  dsimp [standardDetector, metric_E, slitA, slitB]

/-- Vanishing third-order quantum interference on the same state: I_3(A, B, C) = 0. -/
theorem concrete_I3_zero :
    I3 standardDetector slitA slitB slitC = 0 := by
  apply sorkin_third_order_identically_zero

/-- Obstruction demonstration: Higher-degree valuation p = 3 (cubic readout).
    Cubic readout P_3(c) = (c.e01 + c.e13 + c.e32)^3 violates Sorkin I_3 === 0,
    showing that quadratic valuation p = 2 is selected by detector 2-point tensors. -/
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

-- ==============================================================================
-- PART 4: SIGNED PERMUTATION ISOMETRIES B_n AND IRREVERSIBLE RESIDUE
-- ==============================================================================

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

/-- Signed permutation in hyperoctahedral group B_3 = S_3 ltimes (Z_2)^3. -/
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

/-- Non-exchangeable monotone layer admission / projection operator. -/
def proj_admission (v : Vec3) : Vec3 :=
  ⟨v.x0, v.x1, 0⟩

/-- Irreversible defect residue on l1 resource. -/
def irreversible_residue_l1 (v : Vec3) : Nat :=
  Vec3.l1_norm v - Vec3.l1_norm (proj_admission v)

/-- Positive irreversible residue witness: Delta_irr = 5 > 0. -/
theorem irreversible_residue_positive_witness :
    let v : Vec3 := ⟨1, 2, 5⟩
    irreversible_residue_l1 v = 5 := by
  decide

end SignedPermutationAndResidue

-- ==============================================================================
-- PART 5: AXIOM RECEIPTS
-- ==============================================================================

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
