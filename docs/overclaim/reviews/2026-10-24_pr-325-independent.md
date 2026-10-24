# Independent review of PR #325

Scope: original head 7a4887f244bbdcfec55e2ae5d1726ffb4d394a18. Exact source lean4/CampaignFspPachnerInvarianceClaim.lean, SHA-256 3675c610049324080f9f9ed57539909efe180f959cebc77fff1c49f6ce6efec1.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Five-integer face-vector translations preserve the displayed linear functionals; solving two rational linear equations characterizes invariant count weights. In Lean no simplicial complex, move admissibility, topology, or flat-connection extension count is constructed. The independent checker performs additional finite simplex-set examples, not a general refinement proof. normalizedFlatGaugeSum declares inverse-G cancellation for delta 0 and 1 and returns zero otherwise; it proves no gauge-bundle counting theorem. The Regge shift and WDW mass are supplied scalar formulas, not geometric action differences or constraint solutions. The stated face-count trajectories and arithmetic remain exact.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignFspPachnerInvarianceClaim.lean:52 pachner_moves_preserve_euler_characteristic` | `(f : FaceVector4D) : eulerChar4D (pachner1to5 f) = eulerChar4D f ∧ eulerChar4D (pachner5to1 f) = eulerChar4D f ∧ eulerChar4D (pachner2to4 f) = eulerChar4D f ∧ eulerChar4D (pachner4to2 f) = eulerChar4D f ∧ eulerChar4D (pachner3to3 f) = eulerChar4D f ∧ pachner5to1 (pachner1to5 f) = f ∧ pachner4to2 (pachner2to4 f) = f` |
| `lean4/CampaignFspPachnerInvarianceClaim.lean:74 s4_seed_surgical_sequence_face_vectors_and_chi` | `: let f1 := pachner1to5 s4SeedFaceVector let f2 := pachner2to4 f1 let f3 := pachner3to3 f2 eulerChar4D s4SeedFaceVector = 2 ∧ f1 = ⟨7, 20, 30, 25, 10⟩ ∧ eulerChar4D f1 = 2 ∧ f2 = ⟨7, 21, 34, 30, 12⟩ ∧ eulerChar4D f2 = 2 ∧ f3 = ⟨7, 21, 34, 30, 12⟩ ∧ eulerChar4D f3 = 2` |
| `lean4/CampaignFspPachnerInvarianceClaim.lean:92 dehn_sommerville_codim1_invariant_under_pachner_moves` | `(f : FaceVector4D) : dehnSommervilleDefect (pachner1to5 f) = dehnSommervilleDefect f ∧ dehnSommervilleDefect (pachner2to4 f) = dehnSommervilleDefect f ∧ dehnSommervilleDefect (pachner3to3 f) = dehnSommervilleDefect f ∧ dehnSommervilleDefect s4SeedFaceVector = 0` |
| `lean4/CampaignFspPachnerInvarianceClaim.lean:107 linear_topological_state_sum_pachner_invariance_iff` | `(w : Fin 5 → ℚ) (f : FaceVector4D) : ((linearStateSumExponent w (pachner1to5 f) = linearStateSumExponent w f ∧ linearStateSumExponent w (pachner2to4 f) = linearStateSumExponent w f) ↔ (w 0 = 10 * w 2 + 15 * w 3 + 6 * w 4 ∧ w 1 = -4 * w 2 - 5 * w 3 - 2 * w 4)) ∧ linearStateSumExponent ![1, -1, 1, -1, 1] (pachner1to5 f) = linearStateSumExponent ![1, -1, 1, -1, 1] f ∧ linearStateSumExponent ![0, 0, 0, 2, -5] (pachner2to4 f) = linearStateSumExponent ![0, 0, 0, 2, -5] f` |
| `lean4/CampaignFspPachnerInvarianceClaim.lean:140 z2_gauge_state_sum_vertex_normalization_invariance` | `(G invNorm0 flatCount : ℚ) (hG : G ≠ 0) : normalizedFlatGaugeSum G invNorm0 flatCount 1 = normalizedFlatGaugeSum G invNorm0 flatCount 0 ∧ normalizedFlatGaugeSum 2 (1 / 64) 32 1 = 1 / 2 ∧ normalizedFlatGaugeSum 2 (1 / 64) 32 0 = 1 / 2` |
| `lean4/CampaignFspPachnerInvarianceClaim.lean:162 regge_action_non_invariant_under_curved_pachner_subdivision` | `(areaInt epsInt : ℚ) (hA : 0 < areaInt) (hE : epsInt ≠ 0) : pachnerReggeActionShift 10 areaInt 0 = 0 ∧ pachnerReggeActionShift 4 areaInt 0 = 0 ∧ pachnerReggeActionShift 10 areaInt epsInt ≠ 0 ∧ pachnerReggeActionShift 4 areaInt epsInt ≠ 0` |
| `lean4/CampaignFspPachnerInvarianceClaim.lean:181 curved_wdw_defect_mass_shifts_under_pachner_moves` | `: let f0 := s4SeedFaceVector let f1 := pachner1to5 f0 let f2 := pachner2to4 f1 let f3 := pachner3to3 f2 curvedWdwDefectMass f0 = 45 ∧ curvedWdwDefectMass f1 = 60 ∧ curvedWdwDefectMass f2 = 63 ∧ curvedWdwDefectMass f3 = 63 ∧ curvedWdwDefectMass f0 < curvedWdwDefectMass f1 ∧ curvedWdwDefectMass f1 < curvedWdwDefectMass f2` |
| `lean4/CampaignFspPachnerInvarianceClaim.lean:197 signed_hinge_deficits_can_cancel_under_pachner_move_fence` | `: let deficits : Fin 4 → ℚ := ![1, -1, 1, -1] 0 < deficits 0 ∧ (∑ i : Fin 4, deficits i) = 0` |
| `lean4/CampaignFspPachnerInvarianceClaim.lean:206 unnormalized_simplex_weight_fails_pachner_invariance_fence` | `(w4 : ℚ) (hw4 : w4 ≠ 0) (f : FaceVector4D) : linearStateSumExponent ![0, 0, 0, 0, w4] (pachner1to5 f) - linearStateSumExponent ![0, 0, 0, 0, w4] f = 4 * w4 ∧ linearStateSumExponent ![0, 0, 0, 0, w4] (pachner2to4 f) - linearStateSumExponent ![0, 0, 0, 0, w4] f = 2 * w4 ∧ 4 * w4 ≠ 0 ∧ 2 * w4 ≠ 0` |
| `lean4/CampaignFspPachnerInvarianceClaim.lean:223 pachner_moves_independent_of_fermion_sign_fence` | `(f : FaceVector4D) : (1 : ℤ) * eulerChar4D (pachner1to5 f) + (-1 : ℤ) * eulerChar4D (pachner1to5 f) = 0 ∧ (1 : ℤ) * eulerChar4D (pachner2to4 f) + (-1 : ℤ) * eulerChar4D (pachner2to4 f) = 0` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_325_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
