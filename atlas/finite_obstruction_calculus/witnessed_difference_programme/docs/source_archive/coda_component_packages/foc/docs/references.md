# References — CODA-FOC

Bibliographic register of foundational literature, formalization environments, and companion monographs for the Finite Obstruction Calculus (CODA-FOC).

1. Rockafellar, R. T. (1970). *Convex Analysis*. Princeton Mathematical Series, vol. 28. Princeton University Press, Princeton, NJ. ISBN: 978-0-691-01586-6. DOI: 10.1515/9781400873173.
   - Supports: Compact sublevel slice attainment for convex functions (§27), polar cones, subgradient calculus, and Fenchel-Rockafellar duality (§28, §31) underlying Theorem FOC-T1 and Theorem FOC-T2.

2. Schrijver, A. (1986). *Theory of Linear and Integer Programming*. Wiley-Interscience Series in Discrete Mathematics and Optimization. John Wiley & Sons, Chichester. ISBN: 978-0-471-90854-8.
   - Supports: Farkas' lemma, polyhedral separation, strong LP duality with zero duality gap (§7.1–7.4), and exact rational arithmetic solvability of linear programs (§8.2–8.6) underlying Theorem FOC-T2 and the exact certifier in code/finite_obstruction.py.

3. Boyd, S., & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press, Cambridge, UK. ISBN: 978-0-521-83378-3. DOI: 10.1017/CBO9780511804441. URL: <https://web.stanford.edu/~boyd/cvxbook/>.
   - Supports: Formulation of weighted ℓ¹ norm minimization as linear programming via split non-negative slack variables (§6.1), Lagrangian duality certificates (§5.1–5.4), separable problems (Theorem FOC-T4), and induced matrix ℓ¹ operator norms (Appendix A.1.5, Theorem FOC-T5).

4. Rudin, W. (1991). *Functional Analysis*. 2nd ed. International Series in Pure and Applied Mathematics. McGraw-Hill, New York, NY. ISBN: 978-0-07-054236-5.
   - Supports: Quotient spaces X/M by closed linear subspaces, quotient seminorm properties and attainment in finite dimensions (§1.40–1.42, Theorem FOC-T1), annihilator subspaces M° and Hahn-Banach geometric separation (§4.6–4.9, Corollary FOC-C1), and bounded linear operators between quotient spaces (Theorem FOC-T5).

5. Mac Lane, S. (1963). *Homology*. Die Grundlehren der mathematischen Wissenschaften, Band 114. Springer-Verlag, Berlin, Heidelberg. ISBN: 978-3-540-58662-3. DOI: 10.1007/978-3-642-62029-4.
   - Supports: Cochain complexes, coboundary operators, nilpotence condition d₁ ∘ d₀ = 0, cocycles and quotient cohomology (Chapter I & II, Definition FOC-D1, Theorem FOC-T3), direct sums of complexes (Chapter II, §1, Theorem FOC-T4), and cochain transformations with induced quotient maps (Chapter II, §2, Theorem FOC-T5).

6. Steenrod, N. E. (1951). *The Topology of Fibre Bundles*. Princeton Mathematical Series, vol. 14. Princeton University Press, Princeton, NJ. ISBN: 978-0-691-00548-5.
   - Supports: Classical foundations of obstruction cocycles and extension theory (Part II, §12–14), providing the topological and homological motivation for discrete two-stage obstruction diagnostics.

7. de Moura, L., & Ullrich, S. (2021). The Lean 4 Theorem Prover and Programming Language. In *Automated Deduction – CADE 28*, edited by A. Platzer and G. Sutcliffe, Lecture Notes in Computer Science, vol. 12699, pp. 625–635. Springer, Cham. DOI: 10.1007/978-3-030-79876-5_37.
   - Supports: Interactive theorem prover architecture, dependent type theory, elaboration kernel, and Lake build system used for the formal verification of CODA-FOC logical and algebraic kernels in lean4/.

8. Carroll, J. H. (2026). *CODA-A: Residuals of Projections, Kernels, and Cokernels — The Anomalon as a Typed Leftover*. CODA Technical Monograph Series. Companion manuscript; no verified DOI supplied.
   - Supports: Grounding monograph for idempotent projection residuals, kernel/cokernel factorization, and the Anomalon register evaluated by CODA-FOC quotient diagnostics.

9. Carroll, J. H. (2026). *CODA-FDA: Finite Descent Authority — Standing Authorization Gate, Boundary Isolation, and Grounded Action Contracts*. CODA Technical Monograph Series. Companion manuscript; no verified DOI supplied.
   - Supports: Operational authorization and finite descent framework, establishing the boundary between mathematical classification (CODA-FOC) and authorized execution/descent gates.

10. Carroll, J. H. (2026). *CODA-MUR: Certified Representation Transport, Composition, and Irreversible Forgetting*. CODA Technical Monograph Series. Companion manuscript; no verified DOI supplied.
    - Supports: Universal representation transport, functorial lifting, and irreversible forgetting across CODA layers extending Theorem FOC-T5.

11. Carroll, J. H. (2026). *CODA System Foundations and Architecture*. Sealed Derivation v1 (`3100c4e`), cut 2026-08-17. URL: <https://github.com/dbccpage/19L57G1/tree/sealed-derivation-v1>.
    - Supports: Repository of Record frozen baseline defining pipeline stages, exact rational constraints, and mechanical stopping conditions.
