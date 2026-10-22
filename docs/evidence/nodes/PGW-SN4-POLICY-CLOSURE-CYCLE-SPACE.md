# PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_PROSE`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(4) applies a supplied pair-separation closure policy. The sealed source derives no object-language endogenous demand generator; under the declared policy, which reads admitted structure and automorphism orbits and issues one requirement per orbit, the fixed finite datum set reaches the all-pairs-separated fixpoint, and a closed run from an empty requirement store makes at most n(n−1)/2 rounds (closedRun_round_bound_from_empty). At that terminal state the active separation-demand set is empty, so W₄ = ∅ and s₄ = 0, while the retained history H₄ stays nonempty. A complete graph K_m records the separated pairs of m data; for m ≥ 1 it is connected with cycle-space dimension m(m−1)/2 − m + 1.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

- Declared pair-separation closure policy of the sealed Genesis account, token-blind and isomorphism-equivariant (assumption)

## Bottleneck

Neither supply nor a stage number selects the policy, and there is no claim that the carrier has four data or that exactly five receipts were issued, so dual_ledger_independence_at_stage_4 (s₄ = 0, |H₄| = 5) is a table identity; K_m edges need not be admitted binary relations, and S4Orbit counts complete-graph edges without orbit search.

## Source status

genesis_source.txt section 9 (closure under declared policy); 002_oesn level_04_simplex_graph_expansions.md (written)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_education/documentation/002_oesn/lean4/SnTheorems.lean`

- file: `omega_engine_education/documentation/002_oesn/lean4/SnTheorems.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0516_sn4_policy_closure_cycle_space.md`

- file: [dag/derivations/05_mssn_sn/tfq_0516_sn4_policy_closure_cycle_space.md](../../../dag/derivations/05_mssn_sn/tfq_0516_sn4_policy_closure_cycle_space.md)
- sha256 (`lf-normalised`): `c17c5878e071655b4199b937684701b74faa17f025fe7efa2967294c4a772d6d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0516
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_04_simplex_graph_expansions.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_04_simplex_graph_expansions.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean::closedRun_round_bound_from_empty`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/code/sn_core.py::S4Orbit`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/lean4/SnTheorems.lean::dual_ledger_independence_at_stage_4`

## Absences recorded by the TFQ records

- TFQ-0516 rust: no Rust check of the S(4) ledger or of K_m cycle-space dimension

## Routes

Incoming (1):

- `PGW-R-SN4-POLICY-CLOSURE-CYCLE-SPACE` `DERIVED_PROSE`: [PGW-SN3-COST-TWO-UNARY-MARK](PGW-SN3-COST-TWO-UNARY-MARK.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-SN-E08-WEIGHTED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-SN-E08-WEIGHTED-L1-DUALITY](PGW-SN-E08-WEIGHTED-L1-DUALITY.md) (CONDITIONAL)
- `PGW-R-SN5-CONTINUATION-RECORDED-REQUEST` `DERIVED_PROSE`: [PGW-SN5-CONTINUATION-RECORDED-REQUEST](PGW-SN5-CONTINUATION-RECORDED-REQUEST.md) (DEFINITION)
