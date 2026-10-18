# Verification record — research extension 2.4.0

Date: 2026-09-22. AuthorityEffect: None.

## Git custody and scope

Before the requested Git delivery, the CODA repository HEAD was: `4435cbc0adbc157e45a848521ed15cfcf20f7097`. This package was clean at the start; the research extension was verified as local working-tree changes. The surrounding migration was preserved. Work was confined to this paper package; the research phase performed no commit, push, publication or sealed-source rebuild.

Frozen external citation: 19L57G1 `sealed-derivation-v1`, peeled commit `3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`. The post-seal source investigation was read-only at `30805c5c6598310a4b6cef76e800a9015c9ef56a`. Its separate status and exact source anchors are in [hamiltonian_origin.md](docs/hamiltonian_origin.md).

## Workflow

Three parallel agents owned the normal-form audit, SQL model construction, and pinned source investigation. The source investigator then repaired the legacy exact Hamiltonian/Gin path and independently challenged the new SQL certificates. A separate review checked the new mathematical sections. Integration corrected claims and metadata, added the general Lean meron identity, and ran the package checks.

The independent review exposed invalid orientation domains, missing whole graphs, coherent altered weights/signs, stale auxiliary-field relations, and NULL/noninteger SQLite keys. The corrected SQL admission checks reject all of these. The exact L1 solver also corrected a legacy fixture from the iterative value 2.6 to 5/2, with matching primal and dual witnesses. These are scoped audits, not a comprehensive review of every historical physics fixture.

## Research-phase checks

- `python verify_deposit.py`: **PASS**, including **407 tests passed in 23.31 seconds**, eight workers with `--dist=loadfile`, and `lake build` on the declared Lean roots.
- `MeronCharacter.lean` and `NormalFormLaws.lean` were also replayed individually. Their 13 printed declarations use at most `{propext, Quot.sound}`, with no `sorryAx`. The former proves the general finite flip-list sum; the latter mechanizes specific integral/triangle normal forms, not the entire Python normalizers.
- Exact solver governance arithmetic script: **PASS**.
- Model driver replay: **byte-identical** to `code/sign_sql/exact_models_receipt.json`, SHA256 `5646046df2d8ac71c05b8a08e9a623b192d52b3e8b79911aac96abd00d892236`.
- Manifest probes: valid manifest accepted; omitted source, duplicate entry, path escape and changed content rejected.
- `git diff --check` for this package: **PASS**.

The model receipt records model parameters, coverage, positive normalization factors, exact large rational values and source hashes. Its selected negative fields are existence witnesses; their singleton sign is not a full-ensemble average sign. The checksums cover package source, documentation and receipts; generated `.lake`, Python and test caches are excluded. This record was added after the full run, followed by regeneration and verification of the manifest and selected metadata checks; executable sources were unchanged.

## PR preparation

The user subsequently requested commit, push and a pull request. The delivery checkout is isolated on `codex/po023-exact-meron-hubbard`, based on `origin/main` at the same `4435cbc0adbc157e45a848521ed15cfcf20f7097` revision. It contains only the 69 named package files. Markdown lint corrections preserve the mathematics. Git stores LF line endings, so the model driver now writes UTF-8 bytes explicitly; the receipt and manifest were regenerated for those stored bytes. Every model result is unchanged from the research-phase receipt. The resulting model receipt SHA256 is `af89f5b0e537b1507e5d7c2511f4ab1c4374221f1fd3b0a0fce76202f7fd20e5`. The pull request records validation against its exact commit.

## Replay environment

The run used Python 3.12.14, pytest 9.1.1 with pytest-xdist, numpy 2.5.3, scipy 1.18.1 and PyYAML. Tests used writable external temporary directories. The exact SQL model driver uses only the Python standard library and SQLite. Lean was `leanprover/lean4:v4.34.0` from the installed local toolchain.

Standard replay commands are in [README.md](README.md). On this Windows host, the Python executable used was `C:/Users/a343o/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`; cached test dependencies were selected through the temporary `po023-pythonpath-20260922.txt` file, not added to the repository. The detailed command output remains in the host temporary file `po023-final-verification-20260922.log`.

The package check establishes its recorded computational results. It does not establish an efficient generic Hubbard/FSP algorithm, a thermodynamic limit, a physical derivation from the sealed inscription, or publication approval.
