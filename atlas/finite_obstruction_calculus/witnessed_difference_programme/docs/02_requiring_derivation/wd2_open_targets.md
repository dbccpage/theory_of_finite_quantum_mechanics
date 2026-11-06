# Active Derivation Targets: WD2 Distinction Carriers & History Escape

**Status:** OPEN / REQUIRING_DERIVATION  
**Origin:** Satellite Paper #032 (`wd2_finite_distinction_carriers_and_history_escape`)  
**Claim Ledger:** `wd2_claim_ledger.md`

---

## 1. Overview of Formalization Boundary

In the satellite monograph, Theorem `WD2-T1` (monotonic refinement and permanent fixed-point stabilization) and the 5-state sharp witness `sharp_m5_bound` are formally verified in Lean 4 without `sorry` (`lean4/WitnessedDifference/FiniteDistinction.lean`). All claims are computationally verified on concrete instances in Python (`code/witnessed_difference/finite_distinction.py`).

However, several general theorems and lemmas remain open for general formalization in Lean 4:

---

## 2. Target Inventory

### Target WD2-DERIV-01: Word Kernel Representation (Lemma WD2-L1)
- **Statement:** At horizon $n$, the recursive horizon relation $R_n$ coincides exactly with the kernel of all input words of length at most $n$:
  $$R_n = \bigcap_{|w| \le n} \ker(p \circ u_w)$$
- **Current Status:** Prose proof in manuscript §3; finite instance checked in Python (`word_kernel_agrees`); general Lean 4 proof absent.
- **Derivation Required:** Inductive proof in Lean 4 on list length connecting recursive definition `Wd2.related` with word execution over `List (Fin Σ)`.

### Target WD2-DERIV-02: Pigeonhole Stabilization Bound (Theorem WD2-T2)
- **Statement:** For any finite deterministic Moore machine with state set $S$ and initial partition block count $b_0 = |S/R_0|$, the relation sequence stabilizes at an index $N \le |S| - b_0$, with $R_N = R_{N+1}$. Furthermore, the chain is sharp (achieves equality).
- **Current Status:** Prose proof in manuscript §4; `sharp_profile` checked in Python; Lean `Wd2.sharp_m5_bound` verifies the 5-state horizon-3 witness only.
- **Derivation Required:** Formalize the pigeonhole bound on strictly increasing partition block counts for finite types in Lean 4 using Mathlib's `Fintype` and partition lattice theory.

### Target WD2-DERIV-03: No-Escape Characterization (Theorem WD2-T3)
- **Statement:** The initial observation relation $R_0$ is an update congruence if and only if $R_1 = R_0$, if and only if $R_n = R_0$ for all $n$, if and only if no pair in $R_0$ has a separating word.
- **Current Status:** Prose proof in manuscript §5; checked on 2-state identity witness in Python; general Lean 4 proof absent.
- **Derivation Required:** Formalize the 4-way equivalence in Lean 4.

### Target WD2-DERIV-04: Shortest Separating Word Length (Theorem WD2-T4)
- **Statement:** If $(s, t) \in R_n \setminus R_{n+1}$, the shortest word $w$ separating $s$ and $t$ has length exactly $n+1$, and can be constructed recursively as $\sigma v$ where $\sigma$ is the first distinguishing transition.
- **Current Status:** Prose proof in manuscript §5; checked on 4-state chain in Python; general Lean 4 proof absent.
- **Derivation Required:** Constructive existence and minimality proof in Lean 4.

### Target WD2-DERIV-05: Report Factorization Invariance (Theorem WD2-T5)
- **Statement:** A transition report $r(s, \sigma)$ that factors through the two endpoint observations preserves all horizon equivalence relations $R_n$.
- **Current Status:** Prose proof in manuscript §5; checked on 4-state chain in Python; general Lean 4 proof absent.
- **Derivation Required:** Formal Lean proof showing that factoring $r(s, \sigma) = g(p(s), \sigma, p(u_\sigma(s)))$ does not refine $R_n$.

### Target WD2-DERIV-06: Coarsest Update Congruence Quotient (Theorem WD2-T6)
- **Statement:** $R_\infty = R_N$ is the coarsest output-preserving update congruence, and every compatible quotient machine is an abstraction of $S/R_\infty$.
- **Current Status:** Prose proof in manuscript §6; explicitly withdrawn as a proved claim of the package; non-claim in claim ledger.
- **Derivation Required:** Universal mapping property of the Nerode/Moore quotient in Lean 4.
