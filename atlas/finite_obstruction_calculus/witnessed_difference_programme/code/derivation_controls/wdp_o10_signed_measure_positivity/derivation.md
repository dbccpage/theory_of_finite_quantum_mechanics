# WDP-O10-SIGNED-MEASURE-POSITIVITY

Goal id: WDP-O10-SIGNED-MEASURE-POSITIVITY

Selected scope for WDP-O10-SIGNED-MEASURE-POSITIVITY is recorded in this note.

The plan statement is that positivity of a finite signed-history measure is a separate open obligation, and that the finite signed SQL histories are not declared probability measures. The plan entry has an empty `depends_on` list and no fence. This note reads one labelled breakup of the opened SQL constructor on L=4, M=1 and records two negative atoms. It does not execute the database, the M=2 census, or a transfer trace. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Selected scope

L=4, M=1 checkerboard SQL histories (four plaquettes, full Fock, LM=4). One labelled breakup: all four plaquettes horizontal, giving two time-slice 4-cycles. The two opposite staggered masks have signed charges -1 at q=3 and -1/21743271936 at q=193/192. Hypotheses: vertical weight 1, horizontal weight (q-1)/2>0, occupation bit (1-(site mod 2)+mask) mod 2, and sign from the wrap Jordan-Wigner parity. Not the Gibbs covariance, not the zero-meron reduction, not L=2, not the M=2 partition 912, and not a continuum limit.

## Hypotheses

H1. The opened constructor in `meron_exact_model.py` builds the periodic checkerboard for even sites in {4,6} and LM<=12. Here sites=4 and repetitions=M=1, so times=2 and plaquettes=LM=4. A plaquette at time t on the bond (x, x+1 mod L), with x starting at t mod 2, has corners (t,x), (t,x+1), (t+1,x), (t+1,x+1), time taken modulo 2. Breakup bit 0 inserts the two time-like edges and multiplies the graph weight by 1. Breakup bit 1 inserts the two same-time edges and multiplies by the stored horizontal weight (q-1)/2. The all-horizontal graph is the bitmask with every plaquette bit set.

H2. For q>1 the horizontal weight is positive, so every graph weight on this constructor is positive. The two values used here are q=3 and q=193/192. The second has M(q-1)=1/192, the closed endpoint of the O.10 interval 0<=r<=1/192. The finite-check note calls that value its in-disk fixture. This note does not evaluate M log q.

H3. An orientation mask assigns to each site the occupation bit (1-(site mod 2)+mask_bit of its component) mod 2. The configuration sign is -1 exactly when the sum, over plaquettes whose first endpoint changes occupation at the next time, of the Jordan-Wigner popcount strictly between the endpoints in the before-layer occupation, is odd. Adjacent bonds have an empty open interval. These are the constructor statements, not the Gibbs trace.

H4. The unreduced signed-history charging of a configuration is its sign times its graph weight. On a finite set, a positive measure assigns a nonnegative number to each atom. A probability measure is a positive measure whose atoms sum to 1.

## Derivation

### 1. The all-horizontal breakup

At L=4 the even layer has bonds (0,1) and (2,3). The odd layer has bonds (1,2) and (3,0). Horizontal breakup on all four plaquettes inserts only same-time edges. The time-0 edges are (0,0)—(0,1)—(0,2)—(0,3)—(0,0). The same cycle sits on time 1. There is no time-like edge. The components are those two 4-cycles. The smaller node ids lie on time 0, so the constructor's root order labels time 0 as cluster 0 and time 1 as cluster 1. The graph has four orientations.

### 2. Occupations and the wrap sign

Mask bit 0 on a cycle gives occupation (1,0,1,0). Mask bit 1 gives (0,1,0,1). Equal cycle masks put the same occupation on both times, so no endpoint changes and every popcount contribution is 0. The sign is +1. Opposite cycle masks change every site. The three adjacent plaquettes have empty open intervals and contribute 0. The wrap plaquette is (3,0) on the odd layer, so its before-layer is time 1 and its open interval is the site set {1,2}. Both staggered patterns have n_1+n_2=1, so that popcount is 1. The sum is odd. The sign is -1 for either choice of which cycle carries mask bit 1. Those two rows are the global masks 1 and 2.

### 3. The signed charges

The graph weight is ((q-1)/2)^4. At q=3, (q-1)/2=1, so the weight is 1 and each opposite-mask configuration has signed charge -1. At q=193/192, (q-1)/2=1/384. Since 384=2^7*3,

384^4=2^{28}*3^4=21743271936,

and each opposite-mask configuration has signed charge -1/21743271936. Both numbers are negative. By H4 the unreduced charging is not a positive measure, and therefore not a probability measure, on this finite SQL configuration set.

### 4. Orbit cancellation does not delete the atoms

The two equal-mask charges on this graph are the opposite positive number, +1 at q=3 and +1/21743271936 at q=193/192. The four-orientation sum is 0. Reading the cluster-sign view off these rows: the sign at mask 1<<cluster is the opposite-mask sign -1 for both clusters, so the meron count is 2 and the reduced weight is 0. Cancellation drops the orbit from the signed partition and from the zero-meron reduction. It does not delete the negative atoms from the unreduced configuration charging. The zero-meron clause keeps a positive contribution only when the meron count is 0, in which case the kept orientations have sign +1. This graph is not that case.

### 5. What the neighbouring sections do not supply

O.10 bounds cumulants of the signed normalized source sum, uniformly in the time count, and says that this does not prove positivity of a finite signed-history measure. The time-labelled note calls that normalized sum not an asserted probability expectation. O.11 and EP-4 through EP-6 show that each Fourier matrix of the exact finite-volume Gibbs Euclidean covariance is a sum of nonnegative multiples of real outer products, hence positive semidefinite. The covariance note's opening sentence says this is the Hamiltonian Gibbs trace, not a probability interpretation of the signed SQL histories. EP-6 says that the positive-semidefinite conclusion says nothing about positivity of the finite signed transfer-history weights. O.12 takes the row-sum limit of that same Gibbs kernel and still does not declare the finite signed SQL histories probability measures. The negative atoms above are the obstruction those sections leave, on this one SQL carrier, at the algebraic point q=3 and at the in-disk point q=193/192.

## Claims this note does not make

- It does not claim that the unreduced signed SQL charging is a positive measure, a probability measure, or a probability characteristic function. The two opposite-mask atoms are negative.
- It does not claim that orbit cancellation, or the zero-meron reduction, removes those atoms. The reduction keeps a positive contribution when the meron count is 0 and the sign is +1. This graph has meron count 2.
- It does not treat EP-4 through EP-6, the O.12 nonnegative modes, or the O.10 cumulant bound as positivity of the finite signed transfer-history weights. It does not reuse k_0=1/4 or a mode lower bound as this charging.
- It does not identify either atom with the recorded full unscaled partitions 80 or 113837185/7077888. Those are closed sums over the fixture, not the charge of this breakup.
- It does not use the L=2 carrier. The constructor rejects sites below 4. On sites {0,1} the open interval in the hop sign is empty, so every such hop sign is +1. That row is not this atom.
- It does not reuse the unread-executed M=2, q=3 test census (192 negative configurations, average sign 19/27, signed partition 912). That census is a different time count. It is not summed into these charges.
- It does not claim a non-equal-time kernel, a joint spacetime limit, a spacetime field topology, an X_LM comparison, a continuum limit, a physical law, or any carrier other than L=4, M=1 at q=3 and q=193/192.
