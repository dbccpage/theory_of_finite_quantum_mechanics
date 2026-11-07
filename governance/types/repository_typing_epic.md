# Repository typing epic

AuthorityEffect: None. This plan moves, merges and deletes files and wires a checker into CI. It changes no DAG
node, status, statement or route, adds no DAG node, and changes no mathematical content.

Baseline: the merged tip, 341d2e3dc plus this branch (the review began at 88fa973cc; main then gained #574 to #577,
which were merged into this branch and reconciled). Every count is a count of tracked files at that tip or of the tree
after every story, computed from `git ls-tree -r -l HEAD`, the types and the appendix of this file (section 8).

## 1. What this epic does

The repository is typed as one object: the repository is the root class, each top-level folder a typed attribute,
each subfolder or file kind a type, and every tracked file an instance of exactly one type. Superfluous files are
then removed, so that the tree is a checkable object, without breaking anything. The types live in
`governance/types/`: `repository.type.yaml` (the root class, the meta-schema `repo-type/1` in block `meta`, the
naming and public-text rules, the shared leaf types), one `<folder>.type.yaml` per top-level folder of the target
tree (the three dot folders are class `ToolConfigFolders` in the root file), and this epic. The types describe the
target tree; each member records `now` (at the merged tip) and `target` (after the epic). What the epic removes, moves or
renames is listed once, in section 8.

Why `governance/types/`: `governance/` already holds the companion regime (`governance/policy.json`) and the
grandfather list (`governance/baseline.json`); the types are the same kind of rule, so the epic removes three
top-level folders (`rules/`, `problem_sets/`, `reviews/`) and adds none. `governance/**` is outside the governed
populations (`code/**/*.rs`, `code/**/*.py`, `lean4/**/*.lean`), `.gitattributes:148` gives it LF endings, and no
prose scanner treats it as public prose (`scripts/overclaim_scan.py`:108-109).

Sources of truth (block `sources_of_truth` of the root file): `rules/rules.yaml` is subsumed (rule_1 is
`naming_rules`; rule_2, a three-file companion set, contradicts `governance/policy.json`, which requires one
`.contract.score.yaml`, and the tree, which has 2,534 of those under `code/` and no `.score.yaml` or
`.contract.yaml`; rule_3 is invariant `repo.qm_atlas_gate`) and deleted in S03. `library.yaml` is referenced, not
copied: a library checker in a private sibling repository reads it as this repository's catalog, so it stays at
the root, keeps its own schema, and S03, S08 and S11 repoint its stale paths. `governance/policy.json` and
`governance/baseline.json` are referenced; leaf types say `companions: policy` and never restate the regime.

## 2. Target shape

| Top-level folder | Files now | MB now | Files after | MB after |
|---|---:|---:|---:|---:|
| atlas | 5,549 | 315.0 | 4,523 | 301.6 |
| checks | 478 | 11.4 | 903 | 27.7 |
| code | 6,152 | 154.7 | 5,967 | 151.1 |
| dag | 1,449 | 38.6 | 1,397 | 35.1 |
| docs | 1,306 | 10.7 | 1,303 | 9.1 |
| education | 1,056 | 10.9 | 1,094 | 13.3 |
| evidence | 1,181 | 22.3 | 876 | 19.3 |
| governance | 78 | 1.3 | 79 | 1.3 |
| lean4 | 2,137 | 30.8 | 2,008 | 29.7 |
| normal_forms | 70 | 0.5 | 70 | 0.5 |
| papers | 1,246 | 36.5 | 623 | 19.8 |
| problem_sets | 50 | 0.3 | 0 (into education) | 0 |
| reviews | 449 | 16.7 | 0 (into checks and evidence) | 0 |
| rules | 1 | 0.0 | 0 (subsumed) | 0 |
| scripts | 69 | 1.3 | 67 | 1.2 |
| vendor | 2,999 | 36.7 | 2,999 | 36.7 |
| the three dot folders | 62 | 0.2 | 62 | 0.2 |
| root files | 18 | 0.5 | 15 | 0.5 |
| **total** | **24,350** | **688.4** | **21,986** | **647.2** |

Top-level folders without a dot: 16 now, 13 after. Both columns count the 15 files of `governance/types/`; the "after"
column also counts the 2 files S01 adds ('scripts/check_repo_types.py' and its test) but not their bytes. 2,366 files (41.1 MB) are removed;
546 of them are byte twins of a file that stays. 526 files move (S06 1, S10 1, S11 89, S12 6, S14 428, S16 1) and
S17 renames 2. All other files stay where they are.

## 3. Rules for every story

1. One story is one pull request from a branch off current main, reverted with `git revert` of its merge commit.
   Never stash; never force-push main.
2. Change nothing the story does not name. Never change a DAG status, add a DAG node or edit a statement. A path in
   a DAG field changes only through `dag/README.md` "Change": edit `dag/derivation_dag.json` or the fragment that
   owns the slice, run the syncs in the order listed there, then `python -I -X utf8 dag/evidence/build_evidence.py
   --write`.
3. No archives. Superseded material is deleted with `git rm`; git history keeps it. Nothing is moved aside.
4. Removing a governed source leaves its baseline entry stale; `governance-check` only notes that
   (code/rust/src/governance/src/bin/governance-check.rs:197). Run `governance-check baseline --write`, which only
   shrinks the baseline (governance/README.md:127), and commit the result.
5. Editing a governed source voids its grandfathering (governance/README.md:36): the file must then meet the floor,
   or the owner approves a re-pin. Only S16 and S19 do this, each with that approval.
6. Inside an atlas deposit, after removing or renaming files: record the deposit's integrity before the change with
   `sha256sum -c --quiet MANIFEST.sha256` and `sha256sum -c --quiet SHA256SUMS` from the deposit root (only
   genesis, the WDP, higher_cell and projection_obstruction_paper accept `verify_deposit.py --integrity-only`).
   Ten of the 13 deposits already fail at the merged tip (atlas.type.yaml, invariant `deposit.manifest_matches`); list
   those stale entries in the PR, because regenerating seals them too. Regenerate both files with the deposit's
   'scripts/regen_sha256sums.py' (in 12 deposits; `certified_adaptive_quantum_dynamics` has only
   `tools/rebuild_release.py` and 'scripts/rebuild_release.py', so edit its two manifests by hand); after, both
   checks pass. Drop or repoint the matching entries of `atlas/PROVENANCE.json`.
7. Text a story adds passes the public-text rule (root file, block `public_text`) and holds no host-absolute path.
8. Historical records keep the paths they recorded: contract-score histories (`raw_utf8` entries hashed by
   `scripts/score_scope_contracts.py`:439-457), review records, custody records, receipts and manifests of runs. Already
   671 tracked files name the retired 'dag/results/' and 706 name 'dag/research/', and no check fails on that.

### The standard checks

Run before and after every story, from the root, on a clean checkout; "after" equals "before" except as the story
says.

| Id | Command | State at 341d2e3dc |
|---|---|---|
| C1 | `python -I -X utf8 dag/validate_derivation_dag.py --repo-root .` | `nodes=989 routes=997 records=1041 failures=0` |
| C2 | `python -I -X utf8 dag/evidence/build_evidence.py --check` | exit 1, 11 stale files (S02 fixes it) |
| C3 | `cargo build --locked --release --manifest-path governance/Cargo.toml --bin governance-check`, then `governance/target/release/governance-check --root . check` (also with `--changed-since origin/main`), `python -I -X utf8 scripts/score_scope_contracts.py check --changed-since origin/main`, `python -I -X utf8 scripts/contract_scores.py check` | governance.yml passes on main |
| C4 | `python -m pytest scripts/test_overclaim_scan.py scripts/auto/test_auto_checks.py -q -p no:cacheprovider`; `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict`; `python -I -X utf8 scripts/auto/anti_pattern_lint.py --changed-since origin/main`; `python -I -X utf8 scripts/auto/estate_audit.py skills` | overclaim.yml passes on main |
| C5 | `python -I -X utf8 scripts/build_readme_facts.py --check` (a story that changes a counted inventory runs `--write` and commits only the facts block) | stale (S02 fixes it) |
| C6 | `python -I -X utf8 scripts/check_repo_types.py` (from S01); `--plan Snn` lists a story's files | UNTYPED 1,178 at the S01 commit |
| C7 | for each removed or moved path P, `git grep -n -F "P"`; every hit is fixed by the story or is a record under rule 8 | - |
| C8 | `git status --porcelain` shows only the story's paths; `git diff --stat` matches the story's counts | - |

| Workflow | What it runs | Stories that must keep it green |
|---|---|---|
| dag.yml | the DAG validator on every PR and push | all; S01 and S02 add steps |
| governance.yml | governance crate tests, governance-check, contract histories, replay pins | S04, S05, S13, S15, S16, S19 |
| overclaim.yml | overclaim scan, anti-pattern lint, skill audit, non-blocking audits | all (S16 edits skills) |
| reviewed-checkers.yml | review-ledger hash step and checker tests (paths `checks/**`, `reviews/repository_file_review/**`) | S12, S14 |
| projection-obstruction.yml | tests, replay check and integrity of projection_obstruction_paper and higher_cell (path-filtered) | S14 |
| everett-checks.yml | atlas/everett_mw checks (path-filtered) | none |
| lean-gleason.yml | nine Lean targets (path-filtered on lean4) | S04, S16 |
| status.yml | daily status site and Pages build | S06, S12 |
| codeql.yml | CodeQL; ignores atlas/ and evidence/results/ | none |

## 4. Stories

A story's files are the appendix lines tagged with it (section 8); `scripts/check_repo_types.py --plan Snn` prints
them from S01 on. Counts are exact at the merged tip.

### S01 Add the type checker in report-only mode

- Add 'scripts/check_repo_types.py' and 'scripts/test_check_repo_types.py'. The checker loads every
  `governance/types/*.type.yaml` (PyYAML), applies block `meta` of the root file to `git ls-files`, and prints per
  class the files it owns, per member the matched count beside `now` and `target`, and the UNTYPED, DEAD, MISSING,
  UNKNOWN, CLAIM and FORM findings. Options: `--strict` (exit 1 on any of those six), `--report naming`,
  `--report public-text` (paths and categories only, never the matched text), `--report duplicates` (blob groups no
  `derives_from` relation or allow entry declares), `--plan Snn` (the files this epic's appendix removes, keeps or
  moves in story Snn; exit 1 when a `(N files)` count differs from the tree), `--summary FILE` (Markdown for the CI
  step summary).
- The test builds a tree in `tmp_path` with one class of each kind (`path`, `paths`, `path_glob`) and checks every
  error kind, first-match order, `**`, `[...]` and `{a,b}`, the catch-all rule, and the public-text normalisation
  (CamelCase split, trailing "s", word pairs) against hashes of made-up words.
- CI: in `.github/workflows/dag.yml`, after the validator step, add `- name: Repository types (report only)` with
  `continue-on-error: true` and `run: python -m pip install --disable-pip-version-check pyyaml pytest && python -I -X utf8 -m pytest scripts/test_check_repo_types.py -q -p no:cacheprovider && python -I -X utf8 scripts/check_repo_types.py --summary "$GITHUB_STEP_SUMMARY"`.
- Accept: the test passes; on the S01 commit the checker reports UNTYPED 1,178, FORM 0, UNKNOWN 0, CLAIM 0, MISSING 7
  (attributes `GenesisOngoingRun.run_contract`, `ChecksFolder.review_ledger`, `ReviewLedger.readme`,
  `ReviewLedger.ledger`, `EducationFolder.problem_sets`, `EducationFolder.teaching_pack`,
  `GovernanceFolder.scoring_history`) and DEAD 26 (the 18 members that receive files in later stories: the run
  contract, four review-ledger members, six problem-set members, five teaching-pack members, the projection review
  member and the scoring-history attribute; and the 8 leaf types only they use: RunContract, ReviewLedgerFile,
  CheckerReviewRecord, ReviewByteSnapshot, ProblemSheet, ProblemSolution, ProblemResult, GovernanceGuide);
  `--report public-text` counts 3,325 files; `--plan` reproduces every count of section 8; C1 and C4 pass.

### S02 Bring generated outputs up to date and check them in CI

- Diagnosis: `build_evidence.py --check` exits 1 at 341d2e3dc with 11 stale files: `dag/evidence/evidence_map.json`,
  `docs/evidence/README.md`, `docs/evidence/mismatches.md`, seven node pages, one stage page, and the missing page of
  node FQ-CHSH-NORM-ADMISSION-COMPARISON, which #577 added without `--write`. (At 88fa973cc it was 34 files, left by
  commits 56e16ec03 and 0ed4ea6c9; the label sweep regenerated them.) Not line endings: `core.autocrlf` is false and
  the checked-out bytes equal the blobs. No workflow runs `--check`, so the drift goes unseen. The README facts block
  is stale too.
- Do: `python -I -X utf8 dag/evidence/build_evidence.py --write` (commit the files it reports) and
  `python -I -X utf8 scripts/build_readme_facts.py --write` (commit the facts block only). In `dag.yml` add a
  blocking step `python -I -X utf8 dag/evidence/build_evidence.py --check` and two steps with
  `continue-on-error: true`: `python -X utf8 -m pytest -q dag/tests dag/evidence/test_evidence.py` and
  `python -I -X utf8 scripts/build_readme_facts.py --check`; list in the PR every test that fails at this commit.
- Accept: C2 prints `evidence map current`; C5 passes; no file changes beyond the ones `--check` listed and the facts
  block; no grade or status changes (the pages only catch up with the DAG); C1 passes.

### S03 Dissolve `rules/` and repoint `library.yaml`

- Remove `rules/rules.yaml` (1 file). Nothing reads it (`git grep -n -F "rules.yaml"` finds only unrelated strings in
  atlas receipts, a vendored test, and `docs/maintenance/atlas_dependency_inventory.json`, which S06 deletes);
  `.agents/rules/qm_atlas_loc_sync.md` states rule_3 in its own words and stays.
- Edit `library.yaml` in place (keep its header and schema): `atlas/papers/finite_obstruction_calculus`,
  `atlas/papers/projection_obstruction` and `atlas/papers/everett_mw` (and its entry point) lose `papers/`; drop the
  books 'papers/complexity', 'papers/drafts', `sources/atlas` and `rules`; drop the eight entry points under
  `papers/core/` and 'papers/computation/' that no longer exist (their files now live in `dag/derivations/*/sources/`,
  `dag/derivations/master_derivation_ledger.md` and `atlas/computation_complexity_pvnp/`; point to those if the owner
  prefers).
- Accept: UNTYPED falls by 1; the 15 paths of `library.yaml` missing at the merged tip resolve or are gone; C1, C4.

### S04 Remove root leftovers, unused scripts and Lean text saved as Markdown

- Remove (140 files): `PROJECT.md`, `test_infra.md`, `test_ready.md`; `scripts/atlas_import/` (6),
  `scripts/build_l4e_contracts.py`, `scripts/lean_replay_campaign/lakefile_roots.py`; `lean4/Imported/roots.txt`,
  `lean4/Imported/roots_programmes.txt` (read only by `lakefile_roots.py`); `lean4/lakefile.campaignMajorana.contract.score.yaml`
  (companion of a file folded into the lakefile on 2026-10-27); `lean4/majorana_axiom_report.txt` (byte twin of
  `papers/core/majorana/lean4/axiom_report.txt`); and 125 `lean4/qm*.md` files, Lean text saved as Markdown. Their
  stems appear elsewhere only inside other, non-existent `.lean` paths ('lean4/original_lean_20260809/...' in DAG
  prose fields and atlas claim ledgers) and in the exclusion list of `deposit_paths.py`:220 and
  `code/deposit_paths.py`:79; the node those fields describe cites the live `lean4/BornRedundancy.lean`. The 16
  `lean4/qm_*.md` that `dag/derivations/10_finite_qm_core/sources/` prose names stay (the KEEP lines).
- `scripts/overclaim_scan.py`:109 lists `PROJECT.md` in a tuple whose missing entries are skipped: no edit. Rewrite
  `lean4/README.md` (it describes another repository's layout and names deleted files at lines 13 to 16).
- Checks: C1, C3, C4, C5 (no `.lean` file goes), C6. Accept: tracked files fall by 140, UNTYPED by 9.

### S05 Remove dead files under code/ and the uncompiled crate roots

- Remove (34 files): `code/python/verify_pfp_dag_prompts.py` and companion (its inputs 'dag/prompts' and
  'evidence/receipts/pfp_dag_prompts' do not exist); `code/rust/data/` (2; `include_str!` in
  `code/rust/src/qm/finite_witness.rs`:8 and `entropy_bounds.rs`:253 resolves to `code/rust/src/qm/data/`, and
  `code/python/src/qm/api.py`:64 reads the Python copy); `code/rust/src/category_theory/mod.rs.legacy`;
  `code/rust/src/governance/Cargo.lock` (CI builds with `governance/Cargo.toml` and `governance/Cargo.lock`,
  governance.yml:57,60,63); `mod.rs` and companion in the 14 crates whose `Cargo.toml` `[lib] path` is `lib.rs`
  (category_theory, finite_probability, functional, fusion_categories, general_relativity, higher_category_theory,
  holonomy, homotopy_type_theory, lie_theory, local_green_global_red_lggr, majorana, number_theory, operad_theory,
  sheaf_theory). Quality records under `code/rust/quality/` name some of these paths; they are records (rule 8).
- Keep: `code/rust/src/combinatorics/mod.rs` (`lib.rs:15` reads it with `#[path]`), the root modules declared in
  `code/rust/src/lib.rs`:2-6, `code/rust/src/mub/mod.rs` (Q40 of the QM problem atlas), `code/rust/src/wdp/mod.rs`
  (S15), `code/deposit_paths.py` (`verify_deposit.py`:31-35,84).
- Before removing, `grep -n "mod.rs\|#\[path" code/rust/src/<crate>/lib.rs` prints nothing for each crate. On a
  machine with disk, `cargo check --workspace --all-targets --locked` in `code/rust` before and after must agree.
- After: `governance-check baseline --write`; C1, C3, C4, C5, C6. Accept: tracked files fall by 34, UNTYPED by 4, the
  governed population (`governance-check --root . list | wc -l`) by 15. The comment at
  `code/rust/src/governance/Cargo.toml`:22-23 about the lock file is stale; leave it for the next rebind.

### S06 Remove unread evidence and docs records; move the scoring-history guide

- Remove (312 files): run and mutation logs of `evidence/quality/pr215_l4_repair/` (181), the system-repair review
  and four run notes under `evidence/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/` (19), logs and XML of
  `evidence/quality/code_2026_10_26/` (22), `evidence/results/batches/` except the three fixtures below (19),
  dossiers, per-PR validation JSON and run notes (69), `docs/maintenance/atlas_dependency_inventory.{json,md}` (2).
- Keep, because something reads them without a literal file path:
  `evidence/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T162715Z_jordan_classical_qubit/` (40; cited by
  `pfp_review.superseded_by` at `dag/derivation_dag.json`:5423,7115 and `dag/fragments/pfp_review_decisions.json`:544,869);
  `evidence/results/batches/20261019T232430Z_prompts_112_131/tools/witness_cases.json` and
  `evidence/results/batches/20261020T000351Z_prompts_132_151/tools/{specs.py,witness_cases.json}` (built and read by
  `code/python/tests/test_l1_import_exact.py`:12-13 and `test_born_boundary_exact.py`:7-9);
  `evidence/reviews/application_branches_validation.json` (linked from `dag/derivations/README.md`:831, which
  `dag/tools/sync_application_branches.py`:167 renders); the `code_2026_10_26` files linked from
  `docs/maintenance/code_quality_2026_10_26.md`:14,15,96, `reviewed_assessment_proposal.json`
  (`governance/README.md`:19) and that folder's `.gitattributes`. Its `SHA256SUMS` keeps naming 22 removed files and
  already has 3 stale entries; nothing reads it (rule 8).
- Move `docs/CONTRACT_SCORING_HISTORY.md` to `governance/contract_scoring_history.md`; edit `docs/_config.yml`:28 and
  the links at `code/rust/quality/category_homology/README.md`:1137, `code/rust/quality/l4a_qm_six/README.md`:11,
  `code/rust/quality/l4a_six/README.md`:13 and `code/rust/quality/six_module/README.md`:233. The READMEs under
  `category_homology/` and `six_module/` are byte-bound (`.gitattributes:16,20`): if a receipt pins a README's sha256,
  leave its link and say so in the PR.
- Rewrite `evidence/results/README.md` (its heading and paths name the retired 'dag/results' and 'dag/research').
- Checks: C2 before and after prints `evidence map current` without a new `--write`; C5 needs `--write`
  (`scripts/build_readme_facts.py`:136 counts the review folders under `evidence/results/*/reviews/`); C1, C4, C6;
  `python -I -X utf8 -m pytest dag/tests/test_build_status.py dag/tests/test_docs_liquid_safe.py code/python/tests/test_born_boundary_exact.py code/python/tests/test_l1_import_exact.py -q`.
- Accept: tracked files fall by 312; UNTYPED by 17, DEAD by 2, MISSING by 1; `docs/evidence` is byte-unchanged.

### S07 Remove the duplicate WDP graph and fold the JSONL readme

- Remove `dag/wdp_derivation_dag.json`, `dag/wdp_derivation_dag.md`, `dag/theory_of_finite_qm.jsonl.README.md`. The
  WDP file's 151 nodes, 148 routes and 173 records equal their main-DAG entries field for field; no script, test or
  workflow reads it. The `.md` is a byte twin of the atlas copy.
- Append the JSONL readme to `dag/derivation_dag_reading_note.md` as a section, fix the link at its line 22 and the
  mention at `dag/tools/render_dag_views.py.doc.yaml`:15 (the companion's history keeps the old name, rule 8). Edit
  `dag/README.md`:12 and, in the WDP deposit, `QUADRANT_INDEX.md`:65,149,165,
  'docs/04_roadmap_and_gaps/README.md':36 and 'docs/04_roadmap_and_gaps/WDP_DERIVATION_DAG.md':4,36,256 to point at
  `dag/derivation_dag.json` filtered to stage WDP; then rule 6.
- Checks: C1, C2, C4, C6, rule 6 for the WDP. Accept: tracked files fall by 3, UNTYPED by 3.

### S08 Remove the stale paper copies of the atlas packages

- Decision: the atlas packages are canonical. CI runs them (`.github/workflows/projection-obstruction.yml`:6-7,26),
  the DAG cites `atlas/projection_obstruction/` and no `papers/0NN_*` path, and they are the later, reviewed
  editions: of the 165 same-path files whose bytes differ, the atlas side carries the 2026-11-05 content commits
  41743c8ec, 6803005f0 and fd07f2df2 made after the papers copy of 2026-10-27 (5209ba624); the 5 lockfiles the papers
  side bumped later pin versions the atlas twins already carry.
- Remove (623 files): the seven folders `papers/000_projection_obstruction`, `006_*`, `007_*`, `008_*`,
  `009_coordinate_wise_additivity`, `034_*`, `035_*` (574: 375 byte twins, 165 older editions, 34 papers-only files:
  LaTeX by-products, dated release zips, older `Census.lean` drafts, two `projection_vendor` lake manifests the atlas
  edition dropped by design, `034_`-prefixed twins of renamed files); `papers/032_*` (26); and
  `papers/009_conditional_density_lift_and_dual_witness_xi_functional/_support/{history,doi_assignment_*/before,doi_assignment_*/published_bytes}`
  (23, excluded from that deposit by its `verify_deposit.py`:35 and 'scripts/regen_sha256sums.py':24).
- Edit the link at `dag/derivations/20_continuum_interface/tfq_0124_gap_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_manifold.md`:47
  to `atlas/projection_obstruction/zero_container_relational_spacetime_and_witness_holonomy/code/continuum_lorentz_causality.py`
  (byte-identical). In `library.yaml` point the eight paper books at their atlas package and its main paper (032 at
  `atlas/finite_obstruction_calculus/witnessed_difference_programme`; drop the 032 and 034 entry points).
  `dag/tools/prose_proofs.py`:62 scans `papers/**/*.md`, but none of the removed files holds a proof section, so
  `dag/prose_proofs.md` does not change.
- Checks: C1, C2, C4, C5 (`--write`: the papers `.lean` count changes), C6. Accept: tracked files fall by 623, UNTYPED
  by 600; `git grep -n -E "papers/(000|006|007|008|009_coordinate|032|034|035)_"` returns only rule-8 records.

### S09 Remove the WDP deletion quadrant and the private-product application

- Remove (886 files) in `atlas/finite_obstruction_calculus/witnessed_difference_programme/`:
  'docs/03_deletion_and_archive/' (825; its README declares it deletable), 'code/coda_application/' (59; no DAG
  citation), 'code/unit_tests/test_observer_source_archive.py' and 'scripts/verify_observer_source_archive.py'.
- Edit, do not delete, the two regression files that also test kept code: in 'code/tests/test_full_audit_regressions.py'
  drop the `coda_application` imports (lines 12-19) and the six tests that use them (lines 28, 44, 84, 111, 182, 193),
  keeping its 13 other tests; in 'code/tests/test_review_gate_regressions.py' drop the import at line 18 and
  `observer.regular` from the parametrize list at line 113, keeping its 8 other tests. Leave the
  'code/coda_application/build' exclusions at `verify_deposit.py`:95 and 'scripts/regen_sha256sums.py':46, which
  `test_deposit_sweep_includes_archive_component_named_b` relies on.
- Edit kept documents of the deposit: 'scripts/verify_source_provenance.py':119 (drop the fallback into the quadrant),
  'code/derivation_controls/plan_wdp_editorial/witness.py':139,142 (report the two deleted manifests as absent or drop
  the checks), `README.md`:47,53, 'docs/README.md':22, `QUADRANT_INDEX.md`:64,125,132,
  'docs/01_substantiated/coda_mathematical_decomposition.md':88, 'docs/01_substantiated/coda_prime_integration.md':27,
  'docs/01_substantiated/consolidation_validation.md':60,
  'docs/04_roadmap_and_gaps/source_replay_and_remaining_derivations.md':154, and `source_provenance.json`; then rule 6
  (both manifests list 884 removed paths).
- Checks, from the deposit root before and after: `python -I -X utf8 -m pytest -q` (testpaths 'code/unit_tests' and
  'code/tests'); the failing set after is the set before minus the removed tests. C1, C4, C6. Accept: tracked files
  fall by 886, UNTYPED unchanged; `git grep -n "03_deletion_and_archive\|coda_application"` returns only rule-8
  records and the two exclusion lines.

### S10 Remove the other atlas leftovers and the last archive folder

- Remove (140 files): the 126 raw `.log` transcripts under `atlas/finite_obstruction_calculus/genesis_ongoing/meta/review/`
  (each folder keeps its `summary.json`, which names the logs as a record; no code reads them),
  `genesis_ongoing/AGENTS.md`, the two `PR_*_BODY.md` drafts, the predecessor papers in
  `symmetric_groups_and_minimal_symbol_systems/source_archive/` (9), and the LaTeX `.aux` and `.log` of
  `certified_adaptive_quantum_dynamics`.
- Rename the one DAG-cited file left there, `source_archive/000_sn/paper_claim_ledger.md`, to
  `atlas/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/docs/sn_predecessor_claim_ledger.md`
  (the owner's rule allows no archive folder). Edit its owning fragment `dag/fragments/pregenesis_to_wdp.json`:7727
  and follow rule 2, which rewrites `dag/derivation_dag.json`:18449,
  `dag/derivations/05_mssn_sn/tfq_0510_sn_two_boxed_laws.md`:61 and the evidence pages; reword the links to the
  deleted `source_archive/README.md` at the deposit's `README.md`:7, `paper.md`:477 and `paper.tex`:781 (the sentence
  only).
- Keep three intentional twins: the higher-cell `claim_ledger.md` (`verify_deposit.py`:127-128,
  'code/tests/test_claim_evidence.py':25), `covering_edge_descent.md` ('code/monograph_narrative_harmonizer.py':42,
  `README.md`:58) and the pregenesis 'lean4/full_axiom_report.txt' (`tools/replay_full_axiom_census.py`:94).
- Rule 6 for `symmetric_groups_and_minimal_symbol_systems` (6 stale entries at the merged tip) and
  `certified_adaptive_quantum_dynamics` (11 and 12); drop the entries from `atlas/PROVENANCE.json`.
- Checks: C1, C2, C4, C6. Accept: tracked files fall by 140, UNTYPED by 1; no folder named `source_archive` remains.

### S11 Education: take in the problem set and the teaching pack, drop twins and placeholders

- Move `problem_sets/` to `education/problem_sets/` (46 files) and
  `dag/derivations/11_finite_qm_dynamics/hamilton_noether_sources/` to `education/hamilton_noether_sources/` (43;
  `render_sheets_v5.py` imports v4 and v3, so it moves whole). Remove the three `problem_sets/**/.gitkeep` and the
  byte-twin `rust_run.log` (4 files).
- Problem-set edits: `results/undergraduate_qm_25/verify.py`:26-27 (`ROOT = HERE.parents[3]`, catalog path
  `education/problem_sets/problems/undergraduate_qm_25.yaml`); in `problems/undergraduate_qm_25.yaml` replace
  `problem_sets/` by `education/problem_sets/` (lines 21, 23, 31, 32 and every `solution:` line); recorded `.log`
  results keep their text (rule 8); `scripts/scan_lean_references.py`:131 scans the folder name `problem_sets`, so
  make it `education/problem_sets`; the `library.yaml` book `problem_sets` gets path `education/problem_sets`.
- Pack edits: the links at `dag/derivations/11_finite_qm_dynamics/dynamics_hamilton_noether.md`:47-48,
  `dag/derivations/12_finite_qm_structure/records_and_interpretations.md`:25 and
  `dag/derivations/first_mark_to_quantum_gravity.md`:61.
- Remove in education (51 files): the 14 byte twins that nothing reads or links (`3_minimal_symbol_systems/domains/physics/hypothesis_ledger.md`,
  `3_minimal_symbol_systems/domains/cosmology_astrophysics/lean4/cosmology_core.lean`, four
  `5_genesis_reading_notes/normal_forms/nf.*.yaml`, two `8_witnessed_difference_programme/normal_forms/nf.evidence.*.yaml`,
  and the six modules of the package `3_minimal_symbol_systems/lean4/`, which goes whole with its lakefile, manifest,
  toolchain pin and README, 4 files); 27 `.gitkeep` files; 4 stub READMEs; `4_genesis_primitives/archive/` (2).
- Keep 30 twins: the five that `dag/` cites (`1_pregenesis_empty_mark/grammar/pre_genesis.ebnf`,
  `1_pregenesis_empty_mark/sources/analysis_derivation_v1.md`, `2_symmetric_group_presentations/lean4/SnCarrier.lean`,
  `.../SnTheorems.lean`, `3_minimal_symbol_systems/grammar/mssn.ebnf`; Q8); `2_symmetric_group_presentations/lean4/SnSyntax.lean`,
  a root of that package's `lakefile.lean` that `SnCarrier.lean`:1, `SnTheorems.lean`:1 and `SnOffImage.lean`:1 import;
  and 24 that their own module reads by building the path or links: the grammar and conformance files
  (`check_pre_genesis.py`:5, `check_sn.py`:1,16, `check_mssn.py`:16 and their tests), the four
  `normal_form_contract_schema.yaml` (`2_symmetric_group_presentations/code/sn_audit.py`:384,
  `8_witnessed_difference_programme/code/wdp_audit.py`:514, and the `schema_ref: ./normal_form_contract_schema.yaml` of 60
  contracts), seven contracts that `8_witnessed_difference_programme/code/tests/test_wdp_audit.py`:298-310 loads, and
  the files that module READMEs link.
- Edit the links to removed files: `2_symmetric_group_presentations/README.md`:41 and `3_minimal_symbol_systems/README.md`:25
  (stub 'papers/README.md'), `4_genesis_primitives/README.md`:46 and `4_genesis_primitives/genesis.md`:9 (`archive/README.md`),
  `3_minimal_symbol_systems/README.md`:38 (to `atlas/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/`).
  Record every removal in `education/IMPORT_PROVENANCE.json` `post_import_edits` (and its lines 194 and 3746 for the
  archive folder), and fix the file-count table of `education/README.md`.
- Checks: `python -B education/problem_sets/results/undergraduate_qm_25/verify.py` and its `test_verify.py` before
  (old path) and after; the module suites that read the kept twins, `python -m pytest -q
  education/2_symmetric_group_presentations/code/tests education/3_minimal_symbol_systems/code/tests
  education/8_witnessed_difference_programme/code/tests`, with the same result before and after;
  `python -X utf8 -m pytest -q dag/tests/test_source_consolidation.py`; C1, C2, C4, C6.
- Accept: `problem_sets/` is gone; tracked files fall by 55 and 89 move; UNTYPED falls by 93, DEAD by 14, MISSING by 2;
  the verifier output is unchanged.

### S12 Move the four foreign tests out of dag/tests

- Move `dag/tests/test_build_status.py`, `test_docs_liquid_safe.py`, `test_readme_facts.py` and
  `test_readme_facts.contract.score.yaml` to `scripts/`, and `dag/tests/test_foc035_lp_certificates.py` with its
  companion to `checks/tests/`.
- Edit `ROOT = Path(__file__).resolve().parents[2]` to `parents[1]` in the three `scripts/` tests
  (test_build_status.py:13, test_docs_liquid_safe.py:6, test_readme_facts.py:11); the checks test keeps `parents[2]`.
  Repoint `.github/workflows/status.yml`:54, `.github/workflows/reviewed-checkers.yml`:305, `README.md`:45,
  `scripts/build_readme_facts.py`:13 and `checks/tests/README.md`:240. The two companions move unchanged: neither file
  is governed, and `scripts/contract_scores.py check` verifies only history bytes and current pointers
  (scripts/contract_scores.py:330-345, 368-395).
- Checks: the four tests at their new paths; C1, C4, C6; reviewed-checkers.yml runs. Accept: `dag/tests/` holds only
  tests of the graph and its tools; UNTYPED unchanged.

### S13 Retire the l4a_six staging snapshot (Q3)

- Remove (151 files): `code/rust/quality/l4a_six/scalar_port/` (136) and `ordered_port/` (3), activated into live
  `src` on 20261020T104119Z, and the six replay tools that only read them with their companions
  (`activate_scalar_port.py`, `scalar_port_check.py`, `scalar_port_composition.py`, `scalar_port_methods.py`,
  `activate_ordered.py`, `ordered_trial.py`): they build `Path(__file__).parent/'scalar_port'` or `'ordered_port'`.
- Keep `scalar_port_faults.py` and its companion: its `block` is imported by `curvature_faults.py`:2,
  `hott_model_faults.py`:2, `ordered_fault_recipes.py`:2, `pi_trial.py`:14 and `prepare_initial_empty.py`:7, and
  `mutations.py`:205 runs its `recipes` against the live `src` (and hashes it at lines 309, 409, 425).
- The receipts the snapshot served already left the tree in commit 1271b737a. Edit
  `code/rust/quality/l4a_six/README.md` to say that the snapshot lives in git history (88fa973cc), and drop the dead
  attribute line `.gitattributes:101`.
- After: `governance-check baseline --write`; C1, C3, C4, C5, C6. Accept: tracked files fall by 151;
  `python -I -X utf8 -B -c "import sys; sys.path[:0]=['code/rust/quality/l4a_six']; import scalar_port_faults, curvature_faults, hott_model_faults, ordered_fault_recipes, pi_trial, prepare_initial_empty, mutations"`
  succeeds before and after; governance CI passes.

### S14 Fold reviews/ into checks/review_ledger (Q4)

- Move `reviews/repository_file_review/` to 'checks/review_ledger/' (423 files), and
  `reviews/projection_obstruction_outside_review_2026-11-05/` and `reviews/projection_obstruction_review/` to
  `evidence/reviews/` (5 files); remove the 21 files of the `retired_*` folders.
- Edit, in one commit: `.github/workflows/reviewed-checkers.yml`:7,14 (drop the `reviews/` filters; `checks/**`
  covers the ledger) and :46 ('checks/review_ledger/current_file_scores.json'); `.gitattributes:167-168`
  (`checks/review_ledger/**`); `checks/tests/test_gaussian_tomography_controls.py`:37,
  `checks/tests/test_hubbard_transfer.py`:288 and `checks/tests/test_temporal_cycles.py`:384,432
  (`CHECKS.parent/'reviews/repository_file_review'` becomes `CHECKS/'review_ledger'`); the prose links at
  `atlas/README.md`:84,86, `checks/checker_support/README.md`:40,91, `checks/tests/README.md`:55,72,88,
  `dag/derivations/independent/ads-cft-duality-import.md`:104,
  `dag/derivations/independent/fsp-hubbard-protected-representations.md`:98, and line 25 of
  `atlas/projection_obstruction/{projection_obstruction_paper,higher_cell_cochain_projection_and_retraction_dynamics}/docs/review_2026_11_05.md`
  (then rule 6 for those two packages, which projection-obstruction.yml checks). The 121 checks companions that name
  the old ledger path inside their histories keep it (rule 8).
- Rebind the three edited tests with unchanged grades. Their ledger rows pin source and companion sha256 and require
  an L4 or L5 score with every gate at B or better (reviewed-checkers.yml:51-65). `score_scope_contracts.py record`
  refuses them (it calls `language_for`, scripts/score_scope_contracts.py:252-256 via line 678, and `checks/` is no
  governed population), so append the records with the module's own helpers, as `command_record` (lines 665-693)
  does, with language `Python` as reviewed-checkers.yml:56 passes it. For each test T:
  `python -I -X utf8 -c "import sys,copy; sys.path.insert(0,'scripts'); import score_scope_contracts as s; t=sys.argv[1]; src=s.ROOT/t; c=s.companion_for(src); d=s.parse_document(c); h=s.sha256(src.read_bytes()); k=copy.deepcopy(d['contract']); r=copy.deepcopy(s.history_entry(d,'scoring_history',d['current_scoring'])['record']); k['artifact']['sha256']=h; r['artifact']['sha256']=h; assert s.score_error(r,t,h,'Python') is None; l=s.rel(c)+'#path-rebind'; d['current_contract']=s.append_history(d,'contract_history',k,l); d['current_scoring']=s.append_history(d,'scoring_history',r,l); d['contract']=k; s.atomic_write(c,s.canonical_json(d))" T`;
  then set the six sha256 values (three sources, three companions) in 'checks/review_ledger/current_file_scores.json'.
- Checks: run lines 37-68 of reviewed-checkers.yml as a script before and after, and the three tests in normal and
  `-O` mode; C1, C2, C4, C6. Accept: `reviews/` is gone; reviewed-checkers.yml passes on Python 3.12 and 3.14;
  tracked files fall by 21 and 428 move; UNTYPED falls by 449, DEAD by 8, MISSING by 3.
- If the owner declines: keep `reviews/` as a top-level folder, give the `ReviewLedger` class `path:
  reviews/repository_file_review` in checks.type.yaml and add `reviews` to the root attributes.

### S15 Wire or remove the uncompiled Rust (Q11)

- Scope (members `unwired_sources` and `unwired_tests`, UNSURE): `code/rust/src/wdp/derivation_controls/` and
  `wdp/mod.rs` (`wdp/lib.rs` declares no `mod derivation_controls`), `code/rust/src/mub/bin/`
  (`code/rust/src/mub/Cargo.toml`:6 has `autobins = false` and no `[[bin]]`), `wdp/bin/`, `mub/native/`,
  `code/rust/tests/mub/**/*.rs` (no `[[test]]`, no `tests/mub/main.rs`), and the receipt
  `code/rust/src/mub/runs/mub6/szollosi_triad_search_receipt.json` that `mub/native/szollosi_triad_solver.rs`:477-478
  writes: 533 files with companions by a static mod-graph walk (macros and `include!` not expanded).
- Do, per family, on a machine with cargo and disk: register it (`[[bin]]`, `[[test]]` or `mod`) and run
  `cargo test --locked -p <crate>` from `code/rust`; keep it if it compiles and passes, else remove the family with its
  companions and `governance-check baseline --write`.
- Accept: invariant `rust.every_source_reachable` holds; C3 passes; C5 `--write` for the Rust test-function count.

### S16 Repair broken paths (owner-approved re-pin of the lakefile)

- `lean4/lakefile.lean`:986 and :1016 set `srcDir` to `../atlas/papers/finite_obstruction_calculus/...`; `atlas/papers/`
  does not exist since the atlas fold (atlas/README.md:32-33), so `GenesisSealedSource`, `GenesisOngoingSource` and the
  libraries that reuse them cannot build. Change both to `../atlas/finite_obstruction_calculus/...`. The lakefile is
  in `governance/baseline.json`:3375 (deficit FLOOR, sha256 a5bd8da3...): replace the sha256 and append to `reason`
  "Rebound on <date>: srcDir of GenesisSealedSource and GenesisOngoingSource repaired after the atlas fold; score
  unchanged.", and rebind `lean4/lakefile.contract.score.yaml` to the new bytes with the unchanged score
  (`scripts/score_scope_contracts.py record`; the lakefile is governed). The lakefile bytes also sit in replay pins:
  12 receipts under `evidence/lean_receipts/` pin `lean4/lakefile.lean`, and governance.yml:70-71 verifies them
  (`scripts/replay_fqcd_lean.py --verify-receipt`, `scripts/replay_pr492_lean.py --verify-receipts`). Their migration
  rule (scripts/replay_fqcd_lean.py:28-75, `evidence/lean_receipts/lean_replay_pin_migrations.json`) accepts only
  added whole `lean_lib` stanzas, so a `srcDir` edit needs fresh replays on a machine with Lean (the two scripts
  without the verify flag), or the owner's choice to extend that rule. Main already fails that step: #577 added a
  root without a migration record (governance run 42294333196, "Stale replay pin: lean4/lakefile.lean"). Checks: C3;
  `governance-check explain lean4/lakefile.lean` shows it grandfathered; `lake build GenesisSealedSource
  GenesisOngoingSource` from `lean4/`; the two replay verifications; lean-gleason.yml passes.
- Rename the run-contract file at the genesis_ongoing root (the 344 KB Markdown file, blob e5d97eed, whose upper-case
  name names an AI model) to `atlas/finite_obstruction_calculus/genesis_ongoing/run_contract.md`. Edit
  `dag/derivation_dag.json`:2041 and :32723 (node PG-GEN-SAMENESS-REFINEMENTS and route PG-R-SAMENESS; no fragment owns
  them), follow rule 2, repoint `atlas/PROVENANCE.json`:16403, and repoint every hit of the old name inside `atlas/`
  and `education/5_genesis_reading_notes/` (education edits go into `post_import_edits`). C1, C2.
- The missing 'checks/exact_checkers/campaign/README.md' (deleted in a992b578d) is named by 19 files. Leave
  `scripts/build_status.py`:61 (it handles the absence, lines 350-352); reword the sentence in the other 18:
  `.agents/patterns/README.md`:35, seven files of the agent-configuration dot folder
  (`git grep -l "exact_checkers/campaign" -- ':(glob).*/**'`), `education/6_genesis_foundations/this_repo.md`,
  `dag/derivations/20_continuum_interface/tfq_0123_gap_f002_s000_002_carrier_mismatch_and_gap_f002_s000_001_supergravity_triangulation_stay_open.md`
  and `dag/derivations/independent/{pgw-sn-protected-answer-transport,tfq-0006,tfq-0033,tfq-0039,tfq-0050,tfq-0106,tfq-0123,tfq-0376}.md`.
  Never touch the first line of an independent note (overclaim rule R8). C4 includes the skill audit.
- Live documents that still name 'dag/results/' or 'dag/research/': list them with
  `git grep -l -E "dag/(results|research)/" -- . ':!*.contract.score.yaml' ':!*.doc.yaml' ':!evidence/' ':!checks/review_ledger/' ':!docs/overclaim/' ':!docs/maintenance/' ':!docs/evidence/' ':!dag/evidence/evidence_map.json' ':!governance/approvals/'`
  and fix only README files, the front page, root documents, site pages and tool docstrings in `scripts/` and
  `dag/tools/`; every other hit is a record (rule 8).
- Accept: invariant `lean4.srcdirs_resolve` holds; C1 to C4 pass; UNTYPED, DEAD and MISSING fall by 1, 2 and 1, which
  brings all three to 0.

### S17 Naming

- Rename `code/rust/src/wdp/PO000_24G2.md` to `po000_24g2.md` (no tracked file names it) and
  `evidence/quality/full_functor_validation/REVIEW.md` to `review.md` (`git grep -n "full_functor_validation/REVIEW"`
  returns nothing). Every other name satisfies a rule of the root file; the two named exceptions
  (`docs/QM_PROBLEM_AND_PROOF_ATLAS.md`, read at that path by `scripts/verify_qm_atlas_loc.py`:15,53, and
  `lean4/RENAMES.json`, cited by `governance/baseline.json` reasons) are rule `exception`. The DAG-id names of the
  1,023 evidence pages are kept (rule `dag_id`): lower-casing them would touch 602 literal citations in 62 files, some
  inside hashed companion text.
- Accept: `scripts/check_repo_types.py --report naming` lists only `imported` and `exception` names.

### S18 Public text, stage A: free prose and tooling

- Scope: the 3,030 files that hit the rule after the removals, minus stages B to D: 500 files (330 in `code/`, mostly
  quality READMEs and assessment JSON whose assessor field names a tool; 124 in `papers/`; 18 in the
  agent-configuration dot folder, all because the folder name is a hit, see Q14; 9 in `scripts/`; 7 at the root; 12
  elsewhere). `--report public-text` lists them.
- Do: reword each hit neutrally ("a coding assistant", "the private engine project", "the upstream repository"). Do
  not edit a file under a `.gitattributes` `-text` rule or whose sha256 a receipt records: list it for stage C. Do not
  rename a file a DAG field cites (S16 procedure only).
- Accept: stage A is 0 apart from the listed exceptions; C1, C2, C4 pass.

### S19 Public text, stage B: governed sources, DAG sources and generated pages

- Scope: 61 governed sources, 223 DAG sources and derivation pages, 29 generated pages. Generated pages follow their
  sources by regeneration. Each governed source needs a rebound companion (rule 5) and owner approval per batch; DAG
  text follows `dag/README.md` "Change" and changes no status. A Lean module whose name carries a hit is renamed only
  with `lean4/RENAMES.json`, the lakefile root, the baseline entry and every DAG citation in one commit.
- Accept: stage B is 0; C1 to C4 pass.

### S20 Public text, stages C and D: records and imported trees (Q2, Q5)

- Scope: 677 companions and manifests, 350 records, 606 files of imported trees (atlas, normal_forms/contracts,
  education) and 584 vendored files. 49 of all remaining hits are in a path.
- Recommended: records and imported trees are not rewritten; `public_text.allow` gains one entry per class of
  immutable record, with its reason, and imported trees are re-imported from a scrubbed upstream revision when the
  owner has one. Paths that carry a hit are renamed with their ledgers in one commit.
- Accept: `--report public-text` lists only allowed classes.

### S21 Census tables on demand (Q1, optional)

- The 516 census tables (`.csv`, `.jsonl`; 248.9 MB) under `atlas/finite_obstruction_calculus/genesis_ongoing/evidence/`
  are deterministic: the senior review ran all 25 generators with `--check` from the genesis_ongoing folder and each
  reported a match (4,041 s in all). They stay committed here because each `--check` compares the committed folder
  with a fresh run in both directions ('code/tenth/__main__.py':3-4,65-68), so deleting them would break the check.
- If the owner wants them out: make each generator compare the fresh run with its `MANIFEST.sha256` (which lists every
  table with its sha256), run every `--check`, then remove the tables and keep `MANIFEST.sha256`, `summary.json`,
  `given.json`, `counts.csv` and `lean_axioms.txt`; add one CI job that runs the fast generators.
- Accept: every generator's `--check` passes against the manifests; the `census_tables` target in atlas.type.yaml is
  updated.

### S22 Make the checker blocking

- Precondition: S01 to S14 and S16 are merged (S15 is not needed: its files are typed either way), and the owner has
  answered Q2 and Q5 (so S20 has an allow list).
- Do: refresh every `now` and `target` in `governance/types/*.type.yaml` to the merged tree (the checker prints them),
  remove `continue-on-error` from the dag.yml step and add `--strict`. Keep `--report naming` and
  `--report public-text` as non-blocking steps until S17 to S20 are done, then make them part of `--strict`.
- Accept: on main `scripts/check_repo_types.py --strict` exits 0.

## 5. Out of scope

DAG statuses, new DAG nodes, node statements and routes; the mathematical content of papers, Lean, Rust or Python;
re-scoring any source beyond the rebinds of S14 and S16; changing `governance/policy.json`; building the whole Rust
workspace or every Lake library in CI (Q11); the content of vendor/ (Q5).

## 6. Risks and how the stories avoid them

| Risk | Where | Guard |
|---|---|---|
| A deletion breaks code that builds a path or imports a module by name, which a literal-path search misses | S06, S09, S13 | the consumers this review found are kept or edited by name; C7 plus the package tests and the S13 import check before and after |
| A deposit manifest is resealed over unreviewed drift | S07, S09, S10, S14 | rule 6 records the stale entries before regenerating |
| A twin that code reads on purpose is merged away | S10, S11 | the twins that code or a lakefile reads stay and are named |
| Editing a governed or reviewed source voids its pin | S14, S16, S19 | only those stories edit such files, each with an explicit rebind and owner approval |
| Generated pages drift again | all | S02 makes `build_evidence.py --check` blocking |
| The DAG validator fails, or a DAG field dangles, on a cited path | S06, S08, S10, S16 | no DAG-cited file is removed; the two renames change their citations through rule 2 |
| A moved test no longer finds the root | S11, S12 | the `parents[n]` edits are named |
| A CI path filter stops triggering | S14 | `checks/**` covers the new ledger path; the old filter lines go in the same commit |
| A consumer outside the repository breaks | S03 | `library.yaml` stays, read by the sibling repository's library checker |
| The scrub rewrites pinned bytes | S18 to S20 | hash-bound and imported files are a separate, owner-gated stage |
| Line endings change on Windows | S06, S11 | nested `.gitattributes` files of kept folders are kept and moved with their folders |

## 7. Open questions for the owner

| Id | Question | Recommendation |
|---|---|---|
| Q1 | Keep the 248.9 MB of genesis census tables committed, or rebuild them on demand (S21)? | Rebuild on demand, after each `--check` compares against `MANIFEST.sha256`. |
| Q2 | Must paths inside historical records keep resolving? This decides the UNSURE evidence and review files and stage C. | No. Records keep what they recorded; delete raw run logs that only histories name, keep structured receipts. |
| Q3 | Retire the l4a_six staging snapshot and six of its seven replay tools (S13)? | Yes; `scalar_port_faults.py` stays because six kept modules import it. |
| Q4 | Fold reviews/ into checks/review_ledger, rebinding three reviewed tests with unchanged grades by the S14 helper call? | Yes, after S01 to S13 are green. |
| Q5 | May vendored and imported bytes be edited for public text? | No; re-vendor or re-import from a scrubbed upstream revision, and allow-list until then. |
| Q6 | Move the four root deposit-verifier files to scripts/? It needs an edit of the baselined test `code/python/tests/test_deposit_verifier_evidence.py`:16. | Keep them at the root until that test is re-scored for another reason. |
| Q7 | Are `.doc.yaml` companions required, optional or retired? No tool reads them. | Optional; keep the existing ones, require none. |
| Q8 | Repoint the 30 education twins that S11 keeps (5 cited by the DAG through `dag/fragments/pregenesis_to_wdp.json`, 25 read or linked inside their module) to their canonical copies and delete them? | Yes, as a follow-up story per module; it edits imported files, so each edit goes into `post_import_edits`. |
| Q9 | `library.yaml` stays at the root because the sibling repository's library checker reads it (its master list names `catalog: library.yaml`). Keep it, or move the catalog and update that checker in the same change? | Keep it; the types reference it and check its paths. |
| Q10 | The nested workflow in genesis_ongoing never runs. Promote its checks to a root workflow, or delete it? | Delete it with `genesis_ongoing/ci/` unless the owner wants those checks in CI. |
| Q11 | Add CI for the Rust workspace, the root pytest suite (285 Python files under code/python/tests) and dag/tests? None runs today. | Yes, non-blocking first; required before S15. |
| Q12 | 116 of 158 independent checkers are run by neither CI nor a test. Run them or retire them with their notes? | Add them to reviewed-checkers.yml in batches; retire only with the owner. |
| Q13 | `scripts/adversarial_witness_stress_test.py` is called by nothing. | Delete. |
| Q14 | The agent-configuration dot folder's own name is a public-text hit (18 files). | A typed allow entry: the tool fixes the name. |
| Q15 | lean4/Imported holds namespace-rewritten copies of 229 originals tracked byte for byte elsewhere (223 under atlas/finite_obstruction_calculus); 86 originals are not in the repository; 30 modules changed after import. Keep both sides? | Keep both; the import manifests make the copy a `derives_from` relation (invariant `imported.originals_bound`). |
| Q16 | Lower-case the 1,023 DAG-id evidence page names? | No (rule `dag_id`). |
| Q17 | The public-text rule hashes whole words, so ordinary words that are also product names and journal titles in bibliographies that contain a banned word are hits. Reword them, or allow-list bibliographies? | Allow-list reference lists per file with a reason; reword prose. |

## 8. Appendix: paths

Each line is tagged with its story. A line `src -> dst` moves a file, or a folder when `src` ends in `/`; moves
apply in the order listed. Every other tagged line removes one path, a whole folder (a trailing `/`), or the files
a glob matches (`*` stays in one folder, `**` crosses folders, `{a,b}` is a choice), and says `(N files)` when it
covers more than one. A `KEEP` line names a file that stays although a removal line matches it. Removals take
precedence over moves. `scripts/check_repo_types.py --plan Snn` applies these lines to `git ls-files` (S01).

### Moves

```text
S06  docs/CONTRACT_SCORING_HISTORY.md -> governance/contract_scoring_history.md
S10  atlas/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/source_archive/000_sn/paper_claim_ledger.md -> atlas/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/docs/sn_predecessor_claim_ledger.md
S11  problem_sets/ -> education/problem_sets/
S11  dag/derivations/11_finite_qm_dynamics/hamilton_noether_sources/ -> education/hamilton_noether_sources/
S12  dag/tests/test_build_status.py -> scripts/test_build_status.py
S12  dag/tests/test_docs_liquid_safe.py -> scripts/test_docs_liquid_safe.py
S12  dag/tests/test_readme_facts.py -> scripts/test_readme_facts.py
S12  dag/tests/test_readme_facts.contract.score.yaml -> scripts/test_readme_facts.contract.score.yaml
S12  dag/tests/test_foc035_lp_certificates.py -> checks/tests/test_foc035_lp_certificates.py
S12  dag/tests/test_foc035_lp_certificates.contract.score.yaml -> checks/tests/test_foc035_lp_certificates.contract.score.yaml
S14  reviews/repository_file_review/ -> checks/review_ledger/
S14  reviews/projection_obstruction_outside_review_2026-11-05/ -> evidence/reviews/projection_obstruction_outside_review_2026-11-05/
S14  reviews/projection_obstruction_review/ -> evidence/reviews/projection_obstruction_review/
S16  the run-contract file at the genesis_ongoing root (blob e5d97eed) -> atlas/finite_obstruction_calculus/genesis_ongoing/run_contract.md
S17  code/rust/src/wdp/PO000_24G2.md -> code/rust/src/wdp/po000_24g2.md
S17  evidence/quality/full_functor_validation/REVIEW.md -> evidence/quality/full_functor_validation/review.md
```

### Removals (2,366 files) and kept exceptions

```text
S03  rules/
S04  PROJECT.md
S04  lean4/Imported/roots.txt
S04  lean4/Imported/roots_programmes.txt
S04  lean4/lakefile.campaignMajorana.contract.score.yaml
S04  lean4/majorana_axiom_report.txt
S04  lean4/qm*.md  (125 files)
S04  scripts/atlas_import/  (6 files)
S04  scripts/build_l4e_contracts.py
S04  scripts/lean_replay_campaign/lakefile_roots.py
S04  test_infra.md
S04  test_ready.md
S05  code/python/verify_pfp_dag_prompts.contract.score.yaml
S05  code/python/verify_pfp_dag_prompts.py
S05  code/rust/data/  (2 files)
S05  code/rust/src/category_theory/mod.*  (3 files)
S05  code/rust/src/governance/Cargo.lock
S05  code/rust/src/{finite_probability,functional,fusion_categories,general_relativity,higher_category_theory,holonomy,homotopy_type_theory,lie_theory,local_green_global_red_lggr,majorana,number_theory,operad_theory,sheaf_theory}/mod.{rs,contract.score.yaml}  (26 files)
S06  docs/maintenance/atlas_dependency_inventory.json
S06  docs/maintenance/atlas_dependency_inventory.md
S06  evidence/dossiers/*.md  (11 files)
S06  evidence/governance/pr215-independent-review/**  (3 files)
S06  evidence/quality/code_2026_10_26/*.log  (17 files)
S06  evidence/quality/code_2026_10_26/audit-negative-controls.json
S06  evidence/quality/code_2026_10_26/post-suite-docstrings.json
S06  evidence/quality/code_2026_10_26/preserved-artifacts.json
S06  evidence/quality/code_2026_10_26/python-before.xml
S06  evidence/quality/code_2026_10_26/python-intermediate.xml
S06  evidence/quality/full_functor_validation/final_validation.json
S06  evidence/quality/full_functor_validation_attempt1/receipt.json
S06  evidence/quality/functor_shell_pr/final_validation.json
S06  evidence/quality/functor_shell_pr/review_veri*.json  (3 files)
S06  evidence/quality/functor_shell_validation/final_validation.json
S06  evidence/quality/pr201_integration_review.json
S06  evidence/quality/pr214_integration_review.json
S06  evidence/quality/pr215_l4_repair/*.log  (7 files)
S06  evidence/quality/pr215_l4_repair/combined_custody.json
S06  evidence/quality/pr215_l4_repair/contract_coverage.json
S06  evidence/quality/pr215_l4_repair/final/  (7 files)
S06  evidence/quality/pr215_l4_repair/mutations/mutant-0*.log  (150 files)
S06  evidence/quality/pr215_l4_repair/pr244_*.json  (4 files)
S06  evidence/quality/pr215_l4_repair/receipt.json
S06  evidence/quality/pr215_l4_repair/support_mutations/mutant-000*.log  (3 files)
S06  evidence/quality/pr215_l4_repair/support_mutations/preflight_failure.json
S06  evidence/quality/pr215_l4_repair/support_policy_replay/*.log  (6 files)
S06  evidence/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/reviews/20261020T143852Z_system_repair_audit/  (15 files)
S06  evidence/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T205000Z_effect_valuation_lean/next_steps.md
S06  evidence/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T205000Z_effect_valuation_lean/review.md
S06  evidence/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T224000Z_gaussian_hermitian_carrier/next_steps.md
S06  evidence/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T224000Z_gaussian_hermitian_carrier/review.md
S06  evidence/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/next_steps.md
S06  evidence/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps/next_steps.md
S06  evidence/results/FQ-GAP-STONE-CONTINUOUS-TIME/runs/20261020T225000Z_discrete_time_spec/next_steps.md
S06  evidence/results/FQ-GAP-STONE-CONTINUOUS-TIME/runs/20261020T225000Z_discrete_time_spec/review.md
S06  evidence/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T182843Z_pr144/review.json
S06  evidence/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T200001Z_pr147/review.json
S06  evidence/results/FQ-GAP-U1-CIRCLE/runs/20261020T223000Z_u1_phase_completion_lean/next_steps.md
S06  evidence/results/FQ-GAP-U1-CIRCLE/runs/20261020T223000Z_u1_phase_completion_lean/review.md
S06  evidence/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form/next_steps.md
S06  evidence/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner/next_steps.md
S06  evidence/results/batches/**  (19 files)
S06  evidence/reviews/lean_replay_campaign/  (2 files)
S06  evidence/reviews/pr243_review_validation.json
S06  evidence/reviews/pr492/  (10 files)
S06  evidence/reviews/pr500/*.txt  (9 files)
S06  evidence/reviews/pr500/anchors.json
S06  evidence/reviews/pr500/axiom_reports.json
S06  evidence/reviews/pr_320_independent_review_validation.json
S06  evidence/reviews/pr_373_joint_import_and_registry_validation.json
S06  evidence/reviews/pr_390_combined_validation.json
S06  evidence/reviews/pr_391_combined_validation.json
S06  evidence/reviews/pr_392_combined_validation.json
S06  evidence/reviews/prompt_retention_challenges.json
S06  evidence/reviews/prompt_retention_targeted_validation.json
S06  evidence/reviews/tfq-1052-correction/  (5 files)
S07  dag/theory_of_finite_qm.jsonl.README.md
S07  dag/wdp_derivation_dag.json
S07  dag/wdp_derivation_dag.md
S08  papers/000_projection_obstruction/  (177 files)
S08  papers/006_vector_and_quantum_observer_geometries/  (68 files)
S08  papers/007_m_compatible_gauge_classification/  (69 files)
S08  papers/008_so_k_invariant_gauge_classification/  (87 files)
S08  papers/009_conditional_density_lift_and_dual_witness_xi_functional/_support/doi_assignment_2026_10_23_23604860/before/  (14 files)
S08  papers/009_conditional_density_lift_and_dual_witness_xi_functional/_support/doi_assignment_2026_10_23_23604860/published_bytes/  (2 files)
S08  papers/009_conditional_density_lift_and_dual_witness_xi_functional/_support/history/  (7 files)
S08  papers/009_coordinate_wise_additivity/  (65 files)
S08  papers/032_witnessed_difference_finite_distinction_carriers_and_history_escape/  (26 files)
S08  papers/034_higher_cell_cochain_projection_and_retraction_dynamics/  (89 files)
S08  papers/035_zero_container_relational_spacetime_and_witness_holonomy/  (19 files)
S09  atlas/finite_obstruction_calculus/witnessed_difference_programme/code/coda_application/  (59 files)
S09  atlas/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_observer_source_archive.py
S09  atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/03_deletion_and_archive/  (825 files)
S09  atlas/finite_obstruction_calculus/witnessed_difference_programme/scripts/verify_observer_source_archive.py
S10  atlas/finite_obstruction_calculus/genesis_ongoing/AGENTS.md
S10  atlas/finite_obstruction_calculus/genesis_ongoing/meta/review/PR_A_BODY.md
S10  atlas/finite_obstruction_calculus/genesis_ongoing/meta/review/PR_B_BODY.md
S10  atlas/finite_obstruction_calculus/genesis_ongoing/meta/review/baseline/*.log  (51 files)
S10  atlas/finite_obstruction_calculus/genesis_ongoing/meta/review/repair_logs/  (23 files)
S10  atlas/finite_obstruction_calculus/genesis_ongoing/meta/review/repair_suite/*.log  (52 files)
S10  atlas/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/source_archive/**  (9 files)
S10  atlas/projection_obstruction/certified_adaptive_quantum_dynamics/certified_adaptive_quantum_dynamics.aux
S10  atlas/projection_obstruction/certified_adaptive_quantum_dynamics/certified_adaptive_quantum_dynamics.log
S11  education/2_symmetric_group_presentations/papers/
S11  education/3_minimal_symbol_systems/domains/cosmology_astrophysics/lean4/cosmology_core.lean
S11  education/3_minimal_symbol_systems/domains/physics/hypothesis_ledger.md
S11  education/3_minimal_symbol_systems/lean4/  (10 files)
S11  education/3_minimal_symbol_systems/papers/
S11  education/4_genesis_primitives/archive/  (2 files)
S11  education/5_genesis_reading_notes/curriculum/600_genesis_ongoing_overview/scripts/.gitkeep
S11  education/5_genesis_reading_notes/curriculum/600_genesis_ongoing_overview/videos/
S11  education/5_genesis_reading_notes/curriculum/610_h3v7n5qf_derivations/scripts/.gitkeep
S11  education/5_genesis_reading_notes/curriculum/610_h3v7n5qf_derivations/videos/
S11  education/5_genesis_reading_notes/curriculum/620_genesis_ongoing_levels/scripts/.gitkeep
S11  education/5_genesis_reading_notes/curriculum/620_genesis_ongoing_levels/videos/
S11  education/5_genesis_reading_notes/curriculum/scripts/
S11  education/5_genesis_reading_notes/curriculum/videos/
S11  education/5_genesis_reading_notes/normal_forms/nf.*.yaml  (4 files)
S11  education/8_witnessed_difference_programme/contracts/
S11  education/8_witnessed_difference_programme/curriculum/700_wdp_overview/videos/.gitkeep
S11  education/8_witnessed_difference_programme/curriculum/710_wdp_finite_obstruction/videos/.gitkeep
S11  education/8_witnessed_difference_programme/curriculum/720_wdp_levels/videos/.gitkeep
S11  education/8_witnessed_difference_programme/curriculum/730_coda_foundations/scripts/.gitkeep
S11  education/8_witnessed_difference_programme/curriculum/730_coda_foundations/videos/
S11  education/8_witnessed_difference_programme/curriculum/740_coda_terminal_factorization/scripts/.gitkeep
S11  education/8_witnessed_difference_programme/curriculum/740_coda_terminal_factorization/videos/
S11  education/8_witnessed_difference_programme/curriculum/750_three_prime_algos_foundations/scripts/.gitkeep
S11  education/8_witnessed_difference_programme/curriculum/750_three_prime_algos_foundations/videos/
S11  education/8_witnessed_difference_programme/curriculum/760_prime_ascent_and_halting_laws/scripts/.gitkeep
S11  education/8_witnessed_difference_programme/curriculum/760_prime_ascent_and_halting_laws/videos/
S11  education/8_witnessed_difference_programme/curriculum/770_ddc_foundations/scripts/.gitkeep
S11  education/8_witnessed_difference_programme/curriculum/770_ddc_foundations/videos/
S11  education/8_witnessed_difference_programme/curriculum/780_ddc_runtime_laws/scripts/.gitkeep
S11  education/8_witnessed_difference_programme/curriculum/780_ddc_runtime_laws/videos/
S11  education/8_witnessed_difference_programme/curriculum/scripts/.gitkeep
S11  education/8_witnessed_difference_programme/curriculum/videos/**  (3 files)
S11  education/8_witnessed_difference_programme/normal_forms/nf.evidence.certificate.yaml
S11  education/8_witnessed_difference_programme/normal_forms/nf.evidence.loss_ledger.yaml
S11  education/8_witnessed_difference_programme/papers/
S11  problem_sets/problems/.gitkeep
S11  problem_sets/results/.gitkeep
S11  problem_sets/results/undergraduate_qm_25/rust_run.log
S11  problem_sets/solutions/.gitkeep
S13  code/rust/quality/l4a_six/activate_*  (4 files)
S13  code/rust/quality/l4a_six/ordered_port/  (3 files)
S13  code/rust/quality/l4a_six/ordered_trial.contract.score.yaml
S13  code/rust/quality/l4a_six/ordered_trial.py
S13  code/rust/quality/l4a_six/scalar_port*  (6 files)
S13  code/rust/quality/l4a_six/scalar_port/  (136 files)
S14  reviews/repository_file_review/retired_born_controls_sources/
S14  reviews/repository_file_review/retired_computation_sources/  (12 files)
S14  reviews/repository_file_review/retired_discrete_dynamics_sources/
S14  reviews/repository_file_review/retired_positive_form_sources/  (2 files)
S14  reviews/repository_file_review/retired_support_contracts/  (5 files)
KEEP atlas/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/source_archive/000_sn/paper_claim_ledger.md
KEEP code/rust/quality/l4a_six/activate_hott_models.contract.score.yaml
KEEP code/rust/quality/l4a_six/activate_hott_models.py
KEEP code/rust/quality/l4a_six/scalar_port_faults.contract.score.yaml
KEEP code/rust/quality/l4a_six/scalar_port_faults.py
KEEP education/5_genesis_reading_notes/normal_forms/nf.epistemic.cnf.yaml
KEEP education/5_genesis_reading_notes/normal_forms/nf.epistemic.freshness.yaml
KEEP education/8_witnessed_difference_programme/curriculum/videos/README.md
KEEP evidence/dossiers/reduction_proof.md
KEEP evidence/dossiers/spectral_closure.md
KEEP evidence/governance/pr215-independent-review/receipt.json
KEEP evidence/quality/code_2026_10_26/gin-singleton-counterexample.log
KEEP evidence/quality/code_2026_10_26/hosted_governance_bootstrap_40361237504.log
KEEP evidence/quality/code_2026_10_26/python-final-docstrings.log
KEEP evidence/quality/code_2026_10_26/rust-fixture-after.log
KEEP evidence/quality/code_2026_10_26/rust-fixture-clippy.log
KEEP evidence/quality/code_2026_10_26/rust-fixture-release.log
KEEP evidence/quality/pr215_l4_repair/pr244_integrated_pipeline.json
KEEP evidence/results/batches/20261019T232430Z_prompts_112_131/tools/witness_cases.json
KEEP evidence/results/batches/20261020T000351Z_prompts_132_151/tools/specs.py
KEEP evidence/results/batches/20261020T000351Z_prompts_132_151/tools/witness_cases.json
KEEP lean4/qm_compose_monoidal_structure.md
KEEP lean4/qm_continuum_non_promotion.md
KEEP lean4/qm_gellmann_decoherence_matrix.md
KEEP lean4/qm_gellmann_matrix_projections.md
KEEP lean4/qm_import_completeness_audit.md
KEEP lean4/qm_import_independence.md
KEEP lean4/qm_lift_classification_boundary_axiom_audit.md
KEEP lean4/qm_schrodinger_discrete_cochain.md
KEEP lean4/qm_stage_import_map_audit.md
KEEP lean4/qm_superposition_cochain.md
KEEP lean4/qm_superposition_h1_rank.md
KEEP lean4/qm_survival_theorem.md
KEEP lean4/qm_u1_torsion_exclusion.md
KEEP lean4/qm_wave6_completion_axiom_audit.md
KEEP lean4/qm_wave7_completion.md
KEEP lean4/qm_wave7_completion_axiom_audit.md
```

## 9. Implementation status

Implemented on the project-thread branch from 07b3454d1 (main after #578, which modified 18 files and
added none), one commit per story, in order. Every count below was measured with the commands of section 3 on this
branch. Tree: 24,350 tracked files and 688.5 MB before S01; 21,988 files and 648.0 MB after S22 (the epic's 21,986
plus the two S01 files; 2,366 files removed, 526 moved, 2 renamed, exactly the appendix).

| Story | State | Commit | What is left |
|---|---|---|---|
| S01 | done | 67fcad678 | - (UNTYPED 1,178, DEAD 26, MISSING 7, FORM 0 at the commit; `--plan` reproduced every appendix count) |
| S02 | done | 3dff38265 | 13 tests of `dag/tests` fail at that commit on main already (listed in the commit); the step is report-only |
| S03 | done | d8d75a3af | - |
| S04 | done | 2ae056c72 | - |
| S05 | done | 9b4b6082e | `governance-check baseline --write` was not used: on this tree it also drops 43 unrelated entries (41 files that now pass and the two whose bytes changed on main, `code/rust/src/fsp/lib.rs` and `lean4/lakefile.lean`) and relabels 527 deficits; the 15 entries of the removed sources were removed by hand with the summary counts. Owner decision: run the full rewrite or keep the hand shrink |
| S06 | done | b14c918ea | the moved guide keeps a link that was already broken (`evidence/contract_score_migration/index.json`) |
| S07 | done | ffb688e51 | - |
| S08 | done | 1441995be | - |
| S09 | done | 946a5de36 | - |
| S10 | done | 5c345411c | only the owning sync (`sync_pregenesis_to_wdp.py`) was applied; the other six syncs of `dag/README.md` are not a fixed point on main (`sync_pfp_results.py` rewrites a node statement, `sync_application_branches.py` moves a node), which rule 3.2 forbids here |
| S11 | done | 2ec9eda85 | the 25 solution files' `problem_file` backlink and `normal_forms/sql/README.md` were edited too (the verifier compares the backlink with the catalog path); the problem-set verifier stops at its Rust step on this machine before and after (MSVC `cc-rs` build), its YAML checks pass |
| S12 | done | aecd62ecf | - |
| S13 | done | 896b45f82 | baseline shrunk by hand (73 entries), as in S05 |
| S14 | done | 0f3d5ea41 | - (three companions rebound with unchanged L4B grades by the helper call; six ledger hashes updated) |
| S15 | not done | - | registering a family needs `[[bin]]`, `[[test]]` or `mod` edits of governed manifests and roots (`Cargo.toml`, `lib.rs`), whose grandfathering then needs an owner-approved re-pin (rule 3.5), and Q11's CI first; nothing was wired or removed |
| S16 | partial | 0a92bf457 | the lakefile `srcDir` repair, its baseline re-pin and companion rebind: 12 receipts under `evidence/lean_receipts` pin `lean4/lakefile.lean` and their migration rule accepts only added `lean_lib` stanzas, so the edit needs fresh replays on a machine with Lean and Mathlib, or the owner's extension of that rule. Also left: the eight independent notes that name the retired campaign queue (any edit raises overclaim rule R8 because their first lines do not carry the standard header), `.gitattributes:151` (a dead `dag/research` attribute) and `education/6_genesis_foundations/this_repo.md:18`, which are outside the files S16 names |
| S17 | done | d3ba0bbb8 | - (`--report naming` lists only `exception` 2 and `imported`) |
| S18 | not done | - | 789 files still hit after S20 (375 in `code/`, 223 in `dag/`, 124 in `papers/`, 25 in `docs/`, 14 in `lean4/`, 9 in `scripts/`, 19 elsewhere); stage A alone is several hundred prose files to reword by hand against a term list the public tree does not hold |
| S19 | not done | - | governed sources need owner approval per batch (rule 5); DAG sources need rule 2, whose sync chain is not a fixed point on main (see S10) |
| S20 | done | with S22 | 13 allow entries per Q2, Q5 and Q14 (companions, manifests, `evidence/`, the review ledger, overclaim and maintenance records, `vendor/`, `atlas/`, the imported education modules, `normal_forms/contracts/`, `lean4/Imported/`, the agent-configuration folder): hits 2,956 to 789 |
| S21 | not done | - | optional; the recommendation needs the 25 generators changed to compare against `MANIFEST.sha256`, a full census run (about 4,041 s) and a CI job |
| S22 | done | with S20 | every `now` and `target` refreshed to the final tree; the dag.yml step is blocking with `--strict` (0 findings); the naming and public-text reports stay non-blocking until S18 and S19 |

Checks at the end (the same commands as before S01): C1 `nodes=989 routes=997 records=1041 failures=0`; C2 `evidence map
current`; C3 the governance crate builds, the replay pins verify (`all_passed: true`), `contract_scores.py check` and
`score_scope_contracts.py check` pass, and `governance-check --root . check` reports the same 7 failures as main
(the #577 and #578 sources and the lakefile binding) - because `governance/baseline.json` changed, the PR's
`--changed-since` step now selects every source and shows those 7; C4 111 tests pass, overclaim HIGH 0 MEDIUM 0 LOW 4,
lint 0, skill audit 0 HIGH 0 MEDIUM 3 LOW (7 LOW before S01); C5 `README facts current`; C6 0 findings; C7 and C8 per
story commit. Governance re-pins: none; the only rebinds are the three S14 companions (unchanged grades). Deposits
(rule 6): both manifest checks pass in 5 of the 13 deposits after the stories that touched them; the other 8 were not
touched and keep their stale entries (atlas.type.yaml, `deposit.manifest_matches`).

### Review fixes to the types (after S22)

Three read-only reviews of the type files against the implemented tree were applied on the same branch (commits
prefixed `Review fixes:`): the dot-folder class became three folder classes; the catch-all collections of the atlas
deposits, the genesis run, the education modules, the teaching pack, vendor/ and normal_forms/ became typed members;
every `holds_now` was set from a command run on this tree; and `scripts/check_repo_types.py` now enforces the rest of
block `meta` (one type file per folder, root-to-class composition, the four catch-all forms, counts against the tree,
`checked_by` paths, invariant ids, `holds_now: true` needs a command, leaf `format` against the file extension, glob
grammar, gitlinks) with tests beside the existing ones. Follow-up work for the owner, recorded here because records are
not edited to make an invariant true (rule 3.8):

- `checks/review_ledger`: 121 checker companions cite 9,194 records by the pre-S14 path `reviews/repository_file_review/`
  (9,126 resolve by basename, 68 do not) and 204 of the 665 ledger rows point at paths that no longer exist; a rename map
  beside the ledger, not a rewrite of hash-pinned histories, is the repair (`review_ledger.cited_bytes`).
- `dag/derivation_dag.json`: 31 record-field paths (lean4, python, rust fields) name no tracked file; the validator does
  not open record fields (`dag.record_paths_exist`).
- `dag/derivations/master_derivation_ledger.md` differs from what `scripts/build_master_derivation_ledger.py` writes
  (1,011 steps recorded, 1,041 generated) and the script has no `--check` (`dag.master_ledger_current`).
- `atlas/PROVENANCE.json`: 425 tracked atlas files unlisted, 1,042 listed paths untracked, 203 listed files with another
  sha256 (`scripts/check_repo_types.py --report provenance`); `education/hamilton_noether_sources/import_manifest.json`
  names 36 files that left the pack and 2 that changed; `normal_forms/contracts/PROVENANCE.json` differs for 2 files.
- Six upper-case file names written in this repository are listed under naming rule `exception` (a foundations note, the
  language SPEC, two verifier logs, two recovery notes); renaming them with their links is a small follow-up.
- The seven `derives_from`-declared byte-twin classes and the 283 undeclared blob groups (791 files) still need per-class
  `allow` lists before `repo.byte_duplicates_declared` can hold.

## Adversarial review

Method: a scratch evaluator written from block `meta` alone and run on HEAD, the S01 commit and the projected
target; a sweep of every kept text file for path tokens (also resolved as relative links) that name a removed or
moved file or folder; reads of the loaders around each large removal; read-only runs of C1, C2, C5, of
`dag/tools/prose_proofs.py`, of `sha256sum -c` in all 13 atlas deposits, and of the public-text rule over all
24,325 files.

### Mistakes found and fixed

1. S09 deleted 21 regression tests of kept code. 'code/tests/test_full_audit_regressions.py' has 19 tests, 13 of
   them on kept packages (`additive_tensor`, `observer_completion`, `state_effect_readout` and others), and
   'code/tests/test_review_gate_regressions.py' has 9, 8 of them on kept scripts (deposit zip, coverage, prices,
   swaps, causal execution, the Lean admission gate, the genesis bridge). Overturn O9 was wrong for these two. Fixed:
   S09 edits them; its removals fall from 888 to 886.
2. S13 deleted `code/rust/quality/l4a_six/scalar_port_faults.py`, whose `block` five kept modules import and whose
   `recipes` `mutations.py`:205 runs against the live `src`. Overturn O3 was wrong for it. Fixed: it stays with its
   companion (153 to 151) and S13 gains an import check that passes at HEAD.
3. S06 deleted files that code and the DAG read without a literal file path: the `jordan_classical_qubit` run (40
   files) that `pfp_review.superseded_by` cites (`dag/derivation_dag.json`:5423); three batch fixtures that two root
   tests import by building the path (`test_born_boundary_exact.py`:7-9, `test_l1_import_exact.py`:12-13); and
   `evidence/reviews/application_branches_validation.json`, linked from the rendered `dag/derivations/README.md`:831.
   `.gitignore`:53-56 says run files are committed only when something cites them, which is the sign to look.
   Fixed: all 44 stay (356 to 312), and S06 runs C5 `--write`.
4. S03 deleted `library.yaml` as unread. A library checker in a private sibling repository registers this repository
   with `catalog: library.yaml`; the root type held a port of it without its catalog header. Fixed: `library.yaml`
   is referenced, not subsumed; the ported `library` block (657 lines) left the root type; S03, S08 and S11
   repoint its 33 stale paths; invariant `repo.library_paths_resolve`; question Q9.
5. S11 deleted twins that their own education module reads: `test_wdp_audit.py`:298-310 loads seven of the
   removed contracts by name, `sn_audit.py`:384 and `wdp_audit.py`:514 load the schema twins (which 60 contracts name
   in `schema_ref`), the grammar checkers and their tests load four conformance and grammar files, and kept READMEs
   link nine more; it also deleted `2_symmetric_group_presentations/lean4/SnSyntax.lean`, a lakefile root that three
   kept modules import, and all six roots of `3_minimal_symbol_systems/lean4/lakefile.lean` while keeping the
   lakefile. The rule "nothing outside education cites it" never looked inside the module. Fixed: S11 keeps 30 twins
   and removes the 14 that nothing reads or links, with the second Lean package whole (79 to 55); it names the
   README links it must edit and `scripts/scan_lean_references.py`:131, which scans the folder name `problem_sets`.
6. S14's rebind cannot run: `score_scope_contracts.py record` raises "not in a governed population" for
   `checks/tests/*.py` (scripts/score_scope_contracts.py:252-256, called at line 678). Fixed: S14 gives the helper
   call that does what `command_record` does, with language Python as reviewed-checkers.yml:56 uses.
7. Rule 6 relied on `verify_deposit.py --integrity-only`, which 8 of the 12 deposit verifiers do not accept, and 10
   of the 13 deposits already fail `sha256sum -c` at 88fa973cc (so_k_invariant_gauge_classification by 39 entries),
   so "regenerate the manifest" would seal unreviewed drift. Fixed: rule 6 checks with `sha256sum -c` before and after
   and lists the stale entries in the PR; invariant `deposit.manifest_matches` says false with the numbers.
8. The meta-schema was not enforceable as written: `**` without a following `/` and `[...]` were undefined but used;
   four class attributes carried placeholder paths ("see PaperDeposit", `education/<n>_<name>` and two more); the
   instance root of a `path_glob` class was undefined; the catch-all rule depended on an undefined "hand-maintained
   class", two genesis_ongoing members used the `format: any` leaf without the flag and AtlasStudy had a `**` member;
   `authored`, `naming` and `companions` held free text (`derived:...`, `exception (see note)`, "review ledger
   (...)"); and the `changes` blocks held prose instead of globs while repeating the appendix. Fixed: block `meta`
   rewritten (glob grammar, class attributes without paths, a structural catch-all rule, error FORM, value grammars,
   naming rule `exception` with listed paths); `changes` blocks removed. The second scratch evaluator finds FORM 0.
9. MISSING at the S01 commit is 7, not 4: three required class attributes name classes that own no file until S11
   and S14. Fixed in the acceptance counts of S01, S06, S11, S14 and S16.
10. The public-text rule did not produce its own number. As written (whole words and pairs) it counts 2,895 files at
    HEAD; the 3,373 came from a different regular expression. The gap is a plural crate name (a private name plus
    "s", in 503 files) and names inside CamelCase identifiers. Fixed: the rule splits CamelCase and tries each word
    without one trailing "s", and states its text-file test; it counts 3,363 files (23 regex-only, 13 rule-only);
    the removals take out 298; S18 to S20 carry the new stage counts (500, 326, 1,045 and 1,194).
11. The archive rule was left open: `symmetric_groups_and_minimal_symbol_systems/source_archive/` survived the epic
    with one DAG-cited file, so `repo.no_archive_folders` and therefore S22 could never pass. Fixed: S10 renames the
    file through its owning fragment `dag/fragments/pregenesis_to_wdp.json`:7727; the old Q9 is gone.
12. Smaller ones, all fixed: the dag type said the validator checks `prose_proofs.md` (it checks only the two views;
    `prose_proofs.py` and `dag/tests/test_prose_proofs.py`:69 check the index, and its flag is `--write-index`); the
    atlas type said `atlas/PROVENANCE.json` lists every file (5,279 entries; 1,251 tracked atlas files unlisted and
    981 listed paths absent); `ProjectionObstructionSeries.series_files` typed four JSON files as Markdown; the CI
    table sent projection-obstruction.yml to S10, while it is path-filtered to the two packages S14 edits; S22 waited
    for S15, which needs a build machine and changes no type; C5 is stale at HEAD and the plan did not say so; the
    docs type cited `docs/_config.yml`:24, a comment line.
13. Found while reconciling with main: S16's lakefile edit would break the replay pins of `lean4/lakefile.lean`
    that 12 receipts hold and governance.yml:70-71 verifies; their migration rule accepts only added whole `lean_lib`
    stanzas. Main's governance job already fails at that step since #577. Fixed: S16 names the pins and the fresh
    replays they need.

### Questions put to the plan, and the answers

- Do the counts hold? On the senior's files my evaluator reproduces UNTYPED 1,185, 21,906 target files and
  646.2 MB, after three interpretation guesses that the new meta text removes. After the fixes: UNTYPED 1,178 at
  HEAD and at S01 (`library.yaml` and six batch fixtures are now typed), 0 in the target; every member count exact;
  FORM 0; the per-story UNTYPED deltas sum to 1,178. At the merged tip: the same 1,178, 21,986 target files, 647.2 MB.
- Is the atlas side canonical (O1 and O2, 613 files)? Yes: the 2026-11-05 content commits 41743c8ec, 6803005f0 and
  fd07f2df2 follow the papers copy of 5209ba624 (2026-10-27); the papers-only files are build by-products and
  dependencies the atlas edition dropped by design.
- Should the 537 census files stay committed (O11)? Yes: 'code/tenth/__main__.py':65-68 compares the committed
  folder in both directions.
- Does any generated page link a removed file? Only the run-contract file, which S16 renames with regeneration.
- Does S08 change `dag/prose_proofs.md`, whose generator scans `papers/**/*.md` (prose_proofs.py:62)? No: no removed
  file holds a proof section.
- Does S04 remove text a DAG node relies on? No: the stems occur only inside non-existent
  `lean4/original_lean_20260809/*.lean` paths in prose fields, and the node cites `lean4/BornRedundancy.lean`.
- The sweep of kept files found 152 live referrers of removed or moved paths; each is now named by its story or is a
  record under rule 8.

### Reconciliation with main (#574 to #577)

Main gained #574 to #577 after this review began; they were merged into this branch (0fbbb35cd) and the evaluator was
re-run at the merged tip. 25 more files are tracked there (10 added by main, the 15 of this folder). The 6 renames lie
inside folders that S09 and S14 remove or move. A new folder, `evidence/chsh_norm_admission/` (6 files), gained the
member `verification_packages`; the counts of PythonTree, DerivationPapers, LeanFolder, EvidenceFolder and
RepositoryTypes changed with main. The DAG lines that S10 and S16 cite moved (18445 to 18449, 32660 to 32723), and
S06 now names both `superseded_by` citations of the kept run. C2 now reports 11 stale files, not 34. The public-text
count is 3,325 (3,363 before the label sweep). S16 gained the replay-pin step (mistake 13). Unchanged at the tip: the
appendix and every `(N files)` count, the per-story deltas, the deposit manifests (10 of 13 fail), the WDP-graph
identity, the provenance figures and the 546 byte twins. A sweep of main's 240 changed files found no new consumer of a
removed or moved path.

### Mutations

- Type files: 140,816 to 108,803 bytes (the root file 51,484 to 26,181); the epic 113,429 to
  90,443 bytes; the appendix 675 to 204 tagged lines (153 removal lines with globs, 37 KEEP lines, 14 moves); every
  `changes` block removed (the appendix is the one change list); class attributes carry no path; members drop the
  default `authored: hand`.

### Disagreements left alone

- The UNSURE verdicts (the 533 unwired Rust files, 98 byte snapshots and others): each needs a build or an owner
  answer, and each is typed either way.
- `lean_namespace_folder` accepts a PascalCase folder anywhere, not only inside Lean trees. It is decidable and no
  target folder abuses it; narrowing it needs a list of Lean source roots.
- The senior's S02 page-diff measurement and its 25-generator census run (4,041 s) were not repeated.
- The senior's sign-off below is kept as written; where it conflicts with this section, this section holds.

## Sign-off

```yaml
signoff:
  role: senior reviewer of the repository-typing review (five slice reviewers merged)
  date: 2026-11-06
  baseline: 88fa973cc
  files_written: "governance/types/*.type.yaml (14) and this epic; nothing else in the repository was changed, moved or deleted; nothing was committed"
  checked:
    - "The five reviewer inventories re-run through the coverage checker: all exit 0, 24,263 files covered; with the 62 dot-folder files typed here every one of the 24,325 tracked files has a verdict."
    - "Every DELETE, MOVE and MERGE row over 20 files or 1 MB (42 rows) against the CI workflows, dag/derivation_dag.json, the manifests, governance/baseline.json and policy.json, generators, imports and kept documents."
    - "A random sample of 40 smaller DELETE and MOVE files (8 per reviewer, seed 20261106) by full-path and file-name search."
    - "A literal-path sweep of all 2,834 removed or moved files against every kept file outside history records: 98 kept referrers, each handled by a story or an overturn."
    - "dag/validate_derivation_dag.py --repo-root . -> nodes=988 routes=996 records=1040 failures=0."
    - "dag/evidence/build_evidence.py --check -> exit 1, 34 stale files; diagnosed as two commits without --write (S02), not line endings; the full diff classified (106 sha256 lines, 15 symbol rows, one record-status line that catches up with the DAG)."
    - "Projection-obstruction copies: blob and last-commit comparison of the 574 papers files with their atlas twins; the five papers-newer files are lockfile bumps whose pins the atlas twins already carry."
    - "lean4/Imported: the sha256 of every tracked .lean file outside lean4/ matched against the 315 manifest original_sha256 values (229 found, 86 absent, 30 modules drifted from repo_sha256)."
    - "dag/wdp_derivation_dag.json: 151 nodes, 148 routes and 173 records equal to the main DAG field for field; no reader."
    - "Readers of rules/rules.yaml and library.yaml: none."
    - "Genesis census: python -B -X utf8 code/<generator>.py --check from the genesis_ongoing folder: all 25 generators (code/generate.py, generate_second to generate_sixteenth, run_seventeenth to run_twentyfifth) report that the committed evidence matches a fresh regeneration; 4,041 s in total, the longest 734 s (eighth); each writes only to a temporary folder."
    - "Public text: a letter-boundary regular expression over every tracked path and text file (binaries skipped): 3,373 files; 301 are removed by this epic; the other 3,072 are staged in S18 to S20 by class."
    - "The type files: a scratch evaluator of the repo-type/1 rules over HEAD and over the projected target tree: target 0 UNTYPED, 0 DEAD, 0 unknown names, every leaf type used, every relation names a class; HEAD 1,185 UNTYPED; every count in the files was written by that evaluator."
    - "The new files: zero case-insensitive hits for the banned names and words; no host-absolute path; scripts/auto/estate_audit.py docs --paths governance/types -> 0 findings; scripts/auto/anti_pattern_lint.py and scripts/overclaim_scan.py --changed-since origin/main --strict -> 0 findings."
    - "git status --porcelain after the checks: only governance/types/ (untracked)."
  conflicts_settled:
    projection_copies: "atlas is canonical; the papers copies go (S08); the 165 differing files are older editions; the 34 papers-only files are by-products or older drafts."
    lean4_imported_vs_atlas: "keep both as a declared derives_from relation checked through the import manifests (Q15); they are not byte duplicates, so nothing is merged on similarity."
    review_homes: "one class per home: CheckerReviewRecord (checks/review_ledger, after S14), NodeReviewResult (evidence/results/<ID>/reviews), PrValidationRecord (evidence/reviews), OverclaimReview (docs/overclaim/reviews)."
    rules_and_library: "both subsumed by the root type and deleted (S03); governance/policy.json is referenced, not restated."
    problem_sets_and_normal_forms: "problem_sets moves into education with its path fixes (S11); normal_forms stays a top-level folder; 39 uncited education twins go, the 5 DAG-cited ones stay (Q8)."
    wdp_graph_and_teaching_pack: "the WDP graph is merged away (S07); the teaching pack moves to education (S11) with its three derivation links."
    evidence_pages: "diagnosed and made a blocking check (S02); the DAG-id page names are not lower-cased (naming rule dag_id)."
    lakefile_srcdir: "repaired in S16 with an owner-approved baseline re-pin and a companion rebind."
    public_text: "counted once, exactly, by a stated rule; the deletions remove 301 files, not most of them; the rest is staged by class in S18 to S20."
    code_unwired_and_quality: "the 533 unwired Rust files stay UNSURE for S15 (needs a compile); 14 of 16 mod.rs roots merge, two stay; the l4a_six snapshot goes with its seven replay tools, and the receipts it served already left the tree."
    stale_paths: "history records keep old strings (rule 8); live documents are fixed in S16; the retired campaign README is not recreated."
    census_tables: "stay committed: the generators' --check compares the committed tables; S21 is the owner-gated way out."
  overturned:
    count: "19 decisions covering 1,238 files"
    items:
      - "O1 583 files: atlas/projection_obstruction twins and atlas-only files (reviewer 1: MERGE, MOVE or UNSURE toward papers/) -> KEEP; atlas is canonical."
      - "O2 30 files: papers-only files in the seven stale copies (reviewer 5: UNSURE) -> DELETE."
      - "O3 14 files: the seven l4a_six replay tools and their companions (reviewer 2: KEEP) -> DELETE with the snapshot they read."
      - "O4 1 file: lean4/majorana_axiom_report.txt (reviewer 3: MOVE) -> MERGE; it is a byte twin of papers/core/majorana/lean4/axiom_report.txt."
      - "O5 2 files: the Majorana mutation harness in lean4/ (reviewer 3: MOVE to code/python) -> KEEP; it reads the module beside it, and code/ would make it a governed source without a score."
      - "O6 4 files: the root deposit verifier (reviewer 3: MOVE to scripts/) -> KEEP; the move edits a baselined governed test (Q6)."
      - "O7 4 files: evidence/quality/code_2026_10_26 records linked from kept documents (reviewer 4: DELETE or UNSURE) -> KEEP."
      - "O8 5 files: DAG-cited education twins (reviewer 5: MERGE) -> KEEP (Q8)."
      - "O9 4 files: WDP deposit tests and scripts that read the deleted quadrant or application (reviewer 1: KEEP) -> DELETE."
      - "O10 2 files: code/rust/src/wdp/mod.rs and its companion (reviewer 2: MERGE) -> UNSURE; 705 lines differ from lib.rs."
      - "O11 537 files: genesis census tables (reviewer 1: REGENERATE and drop from the tree) -> REGENERATE kept committed; the --check needs them."
      - "O12 1 file: rules/rules.yaml (reviewer 3: MOVE to governance/) -> DELETE; subsumed by the types."
      - "O13 4 files: the operations scoring forwarder and its test (reviewer 2: MERGE) -> KEEP; code/python/operations/__init__.py:16 imports it."
      - "O14 1 file: the szollosi receipt under code/rust/src/mub/runs (reviewer 2: MERGE) -> UNSURE with the unwired solver that writes it (S15)."
      - "O15 38 files: Python-side JSON fixtures and SQL schemas twinned with other copies (reviewer 2: MERGE) -> KEEP; the loaders read the Python-side paths."
      - "O16 3 files: intentional twins read by deposit code (reviewer 1: MERGE) -> KEEP."
      - "O17 2 files: code/deposit_paths.py and its companion (reviewer 2: DELETE) -> KEEP; the root verify_deposit.py binds it."
      - "O18 2 files: code/rust/src/mub/mod.rs and its companion (reviewer 2: MERGE) -> KEEP; the QM problem atlas binds it."
      - "O19 1 file: evidence/quality/code_2026_10_26/.gitattributes (reviewer 4: DELETE) -> KEEP; it governs kept files."
    proposals_not_taken:
      - "Lower-casing the 1,023 evidence page names (reviewer 5)."
      - "Moving rules/rules.yaml to governance/ (reviewer 3); subsumed instead."
      - "Recreating the retired campaign README (a reviewer 4 question); its references are reworded instead."
  could_not_check:
    - "No cargo build or test, no lake build and no governance-check run (the review brief forbids builds); C3 and every Lean or Rust acceptance must be run by the implementer."
    - "No deposit test suite, verify_deposit.py or problem-set verifier was run."
    - "GitHub CI itself."
    - "The checker of S01 does not exist yet; the counts come from a scratch evaluator of the same rules, and the hash-based public-text rule may differ from the regular-expression count by word-form variants."
    - "The compile state of the 533 unwired Rust files."
    - "References built at run time that neither a literal-path nor a file-name search finds, outside the loaders named in the stories; each story's package tests before and after are the guard."
    - "The 1,186 UNSURE files are not resolved; each type names the question that decides them."
  verdict: "ready for adversarial review"
```

```yaml
signoff_adversarial:
  role: adversarial reviewer of the repository-typing plan (second senior review)
  date: 2026-11-06
  baseline: "88fa973cc; reconciled at 341d2e3dc plus this branch"
  files_written: "governance/types/*.type.yaml (14) and this epic, rewritten in place; nothing else in the repository was changed; nothing was staged or committed; the scratch evaluators live outside the repository"
  checked:
    - "A scratch evaluator written from block meta alone, run on HEAD, on the S01 commit (HEAD plus the 17 added files) and on the tree the appendix projects; before the fixes it reproduced the senior's UNTYPED 1,185, 21,906 files and 646.2 MB, and showed MISSING 7 at S01, not 4."
    - "A second evaluator on the rewritten files: HEAD UNTYPED 1,178, DEAD 34, MISSING 12; S01 UNTYPED 1,178, DEAD 26, MISSING 7; target 0, 0, 0; FORM 0; every member and class count equal to the tree; per-story deltas as the stories state."
    - "Hidden consumers of the large removals: Python imports and path building in the WDP deposit, l4a_six, the root tests and dag/tools; the DAG's superseded_by fields; the education lakefiles and the module code and tests that build paths to twins; the sibling catalog that reads library.yaml; scripts/build_readme_facts.py and dag/tools/prose_proofs.py globs."
    - "A sweep of every kept text file for path tokens naming a removed or moved path: 5,715 hits, 152 live referrers after records and co-moving files; each is named by its story or is a rule-8 record."
    - "C1 (nodes=988 routes=996 records=1040 failures=0), C2 (exit 1, 34 stale; diagnosis confirmed), C5 (stale), prose_proofs.py index (current; unaffected by S08), sha256sum -c in all 13 atlas deposits (10 fail at HEAD)."
    - "The public-text rule implemented as stated, over all 24,325 files, before and after tightening it; the 36 term hashes; the files of this folder hit nothing."
    - "Overturns over 20 files: O1 and O2 (atlas canonical) and O11 (census tables committed) hold; O3 and O9 were wrong in part and are reversed for four files; O15 (38 fixtures and schemas) checked by sample (code/python/src/qm/api.py:64)."
    - "git status --porcelain after every check: only governance/types/."
  changed: "the twelve fixes of the Adversarial review section; removals 2,436 to 2,366; target 21,906 to 21,976 files; library.yaml kept and referenced; source_archive/ renamed away in S10; meta grammar, MISSING, catch-all and public-text rule made decidable; changes blocks and the library block removed"
  could_not_check:
    - "No cargo, lake or governance-check run (forbidden here): C3, S05's cargo check, S15 and S16's lake build are for the implementer."
    - "No deposit pytest suite and no problem-set verifier run; S09 and S11 state them as before-and-after checks."
    - "GitHub CI itself, and whether reviewers accept the S14 rebind of three reviewed tests with unchanged grades (Q4)."
    - "The 25 census generators were not re-run; their match is the senior's measurement."
    - "References built at run time that neither a path token nor a module import shows, outside the loaders named in the stories; the package tests before and after each story are the guard."
  reconciled: "at the merged tip: HEAD UNTYPED 1,178, DEAD 29, MISSING 9; S01 1,178, 26, 7; target 0, 0, 0; FORM 0; 24,350 files and 688.4 MB to 21,986 files and 647.2 MB; C1 nodes=989 routes=997 records=1041 failures=0; C2 11 stale; public text 3,325 files; governance CI fails at the replay-pin step exactly as on main (run 42294333196)"
  verdict: "ready to commit"
```
