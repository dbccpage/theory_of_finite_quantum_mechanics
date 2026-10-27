<div align="center">

# Genesis, Pre-Genesis, S(n) and Witnessed Difference: Proofs of the Formalized Results

**Author:** Jeremy H. Carroll

**Date:** 2026-10-26

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Introduction

This note gives written proofs of the results of the Pre-Genesis, Genesis, S(n), MSSN and
witnessed-difference (WDP) stages that the derivation DAG (`dag/derivation_dag.json`) records as
proved in Lean. Each section states one result, proves it, and names the Lean declarations that
check it. The DAG identifier is on the line beginning *DAG node*.

The results are about finite models that the source papers declare: regimes of admitted data,
forms and instances; finite states of terms and assertions; small cochain complexes. None of them
derives these models from an inscription such as $\langle\rangle$, and where a DAG statement also
reports engine runs or censuses, those counts are computations and are not proved here. Where the
Lean covers less than the statement (a worked example, a special case, or a toy model), the
section says so.

Several results are elementary once the definitions are written out. They are included because
the DAG records them, and because the point of most of them is which hypothesis does the work.

## 1. Factorization, quotients and descent

Throughout, for maps $q:A\to V$ and $f:A\to S$, *$f$ factors through $q$* means $f=g\circ q$ for
some $g:V\to S$, and *$f$ is constant on the fibres of $q$* means $q(x)=q(y)\Rightarrow f(x)=f(y)$.

### 1.1 The quotient barrier

DAG nodes: `PG-COLLAPSE-BARRIER` `PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE` `PGW-REPLAY-NECESSITY`

**Proposition.** If $q(x)=q(y)$ and $f(x)\neq f(y)$, then $f$ does not factor through $q$. In
particular, if $\sim$ is an equivalence relation and $x\sim y$, every function on $A/{\sim}$ takes
the same value at $[x]$ and $[y]$. The same holds when $q$ is the profile map
$a\mapsto(o_i(a))_{i\in I}$ of a family of observations: two elements with equal profiles are not
told apart by any function of the profile.

*Proof.* If $f=g\circ q$ then $f(x)=g(q(x))=g(q(y))=f(y)$. For the quotient take
$q(a)=[a]$. $\square$

**Remark (the lift is not unique).** Suppose a task requires $\langle a\rangle$ and
$\langle ab\rangle$ to differ while the current regime identifies them. By the proposition, no
operation on the current quotient performs the task, so some observation $o$ with
$o(\langle a\rangle)\neq o(\langle ab\rangle)$ has to be added. Which one is not determined: under
a decoder that reads the payload as a string, "the payload has more than one position" and "the
payload contains $b$" both separate the pair, and they disagree on $\langle aa\rangle$ (true and
false respectively). Full inscription identity separates the pair as well and carries more than
one bit. A canonical tower of refinements therefore needs a declared selection policy; none is
derived here.

**Remark (replay).** Take $A$ the set of histories, $q=\pi$ the part of a history an auditor sees
and $f=\sigma$ the state it produces. If two histories look the same to the auditor and produce
different states, no auditor reports the state correctly on both. So state certification needs
replay information that separates the relevant histories; on a declared finite population, a
summary on whose fibres $\sigma$ is constant suffices (§1.2, §1.3). The audit trials of the source
illustrate this but are not an instance: the truncated window and the full replay received
different inputs.

Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean::collapsed_observation_barrier`,
`lean4/Imported/Genesis19l57g1/Paper000.lean::separation_not_on_quotient`,
`lean4/Imported/Genesis19l57g1/Derivation/Quot.lean::quotient_barrier`,
`lean4/Imported/PreGenesisToMssn/Observation.lean::collapsed_quotient_barrier`,
`lean4/Imported/Genesis19l57g1/Paper000.lean::insufficient_history_view`,
`lean4/Imported/Genesis19l57g1/Paper000.lean::no_factor_through_common_view`. The two-predicate
example is not in Lean.

### 1.2 The history and report criterion

DAG node: `PG-HISTORY-REPORT-CRITERION`

**Proposition.** Let $r:H\to V$ (the report) and $f:H\to S$ (the answer). Write
$\operatorname{im}r=\{v:\exists h,\ r(h)=v\}$.

1. There is $g:\operatorname{im}r\to S$ with $g(r(h))=f(h)$ for all $h$ if and only if $f$ is
   constant on the fibres of $r$.
2. Such a $g$ is unique.
3. Assuming a total extension $\bar g:V\to S$ of $g$ exists, it is unique if and only if $r$ is surjective or $|S|\le1$. An extension exists whenever $S$ is nonempty.

*Proof.* (1) If $g$ exists, $r(h)=r(h')$ gives $f(h)=g(r(h))=g(r(h'))=f(h')$. Conversely, for
$v\in\operatorname{im}r$ choose $h_v$ with $r(h_v)=v$ and put $g(v)=f(h_v)$. For any $h$,
$r(h)=r(h_{r(h)})$, so $f(h)=f(h_{r(h)})=g(r(h))$ by fibre constancy.

(2) Every element of $\operatorname{im}r$ has the form $r(h)$, and two such $g$ agree there.

(3) An extension is free exactly on $V\setminus\operatorname{im}r$. If that set is empty, or if
$S$ has at most one element, the assumed extension is the only one; otherwise change its value at a point off the image to obtain a second extension. If $S=\varnothing$ and $V\ne\varnothing$, no total extension exists, even though the image factor can exist when $H=\varnothing$. $\square$

The choice of $h_v$ in (1) is the only non-constructive step. In Lean it uses
`Classical.choice` for an arbitrary report; whether choice is needed for arbitrary history types
is not decided. For explicitly listed histories §1.3 avoids it.

Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean::history_report_criterion`,
`lean4/Imported/PreGenesisToMssn/Paper.lean::history_factor_unique`,
`lean4/Imported/SnMssn/Paper001.lean::exists_descent_of_constant`,
`lean4/Imported/SnMssn/Paper001.lean::descent_unique`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/Descent.lean::function_descends_iff_fiber_constant`
(the surjective case),
`lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean::factorization_iff_fiber_constancy`.
Part (3) is not in Lean.

### 1.3 A choice-free reconstruction for listed histories

DAG node: `PG-PREGEN-CONSTRUCTIVE-SUMMARY`

**Proposition.** Let $h_1,\dots,h_m$ be a list of histories and suppose equality of reports is
decidable. Define $\mathrm{recon}(v)=f(h_i)$ for the least $i$ with $r(h_i)=v$, and
$\mathrm{recon}(v)=\text{none}$ if there is no such $i$. Then $\mathrm{recon}(r(h_j))=f(h_j)$ for
every $j$ if and only if $f$ is constant on the fibres of $r$ restricted to the list.

*Proof.* If $f$ is fibre-constant on the list, the least $i$ with $r(h_i)=r(h_j)$ exists (take
$i\le j$) and $f(h_i)=f(h_j)$. Conversely, if $r(h_j)=r(h_k)$ then
$f(h_j)=\mathrm{recon}(r(h_j))=\mathrm{recon}(r(h_k))=f(h_k)$. $\square$

The search for the least index replaces the choice in §1.2, so the argument uses no axiom. It
says nothing about unlisted or infinite populations.

Lean: `lean4/Imported/OePregen/ListedHistorySummary.lean::PreMssnListed.listed_history_report_criterion`,
`lean4/Imported/OePregen/ListedHistorySummary.lean::PreMssnListed.recon_of_fiberConstant`,
`lean4/Imported/OePregen/ListedHistorySummary.lean::PreMssnListed.fiberConstant_of_recon`.

### 1.4 Refinement by a supplied tag

DAG node: `PG-REFINE-SEPARATES`

**Proposition.** Let $q:A\to O$ be a report and $t:A\to T$ a tag. The refined report
$a\mapsto(q(a),t(a))$ has first projection $q$, never identifies two elements that $q$ separates,
and separates $a,b$ whenever $t(a)\neq t(b)$. If $C$ is a set of conflicting pairs inside the
fibres of $q$, a tag with values in $\{0,1\}^b$ resolves every conflict if and only if the graph
$(A,C)$ has a proper colouring with $2^b$ colours. Hence a graph with an odd closed walk admits no
one-bit tag, and $m\ge1$ elements in pairwise conflict need $\lceil\log_2 m\rceil$ bits.

*Proof.* Pairs are equal only if both coordinates are equal, which gives the first three claims.
A tag resolves $C$ exactly when $t(a)\neq t(b)$ for $\{a,b\}\in C$, which is the definition of a
proper colouring with colour set $\{0,1\}^b$. A two-colouring alternates along a walk, so a closed
walk of odd length returns to its start with the other colour. A complete graph on $m$ vertices
needs $m$ distinct colours, so $2^b\ge m$. $\square$

Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean::refine_separates`,
`lean4/Imported/SnMssn/Paper001.lean::supplied_tag_separates`. The colouring criterion is not in
Lean, and nothing here finds a tag or bounds the cost of finding one.

### 1.5 Quotient retention

DAG node: `PGW-QUOTIENT-RETENTION`

**Proposition.** Let $\approx_f$ and $\approx_c$ be equivalence relations on $I$ with
$x\approx_f y\Rightarrow x\approx_c y$. The map $c:[x]_f\mapsto[x]_c$ is well defined and
surjective. It is injective if and only if $x\approx_c y\Rightarrow x\approx_f y$. For
$\approx_f\subseteq\approx_m\subseteq\approx_c$ the maps compose: $c_{fc}=c_{mc}\circ c_{fm}$. If
$x\approx_c y$ but not $x\approx_f y$, then $[x]_f\neq[y]_f$ and $c([x]_f)=c([y]_f)$.

*Proof.* Well defined because fine identifications are coarse ones; surjective because every
coarse class is $[x]_c=c([x]_f)$. $c([x]_f)=c([y]_f)$ means $x\approx_c y$, so injectivity says
exactly that this implies $x\approx_f y$. Both sides of the composition send $[x]_f$ to $[x]_c$.
The last claim restates the definitions. $\square$

Lean: `lean4/Imported/Genesis19l57g1/Derivation/QuotientRetention.lean::collapseMap_surjective`,
`lean4/Imported/Genesis19l57g1/Derivation/QuotientRetention.lean::collapseMap_injective_iff_reverse_refinement`,
`lean4/Imported/Genesis19l57g1/Derivation/QuotientRetention.lean::collapseMap_compose`,
`lean4/Imported/Genesis19l57g1/Derivation/QuotientRetention.lean::failed_identification_retains_two_classes`.

### 1.6 Faithful common descent and round trips

DAG node: `PGW-FAITHFUL-DESCENT-ROUND-TRIP`

**Proposition.** Let $f:P\to Q$ and $g:Q\to P$ be total translations. There are a set $C$ and
injective maps $i:P\to C$, $j:Q\to C$ with $i=j\circ f$ and $j=i\circ g$ if and only if
$g\circ f=\mathrm{id}_P$ and $f\circ g=\mathrm{id}_Q$.

*Proof.* Given $C,i,j$: $i(g(f(p)))=j(f(p))=i(p)$, and $i$ is injective, so $g(f(p))=p$;
symmetrically $j(f(g(q)))=i(g(q))=j(q)$ gives $f(g(q))=q$. Conversely take $C=P$, $i=\mathrm{id}$
and $j=g$. Then $g$ is injective because $f\circ g=\mathrm{id}$, $j\circ f=g\circ f=\mathrm{id}=i$
and $i\circ g=g=j$. $\square$

So a failed round trip for a declared pair of translations rules out a faithful common carrier
for that pair. Another pair of translations may still close.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean::faithful_descent_iff_round_trip_coherent`,
`lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean::faithful_descent_to_coherent`.

### 1.7 Lifts with a typed recovery

DAG node: `PG-OLD-IMAGE-INJECTIVE`

**Proposition.** Let $u:A\to B$ and $r:B\to A\sqcup E$ with $r(u(a))=a$ for all $a$ (the old-image
law). Then $u$ is injective. Conversely, for $E$ a one-point set every injective $u$ has such an
$r$, and for finite $A,B$ there are $(|A|+1)^{|B|-|A|}$ of them. The law does not force $r$ to
refuse points off the image of $u$.

*Proof.* $u(a)=u(b)$ gives $a=r(u(a))=r(u(b))=b$. If $u$ is injective, $r$ is determined on
$u(A)$ by the law and is arbitrary on the $|B|-|A|$ other points, each with $|A|+1$ possible
values. Taking $A=\{0\}$, $B=\{0,1\}$, $u(0)=0$ and $r(1)=0$ satisfies the law and accepts the
off-image point $1$. $\square$

The DAG statement also mentions obstruction repair; no repair notion is defined, so nothing is
proved about it.

Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean::old_image_injective`,
`lean4/Imported/SnMssn/Paper001.lean::old_image_injective`,
`lean4/Imported/SnMssn/Paper001.lean::off_image_not_implied`. The count is not in Lean.

### 1.8 Free monoids on alphabets of different sizes

DAG node: `PG-FREE-MONOID-NONISO`

**Proposition.** For finite $n\neq m$ the free monoids on $n$ and $m$ letters are not isomorphic,
and the discrete categories with $n$ and $m$ objects are not equivalent. For $n,m\ge1$ the
underlying sets of the two free monoids are in bijection.

*Proof.* In a free monoid the *atoms*, elements $w\neq1$ that are not a product of two elements
$\neq1$, are exactly the one-letter words, since a word of length $\ge2$ splits. A monoid
isomorphism preserves $1$ and products, so it maps atoms bijectively to atoms, and so gives a
bijection between the alphabets. An equivalence of discrete categories induces a bijection on
isomorphism classes of objects, which are the objects. Finally, for $n\ge1$ the free monoid is a
countably infinite set. $\square$

So a re-presentation of a numeral as an alphabet can be a bijection of sets but not an
isomorphism of the multiplication. The obstruction is the multiplicative structure, not the
cardinality.

Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean::unequal_finite_alphabets_not_iso`,
`lean4/Imported/SnMssn/Paper001.lean::no_free_monoid_iso`,
`lean4/Imported/SnMssn/Paper001.lean::no_discrete_equivalence`.

### 1.9 A chain retraction cannot kill a class

DAG node: `PG-CHAIN-RETRACTION`

**Proposition.** Let $i:C\to D$ and $r:D\to C$ be chain maps with $r\circ i=\mathrm{id}$. Then
$i_*:H(C)\to H(D)$ is injective. In two cases where an extension kills a class there is therefore
no such retraction: two isolated points joined by an edge, and a hollow triangle with its face
attached.

*Proof.* Let $z$ be a cycle of $C$ with $i(z)=\partial b$ in $D$. Then
$z=r(i(z))=r(\partial b)=\partial r(b)$, so $z$ is a boundary in $C$. For the two points the
reduced class $p_1-p_0$ becomes the boundary of the new edge; a retraction would give
$p_1-p_0=r(p_1-p_0)=r(\partial e)=\partial r(e)=0$, since $C$ has no edges. For the triangle the
cycle $e_{01}+e_{12}+e_{20}$ becomes the boundary of the face, and the same computation gives
$0$ because the hollow triangle has no 2-cells. $\square$

Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean::chain_retraction_cannot_kill`,
`lean4/Imported/PreGenesisToMssn/Homology.lean::induced_homology_injective`,
`lean4/Imported/SnMssn/Paper001.lean::homology_injective_of_chain_retraction`,
`lean4/Imported/SnMssn/Paper001.lean::two_point_retraction_impossible`,
`lean4/Imported/SnMssn/Paper001.lean::triangle_retraction_impossible`. The two cases are checked
on their coordinate vectors, not on full complexes.

### 1.10 Demand accounting

DAG node: `PG-DEMAND-ACCOUNTING`

**Proposition.** For finite sets $W$ (active demands), $D$ (discharged) and $B$ (births),
$$|(W\setminus D)\cup B| = |W|-|D|+|B|$$
in the integers if and only if $|D\setminus W| = |(W\setminus D)\cap B|$. In particular it holds
when $D\subseteq W$ and $B\cap(W\setminus D)=\varnothing$.

*Proof.* $|(W\setminus D)\cup B| = |W|-|W\cap D|+|B|-|(W\setminus D)\cap B|$ and
$|W\cap D|=|D|-|D\setminus W|$. Substitute and compare. $\square$

If exactly one of the two hypotheses fails, one side of the condition is $0$ and the other is
not, so the identity fails; if both fail the two defects can cancel. In natural-number
subtraction $|W|-|D|$ truncates at $0$ and can hide a failure of $D\subseteq W$. Births may
coincide with discharged elements.

Lean: `lean4/Imported/SnMssn/Paper001.lean::demand_accounting` (duplicate-free lists under the two
hypotheses), `lean4/Imported/PreGenesisToMssn/Paper.lean::demand_accounting` (the filter form
$|\{a\in W:\neg\mathrm{disch}(a)\}|=|W|-|\{a\in W:\mathrm{disch}(a)\}|$). The general criterion is
the written argument above.

## 2. Pointed relations and endpoints

### 2.1 Relatedness, distinctness and irreflexivity

DAG nodes: `PGW-WDP-POINTED-APARTNESS` `PG-ADMISSION-FLOOR` `PG-GEN-IRREFLEXIVE-DISTINCT` `PGW-SN-ENDPOINT-LEMMA`

**Proposition.** For a pointed relation $(X,R,a,b)$:

1. $R(a,b)$ does not imply $a\neq b$, and $a\neq b$ does not imply $R(a,b)$.
2. If $R$ is irreflexive, $R(a,b)$ implies $a\neq b$; so $|\{a,b\}|=2$ and $|X|\ge2$.
3. (Exhibited cuts.) If $R$ is irreflexive and $R(a,b)$, then no such pair exists on a
   subsingleton carrier, and for every map $q:X\to Y$ that sends $R$ into an irreflexive
   relation on $Y$, $q(a)\neq q(b)$: identifying the endpoints breaks the law.
4. In the Genesis Ongoing seed the two given names are distinct because the given assertion $arb$
   is subject to the ban on $xrx$; the reverse assertion $bra$ does not follow.
5. The count is of endpoints, not of witnesses: a witness count with one forward and no reverse
   witness is consistent.

*Proof.* (1) $X=\{a\}$, $R=\{(a,a)\}$, $b=a$; and the empty relation on two points. (2) $a=b$
would give $R(a,a)$. (3) On a subsingleton $a=b$, contradicting (2); and $q(a)=q(b)$ would give
$S(q(a),q(a))$ for the target relation $S$. (4) is (2) for the seed's legality condition, and the
relation $\{(0,1)\}$ on $\{0,1\}$ is legal, contains $arb$ and not $bra$. (5) The function
$W(0,1)=1$, $W(1,0)=0$. $\square$

Irreflexivity is therefore a declared ingredient, not a consequence of relatedness, and none of
these statements derives the relation or its law from $\langle\rangle$.

Lean:
`lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean::pointed_relation_independence_fin`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean::pointed_relation_independence`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/PrimitiveAdmissionFloor.lean::endpoints_apart`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/PrimitiveAdmissionFloor.lean::no_cut_on_subsingleton`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/PrimitiveAdmissionFloor.lean::identification_breaks_law`,
`lean4/Imported/GenesisOngoing/H3V7N5QF/Basic.lean::given_distinct`,
`lean4/Imported/GenesisOngoing/H3V7N5QF/Basic.lean::bra_not_derived`,
`lean4/Imported/PreGenesisToMssn/Paper.lean::irreflexive_endpoints`,
`lean4/Imported/OeSn/SnTheorems.lean::irrefl_witness_distinct`,
`lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean::irrefl_witness_ne`,
`lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean::single_oriented_witness_consistent`.
The census of pointed relations on carriers of size at most 3 is a computation.

### 2.2 The pointed two-element graph

DAG node: `PGW-D2-INITIAL-POINTED`

**Proposition.** Let $D_2$ have vertices $\{0,1\}$ and the single edge $0\to1$. For a relation $R$
on $X$ and a witness $R(a,b)$, the map $f(0)=a$, $f(1)=b$ preserves the edge, and it is the only
map with $f(0)=a$, $f(1)=b$. If $R$ is irreflexive, $f$ is injective.

*Proof.* The edge goes to $R(a,b)$. A map on $\{0,1\}$ is determined by its two values.
Injectivity is §2.1(2). $\square$

The map represents the chosen witness only: it says nothing about the other edges of $R$ or its
non-edges, and $D_2$ is initial among pointed structures with an asserted pair, not in a category
of all systems.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean::D2_initial_pointed`,
`lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean::irrefl_witness_ne`.

### 2.3 No point is fixed by every permutation

DAG node: `PG-WDP-PROTECTED-QUESTIONS`

**Proposition.** On a finite set $X$ with at least two elements no point is fixed by every
permutation. Call a subset $\Delta\subseteq X$ a declaration and let $G_\Delta$ be the group of
permutations fixing $\Delta$ pointwise. If $|X|\ge2$, the inclusion-minimal declarations for which
some point is $G_\Delta$-invariant are exactly the singletons. If $|X|=1$ the empty declaration
already works, and on the empty set there is no point.

*Proof.* For $x$ choose $y\neq x$; the transposition $(x\,y)$ moves $x$. Every point of $\Delta$
is $G_\Delta$-invariant, so every singleton works. The empty declaration gives the full symmetric
group, which fixes no point when $|X|\ge2$. A non-empty declaration contains a singleton, so the
minimal ones are the singletons. $\square$

So a distinguished point is not free on a bare set: its price is one declared point. This does
not say that retention or observers cannot exist. The asymmetry-price frontier of the source
(relative to an implementation class and a dependency preorder) is not formalized.

Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean::no_fully_invariant_point`
(the first claim). The pointwise-stabiliser statement is the written argument above.

## 3. The Genesis regime model

### 3.0 The model

A *regime* is $R=(n,\mathbf a,I,U,Q)$: $n$ admitted data $0,\dots,n-1$; a list $\mathbf a$ of
form arities (form $f$ has arity $a_f$); a list $I$ of instances $(f,(d_1,\dots,d_{a_f}))$; a list
$U$ of uniformly ruled forms; and a list $Q$ of imposed requirements, unordered pairs $(i,j)$ to be
separated, stored with $i\le j$ and sorted again after renaming. An instance $x=(f,\mathbf d)$ is *derivable* if $x\in I$ or $f\in U$. A *context* is
a form $f$ with slots, each a hole or a datum $<n$, with at least one hole and $a_f$ slots;
$C[d]$ fills every hole with $d$. Data $d,d'$ are *collapsed* if
$C[d]$ and $C[d']$ are both derivable or both not, for every context $C$, and *separable*
otherwise.

Events are: supply of a token (no change); admission of a datum (always incrementing the data count); admission of a form (always appending its arity, even if that arity already occurs); and admission of an instance, a uniform rule or a requirement (these three insertions deduplicate). Token-aware datum deduplication belongs to the separate model in §3.3. A *response* to $(i,j)$ is a
list $\delta$ of items (new datum, new form, new instance, new uniform rule) whose application
makes $i,j$ separable and keeps every imposed requirement separable. Regimes $R,S$ are
*isomorphic* if bijections of data and of forms preserve arities, instances, rules and
requirements.

Collapse is an equivalence relation, since it is defined by equality of the derivability
profiles $C\mapsto[C[d]\text{ derivable}]$.

### 3.1 Supply is a no-op, and supply events can be erased

DAG nodes: `PG-GEN-SUPPLY-NO-OP` `PG-GEN-SUPPLY-ERASURE`

**Proposition.** A supply event leaves the regime unchanged. Hence removing every supply event
from a history does not change its replay, and a history of supply events alone replays to its
starting regime.

*Proof.* The first claim is the definition of the step. Replay is a left fold of the step over
the history; by induction on the history, a supply step can be dropped wherever it occurs.
$\square$

Reading L (the inscription $\langle\rangle$ supplied but not admitted) and reading F
($\langle\rangle$ admitted as datum $0$) differ by one admission event, and both are kept.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::supply_no_op`,
`lean4/Imported/OeGenPrimitives/SupplyErasure.lean::GenesisPrimitives.SupplyErasure.replayE_filter_supply`,
`lean4/Imported/OeGenPrimitives/SupplyErasure.lean::GenesisPrimitives.SupplyErasure.replayE_supply_only`.
The array and source representations of `lean4/GenesisReplayRefinement.lean` restate
these for the engine's five-field encoding (for example
`lean4/GenesisReplayRefinement.lean::GenesisReplayRefinement.array_supply_erasure`);
refinement of the Python and Rust programs is not claimed.

### 3.2 Collapse without instances

DAG nodes: `PGW-COLLAPSE-WITHOUT-INSTANCES` `PGW-SN1-SUPPLY-NOT-ADMISSION`

**Proposition.** If $I=\varnothing$, every two data are collapsed, whatever the uniform rules.

*Proof.* With no instances, $C[d]$ is derivable exactly when the form of $C$ is in $U$, which does
not depend on $d$. $\square$

So at S(1), where $\langle a\rangle$ is supplied and possibly admitted, admission of a datum does
not by itself increase what can be told apart; and supply alone changes nothing (§3.1).

Lean: `lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::collapsed_of_no_insts`,
`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::supply_no_op`.

### 3.3 Challenge 0: nothing derivable, and the second token

DAG nodes: `PGW-CHALLENGE0-INERTIA-SECOND-TOKEN` `PGW-SN0-GROUND-INERTIA`

**Proposition.**

1. In a regime with no instances and no uniform rules nothing is derivable; in particular nothing
   is derivable at genesis.
2. In the token-aware model, where each datum admission carries a token and admission
   deduplicates tokens, a history whose datum admissions all carry one token $t_0$, started from
   a regime with at most that token, ends with at most one admitted datum. So a regime with two
   data needs the admission of a token different from $t_0$.
3. In the declared S(n) carrier model the ground token is written as the two characters `<>`,
   while the declared carrier at index $0$ is empty.

*Proof.* (1) Derivability needs $x\in I$ or $f\in U$. (2) By induction on the history the token
list is duplicate-free and contained in $\{t_0\}$, so its length is at most $1$. The second claim
is the contrapositive. (3) Both are definitions: the wire form of the ground token is `<>` and
the declared table has $\mathrm{carrierCard}(0)=0$. $\square$

That no successor is internally forced at Challenge 0 is a property of the declared grammar,
whose only state changes are external admissions; no forcing predicate is defined, so it is not a
theorem.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::genesis_underivable`,
`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::underivable_of_empty`,
`lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean::single_token_carrier_bound`,
`lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean::second_token_required`,
`lean4/Imported/OeSn/SnTheorems.lean::ground_presentation_vs_carrier`,
`lean4/Imported/OeSn/SnTheorems.lean::ground_carrier_empty`.

### 3.4 Challenge 2: admitted but collapsed

DAG nodes: `PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED` `PGW-SN2-OPAQUE-COLLAPSE` `PGW-CHALLENGE3-CURRENT-REGIME-FAILS`

**Proposition.** The Challenge 0 to 3 histories replay to $R_{2L}=(2,[\,],[\,],[\,],[(0,1)])$ in
reading L and $R_{2F}=(3,[\,],[\,],[\,],[(1,2)])$ in reading F. In both, every pair of data is
collapsed. Admitting a further datum to $R_{2L}$ changes the regime and leaves $0,1$ collapsed.
Hence the pair that Challenge 3 requires to be separated is not separable, and every function on
the collapse classes of $R_{2L}$ takes the same value at the classes of $0$ and $1$.

*Proof.* The replays are a direct evaluation of seven and eight events. Both regimes have no
instances, so §3.2 applies, before and after the admission of a datum. The last claim is §1.1
applied to the collapse relation. $\square$

So two externally distinct inscriptions stay internally indistinguishable, and a new external
inscription need not increase internal expressive power. A collapsed pair is an obstruction only
once a requirement or question demands that it be separated, as Challenge 3 does; a response must
then change the regime (§3.6). The source does not decompose $\langle ab\rangle$ into $a$ and $b$.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::R2L_collapsed`,
`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::R2F_collapsed`,
`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::admission_without_expressive_increase`,
`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::historyL_replays`,
`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::historyF_replays`,
`lean4/Imported/Genesis19l57g1/Derivation/Quot.lean::barrier_R2L`,
`lean4/Imported/Genesis19l57g1/Derivation/Quot.lean::quot_barrier`.

### 3.5 The number of contexts

DAG node: `PGW-CONTEXT-COUNT-FORMULA`

**Proposition.** With $n$ admitted data, a form of arity $k$ has $(n+1)^k-n^k$ contexts, so a
regime has $\sum_f\big((n+1)^{a_f}-n^{a_f}\big)$ contexts, forms with equal arity counted
separately.

*Proof.* A slot word is a word of length $k$ over the $n+1$ symbols (a hole or a datum). There
are $(n+1)^k$ words and $n^k$ of them have no hole. The Lean enumeration builds the words by
recursion on $k$: a word of length $k+1$ with a hole either starts with a hole followed by any
word of length $k$, or starts with one of the $n$ data followed by a word of length $k$ with a
hole. This gives the recursion
$c_{k+1}=(n+1)^k+n\,c_k$, $c_0=0$, whose solution is $c_k=(n+1)^k-n^k$. The two cases are
disjoint and each is duplicate-free, so the list has no repetitions. $\square$

Lean: `lean4/Imported/Genesis19l57g1/Paper.lean::contextWords_length`,
`lean4/Imported/Genesis19l57g1/Paper.lean::contextWords_mem`,
`lean4/Imported/Genesis19l57g1/Paper.lean::contextWords_nodup`. The sum over forms is the written
corollary.

### 3.6 Cost two, and the shape of the minima

DAG nodes: `PGW-SN3-COST-TWO-UNARY-MARK` `PGW-MU1-MINIMUM-NOT-UNIQUE-L` `PGW-MU1-ARITY-INDEXED-TIE-FAMILY`

**Proposition.** Let $R$ have no forms and no instances.

1. No response of at most one item separates any pair.
2. In $R_{2L}$ the unary mark $\delta_{U}=[\text{form of arity }1,\ \text{instance }(0,[0])]$ and
   the binary link $\delta_{BL}=[\text{form of arity }2,\ \text{instance }(0,[0,1])]$ are valid
   responses to $\mathrm{Separate}(0,1)$, and their results are not isomorphic.
3. More generally, for each $k\ge1$ the $k$-ary mark (a form of arity $k$ and the instance
   $(0,(1,\dots,1))$) is a valid two-item response on $R_{2L}$, and marks of different arities give
   non-isomorphic results. So the two-item minima in reading L form an infinite family.
4. Under the lexicographic cost $\mu_2=(\text{items},\ \text{sum of new-form arities})$ the
   minimum is the unary mark, unique up to isomorphism, in reading L and in reading F.

*Proof.* (1) Separation needs a derivable plugging that is not a uniform-rule plugging, hence an
instance; an instance needs a form; with no forms, one item cannot supply both.

(2) For $\delta_U$ the context $(0,[\square])$ gives $(0,[0])$, derivable, and $(0,[1])$, not. For
$\delta_{BL}$ the context $(0,[\square,1])$ gives $(0,[0,1])$, derivable, and $(0,[1,1])$, not. An
isomorphism preserves form arities, and the results have a single form of arity $1$ and $2$
respectively.

(3) The all-hole context gives $(0,(1,\dots,1))$ at $1$, derivable, and $(0,(0,\dots,0))$ at $0$,
not. Arity is preserved by isomorphisms.

(4) By (1) a minimum has two items. They must be a form and then an instance of it, and the arity
sum $\le1$ forces arity $1$ (a form of arity $0$ has no context). The instance is $(0,[d])$. In
reading L, $d\in\{0,1\}$, and the swap $0\leftrightarrow1$ is an isomorphism between the two
results that fixes the requirement $(0,1)$. In reading F the requirement is $(1,2)$, a mark at
datum $0$ leaves $1,2$ collapsed, and the swap $1\leftrightarrow2$ identifies the marks at $1$ and
at $2$. $\square$

The $\mu_2$ minimizer is a unary mark, not an edge. The counts of tied responses at item bound $2$
and arity bound $2$ (6 in 3 classes in reading L, 10 in 5 in reading F) are engine enumerations.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::cost1_insufficient_general`,
`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::mu1_minimum_not_unique`,
`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::U0_not_iso_BL`,
`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::deltaK_valid`,
`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::deltaK_length`,
`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::markK_pairwise_noniso`,
`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::mu2_unique`,
`lean4/Imported/Genesis19l57g1/Derivation/MinimalityF.lean::mu2_unique_F`. Parts (2) and (3) are
stated for $R_{2L}$ only.

### 3.7 A fresh mark always responds

DAG node: `PGW-RESPONSE-EXISTENCE-MARK-PROGRESS`

**Proposition.** Let $R$ be well formed (instances, rules and requirements refer to existing
data and forms) with every imposed requirement separable, and let $i\neq j$ be data. The delta
consisting of a new unary form $F$ and the instance $(F,[j])$ is a valid response to
$\mathrm{Separate}(i,j)$. Derivability of instances of the old forms is unchanged by it.

*Proof.* The context $(F,[\square])$ gives $(F,[j])$, derivable, and $(F,[i])$, which is not an
instance and whose form is not ruled ($F$ is new and rules refer to old forms). An instance of an
old form is derivable before the extension if and only if after, since the only new instance has
form $F$ and the rules are unchanged; and every context of an old form is still a context. So
every old separating context still separates. $\square$

This is existence of a response to a supplied demand. It does not generate demands.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/Progress.lean::mark_progress`,
`lean4/Imported/Genesis19l57g1/Derivation/Progress.lean::derivable_extend`.

### 3.8 Policy terminals separate every pair

DAG node: `PGW-POLICY-ENDPOINT-ALL-SEPARATED`

**Proposition.** Call $R$ a *policy terminal* if no collapsed pair $i<j$ of data has a valid
response. A well-formed policy terminal whose requirements are all separable separates every
distinct pair of data.

*Proof.* A collapsed pair $i<j$ would have the response of §3.7. $\square$

So an unguarded maximal run of the closure policy cannot stop on an unresolved pair for lack of a
response. A bounded implementation can still stop at a search or resource limit, which is a
different outcome.

Lean: `lean4/Imported/Genesis19l57g1/Paper.lean::policy_terminal_separates`.

### 3.9 Pruning: rules, unmentioned instances and fresh items

DAG node: `PGW-PRUNING-LEMMAS-COST-TWO`

**Proposition.**

1. Removing uniform rules preserves every separation.
2. A response containing a uniform-rule item is not minimal: removing its rule items leaves a
   valid, strictly shorter response with the same new-form arity sum.
3. Appending instances that mention neither $d$ nor $d'$ does not change whether $d,d'$ are
   collapsed.
4. In a well-formed regime, adding a fresh datum or a fresh form does not change the collapse of
   any existing pair.

*Proof.* (1) A separating context $C$ has exactly one of $C[d],C[d']$ derivable, so its form is
not ruled; with fewer rules the form is still not ruled and the instance memberships are
unchanged. (2) Applying the delta without its rule items gives the same regime with fewer rules;
by (1) the pair and the requirements stay separated; rule items carry no arity. (3) $C[d]$
mentions $d$ in every hole, so it is not among the new instances; likewise $C[d']$. (4) A context
that uses the fresh datum in a filled slot gives pluggings that no instance mentions, so both are
derivable exactly when its form is ruled; other contexts are unchanged. A fresh form appears in
no instance and no rule, so its pluggings are never derivable. $\square$

That the pruned cost-two enumeration contains every minimum is a bounded statement checked by
computation, not proved here.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/Progress.lean::separable_of_subrules`,
`lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean::rule_item_never_minimal`,
`lean4/Imported/Genesis19l57g1/Derivation/Mention.lean::collapsed_append_unmentioning`,
`lean4/Imported/Genesis19l57g1/Derivation/Mention.lean::collapsed_fresh_datum`,
`lean4/Imported/Genesis19l57g1/Derivation/Mention.lean::collapsed_fresh_form`.

### 3.10 Collapse is invariant under renaming

DAG node: `PGW-COUNT-INVARIANCE-TRANSPORT`

**Proposition.** Let $\sigma$ be a permutation of the data and $\sigma R$ the regime with
instances renamed. Then $d,d'$ are collapsed in $R$ if and only if $\sigma d,\sigma d'$ are
collapsed in $\sigma R$. The same holds under a permutation of the forms, and across any regime
isomorphism. Hence for a list $L$ of pairs the number of collapsed pairs in $L$ for $R$ equals the
number of collapsed pairs in $\sigma L$ for $\sigma R$.

*Proof.* $\sigma$ induces a bijection of contexts with $(\sigma C)[\sigma d]=\sigma(C[d])$, and an
instance $x$ is derivable in $R$ exactly when $\sigma x$ is derivable in $\sigma R$. Forms are
handled the same way. The count statement follows by counting along the bijection
$L\to\sigma L$. Requirements do not enter collapse. $\square$

Lean: `lean4/Imported/Genesis19l57g1/Derivation/CountTransport.lean::collapsed_rename`,
`lean4/Imported/Genesis19l57g1/Derivation/CountTransport.lean::collapsedCount_rename`,
`lean4/Imported/Genesis19l57g1/Derivation/IsoCollapse.lean::collapsed_transport`,
`lean4/Imported/Genesis19l57g1/Derivation/FormTransport.lean::collapsed_renameDataForm`.

### 3.11 Least-pair selection is not equivariant

DAG node: `PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR`

**Proposition.** Let $R$ have four data, one unary form and the instances $(0,[2])$, $(0,[3])$,
and let $\sigma$ be the double transposition $0\leftrightarrow2$, $1\leftrightarrow3$. Both $R$
and $\sigma R$ collapse the pair $(0,1)$, but $\sigma$ carries $(0,1)$ to $(2,3)$. On the other
hand the relation "$S$ is the result of a valid response $\delta$ to a collapsed pair $(i,j)$ of
$R$", taken over all collapsed pairs and all valid responses, is carried by $\sigma$ onto the same
relation for $\sigma R$, and so are the numbers of valid responses in a supplied candidate list and its relabelled image.

*Proof.* The only contexts are $(0,[\square])$. In $R$ neither $0$ nor $1$ gives a derivable
plugging; in $\sigma R$, whose instances are $(0,[0])$ and $(0,[1])$, both do. So $(0,1)$ is
collapsed in both, and it is the least collapsed pair in both, while $\sigma(0,1)=(2,3)$. The
transport is §3.10 applied to the pair, the delta and its result, with the inverse permutation
for the reverse inclusion. $\square$

A selection rule that picks the least index pair therefore depends on the labelling. The repair
branches once per automorphism orbit of collapsed pairs. That the two same-index choices give
non-isomorphic children is a computation.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean::least_pair_selection_not_congruent`,
`lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean::transStep_rename_fwd`,
`lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean::transStep_image_total`,
`lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean::validCount_rename`.

### 3.12 Lists and sets

DAG node: `PGW-COLLECTION-EXTENSIONALITY`

**Proposition.** If $R,S$ have the same number of data and the same form list, and their
instance, rule and requirement lists have the same members, then they agree on derivability,
contexts, collapse, separability and response validity; applying the same item or delta preserves this same-members relation between the resulting regimes.

*Proof.* Derivability is a membership test. Contexts depend only on the data count and the form
list. Collapse and separability are built from these. Admission inserts an item if it is not
already a member, which preserves equality of members. Validity is built from the previous
notions. $\square$

So two list representations of the same admitted sets cannot be told apart by these observables.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/Ext.lean::derivable_ext`,
`lean4/Imported/Genesis19l57g1/Derivation/Ext.lean::collapsed_ext`,
`lean4/Imported/Genesis19l57g1/Derivation/Ext.lean::separable_ext`,
`lean4/Imported/Genesis19l57g1/Derivation/Ext.lean::validResponse_ext`.

### 3.13 Canonical keys classify regimes

DAG node: `PGW-CANONICAL-KEY-CLASSIFICATION`

**Proposition.**

1. Let $C$ map each regime to a member of its isomorphism class, with $C(R)=C(S)$ whenever
   $R\cong S$, and let $\mathrm{enc}$ be injective. Then $\mathrm{enc}(C(R))=\mathrm{enc}(C(S))$ if
   and only if $R\cong S$.
2. For well-formed regimes with duplicate-free collections, let the canonical key be the least
   structural key over all relabellings by permutations of data and forms. It is attained, and two
   regimes have equal keys if and only if they are isomorphic. The length-prefixed encoding of the
   key as unsigned 64-bit words is injective when every encoded word, including each length prefix, is below $2^{64}$, so the same holds for the
byte encodings.

*Proof.* (1) Equal encodings give $C(R)=C(S)$, so $R\cong C(R)=C(S)\cong S$; conversely
$R\cong S$ gives $C(R)=C(S)$. (2) There are finitely many relabellings, so the minimum is
attained. If $R\cong S$, the relabellings of $S$ are those of $R$ composed with a fixed
isomorphism, so the two sets of keys are equal and so are their minima. If the keys are equal,
the two relabellings that attain them give equal sorted five-field tuples; composing one with the
inverse of the other is an isomorphism, because the tuples list the arities, instances, rules and
requirements as sets. A length-prefixed sequence of fixed-width words determines the sequence,
so the byte encoding is injective. $\square$

Lean: `lean4/Imported/Genesis19l57g1/CanonicalMinimizer.lean::key_classification`,
`lean4/Imported/Genesis19l57g1/PaperCanonical.lean::serializedRelabel_sound`,
`lean4/Imported/Genesis19l57g1/PaperWire.lean::portableBytes_injective`,
`lean4/Imported/Genesis19l57g1/PaperSearch.lean::canonicalKey_attained`,
`lean4/Imported/Genesis19l57g1/PaperSearch.lean::canonicalBytes_classification`. The optimized
Python and Rust searches are compared with this one by finite agreement, not by proof.

### 3.14 Runs do not return

DAG nodes: `PG-GEN-NO-RETURN` `PGW-C2-RUN-FORWARD-EVERY-HISTORY`

**Proposition.** Let $e(R)$ be the number of data plus the lengths of the form, instance, rule
and requirement lists. For every history of sealed events and switch markers:

1. $e$ never decreases, and it strictly increases whenever the history changes the regime;
2. no history returns to a regime once it has left it;
3. if a history leads from $s$ to $t$ and another leads from $t$ back to $s$, then $t$ has the
   regime of $s$;
4. if $a,c$ and $b,c$ are collapsed, then $a,b$ are not separable.

*Proof.* (1) Supply and switch markers keep the regime. A datum admission always increments the data count and a form admission always appends an arity, raising $e$ by one. An instance, rule or requirement admission either finds its item present and changes nothing, or appends it and raises $e$ by one. Induct over the history.
(2) If $t\neq s$ then $e(t)>e(s)$, and any later $u$ has $e(u)\ge e(t)>e(s)$. (3) By (2), if $t$
differed from $s$ the second history could not return to $s$. (4) Collapse is transitive. $\square$

The DAG node also reports 288 engine runs; that each run edge is such a history is read off the
implementation, not proved.

Lean: `lean4/Imported/Genesis19l57g1/SecondRun/Run.lean::ereplay_elems_le`,
`lean4/Imported/Genesis19l57g1/SecondRun/Run.lean::ereplay_elems_lt_of_ne`,
`lean4/Imported/Genesis19l57g1/SecondRun/Run.lean::no_return`,
`lean4/Imported/Genesis19l57g1/SecondRun/Run.lean::cycle_regime_const`,
`lean4/Imported/Genesis19l57g1/SecondRun/Run.lean::not_separable_through`.

### 3.15 Endogenous demands, exogenous payments

DAG node: `PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS`

**Proposition.**

1. A closed run from an empty requirement store, in which each round imposes one new requirement
   on a pair of existing data and admits no datum, has at most $n(n-1)/2$ rounds.
2. In the reflective chain on $0,1,\dots,n$ with tags $1,\dots,n$, for $n\ge3$ the distinct data
   $1$ and $2$ have equal depth-one profiles.
3. Let a strategy assign to each point of the chain a colour below $k$ and a view that is a
   function of the colours within radius $d$. Then the inherited obstruction fires at every large
   chain length, and the strategy does not clear it. A strategy whose view is the point's index
   (radius $0$) does clear, and it is not of this kind.

*Proof.* (1) The requirements are pairs $i<j$ of the $n$ data and each round adds a new one.
(2) Every interior point of the chain has one predecessor, one successor and a tag, so all
interior points have the same profile. (3) Interior points are pairwise obstructed by (2), which
gives firing. A view at a point far from the ends is a function of a word of $2d+1$ colours, so it
takes at most $k^{2d+1}$ values. For a chain of length $n\ge k^{2d+1}+2d+2$ there are more than
$k^{2d+1}$ interior points at distance more than $d$ from the ends, so two of them have the same
view, and the obstruction between them is not cleared. The index view separates all points, but
its colours are unbounded. $\square$

So in this model demands keep arising, and they are paid for by imports from outside: fresh data
or a non-finite declaration. The innovation counts of the sealed trees (53 and 83 unary mark
edges) are computations to a fixed depth.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean::closedRun_round_bound_from_empty`,
`lean4/Imported/Genesis19l57g1/Derivation/Generator.lean::generation_never_dries`,
`lean4/Imported/Genesis19l57g1/Derivation/G1Class.lean::g1_class_exclusion`,
`lean4/Imported/Genesis19l57g1/Derivation/G1Class.lean::clears_does_not_imply_not_fires`.

### 3.16 A proposal record confers no execution

DAG node: `PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD`

**Proposition.** A proposal record at a state $s$ consists of a block from the family of up
blocks at $s$, an embedding and a retraction that is a left inverse on represented positions,
freshness of the admitted tokens, preservation of the old asserted, retained and protected pairs
and of the pairs separated by the declared observation, the new pair (parent, next fresh
position), and a declared cost. On a halted state the block of any proposal replays to $s$
itself. On a live, store-bounded state the up proposal at a represented position is such a
record, with the identity embedding.

*Proof.* Every event is inert on a halted state, so replay of any block returns $s$. The up
proposal is a construction: its block is an up block by definition, and the identity embedding
and retraction satisfy the left-inverse and preservation fields trivially. $\square$

The record has no licence or activation field, it is one sufficient schema with no minimality
property, and its cost is a declared natural number, not a derived cost.

Lean: `lean4/Imported/Genesis19l57g1/Derivation/GraphGenesis.lean::ProposalRecord`,
`lean4/Imported/Genesis19l57g1/Derivation/GraphGenesis.lean::proposal_confers_no_execution`,
`lean4/Imported/Genesis19l57g1/Derivation/GraphGenesis.lean::upProposal`.

### 3.17 The incidence reading and its Betti numbers

DAG node: `PGW-INCIDENCE-CONSTRUCTION-BETTI`

**Proposition.** Read the admission index of a datum as a vertex, an instance of a form of arity
$k$ as a $(k-1)$-simplex on its increasing vertex list, and require an instance for every vertex
and face. For three vertices with the edges $01$, $12$, $02$ the rational Betti numbers are
$(b_0,b_1)=(1,1)$; adding the instance $012$ gives $(b_0,b_1,b_2)=(1,0,0)$.

*Proof.* $b_k=\dim C_k-\operatorname{rank}\partial_k-\operatorname{rank}\partial_{k+1}$. The edge
boundary $\partial_1$ from $\mathbb Q^3$ to $\mathbb Q^3$ has rank $2$ (its image is the
sum-zero vectors), so $b_0=3-2=1$ and, without a face, $b_1=3-2=1$. The face has boundary
$e_{12}-e_{02}+e_{01}\neq0$, so $\partial_2$ has rank $1$, $b_1=3-2-1=0$ and $b_2=1-1=0$. $\square$

The interpretation is a construction choice, not extracted from the spelling of $\langle\rangle$.
The Lean covers this three-vertex complex only; for a general face-closed family the
correspondence is a written argument.

Lean: `lean4/Imported/OeWdp/GenesisIncidence.lean::cycle_rational_betti`,
`lean4/Imported/OeWdp/GenesisIncidence.lean::filled_rational_betti`,
`lean4/Imported/OeWdp/GenesisIncidence.lean::cycle_incidence_eq`,
`lean4/Imported/OeWdp/GenesisIncidence.lean::filled_incidence_eq`.

## 4. The Genesis Ongoing seeds

### 4.0 The base seed

A state is $s=(T,A,a,b)$: a finite set $T$ of terms, a finite set $A\subseteq T\times T$ of
assertions $xry$, and two names $a,b\in T$. It is *legal* if no $xrx$ is asserted. The changes are:
add a new term; add a new assertion $xry$ with $x\neq y$; remove an asserted pair; and identify
$v$ with $u$ (rename $v$ to $u$ in $T$, $A$ and the names). The given state is
$A_0=(\{0,1\},\{(0,1)\},0,1)$, or $B_0$ with $bra$ asserted as well. The size is
$|s|=|T|+|A|$.

### 4.1 Obstruction

DAG node: `PG-GEN-ONGOING-OBSTRUCTION`

**Proposition.** In a legal state, adding $xrx$ is never legal, and identifying $v$ with $u$ is
legal if and only if neither $(u,v)$ nor $(v,u)$ is asserted. Removing the obstruction first or
last gives the same state:
$$\mathrm{id}_{u\leftarrow v}\big(s\setminus\{(u,v),(v,u)\}\big)=\mathrm{id}_{u\leftarrow v}(s)\setminus\{(u,u)\}.$$

*Proof.* Identification sends $(x,y)$ to $(x',y')$ with $v$ replaced by $u$. The image contains a
loop exactly when $(x,y)$ is a loop (excluded by legality) or $\{x,y\}=\{u,v\}$. The only pairs
mapped to $(u,u)$ are $(u,u),(v,v),(u,v),(v,u)$, and the first two are not asserted, which gives
the identity. $\square$

So the three answers to an obstructed change are: refuse it, remove the obstruction, or build
structure that avoids it.

Lean: `lean4/Imported/GenesisOngoing/H3V7N5QF/Finite.lean::identify_legal_iff`,
`lean4/Imported/GenesisOngoing/H3V7N5QF/Finite.lean::adding_xrx_always_obstructed`,
`lean4/Imported/GenesisOngoing/H3V7N5QF/Answers.lean::remove_obstruction_first_or_last`.

### 4.2 The fewest changes

DAG node: `PG-GEN-ONGOING-FEWEST-CHANGES`

**Proposition.** Put $\mathrm{miss}(x,y)=0$ if $(x,y)\in A$ and $1$ otherwise,
$\ell_A(s)=2$ if $a=b$ and $\mathrm{miss}(a,b)$ otherwise, and $\mathrm{cost}_A(s)=|s|+2\ell_A(s)$.
For a legal, well-formed state $g$ with names $a=0$ and $b\in\{0,1\}$, the fewest changes
from $A_0$ to $g$ number $\mathrm{cost}_A(g)-3$. The same holds from $B_0$ with
$\ell_B=3$ if $a=b$, $\ell_B=\mathrm{miss}(a,b)+\mathrm{miss}(b,a)$ otherwise, and the constant
$4$. Merged names stay merged along every sequence.

*Proof.* *Lower bound.* $\mathrm{cost}_A(A_0)=3$. Each change raises $\mathrm{cost}_A$ by at most
one: an addition raises the size by one and does not raise $\ell_A$ (adding $arb$ back lowers it);
a removal lowers the size by one and raises $\ell_A$ by at most one; an identification lowers the
size by at least one (two terms merge) and raises $\ell_A$ by at most one, because when $a\neq b$
and $arb$ is asserted the names cannot be identified (§4.1). So $n$ changes reach cost at most
$3+n$.

*Upper bound.* For a goal that contains the start's terms and keeps its names, remove the
assertions the goal lacks, add the missing terms and add the missing assertions; that is
$|A\setminus A_g|+|T_g\setminus T|+|A_g\setminus A|$ changes. If $g$ keeps $arb$, this is
$|g|-3$. If $a\neq b$ and $g$ lacks $arb$, it is $1+|g|-2=\mathrm{cost}_A(g)-3$. If $a=b=0$,
remove $arb$, identify $1$ with $0$, and then add: $2+(|g|-1)=\mathrm{cost}_A(g)-3$. For $B_0$ the
same count with two given assertions gives the constant $4$. Identification is the only change
that alters the names, and it maps equal names to equal names. $\square$

Lean: `lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean::fewest_changes_A`,
`lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean::reach_by_edits`,
`lean4/Imported/GenesisOngoing/H3V7N5QF/Cost.lean::Reach.names_stay_merged`. The wire and source
refinements of `lean4/GenesisOngoingRefinement.lean` (for example
`lean4/GenesisOngoingRefinement.lean::GenesisOngoingRefinement.costA_exact`)
restate the bounds for the engine encoding.

### 4.3 Every finite legal state is reachable

DAG node: `PGW-GO-REACH-CEILING`

**Proposition.** Every legal state $g$ with $T_g\supseteq T$ and the start's names is reached from
$s$ by the edit path of §4.2. The one-term state $(\{0\},\varnothing,0,0)$ is reached from $A_0$ in
two changes and from $B_0$ in three.

*Proof.* The edit path is legal at every step: removals keep legality, the added terms are new,
and the added assertions are those of the legal goal. For the one-term state, remove $arb$ (and
$bra$) and identify $1$ with $0$. $\square$

With the rewriting of §4.4 the names can be put anywhere, so every finite legal state with at
least one term is a result under either beginning. Hence no statement about the asserting that
holds in one finite legal state and fails in another follows from the seed: this is the seed's
expressive ceiling.

Lean: `lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean::reach_by_edits`,
`lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean::givenA_to_oneTerm`,
`lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean::givenB_to_oneTerm`. The Lean witnesses fix
the names at $0,1$ or $0,0$.

### 4.4 The second and third seeds: carrying maps and rewriting

DAG nodes: `PGW-GO-CONTRACTION-STEP2-STEP3` `PG-GEN-REWRITING-COMMUTATION`

**Proposition.** In the second seed (removal struck; three kinds of change) and the third
(removal and identification struck):

1. every change from $s$ to $t$ comes with a *carrying map* $q:T_s\to T_t$ sending terms to terms,
   asserted pairs to asserted pairs and names to names (the identity for an addition, the merge
   for an identification), and carrying maps compose along sequences;
2. hence an asserted obstruction persists: if $(u,v)$ is asserted in $s$ and $s$ reaches $t$,
   then $(q(u),q(v))$ is asserted in $t$;
3. every third-seed change is a second-seed change;
4. changes and sequences commute with injective rewritings $\pi$ of the terms, and the fewest
   changes from a rewriting of $A_0$ whose names agree with a legal $g$ with $a\neq b$ and $arb$ asserted number
   $|g|-3$ (and $|g|-4$ from $B_0$ when $bra$ is asserted too).

*Proof.* (1) Without removal nothing is un-asserted: an addition keeps everything and an
identification maps each asserted pair to its image. Composition of carrying maps carries.
(2) follows from (1). (3) The third seed's two kinds are kinds of the second. (4) An injective
$\pi$ preserves newness and distinctness, so it maps changes to changes. Each change raises the
size by at most one, which gives the lower bound $|g|\le n+3$; for the upper bound choose $\pi$
sending $0,1$ to the names of $g$ and add the remaining terms and assertions. $\square$

Under the base seed no carrying map exists for a removal, which un-asserts.

Lean: `lean4/Imported/GenesisOngoing/Second/Carry.lean::Step3.carries`,
`lean4/Imported/GenesisOngoing/Second/Carry.lean::Reach3.carries`,
`lean4/Imported/GenesisOngoing/Second/Carry.lean::Reach3.obstruction_persists`,
`lean4/Imported/GenesisOngoing/Third/Step.lean::Step2.toStep3`,
`lean4/Imported/GenesisOngoing/Third/Step.lean::Reach2.toReach3`,
`lean4/Imported/GenesisOngoing/Second/Rename.lean::Step3.rename`,
`lean4/Imported/GenesisOngoing/Second/Rename.lean::Reach3.rename`,
`lean4/Imported/GenesisOngoing/Second/Rename.lean::fewest_changes3_every_writing_A`,
`lean4/Imported/GenesisOngoing/Second/Rename.lean::fewest_changes3_every_writing_B`. The Lean
names run opposite to the seed numbers: `Step3` is the second seed's three-kind step.

### 4.5 The fourth seed: multiplicities only rise

DAG node: `PGW-GO-MULTIPLICITY-MONOTONE`

**Proposition.** In the fourth seed a state has terms, a multiplicity $M(x,y)\in\mathbb N$ for
each ordered pair, and names; every change adds a term or raises one $M(x,y)$, $x\neq y$, by one.
Along every sequence each multiplicity, in particular that of $arb$, is the same or higher.

*Proof.* Each change gives a containment (terms included, multiplicities pointwise $\le$, names
kept), and containment is transitive. $\square$

Taking supports gives a third-seed containment, so the third seed's conclusions hold on the
supports.

Lean: `lean4/Imported/GenesisOngoing/Fourth/Contain.lean::Reach4.mult_le`,
`lean4/Imported/GenesisOngoing/Fourth/Contain.lean::Reach4.arb_mult_le`,
`lean4/Imported/GenesisOngoing/Fourth/Contain.lean::Reach4.contains`.

### 4.6 Two relations and the swap

DAG node: `PGW-GO-TWO-RELATIONS-SWAP`

**Proposition.** In the ninth seed a state has terms and a multiplicity table for each of two
relations $r,s$. The exchange of $r$ and $s$ is an involution on states, it maps changes to
changes, and so maps a sequence of $n$ changes from $s$ to $g$ to one from $\bar s$ to $\bar g$.
A one-relation state embeds with the $s$-table zero.

*Proof.* Swapping twice is the identity. Each kind of change is defined uniformly in the relation
it acts on (a term addition or an identification acts on both tables in the same way), so its
swap is a change of the same kind. The embedding statements hold by definition. $\square$

Lean: `lean4/Imported/GenesisOngoing/Ninth/State.lean::swap9_swap`,
`lean4/Imported/GenesisOngoing/Ninth/State.lean::proj_ofR9_false`,
`lean4/Imported/GenesisOngoing/Ninth/State.lean::proj_ofR9_true`,
`lean4/Imported/GenesisOngoing/Ninth/Reach.lean::reach9_swap`.

### 4.7 Leftover feedback does not terminate

DAG node: `PGW-GO-LEFTOVER-UNBOUNDEDNESS`

**Proposition.** In the sixteenth seed a removal records a leftover and an admission returns it to
the state. If a well-formed state $s$ with at least one term reaches $t$ in $n$ changes, it
reaches $t$ in $2k+n$ changes for every $k$; and the state with one term and one assertion reaches
itself in $2k$ changes for every $k$.

*Proof.* Adding a new term and identifying it with an existing one returns a well-formed state to
itself, a cycle of two changes; prefix $k$ such cycles. Removing an assertion and admitting its
leftover returns the state and the record to what they were, another cycle of two. $\square$

These inserted cycles make the lengths of sequences reaching the same endpoint unbounded. They preserve that endpoint and do not lower the fewest changes to it; no comparison of all reachable states across different seeds follows from this padding argument.

Lean: `lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean::Reach16.unbounded`,
`lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean::admit_remove_unbounded`.

### 4.8 H1: cancellation and the excess

DAG node: `PGW-GO-H1-CANCELLATION-EXCESS`

**Proposition.** In the twenty-second seed a state is $G=(n,\mathcal A)$ with $\mathcal A$ a list
of atoms $xry$ or $xsy$ (loops allowed); results are the same when they differ by rearranging the
list or by an $xry$ and an $xsy$ asserted together. Put
$e_G(x,y)=M_r(x,y)-M_s(x,y)$.

1. For well-formed states, the generated sameness holds if and only if the two states have
   equally many terms and the same excess at every ordered pair.
2. Each result has a unique *plain* multiset of uncancelled atoms, in which no pair is asserted in both relations. Plain list states are unique only up to permutation; choosing a fixed atom order gives a canonical list representative.
3. The fewest changes from the empty state to a state the same as $G$ number
   $\Phi(G)=n+\sum_{x,y}|e_G(x,y)|$, the size of the plain state.

*Proof.* (1) Rearranging and adding a cancelling pair keep $n$ and $e$. Conversely, cancel
$xry$ against $xsy$ in each state until one relation is absent at each pair; what remains, the
plain part, is determined by $e$ ($|e(x,y)|$ copies of the atom of sign $e(x,y)$), so equal $e$
gives equal plain parts. (2) is the cancelled state. (3) $\Phi$ is constant on results, $\Phi(\varnothing)=0$, and each
change raises $\Phi$ by at most one (an addition or removal changes the excess norm by at most one; an identification removes a term and combines excesses, whose total absolute value cannot increase by the triangle inequality), which gives the lower bound. Adding $n$ terms and the atoms of the plain state reaches it in $\Phi(G)$
additions. $\square$

Here an addition can undo an addition (adding $xsy$ cancels $xry$), so the ninth seed's no-return
for additions does not survive. The result counts for the unchosen readings are computations.

Lean: `lean4/Imported/GenesisOngoingCore/Twentysecond/Same.lean::same_iff_excess`,
`lean4/Imported/GenesisOngoingCore/Twentysecond/Same.lean::gen_iff_same`,
`lean4/Imported/GenesisOngoingCore/Twentysecond/Plain.lean::plain_reduced`,
`lean4/Imported/GenesisOngoingCore/Twentysecond/Cost.lean::fewest_changes`.

### 4.9 H2: raising and the gauge

DAG node: `PGW-GO-H2-STATE-RAISING-GAUGE`

**Proposition.** In the twenty-third seed, raising a term $x$ adds $xry$ and $ysx$ for every other
term $y$, and results differing by raising are the same.

1. Raising $x$ changes the excess by $[u=x]-[v=x]$ at $(u,v)$.
2. Two well-formed states are the same if and only if they have equally many terms and
   $e_G(x,y)=e_H(x,y)+g(x)-g(y)$ for some $g:\{0,\dots,n-1\}\to\mathbb Z$.
3. The loops $e(x,x)$, the two-way sums $e(x,y)+e(y,x)$ and the sums around three terms
   $e(x,y)+e(y,z)+e(z,x)$ are invariants, and $G$ is the same as the state asserting nothing if
   and only if all of them vanish.
4. Adding a term does not respect the sameness: $G=(2,\varnothing)$ is the same as the state $H$
   with $0r1$ and $1s0$, but no change of $H$ is the same as the change of $G$ that adds a term.

*Proof.* (1) The atoms $xry$ add $1$ at $(x,y)$ and $ysx$ subtract $1$ at $(y,x)$, for $y\neq x$.
(2) By (1) raising $x$ shifts $e$ by the gauge of the indicator of $x$, and its inverse by minus
that; §4.8(1) handles the cancellation. Conversely raise each $x$ by $g(x)$ (or its inverse) and
apply §4.8(1). (3) The three quantities are unchanged by $g(x)-g(y)$. If $n=0$, the empty gauge suffices. Otherwise, if the invariants vanish, put
$g(x)=e(x,0)$; the sum around $(x,y,0)$ and the two-way sum at $(0,x)$ give
$e(x,y)=e(x,0)-e(y,0)=g(x)-g(y)$. (4) $H$ has $e(0,1)=1=g(0)-g(1)$ with $g=(1,0)$. The change of
$G$ to $(3,\varnothing)$ must be matched by a change of $H$ with three terms, which can only add a
term; the result needs $g(0)-g(1)=1$, $g(0)=g(2)$ and $g(1)=g(2)$, which is impossible. $\square$

Lean: `lean4/Imported/GenesisOngoingCore/Twentythird/Raise.lean::excess_raise`,
`lean4/Imported/GenesisOngoingCore/Twentythird/Same.lean::gen3_iff_same3`,
`lean4/Imported/GenesisOngoingCore/Twentythird/Nothing.lean::Same3.around`,
`lean4/Imported/GenesisOngoingCore/Twentythird/Nothing.lean::same3_nothing_iff`,
`lean4/Imported/GenesisOngoingCore/Twentythird/Nothing.lean::step_of_same3_fails`.

### 4.10 H3: fills and holonomy

DAG node: `PGW-GO-H3-TWIN-FILLS-HOLONOMY`

**Proposition.**

1. (Twenty-fourth seed.) A filled term $x$ balances, $M_r(x,x)=M_s(x,x)$, exactly when
   $e(x,x)=0$; this is the same for every state of a result. A result is told apart from the one
   asserting nothing on the same filled terms exactly when some filled term does not balance.
2. (Twenty-fifth seed.) A filled triple $(x,y,z)$ balances when $e(x,y)+e(y,z)+e(z,x)=0$, which
   the sameness keeps, and every triple balances in a state the same as the one asserting
   nothing. A result is told apart exactly when some filled triple does not balance.
3. With three terms, both orientations of the triple $0,1,2$ balance if and only if the triple
   $(0,1,2)$ balances and the three two-way sums add up to zero.
4. If every loop and every two-way sum vanishes, the triples through one fixed term $c$ decide:
   if they all balance, $G$ is the same as the state asserting nothing.

*Proof.* (1) The loop excess is gauge invariant, since $g(x)-g(x)=0$. The record of the state
asserting nothing marks every filled term as balanced, so the records differ exactly at a filled
term with $e(x,x)\neq0$. (2) The sum around is gauge invariant (§4.9(3)) and zero for the empty
state; the record argument is the same. (3) The sums around $(0,1,2)$ and $(0,2,1)$ add up to the
total of the two-way sums. (4) Put $g(x)=e(x,c)$. Balance of $(c,x,y)$ and the vanishing two-way
sums give $e(x,y)=e(x,c)-e(y,c)$; the cases where $x$, $y$ or $c$ coincide follow from the loops
and two-way sums. Then apply §4.9(2). $\square$

The rank counts of the sums around filled triples modulo raising (2 of 7 dimensions at three
terms, 7 of 13 at four, 16 of 21 at five) come from a scratch computation and are not proved here.

Lean: `lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean::balances_iff`,
`lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean::told_iff`,
`lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean::nothing_balanced`,
`lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean::told_iff`,
`lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean::blind_three_iff`,
`lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean::cone_decides`.

## 5. The S(n) carrier

### 5.1 The restricted lift and its retraction

DAG nodes: `PG-SN-CARRIER` `PG-SN-OFF-IMAGE-REFUSAL` `PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL`

**Proposition.** Over a glyph alphabet $G$ with $g$ letters, the base presentations are the
ground token, a supplied mark $m$, and a pair, a cut or a simplex on two glyphs, so there are
$1+g+3g^2$ of them. The section lift $s_n$ sends them at stage $n$ to the glyph bodies
$[\,]$, $[m]$, $[f,s]$, to an arrow and to a pair. The retraction $r_n$ accepts a lift exactly
when its stage is $n$ and its body has one of these five shapes.

1. $r_n(s_n(b))=b$ for every $b$ (the old-image law), so $s_n$ is injective and its image has
   $1+g+3g^2$ elements at every stage.
2. $r_n(p)$ accepts $q$ only if $p=s_n(b)$ and $q=b$ for some $b$; $r_n$ refuses $p$ if and only if
   $p$ is off the image of $s_n$; a lift at stage $m\neq n$ is refused; and image membership is a
   syntactic test.
3. The declared table $\mathrm{carrierCard}=(0,1,2,2,4,5,6,\dots)$ differs from $1+g+3g^2$ at
   stages $0,2,3$ for every $g$, and at stage $1$ unless $g=0$. The carrier at index $0$ is empty.
4. The unrestricted lift, which also sends the refusal token to the ground body, is not injective,
   has no recovery satisfying the old-image law, and sends the refusal token back as the ground
   presentation.

*Proof.* (1) Evaluate $r_n$ on each of the five shapes. Injectivity follows as in §1.7, and an
injective map preserves cardinality. (2) Read the definition of $r_n$: it returns `accepted` only
in the five shape cases at stage $n$, and each case is the image of exactly one base
presentation. (3) $1+g+3g^2\ge1$, so it is never $0$; it equals $1$ only for $g=0$; and
$g+3g^2=1$ has no solution in $\mathbb N$. (4) The ground token and the refusal token have the
same image; a recovery would make the lift injective (§1.7). $\square$

The refusal in (2) comes from the soundness of the retraction, not from the old-image law, which
does not refuse (§1.7). The table in (3) is a declaration with no theorem tying it to the lift.

Lean: `lean4/Imported/PreGenesisToMssn/SnCarrier.lean::BasePresentation`,
`lean4/Imported/PreGenesisToMssn/SnCarrier.lean::sectionLift`,
`lean4/Imported/PreGenesisToMssn/SnCarrier.lean::retractionDownMap`,
`lean4/Imported/PreGenesisToMssn/SnTheorems.lean::old_image_base`,
`lean4/Imported/PreGenesisToMssn/SnTheorems.lean::ground_carrier_empty`,
`lean4/Imported/OeSn/SnOffImage.lean::SnOffImage.nonDescent_iff_off_image`,
`lean4/Imported/OeSn/SnOffImage.lean::SnOffImage.accepted_only_from_section`,
`lean4/Imported/OeSn/SnOffImage.lean::sectionLift_injective`,
`lean4/Imported/OeSn/SnOffImage.lean::retraction_stage_strict`,
`lean4/Imported/OeSn/SnOffImage.lean::inImage_iff`,
`lean4/SnCarrierPfp.lean::card_image_sectionLift`,
`lean4/SnCarrierPfp.lean::table_ne_base_stage_two`,
`lean4/SnCarrierPfp.lean::table_eq_base_stage_one_iff`,
`lean4/SnCarrierPfp.lean::unrestricted_lift_not_injective`,
`lean4/SnCarrierPfp.lean::refusal_token_round_trip_changes_input`.

### 5.2 The obligation monoid

DAG node: `PG-OBLIGATION-MONOID`

**Proposition.** Obligation vectors $\mathbb N^k$ under pointwise addition form the free
commutative monoid on $k$ generators; it is cancellative and, for $k\ge1$, not a group. With a
bound $N$ on each count, the partial sum defined when the result is $\le N$ is associative, with
the same definedness for both bracketings. The trace of an event list, summing a fixed vector per
event, is a monoid homomorphism from lists under concatenation; a trace that adds at least one
term and at least one assertion has total cost at least $2$.

*Proof.* Every vector is uniquely $\sum_i v_ie_i$, which is freeness; $\mathbb N$ is cancellative
and $e_1$ has no inverse. For the bounded sum, $(x+y)+z$ is defined iff $x+y\le N$ and
$x+y+z\le N$, which, since $x+y\le x+y+z$, is iff $x+y+z\le N$; the same holds for $x+(y+z)$. The
trace of a concatenation is the sum of the traces by induction on the first list. The cost floor
is $1+1$. $\square$

The Lean covers the three-counter trace homomorphism and the cost floor, for a copy of the
source's event table. That Genesis events or S(n) maps carry obligation vectors as monoid
morphisms is not established.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.traceObligation_append`,
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.declare_then_assert_cost_floor`.

### 5.3 The complex balancing map as a representation quotient

DAG node: `PGW-SN-REPRESENTATION-QUOTIENT`

**Proposition.** Over $\mathbb Q$, let $T(r_r,r_i,i_r,i_i)=(r_r-i_i,\ r_i+i_r)$, the coefficient map of
$(x_1+iy_1)\otimes(x_2+iy_2)\mapsto(x_1+iy_1)(x_2+iy_2)$. Then $TT^{\mathsf T}=2I_2$, the map
$P=\tfrac12T^{\mathsf T}T$ is a rank-2 idempotent, and $\ker T=\{r_r=i_i,\ r_i=-i_r\}$, which
contains $(1,0,0,1)$; so $P\neq I_4$.

*Proof.* $T^{\mathsf T}(x,y)=(x,y,y,-x)$ and $T$ of this is $(2x,2y)$. Then
$(T^{\mathsf T}T)^2=T^{\mathsf T}(TT^{\mathsf T})T=2T^{\mathsf T}T$, and the rank of $P$ is that of
$T$, which is $2$. The kernel is read off the two coordinates. $\square$

With $u=T^{\mathsf T}/2$ and $r=T$, $ru=I_2$ while $ur=P$: the declared questions that survive are
those factoring through $T$. This supplies no native S(n) obstruction.

Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean::balance_section`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean::balance_kernel_iff`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean::twice_project_square`
(integer coefficients; the division by $2$ is the written step).

## 6. Cochains, circulation and the obstruction calculus

A *window* is a sequence $C^0\xrightarrow{d_0}C^1\xrightarrow{d_1}C^2$ of finite-dimensional
spaces over $\mathbb Q$ (or abelian groups) with $d_1d_0=0$. A 1-cochain $h$ records edge data;
$h$ is *repairable* if $h\in\operatorname{im}d_0$. Put $Q^1=C^1/\operatorname{im}d_0$,
$H^1=\ker d_1/\operatorname{im}d_0$, and for weights $\omega_e>0$
$$\Phi_1(h)=\min_\alpha\sum_e\omega_e\,|h_e-(d_0\alpha)_e|,\qquad \Gamma_2(h)=\|d_1h\|_1 .$$

### 6.1 The triangle circulation

DAG nodes: `PGW-SN-E12-CIRCULATION-FUNCTIONAL` `PGW-MSSN-CIRCULATION-OBSTRUCTION`

**Proposition.** On the oriented triangle $a\to b\to c\to a$ with $d_0g=(g_b-g_a,\ g_c-g_b,\ g_a-g_c)$
over $\mathbb Z$, put $I(x)=x_{ab}+x_{bc}+x_{ca}$. Then $\operatorname{im}d_0=\ker I$, $I$ is
invariant under adding a coboundary, and $C^1/\operatorname{im}d_0\cong\mathbb Z$. The record
$x=(1,0,0)$ has $I(x)=1$, so no potential realizes it.

*Proof.* $I(d_0g)=0$ by telescoping. If $I(x)=0$, the potential $g=(0,\ x_{ab},\ x_{ab}+x_{bc})$
gives $d_0g=(x_{ab},x_{bc},-x_{ab}-x_{bc})=x$. $I$ is onto $\mathbb Z$, since $I(1,0,0)=1$, so it
induces the isomorphism. $\square$

On the open path $a\to b\to c$ the potential $(0,1,1)$ realizes the first two records of
$(1,0,0)$ and predicts $-1$ on $ca$. The MSSN detector's active-obstruction predicate is by
definition the conjunction of four gates (retained, protected, observation declared, declared
observation not separating); that factorization is a definitional identity.

Lean: `lean4/Imported/PreGenesisToMssn/Cochain.lean::triangle_repair_exact_iff`,
`lean4/Imported/PreGenesisToMssn/Cochain.lean::triangle_repair_invariant`,
`lean4/Imported/OeMssn/MssnObstructionDetector.lean::cycle_circulation_coboundary_vanishes`,
`lean4/Imported/OeMssn/MssnObstructionDetector.lean::circulation_flux_obstruction`,
`lean4/Imported/OeMssn/MssnObstructionDetector.lean::no_scalar_potential_for_unit_flux`,
`lean4/Imported/OeMssn/MssnObstructionDetector.lean::obstP_factors`,
`lean4/Imported/OeMssn/MssnObstructionDetector.lean::obst_of_gates`. The rational case is the same
argument.

### 6.2 Weighted $\ell^1$ duality

DAG nodes: `PGW-SN-E08-WEIGHTED-L1-DUALITY` `L1-FRAMEWORK-KKT-CERT`

**Proposition.** For a finite matrix $d_0$ over $\mathbb Q$, rational weights $\omega\ge0$ and a rational cochain $c$ (with rational optimization variables),
$$\min_g\sum_e\omega_e|c_e-(d_0g)_e| \;=\; \max\{c^{\mathsf T}y:\ d_0^{\mathsf T}y=0,\ |y_e|\le\omega_e\},$$
both attained. A primal $g$ and a dual $y$ with equal values are both optimal. On the unit-weight
oriented 3-cycle with $c=(1,0,0)$ the optimum is $1$, attained by $g=(0,0,0)$ and $g=(0,1,1)$ with
different residuals $(1,0,0)$ and $(0,0,1)$, while the $\ell^2$ (harmonic) residual is
$(1/3,1/3,1/3)$.

*Proof.* *Weak duality.* If $d_0^{\mathsf T}y=0$ then $y^{\mathsf T}d_0g=0$, so
$c^{\mathsf T}y=\sum_ey_e(c-d_0g)_e\le\sum_e\omega_e|c-d_0g|_e$. *Strong duality.* Write the
primal as the linear programme in $(g,t)$ minimizing $\sum\omega_et_e$ subject to
$\pm(c-d_0g)_e\le t_e$; it is feasible and bounded below by $0$, so linear-programming duality
(from Farkas' lemma) gives a dual optimum of the same value, and the dual is the displayed
problem. For the 3-cycle, $y=(1,1,1)$ is dual feasible with value $1$, and the two potentials
have cost $1$. The harmonic potential $(0,2/3,1/3)$ has $d_0g=(2/3,-1/3,-1/3)$. $\square$

The weak-duality step is the optimality certificate used for $\ell^1$ residuals: if
$d_0^{\mathsf T}y=0$, $|y_e|\le\omega_e$ and $\sum_e\omega_e|r_e|=c^{\mathsf T}y$, then $r$ has
the least weighted $\ell^1$ norm in the class $c-\operatorname{im}d_0$, because every member $x$
of the class has $c^{\mathsf T}y=y^{\mathsf T}x\le\sum_e\omega_e|x_e|$.

So an $\ell^1$ minimizer need not be unique and need not be the harmonic residual. The source
also defines a categorical adjunction; the pair $d_0,d_0^{\mathsf T}$ is not one, and nothing here
is claimed about adjunctions.

Lean: `lean4/WeightedL1Duality.lean::weighted_l1_strong_duality`,
`lean4/WeightedL1Duality.lean::e08_rational`,
`lean4/WeightedL1Duality.lean::lp_strong_duality`,
`lean4/WeightedL1Duality.lean::farkas`,
`lean4/WeightedL1Duality.lean::certificate_optimal`,
`lean4/WeightedL1Duality.lean::cyc_optimum`,
`lean4/WeightedL1Duality.lean::cyc_residuals_differ`,
`lean4/WeightedL1Duality.lean::cyc_harmonic`,
`lean4/WeightedL1Duality.lean::adjunctionCochain_not_cycD_transpose`.
`lean4/Imported/L1ObstructionFramework/lp_general_certificate.lean::general_finite_certificate_optimality`
states the certificate over integer lists, with an arbitrary coboundary map in place of $d_0$.

### 6.3 The exact sequence of the closure charge

DAG nodes: `PGW-WDP-EXACT-SEQUENCE-H1-Q1` `PG-WDP-QUOTIENT-EXACT-SEQUENCE`

**Proposition.** In a window, $\kappa^1([h])=d_1h$ is well defined on $Q^1$, and
$$0\to H^1\to Q^1\xrightarrow{\kappa^1}\operatorname{im}d_1\to0$$
is exact; a class has zero charge exactly when every representative is closed. Over a field,
$\dim Q^1=\dim H^1+\dim\operatorname{im}d_1$, and:

1. if $\dim H^1>0$ and $\dim\operatorname{im}d_1>0$, no linear section of $\kappa^1$ is invariant under
   all the automorphisms $1+\iota f\kappa^1$, with linear $f:\operatorname{im}d_1\to H^1$, which act freely
   on linear sections; if either dimension is $0$, the linear section is unique;
2. for a definite norm $J$ with attained minimum, $\min_\alpha J(h+d_0\alpha)=0$ if and only if
   $[h]=0$ (false for a seminorm);
3. for weighted $\ell^1$ with attained minimum, $\Gamma_2(h)\le c\,\Phi_1(h)$ whenever
   $c\ge\max_e\omega_e^{-1}\sum_f|(d_1)_{fe}|$, so, whenever $\Phi_1(h)>0$, the closure ratio $\Gamma_2/\Phi_1$ is at most $c$. When $\Phi_1(h)=0$, the inequality instead implies $\Gamma_2(h)=0$, without forming a quotient.

*Proof.* $d_1(h+d_0\alpha)=d_1h$, so $\kappa^1$ is well defined. Its kernel is
$\ker d_1/\operatorname{im}d_0=H^1$, it maps onto $\operatorname{im}d_1$, and the inclusion of
$H^1$ is injective. Rank–nullity gives the dimension count. (1) If $s$ is a linear section, so is
$(1+\iota f\kappa^1)s=s+\iota f$, which equals $s$ only for $f=0$; when both dimensions are
positive a nonzero $f$ exists. If $\operatorname{im}d_1=0$ the only section is $0$, and if
$H^1=0$, $\kappa^1$ is invertible. (2) A definite norm vanishes only at $0$, so a zero minimum
means some representative is $0$. (3) $d_1h$ does not depend on the representative; for a
minimizing representative $h'$,
$\|d_1h'\|_1\le\sum_e|h'_e|\sum_f|(d_1)_{fe}|\le c\sum_e\omega_e|h'_e|=c\,\Phi_1(h)$. $\square$

The splitting $Q^1\cong H^1\oplus\operatorname{im}d_1$ exists in finite dimension but needs a
chosen linear section, and (1) says it is not canonical with respect to these automorphisms of the
extension. Naturality for automorphisms of the window is not covered.

Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::kappa_well_defined`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::kappa_exact_sequence`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::kappa_mk`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::closure_ratio_le_opnorm`,
`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::closure_ratio_nonneg`.
The Lean exactness is set-level on the literal quotient; the dimension count, (1) and (2) are the
written argument.

### 6.4 Growth does not repair

DAG node: `PG-WDP-GROWTH-NO-REPAIR`

**Proposition.** Let a sub-window have $d_0$ equal to the restriction of the big window's $d_0$
(each sub-edge's coboundary involves only sub-vertices), the restricted cochain, and weights at
most the restricted weights. If the minima are attained, $\Phi_1(\mathrm{sub})\le\Phi_1(\mathrm{big})$.
Attaching a 2-cell whose row $\rho$ satisfies $\rho d_0=0$ leaves $\Phi_1$ unchanged and adds
$|\rho\cdot h|$ to $\Gamma_2$.

*Proof.* Let $\alpha$ minimize for the big window and restrict it to the sub-vertices. On each
sub-edge the residual is unchanged, and the sub-window sums fewer non-negative terms with smaller
weights, so its cost at $\alpha|$ is at most $\Phi_1(\mathrm{big})$. A 2-cell changes only $d_1$,
so $d_0$, $\omega$ and $h$, and hence $\Phi_1$, are unchanged, while $\|d_1h\|_1$ acquires the new
coordinate. $\square$

So growth with an extending cochain and weights not lowered never lowers $\Phi_1$; a decrease
needs deleted cells, lowered weights, or a changed $d_0$ or cochain. The Lean declarations are a
sum inequality for lists of natural numbers and a definitional equality for the 2-cell; the
statement above is the written argument.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.wdp_growth_subcomplex_monotone`,
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.wdp_two_simplex_attachment_preserves_phi1`.

### 6.5 The filled triangle

DAG node: `PGW-WDP-FILLED-TRIANGLE`

**Proposition.** On vertices $0,1,2$, edges $(01,12,02)$ and one face, with
$d_0f=(f_1-f_0,\ f_2-f_1,\ f_2-f_0)$, $d_1x=x_{01}+x_{12}-x_{02}$ and unit weights, the cochain
$\delta=(1,1,0)$ has $\Phi_1=2$, attained at $f=(0,1,0)$, and $\Gamma_2=2$. The operator norm
$\|d_1\|_{1\to1}$ is $1$, and the closure ratio $\Gamma_2/\Phi_1=1$ meets the bound of §6.3(3).

*Proof.* $d_1d_0f=(f_1-f_0)+(f_2-f_1)-(f_2-f_0)=0$. The vector $y=(1,1,-1)$ satisfies
$y\cdot d_0f=0$ and $|y_e|\le1$, and $y\cdot\delta=2$, so $\Phi_1\ge2$ by weak duality (§6.2). At
$f=(0,1,0)$, $d_0f=(1,-1,0)$ and the residual is $(0,2,0)$, of mass $2$. $d_1\delta=2$. Each column
of $d_1$ has absolute value $1$, so $|d_1x|\le\|x\|_1$, with equality at $x=e_{01}$. $\square$

Without the face, $C^2=0$ and $\Gamma_2=0$: the cyclic cochain with value $1$ on each edge
oriented around the cycle, $(1,1,-1)$ in these coordinates, has $\Phi_1=3$ (certificate
$(1,1,-1)$, attained at $f=0$). Filling the triangle turns it into closure charge
$|1+1+1|=3$ without changing $\Phi_1$. These hollow-case numbers are not in Lean.

Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::filled_triangle_signature`.
