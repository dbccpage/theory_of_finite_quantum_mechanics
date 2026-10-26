# Finite Descent Authority: Packets, Pipelines, and Seven Halt Guards (CODA-FDA)

**Subtitle:** A proposal is not a decision  
**Author:** Jeremy H. Carroll  
**Version:** v0.1.1 Preprint  
**Date:** 2026-09-28  
**License:** Creative Commons Attribution 4.0 International (`CC-BY-4.0`)  
**Zenodo Record:** <https://zenodo.org/records/23025011>  
**DOI:** [10.5281/zenodo.23025011](https://doi.org/10.5281/zenodo.23025011)  

---

## 1. Quick Start & Verification

### Prerequisites
Requires Python $\ge 3.11$. Install the declared verification extras in an isolated environment. Lean uses the exact version in `lean4/lean-toolchain`: `leanprover/lean4:v4.34.0-rc1`.

### Python Automated Tests
Run the complete test suite from the package root:

```bash
python -m pip install ".[test,notebooks]"
python -m pytest code/tests -v
```

Unit, property, mutation, and pipeline integration tests use exact rational arithmetic (`sympy.Rational` / `fractions.Fraction`). Floating-point numbers strictly raise `TypeError`.

Optional parallel test execution:
```bash
python -m pytest code/tests -n 8
```

### Interactive Notebook Exploration
Launch or replay the interactive companion notebooks:

```bash
python -m nbconvert --execute --inplace jupyter_notebooks/*.ipynb
```

Platform launchers are provided:
- Windows: `public_export/run_notebook.bat`
- POSIX: `public_export/run_notebook.sh`

**Notebook Routes:**
- `jupyter_notebooks/000_a_proposal_is_not_a_decision.ipynb`: Demonstrates why high confidence, fluent text, or heuristic scores cannot substitute for a five-field descent packet.
- `jupyter_notebooks/001_the_five_fields_and_seven_guards.ipynb`: Walks through the 5-field packet structure $(K, E, V, \tau, \Lambda)$ and the simultaneous conjunction of 7 derived halt guards.
- `jupyter_notebooks/002_when_confidence_is_not_enough.ipynb`: Explores the exact rational $L_1$ quotient solver bridge, demonstrating how leftover mass feeds into guard $g_3$.

### Lean 4 Elaboration & Axiom Audit
Build the formal mechanization and verify that all proofs elaborate without external axioms:

```bash
cd lean4
lake build
```

Elaborates with 0 `sorry` stubs, 0 external dependencies, and all theorems depending exclusively on kernel axioms (`{propext}`). The axiom audit receipt is recorded in `lean4/axiom_report.txt`.

### PDF Manuscript Compilation
To rebuild the PDF manuscript from LaTeX source:

```bash
xelatex -interaction=nonstopmode coda_fda.tex
```

---

## 2. Package Architecture & Components

**Guard derivation reference (2026-09-23).** `code/coda_fda_core.derive_guards` is the reference derivation of $g_1, \ldots, g_7$: each guard is built from a `GuardEvidence` record, and anything that is not exactly `bool` is rejected. `apps/coda` implements a different, app-level list of seven firewall guards (role separation, exact arithmetic, dual witness validation, cocycle consistency, authority gap, non-terminal budget, verification limits). It is not an implementation of $g_1$ to $g_7$, and this package does not cite it as one.

CODA-FDA formalizes finite descent standing: standing is an internal recorded dependent pair where a sealed pipeline produced a terminal outcome $\mathsf{inl}(t)$ and seven halt guards derived from host evidence hold simultaneously. Without a five-field packet $(K, E, V, \tau, \Lambda)$, the standing type is empty.

### Component Map

| Path | Responsibility | Verification Entry Point |
|---|---|---|
| `code/coda_fda_core.py` | Policy and attestation evaluator; validates 5-field packet, derives/checks 7 halt guards, implements refusal taxonomy, bridges to $L_1$ quotient solver. Strict rational arithmetic; floats and non-booleans raise `TypeError`. | `code/tests/test_coda_fda.py`, `code/tests/test_fda_injected_mutations.py` |
| `code/coda_fda_pipeline.py` | Operational 4-stage pipeline execution harness (`route` $\to$ `descend` $\to$ `verify` $\to$ `terminalize`) extending the single-candidate Lean stage model with tested finite candidate enumeration; records SHA-256 hashed `PipelineTrace` and derives `GuardEvidence` from execution stage records. | `code/tests/test_fda_pipeline_integration.py` |
| `code/cochain_presentation.py` | Standalone exact rational $L_1$ quotient distance solver ($\Phi_1([x]) = \min_f \|x + d_0 f\|_1$) via linear programming vertex certification; provides scalar residual mass for guard $g_3$. | `code/tests/test_coda_fda.py` |
| `code/generate_figures.py` | Script generating pedagogical visualization of guard satisfaction progression. | `code/tests/test_fda_generate_figures.py` |
| `lean4/GtfdaAuthorityCore.lean` | Constructive Lean 4 formalization proving definitional firewalls (FDA-T1–T4, FDA-C1) with 0 non-kernel axioms. | `lean4/GtfdaAuthorityCoreAudit.lean`, `lake build` |
| `lean4/FDA.lean`, `lean4/Algebra.lean` | Lean 4 multi-stage pipeline and regime reconstruction proofs (FDA-T5–T8, observation firewall, replay standing) under `{propext}`. | `lean4/Algebra.lean`, `lake build` |
| `coda_fda.md` | Primary authoritative manuscript (editable Markdown). | Rendered in package root |
| `coda_fda.tex` | LaTeX typesetting source with formal math definitions and citations. | `xelatex coda_fda.tex` |
| `coda_fda.pdf` | Reader-facing compiled PDF publication artifact. | PDF viewer |
| `coda_fda_claim_ledger.md` | Maintained claim ledger cataloging definitions, theorems, halt guard specifications, fault injection mutation matrix, non-claims, and open obligations. | Human review & cross-audit |
| `coda_fda_change_log.md` | Maintained version change log recording measured remediation and release history. | Human review |
| `lean4/axiom_report.txt` | Dated Lean 4 compilation and axiom whitelist verification receipt. | Source verification |
| `public_export/fig1_authority_gate_descent.png` | Pedagogical teaching asset for companion notebooks illustrating discrete guard satisfaction. | `jupyter_notebooks/001_*.ipynb` |
| `docs/zenodo_20472337_corrigendum.md` | Historical correction record for Zenodo record 20472337. | Preserved documentation |
| `docs/lean_claim_map.md` | Lean 4 proof-assistant claim-to-symbol mapping reference. | Complement to claim ledger |
| `CITATION.cff`, `zenodo_metadata.json` | Citation and Zenodo deposit metadata. | Machine-readable metadata |
| `pyproject.toml`, `LICENSE` | Python package configuration and CC-BY-4.0 license grant. | Package tooling |
| `MANIFEST.sha256` | Canonical SHA-256 checksum manifest of source files packaged within the release archive. | `sha256sum -c MANIFEST.sha256` |
| `SHA256SUMS` | Comprehensive repository release manifest covering all release assets including `MANIFEST.sha256`. | `sha256sum -c SHA256SUMS` |

`MANIFEST.sha256` lists the canonical checksums for all source files packaged within the release ZIP. After extracting the release archive, verify integrity using `sha256sum -c MANIFEST.sha256`. `SHA256SUMS` is the repository release manifest covering all release assets including `MANIFEST.sha256`. Release ZIP files are excluded from their contained manifests.

---

## 3. Trust Boundary & Claim Scope

### Module-Level Boundaries
- **Policy Evaluator (`coda_fda_core.py`):** Operates as a pure policy evaluator over caller-supplied attestations. It verifies the presence and structure of the 5-field packet and evaluates whether the supplied evidence satisfies all 7 halt guards. It does not by itself verify the empirical correctness of caller claims.
- **Operational Pipeline Harness (`coda_fda_pipeline.py`):** Executes the internal 4-stage pipeline (`route` $\to$ `descend` $\to$ `verify` $\to$ `terminalize`), requires a declared exact repair map and pending-lift registry callback, checks every candidate certificate against its actual descent, and records immutable canonical evidence. The skeleton callback defaults to the routed state and is sampled at stage boundaries. Residual policy uses the maximum distance over all candidates. Skipped replay fails its guard. Hashes cover the complete serialized payload and certify integrity only; callback meaning and registry completeness remain declared assumptions.
- **Quotient Solver Bridge (`cochain_presentation.py`):** Calculates an exact rational scalar measuring leftover residual mass for guard $g_3$. It is a metric calculator, not an authority-origin theorem.
- **Soundness Scope:** Neither module establishes external semantic verifier soundness. In the formal Lean 4 model, soundness is proved strictly for the regime model ($\mathsf{Standing}_R$, FDA-T7) under two explicit hypotheses (verifier soundness and grant soundness). The operational pipeline record of Definition FDA-D2 is not connected to $\mathsf{Standing}_R$ without a declared regime embedding (such as $R_\Pi$ mapping stage evidence to verification and terminal/guards to recorded grants). A constant-success pipeline inhabiting FDA-D2 does not confer truth; when the verifier is untrusted or unsound, countermodels exist where standing is inhabited yet truth does not hold (FDA-T8).

### Non-Authority Disclosure
"Standing" in CODA-FDA is an internal witness type in a declared, finite formal setting. This work confers no legal, institutional, regulatory, safety, publication, or real-world authority.

### Pedagogical Figure Note
`public_export/fig1_authority_gate_descent.png` is an illustrative teaching asset used in the companion notebooks. The visual steps depict the discrete cumulative satisfaction of the 7 halt guards; the connecting slopes do not represent continuous gradient descent, physical relaxation, or an operational quotient metric.

FDA-T2 models `none` in an optional supplied-packet input. FDA-T9 is a promotion policy; its former categorical no-map statement is withdrawn. See the manuscript for the singleton-functor countermodel.
