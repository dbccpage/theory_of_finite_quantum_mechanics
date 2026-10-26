# QCV-CONDITIONAL-VIABILITY-CERTIFICATE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If the initial backlog q0 is nonnegative, g \< 1, kappa \> 0, r is at least lam/((1-g)*kappa), c(k) \<= C for every natural number k, p(k) \>= 0, max(C,1)*p(0) \< 1, and p(k+1) \<= c(k)*p(k)^2 whenever BacklogBounded lam g (kappa*r) q0 holds, then that backlog predicate holds and for every rational L \>= 0 and every epsilon \> 0 some level k has L*p(k) \<= epsilon. If also max(C,1)*p(0) \<= 1/2, then every natural number k with L \<= epsilon*max(C,1)*2^(2^k) has L*p(k) \<= epsilon.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- distinct cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- noise obeys p(k+1) \<= c(k)*p(k)^2 when repair keeps up (independent or local noise)
- fresh ancillas at rate r
- classical control and decoding fast enough for the syndrome
- level-bounded overhead c(k) \<= C

## Bottleneck

The initial backlog q0 is nonnegative. The recurrence, the supply bound, and the overhead bound are hypotheses of the implication. A device, a noise process, and a classical decoder are outside this implication. A negative initial backlog is outside the checked slice.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-Q5 claims CONDITIONAL; audited status CONDITIONAL

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignQcvConditionalViabilityCertificate.lean`

- file: [lean4/CampaignQcvConditionalViabilityCertificate.lean](../../../lean4/CampaignQcvConditionalViabilityCertificate.lean)
- sha256 (`bytes`): `06c68a7ea5e207d83a2211bb0c7960efb974cffc68ec30ea3c94042d8e903b0e`
- cited in: node.lean, node.source, receipt dag/research/campaign_qcv-conditional-viability-certificate_lean_replay.json (CampaignQcvConditionalViabilityCertificate), receipt dag/research/pr_385_round2_replay.json (CampaignQcvConditionalViabilityCertificate), record TFQ-1324
- replay: `verified`
  - receipt [dag/research/campaign_qcv-conditional-viability-certificate_lean_replay.json](../../../dag/research/campaign_qcv-conditional-viability-certificate_lean_replay.json) (module `CampaignQcvConditionalViabilityCertificate`): recorded sha256 `06c68a7ea5e207d83a2211bb0c7960efb974cffc68ec30ea3c94042d8e903b0e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_385_round2_replay.json](../../../dag/research/pr_385_round2_replay.json) (module `CampaignQcvConditionalViabilityCertificate`): recorded sha256 `06c68a7ea5e207d83a2211bb0c7960efb974cffc68ec30ea3c94042d8e903b0e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignQcvConditionalViabilityCertificate`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignQcvConditionalViabilityCertificate.viability_explicit_level` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignQcvConditionalViabilityCertificate.viability_explicit_level` |
| `CampaignQcvConditionalViabilityCertificate.viability_nonneg_initial` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignQcvConditionalViabilityCertificate.viability_nonneg_initial` |

- counts toward the grade: yes

### Lean: `lean4/QcSelfObstruction.lean`

- file: [lean4/QcSelfObstruction.lean](../../../lean4/QcSelfObstruction.lean)
- sha256 (`bytes`): `be7f59c979614e015b49da0d9b4e233e5166f39b91a0c6de61d3e51659209a83`
- cited in: node.lean, record TFQ-1324
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `QcSelfObstruction`): recorded sha256 `be7f59c979614e015b49da0d9b4e233e5166f39b91a0c6de61d3e51659209a83` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build QcSelfObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `conditional_viability` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms conditional_viability` |
| `conditional_viability_explicit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms conditional_viability_explicit` |
| `conditional_viability_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms conditional_viability_instance` |
| `explicit_level` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms explicit_level` |
| `level_error_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms level_error_le` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs`

- file: [code/rust/src/qm/campaigns/qc_self_obstruction.rs](../../../code/rust/src/qm/campaigns/qc_self_obstruction.rs)
- sha256 (`bytes`): `7ec8808a14754317eca2df6528a90985a6cbbaaddbf17c611cd236cd45eef4e3`
- cited in: node.rust, record TFQ-1324

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `level_for_failure` (rust_symbol) | yes | yes | yes | - | - |
| `viability_report` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/qc_self_obstruction.py`

- file: [code/python/src/qm/qc_self_obstruction.py](../../../code/python/src/qm/qc_self_obstruction.py)
- sha256 (`bytes`): `bfc41c6def8f655c61bde3475189a299d276bae04e1f8c75f09f1d35a6d89d66`
- cited in: record TFQ-1324

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `level_for_failure` (python_symbol) | yes | yes | yes | - | - |
| `viability_report` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1324_qcv_conditional_viability_certificate.md`

- file: [dag/derivations/29_computation/tfq_1324_qcv_conditional_viability_certificate.md](../../../dag/derivations/29_computation/tfq_1324_qcv_conditional_viability_certificate.md)
- sha256 (`lf-normalised`): `5c83b6b28624433002b23704ee04152fdc087c6eec8b5890a3f5c5c7be436959`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1324
- counts toward the grade: no

### Documents and data: `dag/research/quantum_computation_self_obstruction.md`

- file: [dag/research/quantum_computation_self_obstruction.md](../../../dag/research/quantum_computation_self_obstruction.md)
- sha256 (`lf-normalised`): `8ae1b2ae291ee74f773da07740ebd0c1f98842bc01d7ec6a4d3c267e0077d178`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/quantum_computation_self_obstruction_axioms.txt`

- file: [dag/research/quantum_computation_self_obstruction_axioms.txt](../../../dag/research/quantum_computation_self_obstruction_axioms.txt)
- sha256 (`lf-normalised`): `b4c803ee2b1a4fe8af1d9d92a351fb11c61d2791bea01a5b7cd3dd7c1623af81`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-QCV-CONDITIONAL-VIABILITY-CERTIFICATE` `CONDITIONAL_ON_IMPORT`: [QCV-OVERHEAD-GROWTH-CRITERION](QCV-OVERHEAD-GROWTH-CRITERION.md) (PROVED_LEAN), [QCV-NET-RATE-BACKLOG-DICHOTOMY](QCV-NET-RATE-BACKLOG-DICHOTOMY.md) (PROVED_LEAN), [QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY](QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-QCV-PHYSICAL-SATISFIABILITY-OPEN` `GAP_NO_DERIVATION`: [QCV-PHYSICAL-SATISFIABILITY-OPEN](QCV-PHYSICAL-SATISFIABILITY-OPEN.md) (OPEN)
- `APP-R-QCV-VIABILITY-NEEDS-ALL-REQUIREMENTS` `DERIVED_LEAN`: [QCV-VIABILITY-NEEDS-ALL-REQUIREMENTS](QCV-VIABILITY-NEEDS-ALL-REQUIREMENTS.md) (PROVED_LEAN)
