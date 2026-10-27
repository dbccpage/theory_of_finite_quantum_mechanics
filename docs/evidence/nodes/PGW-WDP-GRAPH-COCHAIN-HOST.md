# PGW-WDP-GRAPH-COCHAIN-HOST

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a finite oriented graph G = (V, E) with a normed coefficient space A, the host sets C⁰ = A^V, C¹ = A^E and (d₀f)(u, v) = f(v) − f(u); an edge field δ is exact when δ = d₀f. Q¹ = C¹/im d₀ records edge fields modulo vertex-potential repair, relative to the declared graph, coefficient space and repair map, and it is not the first cohomology group unless a next differential d₁ is supplied with d₁d₀ = 0. Worked cases: on the path 0 → 1 → 2, δ = (2, 3) = d₀(0, 2, 5) is exact; on the hollow cyclic triangle (01, 12, 20) every repair of δ = (1, 1, 1) still sums to 3, a quotient obstruction that is not contextuality without a measurement cover and an empirical model.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared finite oriented graph and normed coefficient space (assumption)

## Bottleneck

The graph, orientation and coefficients are declared inputs, not derived from Genesis admission (TFQ-0344); a repair-quotient class is not a cohomology class, and the host carries no measurement cover or empirical model.

## Source status

WDP monograph §4.1 graph-cochain host (definition)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `b5adb85d12297d203151348422a0400482d6cac0397e8fcc5381c9c8a54c9885`
- cited in: node.lean, record TFQ-0542
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `b5adb85d12297d203151348422a0400482d6cac0397e8fcc5381c9c8a54c9885` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Q1` | yes | yes | yes | none | `#print axioms Q1` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/cochains.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/cochains.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/cochains.py)
- sha256 (`bytes`): `56d2c214f55aa7fa2844792d5114656936295171cd38f4acf908df83cc9e2326`
- cited in: record TFQ-0542

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FiniteComplex` (python_symbol) | yes | yes | yes | - | - |
| `d0` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0542_wdp_graph_cochain_host.md`

- file: [dag/derivations/06_wdp/tfq_0542_wdp_graph_cochain_host.md](../../../dag/derivations/06_wdp/tfq_0542_wdp_graph_cochain_host.md)
- sha256 (`lf-normalised`): `35e1217b22b1f935fa2387254d494e139f0015adaf674c8f84e27005ed6440a1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0542
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:83da0237063adab6d54c81f7a608e1c44131ab10ba23aebfeb5378c19f25e4cd::FiniteComplex`
- `external:sha256:f444bcaa3ae162d185a3a8a21cf0b59606958107ac5510e84015090750d5c3cc:68-121`
- `external:upstream/external:sha256:83da0237063adab6d54c81f7a608e1c44131ab10ba23aebfeb5378c19f25e4cd::FiniteComplex`

## Routes

Incoming (1):

- `PGW-R-WDP-GRAPH-COCHAIN-HOST` `DERIVED_PROSE`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN)

Outgoing (3):

- `PGW-R-WDP-CLOSURE-NEEDS-DEGREE` `DERIVED_PROSE`: [PGW-WDP-CLOSURE-NEEDS-DEGREE](PGW-WDP-CLOSURE-NEEDS-DEGREE.md) (DEFINITION)
- `PGW-R-WDP-INCIDENCE-ORIENTATION-TRANSPORT` `GAP_NO_DERIVATION`: [PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT](PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT.md) (OPEN)
- `PGW-R-WDP-PHI-WELL-DEFINED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY](PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY.md) (CONDITIONAL)
