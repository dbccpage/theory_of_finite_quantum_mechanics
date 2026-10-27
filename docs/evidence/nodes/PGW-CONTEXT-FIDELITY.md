# PGW-CONTEXT-FIDELITY

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A trace that starts from a declared context s′ and takes steps valid relative to s′ need not be valid relative to the actual replayed state s ≠ s′: ValidTrace(τ | s′) does not imply ValidTrace(τ | s). Trial 2's Result 15 is the example, with internally consistent reasoning from the stale premise s′ = {\<\>} after Prompt 12 had designated \<a\> as current. A sound execution contract therefore accepts a context binding C(s′) only when s′ = Replay(H). The analysis calls this a clean theorem target and gives no proof. The Prompt 17 contrast fits it: a truncated window answered Verified and the full replay Retracted, each right for the history it received, which the appended analysis calls an information boundary rather than a reasoning failure.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 20
- distinct cited Lean declarations covered by a current replay receipt: 14
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The two-value carrier is not the sealed Genesis event grammar, and ValidTrace here is not the Rust certifies predicate. Trial 2 Result 15, Prompt 12, and the Prompt 17 window are not instantiated. A general trace semantics for arbitrary regimes stays open.

## Source status

v1 Derivation 5 (clean theorem target, no proof); 000_oepregen 03_results_and_arguments.md section 7 (statement 7)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/PregenesisContextFidelity.lean`

- file: [lean4/PregenesisContextFidelity.lean](../../../lean4/PregenesisContextFidelity.lean)
- sha256 (`bytes`): `1014a0c4622f95bfac19d876c5f31a22e13f26868d3763867d8a429a29d6afac`
- cited in: node.lean, receipt dag/research/campaign_pgw-context-fidelity_lean_replay.json (PregenesisContextFidelity), receipt dag/research/pr_344_review_replay.json (PregenesisContextFidelity), record TFQ-0427
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-fidelity_lean_replay.json](../../../dag/research/campaign_pgw-context-fidelity_lean_replay.json) (module `PregenesisContextFidelity`): recorded sha256 `1014a0c4622f95bfac19d876c5f31a22e13f26868d3763867d8a429a29d6afac` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_344_review_replay.json](../../../dag/research/pr_344_review_replay.json) (module `PregenesisContextFidelity`): recorded sha256 `1014a0c4622f95bfac19d876c5f31a22e13f26868d3763867d8a429a29d6afac` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build PregenesisContextFidelity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `PregenesisContextFidelity.acceptEqual_sound` | yes | yes | yes | none | `#print axioms PregenesisContextFidelity.acceptEqual_sound` |
| `PregenesisContextFidelity.answers_follow_received_history` | yes | yes | yes | propext | `#print axioms PregenesisContextFidelity.answers_follow_received_history` |
| `PregenesisContextFidelity.equal_implies_sound` | yes | yes | yes | none | `#print axioms PregenesisContextFidelity.equal_implies_sound` |
| `PregenesisContextFidelity.full_retracted` | yes | yes | yes | propext | `#print axioms PregenesisContextFidelity.full_retracted` |
| `PregenesisContextFidelity.history_count` | yes | yes | yes | none | `#print axioms PregenesisContextFidelity.history_count` |
| `PregenesisContextFidelity.replay_full` | yes | yes | yes | none | `#print axioms PregenesisContextFidelity.replay_full` |
| `PregenesisContextFidelity.replay_supply` | yes | yes | yes | none | `#print axioms PregenesisContextFidelity.replay_supply` |
| `PregenesisContextFidelity.separatingStep_invalid` | yes | yes | yes | propext | `#print axioms PregenesisContextFidelity.separatingStep_invalid` |
| `PregenesisContextFidelity.separatingStep_valid` | yes | yes | yes | propext | `#print axioms PregenesisContextFidelity.separatingStep_valid` |
| `PregenesisContextFidelity.sound_iff_only_replay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PregenesisContextFidelity.sound_iff_only_replay` |
| `PregenesisContextFidelity.sound_implies_equal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PregenesisContextFidelity.sound_implies_equal` |
| `PregenesisContextFidelity.stale_not_transferred` | yes | yes | yes | propext | `#print axioms PregenesisContextFidelity.stale_not_transferred` |
| `PregenesisContextFidelity.truncated_verified` | yes | yes | yes | propext | `#print axioms PregenesisContextFidelity.truncated_verified` |
| `PregenesisContextFidelity.unequal_pair_count` | yes | yes | yes | none | `#print axioms PregenesisContextFidelity.unequal_pair_count` |
| `answers_follow_received_history` | yes | yes | yes | propext | `#print axioms answers_follow_received_history` |
| `sound_iff_only_replay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms sound_iff_only_replay` |
| `stale_not_transferred` | yes | yes | yes | propext | `#print axioms stale_not_transferred` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/certification.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/certification.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/certification.rs)
- sha256 (`bytes`): `7f4c3644fa58c2ae38411c8258d17bdbe74bd8d992da18bf3110099c3ffa2aaf`
- cited in: node.rust, record TFQ-0427

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `certifies` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/model.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/model.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/model.py)
- sha256 (`bytes`): `6a7fd2ba9688d47e9291514c623a811cde3c6b9e8fda1d12a608dc9bb0b1f3c2`
- cited in: record TFQ-0427

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `certify` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/pgw-context-fidelity.py`

- file: [checks/independent/pgw-context-fidelity.py](../../../checks/independent/pgw-context-fidelity.py)
- sha256 (`bytes`): `9c56da423942d7e391c2559cf558f7d09d6723306dce7657f80ddd4c0e960009`
- cited in: record TFQ-0427

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0427_context_fidelity.md`

- file: [dag/derivations/01_pregenesis/tfq_0427_context_fidelity.md](../../../dag/derivations/01_pregenesis/tfq_0427_context_fidelity.md)
- sha256 (`lf-normalised`): `dc1892741490011c6eeddc11922d8e437a69a5c8f656fa2f6366bd6148cac2cb`
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

## Routes

Incoming (1):

- `PGW-R-CONTEXT-FIDELITY` `GAP_NO_DERIVATION`: [PGW-REPLAY-NECESSITY](PGW-REPLAY-NECESSITY.md) (PROVED_LEAN)

Outgoing (0):

