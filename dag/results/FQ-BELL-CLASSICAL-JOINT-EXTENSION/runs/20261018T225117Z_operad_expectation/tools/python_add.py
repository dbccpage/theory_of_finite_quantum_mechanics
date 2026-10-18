

def response_products() -> tuple[tuple[int, int, int, int], ...]:
    """Nullary generator: the ordered product table on the fixed carrier."""
    rows = []
    for mask in range(16):
        a0, a1, b0, b1 = (1 if mask & (1 << j) else -1 for j in range(4))
        rows.append((a0*b0, a0*b1, a1*b0, a1*b1))
    return tuple(rows)


def _exact_vector(values, size):
    if len(values) != size:
        raise ValueError(f"expected {size} exact coordinates")
    if any(type(x) not in (int, Fraction) for x in values):
        raise TypeError("coordinates must be exact integers or Fractions")
    return tuple(Fraction(x) for x in values)


def _joint_weights(weights):
    result = _exact_vector(weights, 16)
    if any(x < 0 for x in result):
        raise ValueError("joint weights must be nonnegative")
    if sum(result, Fraction(0)) != 1:
        raise ValueError("joint weights must sum to one")
    return result


def joint_expectation(weights, responses) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Binary generator (JointLaw, ResponseMap4) -> Q^4, using one law.

    The response table may be arbitrary exact rational four-vectors. The CHSH
    bound requires the specific response_products table, not an arbitrary table.
    """
    probabilities = _joint_weights(weights)
    if len(responses) != 16:
        raise ValueError("the response map must have exactly 16 rows")
    table = tuple(_exact_vector(row, 4) for row in responses)
    return tuple(sum((p * row[j] for p, row in zip(probabilities, table)), Fraction(0)) for j in range(4))


def chsh_linear(correlators) -> Fraction:
    """Unary generator on Q^4; a scalar value alone is not a Bell certificate."""
    a, b, c, d = _exact_vector(correlators, 4)
    return a + b + c - d


def verify_joint_certificate(weights, certificate: JointBellCertificate) -> None:
    """Reject a false certificate by recomputing every component independently.

    Does not call certify_joint_law or accept its verdict. This direct-product
    route is distinct from the producer's factored score partition.
    """
    probabilities = _joint_weights(weights)
    if type(certificate) is not JointBellCertificate:
        raise TypeError("expected a JointBellCertificate")
    fields = (certificate.chsh, certificate.positive_score_mass, certificate.negative_score_mass,
              certificate.lower_slack, certificate.upper_slack)
    _exact_vector(certificate.correlators, 4)
    _exact_vector(fields, 5)
    products = response_products()
    e = tuple(sum((probabilities[m] * products[m][j] for m in range(16)), Fraction(0)) for j in range(4))
    scores = tuple(row[0] + row[1] + row[2] - row[3] for row in products)
    plus = sum((p for p, s in zip(probabilities, scores) if s == 2), Fraction(0))
    minus = sum((p for p, s in zip(probabilities, scores) if s == -2), Fraction(0))
    s = e[0] + e[1] + e[2] - e[3]
    if certificate != JointBellCertificate(e, s, plus, minus, 2+s, 2-s):
        raise ValueError("certificate does not match the supplied joint law")
