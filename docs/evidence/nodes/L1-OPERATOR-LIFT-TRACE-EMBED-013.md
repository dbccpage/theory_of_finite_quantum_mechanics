# L1-OPERATOR-LIFT-TRACE-EMBED-013

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For integer lists v the diagonal trace norm equals sum |v_i| (trace_norm_eq_mass). Scaling by c != 0 keeps the normalized absolute weights and, for |c|\>1, raises the mass. Reconstruction without an admitted mass returns failure. The real operator embedding is not constructed in Lean. C05: the trace embedding carries no physical state or quantum claim.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declaration references covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- real operator / Banach embedding: lift

## Bottleneck

Banach-space embedding, injectivity and the fibre statements are prose-only.

## Source status

013 C01-C03, C06 \[PROVED\] finite integer lists; C05 \[NEGATIVE BOUNDARY\]

## Review

- PFP review: [dag/results/L1-OPERATOR-LIFT-TRACE-EMBED-013/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-OPERATOR-LIFT-TRACE-EMBED-013/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact diagonal/singular-value mass, nonzero-scale invariance and declared-mass reconstruction controls; generic absolute scaling and sign-loss statements in Lean.
  - does not support: Construct the real Banach/operator embedding and exact signed-data reconstruction contract. Retain sign data separately; probability weights plus mass cannot recover signs.
  - next test: Construct the real Banach/operator embedding and exact signed-data reconstruction contract. Retain sign data separately; probability weights plus mass cannot recover signs.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1000
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` |

- counts toward the grade: yes

### Lean: `lean4/Imported/OperatorLifts/Lifts.lean`

- file: [lean4/Imported/OperatorLifts/Lifts.lean](../../../lean4/Imported/OperatorLifts/Lifts.lean)
- sha256 (`bytes`): `da77446b350410fd7d74b397108efa8ba81b0a0a3b0a0aedb0c8f371b23369fa`
- cited in: node.lean, node.source, record TFQ-1000
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `Imported.OperatorLifts.Lifts`): recorded sha256 `da77446b350410fd7d74b397108efa8ba81b0a0a3b0a0aedb0c8f371b23369fa` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OperatorLifts/Lifts.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `trace_norm_eq_mass` | yes | yes | yes | propext | `#print axioms trace_norm_eq_mass` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1000
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1000_l1_operator_lift_trace_embed_013.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1000_l1_operator_lift_trace_embed_013.md](../../../dag/derivations/08_l1_to_l2/tfq_1000_l1_operator_lift_trace_embed_013.md)
- sha256 (`lf-normalised`): `d48aedf432a3cca2373cd55892719c9bf7cfd2e64a2efca29499a5280355ae37`
- generated view: listed, not counted
- cited in: record TFQ-1000
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/013_operator_lifts_trace_metrics_and_representation_limits/operator_lifts_trace_metrics_and_representation_limits_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/013_operator_lifts_trace_metrics_and_representation_limits/operator_lifts_trace_metrics_and_representation_limits_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `L1-R-TRACE-EMBED` `DERIVED_LEAN`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)

Outgoing (0):

