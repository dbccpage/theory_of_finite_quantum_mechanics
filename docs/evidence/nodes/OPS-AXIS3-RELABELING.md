# OPS-AXIS3-RELABELING

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Axis 3 of WDP-CH14-T01 under three hypotheses. (i) NS-14: an injective renaming sigma of presentation tokens commutes with the transition step and with full-history replay. (ii) CL-13 (passage_charge_const): a quantity conserved by internal transitions is constant on reachable states and equals its genesis value. (iii) The verdict V reads a history only through a declared export Exp, so V = Vbar o Exp, with Exp(sigma(H)) = Exp(H) for every injective renaming sigma; this is the identical-accessible-exports premise of Proposition 3.1 of the Argon synthesis. Then V(sigma(H)) = V(H), because V(sigma(H)) = Vbar(Exp(sigma(H))) = Vbar(Exp(H)) = V(H). Without (iii) the statement is false (node OPS-REFUTED-AXIS3-WIDE). A drop in the internal defect Delta_O stays computable and renaming-invariant; whether a drop is a repair or a reinterpretation is a question about the grounding map of the tokens, which no export-reading verdict decides.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Conditional on (iii), and on (i) and (ii) as cited, not re-run. WDP-CH14 has no node in this graph; (iii) is read as the observer-quotient reading of WDP chapter 10.

## Source status

Ledger row L035-C3: proved (conditional on (iii)) + cited. NS-14 and CL-13 are read from the Argon synthesis; their Lean sources are not in the source repository and were cited, not re-run.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2526_ops_axis3_relabeling.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2526_ops_axis3_relabeling.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2526_ops_axis3_relabeling.md)
- sha256 (`lf-normalised`): `2c33c8f28221341f65382b0f8acfd2f75591d14e01d45aca7cbbc4236e1c94f7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2526
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `649532625cf9e8ec085a420fd1bad9227fcc4dae9f06ba02be1eb19f497e3ec7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-AXIS3-RELABELING` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY](PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY.md) (DEFINITION)

Outgoing (3):

- `OPS-R-REFUTED-AXIS3-WIDE` `DERIVED_PROSE`: [OPS-REFUTED-AXIS3-WIDE](OPS-REFUTED-AXIS3-WIDE.md) (REFUTED)
- `OPS-R-REFUTED-NB9` `RECORD_PARENT`: [OPS-REFUTED-NB9](OPS-REFUTED-NB9.md) (REFUTED)
- `OPS-R-REGRESS-COROLLARY` `CONDITIONAL_ON_IMPORT`: [OPS-REGRESS-COROLLARY](OPS-REGRESS-COROLLARY.md) (CONDITIONAL)
