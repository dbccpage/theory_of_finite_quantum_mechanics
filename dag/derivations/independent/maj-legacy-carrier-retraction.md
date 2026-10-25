Status: AI-drafted, awaiting human review.

# MAJ-LEGACY-CARRIER-RETRACTION

## Identity coboundary

For a size t, a 1-cochain is a function from a t-element index set to the two-element set {false, true}. The coboundary d0 sends each such function to itself. The next coboundary d1 sends every such function to the zero function on a one-element index set. Composing them still yields that zero function.

## Exactness

A 1-cochain w is exact when some vertex function a has d0(a) = w. Taking a = w meets that equation, because d0 is the identity. The same w is a cocycle, because d1(w) is the zero function.

## Closed residual

A closed residual is a cocycle that is not exact. The identity coboundary makes every 1-cochain exact, so no 1-cochain is a closed residual. The four sizes t = 1, t = 2, t = 3 and t = 4 are the instances named in the standing text. Their function counts are 2, 4, 8 and 16, and the sum of those counts is 30.

## What is proved

On this identity coboundary, d1(d0(a)) is zero, every 1-cochain is exact, and none is a closed residual. The four sizes 1, 2, 3 and 4 are included.

## What is assumed

Bool and Fin are the ambient types of the argument. No measurement from an external carrier file is used.

## What is open

The recorded claim that a legacy carrier file had first Betti number 0 at those four sizes is not re-run here. A reading of logical sectors from that file, and a comparison with the tetron-array family, stay open.
