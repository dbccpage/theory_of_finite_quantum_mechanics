# 094 Everettian Relative State Contact

## GTOC Foundations — Quantum Contact Series (qm_094_everettian_relative_state_contact)

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

Quantum Contact 2 - Everettian QM as Relative-State Branching
=============================================================

L1 branch weights, L2 record coherence, decoherent descent, and the limits of holonomy

**Series role:** supplementary quantum-contact paper; not a new GTOC degree
**Date:** 2026-07-17 · **Version:** v1.0
**Claim ledger:** [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (IDs `094:QCE-C1` through `094:QCE-C12`)
**Terminal:** conditional finite relative-state mathematics; `OpenObstruction` for Everettian ontology, preferred basis, and probability interpretation
**Authority effect:** `None`
**Depends on:** [`qm_063_holonomy_structured_superposition.md`](qm_063_holonomy_structured_superposition.md), [`qm_072_bit_shadow_and_qubit.md`](qm_072_bit_shadow_and_qubit.md), [`qm_073_correlation_separability_finite_bell.md`](qm_073_correlation_separability_finite_bell.md), [`qm_020_born_normalization_and_conditional_hilbert_lift.md`](qm_020_born_normalization_and_conditional_hilbert_lift.md), [`qm_091_deutsch_everett_wolfram_promotion_error.md`](qm_091_deutsch_everett_wolfram_promotion_error.md), and [`qm_003_residual_density_calculus_l1_l2_boundary.md`](qm_003_residual_density_calculus_l1_l2_boundary.md)
**Mechanization:** not started; targets are stated in Section 10

Abstract

The relative-state formalism admits a sharp finite decomposition. Given an imported tensor-product Hilbert carrier,

$$
|\Psi\rangle=\sum_i c_i|i\rangle|E_i\rangle,
$$

the nonnegative branch weights `w_i=|c_i|^2` form an L1 shadow. The overlaps $\langle E_j|E_i\rangle$, coefficient phases, and off-diagonal terms retain L2 coherence. Tracing out the record carrier yields

$$
\rho_S=\sum_{i,j}c_i\overline{c_j}
\langle E_j|E_i\rangle |i\rangle\langle j|.
$$

Orthogonal record states make this reduced state exactly diagonal. Small overlaps make every bounded local expectation close to its diagonal L1 shadow, with an explicit finite error bound. These are conditional mathematical results. They explain why branch-weight bookkeeping can be locally stable while global coherence remains available.

Holonomy clarifies recombination but has a strict limit. A pure branch tree has no gauge-invariant U(1) loop holonomy: every edge phase is removable. Relative holonomy becomes meaningful only when histories recombine, when two refinement paths identify the same record, or when a 2-complex supplies a consistency face. It can therefore govern recoherence and interference between histories. It cannot create branch multiplicity, select a preferred basis, prove that branches are worlds, or derive Everettian ontology.

The resulting verdict is deliberately split. Relative-state branching is a coherent imported representation. Its L1/L2 descent and recoherence witnesses are exact finite mathematics. “Many worlds,” self-locating chance, unique branch decomposition, and empirical authority remain open or refused as inferences from that mathematics.


0. Scope and interpretation firewall


This paper asks what the L1/L2 boundary can explain about Everettian quantum mechanics after the required quantum structure is declared. It does not ask the degree ladder to produce that structure retroactively.

Three layers must remain separate:

1. **Representation:** a vector in a finite tensor-product Hilbert space can be expanded in relative-state form.
2. **Operational descent:** a restricted observer algebra can lose access to off-diagonal coherence, exactly or approximately.
3. **Ontology:** the terms in an expansion are asserted to be independently real worlds.

The first two admit conditional mathematics. The third does not follow from them.

Retained-carrier prerequisite: branches, records, coefficients, and record overlaps below live only inside the declared finite Hilbert/tensor carrier. A lower-degree flicker with no retained witness does not become a branch of zero weight or an unobserved world; it is non-exhibition relative to the basement and outside this imported representation.

This paper does not claim:

* that the GTOC basement derives quantum mechanics;
* that an expansion term is a world;
* that decoherence is collapse or ontological splitting;
* that branch weights are chances, caring measures, or subjective probabilities;
* that a preferred basis is selected by L1 normalization;
* that unitary evolution, tensor composition, partial trace, or record states are free;
* that Everettian and non-Everettian interpretations are empirically distinguished here;
* that representation, evidence, or a successful calculation mints authority.

### Import Ledger 0

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| finite L1 weights | `delta2` | Paper 2 / Paper 010 | available as proportions, not chance |
| complex L2 amplitudes | not earned | Paper 7 Q1-Q2 / Paper 010 | **IMPORTED** |
| tensor product and partial trace | not earned | Paper 8 import register | **IMPORTED** |
| Everettian ontology | nowhere derived | interpretive proposal | **OPEN / NOT ADMITTED AS THEOREM** |
| authority | never inferred | GTLA firewall | `None` |

**Connective audit.** The numbered layers are distinctions in exposition, not a physical succession.
**Genesis-Bias audit.** Hilbert and record carriers are declared inputs, not hidden substrates presented as derivations.


1. Declared finite relative-state carrier


Let $\mathcal{H}_S$ and $\mathcal{H}_E$ be finite-dimensional complex inner-product spaces. Let $\{|i\rangle\}$ be an orthonormal family in $\mathcal{H}_S$, and let each $|E_i\rangle\in\mathcal{H}_E$ be normalized. Declare

$$
|\Psi\rangle=\sum_{i=1}^n c_i|i\rangle\otimes|E_i\rangle,
\qquad
\sum_i|c_i|^2=1.
$$

Because the system vectors are orthonormal, $|\Psi\rangle$ is normalized even when the record vectors overlap.

### Definition 1.1 - L1 branch shadow

The branch-weight projection is

$$
\mathcal{B}_1(|\Psi\rangle)=w,
\qquad
w_i=|c_i|^2,
\qquad
\sum_iw_i=1.
$$

It retains nonnegative mass and forgets:

* coefficient phase;
* record overlap;
* off-diagonal coherence;
* the basis and factorization that defined the terms;
* every ontological interpretation of those terms.

### Definition 1.2 - Relative record family

The Gram matrix of records is

$$
G_{ij}=\langle E_j|E_i\rangle.
$$

The matrix `G` is positive semidefinite and has `G_ii=1`. It is the finite witness of how strongly the declared records remain mutually coherent.

### Definition 1.3 - Imported dynamics

When a branching description is produced by an isometry `V`, its action is additional structure:

$$
V:|i\rangle|E_0\rangle
\longmapsto
\sum_\alpha r_{i\alpha}|i,\alpha\rangle|E_{i\alpha}\rangle.
$$

No map of this kind is forced by L1 weights. Its isometric or unitary law must be stated and checked.

### Import Ledger 1

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| finite complex inner-product spaces | not earned | carrier declaration | **IMPORTED - Q1/Q2** |
| tensor factorization $\mathcal{H}_S\otimes\mathcal{H}_E$ | not earned | carrier declaration | **IMPORTED** |
| orthonormal system family | not earned | basis declaration | **IMPORTED** |
| normalized record vectors | not earned | packet hypothesis | **DECLARED** |
| branch/world semantics | not mathematical datum | - | **NOT CLAIMED** |

**Connective audit.** “Produced by” in Definition 1.3 refers to the declared map, not an unpriced causal story.
**Genesis-Bias audit.** The factorization is explicitly declared and can be varied; it is not treated as an antecedent natural partition.


2. Exact descent from L2 coherence to an L1 diagonal


### Theorem 2.1 - Reduced-state formula

The reduced state on `H_S` is

$$
\boxed{
\rho_S=\operatorname{Tr}_E|\Psi\rangle\langle\Psi|
=\sum_{i,j}c_i\overline{c_j}
\langle E_j|E_i\rangle |i\rangle\langle j|
}.
$$

**Proof.** Expand the rank-one operator:

$$
|\Psi\rangle\langle\Psi|
=\sum_{i,j}c_i\overline{c_j}
|i\rangle\langle j|\otimes|E_i\rangle\langle E_j|.
$$

The partial trace sends $|E_i\rangle\langle E_j|$ to $\langle E_j|E_i\rangle$. Substitution yields the formula. $\square$

### Corollary 2.2 - Orthogonal-record diagonalization

If the record family is orthonormal, then

$$
\rho_S=\sum_i w_i|i\rangle\langle i|.
$$

The local state is exactly its L1 branch shadow in the declared basis.

This is a descent statement, not an ontology statement. The global vector remains a coherent pure vector unless an additional nonunitary operation or interpretive rule is supplied.

### Definition 2.3 - Off-diagonal coherence mass

Let

$$
\rho_{\mathrm{diag}}=\sum_iw_i|i\rangle\langle i|,
$$

and define

$$
\Phi_{\mathrm{off}}
=\sum_{i\ne j}|c_i|\,|c_j|\,
|\langle E_j|E_i\rangle|.
$$

This is the entrywise L1 mass of the off-diagonal residual in the declared basis. It is basis- and factorization-relative, and the packet must retain that dependence.

### Theorem 2.4 - Finite local expectation bound

For every system operator `A` with operator norm `||A||_op <= 1`,

$$
\left|
\operatorname{Tr}(A\rho_S)
-\operatorname{Tr}(A\rho_{\mathrm{diag}})
\right|
\le \Phi_{\mathrm{off}}.
$$

**Proof.** In the declared orthonormal basis, every matrix entry satisfies `|A_ji|<=||A||_op<=1`. Therefore

$$
\begin{aligned}
\left|\operatorname{Tr}A(\rho_S-\rho_{\mathrm{diag}})\right|
&=\left|\sum_{i\ne j}A_{ji}c_i\overline{c_j}
\langle E_j|E_i\rangle\right|\\
&\le\sum_{i\ne j}|c_i|\,|c_j|\,
|\langle E_j|E_i\rangle|
=\Phi_{\mathrm{off}}.
\end{aligned}
$$

$\square$

The theorem gives a finite operational meaning to approximate decoherence: if `Phi_off` is small, bounded system-only observables cannot strongly distinguish the reduced state from its diagonal shadow. It does not say the global coherence vanished.

### Import Ledger 2

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| density operator and partial trace | not earned | Q-gated package | **IMPORTED** |
| diagonal L1 shadow | `delta2` weights plus imported basis | Corollary 2.2 | conditionally derived |
| operator norm and expectation | not earned | finite Hilbert package | **IMPORTED** |
| decoherence interpretation | contact reading | Theorem 2.4 | **INTERPRETIVE, bounded by exact inequality** |
| collapse | not supplied | - | **REFUSED as inference** |

**Connective audit.** “Reduced” is a mathematical restriction, not temporal decay.
**Genesis-Bias audit.** The observer restriction is a declared algebra/factorization, not a view from an unindexed external observer.


3. LGGR: locally diagonal, globally coherent


The local/global gap is a direct instance of Local-to-Global Gluing Residual.

### Definition 3.1 - Observer-relative ZeroRel

For a declared accessible operator profile, write

$$
\rho\sim_O\sigma
\quad\Longleftrightarrow\quad
\operatorname{Tr}(A\rho)=\operatorname{Tr}(A\sigma)
\text{ for every }A\in\mathcal{A}_O.
$$

To remain finitely certifiable, the packet must either declare equality of exact reduced density matrices, or exhibit a finite spanning family of accessible operators on which equality is tested. For system-only access, equality of reduced states is the corresponding zero relation. For diagonal-only access, equality of the diagonal weights is enough. The scope `O` is part of the packet; it may not be erased.

### Witness 3.2 - Same local L1 shadow, different global phase

Let $|E_0\rangle,|E_1\rangle$ be orthonormal and define

$$
|\Psi_\varphi\rangle
=\frac{|0\rangle|E_0\rangle
+e^{i\varphi}|1\rangle|E_1\rangle}{\sqrt2}.
$$

For every `varphi`,

$$
\operatorname{Tr}_E|\Psi_\varphi\rangle\langle\Psi_\varphi|
=\frac12|0\rangle\langle0|+\frac12|1\rangle\langle1|.
$$

The local L1 shadow is constant. The global projector

$$
P_+=|\Psi_0\rangle\langle\Psi_0|
$$

has expectation

$$
\langle\Psi_\varphi|P_+|\Psi_\varphi\rangle
=\frac{1+\cos\varphi}{2}.
$$

Global recoherence can therefore distinguish candidates that every system-only observable identifies.

### Witness 3.3 - Pure relative state versus classical mixture

At `varphi=0`, compare

$$
\rho_{\mathrm{pure}}=|\Psi_0\rangle\langle\Psi_0|
$$

with

$$
\rho_{\mathrm{mix}}
=\tfrac12|0,E_0\rangle\langle0,E_0|
+\tfrac12|1,E_1\rangle\langle1,E_1|.
$$

Both have the same reduced state and branch weights. Yet

$$
\operatorname{Tr}(P_+\rho_{\mathrm{pure}})=1,
\qquad
\operatorname{Tr}(P_+\rho_{\mathrm{mix}})=\tfrac12.
$$

The diagonal L1 description cannot decide whether global coherence survives.

### LGGR classification

| Region | Local verdict | Global gluing datum |
|---|---|---|
| each declared branch record | nonnegative weight `w_i` | coefficient and record phase relations omitted |
| system-only reduction | diagonal when records are orthogonal | global rank-one coherence survives |
| diagonal observer algebra | all `Psi_varphi` equivalent | recoherence projector distinguishes `varphi` |

The residual is not a contradiction. It is information discarded by the declared descent map.

### Import Ledger 3

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| observer algebra | declared comparison scope | K6 / this section | **DECLARED** |
| global recoherence projector | finite Hilbert package | witnesses | **IMPORTED** |
| LGGR classification | GTOC diagnostic | this section | conditional application |
| claim of actual recoherence in nature | not supplied | - | **NOT CLAIMED** |

**Connective audit.** “Survives” means nonzero in the global mathematical state, not persistence through physical time.
**Genesis-Bias audit.** Local/global is indexed by an explicit restriction map; no observer from nowhere is introduced.


4. Weight conservation under licensed branch refinement


### Theorem 4.1 - Parent weight equals the sum of child weights

Assume the imported isometry acts on one declared parent component as

$$
|i\rangle|E_0\rangle
\longmapsto
\sum_{\alpha=1}^{m_i}r_{i\alpha}
|i,\alpha\rangle|E_{i\alpha}\rangle,
$$

where the child product vectors are orthonormal and

$$
\sum_\alpha|r_{i\alpha}|^2=1.
$$

If the parent coefficient is `c_i`, then child weights

$$
w_{i\alpha}=|c_ir_{i\alpha}|^2
$$

satisfy

$$
\boxed{\sum_\alpha w_{i\alpha}=w_i}.
$$

**Proof.**

$$
\sum_\alpha|c_ir_{i\alpha}|^2
=|c_i|^2\sum_\alpha|r_{i\alpha}|^2
=|c_i|^2=w_i.
$$

$\square$

### Corollary 4.2 - Finite refinement consistency

Repeated licensed isometric refinements preserve total L1 weight at every finite cut of the declared refinement tree.

This statement is finite induction over a declared map family. It is not a probability theorem, a conservation law of physical worlds, or a proof that an infinite branch totality exists.

### Multiplicity warning

Equal counting of branch labels is not invariant under refinement. One component can be represented by many fine labels without changing its total weight. Therefore branch count cannot replace squared-norm weight unless an additional, representation-invariant counting theorem is supplied.

### Import Ledger 4

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| isometry and orthonormal children | not earned | theorem hypotheses | **IMPORTED** |
| squared-norm weight | not earned from L1 alone | coherent lift | **IMPORTED, then conserved conditionally** |
| finite induction | proof method | explicit refinement depth | standard mathematics |
| infinite branch totality | not supplied | - | **NOT CLAIMED** |
| chance semantics | not supplied | - | **OPEN** |

**Connective audit.** “Repeated” is finite proof iteration over an exhibited tree, not a continuum-time process.
**Genesis-Bias audit.** No completed universe of branches is assumed; each finite refinement carrier is declared.


5. Holonomy applies to recombination, not bare branching


Attach a U(1) transport to each edge of a finite history graph as in Quantum Contact 1. Coefficient phase accumulated along a history is then path transport.

### Theorem 5.1 - Pure branch-tree holonomy is trivial

If the underlying history carrier is a finite tree, every U(1) edge connection is gauge-equivalent to the unit connection.

**Proof.** Quantum Contact 1, Theorem 5.1. $\square$

### Consequence 5.2 - Branch phases need a comparison loop

No gauge-invariant phase can be assigned to one isolated branch edge. A relative phase becomes invariant only when two histories can be compared around a closed cycle. In a directed acyclic history graph, such a cycle can arise in the underlying undirected carrier through a diamond:

$$
x\to a\to y,
\qquad
x\to b\to y.
$$

The histories branch and rejoin. Their relative transport is the loop holonomy

$$
h=H(xay)\overline{H(xby)}.
$$

If the two contributions are coherently recombined, Quantum Contact 1 gives the resulting cross-term exactly.

### Definition 5.3 - Recombination obstruction

For every declared refinement diamond, retain:

$$
\Gamma_{\mathrm{diamond}}
=H(xay)\overline{H(xby)}.
$$

If a face fills the diamond, this is the exponentiated face curvature. If no face is declared, it is global loop data. A workflow that identifies the two refinement routes while discarding this datum performs an unlicensed quotient.

### Negative theorem 5.4 - What holonomy does not determine

Tree triviality implies that U(1) holonomy alone does not determine:

* whether a branch event occurs;
* the number of branch labels;
* a preferred decomposition basis;
* the reality or persistence of worlds;
* branch probability or rational credence;
* an observer's identity across branches.

Any proposal using holonomy for those tasks needs additional carrier structure and an explicit theorem. The present construction supplies neither.

### Import Ledger 5

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| U(1) history connection | not earned | Quantum Contact 1 | **IMPORTED** |
| history graph | workflow/representation carrier | this section | **DECLARED** |
| recombination readout | not earned | coherent merge | **IMPORTED Q2** |
| world multiplicity and identity | not mathematical output | - | **OPEN** |

**Connective audit.** Directed edges encode declared dependence; they are not automatically physical time.
**Genesis-Bias audit.** The history graph is a representation under test, not a pre-existing branching cosmos.


6. Basis, records, and the unresolved selection problem


The expression

$$
|\Psi\rangle=\sum_i c_i|i\rangle|E_i\rangle
$$

is basis- and factorization-relative. A different basis can redistribute diagonal and off-diagonal terms. The L1 shadow is therefore not an invariant branch ontology unless the basis-selection rule is itself part of the admissible structure.

### 6.1 What decoherence can conditionally supply

Given an imported interaction, tensor factorization, coarse-graining, and stability criterion, one can search for record families with small overlaps and robust correlations. Theorem 2.4 then bounds local deviations from a diagonal description.

### 6.2 What remains open

The following are not supplied by the L1/L2 split:

* a unique factorization into system and environment;
* a unique preferred basis in degenerate or approximately stable sectors;
* an exact threshold at which an approximate record becomes a world;
* an invariant branch-counting rule under refinement;
* a theorem converting local diagonalization into global ontological plurality.

### OBSTRUCTION - Preferred branch basis

The following cannot be derived from branch weights alone: a unique physically privileged branch decomposition. What would have to be admitted: a system/environment factorization, dynamics, interaction Hamiltonian or channel, stability/coarse-graining criterion, tolerance, and empirical realization map. What is lost if it is admitted: the claim that Everettian branching follows from the L1 shadow or bare unitary representation alone.

### Import Ledger 6

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| basis and factorization | carrier declaration | Section 1 | **IMPORTED** |
| decoherence dynamics | unavailable | contact proposal | **IMPORTED if used** |
| robustness/coarse-graining | unavailable | selection criterion | **IMPORTED** |
| unique preferred basis | nowhere proved | obstruction | **OPEN** |

**Connective audit.** Stability requires a declared dynamics or comparison family; it is not smuggled as temporal persistence.
**Genesis-Bias audit.** No natural system/environment split is presumed before its packet declaration.


7. Probability and ontology do not descend with the diagonal


The branch weights form a finite probability valuation on the declared branch partition. No chance, credence, or typicality interpretation follows from normalization.

The following candidate readings remain distinct:

* frequency over repeated declared trials;
* credence of an indexed observer;
* decision-theoretic caring measure;
* typicality measure over branches;
* objective chance;
* mere squared-norm bookkeeping.

Equality of the numbers does not prove equality of these interpretations.

### Proposition 7.1 - Representation does not terminalize ontology

The existence of an exact relative-state expansion does not entail that its terms are independently real worlds. `[SCOPE FENCE]` `[NON-ENTAILMENT UNDER DECLARED INTERFACE]` `[REFUSED PROMOTION]`

**Reason.** Expansion terms depend on imported factorization and basis choices. The formalism supplies amplitudes and correlations but no predicate `IsWorld`, no identity criterion across refinements, and no ontology terminalizer. Merely relabeling expansion terms as worlds, while leaving the mathematical and empirical interface unchanged, adds no packet-distinguishable prediction. The entailment is therefore absent from the declared interface.

This is a boundary result, not a proof that Everettian ontology is false.

### Proposition 7.2 - Diagonalization is not collapse

When record states are orthogonal, the reduced state is diagonal while the global state can remain pure and recoherable. Therefore reduced-state diagonalization alone does not entail a nonunitary collapse of the global state.

**Proof.** Witnesses 3.2 and 3.3 have the same diagonal reduction but distinct global coherent and mixed states. $\square$

### OBSTRUCTION - Everettian probability

The following cannot be derived from finite normalized branch weights alone: why a pre-measurement observer should use those weights as subjective chance in a theory where all declared outcomes remain represented. What would have to be admitted: an observer-indexing rule, diachronic identity or successor relation, rationality axioms or a typicality postulate, and a theorem binding those assumptions to squared norm. What is lost if it is admitted: the claim that normalization alone derives Everettian probability.

### Import Ledger 7

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| normalized proportions | `delta2` plus L2 lift | Paper 010 | conditional mathematics |
| chance/credence/typicality | modality and normativity | not derived | **OPEN / IMPORT REQUIRED** |
| world predicate | ontology | not derived | **OPEN** |
| collapse | alternative dynamics | not supplied | **NOT INFERRED** |

**Connective audit.** “Pre-measurement” is interpretation vocabulary and requires an imported time/dynamics packet; it is not used in a proof.
**Genesis-Bias audit.** The paper does not posit a completed set of worlds from which an observer is selected.


8. GTOC obstruction packet


### Relative-state descent packet

| Field | Content |
|---|---|
| carrier | finite tensor-product Hilbert carrier, declared basis, and factorization |
| expansion | relative-state coefficients |
| records | record family and Gram matrix |
| descent | partial trace to reduced state |
| local access | declared accessible operator profile |
| `Phi_off` | off-diagonal coherence mass in the declared basis |
| ZeroRel | equality on the explicitly declared accessible algebra |
| allowed repair | declared partial trace, verified isometric refinement |
| forbidden repair | changing factorization, or declaring worlds without a licensed transition |
| terminal | conditional finite relative-state and reduced-state mathematics |
| authority effect | `None` |

### History-holonomy packet

| Field | Content |
|---|---|
| carrier | declared history graph |
| connection | edge phases |
| gauge action | local rephasings |
| faces | recombination diamonds or consistency faces |
| loop holonomy | recombination readout |
| allowed repair | gauge rephasing |
| terminal | conditional exact recombination obstruction |
| authority effect | `None` |

### Per-defect terminalization

| Defect | Terminal |
|---|---|
| reduced-state formula under declared Hilbert/tensor hypotheses | conditional exact result |
| approximate local diagonalization with explicit `Phi_off` bound | conditional bounded result |
| unlicensed Hilbert, tensor, partial-trace, or U(1) import | `OracleNeeded` |
| preferred basis from weights alone | `OpenObstruction` |
| branch count as probability | typed refusal pending a licensed theorem |
| branch representation promoted to many-worlds ontology | typed refusal as unsupported promotion |
| empirical or authority claim from representation alone | typed refusal; `AuthorityEffect::None` |

The per-defect split matters. A valid reduced-state calculation must not be rejected merely because ontology is open. Conversely, a correct calculation must not carry the open ontology through terminalization as if it had been proved.

### Import Ledger 8

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| GTOC packet and terminals | protocol layer | math spine / conductor design | **IMPORTED governance contract** |
| per-defect terminalization | GTOC-6 target | this paper's routing | design application; general theorem OPEN |
| authority firewall | GTLA | standing rule | `None` |

**Connective audit.** A terminal is a workflow classification, not an ontological end state.
**Genesis-Bias audit.** Every carrier and observer restriction is packet-visible; no oracle is hidden inside a repair.


9. Claim ledger


| ID | Claim | Status | Dependency / fence |
|---|---|---|---|
| QCE-C1 | The reduced-state formula contains record-overlap-weighted off-diagonal terms. | `[PROVEN, CONDITIONAL]` | imported finite Hilbert/tensor/partial-trace package |
| QCE-C2 | Orthogonal records make the reduced system state exactly diagonal with weights `\|c_i\|^2`. | `[PROVEN, CONDITIONAL]` | normalized record family |
| QCE-C3 | `Phi_off` bounds the expectation difference for every system operator of norm at most one. | `[PROVEN, CONDITIONAL]` | declared basis and finite operator package |
| QCE-C4 | Equal local L1 shadows can hide globally distinguishable coherent states. | `[PROVEN, CONDITIONAL]` | Witness 3.2 |
| QCE-C5 | A coherent pure state and an incoherent mixture can have the same reduced diagonal. | `[PROVEN, CONDITIONAL]` | Witness 3.3 |
| QCE-C6 | Squared-norm mass is conserved under the declared orthonormal isometric refinement. | `[PROVEN, CONDITIONAL]` | orthonormal child carrier and isometry coefficients |
| QCE-C7 | Every U(1) connection on a pure finite branch tree is gauge-trivial. | `[PROVEN, CONDITIONAL]` | Quantum Contact 1, Theorem 5.1 |
| QCE-C8 | Relative holonomy can govern coherent recombination around a history diamond. | `[PROVEN, CONDITIONAL]` | imported connection and coherent readout |
| QCE-C9 | Holonomy alone selects a preferred branch basis or world decomposition. | `[NoRule / Refused from current carrier]` | blocked by tree triviality and missing selection structure |
| QCE-C10 | Reduced-state diagonalization alone does not entail global physical collapse. | `[Refuted by finite counterexample]` | Witnesses 3.2-3.3; imported finite Hilbert package |
| QCE-C11 | Relative-state representation entails many-worlds ontology. | `[REFUSED unsupported promotion]` | no ontology predicate, identity criterion, or terminalizer |
| QCE-C12 | Normalized branch weights alone derive Everettian probability. | finite probability yes; chance interpretation `[OpenObstruction]` | observer/normative assumptions missing |

QCE-C10 records a conditional non-entailment witness; QCE-C11 records the still-open ontological promotion. Neither claims that collapse theories or Everettian ontology are false. Every positive theorem is conditional on imported quantum structure. No row has authority effect.

### Import Ledger 9

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| claim statuses | ODP vocabulary | series charter | **IMPORTED governance vocabulary** |
| source-local IDs | this paper | ledger | bookkeeping only |

**Connective audit.** Ledger order is editorial.
**Genesis-Bias audit.** Open interpretation rows prevent a representation from becoming an unpriced ontology.


10. Mechanization and adversarial program


### QC-EVE-PL1 - reduced-state finite algebra

Formalize finite system and record index types, a complex coefficient vector, a record Gram matrix, the reduced-state formula, orthogonal-record diagonalization, and the `Phi_off` expectation bound. Print the axiom set of every exported theorem.

### QC-EVE-PL2 - local/global witness

Mechanize `Psi_varphi`, its phase-independent reduced state, and the phase-dependent global projector expectation. Bind the pure-versus-mixture witness to exact rational/algebraic values at `varphi=0` and `varphi=pi` so the core regression does not depend on floating point.

### QC-EVE-PL3 - branch refinement conservation

Formalize a finite isometric refinement matrix and prove parent squared norm equals the sum of child squared norms. Add a refinement invariance test showing why raw branch count is representation-dependent.

### QC-EVE-PL4 - tree and diamond phase packet

Reuse the finite connection object from QC-SUP-PL1/2. Verify tree gauge triviality, diamond relative holonomy, and coherent recombination. Reject a packet that claims nontrivial holonomy on a tree without introducing a comparison edge or recombination.

### QC-EVE-PL5 - interpretation firewall tests

Add schema and policy tests that reject these promotion attempts:

* `branch_term -> IsWorld`;
* `diagonal_reduced_state -> global_collapse`;
* `normalized_weight -> objective_chance`;
* `decoherence_score < epsilon -> authority`;
* `model_says_preferred_basis -> gtoc_classification`.

The trusted host may record such strings as proposals or interpretations. It may not populate terminal or authority fields from them.

### Falsifiers and narrowing witnesses

The positive mathematics is refuted or narrowed by any valid counterexample to its explicit hypotheses. The interpretive boundary is narrowed only by a packet that supplies:

1. a basis/factorization selection rule;
2. an invariant branch identity criterion under refinement;
3. a probability theorem with its observer and rationality assumptions exposed;
4. an observable or terminal distinction attributable specifically to the ontology;
5. independent verification that the distinction is not already carried by the ordinary quantum formalism.

Absent such a packet, broader proposals remain welcome as candidates but cannot be promoted.

### Import Ledger 10

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| Lean/Rust mechanization | software workflow | future targets | **NOT YET EXECUTED** |
| schema firewall | conductor policy | future target | **OPEN** |
| empirical distinction | not supplied | falsifier list | **OPEN** |

**Connective audit.** “Future” and target numbering are project-management conventions.
**Genesis-Bias audit.** Verification can validate a formal implication but cannot act as an unindexed ontology certifier.


11. Conclusion


The finite relative-state formalism has a clean L1/L2 anatomy. Squared coefficient magnitudes produce a normalized L1 shadow. Record overlaps and coefficient phases populate the off-diagonal L2 residue. Orthogonal records make the local reduction exactly diagonal; small overlaps give a quantitative approximation bound. Global recoherence witnesses show why the diagonal shadow is not the whole state.

Holonomy strengthens this picture only where there are alternative routes that can be compared. It assigns an exact phase obstruction to recombination diamonds and 2-cell consistency. A bare branch tree has no such invariant. This prevents the attractive geometric language from doing work it cannot do: holonomy does not generate worlds, count them, select their basis, or interpret their weights.

The strongest honest conclusion is therefore conditional and divided. The relative-state representation and its descent formulas are mathematically coherent. They provide a useful language for local classical-looking records and globally retained coherence. The Everettian ontological reading remains a proposal above that representation. GTOC permits the proposal to be broad, but GTLA prevents it from acquiring a false terminal or authority effect.

### Import Ledger 11

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| relative-state synthesis | imported quantum carrier | Sections 1-10 | conditional only |
| worlds, chance, preferred basis | not derived | open defects | **OPEN** |
| authority | never minted | terminal firewall | `None` |

**Connective audit.** The conclusion states logical dependence, not a genesis sequence.
**Genesis-Bias audit.** No wavefunction, branch tree, or observer scope is presented as an antecedent domain beyond its declared carrier.


References

1. [`qm_063_holonomy_structured_superposition.md`](qm_063_holonomy_structured_superposition.md) (Holonomy-Structured Superposition).
2. [`qm_072_bit_shadow_and_qubit.md`](qm_072_bit_shadow_and_qubit.md) (The Bit-Shadow and the Qubit).
3. [`qm_073_correlation_separability_finite_bell.md`](qm_073_correlation_separability_finite_bell.md) (Correlation, Separability, and Finite Bell Bounds).
4. [`qm_020_born_normalization_and_conditional_hilbert_lift.md`](qm_020_born_normalization_and_conditional_hilbert_lift.md) (Born Normalization and Conditional Hilbert Lift).
5. [`qm_091_deutsch_everett_wolfram_promotion_error.md`](qm_091_deutsch_everett_wolfram_promotion_error.md) (Formal Possibility Is Not Physical Realization).
6. [`qm_003_residual_density_calculus_l1_l2_boundary.md`](qm_003_residual_density_calculus_l1_l2_boundary.md) (Residual Density Calculus).
7. H. Everett III, [“Relative State” Formulation of Quantum Mechanics](https://doi.org/10.1103/RevModPhys.29.454), *Reviews of Modern Physics* 29 (1957), 454-462.
8. B. S. DeWitt and N. Graham, eds., [*The Many-Worlds Interpretation of Quantum Mechanics*](https://doi.org/10.1515/9781400868056), Princeton University Press (1973).
9. H. D. Zeh, [“On the Interpretation of Measurement in Quantum Theory”](https://doi.org/10.1007/BF00708656), *Foundations of Physics* 1 (1970), 69-76.
10. W. H. Zurek, [“Pointer Basis of Quantum Apparatus: Into What Mixture Does the Wave Packet Collapse?”](https://doi.org/10.1103/PhysRevD.24.1516), *Physical Review D* 24 (1981), 1516-1525.

References 7-10 locate the interpretive and decoherence discussion. They are not proof premises; their bibliographic metadata was verified against DOI and publisher records on 2026-07-17.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QCE-C1` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C1`) |
| `QCE-C2` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C2`) |
| `QCE-C3` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C3`) |
| `QCE-C4` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C4`) |
| `QCE-C5` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C5`) |
| `QCE-C6` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C6`) |
| `QCE-C7` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C7`) |
| `QCE-C8` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C8`) |
| `QCE-C9` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C9`) |
| `QCE-C10` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C10`) |
| `QCE-C11` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C11`) |
| `QCE-C12` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `094:QCE-C12`) |

<!-- claim-id-body-index:end -->
