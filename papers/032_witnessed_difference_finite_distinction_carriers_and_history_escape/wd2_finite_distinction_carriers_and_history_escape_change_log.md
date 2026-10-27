# Change log — Finite Distinction Carriers and History Escape

## 2026-10-09 — Finite checker and the horizon fixed-point law

This is not a new Zenodo deposit and does not change the published version.

- Elaborated WD2-T1 in `lean4/FiniteDistinction.lean` as `Wd2.related_refl`,
  `Wd2.related_symm`, `Wd2.related_trans`, `Wd2.related_mono`, and
  `Wd2.related_stable`, with no `sorry`.
- `Wd2.sharp_m5_bound` records the five-state chain at horizon 3.
- `code/finite_distinction.py` evaluates the sharp chain, the update-stable
  pair, and the factored-report instance. The tests call that module.
- The general class-count bound and Theorems WD2-T3, WD2-T4, WD2-T5, and
  WD2-T6 are not Lean theorems in this package. WD2-T2's general bound and
  WD2-T6 are non-claims of this package. The finite profiles stay in the ledger.
- The manuscript headings for WD2-T2 through WD2-T6 now say classical record.
  The prose arguments stay visible. They are not theorems of this package.
  Version unchanged. No new DOI.
- The abstract, verification scope, README, quick start, description, and
  reading notebook name that limit. They no longer say that the package has
  no Lean binding and no theorem tests.
- Reproduction entry:
  `py -3.12 verify_deposit.py --test code/tests/test_proved_rows.py --lean`.
  This does not mint a DOI or change version 1.1.0.

## 1.1.0 — 2026-10-08

Status: author-review prose preprint; not an external publication.

- Replaced conflicting released/proposal metadata with this single status.
- Corrected the refinement equation, finite output assumption, positive
  escape depth, and left-to-right composition convention.
- Wrote the proof of L1 and the proofs of T1–T4, including the fixed-point
  argument, strict-round bound, and first-symbol/suffix witness construction.
- Assigned the largest-congruence/minimal-quotient result the distinct
  identifier T6 and supplied its factorization proof.
- Completed T5 under an explicit sufficient endpoint-profile factorization
  hypothesis, with report timing and a counterexample without that hypothesis.
- Added a sharp-bound family, a noncommuting example, and empty-state,
  empty-alphabet, and zero-output-bit cases.
- Replaced the unrelated cochain inventory and internal workflow terminology
  with the objects used in the proofs. Cited classical automata sources and
  disclaimed novelty for the refinement and quotient results.
- Retired the obsolete proposal ledger, code/Lean maps, and development
  receipt from the public package; the proofs are now in the manuscript.
  Earlier versions remain recoverable from Git history.
- Removed the unreadable PNG and the skipped placeholder test. Replaced
  the deliberately failing notebook with a prose-only reading guide.
- Corrected the metadata-only Python project; no missing library is declared.
  Added canonical packaging utilities, TeX/PDF, manifests, and a dated archive.
  No mathematical implementation or Lean verification is claimed.
- Preserved the existing text and launcher licenses, and retained the
  source license of the newly copied template packaging utilities.

## Historical records

- 2026-07-25 (v0.2.0): recorded a claim-namespace change and an appended
  maximal-congruence statement. The claimed Lean locator was unavailable;
  this entry is history, not evidence of a binding.
- 2026-07-25 (v0.1.0): initial proposal.
- The prior package also displayed v1.0.0 / RELEASED without completing
  the proposal proofs. That label is superseded by the status above.
