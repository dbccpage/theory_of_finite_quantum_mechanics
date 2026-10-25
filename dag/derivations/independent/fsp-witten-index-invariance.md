Status: AI-drafted, awaiting human review.

# FSP-WITTEN-INDEX-INVARIANCE

For every natural-number energy list P, every integer weight function w with w(0)=1, and all zero-mode multiplicities b and f, the difference of weighted sums over b zeros followed by P and f zeros followed by P equals b-f. It is independent of w.

## Derivation

Write each spectral trace as its zero-mode contribution plus the weighted sum over P. Each zero contributes w(0)=1. The same sum over P occurs with opposite signs and cancels, leaving b-f. This coefficient-wise cancellation explains the weight independence. Equal nonempty zero sectors give the zero-index counterexample.

## What is proved

For every natural-number energy list P, every integer weight function w with w(0)=1, and all zero-mode multiplicities b and f, the difference of weighted sums over b zeros followed by P and f zeros followed by P equals b-f. It is independent of w.

## What is assumed

The types, maps and algebraic models named above are declared. Lean uses only its standard core axioms. The independent audit uses exact integers, rational values and symbolic polynomials. AuthorityEffect: None.

## What is open

Pairing is supplied by the shared spectral list; this does not derive that pairing from an arbitrary supercharge, spectral decomposition on a Hilbert space, the analytic exponential trace, or the ground-energy theorem. The full imported Witten-index statement remains open here.

## Zero-index example boundary

The pinned `zero_index_with_ground_modes` declaration states only that the weighted trace of `[0]` minus itself is zero and that `(1 : Nat) + 1 > 0`. Its normalization hypothesis is unused. It does not state a list-membership or zero-mode-count proposition, and it is not cited as a witness for the node-level cancellation claim. The independent Python audit separately checks fifteen constructed equal-multiplicity spectral pairs: both lists contain an explicitly counted zero-energy entry while their symbolic trace difference vanishes. This is a checked example, not an additional general Lean occupancy theorem.
