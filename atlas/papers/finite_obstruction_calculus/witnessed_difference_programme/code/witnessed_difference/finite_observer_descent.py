"""Independent finite constrained-assignment descent witnesses.

This paper reference is separate from the production Rust presheaf/transport
owner. It proves no physical-observer, authority, or cohomology conclusion.
"""

from dataclasses import dataclass
from itertools import product

Report = tuple[tuple[str, str], ...]
Context = frozenset[str]


def restrict(report: Report, context: Context) -> Report:
    return tuple((point, value) for point, value in report if point in context)


class IncompatibleReports(ValueError):
    """Fixed supplied sections disagree on their actual overlap."""


@dataclass(frozen=True)
class FiniteConstrainedSite:
    carrier: Context
    families: tuple[tuple[Context, tuple[Report, ...]], ...]

    def __post_init__(self) -> None:
        normalized_families = tuple(
            (context, tuple(tuple(tuple(pair) for pair in report) for report in reports))
            for context, reports in self.families
        )
        object.__setattr__(self, "families", normalized_families)
        table = dict(self.families)
        if len(table) != len(self.families) or frozenset() not in table or self.carrier not in table:
            raise ValueError("distinct objects must contain empty and full contexts")
        for context, reports in self.families:
            if not context <= self.carrier or len(set(reports)) != len(reports):
                raise ValueError("contexts and report families must be valid and distinct")
            for report in reports:
                if tuple(sorted(report)) != report or len(dict(report)) != len(report):
                    raise ValueError("reports must have canonical distinct point keys")
                if frozenset(dict(report)) != context:
                    raise ValueError("report domain must equal its context")
        for left in table:
            for right in table:
                if left & right not in table:
                    raise ValueError("context objects must be intersection closed")
                if right <= left and any(restrict(report, right) not in table[right] for report in table[left]):
                    raise ValueError("admissible reports must be closed under restriction")

    def _check_cover(self, target: Context, cover: tuple[Context, ...]) -> None:
        table = dict(self.families)
        if target not in table or any(context not in table or not context <= target for context in cover):
            raise ValueError("contexts must form an actual union cover of the target")
        if frozenset().union(*cover) != target:
            raise ValueError("contexts must form an actual union cover of the target")

    def descent_fiber(self, target: Context, cover: tuple[Context, ...], sections: tuple[Report, ...]) -> tuple[Report, ...]:
        table = dict(self.families)
        self._check_cover(target, cover)
        if len(cover) != len(sections):
            raise ValueError("target and one local section per context required")
        if any(section not in table[context] for context, section in zip(cover, sections)):
            raise ValueError("local sections must be admissible")
        for left, context_left in enumerate(cover):
            for right in range(left):
                overlap = context_left & cover[right]
                if restrict(sections[left], overlap) != restrict(sections[right], overlap):
                    raise IncompatibleReports(f"sections {left} and {right} disagree on {sorted(overlap)}")
        return tuple(report for report in table[target] if all(restrict(report, context) == section for context, section in zip(cover, sections)))

    def classify_cover(self, target: Context, cover: tuple[Context, ...]) -> tuple[tuple[tuple[Report, ...], tuple[Report, ...]], ...]:
        self._check_cover(target, cover)
        table = dict(self.families)
        results = []
        for sections in product(*(table[context] for context in cover)):
            try:
                results.append((sections, self.descent_fiber(target, cover, sections)))
            except IncompatibleReports:
                pass
        return tuple(results)


def equality_constraint_site(complete: bool = False) -> FiniteConstrainedSite:
    """00 and 11 are globally admissible; every singleton allows 0 and 1.

    Complete=True additionally allows 01 and 10 and restores the cover sheaf law.
    """
    empty, left, right, full = frozenset(), frozenset({"x"}), frozenset({"y"}), frozenset({"x", "y"})
    reports = ((("x", "0"), ("y", "0")), (("x", "1"), ("y", "1")))
    if complete:
        reports += ((("x", "0"), ("y", "1")), (("x", "1"), ("y", "0")))
    return FiniteConstrainedSite(full, (
        (empty, ((),)), (left, ((("x", "0"),), (("x", "1"),))),
        (right, ((("y", "0"),), (("y", "1"),))), (full, reports),
    ))
