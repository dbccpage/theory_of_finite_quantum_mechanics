# CQFT-FINITE-POSET-NET-TARGET

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement, checked in Lean 4 for site-factorized operators. For a FiniteStrictPoset P on n points put one qubit (a single-site monoid M) at each point; an operator A : Fin n -\> M is localized in a subset O of P when it is the identity outside O, so the Lean "algebra" of O is the set of elementary tensor operators localized in O, not the full matrix algebra on the qubits in O. (a) Isotony: O1 inside O2 and A localized in O1 imply A localized in O2. (b) Locality: if every point of O1 is spacelike to every point of O2, then O1 and O2 are disjoint and operators localized in O1 and in O2 commute under the sitewise product. (c) The spacelike relation of CausalOrder.lean is symmetric (spacelike_symm) and irreflexive (spacelike_irrefl) and not transitive: on the four-element N poset 0\<2, 1\<2, 1\<3, points 1 and 0 are spacelike, 0 and 3 are spacelike, and 1\<3 are related. The content of Haag-Kastler locality (commutation forced by causal separation of dynamics) is absent because this net has no dynamics.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not proved in Lean: the statements for the full local matrix algebras A(O) (linear spans of elementary tensors, for example 2^|O| x 2^|O| matrices): that commutation of elementary tensors extends by bilinearity to the algebras and that A(O1) is a subalgebra of A(O2) as matrix algebras; the single-site monoid M is generic and is not instantiated at 2x2 matrices. The net is kinematical: dynamics, a time-slice property and covariance are not modelled, so the statement is the finite shadow of two axioms and nothing more.

## Source status

Verified against lean4/CausalOrder.lean on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierPosetNet (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `isotony`, `disjoint_of_all_spacelike`, `locality_commute_of_spacelike`, `spacelike_not_transitive_on_posetN`, with `CausalOrder.spacelike_symm` and `spacelike_irrefl`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CausalOrder.lean`

- file: [lean4/CausalOrder.lean](../../../lean4/CausalOrder.lean)
- sha256 (`bytes`): `f8f04b749262b26eeae39f3fc0d96b55e3fd02283f7df29a1c2042faf017edf0`
- cited in: node.lean, node.source, record TFQ-2104
- replay: `none`
- check: `cd lean4 && lake build CausalOrder`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `spacelike_irrefl` | yes | yes | yes | - | `#print axioms spacelike_irrefl` |
| `spacelike_symm` | yes | yes | yes | - | `#print axioms spacelike_symm` |
- counts toward the grade: yes

### Lean: `lean4/FrontierPosetNet.lean`

- file: [lean4/FrontierPosetNet.lean](../../../lean4/FrontierPosetNet.lean)
- sha256 (`bytes`): `85e14da33699f6d5fbf4735dca457545e04f0de0f6209e3301b77f695919fb6d`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierPosetNet)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierPosetNet`): recorded sha256 `85e14da33699f6d5fbf4735dca457545e04f0de0f6209e3301b77f695919fb6d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierPosetNet`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierPosetNet.disjoint_of_all_spacelike` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierPosetNet.disjoint_of_all_spacelike` |
| `FrontierPosetNet.isotony` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierPosetNet.isotony` |
| `FrontierPosetNet.locality_commute_of_spacelike` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierPosetNet.locality_commute_of_spacelike` |
| `FrontierPosetNet.posetN_causal_1_3` | yes | yes | yes | none | `#print axioms FrontierPosetNet.posetN_causal_1_3` |
| `FrontierPosetNet.posetN_spacelike_0_1` | yes | yes | yes | none | `#print axioms FrontierPosetNet.posetN_spacelike_0_1` |
| `FrontierPosetNet.posetN_spacelike_0_3` | yes | yes | yes | none | `#print axioms FrontierPosetNet.posetN_spacelike_0_3` |
| `FrontierPosetNet.spacelike_not_transitive_on_posetN` | yes | yes | yes | none | `#print axioms FrontierPosetNet.spacelike_not_transitive_on_posetN` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/31_causal_qft/tfq_2104_cqft_finite_poset_net_target.md`

- file: [dag/derivations/31_causal_qft/tfq_2104_cqft_finite_poset_net_target.md](../../../dag/derivations/31_causal_qft/tfq_2104_cqft_finite_poset_net_target.md)
- sha256 (`lf-normalised`): `dff53ba6787a3957f04ab42f0c2c2079eb814b1851f20bda64a65db14d8d8324`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2104
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `1c66aabd3bb726fafcd0238c259644d6f79dd304178d171a75ea36d6522bd2cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-CQFT-FINITE-POSET-NET-TARGET` `DERIVED_LEAN`: [CQFT-FINITE-STRICT-POSET-SPACELIKE](CQFT-FINITE-STRICT-POSET-SPACELIKE.md) (PROVED_LEAN), [CQFT-LOCAL-NET-AXIOMS-IMPORT](CQFT-LOCAL-NET-AXIOMS-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

