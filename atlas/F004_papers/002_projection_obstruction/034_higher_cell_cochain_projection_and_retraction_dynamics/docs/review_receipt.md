# PO-034 correction and review receipt

This is a historical receipt for the 2026-10-08 candidate.
The [2026-10-10 revision receipt](publication_revision_receipt.md) supersedes
its artifact page count and pending mathematical-work inventory.
Its 99-test, coverage, and notebook results were not rerun wholesale.

Date: 2026-10-08. Baseline commit: c33fb25be7f7bb340eb7345d90134dc116bac244.
Scope: technical preprint v0.1 (0.1.0) candidate. No merge or Zenodo publication.

## Findings resolved

- The prior proper-support tangent-isolation theorem was false. The corrected
  paper establishes one-site isolation, demonstrates a two-body triangle residual,
  and introduces the distinct R_k projector for the highest-order component.
- Subsystem count and simplicial degree were mixed; p=k-1 is now explicit.
  Boundary-state tangent language and the full-space derivative are qualified.
- The Taylor remainder proof used an unsupported local interaction budget.
  The corrected proof uses the whole Hamiltonian norm and uniform bounds.
- A polar residual witness was falsely said to annihilate the tangent space.
  An exact diagonal counterexample and numerical regression now refute that.
- Hodge/cochain claims were conflated with quantum entanglement. Scalar
  coefficients and the required observation maps are now stated.
- Square signs and semigroup curvature were conflated. Separate formulas and
  a directly totalized sign example replace the unsupported bridge.
- No-op boundary projection, subset ordering, fake vertical nilpotence, scalar
  adapter-loss subtraction, norm-based cycle inference, and verified mock
  receipts were repaired.
- The previous manifest sets and ZIP disagreed. The revised release contract
  checks the full regular payload, both controls, member bytes and envelope.

## Executed validation

- Python 3.12.14; 99 tests passed, including seven archive-contract regressions.
- Core statement coverage: 376/388 statements (96.91%, displayed as 97%).
- Ruff passes with the explicit code/pyproject.toml configuration.
- Mypy 1.19.1 passes on seven core source files.
- The revised notebook executes all seven code cells in explicit direct
  Python mode, from a temporary working directory outside the package.
  Source digest: 958d8fc23e44f036f6c07bc0e57d98d49deb83b47905df9f0fdaf7b770d57262.
  Outputs identify that method; no native-kernel claim is made.
- The static Lean census matches seven stored target declarations. Noncomment
  Lean source text is unchanged from the verified baseline; details and hashes
  are in lean4/evidence_scope.json. Proof terms and the stored report are preserved.
- The 10-page TeX/PDF rebuild and all-page visual inspection are recorded in
  docs/pdf_build_receipt.md.
- Both metadata files now use one description, creator list, version, keyword
  list, and the existing manuscript/code license split.

## Pending full replay gates

Fresh pinned Lean replay failed because Lake is unavailable on PATH in this
environment. The upstream [Lean 4.34.1 release](https://github.com/leanprover/lean4/releases/tag/v4.34.1) exists (2026-09-24); the pin is retained. A stored report and static source comparison do not replace a build.

Native Jupyter replay failed during kernel startup after socket/interface
operations were denied. The kernel died before replying to kernel_info.
The driver has an explicit direct mode; native execution never falls back
silently. The default verifier attempts both fresh gates and fails if either
cannot complete. The --review option checks the numerical review scope only.

No deposition identity was verified for PO-034. The earlier RELEASED label
was replaced with technical preprint v0.1 (0.1.0) candidate status. Manuscript
package version 0.1.0 is set; no DOI or new publication was minted.

## Remaining mathematical work

A concrete Lean density-matrix instantiation, any sharper local interaction
budget theorem, a declared general sheaf model, and a proved quantum-to-cochain
dynamics bridge remain open. None is inferred from the corrected examples.

Authority effect: None.
