# CC-26 through CC-30: code and mathematical review

AuthorityEffect: None. Original user attachment and original executable copy are byte-preserved. This is an exact bounded replay plus separate general written proof notes. No general Lean certificate, full-program closure or physical-input discharge is claimed. CC labels are separate from BR, RS, GF, HL and AS.

## Verdict

The original code's 66 printed checks pass in both normal and optimized Python on Python 3.14.2 / SymPy 1.14.0. The numerical rational values shown for the kernel obstruction, probe inversion, rational Kraus witnesses, Choi products and unitary completions are correct on these fixtures. No evidence of invented values was found in those outputs. General statements require proofs, which are supplied separately in proof_notes.md with their imports and domains explicit. Passing finitely many dimensions/inputs is not such a proof.

The original header overstates the arithmetic restriction, and its success signal is not fail-closed. Preserve the original evidence rather than replacing it with a passing retry. Original and corrected receipts, the intermediate passing version, and the static diagnostic are retained under verification/.

## Arithmetic and success-reporting repairs

1. four_squares used n**0.5, introducing an inexact exponent/bound. The final replay uses math.isqrt on a checked nonnegative exact integer. Lagrange's theorem is a named existence import; exhaustive search has no claimed practical bound for large inputs. The large-integer fixture checks isqrt alone, not a giant four-square search.
2. lift_kraus used sqrt(S[k,j]); on the supplied matrix it creates exact algebraic irrational entries. This is symbolic exactness, but not membership in Q(i). The final admitted Kraus replay uses the separate four-square construction only. The two original tests of the square-root family are superseded by the rational-family equality/normalization tests; their original outputs remain retained.
3. check printed FAIL but did not set a failing process exit. The corrected version records every condition, treats unknown/symbolic truth as failure, and exits nonzero if any check fails. A separate probe uses the actual check function and actual final exit guard to verify false and unknown conditions exit 1, under both normal Python and -O.
4. Recursive completion used assert for structural guards; those disappear under -O. The final replay uses persistent checks and input admission for unit vectors, isometries, dimensions and Gaussian-rational coefficients. It covers e1, square, scalar phase and empty-column recursion branches as well as invalid inputs.
5. Remove stale exploratory comments suggesting rational Kraus presentation is still unresolved. The submitted four-square construction already solves it. The classical-lift Choi comment is corrected to INPUT-FIRST order: sum S[k,j] E_jj tensor E_kk. The original block-building code used that order correctly; the mismatched prose was not a changed mathematical convention.

## Choi admission needs Hermiticity explicitly

SymPy's general positive-semidefinite predicate can accept non-Hermitian matrices under its real-part convention. For example N=[[1,1],[-1,1]] has symmetric/Hermitian part I and is_positive_semidefinite=True, but N is NOT a quantum Choi matrix. The submitted CP example is a Kraus Gram matrix and is Hermitian, so its observed result is valid. Do not promote that predicate alone into a generic CP admission test.

The final replay includes an exact Gaussian-rational helper that first checks square shape, coefficient membership and Hermiticity, then checks ALL principal minors, including singular/zero cases. Principal-minor nonnegativity is a finite exact criterion for Hermitian PSD. It can be exponentially expensive; no complexity improvement is claimed. The general CPTP statement also assumes Phi is K-linear: evaluating an arbitrary nonlinear callable on matrix units does not certify that assumption.

## CC-26 scope

The d^2 states, traces and the two inversion formulas are correct. The finite invertibility argument establishes spanning in ALL positive dimensions; the script alone only samples dimensions. The final replay adds d=1 and all j<k inversions for d<=4. The extra physical assumption that these states can be prepared and deterministic outputs are normalized remains declared. CP alone still does not imply TP; the diag(1,1/2) example correctly loses trace on E11 (zero-based second coordinate).

## CC-27 scope

The exact obstruction is Delta_g Phi (Id-Delta_e) Psi Delta_d. Its zero condition is necessary and sufficient for THIS pair's kernel multiplication; no-creation by Psi and no-detection by Phi are sufficient. The dual diagonal-effect condition is valid with the stated Hilbert-Schmidt adjoint. The 3D disjoint-coherence example genuinely has kernel multiplication while neither sufficient factor condition holds; dephasing covariance is not necessary.

The submission uses U followed by U, which is a valid failure, but the earlier request specifically asked for U and its inverse. The final replay adds that case. The coefficient matrix [-288,288;288,-288]/625 and its Omega(E00) value are correct for U followed by U. They are not relabeled as the inverse case.

## CC-28 identities, dimensions and zero maps

Both rectangular stochastic examples admit the rational four-square Kraus construction. At s=p/q, write pq=sum a_m^2 and use a_m/q times the rectangular matrix unit. This is not a claim that sqrt(s) is rational or in Q(i). The finite bound is at most four Kraus terms per nonzero stochastic entry.

The lift preserves composition, but E(I_d)=Delta_d. This is the identity on the diagonal algebra, not the ambient identity channel for d>1. Use classical diagonal algebras, or objects (M_d,Delta_d) with morphisms fixed by both dephasings, when claiming a unital categorical embedding. The full CPTP category retains its ordinary identity channel. Zero CP maps can be represented by an empty Kraus family only with explicit input/output dimensions; they are not normalized channels on positive-dimensional spaces.

## CC-29 quotient and convention challenges

The identity presentations with different cardinalities and the rotated dephasing family have the claimed equal Choi matrices. K2 in the source is literally K1; the genuinely different family is K3, which is the one tested. Choi equality identifies maps and is stronger than label-permutation equivalence. CPTP hom-sets are not K-vector spaces.

The submitted input-first link product and tensor-leg permutation are correct on the original fixtures. However they use equal dimensions and mostly real symmetric data. The final replay adds a genuinely complex 2->3->2 composition, an independently coded four-index contraction, dual composition and Hilbert-Schmidt pairing, plus a complex rectangular tensor-leg example. It also verifies that omitting the partial transpose or tensor permutation is detected. These challenges improve convention sensitivity; they do not constitute a proof for arbitrary dimensions.

## CC-30 completion

The Householder-like rational formula is correct over Q(i) for an admitted unit vector. The denominator uses 1-conjugate(v1), matching w*e1, and need not be real. The proof in proof_notes.md shows why it is nonzero and why unitarity follows. The recursive block completion is correct. No Witt theorem or new norm-equation solver is needed once the isometry is supplied. Native implementation changes or a general Lean construction have not been made here.

## Retained evidence and validation limits

Original runs reported 66 PASS lines and no FAIL lines. A first corrected version passed 132 checks; its exact source and outputs are retained. A subsequent PSD-test addition contained a parenthesis typo caught by static parsing before execution; the draft and diagnostic are retained separately from final passing evidence. The final attempt's receipts give its actual check/refusal counts and bind its source hash. Expected failure-exit probes are labeled as guard tests, not failed mathematical runs.

The bundle directory was renamed from a provisional 030000 label to the observed 025658 UTC start. Original command receipts retain the path that was actually executed; source bytes are bound by the preserved snapshots and manifest. Nothing in those historical receipts is silently rewritten. Earlier sealed evidence is verified separately before this bundle is sealed.

General written proofs and bounded replay are distinct evidence grades. Four-square existence and the previously reviewed finite Choi theorem remain explicit imports. All original framework-to-Hilbert/Born/physical-channel assumptions remain open or declared as previously recorded. No publication or whole-program closure is implied.
