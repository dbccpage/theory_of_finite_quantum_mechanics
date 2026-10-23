"""Exact finite realization of original WD2 history contexts, over every finite word.

A transducer is a declared subclass of arbitrary rho, not an inference about rho.
The finite product graph certifies global descent; no length bound is used.
"""
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class HistoryMemory:
    transitions: tuple[tuple[int, ...], ...]
    initial: int

    def __post_init__(self):
        if type(self.transitions) is not tuple:
            object.__setattr__(
                self, "transitions", tuple(tuple(x) for x in self.transitions)
            )
        else:
            object.__setattr__(
                self,
                "transitions",
                tuple(tuple(x) if type(x) is not tuple else x for x in self.transitions),
            )
        if type(self.initial) is not int or isinstance(self.initial, bool):
            raise ValueError("invalid memory")
        n = len(self.transitions)
        if not n or not 0 <= self.initial < n:
            raise ValueError("invalid memory")
        k = len(self.transitions[0])
        if any(
            len(row) != k
            or any(type(x) is not int or isinstance(x, bool) or not 0 <= x < n for x in row)
            for row in self.transitions
        ):
            raise ValueError("invalid total update")

    def run(self, word, start=None):
        state = self.initial if start is None else start
        if type(state) is not int or isinstance(state, bool) or not 0 <= state < len(self.transitions):
            raise ValueError("invalid initial state")
        for symbol in word:
            if type(symbol) is not int or isinstance(symbol, bool) or not 0 <= symbol < len(self.transitions[0]):
                raise ValueError("invalid word")
            state = self.transitions[state][symbol]
        return state


@dataclass(frozen=True)
class WordTransducer:
    transitions: tuple[tuple[int, ...], ...]
    outputs: tuple[tuple[tuple[int, ...], ...], ...]
    initial: int
    prefix: tuple[int, ...]
    finals: tuple[tuple[int, ...], ...]

    def __post_init__(self):
        object.__setattr__(
            self,
            "transitions",
            tuple(tuple(x) if type(x) is not tuple else x for x in self.transitions),
        )
        object.__setattr__(
            self,
            "outputs",
            tuple(
                tuple(tuple(w) if type(w) is not tuple else w for w in row)
                for row in self.outputs
            ),
        )
        object.__setattr__(self, "prefix", tuple(self.prefix))
        object.__setattr__(
            self,
            "finals",
            tuple(tuple(w) if type(w) is not tuple else w for w in self.finals),
        )
        HistoryMemory(self.transitions, self.initial)
        n, k = len(self.transitions), len(self.transitions[0])
        if len(self.outputs) != n or len(self.finals) != n or any(len(row) != k for row in self.outputs):
            raise ValueError("invalid output shape")
        words = [self.prefix, *self.finals, *(word for row in self.outputs for word in row)]
        if any(type(d) is not int or isinstance(d, bool) or not 0 <= d < k for word in words for d in word):
            raise ValueError("invalid output word")

    def apply(self, word):
        state, output = self.initial, list(self.prefix)
        for d in word:
            if type(d) is not int or not 0 <= d < len(self.transitions[0]):
                raise ValueError("invalid input word")
            output.extend(self.outputs[state][d])
            state = self.transitions[state][d]
        return tuple(output) + self.finals[state]

    def descent(self, memory):
        if len(memory.transitions[0]) != len(self.transitions[0]):
            raise ValueError("alphabet mismatch")
        first = (memory.initial, self.initial, memory.run(self.prefix))
        witnesses, queue, images = {first: ()}, deque([first]), {}
        while queue:
            source, control, output = vertex = queue.popleft()
            image = memory.run(self.finals[control], output)
            word = witnesses[vertex]
            if source in images and images[source][0] != image:
                return ("collision", images[source][1], word)
            images[source] = (image, word)
            for d in range(len(self.transitions[0])):
                next_vertex = (memory.transitions[source][d], self.transitions[control][d], memory.run(self.outputs[control][d], output))
                if next_vertex not in witnesses:
                    witnesses[next_vertex] = word + (d,)
                    queue.append(next_vertex)
        return ("map", tuple(images[x][0] if x in images else None for x in range(len(memory.transitions))), len(witnesses))

    def verify(self, memory, certificate):
        if certificate != self.descent(memory):
            raise ValueError("invalid descent certificate")
        return True


def original_classification(memory, profiles, contexts):
    """Original T2/T3 with all-history finite-transducer pair receipts."""
    if len(profiles) != len(memory.transitions):
        raise ValueError("profile domain mismatch")
    reached, queue = {memory.initial}, deque([memory.initial])
    while queue:
        for target in memory.transitions[queue.popleft()]:
            if target not in reached:
                reached.add(target)
                queue.append(target)
    o1 = len({profiles[x] for x in reached}) > 1
    for name, rho in contexts.items():
        if len(memory.transitions[0]) != len(rho.transitions[0]):
            raise ValueError("alphabet mismatch")
        first = (memory.initial, rho.initial, memory.run(rho.prefix))
        witnesses, queue, images = {first: ()}, deque([first]), {}
        while queue:
            source, control, output = vertex = queue.popleft()
            word = witnesses[vertex]
            source_profile = profiles[source]
            image = profiles[memory.run(rho.finals[control], output)]
            if source_profile in images and images[source_profile][0] != image:
                return "O2", (name, images[source_profile][1], word)
            images[source_profile] = (image, word)
            for d in range(len(rho.transitions[0])):
                target = (memory.transitions[source][d], rho.transitions[control][d], memory.run(rho.outputs[control][d], output))
                if target not in witnesses:
                    witnesses[target] = word + (d,)
                    queue.append(target)
    return ("O1Only" if o1 else "OutsideO1"), None
