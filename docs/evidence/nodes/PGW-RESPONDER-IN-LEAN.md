# PGW-RESPONDER-IN-LEAN

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The sealed responder, a minimum of the sealed candidate space of at most two items and arity at most two under mu1 or mu2, has no Lean counterpart in the second derivation's packages: no Lean statement about a minimum, cost or tie (S-3); the responder's domain excludes ruled regimes, since it refuses to run on a regime holding a uniform rule (S-1); the other demand kind, a same pair that is separable, is not read (S-2); and the distance bound of two is not known to be the grammar's (S-4). Attempt one's G-4 asks for the same responder in Lean, and attempt two's H-1 (the four streamless carriers past the bounds) needs it.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open; the sealed Challenge-3 minimum and tie claims (CL-3-MIN-TWO, CL-3-TIE-CLASSES) concern the Challenge-3 readings and do not supply the second derivation's responder.

## Source status

continuation.txt §13 Responses in Lean (S-1 to S-4) and attempt one's leftovers (G-4)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs)
- sha256 (`bytes`): `1ce7119c17f0bac2b7f0a81487da586024d0d4e38a5004197e9765ebe96def98`
- cited in: node.rust, record TFQ-0496

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `min_responses` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- sha256 (`bytes`): `856ce42faba2dc2ae1217207ecc8af893eac29b50ae8a374dc06d2ba22c957bb`
- cited in: record TFQ-0496

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `min_responses` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0496_responder_in_lean.md`

- file: [dag/derivations/02_genesis/tfq_0496_responder_in_lean.md](../../../dag/derivations/02_genesis/tfq_0496_responder_in_lean.md)
- sha256 (`lf-normalised`): `08a0f563a0022c44c25750ec6cb8d4139739acc4e3c261c85a1290aeb69e8f2e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0496
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0496 lean4: no Lean statement of the responder's minimum, cost or tie (S-3)

## Routes

Incoming (1):

- `PGW-R-RESPONDER-IN-LEAN` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION), [PGW-K-ITEM-DELTA-GRAMMAR](PGW-K-ITEM-DELTA-GRAMMAR.md) (OPEN)

Outgoing (0):

