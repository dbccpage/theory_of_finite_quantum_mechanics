# Overclaim review: import of the sibling programme folders (branch `lean-import-programmes`)

**AuthorityEffect:** None. Reviewer: the agent that built the branch; the scanner is offline and deterministic.

## Scope

The branch (stacked on #202, `lean-replay-campaign`) adds 79 Lean files under `lean4/Imported/{HigherCategoryTheory,WdpReasoning,Mub6,SymbolGameLoose}`, their receipts (`dag/research/lean_replay_campaign_imported_programmes.json`), `ImportedAtlas` roots, an inventory section and tools. Against its base it changes **no node, route, record, status, statement or bottleneck** (`git diff lean-replay-campaign -- dag/derivation_dag.json dag/fragments dag/derivations` is empty), and no public prose except the generated README facts block and the evidence pages.

## Method

- `python -I -X utf8 scripts/overclaim_scan.py --changed-since lean-replay-campaign --strict`: HIGH 0, MEDIUM 0, LOW 3, exit 0. `--changed-since origin/main --strict` (which also includes #202): HIGH 0, exit 0.
- Whole-checkout scan: HIGH 0, MEDIUM 18, LOW 299. The 8 R2 and 10 R7 findings are in nodes and prose this branch does not touch (all R2 nodes are in the scanner's current output on `origin/main` too); they are not re-reviewed here.
- No status changed, so no node needs the statement-vs-theorem review; no number in a statement or note was changed.
- Lean was built for each imported module (Lean 4.35.0, Mathlib `56a005855`); this review relies on those receipts and did not rebuild.

## Result

0 FULL, 0 NARROWED, 0 OVERCLAIM: nothing to review at node level. No receipt is cited by a node (`dag_node` is absent on every row), so no grade can move because of this branch (evidence grades E0 192, E1 232, E2 36, E3 432, E4 0, as on #202).

## Corrections to the PR's own text

None needed. One claim worth stating exactly: the receipts say a file *builds* and, where it declares theorems, which axioms they use. 10 of the 74 files that build declare no theorem (umbrella or stub modules such as `Master`, `Lib`, `SymbolGame`, `LGGR1`..`LGGR3`), so their rows carry `axiom_audit_passed: false` with `axiom_audit_basis` "the file declares no theorem and cites none: nothing to audit". That is a statement about the file, not a failure.

## Numbers recomputed (from the receipts and manifest, by script)

| Claim | Recomputation | Match |
|---|---|---|
| 79 files imported (22 HCT, 4 WDP, 1 MUB6, 52 loose) | count of `import_manifest_programmes.json` files by slug | yes |
| 74 build with exit code 0, 5 do not | `exit_code` over the 79 rows | yes |
| 64 rows with `axiom_audit_passed` true | rows with exit 0 minus 10 theorem-less | yes |
| 74 new `ImportedAtlas` roots | roots in `lean4/lakefile.lean` for the manifest modules | yes |
| 79 admission scans clean | `admission_scan_passed` over the rows (lexer-based scan) | yes |
| every row's sha256 equals the committed blob | `git cat-file blob HEAD:<path>` for 351 receipt rows | yes |

## What the scanner could not decide

- Whether the imported HCT, WDP-reasoning and S(n)/MSS-N files state what the DAG says about those programmes: no node cites them yet, so there is nothing to compare. Linking nodes to them is a separate change that needs this review.
- `Level21DiscreteRegge.lean` carries its own withdrawal notice ("Withdrawn as evidence for MSS-021"); it builds, but must not be cited as evidence.
- The five files that do not build are not in the library: `MubFiniteCornerReduction` (needs the external `Hadamard6` package), `LGGR` and `LggrNonFactorization` (import four modules that exist nowhere), `FiniteConsequences` (imports `paper_er006`, nowhere) and `TerminalizerPolicy` (a `deriving Fintype` failure under current Mathlib; its header says it never elaborated).
