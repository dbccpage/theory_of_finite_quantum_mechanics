# Finite Path-Sum as Graded Transport — the Feynman path integral, decomposed, and what probability is in quantum mechanics

## GTOC Foundations — Quantum Contact Series (qm_031_finite_path_sum_as_graded_transport)

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

document_id: "OMEGA-QM-PATHSUM-042"
version: "v0.1.0 Pre-Print"
last_updated: "2026-06-19"
status: "DRAFT — component note (synthesis rung) of QM_121 (The Finite QM Ingredient Ladder)"
series: "qm / QM ingredient ladder — synthesis rung"
companions:
- "pub-010 Born Normalization and Conditional Hilbert Lift from L1 Weights (the probability stand)"
- "pub-005 CPTP-Invariant Obstruction Theory (the trace-norm/CPTP boundary)"
- "QM_082 Channels as Stochastic Kernels (population shadows of dynamics)"
- "QM_060 Superposition as the Quotient Fiber (the phase fiber)"
- "QM_061 Interference as the Non-L1 Resource (the cross term)"
- "QM_090 Continuum Shadow Non-Promotion (the imported continuum lift)"
- "QM_010 CODA-A Feynman finite-shadow histories (mechanized finite-shadow, ENC-1072)"
mechanization: "§5 pathSum=Mⁿ + Chapman–Kolmogorov MECHANIZED (ENC-1128: lean4.QM.FinitePathSum — pathSum_eq_matpow/matpow_compose, axiom-clean on the standard Mathlib set); graded finite-shadow core MECHANIZED Classical.choice-free (ENC-1072: lean4.QM.FinitePathSumReplay, FiniteFeynmanShadow); interference reuse MECHANIZED (QM_061 InterferenceBuildability / pub-010 BornRedundancy)"

Finite Path-Sum as Graded Transport
===================================

### The Feynman path integral, decomposed — a finite-shadow synthesis with a fenced stand on quantum probability; *not* a derivation of the path integral, the Born rule, or quantum ontology

> **Component note (rung 4) of *QM_121 — The Finite QM Ingredient Ladder*.** The publishable synthesis
> is QM_121; this note is the detailed source for the path-sum rung (and carries the fuller form of the
> probability stand), and keeps its own claim ledger.

0. Scope fences (read first)


This is a **decomposition + a position paper over already-proven components**, not a
derivation. Explicitly:

- **Not the continuum path integral.** Only its finite, exact *graded-transport
  shadow*. The measure on path space and its convergence are an **imported analytic
  lift** (QM_090; `OracleNeeded`).

- **Not a derivation of quantum mechanics, the Born rule, or unitary dynamics.** The
  $\mathbb C$/$U(1)$ phase carrier, the size-independent generation density, and the
  continuum limit are **imported**.

- **The "stand" of §7 is a *position*, not a new theorem.** Its load-bearing
  components are pub-010's proven theorems; the *framing* ("probability in QM is
  classical L1 normalization") is `[INTERPRETIVE]`, defensible from those components.
  **Born-quadratic uniqueness stays imported (Gleason; pub-010 Thm 6).**

- **Mints no authority:** $\mathsf{StructureDerived}(F,c)\not\Rightarrow\mathsf{IsAuth}(t)$.

Abstract

**Main result (informal).** The Feynman "sum over histories" decomposes, finitely,
into three separable layers, and the decomposition makes precise *where the
classical part ends and the quantum part begins*:

1. **a graded-transport skeleton** — the $n$-step propagation weight is the
   **path-sum**, the sum over length-$n$ histories of edge-weight products, and this
   *is exactly* the $n$-th matrix power $M^n$, composing by Chapman–Kolmogorov. This
   layer is **classical, nonnegative, and finite** (the finite-shadow core is
   mechanized, ENC-1072);

2. **a phase/amplitude lift & EPK gluing defect (G3)** — replacing nonnegative weights by phase-bearing
   amplitudes turns the path-sum into the Feynman *amplitude* sum; the genuinely
   non-classical content enters **here**, as **interference** (the cross term that
   diagonal/L1 data cannot carry — QM_061 / pub-010 Thm 7), and the superposed phase
   is exactly the quotient fiber over the weights (QM_060). When evaluator factorization fails
   ($E(\gamma_2 \circ \gamma_1) \neq E(\gamma_1) E(\gamma_2)$), the EPK composition law acquires
   a non-zero Evaluator Gluing Defect $\Delta_E = E_g - E_1 E_2$ (019_lggr_i / omega_epk),
   quantifying non-compositional interference as an $L^1$ residual mass;

3. **an imported continuum limit** — a measure on an infinite path space with
   convergence certificates, *not* forced by the finite graph (QM_090).

**The stand (§7).** This decomposition forces a position on *what probability is in
quantum mechanics*: **at the finite diagonal / residual-weight level, probability in QM is the L1 normalization of nonnegative
additive residual weights — the same rule as classical probability.** The Born rule
$P=|c|^2/\sum|c|^2$ is a **redundant re-encoding** of $P=w/\sum w$ (pub-010 Thm 1 &
4); For probability normalization, the Born square is redundant once the nonnegative sector weights $w_\gamma$ are already supplied. The physical content lies in why that Hilbert lift, phase carrier, and quadratic readout are the right imported interface. The genuinely quantum surplus is **phase
/ interference (layer 2 — dynamics)**, *not* the probability rule. The one thing that
singles out the Born *quadratic form* over another functional is **imported**
Hilbert/Gleason structure (pub-010 Thm 6), which is *not* derived here.

**Why a researcher should care.** The path integral is usually taught as an
irreducibly quantum, continuum object. This paper shows its *skeleton* is the most
elementary fact in linear algebra (a matrix power counts weighted walks), its
*quantum* content is one isolable thing (phase → interference), and its *continuum*
is an imported analytic lift — and that, once you see this, the Born rule stops
looking like a new law of probability and starts looking like a re-encoding of the
classical one. In Local-Green / Global-Red terms: the finite graded path-sum is the
green, exact propagation; the continuum integral and the Born *ontology* stay red
without their imported certificates.


Part I — The graded-transport skeleton (classical, finite, exact)

### 1. Carrier

A finite state set with a weighted transition matrix $M$ over a commutative semiring
(e.g. $\mathbb Q_{\ge 0}$), $M(b\mid a)$ the weight of edge $a\to b$. The descent
reads a dynamics into its finite transition weights. *(Commutativity is a
simplifying convenience that avoids ordering issues in path-weight products; minimal
algebraic hypotheses are not the point of this synthesis. For ordered/noncommutative operator-valued transport, path order is additional declared structure and is not covered by this finite scalar semiring theorem.)* [DEFINITION]

### 2. Primitive difference

The operative datum is the multi-step transition weight; the "difference" between a
direct $n$-step weight and a composite-through-intermediates weight is what
Chapman–Kolmogorov resolves to zero. [DEFINITION]

### 3. ZeroRel (Omega bookkeeping, not theorem payload)

Two propagation accounts are identified iff they assign the same path-sum to every
$(a,b,n)$; intermediate cuts respecting Chapman–Kolmogorov are identified. This is an
Omega bookkeeping definition; it carries no mathematical weight of its own.
[DEFINITION / OMEGA BOOKKEEPING]

### 4. Structure

The $n$-step propagator is $M^n$; the path-sum is its expansion over length-$n$
paths. No higher structure is needed for the finite statement.
[DEFINITION / SCOPE FENCE]

### 5. The path-sum identity

**Theorem (Finite graded path-sum identity).**
(i) $(M^n)(b\mid a)=\sum_{a=v_0\to\cdots\to v_n=b}\prod_{i=1}^n M(v_i\mid v_{i-1})$;
(ii) $M^{m+n}=M^m M^n$ — Chapman–Kolmogorov:
$(M^{m+n})(c\mid a)=\sum_b (M^m)(c\mid b)(M^n)(b\mid a)$.
[PROVEN, MECHANIZED — ENC-1128, `QM.FinitePathSum`
(`pathSum_eq_matpow`, `matpow_compose`), axiom-clean on the standard Mathlib set;
the graded finite-shadow realization is additionally MECHANIZED `Classical.choice`-free
as ENC-1072; see Mechanization]

*Proof.* Induction on $n$ — appending one edge to each length-$n$ path is exactly
$(M^{n+1})(b\mid a)=\sum_c M(b\mid c)(M^n)(c\mid a)$; (ii) is associativity of the
semiring matrix product. $\square$

**Worked example.** Two states $\{0,1\}$, $M=\begin{psmallmatrix}0&1\\1&0\end{psmallmatrix}$
(a swap). The length-2 walks $0\to1\to0$ and $1\to0\to1$ give $M^2=I$; $M^3=M$. The
$n$-step weight is the count of weighted length-$n$ walks — no continuum needed.
(Mechanized: `swap2_sq`, `swap2_cube` in `QM.FinitePathSum`.)
[WORKED EXAMPLE]

**This is the finite *shadow* of "sum over histories," not the Feynman integral.**
The finite combinatorial shadow of a sum-over-histories propagation is matrix
multiplication: path weights multiply along a history and sum over alternatives. The
Feynman path *integral* requires the layer-2 and layer-3 imports below (complex
amplitudes, action/phase, a path-space measure, convergence). [SCOPE FENCE]


Part II — The phase lift (where "quantum" enters: interference)

### 6. From weights to amplitudes — and the only non-classical step

Replace the nonnegative weight $M(b\mid a)$ by a phase-bearing **amplitude**
$A(b\mid a)\in\mathbb C$. The path-sum becomes the phase-lifted finite shadow of Feynman sum-over-histories
$\sum_{\text{paths}}\prod A$, and the observable is $|{\cdot}|^2$. Two facts, both
already proven elsewhere in the corpus, pin down exactly what this lift adds:

- **The phase is the quotient fiber (QM_060 / pub-010 Thm 3–4).** Relative to a fixed
  sector basis, the amplitude's phase is invisible to the phase-blind L1 quotient: it
  is the fiber over the diagonal weights, carrying no diagonal-readout probability.
  [reuse — QM_060; pub-010 PROVEN]

- **Interference is the non-L1 resource (QM_061 / pub-010 Thm 7).** The cross term
  $\sum_{i\neq j}A_i^* A_j$ — the deviation of $|\sum A|^2$ from $\sum|A|^2$ — is
  *not* a function of the diagonal weights: two amplitude configurations with
  identical L1 data can have different interfered outcomes (witness $(1,1)$ vs
  $(1,-1)$: same weights, interfered $4$ vs $0$). **This is the only place the
  amplitude lift departs from the classical path-sum.** [reuse — pub-010 Thm 7,
  MECHANIZED; QM_061]

So the quantum content of the path integral is **layer 2 = phase → interference**:
not the transport (layer 1, classical) and not the continuum (layer 3, imported).
That amplitudes carry phase at all (the $\mathbb C$/$U(1)$ carrier) is **imported**
(the open $U(1)$-selector), not derived. [IMPORTED]


Part III — The stand: what probability *is* in quantum mechanics

### 7. Probability is L1 normalization; the Born square is redundant

The decomposition forces a position, stated here as a **defensible stand**, with each
clause backed by a proven component or fenced as an import:

> **Quantum probability is not sui generis. It is the L1 normalization of
> nonnegative additive residual (sector) weights — the *same* rule as classical
> probability.**

1. **Probability = L1 normalization.** Given nonnegative additive sector weights
   $w_\gamma$, $P(\gamma)=w_\gamma/\sum_\eta w_\eta$ is already a probability law — no
   Hilbert space required. [STANDARD / reuse — pub-010 Theorem 1, PROVEN+MECHANIZED]

2. **The Born square is redundant re-encoding.** A Hilbert lift
   $c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}$ reproduces the *identical* law:
   $|c_\gamma|^2/\sum|c_\eta|^2 = w_\gamma/\sum w_\eta$. The Born normalization adds no
   probability content; the square is bookkeeping. [reuse — pub-010 Theorem 4,
   PROVEN+MECHANIZED]

3. **The quantum surplus is phase/interference (dynamics), not probability.** What the
   lift *does* add is the phase, which is probability-inert on the diagonal readout
   (clause above) and becomes visible only as **interference under mixing** — a
   property of the *dynamics* (Part II), not of the probability assignment.
   [reuse — pub-010 Theorem 7 / QM_061, MECHANIZED]

4. **Born *uniqueness* is imported, not derived.** That the probability functional is
   the *quadratic* $|\cdot|^2$ rather than some other form is selected only after
   importing complex-Hilbert representation, orthogonal-sector additivity, and
   Gleason/frame-function structure. This paper does **not** derive it. [IMPORTED —
   pub-010 Theorem 6; Gleason]

**The stand (the framing).** Putting 1–4 together: *probability in QM is classical L1
normalization of obstruction weights; the Born square is a redundant encoding of it,
not an independent law; the genuinely quantum thing is phase/interference, which is
dynamics; and the specific quadratic form is an imported representation choice.* This
is a **position**, defensible from the proven components 1–4 — it is **not** a claim
that QM, the Born rule, or its uniqueness is *derived* from L1 structure (that would
require deriving clause 4, which is fenced as imported). [INTERPRETIVE — a stand over
PROVEN components; the firewall against the origin-overclaim is clause 4]

### 8. The continuum lift (imported)

The continuum path integral — a measure on an infinite path space with convergence
certificates — is the layer-3 lift, **not** forced by the finite weighted graph
(QM_090; convergence is `OracleNeeded`). The finite path-sum is exact and replayable;
the continuum is where analysis must be imported. [SCOPE FENCE / IMPORTED]

### 9. Readout: channels as population shadows (QM_082)

Closing the loop to measurement: a finite-dimensional CPTP channel, *after a declared
input/output basis is chosen and only the output diagonal is read*, induces a
column-stochastic **population shadow** $K(\gamma'\mid\gamma)=\sum_k|\langle\gamma'|A_k|\gamma\rangle|^2$
(QM_082). This is the layer-1 (classical transport) reading of dynamics; it records
population transport only and does **not** determine the full channel or carry the
layer-2 coherence. [reuse — QM_082]


10. Mechanization


| layer / claim | status | artifact |
|---|---|---|
| finite-shadow path-sum replay | **MECHANIZED** (ENC-1072) | `QM.FinitePathSumReplay`, `FiniteFeynmanShadow` |
| `pathSum = Mⁿ` + Chapman–Kolmogorov (§5) | **MECHANIZED** (ENC-1128) | `QM.FinitePathSum` (`pathSum_eq_matpow`, `matpow_compose`, `matpow_compose_apply`, `pathSum_compose`; swap-matrix replay `swap2_sq`/`swap2_cube`; axiom-clean) |
| interference ∉ L1 (Part II / §6) | **MECHANIZED** (reuse) | `QM.InterferenceBuildability`; `PaperQF002.L010_01_BornRedundancy` |
| probability = L1 norm; Born redundancy (§7.1–7.3) | **MECHANIZED** (reuse, pub-010 Thm 1/4/7) | `PaperQF002.L010_01_BornRedundancy` |
| Born uniqueness (§7.4) | IMPORTED (Gleason) — not mechanized, not claimed | pub-010 Thm 6 |
| continuum limit (§8) | IMPORTED / `OracleNeeded` — not claimed | QM_090 (ENC-1078) |

**Mechanization receipt.** The proof ledger records checked replays for the stable Lean targets `QM.FinitePathSum`, `QM.InterferenceBuildability`, `QM.FinitePathSumReplay`, and `QM.FiniteFeynmanShadow`. The frozen receipt binds toolchain `leanprover/lean4:v4.31.0-rc1`, commit `0c7b9915ec1b73bd65cf03a52b4efb01a7f4aab1`, and the axiom report `propext`, `Classical.choice`, `Quot.sound`. Exact replay commands and source locations remain in that evidence ledger, not this paper.

The named theorems carry `#print axioms` audits. With `FinitePathSum` landed,
**every load-bearing identity native to this paper is mechanized**: `pathSum = Mⁿ`
and Chapman–Kolmogorov (ENC-1128, standard Mathlib axioms) and their graded
finite-shadow realization (ENC-1072, `Classical.choice`-free). The only
non-mechanized elements are the deliberately **imported** ones — §7.4 Born-quadratic
uniqueness (Gleason) and §8 the continuum limit — which the firewall keeps imported,
not claimed.

11. Claim status (the honest hierarchy)


| status | claims |
|---|---|
| **PROVEN / MECHANIZED** | `pathSum = Mⁿ` + Chapman–Kolmogorov (§5; native, ENC-1128, `FinitePathSum`); path-sum finite-shadow replay (ENC-1072); interference ∉ L1 (pub-010 Thm 7 / QM_061); probability = L1 normalization & Born-normalization redundancy (pub-010 Thm 1/4); superposed phase = quotient fiber (QM_060) |
| **INTERPRETIVE** | the three-layer Feynman decomposition; **the stand** (probability is classical L1 normalization; the quantum surplus is phase/interference, not probability) — a position over the proven components |
| **IMPORTED / CONDITIONAL** | the $\mathbb C$/$U(1)$ phase carrier; the continuum measure + convergence; Born-*quadratic* uniqueness (Gleason) |
| **NOT CLAIMED** | derivation of the continuum path integral; that complex/unitary amplitudes are forced; derivation of the Born rule or its uniqueness; that QM probability is *non-fundamental* or *explained away* (that is the Level-3 overclaim we refuse); any grant of authority |

Falsifiability

Falsified by: a finite $M,n$ with $(M^n)(b\mid a)\ne$ the length-$n$ path-sum, or
$M^{m+n}\ne M^mM^n$ (§5 wrong); an L1 functional reproducing the interfered outcome
(refuting the layer-2 / §6 claim); or a nonnegative weight vector and phase choice
where $|c_\gamma|^2/\sum|c_\eta|^2\ne w_\gamma/\sum w_\eta$ (refuting the §7
redundancy). The *stand* is weakened — not refuted — if Born-quadratic uniqueness is
shown to follow from L1 additivity *without* the imported Gleason-type assumptions
(which would upgrade clause 4 from imported to derived).

What this paper does NOT claim

[SCOPE FENCE — see also §0]

- **Not the continuum path integral**, only its finite matrix-power shadow.
- **Complex/unitary amplitudes are not forced**; the phase carrier is imported.
- **The Born rule is not derived, and its quadratic uniqueness is imported** (Gleason).
- **The stand is not an origin claim.** "Probability is classical L1 normalization" is
  a *position* over proven redundancy + an explicit imported-uniqueness fence; it is
  **not** "QM probability is derived / explained away / non-fundamental."

- **Basis/representation-relative**; **mints no authority.**

References

- pub-010, *Born Normalization and Conditional Hilbert Lift from L1 Weights* (Thm 1
  normalization, Thm 4 Born redundancy, Thm 7 interference cross term, Thm 6
  conditional Born uniqueness / Gleason import).

- pub-005, *CPTP-Invariant Obstruction Theory* (the trace-norm/CPTP boundary).
- QM_082 (channels / population shadows); QM_060 (superposition fiber); QM_061
  (interference ∉ L1); QM_090 (continuum non-promotion); QM_010 (CODA-A Feynman
  finite-shadow, ENC-1072); QM_110 (finite weighted transport).

- A. M. Gleason, *Measures on the closed subspaces of a Hilbert space*, J. Math. Mech.
  **6** (1957) 885 (the imported uniqueness route, §7.4).

- R. P. Feynman, *Space-time approach to non-relativistic quantum mechanics*, Rev.
  Mod. Phys. **20** (1948) 367 (the continuum object this paper takes the finite
  shadow of).

Changelog

Version Note: v1.0 Pre-Print**(v0.1.1, v0.2.0, and v0.2.1 moved to audit lineage)
Version Note: v2.1 (2026-06-19)** — **§5 mechanized.** Landed `QM.FinitePathSum`
  (`pathSum_eq_matpow` = path-sum = `Mⁿ`; `matpow_compose` = Chapman–Kolmogorov
  `M^(m+n)=M^m M^n` = `pow_add`; `matpow_compose_apply`, `pathSum_compose`; swap-matrix
  worked-example replay `swap2_sq`/`swap2_cube`), general over any finite index type and
  any `CommSemiring`, axiom-clean on the standard Mathlib set. This flips QM-031-C5 /
  ENC-1128 from PROVED-PROSE + Lean-TARGETED to **MECHANIZED** and discharges PL-QM042-1;
  the paper now has **no non-mechanized native load-bearing identity** (only the
  deliberately imported §7.4 Gleason uniqueness and §8 continuum remain imported). No
  math change.

Version Note: v2.0 (2026-06-19)** — Major expansion from a path-sum note into the synthesis
  ("granddaddy") rung: added the **three-layer Feynman decomposition** (graded
  skeleton / phase lift / imported continuum), **Part III the stand on quantum
  probability** (Level-2: probability = classical L1 normalization, Born square
  redundant, quantum surplus = phase/interference, Born-uniqueness imported), the
  readout tie-in (QM_082), a claim-status table, the mechanization table + repro
  block, and §0 scope fences before the body. Applied external-review honesty fixes:
  "finite *shadow* of sum-over-histories," not "the Feynman sum is matrix
  multiplication"; semiring-scope note; ZeroRel marked Omega-bookkeeping (not theorem
  payload); rung relabeled "synthesis rung" (was "path-sum / unitary dynamics" —
  unitary dynamics is *not* derived here). Fixed a literal `\n`-escape corruption in
  §1. No math change to §5; the stand's components are all reuse of pub-010's proven
  theorems.

Version Note: v1.1 (2026-06-17)** — First hygiene Improver pass + adversary gates; sibling
  Claim Ledger created; theorem PROVED-PROSE, Lean TARGETED (PL-QM042-1).

Version Note: v1.0 (2026-06-17)** — Initial draft. QM ingredient-ladder path-sum note.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-031-C1` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C1`) |
| `QM-031-C2` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C2`) |
| `QM-031-C3` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C3`) |
| `QM-031-C4` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C4`) |
| `QM-031-C5` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C5`) |
| `QM-031-C6` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C6`) |
| `QM-031-C7` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C7`) |
| `QM-031-C8` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C8`) |
| `QM-031-C9` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C9`) |
| `QM-031-C10` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C10`) |
| `QM-031-C11` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C11`) |
| `QM-031-C12` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C12`) |
| `QM-031-C13` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C13`) |
| `QM-031-C14` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C14`) |
| `QM-031-C15` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C15`) |
| `QM-031-C16` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C16`) |
| `QM-031-C17` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C17`) |
| `QM-031-C18` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `031:QM-031-C18`) |

<!-- claim-id-body-index:end -->
