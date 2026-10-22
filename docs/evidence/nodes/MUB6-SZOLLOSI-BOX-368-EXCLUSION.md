# MUB6-SZOLLOSI-BOX-368-EXCLUSION

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The recorded native candidate box, restricting the six real entries of the first transition row to \[-1/2, 1/2\], contains no solution of the 666-equation system, because the balance equation forces coordinate 368 into \[7/2, 17/2\]; the box contains a point with admissible phases (1,-1,1,i).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

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
- replay: `none`
- check: `cd lean4 && lake build SzollosiGaugedReflection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `native_box_exclusion` | yes | yes | yes | - | `#print axioms native_box_exclusion` |
| `native_box_has_admissible_phase_point` | yes | yes | yes | - | `#print axioms native_box_has_admissible_phase_point` |
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

