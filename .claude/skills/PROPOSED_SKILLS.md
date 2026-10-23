# Proposed skills

**AuthorityEffect:** None. Ranked proposals from `auto-suggest-new-skills`. A proposal is not a skill; it becomes one only
after the user approves it. Last refresh: 2026-10-23.

### dag-sync

- Date: 2026-10-23
- Source: first test run of auto-suggest-new-skills, during the auto-skills import; `dag/derivation_dag_reading_note.md`
  and the "Pipeline after any DAG change" section of `dag/pfp/campaign/README.md`
- Gap: every DAG change runs the fragment sync scripts in a fixed order, then the validator, the evidence pages and the
  README facts. The order is written in two documents and was the subject of earlier session lessons (sync order,
  receipt re-pin); no skill runs it.
- Overlaps: `overclaim-hunter` (reviews the result, does not sync), `auto-docs` (checks generated docs only).
- Confidence: MEDIUM
- Status: PROPOSED

### derivation-note-link-repair

- Date: 2026-10-23
- Source: `estate_audit.py docs` whole-checkout run in the import audit
  (`docs/overclaim/reviews/2026-10-23_auto-skills-import_audit.md`, section 5)
- Gap: 2364 relative links in 366 notes under `dag/derivations/` do not resolve; 2363 of them start with `../../`,
  which from `dag/derivations/<segment>/` lands inside `dag/`. Whether one more `../` repairs each was not checked
  (some targets, such as `code/lean4/`, do not exist at any depth). A generator fix or a repair script is the likely
  remedy, so this may be better as a `scripts/` change than a skill.
- Overlaps: `auto-docs` (finds the links, does not repair them).
- Confidence: LOW (likely a script, not a skill)
- Status: PROPOSED
