# PO-033 in-place repair review

Reviewed 2026-10-02. The local review started from main commit
`f421aea24666bfd77b9cb5dba7aff00988db0cbc`; package tree
`90d2b9dfd10ca2c9bc4203b7f4f9c460081fbf44`.
Every downloaded original file was checked against its Git blob SHA before edits.
The package was unchanged when checked against newer main
`2548dc15be9f95c6bb4be6fcb0b1077be05528b6`.
Changes are limited to this package. Existing version 1.0.0 and archive name are
retained. No Zenodo publication or PR merge is part of this repair.

## Baseline findings and repairs

| Finding | Evidence | Repair |
|:--|:--|:--|
| Final residual attached to the previous state | Two-qubit all-up TFIM, times 0 and 0.2, one-qubit ceiling: reported final rate and integral zero despite recomputed rate about 0.30 and nonzero reference ZZ error | Propagate first, then sense and record the same time |
| Site marginals miss internally correlated cluster boundaries | Bell pair on sites 0,1 and a mixed qubit on site 2 with Z1Z2: site-marginal rate zero, full-factor rate two | Embed each edge on its full adjacent cluster factors |
| Merge could erase prior interval contributions | Post-merge outgoing rate zero at an endpoint with a positive incoming rate | Store incoming/outgoing rates and accumulated interval estimates |
| Blocked edge and order bias | Strongest infeasible edge could hide another merge; effective Hamiltonians read already updated neighbors | Select among feasible edges; construct all substep Hamiltonians from the same incoming states |
| Periodic bond and basis-order errors | Periodic N=2 has two declared ordered bonds; cluster input order defines a tensor basis | Match ordered terms once; permute densities when canonicalizing cluster site order |
| Input and time-grid mismatch | Invalid density matrices and nonfinite/decreasing grids could be accepted; exact and approximate solvers used different origins | Validate domains, use the first sample as initial time, and require identical reference grids |
| Geometric and witness claims overstated | The three-term differential belongs to a normalized ambient extension; an explicit norm witness does not annihilate the tangent | Correct domains and add a best-approximation counterexample |
| Metadata/ledger/PDF/ZIP contradicted scope correction | Loose hashes passed, but archive check failed on the manuscript; old PDF and descriptions retained certification claims | Align the current manuscript, six claim IDs, metadata, notebook, rendered artifacts, and release contents |
| Release verification ignored declared digests and missing ZIP members | Prior archive loop checked only members that existed and did not compare manifest digest values | Validate exact inventories, all hashes, member uniqueness and canonical metadata, and every archived byte |

Before repair the suite passed **41 tests, 98.17% statement coverage**. The loose
checksum inventory also passed. Neither result detected the counterexamples.
The original release check failed on stale manuscript bytes.

## Fresh validation

- **136 tests passed; 99.01% statement coverage**: 710 statements, 7 misses,
  with a 95% threshold enforced. The suite includes the solver counterexamples,
  density/time-domain checks, norm-witness counterexample, and 23 release and
  evidence-association negative controls.
- Six numerical reference comparisons are recorded in
  `review_observations.json`. Reproduction checks rtol $10^{-10}$ and
  atol $10^{-12}$. The adaptive estimate exceeds the 0.1 target in all three
  nine-sample runs. These are fixture-specific observations, not uniform
  bounds or equal-budget performance comparisons.
- The reviewer notebook has **7 code cells**, cleared committed outputs, and
  physicality/assertion checks for its selected fixture. Headless replay runs
  from both the package and notebook directories. It does not test live widgets.
- The canonical manuscript has a rebuilt **7-page PDF** and associated TeX.
  All pages were rendered and inspected; the equations and tables were also
  inspected at full render size. The build reported no missing glyphs or
  overfull lines. Two same-environment rebuilds yielded identical PDF bytes.
  Both artifacts carry the current manuscript SHA256 association marker.
- The release checker enforces payload/manifest/ZIP inventory and bytes. The
  same scoped verifier is used for loose files and extracted archive payload.
  Byte integrity and source association do not establish mathematical truth.
- **Fresh Lean verification was unavailable.** The toolchain pin, proof sources,
  lockfile, and historical axiom report remain unchanged. The explicit
  `--skip-lean` mode reports the skipped build/audit. The default verifier
  requires both a fresh Lake build and axiom audit; unavailable Lean fails that
  requirement.

The final release check and archive extraction commands are:

~~~bash
python scripts/rebuild_release.py --check
python verify_deposit.py --skip-lean
# Within the extracted certified_adaptive_quantum_dynamics directory:
python verify_deposit.py --extracted --skip-lean
~~~

The payload inventory and checksums in the committed manifests identify the
exact reviewed files. The ZIP includes those payloads and both manifests,
excluding its own outer file and build/cache output.

## Environment and remaining limits

Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1, pytest 8.3.5, pytest-cov 7.1.0,
coverage 7.16.2, PyYAML 6.0.3, and Matplotlib 3.11.2. Numerical commands use one
BLAS/OpenMP thread. Typesetting used Pandoc 3.1.3 and TeX Live 2023 XeLaTeX;
inspection used Poppler.

The solver remains `HEURISTIC_UNCERTIFIED`: sampled ideal tangent
residuals do not enclose actual integration or quadrature error. The classical
actual-defect theorem is conditional; the Lean model is an abstract Nat/Int
finite-sum analogue with mathematical premises passed as hypotheses. The
correlation implication additionally assumes a common exact-edge defect lower
bound. These limitations are stated where the claims appear, in both metadata
descriptions, and in the ledgers.

