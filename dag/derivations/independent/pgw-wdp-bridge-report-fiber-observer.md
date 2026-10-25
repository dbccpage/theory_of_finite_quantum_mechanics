Status: AI-drafted, awaiting human review.

# PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER

For arbitrary types X, R and D, a report r:X→R and a decision d:X→D admit a unique decoder on the actual image of r exactly when d is constant on every fibre of r. Equal reports with unequal decisions remain an obstruction after every report-only postprocessor. The joint report (r,d) is sufficient for d.

## Derivation

A decoder maps equal report values to equal decisions, proving necessity. For sufficiency choose a representative of each occupied report; fibre constancy makes its decision independent of the representative. Any other decoder must agree at every occupied report, proving uniqueness by function extensionality. A postprocessor preserves equality of reports, so cannot separate conflicting decisions. Projection from the joint report recovers the decision. The proof includes empty X without assuming an inhabited decision type.

## What is proved

For arbitrary types X, R and D, a report r:X→R and a decision d:X→D admit a unique decoder on the actual image of r exactly when d is constant on every fibre of r. Equal reports with unequal decisions remain an obstruction after every report-only postprocessor. The joint report (r,d) is sufficient for d.

## What is assumed

The types, maps and algebraic models named above are declared. Lean uses only its standard core axioms. The independent audit enumerates finite functions and compares their values exactly. AuthorityEffect: None.

## What is open

The maps are declared. The result constructs no evaluator, permission grantor or physical authenticity test. The decoder is classical/noncomputable in general. Unused reports require no default value, and the empty case is included.
