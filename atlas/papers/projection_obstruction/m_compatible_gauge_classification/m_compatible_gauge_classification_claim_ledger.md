Claim Ledger — GS-001: M-Compatible Gauge Classification
========================================================

**Paper Key:** `000_coda/foc/m_compatible_gauge_classification`  
**Paper Identity:** `GS-001`(`001_m_compatible_gauge_classification.md`, canonical version:`v1.0`)  
**Legacy Paper Identity:**`Paper 001`/`Paper 005`**Authority:** None.

This ledger catalogs every claim in`GS-001`with its type, governing hypotheses, proof location, mechanization status, and open obligations.

---

1. Claim-by-Claim Matrix

---

| ID | Claim | Type | Hypotheses | Proof / support | Mechanization | Open obligation |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Main classification: Faithful + edge-additive observer class + maximal bounded-linear symmetry $\implies$ weighted $\ell^1$. | PROVEN, CONDITIONAL | Finite poset, Banach presheaf, P1-P3, faithfulness, monoid compatibility | Abstract, Thm 4.2, Prop 7.1 | Mechanized-Partial (`PaperGS001`) | Full poset/presheaf Lean formalization |
| 2 | $C^1(P,F) = \bigoplus_e F(a_e)$ cochain space; $\ell^1$ cross-norm selected. | DEFINITION | Ambient cochain space | §1.2 | Defined | None |
| 2b | $\mathbf{Cat}_{\mathrm{Res}}$ morphism cross-reference: $F_{\mathrm{GS001}}\colon P_{\mathrm{host}}\to P_{\mathrm{gauge}}$ with packet sketch and HANDOFF-003 contract table. | SCOPE FENCE / PACKAGING | Declared Banach-presheaf inputs; live Cat_Res carrier under`008_engine_runtime`| §1.2 (Cat_Res morphism binding) | Cross-ref only | Full Cat_Res identity/associativity not claimed; ambient host not derived |
| 3 | $M$-compatible gauge defined. | DEFINITION | Submonoid $M \subseteq \mathrm{End}_b(V)$ | §2.1 | Defined | None |
| 4 | Theorem 2.2: Gauge $\leftrightarrow$ convex body correspondence. | STANDARD | Minkowski functional, finite dimension | §2.2-§2.3 | Standard | None |
| 5 | Corollary 1: Order reversal / monotonicity of gauge class ($M_1 \subseteq M_2 \implies \mathrm{Gauge}(M_2) \subseteq \mathrm{Gauge}(M_1)$). | PROVEN | Weak reduction | §2.4 | Prose-proved | None |
| 6 | Corollary 2: Maximal-symmetry endpoint ($M=\mathrm{End}_b(V) \implies j = c \|\cdot\|_V$). | PROVEN, CONDITIONAL | Hahn-Banach, native ambient norm | §2.4, §2.5 |`PaperGS001.gauge_proportional_hahn_banach`| None |
| 7 | Corollary 3: Compact-group Haar-average construction. | STANDARD | Compact isometry group, normalized Haar measure | §2.4, §2.5 | Standard | None |
| 8 | Corollary 4: Transitive isometric sphere action $\implies j = c \|\cdot\|_V$. | PROVEN, CONDITIONAL | Transitive sphere action | §2.4, §2.5 | Prose-proved | None |
| 9 | Theorem 3.1: $SO(k)$ invariance implies Euclidean balls. | PROVEN, CONDITIONAL | Euclidean ambient norm imported | §3.1 | Prose-proved | Bridge to $SO(k)$ in Lean |
| 10 | Theorem 3.2: Signed permutations classify symmetric unconditional bodies. | PROVEN, CONDITIONAL | Signed-permutation-invariant ambient norm | §3.2 | Prose-proved | None |
| 11 | Theorem 3.3: Diagonal contractions classify monotone unconditional bodies. | PROVEN, CONDITIONAL | $\ell^\infty$ ambient norm | §3.3 | Prose-proved | None |
| 12 | Theorem 3.4: Positive diagonal contractions classify cone-monotone gauges. | PROVEN, CONDITIONAL | Positive-diagonal monoid | §3.4 | Prose-proved | None |
| 13 | Theorem 3.5: Unitary conjugation boundary & singular-value classification. | STANDARD | Two-sided unitary invariance | §3.5, von Neumann [7] | Standard | None |
| 14 | Example 3.6: CPTP monotonicity alone does not force trace norm; resolved on minimal quotient state space $\widehat{X} = X/\mathrm{Core}_C(\mathrm{ker}\,o)$. | INTERPRETIVE | Helstrom distinguishability [8], PCC-20260730 | §3.6 | Mechanized (`PCC.Adequate`/`adequate_iff`,`PCC.qo_minimal_adequate`/`minimal_iso`) | Discharged via minimal state quotient |
| 15 | Theorem 3.7: Trivial monoid admits all gauges ($j$ is $\{I\}$-compatible). | PROVEN (TRIVIAL) | Trivial group | §3.7 | Prose-proved | None |
| 16 | Lemma 4.1: Direction independence under maximal symmetry. | PROVEN, CONDITIONAL | Hahn-Banach theorem | §4, §5 |`PaperGS001.direction_independence_hahn_banach`| None |
| 17 | Theorem 4.2: Maximal-symmetry $\ell^1$ endpoint (per-edge proportionality + edge sum). | PROVEN, CONDITIONAL | P1-P3; uniformity needs P4 | §4, §5 | Mechanized-Partial | Poset/presheaf Lean wrapper |
| 18 | Numerical illustration (weighted $\nu=13$ vs unweighted $I=6$). | WORKED EXAMPLE | Replayable Python calculation | Numerical Illustration | Replay receipt | None |
| 19 | Necessity of properties P1/P2/P3/edge-uniformity (S9b). | PROVEN, CONDITIONAL | Two-sided independence witnesses | §6 | `Enc0523` witness suite + S9b two-sided proof | None (S9b completed) |
| 20 | Proposition 7.1: Normalized uniqueness. | PROVEN, CONDITIONAL | P1-P4 / single orbit | §7 |`weighted_sum_eq_scalar_l1_of_single_orbit` | None |
| 21 | Corollary 7.2: Commutative factorization. | PROVEN, CONDITIONAL | Non-$\ell^1$ fails by P1 or P3 | §7 | Prose-proved | None |
| 22 | $\ell^1$ as additive edge-sum positioning for $C^1(P,F)$. | STANDARD | Cochain cross-norm positioning | §8.2 | Standard | None |
| 23 | Reflective completion is congruence-complete. | CONJECTURE | Inherited from primitive axiomatics [6] | §8.4 | Open | PL-002-3 / PL-000-1 |
| 24 | Observer passivity / no-creation (O1) constrains downstream quotients. | SCOPE FENCE | Imported from primitive axiomatics [6] | §8.4 | Imported | None |
| 25 | Declared regime tuple $(P, E_{\mathrm{cov}}, \{F(x), \|\cdot\|\}, \{r_{b,a}\})$. | DECLARED AXIOM | Poset, Banach stalks, native norms admitted | §1.1, §1.2 | Admitted input | None |

<!-- claim-id-body-only-sync:begin -->

Body-only ID sync (packaging)
---

**AuthorityEffect:** None. Packaging hygiene; no OPEN→PROVED.

| ID | Claim | Type | Status |
|---|---|---|---|
| GS-001 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |

<!-- claim-id-body-only-sync:end -->