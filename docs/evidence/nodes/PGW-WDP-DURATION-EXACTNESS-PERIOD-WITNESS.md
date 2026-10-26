# PGW-WDP-DURATION-EXACTNESS-PERIOD-WITNESS

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH07-D01: a finite duration gauge is a path system with an additive edge valuation λ: E → M into a commutative monoid, D_λ(p) = Σ_j λ(e_j); positivity, Archimedean structure, units and real values are extra hypotheses, and WDP-CH07-P01 gives D_λ(pq) = D_λ(p) + D_λ(q) whenever pq is defined. Section 7.2 keeps four statuses apart: exact (a displayed t with d₀t = λ), closed nonexact (d₁λ = 0 for a declared d₁ while a period or dual certificate shows λ ∉ im d₀), active closure failure (d₁λ ≠ 0 on an exhibited 2-cell) and exactness undetermined. WDP-CH07-P02: if λ = d₀t, every directed path from a to b has duration t(b) − t(a). The converse needs more than weak connectedness: a base vertex reaching every vertex with path-independent sums, or vanishing periods under signed walks; the difference of two path sums with common endpoints is a period witness, and a nonzero period refutes exactness.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Commutative additive monoid of durations, and an abelian group where exactness is asked (assumption)

## Bottleneck

Duration is a declared magnitude, not physical or continuum time; the four-status classification carries no ledger row, Lean mechanizes P01 and P02 (duration_append, exact_duration_path_independent), and Python duration_sum fixes M = ℚ with strict positivity, narrower than D01.

## Source status

WDP monograph §7.1-§7.3 WDP-CH07-D01 definition, P01/P02 (Lean Succession.lean), four statuses

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Succession.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Succession.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Succession.lean)
- sha256 (`bytes`): `c3cbbc5fac35e5044364dd95ee2180c4e1c5c924a63777b42831a7f8f613a1e7`
- cited in: node.lean, record TFQ-0551
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Succession`): recorded sha256 `c3cbbc5fac35e5044364dd95ee2180c4e1c5c924a63777b42831a7f8f613a1e7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Succession.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `duration_append` | yes | yes | yes | propext | `#print axioms duration_append` |
| `exact_duration_path_independent` | yes | yes | yes | none | `#print axioms exact_duration_path_independent` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0551_wdp_duration_exactness_period_witness.md`

- file: [dag/derivations/06_wdp/tfq_0551_wdp_duration_exactness_period_witness.md](../../../dag/derivations/06_wdp/tfq_0551_wdp_duration_exactness_period_witness.md)
- sha256 (`lf-normalised`): `9568cf0c2a80207f071e435ec132108ef18e7da427b176e9669ae61e1262f480`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0551
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_06_finite_event_valuations.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_06_finite_event_valuations.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/cochains.py::solve_potential`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/duration.py::classify_duration`

## Absences recorded by the TFQ records

- TFQ-0551 rust: no omega_wdp Rust binding of the duration gauge or the four exactness statuses

## Routes

Incoming (1):

- `PGW-R-WDP-DURATION-EXACTNESS-PERIOD-WITNESS` `DERIVED_PROSE`: [PGW-WDP-SUCCESSION-STRICT-ORDER](PGW-WDP-SUCCESSION-STRICT-ORDER.md) (DEFINITION), [PG-WDP-DEGREE1-WINDOW](PG-WDP-DEGREE1-WINDOW.md) (DEFINITION)

Outgoing (1):

- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
