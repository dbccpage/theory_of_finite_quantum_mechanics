Claim Ledger — Paper QM_091: Deutsch / Everett / Wolfram — The Promotion Error (OMEGA-QM-PROMOTION-014)
=======================================================================================================

**Paper Key:** `003_quantum_foundations/091_deutsch_everett_wolfram_promotion_error`  

Date: 2026-06-17
Version: v0.1.0 Pre-Print
Series: qm / QM authority-firewall critique (consolidates 02_§1 + QM_090)
Companions: QM_090 (Interpretations as Authority Shadows), QM_110 (T7 no-authority),
QM_100/qm_103_show_the_packet_protocol (packet schema + protocol), QM_Series_Falsifiability_Ledger (per-thesis falsifiers),
QM_082/QM_111/QM_060 (the individual boundary papers — overlap, not subsumed), QM_092.

Firewall note: QM is a realization spine. **No authority minted.** The only arrow into
the authority terminal is CODA-FDA `Π♯`. This paper's whole content is the firewall plus
three *scoped, individually-defeasible readings* of it. `StructureDerived(F,c) ⇏ IsAuth(t)`.

Paper character: an **audit of authority promotion** — a critique/firewall paper, not a
refutation. The load-bearing firewall (§1) splits into: (1a) the bare non-implication
`StructureDerived ⇏ IsAuth`, now genuinely MECHANIZED (axiom-free) in
[index:index:PossibilityBoundaries.lean](omega_engine/research/_indexes/_master_index.yaml); and (1b) the stronger *only-via-`Π♯`*
factorization, which is PROSE/OPEN (NOT mechanized — the `AuthorityNonPromotion.lean`
lemma is vacuously hypothesis-gated). The three per-program boundary claims are
explicitly [INTERPRETIVE] (argued readings), each defeasible by supplying a packet.
(2026-06-18 claim-verification triage: the prior single `[PROVEN, MECHANIZED]` tag was
RED for overstating 1b; this split is the fix.)

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-091-C1a | Bare non-implication `StructureDerived(F,c) ⇏ IsAuth(t)` (structure-derivation does not by itself mint authority). | **[PROVEN, MECHANIZED — axiom-free]** — [index:index:PossibilityBoundaries.lean](omega_engine/research/_indexes/_master_index.yaml) (`structure_not_auth`, `not_structureDerived_implies_isAuth`), a genuine countermodel | §1 (a), §0 Tier 1a |
| QM-091-C1b | Stronger: no constructor `promote: FormalModel → AuthorityTerminal` that skips the packet; authority factors **only** as declare→packet→`Π♯`. | **[PROSE / OPEN]** — NOT mechanized (LT-A factorization target); the `AuthorityNonPromotion.lean` lemma is vacuously hypothesis-gated and does not establish it | §1 (b), §0 Tier 1b, doctrine box |
| QM-091-C2 | The three types `FormalModel`, `PhysicalRealizationPacket`, `AuthorityTerminal` are distinct. | [DEFINITION] | §1 |
| QM-091-C3 | The four-row promotion-error table (Deutsch / Everett–DeWitt / Wolfram / modal "God-proofs") each reads `formal coherence ⊬ world authority`. | [INTERPRETIVE] (classification of the shared gap) | §1 table |
| QM-091-C4 | **Worked instance:** on $C^0=\mathbb R^2,C^1=\mathbb R,d_0=(1,-1),\omega=(1,1)$, the structure fixes $\Phi_1$ but fixes **no** packet field — the promotion error in miniature. | [WORKED EXAMPLE] | §1.3 |
| QM-091-C5 | **Deutsch:** CTD is a high-level physical principle and does not by itself supply the scalable-physical-QC repair-capacity packet; possible-task language is not a repair-capacity certificate. | [INTERPRETIVE / scoped — argued, defeasible] | §2 |
| QM-091-C6 | Deutsch is **right** that QC is formally possible in the quantum model; that admissibility is not physical authority. (Credit, not refutation.) | [INTERPRETIVE / fairness credit] | §2, §5 |
| QM-091-C7 | The conditional physical no-go (PO-QC-T4) is itself conditional; its antecedent is the open Tier-3 burden. | [OPEN] (antecedent open) | §2 |
| QM-091-C8 | **Everett–DeWitt:** a unitary branch *representation* does not construct ontology/authority without a branch-observable packet + terminal evidence. | [INTERPRETIVE / scoped — argued, defeasible] | §3 |
| QM-091-C9 | Per QM_090, an interpretation is incorrect *only* when it makes a packet-distinguishable false claim; absent that, branch ontology is an upper-layer representation shadow. | [INTERPRETIVE] (imports QM_090 rule) | §3 |
| QM-091-C10 | **Wolfram:** rule generativity does not imply world authority / explanatory closure without a finite-descent terminalizer that selects world-authoritative claims and rejects non-world rules. | [INTERPRETIVE / scoped — argued, defeasible] | §4 |
| QM-091-C11 | Wolfram/ruliad internal mathematics is **out of scope** (Master Index Red-11); this section is admissible **only** as the strict non-implication, never as "Wolfram refuted." | [SCOPE FENCE] | §4 scope guard |
| QM-091-C12 | Fairness ledger: each program genuinely supplies real structure (universality principle + real threshold theorems; parsimonious collapse-free unitary account; generative substrate with pattern richness); each lacks the packet for authority/ontology. | [INTERPRETIVE / fairness credit] | §5 |
| QM-091-C13 | Threshold theorems are read as **real conditional repair-capacity certificates under declared hypotheses** (credited, not denied). | [STANDARD — threshold/fault-tolerance theorems; Shor 1996 / Aharonov–Ben-Or 1997 / Kitaev 1997, cited in §1.2] | §2, §5 |
| QM-091-C14 | A *missing* packet does not prove impossibility; it means the claim is **unterminated under this evidence standard**. | [SCOPE FENCE] | §6, §0 Tier 3 |
| QM-091-C15 | Strict non-claims: NOT "QC impossible", NOT "Deutsch/Everett/Wolfram refuted", NOT "unitary formalism inconsistent", NOT "experiment fake / threshold refuted", NOT "GTLA derives QM/Born/any no-go". | [SCOPE FENCE] | §7 |
| QM-091-C16 | Each program **defeats** this critique by supplying the named terminalizing packet (Deutsch: scale-bounded packet; Everett: packet-distinguishable ontology; Wolfram: world-selecting terminalizer). | [OPEN] (defeat conditions, per program) | §2–§4, §6 |

Definition-as-theorem audit
---------------------------

PASSED. The single load-bearing formal claim (C1, the type-separation firewall) is a
genuine non-implication mechanized as the LT-A kernel — it is **not** a definition wearing
"Theorem": the disjointness of the three types (C2, `[DEFINITION]`) is the *setup*, and the
content is the proven *absence of a constructor* between them. The three per-program claims
(C5/C8/C10) are correctly typed `[INTERPRETIVE]` (argued scoped readings), never `[PROVEN]`.
The four-row table (C3) is a classification, typed `[INTERPRETIVE]`, not a theorem. No
inflation; no scoped reading is dressed as a theorem; the firewall is not over-credited to
the applications.

Truth / fair-attribution audit (critique-paper specific)
--------------------------------------------------------

The paper's attributions of Deutsch, Everett–DeWitt, and Wolfram positions are stated at the
level each program actually holds (universality principle, not "scalable device guaranteed";
relative-state/branch *representation*, not asserted ontology; rule *generativity*, not
asserted world-authority) and the paper repeatedly **credits** each program (C6, C12, C13).
All bibliographic attributions added in the §1.2 related-work pass were verified canonical in
the Stage-2 adversary pass (Deutsch 1985, Shor 1996, Aharonov–Ben-Or 1997, Kitaev 1997,
Everett 1957, DeWitt–Graham 1973, Wolfram 2002 / Physics Project 2020, Abramsky–Brandenburger
2011) and cited in full — no citation invented, no `[VERIFY]` tag left dangling. A critique
that misattributed any position would be a truth-gate failure; the typing here isolates
exactly which sentences are attribution (cited) vs. the paper's own [INTERPRETIVE] reading vs.
the [PROVEN] firewall.

Support ledger (Part C — upgrade paths)
---------------------------------------

| ID | What would upgrade / defeat it | Difficulty | Lean/numerical? | Obligation |
|---|---|---|---|---|
| QM-091-C1 | Mechanize the four typed non-implications of LT-A (`StructureDerived ⊬ IsAuth`, `ValidTransport ⊬ Authority`, `LocalReplay ⊬ SealedAuthority`, `ScopedTerminal ≠ ExactAuthority`) in `lean4/QM/` against the LT-A foundation kernel → flips the firewall from prose+target to MECHANIZED-here | Low–Medium (type separation) | LEAN4 | **PL-QM014-1** (hardening; the firewall is already secured ENC-1063 — not honesty-gating) |
| QM-091-C5 | A CTD-extending realization functor emitting a *complete* repair-capacity packet at human-significant scale (bounded `λ≤μ`, `p_pair→0`, replayable `Π♯`) — **defeats** the Deutsch boundary; this is the shared architecture-class question already logged for the projection-obstruction papers (PL-QM003-1 / PL-QM005-1) | Hard | Prose + Numerical | shared with PL-QM003-1 / PL-QM005-1 — not duplicated |
| QM-091-C8 | A packet-distinguishable branch ontology terminalizing without surplus unobservable structure — **defeats** the Everett boundary | Hard (foundational) | Prose | research-level; out of scope here |
| QM-091-C10 | Rule generativity paired with a finite-descent terminalizer that *selects* world-authoritative claims and *rejects* non-world rules — **defeats** the Wolfram boundary | Hard (foundational) | Prose | research-level; out of scope here |

**No honesty-gating open obligations.** C1 is `[PROVEN]` (type separation; firewall secured
ENC-1063, LT-A target). PL-QM014-1 is a LEAN4 *hardening* target for the LT-A non-implications.
C5/C8/C10 are correctly typed `[INTERPRETIVE]` scoped readings whose **defeat** conditions are
fenced open (C16); they are research-level boundaries, not gaps in this paper. C7/C16 are
`[OPEN]` by design (this paper *fences* those openings rather than closing them). The §1.2
attributions were verified canonical and cited in full in Stage 2 (no dangling `[VERIFY]`).
