# PO-000 Lean 4 sources

## v6.9.14 canonical trace addition (2026-10-11)

The current scoped target contains `Po000JordanLie.lean`,
`Po000JordanLieImage.lean` and `Po000JordanTrace.lean` on the same pinned
Lean 4.34.0 / Mathlib v4.34.0 toolchain below. The trace module constructs
`trace(a) = Tr_R(L_a)` and `form(a,b) = trace(a ∘ b)` from real bilinear
operations. Derivation and signed associator identities imply trace
compatibility and the Peirce polynomial. Finite real orthogonal idempotent
spectral witnesses then imply positive definiteness. An inner product is
not a premise. The scalar model supplies an inhabitant.

Its nine `#print axioms` reports use only
`{propext, Classical.choice, Quot.sound}`. These complement the original
seventeen E.1 reports. The module does not construct the spectral witnesses
from primitive distinctions, supply operational states/effects, or prove
E.7 or the full operational classification. Historical source statuses below
are unaffected. The current build and source hashes are recorded in the
external `po000_research_qualification_2026-10-11.json` receipt adjacent to
this package.

## v6.9.1 E.1 bridge (2026-10-08)

The original scoped Lake target contained
`Po000JordanLie.lean` and `Po000JordanLieImage.lean`. It is separate from
the historical mirror and standalone checks below. That target was built
with Lean **4.34.0** and Mathlib **v4.34.0**, commit
`5ed2965256430c3649e86755f9576b54eca72435`.

Use an existing checkout of that Mathlib revision with its dependencies
installed and built. From this directory:

```bash
MATHLIB_NO_CACHE_ON_UPDATE=1 lake -Kmathlib=/absolute/path/to/mathlib4 update
MATHLIB_NO_CACHE_ON_UPDATE=1 lake -Kmathlib=/absolute/path/to/mathlib4 build
```

The Lake file overrides Mathlib and its eight transitive packages with local
paths, so the scoped build does not clone a second dependency tree. The
generated absolute-path `lake-manifest.json` and `.lake/` build cache are
excluded from Git and the deposit. A missing dependency is a build failure;
the package does not include Mathlib's source or binaries. In this cloud
environment the remote Mathlib cache was unavailable, so the required
dependencies were built from source.

`Po000JordanLie.Data` assumes a complex inner-product space with conjugation,
two complex-bilinear operations, and the complexified displayed B1 identities.
Associativity, the anti-multiplicative involution, faithful multiplicative
left representation, adjoint identity and positive squares are derived.
The scalar model `scalarData` inhabits the assumptions. The second module
derives a closed finite-dimensional complex C*-image, its self-adjoint
elements, and equality of its positive cone with finite sums of self-adjoint
Jordan squares. The reverse inclusion uses Mathlib's proved continuous
functional calculus, without an assumed square-root closure conclusion.

The 17 trailing `#print axioms` reports use only
`{propext, Classical.choice, Quot.sound}`; there is no `sorry`, `admit`, or
custom kernel axiom. This is conditional verification of the specified
complexified interface. The real-to-complex construction in Lemma E.1 and
the E.2–E.5 block and operational classification remain written proofs.
The Pauli checks are examples, not classification certificates.

## Historical mirror and build reports

**Package mirror:** `coda_atlas/F004_papers/002_projection_obstruction/000_projection_obstruction/lean4/`

An earlier revision of this line named
`coda_university/.../published_papers/002_projection_obstruction/000_projection_obstruction/lean4/`.
**Withdrawn** 2026-09-03: no `published_papers` tree exists anywhere in the
repository, so that pointer resolved to nothing. The path above is where the
package actually is.

The two locations are byte-identical for every shared file — re-verified
2026-09-03 by `cmp` across all 17 shared files (17 identical, 0 differing).
The estate additionally carries `projection_obstruction.lean`, a true-scaffold
overview file, which also compiles standalone (exit 0).

When first written this claim was **false**: `manifest.json` differed between
the two copies, each naming a different and nonexistent `published_papers`
root. Both were repaired on 2026-09-03 to the package's real location, which
restored byte-identity rather than weakening the claim. Re-check with:
`cmp <estate>/<file> <package>/lean4/<file>` over the shared set. The package `lean4/` folder is a mirror for deposit self-containment;
neither location then had its own Lake project. The scoped v6.9.1 target above
does not change the historical files or revalidate those reports. This README matches
`manifest.json` in this directory; earlier revisions of this README named a
retired `research_programs/004_projection_obstruction/` lake home, a
`sprint-oe-paper-004` sprint, a `PaperPO000` lake target and namespace, and a
"flat paths are retired" rule that contradicted this directory's own layout.
All of that is **withdrawn**: the flat `po000_*.lean` files below are the
current sources, the namespaces are the ones in the files
(`ReplicaHierarchy`, `ProjectionTransfer`, `PO000.*`, ...), and `PaperPO000`
does not exist in this estate.

## v6.4 arithmetic addition (2026-10-06)

`po000_short_time_jets.lean` is a new package-local file, not part of
the historical shared-file comparison above. It uses `import Std` and
was compiled directly with Lean 4.34.1. All ten declarations print their
axiom dependencies: seven use `propext`, and the three concrete
constants use none. No `sorry` or custom axiom is used.

It checks rising support factors and Taylor normalization, including
24, 64 and 160. It does not formalize commutator norm inequalities,
Taylor's analytic theorem, infinite-volume dynamics or the density limit.
The historical statuses below were not revalidated as a whole-package build.

## How the historical files were checked

Each file is compiled **standalone** against the pinned `mathlib_lab` package
(toolchain `leanprover/lean4:v4.34.0-rc1`, local Mathlib):

```bash
cd lean4/mathlib_lab
lake env lean <absolute path to file>.lean
```

There is **no green historical whole-package build context**: the old lake
home is retired, and the two files that import sibling modules
(`po000_core.lean`, `po000_axiom_audit.lean`) therefore compile **nowhere**
at present. That is recorded honestly below rather than papered over. Because
the aggregator has no green build, every claim-bearing file carries its own
trailing `#print axioms` block.

## Per-file build status (all 16 files; verified by actual compile, 2026-08-31)

Status legend: **GREEN** = standalone `lake env lean` exit 0;
**PACKAGE-CONTEXT-ONLY** = imports sibling modules, no current green build
context exists; **BROKEN** = does not compile as written in any current
context.

| File | Status | `#print axioms` reports | Claims / role |
| --- | --- | --- | --- |
| `po000_l001_replica_hierarchy.lean` | GREEN | 2 (propext, Classical.choice, Quot.sound) | D2, D5 |
| `po000_l001_projection_transfer.lean` | GREEN | 4 (propext, Classical.choice, Quot.sound) — own block added 2026-08-31 | E8 |
| `po000_l002_affine_obstruction.lean` | GREEN | 1 (no axioms) | **LEAN_TOY** residual; not full C1 |
| `po000_l003_double_commutator_estimates.lean` | GREEN | 5 (within allowed set) | E4-commutator — **arithmetic factors only**; the commutator inequalities are a structured hypothesis record, and `second_deriv_from_double_factor` is `rfl` |
| `po000_l003_double_commutator_rate.lean` | GREEN | 2 (within allowed set) | **LEAN_TOY** residual; not the E4 quantum bound |
| `po000_l003_second_deriv_bound.lean` | GREEN | 2 (within allowed set) | E4-second |
| `po000_l004_observer_visibility.lean` | GREEN | 14 (within allowed set) | H3--H9: §7.4, 7.4.7-B, §7.4.10 |
| `po000_l005_weighted_hierarchy.lean` | GREEN | 7 (within allowed set) | D3, D4 singleton cores; D6 instances |
| `po000_paper_constants.lean` | GREEN | 2 (within allowed set) | paper constants arithmetic |
| `po000_projection_factor.lean` | GREEN | 4 (no axioms) | finite experiment; not D2/D5/E8, not Thm 5.1 |
| `po000_authorization_boundary.lean` | GREEN | 5 (no axioms) | report-factorization obstruction; not T1 |
| `po000_eval_auth_factor.lean` | GREEN | 6 (no axioms) | finite evaluation-authority experiment |
| `po000_core.lean` | PACKAGE-CONTEXT-ONLY | none | import hub; **no current green receipt** |
| `po000_axiom_audit.lean` | PACKAGE-CONTEXT-ONLY | 13 blocks, never currently elaborated | legacy aggregator; **no current green receipt**; superseded by the per-file blocks |
| `po000_beyond_paper_advancements.lean` | **BROKEN** | none | parked draft: has no `import` lines yet uses `Real`, `Real.log`, `positivity`, `linarith`, `nlinarith`; fails standalone with unsynthesized instances and unknown tactics. **Not claim-bearing**: absent from both claim ledgers. Kept, labelled, unrepaired by policy (record status honestly; do not silently fix or silently ship). |
| `projection_obstruction.lean` (estate copy only) | GREEN | none | true-scaffold overview; its header states it proves nothing |

"Within allowed set" means every report lies within
`{propext, Classical.choice, Quot.sound}`. No `sorry` or `admit` appears in
any file (text scan and kernel check).

## Residual honesty

- **Aggregator gap, closed for E8:** `po000_axiom_audit.lean` was the only
  audit surface for `po000_l001_projection_transfer.lean`, and it does not
  compile anywhere at present; E8's axiom report was therefore uncovered by
  any green receipt. Fixed 2026-08-31 by giving the transfer file its own
  trailing block (compiled: exit 0, 4 reports, all within the allowed set).
- **l004 / l005 (v6.3):** the §7.4 observer-visibility layer (including the
  7.4.7-B necessity refutation and the §7.4.10 quotient witness) and the
  Theorem 4.2 weighted/orbit singleton cores are Lean theorems under
  `PO000.ObserverVisibility` and `PO000.WeightedHierarchy`. Each supports
  only the exact finite statement it mechanizes; nothing quantum, nothing
  §3, no adapter.
- **l002 / l003 toys:** header `RESIDUAL_HONESTY` banners; the ledger keeps
  C1/E4 as non-Lean discharge.
- No `PROVED_IN_LEAN4_AND_PYTHON` marketing from this directory.
