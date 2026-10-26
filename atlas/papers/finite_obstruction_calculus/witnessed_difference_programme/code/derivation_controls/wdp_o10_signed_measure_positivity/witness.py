"""Unreduced signed charges on one L=4, M=1 all-horizontal SQL breakup.

Four plaquettes, two time-slice 4-cycles, four orientations. The opposite
staggered masks are negative, so this charging is not a positive measure
and not a probability measure. Not a continuum limit.
"""

from __future__ import annotations

from fractions import Fraction

_L = 4
_M = 1
_Q_ALGEBRAIC = Fraction(3)
_Q_DISK = Fraction(193, 192)
_DISK_DENOMINATOR = 21743271936
_L2_HOP_SIGN = 1


def _exact_rational(value: object, name: str) -> Fraction:
    if type(value) is bool or type(value) not in (int, Fraction):
        raise ValueError(f"{name} is not an exact rational")
    if type(value) is int:
        return Fraction(value)
    return value


def _plaquettes(sites: int, times: int) -> list[dict[str, int]]:
    found: list[dict[str, int]] = []
    for time in range(times):
        for site in range(time % 2, sites, 2):
            other = (site + 1) % sites
            nxt = (time + 1) % times
            found.append(
                {
                    "pid": len(found),
                    "time": time,
                    "x": site,
                    "y": other,
                    "a": time * sites + site,
                    "b": time * sites + other,
                    "c": nxt * sites + site,
                    "d": nxt * sites + other,
                }
            )
    return found


def _open_popcount(state: int, source: int, target: int) -> int:
    # Strictly between the bond endpoints, in the before-layer occupation.
    lo = source if source < target else target
    hi = target if source < target else source
    width = hi - lo - 1
    if width < 0:
        raise RuntimeError("bond endpoints are not a pair of sites")
    return ((state >> (lo + 1)) & ((1 << width) - 1)).bit_count()


def _same_time_edges(
    plaquettes: list[dict[str, int]], mask: int, sites: int
) -> list[frozenset[int]]:
    edges: list[frozenset[int]] = []
    for plaquette in plaquettes:
        bit = (mask >> plaquette["pid"]) & 1
        if bit:
            pairs = ((plaquette["a"], plaquette["b"]), (plaquette["d"], plaquette["c"]))
        else:
            pairs = ((plaquette["a"], plaquette["c"]), (plaquette["d"], plaquette["b"]))
        for left, right in pairs:
            if (left // sites) != (right // sites):
                raise RuntimeError("horizontal breakup inserted a time-like edge")
            edges.append(frozenset((left, right)))
    return edges


def _cycles(sites: int, times: int, edges: list[frozenset[int]]) -> list[list[int]]:
    nodes = [time * sites + site for time in range(times) for site in range(sites)]
    adjacent: dict[int, list[int]] = {node: [] for node in nodes}
    for edge in edges:
        left, right = tuple(edge)
        adjacent[left].append(right)
        adjacent[right].append(left)
    seen: set[int] = set()
    components: list[list[int]] = []
    for start in nodes:
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component: list[int] = []
        while stack:
            node = stack.pop()
            component.append(node)
            for nxt in adjacent[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        components.append(component)
    components.sort(key=min)
    for component in components:
        times_seen = {node // sites for node in component}
        if len(component) != sites or times_seen != {min(component) // sites}:
            raise RuntimeError("horizontal graph is not two time-slice cycles")
        if any(len(adjacent[node]) != 2 for node in component):
            raise RuntimeError("a time slice is not a 2-regular cycle")
    return components


def _states(
    mask: int,
    cluster_of: dict[tuple[int, int], int],
    sites: int,
    times: int,
) -> list[int]:
    states: list[int] = []
    for time in range(times):
        state = 0
        for site in range(sites):
            cluster = cluster_of[(time, site)]
            bit = (1 - (site % 2) + ((mask >> cluster) & 1)) % 2
            state |= bit << site
        states.append(state)
    return states


def _configuration_sign(
    states: list[int], plaquettes: list[dict[str, int]], times: int
) -> int:
    total = 0
    for time in range(times):
        before = states[time]
        after = states[(time + 1) % times]
        for plaquette in plaquettes:
            if plaquette["time"] != time:
                continue
            changed = ((before >> plaquette["x"]) & 1) != ((after >> plaquette["x"]) & 1)
            if changed:
                total += _open_popcount(before, plaquette["x"], plaquette["y"])
    return 1 if total % 2 == 0 else -1


def _graph_weight(q: Fraction, plaquettes: int, mask: int) -> Fraction:
    vertical = Fraction(1)
    horizontal = (q - 1) / 2
    if horizontal <= 0 or vertical != 1:
        raise RuntimeError("breakup weights are not the stated positive rationals")
    weight = Fraction(1)
    for pid in range(plaquettes):
        bit = (mask >> pid) & 1
        weight *= horizontal if bit else vertical
    if type(weight) is not Fraction or weight <= 0:
        raise RuntimeError("graph weight is not a positive rational")
    return weight


def signed_breakup(
    sites: object = _L,
    repetitions: object = _M,
    q: object = _Q_ALGEBRAIC,
) -> dict[str, int | Fraction]:
    """Charges of the all-horizontal breakup at one selected rational q."""

    if type(sites) is not int or type(repetitions) is not int:
        raise ValueError("sites and repetitions must be exact integers")
    if sites != _L or repetitions != _M:
        raise ValueError("refused: carrier is outside L=4, M=1")
    coupling = _exact_rational(q, "q")
    if coupling != _Q_ALGEBRAIC and coupling != _Q_DISK:
        raise ValueError("refused: q is outside the two selected points")
    times = 2 * repetitions
    plaquettes = _plaquettes(sites, times)
    if len(plaquettes) != sites * repetitions:
        raise RuntimeError("plaquette count is not LM")
    expected = [
        (0, 0, 0, 1, 0, 1, 4, 5),
        (1, 0, 2, 3, 2, 3, 6, 7),
        (2, 1, 1, 2, 5, 6, 1, 2),
        (3, 1, 3, 0, 7, 4, 3, 0),
    ]
    found = [
        (
            row["pid"],
            row["time"],
            row["x"],
            row["y"],
            row["a"],
            row["b"],
            row["c"],
            row["d"],
        )
        for row in plaquettes
    ]
    if found != expected:
        raise RuntimeError("checkerboard corners are not the L=4, M=1 table")
    gid = (1 << len(plaquettes)) - 1
    edges = _same_time_edges(plaquettes, gid, sites)
    if len(edges) != 8 or len(set(edges)) != 8:
        raise RuntimeError("all-horizontal edge set is not eight distinct bonds")
    components = _cycles(sites, times, edges)
    if len(components) != 2:
        raise RuntimeError("all-horizontal graph does not have two cycles")
    cluster_of: dict[tuple[int, int], int] = {}
    for cluster, component in enumerate(components):
        for node in component:
            cluster_of[divmod(node, sites)] = cluster
    for site in range(sites):
        if cluster_of[(0, site)] != 0 or cluster_of[(1, site)] != 1:
            raise RuntimeError("cluster labels are not the time-slice order")
    weight = _graph_weight(coupling, len(plaquettes), gid)
    clusters = len(components)
    signs: dict[int, int] = {}
    charges: dict[int, Fraction] = {}
    for mask in range(1 << clusters):
        states = _states(mask, cluster_of, sites, times)
        sign = _configuration_sign(states, plaquettes, times)
        signs[mask] = sign
        charges[mask] = sign * weight
        if mask in (1, 2):
            if _open_popcount(states[1], 3, 0) != 1:
                raise RuntimeError("wrap Jordan-Wigner popcount is not 1")
            for source, target in ((0, 1), (2, 3), (1, 2)):
                if _open_popcount(states[1], source, target) != 0:
                    raise RuntimeError("an adjacent bond did not have an empty interval")
    if signs != {0: 1, 1: -1, 2: -1, 3: 1}:
        raise RuntimeError("Jordan-Wigner signs do not match the staggered masks")
    merons = sum(1 for cluster in range(clusters) if signs[1 << cluster] == -1)
    if merons != 2:
        raise RuntimeError("meron count is not 2")
    reduced = weight * (1 << clusters) if merons == 0 else Fraction(0)
    if reduced != 0:
        raise RuntimeError("this graph is not outside the zero-meron clause")
    total = sum((charges[mask] for mask in charges), Fraction(0))
    if charges[1] != charges[2] or charges[0] != charges[3]:
        raise RuntimeError("paired orientation charges are not equal")
    if charges[1] >= 0 or charges[0] <= 0 or total != 0:
        raise RuntimeError("unreduced charges are not two negative atoms and sum 0")
    positive = all(charge >= 0 for charge in charges.values())
    return {
        "q": coupling,
        "horizontal": (coupling - 1) / 2,
        "weight": weight,
        "opposite_charge": charges[1],
        "equal_charge": charges[0],
        "orientation_sum": total,
        "reduced_weight": reduced,
        "is_positive_measure": 1 if positive else 0,
        "is_probability_measure": 1 if positive and total == 1 else 0,
        "gid": gid,
        "merons": merons,
    }


def witness() -> dict[str, int | Fraction]:
    algebraic = signed_breakup(q=_Q_ALGEBRAIC)
    disk = signed_breakup(q=_Q_DISK)
    if algebraic["horizontal"] != 1 or algebraic["weight"] != 1:
        raise RuntimeError("q=3 horizontal weight is not 1")
    if disk["horizontal"] != Fraction(1, 384) or disk["q"] != 1 + Fraction(1, 192):
        raise RuntimeError("q=193/192 is not the in-disk endpoint")
    if disk["weight"] != Fraction(1, 384) ** 4:
        raise RuntimeError("disk graph weight is not ((q-1)/2)^4")
    if disk["weight"].denominator != (1 << 28) * 3**4:
        raise RuntimeError("disk denominator is not 2^28*3^4")
    if (1 << 28) * 3**4 != _DISK_DENOMINATOR or 384**4 != _DISK_DENOMINATOR:
        raise RuntimeError("recorded denominator 21743271936 was not reproduced")
    if algebraic["opposite_charge"] != -1:
        raise RuntimeError("q=3 opposite-mask charge is not -1")
    if disk["opposite_charge"] != Fraction(-1, _DISK_DENOMINATOR):
        raise RuntimeError("disk opposite-mask charge is not -1/21743271936")
    if algebraic["is_positive_measure"] != 0 or disk["is_positive_measure"] != 0:
        raise RuntimeError("negative atoms were reported as a positive measure")
    if algebraic["is_probability_measure"] != 0 or disk["is_probability_measure"] != 0:
        raise RuntimeError("the charging was reported as a probability measure")
    if algebraic["merons"] != 2 or disk["merons"] != 2:
        raise RuntimeError("meron count left the selected graph")
    return {
        "L": _L,
        "M": _M,
        "times": 2,
        "LM": _L * _M,
        "plaquettes": 4,
        "fock": 1 << _L,
        "graphs_enumerated": 1,
        "gid": algebraic["gid"],
        "cycles": 2,
        "cycle_length": 4,
        "orientations": 4,
        "mask_lo": 1,
        "mask_hi": 2,
        "q_algebraic": _Q_ALGEBRAIC,
        "q_disk": _Q_DISK,
        "horizontal_q3": algebraic["horizontal"],
        "horizontal_disk": disk["horizontal"],
        "vertical": Fraction(1),
        "weight_q3": algebraic["weight"],
        "weight_disk": disk["weight"],
        "opposite_charge_q3": algebraic["opposite_charge"],
        "opposite_charge_disk": disk["opposite_charge"],
        "equal_charge_q3": algebraic["equal_charge"],
        "equal_charge_disk": disk["equal_charge"],
        "negative_atom_count": 2,
        "orientation_sum_q3": algebraic["orientation_sum"],
        "orientation_sum_disk": disk["orientation_sum"],
        "merons": algebraic["merons"],
        "reduced_weight_q3": algebraic["reduced_weight"],
        "reduced_weight_disk": disk["reduced_weight"],
        "is_positive_measure": 0,
        "is_probability_measure": 0,
        "atoms_deleted": 0,
        "fock_summed": 0,
        "continuum_limit": 0,
    }


def refuse_positive_measure() -> None:
    """The opposite-mask atoms stay negative after orbit cancellation."""

    row = witness()
    if row["opposite_charge_q3"] >= 0 or row["opposite_charge_disk"] >= 0:
        raise RuntimeError("negative atoms were not reproduced")
    if row["is_positive_measure"] != 0 or row["is_probability_measure"] != 0:
        raise RuntimeError("positivity flags do not match the negative atoms")
    raise ValueError(
        "refused: the opposite-mask charges are negative, so the unreduced "
        "charging is not a positive measure and not a probability measure"
    )


def refuse_l2() -> None:
    raise ValueError(
        "refused: the constructor rejects sites below 4; the L=2 empty-interval "
        "hop sign is not this atom"
    )


def refuse_m2_partition(partition: object) -> None:
    if partition == 912:
        raise ValueError(
            "refused: the M=2 partition 912 is a different time count and is not this charge"
        )
    raise ValueError("refused: a partition outside the selected L=4, M=1 breakup")


def refuse_gibbs() -> None:
    raise ValueError(
        "refused: the Gibbs covariance is not positivity of the finite signed SQL histories"
    )


def refuse_zero_meron() -> None:
    raise ValueError(
        "refused: meron count is 2; the zero-meron reduction does not delete the negative atoms"
    )


def refuse_continuum() -> None:
    raise ValueError("refused: a finite model does not establish a continuum limit")


def refuse_higher_dimensional_sum(dimension: object, term: object) -> None:
    """The L=2 empty-interval hop sign is not the L=4 wrap contribution."""

    if type(dimension) is not int:
        raise ValueError("dimension is not an integer")
    if type(term) is bool or type(term) not in (int, Fraction):
        raise ValueError("term is not an exact rational")
    if type(term) is int:
        term = Fraction(term)
    if dimension != 1:
        raise ValueError("do not copy a 1D constant into a higher-dimensional sum")
    if term != Fraction(_L2_HOP_SIGN):
        raise ValueError("term is not the empty-interval hop sign")
