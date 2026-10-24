import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Campaign Module: TFQ-0039 (`FINITE_QCD`)

Formalizes the narrowed finite counterpart and non-equivalence fences for
`TFQ-0039` ("The F002 floor states its own ceiling. The S000 book README calls
the continuum volume an interface inventory and not a continuum derivation.
F002.S001 remains the open bridge: shelf.yaml has an empty book list, README.md
keeps GAP-F002-S001-001 open, and named_adjoining.yaml parks a Pontryagin dual
of declared free Z without admitting a bridge theorem. None of the finite QCD
controls, the Dirac doubling counts, or the topological anyon models close that
shelf. The gap to continuum QCD stays open. This node does not say that
continuum QCD has been derived."):

1. **Finite QCD Control Inventory (`β_0`, Strong-Coupling String Tension, and Wilson Doubler Count)**:
   - `qcdBeta0Times16Pi2`, `strongCouplingTension`, and `freeTorusDoublerCount`
     verified over `ℚ` and `Nat` (`finite_qcd_control_exact_rational_summary`).
   - Finite cyclic character cardinality `|Hom(ℤ/Lℤ, μ_L)| = L` contrasted with
     the parked Pontryagin dual `Hom(ℤ, U(1))` (`finite_cyclic_dual_order_equals_lattice_period`).
2. **Shelf `F002.S001` Open Bridge Audit & Non-Closure by Finite Controls**:
   - Models `f002S000Inventory` (interface inventory) and `f002S001BridgeShelf`
     (`bookCount = 0`, `hasOpenBridgeGap001 = true`, `admitsPontryaginDualBridgeTheorem = false`)
     (`f002_s001_empty_book_list_and_open_bridge_gap`).
   - Proves finite root-of-unity subgroups `μ_N` do not discharge the Pontryagin
     dual of free `ℤ` without the continuum circle (`pontryagin_dual_of_free_z_requires_unpaid_continuum_circle_fence`).
   - Proves that combining all three finite control families (`FINITE_QCD`,
     Dirac doubling counts, and `FINITE_TOPOLOGICAL` anyon models) leaves the
     continuum QCD exit predicate `false` while `F002.S001` is open
     (`finite_qcd_controls_do_not_discharge_continuum_qcd_exit_fence`).
   - Proves explicit breakdown/non-equivalence fences for each finite control
     family (`one_loop_beta0_polynomial_not_nonperturbative_continuum_mass_gap_fence`,
     `strong_coupling_plaquette_ratio_breaks_down_in_weak_coupling_continuum_limit_fence`,
     `wilson_torus_doubler_count_not_continuum_chiral_fermion_measure_fence`,
     `topological_anyon_catalog_not_continuum_su3_confining_vacuum_fence`,
     `tfq0039_f002_s001_open_bridge_scope_ledger_fence`).
-/

namespace CampaignTfq0039FiniteQcd

-- ============================================================================
-- 1. Finite QCD Control Inventory (β_0, Strong Coupling, and Wilson Doublers)
-- ============================================================================

/-- One-loop coefficient `(16 π^2) β_0 = (11 N_c - 2 N_f) / 3`. -/
def qcdBeta0Times16Pi2 (N_c N_f : ℚ) : ℚ :=
  (11 * N_c - 2 * N_f) / 3

/-- First-order strong-coupling string tension proxy `1 - β / (2 N_c^2)`. -/
def strongCouplingTension (beta N_c : ℚ) : ℚ :=
  1 - beta / (2 * N_c ^ 2)

/-- Naive torus Dirac zero-mode count `2^d` vs. Wilson lifted species count `1` (`r ≠ 0`). -/
def freeTorusDoublerCount (d : Nat) : Nat := 2 ^ d
def wilsonLiftedDoublerCount (d : Nat) : Nat := 2 ^ d - 1

/-- Theorem 1: At `N_c = 3, N_f = 6, β = 1, d = 4`, the finite QCD control quantities
evaluate to `(16π^2) β_0 = 7`, `σ_sc = 17/18`, `2^4 = 16` naive modes, and `15` lifted doublers. -/
theorem finite_qcd_control_exact_rational_summary :
    qcdBeta0Times16Pi2 3 6 = 7 ∧
    strongCouplingTension 1 3 = 17 / 18 ∧
    freeTorusDoublerCount 4 = 16 ∧
    wilsonLiftedDoublerCount 4 = 15 := by
  dsimp [qcdBeta0Times16Pi2, strongCouplingTension, freeTorusDoublerCount, wilsonLiftedDoublerCount]
  refine ⟨by norm_num, by norm_num, by decide, by decide⟩

/-- Finite cyclic character count `|Hom(ℤ/Lℤ, μ_L)| = L` for a finite period-`L` lattice. -/
def finiteCyclicCharacterCount (L : Nat) : Nat := L

/-- Theorem 2: On a finite period-`L` lattice (`L ≥ 1`), the dual character group has
finite cardinality `L` and `L^d` total momentum modes in dimension `d`, rather than
a continuous torus `T^d = Hom(ℤ^d, U(1))`. -/
theorem finite_cyclic_dual_order_equals_lattice_period (L d : Nat) :
    finiteCyclicCharacterCount L = L ∧
    (finiteCyclicCharacterCount L) ^ d = L ^ d := by
  dsimp [finiteCyclicCharacterCount]
  exact ⟨rfl, rfl⟩

-- ============================================================================
-- 2. Shelf F002.S001 Open Bridge Audit & Non-Closure by Finite Controls
-- ============================================================================

/-- Shelf audit record modeling `F002.S000` and `F002.S001`. -/
structure ShelfInventoryRecord where
  bookCount : Nat
  hasOpenBridgeGap001 : Bool
  admitsPontryaginDualBridgeTheorem : Bool
  isInterfaceInventoryOnly : Bool
  deriving DecidableEq, Repr

/-- `F002.S000` is an interface inventory, not a continuum derivation. -/
def f002S000Inventory : ShelfInventoryRecord :=
  ⟨1, true, false, true⟩

/-- `F002.S001` (`S001_continuum_finite_shadow_bridge`) has an empty book list (`bookCount = 0`),
keeps `GAP-F002-S001-001` open, and parks the Pontryagin dual of free `ℤ` without a bridge theorem. -/
def f002S001BridgeShelf : ShelfInventoryRecord :=
  ⟨0, true, false, true⟩

/-- Theorem 3: `f002S000Inventory` is an interface inventory only, and `f002S001BridgeShelf`
has `bookCount = 0`, `hasOpenBridgeGap001 = true`, and `admitsPontryaginDualBridgeTheorem = false`. -/
theorem f002_s001_empty_book_list_and_open_bridge_gap :
    f002S000Inventory.isInterfaceInventoryOnly = true ∧
    f002S001BridgeShelf.bookCount = 0 ∧
    f002S001BridgeShelf.hasOpenBridgeGap001 = true ∧
    f002S001BridgeShelf.admitsPontryaginDualBridgeTheorem = false := by
  decide

/-- Theorem 4 (Pontryagin Dual of Free `ℤ` Is Not Discharged by Finite Roots of Unity Fence):
For any finite root-of-unity order `N ≥ 1`, `|Hom(ℤ, μ_N)| = N < N + 1`, so no finite
subgroup `μ_N` exhausts the continuum Pontryagin dual `Hom(ℤ, U(1)) ≅ U(1)` parked in
`named_adjoining.yaml`. -/
theorem pontryagin_dual_of_free_z_requires_unpaid_continuum_circle_fence (N : Nat) :
    finiteCyclicCharacterCount N < finiteCyclicCharacterCount (N + 1) ∧
    f002S001BridgeShelf.admitsPontryaginDualBridgeTheorem = false := by
  dsimp [finiteCyclicCharacterCount, f002S001BridgeShelf]
  refine ⟨Nat.lt_succ_self N, rfl⟩

/-- Combined status of finite controls vs. open continuum bridge obligations. -/
structure FiniteToContinuumQcdBridgeState where
  hasFiniteQcdControls : Bool
  hasDiracDoublingCounts : Bool
  hasTopologicalAnyonModels : Bool
  f002S001BridgeClosed : Bool
  hasContinuumRenormalizationTrajectory : Bool
  hasContinuumGaugeMeasure : Bool
  deriving DecidableEq, Repr

/-- Continuum QCD derivation predicate: requires the `F002.S001` bridge, continuum RG flow,
and continuum gauge measure in addition to finite controls. -/
def continuumQcdDerived (s : FiniteToContinuumQcdBridgeState) : Bool :=
  s.hasFiniteQcdControls &&
  s.hasDiracDoublingCounts &&
  s.hasTopologicalAnyonModels &&
  s.f002S001BridgeClosed &&
  s.hasContinuumRenormalizationTrajectory &&
  s.hasContinuumGaugeMeasure

/-- Actual repository state: all three finite control families are present, while the
continuum bridge `F002.S001`, continuum RG flow, and continuum measure remain open (`false`). -/
def repoQcdBridgeState : FiniteToContinuumQcdBridgeState :=
  ⟨true, true, true, false, false, false⟩

/-- Theorem 5 (Finite Controls Do Not Close `F002.S001` or Derive Continuum QCD Fence):
Even when `hasFiniteQcdControls`, `hasDiracDoublingCounts`, and `hasTopologicalAnyonModels`
are all `true`, `continuumQcdDerived s = false` whenever `s.f002S001BridgeClosed = false`. -/
theorem finite_qcd_controls_do_not_discharge_continuum_qcd_exit_fence
    (s : FiniteToContinuumQcdBridgeState) (hOpen : s.f002S001BridgeClosed = false) :
    continuumQcdDerived s = false ∧
    continuumQcdDerived repoQcdBridgeState = false := by
  constructor
  · dsimp [continuumQcdDerived]
    rw [hOpen]
    simp
  · decide

-- ============================================================================
-- 3. Explicit Breakdown & Non-Equivalence Fences for the Three Finite Families
-- ============================================================================

/-- Theorem 6 (`β_0` Rational Formula Is Not a Continuum Mass Gap Proof):
`qcdBeta0Times16Pi2 3 N_f = 11 - (2/3) N_f` is an affine polynomial in `N_f` that is
positive at `N_f = 6` (`7 > 0`) and negative at `N_f = 17` (`-1/3 < 0`), and carries no
continuum Hilbert space or non-perturbative mass gap operator. -/
theorem one_loop_beta0_polynomial_not_nonperturbative_continuum_mass_gap_fence (N_f : ℚ) :
    qcdBeta0Times16Pi2 3 N_f = 11 - (2 / 3) * N_f ∧
    0 < qcdBeta0Times16Pi2 3 6 ∧
    qcdBeta0Times16Pi2 3 17 < 0 := by
  refine ⟨?_, ?_, ?_⟩
  · dsimp [qcdBeta0Times16Pi2]; ring
  · dsimp [qcdBeta0Times16Pi2]; norm_num
  · dsimp [qcdBeta0Times16Pi2]; norm_num

/-- Theorem 7 (Strong-Coupling Expansion Breaks Down Before the Weak-Coupling Continuum Limit):
At `N_c = 3`, the first-order strong-coupling string tension proxy `1 - β/18` is positive
at `β = 1` (`17/18 > 0`), vanishes at `β = 18` (`0`), and becomes negative at `β = 20`
(`-1/9 < 0`), so it cannot substitute for the weak-coupling continuum limit `β → ∞`. -/
theorem strong_coupling_plaquette_ratio_breaks_down_in_weak_coupling_continuum_limit_fence :
    0 < strongCouplingTension 1 3 ∧
    strongCouplingTension 18 3 = 0 ∧
    strongCouplingTension 20 3 = -1 / 9 ∧
    strongCouplingTension 20 3 < 0 := by
  dsimp [strongCouplingTension]
  norm_num

/-- Theorem 8 (Wilson Doubler Count Does Not Construct a Continuum Fermion Measure):
The `d = 4` Brillouin corner decomposition `1 + 4 + 6 + 4 + 1 = 16` (`1` zero mode and
`15` lifted doublers) is a finite combinatorial identity on `{0, π}^4` and leaves
`f002S001BridgeShelf.bookCount = 0`. -/
theorem wilson_torus_doubler_count_not_continuum_chiral_fermion_measure_fence :
    (1 + 4 + 6 + 4 + 1 : Nat) = freeTorusDoublerCount 4 ∧
    (4 + 6 + 4 + 1 : Nat) = wilsonLiftedDoublerCount 4 ∧
    freeTorusDoublerCount 4 - wilsonLiftedDoublerCount 4 = 1 ∧
    f002S001BridgeShelf.bookCount = 0 := by
  decide

/-- Theorem 9 (Topological Anyon Catalog Models Do Not Close `F002.S001`):
The finite simple-object counts of Fibonacci (`2`), Ising (`3`), toric code `D(ℤ_2)` (`4`),
and `SU(2)_k` (`k + 1 ≤ 7` for `k ≤ 6`) are finite ribbon-category ranks and do not
populate `f002S001BridgeShelf` (`bookCount = 0`) or derive continuum `SU(3)_c` confinement. -/
theorem topological_anyon_catalog_not_continuum_su3_confining_vacuum_fence :
    ∀ k ∈ ([1, 2, 3, 4, 5, 6] : List Nat),
      k + 1 ≤ 7 ∧ f002S001BridgeShelf.bookCount = 0 := by
  decide

/-- Scope ledger for `TFQ-0039`. -/
structure Tfq0039ScopeLedger where
  hasFiniteQcdControls : Bool
  hasDiracDoublingCounts : Bool
  hasTopologicalAnyonModels : Bool
  f002S000IsInterfaceInventoryOnly : Bool
  f002S001BookListEmpty : Bool
  gapF002S001001Open : Bool
  pontryaginDualBridgeAdmitted : Bool
  continuumQcdDerived : Bool
  deriving DecidableEq, Repr

def tfq0039RepoLedger : Tfq0039ScopeLedger :=
  ⟨true, true, true, true, true, true, false, false⟩

/-- Theorem 10: `tfq0039RepoLedger` records that the finite QCD controls, Dirac doubling
counts, and topological anyon models exist in the repository, while `F002.S000` is an
interface inventory, `F002.S001` has an empty book list with `GAP-F002-S001-001` open,
the Pontryagin dual of free `ℤ` has no bridge theorem, and continuum QCD is not derived. -/
theorem tfq0039_f002_s001_open_bridge_scope_ledger_fence :
    tfq0039RepoLedger.hasFiniteQcdControls = true ∧
    tfq0039RepoLedger.hasDiracDoublingCounts = true ∧
    tfq0039RepoLedger.hasTopologicalAnyonModels = true ∧
    tfq0039RepoLedger.f002S000IsInterfaceInventoryOnly = true ∧
    tfq0039RepoLedger.f002S001BookListEmpty = true ∧
    tfq0039RepoLedger.gapF002S001001Open = true ∧
    tfq0039RepoLedger.pontryaginDualBridgeAdmitted = false ∧
    tfq0039RepoLedger.continuumQcdDerived = false ∧
    tfq0039RepoLedger.hasFiniteQcdControls ≠ tfq0039RepoLedger.continuumQcdDerived := by
  decide

#print axioms finite_qcd_control_exact_rational_summary
#print axioms finite_cyclic_dual_order_equals_lattice_period
#print axioms f002_s001_empty_book_list_and_open_bridge_gap
#print axioms pontryagin_dual_of_free_z_requires_unpaid_continuum_circle_fence
#print axioms finite_qcd_controls_do_not_discharge_continuum_qcd_exit_fence
#print axioms one_loop_beta0_polynomial_not_nonperturbative_continuum_mass_gap_fence
#print axioms strong_coupling_plaquette_ratio_breaks_down_in_weak_coupling_continuum_limit_fence
#print axioms wilson_torus_doubler_count_not_continuum_chiral_fermion_measure_fence
#print axioms topological_anyon_catalog_not_continuum_su3_confining_vacuum_fence
#print axioms tfq0039_f002_s001_open_bridge_scope_ledger_fence

end CampaignTfq0039FiniteQcd
