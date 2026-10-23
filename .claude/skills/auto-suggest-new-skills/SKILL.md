---
name: auto-suggest-new-skills
description: Suggest new skills for this repository from recurring work in the session, the review files and the campaign protocol. Use when asked what skills to add, after the same multi-step workflow was done by hand several times, or at the end of an audit run. Deduplicates against .claude/skills, writes ranked proposals to .claude/skills/PROPOSED_SKILLS.md, and drafts a skill package only after the user approves. Never admits a skill automatically and never searches external registries unless asked.
---

# Suggest new skills

**AuthorityEffect:** None. Imported from the_symbol_game `auto-suggest-new-skills`, adapted. The source admitted
skills automatically and mirrored them to four host roots; here a suggestion stays a proposal until the user approves
it, and there is one host root (`.claude/skills/`). The God-run receipts, Algorithm Prime 000 protocol and paper outline
were not ported. Constraints: `.claude/rules/auto_skills_constraints.md`.

## Step 1. Find the capability gap

Sources, in this order:

1. The session: a workflow done by hand three or more times (MIN_SPECIMENS), a repeated failure, a request no skill
   covers.
2. The review files `docs/overclaim/reviews/*.md`: "What the scanner could not decide" sections that recur.
3. The protocols: `dag/pfp/campaign/README.md`, `dag/derivation_dag_reading_note.md` (the sync order), CONTRIBUTING.md
   and REVIEWING.md. A multi-step procedure there with no skill is a candidate.

External registries or papers only if the user asks; no paid provider calls.

## Step 2. Deduplicate

Compare with every `.claude/skills/*/SKILL.md` and with `.claude/skills/PROPOSED_SKILLS.md`. Prefer extending an
existing skill, or a `scripts/auto/` check, to a new skill.

## Step 3. Fence authority

Reject a candidate that would raise statuses, certify model output, skip the statement-vs-theorem review or weaken the
overclaim-hunter hard rules.

## Step 4. Record the proposal

Append to `.claude/skills/PROPOSED_SKILLS.md` (create it if absent):

```
### <skill-name>
- Date: YYYY-MM-DD
- Source: <session, review file or protocol section>
- Gap: <what is done by hand today, with the evidence>
- Overlaps: <existing skills checked>
- Confidence: HIGH | MEDIUM | LOW
- Status: PROPOSED
```

Rank the file HIGH before MEDIUM before LOW. A superseded proposal is marked, not deleted.

## Step 5. Draft, on approval only

When the user approves a proposal: write `.claude/skills/<name>/SKILL.md` with front matter (`name` equal to the
directory, a precise trigger `description`), run `python -I -X utf8 scripts/auto/estate_audit.py skills`, change the
proposal's status to DRAFTED, and commit with `git add -f -- <paths>` in a PR.

## Boundaries

- Writes only `.claude/skills/`. A new skill grants no authority and makes no claim true.
- No retirement or deletion here; that is `auto-review-skills` with evidence and the user's decision.
