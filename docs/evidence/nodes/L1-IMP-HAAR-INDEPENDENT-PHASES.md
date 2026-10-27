# L1-IMP-HAAR-INDEPENDENT-PHASES

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Phase averaging uses independent uniform (Haar) phases on each sector. The Rust implementation substitutes a declared finite phase group.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Haar probability measure on U(1)^n: assumption
- independence of phases: assumption

## Bottleneck

No measure-theoretic discharge; finite group stand-in only.

## Source status

Thm 5 hypotheses: independent Haar phases

## Review

- PFP review: [dag/results/L1-IMP-HAAR-INDEPENDENT-PHASES/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-IMP-HAAR-INDEPENDENT-PHASES/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Complete exact independent/correlated C4 intensity tables and averages, with general four-phase cancellation and correlated-gap identities in Lean.
  - does not support: Admit/construct Haar probability on U(1)^n and justify independence and continuum integration. C4 cancellation of this polynomial moment is not Haar construction.
  - next test: Admit/construct Haar probability on U(1)^n and justify independence and continuum integration. C4 cancellation of this polynomial moment is not Haar construction.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` |
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0301_haar_independent_phases_are_not_the_finite_average.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0301_haar_independent_phases_are_not_the_finite_average.md](../../../dag/derivations/08_l1_to_l2/tfq_0301_haar_independent_phases_are_not_the_finite_average.md)
- sha256 (`lf-normalised`): `95f2d96239c0edfe378442c1c671db920efb7c03475ecf3d985ef248f25a663c`
- generated view: listed, not counted
- cited in: record TFQ-0301
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:726fa8afa05803e040d092cf665b4a775fb5f3626f1631071aac9763510e15d5::phase_group_average`
- `external:sha256:8534bf2948b65ab72605a33c219105f09458247c00aa57acc8beb275df568d27:643`

## Absences recorded by the TFQ records

- TFQ-0301 rust: no local rust twin located for external:sha256:726fa8afa05803e040d092cf665b4a775fb5f3626f1631071aac9763510e15d5

## Routes

Incoming (1):

- `L1-R-HAAR-GAP` `GAP_NO_DERIVATION`: [L1-IMP-U1-PHASES](L1-IMP-U1-PHASES.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `L1-R-THM5` `COMPUTED`: [L1-QM020-THM5-PHASE-AVERAGED-SHADOW](L1-QM020-THM5-PHASE-AVERAGED-SHADOW.md) (COMPUTATIONALLY_CHECKED)
