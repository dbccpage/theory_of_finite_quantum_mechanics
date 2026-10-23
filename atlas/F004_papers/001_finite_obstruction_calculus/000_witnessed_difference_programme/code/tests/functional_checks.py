"""Test adapters to the canonical functional checker; no functional arithmetic."""
from fractions import Fraction
from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import MatrixQuotientCertificate, d0_matrix, verify_matrix_certificate
from witnessed_difference.outcomes import Accepted


def verify_native(vertices, edges, cochain, solution, weights=None):
    weights = {e: Fraction(1) for e in edges} if weights is None else weights
    assert solution.dual_witness is not None
    certificate = MatrixQuotientCertificate(
        d0_matrix(FiniteComplex(vertices, edges)), len(vertices),
        tuple(cochain.get(e, Fraction(0)) for e in edges), tuple(weights[e] for e in edges),
        tuple(solution.potential[v] for v in vertices), tuple(solution.residual[e] for e in edges),
        solution.phi1, tuple(solution.dual_witness[e] for e in edges))
    assert isinstance(verify_matrix_certificate(certificate), Accepted)
