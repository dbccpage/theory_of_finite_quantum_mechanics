# CODA paper package

Start with **[coda.md](coda.md)**, the single active manuscript. Its
**[claim ledger](coda_claim_ledger.md)** records assumptions and evidence;
its **[changelog](coda_change_log.md)** records consolidation and withdrawals.

Version 2.0.1, 2026-09-28. Author: Jeremy H. Carroll.  
**Zenodo Record:** <https://zenodo.org/records/23025415>  
**DOI:** [10.5281/zenodo.23025415](https://doi.org/10.5281/zenodo.23025415)  

| Path | Purpose |
|---|---|
| `coda.md` | Full unified exposition, proofs, examples, source references, and open targets |
| `coda_claim_ledger.md` | Twenty-six current claims and all 48 historical ID dispositions |
| `coda_change_log.md` | Current change record followed by retained historical entries |
| `code/` | Exact examples, certificate checks, tests, figure/notebook recipes, package verifier |
| `lean4/` | Standalone Lean 4.33.0/Std project and twenty-declaration axiom audit |
| `jupyter_notebooks/` | Executed walkthrough of the paper's examples |
| `images/` | Two current scientific figures in PNG/SVG, plus fourteen retained historical SVGs |
| `docs/` | Validation scope, historical-log availability record, scientific descriptions, and references |
| `source_manifest.json` | Historical custody: 17 locally preserved files, 22 external commit-pinned pointers, and six unavailable logs |
| `claim_index.json` | Machine-readable index of the active ledger and historical dispositions |
| `MANIFEST.sha256` | Integrity manifest of deliverable files, excluding generated caches and both manifests |
| `SHA256SUMS` | The same deliverable hashes plus the hash of `MANIFEST.sha256` |

The active exposition is [coda.md](coda.md), and the authoritative claim ledger is
[coda_claim_ledger.md](coda_claim_ledger.md).


## Replay

Run these commands **from this package directory**, using Python 3.13.11 and
the pinned verification environment in
[docs/requirements-verification.txt](docs/requirements-verification.txt). The core
example calculator needs only the Python standard library. NumPy is needed
only for executing the inherited discipline source; plotting, notebook
execution, and testing use the other pinned dependencies.

```powershell
python -m pip install -r docs/requirements-verification.txt
python code/build_claim_index.py
python code/run_examples.py --output code/fixtures/examples.json
python code/audit_legacy_embedding.py --output code/fixtures/legacy_counterexample.json
python code/generate_figures.py
python code/replay_notebook.py
python -m ruff check code
python -m mypy code
```

Run the named test files sequentially:

```powershell
python -m pytest code/tests/test_coda_core.py -q
python -m pytest code/tests/test_coda_discipline.py -q
python -m pytest code/tests/test_adversarial_obstruction_sheaf.py -q
python -m pytest code/tests/test_package_consistency.py -q
python -m pytest code/tests/test_deposit_paths.py -q
python -m pytest code/tests/test_release_boundaries.py -q
```

The notebook replay
creates and shuts down its own temporary kernel using the selected Python
interpreter, without registering a global kernel.

`code/build_notebook.py` regenerates the notebook's source cells and clears
outputs; follow it with `code/replay_notebook.py` when intentionally updating
the recipe. Notebook metadata and figure bytes may depend on the rendering
environment, while the exact mathematical outputs are checked separately.

After reviewing all changed source, output, figure, and PDF artifacts,
regenerate **both** current integrity manifests and run the two verifiers:

```powershell
python scripts/regen_sha256sums.py
python scripts/regen_sha256sums.py --check
python code/verify_package.py
python verify_deposit.py
```

Manifest regeneration records current bytes; it does not establish their
correctness or replace the historical hashes in `source_manifest.json`.
`code/verify_package.py` checks that historical custody, claim/index agreement,
Lean declaration names, local links, exact examples, and notebook structure.
`verify_deposit.py` checks current paths, hashes, and inventory.

For the optional formal check, run `python verify_deposit.py --lean` after the
manifest refresh. It also runs `lake build` and `lake env lean AxiomAudit.lean`
from `lean4/`. Lean 4.33.0 is pinned in `lean4/lean-toolchain`; the project has
no third-party Lake dependencies. The twenty audited declarations cover only
the statements identified in the claim ledger.

See [validation](docs/validation.md) for the actual local results and
their limits. The package is a consolidated manuscript with a finite
companion, not a completed foundation, sealed derivation, or authorization
service. It does not create a release or deposit.

## Release archive identity

The ZIP dated 2026-09-28 contains the current reviewed package snapshot.
Older dated ZIPs are historical release objects; their contents are not the
current working manuscript. Archives are excluded from the manifests they
contain. Publication requires author review of the intended release.
