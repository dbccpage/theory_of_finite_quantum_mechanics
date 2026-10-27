import Mathlib.Data.Rat.Defs
import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-!
# (`TFQ-0016`): B₂(ℚ) Semidirect Factorization, Two-Stage Dressing, and Discrete Curvature

AuthorityEffect: None.

Formalization of the QM-213 mathematical structure:
1. Semidirect factorization of invertible upper-triangular matrices B₂(ℚ) = T ⋉ N into
   a diagonal quotient torus T and the normal unipotent subgroup N.
2. Two-stage hierarchical non-Abelian dressing on the 4-vertex, 5-edge diamond graph:
   - Stage 1 dressing by a conjugate of the tree unipotent leaves tree edges diagonal
     and preserves the quotient projection π_T on all 5 edges.
   - Stage 2 torus dressing reproduces the tree gauge residual tree_gauge_indexed.residual.
3. On the extended diamond poset P₅, discrete curvature is the incidence combination
   K(A) = bA + A ⌣ A, satisfying exact gauge covariance, b² = 0, and the discrete Bianchi identity.
4. The arithmetic comparison `(2 : ℕ) ≠ 3`. This module does not prove a statement
   about SU(3) representations. A search of `FiniteQM.lean` for a QM-213 twin is
   `checks/independent/tfq-0016.py`, not a Lean theorem.
-/

namespace B2SemidirectDressing

/-- Representation of an upper-triangular 2×2 matrix over ℚ:
    [[d1, b], [0, d2]]. -/
@[ext]
structure UpperTri2 where
  d1 : ℚ
  b  : ℚ
  d2 : ℚ
  deriving DecidableEq, Repr

namespace UpperTri2

instance : Mul UpperTri2 where
  mul x y := ⟨x.d1 * y.d1, x.d1 * y.b + x.b * y.d2, x.d2 * y.d2⟩

instance : One UpperTri2 where
  one := ⟨1, 0, 1⟩

@[simp] theorem mul_d1 (x y : UpperTri2) : (x * y).d1 = x.d1 * y.d1 := rfl
@[simp] theorem mul_b (x y : UpperTri2) : (x * y).b = x.d1 * y.b + x.b * y.d2 := rfl
@[simp] theorem mul_d2 (x y : UpperTri2) : (x * y).d2 = x.d2 * y.d2 := rfl
@[simp] theorem one_d1 : (1 : UpperTri2).d1 = 1 := rfl
@[simp] theorem one_b : (1 : UpperTri2).b = 0 := rfl
@[simp] theorem one_d2 : (1 : UpperTri2).d2 = 1 := rfl

theorem mul_assoc (x y z : UpperTri2) : (x * y) * z = x * (y * z) := by
  ext <;> dsimp <;> ring

theorem one_mul (x : UpperTri2) : 1 * x = x := by
  ext <;> dsimp <;> ring

theorem mul_one (x : UpperTri2) : x * 1 = x := by
  ext <;> dsimp <;> ring

lemma mul_sandwich_assoc (A B C D E : UpperTri2) :
    A * (B * C * D) * E = (A * B) * C * (D * E) := by
  ext <;> dsimp <;> ring

/-- Invertibility condition: non-zero diagonal entries. -/
def IsInvertible (x : UpperTri2) : Prop := x.d1 ≠ 0 ∧ x.d2 ≠ 0

def inv (x : UpperTri2) : UpperTri2 :=
  ⟨x.d1⁻¹, -x.b / (x.d1 * x.d2), x.d2⁻¹⟩

theorem mul_inv_cancel (x : UpperTri2) (h : IsInvertible x) : x * inv x = 1 := by
  rcases h with ⟨hd1, hd2⟩
  ext
  · rw [mul_d1]
    dsimp [inv]
    exact mul_inv_cancel₀ hd1
  · rw [mul_b]
    dsimp [inv]
    have h1 : x.d1 * (-x.b / (x.d1 * x.d2)) = -x.b / x.d2 := by
      calc x.d1 * (-x.b / (x.d1 * x.d2))
        _ = (x.d1 * (-x.b)) / (x.d1 * x.d2) := by ring
        _ = (-x.b) / x.d2 := mul_div_mul_left (-x.b) x.d2 hd1
        _ = -x.b / x.d2 := rfl
    rw [h1]
    have h2 : x.b * x.d2⁻¹ = x.b / x.d2 := by ring
    rw [h2]
    ring
  · rw [mul_d2]
    dsimp [inv]
    exact mul_inv_cancel₀ hd2

theorem inv_mul_cancel (x : UpperTri2) (h : IsInvertible x) : inv x * x = 1 := by
  rcases h with ⟨hd1, hd2⟩
  ext
  · rw [mul_d1]
    dsimp [inv]
    exact inv_mul_cancel₀ hd1
  · rw [mul_b]
    dsimp [inv]
    have h1 : (-x.b / (x.d1 * x.d2)) * x.d2 = -x.b / x.d1 := by
      calc (-x.b / (x.d1 * x.d2)) * x.d2
        _ = (-x.b * x.d2) / (x.d1 * x.d2) := by ring
        _ = (-x.b) / x.d1 := mul_div_mul_right (-x.b) x.d1 hd2
        _ = -x.b / x.d1 := rfl
    rw [h1]
    have h2 : x.d1⁻¹ * x.b = x.b / x.d1 := by ring
    rw [h2]
    ring
  · rw [mul_d2]
    dsimp [inv]
    exact inv_mul_cancel₀ hd2

theorem inv_isInvertible (x : UpperTri2) (h : IsInvertible x) : IsInvertible (inv x) := by
  constructor
  · exact inv_ne_zero h.1
  · exact inv_ne_zero h.2

/-- Diagonal torus subgroup T ⊂ B₂(ℚ). -/
def IsTorus (x : UpperTri2) : Prop := x.b = 0

/-- Unit upper-triangular normal subgroup N ⊲ B₂(ℚ). -/
def IsUnipotent (x : UpperTri2) : Prop := x.d1 = 1 ∧ x.d2 = 1

/-- Projection to the diagonal torus quotient T ≅ B₂(ℚ)/N. -/
def torusProj (x : UpperTri2) : UpperTri2 := ⟨x.d1, 0, x.d2⟩

/-- Right unipotent part n(M) ∈ N. -/
def unipotentPart (x : UpperTri2) : UpperTri2 :=
  ⟨1, x.b / x.d1, 1⟩

theorem torusProj_isTorus (x : UpperTri2) : IsTorus (torusProj x) := rfl

theorem torusProj_isInvertible (x : UpperTri2) (h : IsInvertible x) : IsInvertible (torusProj x) := h

theorem unipotentPart_isUnipotent (x : UpperTri2) :
    IsUnipotent (unipotentPart x) := ⟨rfl, rfl⟩

theorem unipotentPart_isInvertible (x : UpperTri2) :
    IsInvertible (unipotentPart x) := by
  dsimp [IsInvertible, unipotentPart]
  norm_num

theorem torus_mul_torus (x y : UpperTri2) (hx : IsTorus x) (hy : IsTorus y) :
    IsTorus (x * y) := by
  dsimp [IsTorus] at *
  calc (x * y).b = x.d1 * y.b + x.b * y.d2 := rfl
    _ = x.d1 * 0 + 0 * y.d2 := by rw [hx, hy]
    _ = 0 := by ring

theorem torus_inv (x : UpperTri2) (hx : IsTorus x) :
    IsTorus (inv x) := by
  dsimp [IsTorus] at *
  dsimp [inv]
  rw [hx]
  ring

/-- Part 1: Semidirect Factorization B₂(ℚ) = T ⋉ N.
    Every invertible upper-triangular matrix factors into a diagonal torus element
    and a unipotent factor in N. -/
theorem b2_semidirect_factorization (x : UpperTri2) (h : IsInvertible x) :
    x = torusProj x * unipotentPart x := by
  ext
  · rw [mul_d1]
    dsimp [torusProj, unipotentPart]; ring
  · rw [mul_b]
    dsimp [torusProj, unipotentPart]
    have : x.d1 * (x.b / x.d1) + 0 * 1 = x.b := by
      rw [zero_mul, add_zero, mul_div_cancel₀ _ h.1]
    exact this.symm
  · rw [mul_d2]
    dsimp [torusProj, unipotentPart]; ring

/-- Uniqueness of the semidirect factorization M = D * n. -/
theorem b2_factorization_unique (x D n : UpperTri2) (hD : IsTorus D) (hn : IsUnipotent n)
    (h_prod : x = D * n) (hx : IsInvertible x) :
    D = torusProj x ∧ n = unipotentPart x := by
  have hd1 : x.d1 = D.d1 * n.d1 := by rw [h_prod, mul_d1]
  have h_b : x.b = D.d1 * n.b + D.b * n.d2 := by rw [h_prod, mul_b]
  have hd2 : x.d2 = D.d2 * n.d2 := by rw [h_prod, mul_d2]
  rcases hn with ⟨hn1, hn2⟩
  have hd1_eq : D.d1 * n.d1 = D.d1 := by rw [hn1, _root_.mul_one]
  have hd2_eq : D.d2 * n.d2 = D.d2 := by rw [hn2, _root_.mul_one]
  rw [hd1_eq] at hd1
  rw [hd2_eq] at hd2
  rw [hD, zero_mul, add_zero] at h_b
  constructor
  · ext
    · exact hd1.symm
    · dsimp [torusProj]
      exact hD.trans rfl
    · exact hd2.symm
  · ext
    · dsimp [unipotentPart]
      exact hn1.trans rfl
    · dsimp [unipotentPart]
      rw [← hd1] at h_b
      calc n.b = (x.d1 * n.b) / x.d1 := (mul_div_cancel_left₀ n.b hx.1).symm
        _ = x.b / x.d1 := by rw [← h_b]
    · dsimp [unipotentPart]
      exact hn2.trans rfl

/-- Normality of N ⊲ B₂(ℚ): conjugation of any unipotent element by any invertible
    Borel matrix produces a unipotent element in N. -/
theorem unipotent_subgroup_normal (M n : UpperTri2) (hM : IsInvertible M) (hn : IsUnipotent n) :
    IsUnipotent (M * n * inv M) := by
  rcases hn with ⟨hn1, hn2⟩
  constructor
  · rw [mul_d1, mul_d1]
    dsimp [inv]
    calc M.d1 * n.d1 * M.d1⁻¹ = M.d1 * 1 * M.d1⁻¹ := by rw [hn1]
      _ = M.d1 * M.d1⁻¹ := by ring
      _ = 1 := mul_inv_cancel₀ hM.1
  · rw [mul_d2, mul_d2]
    dsimp [inv]
    calc M.d2 * n.d2 * M.d2⁻¹ = M.d2 * 1 * M.d2⁻¹ := by rw [hn2]
      _ = M.d2 * M.d2⁻¹ := by ring
      _ = 1 := mul_inv_cancel₀ hM.2

/-- Preservation of the diagonal quotient projection under unipotent multiplication. -/
theorem torusProj_unipotent_invariance (M u1 u2 : UpperTri2)
    (hu1 : IsUnipotent u1) (hu2 : IsUnipotent u2) :
    torusProj (u1 * M * u2) = torusProj M := by
  rcases hu1 with ⟨hu1_d1, hu1_d2⟩
  rcases hu2 with ⟨hu2_d1, hu2_d2⟩
  ext
  · rw [torusProj, torusProj, mul_d1, mul_d1]
    dsimp
    calc u1.d1 * M.d1 * u2.d1 = 1 * M.d1 * 1 := by rw [hu1_d1, hu2_d1]
      _ = M.d1 := by ring
  · rfl
  · rw [torusProj, torusProj, mul_d2, mul_d2]
    dsimp
    calc u1.d2 * M.d2 * u2.d2 = 1 * M.d2 * 1 := by rw [hu1_d2, hu2_d2]
      _ = M.d2 := by ring

end UpperTri2

/-!
### Part 2: Two-Stage Hierarchical Dressing on the 5-Edge Diamond Cell Complex
-/

section DiamondComplex

open UpperTri2

/-- Vertices of the diamond complex: V = {0, 1, 2, 3}. -/
abbrev V4 := Fin 4

/-- Edges of the diamond complex:
    e0 = (0, 1) [tree]
    e1 = (1, 2) [cotree chord]
    e2 = (0, 2) [tree]
    e3 = (2, 3) [tree]
    e4 = (1, 3) [cotree chord] -/
abbrev E5 := Fin 5

def edgeSource : E5 → V4
  | 0 => 0
  | 1 => 1
  | 2 => 0
  | 3 => 2
  | 4 => 1

def edgeTarget : E5 → V4
  | 0 => 1
  | 1 => 2
  | 2 => 2
  | 3 => 3
  | 4 => 3

/-- Spanning tree T = {e0, e2, e3}. -/
def isTreeEdge : E5 → Prop
  | 0 => True
  | 1 => False
  | 2 => True
  | 3 => True
  | 4 => False

/-- Root-to-vertex transport along tree edges:
    T(0) = 1
    T(1) = U(0)
    T(2) = U(2)
    T(3) = U(3) * U(2) -/
def treeTransport (U : E5 → UpperTri2) : V4 → UpperTri2
  | 0 => 1
  | 1 => U 0
  | 2 => U 2
  | 3 => U 3 * U 2

theorem treeTransport_invertible (U : E5 → UpperTri2) (hU : ∀ e, IsInvertible (U e)) :
    ∀ v, IsInvertible (treeTransport U v)
  | 0 => by
    dsimp [treeTransport, IsInvertible]
    decide
  | 1 => hU 0
  | 2 => hU 2
  | 3 => ⟨mul_ne_zero (hU 3).1 (hU 2).1, mul_ne_zero (hU 3).2 (hU 2).2⟩

/-- Diagonal torus part of tree transport. -/
def D_tree (U : E5 → UpperTri2) (v : V4) : UpperTri2 :=
  torusProj (treeTransport U v)

/-- Unipotent part of tree transport. -/
def N_tree (U : E5 → UpperTri2) (v : V4) : UpperTri2 :=
  unipotentPart (treeTransport U v)

/-- Stage 1 dressing field: u_N(v) = D(v) * N_tree(v)⁻¹ * D(v)⁻¹. -/
def u_N (U : E5 → UpperTri2) (v : V4) : UpperTri2 :=
  ⟨1, -(treeTransport U v).b / (treeTransport U v).d2, 1⟩

/-- Stage 1 dressing field lies in the normal unipotent subgroup N. -/
theorem u_N_isUnipotent (U : E5 → UpperTri2) (v : V4) :
    IsUnipotent (u_N U v) := ⟨rfl, rfl⟩

theorem u_N_isInvertible (U : E5 → UpperTri2) (v : V4) :
    IsInvertible (u_N U v) := by
  dsimp [IsInvertible, u_N]
  norm_num

theorem u_N_inv_explicit (U : E5 → UpperTri2) (v : V4) :
    inv (u_N U v) = ⟨1, (treeTransport U v).b / (treeTransport U v).d2, 1⟩ := by
  ext
  · dsimp [inv, u_N]; ring
  · dsimp [inv, u_N]; ring
  · dsimp [inv, u_N]; ring

theorem u_N_zero (U : E5 → UpperTri2) :
    u_N U 0 = 1 := by
  ext
  · rfl
  · dsimp [u_N, treeTransport]; ring
  · rfl

theorem u_N_zero_inv (U : E5 → UpperTri2) :
    inv (u_N U 0) = 1 := by
  rw [u_N_zero]
  ext
  · dsimp [inv]; norm_num
  · dsimp [inv]; ring
  · dsimp [inv]; norm_num

/-- Key structural identity: u_N(v) * T(v) = D(v). -/
theorem u_N_mul_treeTransport (U : E5 → UpperTri2) (hU : ∀ e, IsInvertible (U e)) (v : V4) :
    u_N U v * treeTransport U v = D_tree U v := by
  have hd2 := (treeTransport_invertible U hU v).2
  ext
  · rw [mul_d1]
    dsimp [u_N, D_tree, torusProj]
    ring
  · rw [mul_b]
    dsimp [u_N, D_tree, torusProj]
    have : (-(treeTransport U v).b / (treeTransport U v).d2) * (treeTransport U v).d2 =
           -(treeTransport U v).b := div_mul_cancel₀ _ hd2
    calc 1 * (treeTransport U v).b + (-(treeTransport U v).b / (treeTransport U v).d2) * (treeTransport U v).d2
      _ = (treeTransport U v).b + -(treeTransport U v).b := by rw [this, _root_.one_mul]
      _ = 0 := by ring
  · rw [mul_d2]
    dsimp [u_N, D_tree, torusProj]
    ring

/-- Stage 1 dressed connection: U⁽¹⁾_e = u_N(target e) * U_e * u_N(source e)⁻¹. -/
def U_stage1 (U : E5 → UpperTri2) (e : E5) : UpperTri2 :=
  u_N U (edgeTarget e) * U e * inv (u_N U (edgeSource e))

/-- Stage 1 Theorem A: Stage-one dressing preserves the quotient projection π_T on ALL 5 edges. -/
theorem stage1_preserves_quotient_projection (U : E5 → UpperTri2) (e : E5) :
    torusProj (U_stage1 U e) = torusProj (U e) := by
  dsimp [U_stage1]
  have huT := u_N_isUnipotent U (edgeTarget e)
  have huS_inv : IsUnipotent (inv (u_N U (edgeSource e))) := by
    rw [u_N_inv_explicit]
    exact ⟨rfl, rfl⟩
  exact torusProj_unipotent_invariance (U e) (u_N U (edgeTarget e)) _ huT huS_inv

lemma b2_stage1_edge3_cancel (A B C D E : ℚ) (hD : D ≠ 0) (hE : E ≠ 0) :
    1 * A * (B / D) + (1 * C + (-(A * B + C * D) / (E * D)) * E) * 1 = 0 := by
  have h1 : (-(A * B + C * D) / (E * D)) * E = - ((A * B + C * D) / D) := by
    have : E * D = D * E := by ring
    rw [this]
    calc (-(A * B + C * D) / (D * E)) * E
      _ = - ((A * B + C * D) * E / (D * E)) := by ring
      _ = - ((A * B + C * D) / D) := by rw [mul_div_mul_right _ _ hE]
  rw [h1]
  have h2 : (A * B + C * D) / D = A * (B / D) + C := by
    calc (A * B + C * D) / D
      _ = (A * B) / D + (C * D) / D := by ring
      _ = A * (B / D) + C := by rw [mul_div_assoc, mul_div_cancel_right₀ C hD]
  rw [h2]
  ring

/-- Stage 1 Theorem B: Stage-one dressing leaves tree edges diagonal. -/
theorem stage1_tree_edges_diagonal (U : E5 → UpperTri2) (hU : ∀ e, IsInvertible (U e)) (e : E5)
    (he : isTreeEdge e) : IsTorus (U_stage1 U e) := by
  match e with
  | 0 =>
    dsimp [U_stage1, edgeSource, edgeTarget]
    rw [u_N_zero_inv, mul_one]
    have hT1 : treeTransport U 1 = U 0 := rfl
    have h_prod := u_N_mul_treeTransport U hU 1
    rw [hT1] at h_prod
    rw [h_prod]
    exact torusProj_isTorus (treeTransport U 1)
  | 1 => contradiction
  | 2 =>
    dsimp [U_stage1, edgeSource, edgeTarget]
    rw [u_N_zero_inv, mul_one]
    have hT2 : treeTransport U 2 = U 2 := rfl
    have h_prod := u_N_mul_treeTransport U hU 2
    rw [hT2] at h_prod
    rw [h_prod]
    exact torusProj_isTorus (treeTransport U 2)
  | 3 =>
    dsimp [U_stage1, edgeSource, edgeTarget, IsTorus]
    rw [u_N_inv_explicit]
    have hT2 : treeTransport U 2 = U 2 := rfl
    have hT3 : treeTransport U 3 = U 3 * U 2 := rfl
    have hd22 := (hU 2).2
    have hd32 := (hU 3).2
    dsimp [HMul.hMul, Mul.mul, u_N]
    have h_trans_b : (treeTransport U 3).b = (U 3).d1 * (U 2).b + (U 3).b * (U 2).d2 := by
      rw [hT3]; rfl
    have h_trans_d2 : (treeTransport U 3).d2 = (U 3).d2 * (U 2).d2 := by
      rw [hT3]; rfl
    rw [hT2, h_trans_b, h_trans_d2]
    exact b2_stage1_edge3_cancel (U 3).d1 (U 2).b (U 3).b (U 2).d2 (U 3).d2 hd22 hd32
  | 4 => contradiction

/-- Stage 1 Theorem C: Residual symmetry of the first kind.
    Any further diagonal torus gauge transformation preserves the diagonal property of tree edges. -/
theorem stage1_residual_first_kind_torus (U : E5 → UpperTri2) (hU : ∀ e, IsInvertible (U e))
    (t : V4 → UpperTri2) (ht : ∀ v, IsTorus (t v))
    (e : E5) (he : isTreeEdge e) :
    IsTorus (t (edgeTarget e) * U_stage1 U e * inv (t (edgeSource e))) := by
  have h_diag := stage1_tree_edges_diagonal U hU e he
  have h_t_target := ht (edgeTarget e)
  have h_t_source_inv := torus_inv (t (edgeSource e)) (ht (edgeSource e))
  have h1 := torus_mul_torus _ _ h_t_target h_diag
  exact torus_mul_torus _ _ h1 h_t_source_inv

/-- Stage 2: Torus dressing field u_T(v) = D(v)⁻¹ ∈ T. -/
def u_T (U : E5 → UpperTri2) (v : V4) : UpperTri2 :=
  inv (D_tree U v)

theorem u_T_isTorus (U : E5 → UpperTri2) (v : V4) :
    IsTorus (u_T U v) :=
  torus_inv _ (torusProj_isTorus _)

theorem u_T_isInvertible (U : E5 → UpperTri2) (hU : ∀ e, IsInvertible (U e)) (v : V4) :
    IsInvertible (u_T U v) :=
  inv_isInvertible _ (torusProj_isInvertible _ (treeTransport_invertible U hU v))

/-- Stage 2 Theorem A: Two-stage factorization matches full tree gauge:
    u_T(v) * u_N(v) = T(v)⁻¹. -/
theorem two_stage_factorization (U : E5 → UpperTri2) (hU : ∀ e, IsInvertible (U e)) (v : V4) :
    u_T U v * u_N U v = inv (treeTransport U v) := by
  have _ := (treeTransport_invertible U hU v).1
  have _ := (treeTransport_invertible U hU v).2
  ext
  · rw [mul_d1]
    dsimp [u_T, D_tree, torusProj, inv, u_N]
    ring
  · rw [mul_b]
    dsimp [u_T, D_tree, torusProj, inv, u_N]
    have h_zero : (0 / ((treeTransport U v).d1 * (treeTransport U v).d2)) * 1 = 0 := by ring
    rw [h_zero, add_zero]
    calc (treeTransport U v).d1⁻¹ * (-(treeTransport U v).b / (treeTransport U v).d2)
      _ = (-(treeTransport U v).b / (treeTransport U v).d2) * (treeTransport U v).d1⁻¹ := by ring
      _ = (-(treeTransport U v).b / (treeTransport U v).d2) / (treeTransport U v).d1 := by rw [mul_comm, inv_mul_eq_div]
      _ = -(treeTransport U v).b / ((treeTransport U v).d2 * (treeTransport U v).d1) := by rw [div_div]
      _ = -(treeTransport U v).b / ((treeTransport U v).d1 * (treeTransport U v).d2) := by
        rw [mul_comm ((treeTransport U v).d2)]
  · rw [mul_d2]
    dsimp [u_T, D_tree, torusProj, inv, u_N]
    ring

theorem inv_u_N_mul_inv_u_T (U : E5 → UpperTri2) (hU : ∀ e, IsInvertible (U e)) (v : V4) :
    inv (u_N U v) * inv (u_T U v) = treeTransport U v := by
  have hd2 := (treeTransport_invertible U hU v).2
  have h_inv_uT : inv (u_T U v) = ⟨(treeTransport U v).d1, 0, (treeTransport U v).d2⟩ := by
    dsimp [u_T, D_tree, torusProj, inv]
    ext
    · dsimp; rw [inv_inv]
    · dsimp; ring
    · dsimp; rw [inv_inv]
  ext
  · rw [mul_d1, u_N_inv_explicit, h_inv_uT]
    dsimp; ring
  · rw [mul_b, u_N_inv_explicit, h_inv_uT]
    dsimp
    calc 1 * 0 + ((treeTransport U v).b / (treeTransport U v).d2) * (treeTransport U v).d2
      _ = ((treeTransport U v).b / (treeTransport U v).d2) * (treeTransport U v).d2 := by ring
      _ = (treeTransport U v).b := div_mul_cancel₀ _ hd2
  · rw [mul_d2, u_N_inv_explicit, h_inv_uT]
    dsimp; ring

/-- Full tree-gauge dressing connection: U_full_e = T(target e)⁻¹ * U_e * T(source e). -/
def U_full (U : E5 → UpperTri2) (e : E5) : UpperTri2 :=
  inv (treeTransport U (edgeTarget e)) * U e * treeTransport U (edgeSource e)

/-- Stage 2 Theorem B: Dressing U⁽¹⁾ by u_T reproduces tree_gauge_indexed.residual on all 5 edges. -/
theorem stage2_reproduces_residual (U : E5 → UpperTri2) (hU : ∀ e, IsInvertible (U e)) (e : E5) :
    u_T U (edgeTarget e) * U_stage1 U e * inv (u_T U (edgeSource e)) = U_full U e := by
  dsimp [U_stage1, U_full]
  rw [mul_sandwich_assoc]
  rw [two_stage_factorization U hU (edgeTarget e)]
  rw [inv_u_N_mul_inv_u_T U hU (edgeSource e)]

end DiamondComplex

/-!
### Part 3: Discrete Curvature and Bianchi Identity on the Extended Diamond Poset P₅
-/

section PosetCurvature

variable {R : Type*} [CommRing R]

/-- Internal differential b on 1-cochains:
    (bA)(u, v, w) = - A(u, w) (deletes internal vertex v). -/
def b1 (A : R → R → R) (u _ w : R) : R := - A u w

/-- Cup product on 1-cochains:
    (A ⌣ A)(u, v, w) = A(u, v) * A(v, w). -/
def cup11 (A : R → R → R) (u v w : R) : R := A u v * A v w

/-- Discrete curvature K(A) = bA + A ⌣ A on 2-chains [u, v, w]. -/
def curvature1 (A : R → R → R) (u v w : R) : R :=
  b1 A u v w + cup11 A u v w

theorem curvature_formula (A : R → R → R) (u v w : R) :
    curvature1 A u v w = A u v * A v w - A u w := by
  dsimp [curvature1, b1, cup11]
  ring

/-- Internal differential b on 2-cochains:
    (bK)(u, v, w, z) = - K(u, w, z) + K(u, v, z) (deletes internal vertices v, w). -/
def b2 (K : R → R → R → R) (u v w z : R) : R :=
  - K u w z + K u v z

/-- Cup products between 1-cochains and 2-cochains. -/
def cup12 (A : R → R → R) (K : R → R → R → R) (u v w z : R) : R :=
  A u v * K v w z

def cup21 (K : R → R → R → R) (A : R → R → R) (u v w z : R) : R :=
  K u v w * A w z

/-- Discrete covariant differential on curvature:
    D_A K = bK + A ⌣ K - K ⌣ A. -/
def covariantDiff2 (A : R → R → R) (K : R → R → R → R) (u v w z : R) : R :=
  b2 K u v w z + cup12 A K u v w z - cup21 K A u v w z

/-- Part 3 Theorem A: b² = 0 on 1-cochains:
    b(bA)(u, v, w, z) = - (bA)(u, w, z) + (bA)(u, v, z) = 0. -/
theorem b_squared_zero (A : R → R → R) (u v w z : R) :
    b2 (b1 A) u v w z = 0 := by
  dsimp [b2, b1]
  ring

/-- Part 3 Theorem B: Discrete Bianchi Identity D_A(K(A)) = 0.
    For ANY commutative ring R and ANY 1-cochain A, the discrete curvature satisfies
    b(K(A)) + A ⌣ K(A) - K(A) ⌣ A = 0 identically on all 3-chains. -/
theorem discrete_bianchi_identity (A : R → R → R) (u v w z : R) :
    covariantDiff2 A (curvature1 A) u v w z = 0 := by
  dsimp [covariantDiff2, b2, cup12, cup21, curvature1, b1, cup11]
  ring

/-- Part 3 Theorem C: Curvature gauge covariance.
    Under a vertex dressing field g(v) with inverse g_inv(v),
    the dressed curvature K(A^g) satisfies K(A^g) = g(u) * K(A) * g_inv(w). -/
theorem curvature_gauge_covariance (A : R → R → R) (g g_inv : R → R)
    (h_inv : ∀ v, g v * g_inv v = 1)
    (A_gauge : R → R → R)
    (hA : ∀ x y, A_gauge x y = g x * A x y * g_inv y)
    (u v w : R) :
    curvature1 A_gauge u v w = g u * curvature1 A u v w * g_inv w := by
  rw [curvature_formula, curvature_formula]
  rw [hA u v, hA v w, hA u w]
  have h1 : g u * A u v * g_inv v * (g v * A v w * g_inv w) =
         g u * (A u v * A v w) * g_inv w := by
    calc g u * A u v * g_inv v * (g v * A v w * g_inv w)
      _ = (g u * A u v * A v w * g_inv w) * (g v * g_inv v) := by ring
      _ = (g u * A u v * A v w * g_inv w) * 1 := by rw [h_inv v]
      _ = g u * (A u v * A v w) * g_inv w := by ring
  rw [h1]
  ring

end PosetCurvature

/-!
### Part 4: Arithmetic comparison of the two recorded carrier dimensions
-/

section ColorDimension

/-- `(2 : ℕ) ≠ 3`. This is not a theorem about SU(3) representations or color transport. -/
theorem b2_color_dimension_mismatch : (2 : ℕ) ≠ 3 := by decide

end ColorDimension

end B2SemidirectDressing

#print axioms B2SemidirectDressing.UpperTri2.b2_semidirect_factorization
#print axioms B2SemidirectDressing.UpperTri2.b2_factorization_unique
#print axioms B2SemidirectDressing.UpperTri2.unipotent_subgroup_normal
#print axioms B2SemidirectDressing.stage1_preserves_quotient_projection
#print axioms B2SemidirectDressing.stage1_tree_edges_diagonal
#print axioms B2SemidirectDressing.stage1_residual_first_kind_torus
#print axioms B2SemidirectDressing.two_stage_factorization
#print axioms B2SemidirectDressing.stage2_reproduces_residual
#print axioms B2SemidirectDressing.b_squared_zero
#print axioms B2SemidirectDressing.discrete_bianchi_identity
#print axioms B2SemidirectDressing.curvature_gauge_covariance
#print axioms B2SemidirectDressing.b2_color_dimension_mismatch
