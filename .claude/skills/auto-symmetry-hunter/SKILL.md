---
name: auto-symmetry-hunter
description: Detect drift between copies of the same rule in this repository. Use in the audit umbrella, when a PR edits CONTRIBUTING.md, the campaign README, the overclaim skill, a skill or rule file, or the constants in scripts/overclaim_scan.py or dag/validate_derivation_dag.py, and when asked for a drift or cross-file invariant audit. Runs scripts/auto/symmetry_scan.py (allowed axioms, forbidden Lean tokens, status order, forbidden words) then compares other restated rules by hand. Classifies each break; does not pick which copy changes.
---

# Symmetry hunter

**AuthorityEffect:** None. The invariants it checks are the ones this repository restates. Constraints: `.claude/rules/auto_skills_constraints.md`.

A symmetry break is a rule stated in two places that no longer agree. Declare the correspondence first (which copy
corresponds to which), then compare. File names, PR numbers and proximity do not by themselves establish that two texts
state the same rule.

## Step 1. Scan

```
python -I -X utf8 scripts/auto/symmetry_scan.py --changed-since origin/main
python -I -X utf8 scripts/auto/symmetry_scan.py --fail-on none
```

The reference copy of each invariant is the code that enforces it:

| Invariant | Enforcing code | Prose copies (examples) |
|---|---|---|
| Allowed Lean axioms | `ALLOWED_AXIOMS` in `scripts/overclaim_scan.py` | CONTRIBUTING.md rule 3, `dag/pfp/campaign/README.md`, overclaim skill and rubric, `HP_LN_001` |
| Forbidden Lean tokens | `LEAN_ADMISSION_TOKENS` plus axiom declarations in `scripts/overclaim_scan.py`; `LEAN_FORBIDDEN` in `scripts/auto/anti_pattern_lint.py` | CONTRIBUTING.md rule 5, the campaign honesty gate, `AP_LN_001` |
| Status order | `PFP_STATUS_RANK` in `dag/validate_derivation_dag.py` | the overclaim rubric's honesty rule |
| Forbidden DAG words | `FORBIDDEN` in `dag/validate_derivation_dag.py` | CONTRIBUTING.md rule 8, the rubric's verdict wording |

The scanner reads prose with heuristics (a sentence that lists two allowed axioms and says "only"; a line that says the
validator refuses words and lists three or more quoted words). Read every finding in context before classifying it.

## Step 2. Compare by hand

Rules the scanner does not read, restated in more than one place:

- The honesty gate and the definition of FULL / NARROWED / OVERCLAIM: CONTRIBUTING.md, the campaign README,
  `.claude/skills/overclaim-hunter/SKILL.md` and `rubric.md`, REVIEWING.md.
- The DAG sync order: `dag/derivation_dag_reading_note.md` and the campaign README.
- The auto-* constraints: `.claude/rules/auto_skills_constraints.md` and each auto-* skill that cites them.

## Classify

| Class | Meaning | Action |
|---|---|---|
| INTENTIONAL_VARIANCE | a documented, deliberate difference | keep; cite where it is documented |
| BENIGN_VARIANCE | wording only | keep |
| MISSING_PROPAGATION | a copy omits an item the enforcing code has | propose adding it to the copy |
| EXTENSION | a copy adds a stricter item | say whether the code should enforce it |
| DANGEROUS_DRIFT | a copy is weaker than the code (an extra allowed axiom, a missing forbidden token) | fix the copy first |
| CONTRADICTION | two copies disagree on order or membership | escalate to the user |
| STALE_RULE | a copy names a status, path or tool that no longer exists | propose removal |

## Output

One row per break: invariant, the two locations (file:line), class, proposed propagation. In the audit umbrella these
rows go into the consolidated report.

## Rules for this skill

- Never select a repair silently and never edit the overclaim-hunter hard rules; a propagation is a proposal in a PR.
- Prefer one enforcing check over another copy of the prose.
