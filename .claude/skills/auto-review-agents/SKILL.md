---
name: auto-review-agents
description: Review the agent definitions in this repository for structure and authority safety. Use when cleaning up agents, after adding a .claude/agents or .agents/agents file, and in the audit umbrella when one changed. Runs scripts/auto/estate_audit.py agents (front matter, name matching the file, broken links, authority-unsafe wording such as "self-certify" or "raise a status"), then rates relevance by hand. Proposes archiving; never archives or deletes.
---

# Agent review

**AuthorityEffect:** None. This repository has no agent definitions today. Constraints: `.claude/rules/auto_skills_constraints.md`.

## Step 1. Scan

```
python -I -X utf8 scripts/auto/estate_audit.py agents --fail-on none
```

Roots: `.claude/agents/*.md` and `.agents/agents/*.md` (front matter `name` and `description`; `name` equals the file
stem). An empty root is valid data, not a pass of anything.

| Rule | Sev | Meaning |
|---|---|---|
| INVALID_FRONT_MATTER, MISSING_FIELD, NAME_PATH_MISMATCH | HIGH | the definition cannot be loaded as written |
| NAME_FORMAT, DESCRIPTION_LENGTH | MEDIUM | the name or trigger description is malformed |
| AUTHORITY_UNSAFE | MEDIUM | wording such as "self-certify", "approve its own", "raise a status", "promote a status", "admitted automatically" or "without review" (sentences that forbid or hunt for these, and quoted mentions, are skipped) |
| FOREIGN_PATH | HIGH | a path into a source tree that is not in this repository |
| BROKEN_LINK, MISSING_PATH | MEDIUM, LOW | a link or cited path that does not resolve |

## Step 2. Rate each agent or brief

For each: relevance (5 used weekly ... 1 never), unique value (5 hard-won repository knowledge ... 1 generic), whether
its authority is bounded (it proposes, a host check or a human decides: CONTRIBUTING.md honesty rule 1), and whether
another agent or skill duplicates it. Recommend KEEP, IMPROVE, CONSOLIDATE or ARCHIVE, citing the evidence.

Teamwork briefs are records of past runs. Recommend archiving one only if nothing links to it and its handoff has been
folded into a DAG record or review.

## Output

```
# Agents audit, <date>
Summary: N definitions, N briefs; keep N, improve N, archive candidates N.
Findings (scanner): ...
Recommendations: <agent>: <KEEP|IMPROVE|CONSOLIDATE|ARCHIVE>: <evidence>
```

In the audit umbrella this goes into the consolidated report.

## Rules for this skill

- Archive or delete nothing; recommendations need the user's approval and go in a PR.
- If agents disagree on an evidence, test or authority rule, hand it to `auto-symmetry-hunter`; do not patch here.
- Run `auto-review-skills` alongside when a cleanup covers both.
