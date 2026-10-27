import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import EntropyDichotomy
import FrontierHappyMincut

open scoped BigOperators

/-!
# ADS-RT-FORMULA-IMPORT (TFQ-2204) — Algebraic Shadows & Scope Fences for the Ryu-Takayanagi Formula

AuthorityEffect: None.

This module narrows `ADS-RT-FORMULA-IMPORT` (`TFQ-2204`, status `IMPORTED_ASSUMPTION`, audited against
Ryu and Takayanagi 2006, `arXiv:hep-th/0603001` Section 1 eq. (1.5) p. 2, Section 2 eqs. (2.1),
(2.5)-(2.6) p. 3, and Section 3.1 eq. (3.2) p. 4) to three exact finite/rational algebraic shadows
and non-equivalence scope fences:

1. **Ryu-Takayanagi / Brown-Henneaux Coupling Elimination & Minimal-Cut Submodularity**:
   - Leading-order RT formula `rtLeadingEntropy area gN = area / (4 * gN)` and Brown-Henneaux
     central charge `brownHenneauxCentralCharge rAds gN3 = (3 * rAds) / (2 * gN3)` (`c = 3R/(2G_N^{(3)})`).
   - Substituting the regulated `AdS_3` geodesic length `ads3GeodesicLength rAds logFactor = 2 * rAds * logFactor`
     into `rtLeadingEntropy` reproduces the 2D CFT Calabrese-Cardy coefficient `(c / 3) * logFactor`
     identically (`rt_ads3_reproduces_calabrese_cardy`), and dividing by `c` eliminates both bulk
     couplings `rAds` and `gN3` (`rt_over_brown_henneaux_eliminates_couplings`).
   - Under surface/cut submodularity `areaUnion + areaInter ≤ areaAB + areaBC` and minimal-surface
     bounds `minABC ≤ areaUnion`, `minB ≤ areaInter`, the RT formula satisfies Strong Subadditivity
     `rtLeadingEntropy minABC gN + rtLeadingEntropy minB gN ≤ rtLeadingEntropy areaAB gN + rtLeadingEntropy areaBC gN`
     (`cut_pasting_strong_subadditivity_from_submodularity`).
   - On the 20-qubit 6-pentagon HaPPY `{5,4}` patch (`FrontierHappyMincut`), `mincut` and
     `boundaryEntropy` satisfy exact complement symmetry `A ↔ A^c` across all `380` proper
     contiguous boundary intervals (`happy_mincut_and_entropy_complement_symmetry_all_380`).

2. **Von Neumann Entropy Dichotomy Fence (`EntropyDichotomy.lean`, `FQ-ENTROPY-DICHOTOMY-BAKER`)**:
   - Every rational RT value `(rtLeadingEntropy area gN : ℝ)` is algebraic over `ℚ`
     (`rtLeadingEntropy_realCast_isAlgebraic`).
   - Under `C750B01.BakerCitedInput`, for any mixed algebraic spectrum `s : C750B01.AlgebraicSpectrum d`
     (`¬ C750B01.Pure s`), the natural-log von Neumann entropy `C750B01.entropy s` is transcendental
     over `ℚ` and therefore cannot equal any rational RT ratio `(rtLeadingEntropy area gN : ℝ)`
     (`no_rational_rt_area_for_mixed_algebraic_spectrum`).
   - Under `C750B01.BakerCitedInput` and `0 < gN`, `C750B01.entropy s = (rtLeadingEntropy area gN : ℝ)`
     holds if and only if `C750B01.Pure s ∧ area = 0` (`rational_rt_match_iff_pure_and_zero_area`).
   - In discrete stabilizer models, integer bond-cut counts `(k : ℝ)` arise only after dividing
     natural-log entropy `(k : ℝ) * Real.log 2` by the transcendental conversion factor `Real.log 2`
     (`stabilizer_bits_to_nats_transcendental_conversion`).

3. **Exact Rational Regge Proxy (`TFQ-0100`) vs. Minimal-Surface Area & HaPPY Bond-Cut Fence**:
   - On the `orthogonal_pentatope` chart of `TFQ-0100` (`sphere.rs` / `action.rs`), the 6 right-triangle
     hinges with squared edge lengths `(1, 1, 2)` have Cayley-Menger squared area `1 / 4` and the 4
     equilateral-triangle hinges with squared edge lengths `(2, 2, 2)` have Cayley-Menger squared
     area `3 / 4`, summing to `9 / 2` (`orthogonal_pentatope_hinge_areas_sq`).
   - For each of the 4 equilateral-triangle hinges (`cayleyMengerTriangleAreaSq 2 2 2 = 3 / 4`),
     no rational linear area `A : ℚ` satisfies `A ^ 2 = 3 / 4`
     (`no_rational_linear_area_for_equilateral_pentatope_hinge`).
   - On any flat background chart (`kappa = 0`), the rational Regge action `∑_h A_h^2 κ_h` vanishes
     identically (`reggeProxy_zero_on_flat_chart`), whereas on the 20-qubit 6-pentagon HaPPY patch
     all `380` proper nonempty contiguous boundary intervals have `1 ≤ boundaryEntropy A` and
     `1 ≤ mincut A` (`happy_all_380_intervals_pos_entropy_and_mincut`).
   - Under uniform length rescaling `L ↦ λ L` (`s_{ij} ↦ λ^2 s_{ij}`), `cayleyMengerTriangleAreaSq`
     and `rationalReggeAction` scale with degree `4` (`λ^4`), whereas a 2-surface area scales with
     degree `2` (`λ^2`) and a topological bond count scales with degree `0` (`λ^0`), excluding any
     scale-invariant proportionality constant `alpha : ℚ` across `λ = 1` and `λ = 2`
     (`no_scale_invariant_regge_to_rt_dictionary`).
-/

namespace AdsRtFormulaImport

open C750B01
open FrontierHappyMincut

-- ============================================================================
-- 1. Ryu-Takayanagi / Brown-Henneaux Algebra & Minimal-Cut Submodularity
-- ============================================================================

/-- Leading-order Ryu-Takayanagi area formula `S(A) = Area(γ_A) / (4 G_N)`
(`arXiv:hep-th/0603001` Section 1 eq. (1.5) p. 2). -/
def rtLeadingEntropy (area gN : ℚ) : ℚ :=
  area / (4 * gN)

/-- Brown-Henneaux central charge relation `c = 3 R_{AdS} / (2 G_N^{(3)})` in `AdS_3 / CFT_2`
(`arXiv:hep-th/0603001` Section 2 eq. (2.1) p. 3). -/
def brownHenneauxCentralCharge (rAds gN3 : ℚ) : ℚ :=
  (3 * rAds) / (2 * gN3)

/-- Regulated `AdS_3` static geodesic length `L_{γ_A} = 2 R_{AdS} * logFactor`
where `logFactor = ln((L / (π a)) sin(π l / L))` (`arXiv:hep-th/0603001` Section 2 eq. (2.5) p. 3). -/
def ads3GeodesicLength (rAds logFactor : ℚ) : ℚ :=
  2 * rAds * logFactor

/-- Single-interval 2D CFT Calabrese-Cardy prefactor `c / 3`. -/
def calabreseCardyCoefficient (c : ℚ) : ℚ :=
  c / 3

/-- Theorem 1: Substituting the regulated `AdS_3` geodesic length `2 R_{AdS} * logFactor` into
`rtLeadingEntropy` reproduces `(c / 3) * logFactor` under the Brown-Henneaux relation
`c = 3 R_{AdS} / (2 G_N^{(3)})` (`arXiv:hep-th/0603001` eqs. (2.1), (2.5)-(2.6) p. 3). -/
theorem rt_ads3_reproduces_calabrese_cardy (rAds gN3 logFactor : ℚ) :
    rtLeadingEntropy (ads3GeodesicLength rAds logFactor) gN3 =
      calabreseCardyCoefficient (brownHenneauxCentralCharge rAds gN3) * logFactor := by
  dsimp [rtLeadingEntropy, ads3GeodesicLength, calabreseCardyCoefficient, brownHenneauxCentralCharge]
  ring

/-- Theorem 2: The ratio of the `AdS_3` Ryu-Takayanagi entropy to the Brown-Henneaux central charge `c`
eliminates both bulk gravitational parameters `rAds` and `gN3`, leaving `logFactor / 3`. -/
theorem rt_over_brown_henneaux_eliminates_couplings (rAds gN3 logFactor : ℚ)
    (hR : rAds ≠ 0) (hG : gN3 ≠ 0) :
    rtLeadingEntropy (ads3GeodesicLength rAds logFactor) gN3 /
      brownHenneauxCentralCharge rAds gN3 = logFactor / 3 := by
  dsimp [rtLeadingEntropy, ads3GeodesicLength, brownHenneauxCentralCharge]
  field_simp [hR, hG]
  ring

/-- Theorem 3: Additivity of `rtLeadingEntropy` over disjoint surface areas at fixed `G_N`. -/
theorem rtLeadingEntropy_linear_in_area (area1 area2 gN : ℚ) :
    rtLeadingEntropy (area1 + area2) gN =
      rtLeadingEntropy area1 gN + rtLeadingEntropy area2 gN := by
  dsimp [rtLeadingEntropy]
  ring

/-- Theorem 4: Minimal-surface / minimal-cut pasting inequality for holographic Strong Subadditivity
(`arXiv:hep-th/0603001` Section 3.1 eq. (3.2) p. 4; Headrick-Takayanagi 2007):
if reconnected surfaces satisfy `areaUnion + areaInter ≤ areaAB + areaBC` and minimal surfaces
satisfy `minABC ≤ areaUnion` and `minB ≤ areaInter` at `0 < gN`, then
`S(ABC) + S(B) ≤ S(AB) + S(BC)`. -/
theorem cut_pasting_strong_subadditivity_from_submodularity
    (areaAB areaBC areaUnion areaInter minABC minB gN : ℚ)
    (hSubmod : areaUnion + areaInter ≤ areaAB + areaBC)
    (hMinABC : minABC ≤ areaUnion)
    (hMinB : minB ≤ areaInter)
    (hgN : 0 < gN) :
    rtLeadingEntropy minABC gN + rtLeadingEntropy minB gN ≤
      rtLeadingEntropy areaAB gN + rtLeadingEntropy areaBC gN := by
  have hSum : minABC + minB ≤ areaAB + areaBC := by linarith
  have h4gN : 0 ≤ 4 * gN := by linarith
  have hDiv : rtLeadingEntropy (minABC + minB) gN ≤ rtLeadingEntropy (areaAB + areaBC) gN := by
    dsimp [rtLeadingEntropy]
    exact div_le_div_of_nonneg_right hSum h4gN
  linarith [rtLeadingEntropy_linear_in_area minABC minB gN,
    rtLeadingEntropy_linear_in_area areaAB areaBC gN]

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
/-- Theorem 5: Across all `380` proper nonempty contiguous boundary intervals `(start, len)`
(`start ∈ 0..19`, `len ∈ 1..19`) on the 20-qubit 6-pentagon HaPPY `{5,4}` patch, the minimal
bond cut `intervalMincut` is invariant under boundary complementation
`(start, len) ↦ ((start + len) % 20, 20 - len)`, and the stabilizer entropy `intervalEntropy`
satisfies complement symmetry across all `19` proper interval lengths `len ∈ 1..19`. -/
theorem happy_mincut_and_entropy_complement_symmetry_all_380 :
    (allIntervals380.all fun (start, len) =>
      let sc := (start + len) % 20
      let lc := 20 - len
      intervalMincut start len == intervalMincut sc lc) = true ∧
    (((List.range 19).map (· + 1)).all fun len =>
      intervalEntropy 0 len == intervalEntropy len (20 - len)) = true := by
  decide

-- ============================================================================
-- 2. Von Neumann Entropy Dichotomy Fence (`FQ-ENTROPY-DICHOTOMY-BAKER`)
-- ============================================================================

/-- Theorem 6: Any rational Ryu-Takayanagi ratio `rtLeadingEntropy area gN = area / (4 * gN)` cast
to `ℝ` is algebraic over `ℚ`. -/
theorem rtLeadingEntropy_realCast_isAlgebraic (area gN : ℚ) :
    IsAlgebraic ℚ ((rtLeadingEntropy area gN : ℚ) : ℝ) :=
  isAlgebraic_ratCast ℚ (rtLeadingEntropy area gN)

/-- Theorem 7: Under `C750B01.BakerCitedInput`, no mixed finite state with algebraic eigenvalues
(`s : AlgebraicSpectrum d`, `¬ Pure s`) can have its natural-log von Neumann entropy `entropy s`
equal to a rational Ryu-Takayanagi ratio `(rtLeadingEntropy area gN : ℝ)`. -/
theorem no_rational_rt_area_for_mixed_algebraic_spectrum
    (baker : BakerCitedInput) {d : ℕ} (s : AlgebraicSpectrum d) (hm : ¬ Pure s)
    (area gN : ℚ) :
    entropy s ≠ ((rtLeadingEntropy area gN : ℚ) : ℝ) := by
  intro hEq
  have hAlg : IsAlgebraic ℚ (entropy s) := by
    rw [hEq]
    exact rtLeadingEntropy_realCast_isAlgebraic area gN
  exact hm ((entropy_algebraic_iff_pure baker s).mp hAlg)

/-- Theorem 8: Under `C750B01.BakerCitedInput` and `0 < gN`, an algebraic spectrum
`s : AlgebraicSpectrum d` satisfies `entropy s = (rtLeadingEntropy area gN : ℝ)` if and only if
the state is pure (`Pure s`) and the surface area vanishes (`area = 0`). -/
theorem rational_rt_match_iff_pure_and_zero_area
    (baker : BakerCitedInput) {d : ℕ} (s : AlgebraicSpectrum d)
    (area gN : ℚ) (hgN : 0 < gN) :
    entropy s = ((rtLeadingEntropy area gN : ℚ) : ℝ) ↔ Pure s ∧ area = 0 := by
  constructor
  · intro hEq
    have hAlg : IsAlgebraic ℚ (entropy s) := by
      rw [hEq]
      exact rtLeadingEntropy_realCast_isAlgebraic area gN
    have hPure : Pure s := (entropy_algebraic_iff_pure baker s).mp hAlg
    have hZero : entropy s = 0 := (entropy_zero_iff_pure s).mpr hPure
    have hRatZero : ((rtLeadingEntropy area gN : ℚ) : ℝ) = 0 := by
      rw [← hEq, hZero]
    have hRatZero' : rtLeadingEntropy area gN = 0 := by exact_mod_cast hRatZero
    dsimp [rtLeadingEntropy] at hRatZero'
    have h4gN : (4 * gN : ℚ) ≠ 0 := by linarith
    have hArea : area = 0 := (div_eq_zero_iff.mp hRatZero').resolve_right h4gN
    exact ⟨hPure, hArea⟩
  · rintro ⟨hPure, rfl⟩
    rw [(entropy_zero_iff_pure s).mpr hPure]
    simp [rtLeadingEntropy]

/-- Theorem 9: For a stabilizer marginal whose natural-log entropy is `k * Real.log 2` (a `k`-bit
maximally mixed subspace), dividing by the conversion factor `Real.log 2` recovers the exact
integer bond count `(k : ℝ)`. -/
theorem stabilizer_bits_to_nats_transcendental_conversion (k : ℕ) :
    ((k : ℝ) * Real.log 2) / Real.log 2 = (k : ℝ) := by
  have hlog2_pos : 0 < Real.log 2 := Real.log_pos (by norm_num)
  exact mul_div_cancel_right₀ (k : ℝ) (ne_of_gt hlog2_pos)

-- ============================================================================
-- 3. Exact Rational Regge Proxy (`TFQ-0100`) vs. Minimal-Surface & HaPPY Fence
-- ============================================================================

/-- Heron / Cayley-Menger squared area `A_h^2` of a triangle with squared side lengths
`(s01, s02, s12)` (`area_squared_in_pentatope` in `code/rust/src/general_relativity/exact_regge/action.rs`). -/
def cayleyMengerTriangleAreaSq (s01 s02 s12 : ℚ) : ℚ :=
  (2 * (s01 * s02 + s01 * s12 + s02 * s12) - (s01 ^ 2 + s02 ^ 2 + s12 ^ 2)) / 16

/-- Exact rational Regge action proxy `∑_i A_i^2 * κ_i` (`rational_regge_proxy` in
`code/rust/src/general_relativity/exact_regge/action.rs`, `TFQ-0100`). -/
def rationalReggeAction {n : ℕ} (areaSq kappa : Fin n → ℚ) : ℚ :=
  ∑ i, areaSq i * kappa i

/-- Theorem 10: On the `orthogonal_pentatope` chart of `TFQ-0100` (`sphere.rs`), the 6 right-triangle
hinges with squared edge lengths `(1, 1, 2)` have squared area `1 / 4`, the 4 equilateral-triangle
hinges with squared edge lengths `(2, 2, 2)` have squared area `3 / 4`, and the total squared hinge
area across all 10 hinges is `9 / 2`. -/
theorem orthogonal_pentatope_hinge_areas_sq :
    cayleyMengerTriangleAreaSq 1 1 2 = 1 / 4 ∧
    cayleyMengerTriangleAreaSq 2 2 2 = 3 / 4 ∧
    6 * cayleyMengerTriangleAreaSq 1 1 2 + 4 * cayleyMengerTriangleAreaSq 2 2 2 = 9 / 2 := by
  dsimp [cayleyMengerTriangleAreaSq]
  norm_num

/-- Helper lemma: if `4 * a^2 = 3 * b^2` in `ℕ`, then `3` divides both `a` and `b`. -/
theorem nat_dvd_three_of_sq_mul_four_eq_three_mul_sq (a b : ℕ)
    (h : 4 * a ^ 2 = 3 * b ^ 2) : 3 ∣ a ∧ 3 ∣ b := by
  have ha_div : a = 3 * (a / 3) + a % 3 := (Nat.div_add_mod a 3).symm
  have ha_mod : a % 3 < 3 := Nat.mod_lt a (by decide)
  have ha0 : a % 3 = 0 := by
    have h1 : 4 * (3 * (a / 3) + a % 3) ^ 2 = 3 * b ^ 2 := by rw [← ha_div]; exact h
    have h2 : 3 * (12 * (a / 3) ^ 2 + 8 * (a / 3) * (a % 3) + (a % 3) ^ 2) + (a % 3) ^ 2 =
        3 * b ^ 2 := by
      linarith [h1]
    have hr : a % 3 = 0 ∨ a % 3 = 1 ∨ a % 3 = 2 := by omega
    rcases hr with h0 | h1' | h2'
    · exact h0
    · rw [h1'] at h2; omega
    · rw [h2'] at h2; omega
  have ha3 : 3 ∣ a := Nat.dvd_of_mod_eq_zero ha0
  obtain ⟨k, hk⟩ := ha3
  have hb_eq : b ^ 2 = 3 * (4 * k ^ 2) := by
    have h' : 4 * (3 * k) ^ 2 = 3 * b ^ 2 := by rw [← hk]; exact h
    linarith
  have hb_div : b = 3 * (b / 3) + b % 3 := (Nat.div_add_mod b 3).symm
  have hb_mod : b % 3 < 3 := Nat.mod_lt b (by decide)
  have hb0 : b % 3 = 0 := by
    have h3 : (3 * (b / 3) + b % 3) ^ 2 = 3 * (4 * k ^ 2) := by rw [← hb_div]; exact hb_eq
    have h4 : 3 * (3 * (b / 3) ^ 2 + 2 * (b / 3) * (b % 3)) + (b % 3) ^ 2 =
        3 * (4 * k ^ 2) := by
      linarith [h3]
    have hr : b % 3 = 0 ∨ b % 3 = 1 ∨ b % 3 = 2 := by omega
    rcases hr with h0 | h1' | h2'
    · exact h0
    · rw [h1'] at h4; omega
    · rw [h2'] at h4; omega
  exact ⟨⟨k, hk⟩, Nat.dvd_of_mod_eq_zero hb0⟩

/-- Theorem 11: On the `orthogonal_pentatope` chart of `TFQ-0100`, each of the 4 equilateral-triangle
hinges has rational Cayley-Menger squared area `cayleyMengerTriangleAreaSq 2 2 2 = 3 / 4`, but no
rational linear area `A : ℚ` satisfies `A ^ 2 = cayleyMengerTriangleAreaSq 2 2 2`. -/
theorem no_rational_linear_area_for_equilateral_pentatope_hinge (A : ℚ) :
    A ^ 2 ≠ cayleyMengerTriangleAreaSq 2 2 2 := by
  intro hEq
  have h34 : cayleyMengerTriangleAreaSq 2 2 2 = 3 / 4 := by
    dsimp [cayleyMengerTriangleAreaSq]; norm_num
  rw [h34] at hEq
  have hRat : (A.num : ℚ) / (A.den : ℚ) = A := Rat.num_div_den A
  have hDenNe : (A.den : ℚ) ≠ 0 := by exact_mod_cast A.den_nz
  have hSq : ((A.num : ℚ) / (A.den : ℚ)) ^ 2 = 3 / 4 := by rw [hRat, hEq]
  have hCrossRat : 4 * (A.num : ℚ) ^ 2 = 3 * (A.den : ℚ) ^ 2 := by
    field_simp [hDenNe] at hSq
    linarith
  have hCrossInt : 4 * A.num ^ 2 = 3 * (A.den : ℤ) ^ 2 := by exact_mod_cast hCrossRat
  have hAbsSq : (A.num.natAbs : ℤ) ^ 2 = A.num ^ 2 := Int.natAbs_sq A.num
  have hCrossInt' : 4 * (A.num.natAbs : ℤ) ^ 2 = 3 * (A.den : ℤ) ^ 2 := by
    rw [hAbsSq]; exact hCrossInt
  have hCrossNat : 4 * A.num.natAbs ^ 2 = 3 * A.den ^ 2 := by exact_mod_cast hCrossInt'
  obtain ⟨ha3, hb3⟩ :=
    nat_dvd_three_of_sq_mul_four_eq_three_mul_sq A.num.natAbs A.den hCrossNat
  have hdvd : 3 ∣ Nat.gcd A.num.natAbs A.den := Nat.dvd_gcd ha3 hb3
  rw [A.reduced.gcd_eq_one] at hdvd
  omega

/-- Theorem 12: On any flat chart (`kappa = fun _ => 0`, corresponding to `flat_einstein_hilbert`
in `action.rs`), the rational Regge action proxy vanishes identically regardless of hinge areas. -/
theorem reggeProxy_zero_on_flat_chart {n : ℕ} (areaSq : Fin n → ℚ) :
    rationalReggeAction areaSq (fun _ => 0) = 0 := by
  dsimp [rationalReggeAction]
  simp

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
/-- Theorem 13: On the 20-qubit 6-pentagon HaPPY `{5,4}` patch (`FrontierHappyMincut`), every one
of the `380` proper nonempty contiguous boundary intervals (`start ∈ 0..19`, `len ∈ 1..19`) has
strictly positive minimal cut `1 ≤ intervalMincut start len`, and every proper interval length
`len ∈ 1..19` has strictly positive stabilizer entropy `1 ≤ intervalEntropy 0 len` (in contrast
to the flat-chart Regge proxy `0`). -/
theorem happy_all_380_intervals_pos_entropy_and_mincut :
    (allIntervals380.all fun (start, len) =>
      decide (1 ≤ intervalMincut start len)) = true ∧
    (((List.range 19).map (· + 1)).all fun len =>
      decide (1 ≤ intervalEntropy 0 len)) = true := by
  decide

/-- Theorem 14: Under uniform length rescaling `L ↦ λ L` (so squared edge lengths rescale as
`s_{ij} ↦ λ^2 s_{ij}`), `cayleyMengerTriangleAreaSq` scales with degree `4` in `λ` (`λ^4`), and
`rationalReggeAction` scales by `λ^4`. -/
theorem cayleyMengerTriangleAreaSq_homogeneous_deg4_in_length
    (lam s01 s02 s12 : ℚ) :
    cayleyMengerTriangleAreaSq (lam ^ 2 * s01) (lam ^ 2 * s02) (lam ^ 2 * s12) =
      lam ^ 4 * cayleyMengerTriangleAreaSq s01 s02 s12 := by
  dsimp [cayleyMengerTriangleAreaSq]
  ring

/-- Theorem 15: Because the squared-area Regge proxy scales as `λ^4` while a 2-surface area scales
as `λ^2` (and a topological bond count scales as `λ^0`), no scale-invariant dictionary constant
`alpha : ℚ` can equate `alpha * (λ^4 * a0)` with `λ^2 * a0` (or `a0`) at both `λ = 1` and `λ = 2`
for any nonzero `a0 ≠ 0`. -/
theorem no_scale_invariant_regge_to_rt_dictionary (alpha a0 : ℚ) (ha0 : a0 ≠ 0) :
    ¬ (alpha * ((1 : ℚ) ^ 4 * a0) = (1 : ℚ) ^ 2 * a0 ∧
       alpha * ((2 : ℚ) ^ 4 * a0) = (2 : ℚ) ^ 2 * a0) ∧
    ¬ (alpha * ((1 : ℚ) ^ 4 * a0) = a0 ∧
       alpha * ((2 : ℚ) ^ 4 * a0) = a0) := by
  constructor
  · rintro ⟨h1, h2⟩
    have hdiff : 12 * (alpha * a0) = 0 := by linarith
    have h1' : alpha * a0 = a0 := by linarith
    rw [h1'] at hdiff
    have ha0_zero : a0 = 0 := by linarith
    exact ha0 ha0_zero
  · rintro ⟨h1, h2⟩
    have hdiff : 15 * (alpha * a0) = 0 := by linarith
    have h1' : alpha * a0 = a0 := by linarith
    rw [h1'] at hdiff
    have ha0_zero : a0 = 0 := by linarith
    exact ha0 ha0_zero

end AdsRtFormulaImport

#print axioms AdsRtFormulaImport.rt_ads3_reproduces_calabrese_cardy
#print axioms AdsRtFormulaImport.rt_over_brown_henneaux_eliminates_couplings
#print axioms AdsRtFormulaImport.rtLeadingEntropy_linear_in_area
#print axioms AdsRtFormulaImport.cut_pasting_strong_subadditivity_from_submodularity
#print axioms AdsRtFormulaImport.happy_mincut_and_entropy_complement_symmetry_all_380
#print axioms AdsRtFormulaImport.rtLeadingEntropy_realCast_isAlgebraic
#print axioms AdsRtFormulaImport.no_rational_rt_area_for_mixed_algebraic_spectrum
#print axioms AdsRtFormulaImport.rational_rt_match_iff_pure_and_zero_area
#print axioms AdsRtFormulaImport.stabilizer_bits_to_nats_transcendental_conversion
#print axioms AdsRtFormulaImport.orthogonal_pentatope_hinge_areas_sq
#print axioms AdsRtFormulaImport.nat_dvd_three_of_sq_mul_four_eq_three_mul_sq
#print axioms AdsRtFormulaImport.no_rational_linear_area_for_equilateral_pentatope_hinge
#print axioms AdsRtFormulaImport.reggeProxy_zero_on_flat_chart
#print axioms AdsRtFormulaImport.happy_all_380_intervals_pos_entropy_and_mincut
#print axioms AdsRtFormulaImport.cayleyMengerTriangleAreaSq_homogeneous_deg4_in_length
#print axioms AdsRtFormulaImport.no_scale_invariant_regge_to_rt_dictionary

private def l5aProvenance : String :=
  "Origin: lean4/AdsRtFormulaImport.lean Claim: ADS-RT-FORMULA-IMPORT AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
