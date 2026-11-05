---
title: GS-000 Coordinate-Wise Additivity Change Log
file_name: 009_coordinate_wise_additivity_change_log.md
file_location: omega_engine/research/published/005_gauge_selection/
status: Canonical
authority_effect: None
paper_id: GS-000
canonical_version: v6.1.1
canonical_version_doi: 10.5281/zenodo.20723753
repository_state: unpublished post-v6.1.1 draft
legacy_filename: 003_coordinate_wise_additivity.md
date: 2026-10-02
---

# Change Log — GS-000: Coordinate-Wise Additivity

## Unpublished draft review — 2026-10-02

- Preserved canonical v6.1.1 / DOI identity; assigned no new publication version.
- Made k≥1 and the inherited local-seminorm argument explicit, including empty-edge and positivity boundaries.
- Corrected fixed-profile quotient factorization and separated the coarser-total and varying-profile witnesses throughout manuscript, notebooks, and ledgers.
- Removed unsupported kernel-uniqueness and PCC implication claims; clarified weighted coarea, directed-edge counting, and binary-minimizer scope.
- Restricted the subadditive CE5 candidate to 0<p<1 after weakening seminormhood; kept the matching formalization obligation open. Corrected CE1/CE3 arithmetic-helper scope.
- Hardened core finite probes, graph diagnostics, and imported quantum examples against invalid carriers, negative/nonfinite weights, NaN outputs, invalid orbit indices, empty probes, mismatched counts, and invalid density/channel inputs.
- Added the 20-question Landau quiz, worked key, study guide, and exact arithmetic capstone.
- Corrected notebook CE3 labeling, theorem names, and the strict-CPTP-contraction statement. Recorded isolated direct Python cell execution; native kernel replay was unavailable.
- Removed the identifierless metadata relation and added a regression gate. Replaced stale Banach-presheaf descriptions and keywords with the finite theorem scope.
- Rebuilt TeX/PDF, restored the suppressed counterexample headings, and refreshed the dated draft archive; regenerated both manifests against Git checkout bytes, correcting the Windows launcher hash mismatch. Added LF text attributes for reproducible checkouts.
- Lean proof sources and the historical axiom report are unchanged; this review attests no fresh Lean compilation or full release-gate pass.


## Unpublished repository draft (2026-09-28)

* Reconciled the package identity to the canonical published version, v6.1.1,
  DOI `10.5281/zenodo.20723753`. Later repository bytes remain unpublished and
  have no assigned public version or DOI.
* Kept Counterexample 5 and the manuscript-level LGGR reading in section 3.5
  `OPEN / NOT_VERIFIED`. Lean and Python helpers cover narrower executable
  witnesses and do not promote those broader prose claims.
* Refreshed the focused 81-test receipt, all three notebook replays, the
  complete 43-target Lean axiom census, and the deterministic release envelope.

## Unpublished packaging draft (2026-09-19)

* Synchronized release date to `2026-09-19` across manuscript, Zenodo metadata, and companion artifacts.
* Added standalone fail-closed deposit verifier `verify_deposit.py` and packaging tooling (`scripts/regen_sha256sums.py`, `scripts/build_deposit_zip.py`).
* Added companion notebook execution integrity test suite (`code/tests/test_notebooks.py`).
* Recorded a platform-normalized Lean 4 report with 28 output entries. That partial
  receipt is superseded by the current complete 43-target axiom census.
* Recorded repository-local verification evidence. It did not mint a version,
  establish publication readiness, or modify the canonical Zenodo record.

## Unpublished programme normalization (2026-07-25)

* Standardized primary paper identity as `GS-000 — Coordinate-Wise Additivity and Local ℓ¹ Gauge Selection` (legacy file: `003_coordinate_wise_additivity.md`, Paper 003 / Paper 004).
* Positioned as Step 1 in logical programme order (the purely finite coordinate-separable base theorem).
* Proved Theorem 1 ($\nu_e(x) = w_e \sum_i |x_i|$) under edge locality, coordinate permutation symmetry, disjoint-coordinate additivity, seminorm absolute homogeneity, and graph-isomorphism invariance.
* Consolidated in-body version history into this companion change log.

## v0.1.0 (June 2026)

* Pre-print establishing the coordinate-wise additivity selection theorem,
  CE1–CE4, and the still-open CE5 candidate.

## Extracted from paper body (preflight G6)

## Changelog

### Unpublished post-v6.1.1 draft record (2026-06-21)

* Reconciled Lean-status metadata with the 2026-06-20 proof-ledger discharge of PL-004-2: `PaperGS003/CoordinateL1.lean` now covers the declared finite orbit-action formulation of Theorems 1-3, including `orbit_uniform_l1_collapse` and `edge_uniform_l1_collapse`. This work was not deposited as v6.1.2; it remains part of the unpublished repository draft. No theorem statement or proof was widened; H1-H5 plus edge-transitivity or explicit uniformity remain the hypotheses for the unweighted global `l1` collapse.

### v6.1.1 (2026-06-16)

* Corrected the Lean-status description. The committed `PaperGS003/CoordinateL1.lean` does **not** provide an "integer finite-coordinate scaffold for Theorems 1–3" (that phrasing described a transient working-tree stub); it machine-checks scoped arithmetic helpers, the Theorem 3 edge-uniformity collapse, and primitive-difference quotient-boundary helpers. `lake build PaperGS003` was green with standard-only axioms. At v6.1.1, full formalization of Theorems 1–3 over real cochains remained open under PL-004-2, and CE5 plus the manuscript-level LGGR reading remained `OPEN / NOT_VERIFIED`. Later repository work does not retroactively alter that published status.

### v6.1 (2026-06-15)

* Added §3.5 **LGGR Connection**: proposed the gap between orbit-weighted
  $\ell^1$ and unweighted global $\ell^1$ as an instance of Local Green
  $\ne$ Global Red. The manuscript-level relation remains `OPEN / NOT_VERIFIED`.
* Added §3.6 **EPK Generalization Frontier**: the diagnostic geometry is determined by the observer’s declared kernel structure, not by the ambient vector space alone.
* Added Lean4 support in `PaperGS003/CoordinateL1.lean`: finite arithmetic cores
  for CE1–CE4, a narrower CE5 helper, and the Theorem 3 edge-uniformity collapse,
  plus primitive-difference quotient-boundary helpers. Neither the broader CE5
  prose claim nor the manuscript-level LGGR reading was thereby promoted.
* Added Lean4 mechanization status to the claim ledger.
* No scope widened: the full prose Theorems 1–3 remain proven conditionally in
  the paper, while full Lean mechanization of their general finite induction
  bridge remained PL-004-2 at v6.1. Later work belongs to the unpublished
  repository draft rather than a published v6.1.2.

### v6.0.1 (2026-06-09)

* Improver hygiene pass (Stage 1). Part A rubric verified present (lead sentence, why-care, related work §1.1, worked replay, falsifiability, non-claim box) — no padding added.
* Made explicit the $\ell^1$-isometric fiber hypothesis in Axiom 4 (coordinate action by signed permutations) and cited it at the point of use in Theorem 2's orbit weight-equality step. This closes the only implicit hypothesis found; no claim types changed.
* Created sibling claim ledger `003_coordinate_wise_additivity_claim_ledger.md`; registered Paper 004 obligations in the global proof ledger (`proof_ledger_20260609.md`).

### v6.0 (May 2026)

* Added publication status box.
* Clarified dependency order and repository numbering.
* Softened over-strong physical/finite-structural language.
* Clarified orbit-weighted versus edge-uniform $L^1$ in Corollary 2.2.
* Removed duplicated §3.2 paragraph.
* Polished the compressed conditional characterization in §3.4.

### v5.0 (May 2026)

* Added cross-reference to Paper 000 v004 [8] (observer theory, contextual congruence, reflective completion).
* The coordinate-wise additivity result provides the combinatorial base case for the gauge classification hierarchy. Observer passivity (O1 in [8]) constrains downstream processing of the $\ell^1$ diagnostic derived here.

### v4.0 (April 2026)

* Audit-hardened pre-print. Clarified orbit-weighted vs. uniform $\ell^1$.

---
