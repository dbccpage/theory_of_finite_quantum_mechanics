# Review of GTH-SHADOW P0

Scope: staged diff for derive/GTH-SHADOW, base origin/main at c54ab983ebffd28f05f0e52cd419e647ef5e6cf4. Reviewed before commit. Rule applied: a GAP_NO_DERIVATION route may record a reviewed negative and may not invent a generator, raise a status, or cite AdmitCore as the node's theorem.

Method: read the node and route in dag/derivation_dag.json, the operad, both derivation notes, lean4/Imported/GenesisOngoing/Fifteenth/Step.lean (reaching, reaching_does_not_admit, reaching_ne_admitted, admission_not_assertion, admission_not_a_kind), lean4/GenesisComputation.lean (GenesisCopy.Regime), lean4/GenesisHottShadow.lean (imports, header, AdmissionTupleShadow, shadowOf, edgeRegime, FinSemiSimplicial1, forwardReading, backwardReading, edge_regime_does_not_determine_semisimplicial1, face_map_card, recovers_fun_card, FinGlobular1, globeForward, globeBackward, edge_regime_does_not_determine_globular1, globular_pair_card, globular_orientation_count), and lean4/AdmitCore.lean (header and Regime). Lean, lake, and cargo were not rebuilt.

Result: 0 FULL, 0 NARROWED, 0 OVERCLAIM. No node was raised. The mining record is a negative. It passes the stage bound.

Corrections to the stage text:
- collection_status stays source_candidates_collected_semantic_mining_open. dag/pfp/validate_prompts.py rejects every other value as a fabricated mining completion. The reviewed negative stays in stage_history and dag/results/GTH-SHADOW.
- mining_status is REVIEWED_ABSENT, not FILLED. The slots stay empty.
- The independent note's sentence "Nothing in Lean." is the note's claim. lean4/GenesisHottShadow.lean exists and is not cited by the node. This stage does not rewrite that note and does not treat the file as a theorem of the node.
- The docstring of admission_not_a_kind at line 58 is not the theorem type. The type at lines 59-60 is reaching = .notAdmitted. The stage text keeps that split.
- dag/operads/index.json is not edited. Open campaign rows already touch the neighbouring index entries.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| GTH-SHADOW | none cited; lean list empty | negative mining, not a theorem | Route GTH-R-GTH-SHADOW stays GAP_NO_DERIVATION. reaching_does_not_admit (Step.lean:38) is an equality with notAdmitted. shadowOf (GenesisHottShadow.lean:68) copies five regime fields. edge_regime_does_not_determine_semisimplicial1 (line 295) and edge_regime_does_not_determine_globular1 (line 364) state two unequal readings of one declared tuple. The header at lines 51-52 says the determination claim is not proved. AdmitCore.Regime (AdmitCore.lean:42) is a different carrier. |

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| stage diff | face_map_card is 4 | \|Fin 1 → Fin 2\| = 2^1 = 2, then \|Fin 2 → that\| = 2^2 = 4. Integer powers. Lean was not rebuilt | match |
| stage diff | recovers_fun_card is 2 | The four pairs (f 0 0, f 1 0) in {0,1}^2, of which (1,0) and (0,1) meet recoversFun. Count is 2 | match |
| stage diff | globular_pair_card is 4 | \|Fin 1 → Fin 2\| = 2, and 2 × 2 = 4 | match |
| stage diff | globular_orientation_count is 2 | The four pairs (s 0, t 0) in {0,1}^2, of which (0,1) and (1,0) meet recoversGlobeB. Count is 2 | match |

## Scanner output
`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` exited 0. Scope: changes since origin/main, merge base c54ab983ebff. HIGH=0 MEDIUM=0 LOW=0. Lean was not rebuilt. No baseline entry is added.

## Prompt validator
`python -X utf8 dag/pfp/validate_prompts.py` before this commit reports the same two pre-existing errors: TFQ-0084 local source pin changed, and LQG-PR-ALLOWED-REGION-TARGET legacy fabricated contract. GTH-SHADOW is not in that list. The whole validator is not claimed green. No Lean rebuild is claimed.
