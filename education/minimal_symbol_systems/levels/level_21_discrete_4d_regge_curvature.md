---
documentation_contract: education-documentation/v1
title: "MSS-N Level 21: Discrete 4D Regge Metric Deficit & Simplicial Curvature"
kind: grammar-reference
level: 21
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
  row: MSS-22
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
  - omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/_images/mss_21_discrete_4d_regge_curvature.svg
---

# Four-dimensional simplex geometry: open application obligations

AuthorityEffect: None. GenesisEffect: None. Application status: specification.

A declared Euclidean 4-simplex has ten pairwise squared distances. Its edge data
must satisfy Gram positive-definiteness; the corresponding squared-volume formula
uses the negative Cayley-Menger determinant sign in dimension four.

For an interior triangle hinge in a supplied piecewise-flat triangulation, the
deficit is 2*pi minus the incident dihedral angles. This definition imports the
metric and incidence data. It does not derive spacetime dimension or gravity.

The old statement that an arbitrary closed dual loop has identity holonomy is
withdrawn. Nontrivial curvature can produce nonidentity loop holonomy. A discrete
Bianchi identity needs a specified dual cell, orientation, transport paths and
ordered boundary construction. No such complete verifier is supplied by this note.

`Evaluator::Regge4DCurvature` was a target name, not implementation evidence. The
remaining obligations are validated metric input, explicit dual incidence,
transport construction, arithmetic/error bounds, and independent negative cases.
Finite boundary nilpotence alone does not establish these geometric obligations.
