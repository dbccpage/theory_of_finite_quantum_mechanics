---
documentation_contract: symbol-game-documentation/v1
title: "MSS-N Level 30: Spectral sequence pages"
kind: grammar-reference
level: 30
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
  row: MSS-31
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md
---

# MSS-N Level 30: Spectral sequence pages

**AuthorityEffect:** None.\
**Level:** Level 30 (Epoch I: Higher Category, Sheaves & Homotopy)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(30) = 128 + 8 \times (30 - 22) = 192$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::targets.stage_030` | Primary Error: `ERR_FILTRATION_DEFECT`\
**Atlas Capabilities:** `filtration`, `page_differential`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 30 resides within **Epoch I: Higher Category, Sheaves & Homotopy** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=30$.

- **Stage Classification:** Finite typed representation of spectral sequence pages without self-granting authority.
- **Mathematical Substrate:** Bigraded modules $E_r^{p,q}$ over a declared coefficient ring $R$ (e.g. $\mathbb{Z}$ or $\mathbb{Q}$), equipped with page differentials $d_r$ of bidegree $(r, 1-r)$ in cohomological convention (or $(-r, r-1)$ in homological convention).
- **Page Succession Law:** $E_{r+1}^{p,q} \cong H(E_r, d_r)^{p,q} = \ker(d_r^{p,q}) / \operatorname{im}(d_r^{p-r, q+r-1})$.
- **Invariant:** Retraction from predecessor stages belongs strictly to an attested lift record and is not asserted in the row contract.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet declares the current page index $r$, bigraded module dimensions, differential matrix representations, and the homology quotient data:

```text
<page_index bidegree differential_matrix cycle_submodule boundary_submodule>
```

- `page_index`: Natural number $r \ge 1$ indicating the spectral sequence page.
- `bidegree`: Integer coordinate pair $(p, q)$ identifying the bigraded cell.
- `differential_matrix`: Explicit matrix presentation of $d_r\colon E_r^{p,q} \to E_r^{p+r, q-r+1}$.
- `cycle_submodule`: Finite generator set for $\ker(d_r^{p,q})$.
- `boundary_submodule`: Finite generator set for $\operatorname{im}(d_r^{p-r, q+r-1})$.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_030`
- **Primary Error Code:** `ERR_FILTRATION_DEFECT`
- **Atlas Capabilities:** `filtration`, `page_differential`
- **Locally Checkable Verification Obligation:**
  1. **Differential Nilpotence:** Verify that the composite $d_r \circ d_r = 0$ vanishes identically:
     $$d_r^{p+r, q-r+1} \circ d_r^{p, q} = 0$$
  2. **Boundary Inclusion:** Verify $\operatorname{im}(d_r^{p-r, q+r-1}) \subseteq \ker(d_r^{p,q})$.
  3. **Page Succession Quotient:** Verify that $E_{r+1}^{p,q}$ matches the exact homology quotient module $\ker(d_r^{p,q}) / \operatorname{im}(d_r^{p-r, q+r-1})$.
- **Falsifier Boundary / Negative Counterexample:**
  - Any page differential candidate failing nilpotence ($d_r^2 \neq 0$) is rejected with `ERR_FILTRATION_DEFECT`.
  - Any candidate claiming persistence of a class to $E_{r+1}$ that is not a cycle ($d_r(x) \neq 0$) or that is a boundary ($x \in \operatorname{im}(d_r)$) without transport is rejected with `ERR_FILTRATION_DEFECT`.
- **Boundary Warning:** Level 30 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-30 within Epoch I: Higher Category, Sheaves & Homotopy.
   - Locally checkable verification obligation enforcing differential nilpotence $d_r^2 = 0$ and page homology succession $E_{r+1} = H(E_r, d_r)$ with `ERR_FILTRATION_DEFECT`.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-29 or assert universal convergence of the spectral sequence.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-30 accepts valid spectral page boundary packets and rejects nilpotence or succession violations with `ERR_FILTRATION_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=31$ cochain fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-29 $\to$ MSS-30)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{30}(u_{30}(x))=x$ has been licensed from MSS-29).
- **Predecessor Stage:** MSS-29 (`level_29_derived_obstruction.md`).
- **Successor Rationale:** When derived obstruction complexes (MSS-29) lack multi-page filtered bigraded spectral sequence primitives and page differential transport without ambiguity, MSS-30 is declared as the specification row providing this capability within the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{30}(u_{30}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
