# L1-OPERATOR-LIFT-TRACE-EMBED-013

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For integer lists v the diagonal trace norm equals sum |v_i| (trace_norm_eq_mass). Scaling by c != 0 keeps the normalized absolute weights and, for |c|\>1, raises the mass. Reconstruction without an admitted mass returns failure. The real operator embedding is not constructed in Lean. C05: the trace embedding carries no physical state or quantum claim.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 1 in this checkout (replay: none 1). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

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
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` |
- counts toward the grade: yes

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/013_operator_lifts_trace_metrics_and_representation_limits/lean4/Lifts.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/013_operator_lifts_trace_metrics_and_representation_limits/lean4/Lifts.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source, record TFQ-1000
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1000
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1000_l1_operator_lift_trace_embed_013.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1000_l1_operator_lift_trace_embed_013.md](../../../dag/derivations/08_l1_to_l2/tfq_1000_l1_operator_lift_trace_embed_013.md)
- sha256 (`lf-normalised`): `5072573388bb3387a0e905bbc56417a83b380df62d942e5eeace0a4686242ca8`
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

