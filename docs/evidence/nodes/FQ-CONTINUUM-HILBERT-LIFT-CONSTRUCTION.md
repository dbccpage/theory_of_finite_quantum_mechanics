# FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With the scalar field k in {R, C} and the l2 uniformity supplied as named hypotheses: the exact finite carriers Fin n -\> Q form a tower under zero padding whose directed union N -\>0 Q is exhausted by the finite stages; the Hausdorff completion of N -\>0 k is a complete inner product space into which the exact carrier embeds inner-product-preservingly, injectively and padding-compatibly (lift, liftFin); a sequence of exact vectors is Cauchy in the lift exactly when it is rational-l2-Cauchy, and every such sequence converges; over R the exact carrier is dense, continuous maps out of the lift are determined on exact vectors, and the lift is strictly larger than the carrier; over C the Gaussian-rational pairs a + ib are dense with the exact inner-product identity; the completion of the exact carrier under its intrinsic rational uniformity (the infimum of the rational sqdist-ball filters) is uniformly isomorphic to the real lift; the lift is linearly isometric to l2(N, k) with exact vectors as their coordinate sequences; every Q-linear map of the exact carrier with a rational quadratic bound C lifts uniquely to a continuous linear operator of norm at most sqrt(C) (the shift lifts to an isometry), and the Q-linear coordinate-sum functional admits no continuous extension.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 12
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 9 Lean reference(s) cited, 9 in this checkout (replay: none 9). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- scalar field R or C, i.e. the completion of Q or of Q(i) (assumption)
- l2 uniformity on the exact carrier (assumption; harmonic_separates_uniformities shows that l1 is a different choice)

## Bottleneck

Both hypotheses are supplied; their selection from finite-theory primitives is the content of FQ-GAP-CONTINUUM-HILBERT-LIFT. Dynamics and generators are not lifted (FQ-GAP-STONE-CONTINUOUS-TIME); the bound C on an exact operator is a hypothesis.

## Source status

Kernel-checked (Lean 4.33.1, pinned Mathlib cache) in dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion (four modules, 112 receipts) and dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps (three further modules; 168 receipts including the re-replayed dependencies); exact replays in code/python/src/qm/hilbert_lift_completion.py (20 tests, certificate row in test_isolated_certificates.py) and code/rust/src/qm/hilbert_lift_completion.rs (18 inline tests); replayed with Lean 4.35.0 on 2026-10-21.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/HilbertLiftCompletion.lean`

- file: [lean4/HilbertLiftCompletion.lean](../../../lean4/HilbertLiftCompletion.lean)
- sha256 (`bytes`): `2e188609f0a08148273e9ad7e6a0f931d0799b626df9872c7f26bda4c6dde106`
- cited in: node.lean, record TFQ-1021
- replay: `none`
- check: `cd lean4 && lake build HilbertLiftCompletion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.controlled_completion` | yes | yes | yes | - | `#print axioms HilbertLift.controlled_completion` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftComplexCarrier.lean`

- file: [lean4/HilbertLiftComplexCarrier.lean](../../../lean4/HilbertLiftComplexCarrier.lean)
- sha256 (`bytes`): `4151b5f8a74cdf10988dcf93ca24c2fbcc7562b6e53454cb4b3062d9dcac7309`
- cited in: node.lean, record TFQ-1021
- replay: `none`
- check: `cd lean4 && lake build HilbertLiftComplexCarrier`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.controlled_completion_complex` | yes | yes | yes | - | `#print axioms HilbertLift.controlled_completion_complex` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftFiniteTower.lean`

- file: [lean4/HilbertLiftFiniteTower.lean](../../../lean4/HilbertLiftFiniteTower.lean)
- sha256 (`bytes`): `3b4e86865b4a0e63724cb7ca0b876479f3ac0a9d3364a030d6cc8d2de560e341`
- cited in: node.lean, record TFQ-1021
- replay: `none`
- check: `cd lean4 && lake build HilbertLiftFiniteTower`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.exhaustion` | yes | yes | yes | - | `#print axioms HilbertLift.exhaustion` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftIntrinsicUniformity.lean`

- file: [lean4/HilbertLiftIntrinsicUniformity.lean](../../../lean4/HilbertLiftIntrinsicUniformity.lean)
- sha256 (`bytes`): `25339d6949deb4aa4113a686415e8ba9d40c5ce957d7015d1b8f3d05d06af1ed`
- cited in: node.lean, record TFQ-1021
- replay: `none`
- check: `cd lean4 && lake build HilbertLiftIntrinsicUniformity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.intrinsic_completion` | yes | yes | yes | - | `#print axioms HilbertLift.intrinsic_completion` |
| `HilbertLift.uniformity_eq_iInf_sqdist` | yes | yes | yes | - | `#print axioms HilbertLift.uniformity_eq_iInf_sqdist` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftL2Model.lean`

- file: [lean4/HilbertLiftL2Model.lean](../../../lean4/HilbertLiftL2Model.lean)
- sha256 (`bytes`): `3fade85d7333f166567e8a5927b87219377aaede1e4602655ceb6043d90469ad`
- cited in: node.lean, record TFQ-1021
- replay: `none`
- check: `cd lean4 && lake build HilbertLiftL2Model`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.l2_model_summary` | yes | yes | yes | - | `#print axioms HilbertLift.l2_model_summary` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftOperators.lean`

- file: [lean4/HilbertLiftOperators.lean](../../../lean4/HilbertLiftOperators.lean)
- sha256 (`bytes`): `d7ffd585fc01353bb69bf7534de6c788ca43525084bdb3654bc3161639b72573`
- cited in: node.lean, record TFQ-1021
- replay: `none`
- check: `cd lean4 && lake build HilbertLiftOperators`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.no_continuous_extension_coordSum` | yes | yes | yes | - | `#print axioms HilbertLift.no_continuous_extension_coordSum` |
| `HilbertLift.operator_lift_summary` | yes | yes | yes | - | `#print axioms HilbertLift.operator_lift_summary` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftRationalUniformity.lean`

- file: [lean4/HilbertLiftRationalUniformity.lean](../../../lean4/HilbertLiftRationalUniformity.lean)
- sha256 (`bytes`): `554a6e9f0b593cbda1346c32126615e8b07c769b2ec800bb486cd21d2e6fd27d`
- cited in: node.lean, record TFQ-1021
- replay: `none`
- check: `cd lean4 && lake build HilbertLiftRationalUniformity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.harmonic_separates_uniformities` | yes | yes | yes | - | `#print axioms HilbertLift.harmonic_separates_uniformities` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/hilbert_lift_completion.rs`

- file: [code/rust/src/qm/hilbert_lift_completion.rs](../../../code/rust/src/qm/hilbert_lift_completion.rs)
- sha256 (`bytes`): `dd5e7d6aa4a5447328499f964867e2da125b9ed1fd74b6133dc8fcd8a10135e3`
- cited in: node.rust, record TFQ-1021

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `certify` (rust_symbol) | yes | yes | yes | - | - |
| `coord_sum_gap` (rust_symbol) | yes | yes | yes | - | - |
| `modulus_holds` (rust_symbol) | yes | yes | yes | - | - |
| `shift_is_isometric` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1021_fq_continuum_hilbert_lift_construction.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1021_fq_continuum_hilbert_lift_construction.md](../../../dag/derivations/10_finite_qm_core/tfq_1021_fq_continuum_hilbert_lift_construction.md)
- sha256 (`lf-normalised`): `39108fcea7189f7ded4c721ec39479cf44d54bc5276329eb526d0b930ea2eb4f`
- generated view: listed, not counted
- cited in: record TFQ-1021
- counts toward the grade: no

### Documents and data: `dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/README.md`

- file: [dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/README.md](../../../dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/README.md)
- sha256 (`lf-normalised`): `390ac197881587f3b39d397e87249de26383e82baae3cbf87beeb993b062c6f2`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/review.md`

- file: [dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/review.md](../../../dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/review.md)
- sha256 (`lf-normalised`): `ffcc6ba2caff7e2cb72d94a279ed2341f33c0f8e736e15ddc77e34d60d745817`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps/README.md`

- file: [dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps/README.md](../../../dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps/README.md)
- sha256 (`lf-normalised`): `1876e42480bee8ab05e517f2ddd069134ac4f05b76ba898cc112cf52e990bdaa`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps/review.md`

- file: [dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps/review.md](../../../dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps/review.md)
- sha256 (`lf-normalised`): `68b445d35bae477cb9a9429171d3ad2c9c56ecffd7279ddddba70f02500c72c9`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-CONTINUUM-HILBERT-LIFT-CONSTRUCTION` `CONDITIONAL_ON_IMPORT`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (1):

- `FQ-R-GAP-CONTINUUM-FROM-CONSTRUCTION` `GAP_NO_DERIVATION`: [FQ-GAP-CONTINUUM-HILBERT-LIFT](FQ-GAP-CONTINUUM-HILBERT-LIFT.md) (CONDITIONAL)
