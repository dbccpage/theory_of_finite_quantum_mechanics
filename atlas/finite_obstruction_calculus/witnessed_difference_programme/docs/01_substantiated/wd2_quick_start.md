# Reading and rebuilding

Version 1.1.0 is an author-review preprint dated 2026-10-08.
Theorem WD2-T1 is elaborated in Lean 4. Lemma WD2-L1 and records
WD2-T2 through WD2-T6 are finite-instance checks or prose arguments.

Read the manuscript and its worked examples directly. The notebook
`jupyter_notebooks/001_reviewer_wd2_finite_distinction_carriers_and_history_escape.ipynb`
has only Markdown cells. The optional launchers use an already installed
Jupyter Notebook; they do not install packages or run a mathematical kernel.

## Read-only integrity checks

From the extracted package root, with Python 3.12:

```bash
python verify_deposit.py
python scripts/regen_sha256sums.py --check
python tools/rebuild_release.py --check
```

For the last command, keep the dated ZIP beside the extracted files.
The first two commands need only the extracted contents. On Windows,
replace `python` by `py -3.12`. No repository imports are needed.

## PDF and archive rebuild

Install Pandoc and XeLaTeX. From the package root, generate TeX with the
reader extensions used for the manuscript:

```bash
pandoc --from markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_tex --to latex --standalone -V geometry:margin=1in -V fontsize=11pt -V colorlinks=true -o wd2_finite_distinction_carriers_and_history_escape.tex wd2_finite_distinction_carriers_and_history_escape.md
```

Compile three times with `xelatex -interaction=nonstopmode -halt-on-error
-no-shell-escape`, passing that TeX filename each time and directing
intermediate files to a temporary build directory. Copy only the resulting
PDF back to the package. Inspect the PDF and check the log for missing
characters and overfull boxes; exit status alone does not check layout.

Inside the repository the canonical paper-edition rebuild command performs
the three TeX passes and archive refresh after the Pandoc step. For a
standalone package, refresh the manifests and archive after copying the PDF:

```bash
python scripts/regen_sha256sums.py
python scripts/build_deposit_zip.py --out 032_witnessed_difference_finite_distinction_carriers_and_history_escape_2026-10-08.zip
python verify_deposit.py
python tools/rebuild_release.py --check
```

The archive command pins the member timestamps to the stated edition date.
Checksum-only commands verify file integrity. The reproduction entry also
runs the finite tests and the Lean build:

```bash
py -3.12 verify_deposit.py --test code/tests/test_proved_rows.py --lean
```

That entry covers Theorem WD2-T1. Lemma WD2-L1 and records WD2-T2 through
WD2-T6 are not Lean theorems in this package.
