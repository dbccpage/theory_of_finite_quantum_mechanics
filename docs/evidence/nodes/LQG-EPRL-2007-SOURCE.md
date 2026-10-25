# LQG-EPRL-2007-SOURCE

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `SOURCE_RECORD`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Engle, Livine, Pereira and Rovelli (2008, arXiv:0711.0146, Sections II-IV eqs. (12)-(30) pp. 3-10) define a four-simplex spin-foam vertex amplitude for finite Barbero-Immirzi parameter gamma by imposing the linear simplicity constraint C_f = J_f^(+) - |(1+gamma)/(1-gamma)| J_f^(-) = 0 on Spin(4) representations (eqs. (18)-(20): j^+- = |1 +- gamma| k / 2, embedding the boundary SU(2) spin k into Spin(4) for Euclidean signature and into the SL(2,C) principal series (n, rho) = (2k, 2 gamma k) in Section IV eq. (24) for Lorentzian signature), and Freidel and Krasnov (2008, arXiv:0708.1595, Section II.C Lemmas 2.1-2.4 pp. 10-12 and Section V eqs. (80)-(91) pp. 24-27) construct the coherent-state spin-foam model that coincides with the EPRL vertex for 0 \< gamma \< 1. This node records the two papers.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Record only. The constructions are not reproduced.

## Source status

Audited against the full texts of arXiv:0711.0146 (Sections II-IV eqs. (12)-(30) pp. 3-10) and arXiv:0708.1595 (Section II.C Lemmas 2.1-2.4 pp. 10-12, Section V eqs. (80)-(91) pp. 24-27) on 2026-10-22; recorded as an external source record.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2312_lqg_eprl_2007_source.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2312_lqg_eprl_2007_source.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2312_lqg_eprl_2007_source.md)
- sha256 (`lf-normalised`): `63c59d09fc2858179cb194a50617f12ad570e45bf4054e376757f9149247de48`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2312
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:0708.1595`
- `external:arXiv:0711.0146`

## Routes

Incoming (1):

- `FRO-R-LQG-EPRL-2007-SOURCE` `RECORD_PARENT`: [LQG-PONZANO-REGGE-1968-SOURCE](LQG-PONZANO-REGGE-1968-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-LQG-EPRL-VERTEX-IMPORT` `CONDITIONAL_ON_IMPORT`: [LQG-EPRL-VERTEX-IMPORT](LQG-EPRL-VERTEX-IMPORT.md) (IMPORTED_ASSUMPTION)
- `FRO-R-LQG-SPINFOAM-REVIEW-SOURCE` `RECORD_PARENT`: [LQG-SPINFOAM-REVIEW-SOURCE](LQG-SPINFOAM-REVIEW-SOURCE.md) (SOURCE_RECORD)
