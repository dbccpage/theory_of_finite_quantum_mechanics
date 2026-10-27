---
name: auto-skill
description: Capture durable lessons from the current session as proposed edits to this repository's skills. Use with /auto-skill or /autoskill, at the end of a long session, after a user correction about how a skill should work, after three or more similar fixes, or after a CI or tool failure a skill should have prevented. Detects signals (corrections, rejected tool calls, repeated errors), proposes HIGH-confidence edits to .claude/skills only, and applies them after the user approves. Not for code fixes (auto-learn) or for new skills (auto-suggest-new-skills).
---

# Auto skill

**AuthorityEffect:** None. This skill covers session learning: signal detection, proposal format, the self-reference
check and the git-tracking check. Constraints: `.claude/rules/auto_skills_constraints.md`.

## Step 1. Detect signals

Scan the session for the signals in [references/signals.md](references/signals.md), highest priority first. Keep only
signals that are explicit, project-specific and likely to recur; drop generic best practice and one-offs.

## Step 2. Map each signal to its owner

Find the skill that should have prevented the problem (`.claude/skills/*/SKILL.md`). If a family of skills shares the
rule (the auto-* skills share `.claude/rules/auto_skills_constraints.md`), the change goes in the shared file once,
with a one-line citation in each skill, not N copies.

## Step 3. Propose

For each edit:

```
File: .claude/skills/<skill>/SKILL.md
Section: <existing section, or "new section: X">
Confidence: HIGH | MEDIUM
Signal: "<the user's words or the failing command>"
Current text: > ...
Proposed text: > ...
Rationale: <one sentence>
```

HIGH first. Prefer compressing (one rule, a template, a script check) to adding prose.

Git-tracking check: `.claude/` is gitignored. Tell the user that an edited skill is committed with
`git add -f -- .claude/skills/<skill>/SKILL.md`, or it stays local.

## Step 4. Self-reference check

Do any signals concern how this skill detects signals, or did the user correct this skill? If so, include a proposal
for this file, and flag `auto-improve-autoskill` when two or more self-edits come up in one session.

## Step 5. Apply

Apply only what the user approves, then run `python -I -X utf8 scripts/auto/estate_audit.py skills` and fix any HIGH
finding the edit introduced.

## Boundaries

- Edits only `.claude/skills/` (and the shared constraints file when the rule is shared). Never another repository.
- Never edits the overclaim-hunter hard rules, and never proposes a change that would let a skill raise a status,
  certify its own output or skip the statement-vs-theorem review. Those need a PR a human approves.
- A passing test, a hash or a clean scan is evidence, never a mathematical result; no proposal may say otherwise.
- Invent no new goals: every proposal traces to a signal from this session.
