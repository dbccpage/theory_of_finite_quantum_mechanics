from dataclasses import replace

import pytest
from witnessed_difference.observer import RetentionPacket
from witnessed_difference.semantic_legacy_observers import Memory


def packet():
    return RetentionPacket(("m0", "m1", "m2"), ("keep",),
                           (("m0", "keep", "m0"), ("m1", "keep", "m1"), ("m2", "keep", "m2")),
                           (("m0", "r0"), ("m1", "r1"), ("m2", "r2")),
                           (("r1", "r0"), ("r2", "r1"), ("r0", "r2")))


def test_reaccess_preserves_declared_directed_irreflexive_nontransitive_predicate():
    p = packet()
    m = Memory(p, ("m1", "m2", "m0"), ("r0", "r1", "r2"))
    assert tuple(m.reaccess(i) for i in range(3)) == ("r1", "r2", "r0")
    assert m.packet.comparison == p.comparison
    with pytest.raises(ValueError, match="declared comparison"):
        Memory(replace(p, comparison=tuple((b, a) for a, b in p.comparison)),
               ("m1", "m2", "m0"), ("r0", "r1", "r2"))
    with pytest.raises(ValueError, match="declared comparison"):
        Memory(replace(p, comparison=()), ("m0", "m1", "m2"), ("r0", "r1", "r2"))
