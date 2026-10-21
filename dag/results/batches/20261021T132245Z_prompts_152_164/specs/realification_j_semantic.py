"""Semantic near misses for the realification / declared-J certificate (L1-WDP-REALIFICATION-J).

Each mutant is a well-formed record that a reviewer could believe and each breaks one premise.
"""


def _prod(data, atok0):
    return next(r for r in data['records'] if r['kind'] == 'prod' and r['input'][4][0] == atok0 and r['input'][1] == r['input'][2] == r['input'][3] == 1)


def _img(data, rows, cols, toks):
    for r in data['records']:
        if r['kind'] == 'img' and r['input'][1] == rows and r['input'][2] == cols and r['input'][3][:len(toks)] == toks:
            return r
    raise KeyError((rows, cols, toks))


def _diag(*d):
    out = []
    for i in range(len(d)):
        out += [str(d[i]) if i == j else '0' for j in range(len(d))]
    return out


def _jstruct(data, a, b, c, d):
    return next(r for r in data['records'] if r['kind'] == 'jstruct' and r['input'][1:] == [a, b, c, d])


def _prod2(data):
    return next(r for r in data['records'] if r['kind'] == 'prod' and r['input'][1:4] == [2, 2, 2] and r['input'][4][0] == '1:1')


def _block_R(tokens, m, n, transpose=False):
    """Block-ordered R of a Gaussian matrix given as 're:im' tokens, or of its plain (non-conjugating) transpose."""
    from fractions import Fraction as F
    vals = [tuple(F(x) for x in t.split(':')) for t in tokens]
    A = [vals[i * n:(i + 1) * n] for i in range(m)]
    if transpose:
        A = [list(r) for r in zip(*A)]
        m, n = n, m
    R = [[F(0)] * (2 * n) for _ in range(2 * m)]
    for i in range(m):
        for j in range(n):
            P, Q = A[i][j]
            R[i][j], R[i][n + j], R[m + i][j], R[m + i][n + j] = P, -Q, Q, P
    return [str(x) for row in R for x in row]


def semantic_mutants(data, profile):
    def interleaved_ordering_same_J(d):
        r = _prod2(d)
        r['RA_interleaved'] = _block_R(r['input'][4], 2, 2)
        r['interleaved_commutes_block_J'] = True

    def star_without_transpose_sign(d):
        r = _prod2(d)
        r['RAstar'] = _block_R(r['input'][4], 2, 2, transpose=True)

    def positivity_preserved_asserted(d):
        r = next(x for x in d['records'] if x['kind'] == 'psd' and x['input'][2] == ['1:0', '2:0', '2:0', '1:0'])
        r['complex_psd'] = '1'
        r['real_psd'] = '1'

    def trace_is_twice_complex_trace(d):
        r = _prod(d, '1:1')
        r['trace_twice_complex'] = '1'

    def swapped_block_convention(d):
        # R'(A) = [[P, Q], [-Q, P]] = R(conj A): off-diagonal blocks of R(AB) negated (only the 1x1 case: entries 1 and 3)
        r = _prod(d, '1:1')
        r['RAB'] = [r['RAB'][0], str(-int(r['RAB'][1])), str(-int(r['RAB'][2])), r['RAB'][3]]

    def unrestricted_real_matrix_in_image(d):
        r = _img(d, 4, 4, _diag(1, 0, 0, 0))
        r['status'] = 'ok'
        r['commutes'] = '1'
        r['recovered'] = ['1:0', '0:0', '0:0', '0:0']

    def conjugation_counted_as_complex_linear(d):
        r = _img(d, 2, 2, _diag(1, -1))
        r['status'] = 'ok'
        r['commutes'] = '1'
        r['anticommutes'] = '0'
        r['recovered'] = ['1:0']

    def rectangular_ok_declared_noncommuting(d):
        r = _img(d, 2, 4, ['1', '3', '-2', '1'])
        r['status'] = 'noncommuting'
        r['commutes'] = '0'
        r['recovered'] = []

    def any_square_root_of_minus_one_is_J(d):
        r = _jstruct(d, 1, -1, 2, -1)
        r['pm_J'] = True
        r['commutes_J'] = True

    def j_is_the_only_square_root_of_minus_one(d):
        r = next(x for x in d['records'] if x['kind'] == 'jcensus' and x['input'][1] == 5)
        r['total'] = 2

    def symmetric_real_matrix_is_hermitian_image(d):
        r = _img(d, 4, 4, _diag(1, 2, 3, 4))
        r['symmetric'] = '1'
        r['status'] = 'ok'
        r['commutes'] = '1'
        r['recovered'] = ['1:0', '0:0', '0:0', '2:0']

    def odd_dimension_has_a_J(d):
        r = _img(d, 3, 3, ['1'])
        r['status'] = 'ok'
        r['commutes'] = '1'
        r['anticommutes'] = '0'
        r['recovered'] = ['1:0']

    return [
        {'id': 'interleaved_ordering_same_J', 'rationale': 'The interleaved order (re_1, im_1, re_2, ...) is a different convention: R in that order is P (x) I2 + Q (x) J1, does not commute with the block J_2, and equals the block R only for 1 x 1 matrices.', 'mutate': interleaved_ordering_same_J},
        {'id': 'star_without_transpose_sign', 'rationale': 'R(A*) uses the conjugate transpose (P^T, -Q^T); a plain transpose (P^T, Q^T) gives R(A^T), which differs from R(A*) whenever Q != 0.', 'mutate': star_without_transpose_sign},
        {'id': 'positivity_preserved_asserted', 'rationale': 'The Hermitian matrix [[1,2],[2,1]] has determinant -3 and is indefinite; asserting that it or its realification is positive semidefinite contradicts the exact minors / elimination.', 'mutate': positivity_preserved_asserted},
        {'id': 'trace_is_twice_complex_trace', 'rationale': 'For A = 1 + i read Tr R(A) = 2 as twice the complex trace 1 + i; it is twice the REAL part only.', 'mutate': trace_is_twice_complex_trace},
        {'id': 'swapped_block_convention', 'rationale': 'Use [[P,Q],[-Q,P]] (imaginary part first / J replaced by -J): still multiplicative, but it is R of the conjugate and R(AB) differs.', 'mutate': swapped_block_convention},
        {'id': 'unrestricted_real_matrix_in_image', 'rationale': 'diag(1,0,0,0) is a positive trace-one real matrix but does not commute with J_2, hence is no R(A).', 'mutate': unrestricted_real_matrix_in_image},
        {'id': 'conjugation_counted_as_complex_linear', 'rationale': 'diag(1,-1) implements complex conjugation: it anticommutes with J, so it is not R of a complex matrix.', 'mutate': conjugation_counted_as_complex_linear},
        {'id': 'rectangular_ok_declared_noncommuting', 'rationale': 'For a 2 x 4 doubled operator the test is J_1 M = M J_2 between different carriers; the square-only "commutes with J" is the wrong test.', 'mutate': rectangular_ok_declared_noncommuting},
        {'id': 'any_square_root_of_minus_one_is_J', 'rationale': 'The integer matrix [[1,-1],[2,-1]] squares to -I but is neither J nor commutes with J: J is declared, not forced by J^2 = -I.', 'mutate': any_square_root_of_minus_one_is_J},
        {'id': 'j_is_the_only_square_root_of_minus_one', 'rationale': 'Only +-J commute with J, but J^2 = -I has 26 integer solutions in the box [-5,5]; reading J as unique hides the declaration.', 'mutate': j_is_the_only_square_root_of_minus_one},
        {'id': 'symmetric_real_matrix_is_hermitian_image', 'rationale': 'Symmetry alone does not put a real matrix in the image: diag(1,2,3,4) is symmetric but does not commute with J_2.', 'mutate': symmetric_real_matrix_is_hermitian_image},
        {'id': 'odd_dimension_has_a_J', 'rationale': 'A complex structure needs even real dimension; a 3 x 3 real matrix has no J_n to commute with.', 'mutate': odd_dimension_has_a_J},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
