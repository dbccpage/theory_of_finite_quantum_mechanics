# CHSH norm-admission evidence

This directory accompanies DAG node `FQ-CHSH-NORM-ADMISSION-COMPARISON` and the [TFQ-2621 derivation note](../../dag/derivations/10_finite_qm_core/tfq_2621_chsh_norm_admission_comparison.md).

- `verification.json` records fresh theorem, exact-arithmetic and negative-control checks for the declared comparison. Its status and hashes control what this run supports.
- `dag_validation_baseline.json` preserves the 1,395 full-file DAG validation failures already present before the DAG edits in this slice. Most concern historical paths and moved receipts. It is evidence of the pre-existing checkout state, not evidence against or for a mathematical theorem.
- `dag_validation.json` compares final full-file failures with that baseline and records structural/view checks separately. A passing structural check validates identifiers, routes, source-reference structure and generated views; it does not prove the node's mathematics.

The norm, real linear carrier, contractive effects and unbiased binary readout are supplied. The parallelogram premise belongs only to the quadratic-bound branch. Reconstruction through Mathlib exposes its equivalence to inner-product geometry; it does not derive that premise from the earlier supplied assumptions. The classical positive global joint law is a separate comparison assumption.

Existing historical receipts and the Genesis-to-Hilbert gaps are not discharged or overwritten by this evidence.

## Reproduce

From the repository root on Windows:

```powershell
& .\.venv\Scripts\python.exe evidence/chsh_norm_admission/verify.py
```

The driver uses the installed toolchain named in `lean4/lean-toolchain` and the
existing Mathlib build. Supply `--lean-bin PATH` if the toolchain is installed
outside `ELAN_HOME`. It recompiles the module, audits all 28 expected theorem
axiom reports, runs the exact and atlas tests, checks atlas synchronization and
DAG structure/views, and writes a receipt bound to the source hashes. The full
DAG reference comparison remains separately identified, including its existing
failures; `scope_passed` does not mean the entire repository is validated.

`lake build CHSHAdmission` is the named Lean build target. The proof uses only
the standard reported Lean/Mathlib axioms `propext`, `Classical.choice`, and
`Quot.sound`, with no `sorry` or new axioms. The executable finite replay uses
exact rational and quadratic-field arithmetic, without floating-point tolerances.

## Publication snapshot

`publication_verification.json` identifies the isolated commit prepared from current main. The original workspace receipts above are preserved unchanged. Their whole-DAG hashes and 1,395-reference-failure baseline describe that original workspace, not the publication tree. The published proof, exact replay, tests, Lean toolchain and dependency manifest match the verified inputs byte-for-byte; the publication DAG was separately rendered and structurally checked using main's tools.
