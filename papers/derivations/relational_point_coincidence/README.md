# 003 — Relational Point Coincidence, Witnessed Difference, and Dressing Field Normal Forms

**Publication Class:** Foundational Research Preprint (v1.0, 2026-10-01)  
**Author:** Jeremy H. Carroll  
**Scope:** A formal collision between Lucrezia Ravera's (& Jordan François') relational invariant framework (Dressing Field Method, Mechanical Field Space, and Relational Quantization) and Carroll's Witnessed Difference Programme (WDP, LGGR, Projection Obstruction, Genesis, and the MSS-N Tower). Formulates relational spacetime through relational database theory (Heath's theorem, functional dependencies, candidate keys as field coincidences) and establishes two canonical normal forms: Relational Point Coincidence Normal Form (RPCNF) and Dressing Field Normal Form (DFNF).

> **Pointer (2026-10-06).** The relevant ideas of this package are carried, in
> corrected form, in the Witnessed Difference Programme monograph
> ([`witnessed_difference_programme.md`](../../001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md)):
> point coincidence as a superkey (not a candidate key) and Heath's
> decomposition in Appendix O.6, and the corrected dressing-field convention in
> Appendix P.4. Exact checks are in the WDP package at
> `code/relational_coincidence/`. The corrections are listed in this package's
> change log (2026-10-06 entry). This package is otherwise unchanged.

---

## Paper Architecture & Repository Layout

| Surface | Path | Role |
|---|---|---|
| **Canonical Paper (Markdown)** | [`relational_point_coincidence_and_witnessed_difference.md`](relational_point_coincidence_and_witnessed_difference.md) | **Canonical Manuscript (v1.0)** — DFM, point coincidences, WDP difference carriers, Heath's theorem, RPNF/DFNF, and $\ell^1$ dual witnesses. |
| **Claim Ledger** | [`relational_point_coincidence_and_witnessed_difference_claim_ledger.md`](relational_point_coincidence_and_witnessed_difference_claim_ledger.md) | **Claim Register** — Rigorous status mapping across all definitions, conditional theorems, and quarantined overclaims under strict claim hygiene. |
| **Change Log** | [`relational_point_coincidence_and_witnessed_difference_change_log.md`](relational_point_coincidence_and_witnessed_difference_change_log.md) | **Audit Trail** — Genesis notes, conceptual lineage, and Woland/Old Man adversarial review remediation log. |
| **Code Implementation** | [`code/`](code/) | **Flat Python Layout** — Exact rational relational event schemas, Heath's decomposition engine, dressing projection, and dual witness certifiers. |
| **Test Suite** | [`code/tests/`](code/tests/) | **Verification Suite** — Executable unit and property tests verifying relational lossless join, RPNF/DFNF validation, and exact LP duality. |

---

## Core Mathematical Contributions

1. **Point coincidence, live statement:** The 2026-10-06 pointer above is the live reading: point coincidence is a superkey in the Witnessed Difference monograph, Appendix O.6. The frozen 2026-10-01 manuscript and `CLM-GR003-001` still say candidate key for $\mathcal{K} = \{\phi^0, \phi^1, \phi^2, \phi^3\}$ with $\mathcal{K} \to \mathcal{U}$. `VERIFIED` on that row is the frozen sentence. Minimality of $\mathcal{K}$ is not the live claim.
2. **Lossless Observer Sheet Decomposition via Heath's Theorem:** Demonstrating that partitioning a global spacetime event relation into localized observer reference sheets parameterized by invariant relational clocks and rods is strictly lossless ($r = \pi_{\mathcal{K} A}(r) \bowtie \pi_{\mathcal{K} B}(r)$), eliminating coordinate-dependent update anomalies without loss of physical content.
3. **The Dressing Field Projection on Discrete Scaffolds:** Integrating François and Ravera's Dressing Field Method (DFM) with Carroll's oblique projection obstruction calculus ($\Pi, Q = I - P$). The dressing field $u: P \to G$ acts as a non-gauge-fixing retraction onto the basic invariant field manifold, avoiding artificial boundary modes and Gribov obstructions.
4. **Relational Point Coincidence Normal Form (RPCNF):** Formulating the exact contract schema where every non-trivial functional dependency between field observables is determined by an invariant coincidence witness, excluding coordinate-dependent anomalies.
5. **Dressing Field Normal Form (DFNF):** Formulating the contract schema enforcing that gauge redundancies are factorized into basic invariants via a certified dressing field without gauge-fixing cuts.
6. **Local Green, Global Red in Relational Embeddings:** Demonstrating that local satisfaction of RPCNF (Green locally across every chart) can fail to admit a global smooth embedding due to non-trivial cochain obstruction $\Phi_1([\omega]) > 0$ and holonomy defect $\Gamma_2$, certified by exact rational dual witnesses ($D^T w^* = 0, \|w^*\|_\infty \le 1$).

---

## Test Execution

Run the targeted test suite using Python 3.12:
```bash
py -3.12 -m pytest code/tests/test_relational_spacetime.py -v
```
