# A uniform analytic source and pointwise Meron response

This continues the [actual source-pressure proof](meron_source_field_response.md).
It proves a joint time/volume limit of the protected intensive Kubo query in
an explicit high-temperature region. The argument retains the full periodic
CAR trace. It is a written proof using an imported polymer convergence
criterion; finite exact computation and the existing metric Lean proof have
separate scopes.

## 1. The target and its admitted domain

For even L>=4 use precisely the earlier Hamiltonian and source:

\[
 h_x=I/4-P_x,\quad \|h_x\|=3/4,\qquad
 a_x=(-1)^x(n_x-1/2),\quad \|a_x\|=1/2,
\]

\[
 H_L/t=\sum_xh_x,\quad A_L=\sum_xa_x,\qquad
 p_L(\theta,z)=L^{-1}\log\operatorname{Tr}
      e^{-\theta H_L/t+zA_L}.
\]

Declare 0<=theta<=1/192 and the complex-source radius R=1/64. These are
sufficient constants from the proof below, not a maximal temperature range.
For real source the logarithm is the physical one. Its complex branch is
fixed by continuation of the normalized partition from zero coupling and
zero source. The source remains dimensionless.

For r>=rho>=0, r+rho<=1/192 and integer M>=1 set q=1+r/M and h=log q.
Use the entire source curve

\[
 X_{L,M}(z)=q^{-LM/4}\operatorname{Tr}
 \left[T_{\rm odd}(q)e^{zA_L/(2M)}
       T_{\rm even}(q)e^{zA_L/(2M)}\right]^M,
 \qquad f_{L,M}(z)=L^{-1}\log X_{L,M}(z). \tag{AR-1}
\]

The factor q^(-LM/4) is retained. In particular this is the actual physical
pressure, and z/(2M) is exact along the differentiated curve. Differentiating
the earlier rational Euler source samples would be a different curve.

## 2. Factorization uses even CAR support

The normalized full-Fock trace is tau_L=2^(-L)Tr. Even CAR operators with
disjoint physical site supports commute. Their normalized trace factorizes.
To see the latter, reorder the modes so the disjoint supports form successive
blocks. The induced signed occupation-basis permutation is unitary,
implements the CAR isomorphism, and preserves trace. Its fermionic signs
must be retained; an unsigned permutation of basis vectors is not the
general mode-reordering map. In this ordered basis an even operator on
one block has no parity string on earlier blocks, so the ordinary normalized
tensor trace gives the product. Unused modes contribute one.

Every h_x and a_x is even. This includes the wrapping bond: its support is
the two endpoint modes in the CAR algebra even when its occupation-basis
matrix contains a long parity string. The following support graph is on CAR
supports, not on occupation-matrix tensor supports. Both parity sectors are
included; no unrestricted periodic spin trace is substituted.

## 3. Two exact polymer representations

For the Hamiltonian exponential use L bond labels K_x=-theta h_x and
two source labels K_(x,1)=K_(x,2)=z a_x/2 at each site. There are 3L labels.
Each has norm at most b=1/256 on the admitted domain. Join two labels when
their supports intersect; this graph has degree at most six.

Expand tau_L exp(sum_i K_i) in words. Partition each word's set of distinct
labels into connected components C. Operators belonging to different
components commute and trace-factorize. The interleaving counts cancel the
factorials between components. Thus the partition is exactly the hard-core
polymer partition with polymers the nonempty connected label sets, with
incompatibility whenever their supports overlap. The activity w(C) sums
words using every label in C at least once and no other label. Bounding
each word by its operator norms and summing its positive multiplicities gives

\[
 |w(C)|\le\prod_{i\in C}(e^{\|K_i\|}-1)
          \le(e^b-1)^{|C|}. \tag{AR-2}
\]

For AR-1 distribute its scalar factor among the LM bond factors. The
normalized partition is an ordered product of 3ML individual exponentials:
LM factors exp(-h h_x) and 2ML factors exp(z a_x/(2M)). Each exponent has
norm at most b/M, since h<=r/M. The overlap graph has maximum degree at
most 7M-1: a bond copy meets 3M-1 bond copies and 4M source copies; a source
copy meets 2M bond copies and 2M-1 source copies. The first bound also
covers the latter.

Write exp K_i=I+V_i and expand in subsets of the ordered labels. Each
subset's connected components factor exactly as above, retaining the
original order inside a component. Its activity is tau_L of that ordered
V-product, so

\[
 |w(C)|\le t_M^{|C|},\qquad
 t_M=e^{1/(256M)}-1\le\frac1{256M-1}. \tag{AR-3}
\]

The inequality follows by bounding the exponential series by the geometric
series for 0<=1/(256M)<1. This second representation allows noncommuting
overlapping factors; it makes no classical-diagonal assumption.

## 4. A volume- and time-uniform convergence margin

In a graph of maximum degree Delta, the number of connected k-vertex sets
containing a specified root is at most (4Delta)^(k-1). Choose a canonical
rooted spanning tree of each set and order its children. Plane rooted tree
shapes number at most the Catalan bound 4^(k-1), and each tree edge has at
most Delta choices. Its visited vertices recover the set; repeated or
colliding choices only enlarge this upper bound. The k=1 count is one.

With Delta<=7M-1, take a(C)=|C|. For either representation (M=1 for AR-2),
the sum of |w(C)|e^a(C) over polymers containing one root is at most

\[
 S_M=\frac{e t_M}{1-28M e t_M}
       \le\frac1{57M}, \tag{AR-4}
\]

because e<3 and M e t_M<=3M/(256M-1)<=1/85. A polymer incompatible with C
contains a vertex in C's closed neighborhood, whose size is at most
7M|C|. Therefore

\[
 \sum_{D\not\sim C}|w(D)|e^{|D|}
       \le 7M|C|S_M\le\frac7{57}|C|<|C|. \tag{AR-5}
\]

The imported Kotecky–Preiss criterion gives absolute convergence of the
log partition and its pinned derivatives under this inequality, with
pinned majorant at most exp(a(C)). The precise form used is equations
(2.10), (2.14) and (2.15) in
[Fernandez and Procacci, arXiv:math-ph/0605041v2](https://arxiv.org/pdf/math-ph/0605041v2).
It includes a polymer's self-incompatibility. This import concerns the
abstract polymer partition; AR-2–AR-5 supply its model-specific premises.

Integrate the pinned derivative along the straight activity path from zero
to w. This bounds |log Xi| by sum_C |w(C)|e^|C|. Overcount each polymer by
its label roots, then use AR-4. Since the label count is 3ML,

\[
 |p_L(\theta,z)-\log2|\le C_0,\quad
 |f_{L,M}(z)-\log2|\le C_0,\qquad C_0=1/19,
 \quad |z|\le R. \tag{AR-6}
\]

These functions have no partition zero in this source disk. The strict
margin also allows a neighborhood of the closed disk for each finite
system. AR-6 is uniform in L and M, and is a conclusion about the actual
noncommuting full-CAR model. A finite sample of traces is not its proof.

## 5. Identify one analytic thermodynamic target

SF-1 already gives p_L(theta,x)->p(theta,x) uniformly for real x. AR-6
identifies an analytic continuation p(theta,z) to |z|<R. One elementary
normal-family argument is to bound every Taylor coefficient by Cauchy's
formula, select a coefficientwise convergent subsequence and sum on smaller
disks. Every subsequential analytic limit agrees with the real limit on
(-R,R), so the identity theorem makes it unique. Consequently the entire
sequence converges uniformly on compact disks, with all source derivatives.
The bound AR-6 passes to the target.

For the time product a real-source pressure error against this same target,
uniform on [-R,R], follows from SF-2's positive similar-matrix argument
with exact d=x/(2M), hence with no Euler source drift:

\[
 |f_{L,M}(x)-p(\theta,x)|\le B,
\]

\[
 B=\frac L M(r+R/2)^2
           \exp\left[\frac L M(r+R)\right]
       +\frac34\left[\frac{r^2}{2M}+\rho\right]
       +\frac{3(r+\rho)}{2L},\quad
 \theta\in[r-\rho,r+\rho]. \tag{AR-7}
\]

Along L->infinity, M/L->infinity and rho->0 this tends to zero at bounded
r. The same normal-family uniqueness argument identifies the joint
time/volume analytic limit. All temperatures used here must stay inside
the declared domain; no increasing-temperature scaling is inferred.

## 6. A quantitative pointwise response bound

Cauchy's formula applied to AR-6, after subtracting log 2, gives for
|x|<=R/2

\[
 |p_L^{(4)}(x)|,\ |f_{L,M}^{(4)}(x)|,\ |p^{(4)}(x)|
       \le C_4=384C_0/R^4. \tag{AR-8}
\]

For a real C^4 function, its central second difference at step epsilon
differs from its second derivative by at most C_4 epsilon^2/12. This follows
from Taylor's integral remainder, with the odd cubic terms cancelling.
Apply it to both f and p, and propagate AR-7 through the three values.
For 0<epsilon<=R/2,

\[
 |f_{L,M}''(0)-p''(\theta,0)|
       \le \frac{4B}{\epsilon^2}
                   +\frac{64C_0\epsilon^2}{R^4}. \tag{AR-9}
\]

The same bound for p_L uses B=3theta/(2L). For example, take even
L=4k^4, M=L^2, epsilon=R/(4k) and rho=0 at any fixed admitted theta=r.
Then B=O(k^-4) and AR-9 is O(k^-2). Shrinking parameter intervals can
also be used if rho=O(k^-4), the same theta stays in every interval and
their upper endpoints remain admitted. This is a polynomial joint schedule,
not the earlier fixed-volume bound with an exponential-in-L constant.

Particle-hole symmetry makes the first derivatives vanish. Differentiating
AR-1 at zero inserts Q/(2M), where Q is the earlier sum of staggered
occupations over all half-time states. Thus the actual protected query is

\[
 f_{L,M}''(0)=\frac{\langle Q^2\rangle}{(2M)^2L},
 \qquad p_L''(\theta,0)=K_L(\theta)/L. \tag{AR-10}
\]

It is the original signed SQL history query, with its time and per-site
normalizations retained. AR-9 closes that intensive pointwise response to
one analytic thermodynamic value in the admitted region.

## 7. Computation and the remaining continuum question

The quantum owner retains the admitted temperature interval, exact q,
source radius, resolution and exact AR-7/AR-9 upper bounds. Its exponential
majorant is 3^ceil[(L/M)(r+R)]. The WDP adapter obtains StaggeredMoments
from the existing actual-chain owner, divides its time-averaged square by
L and retains the bound. Python independently binds the same normalized
query to the original SQL histories. A domain violation returns a refusal,
rather than attaching this analytic certificate to a finite answer.

The familiar q=3,M=2 fixture has theta_hat=2 log 3 and lies outside this
region. Its exact finite response remains valid; AR-9 supplies no continuum
certificate for it. Finite carrier and work caps remain in force, so code
does not execute the infinite schedule. Bounds on small carriers can be
wide; neither numerical efficiency nor an optimal convergence rate is claimed.

This result completes a particular observable limit at fixed spatial
lattice. The [presentation-completion theorem](cs_q_presentation_completion.md)
and circle/Pontryagin construction supply the selected geometry, while
AR-1–AR-10 now supply a dynamical estimate for one actual response.
The all-temperature pointwise question, critical/scaling regimes, spatial
mesh and coupling rescaling, nontrivial field correlation functions and
operator/distribution convergence still need their own estimates. There is
no general sign-problem algorithm or derived continuum field theory here.
The five enlarged Genesis obligations remain open at their stated scopes.

## 8. The spatial source-functional extension

The [spatial-source proof](meron_spatial_gaussian_source.md) now extends the
actual source polydisk to independent site sources, derives uniform local
response decay and closes a Gaussian fluctuation profile on the completed
circle. It retains a common continuous test function and an explicit spatial
error, rather than merely adding a mesh label to pressure convergence.
The broader interacting/critical spacetime and operator limits remain open.
