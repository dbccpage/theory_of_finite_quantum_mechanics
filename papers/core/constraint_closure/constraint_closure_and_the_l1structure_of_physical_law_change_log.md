# Change Log — Constraint-Closure Toy Model for $\ell^1$ Residuals on Finite Complexes (GR-002)

--- yaml
title: Constraint-Closure Toy Model for ℓ¹ Residuals Change Log
file_name: constraint_closure_and_the_l1structure_of_physical_law_change_log.md
file_location: coda_atlas/F004_papers/004_general_relativity/002_constraint_closure_and_the_l1structure_of_physical_law/
status: Canonical
evidence_scope: finite_receipts_only
paper_id: GR-002
date: 2026-09-09
---

2026-09-11 — Public Title-Block Cleanup

* Removed internal custody terminology from the public manuscript title area, README header, Zenodo description, and generated PDF front matter.
* Updated the TeX exporter to render Author, Date, Version, and Publication posture as separate stacked lines instead of collapsing them into a single paragraph.
* Reworded the Mechanism Inventory evidence boundary as public-facing "Executable Receipts" language while preserving the same scoped nonclaim.

2026-09-11 — v1.2 TeX Publication Export Correction

* Corrected release metadata from v1.1/v1.0 drift to v1.2 across the manuscript, package metadata, README, and Zenodo description.
* Replaced the emergency ReportLab PDF renderer with a real TeX export path: the builder now emits a `.tex` source and compiles it with Tectonic/XeTeX so mathematical notation is typeset as TeX rather than flattened into ASCII-like text.
* Renamed the Zenodo source bundle to `constraint_closure_toy_model_zenodo_v1_2.zip` and excluded the prior v1.1 ZIP from the v1.2 bundle.
* Rewrote the Zenodo description with Unicode notation where appropriate and recorded `https://zenodo.org/uploads/22715569` as the Zenodo upload URL.

2026-09-11 — Explicit Toy-Model Republication Framing

* Added "toy model" to the manuscript title and front matter.
* Added an author's scope note explaining that this is an as-is continuation of the original constraint-closure toy model, written as an exploratory exercise and not as a derivation of continuous general relativity or physical law.
* Updated README, claim ledger, and package description metadata so the public framing matches the intended Zenodo posture: finite $\ell^1$ quotient/certificate machinery, Regge-style examples, best-effort Python/Lean evidence, and explicit nonclaims.

2026-09-09 — Peer-Reviewed Republication Corrections (Reviewer: Jeremy H. Carroll)

Comprehensive remediation of mathematical scope, computational implementations, and manuscript framing across all 10 items of Jeremy H. Carroll's peer review:

* **Item 1: Corrected Hamiltonian Blind Spot in Wheeler--DeWitt Diagnostic (`wdw_constraint.py`)**:
  * Implemented `build_joint_constraint_system()` and `solve_joint_wdw_constraints()` in $C^1(K) \oplus C^0(K)$ with block operator $D_{\mathrm{joint}} = \begin{pmatrix} d_0 \\ 0 \end{pmatrix}$.
  * Proved that $\Phi_{\mathrm{joint}} = \Phi_{d_0}(p) + \|H_\perp\|_1$, strictly preventing scalar Hamiltonian constraint violations from being absorbed into pure coboundary gauge.
  * Verified on regular 4-simplex boundary $\partial\Delta^4$ with zero momentum, where naive encoding gave $\Phi = 0$ while joint formulation correctly reports $\Phi \approx 103.61 > 0$.
* **Item 2: Simplicial Bianchi Diagnostics & NaN Rejection (`bianchi.py`)**:
  * Withdrew unrestricted 4D scalar Bianchi theorem ($d_2 \varepsilon = 0$); scoped strictly to uniform/abelian complexes.
  * Implemented non-abelian holonomy counterexample on perturbed $\partial\Delta^5$ ($\ell_{01} = 1.1$), yielding $\|d_2 \varepsilon\|_1 \approx 1.9566$.
  * Enforced strict NaN/non-finite rejection in `verify_contracted_bianchi_3d` (`is_satisfied=False`).
* **Item 3: Exact Rational Linear Programming & Nullspace Certificates (`exact_lp.py`)**:
  * Rebuilt exact LP solver over Python `fractions.Fraction` using certified Gauss--Jordan elimination (`_exact_solve_q` and `_exact_nullspace_q`).
  * Verified on Carroll's denominator regression case ($\omega = [1/1000001], D = [[-1, 1]]$), returning exact optimum $0$, $\texttt{is\_closed=True}$, and exporting reconstructed primal gauge parameter $\alpha^*$.
  * Dual nullspace witness certified with exact zero duality gap.
* **Item 4: Dual Certificates, Complementary Slackness & HiGHS Clamping (`dual_witness.py`, `degree2_dual_witness.py`)**:
  * Replaced `np.allclose` heuristic shortcut with exact `np.all(omega == 0.0)`.
  * Clamped SciPy HiGHS tolerances to $\ge 10^{-10}$ (`max(1e-10, float(tol))`), completely eliminating `OptimizeWarning` diagnostics.
  * Exported complete certificates including `primal_alpha`, `beta`, `primal_residual`, `dual_witness`, and explicit complementary slackness checks.
* **Item 5: Ponzano--Regge Asymptotics & Shifted Phase Envelope (`ponzano_regge.py`)**:
  * Corrected semiclassical phase envelope to properly bound shifted physical spins $|j_e + 1/2|$ rather than unshifted variables.
  * Added exact radical expression support for Racah 6j symbols (e.g., $\{1,1,1; 1,2,2\} = -1/\sqrt{20}$).
  * Separated fixed-angle linear functional bounds from dynamical Schläfli path bounds $|S(J') - S(J)| \le \pi \|J' - J\|_1$.
* **Item 6: Realizability & Centered Gram Spectrum Checks (`simplex.py`)**:
  * Implemented strict centered Gram spectrum validation: negative eigenvalues ($< -10^{-10}$) trigger non-realizability rather than silent fallback.
  * Validated Euclidean embedding coordinate reconstruction: pairwise distance error strictly $< 10^{-5}$.
  * Excised unconditional regular simplex fallbacks on unrealizable inputs (e.g., $3 \times 1.0, 3 \times 0.55$).
* **Item 7: Cauchy Sandwich Foliation & Disjoint Top Vertex Mapping (`cauchy_sandwich.py`)**:
  * Replaced fragile $v+n$ indexing with explicit disjoint vertex mapping `top_vertex_map`.
  * Added geometric diagnostics `has_timelike_tracks()`, `is_spacelike_slice()`, and `is_cauchy_foliation()`.
  * Labeled injected test fixtures as synthetic discrete toy models rather than general foliations.
* **Item 8: Falsification of Speculative High-Energy Analogies (`high_energy_fence.py`)**:
  * Corrected hexagonal disk boundary turning angle to $2\pi$ for all radii via Gauss--Bonnet, disproving the claimed $O(R)$ lattice growth.
  * Reframed all 5 receipts as documenting ungrounded analogies and missing discrete physics derivations.
* **Item 9: Retitling & Continuous GR Scope Demotion (`constraint_closure_and_the_l1structure_of_physical_law.md`)**:
  * Retitled paper to: *$\ell^1$ Constraint Residuals on Finite Complexes: Dual Certificates and Regge-Calculus Examples*.
  * Demoted continuous Wheeler--DeWitt and DeWitt supermetric claims to proposed discrete models.
  * Added Section 4.3, Section 8.3, and Section 8.4 covering joint constraint formulations and exact rational worked examples.
* **Item 10: Test Suite Verification (`test_computational_remediations.py`)**:
  * Created comprehensive test suite verifying all 10 review items.
  * Full suite passes: 271 passed, 11 skipped, 0 failures across 8 workers (`pytest -n 8 --basetemp=scratch/pytest_tmp`).
* **Item 11: Consistent Historical Higgs/SUSY Evidence & Linear Certificate (`gauge_higgs_susy_derivation.py`, `higgs_pure_linear_certificate.py`, `claim_vs_reality_plots.py`)**:
  * Reframed `gauge_higgs_susy_derivation.py` and adapter as exploratory historical ansatz demonstrations; computed real SHA-256 witness payload hash and set `is_valid=False`.
  * Replaced broad sampling claims with fixed-carrier quotient homogeneity theorem $\Phi_D(t\omega) = |t|\Phi_D(\omega)$ ($R^2 = 1.000000$ linear vs $0.985563$ quartic).
  * Corrected plots: removed false "1 GeV" natural scale label and "99.6% error", using exact $R^2 = 0.9856$ from certificate.
  * Updated Barbero--Immirzi header with verified finite-run MCMC observations ($80.94\%$ on $[3,8]$ and $0.004\%$ on $[3,15]$ at $k=6$).
* **Item 12: Degree Lifting Arity Repair & Coexact Update Descent Qualification (`higher_simplex_assembly.py`, `discrete_descent_engine.py`, `degree_generic_residual.py`)**:
  * Repaired degree lifting: lifting from degree $k$ targets $(k+1)$-simplices (e.g. tetrahedra with 4 vertices for $C^2 \to C^3$), resolving the arity mismatch where 5-vertex cells were queried against 3-vertex face values.
  * Qualified uncoupled coexact curl updates: on non-manifold complexes (e.g. five triangles sharing an edge), curl increases from $5$ to $20/3$; the engine records $\Delta \gamma = +5/3$ and credits zero canceled mass.
  * Preserved prior-degree obligations: when higher degree residuals vanish while lower obligations remain, engine returns `TYPED_OBSTRUCTION`.
  * Propagated LP failures in `degree_generic_residual.py` as uncertified upper bounds (`is_upper_bound=True`, `lp_success=False`, `is_certified=False`).
  * Qualified midpoint subdivision in `growth_iterator.py` as total variation conserving ($|m-a|+|b-m|=|b-a|$) and SVD extension in `dda_cascade_router.py` as an $L^2$ candidate upper bound.
* **Item 13: Unambiguous State Receipts & Portable Trace Recorders (`certified_pipeline.py`, `dda_trace_recorder.py`, `descent_trace_recorder.py`)**:
  * Implemented length-prefixed structured canonical encoding in `FingerprintedBag.fingerprint()` (`f"{len(k)}:{k}={len(v)}:{v};"`), eliminating the hash collision between `{'a':'bc'}` and `{'ab':'c'}`.
  * Clarified `TransitionCert` as a cryptographic state hash certificate rather than proof of physical correctness.
  * Fixed `IndexError` in both trace recorders by checking `len(parents) > 7` before accessing monorepo mirror paths.
* **Lean 4 Formalization (`lean4/GR002/LinearEnergy.lean`, `manifest.json`, `verify_manifest.py`)**:
  * Formalized fixed-carrier quotient absolute homogeneity $\Phi_D(t\omega) = |t|\Phi_D(\omega)$ and origin unique minimum `linear_energy_has_origin_minimum`.
  * Updated manifest to 6 modules, 20 theorem reports; verified 100% pass via `verify_manifest.py`.
* **Item 14: Monte Carlo Sampling Heuristic & Non-negative Residual Mass (`regge_monte_carlo.py`, `solv_regge_monte_carlo.py`)**:
  * Implemented exact analytical Boltzmann distribution reference $p(6) \approx 0.8095177985$ (`analytical_boltzmann_distribution(beta, immirzi_gamma, k_range)`).
  * Extended `run_regge_monte_carlo_simulation()` to compute Total Variation distance against the analytical distribution and declare `budget_heuristic_reached`.
  * In `ReggeMonteCarloSolverAdapter`, changed certificate type to `"MONTE_CARLO_SAMPLING_RECEIPT"`, set `residual_mass` to non-negative TV distance ($\ge 0$), and preserved signed action ($\approx -2522.45$) in `metadata["total_action"]`.
* **Item 15: Simplex Geometry Scale Invariance & Degenerate Face Detection (`simplex.py`)**:
  * Scale-normalized edge lengths by $L_{\max} = \max(\ell_{ij})$ before constructing the Gram matrix in `compute_simplex_dihedral_angles()` and `reconstruct_simplex_coordinates()`.
  * Verified exact 4-simplex regular dihedral angle $\theta_4 = \arccos(1/4) \approx 1.3181160717$ rad across microscopic ($10^{-8}$), unit ($1.0$), and astronomical ($10^8$) length scales.
  * Replaced manufactured $\cos_n = 0.0$ with explicit `ValueError` when face normals degenerate ($< 10^{-14}$).
  * In `cayley_menger_volume_sq()`, exposed negative squared volume ($< -10^{-12}$) via `ValueError` instead of masking with `max(0.0, val)`.
* **Item 16: Cascade Receipt Predicate Hardening (`solver_of_solvers.py`)**:
  * Fixed `SolverCascadeReceipt.is_solved()` to require `admitted_complex_verified is True`, `terminal_status in ("Exact", "ExactCellAttached")`, `final_residual_size <= 1e-8`, `all(abs(x) <= 1e-8 for x in final_residual_triple)`, and all `prior_degree_obligations` to vanish.
  * Prevents premature declaration of solved status under exhausted authorization or unverified complex admissions.
* **Item 17: Dual Witness Dimension Export & WDW Solver Certification Bridge (`dual_witness.py`, `degree2_dual_witness.py`, `wdw_constraint.py`)**:
  * In `DualWitnessCertificate` and `Degree2DualWitnessCertificate`, added explicit dimension fields (`num_edges`, `num_vertices`, `num_triangles`) to `.to_dict()`.
  * In `wdw_constraint.py`, computed `is_certified` from first-principles mathematical verifications ($r = \omega - D\alpha$, $D^T w = 0$, $\|w\|_\infty \le 1$, $\text{gap} \le \text{tol}$) rather than crashing when older solver interfaces omit the boolean flag.
  * Enforced complete vertex data in `compute_discrete_scalar_curvature()` (raises `KeyError` if vertex is missing).
* **Item 18: Manuscript Formatting & PDF Artifact Withdrawal (`constraint_closure_and_the_l1structure_of_physical_law.md`)**:
  * Replaced raw mathematical pipes in table math with `\Vert \dots \Vert` and `\lvert \dots \rvert` to prevent Pandoc table cell parsing collisions and unicode-math character warnings (`𝜔`, `∑`).
  * Proportioned Mechanism Inventory table separator dashes to guarantee responsive column widths without margin overflow.
  * Formatted monospace Lean and script identifiers in Section 8.6 and 8.7 to ensure proper line breaking.
  * Withdrew the stale `Constraint_Closure_L1_Toy_Model.pdf` artifact after the manuscript retitle; the Markdown manuscript is the canonical source for regenerated publication PDFs.
* **Consolidated Test Verification**:
  * Full suite passes: **286 passed, 11 skipped, 0 failures** across 8 workers (`pytest code/tests -n 8`). Zero regressions.

2026-09-04 — `code/` layout flattened; notebooks moved beside the paper

Layout plus one execution repair. **No mathematical content changed, no claim
was retyped, and no OPEN residual moved.** Exact-head review found that the
relocated `l1_topological_defects.py` evaluated `Optional[...]` without
importing `Optional`, causing two collection errors. Adding the missing typing
import gave 189 passed / 11 skipped both serially under Python 3.12 and with
eight workers under Python 3.14. The earlier description of the suite as
"byte-for-byte the same" is withdrawn: test results are runtime evidence, not
bytes, and this review did not independently replay the pre-change tree.

* Collapsed `code/solvers/`, `code/dda/`, and `code/diagnostics/` into a flat
  `code/`. Those modules already imported each other by bare module name; the
  subpackage boundaries existed only in `sys.path` surgery, not in the imports.
* `code/tests/` is now the single test folder, with a new `tests/conftest.py`
  that puts `code/` on `sys.path`. The per-file `sys.path.insert(..., "solvers")`
  blocks are gone, and the suite now runs from any working directory.
* Moved `code/jupyter_notebooks/` up to
  `002_constraint_closure_and_the_l1structure_of_physical_law/jupyter_notebooks/`.
* **Deleted `code/l1_regge.py`** — a re-export shim pointing at
  `004_projection_obstruction/021_dewitt_superspace_case_study/code/regge_geometry.py`.
  That path does not exist in this repository (the program is numbered `002_`,
  and no `regge_geometry.py` is tracked anywhere), so the module raised
  `ModuleNotFoundError` on import. Every consumer already resolved `l1_regge` to
  `solvers/l1_regge.py`, which shadowed it on `sys.path`; that file is now
  `code/l1_regge.py`. Content is recoverable from git history.
* Receipts follow their producers: `dda/traces/latest_dda_trace.json` →
  `code/latest_dda_trace.json`, and the Higgs certificate JSON sits beside
  `higgs_pure_linear_certificate.py`. Both regenerate byte-identical apart from
  trace timestamps.
* Repointed 17 `code/solvers/` · `code/dda/` · `code/diagnostics/` evidence
  anchors across the paper, the claim ledger, and the package README. All 33
  in-package path anchors resolve.
* Corrected two stale statements found in passing: the paper cited the DDA tape
  as `.agents/dda_traces/latest_dda_trace.json` (the recorder writes
  `code/latest_dda_trace.json`), and the package README claimed "46
  Python/Rust/data files" (there is no Rust in this package).
* Fixed `run_notebook.py`, which pointed at a notebook filename
  (`001_reviewer_constraint_closure_l1.ipynb`) that has never existed here and
  exited 1 on every invocation. It now runs the notebook.

Evidence scope: finite receipts and scoped nonclaims only.
