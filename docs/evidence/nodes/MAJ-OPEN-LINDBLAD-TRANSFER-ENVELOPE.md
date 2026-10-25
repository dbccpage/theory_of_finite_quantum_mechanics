# MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For four MZMs under a Lindblad braiding model with gap Delta, length L/xi and poisoning rate Gamma_qp \> 0, the trace-norm transfer defect obeys Delta_transfer(T) \<= min(1, C_LZ (hbar/(Delta T))^2 + (Delta/hbar) e^{-L/xi} T + 1 - e^{-Gamma_qp T}) for T \>\> hbar/Delta, and that envelope has a positive minimum.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declaration references covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Lindblad master equation with poisoning and dephasing channels
- Landau-Zener leakage asymptotics

## Bottleneck

Derive the envelope from the Lindblad equation; a positive physical lower bound on Delta_transfer needs an independent argument, as the source notes.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C18 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1177
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `OpenSystemTransferBound` | yes | yes | yes | module-level | `#print axioms OpenSystemTransferBound` |
| `transfer_defect_lower_bound_pos` | yes | yes | yes | none | `#print axioms transfer_defect_lower_bound_pos` |
| `transfer_gap_strictly_positive` | yes | yes | yes | none | `#print axioms transfer_gap_strictly_positive` |
| `transfer_pareto_defect_pos` | yes | yes | yes | Quot.sound, propext | `#print axioms transfer_pareto_defect_pos` |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1177

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `OpenSystemMajoranaBraidModel` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1177_maj_open_lindblad_transfer_envelope.md`

- file: [dag/derivations/28_majorana/tfq_1177_maj_open_lindblad_transfer_envelope.md](../../../dag/derivations/28_majorana/tfq_1177_maj_open_lindblad_transfer_envelope.md)
- sha256 (`lf-normalised`): `53cb3ef57709000ab50b2af9f649db908622311f0a3e76d042fb184bdac507f5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1177
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

- `APP-R-MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-REALIZATION-PACKET-GAP](MAJ-REALIZATION-PACKET-GAP.md) (DEFINITION), [MAJ-HARDWARE-NARRATIVE-QUARANTINE](MAJ-HARDWARE-NARRATIVE-QUARANTINE.md) (DEFINITION)

Outgoing (3):

- `APP-R-MAJ-ENVELOPE-NAT-ARITHMETIC` `DERIVED_LEAN`: [MAJ-ENVELOPE-NAT-ARITHMETIC](MAJ-ENVELOPE-NAT-ARITHMETIC.md) (PROVED_LEAN)
- `APP-R-MAJ-OPEN-MULTITERMINAL-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-OPEN-MULTITERMINAL-ENVELOPE](MAJ-OPEN-MULTITERMINAL-ENVELOPE.md) (OPEN)
- `APP-R-MAJ-OPEN-NON-MARKOVIAN-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-OPEN-NON-MARKOVIAN-ENVELOPE](MAJ-OPEN-NON-MARKOVIAN-ENVELOPE.md) (OPEN)
