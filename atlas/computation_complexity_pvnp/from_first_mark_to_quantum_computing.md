# From the first mark to machines, NP and quantum computing

AuthorityEffect: None. A conditional derivation with explicit open boundaries.

## 1. Inscription, admission and a machine that interprets programs

`<>` is not already a binary alphabet. Supply a carrier, identity convention,
forms, admission and replay. The existing `COMP-C1` records construct separated
finite alphabets. `COMP-C2` defines finite words and contextual rewriting.
`COMP-C5` encodes a Turing configuration as end markers, tape cells and a state
mark, and proves forward and backward step simulation. Halting corresponds to
reachability of an irreducible represented word.

The `COMP-C6` construction uses Mathlib's encoded partial-recursive evaluator
and TM2→TM1→TM0 compilation to obtain one fixed machine M₀. On the encoded
pair of a program c and input n, it halts iff evaluation of c on n terminates.
`COMP-C6-FINITE-MARKS` supplies a finite mark set. This is the existing
Universal Turing Machine (UTM) route, conditional on its explicit imports.
The TM0 output decoding result remains `COMP-C6-TM0-OUTPUT-FORM-OPEN`.
Halting equivalence alone should not be quoted as that stronger output theorem.

A finite alphabet is compatible with unbounded word length. A fixed finite
configuration set is not an unbounded machine. `COMP-C4-UNBOUNDED-SUPPLY-IMPORT`
records the necessary supply; permissive event semantics do not generate it.
Binary coding of marks also does not automatically preserve every operational
or time-cost property of a rewriting implementation.

Sources: [the detailed proofs](computation_proofs.md#1-rewriting-over-marks-and-turing-machines),
[the machine research record](../../dag/derivations/29_computation/genesis_to_universal_computation.md),
and [Mathlib's evaluator construction](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Computability/TuringMachine/ToPartrec.html).

## 2. The extra step from computability to complexity

Fix a finite encoding, input length |x| and a uniform machine model that counts
elementary steps. P consists of languages decided by a deterministic machine
in time bounded by a polynomial in |x|. A computable interpreter does not by
itself provide a polynomial simulation theorem; the chosen encoding and
simulation overhead must be accounted for.

NP consists of languages L for which there exist a polynomial p and a
deterministic polynomial-time verifier V such that

    x ∈ L  iff  there exists y with |y| ≤ p(|x|) and V(x,y)=1.

The bound and runtime are uniform over all x. Equivalently, a nondeterministic
polynomial-time machine guesses y and checks it. Conversely, the polynomially
many branch choices of an accepting run form a certificate that a deterministic
machine can replay in polynomial time. This proves the verifier/branching
equivalence under the fixed finite-branching machine model. The letters NP
mean nondeterministic polynomial time, not non-polynomial time.

P⊆NP: the verifier can ignore y and run the P decider. Nothing in that inclusion
proves the converse or a strict separation.

## 3. Where NP appears in the admitted rewriting model

Fix a finite rule list R. Given a,b and a unary bound 1ᵗ, ask whether a reaches
b in at most t rule applications. A certificate lists intermediate words,
rule indices and replacement positions. If c is the largest right-hand-side
length, each word has length at most |a|+tc. At most t local comparisons of
polynomial-size words verify the certificate. Thus the decision language is
in NP for the stated encoding. The witness length is part of the proof.

A binary encoding of t destroys this particular polynomial bound in input
length; it does not, by itself, prove that the resulting language is outside
NP. Likewise, enumerating Σᵢ≤ᴸ kⁱ words gives a search upper bound, not a
lower bound against all algorithms. Length-bounded reachability and
step-bounded reachability are different problem families.

Cook–Levin is an imported theorem connecting polynomial nondeterministic
computation with SAT. A tableau encodes configurations and local transition
constraints, with polynomially many variables and clauses at the stated time
bound. An NP-hardness claim about a particular rewriting or sign problem also
needs its own polynomial reduction; it is not inherited from the word NP.

## 4. P versus NP, encodings and search

P versus NP asks whether every language with such short verifiable witnesses
also has a deterministic polynomial-time decision algorithm. It remains open
in the [official Clay problem statement](https://www.claymath.org/millennium/p-vs-np/).
The route introduces the question and its premises, not an answer.

Two encodings preserve P and NP membership when they translate faithfully in
both directions in polynomial time, with polynomial size bounds and valid
encoding recognition. Composition proves the P statement. For NP, translate
the input and use the verifier of the translated instance, retaining a
polynomial witness bound. An arbitrary computable presentation change is too
weak. For SAT, polynomial decision would give polynomial witness search by
fixing variables and asking satisfiability repeatedly; analogous claims for
other tasks need an explicit search-to-decision reduction.

The retained research note's ETH announcement is not an accepted premise here.
Even a subexponential algorithm does not automatically give a polynomial one.
Counting witnesses, deciding existence, exact amplitudes and sampling require
separate reductions and output/error contracts.

## 5. Reversible classical gates meet an admitted quantum model

For a Boolean function f, (x,y)↦(x,y XOR f(x)) is a permutation and is its own
inverse. To realize it efficiently, a circuit for f must also be supplied;
reversible gates can compute its intermediate values into ancillas, copy the
output and reverse the computation to clear those ancillas. The gate and
workspace overhead must be bounded relative to that circuit.

A finite permutation matrix is unitary under the standard complex inner
product. This embeds the classical reversible circuit in a supplied quantum
model. It does not force that model: phases, linear superposition, tensor
products and the probability rule are new premises. The graph connects this
step to the conditional Hilbert and tensor results and to
[quantum information](../../dag/derivations/13_finite_qm_information/QUANTUM_INFORMATION.md).

## 6. Quantum circuits and BQP

Declare qubit systems, an efficiently specified finite gate set, ancilla
preparation and computational-basis measurement with the Born rule. A
polynomial-time classical algorithm generates Cₙ, whose size is polynomial
in n. BQP contains the decision languages accepted with probability at least
2/3 on yes instances and at most 1/3 on no instances. Uniformity prevents a
noncomputable answer table from being hidden in the circuit family.

Approximation requires an error metric and a precision budget. If an L-gate
circuit replaces each gate by one within operator norm ε/L, a telescoping
sum bounds the total unitary error by ε. Efficient synthesis for a specified
dense gate set is a further theorem. Exact Q(i) matrices alone do not supply
every gate, state normalization, or asymptotic compilation guarantee.

Standard algorithms, error correction and fault tolerance are externally
developed theories with explicit hypotheses; see
[Watrous's course](https://arxiv.org/abs/2507.11536). Repository claims need
matching input families, cost bounds and error contracts. Neither a finite
gate simulation nor an algorithm for factoring decides whether NP⊆BQP or
whether P=NP. Quantum computing is therefore a conditional branch from
classical control plus admitted quantum structure, not a resolution of P/NP.
