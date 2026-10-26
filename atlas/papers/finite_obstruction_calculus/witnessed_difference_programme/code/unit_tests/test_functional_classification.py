from itertools import product

import pytest
from functional_classification import (
    FunctionalModel,
    FunctionalSignature,
    RetentionSignature,
    UnaryRetentionWitness,
    realize_functional,
    realize_retention,
)


def test_every_retention_signature_has_witness_or_proved_obstruction():
    realized = 0
    for flags in product((False, True), repeat=6):
        signature = RetentionSignature(*flags)
        if signature.realizable():
            model = realize_retention(signature)
            assert model.signature() == signature
            assert len(model.raw) <= 4
            realized += 1
        else:
            with pytest.raises(ValueError):
                realize_retention(signature)
    assert realized == 19


def test_every_functional_signature_has_witness_or_proved_obstruction():
    realized = 0
    for flags in product((False, True), repeat=5):
        signature = FunctionalSignature(*flags)
        if signature.realizable():
            model = realize_functional(signature)
            assert model.signature() == signature
            assert len(model.presentation) <= 3
            realized += 1
        else:
            with pytest.raises(ValueError):
                realize_functional(signature)
    assert realized == 20


def test_small_total_functional_models_satisfy_universal_constraints():
    for n in range(1, 4):
        for q, report, target in product(product(range(2), repeat=n), repeat=3):
            for context in product(range(n), repeat=n):
                model = FunctionalModel(q, report, context, target)
                assert model.signature().realizable()
                factor = model.report_factor()
                if factor is not None:
                    assert tuple(factor[p] for p in q) == report


def test_context_and_calibration_countermodels_match_actual_vocabulary():
    # Presentation changes while the report stays fixed: R2 is report stability.
    model = FunctionalModel((0, 1), (0, 0), (1, 0), (0, 0))
    signature = model.signature()
    assert not signature.presentation_stable and signature.report_stable
    # Comparing report/target remains possible even when calibration fails.
    wrong_target = FunctionalModel((0, 1), (0, 0), (1, 0), (1, 0))
    assert not wrong_target.signature().calibrated
    assert wrong_target.report[0] != wrong_target.target[0]
    # A nonlinked raw report can distinguish a q-blind spot; h(q) cannot.
    blind = FunctionalModel((0, 0), (0, 1), (0, 1), (0, 1))
    assert blind.signature().blind_spot and not blind.signature().linked


def test_noncanonical_partial_and_nonfactorizing_data_fail():
    with pytest.raises(TypeError):
        FunctionalSignature(1, True, True, True, True)
    with pytest.raises(TypeError):
        RetentionSignature(True, True, True, True, True, 1)
    for rows in (((), (), (), ()), ((0,), (), (0,), (0,)), ((0,), (0,), (1,), (0,))):
        with pytest.raises(ValueError):
            FunctionalModel(*rows)
    with pytest.raises(TypeError):
        FunctionalModel((True,), (0,), (0,), (0,))
    with pytest.raises(ValueError):
        UnaryRetentionWitness((0, 0), (0, 1), (0, 1))
    with pytest.raises(ValueError):
        UnaryRetentionWitness((0,), (0,), (1,))
    singleton = UnaryRetentionWitness((0,), (0,), (0,))
    with pytest.raises(ValueError):
        singleton.distinguishable(True, 0)
