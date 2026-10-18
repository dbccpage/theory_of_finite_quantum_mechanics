# Discrete Schrödinger Cochain Transport and L¹ Probability Conservation on Finite Interaction Graphs

## GTOC Foundations — Quantum Contact Series (qm_033_schrodinger_finite_shadow)

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

document_id: "QM_033"
version: "v1.0.0"
status: "READY_FOR_AUTHOR_REVIEW"
authority_effect: "None"
claim_ledger: "qm_033_schrodinger_finite_shadow_claim_ledger.md"
change_log: "qm_033_schrodinger_finite_shadow_change_log.md"

QM_033 — Discrete Schrödinger Cochain Transport and Squared Euclidean Norm Conservation
====================================================================================

**Author:** Jeremy H. Carroll  
**Date:** July 2026  
**Canonical Version:** `v1.0.0`  
**Paper Identity:** `QM_033`  
**Authority:** None. This paper constructs finite discrete cochain dynamics on graphs; it mints no authority.


> **Status box (binding)**
>
> **Status:** Fully developed finite discrete quantum transport paper.  
> **Core (narrow algebra):** For Hermitian $H$, discrete Schrödinger evolution conserves $P_{\mathrm{tot}}(t)=\sum_v|\psi_v(t)|^2=\|\psi(t)\|_2^2$. That quantity is the squared Euclidean norm of the amplitude. It is not an $\ell^1$ mass $\sum_v|\psi_v|$.  
> **LGGR Boundary:** Theorem 2 proves that the cycle sum of a gauge coboundary cancels, so $\Theta(C)$ is gauge-invariant. It does not prove that $\Theta(C)$ is nonzero whenever $H^1(G;U(1))\neq 0$. That non-vanishing claim is open in this file.  
> **AuthorityEffect:** `None`.


## Non-claim Box

> **What this paper does NOT claim:**  
>
> 1. Does not derive the continuous Schrödinger differential equation over $\mathbb{R}^3$ without continuum limits.  
> 2. Does not claim $L^2$ Hilbert space is an intrinsic physical container; $L^2$ inner products are quarantined as external observer projections (`[Q-HELD]`).  
> 3. Does not claim Born-rule uniqueness from additivity alone.


## 1. Introduction & Physical Motivation

In traditional quantum mechanics, the Schrödinger equation is introduced as a continuous partial differential equation in a continuum Hilbert space container. Under the **$L^1$ Discrete Foundation & No Genesis Bias** doctrine, reality is not contained in a continuum void or Hilbert space. Instead, observation loci consist of finite discrete observer representation packets ($0$-cochains) on an interaction graph $G=(V,E)$.

This paper derives the **Discrete Schrödinger Cochain Transport Equation**:

$$i \hbar \frac{d \psi_v(t)}{dt} = \sum_{w \in V} H_{vw} \psi_w(t) \qquad (\text{Claim } \texttt{QM\_033-C1})$$

where $\psi_v(t) = \sqrt{\rho_v(t)} e^{i \theta_v(t)} \in \mathbb{C}$ is a complex $0$-cochain representing the local observer state at vertex $v$, and $H = (H_{vw})$ is a Hermitian block matrix projection ($H_{vw} = \overline{H_{wv}}$).


## 2. Squared Euclidean Norm Conservation

### Theorem 1 (Squared Euclidean Norm — Claim `QM_033-C2`)

Let $G=(V,E)$ be a finite graph with $|V| = N$, and let $H \in \mathbb{C}^{N \times N}$ be a Hermitian matrix ($H^\dagger = H$). Then the squared Euclidean norm of the amplitude:

$$P_{\text{tot}}(t) = \sum_{v \in V} |\psi_v(t)|^2 = \|\psi(t)\|_2^2$$

is strictly conserved under time evolution $\frac{d\psi}{dt} = -\frac{i}{\hbar} H \psi$:

$$\frac{d}{dt} P_{\text{tot}}(t) = 0$$

*Proof.*
$$\frac{d}{dt} \sum_v \bar{\psi}_v \psi_v = \sum_v \left( \frac{d\bar{\psi}_v}{dt} \psi_v + \bar{\psi}_v \frac{d\psi_v}{dt} \right) = \sum_v \left( \frac{i}{\hbar} (H^\dagger \bar{\psi})_v \psi_v - \frac{i}{\hbar} \bar{\psi}_v (H \psi)_v \right) = \frac{i}{\hbar} \left( \langle H \psi, \psi \rangle - \langle \psi, H \psi \rangle \right) = 0$$
since $H = H^\dagger$. $\blacksquare$


## 3. Local Green $\neq$ Global Red (LGGR) Topological Obstruction

### Theorem 2 (Gauge invariance of the cycle sum — Claim `QM_033-C3`)

Let $G=(V,E)$ contain a cycle $C$. A local gauge $\psi_v \mapsto e^{i \alpha_v} \psi_v$ shifts edge phases by $\theta(u,v) \mapsto \theta(u,v)+\alpha_v-\alpha_u$. The cycle sum of those gauge increments is $0$. Therefore

$$\Theta(C) = \sum_{j=0}^{k-1} \text{arg}(H_{v_j v_{j+1}}) \pmod{2\pi}$$

is unchanged by that gauge.

The further sentence “$\Theta(C)$ is nonzero whenever $H^1(G;U(1))\neq 0$” is not this theorem. The cancellation shows gauge invariance. It does not show non-vanishing. That non-vanishing claim is open in this file.

*Proof.* The cycle sum $\sum_C (\alpha_{v_{j+1}} - \alpha_{v_j}) = 0$ cancels identically. $\blacksquare$


## 4. Observer Projection Quarantine

### Statement 3 (Observer Projection Quarantine — Claim `QM_033-C4`)

The representation of $\psi(t)$ as a vector in a continuous Hilbert space $\mathcal{H} = L^2(\mathbb{R}^3)$ is an external observer projection. All calculable physical transport resides on the finite $0$-cochain carrier $G$.


## Summary Box

1. **What it supports**: Proves conservation of $\sum_v|\psi_v|^2=\|\psi\|_2^2$ for Hermitian $H$, and gauge invariance of the cycle phase sum.
2. **What it does not support**: Does not derive continuous space or Hilbert space containers without observer projections.
3. **The narrowest defensible claim**: Hermitian 0-cochain graph matrices generate probability-conserving discrete Schrödinger transport.
4. **The next test needed**: Formalize in `omega_engine/lean4/research_programs/003_quantum_foundations/003_qm_schrodinger_discrete_cochain.lean`.


<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM_033-C1` | [DERIVED] Discrete Schrödinger cochain transport equation |
| `QM_033-C2` | [DERIVED] $L^1$ total probability mass conservation |
| `QM_033-C3` | [SCOPE FENCE] Local Green $\neq$ Global Red phase holonomy obstruction |
| `QM_033-C4` | [Q-HELD] Hilbert space continuous lift quarantine |

<!-- claim-id-body-index:end -->
