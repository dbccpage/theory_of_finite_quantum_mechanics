# FQ-CABELLO-NO-INTEGER-FRAME

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The 18 Cabello integer rays with 9 orthogonal tetrads admit no Int-valued 0/1-type frame assignment (odd count 9 = 2k has no solution: cabello_parity_obstruction); frame additivity and bounded nonnegativity do not force PSD (frame_function_additivity_not_force_psd).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- real-symmetric representative of frame function (assumption)

## Bottleneck

Scope is the integer/real-symmetric Cabello system, not arbitrary complex-Hermitian matrices.

## Source status

H054 header carries "PR #205 scope correction" demotion; ledger typed LEAN PROVED (RECEIPTED)

## Review

- PFP review: [dag/results/FQ-CABELLO-NO-INTEGER-FRAME/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-CABELLO-NO-INTEGER-FRAME/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Literal general integer parity, full measured-ray/source scaled checks, and the independently verified normalized M_bad/2 countermodel with a negative quadratic direction.
  - does not support: Arbitrary complex-Hermitian frame systems, general even-parity sufficiency, or a fully instantiated refined-carrier operad.
  - next test: Batch review must compare the source scaled integer checks with actual rational readouts and preserve the even-control limitation.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/EverettForkingTree.lean`

- file: [lean4/EverettForkingTree.lean](../../../lean4/EverettForkingTree.lean)
- sha256 (`bytes`): `1dc256ecbad36c8d1a3cb128ba67fab5efc37880d9a58d58698dfc4765646b0e`
- cited in: node.lean, record TFQ-1015
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `EverettForkingTree`): recorded sha256 `1dc256ecbad36c8d1a3cb128ba67fab5efc37880d9a58d58698dfc4765646b0e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build EverettForkingTree`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cabello_parity_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms cabello_parity_obstruction` |

- counts toward the grade: yes

### Lean: `lean4/GleasonCyclotomicObstruction.lean`

- file: [lean4/GleasonCyclotomicObstruction.lean](../../../lean4/GleasonCyclotomicObstruction.lean)
- sha256 (`bytes`): `1d1e388e88865166cb0d2aa45032dfe400d193d5517abae81060743bc6626c88`
- cited in: node.lean, record TFQ-1015
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `GleasonCyclotomicObstruction`): recorded sha256 `1d1e388e88865166cb0d2aa45032dfe400d193d5517abae81060743bc6626c88` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GleasonCyclotomicObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cabello_no_integer_frame_assignment` | yes | yes | yes | Quot.sound, propext | `#print axioms cabello_no_integer_frame_assignment` |
| `frame_additivity_not_force_psd` | yes | yes | yes | none | `#print axioms frame_additivity_not_force_psd` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1015_fq_cabello_no_integer_frame.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1015_fq_cabello_no_integer_frame.md](../../../dag/derivations/10_finite_qm_core/tfq_1015_fq_cabello_no_integer_frame.md)
- sha256 (`lf-normalised`): `9dd0c96a6ddd06ee8b39bb6e98d54f27a55f29191a290f5ccb8e94f05c078ab3`
- generated view: listed, not counted
- cited in: record TFQ-1015
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md)
- sha256 (`lf-normalised`): `259e971c72c485503b9c9f157bec6ec9412fe24b8c4cc266e1d0ab6aa7e2d1e0`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:604e2768b7d0ee3423792a93ba46749403a8df2cdfa61198bf69fa12243b52f7::cabello_18`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`

## Routes

Incoming (1):

- `FQ-R-CABELLO` `DERIVED_LEAN`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (3):

- `FQ-R-BUSCH` `COMPUTED`: [FQ-BUSCH-EFFECT-FRAME](FQ-BUSCH-EFFECT-FRAME.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-CABELLO-POLYTOPE` `COMPUTED`: [FQ-CABELLO-FRAME-POLYTOPE-146](FQ-CABELLO-FRAME-POLYTOPE-146.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-CONTEXTUALITY` `DERIVED_LEAN`: [FQ-CONTEXTUALITY-CECH-F2](FQ-CONTEXTUALITY-CECH-F2.md) (PROVED_LEAN)
