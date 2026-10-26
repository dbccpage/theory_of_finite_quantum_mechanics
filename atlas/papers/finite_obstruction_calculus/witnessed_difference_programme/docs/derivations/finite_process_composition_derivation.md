# Certified finite process composition and the exact gate boundary

**Status:** finite conditional derivation with a core-only two-dimensional Lean
model and exact Gaussian-rational replay.

**Purpose:** continue from certified states/effects to transformations,
sequential composition, measurement branches and finite tensor composition.
The derivation also identifies the exact scalar obstruction between the
current \(\mathbb Q(i)\) carrier and standard gate presentations.

## 1. State factors and process factors

Use the Gram-factor state language of the preceding derivation.  An ensemble
of matrices \(B_s\) presents

\[
T=\sum_s\|B_s\|_F^2>0,
\qquad
\rho=\frac1T\sum_s B_s^\dagger B_s.
\tag{1.1}
\]

A finite **process certificate** is a labelled family of
Gaussian-rational matrices \((K_o)_{o\in O}\) satisfying

\[
\sum_o K_o^\dagger K_o=I.
\tag{1.2}
\]

For outcome \(o\), replace each input factor by

\[
B_{s,o}'=B_sK_o^\dagger.
\tag{1.3}
\]

Then

\[
(B_{s,o}')^\dagger B_{s,o}'
=K_oB_s^\dagger B_sK_o^\dagger,
\]

so the branch factors present the unnormalized branch state.  The branch mass
and probability are

\[
T_o=\sum_s\|B_sK_o^\dagger\|_F^2,
\qquad
p_o=T_o/T.
\tag{1.4}
\]

If \(T_o>0\), the normalized conditional state is the Gram normalization of
the branch factors.  If \(T_o=0\), the outcome is impossible and no normalized
post-state is manufactured.

## 2. Finite process theorem

`GEN-WDP-66` **Finite conditional theorem (certified process composition).**
For an ensemble state satisfying (1.1) and a process certificate satisfying
(1.2):

1. every branch probability is nonnegative;
2. \(\sum_op_o=1\);
3. the unconditioned output is
   \(\mathcal E(\rho)=\sum_oK_o\rho K_o^\dagger\);
4. sequential certified processes \((K_o)\), then \((L_r)\), have composite
   factors \(L_rK_o\);
5. certified processes on independent carriers tensor to the family
   \(K_o\otimes L_r\);
6. a one-factor process with \(U^\dagger U=I\) preserves mass, and application
   of \(U^\dagger\) reverses the factor update.

All conclusions are exact over \(\mathbb Q(i)\).

### Proof: trace preservation

Using cyclicity of trace and (1.2),

\[
\begin{aligned}
\sum_oT_o
 &=\sum_{s,o}\operatorname{tr}
   (B_sK_o^\dagger K_oB_s^\dagger)\\
 &=\sum_s\operatorname{tr}
   \left(B_s\left(\sum_oK_o^\dagger K_o\right)B_s^\dagger\right)\\
 &=\sum_s\operatorname{tr}(B_sB_s^\dagger)\\
 &=\sum_s\|B_s\|_F^2=T.
\end{aligned}
\]

The branch values are sums of Gaussian-rational squares, so they are
nonnegative.  Division by \(T>0\) gives normalization.

### Proof: sequential composition

Applying \(K_o\) and then \(L_r\) sends a factor to

\[
(B_sK_o^\dagger)L_r^\dagger
=B_sK_o^\dagger L_r^\dagger
=B_s(L_rK_o)^\dagger.
\]

The composite family is complete:

\[
\begin{aligned}
\sum_{o,r}(L_rK_o)^\dagger(L_rK_o)
 &=\sum_o K_o^\dagger
   \left(\sum_rL_r^\dagger L_r\right)K_o\\
 &=\sum_oK_o^\dagger K_o=I.
\end{aligned}
\]

### Proof: tensor composition

For complete families on \(H_A,H_B\),

\[
\begin{aligned}
\sum_{o,r}(K_o\otimes L_r)^\dagger(K_o\otimes L_r)
 &=\left(\sum_oK_o^\dagger K_o\right)
   \otimes
   \left(\sum_rL_r^\dagger L_r\right)\\
 &=I_A\otimes I_B.
\end{aligned}
\]

This proves the finite algebraic composite once the subsystem tensor product
has been admitted.  It does not infer that a given physical system has that
factorization.

## 3. Channels do not determine instruments

An unconditioned channel forgets outcome labels.  That loss is mathematically
real, even when the output density is preserved exactly.

`GEN-WDP-67` **Finite countermodel (instrument nonselection).** The one-outcome
instrument

\[
\{I\}
\]

and the two-outcome instrument

\[
\left\{\frac35I,\frac45I\right\}
\]

induce the same identity channel, because

\[
\left(\frac35\right)^2+
\left(\frac45\right)^2=1.
\]

Their outcome reports differ: the first has probability vector \((1)\), while
the second has \((9/25,16/25)\) for every state.

Therefore a representation retaining only the unconditioned channel can
preserve the current output state while losing future conditioning,
authorization, cost or branch questions.  Instrument labels must be protected
explicitly when those questions matter.  This is the process-level instance of
the contextual-congruence criterion derived earlier.

## 4. Exact Gaussian-rational gates

Several familiar gates are exact over \(\mathbb Q(i)\):

\[
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad
S=\begin{pmatrix}1&0\\0&i\end{pmatrix},
\]

and permutation gates such as CNOT have entries in \(\{0,1\}\).  The Lean
fixture proves exact unitarity, mass preservation, basis transport and the
round trip for \(X\).

The standard Hadamard gate is different:

\[
H=\frac1{\sqrt2}
\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
\]

`GEN-WDP-68` **Exact scalar obstruction.** There is no
\(r\in\mathbb Q\) with \(r^2=1/2\).  Hence the standard Hadamard matrix is not
a matrix over \(\mathbb Q(i)\).  The same missing scalar occurs in the usual
\(T\)-phase \((1+i)/\sqrt2\).

### Proof

Suppose \(r=p/q\) in lowest terms with \(q>0\) and
\(p^2/q^2=1/2\).  Then

\[
2p^2=q^2.
\]

Thus \(q^2\) is even, so \(q\) is even.  Write \(q=2k\).  Then
\(p^2=2k^2\), so \(p\) is even.  This contradicts coprimality of \(p,q\).

The Python checker uses the equivalent exact numerator/denominator
perfect-square test for the submitted scalar request.

This obstruction concerns exact representation in the current field.  It does
not prove that Gaussian-rational unitaries cannot approximate Hadamard, nor
that no alternative rational universal gate set exists.  Approximate
universality requires a topology, an error metric, a finite gate alphabet and
a convergence/compilation theorem.  Exact use of the standard Clifford+T
presentation instead requires at least the algebraic extension containing
\(1/\sqrt2\).

## 5. Measurement and conditioning fixture

For the plus-state factor

\[
B=\begin{pmatrix}1&1\\0&0\end{pmatrix},
\]

the projective factors

\[
P_0=\begin{pmatrix}1&0\\0&0\end{pmatrix},
\qquad
P_1=\begin{pmatrix}0&0\\0&1\end{pmatrix}
\]

give exact probabilities \((1/2,1/2)\) and conditional density matrices
\(|0\rangle\!\langle0|\), \(|1\rangle\!\langle1|\).  The replay separately
checks:

- sequential application versus the composite operator family;
- total-mass preservation;
- branch probabilities and conditioned states;
- a four-dimensional tensor product process;
- the channel/instrument counterexample;
- refusal of an incomplete process;
- the exact Hadamard scalar obstruction.

## 6. WDP/CODA/LGGR consequences

- **WDP:** a process certificate binds the source task, scalar field, state
  factors, ordered operator family, outcome labels, composition history and
  requested reports.  Equality of unconditioned channels is insufficient when
  labels or postselection are protected.
- **CODA/Prime:** proposal of an operator family, completeness checking,
  execution, branch evaluation and authorization remain separate.  A complete
  Kraus family is mathematically trace preserving; it is not automatically an
  authorized physical intervention.
- **LGGR:** local operator validity and global composition are distinct.  A
  tensor or sequential composite is admitted only after its carrier maps and
  completeness equations are checked.
- **Projection Obstruction:** forgetting outcomes projects an instrument to a
  channel.  The identity-instrument counterexample is an explicit collision
  showing which future branch questions fail to descend.
- **DDC:** search may propose factors or gates, but decreasing a residual does
  not replace the exact completeness, scalar-membership and composition
  checks.

## 7. Evidence boundary

The core-only Lean module
[`FiniteProcessComposition.lean`](../../lean4/WitnessedDifference/FiniteProcessComposition.lean)
proves two-by-two matrix associativity, dagger reversal, branch/readout mass
equality, binary mass partition, sequential branch composition, unitary mass
preservation/reversal and the exact \(X\)-gate fixture.

The executable reference in
[`code/process_composition`](../../code/process_composition) works in arbitrary
finite matrix dimension over exact \(\mathbb Q(i)\).  It adds ensembles,
finite Kraus families, conditioned branches, sequential and tensor process
composition, instrument nonselection and the gate-field control.  The Lean
module proves the selected dimension-two algebra; it does not verify the
Python implementation or its arbitrary-dimension loops.

## 8. Path to Bell and quantum computation

The foundational chain has now reached:

\[
\begin{aligned}
&\text{typed histories}
\to\text{signed/tensor carrier}
\to\text{dagger and observer Gram form}\\
&\to\mathbb Q(i)\text{-Hermitian carrier}
\to\text{certified states/effects/readout}
\to\text{certified finite processes}.
\end{aligned}
\]

For a Bell theorem, one must next bind a bipartite tensor realization, two or
more local setting-indexed instruments per party, commuting/spacelike locality,
the admitted trace readout and the empirical independence assumptions.  The
paper's existing conditional CHSH result can then be attached to this newly
constructed finite interface rather than treated as an isolated import.

For quantum computing, one must choose either:

1. an exact algebraic scalar extension and gate set, then prove generation of
   the intended finite transformations; or
2. a completed scalar/topological model, an approximation norm, an error
   budget and a compiler theorem for a finite universal gate alphabet.

Neither route follows from finite process composition alone.

## 9. Next dependency

The next high-value derivation is a **Bell-local operational closure theorem**
on the constructed interface: state the exact tensor, setting, locality,
free-choice and readout assumptions; derive the classical factorizable bound
and quantum Tsirelson bound as separate certificate regimes; and show which
observer quotients preserve or destroy the Bell question.  That result would
connect the WDP notion of retained questions directly to Bell's demand that
physical knowledge be stated without hiding the experimental conditions.
