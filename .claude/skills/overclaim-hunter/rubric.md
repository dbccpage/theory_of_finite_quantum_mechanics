# Overclaim hunter: rubric

**AuthorityEffect:** None.

Reference for `SKILL.md`. Nothing here changes a status.

## The honesty rule

A node may carry PROVED_LEAN only if Lean declarations **in this repository** state the node's **full** statement and compile with only `propext`, `Classical.choice` and `Quot.sound` (the rule of `dag/pfp/campaign/README.md` and `dag/research/frontier_targets_lean_review.md`). The status order is OPEN < IMPORTED_ASSUMPTION < CONDITIONAL < COMPUTATIONALLY_CHECKED < PROVED_PROSE < PROVED_LEAN (`PFP_STATUS_RANK` in `dag/validate_derivation_dag.py`). A review lowers or keeps; it never raises.

## What the scanner rules mean, and what to do

| Rule | Sev | Meaning | Human step |
|---|---|---|---|
| R1 | HIGH | PROVED_LEAN with no Lean ref resolving in this checkout (atlas-only, path missing, or symbol absent from the file) | Not PROVED_LEAN here. Propose the lowered status. If the Lean lives in the atlas, the claim is only as good as an unchecked pointer. |
| R2 | MEDIUM | Cited theorem has type `True`; or the statement says every/all/unique/iff but every cited theorem is closed; or the proof is only `decide`/`rfl`/`norm_num` on a closed instance | Instance-vs-general candidate. A closed exhaustive `decide` is a legitimate proof of a finite instance, so read the statement: does it claim the instance or the general law? The evidence field says whether the statement uses universal wording. On main today R2 flags 13 of the 14 nodes of #171: 10 of the 11 that #176 narrowed (the miss is CT-ENTANGLING-PHASE-FINITE-TARGET, whose problem was a restating witness, class 1 below) and all 3 that proved FULL. So R2 is a prompt, not a verdict. |
| R3 | HIGH | `sorry`, `admit`, `axiom` declaration, `native_decide` or `unsafe` outside comments and strings, in a module cited by a PROVED_LEAN or CONDITIONAL node | Every citing node is OVERCLAIM until the token is removed and replayed. The scan does not follow imports; check the import closure of a flagged module by hand. |
| R4 | HIGH | A replay receipt (`dag/research/*lean_replay*.json`) whose recorded sha256 differs from the file (CRLF-folded hash also accepted), whose source is missing, or whose axioms list more than the allowed three | The receipt no longer certifies this source. Rebuild and re-pin, or treat every node it supports as unreplayed. |
| R5 | LOW | A number (two or more digits) in a node statement, derivation note or README line that appears in no cited Lean/Rust/Python file, receipt entry or `checks/independent/<id>.py` of the node | Step 3 of the skill. Many hits are ids, ranges or numbers in prose that are derived, not copied: recompute, do not assume. The count is the signal, not any single hit. |
| R6 | HIGH | A sentence in README, docs, papers or derivation notes names a node id and says proves/proved/derived/establishes/shows that, while the node's status is not PROVED_LEAN, PROVED_PROSE or COMPUTATIONALLY_CHECKED | Reword the prose to the DAG status. Sentences with a hedge (not, if, whether, target, aim, ...) or that print the node's own status are skipped, so a clean R6 is weak evidence. |
| R7 | MEDIUM | Promotional or absolute wording in public prose (list: `PROMOTIONAL_PHRASES` in the scanner), outside quoted negations | Replace with a scoped statement. Lists of non-claims below a "does not claim" line are skipped when they are in the same paragraph. |
| R8 | MEDIUM | `dag/derivations/independent/*.md` whose first line is not `Status: AI-drafted, awaiting human review.` or `Status: Reviewed by <name>, <date>.` | Fix the line. Only a named human may write the reviewed line; check the PR gives that name. |
| R9 | HIGH | With `--changed-since`: a status that rose versus the base with no new resolving Lean ref plus a receipt entry in the diff (COMPUTATIONALLY_CHECKED may instead add `checks/independent/<id>.py`) | Revert the rise unless the review finds FULL. |
| R10 | LOW | PROVED_LEAN node whose cited modules appear in no replay receipt in this repository | Note it; the compile evidence is outside this repository's receipts. |

## Failure classes seen in #171 (look for each by hand)

1. **Witness restates the hypothesis**: a "Schmidt witness" that is `|det M|^2`, a quadratic function of the amplitudes that just re-expresses the entanglement criterion it claims to detect.
2. **Bounded check, unbounded claim**: exhaustive to twice-spin 3 or to |X| <= 4 while the node says "all labels". Compare every bound in the Lean with every quantifier in the statement.
3. **Table copied, not derived**: identities verified against a case table transcribed from Rust (`isingF`, hard-coded `f(d)` values). The theorem is about the table, not the formula.
4. **Definition makes the claim trivial**: a count entered as a definition (`R(n) = ...`), then proved equal to itself.
5. **Hypothesis presented as theorem**: a lemma assuming "fidelity is monotone under CPTP maps" used for a node that claims it for all CPTP maps.
6. **One direction of an iff**, or an iff stated for a restricted class (`dB <= dA`).
7. **Header or docstring claim with no theorem**: "linearly independent over Q", "the extensions are connected". Only the declaration's type counts.
8. **Wrong counts in prose**: 380 intervals where Lean proves 340 + 40; 10,825 tuples where the exact count is 13,691; 192 where Lean counts 48; a matrix entry 1/2 where Lean has -1/2.
9. **Goes through a different object**: Gram determinant 3x3 proved, node says bordered Cayley-Menger 5x5; equality between them is not a theorem.
10. **Name is not content**: a theorem called `..._iff_...` that proves one implication; `..._all_...` that proves an instance.

## Verdict wording

- **FULL**: "every atomic claim matched: <claim> -> `<decl>` (<file>:<line>)".
- **NARROWED**: give the node's new `statement` verbatim as it should stand, the new `bottleneck` (what is not proved, in the node's own style: no "proves", "obviously", "simply", "merely", "impossible", "universal": the validator's `FORBIDDEN` list), and the status (usually unchanged).
- **OVERCLAIM**: say what the cited Lean does state (if anything), the status to revert to, and the lowest-cost route back (the missing declaration).

## Review file template

```
# Review of <scope>

Scope: <PR/batch, commit, base>. Reviewed against the statements as they stand at <ref>. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: <what was read; scanner version/commit; what was NOT rebuilt (Lean, cargo)>.

Result: N nodes FULL, N NARROWED, N OVERCLAIM. No node was raised.

Corrections to the PR's own text:
- <NODE>: the text says X; the Lean says Y (file:line). Corrected to Y.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|

## Scanner output
HIGH/MEDIUM findings handled; findings not decided; baseline entries proposed (with reason).
```

## What the scanner cannot decide

Whether a statement means what its Lean type says; whether a `decide` over a closed instance is the whole claim; whether an imported Lean lemma hides a hypothesis; whether a number outside any cited file is correct; the import closure of a module for R3; prose that avoids the hedge words yet overclaims; claims in papers that name no node id; and anything in the atlas that is not in this checkout. These are the human-judgement step.
