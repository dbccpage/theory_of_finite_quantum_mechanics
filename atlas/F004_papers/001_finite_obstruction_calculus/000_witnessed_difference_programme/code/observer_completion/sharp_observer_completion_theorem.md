# Sharp Observer-Completion Theorem

A finite rational theorem connecting raw defect detection, repair quotients,
minimal additional measurements, and independently replayable recovery evidence.

Prepared for Jeremy H. Carroll, 4 October 2026.

The proposed measurement counts are correct when additional scalar measurements
may be arbitrary rational linear functionals. Put
$k=\dim\ker Q$ and $r=\dim(\ker Q\cap\operatorname{im}d_0)$.
The minima are $r$ for raw soundness, $k-r$ for quotient soundness, and $k$
for both. The actual three-patch carrier gives $(3,3,6)$; both coordinate
conventions of the actual coupled carrier give $(0,2,2)$.

For any fixed completion and supplied rational polyhedral norms, the theorem
also gives sharp rational recovery constants and finite verification procedures.
Minimum measurement count does not select a unique completion or minimize
its recovery constant. Checked certificates supply evaluation evidence;
authorization remains separate.

## 1. Presentation and definitions

Supply rational matrices
$$
D=d_0:\mathbb R^p\to V=\mathbb R^n,\qquad Q:V\to W=\mathbb R^w,
$$
and put $B=\operatorname{im}D$, $K=\ker Q$, $H=B\cap K$.
These real spaces are the real extensions of the rational presentations.
The constructed measurements, invisible witnesses, and recovery-constant
certificates can be rational. Rational distance certificates below also
require a rational query vector; their inequalities apply over the real
extension.

The same $B$ has two declared roles: realizable raw defects are $Ds\in B$,
and allowed repair changes of an arbitrary cochain are vectors in $B$.
This identification is a hypothesis. If a site's defect operator and its
allowed repair operator have different images, use separate subspaces.

Supply rational polyhedral norms on $V$ and $W$. An exact description is
$$
\|v\|_V=\max_i F_i v,\qquad \|w\|_W=\max_j G_jw,
$$
with rational facet rows occurring in opposite pairs and spanning the
respective dual spaces. Their unit balls are bounded and have interior.
Positive weighted $\ell^1$ and $\ell^\infty$ norms qualify. The
zero-dimensional space has its unique norm.

Define
$$
I(b)=\|b\|_V\ (b\in B),\qquad
\Phi(v)=\min_{b\in B}\|v-b\|_V,\qquad
\Phi_Q(Qv)=\min_{b\in B}\|Qv-Qb\|_W.
$$
Finite-dimensional subspaces are closed. Restricting a minimizing sequence
of residuals to a bounded closed set proves attainment over the real
extension. Rational polyhedral data and a rational query vector additionally
give rational distance optima, as proved below. The optimal recovery constants
are rational independently of the queries. In particular, $\Phi(v)=0$
exactly when $v\in B$.

For $m$ additional scalar rows $R:V\to\mathbb R^m$, write
$A=(Q,R):V\to U=W\oplus\mathbb R^m$. Supply a rational polyhedral norm
on $U$ and define $\Phi_A(Av)=\operatorname{dist}_U(Av,A(B))$.
The augmented norm is additional data, not determined by the row count.
The counts below concern exact scalar linear measurements, not bits,
sensor cost, locality, or finite precision.

## 2. The theorem

**Theorem.** Under the preceding hypotheses:

| Guarantee | Necessary and sufficient condition | Minimum added scalar rows |
| --- | --- | ---: |
| $Qb=0\Rightarrow b=0$ for all $b\in B$ | $H=0$ | $r$ |
| $\Phi_Q(Qv)=0\Rightarrow\Phi(v)=0$ for all $v\in V$ | $K\subseteq B$ | $k-r$ |
| Both | $K=0$ | $k$ |

All three minima admit rational completions. For each fixed completion
satisfying a guarantee, its optimal recovery constant is finite and rational
under the declared polyhedral norms. Exact finite procedures construct
minimality evidence and sharp recovery certificates. Failure of a guarantee
has a rational invisible witness and excludes a finite recovery constant.

### 2.1 Soundness and the exact sequence

The kernel of $Q|_B$ is $H$, proving the raw criterion. For the quotient
criterion the crucial identity is
$$
Q^{-1}(Q(B))=B+K. \tag{1}
$$
Indeed $Qv=Qb$ exactly when $v-b\in K$. Faithfulness of the norms and
closedness of the subspaces give
$\Phi_Q(Qv)=0\iff v\in B+K$.
Thus quotient soundness is $B+K\subseteq B$, equivalent to $K\subseteq B$.
The reverse zero implication, from $\Phi$ to $\Phi_Q$, always holds.

Both criteria imply $K=H=0$, and injectivity of $Q$ implies both.
For any nonzero $z\in K$, membership $z\in B$ witnesses raw failure;
nonmembership $z\notin B$ witnesses quotient failure.

The canonical exact sequence is
$$
0\longrightarrow H\longrightarrow K
 \overset{z\mapsto z+B}{\longrightarrow}(K+B)/B
 \longrightarrow0. \tag{2}
$$
The final map is onto, and its kernel is exactly $H$. Consequently
$K/H\cong(K+B)/B$ has dimension $k-r$.
It is the kernel of
$$
\overline Q:V/B\to W/Q(B),\qquad v+B\mapsto Qv+Q(B).
$$
Surjectivity of $Q$ is unnecessary.

These subspaces, quotient maps, and dimensions are canonical relative to
$(D,Q)$. A splitting $K=H\oplus J$ requires a choice. An individual invisible
vector has no canonical decomposition into a repairable vector and an
irreducible representative.

### 2.2 Lower bounds

For $A=(Q,R)$ put $N=\ker A=K\cap\ker R$. Rank-nullity gives
$\dim N\ge k-m$.

Raw soundness requires $R|_H$ injective, so $m\ge r$.
Quotient soundness requires $N\subseteq B$, hence $N\subseteq H$;
therefore $k-m\le r$ and $m\ge k-r$.
Both require $N=0$, so $m\ge k$.

### 2.3 Rational constructions and all optimal completions

Choose a rational basis $h_1,\ldots,h_r$ of $H$. Extend it by
$j_1,\ldots,j_{k-r}$ to a basis of $K$. Extend further by a basis
of a complement of $H$ inside $B$, and finally to a basis
$\mathcal E$ of $V$. Exact elimination makes every choice rational.
Let $\mathcal E^{-1}$ give the dual coordinates.

The first $r$ dual coordinates give a raw completion.
The next $k-r$ give a quotient completion: they vanish on $B$, and
their kernel inside $K$ is $H$.
The first $k$ give a simultaneous completion.
Use no rows when the respective minimum is zero. This attains each bound.

More precisely:

- An $r$-row raw completion is optimal exactly when $R|_H$ is injective.
- A $(k-r)$-row quotient completion is optimal exactly when
  $\ker(R|_K)=H$; equivalently $R(H)=0$ and the induced map
  $K/H\to\mathbb R^{k-r}$ is an isomorphism.
- A $k$-row simultaneous completion is optimal exactly when
  $R|_K$ is an isomorphism.

For quotient completion, vanishing on all of $B$ is an achievable choice,
not necessary for every optimal $R$. A fixed pivot rule gives reproducibility
in coordinates, not invariance under coordinate changes. This proves the
algebraic and minimality parts of the theorem. ∎

## 3. Exact algebraic certificates

Represent rational numbers as integer or reduced-fraction strings.
Zero, positivity, rank, and membership use exact arithmetic.

From $(D,Q)$ exact elimination produces:

1. A basis matrix $S$ of $B$, with rational factorizations $DT=S$, $SU=D$.
2. A basis matrix $N$ of $K$, with $QN=0$ and
   $\operatorname{rank}Q+\operatorname{rank}N=n$.
3. A basis $H_0=S\operatorname{Null}(QS)$ of $H$.
4. An adapted basis and its rational inverse for Section 2.3.

A checker can recompute reduced row forms. Alternatively, a rank claim
can carry a nonzero maximal minor and a factorization through that rank.
The supplied executable checker recomputes ranks.

A completion receipt contains its target, $R$, $(k,r)$, basis evidence,
and the claimed minimum. Check the original subspaces, dimension lower
bound, row count, and required condition for $A$. A working completion
alone is not evidence of minimality.

Failure has one of two small certificate formats:

| Failure | Rational evidence | Checks |
| --- | --- | --- |
| Raw | $z\ne0$, preimage $s$ | $Ds=z,\ Qz=0$ |
| Quotient | $z$, covector $\lambda$ | $Qz=0,\ \lambda D=0,\ \lambda z=1$ |

For the second, $\lambda z=1$ proves nonmembership and
$\Phi(z)\ge1/\|\lambda\|_{V,*}>0$.
Such a rational covector exists: extend a basis of $B$ by $z$, prescribe
zero on $B$ and one on $z$, then extend linearly.

Thus the procedure can diagnose an observer, complete a requested
guarantee, or check a candidate completion and return an invisible witness
for the augmented observer if it fails. Valid finite presentations always
admit the unrestricted completions. Invalid norm data produce an
invalid-presentation result. A caller-imposed budget can interrupt finite
enumeration; interruption is not an optimality certificate.

## 4. Sharp recovery constants and finite certificates

For a fixed $A$ and fixed norms, define least nonnegative extended constants
$$
C_{\rm raw}(A)=\sup_{0\ne b\in B}\frac{\|b\|_V}{\|Ab\|_U},
\qquad
C_{\rm quo}(A)=\sup_{v\notin B}\frac{\Phi(v)}{\Phi_A(Av)}.
$$
A positive numerator over zero gives infinity. A zero recovery domain
has constant zero: $B=0$ for raw recovery, or $V/B=0$ for quotient recovery.
A zero report space with a nonzero recovery domain instead gives infinity.

They are finite exactly under their respective soundness conditions.
Under soundness they are inverse-map norms on the images of
$A|_B$ and $\overline A:V/B\to U/A(B)$.
An injective finite-dimensional linear map has a positive minimum
norm on the compact unit sphere, proving bounded inverse recovery.
An invisible witness proves the converse.

The forward inequality is
$$
\Phi_A(Av)\le\|A\|\Phi(v). \tag{3}
$$
Apply $\|A(v-b)\|_U\le\|A\|\|v-b\|_V$ and minimize.
Passivity with constant one requires contractivity or an appropriate
induced norm; the kernel conditions alone do not imply it.

### 4.1 An exact distance certificate

For $\|v\|_V=\max_i F_i v$, the quotient distance is
$$
\min_{a,t}t\quad\text{subject to }F(v-Sa)\le t\mathbf1. \tag{4}
$$
A rational pair $a_*,\mu$ certifies the exact value $t_*$ when
$$
\begin{aligned}
F(v-Sa_*)&\le t_*\mathbf1,\\
\mu&\ge0,\qquad \mathbf1^T\mu=1,\qquad S^TF^T\mu=0,\\
\mu^TFv&=t_*.
\end{aligned} \tag{5}
$$
The covector $F^T\mu$ annihilates $B$ and is a convex combination
of norm facet rows. For every repair $a$,
$\mu^TFv=\mu^TF(v-Sa)\le\|v-Sa\|_V$.
The supplied repair attains this lower bound.

Here is why matching certificates exist. The quotient unit ball is the
linear image of the compact unit ball of $V$. A supporting hyperplane
at a nonzero quotient boundary point supplies a norm-one quotient
functional. Its pullback annihilates $B$ and belongs to the polar
$\operatorname{conv}\{F_i\}$, giving (5). At the zero class use a
convex average of opposite rows to give the zero functional.
This is the geometric finite LP duality argument.

For a rational query $v$, exact rational construction enumerates full-rank
active sets in (4).
The epigraph has no lines: symmetry and spanning of $F$, and independence
of the columns of $S$, force every line direction to vanish.
A finite minimum is attained at a vertex. The dual feasible set in (5)
is a rational polytope contained in a simplex; it too has a rational
optimal vertex. Enumerate basic feasible solutions and retain a pair
with matching objective. This terminates and proves rational attainment.
The same construction certifies observed distances using the report
facets and a basis of $A(B)$. When the ambient normed space is zero-dimensional,
use its unique zero vector and distance zero directly. There are no facet
rows and no probability vector $\mu$ of sum one in that branch; the
executable checker records this separate vacuous certificate.

### 4.2 The sharp raw constant

Assume raw soundness, and write $b=Sx$. For report facets $G$,
$$
P_{\rm raw}=\{x:GASx\le\mathbf1\} \tag{6}
$$
is a bounded rational polytope with interior, since $AS$ is injective.
Therefore
$$
C_{\rm raw}(A)
=\max_{x\in\operatorname{vert}P_{\rm raw}}\|Sx\|_V. \tag{7}
$$
A convex function at a convex combination of vertices is no larger than
the largest vertex value. This proves (7).

Enumerate all subsets of $\dim B$ inequality rows, solve those with
independent active normals, and retain feasible solutions. Every vertex
has such an active subset, including degenerate vertices. The complete
vertex list, objective values, and a maximizer certify the sharp constant.
A checker independently enumerates all subsets so an omitted vertex
cannot silently lower the answer. Nonzero maximizing defects have
observation norm one, certifying equality.

### 4.3 The sharp quotient constant

Assume quotient soundness and $q=n-\dim B>0$. Choose a rational complement
matrix $E$ so $[S\ E]$ is invertible, and a basis matrix $T$ for $A(B)$.
The matrix $M=[AE\ -T]$ has independent columns: $AEx=Tc$ implies
$Ex\in B$ by soundness, hence $x=0$, then $c=0$.

The lifted polytope
$$
P_{\rm lift}=\{(x,c):G(AEx-Tc)\le\mathbf1\} \tag{8}
$$
is bounded, rational, and has interior. Its projection to $x$ is
exactly $\{x:\Phi_A(AEx)\le1\}$, including the boundary by attainment.
It has $q+\dim A(B)\le n$ variables. Consequently
$$
C_{\rm quo}(A)
=\max_{(x,c)\in\operatorname{vert}P_{\rm lift}}\Phi(Ex). \tag{9}
$$
The objective is convex, so the same vertex argument applies.

Attach a matching certificate (5) at every vertex and certify that the
enumeration is complete. The largest value is an upper bound everywhere
and is attained. At a positive maximizer $\Phi_A(AEx)=1$:
otherwise scaling its class to that sphere would increase the value.
An additional observed-distance certificate can record that equality.

Equations (7) and (9) prove rationality and give an exact terminating
algorithm for the sharp constants. No efficiency claim is made.
If $B=0$ the raw constant is zero; if $B=V$ the quotient constant is zero.

### 4.4 Reconstruction and perturbed reports

Raw soundness reconstructs a unique $b\in B$ from a report known to lie
in $A(B)$, not a unique site state when $\ker D\ne0$.
Quotient soundness reconstructs a unique class in $V/B$ from a report
class in $\overline A(V/B)$, not a preferred representative or repair.
Exact elimination supplies rational decoders after complements are chosen.
Image membership must be checked before applying a decoder.

For $\|\eta\|_U\le\varepsilon$,
$$
\|b\|_V\le C_{\rm raw}(A)(\|Ab+\eta\|_U+\varepsilon),
$$
and
$$
\Phi(v)\le C_{\rm quo}(A)
\bigl(\operatorname{dist}_U(Av+\eta,A(B))+\varepsilon\bigr).
$$
The triangle inequality and 1-Lipschitz property of distance prove these
bounds. They are deterministic, not probabilistic calibration statements.

## 5. Reconstructing the three-patch carrier

Use LGGR V's site order $(u_0,u_1,u_2,x_{01},x_{12},x_{20})$,
three coordinates per site, identity translations, and edge order
$$
(x_{01},u_0),(x_{01},u_1),(x_{12},u_1),
(x_{12},u_2),(x_{20},u_2),(x_{20},u_0).
$$
This is Projection Obstruction 7.4.5 after changing indices 1,2,3
to 0,1,2. The actual site-to-edge operator is
$$
D=C\otimes I_3,\qquad
C=\begin{pmatrix}
1&0&0&-1&0&0\\
0&1&0&-1&0&0\\
0&1&0&0&-1&0\\
0&0&1&0&-1&0\\
0&0&1&0&0&-1\\
1&0&0&0&0&-1
\end{pmatrix}. \tag{10}
$$
Thus $C^0=V=\mathbb R^{18}$ and $\operatorname{rank}D=15$.
For six edge blocks $v=(v_0,\ldots,v_5)$ put
$$
L=(I_3,-I_3,I_3,-I_3,I_3,-I_3).
$$
Since $LD=0$ and $\operatorname{rank}L=3$, $B=\ker L$.

The observers delete coordinates $(0,1,1,2,2,0)$ on the six
respective edges. Their stacked retained-coordinate matrix $Q$ has
12 rows, and
$$
K=\{(a_0e_0,a_1e_1,a_2e_1,a_3e_2,a_4e_2,a_5e_0)\}.
$$
On $K$,
$$
Lv=(a_0-a_5)e_0+(a_2-a_1)e_1+(a_4-a_3)e_2.
$$
Hence
$$
k=6,\quad r=3,\quad
H=\{(ae_0,be_1,be_1,ce_2,ce_2,ae_0)\}. \tag{11}
$$
Moreover $\dim Q(B)=15-3=12$, so $Q(B)=W$.
The original observed quotient diagnostic vanishes on every cochain.

For the source's actual site assignment $s(u_i)=\lambda e_i$,
$s(x_{ij})=0$, multiplication by (10) gives
$$
Ds=\lambda(e_0,e_1,e_1,e_2,e_2,e_0),\quad
I(Ds)=6|\lambda|,\quad QDs=0,\quad\Phi(Ds)=0. \tag{12}
$$
The site state certifies exactness. This is raw false green, not positive
quotient obstruction. A different cochain
$z=(e_0,0,0,0,0,0)$ is invisible with $Lz=e_0$, so it witnesses
quotient failure and cannot be a section defect.

Use entrywise $\ell^1$ on defects and stacked reports. Then
$$
\Phi(v)=\|Lv\|_1. \tag{13}
$$
The lower bound follows from $\|L\|_{1\to1}=1$ and $LB=0$.
The residual $t=(Lv,0,0,0,0,0)$ attains it, because $v-t\in B$.
Solving $Da=v-t$ gives a site repair certificate. A dual certificate
is $L^T\operatorname{sgn}(Lv)$.

### 5.1 Optimal completions and sharp constants

Add the three raw reads
$$
R_{\rm raw}v=(v_{0,0},v_{2,1},v_{4,2}). \tag{14}
$$
On $B$, the cycle equation reconstructs the other hidden coordinates:
$$
\begin{aligned}
b_{5,0}&=b_{0,0}-b_{1,0}+b_{2,0}-b_{3,0}+b_{4,0},\\
b_{1,1}&=b_{0,1}+b_{2,1}-b_{3,1}+b_{4,1}-b_{5,1},\\
b_{3,2}&=b_{0,2}-b_{1,2}+b_{2,2}+b_{4,2}-b_{5,2}.
\end{aligned}
$$
Each measured scalar contributes to itself and one reconstructed coordinate
with coefficient magnitude one. The decoder's maximum absolute column
sum is 2, proving $I(b)\le2\|Ab\|_1$.
A site state supported only at $u_0$ with value $e_0$ has defect norm 2
and augmented report norm 1, proving $C_{\rm raw}=2$.
Quotient soundness still fails.

For quotient soundness add $R_{\rm quo}=L$, three cross-edge reads.
They annihilate $B$, and $A(B)=\mathbb R^{12}\oplus0$.
Thus $\Phi_A(Av)=\|Lv\|_1=\Phi(v)$, giving $C_{\rm quo}=1$.
Raw failure (12) persists.

For both add all six deleted coordinates
$$
R_{\rm both}v=(v_{0,0},v_{1,1},v_{2,1},v_{3,2},v_{4,2},v_{5,0}).
$$
Then $A$ is a coordinate permutation, an $\ell^1$ isometry.
Both sharp constants are 1. The counts $3,3,6$ are minimal by (11).

## 6. Reconstructing the coupled carriers

Order sites $(b,a_0,a_1)$ with two coordinates per site, edges
$(b,a_0),(b,a_1)$, and zero translations. The full operator is
$$
D=\begin{pmatrix}
-1&0&0&0&0&0\\
0&-1&0&0&0&0\\
-1&0&0&0&0&0\\
0&-1&0&0&0&0
\end{pmatrix},\qquad
B=\{(x,y,x,y)\}. \tag{15}
$$
Both edge defects are $-s(b)$, independent of the two other site states.

The source conventions differ:

| Source | Stacked report |
| --- | --- |
| LGGR V, Theorem 6 | $Q_{\rm L}v=(v_0,v_3)$ |
| Projection Obstruction, 7.4.7-B | $Q_{\rm P}v=(v_1,v_2)$ |

The anchor's first observer reads the second fiber coordinate; its second
reads the first. Their kernels and invisible witnesses differ, even though
dimensions and constants agree. Both are checked in the replay.

For $Q_{\rm L}$, $K=\operatorname{span}(e_1,e_2)$;
for $Q_{\rm P}$, $K=\operatorname{span}(e_0,e_3)$.
In either case $k=2$, $H=0$, and $Q(B)=\mathbb R^2$.
Raw soundness holds, quotient soundness fails, and the minima are
$(0,2,2)$.

With entrywise $\ell^1$,
$$
I(x,y,x,y)=2(|x|+|y|)=2\|Q(x,y,x,y)\|_1,
$$
so the original sharp raw constant is 2. With the source's
best-single-observer aggregation $\max(J^0,J^1)=\max(|x|,|y|)$,
it is instead 4, attained at $x=y=1$.

For arbitrary cochains,
$$
L=\begin{pmatrix}1&0&-1&0\\0&1&0&-1\end{pmatrix},\qquad
\Phi(v)=|v_0-v_2|+|v_1-v_3|=\|Lv\|_1. \tag{16}
$$
The coordinatewise triangle inequalities give the lower bound;
residual $(v_0-v_2,v_1-v_3,0,0)$ attains it.
For LGGR V, $e_1$ is invisible with quotient mass 1.
For the anchor convention, $e_0$ is such a witness.

Adding $R=L$ is a minimum two-row quotient completion. It also preserves
raw soundness, with constants $(C_{\rm raw},C_{\rm quo})=(2,1)$.
Adding the two missing coordinate reads instead makes $A$ an isometry,
with constants $(1,1)$. Thus equally small simultaneous completions
can have different conditioning.

### 6.1 The source scalar quotient witness

The scalar specialization in Projection Obstruction 7.4.12 and LGGR V's
quotient remark has
$$
D=\begin{pmatrix}-1&0&0\\-1&0&0\end{pmatrix},\qquad
B=\{(x,x)\},\qquad\omega=(1,-1).
$$
The zero repair has residual norm 2; the covector $(1,-1)$
annihilates $D$, has dual $\ell^\infty$ norm 1, and evaluates to 2.
Matching bounds prove $\Phi(\omega)=2$, and no site state produces
$\omega$.

That source specialization does not specify an observer $Q$.
The replay also includes a clearly labeled NEW extension with $Q=0$.
Its counts are $(1,1,2)$: one coordinate for raw recovery, one difference
for quotient recovery, two coordinates for both. This observer choice
is not attributed to either source.

### 6.2 Exact results for the selected completions

All table constants use entrywise $\ell^1$ reports. Infinity means a
proved failure of the corresponding recovery inequality.

| Carrier and completion | Added rows | $C_{\rm raw}$ | $C_{\rm quo}$ |
| --- | ---: | ---: | ---: |
| Three-patch original | 0 | $\infty$ | $\infty$ |
| Three-patch raw reads | 3 | 2 | $\infty$ |
| Three-patch cycle reads | 3 | $\infty$ | 1 |
| Three-patch missing coordinates | 6 | 1 | 1 |
| Coupled original, either convention | 0 | 2 | $\infty$ |
| Coupled difference reads | 2 | 2 | 1 |
| Coupled missing coordinates | 2 | 1 | 1 |
| Scalar new zero observer | 0 | $\infty$ | $\infty$ |
| Scalar plus first coordinate | 1 | 2 | $\infty$ |
| Scalar plus difference | 1 | $\infty$ | 1 |
| Scalar plus both coordinates | 2 | 1 | 1 |

## 7. Certificate formats and replay

The package contains this theorem, a standard-library Python reference
implementation, a separate example replay entry point, and generated
rational certificates. No floating-point or external optimization
library is used.

The generic receipt includes the exact input, target, completion,
original dimensions, basis evidence, initial failure witness when one
exists, and optional exhaustive recovery vertices with primal/dual
distance witnesses. Matrix objects store row and column counts and a
rectangular array of rational strings. The authority-effect field is None.

A receipt must be bound to the expected input, norms, target, and source.
Hashing attacker-supplied input does not establish its identity.
The generic command-line checker takes a separate expected-input file.

The larger source examples use shorter global algebraic certificates:

1. $GAD=D$ and $\|G\|_{1\to1}\le C$ certify raw recovery. A nonzero
   site-realized $b$ with $\|b\|_1=C\|Ab\|_1$ certifies sharpness.
2. $LD=0$, $\operatorname{rank}L=n-\operatorname{rank}D$, $LT=I$,
   and $\|L\|_{1\to1},\|T\|_{1\to1}\le1$ certify
   $\Phi(v)=\|Lv\|_1$ for all $v$.
3. The same evidence on the observed carrier, together with
   $L_{\rm obs}A=L$, certifies equality of quotient diagnostics.
   A nonzero quotient class makes the constant 1 sharp.

These are global identities, not sampled estimates.
The induced $\ell^1$ matrix norm is the maximum absolute column sum.
A decoder upper bound alone is not a sharpness certificate.

From the package directory:

~~~text
python replay_examples.py check observer_completion_certificates.json
python replay_examples.py adversarial observer_completion_certificates.json
python observer_completion.py solve generic_input.json
python observer_completion.py check generic_receipt.json generic_input.json
~~~

The generic fixture uses $B=\operatorname{span}(e_0)$ in $\mathbb R^3$,
the first-coordinate observer, an $\ell^1$ defect norm, and an
$\ell^\infty$ completed-report norm. Its sharp constants are 1 and 2.
It exercises the general enumeration path with unequal norms.
A weighted rational distance fixture uses $2|v_0|+3|v_1|$,
the diagonal repair line, and $v=(1/2,-3/2)$; its exact distance is 4.

The source checker reconstructs the site/interface operators before
comparing stored matrices. It checks the scaled section family, the scalar
nonexact cochain, both coupled conventions, minimum completions, and sharp
constants. The delivered package checks nine adversarial mutations: wrong minimum,
raw constant, quotient constant, graph sign, site preimage, target,
missing recovery vertex, forged dual, and authority escalation. The repository
review adds six controls for nested authority labels, false norm labels,
invalid active-row evidence, omitted initial failures, changed distance
queries, and incorrect adapted bases, for fifteen rejected mutations total.
Additional checks cover zero-dimensional spaces, $B=0$, $B=V$, zero
and injective observers, and restricted coordinate menus.

The generic algorithms are intentionally exhaustive and may be impractical
on large facet descriptions. The source fixtures avoid that expansion
through the concise identities above. This is exact fixture and checker
evidence, not a Lean formalization or verification of Python itself.
The scoped repository tests pass 27 cases, including an independent
determinant-minor oracle for 81 small presentations and 243 completions.
No full repository suite, native Rust verification, or Lean build is claimed.

## 8. Counterexamples to omitted hypotheses

**Raw does not imply quotient soundness.**
Let $B=\operatorname{span}(e_0)$ in $\mathbb R^2$ and $Q(x,y)=x$.
Then $H=0$, but $e_1\in K\setminus B$.

**Quotient does not imply raw soundness.**
With the same $B$, let $Q(x,y)=y$. Then $K=B$; the quotient is visible,
but every nonzero raw defect is invisible.

**Separate one-row budgets do not make one row sufficient for both.**
Take $Q=0$, $B=\operatorname{span}(e_0)$ in $\mathbb R^2$.
The three minima are $1,1,2$.

**Restricted sensors change attainability.**
Take $Q=0$, $B=\operatorname{span}(1,1)$.
One unrestricted row $(1,-1)$ restores quotient soundness.
Neither coordinate read alone does: each leaves an axis outside $B$.
If only coordinate reads are allowed, two are required.

**Realizability and repair space are separate hypotheses.**
If all $V$ is realizable but no nonzero repair is allowed, using $B=0$
makes the raw test vacuous and says nothing about realized vectors.
Use the actual raw image for the raw guarantee.

**Seminorms break the membership criterion.**
Take $B=0$, $Q(x,y)=x$, and defect seminorm $p(x,y)=|x|$.
Observed zero implies $p=0$ despite $K\not\subseteq B$.

**Nonclosed repair images break the criterion.**
In $\ell^2$, take $B=c_{00}$ and $Q=0$.
Distance to $B$ is zero everywhere, so the zero-distance implication
holds although $K=\ell^2\not\subseteq B$.

**Rational norms need the stated real-extension condition.**
On $\mathbb Q^2$, $p(x,y)=|x+\sqrt2\,y|$ is a norm over $\mathbb Q$,
but its real extension is not a norm. For $B=\mathbb Q^2$, $Q=I$,
source $\ell^1$ and report $p$, rational approximants to $\sqrt2$
exclude any finite recovery constant despite injectivity.
For legitimate nonpolyhedral real norms, counts still hold, but sharp
constants need not be rational: the identity from an $\ell^2$ report
to an $\ell^1$ defect in two dimensions has constant $\sqrt2$.

**Rank does not determine conditioning.**
For $B=V=\mathbb R$, $Qx=\varepsilon x$, rational $\varepsilon>0$,
both guarantees hold while $C_{\rm raw}=1/\varepsilon$.
Rescaling added rows also changes constants under a fixed report norm.

**A scalar score is not a linear report.**
For $B=\operatorname{span}(1,1)$ and $Q=I$, $(1,1)$ and $(1,-1)$
have identical scalar $\ell^1$ score 2. The first is repairable and the
second has quotient mass 2. Retain $Qv$ and $Q(B)$ for the quotient test.

**Testing only section defects makes the quotient question vacuous.**
Every $Ds$ already has $\Phi(Ds)=0$.
Quotient soundness concerns the entire declared $V$, including cochains
outside $B$; source family (12) cannot itself establish positive
quotient obstruction.

## 9. Interfaces to the source papers

Projection Obstruction 7.2 requires a declared physical-residual adapter
$n_e\in R_e\mapsto q_e(n_e)=\omega_e\in V_e$.
The assembled $\omega$ is an induced cochain, not automatically $Ds$.
Our $Q$ observes the declared cochain carrier and must not silently
replace that physical adapter. The adapter, repair differential,
measurement maps, and rational representation must be explicit.
This theorem does not establish their physical adequacy.

LGGR asks whether a realized $Ds$ can be nonzero while all measurements
vanish. The quotient question asks whether $\overline Q$ preserves
the distinction between the zero obstruction class and every other class.

In WDP's quotient-observer convention the report map satisfies $QD=0$,
so $B\subseteq K$. Our quotient criterion then becomes $K=B$,
exactly separation of all of $V/B$. Its raw criterion fails when
$B\ne0$, because the observer deliberately forgets repairs.
The more general target $W/Q(B)$ permits $QD\ne0$ and makes the
connection to LGGR precise.

CODA can use independently checked certificates as evaluation evidence.
Neither a minimum measurement count, a successful repair, nor a positive
dual obstruction authorizes installing sensors, changing repairs,
promoting claims, or executing a policy. Those require a separate
authority operation and jurisdictional premises. An authority-effect
field records the interface; it does not authenticate a grant.

## 10. Standard mathematics and contribution

The kernel criteria, exact sequence, basis constructions, and dimension
bounds are standard linear algebra. Quotient norms, bounded inverse
arguments, polyhedral vertex enumeration, and matching LP certificates
are also standard. No new foundational principle or complexity result
is claimed.

The combined result makes the two diagnostic guarantees, their distinct
completion budgets, their sharp quantitative certificate obligations, and
their actual site-to-edge instantiations available as one theorem.
The source calculations expose the incorrect evaluation that would result
from conflating raw inconsistency and quotient obstruction.

This work does not establish priority or claim that no equivalent theorem
exists in the literature. Its contribution here is the integrated
derivation and reproducible, source-bound certificate package.

## 11. Source record

Repository sources were inspected at commit
39aacbe33bc7e6fabb94323b14e1ddeebe15e86e.

- [Projection Obstruction](https://github.com/dbccpage/the_symbol_game/blob/39aacbe33bc7e6fabb94323b14e1ddeebe15e86e/omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/000_projection_obstruction/projection_obstruction.md),
  Sections 7.2–7.3, 7.4.5, 7.4.7-B, 7.4.8, 7.4.12.
  Git blob: 886d5b23a7a5635847b21077b78d685284a96991.
- [LGGR V](https://github.com/dbccpage/the_symbol_game/blob/39aacbe33bc7e6fabb94323b14e1ddeebe15e86e/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_local_green_global_red_foundational_series/lggr_v_local_green_global_red/lggr_v_local_green_global_red.md),
  Sections 1, 3, 4, and the formalization boundary in Section 6.
  Git blob: e7cf055125ceea5eb1e3cdc2fe754c7e99406f4b.
- The user-supplied WDP manuscript, version 0.5.0, dated 3 October 2026:
  Chapters 4, 10.2, 10.5, 14.3–14.4, and 15.
  Its bytes are identified in source_provenance.json. This is the delivered
  author's attachment provenance; those manuscript bytes were not supplied
  with this package for independent repository review. The three Git source
  blobs above and below were independently confirmed at the pinned commit.
- [CODA](https://github.com/dbccpage/the_symbol_game/blob/39aacbe33bc7e6fabb94323b14e1ddeebe15e86e/omega_engine_atlas/coda_atlas/F005_coda/coda/coda.md),
  Sections 4.1–4.2 and 7.
  Git blob: b2b2795c4bab93f5c927c9d034f7fdda5e774aef.

The source papers establish their own scoped results. The completion
matrices, instantiated minimum counts, recovery certificates, and labeled
scalar observer extension are derived here. The reviewed package is now
linked from WDP; the pinned Projection Obstruction, LGGR V, and CODA sources
are unchanged. delivered_sha256sums.txt preserves the original package
hashes, and repository_review.json distinguishes the delivered claims from
the repository's checks and corrections.
