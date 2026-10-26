---
documentation_contract: education-documentation/v1
title: "Downstream Domains Catalog — S(n) Carrier Tower (Layer 3)"
kind: application-index
layer: "downstream_application"
realizes: null
application_domain: "catalog"
authority_effect: "None"
genesis_effect: "None"
source_paths:
  - ../sn.md
---

# Downstream Domains Catalog — S(n) Carrier Tower (Layer 3)

**AuthorityEffect:** None.
**GenesisEffect:** None (downstream applications possess zero authority to extend Genesis).
**Layer:** Downstream Applications (Layer 3)
**Realizes:** None (Physical and Computational Analogs)

---

## 1. Architectural Role & Epistemic Boundary

Downstream applications represent external domain mappings, physical analogies, and computational interpretations of structures appearing in the Genesis core and its mathematical shadows.

> [!IMPORTANT]
> **The Third Layer Law:**
> Physics and external domain models are downstream applications (Layer 3). They possess zero generative authority to extend Genesis, alter active survivor registers ($W_n^{\mathrm{active}}, s_n$), or supply axioms to core derivations. All metric data, continuous coordinates, and field equations are imported externally and are never derived by Genesis.

---

## 2. Application Domains in This Estate

### Physics & Discrete Gravity (`physics/`)

| Document | Domain | Mathematical Model | Core Relationship |
| :--- | :--- | :--- | :--- |
| [`regge_metric.md`](physics/regge_metric.md) | Discrete Regge Gravity | Gram matrix positive-definiteness ($G \succ 0$), dihedral cosines, and certified interval enclosures for hinge deficits $\delta_h$. | Downstream metric geometry analog; imports exact rational squared edge lengths $\ell_e^2 \in \mathbb{Q}^+$. |
| [`discrete_4d_regge.md`](physics/discrete_4d_regge.md) | 4D Simplicial Spacetime | 4-simplex complexes, triangle hinge curvature $\delta_t$, dual loop parallel transport $\mathcal{P}_k$, and an explicitly constructed discrete Bianchi relation (open verification obligation). | Downstream geometric specification; no full transport verifier in this strand. |

### Databases, Protocols and Domain Integration

| Document | Worked question | Explicit boundary |
| --- | --- | --- |
| [Relational queries](databases/s21_topological_query.md) | Does a projected report determine the protected column, and can compatible pair tables be joined? | Declared finite tables; local agreement can have an empty global join. The legacy topic number 21 does not name a native stage. |
| [Session protocols](protocols/s24_session_types.md) | Which sends and receives are enabled on two finite FIFO channels? | A local enabled transition does not prove scheduler fairness. Legacy topic 24 does not name a native stage. |
| [Domain integration](domain_integration.md) | Which questions and future transitions survive a domain representation? | Supply the actual carrier, report, transition and preservation witness for each domain. |

---

## 3. Claim Hygiene Quadrant

1. **What this catalog supports:**
   - Systematic indexing of Layer 3 downstream applications with explicit non-forced premise disclosures.
2. **What this catalog does not support:**
   - Does not derive physical spacetime, general relativity, quantum gravity, or continuous geometry from Genesis.
3. **The narrowest defensible claim:**
   - Downstream applications formulate consistent external interpretations of discrete simplicial complexes without extending or mutating the Genesis core ontology.
4. **Next test needed:**
   - Maintain unit tests validating that application modules declare `realizes: null` and `layer: "downstream_application"`.
