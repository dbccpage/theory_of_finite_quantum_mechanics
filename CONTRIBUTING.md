# Contributing

**AuthorityEffect:** None. This file describes a process. It adds no result.

> **On the use of AI.** Much of the code, proofs, prose and review in this repository is drafted by AI models and LLM coding agents (Claude, Gemini, Grok and others), directed and reviewed by the maintainer. That is the reason for the rules here, not an exception to them. Every claim must be backed by evidence a stranger can check: Lean proofs audited for axioms, exact computations, replay receipts and independent checks. Every code change carries a scored YAML contract and must clear the [acceptance rule](#acceptance-rule) below. Every status is reviewed statement against theorem by the overclaim gate. The same standard applies to every contributor, human or model, and to the maintainer. In practice it most often finds the work inadequate: AI-drafted claims are routinely narrowed in review (for example [#171](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/171) narrowed by [#176](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/176), and the campaign pull requests [#184](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/184), [#185](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/185) and [#187](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/187), recorded as Narrowed results), and we publish those corrections. This project is not here to promote unverified claims, speculation presented as result, or pretension. If something here overstates what is proved, that is a bug: please report it with a [bug report](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/issues/new?template=bug_report.yml) or a [derivation review](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/issues/new?template=derivation_review.yml).

This repository records how far finite, exact constructions reach toward quantum mechanics, and where structure has to be supplied from outside. Each step is a node in a derivation graph with a status label and the evidence for it. You can help in three ways. None of them needs the maintainer's permission to start.

| Way | What you do | Skills | Time |
|---|---|---|---|
| [1. Run an example prompt](#1-run-an-example-prompt) | Run a prepared, bounded prompt on a small finite node and submit the record. | Python, a command line, optionally an API key | 15 to 45 minutes, usually under 0.10 USD |
| [2. Attempt a campaign target](#2-attempt-a-campaign-target) | Try to derive an open node in Lean, with an independent check and a prose derivation. | Lean 4 and Mathlib, or a precise paper proof and SymPy | Days; one pull request per target |
| [3. Review](#3-review) | Read a node, its Lean file, its independent check and its derivation note, and report what you find. | Mathematics or physics background; Lean is useful but not required | 1 to 3 hours per node |

Reviews are the most useful contribution at present. A reviewer who finds a statement that says more than its proof does is doing the project a service.

## Acceptance rule

**Governed code requires a YAML contract and a completed L4-or-higher score with composite grade D or higher, except for explicitly authorized, exact-source support exceptions.** The terms are defined in [`SCORING.md`](SCORING.md). The full walk-through, with a real example contract and the commands, is on the wiki page [How to Contribute](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/wiki/How-to-Contribute).

- **The score.** Every source or formal artifact receives one capability level (`L1` to `L5`) and one engineering grade on the scale `E < D < C < B < A < A+` ([§1](SCORING.md#1-overview-core-principles--scoring-calculus)). The token is written `L<level><grade>`, for example `L4C`. The grade is the minimum over the five gates G1 to G5, so one failing gate bounds the whole file ([§1.2](SCORING.md#12-the-fail-closed-weakest-link-rule)).
- **The floor.** Capability level L4 or L5, **and** composite grade D or better, unless an exact-source support exception applies. Without such an exception, rejected: any score at L1, L2 or L3 (for example `L3B`), and any score with grade E at any level (for example `L4E`, a demonstrated defect such as a float cast in an exact path or a hidden `sorryAx`; see the calibration scenarios in [§7](SCORING.md#7-calibration-scenarios--decision-ledger-18-scenarios)).
- **Reviewed finite-proof exceptions.** The current policy lists 76 explicitly authorized exact `lean4/Campaign*.lean` source hashes under `finite_proof_example`. They retain their assessed L1–L3/D scores. Only the listed path and digest receive the exception; changed bytes lose it. Grade E and incomplete scores remain rejected. This does not promote a node status or establish its original broad target. The first 31 pins are recorded in `dag/research/approved_finite_proof_exceptions_2026_10_25.json` and `dag/research/approved_pr_373_finite_proof_exception_2026_10_25.json`. The five subsequent approvals are recorded in `dag/research/approved_*_exception_2026_10_25.json` for the Witten, Kitaev, Laughlin, report-fiber and information-product campaign modules. Nine further approvals from the subsequent PR review are recorded in `dag/research/approved_round2_finite_proof_exceptions_2026_10_25.json`. The later PR #390 approval is recorded in `dag/research/approved_pr_390_finite_proof_exception_2026_10_25.json`. The later PR #391 approval is recorded in `dag/research/approved_pr_391_finite_proof_exception_2026_10_25.json`. The later PR #392 approval is recorded in `dag/research/approved_pr_392_finite_proof_exception_2026_10_26.json`. The 2026-10-26 open-PR review integrates twenty-seven independently reviewed finite-proof pins from PRs #393–400 and #402–420 under the human-authorized exact-hash mechanism; levels remain L1–L3/D and original broad obligations remain open.
- **Unassessed is not accepted.** When no assessed gate is a demonstrated failure, a gate with no evidence leaves the composite grade `null` and no token is issued ([§1.4](SCORING.md#14-missing-evidence-vs-demonstrated-failure-the-unassessed-discipline)). A known grade E stays on the record when other gates are unassessed (§7 scenario 4 is `L3E`). Either shape is rejected by this floor.
- **The contract.** Every code addition or change carries a contract/score companion, `<name>.contract.score.yaml`, next to the source file. It is bound to the SHA-256 of the exact bytes you submit, so changing the source means updating the companion. Pull requests say which companion files they add or change and the score token of each (the [pull request template](.github/pull_request_template.md) has a line for it).
- **How it is checked.** For the files this change adds or edits, run `python -I -X utf8 scripts/score_scope_contracts.py check --changed-since origin/main` and `python -I -X utf8 scripts/contract_scores.py check --changed-since origin/main`. Both use the merge base of that ref and include ordinary untracked files. They exit 0 when every added or edited source under `code/` or `lean4/` has a companion bound to its current bytes, and that companion's stored history matches those bytes. A change that adds or edits no such source exits 0. Neither command writes a file or reads the L4/D floor. The floor is checked by `governance-check` (see [`governance/README.md`](governance/README.md)), which the `governance` workflow runs in enforce mode on every pull request, and which every `cargo build` runs on its own package as a warning. A passing check still does not mean the grades are deserved: the maintainer reads them against the evidence you cite. Without `--changed-since` the same commands scan the whole tree; sources listed in `governance/baseline.json` with unchanged bytes are reported there but do not fail, and `score_scope_contracts.py check` writes `evidence/contract_score_coverage_scope_audit.json` only when given `--write-audit`. Do not repair unrelated companions in a change.

The rule applies to code added or changed from now on. It does not rescore existing code, most of which carries only an explicitly incomplete baseline score. Proofs and DAG changes also follow the [honesty rules](#honesty-rules) below, which apply in addition.

## Setup

- Python 3.11 or later. Install the DAG tooling with `pip install pyyaml` and the declared independent-check dependency with `pip install -r checks/independent/requirements.txt`. Add `pytest` to run the test suites and `anthropic` only if you will use the Anthropic tiers of the ladder.
- Run every repository script as `python -I -X utf8 path/to/script.py` from the repository root. The `-I` flag keeps stray files in the working directory from being imported.
- Lean 4.35.0 (through [elan](https://github.com/leanprover/elan)) and Mathlib `v4.35.0` are needed **only** for Lean work. The pins are in [`lean4/lean-toolchain`](lean4/lean-toolchain) and [`lean4/lake-manifest.json`](lean4/lake-manifest.json). A full Lean build is large; download the Mathlib cache with `lake exe cache get`.
- Rust (stable, with Cargo) is needed only to run the Rust certifiers in [`code/rust/`](code/rust).
- Orientation: read the [README](README.md), then [`dag/derivation_dag_reading_note.md`](dag/derivation_dag_reading_note.md). The current counts and recent changes are on the generated status page, <https://dbccpage.github.io/theory_of_finite_quantum_mechanics/status/>, which the daily workflow publishes once GitHub Pages is enabled; you can build the same pages locally with `python -I -X utf8 scripts/build_status.py --write` (they are not committed). Per-node evidence pages are in [`docs/evidence/`](docs/evidence/README.md), generated by `dag/evidence/build_evidence.py`.

## 1. Run an example prompt

[`docs/contribute/example_prompts.md`](docs/contribute/example_prompts.md) lists seven small, finite nodes. For each it gives the exact command, what a valid result looks like and how to check it yourself. The tool is the PFP LLM ladder in [`dag/pfp/llm_ladder/`](dag/pfp/llm_ladder) (design: [`DESIGN.md`](dag/pfp/llm_ladder/DESIGN.md)).

What a run does, and what it does not do:

- The ladder compiles a short packet from the node, sends it to a model, and asks for typed slots: generators, relations, compositions, lemmas, near misses and open obligations.
- **The reply is an untrusted proposal.** The host program checks every claim it can: that a cited declaration exists at the cited place, that a number recomputes exactly, that a Lean skeleton elaborates when Lean is available. Refused claims are kept as negative entries so that later calls do not repeat them.
- `accepted` means that enough claims passed these host checks. It does **not** mean that the mathematics is right or that the node's status should change. Prompt-result pull requests never change a node's status.

Steps. The commands below use the node `DFM-BPHZ-SECTOR-KERNEL` as the worked example; **replace it with the id of the node you chose, and `alice` with your GitHub handle**. Do not type angle brackets into a shell: `<` is redirection.

1. Fork the repository and create a branch, for example `git switch -c community/alice/dfm-bphz-sector-kernel`.
2. Preview the packet and the cost. This needs no key and makes no call:
   ```
   python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node DFM-BPHZ-SECTOR-KERNEL --stage P0 --max-cost-usd 0.10 --max-tier 1 --dry-run
   ```
3. Provide your own key for the provider you want to use, in the environment or in a git-ignored `.env` file. The tool reads `GROQ_API_KEY` and `OPENROUTER_API_KEY` (free models are available on both) and `ANTHROPIC_API_KEY` (paid). Never print, commit or paste a key.
4. Run it. Point the budget ledger at a file outside the repository, here the parent directory:
   ```
   python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node DFM-BPHZ-SECTOR-KERNEL --stage P0 --max-cost-usd 0.10 --max-tier 1 --ledger ../tfqm-ledger.json
   ```
   `--max-cost-usd` is a hard cap on all paid calls in the run. `--max-tier 0 --max-cost-usd 0` uses free models only. The command prints a JSON summary and exits with 0 for `accepted`, 3 for `accepted_partial`, 4 for `skipped_ungroundable` and 1 for anything else.
5. You may instead do it by hand: paste `system_prompt` and `user_prompt` from the node's file in [`dag/prompts/`](dag/prompts) into any model, and record the reply as a run folder (the example page shows how).
6. **Submit only your own run folder.** A ladder run edits two shared files as a side effect, the negative-entry index `dag/operads/_hallucination_index.json` and, unless you used `--ledger`, the budget ledger `dag/pfp/llm_ladder/budget_ledger.json`. Do not commit them; the maintainer integrates them after review:
   ```
   git restore dag/operads/_hallucination_index.json dag/pfp/llm_ladder/budget_ledger.json
   git status
   ```
   `git status` should list only the new folder under `dag/results/DFM-BPHZ-SECTOR-KERNEL/runs/`.
7. Check the result yourself (the example page has a node-specific SymPy check), then open a pull request. Use the pull request template. State the outcome class **Prompt result**, and say plainly what the run did not establish.
An unsuccessful run is a result. Submit it if it taught you something: a wrong claim that the host caught, or a node that has nothing to ground.

## 2. Attempt a campaign target

The derivation campaign ranks the open and conditional nodes that have never had a non-ladder run, and gives a per-target protocol: [`dag/pfp/campaign/README.md`](dag/pfp/campaign/README.md) (pull request [#180](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/180)). In outline:

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
   python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict
   python -I -X utf8 scripts/score_scope_contracts.py check --changed-since origin/main
   python -I -X utf8 scripts/contract_scores.py check --changed-since origin/main
   ```
   `build_status.py --check` rebuilds the generated status pages in memory, compares them with any copy on disk, and fails if a generated file is committed (it needs the full git history, not a shallow clone).
   The two `--changed-since` commands look only at sources this change adds or edits. They do not read the grade floor and they do not write `evidence/contract_score_coverage_scope_audit.json`.
   A change to the DAG also runs the sync scripts in the order given in the reading note and the campaign protocol.
2. **Scope check.** Does the pull request change only what it says? A prompt-result pull request adds only one run folder under `dag/results/<node id>/runs/`. It does not touch the shared index `dag/operads/_hallucination_index.json`, the budget ledger or any node status; the maintainer integrates those after review.
3. **Statement-versus-theorem table.** The maintainer reads it against the Lean declarations. This is the step that decides whether a status may change.
4. **Independent review.** For anything that changes a node, the maintainer asks a reviewer (see [`REVIEWING.md`](REVIEWING.md)) to read the statement, proof and prose. The outcome is recorded.
5. **Merge.** The maintainer merges. Review is by one person on a best-effort basis; there is no service-level promise. A pull request that overstates its result is asked to narrow it, not rejected. Code that does not meet the [acceptance rule](#acceptance-rule), including its explicitly authorized source exceptions, is not merged until it does.

## Questions and problems

- A possible error in a node, a proof or a script: open a *Bug report* or *Derivation review* issue.
- A result of a prompt run you do not want to put in a pull request: open a *Prompt result* issue.
- Support for the research is welcome but never required: [Buy Me a Coffee](https://buymeacoffee.com/ooutwire).

The separately reviewed PR #421 adds one exact finite-group Pachner proof pin at L3D. Its explicitly revised finite-group statement alone is PROVED_LEAN; general triangulation, Regge and physical claims remain outside scope. Current authority is recorded in dag/research/current_review_pr421_finite_proof_authority_2026_10_26.json.

The human also approved 33 exact-source maintenance pins (18 bounded implementations and 15 harnesses), retaining completed L2/L3D scores. See the [exact authority and list](evidence/quality/code_2026_10_26/approved_scoped_exceptions_20261026.json) and [governance limits](governance/README.md). Unlisted/changed hashes, grade E and incomplete scores remain blocked; the global L4/D floor and baseline are unchanged. Native/publication failures are not waived.

PR #433's exact Lean proof hash retains L3D and the original OPEN target under the user's explicit approval of the DFM and LQG proof pins. This branch applies only the DFM pin; PR #434 carries the other source. The independent checker is outside the governed source population and needs no exception. The conditional infinite-limit result uses the existing technical category without asserting mathematical finiteness. See the [verbatim authorization](dag/research/approved_pr_433_continuum_exception_2026_10_26.json) and [integration scope](docs/maintenance/pr433_integration_scope.md).

PR #434 applies the other exact Lean hash from the user's two-proof approval, retaining L3D and the original LQG OPEN target. The supplied-family probability extension does not derive physical LQG continuum data. See `dag/research/approved_pr_434_continuum_exception_2026_10_26.json`.
