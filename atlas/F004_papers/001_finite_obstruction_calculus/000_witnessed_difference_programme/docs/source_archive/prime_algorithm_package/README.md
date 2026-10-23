# Algorithm Prime Triad: Candidate Intake, Adapter Descent, and Continuation Control — v1.0.0

**Author:** Jeremy H. Carroll · **Date:** 2026-09-26 ·  
**Paper key:** `008_engine_runtime/000_oe_prime_algorithms` ·  
**DOI:** PENDING

The Omega Engine Algorithm Prime Triad (Prime 000, 001, 002) formalizes bounded candidate intake, adapter descent soundness, and continuation control across discrete reasoning loops. Prime 000 establishes a two-phase protocol separating candidate packet admission from execution and measurement. Prime 001 governs adapter descent soundness and loss ledgers across representations. Prime 002 establishes the master continuation predicate $\mathsf{CanContinue}_n$ and six anti-cheat halting laws that enforce bounded operational termination ($\#\mathrm{ops} \le \lfloor B_{\text{tot}} / \delta_{\text{control}} \rfloor$). This deposit computes every diagnostic exactly over the rationals $\mathbb{Q}$ and mechanizes the core theorems in Lean 4 without Mathlib.

## What is in the deposit

| Path | Contents |
|---|---|
| `oe_prime_algorithms.md` / `.tex` / `.pdf` | the monograph: §1–6 |
| `oe_prime_algorithms_claim_ledger.md` | 21 claims with status and evidence |
| `oe_prime_algorithms_change_log.md` | version history and corrections |
| `code/oe_prime_algorithms.py` | reference implementation (stdlib and `fractions` only) |
| `code/test_oe_prime_algorithms.py` | algorithm tests (≥95% implementation line coverage) |
| `code/test_deposit_tools.py` | archive, extraction, mutation-evidence and notebook-cell regressions |
| `lean4/` | the Lean package (core Lean v4.34.0) and its axiom report |
| `jupyter_notebooks/` | `01_enter_the_triad.ipynb`, `02_falsify_the_laws.ipynb` |
| `docs/` | claim maps, nonclaims, quick start, references, mutation audit |
| `scripts/` | Lean census, mutation audit, claim maps, artifacts, checksums, archive |
| `verify_deposit.py` | the deposit gate |

## Verify

From this directory:

```bash
python -m pytest -q
python verify_deposit.py            # hashes, ZIP payload, tests, implementation coverage, claim maps, ledger bijection, links
python verify_deposit.py --lean     # adds lake build and the axiom census
python verify_deposit.py --full     # adds notebooks, PDF and archive reproducibility
```

`--lean` needs `elan` and Lean v4.34.0. `--full` needs `pandoc`, `pdflatex`, `nbclient` and `ipykernel` (`pip install -e .[dev,notebooks]`).

The default gate needs the test dependencies: `pip install -e .[dev]`.
Inside the ZIP's unpacked `oe_prime_algorithms_1.0.0` directory, use
`python verify_deposit.py --extracted`. That explicit mode checks all payload
files against the internal `MANIFEST.sha256`; the external `SHA256SUMS` and
the ZIP itself are not members of the archive. A normal repository checkout
still requires both external controls and verifies the ZIP's member set and
bytes against the current package.

The [2026-10-02 deposit validation](docs/deposit_validation_2026_10_02.md)
records the maintenance fixes and their validation scope.

## Main results

- **Measurement Never Precedes Admission (`Prime.admission_precedes_measurement`):** An unadmitted candidate packet cannot be measured; any attempt to evaluate $\Phi_1$ or $\Gamma_2$ prior to admission raises a typed refusal.
- **Monotone Phase Embedding (`Prime.embedding_order_preserving`):** Given an assumed monotone map embedding admission into execution, admission precedence reflects in execution for any packet pair where the map is monotone.
- **Continuation Form Reconciliation (`Prime.cc9_implies_cc3`):** The nine canonical conjuncts of $\mathsf{CanContinue}$ imply the weakened three-condition summary form (structural, budget, no-stop).
- **Bounded Operational Termination (`Prime.ops_le_floor_div`):** Given finite initial budget $B_{\text{tot}}$ and cost floor $\delta_{\text{control}} > 0$, the operation count is bounded by $\lfloor B_{\text{tot}} / \delta_{\text{control}} \rfloor$.

## Licence

Text, figures and documentation: CC BY 4.0 (`LICENSE`). Code, Lean and tooling: PolyForm Noncommercial 1.0.0 (`LICENSE-CODE`), with the Required Notice "Copyright 2026 Jeremy H. Carroll". Commercial use needs a separate licence; contact the author via <https://github.com/dbccpage>.

## Citation

See `CITATION.cff`. The Algorithm Prime Triad is operational control, never authority.
