# MAJ-OPEN-NON-MARKOVIAN-ENVELOPE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a bath J(w) = 2 pi alpha w_c^{1-s} w^s e^{-w/w_c}, the envelope C_LZ (hbar/(Delta T))^2 + A_s T^p has minimizer T* = (2 C_LZ hbar^2 / (p A_s Delta^2))^{1/(p+2)}, a positive minimum for alpha \> 0, and exponent beta = 2/(p+2).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- structured bosonic bath spectral density (Leggett et al. 1987)

## Bottleneck

Derive the bath term A_s T^p and p(s) from the spectral density; the calculus minimization of the stated envelope is not written out.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C19 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1178
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `NonMarkovianTransferBound` | yes | yes | yes | - | `#print axioms NonMarkovianTransferBound` |
| `non_markovian_pareto_defect_pos` | yes | yes | yes | - | `#print axioms non_markovian_pareto_defect_pos` |
| `non_markovian_transfer_defect_pos` | yes | yes | yes | - | `#print axioms non_markovian_transfer_defect_pos` |
| `pareto_denominator_pos` | yes | yes | yes | - | `#print axioms pareto_denominator_pos` |
| `sub_ohmic_exponent_shift` | yes | yes | yes | - | `#print axioms sub_ohmic_exponent_shift` |
- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1178

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `NonMarkovianBosonicBathModel` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1178_maj_open_non_markovian_envelope.md`

- file: [dag/derivations/28_majorana/tfq_1178_maj_open_non_markovian_envelope.md](../../../dag/derivations/28_majorana/tfq_1178_maj_open_non_markovian_envelope.md)
- sha256 (`lf-normalised`): `5cb1971f2b52353bd3b0d5a0a077c672ff1cefe290f1f02c4704a93ea1a9c1ee`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1178
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_claim_ledger.md`

- file: [papers/core/majorana/the_majorana_problem_claim_ledger.md](../../../papers/core/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `2d2b91881568780f56d7cdb53c97eec42bbfa09c21b2f1c6302665a79aad7565`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-OPEN-NON-MARKOVIAN-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE](MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE.md) (OPEN)

Outgoing (0):

