# Plan: finish PFP prompt creation, execution and incorporation

**AuthorityEffect:** None. This is a work plan from a read-only audit of `dag/prompts/`, `dag/results/`, `dag/derivation_dag.json`, `dag/theory_of_finite_qm.{jsonl,md}` and `papers/core/` (2026-10-21, six parallel audits). It changes no status.

## 1. Where things stand

| Item | State |
|---|---|
| Prompts | 177 (one per DAG node when the DAG had 177 nodes; no status filter; no generator script in the repo). |
| Executed | 151 of 177, in 9 batches over index positions 1–151. |
| Never executed | 26: positions 152–155 (`L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE`, `L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED`, `L1-U1-SELECTOR-OTHER-SEGMENT`, `L1-WDP-REALIFICATION-J`) and 156–177 (22 `PG-*` pregenesis / MSS-N / WDP prompts). They were not skipped for failure; the batch run stopped at 151. All 26 validate and have operad records. |
| Nodes with no prompt | 159 of the 336-node DAG at audit time (137 `PGW-*`, 20 application-branch, 2 from PR #122). After the unified-DAG merge the DAG has more nodes again (see `sync_unified_dag.py`); every node without a prompt needs one. |
| Stages reached | Every executed folder reached P5, but every P5 host check reads `..._recorded_pending_batch_review`; the only verdict is `scoped_result_or_obstruction_reviewed`. Review is self-review by one local researcher. P4 mutants are mostly output-coordinate perturbations. 34 of 44 FQ and all 49 DS `next_test` fields are boilerplate. |
| Incorporated into the DAG/JSONL/MD | **No.** No node carries a review path, `narrowest_claim` or `does_not_support`; results landed only in `dag/operads/index.json`. |
| Incorporated into `papers/core` | **No.** Only three result folders are cited (U1, Born and Stone runs, not reviews). The change log stops at 2026-10-20; nothing covers the PFP batches or PRs #113, #117, #122, #125, #128 and #130. |

### Status gaps the results expose (DAG says more than the review supports)

- **PROVED_LEAN narrower than the result.** About 26 FQ, 21 DS and 30 L1/GP/IMPL/PG-GEN nodes support only a fixed witness, a finite instance or a coordinate case. Examples: BELL-RATIONAL-VIOLATION-14-5, TSIRELSON-SOS, TRACE-ZERO-DUALITY-K23, WEYL, GLEASON-D2, PHASE-BLIND-DESCENT, DS-QM030-GRADED-PATHSUM, DS-QM080-IMPORT-FREE-TRACE-NORM-CORE, DS-QM102, PG-GEN-NO-RETURN, GP-GAP-EXACT-DUALITY and L1-QM003-C17.
- **Vacuous source theorem behind PROVED_LEAN.**
  - DS-QM061-BUILDABILITY: a reflexive iff.
  - DS-QM093-SURVIVAL: a Boolean AND.
  - DS-QM090-092: `decide (defect = 0)`.
  - L1-QM020-THM6-P1: a `True` stub.
  - DS-QM032-CONTINUUM-LIMIT: OracleNeeded, with no convergence.
  - DS-QM206: a toy C4 map.
  - DS-QM207-211: a Boolean ladder.
- **Stale after later Lean work.**
  - L1-IMP-HILBERT-INNER-PRODUCT and L1-IMP-ORTHOGONAL-ADDITIVITY: the #125 sector-form delta was never merged.
  - GP-IMPORT-CONTINUUM-HILBERT still says "OPEN gap" after #117/#122.
  - Eleven import nodes have since been discharged in FQ-* nodes.
  - The Born (×4), Hilbert-lift (×2), Stone and U(1) run deltas were never merged into `dag/operads/`.
  - FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION has no prompt, operad or results folder.
- **Artifact drift.**
  - The CPTP v2 carrier fix was never propagated to `review_result.json`.
  - 14 batch-32–51 operads still say "global baseline failing", although the custody repair shows 0 errors.
  - DAG `lean4/quantum_mechanics/...` paths do not exist; the files live at `lean4/<Name>.lean`.
  - `verify_batch.py` for batch 132–151 fails, because companions moved to `*.contract.score.yaml`.
  - The STONE Lean modules `U1PythagoreanObstruction.lean` and `U1PowerMapInjectivity.lean` were reported uncommitted.

## 2. Plan

### Phase A — tooling (one PR)
1. **Write the generator `dag/pfp/generate_prompts.py`.** It emits, from a DAG node:
   - the prompt (`{stage}_{id}_{status}.yaml` via `custody.canonical_filename`, with the statement text verbatim);
   - the operad record, with `paper_source_pins` and source and declaration-scan candidates;
   - the audit row and the index row.
2. **Leave the sealed files alone.** `prompt_audit.json`, `filename_custody.json` and `custody.py` stay untouched. Add `dag/pfp/prompt_audit_extension.json`, and have `validate_prompts.py` derive its expected count from the corpus instead of the hard-coded 177.
3. **Add `dag/sync_pfp_results.py --check`.** It writes a `pfp_review` object onto each reviewed node: review path, sha256, verdict, `narrowest_claim`, `does_not_support`, `next_test` and `scope_effect`. Extend `validate_derivation_dag.py` (`NODE_KEYS` and an object check) and its tests. The JSONL row gets `pfp_review_refs`, and the MD row gets a "review boundary" line.
4. **Repair `verify_batch.py`** for the companion layout. Pre-clear the cargo target before Rust replays (the errno 28 case).

### Phase B — incorporate the 151 results (one PR)
*Done on branch `pfp-results` (2026-10-21).* `dag/sync_pfp_results.py` writes a `pfp_review` object on each of the 151 reviewed nodes from the decisions in `dag/fragments/pfp_review_decisions.json` (68 consistent, 9 caveat_added, 52 statement_narrowed, 22 status_lowered) and `pfp_review_refs` onto the base JSONL rows; the validator checks the object; the later Born, Hilbert-lift and U(1) run deltas are merged into their operad collections, and the sealed collections and `dag/operads/index.json` are left byte-identical, with `reviews/20261021_post_discharge_addendum/` added to the 25 affected result folders (later runs, the custody repair of the "global baseline failing" status, and the CPTP v2 carrier correction). The 20 operads that still say "global baseline failing" are 14 DS and 6 FQ collections.

5. **Run `sync_pfp_results.py` dry** to list candidates.
6. **Apply status edits by review rule.** A node stays PROVED_LEAN only if its statement lies within the narrowest claim. Otherwise either rewrite the statement down to the narrowest claim (preferred), or move it to CONDITIONAL / COMPUTATIONALLY_CHECKED with the unmet part in the bottleneck. Start with the vacuous-source and overclaim lists above.
7. **Merge the unmerged run deltas** (#113, #117, #122, #125, U1, Stone) into `dag/operads/`. Add "superseded by run …" pointers to the stale reviews, and refresh the CPTP v2 artifacts and the 14 "baseline failing" statuses.
8. **Replace boilerplate `next_test` strings** with each node's real `does_not_support` obligation.

### Phase C — execute the remaining prompts (about 10 PRs of 20 prompts)
9. **Batch 1:** positions 152–177, the 26 existing prompts, in index order. Run the 4 L1 prompts first; L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED is the sole input of the L1-R-SQRT-GAP and L1-R-COMPLEX-GAP routes. Three PG records have 0 operation candidates and need manual mining: COLLAPSE-BARRIER, OLD-IMAGE-INJECTIVE and SN-OFF-IMAGE-REFUSAL.
10. **Batches 2 onward:** prompts for every node without one, ordered in three tiers:
    - Tier A: OPEN, CONDITIONAL, IMPORTED, PROVED_PROSE, COMPUTATIONALLY_CHECKED and SOURCE_RECORD.
    - Tier B: PROVED_LEAN.
    - Tier C: DEFINITION.

    This now includes the unified-DAG record nodes and the audited FSP, MUB6, Majorana and DFM corpus nodes.
11. **Follow-up prompts on the unpaid bridges** the reviews name:
    - normalized/projective PHASE-BLIND;
    - the recurrence-to-matrix bridge;
    - the Bell rational transport;
    - Q(√2) to real SOS;
    - K23 LP duality;
    - real-embedding homomorphisms;
    - Weyl field semantics;
    - Hilbert-lift complex operators;
    - Stone and U(1) divisibility;
    - the [[5,1,3]]/[[7,1,3]] codes for DS-QM102;
    - a formal F2 cochain for DS-QM120;
    - a genuine functor for DS-QM206;
    - import independence for DS-QM207-211;
    - tensor transport for DS-QM074/094.
12. **Per batch:** follow the `init → prepare → run → review → create_companions → integrate → finalize → publish → verify_batch` sequence. Add semantic near-miss P4 mutants, not only coordinate perturbations, and get a second, independent reviewer for any node whose DAG status depends on the result.

### Phase D — papers/core (one PR per paper)
13. **`finite_quantum_mechanics.md` §13.8.8.** It still describes the 177-node DAG, where "every node has ≥2 Lean and ≥2 Rust bindings". That is false now. Regenerate the counts from the DAG, retitle the section as a status census, and add non-claim sentences from `does_not_support` to items 2–5 and to §13.8.9.
14. **Fix understatements and fill missing sections.** Correct §4 items 3 (p=2 is kernel-checked) and 9 (K23). Update §5 item 1 for the Hilbert-lift construction/selection split. Add sections for Born effect-valuation (#113), sector-form uniqueness (#125) and TFQ-0417..0558 (#128).
15. **Add a "DAG results audit" table**, one row per reviewed node: supports / does_not_support / narrowest / next_test.
16. **Claim ledger.** Add PROVED_LEAN to the taxonomy, or retype `FQM-U1-C*`. Fix the Distribution total, `FQM-DAG1` and the projection date.
17. **Change log.** Add dated entries for the PFP batches, for #113, #117/#122, #125, #128 and #130, and for the unified-DAG merge. Fix the "7 modules / C1..C5" mismatch.
18. **TeX/PDF.** The .tex is a pandoc export that ends at §13.8.3, and the PDF is from 2026-10-17. Re-export, bump the version (0.55.0 / 2026-10-14) and rebuild; add `papers/core/build_core.ps1`.
19. **Back-links.** The fsp, mub6, majorana and sign-problem READMEs and ledgers cite no DAG node. Add the node and TFQ ids. The unified DAG now records each corpus record's audited status; reconcile the corpus papers with those audits. For example, FSP-DERIV-056 is refuted as stated, and MUB6 terminal non-existence has no local Lean proof.

### Checks after every phase
`python -I dag/sync_unified_dag.py --check`, `python -I dag/sync_application_branches.py --check`, `python -I dag/sync_pregenesis_to_wdp.py --check`, `python -I dag/sync_unified_dag.py --invariants`, `python -I dag/validate_derivation_dag.py --no-files`, `python -m pytest dag/test_*.py`, `python scripts/build_master_derivation_ledger.py` plus a diff review, and the PFP prompt validator with its 30 tests.
