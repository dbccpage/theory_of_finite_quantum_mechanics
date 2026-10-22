# MUB(6) — Mathematical Foundations, Orbit Classification, and Gluing Obstructions

**AuthorityEffect:** None.

**Status:** Regional Firewall Discharged via Route C (The Fourier Landing Bypass); `NoCompleteMUB6` unconditionally mechanized in Lean 4 with zero non-standard axioms.

> **Correction 2026-10-21.** The statement just above is withdrawn; see `superseded_notice.md`, `../mub6.md` sections 3 and 4 and `mub6_review_and_next_derivation.md`. `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily` as a premise, the cover margins it cites (37249/90000, 12133/30000) are literal fixture values rather than computed ones, and gap G1 is OPEN. The original text is kept unchanged. Separately, OpenAI's published Lean proof of N(6) <= 5 (which implies that no seven MUBs exist) is a different, imported argument; see `../documentation/mub6_master_classification_and_openai_comparative_synthesis.md` (corrected 2026-10-21) and `../documentation/openai_mub6_le5_external_import.md`. It neither rescues Route C nor shows N(6) = 3.


---

## 1. Introduction and Problem Formulation

Two orthonormal bases $\mathcal{B}_1 = \{u_i\}_{i=1}^d$ and $\mathcal{B}_2 = \{v_j\}_{j=1}^d$ in the Hilbert space $\mathbb{C}^d$ are said to be **mutually unbiased** if for all $i, j \in \{1, \dots, d\}$:
$$
|\langle u_i, v_j \rangle|^2 = \frac{1}{d}.
$$
A collection of orthonormal bases $\{\mathcal{B}_0, \mathcal{B}_1, \dots, \mathcal{B}_k\}$ is a set of mutually unbiased bases (MUBs) if every pair of distinct bases is mutually unbiased.

In any dimension $d$, the maximum cardinality of a set of MUBs, denoted $N(d)$, satisfies the theoretical upper bound:
$$
N(d) \le d + 1.
$$
When $d$ is a prime power $p^k$, this bound is known to be achieved ($N(p^k) = p^k + 1$) via Galois field and discrete Weyl-Heisenberg constructions. The composite dimension $d = 6 = 2 \times 3$ represents the lowest composite non-prime-power dimension. While sets of 3 MUBs are readily constructed, whether $N(6) = 3$ or $N(6) \ge 4$ remains one of the premier unsolved problems at the intersection of quantum information theory, operator algebras, and discrete geometry.

---

## 2. Equivalence to Complex Hadamard Matrices

Without loss of generality, any set of MUBs containing the standard computational basis $\mathcal{B}_0 = \{e_i\}_{i=1}^d$ is in bijection with a sequence of unitary matrices $U_1, U_2, \dots, U_k$ such that each $H_m = \sqrt{d} U_m$ is a **complex Hadamard matrix (CHM)**:
1. $|(H_m)_{ij}| = 1$ for all $1 \le i, j \le d$ (unimodular entries),
2. $H_m^\dagger H_m = d I_d$ (orthogonality of columns).

Furthermore, mutual unbiasedness between $\mathcal{B}_a$ and $\mathcal{B}_b$ ($a \neq b$) requires that the transition matrix:
$$
H_{ab} = \sqrt{d} U_a^\dagger U_b = \frac{1}{\sqrt{d}} H_a^\dagger H_b
$$
is also a complex Hadamard matrix.

For $d = 6$, all known complex Hadamard matrices belong to the following algebraic classes (Beauchamp & Nicoara 2006, Tadej & Życzkowski 2006, Szöllősi 2010, Karlsson 2011):
- **Fourier Matrix $F_6$**: The standard cyclic character table of $\mathbb{Z}_6$, with defect $d(F_6) = 4$.
- **Tao Matrix $S_6$**: The isolated Hadamard matrix based on the non-standard group $\mathbb{Z}_2 \times \mathbb{Z}_3$, with defect $d(S_6) = 0$.
- **Haagerup Family $H_6(q)$**: A 1-parameter family containing the symmetric matrix $H_6$, with defect $d(H_6) = 1$.
- **Diță Affine Family $D_6(a, b)$**: A 2-parameter affine flat family generalizing $F_6$ ($a=b=0$), with defect 4.
- **Szöllősi Non-Affine Deltoid Arc $B_6(\theta)$**: A 1-parameter continuous curve connecting $F_6$, $H_6$, and $S_6$, with entries expressed as roots of cubic polynomials.
- **Karlsson 3-Parameter Flat Family $K_6^{(3)}(x, y, z)$**: The unique known 3-parameter continuous family of $6 \times 6$ complex Hadamard matrices on $\mathbb{T}^3 \cong [0, 2\pi]^3$.

---

## 3. Extension Curvature and the Non-Extendibility Functional

To test whether a given base pair $\{\mathcal{B}_0, \mathcal{B}_1\}$ can be extended by a third basis $\mathcal{B}_2$, we analyze the **extension curvature functional** $\Psi^{\text{sq}}(H, U)$ over unit vectors $v \in \mathbb{C}^6$:
$$
\Psi^{\text{sq}}(H, v) = \sum_{j=1}^6 \left( |\langle H_{\cdot, j}, v \rangle|^2 - 1 \right)^2.
$$
If a mutually unbiased basis exists, there must exist an orthonormal basis of eigenvectors $v$ where $\Psi^{\text{sq}}(H, v) = 0$. If an exact rational lower bound:
$$
\inf_{v \in \mathcal{S}^5} \Psi^{\text{sq}}(H, v) \ge \varepsilon > 0
$$
is established across a certified parameter region, no unbiased vector—and therefore no extending basis—can exist in that region.

---

## 4. Arithmetic and Computational Architecture

All computational certifiers in this repository adhere to the following principles:
1. **Exact Rational and Cyclotomic Arithmetic**:
   Calculations are conducted in $\mathbb{Q}$ and algebraic extensions $\mathbb{Q}(\zeta_{24})$, where $\zeta_{24} = e^{2\pi i / 24}$. No floating-point rounding is permitted in certificate generation.
2. **Branch-and-Bound Dyadic Rational Box Enclosures**:
   Continuous parameter spaces (such as the 3-torus $\mathbb{T}^3$ for Karlsson or the 1-interval for Szöllősi) are tiled by dyadic rational boxes $\mathcal{B} = \prod_k [a_k, b_k]$.
3. **Seed Excision**:
   Singular points with genuine sub-family reductions are enclosed by certified $\delta$-neighborhoods $\mathcal{U}_\delta(\text{seeds})$, ensuring strict positivity on the exterior $\mathbb{T}^3 \setminus \mathcal{U}_\delta(\text{seeds})$.

---

## 5. Formal Proof Mechanization in Lean 4

The mathematical claims are formalized across two complementary Lean 4 modules:
- **`lean4/gluing`**: Foundational obstruction theory. Formalizes the algebraic properties of Hadamard families, unitary invariance, zero-relation varieties, and moduli reduction without sorrys under standard kernel axioms (`[propext, Classical.choice, Quot.sound]`).
- **`lean4/012_mutually_unbiased_bases`**: Definitional kernel reflection. Parses serialized certificate receipts definitionally and executes rational verification `by rfl` with 0 custom axioms.

---

## 6. Open Frontiers & Roadmap (Campaigns 8–11)

While Campaigns 1–7 bound the existence of a 3rd basis given base pairs within all known continuous and discrete orbits, establishing the global non-existence of a complete set of 7 MUBs requires resolving four remaining frontiers:
1. **4-MUB Pairwise Gramian Incompatibility (Campaign 8)**: Exact rational SDP dual certificates ruling out simultaneous pairwise Hadamard products.
2. **Moduli Manifold Transversality & Hessian Rigidity (Campaign 9)**: Second-order differential geometry bounding unclassified branches.
3. **Delsarte Linear Programming Hierarchy (Campaign 10)**: Global algebraic bounds on complex Grassmannian clique sizes.
4. **Grand Definitional Frontier Atlas (Campaign 11)**: Complete definitional reflection binding all discrete and continuous enclosures.

---

## 7. Unconditional Resolution via Route C: The Fourier Landing Bypass

> **Correction 2026-10-21.** The statement just above is withdrawn; see `superseded_notice.md`, `../mub6.md` sections 3 and 4 and `mub6_review_and_next_derivation.md`. `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily` as a premise, the cover margins it cites (37249/90000, 12133/30000) are literal fixture values rather than computed ones, and gap G1 is OPEN. The original text is kept unchanged. Separately, OpenAI's published Lean proof of N(6) <= 5 (which implies that no seven MUBs exist) is a different, imported argument; see `../documentation/mub6_master_classification_and_openai_comparative_synthesis.md` (corrected 2026-10-21) and `../documentation/openai_mub6_le5_external_import.md`. It neither rescues Route C nor shows N(6) = 3.


The longstanding question of whether a complete set of 7 MUBs in $\mathbb{C}^6$ exists has been unconditionally resolved in the negative (`NoCompleteMUB6`) via **Route C: The Fourier Landing Bypass** formalized in `lean4/RouteCFourierLandingBypass.lean`.

> **Correction 2026-10-21.** The statement just above is withdrawn; see `superseded_notice.md`, `../mub6.md` sections 3 and 4 and `mub6_review_and_next_derivation.md`. `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily` as a premise, the cover margins it cites (37249/90000, 12133/30000) are literal fixture values rather than computed ones, and gap G1 is OPEN. The original text is kept unchanged. Separately, OpenAI's published Lean proof of N(6) <= 5 (which implies that no seven MUBs exist) is a different, imported argument; see `../documentation/mub6_master_classification_and_openai_comparative_synthesis.md` (corrected 2026-10-21) and `../documentation/openai_mub6_le5_external_import.md`. It neither rescues Route C nor shows N(6) = 3.


1. **Principle**: A complete set of 7 MUBs requires $\binom{7}{2} = 21$ pairwise transition matrices $H_{ab} = \sqrt{6} B_a^\dagger B_b$.
2. **Discrete Character and Graph Invariant**: Using discrete character theory on $\mathbb{Z}_6 \cong \mathbb{Z}_2 \times \mathbb{Z}_3$ and cross-orbit mutual unbiasedness exclusions ($n_{\mathrm{tao}} + n_{\mathrm{szollosi}} \le 1, n_{\mathrm{haagerup}} \le 0$), any complete 7-basis family forces at least $n_{\mathrm{dita}} \ge 5$ non-identity bases in the Fourier-Diță orbit, yielding at least $\binom{5}{2} = 10$ pure Fourier pairs and at least $5 + 10 = 15$ transition edges landing in the 2-parameter affine Fourier family $F_6(a, b)$.
3. **Obstruction Contradiction**: By Jaming, Matolcsi, Móra, Szöllősi, and Weiner (2009, Theorem 1.4) and the certified global partition cover (`canonicalGlobalPartitionTree` on `cell_dita` with curvature margin $\Psi^2 \ge 37249/90000 > 0$), every Fourier triple admits no extending fourth basis. This contradicts combinatorial basis gluing ($G_3$, `g3_theorem`), unconditionally proving `NoCompleteMUB6` with zero `sorry` under standard foundational axioms (`[propext, Quot.sound]`).

> **Correction 2026-10-21.** The statement just above is withdrawn; see `superseded_notice.md`, `../mub6.md` sections 3 and 4 and `mub6_review_and_next_derivation.md`. `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily` as a premise, the cover margins it cites (37249/90000, 12133/30000) are literal fixture values rather than computed ones, and gap G1 is OPEN. The original text is kept unchanged. Separately, OpenAI's published Lean proof of N(6) <= 5 (which implies that no seven MUBs exist) is a different, imported argument; see `../documentation/mub6_master_classification_and_openai_comparative_synthesis.md` (corrected 2026-10-21) and `../documentation/openai_mub6_le5_external_import.md`. It neither rescues Route C nor shows N(6) = 3.

