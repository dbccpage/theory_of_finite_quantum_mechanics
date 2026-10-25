Status: AI-drafted, awaiting human review.

# FSP-KITAEV-HONEYCOMB-SOLUTION

On integer amplitudes indexed by a gauge bit and a matter bit, define W(v)(g,b)=sign(g)*v(g,b) and H(v)(g,b)=sign(g)*v(g,not b). Both square to the identity and commute. The two gauge-sector projectors commute with H and sum to the identity; the restricted hopping blocks are X and -X.

## Derivation

The gauge coordinate is unchanged by hopping. Multiplication by its sign therefore commutes with the matter flip. Applying either operator twice multiplies by sign(g)^2=1 and flips the matter coordinate either zero or twice. Sector projection tests only g, so it commutes with hopping. The projectors are complementary. The independent matrix audit additionally realizes X=i Z Y using exact Pauli matrices; this matrix interpretation is checked by Python, not claimed as a Lean honeycomb proof.

## What is proved

On integer amplitudes indexed by a gauge bit and a matter bit, define W(v)(g,b)=sign(g)*v(g,b) and H(v)(g,b)=sign(g)*v(g,not b). Both square to the identity and commute. The two gauge-sector projectors commute with H and sum to the identity; the restricted hopping blocks are X and -X.

## What is assumed

The types, maps and algebraic models named above are declared. Lean uses only its standard core axioms; exact audit arithmetic uses integers, rational numbers and symbolic polynomials. AuthorityEffect: None.

## What is open

This is one exact gauge-controlled hopping block. No honeycomb lattice, all plaquette operators, physical gauge projection, global flux-sector sum or sign-free sampling theorem is constructed.
