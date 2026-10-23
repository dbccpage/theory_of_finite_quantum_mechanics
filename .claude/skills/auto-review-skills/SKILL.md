---
name: auto-review-skills
description: Review the skills in this repository's .claude/skills for structure, broken references, foreign paths, authority-unsafe wording, overlap and use. Use after adding or editing a skill, when cleaning up skills, and in the audit umbrella when a skill changed. Runs scripts/auto/estate_audit.py skills, then reviews overlap and usage evidence by hand. Proposes consolidation or retirement in a PR with evidence; never archives or deletes.
---

# Skill review

**AuthorityEffect:** None. Imported from the_symbol_game `auto-review-skills`, adapted: the skill compiler, usage
ledger, registry files and four-host mirrors it audits do not exist here. Constraints:
`.claude/rules/auto_skills_constraints.md`.

## Step 1. Scan

```
python -I -X utf8 scripts/auto/estate_audit.py skills
```

It reads every `.claude/skills/*/SKILL.md` (and `.agents/skills/*/SKILL.md` if that root appears) from the filesystem,
so a skill not yet force-added to git is still checked, plus each skill's other Markdown files.

| Rule | Sev | Meaning |
|---|---|---|
| INVALID_FRONT_MATTER, MISSING_FIELD, NAME_PATH_MISMATCH | HIGH | Claude Code cannot load the skill under its directory name |
| FOREIGN_PATH | HIGH | the skill tells the reader to act on a the_symbol_game path |
| NAME_FORMAT, DESCRIPTION_LENGTH | MEDIUM | name not lowercase-hyphenated within 64 characters; description outside 40 to 1024 characters |
| AUTHORITY_UNSAFE | MEDIUM | wording such as "self-certify", "raise a status" or "admitted automatically", outside a negated sentence or a quoted mention |
| BROKEN_LINK | MEDIUM | a relative link that does not resolve |
| MISSING_PATH, NO_SECTIONS | LOW | a cited path that does not exist; a body with no `##` section |

## Step 2. Review by hand

1. Trigger quality: does the description say when to use the skill and when not, precisely enough that it fires on the
   right request and not on a neighbour's?
2. Overlap: two skills with the same trigger. Prefer folding one into the other.
3. Hard rules: no skill may weaken the overclaim-hunter hard rules or the constraints file.
4. Use: state what usage evidence exists (session transcripts, review files under `docs/overclaim/reviews/`, PR
   comments). Git modification time and reference counts are not usage telemetry; with no evidence, usage is UNKNOWN.

## Output

Scanner findings, then one line per skill: KEEP, IMPROVE (what), CONSOLIDATE (into what) or RETIRE-CANDIDATE (evidence).
In the audit umbrella this goes into the consolidated report.

## Rules for this skill

- No archival or deletion as a side effect. A retirement proposal is a focused PR with evidence; deletion needs the
  user's decision.
- `.claude/` is gitignored: a skill edit is committed with `git add -f -- <path>`.
