# The five components of the source observer-relative world

The exact original `001_from_primitive_difference_to_cochain_systems/manuscript.md`
lines 1707–1730 defines
an observer-relative world with five components. To avoid the source's use of
$W_O$ for both the tuple and its witness relation, write
$\mathcal W_O=(\operatorname{im}p_O,C_O,H_O,\mathsf{Wit}_O,G_O)$:
presented profiles, admissible contexts, retained histories, witness relations
and report grammar. It is distinct from
both the Genesis six and the compressed policy five. The source states that its
assembly from an observer is provisional. The following supplies an adapter
without interpreting a history carrier as an update function.

Declare the actual history domain H, the presented profile map q:H→P with
P=image(q), each actual context c:H→H, and the actual witness relation. Define
the WDP presentation to be `(H,P,q,{c})`, retain the witness relation and grammar
verbatim, and attach no memory update, evaluator or policy. This construction
preserves every presentation and contextual witness by substitution. It is
defined exactly when the maps have their stated types and the claimed witness
receipts replay. A context witness `(x,y,c)` requires q(x)=q(y) and
q(c(x))≠q(c(y)). The family may be noncongruent: no quotient context is invented.

To move the contexts onto P requires q(c(x))=q(c(y)) whenever q(x)=q(y).
Necessity evaluates the same presented input twice; sufficiency defines
`c_P(q(x))=q(c(x))`, independently of representative. Surjectivity gives
uniqueness. `ObserverAdapterCompleteness.unique_factorization_iff` proves this
criterion for arbitrary declared history types. It applies to an unbounded
source history function as a mathematical statement; an executable finite table
only verifies its explicitly declared finite domain. The Genesis transducer
owner separately verifies all-word descent for checked finite transducers.

The source's facts are grammar-expressible, context-stable subsets of P. A finite
grammar of names does not declare which subset each name expresses. Given an
explicit interpretation e:G→P(P), the exact forward-stability criterion for S is
`q(h)∈S ⇒ q(c(h))∈S` for every h,c. It is necessary by the definition of
stability, sufficient under each declared context, and then holds under every
finite composition by induction. The fact set is precisely the image of e
restricted to subsets meeting this criterion; duplicate expressions produce
one subset. Without e, two interpretations of identical grammar names can yield
different facts, so no unique fact enumeration follows from the five fields.

`omega_wdp::observer_world_adapter` stores actual words on a declared alphabet,
the exact profile image, total context tables closed on that history domain,
the verified witness triples and the separate grammar interpretation. It
delegates contextual structure to `omega_category_theory::context_reflection`.
The Python implementation independently checks the same data. Receipt replay
binds the actual source maps and interpretation. No append closure or bound on
all original histories is inferred from a closed finite context restriction.

Necessary-hypothesis countermodels reject an unused advertised profile, a
context leaving the history domain and a false witness. The three-history
fixture has profiles `(0,0,1)` and context `(0,2,2)`; its witness `(0,1,c)`
shows exactly why the context does not descend to profile equality. Grammar
interpretations of the same names give either one or two stable subsets. A
changed interpretation invalidates the original receipt. These are actual
semantic distinctions, rather than assertions about tuple arity.
