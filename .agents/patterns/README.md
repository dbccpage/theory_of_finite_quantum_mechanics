# Pattern catalog

**AuthorityEffect:** None. A card describes a failure class and its repair. It changes no status and certifies nothing.

Each card is written for this repository's paths and rules.

## Layout

- `anti/<language>/AP_<ID>_<words>.md`: an anti-pattern, with a `dual_pattern` naming its healthy pattern.
- `helpful/<language>/HP_<ID>_<words>.md`: the repair, with a `dual_pattern` naming the anti-pattern back.
- Languages: `lean4`, `python`, `rust`, `markdown` (prose and DAG records), `math` (claims and certificates).

`python -I -X utf8 scripts/auto/anti_pattern_lint.py --catalog-only` checks the layout: every slot exists, every card
name matches its `pattern_id`, and every dual exists and names the card back.

## Cards

| Id | Language | Class | Mechanical check |
|---|---|---|---|
| `AP_LN_001` | lean4 | Unmechanized sorry proof claim | `scripts/auto/anti_pattern_lint.py` rule AP_LN_001 (added lines with `--changed-since`; every line otherwise); `scripts/overclaim_scan.py` rule R3 for modules cited by a PROVED_LEAN or CONDITIONAL node. |
| `AP_LN_002` | lean4 | Unconstrained Lake Mathlib rebuild | none; read by hand. |
| `AP_LN_004` | lean4 | Smuggled custom axiom | `scripts/auto/anti_pattern_lint.py` rule AP_LN_004; `scripts/overclaim_scan.py` rules R3 and R4. |
| `AP_PY_001` | python | Blanket type ignore | `scripts/auto/anti_pattern_lint.py` rule AP_PY_001 (LOW). |
| `AP_PY_006` | python | Host-absolute path in code | `scripts/auto/anti_pattern_lint.py` rule AP_PY_006 (string literals in non-test Python). |
| `AP_PY_009` | python | Stale binding hash | partly `scripts/overclaim_scan.py` rule R4 (replay receipts) and `scripts/contract_scores.py check` (companion history bytes); otherwise by hand. |
| `AP_PY_019` | python | Tautological test | `scripts/auto/anti_pattern_lint.py` rule AP_PY_019 (an assert over constants only; `pytest.raises` around a bare `raise`). |
| `AP_MATH_006` | math | Bounded check, unbounded claim | partly `scripts/overclaim_scan.py` rule R2 (universal wording over closed instances); otherwise the statement-vs-theorem review. |
| `AP_MATH_011` | math | Floating point in an exact certificate | `scripts/auto/anti_pattern_lint.py` rule AP_MATH_011 (float literals, `float()`, `math.*` and `.evalf()` in `checks/independent/`). |
| `AP_MATH_022` | math | Premature triumph promotion | partly `scripts/overclaim_scan.py` rules R6 and R7; otherwise by hand. |
| `AP_MD_006` | markdown | Unchecked edge as proof | partly `scripts/auto/obstruction_scan.py` rule O3 (a derived route with an OPEN or REFUTED input). |
| `AP_MD_022` | markdown | Axiom lines stand in for a failed build | none; read by hand. |
| `AP_RS_001` | rust | Cargo target duplicated per worktree | none; read by hand. |

A card with no mechanical check is read by hand in the `auto-code-anti-pattern-hunter` pass. The repository-wide rules
these cards serve are CONTRIBUTING.md's honesty rules, the honesty gate of `dag/pfp/campaign/README.md`, the overclaim
rubric (`.claude/skills/overclaim-hunter/rubric.md`) and SCORING.md.

## Adding a card

Add a card only from a concrete failure seen in this repository (the `auto-learn` skill), with its dual, in one PR.
A card with a mechanical check names the rule id of the script that implements it.
