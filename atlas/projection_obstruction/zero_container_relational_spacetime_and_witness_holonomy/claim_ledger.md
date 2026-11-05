# Claim Ledger — PO-035: Zero-Container Relational Spacetime and Witness Holonomy

**Paper:** `PO-035`  
**Version:** `0.1.0`  
**Date:** 2026-10-11  
**AuthorityEffect:** None  

## Master Claim Ledger

| Claim ID | Title & Statement | Claim Status | Proof Status | Hypotheses / Scope | Paper Pointer | Mechanization Status | Limitations & Open Obligations |
|---|---|---|---|---|---|---|---|
| **R01-EMERGENT-CAUSALITY** | Under continuum carrier refinement $a \to 0$, the Lieb–Robinson Duhamel influence envelope converges to the sharp Minkowski forward causal cone with emergent effective light speed $c_{\mathrm{eff}} = v_{\mathrm{LR}}$, and the discrete defect 4-current satisfies relativistic conservation $\partial_\mu J^\mu = \mathcal{O}(a^2) \to 0$. | REQUIRES_CORRECTION | WRITTEN PROOF | Discrete carrier lattice with pitch $a > 0$, bounded local generator strength $g$, Lieb–Robinson velocity $v_{\mathrm{LR}}$, and symmetric central-difference stencil. | §3, §4 | Verified by 33 unit and adversarial tests in Python | Open obligations OBL-R01-01..04: metric scale/dilation non-invariance, continuum scaling gap, null-boundary prefactor, and non-manufactured current conservation (review findings F1, F5). |
| **R02-RELATIONAL-SPINE** | Formal operational definition of the 8-stage categorical vocabulary (Presentation $\to$ Family $\to$ Representation $\to$ Fiber Bundle $\to$ Fact $\to$ Compression $\to$ Obstruction $\to$ Relational Regge Curvature) grounding relational difference cochains without ambient containers. | REQUIRES_CORRECTION | FORMAL SPECIFICATION | Discrete carrier complex $K = (V, E, F)$, difference cochain $\delta \in C^1(K, \mathcal{F})$, coboundary operators $d^0$ and $d^1$, and functorial projection maps. | §5 | Verified by data model and transition tests in Python | Open obligations OBL-R02-01..03: identity transport zero control, cross-fiber transport/covariant coboundary, and categorical functoriality (review finding F4). |
| **R03-REGGE-HOLONOMY** | Regge deficit angle $\epsilon_h = 2\pi - \sum \theta$ on codimension-2 bones is identical to the irreducible cochain quotient holonomy $\Gamma_2 = d^1 \delta \pmod{\operatorname{im}(d^0)}$ without an ambient metric container, and satisfies exact discrete Bianchi identity $d^1 \circ d^0 \equiv 0$. | REQUIRES_CORRECTION | WRITTEN PROOF | Simplicial carrier complex $K$ without background metric coordinates, relational edge differences, and codimension-2 bone stars. | §6 | Verified by 26 unit and adversarial tests in Python | Open obligations OBL-R03-01..03: decouple additive cochain curvature from metric Regge deficit, correct quotient space type errors, and formulate geometric bridge conditions (review finding F2). |
| **R04-OPERATIONAL-STICKINESS** | Projection friction $\inf_\alpha \|\delta - d^0 \alpha\|_1 > 0$ halts fluent continuation when a difference cochain cannot factor through local gauge repair, certified by a dual linear programming witness $y \in \ker((d^0)^T)$ with $\|y\|_\infty \le 1$ and $y^T \delta > 0$. | REQUIRES_CORRECTION | WRITTEN PROOF | Discrete carrier complex $K$, difference cochain $\delta$, and exact coboundary operator $d^0$ under $\ell^1$ minimization. | §7 | Primal-dual LP certificates verified in Python to machine precision | Open obligations OBL-R04-01..03: remediate floating LP false zeros via exact dual certificates, distinguish gauge friction from dynamical halting, and provide operational measurement model (review findings F3, F6). |

## Implementation and Verification Mapping

| Claim ID | Primary Implementation | Test Files | Total Test Cases | Verification Result |
|---|---|---|---|---|
A `PASS (100%)` cell records a Python test count. It does not discharge a `REQUIRES_CORRECTION` row.

| **R01-EMERGENT-CAUSALITY** | `code/continuum_lorentz_causality.py` | `code/tests/test_continuum_lorentz_causality.py`<br>`code/tests/test_adversarial_continuum_causality.py` | 33 | PASS (100%) |
| **R02-RELATIONAL-SPINE** | `code/regge_relational_obstruction.py` | `code/tests/test_regge_relational_obstruction.py` | 10 (shared) | PASS (100%) |
| **R03-REGGE-HOLONOMY** | `code/regge_relational_obstruction.py` | `code/tests/test_regge_relational_obstruction.py`<br>`code/tests/test_adversarial_regge_relational_obstruction.py` | 26 | PASS (100%) |
| **R04-OPERATIONAL-STICKINESS** | `code/regge_relational_obstruction.py` | `code/tests/test_regge_relational_obstruction.py`<br>`code/tests/test_adversarial_regge_relational_obstruction.py` | 26 (shared) | PASS (100%) |
