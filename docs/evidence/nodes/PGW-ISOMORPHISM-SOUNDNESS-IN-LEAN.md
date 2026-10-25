# PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed in Lean 4 to colorings of two data. A coloring is a pair of bits. The swap exchanges the two bits and is an involution. The serialization reads a bit as 0 or 1. The key is the lexicographic minimum of a coloring and its swap. The four keys are (0, 0), (0, 1), (0, 1), and (1, 1). Equal keys hold exactly when one coloring is the other or its swap. Two colorings share the key (0, 1). The two constant colorings are fixed by the swap and have different keys.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open; the run trees are quotiented by the implemented isomorphism, whose soundness is computational at the regimes cross-checked. Narrowed in Lean 4 to colorings of two data, where equal keys hold exactly when one coloring is the other or its swap. The implemented key, the regimes past the brute-force limit, and the orbit comparison stay open.

## Source status

closeout.txt §2.1 and §9.1 D3; continuation.txt §13 leftovers H-4 and G-9

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwIsomorphismSoundnessInLean.lean`

- file: [lean4/CampaignPgwIsomorphismSoundnessInLean.lean](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- sha256 (`bytes`): `0a7746fe915e4c36af9af95683c1155804f19a4287682731f226aac7b794e2d0`
- cited in: node.lean, receipt dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json (CampaignPgwIsomorphismSoundnessInLean), record TFQ-0500
- replay: `verified`
  - receipt [dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json](../../../dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json) (module `CampaignPgwIsomorphismSoundnessInLean`): recorded sha256 `0a7746fe915e4c36af9af95683c1155804f19a4287682731f226aac7b794e2d0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwIsomorphismSoundnessInLean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwIsoConstants` | yes | yes | yes | none | `#print axioms pgwIsoConstants` |
| `pgwIsoFour` | yes | yes | yes | none | `#print axioms pgwIsoFour` |
| `pgwIsoKeyIff` | yes | yes | yes | none | `#print axioms pgwIsoKeyIff` |
| `pgwIsoKeySwap` | yes | yes | yes | none | `#print axioms pgwIsoKeySwap` |
| `pgwIsoKeysOfFour` | yes | yes | yes | none | `#print axioms pgwIsoKeysOfFour` |
| `pgwIsoMixed` | yes | yes | yes | none | `#print axioms pgwIsoMixed` |
| `pgwIsoSwapInvolutive` | yes | yes | yes | none | `#print axioms pgwIsoSwapInvolutive` |
- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-isomorphism-soundness-in-lean.py`

- file: [checks/independent/pgw-isomorphism-soundness-in-lean.py](../../../checks/independent/pgw-isomorphism-soundness-in-lean.py)
- sha256 (`bytes`): `d92aa771404c2b0b6f6da5dfbf2b471886ad3c9b6306a1a802cd549a2a69a0b7`
- cited in: record TFQ-0500

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0500_isomorphism_soundness_in_lean.md`

- file: [dag/derivations/02_genesis/tfq_0500_isomorphism_soundness_in_lean.md](../../../dag/derivations/02_genesis/tfq_0500_isomorphism_soundness_in_lean.md)
- sha256 (`lf-normalised`): `b7370002035fc4b507fd52e6a0e295286921c7bea25fef2cf92e1c85147425d1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0500
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md`

- file: [dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md](../../../dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md)
- sha256 (`lf-normalised`): `4fb55b66f5215bd68c8ec68e70b5b74dada4b1eca936cd883fde7357f041cddf`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json`

- file: [dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json](../../../dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json)
- sha256 (`lf-normalised`): `dbfb0a49f4acb2876d1793dcb187c44353678e785409c3d15beca10ea6a89ab2`
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

