"""Source observer-world five on an explicitly closed finite history restriction."""

from dataclasses import dataclass, fields

from .context_reflection import ContextSystem


@dataclass(frozen=True)
class FiniteObserverWorld:
    alphabet: tuple[str, ...]
    histories: tuple[tuple[int, ...], ...]
    profiles: tuple[str, ...]
    presented_profiles: tuple[int, ...]
    contexts: tuple[str, ...]
    context_actions: tuple[tuple[int, ...], ...]
    witnesses: tuple[tuple[int, int, int], ...]
    grammar: tuple[str, ...]
    grammar_interpretation: tuple[frozenset[int], ...] | None = None

    def __post_init__(self):
        for name in ("alphabet", "profiles", "contexts", "grammar"):
            labels = tuple(getattr(self, name))
            if any(type(label) is not str or not label for label in labels) or len(set(labels)) != len(labels):
                raise ValueError("invalid finite world labels")
            object.__setattr__(self, name, labels)
        for name in ("histories", "context_actions", "witnesses"):
            object.__setattr__(self, name, tuple(tuple(row) for row in getattr(self, name)))
        object.__setattr__(self, "presented_profiles", tuple(self.presented_profiles))
        n = len(self.histories)
        if not n or len(set(self.histories)) != n or any(
            type(d) is not int or not 0 <= d < len(self.alphabet) for h in self.histories for d in h
        ):
            raise ValueError("invalid history carrier")
        if len(self.presented_profiles) != n or any(
            type(p) is not int or not 0 <= p < len(self.profiles) for p in self.presented_profiles
        ) or set(self.presented_profiles) != set(range(len(self.profiles))):
            raise ValueError("declared profile carrier must be the actual image")
        if len(self.context_actions) != len(self.contexts) or any(
            len(row) != n or any(type(h) is not int or not 0 <= h < n for h in row)
            for row in self.context_actions
        ):
            raise ValueError("context must be total and closed on the declared histories")
        for witness in self.witnesses:
            if len(witness) != 3 or any(type(v) is not int for v in witness):
                raise ValueError("invalid witness tuple")
            x, y, c = witness
            if not 0 <= x < n or not 0 <= y < n or not 0 <= c < len(self.contexts):
                raise ValueError("witness leaves its declared carrier")
            action = self.context_actions[c]
            if self.presented_profiles[x] != self.presented_profiles[y] or (
                self.presented_profiles[action[x]] == self.presented_profiles[action[y]]
            ):
                raise ValueError("declared context witness does not replay")
        if self.grammar_interpretation is not None:
            interpretation = tuple(frozenset(subset) for subset in self.grammar_interpretation)
            if len(interpretation) != len(self.grammar) or any(
                type(p) is not int or not 0 <= p < len(self.profiles) for subset in interpretation for p in subset
            ):
                raise ValueError("invalid grammar interpretation")
            object.__setattr__(self, "grammar_interpretation", interpretation)

    def context_system(self):
        return ContextSystem(self.presented_profiles,
                             tuple(tuple(action[h] for action in self.context_actions)
                                   for h in range(len(self.histories))), len(self.contexts))

    def facts(self):
        if self.grammar_interpretation is None:
            raise ValueError("grammar names do not supply an expressibility interpretation")
        return frozenset(subset for subset in self.grammar_interpretation if all(
            self.presented_profiles[h] not in subset or self.presented_profiles[action[h]] in subset
            for action in self.context_actions for h in range(len(self.histories))
        ))

    def verify_against(self, source):
        if type(source) is not FiniteObserverWorld or type(self) is not FiniteObserverWorld:
            raise ValueError("world receipt is not bound to this source packet")
        # Both received objects may have arrived through an untrusted decoder;
        # equality of malformed payloads is not a replay of the domain predicate.
        actual = FiniteObserverWorld(**{f.name: getattr(source, f.name) for f in fields(FiniteObserverWorld)})
        proposed = FiniteObserverWorld(**{f.name: getattr(self, f.name) for f in fields(FiniteObserverWorld)})
        if proposed != actual:
            raise ValueError("world receipt is not bound to this source packet")
        return True
