# Protected subgroup quotients and compact-open character separation

Date: 2026-10-08. AuthorityEffect: None.
Target: PLAN-7D-CSQ-PONTRYAGIN, still in progress.
Dependency: PR #601, reviewed checkpoint
`e10da6bc9714260fbed71af434a70e9a35a51b75`, advanced before publication to
`033d4b44162cdd16b42e1771edc2ed61e34b038d` without discarding its newer commits.

This is a derivation beyond [LE-1–LE-4](lane_e_character_duality_completion.md),
not a replacement for their completed scope. The actual
[CS/CS_Q/Q maps](cs_q_presentation_completion.md) and manuscript Appendix O
supply the image-factor setting:
[CS-D1](source_archive/coda_component_packages/cs/coda_cs.md) defines query
constancy on report fibers;
[CSQ-T1](source_archive/coda_component_packages/cs_q/coda_cs_q_bridge.md)
equates that condition with factorization on the actual image;
[Q-T3](source_archive/coda_component_packages/q/coda_q.md) extends uniformly
continuous maps into a complete metric target. These retained source bytes
are read at the dependency head above. None supplies a local-compactness certificate.
Algebraic image factorization, relative uniform control, closed quotient
separation, and compact-open bidual identification are separate steps.

## 1. Setting and the exact source criterion

Use LE-4's compatible finite abelian homomorphic presentations and their
abelian colimit G. Let p:G→M be the admitted homomorphism, where M is a
complete abelian group with an invariant metric. Write S=p(G) and
H=closure_M(S), with its inherited topology and group structure. View p
henceforth as G→H. The circle T=R/Z has distance in turns

$$
d_T([s],[t])=\min_{k\in\mathbb Z}|s-t-k|.
$$

A character chi:G→T is PC if, for every epsilon>0, some delta>0 satisfies
d_M(p(g),p(h))<delta implies d_T(chi(g),chi(h))<epsilon.
Use the established LE-4 bijection between these characters and continuous
characters of H, by restriction along p. PC kills ker p and descends
uniformly to S; completeness of T extends it to H, and density preserves
addition and uniqueness. Conversely, a continuous homomorphism on H is
uniformly continuous for its invariant group uniformity, so its pullback
is PC. No local compactness is needed for this correspondence.

Supply A≤G explicitly. Put N=closure_H(p(A)), a closed subgroup, and define

$$
A^\perp_{\rm PC}=\{\chi\text{ PC}:\chi|_A=0\},\qquad
D_A=\{g:\forall\chi\in A^\perp_{\rm PC},\ \chi(g)=0\}.
$$

For a subgroup L≤H define its continuous-character double annihilator by

$$
L^{\perp\perp}=\{h\in H:
  \forall\psi\in\widehat H,\ \psi|_L=0\Rightarrow\psi(h)=0\}.
$$

Here the hat denotes all continuous circle characters. It does not yet
assert any bidual topological isomorphism.

**PQ-1 (always-valid source identity).** One has

$$
D_A=p^{-1}(N^{\perp\perp}),\qquad
A+\ker p\ \subseteq\ p^{-1}(N)\ \subseteq\ D_A.                 \tag{1}
$$

Proof. A continuous character of H has a closed kernel, because T is
Hausdorff. Thus it kills p(A) exactly when it kills N. Apply the LE-4
extension correspondence to the definition of D_A to obtain the equality.
Every character killing N vanishes on N, giving the second inclusion.
For a∈A and k∈ker p, p(a+k)=p(a)∈N, giving the first. This also shows
that D_A is a subgroup; it is an intersection of kernels. QED.

## 2. Quotient factorization, continuity and separation

Let q:H→Q=H/N have the quotient topology. If psi:H→T vanishes on N, define

$$
\bar\psi(h+N)=\psi(h).
$$

If h-h'∈N, their psi values agree, so the definition is well-defined.
It preserves addition and is the unique factor with bar-psi composed
with q equal to psi, since q is surjective. For every open V⊆T,

$$
q^{-1}(\bar\psi^{-1}(V))=\psi^{-1}(V).
$$

The quotient topology therefore makes bar-psi continuous exactly when
psi is continuous. Conversely, a continuous character eta:Q→T pulls back
to eta composed with q and vanishes on N. These two operations are
inverse additive maps between characters of Q and characters of H
annihilating N. This establishes a character correspondence; it does not by
itself prove a compact-open topological isomorphism.

For completeness Q really is a Hausdorff topological group here.
The map q is open: q-inverse(q(U))=U+N is a union of translates of U.
Hence q×q is an open quotient map, and addition descends continuously;
inversion descends through q in the same way. If q(x)≠q(y), then x-y∉N.
Closedness of N gives a neighborhood V of zero such that
(x-y)+(V-V) avoids N. The open sets q(x+V) and q(y+V) are disjoint.
This establishes Hausdorffness as well as the algebraic quotient construction.

Define the continuous-character radical

$$
R(Q)=\bigcap_{\eta\in\widehat Q}\ker\eta.
$$

The just-proved correspondence gives

$$
N^{\perp\perp}=q^{-1}(R(Q)),\qquad
D_A=(q\circ p)^{-1}(R(Q)).                                  \tag{2}
$$

**PQ-2 (ambient equivalence).**

$$
N^{\perp\perp}=N
\quad\Longleftrightarrow\quad
R(Q)=\{0\}
\quad\Longleftrightarrow\quad
\widehat Q\text{ separates points of }Q.                     \tag{3}
$$

Proof. Equation (2), surjectivity of q, and ker q=N give the first
equivalence. Characters separate any distinct x,y exactly when some
character is nonzero at x-y, which is the second equivalence. QED.

**PQ-3 (exact source criterion).**

$$
D_A=p^{-1}(N)
\quad\Longleftrightarrow\quad
R(Q)\cap q(S)=\{0\}.                                        \tag{4}
$$

Proof. Equality says that for every g∈G, q(p(g))∈R(Q) implies
q(p(g))=0; this is precisely the displayed intersection condition.
The reverse inclusion always holds by (1). QED.

Thus global character separation of Q is sufficient. The exact source
condition only tests q(S). Replacing (4) with an unqualified equivalence
to global separation would add an unjustified step: density of S does
not say that its intersection with every nontrivial closed subgroup of
Q is nontrivial. We do not use such an inference.

**PQ-4 (recovering the original protected subgroup).** Under (4),

$$
D_A=A
\ \Longleftrightarrow\
A=p^{-1}(N)
\ \Longleftrightarrow\
\bigl(\ker p\le A\ \text{ and }\ S\cap\overline{p(A)}^{\,H}=p(A)\bigr).
                                                               \tag{5}
$$

Proof. The first equivalence uses (4). If A=p-inverse(N), its containment
of ker p follows from 0∈N. If p(g)∈S∩N then g∈A, proving the relative
closedness condition. Conversely, if p(g)∈N, relative closedness gives
a∈A with p(g)=p(a). Hence g-a∈ker p≤A and g∈A. The other inclusion
is automatic. QED.

Without assuming (4), recovery is equivalent to the conjunction of
(4) and the two conditions on the right of (5): if D_A=A, the
sandwich A⊆p-inverse(N)⊆D_A supplies (4) and (5).
Neither kernel containment alone nor relative closedness alone suffices.
For example p:Z/2→{0}, A={0} has closed image but loses all source
distinctions. Section 4 gives an injective p where closure alone destroys
the proposed recovery.

These statements quantify over the whole admitted PC character family.
For a chosen subfamily F⊆A-perp, its common kernel D_F contains D_A.
Equality requires F's joint evaluation to separate every remaining
source class; no finite purchased suite follows. For a concrete finite
bound, on (Z/2)^(m+1) any m circle characters have image in
{0,1/2}^m, so their joint map has a nonzero kernel by cardinality.
The full character family nevertheless separates points.

## 3. Hausdorff LCA specialization and its imported step

Assume additionally that H is locally compact; Hausdorffness already
comes from its metric. N is closed. Q is Hausdorff abelian by section 2.
For a compact neighborhood K of zero in H choose an open U containing
zero inside K. Then q(K) is compact and contains the open neighborhood
q(U), proving local compactness of Q.

Now import continuous-character separation for Hausdorff LCA groups.
Apply it to Q, not to the uncompleted presentation G. Equations (3)–(5)
give N=N-perp-perp, D_A=p-inverse(N), and the exact original-A recovery
criterion. This import is sufficient; biduality is not needed for
these algebraic equalities.

Source inspected 2026-10-08: Dikran Dikranjan,
[Introduction to Topological Groups](https://users.dimi.uniud.it/~dikran.dikranjan/ITG.pdf#page=81),
version 26.02.2018, Theorem 11.3.3, printed page 76 / PDF page 81.
The source's locally compact groups are Hausdorff. Its proof passes through
an open compactly generated subgroup and a compact quotient.
For the separately stronger compact-open bidual identification, its
[Theorem 12.5.4(c)](https://users.dimi.uniud.it/~dikran.dikranjan/ITG.pdf#page=102),
printed page 97 / PDF page 102, identifies canonical evaluation with a
topological isomorphism for Hausdorff LCA groups. These classical results
are imported, not new Lean declarations in this increment.

Completeness of M or H supplies neither local compactness nor character
separation. Closedness of N is essential to the Hausdorff quotient claim.
Nothing here promotes an arbitrary-semiring reconstruction, a native
continuum implementation, or a physical scaling limit.

## 4. A proper dense protected subgroup in the six-primary tower

**PQ-5 (all-level obstruction).** For n≥0 take G_n=Z/6^nZ and the
injective homomorphism k↦6k into G_(n+1). Identify its colimit with

$$
G=\mathbb Z[1/6]/\mathbb Z\subseteq T,\qquad
[k]_{6^n}\longmapsto[k/6^n],
$$

and take p to be inclusion. The displayed maps commute with transitions,
are injective at each level, and their union is exactly G; any two
representations agree at a common higher level. Put A=Z[1/2]/Z.
The element [1/3] is not in A, since 3k=2^n would be required for some
integer k after adjusting by an integer. A is dense in T: for t∈[0,1),
the dyadic floors floor(2^n t)/2^n approach t with error <2^-n.
It follows also that A is dense in the subspace G. Thus H=N=T.

By the integer Chinese remainder theorem there is a unique residue
0≤a_n<6^n with

$$
a_n\equiv0\pmod {2^n},\qquad a_n\equiv1\pmod {3^n}.
$$

At n=0 this means a_0=0. Both congruences reduce at the previous
level, so a_(n+1)≡a_n modulo 6^n. Define

$$
\chi_{3,n}([k])=[a_nk/6^n].
$$

Changing k by 6^n changes this value by an integer. The map is additive.
At the transition, a_(n+1)(6k)/6^(n+1) differs from a_nk/6^n by an
integer, proving compatibility at every level, and by iteration at
every transition. Hence these maps define one homomorphism chi_3:G→T.
This is not an inference from a finite tested prefix.

For k/2^m choose n≥m. Its level-n numerator is k 2^(n-m)3^n;
since 2^n divides a_n, its image is an integer, so chi_3 kills A.
At [1/3], chi_3=[a_n/3]=[1/3] for every n≥1.
More precisely write a_n=2^n u_n, with u_n invertible modulo 3^n.
Then chi_3([k/6^n])=0 iff 3^n divides k, precisely the dyadic
subgroup. Its image is Z[1/3]/Z: the values have 3-power denominators,
and chi_3 acts identically on every [k/3^n]. Consequently the algebraic
quotient G/A is the nonzero Prüfer 3-group.

For the specified sequence, write 2^n=3 b_n+r_n where r_n∈{1,2}.
For all n≥1,

$$
x_n=\frac13-\frac{\lfloor2^n/3\rfloor}{2^n}
    =\frac{r_n}{3\,2^n}
    =\frac{r_n3^{n-1}}{6^n}\in G,\qquad
0<x_n<2^{-n}.                                                \tag{6}
$$

Thus x_n→0 in the actual circle subspace. Since the subtracted
quantity is dyadic, chi_3(x_n)=1/3 for every n.
Fix epsilon=1/4. Given any real delta>0 choose n≥1 with 2^-n<delta;
then d_T(x_n,0)<delta but d_T(chi_3(x_n),0)=1/3>epsilon.
This is an all-delta failure of PC, and even of continuity at zero.

Since N=T, every continuous character of H annihilating N is zero.
Equations (1)–(4) yield D_A=G=p-inverse(N), although A is proper.
Here Q=H/N is trivial and its characters do separate points
vacuously. Thus it is recovery of A, not PQ-3's closure criterion,
that fails. Continuous observation collapses the protected quotient;
the nontrivial algebraic chi_3 survives only outside the PC family.

## 5. Compact-open zero isolation on the actual dyadic subgroup

**PQ-6 (checked zero-isolation argument).** Let D=A with the circle
subspace topology, and

$$
K=\{0\}\cup\{[2^{-n}]:n\ge1\},\qquad
U=\{\chi\in\widehat D:\ \forall x\in K,\ d_T(\chi(x),0)<1/4\}.
$$

The sequence [2^-n] tends to zero in D, not just in its completion,
because its limit belongs to D and D has the subspace topology.
A convergent sequence together with its limit is compact: in an open
cover, one set covers the limit and a tail, leaving only finitely many
points. Therefore K is compact in D. The set U is the compact-open
subbasic neighborhood [K,B(0,1/4)] restricted to continuous homomorphisms;
it is open and contains the zero character.

For j≠0 an integer write |j|=2^v m with m odd. The point
[2^-(v+1)] belongs to K, and j times it is [1/2] or [-1/2].
Its turns distance from zero is 1/2, so the character x↦jx is not in U.
Using LE-1's written classification of all continuous characters of D,
U={0}. Translations then make the entire compact-open dual discrete.

The checked Lean module uses the real quotient AddCircle 1 and its
quotient norm in turns throughout this argument. In particular it does
not insert the same 1/4 and 1/2 constants into Circle's chordal metric.
Its subgroup is {x:∃n, 2^n • x=0}; the checked
mem_dyadicCircle_iff identifies this with dyadic circle coordinates.
It inherits the subtype topology; no discrete domain proxy is used.

## 6. Formal scope, exact replay, and remaining declarations

[ProtectedCharacterQuotient](../lean4/WitnessedDifference/ProtectedCharacterQuotient.lean)
uses actual continuous additive homomorphisms to Additive Circle,
constructs quotientCharacter and pullbackCharacter, checks the closure
and quotient-separation laws, the exact source-image criterion, and
kernel/relative-closedness recovery. These are topological statements;
no numerical chordal/turns constants occur.

Its pcDoubleAnnihilator_eq has an explicit extension-correspondence
hypothesis, matching LE-4. The earlier
[completion module](../lean4/WitnessedDifference/PresentationCompletion.lean)
and [homomorphic extension module](../lean4/WitnessedDifference/PresentationDuality.lean)
supply the completion-side results. The present formal bridge does not
yet instantiate them as a continuous additive equivalence from that
abstract completion onto an arbitrary closed image H.

[DyadicCompactOpen](../lean4/WitnessedDifference/DyadicCompactOpen.lean)
checks K's compactness, U's openness, and exclusion of every nonzero
integer character. Its final theorem has exactly the declared premise

~~~lean
classification : ∀ χ : DyadicCharacter, ∃ j : ℤ, χ = integerCharacter j
~~~

The remaining unformalized implication is the production of this
classification for the actual dyadic subgroup, not zero isolation.
Its complete written proof remains LE-1; this increment does not
rederive it. Neither LCA character separation nor full compact-open
biduality is claimed as newly formalized.

The [exact replay](../../../../../../omega_engine_projects/finite_to_continuum/code/protected_quotient_examples.py)
reuses CyclicPresentation for the protected dyadic subgroup,
the existing exact rational validators, and circle_distance.
The new six-primary arithmetic has its own small coordinate functions;
the existing dyadic owner is not falsely renamed as a six-primary tower.
For every supplied positive rational delta the witness constructor
terminates by 2^-n→0 and implements (6). The independent verifier checks
CRT congruences, both level coordinates, the transition, the fixed
epsilon, the supplied topology label and the actual strict inequalities.
It does not invoke the constructor or repair submitted values.

The [focused tests](../../../../../../omega_engine_projects/finite_to_continuum/tests/test_protected_quotient_examples.py)
enumerate CRT residues through level 4, homomorphism pairs through
level 3, dyadic embedding through level 8 and sequence points through
level 100. They include rational radii as small as 10^-200 and controls
for residues, transition, image value, invalid carrier and wrong topology,
plus schema/type/boundary controls. These finite runs support the
all-level proof above; they do not certify its infinite quantifiers.

| Claim | Evidence ceiling |
| --- | --- |
| PQ-1–PQ-4 | Complete written proof and selected Lean statements; PC bridge explicitly conditional on extension correspondence |
| Hausdorff quotient and LCA specialization | Written quotient proof; classical LCA separation/biduality imported at the stated source pins |
| PQ-5 | All-level written proof; exact finite Python replay and independent mutation controls, not a Lean CRT theorem |
| PQ-6 | Actual-subspace compact-open lemmas Lean-checked; final discreteness conditional on the written classification |
| General CS→Q, native binding, physical limits | Still open; no scope promotion |

The next justified formal derivation is the missing
DyadicCharacter integer-classification declaration, followed by
instantiating the general completion-to-closed-image equivalence.
The separate native target remains an actual presentation binding to
omega_wdp::coda. PLAN-7D-LANE-E stays done only at LE-1–LE-4;
PLAN-7D-CSQ-PONTRYAGIN stays in_progress.

## 7. Verification record

The companion [verification record](protected_subgroup_verification.md)
lists exact commands, observed exit statuses, theorem census, source hashes,
dependency pins and unresolved external-anchor coverage. It verifies this
increment independently of PR #601's earlier build receipt.
