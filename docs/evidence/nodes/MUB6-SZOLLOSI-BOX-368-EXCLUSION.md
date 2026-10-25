# MUB6-SZOLLOSI-BOX-368-EXCLUSION

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The recorded native candidate box, restricting the six real entries of the first transition row to \[-1/2, 1/2\], contains no solution of the 666-equation system, because the balance equation forces coordinate 368 into \[7/2, 17/2\]; the box contains a point with admissible phases (1,-1,1,i).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This excludes one candidate box; it does not exclude all candidates at any family parameter, the six charts, the 56 family cells or the cusp collars.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C28 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/SzollosiGaugedReflection.lean`

- file: [lean4/SzollosiGaugedReflection.lean](../../../lean4/SzollosiGaugedReflection.lean)
- sha256 (`bytes`): `356eab2883d9d9494b06481f1ee41450a5f052a2bd157558657aca48da71c914`
- cited in: node.lean, record TFQ-1270
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiGaugedReflection`): recorded sha256 `356eab2883d9d9494b06481f1ee41450a5f052a2bd157558657aca48da71c914` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiGaugedReflection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `native_box_exclusion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms native_box_exclusion` |
| `native_box_has_admissible_phase_point` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms native_box_has_admissible_phase_point` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1270_mub6_szollosi_box_368_exclusion.md`

- file: [dag/derivations/25_mub/tfq_1270_mub6_szollosi_box_368_exclusion.md](../../../dag/derivations/25_mub/tfq_1270_mub6_szollosi_box_368_exclusion.md)
- sha256 (`lf-normalised`): `d894f95f0a587289360f2d2e5b1e16e59e62e9401bf443888c08087f6026c681`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1270
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

- `APP-R-MUB6-SZOLLOSI-BOX-368-EXCLUSION` `DERIVED_LEAN`: [MUB6-SZOLLOSI-GAUGED-666](MUB6-SZOLLOSI-GAUGED-666.md) (PROVED_LEAN)

Outgoing (0):

