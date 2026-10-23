# OPS-PARITY-HOLONOMY-LEAN

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In Lean (LggrFiniteResults), take a length n \> 0 and edge parities b : Nat -\> Bool. Let holonomy b k be the exclusive or of b 0, ..., b (k-1), and call g a section when, for every i \< n, the exclusive or of g i and g ((i+1) mod n) equals b i. Then (section_exists_iff_holonomy_zero) a section exists if and only if holonomy b n = false. Further (no_joint_measure_when_holonomy_one), if holonomy b n = true then no finitely supported natural-weight measure on assignments Nat -\> Bool with positive total mass has, for every i \< n, zero pushforward weight on every pair of values (g i, g ((i+1) mod n)) whose exclusive or differs from b i. These are the clause "G(e) is nonempty iff the holonomy h is 0" and the clause "holonomy 1 forbids a positive-mass joint measure with parity-supported marginals" of Proposition B6. Not in Lean: the arc-cover clause, the noncontextual-fraction clause and the Cech-cohomology reading.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The Lean statement is the narrowed one above; no Lean statement mentions a nerve, a cohomology class or the noncontextual fraction. Lean not rebuilt in this change.

## Source status

Ledger row L035-B11: proved + computed + Lean-checked for the two clauses above, any n \>= 1; the arc-cover and noncontextual-fraction clauses stay computed (node OPS-PARITY-CYCLE-DESCENT-NCF). The Lean module is on main; this change did not rebuild it. The ledger records Lean 4.34.0 with axioms propext and Quot.sound only.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/LggrFiniteResults.lean`

- file: [lean4/LggrFiniteResults.lean](../../../lean4/LggrFiniteResults.lean)
- sha256 (`bytes`): `ce736b577beb07997dba02bd7f86f83f1ecac7ce7a569e72b6350171179f34de`
- cited in: node.lean, node.source, record TFQ-2502
- replay: `none`
- check: `cd lean4 && lake build LggrFiniteResults`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `LggrFiniteResults.no_joint_measure_when_holonomy_one` | yes | yes | yes | - | `#print axioms LggrFiniteResults.no_joint_measure_when_holonomy_one` |
| `LggrFiniteResults.section_exists_iff_holonomy_zero` | yes | yes | yes | - | `#print axioms LggrFiniteResults.section_exists_iff_holonomy_zero` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2502_ops_parity_holonomy_lean.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2502_ops_parity_holonomy_lean.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2502_ops_parity_holonomy_lean.md)
- sha256 (`lf-normalised`): `c8fb617bb626f99f71e22d2809f1c6f3512a39590c4078750394a055060d9219`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2502
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

- `OPS-R-PARITY-HOLONOMY-LEAN` `DERIVED_LEAN`: [IMPL-LGGR-FINITE-RESULTS-LEAN](IMPL-LGGR-FINITE-RESULTS-LEAN.md) (PROVED_LEAN)

Outgoing (1):

- `OPS-R-PARITY-CYCLE-DESCENT-NCF` `COMPUTED`: [OPS-PARITY-CYCLE-DESCENT-NCF](OPS-PARITY-CYCLE-DESCENT-NCF.md) (COMPUTATIONALLY_CHECKED)
