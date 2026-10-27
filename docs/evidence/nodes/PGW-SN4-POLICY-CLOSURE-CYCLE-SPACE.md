# PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_PROSE`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(4) applies a supplied pair-separation closure policy. The sealed source derives no object-language endogenous demand generator; under the declared policy, which reads admitted structure and automorphism orbits and issues one requirement per orbit, the fixed finite datum set reaches the all-pairs-separated fixpoint, and a closed run from an empty requirement store makes at most n(n−1)/2 rounds (closedRun_round_bound_from_empty). At that terminal state the active separation-demand set is empty, so W₄ = ∅ and s₄ = 0, while the retained history H₄ stays nonempty. A complete graph K_m records the separated pairs of m data; for m ≥ 1 it is connected with cycle-space dimension m(m−1)/2 − m + 1.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

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

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Rounds.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Rounds.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Rounds.lean)
- sha256 (`bytes`): `4b99ab31fc2a384709450f7d9a664d6aa35026a69599d98524802846f2e25b2d`
- cited in: node.lean, record TFQ-0516
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Rounds`): recorded sha256 `4b99ab31fc2a384709450f7d9a664d6aa35026a69599d98524802846f2e25b2d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Rounds.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closedRun_round_bound_from_empty` | yes | yes | yes | Quot.sound, propext | `#print axioms closedRun_round_bound_from_empty` |

- counts toward the grade: yes

### Lean: `lean4/Imported/SymmetricGroupPresentations/SnTheorems.lean`

- file: [lean4/Imported/SymmetricGroupPresentations/SnTheorems.lean](../../../lean4/Imported/SymmetricGroupPresentations/SnTheorems.lean)
- sha256 (`bytes`): `1c2c2b2a0774d7bc849eb584d2b135353e6d7ceb0d77041e70c175182ef93016`
- cited in: node.lean, record TFQ-0516
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.SymmetricGroupPresentations.SnTheorems`): recorded sha256 `1c2c2b2a0774d7bc849eb584d2b135353e6d7ceb0d77041e70c175182ef93016` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/SymmetricGroupPresentations/SnTheorems.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `dual_ledger_independence_at_stage_4` | yes | yes | yes | module-level | `#print axioms dual_ledger_independence_at_stage_4` |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0516_sn4_policy_closure_cycle_space.md`

- file: [dag/derivations/05_mssn_sn/tfq_0516_sn4_policy_closure_cycle_space.md](../../../dag/derivations/05_mssn_sn/tfq_0516_sn4_policy_closure_cycle_space.md)
- sha256 (`lf-normalised`): `21284dfe12202e12a52b6357e65193b9905887428ea7fc2fc82e2f1fced6d335`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0516
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_04_simplex_graph_expansions.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_04_simplex_graph_expansions.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_education/documentation/002_oesn/code/sn_core.py::S4Orbit`

## Absences recorded by the TFQ records

- TFQ-0516 rust: no Rust check of the S(4) ledger or of K_m cycle-space dimension

## Routes

Incoming (1):

- `PGW-R-SN4-POLICY-CLOSURE-CYCLE-SPACE` `DERIVED_PROSE`: [PGW-SN3-COST-TWO-UNARY-MARK](PGW-SN3-COST-TWO-UNARY-MARK.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-SN-E08-WEIGHTED-L1-DUALITY` `DERIVED_LEAN`: [PGW-SN-E08-WEIGHTED-L1-DUALITY](PGW-SN-E08-WEIGHTED-L1-DUALITY.md) (PROVED_LEAN)
- `PGW-R-SN5-CONTINUATION-RECORDED-REQUEST` `DERIVED_PROSE`: [PGW-SN5-CONTINUATION-RECORDED-REQUEST](PGW-SN5-CONTINUATION-RECORDED-REQUEST.md) (DEFINITION)
