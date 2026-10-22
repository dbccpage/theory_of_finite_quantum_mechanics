Status: AI-drafted, awaiting human review.

# Derivation Note: CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT

**Target Node:** `CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT` (Rank 7 in `dag/pfp/campaign/derivation_queue.json`, UUID: `386edbd6-7df4-5ef3-9d65-53c4e3738576`)  
**Stage:** `CONSTRUCTOR_THEORY`  
**Prior Status:** `IMPORTED_ASSUMPTION`  
**Campaign Outcome:** `Reduced`  
**AuthorityEffect:** None.  
**Lean Module:** `lean4/CampaignCtMediatorEntanglement.lean`  
**Independent Check:** `checks/independent/ct-local-mediator-entanglement-import.py`  

---

## 1. Context and Problem Statement

The node `CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT` audits the central inference of two landmark 2017 proposals for testing the quantum nature of gravity:
1. C. Marletto and V. Vedral, *"Gravitationally-induced entanglement between two massive particles is sufficient evidence of quantum effects in gravity"*, Phys. Rev. Lett. 119, 240402 (2017), arXiv:1707.06036 (pp. 2–3).
2. S. Bose et al., *"A Spin Entanglement Witness for Quantum Gravity"*, Phys. Rev. Lett. 119, 240401 (2017), arXiv:1707.06050 (pp. 1–2).

The core conceptual claim of both papers can be stated as follows:
> If two spatial quantum systems $Q_1$ and $Q_2$ start in an unentangled (separable) state, interact only locally through an intermediary mediating system $M$ (with no direct interaction between $Q_1$ and $Q_2$, obeying Principle I locality), and end in an entangled state of $Q_1 + Q_2$, then the mediator $M$ cannot be a classical medium.

In Marletto–Vedral, "classical medium" is formalized in constructor theory: $M$ must possess at least two non-commuting incompatible observables whose union is not an information variable. In Bose et al., "classical mediator" is formalized in quantum information theory: any mediator described by classical states or local operations assisted by classical communication (LOCC) cannot create entanglement from a separable state.

The repository `theory_of_finite_quantum_mechanics` has no continuum gravity model (TFQ-0084 is a finite discrete shadow only). The purpose of this derivation is to establish the strongest honest outcome (`Reduced`): reducing the mediated entanglement inference to the exact finite-dimensional theorem that local quantum operations preserve Schmidt rank and cannot create concurrence from a separable state, while isolating the physical hypothesis that gravity acts as such a mediator as an imported external premise.

---

## 2. Mathematical Reduction to Finite-Dimensional Local Rank Invariance

Let $Q_1$ and $Q_2$ be two qubits with state space $\mathbb{C}^2 \otimes \mathbb{C}^2$, with amplitudes evaluated over the Gaussian rationals $\mathbb{Q}(i)$.

### 2.1 Coefficient Matrix and Schmidt Determinant
A pure bipartite state vector
$$|\psi\rangle = c_{00} |00\rangle + c_{01} |01\rangle + c_{10} |10\rangle + c_{11} |11\rangle$$
is represented by its $2 \times 2$ coefficient matrix:
$$M = \begin{pmatrix} c_{00} & c_{01} \\ c_{10} & c_{11} \end{pmatrix}$$
The Schmidt determinant is:
$$\det(M) = c_{00} c_{11} - c_{01} c_{10}$$
A pure state is a product state ($|\psi\rangle = |a\rangle \otimes |b\rangle$) if and only if $M = a b^T$, which occurs if and only if $\mathrm{rank}(M) \le 1$, or equivalently:
$$\det(M) = 0$$
The squared concurrence of $M$ is:
$$C^2(M) = 4 |\det(M)|^2 = 4 \left( (\mathrm{Re} \det M)^2 + (\mathrm{Im} \det M)^2 \right)$$
Thus, $C^2(M) = 0$ for all pure product states, and $C^2(M) > 0$ for all entangled states.

### 2.2 Invariance Under Local Operations
Under an arbitrary local pure operation $A \otimes B$ (where $A, B \in \mathrm{Mat}_2(\mathbb{Q}(i))$ act on $Q_1$ and $Q_2$ respectively), the coefficient matrix transforms as:
$$M' = A M B^T$$
By the multiplicativity of the $2 \times 2$ determinant:
$$\det(M') = \det(A M B^T) = \det(A) \det(M) \det(B)$$
Therefore:
1. If the initial state is separable ($\det(M) = 0$), then under any local operation pair $(A, B)$:
   $$\det(M') = \det(A) \cdot 0 \cdot \det(B) = 0$$
   Consequently, $C^2(M') = 0$.
2. Local operations cannot raise Schmidt rank: a rank-$\le 1$ state remains rank-$\le 1$.
3. In any channel mediated by a classical medium (LOCC), each conditioning measurement branch acts on the pure state as a local operation $A_i \otimes B_j$. Thus, every pure branch output remains a product state with $\det = 0$.

### 2.3 The Entangling Interaction
Consider the entangling phase family from `lean4/FrontierEntanglingPhase.lean`:
$$\psi_u = \frac{1}{2} (1, 1, 1, u)^T \iff M_u = \frac{1}{2} \begin{pmatrix} 1 & 1 \\ 1 & u \end{pmatrix}$$
Its determinant is:
$$\det(M_u) = \frac{1}{4} (u - 1)$$
and its squared concurrence is:
$$C^2(M_u) = 4 |\det(M_u)|^2 = \frac{|u - 1|^2}{4}$$
- For $u = 1$, $M_1 = \frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix} = \left(\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)\right) \otimes \left(\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)\right)$ is a separable product state with $\det(M_1) = 0$ and $C^2(M_1) = 0$.
- For the exact Pythagorean unit phase $u = \frac{3 + 4i}{5} \in \mathbb{Q}(i)$:
  $$|u|^2 = \left(\frac{3}{5}\right)^2 + \left(\frac{4}{5}\right)^2 = 1$$
  $$u - 1 = \frac{-2 + 4i}{5} \implies |u - 1|^2 = \frac{4 + 16}{25} = \frac{20}{25} = \frac{4}{5}$$
  $$C^2(M_u) = \frac{4/5}{4} = \frac{1}{5} > 0$$

### 2.4 The Non-Classicality Obstruction
Suppose $Q_1$ and $Q_2$ are initialized in $M_1$ and interact locally via a mediator $M$.
If the mediator were classical (generating only LOCC transformations):
$$\forall (A, B), \quad \det(A M_1 B^T) = 0 \implies C^2(A M_1 B^T) = 0$$
However, the target state $M_u$ has:
$$\det(M_u) \ne 0 \quad \text{and} \quad C^2(M_u) = \frac{1}{5} > 0$$
Hence, no local operation pair $(A, B)$ can generate $M_u$ from $M_1$:
$$\forall (A, B), \quad A M_1 B^T \ne M_u$$
The exact concurrence defect is:
$$C^2(M_u) - C^2(A M_1 B^T) = \frac{1}{5} - 0 = \frac{1}{5} > 0$$
Therefore, any mediator capable of generating the state $M_u$ from $M_1$ without direct $Q_1 \leftrightarrow Q_2$ coupling cannot be modeled as a classical / LOCC channel.

---

## 3. What is proved

1. **Determinant Multiplicativity:** Proved in Lean 4 (`applyLocalOp_det`) that for any $2 \times 2$ matrices $A, M, B$ over $\mathbb{Q}(i)$, $\det(A M B^T) = \det(A) \det(M) \det(B)$.
2. **Product State Rank Invariance:** Proved in Lean 4 (`local_op_preserves_product_det` and `local_op_concurrence_zero_of_separable`) that any local operation acting on a separable state preserves $\det = 0$ and $C^2 = 0$.
3. **Exact Pythagorean Concurrence:** Proved in Lean 4 (`M_entangled_concurrence`) and verified symbolically in Python that the Pythagorean unit phase $u = (3+4i)/5$ yields exact squared concurrence $C^2 = 1/5$.
4. **Mediator Non-Classicality:** Proved in Lean 4 (`classical_mediator_cannot_produce_entangled_state` and `no_local_op_produces_entangled_state`) that no classical mediator branch can produce $M_{\mathrm{entangled}}$ from $M_{\mathrm{separable}}$, with exact concurrence defect $1/5$ (`concurrence_gap_under_local_op`).
5. **Universal Phase Obstruction:** Proved in Lean 4 (`no_local_op_produces_phase_entangled_state`) that for every $u \ne 1$, no local operation pair can map $\psi_1$ to $\psi_u$.
6. **Abstract LOCC Reduction:** Proved in Lean 4 (`reduction_of_mediated_entanglement_inference`) that any channel generating non-zero Schmidt determinant from a zero-determinant state violates the LOCC condition.

---

## 4. What is assumed

1. **Finite Dimensionality:** The systems $Q_1, Q_2$ are modeled as 2-level finite-dimensional quantum systems with amplitudes in $\mathbb{Q}(i)$.
2. **Locality Assumption (Principle I Locality):** Direct interaction between $Q_1$ and $Q_2$ is strictly zero; all mediation occurs through $M$.
3. **Information-Theoretic Definition of Classical Mediator:** A classical mediator cannot transmit quantum coherence without measurement and classical communication; any channel it induces is an LOCC channel.
4. **Physical Gravity Hypothesis (Imported):** The claim that physical Newtonian or relativistic gravitational interaction corresponds to such a mediated quantum phase gate is taken as an imported hypothesis from Marletto–Vedral (2017) and Bose et al. (2017). The repository has no continuum gravity model.

---

## 5. What is open

1. **Continuum Quantum Field Theory:** Extending the finite Gaussian-rational qubit model to infinite-dimensional continuous-variable Fock spaces or field operators.
2. **Relativistic Gravitational Mediation:** Formulating the mediator in curved spacetime with local diffeomorphism gauge symmetry rather than an operational mediator channel.
3. **Connection to TFQ-0084:** Connecting this local mediator rank preservation to the Regge, spin-foam, and relational certificates in `TFQ-0084` (currently recorded as gap route `FRO-R-BACK-CT-MEDIATOR-TO-TFQ0084`).
