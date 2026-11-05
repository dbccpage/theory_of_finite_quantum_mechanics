# PO-034 publication revision receipt

Date: 2026-10-10. Version: v0.1 (0.1.0), unpublished technical preprint.
Reviewed snapshot: 79fd9db728055deb001b7618e321f86e9ed4f97c.
Repair branch starts at remote main df84a59644c2a6837756273ccedd7b1233525407.

## Changes

The current rendered manuscript includes the six written lemmas 4.3a--4.3f.
The residual eigenvalues and singular values are distinguished. The generators
are trace-annihilating; their exponential semigroups preserve trace.
The one-term site-budget specialization declares full support.
Every dilation no-go claim uses a fixed finite carrier, a fixed time-independent
Hermitian Hamiltonian and a fixed initial total state for all nonnegative time.
Correlation distance is attributed to Hall, including the two-qubit sufficient
criterion above one. An explicit nearer product state distinguishes the chosen
marginal-preserving retraction from nearest-product optimization.

The YAML syntax and expanded evidence schema are repaired. The verifier checks
thirteen claims, six written-only proof locations and assumptions, seven numerical
example mappings, and seven stored abstract Lean declarations. Location checks
do not execute or validate the written mathematical proofs.

## Scoped validation

- Python 3.12.10: claim-evidence, release-contract and trace-defect regression
  files only. The exact test result and archive digest were recorded in the
  adjacent release receipt. That unchanged historical record now lives at
  [release_receipt_2026-10-10.json](release_receipt_2026-10-10.json); its digest
  identifies the earlier archive, before this packaging consolidation.
- Static census and direct Python notebook replay are recorded separately
  from fresh Lean compilation and native Jupyter execution.
- The regenerated 24-page PDF was inspected on all-page contact sheets;
  pages 9 and 18 were additionally inspected at reading resolution.
  The current hashes and compiler versions are in the PDF build receipt.
- Both checksum controls and the selected canonical ZIP are qualified against
  the complete current payload. Replay subprocesses must leave the initial
  payload, controls and selected archive unchanged.
- Canonical rebuilding must produce identical ZIP bytes. Release-boundary
  tests include extra bytes, duplicate/case-colliding members, nonregular
  controls, fatal traversal errors and post-replay mutations.

The historical 99-test/coverage receipt remains historical. No full repository
test run, new coverage claim, fresh pinned Lean build, native Jupyter execution,
DOI assignment, Zenodo deposit, merge, or publication approval is asserted.
The quantum-to-cochain dynamics bridge remains open.

Authority effect: None.
