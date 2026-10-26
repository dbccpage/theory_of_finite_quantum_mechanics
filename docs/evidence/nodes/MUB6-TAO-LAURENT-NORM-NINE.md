# MUB6-TAO-LAURENT-NORM-NINE

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the Tao matrix S6 and each of the 20 balanced sign vectors g (three +1, three -1), |sum_j prod_r S_rj^{g_r}|^2 = 9, computed over the integer Eisenstein table and over C with w = -1/2 + i sqrt 3/2.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This is a finite evaluation for one matrix; without Conjecture 2 for arbitrary MU triples it gives no nonextension statement, and the source wording as an l1 operator norm does not match the computed quantity. Relation to OpenAI: its Fourier-vanishing theorem exempts exactly the Tao class, and the repository phase table equals OpenAI taoExponent after the index involution (3 5) (exhaustive search; lean4/MubOpenAIBridge.lean tao_phase_bridge, compiled 2026-10-21 under Lean 4.35.0 with standard axioms only), so this evaluation concerns the exceptional matrix. It is not an obstruction to extension.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-076 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Conjecture2GeneralMechanization.lean`

- file: [lean4/Conjecture2GeneralMechanization.lean](../../../lean4/Conjecture2GeneralMechanization.lean)
- sha256 (`bytes`): `6598ff7b86fd0f334a033417fce411be70b569afcf0983ae5882994816b78101`
- cited in: node.lean, record TFQ-1253
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `Conjecture2GeneralMechanization`): recorded sha256 `6598ff7b86fd0f334a033417fce411be70b569afcf0983ae5882994816b78101` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build Conjecture2GeneralMechanization`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `balanced_mask_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms balanced_mask_count` |
| `tao_all_balanced_masks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms tao_all_balanced_masks` |

- counts toward the grade: yes

### Lean: `lean4/MubTaoLaurent.lean`

- file: [lean4/MubTaoLaurent.lean](../../../lean4/MubTaoLaurent.lean)
- sha256 (`bytes`): `52ebf998525088a85ab86f4b089fa8b3ff8ffc1546f6275558dcc351be5ba2d3`
- cited in: node.lean, record TFQ-1253
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MubTaoLaurent`): recorded sha256 `52ebf998525088a85ab86f4b089fa8b3ff8ffc1546f6275558dcc351be5ba2d3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubTaoLaurent`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `tao_all_balanced_laurent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms tao_all_balanced_laurent` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1253_mub6_tao_laurent_norm_nine.md`

- file: [dag/derivations/25_mub/tfq_1253_mub6_tao_laurent_norm_nine.md](../../../dag/derivations/25_mub/tfq_1253_mub6_tao_laurent_norm_nine.md)
- sha256 (`lf-normalised`): `ac7e28d6eb2de50be1fdbc2c3b33e9191762acc6a942dfd1880d665cb72a0210`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1253
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.jsonl`

- file: [papers/core/mub6/theory_of_finite_mub6.jsonl](../../../papers/core/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `815b535641140895e823e99e201cf3314a9054db022f5a0c35be601a18663839`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.md`

- file: [papers/core/mub6/theory_of_finite_mub6.md](../../../papers/core/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `b515bf981d6c3a339c2b0a7937d54d9deb05f3b53186c584b83f5fa3419dc902`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-TAO-LAURENT-NORM-NINE` `DERIVED_LEAN`: [MUB6-TAO-MATRIX-CHM](MUB6-TAO-MATRIX-CHM.md) (PROVED_LEAN), [MUB6-CONJECTURE2-PREMISE](MUB6-CONJECTURE2-PREMISE.md) (OPEN)

Outgoing (0):

