import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Campaign Module: TFQ-0044 (`FINITE_TOPOLOGICAL`)

Formalizes the narrowed finite counterpart and non-equivalence fences for
`TFQ-0044` ("anyon_model.rs wraps a ribbon category after braided validation
and a dimension check. Its SU(2)_k constructor uses the shared Racah gauge in
omega_fusion_categories::su2_level, with a bounded pentagon and hexagon replay.
That file warns the gauge is generally not orthonormal, so the F matrices must
not be advertised as unitary in the ordinary inner product. Labels a=0..k are
twice a spin, which is an SU(2) level family. There is no su3_level.rs beside
su2_level.rs. An SU(2)_k anyon model is not the three-color matrix algebra, and
its quantum dimensions are not C_F or C_A."):

1. **`SU(2)_k` Label Family, Truncated Fusion Rules, and Central Charge (`su2_level.rs`)**:
   - `su2MaxLevel = 6`, `su2LevelRank k = k + 1`, `su2RootOrder k = 8 * (k + 2)` (`24..64`).
   - Proves rank and root-order values for `k = 1..6` (`su2_level_rank_and_root_order_bounds`).
   - Proves central charge formula `su2CentralCharge k = (3 * k) / (k + 2)` and the
     level-3 (`k = 3`) integer-spin Fibonacci subring `2 ⊗ 2 = 0 ⊕ 2`
     (`su2_level_central_charge_and_level3_fibonacci_subring`).
2. **Exact `q`-Racah Non-Orthonormal Gauge vs. Weighted Metric Unitarity (`ℚ(φ)`)**:
   - Constructs `QPhi` (`a + b φ` with `φ^2 = φ + 1`) and the level-3 `q`-Racah
     associator `F^{[2,2,2,2]}` (`racahF00 = φ - 1`, `racahF02 = -1`, `racahF20 = 1 - φ`,
     `racahF22 = 1 - φ`) with tree metric weights `treeWeight0 = φ`, `treeWeight2 = φ + 1`.
   - Proves `F^{[2,2,2,2]}` is NOT orthonormal under the Euclidean inner product
     (`F_{00}^2 + F_{20}^2 ≠ 1`, `F_{00} F_{02} + F_{20} F_{22} ≠ 0`)
     (`racah_level3_fibonacci_f_matrix_not_euclidean_orthonormal`).
   - Proves exact weighted metric unitarity `F^T G F = G` (`w_0 F_{00}^2 + w_2 F_{20}^2 = w_0`,
     `w_0 F_{00} F_{02} + w_2 F_{20} F_{22} = 0`, `w_0 F_{02}^2 + w_2 F_{22}^2 = w_2`)
     and `det(F) = -1` (`racah_level3_fibonacci_f_matrix_weighted_metric_unitarity`).
3. **Why `SU(2)_k` Is Not `SU(3)_c` or a Color Fusion Category (Non-Equivalence Fences)**:
   - Proves `SU(3)_c` quadratic Casimirs `C_F = 4/3` and `C_A = 3` are not `SU(2)_k`
     quantum dimensions (`su2_level_quantum_dimensions_not_su3_casimirs_fence`).
   - Proves `SU(2)_k` has rank-1 self-dual simple labels (`a* = a`, count `k + 1`),
     whereas `SU(3)_k` has rank-2 Dynkin labels `(λ_1, λ_2)` (`(1, 0)* = (0, 1) ≠ (1, 0)`,
     count `(k + 1)(k + 2) / 2 > k + 1` for all `k ≥ 1`)
     (`su2_weight_lattice_rank1_not_su3_rank2_color_fusion_fence`,
      `su2_vs_su3_level_simple_object_count_separation`).
   - Proves budget and cyclotomic-field refusal predicates matching
     `unsupported_field_and_unbounded_level_are_typed_refusals`
     (`su2_level_budget_and_field_refusal_predicates`).
   - Proves the `TFQ-0044` scope ledger fence (`tfq0044_su2_level_scope_ledger_fence`).
-/

namespace CampaignTfq0044FiniteTopological

-- ============================================================================
-- 1. SU(2)_k Label Family, Truncated Fusion Rules, and Central Charge
-- ============================================================================

/-- Maximum admitted `SU(2)_k` level in `code/rust/src/fusion_categories/su2_level.rs`. -/
def su2MaxLevel : Nat := 6

/-- Simple-object count `k + 1` (`a = 0..k`, where `a = 2j`) for `SU(2)_k`. -/
def su2LevelRank (k : Nat) : Nat := k + 1

/-- Cyclotomic root order `8 * (k + 2)` required for `SU(2)_k` braiding in `su2_level.rs`. -/
def su2RootOrder (k : Nat) : Nat := 8 * (k + 2)

/-- Modular central charge `3k / (k + 2)` (`central_charge_mod_4` in `su2_level.rs`). -/
def su2CentralCharge (k : ℚ) : ℚ := (3 * k) / (k + 2)

/-- Truncated `SU(2)_k` fusion admissibility predicate for doubled spins `a, b, c ≤ k`. -/
def su2Admissible (k a b c : Nat) : Bool :=
  (a <= k) && (b <= k) && (c <= k) &&
  ((a + b + c) % 2 == 0) &&
  (c <= a + b) && (a <= b + c) && (b <= a + c) &&
  (a + b + c <= 2 * k)

/-- Theorem 1: For `k = 1..6`, `su2LevelRank k = k + 1` (`2..7`) and
`su2RootOrder k = 8 * (k + 2)` (`24, 32, 40, 48, 56, 64`). -/
theorem su2_level_rank_and_root_order_bounds :
    su2MaxLevel = 6 ∧
    (su2LevelRank 1, su2RootOrder 1) = (2, 24) ∧
    (su2LevelRank 2, su2RootOrder 2) = (3, 32) ∧
    (su2LevelRank 3, su2RootOrder 3) = (4, 40) ∧
    (su2LevelRank 4, su2RootOrder 4) = (5, 48) ∧
    (su2LevelRank 5, su2RootOrder 5) = (6, 56) ∧
    (su2LevelRank 6, su2RootOrder 6) = (7, 64) := by
  decide

/-- Theorem 2: The central charge formula `su2CentralCharge k = 3k / (k + 2)` gives
`1, 3/2, 9/5, 2, 15/7, 9/4` at `k = 1..6`, and at `k = 3`, label `a = 2` (`j = 1`)
closes the even-spin Fibonacci fusion subring `2 ⊗ 2 = 0 ⊕ 2`. -/
theorem su2_level_central_charge_and_level3_fibonacci_subring :
    su2CentralCharge 1 = 1 ∧
    su2CentralCharge 2 = 3 / 2 ∧
    su2CentralCharge 3 = 9 / 5 ∧
    su2CentralCharge 4 = 2 ∧
    su2CentralCharge 5 = 15 / 7 ∧
    su2CentralCharge 6 = 9 / 4 ∧
    su2Admissible 3 2 2 0 = true ∧
    su2Admissible 3 2 2 2 = true ∧
    su2Admissible 3 2 2 1 = false ∧
    su2Admissible 3 2 2 3 = false := by
  dsimp [su2CentralCharge]
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num, by norm_num, by norm_num,
          by decide, by decide, by decide, by decide⟩

-- ============================================================================
-- 2. Exact q-Racah Non-Orthonormal Gauge vs. Weighted Metric Unitarity in ℚ(φ)
-- ============================================================================

/-- Exact quadratic extension `ℚ(φ)` with `φ^2 = φ + 1`, represented as `a + b φ`. -/
@[ext]
structure QPhi where
  a : ℚ
  b : ℚ
  deriving DecidableEq, Repr

def qphiZero : QPhi := ⟨0, 0⟩
def qphiOne : QPhi := ⟨1, 0⟩
def qphiPhi : QPhi := ⟨0, 1⟩
def qphiPhiInv : QPhi := ⟨-1, 1⟩

def qphiAdd (x y : QPhi) : QPhi :=
  ⟨x.a + y.a, x.b + y.b⟩

def qphiSub (x y : QPhi) : QPhi :=
  ⟨x.a - y.a, x.b - y.b⟩

def qphiNeg (x : QPhi) : QPhi :=
  ⟨-x.a, -x.b⟩

/-- Multiplication in `ℚ(φ)` using `φ^2 = 1 + φ`:
`(a_1 + b_1 φ)(a_2 + b_2 φ) = (a_1 a_2 + b_1 b_2) + (a_1 b_2 + b_1 a_2 + b_1 b_2) φ`. -/
def qphiMul (x y : QPhi) : QPhi :=
  ⟨x.a * y.a + x.b * y.b, x.a * y.b + x.b * y.a + x.b * y.b⟩

/-- Theorem 3: In `QPhi`, `φ^2 = 1 + φ` and `φ * (φ - 1) = 1`. -/
theorem qphi_golden_ratio_identities :
    qphiMul qphiPhi qphiPhi = qphiAdd qphiOne qphiPhi ∧
    qphiMul qphiPhi qphiPhiInv = qphiOne := by
  constructor <;> (ext <;> dsimp [qphiMul, qphiAdd, qphiOne, qphiPhi, qphiPhiInv] <;> norm_num)

/-- Level-3 `q`-Racah associator entries for `[2, 2, 2, 2]` on channels `{0, 2}` (`su2_level.rs`):
`F_{00} = φ⁻¹ = φ - 1`, `F_{02} = -1`, `F_{20} = -φ⁻¹ = 1 - φ`, `F_{22} = -φ⁻¹ = 1 - φ`. -/
def racahF00 : QPhi := ⟨-1, 1⟩
def racahF02 : QPhi := ⟨-1, 0⟩
def racahF20 : QPhi := ⟨1, -1⟩
def racahF22 : QPhi := ⟨1, -1⟩

/-- Diagonal tree-metric weights `G = diag(w_0, w_2)` for `[2, 2, 2, 2]` at `k = 3`:
`w_0 = φ = (0, 1)` and `w_2 = φ^2 = 1 + φ = (1, 1)`. -/
def treeWeight0 : QPhi := ⟨0, 1⟩
def treeWeight2 : QPhi := ⟨1, 1⟩

/-- Theorem 4 (Racah Gauge Is Not Euclidean Orthonormal):
In the ordinary Euclidean inner product (`G = I`), `(F^T F)_{00} = F_{00}^2 + F_{20}^2 = 4 - 2φ ≠ 1`
and `(F^T F)_{02} = F_{00} F_{02} + F_{20} F_{22} = 3 - 2φ ≠ 0`, and `F_{02} ≠ F_{20}`. -/
theorem racah_level3_fibonacci_f_matrix_not_euclidean_orthonormal :
    qphiAdd (qphiMul racahF00 racahF00) (qphiMul racahF20 racahF20) ≠ qphiOne ∧
    qphiAdd (qphiMul racahF00 racahF02) (qphiMul racahF20 racahF22) ≠ qphiZero ∧
    racahF02 ≠ racahF20 := by
  refine ⟨?_, ?_, ?_⟩
  · intro h
    have ha := congrArg QPhi.a h
    dsimp [qphiAdd, qphiMul, racahF00, racahF20, qphiOne] at ha
    norm_num at ha
  · intro h
    have ha := congrArg QPhi.a h
    dsimp [qphiAdd, qphiMul, racahF00, racahF02, racahF20, racahF22, qphiZero] at ha
    norm_num at ha
  · intro h
    have hb := congrArg QPhi.b h
    dsimp [racahF02, racahF20] at hb
    norm_num at hb

/-- Theorem 5 (Exact Weighted Metric Unitarity `F^T G F = G`):
Under the diagonal tree metric `G = diag(w_0, w_2)`, the level-3 `q`-Racah `F`-matrix
satisfies `F^T G F = G` entrywise (`(F^T G F)_{00} = w_0`, `(F^T G F)_{02} = 0`,
`(F^T G F)_{22} = w_2`) and `det(F) = F_{00} F_{22} - F_{02} F_{20} = -1 ≠ 0`. -/
theorem racah_level3_fibonacci_f_matrix_weighted_metric_unitarity :
    qphiAdd (qphiMul treeWeight0 (qphiMul racahF00 racahF00))
            (qphiMul treeWeight2 (qphiMul racahF20 racahF20)) = treeWeight0 ∧
    qphiAdd (qphiMul treeWeight0 (qphiMul racahF00 racahF02))
            (qphiMul treeWeight2 (qphiMul racahF20 racahF22)) = qphiZero ∧
    qphiAdd (qphiMul treeWeight0 (qphiMul racahF02 racahF02))
            (qphiMul treeWeight2 (qphiMul racahF22 racahF22)) = treeWeight2 ∧
    qphiSub (qphiMul racahF00 racahF22) (qphiMul racahF02 racahF20) = qphiNeg qphiOne := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
    (ext <;>
     dsimp [qphiAdd, qphiSub, qphiNeg, qphiMul, treeWeight0, treeWeight2,
            racahF00, racahF02, racahF20, racahF22, qphiZero, qphiOne] <;>
     norm_num)

-- ============================================================================
-- 3. Why SU(2)_k Is Not SU(3)_c or a Color Fusion Category (Non-Equivalence Fences)
-- ============================================================================

/-- Quadratic Casimir invariants `C_F = 4/3` and `C_A = 3` of `SU(3)_c`. -/
def su3ColorCasimirCF : ℚ := 4 / 3
def su3ColorCasimirCA : ℚ := 3

/-- Theorem 6 (`SU(2)_k` Quantum Dimensions Are Not `C_F` or `C_A` Fence):
The `SU(3)_c` fundamental Casimir `C_F = 4/3` is neither `1` (`d_0`), nor a root of
`x^2 - 2 = 0` (`d_1` at `k = 2`), nor a root of `x^2 - x - 1 = 0` (`d_1, d_2` at `k = 3`),
nor a root of `x^2 - 3 = 0` (`d_1` at `k = 4`); and for all `k ≤ 6`, `d_1(SU(2)_k) = 2 cos(π/(k+2)) < 2 < C_A = 3`. -/
theorem su2_level_quantum_dimensions_not_su3_casimirs_fence :
    su3ColorCasimirCF ≠ 1 ∧
    su3ColorCasimirCF ^ 2 - 2 ≠ 0 ∧
    su3ColorCasimirCF ^ 2 - su3ColorCasimirCF - 1 ≠ 0 ∧
    su3ColorCasimirCF ^ 2 - 3 ≠ 0 ∧
    (2 : ℚ) < su3ColorCasimirCA := by
  dsimp [su3ColorCasimirCF, su3ColorCasimirCA]
  norm_num

/-- Simple-object count `(k + 1)(k + 2) / 2` for `SU(3)_k` (Dynkin weights `(λ_1, λ_2)` with `λ_1 + λ_2 ≤ k`). -/
def su3LevelRank (k : Nat) : Nat :=
  (k + 1) * (k + 2) / 2

/-- Dual label map `a ↦ a` in `SU(2)_k` (every `SU(2)` representation is self-dual) vs.
`SU(3)_k` conjugate weight `(λ_1, λ_2) ↦ (λ_2, λ_1)` (fundamental `(1, 0)` has dual `(0, 1) ≠ (1, 0)`). -/
def su2DualLabel (a : Nat) : Nat := a
def su3DualWeight (w : Nat × Nat) : Nat × Nat := (w.2, w.1)

/-- Theorem 7 (`SU(2)_k` Rank-1 Self-Dual Labels vs. `SU(3)_k` Rank-2 Conjugate Labels Fence):
Every `SU(2)_k` label is self-dual (`su2DualLabel a = a`), whereas the `SU(3)_k` fundamental
weight `(1, 0)` is not self-dual (`su3DualWeight (1, 0) = (0, 1) ≠ (1, 0)`). -/
theorem su2_weight_lattice_rank1_not_su3_rank2_color_fusion_fence :
    (∀ a : Nat, su2DualLabel a = a) ∧
    su3DualWeight (1, 0) = (0, 1) ∧
    su3DualWeight (1, 0) ≠ (1, 0) := by
  refine ⟨fun _ => rfl, rfl, by decide⟩

/-- Theorem 8: For every admitted level `k ∈ {1, 2, 3, 4, 5, 6}`, the `SU(2)_k` simple-object
count `k + 1` is strictly smaller than the `SU(3)_k` simple-object count `(k + 1)(k + 2) / 2`
(`2 < 3, 3 < 6, 4 < 10, 5 < 15, 6 < 21, 7 < 28`). -/
theorem su2_vs_su3_level_simple_object_count_separation :
    (su2LevelRank 1, su3LevelRank 1) = (2, 3) ∧
    (su2LevelRank 2, su3LevelRank 2) = (3, 6) ∧
    (su2LevelRank 3, su3LevelRank 3) = (4, 10) ∧
    (su2LevelRank 4, su3LevelRank 4) = (5, 15) ∧
    (su2LevelRank 5, su3LevelRank 5) = (6, 21) ∧
    (su2LevelRank 6, su3LevelRank 6) = (7, 28) ∧
    (∀ k ∈ ([1, 2, 3, 4, 5, 6] : List Nat), su2LevelRank k < su3LevelRank k) := by
  decide

/-- Level budget and cyclotomic field order admission predicates matching
`unsupported_field_and_unbounded_level_are_typed_refusals` in `su2_level.rs`. -/
def su2LevelBudgetAdmitted (k : Nat) : Bool :=
  (1 <= k) && (k <= su2MaxLevel)

def cyclotomicFieldAdmitsSu2Level (fieldOrder k : Nat) : Bool :=
  su2LevelBudgetAdmitted k && (fieldOrder > 0) && (fieldOrder % su2RootOrder k == 0)

/-- Theorem 9: `su2LevelBudgetAdmitted` rejects `k = 0` and `k = 7` (`MAX_LEVEL + 1`),
and `cyclotomicFieldAdmitsSu2Level` rejects `Cyclotomic<8>` at `k = 3` while admitting
`Cyclotomic<40>` at `k = 3` and `Cyclotomic<64>` at `k = 6`. -/
theorem su2_level_budget_and_field_refusal_predicates :
    su2LevelBudgetAdmitted 0 = false ∧
    su2LevelBudgetAdmitted 7 = false ∧
    su2LevelBudgetAdmitted 3 = true ∧
    cyclotomicFieldAdmitsSu2Level 8 3 = false ∧
    cyclotomicFieldAdmitsSu2Level 40 3 = true ∧
    cyclotomicFieldAdmitsSu2Level 64 6 = true := by
  decide

/-- Scope ledger for `TFQ-0044`. -/
structure Tfq0044ScopeLedger where
  hasSu2LevelRacahInRepo : Bool
  hasWeightedMetricUnitarityCheck : Bool
  isRacahGaugeEuclideanOrthonormal : Bool
  hasSu3LevelInRepo : Bool
  su2QuantumDimsEqualSu3Casimirs : Bool
  deriving DecidableEq, Repr

def tfq0044RepoLedger : Tfq0044ScopeLedger :=
  ⟨true, true, false, false, false⟩

/-- Theorem 10: `tfq0044RepoLedger` records that `su2_level.rs` implements the `SU(2)_k`
Racah gauge with weighted metric unitarity, while its `F`-matrices are not Euclidean
orthonormal, `su3_level.rs` is absent, and `SU(2)_k` quantum dimensions are not `C_F` or `C_A`. -/
theorem tfq0044_su2_level_scope_ledger_fence :
    tfq0044RepoLedger.hasSu2LevelRacahInRepo = true ∧
    tfq0044RepoLedger.hasWeightedMetricUnitarityCheck = true ∧
    tfq0044RepoLedger.isRacahGaugeEuclideanOrthonormal = false ∧
    tfq0044RepoLedger.hasSu3LevelInRepo = false ∧
    tfq0044RepoLedger.su2QuantumDimsEqualSu3Casimirs = false ∧
    tfq0044RepoLedger.hasSu2LevelRacahInRepo ≠ tfq0044RepoLedger.hasSu3LevelInRepo := by
  decide

#print axioms su2_level_rank_and_root_order_bounds
#print axioms su2_level_central_charge_and_level3_fibonacci_subring
#print axioms qphi_golden_ratio_identities
#print axioms racah_level3_fibonacci_f_matrix_not_euclidean_orthonormal
#print axioms racah_level3_fibonacci_f_matrix_weighted_metric_unitarity
#print axioms su2_level_quantum_dimensions_not_su3_casimirs_fence
#print axioms su2_weight_lattice_rank1_not_su3_rank2_color_fusion_fence
#print axioms su2_vs_su3_level_simple_object_count_separation
#print axioms su2_level_budget_and_field_refusal_predicates
#print axioms tfq0044_su2_level_scope_ledger_fence

end CampaignTfq0044FiniteTopological
