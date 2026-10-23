"""Fixed exact source fixtures; no spectral/optimization algorithm. AuthorityEffect: None."""
from fractions import Fraction
from .obstruction import MatrixQuotientCertificate, verify_matrix_certificate


def incompatible_reference_fixture():
    """Two declared reset comparisons sharing one source vertex."""
    ket0 = (Fraction(1), Fraction(0))
    ket1 = (Fraction(0), Fraction(1))
    # Every input state is ket0; the comparisons discard it and return their constants.
    defects = (tuple(a - b for a, b in zip(ket0, ket0)),
               tuple(a - b for a, b in zip(ket1, ket0)))
    z = (Fraction(-1), Fraction(1))
    dual = (tuple(-a / 2 for a in z), tuple(a / 2 for a in z))
    # Every shared traceless repair pairs to zero: phi0+phi1=0 as operators.
    assert tuple(a + b for a, b in zip(*dual)) == (Fraction(0), Fraction(0))
    # Propose the fixed value 1; the owner checks both bounds on the diagonal
    # traceless shared-repair subspace. No trace-norm arithmetic is repeated here.
    delta = tuple(a for edge in defects for a in edge)
    cert = MatrixQuotientCertificate(
        ((Fraction(1),), (Fraction(-1),), (Fraction(1),), (Fraction(-1),)),
        1, delta, (Fraction(1, 2),) * 4, (Fraction(0),), delta,
        Fraction(1), tuple(a for edge in dual for a in edge))
    upper = verify_matrix_certificate(cert).unwrap().value
    assert ket0 != ket1  # A compatible reference at the shared vertex is impossible.
    return defects, dual, upper


def missing_hypothesis_countermodels():
    """Explicit values for the repair-transport and score-protection nonimplications."""
    # Identity channel, but source repairs everything and target permits no repair.
    source_quotient_distance = Fraction(0)
    target_quotient_distance = Fraction(1)
    before = (Fraction(2), Fraction(0))
    after = (Fraction(0), Fraction(1))
    assert sum(after) < sum(before) and after[1] > before[1]
    return source_quotient_distance, target_quotient_distance, before, after
