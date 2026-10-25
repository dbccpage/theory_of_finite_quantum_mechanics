# OPS-OBSERVER-DECLARATION-REFUSAL

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A five-field draft on one Bell label is classified by comparing each field with a fixed text, and the comparison does not read a defect. The kernel text is "support presheaf over the maximal-context cover {0,2}|{0,3}|{1,2}|{1,3} with arities 2,2,2,2". The admissibility text is "noncontextual polytope conv(A)". The norm text is "L1". The terminal text is "defect = 0 -\> ExactRepair; defect \> 0 and a support-level global section exists -\> ClosedResidual; defect \> 0 and none exists -\> OpenObstruction". The layer text is "WDP-CH10-D01 diagnostic". Take a draft that already carries these five texts. Replacing one field by a missing value, the empty string, or one space yields the undeclared class of that field. Replacing one field by a text other than the empty string, one space, and that field's accepted text yields the unsupported class of that field and keeps the declared text. The draft of the five accepted texts is the accepted class, and the authority text of that class is "None".

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The computing tests are Rust tests of the source repository. The in-repo copy of the module (code/rust/src/sheaf_theory/empirical_presheaf) uses omega_solvers, an external crate that is not a member of the code/rust workspace (cargo metadata --no-deps lists no such package), and the source test file was not imported. These tests are not run here. Outside this slice: a defect receipt, Unicode whitespace other than one space, the terminal token, the typed profile, and any kernel label other than the one Bell label. The Python gate on node OPS-THREE-ROLE-GATE checks its own observer field and is not this classifier.

## Source status

Ledger rows L035-A3 and L035-A4: computed + by construction, by the Rust tests an_undeclared_observer_component_is_refused_before_any_arithmetic, pr1080_blank_observer_fields_are_refused, pr1080_receipt_does_not_accept_an_unsupported_observer_profile and evaluation_receipts_carry_the_terminal_token_and_no_authority. Held at CONDITIONAL because those tests are not run in this repository.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignOpsObserverDeclarationRefusal.lean`

- file: [lean4/CampaignOpsObserverDeclarationRefusal.lean](../../../lean4/CampaignOpsObserverDeclarationRefusal.lean)
- sha256 (`bytes`): `c8007f7921335135f125e83f5c4b53bf556574918f26528a4bd92a2dfac406d2`
- cited in: node.source, receipt dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json (CampaignOpsObserverDeclarationRefusal)
- replay: `verified`
  - receipt [dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json](../../../dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json) (module `CampaignOpsObserverDeclarationRefusal`): recorded sha256 `c8007f7921335135f125e83f5c4b53bf556574918f26528a4bd92a2dfac406d2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignOpsObserverDeclarationRefusal`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `accepted_authority` | yes | yes | yes | propext | `#print axioms accepted_authority` |
| `accepted_draft_class` | yes | yes | yes | propext | `#print axioms accepted_draft_class` |
| `blank_on_accepted` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms blank_on_accepted` |
| `mismatch_on_accepted` | yes | yes | yes | propext | `#print axioms mismatch_on_accepted` |

- counts toward the grade: yes

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/observer.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/observer.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/observer.rs)
- sha256 (`bytes`): `ad805dc728de0f9ff8e80e8cd7b80d9b3682fc86d4d9d8220a462ca556c2c61f`
- cited in: node.rust, record TFQ-2518

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `evaluate_l1_claim` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/ops-observer-declaration-refusal.py`

- file: [checks/independent/ops-observer-declaration-refusal.py](../../../checks/independent/ops-observer-declaration-refusal.py)
- sha256 (`bytes`): `a7cc4ebafe13b323cbd39f6c029495563d700d65ed635cded5b75717661419af`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2518_ops_observer_declaration_refusal.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2518_ops_observer_declaration_refusal.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2518_ops_observer_declaration_refusal.md)
- sha256 (`lf-normalised`): `def99ded1aaab8ec2a5f749108ccad35f403ac3902224d3b6d43bd2aff70e758`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2518
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ops-observer-declaration-refusal.md`

- file: [dag/derivations/independent/ops-observer-declaration-refusal.md](../../../dag/derivations/independent/ops-observer-declaration-refusal.md)
- sha256 (`lf-normalised`): `497b54832bba0af30f5b7f8f4268766202a8508d341844e790f8d26321e68e26`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json`

- file: [dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json](../../../dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json)
- sha256 (`lf-normalised`): `0575c59cdd87fb230882734976515ccbbb5a3c17f958b46b1f74c20c88757741`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `649532625cf9e8ec085a420fd1bad9227fcc4dae9f06ba02be1eb19f497e3ec7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-OBSERVER-DECLARATION-REFUSAL` `RECORD_PARENT`: [OPS-OBSERVER-TUPLE](OPS-OBSERVER-TUPLE.md) (DEFINITION)

Outgoing (1):

- `OPS-R-REFUTED-EARLIER-RUST` `RECORD_PARENT`: [OPS-REFUTED-EARLIER-RUST](OPS-REFUTED-EARLIER-RUST.md) (REFUTED)
