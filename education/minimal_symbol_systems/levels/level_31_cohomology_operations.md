---
documentation_contract: education-documentation/v1
title: "MSS-N Level 31: Cohomology operations"
kind: grammar-reference
level: 31
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
  row: MSS-32
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
---

# MSS-N Level 31: Cohomology operations

**AuthorityEffect:** None.\
**Level:** Level 31 (Epoch I: Higher Category, Sheaves & Homotopy)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(31) = 128 + 8 \times (31 - 22) = 200$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::targets.stage_031` | Primary Error: `ERR_OPERATION_DEGREE_DEFECT`\
**Atlas Capabilities:** `operation_degree`, `naturality_square`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 31 resides within **Epoch I: Higher Category, Sheaves & Homotopy** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=31$.

- **Stage Classification:** Finite typed representation of stable cohomology operations without self-granting authority.
- **Mathematical Substrate:** Given a cochain complex $C^\bullet(X; R)$ over a declared coefficient ring $R$ (e.g. $\mathbb{F}_2 = \mathbb{Z}/2\mathbb{Z}$ for Steenrod squares $Sq^i$, $\mathbb{F}_p$ for Steenrod reduced powers / Bockstein $\beta$, or commutative ring $R$ for the cup product $\smile$), a cohomology operation is a natural transformation of cohomology functors:
  $$\theta \colon H^n(-; R) \longrightarrow H^{n+k}(-; R')$$
- **Well-Definedness Laws:**
  1. **Representative Independence:** $\theta^\sharp(z + \delta b) - \theta^\sharp(z) \in B^{n+k}(X; R')$ for any cocycle $z \in Z^n(X; R)$ and cochain $b \in C^{n-1}(X; R)$.
  2. **Functorial Naturality:** For every cochain map $f^\sharp \colon C^\bullet(Y) \to C^\bullet(X)$, the induced diagram commutes:
     $$f^* \circ \theta = \theta \circ f^*$$

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the coefficient ring, operation family, degree shift, naturality verification square, and representative independence witness:

```text
<coefficient_ring operation_family operation_degree naturality_square representative_map>
```

- `coefficient_ring`: Declared ring identifier (e.g., `F2`, `Fp`, `Z`).
- `operation_family`: Explicit family designation (e.g., `steenrod_square`, `bockstein`, `cup_product`).
- `operation_degree`: For a unary operation, degree shift $k \ge 0$. A cup product is binary, with two input degrees $p,q$ and output degree $p+q$; it requires a separate two-input signature.
- `naturality_square`: Commuting square cochain data $\langle f^\sharp, \theta^\sharp, f^* \circ \theta - \theta \circ f^* \rangle$.
- `representative_map`: Proof witness that coboundary additions evaluate to coboundaries in the target.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_031`
- **Primary Error Code:** `ERR_OPERATION_DEGREE_DEFECT`
- **Atlas Capabilities:** `operation_degree`, `naturality_square`
- **Locally Checkable Verification Obligation:**
  1. **Degree & Ring Validity:** Check that the operation maps cocycles of degree $n$ to cocycles of degree $n+k$ in the declared coefficient ring $R$.
  2. **Representative Independence:** Evaluate $\theta^\sharp(z + \delta b) - \theta^\sharp(z)$ and verify that this difference is a coboundary $\delta(\dots)$ in $B^{n+k}(X; R')$.
  3. **Naturality Commutativity:** For the declared test cochain morphism $f^\sharp$, evaluate the difference $f^*(\theta(z))-\theta(f^*z)$ and exhibit a cochain whose coboundary equals it. No norm is assumed on an arbitrary coefficient ring.
- **Falsifier Boundary / Negative Counterexample:**
  - An operation candidate that produces distinct cohomology classes when evaluated on different cocycle representatives of the same class is rejected with `ERR_OPERATION_DEGREE_DEFECT`.
  - An operation that fails naturality along a declared cochain map is rejected with `ERR_OPERATION_DEGREE_DEFECT`.
- **Boundary Warning:** Level 31 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-31 within Epoch I: Higher Category, Sheaves & Homotopy.
   - Locally checkable verification obligation enforcing cocycle representative independence and naturality for declared cohomology operations.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-30 or assert the full Adem relations without explicit generators.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-31 accepts valid natural cohomology operation boundary packets and rejects representative defects with `ERR_OPERATION_DEGREE_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=32$ coarse graining fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-30 $\to$ MSS-31)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{31}(u_{31}(x))=x$ has been licensed from MSS-30).
- **Predecessor Stage:** MSS-30 (`level_30_spectral_sequence_pages.md`).
- **Successor Rationale:** When spectral sequence page calculations (MSS-30) lack stable cohomology operations (such as Steenrod squares or cup products) to distinguish homotopically distinct spaces with isomorphic cohomology groups, MSS-31 is declared as the specification row providing this capability within the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{31}(u_{31}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
