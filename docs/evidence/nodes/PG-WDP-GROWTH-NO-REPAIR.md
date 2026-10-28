# PG-WDP-GROWTH-NO-REPAIR

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For weighted-L1 windows with attained minima: if the sub-window's d0 is the restriction of the big d0, its cochain is the restriction and its weights are at most the restrictions, then Phi1(sub) \<= Phi1(big), so growth with an extending cochain and weights not lowered never lowers Phi1 (a decrease needs deleting cells, lowered weights, a changed d0 or changed cochain values); attaching a 2-cell whose row satisfies d1 d0 = 0 leaves (D0, w, h) and hence Phi1 unchanged (definitional) and adds |row . h| to Gamma2 = ||d1 h||_1, so Gamma2 cannot decrease. Monotonicity fails when weights are raised, when d0 is not the restriction, or for a norm not monotone under coordinate deletion (norm arithmetic only). Equal-weight subdivision, filtration limit pages, complex coefficients and the existence of minimisers are not covered.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 14
- distinct cited Lean declarations covered by a current replay receipt: 14
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The source Lean theorems (wdp_growth_subcomplex_monotone, wdp_two_simplex_attachment_preserves_phi1) are a List Nat sum bound and an rfl; the real statement is proved here only under hcompat, restricted cochain, weights not raised and attained minima; equal-weight subdivision and existence of minimisers are unported.

## Source status

WDP-CH04-P09 MECHANIZED in DerivationDagQMClosure.lean (subcomplex monotonicity and 2-simplex attachment invariance)

## Review

- PFP review: [dag/results/PG-WDP-GROWTH-NO-REPAIR/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-WDP-GROWTH-NO-REPAIR/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: For weighted-L1 graph windows with attained minima, restricting to a sub-window whose d0, cochain and weights are the restrictions (weights at most the restrictions of the big weights) never raises Phi1, and attaching 2-cells with d1 d0 = 0 leaves Phi1 unchanged and cannot lower Gamma2; in the native table, deleting cells, lowering weights and changing the cochain strictly lowered Phi1 (kernel instances exist only for raised weights and a changed d0).
  - does not support: Monotonicity for arbitrary norms J or renormalised weights (the instances show it fails), or when the sub d0 is not the restriction of d0; existence of minimisers for weighted L1 as a Lean theorem; that each of the three failing hypotheses is by itself sufficient to lower Phi1 in general (kernel instances exist for raised weights and a changed d0; the native rows cover deletion, a changed cochain and lowered weights); equal-weight subdivision and filtration limit pages (clauses of WDP-CH04-P09 absent from the source Lean); the source Gamma2 at a minimal residual of a non-closed window (non-unique, withheld); complex coefficients; any physical reading.
  - next test: Prove the equal-weight subdivision clause of WDP-CH04-P09 (subdividing an edge through a new degree-two vertex with equal weights leaves Phi1 unchanged) as a Lean theorem over IsPhi and check it by exact enumeration; separately discharge the existence of minimisers (IsPhi attainment) for weighted L1 so that phi_restrict_le has no attained-minimum hypothesis.

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
| `QuantumMechanics.DerivationDagQMClosure.wdp_growth_subcomplex_monotone` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.wdp_growth_subcomplex_monotone` |
| `QuantumMechanics.DerivationDagQMClosure.wdp_two_simplex_attachment_preserves_phi1` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.wdp_two_simplex_attachment_preserves_phi1` |

- counts toward the grade: yes

### Lean: `lean4/WdpGrowthNoRepair.lean`

- file: [lean4/WdpGrowthNoRepair.lean](../../../lean4/WdpGrowthNoRepair.lean)
- sha256 (`bytes`): `e63dabeb12267072f7e483d15139c675d71441cef9e4cd006a8f3407c31910e1`
- cited in: node.lean, receipt dag/research/pfp_batch01_lean_replay.json (WdpGrowthNoRepair)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `WdpGrowthNoRepair`): recorded sha256 `e63dabeb12267072f7e483d15139c675d71441cef9e4cd006a8f3407c31910e1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build WdpGrowthNoRepair`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WdpGrowthNoRepair.closed_attach` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.closed_attach` |
| `WdpGrowthNoRepair.gamma2_attach` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.gamma2_attach` |
| `WdpGrowthNoRepair.gamma2_attach_ge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.gamma2_attach_ge` |
| `WdpGrowthNoRepair.gamma2_repair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.gamma2_repair` |
| `WdpGrowthNoRepair.incompatible_d0_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.incompatible_d0_instance` |
| `WdpGrowthNoRepair.nonmonotone_norm_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.nonmonotone_norm_instance` |
| `WdpGrowthNoRepair.phi_attach_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.phi_attach_iff` |
| `WdpGrowthNoRepair.phi_growth_not_lower` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.phi_growth_not_lower` |
| `WdpGrowthNoRepair.phi_le_unrepaired` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.phi_le_unrepaired` |
| `WdpGrowthNoRepair.phi_restrict_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.phi_restrict_le` |
| `WdpGrowthNoRepair.rescaled_weights_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.rescaled_weights_instance` |
| `WdpGrowthNoRepair.triangle_row_closed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpGrowthNoRepair.triangle_row_closed` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `54a2d6c70adcbfb8ef7203785769515f17ab69b375f47f8f9eca1fb4eaa0bcb7`
- cited in: record TFQ-0346 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md)
- sha256 (`lf-normalised`): `1596c27b09af32aec26710dacafcbe1dcb5081bc06d35d094b4c0b0353932e64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0346_do_not_lower_phi1_by_passing_to_a_larger_complex_attaching_faces.md`

- file: [dag/derivations/06_wdp/tfq_0346_do_not_lower_phi1_by_passing_to_a_larger_complex_attaching_faces.md](../../../dag/derivations/06_wdp/tfq_0346_do_not_lower_phi1_by_passing_to_a_larger_complex_attaching_faces.md)
- sha256 (`lf-normalised`): `a3f593ff7910ebfaf1a0be3247c6690513d5c22ee4ef772b6ce7a07f0e292484`
- generated view: listed, not counted
- cited in: record TFQ-0346 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_wdp_obligations_and_growth_witness`

## Routes

Incoming (1):

- `PG-R-GROWTH` `DERIVED_LEAN`: [PG-WDP-QUOTIENT-EXACT-SEQUENCE](PG-WDP-QUOTIENT-EXACT-SEQUENCE.md) (PROVED_LEAN), [PG-CHAIN-RETRACTION](PG-CHAIN-RETRACTION.md) (PROVED_LEAN)

Outgoing (0):

