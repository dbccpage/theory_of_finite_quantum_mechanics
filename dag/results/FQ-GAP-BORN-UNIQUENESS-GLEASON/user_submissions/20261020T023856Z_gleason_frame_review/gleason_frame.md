# Born-rule representation via frame functions: reviewed candidate

Status: CONDITIONAL ON AN EXTERNAL GLEASON IMPORT. Not kernel checked. AuthorityEffect: None. D1-D3 remain OPEN; D4 is a separate purity obligation. This result-folder candidate does not replace a live paper or frozen registry.

## Claim with the correct quantifiers

Fix a finite real or complex Hilbert space H, dimension n>=3. For EACH contextual assignment g(v,B) on all unit vectors in all orthonormal bases, suppose:

A1. Sum_(v in B) g(v,B)=1 for every orthonormal basis B.
A2. g(v,B)=g(v,B') when v belongs to both bases.
A3. Every g(v,B)>=0.

There is a UNIQUE density operator representing THAT assignment, in the declared real or complex operator category. There are MANY such assignments, one for each density operator. Neither a particular preparation nor purity is selected.

The full geometry, scalar carrier and orthonormal context family are inputs. Probabilities are not assumed quadratic in the elementary dictionary. Regularity supplies that dependence as an explicit import.

## Elementary dictionary

1. Every unit vector extends to a basis. A2 defines f(v) independently of that choice, A1 makes it a weight-one frame function, A3 makes it nonnegative. Completion to a basis gives f<=1.
2. Replacing v by lambda v, |lambda|=1, with the same orthogonal complement gives f(lambda v)=f(v). Thus f descends to rays.
3. For a projector P, sum f over a basis of its range. Extend two such bases by the same complementary basis to prove independence. This gives mu(P)>=0, mu(0)=0, mu(I)=1 and finite orthogonal additivity. Conversely such a projection measure gives the contextual assignment.

All sums are finite, but the hypotheses quantify over infinitely many contexts.

## Imported regularity

Gleason 1957, Theorem 3.5: a nonnegative frame function on a real or complex Hilbert space of dimension at least three is regular. Here that means f(v)=<v,Tv> for a self-adjoint T. This theorem, including the real-to-complex and global compatibility steps, is CITED, not reproduced or kernel checked. Continuity or measurability is not an additional premise in this finite-dimensional theorem. A rational-only ray set cannot be substituted silently.

## Density representation and uniqueness

Nonnegativity makes T PSD. A basis sum makes Tr(T)=1. The projector measure is mu(P)=Tr(TP). If two self-adjoint operators have identical evaluations on all unit vectors, homogeneity and real/complex polarization make them equal. Hence the representing rho is unique for the supplied assignment; conversely every density produces one. Over R rho is real symmetric; over C it is complex Hermitian.

If rank(rho)=1 is additionally proved, rho=P_psi and g(v,B)=|<v,psi>|^2. The vector is unique up to sign over R or phase over C. Purity does not follow from A1-A3.

## Counterexamples and their scope

- Dimension two: f(n)=(1+n_z^3)/2 on the Bloch sphere is continuous, nonnegative and normalized on antipodal pairs, but is not a density evaluation. Plain continuity does not repair the qubit projector theorem.
- Context dependence: selecting the largest-overlap atom in each basis is a normalized nonnegative contextual assignment. The rational shared-ray bases in review.md show its A2 failure.
- Missing normalization: fourth powers of overlaps have total 1 in a basis containing psi and total 337/625 on a specific rationally rotated 3D basis.
- Missing nonnegativity: a normalized nonlinear additive real function composed with squared overlaps gives an unbounded frame function. It is a choice-dependent proof obstruction, not a numerical sampler.
- Restricted event geometry: classical events DO have diagonal trace representations. A coordinate context fails to determine off-diagonal entries. This is an identifiability example, not nonexistence of trace form.

## Alternative effect route

In any positive finite dimension admit effects 0<=E<=I and EVERY finite INDEXED POVM (E_i)_i with sum E_i=I, keeping repetitions and zero slots. Require nonnegative normalization and one value f(E) for each effect across slots and contexts. Comparing (E,F,I-E-F) with (E+F,I-E-F) gives additivity for E+F<=I. Positivity gives monotonicity; subdivision gives rational homogeneity; rational bounds squeeze real homogeneity on a real/complex carrier. Scaling extends to the positive cone independently of scale; differences extend to self-adjoint operators independently of decomposition. Finite-dimensional real symmetric or complex Hermitian trace duality then gives a unique density for the supplied f. Optional complex-linear extension applies only over C.

This imports all-effect context compatibility. It is not derived from orthogonal-context sheaf gluing. A rational-only version stops before real homogeneity and needs its own carrier-specific statement.

## Open obligations

D1. Construct the Hilbert carrier, scalar field and dimension>=3, and identify atoms/contexts with ALL rank-one projectors and ALL orthonormal bases. Declare metric or scalar-completion imports.
D2. Prove nonnegative basis-independent normalization without assuming the desired formula.
D3. Supply compatible local evaluation maps showing that gluing of source sections makes probability evaluations agree on shared rays.
D4. Establish purity separately if the vector-state Born formula is required.

A theorem citation and finite controls do not discharge these obligations. A declared extension to a larger full-projector model is another possible strengthening for a qubit; no unique choice of route is asserted.

## Verification policy

Use exact rational/algebraic witnesses to refute specific overclaims. Finite sampling and least-squares fitting do not prove universal axioms or general nonrepresentation. The nonmeasurable example remains proof-only. The accompanying exact replay checks bounded arithmetic and the dictionary, not Gleason regularity.
