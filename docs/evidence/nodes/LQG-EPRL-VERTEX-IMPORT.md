# LQG-EPRL-VERTEX-IMPORT

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported construction, audited against Engle, Livine, Pereira and Rovelli (2008, arXiv:0711.0146, Section III eqs. (18)-(22), (27)-(30) pp. 6-9 and Section IV eqs. (24)-(25) p. 8) and Freidel and Krasnov (2008, arXiv:0708.1595, Section II.C Lemmas 2.1-2.4 pp. 10-12 and Section V eqs. (80)-(91) pp. 24-27): for a four-simplex with ten triangle spins k_ab and five tetrahedral SU(2) intertwiners i_a, the Euclidean EPRL vertex amplitude embeds each SU(2) representation k into Spin(4) = SU(2)_+ x SU(2)_- at j^+- = |1 +- gamma| k / 2 (so k = j^+ + j^- for 0 \< gamma \< 1 and k = j^+ - j^- for gamma \> 1, eqs. (18)-(20)) and contracts the resulting boosters with the Spin(4) 15j symbol (eqs. (29)-(30)), while the Lorentzian vertex embeds k into the SL(2,C) unitary principal series at (n, rho) = (2k, 2 gamma k) in EPRL's integer-n convention (eq. (24) p. 8, often written (j, gamma j) when indexing by half-integer spin j = n/2 = k). It requires continuum Lie-group representations, the boundary Hilbert space of spin networks and sums over spins whose convergence and continuum limit are open research questions. The repository has finite cyclotomic amplitudes (TFQ-0198) that it refuses to identify with a continuum spin foam.

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

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- SU(2) and Spin(4) representation theory (assumption)
- simplicity constraints and Immirzi parameter (assumption)

## Bottleneck

The repository's fences refuse the identification; no source maps the finite cyclotomic amplitudes to the EPRL-FK amplitude.

## Source status

Audited against the full texts of arXiv:0711.0146 (Sections III-IV eqs. (18)-(30) pp. 6-9), arXiv:0708.1595 (Sections II.C, V) and arXiv:1205.2019 (Part III) on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2314_lqg_eprl_vertex_import.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2314_lqg_eprl_vertex_import.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2314_lqg_eprl_vertex_import.md)
- sha256 (`lf-normalised`): `634b33ea5e4c5858149ccde93407f41af4727a3457591c63c6daaf6adb1ff2c9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2314
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:0708.1595`
- `external:arXiv:0711.0146`
- `external:arXiv:1205.2019`

## Routes

Incoming (1):

- `FRO-R-LQG-EPRL-VERTEX-IMPORT` `CONDITIONAL_ON_IMPORT`: [LQG-EPRL-2007-SOURCE](LQG-EPRL-2007-SOURCE.md) (SOURCE_RECORD), [TFQ-0198](TFQ-0198.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `FRO-R-LQG-CONTINUUM-LIMIT-GAP` `GAP_NO_DERIVATION`: [LQG-CONTINUUM-LIMIT-GAP](LQG-CONTINUUM-LIMIT-GAP.md) (OPEN)
