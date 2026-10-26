---
documentation_contract: symbol-game-documentation/v1
title: "Genesis Level 29: Native cells and cost cohomology"
kind: grammar-reference
level: 29
status: active
maturity: research
claim_status: source_scoped
authority_effect: "None"
source_revision: f1d56c010e6ba10a3b9418bd7cc5953c067250f2
---

# Level 29: Native cells and cost cohomology

AuthorityEffect: None. Teaching milestone; no identity with an S(n) stage or MSS index.

**Carrier:** Passage states, events, accepted swaps and integer costs.

**Supplied assumptions:** A 2-cell requires the specified commutation; closedness is vanishing cost around every commuting square.

**Statement:** Put dφ(s,e)=φ(T_e(s))−φ(s). The source proves d_square(dφ)(s;e,f)=φ(T_f(T_e(s)))−φ(T_e(T_f(s))). This is the difference of the two final endpoints, not an alternating sum at four corners. It vanishes for every φ iff the two endpoints agree. The halt/license pair is noncommuting and yields nonzero boundary. Exact costs telescope; a nonzero cycle cost is not exact. Budget delta is exact; the state-changing-step count is closed (NS-10) and non-exact (NS-8). NS-5 has explicit swap words with strict vertical identities/associativity and interchange modulo FarRel, not strict interchange or a groupoid.

**Evidence:** POST-SEAL THEOREMS NS-5 THROUGH NS-10. [Pinned source](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/native_structure/lean/ResearchNativeStructure/Boundary.lean). Source statements and recorded compilation are distinguished from fresh companion tests.

**Implementation or open obligation:** Check each named cell relation. The 88,338-square finite check is not the general closedness proof.

See the [current Genesis account](../genesis.md), [all-source crosswalk](../source_crosswalk.md), [selected families](../primitives/README.md) and [actual source adapters](../research_extension/docs/source_fidelity.md).
