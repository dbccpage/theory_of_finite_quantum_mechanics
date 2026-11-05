# WDP-CH17-SEMIRING-CLASSIFICATION

Goal id: WDP-CH17-SEMIRING-CLASSIFICATION

Selected scope for WDP-CH17-SEMIRING-CLASSIFICATION is recorded in this note.

## Selected scope

Carriers {0,1} and {0,1,2} with row-source matrices over (Z,+,·). Nonempty vertex-block partitions. P0: rows agree inside each source block. P1: endpoint-block path sums are representative-independent at every finite length, equivalently MH=HB. P2: the one-block case of P1, each source summed onto the whole carrier. Census: all 81 matrices with entries in {-1,0,1} on two vertices. Excludes arbitrary history maps, admissibility not compiled into M, infinite sums, and any semiring other than this integer arithmetic.

## Hypotheses

H1. (Z,+,·) is a semiring. Addition is a commutative monoid with identity 0, multiplication is a monoid with identity 1, and multiplication distributes over addition. It is not zerosumfree: 1+(-1)=0.

H2. M is square and row-source, so (M^{n+1})_{a,b} = Σ_c (M^n)_{a,c} M_{c,b}. On the full path family, WDP-CH17-P01 identifies (M^n)_{a,b} with the length-n path aggregate. An admissibility predicate is not that entry unless it has been compiled into M.

H3. For a nonempty partition, H_{x,j}=1 if x lies in block j and H_{x,j}=0 otherwise. The length-n endpoint-block aggregate from x into block j is (M^n H)_{x,j}.

H4. `SemiringCoarseGraining.lean` assumes an associative multiplication and two-sided units. It does not construct a partition, a membership matrix, or the distributivity law for matrix multiplication. `claim_map.md` records that the matrix partition construction remains prose and native. The ledger marks L:partial(SemiringCoarseGraining).

## Derivation

Appendix I.3, restricted to these integer matrices, gives the length criterion. Necessity is length one: the row of MH indexed by x is the tuple of sums of weights from x into the blocks, so MH=HB says those sums depend only on the source block and equal the rows of B. Sufficiency is induction on the semiring laws. M^0 H = H = H B^0. If M^n H = H B^n, then

M^{n+1} H = M (M^n H) = M (H B^n) = (MH) B^n = (HB) B^n = H B^{n+1}.

The regrouping uses associativity of matrix multiplication, which holds because (Z,+,·) distributes. Positivity, subtraction, division, and zerosumfreeness are not used. Length 0 does not constrain B: the empty-path column is the corresponding row of H.

Each block is nonempty, so some row of H is the standard basis row of that block. The matching row of MH is then that row of B. Thus the constants determine B. If MH=HB=HB', those rows agree, so B is unique. The adapter copies the block sums of the first vertex in each block and returns no quotient when another vertex in the block disagrees.

P0 implies P1 for the same partition, because equal rows have equal block sums. The converse is false on (1) and (3). P1 for one partition does not imply P2. P2 does not imply P1 for another partition. Both failures are the opened examples below.

(1) M=((2,-1,3),(0,1,3),(4,-2,1)), blocks ((0,1),(2,)). Source 0 sums to (2+(-1),3)=(1,3). Source 1 sums to (0+1,3)=(1,3). Source 2 sums to (4+(-2),1)=(2,1). Thus B=((1,3),(2,1)) and P1 holds at every finite length by the induction. P0 fails because (2,-1,3)≠(0,1,3). The Rust test source asserts direct and transported membership agree at each length in 0..=12 before the next multiply. The four entries of B are not a one-block total: the full row sums are 4, 4, and 3, so P2 fails. The same witness separates the dual. With P the transpose of H, PM=((2,0,6),(4,-2,1)). Any BP has equal first and second columns, and those columns of PM are (2,4) and (0,-2), so no integer matrix satisfies PM=BP.

(2) M=((2,0,0),(0,0,2),(0,0,2)), blocks ((0,1),(2,)). Source 0 has block sums (2,0) and source 1 has (0,2), so P1 fails. Every full row sum is 2, so M sends the all-ones column to twice itself and P2 holds: the per-source aggregate onto the single block is 2^n, including 2^0=1. The Python test source checks that column for n=0..6. That column is not the sum of all matrix entries, 3·2^n, and it is not a two-block quotient.

(3) M=((1,-1),(0,0)). One-block sums are 1+(-1)=0 and 0+0=0, so B=((0,)) and P1 holds, while the rows differ, so P0 fails. The zero uses additive cancellation. The Python test source records this quotient and the unequal rows.

(4) M=((1,-1,0),(0,1,-1),(0,0,0)), blocks ((0,1),(2,)). Source 0 has block sums (0,0) and source 1 has (1,-1), so P1 fails. All three full row sums are 0, so the one-block quotient is ((0,)). Length 0 has empty-path weight 1. For every n≥1, M^n sends the all-ones column to 0, so the per-source aggregate is 0. The Rust test source asserts the two-block refusal, this one-block quotient, intertwining at each length in 0..=8, and M_{0,0}=1≠0=M_{1,0}. Individual edge weights are not preserved.

(5) Two vertices have exactly two partitions, ((0,1),) and ((0,),(1,)). The test source requires exactly two results on every 2×2 matrix. The discrete partition has H=I and B=M, so P1 holds for all 81 matrices with entries in {-1,0,1}. The one-block partition holds exactly when the two row sums agree. On {-1,0,1}^2 the row-sum multiplicities are 1, 2, 3, 2, 1 for sums -2, -1, 0, 1, 2, because the pairs are (-1,-1); (-1,0) and (0,-1); (-1,1), (0,0), and (1,-1); (0,1) and (1,0); and (1,1). Hence exactly 1^2+2^2+3^2+2^2+1^2=19 matrices satisfy P2, and 81-19=62 do not. Therefore 81+19=100 of the 162 matrix-partition pairs satisfy P1. This count is that entry box only. The test source checks the same 81 matrices and the same split. It was not re-executed for this note.

The abstract power step is the Lean lemma, not this census. If multiplication is associative and unital and a h = h b, then a^n h = h b^n for every n, and the length-one identity is necessary. Matrix multiplication is a monoid only after distributivity. That file assumes the monoid laws and does not prove them. The generic Rust `Semiring` bound is an implementer obligation. The admitted checks above are integer arithmetic stored as exact rationals.

## Obstruction

Chapter 17 states that a comprehensive classification of coarse-grainings which preserve arbitrary path aggregates over general semirings remains a broader research problem, and that CH17-O01 selects only the rational endpoint-block aggregate. The goal record states the same boundary, with empty `depends_on` and no fence. CH17-P03 reindexes one finite commutative sum. The surrounding prose says that this pushforward may fail to preserve composition, and the proposition does not prove Markovianity, decoherence, or consistent histories. Zerosumfreeness blocks a nontrivial sum to zero, but the manuscript says it does not force equal sums to be termwise without further cancellative or idempotence hypotheses. The five separations above do not classify history congruences, admissibility predicates left uncompiled, or any semiring other than (Z,+,·).

## Claims this note does not make

- It does not classify coarse-grainings that preserve arbitrary path aggregates over a general semiring. That goal stays open. CH17-O01 remains the manuscript's rational endpoint-block case. This note does not extend it.
- It does not read the Rust `Semiring` bound, or `powers_intertwine`, as that missing classification. The Lean lemma is not a constructed partition classifier.
- It does not transport the Boolean, natural-number, tropical, nonnegative-real, or complex readings in section 17.3 from this integer census.
- It does not treat a finite path sum as a continuum path integral, a path measure, or the Feynman rule (CH17-N01). It does not select a physical law, Born readout, interference, decoherence, or Markovianity.
- It does not treat zerosumfreeness (CH17-P02) as termwise rigidity of equal sums, or as quantum theory. Examples (3) and (4) use cancellation.
- It does not treat equal unrestricted row totals as endpoint-block preservation. Example (2) has equal totals and fails blocks ((0,1),(2,)).
- It does not treat endpoint-block preservation as preservation of individual histories or of individual edge weights. Examples (1), (3), and (4) separate those predicates.
- It does not identify the dual relation PM=BP with MH=HB. Example (1) satisfies MH=HB and satisfies PM=BP for no integer B.
- It does not treat CH17-P03 as a compositional path congruence.
- It does not treat `classify(()) == (((), ()),)` as part of CH17-O01. That proposition requires a nonempty block partition, and so does the selected scope.
- It does not infer a Kleene star, an infinite series, or analytic convergence from a finite-length aggregate. CH17-P01 states that boundary.
- It does not take the count 100 of 162 outside entries in {-1,0,1} on two vertices. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.
