---
name: auto-learn
description: Turn one concrete correction or failure from the current session into the smallest durable change in this repository (a code fix, a skill or rule edit, or a new .agents/patterns card), then recheck the original task. Use with /auto-learn <task or observation>, at the end of an audit run that found a recurring problem, or after a user correction worth keeping. Scoped to this repository's .claude/skills, .claude/rules, .agents/patterns and the code the task touched; never changes a DAG status or the overclaim-hunter hard rules.
---

# Auto learn

**AuthorityEffect:** None. Imported from the_symbol_game `auto-learn`, adapted: the OE lesson stores, host mirroring,
Woland finish hook and the automatic repair engine (`--repair` for markdown bullets and mypy codes) were not ported.
The candidate-admission boundary of the_symbol_game `auto-anti-skill` is folded in (Step 4). Constraints:
`.claude/rules/auto_skills_constraints.md`.

The outcome is a useful change to an existing file that the next task will find, not a new report.

## Before work

1. Search the existing owners for the task, the failure and the correction: `.claude/skills/`, `.claude/rules/`,
   `.agents/rules/`, `.agents/patterns/` and the affected code. Open the matching entries only.
2. Check whether the source changed since a lesson was written before trusting it. Reuse the existing owner; do not add
   a parallel rule.
3. Put the relevant lesson paths in the brief of any worker you spawn.

## Learn, apply, recheck

1. **Name the obstruction.** A rejected input, a wrong output, a failed assumption, a tool failure or a user correction,
   with its witness (command and output, file:line, or the user's words). A file name, a PASS label or agreement
   between agents is not a witness.
2. **Explain it.** Failure, cause (observed or only hypothesised: say which), correction, the check that shows the
   correction works, where it applies and its exceptions.
3. **Choose the smallest high-confidence change** in the task's scope: fix the code; edit the owning skill or rule; or
   add an anti/healthy card pair under `.agents/patterns/<language>/` (format: `.agents/patterns/README.md`). Prefer a
   check in `scripts/auto/` over more prose when the signature is mechanical, with a test in
   `scripts/auto/test_auto_checks.py`. If no reusable change is justified, say so; do not manufacture one.
4. **Candidates are not rules.** A pattern seen once is a card with its witness, not a new shared rule
   (MIN_SPECIMENS). A rule that changes what counts as evidence needs two independent episodes, a clean counterexample
   and the user's approval.
5. **Recheck the original need** against the changed file with the smallest relevant check: the test, the scanner, or
   rereading the corrected text. Report exactly what ran. Never change a receipt, a pin or an assertion to make a check
   pass.
6. **Carry over.** Put the applied paths, the recheck and anything unresolved in the reply and in the next worker's
   brief.

## Boundaries

- Writes only under `.claude/skills/`, `.claude/rules/`, `.agents/patterns/`, `scripts/auto/` and the files of the task
  at hand. Never another repository.
- Never edits a DAG status, statement or bottleneck, and never the hard rules of `.claude/skills/overclaim-hunter/`;
  those go to a PR a human approves.
- One run per outer task. Applying a lesson and rechecking it does not start another auto-learn run.
- No new receipt, log or `lessons.json` for routine learning. Keep the knowledge in the owner file.
- Never copy keys, environment dumps or private conversation text into a learned file.
