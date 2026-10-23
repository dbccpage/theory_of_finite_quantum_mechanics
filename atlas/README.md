# atlas

AuthorityEffect: None.

## What this is

Seven paper folders copied byte for byte from a private research repository (`the_symbol_game`, folder `omega_engine_atlas/coda_atlas/F004_papers/`). They keep their original relative paths under `atlas/F004_papers/`:

- `001_finite_obstruction_calculus/000_genesis_19l57g1`
- `001_finite_obstruction_calculus/000_pre_genesis_to_mssn`
- `001_finite_obstruction_calculus/000_witnessed_difference_programme`
- `001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf`
- `001_finite_obstruction_calculus/001_local_green_global_red_foundational_series`
- `001_finite_obstruction_calculus/001_sn_mssn`
- `002_projection_obstruction`

Each folder holds a paper (Markdown, TeX, PDF), its Lean 4 sources, and the Python, Rust, JSON and CSV files the paper cites.

## What status these files have

They are source texts. Whatever a file in `atlas/` says about being proved, verified or checked is the source's own wording. It is not a status in this repository, and it changes no node in `dag/derivation_dag.json`. The statuses in the DAG govern; see [`docs/evidence/README.md`](../docs/evidence/README.md) for how each status is backed.

Nothing here is scanned or scored by this repository's checks: the contract/score checker, the overclaim scanner, the evidence builder and the README facts inventory read explicit paths (`code/`, `lean4/`, `papers/`, `dag/`, `docs/`), and `scripts/build_readme_facts.py` skips `atlas/` so archive files do not inflate its counts. The Lean files were not built here. Nothing in the DAG was re-pointed at these files.

## Bytes and provenance

`atlas/**` is marked `-text -whitespace` in `.gitattributes`, so line endings and trailing whitespace stay as copied. [`PROVENANCE.json`](PROVENANCE.json) records the source commit, the source path, the SHA-256 and size of every file, and every exclusion rule with its count.

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
