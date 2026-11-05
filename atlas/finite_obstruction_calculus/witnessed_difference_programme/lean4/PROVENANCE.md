# Provenance

Authority effect: none.

The package was authored in CODA at commit
`a5371ca431eba6deb855662a505edff30723fe07`. No source was imported from the
sealed 19L57G1 repository.

The design was cross-checked against these live CODA sources at that commit:

- `coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/`
  `000_from_primitive_difference_to_finite_obstruction_calculus/lean4/`
  `FromPrimitiveDifferenceToFiniteObstructionCalculus/`
  `J011_minimal_publication.lean`, SHA-256
  `7ee3a63b154220f82b76a49a045ca074afa899f4d6a087bcb29c93cd0698d6f4`.
- `atlas/papers/finite_obstruction_calculus/`
  `006_primitive_axiomatics/lean4/foc000_l000_05_observer_passivity.lean`,
  SHA-256
  `02dddd6ecf7102dea95af07c24f7177364be65a31d0592e9eefcf58b49d827d1`.
- `atlas/papers/finite_obstruction_calculus/`
  `006_primitive_axiomatics/lean4/`
  `foc000_l000_06_finite_observer_family_poset.lean`, SHA-256
  `55325d1ca13b3951062c4999a6a26e05927581edf6d92ce41449ead5ff81a39d`.

Only mathematical ideas and scope boundaries were adapted. Module names,
structures, theorem statements, and proof terms in this package are newly
authored. The provenance links do not upgrade any programme claim.

## 2026-09-29 absorption of the primitive-axiomatics Lean core

`WitnessedDifference/Obstruction.lean` and
`WitnessedDifference/ObserverResolution.lean` were written when the sibling
package `006_primitive_axiomatics` (v2.10.0) was absorbed into this monograph.
They adapt the following source files, read at repository commit
`c11b2da09b3d333013553d621ba5689d2e67aa49`:

| Source file (`006_primitive_axiomatics/lean4/`) | SHA-256 | Disposition |
| --- | --- | --- |
| `KappaWellDefined.lean` | `b6b1ff8d7251ff14bae3ce767272ec1735503225bafdf114f3f51e7b4f30465c` | restated, and lifted to the quotient by the repair relation |
| `ExactSequence.lean` | `20619aaa97b3f72c1edff8edd56af1782e7be4347038151d3761f5eb36706dbe` | replaced: the source proved kernel/range exactness for an arbitrary function; the new theorem is stated on the quotient by the repair relation |
| `ClosureRatioBound.lean` | `bfb78023ffcd4bc3b3fcdfe9048120823bc8c9a8ac330189de4d7f5665d1ea5e` | replaced: the source used natural-number floor division; the new theorems use ℚ and derive the bound from the infimum property |
| `ObserverPassivity.lean` | `be8f6e6cea9b8d3036b70c3a233ad7363e0cb605bc294f86afbb91a9ac03ad59` | restated; still close to packaged, because the fiber lower bound is a hypothesis |
| `ObserverFamilyPoset.lean` | `2aa56f40024aa1dd0bd8e5656c2820cb97f494535fad116a7f2449070986903a` | ported; finest and coarsest theorems added |
| `GrammarBound.lean` | `59e633cf80f6745105f7d812b9915e9d6354a2324355cac939dfdfb0cf7efc8e` | ported; alias theorems dropped |
| `TriangleReplay.lean` | `c60898ce870f1277974ed8118cf7fe7dfefeb5e5798ed21eee4f7f1db39021a0` | replaced: the source quantified over ℤ potentials; the new theorem quantifies over ℚ and derives the lower bound from the dual-certificate lemma |

`ConstructorIncrement.lean` (initiality and reflective completion) was not
ported. Its topic is the open routing and refinement interface (CH04-O01).

## 2026-09-29 absorption of six genesis-alpha papers

`WitnessedDifference/PointedRelation.lean`, `ComplexGrowth.lean`, and
`Interference.lean`, and the additions to `Descent.lean`, were written for the
rows absorbed from papers 012, 015, 003, 035, 020, and 007 under
`../../000_genesis_alpha_program/`. The directories of 012, 015, 003, and 020
were later removed from the tree; the files named below remain readable at
commit `c11b2da09b3d333013553d621ba5689d2e67aa49`. None of those papers' Lean
was copied:

- 007's `lean4/PaperTwo/PrimDiff.lean` (SHA-256
  `cc7c0c0b86691058161ec032a0aa11b0ebc52873f7756a05775c55b73ef9714b`) was read for
  the pointed-relation countermodels; `PointedRelation.lean` restates them
  without its framing, and nothing here depends on the external study it
  describes.
- 035's Lean was judged packaged over natural numbers, 012's cited files were
  unrelated to its claims, and 003's cited theorems live in an unpinned external
  repository; none was ported.
- The Sorkin identity in `Interference.lean` is a clean-room statement for any
  additive operation and biadditive readout, broader than the Gaussian-integer
  instance the 003 paper cited.

## 2026-09-29 classical corner

`WitnessedDifference/ClassicalCorner.lean` is newly authored and is the only
module that imports Mathlib. It uses Mathlib's `Equiv.Perm.permMatrix`,
`GaussianInt` (`Zsqrtd (-1)`) with its norm lemmas, and
`QuadraticAlgebra ℚ (-1) 0` for ℚ(i). No source was copied. The repository's
finite quantum mechanics workspace was read for context at
`lean4/quantum_mechanics/H003ReversibilityGate.lean` and
`H006PermutationUnitary.lean`: H006 shows that the map `(u, v) ↦ (i v, i u)`
over `GaussianInt` preserves the form without being a report bijection, and
`unitary_package_is_classical` classifies that envelope (every such map is
monomial). Nothing here depends on that workspace.

## 2026-09-29 packet adapter

`WitnessedDifference/EmpiricalModel.lean` and
`WitnessedDifference/PacketAdapter.lean` are newly authored. The empirical
models, global sections, and strong contextuality follow the definitions of
Abramsky and Brandenburger (REF-QM-001 in `../docs/references.md`), restated
for rational weights on a cover given as a family of finite sets. The PR box
and its signed global section were computed for this package. No source was
copied.

## 2026-09-30 quantum route

`WitnessedDifference/ClassicalPackage.lean`, `ToleranceAdapter.lean`,
`Composition.lean`, `AmplitudeBridge.lean` and `InstrumentAdapter.lean` are newly
authored for the rows `WDP-CH18-P07`, `WDP-CH18-P08` and `WDP-CH19-P06` through
`WDP-CH19-P14`. The mixture decomposition of a stochastic update, the tolerant
adapter and its two-context repair, the injective-tagging and bilinear-form
statements, the gauge descent of phase-blind readouts, the rational-phase
obstruction, and the qubit instrument adapter were derived for this package.
The definitions follow standard finite-dimensional sources only where the text
cites them (Abramsky and Brandenburger for empirical models, REF-QM-001). No
source was copied.

## 2026-09-30 absorption of eight genesis-alpha papers

No Lean was written or ported for the rows absorbed from papers 004, 005, 006,
008, 009, 010, 011, and 022 under `../../000_genesis_alpha_program/`; their
twelve new rows carry prose evidence only and appear in `claim_map.md` as
prose-only or nonclaim rows. The sources' Lean was read for provenance: 006's
modules are vendored copies of the external Genesis study, which the atlas
rules exclude; 009's single-triple curvature module and 011's cycle modules
prove narrower statements than CH16-P05 and CH11-P02; and 004 and 005 cite
Lean in an external repository at a commit other than the required tag. The
directories were removed from the tree after absorption; their files remain
readable at commit `fd5da94dbebe2702c9a10b3577a64005db3dbf7a`.

