# PGW-WDP-RETENTION-PACKET

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A difference at one exhibition does not by itself remain available at another; a retention packet R = (M, u, r, ≈) with memory carrier M, update u: M × I → M, report r: M → O and declared recognition comparison ≈ is a definition, not a derivation. Five finite countermodels CM1–CM5 separate the components in their instances (a static carrier, a blind readout, a coarse report, a tolerant comparison, a lossy reset). WDP-CH03-O01, now a finite proposition: for a finite nonempty carrier with total labelled deterministic updates and exact readouts or a validated report equivalence, descending partition refinement computes the greatest report-respecting update congruence, its minimal quotient and behavioural classification without a global chronology. WDP-CH03-O02: typed retention extensions on fixed finite M, I, O form the product M^{I×M} × O^M × P(O×O), with quotient and literal-readout descent under separate conditions.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared finite carrier, total labelled deterministic update, report map and validated report comparison (assumption)

## Bottleneck

The O prefix on CH03-O01 and CH03-O02 is historical; Lean coverage is partial (BehavioralQuotient.lean gives the greatest invariant relation and quotient laws, not finite termination of refinement), and nothing here derives retention from a bare set or concerns physical memory.

## Source status

WDP monograph §3.3 and §3.6 retention packet; CH03-O01/O02 finite propositions with partial Lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/BehavioralQuotient.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/BehavioralQuotient.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/BehavioralQuotient.lean)
- sha256 (`bytes`): `a253353fd82047d9c632583c7fe39cd358b226806d9ef61e3de6de3335c812bf`
- cited in: node.lean, record TFQ-0541
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.BehavioralQuotient`): recorded sha256 `a253353fd82047d9c632583c7fe39cd358b226806d9ef61e3de6de3335c812bf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/BehavioralQuotient.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `greatest_invariant_relation` | yes | yes | yes | none | `#print axioms greatest_invariant_relation` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_wdp/src/retention.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/retention.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0541_wdp_retention_packet.md`

- file: [dag/derivations/06_wdp/tfq_0541_wdp_retention_packet.md](../../../dag/derivations/06_wdp/tfq_0541_wdp_retention_packet.md)
- sha256 (`lf-normalised`): `fd4d3b0e33ab4e27f45427573c3246e49cd59df2fcff12c1fd3036fba9413bf2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0541
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/retention.rs::compute_exact_behavioral_quotient`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/observer.py::RetentionPacket`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/retention_choices.py::greatest_forward_relation`

## Routes

Incoming (1):

- `PGW-R-WDP-RETENTION-PACKET` `DERIVED_PROSE`: [PGW-WDP-SEVEN-WITNESS-ROLES](PGW-WDP-SEVEN-WITNESS-ROLES.md) (DEFINITION)

Outgoing (2):

- `PGW-R-WDP-FINITE-VALUATIONS` `DERIVED_PROSE`: [PGW-WDP-FINITE-VALUATIONS](PGW-WDP-FINITE-VALUATIONS.md) (DEFINITION)
- `PGW-R-WDP-SUCCESSION-STRICT-ORDER` `DERIVED_PROSE`: [PGW-WDP-SUCCESSION-STRICT-ORDER](PGW-WDP-SUCCESSION-STRICT-ORDER.md) (DEFINITION)
