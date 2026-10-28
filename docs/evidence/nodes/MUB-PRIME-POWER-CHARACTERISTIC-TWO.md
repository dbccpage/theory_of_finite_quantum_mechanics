# MUB-PRIME-POWER-CHARACTERISTIC-TWO

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For d = 2^k with k \>= 2, construct d+1 bases of C^d, each orthonormal, with |\<u, v\>|^2 = 1/d for vectors u and v from different bases, using the Galois ring GR(4, k) and its Teichmuller set (Klappenecker-Roetteler) or the symplectic construction over F_(2^k) (Wootters-Fields), and verify every identity over an exact cyclotomic carrier.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The odd-characteristic family of MUB-PRIME-POWER-CONSTRUCTION uses x -\> psi(a x^2 + b x), which fails in characteristic two because x -\> x^2 is additive there. A Lean proof of this node, together with the odd case, would complete the prime-power construction.

## Source status

dag/derivations/independent/mub-prime-power-construction-odd.md record MUB-CAMPAIGN-448-CHAR2 claims no status; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MubPrimePowerOddCharacteristic.lean`

- file: [lean4/MubPrimePowerOddCharacteristic.lean](../../../lean4/MubPrimePowerOddCharacteristic.lean)
- sha256 (`bytes`): `b06c0a46415edf0abf7d56c39eee5e0deb074d314f327026e8c9adabcdaa0c28`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json](../../../dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json) (module `MubPrimePowerOddCharacteristic`): recorded sha256 `b06c0a46415edf0abf7d56c39eee5e0deb074d314f327026e8c9adabcdaa0c28` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubPrimePowerOddCharacteristic`
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1366_mub_prime_power_characteristic_two.md`

- file: [dag/derivations/25_mub/tfq_1366_mub_prime_power_characteristic_two.md](../../../dag/derivations/25_mub/tfq_1366_mub_prime_power_characteristic_two.md)
- sha256 (`lf-normalised`): `09f9a588bbb39e69b87bbf1c6a9028d0125bb0b52dd22cf2f2225792960b3f65`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1366
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/mub-prime-power-construction-odd.md`

- file: [dag/derivations/independent/mub-prime-power-construction-odd.md](../../../dag/derivations/independent/mub-prime-power-construction-odd.md)
- sha256 (`lf-normalised`): `9e8ad0fc2ac612f9c5b04dba9346d52f9d65c09154e568189cfce7b4ee816a45`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB-PRIME-POWER-CHARACTERISTIC-TWO` `GAP_NO_DERIVATION`: [MUB-PRIME-POWER-CONSTRUCTION](MUB-PRIME-POWER-CONSTRUCTION.md) (OPEN)

Outgoing (0):

