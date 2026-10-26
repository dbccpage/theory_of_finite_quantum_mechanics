# MUB-PRIME-POWER-CONSTRUCTION

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Construct and verify a complete d+1 MUB family for the stated prime-power carrier, explicitly handling finite-field arithmetic, character sums and normalization.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 17
- distinct cited Lean declarations covered by a current replay receipt: 17
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The characteristic-two family is dimension 2 only. For odd characteristic the construction is now general: for every finite field F with 2 ≠ 0, every commutative domain R with a star ring structure, and every nontrivial additive character ψ : F → R with star (ψ t) = ψ (−t), the q+1 bases indexed by Option F (the standard basis and x ↦ ψ(a x² + b x)) are pairwise orthogonal within a basis, have nonzero norms, and satisfy |⟨u, v⟩|² · q = ‖u‖² ‖v‖² across bases, with q+1 = card (Option F) (mub_family, card_bases). The vectors are left unnormalised, so normalisation is the statement about norms, not a division. What remains: a complete family for characteristic two beyond dimension 2 (which needs the Galois-ring or symplectic-spread construction, not quadratic phases), the instantiation of ψ over the concrete complex or cyclotomic carrier the node names (ψ is a parameter here), and the dimension-six question, which this node does not address.

## Source status

Dimension-2 Gaussian-integer bases Z, X and Y (characteristic two). For every odd prime power q a complete q+1 family of orthogonal, mutually unbiased vector families is constructed over any commutative domain with a star ring structure (bases of R^F when R is a field; spanning is not formalised), given a nontrivial unitary additive character of F_q as a parameter (lean4/CampaignMubPrimePowerOddCharacteristic.lean). Characteristic two beyond dimension 2, and the existence of the character over the concrete complex or cyclotomic carrier, stay open.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignMubPrimePowerConstruction.lean`

- file: [lean4/CampaignMubPrimePowerConstruction.lean](../../../lean4/CampaignMubPrimePowerConstruction.lean)
- sha256 (`bytes`): `9239bffb805755bc6a937dfcbd0d35e258ac7ffb356d5be09f172eda4b93fbec`
- cited in: node.lean, receipt dag/research/campaign_mub-prime-power-construction_lean_replay.json (CampaignMubPrimePowerConstruction), receipt dag/research/pr_359_review_replay.json (CampaignMubPrimePowerConstruction), record TFQ-0403
- replay: `verified`
  - receipt [dag/research/campaign_mub-prime-power-construction_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction_lean_replay.json) (module `CampaignMubPrimePowerConstruction`): recorded sha256 `9239bffb805755bc6a937dfcbd0d35e258ac7ffb356d5be09f172eda4b93fbec` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_359_review_replay.json](../../../dag/research/pr_359_review_replay.json) (module `CampaignMubPrimePowerConstruction`): recorded sha256 `9239bffb805755bc6a937dfcbd0d35e258ac7ffb356d5be09f172eda4b93fbec` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
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

### Lean: `lean4/CampaignMubPrimePowerOddCharacteristic.lean`

- file: [lean4/CampaignMubPrimePowerOddCharacteristic.lean](../../../lean4/CampaignMubPrimePowerOddCharacteristic.lean)
- sha256 (`bytes`): `a4a76bcdb4817fb2a7685940faaf4fb1d08b6fb51f0a87ec554d367796be1b5b`
- cited in: node.lean, receipt dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json (CampaignMubPrimePowerOddCharacteristic)
- replay: `verified`
  - receipt [dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json) (module `CampaignMubPrimePowerOddCharacteristic`): recorded sha256 `a4a76bcdb4817fb2a7685940faaf4fb1d08b6fb51f0a87ec554d367796be1b5b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignMubPrimePowerOddCharacteristic`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `MubFable.PrimePowerOdd.basis_orthogonal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubFable.PrimePowerOdd.basis_orthogonal` |
| `MubFable.PrimePowerOdd.basis_unbiased` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubFable.PrimePowerOdd.basis_unbiased` |
| `MubFable.PrimePowerOdd.card_bases` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubFable.PrimePowerOdd.card_bases` |
| `MubFable.PrimePowerOdd.mub_family` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubFable.PrimePowerOdd.mub_family` |
| `MubFable.PrimePowerOdd.pair_qvec_cross_mul_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubFable.PrimePowerOdd.pair_qvec_cross_mul_star` |
| `MubFable.PrimePowerOdd.pair_qvec_same` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubFable.PrimePowerOdd.pair_qvec_same` |
| `MubFable.PrimePowerOdd.pair_std` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubFable.PrimePowerOdd.pair_std` |
| `MubFable.PrimePowerOdd.pair_std_qvec_mul_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubFable.PrimePowerOdd.pair_std_qvec_mul_star` |
| `MubFable.PrimePowerOdd.sum_mulShift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubFable.PrimePowerOdd.sum_mulShift` |
| `MubFable.PrimePowerOdd.weil_sum_mul_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubFable.PrimePowerOdd.weil_sum_mul_star` |

- counts toward the grade: yes

### Python: `checks/independent/mub-prime-power-construction.py`

- file: [checks/independent/mub-prime-power-construction.py](../../../checks/independent/mub-prime-power-construction.py)
- sha256 (`bytes`): `bd381422744d65b117272aa3b35091b72028741249e15953a163510af796e1bd`
- cited in: record TFQ-0403
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_0403_mub_prime_power_construction.md`

- file: [dag/derivations/25_mub/tfq_0403_mub_prime_power_construction.md](../../../dag/derivations/25_mub/tfq_0403_mub_prime_power_construction.md)
- sha256 (`lf-normalised`): `2f116e1ab962c5884f1b46f70c8bc323833fafbd19c85cfdf9db435a7cda9261`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0403
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/mub-prime-power-construction-odd.md`

- file: [dag/derivations/independent/mub-prime-power-construction-odd.md](../../../dag/derivations/independent/mub-prime-power-construction-odd.md)
- sha256 (`lf-normalised`): `e80e8e33edd70a2b7379216a0660b3f6d5df26e28f7c0116a71af9b180a1b3ea`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/mub-prime-power-construction.md`

- file: [dag/derivations/independent/mub-prime-power-construction.md](../../../dag/derivations/independent/mub-prime-power-construction.md)
- sha256 (`lf-normalised`): `d46d92da346abb519fd4cc96602f6f624bb0d1bf616963f4973a6208e5050064`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json`

- file: [dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json)
- sha256 (`lf-normalised`): `dad4fca8640ba69ff32ee4d72cb34d3685c19b2dc88ef7788f97cb408d05fe41`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_mub-prime-power-construction_lean_replay.json`

- file: [dag/research/campaign_mub-prime-power-construction_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction_lean_replay.json)
- sha256 (`lf-normalised`): `924d70ee83a46e14f69abab050d621fb2a576b10e6437b3b6765a964f4cca204`
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
