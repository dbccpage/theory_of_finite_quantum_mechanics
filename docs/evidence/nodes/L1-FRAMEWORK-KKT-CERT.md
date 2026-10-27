# L1-FRAMEWORK-KKT-CERT

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For integer lists of equal length: if a dual vector z is annihilated by every coboundary (z . (coboundary p') = 0 for all p'), satisfies the capacity bound |z_i| \<= w_i, and closes the gap (sum w_i |r_i| = z . omega), then r has minimal weighted l1 norm among all omega + coboundary(p').

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Stated over integer lists in lean4/Imported/L1ObstructionFramework/lp_general_certificate.lean (general_finite_certificate_optimality). The real-vector version is weak LP duality and is not in Lean. The 3-step iterator in the same paper is REFUTED per its ledger.

## Source status

Thm 4.2 finite KKT certificate; Lean general_finite_certificate_optimality (integer lists)

## Review

- PFP review: [dag/results/L1-FRAMEWORK-KKT-CERT/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-FRAMEWORK-KKT-CERT/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact supplied primal/dual certificate predicates for a triangle, with accepted and capacity/divergence/gap failures; generic rational bound-to-optimality implication in Lean.
  - does not support: Prove representation refinement to the external arbitrary-list integer certificate and arbitrary real-vector attainment. A valid numeric triangle certificate does not establish unrestricted dual attainment.
  - next test: Prove representation refinement to the external arbitrary-list integer certificate and arbitrary real-vector attainment. A valid numeric triangle certificate does not establish unrestricted dual attainment.

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
| `QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` |

- counts toward the grade: yes

### Lean: `lean4/Imported/L1ObstructionFramework/lp_general_certificate.lean`

- file: [lean4/Imported/L1ObstructionFramework/lp_general_certificate.lean](../../../lean4/Imported/L1ObstructionFramework/lp_general_certificate.lean)
- sha256 (`bytes`): `f0364fa7b80f8bd494d99da2e9703461b1bf0b88d33e605e175c19fc58f325f7`
- cited in: node.lean, node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_emergence.json](../../../dag/research/lean_replay_campaign_l1_emergence.json) (module `Imported.L1ObstructionFramework.lp_general_certificate`): recorded sha256 `f0364fa7b80f8bd494d99da2e9703461b1bf0b88d33e605e175c19fc58f325f7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/L1ObstructionFramework/lp_general_certificate.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `general_finite_certificate_optimality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms general_finite_certificate_optimality` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/fenchel_duality.rs`

- file: [code/rust/src/wdp/fenchel_duality.rs](../../../code/rust/src/wdp/fenchel_duality.rs)
- sha256 (`bytes`): `ca7fe2172744dc3952b90c9367a64e649d4b0b46fc81b9471e5f79e6dde41df8`
- cited in: record TFQ-0351
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `d4a9514b3ee22c73ac47193206838c49cd5d908485d2c38dd026cd3bd9416cf8`
- cited in: record TFQ-0351
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0351_accept_an_integer_finite_list_certificate_only_inside_its_capacity_circulation_feasibility.md`

- file: [dag/derivations/07_l1_emergence/tfq_0351_accept_an_integer_finite_list_certificate_only_inside_its_capacity_circulation_feasibility.md](../../../dag/derivations/07_l1_emergence/tfq_0351_accept_an_integer_finite_list_certificate_only_inside_its_capacity_circulation_feasibility.md)
- sha256 (`lf-normalised`): `a02083e57a8b0fb6de4b73077d0d3b757b83196d23f51891f4c0932d629f33b8`
- generated view: listed, not counted
- cited in: record TFQ-0351
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:67f95afb329218e2db037b98e7b7d632e0ee073156f58a6c3b03ff9a386b4702::DualWitnessCertificate`
- `external:sha256:fc5a04df299e671184b29b3468bd5fd18b70680beadaeaf4aebd5d809976d3e1::FenchelDualityReceipt`
- `external:sha256:fd65bc148e80462c1c467b0b5a483e5691a901b95d2789ac25425bb5da64eb19`

## Routes

Incoming (1):

- `L1-R-KKT` `DERIVED_LEAN`: [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION), [L1-CHAIN-D1D0-AXIOM](L1-CHAIN-D1D0-AXIOM.md) (ADMITTED_PRIMITIVE)

Outgoing (1):

- `L1-R-DENSITY-LIFT-PUB009` `GAP_NO_DERIVATION`: [L1-DENSITY-LIFT-SIGNED-SQRT-PUB009](L1-DENSITY-LIFT-SIGNED-SQRT-PUB009.md) (OPEN)
