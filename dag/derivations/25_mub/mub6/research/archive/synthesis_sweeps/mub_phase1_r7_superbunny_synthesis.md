# MUB(6) Phase 1 Step 1.3: Singular Segre Branch (Subgap R7) Super Bunny Alpha Synthesis

**Date:** 2026-09-29T03:55:04.907832+00:00  
**Model:** Super Bunny Alpha (`stealth/space-bunny-alpha`)  
**Firewall Line:** `stated region only; mints no authority`  
**Latency:** 0.84s | **Tokens:** 9365  

---

## Reasoning Trace

<details><summary>Click to view internal reasoning (32657 chars)</summary>

```
We need craft answer. Need analyze task, likely impossible requests / insufficient data. Need maintain firewall exact phrase perhaps acknowledge NOT MUB... They demand zero hype words prohibited. Need rigorous claim discipline four parts. Need not assert false. Need likely explain no explicit f or SOS can be constructed from background; indeed formulation impossible: polynomial vanishing on algebraic closure of union and positive &gt;= eps at all points distance &gt;= delta? Need parse.

"algebraic closure of B6(theta) cup S6 cup H6" ambiguous: Zariski closure likely. A nonzero polynomial cannot vanish on Zariski closure if it is whole V(I55) maybe branch? If vanishes on dense algebraic subset, vanishes entire irreducible component. Then cannot positive on detached points. If entire ideal's real variety connected algebraically? Any polynomial vanishing Zariski dense on component extends. There may be no detached components under claimed certified classification, but circular.

B6(theta) one-parameter non-affine family? Complex H 6x6 orbit perhaps curve. "algebraic closure" of B6 theta likely itself algebraic family. A polynomial in x,y vanishing on curve can be degree low. Need f_sep globally satisfying f=0 on union and &gt; eps for all points distance &gt;= delta from union. This is impossible on points in same Zariski closure? Euclidean detached real semialgebraic components may be in same algebraic irreducible component, any polynomial vanishing Zariski dense set indeed vanishes there. If family is Zariski dense in some high-dimensional component? Need assess B_6(theta) 1-param non-affine Szollosi family perhaps affine orbit? It might be curve, not dense. But union orbit? They say collar neighborhood of B6(theta) ∪ isolated matrices perhaps B6(theta) set, not full orbit. Algebraic closure curve.

The assertion "all points at distance &gt;= delta" includes points on excluded same algebraic locus not in set if Zariski closure relation. If real points of algebraic curve outside parameter range/certified cells? If B6(theta) all theta, okay. Still detached components could intersect closure. But unknown.

Also compactness needed: existence of positive lower bound over all points outside delta-neighborhood? Function f-sep-distance continuous, positivity on open set does not imply uniform lower bound unless closed set and compact ambient. V_R(I55) compact: each 25 row vectors on S1, product (S1)^25 compact. Distance set >=δ closed, yes. But if no such points vacuous. Need choose δ < perhaps certified collar 0.001. They mention delta<1/1000. "distance >= delta" and collar likely < delta. A separating polynomial might use squared distance, but distance non-polynomial. Need finite polynomial.

Could choose f vanishing on target and nonnegative globally, positive exactly target? Polynomial vanishing target and positive outside? If target Zariski dense in component impossible. If isolated target and curve, possible maybe ideal powers. But positivity at exterior and zero on target can be crafted e.g. sum generators? On compact variety with target. If f=0 on curve but detached continuum not in Zariski closure can find polynomial. But detached 0-d points: nonzero polynomial over infinite field cannot vanish on entire positive-dimensional curve and only isolate separate points, okay ideal of curve does not contain points. Yet positive lower bound. But knowing exact coordinates absent.

Question asks exact f, degree monomials, exact SOS. We cannot derive from aggregate information. Worse theorem as stated malformed types: P_corner H for 3x3 corner? H Matrix Fin6 complex, P_corner 3x3. IsCH6 undefined. Orbit relation signatures. B6 theta? Matrix families. "using standard axioms [propext, Quot.sound]" Lean standard axioms include Classical.choice maybe propext, Quot.sound. `Quot.sound` is theorem, not axiom? In Lean, Quot.sound : ∀ {α} {r}, r a -> Quot.mk r a = ... theorem. propext axiom. Can't use Quot.sound to prove mathematical classification. Also the theorem is not valid as written perhaps B6 not orbit? "H in Orbit B6" Hmm B6(theta), H6 confusion. Orbit of a family/matrix? Orthogonal conjugacy `∃ U, H = U* B6? U`. If classification known? Background states "certified canonical components on this locus" but no equations/computational certificates. Could accept as hypothesis? Need distinguish.

Potential logical contradiction: target theorem claims every CH6 singular corner is in orbit of B6/S6/H6. B6(theta) 1 parameter and orbits under U(6) have 36-ish dimensions; notation needs set existential. Also B6 family perhaps H? Need exact signatures.

Could formulate conditional theorem with explicit `SubgapR7` hypothesis encoding exhaustion or separation/SOS. But asked exact theorem declaration. We should not manufacture proof. Need explain.

SOS equation:
`-1 = s0 + Σ h_i f_i + sum_j s_j g_j`.
If all g_j >=0 on V(I) and g=P? Equality guards. If include P=0 as a "guard", equality polynomial g_j=0 not nonnegative. Multiplying by arbitrary SOS still zero, but equality must enter ideal via h P perhaps not semialgebraic SOS certificate. In quadratic module, equalities represented as ideal terms, not g guard. Stengle: infeasible basic closed semialgebraic set can yield weighted SOS. In real algebraic setting:
`-1 = σ0 + Σ_i h_i f_i + Σ_j σ_j g_j` with f_i all vanish; g_j ≥0. Equality h=P in ideal term. If guard `f_sep - ε ≥ 0`, though we're trying prove there are no points at distance >= δ, but polynomial positivity does not encode Euclidean distance. Need encode distance. Exact polynomial distance from union? Euclidean distance to an algebraic set; squared distance may not be polynomial unless projection; semialgebraic formula with existential variables and squared distance:
`Dist²(Z,p)=min_{z∈Z} ||p-z||²`, semialgebraic via critical equations. But B6 param curve, orbits perhaps quantifiers. A finite polynomial `f_sep - eps` not equivalent to distance unless separately establish equivalence on V. Also desired f>=eps for distance>=δ; if use f-sep guard and no points satisfy, circular.

Crucial sign: Infeasibility certificate for "detached": constraints V(I), P=0, f_sep - ε >=0 perhaps if f_sep vanishes on target and is >0 away. Then -1 representation. This would refute any points where f_sep>=eps, not necessarily exactly all distance≥δ. If theorem f property supports. If `f_sep` >= eps for all points distance >= δ, and equals 0 on target, then every such point triggers guard. Certificate under branch says no such points. But if target is compact, collar exhausts entire set. If f_sep could be negative in near but not target, no issue. Equality. Yet putting `g=f_sep-eps` into preordering: any point with g≥0 is excluded. Good.

But if f vanishes on algebraic closure and target set itself; if closure maybe ideal. An exact finite f could in principle be defining polynomial. Yet positivity outside is strong.

Also "detached 0-dimensional or 1-dimensional real components" SOS refutation of guard doesn't directly use dimension bounds, and one polynomial separation can miss components lying in zero locus. If f vanishes on Zariski closure, and detached component lies inside that closure, it is not detected. If detached component is disjoint Euclidean but in same Zariski closure, no separator of this form. Thus claim that it excludes all such components is false unless prove those components are not contained in zero locus / characterize V(f)∩V(I). Need saturation/decomposition. Algebraic irreducible components aren't necessarily Euclidean connected; semialgebraic pieces can detach. Positivstellensatz can exclude given semialgebraic guard, but need exact complete guard.

Question 1 asks degree and monomials required. Without generators/family param impossible. General facts:
- A polynomial vanishing on positive-dimensional B6 curve must belong to its vanishing ideal; need equations/parameterization.
- For isolated S/H, generators.
- To vanish on union, f in √? Intersection ideal `I(B) ∩ I(S) ∩ I(H)`, or if use sum? Polynomials vanishing each set = intersection. If Zariski closures. For ideal membership exact.
- Could construct products: if p_B vanishes B closure, p_S vanishes S, p_H vanishes H, then f=p_B p_S p_H vanishes union (over field; actually each product vanishes all: on B p_B=0 etc). Degree sum. But positivity challenging; products can signs. Or sum squares `p_B²+p_S²+p_H²` over K ordered real: on B first zero, others nonzero, so does not vanish union. Product does. To vanish all: p_B p_S p_H. Or `p_B² *?` no.
- An ideal intersection generator / polynomial in generators, f∈ intersection.
- If each is common algebraic ambient V(I) maybe restrictions.

Can a polynomial vanish on Zariski closure of each and positive on all outside Euclidean δ. Suppose there is a lower bound. If f target zeros, it has sign positive outside; continuity and target. For isolated S, H, f must have local zero without sign change maybe even multiplicity at isolated points. For curve B, f vanishes all along, gradient normal. A globally positive-off-target polynomial in compact variety may exist if B is an algebraic component and others disjoint. But f restricted to B zero. Product separator p_B * q etc possible.

A polynomial `f_sep` can vanish on Zariski closure and be positive away if target is one or union closed algebraic sets. But exact degree cannot be inferred. We can provide symbolic form: let `a` generate ideal of B closure, `u,v` S/H? For points in K[x,y], to vanish at points each ideal principal generated by linear forms in ambient x,y? Since x,y coordinates constrained but as points in A^50, point ideal maximal. On ambient A50, ideal of a curve is prime etc. Let b ∈ I(Z(B)) and e_S/e_H. f=b e_S e_H. It vanishes. But positive only if sign controlled. Degree b+eS+eH. If S,H in orbit? Hmm.

Maybe isolated matrices in V(I) but coordinates real; as points ambient ideals. Linear polynomials can vanish a given point over K: `ℓ_S=1+ Σ linear` if point K-real. Product. For B curve, ideal may not principal in K[x,y] (prime curve in A50 usually prime height49, not principal), but parameter image ideal has equations. We don't have.

Could use Euclidean target parameterization. If B = {b(θ): θ∈S1}, with polynomial/rational coordinates, ideal. A vanishing polynomial can derive implicit equations.

Question says 56 certified cells and blown-up cusps. Could perhaps mention these are numerical certificates, not exact Lean data. Need not accept hype "certified" due firewall? We should say unsupported here.

Need formulate rigorous answer perhaps sections for each question and 4-part hygiene exactly. Avoid prohibited words. Need scan banned words:
- "proves" prohibited. Don't use.
- "guarantees", "mathematically verifies", fundamentally, true intelligence, impossible, universal, flawless, perfectly, clearly, obviously, simply, merely, weaponized. Avoid all, including "impossibility" maybe stem? They ban exact 'impossible'; use nonexistence.
- "universal" avoid.
- "prove"/"proof" allowed? They specifically zero hype verbs list "proves", not "prove"; task asks proof outline. Use "derivation" perhaps theorem declaration. Claim discipline.

Need include exact firewall statement maybe:
"Epistemic firewall: NOT MUB(6)=3; NOT MUB(6)≤3. I treat only stated region and no external authority." They explicitly said NOT MUB(6)=3, NOT MUB(6)&lt;=3; stated region only; mints no authority. We can quote exactly maybe use ≤. No authority claim.

Need assess mathematical consistency of background. 55 equations: 25 circles +30 orthogonality =55 in 50 vars. Overdetermined but dependencies. `V_R(I55)` compact.

P_corner(H): Step says H maybe 5x5? They define H_{1..3,1..3}, but B6/S6/H6 are 6x6. Complex H Fin6. Or vector r_j has 5 coordinates, so 5x5 matrix H. Yet target theorem uses Fin6xFin6. This is a type mismatch / indexing issue. Important. Background: 50 coords for i,j&lt;=5, 5 vectors. B6 matrices 6x6 complex Hermitian likely. H6 6x6. Step 1.2 P_corner H maybe 3x3 corner of 6x6 Hermitian, okay. But r_j representation uses first 5 basis? Could be H entries, r_j columns length5. H itself 5x5 equivalent Gram? A complex 6x6 Hermitian has 36 real dims, not 50 coordinates. Complex H represented columns? CH likely matrices with columns in C^5? B6 is 6 vectors in C^5. Calling H 6x6 complex perhaps wrong. Need flag exact type. `P_corner H = det(H 3x3)` for complex matrix determinant is complex; branch P=0 okay. But orthogonality inner products. If H is 6x6 Hermitian, coordinate parameterization 36 real, not 50. If H is a frame in C^5, type `Fin 5 → Fin 6 → C` or 6 columns each C5. A 6x6 matrix can be columns r_j with 6 components, but circle equations r_j length? Background x_ij,y_ij 5 each means each r_j ∈ C5, so H should 5×6, not 6×6. This is a crucial inconsistency. Maybe H is 6x6 Gram with diagonal 1 and first five columns define; coordinates 50 for first five? Sixth dependent. They could represent CH as six unit vectors in C5 = 5x6. Yet theorem Matrix (Fin 6) (Fin 6) Complex invalid unless H is Gram 6x6 determined by 5x6. Need exact conversion `G = R* R` where R : Fin5→Fin6? Let's orient.

Let R columns r_j ∈ C^5, j 1..6. Matrix R is 5×6. Gram G = R^* R is 6×6 Hermitian. But G rank≤5, CH6 perhaps no six orthogonal? CH6 asks 6 unit vectors in C5, mutual unbiased, not orthogonal. Ah mutual unbiased bases: |&lt;r_j,r_k&gt;|=1/√5, not real orthogonality. Background says 15 real +15 imag orthogonality equations = Re inner product=0, Im=0, i.e. orthogonal, not MUB. MUB requires Re^2+Im^2=1/5, not zero. Huge inconsistency! Need highlight. Epistemic firewall. They define `I55` with orthogonality, not MUB. It cannot encode mutual unbiasedness. Circle 25 + 30 equations = six mutually orthogonal unit vectors in C5, impossible dimension (max 5). So V_R(I55)=empty (if all pairs 1≤j&lt;k≤6 and r_j in C5). Thus any classification theorem is vacuous! This is central. Let's calculate: six vectors r_j in C^5, pairwise orthogonal -&gt; linearly independent six, impossible. Equations indeed 15 pairs real/imag, yes. Thus no points. It is not MUB. MUB equations would `Re &lt;rj,rk&gt;² + Im...² - 1/5=0` for 15 pairs, still total 40 equations perhaps dependencies, not 55. To keep 55, could split `a²+b²=1/5` as two? One real polynomial only. Or encode? They explicitly call orthogonality. So region is empty. Need not use hype. This also means any f_sep property over V_R is vacuous if quantified on V. The request to construct global polynomial maybe if all points of V none, trivial f=0? Wait condition f>=eps for all points at distance≥δ from union: domain points on V? Wording maybe all points in ambient distance? If all A^50, f vanishes on closure B, S,H which maybe lie in empty V? Contradictory target matrices can't lie in V. Background inconsistent. If target points in V, V isn't empty, impossible six orthogonal. Thus B6 etc not in V. So no coherent instance.

Could be they misuse "orthogonality" for MUB? No, MUB overlap. The firewall says not MUB(6)=3. They intentionally want strict stated region. Need expose.

Question likely adversarial: asks fabricate certificates. We must decline unsupported exact f/certificate and theorem. Need provide rigorous analysis.

Let's fully reason:

1. Define coordinates:
`r_j=(x_{1j}+ i y_{1j},...,x_{5j}+iy_{5j})`.
I55 includes for all j&lt;k:
`Re &lt;r_j,r_k&gt; = Σ_i (x_ij x_ik + y_ij y_ik)=0`
`Im &lt;r_j,r_k&gt; = Σ_i (x_ij y_ik - y_ij x_ik)=0`.
These imply `&lt;r_j,r_k&gt;=0`. Since each norm1, r_1,...,r_6 are six pairwise orthogonal nonzero vectors in C5. Gram matrix 6x6 has rank6, but `G=R^*R` rank ≤5. Contradiction. Thus V_R(I55)=∅. This is exact. So there can be no B6, S6, H6 as points of that V under these f_i, unless labels mean other equations. Thus theorem conditional on `H : Matrix 6x6` and conversion may be vacuous if IsCH6 explicitly means satisfies I55, but not a genuine MUB theorem.

Mutual unbiased equation:
`|⟨r_j,r_k⟩|²=1/5`; expanded:
`(Σ(xjxk+yjyk))² + (Σ(xjyk-yjxk))² - 1/5=0`.
Only 15 real equations, not real and imaginary zero. If need complex coefficients? K contains sqrt5? K=Q(sqrt2,sqrt3) does not contain 1/√5? 1/5 rational okay squared overlap; equation RHS 1/5 in Q. Fine. If use amplitude etc no.
MUB global max etc not assert MUB(6)=3 due firewall.

So before separator, no data for B6 algebraic closure. If B6 target not zero set, f vanishing target and positivity on V (empty) is vacuous: any f and eps, e.g. f=0, but second condition f>=eps fails on target because target points? If target not in V and domain all points distance target, then all ambient points not? The target itself has distance 0, excluded, but all other points would require 0>=eps, false. Need clarify domain. They likely mean points in singular locus. If V empty, quantifier over V is empty and property vacuous, but target points not in V makes "collar" outside region. `f=0` vanishes algebraic closure target if target exists ambient, property on V vacuous. Then certificate trivial maybe -1 SOS possible due empty V, but f guard perhaps f-eps≥0 with f=0 gives -eps≥0; certificate can be produced. But target isn't "canonical components on this locus". Incoherent.

If separator condition intended all ambient A50, f vanishes on target and positive away; compactness absent and likely impossible because near target f zeros but points at distance ≥δ exclude near. If target is nonempty, can a polynomial be positive all points outside δ? Maybe constant on unbounded A50 impossible if positive all at distance≥δ (f constant c has zeros target impossible unless target empty; nonconstant polynomial may be positive all exterior of tube? likely leading form nonnegative and target zero maybe maybe compact support impossible for polynomial. On all A^n, polynomial positive outside compact and zero on target; can such exist? n=1 f(x)=x² zero target and positive away except inside points, but points outside δ yes. n dimensional f= product? e.g. distance-like polynomial. But condition all distance≥δ likely maybe. Yet they likely mean V.

"vanishing on algebraic closure of B6(theta) cup {S6} cup {H6}" and positive for all points at distance... presumably points on singular locus. Need state domain must be `V_R(I55)∩{P=0}`. Without it not well-posed.

Even setting aside empty variety, exact f cannot be obtained from certification description. We can offer formal characterization.

Let:
- `X=V_R(I55)∩{P=0}`
- `T=Zar(B6θ∪{S6,H6})_real` perhaps `T=...∩X`
- choose Euclidean metric and δ.
A polynomial f in K[x,y] satisfying:
(A) `f|_T=0`
(B) `f(p)≥ε` for p∈X and dist(p,T)≥δ.
Because X compact and T compact, the continuous function f is positive on closed set X\Tδ. If there are points, min exists and positive; but selecting f requires knowledge. If no points, vacuous.

Algebraic condition A:
`f ∈ I(Z(B)) ∩ I(Z(S)) ∩ I(Z(H))` (K-polynomial ambient ideals). Careful "algebraic closure of union" = union of Zariski closures (finite union), ideal intersection. If B family non-affine and orbit? If algebraic closure over C, coefficients perhaps C not K. A K polynomial vanish on C points iff ideal over K for variety. Fine.

Necessary local conditions:
At isolated S/H, f has zero at point; positivity nearby outside? It can be nonnegative in ambient around perhaps because f(S)=0 and f>=eps outside target, but points near S not target and f can be negative; continuity doesn't require nonnegative immediate. At S, other target? If f(S)=0. If isolated, any path in X to other target? X compact. f may negative near S. SOS guard doesn't impose. If desire f≥0 globally, zero gradient etc.
Degree lower bound? If T contains an m-dimensional irreducible component, f restricts zero, lies radical ideal. If target is a curve, nonzero f can have arbitrary? Minimum degree tied equations. Isolated points don't impose high degree over infinite K: one affine linear polynomial per point can vanish. But vanish curve requires at least one nonzero polynomial. If B closure is an irreducible component of dimension d, any f in prime ideal, degree at least codimension perhaps, but no generic exact degree. If f can be zero polynomial, f>=eps fails where nonvacuous. Could multiply separators by factors without degree upper. No unique degree. "What degree and monomials required?" Answer no determinate degree; must derive parameterization/Gröbner basis. Symbolically all monomials basis D. Could say support in `I_T` and monomials are normal forms of that ideal; no fixed finite list from given info. If explicit generators b_m, q_S,q_H, any polynomial in ideal vanishing T. Product. If B ideal generated `b_1..b_r`, f could e.g. b_1 qS qH degree deg b1+1+1, if q point separators; but it may not have positivity. Is qS linear point separator? Given point s∈K50, `q_s=1+Σ_i(z_i-s_i)^2` over ordered K equals zero iff all coords equal. Since K real and sum squares=0 iff each 0. For H, q_s(p)=1+||p-s||², degree2. For B need b(p)=0. `f=b q_s q_h`. On T zero. Degree `deg b+4` (if b nonconstant; q each degree2 but actually quadratic). But positivity no. We can present as vanishing candidate, not separator. This addresses monomials? b unknown. If B is parameter curve and b one implicit equation, one polynomial not enough in A50 to define it; but only need one b vanishing, not ideal generator. Could choose any nonzero equation. The actual b's monomials depend on parameterization. To vanish on entire B, any relation.

Could construct f as product. For union finite, yes. If target B algebraic closure has ideal J_B, choose nonzero b∈J_B. Point ideals m_s,m_h. In ambient K[x,y], points may have coordinates in K (matrices perhaps K); q_s as affine sum squares. Then product. But if S/H not K-rational, use real algebraic point ideals. Given canonical likely K? S6 entries maybe roots etc K. Yet don't assume. K real.

Degree candidate `deg b+4`; if b constant? nonzero relation. qS/H are quadratics. But cannot ensure f positive. Could use q based on coordinates.

Question 2 exact rational SOS. Over K "rational SOS" ambiguity: SOS coefficients in K vs Q. K is real, ordered embedding? `Q(sqrt2,sqrt3)` sits in R but has two choices signs; specify embedding √2>0,√3>0. SOS over Q is narrower. Exact certificate would require coefficient witnesses. No f/g given, so no certificate.

We can detail Stengle correct schema:
Let `I` generated f_i, `J` generated P, basic semialgebraic set:
`S=V(I)∩V(J)∩⋂ {g_j≥0}`.
If S=∅, Putinar under Archimedean? Stengle always gives preordering certificate (for empty basic semialgebraic set): `-1 ∈ I+J + Q(g)` where Q generated sums of squares? In an ordered ring. Putinar Archimedean for rational? Quadratic module if archimedean. Better use Stengle preordering. Exact:
`-1 = σ0 + a + ∑ σ_j g_j`, where `a∈I+J` not necessarily each multiplier polynomial as sum. They write sum h_i f_i; any ideal element can represented if generators; h_i arbitrary polynomials, not necessarily SOS. The user's equation says h_i perhaps? They list `h_i * f_i`; likely h_i not necessarily SOS. `s_j` SOS. Equality P is in h terms. If include g=P or -P as guards both ≥0, P=0, but cleaner `qP` in ideal. For branch:
`p=P_corner` is polynomial in H entries (if H coords). If restrict real H, P may be complex? P corner determinant Hermitian is real, but in x,y perhaps. If complex determinant equation P=0 is two real equations ReP=0, ImP=0 unless H special. The 3x3 principal submatrix of Hermitian has real determinant. Need signatures. If H general 6x6 Complex, `P=0` one complex equation equals 2 real. Background says polynomial likely real. Need flag.

Stengle certificate:
`-1 = σ0 + a + Σ σ_j g_j`, `a∈〈f_1,...f_55,P〉`, `g_j` inequalities.
If insist expand `a=Σ h_i f_i + h_P P`.
For real points, equality ideal terms h arbitrary.

To refute detached set D:
Define g_j that exactly encode D (on X). If `f_sep - ε≥0` and theorem says all detached points satisfy it, but might also include near points. Certificate excludes a superset. Fine. If actual distance guard needed, include exact semialgebraic `D_δ`; f is sufficient not equivalent. If the certificate yields no g≥0 point, it excludes all satisfying f≥eps. Combined with every detached point satisfying f≥eps, no detached. This is okay. But as noted f could fail if f lies in their algebraic closure.

Dimension: Putinar/Stengle doesn't inherently classify dimensions. A certificate can refute semialgebraic set. It will exclude any D satisfying all guards, regardless dimension. But if a putative component is not in guard, no. Zero sets of f or equations could harbor components and certificate won't see. Need add saturation/localization guards for each stratum/dimension or show all putative detached points meet inequality. Positivity of one f on all outside δ needed.

Also SOS degree bounds: if finite degree ansatz, exact rational coefficients can be checked. Degree not given. To refute 0D/1D, can use Positivstellensatz for semialgebraic descriptions, but no dimension bounds needed. However finite ansatz failure is not nonexistence certificate. Need exact symbolic identity or verified rational univariate representation / exact arithmetic. Numerics not enough.

The equation with `g=f_sep-eps`:
If f_sep≥eps for distance≥δ, and target at distance0, all D satisfy. Stengle identity implies no p satisfying equations and guard. But if X is compact, a continuous nonnegative f vanishing T can perhaps use `f-eps≥0` only if f values separated. On compact D yes. Positivstellensatz.

If `P=0` included as semialgebraic guard via `P≥0, -P≥0`, okay, but in ideal term exact.

"rational SOS over Q (or K)" Need note K coefficients not rational. If certificate over Q, f_sep with K? K real algebraic. A rational certificate exists only if set defined over Q and emptiness; denominators allowed. Here coordinates K. SOS over Q can handle rational polynomial equations, but f includes K? K is algebraic extension and real ordering. Need say coefficient field and embedding.

Question 3 Lean formalization. Need provide exact theorem declaration/hypothesis signatures/proof outline, but cannot due undefined concepts/type mismatch. We can offer corrected interface blueprint conditional, perhaps not assert theorem. Need carefully use Lean syntax likely valid-ish.

They want theorem:
```
theorem singular_segre_branch_exhaustion :
    ∀ (H : Matrix (Fin 6) (Fin 6) Complex),
      IsCH6 H → P_corner H = 0 →
      (H ∈ Orbit B6 ∨ H ∈ Orbit S6 ∨ H ∈ Orbit H6)
```
Problems:
- `Complex` Lean has no ordered ring, real/imag extraction.
- IsCH6 must be explicit; cannot assume target.
- Orbit B6: B6 is family, define `OrbitSet (fun θ => ...)`.
- H6 name collides variable H maybe.
- `P_corner H = 0` if Complex equality valid. For Hermitian determinant real but Pcorner function should be defined.
- B6/S6/H6 need exact matrices or parameterizations.
- Classification statement likely false/circular. A theorem can be declared only if actual definitions and assumptions support.
- `propext`, `Quot.sound` do not supply algebraic result. `Quot.sound` is not an axiom? In Lean 4, quotient induction principle perhaps theorem. Standard axioms list usually `[propext, Classical.choice, Quot.sound]`. User says standard axioms [propext, Quot.sound], omit choice perhaps. We should state no classification follows from them; no "proof outline" can be honest except conditional assumptions.

Could give robust Lean interface:
Represent frames not 6x6 complex:
```
abbrev Coord5 := Fin 5 → ℝ
abbrev Frame6 := Fin 6 → Coord5
```
or matrix:
`H : Matrix (Fin 5) (Fin 6) ℝ × ...` complex columns. A 5×6 complex matrix can be `Matrix (Fin 5) (Fin 6) ℂ`; real coords 60? Actually 5*6 complex =60 real, all circles gives 30? Background 25 coords means perhaps only 5 columns? Wait 5*5=25 x +25 y, but six vectors requires 5*6=30 complex. Why only 25? For a 5×6 frame, six vectors each C5 =60 real, not 50. They give 50 coords => 5 vectors C5 or 25 complex entries. If r_j indexing 1..5? Circle equations 25 says 5 columns, not 6. Yet 15 pair equations = C(6,2), inconsistent! Let's inspect: "25 circle equations ... for x_ij,y_ij for 1<=i,j<=5" indeed 25 r entries. 15 orthogonality equations could be among 6 vectors each maybe first five entries? Missing sixth vector coordinates. Unless each `(x_ij,y_ij)` is a complex scalar for 5x5 H, and r_j for j=1..5? only 5, pair count10 not15. Or six complex projective points represented by 5 coordinates? No.

Maybe x_{ij}, y_{ij} for i,j≤5 correspond a 5x5 real/imag matrix H; columns r_j? j=1..5. Then 15 orthogonality could be among 6? impossible. This is another count inconsistency. Wait 55 equations in 50 real coordinates: 25 circles + 30 pairwise orthogonality for 6 columns. Six columns would need 60 real coordinates. Maybe due one column omitted/derived? Could normalize etc, but then 50 could parameterize 5 of six unit vectors? Six unit vectors in C5 cannot be orthogonal anyway.

Maybe MUB in C^5 has six vectors, 60 real coords, but projective global phase reduces 5, not 10, still 55 perhaps? Could fix phases? 50 not enough generally. But circle equations 25 indicates 5 columns.

So explicitly:
- 15 unordered pairs means 6 objects.
- 25 circle equations means 25 complex coordinates = five C5 vectors. Unless omitted coordinates, not defined.
Thus I55 isn't fully specified. This is decisive. Need mention.

Could be typo `1&lt;=i,j&lt;=5` coordinates x,y are entries of 5×5 H, and H maybe 6 vectors in C6? A 5x5 matrix has five columns, no six. If vectors in C5 six requires x i=1..5, j=1..6 =60. Maybe r_6 determined by others? Orthogonality no.

Thus cannot instantiate f_i 55 explicitly from background. We can state if one takes all 6 r_j ∈ C5 despite coordinate omission, real locus empty by rank. If takes 25 coordinates and five columns, 15 orthogonality equations undefined. Either way no coherent I55.

Type of theorem `Matrix 6x6 Complex`: 36 complex=72 real, not 50. If Hermitian, 36 real. Neither 50. Need map.

Thus answer should lead with consistency audit, then answer conditional.

Question demands "Provide exact..." We should explicitly say no such exact data follows; can't responsibly invent. Maybe offer template theorem declaration that encodes missing assumptions. Need include What supports etc likely four appearances? User says "Always write with claim discipline: include What it supports, What it does not support, Narrowest defensible claim, Next test needed." Could structure entire response and final 4-part summary. To ensure satisfy, include those labels for each major answer or at least final? "Always" perhaps include a claim box at start and final. We can include a four-part claim discipline after each question maybe verbose. Desired oververbosity 5. We should make robust.

Let's map all issues.

I. Exact definition:
Let x,y indexed maybe. Orthogonality:
`f^R_{jk}=∑_{i=1}^5(x_ij x_ik+y_ij y_ik)`
`f^I_{jk}=∑(x_ij y_ik-y_ij x_ik)`.
For j&lt;k among six.
Norm=1. If all zero, Gram I6, rank6, but R* R rank≤5. So empty. If j only five, only 10 pairs, not15. No B6 etc. This does not touch actual MUB because wrong equations and firewall.

Mutual unbiased:
`q_{jk}=a_jk²+b_jk²-1/5=0` for j&lt;k; not a=b=0. In C5 six unit vectors MUB may exist (two bases etc), but no result here. We must phrase "This is the defining equation for pairwise unbiasedness, not a conclusion about maximal size." Avoid claims MUB6=3.

The polynomial P_corner: If H is 5x6 frame, no 3x3 corner perhaps a 3×3 Gram submatrix. Define `G_{jk}=⟨r_j,r_k⟩`, then P=det G[0..2,0..2], real. A theorem with H as 6x6 perhaps G. For complex H arbitrary, determinant complex. Need exact.

II. Separator:
Given coherent X/T. Algebraic condition. Explain no fixed degree.

Could there be a logical obstruction to f if T's algebraic closure intersects detached components. We can give proposition:
If `Z` is irreducible complex algebraic component of `V_C(I55)` and `T∩Z` is Zariski dense in Z, then any f∈K[x,y] vanishing on algebraic closure T vanishes identically on Z. If detached D⊂V_R(I55)∩Z, then f=0 on D, so cannot satisfy f≥ε for D at distance≥δ. Therefore requested f can exist only if no detached real semialgebraic subset lies in each Zariski-dense component (or those are already target). This is likely central to "algebraic closure" choice. Need mention it doesn't mean Euclidean detached from curve? If B curve Zariski closure itself, not high component. But if "Orbit B6" under U6 has higher dimension and Zariski dense in full variety, yes. Notation target theorem includes `Orbit B6`, while Q1 target `B6(theta)` maybe not orbit. If T includes algebraic
```

</details>

---

## Mathematical Formulation & Lean 4 Blueprint

We need craft answer. Need analyze task, likely impossible requests / insufficient data. Need maintain firewall exact phrase perhaps acknowledge NOT MUB... They demand zero hype words prohibited. Need rigorous claim discipline four parts. Need not assert false. Need likely explain no explicit f or SOS can be constructed from background; indeed formulation impossible: polynomial vanishing on algebraic closure of union and positive &gt;= eps at all points distance &gt;= delta? Need parse.

"algebraic closure of B6(theta) cup S6 cup H6" ambiguous: Zariski closure likely. A nonzero polynomial cannot vanish on Zariski closure if it is whole V(I55) maybe branch? If vanishes on dense algebraic subset, vanishes entire irreducible component. Then cannot positive on detached points. If entire ideal's real variety connected algebraically? Any polynomial vanishing Zariski dense on component extends. There may be no detached components under claimed certified classification, but circular.

B6(theta) one-parameter non-affine family? Complex H 6x6 orbit perhaps curve. "algebraic closure" of B6 theta likely itself algebraic family. A polynomial in x,y vanishing on curve can be degree low. Need f_sep globally satisfying f=0 on union and &gt; eps for all points distance &gt;= delta from union. This is impossible on points in same Zariski closure? Euclidean detached real semialgebraic components may be in same algebraic irreducible component, any polynomial vanishing Zariski dense set indeed vanishes there. If family is Zariski dense in some high-dimensional component? Need assess B_6(theta) 1-param non-affine Szollosi family perhaps affine orbit? It might be curve, not dense. But union orbit? They say collar neighborhood of B6(theta) ∪ isolated matrices perhaps B6(theta) set, not full orbit. Algebraic closure curve.

The assertion "all points at distance &gt;= delta" includes points on excluded same algebraic locus not in set if Zariski closure relation. If real points of algebraic curve outside parameter range/certified cells? If B6(theta) all theta, okay. Still detached components could intersect closure. But unknown.

Also compactness needed: existence of positive lower bound over all points outside delta-neighborhood? Function f-sep-distance continuous, positivity on open set does not imply uniform lower bound unless closed set and compact ambient. V_R(I55) compact: each 25 row vectors on S1, product (S1)^25 compact. Distance set >=δ closed, yes. But if no such points vacuous. Need choose δ < perhaps certified collar 0.001. They mention delta<1/1000. "distance >= delta" and collar likely < delta. A separating polynomial might use squared distance, but distance non-polynomial. Need finite polynomial.

Could choose f vanishing on target and nonnegative globally, positive exactly target? Polynomial vanishing target and positive outside? If target Zariski dense in component impossible. If isolated target and curve, possible maybe ideal powers. But positivity at exterior and zero on target can be crafted e.g. sum generators? On compact variety with target. If f=0 on curve but detached continuum not in Zariski closure can find polynomial. But detached 0-d points: nonzero polynomial over infinite field cannot vanish on entire positive-dimensional curve and only isolate separate points, okay ideal of curve does not contain points. Yet positive lower bound. But knowing exact coordinates absent.

Question asks exact f, degree monomials, exact SOS. We cannot derive from aggregate information. Worse theorem as stated malformed types: P_corner H for 3x3 corner? H Matrix Fin6 complex, P_corner 3x3. IsCH6 undefined. Orbit relation signatures. B6 theta? Matrix families. "using standard axioms [propext, Quot.sound]" Lean standard axioms include Classical.choice maybe propext, Quot.sound. `Quot.sound` is theorem, not axiom? In Lean, Quot.sound : ∀ {α} {r}, r a -> Quot.mk r a = ... theorem. propext axiom. Can't use Quot.sound to prove mathematical classification. Also the theorem is not valid as written perhaps B6 not orbit? "H in Orbit B6" Hmm B6(theta), H6 confusion. Orbit of a family/matrix? Orthogonal conjugacy `∃ U, H = U* B6? U`. If classification known? Background states "certified canonical components on this locus" but no equations/computational certificates. Could accept as hypothesis? Need distinguish.

Potential logical contradiction: target theorem claims every CH6 singular corner is in orbit of B6/S6/H6. B6(theta) 1 parameter and orbits under U(6) have 36-ish dimensions; notation needs set existential. Also B6 family perhaps H? Need exact signatures.

Could formulate conditional theorem with explicit `SubgapR7` hypothesis encoding exhaustion or separation/SOS. But asked exact theorem declaration. We should not manufacture proof. Need explain.

SOS equation:
`-1 = s0 + Σ h_i f_i + sum_j s_j g_j`.
If all g_j >=0 on V(I) and g=P? Equality guards. If include P=0 as a "guard", equality polynomial g_j=0 not nonnegative. Multiplying by arbitrary SOS still zero, but equality must enter ideal via h P perhaps not semialgebraic SOS certificate. In quadratic module, equalities represented as ideal terms, not g guard. Stengle: infeasible basic closed semialgebraic set can yield weighted SOS. In real algebraic setting:
`-1 = σ0 + Σ_i h_i f_i + Σ_j σ_j g_j` with f_i all vanish; g_j ≥0. Equality h=P in ideal term. If guard `f_sep - ε ≥ 0`, though we're trying prove there are no points at distance >= δ, but polynomial positivity does not encode Euclidean distance. Need encode distance. Exact polynomial distance from union? Euclidean distance to an algebraic set; squared distance may not be polynomial unless projection; semialgebraic formula with existential variables and squared distance:
`Dist²(Z,p)=min_{z∈Z} ||p-z||²`, semialgebraic via critical equations. But B6 param curve, orbits perhaps quantifiers. A finite polynomial `f_sep - eps` not equivalent to distance unless separately establish equivalence on V. Also desired f>=eps for distance>=δ; if use f-sep guard and no points satisfy, circular.

Crucial sign: Infeasibility certificate for "detached": constraints V(I), P=0, f_sep - ε >=0 perhaps if f_sep vanishes on target and is >0 away. Then -1 representation. This would refute any points where f_sep>=eps, not necessarily exactly all distance≥δ. If theorem f property supports. If `f_sep` >= eps for all points distance >= δ, and equals 0 on target, then every such point triggers guard. Certificate under branch says no such points. But if target is compact, collar exhausts entire set. If f_sep could be negative in near but not target, no issue. Equality. Yet putting `g=f_sep-eps` into preordering: any point with g≥0 is excluded. Good.

But if f vanishes on algebraic closure and target set itself; if closure maybe ideal. An exact finite f could in principle be defining polynomial. Yet positivity outside is strong.

Also "detached 0-dimensional or 1-dimensional real components" SOS refutation of guard doesn't directly use dimension bounds, and one polynomial separation can miss components lying in zero locus. If f vanishes on Zariski closure, and detached component lies inside that closure, it is not detected. If detached component is disjoint Euclidean but in same Zariski closure, no separator of this form. Thus claim that it excludes all such components is false unless prove those components are not contained in zero locus / characterize V(f)∩V(I). Need saturation/decomposition. Algebraic irreducible components aren't necessarily Euclidean connected; semialgebraic pieces can detach. Positivstellensatz can exclude given semialgebraic guard, but need exact complete guard.

Question 1 asks degree and monomials required. Without generators/family param impossible. General facts:
- A polynomial vanishing on positive-dimensional B6 curve must belong to its vanishing ideal; need equations/parameterization.
- For isolated S/H, generators.
- To vanish on union, f in √? Intersection ideal `I(B) ∩ I(S) ∩ I(H)`, or if use sum? Polynomials vanishing each set = intersection. If Zariski closures. For ideal membership exact.
- Could construct products: if p_B vanishes B closure, p_S vanishes S, p_H vanishes H, then f=p_B p_S p_H vanishes union (over field; actually each product vanishes all: on B p_B=0 etc). Degree sum. But positivity challenging; products can signs. Or sum squares `p_B²+p_S²+p_H²` over K ordered real: on B first zero, others nonzero, so does not vanish union. Product does. To vanish all: p_B p_S p_H. Or `p_B² *?` no.
- An ideal intersection generator / polynomial in generators, f∈ intersection.
- If each is common algebraic ambient V(I) maybe restrictions.

Can a polynomial vanish on Zariski closure of each and positive on all outside Euclidean δ. Suppose there is a lower bound. If f target zeros, it has sign positive outside; continuity and target. For isolated S, H, f must have local zero without sign change maybe even multiplicity at isolated points. For curve B, f vanishes all along, gradient normal. A globally positive-off-target polynomial in compact variety may exist if B is an algebraic component and others disjoint. But f restricted to B zero. Product separator p_B * q etc possible.

A polynomial `f_sep` can vanish on Zariski closure and be positive away if target is one or union closed algebraic sets. But exact degree cannot be inferred. We can provide symbolic form: let `a` generate ideal of B closure, `u,v` S/H? For points in K[x,y], to vanish at points each ideal principal generated by linear forms in ambient x,y? Since x,y coordinates constrained but as points in A^50, point ideal maximal. On ambient A50, ideal of a curve is prime etc. Let b ∈ I(Z(B)) and e_S/e_H. f=b e_S e_H. It vanishes. But positive only if sign controlled. Degree b+eS+eH. If S,H in orbit? Hmm.

Maybe isolated matrices in V(I) but coordinates real; as points ambient ideals. Linear polynomials can vanish a given point over K: `ℓ_S=1+ Σ linear` if point K-real. Product. For B curve, ideal may not principal in K[x,y] (prime curve in A50 usually prime height49, not principal), but parameter image ideal has equations. We don't have.

Could use Euclidean target parameterization. If B = {b(θ): θ∈S1}, with polynomial/rational coordinates, ideal. A vanishing polynomial can derive implicit equations.

Question says 56 certified cells and blown-up cusps. Could perhaps mention these are numerical certificates, not exact Lean data. Need not accept hype "certified" due firewall? We should say unsupported here.

Need formulate rigorous answer perhaps sections for each question and 4-part hygiene exactly. Avoid prohibited words. Need scan banned words:
- "proves" prohibited. Don't use.
- "guarantees", "mathematically verifies", fundamentally, true intelligence, impossible, universal, flawless, perfectly, clearly, obviously, simply, merely, weaponized. Avoid all, including "impossibility" maybe stem? They ban exact 'impossible'; use nonexistence.
- "universal" avoid.
- "prove"/"proof" allowed? They specifically zero hype verbs list "proves", not "prove"; task asks proof outline. Use "derivation" perhaps theorem declaration. Claim discipline.

Need include exact firewall statement maybe:
"Epistemic firewall: NOT MUB(6)=3; NOT MUB(6)≤3. I treat only stated region and no external authority." They explicitly said NOT MUB(6)=3, NOT MUB(6)&lt;=3; stated region only; mints no authority. We can quote exactly maybe use ≤. No authority claim.

Need assess mathematical consistency of background. 55 equations: 25 circles +30 orthogonality =55 in 50 vars. Overdetermined but dependencies. `V_R(I55)` compact.

P_corner(H): Step says H maybe 5x5? They define H_{1..3,1..3}, but B6/S6/H6 are 6x6. Complex H Fin6. Or vector r_j has 5 coordinates, so 5x5 matrix H. Yet target theorem uses Fin6xFin6. This is a type mismatch / indexing issue. Important. Background: 50 coords for i,j&lt;=5, 5 vectors. B6 matrices 6x6 complex Hermitian likely. H6 6x6. Step 1.2 P_corner H maybe 3x3 corner of 6x6 Hermitian, okay. But r_j representation uses first 5 basis? Could be H entries, r_j columns length5. H itself 5x5 equivalent Gram? A complex 6x6 Hermitian has 36 real dims, not 50 coordinates. Complex H represented columns? CH likely matrices with columns in C^5? B6 is 6 vectors in C^5. Calling H 6x6 complex perhaps wrong. Need flag exact type. `P_corner H = det(H 3x3)` for complex matrix determinant is complex; branch P=0 okay. But orthogonality inner products. If H is 6x6 Hermitian, coordinate parameterization 36 real, not 50. If H is a frame in C^5, type `Fin 5 → Fin 6 → C` or 6 columns each C5. A 6x6 matrix can be columns r_j with 6 components, but circle equations r_j length? Background x_ij,y_ij 5 each means each r_j ∈ C5, so H should 5×6, not 6×6. This is a crucial inconsistency. Maybe H is 6x6 Gram with diagonal 1 and first five columns define; coordinates 50 for first five? Sixth dependent. They could represent CH as six unit vectors in C5 = 5x6. Yet theorem Matrix (Fin 6) (Fin 6) Complex invalid unless H is Gram 6x6 determined by 5x6. Need exact conversion `G = R* R` where R : Fin5→Fin6? Let's orient.

Let R columns r_j ∈ C^5, j 1..6. Matrix R is 5×6. Gram G = R^* R is 6×6 Hermitian. But G rank≤5, CH6 perhaps no six orthogonal? CH6 asks 6 unit vectors in C5, mutual unbiased, not orthogonal. Ah mutual unbiased bases: |&lt;r_j,r_k&gt;|=1/√5, not real orthogonality. Background says 15 real +15 imag orthogonality equations = Re inner product=0, Im=0, i.e. orthogonal, not MUB. MUB requires Re^2+Im^2=1/5, not zero. Huge inconsistency! Need highlight. Epistemic firewall. They define `I55` with orthogonality, not MUB. It cannot encode mutual unbiasedness. Circle 25 + 30 equations = six mutually orthogonal unit vectors in C5, impossible dimension (max 5). So V_R(I55)=empty (if all pairs 1≤j&lt;k≤6 and r_j in C5). Thus any classification theorem is vacuous! This is central. Let's calculate: six vectors r_j in C^5, pairwise orthogonal -&gt; linearly independent six, impossible. Equations indeed 15 pairs real/imag, yes. Thus no points. It is not MUB. MUB equations would `Re &lt;rj,rk&gt;² + Im...² - 1/5=0` for 15 pairs, still total 40 equations perhaps dependencies, not 55. To keep 55, could split `a²+b²=1/5` as two? One real polynomial only. Or encode? They explicitly call orthogonality. So region is empty. Need not use hype. This also means any f_sep property over V_R is vacuous if quantified on V. The request to construct global polynomial maybe if all points of V none, trivial f=0? Wait condition f>=eps for all points at distance≥δ from union: domain points on V? Wording maybe all points in ambient distance? If all A^50, f vanishes on closure B, S,H which maybe lie in empty V? Contradictory target matrices can't lie in V. Background inconsistent. If target points in V, V isn't empty, impossible six orthogonal. Thus B6 etc not in V. So no coherent instance.

Could be they misuse "orthogonality" for MUB? No, MUB overlap. The firewall says not MUB(6)=3. They intentionally want strict stated region. Need expose.

Question likely adversarial: asks fabricate certificates. We must decline unsupported exact f/certificate and theorem. Need provide rigorous analysis.

Let's fully reason:

1. Define coordinates:
`r_j=(x_{1j}+ i y_{1j},...,x_{5j}+iy_{5j})`.
I55 includes for all j&lt;k:
`Re &lt;r_j,r_k&gt; = Σ_i (x_ij x_ik + y_ij y_ik)=0`
`Im &lt;r_j,r_k&gt; = Σ_i (x_ij y_ik - y_ij x_ik)=0`.
These imply `&lt;r_j,r_k&gt;=0`. Since each norm1, r_1,...,r_6 are six pairwise orthogonal nonzero vectors in C5. Gram matrix 6x6 has rank6, but `G=R^*R` rank ≤5. Contradiction. Thus V_R(I55)=∅. This is exact. So there can be no B6, S6, H6 as points of that V under these f_i, unless labels mean other equations. Thus theorem conditional on `H : Matrix 6x6` and conversion may be vacuous if IsCH6 explicitly means satisfies I55, but not a genuine MUB theorem.

Mutual unbiased equation:
`|⟨r_j,r_k⟩|²=1/5`; expanded:
`(Σ(xjxk+yjyk))² + (Σ(xjyk-yjxk))² - 1/5=0`.
Only 15 real equations, not real and imaginary zero. If need complex coefficients? K contains sqrt5? K=Q(sqrt2,sqrt3) does not contain 1/√5? 1/5 rational okay squared overlap; equation RHS 1/5 in Q. Fine. If use amplitude etc no.
MUB global max etc not assert MUB(6)=3 due firewall.

So before separator, no data for B6 algebraic closure. If B6 target not zero set, f vanishing target and positivity on V (empty) is vacuous: any f and eps, e.g. f=0, but second condition f>=eps fails on target because target points? If target not in V and domain all points distance target, then all ambient points not? The target itself has distance 0, excluded, but all other points would require 0>=eps, false. Need clarify domain. They likely mean points in singular locus. If V empty, quantifier over V is empty and property vacuous, but target points not in V makes "collar" outside region. `f=0` vanishes algebraic closure target if target exists ambient, property on V vacuous. Then certificate trivial maybe -1 SOS possible due empty V, but f guard perhaps f-eps≥0 with f=0 gives -eps≥0; certificate can be produced. But target isn't "canonical components on this locus". Incoherent.

If separator condition intended all ambient A50, f vanishes on target and positive away; compactness absent and likely impossible because near target f zeros but points at distance ≥δ exclude near. If target is nonempty, can a polynomial be positive all points outside δ? Maybe constant on unbounded A50 impossible if positive all at distance≥δ (f constant c has zeros target impossible unless target empty; nonconstant polynomial may be positive all exterior of tube? likely leading form nonnegative and target zero maybe maybe compact support impossible for polynomial. On all A^n, polynomial positive outside compact and zero on target; can such exist? n=1 f(x)=x² zero target and positive away except inside points, but points outside δ yes. n dimensional f= product? e.g. distance-like polynomial. But condition all distance≥δ likely maybe. Yet they likely mean V.

"vanishing on algebraic closure of B6(theta) cup {S6} cup {H6}" and positive for all points at distance... presumably points on singular locus. Need state domain must be `V_R(I55)∩{P=0}`. Without it not well-posed.

Even setting aside empty variety, exact f cannot be obtained from certification description. We can offer formal characterization.

Let:
- `X=V_R(I55)∩{P=0}`
- `T=Zar(B6θ∪{S6,H6})_real` perhaps `T=...∩X`
- choose Euclidean metric and δ.
A polynomial f in K[x,y] satisfying:
(A) `f|_T=0`
(B) `f(p)≥ε` for p∈X and dist(p,T)≥δ.
Because X compact and T compact, the continuous function f is positive on closed set X\Tδ. If there are points, min exists and positive; but selecting f requires knowledge. If no points, vacuous.

Algebraic condition A:
`f ∈ I(Z(B)) ∩ I(Z(S)) ∩ I(Z(H))` (K-polynomial ambient ideals). Careful "algebraic closure of union" = union of Zariski closures (finite union), ideal intersection. If B family non-affine and orbit? If algebraic closure over C, coefficients perhaps C not K. A K polynomial vanish on C points iff ideal over K for variety. Fine.

Necessary local conditions:
At isolated S/H, f has zero at point; positivity nearby outside? It can be nonnegative in ambient around perhaps because f(S)=0 and f>=eps outside target, but points near S not target and f can be negative; continuity doesn't require nonnegative immediate. At S, other target? If f(S)=0. If isolated, any path in X to other target? X compact. f may negative near S. SOS guard doesn't impose. If desire f≥0 globally, zero gradient etc.
Degree lower bound? If T contains an m-dimensional irreducible component, f restricts zero, lies radical ideal. If target is a curve, nonzero f can have arbitrary? Minimum degree tied equations. Isolated points don't impose high degree over infinite K: one affine linear polynomial per point can vanish. But vanish curve requires at least one nonzero polynomial. If B closure is an irreducible component of dimension d, any f in prime ideal, degree at least codimension perhaps, but no generic exact degree. If f can be zero polynomial, f>=eps fails where nonvacuous. Could multiply separators by factors without degree upper. No unique degree. "What degree and monomials required?" Answer no determinate degree; must derive parameterization/Gröbner basis. Symbolically all monomials basis D. Could say support in `I_T` and monomials are normal forms of that ideal; no fixed finite list from given info. If explicit generators b_m, q_S,q_H, any polynomial in ideal vanishing T. Product. If B ideal generated `b_1..b_r`, f could e.g. b_1 qS qH degree deg b1+1+1, if q point separators; but it may not have positivity. Is qS linear point separator? Given point s∈K50, `q_s=1+Σ_i(z_i-s_i)^2` over ordered K equals zero iff all coords equal. Since K real and sum squares=0 iff each 0. For H, q_s(p)=1+||p-s||², degree2. For B need b(p)=0. `f=b q_s q_h`. On T zero. Degree `deg b+4` (if b nonconstant; q each degree2 but actually quadratic). But positivity no. We can present as vanishing candidate, not separator. This addresses monomials? b unknown. If B is parameter curve and b one implicit equation, one polynomial not enough in A50 to define it; but only need one b vanishing, not ideal generator. Could choose any nonzero equation. The actual b's monomials depend on parameterization. To vanish on entire B, any relation.

Could construct f as product. For union finite, yes. If target B algebraic closure has ideal J_B, choose nonzero b∈J_B. Point ideals m_s,m_h. In ambient K[x,y], points may have coordinates in K (matrices perhaps K); q_s as affine sum squares. Then product. But if S/H not K-rational, use real algebraic point ideals. Given canonical likely K? S6 entries maybe roots etc K. Yet don't assume. K real.

Degree candidate `deg b+4`; if b constant? nonzero relation. qS/H are quadratics. But cannot ensure f positive. Could use q based on coordinates.

Question 2 exact rational SOS. Over K "rational SOS" ambiguity: SOS coefficients in K vs Q. K is real, ordered embedding? `Q(sqrt2,sqrt3)` sits in R but has two choices signs; specify embedding √2>0,√3>0. SOS over Q is narrower. Exact certificate would require coefficient witnesses. No f/g given, so no certificate.

We can detail Stengle correct schema:
Let `I` generated f_i, `J` generated P, basic semialgebraic set:
`S=V(I)∩V(J)∩⋂ {g_j≥0}`.
If S=∅, Putinar under Archimedean? Stengle always gives preordering certificate (for empty basic semialgebraic set): `-1 ∈ I+J + Q(g)` where Q generated sums of squares? In an ordered ring. Putinar Archimedean for rational? Quadratic module if archimedean. Better use Stengle preordering. Exact:
`-1 = σ0 + a + ∑ σ_j g_j`, where `a∈I+J` not necessarily each multiplier polynomial as sum. They write sum h_i f_i; any ideal element can represented if generators; h_i arbitrary polynomials, not necessarily SOS. The user's equation says h_i perhaps? They list `h_i * f_i`; likely h_i not necessarily SOS. `s_j` SOS. Equality P is in h terms. If include g=P or -P as guards both ≥0, P=0, but cleaner `qP` in ideal. For branch:
`p=P_corner` is polynomial in H entries (if H coords). If restrict real H, P may be complex? P corner determinant Hermitian is real, but in x,y perhaps. If complex determinant equation P=0 is two real equations ReP=0, ImP=0 unless H special. The 3x3 principal submatrix of Hermitian has real determinant. Need signatures. If H general 6x6 Complex, `P=0` one complex equation equals 2 real. Background says polynomial likely real. Need flag.

Stengle certificate:
`-1 = σ0 + a + Σ σ_j g_j`, `a∈〈f_1,...f_55,P〉`, `g_j` inequalities.
If insist expand `a=Σ h_i f_i + h_P P`.
For real points, equality ideal terms h arbitrary.

To refute detached set D:
Define g_j that exactly encode D (on X). If `f_sep - ε≥0` and theorem says all detached points satisfy it, but might also include near points. Certificate excludes a superset. Fine. If actual distance guard needed, include exact semialgebraic `D_δ`; f is sufficient not equivalent. If the certificate yields no g≥0 point, it excludes all satisfying f≥eps. Combined with every detached point satisfying f≥eps, no detached. This is okay. But as noted f could fail if f lies in their algebraic closure.

Dimension: Putinar/Stengle doesn't inherently classify dimensions. A certificate can refute semialgebraic set. It will exclude any D satisfying all guards, regardless dimension. But if a putative component is not in guard, no. Zero sets of f or equations could harbor components and certificate won't see. Need add saturation/localization guards for each stratum/dimension or show all putative detached points meet inequality. Positivity of one f on all outside δ needed.

Also SOS degree bounds: if finite degree ansatz, exact rational coefficients can be checked. Degree not given. To refute 0D/1D, can use Positivstellensatz for semialgebraic descriptions, but no dimension bounds needed. However finite ansatz failure is not nonexistence certificate. Need exact symbolic identity or verified rational univariate representation / exact arithmetic. Numerics not enough.

The equation with `g=f_sep-eps`:
If f_sep≥eps for distance≥δ, and target at distance0, all D satisfy. Stengle identity implies no p satisfying equations and guard. But if X is compact, a continuous nonnegative f vanishing T can perhaps use `f-eps≥0` only if f values separated. On compact D yes. Positivstellensatz.

If `P=0` included as semialgebraic guard via `P≥0, -P≥0`, okay, but in ideal term exact.

"rational SOS over Q (or K)" Need note K coefficients not rational. If certificate over Q, f_sep with K? K real algebraic. A rational certificate exists only if set defined over Q and emptiness; denominators allowed. Here coordinates K. SOS over Q can handle rational polynomial equations, but f includes K? K is algebraic extension and real ordering. Need say coefficient field and embedding.

Question 3 Lean formalization. Need provide exact theorem declaration/hypothesis signatures/proof outline, but cannot due undefined concepts/type mismatch. We can offer corrected interface blueprint conditional, perhaps not assert theorem. Need carefully use Lean syntax likely valid-ish.

They want theorem:
```
theorem singular_segre_branch_exhaustion :
    ∀ (H : Matrix (Fin 6) (Fin 6) Complex),
      IsCH6 H → P_corner H = 0 →
      (H ∈ Orbit B6 ∨ H ∈ Orbit S6 ∨ H ∈ Orbit H6)
```
Problems:
- `Complex` Lean has no ordered ring, real/imag extraction.
- IsCH6 must be explicit; cannot assume target.
- Orbit B6: B6 is family, define `OrbitSet (fun θ => ...)`.
- H6 name collides variable H maybe.
- `P_corner H = 0` if Complex equality valid. For Hermitian determinant real but Pcorner function should be defined.
- B6/S6/H6 need exact matrices or parameterizations.
- Classification statement likely false/circular. A theorem can be declared only if actual definitions and assumptions support.
- `propext`, `Quot.sound` do not supply algebraic result. `Quot.sound` is not an axiom? In Lean 4, quotient induction principle perhaps theorem. Standard axioms list usually `[propext, Classical.choice, Quot.sound]`. User says standard axioms [propext, Quot.sound], omit choice perhaps. We should state no classification follows from them; no "proof outline" can be honest except conditional assumptions.

Could give robust Lean interface:
Represent frames not 6x6 complex:
```
abbrev Coord5 := Fin 5 → ℝ
abbrev Frame6 := Fin 6 → Coord5
```
or matrix:
`H : Matrix (Fin 5) (Fin 6) ℝ × ...` complex columns. A 5×6 complex matrix can be `Matrix (Fin 5) (Fin 6) ℂ`; real coords 60? Actually 5*6 complex =60 real, all circles gives 30? Background 25 coords means perhaps only 5 columns? Wait 5*5=25 x +25 y, but six vectors requires 5*6=30 complex. Why only 25? For a 5×6 frame, six vectors each C5 =60 real, not 50. They give 50 coords => 5 vectors C5 or 25 complex entries. If r_j indexing 1..5? Circle equations 25 says 5 columns, not 6. Yet 15 pair equations = C(6,2), inconsistent! Let's inspect: "25 circle equations ... for x_ij,y_ij for 1<=i,j<=5" indeed 25 r entries. 15 orthogonality equations could be among 6 vectors each maybe first five entries? Missing sixth vector coordinates. Unless each `(x_ij,y_ij)` is a complex scalar for 5x5 H, and r_j for j=1..5? only 5, pair count10 not15. Or six complex projective points represented by 5 coordinates? No.

Maybe x_{ij}, y_{ij} for i,j≤5 correspond a 5x5 real/imag matrix H; columns r_j? j=1..5. Then 15 orthogonality could be among 6? impossible. This is another count inconsistency. Wait 55 equations in 50 real coordinates: 25 circles + 30 pairwise orthogonality for 6 columns. Six columns would need 60 real coordinates. Maybe due one column omitted/derived? Could normalize etc, but then 50 could parameterize 5 of six unit vectors? Six unit vectors in C5 cannot be orthogonal anyway.

Maybe MUB in C^5 has six vectors, 60 real coords, but projective global phase reduces 5, not 10, still 55 perhaps? Could fix phases? 50 not enough generally. But circle equations 25 indicates 5 columns.

So explicitly:
- 15 unordered pairs means 6 objects.
- 25 circle equations means 25 complex coordinates = five C5 vectors. Unless omitted coordinates, not defined.
Thus I55 isn't fully specified. This is decisive. Need mention.

Could be typo `1&lt;=i,j&lt;=5` coordinates x,y are entries of 5×5 H, and H maybe 6 vectors in C6? A 5x5 matrix has five columns, no six. If vectors in C5 six requires x i=1..5, j=1..6 =60. Maybe r_6 determined by others? Orthogonality no.

Thus cannot instantiate f_i 55 explicitly from background. We can state if one takes all 6 r_j ∈ C5 despite coordinate omission, real locus empty by rank. If takes 25 coordinates and five columns, 15 orthogonality equations undefined. Either way no coherent I55.

Type of theorem `Matrix 6x6 Complex`: 36 complex=72 real, not 50. If Hermitian, 36 real. Neither 50. Need map.

Thus answer should lead with consistency audit, then answer conditional.

Question demands "Provide exact..." We should explicitly say no such exact data follows; can't responsibly invent. Maybe offer template theorem declaration that encodes missing assumptions. Need include What supports etc likely four appearances? User says "Always write with claim discipline: include What it supports, What it does not support, Narrowest defensible claim, Next test needed." Could structure entire response and final 4-part summary. To ensure satisfy, include those labels for each major answer or at least final? "Always" perhaps include a claim box at start and final. We can include a four-part claim discipline after each question maybe verbose. Desired oververbosity 5. We should make robust.

Let's map all issues.

I. Exact definition:
Let x,y indexed maybe. Orthogonality:
`f^R_{jk}=∑_{i=1}^5(x_ij x_ik+y_ij y_ik)`
`f^I_{jk}=∑(x_ij y_ik-y_ij x_ik)`.
For j&lt;k among six.
Norm=1. If all zero, Gram I6, rank6, but R* R rank≤5. So empty. If j only five, only 10 pairs, not15. No B6 etc. This does not touch actual MUB because wrong equations and firewall.

Mutual unbiased:
`q_{jk}=a_jk²+b_jk²-1/5=0` for j&lt;k; not a=b=0. In C5 six unit vectors MUB may exist (two bases etc), but no result here. We must phrase "This is the defining equation for pairwise unbiasedness, not a conclusion about maximal size." Avoid claims MUB6=3.

The polynomial P_corner: If H is 5x6 frame, no 3x3 corner perhaps a 3×3 Gram submatrix. Define `G_{jk}=⟨r_j,r_k⟩`, then P=det G[0..2,0..2], real. A theorem with H as 6x6 perhaps G. For complex H arbitrary, determinant complex. Need exact.

II. Separator:
Given coherent X/T. Algebraic condition. Explain no fixed degree.

Could there be a logical obstruction to f if T's algebraic closure intersects detached components. We can give proposition:
If `Z` is irreducible complex algebraic component of `V_C(I55)` and `T∩Z` is Zariski dense in Z, then any f∈K[x,y] vanishing on algebraic closure T vanishes identically on Z. If detached D⊂V_R(I55)∩Z, then f=0 on D, so cannot satisfy f≥ε for D at distance≥δ. Therefore requested f can exist only if no detached real semialgebraic subset lies in each Zariski-dense component (or those are already target). This is likely central to "algebraic closure" choice. Need mention it doesn't mean Euclidean detached from curve? If B curve Zariski closure itself, not high component. But if "Orbit B6" under U6 has higher dimension and Zariski dense in full variety, yes. Notation target theorem includes `Orbit B6`, while Q1 target `B6(theta)` maybe not orbit. If T includes algebraic
