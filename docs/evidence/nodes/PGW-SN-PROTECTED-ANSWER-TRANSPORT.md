# PGW-SN-PROTECTED-ANSWER-TRANSPORT

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(6) recovers the old image exactly, but transporting a protected answer F across the lift u requires a target counterpart F′ with F′∘u = F, and preserving future operations requires the corresponding commuting transition equations. In Lean 4, OldImageLaw u r yields canonical retraction-induced transport retractionTransport r F d satisfying F′∘u = F (retraction_transport_law) and canonical transition lifts (canonical_transition_lift_commutes), including for SnCarrier (snCarrier_answer_transport, snCarrier_canonical_transition_square) and the integer S6Descent slice model (s6Descent_answer_transport, s6Descent_canonical_transition_square), while k-step commuting squares preserve transported answers (commuting_square_preserves_transported_answer). Off the image, F′ has |Q|^(|B|−|A|) counterparts (transport_counterpart_card, transport_off_image_underdetermined), unconstrained target transitions violate preservation (snCarrier_transition_counterexample, s6Descent_transition_counterexample), and the old-image identity alone establishes neither a logical conservative extension off the image (not_conservative_extension_off_image), nor an adjunction (old_image_not_right_inverse, old_image_not_left_galois_adjunction), nor resolution of an unrelated demand (unrelated_demand_not_resolved_by_lift, snCarrier_s6_demand_active).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 27
- cited Lean declarations covered by a current replay receipt: 26
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The canonical retraction-induced transport, counterpart count, k-step commuting-square preservation, SnCarrier and integer S6Descent instances, and non-implication countermodels are checked in Lean 4; the node remains OPEN because arbitrary future target transitions require case-by-case commuting-square verification, the external Python S6Descent class in 002_oesn/code/sn_core.py is outside this checkout, and the exercise value s₆ = 1 records an issued descent-checking obligation, not a forced survivor.

## Source status

000_pre_genesis_to_mssn paper.md section 7 S(6) row; 002_oesn level_06; CampaignSnProtectedAnswerTransport.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignSnProtectedAnswerTransport.lean`

- file: [lean4/CampaignSnProtectedAnswerTransport.lean](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- sha256 (`bytes`): `dcd1f1a24a9f867c95c141246abd825c3f7caa159ca0c73ebd1b6063b7259ffd`
- cited in: node.lean, receipt dag/research/campaign_pgw-sn-protected-answer-transport_lean_replay.json (CampaignSnProtectedAnswerTransport), record TFQ-0519
- replay: `verified`
  - receipt [dag/research/campaign_pgw-sn-protected-answer-transport_lean_replay.json](../../../dag/research/campaign_pgw-sn-protected-answer-transport_lean_replay.json) (module `CampaignSnProtectedAnswerTransport`): recorded sha256 `dcd1f1a24a9f867c95c141246abd825c3f7caa159ca0c73ebd1b6063b7259ffd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignSnProtectedAnswerTransport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignSnProtectedAnswerTransport.canonical_transition_lift_commutes` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.canonical_transition_lift_commutes` |
| `CampaignSnProtectedAnswerTransport.commuting_square_iff_boolean_answers_preserved_on_image` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.commuting_square_iff_boolean_answers_preserved_on_image` |
| `CampaignSnProtectedAnswerTransport.commuting_square_iterated` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignSnProtectedAnswerTransport.commuting_square_iterated` |
| `CampaignSnProtectedAnswerTransport.commuting_square_preserves_transported_answer` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignSnProtectedAnswerTransport.commuting_square_preserves_transported_answer` |
| `CampaignSnProtectedAnswerTransport.not_conservative_extension_off_image` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.not_conservative_extension_off_image` |
| `CampaignSnProtectedAnswerTransport.old_image_not_left_galois_adjunction` | yes | yes | yes | propext | `#print axioms CampaignSnProtectedAnswerTransport.old_image_not_left_galois_adjunction` |
| `CampaignSnProtectedAnswerTransport.old_image_not_right_inverse` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.old_image_not_right_inverse` |
| `CampaignSnProtectedAnswerTransport.retraction_transport_law` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.retraction_transport_law` |
| `CampaignSnProtectedAnswerTransport.s6Descent_answer_transport` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.s6Descent_answer_transport` |
| `CampaignSnProtectedAnswerTransport.s6Descent_canonical_transition_square` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.s6Descent_canonical_transition_square` |
| `CampaignSnProtectedAnswerTransport.s6Descent_old_image_law` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.s6Descent_old_image_law` |
| `CampaignSnProtectedAnswerTransport.s6Descent_transition_counterexample` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.s6Descent_transition_counterexample` |
| `CampaignSnProtectedAnswerTransport.snCarrier_answer_transport` | yes | yes | yes | propext | `#print axioms CampaignSnProtectedAnswerTransport.snCarrier_answer_transport` |
| `CampaignSnProtectedAnswerTransport.snCarrier_canonical_transition_square` | yes | yes | yes | propext | `#print axioms CampaignSnProtectedAnswerTransport.snCarrier_canonical_transition_square` |
| `CampaignSnProtectedAnswerTransport.snCarrier_off_image_underdetermined` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignSnProtectedAnswerTransport.snCarrier_off_image_underdetermined` |
| `CampaignSnProtectedAnswerTransport.snCarrier_s6_demand_active` | yes | yes | yes | propext | `#print axioms CampaignSnProtectedAnswerTransport.snCarrier_s6_demand_active` |
| `CampaignSnProtectedAnswerTransport.snCarrier_transition_counterexample` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignSnProtectedAnswerTransport.snCarrier_transition_counterexample` |
| `CampaignSnProtectedAnswerTransport.snRetract_nonDescent_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignSnProtectedAnswerTransport.snRetract_nonDescent_iff` |
| `CampaignSnProtectedAnswerTransport.snRetract_old_image_law` | yes | yes | yes | propext | `#print axioms CampaignSnProtectedAnswerTransport.snRetract_old_image_law` |
| `CampaignSnProtectedAnswerTransport.transition_square_not_implied_general` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.transition_square_not_implied_general` |
| `CampaignSnProtectedAnswerTransport.transport_counterpart_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnProtectedAnswerTransport.transport_counterpart_card` |
| `CampaignSnProtectedAnswerTransport.transport_off_image_underdetermined` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnProtectedAnswerTransport.transport_off_image_underdetermined` |
| `CampaignSnProtectedAnswerTransport.transport_unique_on_image` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.transport_unique_on_image` |
| `CampaignSnProtectedAnswerTransport.typed_retraction_transport_law` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.typed_retraction_transport_law` |
| `CampaignSnProtectedAnswerTransport.typed_retraction_transport_refuses` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.typed_retraction_transport_refuses` |
| `CampaignSnProtectedAnswerTransport.unrelated_demand_not_resolved_by_lift` | yes | yes | yes | none | `#print axioms CampaignSnProtectedAnswerTransport.unrelated_demand_not_resolved_by_lift` |
- counts toward the grade: yes

### Python: `checks/independent/pgw-sn-protected-answer-transport.py`

- file: [checks/independent/pgw-sn-protected-answer-transport.py](../../../checks/independent/pgw-sn-protected-answer-transport.py)
- sha256 (`bytes`): `262b74e9e0f5a17e09bd90e670e10af9525c72548f7272e62848f0f9fad2f0d0`
- cited in: record TFQ-0519

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0519_sn_protected_answer_transport.md`

- file: [dag/derivations/05_mssn_sn/tfq_0519_sn_protected_answer_transport.md](../../../dag/derivations/05_mssn_sn/tfq_0519_sn_protected_answer_transport.md)
- sha256 (`lf-normalised`): `b1de6ce655bfb88ddb4ffbe21e31cd9ee65667d91bde3d9b23bd6e100de2fe00`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0519
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-sn-protected-answer-transport.md`

- file: [dag/derivations/independent/pgw-sn-protected-answer-transport.md](../../../dag/derivations/independent/pgw-sn-protected-answer-transport.md)
- sha256 (`lf-normalised`): `af28444b874d2ff50ab0c4ae25109401d610a2f8b694ba97873b2b171b012412`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_06_tower_extension_retraction.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_06_tower_extension_retraction.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/sn.md`

- file: `omega_engine_education/documentation/002_oesn/sn.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0519 rust: no Rust check of answer transport across a lift

## Routes

Incoming (1):

- `PGW-R-SN-PROTECTED-ANSWER-TRANSPORT` `GAP_NO_DERIVATION`: [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) (PROVED_LEAN), [PG-OLD-IMAGE-INJECTIVE](PG-OLD-IMAGE-INJECTIVE.md) (PROVED_LEAN)

Outgoing (0):

