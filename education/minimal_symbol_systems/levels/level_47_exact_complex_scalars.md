---
documentation_contract: education-documentation/v1
title: "MSS-N Level 47: Exact Gaussian-rational scalars"
kind: grammar-reference
level: 47
status: active
maturity: research
atlas_status: specified
evidence_grades:
  named: true
  syntax: true
  computed: true
  Lean: false
  gated: true
successor:
  row: MSS-48
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
---

# MSS-N Level 47: Exact Gaussian-rational scalars

**AuthorityEffect:** None.\
**Level:** Level 47 (Epoch IV: Finite Quantum Mechanics & Entanglement)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(47) = 128 + 8 \times (47 - 22) = 328$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::targets.stage_047` | Primary Error: `ERR_RATIONAL_PAIR_DEFECT`\
**Atlas Capabilities:** `rational_pair`, `conjugation`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 47 opens **Epoch IV: Finite Quantum Mechanics & Entanglement** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=47$.

- **Stage Classification:** Finite typed representation of exact Gaussian-rational scalar arithmetic without self-granting authority.
- **Mathematical Substrate:** The Gaussian rational field $\mathbb{Q}(i) = \{a + bi \mid a, b \in \mathbb{Q}, i^2 = -1\}$, represented as exact ordered rational pairs $(a, b) \in \mathbb{Q} \times \mathbb{Q}$:
  - **Field Addition:** $(a_1, b_1) + (a_2, b_2) = (a_1 + a_2, b_1 + b_2)$
  - **Field Multiplication:** $(a_1, b_1) \times (a_2, b_2) = (a_1 a_2 - b_1 b_2, \, a_1 b_2 + a_2 b_1)$
  - **Multiplicative Inverse:** For $(a, b) \neq (0, 0)$:
    $$(a, b)^{-1} = \left(\frac{a}{a^2 + b^2}, \, \frac{-b}{a^2 + b^2}\right)$$
  - **Complex Conjugation Involution:** $(a, b)^* = (a, -b)$
  - **Exact Squared Modulus:** $|(a, b)|^2 = a^2 + b^2 \in \mathbb{Q}_{\ge 0}$
- **Exact Scalar Policy Boundary:**
  Level 47 formalizes $\mathbb{Q}(i)$, **not arbitrary complex numbers $\mathbb{C}$ or algebraic extensions**. Irrationals such as $1/\sqrt{2}$ and general roots of unity $e^{i\theta}$ do not belong to $\mathbb{Q}(i)$. All downstream quantum stages (MSS-48 through MSS-60) must operate either over $\mathbb{Q}(i)$ with rational-squared normalization or via projective rays.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the real rational component, imaginary rational component, verified field operation identities, conjugation, and squared modulus:

```text
<rational_real rational_imag field_operations complex_conjugation squared_modulus>
```

- `rational_real`: Exact rational number $a \in \mathbb{Q}$ ($p/q$ with $q > 0, \gcd(p,q)=1$).
- `rational_imag`: Exact rational number $b \in \mathbb{Q}$.
- `field_operations`: Record of field axioms verified over declared operations.
- `complex_conjugation`: Exact conjugate pair $(a, -b)$.
- `squared_modulus`: Rational evaluation $a^2 + b^2 \in \mathbb{Q}_{\ge 0}$.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_047`
- **Primary Error Code:** `ERR_RATIONAL_PAIR_DEFECT`
- **Atlas Capabilities:** `rational_pair`, `conjugation`
- **Locally Checkable Verification Obligation:**
  1. **Exact Rational Representation:** Verify that both components are represented as canonical coprimes $p/q \in \mathbb{Q}$ with non-zero denominators.
  2. **Field Axioms Check:** Recompute addition, multiplication, and reciprocal identities $(z \cdot z^{-1} = 1)$ in exact rational arithmetic.
  3. **Conjugation & Norm Invariant:** Verify that $z \cdot z^* = (|z|^2, 0)$ with $|z|^2 \ge 0$.
- **Falsifier Boundary / Negative Counterexample:**
  - Any scalar encoded as an untyped floating-point approximation or inexact decimal is rejected with `ERR_RATIONAL_PAIR_DEFECT`.
  - Division by zero $(0, 0)^{-1}$ or arithmetic violating field closure is rejected with `ERR_RATIONAL_PAIR_DEFECT`.
- **Boundary Warning:** Level 47 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-47 within Epoch IV: Finite Quantum Mechanics & Entanglement.
   - Locally checkable verification obligation enforcing exact Gaussian rational field arithmetic $\mathbb{Q}(i)$ without floating-point error.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-46 or assert continuous complex analysis ($\mathbb{C}$) or general transcendental phases.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-47 accepts valid Gaussian rational scalar pairs in $\mathbb{Q}(i)$ and rejects inexact or malformed representations with `ERR_RATIONAL_PAIR_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=48$ finite Hilbert state fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-46 $\to$ MSS-47)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{47}(u_{47}(x))=x$ has been licensed from MSS-46).
- **Predecessor Stage:** MSS-46 (`level_46_self_host_and_termination.md`).
- **Successor Rationale:** When discrete syntactic evaluator terms (MSS-46) cannot represent complex phase interference, Gaussian rational amplitude rings, or algebraic involutions, MSS-47 is declared as the specification row providing this capability within the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{47}(u_{47}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
