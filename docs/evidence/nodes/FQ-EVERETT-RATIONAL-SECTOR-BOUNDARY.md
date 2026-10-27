# FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Equal-weight branch counting in a forking tree reproduces Born weights iff all weights are rational. For Born weights in Q(zeta_n)^+ minus Q (witness conductor 5, weights (5 +- sqrt5)/10) no finite integer fine-graining N = sum m_j gives m_j/N = w_j (witness polynomial 5x^2-5x+1 has no rational root).

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

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Everett forking tree and equal-weight counting (assumption)

## Bottleneck

Lean states the two-outcome case: rational weights p0/D, p1/D have an equal-weight fine-graining. For the witness polynomial 5x^2 - 5x + 1 Lean checks the rational-root candidates; the multi-outcome iff is not in Lean.

## Source status

H059 (13 theorems); GAP-F001-S000-011 PRICED_CONTINUUM_INTERFACE

## Review

- PFP review: [dag/results/FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: general rational-pair fine graining and full rational-root exclusion are kernel checked; retained multi-outcome multiplicities and quadratic-field root coefficients are exact.
  - does not support: Prove arbitrary finite-vector fine-graining transport and that the declared quadratic-field coefficients realize the intended physical readout. Counting is an admitted interpretation.
  - next test: Prove arbitrary finite-vector fine-graining transport and that the declared quadratic-field coefficients realize the intended physical readout. Counting is an admitted interpretation.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: record TFQ-0276 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`
- counts toward the grade: no

### Lean: `lean4/RationalSector.lean`

- file: [lean4/RationalSector.lean](../../../lean4/RationalSector.lean)
- sha256 (`bytes`): `60a60ca5bb7130f1e6f972532eeadb7f0ccb0dd4dac17b307c32201c566d8d6b`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_dynamics.json](../../../dag/research/lean_replay_campaign_finite_qm_dynamics.json) (module `RationalSector`): recorded sha256 `60a60ca5bb7130f1e6f972532eeadb7f0ccb0dd4dac17b307c32201c566d8d6b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build RationalSector`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `conductors_with_real_q_yield_rational_finegraining` | yes | yes | yes | none | `#print axioms conductors_with_real_q_yield_rational_finegraining` |
| `rational_finegraining_exists` | yes | yes | yes | none | `#print axioms rational_finegraining_exists` |
| `witness_poly_has_no_candidate_rational_root` | yes | yes | yes | none | `#print axioms witness_poly_has_no_candidate_rational_root` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0276_everettian_relative_state_contact.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0276_everettian_relative_state_contact.md](../../../dag/derivations/13_finite_qm_information/tfq_0276_everettian_relative_state_contact.md)
- sha256 (`lf-normalised`): `70e578c4a0ed0d5cb49ffafcff2b07f84b3ec7eaa2f5b328d4ce3fd917d188dc`
- generated view: listed, not counted
- cited in: record TFQ-0276 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:3933bf77065af23c4d3da2c7074185cede173389be6f96c4bc03ae2bd3d3fce8::BranchCounting`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- `external:sha256:6983e52032f87a31b351b356ab57a52f8f75e26e57b8e7746d75e3609470f99c::EverettForkingNode`

## Absences recorded by the TFQ records

- TFQ-0276 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm

## Routes

Incoming (1):

- `FQ-R-EVERETT` `COMPUTED`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION), [FQ-BORN-NORMALIZATION-REDUNDANCY](FQ-BORN-NORMALIZATION-REDUNDANCY.md) (PROVED_LEAN)

Outgoing (0):

