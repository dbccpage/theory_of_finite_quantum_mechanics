# WDP-APPW-ALL-M-INERTIA

Goal id: WDP-APPW-ALL-M-INERTIA

Selected scope for WDP-APPW-ALL-M-INERTIA is recorded in this note.

The goal statement in the plan is that a general all-M inertia formula is a separate obligation, and that the four finite inertias are observations, not an all-M formula. This note records the finite observations. It does not supply the missing formula. No fresh Python replay, Lean kernel run, or congruence was executed for this note.

## Selected scope

Finite carrier only: L=4 periodic CAR, Fock dimension 16, θ=1/10, step r=θ/M, and M∈{1,2,3,4}. G is the symmetric connected response of size LN=8M from Appendix W §1. On this set the recorded Sylvester inertia (n+, n−, n0) equals (4M, 1, 4M−1), i.e. (4,1,3), (8,1,7), (12,1,11), (16,1,15). Not for M≥5, other θ, or other L.

Each recorded triple sums to the matrix order 8M: 4+1+3=8, 8+1+7=16, 12+1+11=24, 16+1+15=32.

## Hypotheses

H1. The carrier is the one fixed in Appendix W §1 and in `docs/meron_field_limit_derivations/trotter_cochain_extinction_derivation.md` §1. There are L=4 sites and the full 16-dimensional Fock space. In the ascending occupation basis, c_x removes site x with sign (−1) raised to the number of occupied sites before x. The operators are n_x=c_x* c_x, a_x=(−1)^x (n_x−½I), and the periodic bond projections P_x. Even bonds commute with each other, and odd bonds commute with each other.

H2. For 0<θ≤1 and an integer M≥1, the step is r=θ/M and N=2M. The layers are T0=(I+r P0)(I+r P2) and T1=(I+r P1)(I+r P3), with K_j=T_(j mod 2). The partition is Z_M(z)=(1+r)^(−M) times the ordered trace of the K_j against the insertions exp(∑_x z_{j,x} a_x/2). The response is the real symmetric matrix G_M=4 D_z^2 log Z_M(0). The scalar (1+r)^(−M) cancels from G. The order is LN=8M. The normalized quadratic is q_M(ψ)=ψ^T G_M ψ/(L N^2).

H3. Inertia here means the Sylvester sign count (n+, n−, n0) of that one matrix: the numbers of positive, negative, and zero eigenvalues, counted with multiplicity, or equivalently the sign counts on a congruence diagonal. It is not the sign of one Rayleigh quotient.

H4. The numerical scope of the sign count is the single temperature θ=1/10 and the four depths M=1,2,3,4, so the steps are r=1/10, 1/20, 1/30, and 1/40. The staggered direction is v_(j,x)=(−1)^j. Outside this set, H1–H3 do not by themselves name (n+, n−, n0).

## Derivation

### 1. Recorded table at θ=1/10

Appendix W §2, and the same table in the live Trotter derivation §2, record congruence inertias (positive, negative, zero) and one staggered eigenvalue on each of four matrices.

| M | dim 8M | step r | normalized partition | staggered eigenvalue | inertia |
|---|--------|--------|----------------------|----------------------|---------|
| 1 | 8 | 1/10 | 17661/1100 | −1/706440 | (4,1,3) |
| 2 | 16 | 1/20 | 755374987/47040000 | −35281/90644998440 | (8,1,7) |
| 3 | 24 | 1/30 | 1395062306051761/86870556000000 | −12188547841/55802492242070440 | (12,1,11) |
| 4 | 32 | 1/40 | 2379246859363301568641/148151258316800000000 | −14588472130734881/95169874374532062745640 | (16,1,15) |

For M=1 the same section gives the full spectrum 10/21, 21/40, 420/841 with multiplicity 2, 0 with multiplicity 3, and −1/706440. The text says the table verifies four finite matrices and is not an all-M inertia theorem, and that the time-limit argument does not depend on extrapolating the table.

`code/locality_smearing/examples.json` stores the same four partitions, the same four staggered eigenvalues, and the inertias [4,1,3], [8,1,7], [12,1,11], and [16,1,15]. `code/locality_smearing/replay.py` rebuilds M=1,2,3,4 from `car.response` and compares each stored inertia with the sign count of that row's congruence diagonal and with [4M, 1, 4M−1]. The comparison sits inside that four-row loop. The checker requires the retained rows to be exactly M=1,2,3,4. It does not range over M≥5.

`car.response` builds G on the 16-dimensional operators, with r=θ/M, N=2M, and the staggered Rayleigh (v^T G v)/(4N). Since L=4, the denominator 4N is LN. The function returns that Rayleigh as `eigenvalue`. This note did not recompute the matrices.

### 2. What the M=1 integer witness decides

`CARResponseWitness.lean` takes one submitted 8×8 integer matrix, `scaledMatrix`, and the denominator 2825760. Its header says Python binds that table to the sixteen-state CAR construction, and that Lean verifies the submitted witnesses, not the Python construction and not an infinite-M spectral extrapolation.

The file decides, by `decide` on those submitted integers:

- the eight listed vectors are eigenvectors, with scaled eigenvalues 1483524, 1345600, 1411200, 1411200, −4, 0, 0, 0;
- those vectors are pairwise orthogonal, each of squared length 8;
- the vector (1,1,1,1,−1,−1,−1,−1) has scaled quadratic form −32;
- the denominator equals 4·706440;
- the sign counts of the scaled eigenvalue list are 4, 1, and 3.

Dividing those scaled eigenvalues by 2825760 recovers the monograph spectrum, as integer arithmetic on the recorded values:

- 4·706440=2825760, so −4/2825760=−1/706440;
- 2825760/40=70644 and 21·70644=1483524, so 1483524/2825760=21/40;
- 2825760/21=134560 and 10·134560=1345600, so 1345600/2825760=10/21;
- 2825760/841=3360 and 420·3360=1411200, so 1411200/2825760=420/841, twice.

The unscaled quadratic form on a staggered vector of squared length 8 is 8·(−1/706440)=−1/88305. The same identity is 2825760·(−1/88305)=−32, because 32·88305=2825760. Appendix W.8 records the opposite global sign (−1,−1,−1,−1,+1,+1,+1,+1), the eigenvalue −1/706440, and v^T G v=−1/88305, with `is_positive_semidefinite` false. `distinct_replay.check_inertia_promotion` reads that Gate E receipt and raises `finite_m_promoted_to_all_m` if a claim sets `all_m_from_this_point`. The point r=1/10 lies outside the declared region r≤1/192. W.8 says one finite point does not establish an unrestricted finite-M claim or an asymptotic formula.

`replay.py` also checks that this scaled integer matrix equals the M=1 rational matrix from `car.response` multiplied by 2825760. That comparison is a Python binding. It is not a Lean proof of the Python program, and it covers M=1 only.

### 3. Characteristic-polynomial calculator and declared fraction checks

`code/trotter_characteristic_polynomials.py` builds operators on the same 16-dimensional Fock space and a matrix G of order 8M. Its second argument is divided by M before it enters T0 and T1. The tests pass 1/10, so the step used in the product is (1/10)/M, which is the Appendix W step at θ=1/10. The module header says the zero-mode count dim ker G = 4M−1 is tested up to M=4, and that physical continuum claims are not asserted from this finite model.

The tests assert, at that input:

- M=1: dimension 8, zero-mode count 3, negative count 1, staggered Rayleigh −1/706440;
- M=2: dimension 16, zero-mode count 7, negative count 1, Rayleigh −35281/90644998440;
- M=3: dimension 24, zero-mode count 11, negative count 1, Rayleigh −12188547841/55802492242070440;
- M=4: dimension 32, zero-mode count 15, negative count 1, Rayleigh −14588472130734881/95169874374532062745640.

On a matrix whose spectrum is fully signed, one negative eigenvalue and 4M−1 zeros leave 8M−(4M−1)−1=4M positive eigenvalues. That arithmetic explains the match with (4M, 1, 4M−1) on these four labelled outputs. It does not create the zero count, or the negative count, at any other M.

`TrotterCharPoly.lean` checks declared rationals through M=3. The header says `evalCleared` identities, the recorded counts `8M` and `4M−1`, the degree tally of the recorded multiplicities, and two cross-multiplications are what is checked, and that the file does not build G and does not derive a characteristic polynomial. In particular `m1_zero_mode_law`, `m2_zero_mode_law`, and `m3_zero_mode_law` are the numeral equalities 3=4·1−1, 7=4·2−1, and 11=4·3−1 on constants defined in that file. They are not a computation of ker G_M.

The one-period scalar in Appendix W §2 is λ_1(r)=−r^4/(4(r+2)(r^2+4r+8)). At r=1/10 the factors are r+2=21/10 and r^2+4r+8=841/100. The Lean identity `m1_closed_form_exact` decides 4·21·841=70644, 10000·70644=1000·706440, and 10·70644=706440, which is the clearing of (1/10000)/(70644/1000)=1/706440. The Python test asserts that `closed_form_lambda_stag_m1(1/10)` equals −1/706440. This fixes one eigenvalue at M=1.

The separate M=2 formula in the Python module, evaluated at the symbol value 1/10, is asserted equal to −35281/90644998440. That is the table's M=2 staggered eigenvalue, which the table attaches to the Trotter step r=θ/M=1/20, not to a second copy of the M=1 step. The Lean theorem `m2_closed_form_numerator` decides the integer identity 10·(8+32·10+32·100)+1=35281. That is the cleared cubic factor of the commented numerator at the symbol value 1/10. It does not build the 16×16 matrix. No closed form for the full spectrum, or for the staggered Rayleigh at M=3 or M=4, is stated in these files.

A negative Rayleigh quotient on one vector gives only n−≥1. It is not reused here as the sign count of the 8M-dimensional matrix.

### 4. What holds for every M, and why it is not the inertia

Appendix W §3 proves a pairing bound and then an all-M bound for one compressed channel. With E=e^(4θ) and v_(j,x)=(−1)^j,

|q_{v,M}| ≤ (E+E^2) D^2 / (16 M^2),

so that channel's contribution tends to 0. The text says this does not use the inertia table, and that it does not prove positivity of the full q_M. It also says that v is the sole negative eigenvector in the four checked instances only, and that outside those instances the identification needs its own proof.

Theorem T1 is an O(1/M) envelope |q_M−Q_θ|≤A_θ/M for samples on this fixed L=4 carrier. The text says the time-limit theorem does not depend on extrapolating the table, and that no spatial quadrature is taken. Theorem T2 is nonnegativity of the continuous covariance Q_θ for the declared real sources. It is not positivity, and not the inertia, of every finite G_M. Theorem T3 turns a supplied margin into eventual strict positivity of q_M. A cochain adapter descends if and only if it kills the declared repair subspace (Theorem T4). Section 20.12 (GEN-WDP-57) says the staggered cochain class is not automatically the physical CAR repair relation, and that neither four spectra nor the fixed spatial carrier's time limit closes all-M inertia or the spatial continuum programme.

Appendix W §7 lists general all-M inertia among the obligations left open, beside uniform infinite-volume estimates and joint spatial reconstruction. W.8 states that the four inertias are four finite observations and that no finite list of inertias is an all-M inertia formula. `docs/four_source_inventory.md` records the same boundary: the finite spectra are tied to θ=1/10 and M=1,2,3,4, and the four inertias are not an all-M formula. The plan entry for this goal has an empty `depends_on` list and names those two monograph anchors. No fence is declared on the entry. The source record therefore admits the obligation and withholds the extrapolation.

An all-M inertia formula would name (n+, n−, n0) of G_M for every integer M≥1. Nothing opened here does that. The matrix order grows with M. The congruence rows and the characteristic-polynomial tests stop at M=4. The Lean integer witness stops at the submitted M=1 matrix. The Lean fraction file stops at declared constants through M=3 and does not build G. The scalar formulas fix one eigenvalue at two depths. The rank-one bound controls one compressed channel for every M and does not count the other eigenvalues. No congruence, kernel basis, or recurrence in the monograph, the Trotter derivation, the two Lean files, `car.py`, `replay.py`, `examples.json`, `trotter_characteristic_polynomials.py`, its tests, or `distinct_replay.py` determines the triple for every integer M≥1. Searching `code/rust` for the CAR response inertia, the denominator 2825760, and the eigenvalue 706440 returned no match. No new inertia triple is claimed.

On the four labelled matrices the recorded integers match (4M, 1, 4M−1). That match is the selected scope. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Claims this note does not make

- It does not claim that (4M, 1, 4M−1) is the inertia of G_M for every integer M≥1, for any θ other than 1/10, or for any L other than 4.
- It does not claim that the staggered vector is the unique negative eigenvector outside M∈{1,2,3,4}. A negative Rayleigh quotient is only n−≥1.
- It does not treat four spectra, the fixed-L time limit T1, the covariance positivity T2, the margin schedule T3, or the rank-one extinction bound as an all-M inertia theorem.
- It does not treat T1–T3 as a spatial continuum, a Gaussian field law, a uniform infinite-volume bound, or a joint spatial reconstruction. It does not treat a cochain adapter, including T4, as the physical CAR repair relation.
- It does not treat `CARResponseWitness.lean` as a verification of the Python construction, or as an infinite-M spectrum. It does not treat the `TrotterCharPoly.lean` constant checks, including 3=4·1−1 and the cleared numerator identity 35281, as a construction of G or as a derived characteristic polynomial.
- It does not identify the symbol `r` in `closed_form_lambda_stag_m2` with the Trotter step θ/M. The code assertion at the symbol value 1/10 matches the table entry whose step is 1/20. The M=1 formula λ_1(r) is the monograph's one-period scalar; at r=1/10 it matches −1/706440. Neither formula is an 8M-dimensional signature.
- It does not claim that a Rust CAR-inertia witness is present under `code/rust`. No such witness was found by the search above.
- It does not rerun replay, the characteristic-polynomial tests, or the Lean `decide` proofs. It does not promote the Gate E point r=1/10, M=1, or the value v^T G v=−1/88305, to an unrestricted finite-M claim or an asymptotic formula.
- It does not claim that an exact rational congruence witness for these four matrices is a continuum limit or an unpinned physical law. The all-M inertia formula remains a separate open obligation.
