# COMP-C8-BINARY-CODING

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For any finite alphabet, the letter-by-letter fixed-width binary code of width clog 2 |alphabet| + 1 is an injective monoid homomorphism on words with the explicit decoder decodeWord (decode_encode), and the same holds with the two separated marks as the target alphabet.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- cited Lean declaration references covered by a current replay receipt: 6
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A code is not an isomorphism of free monoids; no claim that a machine over the coded alphabet simulates a machine over the original (Mathlib TM1to1 is not used).

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C8a claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1312
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bits_injective` | yes | yes | yes | Quot.sound, propext | `#print axioms bits_injective` |
| `decodeMarks_encodeMarks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms decodeMarks_encodeMarks` |
| `decode_encode` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms decode_encode` |
| `encodeMarks_append` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms encodeMarks_append` |
| `encodeMarks_injective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms encodeMarks_injective` |
| `encodeWord_injective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms encodeWord_injective` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1312
- check: `cd code/rust && cargo test -p tfqm_wdp binary_coding_roundtrips_and_is_injective`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `binary_coding_roundtrips_and_is_injective` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp binary_coding_roundtrips_and_is_injective` |
| `code_width` (rust_symbol) | yes | yes | yes | - | - |
| `decode_binary` (rust_symbol) | yes | yes | yes | - | - |
| `encode_binary` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1312

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `code_width` (python_symbol) | yes | yes | yes | - | - |
| `decode_binary` (python_symbol) | yes | yes | yes | - | - |
| `encode_binary` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1312_comp_c8_binary_coding.md`

- file: [dag/derivations/29_computation/tfq_1312_comp_c8_binary_coding.md](../../../dag/derivations/29_computation/tfq_1312_comp_c8_binary_coding.md)
- sha256 (`lf-normalised`): `fe0f3adcc8c5c73758dbbcffc534e5e23b9f6e033f72fdb63cc6baea5868dc63`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1312
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C8-BINARY-CODING` `DERIVED_LEAN`: [COMP-C1-CANONICAL-SEPARATED-ALPHABET](COMP-C1-CANONICAL-SEPARATED-ALPHABET.md) (PROVED_LEAN), [PG-FREE-MONOID-NONISO](PG-FREE-MONOID-NONISO.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-COMP-C8-MINIMALITY-FENCE` `GAP_NO_DERIVATION`: [COMP-C8-MINIMALITY-FENCE](COMP-C8-MINIMALITY-FENCE.md) (OPEN)
