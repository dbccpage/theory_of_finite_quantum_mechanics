# Validation of the maintained CODA package

The current source of claim status is `../coda_claim_ledger.md`; the generated
index and Lean map derive from it. There are 26 current claim IDs and 48
historical dispositions. Twenty local Lean declarations cover only the mapped
logical and algebraic statements.

## Source custody

`../source_manifest.json` binds seventeen local historical files by size,
SHA-256 and immutable Git blob. Fourteen are diagrams; three are original
discipline source transcripts under `source_archive/`. The active Python and
Lean modules are derivatives. Twenty-two other tracked inputs have external
commit-pinned retrieval links. Six previously reported ignored logs and the
scratch build sources are unavailable. Current release hashes are independent
of those historical source hashes.

## Commands

- `python code/build_claim_index.py`: regenerate the claim index and supplemental map.
- `python code/verify_package.py`: verify historical bytes, current claim/index
  agreement, theorem names, local links, exact examples and notebook structure.
- `python -m pytest code/tests/test_coda_core.py`: one targeted runtime test file;
  select other named files sequentially for their own contracts.
- `python -m ruff check code` and `python -m mypy code`: code-quality checks.
- `lake build` and `lake env lean AxiomAudit.lean` in `lean4/`: current formal slice.
- `python code/replay_notebook.py`: subprocess notebook replay.
- `python scripts/regen_sha256sums.py --check`: verify final flat manifests.
- `python verify_deposit.py`: fail-closed path, symlink, checksum and inventory check.

A successful historical log is not evidence for an unexecuted current command.
The publication PDF, manifests and archive are generated only after the source
and computational results are fixed. PDF byte reproducibility is not claimed.
