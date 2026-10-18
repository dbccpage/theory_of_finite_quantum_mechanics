# Bounded reconstruction and division-free quartet equations

AuthorityEffect: None. Research checkpoint: 2026-10-11.
Parent checkpoint: `cbf2545c43c283a3a514e64904885e815be8dafa`.
The global exclusion remains open.

## Exact coverage by a bounded block chart

`MubBoundedBlockChart.lean` supplies the placement and reconstruction steps
left open by the preceding minor bound. For a raw Hadamard on `Fin 6`, the
twenty explicit column triples are extended to complete column permutations.
The selected triple occupies the last three columns. Unit row and column
phases dephase the entire matrix, with simultaneous transport of any further
unbiased bases. Reindexing to `Fin 3 + Fin 3` gives

\[
H=\begin{pmatrix}E&B\\C&D\end{pmatrix},\qquad
|\det B|^2\ge54/5.
\]

Determinant moduli are preserved by those phases. The upper-right block is
therefore invertible and has the already-checked entry bound
`normSq ((B⁻¹) i j) <= 10/27`.
The lower-left row-Gram equation gives

\[
CE^*+DB^*=0,\qquad D=-CE^*(B^{-1})^*.
\]

The predicate `Admissible E B C` consists of unit entries in `E,B,C,D`,
the first row and column of `E` equal to one, the first row of `B` and first
column of `C` equal to one, the determinant lower bound, and

\[
EE^*+BB^*=6I_3,\qquad CC^*+DD^*=6I_3.
\]

Here `D` is the forced expression, not another independent input block.
Its mixed Gram blocks vanish by the inverse identity. Thus the diagonal
Gram conditions imply the complete row Gram equation, and square-matrix
invertibility yields the column Gram equation. `Admissible.hadamard` checks
this soundness direction. `exists_admissible_chart` checks coverage, including
the actual forced-block equality. The existence and nonexistence equivalences
apply to the campaign's concrete normalized quartet predicate.

No external finite-corner theorem or finite-fibre predicate is imported by
this route. It does not identify the bounded minor with the external
finite-fibre minor. The two independently justified domains are alternatives
for a future exclusion; their intersection is not asserted to retain coverage.

## Removing the inverse without admitting singular solutions

`MubBoundedQuartetEquations.lean` sets

\[
q=|\det B|^2,\quad d=\overline{\det B},\quad
N=-CE^*(\operatorname{adj}B)^*,\quad
S=\begin{pmatrix}dE&dB\\dC&N\end{pmatrix}.
\]

The checked bound gives `q > 0` and `d != 0`. The adjugate formula gives
`d D = N` and `d H = S`. Consequently the forced-block constraints are
equivalent to the division-free equations

\[
|N_{ij}|^2=q,\qquad qCC^*+NN^*=6qI_3.
\]

The original top Gram equation, unit-entry constraints on `E,B,C`, gauge
constants and inequality `q >= 54/5` are retained in `BlockEquations`.
`blockEquations_iff_admissible` checks both directions. In particular, the
positive bound cannot be dropped after clearing denominators.

Let `U,V` be the two additional raw bases. Independent column phases fix
their first rows to one and preserve all three MU conditions. In addition
to their unit entries and Gram matrices `6I_6`, the remaining equations are

\[
|(S^*U)_{ij}|^2=6q,\qquad |(S^*V)_{ij}|^2=6q,
\qquad |(U^*V)_{ij}|^2=6.
\]

These are the fields of `QuartetEquations E B C U V`. The endpoint
`exists_quartet_iff_equations` checks

\[
\exists\text{ actual quartet in }\mathbb C^6
\quad\Longleftrightarrow\quad
\exists E,B,C,U,V:\operatorname{QuartetEquations}(E,B,C,U,V).
\]

`no_quartet_iff_no_equations` gives the corresponding universal negation.
Both are reductions; neither establishes that this system has no solution.

## Coordinates, verification and remaining work

After substituting the displayed gauge constants, the free entries consist
of four complex entries of `E`, six each of `B,C`, and thirty each of `U,V`:
76 complex or 152 ambient real coordinates. This is a coordinate count, not
a dimension or rank statement. Unit entries put every real and imaginary
coordinate in `[-1,1]`; `real_bounds_of_unit` checks that scalar implication.
The circle constraints remain part of the system.

The displayed operations are addition, multiplication, conjugation,
determinant, adjugate and norm-square. On real and imaginary parts they are
polynomial expressions, with rational constants and one determinant
inequality. The subsequent
[coordinate and polynomial checkpoint](bounded_polynomials_20261011.md)
checks the 152-coordinate codec and an indexed rational `MvPolynomial`
specification. The [expression checkpoint](bounded_expressions_20261011.md)
then checks upper degree bounds and finite term-list expansion. Complete
native coefficient export and an executable contractor interface remain pending.

The targeted canonical replay checked 19 block-chart and 15 equation
endpoints with only `propext`, `Classical.choice`, and `Quot.sound`. The
receipt binds exact source copies, dependency pins, logs and the orientation
negative control. It is not a full `Mub6` build.

Replay from `lean4/research_programs/mub6`:

```powershell
$env:LEAN_NUM_THREADS = '1'
lake build +MubBoundedBlockChart:olean +MubBoundedQuartetEquations:olean
```

The next substantive obligation is an exact infeasibility argument on this
whole bounded domain, or an exact solution giving a quartet. Coordinate
encoding and contractor work must preserve all five matrix variables and
the determinant inequality. A finite grid or a collection of unresolved
boxes cannot discharge that obligation. The known three-basis construction
still needs the separately recorded fresh concrete replay before claiming
the complete `N(6)=3` derivation.
