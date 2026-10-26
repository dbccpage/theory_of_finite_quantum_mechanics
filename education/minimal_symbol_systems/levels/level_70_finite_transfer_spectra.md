---
documentation_contract: education-documentation/v1
title: "MSS-N Level 70: Finite transfer spectra"
kind: grammar-reference
level: 70
status: active
maturity: research
atlas_status: specified
evidence_grades:
  named: true
  syntax: true
  computed: true
  Lean: false
  gated: true
successor_status: declared
successor:
  row: MSS-71
  relation: declared_research_successor
  lift_status: unlicensed
lift_status: unlicensed
lift_proof_status: absent
lift_license_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
---

# MSS-N Level 70: Finite transfer spectra

**AuthorityEffect:** None.\
**Level:** Level 70 (Epoch VI: Hardness, Real Numbers & Continuum Fences)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(70) = 128 + 8 \times (70 - 22) = 512$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*\
**Runtime Pipeline:** `Evaluator::targets.stage_070` | Primary Error: `ERR_TRANSFER_MATRIX_DEFECT`\
**Atlas Capabilities:** `transfer_matrix`, `characteristic_poly`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 70 resides within **Epoch VI: Hardness, Real Numbers & Continuum Fences** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=70$.

- **Stage Classification:** Finite typed representation of transfer matrices, exact rational characteristic polynomials, and certified algebraic spectral certificates without self-granting authority.
- **Mathematical Carrier & Spectral Semantics:**
  1. **Transfer Operator:** A finite transfer matrix $T \in M_{m \times m}(\mathbb{Q})$ governing discrete 1D lattice transfers or transition weights.
  2. **Exact Characteristic Polynomial (Primary Invariant):**
     The monic determinant polynomial:
     $$P(\lambda) = \det(\lambda I_m - T) = \lambda^m + \sum_{k=0}^{m-1} c_k \lambda^k \in \mathbb{Q}[\lambda]$$
     computed via exact division-free rational algorithms (such as the Berkowitz algorithm over $\mathbb{Q}$). This exact polynomial constitutes the primary checkable finite invariant.
  3. **Algebraic Spectral Certificates:**
     If individual eigenvalues $\lambda_j$ are exposed or evaluated, each eigenvalue must be accompanied by an exact algebraic root certificate conforming to Level 69:
     - An isolating rational interval $I_j = (a_j, b_j) \subset \mathbb{Q}$ ($a_j < b_j$) certified by a Sturm sequence for $P(\lambda)$ satisfying $V(a_j) - V(b_j) = 1$.
     - Floating-point approximations lacking exact rational isolating bounds are explicitly refused.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the transfer matrix dimension, rational entries, exact characteristic polynomial, and optional Sturm root-isolating intervals:

```text
<transfer_matrix characteristic_poly eigenvalue_certificates>
```

- `transfer_matrix`: Dimension $m \in \mathbb{N}_{\ge 1}$ and rational matrix entries $T_{ij} \in \mathbb{Q}$ for $1 \le i, j \le m$.
- `characteristic_poly`: Rational polynomial $P(\lambda) \in \mathbb{Q}[\lambda]$ of degree $m$.
- `eigenvalue_certificates`: Optional array of isolating intervals $(a_j, b_j) \subset \mathbb{Q}$ with exact Sturm root counts certifying distinct real eigenvalues.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_070`
- **Primary Error Code:** `ERR_TRANSFER_MATRIX_DEFECT`
- **Atlas Capabilities:** `transfer_matrix`, `characteristic_poly`
- **Locally Checkable Verification Obligation:**
  1. **Matrix Well-Formedness:** Verify $T$ is an $m \times m$ matrix with rational entries.
  2. **Exact Determinant Polynomial Recomputation:** Recompute the characteristic polynomial $P_{\text{host}}(\lambda) = \det(\lambda I_m - T)$ using exact rational arithmetic and assert coefficient equality with `characteristic_poly`.
  3. **Eigenvalue Certificate Validation:** For each reported eigenvalue isolating interval $(a_j, b_j)$, compute the Sturm sequence for $P(\lambda)$ and verify $V(a_j) - V(b_j) = 1$ and $P(a_j) \cdot P(b_j) \ne 0$.
- **Falsifier Boundary / Negative Counterexample:**
  - An asserted characteristic polynomial diverging from $\det(\lambda I_m - T)$ is rejected with `ERR_TRANSFER_MATRIX_DEFECT`.
  - An asserted eigenvalue without an isolating interval witness or whose interval contains zero roots ($V(a) - V(b) = 0$) or multiple roots ($V(a) - V(b) \ge 2$) is rejected with `ERR_TRANSFER_MATRIX_DEFECT`.
- **Boundary Warning:** Level 70 records computed/gated verification receipts; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-70 within Epoch VI: Hardness, Real Numbers & Continuum Fences.
   - Computed/gated verification receipts enforcing exact characteristic polynomial recomputation and Sturm-certified eigenvalue isolation.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-69 or assert infinite-volume thermodynamic limit convergence.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-70 accepts valid exact transfer matrices and characteristic polynomials, rejecting mismatched polynomials or uncertified eigenvalues with `ERR_TRANSFER_MATRIX_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=71$ analytic limit fence fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-69 $\to$ MSS-70)

- **Lift Status:** `unlicensed` (lift_license_status: unlicensed, lift_proof_status: absent; design-stage specification row; no conservative embedding or retraction proof $r_{70}(u_{70}(x))=x$ has been licensed from MSS-69).
- **Predecessor Stage:** MSS-69 (`level_69_algebraic_real_numbers.md`).
- **Successor Rationale:** When individual algebraic reals (MSS-69) lack matrix representation and operator spectral invariants, MSS-70 is declared as the specification row providing transfer matrices and characteristic polynomials within the external research atlas.
- **Conditional Lift Obligation:** Any future accepted lift into MSS-70 must exhibit $(u_{70}, r_{70})$ satisfying $r_{70}(u_{70}(x)) = x$. No predecessor lift is currently claimed (`lift_status: unlicensed`, `lift_proof_status: absent`).
