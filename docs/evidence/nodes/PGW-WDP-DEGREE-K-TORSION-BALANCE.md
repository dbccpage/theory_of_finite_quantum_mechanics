# PGW-WDP-DEGREE-K-TORSION-BALANCE

Stage: [WDP](../stages/WDP.md). Status: `PROVED_PROSE`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH05-P03: on a finite oriented simplicial complex δ^{k+1}δ^k = 0 for every k, since each k-face of a (k+2)-simplex arises by deleting two vertices in either order with opposite signs; each triple (C^{k−1}, C^k, C^{k+1}) with a norm meeting the §4.8 hypothesis is then a window with κ^k well defined on Q^k, 0 → H^k → Q^k → im δ^k → 0 exact, and Γ_{k+1} ≤ ‖δ^k‖_{J→1}Φ_k. WDP-CH05-P06: the six-vertex, fifteen-edge, ten-triangle triangulation of RP² has rank_ℚ δ¹ = 10 and rank_{F₂} δ¹ = 9, so H²(K; ℚ) = 0 while H²(K; F₂) ≅ F₂; the single-triangle indicator is exact over ℚ (Φ₂ = 0) with only non-integral rational repairs. WDP-CH05-P04: on every finite oriented graph Σ_v (d₀*x)(v) = 0, so d₀*x = ρ needs Σ_v ρ(v) = 0 (necessary, not sufficient, and with no closedness or boundary condition); a functional invariant under A ↦ A + d₀λ descends uniquely to Q¹, so the pairing with a 1-cycle is invariant; and δ²δ¹ = 0 on complexes with 3-simplices.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

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

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/simplicial.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/simplicial.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/simplicial.py)
- sha256 (`bytes`): `d0ef42d42be42024c1d214899cf0e575b5e2d8a4e63cc4dcf46234af8e06fe5d`
- cited in: record TFQ-0549

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gauss_law_solvable` (python_symbol) | yes | yes | yes | - | - |
| `rp2_torsion_witness` (python_symbol) | yes | yes | yes | - | - |
| `verify_nilpotence` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0549_wdp_degree_k_torsion_balance.md`

- file: [dag/derivations/06_wdp/tfq_0549_wdp_degree_k_torsion_balance.md](../../../dag/derivations/06_wdp/tfq_0549_wdp_degree_k_torsion_balance.md)
- sha256 (`lf-normalised`): `23fd328ffb8619339b13bfa26fbbe611e767bc9894fe86e52e5d849a2987c8bd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0549
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0549 lean4: the claim map records WDP-CH05-P03, P04 and P06 as prose-only
- TFQ-0549 rust: no Rust binding for the degree-k window, the RP2 torsion witness or the balance identities

## Routes

Incoming (1):

- `PGW-R-WDP-DEGREE-K-TORSION-BALANCE` `DERIVED_PROSE`: [PG-WDP-DEGREE1-WINDOW](PG-WDP-DEGREE1-WINDOW.md) (DEFINITION)

Outgoing (1):

- `APP-R-FSP-REGGE-DEFICIT-ACTION` `CONDITIONAL_ON_IMPORT`: [FSP-REGGE-DEFICIT-ACTION](FSP-REGGE-DEFICIT-ACTION.md) (IMPORTED_ASSUMPTION)
