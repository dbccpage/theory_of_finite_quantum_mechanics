# OPS-PUSHFORWARD-FUNCTOR-LEAN

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In Lean (LggrFiniteResults), a finitely supported measure with natural-number weights is a list of (value, weight) pairs, and pushforward along f maps each value by f and keeps its weight. Then: push of the identity is the identity (push_id); push along g after f equals push along the composite (push_comp); total mass is unchanged (mass_push); and the weight at b of push f p equals the mass of the entries of p whose image is b (weightAt_push). The note reads marginalisation of a context distribution as such a pushforward along the restriction map, so these are the identity and composition laws of the functor from the opposite of the context poset to probability vectors (Lemma B2). That reading is not a Lean statement. Not covered: rational weights, normalisation to probability vectors, the context poset, and the Rust types. The ledger row states the same narrowing.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The Lean statement is the narrowed one above. The functor over rational probability vectors is proved in prose in the note (Lemma B2) and its instances on the PR box and the noisy PR boxes are recomputed by the independent check, which does not test the Lean statement. Independently replayed with Lean 4.35.0; the source-bound axiom receipt is dag/research/foc035_observer_presheaf_lean_replay.json.

## Source status

Ledger row L035-B1: proved + computed + Lean-checked for pushforward of finitely supported natural-number-weighted measures only. The Lean module is on main; this change did not rebuild it. The ledger records elaboration under Lean 4.34.0 with axioms propext and Quot.sound only, and this repository pins Lean 4.35.0.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/LggrFiniteResults.lean`

- file: [lean4/LggrFiniteResults.lean](../../../lean4/LggrFiniteResults.lean)
- sha256 (`bytes`): `ce736b577beb07997dba02bd7f86f83f1ecac7ce7a569e72b6350171179f34de`
- cited in: node.lean, node.source, receipt dag/research/foc035_observer_presheaf_lean_replay.json (LggrFiniteResults), record TFQ-2501
- replay: `verified`
  - receipt [dag/research/foc035_observer_presheaf_lean_replay.json](../../../dag/research/foc035_observer_presheaf_lean_replay.json) (module `LggrFiniteResults`): recorded sha256 `ce736b577beb07997dba02bd7f86f83f1ecac7ce7a569e72b6350171179f34de` matches the current file; exit code 0; Lean Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/foc035_observer_presheaf_lean_replay.json](../../../dag/research/foc035_observer_presheaf_lean_replay.json) (module `LggrFiniteResults`): recorded sha256 `ce736b577beb07997dba02bd7f86f83f1ecac7ce7a569e72b6350171179f34de` matches the current file; exit code 0; Lean Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `LggrFiniteResults`): recorded sha256 `ce736b577beb07997dba02bd7f86f83f1ecac7ce7a569e72b6350171179f34de` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build LggrFiniteResults`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `LggrFiniteResults.mass_push` | yes | yes | yes | propext | `#print axioms LggrFiniteResults.mass_push` |
| `LggrFiniteResults.push_comp` | yes | yes | yes | Quot.sound, propext | `#print axioms LggrFiniteResults.push_comp` |
| `LggrFiniteResults.push_id` | yes | yes | yes | Quot.sound, propext | `#print axioms LggrFiniteResults.push_id` |
| `LggrFiniteResults.weightAt_push` | yes | yes | yes | propext | `#print axioms LggrFiniteResults.weightAt_push` |

- counts toward the grade: yes

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2501_ops_pushforward_functor_lean.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2501_ops_pushforward_functor_lean.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2501_ops_pushforward_functor_lean.md)
- sha256 (`lf-normalised`): `fe59c997f1d27e7209c17741fddf163a4d89378b14d479f135cc5905d2ac7ffd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2501
- counts toward the grade: no

### Documents and data: `dag/research/foc035_observer_presheaf_lean_replay.json`

- file: [dag/research/foc035_observer_presheaf_lean_replay.json](../../../dag/research/foc035_observer_presheaf_lean_replay.json)
- sha256 (`lf-normalised`): `5810e04e569b5ed7611d007c1497d7d4ee0dac3acec079a3509e4f1d2ad8944d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `ae5564735bb6591e0f149868f83bd9f9793f297be0f8af3cc889c293ae4059cb`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-PUSHFORWARD-FUNCTOR-LEAN` `DERIVED_LEAN`: [IMPL-LGGR-FINITE-RESULTS-LEAN](IMPL-LGGR-FINITE-RESULTS-LEAN.md) (PROVED_LEAN)

Outgoing (1):

- `OPS-R-CECH-COBOUNDARY` `DERIVED_PROSE`: [OPS-CECH-COBOUNDARY](OPS-CECH-COBOUNDARY.md) (PROVED_PROSE)
