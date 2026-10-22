import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import FrontierEntanglingPhase

/-!
# Local Mediator Entanglement Reduction (CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT)

AuthorityEffect: None.
Outcome: Reduced.

This module formalizes the mathematical core of the mediated entanglement inference
audited against Marletto-Vedral (2017, arXiv:1707.06036, pp. 2-3) and Bose et al.
(2017, arXiv:1707.06050, pp. 1-2):
If two quantum systems Q1 and Q2 start in a separable state and interact only locally
with a mediating system M (with no direct Q1-Q2 interaction), producing an entangled
state of Q1 + Q2, then M cannot be a classical medium.

Mathematical Reduction:
In finite dimension over the Gaussian rationals `Q(i)`:
1. Every pure product state has 2x2 Schmidt determinant `det2 M = 0` and squared concurrence `C^2 = 0`.
2. Any local operation `A ⊗ B` on Q1 and Q2 transforms the amplitude matrix as `M ↦ A M B^T`,
   satisfying `det2(A M B^T) = det2(A) * det2(M) * det2(B)`.
3. Consequently, local operations (and any channel mediated by a classical medium, i.e., LOCC)
   cannot raise a separable state (`det2 M = 0`) to an entangled state (`det2 M ≠ 0`, `C^2 > 0`).
4. For the Pythagorean phase gate `u = (3 + 4i)/5`, the target state `ψ_u = (1, 1, 1, u)/2`
   has exact concurrence `C^2 = 1/5 > 0` and `det2 ≠ 0`.
5. Therefore, no local operation pair `(A, B)` can map the initial separable state `ψ_1` to `ψ_u`.
   Any physical medium generating this entanglement without direct Q1-Q2 coupling cannot be modeled
   by local operations / classical communication.
6. The physical interpretation of gravity as such a mediator is isolated as an external hypothesis
   (no gravity model is derived here; TFQ-0084 is a finite shadow only).
-/

namespace CampaignCtMediatorEntanglement

open FrontierEntanglingPhase
open FrontierEntanglingPhase.GaussRat

/-- A local pure operation acting on `Q1` and `Q2` via matrix transformation `M ↦ A M B^T`. -/
def applyLocalOp (A B M : Mat2) : Mat2 :=
  mul2 A (mul2 M (transpose2 B))

/-- A classical mediator branch acts locally on `Q1` and `Q2` via a pair of local operators `(A, B)`. -/
structure ClassicalMediatorBranch where
  opA : Mat2
  opB : Mat2
  deriving DecidableEq, Repr

/-- Action of a classical mediator branch on the bipartite state matrix `M`. -/
def applyMediatorBranch (branch : ClassicalMediatorBranch) (M : Mat2) : Mat2 :=
  applyLocalOp branch.opA branch.opB M

/-- The determinant multiplicativity identity for local operations over `Q(i)`. -/
theorem applyLocalOp_det (A B M : Mat2) :
    det2 (applyLocalOp A B M) = det2 A * det2 M * det2 B :=
  det2_local_action A M B

/-- Local operations strictly preserve the zero-determinant condition (Schmidt rank ≤ 1). -/
theorem local_op_preserves_product_det (A B M : Mat2) (h : det2 M = 0) :
    det2 (applyLocalOp A B M) = 0 :=
  local_op_cannot_raise_product_rank A M B h

/-- Any local operation acting on a separable state produces zero concurrence. -/
theorem local_op_concurrence_zero_of_separable (A B M : Mat2) (h : det2 M = 0) :
    concurrenceSq (applyLocalOp A B M) = 0 := by
  dsimp [concurrenceSq]
  rw [local_op_preserves_product_det A B M h]
  dsimp [normSq]
  ring

/-- The canonical initial separable state `ψ_1 = (1, 1, 1, 1)/2`. -/
def M_separable : Mat2 := M_u 1

/-- The canonical target entangled state `ψ_u` with Pythagorean unit phase `u = (3 + 4i)/5`. -/
def M_entangled : Mat2 := M_u u_pythagorean

/-- Initial state has zero concurrence. -/
theorem M_separable_concurrence_zero :
    concurrenceSq M_separable = 0 := by
  dsimp [M_separable]
  rw [concurrenceSq_M_u]
  dsimp [normSq]
  ring

/-- Initial state has zero determinant. -/
theorem M_separable_det_zero :
    det2 M_separable = 0 := by
  dsimp [M_separable]
  rw [det_M_u]
  ext <;> dsimp [scale] <;> ring

/-- Initial state is a product state. -/
theorem M_separable_is_product :
    IsProductState2 M_separable := by
  dsimp [M_separable]
  rw [psi_u_isProduct_iff]

/-- The entangled state has exact squared concurrence `1/5`. -/
theorem M_entangled_concurrence :
    concurrenceSq M_entangled = 1 / 5 :=
  u_pythagorean_unit_and_concurrence.2

/-- The entangled state determinant is strictly nonzero. -/
theorem M_entangled_det_nonzero :
    det2 M_entangled ≠ 0 := by
  intro hdet
  have hcon : concurrenceSq M_entangled = 0 := by
    dsimp [concurrenceSq]
    rw [hdet]
    dsimp [normSq]
    ring
  have h15 : concurrenceSq M_entangled = 1 / 5 := M_entangled_concurrence
  rw [h15] at hcon
  norm_num at hcon

/-- The target state is not a product state. -/
theorem M_entangled_not_product :
    ¬ IsProductState2 M_entangled := by
  intro hprod
  have hdet := productState2_det_zero M_entangled hprod
  exact M_entangled_det_nonzero hdet

/-- No pair of local operations can transform the separable state into the entangled state. -/
theorem no_local_op_produces_entangled_state (A B : Mat2) :
    applyLocalOp A B M_separable ≠ M_entangled := by
  intro heq
  have hdet_lhs : det2 (applyLocalOp A B M_separable) = 0 :=
    local_op_preserves_product_det A B M_separable M_separable_det_zero
  have hdet_rhs : det2 M_entangled ≠ 0 := M_entangled_det_nonzero
  rw [heq] at hdet_lhs
  exact hdet_rhs hdet_lhs

/-- No classical mediator branch can produce the target entangled state from the separable state. -/
theorem classical_mediator_cannot_produce_entangled_state (branch : ClassicalMediatorBranch) :
    applyMediatorBranch branch M_separable ≠ M_entangled :=
  no_local_op_produces_entangled_state branch.opA branch.opB

/-- The exact concurrence defect under any local operation is `1/5`. -/
theorem concurrence_gap_under_local_op (A B : Mat2) :
    concurrenceSq M_entangled - concurrenceSq (applyLocalOp A B M_separable) = 1 / 5 := by
  rw [M_entangled_concurrence, local_op_concurrence_zero_of_separable A B M_separable M_separable_det_zero]
  ring

/-- Universal phase obstruction: for every phase `u ≠ 1`, no local operation can map `ψ_1` to `ψ_u`. -/
theorem no_local_op_produces_phase_entangled_state (u : GaussRat) (hu : u ≠ 1) (A B : Mat2) :
    applyLocalOp A B M_separable ≠ M_u u := by
  intro heq
  have hdet_lhs : det2 (applyLocalOp A B M_separable) = 0 :=
    local_op_preserves_product_det A B M_separable M_separable_det_zero
  have hdet_rhs : det2 (M_u u) ≠ 0 := by
    rw [det_M_u]
    intro hzero
    apply hu
    have hre := congrArg GaussRat.re hzero
    have him := congrArg GaussRat.im hzero
    dsimp [scale] at hre him
    ext
    · simp; linarith
    · simp; linarith
  rw [heq] at hdet_lhs
  exact hdet_rhs hdet_lhs

/-- A mediator model that respects local operations and classical communication (LOCC). -/
structure LoccMediatorModel where
  action : Mat2 → Mat2
  preserves_zero_det : ∀ M : Mat2, det2 M = 0 → det2 (action M) = 0

/-- Formal reduction: The mediated entanglement inference reduces to Schmidt determinant
preservation under local channels. Any channel generating non-zero determinant from a product
state violates the LOCC condition. -/
theorem reduction_of_mediated_entanglement_inference
    (model : LoccMediatorModel)
    (M_in M_out : Mat2)
    (hin : det2 M_in = 0)
    (hout : det2 M_out ≠ 0) :
    model.action M_in ≠ M_out := by
  intro heq
  have h0 : det2 (model.action M_in) = 0 := model.preserves_zero_det M_in hin
  rw [heq] at h0
  exact hout h0

end CampaignCtMediatorEntanglement

#print axioms CampaignCtMediatorEntanglement.applyLocalOp_det
#print axioms CampaignCtMediatorEntanglement.local_op_preserves_product_det
#print axioms CampaignCtMediatorEntanglement.local_op_concurrence_zero_of_separable
#print axioms CampaignCtMediatorEntanglement.M_separable_concurrence_zero
#print axioms CampaignCtMediatorEntanglement.M_separable_det_zero
#print axioms CampaignCtMediatorEntanglement.M_separable_is_product
#print axioms CampaignCtMediatorEntanglement.M_entangled_concurrence
#print axioms CampaignCtMediatorEntanglement.M_entangled_det_nonzero
#print axioms CampaignCtMediatorEntanglement.M_entangled_not_product
#print axioms CampaignCtMediatorEntanglement.no_local_op_produces_entangled_state
#print axioms CampaignCtMediatorEntanglement.classical_mediator_cannot_produce_entangled_state
#print axioms CampaignCtMediatorEntanglement.concurrence_gap_under_local_op
#print axioms CampaignCtMediatorEntanglement.no_local_op_produces_phase_entangled_state
#print axioms CampaignCtMediatorEntanglement.reduction_of_mediated_entanglement_inference
