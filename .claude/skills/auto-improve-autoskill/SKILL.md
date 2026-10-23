---
name: auto-improve-autoskill
description: Audit what the learning skills (auto-skill, auto-learn, auto-suggest-new-skills) proposed or changed in this repository, and weaken any claim that exceeds its evidence. Use when auto-skill flags it, before a PR that edits skills, rules or pattern cards, and when asked why a lesson was missed or to audit the learner. Classifies every claim, checks for authority creep and receipts sold as results, and returns PASS, PATCH, VETO or BLOCKED. Edits only .claude/skills, .claude/rules and .agents/patterns, never the overclaim-hunter hard rules.
---

# Improve the learner

**AuthorityEffect:** None. Imported from the_symbol_game `auto-improve-autoskill`, adapted: the residual-mass and
symmetry-restoration gates, the Lean axiom-graph regeneration and the budget gate are OE machinery and were not ported;
the claim vocabulary was mapped to this repository's statuses. Constraints: `.claude/rules/auto_skills_constraints.md`.

This skill keeps the learning skills honest. It can weaken or reject what they produce; it never strengthens a claim.

## Step 1. Collect the specimen

The diff of `.claude/skills/`, `.claude/rules/`, `.agents/patterns/` and `scripts/auto/` since the base, plus the
proposals in the session.

## Step 2. Classify every claim

Each claim in the specimen is one of:

| Class | Meaning here |
|---|---|
| process rule | how to run a skill or a check; no mathematical content |
| supplied datum | an input taken from outside (a source, a user statement) |
| imported assumption | structure supplied, not derived (DAG status IMPORTED_ASSUMPTION) |
| definition | a DAG DEFINITION or a code constant |
| theorem | stated by a Lean declaration in this repository that compiles with only the three allowed axioms (PROVED_LEAN under the honesty gate) |
| finite computation | an exact independent check (COMPUTATIONALLY_CHECKED) |
| countermodel | an explicit witness against a claim (REFUTED) |
| open | not proved; with its bottleneck |

Receipts, hashes, test counts, scan results and coverage are evidence about artefacts. They are never a theorem or a
finite computation in this table. An unclassifiable claim is rejected.

## Step 3. Negative checks

- **Authority creep:** does any change give a skill one of these powers: "raise a status", "admit its own output",
  "skip the statement-vs-theorem review", or editing the overclaim-hunter hard rules? Run `python -I -X utf8 scripts/auto/estate_audit.py skills` and read
  every AUTHORITY_UNSAFE finding. Any such change is VETO.
- **Laundering:** does a passing check or receipt stand in for a proof anywhere in the new text? VETO.
- **Placebo change:** a reformat, a restated rule or an added sentence that changes no behaviour and no check, offered
  as an improvement. PATCH (drop it) or VETO.
- **Loosened gate:** a weaker scanner rule, a lowered severity, a widened exclusion or a removed test. VETO unless the
  user asked for it with a reason.
- **Lean honesty** (when the specimen touches Lean or receipts): `scripts/auto/anti_pattern_lint.py --changed-since
  origin/main` and `scripts/overclaim_scan.py --changed-since origin/main --strict`. Do not rebuild Lean.

## Step 4. Weaken

Rewrite prose that exceeds its evidence: "proves" to the status the DAG records, "guarantees" to "checks, for the
stated bound", "all" to the bound actually checked. Use the validator's `FORBIDDEN` list as the floor.

## Report

```
# auto-improve-autoskill report
Verdict: PASS | PATCH | VETO | BLOCKED
Claim classification: ...
Negative checks: authority creep / laundering / placebo / loosened gate / Lean honesty
Weakened text: file:line, before, after
Requires user approval: yes
```

## Boundaries

- Recommendations only; the user approves and a PR carries the change.
- Never loosens an existing check, size ceiling or severity on its own initiative.
- Failure modes seen before: [references/failure_modes.md](references/failure_modes.md).
