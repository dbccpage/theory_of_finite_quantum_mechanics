> **Annex notice (2026-07-31, AuthorityEffect: None).**  
> Packaging annex absorbed: `qm_083_completely_positive_import_boundary/` (CP/Kraus import fence and LGGR — annex to stochastic kernel / CPTP population-shadow paper).  
> Claim namespaces remain distinct; this is not a theorem upgrade.


# Channels as Stochastic Kernels and the CPTP Lift

## GTOC Foundations — Quantum Contact Series (qm_082_channels_as_stochastic_kernels_and_the_cptp_lift)

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

document_id: "OMEGA-QM-CHAN-STOCH-041"
version: "v0.1.0 Pre-Print"
last_updated: "2026-06-19"
status: "DRAFT — component note (rung 4: channels / stochastic kernels / CPTP population shadows) of QM_121 (The Finite QM Ingredient Ladder)"
series: "qm / QM ingredient ladder"
companions:
- "QM_007 Density Matrices as Diagonal Residual Weights (rung 3); pub-005 CPTP trace-norm geometry; pub-010 (voice)"

---

### Population shadows of channels, not a derivation of quantum dynamics

> **Component note (rung 3) of *QM_121 — The Finite QM Ingredient Ladder*.** The publishable synthesis
> is QM_121; this note is the detailed source for the channels/CPTP-shadow rung, and keeps its own
> claim ledger.

Abstract

**Main result (informal).** A channel on finite outcome distributions is a stochastic kernel —
nonnegative entries, unit column sums. It preserves total mass (trace) and composes; channels
form a monoid. A finite-dimensional CPTP channel, **after a declared input/output basis is chosen
and only the output diagonal is read**, induces a column-stochastic **population shadow**
$K(\gamma'\mid\gamma)=\sum_k|\langle\gamma'|A_k|\gamma\rangle|^2$ (column-stochastic because
$\sum_k A_k^\dagger A_k=I$). This shadow records **population transport only**: it does **not** mean
the channel preserves diagonality (a CPTP map may create output coherences even from a diagonal
input), and it does **not** determine the full CPTP map. Complete positivity and coherence
transport are the licensed lift, not forced by the classical kernel.

**Why a researcher should care.** "Quantum channel" arrives loaded with completely-positive
trace-preserving machinery. On the diagonal it collapses to the most ordinary object in applied
probability — a transition matrix — whose state-preservation and composition are one line each.
The framing isolates what is genuinely quantum (off-diagonal/CP transport, the lift) from what is
classical bookkeeping, and records the honest limit (pub-005): **CPTP monotonicity alone does not
uniquely select the trace-norm gauge** (additional operational assumptions are required).

In Local-Green/Global-Red terms: the stochastic population map is the green, phase-blind shadow;
CP transport of coherence is the structure the shadow does not fix.

1. Carrier


Finite outcome distributions $p:\Gamma\to\mathbb{Q}_{\ge0}$, $\sum_\gamma p_\gamma=1$ — the diagonal
densities of rung 3 (QM_007). A channel transports one distribution to another. [DEFINITION]

2. Primitive difference


The operative datum is the transition kernel; the "difference" a channel can introduce is
redistribution of mass across outcomes. [DEFINITION]

3. ZeroRel


The identity kernel fixes every distribution; two kernels agree iff they act identically on the
simplex. Since each basis distribution $e_\gamma$ is itself a simplex point, equality of kernel
action on the whole simplex is equivalent to equality of columns. [DEFINITION]

4. Structure


A classical channel is a stochastic kernel $K(\gamma'\mid\gamma)\ge0$, $\sum_{\gamma'}K(\gamma'\mid\gamma)=1$;
the quantum lift adds CP transport of off-diagonal coherence (outside this carrier). [DEFINITION / SCOPE FENCE]

5. The stochastic channel and the CPTP shadow


$(Kp)(\gamma')=\sum_\gamma K(\gamma'\mid\gamma)\,p_\gamma$.

**Theorem (Stochastic kernels preserve finite distributions; CPTP maps induce population shadows).**
(i) $K$ preserves states ($Kp\ge0$, $\sum_{\gamma'}(Kp)(\gamma')=1$);
(ii) $K\circ L$ is stochastic (channels compose; monoid with identity kernel);
(iii) a CPTP channel $\rho\mapsto\sum_k A_k\rho A_k^\dagger$ ($\sum_k A_k^\dagger A_k=I$) induces on
populations $K(\gamma'\mid\gamma)=\sum_k|\langle\gamma'|A_k|\gamma\rangle|^2$, which is
column-stochastic ($\sum_{\gamma'}K=\langle\gamma|\sum_k A_k^\dagger A_k|\gamma\rangle=1$).
[PROVEN, MECHANIZED — ENC-1127, `QM.StochasticChannel`; see "Mechanization"]

Proof: (i) total $=\sum_\gamma p_\gamma\sum_{\gamma'}K=\sum_\gamma p_\gamma=1$. (ii) column sums
multiply to $1$. (iii) $\sum_{\gamma'}|\langle\gamma'|A_k|\gamma\rangle|^2=\langle\gamma|A_k^\dagger A_k|\gamma\rangle$,
summed over $k$ is $\langle\gamma|I|\gamma\rangle=1$.

**Scope of (iii).** $K$ is the **output-diagonal** readout in the declared basis:
$p'_{\gamma'}=\langle\gamma'|\mathcal E(\operatorname{diag}(p))|\gamma'\rangle=\sum_\gamma K(\gamma'\mid\gamma)p_\gamma$.
The channel $\mathcal E$ may produce nonzero **output coherences** even from a diagonal input; $K$
captures only the diagonal of the output and does **not** determine $\mathcal E$ (many CPTP maps
share one population shadow). For a general input $\rho$ with off-diagonal terms, $\operatorname{diag}(\mathcal{E}(\rho))$ need not be determined by $K\cdot\operatorname{diag}(\rho)$; $K$ is the shadow of the channel on diagonal inputs, not the full channel. [SCOPE FENCE]

6. $\Phi_1$ versus $\Gamma_2$, and the lift


The classical kernel is the green population map. **Complete positivity / coherence transport is
the licensed lift** — not implied by the stochastic kernel (a stochastic matrix has many CPTP
pre-images, and some positive-but-not-completely-positive maps share its diagonal). Fenced. [SCOPE FENCE]

7. Observer


The induced stochastic kernel is basis-relative (it is the population map in the declared sector
basis); a different basis gives a different classical shadow of the same CPTP channel. [INTERPRETIVE]

8. Witnesses


Finite certificates: unit column sums (state-preservation) and the composition column-sum identity
(channels compose); for (iii), $\sum_k A_k^\dagger A_k=I$ ⇒ column-stochastic. [PROVEN — prose]

9. Operators / lifts


The stochastic kernel is the phase-blind realization of the channel; the CPTP/Kraus form is the
lift (coherence transport), and the Kraus→Choi→Stinespring representations are certified-transport
equivalents (cf. the CODA-MUR-Q pentagon, QM_092 / spine §VI.5.1) — imported, not implied. [SCOPE FENCE]

10. Route survivors


A distribution routes through $K$ to its image; the classical channel survives as the diagonal
shadow; CP transport is the lift on top. [DEFINITION / OPERATIONAL RULE]

11. Diagnostic and evidence result


Descent arc: a CPTP channel descends (on populations) to a stochastic kernel; applied to a
distribution it yields a distribution (trace preserved); composition stays stochastic. This is a
finite, replayable, non-authoritative diagnostic; terminal routing is separate.

**Green / red diagnostic firewall.**

- **GREEN (cheap, provable):** the stochastic kernel preserves states and composes; a CPTP channel
  descends to a column-stochastic population map. Elementary; PROVED-PROSE.

- **RED (not claimed):** a derivation of CPTP / quantum dynamics as ontology; that CP is forced by
  the classical kernel; that CPTP *selects* the trace-norm gauge (it is necessary-not-sufficient,
  pub-005); any grant of authority. $\mathsf{StructureDerived}\not\Rightarrow\mathsf{IsAuth}$.

12. Comparison to literature


This is the elementary fact that a stochastic matrix preserves probability and that a CPTP
channel's diagonal action is a stochastic map; the Kraus/Choi/Stinespring representations and
data-processing (CPTP) monotonicity are standard (pub-005 and QM_081 for the trace-norm geometry; the
CODA-MUR-Q Kraus–Choi–Stinespring pentagon for transport among representations). The contribution is
only the packaging — channels as stochastic kernels with the CPTP lift isolated — and the honest
necessary-not-sufficient fence. [INTERPRETIVE]

Worked example

Over $\Gamma=\{0,1\}$: the bit-flip kernel $K=\begin{psmallmatrix}0&1\\1&0\end{psmallmatrix}$
(columns sum to $1$) sends $p=(3/4,1/4)\mapsto(1/4,3/4)$ — a distribution (total preserved).
$K\circ K=I$ (composition stochastic). The CPTP bit-flip $\rho\mapsto X\rho X$ ($A_0=X$,
$A_0^\dagger A_0=I$) induces exactly this $K$ on populations; its coherence transport (off-diagonal)
is the lift not seen by $K$. [WORKED EXAMPLE]

Falsifiability

Falsified by a stochastic kernel that maps some distribution off the simplex, by a composite of
stochastic kernels that is not stochastic, or by a Kraus family with $\sum_k A_k^\dagger A_k=I$
whose population map is not column-stochastic — i.e. by the elementary identities being wrong.

What this paper does NOT claim

[SCOPE FENCE]

- **Not a derivation of CPTP / quantum dynamics as ontology** — only that a channel is a stochastic
  kernel and CPTP descends to one on populations.

- **CP is not forced** by the classical kernel (the lift is imported); **CPTP does not select the
  trace-norm gauge** (necessary-not-sufficient, pub-005).

- **Basis/sector-relative**; **mints no authority**.

Mechanization

The theorem is **MECHANIZED** (2026-06-19), secured as **ENC-1127** (status MECHANIZED). Lean:
`QM.StochasticChannel` — `stochastic_preserves_simplex`, `stochastic_compose`,
`kraus_diagonal_stochastic` — over `ℚ`, axioms ⊆ `{propext, Classical.choice, Quot.sound}`, verified
by a direct theorem-level Lean replay. The Kraus descent is mechanized at the population level (completeness `∑_k A_k†A_k=I`
as the declared diagonal hypothesis). **PL-QM041-1 discharged.**

```text
Lean target: QM
Replay receipt: consolidated QM target
Toolchain: leanprover/lean4:v4.31.0-rc1
Commit: 0c7b9915ec1b73bd65cf03a52b4efb01a7f4aab1
Axiom report: propext, Classical.choice, Quot.sound
```

References

- QM_007 (diagonal density, rung 3); pub-005 (CPTP / trace-norm geometry, necessary-not-sufficient);
  pub-010 (voice). Kraus / Choi / Stinespring representations and the CODA-MUR-Q transport pentagon
  (QM_092 / spine §VI.5.1).

Changelog

Version Note: v1.0 Pre-Print**(v0.1.1 and v0.2.0 moved to audit lineage)
Version Note: v2.0 (2026-06-19)** — External-review honesty pass + marked as a **component note** of the forthcoming *Finite QM Ingredient Ladder* (consolidation). Fixes: the abstract no longer says a CPTP channel "*is*" a stochastic kernel — it **induces a column-stochastic population shadow after a basis is chosen and only the output diagonal is read**, and a CPTP map may create output coherences even from a diagonal input (added §5 "Scope of (iii)"); subtitle fence "population shadows, not a derivation of quantum dynamics"; "CPTP *necessary-not-sufficient* for trace-norm" → "**CPTP monotonicity alone does not uniquely select the trace-norm gauge**" (pub-005); §3 ZeroRel now notes basis distributions are simplex points (so simplex-equality ⟺ column-equality). No math change; theorem still PROVED-PROSE (Lean TARGETED, PL-QM041-1).
Version Note: v1.1 (2026-06-17)**— First hygiene Improver pass + adversary gates. Rubric verified; claims typed; sibling Claim Ledger created. Theorem PROVED-PROSE; Lean handed to the Lean track as TARGETED (PL-QM041-1). No honesty-gating obligation.
Version Note: v1.0 (2026-06-17)** — Initial draft. QM ingredient-ladder rung 4 (channels / CPTP dynamics).

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-082-C1` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C1`) |
| `QM-082-C2` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C2`) |
| `QM-082-C3` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C3`) |
| `QM-082-C4` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C4`) |
| `QM-082-C5` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C5`) |
| `QM-082-C6` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C6`) |
| `QM-082-C7` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C7`) |
| `QM-082-C8` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C8`) |
| `QM-082-C9` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C9`) |
| `QM-082-C10` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C10`) |
| `QM-082-C11` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `082:QM-082-C11`) |

<!-- claim-id-body-index:end -->
