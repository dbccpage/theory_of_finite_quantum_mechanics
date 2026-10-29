# OPS-NOISY-PR-NCF

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the Bell scenario let the noisy PR box be e_lam = (1 - lam) PR + lam U, where U puts 1/4 on every local outcome pair. The exact noncontextual fraction is 1/2 at lam = 1/4 and 1 at lam = 1/2, which is 2 lam at both points. The l1 defect to conv(A) is positive at lam = 1/4 and 0 at lam = 1/2, and the global support has 16 elements at both points. The closed form 2 lam for every lam below 1/2 is not claimed.

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

Tested points only. The Rust receipt replay clause of the ledger row is in node OPS-RUST-RECEIPTS-AND-LIMITS.

## Source status

Ledger row L035-B5: computed by the Rust tests noisy_pr_box_has_exact_noncontextual_fraction_two_lambda and tampered_receipts_are_rejected_by_replay, which are not run here. This node is COMPUTATIONALLY_CHECKED on the strength of checks/independent/foc035_observer_presheaf.py, which restates the box, solves each linear programme exactly and re-verifies the answer with an explicit primal and dual certificate; it does not run the Rust code.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/model.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/model.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/model.rs)
- sha256 (`bytes`): `f3394e924037042349bc7593855651e9f470d5b57fd5512b82e7761a8e40765a`
- cited in: node.rust, record TFQ-2505

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `noncontextual_fraction` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Python: `dag/test_foc035_observer_presheaf.py`

- file: [dag/test_foc035_observer_presheaf.py](../../../dag/test_foc035_observer_presheaf.py)
- sha256 (`bytes`): `66148a006577647bc2bd17c8f113a125215d40d946a9be29ba9325051e04828b`
- cited in: node.source
- check: `python -m pytest dag/test_foc035_observer_presheaf.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2505_ops_noisy_pr_ncf.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2505_ops_noisy_pr_ncf.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2505_ops_noisy_pr_ncf.md)
- sha256 (`lf-normalised`): `c146a47465ef73fc7171d602218d9975ad50d9c24d3a253cd72c91379f85d9f5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2505
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `ae5564735bb6591e0f149868f83bd9f9793f297be0f8af3cc889c293ae4059cb`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-NOISY-PR-NCF` `COMPUTED`: [OPS-NCF-LHV-EQUIVALENCE](OPS-NCF-LHV-EQUIVALENCE.md) (PROVED_PROSE)

Outgoing (1):

- `OPS-R-RUST-RECEIPTS-AND-LIMITS` `RECORD_PARENT`: [OPS-RUST-RECEIPTS-AND-LIMITS](OPS-RUST-RECEIPTS-AND-LIMITS.md) (CONDITIONAL)
