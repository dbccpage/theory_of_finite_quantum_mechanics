# CODA-MUR: Certified Representation Transport, Composition, and Irreversible Forgetting

**Subtitle:** A commuting square is not target standing  
**Author:** Jeremy H. Carroll  
**Date:** 2026-09-28  
**Version:** `v3.1.1`  
**License:** Creative Commons Attribution 4.0 International  

---

## 1. Overview

CODA-MUR (Meta & Universal Re-Presentation, Layer 2 of the Calculus of Obstruction, Descent, and Authorization) provides a formal specification, Lean 4 mechanization, and executable Python companion for representation transport, commuting-square composition, and irreversible forgetting.

A transport of a picture is a commuting square: move the states, then look, or look, then move the observations. The two routes agree. Two such squares paste: the composite move still commutes. Collisions travel, and post-processing preserves them. A non-injective collapse has no left inverse recovering every source value. Crucially, a transport certificate $\chi_F$ certifies compatibility with observation; it is not, by itself, target standing.

---

## 2. Directory Layout

```
coda_atlas/F005_coda/mur/
├── coda_mur.md                 # Primary manuscript (Markdown)
├── coda_mur.tex                # Primary manuscript (LaTeX)
├── coda_mur.pdf                # Compiled manuscript
├── coda_mur_claim_ledger.md    # Claim ledger (1-to-1 bijection with MUR-D1–D3, MUR-T1–T8)
├── coda_mur_change_log.md       # Chronological version history and audit log
├── zenodo_metadata.json        # Zenodo deposit metadata
├── CITATION.cff                # Citation metadata
├── LICENSE                     # Creative Commons Attribution 4.0 International
├── pyproject.toml              # Python packaging and isolated test configuration
├── MANIFEST.sha256             # SHA-256 checksums of release files
├── SHA256SUMS                  # Standard format SHA-256 sums
├── code/
│   ├── coda_mur_core.py        # Core transport, pasting, and firewall logic
│   ├── cochain_presentation.py # Vendored standalone exact rational cochain solver
│   ├── generate_figures.py     # Script rendering policy diagnostic figure
│   └── tests/
│       ├── test_coda_mur.py                # unit & adversarial tests
│       ├── test_mur_generate_figures.py    # figure generation test
│       ├── test_mur_injected_mutations.py  # mutation tests
│       ├── test_mur_lean_wrappers.py       # Lean verification tests
│       └── test_mur_notebook_replay.py     # static notebook validation
├── jupyter_notebooks/
│   ├── 000_moving_a_picture_to_a_coarser_one.ipynb # Elementary commuting square
│   ├── 001_when_two_moves_compose.ipynb            # Pasting and composition
│   └── 002_what_you_cannot_get_back.ipynb          # Non-recoverability & cochain solver
├── lean4/
│   ├── lakefile.lean                       # Self-contained Lake build definition
│   ├── lean-toolchain                      # Lean version pin (leanprover/lean4:v4.34.0-rc1)
│   ├── Core.lean                           # Top-level re-export module
│   ├── Algebra.lean                        # Self-contained core reconstruction algebra
│   ├── D01D02D03Records.lean               # Kinds, certificates, and loss ledgers
│   ├── L02TerminalNonBypass.lean           # Concrete countermodel for MUR-T6
│   ├── T01CertificatePasting.lean          # Pasting theorem MUR-T2
│   └── T03T04T05LossNoCreation.lean        # Theorems MUR-T7 and MUR-T8
└── public_export/
    └── fig1_authority_descent.png          # Generated discrete policy diagnostic figure
```

---

## 3. Dependencies & Prerequisites

### Python Environment

- Python >= 3.11
- Required packages: `sympy`, `numpy`, `matplotlib`, `pytest`, `pytest-xdist`, `nbclient`, `nbformat`, `ipykernel`
- Standalone solver: `code/cochain_presentation.py` is vendored directly within the package, requiring zero external monorepo dependencies.

Install dependencies via pip:

```bash
python -m pip install ".[test,notebooks]"
```

### Lean 4 Environment

- Lean 4 toolchain `v4.34.0-rc1` (managed via `elan`)
- Self-contained: `lake build` executes without external mathlib dependencies.

---

## 4. Execution & Verification Instructions

### Python Test Suite

Run the full test suite across 8 logical cores with isolated temporary basetemp:

```bash
python -m pytest code/tests -n 8 -v --basetemp=scratch/pytest_tmp
```

Record collected counts, pass/fail and branch coverage in the release verification receipt.

### Notebook Replay

All three companion Jupyter notebooks can be verified and executed headlessly:

```bash
python verification/replay_notebooks.py --write
```

### Figure Generation

Generate the discrete policy diagnostic figure (`public_export/fig1_authority_descent.png`):

```bash
python code/generate_figures.py
```

### Lean 4 Compilation

Build the complete Lean 4 mechanization:

```bash
cd lean4
lake build
```

Expected output: 12 jobs build cleanly with 0 errors and 0 `sorry`/`admit` tokens.

### LaTeX Manuscript Rebuild

Compile the publication manuscript to PDF:

```bash
xelatex -interaction=nonstopmode coda_mur.tex
```

Expected output: a readable PDF (`coda_mur.pdf`) with embedded metadata and clickable hyperlinks.

---

## 5. Mathematical Scope & Claim Discipline

1. **Definitional & Theorem Scope:**
   - Definitions: `MUR-D1` (Transport), `MUR-D2` (Descent-Square Certificate), `MUR-D3` (Loss Ledger).
   - Theorems: `MUR-T1` (Composite Commutes), `MUR-T2` (Descent Squares Paste), `MUR-T3` (Collisions Transport), `MUR-T4` (Post-Processing Preserves Collisions), `MUR-T5` (Non-Recoverability after Non-Injective Collapse), `MUR-T6` ($\chi$ Alone Does Not Imply Target Standing), `MUR-T7` (Loss Ledger Necessity / Policy Admissibility), `MUR-T8` (Loss Sums Associate).
2. **Explicit Non-Claims:**
   - No general bicategory theorem is proved; associators, unitors, and interchange laws are not asserted.
   - Theorem MUR-T5 proves non-existence of a left inverse recovering every source value after non-injective collapse ($q : \mathbf{2} \to \mathbf{1}$); it does not claim non-existence of right inverses (sections).
   - Loss ledgers are qualitative finite labels; they do not classify all measure-theoretic or continuous information loss.
   - A verified commuting square does not construct or inhabit target standing without target terminalization and target halt guard verification.

## Verified finite interface and formal scope

The runtime requires a nonempty carrier and all four maps, rechecks the requested
source, and binds the transported artifact to the evaluated state map. Flags alone
cannot authorize transport. Optional quotient evidence must match the declared
defect vector and repair map; stored quotient records and matrices are immutable.
The intended meaning of callbacks is a model assumption.

Lean loss ledgers have four Boolean fields only. The Python rational mass and its
addition are an explicitly separate paper/Python extension. Notebook replay is
separate from pytest and uses the current interpreter in a new host process and
kernel for each notebook.
