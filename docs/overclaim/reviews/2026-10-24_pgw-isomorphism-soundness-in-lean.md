# Review of PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN

Scope: pre-commit derivation on `derive/PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN`, base `1fa451fe1eac640d84f0c34ba88a71dcdd32dfb6`. Reviewed against the statement as it stands in `dag/derivation_dag.json`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full original claim and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH=0 MEDIUM=0 LOW=0) and `scripts/auto/anti_pattern_lint.py --changed-since origin/main` (0 findings). Read the node statement, bottleneck, obligation, `lean4/CampaignPgwIsomorphismSoundnessInLean.lean`, the `#print axioms` lines in `dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json`, `canonicalKey_classification` in `lean4/Imported/Genesis19l57g1/PaperSearch.lean`, `U0`/`U1`/`BL`/`swap01` in `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`, and `SetCollections` in `lean4/Imported/Genesis19l57g1/PaperOrbit.lean`. Re-ran `python -I -X utf8 checks/independent/pgw-isomorphism-soundness-in-lean.py`. The lake build was not rerun for this review; the receipt records exit 0 and wall 9169 ms.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN. Record status stays OPEN_OBLIGATION. AuthorityEffect stays None.

The original claim is the implemented Python key, a budget-truncated cross-check, and a Python-orbit versus Lean-orbit comparison on exported runs. Those sentences are not the current statement, and they are not Lean theorems. The current statement is the finite boundary below. Route `PGW-R-ISOMORPHISM-SOUNDNESS-IN-LEAN` is unchanged.

Corrections to the PR's own text:
- The numeral tuples `(2, [1], [(0, [0])], [], [(0, 1)])` and `(2, [2], [(0, [0, 1])], [], [(0, 1)])` are output of the independent checker. They are not theorems in `lean4/CampaignPgwIsomorphismSoundnessInLean.lean`. Lean states equality and inequality of `canonicalKey`, not those tuples.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN | `pgwIso_U0_wf`, `pgwIso_U1_wf`, `pgwIso_BL_wf`, `pgwIso_set_collections`, `pgwIso_candidate_counts`, `pgwIso_U0_U1`, `pgwIso_keys_eq`, `pgwIso_U0_not_BL`, `pgwIso_keys_ne` | NARROWED | Finite U0, U1, BL boundary matches the declarations. Python key, budget cutoff, and exported-run orbits stay open. Status stays OPEN. |

Statement-vs-theorem, current statement only:

| Atomic claim | Declaration | Match |
|---|---|---|
| U0, U1, BL are the data-count-2 regimes with the stated forms, instances, empty rules, and requirement (0, 1) | definitions `U0`, `U1`, `BL` at `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean:47-51` | by definition |
| U0, U1, BL are well-formed | `pgwIso_U0_wf`, `pgwIso_U1_wf`, `pgwIso_BL_wf` (`CampaignPgwIsomorphismSoundnessInLean.lean:34-83`) | type is `Regime.wf` |
| duplicate-free instances, rules, and requirements | `pgwIso_set_collections` (`:85-91`); `SetCollections` is `insts.Nodup ∧ rules.Nodup ∧ reqs.Nodup` (`PaperOrbit.lean:147-148`) | conjunction of the three |
| each exhaustive candidate list has length 2 | `pgwIso_candidate_counts` (`:93-97`) | `(candidateKeys _).length = 2` for each |
| datum swap is an isomorphism U0 to U1 | `pgwIso_U0_U1` (`:13-32`); `dmap := swap01` (`Minimality.lean:232-233`) | `Iso U0 U1` |
| exhaustive keys of U0 and U1 are equal | `pgwIso_keys_eq` (`:99-102`) via `canonicalKey_classification` (`PaperSearch.lean:279-281`) | `canonicalKey U0 = canonicalKey U1` |
| no isomorphism U0 to BL | `pgwIso_U0_not_BL` (`:104-105`) | `(Iso U0 BL) → False` |
| exhaustive keys of U0 and BL differ | `pgwIso_keys_ne` (`:107-112`) | `canonicalKey U0 ≠ canonicalKey BL` |
| implemented Python key classes match a brute-force minimum | none | open |
| budget-truncated regimes and exported-run orbit comparison | none | open |

Axiom lines recorded in the receipt, inside propext, Classical.choice, and Quot.sound. Classical.choice does not appear. `pgwIso_set_collections` has an empty axiom list. The other eight anchors list propext, or propext and Quot.sound.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement and note | data count 2 | `U0`, `U1`, `BL` first field is 2; checker claim "data count 2" | match |
| statement | one form, arities 1, 1, and 2 | definitions `[1]`, `[1]`, `[2]`; checker "form arities differ" | match |
| statement | candidate-list length 2 | `2! * 1! = 2`; checker `len(candidate_keys) == 2` for each regime | match |
| note | unary minimum `(2, [1], [(0, [0])], [], [(0, 1)])` | checker lex minimum over the two datum swaps and the one form permutation | match, checker only |
| note | binary minimum `(2, [2], [(0, [0, 1])], [], [(0, 1)])` | same enumeration on BL | match, checker only |
| receipt | wall 9169 ms | lake timing already recorded; not an arithmetic identity | unrecomputed measurement |

Independent check on this review pass: `checked 32 claims, failures 0`.

## Scanner output

Before the receipt re-pin: HIGH=0, MEDIUM=0, LOW=0. After the re-pin, the same scan is HIGH=0, MEDIUM=0, LOW=3. The three LOW rows are pre-existing and sit on TENSOR-ASSUMPTION-COUNTERMODELS and FQ-GAP-TENSOR-UNIQUENESS, whose evidence pages changed only because the tensor receipt pins moved. No baseline entry. Anti-pattern lint 0. The route diff does not contain `PGW-R-ISOMORPHISM-SOUNDNESS-IN-LEAN`.

## What the scanner cannot decide

Whether `canonicalKey` equality is the implemented Python key. It is not: `canonicalKey` is the Lean minimum of `candidateKeys`, and the Python procedure is not an input of these declarations. A closed length-2 enumeration does not discharge the source leftovers named in `source_status`.
