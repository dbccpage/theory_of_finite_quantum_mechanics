"""Exchange rates on a priced causal chain.

The cycle product of successive price ratios is recomputed from the prices
and compared with the direct closing rate.
"""
from fractions import Fraction


class CausalPriceError(Exception):
    """A price was nonpositive or a cycle failed to close."""


def cycle_price_defect() -> Fraction:
    """Return the product of edge rates minus the direct return rate.

    Prices 1, 2/3, 4/5. The path 0→1→2→0 multiplies to 1, and the direct
    ratio p0/p0 is 1. The defect is the difference of those two products.
    """
    prices = (Fraction(1), Fraction(2, 3), Fraction(4, 5))
    for price in prices:
        if price <= 0:
            raise CausalPriceError(f"price {price} is not positive")
    cycle = Fraction(1)
    for index in range(len(prices)):
        nxt = prices[(index + 1) % len(prices)]
        cycle *= nxt / prices[index]
    direct = prices[0] / prices[0]
    defect = cycle - direct
    if defect != 0:
        raise CausalPriceError(f"cycle defect is {defect}")
    return defect
