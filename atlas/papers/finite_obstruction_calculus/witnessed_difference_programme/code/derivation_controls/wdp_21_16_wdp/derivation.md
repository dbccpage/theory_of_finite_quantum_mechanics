# WDP-21-16-WDP

Goal id: WDP-21-16-WDP

Selected scope for WDP-21-16-WDP is recorded in this note.

## Selected scope

Two unjoined packets already fixed in the opened monograph, not a yes or no to the unbound section 21.16 bullet and not a device. Packet L is the rational two-qubit fixture in `code/locality_smearing/locality.py`: rho and sigma are the matrices of \((|00\rangle+|11\rangle)/\sqrt{2}\) and \((|00\rangle-|11\rangle)/\sqrt{2}\) with entries in \(\{0,\pm 1/2\}\), \(O_R=\mathrm{diag}(1,1,-1,-1)\), \(O=O_R+(1/8)XX\), \(\beta=1/8\). Packet S is Appendix V, Theorem L1, on \(V=\mathbb F_2^3\) with \(Q(x,y,z)=x+y\), \(B=\{000,110\}\), \(E=\mathbb F_2^3\). No Lieb–Robinson triple \((C,\mu,v)\) and no map from the packet-L residual into packet S are in scope.

The opened goal row is `open`, with empty `depends_on` and no fence. Its note says the bullet is a research question, not a register obligation. Its sources are the section 21.16 heading and the Paper 000/WDP bullet. Those lines name none of the four data in the question. No Python, Rust, or Lean kernel was run for this note.

## Hypotheses

H1. Section 21.16 asks whether the discarded correlation residual lies in an unrepairable class modulo stabilizers under local Lieb–Robinson dynamics and bounded readout precision. The bullet names no residual, no repair subspace \(B\), no syndrome, no constants \((C,\mu,v)\), and no precision. The goal note says this is not a register obligation. The arithmetic below does not close the question.

H2. Appendix V separates information discarded by an observer from operations excluded by locality. They meet only at a declared readout, and neither supplies the adapter for the other. An error in \(B\) has quotient obstruction zero. An error outside \(B\) does not become zero by another representative. A Lieb–Robinson tail of the form \(C_R\exp[-\mu(r-v|t|)]\) is an imported hypothesis and is not inferred from the name of a Hamiltonian. An upper bound is not an error floor.

H3. M2-A37 defines the product residual \(\rho_{AB}-\rho_A\otimes\rho_B\) on the composite carrier. For a Hermitian state it has trace zero, and a Hermitian trace-zero matrix is positive semidefinite only when it is zero.

H4. Packet L checks one reduced state on the first qubit. Both single-qubit marginals of \(\rho\) and of \(\sigma\) are \(I/2\), so the product-of-marginals map sends both states to \(I/4\). Their residual difference is \(R=\rho-\sigma\). The only nonzero entries, in the order \(|00\rangle,|01\rangle,|10\rangle,|11\rangle\), are \(R_{0,3}=R_{3,0}=1\). Thus \(\operatorname{Tr}(R)=0\), \(\operatorname{Tr}(R O_R)=0\), and \(\operatorname{Tr}(R O)=1/4\). The stored readout string `1/4` equals \(2\cdot(1/8)\), so the L3 bound is attained on this declared tail. With local separation \(\eta=0\) and target separation \(\delta=1/4\), L4 forces endpoint error \(\alpha\ge 1/8\) for any decoder of that scalar tail from the local scalar report. That is a reconstruction obstruction on these two maps, not a device error floor.

H5. The same \(R\) equals \((XX-YY)/2\), not a rational multiple of the stabilizer \(ZZ=\mathrm{diag}(1,-1,-1,1)\): \(\operatorname{Tr}(R\,ZZ)=0\) while \(R\) is not zero. The \(\mathbb F_2\) sum of the Pauli support vectors \(XX=(1,1\mid 0,0)\) and \(YY=(1,1\mid 1,1)\) is the support vector of \(ZZ\). That sum is a different object from the signed operator residual, and it is not an encoding of \(R\) into packet S.

H6. Packet S has \(\ker Q=\{000,001,110,111\}\), \(B=\{000,110\}\), and \(000+001=001\notin B\), so \((E-E)\cap\ker Q\) is not contained in \(B\). Because \(E\) is a linear subspace containing \(B\), Theorem L2 gives the minimum number of extra rows as \(\dim(\ker(Q|E)/B)=1\). That integer is a binary hitting number. It is not \(\operatorname{Tr}(R O)\), not the matrix entry \(R_{0,3}\), and not a Lieb–Robinson constant.

H7. No opened carrier places \(R\), or either product residual, in a quotient \(\ker Q/B\) while also instantiating a summed Lieb–Robinson tail. The finite obstruction is this missing adapter. The static identities \(1/4\), \(0\), and \(1\) do not decide the section 21.16 conjunction, and they are not a continuum limit, a physical law, or a theorem outside these two packets.

## Derivation

The two packets stay on their own carriers. Neither value answers the unbound section 21.16 bullet.

### 1. Packet L: the rational Bell readout

Order the basis \(|00\rangle,|01\rangle,|10\rangle,|11\rangle\). The pure-state matrices are

\[
\rho=\begin{pmatrix}1/2&0&0&1/2\\0&0&0&0\\0&0&0&0\\1/2&0&0&1/2\end{pmatrix},\qquad
\sigma=\begin{pmatrix}1/2&0&0&-1/2\\0&0&0&0\\0&0&0&0\\-1/2&0&0&1/2\end{pmatrix}.
\]

These are the matrices returned by `fixture`. The companion operator is \(O_R=\mathrm{diag}(1,1,-1,-1)\), which is \(Z\otimes I\), and

\[
O=O_R+\frac18 XX,\qquad \beta=\frac18,
\]

where \(XX\) is the real matrix with ones in positions \((0,3)\), \((3,0)\), \((1,2)\), and \((2,1)\). The code adds \(1/8\) exactly on those anti-diagonal places. The file `replay.py` stores the submitted readout string `1/4`. The trace below is the matrix calculation that string names. It was not produced by executing the checker.

The partial trace over the second qubit is the sum the fixture's `marginal` uses. For both states it equals \(I/2\):

\[
\rho_A=\begin{pmatrix}\rho_{00}+\rho_{11}&\rho_{02}+\rho_{13}\\\rho_{20}+\rho_{31}&\rho_{22}+\rho_{33}\end{pmatrix}
=\begin{pmatrix}1/2&0\\0&1/2\end{pmatrix},
\]

and the same eight entries of \(\sigma\) agree. The partial trace over the first qubit is also \(I/2\), because

\[
(\rho_B)_{00}=\rho_{00}+\rho_{22}=1/2,\qquad (\rho_B)_{11}=\rho_{11}+\rho_{33}=1/2,
\]

and the cross sums \(\rho_{01}+\rho_{23}\) and \(\rho_{10}+\rho_{32}\) are zero. The coherences \(\rho_{03}\) and \(\rho_{30}\) do not enter either partial trace. The same holds for \(\sigma\). Therefore

\[
\Pi(\rho)=\Pi(\sigma)=(I/2)\otimes(I/2)=I/4.
\]

M2-A37 places the product residual on the composite carrier. Each residual has trace \(1-1=0\). A Hermitian matrix of trace zero is positive semidefinite only if every eigenvalue is zero, hence only if the matrix is zero. Both residuals are nonzero: the computational vector \(|01\rangle\) has expectation \(-1/4\) on each of \(\rho-I/4\) and \(\sigma-I/4\). Their difference cancels \(I/4\),

\[
R=(\rho-I/4)-(\sigma-I/4)=\rho-\sigma.
\]

The diagonal cancels and the corner coherences add, so \(R_{0,3}=R_{3,0}=1\) and every other entry is zero. In particular \(\operatorname{Tr}(R)=0\). Since \(O_R\) is diagonal, \(\operatorname{Tr}(R O_R)=0\). The same diagonal pairing gives \(\operatorname{Tr}(R\,ZZ)=0\) for \(ZZ=\mathrm{diag}(1,-1,-1,1)\). The only surviving pairing with \(O\) is the anti-diagonal of \((1/8)XX\):

\[
\operatorname{Tr}(R O)=R_{0,3}O_{3,0}+R_{3,0}O_{0,3}=\frac18+\frac18=\frac14.
\]

Thus the stored string `1/4` equals the trace, and \(1/4=2\beta\).

The tail is exactly \((1/8)XX\), not an exponential envelope. \(X^2=I\) gives \((XX)^2=I\). \(XX\) is Hermitian, so its eigenvalues are \(\pm 1\) and \(\|XX\|_\infty=1\). Hence \(\|O-O_R\|_\infty=1/8=\beta\). The nonzero block of \(R\) is \(\begin{pmatrix}0&1\\1&0\end{pmatrix}\), with singular values \(1,1\), and the other two singular values are zero, so \(\|R\|_1=2\). Theorem L3 therefore reads

\[
|\operatorname{Tr}(R O)|\le\|R\|_1\beta\le 2\beta,
\]

and both comparisons are equalities on this fixture: \(1/4=2\cdot(1/8)\). Attainment is a finite identity for these matrices. Appendix V states that a Lieb–Robinson upper bound is not a reconstruction-error floor, and this note does not turn the attained upper bound into one. No constants \((C,\mu,v)\) are fixed, and the name of a Hamiltonian is not used.

The scalar local reports agree. \(\operatorname{Tr}(\rho O_R)=(1/2)(1)+(1/2)(-1)=0\), and the same diagonal computation gives \(\operatorname{Tr}(\sigma O_R)=0\). The scalar full reports are

\[
\operatorname{Tr}(\rho O)=\frac18\operatorname{Tr}(\rho\,XX)=\frac18,\qquad
\operatorname{Tr}(\sigma O)=-\frac18,
\]

because \(\operatorname{Tr}(\rho\,XX)=1\) and \(\operatorname{Tr}(\sigma\,XX)=-1\). Their separation is \(\delta=1/4\). Take the report map to be \(\operatorname{Tr}(\,\cdot\,O_R)\), so the readout separation is \(\eta=0\), and take the targets to be these two full reports. Theorem L4 says \(\delta\le 2\alpha+\kappa\eta\). The \(\kappa\) term drops, and \(\alpha\ge\delta/2=1/8\). The same half-separation is the common-report sentence in Appendix V and in §10.7. It is an obstruction to stable reconstruction from that local scalar. It is not a lower bound on the physical error of a device, and it is not a waiting time \(T\ge r/v\).

The region supporting \(O_R\) is the first qubit. Agreement of the reduced states on that qubit is the hypothesis used for \(\operatorname{Tr}(R O_R)=0\). Equal single-site marginals do not, by the monograph's warning, give equal joint marginals on a larger region. Here they do not: \(\rho\neq\sigma\). The fixture does not claim a two-qubit joint marginal equality.

### 2. The signed residual is not the support sum

Use \(Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix}\), so \(Y|0\rangle=i|1\rangle\) and \(Y|1\rangle=-i|0\rangle\). Then

\[
YY|00\rangle=-|11\rangle,\quad YY|11\rangle=-|00\rangle,\quad YY|01\rangle=|10\rangle,\quad YY|10\rangle=|01\rangle.
\]

Subtracting from \(XX\) cancels the middle anti-diagonal and doubles the corners:

\[
XX-YY=\begin{pmatrix}0&0&0&2\\0&0&0&0\\0&0&0&0\\2&0&0&0\end{pmatrix},\qquad
\frac{XX-YY}{2}=R.
\]

If \(c\,ZZ=R\), the diagonal \((c,-c,-c,c)\) is zero, so \(c=0\), but \(R\neq 0\). Thus \(R\) is not a rational multiple of \(ZZ\).

The phase-forgetting two-qubit support map sends \(XX\) to \((1,1\mid 0,0)\) and \(YY\) to \((1,1\mid 1,1)\). Their sum in \(\mathbb F_2^4\) is

\[
(0,0\mid 1,1),
\]

the support vector of \(ZZ\). The operator sum \(XX+YY\) is a different matrix, with \(2\) in positions \((1,2)\) and \((2,1)\) and zeros elsewhere. Neither that sum nor the support vector equals \(R=(XX-YY)/2\). The support vector has four coordinates. Packet S lives in \(\mathbb F_2^3\). No padding, projection, or isomorphism between those carriers is written in `locality.py`, `finite.py`, or the L1 paragraph.

### 3. Packet S: the three-bit fiber

\(Q(x,y,z)=x+y=0\) forces \(x=y\), with \(z\) free. Thus

\[
\ker Q=\{000,001,110,111\},\qquad B=\{000,110\}.
\]

Both generators of \(B\) lie in the kernel. The whole carrier \(E=\mathbb F_2^3\) is a subspace containing \(B\), so \(E-E=E\) and \((E-E)\cap\ker Q=\ker Q\). The vector \(001\) lies in the kernel and outside \(B\). In particular \(Q(000)=Q(001)=0\) and \(000+001=001\notin B\). The inclusion asked by the Majorana wording of L1 fails on this example. The quotient \(\ker Q/B\) has the two classes \(\{000,110\}\) and \(\{001,111\}\).

Theorem L2 says that when \(E\) itself is a linear subspace containing \(B\), the minimum number of added rows is \(\dim(\ker(Q|E)/B)\). Here that dimension is \(2-1=1\). The monograph exhibits one row, the coordinate \(z\): it annihilates \(B\) because the third bit of \(110\) is \(0\), and it is nonzero on \(001\). Zero rows leave the collision. The exact minimum on this example is one. `test_finite.py` asserts that same minimum for these rows, errors, and repairs. That assertion was not re-executed.

The integer \(1\) equals the numeral \(R_{0,3}\) and does not equal \(\operatorname{Tr}(R O)=1/4\). Equality of the numerals \(1\) and \(1\) does not move the hitting number onto the matrix carrier. The cosets above are not indexed by \(1/4\) or by the row budget. L2 also says the dimension formula is not asserted for an arbitrary restricted \(E\). This application uses that \(E\) is the whole subspace.

### 4. The packets do not decide the conjunction

Packet L supplies a \(4\times 4\) rational matrix \(R\), a declared tail norm \(1/8\), a readout \(1/4\), and a conditional reconstruction bound \(\alpha\ge 1/8\) for one pair of scalar maps. Packet S supplies a failed fiber inclusion and a hitting number \(1\) on \(\mathbb F_2^3\). Appendix V says the discarded-information restriction and the locality restriction do not supply each other's adapter. Section 10.6 says the physical-residual-to-cochain adapter must still be supplied separately. No opened text supplies a map that sends \(R\), or either product residual \(\rho-I/4\) or \(\sigma-I/4\), into \(\ker Q/B\), and no opened text instantiates \((C,\mu,v)\) for this bullet.

The static identities on these packets are \(1/4\), \(0\), and \(1\): the readout, the several zero pairings and the local separation, and the binary minimum. They do not decide whether one discarded correlation residual lies in an unrepairable class modulo stabilizers under local Lieb–Robinson dynamics and a bounded readout precision. The bullet stays open. It is not a register obligation.

Nonclaim 23 already refuses the nearest reading that would skip the adapter: a positive product-projection residual is not a computational or logical failure, and a raw residual bound is not an obstruction modulo repairs unless an adapter and a repair space are declared. Those two data are not declared for this bullet. GEN-WDP-56 repeats the split between the finite readout deduction and the imported analytic Lieb–Robinson hypothesis. Section 22.4 refuses Tier-4 selection of continuum spacetime or a physical law from the finite calculus. Section 22.6 says the monograph does not become a physical theory by declaration.

A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Claims this note does not make

- It does not answer section 21.16 yes or no. The bullet names no residual, no repair subspace, no syndrome, no Lieb–Robinson constants, and no precision. The question stays open outside the two packets above, and it is not a register obligation.
- It does not place \(R\), \(\rho-I/4\), \(\sigma-I/4\), the readout \(1/4\), or the hitting number \(1\) in a quotient \(\ker Q/B\). The numeral agreement of \(1\) with \(R_{0,3}\) is not that placement. Neither numeral is a class index of a coset.
- It does not treat the \(\mathbb F_2^4\) support sum \((0,0\mid 1,1)\), or the operator \(ZZ\), as an encoding of \(R=(XX-YY)/2\). It does not treat packet S as the Majorana bullet.
- It does not infer a triple \((C,\mu,v)\), a tail \(C_R\exp[-\mu(r-v|t|)]\), or an error floor from this fixture or from the name of a Hamiltonian. The tail used here is \((1/8)XX\), with \(\|(1/8)XX\|_\infty=1/8\) because \((XX)^2=I\).
- It does not turn L4 into a device error. The bound \(\alpha\ge 1/8\) is the reconstruction obstruction for the declared scalar report \(\operatorname{Tr}(\,\cdot\,O_R)\) and the declared targets \(\operatorname{Tr}(\,\cdot\,O)\) on this fixture. Section 10.7 states that no exact waiting threshold \(T\ge r/v\) follows from an exponential upper envelope without its constants, the desired precision, and lower evidence. None of those data are in scope.
- It does not identify the nonzero product residuals with a computational or logical failure. Nonclaim 23 refuses that reading unless an adapter and a repair space are declared.
- It does not import, as a witness for this bullet, the Appendix P.19.c two-qubit envelope, the degree-1 classes ExactClass, ClosedResidual, and ActiveClosureFailure, the zero-row quotient charge, the toric schedule, Chapter 23's P15C–P16C comparisons, Appendix Y.6's costs, or Paper 000's Ising-ring identity. Those statements stay on their own carriers and were not replayed.
- It does not run the Python checker, the unit tests, the Lean encoding, or a Rust port. The identities above are matrix arithmetic and the subspace count on the two packets.
- It does not establish a continuum limit, a physical law, or a closed theorem outside these two packets.
