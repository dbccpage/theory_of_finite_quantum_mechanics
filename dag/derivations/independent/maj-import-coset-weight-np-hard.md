Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `MAJ-IMPORT-COSET-WEIGHT-NP-HARD` (`TFQ-1157`)

- **DAG Node**: `MAJ-IMPORT-COSET-WEIGHT-NP-HARD` (`TFQ-1157` / `MAJ-IMPORT-BMVT`)
- **Stage**: `MAJORANA`
- **Status**: `IMPORTED_ASSUMPTION` (preserved; formalizes finite $\mathbb{F}_2$ coset-weight algebra, primal-to-syndrome decoding equivalence, gauge invariance, greedy local-minimum trap, and scope fences)
- **Evidence Grade**: `E3` (`L4D`, `lean4/CampaignMajImportCosetWeightNpHard.lean`, 10 theorems, 0 `sorry`, 6/6 mutations killed)

---

## 1. Mathematical Structure & Mechanized Theorems

For a binary linear code defined by a coboundary/generator map $d_0 : \mathbb{F}_2^k \to \mathbb{F}_2^n$ and a residual vector $r \in \mathbb{F}_2^n$, the $\Phi_1([r])$ coset-leader weight is
$$
\Phi_1([r]) = \min_{\alpha \in \mathbb{F}_2^k} \mathrm{wt}(r \oplus d_0 \alpha),
$$
where $\mathrm{wt}(v) = \sum_{i=0}^{n-1} \mathbf{1}[v_i = 1]$ is the Hamming weight on $\mathbb{F}_2^n$.

1. **$\mathbb{F}_2^n$ Involutive Vector Addition (`f2_vector_space_involutive_cancel`)**:
   On `F2Vec n := Fin n → Bool`, bitwise XOR addition `f2Add` is commutative, self-inverse ($c \oplus c = 0$), and involutive ($(r \oplus c) \oplus c = r$).
2. **Bitwise Weight Identity and Triangle Inequality (`f2_pointwise_bit_weight_identity`)**:
   For any bits $a, b \in \mathrm{Bool}$, $\mathrm{wt}(a \oplus b) + 2\,\mathrm{wt}(a \wedge b) = \mathrm{wt}(a) + \mathrm{wt}(b)$ and $\mathrm{wt}(a \oplus b) \le \mathrm{wt}(a) + \mathrm{wt}(b)$.
3. **Hamming Weight Subadditivity on $\mathbb{F}_2^n$ (`f2_hamming_weight_subadditive`)**:
   Summing over `Fin n`, $\mathrm{wt}(u \oplus v) + 2\,\mathrm{overlap}(u, v) = \mathrm{wt}(u) + \mathrm{wt}(v)$ and $\mathrm{wt}(u \oplus v) \le \mathrm{wt}(u) + \mathrm{wt}(v)$.
4. **Primal Coset-Weight vs Parity-Check Syndrome Decoding Equivalence (`coset_decoding_iff_syndrome_decoding`)**:
   For any parity-check map $H : \mathbb{F}_2^n \to \mathbb{F}_2^m$ whose coset fiber satisfies $H(e) = H(r) \leftrightarrow \exists \alpha \in \mathbb{F}_2^k,\ e = r \oplus d_0 \alpha$, deciding whether $\exists \alpha \in \mathbb{F}_2^k,\ \mathrm{wt}(r \oplus d_0 \alpha) \le w$ (primal coset-weight decision) is logically equivalent to deciding whether $\exists e \in \mathbb{F}_2^n,\ H(e) = H(r) \wedge \mathrm{wt}(e) \le w$ (the Berlekamp-McEliece-van Tilborg 1978 syndrome-decoding decision problem).
5. **Gauge-Shift Invariance (`coset_weight_decision_gauge_invariant`)**:
   For any $\mathbb{F}_2$-linear map $d_0$ satisfying $d_0(\alpha \oplus \beta) = d_0 \alpha \oplus d_0 \beta$, shifting $r \mapsto r \oplus d_0 \beta$ preserves the coset-weight decision predicate $\exists \alpha,\ \mathrm{wt}(r \oplus d_0 \alpha) \le w$.
6. **Budget-Capped Upper-Bound Certification (`sampled_gauge_upper_bounds_coset_leader`)**:
   Every budget-sampled gauge vector $\alpha_{\mathrm{cap}} \in \mathbb{F}_2^k$ certifies an upper bound $\Phi_1([r]) \le \mathrm{wt}(r \oplus d_0 \alpha_{\mathrm{cap}})$.
7. **Greedy Single-Flip Local Minimum Trap (`greedy_single_gauge_flip_local_minimum_trap`)**:
   On $n = 5, k = 2$ with generator columns $g_0 = (1, 1, 1, 0, 0)$ and $g_1 = (0, 1, 1, 1, 0)$, the residual $r = (1, 0, 0, 1, 0)$ has weight $\mathrm{wt}(r) = 2$, both single-generator flips strictly increase weight ($\mathrm{wt}(r \oplus g_0) = 3 > 2$ and $\mathrm{wt}(r \oplus g_1) = 3 > 2$), yet the 2-generator flip $r \oplus g_0 \oplus g_1 = (0, 0, 0, 0, 0)$ reaches weight $0 < 2$.
8. **Coset Cardinality Budget Overflow (`coset_search_budget_overflow_witness`)**:
   Relative to `defaultCosetBudget` $B_{\max} = 2^{20} = 1048576$, the $3 \times 4$ torus ($\mathrm{rank}\,d_0 = 11$, $2^{11} = 2048 \le B_{\max}$) is searched exhaustively, whereas the $6 \times 6$ torus ($\mathrm{rank}\,d_0 = 35$, $2^{35} = 34359738368 > B_{\max}$) overflows the budget by a factor of $2^{15} = 32768$.
9. **Scope Fence — General Binary Matrix vs Graphic Incidence (`worst_case_code_hardness_vs_planar_toric_scope`)**:
   Separates general binary linear codes from graphic/planar surface-code incidence matrices.
10. **Scope Fence (`bmvt_import_scope_fence`)**:
    Separates the verified finite $\mathbb{F}_2$ coset-weight identities and greedy-trap witness from a formalization of the external 3-Dimensional Matching reduction of Berlekamp, McEliece, and van Tilborg (1978), justifying keeping `status: "IMPORTED_ASSUMPTION"`.

---

## 2. Claim Hygiene Summary

1. **What it supports**: Exact $\mathbb{F}_2^n$ involutive vector space laws, Hamming weight subadditivity, primal-to-syndrome decoding equivalence, gauge-shift invariance, a 5-coordinate greedy local-minimum counterexample, and budget-overflow arithmetic for $3 \times 4$ vs $6 \times 6$ tetron tori.
2. **What it does not support**: Does not formalize the Cook-Levin / 3-Dimensional Matching NP-completeness reduction of Berlekamp, McEliece, and van Tilborg (1978), and does not imply that planar or toric graph-incidence decoding is NP-hard.
3. **Narrowest defensible claim**: In the declared finite $\mathbb{F}_2$ model, primal coset-weight minimization $\min_\alpha \mathrm{wt}(r \oplus d_0 \alpha)$ is equivalent to syndrome-constrained minimum-weight decoding $\min_{H e = H r} \mathrm{wt}(e)$, is invariant under gauge shifts $r \mapsto r \oplus d_0 \beta$, admits strict local minima under single-generator flips on $n = 5, k = 2$, and exceeds the $2^{20}$ Gray-code budget at $\mathrm{rank}\,d_0 = 35$.
4. **Next test needed**: Formalize the discrete Lieb-Robinson causal cone and syndrome-detectability locality bounds (`MAJ-OPEN-LIEB-ROBINSON-LOCALITY`, `TFQ-1149`) and the distance-weight recovery equivalence $2t < d$ (`MAJ-DISTANCE-WEIGHT-CORRECTION`, `TFQ-1148`).
