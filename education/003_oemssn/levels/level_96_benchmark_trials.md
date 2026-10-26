---
documentation_contract: symbol-game-documentation/v1
title: "MSS-N Level 96: Benchmark trials"
kind: grammar-reference
level: 96
status: active
maturity: research
atlas_status: specified
syntax_status: verified
checker_status: verified
mathematical_status: computed
successor_status: declared
lift_status: unproved
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md
---

# MSS-N Level 96: Benchmark trials

**AuthorityEffect:** None.\
**Level:** Level 96 (Epoch IX: Verification, Compilers, Benchmarks & Open Horizons)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(96) = 128 + 8 \times (96 - 22) = 720$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*\
**Runtime Pipeline:** `Evaluator::targets.stage_096` | Primary Error: `ERR_TRIAL_MANIFEST_DEFECT`\
**Atlas Capabilities:** `trial_manifest`, `statistical_interval`, `confidence_level`, `interval_method`, `sampling_protocol`, `corpus_seed_digest`

---

## 1. Architectural Overview & Context

Level 96 resides within **Epoch IX: Verification, Compilers, Benchmarks & Open Horizons** (Compiler Bisimulation & Open Horizons) in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=96$.

- **Stage Classification:** Finite typed representation of benchmark trials without self-granting authority.
- **Conditional Lift Obligation:** Any accepted lift record into MSS-96 must provide $u_{96}, r_{96}$ satisfying $r_{96}(u_{96}(x)) = x$. No accepted predecessor lift is currently claimed (`lift_status: unproved`). Novel terms lacking prior preimage return typed `NON_DESCENT`.

---

## 2. Wire Packet Grammar & Successor Rationale

- **Meaning:** Finite typed representation of benchmark trials without self-granting authority.
- **Declared Successor Rationale:** When previous stage capacities lack primitives to articulate benchmark trials without ambiguity, MSS-96 is declared as the specification row providing this capability within the external research atlas. (Actual transition requires an accepted lift record; lift status is unproved.)
- **Wire Packet(s):**

```text
  <benchmark_trials <corpus_digest test_corpus_hash> <seed_digest rng_seed_hash> <trial_count N_trials> <sampling_protocol protocol_id> <confidence_level 1_minus_alpha> <interval_method method_id> <recomputed_interval lower_upper_bounds>>
```

---

## 3. Runtime Pipeline Evaluator & Mathematical Core

- **Runtime Pipeline:** `Evaluator::targets.stage_096`
- **Primary Error Code:** `ERR_TRIAL_MANIFEST_DEFECT`
- **Atlas Capabilities:** `trial_manifest`, `statistical_interval`, `confidence_level`, `interval_method`, `sampling_protocol`, `corpus_seed_digest`
- **Mathematical Core & Boundary:** Ruling D4: Counted in apparatus column (A) and atlas specification coverage ($C_{\rm atlas}$), never in object-language mathematical capability coverage ($C_{\rm object}$); object-language witness owed. A future licensed lift must discharge the retraction obligation $r_{96}(u_{96}(x))=x$; undefined terms return `NON_DESCENT`. AuthorityEffect: None.

---

## 4. Verification Obligation & Falsifier Boundary

- **Verification Obligation:** Recompute confidence/coverage interval from verified trial count, immutable corpus digest, PRNG seed digest, declared sampling protocol, and declared interval method.
- **Negative Counterexample:** A benchmark score reported as a single point estimate, missing trial counts, or ungrounded in declared sampling protocol is rejected.
- **Boundary Warning:** Level 96 records machine-checked finite verification receipts; it does not confer ambient authority or self-grant execution privileges.

---

## 5. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-96 within Epoch IX: Verification, Compilers, Benchmarks & Open Horizons.
   - Machine-checked verification obligation enforcing `ERR_TRIAL_MANIFEST_DEFECT` upon invalid candidate proposals.
2. **What this does not support:**
   - Does not establish un-mechanized continuum properties or heuristic physics models.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-96 accepts valid boundary packets and rejects negative counterexamples with `ERR_TRIAL_MANIFEST_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=97$ fixtures using the local CI test harness.
