# 072 Bit Shadow And Qubit

## GTOC Foundations — Quantum Contact Series (qm_072_bit_shadow_and_qubit)

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

Paper 7 — The Bit-Shadow and the Qubit
======================================

GTOC Foundations — Physics-Contact Extension. The Two-Locus One-Edge Carrier, the Three Minimality Splits, Exchange on a Pair of Bit-Shadows, and the Itemized Bit→Qubit Import Price List

**Date:** 2026-07-17 · **Version:** v1.0 · **Series:** GTOC Foundations, Physics-Contact Extension
**Claim ledger:** [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (IDs `072:P7-C1` through `072:P7-C10`)
**Degree:** δ7 (consumes δ0–δ6; cites δ3)
**Requires:** Paper 0 (δ0: minimal carriers, $Q^1$ relational, the triangle §7.6, exhibition-relative residuality §7.5), Paper 2 (δ2: weights; the repaired R1/R2a/R2b pricing of §6), Paper 3 (δ3: the Two Scalar Symmetric-Exchange Characters Theorem, K9-conditional), Paper 6 (δ6: the 𝔻 bit-shadow, channels, capacity).
**Main claim:** the goal prompt's target identity — "$\mathbb{D}$-as-carrier **=** the obstruction-qubit" — is **corrected, not executed**: what the two-locus one-edge carrier supports is the **bit-shadow** (the external review's ruling — "the $\mathbb{D}$ object is bit-like, not qubit-like" — is adopted and *derived*, not merely deferred to). Three theorem-grade findings replace the identity. **(1) The minimality split:** "smallest carrier with $\Phi_1 > 0$" is ambiguous three ways, and the three answers differ — the single cut carries *difference* (δ0, trivially); the two-locus one-edge carrier carries **repair-family-relative** residual only (over an assignment family full for the cut, every pattern on it is removable — this one-edge tree has no parity obstruction — so its $\Phi_1 > 0$ is Adm-relative, the Paper 000b $Q^1_O$ situation); the **odd triangle** (Paper 0 §7.6) is the least such carrier — least-ness forward-logged, PL-GTOC-7(c) — with a parity-**forced** non-removable pattern. The goal prompt's minimality claim holds only in the second, declared-relative sense, and the correction is recorded. **(2) The exchange dichotomy on a pair:** two K9-saturated indistinguishable bit-shadows already carry exactly two coherent scalar exchange characters (Paper 3 §4.4 at $|W| = 2$) — the transport-level Bose/Fermi split needs no quantum import. **(3) The bit→qubit price list:** four itemized imports separate the bit-shadow from the qubit — the phase fiber (QM_060/ENC-1129; with the finite-phase sub-door R2a-cheap and full $U(1)$ continuity-priced per QM_062), the interference/ℓ² readout (mechanized boundary ENC-1135), contextual multi-window structure (whose parity core is already finite — QM_120 — but whose operator provenance is imported), and continuous reversible dynamics (QM_062's named residual import). Superposition is obstructed at every derived degree as the R1 added fiber, exactly priced.
**Non-claim:** no qubit is derived; no Hilbert space, no $\mathbb{C}^2$, no Bloch sphere, no Born pairing, no measurement postulate, no complementarity theorem; no claim that the bit-shadow *is* a physical two-level system. Registered in §5.
**Authority:** none.
**State note (binding).** Authored against the post-2026-07-14-verdict, post-2026-07-15-review state of Papers 0–6 (all conditionalities inherited row by row; the R2a/R2b split of Paper 2 §6.2 is load-bearing throughout §4).

**Retention inheritance note.** The bit-shadow requires a retained two-locus one-edge carrier. A fleeting local sameness failure is not a bit-shadow and cannot be upgraded to a qubit by naming: without retained loci, edge, repair family, and weight slot, there is no $\mathbb{D}$ alphabet object for this paper to price.

Abstract

This paper proves that the minimal two-locus carrier is a bit-shadow rather than a qubit and separates three different minimality questions that earlier drafts conflated. It then prices the phase, interference, operator-window, state-space, Born-pairing, and continuous-dynamics imports needed for a qubit, leaving superposition and physical two-level realization obstructed at the derived finite grade.


§1 — The problem, stated exactly, and the correction announced

The goal prompt (Paper 7 brief) asks this paper to *show* that $\mathbb{D}$-as-carrier is "the obstruction-qubit," the minimal carrier with $\Phi_1 > 0$, on which the exchange dichotomy acts. The external review (2026-07-15) rules the opposite placement: the $\mathbb{D}$ object is **bit-like**; qubit-hood requires "$\mathbb{C}^2$ or equivalent state-space reconstruction, phase, effects, reversible dynamics, and Born pairing" and belongs to quantum realization. The series' construction rule (charter) settles how to proceed: *prove or obstruct* — and here the honest outcome is a **correction with derivations**: the brief's identity fails for stated, checkable reasons (§2's minimality split; §4's four priced imports), while everything in the brief that is derivable is derived (§2's diagnostic, §3's exchange action, §4's prices, §5's obstructions). The name "obstruction-qubit" is **[REFUSED]** for the minimal carrier; the derived object is the **bit-shadow** (Paper 6 §5), and the qubit is located at the end of an itemized price list, not at the ground.

### Import Ledger — §1

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| bit-shadow (𝔻-alphabet channel) | δ6 | Paper 6 §5 | K1-relative — flagged |
| "obstruction-qubit" (name) | — | — | REFUSED for the two-locus one-edge carrier (§1; grounds in §2, §4) |
| qubit | — | — | not derived; located by the §4 price list |

Connective audit: clean.

### Genesis-Bias Fence — No Prior Quantum State-Space

This paper does not begin with a qubit, state-space, Hilbert space, amplitude, phase, superposition, Bloch sphere, measurement basis, operator algebra, or physical two-level system. It begins with an exhibited two-locus one-edge carrier and the $\mathbb{D}$-valued pattern alphabet it supports.

The **bit-shadow** is not a foundational bit and not a qubit. It is the K1-relative two-pattern comparison alphabet inherited from the ground. Its binary form is priced by the exhaustive bivalence ruling.

The one-edge carrier is not intrinsically obstructed. Over an assignment family full for the cut, every one-edge pattern is removable. Any non-removability on that carrier is Adm-relative: it diagnoses a declared or exhibited repair family that omits a separating assignment.

The **qubit** is not hidden inside the bit-shadow. It is a later interface obtained only after additional imports are paid: phase fiber, interference / $\ell^2$ readout, contextual operator-window structure, continuous reversible dynamics, and a $\mathbb{C}^2$ / Born interface declaration.

Superposition is not an unexpressed state already present in the bit-shadow. It is an added fiber structure over exhibited labels: a superposition law, phase, involution, sesquilinear pairing, and quadratic readout. None is fixed by the derived count or weight data.

> **GENESIS-BIAS AUDIT.** Does this section explain the qubit by presupposing a prior quantum state-space, amplitude domain, phase continuum, operator algebra, measurement basis, physical two-level system, Bloch sphere, or hidden Hilbert geometry? If so, declare and price that antecedent, replace it with bit-shadow / repair-family / import-ledger data, or stop with an OBSTRUCTION.


§2 — The two-locus one-edge carrier, and the three-way minimality split

**2.1 The carrier.** Exhibit $V = \{a, b\}$, $E = \{\partial\{a,b\}\}$, $T = \varnothing$ ("two loci, one cut": K4 case-listing names). $C^1$-patterns assign the single cut an outcome: the pattern family is a token of $\mathbb{D}$. This much realizes the brief's "$\mathbb{D}$ viewed as a carrier": the carrier's pattern-alphabet *is* the outcome object. [PROVEN-grade display]

**2.2 Worked reproducible example — the three-way split.** "Smallest carrier with $\Phi_1 > 0$ for some assignment" resolves three inequivalent ways, and they must not be conflated:

* **(a) Difference simpliciter.** The single cut with $\mathrm{out} = \mathsf{diff}$ carries difference — δ0, before any cochain talk. Trivial, and not obstruction: nothing is failing to be repaired; nothing has been tried.
* **(b) Repair-relative residual (the one-edge case).** On the two-locus one-edge carrier, $(\delta^0 f)(\partial\{a,b\}) = f(a) \oplus f(b)$. Define (2026-07-15 second pass — the hypothesis the first draft left unnamed): an exhibited assignment family is **full for the cut** when it contains both a *constant* assignment (both loci compare alike to the reference — $\delta^0$-image $\mathsf{same}$) and a *separating* one ($\delta^0$-image $\mathsf{diff}$) — a K4-finite, per-exhibition condition on the exhibition, **not** a free function-space totality (Paper 0 §7.1: assignments are outcome-determined bundles against exhibited reference poles; whether a separating assignment is exhibited is exhibition-contingent, and K5's $\oplus$-closure cannot manufacture one from constants). Then: **over an assignment family full for the cut, every pattern on the one-edge carrier is removable** — this tree supports no parity obstruction; $Q^1$ collapses. [PROVEN, CONDITIONAL on the fullness hypothesis; PL-GTOC-18's `ZMod 2` function space is the model-level surrogate for fullness, not its discharge] The pattern $h = \mathsf{diff}$ is residual **only relative to an impoverished declared repair family** (e.g. only constant assignments exhibited/admissible) — precisely the corpus's admissible-repair relativity, $Q^1_O = C^1/\operatorname{im}(d_0|_{\mathrm{Adm}})$ (Paper 000b; Paper 0 §7.5 first honesty note). Then, with unit count-weight (δ2), $\Phi_1(h) \in \{0, 1\}$: $0$ when some admissible exhibited repair explains $h$, $1$ when none does — the brief's "qubit diagnostic," derived, but **Adm-indexed**: it diagnoses the declared repair family as much as the carrier. [PROVEN, per-exhibition; the two-valuedness is K1 + unit weight]
* **(c) Parity-forced residual.** The least carrier with a non-removable pattern *over every exhibited assignment family* is the odd triangle (Paper 0 §7.6: $(\delta^1 h)(t) = \mathsf{diff}$ blocks $\delta^0$-explanation in any exhibition; least-ness forward-logged at PL-GTOC-7(c)). Forced obstruction begins at the cycle, not the edge.

**Correction, recorded.** The brief's minimality claim is true in sense (b) only — a *declared-relative* sense — and false in sense (c), where the triangle is minimal. An "obstruction-qubit" built on (b) would have its obstruction by declaration; calling that "the ground's own qubit" would smuggle the declaration into the ontology. This is the first independent ground for §1's refusal of the name.

**2.3 What the two-locus one-edge carrier honestly is.** One declared comparison, a two-pattern alphabet, capacity-two-classes as a channel (Paper 6 §5.1), an Adm-indexed binary diagnostic (§2.2b). That is a **bit** in every derived respect and a qubit in none: no second window, no phase, no superposed pattern — a pattern *is* $\mathsf{diff}$ or $\mathsf{same}$ (K1; §5.2's superposition obstruction).

### Import Ledger — §2

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| two-locus one-edge carrier $(\{a,b\}, \{\partial\{a,b\}\}, \varnothing)$ | δ0 | §2.1 | — |
| tree-triviality (removability over a family full for the cut) | δ7 | §2.2(b) | [PROVEN, CONDITIONAL on the fullness hypothesis — an exhibition condition, named 2026-07-15]; Lean target PL-GTOC-18 (function-space surrogate, flagged) |
| Adm-relative residual; Adm-indexed $\Phi_1 \in \{0,1\}$ | δ7 | §2.2(b) (via P0 §7.5; unit weight δ2) | Adm is DECLARED — flagged; diagnostic two-valuedness K1-relative |
| parity-forced minimality of the triangle | δ0/δ2 | Paper 0 §7.6; PL-GTOC-7(c) forward log | least-ness still forward-logged — inherited flag |
| "obstruction-qubit" | — | — | REFUSED — ground (b)-vs-(c) recorded in §2.2 |

Connective audit: "tried" in (a) glosses the absence of any exhibited repair attempt; *must* in the Correction paragraph is editorial imperative about presentation; *would* occurrences in §2 are counterfactual pricing commentary in the protocol register; *before* is degree-order, not temporal — each licensed, none load-bearing.


§3 — Exchange on a pair of bit-shadows

**3.1 The pair.** Exhibit two two-locus one-edge carriers whose cut-tokens are relatively indistinguishable under the declared comparisons (Paper 3 §4.1 discipline), with exchange-saturation **declared** (K9 — inherited flag: saturation is a declaration, not a consequence of indistinguishability). The witness family $W$ has the two-link tally: $\mathrm{Sym}(W) = S_2$, exhibited as {identity, the transposition}.

**3.2 The dichotomy at $|W| = 2$.** By the Two Scalar Symmetric-Exchange Characters Theorem (Paper 3 §4.4 — [PROVEN, CONDITIONAL H1–H3, PL-GTOC-12]), the coherent one-dimensional scalar characters of the pair are exactly $\chi(\tau) = +1$ (trivial) and $\chi(\tau) = -1$ (alternating): $\tau^2 = \mathrm{id}$ forces $\chi(\tau)^2 = 1$, and the derived scalars' sign poles are distinct. **The transport-level Bose/Fermi split is thus already present on a pair of bits** — it needs indistinguishability, declared saturation, scalar weights, and coherence, and nothing quantum: no amplitudes, no spin, no Hilbert space. What it does *not* give is everything the physics adds (state-space symmetrization, spin-statistics — M13 stands, Paper 3 §4.7). [PROVEN, CONDITIONAL — inherited hypotheses; physics naming [INTERPRETIVE], fenced]

**3.3 Reading against the brief.** The brief asked that "the Two-Statistics dichotomy acts on" the two-locus one-edge carrier — this is the derivable content of that request, and its exact scope: the dichotomy acts on *transport of weight-contributions along declared exchanges of a pair*, not on any state space of a single carrier. A single bit-shadow has no exchange to be statistical about; statistics begins at the pair, as a property of declared transport.

### Import Ledger — §3

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| pair of indistinguishable bit-shadows; $S_2$ | δ7 | §3.1 | K9 saturation DECLARED — inherited flag |
| two characters at $|W|=2$ | δ7 | §3.2 (P3 §4.4 instance) | conditional H1–H3 + PL-GTOC-12 — inherited |
| Bose/Fermi naming; state symmetrization | — | — | INTERPRETIVE / NOT DERIVED (M13) — fenced |

Connective audit: clean.


§4 — The bit→qubit import price list

Each import is named, its corpus boundary cited at its actual verification status, and its R2a/R2b grade assigned where the stratification applies (Paper 2 §6.2, repaired form; Q3's operator-provenance import is R1-type added structure whose physical-realization component sits outside the R-stratification entirely — a [SCOPE FENCE], graded as such). The standard qubit interface is available only after Q1–Q4 and the $\mathbb{C}^2$ / Born interface declaration are paid; none is paid here.

**Q1 — The phase fiber (superposition's carrier).** Over exhibited weights $w_\gamma$, the quantum object adds a lift $c_\gamma = \sqrt{w_\gamma}\, e^{i\theta_\gamma}$; the added data is the relative-phase fiber $U(1)^{|E_w|-1}$ over the weight base (QM_060, ENC-1129 — "the complex Hilbert structure and unitarity are imported, not derived"). At the derived degrees this is exactly the **R1 added-structure obstruction** (Paper 2 §6.2-R1, repaired form: a fiber over the exhibited $L^1$ data — superposition law, phase, involution, sesquilinear pairing, quadratic readout — added structure, not modality). **Sub-door, priced separately (2026-07-15 R2 split):** a *finite* phase alphabet ($\mathbb{Z}/n$ cyclotomic phases) is an R2a-cheap import — finite, non-continuum; QM_062's honest gap (the abstract phase-group shadow cannot separate $U(1)$ from the torsion shadow $\mathbb{Q}/\mathbb{Z}$) means finite phases genuinely fall short of the qubit's $U(1)$, which costs continuity (Q4). A "qubit with $\mathbb{Z}/n$ phases" is a strictly cheaper object on the price list's interior — named here so the list is a lattice, not a single door.

**Q2 — Interference / the ℓ² readout.** The cross term $|c_i + c_j|^2 - |c_i|^2 - |c_j|^2 = 2\,\mathrm{Re}(c_i \bar c_j)$ is **not computable from any $\ell^1$ functional of the weights** — the corpus's mechanized boundary (QM_061, `L1_cannot_compute_interference`, ENC-1135; via pub-010 Thm 7). The $\ell^2$ norm's values are R2a-cheap for specific radicals, R2b for the completed norm; the *readout semantics* (quadratic, sesquilinear) is Q1's fiber put to work. Without Q2 a device holding a "logical qubit" stays in the coboundary/stabilizer regime — classically simulable (QM_061 §7's Gottesman–Knill reading, cited [STANDARD]) — the corpus's own "qubits that do nothing."

**Q3 — Multi-window (contextual) structure.** A qubit is measurable in non-commuting bases; the bit-shadow has one declared window, and further declared windows at δ6 are jointly classical (their outcome-patterns co-exhibit). The honest split: the **parity core of contextuality is already finite and derived-grade** — the Mermin–Peres square's $F_2$ cochain obstruction is mechanized with no Hilbert import (QM_120, `mermin_peres_f2_cochain_obstruction`, ENC-1143: parity-closure vs. declared signs, an odd-cycle-type obstruction of exactly this series' kind) — while the **operator provenance** (Pauli operators, tensor-product commutation, which windows physically co-measure) is imported and scope-fenced *there and here alike*. So Q3's price is not the parity mathematics (free) but the physical window-algebra (imported). The parity obstruction is finite and obstruction-calculus grade; the Pauli/operator reading is not. No measurement basis, observable algebra, or co-measurability relation is derived from the bit-shadow.

**Q4 — Continuous reversible dynamics (the named residual import).** QM_062's conditional forcing localizes what makes the phase carrier $\mathbb{C}/U(1)$: conjugation ∧ abelian phase ∧ **continuous** reversible pairing-preserving transport ⟹ $\mathbb{C}/U(1)$ — with continuity itself, and global field-uniqueness for composites, *named as what remains imported*. Continuity of dynamics is a continuous one-parameter transport: by Paper 4 §5.2 its parameter is a continuous duration — the R2b/G7 door of this extension's own Paper 4, now seen from the quantum side. The Bloch sphere (a continuum of states) sits behind Q1+Q2+Q4 jointly; its every great circle is a Q4 purchase.

**The list, assembled.** bit-shadow $\xrightarrow{+Q1}$ phase-bearing bit $\xrightarrow{+Q2}$ interfering two-level object $\xrightarrow{+Q3}$ contextually measurable object $\xrightarrow{+Q4}$ **qubit** (Bloch sphere, $\mathbb{C}^2$, Born pairing per the quantum-realization spine's imported interface package). Orderings other than this one are possible and the list is not claimed canonical; what is claimed is completeness-relative-to-the-cited-boundaries: each arrow is an import the corpus has explicitly located (ENC-1129, ENC-1135, ENC-1143, ENC-1136), none is derivable at δ0–δ7, and no fifth import is known to be needed for the standard qubit interface beyond these plus the $\mathbb{C}^2$ dimension declaration itself. [The completeness reading is [INTERPRETIVE]; each individual price is [STANDARD within corpus] or OBSTRUCTED here]

### Import Ledger — §4

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| phase fiber $U(1)^{|E_w|-1}$ | — | — | IMPORTED (Q1) — R1 added fiber; ENC-1129; unpaid |
| finite phase alphabet $\mathbb{Z}/n$ | — | — | IMPORTED if used (Q1 sub-door) — R2a-cheap, non-continuum; falls short of $U(1)$ (QM_062 torsion gap); unpaid |
| interference cross term; ℓ² readout | — | — | IMPORTED (Q2) — mechanized boundary ENC-1135; unpaid |
| contextual parity obstruction ($F_2$) | δ0-grade | §4-Q3 (QM_120 cited, MECHANIZED) | the parity core is finite and free; operator provenance IMPORTED — fenced |
| continuous reversible dynamics; $U(1)$; $\mathbb{C}$ | — | — | IMPORTED (Q4) — QM_062's named residual imports (continuity; global field-uniqueness); R2b/G7 via Paper 4 §5.2 |
| Bloch sphere, $\mathbb{C}^2$, Born pairing | — | — | composite of Q1+Q2+Q4 + dimension declaration — quantum-realization interface package; never used |

Connective audit: the $\xrightarrow{+Q_i}$ arrows are ledger structure (which import is added), not temporal or dynamical steps; "purchase" is price-list register; *possible* ("orderings other than this one are possible") is fenced inside the [INTERPRETIVE] completeness reading, not a derived modality.


§5 — Obstruction register

**5.1 The qubit itself.**

> **OBSTRUCTION.** The following cannot be derived from what is available at this degree: the qubit — a two-level system with phase, interference, multi-basis measurability, and continuous reversible dynamics. What would have to be admitted: imports Q1–Q4 (§4), plus the $\mathbb{C}^2$ state-space declaration. What is lost if it is admitted: the count semantics of the bit-shadow's weights (R1's stated loss), the per-exhibition semantics of its diagnostics, and — for Q4 — exhibition-closure at the continuum door (G7). "State-space" here is not a hidden domain already present behind the bit-shadow. It is an imported representation interface whose carrier, scalars, effects, and readout rules must be declared.

**5.2 Superposition.**

> **OBSTRUCTION.** The following cannot be derived from what is available at this degree: superposition. At every derived degree a pattern on the two-locus one-edge carrier *is* $\mathsf{diff}$ or $\mathsf{same}$ — K1's exhaustive bivalence ruling admits no third or blended verdict, and the K1-relativity of this very exclusion is on the charter's ledger (drop K1 and there is no two-valued alphabet to superpose *over*, not a superposition). What would have to be admitted: the R1 fiber (Q1) — amplitude components over exhibited pattern labels as **added structure** (not modality: the components attach to exhibited labels; what is missing is the superposition law, phase, and quadratic readout the counts do not determine). What is lost if it is admitted: weight-as-carriage — a weight becomes an amplitude coordinate; positivity and the proportion reading of Paper 2 §5.3 go with it.

**5.3 What "qubit capacity" would even mean.** The bit-shadow's channel capacity is the two-class count (Paper 6 §5). Qubit accessible-information results (one qubit yields at most one bit — Holevo-type) are **imported wholesale**: QM_061's fence is inherited verbatim ("not a derivation or finite version of Holevo's theorem"), and nothing at δ7 shrinks that distance.

**5.4 Naming discipline.** "Obstruction-qubit" [REFUSED] (grounds: §2.2's declared-relative obstruction; §4's four unpaid imports). "Bit-shadow" is the derived name; "qubit" appears in this series only to the right of the §4 price list. The quantum-realization spine (GTQ/GTQM as realization, not a tower layer — the review's glossary note) is the proper home of everything past the list.

### Import Ledger — §5

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| qubit | — | — | **OBSTRUCTION** §5.1 — Q1–Q4 + dimension declaration; never admitted here |
| superposition | — | — | **OBSTRUCTION** §5.2 — R1 fiber; K1-relative exclusion flagged |
| Holevo-type accessible information | — | — | IMPORTED — QM_061 fence inherited; not used |
| "obstruction-qubit" / "bit-shadow" / "qubit" (names) | δ7 | §5.4 naming discipline | REFUSED / derived / price-listed respectively |

Connective audit: clean; modal verbs confined to obstruction templates.


§6 — Claim ledger, falsifiability, boundary

**6.1 Claim Ledger.**

| ID | Claim (location) | Type | Basis / notes |
|---|---|---|---|
| P7-C1 | Minimal carrier displayed; pattern alphabet = 𝔻 (§2.1) | [PROVEN] | finite display |
| P7-C2 | Tree-triviality on the one-edge carrier, over an assignment family full for the cut (§2.2b) | [PROVEN, CONDITIONAL] | H: the fullness exhibition-hypothesis (named 2026-07-15 — "full" defined, not assumed); finite check given it; PL-GTOC-18's `ZMod 2` space is the surrogate, not the discharge |
| P7-C3 | Adm-relative residual + Adm-indexed binary $\Phi_1$ on the minimal carrier (§2.2b) | [PROVEN, CONDITIONAL] | Adm declared; K1 + unit weight; P0 §7.5 machinery |
| P7-C4 | Three-way minimality split; brief's claim true only in sense (b) (§2.2) | [PROVEN] | (a),(b) here; (c) = P0 §7.6 with least-ness forward-logged (PL-GTOC-7(c)) — inherited flag |
| P7-C5 | Exchange dichotomy on a pair of bit-shadows (§3.2) | [PROVEN, CONDITIONAL] | P3 §4.4 at $\|W\|=2$; H1–H3, K9, PL-GTOC-12 inherited |
| P7-C6 | The four-import price list Q1–Q4 with cited boundaries (§4) | [STANDARD within corpus] + `OPEN` here | ENC-1129/1135/1143/1136; each import obstructed-or-imported at δ7 |
| P7-C7 | Completeness reading of the price list (§4, "assembled") | [INTERPRETIVE] | fenced — no fifth-import theorem claimed |
| P7-C8 | Qubit and superposition obstructed (§5.1–5.2) | `OPEN` | obstruction blocks; R1 pricing per repaired Paper 2 |
| P7-C9 | Naming discipline: obstruction-qubit REFUSED; bit-shadow derived (§1, §5.4) | [PROVEN]-grounded ruling | grounds P7-C2/C4/C6; review placement adopted |

**6.2 Falsifiability.** This paper fails if: (a) a non-removable pattern over a *full* exhibited assignment family is exhibited on the one-edge carrier (refuting P7-C2 — a finite check); (b) the interference cross term is computed from the derived weight functionals alone (contradicting the mechanized ENC-1135 boundary, which blocks exactly that), or interference/phase structure is otherwise constructed from δ0–δ7 resources without paying Q1/Q2 (refuting this paper's §5 obstruction blocks — a foundational event); (c) the $|W|=2$ character count differs from two over the derived scalars (refuting P7-C5 and with it Paper 3's theorem); (d) a fifth independent import is shown *necessary* for the standard qubit interface (P7-C7's completeness reading falls — a correction, not a refutation, since it is fenced [INTERPRETIVE]); (e) the review's bit-like ruling is itself overturned by a derivation of any Q-import from the ground (each import row would need re-audit).

**6.3 What this paper does NOT claim.** No qubit, no Hilbert space, no Bloch sphere, no Born pairing, no measurement theory, no complementarity, no quantum computing claims in either direction (QM_061's non-claims inherited), no claim that physical two-level systems are bit-shadows. No authority.

**6.4 New proof obligations** (recorded in `omega_engine/research/encyclopedia/proof_ledger_20260715.md`):

* **PL-GTOC-18 (LEAN4, not-gating-honesty):** on the two-point one-edge carrier over `ZMod 2`: (i) $\operatorname{im}(\delta^0)$ is all of $C^1$ (tree-triviality, P7-C2); (ii) restricting the repair family to constants makes the $\mathsf{diff}$ pattern non-removable (Adm-relativity witness, P7-C3); packaged beside PL-GTOC-1/8's carrier setting.

**6.5 Why this matters.** "The qubit is just a generalized bit" and "the qubit is fundamentally non-classical" are both slogans; this paper replaces the pair with a ledger. Everything bit-like about a two-level system is derived here at named cost (K1 for the alphabet; a declaration for its window; Adm for its binary diagnostic) — and everything qubit-like is one of four cited imports, **three of them mechanized boundaries in this corpus (ENC-1135/1136/1143) and the fourth a prose-proved fiber reading whose constituents are mechanized in pub-010 (ENC-1129: status PROVED-PROSE, dedicated Lean an open target, PL-QM043-1)** — the 2026-07-15 second pass corrected this sentence's memberships in both directions (the first draft overstated 1129 and understated 1136). The finite-phase sub-door (Q1, R2a) marks a genuinely intermediate object — phase-bearing but not continuum-phased — that folklore skips over. And the minimality split (§2.2) corrects a natural error the goal prompt itself instantiated: reading a *repair-family-relative* obstruction as an intrinsic one. The one-edge tree is innocent (proven here; the general-tree statement is the still-open PL-GTOC-7(c) companion, [STANDARD] externally); cycles obstruct; declarations do the rest.

**6.6 Nearest neighbors (external positioning).** [Positioning [INTERPRETIVE]; citations [VERIFY].]

* **Quantum reconstructions** (Hardy 2001; Masanes–Müller 2011; Chiribella–D'Ariano–Perinotti 2011 [VERIFY]): derive the qubit from operational axioms (continuity/reversibility among them). This paper stops before every such axiom and prices it (Q4 is exactly their continuity postulate, named as an import per QM_062).
* **Stabilizer formalism / Gottesman–Knill** (Gottesman 1997 [VERIFY]): the phase-blind/coboundary regime is classically simulable. Cited via QM_061 as the *content* of "bit-shadow plus nothing": short of Q2, no quantum advantage object exists.
* **Kochen–Specker / Mermin–Peres** (Kochen–Specker 1967; Mermin 1990; Peres 1990 [VERIFY]): contextuality. Q3's split follows QM_120: the parity-cochain core is finite mathematics (mechanized, no Hilbert); the operator realization is the import.
* **Real-vs-complex quantum theory** (Renou et al., *Nature* 2021, via QM_062 [VERIFY]): empirical separation of complex QM. Enters only as QM_062's cited support for the *global field-uniqueness* import — nothing empirical is claimed here.
* **Spekkens' toy theory** (Spekkens 2007 [VERIFY]): a local-hidden-state model reproducing many qubit phenomena without quantum structure. Nearest in spirit; the bit-shadow is poorer still — no epistemic-state machinery, no toy dynamics — and the comparison marks how much even a "toy qubit" imports beyond the derived floor.

In each case the direction is the same: this paper claims *less*, and states exactly what the neighbor adds.

### Import Ledger — §6 (consolidated, paper-level)

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| two-locus one-edge carrier, tree-triviality, Adm-indexed diagnostic, bit-shadow | δ0–δ7 | §2 | Adm/K1 relativities flagged; no new conventions at δ7 |
| pair-exchange dichotomy | δ7 | §3 | inherited conditionalities (H1–H3, K9, PL-GTOC-12) |
| Q1–Q4 imports; qubit; superposition | — | — | OBSTRUCTED/IMPORTED (§4–§5) — every door priced, none taken |

Connective audit (paper-level): per-exhibition discipline in every universal; price-list arrows are ledger notation; modal verbs confined to obstruction and pricing registers.

### §6.6 — Mathematical Generalization: Qudit Shadow & CPTP Contraction Bounds (`Stage 1.5`)

Corpus-wide mining over quantum channel transport (qm_080 / qm_081) permits generalizing the 2-locus binary bit-shadow $\mathbb{D}$ to $d$-locus qudit shadows $\mathbb{D}_d$ ($d \ge 2$) under trace-preserving positive maps. For any positive trace-preserving channel $\mathcal{E}$ acting on the generalized shadow space, the contraction ratio $\gamma(\mathcal{E}) = \sup_{\vec{r} \neq 0} \frac{\|\mathcal{E}(\vec{r})\|_2}{\|\vec{r}\|_2} \le 1$ upper-bounds the shadow capacity. We record this as a formal obligation `PL-QM072-10` (`P7-C10`, `[CONJECTURE]`): strict contraction $\gamma(\mathcal{E}) < 1$ occurs if and only if $\mathcal{E}$ introduces non-zero residual dissipation.


Post-paper protocol (per the charter failure protocol and `../../001_gtoc_gtla/999_gtoc/theorem_ledger.md` §5)

**Degree index row (for the charter):**

| Degree | Paper | What becomes available |
|---|---|---|
| δ7 | Paper 7 | the minimal carrier's three-way minimality split (tree-triviality theorem; Adm-relative residual; parity-forced triangle); the Adm-indexed binary diagnostic; the exchange dichotomy on a pair of bit-shadows; the itemized bit→qubit price list (Q1 phase fiber / Q2 interference-ℓ² / Q3 window-algebra / Q4 continuity), with the finite-phase R2a sub-door; superposition and the qubit obstructed with stated losses |

**What this paper supports:** exact bit-content of two-level talk; the corrected minimality claim; transport-level statistics on pairs; a lattice of intermediate objects between bit and qubit with per-arrow prices.
**What it does not support:** any qubit, superposition, interference, complementarity, or quantum-information claim.
**Narrowest defensible claim:** on the exhibited two-locus one-edge carrier, every pattern is removable over an assignment family full for the cut, and non-removability there is exactly relative to a repair family — exhibited or declared — that misses a separating assignment.
<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `P7-C1` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `072:P7-C1`) |
| `P7-C2` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `072:P7-C2`) |
| `P7-C3` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `072:P7-C3`) |
| `P7-C4` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `072:P7-C4`) |
| `P7-C5` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `072:P7-C5`) |
| `P7-C6` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `072:P7-C6`) |
| `P7-C7` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `072:P7-C7`) |
| `P7-C8` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `072:P7-C8`) |
| `P7-C9` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `072:P7-C9`) |
| `P7-C10` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `072:P7-C10`) |

<!-- claim-id-body-index:end -->
