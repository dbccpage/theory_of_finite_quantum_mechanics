# QM_091 — Formal Possibility Is Not Physical Terminalization: The Shared Promotion Error in Deutsch, Everett-DeWitt, and Wolfram

## GTOC Foundations — Quantum Contact Series (qm_091_deutsch_everett_wolfram_promotion_error)

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

document_id: "QM_091"
version: "v1.0.0 (Mechanized Authority Non-Promotion Firewall)"
status: "READY_FOR_AUTHOR_REVIEW"
authority_effect: "None"
mechanization: "MECHANIZED (ENC-1063: lean4/007_authority_firewall/001_the_authority_firewall_a_machine_checked_separation_of_evidence_from_authority_in_finite_systems/OmegaCosmology/Primitives/AuthorityNonPromotion.lean, lean4/shared_kernel/primitive_difference.lean; authorityNonPromotionPrimitiveDifference, authority_non_promotion_nonzero_of_unsealed)"
claim_ledger: "qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md"
change_log: "qm_091_deutsch_everett_wolfram_promotion_error_change_log.md"

QM_091 — Formal Possibility Is Not Physical Terminalization
===========================================================

The shared promotion error in certain readings of Deutsch, Everett-DeWitt, and Wolfram

```text
Result type: type separation (one [PROVEN] firewall) + three scoped [INTERPRETIVE] corollaries
Authority:  none minted. CODA-FDA Pi_sharp checks terminal policy with AuthorityEffect None; it is not an authority arrow.
Lean: bare `StructureDerived ⇏ IsAuth` MECHANIZED in `QM.PossibilityBoundaries`; full LT-A factorization (only-via-Π♯) still OPEN
Supersedes nothing; consolidates 02_ Section 1 + qm_090_interpretations_as_authority_shadows
Companion:   qm_091_deutsch_everett_wolfram_promotion_error Claim Ledger
```

> **Current status-domain fence (2026-07-20).** Historical occurrences below of `AuthorityTerminal`, `T_auth`, `SealedAuthority`, and “only via Pi_sharp” are local theorem-model vocabulary, not the current `GtocTerminal` domain. Pi_sharp emits non-authoritative checked evidence. No model-facing diagnostic or terminal constructs `AuthorityStatus`; any bounded promotion is a separate external authenticated human decision. The retained result is the nonconstruction theorem, not an authority-constructor recipe.

> **Core doctrine.** GTLA is not an origin theory. Its model-facing finite-descent layer checks evidence and terminal policy; it does not mint authority. This paper does not claim physical-QC impossibility,
> full-stop Deutsch rejection, Everett rejection, or Wolfram rejection. It
> isolates one promotion error that three otherwise-different
> programs commit, and states it as a typed non-implication.

$$
\boxed{\ \mathsf{StructureDerived}(F,c)\ \not\Longrightarrow\ \mathsf{IsAuth}(t) }
$$

$$
\boxed{\ \text{formal coherence} \not\Rightarrow \text{world authority} }
$$


Abstract

**A mathematically coherent model does not, by that coherence alone, mint
physical or ontological authority.** This paper isolates one inference — call it
the *promotion error* — that certain strong readings or public uses of these programs commit: treating a
**derived or formally-coherent structure** as if it thereby established
**world authority** (scalable physical computation, an ontology of worlds, or
explanatory closure over physics). We state the error as a single typed
non-implication, $\mathsf{StructureDerived}(F,c)\not\Rightarrow\mathsf{IsAuth}(t)$,
and apply it as three *scoped, individually-defeasible* boundary claims against
Deutsch's Church–Turing–Deutsch reading, the Everett–DeWitt branch-ontology
reading, and Wolfram's rule-generativity reading. We do **not** claim any of these
programs is refuted; each defeats the critique by supplying the finite-descent
*realization packet* the promotion would require (Section 6). The load-bearing
content is the firewall (the absence of a packet-free authority constructor); the
three applications are argued readings, not theorems.

### Why a researcher should care

Across the foundations of physics, quantum-computing roadmaps, and computational
metaphysics, the same step recurs: "the formal model is consistent / the principle
holds / the rule is generative, **therefore** the corresponding physical or
ontological claim is established." If that step is illicit, then a large class of
strong claims is *unterminated* — not false, but not yet licensed by their stated
evidence. Naming the step precisely (and stating exactly what evidence would
license it) lets a reader audit any such argument with a single check: *was a
realization packet supplied, or was authority assumed?* The contribution is an
auditing instrument, not a metaphysical verdict.

### One-paragraph recap (self-contained)

The framework behind this paper is not an origin theory of physics. Its model-facing finite-descent layer checks a declared `PhysicalRealizationPacket` and emits evidence plus terminal-policy results through `Π♯`, all with `AuthorityEffect::None`. The single current fact this paper uses is that there is no constructor from a bare `FormalModel`, packet, diagnostic, or terminal into `AuthorityStatus`; any bounded promotion is external and human.
Readers need no prior paper: the firewall is restated in Section 1 and the only
cross-references are to where it is mechanized.


0. Claim discipline (read first)


| Tier | Claim | Status |
|---|---|---|
| 1a | Bare non-implication: `StructureDerived ⇏ IsAuth` (structure-derivation does not by itself mint authority). | **[PROVEN, MECHANIZED — axiom-free]** (`QM.PossibilityBoundaries`: `structure_not_auth`, `not_structureDerived_implies_isAuth`). |
| 1b | Historical stronger claim: authority factors *only* through `Pi_sharp`. | **[SUPERSEDED / DECODE-ONLY]** Current semantics make `Pi_sharp` non-authoritative and place promotion at a separate external human boundary. |
| 2 | Deutsch (CTD), Everett-DeWitt branching, and Wolfram generativity each *lack* the terminalization their authority/ontology claims would require. | **Conditional / scoped** (per-program, below). |
| 3 | No physical/world-authoritative system in the relevant class can ever supply that terminalization. | **NOT claimed.** Each program can defeat the critique by supplying the packet. |

This paper is Tier-1 + Tier-2 only. It is an **audit of authority promotion**, not
a refutation of quantum computation, of the unitary formalism, or of computational
models of physics.

**Preferred language used throughout:** *formal possibility is not physical
terminalization; possible-task language is not a repair-capacity certificate
branch representation is not ontology terminalization; rule generativity is not
world authority; no packet, no authority; a missing packet means unterminated
under this evidence standard.*


1. The promotion error, abstractly


Fix three distinct types:

```text
FormalModel              -- an internally consistent mathematical object
PhysicalRealizationPacket -- declared finite descent data (carrier, defects,
                            repair, quotient, bounds, terminalizer)
AuthorityTerminal        -- historical local proof-model type; not GtocTerminal and not produced by current Pi_sharp
```

The promotion error is the assumption of a constructor

$$
\mathsf{promote}:\ \mathsf{FormalModel}\ \longrightarrow\ \mathsf{AuthorityTerminal}
$$

that does **not** factor through `PhysicalRealizationPacket` and its terminalizer
`Pi_sharp`. GTLA's firewall has **two parts**, tagged honestly (split after a
2026-06-18 claim-verification triage found the prior single `[PROVEN, MECHANIZED]`
tag overstated):

* **(a) the bare non-implication `StructureDerived ⇏ IsAuth` is [PROVEN,
  MECHANIZED — axiom-free]**: a genuine countermodel in
  `QM.PossibilityBoundaries` (`structure_not_auth`,
  `not_structureDerived_implies_isAuth`) — an inhabitant that is structure-derived
  yet not authority, so structure-derivation does not by itself mint authority.

* **(b) the historical STRONGER only-via-`Pi_sharp` claim is [SUPERSEDED / DECODE-ONLY]**. The vacuously gated `OmegaCosmology.Primitives.AuthorityNonPromotion.no_formal_to_authority_when_no_terminalizer` lemma does not establish an authority factorization. Current semantics instead prohibit every model-facing diagnostic or terminal from constructing authority and reserve any bounded promotion for a separate external authenticated human decision.

The boxed factorization below is retained as the superseded historical prose target; only part (a) is machine-checked and current:

$$
\boxed{
\nexists\,\mathsf{promote}quad
\text{Authority factors only as }
\mathsf{FormalModel}\xrightarrow{\text{declare}}\mathsf{Packet}\xrightarrow{\ \Pi^\sharp\ }\mathsf{AuthorityTerminal}.
}
$$

**Lean target LT-A.** `StructureDerived ⊬ IsAuth` is now **DONE** (mechanized,
axiom-free, in `QM.PossibilityBoundaries`). The remaining typed
non-implications `ValidTransport t ⊬ Authority`, `LocalReplay p ⊬ SealedAuthority p`,
`ScopedTerminal ≠ ExactAuthority`, and the *only-via-`Pi_sharp`* factorization
remain the OPEN part of LT-A. (See `TARGETS` LT-A; foundation kernel
`GTLA_T49_T52_O023_kernel`.) **Note:** the prior
`AuthorityNonPromotion` non-promotion lemma is *vacuously hypothesis-gated*
(assumes the never-true `TerminalizerEvidence → False`) and must not be cited as
the mechanization of the firewall.

This is the same error catalogued, in physical-QC form, in `02_` Section 1:

| Program | The structure it has | The terminalization it promotes to without a packet |
|---|---|---|
| Deutsch / CTD | a formally possible task in the quantum circuit model | scalable *physical* computation |
| Everett-DeWitt | a unitary mathematical branch structure | physical *ontology* of worlds |
| Wolfram | a generative rule producing rich patterns | *world*-explanatory authority |

Each row is `formal coherence ⊬ world authority`. [^1]

[^1]: A similar gap appears in modal "God-proofs," which promote logical/modal consistency of a construction to existential authority. The differences between the
programs are real; the shared gap is the missing terminalizing packet.

### 1.1 Notation pointer

`StructureDerived(F,c)` — predicate: structure $F$ is derived/coherent under
constraints $c$. `IsAuth(t)` — predicate: $t$ inhabits the authority terminal.
`Π♯` (`Pi_sharp`) — the non-authoritative CODA-FDA terminal-policy checker. Its historical local-model reading as the only map into `T_auth` is decode-only and superseded.
`Φ₁` — the finite obstruction functional. The packet fields (`C0, C1, d0, B1,
λ_proj, μ_repair, ε_mix, p_pair, …`) are defined in `qm_103_show_the_packet_protocol` (the packet schema)
and used here only by name. No symbol in this paper is introduced as new
mathematics; the firewall predicate and `Π♯` are the QM-series primitives.

### 1.2 Related work and fair attribution

This is a critique paper, so its first obligation is to represent each target
program **fairly**. We position against the actual stated positions, not strawmen:

* **Deutsch / Church–Turing–Deutsch principle** — Deutsch's claim is that every
  finitely realizable physical process can be simulated by a universal (quantum)
  computer; the principle is a statement about *physical universality*, not a
  guarantee that a *scalable* device exists at human-significant scale.
  We dispute neither the principle nor the existence of abstract quantum
  computation. Primary source: D. Deutsch, *Quantum theory, the Church–Turing
  principle and the universal quantum computer*, Proc. R. Soc. Lond. A **400**
  (1985) 97–117. Fault-tolerance / threshold results (the genuine conditional
  repair theorems we credit): P. Shor, *Fault-tolerant quantum computation*,
  FOCS 1996; D. Aharonov & M. Ben-Or, *Fault-tolerant quantum computation with
  constant error*, STOC 1997; A. Kitaev, *Quantum computations: algorithms and
  error correction*, Russ. Math. Surv. **52** (1997) 1191–1249.

* **Everett relative-state / DeWitt many-worlds** — Everett's formulation gives a
  *relative-state* (universal-unitary, no-collapse) account; DeWitt's later
  exposition foregrounds the "many worlds" reading. We treat the *unitary
  formalism* as a coherent formal story and dispute only the step from a branch
  *representation* to a branch *ontology* with authority. Primary sources:
  H. Everett III, *"Relative State" formulation of quantum mechanics*,
  Rev. Mod. Phys. **29** (1957) 454–462; B. DeWitt & N. Graham (eds.),
  *The Many-Worlds Interpretation of Quantum Mechanics*, Princeton Univ. Press,
  1973.

* **Wolfram computational / ruliad program** — the claim that simple generative
  rules can produce the richness of physical phenomena. We dispute neither the
  generativity nor the internal mathematics of the rule systems; only the step
  from *rich generation* to *world-explanatory authority*. Primary source:
  S. Wolfram, *A New Kind of Science*, Wolfram Media, 2002; and the Wolfram
  Physics Project (announced 2020).

* **Nearest methodological neighbors** — the type-separation here is in the
  spirit of (i) sheaf-theoretic contextuality, which separates local consistency
  from global sections (S. Abramsky & A. Brandenburger, *The sheaf-theoretic
  structure of non-locality and contextuality*, New J. Phys. **13** (2011)
  113036); (ii) obstruction
  theory proper, where a locally-defined structure carries a cohomological
  obstruction to global extension; and (iii) the **internal** QM-series authority
  firewall `qm_090_interpretations_as_authority_shadows` (the
  interpretation-as-shadow rule) and `QM_007_Finite Weighted Transport Calculus
  for QM` (T7, the no-authority theorem). The boundary papers
  `QM_082`/`QM_111`/`QM_060` (the Deutsch/Everett/Wolfram boundaries treated
  individually) and `QM_092` overlap this paper's themes and are
  cross-referenced, not subsumed.

How this paper differs from each: it does **not** argue any program is wrong on
its own terms; it argues that a *specific cross-program inference* (structure ⇒
authority) is unlicensed, and gives the exact evidence (a packet) that would
license it. A critique that misattributed any of the three positions above would
itself fail the truth standard; the primary sources above are the canonical
statements of each program, cited so the attribution can be checked directly.

### 1.3 Worked instance of the type separation

The promotion error is concrete, not just schematic. Take the smallest
CODA-FOC carrier on which a formal structure exists but no packet is declared.

> **Instance.** Let the cochain data be $C^0=\mathbb R$, $C^1=\mathbb R^2$, with
> coboundary $d_0(\alpha)=(\alpha,-\alpha)$ and weights $\omega=(1,1)$. A `FormalModel` here is the
> linear-algebraic object $(C^0,C^1,d_0)$ itself: it is internally consistent and
> "derived" in the sense that every entry is fixed by the data. The obstruction
> functional evaluates to a finite number — e.g. on the residual $x=(0,1)$ one
> computes $\Phi_1$ by the declared finite rule — and that number is a *property
> of the structure*. **No field of a `PhysicalRealizationPacket`**
> (`λ_proj, μ_repair, ε_mix, p_pair, Π♯, terminal_status`) is determined by
> $(C^0,C^1,d_0,\omega)$ alone: the structure fixes the diagnostic, the packet
> fixes the authority, and the map from the first to the second is exactly what is
> *not* supplied. Reading $\Phi_1$ off the structure and then asserting
> $\mathsf{IsAuth}(t)$ is the promotion error in miniature.

This instance is hand-checkable and replays the type-separation kernel cited in
Section 1 (the Lean target LT-A treats `StructureDerived`, `ValidTransport`,
`LocalReplay`, `ScopedTerminal` as inhabiting types disjoint from the authority
terminal). It is deliberately small: the point is the *absence of a constructor*,
which a two-dimensional example exhibits as well as any large one.


2. The Deutsch boundary (scoped)


**Scoped claim [INTERPRETIVE / scoped reading — argued, not a theorem; the
underlying type separation is the [PROVEN] firewall of §1].** The
Church-Turing-Deutsch principle is a high-level physical principle; it does
**not** by itself supply the repair-capacity packet a scalable *physical*
quantum-computing claim requires:

```text
C0, C1, d0, B1, Q1, Phi, omega_t, lambda_proj, mu_repair, epsilon_mix,
L*, p_pair, Pi_sharp, terminal_status
```

A possible task is not yet a terminalized physical computation
(`appendix_B` Section 9; `02_` Section 1). Deutsch is **right** that quantum
computation is formally possible in the quantum model; that admissibility is not
physical authority.

$$
\boxed{\text{possible-task language is not a repair-capacity certificate.}}
$$

**Status:** Conditional / scoped. **Not claimed:** physical-QC impossibility or a
full-stop rejection of Deutsch. The conditional physical no-go (PO-QC-T4)
is itself conditional and its antecedent is the open Tier-3 burden.

**What defeats this critique:** a realization functor extending CTD that emits a
*complete* repair-capacity packet (all fields above, with bounded `lambda<=mu`,
`p_pair->0` at human-significant workload, acceptable overhead, replayable
`Pi_sharp`). Then the critique must target the *packet*, not the principle.
(See `QM_Series_Falsifiability_Ledger` Section F.)


3. The Everett-DeWitt authority shadow (scoped)


**Scoped claim [INTERPRETIVE / scoped reading — argued, not a theorem; the
underlying type separation is the [PROVEN] firewall of §1].** A unitary branch
representation does not construct ontology or authority without a
branch-observable packet and terminal evidence:

$$
\mathsf{BranchRepresentation}\ \not\Longrightarrow\ \mathsf{OntologyTerminal}\ \vee\ \mathsf{AuthorityTerminal}.
$$

Universal unitary evolution with branch-relative description is a coherent formal
story. Naming or emphasizing branches (DeWitt) adds no packet-distinguishable
content. Per `qm_090_interpretations_as_authority_shadows`, an interpretation is
treated as incorrect *only* when it makes a packet-distinguishable false claim
absent that, branch ontology is an upper-layer representation shadow.

$$
\boxed{\text{branch representation is not ontology terminalization.}}
$$

**Status:** upper-layer shadow / Open. **Not claimed:** that Everett is false, or
that the unitary formalism is wrong.

**What defeats this critique:** make branch ontology *packet-distinguishable*
(supply observables and a terminal difference) and terminalize it without surplus
unobservable structure. Then it leaves the shadow class.


4. The Wolfram generativity boundary (scoped)


**Scope guard (read first).** The master index Red-team list (Section 10, item 11)
marks ruliad / computational-generativity claims as **out of scope** for the QM
index. This section is admissible **only** as the strictly-scoped non-implication
below — never as "Wolfram refuted," and never as a claim about the ruliad's
internal mathematics.

**Scoped claim [INTERPRETIVE / scoped reading — argued, not a theorem; the
underlying type separation is the [PROVEN] firewall of §1].** Rule generativity
does not imply world authority or explanatory closure without finite-descent
terminalization:

$$
\mathsf{RuleGeneratesPatterns}\ \not\Longrightarrow\ \mathsf{WorldAuthority}.
$$

A rule that generates rich patterns is a `FormalModel`. World-explanatory
authority is an `AuthorityTerminal`. The constructor between them does not exist
without a finite-descent terminalizer that *selects* world-authoritative claims
and *rejects* non-world rules.

$$
\boxed{\text{rule generativity is not world authority.}}
$$

**Status:** Heuristic / Open. **Not claimed:** that Wolfram is refuted, or that
computational models of physics are impossible.

**What defeats this critique:** pair rule generativity with finite-descent
terminalizers that select world-authoritative claims and reject non-world rules.


5. Defeat Packet Checklists


Each program can immediately defeat the critique by supplying the required finite-descent packet.

### The Deutsch/CTD Defeat Packet

* [ ] Explicit architecture-scale fields $\lambda, \mu, p_{\mathrm{pair}}$ defined for the physical hardware.
* [ ] Bounded repair cost $\lambda \le \mu$ under realistic noise profiles.
* [ ] $p_{\mathrm{pair}} \to 0$ validated at human-significant workload scales.
* [ ] A sealed $\Pi^\sharp$ terminalizer validating the physical repair capacity.

### The Everett-DeWitt Defeat Packet

* [ ] A packet-distinguishable ontology terminal.
* [ ] Observable finite-descent markers for branch differentiation.
* [ ] No unobservable surplus structure required for terminalization.

### The Wolfram Defeat Packet

* [ ] A finite-descent terminalizer that explicitly *selects* world-authoritative claims.
* [ ] An explicit rejection mechanism for internally consistent non-world rules.

6. What each program *does* supply (fairness ledger)


Building the cathedral well means crediting what each program has.

| Program | Genuinely supplies | Missing for authority/ontology |
|---|---|---|
| Deutsch / CTD | a precise universality principle; abstract QC exists; threshold theorems are real conditional repair-capacity theorems | architecture-scale `lambda`, `mu`, `p_pair`, and a sealed `Pi_sharp` at human-significant scale |
| Everett-DeWitt | a parsimonious unitary account with no collapse postulate | a packet-distinguishable ontology terminal with no unobservable surplus |
| Wolfram | a generative substrate with demonstrable pattern richness | a finite-descent terminalizer selecting world-authority and rejecting non-world rules |

Threshold theorems, specifically, are **read as repair-capacity certificates under
declared hypotheses** (not denied) — see `02_` Section 3, `03_` Section 10.


7. What would falsify, weaken, or redirect this claim?


**Falsifiability (one line).** This paper fails if anyone exhibits an inhabitant
of `AuthorityTerminal` constructed from a `FormalModel` alone — with no declared
`PhysicalRealizationPacket` and no `Π♯` replay — which would refute the core
firewall and, with it, the whole series.

* **Tier-1 (LT-A):** produce an inhabitant of `AuthorityTerminal` from a
  `FormalModel` alone, with no packet and no `Pi_sharp`. That refutes the core
  doctrine of the entire series, not just this paper.

* **Deutsch:** a CTD-extending realization functor emitting a complete
  repair-capacity packet at scale (Section 2).

* **Everett:** a packet-distinguishable branch ontology terminalizing without
  surplus unobservable structure (Section 3).

* **Wolfram:** rule generativity paired with finite-descent terminalizers
  selecting world-authority (Section 4).

A *missing* packet does not prove impossibility; it means the claim is
**unterminated under this evidence standard**.


8. Strict non-claims


>[!WARNING]
> **[OBLIGATION]** Verify the exact source quotations before public release, especially the Deutsch resource-count language in Appendix A.

This paper does **not** claim, and no sentence here should be quoted as:

1. "quantum computing is impossible"
2. "Deutsch is wrong" (full stop)
3. "Everett is refuted"
4. "Wolfram is refuted"
5. "the unitary formalism / circuit model is inconsistent"
6. "experiment is fake" or "the threshold theorem is refuted"
7. that GTLA derives QM, Born, or any physical no-go.

Each program is challenged **only** on the scoped non-implication
`formal coherence ⊬ world authority`, and each can defeat the challenge by
supplying the terminalizing packet named in Section 6.


9. Cross-references


* `TARGETS` — LT-A (authority non-promotion), the Lean target for Section 1.
* `qm_100_projection_obstruction_public_paper` Section 1 — the
  Deutsch-boundary framing and the four-row promotion-error table.

* `qm_090_interpretations_as_authority_shadows` — interpretation-as-shadow rule.
* `qm_110_finite_weighted_transport_calculus_for_qm` T7 — the no-authority theorem.
* `QM_Series_Falsifiability_Ledger` Section F — the per-thesis falsifiers.
* `QM_000_QM GTLA Master Index` Section 10 Red-11 — ruliad/computation out-of-scope guard.
* `QM_082` / `QM_111` / `QM_060` — the individual Deutsch / Everett / Wolfram
  boundary papers (overlapping themes; cross-referenced, not subsumed).

* `QM_092` — adjacent projection-obstruction treatment (overlapping themes).



Appendix A: The finiteness contradiction (the sharper attack on the *marketing*)

The promotion above is the *general* boundary. There is a *sharper, internal*
result aimed only at the most-marketed popular argument for the quantum-
computational multiverse — and it uses Deutsch's **own** foundational axiom against
it. (Full claim-by-claim sweep: `2026-06-18_deutsch_1985_sweep_and_attack`.)

* **D1 (Deutsch 1985, p. 99).** The Church–Turing–Deutsch principle: *"Every
  finitely realizable physical system can be perfectly simulated by a universal
  model computing machine operating by finite means."*

* **D5 (Deutsch, *The Fabric of Reality*, 1997, ch. 9).** The resource-count
  argument: Shor's factorisation uses *"10^500 or so times the computational
  resources that can be seen to be present,"* against *"only about 10^80 atoms in
  the entire visible universe,"* so the computation must run in parallel universes.

**Claim [PROVEN — textual/logical, conditional].** Read literally (as a count of
*physical computational substrates*), D5 contradicts D1: a process requiring 10^500
substrates *not present* is, by construction, **not finitely realizable by the means
present** — exactly what D1 forbids. So `D1 ∧ D5(literal) ⊢ ⊥`. The repair is a
forced **dilemma**: either (i) read D5 literally and **abandon CTD finiteness** (the
foundation of the field), or (ii) read D5 as **rhetoric** — the `10^500` is the
*dimension of the representation* (Hilbert space), not a population of substrates —
in which case it carries **no evidential force**, because the work is done by
*interference on one finite device* (see QM_061: interference is a finite `H^1`
holonomy, not L1-computable). Either horn removes the multiverse-as-explanation
conclusion.

$$
\boxed{\ \text{finite realizability (D1)}\ \wedge\ \text{10}^{500}\text{ substrates (D5, literal)}\ \vdash\ \bot.\ }
$$

The reification "representation dimension ⇒ physical substrate count" is the *same*
`StructureDerived ⇏ IsAuth` error as §1/§3 (the `10^500` is the size of the chart,
not the territory).

**Scope [INTERPRETIVE], explicit.** This attacks an **argument** and its **public
marketing**, *not* the many-worlds interpretation. The strongest modern Everettians
already rest the case elsewhere (decoherence + parsimony, not resource-counting), so
the dilemma's horn (ii) is the one they take — which *is* the honest-marketing point:
the case sold to the public is not the case the experts defend. Underdetermination is
applied **symmetrically** here — no surplus-ontology (many-worlds, collapse, or
pilot-wave) is *certified* by the finite packet; parsimony may rationally favour one
but is a methodological virtue, **not** a packet-distinguishable terminal. The
companion interference result is interpretation-**neutral** (an Everettian may read
the `H^1` holonomy as branch interference). **Not claimed:** that many-worlds is
false, or that the unitary formalism is wrong.

Changelog

Version Note: v1.0-audit (2026-06-21)** — Series-wide hygiene pass.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-091-C1a` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C1b` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C2` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C3` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C4` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C5` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C6` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C7` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C8` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C9` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C10` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C11` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C12` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C13` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C14` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C15` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C16` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |
| `QM-091-C1` | sibling `qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md` |

<!-- claim-id-body-index:end -->
