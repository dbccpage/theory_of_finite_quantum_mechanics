# OPS-VOROBEV-PATH-INSTANCE

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the path cover {0,1}, {1,2}, {2,3} of four binary measurements, with parity targets 0, 1, 1, the product formula of node OPS-VOROBEV-THEOREM (join-tree edges ({0,1},{1,2}) and ({1,2},{2,3})) gives a probability distribution on the 16 assignments whose three marginals equal the three given tables exactly, and NCF is 1. The GYO reduction empties the three-context path and the two-context path and does not empty the Bell 4-cycle or a triangle. This is one instance of the cited theorem, not a check of it.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

One path cover. The Rust join-tree code and its refusal of the 4-cycle (NotAcyclic) are not run here. The theorem itself is node OPS-VOROBEV-THEOREM.

## Source status

Ledger row L035-B13, the computed part: the Rust test vorobev_product_formula_glues_acyclic_covers_and_refuses_cycles is not run here. The instance is recomputed by checks/independent/foc035_observer_presheaf.py.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/model.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/model.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/model.rs)
- sha256 (`bytes`): `e810daa27f63e26cebb273fc083bef80797858f842573ba2ea837ac75d4ed06e`
- cited in: node.rust, record TFQ-2515

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `acyclic_global_section` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Python: `dag/test_foc035_observer_presheaf.py`

- file: [dag/test_foc035_observer_presheaf.py](../../../dag/test_foc035_observer_presheaf.py)
- sha256 (`bytes`): `17b962ed09fd6127e11d44e3bbc0524f076a9bd85a316992a4e2612ae66a15ee`
- cited in: node.source
- check: `python -m pytest dag/test_foc035_observer_presheaf.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2515_ops_vorobev_path_instance.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2515_ops_vorobev_path_instance.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2515_ops_vorobev_path_instance.md)
- sha256 (`lf-normalised`): `627d18eb7e4ff52955f3568abf87bc459fc6091a7320d0f3447e9878e80da9c7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2515
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

- `OPS-R-VOROBEV-PATH-INSTANCE` `COMPUTED`: [OPS-VOROBEV-THEOREM](OPS-VOROBEV-THEOREM.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

