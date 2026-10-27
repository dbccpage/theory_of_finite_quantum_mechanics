# PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> At Challenge 2 both \<a\> and \<ab\> are supplied and retained, so reading L admits (\<a\>, \<ab\>) and reading F admits (\<\>, \<a\>, \<ab\>). In both readings every admitted pair is observationally collapsed (R2L_collapsed, R2F_collapsed): two externally distinct inscriptions remain internally indistinguishable. The countermodel admission_without_expressive_increase admits a fresh datum, a real state change, while the pair stays collapsed, a counterexample to the claim that a new external inscription necessarily increases internal expressive power. The recorded Challenge 0-3 histories replay exactly to the Challenge 3 regimes R2L and R2F (historyL_replays, historyF_replays).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Admission changed only the metatheoretic datum count and the replayable history; glyph identity, component count, order and substring structure stay internally unavailable, and the readings stay unselected (TFQ-0380).

## Source status

genesis_source.txt section 6 \[theorem\] and \[counterexample\]; Inertia.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Inertia.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Inertia.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Inertia.lean)
- sha256 (`bytes`): `f13ac6bc0563ae6e1c731e705e79fbb7bd28cc3d287f5bb90ad7fe9fae607f67`
- cited in: node.lean, record TFQ-0435
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Inertia`): recorded sha256 `f13ac6bc0563ae6e1c731e705e79fbb7bd28cc3d287f5bb90ad7fe9fae607f67` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Inertia.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `R2F_collapsed` | yes | yes | yes | propext | `#print axioms R2F_collapsed` |
| `R2L_collapsed` | yes | yes | yes | propext | `#print axioms R2L_collapsed` |
| `admission_without_expressive_increase` | yes | yes | yes | propext | `#print axioms admission_without_expressive_increase` |
| `historyF_replays` | yes | yes | yes | propext | `#print axioms historyF_replays` |
| `historyL_replays` | yes | yes | yes | propext | `#print axioms historyL_replays` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs)
- sha256 (`bytes`): `0e3a65e8050ce25cab79310ab655dbae54e8c6bc1dbdbdbd130d8cc65dff4452`
- cited in: node.rust, record TFQ-0435

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `challenge2_admission_need_not_increase_expressive_power` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py)
- sha256 (`bytes`): `23803a3dcce2adf0dee623caba33791d41a25d2da3fdfd226da3cad2ee140b5e`
- cited in: record TFQ-0435

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `challenge2_report` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0435_challenge2_admitted_but_collapsed.md`

- file: [dag/derivations/02_genesis/tfq_0435_challenge2_admitted_but_collapsed.md](../../../dag/derivations/02_genesis/tfq_0435_challenge2_admitted_but_collapsed.md)
- sha256 (`lf-normalised`): `1619a3f2cbe5799f140c41015f1114dfd8e42bbe206a09b4495a9f2a6dc3925a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0435
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-CHALLENGE2-ADMITTED-BUT-COLLAPSED` `DERIVED_LEAN`: [PG-GEN-SUPPLY-NO-OP](PG-GEN-SUPPLY-NO-OP.md) (PROVED_LEAN), [PGW-COLLAPSE-WITHOUT-INSTANCES](PGW-COLLAPSE-WITHOUT-INSTANCES.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-CHALLENGE3-CURRENT-REGIME-FAILS` `DERIVED_LEAN`: [PGW-CHALLENGE3-CURRENT-REGIME-FAILS](PGW-CHALLENGE3-CURRENT-REGIME-FAILS.md) (PROVED_LEAN)
