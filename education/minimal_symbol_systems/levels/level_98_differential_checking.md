---
documentation_contract: education-documentation/v1
title: "MSS-N Level 98: Differential checking"
kind: grammar-reference
level: 98
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
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
---

# MSS-N Level 98: Differential checking

**AuthorityEffect:** None.\
**Level:** Level 98 (Epoch IX: Verification, Compilers, Benchmarks & Open Horizons)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(98) = 128 + 8 \times (98 - 22) = 736$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*\
**Runtime Pipeline:** `Evaluator::targets.stage_098` | Primary Error: `ERR_CHECKER_PAIR_DEFECT`\
**Atlas Capabilities:** `checker_pair`, `disagreement_receipt`, `differential_replay`, `independence_boundary`

---

## 1. Architectural Overview & Context

Level 98 resides within **Epoch IX: Verification, Compilers, Benchmarks & Open Horizons** (Compiler Bisimulation & Open Horizons) in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=98$.

- **Stage Classification:** Finite typed representation of differential checking without self-granting authority.
- **Conditional Lift Obligation:** Any accepted lift record into MSS-98 must provide $u_{98}, r_{98}$ satisfying $r_{98}(u_{98}(x)) = x$. No accepted predecessor lift is currently claimed (`lift_status: unproved`). Novel terms lacking prior preimage return typed `NON_DESCENT`.

---

## 2. Wire Packet Grammar & Successor Rationale

- **Meaning:** Finite typed representation of differential checking without self-granting authority.
- **Declared Successor Rationale:** When previous stage capacities lack primitives to articulate differential checking without ambiguity, MSS-98 is declared as the specification row providing this capability within the external research atlas. (Actual transition requires an accepted lift record; lift status is unproved.)
- **Wire Packet(s):**

```text
  <differential_checking <canonical_input input_digest> <impl_A impl_hash_A> <impl_B impl_hash_B> <differential_receipt status_receipt>>
```

---

## 3. Runtime Pipeline Evaluator & Mathematical Core

- **Runtime Pipeline:** `Evaluator::targets.stage_098`
- **Primary Error Code:** `ERR_CHECKER_PAIR_DEFECT`
- **Atlas Capabilities:** `checker_pair`, `disagreement_receipt`, `differential_replay`, `independence_boundary`
- **Mathematical Core & Boundary:** Ruling D4: Counted in apparatus column (A) and atlas specification coverage ($C_{\rm atlas}$), never in object-language mathematical capability coverage ($C_{\rm object}$); object-language witness owed. A future licensed lift must discharge the retraction obligation $r_{98}(u_{98}(x))=x$; undefined terms return `NON_DESCENT`. AuthorityEffect: None.

---

## 4. Verification Obligation & Falsifier Boundary

- **Verification Obligation:** Execute independent implementations on identical canonical inputs; record any divergence as an explicit disagreement receipt and refuse silent merge. Note converse boundary: implementation agreement increases empirical confidence but does not prove mathematical correctness (especially under shared dependencies or specification defects).
- **Negative Counterexample:** Discrepant outputs between differential checkers that are averaged, silently merged, or arbitrarily resolved without root-cause witness are rejected.
- **Boundary Warning:** Level 98 records machine-checked finite verification receipts; it does not confer ambient authority or self-grant execution privileges.

---

## 5. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-98 within Epoch IX: Verification, Compilers, Benchmarks & Open Horizons.
   - Machine-checked verification obligation enforcing `ERR_CHECKER_PAIR_DEFECT` upon invalid candidate proposals.
   - Deterministic execution and discrepancy detection across differential implementations.
2. **What this does not support:**
   - Does not establish un-mechanized continuum properties or heuristic physics models.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
   - Does not treat implementation agreement as mathematical proof of correctness (shared dependencies or spec defects remain possible).
3. **The narrowest defensible claim:**
   - Stage MSS-98 accepts valid boundary packets and rejects negative counterexamples with `ERR_CHECKER_PAIR_DEFECT`.
   - Multi-checker agreement raises empirical confidence but leaves shared-mode vulnerabilities open to adversarial audit.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=99$ fixtures using the local CI test harness.
