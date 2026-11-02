# Independent referee report on "Can Everett be refuted?" (revision 2)

Referee: Sakana `fugu-ultra-v2` (via OpenRouter), 2026-11-02, run once on revision 2 of [refuting_everett_assessment.md](refuting_everett_assessment.md) together with [everett_from_weights_math_only.md](everett_from_weights_math_only.md). Text below is the referee's, unedited except for headings. Revision 3 of the assessment adopts sections 1, 3 and 4; the ℚ(√2) witness is checked exactly in `check_conjugate_measure.py`. Claims marked UNSURE are the referee's own.

## 1. Errors

### 1.1 Lemma 0 and the predictive map

> "Any empirical refutation of Everett is a refutation of universal unitarity."

False except as a stipulative tautology. Equation EW(5.2) defines $\mathcal W$ to be absent from a predictive map in which the Born rule has already been inserted. It proves only: if two theories have the same complete predictive map, experiments do not distinguish them. It does not prove that every defensible Everett theory has that map. In particular:

- A Born-rule violation could refute Everett + $\mathrm{Pred}_{\rm Born}$ while leaving wave-function evolution unitary. Non-equilibrium Bohmian and some modal models are logical examples.
- Naive branch-counting Everett makes non-Born predictions while retaining unitary dynamics. The assessment itself calls this theory empirically refuted, contradicting Lemma 0.
- Two theories with the same unitary state can differ through an observer-selection or self-location kernel $p(o\mid \Psi,\text{observer data})$.

**Fix:** Theories sharing dynamics, observables, preparation assumptions, the Born map, and the same observer-selection/conditionalization rule cannot be distinguished if they differ only by an operationally idle predicate $\mathcal W$. There is no established experiment separating standard Born-weighted Everett from equilibrium Bohmian mechanics or another empirically equivalent unitary single-world theory. Differences arise only after adding different probability, typicality, or observer-selection rules.

| Proposal | Does it distinguish Everett from all unitary single-world theories? |
|---|---|
| Self-locating probability | Potentially, but only after rival conditionalization kernels are specified. This changes Pred; bare Everett does not uniquely fix the kernel. |
| Quantum suicide/immortality | No. External frequencies remain Born-weighted, and first-person "certain survival" requires a nonstandard self-location rule. |
| Deutsch's 1985 reversible observer/Wigner-friend experiment | No. It distinguishes reversible coherence from irreversible collapse; Bohmian and suitable modal theories also allow reversal. |
| Local Friendliness | No. It excludes a conjunction involving observer-independent events, locality/local agency, and freedom assumptions. Bohmian mechanics survives by rejecting locality; Everett is not uniquely selected. |
| Cosmological measure problems | Yes in principle: different measures or xerographic distributions change first-person predictions despite identical unitary dynamics. No accepted uniquely Everettian measure currently gives a clean discriminator. |
| Quantum gravity | Demonstrated closed-system pure-to-mixed evolution would refute orthodox universal-unitary Everett. It would not distinguish Everett from unitary single-world theories if unitarity survives, and generalized timeless Everett formulations may not use a fundamental $U(t)$. |

> "holds in every dimension … separable or not, any field"

False. Positivity and probabilities require an ordered $*$-field or an appropriate positive cone. In infinite dimension, density-operator traces do not represent every state; normality and trace-class hypotheses matter. Over arbitrary fields the displayed Born map is not defined.

> "W can only be refuted by showing it is ill-defined or self-undermining"

Not exhaustive. A precise $\mathcal W$ could be inconsistent with Lorentz covariance, an independently justified ontology of records or persons, an AQFT subsystem structure, or another accepted constraint.

> "every decohered term is an actual world"

Not a faithful formulation of modern Everett. "Term" is decomposition-dependent; Wallace-style worlds are approximate, emergent, temporally extended structures, not a fundamental predicate on exact expansion terms.

> "every serious anti-Everett program in 70 years has been one of three kinds"

Unsupported. Confirmation/self-location, empirical incoherence, relativistic branching, personal identity, AQFT, and cosmological typicality do not fit cleanly into the three stated routes.

### 1.2 Route A

- "Everett's single empirical commitment is unitarity without exception": overclaim. The theory also assumes the Born/POVM map, observable and subsystem structure, preparation assumptions, and a rule relating branches to observations.
- EW(5.3)–(5.4) "non-unitary dephasing": a Kraus dephasing channel has a unitary system–environment dilation; it is not evidence of fundamental non-unitarity. Fix: formulate a closed-system collapse generator (CSL $(\lambda,r_C)$ or regularized DP), derive its mass, geometry and time dependence, and exclude environmental and technical noise.
- Diósi–Penrose: Donadi et al. constrain the regularization and exclude the natural parameter-free choice ($R_0\gtrsim0.54$ Å). "DP" is a family.
- "Gravity cannot entangle": no-entanglement results assume local classical mediation and restricted classical–quantum interactions.
- Absence of gravitationally induced entanglement would not kill unitarity (insufficient interaction, ordinary decoherence, calibration, detector noise). Its presence supports Everett, Bohm and other no-collapse views equally.
- "Nobody will [win a Nobel for an interpretation]": unfalsifiable rhetoric.
- Frauchiger–Renner (universal validity, consistency, single outcomes) and Local Friendliness (locality/free choice/absoluteness) are distinct; neither uniquely favours Everett; nonlocal Bohmian mechanics is a unitary single-world counterexample to "these pressure single-world unitary views".

### 1.3 Route B1

The no-go is not yet a theorem statement ("branch", "stable", "generic", "symmetry" undefined; the one-branch decomposition satisfies much of it; recurrence defeats exact permanence in finite closed systems). Dowker–Kent established set-selection and multiplicity problems for consistent histories, not this theorem. Schwindt's claim is at most heuristic (UNSURE). Cotler–Penington–Ranard assume a restricted local-Hamiltonian ansatz and genericity. The limited conclusion, that an exact-branch theorem would not refute emergent-branch Everett, is correct.

### 1.4 Route B2

- Counting = Born iff rational holds only for finite exact equal-weight fine-graining; finite observations cannot establish exact irrationality, and Saunders' decoherence-based counting must be addressed.
- Survival of the exotic $\mathbb Q^3$ measure would not prove circularity. It already fails pure-state certainty: its range $\{0,\tfrac13,\tfrac23\}$ contains no 1. Its 0/1-valued Godsil–Zaks relatives are incompatible with the rational fine-graining argument below.
- There is no unique Deutsch–Wallace axiom list. In Wallace, Equivalence is derived, erasure is a proof construction, and continuity sits inside a preference/representation framework. Wallace gives explicit axiom systems; the dispute is about their justification, not their syntax.
- "Nobody has mechanized the axioms": UNSURE. Novelty and the 3–6 month estimate: UNSURE; prior art on rational-sphere colourings and non-Born frame functions includes Godsil–Zaks, Meyer, Kent, Clifton–Kent, Havlíček et al., Pitowsky.
- The $\mathbb Q(i)^3$ mod-2 result constrains a residue-class ansatz, not all frame functions.
- $d=2$ non-Born frame functions are closed by ancillas or POVM richness (Busch; Caves–Fuchs–Manne–Renes); Deutsch–Wallace richness includes ancillas.

### 1.5 Route C and the conclusion

Holevo ($I_{\rm acc}\le\chi\le n$) is correct but does not support the ontological inference or explain speedup. Howard et al. make contextuality necessary for magic-state advantage in specified models, not a complete account. "W-structure is a gauge" is unsupported: branch-mixing maps change record observables and are physical. Non-unitarity eliminates universal-unitary Everett, not every many-worlds ontology. "No mathematics can refute Everett" is false for any precise theory; what cannot be refuted is an indefinitely revisable interpretation defined to add no predictive content.

## 2. Missed routes

1. **Observer-selection/confirmation theorem.** Uniqueness or impossibility for kernels $p(o\mid\Psi,\text{observer data})$ under covariance, diachronic consistency and duplication constraints. Could change Pred: yes.
2. **Finite or mangled-world theories.** Cut-off corrections constrained by rare-event data (Hanson; Many Interacting Worlds is a distinct theory). Could change Pred: yes; status UNSURE.
3. **Unitary non-Born single-world models** (non-equilibrium Bohm/modal). Not a direct refutation; disproves the unconditional Lemma 0. Could change Pred: yes.
4. **Relativistic/AQFT branching** in type III without a preferred tensor factorization. No accepted no-go. Changes Pred: normally no.
5. **Quantum-Darwinism uniqueness** for a generic class of Hamiltonians. Changes Pred: no.
6. **Continuum branching and unbounded acts** (St. Petersburg pathologies). Changes Pred only with an alternative measure.
7. **Macroscopic recoherence.** Constrains collapse, not Everett specifically.
8. **Personal identity / empirical incoherence.** No accepted theorem; identity axioms are easy to change.

## 3. Target B2: formalization and result

### 3.1 Core

$K\subseteq\mathbb C$ closed under conjugation. A finite game: a finite-dimensional $K$-Hilbert space, normalized $\psi$, a $K$-rational projective partition $\{P_i\}$, rewards $r_i$, arbitrary finite $K$-ancillas and $K$-isometries. Hilbert weight $b_\psi(P)=\langle\psi,P\psi\rangle$. Axioms:

1. Certainty/nullity, positivity: $P\psi=\psi\Rightarrow\mu_\psi(P)=1$; $P\psi=0\Rightarrow\mu_\psi(P)=0$; $\mu\ge0$.
2. Finite additivity / branching indifference: $PQ=0\Rightarrow\mu_\psi(P+Q)=\mu_\psi(P)+\mu_\psi(Q)$.
3. State supervenience and $K$-unitary covariance: $\mu_{U\psi}(UPU^\dagger)=\mu_\psi(P)$.
4. Measurement neutrality, erasure, richness: reward-preserving ancillary refinements by $K$-isometries do not change value.
5. Diachronic/tensor composition: independent weights multiply.
6. No continuity axiom.

$V(G)=\sum_i\mu_\psi(P_i)u(r_i)$. This is a precise measure-theoretic core, not a claim that every historical formulation has exactly these axioms.

### 3.2 Equivalence is derived

If $(\psi,P)$ and $(\phi,Q)$ have the same Hilbert weight $b$, the orthogonal components have equal Gram data; after padding with ancillas, Witt's extension theorem gives a $K$-isometry, so $\mu_\psi(P)=\mu_\phi(Q)=:f(b)$. Realizable weights: $\mathcal W_K=\{b\in K\cap\mathbb R: b=\sum|x_j|^2,\ 1-b=\sum|y_k|^2\}$.

### 3.3 Rational-weight lemma

If $b_\psi(P_i)=w_i=q_i/D^2$ with $\sum q_i=D^2$, map $P_i\psi\mapsto y_i=\tfrac1D\sum_{k\le q_i}e_{ik}$ (Gram-preserving, extends to a $K$-isometry). The refined state $\Phi=\tfrac1D\sum_{i,k}e_{ik}$ is invariant under all cell permutations, so each cell has weight $1/D^2$ and $\mu_\psi(P_i)=q_i/D^2=w_i$. No continuity is used.

### 3.4 Consequences

- $K=\mathbb Q,\ \mathbb Q(i)$: every weight is rational and every positive rational is a sum of rational squares, so $\mu_\psi(P)=\langle\psi,P\psi\rangle$. The exotic $\mathbb Q^3$ function is not a counterexample (fails certainty; 0/1 colourings fail the rational lemma).
- Real-closed $K$ or $K=F(i)$: every $x\in K\cap[0,1]$ is realizable; additivity gives monotonicity; for rationals $r<x<s$, $r\le f(x)\le s$, so $f(x)=x$. An order squeeze, not a continuity axiom. Includes the real algebraic numbers.
- $K=\mathbb Q(\sqrt2)$, $\sigma(a+b\sqrt2)=a-b\sqrt2$: $\mu_\psi(P)=\sigma(\langle\psi,P\psi\rangle)$ satisfies all axioms (realizable $b,1-b$ are sums of squares, so $0\le\sigma(b)\le1$; $\sigma$ additive and multiplicative; $b$ invariant). Non-Born: $a=\frac{-3-8\sqrt2}{17}$, $c=\frac{12-2\sqrt2}{17}$, $a^2+c^2=1$, $a^2=\frac{137+48\sqrt2}{289}$, $\sigma(a^2)=\frac{137-48\sqrt2}{289}\ne a^2$. $\sigma$ is discontinuous in the topology of the chosen embedding. "Algebraic field" is ambiguous: real algebraic numbers are Born-unique, $\mathbb Q(\sqrt2)$ is not.

### 3.5 Which axiom carries Born?

Equal amplitudes: covariance. Rational unequal weights: branching indifference, additivity, measurement neutrality, ancillary richness. Real-closed irrational weights: positivity/additivity plus the unique order. Fields with several real embeddings: continuity or explicit choice of the physical embedding. "Born enters through continuity" is false over $\mathbb Q$, $\mathbb Q(i)$ and real-closed fields; the most contestable physical premise is branching indifference / measurement neutrality.

## 4. Verdict

1. No small team can eliminate every reasonable Everett formulation in 12 months.
2. Lemma 0 must be withdrawn or reduced to a conditional tautology about a fixed predictive map.
3. Do B2 first, as a field-dependent classification theorem, not an anti-Everett theorem.
4. Born is forced over $\mathbb Q$, $\mathbb Q(i)$ and real-closed fields without continuity.
5. Conjugate non-Born measures over fields such as $\mathbb Q(\sqrt2)$ are a genuine, Lean-suitable result.
6. The load-bearing premise is ancillary branching indifference / measurement neutrality; continuity is secondary.
7. B1 can yield an exact-branch no-go, but emergent Everett survives it.
8. A collapse exclusion model is feasible; a decisive empirical discovery is outside the team's control.
9. Realistic 12-month output: a rigorous B2 classification plus a parameterized collapse analysis, not a refutation of Everett.
