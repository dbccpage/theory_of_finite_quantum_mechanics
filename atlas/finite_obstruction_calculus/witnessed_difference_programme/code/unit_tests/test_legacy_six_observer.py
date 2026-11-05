from fractions import Fraction as Q

import pytest
from witnessed_difference.legacy_six_observer import SixObserver
from witnessed_difference.obstruction import MatrixQuotientCertificate
from witnessed_difference.semantic_legacy_observers import SourceCustody


def cert(x):
    return MatrixQuotientCertificate(((Q(0),),), 1, (Q(x),), (Q(1),), (Q(0),),
                                    (Q(x),), Q(abs(x)), (Q((x > 0)-(x < 0)),))


def build(relation, pairs):
    return SixObserver(SourceCustody("known-education-source.md", "a"*64), ("edge",), ("x", "y"),
                       (cert(0), cert(1)), pairs, relation, ("zero", "positive"), (0, 1))


def test_actual_six_fields_and_missing_comparison_countermodels():
    pairs = ((cert(0), cert(-1)), (cert(1), cert(0)))
    observer = build(((True, False), (False, True)), pairs)
    assert observer.terminal(1) == "positive"
    with pytest.raises(ValueError):
        build(((True, True), (True, True)), pairs)
    with pytest.raises(ValueError):
        build(((True, False), (False, True)), ((cert(0), cert(0)), (cert(1), cert(0))))
    with pytest.raises(ValueError):
        build(((True,),), pairs)
