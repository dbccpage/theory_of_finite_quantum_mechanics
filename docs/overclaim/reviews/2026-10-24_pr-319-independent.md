# Independent review of PR #319

Scope: original head 4014caad9d8a9e113ec64db9ed8141120ab7f7ff. Exact source lean4/CampaignFspCobordismIntrinsicSign.lean, SHA-256 be8a115911db61211f437136c8db75dfcfa0262af23ff050a890ddc4f644dfc8.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

The integer spectral-sign function is odd; the declared 2x2 block has determinant m^2-s; two four-entry sign sums are 2 and -2. The exact supplied ZMod 2 formula is a3*arf+w1*sigmaDiv16, not n1+arf*c2+n2*w2. The Ward lemma concerns two nonnegative integer weights under the supplied equation w0+w1=-(w0+w1); it does not derive that equation from an anomaly or quantify over a configuration involution. P*H*P=2*D and equality of H/D traces/determinants do not assert trace preservation for P*H*P. Arithmetic in ZMod 16 computes no Pin bordism group. No manifold, AHSS, mapping-torus Dirac construction, anomaly classification, or bulk-boundary no-go theorem is formalized.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignFspCobordismIntrinsicSign.lean:24 spectralSign_odd_and_symmetric_pair_zero` | `(lam : ℤ) : spectralSign (-lam) = -spectralSign lam ∧ spectralSign lam + spectralSign (-lam) = 0` |
| `lean4/CampaignFspCobordismIntrinsicSign.lean:31 single_eigenvalue_crossing_eta_jump_by_two` | `(lam : ℤ) (hpos : 0 < lam) (k : ℕ) : spectralSign lam = 1 ∧ spectralSign (-lam) = -1 ∧ spectralSign lam - spectralSign (-lam) = 2 ∧ (-1 : ℤ) ^ (k + 1) = -((-1 : ℤ) ^ k)` |
| `lean4/CampaignFspCobordismIntrinsicSign.lean:51 mapping_torus_fermion_det_sign_reversal` | `(m s : ℤ) : Matrix.det (diracMappingBlock m s) = m ^ 2 - s ∧ Matrix.det (diracMappingBlock 0 (-1)) = 1 ∧ Matrix.det (diracMappingBlock 0 1) = -1 ∧ Matrix.det (diracMappingBlock 0 (-1)) + Matrix.det (diracMappingBlock 0 1) = 0` |
| `lean4/CampaignFspCobordismIntrinsicSign.lean:71 arf_gaussian_sign_sum_dichotomy` | `: arfGaussianSum arf0Form = 2 ∧ arfGaussianSum arf1Form = -2 ∧ arfGaussianSum arf0Form + arfGaussianSum arf1Form = 0` |
| `lean4/CampaignFspCobordismIntrinsicSign.lean:82 ahss_5d_spin_cobordism_pairing_sectors` | `(a3 arf w1 sigmaDiv16 : ZMod 2) : nu5Pairing a3 0 w1 0 = 0 ∧ nu5Pairing 0 arf 1 1 = 1 ∧ nu5Pairing 1 1 0 sigmaDiv16 = 1 ∧ (1 : ZMod 2) ≠ 0` |
| `lean4/CampaignFspCobordismIntrinsicSign.lean:93 anomaly_odd_ward_identity_rules_out_positive_weights_in_class` | `(w0 w1 : ℤ) (hw0 : 0 ≤ w0) (hw1 : 0 ≤ w1) : (w0 + w1 = -(w0 + w1) → w0 = 0 ∧ w1 = 0) ∧ (0 < w0 + w1 → w0 + w1 ≠ -(w0 + w1))` |
| `lean4/CampaignFspCobordismIntrinsicSign.lean:104 five_d_bulk_inflow_cancels_boundary_anomaly_sign` | `(nu5 : ZMod 2) : nu5 + (-nu5) = 0 ∧ ((-1 : ℤ) ^ nu5.val) * ((-1 : ℤ) ^ nu5.val) = 1` |
| `lean4/CampaignFspCobordismIntrinsicSign.lean:111 pin_minus_z16_order_sixteen_fence` | `: (1 : ZMod 16) ≠ 0 ∧ (2 : ZMod 16) * (1 : ZMod 16) ≠ 0 ∧ (8 : ZMod 16) * (1 : ZMod 16) ≠ 0 ∧ (16 : ZMod 16) * (1 : ZMod 16) = 0` |
| `lean4/CampaignFspCobordismIntrinsicSign.lean:134 basis_change_removes_sign_outside_constrained_class_fence` | `: offDiagSignedMat 0 1 = -1 ∧ Matrix.trace offDiagSignedMat = Matrix.trace diagNonnegMat ∧ Matrix.det offDiagSignedMat = Matrix.det diagNonnegMat ∧ hadamardBasisMat * offDiagSignedMat * hadamardBasisMat = (2 : ℤ) • diagNonnegMat` |
| `lean4/CampaignFspCobordismIntrinsicSign.lean:144 thermal_orientation_weight_asymmetry_fence` | `(w_pos w_neg : ℤ) : (w_pos = w_neg → w_pos - w_neg = 0) ∧ (w_pos ≠ w_neg → w_pos - w_neg ≠ 0)` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_319_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
