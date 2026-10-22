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
python -I -X utf8 checks/independent/<file>.py      # independent check, if any
lake build <Module>                                 # Lean, if any
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
- [ ] I state which parts, if any, were drafted by a model, and I have read them.
- [ ] I changed only the files this pull request is about.
