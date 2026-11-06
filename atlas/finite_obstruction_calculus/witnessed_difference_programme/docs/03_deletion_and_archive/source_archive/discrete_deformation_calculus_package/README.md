# Discrete Deformation Calculus — v1.0.3

**Author:** Jeremy H. Carroll · **Date:** 2026-10-03 · **DOI:** pending

DDC records how a finite computation handles a declared obstruction using
eight letters: exact repair E, residual projection R, context exposure C,
integration I, licensed lift Λ, descent D, typed refusal M and terminalization T.
The companion computes exact rational examples and formalizes abstract tape
laws in core Lean. Its control states are finite; its data are unbounded.

## Start here

Prerequisites: rational arithmetic, directed graphs and elementary linear algebra.
After the companion exercises you should be able to compute both diagnostics,
identify a missing step hypothesis, and distinguish a policy check from a
verified cochain operation.

- [Quick start](docs/quick_start.md)
- [Enter the calculus](jupyter_notebooks/01_enter_the_calculus.ipynb)
- [Try to falsify the laws](jupyter_notebooks/02_falsify_the_laws.ipynb)
- [Monograph](discrete_deformation_calculus.pdf) and [source](discrete_deformation_calculus.md)
- [Change log](discrete_deformation_calculus_change_log.md) and [references](docs/references.md)

## Verify the release

Unpack `discrete_deformation_calculus_2026-10-03.zip`, enter the extracted
directory, and create a Python environment (Python 3.10 or newer):

```bash
python -m pip install -e '.[dev,notebooks]'
python verify_deposit.py --static
python verify_deposit.py
python verify_deposit.py --lean
python verify_deposit.py --full
```

The default verifier runs each named test file in a separate subprocess,
with a 60-second limit per file, then checks at least 95% line and branch
coverage for `code/ddc`. Tests exercise release tooling separately; external
tool orchestration is verified by actual Lean, notebook and PDF commands,
and is excluded from the runtime coverage denominator. The static check
verifies the complete payload, metadata, links and any current release ZIP.
An extracted package needs no copy of its outer ZIP.

`--lean` needs elan and the pinned Lean v4.34.0. `--full` also needs Pandoc
and pdfLaTeX. It replays each notebook in a fresh kernel using the verifier's
Python interpreter, compares deterministic outputs, checks regenerated TeX
against the deposited source using normalized semantic comparison (built with
recorded Pandoc 3.7.0.2; compatible with Pandoc >= 3.1), rebuilds the PDF and
compares its extracted text, and runs bounded mutation tests. PDF bytes and
compressed ZIP streams can vary across toolchain versions; payload member
bytes, successful compilation and inspected layout are the release contract.

### Recorded build and verification toolchain

- **Python**: requires >= 3.10; this review used 3.12.14
- **Pandoc**: 3.7.0.2 recorded; compatible with Pandoc >= 3.1 via semantic TeX normalizer
- **pdfLaTeX**: pdfTeX 3.141592653-2.6-1.40.25 / MiKTeX-pdfTeX 4.23
- **Ruff**: 0.16.10 (configured via `pyproject.toml`)
- **Mypy**: 1.19.1
- **Lean 4**: v4.34.0 pinned; fresh compiler pass and axiom census verified

The review dated 2026-10-03 confirms full verification across local checks and
release gates. Both companion notebooks execute cleanly under fresh `nbclient`
kernel replays with matching deterministic outputs and stable cell IDs. The
61-theorem Lean 4 formalization compiles cleanly under pinned Lean v4.34.0 with
axiom dependencies strictly bounded to `{Quot.sound, propext}`. All gates in
`--full` pass cleanly prior to release freeze.

For one focused check:

```bash
python -m pytest -q code/tests/test_review_regressions.py
python -m ruff check code scripts verify_deposit.py
python -m mypy code/ddc scripts verify_deposit.py
```

After source edits: replay notebooks with `--write`, build
and inspect the PDF, regenerate manifests and ZIP, then verify the extraction.
Use the scripts in `scripts/` in that order. Both checksum manifests exclude
the outer ZIP and include every payload file; SHA256SUMS also pins MANIFEST.sha256.

### Zenodo deposit and DOI reservation procedure

1. **Reserve DOI before final build**: Create the draft record on Zenodo and click "Reserve DOI" (e.g. `10.5281/zenodo.XXXXXXX`). Insert this DOI into `zenodo_metadata.json`, `CITATION.cff`, `README.md`, `discrete_deformation_calculus.md`, `scripts/preamble.tex`, and `docs/descriptions.md`.
2. **Rebuild release artifacts**: Run `python scripts/build_paper_artifacts.py` and `python scripts/regen_sha256sums.py`, then run `python verify_deposit.py --full`.
3. **Zenodo deposit settings**: Upload only the canonical PDF (`discrete_deformation_calculus.pdf`) and ZIP (`discrete_deformation_calculus_2026-10-03.zip`). Classify as **Publication → Preprint**. Enter both licenses under Rights/Licenses: **CC BY 4.0** for text/documentation and **PolyForm Noncommercial 1.0.0** for code/Lean/tooling. Set the PDF as the default file preview.

## Evidence boundaries

- `State` and `Witness` are inputs to an abstract policy model. Witness flags
  and detector adequacy are assumptions, not authenticated evidence.
- `measure` computes the diagnostics. `run_tape(..., carriers=...)` recomputes
  them and checks R's quotient preservation; carrier topology and weights are
  bound into the tape genesis digest.
- Internal hash consistency cannot detect a fully rehashed replacement or a
  truncated history. Keep `tape.checkpoint()` independently and supply it to
  `verify_integrity(checkpoint)` to detect such changes.
- The 61 Lean theorems concern their stated abstract model. They do not
  mechanize the rational optimization solver, authenticate licences, or prove
  conformance with a deployed Rust runtime. The historical comparison model
  is defined by the deposited source and identified in manuscript §7.
- A lawful CREDIT tape satisfies all six step laws; an exact start and booked
  descent are necessary conditions. The continuation predicate is a separate
  optional terminal-policy guard, explicitly supplied as `continuation_facts`.
- A forest representative's recorded residual norm need not equal the
  minimized quotient distance. Use the checked primal/dual certificate for
  $\Phi_1$; see the study guide's exact K4 example.
- `FiniteLambdaLedger` checks exact row storage, adjacency and declared
  Boolean flags. It does not execute external Rust certificate validators.

## Licence and citation

Text, figures and documentation: CC BY 4.0 ([LICENSE](LICENSE)). Code, Lean and
tooling: PolyForm Noncommercial 1.0.0 ([LICENSE-CODE](LICENSE-CODE)), with the
Required Notice “Copyright 2026 Jeremy H. Carroll”. See [CITATION.cff](CITATION.cff).
