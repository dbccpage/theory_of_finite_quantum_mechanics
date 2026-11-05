from dataclasses import replace

import pytest
from witnessed_difference.linear_sensing_presentation import (
    LinearSensingPresentation,
    LinearSensingQuotient,
)
from witnessed_difference.semantic_legacy_observers import (
    SourceCustody,
    adapt_linear_sensing,
)


def test_general_sensing_adapter_visible_repairs_and_actual_blindspot():
    s = LinearSensingPresentation(((1, 0),), ((1, 0), (0, 1)), 2)
    adapted = adapt_linear_sensing(s, SourceCustody("ObserverHarness", "a" * 64))
    assert adapted.linear_sensing.report((3, 7)) == (3,)
    assert adapted.linear is None and adapted.memory is None and adapted.policy is None
    with pytest.raises(ValueError, match="sees admissible repairs"):
        s.try_quotient()
    with pytest.raises(ValueError, match="sees admissible repairs"):
        LinearSensingQuotient(s)
    hidden = s.check_repair_blindspot((0, 7))
    assert hidden.is_blindspot and hidden.is_nontrivial
    s.verify_blindspot_witness(hidden)
    assert not s.check_repair_blindspot((3, 0)).is_blindspot
    zero = s.check_repair_blindspot((0, 0))
    assert zero.is_blindspot and not zero.is_nontrivial
    with pytest.raises(ValueError, match="differs from actual maps"):
        s.verify_blindspot_witness(replace(hidden, repair_defect=(0, 8)))


def test_invisible_repairs_strengthen_and_exact_shape_inputs_refuse():
    s = LinearSensingPresentation(((1, -1),), ((1,), (1,)), 1)
    assert s.try_quotient().report((5, 2)) == s.report((5, 2)) == (3,)
    assert s.check_repair_blindspot((4,)).is_blindspot
    with pytest.raises(ValueError, match="shape"):
        s.report((5,))
    with pytest.raises(ValueError, match="shape"):
        LinearSensingPresentation(((1, 0),), ((1,),), 1)
    with pytest.raises(ValueError, match="exact rational"):
        s.report((0.1, 2))
