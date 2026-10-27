# PGW-MINIMAL-OR-INITIAL-REFUSED

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_PROSE`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Question 10 asks whether the final process is minimal or initial among a defined class of finite processes satisfying the same challenges. The sealed answer is that the claim is refused and tagged unresolved: no such initiality or minimality property was established. What is established is narrower: determinism of the artifacts across the exercised runs and platforms is a finite computation (byte-identical artifacts are repeated-run agreement, not an engine theorem), completeness of enumerations within declared bounds is a bounded theorem under its ledger conditions, and the per-stage minimality and uniqueness results are theorems with their stated scopes. An earlier wording, what is proved: determinism of the engine, was corrected on 2026-09-08.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- distinct cited Lean declarations covered by a current replay receipt: 16
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

An explicit clock-closed observed-process class now has a proved initiality obstruction, including the actual source-regime supply self-loop, and a reachable/reduced finite-model minimum-state criterion. These supplementary results do not certify the full Alpha engine, its class membership, or minimum program/declaration cost; the historical refusal remains accurate.

## Source status

genesis_source.txt question 10 claim refused \[unresolved\]; written refusal with scoped alternatives

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisProcessComparison.lean`

- file: [lean4/GenesisProcessComparison.lean](../../../lean4/GenesisProcessComparison.lean)
- sha256 (`bytes`): `ca09cff33f2c586039c2a25c839fe93f32e9f1b68de4e4ef23076ea050288b96`
- cited in: node.lean, receipt dag/research/campaign_pgw-minimal-or-initial-refused_lean_replay.json (GenesisProcessComparison), receipt dag/research/genesis_merged_20261023_lean_replay.json (GenesisProcessComparison), record TFQ-0453
- replay: `verified`
  - receipt [dag/research/campaign_pgw-minimal-or-initial-refused_lean_replay.json](../../../dag/research/campaign_pgw-minimal-or-initial-refused_lean_replay.json) (module `GenesisProcessComparison`): recorded sha256 `ca09cff33f2c586039c2a25c839fe93f32e9f1b68de4e4ef23076ea050288b96` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/genesis_merged_20261023_lean_replay.json](../../../dag/research/genesis_merged_20261023_lean_replay.json) (module `GenesisProcessComparison`): recorded sha256 `ca09cff33f2c586039c2a25c839fe93f32e9f1b68de4e4ef23076ea050288b96` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisProcessComparison`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GenesisProcessComparison.all_words_agree` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisProcessComparison.all_words_agree` |
| `GenesisProcessComparison.all_words_minimum_size` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisProcessComparison.all_words_minimum_size` |
| `GenesisProcessComparison.every_challenge_answer_agrees` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisProcessComparison.every_challenge_answer_agrees` |
| `GenesisProcessComparison.hom_run` | yes | yes | yes | propext | `#print axioms GenesisProcessComparison.hom_run` |
| `GenesisProcessComparison.labelled_append` | yes | yes | yes | none | `#print axioms GenesisProcessComparison.labelled_append` |
| `GenesisProcessComparison.no_clock_hom_of_self_loop` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisProcessComparison.no_clock_hom_of_self_loop` |
| `GenesisProcessComparison.no_initial_in_clock_closed_class` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisProcessComparison.no_initial_in_clock_closed_class` |
| `GenesisProcessComparison.no_map_to_clock_lift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisProcessComparison.no_map_to_clock_lift` |
| `GenesisProcessComparison.no_source_initial_in_clock_closed_class` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisProcessComparison.no_source_initial_in_clock_closed_class` |
| `GenesisProcessComparison.nonminimal_adequate_process` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisProcessComparison.nonminimal_adequate_process` |
| `GenesisProcessComparison.oneState_is_reduced_reachable` | yes | yes | yes | none | `#print axioms GenesisProcessComparison.oneState_is_reduced_reachable` |
| `GenesisProcessComparison.reduced_reachable_is_minimal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisProcessComparison.reduced_reachable_is_minimal` |
| `GenesisProcessComparison.run_add` | yes | yes | yes | none | `#print axioms GenesisProcessComparison.run_add` |
| `GenesisProcessComparison.source_advance_matches` | yes | yes | yes | propext | `#print axioms GenesisProcessComparison.source_advance_matches` |
| `GenesisProcessComparison.source_run_matches` | yes | yes | yes | propext | `#print axioms GenesisProcessComparison.source_run_matches` |
| `GenesisProcessComparison.source_supply_self_loop` | yes | yes | yes | propext | `#print axioms GenesisProcessComparison.source_supply_self_loop` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Initiality.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Initiality.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Initiality.lean)
- sha256 (`bytes`): `cd20947d80573e7fc077b0bc455f53af63684c52ff4ed4f14893d845d9e51e1f`
- cited in: node.source
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Initiality.lean`
- counts toward the grade: yes

### Python: `checks/independent/pgw-minimal-or-initial-refused.py`

- file: [checks/independent/pgw-minimal-or-initial-refused.py](../../../checks/independent/pgw-minimal-or-initial-refused.py)
- sha256 (`bytes`): `67fa864d43432040bd7af3a1e02077c4c8757cae77db55851d2660d449be046c`
- cited in: record TFQ-0453
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0453_minimal_or_initial_refused.md`

- file: [dag/derivations/02_genesis/tfq_0453_minimal_or_initial_refused.md](../../../dag/derivations/02_genesis/tfq_0453_minimal_or_initial_refused.md)
- sha256 (`lf-normalised`): `bb5e13eeeedc75ca3f7eee378fbb5622c4c56c66898cff332099fd16b665eec4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0453
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-minimal-or-initial-refused.md`

- file: [dag/derivations/independent/pgw-minimal-or-initial-refused.md](../../../dag/derivations/independent/pgw-minimal-or-initial-refused.md)
- sha256 (`lf-normalised`): `a3de462e1958dc96ae0cf6e7c93caf7e1b162842bdd7142c52178499dfc41dd6`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0453 lean4: no Lean statement of minimality or initiality among finite processes satisfying the sealed challenges
- TFQ-0453 python: no Python check; artifact determinism is repeated-run byte agreement, not a program
- TFQ-0453 rust: no Rust check; artifact determinism is repeated-run byte agreement, not a program

## Routes

Incoming (1):

- `PGW-R-MINIMAL-OR-INITIAL-REFUSED` `DERIVED_PROSE`: [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) (PROVED_PROSE)

Outgoing (1):

- `PGW-R-SEALED-TERMINAL-STATEMENT` `DERIVED_PROSE`: [PGW-SEALED-TERMINAL-STATEMENT](PGW-SEALED-TERMINAL-STATEMENT.md) (PROVED_PROSE)
