---
title: "Everett from Phase-Blind Weights: A Math-Only Derivation"
subtitle: "weights → amplitudes → records → relative states → is \"many worlds\" needed?"
author: "Jeremy H. Carroll"
date: "2026-11-02 · working note · math only"
---

**Tags.** **[A]** admitted (import, not derived here). **[D]** derived here, numerically checked (`check_everett.py`). **[L]** kernel-checked in the repository (`lean4/…`, theorem named). **[O]** open.

# 0. Objects

$$X=\{1,\dots,n\},\qquad \Delta_n=\Big\{w\in\mathbb{R}^n:\ w_i\ge 0,\ \textstyle\sum_i w_i=1\Big\},\qquad \dim\Delta_n=n-1. \tag{0.1}$$

A *phase-blind report* is a point $w\in\Delta_n$. **[A]**

# 1. Lift: weights → amplitudes

$$S=\{c\in\mathbb{C}^n:\ \|c\|^2=\textstyle\sum_i|c_i|^2=1\},\qquad \pi:S\to\Delta_n,\quad \pi(c)_i=|c_i|^2. \tag{1.1}$$ **[A]** complex amplitudes; **[A]** exponent 2 (Born). 

$$L:\Delta_n\to S,\quad L(w)_i=\sqrt{w_i}\ \Rightarrow\ \pi\circ L=\mathrm{id}_{\Delta_n}\quad(\pi\text{ is onto}). \tag{1.2}$$ **[D]**

$$\pi^{-1}(w)=\{(\sqrt{w_i}\,e^{i\theta_i})_i\}\cong T^{|\operatorname{supp}w|};\qquad \pi^{-1}(w)/U(1)_{\text{global}}\cong T^{|\operatorname{supp}w|-1}. \tag{1.3}$$ **[D]**

$$\dim_{\mathbb{R}}\big(S/U(1)\big)-\dim\Delta_n=(2n-2)-(n-1)=n-1\quad(\text{relative phases: invisible to }w). \tag{1.4}$$ **[D]**; **[L]** `PhaseFiber.global_phase_in_fiber`, `PhaseFiber.phase_fiber`, `QuotientFiber.fiber_exceeds_global_gauge_orbit` (the fiber is strictly larger than the global-phase orbit).

Exponent is not selected by the weight algebra, and is selected by linear norm-preserving mixing:
$$p^{(q)}_i=\frac{|z_i|^q}{\sum_j|z_j|^q}\in\Delta_n\ \ \forall q>0;\qquad z=(1,2):\ p^{(1)}=(\tfrac13,\tfrac23)\neq p^{(2)}=(\tfrac15,\tfrac45). \tag{1.5}$$ **[A]** $q=2$. Repository status: `GP-IMPORT-GLEASON` = IMPORTED_ASSUMPTION; `FQ-GAP-BORN-UNIQUENESS-GLEASON` = CONDITIONAL; $d=2$ non-Born frame functions exist, **[L]** `GleasonTheorem.d2_binary_non_bornian_obstruction`.

$$q\ne2:\quad \Big\{A\in M_n(\mathbb C):\ \textstyle\sum_i|(Az)_i|^q=\sum_i|z_i|^q\ \forall z\Big\}=\{\text{phased permutations}\}\quad\Rightarrow\quad\text{no cross term in (2.2)}. \tag{1.6}$$ **[A]** (isometries of $\ell^q_n$, $1\le q<\infty$, $q\ne2$: Lamperti 1958; Li–So 1994). Hence *linear mixing that preserves normalization and interferes* exists only for $q=2$; this is the conditional sense in which the exponent is forced (it is conditional on linearity and norm preservation, both **[A]**).

# 2. Mixing: why the lift is needed

$$U\in U(n),\qquad c\mapsto Uc,\qquad P_k=|(Uc)_k|^2=\Big|\sum_i U_{ki}c_i\Big|^2. \tag{2.1}$$ **[A]** unitary dynamics.

$$P_k=\underbrace{\sum_i|U_{ki}|^2 w_i}_{\text{function of }w}\;+\;\underbrace{2\sum_{i<j}\mathrm{Re}\big(U_{ki}\overline{U_{kj}}\,c_i\overline{c_j}\big)}_{\text{depends on }\theta_i-\theta_j}. \tag{2.2}$$ **[D]**; **[L]** `Superposition.beam_splitter_interference_expansion`, `InterferenceDeficit.deficit_eq_cross_term`.

Two-alternative form ($U=H=\tfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$, $\theta=\theta_2-\theta_1$):
$$P_1=\tfrac12\big(w_1+w_2+2\sqrt{w_1w_2}\cos\theta\big),\qquad P_2=\tfrac12\big(w_1+w_2-2\sqrt{w_1w_2}\cos\theta\big). \tag{2.3}$$ **[D]**

**No descent.** $\nexists\ f:\Delta_n\to\Delta_n$ with $f(\pi(c))=\pi(Uc)\ \forall c$:
$$c_\pm=\tfrac{1}{\sqrt2}(1,\pm1):\quad \pi(c_+)=\pi(c_-)=(\tfrac12,\tfrac12),\qquad \pi(Hc_+)=(1,0)\ne(0,1)=\pi(Hc_-). \tag{2.4}$$ **[D]**; **[L]** (Gaussian-integer instance, unnormalized $(2,0)$ vs $(0,2)$ and $(4,0)$ vs $(0,4)$) `InterferenceDeficit.L1_cannot_compute_interference`, `InterferenceNonDescent.no_descent_through_fiber`, `InterferenceNonDescent.mix_separates`, `PhaseBlindFiber.no_descent`, `QuotientFiber.psi1_psi2_in_same_fiber`, `QuotientFiber.psi1_psi2_distinct`.

**Fiber criterion (general).** For $r:X\to R$ (report) and $d:X\to D$ (question):
$$\big(\exists!\ g:\operatorname{im}r\to D,\ g\circ r=d\big)\iff\big(r(x)=r(y)\Rightarrow d(x)=d(y)\big);\qquad r(x)=r(y)\wedge d(x)\ne d(y)\ \Rightarrow\ \nexists\,g. \tag{2.5}$$ **[L]** `ReportFiberDescent.unique_decoder_iff`, `ReportFiberDescent.postprocess_obstruction`, `FrontierDistinguishability.separatedByTask_iff_disjoint_image`. Apply with $r=\pi$, $d=\pi\circ U$, $x=c_+$, $y=c_-$.

**How much the lift adds: exactly pairwise.** With $P(A)=|\sum_{i\in A}c_i|^2$:
$$I_2=P(\{1,2\})-P(\{1\})-P(\{2\})=2\,\mathrm{Re}(\overline{c_1}c_2)\ne0\ \text{generically}, \tag{2.6a}$$
$$I_3=P(123)-P(12)-P(13)-P(23)+P(1)+P(2)+P(3)=0. \tag{2.6b}$$ **[D]**; **[L]** `Superposition.sorkin_third_order_interference_vanishes`.

**Exactly when descent fails.** For $A\in M_n(\mathbb C)$:
$$\big(\exists f:\ \pi(Az)=f(\pi(z))\ \forall z\in\mathbb C^n\big)\iff\text{every row of }A\text{ has at most one nonzero entry}. \tag{2.7}$$ **[D]**, **[L]** ($\Leftarrow$: $|(Az)_b|^2=|A_{bj}|^2|z_j|^2$. $\Rightarrow$: a row with $A_{bj}A_{bk}\ne0$ and $z(\theta)=e_j+e^{i\theta}e_k$ gives constant $\pi(z(\theta))$ but $|(Az)_b|^2=|A_{bj}|^2+|A_{bk}|^2+2\,\mathrm{Re}(A_{bj}\overline{A_{bk}}e^{-i\theta})$.) This is the repository's own theorem: `qm_020` Thm 3 (Strict Row-Sparsity, MECHANIZED finite rational) and `qm_122` Thm 3.2 (Row-Intensity Descent Characterization, written proof for $\mathbb C^n\to\mathbb C^m$); **[L]** $2\times2$ real instance `BornRedundancy.descent_compatible_iff_row_sparse` (0 `sorry`). The DeepSeek draft restates it; verified here numerically; (2.4) is the case $A=H$.

**Conclusion 1.** $w\mapsto c$ is *necessary* exactly when the mixing matrix has a row with two nonzero entries (every beam splitter): (2.4)–(2.5), (2.7) show no function of $w$ reproduces the readouts; (2.6) shows the added data is the pairwise relative phases and nothing beyond.

# 3. Records: what a detector changes

$$\mathcal H_S\otimes\mathcal H_E,\qquad \Psi=\sum_i c_i\,|i\rangle\otimes|E_i\rangle,\qquad \|E_i\|=1,\qquad G_{ij}:=\langle E_j|E_i\rangle. \tag{3.1}$$ **[A]** tensor product; **[A]** partial trace.

$$\rho_S=\operatorname{Tr}_E|\Psi\rangle\langle\Psi|=\sum_{i,j}c_i\overline{c_j}\,G_{ij}\,|i\rangle\langle j|,\qquad (\rho_S)_{ii}=w_i\ \ \forall G. \tag{3.2}$$ **[D]** (written proof in QM_094 Thm 2.1; the DAG node `DS-QM094-EVERETT-RELATIVE-STATE-CONTACT` is COMPUTATIONALLY_CHECKED only, its Lean item is a literal identity, so not **[L]**).

$$P_k=\operatorname{Tr}\big(\rho_S\,U^\dagger|k\rangle\langle k|U\big)=\sum_{i,j}U_{ki}\overline{U_{kj}}\,c_i\overline{c_j}\,G_{ij}. \tag{3.3}$$ **[D]**

Two alternatives with record overlap $\gamma=G_{21}=\langle E_1|E_2\rangle$:
$$P_1=\tfrac12\big(w_1+w_2+2\sqrt{w_1w_2}\,|\gamma|\cos(\theta+\arg\gamma)\big),\qquad V:=|\gamma|,\quad D:=\sqrt{1-|\gamma|^2},\quad V^2+D^2=1. \tag{3.4}$$ **[D]** (pure records; mixed records give $V^2+D^2\le1$, Jaeger–Shimony–Vaidman 1995, Englert 1996 **[A]**).

**Perfect record descends.** $G=I$:
$$\rho_S=\sum_i w_i|i\rangle\langle i|,\qquad P_k=\sum_i|U_{ki}|^2w_i=:f_U(w)\quad\forall U. \tag{3.5}$$ **[D]** — with orthogonal records the readout *is* a function of $w$ alone (the fiber criterion is now satisfied); the interference term of (2.2) is multiplied by $G_{ij}=0$.

**Decoherence $\ne$ collapse.** $\Psi_\varphi=\tfrac{1}{\sqrt2}\big(|1\rangle|E_1\rangle+e^{i\varphi}|2\rangle|E_2\rangle\big)$, $G=I$:
$$\rho_S(\varphi)=\tfrac12 I\ \ \forall\varphi,\qquad \operatorname{Tr}\rho_S^2=\tfrac12,\qquad \operatorname{Tr}\rho_{SE}^2=1,\qquad \langle\Psi_\varphi|\,|\Psi_0\rangle\langle\Psi_0|\,|\Psi_\varphi\rangle=\tfrac{1+\cos\varphi}{2}. \tag{3.6}$$ **[D]** — $\varphi$ is erased from $S$ and retained in $S\otimes E$; a joint observable recovers it.

**Eraser.** Measure $E$ in $|E_\pm\rangle=\tfrac{1}{\sqrt2}(|E_1\rangle\pm|E_2\rangle)$ ($G=I$):
$$P(k\,|\,E_\pm)\propto\big|U_{k1}c_1\pm U_{k2}c_2\big|^2,\qquad P(k|E_+)+P(k|E_-)\propto 2\big(|U_{k1}c_1|^2+|U_{k2}c_2|^2\big)=2f_U(w)_k. \tag{3.7}$$ **[D]** — fringes per subensemble, phase-shifted by $\pi$; sum over subensembles flat. Fringes are visible only after conditioning on the $E$ outcome (no signalling).

# 4. Everett: relative states, no new axiom

**Measurement as an isometry.** With $|E_0\rangle$ a ready state and $\langle i|j\rangle=\delta_{ij}$:
$$U_M:\ |i\rangle\otimes|E_0\rangle\mapsto|i\rangle\otimes|E_i\rangle,\qquad U_M\Big(\sum_ic_i|i\rangle\Big)|E_0\rangle=\sum_ic_i|i\rangle|E_i\rangle. \tag{4.1}$$ $U_M$ extends linearly to an isometry because $\{|i\rangle|E_i\rangle\}_i$ is orthonormal. **[A]** linearity + unitarity; **[D]** the consequence.

**Relative state (Everett 1957).** For $c_i\ne0$: the state of $E$ relative to $|i\rangle$ is
$$|E\rangle_{\text{rel }i}=\frac{(\langle i|\otimes 1)\Psi}{\|(\langle i|\otimes 1)\Psi\|}=|E_i\rangle. \tag{4.2}$$ **[D]**

**Observer included.** $|O_0\rangle\to|O_i\rangle$ on reading $E_i$, $\langle O_i|O_j\rangle=\delta_{ij}$:
$$\Psi'=\sum_ic_i\,|i\rangle|E_i\rangle|O_i\rangle,\qquad R:=\sum_i i\,|O_i\rangle\langle O_i|,\qquad (1\otimes1\otimes R)\big(c_i|i\rangle|E_i\rangle|O_i\rangle\big)=i\cdot c_i|i\rangle|E_i\rangle|O_i\rangle. \tag{4.3}$$ **[D]** — each term is an eigenvector of the record observable with one definite value; no term records "all $i$".

**Local observables do not see other terms.** For $F$ on $S$ alone:
$$\langle\Psi'|F\otimes1\otimes1|\Psi'\rangle=\sum_{i,j}c_i\overline{c_j}F_{ji}\,G_{ij}\langle O_j|O_i\rangle\ \xrightarrow{\ G=I\ }\ \sum_iw_iF_{ii}. \tag{4.4}$$ **[D]** — cross terms between branches are suppressed by the record overlaps; (3.6) shows a *joint* observable still sees them.

**Weights conserved under refinement.** If branch $i$ splits, $|E_i\rangle\mapsto\sum_\alpha r_{i\alpha}|E_{i\alpha}\rangle$, $\sum_\alpha|r_{i\alpha}|^2=1$:
$$w_{i\alpha}=|c_i r_{i\alpha}|^2,\qquad \sum_\alpha w_{i\alpha}=w_i. \tag{4.5}$$ **[D]**

**Branch counting $\ne$ Born weight.** Counting works iff weights are rational:
$$w=\big(\tfrac{p_0}{D},\tfrac{p_1}{D}\big)\ \Rightarrow\ \exists\ \text{equal-weight fine-graining into }D\text{ cells}; \tag{4.6}$$
$$w=\Big(\tfrac{5+\sqrt5}{10},\tfrac{5-\sqrt5}{10}\Big)\ \text{are the roots of}\ 5x^2-5x+1=0;\quad \text{candidates }\pm1,\pm\tfrac15\text{ all fail} \tag{4.7a}$$
$$\Rightarrow\ w\notin\mathbb{Q}^2\ \Rightarrow\ \nexists\ \text{finite equal-weight count reproducing }w. \tag{4.7b}$$ **[L]** `RationalSector.rational_finegraining_exists`, `RationalSector.witness_poly_has_no_candidate_rational_root` (+ rational root theorem **[A]**); DAG `FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY` COMPUTATIONALLY_CHECKED. **[O]** deriving $w=|c|^2$ as the branch measure without assuming it (Deutsch–Wallace decision theory is outside this document).

**Decomposition is not canonical.**
$$\tfrac{1}{\sqrt2}\big(|0\rangle|0\rangle+|1\rangle|1\rangle\big)=\tfrac{1}{\sqrt2}\big(|+\rangle|+\rangle+|-\rangle|-\rangle\big),\qquad |\pm\rangle=\tfrac{1}{\sqrt2}(|0\rangle\pm|1\rangle). \tag{4.8}$$ **[D]** — "which terms are the branches" is fixed only by a dynamical condition $G\approx I$ (record orthogonality), which is approximate: generically $0<|G_{ij}|\ll1$. **[O]** exact preferred basis.

**Inputs Everett declares.** Reading (4.3) literally requires, beyond (5.1):
$$\mathcal H=\mathcal H_S\otimes\mathcal H_E\otimes\mathcal H_O\ \text{(a chosen factorization)},\qquad \langle O_i|O_j\rangle=\delta_{ij}\ \text{persisting under later dynamics (stable records)},\qquad w\ \text{(the branch measure)},\qquad \{|i\rangle\}\ \text{(the basis)}. \tag{4.9}$$ **[A]** factorization, stable records; **[O]** measure, exact basis. Agent-level notions (evaluation, policy, authority) are not arguments of (5.1) and have the same status as $\mathcal W$ below: they change no prediction.

# 5. Is "many worlds" needed?

**Predictive content.** Everything measurable is the map
$$\mathrm{Pred}:\ (\Psi,\ U,\ \{F_k\})\ \longmapsto\ p_k=\operatorname{Tr}\big(\rho\,U^\dagger F_kU\big),\qquad F_k\ge0,\ \textstyle\sum_kF_k=1. \tag{5.1}$$ **[A]** (Born/POVM). Sections 1–4 are statements about (5.1).

**Everett's addition.** Let $\mathcal W$ be the predicate "every term $c_i|i\rangle|E_i\rangle|O_i\rangle$ with $c_i\ne0$ is an actual world". Then
$$\mathcal W\notin\operatorname{args}(\mathrm{Pred})\quad\Rightarrow\quad \mathrm{Pred}(\,\cdot\,|\,\mathrm{QM}+\mathcal W)=\mathrm{Pred}(\,\cdot\,|\,\mathrm{QM})=\mathrm{Pred}(\,\cdot\,|\,\mathrm{QM}+\neg\mathcal W). \tag{5.2}$$ **[D]** (a statement about the formula, not about nature).

**What *does* change predictions: altering (5.1), not labelling its terms.** Non-unitary dephasing,
$$\rho_{ij}\mapsto e^{-\lambda t}\rho_{ij}\ (i\ne j)\quad\text{or}\quad K_0=\begin{pmatrix}1&0\\0&\tfrac35\end{pmatrix},\ K_1=\begin{pmatrix}0&0\\0&\tfrac45\end{pmatrix},\ K_0^\dagger K_0+K_1^\dagger K_1=I,\qquad \rho_{01}:\ \tfrac12\to\tfrac{3}{10}\to\tfrac{9}{50}\to\tfrac{27}{250}, \tag{5.3}$$
$$P_1^{(k)}=\tfrac12\big(1+2\rho_{01}^{(k)}\big)=\tfrac12\big(1+(\tfrac35)^k\big)\ \ne\ 1. \tag{5.4}$$ **[L]** `FiniteQFTAndGravity.phase_damping_coherence_three_steps`; **[D]** (5.4). Visibility decay $(3/5)^k$ is testable and holds with or without $\mathcal W$: the experimental axis is *unitary vs non-unitary*, not *worlds vs no worlds*.

**Description size vs readout size.** $n$ qubits: $2^n$ complex amplitudes; accessible classical information per copy $\le n$ bits (Holevo **[A]**):
$$\dim_{\mathbb C}\mathcal H=2^n,\qquad I_{\text{acc}}\le S(\rho)\le n. \tag{5.5}$$ **[D]** — the $2^n$ is a size of the *description* that the formula requires; whether a description's size entails ontological multiplicity is $\mathcal W$ again (Deutsch's "where was the computation done?" is a question about (5.5), and (5.2) says the formula does not answer it).

**Verdict (three lifts).**

| Lift | Verdict | Reason |
|------|---------|--------|
| $w\to c$ (weights to amplitudes) | **needed** | (2.4)–(2.6): changes predictions after mixing |
| $c\to\Psi=\sum_ic_i\lvert i\rangle\lvert E_i\rangle\lvert O_i\rangle$ (amplitudes to records) | **needed** | (3.2)–(3.7), (4.1): changes predictions when records exist |
| terms $\to$ worlds ($\mathcal W$) | **not needed, not excluded** | (5.2): changes no prediction; (5.3)–(5.4): rivals differ elsewhere |

Table (5.6).

**Not established here.** $\neg\mathcal W$ (no refutation); $\mathcal W$ as the unique consistent reading; $w=|c|^2$ from branch structure; an exact preferred basis. **[O]**

# 6. Minimal skeleton for the intuitive model

$$\text{(E1)}\qquad P=w_1+w_2+2\sqrt{w_1w_2}\,\cos\theta$$ no record: the relative phase $\theta$ is in the answer.

$$\text{(E2)}\qquad P=w_1+w_2+2\sqrt{w_1w_2}\,|\gamma|\cos(\theta+\arg\gamma),\qquad |\gamma|=|\langle E_1|E_2\rangle|\in[0,1]$$ a record with overlap $\gamma$: one dial from full fringes ($|\gamma|=1$) to none ($|\gamma|=0$).

$$\text{(E3)}\qquad \Psi=\sum_ic_i\,|i\rangle|E_i\rangle|O_i\rangle,\qquad \sum_i|c_i|^2=1$$ the terms are in the formula; "worlds" is a name for the terms, not a term in the formula.

# 7. Evidence table

| Eq. | Claim | Tag | Source |
|----|------------------|-----|------------------------|
| 1.2–1.4 | $\pi$ onto; fiber $=$ relative phases, bigger than global phase | D, L | `PhaseFiber.lean`, `QuotientFiber.lean` (0 `sorry`) |
| 1.5–1.6 | exponent 2 not selected by weights; selected by linear norm-preserving mixing | A | `GP-IMPORT-GLEASON` (IMPORTED_ASSUMPTION), `FQ-GAP-BORN-UNIQUENESS-GLEASON` (CONDITIONAL); Lamperti 1958, Li–So 1994 |
| 2.2 | readout $=$ weight term $+$ pairwise cross term | D, L | `Superposition.beam_splitter_interference_expansion`, `InterferenceDeficit.deficit_eq_cross_term` |
| 2.4 | no function of $w$ gives readouts | D, L | `InterferenceDeficit.L1_cannot_compute_interference`, `InterferenceNonDescent.no_descent_through_fiber`, `PhaseBlindFiber.no_descent` |
| 2.5 | fiber criterion, post-processing obstruction | L | `ReportFiberDescent.unique_decoder_iff`, `ReportFiberDescent.postprocess_obstruction` |
| 2.6a–b | pairwise cross term; third-order interference vanishes | D, L | `Superposition.sorkin_third_order_interference_vanishes` |
| 2.7 | descent iff rows monomial | D, L | `qm_020` Thm 3, `qm_122` Thm 3.2; `BornRedundancy.descent_compatible_iff_row_sparse` (2×2); `check_everett.py` |
| 3.2–3.4 | reduced state, overlap-weighted fringes, $V^2+D^2=1$ | D (+A) | QM_094 Thm 2.1 (written); Jaeger–Shimony–Vaidman 1995, Englert 1996 |
| 3.5–3.7 | perfect record descends; decoherence $\ne$ collapse; eraser | D | `check_everett.py` |
| 4.1–4.5 | isometric measurement, relative state, record eigenvalue, local blindness, refinement | D | Everett 1957 (form); `check_everett.py` |
| 4.6–4.7b | counting $=$ Born iff rational; $(5\pm\sqrt5)/10$ witness | L (+A) | `RationalSector.lean` (0 `sorry`); `FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY` |
| 4.8 | decomposition not canonical | D | Bell-state identity |
| 4.9 | Everett's declared inputs: factorization, stable records, measure, basis | A, O | Wallace 2012 (emergent worlds, no world count); Carroll–Singh 2021 (factorization open) |
| 5.2 | $\mathcal W$ is not an argument of Pred | D | tautology of (5.1) |
| 5.3–5.4 | non-unitary dephasing changes predictions | L, D | `FiniteQFTAndGravity.phase_damping_coherence_three_steps` |
| 5.5 | Holevo bound | A | Holevo 1973 |

All cited Lean files: 0 `sorry`. Lean instances are over Gaussian integers / `Int` (exact arithmetic); the $\mathbb C$ statements are the **[D]** rows.
