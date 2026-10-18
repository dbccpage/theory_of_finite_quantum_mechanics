# Relational Point Coincidence, Witnessed Difference, and Dressing Field Normal Forms

*Subtitle:* Colliding the Dressing Field Method with the Witnessed Difference Programme: Relational Spacetime, Heath's Theorem, and Exact Obstruction Quotients

*Author:* Jeremy H. Carroll

*Date:* 2026-10-01

*License:* Creative Commons Attribution 4.0 International (CC-BY-4.0)

*Status:* Pre-Print (v1.0). Supersession 2026-10-06: the live reading of point coincidence is a superkey in the Witnessed Difference monograph, Appendix O.6. `VERIFIED` on `CLM-GR003-001` is this frozen candidate-key text. Minimality of \(\mathcal{K}\) is not the live claim.

---

> **Vocabulary and Claim Discipline Note.** This paper operates inside the Calculus of Obstruction, Descent, and Authority (CODA) and Witnessed Difference Programme (WDP) discipline. Claims are scoped strictly to finite relational schemas, discrete cell complexes, and declared algebraic models. We do not claim to derive continuous General Relativity from discrete bits, nor to solve quantum gravity, nor to establish universal physical laws. Results are conditional on declared hypotheses, evaluated in exact rational arithmetic over $\mathbb{Q}$ or formal relational algebra. In accordance with strict claim hygiene:
> - "supports" or "exhibits in this discrete model" replaces ungrounded proof claims;
> - "guarantees under declared assumptions" replaces unconditional guarantees;
> - "failure mode" replaces speculative assertions of fundamental flaws.

---

## Abstract

In general-relativistic gauge field theories, the conjunction of Einstein's hole argument and the Kretschmann--Komar--Bergmann--Rovelli point-coincidence argument strips bare manifold points of physical individuality: physical spacetime events exist only as relational coincidences of dynamical fields. Recently, François and Ravera (arXiv:2510.19845) introduced the Mechanical Field Space (MFS) and the Dressing Field Method (DFM) to formulate mechanics as a general-relativistic gauge theory and systematically reduce gauge symmetries without gauge-fixing cuts or artificial boundary anomalies, motivating a program of Relational Quantization (RQ).

In this work, we establish a formal collision between the François--Ravera relational framework and Carroll's Witnessed Difference Programme (WDP), Projection Obstruction calculus, and Multi-Scale Simplicial (MSS-N) tower. By modeling spacetime events as tuples in a relational database schema under `panep-relational-algebra-theory`, we demonstrate:

1. **Point Coincidences as Relational Candidate Keys:** Four functionally independent scalar field observables $\mathcal{K} = \{\phi^0, \phi^1, \phi^2, \phi^3\}$ constitute a candidate key for the event relvar, establishing the functional dependency $\mathcal{K} \to \mathcal{U}$. Physical point identity is precisely relational tuple identity under the candidate key.
2. **Lossless Decomposition via Heath's Theorem:** Heath's theorem of relational algebra guarantees that decomposing an event relation across distinct observer sheets parameterized by $\mathcal{K}$ is strictly lossless ($r = \pi_{\mathcal{K} A}(r) \bowtie \pi_{\mathcal{K} B}(r)$), eliminating coordinate update anomalies without discarding physical degrees of freedom.
3. **Dressing as Oblique Cochain Projection:** The Dressing Field Method corresponds to a nonlinear retraction $\Pi$ on the field carrier with vanishing coboundary defect, factorizing gauge redundancies into basic invariants without introducing boundary edge-modes.
4. **Relational Normal Forms:** We formalize two executable contract specifications: Relational Point Coincidence Normal Form (RPCNF) and Dressing Field Normal Form (DFNF).
5. **Local Green, Global Red in Relational Embeddings:** Even when every local chart satisfies RPCNF and admits independent scalar fields (Green locally), the global relational transition structure may exhibit non-trivial cochain obstruction $\Phi_1([\omega]) > 0$ and holonomy defect $\Gamma_2$, certified by exact rational dual witnesses ($D^T w^* = 0, \|w^*\|_\infty \le 1$) over $\mathbb{Q}$.

---

## 1. Introduction and Conceptual Foundations

### 1.1 The Substantivalist Fallacy and the Point-Coincidence Argument

Standard textbook general relativity introduces spacetime as a smooth four-dimensional pseudo-Riemannian manifold $(M, g_{\mu\nu})$. In this presentation, points $p \in M$ are treated as preexisting geometric containers upon which physical fields (the metric tensor $g_{\mu\nu}$, the electromagnetic potential $A_\mu$, matter fields $\psi$) are defined.

However, as realized by Einstein in his celebrated *hole argument* (1913–1915) and subsequently clarified by Kretschmann (1917), Komar (1958), Bergmann (1961), and Rovelli (1991), the diffeomorphism covariance $\operatorname{Diff}(M)$ of the theory fundamentally undermines this substantivalist interpretation:

1. Let $U \subset M$ be an open region devoid of matter ("the hole").
2. Let $\psi: M \to M$ be a smooth diffeomorphism that is the identity on $M \setminus U$ but non-trivial inside $U$.
3. If $g$ is a solution to Einstein's field equations, then the pullback $\psi^* g$ is also a mathematically valid solution.
4. If the manifold point $p \in U$ possesses physical identity independently of the fields, then $g(p)$ and $(\psi^* g)(p)$ represent two distinct physical states evolving from identical initial data on a Cauchy surface outside $U$, violating determinism.

The resolution accepted in modern relational physics is that **manifold points $p \in M$ carry zero physical meaning**. Physical spacetime points are defined exclusively by **point coincidences**: the intersection of physical dynamical fields. As Einstein stated in 1916:
> *"All our space-time verifications invariably amount to a determination of space-time coincidences... The introduction of a system of coordinates serves no other purpose than to facilitate the description of this totality of coincidences."*

### 1.2 François and Ravera: The Dressing Field Method and Relational Quantization

In recent work, François and Ravera (2025, arXiv:2510.19845) systematized this insight by demonstrating that even classical non-relativistic mechanics can be formulated as a 1D general-relativistic gauge field theory (Mechanical Field Theory, MFT) over a Mechanical Field Space (MFS).

In standard gauge theory, one typically deals with local symmetries by **gauge fixing** (choosing a slice through the gauge orbits). However, gauge fixing suffers from severe pathologies:
- It breaks manifest covariance;
- It introduces artificial boundaries, boundary edge-modes, and spurious boundary charges;
- It is obstructed globally by Gribov ambiguities.

To overcome this, François and Ravera apply the **Dressing Field Method (DFM)**. Let $P(M, H)$ be a principal bundle with gauge group $H$. A *dressing field* is a map $u: P \to G$ (where $H \subseteq G$) satisfying the specific equivariance property:
$$u(p \cdot h) = h^{-1} u(p), \quad \forall h \in H, \, p \in P$$
Given a gauge-dependent field $\phi$ transforming as $\phi^h = \rho(h^{-1})\phi$, the *dressed field*:
$$\phi^u \equiv \rho(u)\phi$$
is **strictly invariant (basic)** under $H$:
$$(\phi^u)^h = \rho(u^h)\phi^h = \rho(h^{-1} u)\rho(h^{-1})\phi = \rho(u)\phi = \phi^u$$
The DFM extracts the gauge-invariant physical degrees of freedom **without gauge fixing**. When applied to a clock field in MFT, the dressing field reproduces standard unparameterized mechanics and provides a clear conceptual foundation for **Relational Quantization (RQ)**: quantizing the basic, dressed degrees of freedom rather than the unphysical gauge-redundant space.

### 1.3 The Collision: Witnessed Differences, Oblique Retractions, and Relational Algebra

While François and Ravera develop this relational machinery within continuous differential geometry and infinite-dimensional field spaces, the **Witnessed Difference Programme (WDP)** (Carroll, 2026) grounds physical distinction in finite, discrete, and computationally verifiable carriers.

The collision of these two perspectives generates several foundational insights:

1. **Carrier Honesty:** A continuous manifold $M$ or infinite-dimensional field space $\Phi$ cannot serve as an unexamined primitive carrier. Physical differences must be carried by verifiable, discrete distinction structures (Genesis $\emptyset \to \{0, 1\}$, simplicial complexes, or relational databases).
2. **Relational Database Theory as Foundational Mechanics:** What physicists call a "point coincidence" is mathematically identical to a **candidate key** in relational database theory (`panep-relational-algebra-theory`). When four invariant scalar fields $\mathcal{K} = \{\phi^0, \phi^1, \phi^2, \phi^3\}$ are measured, they form a composite key that functionally determines all other field properties.
3. **Heath's Lossless Join Decomposition:** Decomposing field data across observer charts without coordinate artifacts is rigorously governed by Heath's theorem ($r = \pi_{\mathcal{K} A}(r) \bowtie \pi_{\mathcal{K} B}(r)$).
4. **Oblique Projection Obstruction:** The dressing field $u$ represents an oblique retraction $\Pi$ from unconstrained field data onto the relational submanifold. When applied to discrete lattices or finite networks, the retraction generates cochain residuals $Q_e = I - P_e$.
5. **Local Green, Global Red:** Local satisfaction of relational coincidences does not imply global topological embeddability. The obstruction is measured by the cochain quotient $\Phi_1([\omega])$ and certified by exact rational dual LP witnesses.

---

## 2. Spacetime as a Relvar: Dependency Theory and Point Coincidences

### 2.1 The Relational Spacetime Schema

In relational database theory (Codd 1970; Date 2004; Fagin 1977), we define a relation schema by an attribute universe $\mathcal{U}$ and a set of functional dependencies $\mathcal{F}$.

**Definition 2.1 (Relational Spacetime Schema).**  
A *Relational Spacetime Schema* $\mathcal{S}_{\text{ST}}$ is a pair $(\mathcal{U}, \mathcal{F})$ where:
1. $\mathcal{U} = \mathcal{K} \cup \mathcal{A}$ is a finite set of attribute names;
2. $\mathcal{K} = \{\Phi^0, \Phi^1, \Phi^2, \Phi^3\}$ is a distinguished quartet of physical scalar field observables (e.g., Kretschmann scalar $K_1 = R_{\alpha\beta\gamma\delta}R^{\alpha\beta\gamma\delta}$, Chern--Pontryagin scalar $K_2 = R_{\alpha\beta\gamma\delta}{}^*R^{\alpha\beta\gamma\delta}$, Euler scalar $K_3$, and a scalar matter field $\psi$);
3. $\mathcal{A} = \{A_1, A_2, \dots, A_m\}$ represents additional physical observables (energy density $\rho$, matter currents $j^\mu$, local invariant curvature eigenvalues);
4. $\mathcal{F}$ is a set of functional dependencies over $\mathcal{U}$.

A *spacetime event instance* $r$ is a finite relation (set of tuples) $r \subset \prod_{X \in \mathcal{U}} \operatorname{dom}(X)$. Each tuple $t \in r$ represents a witnessed physical event.

### 2.2 Point Coincidence as a Candidate Key

In standard general relativity, two events occur at the same spacetime point if they have the same coordinates $x^\mu$. But coordinates are physically unobservable.

In the relational formulation:
**Postulate 2.1 (Relational Point Coincidence).**  
Two physical event measurements $t_1, t_2 \in r$ occur at the **same physical spacetime point** if and only if their relational coordinate fields coincide:
$$t_1[\mathcal{K}] = t_2[\mathcal{K}] \implies t_1 = t_2$$

In database theory, this is the precise definition of a **superkey**:
$$\mathcal{K} \to \mathcal{U} \in \mathcal{F}^+$$
Since no proper subset of $\mathcal{K}$ suffices to parameterize a four-dimensional spacetime region, $\mathcal{K}$ is minimal, and therefore $\mathcal{K}$ is a **Candidate Key**.

**Theorem 2.1 (Equivalence of Point Coincidence and Key Uniqueness).**  
*Let $r$ be an instance of $\mathcal{S}_{\text{ST}}$. The relational point-coincidence principle holds in $r$ if and only if $\mathcal{K}$ is a candidate key for $r$.*

*Proof.*  
If $\mathcal{K}$ is a candidate key, then by definition, for all $t_1, t_2 \in r$, $t_1[\mathcal{K}] = t_2[\mathcal{K}] \implies t_1[\mathcal{U}] = t_2[\mathcal{U}] \implies t_1 = t_2$. Conversely, if $t_1[\mathcal{K}] = t_2[\mathcal{K}] \implies t_1 = t_2$, then $\mathcal{K}$ functionally determines all attributes in $\mathcal{U}$. Minimality follows from the four-dimensionality of the underlying local degrees of freedom. $\square$

---

## 3. Heath's Theorem and Observer Sheet Decomposition

### 3.1 Lossless Join Decomposition of Reference Sheets

A central problem in general relativity is how different observers, each carrying their own instruments (reference sheets), combine their local data without introducing coordinate distortions.

Let an observer $\alpha$ measure attributes $\mathcal{K} \cup X$, and an observer $\beta$ measure attributes $\mathcal{K} \cup Y$, where $\mathcal{U} = \mathcal{K} \cup X \cup Y$.

**Theorem 3.1 (Spacetime Lossless Decomposition via Heath's Theorem).**  
*Let $r(\mathcal{U})$ be a spacetime event relation satisfying the candidate key dependency $\mathcal{K} \to X$. Then the decomposition of $r$ into projections:*
$$r_1 = \pi_{\mathcal{K} \cup X}(r), \quad r_2 = \pi_{\mathcal{K} \cup Y}(r)$$
*is strictly lossless under natural join:*
$$r = r_1 \bowtie r_2$$

*Proof.*  
This is a direct instantiation of Heath's Theorem (Heath 1971; `panep-relational-algebra-theory`).  
1. By relational algebra definitions, $r \subseteq \pi_{\mathcal{K} X}(r) \bowtie \pi_{\mathcal{K} Y}(r)$ always holds.  
2. Let $t \in \pi_{\mathcal{K} X}(r) \bowtie \pi_{\mathcal{K} Y}(r)$. By definition of natural join, there exist $u, v \in r$ such that:
   $$t[\mathcal{K} X] = u[\mathcal{K} X], \quad t[\mathcal{K} Y] = v[\mathcal{K} Y], \quad u[\mathcal{K}] = v[\mathcal{K}]$$
3. Because $\mathcal{K} \to X$ holds in $r$, and $u[\mathcal{K}] = v[\mathcal{K}]$, it follows that $u[X] = v[X]$.  
4. Therefore, $t[\mathcal{K} X Y] = v[\mathcal{K} X Y] = v[\mathcal{U}] \in r$. Thus $\pi_{\mathcal{K} X}(r) \bowtie \pi_{\mathcal{K} Y}(r) \subseteq r$.  
5. Equality holds: $r = r_1 \bowtie r_2$. $\square$

### 3.2 Physical Implication: Elimination of Coordinate Update Anomalies

In substantivalist physics, if an observer updates their coordinate chart $x^\mu \mapsto x'^\mu$, every record in the database must be modified (an update anomaly). If two observers label the same physical event with different coordinates, a join produces spurious tuples (lossy join).

Under Theorem 3.1:
- The join is performed on physical invariant field values $\mathcal{K}$, not on arbitrary coordinate labels.
- The join is provably lossless.
- No update anomalies occur: changing a local coordinate chart does not alter the tuple values of $r$, because coordinates are not stored attributes in the normalized relvar.

---

## 4. The Dressing Field Method as an Oblique Cochain Retraction

### 4.1 Retractions and Normal Residuals

In Carroll's *Projection Obstruction for Factorized States* (2026), a projection $\Pi: X \to M$ onto a factorized or invariant submanifold generates a linear normal projector $Q = I - P$ and an associated rate of defect production.

In François and Ravera's framework, let $\mathcal{F}$ be the unconstrained field space on a manifold or discrete complex, which includes gauge-variant configurations. The gauge group $\mathcal{G} = \operatorname{Diff}(M) \ltimes \mathcal{H}$ acts on $\mathcal{F}$.

A dressing field $u: \mathcal{F} \to \mathcal{G}$ constructs a retraction:
$$\Pi_{\text{dress}}: \mathcal{F} \to \mathcal{F}_{\text{basic}}, \quad \phi \mapsto \phi^u = \rho(u)\phi$$

**Proposition 4.1 (Idempotence and Transversality of Dressing Retraction).**  
*The dressing map $\Pi_{\text{dress}}$ satisfies:*
1. *$\Pi_{\text{dress}} \circ \Pi_{\text{dress}} = \Pi_{\text{dress}}$ (Idempotence);*
2. *$\Pi_{\text{dress}}(\phi^g) = \Pi_{\text{dress}}(\phi)$ for all $g \in \mathcal{G}$ (Gauge Invariance);*
3. *$\operatorname{im}(\Pi_{\text{dress}}) = \mathcal{F}_{\text{basic}}$ (Basic Submanifold).*

*Proof.*  
1. For any $\phi$, $\phi^u$ is basic, meaning its gauge transformation under any $h \in \mathcal{G}$ is trivial. For a basic field $\phi_0$, the canonical dressing field evaluates to the identity $u(\phi_0) = e$. Thus $\Pi_{\text{dress}}(\phi_0) = \rho(e)\phi_0 = \phi_0$, establishing idempotence $\Pi_{\text{dress}}^2 = \Pi_{\text{dress}}$.  
2. Under gauge transformation $\phi \mapsto \phi^g$, the equivariance $u(\phi^g) = g^{-1} u(\phi)$ implies:
   $$\Pi_{\text{dress}}(\phi^g) = \rho(u(\phi^g))\phi^g = \rho(g^{-1} u(\phi))\rho(g)\phi = \rho(u(\phi))\rho(g^{-1})\rho(g)\phi = \rho(u(\phi))\phi = \Pi_{\text{dress}}(\phi)$$
3. The image is precisely the set of $H$-basic fields by construction. $\square$

### 4.2 Contrast with Gauge Fixing

| Property | Gauge Fixing Slice | Dressing Field Method (DFM) |
|---|---|---|
| **Mechanism** | Submanifold cut $\sigma(x) = 0$ intersecting gauge orbits | Equivariant map $u: P \to G$ retracting fields to basic space |
| **Boundary Effects** | Generates artificial boundary edge-modes & boundary charges | Zero boundary edge-modes; preserves boundary covariance |
| **Global Obstruction** | Gribov copies preclude global smooth slices | Valid wherever an equivariant dressing field can be constructed |
| **Quantization Path** | Gauge-fixing + Faddeev--Popov ghosts + BRST cohomology | Direct path integral over basic moduli space $\mathcal{F}_{\text{basic}}$ |

---

## 5. Normal Form Contracts: RPCNF and DFNF

In accordance with the standards of `omega_engine_education/documentation/15_normal_forms/contracts_normal_forms/`, we establish two formal normal forms.

### 5.1 Relational Point Coincidence Normal Form (RPCNF)

**Definition 5.1 (RPCNF Contract Requirements).**  
A spacetime field database schema $\mathcal{S} = (\mathcal{U}, \mathcal{F})$ is in **Relational Point Coincidence Normal Form (RPCNF)** if and only if:
1. **1NF Compliance:** Every attribute domain consists of atomic, discrete, or exact rational scalar values.
2. **Key Minimality:** There exists a declared subset $\mathcal{K} \subset \mathcal{U}$ with $|\mathcal{K}| = 4$ such that $\mathcal{K} \to \mathcal{U} \in \mathcal{F}^+$.
3. **No Coordinate Contamination:** $\mathcal{U}$ contains no bare spacetime manifold coordinates ($x^0, x^1, x^2, x^3$). All attributes are scalar field invariants.
4. **Coincidence Determinism:** For every non-trivial functional dependency $X \to Y \in \mathcal{F}^+$, $X$ is a superkey containing $\mathcal{K}$.

*Excluded Anomalies:*
- *Coordinate Drift Anomaly:* Two distinct tuples representing the same physical event because they were recorded in different chart coordinates.
- *Spurious Disconnection Anomaly:* Physical event intersections missed because field coincidences were masked by coordinate transformations.

### 5.2 Dressing Field Normal Form (DFNF)

**Definition 5.2 (DFNF Contract Requirements).**  
A field theory state representation is in **Dressing Field Normal Form (DFNF)** if and only if:
1. **Dressing Certification:** An explicit dressing operator $u$ is declared with verified equivariance $u(\phi^g) = g^{-1} u(\phi)$.
2. **Basic Presentation:** The stored state vector $\phi_{\text{stored}}$ satisfies $\phi_{\text{stored}} = \Pi_{\text{dress}}(\phi)$.
3. **Ghost and Gauge Elimination:** No Faddeev--Popov ghost fields or unphysical longitudinal gauge degrees of freedom are stored in the state vector.
4. **Zero Gauge Residual:** The gauge coboundary defect $\delta_{\text{gauge}}(\phi_{\text{stored}}) = 0$ is verified identically.

*Excluded Anomalies:*
- *Gribov Ambiguity Anomaly:* Multi-valued state vectors arising from non-injective gauge-fixing slices.
- *Spurious Boundary Charge Anomaly:* Non-physical surface degrees of freedom induced by cutting gauge orbits at boundaries.

---

## 6. Obstruction Calculus: Local Green, Global Red in Relational Spacetimes

### 6.1 The Fallacy of Local Consistency

A central danger in relational physics is assuming that because relational point coincidences work locally in every neighborhood, they automatically assemble into a smooth global spacetime manifold.

In Carroll's *Local Green, Global Red Foundational Series* (`001_local_green_global_red_foundational_series`), we demonstrated that local exactness can coexist with severe global topological and differential obstructions.

**Theorem 6.1 (Relational Local Green, Global Red).**  
*There exist discrete relational spacetime configurations where:*
1. *Every local chart $U_i$ satisfies RPCNF and DFNF (Local Green);*
2. *Every local transition matrix between scalar fields has non-zero Jacobian determinant $\det\left(\frac{\partial \phi^I}{\partial \psi^J}\right) \ne 0$;*
3. *Yet the global 1-cochain of transition residuals $\omega \in C^1(K, \mathbb{Q})$ cannot be expressed as a coboundary $\omega = D \alpha$ for any 0-cochain $\alpha$, yielding a strictly positive obstruction quotient:*
   $$\Phi_1([\omega]) = \min_\alpha \|\omega - D \alpha\|_1 > 0$$

### 6.2 Exact Rational Dual Witness Certification

To certify this global obstruction without relying on numerical approximations or floating-point heuristics, we utilize exact linear programming (LP) duality over $\mathbb{Q}$:

The primal problem:
$$\min_{\alpha \in \mathbb{Q}^k} \|\omega - D \alpha\|_1$$
The exact dual problem:
$$\max_{w \in \mathbb{Q}^m} \langle w, \omega \rangle \quad \text{subject to} \quad D^T w = 0, \quad \|w\|_\infty \le 1$$

By strong LP duality:
$$\Phi_1([\omega]) = \langle w^*, \omega \rangle$$
Where $w^* \in \mathbb{Q}^m$ is a **divergence-free dual circulation witness** ($D^T w^* = 0$) bounded by $\|w^*\|_\infty \le 1$. If $\langle w^*, \omega \rangle > 0$, the existence of $w^*$ provides an unassailable finite certificate that the local relational data **cannot close globally**.

---

## 7. Mathematical Synthesis and Claim Register

### 7.1 Summary of Results

| Result | Mathematical Statement | Scope & Posture |
|---|---|---|
| **Point Coincidence Theorem** | $\mathcal{K} \to \mathcal{U} \iff$ Point Coincidence holds | Formal Relational Algebra |
| **Lossless Reference Sheet Join** | $r = \pi_{\mathcal{K} X}(r) \bowtie \pi_{\mathcal{K} Y}(r)$ via Heath's Theorem | Discrete Relational Schemas |
| **Dressing Retraction** | $\Pi_{\text{dress}}^2 = \Pi_{\text{dress}}, \, \Pi_{\text{dress}}(\phi^g) = \Pi_{\text{dress}}(\phi)$ | Discrete / Bundle Gauge Fields |
| **RPCNF & DFNF Contracts** | Normal form definitions excluding coordinate & gauge anomalies | Executable YAML Contracts |
| **Relational LGGR Obstruction** | $\Phi_1([\omega]) > 0$ certified by $D^T w^* = 0, \|w^*\|_\infty \le 1$ | Exact Rational $\mathbb{Q}$ LP Duality |

### 7.2 Explicit Non-Claims (Claim Hygiene)

1. **No Continuous GR Derivation:** This paper does not claim that smooth continuous Einstein manifolds emerge inevitably from discrete relational tuples.
2. **No Quantum Gravity Derivation:** This paper does not claim to have formulated a complete or predictive theory of quantum gravity.
3. **No Claim of Universal Field Independence:** Four scalar fields are not guaranteed to remain functionally independent everywhere; caustic singularities, gradient crossings, or degenerate points ($\mathrm{d}\phi^0 \wedge \dots \wedge \mathrm{d}\phi^3 = 0$) are explicit failure modes that require regional partitioning.
4. **Finite Setting Only:** All statements regarding cochain quotients and dual witnesses are established for finite cell complexes and finite relational tables over $\mathbb{Q}$.

---

## References

1. Einstein, A. (1916). *Die Grundlage der allgemeinen Relativitätstheorie*. Annalen der Physik, 49(7), 769-822.
2. François, J. T., & Ravera, L. (2025). *Mechanics as a general-relativistic gauge field theory, and Relational Quantization*. arXiv:2510.19845 [physics.gen-ph].
3. Kretschmann, E. (1917). *Über den physikalischen Sinn der Relativitätspostulate*. Annalen der Physik, 53, 575-614.
4. Komar, A. (1958). *Coordinate Invariants in General Relativity*. Physical Review, 111(4), 1182-1187.
5. Bergmann, P. G. (1961). *The General Theory of Relativity*. Handbuch der Physik, 4, 203.
6. Rovelli, C. (1991). *What is observable in classical and quantum gravity?* Classical and Quantum Gravity, 8(2), 297-316.
7. Codd, E. F. (1970). *A Relational Model of Data for Large Shared Data Banks*. Communications of the ACM, 13(6), 377-387.
8. Heath, I. J. (1971). *Unacceptable file operations in a relational database*. Proceedings of the 1971 ACM SIGFIDET Workshop, 19-33.
9. Date, C. J. (2004). *An Introduction to Database Systems* (8th ed.). Addison-Wesley.
10. Fagin, R. (1977). *Multivalued Dependencies and a New Normal Form for Relational Databases*. ACM Transactions on Database Systems, 2(3), 262-278.
11. Carroll, J. H. (2026). *The Witnessed Difference Programme: From Finite Distinction to Witnessed Measurement*. Omega Engine Atlas, F004/001/000.
12. Carroll, J. H. (2026). *Local Green, Global Red Foundational Series*. Omega Engine Atlas, F004/001/001.
13. Carroll, J. H. (2026). *Projection Obstruction for Factorized States*. Omega Engine Atlas, F004/002/000.
14. Carroll, J. H. (2026). *Constraint Closure Toy Model and the ℓ¹ Structure of Physical Law*. Omega Engine Atlas, F004/004/002.
