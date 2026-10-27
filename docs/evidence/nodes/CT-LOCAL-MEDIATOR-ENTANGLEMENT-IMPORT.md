# CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported inference, audited against Marletto-Vedral (2017, arXiv:1707.06036, pp. 2-3) and Bose et al. (2017, arXiv:1707.06050, pp. 1-2): if two quantum systems Q1 and Q2 start in a separable state, interact only locally through a mediating system M (Q1 \<-\> M and M \<-\> Q2, with no direct Q1-Q2 interaction, Principle I locality), and end in an entangled state of Q1 + Q2, then M cannot be a classical medium (in Marletto-Vedral, M must have at least two disjoint incompatible observables whose union is not an information variable; in Bose et al., any mediator modeled by local operations and classical communication cannot create entanglement). The repository has no gravity model; TFQ-0084 is a finite shadow only.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 17
- distinct cited Lean declarations covered by a current replay receipt: 17
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- locality of the mediated interaction (assumption)
- information-theoretic definition of a classical mediator (assumption)

## Bottleneck

The inference (arXiv:1707.06036 pp. 2-3; arXiv:1707.06050 pp. 1-2) remains an assumption of this branch. ConstructorTheoryMediatorEntanglement.lean states only a finite shadow: a single linear local map A (x) B applied to one pure bipartite state does not raise the rank of its coefficient matrix (any finite dimension over any field), and for two qubits over Q(i) it does not carry the product state (1,1,1,1)/2 to (1,1,1,u)/2 with u=(3+4i)/5, whose squared concurrence is 1/5. Not stated: mixed states, local channels with ancillas, mixtures of branches, classical communication (LOCC), a mediating system M, the definition of a classical medium, or any gravity model.

## Source status

Audited against the full texts of arXiv:1707.06036 (pp. 2-3) and arXiv:1707.06050 (pp. 1-2, eqs. (1)-(5)) on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ConstructorTheoryMediatorEntanglement.lean`

- file: [lean4/ConstructorTheoryMediatorEntanglement.lean](../../../lean4/ConstructorTheoryMediatorEntanglement.lean)
- sha256 (`bytes`): `370825e363db8a2687c082c86b7038f8acb8a672ba9f367528f5d2eb5768d468`
- cited in: node.lean, receipt dag/research/campaign_ct-local-mediator-entanglement-import_lean_replay.json (ConstructorTheoryMediatorEntanglement)
- replay: `verified`
  - receipt [dag/research/campaign_ct-local-mediator-entanglement-import_lean_replay.json](../../../dag/research/campaign_ct-local-mediator-entanglement-import_lean_replay.json) (module `ConstructorTheoryMediatorEntanglement`): recorded sha256 `370825e363db8a2687c082c86b7038f8acb8a672ba9f367528f5d2eb5768d468` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ConstructorTheoryMediatorEntanglement`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ConstructorTheoryMediatorEntanglement.M_entangled_concurrence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.M_entangled_concurrence` |
| `ConstructorTheoryMediatorEntanglement.M_entangled_det_nonzero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.M_entangled_det_nonzero` |
| `ConstructorTheoryMediatorEntanglement.M_entangled_not_product` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.M_entangled_not_product` |
| `ConstructorTheoryMediatorEntanglement.M_separable_concurrence_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.M_separable_concurrence_zero` |
| `ConstructorTheoryMediatorEntanglement.M_separable_det_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.M_separable_det_zero` |
| `ConstructorTheoryMediatorEntanglement.M_separable_is_product` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.M_separable_is_product` |
| `ConstructorTheoryMediatorEntanglement.applyLocalOp_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.applyLocalOp_det` |
| `ConstructorTheoryMediatorEntanglement.classical_mediator_cannot_produce_entangled_state` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.classical_mediator_cannot_produce_entangled_state` |
| `ConstructorTheoryMediatorEntanglement.concurrence_gap_under_local_op` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.concurrence_gap_under_local_op` |
| `ConstructorTheoryMediatorEntanglement.local_op_concurrence_zero_of_separable` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.local_op_concurrence_zero_of_separable` |
| `ConstructorTheoryMediatorEntanglement.local_op_preserves_product_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.local_op_preserves_product_det` |
| `ConstructorTheoryMediatorEntanglement.no_local_op_produces_entangled_state` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.no_local_op_produces_entangled_state` |
| `ConstructorTheoryMediatorEntanglement.no_local_op_produces_phase_entangled_state` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.no_local_op_produces_phase_entangled_state` |
| `ConstructorTheoryMediatorEntanglement.reduction_of_mediated_entanglement_inference` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.reduction_of_mediated_entanglement_inference` |
| `ConstructorTheoryMediatorEntanglement.schmidtRank_le_one_preserved` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.schmidtRank_le_one_preserved` |
| `ConstructorTheoryMediatorEntanglement.schmidtRank_local_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.schmidtRank_local_le` |
| `ConstructorTheoryMediatorEntanglement.schmidtRank_not_reachable` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ConstructorTheoryMediatorEntanglement.schmidtRank_not_reachable` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2013_ct_local_mediator_entanglement_import.md`

- file: [dag/derivations/30_constructor_theory/tfq_2013_ct_local_mediator_entanglement_import.md](../../../dag/derivations/30_constructor_theory/tfq_2013_ct_local_mediator_entanglement_import.md)
- sha256 (`lf-normalised`): `cb05b1452d07f20c26223ab373376944689b1c7280e857a2ebe77c892b3e0c57`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2013
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ct-local-mediator-entanglement-import.md`

- file: [dag/derivations/independent/ct-local-mediator-entanglement-import.md](../../../dag/derivations/independent/ct-local-mediator-entanglement-import.md)
- sha256 (`lf-normalised`): `5ed6b88d65928fa8dc2aa8febc81936fd5925ed6b5e9c9010096ca80e32920a3`
- cited in: node.source
- counts toward the grade: yes

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
