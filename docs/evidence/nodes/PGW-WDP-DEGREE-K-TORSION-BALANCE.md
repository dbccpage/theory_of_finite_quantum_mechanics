# PGW-WDP-DEGREE-K-TORSION-BALANCE

Stage: [WDP](../stages/WDP.md). Status: `PROVED_PROSE`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH05-P03: on a finite oriented simplicial complex δ^{k+1}δ^k = 0 for every k, since each k-face of a (k+2)-simplex arises by deleting two vertices in either order with opposite signs; each triple (C^{k−1}, C^k, C^{k+1}) with a norm meeting the §4.8 hypothesis is then a window with κ^k well defined on Q^k, 0 → H^k → Q^k → im δ^k → 0 exact, and Γ_{k+1} ≤ ‖δ^k‖_{J→1}Φ_k. WDP-CH05-P06: the six-vertex, fifteen-edge, ten-triangle triangulation of RP² has rank_ℚ δ¹ = 10 and rank_{F₂} δ¹ = 9, so H²(K; ℚ) = 0 while H²(K; F₂) ≅ F₂; the single-triangle indicator is exact over ℚ (Φ₂ = 0) with only non-integral rational repairs. WDP-CH05-P04: on every finite oriented graph Σ_v (d₀*x)(v) = 0, so d₀*x = ρ needs Σ_v ρ(v) = 0 (necessary, not sufficient, and with no closedness or boundary condition); a functional invariant under A ↦ A + d₀λ descends uniquely to Q¹, so the pairing with a 1-cycle is invariant; and δ²δ¹ = 0 on complexes with 3-simplices.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

- Declared finite oriented simplicial complex with a total vertex order and a declared coefficient field (assumption)

## Bottleneck

Written proofs with Python checks and no Lean declaration; the coefficient field is part of the window, the degree-k extension says nothing about cup products or continuum forms, and the balance identities are not physical conservation laws.

## Source status

WDP monograph §5.10-§5.12 WDP-CH05-P03/P06/P04 written proofs; Python simplicial.py

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/06_wdp/tfq_0549_wdp_degree_k_torsion_balance.md`

- file: [dag/derivations/06_wdp/tfq_0549_wdp_degree_k_torsion_balance.md](../../../dag/derivations/06_wdp/tfq_0549_wdp_degree_k_torsion_balance.md)
- sha256 (`lf-normalised`): `de528eb117f82196581677615c3e97e52bf84a0c2553c9f3c4d5661de228359f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0549
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/simplicial.py::gauss_law_solvable`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/simplicial.py::rp2_torsion_witness`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/simplicial.py::verify_nilpotence`

## Absences recorded by the TFQ records

- TFQ-0549 lean4: the claim map records WDP-CH05-P03, P04 and P06 as prose-only
- TFQ-0549 rust: no Rust binding for the degree-k window, the RP2 torsion witness or the balance identities

## Routes

Incoming (1):

- `PGW-R-WDP-DEGREE-K-TORSION-BALANCE` `DERIVED_PROSE`: [PG-WDP-DEGREE1-WINDOW](PG-WDP-DEGREE1-WINDOW.md) (DEFINITION)

Outgoing (1):

- `APP-R-FSP-REGGE-DEFICIT-ACTION` `CONDITIONAL_ON_IMPORT`: [FSP-REGGE-DEFICIT-ACTION](FSP-REGGE-DEFICIT-ACTION.md) (IMPORTED_ASSUMPTION)
