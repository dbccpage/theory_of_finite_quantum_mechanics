---
name: audit
description: Umbrella quality gate for this repository. Use before merging a PR, after a derivation-campaign batch, weekly on main, or when asked to "audit" a change or run every check. Runs overclaim-hunter first (claims vs proofs), then the auto-* hunters that apply to the change (obstruction, symmetry, anti-pattern lint and hunter, docs, agent and skill review), and writes one consolidated report to docs/overclaim/reviews/<date>_<scope>_audit.md plus a PR comment. Raises no status and merges nothing.
---

# Audit

**AuthorityEffect:** None. Orchestrates existing skills; adds no rule of its own. Every hard rule of
[overclaim-hunter](../overclaim-hunter/SKILL.md) applies to the whole run, and the auto-* constraints are in
`.claude/rules/auto_skills_constraints.md`. A clean audit is not a proof of anything: each stage says what it cannot
decide.

## Step 0. Scope

Pick the scope label: `pr-<n>`, `campaign-batch-<k>` or `weekly`. For a PR, check it out in a scratch worktree, never
in your working tree, exactly as overclaim-hunter Step 1 says (run git commands one at a time), and remove the worktree
afterwards. For `weekly`, run on an up-to-date `main`. Below, `<diff-flags>` is `--changed-since origin/main` for a PR or
batch and empty for weekly.

List the changed files once (`git diff --name-only origin/main...HEAD`); the table in Step 2 uses it.

## Step 1. Claims vs proofs: overclaim-hunter

Run [overclaim-hunter](../overclaim-hunter/SKILL.md) Steps 1 to 3 in full: the scan, the statement-vs-theorem review
of every flagged node and every node whose status or statement changed, and the exact recomputation of every number.
Nothing later in this skill replaces or shortens that review. Its findings become section 1 of the consolidated report,
in the overclaim review template (`rubric.md`, "Review file template"), so a separate `<date>_<scope>.md` file is not
needed for the same scope.

## Step 2. The hunters that apply

Run each row whose trigger matches the changed files (all rows for `weekly`). Mechanical commands first, then the
skill's by-hand step.

| Stage | Trigger | Mechanical command | Skill |
|---|---|---|---|
| 2a | always | `python -I -X utf8 scripts/auto/obstruction_scan.py <diff-flags> --fail-on none` | [auto-obstruction-hunter](../auto-obstruction-hunter/SKILL.md) |
| 2b | always (cheap); by hand when CONTRIBUTING.md, REVIEWING.md, the campaign README, a skill, a rule, a pattern card, `scripts/overclaim_scan.py` or `dag/validate_derivation_dag.py` changed | `python -I -X utf8 scripts/auto/symmetry_scan.py <diff-flags> --fail-on none` | [auto-symmetry-hunter](../auto-symmetry-hunter/SKILL.md) |
| 2c | always | `python -I -X utf8 scripts/auto/anti_pattern_lint.py <diff-flags> --fail-on none` | [auto-anti-pattern-lint](../auto-anti-pattern-lint/SKILL.md) |
| 2d | Lean, Python, independent checks, replay receipts, companions or DAG prose changed | (2c's output) | [auto-code-anti-pattern-hunter](../auto-code-anti-pattern-hunter/SKILL.md) |
| 2e | Markdown or scripts changed | `python -I -X utf8 scripts/auto/estate_audit.py docs <diff-flags> --fail-on none`, then `scripts/build_readme_facts.py --check` | [auto-docs](../auto-docs/SKILL.md) |
| 2f | an agent definition changed (`.claude/agents/`, `.agents/agents/`) | `python -I -X utf8 scripts/auto/estate_audit.py agents --fail-on none` | [auto-review-agents](../auto-review-agents/SKILL.md) |
| 2g | a skill or rule changed (`.claude/skills/`, `.claude/rules/`) | `python -I -X utf8 scripts/auto/estate_audit.py skills --fail-on none` | [auto-review-skills](../auto-review-skills/SKILL.md) and, for a learner's output, [auto-improve-autoskill](../auto-improve-autoskill/SKILL.md) |

A stage that does not apply is listed in the report as "not run: no matching change". A stage that could not run (a
missing tool, an error exit 2) is listed as "could not run" with the error, never as clean.

Any node a hunter flags (an O3 route, an `AP_MATH_*` card, a symmetry break about a status) goes back to Step 1's
statement-vs-theorem table; the hunters do not give node verdicts.

## Step 3. One consolidated report

Write `docs/overclaim/reviews/<YYYY-MM-DD>_<scope>_audit.md`:

```
# Audit of <scope>

Scope: <PR/batch/weekly, commit, base>. Stages run: <list>; not run: <list, reason>.
Method: <commands and their versions or commit>; not rebuilt: Lean, cargo.
Result: overclaim N FULL, N NARROWED, N OVERCLAIM; hunters N HIGH, N MEDIUM, N LOW. No node was raised.

## 1. Claims vs proofs (overclaim-hunter)
<the overclaim review template: corrections, per-node table, numbers recomputed, scanner output>

## 2. Obstructions
## 3. Symmetry breaks
## 4. Anti-patterns
## 5. Documentation
## 6. Agents and skills
<each: the table the skill's Output section defines, or "not run: ...">

## What no stage could decide
```

Lead each section with the worst finding. After writing, run
`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` again: the report lives under
`docs/` and must not itself add a finding (no node called proved beyond its status, no promotional wording).

For a PR, post it: `gh pr comment <n> --body-file docs/overclaim/reviews/<file>.md`. Do not approve, merge or push to
the PR branch.

## Step 4. Afterwards (optional, once)

- Corrections the report proposes go in a separate, clearly titled PR from `origin/main`, narrowing only (overclaim-hunter
  Step 4).
- If the run exposed a recurring problem, run [auto-learn](../auto-learn/SKILL.md) once with it. Learning does not start
  another audit.
- If a by-hand step recurred across audits, note it for [auto-suggest-new-skills](../auto-suggest-new-skills/SKILL.md).

## Output to the user

Overclaim verdict counts first, then the HIGH findings of every stage, the stages not run, and what no stage could
decide.
