# PGW-ENDOGENOUS-DEMAND-OB1

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No endogenous demand generator exists in the Alpha harness (AE-DEMAND-OPEN, OB-1, successor research S2): a demand is a target pair (i, j) with 0 ≤ i \< j \< n_data supplied by the host together with the measure and the declared bounds, nothing in the harness chooses a next demand, and the collapsed pairs left after an admission are returned as observations, not demands (leftover_as_demand refuses). The sealed derivation's pair-separation closure policy is declared metatheory, not a harness function, and the sealed result is that no object-language endogenous demand generator was derived.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 18
- distinct cited Lean declarations covered by a current replay receipt: 17
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A declared policy and object-language SEEK extension now computes fresh targets from source contexts and records source impose events. This is a narrowed extension, not a derivation of the policy from frozen observations or a refinement of Alpha search/licensing. Requests do not satisfy demands; unbounded continuation remains open.

## Source status

genesis_source.txt §9 continuation obligation; closeout.txt §2.1 and §4 S2; ALPHA_HANDOFF §4 demand policy

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisDemandPolicy.lean`

- file: [lean4/GenesisDemandPolicy.lean](../../../lean4/GenesisDemandPolicy.lean)
- sha256 (`bytes`): `9c62ca49ae596150d8b615697097cf2d579ae172ac3f342063dc8ae63d82f603`
- cited in: node.lean, receipt dag/research/campaign_pgw-endogenous-demand-ob1_lean_replay.json (GenesisDemandPolicy), receipt dag/research/genesis_merged_20261023_lean_replay.json (GenesisDemandPolicy), record TFQ-0504
- replay: `verified`
  - receipt [dag/research/campaign_pgw-endogenous-demand-ob1_lean_replay.json](../../../dag/research/campaign_pgw-endogenous-demand-ob1_lean_replay.json) (module `GenesisDemandPolicy`): recorded sha256 `9c62ca49ae596150d8b615697097cf2d579ae172ac3f342063dc8ae63d82f603` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/genesis_merged_20261023_lean_replay.json](../../../dag/research/genesis_merged_20261023_lean_replay.json) (module `GenesisDemandPolicy`): recorded sha256 `9c62ca49ae596150d8b615697097cf2d579ae172ac3f342063dc8ae63d82f603` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisDemandPolicy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GenesisDemandPolicy.collapseTest_correct` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisDemandPolicy.collapseTest_correct` |
| `GenesisDemandPolicy.fixed_data_saturates` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisDemandPolicy.fixed_data_saturates` |
| `GenesisDemandPolicy.instruction_records_demand` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisDemandPolicy.instruction_records_demand` |
| `GenesisDemandPolicy.mem_agenda` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisDemandPolicy.mem_agenda` |
| `GenesisDemandPolicy.mem_candidates` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisDemandPolicy.mem_candidates` |
| `GenesisDemandPolicy.mem_contexts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisDemandPolicy.mem_contexts` |
| `GenesisDemandPolicy.mem_options` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisDemandPolicy.mem_options` |
| `GenesisDemandPolicy.mem_tuples` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisDemandPolicy.mem_tuples` |
| `GenesisDemandPolicy.next_none_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisDemandPolicy.next_none_iff` |
| `GenesisDemandPolicy.next_sound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisDemandPolicy.next_sound` |
| `GenesisDemandPolicy.no_host_target_in_program` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisDemandPolicy.no_host_target_in_program` |
| `GenesisDemandPolicy.no_immediate_repeat` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisDemandPolicy.no_immediate_repeat` |
| `GenesisDemandPolicy.policy_is_not_forced` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisDemandPolicy.policy_is_not_forced` |
| `GenesisDemandPolicy.seek_grows_one` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisDemandPolicy.seek_grows_one` |
| `GenesisDemandPolicy.seek_is_recorded_source_step` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisDemandPolicy.seek_is_recorded_source_step` |
| `GenesisDemandPolicy.seek_preserves_observations` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisDemandPolicy.seek_preserves_observations` |
| `GenesisDemandPolicy.seek_preserves_policy` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisDemandPolicy.seek_preserves_policy` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs)
- sha256 (`bytes`): `79461000d78d732752daca76f68288e27be855dc36605c2de578e0478e1798d1`
- cited in: node.rust, record TFQ-0504

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Outside` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/pgw-endogenous-demand-ob1.py`

- file: [checks/independent/pgw-endogenous-demand-ob1.py](../../../checks/independent/pgw-endogenous-demand-ob1.py)
- sha256 (`bytes`): `5e7e78bc5a5cc333a82d61b0accf13134504983190c0d07fe50bce1792616d57`
- cited in: record TFQ-0504
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt)
- sha256 (`lf-normalised`): `c613e357809438876d1fcec34ea896548f17f4e9d4ea7f21048fafe9451651ac`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0504_endogenous_demand_ob1.md`

- file: [dag/derivations/02_genesis/tfq_0504_endogenous_demand_ob1.md](../../../dag/derivations/02_genesis/tfq_0504_endogenous_demand_ob1.md)
- sha256 (`lf-normalised`): `2c5f3208be1b7f22459a041382207742503c59e33c55be8697783adf19420244`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0504
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-endogenous-demand-ob1.md`

- file: [dag/derivations/independent/pgw-endogenous-demand-ob1.md](../../../dag/derivations/independent/pgw-endogenous-demand-ob1.md)
- sha256 (`lf-normalised`): `ffa9f6f8ff1b5b6ac0dcdbb04786ac7fccc6effb28090f963557e9fd11fe3d9d`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/docs/ALPHA_HANDOFF.md:78-88`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/harness.py::leftover_as_demand`

## Absences recorded by the TFQ records

- TFQ-0504 lean4: no Lean demand generator for the harness; Generator.generation_never_dries concerns the reflective composite (TFQ-0487)

## Routes

Incoming (1):

- `PGW-R-ENDOGENOUS-DEMAND-OB1` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION), [PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS](PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-COMP-C4-UNBOUNDED-SUPPLY-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-C4-UNBOUNDED-SUPPLY-IMPORT](COMP-C4-UNBOUNDED-SUPPLY-IMPORT.md) (IMPORTED_ASSUMPTION)
