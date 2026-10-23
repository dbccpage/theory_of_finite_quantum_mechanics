<!--
Fill every section. Write "none" or "not applicable" rather than deleting one.
State what was checked and with what. Do not describe a result as more than the table below shows.
-->

## Outcome class

Tick one.

- [ ] **Prompt result**: a recorded run of a prompt or of the LLM ladder. Changes no node status.
- [ ] **Derived**: the node's full statement is proved from the admitted primitives, with no new imports.
- [ ] **Reduced**: the statement is proved from a strictly weaker, named assumption. The node stays `CONDITIONAL`.
- [ ] **Refuted / not derivable**: a countermodel shows the statement does not follow from the stated primitives.
- [ ] **Narrowed**: a precisely stated special case is proved, and the node statement is narrowed to it.
- [ ] **Review fix**: a change made because of a recorded review (link the issue).
- [ ] **Tooling, docs or process**: no node is affected.

Node id(s):

## Summary

One paragraph: what this changes and why.

## Statement versus theorem

One row per claim in the node statement. The verdict is FULL, NARROWED or NOT PROVED. For a prompt result every row is NOT PROVED.

| Claim in the node statement | Lean declaration or other evidence that proves it (path and name), or "not proved" | Verdict |
|---|---|---|
| | | |

A node becomes `PROVED_LEAN` only if a declaration states its **full** statement and compiles with only `propext`, `Classical.choice` and `Quot.sound`. If any row is not FULL, the statement must be narrowed or the status must stay as it is.

## Contract and score

Every code addition or change needs a `*.contract.score.yaml` companion (see the acceptance rule in `CONTRIBUTING.md`). At this time code is accepted only at capability level L4 or L5 with composite grade D or better; a grade of E, or any unassessed gate, is not accepted. Write "no code in this change" if that is so.

Contract file(s): …; score token: L?G (≥ L4, grade ≥ D)

## Axioms

Paste the `#print axioms` output for each new declaration, or write "no Lean in this change".

```
```

## Check output

Paste the last lines of each command you ran. Delete the ones that do not apply and add others.

```
python -I -X utf8 dag/validate_derivation_dag.py --no-files
python -I -X utf8 scripts/build_readme_facts.py --check
python -I -X utf8 scripts/build_status.py --check
python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict
python -I -X utf8 scripts/score_scope_contracts.py check            # code changes
python -I -X utf8 scripts/contract_scores.py check                  # code changes
python -I -X utf8 checks/independent/your_check.py   # your independent check, if any
lake build YourModule                               # Lean, if any
```

```
```

For a prompt result, also give: the command line (without keys), the summary status and exit code, the models that answered, and the rated cost.

## What is still open

What this change does not establish. For a narrowed or reduced result, the part of the statement that remains. For a prompt result, which claims in the reply were refused or are unverified.

## Checklist

- [ ] I did not raise any node status, or I raised it only under the rule above and the table shows FULL on every row.
- [ ] Added Lean contains no `sorry`, `admit`, `axiom`, `native_decide` or `unsafe`.
- [ ] Every number in prose is recomputed by something in this pull request.
- [ ] No key, token or `.env` content is committed or pasted.
- [ ] Every source file I added or changed has its contract companion, bound to the submitted bytes, with a completed score at L4 or higher and grade D or higher, or this change contains no code.
- [ ] I state which parts, if any, were drafted by a model, and I have read them.
- [ ] I changed only the files this pull request is about.
