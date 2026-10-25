# LQG-ROBERTS-1999-SOURCE

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `SOURCE_RECORD`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Roberts (1999, arXiv:math-ph/9812013, Section 1 Theorem 1 eq. (2) p. 22 and Section 6.1 eqs. (12)-(13) p. 61) establishes by geometric quantization of the 8-sphere and stationary phase on the symplectic reduction that for an admissible 6-tuple of integers a, b, c, d, e, f (where a = 2j labels the (a+1)-dimensional irreducible representation of SU(2)) whose side lengths form a non-degenerate Euclidean tetrahedron tau of positive volume V(tau) \> 0 and exterior dihedral angles theta_r, the rescaled 6j symbol {ka, kb, kc; kd, ke, kf} has the k -\> infinity asymptotic expansion sqrt(2 / (3 pi V(tau) k^3)) cos(sum_{r=1}^6 (k a_r + 1) theta_r / 2 + pi/4) + O(k^{-5/2}). Since a tetrahedron of side lengths j_r = a_r/2 has volume V_j = V(tau)/8, substituting 2 / (3 pi V(tau)) = 1 / (12 pi V_j) and (a_r + 1)/2 = j_r + 1/2 recovers the Ponzano-Regge prefactor (12 pi V_j)^{-1/2}. This node records the paper's theorem.

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

None recorded.

## Bottleneck

Record only. Audited against arXiv:math-ph/9812013 Theorem 1 eq. (2) p. 22 and Section 6.1 eqs. (12)-(13) p. 61 on 2026-10-22.

## Source status

Audited against the full text of arXiv:math-ph/9812013 (Section 1 Theorem 1 eq. (2) p. 22, Section 6.1 eqs. (12)-(13) p. 61) on 2026-10-22; recorded as an external source record.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2306_lqg_roberts_1999_source.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2306_lqg_roberts_1999_source.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2306_lqg_roberts_1999_source.md)
- sha256 (`lf-normalised`): `abde4fe4149393cca44fe6075fff8c7067c4f8d43c8cd15af456fbde14dfe5a8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2306
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:math-ph/9812013`

## Routes

Incoming (1):

- `FRO-R-LQG-ROBERTS-1999-SOURCE` `RECORD_PARENT`: [LQG-PONZANO-REGGE-1968-SOURCE](LQG-PONZANO-REGGE-1968-SOURCE.md) (SOURCE_RECORD)

Outgoing (1):

- `FRO-R-LQG-PR-ASYMPTOTICS-IMPORT` `CONDITIONAL_ON_IMPORT`: [LQG-PR-ASYMPTOTICS-IMPORT](LQG-PR-ASYMPTOTICS-IMPORT.md) (IMPORTED_ASSUMPTION)
