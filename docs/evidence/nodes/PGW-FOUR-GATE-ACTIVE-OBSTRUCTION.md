# PGW-FOUR-GATE-ACTIVE-OBSTRUCTION

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared here as the test a residual must pass before it counts as an active obstruction: obstP = retainedP ∧ protectedP ∧ declaredP ∧ zeroDeclP, that is, the pair is retained in the witness store, carries a protected demand, an observation is declared, and the declared observation does not separate the pair. In the sealed passage system this is an identity of Bool-valued functions at every state and pair (PrimitivePassage.obstP_factors), with sufficiency obst_of_gates and necessity gates_of_obst; the source calls the factorization near-definitional, gives the four-way reading content through the four gate_*_independent theorems, and refutes joint freedom of the gates (obs_gates_not_both_false). zeroDeclP answers true before any observation by a declared convention that never makes anything obstructed (obst_requires_observation). The education module MssnObstructionDetector restates the factorization over supplied observation columns.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Necessity is relative to this predicate, not to any notion of obstruction, and the decomposition is not claimed unique; the education archive's label apnf does not match the current nf.derivation.apnf.yaml, which is the apartness normal form.

## Source status

declared here; Derivation/PrimitivePassage.lean four gates (obstP_factors, obst_of_gates, gates_of_obst); education archive §6 normal-form table

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean](../../../lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean)
- sha256 (`bytes`): `f4447568db285df8fdf2d4362c579235072b4de42b4866d980e01ad2cb6ddbc4`
- cited in: node.lean, node.source, record TFQ-0493
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.PrimitivePassage`): recorded sha256 `f4447568db285df8fdf2d4362c579235072b4de42b4866d980e01ad2cb6ddbc4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gates_of_obst` | yes | yes | yes | Quot.sound, propext | `#print axioms gates_of_obst` |
| `obstP_factors` | yes | yes | yes | Quot.sound, propext | `#print axioms obstP_factors` |
| `obst_of_gates` | yes | yes | yes | Quot.sound, propext | `#print axioms obst_of_gates` |

- counts toward the grade: yes

### Lean: `lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean`

- file: [lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean](../../../lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean)
- sha256 (`bytes`): `4c4d0d2348ce89a0caa80aa4860c8fbcd3a038c8a4a2bbcc55a4e58bb609894a`
- cited in: node.lean, node.source, record TFQ-0493
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.MinimalSymbolSystems.MssnObstructionDetector`): recorded sha256 `4c4d0d2348ce89a0caa80aa4860c8fbcd3a038c8a4a2bbcc55a4e58bb609894a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `obstP_factors` | yes | yes | yes | Quot.sound, propext | `#print axioms obstP_factors` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/primitive_passage.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/primitive_passage.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/primitive_passage.py)
- sha256 (`bytes`): `ce263503fd67c4c3740db26796f42e3e011b67cf4a9d6383aa7093a2a1435531`
- cited in: record TFQ-0493

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `obst_p` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0493_four_gate_active_obstruction.md`

- file: [dag/derivations/02_genesis/tfq_0493_four_gate_active_obstruction.md](../../../dag/derivations/02_genesis/tfq_0493_four_gate_active_obstruction.md)
- sha256 (`lf-normalised`): `ffd51617382c812095439d19d52e4e8be9cb3a232edbbb105a95992bf2a3a72c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0493
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:0d098004a566c40656af6035d6e66ff13f7e873b11966677df080686a1b29cf9:1105-1107`

## Absences recorded by the TFQ records

- TFQ-0493 rust: no Rust port of the passage-system obstP; obstruction.rs::obstructed is the kernel's exhausted-menu notion, a different predicate

## Routes

Incoming (1):

- `PGW-R-FOUR-GATE-ACTIVE-OBSTRUCTION` `DERIVED_PROSE`: [PGW-CANDIDATE-EXTENSION-GENERATOR](PGW-CANDIDATE-EXTENSION-GENERATOR.md) (DEFINITION)

Outgoing (1):

- `PGW-R-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD` `DERIVED_LEAN`: [PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD](PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD.md) (PROVED_LEAN)
