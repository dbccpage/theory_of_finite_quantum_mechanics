# Round 2 High-Depth Prompt Allocation (5 Prompts per Team = 50 Prompts Total)

**AuthorityEffect:** None  
**Firewall Line:** `stated region only; mints no authority`  
**Allocators:** Executive Steering Team (Team 0: 5 Experts)

---

## 1. Allocation Matrix

Derived directly from the Top 50 curated portfolio, each of the 10 execution teams receives exactly 5 high-depth prompts for Round 2 deep-dive formalization, solver construction, and exact rational verification:

| Team | Target Focus | Round 2 Allocated Prompts | Primary Technical Deliverable |
|---|---|---|---|
| **Team 1** | Target G1: Fourier & Diță Affine Torus | `PROMPT_T01_01`, `PROMPT_T01_04`, `PROMPT_T01_08`, `PROMPT_T01_16`, `PROMPT_T01_25` | Lean 4 Diță non-extendibility theorem & seed cross-ratio certifier. |
| **Team 2** | Target G1: Chernyavsky-Tao Isolated Orbit | `PROMPT_T02_02`, `PROMPT_T02_05`, `PROMPT_T02_07`, `PROMPT_T02_10`, `PROMPT_T02_25` | Lean 4 Tao rigidity theorem & exact rational degree-8 SDP refutation. |
| **Team 3** | Target G1: Szöllősi Family & Haagerup Point | `PROMPT_T03_03`, `PROMPT_T03_06`, `PROMPT_T03_08`, `PROMPT_T03_10`, `PROMPT_T03_25` | Projective blow-up desingularization & Haagerup isolation certificate. |
| **Team 4** | Target G1: Karlsson Manifold & Boundary Chaining | `PROMPT_T04_02`, `PROMPT_T04_07`, `PROMPT_T04_10`, `PROMPT_T04_11`, `PROMPT_T04_25` | Exact rational volume conservation & multi-chart cocycle chaining. |
| **Team 5** | Target G1: Variety $\mathcal{H}_6$ Decomposition & Triad Pigeonhole | `PROMPT_T05_03`, `PROMPT_T05_06`, `PROMPT_T05_10`, `PROMPT_T05_11`, `PROMPT_T05_25` | Lean 4 TriadModuliPigeonhole lemma & corner variety factorization. |
| **Team 6** | Target Q: Projector Algebra Ideals & Monomial Rewriting | `PROMPT_T06_03`, `PROMPT_T06_08`, `PROMPT_T06_12`, `PROMPT_T06_16`, `PROMPT_T06_25` | Confluent term rewriting system & graded projector word basis. |
| **Team 7** | Target Q: Truncated Moment Matrices & LDLᵀ Pivots | `PROMPT_T07_01`, `PROMPT_T07_06`, `PROMPT_T07_08`, `PROMPT_T07_09`, `PROMPT_T07_22` | Cross-runtime SHA-256 fixture parity & certified candidate refutation. |
| **Team 8** | Target Q: Archimedean Positivstellensatz Certificates | `PROMPT_T08_03`, `PROMPT_T08_05`, `PROMPT_T08_08`, `PROMPT_T08_16`, `PROMPT_T08_19` | Explicit exact rational Archimedean norm bound identity & Lean 4 bridge. |
| **Team 9** | Target Q: Curto-Fialkow Flat Extensions & GNS Rank Loops | `PROMPT_T09_03`, `PROMPT_T09_07`, `PROMPT_T09_10`, `PROMPT_T09_13`, `PROMPT_T09_21` | Rank-gap sequence evaluation & GNS pre-Hilbert space construction. |
| **Team 10** | Target Q: Fail-Closed Epistemic Gate & Smale Sentry | `PROMPT_T10_01`, `PROMPT_T10_06`, `PROMPT_T10_10`, `PROMPT_T10_19`, `PROMPT_T10_25` | Fail-closed auditor (`MissingProofObligationError`) & master regression. |

---

## 2. Execution Directives for Round 2

1. **Lean 4 Proof Obligations**:
   - Production modules must compile cleanly via `lake build` with zero `sorry` or `admit` placeholders.
   - `#print axioms` must verify dependencies strictly on foundational kernel axioms: `[propext, Quot.sound]`.
2. **Rust Native Engines**:
   - Implement exact rational arithmetic over `num_rational::BigRational` and `Cyc24`.
   - Zero floating-point operations verified at AST and runtime levels.
3. **Python Verification Suites**:
   - Enforce 100% exact rational arithmetic over `fractions.Fraction`.
   - Comprehensive negative control tests verifying rejection of perturbed matrices, mutated bounds, or non-orthogonal blocks.
4. **Epistemic Scoping**:
   - `AuthorityEffect: None` and the mandatory firewall line must be embedded in all code and documentation.
   - Under NO circumstances may any agent claim or imply that $\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$.
