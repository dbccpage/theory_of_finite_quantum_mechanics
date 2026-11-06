# Consolidation validation — 2026-11-05

AuthorityEffect: None. Local editorial, structural and custody validation.

## Completed scope

- 1,255 versioned original files have recorded source hashes and surviving destinations.
  1,157 retain their original bytes. The remaining 98 have separately recorded
  edited-copy hashes for navigation, manuscript corrections or relocated tools.
- `atlas/foundations`, `atlas/core`, `atlas/computation`, `atlas/complexity`, and
  `education/l1_to_many_worlds` are absent. The computation sources share
  `atlas/computation_complexity_pvnp`; the other material is under numbered
  `dag/derivations` stages.
- The shorter reading path combines the repeated exposition in ten overview
  documents. Detailed sources, exports, renderers and reviews remain available.
  All local links in those ten documents resolve.
- The DAG has 959 nodes, 967 routes and 1,011 records. The 21 additions comprise
  ten conditional routes or proof sketches, two definitions, three imports and
  six open obligations. No pre-existing node statement or status changed.
- Generated graph views, application/unified indexes, the live master ledger,
  prose-proof index, README facts and evidence pages have been refreshed. The
  pregenesis fragment now cites 399 relocated `atlas/finite_obstruction_calculus`
  paths and its generated block has a stable position ahead of the new
  source-consolidation block.

## Checks performed

In the isolated PR worktree, 85 focused tests passed and one was skipped
across DAG validation, fragment synchronization, source consolidation,
prose-proof indexing, evidence generation and QM atlas bindings. The
application-fragment test initially caught 13 missing mirrored records;
those records were restored and all eight application tests passed on
rerun. A writable task-local temporary directory was used for pytest.

Additional checks passed:

- `scripts/consolidate_derivation_sources.py`: all 1,255 destination hashes and
  all listed retired directories checked, zero custody failures.
- `dag/validate_derivation_dag.py --repo-root .`: full file-and-symbol
  validation passes with 959 nodes, 967 routes, 1,011 records and zero failures.
- All eight DAG sync/view generators, the evidence map and README facts pass
  their `--check` modes after regeneration.
- `scripts/verify_qm_atlas_loc.py`: all 65 questions pass, with 403 links,
  197 in-window symbols and Rust/Python parity.
- The relocated bicategory test passes 10 focused cases in normal and optimized Python. A new source-bound L4C reassessment retains prior history and cites `dag/research/bicategory_relocation_recheck_20261105.json`; this is scoped to the changed origin path.
- The consolidated complexity checker passes all six finite check groups.
- The core manuscript cites 187 distinct DAG-style identifiers; all resolve.
- The prose citation scanner finds valid linked sections for 211 of the 220
  Lean-labeled nodes. This is lexical citation coverage, not Lean elaboration.
- All nine new proof sketches have explicit hypotheses and an argument in their
  TFQ paper and combined chapter. Their status is CONDITIONAL pending
  independent replay or Lean formalization; no Lean proof status was added.

## Reference repairs and retained limits

The previous 186 reference failures are resolved. The 174 Lean file references
now use the files' current locations. Three references to an absent historical
authority rubric are marked `external:unavailable:` with their original path
retained, so they supply no local evidence. Nine U(1) declaration references
were removed after confirming that the named declarations do not occur in the
cited Lean files; `FQ-GAP-U1-CIRCLE` remains conditional. No proof status was
raised. The refreshed evidence map retains 239 flags; generating pages does not
discharge them.
The operad-pinned TFQ papers retain historical citation labels; the
[crosswalk](SOURCE_CROSSWALK.md) maps the old Lean and atlas path prefixes to
their current local locations. Two unpinned live source documents now use the
relocated atlas paths, with edited-copy hashes recorded in the source manifest.

No full Lean build, Cargo build, whole-repository test suite, physical-model
verification or hosted CI run was performed. Historical deposits, hash-bound
receipts and verbatim reviews retain their internal source-era references.
The [crosswalk](SOURCE_CROSSWALK.md) resolves relocated source locations;
historical PDF/TeX exports are not regenerated versions of the new chapters.

The publication candidate was assembled in an isolated worktree from current
`main`. Versioned `papers/` sources were moved to the stage-aligned destinations;
217 local build/cache files from the intermediate workspace were excluded.
Existing mathematical statements and statuses were preserved.

See [the reading path](FIRST_MARK_TO_QUANTUM_GRAVITY.md),
[the source manifest](source_consolidation_manifest.json), and
[the new route fragment](../fragments/computation_information_route.json).
