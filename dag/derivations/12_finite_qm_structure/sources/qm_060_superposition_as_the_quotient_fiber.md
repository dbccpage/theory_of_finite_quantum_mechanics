# Superposition as the Quotient Fiber

## GTOC Foundations — Quantum Contact Series (qm_060_superposition_as_the_quotient_fiber)

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

document_id: "OMEGA-QM-SUPERPOS-043"
version: "v0.1.0 Pre-Print"
last_updated: "2026-06-19"
status: "DRAFT — component note (phase-fiber rung) of QM_121 (The Finite QM Ingredient Ladder)"
series: "qm / QM ingredient ladder"
companions:
- "pub-010 Born Normalization … Redundancy (the lift, row-sparsity, and cross term this paper reads)"
- "QM_070 Product Non-Factorization (the phase-blind quotient)"
mechanization: "MECHANIZED (ENC-1129: lean4/research_programs/quantum_foundations/003_qm_phase_fiber_interference.lean, lean4/shared_kernel/primitive_difference.lean; QM.PhaseFiber.SuperpositionState.lggr_non_factorization)"

---

### The phase *content* of superposition, relative to a declared sector basis — a reuse/synthesis of pub-010, not new machinery

> **Component note (rung 5) of *QM_121 — The Finite QM Ingredient Ladder*.** The publishable synthesis
> is QM_121; this note is the detailed source for the phase-fiber rung, and keeps its own claim ledger.

Abstract

**Main result (informal).** Relative to a **declared residual-sector basis**, a superposition is a
Hilbert lift $c_\gamma=\sqrt{w_\gamma}\,e^{i\theta_\gamma}$ of residual weights $w$. It is
*probabilistically redundant* — $|c_\gamma|^2=w_\gamma$ gives the same diagonal law as the bare
weights — and its phase is *invisible* to the phase-blind L1 quotient, yet it *reappears* under a
mixing/readout operation as a non-quotient cross term. So, **in the declared sector basis, the
*phase content* of a superposition is the fiber of the phase-blind L1 quotient over the diagonal
weights**: nothing probabilistically (on the diagonal readout), something dynamically (under
mixing). This is **basis-relative** (the weight/phase split changes with the chosen basis) and a
reading of the already-published pub-010 results, **not new machinery**. We do *not* claim
"superposition itself is nothing but a quotient fiber" — only its phase content, in the declared
representation.

**Why a researcher should care.** "Superposition" is usually treated as the irreducible quantum
mystery. Placed on residual weights it splits cleanly into a part that does nothing (the phase, as
far as probabilities go — pub-010's redundancy) and a part that does everything (the same phase,
once two branches are mixed — pub-010's interference cross term). Naming superposition as the
quotient fiber says precisely *where* its content lives and where it does not, and reuses
machine-checked facts rather than postulating new ones.

1. Carrier


Residual sector weights $w_\gamma\ge0$ (the L1 carrier of the ladder). A superposition is a complex
lift $c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}$ over them. [DEFINITION]

2. Primitive difference


The phase-blind primitive difference $\delta(c,c')_\gamma=|c_\gamma|^2-|c'_\gamma|^2$ (pub-010): it
compares squared moduli ($|c_\gamma|^2=w_\gamma$, the Born weight) and ignores phase entirely. [DEFINITION]

3. ZeroRel


$\delta\equiv0$ identifies lifts with equal moduli — superpositions sharing those moduli, at *any*
phase, are the same point of the quotient (pub-010 row-sparsity). [DEFINITION]

4. Structure


The quotient is the space of weight vectors; the **fiber** over a weight point is the set of phases
— the superpositions sharing those weights. The fiber dimension is support-dependent and
global-phase-reduced: for sectors with $w_\gamma=0$ the phase coordinate is **inert**, and on the
nonzero support $E_w=\{\gamma:w_\gamma>0\}$ the raw lift fiber is $U(1)^{E_w}$ while the physically
relevant **relative-phase** fiber (after quotienting the gauge global phase) is $U(1)^{|E_w|-1}$.
"Fiber" here is in the declared residual-sector representation, not an ontology of physical phase.
[DEFINITION]

5. The fiber


**Theorem (Phase-content fiber theorem).** For weights $w$ and lift $c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}$:
(i) $|c_\gamma|^2=w_\gamma$ — same probability law (redundant; pub-010 Thm 4);
(ii) the phase $\theta$ is in the kernel of $\delta$ — quotient-invisible (pub-010 Thm 3);
(iii) under a two-row mixing operation the phase reappears as a non-quotient-factoring cross term
(pub-010 Thm 7).
[PROVEN — by reuse of pub-010 (its constituents MECHANIZED); see "Mechanization"]

6. $\Phi_1$ versus $\Gamma_2$


The fiber carries no probability mass (it is quotient-trivial for $\Phi$); its content is the
dynamical cross term, which is the interference diagnostic (rung 7). [SCOPE FENCE]

7. Observer


The phase-blind readout sees only the weights (the quotient base); a mixing readout sees the
fiber (the phase) via interference. Superposition's weight/phase split is **readout-relative**
(context-relative) in exactly this sense — "observer" here means the declared readout/quotient, not
a conscious observer. [INTERPRETIVE]

8. Witnesses


The certificates are pub-010's: Born redundancy ($|c|^2=w$), phase-blind row-sparsity (phase in
$\ker\delta$), and the two-row mixing LGGR cross term (phase made visible). [PROVEN — mechanized in pub-010]

9. Operators / lifts


Superposition *is* the lift (the fiber); a mixing/unitary operation acts on the fiber and projects
the phase into observable weight differences (the cross term). The complex Hilbert structure and
unitarity are imported (pub-010 Thm 6), not derived. [SCOPE FENCE]

10. Route survivors


A weight point + a phase choice routes to a superposition; phase-equal-modulus choices are the same
quotient point but distinct fiber points. [DEFINITION / OPERATIONAL RULE]

11. Terminalize


Descent arc: weights + phase → a superposition (fiber point); probabilistically it terminalizes to
the same law (redundant); dynamically (under mixing) it contributes a **replayable cross-term
witness**. Finite, replayable (pub-010's worked replay). ("Terminalizes" is reserved for the actual
terminal-packet machinery; here the phase yields a cross-term witness, not a packet terminal.)

**Green / red firewall (the terminal).**

- **GREEN (cheap, mechanized in pub-010):** the lift is probability-redundant; phase is
  quotient-invisible; phase reappears as the mixing cross term.

- **RED (not claimed):** a derivation of the complex Hilbert space, unitarity, or the Born rule as
  ontology (pub-010 Thm 6 fences these as imported); that phase is physical beyond its cross-term
  effect; any grant of authority. $\mathsf{StructureDerived}\not\Rightarrow\mathsf{IsAuth}$.

12. Comparison to literature


Standard QM treats superposition as a state-vector primitive; pub-010 already showed that, over
$\ell^1$ weights, the Hilbert lift is a redundant encoding whose phase is dynamically (not
probabilistically) meaningful. This paper only *names* that result — superposition is the quotient
fiber — and connects it to interference (rung 7). No new theorem; a synthesis of pub-010. [INTERPRETIVE]

Worked example

Weights $w=(1,1)$. The (unnormalized) amplitude lifts $c=(1,1)$ and $c'=(1,-1)$ have the same
moduli $|c|^2=|c'|^2=(1,1)$, hence the same **L1-normalized diagonal law** $(\tfrac12,\tfrac12)$ and
the same quotient point (phase-invisible). But a two-row mix sends the amplitudes to $(x{+}y,x{-}y)$:
$(2,0)$ and $(0,2)$ respectively — i.e. mixed weights $(4,0)$ and $(0,4)$, normalized $(1,0)$ and
$(0,1)$ — so the phase becomes visible (pub-010's LGGR witness). One quotient point, two fiber
points. *(Registers: the diagonal law is L1-normalized; the mixed outputs $(2,0)/(0,2)$ are
unnormalized coherent-sum amplitudes, $(4,0)/(0,4)$ the corresponding weights.)* [WORKED EXAMPLE]

Falsifiability

Falsified if a lift with $|c_\gamma|^2=w_\gamma$ gave a *different* probability law (it cannot —
pub-010 Thm 4), or if phase-equal-modulus lifts were *distinguished* by the phase-blind quotient
(they are not — Thm 3), or if no mixing operation could make the phase visible (it can — Thm 7).

What this paper does NOT claim

[SCOPE FENCE]

- **Not a derivation of complex Hilbert space / unitarity / Born-as-ontology** (pub-010 Thm 6 fences
  these as imported).

- **Phase is assigned no ontology beyond its packet-distinguishable effects under declared
  transformations** (the two-row cross term is the *minimal* witness used here, not the only effect);
  superposition adds no diagonal-readout probability content.

- **Not "superposition itself is nothing but a quotient fiber"** — only its *phase content*, in the
  declared sector basis.

- **Reuse, not new machinery**; **basis/sector-relative**; **mints no authority**.

Mechanization

`PROVED-PROSE` by **reuse of pub-010**, secured as **ENC-1129** (`paper:qm060:SUPERPOS-FIBER-001`).
The constituents — Born redundancy, phase-blind row-sparsity, and the two-row mixing LGGR cross
term — are already MECHANIZED in pub-010 (`PaperQF002.L010_01_BornRedundancy`). A dedicated
superposition-fiber Lean is optional (`PL-QM043-1`, TARGETED, NON-BLOCKING) and would only re-package them.

References

- pub-010, *Born Normalization … Redundancy* (Thms 3, 4, 7 — the lift, row-sparsity, cross term);
  QM_070 (the phase-blind quotient); interference is rung 7 (also pub-010's cross term).

Changelog

Version Note: v2.0 (2026-06-19)** — External-review honesty pass + marked as a **component note** of the
  forthcoming *Finite QM Ingredient Ladder*. Title qualified to the **phase content** of
  superposition (subtitle); abstract now leads with **basis-relativity** and refuses "superposition
  itself is nothing but a quotient fiber" (only its phase content, in the declared basis); §4 adds
  the **global-phase / zero-weight** caveat (relative-phase fiber $U(1)^{|E_w|-1}$, inert phase at
  $w_\gamma=0$); §7 "observer-relative" → **"readout/context-relative"** (observer = declared
  readout, not conscious); non-claims: "phase not physical beyond cross term" → **packet-
  distinguishable effects** (cross term is the *minimal* witness, not the only effect); §11
  "terminalizes to the cross term" → "**replayable cross-term witness**" ("terminalizes" reserved
  for the packet machinery); worked example made **register-explicit** (normalized law vs
  unnormalized mixed amplitudes). No math change; still PROVED-PROSE reuse of pub-010.

Version Note: v1.2 (2026-06-17)** — Fixed the phase-blind primitive difference: $\delta=c^2-c'^2$ →
  $\delta=|c_\gamma|^2-|c'_\gamma|^2$ (modulus-squared, the Born weight). The algebraic-square form
  carried doubled phase ($c_\gamma^2=w_\gamma e^{2i\theta_\gamma}$) and so identified only
  sign-equivalent lifts ($c=\pm c'$, phase mod $\pi$), not equal-modulus lifts at any phase as the
  text claims; the modulus-squared form is the correct phase-blind quotient (matches pub-010's
  $\ell^1$ weight). Caught in PR review.

Version Note: v1.1 (2026-06-17)** — First hygiene Improver pass + adversary gates. Rubric verified; claims
  typed; sibling Claim Ledger created. Reuse paper (synthesis of pub-010); no honesty-gating
  obligation (constituents mechanized in pub-010).

Version Note: v1.0 (2026-06-17)** — Initial draft. QM ingredient-ladder rung 6 (superposition).

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-060-C1` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `060:QM-060-C1`) |
| `QM-060-C2` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `060:QM-060-C2`) |
| `QM-060-C3` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `060:QM-060-C3`) |
| `QM-060-C4` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `060:QM-060-C4`) |
| `QM-060-C5` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `060:QM-060-C5`) |
| `QM-060-C6` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `060:QM-060-C6`) |
| `QM-060-C7` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `060:QM-060-C7`) |
| `QM-060-C8` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `060:QM-060-C8`) |
| `QM-060-C9` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `060:QM-060-C9`) |

<!-- claim-id-body-index:end -->
