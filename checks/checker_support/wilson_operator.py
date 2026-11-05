"""Independent four-spin, two-color Wilson fixture on a (2,1,1,1) torus.

Bounded context: exact lattice checking. Matrices have fixed sizes 4 or 16;
the construction is not an arbitrary-dimension Clifford implementation.
A separate fixed 8-by-8 fixture is eliminated for mass/determinant checks.
"""
from fractions import Fraction as Q
from itertools import product
from .domains import integer, rational, sequence
from .gaussian_rational import GaussianRational as G
from .boundary import Violation

Matrix = list[list[G]]
Link = tuple[tuple[G, G], tuple[G, G]]

ZERO, ONE, IMAG = G(0), G(1), G(0,1)
CHIRAL_SIGNS = (1,1,-1,-1)


def _matrix(value: object, size: int) -> Matrix:
    """Admit and snapshot a fixed square Gaussian matrix before any indexing."""
    rows = [sequence(row, "matrix row", size) for row in sequence(value, "matrix", size)]
    return [[_entry(entry) for entry in row] for row in rows]


def _entry(value: object) -> G:
    if not isinstance(value, G) or type(value) is not G:
        raise Violation("input", "Wilson matrix entries must be GaussianRational values")
    return value


def _signs(value: object) -> tuple[int, ...]:
    signs = tuple(integer(sign, "chirality sign", -1, 1)
                  for sign in sequence(value, "chirality signs", 4))
    if 0 in signs:
        raise Violation("input", "chirality signs must be -1 or +1")
    return signs


def gamma_matrices() -> list[Matrix]:
    pauli = (((ZERO,ONE),(ONE,ZERO)), ((ZERO,G(0,-1)),(IMAG,ZERO)),
             ((ONE,ZERO),(ZERO,G(-1))))
    identity = ((ONE,ZERO),(ZERO,ONE))
    matrices = []
    for direction in range(4):
        block = identity if direction == 0 else pauli[direction-1]
        gamma = [[ZERO]*4 for _ in range(4)]
        for a,b in product(range(2),repeat=2):
            gamma[a][b+2] = block[a][b] if direction == 0 else G(0,-1)*block[a][b]
            gamma[a+2][b] = block[a][b] if direction == 0 else IMAG*block[a][b]
        matrices.append(gamma)
    return matrices


def _entry_product(a: Matrix, b: Matrix, row: int, col: int) -> G:
    return sum((a[row][k]*b[k][col] for k in range(4)),ZERO)


def clifford_relations(gamma: object, signs: object = CHIRAL_SIGNS) -> bool:
    matrices = [_matrix(matrix, 4) for matrix in sequence(gamma, "gamma family", 4)]
    chirality = _signs(signs)
    for mu,a,b in product(range(4),repeat=3):
        entry=matrices[mu][a][b]
        if entry != matrices[mu][b][a].conj():
            return False
        if G(chirality[a]*chirality[b])*entry != G(-1)*entry:
            return False
        for nu in range(4):
            anti=_entry_product(matrices[mu],matrices[nu],a,b)+_entry_product(matrices[nu],matrices[mu],a,b)
            if anti != (G(2) if mu==nu and a==b else ZERO):
                return False
    return True


def color_link(direction: int, site: int) -> Link:
    integer(direction, "direction", 0, 3)
    integer(site, "site", 0, 1)
    c,t=(Q(3,5),Q(4,5)) if (direction+site)%2 else (Q(5,13),Q(12,13))
    phase=G(Q(3,5),Q(4,5)) if site else ONE
    return ((G(c)*phase,G(-t)*phase),(G(t)*phase,G(c)*phase))


def spin_color_index(site: int, spin: int, color: int) -> int:
    integer(site, "site", 0, 1)
    integer(spin, "spin", 0, 3)
    integer(color, "color", 0, 1)
    return (site*4+spin)*2+color


def _add_hop(operator: Matrix, gamma: list[Matrix], site: int, spin: int,
             color: int, direction: int, r: Q) -> None:
    target=1-site if direction==0 else site
    forward,reverse=color_link(direction,site),color_link(direction,target)
    row=spin_color_index(site,spin,color)
    for other_spin,other_color in product(range(4),range(2)):
        diagonal=G(-r/2) if spin==other_spin else ZERO
        minus=G(Q(1,2))*gamma[direction][spin][other_spin]+diagonal
        plus=G(Q(-1,2))*gamma[direction][spin][other_spin]+diagonal
        col=spin_color_index(target,other_spin,other_color)
        operator[row][col]=operator[row][col]+minus*forward[color][other_color]+plus*reverse[other_color][color].conj()


def assembled_operator(r: object) -> Matrix:
    r=rational(r,"Wilson parameter")
    gamma=gamma_matrices()
    operator=[[ZERO]*16 for _ in range(16)]
    for site,spin,color in product(range(2),range(4),range(2)):
        row=spin_color_index(site,spin,color)
        operator[row][row]=G(-1+4*r)
        for direction in range(4):
            _add_hop(operator,gamma,site,spin,color,direction,r)
    return operator


def gamma5_hermitian(operator: object, signs: object = CHIRAL_SIGNS) -> bool:
    matrix, chirality = _matrix(operator, 16), _signs(signs)
    for i,j in product(range(16),repeat=2):
        if G(chirality[(i//2)%4]*chirality[(j//2)%4])*matrix[i][j] != matrix[j][i].conj():
            return False
    return True


def assembled_operator_checks() -> bool:
    if not clifford_relations(gamma_matrices()):
        return False
    return all(gamma5_hermitian(assembled_operator(r)) for r in (Q(0),Q(1,2),Q(1),Q(3,2)))


def direct_wilson_determinant(m: object, r: object) -> Q:
    """Eliminate the actual 8x8 matrix; no determinant polynomial is used."""
    m, r = rational(m, "mass"), rational(r, "Wilson parameter")
    s = m + 2*r
    raw: list[list[int | Q]] = [
        [s, 0, -r, 0, -r, 0, 0, 0], [0, s, 0, -r, 0, -r, 0, 0],
        [-r, 0, s, 0, 0, 0, 0, 1], [0, -r, 0, s, 0, 0, 1, 0],
        [-r, 0, 0, 0, s, 0, 0, 1], [0, -r, 0, 0, 0, s, -1, 0],
        [0, 0, 0, -1, 0, 1, s, 0], [0, 0, -1, 0, -1, 0, 0, s],
    ]
    a = [[Q(x) for x in row] for row in raw]
    det = Q(1)
    for col in range(8):
        pivot = next((row for row in range(col, 8) if a[row][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        p = a[col][col]
        det *= p
        for row in range(col + 1, 8):
            q = a[row][col] / p
            for k in range(col + 1, 8):
                a[row][k] -= q * a[col][k]
    return det
