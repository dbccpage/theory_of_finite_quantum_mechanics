# Density Matrices as Diagonal Residual Weights

## GTOC Foundations — Quantum Contact Series (qm_012_density_matrices_as_diagonal_residual_weights)

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

document_id: "OMEGA-QM-DIAG-DENSITY-038"
version: "v0.1.0 Pre-Print"
last_updated: "2026-06-17"
status: "DRAFT — component note (rung 3: diagonal density / mixed-state bookkeeping) of QM_121 (The Finite QM Ingredient Ladder)"
series: "qm / QM ingredient ladder"
companions:
- "pub-009 Conditional Density Lift and Dual-Witness Xi; pub-010 Born Normalization (voice)"
- "QM_002 Residual Density Calculus (RDB-01..13)"

---

> **Component note (rung 2) of *QM_121 — The Finite QM Ingredient Ladder*.** The publishable synthesis
> is QM_121; this note is the detailed source for the diagonal-density rung, and keeps its own claim
> ledger.

Abstract

**Main result (informal).** A finite residual-weight distribution, placed on the diagonal, is
already a finite diagonal density carrier: nonnegative diagonal makes it positive semidefinite, the weights sum
to one makes it trace-one. Its purity is $\operatorname{tr}(\rho^2)=\sum_\gamma p_\gamma^2$ — one
exactly when the weight sits on a single sector (pure), below one otherwise (mixed). The
off-diagonal coherences are *not* fixed by the weights; they are the same non-forced lift that
pub-010 found for the Hilbert encoding. A "mixed state" is nothing more mysterious than the
residual-weight distribution.

**Why a researcher should care.** The density matrix is usually introduced as primitive
machinery (a PSD trace-one operator) and "mixedness" as a separate notion. Read on residual
weights, the diagonal density needs no postulate — it is the obstruction-quotient's own weight
distribution, and purity is one finite number computed from it. The framing also fixes what is
*not* free: coherence (off-diagonal structure) is imported, not implied — exactly where an
$\ell^1$ account would otherwise overclaim a derivation of quantum coherence.

In Local-Green/Global-Red terms: the diagonal (classical-mixture) density is the green,
phase-blind shadow of the weights; coherence is the global structure that shadow cannot fix.

1. Carrier


Finite residual sector weights $w:\Gamma\to\mathbb{Q}_{\ge0}$ with $W=\sum_\gamma w_\gamma>0$ — the
same L1 residual carrier as the rest of the ladder (pub-010, QM_070). Write $p_\gamma=w_\gamma/W$.
The descent reads a state's sector populations into $w$. [DEFINITION]

2. Primitive difference


The operative datum is the weight distribution itself; the "difference" from a pure state is the
spread of $p$ across more than one sector (mixedness). [DEFINITION]

3. ZeroRel


Two weight vectors give the same diagonal density iff they have the same normalized distribution
$p$ (scalar-ray equivalence, as in pub-010). [DEFINITION]

4. Structure


The diagonal density is the residual-weight distribution realized as an operator; no higher
cochain object is needed. Off-diagonal coherence sits outside this carrier (see §6). [DEFINITION / SCOPE FENCE]

5. The diagonal density and its purity


$$
\rho_{\gamma\gamma'} = [\gamma=\gamma']\,p_\gamma,\qquad p_\gamma=w_\gamma/W .
$$

**Theorem (Diagonal density is a state; purity).** For $W>0$:
(If $W=0$, the diagonal-density constructor refuses / is undefined.)
(i) $\rho$ is PSD and $\operatorname{tr}\rho=1$ (a valid finite diagonal density carrier);
(ii) $\operatorname{tr}(\rho^2)=\sum_\gamma p_\gamma^2\in(0,1]$, $=1$ iff $w$ is concentrated on one
sector (pure); mixedness $=1-\sum_\gamma p_\gamma^2$.
[PROVEN, MECHANIZED — ENC-1126, `QM.DiagonalDensity`; see "Mechanization"]

Proof: (i) nonnegative diagonal ⇒ PSD; trace $=\sum p_\gamma=1$. (ii) $0\le p_\gamma\le1$,
$\sum p_\gamma=1$ ⇒ $\sum p_\gamma^2\le\sum p_\gamma=1$, equality iff one $p_\gamma=1$.

6. $\Phi_1$ versus $\Gamma_2$, and coherence


Mixedness $1-\sum p_\gamma^2$ is the finite spread diagnostic. **Coherence (off-diagonal entries)
is the non-forced lift:** it is not a function of $w$ — exactly pub-010's redundant-Hilbert-lift
phenomenon at the density level (the diagonal is the phase-blind shadow; coherence is imported,
licensed structure, cf. QM_002 RDB licensed-coherence). It is fenced out of this carrier. [SCOPE FENCE]

7. Observer


The diagonal density is observer/basis-relative: it is the population distribution in the declared
sector basis. A different basis has a different diagonal (and different off-diagonal coherence). [INTERPRETIVE]

8. Witnesses


The finite certificates are PSD + trace-one (a valid state) and the purity value (a single
rational, $1$ iff pure). [PROVEN — prose]

9. Operators / lifts


The diagonal density is the phase-blind realization of $w$; the licensed *lift* adds off-diagonal
coherence (not forced) and, separately, channel dynamics (rung 4) acts on it — both imported, not
implied by $w$. [SCOPE FENCE]

10. Route survivors


A residual-weight distribution routes to its diagonal density; pure (one sector) vs mixed
(spread) is read off the purity. [DEFINITION / OPERATIONAL RULE]

11. Diagnostic and evidence result


Descent arc: sector populations → weights → diagonal density (PSD, trace-one) with a computed
purity. This is a finite, replayable, non-authoritative diagnostic; terminal routing is separate.

**Green / red diagnostic firewall.**

- **GREEN (cheap, provable):** the diagonal density from residual weights is a valid state; purity
  $=\sum p_\gamma^2$, $1$ iff pure. Elementary; PROVED-PROSE.

- **RED (not claimed):** that this derives the density-operator formalism as ontology; that
  coherence is forced by the weights (it is an imported lift); CPTP dynamics (rung 4); any grant of
  authority. $\mathsf{StructureDerived}\not\Rightarrow\mathsf{IsAuth}$.

12. Comparison to literature


This is the elementary fact that a probability vector is a diagonal density operator and purity
$\operatorname{tr}(\rho^2)=\sum p_i^2$ measures mixedness; pub-009 gives the conditional density
lift and dual-witness Ξ, and QM_002 as the more general residual-density bridge theorem package (RDB-01..13). The contribution is
only the packaging — mixed states as residual-weight distributions, coherence isolated as the
non-forced lift, with one-line proofs. (It supersedes the now-retired QM_091 Rust-blueprint, which is not a
derivation.) [INTERPRETIVE]

Worked example

Over $\Gamma=\{0,1\}$ with $w=(3,1)$, $W=4$, $p=(3/4,1/4)$:

- $\rho=\operatorname{diag}(3/4,1/4)$ — PSD, trace $1$ (a valid mixed state). [WORKED EXAMPLE]
- purity $\operatorname{tr}(\rho^2)=(3/4)^2+(1/4)^2=10/16=5/8<1$ (mixed); mixedness $3/8$.
- $w=(4,0)$ gives $p=(1,0)$, purity $1$ (pure). The off-diagonal of a Bell-derived state is *not*
  visible here — that coherence is the imported lift, not implied by the diagonal. [WORKED EXAMPLE]

Falsifiability

The theorem is falsified by a nonnegative normalized weight vector whose diagonal operator is not
PSD or not trace-one, or by a purity value outside $(0,1]$, or by $\operatorname{tr}(\rho^2)=1$
without single-sector concentration — i.e. by the elementary identities being wrong.

What this paper does NOT claim

[SCOPE FENCE]

- **Not a derivation of the density-operator formalism as ontology** — only that the residual-weight
  distribution *is* a diagonal density.

- **Coherence is not forced** — off-diagonal structure is an imported lift, not implied by $w$.
- **No dynamics** — CPTP channels are rung 4 (separate); **basis/sector-relative**; **mints no authority**.

Mechanization

The theorem is **MECHANIZED** (2026-06-19), secured as **ENC-1126** (status MECHANIZED). Lean:
`QM.DiagonalDensity` — `diag_density_trace_one`, `diag_density_psd` (PSD quadratic-form
`∑ pᵢ xᵢ² ≥ 0`), `purity_le_one`, `purity_one_iff_pure` (full iff) — over `ℚ`, axioms ⊆
`{propext, Classical.choice, Quot.sound}`, verified by a direct theorem-level Lean replay. **PL-QM038-1 discharged.**

```text
Lean target: QM
Replay receipt: consolidated QM target
Toolchain: leanprover/lean4:v4.31.0-rc1
Commit: 0c7b9915ec1b73bd65cf03a52b4efb01a7f4aab1
Axiom report: propext, Classical.choice, Quot.sound
```

References

- pub-009 (conditional density lift + dual-witness Ξ); pub-010 (Born/L1, redundant lift, voice);
  QM_002 (Residual Density Bridge, RDB-01..13).

Changelog

Version Note: v1.0 Pre-Print**(v0.1.1 and v0.1.2 moved to audit lineage)
Version Note: v1.2 (2026-06-19)** — Lean mechanization completed; PL-QM038-1 discharged.
Version Note: v1.1 (2026-06-17)**— First hygiene Improver pass + adversary gates. Rubric verified; claims typed; sibling Claim Ledger created. Theorem PROVED-PROSE; Lean handed to the Lean track as TARGETED (PL-QM038-1). No honesty-gating obligation.
Version Note: v1.0 (2026-06-17)** — Initial draft. QM ingredient-ladder rung 3: diagonal density / mixed-state bookkeeping.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-012-C1` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C2` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C3` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C4` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C5` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C6` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C7` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C8` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C9` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C10` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C11` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-012-C12` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |

<!-- claim-id-body-index:end -->
