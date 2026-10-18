"""Origin: research/quantum_to_classical_descent/check_exact.py
Claim: the finite cochain, unitary, open, measurement, Bell, and carrier fixtures hold in exact Q(i)
AuthorityEffect: None
Scope Fence: this file does not claim analytic all-time proofs, Lieb-Robinson premises, hardware, or Lean
Level: L5
MutationKillCount: 4
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product

BigRational = Fraction
F = Fraction
Mat = list[list["C"]]


def _refuse_optimized() -> None:
    if not __debug__:
        raise RuntimeError("Run without -O: certificate checks must remain enabled.")


_refuse_optimized()


class CertificateError(ValueError):
    def __init__(self, invariant: str) -> None:
        self.invariant = invariant
        super().__init__(invariant)


@dataclass(frozen=True)
class Verification:
    claim: str
    holds: bool
    detail: str


def exact_int(value: object) -> int:
    if type(value) is not int:
        raise CertificateError("Expected exact integer, received boolean or non-integer")
    return value


def exact_nat(value: object) -> int:
    number = exact_int(value)
    if number < 0:
        raise CertificateError("exact integer is nonnegative")
    return number


def big_rational(numer: object, denom: object) -> BigRational:
    den = exact_int(denom)
    if den == 0:
        raise CertificateError("rational denominator is nonzero")
    return BigRational(exact_int(numer), den)


def verify_rank(found: object, expected: object) -> Verification:
    got = exact_nat(found)
    goal = exact_nat(expected)
    if goal == 0:
        raise CertificateError("rank target is positive")
    ratio = big_rational(got, goal)
    return Verification("rank certificate", ratio == BigRational(1, 1), f"{got}/{goal}")


def _fraction(value: object) -> F:
    if isinstance(value, F):
        return value
    if isinstance(value, bool) or not isinstance(value, int):
        raise CertificateError("Q(i) coordinate is an exact integer or rational")
    return F(value)


@dataclass(frozen=True)
class C:
    re: F = F(0)
    im: F = F(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "re", _fraction(self.re))
        object.__setattr__(self, "im", _fraction(self.im))

    def __add__(self, other: object) -> C:
        partner = c(other)
        return C(self.re + partner.re, self.im + partner.im)

    def __radd__(self, other: object) -> C:
        return self + other

    def __neg__(self) -> C:
        return C(-self.re, -self.im)

    def __sub__(self, other: object) -> C:
        return self + -c(other)

    def __rsub__(self, other: object) -> C:
        return c(other) + -self

    def __mul__(self, other: object) -> C:
        partner = c(other)
        real = self.re * partner.re - self.im * partner.im
        imag = self.re * partner.im + self.im * partner.re
        return C(real, imag)

    def __rmul__(self, other: object) -> C:
        return self * other

    def conj(self) -> C:
        return C(self.re, -self.im)

    def __truediv__(self, other: object) -> C:
        partner = c(other)
        denom = partner.re * partner.re + partner.im * partner.im
        if denom == 0:
            raise CertificateError("Q(i) divisor is nonzero")
        scaled = self * partner.conj()
        return C(scaled.re / denom, scaled.im / denom)


def c(value: object) -> C:
    if isinstance(value, C):
        return value
    return C(_fraction(value), F(0))


def require(ok: bool, invariant: str) -> None:
    if not ok:
        raise CertificateError(invariant)


ZERO = C()
ONE = C(F(1))
II = C(F(0), F(1))
_BINARY = {(0, 0, 0), (1, 1, 0)}
_OUTCOMES = ((1, 1), (1, -1), (-1, 1), (-1, -1))


def _row(row: object) -> list[C]:
    if not isinstance(row, list):
        raise CertificateError("matrix row is a list")
    return [c(entry) for entry in row]


def mat(rows: object) -> Mat:
    if not isinstance(rows, list):
        raise CertificateError("matrix rows are a list")
    return [_row(row) for row in rows]


def _one(ok: bool) -> int:
    if ok:
        return 1
    return 0


def eye(n: object) -> Mat:
    size = exact_nat(n)
    return mat([[_one(i == j) for j in range(size)] for i in range(size)])


def zeros(rows: object, cols: object) -> Mat:
    height = exact_nat(rows)
    width = exact_nat(cols)
    return mat([[0] * width for _ in range(height)])


def add(left: Mat, right: Mat) -> Mat:
    rows: Mat = []
    for left_row, right_row in zip(left, right):
        rows.append([a + b for a, b in zip(left_row, right_row)])
    return rows


def scale(factor: object, matrix: Mat) -> Mat:
    coeff = c(factor)
    return [[coeff * entry for entry in row] for row in matrix]


def _dot(left: list[C], right: list[C]) -> C:
    total = ZERO
    for left_entry, right_entry in zip(left, right):
        total = total + left_entry * right_entry
    return total


def _column(matrix: Mat, index: int) -> list[C]:
    return [row[index] for row in matrix]


def mm(left: Mat, right: Mat) -> Mat:
    columns = [_column(right, index) for index in range(len(right[0]))]
    return [[_dot(row, column) for column in columns] for row in left]


def dag(matrix: Mat) -> Mat:
    return [[entry.conj() for entry in column] for column in zip(*matrix)]


def _kron_row(left_row: list[C], right_row: list[C]) -> list[C]:
    row: list[C] = []
    for left_entry in left_row:
        for right_entry in right_row:
            row.append(left_entry * right_entry)
    return row


def kron(left: Mat, right: Mat) -> Mat:
    rows: Mat = []
    for left_row in left:
        for right_row in right:
            rows.append(_kron_row(left_row, right_row))
    return rows


def trace(matrix: Mat) -> C:
    total = ZERO
    for index in range(len(matrix)):
        total = total + matrix[index][index]
    return total


def real(value: C) -> F:
    if value.im != 0:
        raise CertificateError("coordinate is real")
    return value.re


def ket(n: object, index: object) -> Mat:
    size = exact_nat(n)
    chosen = exact_nat(index)
    return mat([[_one(slot == chosen)] for slot in range(size)])


def outer(vector: Mat) -> Mat:
    return mm(vector, dag(vector))


def flatten(matrix: Mat) -> list[C]:
    row: list[C] = []
    for line in matrix:
        for entry in line:
            row.append(entry)
    return row


def _column_pivot(rows: Mat, start: int, column: int) -> int | None:
    index = start
    while index < len(rows):
        if rows[index][column] != ZERO:
            return index
        index = index + 1
    return None


def _clear_column(rows: Mat, pivot_row: int, column: int) -> None:
    pivot = rows[pivot_row][column]
    rows[pivot_row] = [entry / pivot for entry in rows[pivot_row]]
    for index in range(len(rows)):
        if index != pivot_row:
            factor = rows[index][column]
            rows[index] = [left - factor * right for left, right in zip(rows[index], rows[pivot_row])]


def _eliminate_column(rows: Mat, rank_index: int, column: int) -> int:
    pivot = _column_pivot(rows, rank_index, column)
    if pivot is None:
        return rank_index
    rows[rank_index], rows[pivot] = rows[pivot], rows[rank_index]
    _clear_column(rows, rank_index, column)
    return rank_index + 1


def basis(matrix: Mat) -> Mat:
    if not matrix or not matrix[0]:
        return []
    rows = [row[:] for row in matrix]
    rank_index = 0
    for column in range(len(rows[0])):
        rank_index = _eliminate_column(rows, rank_index, column)
    return rows[:rank_index]


def rank(matrix: Mat) -> int:
    return len(basis(matrix))


def closure(seed: Mat, step: Mat) -> tuple[Mat, list[int]]:
    current = basis(seed)
    dimensions = [len(current)]
    steps = 0
    while steps < 8:
        grown = basis(current + mm(current, step))
        dimensions.append(len(grown))
        if len(grown) == len(current):
            return grown, dimensions
        current = grown
        steps = steps + 1
    raise CertificateError("closure stabilizes")


def _pivot_clear(matrix: Mat, index: int) -> bool:
    row = index + 1
    while row < len(matrix):
        if matrix[row][index] != ZERO:
            return False
        row = row + 1
    return True


def _scaled_difference(row: list[C], pivot_row: list[C], factor: C) -> list[C]:
    updated: list[C] = []
    for left, right in zip(row, pivot_row):
        updated.append(left - factor * right)
    return updated


def _schur(matrix: Mat, index: int, pivot: F) -> None:
    row = index + 1
    while row < len(matrix):
        matrix[row] = _scaled_difference(matrix[row], matrix[index], matrix[row][index] / pivot)
        row = row + 1


def _psd_pivot(matrix: Mat, index: int) -> None:
    pivot = real(matrix[index][index])
    if pivot < 0:
        raise CertificateError("Hermitian pivot is nonnegative")
    if pivot == 0:
        if not _pivot_clear(matrix, index):
            raise CertificateError("zero pivot column is clear")
        return
    _schur(matrix, index, pivot)


def psd(matrix: Mat) -> None:
    if matrix != dag(matrix):
        raise CertificateError("argument is Hermitian")
    work = [row[:] for row in matrix]
    for index in range(len(work)):
        _psd_pivot(work, index)


def density(matrix: Mat) -> None:
    psd(matrix)
    require(trace(matrix) == ONE, "density trace is 1")


def _kept_index(bits: tuple[int, ...], keep: tuple[int, ...]) -> int:
    total = 0
    width = len(keep)
    place = 0
    while place < width:
        total = total + (bits[keep[place]] << (width - place - 1))
        place = place + 1
    return total


def _same_traced(left: tuple[int, ...], right: tuple[int, ...], keep: tuple[int, ...], n: int) -> bool:
    kept = set(keep)
    bit = 0
    while bit < n:
        if bit not in kept and left[bit] != right[bit]:
            return False
        bit = bit + 1
    return True


def _accumulate(
    result: Mat,
    state: Mat,
    bits: list[tuple[int, ...]],
    row_bits: tuple[int, ...],
    row_index: int,
    keep: tuple[int, ...],
    n: int,
) -> None:
    col_index = 0
    while col_index < len(bits):
        col_bits = bits[col_index]
        if _same_traced(row_bits, col_bits, keep, n):
            u = _kept_index(row_bits, keep)
            v = _kept_index(col_bits, keep)
            result[u][v] = result[u][v] + state[row_index][col_index]
        col_index = col_index + 1


def _bit_tuples(n: int) -> list[tuple[int, ...]]:
    typed: list[tuple[int, ...]] = []
    for item in product((0, 1), repeat=exact_nat(n)):
        typed.append(tuple(exact_int(bit) for bit in item))
    return typed


def ptrace(state: Mat, keep: tuple[int, ...], n: object) -> Mat:
    qubits = exact_nat(n)
    bits = _bit_tuples(qubits)
    result = zeros(2 ** len(keep), 2 ** len(keep))
    for index, row_bits in enumerate(bits):
        _accumulate(result, state, bits, row_bits, index, keep, qubits)
    return result


def _max_abs(column: Mat) -> F:
    best = F(0)
    for row in column:
        size = abs(real(row[0]))
        if size > best:
            best = size
    return best


def _sum_abs(column: Mat) -> F:
    total = F(0)
    for row in column:
        total = total + abs(real(row[0]))
    return total


def _sum_real(column: Mat) -> F:
    total = F(0)
    for row in column:
        total = total + real(row[0])
    return total


def _require_rank(matrix: Mat, expected: int, invariant: str) -> None:
    require(verify_rank(rank(matrix), expected).holds, invariant)


def run_cochain() -> None:
    d0 = mat([[-1, 0, 0], [-1, 0, 0]])
    qp = mat([[1, 1]])
    qm = mat([[1, -1]])
    stacked = qp + qm
    right_b = mat([[1], [1]])
    right_w = mat([[1], [-1]])
    require(verify_rank(rank(d0), 1).holds, "cochain rank D0 is 1")
    _require_rank(stacked, 2, "cochain rank A is 2")
    require(mm(d0, mat([[-1], [0], [0]])) == right_b, "cochain D0 maps the first cycle to b")
    require(mm(d0, mat([[0, 0], [1, 0], [0, 1]])) == zeros(2, 2), "cochain D0 kills the face pair")
    require(mm(qp, right_w) == mat([[0]]), "qp annihilates w")
    require(mm(qm, right_b) == mat([[0]]), "qm annihilates b")
    require(mm(qp, right_b) == mat([[2]]), "qp pairs with b")
    require(mm(qm, right_w) == mat([[2]]), "qm pairs with w")
    _require_rank(dag(right_b) + dag(right_w), 2, "completed constants span rank 2")
    require(mm(dag(d0), right_w) == zeros(3, 1), "D0 adjoint kills w")
    require(mm(dag(right_w), right_w) == mat([[2]]), "w norm is 2")
    require(_max_abs(right_w) == F(1), "w height is 1")
    require(_sum_abs(right_w) == F(2), "w mass is 2")
    require(mm(stacked, right_b) == mat([[2], [0]]), "A b is (2, 0)")
    require(mm(stacked, right_w) == mat([[0], [2]]), "A w is (0, 2)")
    require(mm(scale(F(1, 2), stacked), stacked) == eye(2), "half A is a left inverse")
    print("cochain: rank D0=1; Phi(b)=0; Phi(w)=2; completed constants=1,1")


def _projector_checks() -> None:
    proj = mat([[1, 0], [0, 0]])
    lower = mat([[0, 0], [1, 0]])
    upper = dag(lower)
    complement = add(eye(2), scale(-1, proj))
    require(mm(mm(proj, lower), complement) == zeros(2, 2), "lower raises into the projector")
    require(mm(complement, mm(lower, ket(2, 0))) == ket(2, 1), "lower sends the ground ket up")
    require(mm(mm(proj, upper), complement) != zeros(2, 2), "upper leaves the complement")
    require(mm(mm(proj, upper), proj) == zeros(2, 2), "upper kills the projector")
    bad = mat([[1, 0], [0, 2]])
    require(mm(mat([[1, -1]]), mm(bad, mat([[1], [1]]))) == mat([[-1]]), "bad generator is visible")


def _unitary_closure() -> None:
    ell = mat([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    q = mat([[0, 0, 1]])
    ad = q + mat([[0, 1, 0]])
    em = mat([[0, 1], [-1, 0]])
    vec = mat([[0], [1], [0]])
    require(mm(q, vec) == mat([[0]]), "Q v is 0")
    require(mm(mm(q, ell), vec) == mat([[1]]), "Q L v is 1")
    require(mm(ad, ell) == mm(em, ad), "Ad intertwines L and M")
    rows, dims = closure(q, ell)
    require(dims == [1, 2, 2], "closure ranks are 1,2,2")
    require(rows == basis(ad), "closure equals the Ad row space")
    stacked = q + mm(q, ell) + mm(mm(q, ell), ell)
    require(basis(stacked) == rows, "the cubic word spans the closure")
    require(mm(mm(q, ell), ell) == scale(-1, q), "L squared acts as -1 on Q")
    _projector_checks()


def comm(left: Mat, right: Mat) -> Mat:
    return add(mm(left, right), scale(-1, mm(right, left)))


def _generator(state: Mat, ham: Mat) -> Mat:
    return scale(-II, comm(ham, state))


def _paulis() -> tuple[Mat, Mat, Mat, Mat]:
    return (
        eye(2),
        mat([[0, 1], [1, 0]]),
        mat([[0, -II], [II, 0]]),
        mat([[1, 0], [0, -1]]),
    )


def _lie_row(left: Mat, paulis: list[Mat], ham: Mat) -> list[C]:
    row: list[C] = []
    for right in paulis:
        row.append(trace(mm(left, _generator(scale(F(1, 2), right), ham))))
    return row


def _lie_matrix(paulis: list[Mat], ham: Mat) -> Mat:
    return [_lie_row(left, paulis, ham) for left in paulis]


def _sign_once(sign: int, i2: Mat, y: Mat, z: Mat, ham: Mat) -> None:
    state = scale(F(1, 2), add(i2, scale(sign * F(3, 5), y)))
    density(state)
    require(trace(mm(z, state)) == ZERO, "Y rotation keeps Z expectation 0")
    require(trace(mm(z, _generator(state, ham))) == c(sign * F(3, 5)), "derivative is signed 3/5")
    factor = add(i2, scale(-II, mat([[0, 1], [1, 0]])))
    rotated = scale(F(1, 2), mm(mm(factor, state), dag(factor)))
    require(trace(mm(z, rotated)) == c(sign * F(3, 5)), "rotated Z expectation is signed 3/5")


def _sign_suite(i2: Mat, y: Mat, z: Mat, ham: Mat) -> None:
    for sign in (1, -1):
        _sign_once(sign, i2, y, z, ham)


def run_unitary() -> None:
    _unitary_closure()
    i2, x, y, z = _paulis()
    ham = scale(F(1, 2), x)
    ell = mat([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    require(_lie_matrix([x, y, z], ham) == ell, "Pauli derivatives reproduce L")
    _sign_suite(i2, y, z, ham)
    require(comm(y, z) == scale(2 * II, x), "Pauli commutator")
    require(rank([flatten(i2), flatten(z), flatten(y)]) == 3, "I, Z, Y are independent")
    half = mat([[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]])
    require(mm(half, half) == half, "half projector squares")
    require(half != x, "half projector is not the bit flip")
    print("unitary fixture: derivatives +/-3/5; closure ranks=1,2,2; one new row")


def _lindblad_term(state: Mat, jump: Mat) -> Mat:
    emission = mm(dag(jump), jump)
    sandwich = mm(mm(jump, state), dag(jump))
    damp = scale(F(-1, 2), add(mm(emission, state), mm(state, emission)))
    return add(sandwich, damp)


def lindblad(state: Mat) -> Mat:
    result = zeros(2, 2)
    jumps = ((1, mat([[0, 1], [0, 0]])), (2, mat([[0, 0], [1, 0]])))
    for rate, jump in jumps:
        result = add(result, scale(rate, _lindblad_term(state, jump)))
    return result


def _open_cell(i: int, j: int, rate: Mat) -> None:
    basis_op = mm(ket(2, i), dag(ket(2, j)))
    out = lindblad(basis_op)
    diag = mat([[out[0][0]], [out[1][1]]])
    column = mat([[basis_op[0][0]], [basis_op[1][1]]])
    require(diag == mm(rate, column), "populations follow G")
    if i != j:
        require(out == scale(F(-3, 2), basis_op), "coherences decay at 3/2")


def _open_population(rate: Mat) -> None:
    stationary = mat([[F(1, 3)], [F(2, 3)]])
    require(mm(rate, stationary) == zeros(2, 1), "stationary population")
    require(mm(mat([[1, 1]]), rate) == zeros(1, 2), "trace is conserved")
    pi = mat([[F(1, 3), F(1, 3)], [F(2, 3), F(2, 3)]])
    require(mm(pi, pi) == pi, "Pi is a projector")
    require(rate == scale(-3, add(eye(2), scale(-1, pi))), "G is the scaled complement of Pi")


def run_open() -> None:
    rate = mat([[-2, 1], [2, -1]])
    for i, j in product(range(2), repeat=2):
        _open_cell(i, j, rate)
    _open_population(rate)
    print("open fixture: G=[[-2,1],[2,-1]]; stationary=(1/3,2/3)")


def _cnot_image(state: int, control: int, target: int) -> int:
    if state & (1 << (2 - control)):
        return state ^ (1 << (2 - target))
    return state


def cnot(control: object, target: object) -> Mat:
    gate = zeros(8, 8)
    control_bit = exact_nat(control)
    target_bit = exact_nat(target)
    state = 0
    while state < 8:
        gate[_cnot_image(state, control_bit, target_bit)][state] = ONE
        state = state + 1
    return gate


def _permutation_ok(unitary: Mat) -> None:
    images = (0, 1, 3, 2, 7, 6, 4, 5)
    state = 0
    while state < 8:
        require(mm(unitary, ket(8, state)) == ket(8, images[state]), "cnot permutation")
        state = state + 1
    require(mm(dag(unitary), unitary) == eye(8), "cnot is unitary")


def _prepared() -> tuple[Mat, Mat]:
    initial = add(scale(F(3, 5), ket(8, 0)), scale(F(4, 5), ket(8, 4)))
    psi = add(scale(F(3, 5), ket(8, 0)), scale(F(4, 5), ket(8, 7)))
    return initial, psi


def _pointers() -> list[Mat]:
    identity = eye(2)
    projectors = (outer(ket(2, 0)), outer(ket(2, 1)))
    return [kron(kron(identity, proj), identity) for proj in projectors]


def _pointer_products(pointer: list[Mat]) -> None:
    left = 0
    while left < 2:
        right = 0
        while right < 2:
            expected = pointer[left] if left == right else zeros(8, 8)
            require(mm(pointer[left], pointer[right]) == expected, "pointer projectors multiply")
            right = right + 1
        left = left + 1


def _kraus_resolution(pointer: list[Mat]) -> None:
    first = [row[0] for row in ket(8, 0)]
    second = [row[0] for row in ket(8, 7)]
    width = [list(pair) for pair in zip(first, second)]
    left = mm(pointer[0], width)
    right = mm(pointer[1], width)
    require(add(mm(dag(left), left), mm(dag(right), right)) == eye(2), "Kraus resolution")


def _outcome_probabilities(pointer: list[Mat], rho: Mat, sigma: Mat) -> None:
    found = [real(trace(mm(proj, rho))) for proj in pointer]
    require(found == [F(9, 25), F(16, 25)], "outcome probabilities")
    collapsed = add(mm(mm(pointer[0], rho), pointer[0]), mm(mm(pointer[1], rho), pointer[1]))
    require(collapsed == sigma, "selective state is sigma")


def _partial_size(rho: Mat, sigma: Mat, size: int) -> None:
    for keep in combinations(range(3), size):
        kept = tuple(keep)
        require(ptrace(rho, kept, 3) == ptrace(sigma, kept, 3), "partial traces agree")
        density(ptrace(rho, kept, 3))


def _partial_agrees(rho: Mat, sigma: Mat) -> None:
    size = 0
    while size < 3:
        _partial_size(rho, sigma, size)
        size = size + 1


def _xxx(matrix: Mat) -> C:
    x = mat([[0, 1], [1, 0]])
    return trace(mm(matrix, kron(kron(x, x), x)))


def _difference_sign(diff: Mat, sign: int) -> None:
    vector = add(ket(8, 0), scale(sign, ket(8, 7)))
    require(mm(diff, vector) == scale(sign * F(12, 25), vector), "difference eigenvalue")


def _difference_kernel(diff: Mat) -> None:
    state = 1
    while state < 7:
        require(mm(diff, ket(8, state)) == zeros(8, 1), "difference kernel")
        state = state + 1


def _offdiag_zero(residual: Mat) -> None:
    row = 0
    while row < 4:
        col = 0
        while col < 4:
            if row != col:
                require(residual[row][col] == ZERO, "SA residual is diagonal")
            col = col + 1
        row = row + 1


def _sum_abs_diag(residual: Mat) -> F:
    total = F(0)
    index = 0
    while index < 4:
        total = total + abs(real(residual[index][index]))
        index = index + 1
    return total


def _sa_defect(rho: Mat) -> None:
    sa = ptrace(rho, (0, 1), 3)
    prod = kron(ptrace(rho, (0,), 3), ptrace(rho, (1,), 3))
    residual = add(sa, scale(-1, prod))
    diagonal = [real(residual[index][index]) for index in range(4)]
    expected = [F(144, 625) * sign for sign in (1, -1, -1, 1)]
    require(diagonal == expected, "SA diagonal defect")
    _offdiag_zero(residual)
    require(_sum_abs_diag(residual) == F(576, 625), "SA defect mass")


def run_measurement() -> None:
    unitary = mm(cnot(1, 2), cnot(0, 1))
    _permutation_ok(unitary)
    initial, psi = _prepared()
    require(mm(unitary, initial) == psi, "prepared state maps to psi")
    rho = outer(psi)
    sigma = add(scale(F(9, 25), outer(ket(8, 0))), scale(F(16, 25), outer(ket(8, 7))))
    pointer = _pointers()
    require(add(pointer[0], pointer[1]) == eye(8), "pointers resolve the identity")
    _kraus_resolution(pointer)
    _pointer_products(pointer)
    _outcome_probabilities(pointer, rho, sigma)
    _partial_agrees(rho, sigma)
    density(rho)
    density(sigma)
    require(_xxx(rho) == c(F(24, 25)), "rho XXX correlation")
    require(_xxx(sigma) == ZERO, "sigma XXX correlation")
    diff = add(rho, scale(-1, sigma))
    for sign in (1, -1):
        _difference_sign(diff, sign)
    _difference_kernel(diff)
    _sa_defect(rho)
    require(rank([flatten(pointer[0]), flatten(pointer[1])]) == 2, "pointers are independent")
    print("measurement: p=(9/25,16/25); D(rho,sigma)=12/25; SA defect=576/625")


def _observables() -> tuple[list[Mat], list[Mat]]:
    z = mat([[1, 0], [0, -1]])
    x = mat([[0, 1], [1, 0]])
    alice = [z, x]
    bob = [
        scale(F(1, 5), add(scale(4, z), scale(3, x))),
        scale(F(1, 5), add(scale(4, z), scale(-3, x))),
    ]
    return alice, bob


def _observable_ok(observable: Mat) -> None:
    require(dag(observable) == observable, "observable is Hermitian")
    require(mm(observable, observable) == eye(2), "observable squares to identity")


def _effect(alice: list[Mat], bob: list[Mat], x: int, y: int, a: int, bval: int) -> Mat:
    left = scale(F(1, 2), add(eye(2), scale(a, alice[x])))
    right = scale(F(1, 2), add(eye(2), scale(bval, bob[y])))
    return kron(left, right)


def _bell_row_ok(table: list[F]) -> None:
    require(sum(table, F(0)) == 1, "bell row sums to 1")
    require(min(table) >= 0, "bell row is nonnegative")
    require(table[0] + table[1] == F(1, 2), "bell row pair 01")
    require(table[2] + table[3] == F(1, 2), "bell row pair 23")
    require(table[0] + table[2] == F(1, 2), "bell row pair 02")
    require(table[1] + table[3] == F(1, 2), "bell row pair 13")


def _bell_row(alice: list[Mat], bob: list[Mat], bell: Mat, x: int, y: int) -> list[F]:
    table: list[F] = []
    for a, bval in _OUTCOMES:
        effect = _effect(alice, bob, x, y, a, bval)
        psd(effect)
        table.append(real(trace(mm(bell, effect))))
    _bell_row_ok(table)
    return table


def _contexts() -> list[tuple[int, int]]:
    found: list[tuple[int, int]] = []
    for pair in product(range(2), repeat=2):
        found.append((pair[0], pair[1]))
    return found


def _correlation(table: list[F]) -> F:
    total = F(0)
    for (a, bval), prob in zip(_OUTCOMES, table):
        total = total + F(a * bval) * prob
    return total


def _score(correlations: list[F]) -> F:
    total = F(0)
    for sign, value in zip((1, 1, 1, -1), correlations):
        total = total + F(sign) * value
    return total


def _assignments() -> list[tuple[int, int, int, int]]:
    found: list[tuple[int, int, int, int]] = []
    for lam in product((1, -1), repeat=4):
        found.append((lam[0], lam[1], lam[2], lam[3]))
    return found


def _marginal_row(ok: bool) -> C:
    if ok:
        return ONE
    return ZERO


def _marginal(assignments: list[tuple[int, int, int, int]]) -> Mat:
    rows: Mat = []
    for x, y in _contexts():
        for a, bval in _OUTCOMES:
            row = [_marginal_row(lam[x] == a and lam[2 + y] == bval) for lam in assignments]
            rows.append(row)
    return rows


def _dual_entry(x: int, y: int, a: int, bval: int) -> C:
    sign = 1
    if (x, y) == (1, 1):
        sign = -1
    return c(F(1, 2) - sign * a * bval)


def _dual() -> Mat:
    rows: Mat = []
    for x, y in _contexts():
        for a, bval in _OUTCOMES:
            rows.append([_dual_entry(x, y, a, bval)])
    return rows


def _dual_image(marginal: Mat, dual: Mat) -> None:
    found: set[F] = set()
    for row in mm(dag(marginal), dual):
        found.add(real(row[0]))
    require(found == {F(0), F(4)}, "dual transpose entries")


def _tvec(tables: list[list[F]]) -> Mat:
    rows: Mat = []
    for table in tables:
        for prob in table:
            rows.append([c(prob)])
    return rows


def _signed_entry(a0: int, a1: int, b0: int, b1: int) -> C:
    value = (
        1
        + F(4, 5) * a0 * b0
        + F(4, 5) * a0 * b1
        + F(3, 5) * a1 * b0
        - F(3, 5) * a1 * b1
    )
    return c(value / 16)


def _signed(assignments: list[tuple[int, int, int, int]]) -> Mat:
    return [[_signed_entry(*lam)] for lam in assignments]


def _min_real(column: Mat) -> F:
    best = real(column[0][0])
    for row in column[1:]:
        value = real(row[0])
        if value < best:
            best = value
    return best


def _expected_tables() -> list[list[F]]:
    first = [F(9, 20), F(1, 20), F(1, 20), F(9, 20)]
    third = [F(2, 5), F(1, 10), F(1, 10), F(2, 5)]
    fourth = [F(1, 10), F(2, 5), F(2, 5), F(1, 10)]
    return [first, list(first), third, fourth]


def run_bell() -> None:
    bell = scale(F(1, 2), outer(add(ket(4, 0), ket(4, 3))))
    density(bell)
    alice, bob = _observables()
    for observable in alice + bob:
        _observable_ok(observable)
    tables = [_bell_row(alice, bob, bell, x, y) for x, y in _contexts()]
    require(tables == _expected_tables(), "bell probability tables")
    correlations = [_correlation(table) for table in tables]
    require(correlations == [F(4, 5), F(4, 5), F(3, 5), F(-3, 5)], "bell correlations")
    require(_score(correlations) == F(14, 5), "Bell score is 14/5")
    assignments = _assignments()
    marginal = _marginal(assignments)
    dual = _dual()
    _dual_image(marginal, dual)
    require(mm(dag(dual), _tvec(tables)) == mat([[F(-4, 5)]]), "dual objective")
    signed = _signed(assignments)
    require(mm(marginal, signed) == _tvec(tables), "signed distribution reproduces the tables")
    require(_min_real(signed) == F(-3, 80), "signed distribution minimum")
    print("Bell: S=14/5; dual transpose entries={0,4}; dual objective=-4/5")


def _triangle() -> None:
    triangle = mat([[-1, 1, 0], [0, -1, 1], [1, 0, -1]])
    trial = mm(triangle, mat([[0], [1], [0]]))
    require(trial == mat([[1], [-1], [0]]), "triangle image")
    require(_sum_real(trial) == F(0), "triangle quotient")
    require(_sum_abs(trial) == F(2), "triangle raw mass")
    _require_rank(triangle, 2, "triangle rank")


def syndrome(word: tuple[int, int, int]) -> int:
    return word[0] ^ word[1]


def xor_word(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    return (left[0] ^ right[0], left[1] ^ right[1], left[2] ^ right[2])


def _pair_ok(left: tuple[int, int, int], group: list[tuple[int, int, int]]) -> bool:
    for right in group:
        if syndrome(left) == syndrome(right) and xor_word(left, right) not in _BINARY:
            return False
    return True


def criterion(group: list[tuple[int, int, int]]) -> bool:
    for left in group:
        if not _pair_ok(left, group):
            return False
    return True


def _binary_checks() -> None:
    good = [(0, 0, 0), (1, 0, 0)]
    bad = [(0, 0, 0), (0, 0, 1)]
    require(criterion(good), "good errors correct")
    require(not criterion(bad), "bad errors do not correct")
    for word in good:
        require(xor_word(word, good[syndrome(word)]) in _BINARY, "syndrome lookup lands in the code")


def _between(low: int, high: int, items: set[int]) -> int:
    count = 0
    for item in items:
        if low < item < high:
            count = count + 1
    return count


def _edge_parity(before: set[int], after: set[int]) -> int:
    lost = before - after
    gained = after - before
    if len(lost) != 1 or len(gained) != 1:
        raise CertificateError("star edge changes one vertex")
    src = next(iter(lost))
    dst = next(iter(gained))
    if 0 not in (src, dst):
        raise CertificateError("star edge touches the center")
    return _between(min(src, dst), max(src, dst), before) % 2


def _sum_int(values: list[int]) -> int:
    total = 0
    for value in values:
        total = total + value
    return total


def _star_loop() -> None:
    loop = [{1, 2}, {0, 2}, {2, 3}, {0, 3}, {1, 3}, {0, 1}, {1, 2}]
    parities: list[int] = []
    index = 0
    while index < len(loop) - 1:
        parities.append(_edge_parity(loop[index], loop[index + 1]))
        index = index + 1
    require(parities == [0, 1, 0, 0, 1, 1], "star parities")
    require(_sum_int(parities) % 2 == 1, "star loop is odd")


def run_other() -> None:
    _triangle()
    _binary_checks()
    _star_loop()
    print("other carriers: triangle raw=2, quotient=0; binary correction controls; odd star loop")


def main() -> int:
    run_cochain()
    run_unitary()
    run_open()
    run_measurement()
    run_bell()
    run_other()
    print("PASS: explicit finite certificates, using exact Q(i) arithmetic.")
    print(
        "Not checked by this program: analytic all-time proofs, Lieb-Robinson premises, hardware, or Lean."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
