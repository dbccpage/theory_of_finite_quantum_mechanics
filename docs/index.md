# Theory of Finite Quantum Mechanics

Can quantum mechanics be built from a finite, exact substrate, starting from a single inert mark, and where exactly must continuum or other extra structure be imported? This repository answers that question one step at a time. Each step is a node in a derivation graph, recorded as derived, conditional on named hypotheses, imported, refuted or open, with the evidence for that label. The project does not claim to derive quantum mechanics. It records how far finite constructions reach and names every structure that has to be supplied from outside.

Current counts, recent changes and open pull requests: [where the project stands](status/README.md). A short digest of each day's changes: [daily digests](status/daily/index.md).

## What is proved, what is imported, what is open

- **Proved, with exact scope.** Some nodes are kernel-checked in Lean 4 against Mathlib: for example a finite exact Wigner theorem over the Gaussian rationals, a sector-form inner-product uniqueness result, and a Born-rule result for effect-additive valuations on rational matrices. The scope of each is part of its statement and is usually narrower than its name. Several earlier claims were lowered when review found them too strong. The record is in the [README](https://github.com/dbccpage/theory_of_finite_quantum_mechanics#selected-results-with-exact-scope) and in [How claims are kept honest](https://github.com/dbccpage/theory_of_finite_quantum_mechanics#how-claims-are-kept-honest).
- **Imported.** Structure that the finite construction does not produce is supplied and named: the complex field, local tomography, the transition-probability law, an unbounded supply of fresh marks, and others. These are nodes with status `IMPORTED_ASSUMPTION`, or `CONDITIONAL` when a result holds only under them. They are assumptions, not results. The list is in [the status tables](status/README.md#nodes-by-status).
- **Open.** Born and Gleason uniqueness without a supplied carrier, selection of the scalar field and of the uniformity, Stone's theorem and continuous time, the U(1) circle, endogenous unbounded supply, the maximum number of mutually unbiased bases in dimension six, and a finite Regge/Schläfli target. The list, with node ids, is in [Open problems: help wanted](https://github.com/dbccpage/theory_of_finite_quantum_mechanics#open-problems-help-wanted).

A status label is only as strong as its evidence. `PROVED_LEAN` means a named Lean declaration exists and the source cites it. `COMPUTATIONALLY_CHECKED` means an exact finite computation exists, which is not a proof of a general statement.

## Verify it yourself

- **The evidence map (in progress):** per-node pages with the statement, the Lean declaration, the independent check and the derivation note are proposed in [pull request #181](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/181) and will be linked here when it is merged.
- **Reproduce the checks.** The commands for the DAG validator, the three-language parity checks and the Lean build are in [Reproduce it](https://github.com/dbccpage/theory_of_finite_quantum_mechanics#reproduce-it). The shortest check is `python -I -X utf8 dag/validate_derivation_dag.py --no-files`, which must report `failures=0`.
- **Read the method.** [`dag/derivation_dag_reading_note.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/derivation_dag_reading_note.md) explains how the graph is built and what the validator does and does not check.

## Help

- **Run a prompt.** Small finite nodes, a command that costs a few cents or nothing, and a check you can run yourself: [example prompts](contribute/example_prompts.md).
- **Attempt a target.** Open nodes ranked by how much depends on them, with a per-target protocol: [`CONTRIBUTING.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/CONTRIBUTING.md).
- **Review.** If you are a mathematician or physicist and can read one node critically, see [`REVIEWING.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/REVIEWING.md). Reviewers are credited in [the reviewer list](reviewers.md).

## Support

The research is independently funded. If you want to support it, you can [buy me a coffee](https://buymeacoffee.com/ooutwire). It is never required for a contribution or a review.
