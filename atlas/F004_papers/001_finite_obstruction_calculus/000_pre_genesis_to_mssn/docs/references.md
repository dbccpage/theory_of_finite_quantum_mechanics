# Sources

All imported source records and proofs are exact Git blobs from revision
`d1d2f034198a72b730320a69691e63351557c019` of `dbccpage/the_symbol_game`.
The [manifest](../manifests/imported_sources.json) identifies each original path,
Git blob identifier, byte length and SHA-256. Local `.txt` reading copies retain
their original Markdown source, including historical relative links. Resolve
those links in the original tree at the recorded revision.

- [Pre-Genesis design and record](sources/pre_genesis/readme.txt).
- [Trial 1](sources/pre_genesis/sources/trial_1_transcript.txt),
  [Trial 2](sources/pre_genesis/sources/trial_2_transcript.txt) and
  [full replay](sources/pre_genesis/sources/full_replay_transcript.txt).
- [Genesis education account](sources/genesis_education.txt).
- [MSS-N correction record](sources/architecture.txt).
- [S(n) syntax](../code/grammar/sn.ebnf) and [MSS grammar](../code/grammar/mssn.ebnf).
- Allen Hatcher, [*Algebraic Topology*](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf),
  Cambridge University Press, 2002; §1.A, Proposition 2.7 and §2.A.

The predecessor manuscripts are preserved in the repository's internal source
intake. The main paper incorporates their substantive material and corrections;
their historic review documents are not part of the public package.

## Provenance of the HoTT interpretation

- The [S(n) account at the pinned revision](https://github.com/dbccpage/the_symbol_game/blob/d1d2f034198a72b730320a69691e63351557c019/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/source_archive/000_sn/paper.md#decoupling-construction-stage-n-from-homotopy-truncation-depth-j)
  distinguishes construction stage from homotopy truncation depth and requires
  a supplied realization before considering its Postnikov stages.
- The [MSS-N account at the pinned revision](https://github.com/dbccpage/the_symbol_game/blob/d1d2f034198a72b730320a69691e63351557c019/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/source_archive/000_mssn/paper.md#22-homotopy-type-theory-hott-lens-types-paths-and-directions)
  introduces HoTT explicitly as one of three mathematical lenses.
- The corrected walkthrough withdraws the inference from inverse carrier maps
  to univalence. The Pre-Genesis trial record supplies no derivation of HoTT.

## Companion monograph

The [WDP reading route](monograph_route.md) identifies the author-supplied
version 2.4.0 working manuscript and its exact SHA-256. This companion reference
is separate from the 34 historical imports pinned above. It provides the
chapter handoff and conditional finite-QM destination; no whole-monograph
verification is inferred from the present package checks.
