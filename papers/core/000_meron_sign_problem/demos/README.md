# The Symbol Game: Meron Fermion Sign Problem Demos & Certified Replay

**AuthorityEffect:** None.  
**Package:** `omega_engine_projects/fsp/meron_sign_problem/demos/`  
**License:** CC BY 4.0 for documentation; PolyForm Noncommercial 1.0.0 for code.

---

## Overview

This directory provides self-contained demonstrations, certified benchmark receipts, and test harnesses accompanying the research paper on solving the 1D Meron Fermion Sign Problem using **The Symbol Game Proposal Fidelity Protocol (PFP)**.

Anyone who downloads this paper deposit can:
1. **Replay host fixtures offline:** Inspect exact finite arithmetic and retained wire examples. Model-labelled summaries without raw provider custody cannot certify performance or discovery rates.
2. **Execute Live Model Queries:** Feed your own OpenRouter API key (`--live --api-key <KEY>`) to test live models in real time under identical protocol constraints.
3. **Verify 6-Site Scaling & GIN Indexing:** Run the 6-site lattice ($N = 4{,}096$ breakup graphs, $33{,}396$ configurations) demonstrating blind multi-meron loop identification from pure DDC cycle spectra without prior sector counts, achieving $Z = 33{,}012$ in under 15 seconds.

---

## Directory Layout

```
demos/
├── README.md                              # This user manual and documentation
├── code/
│   ├── demo_4site_symbol_game.py          # 4-site PFP runner (offline replay + live OpenRouter mode)
│   ├── demo_6site_scaling_gin.py          # 6-site scaling & GIN involution synthesis demo
│   ├── demo_multistage_symbol_game.py     # Multi-stage DDC DAG replay & Gamma38 wire verification
│   ├── demo_multiturn_interactive_pfp.py  # Multi-turn zero-shot interactive trials (reasoning latency & lift emission)
│   ├── demo_pure_symbolic_meron.py        # Pure Gamma38 wire communication (zero domain words)
│   └── demo_pure_symbolic_6site.py        # Pure Gamma38 wire 6-site scaling & GIN index runner
├── tests/
│   ├── test_demo_4site_replay.py          # Pytest module certifying 4-site replay and oracle ground truth
│   ├── test_demo_6site_replay.py          # Pytest module certifying 6-site DDC scaling and GIN index
│   ├── test_demo_multistage_dag.py        # Pytest module certifying multi-stage DAG causality & Gamma38 purity
│   ├── test_demo_multiturn_interactive.py # Pytest module certifying multi-turn interactive trials & latency
│   ├── test_demo_pure_symbolic.py         # Pytest module certifying pure Gamma38 wire grammar & AST roundtrip
│   ├── test_demo_pure_symbolic_ladder.py  # Pytest module certifying multi-model ladder on pure wire
│   └── test_demo_pure_symbolic_6site.py   # Pytest module certifying pure Gamma38 6-site scaling & GIN pairing
└── results/
    ├── certified_4site_ladder_results.json # Full master receipt for the 4-model ladder (scores, tokens, latency)
    ├── certified_6site_scaling_results.json# Certified ground truth and GIN synthesis receipt for 6 sites
    ├── certified_multiturn_trial_results.json # Certified multi-turn interactive trial receipts (reasoning latency & lift emission)
    ├── certified_pure_symbolic_results.json# Certified pure Gamma38 wire grammar execution receipt
    ├── certified_pure_wire_ladder_results.json # Certified pure Gamma38 model ladder results (3 models)
    ├── certified_pure_wire_6site_results.json # Certified pure Gamma38 6-site scaling receipt
    ├── symbol_game_ddc_4site_dag.jsonl    # Certified 4-site 6-node DAG trace in JSONL
    ├── symbol_game_ddc_6site_dag.jsonl    # Certified 6-site 6-node DAG trace in JSONL
    ├── symbol_game_pure_wire_dag.jsonl    # Certified pure-wire DAG trace in JSONL
    ├── symbol_game_pure_wire_6site_dag.jsonl # Certified pure-wire 6-site DAG trace in JSONL
    ├── refined_stealth_space_bunny_alpha_result.json
    ├── refined_meta_llama_llama_3_3_70b_instruct_result.json
    ├── refined_meta_llama_llama_3_1_8b_instruct_result.json
    └── refined_z_ai_glm_5_3_flash_result.json
```

---

## Quickstart

### 1. Replay 4-Site Certified Model Ladder (Offline, Instant)

```bash
python demos/code/demo_4site_symbol_game.py
```

Expected output:
```
==========================================================================
  THE SYMBOL GAME: 4-SITE MERON FERMION SIGN PROBLEM DEMO
  Model: Chandrasekharan & Wiese 1D Perimeter Loop Hamiltonian (q=3)
  Ground Truth: 256 Subgraphs, 1,296 States, Z = 912, Avg Sign = 19/27
==========================================================================

[REPLAY MODE] Verifying certified model ladder results offline...

STATUS     MODEL ID                               TIER                           LATENCY   
------------------------------------------------------------------------------------------
PASS 4/4   stealth/space-bunny-alpha              Deep Reasoning (Free tier)     14.72s    
PASS 4/4   meta-llama/llama-3.3-70b-instruct      70B Open-Weights Instruct      3.87s     
PASS 4/4   meta-llama/llama-3.1-8b-instruct       8B Lightweight Open-Weights    58.15s    
PASS 4/4   z-ai/glm-5.3-flash                     Frontier Deep Reasoning        91.99s    
------------------------------------------------------------------------------------------
All 4 models certified perfect 4/4: True
```

### 2. Run 6-Site Scaling & GIN Involution (Offline)

```bash
python demos/code/demo_6site_scaling_gin.py
```

Expected output:
```
==========================================================================
  THE SYMBOL GAME: 6-SITE SCALING & GIN INVOLUTION SYNTHESIS DEMO
  Model: 6-Site, 2-Repetition, q=3 Periodic Chain (12 Plaquettes, 24 Nodes)
==========================================================================

[Step 1] Initializing SQLite Exact Rational Construction...
[Step 2] Blind DDC Multi-Meron Loop Identification Complete:
  - Total Breakup Graphs:            4096
  - Total Configurations:            33396
  - Meron Charge Distribution:       {0: 4024, 2: 72}
  - Cancelling Subgraphs (Merons=2): 72
  - Surviving Subgraphs (Merons=0):  4024

[Step 3] GIN Inverted Mode Posting Index Involution Synthesis:
  - Involution Execution Time:       2.000 ms
  - Cancelling Doublets Formed:      192
  - Configurations Annihilated:      384 (= 192 neg + 192 pos)

[Step 4] Dual Partition Certification:
  - Cluster Sum Partition Z:         33012
  - Transfer Matrix Trace Tr(T):     33012
  - Discrepancy:                     0 (Exact Integer Agreement)

--------------------------------------------------------------------------
  OUTCOME: EXACT_REPAIR Certified in ~10s total execution time.
--------------------------------------------------------------------------
```

### 3. Replay Multi-Stage DDC DAG Traces (Offline, JSONL & Gamma38 Wire)

Replays the 5-stage DDC solution generation pipeline, emitting an append-only Directed Acyclic Graph (DAG) in JSON Lines (`symbol_game_ddc_4site_dag.jsonl`) and asserting pure 38-character $\Gamma_{38}$ wire alphabet conformity (`{0-9, a-z, <, >}`):

```bash
# Replay 4-site multi-stage DDC DAG (Z = 912)
python demos/code/demo_multistage_symbol_game.py --sites 4

# Replay 6-site multi-stage DDC DAG (Z = 33012)
python demos/code/demo_multistage_symbol_game.py --sites 6
```

Expected output:
```text
================================================================================
  THE SYMBOL GAME: MULTI-STAGE DDC DAG REPLAY (4-SITE LATTICE)
================================================================================
Stages Executed: 6 turns
Terminal Status: EXACT_REPAIR
Exact Partition Z: 912
Gamma38 Wire Alphabet Purity: True
DAG Output File: demos/results/symbol_game_ddc_4site_dag.jsonl
Verification: SUCCESS (EXACT_REPAIR)

--- DAG EXECUTION TRACE (JSONL) ---
[0] DAG_N00_CARRIER    | Action: ASSERT_CARRIER         | Wire: op<<11>op<<1><10000>>op<<10><0><1>>>
[1] DAG_N01_BREAKUP    | Action: PROBE_PLAQUETTES       | Wire: op<<101><10><0><1><10>>
[2] DAG_N02_HOLONOMY   | Action: MEASURE_HOLONOMY       | Wire: op<<100><>op<<11>op<<1><10>>op<<1><11>>>>
[3] DAG_N03_LIFT_REQ   | Action: REQUEST_LIFT           | Wire: op<<1100><liftreq>>
[3] DAG_N03_LIFT_GRANT | Action: GRANT_LIFT             | Wire: op<<0><><0><1>>
[4] DAG_N04_EXACT_REPAIR | Action: CERTIFY_EXACT_REPAIR   | Wire: op<<10010><0><1110010000><1>>
```

### 4. Retained interactive example

The model-labelled multi-turn fixture is synthetic and lacks raw provider
custody. Its reported usage and success percentages are unverified. The English
prompts supply counts and request the lift; keyword screening is not a discovery
or mathematical certification test. Future live runs retain full responses.

```console
.venv/bin/python demos/code/demo_multiturn_interactive_pfp.py
```

### 5. Four-site host and packet replay

The revised four-site runner sends and checks Gamma38 packets only. Offline
candidates are supplied fixtures bound to LlmTurn run roots; TransportValidated
is a transport status. Offline execution computes the host partition and
transfer trace (912), checks packet grammar, and preserves retained artifacts.
Valid packets with a wrong opcode or value fail the live response checker.

```console
.venv/bin/python demos/code/demo_pure_symbolic_meron.py
```

To save a new replay, select an external `--output-directory`. Live mode requires
an API key and tests expected packet compliance; no model discovery is inferred.

### 6. Run Live OpenRouter Single-Shot Query (Requires API Key)

Set your environment variable `OPENROUTER_API_KEY` or pass `--api-key`:

```bash
# Test with Space Bunny Alpha (Free model tier)
python demos/code/demo_4site_symbol_game.py --live --model stealth/space-bunny-alpha

# Test with Llama-3.3-70B Instruct (Ultra-fast, ~$0.00035 per call)
python demos/code/demo_4site_symbol_game.py --live --model meta-llama/llama-3.3-70b-instruct
```

### 7. Run Pytest Test Suite

```bash
pytest demos/tests/ -v
```

The phase-two three-model summary lacks complete requests, raw responses and
source bindings. Its reported metrics remain unverified. The packet test checks
the retained examples and their explicit evidence ceiling.
