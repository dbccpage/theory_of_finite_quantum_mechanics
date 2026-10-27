# COMP-C6-TM0-OUTPUT-FORM-OPEN

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The tape of the halting TM0 configuration of M0 from initCfg0 should read the value of Code.eval c n; Mathlib gives this only existentially through TM2to1.tr_eval and is not composed here.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Still open: a natural number v lies in Code.eval c n exactly when M0 halts from initCfg0 with the encoded v on its output tape.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C6e claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ComputationC6Tm0OutputFormOpen.lean`

- file: [lean4/ComputationC6Tm0OutputFormOpen.lean](../../../lean4/ComputationC6Tm0OutputFormOpen.lean)
- sha256 (`bytes`): `df403415af32c9a579466ea33a6aa790896381efbbe521322eb020f74e0d3fc5`
- cited in: node.lean, receipt dag/research/campaign_comp-c6-tm0-output-form-open_lean_replay.json (ComputationC6Tm0OutputFormOpen), receipt dag/research/pr_368_review_replay.json (ComputationC6Tm0OutputFormOpen), record TFQ-1307
- replay: `verified`
  - receipt [dag/research/campaign_comp-c6-tm0-output-form-open_lean_replay.json](../../../dag/research/campaign_comp-c6-tm0-output-form-open_lean_replay.json) (module `ComputationC6Tm0OutputFormOpen`): recorded sha256 `df403415af32c9a579466ea33a6aa790896381efbbe521322eb020f74e0d3fc5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_368_review_replay.json](../../../dag/research/pr_368_review_replay.json) (module `ComputationC6Tm0OutputFormOpen`): recorded sha256 `df403415af32c9a579466ea33a6aa790896381efbbe521322eb020f74e0d3fc5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build ComputationC6Tm0OutputFormOpen`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `constAgrees` | yes | yes | yes | none | `#print axioms constAgrees` |
| `evalConstReturns` | yes | yes | yes | none | `#print axioms evalConstReturns` |
| `writeHaltFromBlank` | yes | yes | yes | none | `#print axioms writeHaltFromBlank` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1307_comp_c6_tm0_output_form_open.md`

- file: [dag/derivations/29_computation/tfq_1307_comp_c6_tm0_output_form_open.md](../../../dag/derivations/29_computation/tfq_1307_comp_c6_tm0_output_form_open.md)
- sha256 (`lf-normalised`): `f08ab0bb36ddeb4c956fdb67a44fb4f3b763b3c19fb62c7cc8dad8556a21a487`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1307
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C6-TM0-OUTPUT-FORM-OPEN` `GAP_NO_DERIVATION`: [COMP-C6-TM0-HALTING-EQUIVALENCE](COMP-C6-TM0-HALTING-EQUIVALENCE.md) (PROVED_LEAN)

Outgoing (0):

