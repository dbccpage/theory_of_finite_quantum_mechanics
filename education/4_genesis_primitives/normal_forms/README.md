# Genesis form contracts

AuthorityEffect: None. These 14 YAML files are draft declarations under `smplx.nf.contract.v0`. All have `qualifies_as_true_normal_form: false`; the qualification gaps differ by contract. `verification_status: absent` means no local evaluator is bound to the whole contract. It does not deny existing source theorems or normalization algorithms. Schema validation, executable availability, an instance certificate and a semantic proof are separate checks.

| Contract | Actual subject | Qualification gap |
| --- | --- | --- |
| [AONF](nf.derivation.aonf.yaml) | Active Obstruction Normal Form | no_project_join_theorem |
| [APNF](nf.derivation.apnf.yaml) | Constructive Apartness Normal Form | no_project_join_theorem |
| [IGNF](nf.derivation.ignf.yaml) | Isomorphism Gauge Normal Form | no_project_join_theorem |
| [IRNF](nf.derivation.irnf.yaml) | Integer Ray Normal Form | no_project_join_theorem |
| [LSNF](nf.derivation.lsnf.yaml) | Lawful Skeletal Filtration Normal Form | no_project_join_theorem |
| [OBNF](nf.derivation.obnf.yaml) | Obstruction Relativization Normal Form | no_project_join_theorem |
| [PDNF](nf.derivation.pdnf.yaml) | Primitive Difference Normal Form | no_project_join_theorem |
| [RPNF](nf.derivation.rpnf.yaml) | Replay Provenance Normal Form | reconstruction_is_replay_not_a_relational_join |
| [ANF](nf.epistemic.authority.yaml) | Authority Normal Form | reconstruction_is_not_a_relational_project_join |
| [EFNF](nf.epistemic.efnf.yaml) | Endogenous Fidelity Normal Form | no_project_join_theorem |
| [ENF](nf.epistemic.enf.yaml) | Epistemic Normal Form | reconstruction_is_not_a_relational_project_join |
| [ObsNF](nf.epistemic.observer.yaml) | Observer Normal Form | reconstruction_is_not_a_relational_project_join |
| [ProvF](nf.evidence.provenance.yaml) | Provenance Form | reconstruction_is_not_a_relational_project_join |
| [MTNF](nf.runtime.mtnf.yaml) | Mazurkiewicz Trace Normal Form | no_project_join_theorem |

PDNF requires a supplied irreflexive relation and an actual relation witness. APNF additionally declares symmetry and cotransitivity; finite enumeration is not a universal theorem. RPNF replays the declared admission history from its declared genesis and retains event order. AONF's remove/build alternatives belong to its supplied response grammar.

IGNF minimizes the declared finite relation over vertex permutations in exact mode; original labels need retained invertible transport, and automorphisms are conjugated. A bounded failure to finish is undetermined. This relation helper is not a proof of the complete native regime canonicalizer or augmentation equivariance.

IRNF accepts a nonnegative integer vector with positive total, divides by its positive gcd, and retains the gcd for reconstruction. Zero mass has no primitive probability representative. Cross-products decide positive-mass ratio agreement exactly; the Python helper's zero-vector ray convention is a separate interface decision.

LSNF separates lawful parent indices from face closure and oriented boundary cancellation. Sorted vertices alone do not prove that every face exists or that a supplied differential squares to zero. MTNF requires a symmetric irreflexive independence relation and accepted commutation at each relevant prefix, including guard reads. Disjoint writes alone are insufficient. EFNF declares u:B→E and r:E→B with r∘u=id_B; evaluator factorization is another premise, not a property established by a support flag.

**ProvF is semiring tuple provenance**, not a cryptographic custody or Merkle-chain contract. **ObsNF records attribution, measurement context and visibility boundaries**, not the source's context-plugging profile. ENF and ANF govern declared epistemic and authority metadata; none of these grants execution authority.

The [shared language boundary](shared_language_boundary.md), [WDP crosswalk](../wdp_integration.md) and [canonical contract standard](../../014_normal_forms/contracts_nf_standards/standard.yaml) explain the surrounding interfaces. Fresh schema-check results belong to the [education audit](../education_audit_2026-10-09.json); a successful schema check does not discharge these mathematical obligations.
