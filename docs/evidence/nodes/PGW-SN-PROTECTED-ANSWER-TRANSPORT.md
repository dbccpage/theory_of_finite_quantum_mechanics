# PGW-SN-PROTECTED-ANSWER-TRANSPORT

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(6) recovers the old image exactly, but transporting a protected answer F across the lift u requires a target counterpart F′ with F′∘u = F, and preserving future operations requires the corresponding commuting transition equations. In Lean 4, OldImageLaw u r yields canonical retraction-induced transport retractionTransport r F d satisfying F′∘u = F (retraction_transport_law) and canonical transition lifts (canonical_transition_lift_commutes), including for SnCarrier (snCarrier_answer_transport, snCarrier_canonical_transition_square) and the integer S6Descent slice model (s6Descent_answer_transport, s6Descent_canonical_transition_square), while k-step commuting squares preserve transported answers (commuting_square_preserves_transported_answer). Off the image, F′ has |Q|^(|B|−|A|) counterparts (transport_counterpart_card, transport_off_image_underdetermined), unconstrained target transitions violate preservation (snCarrier_transition_counterexample, s6Descent_transition_counterexample), and the old-image identity alone establishes neither a logical conservative extension off the image (not_conservative_extension_off_image), nor an adjunction (old_image_not_right_inverse, old_image_not_left_galois_adjunction), nor resolution of an unrelated demand (unrelated_demand_not_resolved_by_lift, snCarrier_s6_demand_active).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 27
- distinct cited Lean declarations covered by a current replay receipt: 26
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

pregenesis_to_minimal_symbol_systems paper.md section 7 S(6) row; 002_oesn level_06; ProtectedAnswerTransport.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ProtectedAnswerTransport.lean`

- file: [lean4/ProtectedAnswerTransport.lean](../../../lean4/ProtectedAnswerTransport.lean)
- sha256 (`bytes`): `8dffedb7cf1be35160e7ff6b9b230efdd40a9da12b2df55d6aac997abfb84338`
- cited in: node.lean, receipt dag/research/campaign_pgw-sn-protected-answer-transport_lean_replay.json (ProtectedAnswerTransport), record TFQ-0519
- replay: `verified`
  - receipt [dag/research/campaign_pgw-sn-protected-answer-transport_lean_replay.json](../../../dag/research/campaign_pgw-sn-protected-answer-transport_lean_replay.json) (module `ProtectedAnswerTransport`): recorded sha256 `8dffedb7cf1be35160e7ff6b9b230efdd40a9da12b2df55d6aac997abfb84338` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ProtectedAnswerTransport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ProtectedAnswerTransport.canonical_transition_lift_commutes` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.canonical_transition_lift_commutes` |
| `ProtectedAnswerTransport.commuting_square_iff_boolean_answers_preserved_on_image` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.commuting_square_iff_boolean_answers_preserved_on_image` |
| `ProtectedAnswerTransport.commuting_square_iterated` | yes | yes | yes | Quot.sound, propext | `#print axioms ProtectedAnswerTransport.commuting_square_iterated` |
| `ProtectedAnswerTransport.commuting_square_preserves_transported_answer` | yes | yes | yes | Quot.sound, propext | `#print axioms ProtectedAnswerTransport.commuting_square_preserves_transported_answer` |
| `ProtectedAnswerTransport.not_conservative_extension_off_image` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.not_conservative_extension_off_image` |
| `ProtectedAnswerTransport.old_image_not_left_galois_adjunction` | yes | yes | yes | propext | `#print axioms ProtectedAnswerTransport.old_image_not_left_galois_adjunction` |
| `ProtectedAnswerTransport.old_image_not_right_inverse` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.old_image_not_right_inverse` |
| `ProtectedAnswerTransport.retraction_transport_law` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.retraction_transport_law` |
| `ProtectedAnswerTransport.s6Descent_answer_transport` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.s6Descent_answer_transport` |
| `ProtectedAnswerTransport.s6Descent_canonical_transition_square` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.s6Descent_canonical_transition_square` |
| `ProtectedAnswerTransport.s6Descent_old_image_law` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.s6Descent_old_image_law` |
| `ProtectedAnswerTransport.s6Descent_transition_counterexample` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.s6Descent_transition_counterexample` |
| `ProtectedAnswerTransport.snCarrier_answer_transport` | yes | yes | yes | propext | `#print axioms ProtectedAnswerTransport.snCarrier_answer_transport` |
| `ProtectedAnswerTransport.snCarrier_canonical_transition_square` | yes | yes | yes | propext | `#print axioms ProtectedAnswerTransport.snCarrier_canonical_transition_square` |
| `ProtectedAnswerTransport.snCarrier_off_image_underdetermined` | yes | yes | yes | Quot.sound, propext | `#print axioms ProtectedAnswerTransport.snCarrier_off_image_underdetermined` |
| `ProtectedAnswerTransport.snCarrier_s6_demand_active` | yes | yes | yes | propext | `#print axioms ProtectedAnswerTransport.snCarrier_s6_demand_active` |
| `ProtectedAnswerTransport.snCarrier_transition_counterexample` | yes | yes | yes | Quot.sound, propext | `#print axioms ProtectedAnswerTransport.snCarrier_transition_counterexample` |
| `ProtectedAnswerTransport.snRetract_nonDescent_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms ProtectedAnswerTransport.snRetract_nonDescent_iff` |
| `ProtectedAnswerTransport.snRetract_old_image_law` | yes | yes | yes | propext | `#print axioms ProtectedAnswerTransport.snRetract_old_image_law` |
| `ProtectedAnswerTransport.transition_square_not_implied_general` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.transition_square_not_implied_general` |
| `ProtectedAnswerTransport.transport_counterpart_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ProtectedAnswerTransport.transport_counterpart_card` |
| `ProtectedAnswerTransport.transport_off_image_underdetermined` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ProtectedAnswerTransport.transport_off_image_underdetermined` |
| `ProtectedAnswerTransport.transport_unique_on_image` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.transport_unique_on_image` |
| `ProtectedAnswerTransport.typed_retraction_transport_law` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.typed_retraction_transport_law` |
| `ProtectedAnswerTransport.typed_retraction_transport_refuses` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.typed_retraction_transport_refuses` |
| `ProtectedAnswerTransport.unrelated_demand_not_resolved_by_lift` | yes | yes | yes | none | `#print axioms ProtectedAnswerTransport.unrelated_demand_not_resolved_by_lift` |

- counts toward the grade: yes

### Python: `checks/independent/pgw-sn-protected-answer-transport.py`

- file: [checks/independent/pgw-sn-protected-answer-transport.py](../../../checks/independent/pgw-sn-protected-answer-transport.py)
- sha256 (`bytes`): `262b74e9e0f5a17e09bd90e670e10af9525c72548f7272e62848f0f9fad2f0d0`
- cited in: record TFQ-0519

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md)
- sha256 (`lf-normalised`): `a4a7d840b11e912896032aebc9ead95f7978c0e6f60656f44645c6d8fadf593b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0519_sn_protected_answer_transport.md`

- file: [dag/derivations/05_mssn_sn/tfq_0519_sn_protected_answer_transport.md](../../../dag/derivations/05_mssn_sn/tfq_0519_sn_protected_answer_transport.md)
- sha256 (`lf-normalised`): `879819ca8bf8b694621267993f1561ec5a7de6b507c67efc5addabc02806e5bf`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0519
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-sn-protected-answer-transport.md`

- file: [dag/derivations/independent/pgw-sn-protected-answer-transport.md](../../../dag/derivations/independent/pgw-sn-protected-answer-transport.md)
- sha256 (`lf-normalised`): `05e6d5867f9a25014fd119c5cd98293bf01c8c311ad1a1a63b06c0b94d43181b`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:500c64e5f321b6a2bc3c9e2258464755d50505324ac671b644f2848cf7a84f01:39-42`
- `external:sha256:7cd90f66662c2628f0fcc5d8fb3154cfa6b0c4274de439fb73be21b2eb5673f7:97-99`

## Absences recorded by the TFQ records

- TFQ-0519 rust: no Rust check of answer transport across a lift

## Routes

Incoming (1):

- `PGW-R-SN-PROTECTED-ANSWER-TRANSPORT` `GAP_NO_DERIVATION`: [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) (PROVED_LEAN), [PG-OLD-IMAGE-INJECTIVE](PG-OLD-IMAGE-INJECTIVE.md) (PROVED_LEAN)

Outgoing (0):

