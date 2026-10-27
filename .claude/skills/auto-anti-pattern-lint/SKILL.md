---
name: auto-anti-pattern-lint
description: Mechanical anti-pattern lint for this repository. Use on every PR (CI runs it), before committing Lean or Python, and inside the audit umbrella. Runs scripts/auto/anti_pattern_lint.py, which checks the .agents/patterns catalog and flags Lean admission tokens or axiom declarations on added lines, blanket type ignores, host-absolute paths, tautological tests and floating point in independent checks. Not for judging cards that have no mechanical signature (use auto-code-anti-pattern-hunter).
---

# Anti-pattern lint

**AuthorityEffect:** None. Constraints: `.claude/rules/auto_skills_constraints.md`.

## Run

A change (what CI runs; blocking on HIGH):

```
python -I -X utf8 scripts/auto/anti_pattern_lint.py --changed-since origin/main
```

The whole checkout (weekly, inside `audit`; report only):

```
python -I -X utf8 scripts/auto/anti_pattern_lint.py --fail-on none
```

The catalog alone: `--catalog-only`. Machine output: `--json`. Exit status: 0 ok, 1 a finding at or above `--fail-on`
(default HIGH), 2 usage or environment error.

## Rules

| Rule | Sev | Signature | Card |
|---|---|---|---|
| AP_LN_001 | HIGH | `sorry`, `admit`, `native_decide`, `unsafe` outside comments and strings (not a constructor name after `\|`); with `--changed-since`, added lines only | `.agents/patterns/anti/lean4/AP_LN_001_unmechanized_sorry_proof_claim.md` |
| AP_LN_004 | HIGH | an `axiom` declaration; added lines only with `--changed-since` | `.agents/patterns/anti/lean4/AP_LN_004_smuggled_custom_axiom_injection.md` |
| AP_PY_006 | MEDIUM | host-absolute path literal in non-test Python | `.agents/patterns/anti/python/AP_PY_006_host_absolute_path_injection.md` |
| AP_PY_019 | MEDIUM | in a test file: assert over constants only, or `pytest.raises` around a bare `raise` | `.agents/patterns/anti/python/AP_PY_019_tautological_and_self_certifying_test_slop.md` |
| AP_MATH_011 | MEDIUM | float literal, `float()`, `math.*` or `.evalf()` in `checks/independent/` | `.agents/patterns/anti/math/AP_MATH_011_float_in_exact_certificate.md` |
| AP_PY_001 | LOW | `# type: ignore` with no error code | `.agents/patterns/anti/python/AP_PY_001_blanket_mypy_ignore.md` |
| CATALOG_*, CARD_*, DUAL_* | MEDIUM | catalog layout: slots, card names, `pattern_id`, reciprocal `dual_pattern` | `.agents/patterns/README.md` |

Sealed run snapshots (`dag/results/`, `sealed_runs/`), `atlas/` and build directories are not scanned. Whole-checkout
mode reads the git index; `--changed-since` also reads untracked files.

## Triage

- AP_LN_001 / AP_LN_004 on an added line: the campaign honesty gate forbids it. Remove it, or keep the module out of the
  change. The same token in a module cited by a PROVED_LEAN or CONDITIONAL node is also overclaim rule R3: hand those
  nodes to `overclaim-hunter`.
- AP_MATH_011: an independent check must certify with exact arithmetic (CONTRIBUTING.md honesty rule 4). A float used
  only to print, after an exact comparison, is acceptable; say so in the review.
- The rest are prompts. Report them; do not fix them in the PR under review unless that PR introduced them.

## Rules for this skill

- The lint never edits a file. A fix is a separate change.
- An empty lint is not a clean bill: most cards have no mechanical signature. Hand those to
  `auto-code-anti-pattern-hunter`.
