# Blind Cluster Recovery Benchmark: Symbol Game Epistemic Immune System

**AuthorityEffect**: None

**Domain**: Fermion Sign Problem / Cluster Recovery (`omega_engine_projects/fsp`)

**Firewall**: Strict Lexical Hygiene (Zero Physics / Meron / Hubbard vocabulary)

---

## 1. Overview & Objective

This benchmark evaluates whether large language models across multiple scales (70B, ~500B MoE, 770B MoE, 1T+ Frontier) can recover the exact non-perturbative cluster cancellation mechanism of the **Fermion Sign Problem** without any physics domain clues.

### The Blindness Protocol
The system enforces strict lexical hygiene (`assert_lexical_hygiene`). The prompt contains **zero occurrences** of the following banned tokens:
- `meron`
- `fermion`
- `physics`
- `hamiltonian`
- `hubbard`
- `chandrasekharan`
- `wiese`

Instead, the problem is formulated purely as an **abstract oriented graph partition problem**:
Given a periodic bipartite grid and a collection of 256 subgraphs, each subgraph $g$ possesses $k$ independent cycles and $2^k$ binary cycle orientation configurations $f \in \mathbb{Z}_2^k$ with alternating signs $s_g(f) = (-1)^{\text{crossings}(g, f)}$.
The objective is to deduce:
1. Under what algebraic or topological condition does $\sum_{f \in \mathbb{Z}_2^k} s_g(f) = 0$?
2. Which subgraphs survive the sum?
3. What is the exact total partition sum $Z$?

---

## 2. Five Experimental Arms

| Arm | Description | Cognitive / Symbolic Mechanism |
|---|---|---|
| **Arm 1** | **Constrained JSON Decoding** | Standard single-turn prompt enforced with strict JSON Schema output. |
| **Arm 2** | **Attention Distractor-Key Masking** | Macro-cycle topological spectra (cycle lengths and winding parity) isolate the salient keys from the longer baseline narrative. |
| **Arm 3** | **DDC Hieroglyphic Factorization** | Spanning tree and chord factorization using the Discrete Deformation Calculus 8-letter alphabet ($\mathcal{A}_{\mathrm{DDC}} = \{E, R, C, I, \Lambda, D, M, T\}$). |
| **Arm 4** | **Multi-Round Epistemic Immune Mining** | Up to five rounds where model errors are mined into four typed antibody classes and injected as falsification constraints. |
| **Arm 5** | **Full Hybrid** | Hieroglyphic prompt compression + distractor masking + mandatory numeric scratchpad + accumulated antibody constraints. |

---

## 3. Mathematical Ground Truth (Oracle)

Derived from exact relational enumeration in `omega_engine_projects/fsp/code/sign_sql/exact_models.py`:
- **Model Parameters**: 4-site periodic chain, 2 Trotter repetitions ($T=4$ time slices), parameter $q = 3$ ($b = 1$, $a = 1$).
- **Total Breakup Subgraphs**: $2^8 = 256$.
- **Total Configurations**: $1,296$.
- **Unflipped Negative Configurations**: $192$.
- **Average Sign**: $\langle \sigma \rangle = 912 / 1296 = 19/27 \approx 0.7037$.
- **Zero-Charge Subgraphs ($m_g = 0$)**: $199$ subgraphs where every cycle has even temporal winding. Total weight sum $= 912$.
- **Cancelling Subgraphs ($m_g \ne 0$)**: $57$ subgraphs with $\ge 1$ odd temporal winding cycle. For each such subgraph:
  $$\sum_{f \in \mathbb{Z}_2^k} s_g(f) = W(g) \prod_{j=1}^k (1 + (-1)^{m_{g, j}}) = 0$$
  identically cancelling all $57 \times 2^k$ configurations to zero.
- **Exact Target Partition**: $Z = 912$.

---

## 4. Evaluated Models & Pricing

Evaluated via OpenRouter under a configured-price ceiling of **$1.50** (target spend < $0.50):
1. **70B Dense**: `meta-llama/llama-3.3-70b-instruct` ($0.12 / $0.30 per M tokens)
2. **~500B MoE**: `deepseek/deepseek-v4-flash-0731` ($0.04 / $0.10 per M tokens)
3. **~500B MoE**: `z-ai/glm-5.3-flash` ($0.075 / $0.25 per M tokens)
4. **770B MoE**: `tencent/hy4-preview` ($0.30 / $0.60 per M tokens)
5. **1T+ Frontier**: `qwen/qwen3.7-max` ($0.40 / $1.20 per M tokens)

---

## 5. Execution & Reproduction

### Dry Run (Mock API, zero cost)

```bash
python omega_engine_projects/fsp/demos/blind_cluster_recovery/run_blind_benchmark.py --dry-run
```

### Live Benchmark Run

Install the live-provider dependencies first:

```bash
python -m pip install -e ".[bench]"
```

Then supply `OPENROUTER_API_KEY` in the environment or name an explicit dotenv file:

```bash
python omega_engine_projects/fsp/demos/blind_cluster_recovery/run_blind_benchmark.py --budget-ceiling 1.50 --env-file .env
```

All results and execution receipts are written to:

- `results/master_evaluation_report.json`
- `results/summary.json`
- `results/receipt.json`
