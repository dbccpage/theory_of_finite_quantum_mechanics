import FrontierHappyMincut
import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

/-!
# ADS-HAPPY-TOY-NOT-DUALITY-GAP (TFQ-2212)

AuthorityEffect: None.

This module formalizes exact mathematical non-equivalence fences showing why finite
HaPPY stabilizer-code tensor networks (Pastawski-Yoshida-Harlow-Preskill 2015,
arXiv:1503.06237) are discrete kinematic toy models and do NOT derive continuum
AdS/CFT or the continuum Ryu-Takayanagi minimal-surface formula:

1. **Flat Stabilizer Rényi Spectrum vs. Continuum CFT Rényi Scaling**:
   Every stabilizer reduced density matrix on a boundary region `A` is proportional to
   a projector of rank `2^{S(A)}`, so its Rényi-`n` entropy ratio `stabilizerRenyiFactor n = 1`
   is independent of `n`. In contrast, a 2D CFT interval with von Neumann entropy `S_1 > 0`
   satisfies the Calabrese-Cardy / Ryu-Takayanagi Rényi scaling
   `S_n^{CFT} = ((1 + 1 / n) / 2) * S_1 = cftRenyiFactor n * S_1`, producing a strictly
   positive Rényi spectrum defect `((n - 1) / (2 * n)) * S_1 > 0` for all `n > 1`.

2. **Explicit Ryu-Takayanagi Minimal-Cut Deficit Witnesses and Length Census on the HaPPY Patch**:
   On the 20-qubit boundary state of the 6-pentagon `{5,4}` HaPPY patch (`FrontierHappyMincut`,
   with all 6 bulk legs fixed in `|0_L⟩`), the contiguous interval `(start = 2, len = 8)` and
   its complement `(start = 2, len = 12)` satisfy `S(A) = 4 < 5 = mincut(A)` along a 5-fold
   rotational orbit `start = 4 * k + 2`. Across all 380 proper contiguous intervals,
   every interval of length `1..7` or `13..19` satisfies `S(A) = mincut(A)`, whereas lengths
   `8, 9, 10, 11, 12` exhibit exactly `5, 10, 10, 10, 5` strict deficits (`S(A) = mincut(A) - 1`),
   summing to `40`.

3. **General-Region Mutual Information Jumps and Bulk-to-Boundary Hilbert Codimension**:
   On the 20-qubit HaPPY boundary state, separated single-qubit regions `[0]` and `[8]`
   and separated 4-qubit outer pentagons `[0,1,2,3]` and `[8,9,10,11]` have zero mutual
   information, whereas two halves `[0,1]` and `[2,3]` of one outer pentagon have mutual
   information `3` bits and `[0..7]` with `[8..11]` has mutual information `1` bit.
   Finally, for `N_bulk < N_bdry`, the bulk code subspace `2^{N_bulk}` has strictly positive
   orthogonal codimension `2^{N_bdry} - 2^{N_bulk} > 0` (`30` for 1 pentagon, `1048512` for
   the 6-pentagon star patch, and `33552384` for the 11-pentagon `{5,4}` 1-ring).

This module does NOT derive AdS/CFT or continuum gravity. The node status remains `OPEN`.
-/

namespace AdsHappyToyNotDualityGap

open FrontierHappyMincut

/-! ## 1. Flat Stabilizer Rényi Spectrum vs. Continuum CFT Rényi Scaling -/

/-- Normalized Rényi-`n` to von Neumann entropy ratio `S_n / S_1 = 1` of any stabilizer state. -/
def stabilizerRenyiFactor (_n : ℚ) : ℚ :=
  1

/-- Normalized Rényi-`n` to von Neumann entropy ratio `S_n^{CFT} / S_1^{CFT} = (1 + 1/n) / 2`
for a single interval in a 2D conformal field theory (Calabrese-Cardy / Dong cosmic brane). -/
def cftRenyiFactor (n : ℚ) : ℚ :=
  (1 + 1 / n) / 2

/-- Difference `S_n^{stab}(S_1) - S_n^{CFT}(S_1)` between a flat-spectrum stabilizer state
and a 2D CFT state of the same von Neumann entropy `S_1`. -/
def renyiSpectrumDefect (n S1 : ℚ) : ℚ :=
  stabilizerRenyiFactor n * S1 - cftRenyiFactor n * S1

/-- At `n = 1`, the CFT Rényi factor equals the stabilizer factor `1`. -/
theorem cftRenyiFactor_one :
    cftRenyiFactor 1 = stabilizerRenyiFactor 1 ∧ cftRenyiFactor 1 = 1 := by
  dsimp [cftRenyiFactor, stabilizerRenyiFactor]
  norm_num

/-- Concrete CFT Rényi factors at `n = 2, 3, 4` (`3/4`, `2/3`, `5/8`) and their nonzero
defects (`1/4`, `1/3`, `3/8`) relative to the flat stabilizer factor `1`. -/
theorem recorded_cft_vs_stabilizer_renyi_factors :
    cftRenyiFactor 2 = 3 / 4 ∧
      cftRenyiFactor 3 = 2 / 3 ∧
      cftRenyiFactor 4 = 5 / 8 ∧
      renyiSpectrumDefect 2 1 = 1 / 4 ∧
      renyiSpectrumDefect 3 1 = 1 / 3 ∧
      renyiSpectrumDefect 4 1 = 3 / 8 := by
  dsimp [cftRenyiFactor, renyiSpectrumDefect, stabilizerRenyiFactor]
  norm_num

/-- Exact rational decomposition `cftRenyiFactor n - 1/2 = 1 / (2 n)` above the `n → ∞`
min-entropy floor `1/2`. -/
theorem cftRenyiFactor_sub_half (n : ℚ) :
    cftRenyiFactor n - 1 / 2 = 1 / (2 * n) := by
  dsimp [cftRenyiFactor]
  ring

/-- Closed-form expression for the Rényi spectrum defect:
`renyiSpectrumDefect n S1 = ((n - 1) / (2 * n)) * S1` for `n ≠ 0`. -/
theorem renyiSpectrumDefect_formula (n S1 : ℚ) (hn : n ≠ 0) :
    renyiSpectrumDefect n S1 = ((n - 1) / (2 * n)) * S1 := by
  dsimp [renyiSpectrumDefect, stabilizerRenyiFactor, cftRenyiFactor]
  field_simp [hn]
  ring

/-- For every Rényi index `n > 1` and every positive entropy `S1 > 0`, the stabilizer Rényi
entropy strictly exceeds the CFT Rényi entropy (`0 < renyiSpectrumDefect n S1`). -/
theorem renyiSpectrumDefect_pos_of_gt_one (n S1 : ℚ) (hn : 1 < n) (hS : 0 < S1) :
    0 < renyiSpectrumDefect n S1 := by
  have hn0 : n ≠ 0 := by linarith
  rw [renyiSpectrumDefect_formula n S1 hn0]
  have hnum : 0 < n - 1 := by linarith
  have hden : 0 < 2 * n := by linarith
  exact mul_pos (div_pos hnum hden) hS

/-- No stabilizer state with positive von Neumann entropy `S1 > 0` can match the 2D CFT
Rényi-`n` entropy at any `n > 1`. -/
theorem cft_ne_stabilizer_renyi_of_gt_one (n S1 : ℚ) (hn : 1 < n) (hS : 0 < S1) :
    cftRenyiFactor n * S1 ≠ stabilizerRenyiFactor n * S1 := by
  have hpos := renyiSpectrumDefect_pos_of_gt_one n S1 hn hS
  dsimp [renyiSpectrumDefect] at hpos
  linarith

/-- The 2D CFT Rényi factor is strictly decreasing on `0 < m < n`, whereas the stabilizer
Rényi factor is constant. -/
theorem cftRenyiFactor_strict_anti (m n : ℚ) (hm : 0 < m) (hmn : m < n) :
    cftRenyiFactor n < cftRenyiFactor m := by
  have hn : 0 < n := lt_trans hm hmn
  have hm0 : m ≠ 0 := ne_of_gt hm
  have hn0 : n ≠ 0 := ne_of_gt hn
  have hid : cftRenyiFactor m - cftRenyiFactor n = (n - m) / (2 * m * n) := by
    dsimp [cftRenyiFactor]
    field_simp [hm0, hn0]
    ring
  have hnum : 0 < n - m := by linarith
  have hden : 0 < 2 * m * n := mul_pos (mul_pos (by norm_num) hm) hn
  have hpos : 0 < cftRenyiFactor m - cftRenyiFactor n := by
    rw [hid]
    exact div_pos hnum hden
  linarith

/-! ## 2. Explicit Ryu-Takayanagi Minimal-Cut Deficit Witnesses on the HaPPY `{5,4}` Patch -/

/-- Count of contiguous boundary intervals of fixed length `len` (`start ∈ 0..19`) on the
20-qubit HaPPY patch where `S(A) + 1 = mincut(A)`. -/
def deficitCountAtLength (len : Nat) : Nat :=
  ((List.range 20).filter fun s => intervalEntropy s len + 1 == intervalMincut s len).length

/-- Count of contiguous boundary intervals of fixed length `len` (`start ∈ 0..19`) on the
20-qubit HaPPY patch where `S(A) = mincut(A)`. -/
def exactMincutCountAtLength (len : Nat) : Nat :=
  ((List.range 20).filter fun s => intervalEntropy s len == intervalMincut s len).length

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
/-- Explicit contiguous 8-qubit boundary interval `(start = 2, len = 8)` (qubits `2..9`,
splitting outer pentagons `0` and `2` each `2|2` across outer pentagon `1`) where the
stabilizer entropy is `4` bits while the minimal bond cut is `5` bonds (`S(A) < mincut(A)`). -/
theorem happy_witness_start2_len8_deficit :
    intervalEntropy 2 8 = 4 ∧
      intervalMincut 2 8 = 5 ∧
      intervalEntropy 2 8 < intervalMincut 2 8 := by
  decide

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
/-- Explicit complementary 12-qubit boundary interval `(start = 2, len = 12)` where the
stabilizer entropy is `4` bits while the minimal bond cut is `5` bonds (`S(A) < mincut(A)`). -/
theorem happy_witness_start2_len12_deficit :
    intervalEntropy 2 12 = 4 ∧
      intervalMincut 2 12 = 5 ∧
      intervalEntropy 2 12 < intervalMincut 2 12 := by
  decide

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
/-- Five-fold rotational orbit of the length-8 Ryu-Takayanagi deficit witness across all five
outer pentagons (`start = 4 * k + 2` for `k = 0, 1, 2, 3, 4`). -/
theorem happy_fivefold_rotational_deficit_orbit :
    ((List.range 5).all fun k =>
      intervalEntropy (4 * k + 2) 8 == 4 && intervalMincut (4 * k + 2) 8 == 5) = true := by
  decide

set_option maxRecDepth 20000 in
set_option maxHeartbeats 1600000 in
/-- Every contiguous boundary interval of length `1..7` or `13..19` satisfies exact equality
`S(A) = mincut(A)` (`20` intervals per length, `0` deficits). -/
theorem happy_short_and_long_intervals_exact_mincut :
    (([1, 2, 3, 4, 5, 6, 7, 13, 14, 15, 16, 17, 18, 19] : List Nat).all fun len =>
      exactMincutCountAtLength len == 20 && deficitCountAtLength len == 0) = true := by
  decide

set_option maxRecDepth 20000 in
set_option maxHeartbeats 1600000 in
/-- Complete length-resolved census of the 40 Ryu-Takayanagi deficit intervals on the 6-pentagon
HaPPY patch: lengths `8, 9, 10, 11, 12` contribute `5, 10, 10, 10, 5` strict deficits respectively,
summing to `40`. -/
theorem happy_deficit_distribution_by_length :
    deficitCountAtLength 8 = 5 ∧
      deficitCountAtLength 9 = 10 ∧
      deficitCountAtLength 10 = 10 ∧
      deficitCountAtLength 11 = 10 ∧
      deficitCountAtLength 12 = 5 ∧
      deficitCountAtLength 8 + deficitCountAtLength 9 + deficitCountAtLength 10 +
        deficitCountAtLength 11 + deficitCountAtLength 12 = 40 := by
  decide

/-! ## 3. General-Region Mutual Information Jumps and Bulk-to-Boundary Hilbert Codimension -/

/-- 40-bit symplectic bitmask selecting an arbitrary list `qs` of boundary qubits (`0..19`). -/
def regionBitmask40 (qs : List Nat) : Nat :=
  qs.foldl (fun acc q => acc ||| (3 <<< (2 * q))) 0

/-- Stabilizer entanglement entropy `S(A) = rank(G|_A) - |A|` in bits for a list `qs` of
distinct boundary qubits on the 20-qubit HaPPY boundary state. -/
def regionEntropy (qs : List Nat) : Nat :=
  let mask40 := regionBitmask40 qs
  let rows := boundaryGens20.map (fun r => r &&& mask40)
  gf2Rank rows - qs.length

/-- Mutual information `I(A : B) = S(A) + S(B) - S(A ∪ B)` in bits between disjoint boundary
qubit lists `A` and `B`. -/
def regionMutualInformation (A B : List Nat) : Nat :=
  regionEntropy A + regionEntropy B - regionEntropy (A ++ B)

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
/-- Disconnected boundary regions on the 20-qubit HaPPY state exhibit discrete integer jumps
in mutual information:
- Separated single boundary qubits `[0]` and `[8]` have `I([0] : [8]) = 0`.
- Two separated 4-qubit outer pentagons `P0 = [0,1,2,3]` and `P2 = [8,9,10,11]` each have
  entropy `1` bit (cut along their single internal bond to the central pentagon) and
  joint entropy `2` bits, so `I(P0 : P2) = 0`.
- Two halves `[0,1]` and `[2,3]` of outer pentagon `P0` each have entropy `2` bits while
  `S(P0) = 1` bit, so `I([0,1] : [2,3]) = 3` bits.
- Two outer pentagons `P0 ∪ P1 = [0..7]` (`S = 2`) and `P2 = [8..11]` (`S = 1`) have joint
  entropy `2` bits (cutting the remaining two central-pentagon bonds), so
  `I(P0 ∪ P1 : P2) = 1` bit. -/
theorem happy_disconnected_mutual_information_witnesses :
    regionEntropy [0] = 1 ∧ regionEntropy [8] = 1 ∧
      regionMutualInformation [0] [8] = 0 ∧
      regionEntropy [0, 1, 2, 3] = 1 ∧ regionEntropy [8, 9, 10, 11] = 1 ∧
      regionEntropy [0, 1, 2, 3, 8, 9, 10, 11] = 2 ∧
      regionMutualInformation [0, 1, 2, 3] [8, 9, 10, 11] = 0 ∧
      regionEntropy [0, 1] = 2 ∧ regionEntropy [2, 3] = 2 ∧
      regionMutualInformation [0, 1] [2, 3] = 3 ∧
      regionEntropy [0, 1, 2, 3, 4, 5, 6, 7] = 2 ∧
      regionEntropy [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] = 2 ∧
      regionMutualInformation [0, 1, 2, 3, 4, 5, 6, 7] [8, 9, 10, 11] = 1 := by
  decide

/-- Hilbert space dimension `2^n` of `n` qubits. -/
def qubitHilbertDim (n : Nat) : Nat :=
  2 ^ n

/-- Orthogonal complement dimension `2^{nBdry} - 2^{nBulk}` of an isometric bulk-to-boundary
code embedding `nBulk` logical qubits into `nBdry` physical boundary qubits. -/
def codeOrthogonalCodim (nBulk nBdry : Nat) : Nat :=
  qubitHilbertDim nBdry - qubitHilbertDim nBulk

/-- Whenever a finite tensor-network code has fewer bulk logical qubits than boundary qubits
(`nBulk < nBdry`), the encoded bulk subspace has strictly smaller Hilbert dimension than the
boundary space and a strictly positive orthogonal codimension. -/
theorem code_subspace_strict_codimension {nBulk nBdry : Nat} (h : nBulk < nBdry) :
    qubitHilbertDim nBulk < qubitHilbertDim nBdry ∧
      0 < codeOrthogonalCodim nBulk nBdry := by
  dsimp [qubitHilbertDim, codeOrthogonalCodim]
  have hlt : 2 ^ nBulk < 2 ^ nBdry := Nat.pow_lt_pow_right (by decide : 1 < 2) h
  exact ⟨hlt, Nat.sub_pos_of_lt hlt⟩

/-- Concrete bulk vs. boundary qubit and Hilbert-space dimension counts across the first three
radial `{5,4}` pentagon patch sizes:
- Single pentagon (`nBulk = 1, nBdry = 5`): `2^1 = 2`, `2^5 = 32`, codimension `30`.
- 6-pentagon star patch (`nBulk = 6, nBdry = 20`): `2^6 = 64`, `2^20 = 1048576`, codimension `1048512`.
- 11-pentagon closed `{5,4}` 1-ring (`nBulk = 11, nBdry = 25`): `2^11 = 2048`,
  `2^25 = 33554432`, codimension `33552384`. -/
theorem recorded_happy_tiling_hilbert_codimensions :
    qubitHilbertDim 1 = 2 ∧ qubitHilbertDim 5 = 32 ∧ codeOrthogonalCodim 1 5 = 30 ∧
      qubitHilbertDim 6 = 64 ∧ qubitHilbertDim 20 = 1048576 ∧ codeOrthogonalCodim 6 20 = 1048512 ∧
      qubitHilbertDim 11 = 2048 ∧ qubitHilbertDim 25 = 33554432 ∧
      codeOrthogonalCodim 11 25 = 33552384 := by
  dsimp [qubitHilbertDim, codeOrthogonalCodim]
  norm_num

#print axioms cftRenyiFactor_one
#print axioms recorded_cft_vs_stabilizer_renyi_factors
#print axioms cftRenyiFactor_sub_half
#print axioms renyiSpectrumDefect_formula
#print axioms renyiSpectrumDefect_pos_of_gt_one
#print axioms cft_ne_stabilizer_renyi_of_gt_one
#print axioms cftRenyiFactor_strict_anti
#print axioms happy_witness_start2_len8_deficit
#print axioms happy_witness_start2_len12_deficit
#print axioms happy_fivefold_rotational_deficit_orbit
#print axioms happy_short_and_long_intervals_exact_mincut
#print axioms happy_deficit_distribution_by_length
#print axioms happy_disconnected_mutual_information_witnesses
#print axioms code_subspace_strict_codimension
#print axioms recorded_happy_tiling_hilbert_codimensions

end AdsHappyToyNotDualityGap
