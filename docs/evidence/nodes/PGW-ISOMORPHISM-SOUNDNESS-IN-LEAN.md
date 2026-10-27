# PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> CL-ISO-SOUND, soundness of the implemented isomorphism key, is a finite computation only: the Python key procedure's classes are cross-checked against a brute-force minimum over bijections, and the Lean side is unresolved (D3: no Lean evidence). Attempt two leaves 482 regimes above the brute-force limit of the key cross-check (H-4), and attempt one's check of the Python orbit against the Lean orbit (G-9) is not done.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- distinct cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

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

### Lean: `lean4/PregenesisIsomorphismSoundness.lean`

- file: [lean4/PregenesisIsomorphismSoundness.lean](../../../lean4/PregenesisIsomorphismSoundness.lean)
- sha256 (`bytes`): `0a7746fe915e4c36af9af95683c1155804f19a4287682731f226aac7b794e2d0`
- cited in: node.lean, receipt dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json (PregenesisIsomorphismSoundness), receipt dag/research/pr_352_review_replay.json (PregenesisIsomorphismSoundness), record TFQ-0500
- replay: `verified`
  - receipt [dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json](../../../dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json) (module `PregenesisIsomorphismSoundness`): recorded sha256 `0a7746fe915e4c36af9af95683c1155804f19a4287682731f226aac7b794e2d0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_352_review_replay.json](../../../dag/research/pr_352_review_replay.json) (module `PregenesisIsomorphismSoundness`): recorded sha256 `0a7746fe915e4c36af9af95683c1155804f19a4287682731f226aac7b794e2d0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build PregenesisIsomorphismSoundness`

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

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs)
- sha256 (`bytes`): `bd91e864bb54ade9ed3890a65d89f57500cef2fb66e060eb5e18359d6c6187ea`
- cited in: node.rust, record TFQ-0500

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `canonical_bruteforce` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py)
- sha256 (`bytes`): `b0f1f3bcf05126111a07706f4388a9fff5e30455d4b8f127966cf99ab0d0886e`
- cited in: record TFQ-0500

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `canonical_bruteforce` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/pgw-isomorphism-soundness-in-lean.py`

- file: [checks/independent/pgw-isomorphism-soundness-in-lean.py](../../../checks/independent/pgw-isomorphism-soundness-in-lean.py)
- sha256 (`bytes`): `d92aa771404c2b0b6f6da5dfbf2b471886ad3c9b6306a1a802cd549a2a69a0b7`
- cited in: record TFQ-0500

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt)
- sha256 (`lf-normalised`): `c613e357809438876d1fcec34ea896548f17f4e9d4ea7f21048fafe9451651ac`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0500_isomorphism_soundness_in_lean.md`

- file: [dag/derivations/02_genesis/tfq_0500_isomorphism_soundness_in_lean.md](../../../dag/derivations/02_genesis/tfq_0500_isomorphism_soundness_in_lean.md)
- sha256 (`lf-normalised`): `bab5014a670aff68e6ff6c5036bc70ab78443ee3c1caa9be5d7fad0f56f936c0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0500
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md`

- file: [dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md](../../../dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md)
- sha256 (`lf-normalised`): `c3402ac66350da58e38708532e19f867114313383b42ca60ebbef9dc171ff771`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json`

- file: [dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json](../../../dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json)
- sha256 (`lf-normalised`): `c9b03c277045c95d1dc054e62cfd9b1e1da0c3a9972832d83311fb9efb6e0e1d`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `PGW-R-ISOMORPHISM-SOUNDNESS-IN-LEAN` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

