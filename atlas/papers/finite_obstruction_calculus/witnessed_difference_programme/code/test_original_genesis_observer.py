import pytest
from original_genesis_observer import HistoryMemory, WordTransducer, original_classification


def prefix():
    return WordTransducer(((0, 0),), (((0,), (1,)),), 0, (1,), ((),))


def test_universal_product_map_and_replay():
    memory = HistoryMemory(((0, 1), (1, 0)), 0)
    rho = prefix()
    certificate = rho.descent(memory)
    assert certificate[:2] == ("map", (1, 0))
    assert rho.verify(memory, certificate)
    assert memory.run(rho.apply((1,) * 10001)) == 0
    with pytest.raises(ValueError):
        rho.verify(memory, ("map", (0, 0), certificate[2]))


def test_collision_is_actual_history_countermodel():
    memory = HistoryMemory(((0, 1), (0, 1)), 0)
    rho = prefix()
    kind, first, second = rho.descent(memory)
    assert kind == "collision"
    assert memory.run(first) == memory.run(second)
    assert memory.run(rho.apply(first)) != memory.run(rho.apply(second))


def test_final_words_and_invalid_models():
    memory = HistoryMemory(((1,), (0,), (2,)), 0)
    rho = WordTransducer(((0,),), (((0,),),), 0, (), ((0,),))
    assert rho.descent(memory)[1] == (1, 0, None)
    with pytest.raises(ValueError):
        WordTransducer(((0,),), (((1,),),), 0, (), ((),))
    with pytest.raises(ValueError):
        rho.apply((1,))


def test_original_o2_requires_profile_kernel_noncongruence():
    rho = prefix()
    parity = HistoryMemory(((0, 1), (1, 0)), 0)
    assert original_classification(parity, ("a", "b"), {"prefix": rho}) == ("O1Only", None)
    last = HistoryMemory(((0, 1), (0, 1)), 0)
    status, (name, first, second) = original_classification(last, ("a", "b"), {"prefix": rho})
    assert status == "O2" and name == "prefix"
    assert last.run(first) == last.run(second)
    assert last.run(rho.apply(first)) != last.run(rho.apply(second))
    assert original_classification(parity, ("a", "a"), {"prefix": rho}) == ("OutsideO1", None)


def test_original_genesis_observer_container_normalization_and_bool_rejection():
    transitions = [[0, 1], [1, 0]]
    mem = HistoryMemory(transitions, 0)
    transitions[0][1] = 0
    assert mem.transitions == ((0, 1), (1, 0))
    assert mem.run((1,)) == 1

    with pytest.raises(ValueError):
        HistoryMemory(((0, 1), (1, 0)), False)  # type: ignore[arg-type]
