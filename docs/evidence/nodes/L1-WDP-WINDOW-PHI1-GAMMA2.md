# L1-WDP-WINDOW-PHI1-GAMMA2

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A finite cochain window (C0,C1,C2,d0,d1) with d1 d0 = 0 has quotient Q1 = C1/im(d0). Phi1(\[x\]) is the quotient seminorm (min over potentials of the weighted l1 norm of x - d0 h). Gamma2 is the l1 norm of d1 applied to a minimizer, and R_cl = Gamma2/Phi1. Missing or ill-typed window data gives a typed NoRule refusal. Gamma2 here is a norm; QM_020 uses 'Gamma' for a set of residual sectors.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- weighted l1 norm on C1 (declared, see L1-OBSERVER-AXIOMS-H1-H5): assumption

## Bottleneck

The weighted l1 form of the norm is declared in the window definition, not derived from MSS-0 or Difference. Upstream window construction is in the WDP fragment.

## Source status

WDP-CH04-D02 definition; diagnostic classes ExactClass / ClosedResidual / ActiveClosureFailure

## Review

- PFP review: [dag/results/L1-WDP-WINDOW-PHI1-GAMMA2/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-WDP-WINDOW-PHI1-GAMMA2/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: Actual flatness refusal, weighted quotient residual and Gamma2/Phi1 with explicit zero-denominator handling; generic kernel identities and refusal control.
  - does not support: Provide arbitrary typed cochain-window validation and norm choices and prove refinement to the production Phi1/Gamma2 contract. No probability or sector weight follows.
  - next test: Provide arbitrary typed cochain-window validation and norm choices and prove refinement to the production Phi1/Gamma2 contract. No probability or sector weight follows.

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
| `QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance` |
| `QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `d4a9514b3ee22c73ac47193206838c49cd5d908485d2c38dd026cd3bd9416cf8`
- cited in: record TFQ-0349 (shared), record TFQ-0354 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `code/rust/src/wdp/phi1_coda_adapter.rs`

- file: [code/rust/src/wdp/phi1_coda_adapter.rs](../../../code/rust/src/wdp/phi1_coda_adapter.rs)
- sha256 (`bytes`): `a87803bfe55c4f16247dfe593bbb691570ee495b19d07c0a82ff096c5591c276`
- cited in: record TFQ-0349 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `code/rust/src/wdp/primitive_axiomatics.rs`

- file: [code/rust/src/wdp/primitive_axiomatics.rs](../../../code/rust/src/wdp/primitive_axiomatics.rs)
- sha256 (`bytes`): `c1ae6edba4d807a8247b3a2726dd7d07f30d83dbb27611e036c09e5e6ef26efc`
- cited in: record TFQ-0349 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md)
- sha256 (`lf-normalised`): `1596c27b09af32aec26710dacafcbe1dcb5081bc06d35d094b4c0b0353932e64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md`

- file: [dag/derivations/07_l1_emergence/tfq_0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md](../../../dag/derivations/07_l1_emergence/tfq_0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md)
- sha256 (`lf-normalised`): `fd010b5046d0bcdf92ac381f394fc56ffd2373d7101bfc2bcccb0dd066cd6d1e`
- generated view: listed, not counted
- cited in: record TFQ-0349 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md`

- file: [dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md](../../../dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md)
- sha256 (`lf-normalised`): `d4531de0213a9426dd4e3025c034634a7373aed0a94d9b8eb21bcf4f662e1e65`
- generated view: listed, not counted
- cited in: record TFQ-0354 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:075755bfa5d217bf1c7ea42e9169ee078e6a15e40018e318b77d5ba829dda5d8::Phi1Functional`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:67f95afb329218e2db037b98e7b7d632e0ee073156f58a6c3b03ff9a386b4702::Cochain1`
- `external:sha256:67f95afb329218e2db037b98e7b7d632e0ee073156f58a6c3b03ff9a386b4702::solve_exact_potential_weighted`

## Routes

Incoming (1):

- `X-R-WDP-WINDOW-TO-L1-WINDOW` `DERIVED_LEAN`: [PG-WDP-DEGREE1-WINDOW](PG-WDP-DEGREE1-WINDOW.md) (DEFINITION)

Outgoing (8):

- `APP-R-FSP-RATIONAL-QUOTIENT-NORMAL-FORM` `DERIVED_PROSE`: [FSP-RATIONAL-QUOTIENT-NORMAL-FORM](FSP-RATIONAL-QUOTIENT-NORMAL-FORM.md) (PROVED_PROSE)
- `APP-R-MAJ-F2-PARITY-SCHEDULE` `DERIVED_PROSE`: [MAJ-F2-PARITY-SCHEDULE](MAJ-F2-PARITY-SCHEDULE.md) (DEFINITION)
- `APP-R-MAJ-PHI1-HAMMING-COSET` `DERIVED_PROSE`: [MAJ-PHI1-HAMMING-COSET](MAJ-PHI1-HAMMING-COSET.md) (DEFINITION)
- `APP-R-QCV-SELF-OBSTRUCTION-MODEL` `DERIVED_PROSE`: [QCV-SELF-OBSTRUCTION-MODEL](QCV-SELF-OBSTRUCTION-MODEL.md) (DEFINITION)
- `L1-R-KKT` `DERIVED_LEAN`: [L1-FRAMEWORK-KKT-CERT](L1-FRAMEWORK-KKT-CERT.md) (PROVED_LEAN)
- `L1-R-PHI1-QUOTIENT` `GAP_NO_DERIVATION`: [L1-QM002-O022A-PHI1-QUOTIENT](L1-QM002-O022A-PHI1-QUOTIENT.md) (OPEN)
- `L1-R-REPLICA-L1` `GAP_NO_DERIVATION`: [L1-WDP-CH08-C01-REPLICA-L1](L1-WDP-CH08-C01-REPLICA-L1.md) (OPEN)
- `L1-R-RESIDUAL-TO-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)
