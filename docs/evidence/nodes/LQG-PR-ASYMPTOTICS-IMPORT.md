# LQG-PR-ASYMPTOTICS-IMPORT

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported asymptotic form, audited against Roberts (1999, arXiv:math-ph/9812013, Theorem 1 eq. (2) p. 22 and Section 6.1 eqs. (12)-(13) p. 61): for large spins with edge lengths l_r = j_r + 1/2 = (a_r + 1)/2 (where a_r = 2 j_r), when the six lengths bound a non-degenerate Euclidean tetrahedron of positive volume V \> 0 and exterior dihedral angles theta_r, the 6j symbol behaves asymptotically as (12 pi V)^{-1/2} cos(sum_{r=1}^6 (j_r + 1/2) theta_r + pi/4) (equivalently sqrt(2 / (3 pi V(a))) cos(sum_{r=1}^6 (a_r + 1) theta_r / 2 + pi/4) where V(a) = 8 V is the volume for side lengths a_r = 2 j_r), and decays exponentially when the Cayley-Menger squared volume is negative (Lorentzian tetrahedron, Section 6.2 p. 62). The phase is the Regge action of the tetrahedron.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- large-spin asymptotics of the 6j symbol (assumption)

## Bottleneck

The asymptotic statement is a limit of real-valued quantities; the repository's exact finite targets do not establish a limit.

## Source status

Audited against the full text of arXiv:math-ph/9812013 (Theorem 1 eq. (2) p. 22, Section 6.1 eqs. (12)-(13) p. 61) on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2307_lqg_pr_asymptotics_import.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2307_lqg_pr_asymptotics_import.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2307_lqg_pr_asymptotics_import.md)
- sha256 (`lf-normalised`): `4c77556d3385fc0d479abf43d882e90d7a872c0a41a5d9668b9d5c41f166a5e4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2307
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:math-ph/9812013`
- `external:book:Ponzano-Regge-1968-Semiclassical-limit-of-Racah-coefficients`

## Routes

Incoming (1):

- `FRO-R-LQG-PR-ASYMPTOTICS-IMPORT` `CONDITIONAL_ON_IMPORT`: [LQG-ROBERTS-1999-SOURCE](LQG-ROBERTS-1999-SOURCE.md) (SOURCE_RECORD), [TFQ-0084](TFQ-0084.md) (OPEN)

Outgoing (1):

- `FRO-R-LQG-PR-ALLOWED-REGION-TARGET` `DERIVED_LEAN`: [LQG-PR-ALLOWED-REGION-TARGET](LQG-PR-ALLOWED-REGION-TARGET.md) (PROVED_LEAN)
