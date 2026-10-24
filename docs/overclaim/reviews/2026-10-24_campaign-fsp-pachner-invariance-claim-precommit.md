# Pre-Commit Claim Hygiene & Overclaim Review: `FSP-PACHNER-INVARIANCE-CLAIM` (`TFQ-1214`)

- **Date**: 2026-10-24
- **Branch**: `campaign/fsp-pachner-invariance-claim`
- **Target Node**: `FSP-PACHNER-INVARIANCE-CLAIM` (`TFQ-1214` / `FSP-DERIV-050`)
- **Stage**: `FERMION_SIGN`
- **Status**: `OPEN` (`E1 -> E3`, `L4D`)
- **AuthorityEffect**: `None`

## 1. What It Supports
- `lean4/CampaignFspPachnerInvarianceClaim.lean` (10 exported theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed) formalizes:
  - Euler-Poincaré characteristic $\chi = N_0 - N_1 + N_2 - N_3 + N_4$ invariance and move invertibility across $1 \leftrightarrow 5$, $2 \leftrightarrow 4$, and $3 \leftrightarrow 3$ 4D Pachner moves (`pachner_moves_preserve_euler_characteristic`).
  - Exact surgical face-vector trajectory $(6, 15, 20, 15, 6) \to (7, 20, 30, 25, 10) \to (7, 21, 34, 30, 12) \to (7, 21, 34, 30, 12)$ on $\partial \Delta^5 \cong S^4$ (`s4_seed_surgical_sequence_face_vectors_and_chi`) and codimension-1 Dehn-Sommerville invariance $2 N_3 - 5 N_4 = 0$ (`dehn_sommerville_codim1_invariant_under_pachner_moves`).
  - Exact counterterm equations $w_0 = 10 w_2 + 15 w_3 + 6 w_4$ and $w_1 = -4 w_2 - 5 w_3 - 2 w_4$ for linear state-sum invariance (`linear_topological_state_sum_pachner_invariance_iff`) and finite-group flat bundle vertex normalization invariance $G^{-N_0} |\text{Flat}|$ (`z2_gauge_state_sum_vertex_normalization_invariance`).
  - Non-invariance of the curved Regge action (`regge_action_non_invariant_under_curved_pachner_subdivision`) and strict growth ($45 < 60 < 63$) of the curved WDW scalar defect mass $3 N_1$ (`curved_wdw_defect_mass_shifts_under_pachner_moves`).
  - Scope fences for signed rational deficit cancellation (`signed_hinge_deficits_can_cancel_under_pachner_move_fence`), unnormalized 4-simplex weight non-invariance (`unnormalized_simplex_weight_fails_pachner_invariance_fence`), and fermion-sign independence (`pachner_moves_independent_of_fermion_sign_fence`).
- `checks/independent/fsp-pachner-invariance-claim.py` independently verifies all combinatorial and rational identities with zero failures.

## 2. What It Does Not Support
- Does not construct a 4D Crane-Yetter ribbon 2-category state sum, claim Pachner invariance of the curved Regge action, or claim any fermion-sign resolution from bistellar Pachner surgery.

## 3. Narrowest Defensible Claim
- Combinatorial 4D Pachner moves preserve $\chi$ and $2 N_3 - 5 N_4$, and preserve simplex-factorized state sums iff $w_0 = 10 w_2 + 15 w_3 + 6 w_4$ and $w_1 = -4 w_2 - 5 w_3 - 2 w_4$, whereas curved Regge actions and the degree-weighted WDW defect mass $3 N_1$ shift under $1 \to 5$ and $2 \to 4$ moves.

## 4. Next Test Needed
- Formalize the causal foliation and transfer-matrix positivity conditions on `FSP-CDT-FOLIATION-POSITIVITY` (`TFQ-1215` / `FSP-DERIV-051`) and keep numerical de Sitter phase claims fenced as external literature.
