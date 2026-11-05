Change Log — GS-002: SO(k)-Invariant Gauge Rigidity
===================================================

--- yaml
title: GS-002 SO(k)-Invariant Gauge Rigidity Change Log
file_name: 008_so_k_invariant_gauge_classification_change_log.md
file_location: omega_engine/research/published/005_gauge_selection/
status: Canonical
paper_id: GS-002
canonical_version: v2.0.0
legacy_filename: 002_so_k_invariant_gauge_classification.md
date: 2026-09-21
---

Unreleased publication review of the v2.0.0 candidate (2026-10-02)
---

The canonical candidate remains `v2.0.0`; this review does not publish a new
Zenodo record or relabel the retained 2026-09-28 Lean build as fresh.

* Restored boundedness in the imported finite-dimensional unit-body statement, matching companion §2.2; kept its imported status. Specified compact orbit-hull hypotheses.
* Declared indexed directed edges, target-stalk transport direction, and the identity-transport scope of ordinary divergence and cycle sums. Added explicit cycle repair and extremum attainment arguments and the scalar-incidence operator-norm formula.
* Repaired small-circulation routing and norm underflow, invalid certificate tolerances, NaN/negative/vacuous gauge audits, degenerate-face orientation selection, smoothed-solver tolerance use, and closure ratio/zero reporting. Added independent regression probes.
* Completed the related source identifier in Zenodo metadata. The metadata gate now rejects incomplete relations and invalid dates/types; the Lean gate requires the stored and fresh axiom dependency sets to match.
* Clarified numerical and formal evidence scopes, completed the claim map, added a study guide and sixteen written Landau problems with solutions, and added notebook assertions.
* Rebuilt the manuscript PDF and deterministic release envelope. Fresh validation and blocked gates are recorded in `docs/publication_review.md`.

Unreleased maintenance for the v2.0.0 candidate (2026-09-21)
---

This maintenance does not promote the canonical release identity beyond
`v2.0.0`.

* **F1 (Honest Numerical Solver Representation):** Renamed general solver facade to `SOCPCertifier` with `solver_method="numerical_socp_subspace"`, reserved "exact" exclusively for `CycleClosedFormCertifier` and coboundary solutions, replaced `exact: bool` with `method="auto" | "cycle_closed_form" | "numerical"`, and recorded the signed weak-duality gap `signed_duality_gap = primal_value - dual_value`.
* **F2 (Fail-Fast Input Domain Validation & Secondary Gaps Closed):** Added strict preconditions rejecting invalid theorem-domain inputs: Cochain data rank $\le 2$, degree $\in \{0, 1, 2\}$, finite reals; strictly positive, finite edge and face weights; GraphComplex vertex bounds checking ($0 \le u, v < V, u \ne v$); CoordinateL1Solver cochain dimension matching; analytical cycle weights length matching; orientations strictly in $\{+1, -1\}$; holonomy matrix squareness, $\mathrm{SO}(k)$ orthogonality, and unit determinant; empty-edge complexes rejected at construction ($m \ge 1$); non-boolean integer types enforced for graph endpoints, stalk dimensions, and vertex counts; dimension scaling requiring positive integers $k \ge 1$; rotation generators requiring positive integers $k \ge 1$; $\mathrm{SO}(2)$ rotation requiring finite real angles; sphere constancy audit requiring finite positive radius and finite nonnegative tolerance; and cochain shape and orientation validation in `CycleClosedFormCertifier.certify`.
* **F3 (Self-Contained Release Surface):** Removed unused `matplotlib` dependency and placeholder figure generation, eliminated stale figure test, and authored comprehensive `code/README.md` documenting architecture, solver bounds, and quick start.
* **F4 (Honest Connection Repair & Vertex Gauge Conjugacy):** Renamed invasive connection recovery to `test_connection_corruption_and_direct_repair` (honest direct replacement); implemented `apply_vertex_gauge_transformation` and added `test_vertex_gauge_transformation_conjugacy` verifying that $H_C' = g_0 H_C g_0^T$ preserves curvature, eigenvalues, and trace; and added an $\mathrm{SO}(3)$ noncommuting product-order regression test.
* **F5 (Closure Candidate vs Certified Infimum):** Separated `candidate_primal_value` from `certified_quotient_value` (None if certificate not optimal), with fail-closed `certified_bound_holds = cert.is_optimal and candidate_bound_holds`.
* **F6 (Canonical Package Architecture & Test Expansion):** Relocated all implementation modules directly into `code/` (`carrier.py`, `closure.py`, `cycle_analytics.py`, `falsification.py`, `gauges.py`, `socp_certifier.py`, `socp_exact_certifier.py`, `solver.py`, `__init__.py`), completely removed legacy subfolder `code/so_k_gauge/`, provided `so_k_gauge.py` as an in-process backward-compatibility facade mapping `sys.modules["so_k_gauge.<module>"]` for external callers and notebooks, and expanded test suite to 100 tests (11 modules) passing with 98.85% statement coverage, verifiable over 8 parallel workers (`pytest -n 8`).
* **F7 (Header Centering Discipline):** Deployed zero-horizontal-line centered header block (Title, Subtitle, Author, Date, Version, License) across `.md`, `.tex`, and `.pdf`, eliminating `\maketitle` rule injection and empty table of contents.
* **F8 (Claim and Receipt Custody):** Marked Theorem 2.1 as imported evidence rather than a local proof, scoped Theorem 3.2 to conditional/definitional aggregation, censused every Lean theorem and lemma, and regenerated the deterministic manifest and archive envelope.

v2.0.0 (2026-09-21) — Major Revision for Zenodo Republication (B1–B13 Resolution)
---

* **B1, B4, B5, B6 (Mathematical Scope & Section 5.3 Excised):** Excised §5.3 in full, removing the falsified non-Abelian holonomy inequality (§5.3.1 / E1), unverified numerical stability overclaims (§5.3.2 / E2), and unsupported McLachlan trace-norm oblique projection attribution (§5.3.3 / E3). Withdrew claims C25, C26, and C27 from the claim ledger and removed corresponding code and test helpers.
* **B2 (Carrier Rectification):** Replaced the acyclic poset-cover carrier with a finite directed graph complex $G = (V, E)$ throughout manuscript prose, definitions, theorems, and code, fully supporting directed cycles and circulations.
* **B3 (Corollary 3 Scope):** Corrected Corollary 3 to conclude native-norm rigidity $j(x) = c \|x\|_V$ generally under transitive linear isometric action, reserving Euclidean $\ell^2$ for the declared standard $\mathrm{SO}(k)$ action on Euclidean $\mathbb{R}^k$. Updated ledger row C5.
* **B7 (Lean Provenance Reconciled):** Pinned Lake package to `gs002` (library target `GS002`), toolchain to `v4.34.0-rc1`, verified SHA256 hashes of all eight Lean sources in `lean4/PROVENANCE.md`, and synchronized all file paths and theorem descriptions across the manuscript and ledger.
* **B8 (Dependency Declaration):** Added `scipy>=1.10.0` and `matplotlib>=3.7.0` to runtime dependencies in `pyproject.toml`, and verified that a clean install collects and passes all 51 tests with 98.93% coverage.
* **B9, B10 (Release Package & Integrity):** Cleaned package structure, updated `pyproject.toml` to point to full `README.md`, populated all documentation guides (`docs/quick_start.md`, `docs/descriptions.md`, `docs/keywords.md`, `docs/references.md`), built comprehensive `claim_code_map.yaml` (C1–C24), renamed numerical optimizer to `numerical_socp_subspace` with explicit `is_zero_gap: bool = False`, and purged stale `.coverage` files.
* **B11 (Scientific Figure):** Replaced placeholder cosine curve with scientific visualization of $\ell^1$ vs $\ell^2$ unit ball geometry, triangle circulation defect, and dimension scaling.
* **B12 (House Dialect Stripped):** Excised internal governance jargon (ENC-1138, charter §6.2, R2a/R2b, Q-gated G7, GTOC lift discipline, terminalizer) and formatted academic references cleanly.
* **B13 (Version & Metadata):** Bumped version to `v2.0.0` (advancing past published Zenodo record v1.1), adopted canonical title *SO(k)-Invariant Gauge Rigidity for Declared Euclidean Stalks: Local $\ell^2$ Selection and Outer $\ell^1$ Aggregation (GS-002)*, set `publication_type: preprint`, and aligned `zenodo_metadata.json`.

v1.0 (2026-09-21) — Release Pre-Flight Normalization
---

* Enforced Stage 4 clean manuscript law: deployed strict 4-field header.
* Delegated internal proof packet ledgers, support ledgers (S1–S9), and import registers (I1–I8) to companion claim ledger.
* Cleaned house dialect references and normalized imported theorem tags to standard academic citations ([2]).
* Synchronized and compiled publication-grade preprints (.tex and .pdf) and updated SHA256SUMS.

v1.0 (2026-07-25) — Gauge Selection Programme Normalization
---

* Standardized primary paper identity as `GS-002 — SO(k)-Invariant Gauge Rigidity for Declared Euclidean Stalks` (legacy identity: `Paper 002`, `Paper 006`).
* Positioned as Step 3 in logical programme order (the vector $SO(k)$ branch).
* Separated local gauge selection ($SO(k) \to \text{local } \ell^2$) from outer aggregation (edge additivity $\to \ell^1(E;\ell^2)$).
* Fenced imported Euclidean inner product: declaring $SO(k)$ symmetry admits Euclidean stalk structure; Theorem 3.1 is rigidity relative to that admitted structure.
* Consolidated in-body version history into this companion change log.

v0.1.0 (June 2026)
---

* Pre-print establishing $SO(k)$-invariant gauge classification and mixed $\ell^1(E;\ell^2)$ edge aggregation.
