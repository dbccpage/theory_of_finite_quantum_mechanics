Claim Ledger — Paper QM_101: Threshold Theorems as Repair-Capacity Certificates (THR-001)
=========================================================================================

**Paper Key:** `003_quantum_foundations/101_threshold_theorems_as_repair_capacity_certificates`  

Date: 2026-06-17
Version: v0.1.0 Pre-Print
Series: qm / projection-obstruction route — pro-QC complement
Companions: QM_100 (public no-go), qm_100_projection_obstruction_technical_appendix (technical appendix), qm_103_show_the_packet_protocol (Show-the-Packet),
QM_Series_Falsifiability_Ledger (falsifiability ledger), QM_061 (archived to qm_archived_stubs_022_026.md; its Repair-Capacity Conditional No-Go = PO-QC-T4, carried by QM_100/003/015/021)

Firewall note: QM is a realization spine. **No authority minted.** The only arrow into
authority is a CODA-FDA `Pi_sharp` terminalization; structural derivation does not promote:
`StructureDerived(F,c) ⇏ IsAuth(t)`.

Paper character: a **reading + packet-population audit**. The fault-tolerance threshold
theorems themselves are STANDARD and **imported** (Aharonov–Ben-Or, Knill–Laflamme–Zurek,
Kitaev — cited, not re-proved). The paper's own contribution is the *reading* — threshold
theorem ⇒ scoped repair-capacity certificate — and the residual-quotient framing of when
the projection-obstruction conditional no-go is suppressed. The one paper-original result
(THR-001) is the packet-population mapping (a *construction* — true by how the packet is
defined; demoted from `[PROVEN]` in Stage 2); its no-go-does-not-fire corollary is the
genuinely derived content, conditional on the imported architecture hypotheses. The
complementary combinatorial repair-image monotonicity is MECHANIZED axiom-free (ENC-1066,
`OmegaCore.QM.repair_monotone`); only the *rate* inequality at scale stays imported.

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-101-C1 | A threshold theorem is the strongest existing *pro-QC* answer to the Show-the-Packet demand | [INTERPRETIVE / DOCTRINE] | Core-doctrine box, §0 |
| QM-101-C2 | Boxed implication: (declared threshold hyps hold) ∧ (`p_pair → 0`) ⇒ ¬ConditionalNoGo(packet) | [PROVEN, CONDITIONAL + declared threshold hyps + `p_pair → 0`] | Boxed eq, §0 |
| QM-101-C3 | A threshold theorem populates every repair-capacity packet field + yields a logical-pairing bound | [DEFINITION / CONSTRUCTION] (THR-001 mapping — true by how the packet is defined) | §0 tier 1, §2 |
| QM-101-C4 | If declared hyps hold at target workload and `p_pair → 0`, the projection-obstruction conditional no-go does not follow inside that packet | [PROVEN, CONDITIONAL + H(Theta) + `p_pair → 0`] | §0 tier 2, §2 corollary |
| QM-101-C5 | Physical scalability is thereby *established* for any real device | **NOT claimed** [SCOPE FENCE] | §0 tier 3 |
| QM-101-C6 | The threshold theorem(s) (Aharonov–Ben-Or, Knill–Laflamme–Zurek, Kitaev) | [STANDARD + citation] (imported, not re-proved) | §0.2, §2 statement |
| QM-101-C7 | THR-001: `Theta` with declared hyps `H(Theta)` induces `QCRealizationPacket(A_Theta, T_n)` via the field assignment | [DEFINITION / CONSTRUCTION — packet-population mapping] | §2 statement + table |
| QM-101-C8 | Scoped corollary: under `H(Theta)` + `p_pair(d) → 0`, residual mass drops below any fixed visibility threshold ⇒ conditional no-go does not fire; threshold theorem = repair-capacity certificate | [PROVEN, CONDITIONAL + H(Theta) + `p_pair → 0`] | §2 corollary |
| QM-101-C9 | Combinatorial repair-image monotonicity: $B\subseteq B'\Rightarrow|\{d\notin B'\}|\le|\{d\notin B\}|$ (enlarging the repair image strands no more defects) | [PROVEN — MECHANIZED axiom-free] secured ENC-1066 (`OmegaCore.QM.repair_monotone`) | §2, §4 |
| QM-101-C9b | The *rate* inequality `mu_repair ≥ lambda_proj` at scale (distinct from C9) | [OPEN / SCOPE FENCE — imported burden, never mechanized] | §2.1, §3 |
| QM-101-C10 | Worked example: `p_pair(d)=(p/p_th)^{(d+1)/2}` with `p=1e-3, p_th=1e-2` gives `1e-2,1e-3,1e-4,1e-5` for `d=3,5,7,9`; flips to growth when `p>p_th` | [WORKED EXAMPLE] | §2.1 |
| QM-101-C11 | The five imported architecture-class accounting obligations (λ<μ at scale, decoder throughput, bounded leakage/crosstalk/tails, `p_pair → 0`, accepted overhead) are imported, not derived here | [OPEN / SCOPE FENCE — imported burden] | §3 |
| QM-101-C12 | Status/Scope/Evidence/Authority: Derived+Conditional; no authority minted; only arrow into authority is CODA-FDA `Pi_sharp` | [SCOPE FENCE / DEFINITION] | §4 |
| QM-101-C13 | Falsifiability: falsified if a threshold theorem's hyps hold at target workload while `p_pair` provably fails to → 0 | [SCOPE FENCE / FALSIFIABILITY] | §5 |
| QM-101-C14 | Non-claims: no threshold theorem refuted; QC neither established nor impossible; QM not derived, no threshold theorem derived, no authority minted | [SCOPE FENCE] | §6, non-claims box |

Definition-as-theorem audit
---------------------------

**PASSED (one demotion applied in Stage 2).** THR-001's packet-population *mapping* (C3/C7) was
initially typed `[PROVEN — prose]`; Stage 2 demoted it to `[DEFINITION / CONSTRUCTION]` — the
field-by-field assignment from `H(Theta)` reads packet fields off `Theta`'s declared data and is
true by how the packet is *defined*, not a proved theorem (the QM_100/QM_081 quotient-identity
demotion precedent). The genuinely **derived** content is the §2 *scoped corollary* (C8: suppression
⇒ the conditional no-go does not fire inside the packet), correctly typed
`[PROVEN, CONDITIONAL + H(Theta) + p_pair→0]`. The imported threshold theorems (C6) are correctly
typed `[STANDARD]` and **not** presented as the paper's own results (the principal corpus trap for
this paper — verified clean). The §4 Status/Authority block (C12) is a fence/definition, not a
theorem. **No threshold theorem relabeled as a paper result; the one mapping-as-theorem inflation
was demoted.**

Conditional-no-go / authority firewall audit
--------------------------------------------

**PASSED.** Every no-go statement here is CONDITIONAL (C2/C4/C8) on the imported threshold
hypotheses and `p_pair → 0`; there is **no** unconditional / all-architecture no-go asserted —
the universal-class question is fenced OPEN as the imported burden (C11) and routed to the
shared architecture-class obligation (PL-QM003-1 / PL-QM005-1). The complementary "QC impossible"
claim is explicitly a **non-claim** (C5/C14). Authority firewall held: no authority minted,
`StructureDerived ⇏ IsAuth` stated (§4).

Support ledger (Part C — upgrade paths)
---------------------------------------

| ID | What would upgrade it | Difficulty | Lean/numerical? | Obligation |
|---|---|---|---|---|
| QM-101-C9 | **Already done** — combinatorial repair-image monotonicity is MECHANIZED axiom-free as `OmegaCore.QM.repair_monotone` (ENC-1066); no open obligation | — | LEAN4 (done) | DISCHARGED (ENC-1066, MECHANIZED axiom-free 2026-06-15) |
| QM-101-C8 | Mechanize the §2 scoped corollary (the "no-go does not fire" step) in Lean so the suppression implication is checked, not prose-proved | Medium | LEAN4 | **PL-QM015-2** (hardening; the §5 "what would strengthen it" target) |
| QM-101-C4/C11 | Discharge (or refute via a counterexample class) the architecture-class antecedent: a named realistic class meeting `H(Theta)` at human-significant scale | Hard | Prose / Numerical | **shared with PL-QM003-1 / PL-QM005-1** (the central open architecture-class question — not duplicated) |
| QM-101-C7 | Populate THR-001 for a named surface-code architecture (replayable `QCRealizationPacket` fields) so the mapping is a checked worked instance | Medium | Numerical | **shared with PL-QM003-3** (surface-code packet instantiation — not duplicated) |

**No honesty-gating open obligations.** C3/C7 (THR-001 mapping) are `[DEFINITION / CONSTRUCTION]`
(true by packet definition); the genuinely derived no-go-suppression content (C2/C4/C8) is correctly
typed CONDITIONAL; the combinatorial repair-image monotonicity (C9) is **MECHANIZED axiom-free**
(ENC-1066), while the *rate* inequality at scale (C9b) is correctly fenced OPEN/imported; the
architecture-class antecedent (C4/C11) is fenced OPEN and routed to the shared program-level
obligation. The imported threshold theorems are STANDARD, not paper results.
