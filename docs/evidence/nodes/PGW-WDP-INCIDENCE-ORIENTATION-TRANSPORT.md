# PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> GenesisIncidence.lean reads the declared incidence complex on vertices 0, 1, 2 with signed boundary maps on the edge basis (01, 02, 12), the admitted face 012 entering as the column (1, −1, 1), and establishes that the boundary of that face has zero boundary (boundary_boundary_filled). The WDP window instead uses coboundaries with the simplicial edge order (01, 12, 02), d₀f = (f₁ − f₀, f₂ − f₁, f₂ − f₀) and d₁x = x₀₁ + x₁₂ − x₀₂ (Obstruction.lean), while the cyclic presentation (01, 12, 20) negates the reversed component. The monograph states that every window quantity is invariant once the cochain is transported with its edges, but no declared map takes the GenesisIncidence chains, with their edge order and boundary convention, to the WDP cochain window.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- distinct cited Lean declarations covered by a current replay receipt: 14
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open. One triangle is transported. The reorder, the transpose identity, the sign for edge 20, the charge 2, and the residual lower bound 2 are checked. A transport for every window quantity, a derivation of the WDP window from Genesis admission, and the external orientation test stay open.

## Source status

006_oewdp lean4/GenesisIncidence.lean (boundary order 01,02,12) vs WDP monograph §4.7 orientation convention; transport owed

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/OeWdp/GenesisIncidence.lean`

- file: [lean4/Imported/OeWdp/GenesisIncidence.lean](../../../lean4/Imported/OeWdp/GenesisIncidence.lean)
- sha256 (`bytes`): `ea27798ed2765ce05c4ee2b822efd380aaf2948486db66fdc0d42b2ad63797c9`
- cited in: node.lean, node.source, record TFQ-0543
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.OeWdp.GenesisIncidence`): recorded sha256 `ea27798ed2765ce05c4ee2b822efd380aaf2948486db66fdc0d42b2ad63797c9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OeWdp/GenesisIncidence.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `boundary_boundary_filled` | yes | yes | yes | module-level | `#print axioms boundary_boundary_filled` |

- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a`
- cited in: node.lean, node.source, record TFQ-0543
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `triD1` | yes | yes | yes | module-level | `#print axioms triD1` |

- counts toward the grade: yes

### Lean: `lean4/PregenesisWdpIncidenceTransport.lean`

- file: [lean4/PregenesisWdpIncidenceTransport.lean](../../../lean4/PregenesisWdpIncidenceTransport.lean)
- sha256 (`bytes`): `d1671fb7df23ee9b65b0032c9bab2f4875067f141e045a8da64e107ffea5fbcf`
- cited in: node.lean, receipt dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json (PregenesisWdpIncidenceTransport), receipt dag/research/pr_356_review_replay.json (PregenesisWdpIncidenceTransport), record TFQ-0543
- replay: `verified`
  - receipt [dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json](../../../dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json) (module `PregenesisWdpIncidenceTransport`): recorded sha256 `d1671fb7df23ee9b65b0032c9bab2f4875067f141e045a8da64e107ffea5fbcf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_356_review_replay.json](../../../dag/research/pr_356_review_replay.json) (module `PregenesisWdpIncidenceTransport`): recorded sha256 `d1671fb7df23ee9b65b0032c9bab2f4875067f141e045a8da64e107ffea5fbcf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build PregenesisWdpIncidenceTransport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `column_01` | yes | yes | yes | none | `#print axioms column_01` |
| `column_02` | yes | yes | yes | none | `#print axioms column_02` |
| `column_12` | yes | yes | yes | none | `#print axioms column_12` |
| `defect_charge` | yes | yes | yes | none | `#print axioms defect_charge` |
| `face_reorders` | yes | yes | yes | none | `#print axioms face_reorders` |
| `incidence_face_boundary_zero` | yes | yes | yes | none | `#print axioms incidence_face_boundary_zero` |
| `pairing_is_two` | yes | yes | yes | Quot.sound, propext | `#print axioms pairing_is_two` |
| `residual_at_least_two` | yes | yes | yes | Quot.sound, propext | `#print axioms residual_at_least_two` |
| `residual_at_repair` | yes | yes | yes | none | `#print axioms residual_at_repair` |
| `reverse_edge_20` | yes | yes | yes | Quot.sound, propext | `#print axioms reverse_edge_20` |
| `transport_matches_transpose` | yes | yes | yes | Quot.sound, propext | `#print axioms transport_matches_transpose` |
| `wdp_d1_d0` | yes | yes | yes | Quot.sound, propext | `#print axioms wdp_d1_d0` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py)
- sha256 (`bytes`): `5a88f14b6c7d3118868d35e112487ee944ca200ee690736a22a867f2c461ca9b`
- cited in: record TFQ-0543
- check: `python -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py::test_reversed_edge_orientation_changes_signs_not_the_signature`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_reversed_edge_orientation_changes_signs_not_the_signature` (python_test) | yes | yes | yes | - | `python -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py::test_reversed_edge_orientation_changes_signs_not_the_signature` |

- counts toward the grade: yes

### Python: `checks/independent/pgw-wdp-incidence-orientation-transport.py`

- file: [checks/independent/pgw-wdp-incidence-orientation-transport.py](../../../checks/independent/pgw-wdp-incidence-orientation-transport.py)
- sha256 (`bytes`): `c81e863a43fef5d200c457254fbcb535020cc36593508a46eed4d25e732d33ba`
- cited in: record TFQ-0543

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0543_wdp_incidence_orientation_transport.md`

- file: [dag/derivations/06_wdp/tfq_0543_wdp_incidence_orientation_transport.md](../../../dag/derivations/06_wdp/tfq_0543_wdp_incidence_orientation_transport.md)
- sha256 (`lf-normalised`): `11345ce2abe36b28dd6bfcb43963d2a2d509b72855510d024262449c0b91edb4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0543
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-wdp-incidence-orientation-transport.md`

- file: [dag/derivations/independent/pgw-wdp-incidence-orientation-transport.md](../../../dag/derivations/independent/pgw-wdp-incidence-orientation-transport.md)
- sha256 (`lf-normalised`): `fb59c34f1836445abfa9d6b10d7ca947d9cbf34c91689ab59c0beec6a29804f4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json`

- file: [dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json](../../../dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json)
- sha256 (`lf-normalised`): `54eeb8427dab32c55b302aa0307ab1fbf2de9bf45e6fbc1c437fc209ad0153a0`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0543 rust: no Rust transport between the GenesisIncidence boundary convention and the WDP coboundary window

## Routes

Incoming (1):

- `PGW-R-WDP-INCIDENCE-ORIENTATION-TRANSPORT` `GAP_NO_DERIVATION`: [PGW-WDP-GRAPH-COCHAIN-HOST](PGW-WDP-GRAPH-COCHAIN-HOST.md) (DEFINITION), [PGW-INCIDENCE-CONSTRUCTION-BETTI](PGW-INCIDENCE-CONSTRUCTION-BETTI.md) (PROVED_LEAN)

Outgoing (0):

