"""CH04 checked contextual category and relation-coarsening reflector.

Objects: finite nonempty carriers with profile equality and total context
operations. Arrows preserve equality and commute with every context. The
completion is initial in S down-arrow Cong; it can merge report profiles.
It is not a profile-reflecting constructor refinement. AuthorityEffect: None.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ContextSystem:
    profiles: tuple[int, ...]
    transitions: tuple[tuple[int, ...], ...]
    contexts: int

    def __post_init__(self):
        object.__setattr__(self, "profiles", tuple(self.profiles))
        object.__setattr__(self, "transitions", tuple(tuple(row) for row in self.transitions))
        n = len(self.profiles)
        if not n or type(self.contexts) is not int or self.contexts < 0:
            raise ValueError("invalid finite carrier or context count")
        if any(type(value) is not int for value in self.profiles):
            raise TypeError("profile identifiers must be integers")
        if len(self.transitions) != n or any(len(row) != self.contexts for row in self.transitions):
            raise ValueError("transition shape mismatch")
        if any(type(value) is not int or not 0 <= value < n for row in self.transitions for value in row):
            raise ValueError("transition leaves carrier")

    def related(self, x, y):
        return self.profiles[x] == self.profiles[y]

    def obstruction(self):
        for x in range(len(self.profiles)):
            for y in range(x):
                for c in range(self.contexts):
                    if self.related(x, y) and not self.related(self.transitions[x][c], self.transitions[y][c]):
                        return (x, y, c)
        return None


@dataclass(frozen=True)
class ContextHom:
    source: ContextSystem
    target: ContextSystem
    mapping: tuple[int, ...]

    def __post_init__(self):
        object.__setattr__(self, "mapping", tuple(self.mapping))
        if self.source.contexts != self.target.contexts:
            raise ValueError("context vocabularies differ")
        if len(self.mapping) != len(self.source.profiles) or any(
            type(value) is not int or not 0 <= value < len(self.target.profiles) for value in self.mapping
        ):
            raise ValueError("map is not a total carrier map")
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping)):
                if self.source.related(x, y) and not self.target.related(self.mapping[x], self.mapping[y]):
                    raise ValueError("map does not preserve profiles")
            for c in range(self.source.contexts):
                if self.mapping[self.source.transitions[x][c]] != self.target.transitions[self.mapping[x]][c]:
                    raise ValueError("map does not commute with contexts")

    def then(self, other):
        if self.target != other.source:
            raise ValueError("composition endpoints differ")
        return ContextHom(self.source, other.target, tuple(other.mapping[x] for x in self.mapping))

    def reflects_profiles(self):
        return all(not self.target.related(self.mapping[x], self.mapping[y]) or self.source.related(x, y)
                   for x in range(len(self.mapping)) for y in range(len(self.mapping)))


def identity(system):
    return ContextHom(system, system, tuple(range(len(system.profiles))))


def _canonicalize(labels):
    representatives = {}
    return tuple(representatives.setdefault(label, len(representatives)) for label in labels)


@dataclass(frozen=True)
class CongruenceReflection:
    source: ContextSystem

    def completed(self):
        labels = _canonicalize(self.source.profiles)
        while True:
            updated = list(labels)
            for x in range(len(labels)):
                for y in range(x):
                    if labels[x] == labels[y]:
                        for c in range(self.source.contexts):
                            a, b = self.source.transitions[x][c], self.source.transitions[y][c]
                            old, new = updated[b], updated[a]
                            updated = [new if value == old else value for value in updated]
            updated = _canonicalize(updated)
            if updated == labels:
                return ContextSystem(labels, self.source.transitions, self.source.contexts)
            labels = updated

    def unit(self):
        return ContextHom(self.source, self.completed(), tuple(range(len(self.source.profiles))))

    def factor(self, arrow):
        if arrow.source != self.source or arrow.target.obstruction() is not None:
            raise ValueError("arrow is not an object of S down-arrow Cong")
        return ContextHom(self.completed(), arrow.target, arrow.mapping)

    def is_factor(self, arrow, candidate):
        return (arrow.source == self.source and arrow.target.obstruction() is None
                and candidate.source == self.completed() and candidate.target == arrow.target
                and candidate.mapping == arrow.mapping)
