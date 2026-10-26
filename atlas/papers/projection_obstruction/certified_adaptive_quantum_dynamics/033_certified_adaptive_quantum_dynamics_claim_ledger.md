# Claim ledger: PO-033

Updated 2026-10-11 (1.0.1). IDs PO033-C1 through PO033-C5 are retained; PO033-C6 registers the conditional correlation implication that previously appeared without a ledger entry. The YAML is the machine-readable companion. Test mappings identify regressions and numerical observations, not proofs.

| ID | Defensible statement | Evidence and limits |
|:--|:--|:--|
| PO033-C1 | Actual-defect observable bound under finite CPTP dynamics, with an initial mismatch term | Classical proof in §3.1. The edge version needs the ideal cluster-product decomposition in §3.2. Lean establishes a conditional abstract finite-sum analogue. Sampled quadrature is uncertified. |
| PO033-C2 | Normalized ambient differential is idempotent and marginal preserving | §2.1 establishes the algebraic identities. The normalized tangent image is restricted to trace-zero Hermitian inputs; full rank is needed for a smooth density-manifold interpretation. Ambient scaling is included. |
| PO033-C3 | Thin-SVD polar witness certifies a matrix trace norm | §2.3 and rectangular numerical regressions. Tangent-space annihilation is an additional optimality condition. A concrete regression disproves general best-approximation status for the marginal projector. |
| PO033-C4 | Residual-driven cluster merging is an executable research heuristic with causal cone filtering | Full-factor boundary sensing, time alignment, preserved interval estimates, synchronous cluster updates, and feasible merge selection have regressions. Causal envelope extension (`PO033-C4-LR`) incorporates Lieb–Robinson velocity filtering to prevent acausal cluster fusion and spacelike defect leakage (`test_causal_adaptive_dynamics.py`), consistent with formal no-signalling (`LT-NS` / `NoSignalling.lean`), `LT-U1`, and `LT-A`. The status is `HEURISTIC_UNCERTIFIED`. Neither the code nor conditional Lean tolerance implication ensures the target. |
| PO033-C5 | Continuous rates give the integral's leading coefficient | §3.3 is a classical argument; Lipschitz regularity is needed for an $O(t^2)$ remainder. Lean establishes only Nat one-step identities. Every observable need not attain the coefficient. |
| PO033-C6 | Assumed edge lower bounds imply an extensive total-correlation bound | §3.4 states the common edge bound, matching, and Pinsker premises. No global remainder constant, numerical bond-dimension lower bound, code test, or Lean proof is claimed. |

## Reproduction and provenance

The paths and function names in `claim_ledger.yaml` are checked against the actual source and test definitions by `verify_deposit.py`. Those checks establish association and inventory, not semantic entailment.

`review_observations.json` records six explicitly parameterized TFIM/XXZ reference comparisons and two review counterexamples. `scripts/reproduce_review.py --check` replays them at rtol $10^{-10}$ and atol $10^{-12}$. None is an interval-certified computation or a general performance comparison.

The Lean proof sources, pinned toolchain, lockfile, and stored axiom report were preserved. The stored report remains historical. A fresh pinned Lean 4.34.0 build and all 11 selected axiom reports passed on 2026-10-11, with only propext/Quot.sound or no axioms. Standard logical axioms do not list theorem parameters such as assumed Hölder inequalities and contractivity. See `lean4/README.md`.

## Outstanding work

A certified numerical trajectory needs validated integration, actual-defect control, conservative quadrature, and floating-point enclosures. A general tangent best-approximation method needs an annihilating norm witness. Transfer to arbitrary MPS, CPS, NQS, dissipative solvers, or thermodynamic limits is open.

