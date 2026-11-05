# PO-034: Higher-Cell Product Retractions, Simplicial Cochains, and Finite Retraction Dynamics

Technical preprint **v0.1 (0.1.0)**, dated 2026-10-10. First publication
candidate; deposition not verified.
The Python example package separately retains its existing 0.1.0 code version.

The principal correction distinguishes the product-state complement Q from
the highest-order component projector R_k. A two-site interaction inside a
three-site cell can have QL=L while R_3 L=0.

- [Manuscript](higher_cell_cochain_projection_and_retraction_dynamics.md)
- [PDF](higher_cell_cochain_projection_and_retraction_dynamics.pdf)
- [Claim ledger](claim_ledger.md) and machine-readable [ledger](claim_ledger.yaml)
- [Notebook](jupyter_notebooks/034_higher_cell_projection_demo.ipynb)
- [Formal evidence scope](lean4/README.md)
- [Review receipt](docs/review_receipt.md)
- [Historical release validation, 2026-10-10](docs/release_receipt_2026-10-10.json)

The formerly adjacent JSON release receipt is now kept with this paper. Its
bytes and recorded hashes are unchanged: it describes the 2026-10-10 archive,
not the rebuilt archive containing this receipt. Its 74 focused tests, static
Lean census and direct notebook replay are historical results; fresh pinned
Lean and native Jupyter execution were explicitly excluded. Git history
preserves the earlier archive identified by that receipt.

The ledger contains thirteen claims, including six written-only lemmas.
Its seven stored Lean targets cover conditional abstract projector identities.

The finite Taylor bound uses the operator norm of the **whole Hamiltonian**.
The polar witness certifies a residual norm, without an automatic tangent
annihilator property. Hodge calculations use scalar constant coefficients.
The seven-step protocol helper is an unevaluated schema.

## Reproduce the numerical review

From this package directory, using Python 3.12 and uv:

~~~bash
uv sync --project code --frozen --extra dev --extra notebooks
uv run --project code python -m pytest code/tests -q
uv run --project code python scripts/replay_notebook.py --direct
uv run --project code python verify_deposit.py --review
~~~

For integrity and evidence mappings without executing tests, use
`python verify_deposit.py --integrity-only --archive /absolute/path/to/release.zip`.
The selected ZIP is checked byte for byte against the current payload.

The review mode checks integrity, claim mappings, numerical tests,
direct notebook replay, and the static Lean census. It does not
claim fresh Lean compilation or native Jupyter execution.

For the complete replay gate, omit --review. This attempts a pinned Lean
build and native notebook replay and fails if either is unavailable.
The notebook driver creates a temporary kernel specification for the active
Python interpreter.

## Rebuild the artifacts and archive

~~~bash
uv run --project code python code/generate_figures.py
python scripts/build_paper_artifacts.py
python tools/rebuild_release.py
python tools/rebuild_release.py --check
~~~

Pandoc and XeLaTeX are required for the paper. All PDF pages must be rendered
and inspected after substantive edits. The build rejects overfull boxes and
missing characters. All release scripts use one manifest/archive contract.

Checksums and ZIP validation establish byte identity. They do not demonstrate
mathematical claims, confirm Zenodo publication, or grant authority.

Manuscript, figures, and prose: CC-BY-4.0 (LICENSE).
Code, Lean sources, notebooks, and tooling: PolyForm Noncommercial 1.0.0
(LICENSE-CODE). License files are unchanged.
