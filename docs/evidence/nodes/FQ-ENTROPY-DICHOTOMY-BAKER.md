# FQ-ENTROPY-DICHOTOMY-BAKER

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For an algebraic spectrum, von Neumann entropy is zero iff the state is pure (entropy_zero_iff_pure) and positive for mixed spectra (mixed_entropy_positive); transcendence of mixed entropy follows from the Baker hypothesis supplied as a hypothesis. Rust gives exact rational spectra and cited-anchor rational interval enclosures with integer Renyi power sums.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

None (algebraic purity dichotomy, Renyi-2 purity deficit, and C750 prime-reduction linear form separation from the imported Baker transcendence axiom mechanized in fq_embedding_relativity_and_entropy_baker_dichotomy_closure and fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census).

## Source status

C750 algebraic purity dichotomy (entropy_zero_iff_pure and Renyi-2 purity deficit d^2 - (p^2 + (d-p)^2) = 2(dp - p^2)), prime-reduction linear form vanishing on pure weights (gamma = 0) vs non-zero mixed witness (gamma = 6 != 0 on d=4, S=1, b=2), and conditional Baker transcendence gate mechanized in DerivationDagQMClosure.lean, EntropyDichotomy.lean, C750Purity.lean, and finite_quantum_mechanics

## Review

- PFP review: [dag/results/FQ-ENTROPY-DICHOTOMY-BAKER/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-ENTROPY-DICHOTOMY-BAKER/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Literal general-dimension source entropy signatures with explicit Baker hypothesis, plus five exact rational series computations with an explicit analytic remainder argument.
  - does not support: An unconditional proof of Baker or transcendence from a native flag, base-two entropy claims, or a kernel-verified finite-tail array transport.
  - next test: Recompute each rational series/tail/width and challenge both units and hypothesis promotion.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0268
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_embedding_relativity_and_entropy_baker_dichotomy_closure` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_embedding_relativity_and_entropy_baker_dichotomy_closure` |
| `QuantumMechanics.DerivationDagQMClosure.fq_entropy_purity_and_ds_qm034_051_cayley_clifford_witness` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_entropy_purity_and_ds_qm034_051_cayley_clifford_witness` |
| `QuantumMechanics.DerivationDagQMClosure.fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census` |

- counts toward the grade: yes

### Lean: `lean4/EntropyDichotomy.lean`

- file: [lean4/EntropyDichotomy.lean](../../../lean4/EntropyDichotomy.lean)
- sha256 (`bytes`): `6bc9bc70f4328a35208832f5754cbffb2ac646cd8323d16d5dc0647b75f7f96c`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `EntropyDichotomy`): recorded sha256 `6bc9bc70f4328a35208832f5754cbffb2ac646cd8323d16d5dc0647b75f7f96c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build EntropyDichotomy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `entropy_zero_iff_pure` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms entropy_zero_iff_pure` |
| `mixed_entropy_positive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms mixed_entropy_positive` |

- counts toward the grade: yes

### Lean: `lean4/EntropyPurity.lean`

- file: [lean4/EntropyPurity.lean](../../../lean4/EntropyPurity.lean)
- sha256 (`bytes`): `3b79f31d0247f34d89832dffa1f1ab75503e49fe3b78514dcf008214e3f8230e`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `EntropyPurity`): recorded sha256 `3b79f31d0247f34d89832dffa1f1ab75503e49fe3b78514dcf008214e3f8230e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build EntropyPurity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mixed_entropy_is_transcendental` | yes | yes | yes | Quot.sound, propext | `#print axioms mixed_entropy_is_transcendental` |

- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0268_von_neumann_entropy_interface_for_mixed_states.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0268_von_neumann_entropy_interface_for_mixed_states.md](../../../dag/derivations/13_finite_qm_information/tfq_0268_von_neumann_entropy_interface_for_mixed_states.md)
- sha256 (`lf-normalised`): `eba7e0962d5bd9b5d089ea55a6064d603ce041a426debabec7d873bcee3924cc`
- generated view: listed, not counted
- cited in: record TFQ-0268
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche8_tensor_stone_continuum_embedding_and_leftover_mnc_witness`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness`
- `external:sha256:b4c75f1ec3426411ee8aefa7428ed3b708ee0263ab2507b10ceca7a821abb88a::CitedAnchor`
- `external:sha256:b4c75f1ec3426411ee8aefa7428ed3b708ee0263ab2507b10ceca7a821abb88a::RationalSpectrum`

## Absences recorded by the TFQ records

- TFQ-0268 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0268 rust: no local rust twin located for external:sha256:a535b66c7800bd1d4f29228891ab5a6c23dd8ce3173c2521621c366686fe5ab5
- TFQ-0268 rust: no local rust twin located for external:sha256:b4c75f1ec3426411ee8aefa7428ed3b708ee0263ab2507b10ceca7a821abb88a

## Routes

Incoming (1):

- `FQ-R-ENTROPY` `DERIVED_LEAN`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (0):

