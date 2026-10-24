# PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN. U0 and U1 are well-formed duplicate-free regimes with data count 2, one form of arity 1, and requirement (0, 1). BL is well-formed and duplicate-free with form arity 2 and instance arguments 0 and 1. Each exhaustive candidate list has length 2. The datum swap is an isomorphism from U0 to U1, and the exhaustive keys of U0 and U1 are equal. No isomorphism from U0 to BL exists, and those exhaustive keys differ.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 9
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

These facts are the exhaustive Lean search on U0, U1, and BL. They are not a Python key cross-check and not an orbit comparison on exported runs. Status stays OPEN.

## Source status

closeout.txt §2.1 and §9.1 D3; continuation.txt §13 leftovers H-4 and G-9

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwIsomorphismSoundnessInLean.lean`

- file: [lean4/CampaignPgwIsomorphismSoundnessInLean.lean](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- sha256 (`bytes`): `c2602a24aae6b99d24608c00c76234467829da96088ed24cdc129f3193370d2b`
- cited in: node.lean, receipt dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json (CampaignPgwIsomorphismSoundnessInLean), record TFQ-0500
- replay: `verified`
  - receipt [dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json](../../../dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json) (module `CampaignPgwIsomorphismSoundnessInLean`): recorded sha256 `c2602a24aae6b99d24608c00c76234467829da96088ed24cdc129f3193370d2b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwIsomorphismSoundnessInLean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwIso_BL_wf` | yes | yes | yes | propext | `#print axioms pgwIso_BL_wf` |
| `pgwIso_U0_U1` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwIso_U0_U1` |
| `pgwIso_U0_not_BL` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwIso_U0_not_BL` |
| `pgwIso_U0_wf` | yes | yes | yes | propext | `#print axioms pgwIso_U0_wf` |
| `pgwIso_U1_wf` | yes | yes | yes | propext | `#print axioms pgwIso_U1_wf` |
| `pgwIso_candidate_counts` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwIso_candidate_counts` |
| `pgwIso_keys_eq` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwIso_keys_eq` |
| `pgwIso_keys_ne` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwIso_keys_ne` |
| `pgwIso_set_collections` | yes | yes | yes | none | `#print axioms pgwIso_set_collections` |
- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-isomorphism-soundness-in-lean.py`

- file: [checks/independent/pgw-isomorphism-soundness-in-lean.py](../../../checks/independent/pgw-isomorphism-soundness-in-lean.py)
- sha256 (`bytes`): `a4aa2455b1a9bbf4a81c29d09095f4b78a15ad1e50129a0f3182960fedbcb841`
- cited in: record TFQ-0500

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0500_isomorphism_soundness_in_lean.md`

- file: [dag/derivations/02_genesis/tfq_0500_isomorphism_soundness_in_lean.md](../../../dag/derivations/02_genesis/tfq_0500_isomorphism_soundness_in_lean.md)
- sha256 (`lf-normalised`): `89cc86c47a64f2f49988950238f32c1503d09a445f732de82da2ecda9cb1636c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0500
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md`

- file: [dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md](../../../dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md)
- sha256 (`lf-normalised`): `539e92db444008829dc5b977f1ab37b185fb180012a1e435b0e7e1aa1c7dd74d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json`

- file: [dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json](../../../dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json)
- sha256 (`lf-normalised`): `d74c213ad293d2fc6f82dd6c5dbda67728bb023173c99f2ee834174de465b95d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py::canonical_bruteforce`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs::canonical_bruteforce`

## Routes

Incoming (1):

- `PGW-R-ISOMORPHISM-SOUNDNESS-IN-LEAN` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

