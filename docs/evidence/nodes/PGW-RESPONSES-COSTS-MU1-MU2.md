# PGW-RESPONSES-COSTS-MU1-MU2

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A response (delta) is an ordered finite list of NewDatum, NewForm(arity), NewInst(form, args) and NewRuleAll(form) items applied in order; an instance may name a form added earlier in the same list, and the reverse order is an ill-formed admission. The declared costs are mu1 = item count and mu2 = (item count, sum of new-form arities) compared lexicographically, where the sum counts every NewForm item, including distinct forms of equal arity. A valid response to Separate(i, j) applies, separates the target, and keeps every previously imposed requirement separated, because requirements are persistent constraints.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared item grammar and cost measures mu1 and mu2, genesis_source.txt sections 3.6-3.7 (assumption)

## Bottleneck

Both measures and the item grammar are declared, not derived; bundling a form and an instance into one primitive would change every cost, and the enumerator's canonical item order makes a delta a multiset only up to that convention.

## Source status

genesis_source.txt sections 3.6-3.7 and paper.md section 7 \[definition\]; Basic.lean, Minimality.lean aritySum

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Basic.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Basic.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Basic.lean)
- sha256 (`bytes`): `151fa22bcd2d75b01ec4d924ea3f94cb4b1c020c2a9254471ff013eb43aabcc7`
- cited in: node.lean, record TFQ-0438
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Basic`): recorded sha256 `151fa22bcd2d75b01ec4d924ea3f94cb4b1c020c2a9254471ff013eb43aabcc7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Basic.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `applyDelta` | yes | yes | yes | propext | `#print axioms applyDelta` |
| `validResponse` | yes | yes | yes | propext | `#print axioms validResponse` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)
- sha256 (`bytes`): `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925`
- cited in: node.lean, record TFQ-0438
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Minimality`): recorded sha256 `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `aritySum` | yes | yes | yes | propext | `#print axioms aritySum` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/measure.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/measure.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/measure.rs)
- sha256 (`bytes`): `cf9d862e8d00e3ad228ac247728a8a58c306b479f47fbd533ebefc7ef0b3e644`
- cited in: node.rust, record TFQ-0438

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `arity_sum` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/response.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/response.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/response.rs)
- sha256 (`bytes`): `c8f7f65f7eb58c918020716fc34ef462d7799fc9546efba688c4ef8e2978bd20`
- cited in: node.rust, record TFQ-0438

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `response_valid_naive` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- sha256 (`bytes`): `856ce42faba2dc2ae1217207ecc8af893eac29b50ae8a374dc06d2ba22c957bb`
- cited in: record TFQ-0438

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mu1` (python_symbol) | yes | yes | yes | - | - |
| `mu2` (python_symbol) | yes | yes | yes | - | - |
| `response_valid_naive` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/paper.md](../../../atlas/papers/finite_obstruction_calculus/genesis/paper.md)
- sha256 (`lf-normalised`): `0dde974e14ff1b54ff6e65705a1194aea38fad7e65bf77b159a07ea1b96bb9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0438_responses_costs_mu1_mu2.md`

- file: [dag/derivations/02_genesis/tfq_0438_responses_costs_mu1_mu2.md](../../../dag/derivations/02_genesis/tfq_0438_responses_costs_mu1_mu2.md)
- sha256 (`lf-normalised`): `f9c2b2c74c67cade23e6f109762884598a31eb8d6cecc62f8de25c032d897fbf`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0438
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-RESPONSES-COSTS-MU1-MU2` `DERIVED_PROSE`: [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)

Outgoing (2):

- `PGW-R-CHALLENGE3-CURRENT-REGIME-FAILS` `DERIVED_LEAN`: [PGW-CHALLENGE3-CURRENT-REGIME-FAILS](PGW-CHALLENGE3-CURRENT-REGIME-FAILS.md) (PROVED_LEAN)
- `PGW-R-RESPONSE-EXISTENCE-MARK-PROGRESS` `DERIVED_LEAN`: [PGW-RESPONSE-EXISTENCE-MARK-PROGRESS](PGW-RESPONSE-EXISTENCE-MARK-PROGRESS.md) (PROVED_LEAN)
