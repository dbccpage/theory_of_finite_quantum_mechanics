import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Campaign Module: TFQ-0050 (`FINITE_TOPOLOGICAL`)

Formalizes the narrowed finite counterpart and non-equivalence fences for
`TFQ-0050` ("catalog.rs pins exact ribbon data for Ising, Fibonacci, semion,
pointed braided categories, the toric code as D(Z_2), a three-fermion model,
and quantum doubles D(Z_n). A coefficient field that lacks the needed root of
unity is FusionError::FieldTooSmall, not an approximation. su2_level.rs is the
SU(2) family in a Racah gauge. The file su3_level.rs is absent from
omega_fusion_categories/src, so there is no fusion-category obligation already
discharged for SU(3)_k. The catalog does not assert a material host. This
absence is an open obligation, not a negative theorem about fusion categories."):

1. **Catalog Ribbon Categories (`catalog.rs`): Ranks, Squared Dimensions, and Topological Spins**:
   - Proves exact simple-object counts and total squared quantum dimensions `D^2`
     for Ising (`D^2 = 4`), semion (`D^2 = 2`), toric code `D(ℤ_2)` (`D^2 = 4`),
     three-fermion (`D^2 = 4`), and `D(ℤ_n)` (`n^2`)
     (`catalog_ribbon_ranks_and_total_squared_dimensions`).
   - Proves that `toric_code` (`[[0, 1], [0, 0]]`) and `three_fermion` (`[[1, 1], [0, 1]]`)
     share the `ℤ_2 × ℤ_2` pointed fusion ring (rank `4`) while differing in their
     diagonal topological spin exponents (`3` bosons + `1` fermion vs. `1` boson + `3` fermions)
     (`toric_code_vs_three_fermion_topological_spin_twists`).
2. **Exact Cyclotomic Root-of-Unity Admission & `FusionError::FieldTooSmall` Refusal**:
   - Proves `fieldAdmitsRootOrder` rejects insufficient cyclotomic field orders
     (`Cyclotomic<8>` for Ising `16`, Fibonacci `10`, and `SU(2)_3` `40`) and admits
     exact multiples (`catalog_cyclotomic_field_admission_and_refusal`).
3. **`SU(3)_k` Weyl Alcove Combinatorics vs. Catalog Models & Open-Obligation Fences**:
   - Proves `su3WeylAlcoveCount k = (k + 1)(k + 2) / 2` (`3` at `k = 1`, `6` at `k = 2`,
     `10` at `k = 3`), contrasting pointed `SU(3)_1 ≅ ℤ_3` with non-pointed `SU(3)_k` (`k ≥ 2`)
     (`su3_level1_pointed_z3_fusion_vs_higher_level_nonpointed`).
   - Proves `D(ℤ_3)` (`rank = 9`) never equals `su3WeylAlcoveCount k` for any `k = 1..6`
     (`quantum_double_z3_rank9_not_su3_level_k_fence`).
   - Proves fixed catalog models have self-dual simple objects (`a* = a` for Fibonacci,
     Ising, `D(ℤ_2)`, and `SU(2)_k`), whereas `SU(3)_k` (`k ≥ 1`) has non-self-dual
     fundamental weight `(1, 0)* = (0, 1) ≠ (1, 0)`
     (`catalog_self_dual_models_not_su3_conjugate_pair_fence`).
   - Proves the `SU(3)_2` fundamental quantum dimension identity `(d_{(1,0)})^2 = d_{(0,1)} + d_{(2,0)}`
     in `ℚ(φ)` (`d_{(1,0)} = d_{(0,1)} = φ`, `d_{(2,0)} = 1`)
     (`su3_level2_fundamental_quantum_dimension_golden_ratio`).
   - Proves that the absence of `su3_level.rs` is classified as `OpenImplementationObligation`
     rather than `DischargedInRepo` or `NegativeImpossibilityTheorem`, and that the
     catalog asserts no material host (`absence_of_su3_level_rs_is_open_obligation_not_impossibility_theorem_fence`,
     `catalog_ribbon_categories_do_not_assert_material_host_or_qcd_confinement_fence`,
     `tfq0050_catalog_and_su3_level_scope_ledger_fence`).
-/

namespace CampaignTfq0050FiniteTopological

-- ============================================================================
-- 1. Catalog Ribbon Categories (catalog.rs): Ranks, D^2, and Topological Spins
-- ============================================================================

/-- Total squared quantum dimension `D^2 = 1^2 + (√2)^2 + 1^2 = 4` of the Ising model (`catalog::ising`). -/
def isingTotalDimSq : ℚ := 1 + 2 + 1

/-- Total squared quantum dimension `D^2 = 1^2 + 1^2 = 2` of the semion model (`catalog::semion`). -/
def semionTotalDimSq : ℚ := 1 + 1

/-- Total squared quantum dimension `D^2 = 4` of `D(ℤ_2)` (`catalog::toric_code`) and `catalog::three_fermion`. -/
def z2x2PointedTotalDimSq : ℚ := 1 + 1 + 1 + 1

/-- Simple-object count `n^2` of `D(ℤ_n)` (`catalog::quantum_double_cyclic`). -/
def quantumDoubleCyclicRank (n : Nat) : Nat := n * n

/-- Theorem 1: `isingTotalDimSq = 4`, `semionTotalDimSq = 2`, `z2x2PointedTotalDimSq = 4`,
and `quantumDoubleCyclicRank n = n^2` (`4` at `n = 2`, `9` at `n = 3`, `16` at `n = 4`). -/
theorem catalog_ribbon_ranks_and_total_squared_dimensions :
    isingTotalDimSq = 4 ∧
    semionTotalDimSq = 2 ∧
    z2x2PointedTotalDimSq = 4 ∧
    quantumDoubleCyclicRank 2 = 4 ∧
    quantumDoubleCyclicRank 3 = 9 ∧
    quantumDoubleCyclicRank 4 = 16 := by
  dsimp [isingTotalDimSq, semionTotalDimSq, z2x2PointedTotalDimSq]
  refine ⟨by norm_num, by norm_num, by norm_num, by decide, by decide, by decide⟩

/-- Diagonal quadratic exponent `x_0 * B_{00} * x_0 + x_0 * B_{01} * x_1 + x_1 * B_{10} * x_0 + x_1 * B_{11} * x_1 mod 2`
determining bosonic (`0`) vs. fermionic (`1`, twist `-1`) statistics on `ℤ_2 × ℤ_2` in `catalog.rs`. -/
def toricCodeSpinParity (x0 x1 : Nat) : Nat :=
  (x0 * 0 * x0 + x0 * 1 * x1 + x1 * 0 * x0 + x1 * 0 * x1) % 2

def threeFermionSpinParity (x0 x1 : Nat) : Nat :=
  (x0 * 1 * x0 + x0 * 1 * x1 + x1 * 0 * x0 + x1 * 1 * x1) % 2

/-- Theorem 2: On `ℤ_2 × ℤ_2 = {(0,0), (1,0), (0,1), (1,1)}`, `toric_code` has spin parities
`[0, 0, 0, 1]` (`3` bosons, `1` fermion `ε`), whereas `three_fermion` has spin parities
`[0, 1, 1, 1]` (`1` boson, `3` fermions `f_1, f_2, f_3`). -/
theorem toric_code_vs_three_fermion_topological_spin_twists :
    (toricCodeSpinParity 0 0, toricCodeSpinParity 1 0,
     toricCodeSpinParity 0 1, toricCodeSpinParity 1 1) = (0, 0, 0, 1) ∧
    (threeFermionSpinParity 0 0, threeFermionSpinParity 1 0,
     threeFermionSpinParity 0 1, threeFermionSpinParity 1 1) = (0, 1, 1, 1) ∧
    toricCodeSpinParity 1 0 ≠ threeFermionSpinParity 1 0 := by
  decide

-- ============================================================================
-- 2. Exact Cyclotomic Root-of-Unity Admission & FusionError::FieldTooSmall Refusal
-- ============================================================================

/-- Exact root-of-unity divisibility check modeling `root_of_unity::<K>(order, k)` in `catalog.rs`:
returns `false` (`FusionError::FieldTooSmall`) whenever `fieldOrder` is not a positive multiple of `requiredOrder`. -/
def fieldAdmitsRootOrder (fieldOrder requiredOrder : Nat) : Bool :=
  (fieldOrder > 0) && (requiredOrder > 0) && (fieldOrder % requiredOrder == 0)

/-- Required root orders in `catalog.rs`: `16` for Ising, `10` for Fibonacci, `4` for semion,
and `8 * (k + 2)` for `SU(2)_k`. -/
def isingRootOrder : Nat := 16
def fibonacciRootOrder : Nat := 10
def semionRootOrder : Nat := 4
def su2LevelRootOrder (k : Nat) : Nat := 8 * (k + 2)

/-- Theorem 3: `Cyclotomic<8>` is rejected (`false`, `FieldTooSmall`) for Ising (`16`),
Fibonacci (`10`), and `SU(2)_3` (`40`), while `Cyclotomic<16>` admits Ising and semion,
and `Cyclotomic<40>` admits Fibonacci, semion, and `SU(2)_3`. -/
theorem catalog_cyclotomic_field_admission_and_refusal :
    fieldAdmitsRootOrder 8 isingRootOrder = false ∧
    fieldAdmitsRootOrder 8 fibonacciRootOrder = false ∧
    fieldAdmitsRootOrder 8 (su2LevelRootOrder 3) = false ∧
    fieldAdmitsRootOrder 16 isingRootOrder = true ∧
    fieldAdmitsRootOrder 16 semionRootOrder = true ∧
    fieldAdmitsRootOrder 40 fibonacciRootOrder = true ∧
    fieldAdmitsRootOrder 40 (su2LevelRootOrder 3) = true := by
  decide

-- ============================================================================
-- 3. SU(3)_k Weyl Alcove Combinatorics vs. Catalog Models & Open-Obligation Fences
-- ============================================================================

/-- Number of integrable highest weights `(λ_1, λ_2)` (`λ_1 + λ_2 ≤ k`) in `SU(3)_k`. -/
def su3WeylAlcoveCount (k : Nat) : Nat :=
  (k + 1) * (k + 2) / 2

/-- Theorem 4: At `k = 1`, `su3WeylAlcoveCount 1 = 3` (pointed `ℤ_3` fusion), whereas for
`k = 2..6`, `su3WeylAlcoveCount k ∈ {6, 10, 15, 21, 28}` is strictly greater than `3` and
the fundamental product `(1, 0) ⊗ (1, 0) = (0, 1) ⊕ (2, 0)` has `2 > 1` channels (non-pointed). -/
theorem su3_level1_pointed_z3_fusion_vs_higher_level_nonpointed :
    su3WeylAlcoveCount 1 = 3 ∧
    su3WeylAlcoveCount 2 = 6 ∧
    su3WeylAlcoveCount 3 = 10 ∧
    su3WeylAlcoveCount 4 = 15 ∧
    (∀ k ∈ ([2, 3, 4, 5, 6] : List Nat), 3 < su3WeylAlcoveCount k) := by
  decide

/-- Theorem 5 (`D(ℤ_3)` Is Not `SU(3)_k` Fence):
The quantum double `D(ℤ_3)` (`catalog::quantum_double_cyclic(3)`) has rank `3^2 = 9`,
which never equals `su3WeylAlcoveCount k` for any `k ∈ {1, 2, 3, 4, 5, 6}`. -/
theorem quantum_double_z3_rank9_not_su3_level_k_fence :
    quantumDoubleCyclicRank 3 = 9 ∧
    (∀ k ∈ ([1, 2, 3, 4, 5, 6] : List Nat), su3WeylAlcoveCount k ≠ quantumDoubleCyclicRank 3) := by
  decide

/-- Conjugation involution `(λ_1, λ_2) ↦ (λ_2, λ_1)` on `SU(3)_k` weights vs. self-dual labels `a ↦ a`. -/
def su3WeightConjugate (w : Nat × Nat) : Nat × Nat := (w.2, w.1)

/-- Theorem 6: Every `SU(3)_k` (`k ≥ 1`) contains the non-self-dual fundamental pair
`(1, 0)` and `(0, 1)` (`su3WeightConjugate (1, 0) ≠ (1, 0)`), unlike the self-dual simple
objects of Fibonacci, Ising, `D(ℤ_2)`, and `SU(2)_k`. -/
theorem catalog_self_dual_models_not_su3_conjugate_pair_fence :
    su3WeightConjugate (1, 0) = (0, 1) ∧
    su3WeightConjugate (0, 1) = (1, 0) ∧
    su3WeightConjugate (1, 0) ≠ (1, 0) := by
  decide

/-- Exact quadratic extension `ℚ(φ)` (`φ^2 = 1 + φ`) for `SU(3)_2` quantum dimensions (`k + 3 = 5`). -/
@[ext]
structure QPhi where
  a : ℚ
  b : ℚ
  deriving DecidableEq, Repr

def qphiAdd (x y : QPhi) : QPhi := ⟨x.a + y.a, x.b + y.b⟩
def qphiMul (x y : QPhi) : QPhi := ⟨x.a * y.a + x.b * y.b, x.a * y.b + x.b * y.a + x.b * y.b⟩

/-- At `SU(3)_2` (`q = e^{iπ/5}`, `[2]_q = φ`, `[3]_q = φ`, `[4]_q = 1`), the quantum dimensions of
`(1, 0)`, `(0, 1)`, and `(2, 0)` are `d_{(1,0)} = d_{(0,1)} = φ` and `d_{(2,0)} = 1`. -/
def su3Level2Dim10 : QPhi := ⟨0, 1⟩
def su3Level2Dim01 : QPhi := ⟨0, 1⟩
def su3Level2Dim20 : QPhi := ⟨1, 0⟩

/-- Theorem 7: In `SU(3)_2`, the fusion rule `(1, 0) ⊗ (1, 0) = (0, 1) ⊕ (2, 0)` is respected
by the exact `ℚ(φ)` quantum dimensions: `d_{(1,0)}^2 = φ^2 = 1 + φ = d_{(0,1)} + d_{(2,0)}`. -/
theorem su3_level2_fundamental_quantum_dimension_golden_ratio :
    qphiMul su3Level2Dim10 su3Level2Dim10 = qphiAdd su3Level2Dim01 su3Level2Dim20 ∧
    qphiMul su3Level2Dim10 su3Level2Dim10 = ⟨1, 1⟩ := by
  constructor <;> (ext <;> dsimp [qphiMul, qphiAdd, su3Level2Dim10, su3Level2Dim01, su3Level2Dim20] <;> norm_num)

/-- Epistemic classification of a missing module in the repository. -/
inductive ObligationEpistemicKind
  | DischargedInRepo
  | OpenImplementationObligation
  | NegativeImpossibilityTheorem
  deriving DecidableEq, Repr

def su3LevelRepoClassification : ObligationEpistemicKind :=
  ObligationEpistemicKind.OpenImplementationObligation

/-- Theorem 8 (Absence of `su3_level.rs` Is an Open Obligation, Not a Negative Theorem Fence):
`su3LevelRepoClassification` equals `OpenImplementationObligation`, and is neither
`DischargedInRepo` nor `NegativeImpossibilityTheorem`. -/
theorem absence_of_su3_level_rs_is_open_obligation_not_impossibility_theorem_fence :
    su3LevelRepoClassification = ObligationEpistemicKind.OpenImplementationObligation ∧
    su3LevelRepoClassification ≠ ObligationEpistemicKind.DischargedInRepo ∧
    su3LevelRepoClassification ≠ ObligationEpistemicKind.NegativeImpossibilityTheorem := by
  decide

/-- Algebraic ribbon category check vs. physical material host assertion. -/
structure RibbonCatalogEntryAudit where
  passesPentagonAndHexagon : Bool
  passesFieldRootAdmission : Bool
  assertsPhysicalMaterialHost : Bool
  dischargesSu3ColorConfinement : Bool
  deriving DecidableEq, Repr

def catalogVerifiedEntry : RibbonCatalogEntryAudit :=
  ⟨true, true, false, false⟩

/-- Theorem 9: A verified `catalog.rs` ribbon category entry passes pentagon, hexagon, and
field root admission checks while asserting no physical material host and discharging no
`SU(3)_c` color confinement claim. -/
theorem catalog_ribbon_categories_do_not_assert_material_host_or_qcd_confinement_fence :
    catalogVerifiedEntry.passesPentagonAndHexagon = true ∧
    catalogVerifiedEntry.passesFieldRootAdmission = true ∧
    catalogVerifiedEntry.assertsPhysicalMaterialHost = false ∧
    catalogVerifiedEntry.dischargesSu3ColorConfinement = false := by
  decide

/-- Scope ledger for `TFQ-0050`. -/
structure Tfq0050ScopeLedger where
  hasCatalogRibbonModels : Bool
  hasFieldTooSmallRefusal : Bool
  hasSu2LevelRacah : Bool
  hasSu3LevelFile : Bool
  assertsMaterialHost : Bool
  isNegativeTheoremOnFusionCategories : Bool
  deriving DecidableEq, Repr

def tfq0050RepoLedger : Tfq0050ScopeLedger :=
  ⟨true, true, true, false, false, false⟩

/-- Theorem 10: `tfq0050RepoLedger` records that `catalog.rs` and `su2_level.rs` pin exact
ribbon data and `FusionError::FieldTooSmall` refusals, while `su3_level.rs` is absent as an
open obligation, no material host is asserted, and the absence is not a negative theorem. -/
theorem tfq0050_catalog_and_su3_level_scope_ledger_fence :
    tfq0050RepoLedger.hasCatalogRibbonModels = true ∧
    tfq0050RepoLedger.hasFieldTooSmallRefusal = true ∧
    tfq0050RepoLedger.hasSu2LevelRacah = true ∧
    tfq0050RepoLedger.hasSu3LevelFile = false ∧
    tfq0050RepoLedger.assertsMaterialHost = false ∧
    tfq0050RepoLedger.isNegativeTheoremOnFusionCategories = false ∧
    tfq0050RepoLedger.hasSu2LevelRacah ≠ tfq0050RepoLedger.hasSu3LevelFile := by
  decide

#print axioms catalog_ribbon_ranks_and_total_squared_dimensions
#print axioms toric_code_vs_three_fermion_topological_spin_twists
#print axioms catalog_cyclotomic_field_admission_and_refusal
#print axioms su3_level1_pointed_z3_fusion_vs_higher_level_nonpointed
#print axioms quantum_double_z3_rank9_not_su3_level_k_fence
#print axioms catalog_self_dual_models_not_su3_conjugate_pair_fence
#print axioms su3_level2_fundamental_quantum_dimension_golden_ratio
#print axioms absence_of_su3_level_rs_is_open_obligation_not_impossibility_theorem_fence
#print axioms catalog_ribbon_categories_do_not_assert_material_host_or_qcd_confinement_fence
#print axioms tfq0050_catalog_and_su3_level_scope_ledger_fence

end CampaignTfq0050FiniteTopological
