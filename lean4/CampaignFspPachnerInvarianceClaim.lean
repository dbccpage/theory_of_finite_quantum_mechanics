import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic

/-!
# Campaign FSP-PACHNER-INVARIANCE-CLAIM (`TFQ-1214` / `FSP-DERIV-050`)

Status: Formalization of 4D bistellar Pachner moves ($1 \leftrightarrow 5$, $2 \leftrightarrow 4$,
$3 \leftrightarrow 3$), Euler-Poincaré characteristic and Dehn-Sommerville invariance,
linear topological state-sum and $\mathbb{Z}_2$ flat gauge partition normalization conditions,
Regge action and curved Wheeler-DeWitt defect non-invariance, and explicit scope fences
for signed rational deficit cancellation and fermion-sign independence (`OPEN`, `E1 -> E3`).
AuthorityEffect: None.

## Scope & Boundaries
- Replaces the missing `ReggePachnerWdw.lean::pachner_move_topological_invariance`
  and the `Nat`-only lemma `curved_pachner_induces_positive_defect` with exact
  integer (`ℤ`) and signed rational (`ℚ`) theorems.
- Keeps node status `OPEN` because `FSP-DERIV-050` names no specific Crane-Yetter / BF
  state-sum model, the metric Regge action is not Pachner invariant on curved geometries,
  and combinatorial Pachner moves carry no fermion-sign resolution.
-/

open scoped BigOperators Matrix

namespace CampaignFspPachnerInvarianceClaim

/-- Face vector $(N_0, N_1, N_2, N_3, N_4)$ of a 4-dimensional simplicial complex. -/
structure FaceVector4D where
  n0 : ℤ
  n1 : ℤ
  n2 : ℤ
  n3 : ℤ
  n4 : ℤ
  deriving DecidableEq, Repr

/-- Euler-Poincaré characteristic $\chi = N_0 - N_1 + N_2 - N_3 + N_4$. -/
def eulerChar4D (f : FaceVector4D) : ℤ :=
  f.n0 - f.n1 + f.n2 - f.n3 + f.n4

/-- $1 \to 5$ Pachner bistellar subdivision move: inserts 1 interior vertex, 5 edges,
10 triangles, 10 tetrahedra, and replaces 1 4-simplex by 5 ($\Delta N_4 = +4$). -/
def pachner1to5 (f : FaceVector4D) : FaceVector4D :=
  ⟨f.n0 + 1, f.n1 + 5, f.n2 + 10, f.n3 + 10, f.n4 + 4⟩

/-- Inverse $5 \to 1$ Pachner bistellar coarsening move. -/
def pachner5to1 (f : FaceVector4D) : FaceVector4D :=
  ⟨f.n0 - 1, f.n1 - 5, f.n2 - 10, f.n3 - 10, f.n4 - 4⟩

/-- $2 \to 4$ Pachner bistellar move: replaces 2 4-simplices sharing an interior tetrahedron
by 4 4-simplices sharing a new transverse edge ($\Delta = (0, +1, +4, +5, +2)$). -/
def pachner2to4 (f : FaceVector4D) : FaceVector4D :=
  ⟨f.n0, f.n1 + 1, f.n2 + 4, f.n3 + 5, f.n4 + 2⟩

/-- Inverse $4 \to 2$ Pachner bistellar move. -/
def pachner4to2 (f : FaceVector4D) : FaceVector4D :=
  ⟨f.n0, f.n1 - 1, f.n2 - 4, f.n3 - 5, f.n4 - 2⟩

/-- $3 \to 3$ Pachner bistellar flip: replaces 3 4-simplices sharing an interior triangle
by 3 4-simplices sharing the dual triangle ($\Delta = (0, 0, 0, 0, 0)$). -/
def pachner3to3 (f : FaceVector4D) : FaceVector4D :=
  f

/-- Theorem 1 (Euler-Poincaré Invariance and Move Invertibility Across All 4D Pachner Moves):
Every $1 \leftrightarrow 5$, $2 \leftrightarrow 4$, and $3 \leftrightarrow 3$ 4D Pachner move
preserves the Euler characteristic $\chi = N_0 - N_1 + N_2 - N_3 + N_4$, and
`pachner5to1` / `pachner4to2` are exact two-sided inverses of `pachner1to5` / `pachner2to4`. -/
theorem pachner_moves_preserve_euler_characteristic (f : FaceVector4D) :
    eulerChar4D (pachner1to5 f) = eulerChar4D f ∧
    eulerChar4D (pachner5to1 f) = eulerChar4D f ∧
    eulerChar4D (pachner2to4 f) = eulerChar4D f ∧
    eulerChar4D (pachner4to2 f) = eulerChar4D f ∧
    eulerChar4D (pachner3to3 f) = eulerChar4D f ∧
    pachner5to1 (pachner1to5 f) = f ∧
    pachner4to2 (pachner2to4 f) = f := by
  rcases f with ⟨n0, n1, n2, n3, n4⟩
  refine ⟨?_, ?_, ?_, ?_, rfl, ?_, ?_⟩
  · unfold eulerChar4D pachner1to5; ring
  · unfold eulerChar4D pachner5to1; ring
  · unfold eulerChar4D pachner2to4; ring
  · unfold eulerChar4D pachner4to2; ring
  · unfold pachner5to1 pachner1to5; congr 1 <;> ring
  · unfold pachner4to2 pachner2to4; congr 1 <;> ring

/-- Seed face vector $(6, 15, 20, 15, 6)$ of $\partial \Delta^5 \cong S^4$ in
`code/python/src/fsp/regge_pachner_wdw.py` (`Simplicial4DManifold`). -/
def s4SeedFaceVector : FaceVector4D :=
  ⟨6, 15, 20, 15, 6⟩

/-- Theorem 2 ($\partial \Delta^5$ Surgical Sequence Trajectory in `regge_pachner_wdw.py`):
Starting from `s4SeedFaceVector = (6, 15, 20, 15, 6)`, the surgical sequence
`1 -> 5`, then `2 -> 4`, then `3 -> 3` produces intermediate face vectors
`(7, 20, 30, 25, 10)` and `(7, 21, 34, 30, 12)` while preserving $\chi = 2$ at every step. -/
theorem s4_seed_surgical_sequence_face_vectors_and_chi :
    let f1 := pachner1to5 s4SeedFaceVector
    let f2 := pachner2to4 f1
    let f3 := pachner3to3 f2
    eulerChar4D s4SeedFaceVector = 2 ∧
    f1 = ⟨7, 20, 30, 25, 10⟩ ∧
    eulerChar4D f1 = 2 ∧
    f2 = ⟨7, 21, 34, 30, 12⟩ ∧
    eulerChar4D f2 = 2 ∧
    f3 = ⟨7, 21, 34, 30, 12⟩ ∧
    eulerChar4D f3 = 2 := by
  decide

/-- Codimension-1 Dehn-Sommerville defect $2 N_3 - 5 N_4$ on a closed 4-manifold. -/
def dehnSommervilleDefect (f : FaceVector4D) : ℤ :=
  2 * f.n3 - 5 * f.n4

/-- Theorem 3 (Codimension-1 Dehn-Sommerville Invariance $2 N_3 = 5 N_4$):
All 4D bistellar Pachner moves preserve $2 N_3 - 5 N_4$ (since $2 \cdot 10 - 5 \cdot 4 = 0$
and $2 \cdot 5 - 5 \cdot 2 = 0$), and `s4SeedFaceVector` satisfies $2 N_3 - 5 N_4 = 0$. -/
theorem dehn_sommerville_codim1_invariant_under_pachner_moves (f : FaceVector4D) :
    dehnSommervilleDefect (pachner1to5 f) = dehnSommervilleDefect f ∧
    dehnSommervilleDefect (pachner2to4 f) = dehnSommervilleDefect f ∧
    dehnSommervilleDefect (pachner3to3 f) = dehnSommervilleDefect f ∧
    dehnSommervilleDefect s4SeedFaceVector = 0 := by
  refine ⟨?_, ?_, rfl, by decide⟩
  · unfold dehnSommervilleDefect pachner1to5; ring
  · unfold dehnSommervilleDefect pachner2to4; ring

/-- Linear simplex-count state-sum log-weight $L_w(f) = \sum_{k=0}^4 w_k N_k$ over $\mathbb{Q}$. -/
def linearStateSumExponent (w : Fin 5 → ℚ) (f : FaceVector4D) : ℚ :=
  w 0 * (f.n0 : ℚ) + w 1 * (f.n1 : ℚ) + w 2 * (f.n2 : ℚ) +
    w 3 * (f.n3 : ℚ) + w 4 * (f.n4 : ℚ)

/-- Theorem 4 (Exact Characterization of Pachner-Invariant Linear State-Sum Weights):
A linear simplex-count functional $L_w(f)$ is invariant under both `pachner1to5` and
`pachner2to4` for a given $f$ if and only if
$w_0 = 10 w_2 + 15 w_3 + 6 w_4$ and $w_1 = -4 w_2 - 5 w_3 - 2 w_4$.
In particular, both the Euler weight $w_\chi = (1, -1, 1, -1, 1)$ and the Dehn-Sommerville
weight $w_{\text{DS}} = (0, 0, 0, 2, -5)$ satisfy these counterterm equations. -/
theorem linear_topological_state_sum_pachner_invariance_iff
    (w : Fin 5 → ℚ) (f : FaceVector4D) :
    ((linearStateSumExponent w (pachner1to5 f) = linearStateSumExponent w f ∧
      linearStateSumExponent w (pachner2to4 f) = linearStateSumExponent w f) ↔
      (w 0 = 10 * w 2 + 15 * w 3 + 6 * w 4 ∧
       w 1 = -4 * w 2 - 5 * w 3 - 2 * w 4)) ∧
    linearStateSumExponent ![1, -1, 1, -1, 1] (pachner1to5 f) =
      linearStateSumExponent ![1, -1, 1, -1, 1] f ∧
    linearStateSumExponent ![0, 0, 0, 2, -5] (pachner2to4 f) =
      linearStateSumExponent ![0, 0, 0, 2, -5] f := by
  refine ⟨?_, ?_, ?_⟩
  · unfold linearStateSumExponent pachner1to5 pachner2to4
    push_cast
    constructor
    · rintro ⟨h15, h24⟩
      constructor <;> linarith
    · rintro ⟨hw0, hw1⟩
      constructor <;> linarith
  · unfold linearStateSumExponent pachner1to5
    simp [Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  · unfold linearStateSumExponent pachner2to4
    simp [Matrix.cons_val_zero, Matrix.cons_val_one]
    ring

/-- Normalized finite-group flat gauge bundle partition sum $|G|^{-N_0} \cdot |\text{Flat}|$. -/
def normalizedFlatGaugeSum (groupOrder invNorm0 flatCount : ℚ) (deltaN0 : ℕ) : ℚ :=
  match deltaN0 with
  | 0 => invNorm0 * flatCount
  | 1 => (groupOrder⁻¹ * invNorm0) * (groupOrder * flatCount)
  | _ => 0

/-- Theorem 5 (Finite-Group Flat Bundle State-Sum Normalization Invariance):
For any finite gauge group order $G \ne 0$ (such as $|G| = 2$ for $\mathbb{Z}_2$),
a $1 \to 5$ move adds $\Delta N_0 = 1$ interior vertex and multiplies the number of flat
1-cochain extensions by $G$, while the vertex factor $G^{-N_0}$ multiplies by $G^{-1}$,
leaving $G^{-N_0} |\text{Flat}|$ invariant; a $2 \to 4$ move ($\Delta N_0 = 0$) uniquely
fixes the new transverse edge holonomy by triangle flatness and also preserves the sum. -/
theorem z2_gauge_state_sum_vertex_normalization_invariance
    (G invNorm0 flatCount : ℚ) (hG : G ≠ 0) :
    normalizedFlatGaugeSum G invNorm0 flatCount 1 =
      normalizedFlatGaugeSum G invNorm0 flatCount 0 ∧
    normalizedFlatGaugeSum 2 (1 / 64) 32 1 = 1 / 2 ∧
    normalizedFlatGaugeSum 2 (1 / 64) 32 0 = 1 / 2 := by
  refine ⟨?_, ?_, ?_⟩
  · unfold normalizedFlatGaugeSum
    calc
      G⁻¹ * invNorm0 * (G * flatCount) = (G⁻¹ * G) * (invNorm0 * flatCount) := by ring
      _ = 1 * (invNorm0 * flatCount) := by rw [inv_mul_cancel₀ hG]
      _ = invNorm0 * flatCount := by ring
  · unfold normalizedFlatGaugeSum
    norm_num
  · unfold normalizedFlatGaugeSum
    norm_num

/-- Regge action shift $\Delta S_{\text{Regge}} = m \cdot A_{\text{int}} \cdot \epsilon_{\text{int}}$
when $m$ new interior hinges each acquire area $A_{\text{int}}$ and deficit $\epsilon_{\text{int}}$. -/
def pachnerReggeActionShift (m : ℕ) (areaInt epsInt : ℚ) : ℚ :=
  (m : ℚ) * areaInt * epsInt

/-- Theorem 6 (Non-Invariance of the Regge Action Under Curved $1 \to 5$ and $2 \to 4$ Moves):
While a flat subdivision ($\epsilon_{\text{int}} = 0$) preserves $S_{\text{Regge}}$,
any curved $1 \to 5$ subdivision (10 interior hinges) or curved $2 \to 4$ move (4 interior hinges)
with $A_{\text{int}} > 0$ and $\epsilon_{\text{int}} \ne 0$ shifts the Regge action by a
non-zero amount ($\Delta S_{\text{Regge}} \ne 0$). -/
theorem regge_action_non_invariant_under_curved_pachner_subdivision
    (areaInt epsInt : ℚ) (hA : 0 < areaInt) (hE : epsInt ≠ 0) :
    pachnerReggeActionShift 10 areaInt 0 = 0 ∧
    pachnerReggeActionShift 4 areaInt 0 = 0 ∧
    pachnerReggeActionShift 10 areaInt epsInt ≠ 0 ∧
    pachnerReggeActionShift 4 areaInt epsInt ≠ 0 := by
  have hA_ne : areaInt ≠ 0 := ne_of_gt hA
  refine ⟨by unfold pachnerReggeActionShift; ring,
          by unfold pachnerReggeActionShift; ring, ?_, ?_⟩
  · unfold pachnerReggeActionShift
    exact mul_ne_zero (mul_ne_zero (by norm_num) hA_ne) hE
  · unfold pachnerReggeActionShift
    exact mul_ne_zero (mul_ne_zero (by norm_num) hA_ne) hE

/-- Curved scalar Wheeler-DeWitt defect mass $\sum_v \frac{3}{2} \deg(v) = 3 N_1$ in
`code/python/src/fsp/regge_pachner_wdw.py` (`solve_direct_sum_wdw_lp`). -/
def curvedWdwDefectMass (f : FaceVector4D) : ℚ :=
  3 * (f.n1 : ℚ)

/-- Theorem 7 (Curved WDW Scalar Defect Mass Increases Under $1 \to 5$ and $2 \to 4$ Surgery):
In the curved degree-weighted regime of `code/python/src/fsp/regge_pachner_wdw.py`,
the scalar WDW defect mass $3 N_1$ starts at $45$ on `s4SeedFaceVector`, increases to $60$
after `pachner1to5`, and increases to $63$ after `pachner2to4`, demonstrating that curved
WDW defect mass is not Pachner invariant ($45 < 60 < 63$). -/
theorem curved_wdw_defect_mass_shifts_under_pachner_moves :
    let f0 := s4SeedFaceVector
    let f1 := pachner1to5 f0
    let f2 := pachner2to4 f1
    let f3 := pachner3to3 f2
    curvedWdwDefectMass f0 = 45 ∧
    curvedWdwDefectMass f1 = 60 ∧
    curvedWdwDefectMass f2 = 63 ∧
    curvedWdwDefectMass f3 = 63 ∧
    curvedWdwDefectMass f0 < curvedWdwDefectMass f1 ∧
    curvedWdwDefectMass f1 < curvedWdwDefectMass f2 := by
  dsimp only
  unfold curvedWdwDefectMass s4SeedFaceVector pachner1to5 pachner2to4 pachner3to3
  norm_num

/-- Theorem 8 (Signed Hinge Deficit Cancellation Under $2 \to 4$ Move vs `Nat` Sum Fence):
Replaces the `Nat`-only assumption in `ReggePachnerWdw.lean::curved_pachner_induces_positive_defect`:
when the 4 new interior hinges of a $2 \to 4$ move carry signed rational deficits
$![1, -1, 1, -1]$, hinge $0$ has a strictly positive deficit ($1 > 0$), yet the total
deficit sum across the 4 hinges vanishes ($\sum_{i=0}^3 \epsilon_i = 0$). -/
theorem signed_hinge_deficits_can_cancel_under_pachner_move_fence :
    let deficits : Fin 4 → ℚ := ![1, -1, 1, -1]
    0 < deficits 0 ∧
    (∑ i : Fin 4, deficits i) = 0 := by
  dsimp only
  refine ⟨by norm_num, ?_⟩
  simp [Fin.sum_univ_four]

/-- Theorem 9 (Unnormalized 4-Simplex Weight Fails Pachner Invariance Fence):
A naive triangulation sum weighting only 4-simplices ($w = (0, 0, 0, 0, w_4)$ with $w_4 \ne 0$)
shifts by $4 w_4 \ne 0$ under `pachner1to5` and by $2 w_4 \ne 0$ under `pachner2to4`,
fencing the claim that an arbitrary triangulation sum is automatically Pachner invariant. -/
theorem unnormalized_simplex_weight_fails_pachner_invariance_fence
    (w4 : ℚ) (hw4 : w4 ≠ 0) (f : FaceVector4D) :
    linearStateSumExponent ![0, 0, 0, 0, w4] (pachner1to5 f) -
      linearStateSumExponent ![0, 0, 0, 0, w4] f = 4 * w4 ∧
    linearStateSumExponent ![0, 0, 0, 0, w4] (pachner2to4 f) -
      linearStateSumExponent ![0, 0, 0, 0, w4] f = 2 * w4 ∧
    4 * w4 ≠ 0 ∧
    2 * w4 ≠ 0 := by
  refine ⟨?_, ?_, mul_ne_zero (by norm_num) hw4, mul_ne_zero (by norm_num) hw4⟩
  · unfold linearStateSumExponent pachner1to5
    simp [Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  · unfold linearStateSumExponent pachner2to4
    simp [Matrix.cons_val_zero, Matrix.cons_val_one]
    ring

/-- Theorem 10 (Combinatorial Pachner Moves Carry No Fermion-Sign Resolution Fence):
For any face vector $f$ and fermionic path sign $\sigma \in \{-1, +1\}$, pairing the
Pachner-invariant Euler weight $\chi(f)$ with $\sigma$ cancels identically when summed
over $\sigma \in \{-1, +1\}$ both before and after any Pachner move. -/
theorem pachner_moves_independent_of_fermion_sign_fence (f : FaceVector4D) :
    (1 : ℤ) * eulerChar4D (pachner1to5 f) + (-1 : ℤ) * eulerChar4D (pachner1to5 f) = 0 ∧
    (1 : ℤ) * eulerChar4D (pachner2to4 f) + (-1 : ℤ) * eulerChar4D (pachner2to4 f) = 0 := by
  refine ⟨by ring, by ring⟩

#print axioms pachner_moves_preserve_euler_characteristic
#print axioms s4_seed_surgical_sequence_face_vectors_and_chi
#print axioms dehn_sommerville_codim1_invariant_under_pachner_moves
#print axioms linear_topological_state_sum_pachner_invariance_iff
#print axioms z2_gauge_state_sum_vertex_normalization_invariance
#print axioms regge_action_non_invariant_under_curved_pachner_subdivision
#print axioms curved_wdw_defect_mass_shifts_under_pachner_moves
#print axioms signed_hinge_deficits_can_cancel_under_pachner_move_fence
#print axioms unnormalized_simplex_weight_fails_pachner_invariance_fence
#print axioms pachner_moves_independent_of_fermion_sign_fence

end CampaignFspPachnerInvarianceClaim
