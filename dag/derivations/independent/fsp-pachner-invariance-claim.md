Status: AI-drafted, awaiting human review.
AuthorityEffect: None.

# Independent Derivation Note: `FSP-PACHNER-INVARIANCE-CLAIM` (`TFQ-1214` / `FSP-DERIV-050`)

- **Node ID**: `FSP-PACHNER-INVARIANCE-CLAIM` (`TFQ-1214`)
- **Source Record**: `FSP-DERIV-050` (`papers/core/fsp/theory_of_finite_fsp.md:694-706`)
- **Stage**: `FERMION_SIGN`
- **Status**: `OPEN` (`E1 -> E3`, `L4D`)
- **Lean 4 Module**: `lean4/CampaignFspPachnerInvarianceClaim.lean`
- **Independent Checker**: `checks/independent/fsp-pachner-invariance-claim.py`

---

## 1. Narrowed Mathematical Scope

`FSP-DERIV-050` claims that a discrete topological partition function on 4D triangulations is invariant under the $1 \leftrightarrow 5$, $2 \leftrightarrow 4$, and $3 \leftrightarrow 3$ bistellar Pachner moves. However, the source names no specific state-sum model (such as a Crane-Yetter or finite-group Dijkgraaf-Witten model), the metric Regge action is not Pachner invariant on curved geometries, and combinatorial Pachner moves carry no fermion-sign resolution.

In `lean4/CampaignFspPachnerInvarianceClaim.lean` and `checks/independent/fsp-pachner-invariance-claim.py`, we replace the missing `ReggePachnerWdw.lean::pachner_move_topological_invariance` and the `Nat`-only lemma `curved_pachner_induces_positive_defect` with 10 kernel-checked theorems while keeping the node status `OPEN`:
1. Euler-Poincaré characteristic $\chi = N_0 - N_1 + N_2 - N_3 + N_4$ invariance and move invertibility across $1 \leftrightarrow 5$, $2 \leftrightarrow 4$, and $3 \leftrightarrow 3$ 4D Pachner moves (`pachner_moves_preserve_euler_characteristic`).
2. Exact face-vector surgical trajectory $(6, 15, 20, 15, 6) \to (7, 20, 30, 25, 10) \to (7, 21, 34, 30, 12) \to (7, 21, 34, 30, 12)$ on $\partial \Delta^5 \cong S^4$ matching `Simplicial4DManifold` in `code/python/src/fsp/regge_pachner_wdw.py` (`s4_seed_surgical_sequence_face_vectors_and_chi`).
3. Codimension-1 Dehn-Sommerville relation $2 N_3 - 5 N_4 = 0$ invariance under all 4D Pachner moves (`dehn_sommerville_codim1_invariant_under_pachner_moves`).
4. Necessary and sufficient linear counterterm equations $w_0 = 10 w_2 + 15 w_3 + 6 w_4$ and $w_1 = -4 w_2 - 5 w_3 - 2 w_4$ for a simplex-count state-sum exponent $\sum_{k=0}^4 w_k N_k$ to be invariant under $1 \to 5$ and $2 \to 4$ moves (`linear_topological_state_sum_pachner_invariance_iff`).
5. Finite-group flat gauge bundle vertex normalization invariance $G^{-N_0} |\text{Flat}|$ under $1 \to 5$ ($\Delta N_0 = 1$, multiplying flat extensions by $G$) and $2 \to 4$ ($\Delta N_0 = 0$) moves (`z2_gauge_state_sum_vertex_normalization_invariance`).
6. Non-invariance of the metric Regge action under curved $1 \to 5$ and $2 \to 4$ subdivisions (`regge_action_non_invariant_under_curved_pachner_subdivision`) and strict growth ($45 < 60 < 63$) of the curved WDW scalar defect mass $3 N_1$ in `regge_pachner_wdw.py` (`curved_wdw_defect_mass_shifts_under_pachner_moves`).
7. Scope fences for signed rational hinge deficit cancellation (`signed_hinge_deficits_can_cancel_under_pachner_move_fence`), unnormalized 4-simplex weight non-invariance (`unnormalized_simplex_weight_fails_pachner_invariance_fence`), and fermion-sign independence (`pachner_moves_independent_of_fermion_sign_fence`).

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - Exact face-vector, Euler characteristic $\chi = 2$, and Dehn-Sommerville $2 N_3 = 5 N_4$ invariance across 4D bistellar Pachner moves, exact counterterm equations for linear simplex-count state sums, vertex normalization invariance $G^{-N_0} |\text{Flat}|$ for finite-group flat gauge bundles, and explicit proofs that curved Regge actions and curved WDW defect masses are not Pachner invariant.
2. **What it does not support**:
   - Does not construct a full 4D Crane-Yetter ribbon 2-category state sum, establish Pachner invariance of the curved Regge action, or resolve any fermionic path-integral sign problem.
3. **Narrowest defensible claim**:
   - Combinatorial 4D Pachner moves preserve $\chi$ and $2 N_3 - 5 N_4$, and preserve simplex-factorized state sums iff the vertex/edge counterterms satisfy $w_0 = 10 w_2 + 15 w_3 + 6 w_4$ and $w_1 = -4 w_2 - 5 w_3 - 2 w_4$, whereas curved Regge actions and the degree-weighted WDW defect mass $3 N_1$ shift under $1 \to 5$ and $2 \to 4$ moves.
4. **Next test needed**:
   - Formalize the causal foliation and transfer-matrix positivity conditions on `FSP-CDT-FOLIATION-POSITIVITY` (`TFQ-1215` / `FSP-DERIV-051`) and keep numerical de Sitter phase claims fenced as external literature.
