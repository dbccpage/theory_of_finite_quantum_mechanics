from itertools import product

import pytest
from witnessed_difference.context_reflection import (
    CongruenceReflection,
    ContextHom,
    ContextSystem,
    identity,
)


def source():
    return ContextSystem((0, 0, 1), ((0,), (2,), (2,)), 1)


def test_universal_comma_factor_for_every_arrow_into_declared_congruent_target():
    system = source()
    reflection = CongruenceReflection(system)
    target = ContextSystem((0, 0, 1), ((0,), (1,), (2,)), 1)
    assert reflection.completed().profiles == (0, 0, 0)
    assert reflection.completed().obstruction() is None
    count = 0
    for values in product(range(3), repeat=3):
        try:
            arrow = ContextHom(system, target, values)
        except ValueError:
            continue
        count += 1
        factor = reflection.factor(arrow)
        assert reflection.unit().then(factor) == arrow
        for other in product(range(3), repeat=3):
            try:
                candidate = ContextHom(reflection.completed(), target, other)
            except ValueError:
                continue
            if reflection.is_factor(arrow, candidate):
                assert candidate == factor
    assert count > 0


def test_noncongruent_source_has_no_reflecting_arrow_into_congruent_small_targets():
    system = source()
    assert system.obstruction() is not None
    assert not CongruenceReflection(system).unit().reflects_profiles()
    for profiles in ((0, 0), (0, 1)):
        for transitions in product(range(2), repeat=2):
            target = ContextSystem(profiles, tuple((x,) for x in transitions), 1)
            if target.obstruction() is not None:
                continue
            for values in product(range(2), repeat=3):
                try:
                    arrow = ContextHom(system, target, values)
                except ValueError:
                    continue
                assert not arrow.reflects_profiles()


def test_category_identity_associativity_and_endpoint_validation():
    system = source()
    target = CongruenceReflection(system).completed()
    unit = CongruenceReflection(system).unit()
    assert identity(system).then(unit) == unit
    assert unit.then(identity(target)) == unit
    assert identity(system).then(unit).then(identity(target)) == identity(system).then(unit.then(identity(target)))
    with pytest.raises(ValueError):
        CongruenceReflection(system).factor(identity(system))
    with pytest.raises(ValueError):
        identity(target).then(identity(system))
    with pytest.raises(ValueError):
        ContextHom(system, target, (0,))
    with pytest.raises(ValueError):
        ContextSystem((0,), ((2,),), 1)
