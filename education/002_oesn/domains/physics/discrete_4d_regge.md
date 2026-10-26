---
documentation_contract: symbol-game-documentation/v1
title: "Downstream Application: Discrete 4D Regge Curvature & Deficit Angles"
kind: mathematical-reference
layer: "downstream_application"
realizes: null
application_domain: "discrete_gravity"
authority_effect: "None"
genesis_effect: "None"
reflection_bridge: "unproved"
source_paths:
  - ../../sn.md
  - ../../_images/sn_21_discrete_4d_regge_curvature.svg
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
