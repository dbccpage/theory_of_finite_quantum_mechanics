---
documentation_contract: education-documentation/v1
title: "Example E12: Local Potentials & Global Obstruction"
kind: mathematical-reference
level: 12
status: active
maturity: research
claim_status: review_required
authority_effect: "None"
source_paths:
  - omega_engine_education/documentation/002_s_n/sn.md
  - omega_engine_education/documentation/002_s_n/_images/sn_12_observer_stack_dda.svg
---

# Example E12: Local Potentials & Global Obstruction

**AuthorityEffect:** None.
**GenesisEffect:** None (example level must never extend Genesis core merely by being constructed).
**Layer:** Example Specification
**ExampleId:** E12 (Candidate Example Level; not a normative Genesis core stage)
**Description:** Local potential witnesses and global circulation obstruction on an oriented triangle graph.

---

## 1. Schematic & Conceptual Architecture

> [!NOTE]
> **Epistemic Provenance Boundary:** S(0)–S(6) are this strand’s presentation labels; see the [source correspondence](../source_correspondence.md). Example $E12$ replaces broad subject headings with a finite problem whose witnesses, obstructions, and extension costs are displayed completely.

This level formalizes local potential feasibility vs. global circulation obstruction:
1. **Finite Seed Configuration:**
   - Oriented graph with edges $a \to b, b \to c, c \to a$. (These arrows are declared graph adapter incidences, not the intrinsic meaning of retained pair `<ab>`).
   - Free integer modules on vertices $C_0 = \mathbb{Z}^3$ and edges $C_1 = \mathbb{Z}^3$.
   - Coboundary matrix:
     $$d_0 = \begin{pmatrix} -1 & 1 & 0 \\ 0 & -1 & 1 \\ 1 & 0 & -1 \end{pmatrix}$$
   - Supplied edge record: $x = (x_{ab}, x_{bc}, x_{ca}) = (1, 0, 0)$.
   - Demand: Find an integer vertex potential $g \in C_0$ satisfying $d_0 g = x$.

---

## 2. Mathematical Presentation & Invariant Proofs

1. **Positive Local Witness:**
   - On the open path $a \to b \to c$, potential $g = (0, 1, 1)$ realizes the first two edge records:
     $$(d_0 g)_{ab} = g_b - g_a = 1 - 0 = 1, \qquad (d_0 g)_{bc} = g_c - g_b = 1 - 1 = 0$$
   - The third record predicted by $g$ is $(d_0 g)_{ca} = g_a - g_c = 0 - 1 = -1$, whereas the supplied third record is $x_{ca} = 0$.
2. **Exact Global Obstruction:**
   - Define circulation linear functional $I(x) := x_{ab} + x_{bc} + x_{ca}$.
   - For every vertex potential $g$, $I(d_0 g) = (g_b - g_a) + (g_c - g_b) + (g_a - g_c) = 0$. Thus $I$ is an exact invariant under potential repair.
   - For supplied edge data $x = (1, 0, 0)$, $I(x) = 1 + 0 + 0 = 1 \neq 0$.
   - *Conclusion:* No integer or rational potential $g$ realizes all three records.
3. **Completeness of Obstruction ($\operatorname{im}(d_0) = \ker(I)$):**
   - Conversely, if $I(x) = 0$, then potential $g = (0, x_{ab}, x_{ab} + x_{bc})$ satisfies $d_0 g = x$.
   - Therefore $\operatorname{im}(d_0) = \ker(I)$, and $I$ completely describes the quotient obstruction $C^1 / \operatorname{im}(d_0) \cong \mathbb{Z}$.

---

## 3. Priced Responses & Adapter Costs

- **Response Option A (Edge Data Repair):** If edge-data modifications are permitted and priced by number of changed entries, 1 changed entry is necessary and sufficient: replace $x_{ab}=1$ by $0$.
- **Response Option B (Obstruction Certificate):** If supplied edge evidence must remain fixed, the valid result is the exact obstruction certificate $I(x) = 1$. Additional potential terms or computation cannot repair it.
- **Adapter Cost:** Oriented incidence, integer group operations, and the explicit distinction between admissible potential changes and changes to supplied evidence.
- **Build Obligation:** Check $I \circ d_0 = 0$, replay local potential $g=(0,1,1)$, and prove both inclusions of $\operatorname{im}(d_0) = \ker(I)$.

---

## 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Proof that $I(x) = x_{ab} + x_{bc} + x_{ca} = 1$ obstructs integer and rational potential realization for $x=(1,0,0)$.
   - Proof that $\operatorname{im}(d_0) = \ker(I)$ completely characterizes exact potentials.
2. **What this does not support:**
   - Does not claim that local path consistency guarantees global potential existence.
   - Does not establish a normative Genesis core stage succession.
3. **The narrowest defensible claim:**
   - On the oriented triangle graph, edge data $x=(1,0,0)$ admits a local potential on $a \to b \to c$ but possesses circulation $I(x)=1$, obstructing global potential realization.
4. **Next test needed:**
   - Verify linear solver returns non-zero circulation certificate $I(x)=1$ for $x=(1,0,0)$.

