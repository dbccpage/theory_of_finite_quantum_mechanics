---
documentation_contract: education-documentation/v1
title: "MSS-N Level 05: Regge Metric Simplices & Deficit Obstructions"
kind: grammar-reference
level: 5
status: active
maturity: research
atlas_status: specified
evidence_grades:
  named: true
  syntax: true
  computed: true
  Lean: false
  gated: true
successor:
  row: MSS-6
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
  - omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/_images/mss_05_regge_metric_simplices.svg
---

# Finite simplex metric data

AuthorityEffect: None. GenesisEffect: None. Application status: declared mathematical model.

For squared distances s_ij and vertex 0 as origin, define the Gram matrix
G_ij = (s_0i + s_0j - s_ij)/2. A nondegenerate Euclidean n-simplex requires
G to be positive definite. The signed Cayley-Menger determinant gives its
squared volume: V_n^2 = (-1)^(n+1) det(CM)/(2^n (n!)^2).
The determinant sign alone is not a sufficient general embeddability test;
positive definiteness requires the appropriate principal-minor conditions.

Declared Euclidean metrics may be used to calculate dihedral angles and interior
hinge deficits. Rational squared lengths need not give rational cosines or angles.
Floating-point angle evaluation is not a certified interval enclosure.

The earlier named `Evaluator::GramPositivity` and `Certifier::HingeDeficit`
were not evidence of an implemented verifier in this strand. No five-deficit
physical register, gravitational dynamics, or native Genesis survivor count is
established here. A working interval certifier and explicit triangulation fixtures
remain separate implementation obligations.
