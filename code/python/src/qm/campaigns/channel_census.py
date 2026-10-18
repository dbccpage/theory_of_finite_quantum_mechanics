"""Census of classical channels by exact column sums.

Origin: code/python/src/qm/campaigns/channel_census.py
Claim: a channel is trace-preserving exactly when every column sums to 1 over Q.
AuthorityEffect: None. This census is classical, not a CPTP classification.
"""
from fractions import Fraction


class ChannelCensusError(Exception):
    """A channel matrix was not square or not rational."""


def column_sums(matrix) -> list:
    if not matrix or any(len(row) != len(matrix) for row in matrix):
        raise ChannelCensusError("a classical channel must be square")
    totals = []
    for col in range(len(matrix)):
        total = Fraction(0)
        for row in matrix:
            total += Fraction(row[col])
        totals.append(total)
    return totals


def trace_preserving_count(channels) -> int:
    """How many channels have every column sum equal to 1."""
    count = 0
    for channel in channels:
        if all(total == 1 for total in column_sums(channel)):
            count += 1
    return count


def qubit_channel_census() -> int:
    identity = ((1, 0), (0, 1))
    depolarizing = ((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 2), Fraction(1, 2)))
    leaking = ((Fraction(1, 2), 0), (0, Fraction(1, 2)))
    return trace_preserving_count((identity, depolarizing, leaking))
