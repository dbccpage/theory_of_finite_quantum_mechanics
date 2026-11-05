# Zero-Container Relational Spacetime, Emergent Lorentz Causality, and Witness Holonomy (PO-035)

**Paper:** `PO-035`  
**Version:** `v0.1.0`  
**Author:** Jeremy H. Carroll  
**AuthorityEffect:** None  

## Abstract

We investigate a zero-container relational ontology built on bare marks and discrete comparison networks. In contrast to conventional field theories and differential geometry that posit an a priori ambient spacetime manifold ($\mathbb{R}^{3,1}$) or an ungrounded continuous Hilbert space as background containers, all operational distinctions here arise from primitive pairwise and multi-way comparisons across a discrete carrier complex $K = (V, E, F)$.

Space, time, coordinates, and light-cones do not pre-exist as containers; they emerge relationally from the bounded transport and non-contractible holonomy of difference cochains.

## Key Mathematical Results

The four master rows in `claim_ledger.md` are `REQUIRES_CORRECTION`. A Python `PASS (100%)` count in that ledger is a test count. It does not discharge `REQUIRES_CORRECTION`. The written arguments, and the open obligations that block them, are:

1. **R01, emergent Minkowski cone.** The written argument says that under continuum lattice refinement ($a \to 0$) the Lieb–Robinson Duhamel influence envelope converges to a forward light-cone with $c_{\mathrm{eff}} = v_{\mathrm{LR}}$. Obligations OBL-R01-01 through OBL-R01-04 remain open: metric scale non-invariance, the continuum scaling gap, the null-boundary prefactor, and non-manufactured current conservation.
2. **R01, defect current.** The written argument gives a discrete 4-current with central-difference truncation $\mathcal{O}(a^2 + \Delta t^2)$. Exact continuum conservation $\partial_\mu J^\mu = 0$ is part of the same `REQUIRES_CORRECTION` row.
3. **R03, Regge identification.** The written argument identifies $\epsilon_h = 2\pi - \sum \theta$ with $\Gamma_2 = d^1 \delta \pmod{\operatorname{im}(d^0)}$ and records $d^1 \circ d^0 \equiv 0$. OBL-R03 remains open: additive cochain curvature is not yet decoupled from metric Regge deficit.
4. **R04, dual witness.** The written argument is the ell-one distance to the coboundary image and a dual witness of sup-norm at most one. OBL-R04 remains open: floating-point false zeros, and gauge friction distinguished from dynamical halting.
5. **R02, 8-stage vocabulary.** This row is a `FORMAL SPECIFICATION`, also `REQUIRES_CORRECTION`. It is not a theorem that the vocabulary constructs curved geometry.

## Code Architecture

- `code/continuum_lorentz_causality.py`: Relational observer packet $\mathcal{O} = (K, \mathcal{F}, \mathcal{R}, \delta, d^0, d^1, J, M, \tau)$, Duhamel causal envelope scaling, defect 4-current conservation, and discrete Lorentz boost invariance.
- `code/regge_relational_obstruction.py`: 8-Stage Unified Relational Spine, coordinate-free simplicial carrier complexes, relational Regge deficit angles, discrete Bianchi exactness, and primal-dual LP stickiness certification.
- `code/tests/`: 59 unit, property, and adversarial stress tests verifying algebraic closure, numerical bounds, and LP duality certificates.

## Quick Start

```powershell
# Run the complete test suite (59 test cases)
py -3.12 -m pytest
```

## Claim Hygiene & Scope Fence

This package is an exploratory mathematical and computational physics investigation. All models, definitions, and theorems operate within declared discrete carrier complexes and explicit refinement scalings. No claims of ambient continuous differential geometry or real-world policy authorization are made.
