---
doc: 000_oe_prime_algorithms.md
status: published_living_document
document_class: CHAPTER_STEM_PAPER
paper_id: "000_oe_prime_algorithms"
series: "008_engine_runtime / 000_oe_prime_algorithms"
series_position: "OE-000"
date: "2026-09-26"
version: "1.0.0"
---

# Algorithm Prime Triad: Candidate Intake, Adapter Descent, and Continuation Control

**Series:** `008_engine_runtime` / `000_oe_prime_algorithms`  
**Series position:** OE-000 (Part I — Algorithm Prime Triad Master Monograph)  
**Author:** Jeremy H. Carroll  
**Date:** 2026-09-26  
**Version:** 1.0.0 (Unified Monograph combining Prime -1, 000, 001, 002, and CODA $C^n$ Ascent)  
**Document class:** Chapter / stem paper  

---

## Why a Researcher Should Care

Every recursive evaluator faces a fatal failure mode: it can always add a dimension, rename an unresolved residual, or re-enter an evaluation locus, thereby appearing to make progress forever without discharging anything.

The **Algorithm Prime Triad (000, 001, 002)** establishes the foundational operational control law of the Omega Engine:

1. **Prime -1 & 000:** Enforces strict locus grounding and a 7-step local packet declaration order ($\text{Grounding} \to \text{Carrier} \to \text{Observer} \to \text{Primitive Difference} \to \text{ZeroRel} \to \text{Witness} \to \text{Quotient}$).
2. **Prime 001:** Governs intake and inter-carrier transport soundness, enforcing that translation into an `OmegaPacket` does not confer validity and tracking all lost data in explicit loss ledgers ($L_{\text{adapter}}$).
3. **Prime 002:** Enforces the master continuation control law ($\mathsf{CanContinue}_n$) and six anti-cheat halting laws, guaranteeing finite, budgeted stopping.
4. **CODA $C^n$ Ascent:** Formalizes recursive re-entry $\Omega_{000}(L)$ at any locus without minting false terminal authority.

Without a strict declaration, transport, and halting calculus, agentic execution swarms degenerate into endless prompt retries, un-grounded carrier hallucinations, and authority laundering.

---

## Refusal Box & Scope Fence

```text
No automatic conversion of raw prompts into valid cochains.
No degree, lift, or authority laundering.
No un-bounded recursive evaluation.
No un-grounded carrier hallucinations.

Candidate proposals under Prime -1 carry status: proposed_only
and confer no validity until Prime 000 admission.
Step 10 terminalization emits LOCAL_GREEN_FOR_SCOPE,
never an un-scoped global green certificate.
```

---

## Mathematical Foundations & Notation

The operational calculus operates over discrete finite simplicial complexes $K = (V, E, F)$ equipped with exact rational arithmetic over $\mathbb{Q}$:

1. **Chains and Cochains:** $C_0, C_1, C_2$ denote the rational vector spaces spanned by vertices, oriented edges, and oriented faces. Cochain spaces $C^k = \operatorname{Hom}(C_k, \mathbb{Q})$ represent evaluation functions.
2. **Coboundary Operators:** The discrete derivative $d_0: C^0 \to C^1$ assigns to potential $\phi$ the edge difference $(d_0 \phi)(u, v) = \phi(v) - \phi(u)$. The curl operator $d_1: C^1 \to C^2$ evaluates circulation around faces $(d_1 h)(u, v, w) = h(u, v) + h(v, w) - h(u, w)$, satisfying $d_1 \circ d_0 = 0$.
3. **Exact Quotient Potential ($\Phi_1$):** Given a 1-cochain $h \in C^1$, the quotient potential is the exact minimum L1 distance to the subspace of coboundaries (gauge transforms):
   $$\Phi_1(h) := \min_{\phi \in C^0} \|h - d_0 \phi\|_1$$
   This is evaluated exactly over $\mathbb{Q}$ via rational linear programming, yielding a dual witness vector $z \in [-1, 1]^{|E|}$ with $d_0^* z = 0$ certifying the zero duality gap: $\Phi_1(h) = \langle z, h \rangle$.
4. **Closure Charge ($\Gamma_2$):** The 2-obstruction measuring non-closure is:
   $$\Gamma_2(h) := \|d_1 h\|_1$$
5. **Discrete Hodge Decomposition:** For an inner product with positive edge weights $W$, any 1-cochain decomposes orthogonally over $\mathbb{Q}$ into exact, harmonic, and coexact components:
   $$h = d_0 \phi + h_{\text{harm}} + d_1^* \psi$$
   where $h_{\text{harm}} \in \ker(d_1) \cap \ker(d_0^* W)$.

---

## 1. Prime -1 & Prime 000: Candidate Proposal Engine & Local Declaration Order

$$\begin{aligned}
\text{Prime -1: Candidate Proposal} &\longrightarrow \text{Prime 001 Intake Check} \\
&\longrightarrow \text{Prime 000 Validation} \longrightarrow \text{DDA Execution}
\end{aligned}$$

Requiring an end-user to manually invent carriers, primitive differences, or observers forces them to perform internal mathematical tasks. **Prime -1 (Carrier Proposal Engine / Packet Compiler)** acts as the front-end intake compiler:

$$\boxed{\begin{gathered}
\text{The Omega Engine does not begin by knowing the carrier.} \\
\text{It begins by proposing candidate carriers under scoped admission.}
\end{gathered}}$$

### 1.1 CandidatePacket & IntakeTrace Schema (`OE001-01`)

Prime -1 ingests a raw artifact and emits candidate `CandidatePacket` structures. Pre-admission refusals live strictly in an `IntakeTrace` (`enters_dda_trace: false`) to prevent contaminating the operational `DdaTrace`: `[DEFINITION]` (`OE001-01`)

```yaml
IntakeTrace:
  raw_artifact_hash: "doc_001_sha256"
  candidate_locus: "lines 1-12"
  candidate_packet:
    artifact_id: "doc_001_ref"
    locus_id: "locus_frontmatter_01"
    problem_family: "claim | proof | narrative | code"
    primitive_difference_proposal: "metadata mismatch"
    carrier_proposal: "document metadata block"
    zero_rel_proposal: "canonical metadata equality"
    observer_proposal: "frontmatter schema checker"
    witness_available: true
    quotient_or_refusal: "E or M"
    adapter_confidence: "high"
    status: "proposed_only"
  intake_adapter_status: "ADMITTED | REFUSED_UNTYPED"
  enters_dda_trace: false
```

Prime 000 receives each candidate and emits one of seven formal responses:
`ACCEPT_DECLARATION` · `REFUSE_MISSING_CARRIER` · `REFUSE_MISSING_OBSERVER` · `REFUSE_MISSING_WITNESS` · `REFUSE_MISSING_QUOTIENT` · `SPLIT_PACKET` · `REQUEST_LIFT`.

### 1.2 Prime 000 Local Packet Declaration Order (`OE001-02`)

Every admitted packet MUST be declared according to the 7-step local runtime declaration order: `[DEFINITION]` (`OE001-02`)

```text
0. Grounding (cryptographic raw text / AST / commit hash anchor)
1. Carrier (simplicial complex / AST graph / discrete carrier)
2. Observer packet / detector (resolution, probe, gauge)
3. Primitive difference (cochain h in C1 or defect functional)
4. ZeroRel rule (gauge equivalence / coboundary relation)
5. Witness or refusal route (replay certificate chi or typed refusal)
6. Optional quotient, degree, lift, or terminal policy
```

### 1.3 Layered Multi-Carrier Lenses & LensSpan Model (`OE001-03`)

A complex artifact (paper, codebase, financial plan) is **not** a single monolithic cochain complex. It is a **bundle of carriers** extracted via layered partial spans: `[SCOPE FENCE]` (`OE001-03`)

$$A \xleftarrow{s_L} S_L \xrightarrow{p_L} K_L$$

where $S_L$ is the selected source span, $K_L$ is the extracted carrier, and span composition proceeds by pullback in the category $\mathbf{LensSpan}(A)$ under canonical inclusion subcomplexes:

$$\begin{aligned}
L_0 \ (\text{lexical}) &\longrightarrow L_1 \ (\text{syntactic}) \longrightarrow L_2 \ (\text{semantic}) \\
&\longrightarrow L_3 \ (\text{proof}) \longrightarrow L_4 \ (\text{rhetoric}) \longrightarrow L_5 \ (\text{strategic})
\end{aligned}$$

### 1.4 Scoped Terminalization (`OE001-04`)

Terminalization ($T$) emits scoped local status rather than un-scoped global green: `[OPERATIONAL RULE]` (`OE001-04`)

$$\begin{aligned}
\text{Step 10: } T &\longrightarrow \text{Terminalize local repair pass:} \\
&\quad \mathsf{LOCAL\_GREEN\_FOR\_SCOPE}(\text{scope}, \text{remaining\_obligations})
\end{aligned}$$

Terminalization evaluates the active cochain state and routes through two distinct terminal paths:

1. **Zero-Residual Terminalization ($T_{\text{res}}$):** If the quotient residual vanishes ($\Phi_1 = 0$) and the closure charge is exact ($\Gamma_2 = 0$) under an adequate detector, the pass seals with $\mathsf{LOCAL\_GREEN\_FOR\_SCOPE}$. The emitted receipt registers the exact potential and witnesses, certifying completion strictly within the declared carrier scope.
2. **Terminal Failure / Refusal ($F_{\text{term}}$):** If an open residual ($\Phi_1 > 0$) or closure failure ($\Gamma_2 > 0$) persists, terminalization is refused. The evaluator halts with typed terminal failure $F_{\text{term}}$ (`REFUSED_OPEN_RESIDUAL` or `REFUSED_BLIND_OBSERVER`), preventing un-repaired defects from being sealed as green.

Under no circumstances does terminalization convert a local repair into an un-scoped global green certificate.

---

## 2. Prime 001: Adapter Descent Soundness & Transport Verification

### 2.1 Dual Prime 001 Placement Protocol (`OE002-01`)

To prevent un-grounded or invalid translations from contaminating the execution log, Prime 001 is deployed at **two distinct boundary points**: `[OPERATIONAL RULE]` (`OE002-01`)

$$\begin{aligned}
\text{Prime (-1)} &\longrightarrow \text{Prime 001 [Intake Adapter]} \longrightarrow \text{Prime 000 [Admit]} \\
&\longrightarrow \text{DDA Runner} \longrightarrow \text{Prime 001 [Transport Adapter]} \longrightarrow \text{Prime 002 [Control]}
\end{aligned}$$

1. **Intake Adapter Check:** Evaluates raw artifact $\to$ candidate packet translation before Prime 000 admission.
2. **Transport Adapter Check:** Evaluates inter-carrier transport steps whenever a DDA operation changes carrier.

### 2.2 Adapter Descent Soundness Rule (`OE002-02`)

Translation of a native claim into an `OmegaPacket` is a representation mapping, not a proof of validity. An intake or transport adapter $\alpha: C_{\text{source}} \to C_{\text{target}}$ is sound if and only if it preserves operations, equations, witnesses, and authority fences while recording all lost data in an explicit loss ledger $L_{\text{adapter}}$: `[DEFINITION]` (`OE002-02`)

```yaml
AdapterContract:
  source_carrier: C_source
  target_carrier: C_target
  preserved_operations: [d0, d1]
  preserved_equations: [d1_d0_zero]
  preserved_witnesses: [dual_certificate]
  loss_ledger: L_adapter
```

If $L_{\text{adapter}} \neq \varnothing$, the adapter emits `ADAPTER_DEBT` and halts automatic promotion.

### 2.3 Refusal & Debt Taxonomy (`OE002-03`)

1. `REFUSED_UNTYPED`: Raw input cannot be mapped to any known carrier signature or observer probe.
2. `ADAPTER_INADEQUATE`: Candidate carrier mapping exists but fails boundary operator or witness preservation.
3. `REFUSED_ADAPTER_DEBT`: Transport across carrier boundaries failed adapter soundness checks (`C · M · T`).

---

## 3. Prime 002: Master Continuation Predicate & Anti-Cheat Control

### 3.1 Master Control Loop & Predicate $\mathsf{CanContinue}_n$ (`OE003-01`)

At stage $n$, continuation to stage $n+1$ is lawful if and only if predicate $\mathsf{CanContinue}_n$ evaluates to `True`: `[DEFINITION]` (`OE003-01`)

$$\begin{aligned}
\mathsf{CanContinue}_n :\iff &\mathsf{OutstandingObligation}(r_n) \wedge \mathsf{HigherObligationWitness}(r_n) \wedge \\
&\mathsf{NextCarrierDeclared}(r_n) \wedge \mathsf{AdapterSound}_{n\to n+1} \wedge \\
&\mathsf{DetectorAdequate}_{n+1} \wedge \mathsf{MinimalLicensedLift}_{n\to n+1} \wedge \\
&\mathsf{SkeletonPreserved}_{n\to n+1} \wedge \mathsf{BudgetAvailable}_n \wedge \\
&\neg\mathsf{GTLAContinuationRefusal}_n
\end{aligned}$$

The three-condition form groups these conjuncts into structural validity, resource availability, and absence of terminal refusal. The Lean theorem `Prime.cc9_implies_cc3` formalizes this equivalent regrouping.

### 3.2 Six Anti-Cheat Halting Laws (`OE003-02`)

> **Halting Law Constraints:**
>
> 1. **No Degree Laundering:** Adding $C^{n+1}$ requires an exhibited $(n+1)$-dimensional obligation.
> 2. **No Lift Laundering:** A representation extension must prove no same-carrier repair exists.
> 3. **No Anomalon Evasion:** A stable residual cannot be perpetually renamed to avoid terminalization.
> 4. **Old-Skeleton Preservation:** A continuation must preserve certified data or emit a loss ledger.
> 5. **Detector Revalidation:** Repacketization must revalidate detector adequacy at degree $n+1$.
> 6. **First-Unresolved-Degree Honesty:** If $n_0$ is unresolved, claims above $n_0$ are conditional: $\mathsf{CoherentUpTo}(n_0-1)$ and $\mathsf{ResidualAt}(n_0)$.

### 3.3 Bounded Operational Termination (`OE003-03`)

Given a finite non-replenished budget $B_{\text{tot}} \in \mathbb{N}$ (or scaled rational budget) where every counted operation debits the shared budget by at least a strictly positive cost floor $\delta_{\text{control}} > 0$ and no operation can begin without sufficient remaining budget ($B \ge \delta_{\text{control}}$), the number of executed operations is bounded by: `[CONDITIONAL THEOREM]` (`OE003-03`)

$$\#\mathrm{ops} \le \left\lfloor \frac{B_{\text{tot}}}{\delta_{\text{control}}} \right\rfloor$$

This bound (`Prime.ops_le_floor_div`) formalizes the natural-number arithmetic consequence of the non-replenished debit invariant ($n \cdot \delta \le B$). Total runtime termination additionally assumes that each individual operational checker halts in finite time. If budgets are tracked in exact rationals $\mathbb{Q}$, the bound applies via scaling by the least common denominator.

### 3.4 Local Queue Scheduler (`OE003-04`) & CODA Taxonomy (`OE003-05`)

For local execution on a fixed carrier, Prime 002 acts as a finite residual queue scheduler. To prevent anomalon evasion (Law 3), progress requires strict lexicographical descent on the diagnostic tuple: `[OPERATIONAL RULE]` (`OE003-04`)

$$\text{Descent} :\iff (\Gamma_{2, n+1}, \Phi_{1, n+1}, \text{defect\_count}_{n+1}) <_{\text{lex}} (\Gamma_{2, n}, \Phi_{1, n}, \text{defect\_count}_n)$$

Witnessed exploration or residual fingerprint changes represent exploratory transitions, not mathematical progress. Across steps on a fixed carrier, continuation requires quantitative potential descent $\Delta \Phi_1 \le 0$ evaluated using the exact quotient norm $\|[h]\|_{Q1}$. Under a licensed lift across carriers ($C^n \to C^{n+1}$), $\Phi_1$ may temporarily increase if the representation extension exposes higher-dimensional boundary obligations, provided the lift license explicitly certifies that no same-carrier descent is possible: `[FINITE THEOREM]` (`OE003-06`).

#### CODA Pipeline-Order Taxonomy (`OE003-05`)

CODA formalizes local obstruction analysis as a strict 7-stage pipeline sequence, with $Q$ as The Continuum: `[DEFINITION]` (`OE003-05`)

$$\begin{aligned}
G \ (\text{Grounding}) &\longrightarrow C \ (\text{Carrier}) \longrightarrow J \ (\text{Observer}) \\
&\longrightarrow \Delta \ (\text{Primitive Difference}) \longrightarrow Z \ (\text{ZeroRel}) \\
&\longrightarrow \chi \ (\text{Witness}) \longrightarrow Q \ (\text{Quotient})
\end{aligned}$$

1. **Grounding ($G$):** Raw artifact cryptographic digest and origin anchor.
2. **Carrier ($C$):** Explicit simplicial complex or discrete chain module representing the substrate.
3. **Observer ($J$):** Finite projection and resolution window specifying measurement capacity.
4. **Primitive Difference ($\Delta$):** Concrete difference cochain $h \in C^1$ between competing models or steps.
5. **ZeroRel ($Z$):** Equivalence relation specifying exact triviality or gauge equivalence ($\operatorname{im} d_0$).
6. **Witness ($\chi$):** Explicit dual witness certificate bounding the duality gap or confirming exact repair.
7. **Quotient ($Q$):** The Continuum, the quotient space $C^1 / \operatorname{im}(d_0)$ hosting the residual obstruction.

Output status taxonomy:

- `LOCAL_GREEN_FOR_SCOPE`: Exact zero residual ($\Phi_1 = 0, \Gamma_2 = 0$) under an adequate observer.
- `REFUSED_UNTYPED`: Candidate locus lacking a declared carrier or grounding anchor.
- `ADAPTER_INADEQUATE`: Loss ledger identifies loss of essential invariants or unpreservable equations.
- `HALTED_BUDGET_EXHAUSTED`: Operational budget depleted ($B < \delta_{\text{control}}$).
- `HALTED_STAGNANT_PROGRESS`: Lookback window detects lack of strictly decreasing residual mass.
- `GTLA_STOP`: Terminal local stop halted with an unresolved obstruction that cannot be discharged under available resources.
- `GTTA_GLOBAL_RESIDUAL`: Ambient structural obstruction surviving into all admissible representations.

---

## 4. CODA Recursive Re-Entry and $C^n$ Ascent Protocol

### 4.1 CODA Recursive Re-Entry Protocol (`OE004-01`)

Algorithm Prime 000 may be recursively re-entered at any CODA locus $L \in \text{CODA}$ (object, morphism, witness, residual, quotient, adapter, or terminal claim).

A **locus** $L$ is the entity under examination, whereas a **carrier** $C_L$ is the declared local mathematical structure in which comparisons and primitive differences on $L$ are represented. In general, $L \neq C_L$ (identifying them without an explicit typing witness silently promotes an arbitrary locus into a carrier, bypassing the Prime -1 proposal engine and Prime 000 declaration order).

The recursive re-entry pipeline requires proposing and declaring a candidate carrier $C_L$ for locus $L$ before running Prime 000 on $(L, C_L)$: `[PROTOCOL SPECIFICATION]` (`OE004-01`)

$$\boxed{\text{locus } L \longrightarrow \text{propose/declare carrier } C_L \longrightarrow \text{run Prime 000 on } (L, C_L)}$$

$$\begin{aligned}
\Omega_{000}(L) \Longrightarrow \bigl(&\text{Carrier}=C_L,\ \mathrm{ZeroRel}_L,\ \text{Observer}=J_L, \\
&\text{Witness}=\chi_L,\ \text{Residual}=R_L,\ \text{Quotient}=Q_L \bigr)
\end{aligned}$$

subject to standard Prime 000 admission requirements.

### 4.2 Lawful $C^n$ Ascent Protocol (`OE004-02`)

Degree ascent $C^k \longrightarrow C^{k+1}$ is permitted if and only if the paper declares: `[DEFINITION]` (`OE004-02`)

1. Carrier complex $C^k$, Differential $d^k: C^k \to C^{k+1}$, Next Differential $d^{k+1}: C^{k+1} \to C^{k+2}$, and exact nilpotency $d^{k+1} \circ d^k = 0$.
2. **Monotone Phase Embedding Definition:** Given an assumed monotone map embedding admission into execution, if admission precedes measurement ($\operatorname{admit}(P) \le \operatorname{measure}(P)$), then the order-preserving structure guarantees that admission precedence reflects in execution for any packet pair where the map is monotone (`Prime.embedding_order_preserving`). This formalization proves the property of the assumed monotone structure; constructing a concrete causal trace embedding and differential nilpotency ($d \circ d = 0$) are separate, independent verification obligations.

### 4.3 Stop Conditions: GTLA Stop vs. CODA-A Global Residual (`OE004-03`)

- **`GTLA_STOP`:** Local authority construction halted due to missing carrier, detector, witness, quotient, or exhausted resources.
- **`GTTA_GLOBAL_RESIDUAL`:** Ambient structural obstruction $R_U$ surviving transport into all admissible adapters.

### 4.4 Observer Envelopes & Evaluator Defect Linearity (`OE004-04`, `OE004-05`, `OE004-06`)

#### Observer Envelope Comparability (`OE004-04`)
Observer envelopes $J_1, J_2$ are comparable only under shared grounding and explicit coordinate transformation bounds: `[SCOPE FENCE]` (`OE004-04`). Comparing evaluation scores across ungrounded or incomparable observers is strictly refused.

#### Evaluator Defect Linearity (`OE004-05`)
Let $\Omega$ be a finite probability space with joint probability distribution $\mathbb{P}$. Let $E_g: A \otimes B \to [0, 1]$ be a global composite evaluator and $E_1: A \to [0, 1], E_2: B \to [0, 1]$ be local component evaluators. Define the global pass rate and joint local pass rate: `[FINITE THEOREM]` (`OE004-05`)

$$\mathrm{GPR} := \mathbb{E}[E_g(A \otimes B)], \qquad \mathrm{LPR} := \mathbb{E}[E_1(A) E_2(B)]$$

The pointwise evaluator defect is defined as:
$$\Delta_E(A, B) := E_g(A \otimes B) - E_1(A) E_2(B)$$
By linearity of expectation over the joint probability law:
$$\mathrm{GPR} - \mathrm{LPR} = \mathbb{E}[E_g(A \otimes B) - E_1(A) E_2(B)] = \mathbb{E}[\Delta_E]$$
When evaluators decouple without cross-module obstruction ($\Delta_E = 0$ pointwise), local pass rates predict global pass rates identically ($\mathrm{GPR} = \mathrm{LPR}$). Note that zero expected defect ($\mathbb{E}[\Delta_E] = 0$) can also arise via cancellation unless $\Delta_E \ge 0$; only a non-zero expected defect forces a non-zero defect on some supported instances.

#### Six-Role EPK Overlay Diagnostic Scope Fence (`OE004-06`)
The six-role EPK overlay enforces strict role boundaries: `[SCOPE FENCE]` (`OE004-06`). Evaluators, improvers, adversaries, certifiers, archivers, and governors evaluate strictly within their declared diagnostic scopes.

Engine self-examination ($\Omega_{000}(L_{\text{self}})$) and its anti-cheat queue upgrade rules are specified in `docs/residual_aware_can_continue.md`: `[MODEL CONSEQUENCE]` (`OE004-07`, `OE004-08`).

---

## 5. Summary & Claim-ID Index

| Claim ID | Type | Section | Summary |
|---|---|---|---|
| `OE001-01` | `Definition` | §1.1 | CandidatePacket & IntakeTrace schema definition |
| `OE001-02` | `Definition` | §1.2 | Prime 000 7-step local packet declaration order |
| `OE001-03` | `Scope` | §1.3 | Multi-carrier lens span pullback model |
| `OE001-04` | `Model consequence` | §1.4 | Scoped terminalization `LOCAL_GREEN_FOR_SCOPE` |
| `OE002-01` | `Scope` | §2.1 | Dual Prime 001 boundary placement (Intake & Transport) |
| `OE002-02` | `Definition` | §2.2 | Adapter contract definition & loss ledger structure |
| `OE002-03` | `Definition` | §2.3 | Refusal & debt taxonomy (`REFUSED_UNTYPED`, `ADAPTER_INADEQUATE`) |
| `OE003-01` | `Definition` | §3.1 | Continuation predicate definition & equivalent 3-form regrouping |
| `OE003-02` | `Protocol specification` | §3.2 | Six anti-cheat halting laws |
| `OE003-03` | `Conditional theorem` | §3.3 | Bounded operational termination law |
| `OE003-04` | `Operational rule` | §3.4 | Local queue scheduler & strict quotient descent condition |
| `OE003-05` | `Definition` | §3.4 | CODA taxonomy in pipeline order with $Q$ as The Continuum |
| `OE003-06` | `Finite theorem` | `docs/residual_aware_can_continue.md` | Residual-aware $\mathsf{CanContinue}_n$ with quantitative $\Delta \Phi \le 0$ bound |
| `OE004-01` | `Scope` | §4.1 | CODA recursive re-entry protocol $\Omega_{000}(L)$ over declared carrier $C_L$ ($L \neq C_L$) |
| `OE004-02` | `Definition` | §4.2 | Lawful ascent protocol & assumed monotone phase embedding |
| `OE004-03` | `Definition` | §4.3 | `GTLA_STOP` vs. `GTTA_GLOBAL_RESIDUAL` stop conditions |
| `OE004-04` | `Scope` | §4.4 | Observer envelope comparability |
| `OE004-05` | `Finite theorem` | §4.4 | Evaluator defect linearity $\mathrm{GPR} - \mathrm{LPR} = \mathbb{E}[\Delta_E]$ |
| `OE004-06` | `Scope` | §4.4 | Six-role EPK overlay diagnostic scope fence |
| `OE004-07` | `Model consequence` | `docs/residual_aware_can_continue.md` | Self-examination re-entry path $\Omega_{000}(L_{\text{self}})$ for engine state |
| `OE004-08` | `Model consequence` | `docs/residual_aware_can_continue.md` | Anti-cheat laws for self-proposal & progress queue upgrade |

---

## 6. References

1. J. H. Carroll. *Discrete Deformation Calculus: A Finite Trace Calculus for Obstructions, Exact Repair, and Bounded Replay*, v1.0.0 (2026).
2. J. H. Carroll. *Local Green, Global Red I: Evaluated Path Kernels for Composed Agent Reliability*, v1.2.3 (2026). Zenodo, DOI: 10.5281/zenodo.22881911.
3. J. H. Carroll. *CODA-FOC: Finite Obstruction Calculus — Exact Quotient Diagnostics, Dual Witnesses and Two-Stage Coherence*. Omega Engine Research Programme (2026).
4. J. H. Carroll. *CODA-GTLA: General Theory of Layered Authority — A Leftover Class is Not Standing*. Omega Engine Research Programme (2026).
5. The Lean 4 Theorem Prover, v4.34.0. `https://lean-lang.org`.
