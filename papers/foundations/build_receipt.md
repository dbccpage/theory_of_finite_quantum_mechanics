# BUILD_RECEIPT — fable_hilbert_walk_20260819

**AuthorityEffect:** None. A receipt describes commands and bytes;
it is not a mathematical verdict.

A second external adversarial review (2026-08-19, verified at the
first campaign commit) requested changes before merge: it caught a
false "different coordinate count" claim in H014, over-strong
"unitary" and "ℚ inadmissible" language, and that the capstone is
a conjunction of witnesses rather than one threaded object. All
were applied: H014 corrected to an entanglement-witness + open
non-forcing boundary; H006 reframed as isometry / positive-definite
automorphism with `permU_isometric_automorphism_over_posdef`; the ℚ
boundary deflated to a priced import (not an impossibility); a
genuine cross-rung thread `HWThread.phaseBlind_intertwines` added;
full threading named open residue R0; trailing whitespace and the
paper-audit self-containment boundary fixed.

A THIRD review round (2026-08-19) requested further changes: the
H001 code header still claimed ℚ "inadmissible" (now deflated to a
priced import, matching the docs); the H013 Born claim overstated
non-uniqueness (the quartic rival totals 17 vs the quadratic's 5 —
no shared normalization contract, so reframed to a positive
non-proportional rival with same-contract non-uniqueness marked
open O-6); the "all ten obligations discharged" claim was too
strong (now an honest per-obligation status: 7 direct theorems, #6
host-weakened to Int, #9/#10 as named imports — FRONTIER); the
ImportLedger is labelled metadata, not a theorem-bound gate; a
stale `sum_always_splits` header reference fixed; and this custody
manifest added.

A FOURTH review round (2026-08-19) requested: the PR *description*
(edited on GitHub) to match the corrected obligation status, ℚ
framing, and G1 replayability; H013's residual "same interface"
language and its `two_effect_rules_differ := true` flag (no
effect-bearing rule exists — set to false); the H017 headline to
stop asserting the licensed connected presented-carrier capstone
(reframed as a conjunction of witnesses); the general degenerate-
form isometry to stop being called "unitary" (theorem
`permutation_unitary` → `permutation_isometry_envelope`, yaml and
prose updated; the module filename retains the work-order rung
name); the manifest upgraded to a genuine import closure; and this
module count corrected (21, not 20). The build remains green within
`{propext, Quot.sound}` (sole exception: the disclosed ratPack
receipts).

A FIFTH review round (2026-08-20) found that the round-4 manifest
bound the campaign import closure but not 18 additional sources that
produce the recorded COMPLETE `J011Admitted` axiom report. The
manifest now binds the union of both recorded build targets. It also
pins bytewise C-locale ordering, retracts the remaining H001/H006/
H017/HWThread scope overclaims, and labels all hand-set Bool ledgers
as metadata rather than theorem gates or countermodels.

The earlier round-2 receipt was regenerated late on 2026-08-19,
after (a) the 37-agent paper audit delivered paper_claim_map.md and
(b) a 7-agent adversarial verification pass whose findings were applied
(new theorems: gramStd_pos_def, gramWeighted_pos_def,
permU_left_inverse, permU_right_inverse, psi2_not_scalar_multiple,
mutation_descent_restored, pair_linear_effect, pair_linear_state,
quartic_not_proportional, mutant_is_phase_stripped; extended
finite_hilbert_boundary conjunction; per-law Rat axiom receipts;
prose corrections across all documents). An earlier revision of
this receipt listed paper_claim_map.md while it was still being
rendered; this revision describes observed bytes only.

## Custody — binding this receipt to exact sources

A prior review round correctly noted this receipt recorded only a
base SHA and "dirty", which cannot bind the build/axiom claims to a
specific tree. Round 4 then covered only the campaign's import
closure, despite this receipt also recording the complete
`J011Admitted` build and axiom report. **`source_manifest.txt`** now
binds the union of both targets: all 21 campaign modules, all 27
`J011Admitted` roots, `lakefile.lean`, and `lean-toolchain` (50
entries). Imports of both targets stay inside those Lean sources.
The remaining fixed external is the Lean stdlib/prelude, pinned by
the hashed `lean-toolchain`. The two build results and every
`axiom_report.txt` line below are determined by exactly those bytes.

- **Aggregate closure SHA-256:**
  `b4eb12d7b8196b34e209c65e7b9664ad051719fb1fe46d1eb7c235ed4737dda2`
  (recompute per `source_manifest.txt`).
- The campaign commit SHA is in git log / PR #56 — a receipt
  committed *with* its tree cannot contain its own commit hash, so
  the manifest binds the content instead; the commit SHA binds the
  content to a point in history.

## Original campaign revision and dirty state

- Repository: `dbccpage/CODA`, worktree branch
  `claude/sync-remote-main-worktree-5fad0e`
- Base revision: `94b6657606d20d6d4bb1786d2690ebf79a6506d4`
  (= `origin/main` at run time)
- Dirty state at receipt time (full disclosure):
  - `M lean4/genx/lakefile.lean` — added the
    `FableHilbertWalk20260819` lean_lib (additive; no existing
    target's roots changed)
  - `?? lean4/genx/_work_review_queue/fable_hilbert_walk_20260819/`
    — this campaign folder (all new files)
- No estate paper was modified. Paper 0
  (`coda_university/coda_research/002_projection_obstruction/000_projection_obstruction/projection_obstruction.md`)
  SHA256 before and after the run:
  `fb7d2436f1e5da5969c8c4d9b1a143b4a2a0ba8024748568733f4290414d701e`
  (byte-identical — gate G3).

## Toolchain

- `elan`-managed Lean `leanprover/lean4:v4.32.2`
  (from `lean4/genx/lean-toolchain`)
- Lake version 5.0.0-src (bundled with the toolchain)
- No mathlib, no external `require`: the genx package is
  self-contained Lean core.

## Commands and results

From `lean4/genx/`:

1. `lake build J011Admitted`
   — Hour-1 trunk gate (G2). Result: **Build completed successfully
   (29 jobs)**. All `#print axioms` outputs within
   `{propext, Quot.sound}` or axiom-free. The admitted roots
   contain only `Core`, `B*`, `E*`, `J001`, `J011`: no C/D
   cohomology, no F Banach, no G observer, no I quantum modules.
2. `lake build FableHilbertWalk20260819`
   — the campaign library. Result: **Build completed successfully
   (32 jobs), zero errors** (21 campaign modules plus replayed trunk
   deps). Warnings present: unused-simp-arg lints (HWKernel, H005,
   H006, H016).
   The campaign lib is a `@[default_target]`, so bare `lake build`
   cannot stay green while these files are unrooted.
3. Axiom disclosure: see `axiom_report.txt` (generated from both
   build replays' `#print axioms` output; gate G7).

## File inventory (this folder)

| file | role |
|---|---|
| `HWKernel.lean` | coefficient packs, Enum, rsum calculus (support) |
| `H000_finite_presented_carrier.lean` | rung H000 |
| `H001_probability_simplex.lean` | rung H001 |
| `H002_report_dynamics.lean` | rung H002 |
| `H003_reversibility_gate.lean` | rung H003 |
| `H004_free_linearization.lean` | rung H004 |
| `H005_inner_product_admission.lean` | rung H005 |
| `H006_permutation_unitary.lean` | rung H006 |
| `H007_complexification.lean` | rung H007 |
| `H008_phase_blind_presentation.lean` | rung H008 |
| `H009_phase_fiber.lean` | rung H009 |
| `H010_interference_non_descent.lean` | rung H010 |
| `H011_u1_selector_boundary.lean` | rung H011 |
| `H012_operator_algebra_shadow.lean` | rung H012 |
| `H013_born_pairing_boundary.lean` | rung H013 |
| `H014_tensor_composition_boundary.lean` | rung H014 |
| `H015_irreversible_fork.lean` | rung H015 |
| `H016_continuous_dynamics_fork.lean` | rung H016 |
| `H017_finite_hilbert_boundary.lean` | rung H017 (assembly) |
| `HWThread.lean` | genuine cross-rung thread (phase-blind equivariance) |
| `HilbertWalkAll.lean` | admitted root |
| `source_manifest.txt` | SHA-256 of build inputs (custody binding) |
| `hilbert_walk.md` | lift-by-lift account |
| `hilbert_walk.yaml` | invariant/import/nonclaim records |
| `paper_claim_map.md` | audit of QM_020/060/061/062/121, 200–211 |
| `countermodel_register.md` | separators and receipt witnesses per non-forced lift |
| `axiom_report.txt` | printed axioms, gate G7 |
| `build_receipt.md` | this file |
| `frontier.md` | strongest theorem, residues, next experiments |

## What this receipt does not certify

A green build proves elaboration, not that prose and theorems
match, and not any physical claim. `AuthorityEffect: None.`
