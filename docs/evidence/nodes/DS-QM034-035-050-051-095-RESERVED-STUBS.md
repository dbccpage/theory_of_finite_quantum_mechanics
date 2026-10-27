# DS-QM034-035-050-051-095-RESERVED-STUBS

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Unitary finite shadow, Hamiltonian generator admission, Dirac equation admission, spinor structure admission, Copenhagen as authority shadow and the 200-series slots 200/202/203/204/205 have 1-row ledgers that only reserve a slot. They contain no claim; recorded as OPEN, not as results. Papers carry release headers over internal stub bodies where I opened them (034, 035, 050, 051, 202, 203, 205).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- unitary group (assumption)
- Hamiltonian generator (assumption)
- Dirac gamma matrices / spinors (assumption)

## Bottleneck

Finite rational Cayley unitary shadow U=(I-tJ)(I+tJ)^{-1} and 2D Dirac/Clifford spinor relations are mechanized in DerivationDagQMClosure.lean; full monograph expansions remain conditional on unitary/Hamiltonian/spinor imports.

## Source status

Finite rational Cayley unitary shadow U=(I-tJ)(I+tJ)^{-1}, exact quadratic norm preservation vs Euler inflation, and 2D Dirac/Clifford spinor relations mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/DS-QM034-035-050-051-095-RESERVED-STUBS/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM034-035-050-051-095-RESERVED-STUBS/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Declared Cayley matrices are orthogonal while Euler expands norm at nonzero t; concrete two-generator Clifford identities are recomputed.
  - does not support: Supply spinor/Dirac carrier, Hamiltonian, dynamics and formal matrix bridges before closing the reserved paper stubs.
  - next test: Supply spinor/Dirac carrier, Hamiltonian, dynamics and formal matrix bridges before closing the reserved paper stubs.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0245 (shared), record TFQ-0246 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` |
| `QuantumMechanics.DerivationDagQMClosure.fq_entropy_purity_and_ds_qm034_051_cayley_clifford_witness` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_entropy_purity_and_ds_qm034_051_cayley_clifford_witness` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md)
- sha256 (`lf-normalised`): `a70dea94189cb9ca6b93b538a6421895c099576905968fec92f698c6cbfcdbbb`
- generated view: listed, not counted
- cited in: record TFQ-0245 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md)
- sha256 (`lf-normalised`): `5a5e181911194955dd1390a01fc988265bfba481d61489d270abc7ed4689f568`
- generated view: listed, not counted
- cited in: record TFQ-0246 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0278_copenhagen_slot_reserved_as_an_authority_shadow.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0278_copenhagen_slot_reserved_as_an_authority_shadow.md](../../../dag/derivations/13_finite_qm_information/tfq_0278_copenhagen_slot_reserved_as_an_authority_shadow.md)
- sha256 (`lf-normalised`): `13bab7cc5334068682024b2f5a505ec0cd6ca48f568032a5f2421e8a42be2917`
- generated view: listed, not counted
- cited in: record TFQ-0278 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:1494bf7bd4b575bf4fd55f701625313b640d6bb6da9cc7d8bdb0fcf61b7356b7#QM_203-C0`
- `external:sha256:2146758ae7ffadfd070bcf96aa58f57462830217e4e29483e28a545aefe01ea2#QM_034-C0`
- `external:sha256:2e330e8070370c47aa7ce824d0a91b49d9fd057458c5646e4e0440c106eb403d#QM_051-C0`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`
- `external:sha256:9a029ebf407a2437256e94496d09add63ef1b27449ec9543b88f64b4f73f9b86#QM_035-C0`
- `external:sha256:a0c447cab768c3fe12823d4618525f4335d3ed27a61d7d7e00c363426865ab57#QM_205-C0`
- `external:sha256:a0f370963e9ed2fa38ebc7e309fff86340e17a90e6f342ccc8d0d29391290164#QM_050-C0`
- `external:sha256:b5b7f6d366f589b342d69bcd0cc6206ad025317ad0837a2059b51ec8ab822cf8#QM_095-C0`
- `external:sha256:ecea5df07ecd8ffaabcfccbca41f85aa940dcf0b051bc9ee69481bc1f700c04e#QM_202-C0`

## Routes

Incoming (2):

- `DS-R-QM034-051-FINITE-SHADOWS` `CONDITIONAL_ON_IMPORT`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-UNITARY-SHADOW-STUB` `CONDITIONAL_ON_IMPORT`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

