---
name: auto-code-anti-pattern-hunter
description: Human-judgement pass over the .agents/patterns cards for a change in this repository. Use after auto-anti-pattern-lint, in the audit umbrella, or when asked to hunt anti-patterns in Lean, Python, Rust, independent checks or DAG prose. Reads every card that applies to the changed files, including the ones with no mechanical signature (bounded check behind an unbounded claim, stale binding hash, axiom lines from a failed build, duplicated cargo targets), and reports findings with file:line. Does not edit code or statuses.
---

# Code anti-pattern hunter

**AuthorityEffect:** None. Imported from the_symbol_game `auto-code-anti-pattern-hunter`, adapted: the four
language-specialist skills it dispatched to do not exist here, so their scope is the card catalog in
`.agents/patterns/`. Constraints: `.claude/rules/auto_skills_constraints.md`.

Each anti-pattern card (`anti/`) has a dual healthy pattern (`helpful/`). Finding the anti-pattern and confirming the
healthy pattern are the same check read two ways, so this skill does both.

## Step 1. Mechanical pass

Run `auto-anti-pattern-lint` on the same scope and keep its output. Its findings are the starting list.

## Step 2. Pick the cards

List the changed files (`git diff --name-only origin/main...HEAD`), then read the cards for their languages:

| Changed | Cards to read by hand |
|---|---|
| `lean4/**/*.lean` | `AP_LN_001`, `AP_LN_002`, `AP_LN_004`; and `AP_MD_022` if a replay receipt changed |
| `checks/independent/*.py` | `AP_MATH_011`, `AP_MATH_006` |
| `dag/derivation_dag.json`, `dag/derivations/**`, README, docs, papers | `AP_MATH_006`, `AP_MATH_022`, `AP_MD_006` |
| `dag/research/*lean_replay*.json`, `*.contract.score.yaml` | `AP_PY_009`, `AP_MD_022` |
| any test file | `AP_PY_019` |
| `code/rust/**` | `AP_RS_001` |
| any Python | `AP_PY_001`, `AP_PY_006` |

The index of cards is `.agents/patterns/README.md`.

## Step 3. Read and decide

For each card: read its detection signature, look for it in the changed lines and their context, and record either a
finding (`file:line`, card id, one sentence of evidence) or "healthy pattern holds" with the reason. For a finding on a
DAG claim (`AP_MATH_006`, `AP_MATH_022`, `AP_MD_006`), do not judge the node here: pass the node id to
`overclaim-hunter` Step 2, which owns statement-vs-theorem review.

## Output

A table: card, file:line, finding or "holds", evidence. Lead with findings. In the audit umbrella this table goes into the
consolidated report.

## Rules for this skill

- Read only; no edits, no status changes, no new cards. A recurring finding with no card goes to `auto-learn`.
- A card's witness is history, not a fresh check. Say what you looked at.
