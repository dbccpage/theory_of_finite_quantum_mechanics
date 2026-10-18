# General PFP Strategy & Multi-Stage Operad Mining Plan for the 35 Finite-QM DAG Prompts

**AuthorityEffect:** `None`  
**Policy & Stage Contract:** `SPK-001` (`pfp-staged.0.3`, `COPP-v2-COMPACT`, `PromptPacketV0_1`)  
**Target Prompt Directory:** [`C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\dag\prompts`](file:///C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/dag/prompts)  
**Target Evidence Directory:** [`C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\evidence`](file:///C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/evidence)  
**Target Papers Directory:** [`C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\papers`](file:///C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/papers)

---

## 1. Architectural Synthesis (`omega_engine_pfp/infrastructure/yaml/` + `004_oepfp`)

Based on a full audit of `omega_engine_pfp/infrastructure/yaml/` (`stages/`, `prompts/`, `modes/`, `nf/`, `schemas/`, `pilots/`) and `omega_engine_education/documentation/004_oepfp/` (`docs/00`–`21`, `math/00`–`09`, `grammar/`, `rewriting/`, `lean4/`), we combine four core PFP mechanisms to make every derivation run fast (`< 1,500` completion tokens), deterministic, and steerable:

1. **Upgraded 11-Stage Controller (`stages/controller.yaml`, `pfp-staged.0.3`, `SPK-001`)**:
   - **Stage 1 (`admit`, host)**: Validates the YAML envelope, binds the DAG node (`id`, `stage`, `status`, `statement`, `bottleneck`), and checks whether all 4 operad mining slots (`slot_m1`..`slot_m4`) are populated.
   - **Stage 1a & 1b (`P*` Cochain Syndrome Pre-Check, model + host)**: Verifies spanning-tree vertex potentials ($C^0 \xrightarrow{d_0} C^1$) and fundamental cycle chord obstructions ($C^1 \xrightarrow{d_1} C^2$, $d_1 d_0 = 0$) before any domain lift is accepted.
   - **Stage 2 (`ideation`, model — `seat_begemot`)**: Proposes candidate constructions, finite countermodels, and scope weakenings (at least one explicit refutation/countermodel and two LLM-free checkable routes).
   - **Stage 3 (`audit`, model — `seat_koroviev`)**: Filters candidates through the mined Congruence Ideals ($\mathcal{I}$) and Annihilator Decoys ($\mathcal{O}^-$), routing the strongest finite-witnessable candidate.
   - **Stage 4 (`l2_extraction`, model — `seat_begemot`)**: Emits the strict typed JSON derivation certificate over exact arithmetic ($\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{Z}[i]$, $\mathbb{F}_2$).
   - **Stage 5 (`evaluation`, host — `seat_woland`)**: Sovereign deterministic gate engine (`G0`..`G9` + node-specific exact equations + Lean 4 / Rust symbol resolution) executing in `< 2 ms`.
   - **Stage 6 (`adversarial`, model — `seat_margarita`) & Stage 7 (`challenge_replay`, host)**: Probes boundary mutations (e.g., dropping an imported assumption or perturbing a rational witness) and verifies that the host gate catches the perturbation.
   - **Stage 8 (`selection`, host) & Stage 9 (`receipt`, host)**: Emits a SHA-256 sealed machine receipt to `evidence/receipts/` and updates the corresponding paper in `papers/derivations/`.

2. **3-Layer Compressed Coloured Operad Architecture (`template_operad_compressed.yaml`, `COPP-v2-COMPACT`)**:
   - Replaces verbose prose instructions with a 3-layer planar coloured operad $(\mathcal{C}, \mathcal{O}^+, \circ_i, \mathcal{I}, \mathcal{O}^-)$:
     - **Layer 0 (`Environment`)**: Algebraic ring ($\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{Z}[i]$), finite carrier dimensions, normal-form contract (`nf.cochain.dhnf`, `nf.ddc.dual_witness`, `nf.epistemic.authority`), and observer budget.
     - **Layer 1 (`TreeSkeleton`)**: Forward generative operators ($\mathcal{O}^+$) with explicit arities, source/target colours, and planar grafting sequence ($\circ_i$).
     - **Layer 2 (`SpanTable`)**: Concrete source spans, fail-closed Congruence Ideals ($\mathcal{I} \to \text{NullTree}$), and Annihilator Decoy antibodies ($\mathcal{O}^-$).

3. **PFP Steering Modes (`modes/mode_catalog.yaml`)**:
   - **Mode 2 (`Packets & Sealed Envelopes`) & Mode 14 (`Fail-Closed Typed Refusal`)**: Every node with status `IMPORTED_ASSUMPTION`, `CONDITIONAL`, or `OPEN` must explicitly separate its *finite derived shadow* (what holds over $\mathbb{Z}/\mathbb{Q}/\mathbb{Z}[i]$) from its *unpaid external import boundary* (what requires continuum $\mathbb{R}/\mathbb{C}$, $U(1)$ topology, Gleason $\sigma$-additivity, or CPTP complete positivity), accompanied by an exact finite countermodel showing why the unpaid import is not free.
   - **Mode 4 (`Epistemic Antibody Injections`) & Mode 10 (`Cemetery DAG Mining`)**: Injects node-specific decoy traps (`O^-`) mined from `derivation_dag.json` bottlenecks and `H001`–`H062` countermodels.
   - **Mode 5 (`Skill Injection & Operad Morphisms`) & Mode 8 (`Discrete Cochain Involutions`)**: Steers the model along the exact DAG route morphisms in `derivation_dag_operads.binding.yaml`.
   - **Mode 9 (`Lean 4 Proof Kernel Elaboration`)**: Binds every prompt to its exact theorem anchor in `lean/DerivationDagQMClosure.lean` and Rust witness in `code/rust/src/dag_witnesses.rs`.

4. **Five Operational Laws for High-Speed Reasoning-Model Execution**:
   - **Law 1 (Zero Nested Schema Wrapping)**: Call `EstimatedBudgetGateway.for_action(attempt_id).complete_result(...)` directly with a single top-level JSON schema (`max_output_tokens = 3000`).
   - **Law 2 (1-Line System Prompt + Compact Operad User Payload)**: Keep `system_prompt` to a single declarative sentence and place the grafted Operad + `P*` payload in `user_prompt` (`< 950` prompt tokens). This prevents reasoning-token blowup on `deepseek/deepseek-v4.1-flash` (`default_effort: "high"`), cutting completion tokens to `~1,000–1,350` and cost to `~$0.000035` per turn.
   - **Law 3 (Multi-Mission Pre-Run Operad Mining)**: Never send an un-mined stub prompt to a model. Populate all 4 operad slots (`slot_m1`..`slot_m4`) via deterministic operad mining before live model dispatch.
   - **Law 4 (Tiered Model Escalation)**: Dispatch first to `deepseek/deepseek-v4.1-flash` via OpenRouter; if any gate in `G0`..`G9` fails, escalate with the exact Stage 5 failure syndrome to `deepseek/deepseek-v4-flash` and then to Anthropic `fable5.1` (`claude-sonnet-4-5`).
   - **Law 5 (Tri-Language & Paper Closure)**: Every passed prompt writes a cryptographic receipt to `evidence/receipts/pfp_dag_prompts/`, updates the corresponding `TFQ-*.md` paper(s) in `papers/derivations/`, and verifies/updates Python, Rust (`code/rust/src/dag_witnesses.rs`), and Lean 4 (`lean/DerivationDagQMClosure.lean`).

---

## 2. Two-Phase Prompt Lifecycle: Unfilled Operad Slots $\to$ Multi-Mission Operad Mining $\to$ Live Execution

### Phase A: Initial Prompt Specification (Unfilled Operad Slots)
All 35 prompt files in `C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\dag\prompts\*.yaml` are first upgraded from 1-line stubs (`user_prompt: prompt_text`) to full `omega.pfp.finite_qm.dag_prompt.v1` YAML packets containing:
- Exact DAG metadata (`node_id`, `stage`, `status`, `source_status`, `statement`, `bottleneck`, `imported_structure`, `incoming_routes`, `outgoing_routes`, `source_refs`, `lean_refs`, `rust_refs`, `paper_refs`).
- **Four Structured Operad Slots (`operad_slots`) initialized with `mining_status: UNFILLED_PENDING_MINING`**:
  - `slot_m1_layer0_ambient_carrier`: `{ mining_status: UNFILLED_PENDING_MINING, algebraic_ring: null, ambient_carrier: null, normal_form_contracts: [], observer_budget: null }`
  - `slot_m2_layer1_forward_morphisms`: `{ mining_status: UNFILLED_PENDING_MINING, operad_family_id: null, source_colours: [], target_colour: null, operators: [], planar_grafting_sequence: [] }`
  - `slot_m3_layer2_ideals_and_annihilators`: `{ mining_status: UNFILLED_PENDING_MINING, concrete_spans: {}, congruence_ideals: [], annihilator_antibodies: [] }`
  - `slot_m4_tri_language_witness_anchors`: `{ mining_status: UNFILLED_PENDING_MINING, exact_integer_identities: [], finite_countermodel_witness: null, lean4_theorems: [], rust_witness_fns: [] }`
- Multi-stage `pfp-staged.0.3` execution plan (`stages_plan`), compact `system_prompt`, parameterized `user_prompt_template`, and strict JSON `response_schema`.

### Phase B: Per-Prompt 4-Mission Operad Mining & Live Multi-Stage Execution Loop
For each prompt $k \in \{1, \dots, 35\}$ in `dag/prompts/`:
1. **Execute 4 Operad Mining Missions (`mine_operads_for_prompt`)**:
   - **Mission M1 (Carrier & Normal Form Miner)**: Extracts the exact coefficient ring ($\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{Z}[i]$, $\mathbb{F}_2$), carrier dimensions, and normal-form contracts from `derivation_dag.json` and `omega_engine_pfp/infrastructure/yaml/nf/`.
   - **Mission M2 (Operad Family & Route Morphism Miner)**: Mines the governing operad family and composition rules from `derivation_dag_operads.binding.yaml` and the node's incoming/outgoing routes in `derivation_dag.json`.
   - **Mission M3 (Congruence Ideal & Decoy Antibody Miner)**: Extracts fail-closed quotient fences ($\mathcal{I}$) and decoy refutation witnesses ($\mathcal{O}^-$) from `bottleneck`, `imported_structure`, and the `H001`–`H062` countermodel catalog.
   - **Mission M4 (Tri-Language Witness & Invariant Miner)**: Mines the exact integer/rational equations, Lean 4 theorem anchors (`lean/DerivationDagQMClosure.lean`), and Rust witness functions (`code/rust/src/dag_witnesses.rs`).
2. **Fill the Operad Slots in the Prompt YAML (`mining_status: FILLED_VERIFIED`)**:
   - Writes the mined operads into `operad_slots` and compiles the active `user_prompt` with the grafted 3-Layer Operad + `P*` payload.
3. **Execute Multi-Stage PFP Run Live**:
   - Dispatches Stage 2/3 (`Ideation & Audit`) and Stage 4 (`L2 Typed Extraction`) + Stage 5 (`Host Gate G0..G9`) against OpenRouter `deepseek/deepseek-v4.1-flash` (with fallback to `deepseek/deepseek-v4-flash` and Anthropic `fable5.1` / `claude-sonnet-4-5`).
4. **Record Evidence, Update Papers, and Sync Code (Python, Rust, Lean 4)**:
   - Saves the cryptographic receipt to `C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\evidence\receipts\pfp_dag_prompts\<node_id>_pfp_receipt.json` and updates the master campaign ledger `evidence\dossiers\pfp_dag_prompts_campaign.md`.
   - Updates the corresponding paper(s) in `C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\papers\derivations\`.
   - Updates Python, Rust, and Lean 4 witnesses as needed and runs `validate_derivation_dag.py` and `cargo test`.

---

## 3. Complete Queue of the 35 Finite-QM DAG Prompts

| # | Prompt File (`dag/prompts/`) | Stage | Node ID | Status | Primary Operad Family |
|---|---|---|---|---|---|
| 01 | `FINITE_QM_CORE__FQ-DECLARED-QUANTUM-INTERFACE__IMPORTED_ASSUMPTION.yaml` | `FINITE_QM_CORE` | `FQ-DECLARED-QUANTUM-INTERFACE` | `IMPORTED_ASSUMPTION` | `OP-FQ-DECLARED-INTERFACE-GATE` |
| 02 | `FINITE_QM_CORE__FQ-GAP-BORN-UNIQUENESS-GLEASON__CONDITIONAL.yaml` | `FINITE_QM_CORE` | `FQ-GAP-BORN-UNIQUENESS-GLEASON` | `CONDITIONAL` | `OP-FQ-SORKIN-GLEASON-BUSCH` |
| 03 | `FINITE_QM_CORE__FQ-GAP-C500-ORIGINAL-TARGETS__OPEN.yaml` | `FINITE_QM_CORE` | `FQ-GAP-C500-ORIGINAL-TARGETS` | `OPEN` | `OP-FQ-C500-SCOPE-REDUCTION` |
| 04 | `FINITE_QM_CORE__FQ-GAP-CONTINUUM-HILBERT-LIFT__CONDITIONAL.yaml` | `FINITE_QM_CORE` | `FQ-GAP-CONTINUUM-HILBERT-LIFT` | `CONDITIONAL` | `OP-FQ-CONTINUUM-WINTNER-WIELANDT` |
| 05 | `FINITE_QM_CORE__FQ-GAP-CORPUS-REWRITE__OPEN.yaml` | `FINITE_QM_CORE` | `FQ-GAP-CORPUS-REWRITE` | `OPEN` | `OP-FQ-CORPUS-CONSOLIDATION` |
| 06 | `FINITE_QM_CORE__FQ-GAP-CUSTODY-AND-RECEIPTS__OPEN.yaml` | `FINITE_QM_CORE` | `FQ-GAP-CUSTODY-AND-RECEIPTS` | `OPEN` | `OP-FQ-CUSTODY-RECEIPT-AUDIT` |
| 07 | `FINITE_QM_CORE__FQ-GAP-TENSOR-UNIQUENESS__CONDITIONAL.yaml` | `FINITE_QM_CORE` | `FQ-GAP-TENSOR-UNIQUENESS` | `CONDITIONAL` | `OP-FQ-TENSOR-CONE-BRACKETING` |
| 08 | `FINITE_QM_CORE__FQ-GAP-U1-CIRCLE__CONDITIONAL.yaml` | `FINITE_QM_CORE` | `FQ-GAP-U1-CIRCLE` | `CONDITIONAL` | `OP-FQ-CAYLEY-U1-PUNCTURED-CIRCLE` |
| 09 | `FINITE_QM_CORE__FQ-POSITIVE-WEIGHTS-ADMITTED__IMPORTED_ASSUMPTION.yaml` | `FINITE_QM_CORE` | `FQ-POSITIVE-WEIGHTS-ADMITTED` | `IMPORTED_ASSUMPTION` | `OP-FQ-POSITIVE-L1-WEIGHT-ADMISSION` |
| 10 | `FINITE_QM_CORE__FQ-PRIM-TO-QM-SELECTION-OPEN__CONDITIONAL.yaml` | `FINITE_QM_CORE` | `FQ-PRIM-TO-QM-SELECTION-OPEN` | `CONDITIONAL` | `OP-FQ-PRIM-TO-QM-PARAMETER-GAP` |
| 11 | `FINITE_QM_DYNAMICS__DS-CONTINUOUS-TIME-EXP-GENERATOR__IMPORTED_ASSUMPTION.yaml` | `FINITE_QM_DYNAMICS` | `DS-CONTINUOUS-TIME-EXP-GENERATOR` | `IMPORTED_ASSUMPTION` | `OP-DS-EXP-GENERATOR-BOUNDARY` |
| 12 | `FINITE_QM_DYNAMICS__DS-QM033-064-074-083-QHELD-CONTINUUM__IMPORTED_ASSUMPTION.yaml` | `FINITE_QM_DYNAMICS` | `DS-QM033-064-074-083-QHELD-CONTINUUM` | `IMPORTED_ASSUMPTION` | `OP-DS-QHELD-CONTINUUM-FENCE` |
| 13 | `FINITE_QM_DYNAMICS__DS-QM034-035-050-051-095-RESERVED-STUBS__CONDITIONAL.yaml` | `FINITE_QM_DYNAMICS` | `DS-QM034-035-050-051-095-RESERVED-STUBS` | `CONDITIONAL` | `OP-DS-CAYLEY-DIRAC-FINITE-SHADOW` |
| 14 | `FINITE_QM_DYNAMICS__DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT__IMPORTED_ASSUMPTION.yaml` | `FINITE_QM_DYNAMICS` | `DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT` | `IMPORTED_ASSUMPTION` | `OP-DS-DECOHERENCE-GRAM-MATRIX` |
| 15 | `FINITE_QM_DYNAMICS__FQ-GAP-STONE-CONTINUOUS-TIME__CONDITIONAL.yaml` | `FINITE_QM_DYNAMICS` | `FQ-GAP-STONE-CONTINUOUS-TIME` | `CONDITIONAL` | `OP-DS-STONE-PYTHAGOREAN-ALIASING` |
| 16 | `FINITE_QM_STRUCTURE__DS-CPTP-COMPLETE-POSITIVITY-IMPORT__IMPORTED_ASSUMPTION.yaml` | `FINITE_QM_STRUCTURE` | `DS-CPTP-COMPLETE-POSITIVITY-IMPORT` | `IMPORTED_ASSUMPTION` | `OP-DS-CPTP-CHOI-PARTIAL-TRANSPOSE` |
| 17 | `FINITE_QM_STRUCTURE__DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT__IMPORTED_ASSUMPTION.yaml` | `FINITE_QM_STRUCTURE` | `DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT` | `IMPORTED_ASSUMPTION` | `OP-DS-PROJECTION-POSTULATE-BOUNDARY` |
| 18 | `FINITE_QM_STRUCTURE__DS-QM062-U1-RESIDUES-IMPORT__IMPORTED_ASSUMPTION.yaml` | `FINITE_QM_STRUCTURE` | `DS-QM062-U1-RESIDUES-IMPORT` | `IMPORTED_ASSUMPTION` | `OP-DS-U1-SELECTOR-RESIDUES` |
| 19 | `FINITE_QM_STRUCTURE__DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY__IMPORTED_ASSUMPTION.yaml` | `FINITE_QM_STRUCTURE` | `DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY` | `IMPORTED_ASSUMPTION` | `OP-DS-BORN-LP-RIVAL-BOUNDARY` |
| 20 | `L1_TO_L2__GP-IMPORT-CIRCLE-U1__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `GP-IMPORT-CIRCLE-U1` | `IMPORTED_ASSUMPTION` | `OP-GP-CIRCLE-U1-IMPORT` |
| 21 | `L1_TO_L2__GP-IMPORT-COMPLEX-FIELD__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `GP-IMPORT-COMPLEX-FIELD` | `IMPORTED_ASSUMPTION` | `OP-GP-COMPLEX-FIELD-GAUSSIAN-GAP` |
| 22 | `L1_TO_L2__GP-IMPORT-CONTINUOUS-TIME__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `GP-IMPORT-CONTINUOUS-TIME` | `IMPORTED_ASSUMPTION` | `OP-GP-CONTINUOUS-TIME-TOGGLE-GAP` |
| 23 | `L1_TO_L2__GP-IMPORT-CONTINUUM-HILBERT__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `GP-IMPORT-CONTINUUM-HILBERT` | `IMPORTED_ASSUMPTION` | `OP-GP-CONTINUUM-HILBERT-COMPLETION` |
| 24 | `L1_TO_L2__GP-IMPORT-CPTP-CLASS__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `GP-IMPORT-CPTP-CLASS` | `IMPORTED_ASSUMPTION` | `OP-GP-CPTP-STINESPRING-IMPORT` |
| 25 | `L1_TO_L2__GP-IMPORT-GLEASON__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `GP-IMPORT-GLEASON` | `IMPORTED_ASSUMPTION` | `OP-GP-GLEASON-FRAME-IMPORT` |
| 26 | `L1_TO_L2__GP-IMPORT-TENSOR-PRODUCT__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `GP-IMPORT-TENSOR-PRODUCT` | `IMPORTED_ASSUMPTION` | `OP-GP-TENSOR-BILINEAR-RIVAL` |
| 27 | `L1_TO_L2__L1-IMP-COMPLEX-FIELD__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `L1-IMP-COMPLEX-FIELD` | `IMPORTED_ASSUMPTION` | `OP-L1-COMPLEX-FIELD-H007` |
| 28 | `L1_TO_L2__L1-IMP-HAAR-INDEPENDENT-PHASES__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `L1-IMP-HAAR-INDEPENDENT-PHASES` | `IMPORTED_ASSUMPTION` | `OP-L1-HAAR-VS-FINITE-Z4-AVERAGE` |
| 29 | `L1_TO_L2__L1-IMP-HILBERT-INNER-PRODUCT__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `L1-IMP-HILBERT-INNER-PRODUCT` | `IMPORTED_ASSUMPTION` | `OP-L1-GRAM-INNER-PRODUCT-H005` |
| 30 | `L1_TO_L2__L1-IMP-LINEAR-ISOMETRIC-DYNAMICS__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `L1-IMP-LINEAR-ISOMETRIC-DYNAMICS` | `IMPORTED_ASSUMPTION` | `OP-L1-ISOMETRIC-DYNAMICS-H003` |
| 31 | `L1_TO_L2__L1-IMP-ORTHOGONAL-ADDITIVITY__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `L1-IMP-ORTHOGONAL-ADDITIVITY` | `IMPORTED_ASSUMPTION` | `OP-L1-ORTHOGONAL-ADDITIVITY-H013` |
| 32 | `L1_TO_L2__L1-IMP-SQRT-FIELD__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `L1-IMP-SQRT-FIELD` | `IMPORTED_ASSUMPTION` | `OP-L1-SQRT-FIELD-EXTENSION` |
| 33 | `L1_TO_L2__L1-IMP-U1-PHASES__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `L1-IMP-U1-PHASES` | `IMPORTED_ASSUMPTION` | `OP-L1-U1-PHASE-GROUP-H011` |
| 34 | `L1_TO_L2__L1-QM020-THM2B-MINKOWSKI__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `L1-QM020-THM2B-MINKOWSKI` | `IMPORTED_ASSUMPTION` | `OP-L1-MINKOWSKI-LP-SUBADDITIVITY` |
| 35 | `L1_TO_L2__L1-QM020-THM6-P2-GLEASON__IMPORTED_ASSUMPTION.yaml` | `L1_TO_L2` | `L1-QM020-THM6-P2-GLEASON` | `IMPORTED_ASSUMPTION` | `OP-L1-GLEASON-BORN-UNIQUENESS` |

---

## 4. Claim Hygiene Envelope (`RULE[user_global]`)

1. **What this plan supports**: Deterministic 4-mission operad mining and multi-stage PFP (`pfp-staged.0.3` + `COPP-v2-COMPACT`) execution across all 35 unfinished/boundary nodes in `C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\dag\prompts`, checked by exact integer/rational gates (`G0`..`G9`), Lean 4 theorem anchors, and Rust witness functions.
2. **What this plan does not support**: Promoting external continuum, topological, or Gleason/Stone/CPTP imported assumptions to unconditional finite derivations without explicit hypothesis declarations.
3. **Narrowest defensible claim**: Structuring each DAG prompt with explicit unfilled operad slots (`slot_m1`..`slot_m4`), populating those slots via 4-mission operad mining prior to execution, and enforcing compact typed JSON extraction under `SPK-001` yields reproducible, low-token (`< 1,500` completion tokens) multi-stage verification receipts across the 35 boundary nodes.
4. **Next test needed**: Execute the Phase A prompt generation across all 35 YAML files in `dag/prompts/`, then run the Phase B operad-mining + live OpenRouter `deepseek/deepseek-v4.1-flash` (with `fable5.1` fallback) loop starting from Prompt #01 (`FINITE_QM_CORE__FQ-DECLARED-QUANTUM-INTERFACE__IMPORTED_ASSUMPTION.yaml`).
