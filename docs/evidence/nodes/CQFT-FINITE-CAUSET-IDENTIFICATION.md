# CQFT-FINITE-CAUSET-IDENTIFICATION

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reading of definitions. A causal set in the sense of the source is a locally finite partially ordered set; in the strict-order form its relation is irreflexive and transitive, and local finiteness is automatic on a finite set. This is the structure FiniteStrictPoset n of lean4/CausalOrder.lean. The Python class CausalSet in code/python/src/general_relativity/causal_set.py builds a poset from relations, takes the transitive closure and refuses cycles. The identification involves no sprinkling, no embedding in a Lorentzian manifold and no dynamics.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Definitional only. Nothing about manifold-likeness, dimension or the continuum limit is asserted.

## Source status

Definition of this branch, audited against lean4/CausalOrder.lean, code/python/src/general_relativity/causal_set.py, arXiv:gr-qc/0309009 Section 3 p. 6 and arXiv:gr-qc/0207103 Section II p. 2 on 2026-10-22.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CausalOrder.lean`

- file: [lean4/CausalOrder.lean](../../../lean4/CausalOrder.lean)
- sha256 (`bytes`): `f8f04b749262b26eeae39f3fc0d96b55e3fd02283f7df29a1c2042faf017edf0`
- cited in: node.lean, node.source, record TFQ-2112
- replay: `none`
- check: `cd lean4 && lake build CausalOrder`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FiniteStrictPoset` | yes | yes | yes | - | `#print axioms FiniteStrictPoset` |
- counts toward the grade: yes

### Python: `code/python/src/general_relativity/causal_set.py`

- file: [code/python/src/general_relativity/causal_set.py](../../../code/python/src/general_relativity/causal_set.py)
- sha256 (`bytes`): `fe0391e534586e7ef4b5856b1c9f9fa190a19f55fdd368e36d85950ef1af92fb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/31_causal_qft/tfq_2112_cqft_finite_causet_identification.md`

- file: [dag/derivations/31_causal_qft/tfq_2112_cqft_finite_causet_identification.md](../../../dag/derivations/31_causal_qft/tfq_2112_cqft_finite_causet_identification.md)
- sha256 (`lf-normalised`): `6e3e6f8c5c3a48398e59577eded89f7884d6b4ab8ac1a49ccba5e492aa778b1e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2112
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:doi:10.1103/PhysRevLett.59.521`

## Routes

Incoming (1):

- `FRO-R-CQFT-FINITE-CAUSET-IDENTIFICATION` `DERIVED_PROSE`: [CQFT-BLMS-1987-SOURCE](CQFT-BLMS-1987-SOURCE.md) (SOURCE_RECORD), [CQFT-FINITE-STRICT-POSET-SPACELIKE](CQFT-FINITE-STRICT-POSET-SPACELIKE.md) (PROVED_LEAN)

Outgoing (1):

- `FRO-R-CQFT-MYRHEIM-MEYER-ORDERING-FRACTION-TARGET` `DERIVED_LEAN`: [CQFT-MYRHEIM-MEYER-ORDERING-FRACTION-TARGET](CQFT-MYRHEIM-MEYER-ORDERING-FRACTION-TARGET.md) (PROVED_LEAN)
