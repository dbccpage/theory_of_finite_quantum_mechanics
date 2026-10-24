/-
Exact algebraic model; AuthorityEffect: None.
The integer spectral-sign function is odd; the declared 2x2 block has determinant m^2-s; two four-entry sign sums are 2 and -2. The exact supplied ZMod 2 formula is a3*arf+w1*sigmaDiv16, not n1+arf*c2+n2*w2. The Ward lemma concerns two nonnegative integer weights under the supplied equation w0+w1=-(w0+w1); it does not derive that equation from an anomaly or quantify over a configuration involution. P*H*P=2*D and equality of H/D traces/determinants do not assert trace preservation for P*H*P. Arithmetic in ZMod 16 computes no Pin bordism group. No manifold, AHSS, mapping-torus Dirac construction, anomaly classification, or bulk-boundary no-go theorem is formalized.
Historical names are labels; their physical or operational interpretations require separate evidence.
-/

import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic



namespace CampaignFspCobordismIntrinsicSign

open Matrix


def spectralSign (lam : ℤ) : ℤ :=
  if 0 < lam then 1 else if lam < 0 then -1 else 0


theorem spectralSign_odd_and_symmetric_pair_zero (lam : ℤ) :
    spectralSign (-lam) = -spectralSign lam ∧
    spectralSign lam + spectralSign (-lam) = 0 := by
  unfold spectralSign
  split_ifs <;> omega


theorem single_eigenvalue_crossing_eta_jump_by_two (lam : ℤ) (hpos : 0 < lam) (k : ℕ) :
    spectralSign lam = 1 ∧
    spectralSign (-lam) = -1 ∧
    spectralSign lam - spectralSign (-lam) = 2 ∧
    (-1 : ℤ) ^ (k + 1) = -((-1 : ℤ) ^ k) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [spectralSign, if_pos hpos]
  · unfold spectralSign
    split_ifs <;> omega
  · unfold spectralSign
    split_ifs <;> omega
  · rw [pow_succ]
    ring


def diracMappingBlock (m s : ℤ) : Matrix (Fin 2) (Fin 2) ℤ :=
  !![m, s;
     1, m]


theorem mapping_torus_fermion_det_sign_reversal (m s : ℤ) :
    Matrix.det (diracMappingBlock m s) = m ^ 2 - s ∧
    Matrix.det (diracMappingBlock 0 (-1)) = 1 ∧
    Matrix.det (diracMappingBlock 0 1) = -1 ∧
    Matrix.det (diracMappingBlock 0 (-1)) + Matrix.det (diracMappingBlock 0 1) = 0 := by
  refine ⟨?_, by decide, by decide, by decide⟩
  simp [diracMappingBlock, Matrix.det_fin_two]
  ring


def arf0Form (x y : Fin 2) : ℕ := x.val * y.val


def arf1Form (x y : Fin 2) : ℕ := x.val * y.val + x.val + y.val


def arfGaussianSum (q : Fin 2 → Fin 2 → ℕ) : ℤ :=
  ((-1 : ℤ) ^ q 0 0) + ((-1 : ℤ) ^ q 0 1) + ((-1 : ℤ) ^ q 1 0) + ((-1 : ℤ) ^ q 1 1)


theorem arf_gaussian_sign_sum_dichotomy :
    arfGaussianSum arf0Form = 2 ∧
    arfGaussianSum arf1Form = -2 ∧
    arfGaussianSum arf0Form + arfGaussianSum arf1Form = 0 := by
  decide


def nu5Pairing (a3 arf w1 sigmaDiv16 : ZMod 2) : ZMod 2 :=
  a3 * arf + w1 * sigmaDiv16


theorem ahss_5d_spin_cobordism_pairing_sectors (a3 arf w1 sigmaDiv16 : ZMod 2) :
    nu5Pairing a3 0 w1 0 = 0 ∧
    nu5Pairing 0 arf 1 1 = 1 ∧
    nu5Pairing 1 1 0 sigmaDiv16 = 1 ∧
    (1 : ZMod 2) ≠ 0 := by
  refine ⟨?_, ?_, ?_, by decide⟩
  · simp [nu5Pairing]
  · simp [nu5Pairing]
  · simp [nu5Pairing]


theorem anomaly_odd_ward_identity_rules_out_positive_weights_in_class
    (w0 w1 : ℤ) (hw0 : 0 ≤ w0) (hw1 : 0 ≤ w1) :
    (w0 + w1 = -(w0 + w1) → w0 = 0 ∧ w1 = 0) ∧
    (0 < w0 + w1 → w0 + w1 ≠ -(w0 + w1)) := by
  refine ⟨?_, ?_⟩
  · intro hward
    omega
  · intro hpos hward
    omega


theorem five_d_bulk_inflow_cancels_boundary_anomaly_sign (nu5 : ZMod 2) :
    nu5 + (-nu5) = 0 ∧
    ((-1 : ℤ) ^ nu5.val) * ((-1 : ℤ) ^ nu5.val) = 1 := by
  refine ⟨add_neg_cancel nu5, ?_⟩
  fin_cases nu5 <;> decide


theorem pin_minus_z16_order_sixteen_fence :
    (1 : ZMod 16) ≠ 0 ∧
    (2 : ZMod 16) * (1 : ZMod 16) ≠ 0 ∧
    (8 : ZMod 16) * (1 : ZMod 16) ≠ 0 ∧
    (16 : ZMod 16) * (1 : ZMod 16) = 0 := by
  decide


def offDiagSignedMat : Matrix (Fin 2) (Fin 2) ℤ :=
  !![1, -1;
     -1, 1]


def diagNonnegMat : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, 0;
     0, 2]


def hadamardBasisMat : Matrix (Fin 2) (Fin 2) ℤ :=
  !![1, 1;
     1, -1]


theorem basis_change_removes_sign_outside_constrained_class_fence :
    offDiagSignedMat 0 1 = -1 ∧
    Matrix.trace offDiagSignedMat = Matrix.trace diagNonnegMat ∧
    Matrix.det offDiagSignedMat = Matrix.det diagNonnegMat ∧
    hadamardBasisMat * offDiagSignedMat * hadamardBasisMat =
      (2 : ℤ) • diagNonnegMat := by
  refine ⟨rfl, by decide, by decide, ?_⟩
  ext i j; fin_cases i <;> fin_cases j <;> decide


theorem thermal_orientation_weight_asymmetry_fence (w_pos w_neg : ℤ) :
    (w_pos = w_neg → w_pos - w_neg = 0) ∧
    (w_pos ≠ w_neg → w_pos - w_neg ≠ 0) := by
  refine ⟨by omega, by omega⟩

end CampaignFspCobordismIntrinsicSign

#print axioms CampaignFspCobordismIntrinsicSign.spectralSign_odd_and_symmetric_pair_zero
#print axioms CampaignFspCobordismIntrinsicSign.single_eigenvalue_crossing_eta_jump_by_two
#print axioms CampaignFspCobordismIntrinsicSign.mapping_torus_fermion_det_sign_reversal
#print axioms CampaignFspCobordismIntrinsicSign.arf_gaussian_sign_sum_dichotomy
#print axioms CampaignFspCobordismIntrinsicSign.ahss_5d_spin_cobordism_pairing_sectors
#print axioms CampaignFspCobordismIntrinsicSign.anomaly_odd_ward_identity_rules_out_positive_weights_in_class
#print axioms CampaignFspCobordismIntrinsicSign.five_d_bulk_inflow_cancels_boundary_anomaly_sign
#print axioms CampaignFspCobordismIntrinsicSign.pin_minus_z16_order_sixteen_fence
#print axioms CampaignFspCobordismIntrinsicSign.basis_change_removes_sign_outside_constrained_class_fence
#print axioms CampaignFspCobordismIntrinsicSign.thermal_orientation_weight_asymmetry_fence
