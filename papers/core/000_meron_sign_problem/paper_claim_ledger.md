# Claim Ledger: A Lexically Filtered Meron-Cluster Benchmark

Version 0.4.0, 2026-09-28. Manuscript: `paper.md`. Paths are relative to the
package root. Each row states the narrowest claim the evidence supports. Tests
run from the package root with `py -3.12 -m pytest code/tests/<file> -q`.

| ID | Claim | Status | Evidence |
|:--|:--|:--|:--|
| MSP-01 | For one orbit with unit weight, if some cluster is a meron the signs sum to 0 (Lemma 2.4). | Lean theorem | `MeronCharacter.meron_orbit_cancels`; pairwise form `MeronClusterInvolution.meron_pair_exact_cancellation` |
| MSP-02 | For one orbit with unit weight and no meron, the signs sum to $2^k$ (Lemma 2.5). | Lean theorem | `MeronCharacter.zero_meron_orbit_positive` |
| MSP-03 | One orbit sums to 0 if it has a meron and to $2^k$ otherwise (Theorem 2.6 per orbit). The factor $W_0(g)$ and the sum over graphs are not mechanized. | Lean theorem, scoped | `MeronCharacter.compression_preserves_partition` |
| MSP-04 | A weight-preserving, sign-reversing involution has no fixed point, whatever the weight. | Lean theorem | `MeronClusterInvolution.no_fixed_points_when_sign_reverses`, `MeronClusterInvolution.fixed_point_contradiction` |
| MSP-05 | The fixture (four sites, two repetitions, $q = 3$) has 256 graphs, 1,296 configurations, 192 negative, 57 cancelling graphs, 199 graphs without a meron, $Z = 912$, $Z_{\mathrm{abs}} = 1{,}296$ and average sign 19/27. Every orbit of the 57 sums to 0 and the 199 others sum to 912. | Exact computation | `test_meron_cluster_solution.py::test_oracle_ground_truth_invariants`; `test_meron_cluster_solution.py::test_orbit_exact_cancellation_on_odd_cycle_subgraphs` |
| MSP-06 | An occupation-basis transfer-matrix trace, computed without clusters, also gives 912. | Exact computation | `test_meron_cluster_solution.py::test_cluster_sum_matches_independent_transfer_trace` |
| MSP-07 | On the fixture, Assumptions 2.1 and 2.2 hold: weights are constant on orbits and the sign is the product of single-flip signs. | Exact computation | `test_meron_cluster_solution.py::test_fixture_satisfies_character_law_and_equal_orbit_weights` |
| MSP-08 | The filter rejects text containing any of twelve substrings, and all five prompt builders pass it. It is a substring filter; the prompts keep other sign-problem vocabulary. | Tested behavior | `test_meron_cluster_solution.py::test_lexical_hygiene_blocks_all_forbidden_tokens`; `test_meron_cluster_solution.py::test_all_five_prompt_arms_pass_lexical_hygiene` |
| MSP-09 | The retained record lists 22 calls to five models, one run per model and arm, with the scores of Table 2; its SHA-256 digest is recorded in `receipt.json`; the estimated spend of 0.01496 USD uses configured prices and is not billed. | Retained record | `test_pilot_evidence.py::test_recorded_call_ledger`; `test_pilot_evidence.py::test_recorded_scores_by_arm`; `test_pilot_evidence.py::test_receipt_digest_matches_report` |
| MSP-10 | Re-scoring the twelve retained single-turn answers with the current scorer reproduces every recorded score. The rubric checks values and keywords, not derivations. | Tested behavior | `test_pilot_evidence.py::test_recorded_scores_reproduce_under_package_scorer`; `test_meron_cluster_solution.py::test_positive_control_scores_perfect`; `test_meron_cluster_solution.py::test_hallucination_mutation_mines_antibodies` |
| MSP-11 | No cell of Arms 1 to 3 passed (0 of 9). Their prompts do not state 912 or 199, but state 1,296 and 19/27, which fix $Z = 912$, and state the property to be proved; the four listed samples have no odd-winding cycle. | Retained record and tested prompts | `test_pilot_evidence.py::test_recorded_scores_by_arm`; `test_pilot_evidence.py::test_unassisted_prompts_state_quantities_that_fix_z`; `test_pilot_evidence.py::test_sample_subgraphs_in_prompts_have_no_odd_cycles` |
| MSP-12 | GLM 5.3 Flash in Arm 2 wrote $Z = 912$ under the key `Z`, outside the schema, and scored 0. | Retained record | `test_pilot_evidence.py::test_glm_arm2_answer_used_keys_outside_the_schema` |
| MSP-13 | Arm 4 feedback states "Z must equal 912" and the 57/199 split; the Arm 5 prompt as run also states the sign formula and the cancellation step. Every passing run had such a prompt. | Tested prompts | `test_pilot_evidence.py::test_arm4_corrections_state_the_target`; `test_pilot_evidence.py::test_arm5_prompt_as_run_states_target_and_method` |
| MSP-14 | The Arm 3 prompt has 1,124 characters against 4,320 for Arm 1 because it omits the narrative and the configuration lists. | Tested prompts | `test_pilot_evidence.py::test_arm3_prompt_is_shorter_because_it_omits_content` |
| MSP-15 | The anonymous model's retained output records no model, prompt, parameters, latency or score; it re-scores 4 of 4 but does not conform to the schema; its counts 57 and 199 come only from correction strings. The result cannot be reproduced. | Retained record, not reproducible | `test_space_bunny.py::test_retained_record_fields`; `test_space_bunny.py::test_retained_output_scores_four_of_four`; `test_space_bunny.py::test_retained_output_does_not_conform_to_schema`; `test_space_bunny.py::test_counts_in_output_come_only_from_guard_text` |
| MSP-16 | The harness dry run makes no network call, and the budget guard refuses a request whose configured-price bound exceeds the ceiling. | Tested behavior | `test_meron_cluster_solution.py::test_dry_run_executes_safely_without_spend`; `test_meron_cluster_solution.py::test_budget_guard_blocks_over_ceiling` |
| MSP-17 | Language models discovered the cancellation mechanism, or prompt formats and feedback enabled discovery. | Withdrawn | Contradicted by MSP-11 and MSP-13 |
| MSP-18 | Prompt compression reduced latency to 1.6 s. | Withdrawn | The retained Arm 3 cell for Llama 3.3 70B scored 0 after 3,000 tokens (133.7 s); latency is not attributable to the prompt |

## Scope notes

- MSP-01 to MSP-04 concern lists of signs and abstract involutions. The Lean
  files do not import the SQL fixture, and no proof connects them.
- MSP-05 to MSP-07 concern one fixture. They say nothing about other models,
  sizes or couplings.
- MSP-09 to MSP-15 describe one pilot run with $n = 1$ per cell, decoding
  parameters not recorded per request, and no pre-specified analysis. They
  support no comparison between arms or models.
- The rerun described in Section 6 of the manuscript requires authorized live
  API calls and has not been made.

## 2026-10-02 finite witness extension

The historical ledger above retains its source revision and scope. The current
local preprint candidate is version 0.1.0 dated 2026-10-02.

| ID | Claim | Status | Evidence |
|:--|:--|:--|:--|
| MSP-19 | Four selected orbits at q=5/2 form a reproducible witness task with complete input data, opaque public case IDs, no supplied computed aggregate answers, and exact pair/count/partition checks. | Finite tested task | `code/witness_benchmark.py`; `code/tests/test_witness_benchmark.py`; protocol in `docs/witness_benchmark.md` |
| MSP-20 | The host positive control succeeds with zero provider calls. It is not a model trial. | Offline execution scope | Dated local run receipt; `code/run_witness_benchmark.py` |
| MSP-21 | A cocycle evaluates equally on cycles differing by a boundary. This does not construct a Meron-to-cochain map. | Conditional algebra and open transport obligation | Section 8.1 and chain/cochain definitions in Hatcher Section 3.1 |
| MSP-22 | Withdrawn. The only committed `results.json` is `docs/witness_host_control_2026_10_02/results.json`, mode `host_positive_control`, with `provider_calls` 0 and `provider_usage` null. The token counts, reported cost, and omission quote are not in that file. | Withdrawn | Host-control receipt; no live-trial receipt is in this package |
| MSP-23 | Withdrawn as stated. `MeronClusterInvolution.lean` mechanizes an abstract sign-reversing, weight-preserving involution for one pair. It does not define $\tau(s) = s \oplus e_{j^*}$, an $O(2^k)$ synthesis, packet URNs, GIN inverted mode, or a terminal repair route. The cited packet file is absent. | Withdrawn | `lean4/MeronClusterInvolution.lean` |
| MSP-24 | `meron_database(6, 2, "3")` returns 4,096 graphs, 33,396 configurations, 192 negative configurations, 4,024 zero-meron graphs (72 with a positive meron count), signed and reduced partitions 33012, and transfer trace 33012. | Exact computation on one fixture | `code/tests/test_meron_cluster_solution.py::test_six_site_q3_census_matches_transfer_trace`; Section 6.2 |
| MSP-25 | Under The Symbol Game Proposal Fidelity Protocol (PFP) with DDC cycle spectra and host antibody guards, four models across parameter tiers (Space Bunny Alpha, Llama 3.3 70B, Llama 3.1 8B, GLM 5.3 Flash) score 4 of 4 against BlindClusterOracle on the 4-site fixture. Supported by certified receipts in `code/results/` and `demos/results/`, runnable offline via `demos/code/demo_4site_symbol_game.py` and `code/tests/test_symbol_game_pfp_ladder.py`. This 4-of-4 score does not discharge MSP-11, MSP-13, or MSP-17. MSP-11 and MSP-13 record that prompts contained quantities that fix \(Z = 912\). MSP-17 is Withdrawn. | Certified empirical trial | `demos/code/demo_4site_symbol_game.py`; `code/tests/test_symbol_game_pfp_ladder.py`; `code/results/certified_4site_ladder_results.json` |
| MSP-26 | On the 6-site fixture (4,096 breakup graphs, 33,396 configurations), blind DDC multi-meron loop identification detects the 72 cancelling subgraphs (each having exactly 2 merons) and 4,024 surviving subgraphs without prior sector counts, and the GIN posting index pairs all 384 cancelling states into 192 sign-inverting doublets, reproducing Z = 33,012. Supported by `demos/code/demo_6site_scaling_gin.py` and `code/tests/test_symbol_game_6site_pfp.py`. | Exact computation and witness synthesis | `demos/code/demo_6site_scaling_gin.py`; `code/tests/test_symbol_game_6site_pfp.py`; `code/results/certified_6site_scaling_results.json` |
| MSP-27 | The Discrete Deformation Calculus (DDC) 5-stage solution generation pipeline emits an append-only DAG in JSON Lines with explicit `LIFT_REQUEST` / `LIFT_GRANT` mechanics and pure $\Gamma_{38}$ wire encoding ($\Sigma_{36} \cup \{<, >\}$), reproducing exact repair $Z = 912$ (4 sites) and $Z = 33{,}012$ (6 sites) under strict zero-smuggling lexical hygiene (`assert_lexical_hygiene`). Supported by `code/symbol_game_stage_controller.py`, `demos/code/demo_multistage_symbol_game.py`, and `code/tests/test_symbol_game_stage_controller.py`. | Exact computation and protocol verification | `code/symbol_game_stage_controller.py`; `demos/code/demo_multistage_symbol_game.py`; `code/tests/test_symbol_game_stage_controller.py`; `demos/tests/test_demo_multistage_dag.py` |
| MSP-28 | Concrete physical sign-factorization and involution witnesses are demonstrated on finite 2D and 3D lattices (Sections 6.5 and 6.6); continuum scaling and doped regimes remain open. | Tested finite models; continuum open | Section 8.2; `demos/code/demo_2d_gross_neveu_meron.py`; `demos/code/demo_3d_meron_string_linking.py` |
| MSP-29 | The coached prose runner retains raw responses for future runs. The retained multi-turn record is a synthetic model-labelled fixture; provider latency, usage and discovery rates are unverified. | Tested runner; illustrative fixture | `demos/code/demo_multiturn_interactive_pfp.py`; `demos/tests/test_demo_multiturn_interactive.py` |
| MSP-30 | The deterministic host recomputes Z=912 and the independent transfer trace. The revised four-site inputs are wire-only; offline responses are supplied fixtures with LlmTurn transport bindings. Live acceptance requires the expected packet. | Finite host computation and protocol check | `demos/code/demo_pure_symbolic_meron.py`; `demos/tests/test_demo_pure_symbolic.py` |

| MSP-31 | The retained three-model summary contains four expected wire examples per model but lacks raw provider responses, complete requests and source bindings. Reported latency, usage and discovery rates remain unverified; packet syntax alone is replayable. | Unverified retained summary; packet examples | `demos/results/certified_pure_wire_ladder_results.json`; `demos/tests/test_demo_pure_symbolic_ladder.py` |

Any live outputs of the new task must be reported from their own source-bound
receipts. They do not repair the historical discovery pilot or support model
comparisons from one trial.

## Six-site replay and release scope

| ID | Claim | Status | Evidence |
|:--|:--|:--|:--|
| MSP-32 | On the specified six-site fixture, the host enumerates 4,096 graphs and 33,396 configurations, pairs 384 cancelling states into 192 doublets, and independently obtains partition and transfer trace 33,012. Offline wire replies are supplied fixtures. Live replies pass only when both pure and equal to the expected packet; complete raw provider responses are retained. | Bounded host computation and checked transport; no model discovery claim | `demos/code/demo_pure_symbolic_6site.py`; `demos/tests/test_demo_pure_symbolic_6site.py` |
| MSP-33 | The package manifests and deterministic ZIP can be checked locally. Retained phase signoffs are authored assertions, and do not establish an independent approval, external deposit, DOI or publication. | Local inventory checks; authority effect None | `verify_deposit.py`; `tools/rebuild_release.py`; scoped phase receipts in `docs/evidence/` |
| MSP-34 | For repetitions 2 and $q=3$, the bridge stores $Z(4)=912$, $Z(6)=33012$, and $Z(8)=973824$. A three-point Neville extrapolation on $L\in\{4,6,8\}$ has a midpoint that agrees with 1.69411 through four digits, and the $L=4$ log-density width is below $10^{-18}$. The log-densities are not monotone, and the check does not include $L=12$. | Finite recorded traces and one extrapolation test | `omega_engine_projects/finite_to_continuum/code/meron_wilsonian_bridge.py`; `omega_engine_projects/finite_to_continuum/tests/test_meron_wilsonian_bridge.py`; Section 6.5 |
| MSP-35 | On a 2D staggered Gross-Neveu lattice on $T^2$ (8 sites, 4 bond graphs, 16 occupation states), exact cluster breakup identifies 2 odd-winding meron graphs whose 8 states cancel pairwise under flip involution $\tau$, yielding exact zero sign sum ($Z_{\mathrm{odd}} = 0$) and positive partition sum $Z = 150$, matching the independent transfer matrix trace $Z = 150$. | Exact computation on finite 2D lattice | `demos/code/demo_2d_gross_neveu_meron.py`; `demos/tests/test_demo_2d_gross_neveu.py`; Section 6.5 |
| MSP-36 | On a 3D periodic lattice $T^3$ (8 sites, 12 links), closed meron loop configurations are classified by 3D winding parity vector $\mathbf{W} \in (\mathbb{Z}_2)^3$ and Gauss linking numbers $\operatorname{Lk}(c_1, c_2) \in \mathbb{Z}$. Reversing the orientation of odd-winding string loops induces an exact weight-preserving sign-reversing involution $\tau$ cancelling all 4 odd-winding configurations pairwise to 0, yielding $Z = 310$. | Exact computation on finite 3D lattice | `demos/code/demo_3d_meron_string_linking.py`; `demos/tests/test_demo_3d_meron_string.py`; Section 6.6 |
| MSP-37 | The OpenRouter multi-turn model ladder benchmark on the 2D meron cluster problem evaluates frontier models across 4 stages in pure $\Gamma_{38}$ wire format. Under zero-smuggling lexical hygiene (`assert_lexical_hygiene`), mock/cached ladder runs score 4 of 4 with 0 syntax errors, certified in `demos/results/certified_2d_meron_benchmark_receipt.json`. | Certified empirical benchmark trial | `demos/code/bench_openrouter_meron_2d.py`; `demos/tests/test_bench_openrouter_meron_2d.py`; Section 6.7 |

<!-- BEGIN UNIFIED-DAG-BACKLINKS -->
<!-- Generated by papers/core/tools/build_corpus_dag_backlinks.py; edit the tool, not this region. -->

## Unified DAG

Audit of 2026-10-21. The unified derivation DAG (`dag/fragments/unified_dag.json`) folds the records of this corpus into one graph: a record with no trunk counterpart is a NEW application-branch node with its own TFQ record; a restatement of a trunk step is an ALIAS row that points to the trunk node. *Source claimed* is the status the source asserted; *Audited* is the status the audit assigned against what is actually in this checkout (Lean declarations resolved, replays rerun, statements compared). The original claims, labels and text of this document are kept unchanged. A status below the source claim means the claim is not established as stated; it does not mean the underlying mathematics is false (only REFUTED means that). For an ALIAS row the audited column is the status of the trunk node, which is the authority for the restated step. Regenerate with `python -I -X utf8 papers/core/tools/build_corpus_dag_backlinks.py`. This package backs the FSP register record(s) FSP-DERIV-028; only those rows are listed here, the full table is in `papers/core/fsp/`.

0 NEW records and 1 ALIAS rows.

| Source id | Kind | TFQ record | DAG node | Source claimed | Audited | Reconciliation |
|---|---|---|---|---|---|---|
| `FSP-DERIV-028` | ALIAS | [TFQ-0407](../../../dag/derivations/26_fsp/tfq_0407_fsp_meron_character_cancellation.md) | `FSP-MERON-CHARACTER-CANCELLATION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |

<!-- END UNIFIED-DAG-BACKLINKS -->
