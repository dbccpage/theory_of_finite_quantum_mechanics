---
documentation_contract: symbol-game-documentation/v1
title: "s_n / S(n): The Genesis Presentation Tower, Four-Layer Architecture, and Epistemic Reflection Fences (v0.1 Pre-Print)"
kind: mathematical-reference
audience:
  - researchers
  - engineers
  - coding-agents
status: active
maturity: research
claim_status: review_required
authority_effect: "None"
source_paths:
  - omega_engine_education/documentation/002_s_n/sn.md
prerequisites:
  - 002_s_n/README.md
  - 003_minimal_symbol_system_n_mssn/papers/000_mssn/paper.md
aliases:
  - s_n
  - S(n)
  - genesis_tower_architecture
related:
  - ../../../003_minimal_symbol_system_n_mssn/papers/001_pregenesis_through_mssn/pregenesis_through_mssn.md
  - ../../../003_minimal_symbol_system_n_mssn/README.md
  - ../../../001_genesis/README.md
  - ../../../030_the_symbol_game_proposal_fidelity_protocol_pfp/README.md
last_verified: 2026-09-29
---

# $s_n$ / $S(n)$: The Genesis Presentation Tower, Four-Layer Architecture, and Epistemic Reflection Fences

**AuthorityEffect:** None.\
**Genesis Provenance:** Sealed blind derivation from opaque seed `<>` ([19L57G1](https://github.com/dbccpage/19L57G1)).\

---

## 1. The Cardinal Rule & Epistemic Separation

The fundamental architectural principle governing all $S(n)$ documentation is the strict separation between internal Genesis derivation and external mathematical description:

> **Mathematics may describe or verify an $S(n)$ structure, but mathematics cannot be the reason that the next $S(n)$ structure exists unless Genesis itself forces it.**\
> *Physics is even further removed: it can be an application or interpretation only.*

To prevent representation choices from feeding back into the derivation and corrupting the ontology, the system enforces two universal laws:

$$\boxed{S(n+1) \text{ may contain only structure forced by an unresolved Genesis obstruction at } S(n).}$$

$$\boxed{\text{A mathematical realization } R(S(n)) \text{ has no authority to extend } S(n).}$$

### The Epistemic One-Way Arrow

The connection between Genesis and mathematical formalisms is strictly one-way:

$$S(n) \xrightarrow{\quad\rho\quad} R(S(n))$$

1. **One-Way Mapping:** Genesis states and receipts may be mapped into mathematical representations $\rho(S(n))$ (e.g. graphs, chain complexes, categories).
2. **Reflection Bridge Required:** Properties proved inside a mathematical shadow return to Genesis **only through an explicitly proved faithful reflection bridge**.
3. **Zero Generative Authority:** Discovering an interesting, symmetrical, or rich mathematical structure inside $R(S(n))$ (such as Ramanujan eigenvalues, de Rham cohomology, or Regge deficits) **confers zero authority to create or extend the next Genesis stage**.

---

## 2. WDP Harmonization & The Anti-Slop Definition Firewall

To eliminate semantic drift and "definition spread" between the **Witnessed Difference Programme (WDP)** (codified in [`witnessed_difference_programme.md`](../../../witnessed_difference_programme/witnessed_difference_programme.md) and [`genesis_to_wdp_derivation_programme.md`](../../../witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md)) and the **$S(n)$ Carrier Tower**, all models and documentation must adhere to the unified triadic architecture:

$$\boxed{\text{Genesis (Derivation)} \quad\xrightarrow{\quad\text{admissions \& fidelity}\quad}\quad \text{WDP (Calculus)} \quad\xrightarrow{\quad\text{presentation}\quad}\quad S(n) \text{ (Presentation Tower)}}$$

### 2.1 The Binary Germ, Endpoint Support ($\Delta_{\mathrm{support}} = 2$), and Witness Multiplicity

For an irreflexive relation $R$,
$$R(a,b) \implies a \neq b$$
Otherwise $R(a,b)$ would become $R(a,a)$, contradicting irreflexivity. Consequently, every admitted primitive cut has **exactly two distinct endpoints**:
$$\Delta_{\mathrm{support}}(a,b) := |\{a,b\}| = 2$$
This provides the mathematically defensible meaning for the constant $\Delta_w = 2$. It applies wherever an inhabited primitive cut exists; the ground and singleton stages contain no such cut.

#### Separation of Quantities

| Quantity | What Follows from an Inhabited Irreflexive Cut | Source Verification / Lean 4 Evidence |
| :--- | :--- | :--- |
| **Distinct endpoints of that cut** | **Exactly 2** ($\Delta_{\mathrm{support}} = 2$) | `PrimDiff.irrefl_witness_ne` ($a \neq b$) |
| **Minimum carrier size supporting it** | **2** | `PrimDiff.no_witness_on_subsingleton` |
| **Witness occurrences or certificates** | **May be 1, 2, or more** | `PrimDiff.single_oriented_witness_consistent` (1 fwd witness, 0 rev) |
| **Newly supplied carrier elements** | **May be 0** (when both endpoints already exist) | `sn_core.py` stage transitions |
| **Operator count or description cost** | Depends on declared accounting model ($\mu_1, \mu_2$) | `cost1_insufficient_general` |
| **Total carrier size** | Can grow while each primitive cut remains binary | Carrier growth across stages |

`PrimDiff.lean` makes this distinction concrete: `irrefl_witness_ne` establishes distinct endpoints ($a \neq b$), while `single_oriented_witness_consistent` constructs an explicit model with one witness occurrence from false to true and none in the reverse direction. Thus, **two endpoints** is established; "exactly two witness occurrences everywhere" is contradicted by explicit models.

#### Pointed Universal Binary Germ ($D_2$)

Let $D_2$ have carrier $\{0,1\}$ and the single directed edge $0 \to 1$. Given any admitted pair $R(a,b)$, there is exactly one point-preserving function:
$$f: D_2 \longrightarrow (A, R), \qquad f(0) = a, \quad f(1) = b$$
and it preserves the edge. Irreflexivity makes its two endpoint images distinct. At the level of relation-preserving functions, this yields the universal binary germ (`D2_initial_pointed`).

#### Observation Collision Resolution & Tagging

Suppose an observation $q: A \to O$ collapses an admitted distinction: $q(a) = q(b)$. Supply a binary tag $t: A \to \{0,1\}$ with $t(a) = 0$ and $t(b) = 1$, and define:
$$q'(x) = (q(x), t(x))$$
Then:
$$q'(a) \neq q'(b), \qquad \operatorname{pr}_O \circ q' = q$$
The lifted presentation resolves that collision while retaining the previous observation. Two tag values suffice for one conflicting pair; multiple conflicting pairs generalize to a graph-coloring problem whose primitive constraints remain binary.

#### Decoupling Construction Stage ($n$) from Homotopy Truncation Depth ($j$)

Calling $S(n)$ a Postnikov tower adds mathematical requirements:
- $n = \text{construction stage}$
- $j = \text{homotopy truncation depth}$

For a fixed space $X$, its Postnikov stages $P_j X = \tau_{\le j} X$ preserve homotopy groups through degree $j$ and remove higher ones. Downward maps are total; upward sections are additional structure and need not exist. Successive truncations preserve $\pi_0$. Therefore, an empty-space stage followed by a point cannot be successive truncations of the same space $X$.

After supplying an explicit realization $\rho(S(n))$, $P_j(\rho(S(n)))$ is the candidate Postnikov tower at fixed $n$. Growth across construction stages $n$ remains a separate construction requiring its own maps and preservation proofs. If realizations are merely discrete sets, their higher homotopy groups vanish; nontrivial higher stages require additional topological structure.

#### Section and Retraction Dynamics

For presentation stages $P_n$ and $P_{n+1}$:
- Section lift: $u_n: P_n \hookrightarrow P_{n+1}$.
- Typed retraction down-map: $\widehat{r}_n: P_{n+1} \to P_n \sqcup \{\mathrm{NON\_DESCENT}\}$.
- Exact typed retraction law:
  $$\widehat{r}_n \circ u_n = \mathrm{inl}$$
  Rejecting every element outside $\operatorname{im}(u_n)$ defines exact recovery from the image, separate from total forgetful projections or Postnikov down-maps. An old-image law also requires a separate theorem showing that the lift resolves the selected obstruction.
- Generating edges vs. Categorical Morphisms: An irreflexive cut relation cannot itself be the entire categorical morphism relation because categories require identity arrows; it instead supplies distinguished generating edges for an upfunctor.

### 2.2 Canonical Anti-Slop Definition Firewall

| Canonical Term | Pinned Mathematical Definition | Explicit Negative Boundary (Anti-Slop Firewall) |
|---|---|---|
| **Opaque Inscription `<>`** | Exactly one presentation token / boundary inscription (`len = 2` bytes, 1 token), with zero admitted carrier items ($|V_0| = 0$). Proved ground inertia under `CL-0-INERTIA` and `supply_no_op`. | NOT the empty string `""` or $\varepsilon$. NOT the empty set $\emptyset$ inside an ambient ZFC universe. Inscription alone does not constitute admission. |
| **Inhabited Mark `<a>`** | Records a single mark. Admission requires an explicit consumer or retention receipt ($|V_1| = 1$). Sits in pure quiescence (${\longrightarrow}_0 = \emptyset$). | `<a>` alone does not force admission or carrier cardinality. Cannot express relations, directions, orderings, or comparisons. Possesses zero relational capacity. |
| **Retained Pair `<ab>`** | Records two marks ($|V_2| = 2$). In the absence of distinguishing forms, data remain observationally collapsed (`R2L_collapsed`, `R2F_collapsed`). | Records two marks without asserting a relation. Does NOT assert an edge or directed cut. Distinguishing relation is postponed to Stage 3. |
| **Directed Irreflexive Cut `<a->b>` / `[a,b]`** | Inhabited irreflexive relation $R(a,b)$ with distinct endpoints $a \neq b$. Endpoint support $\Delta_{\mathrm{support}}(a,b) := |\{a,b\}| = 2$. | NOT a self-loop. Bare assertions without irreflexivity do not force distinctness. Witness multiplicity may be 1, 2, or more. |
| **Obstruction Carrier $W_n$** | The typed unresolved-obstruction carrier at stage $n$ ($W_n^{\mathrm{active}}$). | NOT an arbitrary set of errors. Must denote an exact structural blockage that forces the next stage. |
| **Measurement Functor $s_n$** | The declared measurement of the obstruction carrier: $s_n = \mu_n(W_n)$. | Specific integer values ($s_1=1, s_2=2, \dots$) are **example receipts** on declared reference complexes, NOT universal theorems for arbitrary graphs. |
| **Lift Rank $\delta_n$** | $\delta_n = \operatorname{rank}(\mathrm{op}_{n+1}/\mathrm{op}_n)_1 = 2$ in the regular involution-pair operadic lift tower. | $\delta_n = 2$ is an admitted hypothesis (involution pair / dual witness), NOT a universal law for single-bit distinctions. |
| **Semantic Role Separation** | Strict signature distinction: `generate` $\neq$ `evaluate` $\neq$ `admit`. | An evaluator report does NOT grant authorization (`GEN-WDP-03`, `GEN-WDP-04`). Three physical agents are neither required nor sufficient (`GEN-WDP-10`). |
| **Mathematical Shadow $R(S(n))$** | External mathematical representation (graph, simplicial complex, category, Regge action). | Holds ZERO generative authority to extend $S(n)$ (Two Boxed Laws). |

---

## 3. The Four-Layer Architectural Model

All concepts, modules, and documentation across the estate are partitioned into four non-overlapping layers:

| Layer | Allowed Content & Governing Boundaries | Example Formal Constructs |
| :--- | :--- | :--- |
| **1. S(n) Genesis Core (`levels/`)** | **Only structures strictly forced by the Genesis derivation.** Operates over opaque inscriptions, admission events, observational profiles, collapsed pairs, and minimum response deltas. Strictly domain-neutral and representation-free. | Opaque seed `<>`, `supply_no_op`, profile collapse, cost-2 separation floor, automorphism orbit closure, section/retraction down-maps $r_N$. |
| **2. Formal Shadows (`levels/`)** | **Mathematical representations of a core structure.** Graph, simplicial, algebraic, category-theoretic, homological, or dynamical models that encode core states without defining them. | Directed cut $a \to b$, complete 1-skeletons $K_4$, transfer operators $\mathcal{L}$, dagger categories $\dagger$. |
| **3. Downstream Applications (`domains/`)** | **External interpretations and physical analogies.** Domain-specific mappings into external physical, computational, or cognitive theories. *Cannot alter core state or mint authority.* | Discrete 4D Regge spacetime, lattice gauge theory, neural network attention, database schemas. |
| **4. Verification & Receipts (`levels/`)** | **Hermetic execution engines, solvers, and proof kernels.** Software and proof scripts that verify declared properties and emit immutable receipts. | Lean 4 proof terms, native Rust crates (`omega_homology`), Python reference kernels, deterministic JSON exports. |

---

## 4. The Native Genesis Tower (19L57G1 Core Ladder)

In the sealed greenfield derivation ([19L57G1](https://github.com/dbccpage/19L57G1)), the object language begins from the single opaque atomic datum `<>` under blind external challenges, without importing set theory, graphs, simplices, or geometry.

```
                  [ The Genesis Core Ladder ]
   S(0) ─────────> S(1) ─────────> S(2) ─────────> S(3) ── ... ──> S(6)
  (Void)          (Mark)          (Pair)         (Separation)    (Extension)
    │               │               │               │               │
    │ ρ_0           │ ρ_1           │ ρ_2           │ ρ_3           │ ρ_6
    ▼               ▼               ▼               ▼               ▼
 R(S(0))         R(S(1))         R(S(2))         R(S(3))         R(S(6))
Empty Set     Augmented Simplex  S_2 Module      Directed Cut    Section / Retract
               [ Formal Mathematical Shadows — Zero Authority to Extend ]
```

### Stage 0: The Initial Inscription (Challenge 0)
- **Genesis Core:** Opaque whole `<>`, treated as one atomic presentation datum with no inherited meaning.
  - *Distinction between Presentation and Carrier:* `<>` is **one opaque wire presentation token / inscription** (`len = 1`), while the carrier has **zero admitted elements** ($V_0 = \emptyset$, $|V_0| = 0$).
- **Proved Result:** **Inertia**. Nothing is derivable (`genesis_underivable`), bare supply is a no-op (`supply_no_op`), and no successor is internally forced.
- **Active Obstruction & History:**
  - Active unresolved obstructions: $W_0^{\mathrm{active}} = \emptyset \implies s_0 := |W_0^{\mathrm{active}}| = 0$.
  - Persistent history ledger: $H_0 = \{\mathrm{receipt}_{\mathrm{ground\_inertia}}\}$.
- *Formal Shadow $\rho(S(0))$:* Representable as the empty set $V_0 = \emptyset$ or zero complex $C_* = 0$.

### Stage 1: First External Supply (Challenge 1)
- **Genesis Core:** External supply of `<a>`. Supply without explicit retention changes no internal state (`supply_no_op`). With zero admitted instances, every pair of data is observationally collapsed (`collapsed_of_no_insts`).
- **Domain-Neutral Fact:** Renaming the lone mark does not change the presentation structure.
- **Active Obstruction & History:**
  - Active unresolved obstruction: mark supplied without consumer: $W_1^{\mathrm{active}} = \{\mathrm{obs}_{\mathrm{unconsumed\_mark}}\} \implies s_1 := |W_1^{\mathrm{active}}| = 1$.
  - Persistent history ledger: $H_1 = H_0 \cup \{\mathrm{receipt}_{\mathrm{lone\_mark}}\}$.
- *Formal Shadow $\rho(S(1))$:* Augmented 0-simplex $[a]$ with $\widetilde{\partial}_0 [a] = [\emptyset]$.

### Stage 2: Retained Inscriptions & Internal Collapse (Challenge 2)
- **Genesis Core:** Both `<a>` and `<b>` supplied and retained ($V_2 = \{a, b\}$). In the absence of distinguishing forms and relational instances, all data remain observationally collapsed (`R2L_collapsed`, `R2F_collapsed`). Admitting fresh data changes metatheoretic cardinality without increasing internal expressive power. Inscription `<ab>` records two marks without asserting a relation.
- **Active Obstruction & History:**
  - Active unresolved obstruction: collapsed pair: $W_2^{\mathrm{active}} = \{\mathrm{obs}_{\mathrm{collapsed\_pair}}\} \implies s_2 := |W_2^{\mathrm{active}}| = 1$.
  - Persistent history ledger: $H_2 = H_1 \cup \{\mathrm{receipt}_{\mathrm{retained\_pair}}\}$.
- *Formal Shadow $\rho(S(2))$:* Permutation representation of the symmetric group on a 2-dimensional free module: $S_2 \curvearrowright \mathbb{Q}^2$ by basis swap $\sigma(e_1) = e_2, \sigma(e_2) = e_1$.
- *Epistemic Demarcation:* A directed cut $a \to b$ ($r(a, b) \implies a \neq b$) does **not** belong to Stage 2 core; it belongs to the Stage 3 formal shadow with endpoint support $\Delta_{\mathrm{support}} = 2$.

### Stage 3: Required Separation & Cost-2 Minimality (Challenge 3)
- **Genesis Core:** The caller requires `<a>` and `<b>` to be internally separable (differing positive derivability profiles).
  - *Cost Floor Theorem (`cost1_insufficient_general`):* The minimum cost to separate a form-less, instance-less regime is **strictly 2 items** (bundling 1 new form and 1 new instance).
  - *Non-Uniqueness under $\mu_1$:* Tied minima exist under raw item count $\mu_1$: unary mark $U_0$ vs binary link $B_0$.
  - *Uniqueness under $\mu_2$:* Under lexicographic measure $\mu_2 = (\text{items}, \text{arity sum})$, the unary mark $(2, 1)$ is unique up to isomorphism.
- **Active Obstruction & History:**
  - The collapsed-pair obstruction is resolved ($D_3 = \{\mathrm{obs}_{\mathrm{collapsed\_pair}}\}$). The new distinction requires automorphism orbit closure:
    $W_3^{\mathrm{active}} = \{\mathrm{obs}_{\mathrm{unclosed\_orbits}}\} \implies s_3 := |W_3^{\mathrm{active}}| = 1$.
  - Persistent history ledger: $H_3 = H_2 \cup \{\mathrm{cert}_{\mathrm{cost\_2\_floor}}\}$.
- *Formal Shadows $\rho(S(3))$:*
  - *Directed Cut Shadow:* Inhabited irreflexive relation $r(a, b) \implies a \neq b$.
  - *Simplicial Shadow:* 1-simplex $\Delta_1 = [a, b]$ with $\partial_1 [a, b] = [b] - [a] \neq 0$.

### Stage 4: Automorphism Orbit Closure & Progress (Autonomous Continuation)
- **Genesis Core:** Reissue separation demands on collapsed pairs along automorphism orbits until the closure fixpoint is reached (`terminal_all_separated`). Every supplied separation demand has a valid response (`mark_progress`), preventing terminal deadlocks.
- **Active Obstruction & History:**
  - All pairs are observationally separated. **Zero active unresolved obstructions remain**:
    $$W_4^{\mathrm{active}} = \emptyset \implies s_4 := |W_4^{\mathrm{active}}| = 0$$
  - Persistent history ledger: $H_4 = H_3 \cup \{\mathrm{cert}_{\mathrm{orbit\_closure}}\}$.
- *Formal Shadows:* Complete graph 1-skeletons $K_{k+1}$ and partition refinement lattices.

### Stage 5: External Continuation & Token Ingestion
- **Genesis Core:** At the closure fixpoint ($s_4 = 0$), endogenous demand generation halts (`OB-1`). Progress requires an explicit external continuation policy (`engine.build_tree`), admitting fresh opaque tokens into the stream.
- **Active Obstruction & History:**
  - Active unresolved obstruction: external continuation demand:
    $$W_5^{\mathrm{active}} = \{\mathrm{obs}_{\mathrm{continuation\_gap}}\} \implies s_5 := |W_5^{\mathrm{active}}| = 1$$
  - Persistent history ledger: $H_5 = H_4 \cup \{\mathrm{receipt}_{\mathrm{continuation\_demand}}\}$.
- *Formal Shadows:* Branching search DAGs of continuation candidates under measures $\mu_1$ and $\mu_2$. (Regge geometry resides in Layer 3 Applications).

### Stage 6: Extension, Retraction Down-Maps, and Descent Failure
- **Genesis Core:** Structural relation between adjacent presentation stages: section lift $u_N: S(N) \to S(N+1)$ accompanied by typed retraction down-map $\widehat{r}_N: S(N+1) \to S(N) \sqcup \{\mathrm{NON\_DESCENT}\}$ satisfying $\widehat{r}_N(u_N(x)) = \mathrm{inl}(x)$. Novel generators lacking preimages return typed $\mathrm{inr}(\mathrm{NON\_DESCENT})$.
- **Section/Retraction Demarcation:** $\{u_N, \widehat{r}_N\}$ is a **section/retraction pair**, NOT an involution pair ($u_N \circ \widehat{r}_N \neq \operatorname{id}$).
- **Independent Lift Rank Definition ($\delta_n$):** $\delta_n := \#\{\text{newly adjoined primitive operators/generators}\}$. Under an adjoined paired policy, $\delta_n = 2$. Active survivor change remains $s_{n+1} - s_n = b_{n+1} - d_{n+1}$.
- **Active Obstruction & History:**
  - Active unresolved obstruction: $W_6^{\mathrm{active}} = \{\mathrm{obs}_{\mathrm{descent\_gap}}\} \implies s_6 := |W_6^{\mathrm{active}}| = 1$.
  - Persistent history ledger: $H_6 = H_5 \cup \{\mathrm{cert}_{\mathrm{section\_retraction}}\}$.
- *Formal Shadows:* Split monomorphism/epimorphism pairs in concrete categories, monad adjunction units/counits.

---

## 5. Active Obstruction Accounting ($W_n^{\mathrm{active}}$) vs Persistent History ($H_n$) and Survivor Dynamics ($s_n$)

In the native Genesis Presentation Tower $S(n)$, **$s_n$** is the **active survivor count** (or active survivor observable). Mathematically, it is defined as the exact cardinality of the **active obstruction register** $W_n^{\mathrm{active}}$ at stage $S(n)$:

$$s_n := |W_n^{\mathrm{active}}|$$

Genesis strictly separates three distinct registers:

1. **Active Obstruction Register ($W_n^{\mathrm{active}}$):**
   The finite typed set of **currently surviving, unresolved Genesis obstruction receipts**:
   $$s_n := |W_n^{\mathrm{active}}|$$
   The observable $s_n$ measures active demand pressure. It fluctuates naturally across derivational stages:
   - $s_0 = 0$ (inert ground)
   - $s_1 = 1$ (unconsumed mark)
   - $s_2 = 1$ (collapsed pair)
   - $s_3 = 1$ (unclosed orbit demand)
   - $s_4 = 0$ (terminal fixpoint; zero active obstructions)
   - $s_5 = 1$ (external continuation demand)
   - $s_6 = 1$ (descent stabilization gap)
   *(We strictly reject mechanically forcing $s_n = n$).*

2. **Persistent History Ledger ($H_n$):**
   The cumulative deduplicated set of all historical certificates, receipts, and closure proofs emitted up to stage $n$:
   $$H_n = H_{n-1} \cup C_n, \qquad |H_n| \text{ is monotonically non-decreasing}$$

3. **Ordered Replay History (Replay Log):**
   The chronological sequence of transition events with exact ordering and multiplicity. A replay log cannot generally be collapsed to a set without losing causal precedence and event multiplicity.

---

### 5.1 The Physical & Structural Meaning of $s_n$

Physically and geometrically, $s_n$ measures the **active, unresolved structural demand pressure (or "unclosed debt")** present in the system at derivational stage $n$.

- **$s_n > 0$ (Obstructed / Out of Equilibrium):** Represents an active, un-repaired topological defect, uncancelled flux, or unresolved distinction in the system. This active obstruction exerts structural pressure that forces the system to either retract or adjoin new structure to resolve the tension.
- **$s_n = 0$ (Terminal Fixpoint / Structural Equilibrium):** Indicates that the active obstruction register has been completely cleared ($W_n^{\mathrm{active}} = \emptyset$). All active demands issued up to that point have been fully resolved, putting the system in a closed, self-consistent equilibrium where no internal transitions are forced.

---

### 5.2 The Native Genesis Survivor Sequence $s_n = (0, 1, 1, 1, 0, 1, 1)$

Across the core derivational stages $S(0)$ through $S(6)$, $s_n$ tracks the structural life cycle of tension:

1. **$S(0)$ — Ground State ($s_0 = 0$):**
   $W_0^{\mathrm{active}} = \emptyset$. The uncarved boundary token $\langle\rangle$ carries zero active demand.
2. **$S(1)$ — Mark Genesis ($s_1 = 1$):**
   $W_1^{\mathrm{active}} = \{\mathrm{obs}_{\mathrm{unconsumed\_mark}}\}$. Admitting a single mark $a$ creates an active demand because the mark exists without an internal consumer or distinguishing context.
3. **$S(2)$ — Collapsed Pair ($s_2 = 1$):**
   $W_2^{\mathrm{active}} = \{\mathrm{obs}_{\mathrm{collapsed\_pair}}\}$. Admitting two tokens without a declared cut creates a single collective observational collapse obstruction between $a$ and $b$.
4. **$S(3)$ — Asymmetric Cut ($s_3 = 1$):**
   $W_3^{\mathrm{active}} = \{\mathrm{obs}_{\mathrm{unclosed\_orbits}}\}$. Enforcing separation creates an asymmetric distinction, issuing an active demand for automorphism orbit closure.
5. **$S(4)$ — Automorphism Orbit Fixpoint ($s_4 = 0$):**
   **Terminal Closure Achieved.** $W_4^{\mathrm{active}} = \emptyset$. Automorphism orbit closure resolves all pending demands, clearing active tension to zero ($s_4 = 0$).
6. **$S(5)$ & $S(6)$ — Continuation Gap ($s_5 = 1, s_6 = 1$):**
   $W_5^{\mathrm{active}} = \{\mathrm{obs}_{\mathrm{continuation\_gap}}\}$. External continuation demands re-introduce active structural obligations.

---

### 5.3 Dual Ledger Independence: $s_n$ vs. Cumulative History $|H_n|$

A central principle of Genesis dynamics is the **strict decoupling of the active survivor count $s_n$ from the cumulative history ledger $H_n$**:

$$\text{Active Tension } (s_n = |W_n^{\mathrm{active}}|) \quad \neq \quad \text{Historical Memory } (|H_n|)$$

- At stage $S(4)$, the active obstruction register clears to zero ($s_4 = 0$) because all active demands are satisfied.
- However, the cumulative history ledger retains all past resolved certificates ($|H_4| = 5$).

**Physical Analogy:** When a physical system cancels a boundary charge or fills a topological hole, the active force drops to zero ($s_n \to 0$), but the spatial geometry and field structure built to perform that cancellation remain in memory ($H_n$).

---

### 5.4 Downstream Physical Realizations

In downstream applications—such as Regge calculus, gauge fields, or Hilbert spaces—observables like curvature deficits $\delta_h$ or matrix ranks provide analytical views. However, as the system's epistemic guardrails strictly enforce, downstream physical analogies **possess zero generative authority over Genesis** and can never define or alter the native survivor register $s_n$. $s_n$ belongs strictly to the pre-geometric, combinatorial core.

---

### 5.5 The Genesis Shift Equation

In the native Genesis Presentation Tower $S(n)$, transition dynamics and active structural tension are governed by the **Genesis Shift Equation**.

Rather than arbitrarily setting the survivor count equal to the stage index ($s_n \neq n$), the active survivor count $s_n := |W_n^{\mathrm{active}}|$ tracks the exact balance of **discharged (dead) obstructions** and **newly adjoined (born) demands** at each transition.

#### The Set-Theoretic and Shift Equations

When the system transitions from stage $S(n)$ to stage $S(n+1)$, two distinct sets are evaluated:
- **Discharged Obstructions ($D_{n+1}$):** Active demands from $W_n^{\mathrm{active}}$ that are resolved by the transition. Its cardinality is the **death rate**: $d_{n+1} := |D_{n+1}|$.
- **Born Obstructions ($B_{n+1}$):** Novel demands or obligations introduced by the new challenge or extension. Its cardinality is the **birth rate**: $b_{n+1} := |B_{n+1}|$.

The active obstruction register updates via set-difference and disjoint union:
$$W_{n+1}^{\mathrm{active}} = (W_n^{\mathrm{active}} \setminus D_{n+1}) \sqcup B_{n+1}$$

Taking the cardinality of both sides yields the **Genesis Shift Equation**:
$$\mathbf{s_{n+1} - s_n = b_{n+1} - d_{n+1} \quad \implies \quad s_{n+1} = s_n - d_{n+1} + b_{n+1}}$$

#### Step-by-Step Derivation Across the Core Ladder ($S(0) \to S(6)$)

Tracking this equation across stages $S(0)$ through $S(6)$ yields the exact native survivor sequence **$s_n = (0, 1, 1, 1, 0, 1, 1)$**:

1. **$S(0) \to S(1)$ (Ground to First Mark):**
   - Baseline: $s_0 = 0$ ($W_0^{\mathrm{active}} = \emptyset$).
   - Transition: $D_1 = \emptyset \implies d_1 = 0$; $B_1 = \{\mathrm{obs}_{\mathrm{unconsumed\_mark}}\} \implies b_1 = 1$.
   - Shift Calculation: $s_1 = 0 - 0 + 1 = \mathbf{1}$.

2. **$S(1) \to S(2)$ (Retained Pair & Observational Collapse):**
   - Transition: Retaining a second mark resolves the lone-mark demand ($D_2 = \{\mathrm{obs}_{\mathrm{unconsumed\_mark}}\} \implies d_2 = 1$), but creates a collapsed-pair demand under $S_2$ symmetry ($B_2 = \{\mathrm{obs}_{\mathrm{collapsed\_pair}}\} \implies b_2 = 1$).
   - Shift Calculation: $s_2 = 1 - 1 + 1 = \mathbf{1}$.

3. **$S(2) \to S(3)$ (Required Separation / Cost-2 Floor):**
   - Transition: Enforcing separation discharges the collapsed pair ($D_3 = \{\mathrm{obs}_{\mathrm{collapsed\_pair}}\} \implies d_3 = 1$), but introduces an asymmetric distinction requiring orbit closure ($B_3 = \{\mathrm{obs}_{\mathrm{unclosed\_orbits}}\} \implies b_3 = 1$).
   - Shift Calculation: $s_3 = 1 - 1 + 1 = \mathbf{1}$.

4. **$S(3) \to S(4)$ (Automorphism Orbit Closure Fixpoint):**
   - Transition: Saturated separation along canonical orbits resolves all unclosed orbit demands ($D_4 = \{\mathrm{obs}_{\mathrm{unclosed\_orbits}}\} \implies d_4 = 1$), with no new internal demands adjoined ($B_4 = \emptyset \implies b_4 = 0$).
   - Shift Calculation: $s_4 = 1 - 1 + 0 = \mathbf{0}$.
   - *Structural Result:* **Terminal Fixpoint.** The active obstruction set is empty ($W_4^{\mathrm{active}} = \emptyset$), bringing endogenous demand to a halt.

5. **$S(4) \to S(5)$ (External Continuation / Token Ingestion):**
   - Transition: Progress beyond fixpoint deadlock requires an external continuation demand ($D_5 = \emptyset \implies d_5 = 0$; $B_5 = \{\mathrm{obs}_{\mathrm{continuation\_gap}}\} \implies b_5 = 1$).
   - Shift Calculation: $s_5 = 0 - 0 + 1 = \mathbf{1}$.

6. **$S(5) \to S(6)$ (Section Lift & Retraction Down-Map):**
   - Transition: Resolves the continuation gap while stabilizing the cross-stage retraction down-map ($D_6 = \{\mathrm{obs}_{\mathrm{continuation\_gap}}\} \implies d_6 = 1$; $B_6 = \{\mathrm{obs}_{\mathrm{descent\_gap}}\} \implies b_6 = 1$).
   - Shift Calculation: $s_6 = 1 - 1 + 1 = \mathbf{1}$.

#### Independence of Lift Rank ($\delta_n$)

The system strictly distinguishes the **survivor delta** ($s_{n+1} - s_n = b_{n+1} - d_{n+1}$) from the **lift rank** ($\delta_n$):
- **Lift Rank Definition:** $\delta_n := \#\{\text{newly adjoined primitive operators/generators}\}$.
- For example, adjoining a section/retraction operator pair sets $\delta_n = 2$.
- **The Independence Law:** Adding operators changes the syntactic description capacity ($\delta_n = 2$), but does **not** artificially inflate the active obstruction count ($s_6$ remains $1$).

---

### 5.6 Lean 4 Retraction Down-Maps & Evaluator Dynamics ([SnCarrier.lean](../../../../../../../omega_engine_education/documentation/002_s_n/lean4/SnCarrier.lean))

In [`SnCarrier.lean`](../../../../../../../omega_engine_education/documentation/002_s_n/lean4/SnCarrier.lean), retraction down-maps ($\widehat{r}_N$ or $r_N$) are formalized in Lean 4 as a fail-close, pattern-matched evaluator that enforces the **Section-Retraction Invariant** ($r_N \circ u_N = \text{id}$) across derivational stages.

#### The Retraction Sum Type (`RetractOutcome`)

Rather than forcing every input term to reduce or defaulting to self-assignment, `SnCarrier` models the output of a retraction down-map using a two-constructor inductive type:

```lean
inductive RetractOutcome where
| accepted (p : SnPresentation)
| nonDescent
```

- **`accepted p`**: The input term is certified as a valid section-lifted image from stage $N$ and successfully retracts back to its native lower-stage presentation $p$.
- **`nonDescent`**: The input term lacks a valid lift preimage or violates stage alignment, returning a typed refusal (`NON_DESCENT`) rather than penetrating the lower-stage boundary.

#### Evaluator Logic (`retractionDownMap`)

The retraction down-map `retractionDownMap (stage : Nat) (p : SnPresentation) : RetractOutcome` evaluates input presentations down to stage $N$ through two main branches:

##### A. Lifted Terms (`.lift ⟨stage, body⟩`)
When inspecting a lifted term payload, `SnCarrier` checks stage tag alignment (`l.stage == stage`) and matches the body shape to reconstruct the lower-stage presentation:
- **Empty Glyphs (`.glyphs []`)** $\to$ `.accepted (.ground ⟨()⟩)` *(Stage 0 Ground Carrier)*
- **Single Glyph (`.glyphs [m]`)** $\to$ `.accepted (.supplied ⟨m⟩)` *(Stage 1 Supplied Mark)*
- **Glyph Pair (`.glyphs [f, s]`)** $\to$ `.accepted (.relation (.pair ⟨f, s⟩))` *(Stage 2 Retained Pair)*
- **Arrow (`.arrow src tgt`)** $\to$ `.accepted (.relation (.cut ⟨src, tgt⟩))` *(Stage 3 Directed Cut)*
- **Simplex Pair (`.pair v0 v1`)** $\to$ `.accepted (.relation (.simplex ⟨v0, v1⟩))` *(Stage 3 Simplex)*

If the stage tag mismatches or the body structure is unrecognized for that stage, `retractionDownMap` evaluates directly to **`nonDescent`**.

##### B. Unlifted Native Terms
For unlifted presentation terms, `SnCarrier` validates native stage membership:
- Stage 0 natively accepts `.ground`
- Stage 1 natively accepts `.supplied`
- Stages 2 and 3 natively accept `.relation`

If the requested target stage does not match the native stage of the term, it evaluates to **`nonDescent`**.

#### Verification Invariants & Properties

1. **The Section-Retraction Law ($r_N(u_N(p)) = p$):**
   For every valid presentation $p$ at stage $N$, lifting $p$ via `sectionLift stage p` and then applying `retractionDownMap stage` yields `accepted p`. This ensures under the constructive formalization that old presentations embed **conservatively** into higher stages without loss of structural identity.
2. **Epistemic Refusal of Unearned Identity:**
   Any novel term or higher-stage generator that cannot prove its origin via a valid section-lift record $u_N(p)$ returns `nonDescent` (serializing as `NON_DESCENT`).

---

### 5.7 Preservation Under the Old-Image Law

In MSS-N and the $S(n)$ presentation tower (Stage 6 / Level 06), old images and previous observations are preserved through a **section/partial-retraction pair** $(u_N, \widehat{r}_N)$ operating under the **Old-Image Law**.

#### The Section-Retraction Operators

Stage transitions link adjacent presentation stages $S(N)$ and $S(N+1)$ via two complementary maps:

- **Injective Section Lift ($u_N$):**
  Embeds a lower-stage presentation term $x \in S(N)$ into the expanded, higher-stage presentation space $S(N+1)$:
  $$u_N : S(N) \hookrightarrow S(N+1)$$
- **Typed Retraction Down-Map ($\widehat{r}_N$):**
  Evaluates terms from the expanded space back down to $S(N)$ or emits an explicit typed refusal token:
  $$\widehat{r}_N : S(N+1) \longrightarrow S(N) \sqcup \{\mathrm{NON\_DESCENT}\}$$

#### The Old-Image Law ($\widehat{r}_N \circ u_N = \mathrm{inl}$)

To preserve old images, the retraction down-map is required to act as an exact left inverse to the section lift on its image $\operatorname{im}(u_N)$. This is codified in Lean 4 as the **Old-Image Retraction Law**:

$$\widehat{r}_N(u_N(x)) = \mathrm{inl}(x) \quad \text{or in Lean 4 syntax:} \quad \texttt{retractionDownMap } N \, (\texttt{sectionLift } N \, x) = \texttt{.accepted}(x)$$

Because $u_N$ is a split monomorphism (section) and $\widehat{r}_N$ is its partial retraction:
1. **Zero Information Loss:** Lower-stage terms (`ground`, `supplied`, `relation`, `cut`, `simplex`) retain their exact structural identity when lifted and retracted.
2. **Observation Preservation:** All observation profiles, certificates, and persistent history receipts ($H_N$) established at stage $N$ remain valid and recoverable after the lift.

#### Fail-Closed Refusal on Unearned Novelty (`NON_DESCENT`)

For any higher-stage term $y \in S(N+1)$ that lacks a valid pre-image under $u_N$ ($y \notin \operatorname{im}(u_N)$) or exhibits a stage mismatch, the retraction down-map evaluates to the typed refusal token:

$$\widehat{r}_N(y) = \mathrm{inr}(\mathrm{NON\_DESCENT})$$

This ensures that:
- **Unearned terms cannot penetrate the lower boundary:** Higher-stage generators cannot retroactively alter or collapse lower-stage structures without an explicit, certified lift record.
- **Exact recovery is distinguished from total forgetful projections:** Unlike a total forgetful map or Postnikov truncation, partial descent uses option/coproduct types to refuse unmapped terms rather than forcing an unearned map to an arbitrary lower element.

#### Section/Retraction vs. Involution

The pair $\{u_N, \widehat{r}_N\}$ is strictly a **section/retraction pair**, **not an involution pair**:
$$u_N \circ \widehat{r}_N \neq \operatorname{id}_{S(N+1)}$$

Applying retraction to a refusal token or an unmapped term continues to return `NON_DESCENT` (`retractionDownMap N (.nonDescent) = .nonDescent`). The lift adds structural capacity, while the retraction ensures under the declared assumptions that the original image remains preserved intact.

---

### 5.8 Eliminating Representation Leakage

In prior documentation, $W_n$ was populated directly with downstream mathematical constructs (homology classes, graph cycles, Regge deficits). Under the Four-Layer Model, mathematical shadows project *from* Genesis receipts via representation morphisms:

$$\rho_{\mathrm{homology}}: W_n \to W_n^H, \qquad \rho_{\mathrm{graph}}: W_n \to W_n^{\mathrm{graph}}$$

These projections provide analytical views, but **never define, alter, or populate the native Genesis survivor register $W_n^{\mathrm{active}}$**.

---

## 6. Architectural Directory Layout: The Four Canonical Pillars

In accordance with `RULE_EDUCATION_DOCS_SUBMODULE_LAYOUT_001`, the estate is strictly partitioned into the four canonical educational pillars under `omega_engine_education/documentation/002_s_n/`:

```text
002_s_n/
  sn.md                                 # Master architectural specification
  README.md                             # Catalog and directory index
  reading_guide.md                      # Reading roadmap & survivor ledger
  _images/                              # Canonical SVG schematics (sn_00 through sn_21)

  grammar/                              # Pillar 1: Syntax & Token Profiles
    sn.ebnf                             # Formal grammar for presentations, lifts (u_N), and retractions (r_N)
    sn_guide.md                         # Syntax profiles, Old-Image law, and wire definitions

  papers/                               # Pillar 2: Formal Pre-Print Packages
    000_sn/
      paper.md                          # Comprehensive S(n) research monograph (v0.1 Pre-Print)
      paper_change_log.md               # Version change log
      paper_claim_ledger.md             # Formal claim and evidence ledger

  levels/                               # Pillar 3: Discrete Carrier Levels (S(00) through S(21))
    README.md                           # Master level directory and invariant definitions (W_n, s_n, \delta_n)
    level_00_ground.md                  # S(0): The Ground & Radical Void (Inertia, s_0 = 0)
    level_01_symbol_genesis.md          # S(1): Symbol Genesis (single mark <a>, s_1 = 1)
    level_02_relational_pairings.md      # S(2): Relational Pairings (irreflexive cut, a != b, s_2 = 2)
    level_03_abstract_simplices.md      # S(3): Abstract Simplices & Boundary Nilpotence
    level_04_simplex_graph_expansions.md# S(4): Simplex 1-Skeletons & Orbit Closure (s_4 = 0)
    ...
    level_21_discrete_4d_regge_curvature.md # S(21): Discrete 4D Regge Curvature

  domains/                              # Pillar 4: Downstream Domain Integrations
    README.md                           # Domain catalog and non-generative boundary
    domain_integration.md               # Bridge specification and reflection contracts
    databases/s21_topological_query.md  # Topological relational queries and finite joins
    protocols/s24_session_types.md      # Dual-channel session types
    physics/regge_metric.md             # Gram positivity and hinge deficits
    physics/discrete_4d_regge.md        # 4D simplicial Regge curvature & action
```

---

## 7. The Four Non-Forced Premises (Epistemic Hygiene)

To maintain absolute claim hygiene, four premises historically assumed to be universal necessities are classified:

1. **Premise 1 (The next lift is not unique):** Under item measure $\mu_1$, resolving a separation demand yields tied non-isomorphic candidate deltas. Uniqueness requires declaring a specific tie-breaking measure (such as $\mu_2$).
2. **Premise 2 ($\Delta_{\mathrm{support}} = 2$ vs. Witness Multiplicity):** For any inhabited irreflexive relation $R(a,b)$, irreflexivity forces $a \neq b$, so the primitive cut has exactly two distinct endpoints ($\Delta_{\mathrm{support}} = 2$). However, witness multiplicity may be 1, 2, or more (as demonstrated in `PrimDiff.single_oriented_witness_consistent`). Furthermore, tower growth across construction stages $n$ is distinct from the Postnikov truncation depth $j$ ($P_j X = \tau_{\le j} X$).
3. **Premise 3 (Linear towers require an external selection policy):** Without choosing a closure policy, autonomous continuation forms a branching search DAG rather than a linear sequence.
4. **Premise 4 (Mathematical shadows do not extend the core):** Proving a property within a simplicial, graph, or categorical shadow describes that mathematical model only; it does not force the next Genesis stage.

---

## 8. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal mathematical separation between Genesis derivation (Layer 1 Core) and external mathematical/physical representations (Layers 2 and 3).
   - Inhabited irreflexive relation endpoint support $\Delta_{\mathrm{support}}(a,b) := |\{a,b\}| = 2$ (`PrimDiff.irrefl_witness_ne`) and universal binary germ $D_2$ pointing (`D2_initial_pointed`).
   - Exact typed retraction law $\widehat{r}_n \circ u_n = \mathrm{inl}$ for section/retraction stage pairs.
   - Tagging collision resolution $q'(x) = (q(x), t(x))$ for collapsed observations.
   - Grounding of the Genesis core ladder in machine-checked 19L57G1 Lean 4 theorems and deterministic Python reference models (`sn_audit.py`).
   - Exact one-way epistemic fencing preventing mathematical shadows from retroactively mutating Genesis ontology.
   - Separation of active unresolved obstruction tracking ($W_n^{\mathrm{active}}, s_n$), ordered replay logs, and persistent history certification sets ($H_n$).
2. **What this does not support:**
   - Does not claim that witness multiplicity is universally 2 everywhere (refuted by `PrimDiff.single_oriented_witness_consistent`, which exhibits 1 forward and 0 reverse witnesses).
   - Does not claim that stage transitions across $n$ constitute a topological Postnikov tower of a single space (successive Postnikov truncations preserve $\pi_0$, so an empty space cannot transition to a point).
   - Does not claim that vanishing of a single homology class $[z] = 0$ implies the entire group vanishes ($H_1 = 0$).
   - Does not claim that simplicial complexes, homology, de Bruijn graphs, Regge calculus, or Ihara zeta functions are derived from the opaque seed `<>`.
   - Does not claim physical spacetime, continuous quantum mechanics, or the classical Riemann Hypothesis.
3. **The narrowest defensible claim:**
   - The Genesis core derives a cost-2 separation floor for the declared Stage-3 challenge. When a binary irreflexive relation is chosen as a formal realization of that separation, the relation forces exactly two distinct endpoints ($\Delta_{\mathrm{support}} = 2$). All simplicial, graph-theoretic, and categorical models are formal shadows that describe these core structures without possessing the authority to extend them.
4. **Next test needed:**
   - Run automated verification scripts (`py -3.12 -m pytest omega_engine_education/documentation/002_s_n/code/tests/test_sn_audit.py`) asserting wire profile conformance, typed retraction laws, WIR endpoint invariants, and contract schema validity.

