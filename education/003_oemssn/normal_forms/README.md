---
documentation_contract: symbol-game-documentation/v1
title: "Normal Forms & Canonical Form Contracts — MSS-N — Minimal Symbol System Tower"
kind: normal-form-index
status: active
atlas_status: specified
evidence_grades:
  named: true
  syntax: true
  computed: true
  Lean: false
  gated: true
source_provenance: external_mss_atlas
authority_effect: "None"
canonical_source: omega_engine_education/documentation/014_normal_forms/contracts_normal_forms/
last_verified: 2026-10-05
---

# Normal Forms & Canonical Form Contracts — MSS-N Tower

**AuthorityEffect:** None.\
**Canonical Source:** [`omega_engine_education/documentation/014_normal_forms/contracts_normal_forms/`](../../014_normal_forms/contracts_normal_forms)

---

## Architectural Taxonomy: Base Symbol System Forms vs. Higher Tower Forms

The normal forms in this directory govern data representations in the Minimal Symbol System N (MSS-N) tower. They are organized into two tiers:

1. **Foundational Symbol System Contracts (The MSS-N Base):**
   - [`nf.mssn`](./nf.mssn.yaml): Minimal Symbol System Normal Form. Governs Levels -1 to 38 of the keyboard ladder, preventing smuggled ambient containers (the radical void vs. $\varepsilon$), enforcing the Syntactic Firewall, and verifying split retractions ($r_N \circ \ell_N = \operatorname{id}$) and Rent Rule diagonal avoidance.
   - [`nf.mssn.bqnf`](./nf.mssn.bqnf.yaml): MSS-N Boundary-Quotient Normal Form. Derived from [`nf.change.bqnf`](../../014_normal_forms/contracts_normal_forms/nf.change.bqnf.yaml); governs incremental repair, K0 cycle repair ($d_1 z = 0, z = d_{2,\text{ext}} c$), and boundary quotient exactness.

2. **Higher-Tower Extended Form Contracts:**
   - Higher-tier contracts ([`DHNF`](./nf.cochain.dhnf.yaml), [`OBNF`](./nf.derivation.obnf.yaml), [`SCNF`](./nf.derivation.scnf.yaml), [`ASRF`](./nf.recursion.asrf.yaml), [`TSNF`](./nf.coda.tsnf.yaml), [`GNF`](./nf.representation.gnf.yaml)) govern specialized homological decompositions, derivation costs, simplicial orientations, and representation transport further up the tower.

---

## Contracts in This Domain

| ID | Name | Short | Form Category | Family | Relevance & Mathematical Invariant |
|---|---|---|---|---|---|
| [`nf.mssn`](./nf.mssn.yaml) | Minimal Symbol System Normal Form | MSSNF | Extended Form Contract | shape | Proposed alphabet/profile contract: 22 public starts, language-level retraction, and separately declared relational constraints. The full contract is not implemented. |
| [`nf.representation.tbnf`](./nf.representation.tbnf.yaml) | Token-Bounded Normal Form | TBNF | Extended Form Contract | representation | MSS-N Levels 0–1: tree-bracket wire format over the 38-character primitive alphabet $\{a..z, 0..9, <, >\}$ with unique prefix decodability. |
| [`nf.representation.dbcnf`](./nf.representation.dbcnf.yaml) | De Bruijn Cyclic Normal Form | DBCNF | Extended Form Contract | representation | MSS-N Level 7: canonical necklace representative / Lyndon word minimization under cyclic group shift $C_k$. |
| [`nf.evidence.ddanf`](./nf.evidence.ddanf.yaml) | Deterministic Data-Flow Architecture NF | DDANF | Extended Form Contract | evidence | MSS-N Level 12: immutable 13-tuple trace ledger $\tau$ and 4-field irredundant state kernel $K = (B, C, x, \Omega)$. |
| [`nf.runtime.zfnf`](./nf.runtime.zfnf.yaml) | Zero-Float Rational Normal Form | ZFNF | Extended Form Contract | runtime | MSS-N Level 18: exact rational arithmetic $q = a/b \in \mathbb{Q}$ and exact zero duality gap on LP certificates. |
| [`nf.mssn.bqnf`](./nf.mssn.bqnf.yaml) | MSS-N Boundary-Quotient Normal Form | MSSN-BQNF | Extended Form Contract | change | MSS-N incremental & cycle repair: K0 boundary complex ($d_1 b = 0, d_{2,\text{ext}} c = z$), homological quotient exactness, `UNVERIFIED` receipt firewall. |
| [`nf.cochain.dhnf`](./nf.cochain.dhnf.yaml) | Discrete Hodge Normal Form | DHNF | Extended Form Contract | shape | MSS-N Level 18 (Discrete Hodge): orthogonal split $C^1 = \operatorname{im}(d_0) \oplus H^1 \oplus \operatorname{im}(d_1^*)$. Nonzero harmonic part is a `residual_harmonic_class`. |
| [`nf.derivation.obnf`](./nf.derivation.obnf.yaml) | Obstruction Relativization Normal Form | OBNF | Extended Form Contract | derivation | MSS-N obstruction theory: a collision is an obstruction only relative to a declared protected law whose pushforward is violated. |
| [`nf.derivation.scnf`](./nf.derivation.scnf.yaml) | Separation Cost Normal Form | SCNF | Extended Form Contract | derivation | MSS-N stage transition costs: minimizers require explicit declaration of cost measure, grammar, and isomorphism relations without silent tie-breaking. |
| [`nf.recursion.asrf`](./nf.recursion.asrf.yaml) | Autopoietic Self-Reference Refusal Form | ASRF | Extended Form Contract | recursion | MSS-N recursion breaking: caller hash must differ from target hash; refuses self-certification cycles. (Computes no cohomology). |
| [`nf.coda.tsnf`](./nf.coda.tsnf.yaml) | Topological Simplex Normal Form | TSNF | Extended Form Contract | topology | MSS-N simplicial complexes: relative to a declared `vertex_total_order`, enforces boundary nilpotence and quotient integer homology $H_k = \ker d_k / \operatorname{im} d_{k+1}$. |
| [`nf.representation.gnf`](./nf.representation.gnf.yaml) | Gauge Normal Form | GNF | Extended Form Contract | transport | MSS-N representation transport: verifies schema/encoding equivalence across data serializations (not physical gauge symmetries). |

---

## Domain-Specific Rationale & Integration

### `nf.mssn` — Minimal Symbol System Normal Form
- **Base Grounding:** Bridges the 38-key keyboard ladder directly into the normal form estate.
- **Container Refusal:** Enforces the epistemic baseline of Level -1: not even a blank page exists; no unearned ambient container is smuggled into the derivation.
- **Syntactic Firewall:** Syntactic well-formedness under the 22 public starts in `mssn.ebnf` or 6 retained profiles verifies character sequence formation, not empirical truth.
- **Terminal Route Parity:** Maps local validation routes (`AcceptMSSN`, `RejectSmuggledContainer`, `RejectDiagonalSelfLoop`, etc.) into canonical terminals in `standard.yaml`.

### `nf.representation.tbnf` — Token-Bounded Normal Form (Levels 0–1)
- Eliminates lexical injection and out-of-alphabet ambiguities, constraining wires strictly to the 38-token alphabet $\Sigma = \{a..z, 0..9, <, >\}$.

### `nf.representation.dbcnf` — De Bruijn Cyclic Normal Form (Level 7)
- Eliminates spurious cycle enumeration by canonicalizing cyclic shift orbits to their minimal lexicographic necklace representative.

### `nf.evidence.ddanf` — Deterministic Data-Flow Architecture Normal Form (Level 12)
- Eliminates state desynchronization and untracked side-effects via the immutable 13-tuple trace ledger and 4-field kernel $K = (B, C, x, \Omega)$.

### `nf.runtime.zfnf` — Zero-Float Rational Normal Form (Level 18)
- Eliminates floating-point drift and artificial epsilon tolerance by enforcing exact rational arithmetic $a/b \in \mathbb{Q}$ and exact zero duality gaps.

### `nf.mssn.bqnf` — MSS-N Boundary-Quotient Normal Form
- **K0 Cycle Repair:** Formalizes the homological repair of closed 1-cycles ($d_1 b = 0$) via external 2-cell preimages ($d_{2,\text{ext}} c = z$) under the pinned 4-vertex, 5-edge, 1-face simplicial complex.
- **Receipt Firewall:** Enforces that `qed<exact>` literals remain `UNVERIFIED` until independent exact rational solver replay certifies $[z] = 0$.

### Higher Tower Contracts (`dhnf`, `obnf`, `scnf`, `asrf`, `tsnf`, `gnf`)
- Provide specialized normalizations for discrete Hodge decompositions, cost measure minimization, self-reference cycle refusal, and representation transport further up the tower.

---

## Claim Hygiene Quadrant

1. **What these contracts support:**
   - Formal anomaly exclusion, canonicalization, and deterministic terminal routing across finite data representations from Level -1 to higher tower stages.
2. **What they do not support:**
   - Do not claim relational project-join decomposition theorems (`qualifies_as_true_normal_form: false`).
   - Do not mint authority (`AuthorityEffect: None`) or establish unproved empirical truth.
3. **The narrowest defensible claim:**
   - Each extended form contract isolates a specific structural anomaly and verifies data invariants relative to explicitly declared parameters and boundary complexes.
4. **Next test needed:**
   - Execute test suites linking MSS-N level evaluators and K0 transcoders to these contract specifications.
