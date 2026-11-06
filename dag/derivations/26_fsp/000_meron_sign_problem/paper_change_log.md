# Change Log: A Lexically Filtered Meron-Cluster Benchmark

Manuscript: `paper.md`. Package: `omega_engine_projects/fsp/meron_sign_problem/`.
Entries are newest first. Earlier entries keep their original dates and describe
what was claimed at the time; version 0.4.0 withdraws or narrows those claims as
listed.


## [2026-10-03] 2D/3D Meron extensions and OpenRouter benchmark

- Added Section 6.5: 2D staggered Gross-Neveu meron cluster solver on $T^2$ ($Z = 150$, matching independent transfer trace; Claim MSP-35).
- Added Section 6.6: 3D closed meron string loops, winding parity $\mathbf{W} \in (\mathbb{Z}_2)^3$, and Gauss linking on $T^3$ ($Z = 310$; Claim MSP-36).
- Added Section 6.7: OpenRouter multi-turn model ladder benchmark on 2D meron clusters with pure $\Gamma_{38}$ wire format across Claude 3.5 Sonnet, GPT-4o, and Gemini 2.5 Flash (Claim MSP-37).
- Updated Section 8.2 with finite 2D/3D lattice scope and explicit continuum non-claims.
- Updated Claim MSP-28 to reflect tested finite 2D/3D models while keeping continuum scaling and doped regimes open.

## [2026-10-03] Wilsonian chain note

- Replaced the §6.5 continuum claim with the traces the bridge records: $Z(4)=912$, $Z(6)=33{,}012$, $Z(8)=973{,}824$. The three-point midpoint agrees with $1.69411$ through four digits. The note does not include $L=12$ or a width below $2.8\times 10^{-21}$.
- Retargeted MSP-34 at `meron_wilsonian_bridge.py` and `test_meron_wilsonian_bridge.py`.

## [0.1.0 PR review repair] — 2026-10-02

- Refused valid but wrong live packets and prose-wrapped replies; retained complete
  prompts and provider responses for future checks.
- Recomputed the four-site host partition and transfer trace; made offline replay
  read-only unless an output directory is explicitly selected.
- Removed automatic synthetic provider-record generation and withdrew empirical
  discovery, latency, token, pure-prompt, and concrete two-dimensional claims.
- Rebuilt the manuscript and complete pinned release package.

## [0.1.0 local candidate repair] — 2026-10-02

- Corrected the 4-site live prompt so `build_pfp_prompt_4site` passes `assert_lexical_hygiene`.
- Corrected the space-bunny ladder line to 1,380 completion tokens, 0 reasoning tokens, and a stored reasoning text of 3,692 characters.
- Regenerated `manifest.sha256`, `sha256sums`, and the deposit archive from the LF checkout.

## [0.1.0 local candidate] — 2026-10-02

- Added The Symbol Game Proposal Fidelity Protocol (PFP) model ladder evaluation
  on the 4-site fixture across four models (`stealth/space-bunny-alpha`,
  `meta-llama/llama-3.3-70b-instruct`, `meta-llama/llama-3.1-8b-instruct`,
  and `z-ai/glm-5.3-flash`), all scoring 4 of 4 against BlindClusterOracle.
- Added a dedicated `demos/` directory with `demos/code/`, `demos/tests/`, and
  `demos/results/`, enabling anyone downloading the paper deposit to replay the
  certified ladder receipts offline or execute live OpenRouter queries with their
  own API key.
- Verified blind DDC multi-meron loop identification and GIN inverted mode posting
  index partner pairing on the 6-site lattice (4,096 breakup graphs, 33,396
  configurations), identifying all 72 two-meron cancelling graphs without prior
  sector counts and pairing all 192 cancelling doublets in 2 milliseconds, matching
  the transfer matrix trace $Z = 33{,}012$.
- Added a multi-stage Discrete Deformation Calculus (DDC) solution generation
  controller (`code/symbol_game_stage_controller.py`) emitting an append-only
  Directed Acyclic Graph (DAG) in JSON Lines (`symbol_game_ddc_dag.jsonl`).
- Implemented explicit `LIFT_REQUEST` and `LIFT_GRANT` mechanics: when topological
  cycle sign obstruction ($\Phi_1 > 0$) is encountered, the model requests an involution
  lift, and the host grants/verifies the $\tau: s_i \mapsto -s_i$ coboundary map,
  annihilating the odd-winding sectors via $(1 + (-1)) = 0$.
- Implemented pure 38-character $\Gamma_{38}$ wire grammar encoding ($\Sigma_{36} \cup \{<, >\}$)
  across all stages without natural language or physics domain smuggling.
- Added standalone CLI demo `demos/code/demo_multistage_symbol_game.py` and unit test
  `demos/tests/test_demo_multistage_dag.py` verifying DAG causality, wire purity,
  and terminal exact repair.
- Added package test `code/tests/test_symbol_game_stage_controller.py` testing lexical
  hygiene, Gamma38 wire compliance, and partition recovery.
- Documented the multi-stage DDC DAG controller, topological lift grant protocol,
  and 38-character wire grammar in Section 6.4 of the manuscript.
- Added Section 8.2 extending the DDC loop formulation to 2D spatial lattices
  (3-torus $\mathbb{T}^3 = S^1 \times S^1 \times S^1$) where cycle winding numbers
  classify under the Klein four-group $\mathbb{Z}_2 \times \mathbb{Z}_2$, and
  spin-paired electronic loops at half-filling decompose into positive-definite
  or pairwise-cancelling multi-generator sectors (Claim MSP-28).
- Preserved every historical prompt, witness task, and retained pilot output.
- Aligned current candidate date metadata and regenerated derived artifacts
  after source changes. Historical receipts and release descriptions retain
  their dates; no publication or DOI is claimed.

## [0.4.0] — 2026-09-28

Author-review revision. The paper is rescoped from a discovery study to an exact
benchmark fixture, mechanized per-orbit lemmas, and a pilot whose passing runs
received the answer in the prompt.

### Changed

- Retitled from "Blind Recovery of Fermion Sign Cancellation via Topological
  Cluster Involutions and Epistemic Immune Decoding" to "A Lexically Filtered
  Meron-Cluster Benchmark: Exact Ground Truth, Mechanized Cancellation Lemmas,
  and a Pilot That Exposes Answer Leakage". Centered header block; version
  0.4.0; no horizontal rules.
- Section 2: Definitions 2.1 and 2.2 became Assumptions 2.1 and 2.2. Equal
  weights on an orbit is stated as a property of the model's cluster rules; the
  former justification ("because cluster components share no vertices or edges,
  configuration weight magnitudes are invariant") is withdrawn. The meron
  indicator is defined operationally instead of as a temporal winding index.
- New results table with an "Answer-bearing input? (yes/no)" column, built only
  from the retained files in `code/results/`, with the leaking strings quoted.
- The design fix for a valid rerun is stated (Section 6): task text that does not
  fix the target, feedback that names only the failed check, several trials per
  cell, fixed and recorded decoding parameters, and a pre-specified analysis.
- Code: the oracle now uses a vendored copy of the exact meron model
  (`code/meron_exact_model.py`, `code/meron_schema.sql`, from commit
  52cb5457f6c485ba548cfd292f6012a941ed22cf), so the package no longer imports
  files outside itself. Modules import their siblings directly; no repository
  path is added to `sys.path`.
- Code: `code/test_space_bunny.py` moved to `code/tests/test_space_bunny.py`. It
  no longer reads a `.env` file on import; its live probe is corrected so that it
  can run and is always skipped; offline tests check the retained output.
- Tests: the cancellation test now covers all 256 graphs instead of the first
  50 (which held 5 of the 57 cancelling graphs). New tests cover the independent
  transfer-matrix trace, the character law and equal orbit weights on the
  fixture, and every statement the paper makes about the retained run
  (`code/tests/test_pilot_evidence.py`).
- Lean: doc comments in `lean4/MeronClusterInvolution.lean` and
  `lean4/MeronCharacter.lean` now describe exactly what is proved; no statement
  or proof changed.
- Packaging: `pyproject.toml` pins ruff, pytest and mypy settings;
  `tools/compile_paper.py` reads the title, date and version from the
  manuscript and builds with XeLaTeX; release tools updated from the template.

### Withdrawn or narrowed

- "can discover the non-perturbative cluster cancellation mechanism ... without
  access to physics domain vocabulary": withdrawn. Every prompt states the
  property to be proved and quantities that fix $Z = 912$.
- "typed antibody constraints and DDC hieroglyphic factorization enable open
  models to deduce ... and recover ... Z = 912": withdrawn. Every pass followed
  a prompt that stated the answer; no unassisted cell passed (0 of 9).
- "Typed epistemic antibody mining effectively suppresses algebraic drift and
  forces rapid convergence": withdrawn. The feedback strings state the target.
- "This confirms that DDC hieroglyphic prompt compression and distractor masking
  are effective across reasoning model architectures": withdrawn.
- "DDC hieroglyphic factorization achieves up to 74% compression ... reducing
  inference latency down to 1.6s": narrowed to "the Arm 3 prompt is 74% shorter
  because it omits content". Latencies are client wall-clock times that differ
  across providers; no latency claim remains.
- Arm 3, Llama 3.3 70B, "2/4, 1.6 s, formulates gauge lift ...": not in the
  retained report, which records 0 of 4 (an empty JSON object after 3,000
  completion tokens, 133.7 s). The retained value is reported.
- Arm 4, Llama 3.3 70B, "outputs exact Z = 912 and 199 surviving sectors":
  narrowed to "scored 4 in round 2 after the prompt stated Z = 912 and the
  57/199 split"; the round-2 answer was not retained.
- Arm 4, DeepSeek V4 Flash, "3/4": narrowed to "scores 0, 0, 3, 0, 0 over five
  rounds; did not pass".
- Arm 5, Qwen 3.7 Max, "single-turn zero-shot convergence": narrowed to "scored
  4 with a prompt that stated the answer and dictated the method".
- stealth/space-bunny-alpha, Arm 5, "zero-shot single-turn convergence ... valid
  JSON conforming to the schema with a perfect 4/4": narrowed. The retained file
  records no model, prompt, parameters, latency or score; the answer re-scores 4
  of 4 but does not conform to the schema; its prompt was answer-bearing; the
  committed probe script could not have produced the file; the result cannot be
  reproduced.
- stealth/space-bunny-alpha, Arm 1, "35,079 characters of reasoning ... 35.1 s":
  withdrawn; no output was retained.
- "24 live API queries across six model architectures": the retained report
  lists 22 calls to five models; one further output from a sixth model is
  retained.
- "at an API cost under $0.02 USD" and per-cell costs: narrowed to "estimated
  spend 0.01496 USD from configured prices, not billed".
- "All executions were recorded and certified under SHA-256 digests": narrowed
  to "the report's SHA-256 digest is recorded in `receipt.json`"; the anonymous
  model's output has no digest, and the receipt's `status` field is a constant.
- Model descriptions "~500B MoE", "770B MoE", "1T+ frontier" and "open language
  models": removed; the models are described as language models accessed
  through OpenRouter.
- "All underlying algebraic cancellation lemmas are certified sorry-free in
  Lean 4": narrowed to per-orbit lemmas with unit weight; the weight factor and
  the sum over graphs are not mechanized.
- "`no_fixed_points_when_sign_reverses` confirms that any configuration with
  non-zero weight cannot be a fixed point": corrected; the weight plays no role.
- "exact relational transfer matrix oracle": corrected. SQLite enumerates the
  configurations; the transfer-matrix trace is a separate computation.
- "Invariant tests verify that every one of the 57 cancelling subgraphs sums to
  0": was untrue for version 0.3.0 (the test covered 5 of them); now true.
- "a lexical firewall that strictly filters domain tokens": narrowed to a
  substring filter for twelve words; other sign-problem vocabulary remains.
- Troyer and Wiese: "generic fermionic and frustrated sign problems belong to
  the NP-hard complexity class" and "No general polynomial-time classical
  algorithm exists ... unless P = NP": rescoped to "a generic solution of the
  sign problem for a class of frustrated systems would solve NP-hard problems",
  a worst-case statement. The citation volume is corrected from 95 to 94.
- Reference 4 ("Anomalon Research Group ... Zenodo (2026), DOI
  10.5281/zenodo.1790605"): removed. The number was a fragment of the run
  receipt identifier, not a DOI.
- Reference titles corrected: Chandrasekharan and Wiese, "Meron-Cluster Solution
  of Fermion Sign Problems"; Huffman and Chandrasekharan, "Solution to sign
  problems in half-filled spin-polarized electronic systems".
- "Non-Abelian holonomy obstructions vanish identically", the "claim hygiene
  quad" introduced "in accordance with estate governance rules", "Epistemic
  Immune Decoding", and "hieroglyphic" and "rune" terminology: removed.

## [0.3.0] — 2026-09-28

### Added

- Section 2 formal environments (Definitions 2.1 and 2.2, Lemmas 2.3 to 2.5,
  Theorem 2.6), mapped to Lean 4 modules.
- A live evaluation of `stealth/space-bunny-alpha` on Arms 1 and 5, reported as
  a length-limit failure in Arm 1 and a 4 of 4 pass in Arm 5; the Arm 5 output
  was saved to `code/results/space_bunny_arm5_result.json`.
- Subsection 6.3 on the anonymous model, and claim profile MERON-AUD-008.

## [0.2.0] — 2026-09-28

### Added

- Preprint text with results from the five-model, five-arm run.
- Lean 4 modules `MeronCharacter.lean` and `MeronClusterInvolution.lean`, with
  `lakefile.lean` and `lean-toolchain`.
- Harness and results in `code/`: `oracle.py`, `blind_problem.py`,
  `prompt_builder.py`, `antibody_miner.py`, `run_blind_benchmark.py`, and
  `results/` (report, receipt `REC_FSP_BLIND_1790605314`, summary).
- Test suite `code/tests/test_meron_cluster_solution.py` (10 tests).
- Claim profiles MERON-AUD-001 to MERON-AUD-007.

## [0.1.0] — 2026-09-28

### Added

- Initial package structure under `omega_engine_projects/fsp/meron_sign_problem/`.
- Draft `paper.md` on meron-cluster decomposition and finite sign cancellation.
- `lean4/`, `code/` and `code/tests/` directories.

## 0.1.0 — 2026-10-01 — initial Zenodo preprint release designation

Re-designated from internal revision 0.4.0 for the requested initial v0.1
preprint release. Prior corrections, scope limits, and retained pilot records
are unchanged. Derived publication artifacts and manifests must be rebuilt
and current verification recorded before deposit readiness is asserted.
