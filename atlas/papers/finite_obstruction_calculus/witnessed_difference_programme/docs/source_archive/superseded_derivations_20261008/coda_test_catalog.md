# CODA Test Catalog and Structural Failure Modes

**AuthorityEffect:** None.

## 1. Executive Summary

This document catalogs the complete suite of verification, unit, integration, and high-dimensional stress tests completed across the CODA stack (`apps/coda` and `coda_gtla`). It details the expected versus actual outcomes of each test and provides an exact, mathematically grounded analysis of **how and where the CODA framework will fail**, structured directly around six foundational reference papers in the Finite Obstruction Calculus series (`atlas/papers/finite_obstruction_calculus/`):

1. **Paper 004 (AF-005):** *Role Non-Impersonation and Authority Preservation in Agentic AI*
2. **Paper 005 (AF-031):** *The Authority Gap*
3. **Paper 027 (AF-001):** *The Authority Firewall: A Machine-Checked Separation of Evidence from Authority in Finite Systems*
4. **Paper 028 (AF-003):** *Finite Authority and Non-Terminal Computation*
5. **Paper 029 (FOC-002):** *The Anomalon Boundary: Primitive Difference, Structure, and the Authority Boundary of Meaning*
6. **Paper 030 (OE-018):** *The Authority Firewall and Verification Limits*

---

## 2. Completed Test Suite Catalog

### Table 1: End-to-End Stress Tests & High-Dimensional Scaling

Runtimes were re-measured on 2026-09-23 after the repair recorded in
`docs/adversarial_review_2026-09-23.md` §7: every Layer 1 solve now returns an exact
certificate (primal repair and dual witness of equal value), and authorization runs
through a signed external grant. The earlier 0.02–0.05 s figures were measured on the
unrepaired pipeline and are **withdrawn** (2026-09-23). A figure below is one run on
one machine; the test asserts only the bound.

| Test ID | Test Target | Topology / Vertices | Expected Result | Actual Result | Runtime | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ST-01** | `test_high_dim_graph_1000_vertices_runtime_and_witness_pairing` | Directed cycle + chords, $V=1000, E=1100$ | Runtime $< 3.0$s; $\Phi_1 = 1000$; Dual witness $y^* \in \ker(D_0^T)$ with $\|y^*\|_\infty \le 1$; $\langle y^*, \Omega \rangle = 1000$; Terminal `CLOSED_RESIDUAL` | $\Phi_1 = 1000$; $D_0^T y^* = 0$ holds; $\|y^*\|_\infty = 1$; Pairing $= 1000$; `CLOSED_RESIDUAL` | ≈0.3s | **PASS** |
| **ST-02** | `test_high_dim_graph_1500_vertices_scaling` | Directed cycle + chords, $V=1500, E=1600$ | Runtime $< 3.0$s; $\Phi_1 = 1500$; $D_0^T y^* = 0$; Pairing $= 1500$ | $\Phi_1 = 1500$; exact kernel pairing matches | ≈0.5s | **PASS** |
| **ST-03** | `test_high_dim_conservative_flow_zero_defect` | Spanning potential $f(i)=i$, $V=1000, E=1100$, verified external grant | $\Phi_1 = 0$; $\Gamma_2 = 0$; Dual witness `None`; Terminal `AUTHORIZED` | $\Phi_1 = 0$; Witness `None`; `AUTHORIZED`, token bound to the evidence digest. The row formerly read "licensed" (a flag); a flag no longer authorizes. | < 6.0s asserted (two evaluations) | **PASS** |
| **ST-04** | `test_high_dim_firewall_unlicensed_routes_to_closed_residual` | Conservative flow $\Phi_1 = 0$, $V=1000$, unlicensed | Terminal `REFUSED`; Firewall `ROUTE_REFUSED`; No token (GTLA-T9) | Terminal `REFUSED`; `ROUTE_REFUSED`; `auth_token=None` | — | **PASS** |
| **ST-05** | `test_coda_cli_stress_test_entrypoint` | CLI `stress-test --vertices 1000` | Exit code 0 only if every verdict passes; receipts for all four audit criteria | Exit code 0; Runtime bound PASS; Nullspace PASS; Bound PASS; Pairing PASS | — | **PASS** |
| **ST-06** | `test_budget_exhaustion_inside_layer_one_refuses` | Dense non-incidence $D_0$ ($60 \times 40$), `max_seconds=0.05` | The budget interrupts the exact simplex inside Layer 1; `REFUSED`; $\Phi_1, \Gamma_2$ reported unknown | `REFUSED`; evidence `phi1 = gamma2 = None` | < 0.5s asserted | **PASS** |
| **ST-07** | `test_budget_exhaustion_by_step_limit_refuses` | $V=1000$ graph, `max_steps=50` | The step budget exhausts deterministically; `REFUSED`; no residual pair, no token | `REFUSED`; `residual_pair = None` | — | **PASS** |
| **ST-08** | `test_surviving_residual_is_read_back_from_the_register` | $V=1000$ graph, $\Phi_1 = 1000$ | The anomalon is read back from the persistent register through a fresh handle | One `RETAINED_OPEN` record with $\Phi_1 = 1000$ | — | **PASS** |

---

### Table 2: CODA Nine-Layer Unit & Integration Tests (`apps/coda/tests/`)

| Test ID | Layer / Module | Invariant Verified | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **L1-01** | Layer 1 (CODA-FOC) | Vanishing defect $\Omega = 0$ | $\Phi_1 = 0, \Gamma_2 = 0$, dual witness `None` | Exact zero rational, witness `None` | **PASS** |
| **L1-02** | Layer 1 (CODA-FOC) | Obstructed cochain $[1, 0]^T \notin \mathrm{im}(D_0)$ | $\Phi_1 = 1, \Gamma_2 = 0$, dual witness in $\ker(D_0^T)$ with $\|y^*\|_\infty \le 1$ | Exact rational $\Phi_1 = 1$, certified dual witness | **PASS** |
| **L2-01** | Layer 2 (CODA-MUR) | Section overlap transport commutation | Compatible overlap yields $\mathsf{Loss} = 0$ | Record succeeded, loss exact zero | **PASS** |
| **L2-02** | Layer 2 (CODA-MUR) | Incompatible section overlap | Incompatible overlap yields $\mathsf{Loss} > 0$, layer marks failure | Record failed, loss exact $1$ | **PASS** |
| **L3-01** | Layer 3 (CODA-CS) | Coarse / fine profile projection | Consistent projection preserves fiber | Record succeeded, consistent `True` | **PASS** |
| **L3-02** | Layer 3 (CODA-CS) | Inconsistent continuum projection | Projection mapping outside coarse range fails | Record failed, consistent `False` | **PASS** |
| **L4-01** | Layer 4 (CODA-CS-Q) | Metric separation & collision bounds | Identical values on a declared-compatible overlap are agreement, not a collision; separation $0$ | Record succeeded, separation exact $0$ | **PASS** |
| **L4-02** | Layer 4 (CODA-CS-Q) | Strict positive metric separation | Perturbed section $(3/4)$ yields separation $1/4$ | Record succeeded, separation exact $1/4$ | **PASS** |
| **L5-01** | Layer 5 (CODA-Q) | Convex interval enclosure | Inhabited interval $[0, 1]$ yields diameter $1$ | Record succeeded, diameter exact $1$ | **PASS** |
| **L5-02** | Layer 5 (CODA-Q) | Inverted enclosure detection | Interval $[2, 1]$ triggers enclosure violation | Record failed, inverted interval rejected | **PASS** |
| **L6-01** | Layer 6 (CODA-A) | Cokernel residue accounting | $\Phi_1 = 0, \Gamma_2 = 0$ yields zero residue | Record succeeded, `has_residual = False` | **PASS** |
| **L6-02** | Layer 6 (CODA-A) | Anomalon retention | $\Phi_1 > 0, \Gamma_2 = 0$ is retained, not smoothed | Record succeeded, `has_residual = True`, Anomalon diagnostic emitted. Layer 6 records retention; the firewall writes the register entry (ST-08). | **PASS** |
| **L7-01** | Layer 7 (CODA-OR) | Hard refusal sieve baseline | Non-empty candidate sieve passes | Record succeeded, `refused = False` | **PASS** |
| **L7-02** | Layer 7 (CODA-OR) | Empty candidate sieve trigger | Empty candidate sieve triggers hard refusal | Record failed, `refused = True` (OR-T5) | **PASS** |
| **L8-01** | Layer 8 (CODA-FDA) | Non-promotion gate (unlicensed) | $\Phi_1 = 0$, `licensed = False` routes to `CLOSED_RESIDUAL` | `ROUTE_CLOSED_RESIDUAL`, token `None` | **PASS** |
| **L8-02** | Layer 8 (CODA-FDA) | A license claim alone | $\Phi_1 = 0$ with `fda_license_granted = True`: Layer 8 never mints and never permits | No `PERMIT_AUTHORIZED`, token `None`. ~~`PERMIT_AUTHORIZED`, valid token granted~~ **WITHDRAWN 2026-09-23**: a flag minted a token. Authorization belongs to the firewall, on a verified `AuthorityGrant`. | **PASS** |
| **L8-03** | Layer 8 (CODA-FDA) | Upstream refusal cascade | Upstream refusal forces `ROUTE_REFUSED` | `ROUTE_REFUSED`, token `None` | **PASS** |
| **L9-01** | Layer 9 (CODA-GTLA) | Terminal disjointness | Terminal partition into $\mathbb{T}_{\mathsf{auth}} \amalg \mathbb{T}_{\mathrm{res}} \amalg \mathbb{F}_{\mathrm{term}}$ | Mutually exclusive flags: only `is_closed_residual` true | **PASS** |
| **PIP-01**| Pipeline Flow | End-to-end authorized flow under a verified external grant | All 9 layers succeed; outcome `AUTHORIZED` | Outcome `AUTHORIZED`, 9 layer records clean | **PASS** |
| **PIP-02**| Pipeline Flow | End-to-end anomalon flow | Obstructed instance; outcome `CLOSED_RESIDUAL` | Outcome `CLOSED_RESIDUAL`, Anomalon registered | **PASS** |
| **PIP-03**| Pipeline Flow | End-to-end refusal flow | Empty sieve; outcome `REFUSED` | Outcome `REFUSED`, reason records OR-T5 | **PASS** |
| **FW-01** | Firewall Suite | Internal authority minting block | Proposer / Evaluator cannot instantiate `AuthorityToken` without external license | Raises `PermissionError`; token forgery blocked | **PASS** |
| **FW-03** | Firewall Suite | Token minting | The firewall's minting helper, called with a fabricated grant or with a genuine grant whose nonce is unspent | Raises `PermissionError`; only a verified, spent grant yields a sealed token | **PASS** |
| **FW-02** | Firewall Suite | Firewall audit | Named checks (disjointness, token iff authorized, token validity, grant presented, zero residual, license claim, independent certificate check) on an unlicensed and a granted instance | `firewall_audit_passed` with empty `failed_checks`; an injected breach is reported as failed, not crashed on | **PASS** |
| **BR-01** | Infrastructure Bridge| Rust workspace detection | `omega_engine/crates_rs` cargo manifest discovered | Found workspace, 42 crates enumerated | **PASS** |
| **BR-02** | Infrastructure Bridge| Rust solver IPC payload | Matrix boundary serialized to exact integer pairs | Status `PYTHON_EXACT_RUST_NOT_EXECUTED`: $\Phi_1$ comes from the exact Python solver; no Rust runner is invoked | **PASS** |
| **BR-03** | Infrastructure Bridge| Exact solver adapter parity | `compute_quotient_distance` matches dual witness | Exact rational $\Phi_1$ and dual witness certified | **PASS** |
| **TRI-01**| Triad Architecture | Role Non-Impersonation (Paper 004) | A proposer submits without authority flags; cannot self-authorize | Evaluated as `PROPOSER`; routes to `CLOSED_RESIDUAL`, token `None`. The Alpha client's own test moved to `apps/alpha/tests/test_client.py`. | **PASS** |
| **TRI-02**| Triad Architecture | Authority Gap Invariant (Paper 005) | $\Phi_1 = 0 \land \Gamma_2 = 0$ requires a verified external grant | Unlicensed routes to `CLOSED_RESIDUAL`; a bare `True` claim routes to `REFUSED`; a verified grant routes to `AUTHORIZED` | **PASS** |
| **TRI-03**| Triad Architecture | Anomalon Boundary (Paper 029) | Surviving cokernels registered with SHA-256 fingerprint; anti-smoothing | Recorded in `AnomalonRegistry`; zero defect registration refused | **PASS** |
| **TRI-04**| Triad Architecture | Non-Terminal Budget Guard (Paper 028) | Computation loops bounded by $T < T_{\max}$; timeout halts into refusal | Raises `BudgetExhaustedError`; routes to `REFUSED` (`BudgetUnknown`) | **PASS** |
| **TRI-05**| Triad Architecture | Verification Limits (Paper 030) | Self-referential / undecidable envelope halts closed into refusal | Routes to `REFUSED` (`HALT_GUARD_7_BREACH`); no permissive license | **PASS** |
| **TRI-06**| Triad Architecture | Halt Guard 1 Impersonation (Paper 027)| Caller claiming `AUTHORITY` without license halts closed | Routes to `REFUSED` (`HALT_GUARD_1_BREACH`); caller blocked | **PASS** |

---

## 3. How and Where CODA Will Fail: Six Foundational Failure Modes

The CODA architecture is deliberately engineered to **fail closed**. It does not attempt to "heal" defects, smooth away discrepancies, or manufacture artificial consensus. Below is an exhaustive structural mapping of the exact points where CODA will fail, keyed to the foundational reference papers:

```
                            [ Incoming Problem Instance ]
                                          │
                                          ▼
   [ Layer 1-5: Detection & Transport ] ──► Failure Mode 5 (Paper 029): Non-zero coherent defect
                                          │  Cannot smooth or discard; locked into Anomalon register.
                                          ▼
   [ Layer 7: Omniversal Re-Presentation ]   ──► Failure Mode 4 (Paper 028): Budget exhaustion or empty sieve
                                          │  Terminates in REFUSED (F_term); cannot continue loop.
                                          ▼
   [ Layer 8: Authority Firewall ]      ──► Failure Mode 1 (Paper 004): Proposer/Evaluator mints token
                                          │  PermissionError; internal minting strictly blocked.
                                          │
                                          ──► Failure Mode 2 (Paper 005): Zero-defect without license
                                          │  Routes to CLOSED_RESIDUAL; green alone does not authorize.
                                          │
                                          ──► Failure Mode 3 (Paper 027): Violation of any 7 halt guards
                                          │  Coproduct split forbids promotion to T_auth.
                                          │
                                          ──► Failure Mode 6 (Paper 030): Recursive self-auditing
                                             Lacks external trust root (C4); fails closed.
```

---

### Failure Mode 1: Role Impersonation & Rubber-Stamp Forgery

* **Governing Paper:** `004_role_non_impersonation_and_authority_preservation` (AF-005, §1, §4, §5)
* **Mathematical Statement:**
  $$\boxed{ p \in \mathcal{P} \not\Rightarrow \mathsf{Auth}(p) }$$
* **Structural Mechanism:**
  In the Omega governance tower, the six tower positions ($\partial, \mathbb{A}, \chi, \mathfrak{O}, \kappa, \Lambda\Omega$) form non-identifiable roles. A proposer generating candidates $p \in \mathcal{P}$, an evaluator computing $\Phi_1$, or a transport functor computing $\tau^\sharp$ cannot impersonate an authority terminal.
* **How and Where CODA Fails:**
  * If any internal pipeline component, solver, or subagent attempts to instantiate an `AuthorityToken` directly, the constructor raises `PermissionError`: a token needs a seal that only the firewall's `_mint_token` (in `apps/coda/domain/authority.py`) produces, and only for an `AuthorityGrant` that the keyring has verified and whose nonce it has spent.
  * ~~In `apps/coda/domain/layers/layer8_fda.py`, the firewall verifies `problem.fda_license_granted`. If `False`, authority is structurally impossible.~~ **WITHDRAWN 2026-09-23**: a `True` flag was enough to mint a token. Now `AuthorityFirewallEngine` authorizes only on an `AuthorityGrant` signed by a key in the caller-supplied keyring, bound to this problem's digest and evidence digest, naming this proposer, with an unspent nonce. A flag, a bool or any other object is refused (`HALT_GUARD_5_BREACH`). Layer 8 alone never mints.

---

### Failure Mode 2: The Authority Gap & Counterfeit Green Descent

* **Governing Paper:** `005_the_authority_gap` (AF-031, §4, §6, §7)
* **Mathematical Statement:**
  $$\Phi_1(\Omega) = 0 \not\Rightarrow \text{Genuine Semantic Correctness}$$
  $$\text{Under Lemma O1: Observers do not create defects; they erase them.}$$
* **Structural Mechanism:**
  A lossy observation profile or an adversarial evaluator can yield zero quotient defect ($\Phi_1 = 0$) simply by projecting onto a degenerate carrier. This is the **Exactness Fraud Criterion**: an unprincipled optimizer minimizes $\Phi_1$ by selecting an observer that hides defects rather than repairing them.
* **How and Where CODA Fails:**
  * When CODA evaluates an instance with exact zero quotient distance ($\Phi_1 = 0$) and zero cocycle defect ($\Gamma_2 = 0$), but without external institutional authority, Layer 8 **hard-refuses** authorization and routes to `TerminalKind.CLOSED_RESIDUAL`.
  * In our high-dimensional stress test `test_high_dim_firewall_unlicensed_routes_to_closed_residual`, a 1,000-vertex graph with perfectly conservative circulation ($\Phi_1 = 0$) is refused authorization and routed to `CLOSED_RESIDUAL`. CODA fails to promote diagnostic perfection to authority.

---

### Failure Mode 3: The Seven Halt Guards of the Authority Firewall

* **Governing Paper:** `027_the_authority_firewall_a_machine_checked_separation_of_evidence_from_authority_in_finite_systems` (AF-001, §1, §3)
* **Mathematical Statement:**
  $$\mathbb{T} = \mathbb{T}_{\mathsf{auth}} \oplus (\mathbb{T}_{\mathrm{res}} + \mathbb{F}_{\mathrm{res}}), \quad \operatorname{Nat}(\Omega_{\Lambda\Omega}, \mathsf{Auth}) = \varnothing$$
* **Structural Mechanism:**
  Terminal outcomes occupy mutually disjoint summands of a coproduct type. Evidence lane outputs (CODA-FOC) and authority lane outputs (CODA-FDA) are separated by seven machine-checked halt guards ($G_1$ through $G_7$):
  1. **$G_1$ (Role Separation):** The caller role is exactly `PROPOSER`, `REFEREE` or `AUTHORITY`; `AUTHORITY` requires a verified grant.
  2. **$G_2$ (Exact Arithmetic):** The problem passes intake, the evidence is exact rational, and the evidence is bound to the problem's digest.
  3. **$G_3$ (Dual Witness Validation):** A supplied witness has the right shape, $\|y\|_\infty \le 1$, $D_0^T y = 0$ and $\langle y, x \rangle = \Phi_1$; with $\Phi_1 = 0$ the guard is recorded as not applicable.
  4. **$G_4$ (Cocycle Consistency):** $\Gamma_2 \ge 0$; $\Gamma_2 > 0$ refuses.
  5. **$G_5$ (Authority Gap):** Zero defect without a grant closes as residual; a bare claim or an unverified, mis-bound or replayed grant refuses.
  6. **$G_6$ (Non-Terminal Budget):** Time and step budgets, checked inside the Layer 1 solver, not only between layers.
  7. **$G_7$ (Verification Limits):** A self-referential or undecidable envelope refuses; only `None` or `False` pass.

  This list is the one the code enforces (`AuthorityFirewallEngine.GUARD_1` to `GUARD_7`). An earlier list named seven other conditions (Well-Formedness, Quotient Defect, Cocycle Defect, Transport Loss, Continuum Profile, Refusal Cascade, External License) that shared only the word "cocycle" with the code; it is **WITHDRAWN 2026-09-23**. Its layer conditions are now enforced as "any failed layer record refuses", not as guards.
* **How and Where CODA Fails:**
  * If **any single guard** fails ($G_i = \text{Fail}$), the transition to $\mathbb{T}_{\mathsf{auth}}$ is blocked by constructor disjointness.
  * CODA fails closed: it emits an immutable diagnostic audit trail and routes the packet to either `ROUTE_CLOSED_RESIDUAL` (if evidence survives) or `ROUTE_REFUSED` (if consistency fails).

---

### Failure Mode 4: Non-Terminal Computation & Resource Exhaustion

* **Governing Paper:** `028_finite_authority_and_non_terminal_computation` (AF-003, §1, §4, §9)
* **Mathematical Statement:**
  $$\text{Universal symbol manipulation is not universal authority.}$$
  $$\text{Reasoning authority is not generated; it is terminalized.}$$
* **Structural Mechanism:**
  A proposal engine (such as an LLM or unconstrained heuristic solver) can generate unbounded reasoning traces without ever terminating at an admissible terminalizer. When resource budgets are exhausted, or when candidate sieves become empty, the system cannot guess or fabricate an answer.
* **How and Where CODA Fails:**
  * If an evaluation exhausts its time or step budget (tested in `test_budget_exhaustion_inside_layer_one_refuses` and `test_budget_exhaustion_by_step_limit_refuses`), or if candidate generation empties the support sieve (as tested in `test_layer7_or_hard_refusal_sieve`), CODA terminates in `TerminalKind.REFUSED` ($\mathbb{F}_{\mathrm{term}}$). The budget is ticked on every solver pivot, so a long Layer 1 solve is interrupted rather than overrun.
  * CODA strictly refuses to fall back to heuristics or majority voting; non-terminal computation is terminalized as hard failure.

---

### Failure Mode 5: The Anomalon Boundary & Residual Invariance

* **Governing Paper:** `029_the_anomalon_boundary` (FOC-002, §0, §1, §3)
* **Mathematical Statement:**
  $$\mathrm{Real}_0 = \text{Primitive Difference} \cup \text{Structure}$$
  $$[x] \in V / \mathrm{im}(D_0), \qquad \Phi_1([x]) > 0$$

  ~~$x - C x \in \ker(C) \subset V / \mathrm{im}(C)$~~ **WITHDRAWN 2026-09-23**: $\ker C$ is a subspace of $V$ and $V/\mathrm{im}(C)$ is a quotient, so neither contains the other. For an idempotent $C$, $V = \mathrm{im}(C) \oplus \ker(C)$ and the quotient map restricts to an isomorphism $\ker(C) \cong V/\mathrm{im}(C)$. The identification is that isomorphism (A-T6), not an inclusion.
* **Structural Mechanism:**
  When an obstruction cannot be repaired within the declared repair class, it represents an irreducible primitive difference. If the defect is coherent ($\Phi_1 > 0, \Gamma_2 = 0$), it is an **Anomalon**—a genuine topological invariant of the system.
* **How and Where CODA Fails:**
  * A non-zero quotient obstruction ($\Phi_1 > 0$) is never smoothed, projected away or rounded: Layer 6 (`Layer6A`) records it as retained.
  * The firewall writes the class to the persistent Anomalon register (an append-only JSONL file; the first registration of a fingerprint wins) and routes to `CLOSED_RESIDUAL` with the exact defect mass, its primal repair and its dual witness.

---

### Failure Mode 6: Verification Limits & The Irreducible Trust Root

* **Governing Paper:** `030_authority_firewall_and_verification_limits` (OE-018, §1, §3)
* **Mathematical Statement:**
  $$\text{Elaboration-is-not-auditing obstruction: A verifier cannot verify its own adequacy.}$$
* **Structural Mechanism:**
  A finite formal system cannot internally discharge the adequacy of its own specification or the authenticity of its external authority root (the C4 Irreducible Trust Root). Recursive self-auditing results in infinite regression or circular self-certification.
* **How and Where CODA Fails:**
  * If CODA is asked to certify the semantic truth or real-world validity of a claim without an exhibited external license and specification identity, it fails closed.
  * It explicitly restricts its verdict to `ContractAuthority` and `VerifierScopedAuthority`, formally disclaiming `SemanticAuthority`. Any attempt to infer semantic truth from a green build is rejected as an uncontracted overclaim.

---

## 4. Claim Discipline & Scope Summary

### 1. What This Test Suite Supports

* It demonstrates in this software implementation that the two generated graph instances ($V = 1000, E = 1100$ and $V = 1500, E = 1600$) are evaluated across all 9 CODA layers within the asserted $< 3.0$s bound. ~~in under $0.05$s~~ **WITHDRAWN 2026-09-23** (measured before the repair).

* It demonstrates that exact rational circulation dual witnesses $y^* \in \ker(D_0^T)$ can be extracted with $\|y^*\|_\infty \le 1$ and exact pairing $\langle y^*, \Omega \rangle = \Phi_1 = 1000$. The outcome also carries a primal repair $f$ with $\|x - D_0 f\|_1 = \Phi_1$, so the primal and dual values are equal: zero duality gap, checked on the returned certificate.
* It verifies that the authority firewall blocks self-authorization and enforces terminal constructor disjointness across all 34 automated tests in `tests/test_*.py`. The adversarial suite in `tests/adversarial/` is catalogued separately in `docs/adversarial_review_2026-09-23.md`.

### 2. What This Test Suite Does Not Support

* It does not support claims of general polynomial-time solvability for non-convex or continuous NP-hard quotient problems.

* It does not support semantic truth or physical reality of graph models outside their declared discrete incidence complexes.
* It does not support that passing software unit tests constitutes a mathematical proof of system-wide security against arbitrary adversarial runtime tampering.

### 3. The Narrowest Defensible Claim

Under the declared discrete 1-complex carrier and exact rational arithmetic of `apps/coda`, the 9-layer pipeline correctly evaluates quotient distance, extracts annihilating dual witnesses, and routes problem instances into pairwise disjoint terminal branches ($\mathbb{T}_{\mathsf{auth}} \amalg \mathbb{T}_{\mathrm{res}} \amalg \mathbb{F}_{\mathrm{term}}$) without internal authority minting.

### 4. The Next Test Needed

An adversarial carrier mutation test evaluating whether perturbing boundary incidence signs in high-degree chordal cycles induces spurious circulation traps or degrades exact dual witness extraction.
