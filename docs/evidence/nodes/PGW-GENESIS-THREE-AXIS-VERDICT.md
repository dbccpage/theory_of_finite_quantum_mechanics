# PGW-GENESIS-THREE-AXIS-VERDICT

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The final source closeout records three independent axes after the author's 2026-09-28 freeze of snapshot 90ab34a0: research_phase CLOSED_WITH_OPEN_OBSTRUCTIONS, alpha_reference READY_WITHIN_DECLARED_SCOPE and original_seed_completion_gate UNSATISFIED, the last with its live-injection and comparison clauses unmet and the input-count floor NOT_ESTABLISHED. A source defect stays on the record: delta_events names a fresh datum w\<n\> from the current datum count, so when the sole admitted token is w1 a NewDatum item emits AdmitDatum(w1) and deduplication leaves the state unchanged; the standalone replay reproduces this. Pinned Lean modules use only propext and Quot.sound, companion results such as the carrier-general image factorization also use Classical.choice, and the compiled census reports 2,475 non-internal theorem constants. Native Rust and frozen Python agree on every context observation and portable key over 1,436 regimes, and the compiled Lean wire encoder agrees with Python on 1,439 tuples.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 4 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

The axis values are recorded author-approved verdicts, not computed results: a closed stage does not imply readiness, companion work does not rewrite the frozen gate, and finite agreement is not a compiler-verified refinement proof for all source code.

## Source status

closeout.txt section 10 recorded verdicts; paper.md section 12 defect and agreement counts (ledger WDP-P000-023, -024)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/bin/genesis_replay.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/bin/genesis_replay.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/bin/genesis_replay.rs)
- sha256 (`bytes`): `eecf7e7e8ae1b7b395e5fda1afc81fcda8c72742af478b483c7a1cb931047990`
- cited in: node.rust, record TFQ-0461

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `run` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- sha256 (`bytes`): `856ce42faba2dc2ae1217207ecc8af893eac29b50ae8a374dc06d2ba22c957bb`
- cited in: record TFQ-0461

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `delta_events` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py)
- sha256 (`bytes`): `60d4be592f4528fa5f40f3fa03179c84225daf914c79660f62cbd016fb649c71`
- cited in: record TFQ-0461

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `compare_rust` (python_symbol) | yes | yes | yes | - | - |
| `python_replay` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt)
- sha256 (`lf-normalised`): `c613e357809438876d1fcec34ea896548f17f4e9d4ea7f21048fafe9451651ac`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/paper.md](../../../atlas/papers/finite_obstruction_calculus/genesis/paper.md)
- sha256 (`lf-normalised`): `0dde974e14ff1b54ff6e65705a1194aea38fad7e65bf77b159a07ea1b96bb9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0461_genesis_three_axis_verdict.md`

- file: [dag/derivations/02_genesis/tfq_0461_genesis_three_axis_verdict.md](../../../dag/derivations/02_genesis/tfq_0461_genesis_three_axis_verdict.md)
- sha256 (`lf-normalised`): `240f23382909bba34db2e96fe0708a703aaabb0f954dbabfd642974a892b0c68`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0461
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0461 lean4: no Lean statement of the verdicts or of the fresh-label defect; the axiom census is the compiled lean4/axiom_report.txt

## Routes

Incoming (1):

- `PGW-R-GENESIS-THREE-AXIS-VERDICT` `COMPUTED`: [PGW-SEALED-TERMINAL-STATEMENT](PGW-SEALED-TERMINAL-STATEMENT.md) (PROVED_PROSE)

Outgoing (2):

- `PGW-R-GENESIS-FREEZE-ENDPOINT-LEDGER` `DERIVED_PROSE`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)
- `PGW-R-RUNG0-INHERITANCE-REPLAY` `COMPUTED`: [PGW-RUNG0-INHERITANCE-REPLAY](PGW-RUNG0-INHERITANCE-REPLAY.md) (COMPUTATIONALLY_CHECKED)
