# Wilson row-swap mutation adjudication

AuthorityEffect: None.

The mutation `determinant-row-swap-sign` replaces `det = -det` with
`det = det` in `direct_wilson_determinant` (now composed into
`checks/checker_support/wilson_operator.py`). The executed
test outcome remains **survived** in the raw campaign receipt. The following
argument establishes equivalence for this file's admitted inputs, rational
mass `m` and Wilson parameter `r`, and its fixed 8-by-8 matrix. This does not
establish equivalence for general Gaussian elimination. The other tested
mutation of this file, changing elimination subtraction to addition, is killed.

Put `s = m + 2r`. Simultaneously permuting rows and columns into the index sets
`(0,2,4,7)` and `(1,3,5,6)` exposes independent blocks

```
A = [ s -r -r  0 ]       B = [ s -r -r  0 ]
    [-r  s  0  1 ]           [-r  s  0  1 ]
    [-r  0  s  1 ]           [-r  0  s -1 ]
    [ 0 -1 -1  s ]           [ 0 -1  1  s ]
```

Both blocks have the same leading 3-by-3 block, with leading principal minors
`s`, `s²-r²`, and `s(s²-2r²)`. The implementation processes the first three
coordinates of these blocks in alternating order, then the fourth coordinate
of B and of A. Row elimination does not mix their supports.

* If `s != 0` and `s² != r²`, the first two pivots in each block are nonzero.
  The third is nonzero too: `s² = 2r²` with rational `s,r` forces both to be zero,
  contrary to `s != 0`. Hence no row swap occurs before the final coordinate of
  either block. At that coordinate, no later row has a nonzero entry in that
  block's column; a zero pivot returns determinant zero, rather than swapping.
* If `s != 0` and `s² = r²`, the second pivot in each block is zero and the next
  row has entry `-r²/s = -s != 0`. The implementation swaps rows 2 and 4, and
  rows 3 and 5: exactly two swaps. The leading 3-by-3 determinant is `-s³`, so
  the third pivot is then nonzero in each block. Final pivots again either
  require no swap or return zero.
* If `s = 0` and `r != 0`, rows 0/2 and 1/3 are swapped. After these pivots,
  row 4 becomes the zero row: its initial entries coincide with the original
  row 2 when `s=0`. Its column has no surviving candidate in block A either;
  column 4 returns determinant zero. In particular, A is singular.
* If `s = r = 0`, column 0 immediately returns determinant zero.

Thus every nonzero returned determinant has **zero or two** swaps. Multiplying
by `-1` at each swap has net factor `+1`; every remaining branch returns zero.
Removing these sign flips preserves every returned value on the admitted domain.
Input admission is unchanged by the mutation.

As an independent algebra check, SymPy 1.14.0 gives
`det(A) = s²(s²-2r²+2)` and `det(B) = (s²-2r²)(s²+2)`. This check corroborates the
singular case; the case argument above, not a finite search or a passing test,
is the basis for equivalence. A 729-pair rational search also found no differing
result, but that search alone was explicitly not treated as a proof.

The adjudicated ledger may exclude this one candidate as **demonstrably
equivalent**, retaining the raw observed outcome and this justification. No
timeout, import failure, or other survivor is excluded by this argument.
