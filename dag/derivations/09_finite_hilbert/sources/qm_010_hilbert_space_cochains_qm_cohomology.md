# Hilbert-Space Cochains and QM Cohomology Admission

## GTOC Foundations — Quantum Contact Series (qm_010_hilbert_space_cochains_qm_cohomology)

**Date:** 2026-07-29 · **Version:** v1.0  
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  
**Status:** RELEASED  
**Authority:** `AuthorityEffect::None`  

## Mechanism inventory

| Slot | Value / Description |
| --- | --- |
| **Primitive Differences** | $\delta c = \text{{defect mass}}$ |
| **Carriers / Structure** | Finite Graph 0-Cochain / Hilbert Space |
| **Cochain complex** | $C^0 \to C^1 \to C^2$ |
| **Coboundary maps** | $\delta^0, \delta^1$ |
| **ZeroRel** | Preserved under $L_1$ quotient |
| **Licensed repairs** | None |
| **Quotient / Q1** | Banach Quotient |
| **Residuals** | $\delta c \neq 0$ boundary defect |
| **Witnesses** | Replayable Python / Rust Certifiers |
| **Observers / profiles** | Operational Observer |
| **Anomalons** | None |
| **CompletionLaw** | Finite Cochain Completion |
| **Terminal / route** | Route to 003 Quantum Foundations |
| **AuthorityEffect** | None |

**Document ID:** `QM_010`  
**Version:** v0.1 (Internal Pre-Print)  
**Date:** 2026-07-24  
**Folder:** `quantum_foundations/`  
**Claim ledger:** [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (IDs `010:QM-010-C1` through `010:QM-010-C8`)  
**Authority:** `AuthorityEffect::None`

### Status box (binding)

```text
Main deliverable: CODAQMBridge adapter + cohomology admission classifier

  + classical/quantum non-selection countermodel on a shared Hilbert-cochain skeleton.
Honesty: does not derive QM, Hilbert space, Born uniqueness, or authority.
Open: Lean for image-in-kernel / admission / d1=0 quotient (not-gating-honesty until labeled MECHANIZED).
Terminal: READY_AS_INTERNAL_DRAFT_v0.1
AuthorityEffect::None
Not Zenodo-final.
```

**Lead sentence.** A CODA quantum model is an **explicitly imported** finite quantum realization attached to a CODA observation/residual packet; cohomology diagnoses exactness, gluing, and persistent obstruction and does **not** select Hilbert space, derive the Born rule, establish physical quantum mechanics, or mint authority.

**Why a researcher should care.** Residual/cochain language is often silently rebranded as “quantum.” This paper makes the import boundary and admission table explicit, so FOC graph cohomology ($d_1=0$), Mermin–Peres quotient obstruction (QM_120), and any Hilbert-facing adapter cannot be confused with a derivation of QM.

```{=latex}
\begin{nonclaim}
This paper does not claim that CODA/GTLA derives quantum mechanics, Hilbert space,
Born uniqueness, contextuality in general, continuum physics, or authority. It does
not replace FOC004's finite Hilbert/Hodge overlay; it owns the distinct cohomology-admission
and quantum-non-selection result. It does not discharge WD-7's classical-countermodel
or contextuality/$H^1$ gates beyond the forward architecture stated here.
\end{nonclaim}
```


§1 — Governing thesis

> A CODA quantum model is an explicitly imported finite quantum realization attached to a CODA observation/residual packet. Cohomology diagnoses exactness, gluing, and persistent obstruction; it does not select Hilbert space, derive the Born rule, establish physical quantum mechanics, or mint authority.

**Programme links.** Consumes QM_005 / GTQ packet shape (imported quantum side), FOC003/FOC006 cochain language (cochain side), WD-7 founding concession (classical models exist for residual substrates), CODA term corpus v0.2 residual ladder + adapter $\iota$.

**Does not extend FOC004.** FOC004 retains finite Hilbert/Hodge synthesis ownership. QM_010 owns **admission classification** and **non-selection**.


§2 — Definition: `CODAQMBridge` — [DEFINITION] `QM-010-C1`

A **CODAQMBridge** is an adapter packet

\[
\mathcal B = (\mathcal C_{\mathrm{CODA}},\, \mathcal Q_{\mathrm{imp}},\, \mathcal K_{\mathrm{cochain}},\, \mathcal E_{\mathrm{evid}})
\]

with four sides:

### 2.1 CODA side $\mathcal C_{\mathrm{CODA}}$

* finite carrier / domain of marks  
* context/observer cover  
* registration + provenance  
* registered residual  
* admitted repair family  
* terminal policy (Accept / Refuse / OracleNeeded / …)

### 2.2 Imported quantum side $\mathcal Q_{\mathrm{imp}}$ (from QM_005/GTQ-shaped packet)

Exact coefficient domain; finite Hilbert carrier; states; effects; POVMs; Born pairing; channels; phase/involution; declared composition data. **All imported** — none derived by cohomology.

### 2.3 Cochain side $\mathcal K_{\mathrm{cochain}}$

Modules $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ with complex law $d_1\circ d_0 = 0$, and adapter

\[
\iota_{\mathrm{res}} : \mathrm{RegisteredResidual} \to C^1.
\]

Without $\iota_{\mathrm{res}}$, residual language must not use $H^1$ vocabulary.

### 2.4 Evidence side $\mathcal E_{\mathrm{evid}}$

Exact certificates and receipts. Diagnostic classes are **not** terminal-policy decisions and **not** authority.

**Claim `QM-010-C1`:** the above four-tuple is the definition of `CODAQMBridge`. Type: DEFINITION.


§3 — Complex law: $\operatorname{im}(d_0)\subseteq\ker(d_1)$ — [PROVEN, CONDITIONAL] `QM-010-C2`

**Hypotheses.** Modules $C^0,C^1,C^2$ over a declared coefficient ring/field; linear maps $d_0,d_1$ with $d_1\circ d_0=0$ as part of the cochain complex declaration.

**Conclusion.** $\operatorname{im}(d_0)\subseteq\ker(d_1)$.

**Proof.** Let $x=d_0 a$. Then $d_1 x = d_1(d_0 a)=(d_1\circ d_0)a=0$, so $x\in\ker(d_1)$. $\square$

**Type note.** This is the standard complex law, restated for the bridge; Lean target `QM032.im_d0_subset_ker_d1` (OPEN until MECHANIZED).


§4 — Admission classification — [DEFINITION / OPERATIONAL RULE] `QM-010-C3`

Given $s\in C^1$ (typically $s=\iota_{\mathrm{res}}(r)$) and certificates for membership in $\operatorname{im}(d_0)$ and evaluation of $d_1(s)$:

| Condition | Diagnostic class | Notes |
|---|---|---|
| $s\in\operatorname{im}(d_0)$ | **Exact** | gauge-exact residual |
| $s\notin\operatorname{im}(d_0)$ and $d_1(s)=0$ | **ClosedNonexact** | closed residual / survivor candidate under freeze+repairs |
| $d_1(s)\neq 0$ | **ActiveClosureFailure** | closure defect active |
| missing $\iota$, ill-typed $s$, or undecided certificates | **IllFormed / Refuse** | refuse $H^1$ language |

Four worked diagnostic cases (finite):

1. **Exact:** $s=d_0 a$ for exhibited $a$.  
2. **Closed nonexact:** $d_1=0$ complex, $s\notin\operatorname{im}(d_0)$.  
3. **Active closure:** $C^2\neq 0$, $d_1(s)\neq 0$.  
4. **Ill-formed:** residual without $\iota_{\mathrm{res}}$ — classifier refuses cohomological promotion.

**Claim `QM-010-C3`:** DEFINITION / OPERATIONAL RULE for admission. Not a physical law.


§5 — Degenerate case $d_1=0$ — [PROVEN, CONDITIONAL] `QM-010-C4`

**Hypotheses.** Complex with $C^2=0$ (hence $d_1=0$), as in FOC003 finite graphs without 2-cells.

**Conclusion.** $H^1=\ker(d_1)/\operatorname{im}(d_0)=C^1/\operatorname{im}(d_0)=Q^1$.

**Proof.** $\ker(d_1)=C^1$ when $d_1=0$; quotient by $\operatorname{im}(d_0)$ yields $Q^1$. $\square$

**Honesty fence.** This is a **degenerate special case**, not the general cohomology story when 2-cells / nontrivial $d_1$ are present (FOC003 already states this; QM_010 re-exports the fence for the quantum-facing corpus).


§6 — Non-selection: shared skeleton, classical and quantum realizations — [PROVEN, CONDITIONAL] `QM-010-C5`

**Hypotheses.** A finite cochain skeleton $(C^\bullet,d)$ is fixed. Two realization maps:

* $\rho_{\mathrm{cl}}$: classical simplex / stochastic shadow filling states and readout without noncommuting contexts;  
* $\rho_{\mathrm{q}}$: imported finite Hilbert packet (QM_005-shaped) with states/effects/Born.

Both produce residual-to-$C^1$ data through the same $\iota$ shape on a declared cover.

**Conclusion.** The pair $(\rho_{\mathrm{cl}},\rho_{\mathrm{q}})$ shows that **the cochain skeleton and $H^1$ admission class alone do not select quantum mechanics**: classical realizations can occupy the same diagnostic classes.

**Proof sketch.** WD-7 founding concession + Paper 001G-style classical residual models already exhibit residual/cochain logic classically; import a matching $\iota$ into $(C^\bullet,d)$. Separately import a QM_005 packet on the same $(C^\bullet,d)$ indexing. Diagnostic class depends only on $(s,d_0,d_1)$, not on Born/phase. $\square$

**Best-guess discriminator bundle (imported, not derived):** complex phase / involution; nonclassical composition; state/effect/Born readout; channel transport; declared contextuality or quantum-bound predicate. **None follows from cohomology alone.**


§7 — QM_120 quotient vs $H^1$ class — [PROVEN, CONDITIONAL] `QM-010-C6`

**Claim.** QM_120’s witness that a parity target $s\notin\operatorname{im}(d_0)$ is a **quotient obstruction**. Promotion of $s$ to an $H^1$ class additionally requires a declared $d_1$ and a proof that $d_1(s)=0$.

**Proof.** By definition $Q^1 = C^1/\operatorname{im}(d_0)$ and $H^1 = \ker(d_1)/\operatorname{im}(d_0)$. Membership in $H^1$ requires $s \in \ker(d_1)$. Quotient non-membership $s \notin \operatorname{im}(d_0)$ alone yields a class in $Q^1 = C^1/\operatorname{im}(d_0)$. If $d_1 s = 0$, then $[s]$ lies in the natural subspace $H^1 \subseteq Q^1$. Equality $H^1 = Q^1$ requires $\ker(d_1) = C^1$, equivalently $d_1 = 0$. $\square$


§8 — Architecture status — [INTERPRETIVE] `QM-010-C7`

The proposed CODA–QM architecture is an **imported, interpretive realization interface**, not an origin theorem and not a completeness theorem for quantum theory.


§9 — Nonclaims and authority — [SCOPE FENCE] `QM-010-C8`

| Forbidden as load-bearing |
|---|
| CODA/GTLA derives QM, Hilbert space, or Born uniqueness |
| Cohomology selects complex quantum theory |
| Continuum physics from finite cochains |
| Authority minting from diagnostics or $H^1$ |
| Replacing FOC004 Hilbert/Hodge ownership |
| Closing WD-7 classical-countermodel / contextuality gates without their obligations |

**AuthorityEffect::None** for all diagnostics, examples, and admission outputs in this paper.


§10 — Finite examples (four cases)

| Case | Skeleton | $s$ | Class |
|---|---|---|---|
| Exact | path graph, $d_1=0$ | $s=d_0 a$ | Exact |
| Closed nonexact | cycle $C_4$, $d_1=0$ | generator of $H^1$ | ClosedNonexact |
| Active closure | declared 2-cell, nontrivial $d_1$ | $d_1(s)\neq 0$ | ActiveClosureFailure |
| Ill-formed | residual without $\iota$ | — | Refuse cohomological promotion |


§11 — Relation to FOC and WD

| Package | Relation |
|---|---|
| FOC003 | $d_1=0$ degenerate $H^1\cong Q^1$ — re-exported as `QM-010-C4` |
| FOC004 | Hilbert/Hodge overlay ownership retained; QM_010 does not steal it |
| FOC006 | degree-wise complex DSL linked as cochain declaration surface; not duplicated |
| WD-7 | classical-model no-go founding concession; QM_010 is the numbered QM home for admission/non-selection |
| QM_120 | quotient obstruction; $H^1$ promotion needs $d_1(s)=0$ (`QM-010-C6`) |
| QM_005 | imported quantum packet side of the bridge |


§12 — Formalization targets (not MECHANIZED)

| ID | Target | Gate |
|---|---|---|
| PL-QM032-1 | `im_d0_subset_ker_d1` | not-gating-honesty until labeled MECHANIZED |
| PL-QM032-2 | admission classifier on finite certificates | not-gating-honesty |
| PL-QM032-3 | `d1=0` quotient equivalence | not-gating-honesty |

Do **not** mark MECHANIZED without focused `lake build` + axiom receipts. Existing Mermin–Peres (QM_120) builds must remain green; QM_010 must not overstate them.


§13 — Claim registry (inline)

| ID | Statement | Type |
|---|---|---|
| QM-010-C1 | CODAQMBridge definition | DEFINITION |
| QM-010-C2 | $\operatorname{im}(d_0)\subseteq\ker(d_1)$ | PROVEN, CONDITIONAL |
| QM-010-C3 | Admission classification | DEFINITION / OPERATIONAL RULE |
| QM-010-C4 | $d_1=0\Rightarrow H^1\cong Q^1$ | PROVEN, CONDITIONAL |
| QM-010-C5 | Cochains/$H^1$ do not select QM | PROVEN, CONDITIONAL |
| QM-010-C6 | QM_120 quotient vs $H^1$ promotion | PROVEN, CONDITIONAL |
| QM-010-C7 | Architecture is imported interface | INTERPRETIVE |
| QM-010-C8 | Nonclaims + Auth None | SCOPE FENCE |


§14 — Changelog

* **2026-07-24 — v0.1.** Initial internal pre-print: CODAQMBridge, admission table, non-selection, QM_120 promotion fence, FOC/WD links. AuthorityEffect::None.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-010-C1` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-010-C2` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-010-C3` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-010-C4` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-010-C5` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-010-C6` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-010-C7` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-010-C8` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `PL-QM032-1` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `PL-QM032-2` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `PL-QM032-3` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `Consumes` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM_005` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM_120` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `FOC003` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `FOC006` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `WD-7` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |

<!-- claim-id-body-index:end -->
