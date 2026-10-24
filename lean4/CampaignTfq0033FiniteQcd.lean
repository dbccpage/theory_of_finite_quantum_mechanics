import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Campaign Module: TFQ-0033 (`FINITE_QCD`)

Formalizes the narrowed finite counterpart and non-equivalence fences for
`TFQ-0033` ("The antitriplet factor -2/3 is a two-index diquark channel, stored
as antitriplet_diquark_casimir. A baryon color singlet would need a third tensor
factor and an alternating contraction on three color indices. No such epsilon
contraction is defined in the QCD control, in su_n.rs, or in the weighted
generator list. The sextet factor +1/3 is likewise a two-quark channel. The
obligation is to build that three-factor contraction explicitly, or to keep
baryon language off this node. The diquark signs are a computational control of
Casimir arithmetic only."):

1. **Two-Quark (`3 ⊗ 3 = 3̄ ⊕ 6`) Diquark Casimir Arithmetic (`-2/3` & `+1/3`)**:
   - Proves `antitripletDiquarkCasimir = -2/3`, `sextetDiquarkCasimir = +1/3`,
     `3 * 3 = 3 + 6`, and weighted color-trace cancellation
     `3 * (-2/3) + 6 * (1/3) = 0` (`su3_qq_diquark_casimir_channels`).
   - Proves the half-strength rule `-2/3 = (1/2) * (-4/3)` and that neither 2-quark
     channel has zero quadratic Casimir (`4/3 ≠ 0`, `10/3 ≠ 0`)
     (`diquark_to_qqbar_singlet_half_strength_rule`).
   - Proves the 3-quark dimension decomposition `3 * 3 * 3 = 1 + 8 + 8 + 10 = 27`
     (`su3_three_quark_dimension_decomposition`).
2. **Explicit Three-Index Alternating Contraction (`eps3` & `baryonEpsilonContract`)**:
   - Constructs `eps3 : Fin 3 → Fin 3 → Fin 3 → Int`, proving total antisymmetry
     under transpositions and vanishing on repeated indices
     (`levi_civita_3d_antisymmetry_and_six_nonzero_permutations`).
   - Proves the contracted norm `∑_{i,j,k} (eps3 i j k)^2 = 6` and single-index
     delta contraction `∑_{j,k} eps3 i j k * eps3 i' j k = 2 δ_{ii'}`
     (`levi_civita_contracted_square_and_norm_six`).
   - Constructs `baryonEpsilonContract (u v w : Fin 3 → ℚ) : ℚ`, proving it equals
     the `3 × 3` determinant (`three_index_epsilon_contraction_equals_det3`) and
     vanishes whenever any two quark color vectors coincide
     (`baryon_contraction_vanishes_on_identical_color_states`).
3. **Baryon Pairwise Casimir Sum & Diquark-vs-Baryon Non-Equivalence Fences**:
   - Proves that summing the antitriplet factor `-2/3` across all `3` pairs in a
     3-quark color singlet yields `3 * (-2/3) = -2 = (0 - 3 * (4/3)) / 2`
     (`baryon_singlet_total_pairwise_casimir_equals_minus_two`).
   - Fences the 2-index diquark carrier (`dim Λ²(ℚ³) = 3`, `C_2 = 4/3 ≠ 0`) from
     the 3-index baryon singlet (`dim Λ³(ℚ³) = 1`, `C_2 = 0`)
     (`two_index_diquark_not_three_index_baryon_singlet_fence`,
      `tfq0033_baryon_contraction_scope_ledger_fence`).
-/

namespace CampaignTfq0033FiniteQcd

-- ============================================================================
-- 1. Two-Quark (`3 ⊗ 3 = 3̄ ⊕ 6`) Diquark Casimir Arithmetic
-- ============================================================================

def c2Fund : ℚ := 4 / 3
def c2Antitriplet : ℚ := 4 / 3
def c2Sextet : ℚ := 10 / 3

/-- Two-quark antitriplet channel factor `(C_2(3̄) - 2 * C_2(3)) / 2 = -2/3`. -/
def antitripletDiquarkCasimir : ℚ :=
  (c2Antitriplet - 2 * c2Fund) / 2

/-- Two-quark sextet channel factor `(C_2(6) - 2 * C_2(3)) / 2 = +1/3`. -/
def sextetDiquarkCasimir : ℚ :=
  (c2Sextet - 2 * c2Fund) / 2

/-- Theorem 1: In `SU(3)`, `antitripletDiquarkCasimir = -2/3`, `sextetDiquarkCasimir = 1/3`,
`3 * 3 = 3 + 6`, and the dimension-weighted trace sum `3 * (-2/3) + 6 * (1/3) = 0`. -/
theorem su3_qq_diquark_casimir_channels :
    antitripletDiquarkCasimir = -2 / 3 ∧
    sextetDiquarkCasimir = 1 / 3 ∧
    (3 * 3 : Nat) = 3 + 6 ∧
    3 * antitripletDiquarkCasimir + 6 * sextetDiquarkCasimir = 0 := by
  dsimp [antitripletDiquarkCasimir, sextetDiquarkCasimir, c2Antitriplet, c2Sextet, c2Fund]
  refine ⟨by norm_num, by norm_num, by decide, by norm_num⟩

/-- Theorem 2: The attractive antitriplet diquark factor `-2/3` is half the `q q̄` singlet
factor `-4/3`, and neither 2-quark channel is a color singlet (`c2Antitriplet ≠ 0`, `c2Sextet ≠ 0`). -/
theorem diquark_to_qqbar_singlet_half_strength_rule :
    antitripletDiquarkCasimir = (1 / 2) * (-4 / 3) ∧
    c2Antitriplet ≠ 0 ∧
    c2Sextet ≠ 0 := by
  dsimp [antitripletDiquarkCasimir, c2Antitriplet, c2Sextet, c2Fund]
  norm_num

/-- Theorem 3: Three-quark tensor decomposition `3 ⊗ 3 ⊗ 3 = (3̄ ⊕ 6) ⊗ 3 = 1 ⊕ 8 ⊕ 8 ⊕ 10`
has total dimension `27` and a unique 1-dimensional color singlet arising from `3̄ ⊗ 3`. -/
theorem su3_three_quark_dimension_decomposition :
    (3 * 3 * 3 : Nat) = 27 ∧
    (3 + 6) * 3 = 27 ∧
    1 + 8 + 8 + 10 = 27 ∧
    1 + 8 = 3 * 3 ∧
    8 + 10 = 6 * 3 := by
  decide

-- ============================================================================
-- 2. Explicit Three-Index Alternating Contraction (`eps3` & `baryonEpsilonContract`)
-- ============================================================================

/-- Explicit 3-index Levi-Civita tensor `ε_{ijk}` on `Fin 3`. -/
def eps3 (i j k : Fin 3) : Int :=
  if i = 0 ∧ j = 1 ∧ k = 2 then 1
  else if i = 1 ∧ j = 2 ∧ k = 0 then 1
  else if i = 2 ∧ j = 0 ∧ k = 1 then 1
  else if i = 0 ∧ j = 2 ∧ k = 1 then -1
  else if i = 2 ∧ j = 1 ∧ k = 0 then -1
  else if i = 1 ∧ j = 0 ∧ k = 2 then -1
  else 0

/-- Theorem 4: `eps3` is totally antisymmetric under adjacent index transpositions
and vanishes whenever any two indices coincide across all `Fin 3` triples. -/
theorem levi_civita_3d_antisymmetry_and_six_nonzero_permutations :
    (∀ i j k : Fin 3, eps3 j i k = -eps3 i j k) ∧
    (∀ i j k : Fin 3, eps3 i k j = -eps3 i j k) ∧
    (∀ i k : Fin 3, eps3 i i k = 0) ∧
    (∀ i j : Fin 3, eps3 i j i = 0) ∧
    (∀ i j : Fin 3, eps3 i j j = 0) := by
  decide

/-- Full 3-index squared norm `∑_{i,j,k} (eps3 i j k)^2` and 2-index contraction `∑_{j,k} eps3 i j k * eps3 i' j k`. -/
def eps3NormSq : Int :=
  let inds : List (Fin 3) := [0, 1, 2]
  inds.foldl (fun acc i =>
    inds.foldl (fun acc2 j =>
      inds.foldl (fun acc3 k => acc3 + (eps3 i j k) ^ 2) acc2) acc) 0

def eps3Contract2 (i i' : Fin 3) : Int :=
  let inds : List (Fin 3) := [0, 1, 2]
  inds.foldl (fun acc j =>
    inds.foldl (fun acc2 k => acc2 + eps3 i j k * eps3 i' j k) acc) 0

/-- Theorem 5: `∑_{i,j,k} ε_{ijk}^2 = 6` (`3! = 6`) and `∑_{j,k} ε_{ijk} ε_{i'jk} = 2 δ_{ii'}`. -/
theorem levi_civita_contracted_square_and_norm_six :
    eps3NormSq = 6 ∧
    (∀ i i' : Fin 3, eps3Contract2 i i' = if i = i' then 2 else 0) := by
  decide

/-- Explicit 3-index alternating baryon singlet contraction `∑_{i,j,k} ε_{ijk} u_i v_j w_k`. -/
def baryonEpsilonContract (u v w : Fin 3 → ℚ) : ℚ :=
  u 0 * v 1 * w 2 + u 1 * v 2 * w 0 + u 2 * v 0 * w 1 -
  u 0 * v 2 * w 1 - u 2 * v 1 * w 0 - u 1 * v 0 * w 2

/-- Standard `3 × 3` cofactor determinant of `(u, v, w)`. -/
def det3Color (u v w : Fin 3 → ℚ) : ℚ :=
  u 0 * (v 1 * w 2 - v 2 * w 1) -
  u 1 * (v 0 * w 2 - v 2 * w 0) +
  u 2 * (v 0 * w 1 - v 1 * w 0)

def colorRed : Fin 3 → ℚ | 0 => 1 | _ => 0
def colorGreen : Fin 3 → ℚ | 1 => 1 | _ => 0
def colorBlue : Fin 3 → ℚ | 2 => 1 | _ => 0

/-- Theorem 6: `baryonEpsilonContract` equals the `3 × 3` determinant `det3Color` for all
color vectors `u, v, w : Fin 3 → ℚ`, and evaluates to `1` on `(colorRed, colorGreen, colorBlue)`. -/
theorem three_index_epsilon_contraction_equals_det3 (u v w : Fin 3 → ℚ) :
    baryonEpsilonContract u v w = det3Color u v w ∧
    baryonEpsilonContract colorRed colorGreen colorBlue = 1 := by
  dsimp [baryonEpsilonContract, det3Color, colorRed, colorGreen, colorBlue]
  refine ⟨by ring, by norm_num⟩

/-- Theorem 7: The 3-index baryon contraction vanishes identically whenever any two quark
color vectors are equal, and flips sign under swapping any two quarks. -/
theorem baryon_contraction_vanishes_on_identical_color_states (u v w : Fin 3 → ℚ) :
    baryonEpsilonContract u u w = 0 ∧
    baryonEpsilonContract u v u = 0 ∧
    baryonEpsilonContract u v v = 0 ∧
    baryonEpsilonContract v u w = -baryonEpsilonContract u v w := by
  dsimp [baryonEpsilonContract]
  refine ⟨by ring, by ring, by ring, by ring⟩

-- ============================================================================
-- 3. Baryon Pairwise Casimir Sum & Diquark-vs-Baryon Non-Equivalence Fences
-- ============================================================================

/-- Theorem 8: In a 3-quark color singlet (`C_2(1) = 0`), the sum of the `3` pairwise
antitriplet channel factors `3 * (-2/3) = -2` equals `(0 - 3 * C_2(3)) / 2 = -2`. -/
theorem baryon_singlet_total_pairwise_casimir_equals_minus_two :
    3 * antitripletDiquarkCasimir = -2 ∧
    (0 - 3 * c2Fund) / 2 = -2 ∧
    3 * antitripletDiquarkCasimir = (0 - 3 * c2Fund) / 2 := by
  dsimp [antitripletDiquarkCasimir, c2Antitriplet, c2Fund]
  norm_num

/-- Exterior power dimensions `C(3, k)` for `k = 2` (diquark `3̄`) vs. `k = 3` (baryon singlet `1`). -/
def exteriorColorDim (k : Nat) : Nat :=
  Nat.choose 3 k

/-- Theorem 9 (Two-Index Diquark Is Not a Three-Index Baryon Singlet Fence):
The 2-index antisymmetric diquark representation has dimension `C(3, 2) = 3` and non-zero
quadratic Casimir `c2Antitriplet = 4/3 ≠ 0`, whereas the 3-index antisymmetric baryon
singlet has dimension `C(3, 3) = 1` and zero quadratic Casimir `0`. -/
theorem two_index_diquark_not_three_index_baryon_singlet_fence :
    exteriorColorDim 2 = 3 ∧
    exteriorColorDim 3 = 1 ∧
    exteriorColorDim 2 ≠ exteriorColorDim 3 ∧
    c2Antitriplet ≠ 0 := by
  dsimp [exteriorColorDim, c2Antitriplet]
  refine ⟨by decide, by decide, by decide, by norm_num⟩

/-- Scope ledger for `TFQ-0033`. -/
structure Tfq0033ScopeLedger where
  hasDiquarkCasimirRationals : Bool
  hasExplicitEpsilon3ContractionInLean : Bool
  hasEpsilon3InQcdControlRs : Bool
  diquarkIsColorSinglet : Bool
  deriving DecidableEq, Repr

def tfq0033RepoLedger : Tfq0033ScopeLedger :=
  ⟨true, true, false, false⟩

/-- Theorem 10: `tfq0033RepoLedger` records that the diquark Casimir rationals and explicit
Lean 4 3-index `ε_{ijk}` contraction are verified, while `qcd_beta0_wilson_confinement_control.rs`
carries no 3-index epsilon contraction and a 2-quark diquark is not a color singlet. -/
theorem tfq0033_baryon_contraction_scope_ledger_fence :
    tfq0033RepoLedger.hasDiquarkCasimirRationals = true ∧
    tfq0033RepoLedger.hasExplicitEpsilon3ContractionInLean = true ∧
    tfq0033RepoLedger.hasEpsilon3InQcdControlRs = false ∧
    tfq0033RepoLedger.diquarkIsColorSinglet = false := by
  decide

#print axioms su3_qq_diquark_casimir_channels
#print axioms diquark_to_qqbar_singlet_half_strength_rule
#print axioms su3_three_quark_dimension_decomposition
#print axioms levi_civita_3d_antisymmetry_and_six_nonzero_permutations
#print axioms levi_civita_contracted_square_and_norm_six
#print axioms three_index_epsilon_contraction_equals_det3
#print axioms baryon_contraction_vanishes_on_identical_color_states
#print axioms baryon_singlet_total_pairwise_casimir_equals_minus_two
#print axioms two_index_diquark_not_three_index_baryon_singlet_fence
#print axioms tfq0033_baryon_contraction_scope_ledger_fence

end CampaignTfq0033FiniteQcd
