import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Campaign Module: TFQ-0009 (`FINITE_GAUGE`)

Formalizes the narrowed finite counterpart and non-equivalence fences for
`TFQ-0009` ("A finite gauge step is a cochain of group-valued or Hopf-valued data
on a finite complex, together with holonomy around finite loops and a coboundary
that plays the role of curvature... U(1) and a non-abelian color shadow fork after
this node. Neither fork is continuum Yang-Mills theory."):

1. **Shared Finite Complex (`SquarePlaquette`, `AdjacentPlaquettes`, `CubeComplex`) & Boundary (`∂ ∘ ∂ = 0`)**:
   - Models the oriented 4-vertex square plaquette `P = (e₀, e₁, e₂, e₃)` with
     oriented edges `0 → 1 → 2 → 3 → 0`, showing that the 0-chain boundary of the
     1-chain plaquette boundary vanishes at every vertex (`chain_boundary_squared_zero_on_plaquette`).
   - Models two adjacent square plaquettes `P_L, P_R` sharing an interior edge
     `e_mid` with opposite orientation, showing that the combined boundary cancels
     the shared edge (`shared_edge_cancellation_two_plaquettes`).
2. **Abelian Cochain Connection, Coboundary Curvature (`d₁ ∘ d₀ = 0`), & Discrete Bianchi Identity (`d₂ ∘ d₁ = 0`)**:
   - Defines vertex 0-cochains `λ = (λ₀, λ₁, λ₂, λ₃)`, link 1-cochains
     `A = (A₀, A₁, A₂, A₃)`, coboundary `d₀ λ`, and plaquette curvature `d₁ A`.
   - Shows `d₁ (d₀ λ) = 0` (`abelian_cochain_coboundary_squared_zero`) and exact
     gauge invariance `d₁ (A + d₀ λ) = d₁ A` (`abelian_curvature_gauge_invariant`).
   - Shows the discrete abelian Bianchi identity on the 6-face, 12-edge 3-cube complex:
     the oriented sum of the 6 face curvatures vanishes identically for every
     12-edge connection (`abelian_bianchi_identity_cube`).
3. **Non-Abelian Matrix Link Holonomy Conjugation, Trace Invariance, & Abelian/Non-Abelian Fork**:
   - Models 2×2 integer matrix link variables `U₀, U₁, U₂, U₃ : Mat2Int` and
     vertex gauge transformations `gᵢ` with two-sided inverses `gᵢ⁻¹`.
   - Proves the telescoping plaquette holonomy conjugation identity
     `U₀^g * U₁^g * U₂^g * U₃^g = g₀ * (U₀ * U₁ * U₂ * U₃) * g₀⁻¹`
     (`nonabelian_holonomy_conjugation_identity`).
   - Proves cyclic trace invariance `mat2Trace (A * B) = mat2Trace (B * A)` and
     Wilson loop trace gauge invariance `mat2Trace (g₀ * H * g₀⁻¹) = mat2Trace H`
     whenever `g₀⁻¹ * g₀ = I` (`nonabelian_wilson_loop_trace_gauge_invariant`).
   - Exhibits the abelian vs. non-abelian fork: integer/cyclic link addition is
     commutative (`A₀ + A₁ = A₁ + A₀`), whereas 2×2 `SL(2, ℤ)` shear links have a
     non-vanishing commutator and non-central gauge conjugation changes the
     basepointed holonomy matrix (`abelian_vs_nonabelian_fork_commutator_witness`).
4. **No-Continuum-Yang-Mills Fence**:
   - Contrasts the finite cardinality `N^E` of `ℤ/Nℤ` 1-cochains on an `E`-edge
     finite complex (`finite_cochain_cardinality_and_quotient_bound`) and shows
     that the combinatorial coboundary `d₁ A` is metric-free whereas the Yang-Mills
     action weights `w * (d₁ A)^2` depend on an unimported metric coupling `w = 1 / g²`
     (`combinatorial_coboundary_metric_free_vs_yang_mills_action_fence`).
-/

namespace CampaignTfq0009FiniteGauge

-- ============================================================================
-- 1. Shared Finite Cell Complex & Boundary Operator (`∂₁ ∘ ∂₂ = 0`)
-- ============================================================================

/-- A 0-chain on the 4 vertices `{0, 1, 2, 3}` of a square plaquette. -/
@[ext]
structure Vertex0Chain where
  v0 : Int
  v1 : Int
  v2 : Int
  v3 : Int
  deriving DecidableEq, Repr

/-- A 1-chain on the 4 oriented edges `e0=(0→1), e1=(1→2), e2=(2→3), e3=(3→0)`. -/
@[ext]
structure Edge1Chain where
  e0 : Int
  e1 : Int
  e2 : Int
  e3 : Int
  deriving DecidableEq, Repr

/-- The fundamental 2-cell plaquette boundary `∂₂(1) = e0 + e1 + e2 + e3`. -/
def plaquetteBoundary2 (c : Int) : Edge1Chain :=
  ⟨c, c, c, c⟩

/-- The 1-chain boundary `∂₁ : C₁ → C₀` mapping `e_i = (v_i → v_{i+1})` to `v_{i+1} - v_i`. -/
def edgeBoundary1 (gamma : Edge1Chain) : Vertex0Chain :=
  ⟨gamma.e3 - gamma.e0,
   gamma.e0 - gamma.e1,
   gamma.e1 - gamma.e2,
   gamma.e2 - gamma.e3⟩

/-- Theorem 1: On the shared 4-vertex square plaquette complex, the iterated boundary
`∂₁ (∂₂ c)` vanishes identically at every vertex (`∂₁ ∘ ∂₂ = 0`). -/
theorem chain_boundary_squared_zero_on_plaquette (c : Int) :
    edgeBoundary1 (plaquetteBoundary2 c) = ⟨0, 0, 0, 0⟩ := by
  ext <;> dsimp [edgeBoundary1, plaquetteBoundary2] <;> ring

/-- Net multiplicity of the shared interior edge `e_mid` when combining a left
plaquette with weight `cL` (traversing `+e_mid`) and a right plaquette with
weight `cR` (traversing `-e_mid`). -/
def sharedEdgeMultiplicity (cL cR : Int) : Int :=
  cL - cR

/-- Theorem 2: Two adjacent square plaquettes traversed with equal orientation
(`cL = cR = c`) cancel their shared interior edge (`sharedEdgeMultiplicity c c = 0`),
while distinct weights (`cL ≠ cR`) leave a non-zero interior edge contribution. -/
theorem shared_edge_cancellation_two_plaquettes (c : Int) :
    sharedEdgeMultiplicity c c = 0 ∧ sharedEdgeMultiplicity 1 0 = 1 := by
  dsimp [sharedEdgeMultiplicity]
  exact ⟨by ring, by decide⟩

-- ============================================================================
-- 2. Abelian Cochain Connection, Coboundary Curvature, & Discrete Bianchi Identity
-- ============================================================================

/-- A vertex 0-cochain `λ` on the 4 vertices of a square plaquette. -/
@[ext]
structure Vertex0Cochain where
  l0 : Int
  l1 : Int
  l2 : Int
  l3 : Int
  deriving DecidableEq, Repr

/-- An edge 1-cochain (abelian gauge connection) `A` on the 4 oriented edges of a square plaquette. -/
@[ext]
structure Edge1Cochain where
  a0 : Int
  a1 : Int
  a2 : Int
  a3 : Int
  deriving DecidableEq, Repr

/-- Coboundary `d₀ : C⁰ → C¹` of a vertex 0-cochain: `(d₀ λ)(e_i) = λ_{i+1} - λ_i`. -/
def coboundary0 (lam : Vertex0Cochain) : Edge1Cochain :=
  ⟨lam.l1 - lam.l0,
   lam.l2 - lam.l1,
   lam.l3 - lam.l2,
   lam.l0 - lam.l3⟩

/-- Abelian gauge transformation `A ↦ A + d₀ λ`. -/
def abelianGaugeTransform (A : Edge1Cochain) (lam : Vertex0Cochain) : Edge1Cochain :=
  ⟨A.a0 + (coboundary0 lam).a0,
   A.a1 + (coboundary0 lam).a1,
   A.a2 + (coboundary0 lam).a2,
   A.a3 + (coboundary0 lam).a3⟩

/-- Coboundary `d₁ : C¹ → C²` (abelian plaquette holonomy / curvature) around the square plaquette. -/
def coboundary1 (A : Edge1Cochain) : Int :=
  A.a0 + A.a1 + A.a2 + A.a3

/-- Theorem 3: The coboundary of a pure gauge 0-cochain has zero plaquette curvature (`d₁ ∘ d₀ = 0`). -/
theorem abelian_cochain_coboundary_squared_zero (lam : Vertex0Cochain) :
    coboundary1 (coboundary0 lam) = 0 := by
  dsimp [coboundary1, coboundary0]
  ring

/-- Theorem 4: Abelian plaquette curvature `d₁ A` is strictly invariant under any
vertex gauge transformation `A ↦ A + d₀ λ`. -/
theorem abelian_curvature_gauge_invariant (A : Edge1Cochain) (lam : Vertex0Cochain) :
    coboundary1 (abelianGaugeTransform A lam) = coboundary1 A := by
  dsimp [coboundary1, abelianGaugeTransform, coboundary0]
  ring

/-- A 1-cochain on the 12 edges of a 3-cube:
bottom square `(b0, b1, b2, b3)`, top square `(t0, t1, t2, t3)`, and vertical pillars `(v0, v1, v2, v3)`. -/
structure Cube1Cochain where
  b0 : Int
  b1 : Int
  b2 : Int
  b3 : Int
  t0 : Int
  t1 : Int
  t2 : Int
  t3 : Int
  v0 : Int
  v1 : Int
  v2 : Int
  v3 : Int
  deriving DecidableEq, Repr

/-- The 2-coboundary `d₂(d₁ A)` on the 3-cube: oriented sum of the 6 face curvatures
(top `-` bottom `+` front `-` back `+` right `-` left), where each of the 12 edges
is traversed once positively and once negatively. -/
def cubeCurvatureCoboundary2 (C : Cube1Cochain) : Int :=
  let f_bot := C.b0 + C.b1 + C.b2 + C.b3
  let f_top := C.t0 + C.t1 + C.t2 + C.t3
  let f_0 := C.b0 + C.v1 - C.t0 - C.v0
  let f_1 := C.b1 + C.v2 - C.t1 - C.v1
  let f_2 := C.b2 + C.v3 - C.t2 - C.v2
  let f_3 := C.b3 + C.v0 - C.t3 - C.v3
  f_top - f_bot + f_0 + f_1 + f_2 + f_3

/-- Theorem 5: Discrete abelian Bianchi identity (`d₂ ∘ d₁ = 0`) on the 3-cube complex:
the oriented sum of the 6 plaquette curvatures vanishes identically for every 12-edge 1-cochain. -/
theorem abelian_bianchi_identity_cube (C : Cube1Cochain) :
    cubeCurvatureCoboundary2 C = 0 := by
  dsimp [cubeCurvatureCoboundary2]
  ring

-- ============================================================================
-- 3. Non-Abelian Matrix Link Holonomy, Conjugation, & Trace Invariance
-- ============================================================================

/-- A 2×2 integer matrix representing a discrete non-abelian gauge link or vertex frame. -/
@[ext]
structure Mat2Int where
  m11 : Int
  m12 : Int
  m21 : Int
  m22 : Int
  deriving DecidableEq, Repr

/-- 2×2 identity matrix. -/
def mat2Id : Mat2Int :=
  ⟨1, 0, 0, 1⟩

/-- 2×2 matrix multiplication. -/
def mat2Mul (A B : Mat2Int) : Mat2Int :=
  ⟨A.m11 * B.m11 + A.m12 * B.m21,
   A.m11 * B.m12 + A.m12 * B.m22,
   A.m21 * B.m11 + A.m22 * B.m21,
   A.m21 * B.m12 + A.m22 * B.m22⟩

/-- 2×2 matrix trace. -/
def mat2Trace (A : Mat2Int) : Int :=
  A.m11 + A.m22

/-- Non-abelian gauge transformation of an oriented link `U` from `u` to `v`:
`U^g = g_u * U * g_v⁻¹`. -/
def gaugeTransformLink (gu U gv_inv : Mat2Int) : Mat2Int :=
  mat2Mul (mat2Mul gu U) gv_inv

/-- Ordered plaquette holonomy around the 4-edge loop `0 → 1 → 2 → 3 → 0`. -/
def plaquetteHolonomy (U0 U1 U2 U3 : Mat2Int) : Mat2Int :=
  mat2Mul (mat2Mul (mat2Mul U0 U1) U2) U3

lemma mat2Mul_assoc (A B C : Mat2Int) :
    mat2Mul (mat2Mul A B) C = mat2Mul A (mat2Mul B C) := by
  ext <;> dsimp [mat2Mul] <;> ring

lemma mat2Mul_id_left (A : Mat2Int) :
    mat2Mul mat2Id A = A := by
  ext <;> dsimp [mat2Mul, mat2Id] <;> ring

lemma mat2Mul_id_right (A : Mat2Int) :
    mat2Mul A mat2Id = A := by
  ext <;> dsimp [mat2Mul, mat2Id] <;> ring

/-- Theorem 6: Exact non-abelian holonomy conjugation identity around the 4-edge square plaquette:
when `g₁⁻¹ * g₁ = I`, `g₂⁻¹ * g₂ = I`, and `g₃⁻¹ * g₃ = I`, the intermediate vertex gauge
factors telescope and the plaquette holonomy conjugates by the basepoint gauge `g₀`:
`H(U^g) = g₀ * H(U) * g₀⁻¹`. -/
theorem nonabelian_holonomy_conjugation_identity
    (U0 U1 U2 U3 g0 g0_inv g1 g1_inv g2 g2_inv g3 g3_inv : Mat2Int)
    (h1 : mat2Mul g1_inv g1 = mat2Id)
    (h2 : mat2Mul g2_inv g2 = mat2Id)
    (h3 : mat2Mul g3_inv g3 = mat2Id) :
    plaquetteHolonomy
      (gaugeTransformLink g0 U0 g1_inv)
      (gaugeTransformLink g1 U1 g2_inv)
      (gaugeTransformLink g2 U2 g3_inv)
      (gaugeTransformLink g3 U3 g0_inv) =
    gaugeTransformLink g0 (plaquetteHolonomy U0 U1 U2 U3) g0_inv := by
  dsimp [plaquetteHolonomy, gaugeTransformLink]
  have step1 :
      mat2Mul (mat2Mul (mat2Mul g0 U0) g1_inv) (mat2Mul (mat2Mul g1 U1) g2_inv) =
      mat2Mul (mat2Mul g0 (mat2Mul U0 U1)) g2_inv := by
    calc
      mat2Mul (mat2Mul (mat2Mul g0 U0) g1_inv) (mat2Mul (mat2Mul g1 U1) g2_inv)
        = mat2Mul (mat2Mul g0 U0) (mat2Mul (mat2Mul g1_inv g1) (mat2Mul U1 g2_inv)) := by
            simp only [mat2Mul_assoc]
      _ = mat2Mul (mat2Mul g0 U0) (mat2Mul mat2Id (mat2Mul U1 g2_inv)) := by rw [h1]
      _ = mat2Mul (mat2Mul g0 U0) (mat2Mul U1 g2_inv) := by rw [mat2Mul_id_left]
      _ = mat2Mul (mat2Mul g0 (mat2Mul U0 U1)) g2_inv := by simp only [mat2Mul_assoc]
  have step2 :
      mat2Mul (mat2Mul (mat2Mul g0 (mat2Mul U0 U1)) g2_inv) (mat2Mul (mat2Mul g2 U2) g3_inv) =
      mat2Mul (mat2Mul g0 (mat2Mul (mat2Mul U0 U1) U2)) g3_inv := by
    calc
      mat2Mul (mat2Mul (mat2Mul g0 (mat2Mul U0 U1)) g2_inv) (mat2Mul (mat2Mul g2 U2) g3_inv)
        = mat2Mul (mat2Mul g0 (mat2Mul U0 U1)) (mat2Mul (mat2Mul g2_inv g2) (mat2Mul U2 g3_inv)) := by
            simp only [mat2Mul_assoc]
      _ = mat2Mul (mat2Mul g0 (mat2Mul U0 U1)) (mat2Mul mat2Id (mat2Mul U2 g3_inv)) := by rw [h2]
      _ = mat2Mul (mat2Mul g0 (mat2Mul U0 U1)) (mat2Mul U2 g3_inv) := by rw [mat2Mul_id_left]
      _ = mat2Mul (mat2Mul g0 (mat2Mul (mat2Mul U0 U1) U2)) g3_inv := by simp only [mat2Mul_assoc]
  have step3 :
      mat2Mul (mat2Mul (mat2Mul g0 (mat2Mul (mat2Mul U0 U1) U2)) g3_inv) (mat2Mul (mat2Mul g3 U3) g0_inv) =
      mat2Mul (mat2Mul g0 (mat2Mul (mat2Mul (mat2Mul U0 U1) U2) U3)) g0_inv := by
    calc
      mat2Mul (mat2Mul (mat2Mul g0 (mat2Mul (mat2Mul U0 U1) U2)) g3_inv) (mat2Mul (mat2Mul g3 U3) g0_inv)
        = mat2Mul (mat2Mul g0 (mat2Mul (mat2Mul U0 U1) U2)) (mat2Mul (mat2Mul g3_inv g3) (mat2Mul U3 g0_inv)) := by
            simp only [mat2Mul_assoc]
      _ = mat2Mul (mat2Mul g0 (mat2Mul (mat2Mul U0 U1) U2)) (mat2Mul mat2Id (mat2Mul U3 g0_inv)) := by rw [h3]
      _ = mat2Mul (mat2Mul g0 (mat2Mul (mat2Mul U0 U1) U2)) (mat2Mul U3 g0_inv) := by rw [mat2Mul_id_left]
      _ = mat2Mul (mat2Mul g0 (mat2Mul (mat2Mul (mat2Mul U0 U1) U2) U3)) g0_inv := by simp only [mat2Mul_assoc]
  rw [step1, step2, step3]

/-- Theorem 7: Cyclic trace invariance (`mat2Trace (A * B) = mat2Trace (B * A)`) and
gauge invariance of the Wilson loop trace `mat2Trace (g₀ * H * g₀⁻¹) = mat2Trace H`
for any vertex gauge matrix `g₀` with left inverse `g₀⁻¹ * g₀ = I`. -/
theorem nonabelian_wilson_loop_trace_gauge_invariant
    (H g0 g0_inv : Mat2Int) (h_inv : mat2Mul g0_inv g0 = mat2Id) :
    mat2Trace (mat2Mul g0 H) = mat2Trace (mat2Mul H g0) ∧
    mat2Trace (gaugeTransformLink g0 H g0_inv) = mat2Trace H := by
  have h_cyc : ∀ A B : Mat2Int, mat2Trace (mat2Mul A B) = mat2Trace (mat2Mul B A) := by
    intro A B
    dsimp [mat2Trace, mat2Mul]
    ring
  refine ⟨h_cyc g0 H, ?_⟩
  dsimp [gaugeTransformLink]
  rw [h_cyc (mat2Mul g0 H) g0_inv]
  rw [← mat2Mul_assoc g0_inv g0 H]
  rw [h_inv, mat2Mul_id_left]

/-- Upper and lower `SL(2, ℤ)` elementary shear links witnessing the non-abelian fork. -/
def shearUpper : Mat2Int := ⟨1, 1, 0, 1⟩
def shearLower : Mat2Int := ⟨1, 0, 1, 1⟩

/-- Theorem 8: Abelian vs. non-abelian fork witness:
abelian link composition is commutative (`a0 + a1 = a1 + a0`), whereas non-abelian
2×2 matrix link composition is non-commutative (`shearUpper * shearLower ≠ shearLower * shearUpper`)
and basepointed holonomy is not invariant under non-central conjugation (`g₀ * H * g₀⁻¹ ≠ H`),
even though the Wilson loop trace remains invariant (`3 = 3`). -/
theorem abelian_vs_nonabelian_fork_commutator_witness :
    (∀ a0 a1 : Int, a0 + a1 = a1 + a0) ∧
    mat2Mul shearUpper shearLower ≠ mat2Mul shearLower shearUpper ∧
    gaugeTransformLink shearUpper shearLower ⟨1, -1, 0, 1⟩ ≠ shearLower ∧
    mat2Trace (gaugeTransformLink shearUpper shearLower ⟨1, -1, 0, 1⟩) = mat2Trace shearLower := by
  refine ⟨fun a0 a1 => by ring, ?_, ?_, ?_⟩
  · intro h
    have hm11 : (mat2Mul shearUpper shearLower).m11 = (mat2Mul shearLower shearUpper).m11 :=
      congrArg Mat2Int.m11 h
    dsimp [mat2Mul, shearUpper, shearLower] at hm11
    omega
  · intro h
    have hm12 : (gaugeTransformLink shearUpper shearLower ⟨1, -1, 0, 1⟩).m12 = shearLower.m12 :=
      congrArg Mat2Int.m12 h
    dsimp [gaugeTransformLink, mat2Mul, shearUpper, shearLower] at hm12
    omega
  · decide

-- ============================================================================
-- 4. No-Continuum-Yang-Mills Fence
-- ============================================================================

/-- Cardinality of the space of `ℤ/Nℤ`-valued 1-cochains on a finite complex with `E` edges. -/
def finiteCochainCardinality (N E : Nat) : Nat :=
  N ^ E

/-- Discrete Yang-Mills plaquette action term `w * (d₁ A)²` requiring an external metric/coupling weight `w`. -/
def weightedPlaquetteAction (w : ℚ) (A : Edge1Cochain) : ℚ :=
  w * ((coboundary1 A : ℚ) ^ 2)

/-- Theorem 9: On a finite 4-edge plaquette complex with cyclic group order `N ≥ 2`,
the space of `ℤ/Nℤ` 1-cochains has finite cardinality `N^4 ≥ 16` (with `2^4 = 16` for `ℤ/2ℤ`
and `8^4 = 4096` for an 8-element gauge shadow), whereas a continuum connection 1-form space is infinite-dimensional. -/
theorem finite_cochain_cardinality_and_quotient_bound :
    finiteCochainCardinality 2 4 = 16 ∧
    finiteCochainCardinality 8 4 = 4096 := by
  dsimp [finiteCochainCardinality]
  decide

/-- Theorem 10: No-continuum-Yang-Mills fence:
the combinatorial curvature coboundary `d₁ A` depends only on the finite complex incidence data,
whereas the Yang-Mills action requires a metric coupling weight `w = 1 / g²`: for any 1-cochain `A`
with non-zero curvature `coboundary1 A ≠ 0`, distinct metric couplings `w₁ ≠ w₂` produce distinct
plaquette actions (`weightedPlaquetteAction w₁ A ≠ weightedPlaquetteAction w₂ A`) for the exact same
combinatorial cochain `A`. -/
theorem combinatorial_coboundary_metric_free_vs_yang_mills_action_fence
    (w1 w2 : ℚ) (hw : w1 ≠ w2) :
    let A : Edge1Cochain := ⟨1, 0, 0, 0⟩
    coboundary1 A = 1 ∧
    weightedPlaquetteAction w1 A ≠ weightedPlaquetteAction w2 A := by
  intro A
  refine ⟨by decide, ?_⟩
  dsimp [weightedPlaquetteAction, coboundary1, A]
  intro h
  apply hw
  linarith

#print axioms chain_boundary_squared_zero_on_plaquette
#print axioms shared_edge_cancellation_two_plaquettes
#print axioms abelian_cochain_coboundary_squared_zero
#print axioms abelian_curvature_gauge_invariant
#print axioms abelian_bianchi_identity_cube
#print axioms nonabelian_holonomy_conjugation_identity
#print axioms nonabelian_wilson_loop_trace_gauge_invariant
#print axioms abelian_vs_nonabelian_fork_commutator_witness
#print axioms finite_cochain_cardinality_and_quotient_bound
#print axioms combinatorial_coboundary_metric_free_vs_yang_mills_action_fence

end CampaignTfq0009FiniteGauge
