# Global affine reduction to 320 real coordinates

AuthorityEffect: None.

The proved transition row and column sums now eliminate 66 real coordinates
from the quadratic quartet model. Actual quartet existence is equivalent to
a common zero of the substituted 648 rational polynomial equations in
`[-1,1]^170 × [-10035/4096,10035/4096]^150`. Every substituted polynomial
still has total degree at most two. Infeasibility remains open.

## Completion formula and coverage

For a transition matrix with all row and column sums equal to six, retain
its leading `5 × 5` block `A`, using ordinary zero-based matrix indices.
The remaining entries are

\[
W_{i5}=6-\sum_{j<5}A_{ij},\qquad
W_{5j}=6-\sum_{i<5}A_{ij},\qquad
W_{55}=\sum_{i,j<5}A_{ij}-24.
\]

`MubBalancedCompletion.lean` proves both sums of the completed matrix and
both reconstruction directions over any commutative ring. No division or
invertibility assumption occurs. Each of three transitions loses eleven
complex entries, giving 66 fewer ambient real coordinates.

`MubBalancedQuadraticLift.lean` supplies `compress` and `expand` for the
actual quartet model. Compressing an expanded assignment returns that
assignment unconditionally. Expanding a compressed full solution returns
that full solution, using the already proved transition balances.
`exists_quartet_iff_balanced_lift` checks the global existence equivalence.
The first 170 matrix-entry coordinates are retained; each transition now has
25 free complex entries. These counts are not solution-dimension claims.

The reduced system retains every original full-matrix equation after
expansion. It does not assume that row and column sums alone imply unitarity,
mutual unbiasedness, or quartet existence.

## Polynomial semantics and bounds

`MubBalancedQuadraticPolynomials.lean` constructs the affine replacement for
each original real variable and substitutes it into every original equation.
`replacement_eval` and `substitute_eval` identify evaluation with the actual
expanded matrices. `solution_iff_system` and
`exists_quartet_iff_balanced_polynomials` preserve quartet existence.
The generic `affine_substitution_degree` lemma and `equation_degree` check
that this substitution cannot increase the original degree-two bound.

Bounds on reconstructed entries require the equations. `expand_inBox`
has both reduced-system and reduced-box hypotheses. An arbitrary point of
the reduced box need not expand into the old box: the all-zero free assignment
is in the reduced box, but its completed transition corner is `-24`.
`zero_expansion_not_narrowBox` and `zero_not_system` check this counterexample
and prevent using unconditional box containment in a future search.

## Evidence and next obligation

The three new modules have 27 displayed endpoints. Their scoped Lean 4.33.1
build and transitive axiom reports admit only `propext`, `Classical.choice`
and `Quot.sound`. Sources, dependency pins, diagnostics and manuscript outputs
are bound by `artifacts/mub6_balanced_reduction_20261011_receipt.json`.

From the canonical Lean package, the scoped command is:

```powershell
$env:LEAN_NUM_THREADS = '1'
lake build +MubBalancedQuadraticPolynomials:olean
```

This checkpoint does not export the new coefficient lists, run a native
320-coordinate contractor, or establish a solver speedup. Affine substitution
can increase polynomial density despite decreasing the coordinate count.
The next operational check is therefore an exact coefficient export and size
comparison before choosing the representation for a coverage-preserving
exclusion search. The earlier 386-coordinate solver and its regional
exclusion receipts remain separate, unchanged evidence. No complete cover,
global quartet exclusion, quartet witness, or `N(6)=3` result is claimed.
