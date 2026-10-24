Status: AI-drafted, awaiting human review.

# Imaginary fugacity: finite staggered determinants and a center-orbit sum

AuthorityEffect: None. Target: `FSP-IMAGINARY-MU-REAL-DET` (queue rank 19).
Provisional outcome: **Narrowed**. The node remains `IMPORTED_ASSUMPTION`.
Rank 18 already had active work on its campaign branch when this target was selected.

## Declared model and the operator identity

Let P and N be arbitrary finite sets of even and odd sites, including color indices.
Set G = diag(I_P, -I_N). Let A: N → P and B: P → N be complex transport matrices.
The adjoint of a reverse link is part of the declared discretization, not a consequence
of primitive difference. For real mass m and nonzero fugacity z, define

```
D(m,z) = [ m I_P,  z A - z^-1 B^H ]
         [ z B - z^-1 A^H,  m I_N ].
```

The transport matrices can include real staggered signs, a hopping coefficient, and
real boundary signs. The independent model is an even temporal cycle with three colors,
SU(3) links, antiperiodic fermions and hopping coefficient 1/2. It has no spatial directions.
Its even/odd blocks are the matrices above. This is a finite one-dimensional staggered
model, not a four-dimensional QCD construction. The Lean statements allow arbitrary
finite block sizes and arbitrary transports; link unitarity is not needed for these identities.
The independent code constructs and checks its SU(3) links separately.

At imaginary chemical potential the conventional parameterization is z = exp(i a mu_I).
The formal input is instead the algebraic condition conjugate(z) z = 1.
`inverse_eq_star` derives z^-1 = conjugate(z), including exclusion of z = 0.
Writing X = z A - conjugate(z) B^H then gives

```
D(m,z) = [ m I_P, X; -X^H, m I_N ],   G D(m,z) G = D(m,z)^H.
```

`staggered_unit` and `staggered_adjoint` state these identities.
Here G is staggered site parity; identifying it with the source's gamma5 notation
does not supply a spin-taste reconstruction theorem. The exponential parameterization
is explanatory imported physics; no exponential approximation or floating number is evaluated.

## Reality is weaker than positivity

For any square finite D and G with G G = I and G D G = D^H,
taking determinants gives conjugate(det D) = det D, since det(G)^2 = 1.
This is `det_real_of_involution`. Two identical block-diagonal flavors then have
determinant (det D)^2, whose real part is nonnegative (`two_flavor_nonneg`).
No fractional root of a determinant is taken.

The implication from gamma Hermiticity to a single positive determinant is false:
G = diag(1,-1), D = diag(-1,1) obey the symmetry but det D = -1.
`gamma_hermitian_negative` certifies this exact counterexample.
It is a counterexample to that implication, not a positive-mass staggered counterexample.

For the declared bipartite staggered class there is a stronger theorem when m > 0.
At normalized mass one the Schur complement gives

```
det [ I, X; -X^H, I ] = det(I + X^H X) > 0.
```

The Gram matrix is positive semidefinite, so adding the identity is positive definite.
For arbitrary positive m, factor out m and replace X by X/m. The determinant acquires
the positive factor m^(|P|+|N|). `bipartite_det_pos` and `staggered_det_pos` state this
for arbitrary finite P and N, including empty parts. Thus a single unrooted staggered
flavor in this declared class has positive determinant. At zero mass strict positivity
need not hold: the independent two-site identity-link example at z = i has determinant zero.

## Exact witnesses and the periodicity fence

The independent checker uses Q(i), with three unit fugacities 1, i, (3+4i)/5,
three masses 0, 1/3, 1, and cycles of 2, 4, 6 sites: 27 exact cases.
For the two-site links diag(i,i,-1) and the rational color rotation with entries
3/5 and 4/5, the mass-one determinants are respectively 209/100, 209/50,
and 149281/62500. Each positive-mass determinant is also recomputed using the Schur
complement, independently of the full dense determinant.
With two-site links I and diag(i,i,-1), real fugacity z = 2 instead gives
2457/4096 + (315/256)i. The imaginary-fugacity symmetry does not extend to this input.

For a separate boundary-twist model let f(t) be the determinant with the unit phase t
on the final antiperiodic temporal link. Define the declared finite center ensemble
Z_orbit(t) = f(t) + f(w t) + f(w^2 t), where w^3 = 1.
`centerSum_periodic` states Z_orbit(w t) = Z_orbit(t) for any f: C → C.
This is a finite reindexing identity, not a proof about the QCD gauge measure.
The independent calculation uses w = (-1+i sqrt(3))/2 in Q(zeta_12), derives f as a
Laurent polynomial from the two-site matrix, and checks the coefficient identity exactly.
It obtains Z_orbit(1) = Z_orbit(w) = 345/32 and checks f(1) != f(w).
Thus reality of a determinant on a fixed gauge background does not imply center periodicity.
No thermodynamic phase transition follows from this finite sum.

The physical Roberge-Weiss statement concerns theta = mu_I/T and the full partition
function's period 2 pi/3 in theta. That measure and its invariance are still imported.
The boundary-phase/center distinction is also explicit in
[Kashiwa and Kouno, arXiv:1903.11737](https://arxiv.org/abs/1903.11737).
That literature statement is not counted as a local theorem.

## What is proved

Finite block operator adjoint identities, determinant reality, two-flavor nonnegativity,
strict positivity for the positive-mass bipartite staggered class, a negative determinant
with gamma Hermiticity alone, and algebraic periodicity of a declared finite center-orbit sum.
The replay binds the committed LF bytes and lists the axioms printed by Lean.
The independent checker checks explicit SU(3) links and all numerical witnesses exactly.

## What is assumed

The lattice discretization, even/odd split, real mass, unit fugacity, and reverse-adjoint
transport convention. The physical interpretation of fugacity and imaginary chemical
potential, and the literature's QCD measure and Roberge-Weiss theorem, remain imports.
Lean uses complex scalars symbolically; concrete arithmetic uses only the named exact fields.

## What is open

Four-dimensional source-regime refinement, spin-taste reconstruction, a full gauge-measure
formalization of Roberge-Weiss periodicity, any phase transition, and controlled continuation
to real chemical potential. No new status, sign-free real-density algorithm, continuum
theorem, or physical authority follows from these results.
