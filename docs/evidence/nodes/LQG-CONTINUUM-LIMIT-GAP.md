# LQG-CONTINUUM-LIMIT-GAP

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No source read for this change derives a continuum limit, a semiclassical limit or a physical cosmological constant from the finite recoupling tables of the repository, or from the exact finite targets of this stage. The fences of TFQ-0104 and TFQ-0105 say so; this node records the gap so that the exact 6j, area and pentagon checks are not read as steps toward a limit.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The census and the two dimension identities do not discharge a continuum limit, a semiclassical limit, or a physical cosmological constant. No sequence of triangulations and no Einstein equation is constructed. Routes FRO-R-LQG-CONTINUUM-LIMIT-GAP and FRO-R-BACK-LQG-LIMIT-TO-TFQ0105 stay GAP_NO_DERIVATION. The broader audit sentence, that no source read for this change derives a limit, is not discharged in full.

## Source status

Finite census and Q(sqrt 2) dimension identities checked in Lean 4.35.0 on 2026-10-24. Node stays OPEN. No continuum limit, semiclassical limit, or physical cosmological constant is derived. Earlier audit against arXiv:1205.2019 Part V and TFQ-0104/TFQ-0105 was on 2026-10-22.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignLqgContinuumLimitGap.lean`

- file: [lean4/CampaignLqgContinuumLimitGap.lean](../../../lean4/CampaignLqgContinuumLimitGap.lean)
- sha256 (`bytes`): `a6adec8e3fe5ad9453a5a7ae74767860bd6794957da7dc9393242516b3d49d3d`
- cited in: node.lean, node.source, receipt dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json (CampaignLqgContinuumLimitGap)
- replay: `verified`
  - receipt [dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json](../../../dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json) (module `CampaignLqgContinuumLimitGap`): recorded sha256 `a6adec8e3fe5ad9453a5a7ae74767860bd6794957da7dc9393242516b3d49d3d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignLqgContinuumLimitGap`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignLqgContinuumLimitGap.level2_admissible_count` | yes | yes | yes | none | `#print axioms CampaignLqgContinuumLimitGap.level2_admissible_count` |
| `CampaignLqgContinuumLimitGap.level2_counts_do_not_select_a_scale` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgContinuumLimitGap.level2_counts_do_not_select_a_scale` |
| `CampaignLqgContinuumLimitGap.level2_dimension_truncation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgContinuumLimitGap.level2_dimension_truncation` |
| `CampaignLqgContinuumLimitGap.level2_free_positive_scale` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgContinuumLimitGap.level2_free_positive_scale` |
| `CampaignLqgContinuumLimitGap.level2_tuple_census` | yes | yes | yes | none | `#print axioms CampaignLqgContinuumLimitGap.level2_tuple_census` |

- counts toward the grade: yes

### Rust: `code/rust/src/general_relativity/spin_foam.rs`

- file: [code/rust/src/general_relativity/spin_foam.rs](../../../code/rust/src/general_relativity/spin_foam.rs)
- sha256 (`bytes`): `8ab22473e5ebc36ab2cb23247e2d6835664bab9ac0e9f0f26b6ab9b4fd63892e`
- cited in: node.source
- note: no test is cited for this symbol; its crate is tfqm_general_relativity
- counts toward the grade: yes

### Python: `checks/independent/lqg-continuum-limit-gap.py`

- file: [checks/independent/lqg-continuum-limit-gap.py](../../../checks/independent/lqg-continuum-limit-gap.py)
- sha256 (`bytes`): `7a81f17c2b4c021a84348b6eaa13951a111920f338fb3ffabcdf962f5433f52a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2315_lqg_continuum_limit_gap.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2315_lqg_continuum_limit_gap.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2315_lqg_continuum_limit_gap.md)
- sha256 (`lf-normalised`): `8d5c94eeb400b130c53d529eb2a71ef51d57115d02fd83ebebc081ea9ec819ab`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2315
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/lqg-continuum-limit-gap.md`

- file: [dag/derivations/independent/lqg-continuum-limit-gap.md](../../../dag/derivations/independent/lqg-continuum-limit-gap.md)
- sha256 (`lf-normalised`): `838971aee13396e955879ac3c0820840c4546365d5da622375f7193dc2a9ca16`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json`

- file: [dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json](../../../dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json)
- sha256 (`lf-normalised`): `1b9cfaf12cd195764cd17567b71c47010ae2ba2273cd361c9323c8326eb86239`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-LQG-CONTINUUM-LIMIT-GAP` `GAP_NO_DERIVATION`: [LQG-EPRL-VERTEX-IMPORT](LQG-EPRL-VERTEX-IMPORT.md) (IMPORTED_ASSUMPTION), [LQG-TV-LEVEL2-PENTAGON-TARGET](LQG-TV-LEVEL2-PENTAGON-TARGET.md) (PROVED_LEAN)

Outgoing (1):

- `FRO-R-BACK-LQG-LIMIT-TO-TFQ0105` `GAP_NO_DERIVATION`: [TFQ-0105](TFQ-0105.md) (SOURCE_RECORD)
