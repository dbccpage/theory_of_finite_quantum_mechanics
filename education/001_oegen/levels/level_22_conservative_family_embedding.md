---
documentation_contract: symbol-game-documentation/v1
title: "Genesis Level 22: Flat families as heterogeneous families"
kind: grammar-reference
level: 22
status: active
maturity: research
claim_status: source_scoped
authority_effect: "None"
source_revision: f1d56c010e6ba10a3b9418bd7cc5953c067250f2
---

# Level 22: Flat families as heterogeneous families

AuthorityEffect: None. Teaching milestone; no identity with an S(n) stage or MSS index.

**Carrier:** PresentationNaturality Family X R: X and R are types, not a binary relation R:X→X→Prop.

**Supplied assumptions:** F supplies objects, observers, arrows with src/tgt and presentation isomorphisms.

**Statement:** The embedding H retains objects/observers and sets Hom(a,b)={f:F.Arr // F.src f=a ∧ F.tgt f=b}. Its isomorphism transports F.iso along these equalities. `natural_section_iff_embed` proves (∃s:Sec F, IsNatural F s) ↔ (∃s′:HSec(H F), HIsNatural(H F) s′). Both directions retain the same section. This is an exact section-existence correspondence, not a general physical reconstruction.

**Evidence:** POST-SEAL THEOREM. [Pinned source](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/family_embedding/lean/FamilyEmbedding.lean). Source statements and recorded compilation are distinguished from fresh companion tests.

**Implementation or open obligation:** Registration, manual receipt and Lean-job participation are distinct; consult the pinned branch status, not an inferred ungated label.

See the [current Genesis account](../genesis.md), [all-source crosswalk](../source_crosswalk.md), [selected families](../primitives/README.md) and [actual source adapters](../research_extension/docs/source_fidelity.md).
