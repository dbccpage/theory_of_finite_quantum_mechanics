# C500 Block 08: reviewed computation

AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).

The original publication at `b1b749a9c8fb1e61492673c251deb791ff2501a9` claimed all 25 targets passed. That conclusion is withdrawn. This root records reviewed exploratory computations; it is not a qualified execution of the frozen campaign.

What the local evidence supports: Exact rational enclosure arithmetic for the cited CHSH value expression, plus separate correlation-model labels and cited guardrails. No NPA implementation, extracted strategy, or general correlation solver is supplied.

Unresolved original obligations: launch-frozen game family; NPA matrices and feasibility; strategy extraction; theorem-level correlation-set inclusions.

All 25 original target IDs, actions and required exit evidence are preserved in `review.json`, each with evidence class `OPEN`, `plan_target_satisfied: false`, and scoped source locations. An OPEN target may have useful partial evidence. The review does not claim those partial checks satisfy the complete original target contract.

`result.json` is the deterministic Python generator output, also retained at `../../../evidence/tensor_commuting_correlation_frontier.json`. `../tools/verify_execution.py --check` compares parsed canonical JSON against a fresh generator run and checks the source/result/review hash inventory. Rust parity, Lean compilation and theorem meaning are separate validation obligations; this replay gate does not prove them.

The former general theorem/completion claims and all-HIT score are recoverable from the publication commit and superseded by this report. Next work is to establish the launch contract and discharge the named original obligations; no block advancement is authorized by this retrospective review.
