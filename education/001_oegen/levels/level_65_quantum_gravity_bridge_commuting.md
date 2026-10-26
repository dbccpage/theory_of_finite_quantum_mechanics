---
documentation_contract: symbol-game-documentation/v1
title: "Genesis Level 65: Observation-preserving translations"
kind: grammar-reference
level: 65
status: active
maturity: research
claim_status: source_scoped
authority_effect: "None"
source_revision: f1d56c010e6ba10a3b9418bd7cc5953c067250f2
---

# Level 65: Observation-preserving translations

AuthorityEffect: None. Teaching milestone; no identity with an S(n) stage or MSS index.

**Carrier:** Source step g:S×E→S and native Passage replay, with source observation obsA.

**Supplied assumptions:** Supply a commuting translation Sim, an observation map obsMap, and nobs(enc(s))=obsMap(obsA(s)).

**Statement:** NB-7 (`Sim.run_trHist`, `Sim.lift_append`) lifts histories and composition. NB-9 gives an injective commuting budget encoding of every injectively numbered source while its core stays constant. NB-16 (`ObsSim.obs_const_on_cycle`) proves that, when obsMap is injective, obsA is constant on every source cycle. `toggle_no_faithful_obs` excludes the toggle observed by its own state. It is not a universal profile-equivalence theorem or a quantum-gravity unification.

**Evidence:** POST-SEAL THEOREMS AND COUNTERMODEL. [Pinned source](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/native_bridge/lean/ResearchNativeBridge/Observe.lean). Source statements and recorded compilation are distinguished from fresh companion tests.

**Implementation or open obligation:** Event selection (NB-15) and X310/G012 read-back (NB-17) retain their separate open obligations.

See the [current Genesis account](../genesis.md), [all-source crosswalk](../source_crosswalk.md), [selected families](../primitives/README.md) and [actual source adapters](../research_extension/docs/source_fidelity.md).
