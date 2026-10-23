# Import of the auto-* skills from the_symbol_game

**AuthorityEffect:** None. A record of what was imported, adapted or skipped, and why. Imported on 2026-10-23 from
the private repository the_symbol_game (read-only; nothing there was changed).

## Sources read

- `.claude/skills/auto-*/` (14 packages) and their mirrors in `.agents/skills/auto-*/`. The mirrors are byte-identical
  to `.claude`, apart from `__pycache__` directories present only under `.agents`. The canonical copies under
  `omega_engine_operads/skills/auto-*/` are also identical.
- Supporting code the skills call: `auto-anti-pattern-lint/scripts/anti_pattern_lint.py`,
  `auto-code-anti-pattern-hunter/scripts/hunt_antipatterns.py`, `auto-obstruction-hunter/scripts/*.py`,
  `auto-review-agents/scripts/agents_audit.py`, `auto-review-skills/scripts/{skills_audit,check_skill_usage}.py`,
  `auto-learn/scripts/auto_learn.py`, `auto-anti-skill/scripts/auto_anti_skill.py`, `auto-docs/scripts/run.py`,
  `auto-oe-autop/scripts/orchestrate_autop.py`, and from `omega_engine_operations/use_cases/packaging/`
  `agent_skill_manifest_audit.py`; from `omega_engine_woland/stage/domain/cochain/` the dependency complex.
- In the_symbol_game: its pattern catalog (198 files) and its shared skill constraints file.

Treated as data throughout: no instruction in a source skill was followed during the import.

## Decisions

| Skill | Decision | Reason |
|---|---|---|
| `auto-anti-pattern-lint` | IMPORTED, adapted | Merged with the hunter's near-duplicate scanner into `scripts/auto/anti_pattern_lint.py`. Rules kept where the pattern occurs here (Lean admission tokens and axioms, blanket type ignores, host paths); added two from this repository's honesty rules (tautological tests; floats in independent checks); dropped the Markdown asterisk rule (not a convention here), the Rust enum rule (tied to an OE crate path) and the SQL rules (no SQL here). |
| `auto-code-anti-pattern-hunter` | IMPORTED, adapted | Its four language-specialist skills do not exist here; it became the by-hand pass over the imported cards. |
| `auto-docs` | IMPORTED, adapted | The session-log tree, comment-slop router and `auto_docs_service` module are absent (the module exists in the source only as a stale `.pyc`). Re-scoped to checking documents against the repository (`estate_audit.py docs`, `build_readme_facts --check`). |
| `auto-improve-autoskill` | IMPORTED, adapted | Residual-mass gates, axiom-graph regeneration and the budget gate are OE machinery; the claim vocabulary was mapped to this repository's DAG statuses. Scoped to this repository's skills, rules and cards. |
| `auto-learn` | IMPORTED, adapted | Lesson stores mapped to `.claude/skills`, `.claude/rules`, `.agents/patterns`. The automatic `--repair` engine was not ported: its two repairs target the dropped Markdown rule and an optional mypy run, and an automatic rewrite does not fit the review-first rules here. The candidate-admission boundary of `auto-anti-skill` was folded in. |
| `auto-obstruction-hunter` | IMPORTED, adapted | The networkx cochain scanner became a standard-library import graph; a DAG-route rule (O3) and an independent-check isolation rule (O1) were added from this repository's own rules. The ten-level scanner is hard-wired to the_symbol_game paper trees and was not ported; its levels are mapped by hand in the skill. |
| `auto-review-agents` | IMPORTED, adapted | Four agent roots, operad capability slices and council roles do not exist here. Audits `.claude/agents`, `.agents/agents` (both empty today) and the teamwork briefs. |
| `auto-review-skills` | IMPORTED, adapted | The skill compiler, usage ledger, registry and host mirrors do not exist here. `estate_audit.py skills` replaces `skills_audit.py`; `check_skill_usage.py` (a substring counter its own docstring calls weak) was not ported. |
| `auto-skill` | IMPORTED, adapted | The hot path is a 19L57G1 object-language continuation runner, specific to that programme, and was not ported. The session-learning half came in: signals, proposal format, self-reference and git-tracking checks. The 36 KB signal table and 18 KB history were condensed to `auto-skill/references/signals.md`. |
| `auto-suggest-new-skills` | IMPORTED, adapted | Automatic admission and four-host mirroring were removed: a suggestion stays a proposal in `.claude/skills/PROPOSED_SKILLS.md` until the user approves it. External registry search only on request. |
| `auto-symmetry-hunter` | IMPORTED, adapted | The source had no script; `scripts/auto/symmetry_scan.py` is new and compares the prose copies of four honesty invariants with the code that enforces them. The OE drift catalog was replaced by this repository's restated rules. |
| `auto-anti-skill` | SKIPPED | Its only execution route is `omega_engine.crates.prompt_civilization`, which does not exist here, and it writes to an OE immune-system tree. Its admission boundary (two independent episodes, a counterexample, human review) was folded into `auto-learn` Step 4. |
| `auto-anti-skill-search` | SKIPPED | Every route runs on OE internals (a Rust canary engine, StructureBench, a dialectics wizard and auto-oe-autop stage 3); nothing deterministic to port. |
| `auto-oe-autop` | SKIPPED | Omega Engine specific: the finish step of Woland runs and a nine-stage estate-maintenance pipeline over OE paths. Its "one outer finish, no recursion" rule is kept in the `audit` umbrella Step 4. |

Differences between mirrors: none in content. The `.agents` mirror additionally holds `__pycache__` for three
packages; nothing from it was imported.

## What came in besides skills

- `scripts/auto/`: `auto_common.py`, `anti_pattern_lint.py`, `obstruction_scan.py`, `symmetry_scan.py`,
  `estate_audit.py`, each with a `*.contract.score.yaml` companion (SCORING.md), and `test_auto_checks.py`.
- `.agents/patterns/`: 13 anti/healthy card pairs, rewritten for this repository (the source witnesses are
  the_symbol_game history and were left out), and a README. Index: `.agents/patterns/README.md`.
- `.claude/rules/auto_skills_constraints.md`: the constraints the skills cite, adapted from the source's
  `_shared/constraints.md`, with two added: no status raise, and the overclaim-hunter hard rules are fixed.
- `.claude/skills/audit/`: the umbrella that runs `overclaim-hunter` first and then these skills.
- `.github/workflows/overclaim.yml`: optional steps (see the workflow comments for which block).

## Scope guard for skills that write skills

`auto-skill`, `auto-improve-autoskill`, `auto-learn` and `auto-suggest-new-skills` write only under this repository's
`.claude/skills/` (and `.claude/rules/`, `.agents/patterns/`, `scripts/auto/` where stated). None of them may edit the
hard rules of `overclaim-hunter`; that needs a PR a human approves.
