<div align="center">

# Computation in the Finite Models: Proofs of the Formalized Results

**Author:** Jeremy H. Carroll

**Date:** 2026-10-26

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Introduction

This note gives written proofs of the COMPUTATION-stage results that the derivation DAG
(`dag/derivation_dag.json`) records as proved in Lean. Each section states one result, proves
it, and names the Lean declarations that check it. The DAG identifier is on the line beginning
*DAG node*.

There are three groups. Section 1 shows that word rewriting over admitted marks simulates Turing
machines, so that reachability questions in the Genesis-style rewriting regimes are undecidable
in general and decidable under a length bound. Section 2 treats simple models of the viability
of fault-tolerant quantum computation: a repair queue, concatenated error recurrences, and the
contraction of distances under depolarizing noise. Section 3 treats the authorization models:
when a report or a terminal verdict can decide a validity predicate. Many results in Section 3
are about two- or four-element fixtures, and their proofs are evaluations; they are included
because the DAG records them, and the point is which hypothesis fails in each fixture.

Results that rest on Mathlib's computability library (Kleene's universal function, the
TM2→TM1→TM0 compilers, the undecidability of the halting problem) are cited as such; the proofs
here say how they are combined.

## 1. Rewriting over marks and Turing machines

### 1.0 Words and rules

A *rule* is a pair of words $(l,r)$ over an alphabet of marks. A *step* $w\to w'$ replaces an
occurrence of $l$ by $r$: $w=u\,l\,v$ and $w'=u\,r\,v$. *Reach* is the reflexive–transitive
closure, and a word is *irreducible* if no step applies to it. A *bounded* step also requires
both words to have length at most $L$, and *bounded reach* is the closure of bounded steps.

### 1.1 A separated alphabet of any size

DAG node: `COMP-C1-CANONICAL-SEPARATED-ALPHABET`

**Proposition.** Say that data $i,j$ are *unarily separated* in a regime if some unary form has an
instance at exactly one of $i,j$. In the regime with $n$ data, $n-1$ unary forms and the
instances $(i,[i])$ for $i<n-1$, every two distinct data are unarily separated. Two data with no
forms are not.

*Proof.* For $i\neq j$ at most one of them equals $n-1$; if $i<n-1$ then form $i$ has the
instance $(i,[i])$ and not $(i,[j])$, and symmetrically. With no forms there is nothing to
separate by. Unary separation is a finite search over forms and instances, hence decidable.
$\square$

So $n$ marks can be admitted and told apart at the cost of $n-1$ forms and $n-1$ instances.

Lean: `lean4/GenesisComputation.lean::canonicalRegime_pairwise`,
`lean4/GenesisComputation.lean::two_marks_without_forms_collapsed`,
`lean4/GenesisComputation.lean::unarySep_iff`,
`lean4/GenesisComputation.lean::pairwiseSeparated_iff`.

### 1.2 Renaming letters commutes with rewriting

DAG node: `COMP-C2-LETTER-RENAME-COMMUTES`

**Proposition.** For a letter map $f$, a step $w\to w'$ under rules $R$ gives a step
$f(w)\to f(w')$ under the image rules $f(R)$, and so for reach. If $f$ is injective, every step
from $f(w)$ under $f(R)$ is the image of a step from $w$, and a reach from $f(w)$ to $f(w')$ comes
from a reach from $w$ to $w'$.

*Proof.* $f$ acts letter by letter, so $f(u\,l\,v)=f(u)f(l)f(v)$. Conversely, if
$f(w)=u'\,f(l)\,v'$ then, cutting $w$ at the positions $|u'|$ and $|u'|+|l|$, $w=u\,l_0\,v$ with
$f(u)=u'$, $f(l_0)=f(l)$ and $f(v)=v'$; injectivity of $f$ on letters gives $l_0=l$, and the
result of the step is $f(u\,r\,v)$. Induct along the reach. $\square$

Lean: `lean4/GenesisComputation.lean::Step.map`, `lean4/GenesisComputation.lean::Reach.map`,
`lean4/GenesisComputation.lean::Reach.of_map`,
`lean4/GenesisComputation.lean::Step.exists_of_map`,
`lean4/GenesisComputation.lean::Reach.exists_of_map`.

### 1.3 One-hole contexts are word contexts

DAG node: `COMP-C2-ONE-HOLE-CONTEXTS`

**Proposition.** A Genesis context (a tuple of slots, each a hole or a letter) has exactly one
hole if and only if it is $u\,\square\,v$ for letter lists $u,v$, and $u,v$ are then unique.
Plugging $d$ into it gives $u\,d\,v$. So the one-hole contexts of arity $a$ are the pairs $(u,v)$
with $|u|+|v|=a-1$.

*Proof.* Cut the tuple at its unique hole. Two such decompositions of one tuple have the hole at
the same position, so the prefixes and suffixes agree. Plugging replaces the hole. $\square$

Lean: `lean4/GenesisComputation.lean::oneHole_iff_split`,
`lean4/GenesisComputation.lean::ofSplit_injective`,
`lean4/GenesisComputation.lean::plug1_ofSplit`,
`lean4/GenesisComputation.lean::holes_ofSplit`,
`lean4/GenesisComputation.lean::plug1_ofSplit_eq_plug`.

### 1.4 Bounded reach is decidable, and the three-valued verdict is sound

DAG nodes: `COMP-C3-BOUNDED-REACH-DECIDABLE` `COMP-C3-VERDICT-SOUND`

**Proposition.** Fix $k$ marks, a finite rule list and a bound $L\ge|a|$.

1. There are $\sum_{i=0}^{L}k^i$ words of length at most $L$, and the bounded successors of a
   word are computed from the rule list.
2. Bounded reach from $a$ is decided by iterating the successor map at most that many times.
3. Define the verdict on $(a,b)$: *reachable* if $b$ is in the bounded reach set of $a$;
   otherwise *unreachable* if the set is *closed* (no step from it leaves length $L$); otherwise
   *bound exceeded*. Then *reachable* implies reach, *unreachable* implies no reach at any
   length, and *bound exceeded* comes with a word of the set and a step from it to a word longer
   than $L$.
4. Every reach is a bounded reach for some bound.

*Proof.* (1) Count words by length. For each occurrence of a left side in $w$ there is one
successor. (2) Let $U$ be the finite set of words of length $\le L$; it is closed under bounded
successors. The sets $S_0=\{a\}$, $S_{m+1}=S_m\cup\mathrm{succ}(S_m)$ increase inside $U$, so they
are constant from $m=|U|$ on, and their union is the reach set. (3) A bounded reach is a reach.
If the set is closed, induction along any reach shows that it never leaves the set, so a word
outside it is not reachable. If it is not closed, the failure of closure is the witness. (4) Take
$L$ the largest length along the path. $\square$

Lean: `lean4/GenesisComputation.lean::reachB_iff`,
`lean4/GenesisComputation.lean::decideReachB_iff`,
`lean4/GenesisComputation.lean::card_wordsLE`,
`lean4/GenesisComputation.lean::mem_succList`,
`lean4/GenesisComputation.lean::reachSet_card_le`,
`lean4/GenesisComputation.lean::rtg_iff_mem_reachN_card`,
`lean4/GenesisComputation.lean::verdict_reachable_sound`,
`lean4/GenesisComputation.lean::verdict_unreachable_sound`,
`lean4/GenesisComputation.lean::verdict_boundExceeded_witness`,
`lean4/GenesisComputation.lean::closed_reach`,
`lean4/GenesisComputation.lean::reach_iff_reachB_of_closed`,
`lean4/GenesisComputation.lean::Reach.exists_bound`,
`lean4/GenesisComputation.lean::ReachB.reach`.

### 1.5 A machine that needs unboundedly many blanks

DAG node: `COMP-C3-RUNNER-NEEDS-BLANKS`

**Proposition.** If a regime reaches words of every length from $a$, its reach set is closed at
no bound $L\ge|a|$, so the verdict of §1.4 is *bound exceeded* at every bound. The one-state
machine that moves right forever is such a regime under the encoding of §1.6.

*Proof.* A closed set at bound $L$ contains every reachable word (§1.4), so all reachable words
would have length $\le L$. For the runner, each step at the right end applies the rule that
inserts a blank before the end marker, so the word grows by one at each such step. $\square$

So the bounded decider cannot settle a machine that consumes fresh tape: blank cells are a
supply, and the bound must be raised without end.

Lean: `lean4/GenesisCompTM.lean::runner_unbounded`, `lean4/GenesisCompTM.lean::runner_step`,
`lean4/GenesisCompTM.lean::runner_not_closed`,
`lean4/GenesisCompTM.lean::runner_unboundedSupply`,
`lean4/GenesisComputation.lean::not_closed_of_unbounded`,
`lean4/GenesisComputation.lean::closed_bounds_reach`.

### 1.6 Rewriting simulates TM0 machines

DAG nodes: `COMP-C5-TM0-STEP-SIMULATION` `COMP-C5-CLOSURES-HALTING` `COMP-C5-MARK-BUDGET-RULE-LIST`

**Proposition.** Let $M$ be a Mathlib TM0 machine with tape alphabet $\Gamma$ (blank $\flat$)
and states $\Lambda$. Use the marks $\Gamma\sqcup\Lambda\sqcup\{\vdash,\dashv\}$, and write a
configuration with state $q$, head symbol $a$, left cells $u$ and right cells $v$ (each
determined up to trailing blanks) as $\vdash\,u^{\mathrm{rev}}\,q\,a\,v\,\dashv$. The rules are,
for each transition $M(q,a)=(q',s)$:

| $s$ | rule |
|---|---|
| write $b$ | $q\,a\to q'\,b$ |
| move right | $q\,a\,c\to a\,q'\,c$, and $q\,a\dashv\ \to a\,q'\,\flat\dashv$ |
| move left | $c\,q\,a\to q'\,c\,a$, and $\vdash q\,a\to\ \vdash q'\,\flat\,a$ |

Then:

1. every configuration has a word, and a word represents at most one configuration;
2. if $M$ steps from $c$ to $c'$ and $w$ represents $c$, some step $w\to w'$ has $w'$ representing
   $c'$; and every step from a word representing $c$ is of this kind;
3. the same holds for reach, and $M$ halts from $c$ if and only if some word reachable from a word
   representing $c$ is irreducible;
4. there are $|\Gamma|+|\Lambda|+2$ marks, and for finite $\Gamma,\Lambda$ the rules form a finite
   list, to which §1.4 applies.

*Proof.* (1) Existence is the displayed word. A represented word has exactly one state mark, so
the position of $q$ is determined, and with it $u$, $a$ and $v$ up to trailing blanks, which is
the identity of a Mathlib tape. (2) Every left side contains the state mark, so a step rewrites at
the state mark; the symbol after it is $a$, and determinism of $M$ fixes the transition. Each
transition has a rule that applies: a right move has a cell or $\dashv$ after $a$, and a left move
has a cell or $\vdash$ before $q$. Reading off the result gives the next configuration, with a
blank inserted where the head moves past an end. (3) Induct along the run. A word representing $c$
is irreducible exactly when no rule applies, which by (2) is exactly when $M(q,a)$ is undefined,
which is halting. (4) Count the four kinds of marks; there are finitely many triples
$(q,a,c)$. $\square$

Lean: `lean4/GenesisCompTM.lean::step_fwd`, `lean4/GenesisCompTM.lean::step_bwd`,
`lean4/GenesisCompTM.lean::rep_exists`, `lean4/GenesisCompTM.lean::rep_unique`,
`lean4/GenesisCompTM.lean::Rules`, `lean4/GenesisCompTM.lean::cfgWord`,
`lean4/GenesisCompTM.lean::split_st`, `lean4/GenesisCompTM.lean::reaches_fwd`,
`lean4/GenesisCompTM.lean::reach_bwd`, `lean4/GenesisCompTM.lean::halts_iff`,
`lean4/GenesisCompTM.lean::Halts`, `lean4/GenesisCompTM.lean::Irreducible`,
`lean4/GenesisCompTM.lean::card_sym`, `lean4/GenesisCompTM.lean::ruleList`,
`lean4/GenesisCompTM.lean::mem_ruleList`, `lean4/GenesisCompTM.lean::reach_ruleList_iff`.

### 1.7 A universal machine with finitely many marks

DAG nodes: `COMP-C6-EVAL-HAS-A-CODE` `COMP-C6-TM2-OUTPUT-FORM` `COMP-C6-TM0-HALTING-EQUIVALENCE` `COMP-C6-FINITE-MARKS`

**Proposition.**

1. There is a fixed code $u$ with $\mathrm{eval}\,u\,\langle\ulcorner c\urcorner,n\rangle=\mathrm{eval}\,c\,n$
   for all codes $c$ and inputs $n$, and a fixed `ToPartrec` code computing the same function of
   one number.
2. The fixed TM2 machine compiled from that code, started on the paired input, halts with output
   $\mathrm{eval}\,c\,n$ exactly when the value is defined.
3. The TM0 machine $M_0$ obtained by compiling further to TM1 and TM0 halts from the explicit
   initial configuration on $\langle\ulcorner c\urcorner,n\rangle$ if and only if
   $\mathrm{eval}\,c\,n$ is defined.
4. Every word reachable from a start word of the rewriting regime of $M_0$ uses marks from one
   finite set: the two end markers, the $1250$ tape marks, and the state marks of a finite set
   closed under the machine's steps.

*Proof.* (1) The map $(c,n)\mapsto\mathrm{eval}\,c\,n$ is partial recursive (Kleene's universal
function, in Mathlib), so it has a code; composing with the unpairing gives a function of one
number, which Mathlib's `ToPartrec` translation also computes. (2) is Mathlib's correctness
theorem for the `PartrecToTM2` compiler applied to that code. (3) The TM2→TM1 and TM1→TM0
compilers preserve the domain of evaluation from corresponding configurations, and the initial
configurations correspond. (4) The TM1 tape alphabet is $\mathrm{Bool}\times(K\to
\mathrm{Option}\,\Gamma')$ with $|K|=|\Gamma'|=4$, which has $2\cdot5^4=1250$ elements. Mathlib's
support lemmas give a finite set of states that contains the initial state and is closed under
steps. By §1.6(2) every reachable word represents a configuration reachable by $M_0$, so its marks
lie in this set. $\square$

So a single finite alphabet of marks, admitted and separated as in §1.1, carries a universal
computation.

Lean: `lean4/GenesisCompUniv.lean::univFun_partrec`, `lean4/GenesisCompUniv.lean::universal_code`,
`lean4/GenesisCompUniv.lean::univCode_exists`, `lean4/GenesisCompUniv.lean::univCode_eval`,
`lean4/GenesisCompUniv.lean::tm2_computes_eval`, `lean4/GenesisCompUniv.lean::dom_chain`,
`lean4/GenesisCompUniv.lean::halts_iff_dom`, `lean4/GenesisCompUniv.lean::halts_iff_eval_dom`,
`lean4/GenesisCompUniv.lean::trCfg_init_gen`, `lean4/GenesisCompUniv.lean::initCfg0`,
`lean4/GenesisCompUniv.lean::used_marks_finite`,
`lean4/GenesisCompUniv.lean::used_state_marks_finite`, `lean4/GenesisCompUniv.lean::card_G1`,
`lean4/GenesisCompUniv.lean::step_closed`, `lean4/GenesisCompUniv.lean::init_mem`,
`lean4/GenesisCompUniv.lean::markSet`.

### 1.8 Halting and normal-form reach are undecidable

DAG nodes: `COMP-C7-MACHINE-HALTING-UNDECIDABLE` `COMP-C7-NF-REACH-UNDECIDABLE`

**Proposition.** For each $n$, the predicate "$M_0$ halts from the initial configuration on
$\langle\ulcorner c\urcorner,n\rangle$" is not a computable predicate of $c$. For the fixed rules
of $M_0$ and its start words, "the start word reaches an irreducible word" is not computable, as
a predicate of the code $c$ or of the number input.

*Proof.* By §1.7(3) the first predicate is "$\mathrm{eval}\,c\,n$ is defined", which is not
computable (the halting problem, in Mathlib). The start word represents the initial
configuration, so by §1.6(3) the second predicate equals the first. As a predicate of the number
$x$ it is "$u$ halts on $x$"; if that were computable, composing with the computable map
$c\mapsto\langle\ulcorner c\urcorner,n\rangle$ would decide the first. $\square$

Lean: `lean4/GenesisCompUniv.lean::halting_not_computable`,
`lean4/GenesisCompUniv.lean::reach_irreducible_iff`,
`lean4/GenesisCompUniv.lean::reach_irreducible_not_computable`,
`lean4/GenesisCompUniv.lean::nfReach_iff`, `lean4/GenesisCompUniv.lean::nfReach_not_computable`,
`lean4/GenesisCompUniv.lean::startWord_rep`.

### 1.9 Two marks suffice for coding

DAG node: `COMP-C8-BINARY-CODING`

**Proposition.** For a finite alphabet $\alpha$, code each letter by its index in
$w=\lceil\log_2|\alpha|\rceil+1$ binary digits and a word by concatenating the codes. This is an
injective monoid homomorphism with an explicit decoder, and the same holds with the two separated
marks as the binary digits.

*Proof.* Indices are below $2^w$, so the $w$-digit representation is injective. The code of a
concatenation is the concatenation of codes by definition. The decoder cuts the input into blocks
of $w$ and reads each one, which inverts the encoder; a map with a left inverse is injective.
Replacing $0,1$ by two marks is a letter bijection (§1.2). $\square$

Lean: `lean4/GenesisComputation.lean::decode_encode`,
`lean4/GenesisComputation.lean::encodeWord_injective`,
`lean4/GenesisComputation.lean::encodeMarks_injective`,
`lean4/GenesisComputation.lean::encodeMarks_append`,
`lean4/GenesisComputation.lean::decodeMarks_encodeMarks`,
`lean4/GenesisComputation.lean::bits_injective`.

### 1.10 Admission is uncapped and supply drives growth

DAG nodes: `COMP-C4-STEPE-UNCAPPED` `COMP-C4-SUPPLY-GROWTH`

**Proposition.** In the event semantics, $k$ datum admissions raise the number of data by $k$,
so every number of data is reached, and no event lowers it. If $s_{n+1}=s_n-d_n+b_n$ with
$d_n\le s_n$ and $d_n<b_n$ for every $n$, then $s_n\ge s_0+n$.

*Proof.* An admission adds one datum and every other event leaves the count. For the recurrence,
$d_n\le s_n$ makes the subtraction exact, so $s_{n+1}=s_n+(b_n-d_n)\ge s_n+1$. $\square$

The births $b_n$ are an input of the recurrence; nothing here produces them.

Lean: `lean4/GenesisComputation.lean::replay_admitDatum_replicate`,
`lean4/GenesisComputation.lean::genesis_unbounded_admission`,
`lean4/GenesisComputation.lean::stepE_data_mono`, `lean4/GenesisComputation.lean::stepE`,
`lean4/GenesisComputation.lean::supply_growth`.

## 2. Models of fault-tolerant viability

All quantities in this section are rational unless stated otherwise. The models are simple
recurrences; they say what each recurrence permits, not what a physical device does.

### 2.1 The repair queue

DAG node: `QCV-NET-RATE-BACKLOG-DICHOTOMY`

**Proposition.** Let $q_0\ge0$ and $q_{t+1}=\max(0,\ q_t+\delta)$ with drift
$\delta=\lambda+g\mu-\mu$ (arrivals $\lambda$, repairs $\mu$, of which a fraction $g$ create new
faults). The backlog is bounded if and only if $\lambda\le(1-g)\mu$. Consequently: for $g\ge1$
and $\lambda>0$ no $\mu\ge0$ bounds it; for $g<1$ and $\mu=\kappa r$ with $\kappa>0$ it is bounded
if and only if $r\ge\lambda/((1-g)\kappa)$; and with $r=0$ and $\lambda>0$, $q_t=q_0+t\lambda$.

*Proof.* If $\delta\le0$, then $q_t\le q_0$ by induction, since $\max(0,q_t+\delta)\le\max(0,q_t)$.
If $\delta>0$, the maximum is never truncated from $q_0\ge0$, so $q_t=q_0+t\delta$, unbounded. The
condition $\delta\le0$ is $\lambda\le(1-g)\mu$. For $g\ge1$ the right side is $\le0<\lambda$. For
$g<1$ divide by $(1-g)\kappa>0$. For $\mu=0$, $\delta=\lambda>0$. $\square$

Lean: `lean4/QcRepairQueue.lean::backlog_bounded_iff`,
`lean4/QcRepairQueue.lean::no_bounded_backlog_if_unit_gain`,
`lean4/QcRepairQueue.lean::fresh_supply_threshold`,
`lean4/QcRepairQueue.lean::no_supply_linear_growth`,
`lean4/QcRepairQueue.lean::backlog_linear`, `lean4/QcRepairQueue.lean::backlog_le_initial`.

### 2.2 Linear recurrences and the cost of repair

DAG node: `QCV-REPAIR-NEEDED-BUT-COSTLY`

**Proposition.** The union-bound recurrence $p_{k+1}=a\,p_k$ with $a\ge1$ and $p_0>0$ has
$p_k=a^kp_0$ and does not tend to zero. With $\binom a2$ fault pairs, the certified threshold
$1/\binom b2$ for $2\le a\le b$ fault locations is at most $1/\binom a2$.

*Proof.* Induction gives $p_k=a^kp_0\ge p_0$. $\binom x2=x(x-1)/2$ is increasing for $x\ge1$, and
both values are positive for $a\ge2$. $\square$

So a code that only accumulates faults linearly never suppresses them, and adding fault
locations lowers the threshold.

Lean: `lean4/QcConcatenation.lean::lin_not_goesToZero`, `lean4/QcConcatenation.lean::lin_closed`,
`lean4/QcConcatenation.lean::pairCount_mono`,
`lean4/QcConcatenation.lean::threshold_decreases_with_repair`.

### 2.3 The concatenation threshold

DAG node: `QCV-CONCATENATION-THRESHOLD-DICHOTOMY`

**Proposition.** Let $p_{k+1}=c\,p_k^2$ with $c>0$, $p_0\ge0$, and $r=c\,p_0$. Then
$c\,p_k=r^{2^k}$, and:

1. if $r<1$, $p_k\to0$ with $c\,p_k\le r^{k+1}$, and for $r\le1/2$, $p_k\le(1/2)^{2^k}/c$;
2. if $r=1$, $p_k=1/c$ for all $k$;
3. if $r>1$, $c\,p_k\ge1+2^k(r-1)$, so $p_k$ diverges.

Hence $p_k\to0$ if and only if $p_0<1/c$.

*Proof.* $c\,p_{k+1}=(c\,p_k)^2$, and induction gives the closed form. (1) $2^k\ge k+1$ and
$0\le r<1$ give $r^{2^k}\le r^{k+1}\to0$; for $r\le1/2$, $r^{2^k}\le(1/2)^{2^k}$. (2) is the fixed
point. (3) is Bernoulli's inequality $(1+x)^m\ge1+mx$ with $x=r-1>0$. $\square$

Lean: `lean4/QcConcatenation.lean::conc_closed`, `lean4/QcConcatenation.lean::conc_eq_div`,
`lean4/QcConcatenation.lean::threshold_trichotomy`,
`lean4/QcConcatenation.lean::goesToZero_iff_below_threshold`,
`lean4/QcConcatenation.lean::sub_bound`, `lean4/QcConcatenation.lean::sub_half_bound`,
`lean4/QcConcatenation.lean::super_bound`, `lean4/QcConcatenation.lean::super_diverges`,
`lean4/QcConcatenation.lean::fixed_point`.

### 2.4 Level-dependent overhead

DAG node: `QCV-OVERHEAD-GROWTH-CRITERION`

**Proposition.** Let $p_{k+1}=c_k\,p_k^2$ with $c_k\ge0$, and define $A_0=1$,
$A_{k+1}=c_kA_k^2$. Then $p_k=p_0^{2^k}A_k$, and some $p_0>0$ has $p_k\to0$ if and only if
$A_k\le M^{2^k}$ for some $M>0$ and all $k$. This criterion holds when

1. $c_k\le C$;
2. $c_k\le\alpha\beta^{k+1}$ with $\alpha,\beta\ge1$ (for example $c_k=(k+1)^2$);
3. $c_k\le\alpha\beta^{N_k}$ with $\alpha,\beta\ge1$ and block sizes $N_{k+1}\le sN_k$, $s<2$;

and it fails, so no $p_0>0$ has $p_k\to0$, when $c_k\ge\alpha\beta^{2^k}$ with $\alpha>0$,
$\beta>1$, or $c_k\ge\alpha\beta^{N_k}$ with $N_k\ge2^k$ and $\beta>1$.

*Proof.* The closed form follows by induction. If $A_k\le M^{2^k}$, take $p_0<1/M$; then
$p_k\le(p_0M)^{2^k}\to0$. Conversely, if $p_k\to0$ then $p_k<1$ for $k\ge K$, so
$A_k<(1/p_0)^{2^k}$ there; take $M\ge\max(1/p_0,1,A_0,\dots,A_{K-1})$, using $M^{2^k}\ge M$ for
$M\ge1$.

In each positive case write $A_k=\prod_{j<k}c_j^{2^{k-1-j}}$. (1) $A_k\le C'^{2^k-1}\le C'^{2^k}$
with $C'=\max(C,1)$. (2) The exponent of $\beta$ is $\sum_{j<k}2^{k-1-j}(j+1)\le2^k\sum_{j\ge0}
(j+1)2^{-j-1}=2^{k+1}$, so $A_k\le(\alpha\beta^2)^{2^k}$; and $(k+1)^2\le4^{k+1}$. (3) The exponent
of $\beta$ is $E_k$ with $E_0=0$, $E_{k+1}=2E_k+N_k$, and induction with $N_{k+1}\le sN_k$ gives
$E_k+N_k/(2-s)\le2^kN_0/(2-s)$, so $A_k\le(\alpha\beta^{N_0/(2-s)})^{2^k}$.

For the negative case with $c_j=\alpha\beta^{2^j}$ exactly, induction gives
$(\alpha A_k)^2=(\alpha^2\beta^k)^{2^k}$, so $A_k^{1/2^k}$ grows like $\beta^{k/2}$ and no $M$
bounds it; larger $c_k$ give larger $A_k$. The block-size case reduces to it since
$\beta^{N_k}\ge\beta^{2^k}$. $\square$

Lean: `lean4/QcConcatenation.lean::concv_eq_amp`,
`lean4/QcConcatenation.lean::threshold_region_iff`,
`lean4/QcConcatenation.lean::region_empty_iff`,
`lean4/QcConcatenation.lean::ampBounded_of_bounded`,
`lean4/QcConcatenation.lean::bounded_overhead_goesToZero`,
`lean4/QcConcatenation.lean::ampBounded_of_geom`, `lean4/QcConcatenation.lean::ampBounded_poly`,
`lean4/QcConcatenation.lean::ampBounded_of_sizes`, `lean4/QcConcatenation.lean::blockExp_le`,
`lean4/QcConcatenation.lean::dexp_not_ampBounded`,
`lean4/QcConcatenation.lean::dexp_region_empty`,
`lean4/QcConcatenation.lean::sizes_not_ampBounded`, `lean4/QcConcatenation.lean::amp_dexp_sq`.

### 2.5 Viability needs every requirement

DAG node: `QCV-VIABILITY-NEEDS-ALL-REQUIREMENTS`

**Proposition.** For $g<1$, $\kappa>0$ and $c_k\ge0$, the backlog is bounded and some positive
physical rate has $p_k\to0$ if and only if $r\ge\lambda/((1-g)\kappa)$ and $A_k\le M^{2^k}$ for
some $M>0$. Without supply the backlog is unbounded; with $g\ge1$ it is unbounded for every
supply; and an error profile with $p_{k+1}\ge c_kp_k^2$, $c_k\ge\alpha\beta^{2^k}$, $\beta>1$,
$p_0>0$ does not tend to zero.

*Proof.* The equivalence is the conjunction of §2.1 and §2.4. The two backlog statements are
§2.1. For the profile, induction gives $p_k\ge p'_k$, where $p'$ solves the recurrence with
equality from $p_0$, because squaring is monotone on non-negative numbers; by §2.4 $p'_k$ does
not tend to zero, so neither does $p_k$. $\square$

Lean: `lean4/QcSelfObstruction.lean::model_viable_iff`,
`lean4/QcSelfObstruction.lean::not_viable_without_supply`,
`lean4/QcSelfObstruction.lean::not_viable_unit_gain`,
`lean4/QcSelfObstruction.lean::not_viable_dexp_profile`,
`lean4/QcSelfObstruction.lean::level_error_ge`.

### 2.6 Noisy histories contract the trace distance exactly

DAG node: `QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY`

**Proposition.** For complex $d\times d$ matrices let $\|X\|=\sup_U|\operatorname{tr}(UX)|$ over
unitaries $U$, and $\Delta_p(\rho)=(1-p)\rho+p\operatorname{tr}(\rho)I/d$. For $p\le1$ and
$\operatorname{tr}\rho=\operatorname{tr}\sigma$,
$\|\Delta_p(\rho)-\Delta_p(\sigma)\|=(1-p)\|\rho-\sigma\|$. Along a history of unitaries $V_i$
followed by depolarizing at rates $p_i\in[0,1]$, the distance is multiplied by
$\prod_i(1-p_i)$, which is at most $(1-p)^t$ if every $p_i\ge p$; and
$(1-p)^t\le1/(1+pt)$ for $p\in[0,1]$.

*Proof.* The supremum is finite since $|\operatorname{tr}(UX)|\le\sum_{ij}|X_{ij}|$. With equal
traces the identity terms cancel, so the difference is $(1-p)(\rho-\sigma)$ and $1-p\ge0$ comes
out of the supremum. Conjugation by a unitary $V$ does not change the supremum, since
$\operatorname{tr}(UVXV^*)=\operatorname{tr}((V^*UV)X)$ and $U\mapsto V^*UV$ is a bijection of the
unitary group; it also keeps traces equal. Induct along the history. Finally
$(1+pt)(1-p)^t\le(1+p)^t(1-p)^t=(1-p^2)^t\le1$ by Bernoulli's inequality. $\square$

So $(1-p)^t\le\delta$ once $t\ge(1/\delta-1)/p$: noise erases the record of the initial state at
a rate fixed by $p$, whatever the unitaries.

Lean: `lean4/QcEntropySink.lean::tn`, `lean4/QcEntropySink.lean::tn_smul`,
`lean4/QcEntropySink.lean::tn_conj`, `lean4/QcEntropySink.lean::pairingSet_bddAbove`,
`lean4/QcEntropySink.lean::depol_dist`, `lean4/QcEntropySink.lean::noisyStep_dist`,
`lean4/QcEntropySink.lean::run_dist`, `lean4/QcEntropySink.lean::run_dist_le`,
`lean4/QcEntropySink.lean::decay_le_inv`, `lean4/QcEntropySink.lean::decay_below`.

### 2.7 The qubit case on Bloch vectors

DAG node: `QCV-QUBIT-BLOCH-DECAY-EXACT`

**Proposition.** For rational Bloch vectors and noisy steps $r\mapsto(1-p)Rr$ with rational
rotations ($R^{\mathsf T}R=I$), the squared distance of two runs is multiplied by
$\prod_i(1-p_i)^2$, so it is at most $((1-p)^2)^t$ times the initial one when every
$p_i\in[p,1]$. Moreover $(v\cdot\vec\sigma)^2=(v\cdot v)I$, so the difference of two qubit states
with Bloch vectors $r,s$ has both singular values equal to $|r-s|/2$.

*Proof.* $|(1-p)R(r-s)|^2=(1-p)^2(r-s)^{\mathsf T}R^{\mathsf T}R(r-s)=(1-p)^2|r-s|^2$; induct. The
Pauli matrices square to $I$ and anticommute pairwise, so the cross terms of $(v\cdot\vec\sigma)^2$
cancel. The difference of the states is $\tfrac12(r-s)\cdot\vec\sigma$, a Hermitian matrix whose
square is $\tfrac14|r-s|^2I$, so its eigenvalues are $\pm|r-s|/2$. $\square$

Lean: `lean4/QcEntropySink.lean::sqDist_runB`, `lean4/QcEntropySink.lean::sqDist_runB_le`,
`lean4/QcEntropySink.lean::sqDist_stepB`, `lean4/QcEntropySink.lean::rot_dot`,
`lean4/QcEntropySink.lean::blochMat_sq`.

## 3. Authorization

### 3.0 Definitions

A predicate $P$ on a set $X$ is *decided* by $d:X\to\mathrm{Bool}$ if $d(x)=\mathrm{true}\iff P(x)$.
A class of allowed deciders has *no total decider* for $P$ if no allowed $d$ decides it. A
*terminalizer* sends each proposal to one of *authorized*, *rejected*, *unresolved*. It is
*acceptance-sound* if authorized implies valid, *acceptance-complete* if valid implies
authorized, *rejection-sound* if rejected implies not valid, and *closed* if it never returns
unresolved. Its *acceptance bit* is true exactly on authorized proposals.

### 3.1 Class-relative transport

DAG nodes: `AUTHF-CLASS-RELATIVE-TRANSPORT` `AUTH-G5A-CLASS-RELATIVE-TRANSPORT` `AUTHF-MATHLIB-HALTING-BRIDGE`

**Proposition.** Let $m:H\to X$ satisfy $h(x)\iff\mathrm{valid}(m(x))$, and suppose that $a\circ m$
is an allowed source decider whenever $a$ is an allowed proposal decider. If the source predicate
has no allowed total decider, neither does validity. With the computable functions as the allowed
class on both sides and $m$ computable, the closure hypothesis holds, and for the source predicate
"code $c$ halts on input $n$" the conclusion holds.

*Proof.* If $a$ decides validity, $a\circ m$ decides $h$, since $a(m(x))=\mathrm{true}\iff
\mathrm{valid}(m(x))\iff h(x)$, and it is allowed. Computable functions are closed under
composition, and the halting predicate has no computable decider (Mathlib). $\square$

Lean: `lean4/AuthIncompleteness/GlobalLift.lean::AuthorizationIncompleteness.GlobalComputabilityLift.Decides`,
`lean4/AuthIncompleteness/GlobalLift.lean::AuthorizationIncompleteness.GlobalComputabilityLift.NoTotalDecider`,
`lean4/AuthIncompleteness/GlobalLift.lean::AuthorizationIncompleteness.GlobalComputabilityLift.ValidityReduction`,
`lean4/AuthIncompleteness/GlobalLift.lean::AuthorizationIncompleteness.GlobalComputabilityLift.ClosedUnderReduction`,
`lean4/AuthIncompleteness/GlobalLift.lean::AuthorizationIncompleteness.GlobalComputabilityLift.total_authorizer_yields_source_decider`,
`lean4/AuthIncompleteness/GlobalLift.lean::AuthorizationIncompleteness.GlobalComputabilityLift.no_source_decider_blocks_total_authorizer`,
`papers/foundations/authorization_incompleteness/evidence/original/formal/global_computability_lift_models.lean::AuthorizationIncompleteness.GlobalComputabilityLift.no_source_decider_blocks_total_authorizer`,
`papers/foundations/authorization_incompleteness/evidence/original/formal/global_computability_lift_models.lean::AuthorizationIncompleteness.GlobalComputabilityLift.total_authorizer_yields_source_decider`,
`lean4/AuthIncompleteness/MathlibBridge.lean::AuthorizationIncompleteness.MathlibBridge.halting_has_no_computable_decider`,
`lean4/AuthIncompleteness/MathlibBridge.lean::AuthorizationIncompleteness.MathlibBridge.computable_closed_under_computable_reduction`,
`lean4/AuthIncompleteness/MathlibBridge.lean::AuthorizationIncompleteness.MathlibBridge.no_computable_authorizer_of_computable_reduction`,
`lean4/AuthIncompleteness/MathlibBridge.lean::AuthorizationIncompleteness.MathlibBridge.halting_transport_instance`.

### 3.2 Terminal verdicts

DAG nodes: `AUTHF-TERMINAL-ACCEPT-BIT` `AUTHF-TERMINAL-CLOSED-TWO-SIDED` `AUTH-G5C-TERMINALIZATION-CONSEQUENCE` `AUTHF-TERMINAL-BOOL-FIXTURE`

**Proposition.**

1. The acceptance bit of an acceptance-sound and acceptance-complete terminalizer decides
   validity.
2. A rejection-sound, closed terminalizer is acceptance-complete.
3. Hence, if the acceptance bit is allowed and validity has no allowed total decider, no
   terminalizer is both acceptance-sound and acceptance-complete, and none is acceptance-sound,
   rejection-sound and closed.
4. On $\mathrm{Bool}$ with validity equal to the bit, sending true to authorized and false to
   rejected has all four properties.

*Proof.* (1) Soundness and completeness say authorized $\iff$ valid. (2) A valid proposal is not
rejected (rejection-soundness) and not unresolved (closure), so it is authorized. (3) follows from
(1) and (2). (4) Check the two cases. $\square$

The fixture shows that the obstruction in (3) comes from the absence of an allowed decider, not
from the three-valued format.

Lean: `lean4/AuthIncompleteness/Terminal.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.acceptance_bit_true_iff`,
`lean4/AuthIncompleteness/Terminal.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.acceptance_bit_decides_of_sound_complete`,
`lean4/AuthIncompleteness/Terminal.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_sound_complete_authorization`,
`lean4/AuthIncompleteness/Terminal.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.closed_two_sided_terminalization_is_acceptance_complete`,
`lean4/AuthIncompleteness/Terminal.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_closed_two_sided_terminalization`,
`lean4/AuthIncompleteness/Terminal.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.finite_closed_terminalizer_remains_possible`,
`lean4/AuthIncompleteness/Terminal.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.boolTerminalize`,
`lean4/AuthIncompleteness/Terminal.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.boolValidity`,
`papers/foundations/authorization_incompleteness/evidence/original/formal/terminal_authorization_boundary_models.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.acceptance_bit_decides_of_sound_complete`,
`papers/foundations/authorization_incompleteness/evidence/original/formal/terminal_authorization_boundary_models.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_sound_complete_authorization`,
`papers/foundations/authorization_incompleteness/evidence/original/formal/terminal_authorization_boundary_models.lean::AuthorizationIncompleteness.TerminalAuthorizationBoundary.finite_closed_terminalizer_remains_possible`.

### 3.3 Reports that cannot decide

DAG nodes: `AUTHF-SELF-RECEIPT-TOY` `AUTHF-LOGICAL-EXTERNALITY` `AUTHF-TAPE-CONTROL-REPORTS` `AUTHF-TRANSITION-ADEQUACY`

**Proposition.** If a report $\pi$ takes the same value on two proposals with different validity,
no function of the report decides validity; the identity report always does. In particular:

1. for the one-bit packet with validity equal to its bit, the receipt into the one-point set does
   not decide validity, and the identity receipt does;
2. a presentation with the identity report admits a report-only authorization, and a presentation
   with a one-point report and two packets of different validity admits none, whether or not the
   source and evaluator sites coincide;
3. in the tape-control model, the control outcome and the always-unread report each take one value
   on two presentations that the content contract separates; and the same read token is given
   opposite verdicts by the two supplied semantic adapters;
4. on the four-configuration transition table, the identity report is adequate for the marked-cell
   contract, while the control-outcome report is not: the halted blank and halted marked
   configurations both report *stay* and the contract separates them.

*Proof.* The general statement is the factorization barrier: $a(\pi(x))=a(\pi(y))$ when
$\pi(x)=\pi(y)$. Items (1) to (4) exhibit the pair in each model; the identity report factors
validity through itself. The adapter claim in (3) is an evaluation of the two adapters. $\square$

So in these models physical separation of sites is neither needed nor sufficient: what matters is
whether the report separates proposals of different validity.

Lean: `lean4/AuthIncompleteness/Core.lean::AuthorizationIncompleteness.self_receipt_splits_validity`,
`lean4/AuthIncompleteness/Core.lean::AuthorizationIncompleteness.self_receipt_blocks_authorization`,
`lean4/AuthIncompleteness/Core.lean::AuthorizationIncompleteness.complete_receipt_decides_toy_contract`,
`lean4/AuthIncompleteness/Externality.lean::AuthorizationIncompleteness.LogicalExternalityModels.physical_separation_neither_needed_nor_sufficient_for_toy_authorization`,
`lean4/AuthIncompleteness/Externality.lean::AuthorizationIncompleteness.LogicalExternalityModels.coLocatedComplete_can_authorize`,
`lean4/AuthIncompleteness/Externality.lean::AuthorizationIncompleteness.LogicalExternalityModels.separatedCollapsed_cannot_authorize`,
`lean4/AuthIncompleteness/TapeControl.lean::AuthorizationIncompleteness.TapeControlModels.same_halt_control_blocks_control_only_decider`,
`lean4/AuthIncompleteness/TapeControl.lean::AuthorizationIncompleteness.TapeControlModels.unread_report_blocks_content_decider`,
`lean4/AuthIncompleteness/TapeControl.lean::AuthorizationIncompleteness.TapeControlModels.same_read_token_allows_distinct_semantic_adapters`,
`lean4/AuthIncompleteness/TapeControl.lean::AuthorizationIncompleteness.TapeControlModels.shared_halt_control_splits_content_contract`,
`lean4/AuthIncompleteness/TapeTransition.lean::AuthorizationIncompleteness.TapeTransitionInvariantModels.full_configuration_report_adequate_for_marked_cell_contract`,
`lean4/AuthIncompleteness/TapeTransition.lean::AuthorizationIncompleteness.TapeTransitionInvariantModels.full_configuration_report_admits_marked_cell_decider`,
`lean4/AuthIncompleteness/TapeTransition.lean::AuthorizationIncompleteness.TapeTransitionInvariantModels.control_report_not_adequate_for_marked_cell_contract`,
`lean4/AuthIncompleteness/TapeTransition.lean::AuthorizationIncompleteness.TapeTransitionInvariantModels.shared_stay_control_blocks_control_only_contract_decider`.

### 3.4 Finite fixtures

DAG nodes: `AUTHF-HALT-NOT-POLICY` `AUTHF-PD-EXTENSION-NONUNIQUE` `AUTHF-TRANSITION-INVARIANTS` `AUTHF-REPLAY-BOUND-SUBMISSION`

**Proposition.**

1. In the direct machine model, the tape-control model and the replay model, a halted or verified
   outcome receives different terminal values from two supplied policies (accept halted against
   leave all open; accept halt against reject all; authorize on verified against leave verified
   open).
2. Over the two-mark Boolean analogue of a primitive difference, the identity extension and the
   rejecting extension give different validity and terminal values at the same carrier point.
3. The four-configuration transition table maps every configuration to one that the
   clean-terminal contract accepts, so it preserves that contract. It does not preserve the
   marked-cell contract: the running marked configuration is accepted and its successor, the
   running blank configuration, is not.
4. In the finite replay model, if replay of a receipt on an observed submission returns
   *replayed*, the observed submission is the one bound in the receipt.

*Proof.* (1) to (3) are checks of finitely many cases. (4) Replay first compares the observed
submission with the bound one and returns *replayed* only in the equal branch. $\square$

Items (1) and (2) say that the syntax (a halt, a verified replay, a primitive difference) is
compatible with more than one policy, so the policy is an additional declaration.

Lean: `lean4/AuthIncompleteness/DirectTM.lean::AuthorizationIncompleteness.DirectTuringMachineModels.syntactic_halt_does_not_select_direct_machine_policy`,
`lean4/AuthIncompleteness/TapeControl.lean::AuthorizationIncompleteness.TapeControlModels.syntactic_halt_does_not_select_terminal_policy`,
`lean4/AuthIncompleteness/Replay.lean::AuthorizationIncompleteness.ReplayPacketBindingModels.terminal_policy_is_not_selected_by_verification`,
`lean4/AuthIncompleteness/PDModels.lean::AuthorizationIncompleteness.PrimitiveDifferenceModels.primitive_interface_has_distinct_authorization_extensions`,
`lean4/AuthIncompleteness/PDModels.lean::AuthorizationIncompleteness.PrimitiveDifferenceModels.same_primitive_extensions_split_validity`,
`lean4/AuthIncompleteness/PDModels.lean::AuthorizationIncompleteness.PrimitiveDifferenceModels.same_primitive_extensions_split_policy`,
`lean4/AuthIncompleteness/TapeTransition.lean::AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_preserves_clean_terminal_contract`,
`lean4/AuthIncompleteness/TapeTransition.lean::AuthorizationIncompleteness.TapeTransitionInvariantModels.marked_contract_countertrace`,
`lean4/AuthIncompleteness/TapeTransition.lean::AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_does_not_preserve_marked_cell_contract`,
`lean4/AuthIncompleteness/Replay.lean::AuthorizationIncompleteness.ReplayPacketBindingModels.replayed_status_requires_bound_submission`,
`lean4/AuthIncompleteness/Replay.lean::AuthorizationIncompleteness.ReplayPacketBindingModels.replay`.

### 3.5 The direct machine model and its token code

DAG nodes: `AUTHF-DTM0-HALT-IFF-STATE` `AUTHF-DTM1-ROUNDTRIP` `AUTH-DTM1-TOKEN-CODE-ROUNDTRIP`

**Proposition.** In the direct machine model, a step returns *halted* exactly when the
configuration's state is the machine's halt state, and execution then returns *halted* at every
fuel budget. Encode a machine as its halt-state token followed by one five-token frame per rule
(state, scanned tag, next state, written tag, move tag). Decoding the encoding returns the
machine. The decoder, which must consume its whole input, rejects the empty list, a truncated
frame, an invalid symbol tag and an invalid move tag.

*Proof.* The step function tests the halt state first. Execution at fuel $f+1$ performs a step,
which is halted, and at fuel $0$ the halt test also applies; induct on the fuel. The tag codes
for symbols and moves round-trip by cases. The frame decoder reads five tokens and recurses, so
induction on the rule list gives $\mathrm{decode}(\mathrm{encode}(\mathit{rules}))=\mathit{rules}$,
and prefixing the halt token gives the machine. The four rejections are evaluations on the
fixtures $[\,]$, $[0,0,0,1]$, $[0,0,2,1,0,0]$ and $[0,0,0,1,0,3]$. $\square$

Lean: `lean4/AuthIncompleteness/DirectTM.lean::AuthorizationIncompleteness.DirectTuringMachineModels.step_halted_iff_declared_halt`,
`lean4/AuthIncompleteness/DirectTM.lean::AuthorizationIncompleteness.DirectTuringMachineModels.execute_halted_of_declared_halt`,
`lean4/AuthIncompleteness/TokenCode.lean::AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMachine_encodeMachine`,
`lean4/AuthIncompleteness/TokenCode.lean::AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeRules_encodeRules`,
`lean4/AuthIncompleteness/TokenCode.lean::AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeTapeSymbol_encodeTapeSymbol`,
`lean4/AuthIncompleteness/TokenCode.lean::AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMove_encodeMove`,
`papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_token_code_models.lean::AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMachine_encodeMachine`,
`papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_token_code_models.lean::AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.empty_machine_code_is_rejected`,
`papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_token_code_models.lean::AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.truncated_rule_code_is_rejected`,
`papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_token_code_models.lean::AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_symbol_tag_is_rejected`,
`papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_token_code_models.lean::AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_move_tag_is_rejected`.
