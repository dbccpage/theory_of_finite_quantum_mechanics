> **Annex notice (2026-07-31, AuthorityEffect: None).**  
> Packaging annex absorbed: `qm_074_no_signaling_finite_shadow/` (no-signaling ≠ factorization LGGR — annex to finite Bell / separability paper).  
> Claim namespaces remain distinct; this is not a theorem upgrade.


# 073 Correlation Separability Finite Bell

## GTOC Foundations — Quantum Contact Series (qm_073_correlation_separability_finite_bell)

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

Paper 8 — Correlation, Separability, and Finite Bell Bounds (The Entanglement Boundary)
=======================================================================================

GTOC Foundations — Physics-Contact Extension. Composite Carriers, the Product Defect, Universal Separability of Bare Tables, the Finite CHSH Bound, and the Priced Doors to Violation

**Date:** 2026-07-17 · **Version:** v1.0 · **Series:** GTOC Foundations, Physics-Contact Extension
**Claim ledger:** [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (IDs `073:P8-C1` through `073:P8-C11`)
**Degree:** δ8 (consumes δ0–δ7; cites δ3)
**Requires:** Paper 2 (δ2: pair-families, slice-tallies via the repaired block machinery, signed counts — scalar package PL-GTOC-12), Paper 3 (δ3: exchange characters, K9-conditional), Paper 6 (δ6: the product-defect surrogate, §6.2 there), Paper 7 (δ7: bit-shadows; the Q1–Q4 price list). Corpus floor: QM_070 (ENC-1123, mechanized), QM_071 (ENC-1124, mechanized), QM_120 (ENC-1143, mechanized).
**Main claim:** composite carriers and their joint weight tables are δ2/δ8-derivable, and on them three exact results hold. **(1) The product defect is derived and per-exhibition checkable** — $\delta_{\mathrm{prod}}(a,b) = w(a,b) - w_A(a)w_B(b)/W$ with $\ell^1$ mass $\Phi$, and $\Phi = 0 \Leftrightarrow$ factorization is the corpus's mechanized theorem (QM_070) *at exactly this series' scalar grade* — but, per the external review's firewall and QM_070's own fence, **the product defect is correlation, not entanglement**. **(2) Universal separability of bare tables (theorem):** every exhibited normalized nonnegative joint table is a convex combination of point product tables — so at the unrestricted bare-table grade *nothing is entangled*: the separability obstruction relative to the full exhibited point-product family is **empty**, and entanglement proper is definable only *relative to a declared restricted product family* (QM_071's soundness machinery, adopted) or on richer carriers behind the Q1/Q2 imports. The classically famous fact that a Bell-state descent and a classical mixture share the table $(\tfrac12, 0, 0, \tfrac12)$ is exhibited as the witness. **(3) The finite CHSH bound (theorem):** for exhibited weight families over joint assignments of four sign-valued windows, the CHSH combination of correlators lies in $[-2, +2]$ — an $\ell^1$, rational-arithmetic, per-exhibition theorem. The violation doors are each priced: dropping the single-global-joint-table hypothesis (the LGGR/no-global-section structure, whose parity core is mechanized in QM_120), the phase/ℓ² imports (Q1/Q2 — with the *value* $2\sqrt2$ R2a-cheap but the *structure* attaining it Q-priced), and the declared tensor-composition rule. Bell's theorem proper (locality, measurement independence, continuum observables) is obstructed clause by clause. Under the alternating exchange character, **diagonal suppression** is derived (a $\mathrm{char} \neq 2$ cancellation fact); full antisymmetrized entanglement structure is a Q1 import.
**Non-claim:** no entanglement is derived (the review's firewall is enforced, not evaded); no quantum nonlocality, no hidden-variable refutation, no Tsirelson bound, no LOCC theory, no monogamy; no claim that any physical system realizes any object here. Registered in §6.
**Authority:** none.
**State note (binding).** Authored against the post-2026-07-14-verdict, post-2026-07-15-review state of Papers 0–7 (all conditionalities inherited; slice-tallies and products consume the *repaired* cancellation machinery of Paper 2 §3.3 throughout).

**Retention inheritance note.** Composite carriers and joint tables are built only from retained carriers with exhibited weights. A flicker does not become a zero row in a joint table, a product defect, or an entanglement candidate. If a component leaves no retained witness slot, this paper has no factor to compose.

Abstract

This paper derives finite composite tables, marginals, a product-defect diagnostic, universal separability of unrestricted bare tables, and the classical CHSH bound under one global joint table. The results enforce rather than bypass the entanglement firewall: tensor composition, restricted product families, quantum amplitudes, Tsirelson structure, locality, measurement independence, and physical realization remain declared, imported, or obstructed.


§1 — The problem, stated exactly, and the firewall adopted

The goal prompt asks whether non-factorizability can be derived and whether $\ell^1$ alone yields a Bell-type bound. The external review (2026-07-15) adds a binding firewall: *entanglement must remain distinct from generic obstruction, compositional inconsistency, contextuality, and mutual information* — "a nonzero generic compositional residual is broader than entanglement," and the corpus already records the direction: entanglement implies its compositional-inconsistency diagnostic, the converse fails. The corpus floor is exact here and this paper builds on it rather than beside it: QM_070 derives the product defect on $\mathbb{Q}_{\ge 0}$ tables and *fences it as not-entanglement*; QM_071 derives separability-witness *soundness* relative to a declared finite product family and fences everything else. Both are mechanized at precisely the scalar grade this series has earned. What this paper adds from below: the carriers themselves (δ2 pair-families — the tables are now *derived objects*, not declared inputs), the universal-separability theorem that explains *why* the firewall is mandatory at this grade (§3), the finite CHSH bound as an $\ell^1$ theorem (§4), the priced violation doors (§5), and the exchange-character connection (§5.4).

### Import Ledger — §1

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| product defect, $\Phi$ | δ8 (from δ2 parts) | §2; corpus theorem QM_070 (ENC-1123, MECHANIZED) cited | — |
| entanglement (the word) | — | — | firewalled: not the product defect; disposition §3 |
| separability witness soundness | δ3-grade corpus result | QM_071 (ENC-1124, MECHANIZED) cited | relative to DECLARED finite product family — inherited fence |

Connective audit: clean.


### Genesis-Bias Fence — No Prior Entangled State-Space

This paper does not begin with entanglement, quantum state-space, tensor products, hidden variables, locality, measurement settings, nonlocality, physical subsystems, or a space of possible outcomes. It begins with exhibited pair-configurations, joint weight tables, declared product families, and finite sign-valued windows.

A **composite carrier** is not a tensor product and not a physical composite system. It is an exhibited pair-configuration. Tensor composition is a separate declared rule and remains an import.

A **joint table** is not a probability distribution over possible hidden states. It is an exhibited nonnegative weight family over displayed joint assignments. Its normalized ratios remain finite weight proportions, not chance semantics.

The **product defect** is correlation, not entanglement. A nonzero defect says the exhibited table fails product factorization. It does not certify quantum entanglement.

**Separability** at the bare-table grade is arithmetic: every exhibited normalized table decomposes into point product tables. Entanglement becomes a contentful verdict only relative to a declared restricted product family or after richer Q-imports are paid.

The **finite CHSH bound** is a theorem about one exhibited joint table over four sign-valued windows. It is not Bell’s theorem about nature. If only pairwise tables are exhibited, the joint-table theorem does not apply.

“Locality,” “measurement independence,” “spacelike separation,” “settings,” “hidden variables,” “Tsirelson bound,” and “quantum violation” are not derived vocabulary here. Each belongs to a priced physical or quantum realization branch.

> **GENESIS-BIAS AUDIT.** Does this section explain entanglement, Bell violation, separability, locality, or quantum composition by presupposing a prior tensor-product state-space, hidden-variable sample space, physical subsystem split, spatial separation, measurement-choice domain, probability space, or quantum amplitude structure? If so, declare and price that antecedent, replace it with exhibited table / product-family / joint-window data, or stop with an OBSTRUCTION.


§2 — Composite carriers and the product defect, from below

**2.1 Composite carrier.** For exhibited carriers with locus families $A$ and $B$, the **composite carrier** has as loci the exhibited pair-family $A \times B$ (Paper 2 §3.2's product construction — the Cartesian pair-former of the declared scalar-construction package, flag inherited) with cuts induced per-exhibition. No tensor product is invoked: the composite is a pair-*configuration*, and the difference between pair-formation (δ2, combinatorial) and tensor composition (a declared linear-structure rule — priced at §5.3) is load-bearing.

**2.2 Joint weight tables, marginals.** A **joint table** is an exhibited weight assignment $w : A \times B \to$ derived scalars $\ge 0$ with total $W = \sum_{a,b} w(a,b) > 0$ (δ2 additivity; normalization per Paper 2 §5.3's finite weight normalization). **Marginals** are slice-tallies: $w_A(a) = \sum_b w(a,b)$, $w_B(b) = \sum_a w(a,b)$ — per-exhibition sums over exhibited slices, governed by the repaired block machinery (Paper 2 §3.3). The review's requirement for even *speaking* of mutual dependence — "a joint carrier and marginalization" — is thereby met from below, as derived objects. [PROVEN, CONDITIONAL on the scalar package]

**2.3 Product defect.** Define $\delta_{\mathrm{prod}}(a,b) := w(a,b) - w_A(a)\,w_B(b)/W$ and $\Phi(w) := \sum_{a,b} |\delta_{\mathrm{prod}}(a,b)|$ — the $\ell^1$ product-defect mass. The corpus's mechanized theorem holds verbatim at this grade: $\Phi(w) = 0 \Leftrightarrow w(a,b) = w_A(a) w_B(b)/W$ for all $(a,b)$ (QM_070, `Phi_zero_iff_factors`). Non-factorizability is thus **a per-exhibition checkable obstruction** — the brief's demand, discharged — and it is **correlation**: the δ8 refinement of Paper 6 §6.2's mutual-dependence surrogate. What it is not, the next section proves.

### Import Ledger — §2

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| composite carrier (pair-configuration) | δ8 | §2.1 (δ2 pair-former) | scalar package flag inherited; tensor composition NOT used — priced §5.3 |
| joint table, marginals (slice-tallies) | δ8 | §2.2 | conditional on scalar package (PL-GTOC-12) |
| $\delta_{\mathrm{prod}}$, $\Phi$; $\Phi = 0 \Leftrightarrow$ factorization | δ8 | §2.3; QM_070 MECHANIZED | — |
| correlation (= product defect) | δ8 | §2.3 | firewalled from "entanglement" — §3 |

Connective audit: exposition-order occurrences are presentation artifacts, flagged per the charter's standing clause; none load-bearing.


§3 — Universal separability of bare tables: why the firewall is a theorem, not a scruple

**3.1 Mixtures and separability.** A **product table** is one with $\Phi = 0$. A table is **$P$-separable** (QM_071's object, from below) when it is an exhibited convex combination $w = \sum_k \lambda_k P_k$ ($\lambda_k \ge 0$ derived scalars, $\sum_k \lambda_k = 1$) of tables from a declared family $P$ of product tables. Entanglement-relative-to-$P$ is non-membership in the exhibited hull — and QM_071's witness-soundness theorem (a separating functional certifies non-membership) is adopted as the corpus's mechanized tool, with its operational rule inherited: *neither decomposition nor witness exhibited ⇒ verdict `open`/`refused`, never "entangled by default."*

**3.2 Theorem (universal separability of bare tables).** Every exhibited normalized joint table is a convex combination of **point product tables**. “Deterministic” is only the external probability-theory name for point support; no hidden variable or causal determination is meant. *Proof.* For each exhibited pair $(a,b)$ with $w(a,b) > 0$, the point table $e_{(a,b)}$ (weight $1$ at $(a,b)$, zero — the negative diagnostic — elsewhere) is a product table: its marginals are point marginals and $e_{(a,b)}(x,y) = e_a(x)\,e_b(y)$ per-exhibition. Then $w = \sum_{(a,b)} \big(w(a,b)/W\big)\, e_{(a,b)}$ — an exhibited convex combination with derived-scalar coefficients. $\blacksquare$ [PROVEN, per-exhibition, CONDITIONAL on the scalar package]

**Consequence, stated exactly.** Relative to the full exhibited point-product family generated by the displayed support of the table, the separability obstruction is **empty at the bare-table grade**: $\Phi > 0$ (correlation) never certifies entanglement, because every table — however correlated — decomposes classically. The firewall the review demands is therefore not caution but arithmetic: *at the unrestricted bare-table grade, "entangled" has no nonempty extension*. Entanglement becomes a contentful diagnosis only (i) **relative to a declared restricted family $P$** (then non-membership in $\operatorname{conv}(P)$ is checkable and witness-certifiable — QM_071, machinery adopted), or (ii) **on richer carriers** carrying coherence coordinates — which cost exactly Paper 7's Q1/Q2 imports.

**3.3 The witness pair, exhibited.** The table $w = (\tfrac12, 0, 0, \tfrac12)$ on $\{0,1\} \times \{0,1\}$: marginals uniform, product prediction $\tfrac14$ everywhere, $\delta_{\mathrm{prod}} = \pm\tfrac14$, $\Phi = 1 > 0$ — correlated. Yet $w = \tfrac12 e_{(0,0)} + \tfrac12 e_{(1,1)}$ — separable by §3.2's recipe. And per QM_070's descent fence, the *same* table is the phase-blind shadow of both a classical mixture and a Bell state: the coordinates that would distinguish them are discarded by the descent. Correlation without entanglement, and quantum entanglement invisible at this grade — one exhibit, both morals. [WORKED EXAMPLE]

### Import Ledger — §3

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| convex mixture, $P$-separability, hull membership | δ8 | §3.1 (from δ2 scalars); QM_071 machinery adopted | $P$ DECLARED — inherited fence; verdicts open/refused, never default |
| **universal separability of bare tables** | δ8 | **Theorem 3.2** | [PROVEN, CONDITIONAL scalar package]; Lean target PL-GTOC-19 |
| emptiness of full-family entanglement at table grade | δ8 | §3.2 Consequence | the review's firewall, upgraded to arithmetic |
| Bell-vs-mixture invisibility | δ8 | §3.3 (QM_070 descent fence cited) | [WORKED EXAMPLE]; phase coordinates IMPORTED if restored |

Connective audit: "classically" names the derived mixture recipe, not a physics; §3.3 *would* ("the coordinates that would distinguish them") names discarded-coordinate content under the QM_070 descent fence, not a modality; *then* in §3.2 is conditional dependence-tracking (licensed); the §1-quoted "must" is mention, not use.


§4 — The finite CHSH bound: an ℓ¹ theorem

**4.1 Setting (four sign-valued windows, one joint assignment family).** Exhibit four sign-valued readouts (δ1 sign object × declared windows, Paper 6 §3): the $A$-coordinate windows $a_0,a_1$ and the $B$-coordinate windows $b_0,b_1$, each valued in $\{+1, -1\}$ (derived signed scalars — package flag). A **joint assignment** is an exhibited assignment of all four values at once; a **single-global-joint-table model** is an exhibited weight family $\{w_s\}$ over joint assignments (nonnegative — load-bearing for the convexity step — and normalized, derived scalars). This is the finite table-form of what Bell literature later reads as a local hidden-variable model, but no locality or hidden-variable ontology is derived here. Correlators are ratio-valued: $E(i,j) = \sum_s w_s\, a_i(s)\, b_j(s) / W$.

**4.2 Theorem (finite CHSH).** For every exhibited single-global-joint-table model,

$$-2 \;\le\; E(0,0) + E(0,1) + E(1,0) - E(1,1) \;\le\; +2.$$

*Proof.* Per joint assignment $s$: $a_0(b_0 + b_1) + a_1(b_0 - b_1)$ — one bracket is $\pm 2$, the other is the zero diagnostic, so the combination is $\pm 2$ (finite case table over the four sign choices of $b_0, b_1$, each side by K1's exhaustive dichotomy on the sign object). The correlator combination is the $w$-weighted average of these per-assignment values; a normalized nonnegative-weighted average of values in $\{+2, -2\}$ lies in $[-2, +2]$ (derived-scalar arithmetic: convexity as exhibited inequality-bookkeeping). $\blacksquare$ [PROVEN, per-exhibition, CONDITIONAL on the scalar package; Lean target PL-GTOC-19]

**The answer to the brief's key question:** yes — $\ell^1$ alone (weights, signs, normalization; nothing quadratic, nothing complex) produces the Bell-type bound. The bound is a facet of the exhibited correlation polytope, reached with rational arithmetic.

**4.3 The load-bearing hypothesis, named.** The theorem's strength is its hypothesis: **one exhibited weight family over *joint* assignments of all four windows.** That is the finite form of "local hidden variables + measurement independence" — and it is *structural*, not metaphysical: it says the four windows' statistics are marginals of a single exhibited table. Where no such joint table is exhibited, the bound is not derived — and *that* situation has a name in this corpus: local-green-global-red, the no-global-section structure whose parity core is exactly QM_120's mechanized obstruction (each context satisfiable, no global assignment). The distance between "four windows, jointly tabled" and "four windows, only pairwise tabled" is the entire content of the bound.

### Import Ledger — §4

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| sign-valued windows; joint assignment; single-global-joint-table model | δ8 | §4.1 (δ1 signs + δ6 windows + δ2 weights) | scalar package flag |
| correlators $E(i,j)$ | δ8 | §4.1 | ratio-valued — conditional |
| **finite CHSH bound** | δ8 | **Theorem 4.2** | [PROVEN, per-exhibition]; PL-GTOC-19 |
| single-global-joint-table hypothesis | δ8 | §4.3 (named, load-bearing) | its failure = LGGR structure (QM_120 parity core MECHANIZED) — cited |

Connective audit: clean; "average" is exhibited weighted-sum bookkeeping.


§5 — The violation doors and the exchange connection, each priced

**5.1 Door V1 — drop the joint table (contextual/no-global-section route; corrected 2026-07-15).** Exhibit the four windows with only *pairwise* tables, no joint one. Then §4.2 does not apply — and, the second pass corrects the first draft here, **the derived layer already exhibits CHSH-bound-exceeding pairwise families, no quantum import needed**: take the three tables $(\tfrac12, 0, 0, \tfrac12)$ on $(a_0,b_0), (a_0,b_1), (a_1,b_0)$ and $(0, \tfrac12, \tfrac12, 0)$ on $(a_1,b_1)$ — each a §2.2 normalized joint table on derived scalars — giving $S = 1 + 1 + 1 - (-1) = 4$, the parity/PR-box facet (“PR-box” is an external name for the displayed pairwise-table pattern; no physical box, no non-signalling principle, and no operational theory is imported), with no joint extension by a finite parity check (the three perfect correlations force agreement on the support; the anticorrelation contradicts it — exactly QM_120's LGGR shape, whose parity core is mechanized). The first draft's sentence "nothing at δ8 produces pairwise tables violating the bound" is **withdrawn as false**; what is true, and now stated exactly: Theorem 4.2 constrains *jointly-tabled* families only; exhibited pairwise families without joint extension exceed the single-global-joint-table bound freely up to $|S| = 4$; and what costs Q1/Q2 is the **specific quantum shape** — pairwise tables that fail the joint-table-bound facet while respecting the Tsirelson ceiling $|S| \le 2\sqrt2$ (§5.2), plus their physical realization. The door's derived content is thus *larger* than the first draft claimed, and the bound's content correspondingly sharper: everything is in the joint-table hypothesis.

**5.2 Door V2 — phase/ℓ² and the quantum CHSH violation (the Tsirelson route).** The quantum violation of the finite CHSH bound requires a specific and heavy price list to be paid:

1. Complex amplitude carrier (Q1)
2. Tensor composition (declaring the linear rule for composites, V3)
3. An entangled state vector (a non-separable vector in the tensor product)
4. Incompatible local effects (non-commuting observables for each side)
5. Born pairing (yielding probabilities that form the pairwise tables)

Only after all these structural imports are paid do pairwise tables reaching $|S| = 2\sqrt2$ become available. Split price, per the repaired R2 stratification: the *value* $2\sqrt2$ is R2a-cheap (a quadratic irrational — one algebraic extension); the *structure* that attains it is the heavy quantum import list above. Additional operator inequalities give the Tsirelson ceiling. No Tsirelson bound is derived here in either direction — the ceiling $2\sqrt2$ is quantum-imported mathematics, cited as the door's far wall, not established.

**5.3 Door V3 — tensor composition (the categorical import).** The composite carrier of §2.1 is a pair-configuration; quantum composition is a *declared linear rule* — state spaces compose by tensor product, with entangled vectors exactly the non-product elements the rule creates. The import is the rule itself: nothing in pair-formation forces linear composition, and the QM-series' representation-transport discipline (`cosmology/qm_looping_goal_prompt.md`'s audit) governs any attempt to carry structure across that declaration. Declaring the rule buys the very *object* whose absence §3.2 proved: a composite with more admissible "states" than mixtures of products.

**5.4 The exchange connection — diagonal suppression derived, antisymmetrization priced.** Under the alternating character on a K9-saturated pair (Paper 3 §4.4; Paper 7 §3), let a weight contribution sit at a transposition-fixed pair-locus (a diagonal locus $(x,x)$ of the composite), and let the signed weight assignment be **exchange-equivariant** (the K10 condition, stated as the transport hypothesis: the assignment's transported value along an exchange is its value at the image locus — the signed analogue of Paper 2 §4.2's declared equivariance; this hypothesis is load-bearing and named). Transport along the transposition multiplies the contribution by $\chi(\tau) = -1$ while fixing its locus; equivariance identifies the transported value with the value in place, so coherence forces $c = -c$, hence $2c = 0$, hence $c = 0$ — the step from $2c = 0$ to $c = 0$ uses the derived scalars being an **integral domain** with $+1 \neq -1$ (P2 §3.3, facts (i) *and* (iii) jointly, package flag; char $\neq 2$ alone does not suffice in a general ring — $\mathbb{Z}/4$ is the standing countermodel). **Diagonal suppression under the alternating character is a theorem** [PROVEN, CONDITIONAL: H1–H3, K9, K10-equivariance of the signed assignment, PL-GTOC-12]: sign-twisted transport tolerates no weight on exchange-fixed diagonal loci. That is the derived kernel of "antisymmetrization excludes double occupancy." The *full* Fermi entanglement structure — Slater-determinant states, antisymmetrized amplitudes — is Q1-imported (amplitudes first, then the sign-twist acts on them); the symmetric character imposes no such suppression, and *that asymmetry between the characters is itself derived*. [Physics reading [INTERPRETIVE], fenced; M13 stands]

**5.5 Bell's theorem proper, clause by clause.**

> **OBSTRUCTION.** The following cannot be derived from what is available at this degree: Bell's theorem as a statement about nature. What would have to be admitted, clause by clause: **locality** — spatial separation of the $A$-coordinate and $B$-coordinate windows (space is not derived, Paper 0 §8.7; coordinates here are pair-coordinates, not places); **measurement independence / free choice** — settings uncorrelated with the model's weights (a counterfactual-independence posit: modality, Paper 0 §8.5); **continuum observables and quantum statistics** — the Q1/Q2/Q4 imports plus empirical input. What is lost if admitted: the finite-diagnostic character of the calculus, and the per-exhibition semantics of §4's bound — which would become a claim about unperformed experiments (chance semantics, obstructed at Paper 2 §7.3).

### Import Ledger — §5

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| no-joint-table door (V1); LGGR shape | δ8 / parity grade | §5.1; QM_120 cited (MECHANIZED core) | quantum pairwise tables IMPORTED (Q1/Q2) |
| Tsirelson route (V2); $2\sqrt2$ | — | §5.2 | value R2a-cheap; attaining structure Q1+Q2 (+Q4); ceiling itself NOT derived — cited as imported mathematics |
| tensor composition rule (V3) | — | §5.3 | DECLARED/IMPORTED — categorical import; representation-transport audit governs |
| diagonal suppression under $\mathrm{sgn}$ | δ8 | **§5.4 theorem** | [PROVEN, CONDITIONAL H1–H3/K9/K10-equivariance/PL-GTOC-12 — integral-domain + char≠2 jointly]; Lean target PL-GTOC-20 (corrected statement) |
| antisymmetrized states, Slater structure | — | — | IMPORTED (Q1 + sign-twist); M13 stands |
| Bell's theorem (nature-claim) | — | — | **OBSTRUCTION** §5.5 — three clauses priced |

Connective audit: "walks through," "far wall" are price-list register; modal verbs confined to obstruction/pricing blocks.


§6 — Claim ledger, falsifiability, boundary

**6.1 Claim Ledger.**

| ID | Claim (location) | Type | Basis / notes |
|---|---|---|---|
| P8-C1 | Composite carriers, joint tables, marginals derivable from below (§2.1–2.2) | [PROVEN, CONDITIONAL] | scalar package (PL-GTOC-12); repaired block machinery |
| P8-C2 | Product defect + factorization criterion at the derived grade (§2.3) | [STANDARD within corpus] | QM_070/ENC-1123 mechanized; carriers now derived, not declared |
| P8-C3 | **Universal separability of bare tables** (§3.2) | [PROVEN, CONDITIONAL] | point-table decomposition; PL-GTOC-19 |
| P8-C4 | Emptiness of full-family entanglement at table grade; firewall = arithmetic (§3.2–3.3) | [PROVEN, CONDITIONAL] | consequence of P8-C3 + QM_070 descent fence |
| P8-C5 | Relative entanglement machinery adopted (declared $P$; witness soundness; open/refused verdicts) (§3.1) | [STANDARD within corpus] | QM_071/ENC-1124 mechanized; fences inherited |
| P8-C6 | **Finite CHSH bound** (§4.2) | [PROVEN, CONDITIONAL] | per-assignment $\pm2$ + convex bookkeeping; PL-GTOC-19 |
| P8-C7 | Load-bearing hypothesis = single global joint table; its failure exhibited at the derived grade (PR-box facet, $S = 4$, no joint extension) = LGGR shape (§4.3, §5.1) | [PROVEN, CONDITIONAL] + [STANDARD within corpus] | H: scalar package (the exhibited tables); QM_120 parity core cited (mechanized); first-draft "δ8 supplies no violating pairwise tables" withdrawn |
| P8-C8 | Violation doors V1–V3 priced (§5.1–5.3) | `OPEN` here + [STANDARD] citations | R2a/R2b split applied; Tsirelson ceiling not derived |
| P8-C9 | **Diagonal suppression under the alternating character** (§5.4) | [PROVEN, CONDITIONAL] | char ≠ 2 cancellation; H1–H3/K9/K10-equivariance/PL-GTOC-12; PL-GTOC-20 |
| P8-C10 | Bell's theorem obstructed clause by clause (§5.5) | `OPEN` | obstruction block; three named admissions |
| P8-C11 | Physics readings (occupancy, nonlocality, nature-claims) | [INTERPRETIVE] | fenced throughout; M13 stands |

**6.2 Falsifiability.** This paper fails if: (a) an exhibited normalized table is produced admitting no point-product decomposition (refuting Theorem 3.2 — a finite check); (b) an exhibited single-global-joint-table model violates the CHSH bound (refuting Theorem 4.2 — finite arithmetic); (c) a nonzero weight survives at a transposition-fixed locus under coherent $\mathrm{sgn}$-transport with a K10-equivariant signed assignment over integral-domain scalars with $\mathrm{char} \neq 2$ (refuting §5.4 with all its hypotheses in force); (d) entanglement is derived at the bare-table grade without a declared restriction or Q-import (P8-C4 falls — and with it the review's firewall would need re-audit); (e) any of the cited mechanized results (ENC-1123/1124/1143) fails its stated statement on re-verification.

**6.3 What this paper does NOT claim.** No entanglement derived; no nonlocality; no hidden-variable refutation; no Tsirelson bound; no monogamy, LOCC, or entanglement measures; no Fock/CCR/CAR (M13); no claim about spacelike separation, experiments, or nature. No authority — a table, a bound, a suppression lemma license nothing.

**6.4 New proof obligations** (recorded in `omega_engine/research/encyclopedia/proof_ledger_20260715.md`):

* **PL-GTOC-19 (LEAN4 — the extension's central mechanization target):** (i) universal separability: every normalized $w : A \times B \to \mathbb{Q}_{\ge 0}$ is a convex combination of point product tables (finite decomposition, constructive); (ii) finite CHSH: for weights over joint sign assignments, $|E(0,0)+E(0,1)+E(1,0)-E(1,1)| \le 2$ (per-assignment case split + weighted-average bound). Both `Finset`-sum arithmetic over `ℚ`; sits beside `QM/ProductNonFactorization.lean`.
* **PL-GTOC-20 (LEAN4, not-gating-honesty; statement corrected 2026-07-15 second pass):** in an **integral domain of characteristic $\neq 2$** (or any commutative ring in which $2$ is a non-zero-divisor): $c = -c \Rightarrow c = 0$ — the first-pass form "commutative ring with $2 \neq 0$" is false ($c = 2$ in $\mathbb{Z}/4$); packaged with the transposition-fixed-locus reading under K10-equivariance (mechanizing §5.4's kernel, which cites P2 §3.3(i) and (iii) jointly).

**6.5 Why this matters.** The two commonest category errors about entanglement are both dissolved here by theorems rather than warnings: (1) "correlation is entanglement" — refuted at the ground by universal separability (§3.2): *no* bare table is entangled, however correlated, so any entanglement diagnosis is either family-relative (declared, witnessable — QM_071) or import-bearing (Q1/Q2); and (2) "Bell violations refute classical probability" — located exactly: what the folklore calls classical probability — here, derived ℓ¹ proportions on exhibited tables ("probability" itself stays reserved, per Paper 2) — *derives* the CHSH bound (§4.2) from one structural hypothesis (a single global joint table), the derived layer itself exceeds the bound the moment that hypothesis is dropped (§5.1, up to the PR-box facet), and the *quantum-shaped* joint-table-bound failures are named imports (§5.2). The exchange connection adds the least-known item: the Fermi/Bose asymmetry already acts at the composite-table grade as a derived suppression law (§5.4), before any amplitude exists. The deliverable is the extension's boundary stone: everything Bell-flavored that is finite and ℓ¹ is a theorem below; everything genuinely quantum is one of the priced doors above.

**6.6 Nearest neighbors (external positioning).** [Positioning [INTERPRETIVE]; citations [VERIFY].]

* **Bell / CHSH** (Bell 1964; Clauser–Horne–Shimony–Holt 1969; Fine 1982 [VERIFY]): the bound and its joint-distribution equivalence. Theorem 4.2 is Fine's-theorem-adjacent finite content — deliberately only the classical-side facet, with no experiment, no nature-claim, and the joint-table hypothesis named as the whole story (§4.3).
* **Correlation polytopes** (Pitowsky, *Quantum Probability–Quantum Logic*, 1989 [VERIFY]): Bell inequalities as facets of finite polytopes. Nearest mathematical neighbor of §4; this paper is narrower — per-exhibition, rational-scalar, no polytope *totality* comprehended (the hull is exhibited combination by combination).
* **Entanglement witnesses** (Horodecki×3 1996; Terhal 2000; Gühne–Tóth 2009 [VERIFY]): separating functionals certify non-separability. Adopted from QM_071 in its mechanized, declared-family, soundness-only form; completeness (Hahn–Banach) stays imported there and untouched here.
* **Werner states / separability subtleties** (Werner 1989 [VERIFY]): entangled states admitting local models — the quantum-side warning that entanglement ≠ Bell violation. Mirrored here from below: correlation ≠ entanglement (§3), bound-satisfaction ≠ classicality-of-source (§5.1). The two firewalls compose.
* **Pauli exclusion / antisymmetrization** (standard [VERIFY]): §5.4 derives only the diagonal-suppression kernel at the transport level; occupancy, spin, and field structure are all imported past it.

In each case the direction is the same: this paper claims *less*, and states exactly what the neighbor adds.

### Import Ledger — §6 (consolidated, paper-level)

| Term used | Degree first available | Where derived | Or: IMPORTED — flag |
|---|---|---|---|
| composite carriers, joint tables, marginals, product defect, universal separability, finite CHSH, diagonal suppression | δ8 | §2–§5 | conditional on inherited packages (PL-GTOC-12; H1–H3/K9 where exchange enters); no new conventions at δ8 |
| entanglement (absolute), Tsirelson, tensor rule, Bell-as-nature | — | — | OBSTRUCTED / IMPORTED / DECLARED — every door priced (§3, §5); none taken |
| mechanized corpus floor | — | QM_070/020/029 cited | ENC-1123/1124/1143 — statements used as stated, nothing extended |

Connective audit (paper-level): per-exhibition discipline in every universal and every hull; *violation/door/wall* are price-list register; no chance semantics anywhere ($E(i,j)$ is a ratio of exhibited weights; the word "model" names an exhibited table family, not a hypothesis about nature).


Post-paper protocol (per the charter failure protocol and `../../001_gtoc_gtla/999_gtoc/theorem_ledger.md` §5)

**Degree index row (for the charter):**

| Degree | Paper | What becomes available |
|---|---|---|
| δ8 | Paper 8 | composite carriers as pair-configurations; joint tables and marginals from below; the product defect at the derived grade (corpus-mechanized criterion); universal separability of bare tables (theorem — the entanglement firewall as arithmetic); relative entanglement machinery (declared family, witness soundness, open/refused verdicts); the finite CHSH bound (theorem); the three violation doors priced; diagonal suppression under the alternating character (theorem); Bell's theorem obstructed clause by clause |

**What this paper supports:** correlation diagnostics on derived tables; family-relative entanglement verdicts with witnesses; the classical Bell facet as finite arithmetic; the exchange-character suppression law.
**What it does not support:** any absolute entanglement claim, any quantum violation, any nature-claim.
**Narrowest defensible claim:** every exhibited normalized joint table decomposes into point product tables, and every exhibited weight family over joint sign-assignments satisfies $|S| \le 2$.
**Next test needed:** mechanize PL-GTOC-19 (the extension's central target); then the consolidated import price list and the tower-contact capstone.

Changelog

* **2026-07-15 (second pass) — adversary-workflow repairs.** (i) **Door V1 inverted** (§5.1): the first draft's "nothing at δ8 produces bound-violating pairwise tables" was false — the PR-box family ($S = 4$, no joint extension, all derived-scalar tables) is exhibited in place; the door's derived content enlarged, the joint-table hypothesis thereby shown to carry the bound's *entire* content, and Q1/Q2 repriced as buying the quantum *shape* (Tsirelson-respecting violations), not violation per se; P8-C7 retagged. (ii) **PL-GTOC-20 corrected** (§5.4, §6.4, dated ledger): "commutative ring with $2 \neq 0$" is false ($\mathbb{Z}/4$); restated for integral domains char $\neq 2$ / 2-non-zero-divisor rings, with §5.4 citing P2 §3.3(i)+(iii) jointly. (iii) Minors: local-model nonnegativity made explicit (§4.1, load-bearing for convexity); §6.2(c) restated with all §5.4 hypotheses; "classical probability" fenced to derived proportions in §6.5 (the word stays reserved).
* **2026-07-15 — first draft (v0.1).** Authored as Paper 8, closing the Physics-Contact Extension's derivational ladder. The review's entanglement firewall enforced as a theorem (universal separability, §3.2) rather than a scruple; the brief's Bell question answered positively at the ℓ¹ grade (finite CHSH, §4.2) with the joint-table hypothesis named as the entire content; violation doors priced under the repaired R2a/R2b split; diagonal suppression derived as the exchange connection; Bell-as-nature obstructed clause by clause. Corpus floor (QM_070/020/029) cited at its mechanized statements only. New obligations PL-GTOC-19/20 opened in `encyclopedia/proof_ledger_20260715.md`.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `P8-C1` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C1`) |
| `P8-C2` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C2`) |
| `P8-C3` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C3`) |
| `P8-C4` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C4`) |
| `P8-C5` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C5`) |
| `P8-C6` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C6`) |
| `P8-C7` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C7`) |
| `P8-C8` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C8`) |
| `P8-C9` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C9`) |
| `P8-C10` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C10`) |
| `P8-C11` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `073:P8-C11`) |

<!-- claim-id-body-index:end -->
