---
name: auto-obstruction-hunter
description: Find places in this repository where two records do not fit, from a sentence up to the derivation DAG. Use in the audit umbrella, after a DAG sync, or when asked to "find obstructions" or "where does it not fit". Runs scripts/auto/obstruction_scan.py (an independent check that imports repository code, a module-level import cycle, a derived DAG route that needs an OPEN or REFUTED input) and then walks the levels by hand. Reports non-fits; does not choose which side is wrong and changes no status.
---

# Obstruction hunter

**AuthorityEffect:** None. The scanner is a standard-library import graph; the levels below are this repository's.
Constraints: `.claude/rules/auto_skills_constraints.md`.

An obstruction is a non-fit: two records that cannot both be right as written. The hunter finds it and states both
sides. It does not pick the repair.

## Step 1. Scan

```
python -I -X utf8 scripts/auto/obstruction_scan.py --changed-since origin/main     # a change
python -I -X utf8 scripts/auto/obstruction_scan.py --fail-on none                  # the whole checkout (minutes: it parses every Python file)
python -I -X utf8 scripts/auto/obstruction_scan.py --only O3 --fail-on none        # the DAG only (seconds)
```

| Rule | Sev | Non-fit | What to do |
|---|---|---|---|
| O1 | HIGH | `checks/independent/*.py` imports a repository module or uses a relative import (MEDIUM: edits `sys.path`) | CONTRIBUTING.md: an independent check does not import repository code. Inline what it needs. |
| O2 | MEDIUM | a cycle of module-level imports among repository Python files | Break the cycle or move the shared part down. |
| O3 | MEDIUM | a `DERIVED_LEAN`, `DERIVED_PROSE` or `COMPUTED` route with an `OPEN` or `REFUTED` input | A route requires all of its inputs (`edge_semantics` in `dag/derivation_dag.json`). Read the output's proof: if it does not use the input, the route lists a spurious input; if it does, the output claims more than its inputs hold. Hand the node to `overclaim-hunter`. |

With `--changed-since`, O1 and O2 look at the changed Python files (and files they import), and O3 at routes touching
a node or route that differs from the base.

## Step 2. Walk the levels by hand

Use only the levels the change touches.

| Level | Locus in this repository | Non-fit to look for |
|---|---|---|
| 0 | names, encoding | a file name or id that differs between the DAG, the Lean module and the check; mojibake |
| 1 | node ids in prose | an id in README, docs or papers that is not a DAG node |
| 2 | node `statement` vs `bottleneck` | the bottleneck says something is open that the statement asserts |
| 3 | derivation notes (`dag/derivations/**`) | the note's conclusion differs from the node statement |
| 4 | modules | O1, O2 |
| 5 | data records | a replay receipt or contract companion naming a different source than the node cites |
| 6 | functions | a Lean theorem whose hypotheses are wider or narrower than the node's statement (hand to `overclaim-hunter`) |
| 7 | tests and checks | a check that tests a copied table instead of the formula (overclaim failure class 3) |
| 8 | DAG segments | `see_also` nodes that cover the same question with different statuses |
| 9 | the derivation spine | O3; a PROVED node whose every route rests on an open input |

## Output

For each obstruction: the two records (file:line each), the sentence that says why they do not fit, and the owner who
can decide (`overclaim-hunter`, a DAG fragment, or the module author). In the audit umbrella these rows go into the
consolidated report.

## Rules for this skill

- Never select a repair and never edit a status or a route. A route correction is a DAG change through the owning
  fragment and the sync order in `dag/pfp/campaign/README.md`.
- No Lean build, no cargo. Say "not rebuilt" where a receipt is relied on.
