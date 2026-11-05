# Migration record, distinct-image closure

AuthorityEffect: None. Date: 2026-10-05.

No live derivation file was deleted. The merge with current main moved the
live Gate E checker to
`wdp_research_sources/code/gate_e_exact_counterexample.py` and moved the
corrected locality and Trotter derivations under `wdp_research_sources/`.
Locality replay hashes the unified Lieb–Robinson derivation only through the
progress snapshot. It hashes
`wdp_research_sources/code/gate_e_exact_counterexample.py`,
`code/trotter_characteristic_polynomials.py`, and
`lean4/WitnessedDifference/CARResponseWitness.lean` directly. The archive
`bytes/` tree keeps the imported directory names, including
`bytes/g3_g4_meron_field_theorems/`. The older directory
`docs/source_archive/locality_and_smearing/` holds the original submitted
drafts, not these corrected bytes.

Canonical destinations:

- Distinct-image theorem WDP-DIM-1: Appendix T of `witnessed_difference_programme.md`.
- Chapter 23 corrections WDP-CH23-P01C and the later correction identifiers: Appendix U. The imported Chapter 23 text keeps its old identifiers.
- Accepted L1–L4 proofs: Appendix V.
- Accepted T1–T4 proofs and the Gate E boundary: Appendix W.
- Executable checkers: `code/observer_completion/distinct_image.py`, `code/observer_completion/distinct_replay.py`, and the added functions in `code/toric_code_observer_completion.py`.
- Lean encoding: `lean4/WitnessedDifference/DistinctImageCompletion.lean` and `ToricSyndromeCorrespondence.lean`.

The Gate E receipt bytes in this archive match the live receipt. They were copied, not regenerated. `gate_e_exact_counterexample.py` was not executed.

Targets 2–5, guarded-history coherence, unrestricted source refinement, physical reconstruction, and joint continuum foundations remain open.

Correction appended after the first delivery. Appendix U no longer states that, for \(1\le t\) and \(2t<L\) with \(B=S\), separation holds if and only if the stabilizer checks have rank \(2L^2-2\). Full rank stays sufficient. The \(L=3\) face rows \(\{0,1,3,5,7,8\}\) and the \(L=4\) deletion of syndrome rows \(1\), \(10\), and \(16\) are the counterexamples, and the matroid hypothesis for that regime is withdrawn. The distinct-image checker accepts `lower_columns` only as an obstruction basis. The archived chapter bytes in `bytes/` are the imported source and were not rewritten to match this correction. The Gate E receipt was not regenerated.
