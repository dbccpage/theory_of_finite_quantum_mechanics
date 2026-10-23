# Selected package Q2: a finite bipartite representation

**Status.** Selected finite derivation for the broader-work column of
`CH18-O01`. The signed block-mass criterion and the instrument-quotient
criterion stay where Appendix J.4 and `docs/swarm_qm_reconstruction.md`
already put them. This note does not replace those classifications, and it
does not change the canonical ledger row `WDP-CH18-O01` or the nonclaim
`CH18-N01`.

**Witness.** `q2-reconstruction-package`,
`problem_sha256` `79e7c3c6fdc2d19c132ee11bd5b9a5e8bf3cf29488d83cfff21ee6a77fb8aece`,
receipt
[`evidence/q2_reconstruction_package_receipt.json`](../../evidence/q2_reconstruction_package_receipt.json).
The checker is
[`code/witnessed_difference/q2_reconstruction_package.py`](../../code/witnessed_difference/q2_reconstruction_package.py).

## 1. What is being selected

The open remainder asks for one reconstruction package, the assumptions that
package adds, and a representation argument that is not the block-mass theorem
and not the instrument-quotient theorem. The package selected here is **Q2**,
a finite two-qubit correlation representation. It is one admitted route. It is
not forced by primitive difference, by package S, or by CP.

## 2. Additional assumptions

The following are hypotheses of Q2. None is a theorem of nonnegative block
masses or of a stochastic report quotient.

1. **(H) Carrier.** Each local system is the standard Hermitian space
   \(\mathbb C^2\). The composite carrier is the Hilbert tensor product
   \(\mathbb C^2\otimes\mathbb C^2\), so the multiplicity allowed by a general
   commuting matrix-unit classification is fixed at \(r=1\).
2. **(O) Local observables.** For settings \(x,y\in\{0,1\}\) the local
   operators \(A_x\) and \(B_y\) are Hermitian and satisfy
   \(A_x^2=B_y^2=I_2\).
3. **(S) State.** The composite state \(\rho\) is positive semidefinite and
   has trace one.
4. **(B) Readout.** Outcomes \(a,b\in\{+1,-1\}\) are read by the trace pairing
   \[
   p(a,b\mid x,y)
   =\operatorname{tr}\Bigl(\rho\,
     \tfrac{I+a A_x}{2}\otimes\tfrac{I+b B_y}{2}\Bigr).
   \]
   This Born pairing is supplied. Gauge invariance and normalization do not
   select it.

A **Q2-representation** of a rational no-signalling table is a tuple
\((\rho,A_0,A_1,B_0,B_1)\) satisfying (H), (O), (S) and (B) and reproducing
that table.

## 3. Correlators and the square identity

Write \(P=B_0+B_1\), \(Q=B_0-B_1\) and
\[
S=A_0\otimes P+A_1\otimes Q.
\]
Hermiticity of the local observables makes \(P\) and \(Q\) Hermitian.
Expanding \(B_0^2=B_1^2=I\) gives the two scalar equations
\[
P^2+Q^2=4I, \qquad PQ+QP=0.
\]
The second says \(PQ=-QP\). The commutator is then
\[
C_B=[B_0,B_1]=QP=-PQ,
\]
and \(C_A=[A_0,A_1]\). Expanding \(S^2\) and substituting these relations
yields
\[
S^2=4I-C_A\otimes C_B.
\]
The same expansion with the opposite sign produces the Gram form used for the
bound. Because \(A_0,A_1\) are Hermitian involutions,
\[
2I+i C_A=(A_0+i A_1)^\dagger(A_0+i A_1),
\qquad
2I-i C_A=(A_0-i A_1)^\dagger(A_0-i A_1),
\]
and likewise for \(B\). Both factors are positive semidefinite, and so are
their tensor products. Averaging the two crossed products gives
\[
8I-S^2
=\frac12\Bigl(
(2I+i C_A)\otimes(2I-i C_B)
+(2I-i C_A)\otimes(2I+i C_B)
\Bigr)\succeq 0.
\]
For \(s=\operatorname{tr}(\rho S)\) the operator \((S-s I)^2\) is positive
semidefinite, so
\[
0\le\operatorname{tr}\bigl(\rho(S-s I)^2\bigr)
=\operatorname{tr}(\rho S^2)-s^2.
\]
Positivity of \(8I-S^2\) likewise gives \(\operatorname{tr}(\rho S^2)\le 8\).
Hence every Q2-representation obeys
\[
s^2\le 8.
\]
No irrational root is required to state the bound. The identity
\(S^2=4I-C_A\otimes C_B\) is an equality of finite matrices once the local
operators are given.

## 4. The rational representation

Take the Bell projector in the ordered basis \(\lvert00\rangle,\lvert01\rangle,
\lvert10\rangle,\lvert11\rangle\),
\[
\rho=\frac12\begin{pmatrix}
1&0&0&1\\
0&0&0&0\\
0&0&0&0\\
1&0&0&1
\end{pmatrix},
\]
and the local directions
\[
A_0=Z,\quad A_1=X,\quad
B_0=\frac{3Z+4X}{5},\quad
B_1=\frac{3Z-4X}{5}.
\]
Each square is \(I_2\), because \(X^2=Z^2=I\) and
\((3/5)^2+(4/5)^2=1\), while \(X\) and \(Z\) anticommute. The only nonzero
blocks of \(\rho\) give the four correlators
\[
\operatorname{tr}(\rho\, A_x\otimes B_y)
\in\Bigl\{\tfrac35,\tfrac35,\tfrac45,-\tfrac45\Bigr\}
\]
in setting order \((0,0),(0,1),(1,0),(1,1)\). Their CHSH combination is
\[
s=\frac{3}{5}+\frac{3}{5}+\frac{4}{5}-\Bigl(-\frac{4}{5}\Bigr)=\frac{14}{5}.
\]
Then \(s^2=196/25\) and \(8-s^2=4/25\). Direct matrix multiplication on this
tuple confirms \(S^2=4I-C_A\otimes C_B\) and
\(\operatorname{tr}(\rho S^2)=s^2\), so the variance slack vanishes while the
operator slack does not. The four local marginals
\(\operatorname{tr}(\rho\, A_x\otimes I)\) and
\(\operatorname{tr}(\rho\, I\otimes B_y)\) are zero, and therefore
\[
p(a,b\mid x,y)=\frac{1+ab\,c(x,y)}{4}
\]
agrees with the trace formula in assumption (B). All sixteen probabilities
are rational and are stored in the receipt.

This tuple is a Q2-representation of that table. The representation is not
claimed to be unique.

## 5. Separation from the two classifications already on record

**Classical joints.** Every deterministic assignment of signs
\((a_0,a_1,b_0,b_1)\) has CHSH value \(\pm 2\): if \(b_0=b_1\) the expression
collapses to \(2 a_0 b_0\), and if \(b_0=-b_1\) it collapses to
\(2 a_1 b_0\). The receipt enumerates all sixteen assignments. A nonnegative
joint distribution is a mixture of these assignments, so its expectation lies
in \([-2,2]\). The represented table has expectation \(14/5>2\), so it has no
nonnegative global section on the four classical coordinates. Nonnegative
block mass of a report partition is a different predicate: it can hold for a
classical joint with CHSH at most \(2\), and it can hold for the observable
PR marginals, which are nonnegative, while those marginals have CHSH \(4\).

**The instrument quotient.** A fiberwise constant signed hidden update with a
nonnegative stochastic quotient represents a classical report instrument. It
does not supply Hermitian involutions, a tensor factorisation, or the trace
pairing (B). Q2 does not call that quotient. Conversely, the existence of a
Q2-representation is not a fibre-intertwining statement about a report
partition of a hidden classical carrier.

**Block mass is not sufficient for Q2.** The PR table
\(p(a,b\mid x,y)=(1+(-1)^{xy} ab)/4\) has nonnegative observable blocks and
total mass one, and its CHSH value is \(4\). Since \(4^2=16>8\), assumption
set (H)+(O)+(S)+(B) admits no representation of PR. The same table is the
standard obstruction to a nonnegative joint. So passing the observable
block-mass test, or failing it, does not decide Q2-representability, and the
Q2 bound does not decide classical block mass.

**Signed full-effect readout remains a separate no-go.** The weight
\((2,-1)\) still has a negative coordinate. Q2 does not interpret that
coordinate as a trace probability, and this note does not reopen the
full-effect classical obstruction.

## 6. What the package does not pay

- Q2 is admitted, not derived from W1–W6, from package S, or from CP.
- The trace readout (B) is an extra assumption. Phase-blind quadratic and
  quartic rules remain distinct under gauge descent.
- Multiplicity \(r=1\) is an extra dimension clause. A commuting matrix-unit
  pair of sizes \(2\) and \(2\) on a larger space is a different package.
- The eight external interfaces of §18.5 stay external. In particular this
  note does not supply Gleason's theorem, Stone's theorem, a continuous field,
  or a CPTP dilation.
- One rational table inside the bound is not a membership test for every
  quantum correlation. Satisfying \(s^2\le 8\) is necessary under Q2 and is
  not sufficient for the existence of a Q2-representation.
- No physical apparatus, calibration, or operational model selection is
  identified. Those remain `CH19-O04` and the other open interface rows.
- The canonical conditional row `WDP-CH18-O01` already records the block-mass
  and instrument-quotient classifications and the PR obstruction. This
  supplement discharges only the selected-package remainder named by the goal
  DAG. It does not mark the manuscript nonclaim withdrawn.

## 7. Replay

From the programme directory, with `code` on `PYTHONPATH`:

```text
python -m pytest -o addopts='' -q code/unit_tests/test_q2_reconstruction_package.py
```

The test rebuilds the matrices over `Fraction`, checks the square identity,
the sixteen Born probabilities, the deterministic CHSH census, and the
receipt digest.
