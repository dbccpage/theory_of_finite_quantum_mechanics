# Audit of auto-skills-import

Scope: branch `auto-skills-import` (the import of the auto-* skills from the_symbol_game), base `origin/main` at
`3924d378f`. This is the first run of the `audit` umbrella, used as the test run of each imported skill: section 1 and
the `--changed-since` rows are on this change; the whole-checkout rows run each scanner once on the repository as it
stands on main, to see what it finds. Nothing found here was fixed in this branch.

Method: `scripts/overclaim_scan.py`, `scripts/auto/{anti_pattern_lint,obstruction_scan,symmetry_scan,estate_audit}.py`
at this branch's head, then the by-hand step of each skill. Not rebuilt: Lean, cargo.

Result: overclaim 0 nodes reviewed (the change touches no node, status, statement, Lean file or receipt); hunters on
this change 0 HIGH, 0 MEDIUM, 11 LOW; on the whole checkout 0 HIGH, MEDIUM 2 994 (docs) + 36 (obstruction) + 28 (lint),
LOW 6 547 (docs) + 24 (lint) (sections 2 to 5). No node was raised.

## 1. Claims vs proofs (overclaim-hunter)

- `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict`: HIGH 0, MEDIUM 0, LOW 0.
- Step 2 scope: no node's status, statement, bottleneck or `lean` list changed (`dag/derivation_dag.json` is not in the
  diff), so no statement-vs-theorem rows.
- Step 3, numbers this branch states, each recomputed by a command rather than by hand:

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| PR text, import record | 13 card pairs, 26 cards | `anti_pattern_lint.py --catalog-only` on 26 files, 0 findings; generator printed `cards: 26` | yes |
| PR text, companions | 78 tests in `scripts/auto/test_auto_checks.py` | `pytest scripts/auto/test_auto_checks.py`: 78 passed | yes |
| companions | mutation ratios 0.9032, 0.9677, 0.9753, 1.0, 0.9286 | killed / (killed + survived + inconclusive) from the campaign counts: 28/31, 90/93, 79/81, 44/44, 52/56 | yes |
| section 5 | 2364 broken links in 366 notes, 2363 starting `../../` | count over the JSON output of `estate_audit.py docs` | yes |

## 2. Obstructions (auto-obstruction-hunter)

`obstruction_scan.py --fail-on none` on the whole checkout: O1 0, O2 2, O3 34. On this change: 0.

O1 (independent checks import repository code): none of the 9 files in `checks/independent/` imports repository code
or edits `sys.path`.

O2: two module-level import cycles, both through a package `__init__.py` that imports its submodules while they import
the package back: `code/python/src/qm/` (21 files) and `code/python/src/linear_algebra/` (8 files). Python tolerates
this when names are bound in a safe order; it breaks when one is not. Owner: the module authors.

O3: 34 routes recorded as `DERIVED_LEAN`, `DERIVED_PROSE` or `COMPUTED` take an input whose status is `OPEN` (one of
them, into a `REFUTED` node, has four `OPEN` inputs). By `edge_semantics` a route requires all of its inputs, so each row is
either a spurious input on the route or an output that rests on an open input. For every row, no other derived route
into the output has only held inputs. Owner: `overclaim-hunter` Step 2 for the 12 `PROVED_LEAN` and 1 `PROVED_PROSE`
outputs; the owning DAG fragment for the rest.

| Route | Route status | Output [status] | Open input(s) | `dag/derivation_dag.json` line |
|---|---|---|---|---|
| PG-R-GAP-GENESIS-TO-WINDOW | DERIVED_LEAN | PG-WDP-DEGREE1-WINDOW [DEFINITION] | PG-WDP-GENESIS-BRIDGE-OBLIGATIONS | 27705 |
| UDG-R-TFQ-0013 | COMPUTED | TFQ-0013 [COMPUTATIONALLY_CHECKED] | TFQ-0012 | 29891 |
| UDG-R-TFQ-0015 | COMPUTED | TFQ-0015 [COMPUTATIONALLY_CHECKED] | TFQ-0014 | 29913 |
| UDG-R-TFQ-0018 | COMPUTED | TFQ-0018 [COMPUTATIONALLY_CHECKED] | TFQ-0017 | 29946 |
| UDG-R-TFQ-0028 | COMPUTED | TFQ-0028 [COMPUTATIONALLY_CHECKED] | TFQ-0027 | 30056 |
| UDG-R-TFQ-0034 | COMPUTED | TFQ-0034 [COMPUTATIONALLY_CHECKED] | TFQ-0033 | 30122 |
| UDG-R-TFQ-0043 | COMPUTED | TFQ-0043 [COMPUTATIONALLY_CHECKED] | TFQ-0012 | 30221 |
| UDG-R-TFQ-0045 | COMPUTED | TFQ-0045 [COMPUTATIONALLY_CHECKED] | TFQ-0044 | 30243 |
| UDG-R-TFQ-0051 | COMPUTED | TFQ-0051 [COMPUTATIONALLY_CHECKED] | TFQ-0050 | 30309 |
| UDG-R-TFQ-0125 | COMPUTED | TFQ-0125 [COMPUTATIONALLY_CHECKED] | TFQ-0007 | 30584 |
| UDG-R-TFQ-0166 | COMPUTED | TFQ-0166 [COMPUTATIONALLY_CHECKED] | TFQ-0007 | 31035 |
| UDG-R-TFQ-0178 | COMPUTED | TFQ-0178 [COMPUTATIONALLY_CHECKED] | TFQ-0177 | 31156 |
| UDG-R-TFQ-0180 | COMPUTED | TFQ-0180 [COMPUTATIONALLY_CHECKED] | TFQ-0177 | 31167 |
| PGW-R-NO-ENDOGENOUS-DEMAND-GENERATOR | DERIVED_PROSE | PGW-NO-ENDOGENOUS-DEMAND-GENERATOR [PROVED_PROSE] | TFQ-0385 | 32614 |
| PGW-R-WDP-GENESIS-BRIDGES-LEDGER | DERIVED_PROSE | PGW-WDP-GENESIS-BRIDGES-LEDGER [DEFINITION] | PG-WDP-GENESIS-BRIDGE-OBLIGATIONS | 33960 |
| PGW-R-WDP-SYNTHESIS-TRUNK-TIERS | DERIVED_PROSE | PGW-WDP-SYNTHESIS-TRUNK-TIERS [DEFINITION] | PGW-WDP-BRIDGE-ONGOING-TO-WINDOW | 34003 |
| APP-R-DFM-BOREL-LEVI-FACTORIZATION | DERIVED_PROSE | DFM-BOREL-LEVI-FACTORIZATION [DEFINITION] | DFM-HIERARCHICAL-BOREL | 34355 |
| APP-R-DFM-BOREL-TWO-STAGE-DIAMOND | COMPUTED | DFM-BOREL-TWO-STAGE-DIAMOND [COMPUTATIONALLY_CHECKED] | DFM-HIERARCHICAL-BOREL | 34369 |
| APP-R-MAJ-GIN-INVOLUTION-PAIR-CANCEL | DERIVED_LEAN | MAJ-GIN-INVOLUTION-PAIR-CANCEL [PROVED_LEAN] | FSP-EFFICIENT-SAMPLING-OBLIGATIONS | 35334 |
| APP-R-MAJ-ENVELOPE-NAT-ARITHMETIC | DERIVED_LEAN | MAJ-ENVELOPE-NAT-ARITHMETIC [PROVED_LEAN] | MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE | 35405 |
| APP-R-FSP-MASTER-DICHOTOMY-REFUTED | DERIVED_PROSE | FSP-MASTER-DICHOTOMY-REFUTED [REFUTED] | FSP-LATTICE-ANOMALY-INFLOW, FSP-COBORDISM-INTRINSIC-SIGN, FSP-DIRAC-KAHLER-SPINFOAM-CLAIM, FSP-HINGE-LINEON-SIGN-CLAIM | 35966 |
| APP-R-MUB6-TAO-LAURENT-NORM-NINE | DERIVED_LEAN | MUB6-TAO-LAURENT-NORM-NINE [PROVED_LEAN] | MUB6-CONJECTURE2-PREMISE | 36458 |
| APP-R-MUB6-ROUTE-C-LABEL-ARITHMETIC | DERIVED_LEAN | MUB6-ROUTE-C-LABEL-ARITHMETIC [PROVED_LEAN] | MUB6-GLOBAL-OBLIGATIONS | 36518 |
| APP-R-MUB6-GLUING-G3-OPAQUE | DERIVED_LEAN | MUB6-GLUING-G3-OPAQUE [PROVED_LEAN] | MUB6-GLOBAL-OBLIGATIONS | 36545 |
| APP-R-MUB6-INTERFACE-COUNTERMODEL | DERIVED_LEAN | MUB6-INTERFACE-COUNTERMODEL [PROVED_LEAN] | MUB6-FLAT-EXTENSION-FAILURE-CLAIM | 36825 |
| APP-R-COMP-C3-BOUNDED-REACH-DECIDABLE | DERIVED_LEAN | COMP-C3-BOUNDED-REACH-DECIDABLE [PROVED_LEAN] | PGW-RUNS-PAST-DECLARED-BOUNDS | 37001 |
| APP-R-QCV-SELF-OBSTRUCTION-MODEL | DERIVED_PROSE | QCV-SELF-OBSTRUCTION-MODEL [DEFINITION] | QCV-QUESTION-SELF-LIMITING-REPAIR | 37349 |
| APP-R-AUTH-FUEL-EXHAUSTION-TYPED-STOP | DERIVED_PROSE | AUTH-FUEL-EXHAUSTION-TYPED-STOP [DEFINITION] | PGW-RUNS-PAST-DECLARED-BOUNDS | 37582 |
| APP-R-AUTH-G5A-CLASS-RELATIVE-TRANSPORT | DERIVED_LEAN | AUTH-G5A-CLASS-RELATIVE-TRANSPORT [PROVED_LEAN] | TFQ-0330 | 37626 |
| APP-R-AUTH-G5C-TERMINALIZATION-CONSEQUENCE | DERIVED_LEAN | AUTH-G5C-TERMINALIZATION-CONSEQUENCE [PROVED_LEAN] | TFQ-0330 | 37640 |
| APP-R-AUTHF-DTM0-FIXTURES | COMPUTED | AUTHF-DTM0-FIXTURES [COMPUTATIONALLY_CHECKED] | PGW-RUNS-PAST-DECLARED-BOUNDS | 37742 |
| APP-R-AUTHF-CLASS-RELATIVE-TRANSPORT | DERIVED_LEAN | AUTHF-CLASS-RELATIVE-TRANSPORT [PROVED_LEAN] | PGW-CONTEXT-DECISION-PROCEDURE | 37809 |
| APP-R-AUTHF-TERMINAL-ACCEPT-BIT | DERIVED_LEAN | AUTHF-TERMINAL-ACCEPT-BIT [PROVED_LEAN] | TFQ-0330 | 37835 |
| APP-R-AUTHF-PD-EXTENSION-NONUNIQUE | DERIVED_LEAN | AUTHF-PD-EXTENSION-NONUNIQUE [PROVED_LEAN] | TFQ-0332 | 37967 |

The `COMPUTED` rows from `TFQ-*` records may be reading-order links recorded with a derived status; that is for the
fragment owner to say. No row was given a verdict here.

## 3. Symmetry breaks (auto-symmetry-hunter)

`symmetry_scan.py --fail-on none`: 0 findings over 51 prose files (the four invariants agree with
`ALLOWED_AXIOMS`, `LEAN_ADMISSION_TOKENS`, `PFP_STATUS_RANK` and `FORBIDDEN`, and the lint's `LEAN_FORBIDDEN` equals
the overclaim scanner's tokens plus `axiom`). By hand, two differences between the new lint and overclaim rule R3:

| Invariant | Locations | Class | Proposed propagation |
|---|---|---|---|
| What counts as an `admit` token | `scripts/overclaim_scan.py` R3 skips only names after `\|`; `scripts/auto/anti_pattern_lint.py` also skips `admit` used as an ordinary identifier (`def admit`, `unfold admit`, `admit d guards`) | EXTENSION | Decide whether R3 should skip identifier uses too; on this checkout the identifier `admit` occurs on 75 lines of 10 Lean files under `code/rust/quality/category_homology/proofs/` |
| Modifiers before `axiom` | R3 accepts `private`, `protected`, `noncomputable`; the lint also accepts `unsafe` and `partial` | EXTENSION | Align R3 if `unsafe axiom` is to be caught |

## 4. Anti-patterns (auto-anti-pattern-lint, auto-code-anti-pattern-hunter)

`anti_pattern_lint.py --changed-since origin/main`: 0 findings. Whole checkout (7 124 Lean and Python files, sealed
`dag/results/` excluded): 0 HIGH, 28 MEDIUM, 24 LOW.

| Rule | Count | Examples (file:line) | Note |
|---|---|---|---|
| AP_LN_001 / AP_LN_004 | 0 | | no admission token or axiom declaration outside comments, strings and identifier uses |
| AP_PY_019 | 23 | `code/python/src/majorana/test_codaq_omega_engine_integration.py:42` (`assert True`); `code/python/src/majorana/test_finite_matrix_recovery.py:353` (`assert 8 > 4`); `code/python/tests/test_finite_witness.py:109` (`assert 5 * 5 - 3 * 3 == 16`) | 19 of 23 are in `code/python/src/majorana/` |
| AP_PY_006 | 5 | `code/rust/quality/l4a_qm_six/replay.py:209` hard-codes a the_symbol_game `Cargo.lock` path on one workstation; `papers/core/constraint_closure/public_export/build_publication_assets.py:633` | |
| AP_MATH_011 | 0 | | no floating point in the 9 independent checks |
| AP_PY_001 | 24 | blanket `# type: ignore` | LOW |

By hand on this change (cards `AP_PY_009`, `AP_PY_019`, `AP_PY_006`): the five companions bind the sha256 of the
committed sources (holds); the new tests call the code under test and the lint reports none of them (holds); no
host-absolute path in `scripts/auto/` (holds).

## 5. Documentation (auto-docs)

On this change: 11 LOW (paths created on demand, such as `.claude/agents/`, or generated directories such as
`lean4/.lake`); `scripts/build_readme_facts.py --check` was stale because of the new test functions and was regenerated
with `--write` in this branch.

Whole checkout (9 339 Markdown and Python files, sealed `dag/results/` and `atlas/` excluded): 2 994 broken relative
links (MEDIUM) and 6 547 cited paths that do not exist (LOW). (One further LOW, a missing provenance header on
`scripts/auto/test_auto_checks.py`, was fixed in this branch.)

- 2 364 of the broken links are in 366 derivation notes under `dag/derivations/`; 2 363 start with `../../`, which
  from `dag/derivations/<segment>/` lands inside `dag/` (for example `dag/derivations/01_pregenesis/tfq_0361_inert_literal_inscription.md:33`
  links `../../code/lean4/`). This looks like one generator defect; proposed for follow-up in
  `.claude/skills/PROPOSED_SKILLS.md`.
- The rest: `papers/foundations` 397, `papers/core` 134, `dag/research` 67, smaller counts elsewhere.

## 6. Agents and skills (auto-review-agents, auto-review-skills, auto-improve-autoskill)

- Agents: 0 definitions in `.claude/agents` or `.agents/agents`; 25 teamwork briefs, 0 findings. The first version of
  the wording rule flagged `.agents/teamwork/reviewer_2_formal/BRIEFING.md:16`, a sentence telling the reviewer to
  check for self-certifying code; detection verbs were added to the negation cues and the finding cleared.
- Skills: 13 skills, 0 HIGH, 0 MEDIUM, 5 LOW (on-demand paths).
- auto-improve-autoskill on the imported skills (a self-review by the importing agent, not an independent one):
  verdict PATCH, applied during the import. Removed from the sources: automatic admission and four-host mirroring
  (`auto-suggest-new-skills`), the residual-mass and budget gates and OE paths (`auto-improve-autoskill`), the
  automatic repair engine (`auto-learn`). No imported skill can raise a status or edit the overclaim-hunter hard rules;
  `estate_audit.py skills` reports no authority-unsafe wording.

## Learning runs during the import

- auto-learn, two applied lessons: the lint first flagged 75 lines in 10 files under `code/rust/quality/category_homology/proofs/`
  where `admit` is an ordinary identifier; the rule now skips identifier uses, with a test, and the whole-checkout count
  fell to 0. The wording audit first flagged the skills' own quoted descriptions of unsafe phrases; quoted text is now a
  mention, with a test.
- auto-skill: one signal (the shell guard rejects heredocs and variable loops) is already in
  `.claude/skills/auto-skill/references/signals.md`; no skill edit proposed.
- auto-suggest-new-skills: two proposals in `.claude/skills/PROPOSED_SKILLS.md` (`dag-sync`, MEDIUM;
  `derivation-note-link-repair`, LOW).

## What no stage could decide

Whether each O3 route lists a spurious input or rests a claim on an open node (needs the Lean or prose of each output);
whether the two package import cycles ever fail at import time; whether a heuristic prose rule (symmetry, wording)
missed a rephrased copy; the 6 547 missing cited paths, many of which may name files that live in other repositories.
