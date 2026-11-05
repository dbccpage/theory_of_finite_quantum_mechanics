# WDP-21-16-MAJORANA

Goal id: WDP-21-16-MAJORANA

Selected scope for WDP-21-16-MAJORANA is recorded in this note.

## Selected scope

Two labelled packets already fixed in the opened monograph, not a yes or no to the unbound section 21.16 Majorana bullet and not a device.

The opened goal row is `open`, with empty `depends_on` and no fence field. Its note says the bullet is a research question, not a register obligation. Its sources are the section 21.16 heading and the Majorana bullet. Those lines name neither a matrix nor an error list.

1. Packet A. Appendix V, Theorem L1. \(V=\mathbb F_2^3\), \(Q(x,y,z)=x+y\), \(B=\{000,110\}\), and \(E=\mathbb F_2^3\). The one extra row \(z\) is the comparison map in the same paragraph, not a second carrier.
2. Packet B. Chapter 23 and Appendix U at \(L=3\) only. Full commutation syndrome \(Q(x\mid z)=(Ax,A_v z)\), \(B=S\), admitted sets \(\mathcal E_1\) and \(\mathcal E_2\), plus the \(X\)-block detector set that omits faces \(f_{0,2}\) and \(f_{2,0}\).

The quotient count 4, the \(L=4\) rank-29 suite, adaptive costs, the section 23.9 calibration statistics, and `surface_grid_2x2_torus` are outside this scope. No Python, Rust, or Lean kernel was run for this note.

## Hypotheses

H1. Section 21.16 asks whether \(Q\) distinguishes the admitted set up to stabilizer-trivial changes, meaning \((\mathcal E-\mathcal E)\cap\ker Q\subseteq B\), while preserving the logical codespace written there as \(H^1=\ker Q/B\). The section states that question and names no triple \((E,Q,B)\). The goal note says this is not a register obligation. The arithmetic below does not close the question.

H2. Theorem L1 assumes a nonempty finite admitted set \(E\subseteq V=\mathbb F_2^n\), a repair subspace \(B\le V\), and a linear syndrome \(Q\) with \(B\subseteq\ker Q\). For a full Hamming ball the same paragraph makes the fiber criterion equivalent to \(2t<d\), where \(d=\min\{\mathrm{wt}(v):v\in\ker Q\setminus B\}\). On packet A the admitted set is the whole carrier, which is a subspace, so \(E-E=E\). The distance shortcut is not required for that enumeration.

H3. Packet B uses the Appendix U incidences at \(L=3\): face \(f_{i,j}\) meets \(h_{i,j}\), \(h_{i+1,j}\), \(v_{i,j}\), and \(v_{i,j+1}\); star \(s_{i,j}\) meets \(h_{i,j}\), \(h_{i,j-1}\), \(v_{i,j}\), and \(v_{i-1,j}\); indices modulo 3. The Pauli space is \(\mathbb F_2^{18}\oplus\mathbb F_2^{18}\). Weight is \(|\mathrm{supp}\,e_X|+|\mathrm{supp}\,e_Z|\), so one \(Y\) has weight 2. \(Q(x\mid z)=(Ax,A_v z)\) and \(B=S\). Chapter 23 states \(S\subseteq\ker Q\) from \(AA_v^{\mathsf T}=0\). This note uses those incidences. It does not recompute a rank.

H4. Chapter 4 defines a different \(H^1\) as \(\ker\kappa^1\) on a cochain window, after \(d_1d_0=0\) is certified. That quotient is not identified with either packet. Chapter 23 assumes \(L\ge 3\), so a \(2\times 2\) torus is not an instance of packet B.

## Derivation

The two packets stay separate. Neither boolean answers the unbound section 21.16 bullet.

### 1. Packet A: the whole three-bit carrier

\(Q(x,y,z)=x+y=0\) forces \(x=y\), with \(z\) free. Thus

\[
\ker Q=\{000,001,110,111\},\qquad B=\{000,110\}.
\]

The vectors \(001\) and \(111\) lie in the kernel and outside \(B\). In particular \(Q(000)=Q(001)=0\) and \(000+001=001\notin B\). Since \(E-E=E\), the inclusion \((E-E)\cap\ker Q\subseteq B\) fails. The quotient \(\ker Q/B\) has the two classes \(\{000,110\}\) and \(\{001,111\}\), and the second class is an admitted difference. This \(Q\) does not distinguish \(E\) up to \(B\).

The extra row \(z\) is a different map \(Q'=(x+y,z)\). Its kernel is \(\{000,110\}=B\), so \((E-E)\cap\ker Q'\subseteq B\) holds and \(\ker Q'/B\) is trivial. The stated repair \((0,x+y,z)\) sends \(e=(x,y,z)\) to \((x,x,0)\), which is \(000\) or \(110\). Zero extra rows fail on the pair \(000,001\), and one row succeeds, so the exact minimum on this example is one. That integer is a row budget for this example. It does not preserve the two-class quotient of the original \(Q\): the row that separates every vector extinguishes it. L2 states that the dimension formula \(\dim(\ker(Q|E)/B)\) is not asserted for an arbitrary restricted \(E\).

### 2. Packet B: one logical and the balls \(\mathcal E_1\), \(\mathcal E_2\)

Let \(Lx\) be the \(X\)-support \(\{h_{0,0},h_{1,0},h_{2,0}\}\) with \(Z\) block zero. Its weight is 3. Face \(f_{i,0}\) contains \(h_{i,0}\) and \(h_{i+1,0}\), hence exactly two of those three edges, and every face with second index not \(0\) contains none. So \(A\,Lx=0\) and \(Q(Lx)=0\).

Each star meets one lattice row in two horizontal edges and every other row in none, so every star vector has row-flux \(0\). Each row of \(Lx\) contains exactly one edge, so each row-flux of \(Lx\) is \(1\). Hence \(Lx\) lies outside the star span. It lies in \(\ker Q\) and outside \(S\).

For \(\mathcal E_2\), let \(e_1\) be \(X\) on \(h_{0,0}\) and let \(e_2\) be \(X\) on \(h_{1,0}\) and \(h_{2,0}\). The weights are \(1\) and \(2\). The edge \(h_{0,0}\) lies in \(f_{0,0}\) and \(f_{2,0}\). The edges of \(e_2\) lie in \(f_{1,0}+f_{0,0}\) and \(f_{2,0}+f_{1,0}\), which sum to the same two faces. Both \(Z\) blocks are zero, so the full syndromes agree. The difference is \(Lx\notin S\). The inclusion fails on \(\mathcal E_2\). This \(Q\) does not preserve the class of \(Lx\) inside that ball. One colliding pair is enough for failure; the ball was not enumerated.

For \(\mathcal E_1\), every admitted difference has weight at most \(2\). A single \(X\) meets two faces, and a single \(Z\) meets two stars, so neither block of weight \(1\) lies in the corresponding kernel. An \(X\) and a \(Z\) on different edges leave a weight-\(1\) block. An \(X\) and a \(Z\) on the same edge are one \(Y\), and that \(X\) block still meets two faces, so the sum is outside \(\ker Q\). A same-sector weight-\(2\) vector would meet every face, or every star, evenly. Each edge lies in two faces. Adjacent faces share one edge and diagonal faces share none, so no two edges occupy the same pair of faces. The \(L=3\) grid has no \(2\)-cycle. The same count holds for stars. Thus no weight-\(2\) vector lies in \(\ker Q\), \((\mathcal E_1-\mathcal E_1)\cap\ker Q=\{0\}\subseteq S\), and the inclusion holds. Distinguishing \(\mathcal E_1\) up to \(S\) is this membership fact. It is not a quotient dimension. P10C already says a rank defect is not an admitted collision.

The \(X\)-block observer that omits \(f_{0,2}\) and \(f_{2,0}\) fails on \(\mathcal E_1\). The edge \(h_{0,0}\) meets \(f_{0,0}\) and \(f_{2,0}\); the edge \(v_{0,0}\) meets \(f_{0,0}\) and \(f_{0,2}\). Each retained syndrome is the single face \(f_{0,0}\). The two weight-\(1\) errors therefore share the retained syndrome. Their sum is supported on the two omitted faces, so it lies outside \(\ker A\), outside the full \(\ker Q\), and outside \(S\).

### 3. The booleans do not close the bullet

Failure on packet A, failure on packet B for \(\mathcal E_2\), success on packet B for the full syndrome and \(\mathcal E_1\), and failure for that partial detector set: those four booleans stay on their packets. Section 21.16 selects none of them. On packet A, separating every vector replaces the two-class quotient by the trivial quotient. On packet B, the \(\mathcal E_1\) inclusion does not add a row and does not by itself name a dimension of \(\ker Q/S\).

Appendix V states that no Majorana device is claimed to realize these declarations, and that L1 is a finite binary admitted-error theorem, not a proof of the Knill–Laflamme operator theorem. Chapter 23 says the packet says nothing about any physical device. No continuum limit, physical law, or closed theorem outside these packets follows. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Claims this note does not make

- It does not answer section 21.16 yes or no. The bullet names no triple \((E,Q,B)\). The question stays open outside the two packets above, and it is not a register obligation.
- It does not claim that a Majorana device, or any physical readout, realizes these declarations. Appendix V states that nonclaim. Chapter 23 says the chapter says nothing about any physical device. A classical bit table is not physical non-disturbance.
- It does not treat L1 as a proof of the Knill–Laflamme operator theorem.
- It does not preserve the two-class quotient of packet A while distinguishing every vector of \(\mathbb F_2^3\). The one extra row \(z\) makes the new kernel equal to \(B\). That row count is a budget for this example, not a toric purchase.
- It does not claim that the full \(L=3\) syndrome separates \(\mathcal E_2\) up to \(S\). The pair \(e_1=h_{0,0}\), \(e_2=\{h_{1,0},h_{2,0}\}\) collides, and the difference \(Lx\) lies outside \(S\).
- It does not identify the \(\mathcal E_1\) membership fact with a quotient dimension. The displayed count \(\dim(\ker Q/S)=4\), the identity \((2L^2+2)-(2L^2-2)=4\), and P01C are outside this scope. P10C says a global rank defect is not an admitted collision.
- It does not recompute the \(L=4\) syndrome of shape \((32,64)\), the rank-\(29\) suite, the adaptive costs \(6\) and \(4\), or the section 23.9 calibration comparison. Those statistics were not read as a measured table and were not rerun.
- It does not adopt the coarser question \(B=S+\langle u+v\rangle\), the inference \(t\le L-1\), or a cone-radius comparison as a result of this note.
- It does not identify either packet with Chapter 4's \(H^1=\ker\kappa^1\). That equality is the usual \(Z^1/B^1\) only on a window where \(d_1d_0=0\) is certified. No such identification is declared here.
- It does not settle `surface_grid_2x2_torus`. Chapter 23 assumes \(L\ge 3\). The separate Majorana monograph's \(2\times 2\) edge complex is a different carrier. Its rank lines are not this calculation, and they are not a CSS quotient of dimension \(4\).
- It does not run the Python reconstruction, the unit tests, the Lean encoding, or a Rust port. The booleans above are incidence checks on the two packets.
- It does not establish a continuum limit, a physical law, or a closed theorem outside these two packets.
