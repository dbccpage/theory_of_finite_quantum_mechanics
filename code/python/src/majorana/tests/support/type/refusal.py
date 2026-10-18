"""The Refusal monad and Kleisli pipeline.

Every failed witness, missing theorem, transport failure, or boundary check
must return a typed Refusal.
"""

from typing import Any, Callable, List, TypeVar, Union

T = TypeVar("T")
U = TypeVar("U")


class Refusal:
    """Represents a refusal/failure in the mathematical pipeline."""

    def __init__(self, reason: str, details: Any = None) -> None:
        self.reason = reason
        self.details = details

    def __repr__(self) -> str:
        return f"Refusal(reason={self.reason!r})"


Result = Union[T, Refusal]


def bind(result: Result[T], f: Callable[[T], Result[U]]) -> Result[U]:
    """Monadic bind for Result[T].

    If result is a Refusal, propagates it. Otherwise, applies f to the value.
    """
    if isinstance(result, Refusal):
        return result
    return f(result)


def pipeline(
    stages: List[Callable[[Any], Result[Any]]],
) -> Callable[[Any], Result[Any]]:
    """Compose a list of monadic functions into a single pipeline.

    Short-circuits on the first Refusal.
    """

    def run(initial: Any) -> Result[Any]:
        current: Result[Any] = initial
        for stage in stages:
            current = bind(current, stage)
            if isinstance(current, Refusal):
                break
        return current

    return run
