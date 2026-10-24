# FSP-EFFICIENT-SAMPLING-OBLIGATIONS

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Canonical sign representatives, finite cancellation and nonnegative determinant weights do not establish an efficient sampler or a general fermion sign-problem solution.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Define input size, transformation cost, estimator variance, normalization and mixing or sampling bounds for the chosen model family. Narrowed in lean4/CampaignFspEfficientSamplingObligations.lean and checks/independent/fsp-efficient-sampling-obligations.py while keeping status OPEN to: (1) exponential Fock/SQL orbit scaling 4^L \> L^3 for L \>= 3 and half-filled configuration vertex growth comb(2m, m) vs polynomial per-step DQMC rank-1 update (c * Ns^2) and stabilization (c * Ns^3) costs; (2) exact meron zero-sum pair cancellation (+w_m, -w_m) preserving Z = w1 + w2 while reducing Z_abs and raising \<Sign\> to 1; (3) RREF pivot-zero canonical section non-optimality in L1 norm (||N(c)||_1 = 2 \> ||c - d0||_1 = 1 for d0 = (1,1,1), c = (0,1,1) in BQNFSignEvaluator); and (4) explicit scope fences showing that strictly positive weights (p, 1-p) do not bound observable variance 1/p - 1 or bimodal barrier mixing lower bounds W_well / (2b), and separating exact finite identities and protected sign-free weights from polynomial-time sampling and unrestricted FSP solutions.

## Source status

Source record or explicit branch obligation; status scoped to the statement.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspEfficientSamplingObligations.lean`

- file: [lean4/CampaignFspEfficientSamplingObligations.lean](../../../lean4/CampaignFspEfficientSamplingObligations.lean)
- sha256 (`bytes`): `99790e3733deca7cd2a5fb4f5d519518949ea7f57ff5b67c1a3ed3835bc4cff8`
- cited in: node.lean, receipt dag/research/campaign_fsp-efficient-sampling-obligations_lean_replay.json (CampaignFspEfficientSamplingObligations), record TFQ-0409
- replay: `verified`
  - receipt [dag/research/campaign_fsp-efficient-sampling-obligations_lean_replay.json](../../../dag/research/campaign_fsp-efficient-sampling-obligations_lean_replay.json) (module `CampaignFspEfficientSamplingObligations`): recorded sha256 `99790e3733deca7cd2a5fb4f5d519518949ea7f57ff5b67c1a3ed3835bc4cff8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspEfficientSamplingObligations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspEfficientSamplingObligations.bimodal_energy_barrier_conductance_bottleneck_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspEfficientSamplingObligations.bimodal_energy_barrier_conductance_bottleneck_fence` |
| `CampaignFspEfficientSamplingObligations.bipartite_hubbard_protection_broken_by_doping_or_frustration_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspEfficientSamplingObligations.bipartite_hubbard_protection_broken_by_doping_or_frustration_fence` |
| `CampaignFspEfficientSamplingObligations.determinant_weight_evaluation_and_update_cost_accounting` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspEfficientSamplingObligations.determinant_weight_evaluation_and_update_cost_accounting` |
| `CampaignFspEfficientSamplingObligations.exponential_configuration_graph_sign_switching_cost_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspEfficientSamplingObligations.exponential_configuration_graph_sign_switching_cost_fence` |
| `CampaignFspEfficientSamplingObligations.four_tier_fsp_epistemic_separation_obligations` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspEfficientSamplingObligations.four_tier_fsp_epistemic_separation_obligations` |
| `CampaignFspEfficientSamplingObligations.meron_orbit_cancellation_preserves_partition_and_observable` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspEfficientSamplingObligations.meron_orbit_cancellation_preserves_partition_and_observable` |
| `CampaignFspEfficientSamplingObligations.nonnegative_weights_do_not_bound_observable_variance_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspEfficientSamplingObligations.nonnegative_weights_do_not_bound_observable_variance_fence` |
| `CampaignFspEfficientSamplingObligations.rref_canonical_section_not_l1_minimizer_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspEfficientSamplingObligations.rref_canonical_section_not_l1_minimizer_witness` |
| `CampaignFspEfficientSamplingObligations.sign_reweighted_sample_complexity_amplification` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspEfficientSamplingObligations.sign_reweighted_sample_complexity_amplification` |
| `CampaignFspEfficientSamplingObligations.sql_exhaustive_orbit_size_exponential_vs_polynomial` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspEfficientSamplingObligations.sql_exhaustive_orbit_size_exponential_vs_polynomial` |
- counts toward the grade: yes

### Python: `checks/independent/fsp-efficient-sampling-obligations.py`

- file: [checks/independent/fsp-efficient-sampling-obligations.py](../../../checks/independent/fsp-efficient-sampling-obligations.py)
- sha256 (`bytes`): `06d14cdbc57eb4e26ab56670ed0fcb4a2340df05d7db14710fc6e6107a38bee5`
- cited in: record TFQ-0409

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/fsp/bqnf_sign_evaluator.py`

- file: [code/python/src/fsp/bqnf_sign_evaluator.py](../../../code/python/src/fsp/bqnf_sign_evaluator.py)
- sha256 (`bytes`): `6bbc7a71841797e537bf4f62308124325c6f39848c08ee914dfb96187f892f92`
- cited in: record TFQ-0409

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BQNFSignEvaluator` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_0409_fsp_efficient_sampling_obligations.md`

- file: [dag/derivations/26_fsp/tfq_0409_fsp_efficient_sampling_obligations.md](../../../dag/derivations/26_fsp/tfq_0409_fsp_efficient_sampling_obligations.md)
- sha256 (`lf-normalised`): `0c0469d21bc933ec31e7b2aa5834aaccb5d653b4ae5bf46ff51fcd641bd9ea58`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0409
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-efficient-sampling-obligations.md`

- file: [dag/derivations/independent/fsp-efficient-sampling-obligations.md](../../../dag/derivations/independent/fsp-efficient-sampling-obligations.md)
- sha256 (`lf-normalised`): `a9089f326fdd99af87f61fde017de465cedb5b017f6b35f2a3db803d12f9016a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-efficient-sampling-obligations_independent.json`

- file: [dag/research/campaign_fsp-efficient-sampling-obligations_independent.json](../../../dag/research/campaign_fsp-efficient-sampling-obligations_independent.json)
- sha256 (`lf-normalised`): `585691b46591b69c39eef4e9fee880d60fa01b0bab04ff5448767321e73f0b1d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-efficient-sampling-obligations_lean_mutation.json`

- file: [dag/research/campaign_fsp-efficient-sampling-obligations_lean_mutation.json](../../../dag/research/campaign_fsp-efficient-sampling-obligations_lean_mutation.json)
- sha256 (`lf-normalised`): `aafd8302f97e67b2a069bf67293cb8d26b3c2aeccea7dc44cad0bebb7640b7ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-efficient-sampling-obligations_lean_replay.json`

- file: [dag/research/campaign_fsp-efficient-sampling-obligations_lean_replay.json](../../../dag/research/campaign_fsp-efficient-sampling-obligations_lean_replay.json)
- sha256 (`lf-normalised`): `d18b050799c32ff8cc7cb12b652003fe39d9d3fb399d0a0fc3329dc8b2baed22`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/README.md`

- file: [papers/core/fsp/README.md](../../../papers/core/fsp/README.md)
- sha256 (`lf-normalised`): `49bf9e23ec5b96cfd3fbd8bfff74f2a03d0151e20c497589d4233136dc24ca5b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-EFFICIENT-SAMPLING-OBLIGATIONS` `GAP_NO_DERIVATION`: [FSP-HUBBARD-PROTECTED-REPRESENTATIONS](FSP-HUBBARD-PROTECTED-REPRESENTATIONS.md) (CONDITIONAL), [FSP-MERON-CHARACTER-CANCELLATION](FSP-MERON-CHARACTER-CANCELLATION.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MAJ-GIN-INVOLUTION-PAIR-CANCEL` `DERIVED_LEAN`: [MAJ-GIN-INVOLUTION-PAIR-CANCEL](MAJ-GIN-INVOLUTION-PAIR-CANCEL.md) (PROVED_LEAN)
