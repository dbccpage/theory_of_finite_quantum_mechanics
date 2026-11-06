# atlas

AuthorityEffect: None.

## What this is

The original import copied seven paper folders from a private research repository. Its manifest records 5,613 files, including 323 files with recorded edits on 2026-10-26, when links into that repository were removed and paths were updated to the renamed folders (six of them were also changed by the certifi bump in #450). Those files are marked `edited_after_copy` in `PROVENANCE.json`, which also keeps their original sha256. On 2026-10-26 the folders were renamed to descriptive names under `atlas/` (the old-to-new map is `destination_renames` in `PROVENANCE.json`):

- `finite_obstruction_calculus/genesis`
- `finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems`
- `finite_obstruction_calculus/witnessed_difference_programme`
- `finite_obstruction_calculus/genesis_ongoing`
- `finite_obstruction_calculus/local_green_global_red` (removed 2026-11-06; the series now lives in [local_green_global_red_lggr](https://github.com/dbccpage/local_green_global_red_lggr))
- `finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems`
- `projection_obstruction`

Each remaining folder holds a paper (Markdown, TeX, PDF), its Lean 4 sources, and the Python, Rust, JSON and CSV files the paper cites.

## QM and computation consolidation, 2026-11-05

The former `foundations/` and `core/` contents now live under the corresponding
numbered stages in [`dag/derivations`](../dag/derivations/). Start with the
[combined reading path](../dag/derivations/FIRST_MARK_TO_QUANTUM_GRAVITY.md)
and [file crosswalk](../dag/derivations/SOURCE_CROSSWALK.md).
The computation and complexity sources share
[`computation_complexity_pvnp/`](computation_complexity_pvnp/README.md).
The import counts and prior byte audit below describe their historical
snapshots, before this further consolidation; the new manifest records this move.

## What status these files have

They are source texts. Whatever a file in `atlas/` says about being proved, verified or checked is the source's own wording. It is not a status in this repository, and it changes no node in `dag/derivation_dag.json`. The statuses in the DAG govern; see [`docs/evidence/README.md`](../docs/evidence/README.md) for how each status is backed.

The original import was a source-custody operation. The governed code-scoring policy names its own source populations, and `scripts/build_readme_facts.py` treats `atlas/` as an archive. The current byte audit is linked below. A build or theorem claim requires the corresponding module, toolchain and verification receipt. DAG citations of copied upstream files use their current atlas paths.

## Bytes and provenance

`atlas/**` is marked `-text -whitespace` in `.gitattributes`, so line endings and trailing whitespace stay as copied. [`PROVENANCE.json`](PROVENANCE.json) records the source commit, the source path, the current path, the SHA-256 and size of every file, and every exclusion rule with its count.

## What was left out, and why

Left out of the copy (counts and sizes are in `PROVENANCE.json`):

- version-control and dependency trees: `.git` (including a 431 MB pack temp file, over GitHub's 100 MB limit), `.lake`, `.venv`, `site-packages`, the Lean build tree `lean4/b`;
- build output and caches: `build`, `dist`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.hypothesis`;
- binaries: `*.pyc`, `*.pyd`, `*.dll`, `*.pdb`, `*.exe`, `*.olean`, `*.ilean`, `*.trace`, `*.so`, `*.lib`;
- `*.zip` snapshots of the same folders (redundant, opaque);
- nested `.gitignore` and `.gitattributes` files, a `.coverage` database, and a folder-local `.claude` settings file;
- nine files that were never tracked in the source repository (egg-info, LaTeX aux/log/toc, a scratch file);
- one full copy of a published third-party paper (Witten, arXiv:1001.2933) from a `references/` folder.

No file over 25 MB is kept, and no file matched a secret pattern. Absolute local paths from the original machine remain in some logs and receipts; they were left as written.

Because files were removed, the `MANIFEST.sha256` and `SHA256SUMS` files inside the copied folders may list files that are not here.

The papers directory contents were moved directly under `atlas/` on 2026-11-05. The provenance manifest records the current locations and retains the historical rename map.

## Current import audit

The November 5 byte audit
compares every recorded import entry with the current tree. It finds 5,558
matching entries, 53 with different bytes or sizes, and 2 missing generated
auxiliary/log files. The manifest retains the recorded hashes, and the audit
lists each discrepancy with its observed hash and size.

The current atlas also contains 1,548 files outside that original import
manifest, mainly under core and foundations. Their origin needs to be read from
their own source records. The manifest's original import totals and exclusion
counts describe that import operation.

For historical source citations beginning with `atlas/papers/`, the current
local prefix is `atlas/`. Imported snapshots and their recorded byte hashes
preserve the original citation text. Mutable education and derivation links
have a separate [relocation receipt](../reviews/repository_file_review/2026-11-05-atlas-reference-cleanup.json).

The [publication relocation audit](../reviews/repository_file_review/2026-11-05-publication-atlas.json) checks this PR tree. Earlier November 5 cleanup receipts record observations in the maintainer's older source checkout; their mismatches and missing files do not describe this publication checkout. The later `everett_mw` notes are outside the original 5,613-file import manifest.

The publication audit matches 5,606 of the original 5,613 import records. Seven requirements/lock files already differed from those recorded import bytes on the PR base; the move preserves those files and the original manifest digests. All 5,613 manifest destinations are present.

## Quantum foundations backup, 2026-11-06

[`quantum_foundations/`](quantum_foundations/README.md) is the author's local
quantum foundations folder (41 manuscripts `qm_002`..`qm_212`, its derivation
DAG snapshot, code, evidence receipts and support notes), copied as a research
backup. Filenames were lowercased and private names were replaced; nothing else
was edited, so recorded hashes inside the evidence manifests describe the
original bytes. [`derivation_map.md`](quantum_foundations/derivation_map.md)
lists the `dag/derivations` stage each manuscript belongs to; merging them
into those derivations is later work.
