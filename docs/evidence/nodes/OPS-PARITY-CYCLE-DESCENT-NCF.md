# OPS-PARITY-CYCLE-DESCENT-NCF

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For n = 3, 4, 5 and every one of the 2^n parity-target vectors t on the n-cycle of binary measurements (contexts {m_i, m_(i+1 mod n)}, each distribution uniform on the two pairs with x_i xor x_(i+1) = t_i), let h be the exclusive or of the t_i. Then |G| is 2 if h = 0 and 0 if h = 1; the arc cover {m_0, ..., m_(n-2)}, {m_1, ..., m_(n-1)} has exactly 2 matching families, both with one gluing if h = 0 and both without a gluing if h = 1; and NCF is 1 if h = 0 and 0 if h = 1. That is 8 + 16 + 32 = 56 cases.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Finite cases n = 3, 4, 5 only. The two clauses proved in Lean for every n are in node OPS-PARITY-HOLONOMY-LEAN; the arc-cover and NCF clauses for general n are not claimed.

## Source status

Ledger row L035-B11, the clauses that stay computed: the Rust test parity_cycles_holonomy_decides_descent_and_strong_contextuality is not run here. The 56 cases are recomputed by checks/independent/foc035_observer_presheaf.py.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/parity.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/parity.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/parity.rs)
- sha256 (`bytes`): `0605ef9be260d46ecfabbb6f8fd1c19eb5fcffc13b18f0fd9fe2bef3b315aef4`
- cited in: node.rust, record TFQ-2511

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ParityCycle` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Python: `dag/test_foc035_observer_presheaf.py`

- file: [dag/test_foc035_observer_presheaf.py](../../../dag/test_foc035_observer_presheaf.py)
- sha256 (`bytes`): `a6ef3d2de18f783960c87ac49fee3467ae4e5ef18ac598ee533c0fa907ada1c7`
- cited in: node.source
- check: `python -m pytest dag/test_foc035_observer_presheaf.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2511_ops_parity_cycle_descent_ncf.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2511_ops_parity_cycle_descent_ncf.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2511_ops_parity_cycle_descent_ncf.md)
- sha256 (`lf-normalised`): `10a67427df7b0c433a7fdbefd788b00a8d30101c1bbd586c805585291d00f0fa`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2511
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

- `OPS-R-PARITY-CYCLE-DESCENT-NCF` `COMPUTED`: [OPS-PARITY-HOLONOMY-LEAN](OPS-PARITY-HOLONOMY-LEAN.md) (PROVED_LEAN), [OPS-MAXIMAL-COVER-DESCENT](OPS-MAXIMAL-COVER-DESCENT.md) (PROVED_PROSE)

Outgoing (1):

- `OPS-R-Z2-WITNESS-FALSE-NEGATIVES` `GAP_NO_DERIVATION`: [OPS-Z2-WITNESS-FALSE-NEGATIVES](OPS-Z2-WITNESS-FALSE-NEGATIVES.md) (IMPORTED_ASSUMPTION)
