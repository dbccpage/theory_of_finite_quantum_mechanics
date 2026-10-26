---
documentation_contract: symbol-game-documentation/v1
title: "MSS-N Level 91: Typed translation"
kind: grammar-reference
level: 91
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

# MSS-N Level 91: Typed translation

**AuthorityEffect:** None.\
**Level:** Level 91 (Epoch IX: Verification, Compilers, Benchmarks & Open Horizons)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(91) = 128 + 8 \times (91 - 22) = 680$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*\
**Runtime Pipeline:** `Evaluator::targets.stage_091` | Primary Error: `ERR_SOURCE_AST_DEFECT`\
**Atlas Capabilities:** `source_ast`, `target_ast`, `decidable_fragment`, `semantic_preservation_relation`

---

## 1. Architectural Overview & Context

Level 91 resides within **Epoch IX: Verification, Compilers, Benchmarks & Open Horizons** (Compiler Bisimulation & Open Horizons) in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=91$.

- **Stage Classification:** Finite typed representation of typed translation without self-granting authority.
- **Conditional Lift Obligation:** Any accepted lift record into MSS-91 must provide $u_{91}, r_{91}$ satisfying $r_{91}(u_{91}(x)) = x$. No accepted predecessor lift is currently claimed (`lift_status: unproved`). Novel terms lacking prior preimage return typed `NON_DESCENT`.

---

## 2. Wire Packet Grammar & Successor Rationale

- **Meaning:** Finite typed representation of typed translation without self-granting authority.
- **Declared Successor Rationale:** When previous stage capacities lack primitives to articulate typed translation without ambiguity, MSS-91 is declared as the specification row providing this capability within the external research atlas. (Actual transition requires an accepted lift record; lift status is unproved.)
- **Wire Packet(s):**

```text
  <typed_translation <source_ast S> <target_ast T> <decidable_fragment fragment_id> <semantic_preservation [|S|]_S_rel_[|T|]_T>>
```

---

## 3. Runtime Pipeline Evaluator & Mathematical Core

- **Runtime Pipeline:** `Evaluator::targets.stage_091`
- **Primary Error Code:** `ERR_SOURCE_AST_DEFECT`
- **Atlas Capabilities:** `source_ast`, `target_ast`, `decidable_fragment`, `semantic_preservation_relation`
- **Mathematical Core & Boundary:** Ruling D4: Counted in apparatus column (A) and atlas specification coverage ($C_{\rm atlas}$), never in object-language mathematical capability coverage ($C_{\rm object}$); object-language witness owed. A future licensed lift must discharge the retraction obligation $r_{91}(u_{91}(x))=x$; undefined terms return `NON_DESCENT`. AuthorityEffect: None.

---

## 4. Verification Obligation & Falsifier Boundary

- **Verification Obligation:** Verify semantic preservation relation ⟦S⟧_S ∼ ⟦T⟧_T between source AST S and target AST T strictly within the declared decidable fragment.
- **Negative Counterexample:** Translating beyond the declared decidable fragment or altering quantifier order/polarity without a verified semantic preservation relation is rejected.
- **Boundary Warning:** Level 91 records machine-checked finite verification receipts; it does not confer ambient authority or self-grant execution privileges.

---

## 5. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-91 within Epoch IX: Verification, Compilers, Benchmarks & Open Horizons.
   - Machine-checked verification obligation enforcing `ERR_SOURCE_AST_DEFECT` upon invalid candidate proposals.
2. **What this does not support:**
   - Does not establish un-mechanized continuum properties or heuristic physics models.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-91 accepts valid boundary packets and rejects negative counterexamples with `ERR_SOURCE_AST_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=92$ fixtures using the local CI test harness.
