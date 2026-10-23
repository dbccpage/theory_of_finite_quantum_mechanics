# FSP-INVOLUTION-PAIR-CANCELLATION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For any carrier with weights in N and signs +-1, an involution tau with w(tau c) = w(c) and sign(tau c) = -sign(c) has no fixed point and each pair satisfies w(c) sign(c) + w(tau c) sign(tau c) = 0; zero signed sum does not require such a pairing (+2, -1, -1), and a cancelling doublet can carry a nonzero observable numerator.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- supplied weight-preserving sign-reversing involution

## Bottleneck

Summing pairs to get sum_c w(c) sign(c) = 0 on a finite set is a prose orbit-partition step (manuscript Section 4.2), not mechanized; observable numerators need A o tau = A; the involution is sufficient, not necessary (INV-INVOL-CANC).

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-027 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean`

- file: [papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean](../../../papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean)
- sha256 (`bytes`): `85c88263bbce28035a35b9282b747a7e97959c514a66c3c49fa770d5db49f6cd`
- cited in: node.lean, record TFQ-1193
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_fermion_sign.json](../../../dag/research/lean_replay_campaign_fermion_sign.json) (module `papers.core.fsp.lean4.FrustratedSpectrumObstruction`): recorded sha256 `85c88263bbce28035a35b9282b747a7e97959c514a66c3c49fa770d5db49f6cd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bipartite_pair_exact_cancellation` | yes | yes | yes | propext | `#print axioms bipartite_pair_exact_cancellation` |
- counts toward the grade: yes

### Lean: `papers/core/fsp/lean4/MeronCharacter.lean`

- file: [papers/core/fsp/lean4/MeronCharacter.lean](../../../papers/core/fsp/lean4/MeronCharacter.lean)
- sha256 (`bytes`): `0252c6f943a0bdf6a9975a60cbc041c932c58fe9cf335fa3381f1c987b9e1870`
- cited in: node.lean, record TFQ-1193
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_fermion_sign.json](../../../dag/research/lean_replay_campaign_fermion_sign.json) (module `papers.core.fsp.lean4.MeronCharacter`): recorded sha256 `0252c6f943a0bdf6a9975a60cbc041c932c58fe9cf335fa3381f1c987b9e1870` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/MeronCharacter.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `observable_doublet_counterexample` | yes | yes | yes | none | `#print axioms observable_doublet_counterexample` |
| `unequal_three_term_cancellation` | yes | yes | yes | none | `#print axioms unequal_three_term_cancellation` |
- counts toward the grade: yes

### Lean: `papers/core/fsp/lean4/MeronClusterInvolution.lean`

- file: [papers/core/fsp/lean4/MeronClusterInvolution.lean](../../../papers/core/fsp/lean4/MeronClusterInvolution.lean)
- sha256 (`bytes`): `82aec60d21a474e25be9f3c7f1165b201bb6b6e2a972f047b6ae88758ba4044f`
- cited in: node.lean, record TFQ-1193
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_fermion_sign.json](../../../dag/research/lean_replay_campaign_fermion_sign.json) (module `papers.core.fsp.lean4.MeronClusterInvolution`): recorded sha256 `82aec60d21a474e25be9f3c7f1165b201bb6b6e2a972f047b6ae88758ba4044f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/MeronClusterInvolution.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `fixed_point_contradiction` | yes | yes | yes | none | `#print axioms fixed_point_contradiction` |
| `meron_pair_exact_cancellation` | yes | yes | yes | propext | `#print axioms meron_pair_exact_cancellation` |
- counts toward the grade: yes

### Python: `code/python/tests/fsp/test_normal_form_laws.py`

- file: [code/python/tests/fsp/test_normal_form_laws.py](../../../code/python/tests/fsp/test_normal_form_laws.py)
- sha256 (`bytes`): `a8cd7a31a7c283efd112f89d8c2a12f4a258e8dbbe360247a50e72cb02da9aaa`
- cited in: record TFQ-1193
- check: `python -m pytest code/python/tests/fsp/test_normal_form_laws.py::test_near_equal_or_zero_total_does_not_imply_equal_weight_pairing`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_near_equal_or_zero_total_does_not_imply_equal_weight_pairing` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/test_normal_form_laws.py::test_near_equal_or_zero_total_does_not_imply_equal_weight_pairing` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1193_fsp_involution_pair_cancellation.md`

- file: [dag/derivations/26_fsp/tfq_1193_fsp_involution_pair_cancellation.md](../../../dag/derivations/26_fsp/tfq_1193_fsp_involution_pair_cancellation.md)
- sha256 (`lf-normalised`): `aa785d94a1372927e3ca237e4c0fb075b11903f6e2500e9c096e84d770cbe5ef`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1193
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3268ac1be0222f75b9b9238508325cab337a6f767114e2d25afff56163a42cf4`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-INVOLUTION-PAIR-CANCELLATION` `DERIVED_LEAN`: [FSP-SIGNED-HOPPING-PATH-SERIES](FSP-SIGNED-HOPPING-PATH-SERIES.md) (PROVED_PROSE)

Outgoing (2):

- `APP-R-FSP-GIN-EQUAL-WEIGHT-PAIRING` `COMPUTED`: [FSP-GIN-EQUAL-WEIGHT-PAIRING](FSP-GIN-EQUAL-WEIGHT-PAIRING.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
