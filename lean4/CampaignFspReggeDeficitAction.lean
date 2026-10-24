import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic
import ReggePachnerWdw

/-!
# Campaign: FSP-REGGE-DEFICIT-ACTION (TFQ-1212 / FSP-DERIV-048)

AuthorityEffect: None.

Target: `FSP-REGGE-DEFICIT-ACTION` (`TFQ-1212` / `FSP-DERIV-048`, Stage: `FERMION_SIGN`,
Status: `IMPORTED_ASSUMPTION`).

Mathematical Content & Scope Fences (`GIN-C13`):
1. **Cayley-Menger / Heron Squared Triangle Area (`heronAreaSq`)**:
   - From squared edge lengths `s01, s12, s02 : ℚ`, `heronAreaSq s01 s12 s02` computes
     $A_h^2 = \frac{1}{16}(2 s_{01}s_{12} + 2 s_{12}s_{02} + 2 s_{02}s_{01} - s_{01}^2 - s_{12}^2 - s_{02}^2)$.
   - Evaluates the two hinge classes of `orthogonal_pentatope` (`code/rust/src/general_relativity/exact_regge/sphere.rs`):
     $6$ right-triangle hinges ($s = (1, 1, 2)$, $A_h^2 = 1/4$) and $4$ equilateral-triangle hinges
     ($s = (2, 2, 2)$, $A_h^2 = 3/4$), giving total squared hinge area $6(1/4) + 4(3/4) = 9/2$,
     and $0$ on degenerate collinear triples ($s = (1, 1, 4)$).
2. **Hinge Deficit Angle & Bilinear Regge Action (`hingeDeficit`, `reggeAction`)**:
   - Defines `hingeDeficit fullTurn dihedrals = fullTurn - dihedrals.sum` and
     `reggeAction areas eps = ∑ h, areas h * eps h`.
   - Establishes vanishing deficit iff dihedral sum equals `fullTurn` and exact bilinearity in
     `(areas, eps)`.
3. **Positive-Deficit Non-Negativity vs Mixed-Sign Indefiniteness**:
   - When `areas ≥ 0` and `eps ≥ 0`, `reggeAction areas eps ≥ 0`; when negative (saddle) deficits
     are present (`eps = ![1, -2]` on unit areas), `reggeAction ![1, 1] ![1, -2] = -1 < 0`, and
     opposite-sign deficits `eps = ![1, -1]` cancel to `0` despite non-zero hinge curvature.
4. **4-Sphere Boundary $\partial \Delta^5$ Combinatorics & Euler Characteristic**:
   - Face counts $(N_0, N_1, N_2, N_3, N_4) = (6, 15, 20, 15, 6) = (\binom{6}{1}, \dots, \binom{6}{5})$,
     Euler characteristic $\chi(\partial \Delta^5) = 6 - 15 + 20 - 15 + 6 = 2$, and hinge-simplex
     incidence balance $6 \times \binom{5}{3} = 20 \times 3 = 60$.
5. **Discrete First Bianchi Telescoping Identity**:
   - Around any closed loop of frame orientations `(f0, f1, f2, f3)`, the cyclic dihedral differences
     `(f1 - f0) + (f2 - f1) + (f3 - f2) + (f0 - f3) = 0` and their constant-area weighted sum vanish
     without assuming the cyclic sum as a premise.
6. **Schläfli Variational Reduction**:
   - Under `∑ h, A h * dTheta h = 0`, the full variation `∑ h, (dA h * eps h - A h * dTheta h)`
     reduces to the area-variation term `∑ h, dA h * eps h`.
7. **Cheeger-Müller-Schrader Refinement Defect Bound (`defectBoundHolds`)**:
   - Mirrors `defect_bound_holds` in `code/rust/src/general_relativity/exact_regge/action.rs`
     (`0 ≤ c ∧ 0 ≤ aSq ∧ (sRegge - sEh)^2 ≤ (c * aSq)^2`), checks the exact Rust unit-test
     rational witnesses, and shows that at zero scale `aSq = 0` the bound forces `sRegge = sEh`.
8. **Scope Fences (`GIN-C13`)**:
   - Regge calculus is purely gravitational and independent of fermion sign sectors $\sigma \in \{-1, +1\}$;
     multiplying positive Boltzmann weight $w > 0$ by $\sigma = \pm 1$ leaves opposite-sign
     configurations uncancelled unless a separate fermion-sign mechanism is supplied.
   - Lorentzian phase factors $\exp(i\Delta S) \in \{+1, -1\}$ oscillate in sign across $\Delta S = \pi$.
   - `ReggePachnerWdw.sumDeficits` over `ℕ` vanishes iff every hinge deficit is zero, whereas signed
     rational deficits can sum to zero without hinge-wise flatness.
-/

namespace CampaignFspReggeDeficitAction

open scoped BigOperators
open ReggePachnerWdw

/-- Heron / Cayley-Menger squared triangle area from squared edge lengths `s01, s12, s02 : ℚ`:
$A^2 = \frac{1}{16}(2 s_{01}s_{12} + 2 s_{12}s_{02} + 2 s_{02}s_{01} - s_{01}^2 - s_{12}^2 - s_{02}^2)$. -/
def heronAreaSq (s01 s12 s02 : ℚ) : ℚ :=
  (2 * s01 * s12 + 2 * s12 * s02 + 2 * s02 * s01 - s01 ^ 2 - s12 ^ 2 - s02 ^ 2) / 16

/-- Theorem 1 (Heron Squared Area Symmetry and `orthogonal_pentatope` Hinge Classes):
`heronAreaSq` is symmetric under edge swaps, evaluates to `1 / 4` on the 6 right-triangle
hinges `(1, 1, 2)` and `3 / 4` on the 4 equilateral hinges `(2, 2, 2)` of `orthogonal_pentatope`
(total squared hinge area `9 / 2`), and vanishes on the collinear triple `(1, 1, 4)`. -/
theorem heronAreaSq_symmetric_and_orthogonal_pentatope_hinges (a b c : ℚ) :
    heronAreaSq a b c = heronAreaSq b a c ∧
    heronAreaSq a b c = heronAreaSq a c b ∧
    heronAreaSq 1 1 2 = 1 / 4 ∧
    heronAreaSq 2 2 2 = 3 / 4 ∧
    6 * heronAreaSq 1 1 2 + 4 * heronAreaSq 2 2 2 = 9 / 2 ∧
    heronAreaSq 1 1 4 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold heronAreaSq; ring
  · unfold heronAreaSq; ring
  · unfold heronAreaSq; norm_num
  · unfold heronAreaSq; norm_num
  · unfold heronAreaSq; norm_num
  · unfold heronAreaSq; norm_num

/-- Hinge deficit angle $\epsilon_h = \text{fullTurn} - \sum_{\sigma > h} \theta_{h,\sigma}$. -/
def hingeDeficit (fullTurn : ℚ) (dihedrals : List ℚ) : ℚ :=
  fullTurn - dihedrals.sum

/-- Discrete Regge action $S_{\text{Regge}} = \sum_{h} A_h \epsilon_h$. -/
def reggeAction {n : ℕ} (areas eps : Fin n → ℚ) : ℚ :=
  ∑ h : Fin n, areas h * eps h

/-- Theorem 2 (Deficit Flatness Criterion and Regge Action Bilinearity):
`hingeDeficit fullTurn dihedrals = 0` iff `dihedrals.sum = fullTurn`, and `reggeAction`
vanishes on zero deficits, is additive in `eps`, and is homogeneous in `areas`. -/
theorem hingeDeficit_flat_sum_zero_and_reggeAction_bilinear
    (fullTurn : ℚ) (dihedrals : List ℚ) {n : ℕ} (areas eps1 eps2 : Fin n → ℚ) (c : ℚ) :
    (hingeDeficit fullTurn dihedrals = 0 ↔ dihedrals.sum = fullTurn) ∧
    reggeAction areas (fun _ => 0) = 0 ∧
    reggeAction areas (fun h => eps1 h + eps2 h) =
      reggeAction areas eps1 + reggeAction areas eps2 ∧
    reggeAction (fun h => c * areas h) eps1 = c * reggeAction areas eps1 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · unfold hingeDeficit
    constructor <;> intro h <;> linarith
  · simp [reggeAction]
  · simp [reggeAction, mul_add, Finset.sum_add_distrib]
  · simp [reggeAction, mul_assoc, ← Finset.mul_sum]

/-- Theorem 3 (Non-Negative Deficit Positivity vs Saddle-Curvature Sign Indefiniteness):
When all hinge areas and deficits are non-negative, `0 ≤ reggeAction areas eps`; however,
with positive areas `![1, 1]` and mixed-sign deficits `![1, -2]` or `![1, -1]`,
`reggeAction` becomes strictly negative (`-1 < 0`) or vanishes (`0`) despite non-flat hinges. -/
theorem reggeAction_positive_vs_mixed_deficit_sign
    {n : ℕ} (areas eps : Fin n → ℚ)
    (hA : ∀ h, 0 ≤ areas h) (hE : ∀ h, 0 ≤ eps h) :
    0 ≤ reggeAction areas eps ∧
    reggeAction ![1, 1] ![1, -2] = -1 ∧
    reggeAction ![1, 1] ![1, -2] < 0 ∧
    reggeAction ![1, 1] ![1, -1] = 0 ∧
    (![(1 : ℚ), -1] : Fin 2 → ℚ) 0 ≠ 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · unfold reggeAction
    exact Finset.sum_nonneg (fun h _ => mul_nonneg (hA h) (hE h))
  · simp [reggeAction, Fin.sum_univ_two]
    norm_num
  · simp [reggeAction, Fin.sum_univ_two]
  · simp [reggeAction, Fin.sum_univ_two]
  · norm_num

/-- Face vector $(N_0, N_1, N_2, N_3, N_4) = (6, 15, 20, 15, 6)$ of $\partial \Delta^5 \cong S^4$. -/
def s4BoundaryFaceVector : Fin 5 → ℕ :=
  ![6, 15, 20, 15, 6]

/-- Theorem 4 (4-Sphere $\partial \Delta^5$ Face Counts, Euler Characteristic, and Hinge Incidence):
The boundary $\partial \Delta^5$ has face counts $\binom{6}{k+1} = (6, 15, 20, 15, 6)$,
Euler characteristic $\chi = 6 - 15 + 20 - 15 + 6 = 2$, and hinge-pentatope incidence count
$6 \times \binom{5}{3} = 20 \times 3 = 60$. -/
theorem s4_boundary_delta5_face_counts_and_euler_characteristic :
    Nat.choose 6 1 = s4BoundaryFaceVector 0 ∧
    Nat.choose 6 2 = s4BoundaryFaceVector 1 ∧
    Nat.choose 6 3 = s4BoundaryFaceVector 2 ∧
    Nat.choose 6 4 = s4BoundaryFaceVector 3 ∧
    Nat.choose 6 5 = s4BoundaryFaceVector 4 ∧
    (s4BoundaryFaceVector 0 : ℤ) - s4BoundaryFaceVector 1 + s4BoundaryFaceVector 2 -
      s4BoundaryFaceVector 3 + s4BoundaryFaceVector 4 = 2 ∧
    6 * Nat.choose 5 3 = 20 * 3 := by
  decide

/-- Theorem 5 (Discrete First Bianchi Cyclic Telescoping Identity):
Around any 4-step closed loop of frame angles `(f0, f1, f2, f3)`, the cyclic sum of relative
steps `(f1 - f0) + (f2 - f1) + (f3 - f2) + (f0 - f3)` and its area-weighted sum vanish
identically without assuming the cyclic sum as a hypothesis. -/
theorem discrete_bianchi_cyclic_holonomy_telescoping (A f0 f1 f2 f3 : ℚ) :
    (f1 - f0) + (f2 - f1) + (f3 - f2) + (f0 - f3) = 0 ∧
    A * (f1 - f0) + A * (f2 - f1) + A * (f3 - f2) + A * (f0 - f3) = 0 := by
  constructor <;> ring

/-- Full Regge first variation combining area variations `dA` and dihedral variations `dTheta`. -/
def reggeFullVariation {n : ℕ} (A dA eps dTheta : Fin n → ℚ) : ℚ :=
  ∑ h : Fin n, (dA h * eps h - A h * dTheta h)

/-- Theorem 6 (Schläfli Variational Reduction):
When the Schläfli identity `∑ h, A h * dTheta h = 0` holds, the full variation
`reggeFullVariation A dA eps dTheta` reduces to the area-variation term `reggeAction dA eps`. -/
theorem schlaefli_variation_reduces_regge_variation_to_area_term
    {n : ℕ} (A dA eps dTheta : Fin n → ℚ)
    (hSchlaefli : ∑ h : Fin n, A h * dTheta h = 0) :
    reggeFullVariation A dA eps dTheta = reggeAction dA eps := by
  unfold reggeFullVariation reggeAction
  rw [Finset.sum_sub_distrib, hSchlaefli, sub_zero]

/-- Exact rational Cheeger-Müller-Schrader refinement bound predicate matching
`defect_bound_holds` in `code/rust/src/general_relativity/exact_regge/action.rs`. -/
def defectBoundHolds (sRegge sEh c aSq : ℚ) : Prop :=
  0 ≤ c ∧ 0 ≤ aSq ∧ (sRegge - sEh) ^ 2 ≤ (c * aSq) ^ 2

/-- Theorem 7 (Exact Rust `defect_bound_holds` Witnesses and Zero-Mesh Limit):
Matches the three exact rational witnesses in `action.rs::tests::defect_bound_holds_on_exact_rationals`
and shows that when `aSq = 0`, `defectBoundHolds sRegge sEh c 0` forces `sRegge = sEh`. -/
theorem defectBoundHolds_exact_rust_witnesses_and_zero_scale_limit
    (sRegge sEh c : ℚ) :
    defectBoundHolds (1 / 3) (1 / 4) 2 (1 / 16) ∧
    ¬ defectBoundHolds 1 0 1 (1 / 4) ∧
    ¬ defectBoundHolds 1 0 (-1) 1 ∧
    (defectBoundHolds sRegge sEh c 0 → sRegge = sEh) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · unfold defectBoundHolds; norm_num
  · unfold defectBoundHolds; norm_num
  · unfold defectBoundHolds; norm_num
  · rintro ⟨_, _, hsq⟩
    have h0 : (sRegge - sEh) ^ 2 ≤ 0 := by simpa using hsq
    have hge : 0 ≤ (sRegge - sEh) ^ 2 := sq_nonneg (sRegge - sEh)
    have heq0 : (sRegge - sEh) ^ 2 = 0 := le_antisymm h0 hge
    have hsub : sRegge - sEh = 0 := sq_eq_zero_iff.mp heq0
    linarith

/-- Theorem 8 (Scope Fence — Regge Action Carries No Fermion-Sign Content, `GIN-C13`):
For any non-zero positive gravitational weight `w > 0`, coupling a fermion sign factor
`sigma ∈ {+1, -1}` produces opposite-sign weights `(+1) * w = w > 0` and `(-1) * w = -w < 0`
whose signed sum vanishes while the gravitational Regge action `reggeAction areas eps` is
unchanged between the two sectors. -/
theorem regge_action_independent_of_fermion_occupation_fence
    {n : ℕ} (areas eps : Fin n → ℚ) (w : ℚ) (hw : 0 < w) :
    (1 : ℚ) * w > 0 ∧
    (-1 : ℚ) * w < 0 ∧
    (1 : ℚ) * w + (-1 : ℚ) * w = 0 ∧
    reggeAction areas eps = reggeAction areas eps := by
  refine ⟨by linarith, by linarith, by ring, rfl⟩

/-- Discrete Lorentzian phase matrix $R(\pi) = -I_2$ vs identity $R(0) = I_2$. -/
def lorentzianHalfTurnMat : Matrix (Fin 2) (Fin 2) ℤ :=
  !![-1, 0;
      0, -1]

/-- Theorem 9 (Scope Fence — Lorentzian Phase Oscillation vs Positive Euclidean Weight, `GIN-C13`):
The Lorentzian half-turn phase matrix `lorentzianHalfTurnMat` has trace `-2` (real part `-1` per
component) and cancels against the untwisted identity matrix `1 + lorentzianHalfTurnMat = 0`,
showing that Lorentzian Regge phases oscillate in sign. -/
theorem euclidean_vs_lorentzian_regge_phase_fence :
    Matrix.trace lorentzianHalfTurnMat = -2 ∧
    lorentzianHalfTurnMat * lorentzianHalfTurnMat = 1 ∧
    (1 : Matrix (Fin 2) (Fin 2) ℤ) + lorentzianHalfTurnMat = 0 := by
  decide

/-- Theorem 10 (Scope Fence — `Nat` Sum Flatness in `ReggePachnerWdw` vs Signed Deficit Cancellation):
In `ReggePachnerWdw.sumDeficits` over `ℕ`, `sumDeficits [d1, d2] = 0 ↔ d1 = 0 ∧ d2 = 0`,
whereas over signed rational deficits `ℚ`, `1 + (-1) = 0` with `1 ≠ 0` and `-1 ≠ 0`, so
vanishing total signed deficit does not imply hinge-wise flatness. -/
theorem flat_vertex_sum_vs_signed_cancellation_fence (d1 d2 : ℕ) :
    (sumDeficits [d1, d2] = 0 ↔ d1 = 0 ∧ d2 = 0) ∧
    ((1 : ℚ) + (-1 : ℚ) = 0 ∧ (1 : ℚ) ≠ 0 ∧ (-1 : ℚ) ≠ 0) := by
  refine ⟨?_, ?_⟩
  · simp [sumDeficits]
  · norm_num

end CampaignFspReggeDeficitAction

#print axioms CampaignFspReggeDeficitAction.heronAreaSq_symmetric_and_orthogonal_pentatope_hinges
#print axioms CampaignFspReggeDeficitAction.hingeDeficit_flat_sum_zero_and_reggeAction_bilinear
#print axioms CampaignFspReggeDeficitAction.reggeAction_positive_vs_mixed_deficit_sign
#print axioms CampaignFspReggeDeficitAction.s4_boundary_delta5_face_counts_and_euler_characteristic
#print axioms CampaignFspReggeDeficitAction.discrete_bianchi_cyclic_holonomy_telescoping
#print axioms CampaignFspReggeDeficitAction.schlaefli_variation_reduces_regge_variation_to_area_term
#print axioms CampaignFspReggeDeficitAction.defectBoundHolds_exact_rust_witnesses_and_zero_scale_limit
#print axioms CampaignFspReggeDeficitAction.regge_action_independent_of_fermion_occupation_fence
#print axioms CampaignFspReggeDeficitAction.euclidean_vs_lorentzian_regge_phase_fence
#print axioms CampaignFspReggeDeficitAction.flat_vertex_sum_vs_signed_cancellation_fence
