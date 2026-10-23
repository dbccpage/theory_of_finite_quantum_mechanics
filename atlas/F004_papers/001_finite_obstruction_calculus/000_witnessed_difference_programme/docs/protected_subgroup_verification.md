# Protected subgroup increment: local verification

Date: 2026-10-08. AuthorityEffect: None.
Scope: [PQ-1–PQ-6](protected_subgroup_character_quotients.md), not the full
WDP programme. No GitHub Actions run is assumed.

## Branch and source custody

The work started at PR #601's reviewed checkpoint
`e10da6bc9714260fbed71af434a70e9a35a51b75`.
Before publication, the parent was refreshed and remained OPEN at
`033d4b44162cdd16b42e1771edc2ed61e34b038d`.
Its only newer file changes were the existing reviewer-gate repair and test.
The follow-on branch was fast-forwarded to that head, preserving those changes.
Its declared PR base is codex/lane-e-duality; this increment does not merge #601.
Current main at that refresh was
`1e1182c2bb87873d6cf28abe293c79673dbbbd75`, an ancestor of the new parent.

Only the twelve named derivation, proof, replay and planning files belong to
this increment. Sealed manifests, source archives, release decisions, host
skills and unrelated local caches are unchanged.

## Python and DAG commands

Working directory: repository root. Python 3.12.10, pytest 8.3.5,
ruff 0.14.13. Each command below exited 0. The repository emits a pre-existing
pytest-asyncio warning about an unset default fixture-loop scope; it is not
silently counted as an error-free warning census.

~~~powershell
py -3.12 -m pytest -q -o addopts= omega_engine_projects/finite_to_continuum/tests/test_protected_quotient_examples.py omega_engine_projects/finite_to_continuum/tests/test_presentation_duality.py omega_engine_projects/finite_to_continuum/tests/test_presentation_closure_examples.py
py -3.12 -m pytest -q -o addopts= omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/plans/test_goal_dag.py
py -3.12 omega_engine_projects/finite_to_continuum/code/protected_quotient_examples.py
py -3.12 omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/plans/goal_dag.py validate
py -3.12 omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/plans/goal_dag.py path PLAN-7D-CSQ-PONTRYAGIN
py -3.12 -m ruff check --select F401,F841,I omega_engine_projects/finite_to_continuum/code/protected_quotient_examples.py omega_engine_projects/finite_to_continuum/tests/test_protected_quotient_examples.py
py -3.12 -m ruff format --check omega_engine_projects/finite_to_continuum/code/protected_quotient_examples.py omega_engine_projects/finite_to_continuum/tests/test_protected_quotient_examples.py
py -3.12 .agents/skills/governance-wdp/scripts/check_coda.py
py -3.12 .agents/skills/governance-lean4-estate/scripts/check_lean4_estate.py
py -3.12 -m omega_engine_operations.use_cases.cicd.republication_checklist_gate
~~~

| Check | Observed scope and result |
| --- | --- |
| Three presentation test files | 89 passed: 26 new obstruction tests, 35 duality regressions, 28 closure regressions |
| DAG test file | 30 passed, including anchor-validation regressions |
| Exact replay | PASS for dyadic-owner levels 0–8 and four rational radii; witnesses at levels 1, 2, 4, 333; infinite_quantifiers_checked=false |
| DAG validation | 246 nodes, 527 local anchors checked, zero validation errors; 29 external anchors unverified |
| DAG target path | Four new completed children, one new open classification child; parent in_progress and Lane E done |
| Ruff | F401/F841/I pass; both Python files formatted |
| CODA self-check | Eight named checks pass against existing sources |
| Lean estate self-check | 77 toolchain/package configurations checked; this is not the Lean build evidence |
| Republication checklist | PASS, 52/52 checks and 9/9 channels; no release authorization follows |

The 29 unverified anchors are the existing external openai-math and
wdp-product-notes references, not failed local anchors. No strict all-external
validation is claimed. The DAG validator checks source references and graph
shape, not mathematical truth.

## Pinned Lean build and complete new-theorem census

The unchanged package pins Lean 4.33.1, compiler commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`,
Lake 5.0.0-src+819816b, and Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`.

The canonical package sources were staged in .lane_e_lean and accessed
through the short Windows junction C:\lk\lane_e_8162. All 97 Lean source and
configuration files matched the canonical package byte-for-byte after the
build. The existing local cache supplied all nine dependencies; each Git
HEAD was compared with its revision in the unchanged lake-manifest.json,
with zero mismatches. No tracked Lake configuration or dependency pin changed.

From working directory C:\lk\lane_e_8162, this exact command exited 0:

~~~powershell
& 'C:\Users\a343o\.elan\toolchains\leanprover--lean4---v4.33.1\bin\lake.exe' --no-cache build +WitnessedDifference.ProtectedCharacterQuotient +WitnessedDifference.ProtectedCharacterQuotientAxiomReport +WitnessedDifference.DyadicCompactOpen +WitnessedDifference.DyadicCompactOpenAxiomReport
~~~

Observed: Build completed successfully (2142 jobs).
This is the selected module build, not a new full-package build.
The no-cache option disables build-cache downloads; it is not a claim that
Lake has an unconditional offline switch.

| Source/report | SHA-256 of checked canonical and staged bytes |
| --- | --- |
| ProtectedCharacterQuotient.lean | 328b2211531a4f54b3d11e4cf17e8fdc936a323b1dc2afb875acb891615cf6b4 |
| ProtectedCharacterQuotientAxiomReport.lean | 6dac0b054052f764cbe3ff6fffc0418864eaf01c75ad4d1edf37f35a7852ea70 |
| DyadicCompactOpen.lean | 787e5309ad8328bda158a2aab1e6ac4ebef2ca430d2008f7665d492486f3a090 |
| DyadicCompactOpenAxiomReport.lean | 535346fb2095b8268864e135f88d6e3f6ad7085081d494f9c0cdaae05e20d053 |

[The quotient report](../lean4/WitnessedDifference/ProtectedCharacterQuotientAxiomReport.lean)
prints all 13 new quotient/source theorems.
[The compact-open report](../lean4/WitnessedDifference/DyadicCompactOpenAxiomReport.lean)
prints all 11 new compact-open theorems.
Every one of the 24 printed declarations has exactly the foundational
axiom set propext, Classical.choice, Quot.sound; none lists sorryAx or a
custom axiom. A declaration-line inventory equals each report's inventory.
Both new proof modules have no sorry, admit, sorryAx, axiom or constant
declarations under the checked token/declaration scan.

The first helper inventory scan also matched the word “theorem” in a
module comment and refused coverage. Restricting that scan to declaration
lines yielded exact 13+11 coverage; no theorem/report was removed to pass it.
An initial dependency-read attempt was sandbox-denied; the explicit
short-cache read was rerun with approval and verified all nine pins.
These were verification-invocation issues, not successful earlier checks.
During development the replay tests also exposed an incorrect test
assumption that numeric strings were disallowed. The existing exact
validator explicitly admits them; the test now checks that contract and
continues to reject floats, booleans and malformed strings.

## Formatting and encoding

Markdownlint CLI 0.41.0 is the cached local executable below. It uses the
repository's .markdownlint.json; no linter configuration was changed.
The following exact command exits 0 for the five touched Markdown files:

~~~powershell
node 'C:\Users\a343o\AppData\Local\npm-cache\_npx\fa35645811bac41d\node_modules\markdownlint-cli\markdownlint.js' 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/protected_subgroup_character_quotients.md' 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/protected_subgroup_verification.md' 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md' 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/plans/derivations_7day_plan.md' 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/plans/outstanding_derivations_master.md'
~~~

The explicitly enumerated twelve-file payload is checked for strict UTF-8
decoding and no leading BOM. git diff --check checks whitespace.
Existing unrelated text is not rewritten to satisfy a new style preference.

## Changed DAG nodes and remaining scope

| Node | Status after this increment |
| --- | --- |
| PLAN-7D-CSQ-ANNIHILATOR | New, done: written PQ-1–PQ-4 and conditional LCA specialization |
| PLAN-7D-CSQ-ANNIHILATOR-LEAN | New, done: selected actual-character laws; extension correspondence explicit |
| PLAN-7D-CSQ-DENSE-PROTECTED | New, done: all-level written obstruction and finite exact replay |
| PLAN-7D-CSQ-COMPACT-OPEN | New, done: selected compact-open laws, classification explicitly conditional |
| PLAN-7D-CSQ-CHARACTER-CLASSIFICATION | New, open: produce the actual-subspace integer-classification declaration |
| PLAN-7D-CSQ-PONTRYAGIN | Modified, still in_progress: depends on these narrower obligations |

PLAN-7D-LANE-E is unchanged and done at LE-1–LE-4 only.
The precise remaining formal implications are integer classification for
DyadicCharacter and the completion-to-arbitrary-closed-image instantiation.
The LCA import, written CRT proof and finite replay retain separate evidence
ceilings. Native continuum binding, general foundations and physical limits
remain open. No sealed manifest or release-decision status was changed.
