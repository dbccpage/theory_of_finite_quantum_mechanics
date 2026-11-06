---
documentation_contract: education-documentation/v1
title: "Downstream Application: Discrete Regge Metric & Hinge Deficits"
kind: mathematical-reference
layer: "downstream_application"
realizes: null
application_domain: "discrete_gravity"
authority_effect: "None"
genesis_effect: "None"
reflection_bridge: "unproved"
source_paths:
  - ../../sn.md
  - ../../_images/sn_05_regge_metric_simplices.svg
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
