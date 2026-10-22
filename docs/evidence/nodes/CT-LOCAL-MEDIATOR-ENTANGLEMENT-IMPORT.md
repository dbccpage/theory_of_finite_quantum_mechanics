# CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported inference, audited against Marletto-Vedral (2017, arXiv:1707.06036, pp. 2-3) and Bose et al. (2017, arXiv:1707.06050, pp. 1-2): if two quantum systems Q1 and Q2 start in a separable state, interact only locally through a mediating system M (Q1 \<-\> M and M \<-\> Q2, with no direct Q1-Q2 interaction, Principle I locality), and end in an entangled state of Q1 + Q2, then M cannot be a classical medium (in Marletto-Vedral, M must have at least two disjoint incompatible observables whose union is not an information variable; in Bose et al., any mediator modeled by local operations and classical communication cannot create entanglement). The repository has no gravity model; TFQ-0084 is a finite shadow only.

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

- locality of the mediated interaction (assumption)
- information-theoretic definition of a classical mediator (assumption)

## Bottleneck

The inference (arXiv:1707.06036 pp. 2-3; arXiv:1707.06050 pp. 1-2) is an assumption of this branch. It does not use or support any repository Lean result.

## Source status

Audited against the full texts of arXiv:1707.06036 (pp. 2-3) and arXiv:1707.06050 (pp. 1-2, eqs. (1)-(5)) on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2013_ct_local_mediator_entanglement_import.md`

- file: [dag/derivations/30_constructor_theory/tfq_2013_ct_local_mediator_entanglement_import.md](../../../dag/derivations/30_constructor_theory/tfq_2013_ct_local_mediator_entanglement_import.md)
- sha256 (`lf-normalised`): `2a4eaa620b1641a3d85e1f4c6c6d6482273e47cf316b93c337d08d7271f06dd0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2013
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1707.06036`
- `external:arXiv:1707.06050`

## Routes

Incoming (1):

- `FRO-R-CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT` `CONDITIONAL_ON_IMPORT`: [CT-MARLETTO-VEDRAL-2017-SOURCE](CT-MARLETTO-VEDRAL-2017-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-BACK-CT-MEDIATOR-TO-TFQ0084` `GAP_NO_DERIVATION`: [TFQ-0084](TFQ-0084.md) (OPEN)
- `FRO-R-CT-ENTANGLING-PHASE-FINITE-TARGET` `DERIVED_LEAN`: [CT-ENTANGLING-PHASE-FINITE-TARGET](CT-ENTANGLING-PHASE-FINITE-TARGET.md) (PROVED_LEAN)
