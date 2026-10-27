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

The characteristic-two family is dimension 2 only. For odd characteristic the construction is now general: for every finite field F with 2 ≠ 0, every commutative domain R with a star ring structure, every nontrivial additive character ψ : F → R with star (ψ t) = ψ (−t), and q = |F| nonzero in R (hypothesis hq of mub_family), the q+1 bases indexed by Option F (the standard basis and x ↦ ψ(a x² + b x)) are pairwise orthogonal within a basis, have nonzero norms, and satisfy |⟨u, v⟩|² · q = ‖u‖² ‖v‖² across bases, with q+1 = card (Option F) (mub_family, card_bases). Spanning is not proved: the Lean statement is about orthogonal families, which are R-bases of R^F when R is a field (so over ℂ or ℚ(ζ_p)) but need not span over a domain in which q is not a unit (F = 𝔽₃, R = ℤ\[ζ₃\]). The vectors are left unnormalised, so normalisation is the statement about norms, not a division. What remains: a complete family for characteristic two beyond dimension 2 (which needs the Galois-ring or symplectic-spread construction, not quadratic phases), the instantiation of ψ over the concrete complex or cyclotomic carrier the node names (ψ is a parameter here), and the dimension-six question, which this node does not address.

## Source status

Dimension-2 Gaussian-integer bases Z, X and Y (characteristic two). For every odd prime power q a complete q+1 family of orthogonal, mutually unbiased vector families is constructed over any commutative domain with a star ring structure (bases of R^F when R is a field; spanning is not formalised), given a nontrivial unitary additive character of F_q as a parameter (lean4/MubPrimePowerOddCharacteristic.lean). Characteristic two beyond dimension 2, and the existence of the character over the concrete complex or cyclotomic carrier, stay open.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MubPrimePowerConstruction.lean`

- file: [lean4/MubPrimePowerConstruction.lean](../../../lean4/MubPrimePowerConstruction.lean)
- sha256 (`bytes`): `9239bffb805755bc6a937dfcbd0d35e258ac7ffb356d5be09f172eda4b93fbec`
- cited in: node.lean, receipt dag/research/campaign_mub-prime-power-construction_lean_replay.json (MubPrimePowerConstruction), receipt dag/research/pr_359_review_replay.json (MubPrimePowerConstruction), record TFQ-0403
- replay: `verified`
  - receipt [dag/research/campaign_mub-prime-power-construction_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction_lean_replay.json) (module `MubPrimePowerConstruction`): recorded sha256 `9239bffb805755bc6a937dfcbd0d35e258ac7ffb356d5be09f172eda4b93fbec` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_359_review_replay.json](../../../dag/research/pr_359_review_replay.json) (module `MubPrimePowerConstruction`): recorded sha256 `9239bffb805755bc6a937dfcbd0d35e258ac7ffb356d5be09f172eda4b93fbec` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build MubPrimePowerConstruction`

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

### Lean: `lean4/MubPrimePowerOddCharacteristic.lean`

- file: [lean4/MubPrimePowerOddCharacteristic.lean](../../../lean4/MubPrimePowerOddCharacteristic.lean)
- sha256 (`bytes`): `b06c0a46415edf0abf7d56c39eee5e0deb074d314f327026e8c9adabcdaa0c28`
- cited in: node.lean, receipt dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json (MubPrimePowerOddCharacteristic)
- replay: `verified`
  - receipt [dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json) (module `MubPrimePowerOddCharacteristic`): recorded sha256 `b06c0a46415edf0abf7d56c39eee5e0deb074d314f327026e8c9adabcdaa0c28` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubPrimePowerOddCharacteristic`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `MubPrimePower.PrimePowerOdd.basis_orthogonal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubPrimePower.PrimePowerOdd.basis_orthogonal` |
| `MubPrimePower.PrimePowerOdd.basis_unbiased` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubPrimePower.PrimePowerOdd.basis_unbiased` |
| `MubPrimePower.PrimePowerOdd.card_bases` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubPrimePower.PrimePowerOdd.card_bases` |
| `MubPrimePower.PrimePowerOdd.mub_family` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubPrimePower.PrimePowerOdd.mub_family` |
| `MubPrimePower.PrimePowerOdd.pair_qvec_cross_mul_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubPrimePower.PrimePowerOdd.pair_qvec_cross_mul_star` |
| `MubPrimePower.PrimePowerOdd.pair_qvec_same` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubPrimePower.PrimePowerOdd.pair_qvec_same` |
| `MubPrimePower.PrimePowerOdd.pair_std` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubPrimePower.PrimePowerOdd.pair_std` |
| `MubPrimePower.PrimePowerOdd.pair_std_qvec_mul_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubPrimePower.PrimePowerOdd.pair_std_qvec_mul_star` |
| `MubPrimePower.PrimePowerOdd.sum_mulShift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubPrimePower.PrimePowerOdd.sum_mulShift` |
| `MubPrimePower.PrimePowerOdd.weil_sum_mul_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MubPrimePower.PrimePowerOdd.weil_sum_mul_star` |

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
- sha256 (`lf-normalised`): `9e8ad0fc2ac612f9c5b04dba9346d52f9d65c09154e568189cfce7b4ee816a45`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/mub-prime-power-construction.md`

- file: [dag/derivations/independent/mub-prime-power-construction.md](../../../dag/derivations/independent/mub-prime-power-construction.md)
- sha256 (`lf-normalised`): `d46d92da346abb519fd4cc96602f6f624bb0d1bf616963f4973a6208e5050064`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json`

- file: [dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json)
- sha256 (`lf-normalised`): `c6ffea0c7c63b8026e7862b5b74364f234970dce759dde850517ba6cbfa35641`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_mub-prime-power-construction_lean_replay.json`

- file: [dag/research/campaign_mub-prime-power-construction_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction_lean_replay.json)
- sha256 (`lf-normalised`): `4826491277051b78fa1d5060cc5be1d77ccd681537cdfbe64bfe1c9de1e39450`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/README.md`

- file: [papers/core/mub6/README.md](../../../papers/core/mub6/README.md)
- sha256 (`lf-normalised`): `b876520ea3960bef932e3723a1c47c60d05dace398dcb9a77518b724d8216f8e`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB-PRIME-POWER-CONSTRUCTION` `GAP_NO_DERIVATION`: [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)

Outgoing (1):

- `APP-R-MUB6-NO-FIELD-OF-ORDER-SIX` `CONDITIONAL_ON_IMPORT`: [MUB6-NO-FIELD-OF-ORDER-SIX](MUB6-NO-FIELD-OF-ORDER-SIX.md) (IMPORTED_ASSUMPTION)
