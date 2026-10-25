# MUB-PRIME-POWER-CONSTRUCTION

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN. In dimension 2, the three bases Z = ((1, 0), (0, 1)), X = ((1, 1), (1, -1)) and Y = ((1, i), (1, -i)) are mutually unbiased over the Gaussian integers. Their squared norms are 1, 1, 2, 2, 2 and 2. Vectors inside one basis have inner product 0. For every vector from one basis and every vector from another, twice the squared modulus of the inner product equals the product of the squared norms. The square of i is -1. The additive character of the two-element field sends 0 to 1 and 1 to -1, and it sends 1+1 to 1.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This is the dimension-2 characteristic-two family only. It does not construct a complete family for any larger prime power, does not treat odd characteristic, does not run a general character sum, and does not infer a dimension-six family from this carrier.

## Source status

Dimension-2 Gaussian-integer bases Z, X and Y; the two-element character sends 1+1 to 1. Larger prime powers stay open.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignMubPrimePowerConstruction.lean`

- file: [lean4/CampaignMubPrimePowerConstruction.lean](../../../lean4/CampaignMubPrimePowerConstruction.lean)
- sha256 (`bytes`): `1a982efc2d477c63d2d51f591116c99c948d1f40af2ce2caa385ea5524716bef`
- cited in: node.lean, receipt dag/research/campaign_mub-prime-power-construction_lean_replay.json (CampaignMubPrimePowerConstruction), record TFQ-0403
- replay: `verified`
  - receipt [dag/research/campaign_mub-prime-power-construction_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction_lean_replay.json) (module `CampaignMubPrimePowerConstruction`): recorded sha256 `1a982efc2d477c63d2d51f591116c99c948d1f40af2ce2caa385ea5524716bef` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignMubPrimePowerConstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `basis_orthogonal` | yes | yes | yes | none | `#print axioms basis_orthogonal` |
| `char_of_double` | yes | yes | yes | none | `#print axioms char_of_double` |
| `char_values` | yes | yes | yes | none | `#print axioms char_values` |
| `cross_unbiased` | yes | yes | yes | none | `#print axioms cross_unbiased` |
| `i_squared` | yes | yes | yes | none | `#print axioms i_squared` |
| `self_inner` | yes | yes | yes | none | `#print axioms self_inner` |
| `squared_norms` | yes | yes | yes | none | `#print axioms squared_norms` |
- counts toward the grade: yes

### Python: `checks/independent/mub-prime-power-construction.py`

- file: [checks/independent/mub-prime-power-construction.py](../../../checks/independent/mub-prime-power-construction.py)
- sha256 (`bytes`): `bd381422744d65b117272aa3b35091b72028741249e15953a163510af796e1bd`
- cited in: record TFQ-0403
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_0403_mub_prime_power_construction.md`

- file: [dag/derivations/25_mub/tfq_0403_mub_prime_power_construction.md](../../../dag/derivations/25_mub/tfq_0403_mub_prime_power_construction.md)
- sha256 (`lf-normalised`): `35808b69007abc4faa0461ae3dd99cfdcb4b2f7dd48b61f3ab3e2aaad5682db1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0403
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/mub-prime-power-construction.md`

- file: [dag/derivations/independent/mub-prime-power-construction.md](../../../dag/derivations/independent/mub-prime-power-construction.md)
- sha256 (`lf-normalised`): `0c9855bc99257664b006985635ef7e6b4b97cc8e25c98a06e78155b140d7451e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_mub-prime-power-construction_lean_replay.json`

- file: [dag/research/campaign_mub-prime-power-construction_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction_lean_replay.json)
- sha256 (`lf-normalised`): `1e01a8f877033ba42ab05b23f34d18cf5ce14781497b6c34739f4e9f990ce124`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/README.md`

- file: [papers/core/mub6/README.md](../../../papers/core/mub6/README.md)
- sha256 (`lf-normalised`): `df09e721db359b5d96928ae66ee18f6f67d8e805182e6ae7dd76d156496198f9`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB-PRIME-POWER-CONSTRUCTION` `GAP_NO_DERIVATION`: [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)

Outgoing (1):

- `APP-R-MUB6-NO-FIELD-OF-ORDER-SIX` `CONDITIONAL_ON_IMPORT`: [MUB6-NO-FIELD-OF-ORDER-SIX](MUB6-NO-FIELD-OF-ORDER-SIX.md) (IMPORTED_ASSUMPTION)
