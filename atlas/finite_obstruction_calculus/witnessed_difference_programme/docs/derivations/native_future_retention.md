# Minimum retained information for two native edits

Status: finite proposition for the declared carrier and two-edit horizon.
Register binding: GEN-WDP-73. The manuscript statement is in Appendix P.21.

## 1. Declared finite questions

**Definition.** A raw state is $s=(n,R,S,F)$, where $0\le n\le3$,
$R,S\in\mathbb N^{n\times n}$, and

\[
 T(s)=\sum_{i,j}(R_{ij}+S_{ij})\le4.
\]

The term names are literally $0,\ldots,n-1$. The set $F$ contains any
subset of the cyclically oriented nondegenerate triples. At $n=3$ the two
possible triples are $(0,1,2)$ and $(0,2,1)$; both may occur, regardless
of balance. Below three terms $F$ is empty. Raw equality does not identify
states under a permutation. All loops and both directed count tables remain.

The action alphabet has 42 literal descriptors: three identifications
$x<y$ in $0..2$; eighteen removals (two relations and nine ordered
addresses); two fillings; one term addition; and eighteen assertion additions.
Their guards and updates are the existing native five-edit operations:

| Kind | Native guard | Update | Native addition price |
|---|---|---|---|
| Identify $x,y$ | $0\le x<y<n$ | Push counts along the identification; discard degenerate faces and deduplicate the others | $(0,0)$ |
| Remove $A,x,y$ | Valid address and $A_{xy}>0$ | Subtract one at that coordinate | $(0,0)$ |
| Fill $x,y,z$ | Valid canonical nondegenerate triple absent from $F$ | Insert the triple | $(0,0)$ |
| AddTerm | Always enabled | Append one term with zero incident counts | $(1,0)$ |
| AddAssertion $A,x,y$ | Valid address | Add one at that coordinate | $(0,1)$ |

First test the native guard. If it fails, report `native_disabled`, with no
price or successor. Otherwise compute the native successor and native price.
If that successor is outside the declared carrier, report `bound_excluded`,
retaining its native price but executing no edge. Otherwise report `admitted`
with that successor, the native price, and one successful occurrence. Refused
offers do not change the state or use a successful-edit slot. They are not
self-loops. The horizon is two successful edits; native prices need not be
positive, so occurrences are a separate retained quantity.

Put $E=R-S$. The existing joint mark $M(s)$ records $n$ and the
lexicographically least joint pair of root-normalized excess table and face
decoration over all term permutations. For a fixed writing the root normalizer
is

\[
 N(E)_{ij}=E_{ij}-p_i+p_j,\qquad p_0=0,\quad p_i=E_{i0}\ (i>0).
\]

The empty writing has its unique empty table. For $f=(i,j,k)\in F$, the
literal balance answer is whether $E_{ij}+E_{jk}+E_{ki}=0$. The protected
present record $O(s)$ consists of $M(s)$ and the complete sorted list
of $(f,\operatorname{balanced}(f))$, including the literal keys $f$.
It therefore determines $F$, even when every balance answer is the same.

**Definition (terminal conventions).** Under `terminal_present_only`, at
zero remaining edits only $O(s)$ is observed. Under
`terminal_status_probes`, one also observes the 42-offer table of native
statuses and enabled native prices, but executes no edge. At positive
horizons both conventions observe $O(s)$, every offer, and all admitted
continuations with the remaining horizon decremented. A terminal halt is
neither a false native guard nor a bound exclusion. Each conclusion below
that mentions a lower layer identifies its convention.

## 2. The exact layer quotient

**Definition.** Let $G(s,a)$ contain the offer status and enabled native
price, but no executed child. Define complete signatures

\[
 K_0^{\mathrm p}(s)=O(s),\qquad
 K_0^{\mathrm g}(s)=(O(s),(G(s,a))_a).
\]

For either convention and $h>0$, let $K_h(s)$ consist of $O(s)$
and the ordered action table whose row is the status and price together
with $K_{h-1}(s\cdot a)$ and occurrence one for admitted edges; a
refused row has no child and occurrence zero. Write
$s\sim_h t\iff K_h(s)=K_h(t)$, and $q_h(s)=[s]_h$.
Equality here is equality of complete finite records, not equality of hashes.

**Conditional result (finite transition tables).** On any finite deterministic
partial action table with these observation conventions, $q_h$ is the
coarsest partition preserving and reflecting all declared observations and
continuations through horizon $h$.

*Proof.* At zero, equality of the stated terminal record is necessary and
sufficient. At $h+1$, equal signatures give equal present answers and offer
outcomes. For each admitted action they give equal $h$-signatures at its
two successors, so induction matches every remaining continuation. Conversely,
if all declared continuations agree, their empty prefixes give the present
answers and offer table; every admitted first action followed by every
remaining continuation gives equality of its child signature by induction.
This yields signature equality. Thus every adequate report refines $q_h$,
and $q_h$ itself is adequate. Termination follows by the finite state set,
finite action set, and finite layer count. ∎

**Imported standard.** Refining a finite partition by outputs and successor
classes is established automata mathematics; see John Hopcroft,
*An n log n algorithm for minimizing states in a finite automaton*,
STAN-CS-71-190 (1971), introduction and correctness section,
[primary report](https://www.cs.cmu.edu/~cdm/resources/Hopcroft1971.pdf).
The recurrence above is a direct bounded construction; it makes no claim to
that report's running-time bound. The source-specific content here is the
raw-state lower bound below, its native guard and carrier-change semantics,
the explicit attaining report, and separately checked source replay.

## 3. Recovering the raw counts

**Finite proposition (signed total).** The joint mark determines

\[
 \sigma(s)=\sum R_{ij}-\sum S_{ij}=\sum M(s).\mathrm{normal}.
\]

*Proof.* Summing the displayed normalizer over all ordered pairs gives
$\sum E_{ij}-n\sum p_i+n\sum p_j=\sum E_{ij}$. A term permutation
reorders the same sum. Choosing the writing jointly with the face decoration
does not alter this equality. At $n=0$ all sums are zero. ∎

**Finite proposition (two removal queries).** Equality of horizon-two
signatures determines $u_i=\min(c_i,2)$ for every count coordinate $c_i$.

*Proof.* Its removal is enabled exactly when $c_i>0$. If enabled, removing
one stays inside the carrier and the same next removal is enabled exactly
when $c_i>1$. These two answers give $u_i=0,1,2$. The argument uses
separate short continuations for different coordinates; it does not assert
that one two-edit experiment reads all coordinates. Both terminal conventions
include these observations at horizon two. ∎

**Finite proposition (clipped reconstruction).** A finite list of nonnegative
counts with total at most four is determined by its coordinatewise cap at two
and its signed total, provided each coordinate has its fixed sign $+1$
or $-1$.

*Proof.* If no cap equals two, all counts equal their caps. If at least two
caps equal two, the total bound forces exactly two such coordinates, both
equal to two, and all other counts zero. If exactly one cap, at $j$, equals
two, all other counts are already known. Writing its sign as $e_j$,

\[
 c_j=e_j\left(\sigma-\sum_{i\ne j}e_i u_i\right)
\]

recovers the remaining count because $e_j^2=1$. These cases exhaust all
possibilities. The formula is exact over the integers. ∎

## 4. Sharp minimum and an attaining report

**Finite proposition (GEN-WDP-73).** For the carrier of §1, under
either terminal convention, horizon-two signature equality is raw equality.
Consequently any report preserving and reflecting the declared futures needs
exactly 29,771 classes in total, and at least $|M^{-1}(m)|$ distinct reports
within every result-mark fiber. The report

\[
 H(s)=(M(s),F(s),\min(R,2),\min(S,2))
\]

attains those minima.

*Written proof.* Equal signatures give equal $n$ from the mark and equal
literal $F$ from the present record. The two removal queries give equal
capped counts. Equal marks give equal signed totals. Clipped reconstruction
therefore gives equal $R,S$, hence raw equality. Conversely identical raw
states have identical native guards, successors, costs, and observations at
every admitted prefix. Thus each signature class contains one raw state.

Any adequate report must refine that partition by §2. It therefore requires
one class per raw state, also after restricting to a fixed mark. The displayed
$H$ determines $n,F$, the caps and the signed total, so the same explicit
decoder recovers $s$. On arbitrary proposed reports, the decoder additionally
checks count nonnegativity, the total bound, dimensions, faces, and that the
decoded state's actual mark and caps reproduce the supplied report. A failed
candidate is rejected, never replaced with another solution.

At fixed $n$, the $2n^2$ nonnegative coordinates with sum at most four
number ${2n^2+4\choose4}$. The face-subset multipliers for $n=0,1,2,3$
are $1,1,1,4$. Thus the respective cardinalities are $1,15,495,29260$,
whose sum is 29,771. This combinatorial argument is independent of the
enumeration implementation. ∎

**Nonclaim.** This is a minimum number of semantic classes, not a minimum
number of named fields, bits, scalar observations, or physical instruments.
An index within a finite mark fiber could encode the same information. No
particular byte compression ratio follows.

## 5. State maps, step reflection, and composition

**Conditional result (layered lifting).** The forward state map is $q_h$.
For $h>0$, an admitted quotient action from $q_h(s)$ has successor
$q_{h-1}(s\cdot a)$. Its status, price and successor class do not depend
on the selected representative by §2. Every such quotient action has an
actual admitted action at every representative, with the same annotations.

The backward construction takes a quotient path and a **supplied original
raw starting state** in its first class, then executes its literal action
word in the original transition table. Each next state remains in the
supplied next class by the signature law. Induction constructs the full lift;
determinism gives uniqueness from that supplied start. The original state is
used to construct a lift, never to answer a quotient guard that failed to
factor through the report. At layer two, $H$'s decoder is an actual inverse
on its image. Lower-layer class selection is not recovery of discarded bytes.

Projection preserves the empty history, its zero occurrence count, and its
zero price. If a prefix has $k$ successful edits, its suffix must start at
the same raw intermediate state with layer $h-k$. For suffix length
$\ell\le h-k$, deterministic recursion on the concatenated action word
gives the same states as prefix followed by suffix. Prices add coordinatewise
and occurrences add as $k+\ell$. Projection and lifting commute with that
concatenation. Replacing the intermediate state or restoring a fresh horizon
changes this assertion's premises and is refused by the checker. ∎

## 6. Separation and boundary examples

**Finite propositions (whole-field deletion).** In each pair below, all
unspecified counts are zero. The retained fields other than the deleted one
agree; the stated protected question separates the pair.

| Deleted field from $H$ | Same reduced-report pair | Separating observation |
|---|---|---|
| $\min(R,2)$ | $n=2,F=\varnothing,S=0$; one count at $R_{01}$ versus $R_{10}$ | Remove $R,0,1$ enabled only in the first |
| $\min(S,2)$ | Corresponding second-relation pair, $R=0$ | Remove $S,0,1$ enabled only in the first |
| Literal $F$ | $n=3,R=S=0$; $F=\{(0,1,2)\}$ versus $F=\{(0,2,1)\}$ | Different literal balance keys, and opposite Fill $0,1,2$ guards |

The count pairs have equal marks by term permutation, as do the two oriented
face pairs. This establishes whole-field necessity in this encoding; adding
a duplicate balance-key list to $H$ would change the field-deletion claim.

**Finite proposition (horizon convention matters).** With two terms, no faces
and $S=0$, compare $(R_{01},R_{10})=(1,2)$ and $(2,1)$. Their mark
normal table is $[0,3,0,0]$. All 42 root offers agree. The twelve admitted
offers consist of Identify $0,1$, two positive removals, AddTerm, and eight
valid assertion additions; their successor present records agree. For
AddTerm, swapping terms zero and one while fixing the new term witnesses
equal joint marks. The thirty remaining offers are disabled.

After removing $R_{01}$, its next removal is disabled in the first state
and enabled in the second. Thus the pair agrees at horizon one under
`terminal_present_only` and separates at horizon two. Under
`terminal_status_probes`, the terminal guard already separates it at horizon
one. There is no convention-independent least-horizon conclusion.

**Finite propositions (carrier changes and refusal types).** The following
are retained independently of the reconstruction argument:

- At two terms, compare zero counts with $R_{01}=1,S_{10}=1$. Their initial
  marks agree. AddTerm followed by Fill $0,1,2$ gives balanced versus
  unbalanced, with price $(1,0)$ and two occurrences in both runs.
- At three terms compare $R_{01}=1$ with $R_{02}=1$, both with $S=0$
  and no faces. Initial marks agree. Identify $0,1$ gives two-term mark
  normals $[0,0,0,1]$ and $[0,1,0,0]$, with price zero and one occurrence.
- At three terms AddTerm is native-enabled, price $(1,0)$, but excluded by
  the term bound. At one term with $R_{00}=S_{00}=2$, adding at $R_{00}$
  is native-enabled, price $(0,1)$, but excluded by the count bound. Adding
  at $R_{22}$ instead has a false native guard and no price.
- Removing the sole count from a one-term state costs zero but executes one
  occurrence. The empty history has the same price and zero occurrences.
- At total five, same-relation reciprocal counts $(2,3)$ and $(3,2)$
  have equal caps, signed totals and marks. This rejects extension of the
  displayed decoder beyond total four. It does not settle larger profiles.

## 7. Evidence boundary

The native construction calls the existing owner. The Python reference
independently reconstructs the finite mathematics and compares every state
and action with the pinned original source. The
[formal module](../../lean4/WitnessedDifference/NativeFutureCompression.lean)
has the following selected declaration surface:

| Mathematical step | Formal declarations | Exact boundary |
|---|---|---|
| Signed total under normalization and permutation | normalization_preserves_signed_sum; square_sum_permutation | Exact integer sums on supplied finite index lists |
| Counts from caps and signed total | clipped_signed_counts_unique; count_report_injective | Fixed sign list, nonnegative counts, length agreement; total $\le 4$ for $h=2$ only |
| Removal observations and separation | two_removal_answers_determine_clip; removal_answers_determine_clips; unequal_counts_have_separating_observation; adequate_report_is_injective | The supplied natural-count guard model; native correspondence is separately replayed |
| Bound control and sharp collision | bound_five_clipped_collision | Exact lists \([2,3]\) and \([3,2]\) at $h=2, T=5$; the general-horizon collision is a written claim, not a declaration in this module |
| Forward and backward steps | step_projection; step_reflection | Supplied deterministic offer table, with distinct refusal constructors |
| Paths and composition | project_fine_path; lift_layer_path; fine_path_append; fine_path_deterministic; layer_path_append | Layer-indexed paths and their supplied original state |
| Identity and accounting | lifted_empty_path_is_identity; zero_price_step_retains_occurrence; occurrence_count_composes; layer_path_length; horizon_two_composition_bound | Exact natural occurrence counts and pairs of natural prices |

The module imports core Lean only. Its selected audit declares
propext, Quot.sound and Classical.choice; the count and guard proofs use
choice through their proof infrastructure. The path lifting and composition
laws avoid it. No custom axiom or admitted proof is introduced. These are
mathematical model results, not verification of the concrete Rust or Python
source, orbit enumeration, or the 29,771 carrier count. Those concrete
obligations are checked by the native tests and independent replay. The final
replay compares all 29,771 raw states and 1,250,382 offers with the bound native
implementation and the pinned original nineteen-file source closure. It checks
1,248,984 member-step lifts across the positive layers of both profiles. Seven
native tests, 72 focused reference tests, and a separate 33-case negative matrix
supply concrete checks; none expands the stated formal-model scope.

The bound, literal action addresses, two terminal conventions, two-edit horizon,
source versions and supplied original start are certificate inputs. Larger
carriers, action transport under renaming, unbounded histories, realizable
observation instruments, higher coherence, physical reconstruction, and
institutional authorization retain their separate obligations. The result
closes this declared finite retention problem;
it does not close GEN-WDP-O02 or GEN-WDP-O03 in their broader scope.
