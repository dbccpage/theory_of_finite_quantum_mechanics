Status: AI-drafted, awaiting human review.

# FSP-WILSON-DIRAC-GAMMA5

AuthorityEffect: None.

The node statement is unchanged. This note records the part that is checked and the part that remains open.

## Operator

On a finite set of sites, with a direction index `μ`, a spin space, and a color space, the Wilson-Dirac operator at Wilson parameter `r = 1` and real bare mass `m` is the matrix

```
(D ψ)(x) = (m + d) ψ(x)
  + Σ_μ (1/2) (γ_μ - 1) U_μ(x) ψ(x+μ)
  + Σ_μ (-1/2) (γ_μ + 1) U_μ(x-μ)^† ψ(x-μ)
```

The spin matrices are a Euclidean Clifford representation: each `γ_μ` is hermitian, `γ_μ γ_ν + γ_ν γ_μ` is `2` on the diagonal and `0` off it, and `γ5` is hermitian, squares to `1`, and anticommutes with every `γ_μ`. When a forward hop and a backward hop land on the same site, the two blocks are added.

The intended adjoint identity is `γ5 D γ5 = D†`. The bookkeeping that would support it uses hermiticity of the gammas, hermiticity of `γ5`, `γ5^2 = 1`, the anticommutation `γ5 γ_μ γ5 = -γ_μ`, reality of `m`, and `(M†)† = M`. Link unitarity is the domain hypothesis for the gauge-theory operator. That identity is not a Lean theorem in this checkout.

## What is proved

In `lean4/FermionSignWilsonDiracGamma5.lean`, with axioms `propext`, `Classical.choice`, and `Quot.sound`:

- `euclideanClifford2` is a Euclidean Clifford representation in dimension 2 on spin space `Fin 2`. The matrices are `γ0 = [[0, 1], [1, 0]]`, `γ1 = [[1, 0], [0, -1]]`, and `γ5 = [[0, I], [-I, 0]]`.
- `euclideanClifford4` is a Euclidean Clifford representation in dimension 4 on spin space `Fin 2 ⊕ Fin 2`, with the chiral block form `γ_k = off( (-I) σ_k , I σ_k )` for `k = 0, 1, 2`, `γ3 = off(1, 1)`, and `γ5 = diag(1, -1)`.
- `charpoly_rootMultiplicity_conj` states that if every coefficient of a complex polynomial is fixed by conjugation, then each root and its conjugate have the same algebraic multiplicity. The coefficient hypothesis is an assumption of the theorem.
- `two_flavor_det_eq_sq` states that for every square matrix `D`, the determinant of the block matrix `diag(D, D)` equals `(det D)^2`.
- `two_flavor_det_real_nonneg` states that if a complex number `z` is fixed by conjugation, then `z^2` has imaginary part 0 and real part at least 0.

These declarations do not mention a Wilson-Dirac operator.

## What is assumed

The Clifford theorems assume the matrices written above. The root-multiplicity theorem assumes conjugation-fixed coefficients. The nonnegativity theorem assumes that its input is already fixed by conjugation. The independent check assumes the Wilson formula at `r = 1`, periodic extents `(2, 2)`, mass `-1`, color `U(1)`, and the link phases recorded in `checks/independent/fsp-wilson-dirac-gamma5.py`.

## What is open

The identity `γ5 D γ5 = D†` for this operator, reality of `det D`, conjugate multiplicities of its characteristic polynomial, and nonnegativity of `(det D)^2` for two degenerate flavors are not Lean theorems here. Odd dimensions, the continuum limit, doubler decoupling, and anomaly inflow are outside this note.

An exact SymPy check on the one `2×2` configuration above rebuilds the `8×8` matrix from the formula, checks `γ5 M γ5 = M†`, and finds determinant `-3`, characteristic polynomial `[1, -8, 28, -56, 66, -40, 4, 8, -3]`, and two-flavor determinant `9`. That check is not a Lean proof. A single flavor on that configuration is a negative real, so nonnegativity of one determinant is not claimed.
