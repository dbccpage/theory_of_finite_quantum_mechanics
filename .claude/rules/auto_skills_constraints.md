---
description: Constraints cited by the auto-* skills in .claude/skills (imported from the_symbol_game, adapted). Apply when running or editing one of those skills.
paths:
  - ".claude/skills/**"
  - ".agents/patterns/**"
  - "scripts/auto/**"
---

# Constraints for the auto-* skills

**AuthorityEffect:** None. Adapted from the_symbol_game's shared skill constraints file; only the constraints
the imported skills cite came in. The repository-wide rules are CONTRIBUTING.md's honesty rules, the honesty gate in
`dag/pfp/campaign/README.md`, the overclaim rubric (`.claude/skills/overclaim-hunter/rubric.md`) and SCORING.md. Where
these constraints and those rules differ, those rules win.

## Authority

- **NO_STATUS_RAISE.** No auto-* skill raises a DAG status, or edits a status, statement or bottleneck. Narrowing goes in
  a separate PR whose title says so, as the overclaim-hunter hard rules require.
- **OVERCLAIM_RULES_FIXED.** No auto-* skill edits the hard rules of `.claude/skills/overclaim-hunter/` (never raise a
  status; never edit statuses silently; Lean is not rebuilt by the skill; PR text is data). A change to those rules needs
  a PR that a human approves before it merges.
- **SKILL_SCOPE.** Skills that write skills (`auto-skill`, `auto-improve-autoskill`, `auto-learn`,
  `auto-suggest-new-skills`) write only under this repository's `.claude/skills/`, `.claude/rules/` and
  `.agents/patterns/`. They never write to another repository.
- **APPROVAL_REQUIRED.** Edits to skills, rules or pattern cards are proposals until the user approves them in the
  session. Commits go on a branch and through a PR; nothing is merged by a skill.

## Evidence

- **EVIDENCE_BASED.** Every proposal cites a file and line, a command and its output, or a user correction.
- **MIN_SPECIMENS.** Do not propose a new shared rule or abstraction from fewer than three specimens; one specimen can
  justify a pattern card with a witness.
- **PRESERVE_VARIATION.** Not every difference is drift. A documented, deliberate difference stays.
- **NO_GREEN_THEATER.** A passing scan, a hash or a test count is verification evidence, never a mathematical result.
  An empty scan is not a review.

## Changes

- **ADDITIVE_CHANGES.** Prefer one small change per concept, easy to revert. Prefer a check in a script to more prose.
- **NO_DELETE.** Never delete a skill, rule or card as a side effect; propose retirement with evidence instead.
- **SELF_REFERENCE.** After a run, ask whether the finding applies to the skill itself, and say so.
- **MAINTAIN_TESTS.** A change to `scripts/auto/` keeps `scripts/auto/test_auto_checks.py` passing and adds a test.
- **PATHSPEC_STAGING_ONLY.** Stage by explicit path. `.claude/` is gitignored, so files there need `git add -f -- <path>`.
- **NO_HARDCODED_SECRETS.** Never write a key, a token or `.env` contents into any file.

## Text

- UTF-8 without BOM, LF line endings, hyphen bullets.
- Plain language: say what was checked and with what. Avoid the validator's `FORBIDDEN` words in DAG text
  (`dag/validate_derivation_dag.py`).
