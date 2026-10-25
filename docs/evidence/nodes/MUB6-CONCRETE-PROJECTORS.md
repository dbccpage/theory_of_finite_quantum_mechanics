# MUB6-CONCRETE-PROJECTORS

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> From a supplied finite complex MUB family, the matrices P_{b,l} = v_{b,l} v_{b,l}* are self-adjoint, sum to I within each basis, have trace one and rank one, and satisfy tr(P_{b,l} P_{c,k}) = 1/|iota| for distinct bases.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declaration references covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Forward construction only: it does not supply such a family in dimension six or extract one from moments.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C29 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ConcreteMubProjectors.lean`

- file: [lean4/ConcreteMubProjectors.lean](../../../lean4/ConcreteMubProjectors.lean)
- sha256 (`bytes`): `f592f57d1ca98cd39a4450be121b582e62f38f2dec9cb1782d67776a60ec6601`
- cited in: node.lean, record TFQ-1276
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `ConcreteMubProjectors`): recorded sha256 `f592f57d1ca98cd39a4450be121b582e62f38f2dec9cb1782d67776a60ec6601` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ConcreteMubProjectors`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `concreteProjector_complete` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms concreteProjector_complete` |
| `concreteProjector_cross_basis_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms concreteProjector_cross_basis_trace` |
| `concreteProjector_rank_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms concreteProjector_rank_one` |
| `concreteProjector_self_adjoint` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms concreteProjector_self_adjoint` |
| `concreteProjector_trace_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms concreteProjector_trace_one` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1276_mub6_concrete_projectors.md`

- file: [dag/derivations/25_mub/tfq_1276_mub6_concrete_projectors.md](../../../dag/derivations/25_mub/tfq_1276_mub6_concrete_projectors.md)
- sha256 (`lf-normalised`): `c9dc1a2be8e700a8cc46985019c2799ba0c21a3f62f98870a93ef9cc6c858228`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1276
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-CONCRETE-PROJECTORS` `DERIVED_LEAN`: [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)

Outgoing (1):

- `APP-R-MUB6-CONCRETE-MOMENT-FLATNESS` `DERIVED_LEAN`: [MUB6-CONCRETE-MOMENT-FLATNESS](MUB6-CONCRETE-MOMENT-FLATNESS.md) (PROVED_LEAN)
