# 011 State Effect Pairing Audit

## GTOC Foundations — Quantum Contact Series (qm_011_state_effect_pairing_audit)

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

QM_011 — State–Effect Pairing Non-Selection Audit
=================================================

**Born as an imported registry row, not a selected rule**

Series: qm / QM Atlas (paper QM_011)

**Lead.** Given a *declared* finite state/effect packet, this paper audits — it does **not** derive — which probability pairings are compatible with terminal gluing: a candidate pairing is checked, row by row, against positivity, normalization, transport coherence, and local-to-global terminal agreement, and assigned a typed terminal status. The main result is the Lean-backed non-selection theorem: the declared compatibility skeleton does **not** uniquely select Born. The Born trace pairing enters as one **imported** registry row whose local replay can pass; it is **not** uniquely selected over its rivals by the audit, and sealed authority remains a separate question. [SCOPE FENCE — selector audit, not a Born/Hilbert derivation]

**Why a researcher should care.** Reconstruction programs (operational/GPT, Spekkens-style epistemic toys, quantum-logic and Hardy-style axiomatics) all ask *which* probability rule a physical theory is forced to carry. This paper offers a finite, replayable discipline for that question that refuses to overclaim: each candidate pairing — classical simplex, square-bit GPT, Spekkens toy, real/complex Hilbert, quaternionic, and a nonlinear control — is graded by the *same* finite checks, so "this pairing is terminal-compatible" becomes a checked computation with an exact boundary, rather than a reconstruction claim. The headline non-result (the compatibility skeleton does not uniquely select Born) is machine-checked.

Thesis

The local-to-global gluing layer now exists:

```text
finite local packets

+ certified transport
+ terminal agreement
+ coherent cone/projection replay
-> lawful global terminal
```

The relevant foundations are:

* GTOR-21: Coherent Limit Authority Gluing Theorem (Sufficiency).
* GTTC-7: Cofinal Shadow Introduction Rule, the directed/cofinal face of GTOR-21.

These theorems do not manufacture authority. They read a declared terminalizer and state when compatible local authority may be inherited by a global terminal. GTOR-21 remains proved-prose and is not mechanized.

The next QM-facing target is narrower than a Born-rule derivation:

```text
Under a declared finite state/effect packet,
when is the probability pairing terminalization-compatible?
```

O024 Target

```text
O024: Born-Compatible Pairing Audit

Terminal-compatible probability pairings are constrained by positivity,
normalization, transport, and gluing.
```

*Status of the target.* The statement "terminal-compatible pairings are constrained
by [the seven checks]" is **definitional** — *compatibility is defined as* passing
those finite checks, so this is the audit's contract, not a theorem.
[DEFINITION / OPERATIONAL RULE — compatibility = passing the declared finite checks.]
The genuinely *proven* content of O024 is the **non-selection** firewall — that the
declared compatibility skeleton does **not** uniquely pin down a pairing (in
particular does not single out Born), and that probability is effect-relative
[PROVEN — Lean-mechanized, ENC-1070; see Lean Support]. Each registry row's verdict
is then a [PROVEN, CONDITIONAL — registry-relative; per declared packet, conditional
on the scoped terminalizer $\Pi_\sharp$] finite replay. The audit is relative to the
declared registry and mints no authority (firewall ENC-1063,
$\mathsf{StructureDerived}\not\Rightarrow\mathsf{IsAuth}$).

Non-claim:

```text
O024 does not derive the Born rule or select complex Hilbert QM.
```

[SCOPE FENCE — Born and complex Hilbert structure are IMPORTED registry rows, never derived or uniquely selected by the audit.]

Packet Schema

Each registry row declares:

```text
(S, E, <->, T, Pi_sharp)
```

| Field | Meaning |
|---|---|
| `S` | Declared finite state space or finite state sample. |
| `E` | Declared finite effect space or finite effect sample. |
| `<->` | Declared probability pairing. |
| `T` | Scoped terminal map used by the replay. |
| `Pi_sharp` | Scoped terminalization claim. No row silently mints authority. |

Each row checks:

1. normalization
2. positivity
3. no-signalling or marginal consistency where composition is declared
4. transport coherence
5. local-to-global terminal agreement
6. quotient non-promotion
7. finite replay.

Pairing Registry

**Terminal Status Definitions:**

* `failed` = declared obligations replay and fail
* `refused` = required declaration missing (e.g. composite rule undeclared)

| Row | Declared Carrier | Checks Actually Replayed | Checks Not Declared | Terminal Status | Scope Fence |
|---|---|---|---|---|---|
| `classical_simplex_dot_pairing` | Classical `R^2` simplex | Normalization, Positivity, Transport | Continuous reversibility | `passes_classical_packet` | Exact-rational classical gluing witness |
| `square_bit_effect_pairing` | Square-bit GPT | Single-system affine pairing | Composite tensor / marginal rule | `refused` | Single-system only |
| `spekkens_epistemic_pairing` | Spekkens toy bit | Overlap pairing, two-system table | Full composition theorem | `passes_scoped_spekkens_classical_packet` | Spekkens epistemic restriction only |
| `real_hilbert_trace_pairing` | Real Hilbert rebit | Local trace pairing | Composite local tomography ($9 \neq 10$) | `failed` | Local tomography boundary |
| `complex_hilbert_born_pairing` | Imported complex `M2` packet | Born trace pairing, POVMs, Hadamard transport | External sealed CODA-FDA `Pi_sharp` | `conditional imported complex born pairing local replay only` | Never selected, never sealed authority |
| `quaternionic_guarded_pairing` | Guarded quaternionic candidate | Single-system `D1 = 6` | Canonical composite rule | `refused` | Until composition contract |
| `nonlinear_ad_hoc_pairing` | Classical simplex negative control | Normalization, Positivity, Transport | Coherent gluing | `fails_pairing_audit_transport_and_normalization` | Deliberate nonlinear control fails normalization, positivity, transport, and coherent gluing |

Result Boundary

O024 establishes a registry-relative selector audit:

```text
declared pairing
-> finite normalization and positivity checks
-> declared transport replay
-> declared local/global agreement replay where admitted
-> typed terminal status
```

O024 does not establish:

1. that Born pairing is uniquely selected
2. that GTLA derives the Born rule
3. that complex Hilbert QM is selected over every undeclared carrier
4. that a local imported `M2` replay is a sealed CODA-FDA authority result
5. that a bounded agreement replay mechanizes GTOR-21 or GTTC-7
6. that every nonlinear pairing fails
7. that refusal of a quaternionic composite is a refutation of quaternionic QM.

Worked Example (hand-checkable non-selection witness)

A reader can replay the headline non-result by hand. Model a two-outcome
probability pairing as a weight pair $(w_0, w_1)$ and take the declared
compatibility slice to be normalization to a fixed total $2$ (over $\mathbb N$,
positivity is automatic):

$$\mathrm{Compatible}_2(w_0, w_1) \iff w_0 + w_1 = 2.$$

Then $(1,1)$ and $(2,0)$ are **both** compatible yet **distinct**:
$1+1 = 2 = 2+0$ and $(1,1) \neq (2,0)$. So the compatibility skeleton admits at
least two pairings and does not single out the designated Born-like uniform
pairing $(1,1)$. [WORKED EXAMPLE — hand-checkable instance of the non-selection
firewall; this is exactly what `QM.compatible_not_unique` / `QM.born_not_selected`
mechanize.]

Effect-relativity (the LT-Q half) is equally concrete: with operational pairing
$\langle E, \rho\rangle = \rho\cdot E$, a fixed state $\rho = 1$ gives
$\langle 1, 1\rangle = 1 \neq 2 = \langle 2, 1\rangle$, so no probability can be
assigned to the state independently of the effect. [WORKED EXAMPLE — instance of
`QM.no_probability_without_pairing`.]

**Finite Matrix Example:**
Consider a declared 3-state, 2-effect classical probability table.
States $S = \{s_1, s_2, s_3\}$, Effects $E = \{e_1, e_2\}$.
Let the pairing be given by matrix $M_{ij} = p(e_j | s_i)$:

$$
M = \begin{pmatrix} 1.0 & 0.0 \\ 0.5 & 0.5 \\ 0.0 & 1.0 \end{pmatrix}
$$
This passes positivity and normalization (rows sum to 1). If we permute the rows, or deform the middle row to $(0.4, 0.6)$, it *still* passes all finite compatibility checks. The compatibility skeleton (normalization + positivity) admits infinite continuous deformations of the table. It does not select a unique pairing matrix.

Effect-relativity is obvious here: the probability $p=0.5$ for $s_2$ only has meaning relative to an effect column; without declaring $e_1$ or $e_2$, state $s_2$ alone carries no absolute probability.

This worked example is illustrative of the firewall only; it is **not** a claim
about any registry row's full terminal status (those are graded by the seven
per-row checks above).

Lean Support

The registry-relative non-selection boundary is machine-checked in
`QM.PairingNonSelection`:

* `QM.compatible_not_unique`
* `QM.born_not_selected`
* `QM.probability_is_pairing_relative`
* `QM.no_probability_without_pairing`

These theorems prove only the finite firewall: the declared compatibility
skeleton does not uniquely select the designated Born-like pairing, and
probability is effect-relative rather than state-only. They do not derive Born,
Hilbert space, or physical quantum authority. [PROVEN — Lean-mechanized firewall;
the file is Mathlib-free (core `Nat`/`Prod`); LT-K (`compatible_not_unique`,
`born_not_selected`) is axiom-free, LT-Q's state-only firewall
(`no_probability_without_pairing`) inherits `propext`, `Quot.sound`.]

**Reproducibility pointer.** This firewall is secured in the encyclopedia as
**ENC-1070** — *Pairing Non-Selection: O024 ⊬ Unique Born (BORN-PAIR-001)*
(`quantum` layer, MECHANIZED; aliases `paper:qm092:BORN-PAIR-001`,
`paper:qm092:LT-K`, `paper:qm092:LT-Q`; view
`paper_qm030`), whose Notes
name "08" as a dependent paper. The authority firewall the whole audit rests on
($\mathsf{StructureDerived}\not\Rightarrow\mathsf{IsAuth}$) is **ENC-1063**
(Authority Non-Promotion, MECHANIZED). QM is a realization spine: QM_011 mints no
tower authority and secures under the shared `paper:qm092` namespace.

O025 Handoff (non-smuggling)

O024 prepares O025 but must not smuggle it. The CPTP/trace-norm transport audit is a separate downstream result: trace norm is not selected by CPTP monotonicity alone, and CPTP does not arise from noncommutativity alone. O024 establishes none of the CPTP trace-norm properties; it only establishes that pairings must be declared and audited, and compatibility alone does not select Born.

Next Results

1. `O025`: trace-norm / CPTP transport audit.
2. `O026`: minimal quantum-interface survival theorem.

Both remain downstream of the declared O024 pairing packet and the sealed-terminal obligations.

Related Work

This audit sits beside the operational-reconstruction literature but answers a
strictly narrower question — *terminal-compatibility per declared packet*, not
*forced selection*:

* **Axiomatic reconstructions of complex-Hilbert QM** — Hardy (2001);
  Chiribella–D'Ariano–Perinotti (2011); Masanes–Müller (2011). These *derive* the
  quantum probability rule by **assuming** informational axioms (local tomography,
  purification, continuous reversibility). O024 instead *grades* declared pairings
  against finite terminal checks and refuses any selection claim; it is the
  contrapositive bookkeeping of those theorems, not a competing reconstruction.
  (Cited identically by the sibling QM_081 §-related-work.)

* **Generalized Probabilistic Theories (GPT)** — Barnum–Barrett–Leifer–Wilce (2007)
  and the convex state/effect framework. The `square_bit_effect_pairing` row reuses
  the GPT state/effect/cone vocabulary as one audited carrier; O024 asks which
  pairings are terminal-compatible, not which GPT axioms force QM.

* **Spekkens toy model** (Spekkens 2007, epistemic-restriction toy theory) — the
  `spekkens_epistemic_pairing` row replays an elementary overlap pairing and a
  single two-system table; we claim no full composition theorem.

* **Quantum-logic / effect-algebra approaches** (Birkhoff–von Neumann 1936; the
  states-and-effects / effect-algebra framework) — supply the states/effects/pairing
  vocabulary this paper audits; O024 adds the finite terminal-gluing grading and
  the authority firewall.

* **Gleason-type theorems** — Gleason (1957) *derives* the Born trace rule from the
  measures on the lattice of projections (dimension $\ge 3$). O024 deliberately does
  **not** invoke a Gleason-style derivation: the Born trace pairing enters as an
  *imported* registry row, and the audit's headline non-result is precisely that the
  declared finite compatibility skeleton (without Gleason's structural hypotheses)
  does not uniquely select it.

* **In-corpus neighbors:** QM_081 (what GTLA must import to recover QM — Born-import
  framing), QM_081/QM_006 (descent / tower-walk survival audits), QM_001 (the
  cofiber→Banach scalar bridge O022a), and the projection-obstruction quotient
  papers QM_100/qm_100_projection_obstruction_technical_appendix.

Falsifiability

This audit fails if a *declared* finite compatibility skeleton (positivity,
normalization, transport, gluing — without additional imported axioms) is exhibited
that admits the designated Born pairing as its **unique** compatible pairing; that
would refute the LT-K non-selection firewall (`compatible_not_unique` /
`born_not_selected`). It also fails if any registry row's typed terminal status is
shown to disagree with a faithful re-run of the seven per-row checks on its declared
carrier.

Notation pointer

$S$ / $E$ — declared finite state / effect spaces; $\langle\cdot,\cdot\rangle$
(written `<->` in the packet schema) — the declared probability pairing; $T$ — the
scoped terminal map; $\Pi_\sharp$ — the scoped terminalization claim (no row mints
authority). $\Phi_1$, $Q^1=C^1/B^1$, $\mathsf{StructureDerived}$, $\mathsf{IsAuth}$,
CODA-FOC / CODA-OR / CODA-CS / CODA-FDA, and the terminal-status type system are the canonical
Omega-tower objects; see the encyclopedia (`by_layer`,
`indexes/ledgers/`) and the QM-series companions QM_081/QM_081/QM_006/QM_001 for
definitions on first use.

What This Does NOT Claim

```text
O024 does NOT:

* derive the Born rule from the compatibility skeleton;
* uniquely select complex Hilbert QM over any other declared or undeclared carrier;
* treat a local imported M2 replay as a sealed CODA-FDA authority result;
* mechanize GTOR-21 or GTTC-7 via a bounded agreement replay;
* assert that every nonlinear pairing fails (only the declared control does);
* refute quaternionic QM (it refuses a composite until a composition contract);
* mint any tower authority (StructureDerived ⇏ IsAuth; firewall ENC-1063).
```

[SCOPE FENCE — this box is the fence that protects the registry-relative audit.]

Changelog

Version Note: v1.0-audit (2026-06-21):** First pipeline pass.
  Part-A rubric elements that were missing — lead sentence, "why a researcher
  should care", a hand-checkable worked-example non-selection witness (the
  $(1,1)$ vs $(2,0)$ compatible-but-distinct pairings mechanized by
  `compatible_not_unique`), a Related-Work section (GPT / Hardy / CDP, Spekkens,
  quantum logic / effect algebras, Gleason, in-corpus QM neighbors), an explicit
  Falsifiability line, a Notation pointer, and a "What this does not claim" box.
  Claim-typed the O024 target, non-claim, Lean Support, and worked example.
  Added the reproducibility pointer to ENC-1070 / ENC-1063 and recorded the Lean
  axiom profile. Companion `qm_011_state_effect_pairing_audit Claim Ledger`
  created. No mathematical content, scope, or status changed; no hedge softened.
  Related-Work citations aligned to the corpus-verified forms carried by the
  sibling QM_081 (Hardy 2001; Chiribella–D'Ariano–Perinotti 2011; Masanes–Müller
  2011; Barnum–Barrett–Leifer–Wilce 2007; Spekkens 2007; Birkhoff–von Neumann 1936;
  Gleason 1957).

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-011-C1` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C2` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C3` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C4` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C5` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C6` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C7` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C8` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C9` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C10` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C11` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C12` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C13` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C14` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C15` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `QM-011-C5..C11` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `ENC` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `ENC-1070` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |
| `ENC-1063` | [`claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) |

<!-- claim-id-body-index:end -->
