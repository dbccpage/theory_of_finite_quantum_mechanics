# Contributing

**AuthorityEffect:** None. This file describes a process. It adds no result.

This repository records how far finite, exact constructions reach toward quantum mechanics, and where structure has to be supplied from outside. Each step is a node in a derivation graph with a status label and the evidence for it. You can help in three ways. None of them needs the maintainer's permission to start.

| Way | What you do | Skills | Time |
|---|---|---|---|
| [1. Run an example prompt](#1-run-an-example-prompt) | Run a prepared, bounded prompt on a small finite node and submit the record. | Python, a command line, optionally an API key | 15 to 45 minutes, usually under 0.10 USD |
| [2. Attempt a campaign target](#2-attempt-a-campaign-target) | Try to derive an open node in Lean, with an independent check and a prose derivation. | Lean 4 and Mathlib, or a precise paper proof and SymPy | Days; one pull request per target |
| [3. Review](#3-review) | Read a node, its Lean file, its independent check and its derivation note, and report what you find. | Mathematics or physics background; Lean is useful but not required | 1 to 3 hours per node |

Reviews are the most useful contribution at present. A reviewer who finds a statement that says more than its proof does is doing the project a service.

## Setup

- Python 3.11 or later. Install the libraries the tools use: `pip install pyyaml sympy`. Add `pytest` to run the test suites and `anthropic` only if you will use the Anthropic tiers of the ladder.
- Run every repository script as `python -I -X utf8 <script>` from the repository root. The `-I` flag keeps stray files in the working directory from being imported.
- Lean 4.35.0 (through [elan](https://github.com/leanprover/elan)) and Mathlib `v4.35.0` are needed **only** for Lean work. The pins are in [`lean4/lean-toolchain`](lean4/lean-toolchain) and [`lean4/lake-manifest.json`](lean4/lake-manifest.json). A full Lean build is large; download the Mathlib cache with `lake exe cache get`.
- Rust (stable, with Cargo) is needed only to run the Rust certifiers in [`code/rust/`](code/rust).
- Orientation: read the [README](README.md), then [`dag/derivation_dag_reading_note.md`](dag/derivation_dag_reading_note.md). The current counts and recent changes are on the status page, [`docs/status/README.md`](docs/status/README.md). The per-node evidence pages are being built; see [the evidence map (in progress)](docs/evidence/README.md).

## 1. Run an example prompt

[`docs/contribute/example_prompts.md`](docs/contribute/example_prompts.md) lists seven small, finite nodes. For each it gives the exact command, what a valid result looks like and how to check it yourself. The tool is the PFP LLM ladder in [`dag/pfp/llm_ladder/`](dag/pfp/llm_ladder) (design: [`DESIGN.md`](dag/pfp/llm_ladder/DESIGN.md)).

What a run does, and what it does not do:

- The ladder compiles a short packet from the node, sends it to a model, and asks for typed slots: generators, relations, compositions, lemmas, near misses and open obligations.
- **The reply is an untrusted proposal.** The host program checks every claim it can: that a cited declaration exists at the cited place, that a number recomputes exactly, that a Lean skeleton elaborates when Lean is available. Refused claims are kept as negative entries so that later calls do not repeat them.
- `accepted` means that enough claims passed these host checks. It does **not** mean that the mathematics is right or that the node's status should change. Prompt-result pull requests never change a node's status.

Steps:

1. Fork the repository and create a branch, for example `community/<your-handle>/<node-id-lowercase>`.
2. Preview the packet and the cost. This needs no key and makes no call:
   ```
   python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node <NODE-ID> --stage P0 --max-cost-usd 0.10 --max-tier 1 --dry-run
   ```
3. Provide your own key for the provider you want to use, in the environment or in a git-ignored `.env` file. The tool reads `GROQ_API_KEY` and `OPENROUTER_API_KEY` (free models are available on both) and `ANTHROPIC_API_KEY` (paid). Never print, commit or paste a key.
4. Run it. Keep the budget ledger out of your pull request by pointing it at a file outside the repository:
   ```
   python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node <NODE-ID> --stage P0 --max-cost-usd 0.10 --max-tier 1 --ledger <path-outside-the-repo>/ledger.json
   ```
   `--max-cost-usd` is a hard cap on all paid calls in the run. `--max-tier 0 --max-cost-usd 0` uses free models only. The command prints a JSON summary and exits with 0 for `accepted`, 3 for `accepted_partial`, 4 for `skipped_ungroundable` and 1 for anything else.
5. You may instead do it by hand: paste `system_prompt` and `user_prompt` from the node's file in [`dag/prompts/`](dag/prompts) into any model. The example page shows how to record such a reply.
6. Check the result yourself (the example page has a node-specific SymPy check), then open a pull request. Use the pull request template. State the outcome class **Prompt result**, and say plainly what the run did not establish.

An unsuccessful run is a result. Submit it if it taught you something: a wrong claim that the host caught, or a node that has nothing to ground.

## 2. Attempt a campaign target

The derivation campaign ranks the open and conditional nodes that have never had a non-ladder run, and gives a per-target protocol: [`dag/pfp/campaign/README.md`](dag/pfp/campaign/README.md) (added by pull request [#180](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/180); if the link does not resolve yet, that pull request is not merged). In outline:

- One target, one pull request. Take targets in rank order, or tell the maintainer which one you are taking by opening an issue, so that two people do not do the same work.
- Every outcome that is proved is a result: **Derived** (the full statement is proved from the admitted primitives), **Reduced** (it is proved from a strictly weaker named assumption), **Refuted** (a countermodel shows the import is needed) or **Narrowed** (a precisely stated special case is proved).
- Deliverables in the same pull request: one Lean module with `#print axioms` lines; a replay receipt; an independent check, a SymPy or plain-Python script that does not import repository code; a derivation note that starts with `Status: AI-drafted, awaiting human review.` if a model drafted it; and the DAG update through the owning fragment.
- The pull request body carries the statement-versus-theorem table described below.

If you do not use Lean, a precise paper derivation with an independent SymPy check is still useful as a **proposal**: open a pull request or an issue with it, labelled `campaign-target`, and say that it has no Lean proof. It will be recorded as a proposal, not as a result.

## 3. Review

Read [`REVIEWING.md`](REVIEWING.md). In short: choose a node (the example list and the issue label `review-needed` are good places to start), read its statement, its Lean declaration, its independent check and its derivation note, and open a *Derivation review* issue with a verdict on the statement, the proof and the prose. The maintainer records it, and you are credited in [`docs/reviewers.md`](docs/reviewers.md) if you wish. A review does not need a pull request.

## Honesty rules

These apply to every contribution. They are the reason the project keeps its labels low.

1. **A model's answer is an untrusted proposal.** Acceptance belongs to a host check on the original bytes, never to a model's statement about itself.
2. **Statement versus theorem.** Say exactly what the Lean declaration states, and compare it claim by claim with what the node states. Where it states less, say so. The pull request template has the table.
3. **No promotion without the full statement.** A node becomes `PROVED_LEAN` only if a Lean declaration states its full statement and compiles with only `propext`, `Classical.choice` and `Quot.sound`. A lemma with the target's name is not enough, and neither is `decide` over one small instance. When unsure, narrow the statement. Never raise a status on thin evidence.
4. **Exact arithmetic.** Certificates use integers, rationals, Gaussian rationals and explicit algebraic extensions. A floating-point number is never a certificate. Every number in prose must be recomputed by something in the pull request.
5. **No `sorry`, `admit`, `axiom`, `native_decide` or `unsafe`** in added Lean.
6. **Say what is imported and what is open.** Assumptions that are supplied rather than derived are named as such. A finite check is not a statement about the continuum.
7. **Negative results count.** A counterexample, a refuted claim or a precise obstruction is a result. Report it as plainly as a success.
8. **Plain language.** Avoid words that claim more than the evidence does (`proves` for a conditional step, `guarantees`, `obviously`, `flawless`). The DAG validator refuses a list of them. State what was checked and with what.
9. **No secrets.** Never commit or print a key or the contents of a `.env` file.

## How a pull request is reviewed

1. **Automated and mechanical checks.** The maintainer (or you, beforehand) runs the checks the change calls for. Typical ones, from the repository root:
   ```
   python -I -X utf8 dag/validate_derivation_dag.py --no-files      # must print failures=0
   python -I -X utf8 scripts/build_readme_facts.py --check
   python -I -X utf8 scripts/build_status.py --check
   ```
   A change to the DAG also runs the sync scripts in the order given in the reading note and the campaign protocol.
2. **Scope check.** Does the pull request change only what it says? A prompt-result pull request touches only the run folder under `dag/results/<NODE>/runs/` and the shared hallucination index `dag/operads/_hallucination_index.json`, and no node status.
3. **Statement-versus-theorem table.** The maintainer reads it against the Lean declarations. This is the step that decides whether a status may change.
4. **Independent review.** For anything that changes a node, the maintainer asks a reviewer (see [`REVIEWING.md`](REVIEWING.md)) to read the statement, proof and prose. The outcome is recorded.
5. **Merge.** The maintainer merges. Review is by one person on a best-effort basis; there is no service-level promise. A pull request that overstates its result is asked to narrow it, not rejected.

## Questions and problems

- A possible error in a node, a proof or a script: open a *Bug report* or *Derivation review* issue.
- A result of a prompt run you do not want to put in a pull request: open a *Prompt result* issue.
- Support for the research is welcome but never required: [Buy Me a Coffee](https://buymeacoffee.com/ooutwire).
