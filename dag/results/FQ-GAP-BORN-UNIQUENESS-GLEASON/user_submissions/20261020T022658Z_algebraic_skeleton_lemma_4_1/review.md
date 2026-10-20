# Lemma 4.1 review: algebraic skeleton and semialgebraic transfer

AuthorityEffect: None. Status: WRITTEN REVIEW ACCEPTED WITH THE EXPLICIT REPAIRS BELOW; not kernel checked. Original proposal retained separately, not overwritten. Namespace AS-4.1 is distinct from BR, CC, PC and DT.

## Mathematical verdict

Parts (a)-(d) are sound with standard field/Galois/Gauss-sum imports and ordinary complex-metric qualifications. Part (e) is sound for the explicitly translated finite semialgebraic witness language, with standard complex conjugation and algebraic parameters. The residual overstates what the skeleton and completion hypotheses establish. D3 is redundant once the full D2 scheme and field structure are assumed.

## (a) Characteristic

A nonzero field has characteristic zero or a prime ell. In characteristic ell, X^ell-1=(X-1)^ell, so the only ell-th root of unity is 1. D2 supplies a phase of order ell, a contradiction. This uses D1 and D2, not D3; it also resolves the rational interpretation in D3 without circularly assuming rational division in positive characteristic.

## (b) Roots, colimit, and involution

A finite subgroup G of field units is cyclic. One proof uses that a finite abelian group's exponent e is attained by an element (combine its prime-power components); all |G| elements satisfy X^e=1, so |G|<=e<=|G| and an element has order |G|. The order-n subgroup supplied by D2 contains n distinct roots of X^n-1; the root bound shows it is exactly all mu_n(K). Hence every torsion field unit is a phase: if v^n=1 then v is in this subgroup. Refinement of these algebraic root subgroups is automatic under divisibility.

The abstract direct system Z/m -> Z/n, k -> (n/m)k for m|n, has colimit Q/Z by k -> k/n. To identify it with the particular root groups, choose compatible primitive generators. Independently chosen primitive zeta_m,zeta_n need not satisfy zeta_m=zeta_n^(n/m). No canonical coherent generator choice is claimed. A Q-isomorphism from the splitting field K0 to the standard cyclotomic union supplies a coherent choice via exp(2pi i/n). This proves existence of an isomorphism, not a distinguished labeling.

An embedding of the algebraic K0 into Qbar exists by standard algebraic-extension theory; its image contains every root of unity and equals the cyclotomic union. The involution fixes Q and sends each root to its inverse, so every such isomorphism intertwines it with complex conjugation. The involutive field is unique up to isomorphism, not unique isomorphism. Gal is the inverse limit of (Z/n)^times; its conjugation element is -1 in the profinite units.

The algebraic inclusions do not prove a physical coarsening law for interferometers with additional apparatus data. D2 encodes such realization/coarsening as declared data; the proof only uses its subgroup-existence part. D2 is an infinite family of finite witnesses, not one finite witness or a derivation from finitely many tested n.

## (c) Rational weights: fixed square roots, not just square roots

To establish aa*=p, explicitly obtain a self-adjoint square root, not merely some root of X^2-p. For p=2, zeta_8+zeta_8^-1 is fixed by * and squares to 2. For an odd prime ell, let epsilon=(-1)^((ell-1)/2). The quadratic Gauss sum obeys g^2=epsilon ell and g*=epsilon g. If epsilon=1 take s=g; if epsilon=-1 take s=g/i, with i*= -i. In both cases s*=s and s^2=ell. This does not require knowing the analytic sign of the Gauss sum. Products give a fixed square root of each positive integer. For a/b>=0 with integers a>=0,b>0, take s_ab/b; for zero take 0. Then aa*=p, including all rational p in [0,1]. Thus D3 adds no restriction under D1-D2.

Kronecker-Weber states that every FINITE abelian extension is contained in some cyclotomic field. The union is Q^ab; an infinite abelian extension need not lie in one finite cyclotomic field. In abstract K write K0 isomorphic to Q^ab; equality is valid after choosing an embedding into Qbar. This theorem is a named imported result, not a new formal proof.

## (d) Density and incompleteness

Every embedding sends roots of unity to roots of the same order; its restriction to K0 has the whole cyclotomic union as image and intertwines *. Density is in the usual complex absolute-value metric: Q(i) is already dense. Torsion phases are countable and dense but proper. Countability alone does not imply metric incompleteness (finite metric spaces and the integers in the usual metric are complete and countable); here the missing premise is density in C. A complete subspace of a metric space is closed. K0 is dense and proper in C, so it is not complete for the inherited metric. No topology is derived from D1-D3.

For non-algebraic-closure, any algebraic element of Q^ab lies in a finite abelian extension, whose intermediate fields are Galois over Q. The real root cbrt(2) generates a nonnormal degree-three extension by Eisenstein and its missing nonreal conjugates; it cannot lie in Q^ab. Therefore X^3-2 has no root in K0 (the other roots would yield the real one using zeta_3 in K0).

## (e) The transfer statement is valid in its language

Fix Qbar inside C with STANDARD conjugation. Write each complex variable z=x+iy and each algebraic parameter c=a+ib with a,b real algebraic. Translate conjugation as (x,y)->(x,-y), polynomial equality as equality of both coordinates, and inequation as the negation of that pair of equalities. Weight comparisons must mean polynomial real inequalities between these coordinate expressions (e.g. |z|^2<=r), with algebraic real parameters. Every resulting finite witness is a finite semialgebraic formula over R_alg. R_alg and R are real closed and quantifier elimination makes the inclusion elementary. Thus existential satisfiability transfers in both directions. The same translation actually handles all first-order formulas in this language with these parameters. Add i as a named algebraic parameter for the coordinate identification; no unqualified parameter-free bi-interpretability claim is needed.

Requiring u u*=1 is one such equation, so phase-variable witnesses transfer between U(1)(Qbar) and U(1). This is a statement about existence for finite formulas, not equality of solution sets, individual identifications, executable preparation of every algebraic point, or preservation of arbitrary topological/physical predicates. It excludes transcendental parameters, unrestricted analytic functions, algebraicity predicates, integer quantification, infinite configurations and infinite conjunctions such as u^n!=1 for every n. It does not transfer to K0 or to the torsion phase group mu_infinity.

Two exact counterexamples to stronger interpretations:

1. W: x^3=2 is realizable in C and Qbar but not in K0=Q^ab. Hence K0 is not an upper ceiling for arbitrary finite polynomial witnesses.
2. W: u=(3+4i)/5 and uu*=1 is realized in K0 and U(1)(Qbar), but not in mu_infinity. If this u were a root of unity, u+u^-1=6/5 would be a rational algebraic integer and hence an integer, contradiction. Thus finite polynomial data CAN distinguish torsion-only phase models from the algebraic circle; this does not contradict (e).

## Residual and competitor repairs

K0 is a minimal forced involutive subfield, not an upper bound on K or all finitely realizable algebra. K=K0, K=Qbar and K=C all satisfy D1-D3. The norm witnesses do not choose between them. Calling Qbar a sufficient algebraic realization domain for the specified witness language is justified by (e); calling it the only possible field is not.

Z[i] already fails D1's field requirement; its norms are integer sums of squares so p=1/2 also refutes D3 concretely. Q(i) fails D2 at n=3. It also fails D3 at p=1/3: rational x,y with x^2+y^2=1/3 would yield primitive integer X,Y,Z satisfying 3(X^2+Y^2)=Z^2. Modulo 3 gives 3|Z, then X^2+Y^2=0 mod3 forces 3|X,Y, contradicting primitivity. Full Phi(K0) contains nontorsion phases; it is not mu_infinity.

A precise completion import is: choose an embedding in C and its ordinary absolute-value metric, then take metric completion (or require this subfield to be complete for that metric). Its completion is C by density. The completion of the torsion subgroup in the inherited circle metric is U(1). Mere continuity of a selected family of reversible transformations is not a scalar-completion theorem. Closure of a state space needs its ambient space, topology and density link specified. Local tomography only discriminates among specified real/complex/quaternionic composite models under their composition hypotheses; it is not a premise-free selection of C among all theories.

## Existing Lean evidence boundary

Local lean4/H052CyclotomicTowerDirected.lean proves conductor divisibility/directedness and integer record identities; is_cyclotomic_subfield is DEFINED as Nat divisibility. It is not a construction of actual cyclotomic fields, roots or this colimit. lean4/QuadraticGaussReduction.lean contains actual finite-field character reductions, but has not been compiled or connected to Lemma 4.1 in this review. Source presence is not a certificate of the current theorem. The proposed Mathlib identifiers are not confirmed against an installed dependency in this turn; no formalization-effort estimate or new Lean theorem is claimed.
