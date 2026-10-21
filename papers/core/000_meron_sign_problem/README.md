# A Lexically Filtered Meron-Cluster Benchmark

Jeremy H. Carroll. Version 0.1.0, 2026-10-02. Preprint, author-review revision.

Full title: "A Lexically Filtered Meron-Cluster Benchmark: Exact Ground Truth,
Mechanized Cancellation Lemmas, and a Pilot That Exposes Answer Leakage".

## What this package is

- `paper.md` (with `paper.tex` and `paper.pdf`): the manuscript.
- `paper_claim_ledger.md`: each claim, its status, and the test or Lean theorem
  behind it. `paper_change_log.md`: what changed and what was withdrawn.
- `code/`: an exact oracle for one meron-cluster fixture (256 breakup graphs,
  1,296 configurations, $Z = 912$), a substring filter, five prompt builders, a
  scorer, and the pilot harness.
- `code/results/`: the retained record of the pilot run, including one output
  from an anonymous model. These files are kept as recorded.
- `code/tests/`: tests for the oracle, the harness, and every statement the
  paper makes about the retained run. They make no network calls.
- `lean4/`: Lean 4 proofs of the per-orbit cancellation lemmas.

The pilot's passing runs received the answer in their prompts, so the package
supports no claim that a model discovered the cancellation mechanism. See
Sections 5 and 6 of the paper.

## How to check it

Run from this directory with Python 3.12, one test file per command:

```text
py -3.12 -m pytest code/tests/test_meron_cluster_solution.py -q
py -3.12 -m pytest code/tests/test_pilot_evidence.py -q
py -3.12 -m pytest code/tests/test_space_bunny.py -q
py -3.12 -m ruff check code
```

The harness can be exercised without network access or spending:

```text
py -3.12 code/run_blind_benchmark.py --dry-run --output-dir <new-directory>
```

Choose an output directory outside this package. A live run needs an explicit
decision to spend money, the `bench` extras (`requests`, `python-dotenv`), and
an `OPENROUTER_API_KEY` in the environment; it is not part of these checks.

Build the Lean proofs and replay the axiom census:

```text
cd lean4
lake build
lake env lean Census.lean
```

Verify the file manifest, the two-way census and the release archive:

```text
py -3.12 verify_deposit.py
py -3.12 tools/rebuild_release.py --check
```

Rebuild the TeX and PDF from `paper.md` with `py -3.12 tools/compile_paper.py`.

## Toolchain

Python 3.12.10, pytest 8.3.5, ruff 0.14.13 (settings pinned in
`pyproject.toml`), Lean 4.35.0 with Lake 5.0.0 (pinned in
`lean4/lean-toolchain`), Pandoc 3.7.0.2, and XeLaTeX from MiKTeX 25.12.

## Verification receipt

The dated review receipt for this revision is kept in the source repository at
`_ic/nara/historical/omega_paper_reviews/pfp_loop_011_agent/meron_sign_problem/run_all_receipt.json`.
It lists each command, tool version, exit status and tested scope. The files in
`code/results/` are the historical record of the pilot run, not current
execution evidence.

## Licenses

Text: Creative Commons Attribution 4.0 International (`LICENSE`). Code:
PolyForm Noncommercial 1.0.0 (`LICENSE-CODE`).

## Initial Zenodo preprint release candidate

Version 0.1.0, 2026-10-01, designates the initial v0.1 preprint release.
Earlier internal revision 0.4.0 and its corrections are preserved in the
change log and historical evidence. Current readiness depends on the dated
verification report; this designation alone does not establish readiness.
No external publication or DOI is claimed.

The current package-local execution record is
`docs/release_validation_2026_10_02.json`. It records scoped tests and replay;
the prior `docs/release_validation_2026_10_01.json` and other historical
review receipts keep their original dates and scope.

## Separate finite witness companion

The [finite witness protocol](docs/witness_benchmark.md) uses four selected
orbits at q = 5/2, complete raw inputs and strict pair-witness checks.
It preserves the historical prompts and retained pilot without rewriting
their results. Run its zero-provider host control with:

```text
py -3.12 code/run_witness_benchmark.py --output-dir <new-directory>
py -3.12 -m pytest code/tests/test_witness_benchmark.py -q
```

Live mode requires explicit named models, a spend ceiling, a deadline and
configured credentials. A host control is not model evidence. Current local
candidate rebuilding is dated 2026-10-02; historical 2026-10-01 receipts retain
their dates. No external publication or DOI is claimed.
