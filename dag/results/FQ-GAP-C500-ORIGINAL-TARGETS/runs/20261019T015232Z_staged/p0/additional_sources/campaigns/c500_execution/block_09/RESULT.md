# C500 Block 09: reviewed computation

AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).

The original publication at `b1b749a9c8fb1e61492673c251deb791ff2501a9` claimed all 25 targets passed. That conclusion is withdrawn. This root records reviewed exploratory computations; it is not a qualified execution of the frozen campaign.

What the local evidence supports: The explicit two-site Ising Hamiltonian has characteristic polynomial x^4-6*x^2+5 and algebraic spectrum {-sqrt(5),-1,1,sqrt(5)}. A finite plaquette parity calculation is separate from any continuum or thermodynamic limit.

Unresolved original obligations: launch-frozen extrapolation grid; broader many-body observables; separate volume, truncation and spacing estimates.

All 25 original target IDs, actions and required exit evidence are preserved in `review.json`, each with evidence class `OPEN`, `plan_target_satisfied: false`, and scoped source locations. An OPEN target may have useful partial evidence. The review does not claim those partial checks satisfy the complete original target contract.

`result.json` is the deterministic Python generator output, also retained at `../../../evidence/lattice_gauge_manybody_benchmark.json`. `../tools/verify_execution.py --check` compares parsed canonical JSON against a fresh generator run and checks the source/result/review hash inventory. Rust parity, Lean compilation and theorem meaning are separate validation obligations; this replay gate does not prove them.

The former general theorem/completion claims and all-HIT score are recoverable from the publication commit and superseded by this report. Next work is to establish the launch contract and discharge the named original obligations; no block advancement is authorized by this retrospective review.
