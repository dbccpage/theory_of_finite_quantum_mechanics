import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.LinearAlgebra.Matrix.Rank
import FrontierEntanglingPhase

/-!
# Local operations and Schmidt rank (CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT)

AuthorityEffect: None.
Outcome: Narrowed (campaign class). The node stays IMPORTED_ASSUMPTION.

What this module proves, and nothing more:

1. For every field `K`, every finite index types and every pair of matrices `A`, `B`, the
   coefficient matrix `A * M * Bᵀ` of the pure bipartite state `(A ⊗ B) ψ` has rank at most the
   rank of `M` (`schmidtRank_local_le`). The Schmidt rank of a pure state is the rank of its
   coefficient matrix. This is arbitrary finite dimension, but only for ONE linear local map
   `A ⊗ B` applied to ONE pure state.
2. In the two-qubit case over the Gaussian rationals `Q(i)` (`FrontierEntanglingPhase.Mat2`):
   `det2 (A M Bᵀ) = det2 A * det2 M * det2 B`, so a zero-determinant (product) state stays
   zero-determinant, and the state `ψ_u = (1,1,1,u)/2` with `u = (3+4i)/5`, whose squared
   concurrence is exactly `1/5`, is not of the form `A ⊗ B` applied to `ψ_1`.

What it does NOT prove: anything about mixed states, completely positive maps with ancillas,
convex combinations of branches, classical communication between the parties, a mediating
system `M`, the information-theoretic definition of a classical medium used by Marletto and
Vedral, or gravity. `ClassicalMediatorBranch` is by definition a pair of local operators
`(A, B)` on `Q1`, `Q2`; calling it a "classical mediator branch" is a label, not a derived
fact. `LoccMediatorModel` carries the preservation of the zero determinant as a field, so
`reduction_of_mediated_entanglement_inference` restates its hypothesis.
-/

namespace CampaignCtMediatorEntanglement

open FrontierEntanglingPhase
open FrontierEntanglingPhase.GaussRat

/-- A local pure operation acting on `Q1` and `Q2` via matrix transformation `M ↦ A M B^T`. -/
def applyLocalOp (A B M : Mat2) : Mat2 :=
  mul2 A (mul2 M (transpose2 B))

/-- A pair of local operators `(A, B)` on `Q1` and `Q2`. The name "classical mediator branch" is a label: no mediating system and no classical communication is modelled. -/
structure ClassicalMediatorBranch where
  opA : Mat2
  opB : Mat2
  deriving DecidableEq, Repr

/-- Action of a classical mediator branch on the bipartite state matrix `M`. -/
def applyMediatorBranch (branch : ClassicalMediatorBranch) (M : Mat2) : Mat2 :=
  applyLocalOp branch.opA branch.opB M

/-- Schmidt rank of a pure bipartite state is the rank of its coefficient matrix. A single
linear local map `A ⊗ B` acts as `M ↦ A * M * Bᵀ` and cannot raise it, in any finite dimension
over any field. -/
theorem schmidtRank_local_le {K : Type*} [Field K] {m n p q : Type*}
    [Fintype m] [Fintype n] [Fintype p] [Fintype q]
    (A : Matrix m p K) (M : Matrix p q K) (B : Matrix n q K) :
    (A * M * B.transpose).rank ≤ M.rank :=
  (Matrix.rank_mul_le_left (A * M) B.transpose).trans (Matrix.rank_mul_le_right A M)

/-- Consequently a state of Schmidt rank at most one stays of Schmidt rank at most one. -/
theorem schmidtRank_le_one_preserved {K : Type*} [Field K] {m n p q : Type*}
    [Fintype m] [Fintype n] [Fintype p] [Fintype q]
    (A : Matrix m p K) (M : Matrix p q K) (B : Matrix n q K) (h : M.rank ≤ 1) :
    (A * M * B.transpose).rank ≤ 1 :=
  (schmidtRank_local_le A M B).trans h

/-- A target of strictly larger Schmidt rank is not the image of `M` under any single local map. -/
theorem schmidtRank_not_reachable {K : Type*} [Field K] {m n p q : Type*}
    [Fintype m] [Fintype n] [Fintype p] [Fintype q]
    (A : Matrix m p K) (M : Matrix p q K) (B : Matrix n q K) (T : Matrix m n K)
    (h : M.rank < T.rank) : A * M * B.transpose ≠ T := by
  intro heq
  have := schmidtRank_local_le A M B
  rw [heq] at this
  omega

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

/-- No pair of local operators (a "branch" in the sense of `ClassicalMediatorBranch`) maps `M_separable` to `M_entangled`. -/
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

/-- A map on two-qubit coefficient matrices ASSUMED to preserve the zero determinant (a hypothesis packaged as a structure; not a definition of LOCC). -/
structure LoccMediatorModel where
  action : Mat2 → Mat2
  preserves_zero_det : ∀ M : Mat2, det2 M = 0 → det2 (action M) = 0

/-- Restatement of the hypothesis `preserves_zero_det`: a map assumed to preserve the zero
determinant does not send a zero-determinant state to a nonzero-determinant state. This is
logic, not physics: it does not show that any classical mediator satisfies the hypothesis. -/
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
#print axioms CampaignCtMediatorEntanglement.schmidtRank_local_le
#print axioms CampaignCtMediatorEntanglement.schmidtRank_le_one_preserved
#print axioms CampaignCtMediatorEntanglement.schmidtRank_not_reachable
