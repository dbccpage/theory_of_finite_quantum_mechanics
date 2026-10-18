# GR-002 `code/` — flat module inventory

## Layout

Every module sits **directly under `code/`**. There are no `solvers/`, `dda/`,
or `diagnostics/` subpackages: the modules import each other by bare module
name, so one directory on `sys.path` is the whole import story.

| Path | Content |
|---|---|
| `code/*.py` | Solvers, DDA modules, diagnostics, and the notebook runner |
| `code/tests/` | The suite, plus `conftest.py`, which puts `code/`, the package root, and the CODA repo root on `sys.path` when present |
| `code/*.json` | Regenerable receipts written beside their producers |
| `code/_quarantine_vendored/` | Quarantine landing zone — never an import path |
| `../jupyter_notebooks/` | Reviewer notebook (one level up, beside the paper) |

## Modules

| File | Role |
|---|---|
| `constraint_closure_l1_structure.py` | Facade (Regge + defects + L1 functor) |
| `l1_regge.py` | 2D/3D/4D Regge–Barbero–Immirzi action and curvature deficits |
| `l1_topological_defects.py` | LGGR / Λ residual toys |
| `l1_functor.py`, `poset.py`, `growth_iterator.py` | Structural utilities |
| `l1_sm_susy_proximity.py`, `sm_susy_proximity.py` | Stdlib $\ell^1$ census: uniqueness killed; SM/SUSY extra distances |
| `regge_climb.py` | Ponzano–Regge SU(2), deficit U(1), Witten $Q^2=\Delta$ |
| `regge_walk.py` | $0$–$4$ simplex fixtures, computed residuals, explicit interpretation refusals |
| `regge_alpha_wall.py` | Hex deficit, post-hoc $248\to137$ arithmetic comparison, declared telescoping ansatz |
| `regge_deficit_hexwall.py`, `ponzano_regge_6j.py` | Hex-disk deficit counts; exact Racah fixtures |
| `hodge_split_c3.py`, `hodge_dirac_susy.py` | $C_3$ split ratios; finite Hodge–Dirac linear algebra |
| `linear_energy_obstruction.py` | Degree-one energy family; no Mexican-hat potential |
| `barbero_immirzi_fence.py`, `causal_regge_cdt_fence.py` | Track B action fences (window-relative, declared penalty) |
| `cosmological_ads_fence.py`, `horizon_boundary_fence.py` | Tier-2 sign fixtures; wheel-complex $H^1$ ranks |
| `path_kernel_lift.py` | FOC-012 kernel fixtures; conditional PO-011 $\chi>1$ bound |
| `regge_monte_carlo.py` | Paper-local Regge Monte Carlo fixture |
| `solv_regge_monte_carlo.py` | Thin re-export of `regge_monte_carlo` |
| `regge_susy_saturation_solver.py` | Historical Regge–SUSY bridge |
| `gauge_higgs_susy_derivation.py`, `gauge_higgs_susy_solver.py` | Historical SUSY ladder — **do not re-promote**; imports `universe_anomalonica` |
| `dda_engine.py`, `dda_cascade_router.py`, `solver_of_solvers.py`, `dda_trace_recorder.py` | DDA execution engine, cascade router, solver of solvers, trace tape |
| `pure_diagnostics.py`, `claim_vs_reality*.py`, `higgs_pure_linear_certificate.py` | Kill-track diagnostics and the linear pure certificate |
| `run_notebook.py`, `run_notebook.ps1` | Execute `../jupyter_notebooks/reviewer_constraint_closure_l1.ipynb` |

## Receipts written by this code

| File | Producer |
|---|---|
| `latest_dda_trace.json` | `DDATraceRecorder`, with optional external mirroring only when `CODA_DDA_TRACE_MIRROR_DIR` is set |
| `higgs_pure_linear_certificate.json` | `higgs_pure_linear_certificate.generate_certificate` |

Both are regenerated deterministically apart from trace timestamps.

## Quarantine

`_quarantine_vendored/` is where any accidental nested `omega_engine` monorepo
dump goes. **Do not resurrect** a quarantined tree as PROD, and do not import
from that directory.

## Run the suite

`tests/conftest.py` handles the path, so the suite runs from the CODA checkout
or from the extracted Zenodo source bundle. The source bundle includes an
`omega_engine/` dependency snapshot at its root for the paper-local replay.

```powershell
python -m pytest tests -n 8
```

Or from the repository root, by path.

## Non-claims

Constraint-closure toys **generate candidates**. They do **not** terminalize
SM/Higgs/SUSY/α physics. See the package root README and the salvage
assessment.
