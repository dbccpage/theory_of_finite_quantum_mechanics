# PGW-CONTEXT-FIDELITY

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN: in the two-code model the stale context is 0 and the replayed context is 1. These codes differ. The empty-claim step holds at 0 and fails at 1. The binding check accepts a pair exactly when the two codes are equal, so it refuses (0, 1) and accepts (1, 1). Of the four ordered pairs drawn from {0, 1}, exactly two are accepted. Trial 2 Result 15, Prompt 12, Prompt 17, and a general ValidTrace semantics stay unresolved. Status stays OPEN.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The identities are one two-code witness. They do not define ValidTrace for an arbitrary trace, do not reconstruct a history, and do not read the trial record. The listed replay certifiers still do not define ValidTrace. Status stays OPEN.

## Source status

v1 Derivation 5 (clean theorem target, no proof); 000_oepregen 03_results_and_arguments.md section 7 (statement 7)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwContextFidelity.lean`

- file: [lean4/CampaignPgwContextFidelity.lean](../../../lean4/CampaignPgwContextFidelity.lean)
- sha256 (`bytes`): `b2e809eb8eb262db8101602ebeb242043e07260005f91b7cc848ac061656ac81`
- cited in: node.lean, receipt dag/research/campaign_pgw-context-fidelity_lean_replay.json (CampaignPgwContextFidelity), record TFQ-0427
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-fidelity_lean_replay.json](../../../dag/research/campaign_pgw-context-fidelity_lean_replay.json) (module `CampaignPgwContextFidelity`): recorded sha256 `b2e809eb8eb262db8101602ebeb242043e07260005f91b7cc848ac061656ac81` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwContextFidelity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwContext_accept_count` | yes | yes | yes | none | `#print axioms pgwContext_accept_count` |
| `pgwContext_binding_accepts_match` | yes | yes | yes | none | `#print axioms pgwContext_binding_accepts_match` |
| `pgwContext_binding_refuses_stale` | yes | yes | yes | none | `#print axioms pgwContext_binding_refuses_stale` |
| `pgwContext_codes_differ` | yes | yes | yes | none | `#print axioms pgwContext_codes_differ` |
| `pgwContext_empty_claim_on_replay` | yes | yes | yes | none | `#print axioms pgwContext_empty_claim_on_replay` |
| `pgwContext_empty_claim_on_stale` | yes | yes | yes | none | `#print axioms pgwContext_empty_claim_on_stale` |
- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/certification.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/certification.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-context-fidelity.py`

- file: [checks/independent/pgw-context-fidelity.py](../../../checks/independent/pgw-context-fidelity.py)
- sha256 (`bytes`): `98856d79779ed2da10320b7ec84bf410c74b464286748ed7f9e7a48dd801bdf0`
- cited in: record TFQ-0427
- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0427_context_fidelity.md`

- file: [dag/derivations/01_pregenesis/tfq_0427_context_fidelity.md](../../../dag/derivations/01_pregenesis/tfq_0427_context_fidelity.md)
- sha256 (`lf-normalised`): `9b799936c51c90b64d467ab9242464e198ab8fb023e7ac7f9d749e81aa9d7fb9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0427
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/02_trial_record.md`

- file: `omega_engine_education/documentation/000_oepregen/02_trial_record.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`

- file: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md`

- file: `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py::certify`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/certification.rs::certifies`

## Absences recorded by the TFQ records

- TFQ-0427 lean4: no Lean definition of ValidTrace or of the context-fidelity non-implication; Represented.replay_deterministic in 000_genesis_19l57g1/lean4/Derivation/Represented.lean shows only that replay is a function of the history

## Routes

Incoming (1):

- `PGW-R-CONTEXT-FIDELITY` `GAP_NO_DERIVATION`: [PGW-REPLAY-NECESSITY](PGW-REPLAY-NECESSITY.md) (PROVED_LEAN)

Outgoing (0):

