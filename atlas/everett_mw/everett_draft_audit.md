# Audit of the DeepSeek draft "Double Slit → Schrödinger → Everett: Math Only"

Checked 2026-11-02 against `everett_from_weights_math_only.md` (numerical checks in `check_everett.py`). Verdicts: **OK** (keep), **FIX** (true with a stated restriction), **WRONG** (do not keep as stated).

| § | DeepSeek claim | Verdict | What to do |
|---|---|---|---|
| 1 | $p_{12}=p_1+p_2$ cannot give zeros where $p_1,p_2>0$; "L1 is false" | **OK** | Keep. Same content as our (2.4): non-negative weights cannot cancel. (Our "no descent" is the sharper form: no *function* of the weights gives the readout.) |
| 2 | $p_{12}=p_1+p_2+2\sqrt{p_1p_2}\cos(\varphi_1-\varphi_2)$ | **OK** | Keep; identical to our (2.3). |
| 2 | "Why $\mathbb C$": continuous fringe shift $\Rightarrow$ $S^1$ $\Rightarrow$ only $\mathbb R[x]/(x^2+1)$ qualifies | **WRONG as a derivation** | Fringes with continuous shift also exist in real-amplitude QM (complex $\mathbb C^n$ is real $\mathbb R^{2n}$ with an operator $J$, $J^2=-1$; Stueckelberg 1960). The algebra fact (only $\sigma=-1$ gives a field with a positive-definite multiplicative norm) is true but does not follow from the double slit. Complex amplitudes are an **import**. The experimental case against real QM is Renou et al., Nature 600, 625 (2021), and it needs a network Bell test plus an independent-sources assumption, not a double slit. |
| 2 | "$[\hat x,\hat p]=i\hbar$ has no real representation" | **WRONG** | The CCR has no finite-dimensional representation over any field (trace argument), and has infinite-dimensional real representations via realification. Not an argument for $\mathbb C$. Drop. |
| 3 | $\frac{d}{dt}\langle\psi|\psi\rangle=0\Rightarrow U^\dagger U=1$ | **FIX** | Needs **linearity** of $U$ first (a norm-preserving nonlinear map is not unitary). Linearity is the superposition postulate, an import; or Wigner's theorem (transition probabilities preserved $\Rightarrow$ unitary or antiunitary) plus continuity to exclude antiunitary. |
| 3 | Stone $\Rightarrow$ $i\hbar\partial_t\psi=H\psi$; "not an independent postulate" | **FIX** | Stone needs the one-parameter **group law** $U(t+s)=U(t)U(s)$ (time-homogeneity) and strong continuity. Correct statement: Schrödinger is the infinitesimal form of *linear + norm-preserving + continuous group*; two of those three are imports. |
| 3 aside | Cayley step $U=(I-A)(I+A)^{-1}$, $A^\dagger=-A$, is exactly unitary; Euler $I-A$ gives $\|\psi\|^2+\|A\psi\|^2$ | **OK** | Verified numerically ($U^\dagger U=I$ to machine precision; Euler identity exact). Over $\mathbb Q(i)$ the entries stay rational since $I+A$ is invertible for skew-Hermitian $A$. |
| 4 | Unitary measurement coupling; "no collapse term in the equation" | **OK** | Keep; identical to our (4.1). |
| 5 | $\rho_A=\operatorname{Tr}_B|\Psi\rangle\langle\Psi|$, diagonal when $\langle D_0|D_1\rangle=0$ | **OK** | Keep; our (3.2), (3.5). |
| 5 | "diagonal $\rho_A\equiv$ collapsed $\rho_A$ **for all observables**" | **FIX** | True only for observables on $A$ **alone**. A joint observable on $A\otimes B$ distinguishes them: our (3.6), $\langle\Psi_\varphi|P_{\Psi_0}|\Psi_\varphi\rangle=(1+\cos\varphi)/2$ while $\rho_A=I/2$ for all $\varphi$. DeepSeek's own next sentence ("they moved into the apparatus records") already says this; the box overstates it. |
| 6 | $P_{\text{Born}}(\gamma)=w_\gamma/W$ for any phases; "Born normalization is a redundant encoding" | **OK (tautology)** | True by construction of the lift. The non-trivial statement is which **exponent** survives mixing: for $q\ne2$ the only linear maps preserving $\sum|c_i|^q$ are phased permutations (Lamperti 1958, Li–So 1994), which have no cross term. Added as our (1.6). |
| 6 | Phase-fiber invariance; fiber $=U(1)^{n-1}$ | **OK** | Keep; our (1.3)–(1.4), Lean-checked instances. |
| 6 | **Row-sparsity theorem**: $q(Az)$ is a function of $q(z)$ iff every row of $A$ has at most one nonzero entry | **OK** | Correct, and it is the repository's own result: `qm_020` Thm 3 and `qm_122` Thm 3.2, Lean 2×2 instance `BornRedundancy.descent_compatible_iff_row_sparse`. Adopted as our (2.7) with the repo citation. |
| 6 | Two-row witness $(1,\pm1)\mapsto(4,0)/(0,4)$ | **OK** | Matches the Lean theorems `InterferenceNonDescent.mix_separates`, `PhaseBlindFiber.no_descent`. |
| 7 | Everett $:=$ diagonal $\rho_A$ $\wedge$ unitary $\Psi$; axiom table | **FIX** | Fine as "QM minus collapse". Two corrections to the table: (i) Bohm's "Born" is the quantum-equilibrium hypothesis on initial positions, not an outcome rule; (ii) the table should list the **preferred-basis** choice as an Everett input, since DeepSeek's own cost list does. |
| 7 | "Both branches are real" and "only one branch is real" are both non-theorems | **OK** | Keep; identical to our (5.2) and "Not established here". |
| 8 | Collapse SDE $d\psi=[-\tfrac{i}{\hbar}H\,dt+\sqrt\gamma(\hat q-\langle\hat q\rangle)dW]\psi$ | **FIX** | Missing the Itô term $-\tfrac{\gamma}{2}(\hat q-\langle\hat q\rangle)^2dt$; without it the norm is not preserved. (This is the continuous QMUPL/CSL form; GRW proper is discrete jumps.) |
| 8 | $V(m)=V_0e^{-\Gamma(m)t}$, $\Gamma\propto m^2$ | **FIX** | $\Gamma\propto N^2$ (mass-proportional CSL) only for an object smaller than $r_C\approx10^{-7}$ m displaced by more than $r_C$. For larger bodies the rate is $\lambda\,N\,N_{r_C}$-type, geometry-dependent (Bassi et al., Phys. Rep. 526, 471 (2013)). Say "superlinear in mass, geometry-dependent". |
| 8 | "$\Gamma>0$ observed $\Rightarrow$ Everett refuted" | **FIX** | Only after **every environmental channel is excluded**: visibility loss with an environment present is our (3.5), fully unitary. And what $\Gamma>0$ refutes is unitarity, hence Everett **and** Bohm **and** unitary-between-measurements Copenhagen together. The experimental axis is *unitary vs non-unitary*, not *worlds vs no worlds* (our (5.3)–(5.4)). |
| 9 | "Needed iff you refuse to add structure no measurement can notice" then "not needed as an explanation" | **WRONG (self-contradictory)** | Two different things are being called "Everett". *Deleting collapse* is forced by nothing and refuted by nothing (it changes no local prediction). *Adding "the terms are worlds"* is a further statement the formula does not take as an argument, our (5.2). Clean statement: collapse is **not needed** for predictions; worlds are **not needed and not excluded**. Everett is Occam on the postulate list only if one also accepts an unexplained Born measure and an approximate preferred basis, which DeepSeek's §7 cost list concedes. |

## Net

Keep DeepSeek §1, §2 (first half), §4, §5 (with the "on $A$ alone" restriction), §6 (all), §7 (non-theorem bullets). Replace the "Why $\mathbb C$" paragraph, the norm$\Rightarrow$Schrödinger chain, the §8 SDE and scaling, and §9 with the tagged versions in `everett_from_weights_math_only.md`. What DeepSeek added that the first draft of our derivation lacked: the general row-sparsity criterion (it turned out to be `qm_020` Thm 3 / `qm_122` Thm 3.2; now cited) and the explicit postulate table (adopt with the two fixes).


# Part 2: audit of the second draft, "Does ℓ¹ need the ℓ² observer to normalize? No."

Citations checked against the checkout (2026-11-02). The mathematics of the draft is sound; three of its citations are not.

| § | Claim | Verdict | What to do |
|---|---|---|---|
| 1 | ℓ¹ weights normalize with no Hilbert lift; `qm_020` Theorem 1 "Direct Normalization" | **OK** | Verified: `qm_020` §1.2 (PROVEN). The quoted sentence "A later probabilistic adapter may read this unit-sum profile as a probability distribution; this paper does not supply that adapter" is verbatim (§1.2). Our (1.2). |
| 1 | Theorem 4 "Hilbert-Lift Redundancy": the lift reproduces $w/W$ for any phases | **OK** | Verified: `qm_020` §1.5 (PROVEN). Our (1.2), (1.5). |
| 2 | "the ℓ² structure is forced by the data (fringes)" | **FIX** | Fringes force a *signed/complex* amplitude with a cross term. The **exponent** 2 is forced only under linear norm-preserving mixing, our (1.6); `qm_020` Theorem 6 fences Born uniqueness as imported. Say "a cross term is forced; the quadratic readout is forced conditionally". |
| 3a | $\Phi_1([\delta])=\inf_f\|\delta-d_0f\|_1=3$ on the oriented triangle, dual certificate $y=(1,1,1)$ | **OK (math)** | LP-checked: 3 when the three edges are oriented around the cycle (`check_everett.py`). With the simplicial orientation $(e_{01},e_{12},e_{02})$ the circulation of $(1,1,1)$ is $1$ and $\Phi_1=1$, so state the orientation. |
| 3a | "(`qm_020`, Theorem 2)" as the source of the circulation / quotient defect | **WRONG citation** | `qm_020` Theorem 2 is "Nonlinear Aggregation for $p>1$" (ℓ¹ additivity defect kernel, ℓᵖ subadditivity). $\Phi_1$ is defined in `papers/core/finite_quantum_mechanics.md` (quotient-norm display in the primitive-difference section) and the Zenodo "L1-Native Cohomology of Defect Fields" paper (`qm_020` ref. [6]); the circulation invariance under $A\mapsto A+d_0\lambda$ is `WDP-CH05-P04`. |
| 3b | $\mathrm{Hol}_U(\gamma)=U_{e_k}\cdots U_{e_1}$ "in `qm_060` and CH05 §5.2" | **FIX citation** | `qm_060` contains no holonomy; it is the phase-fiber paper (correct source for $q(D\psi)=q(\psi)$ and the $U(1)^{n-1}$ fiber). Holonomy is WDP level 04 §2.2 "U(1) connection and holonomy (§5.2)", i.e. CH05 §5.2 is right, `qm_060` is not. |
| 3b | Row-sparsity theorem "`qm_122` Thm 3.2" | **OK** | Verified: `qm_122` Theorem 3.2 "Row-Intensity Descent Characterization"; also `qm_020` Theorem 3; Lean 2×2 `BornRedundancy.descent_compatible_iff_row_sparse` (0 `sorry`). Our (2.7). |
| 4 | Theorem 6 "Conditional Quadratic/Born Uniqueness Requires Imported Representation Assumptions"; `OracleNeeded` | **OK** | Verified: `qm_020` §1.7; mechanization status line says "Theorem 6: SCOPE FENCE + STANDARD citation". |
| 4 | Five-row obligation table | **OK, add one row** | Add "exponent of the readout: not ℓ¹-native; selected by linear norm-preserving mixing (1.6), otherwise imported (Thm 6)". |
| 5 | "ℓ¹ normalizes; ℓ² interferes and carries phase; the holonomy in ℓ¹ is circulation, not phase" | **OK** | Consistent with our (1.2)–(1.4), (2.4), (2.7). |


# Part 3: audit of the third draft, "Where Everett Breaks: The Imported Container Does Not Account for Itself"

Every identifier was looked up in `witnessed_difference_programme.md` (17,685 lines) on 2026-11-02.

| Entry | Cited ids | Found? | Judgment |
|---|---|---|---|
| Observer as four layers: presentation, memory, evaluator, policy | CH10-D01..D04 | **Yes**, as described; D04 says "Policy is not authority" | Presentation (which report map) and memory (retention of the record) correspond to genuine physical inputs of Everett: the system/record/observer **factorization** and **stable records**, now (4.9). Evaluator and policy are agent-level constructs that do not enter $\mathrm{Tr}(\rho F)$: **not imports of the physics**. |
| Authority outside the observer | CH15-D01, CH15-N01 | **Yes**, but N01 says the *monograph* "assigns no authorization and changes no jurisdiction", not the quoted "no observation, no proof, no test, no formalization confers institutional standing" | Loose paraphrase, and a **category stretch**: institutional standing is not something Everett's physics imports. |
| Descent criterion | CH16-P01 | **Yes** (verbatim match) | Correct; it is our (2.5). |
| Typing fence `ObservationAccept` ⇏ `AuthStanding` | CH12-P01 | **Yes** | Correct, irrelevant to Everett. |
| "This chapter does not derive Hilbert space, unitarity…" | CH05-N01 | **Yes**, verbatim | Correct. |
| Born-quadratic uniqueness not proved; Sorkin sums vanish under quadratic readout | CH19-N01, CH19-P01 | **Yes** (P01 text matches) | Correct; our (1.5), (2.6). |
| Normalization nonselection | CH09-P01 | **Yes** | Correct; our (1.5). |
| "The monograph does not derive all structure from Primitive Difference" | CH00-N01 | **Yes** | Correct. |
| "A question whose inputs are not on the list is `OutsideProfile`, not `Undetermined`" | CH20-N01 | **No**: N01 reads "Relative completeness is not absolute omniscience, a truth-decider, a Gödel escape, world creation, or cosmogenesis". `OutsideProfile` occurs elsewhere | Wrong id for the claim. |
| Preferred basis | CH03-D01, CH03-P01 | **Partly**: P01 ("no $S_X$-equivariant selection of a distinguished element of an unstructured finite set") is an apt analogy; D01 is the asymmetry-price frontier, not a basis statement | Keep P01, drop D01. The physics version is our (4.8): decomposition is basis-dependent; decoherence narrows, does not select. |
| Branch access structure: P.13–P.22, $K(n,c)\simeq M(n,c+1)$, simply connected only for $c\ge3$ | P.13–P.21 exist (register row R6: P.18 disconnected guarded schedules, P.20 star-shaped legality ⇒ connected, trivial $\pi_1$); $K(n,c)$ is defined in `docs/guarded_schedule_topology.md`; "P.22" and the homotopy classification were **not found** | **Unverified**, and the relevance is asserted, not shown: a schedule-topology model of edit histories is not the branch structure of a quantum state. Do not use. |
| Born rule "`OracleNeeded` in the import register (Appendix D.3, Appendix L)" | `OracleNeeded`: **0 hits** in the monograph (it is `qm_020`'s term); D.3 is "Evidence separation"; L is the source-derivation obligations | Substance right (Born is imported), citation wrong. |
| Seven witness roles do not coerce | CH02-P01 | **Yes** | Correct; it is WDP's own typing discipline, not an Everett import. |
| Synthesis conclusion quote | CH22-C01 | **Yes**, verbatim | Correct. |

**Verdict.** Of the nine "imports", four are genuine physics inputs and were already in our ledger or are now (4.9): presentation → factorization and record observable; memory → stable records; preferred basis; Born measure. Four are category stretches (evaluator, policy, authority, witness typing: they concern agents and bookkeeping and do not enter the predictive map). One (branch access topology) is unverified and unconnected. The sentence "two named imports is a bookkeeping error" criticizes DeepSeek's own first draft, not our derivation, which lists seven **[A]** imports and two **[O]** items. The slogan "the equation never picks, so every pick must be named" is adopted: it is (5.2) and (5.6) in words.
