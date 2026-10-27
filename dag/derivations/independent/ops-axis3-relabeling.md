Status: AI-drafted, awaiting human review.

# OPS-AXIS3-RELABELING

The node stays CONDITIONAL. This note records the composition step from a declared export. Hypotheses (i) and (ii) are not used.

## The composition step

Let Exp send a history to an export, and let Vbar send an export to a verdict. Define V(H) as Vbar applied to Exp(H).

Let sigma be a function on histories. Assume Exp(sigma(H)) equals Exp(H) for each history H. Substitute that equality into Vbar. Then V(sigma(H)) equals V(H) for each history H.

The argument does not use injectivity of sigma.

## One export

Let a history be a list of natural numbers. Let Exp be the length of the list. Let sigma replace each entry by the map that sends 0 to 1, sends 1 to 0, and sends each other natural number to itself.

Mapping a list does not change its length. A verdict of that length is therefore unchanged.

## What is proved

- If an export is unchanged by sigma, the verdict that reads only that export is unchanged.
- List length is unchanged by any token map, including the map that swaps 0 with 1.
- A verdict of that length is unchanged by the same map.

The Lean declarations are `exportVerdictRelabel`, `lengthMapInvariant`, and `lengthVerdictRelabel` in `lean4/ObserverPresheafAxis3Relabeling.lean`.

## What is assumed

Function application and the length of a mapped list. No new axiom is declared. The node status stays CONDITIONAL. Hypotheses (i) and (ii) are cited, not re-run.

## What is open

A commute of sigma with a transition step, constancy of a conserved charge, a defect value, and whether a drop is a repair or a reinterpretation stay outside this slice.
