# Projective history algebras: sectors, purification and a scoped MUB6 consequence

2026-10-11. Written conditional proofs and exact native controls.
`realizes: null`; `authority_effect: None`; `genesis_effect: None`.

A phase in history composition changes the algebraic reconstruction problem.
For a finite abelian group $A$ and a normalized unitary two-cocycle $\alpha$,
the full twisted complex group algebra is simple exactly when its commutator
bicharacter has trivial radical. More generally, if that radical has order
$r$, the algebra has $r$ equally sized simple blocks, each of size
$d=\sqrt{|A|/r}$. This extends the
[untwisted groupoid result](qm_finite_history_groupoid.md) without applying
its thinness criterion to a different multiplication law.

## 1. Admitted data and the positive algebra

Let $A$ be a finite abelian group, written additively, with identity $0$.
Supply $\alpha:A\times A\to U(1)$ satisfying

$$
\alpha(0,g)=\alpha(g,0)=1,\qquad
\alpha(g,h)\alpha(g+h,k)=\alpha(h,k)\alpha(g,h+k).
\tag{1}
$$

Define a complex vector space with **independent** basis $u_g$ and product
$u_gu_h=\alpha(g,h)u_{g+h}$. Equation (1) is precisely associativity on this
basis. Its identity is $u_0$. Taking $(g,h,k)=(g,-g,g)$ gives
$\alpha(g,-g)=\alpha(-g,g)$, so define

$$u_g^*=\overline{\alpha(-g,g)}u_{-g}=u_g^{-1}.$$

Left multiplication by $u_g$ is a permutation of the label basis with
unit-modulus coefficients. It is unitary for the standard coefficient inner
product, and its inverse is left multiplication by $u_g^*$. Extending
conjugate-linearly gives $L_{a^*}=L_a^\dagger$. Associativity and
$L_a u_0=a$ establish a faithful $*$-representation. Its finite-dimensional
image is a complex C*-algebra.

The identity-coefficient trace $\tau(a)=a_0$ satisfies

$$\tau(ab)=\tau(ba),\qquad
\tau(a^*b)=\sum_g\overline{a_g}b_g.$$

The first identity uses $\alpha(g,-g)=\alpha(-g,g)$; the second uses the
inverse phase in the involution. Thus positivity and faithfulness follow from
the declared unitary cocycle. This constructs an algebra after complex scalars,
linear combinations and the cocycle have been supplied. It does not derive
them from an inscription, a finite category or a cochain identity.

## 2. The center and the complete complex block profile

Set

$$B(g,h)=\alpha(g,h)\overline{\alpha(h,g)},\qquad
R=\{g\in A:B(g,h)=1\text{ for every }h\in A\}.$$

**Bicharacter.** Conjugation by $u_g$ sends $u_h$ to $B(g,h)u_h$.
Since $u_gu_k$ differs from $u_{g+k}$ by a scalar, their inner automorphisms
give $B(g+k,h)=B(g,h)B(k,h)$. The identity
$B(g,h)=B(h,g)^{-1}$ gives multiplicativity in the second variable as well;
$B(g,g)=1$. Hence $R$ is a subgroup.

**Center.** In $au_h-u_ha$, the coefficient of $u_{g+h}$ is
$a_g(\alpha(g,h)-\alpha(h,g))$. Translation by $h$ permutes the labels, so
there is no cancellation between distinct $g$ at that coefficient. It follows
that

$$Z(\mathbb C_\alpha[A])=\operatorname{span}\{u_r:r\in R\},\qquad
\dim_{\mathbb C}Z=|R|.\tag{2}$$

To extract blocks we use the standard **finite-dimensional complex C*-algebra
decomposition theorem**: a finite-dimensional complex C*-algebra is a direct
sum of full complex matrix algebras. This classification is an imported
mathematical theorem here, not a new Lean proof or a consequence of counting
dimensions. Equation (2) therefore gives exactly $r=|R|$ simple blocks.

Their sizes are equal for an additional structural reason. Choose one
representative $t$ for each coset of $R$. Because each $u_t$ is invertible,

$$\mathbb C_\alpha[A]=\bigoplus_{t\in A/R}u_t Z$$

is a free module over its center, of rank $|A|/r$. For any minimal central
projection $p$, the space $Zp$ is one-dimensional, so the simple ideal
$\mathbb C_\alpha[A]p$ has complex dimension $|A|/r$. If it is $M_d(\mathbb C)$,
then $d^2=|A|/r$. This proves the profile, including equal block sizes:

$$\boxed{\mathbb C_\alpha[A]\cong\bigoplus_{j=1}^{r}M_d(\mathbb C),\qquad
r=|R|,\quad d^2=|A|/r.}\tag{3}$$

In particular it is simple iff $R=\{0\}$. The native profile reports this
**complex** classification. Over a smaller exact coefficient field the blocks
need not split there. For example, over $\mathbb Q(i)$ the two-label algebra
$u_s^2=i$ does not split into two copies of $\mathbb Q(i)$, whereas its complex
extension has two scalar blocks. Writing a native exact element is not the
same operation as extending the scalar field.

**Gauge qualification.** Replacing $u_g$ by $\beta(g)u_g$, with $\beta(0)=1$
and $|\beta(g)|=1$, changes the cocycle to

$$\alpha'(g,h)=\beta(g)\beta(h)\overline{\beta(g+h)}\alpha(g,h).$$

For abelian $A$ the new factors cancel in $B$, so the radical and profile are
unchanged. This proves invariance under the stated scalar rephasing. It does
not authorize arbitrary history identifications or physical transformations.

## 3. One 36-label carrier, different sector structures

For $A=\mathbb Z_n^2$, a primitive $n$th root $\zeta$, and integer $k$, take

$$\alpha_k((a,b),(c,d))=\zeta^{kbc},\qquad
B_k((a,b),(c,d))=\zeta^{k(bc-da)}.$$

The cocycle identity follows by expanding the exponents on both sides of (1).
Testing the two coordinate generators shows that the radical consists exactly
of labels with $ka=kb=0\pmod n$. If $s=\gcd(k,n)$, then $|R|=s^2$ and
equation (3) gives $s^2$ blocks of size $n/s$.

For $n=6$ every row has the same group, 36 independent basis labels, and complex
vector-space dimension 36:

| $k\pmod6$ | Radical size / sector count | Full complex algebra |
| --- | ---: | --- |
| 0 | 36 | $\mathbb C^{36}$ |
| 1 or 5 | 1 | $M_6(\mathbb C)$ |
| 2 or 4 | 4 | $\bigoplus_1^4 M_3(\mathbb C)$ |
| 3 | 9 | $\bigoplus_1^9 M_2(\mathbb C)$ |

No dimension count can distinguish these multiplication laws or their state
spaces. The native validator checks every cocycle triple for all six values
of $k$, then checks the radicals against the explicit congruence conditions.

For $k=1$, let $X|j\rangle=|j+1\rangle$ and
$Z|j\rangle=\zeta^j|j\rangle$. Then $ZX=\zeta XZ$ and
$U_{ab}=X^aZ^b$ realizes exactly $\alpha_1$. If $a\ne0$, $U_{ab}$ has no
diagonal entries; if $a=0,b\ne0$, its trace is a vanishing geometric sum.
Therefore

$$\operatorname{Tr}(U_{ab}^*U_{cd})=n\,\delta_{a,c}\delta_{b,d}.$$

The $n^2$ operators are independent and span all $n\times n$ matrices. Together
with the product and involution checks, this gives a faithful algebra
isomorphism, rather than a dimension-compatible guess. In dimension six the
native test verifies every one of the 1,296 basis products and overlaps, all
36 adjoints, and reconstruction of all 36 matrix units using the existing
Weyl owner. Symmetric displacements use a primitive 12th root and labels
modulo 12; reducing those labels modulo six without the extra phase loses a
winding sign. The unsymmetrized $U_{ab}$ above is periodic modulo six.

## 4. Purification and protected questions

Assume the full complex algebra is retained faithfully, all normalized positive
linear functionals and positive-contraction effects are admitted, composition
is the standard C*-tensor product, and sufficient simple ancillas and joint
states are operationally available. Under these **additional operational
premises**, [PO-000 E.7](../../projection_obstruction/projection_obstruction_paper/projection_obstruction.md)
applies to the $r$ sectors in (3):

$$\operatorname{Tr}\sigma^2\le\sum_{j=1}^{r}p_j^2,
\qquad \min_{\eta\text{ pure-composite marginal}}\tfrac12\|\rho-\eta\|_1
=1-\max_jp_j.$$

Here the trace is the canonical sum of simple-block matrix traces, not the
trace of a redundant regular representation. Attainment needs the specified
ancilla availability. Every state is purifiable iff $r=1$, equivalently the
commutator pairing is nondegenerate. For equal sector weights, the sharp purity
ceiling is $1/r$ and the closest pure-composite marginal is at distance
$1-1/r$. Thus the rows above give ceilings $1/36,1,1/4,1/9$ and distances
$35/36,0,3/4,8/9$, respectively, for the stated equal-weight inputs.

The [limited-ancilla extension](qm_ancilla_capacity.md) gives sharp
bounds for a specified available ancilla algebra and a separate separable-state
restriction. Its six-dimensional example uses these same algebras as ancillas;
the largest simple block, rather than total algebra dimension, controls capacity.

Let a report retain $A$ and the scalar field but omit the cocycle. On the
two-model class $k=0,1$, the protected question “dimension of the center” has
answers 36 and 1 at the same report. It cannot descend through that report.
The exact minimax absolute-error floor is $35/2$, attained at the midpoint
$37/2$. This applies the
[WDP fiber criterion](../../finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_bridge_register.md)
to a missing algebraic premise. It is not a measured physical uncertainty.

Selecting a simple sector after the fact has a nontrivial kernel whenever
$r>1$; it must declare which protected questions are lost. Retaining individual
history labels does not by itself guarantee faithfulness on their linear span,
as the earlier $C_2$ sign-character control demonstrates.

## 5. An exact restricted MUB6 consequence

The $M_6$ algebra is necessary background for the six-dimensional question; it
does not supply seven mutually unbiased bases. A useful tractable subproblem
is the family of bases from **order-six cyclic commuting Weyl classes** in
the particular $\mathbb Z_6^2$ realization above.

Every cyclic subgroup $L$ of order six is isotropic for $B_1$ and its six Weyl
operators commute. A generator can be scalar-rephased to have order six.
All its nonidentity powers have trace zero, so its six eigenvalues are the
sixth roots, each with multiplicity one. Its spectral projectors are the
Fourier sums of those powers divided by six. These give a rank-one basis.

Two such bases are mutually unbiased **iff** $L\cap M=\{0\}$. For sufficiency,
expand their rank-one projectors in the Weyl basis. Only the identity term
contributes to the trace of the product, yielding $1/6$. For necessity, a
nonidentity shared Weyl operator is a nonzero traceless element of both
diagonal algebras. Mutually unbiased bases have orthogonal traceless diagonal
spaces: this follows by expanding in their rank-one projectors and using
the overlaps $1/6$. Such a common nonzero element is impossible.

By the Chinese remainder isomorphism,
$\mathbb Z_6^2\cong\mathbb F_2^2\times\mathbb F_3^2$. Each order-six cyclic
subgroup is exactly a pair of lines, one in each factor. There are three lines
over $\mathbb F_2$ and four over $\mathbb F_3$, giving 12 classes. Two classes
intersect only at zero iff their lines differ in **both** factors. At most
three classes can therefore be pairwise disjoint. Three are attained by the
classes generated by $(1,0),(0,1),(1,1)$. There are exactly
$\binom43\,3!=24$ unordered triples and no four-class family.

The native group test enumerates all 12 classes with the sovereign subgroup
owner and checks all candidate triples and quadruples. A separate physics
test constructs the 18 spectral projectors for $X,Z,D(1,1)$ and submits them
to the existing `MubSystem::try_new` validator. It checks projector laws,
orthogonal resolutions of identity and every cross-basis overlap. The system
has three bases and is incomplete in the seven-basis sense.

**This is an exact result for the stated Weyl class family, not a global
upper bound on MUBs in $\mathbb C^6$.** No theorem here places an arbitrary
fourth basis in that family. That representation/coverage obligation is
precisely why a finite family exhaustion cannot settle unrestricted MUB6.

## 6. Native history and FSP obligations

The existing [generative-history construction](../../finite_obstruction_calculus/witnessed_difference_programme/docs/derivations/generative_histories_contextual_compression_derivation.md)
starts with an admitted typed signature or an actual guarded transition
function. GEN-WDP-72 identifies the greatest protected contextual congruence;
it supplies neither finite index nor native reversibility. A proposed
history-to-projective-group map must preserve the actual guards and declared
questions in every compatible two-sided context before the algebraic theorems
above can reflect information back to the source.

There is a general finite-quotient obstruction worth making explicit. Suppose
a legal loop $h:x\to x$ can be repeated arbitrarily and has protected additive
cost $c(h)>0$, with $c(1_x)=0$. Its powers have pairwise different costs
$c(h^m)=m c(h)$, so **no finite report can preserve the exact cost of all
powers**. In a finite groupoid image, the image of $h$ has finite order $m$,
which gives the explicit collision $q(h^m)=q(1_x)$ with unequal costs.
Thus a finite projective realization must either exclude this source case,
restrict the admitted histories, or explicitly give up/refine that protected
question. This is a conditional no-go theorem, not an assertion that every
native Genesis regime has such a repeatable positive-cost loop.
Finite-dimensional amplitude spaces still have infinitely many elements: this
no-go concerns a finite-valued report or finite groupoid label, not every
possible complex-valued encoding of an unbounded history.

The follow-on [native history cost bridge](qm_native_history_cost.md)
now instantiates this premise in Source-25's add/remove rules, proves a sharp
finite-window report bound, and separately treats free linearization. It
distinguishes accumulated history price from endpoint/minimum result cost and
the source's original 100-step request from the unbounded rule closure.

FSP's ordinary sign character on paths remains distinct from the two-cocycle
that changes multiplication here. A vertex sign gauge preserves loop signs;
an arbitrary rephasing $\beta$ of algebra basis labels is a different declared
family. The [existing six-hop sign obstruction](quantum_to_classical_descent/README.md)
and its endpoint-descent criterion survive in their stated family. A
nondegenerate projective algebra does not remove negative Monte Carlo weights
or establish efficient sampling.

The [S(n)/MSS-N architecture](../../finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/README.md)
still prohibits a selected mathematical realization from creating a native
stage. Carrier admission, finite quotient, scalar choice, cocycle selection,
faithful reflection, full state/effect spaces, composition and process
availability remain separately justified premises. GAP-FQM-021 stays open.

## 7. Implementation and reproduction scope

TwistedAbelianAlgebra (`external:sha256:e18265604b1f898f958b563058d2a4992246262d498213293f44f138621b6a75`)
uses the existing `FiniteGroup::from_table` owner and canonical exact complex
fields. It checks all group laws, commutativity, normalization, unitarity and
every cocycle triple, with a 64-label limit. It exposes the radical, complex
block profile, twisted product/involution, identity trace and faithful regular
action. Missing, nonunitary or incoherent data are refused; no phases are
silently completed. The exact native coefficient fields do not replace the
complex scalar extension used in (3).

From `external:git-tree:ac1f6d647c3ecc2bf45f6fc4922213ac752e71a3`, with the configured toolchain/cache, run the
two packages sequentially:

```sh
cargo test -j 1 --offline --locked -p tfqm_lie_theory --test twisted_abelian_algebra
cargo test -j 1 --offline --locked -p quantum_physics --test projective_history_mub6
```

The algebra tests (`external:sha256:6005a1eda9d6d760c8e82023d88eaf47bc5580265128a247a3a405c49d6b12d5`)
and physics test (`external:sha256:d145f197c01e78b7ee0c612e93a8f46089b5c7940767cd2e0a57640970f2be35`)
separate finite arithmetic from the general written proofs. The execution
receipt records actual results and selected source hashes. There is no new
Lean module in this block, no full-suite claim, and no claim that the finite
MUB family exhausts all operational measurements. Historical receipts and
source archives are unchanged; this is a research note, not a new publication
release or deposit.
