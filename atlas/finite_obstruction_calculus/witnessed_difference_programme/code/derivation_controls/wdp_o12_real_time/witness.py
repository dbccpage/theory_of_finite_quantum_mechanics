"""Infinite-temperature atomic moments of one finite Meron row-sum.

Labelled carrier: periodic full-Fock CAR ring, even L=4, dimension 16.
Integer scaling is the TL-0 ring: K4 = 4 K_L and A2 = 2 A_L.
Not a Lebesgue density, not a Gibbs state, and not a continuum limit.
"""

from __future__ import annotations

from fractions import Fraction


def _zeros(dim: int) -> list[list[int]]:
    return [[0] * dim for _ in range(dim)]


def _transpose(mat: list[list[int]]) -> list[list[int]]:
    dim = len(mat)
    return [[mat[row][col] for row in range(dim)] for col in range(dim)]


def _scale(mat: list[list[int]], factor: int) -> list[list[int]]:
    return [[factor * value for value in row] for row in mat]


def _add(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    dim = len(left)
    return [[left[row][col] + right[row][col] for col in range(dim)] for row in range(dim)]


def _sub(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    dim = len(left)
    return [[left[row][col] - right[row][col] for col in range(dim)] for row in range(dim)]


def _matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    dim = len(left)
    out = _zeros(dim)
    for mid in range(dim):
        right_row = right[mid]
        for col, right_value in enumerate(right_row):
            if right_value == 0:
                continue
            for row in range(dim):
                left_value = left[row][mid]
                if left_value:
                    out[row][col] += left_value * right_value
    return out


def _symmetric(mat: list[list[int]]) -> bool:
    dim = len(mat)
    for row in range(dim):
        for col in range(row + 1, dim):
            if mat[col][row] != mat[row][col]:
                return False
    return True


def _antihermitian(mat: list[list[int]]) -> bool:
    dim = len(mat)
    for row in range(dim):
        for col in range(dim):
            if mat[col][row] != -mat[row][col]:
                return False
    return True


def _frobenius(left: list[list[int]], right: list[list[int]]) -> int:
    total = 0
    for row, left_row in enumerate(left):
        right_row = right[row]
        for col, left_value in enumerate(left_row):
            right_value = right_row[col]
            if left_value and right_value:
                total += left_value * right_value
    return total


def _raise_mismatch(name: str, left: list[list[int]], right: list[list[int]]) -> None:
    for row, left_row in enumerate(left):
        for col, left_value in enumerate(left_row):
            right_value = right[row][col]
            if left_value != right_value:
                raise RuntimeError(
                    f"{name} disagrees at {(row, col)}: {left_value} != {right_value}"
                )
    raise RuntimeError(f"{name} disagrees")


def _annihilator(modes: int, site: int) -> list[list[int]]:
    dim = 1 << modes
    mat = _zeros(dim)
    low_mask = (1 << site) - 1
    for source in range(dim):
        if (source >> site) & 1:
            sign = -1 if (source & low_mask).bit_count() % 2 else 1
            mat[source ^ (1 << site)][source] = sign
    return mat


def _number_diag(annihilator: list[list[int]]) -> list[int]:
    dim = len(annihilator)
    diag = [0] * dim
    for col in range(dim):
        acc = 0
        for row in range(dim):
            value = annihilator[row][col]
            if value:
                acc += value * value
        diag[col] = acc
    return diag


def _apply(kind: str, site: int, state: int) -> tuple[int, int] | None:
    occupied = (state >> site) & 1
    if kind == "ann":
        if not occupied:
            return None
    elif kind == "cre":
        if occupied:
            return None
    else:
        raise RuntimeError("operator kind is not ann or cre")
    sign = -1 if (state & ((1 << site) - 1)).bit_count() % 2 else 1
    return state ^ (1 << site), sign


def _four_point_trace(length: int, p: int, q: int, r: int, s: int) -> int:
    """Tr(c_p* c_q c_r* c_s) by applying the word to every Fock state."""
    total = 0
    for state in range(1 << length):
        current = state
        coeff = 1
        failed = False
        for kind, site in (("ann", s), ("cre", r), ("ann", q), ("cre", p)):
            step = _apply(kind, site, current)
            if step is None:
                failed = True
                break
            current, sign = step
            coeff *= sign
        if not failed and current == state:
            total += coeff
    return total


def _check_four_point(length: int) -> None:
    dim = 1 << length
    for p in range(length):
        for q in range(length):
            for r in range(length):
                for s in range(length):
                    got = _four_point_trace(length, p, q, r, s)
                    first = 1 if p == q and r == s else 0
                    second = 1 if p == s and q == r else 0
                    expect = (dim // 4) * (first + second)
                    if got != expect:
                        raise RuntimeError(
                            f"four-point L={length} {(p, q, r, s)}: {got} != {expect}"
                        )


def _current(annihilators: list[list[list[int]]], site: int, length: int) -> list[list[int]]:
    nxt = (site + 1) % length
    forward = _matmul(_transpose(annihilators[site]), annihilators[nxt])
    backward = _matmul(_transpose(annihilators[nxt]), annihilators[site])
    return _sub(forward, backward)


def _jw_ring(
    length: int,
) -> tuple[list[list[int]], list[int], list[list[list[int]]], list[list[list[int]]]]:
    dim = 1 << length
    annihilators = [_annihilator(length, site) for site in range(length)]
    numbers = [_number_diag(mat) for mat in annihilators]
    for site, diag in enumerate(numbers):
        for state, value in enumerate(diag):
            if value != ((state >> site) & 1):
                raise RuntimeError("number operator disagrees with the occupation bit")
    hamiltonian = _zeros(dim)
    for state in range(dim):
        hamiltonian[state][state] = length
    projectors: list[list[list[int]]] = []
    currents: list[list[list[int]]] = []
    for site in range(length):
        nxt = (site + 1) % length
        hop = _add(
            _matmul(_transpose(annihilators[site]), annihilators[nxt]),
            _matmul(_transpose(annihilators[nxt]), annihilators[site]),
        )
        projector = _scale(hop, 2)
        for state in range(dim):
            density = (
                numbers[site][state]
                + numbers[nxt][state]
                - 2 * numbers[site][state] * numbers[nxt][state]
            )
            projector[state][state] += 2 * density
        hamiltonian = _sub(hamiltonian, projector)
        projectors.append(projector)
        currents.append(_current(annihilators, site, length))
    staggered = [0] * dim
    for state in range(dim):
        acc = 0
        for site in range(length):
            sign = -1 if site % 2 else 1
            acc += sign * (2 * numbers[site][state] - 1)
        staggered[state] = acc
    return hamiltonian, staggered, projectors, currents


def _bit_ring(length: int) -> tuple[list[list[int]], list[int]]:
    """Same K4 and diagonal of A2, written from occupation bits."""
    dim = 1 << length
    hamiltonian = _zeros(dim)
    for site in range(length):
        nxt = (site + 1) % length
        lo, hi = (site, nxt) if site < nxt else (nxt, site)
        between = ((1 << hi) - 1) ^ ((1 << (lo + 1)) - 1)
        for state in range(dim):
            left = (state >> site) & 1
            right = (state >> nxt) & 1
            density = left + right - 2 * left * right
            hamiltonian[state][state] += 1 - 2 * density
            if left != right:
                sign = -1 if (state & between).bit_count() % 2 else 1
                target = state ^ (1 << lo) ^ (1 << hi)
                hamiltonian[target][state] -= 2 * sign
    staggered = [0] * dim
    for state in range(dim):
        acc = 0
        for site in range(length):
            sign = -1 if site % 2 else 1
            acc += sign * (2 * ((state >> site) & 1) - 1)
        staggered[state] = acc
    return hamiltonian, staggered


def _check_projectors(length: int, hamiltonian: list[list[int]], projectors: list[list[list[int]]]) -> None:
    dim = 1 << length
    total = _zeros(dim)
    for projector in projectors:
        if not _symmetric(projector):
            raise RuntimeError("4P is not symmetric")
        if _matmul(projector, projector) != _scale(projector, 4):
            raise RuntimeError("(4P)^2 is not 4*(4P)")
        total = _add(total, projector)
    bare = _zeros(dim)
    for state in range(dim):
        bare[state][state] = length
    if _sub(bare, total) != hamiltonian:
        raise RuntimeError("K4 is not L*I - sum 4P")


def _commutator(hamiltonian: list[list[int]], staggered: list[int]) -> list[list[int]]:
    dim = len(staggered)
    comm = _zeros(dim)
    for row in range(dim):
        left = staggered[row]
        source = hamiltonian[row]
        target = comm[row]
        for col, entry in enumerate(source):
            if entry:
                target[col] = entry * (staggered[col] - left)
    return comm


def _scaled_edge_commutator(currents: list[list[list[int]]]) -> list[list[int]]:
    # [K4, A2] = 8 [K_L, A_L] and [K_L, A_L] = sum_x (-1)^x j_x.
    dim = len(currents[0])
    total = _zeros(dim)
    for site, current in enumerate(currents):
        if not _antihermitian(current):
            raise RuntimeError("edge current is not real antihermitian")
        sign = -1 if site % 2 else 1
        for row in range(dim):
            target = total[row]
            for col, entry in enumerate(current[row]):
                if entry:
                    target[col] += 8 * sign * entry
    return total


def _trace_numbers(staggered: list[int], comm: list[list[int]]) -> tuple[int, int, int]:
    trace_square = sum(value * value for value in staggered)
    trace_odd = 0
    trace_comm = 0
    for row, value in enumerate(staggered):
        trace_odd += value * comm[row][row]
        for entry in comm[row]:
            if entry:
                trace_comm += entry * entry
    return trace_square, trace_odd, trace_comm


def _check_edge_square(length: int, currents: list[list[list[int]]]) -> None:
    dim = 1 << length
    for site, current in enumerate(currents):
        nxt = (site + 1) % length
        squared = _matmul(_transpose(current), current)
        for state in range(dim):
            left = (state >> site) & 1
            right = (state >> nxt) & 1
            expect = left + right - 2 * left * right
            if squared[state][state] != expect:
                raise RuntimeError("j* j is not the edge density")
            for col in range(dim):
                if col != state and squared[state][col] != 0:
                    raise RuntimeError("j* j is not diagonal")


def _tr_jstar_j(length: int, left: int, right: int) -> int:
    left_next = (left + 1) % length
    right_next = (right + 1) % length
    terms = (
        (1, left_next, left, right, right_next),
        (-1, left_next, left, right_next, right),
        (-1, left, left_next, right, right_next),
        (1, left, left_next, right_next, right),
    )
    total = 0
    for coeff, p, q, r, s in terms:
        total += coeff * _four_point_trace(length, p, q, r, s)
    return total


def _edge_gram_states(length: int) -> list[list[int]]:
    return [[_tr_jstar_j(length, left, right) for right in range(length)] for left in range(length)]


def _edge_gram_matrices(currents: list[list[list[int]]]) -> list[list[int]]:
    count = len(currents)
    return [[_frobenius(currents[left], currents[right]) for right in range(count)] for left in range(count)]


def _same_two_sites(length: int, left: int, right: int) -> bool:
    return right == (left + 1) % length and (right + 1) % length == left


def _check_pair_expansion(length: int, trace_a2: int) -> None:
    dim = 1 << length
    pair = [[0] * length for _ in range(length)]
    for state in range(dim):
        diags = []
        for site in range(length):
            sign = -1 if site % 2 else 1
            diags.append(sign * (2 * ((state >> site) & 1) - 1))
        for left in range(length):
            for right in range(length):
                pair[left][right] += diags[left] * diags[right]
    for left in range(length):
        for right in range(length):
            if left == right:
                if pair[left][right] != dim:
                    raise RuntimeError("(2a_x)^2 is not I")
            elif pair[left][right] != 0:
                raise RuntimeError("distinct staggered densities are not trace-orthogonal")
            occupations = _number_cross(length, left, right)
            if left == right and occupations != Fraction(1, 4):
                raise RuntimeError("on-site density square is not 1/4")
            if left != right and occupations != 0:
                raise RuntimeError("off-site density square did not cancel")
    if sum(sum(row) for row in pair) != trace_a2:
        raise RuntimeError("row-sum square disagrees with the site expansion")


def _number_cross(length: int, left: int, right: int) -> Fraction:
    dim = 1 << length
    trace_both = 0
    trace_left = 0
    trace_right = 0
    for state in range(dim):
        occ_left = (state >> left) & 1
        occ_right = (state >> right) & 1
        trace_left += occ_left
        trace_right += occ_right
        trace_both += occ_left * occ_right
    return (
        Fraction(trace_both, dim)
        - Fraction(trace_left, 2 * dim)
        - Fraction(trace_right, 2 * dim)
        + Fraction(1, 4)
    )


def _analyse(length: int) -> dict[str, int | Fraction]:
    if type(length) is not int or length % 2 or length < 4:
        raise ValueError("ring length must be even and at least 4")
    dim = 1 << length
    by_bits, staggered_bits = _bit_ring(length)
    hamiltonian, staggered, projectors, currents = _jw_ring(length)
    if by_bits != hamiltonian or staggered_bits != staggered:
        raise RuntimeError("Jordan-Wigner and bit rings disagree")
    if not _symmetric(hamiltonian):
        raise RuntimeError("K4 is not symmetric")
    if sum(staggered) != 0:
        raise RuntimeError("staggered row-sum has nonzero trace")
    _check_projectors(length, hamiltonian, projectors)
    _check_four_point(length)
    _check_edge_square(length, currents)
    gram = _edge_gram_states(length)
    if gram != _edge_gram_matrices(currents):
        raise RuntimeError("state-sum edge traces disagree with the matrices")
    edge = dim // 2
    off_pairs = 0
    off_nonzero = 0
    for left in range(length):
        for right in range(length):
            if _same_two_sites(length, left, right):
                raise RuntimeError("L>=4 identified two bonds with one pair of sites")
            expect = edge if left == right else 0
            if gram[left][right] != expect:
                raise RuntimeError(
                    f"edge trace {(left, right)} is {gram[left][right]}, not {expect}"
                )
            if left != right:
                off_pairs += 1
                if gram[left][right] != 0:
                    off_nonzero += 1
    comm = _commutator(hamiltonian, staggered)
    predicted = _scaled_edge_commutator(currents)
    if comm != predicted:
        _raise_mismatch("scaled commutator", comm, predicted)
    trace_a2, trace_odd_scaled, trace_comm4 = _trace_numbers(staggered, comm)
    # K4 = 4 K_L and A2 = 2 A_L, so [K4, A2] = 8 [K_L, A_L].
    if trace_a2 % 4 or trace_odd_scaled % 16 or trace_comm4 % 64:
        raise RuntimeError("scaled traces are not divisible by the integer weights")
    trace_a = trace_a2 // 4
    trace_odd = trace_odd_scaled // 16
    trace_second = trace_comm4 // 64
    signed = 0
    for left in range(length):
        for right in range(length):
            sign = 1 if (left + right) % 2 == 0 else -1
            signed += sign * gram[left][right]
    if signed != trace_second or trace_second != length * edge:
        raise RuntimeError("signed edge sum disagrees with the commutator trace")
    _check_pair_expansion(length, trace_a2)
    denominator = length * dim
    mass = Fraction(trace_a, denominator)
    moment_1 = Fraction(trace_odd, denominator)
    moment_2 = Fraction(trace_second, denominator)
    if (mass, moment_1, moment_2) != (Fraction(1, 4), Fraction(0), Fraction(1, 2)):
        raise RuntimeError(f"normalized moments are {(mass, moment_1, moment_2)}")
    if Fraction(edge, dim) != Fraction(1, 2):
        raise RuntimeError("one-edge normalized trace is not 1/2")
    return {
        "dimension": dim,
        "trace_denominator": denominator,
        "edge_squared_trace": edge,
        "off_edge_pairs": off_pairs,
        "off_edge_nonzero": off_nonzero,
        "tr_A2": trace_a2,
        "tr_ac": trace_odd_scaled,
        "tr_c4": trace_comm4,
        "tr_A": trace_a,
        "tr_odd": trace_odd,
        "tr_second": trace_second,
        "mass": mass,
        "moment_1": moment_1,
        "moment_2": moment_2,
    }


def _l2_exclusion() -> dict[str, int]:
    _check_four_point(2)
    annihilators = [_annihilator(2, site) for site in range(2)]
    currents = [_current(annihilators, site, 2) for site in range(2)]
    _check_edge_square(2, currents)
    gram = _edge_gram_states(2)
    if gram != _edge_gram_matrices(currents):
        raise RuntimeError("L=2 edge traces disagree")
    if not _same_two_sites(2, 0, 1) or not _same_two_sites(2, 1, 0):
        raise RuntimeError("L=2 did not identify the two bonds")
    off = gram[0][1]
    if off == 0 or gram[1][0] == 0:
        raise RuntimeError("L=2 edges were orthogonal")
    diagonal = gram[0][0] + gram[1][1]
    signed = diagonal - gram[0][1] - gram[1][0]
    if diagonal == signed:
        raise RuntimeError("L=2 diagonal formula reproduced the signed sum")
    if gram[0][0] != 2 or gram[1][1] != 2 or off != -2 or gram[1][0] != -2:
        raise RuntimeError(f"unexpected L=2 gram {gram}")
    if diagonal != 4 or signed != 8:
        raise RuntimeError("unexpected L=2 edge sums")
    return {
        "off": off,
        "diagonal_sum": diagonal,
        "signed_sum": signed,
        "same_two_sites": 1,
        "orthogonality": 0,
    }


def carrier_traces(length: object) -> tuple[int, int, int]:
    """Unscaled Tr(A_L^2), Tr(A_L[K_L, A_L]), Tr([K_L, A_L]^* [K_L, A_L])."""
    if type(length) is not int:
        raise ValueError("length is not an integer")
    if length == 2:
        excluded = _l2_exclusion()
        raise ValueError(
            "refused: L=2 is outside the ring hypothesis; "
            f"Tr(j_0^* j_1)={excluded['off']} is not 0"
        )
    if length % 2 or length < 4:
        raise ValueError("ring length must be even and at least 4")
    data = _analyse(length)
    return (data["tr_A"], data["tr_odd"], data["tr_second"])


def scaled_traces(length: object) -> tuple[int, int, int]:
    """Tr(A2^2), Tr(A2[K4, A2]), Tr([K4, A2]^T [K4, A2]) on the integer ring."""
    if type(length) is not int:
        raise ValueError("length is not an integer")
    if length % 2 or length < 4:
        raise ValueError("ring length must be even and at least 4")
    data = _analyse(length)
    return (data["tr_A2"], data["tr_ac"], data["tr_c4"])


def witness() -> dict[str, int | Fraction]:
    ring4 = _analyse(4)
    ring6 = _analyse(6)
    excluded = _l2_exclusion()
    if (ring4["mass"], ring4["moment_1"], ring4["moment_2"]) != (
        ring6["mass"],
        ring6["moment_1"],
        ring6["moment_2"],
    ):
        raise RuntimeError("normalized moments were not stable under the edge count")
    copies_unscaled = (
        1
        if (ring6["tr_A"], ring6["tr_odd"], ring6["tr_second"])
        == (ring4["tr_A"], ring4["tr_odd"], ring4["tr_second"])
        else 0
    )
    copies_scaled = (
        1
        if (ring6["tr_A2"], ring6["tr_ac"], ring6["tr_c4"])
        == (ring4["tr_A2"], ring4["tr_ac"], ring4["tr_c4"])
        else 0
    )
    if copies_unscaled or copies_scaled:
        raise RuntimeError("L=6 reproduced the labelled integers")
    mass = ring4["mass"]
    moment_2 = ring4["moment_2"]
    if type(mass) is not Fraction or type(moment_2) is not Fraction:
        raise RuntimeError("moments are not exact rationals")
    # theta = 0 makes exp(u theta K_L) the identity, so the Euclidean row-sum is constant.
    samples = (mass, mass, mass)
    circle_second = samples[2] - 2 * samples[1] + samples[0]
    if circle_second != 0 or circle_second == -moment_2:
        raise RuntimeError("theta=0 Euclidean kernel displayed s''(0)")
    result: dict[str, int | Fraction] = {
        "L": 4,
        "dimension": ring4["dimension"],
        "theta": 0,
        "trace_denominator": ring4["trace_denominator"],
        "builders_agree": 1,
        "projector_identity": 1,
        "k_symmetric": 1,
        "commutator_is_edge_sum": 1,
        "four_point_identity": 1,
        "edge_count": 4,
        "edge_squared_trace": ring4["edge_squared_trace"],
        "edge_squared_tau": Fraction(ring4["edge_squared_trace"], ring4["dimension"]),
        "off_edge_pairs": ring4["off_edge_pairs"],
        "off_edge_nonzero": ring4["off_edge_nonzero"],
        "tr_A2_sq": ring4["tr_A2"],
        "tr_A2_comm": ring4["tr_ac"],
        "tr_comm4_sq": ring4["tr_c4"],
        "tr_A_sq": ring4["tr_A"],
        "tr_A_comm": ring4["tr_odd"],
        "tr_comm_sq": ring4["tr_second"],
        "mass": mass,
        "moment_1": ring4["moment_1"],
        "moment_2": moment_2,
        "s0": mass,
        "s1": Fraction(0),
        "s2": -moment_2,
        "euclidean_u0": samples[0],
        "euclidean_u_half": samples[1],
        "euclidean_u1": samples[2],
        "euclidean_circle_second": circle_second,
        "euclidean_displays_s2": 0,
        "L6": 6,
        "L6_dimension": ring6["dimension"],
        "L6_trace_denominator": ring6["trace_denominator"],
        "L6_edge_squared_trace": ring6["edge_squared_trace"],
        "L6_off_edge_pairs": ring6["off_edge_pairs"],
        "L6_off_edge_nonzero": ring6["off_edge_nonzero"],
        "L6_tr_A2_sq": ring6["tr_A2"],
        "L6_tr_A2_comm": ring6["tr_ac"],
        "L6_tr_comm4_sq": ring6["tr_c4"],
        "L6_tr_A_sq": ring6["tr_A"],
        "L6_tr_A_comm": ring6["tr_odd"],
        "L6_tr_comm_sq": ring6["tr_second"],
        "L6_mass": ring6["mass"],
        "L6_moment_1": ring6["moment_1"],
        "L6_moment_2": ring6["moment_2"],
        "L6_copies_unscaled": copies_unscaled,
        "L6_copies_scaled": copies_scaled,
        "L2_same_two_sites": excluded["same_two_sites"],
        "L2_off_edge_trace": excluded["off"],
        "L2_diagonal_sum": excluded["diagonal_sum"],
        "L2_signed_sum": excluded["signed_sum"],
        "L2_orthogonality": excluded["orthogonality"],
        "real_time_density_supplied": 0,
        "spectral_density_supplied": 0,
        "lebesgue_density": 0,
        "theta_positive": 0,
        "volume_limit": 0,
        "trotter_20_12": 0,
        "continuum_limit": 0,
        "gibbs_moments_supplied": 0,
        "closed_real_time_law": 0,
        "higher_dimensional_sum": 0,
        "second_time_index": 0,
    }
    for value in result.values():
        if type(value) is not int and type(value) is not Fraction:
            raise RuntimeError("witness value is not an exact integer or rational")
    if result["spectral_density_supplied"] or result["continuum_limit"] or result["volume_limit"]:
        raise RuntimeError("an excluded claim was marked supplied")
    return result


def refuse_spectral_density() -> None:
    raise ValueError(
        "refused: mu_L is a finite sum of atoms, not a Lebesgue spectral density, "
        "and O.12 does not supply a real-time spectral density"
    )


def refuse_continuum() -> None:
    raise ValueError("refused: a finite model does not establish a continuum limit")


def refuse_volume_limit() -> None:
    raise ValueError(
        "refused: L to infinity is excluded; these moments are not an infinite-volume spectral density"
    )


def refuse_trotter_covariance() -> None:
    raise ValueError(
        "refused: the atomic measure is not the section 20.12 four-site Trotter covariance"
    )


def refuse_positive_theta(theta: object) -> None:
    if type(theta) is int:
        theta = Fraction(theta)
    if type(theta) is not Fraction:
        raise ValueError("theta is not an exact rational")
    if theta > 0:
        raise ValueError(
            "refused: theta>0 replaces the normalized trace by a Gibbs state; "
            "the moments 1/4, 0, 1/2 are not supplied for that state"
        )
    if theta < 0:
        raise ValueError("refused: theta<0 is outside the selected scope")


def refuse_copied_labelled_integers(length: object) -> None:
    if type(length) is not int:
        raise ValueError("length is not an integer")
    if length % 2 or length < 4:
        raise ValueError("ring length must be even and at least 4")
    got = carrier_traces(length)
    scaled = scaled_traces(length)
    labelled = (16, 0, 32)
    labelled_scaled = (64, 0, 2048)
    if length == 4:
        if got != labelled or scaled != labelled_scaled:
            raise RuntimeError("labelled ring traces moved")
        return
    if got == labelled or scaled == labelled_scaled:
        raise RuntimeError("larger ring reproduced the labelled integers")
    raise ValueError(
        "refused: the labelled integers 16, 0, 32 and 64, 0, 2048 stay on L=4; "
        f"L={length} unscaled traces are {got[0]}, {got[1]}, {got[2]}"
    )


def refuse_higher_dimensional_sum(dimension: object, term: object) -> None:
    if type(dimension) is not int:
        raise ValueError("dimension is not an integer")
    if type(term) is int:
        term = Fraction(term)
    if type(term) is not Fraction:
        raise ValueError("term is not an exact rational")
    if dimension != 1:
        raise ValueError("do not copy a 1D constant into a higher-dimensional sum")
    if term != Fraction(1, 4):
        raise ValueError("term is not the equal-time row-sum mass 1/4")


def refuse_closed_real_time() -> None:
    raise ValueError(
        "refused: the Taylor numbers 1/4, 0, -1/2 are not a closed real-time law "
        "and not a spectral density"
    )
