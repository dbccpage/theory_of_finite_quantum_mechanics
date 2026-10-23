# OPS-PUSHFORWARD-FUNCTOR-LEAN

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In Lean (LggrFiniteResults), a finitely supported measure with natural-number weights is a list of (value, weight) pairs, and pushforward along f maps each value by f and keeps its weight. Then: push of the identity is the identity (push_id); push along g after f equals push along the composite (push_comp); total mass is unchanged (mass_push); and the weight at b of push f p equals the mass of the entries of p whose image is b (weightAt_push). The note reads marginalisation of a context distribution as such a pushforward along the restriction map, so these are the identity and composition laws of the functor from the opposite of the context poset to probability vectors (Lemma B2). That reading is not a Lean statement. Not covered: rational weights, normalisation to probability vectors, the context poset, and the Rust types. The ledger row states the same narrowing.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The Lean statement is the narrowed one above. The functor over rational probability vectors is proved in prose in the note (Lemma B2) and its instances on the PR box and the noisy PR boxes are recomputed by the independent check, which does not test the Lean statement. Lean not rebuilt in this change.

## Source status

Ledger row L035-B1: proved + computed + Lean-checked for pushforward of finitely supported natural-number-weighted measures only. The Lean module is on main; this change did not rebuild it. The ledger records elaboration under Lean 4.34.0 with axioms propext and Quot.sound only, and this repository pins Lean 4.35.0.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/LggrFiniteResults.lean`

- file: [lean4/LggrFiniteResults.lean](../../../lean4/LggrFiniteResults.lean)
- sha256 (`bytes`): `ce736b577beb07997dba02bd7f86f83f1ecac7ce7a569e72b6350171179f34de`
- cited in: node.lean, node.source, record TFQ-2501
- replay: `none`
- check: `cd lean4 && lake build LggrFiniteResults`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `LggrFiniteResults.mass_push` | yes | yes | yes | - | `#print axioms LggrFiniteResults.mass_push` |
| `LggrFiniteResults.push_comp` | yes | yes | yes | - | `#print axioms LggrFiniteResults.push_comp` |
| `LggrFiniteResults.push_id` | yes | yes | yes | - | `#print axioms LggrFiniteResults.push_id` |
| `LggrFiniteResults.weightAt_push` | yes | yes | yes | - | `#print axioms LggrFiniteResults.weightAt_push` |
- counts toward the grade: yes

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `6c1962e9a7e6b987ed5ba1b47afca56f17065d81fbfd2522245711b3840967ef`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2501_ops_pushforward_functor_lean.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2501_ops_pushforward_functor_lean.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2501_ops_pushforward_functor_lean.md)
- sha256 (`lf-normalised`): `d1d26ae5e1c84dc1441e44406b586e7a4e033232a3427baf653882d5fcebe1c4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2501
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `649532625cf9e8ec085a420fd1bad9227fcc4dae9f06ba02be1eb19f497e3ec7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-PUSHFORWARD-FUNCTOR-LEAN` `DERIVED_LEAN`: [IMPL-LGGR-FINITE-RESULTS-LEAN](IMPL-LGGR-FINITE-RESULTS-LEAN.md) (PROVED_LEAN)

Outgoing (1):

- `OPS-R-CECH-COBOUNDARY` `DERIVED_PROSE`: [OPS-CECH-COBOUNDARY](OPS-CECH-COBOUNDARY.md) (PROVED_PROSE)
