Status: AI-drafted, awaiting human review.

# FSP-REGGE-DEFICIT-ACTION: finite deficit-action expansion and area dependence

For any commutative ring and finite hinge set, the action S=sum_h A_h*(tau-sum_j theta_hj) equals tau*sum_h A_h-sum_h A_h*sum_j theta_hj. For fixed deficits it is linear in the declared areas, and splitting an area while keeping its deficit fixed preserves its contribution. Zero deficits imply zero action. Declared integer data also show that zero total action need not mean zero deficits, and changing areas can change the action on the same finite index set.

AuthorityEffect: None.

## Derivation

For a finite set of hinges, write the declared deficit at h as tau minus the finite sum of angles around h. Distribute multiplication by A_h and then the finite sum. Commutativity identifies the first term with tau times the sum of areas. This proves the displayed deficit-action expansion over any commutative ring.

For fixed deficits, replacing A_h by a*A_h+b*B_h gives a*S(A)+b*S(B). The one-hinge identity A_1*epsilon+A_2*epsilon=(A_1+A_2)*epsilon expresses an area split with an unchanged deficit. It does not assert that an actual triangulation refinement preserves the geometric deficits.

If every deficit is zero, every summand vanishes. The converse fails for declared integer data: two unit areas and deficits 1 and -1 give zero action while the deficits are nonzero. One hinge with deficit 1 gives action 1 or 2 when its area is declared to be 1 or 2.

The independent audit uses symbolic matrix contraction and expansion, plus exact integer samples and the stated cancellation and area-dependence witnesses. These are algebraic data; their realization by simplices and their continuum behavior are separate questions.

## What is proved

For any commutative ring and finite hinge set, the action S=sum_h A_h*(tau-sum_j theta_hj) equals tau*sum_h A_h-sum_h A_h*sum_j theta_hj. For fixed deficits it is linear in the declared areas, and splitting an area while keeping its deficit fixed preserves its contribution. Zero deficits imply zero action. Declared integer data also show that zero total action need not mean zero deficits, and changing areas can change the action on the same finite index set.

## What is assumed

The mathematical structures and operations are exactly those declared in `lean4/CampaignReggeFiniteAction.lean`. Areas, angles and the full-turn parameter are declared algebraic data. Geometric realizability, actual triangulation moves, Lorentzian signature, convergence to the Einstein-Hilbert action, and fermion-sign consequences are not established.

## What is open

On a 4D triangulation with squared edge lengths, the deficit angle at a hinge h is epsilon_h = 2 pi - sum of dihedral angles at h and the Regge action is S = sum_h A_h epsilon_h; its convergence to the Einstein-Hilbert action under refinement is a literature result imported here.

Regge calculus carries no fermion-sign content in this package; Lorentzian signature, convergence conditions and any sign consequence need separate evidence (ledger GIN-C13).
