# Lean verification receipts

Current audit scope (2026-10-08): 50 core-only modules and 691 selected declaration reports were replayed under Lean 4.33.1; 25 additional named module compilations include overlaps with that set. Counts below describe their dated receipts. Fresh compilation of the full Mathlib-backed root remains unverified because the pinned cache download is blocked in this environment. Source review and historical receipts are not a substitute for that build.

## Core-only supplement recorded on 2026-10-02

The separate `FiniteDerivations.lean` spine has twenty-seven modules and 379 selected
declaration reports from the recorded 2026-10-02 replay. The source-bound
`*_axioms.txt` files bind each module's complete SHA-256 and compiler output.
Run `python scripts/verify_finite_derivations.py --lean /path/to/lean-4.33.1`
from the paper directory to recheck them and the combined import spine.
This does not require Mathlib and is not part of the default historical root.

That recorded package contained 57 `.lean` sources (the lakefile, root and 55
modules), including this independent spine. Claim coverage is stated in
`claim_map.md`: 29 exact theorem rows, one exact definition row, and partial or
absent whole-row bindings elsewhere. The register at that revision had no open rows;
the five separate Genesis bridge obligations remain open.

## Historical Mathlib-backed receipt

Everything below records the 2026-09-30 replay against its then-current source
set. Its counts, open-row statuses and hashes are historical. They do not
describe the enlarged package or certify later edits. The default `lake build`
and `AxiomReport.lean` retain this 202-selected-theorem audit surface; they do
not import the independent core-only spine above.

**Replay date:** 2026-09-30

The package now depends on Mathlib, so it was not built in place: on Windows
Lean's tools cannot open paths longer than 260 characters, and Mathlib's nested
build paths overflow at this package's depth (see `README.md`). The sources in
this directory were copied to `C:\lk\r\lean4` and the following commands were
run there:

```text
lake exe cache get
lake build
```

Both exited 0. `lake exe cache get` unpacked the Mathlib build from the local
cache (no download), and `lake build` completed 8734 of 8734 jobs, including
every module of this package. `axiom_report.txt` was then written by
`capture_axiom_report` in `verify_deposit.py` (the function that
`scripts/capture_axiom_report.py` calls), with the copy as its package root.
It ran `lake build WitnessedDifference.AxiomReport`, which printed one report
for each of the 202 selected theorems, all within the whitelist.
`verify_deposit.py --lean` checks that the packaged file equals a fresh
capture; on Windows it has to be run from a short-path copy of the package.

## Pinned environment

- Lean: `4.33.1`, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`
- Lake: `5.0.0-src+819816b`
- Mathlib: `0df444a360eaa60ab8c11dca51a86af692955474`, with the transitive
  pins recorded in `lake-manifest.json`. `ClassicalCorner.lean`,
  `EmpiricalModel.lean` and the five modules of the quantum route
  (`ClassicalPackage.lean`, `ToleranceAdapter.lean`, `Composition.lean`,
  `AmplitudeBridge.lean`, `InstrumentAdapter.lean`) import it directly and
  `PacketAdapter.lean` through `EmpiricalModel.lean`.

## Audited surface

- 29 Lean source files (1 package file, 1 root module, 27 modules in
  `WitnessedDifference/`);
- 341 theorem and lemma declarations across the package, counted as
  line-initial `theorem` or `lemma` declarations, including attributed ones;
- 202 selected theorem reports audited in `AxiomReport.lean` and
  `axiom_report.txt`;
- theorem-dependency union strictly within `{propext, Classical.choice,
  Quot.sound}`;
- zero `sorry`, `admit`, custom `axiom`, `opaque`, or `unsafe` declarations in
  this package's sources (the scan skips `.lake/` and `b/`).

The claim map covers all 154 canonical IDs exactly once: 29 exact theorem
bindings, 1 exact definition binding, 52 narrower or prose-only rows, 26
definition rows without an exact declaration, 19 open rows, and 27 nonclaims.
This partition is deliberately not a claim of 154 formalized theorems.

## Changes since the previous receipt

Five modules were added for the quantum route, all importing Mathlib
(100 declarations, 38 reports): `ClassicalPackage.lean` (`WDP-CH18-P07`,
`WDP-CH18-P08`), `ToleranceAdapter.lean` (`WDP-CH19-P06`, `WDP-CH19-P07`),
`Composition.lean` (`WDP-CH19-P08` to `WDP-CH19-P10`), `AmplitudeBridge.lean`
(`WDP-CH19-P11`, `WDP-CH19-P12`), and `InstrumentAdapter.lean` (`WDP-CH19-P13`,
`WDP-CH19-P14`). Ten of the eleven rows are exact bindings; `WDP-CH19-P13` is
narrower than its row (see `claim_map.md`). The five open rows of the route stay
open, with `L:partial` milestones. No existing module changed.

`WitnessedDifference/EmpiricalModel.lean` (48 declarations, 26 reports) and
`WitnessedDifference/PacketAdapter.lean` (9 declarations, 8 reports) were
added. They bind the new rows `WDP-CH19-P02` through `WDP-CH19-P05` through the
bundle theorems `measurement_packet_adapter`, `what_survives_the_adapter`,
`every_model_is_a_packet_image`, and `contextuality_is_a_missing_global_table`.
`EmpiricalModel.lean` imports only the Mathlib files it uses rather than all of
Mathlib. No existing module changed.

Earlier: `WitnessedDifference/ClassicalCorner.lean` was added (28 declarations, 18
reports). It is the first module to use Mathlib, and it binds the new rows
`WDP-CH18-P02` through `WDP-CH18-P05` through the bundle theorems
`nonnegative_weights_force_permutations`, `signed_weights_break_the_corner`,
`unitary_package_is_classical`, and `classical_corner_ends`. The toolchain
moved from `4.34.0-rc1` to `4.33.1` to match the Mathlib pin; every earlier
module builds unchanged on it. The placeholder scan in `verify_deposit.py` now
skips ignored directories, since `.lake/packages` holds Mathlib's own sources.

Earlier: `Obstruction.lean` and `ObserverResolution.lean` were added when the
primitive-axiomatics package was absorbed (46 declarations, 27 reports).
`PointedRelation.lean`, `ComplexGrowth.lean`, `Interference.lean`, and
additions to `Descent.lean` were added for six genesis-alpha papers (29
declarations, 23 reports). A binding review then added five bundle theorems
(`closure_ratio_signature`, `declared_family_order`,
`visible_classes_le_grammar`, `grammar_resolution_bound`, and
`pointed_relation_independence_fin`) so that each exact row cites one
declaration, and demoted `WDP-CH04-P03` and `WDP-CH04-P06` to narrower
bindings. `PROVENANCE.md` records the sources.

## Source custody

Key source hashes at replay:

| File | SHA-256 |
| --- | --- |
| `claim_map.md` | `7fb35eacfdabc2295393392114445942bfd285fa717ae7926c327687eab68d82` |
| `lake-manifest.json` | `b510cb9ab3ed40df18961c35e42d8200323c573aeef837790371829619eb4727` |
| `lakefile.lean` | `3be662ff411d6898353588db6e3f44ef73730fc2b2ee4c28da1795748ca27394` |
| `lean-toolchain` | `3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71` |
| `WitnessedDifference.lean` | `4c346f945f88cbf8b72c6b5b77145d4feb795ba405b9ccd235c9a7f3e14d1a92` |
| `WitnessedDifference/AmplitudeBridge.lean` | `f79384f95a7e40ef79b811bac420759e10fe14a6e5fc4a6adc721803fef8bd40` |
| `WitnessedDifference/AxiomReport.lean` | `45e865a1bef265e5ddc7d1faaee474d5f76344b3bd88b51d427d6b381d2e8b8e` |
| `WitnessedDifference/Boundaries.lean` | `7bfc5d3eb0250020dd92734904b0c479e53adb252f70dfac140ec72e5a74ef3e` |
| `WitnessedDifference/ClassicalCorner.lean` | `39bd730439833866e1b7fbcc2447a781e049fa97b96dfca26192065de650cd4e` |
| `WitnessedDifference/ClassicalPackage.lean` | `7c6ea42572903e2b4685ba2b5331e88037c5c5ba66473bd767b4280d8cfb5d11` |
| `WitnessedDifference/ComplexGrowth.lean` | `d4498f18026c76a2c58059864feb2238790ca87685160f34bd1bb5c0eabc72f6` |
| `WitnessedDifference/Composition.lean` | `f537e479ca3f5ab551855081a83ace36fe8c952dc25f18e3a9218f19639a5b41` |
| `WitnessedDifference/Core.lean` | `bd08fb973c8fd1b94b1b76e7f98801c264d719178904b15bcddde5693f2dbe96` |
| `WitnessedDifference/Descent.lean` | `06f7cc18fdbed3daf177f71300f15e5930fd87494b4d7d4275741c6da5c02a37` |
| `WitnessedDifference/Difference.lean` | `abfb3e960df69d6918e1d3a70a7e21466f4388f9a86ba8d3b7c581108b11e497` |
| `WitnessedDifference/EmpiricalModel.lean` | `e922d789bf8bf61d760b0bb2089805c375fe7c057764adf7132f8195477d5f6f` |
| `WitnessedDifference/History.lean` | `6f459972c8f30c66e56426536ef4aaa2d311824413bd49018151006f37479f72` |
| `WitnessedDifference/InstrumentAdapter.lean` | `2b1b2ca6fc05be538e5050ae77746c9d87d72d98f929fec619ec4ea6f9f410ad` |
| `WitnessedDifference/Interference.lean` | `a54c500fbbdbdfeb3ac20635d83aafb7769c80690d01376940e56d029ff6b190` |
| `WitnessedDifference/Measurement.lean` | `c706d9cb975117d887591d2180960e80a7756a4502705fda143977f55722f204` |
| `WitnessedDifference/Observer.lean` | `3f72931e70cf743db4b7a5b86bee85ba30d093aaa5ce3f0a1ee6cb17536b5ff1` |
| `WitnessedDifference/ObserverResolution.lean` | `f6370f844053f4d6b8330257d3769f94fcc679721827013120f1aec079cc0053` |
| `WitnessedDifference/Obstruction.lean` | `3d970ea9cc3ed97c56f7f002b31a96f5989e91bb2698f3785d887d9eb9369a22` |
| `WitnessedDifference/PacketAdapter.lean` | `3d6b236b2239d0e4fe6701b759a1faaed475defaea5c768c0b20a2b004d9b4a5` |
| `WitnessedDifference/PointedRelation.lean` | `2d36b5427b54767a391d0760ac563ea300c4e7381809c059610ad592bfa28fa5` |
| `WitnessedDifference/Probability.lean` | `6d7504e83609d7d6f0d877d9adcfda00012d048f4c4d3e45f13203906c631ba7` |
| `WitnessedDifference/QuantumImports.lean` | `6cff260525ac690f2cee6a8c6b0da565db64d70a671a00a9ffb2e90cd06ece7a` |
| `WitnessedDifference/Routing.lean` | `cd9087a9ef86a63ad055c7be4310ef2fbdba6f3470243cf6e16161f8bfc35e13` |
| `WitnessedDifference/SemiringTransport.lean` | `6d1e4e240c20a295404805e9e1403ea9879ad24226d4ba697a2cc83d8513315b` |
| `WitnessedDifference/Succession.lean` | `5713213024bcd74fdadfb0dd0895b5efb13b35cd198e6a0328f9ad83f0c93223` |
| `WitnessedDifference/Symmetry.lean` | `5cbc349795aa927aca9a850768d539bc478ab1cca8a7367b1f7458bed8260f90` |
| `WitnessedDifference/ToleranceAdapter.lean` | `abe26a0476952d63ce6b960eb206e74273042b5b1e2df4fc22339aa06bc7ce4f` |

`claim_map.md` changes whenever the claim map does, so its hash here describes
this replay only.

This is a local elaboration receipt, not hosted CI, a publication action, or a
mathematical audit of claims left open in `claim_map.md`.
