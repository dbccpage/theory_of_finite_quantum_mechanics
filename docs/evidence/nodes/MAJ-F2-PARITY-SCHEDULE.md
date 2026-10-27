# MAJ-F2-PARITY-SCHEDULE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A parity schedule is a declared finite cochain complex C0 -d0-\> C1 -d1-\> C2 over F2 given by binary incidence matrices with d1 d0 = 0 mod 2; C0 holds vertex gauge flips, C1 edge parity residuals, C2 plaquette syndromes.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- declared incidence matrices d0, d1 over F2

## Bottleneck

The complex and its incidence matrices are declared inputs; nothing here derives them from a device or from the trunk window.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-DEF-PARITY-SCHEDULE claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1138
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `F2CochainComplex` | yes | yes | yes | none | `#print axioms F2CochainComplex` |
| `F2Map` | yes | yes | yes | none | `#print axioms F2Map` |
| `F2Vec.add` | yes | yes | yes | none | `#print axioms F2Vec.add` |

- counts toward the grade: yes

### Rust: `code/rust/src/majorana/complexes.rs`

- file: [code/rust/src/majorana/complexes.rs](../../../code/rust/src/majorana/complexes.rs)
- sha256 (`bytes`): `185042ba131c005d8519b65159791a78f6a64df90e7976a54c0845f6de489646`
- cited in: node.rust, record TFQ-1138

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ChainComplexGf2` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/majorana/majorana_f2_trichotomy.py`

- file: [code/python/src/majorana/majorana_f2_trichotomy.py](../../../code/python/src/majorana/majorana_f2_trichotomy.py)
- sha256 (`bytes`): `d6ffe11ba0e9fd0ba5a4a467147b95cf560b3d4c860b845a025e3b0e5e283b7a`
- cited in: record TFQ-1138

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `F2CochainComplex` (python_symbol) | yes | yes | yes | - | - |
| `GF2Matrix` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1138_maj_f2_parity_schedule.md`

- file: [dag/derivations/28_majorana/tfq_1138_maj_f2_parity_schedule.md](../../../dag/derivations/28_majorana/tfq_1138_maj_f2_parity_schedule.md)
- sha256 (`lf-normalised`): `9be58028ba5178368e6647757f7de604d15c9b436bfbeca3ce379e9537dece39`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1138
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-F2-PARITY-SCHEDULE` `DERIVED_PROSE`: [DS-QM212-MAJORANA-PROBLEM](DS-QM212-MAJORANA-PROBLEM.md) (PROVED_LEAN), [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION), [L1-CHAIN-D1D0-AXIOM](L1-CHAIN-D1D0-AXIOM.md) (ADMITTED_PRIMITIVE)

Outgoing (6):

- `APP-R-MAJ-NILPOTENCY-REFUSAL` `DERIVED_PROSE`: [MAJ-NILPOTENCY-REFUSAL](MAJ-NILPOTENCY-REFUSAL.md) (DEFINITION)
- `APP-R-MAJ-PHI1-HAMMING-COSET` `DERIVED_PROSE`: [MAJ-PHI1-HAMMING-COSET](MAJ-PHI1-HAMMING-COSET.md) (DEFINITION)
- `APP-R-MAJ-REALIZATION-PACKET-GAP` `DERIVED_PROSE`: [MAJ-REALIZATION-PACKET-GAP](MAJ-REALIZATION-PACKET-GAP.md) (DEFINITION)
- `APP-R-MAJ-SURFACE-SHADOW-FENCE` `DERIVED_PROSE`: [MAJ-SURFACE-SHADOW-FENCE](MAJ-SURFACE-SHADOW-FENCE.md) (DEFINITION)
- `APP-R-MAJ-TETRON-ARRAY-CARRIER` `DERIVED_PROSE`: [MAJ-TETRON-ARRAY-CARRIER](MAJ-TETRON-ARRAY-CARRIER.md) (DEFINITION)
- `APP-R-MAJ-TRICHOTOMY-LABELS` `DERIVED_PROSE`: [MAJ-TRICHOTOMY-LABELS](MAJ-TRICHOTOMY-LABELS.md) (DEFINITION)
