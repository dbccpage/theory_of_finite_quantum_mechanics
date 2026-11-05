"""Three deliberately distinct finite observer representations."""

from __future__ import annotations

from dataclasses import dataclass

from .outcomes import Accepted, Outcome, RefusalCode, Refused


@dataclass(frozen=True)
class QuotientObserver:
    carrier: tuple[str, ...]
    equivalence_classes: tuple[frozenset[str], ...]
    comparison: str

    def __post_init__(self) -> None:
        if (
            type(self.carrier) is not tuple
            or not self.carrier
            or any(not isinstance(label, str) or not label for label in self.carrier)
        ):
            raise ValueError("quotient carrier must be an immutable tuple of named states")
        if type(self.equivalence_classes) is not tuple or any(
            type(block) is not frozenset
            or not block
            or any(not isinstance(label, str) or not label for label in block)
            for block in self.equivalence_classes
        ):
            raise ValueError("equivalence classes must be immutable nonempty named blocks")
        labels = set(self.carrier)
        if len(labels) != len(self.carrier):
            raise ValueError("quotient carrier must be nonempty and unique")
        if not isinstance(self.comparison, str) or not self.comparison:
            raise ValueError("comparison is required")
        seen: set[str] = set()
        for block in self.equivalence_classes:
            if not block or seen.intersection(block) or not block.issubset(labels):
                raise ValueError("equivalence classes must be a disjoint partition")
            seen.update(block)
        if seen != labels:
            raise ValueError("equivalence classes must cover the carrier")


@dataclass(frozen=True)
class OperationalObserverPacket:
    states: tuple[str, ...]
    start_state: str
    alphabet: tuple[str, ...]
    transitions: tuple[tuple[str, str, str], ...]
    reports: tuple[tuple[str, str], ...]
    profiles: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if (
            type(self.states) is not tuple
            or not self.states
            or any(not isinstance(state, str) or not state for state in self.states)
            or type(self.alphabet) is not tuple
            or not self.alphabet
            or any(not isinstance(symbol, str) or not symbol for symbol in self.alphabet)
            or type(self.transitions) is not tuple
            or type(self.reports) is not tuple
            or type(self.profiles) is not tuple
        ):
            raise ValueError("operational observer collections must be immutable named tuples")
        state_set = set(self.states)
        symbol_set = set(self.alphabet)
        if (
            len(state_set) != len(self.states)
            or not isinstance(self.start_state, str)
            or self.start_state not in state_set
        ):
            raise ValueError("operational states must be unique and contain the start state")
        if len(symbol_set) != len(self.alphabet):
            raise ValueError("alphabet must be nonempty and unique")
        if any(
            type(transition) is not tuple
            or len(transition) != 3
            or any(not isinstance(item, str) or not item for item in transition)
            for transition in self.transitions
        ):
            raise ValueError("transitions must be immutable named triples")
        if any(
            source not in state_set or target not in state_set or symbol not in symbol_set
            for source, symbol, target in self.transitions
        ):
            raise ValueError("transition lies outside the operational carrier")
        for name, records in (("reports", self.reports), ("profiles", self.profiles)):
            if any(
                type(record) is not tuple
                or len(record) != 2
                or any(not isinstance(item, str) or not item for item in record)
                for record in records
            ):
                raise ValueError(f"{name} must be immutable named pairs")
        if len(self.reports) != len(self.states) or {state for state, _ in self.reports} != state_set:
            raise ValueError("reports must cover every state exactly once")
        if len(self.profiles) != len(self.states) or {state for state, _ in self.profiles} != state_set:
            raise ValueError("profiles must cover every state exactly once")


@dataclass(frozen=True)
class ObserverObject:
    carrier_k: str
    local_state_f: str
    comparison_r: str
    defect_map_delta: str
    repair_d0: str
    closure_d1: str | None
    gauge_j: str
    transform_m: str
    terminalizer_tau: str

    @property
    def complete(self) -> bool:
        required = (
            self.carrier_k,
            self.local_state_f,
            self.comparison_r,
            self.defect_map_delta,
            self.repair_d0,
            self.gauge_j,
            self.transform_m,
            self.terminalizer_tau,
        )
        return all(isinstance(value, str) and bool(value) for value in required) and (
            self.closure_d1 is None
            or isinstance(self.closure_d1, str) and bool(self.closure_d1)
        )


@dataclass(frozen=True)
class ObserverBridge:
    source_kind: str
    local_state_f: str
    defect_map_delta: str
    repair_d0: str
    closure_d1: str | None
    gauge_j: str
    transform_m: str
    terminalizer_tau: str


def _bridge_is_typed(bridge: ObserverBridge) -> bool:
    required = (
        bridge.source_kind,
        bridge.local_state_f,
        bridge.defect_map_delta,
        bridge.repair_d0,
        bridge.gauge_j,
        bridge.transform_m,
        bridge.terminalizer_tau,
    )
    return all(isinstance(value, str) and bool(value) for value in required) and (
        bridge.closure_d1 is None
        or isinstance(bridge.closure_d1, str) and bool(bridge.closure_d1)
    )


def adapt_quotient(
    observer: QuotientObserver,
    bridge: ObserverBridge | None,
) -> Outcome[ObserverObject]:
    if not isinstance(observer, QuotientObserver):
        return Refused(RefusalCode.INVALID_INPUT, "quotient observer has the wrong type")
    if bridge is None:
        return Refused(RefusalCode.MISSING_ADAPTER, "quotient observers need an explicit bridge")
    if not isinstance(bridge, ObserverBridge) or not _bridge_is_typed(bridge):
        return Refused(RefusalCode.INVALID_INPUT, "bridge fields must be nonempty typed strings")
    if bridge.source_kind != "quotient":
        return Refused(RefusalCode.ADAPTER_MISMATCH, "bridge is not declared for a quotient observer")
    result = ObserverObject(
        carrier_k="quotient:" + ",".join(observer.carrier),
        local_state_f=bridge.local_state_f,
        comparison_r=observer.comparison,
        defect_map_delta=bridge.defect_map_delta,
        repair_d0=bridge.repair_d0,
        closure_d1=bridge.closure_d1,
        gauge_j=bridge.gauge_j,
        transform_m=bridge.transform_m,
        terminalizer_tau=bridge.terminalizer_tau,
    )
    if not result.complete:
        return Refused(RefusalCode.INVALID_INPUT, "bridge leaves a required observer field empty")
    return Accepted(result)


def adapt_operational(
    observer: OperationalObserverPacket,
    bridge: ObserverBridge | None,
) -> Outcome[ObserverObject]:
    if not isinstance(observer, OperationalObserverPacket):
        return Refused(RefusalCode.INVALID_INPUT, "operational observer has the wrong type")
    if bridge is None:
        return Refused(RefusalCode.MISSING_ADAPTER, "operational observers need an explicit bridge")
    if not isinstance(bridge, ObserverBridge) or not _bridge_is_typed(bridge):
        return Refused(RefusalCode.INVALID_INPUT, "bridge fields must be nonempty typed strings")
    if bridge.source_kind != "operational":
        return Refused(RefusalCode.ADAPTER_MISMATCH, "bridge is not declared for an operational observer")
    result = ObserverObject(
        carrier_k="operational:" + ",".join(observer.states),
        local_state_f=bridge.local_state_f,
        comparison_r="report/profile comparison",
        defect_map_delta=bridge.defect_map_delta,
        repair_d0=bridge.repair_d0,
        closure_d1=bridge.closure_d1,
        gauge_j=bridge.gauge_j,
        transform_m=bridge.transform_m,
        terminalizer_tau=bridge.terminalizer_tau,
    )
    if not result.complete:
        return Refused(RefusalCode.INVALID_INPUT, "bridge leaves a required observer field empty")
    return Accepted(result)


def validate_report_profile_separation(observer: OperationalObserverPacket) -> Outcome[bool]:
    """Require profile-distinct states to remain report-distinguishable."""

    if not isinstance(observer, OperationalObserverPacket):
        return Refused(RefusalCode.INVALID_INPUT, "operational observer has the wrong type")
    reports = dict(observer.reports)
    profiles = dict(observer.profiles)
    for index, left in enumerate(observer.states):
        for right in observer.states[index + 1 :]:
            if profiles[left] != profiles[right] and reports[left] == reports[right]:
                return Refused(
                    RefusalCode.REPORT_PROFILE_COLLAPSE,
                    f"profile-distinct states {left!r}, {right!r} share one report",
                )
    return Accepted(True)


# --- Stage 2: Retention Packet & Component-Independence Countermodels CM1–CM5 ---


@dataclass(frozen=True)
class RetentionPacket:
    """Finite memory packet R = (M, u, r, approx) under declared inputs I."""

    memory_carrier: tuple[str, ...]
    inputs: tuple[str, ...]
    update_map: tuple[tuple[str, str, str], ...]
    report_map: tuple[tuple[str, str], ...]
    comparison: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if (
            type(self.memory_carrier) is not tuple
            or not self.memory_carrier
            or any(not isinstance(m, str) or not m for m in self.memory_carrier)
            or len(set(self.memory_carrier)) != len(self.memory_carrier)
        ):
            raise ValueError("memory carrier must be a tuple of unique nonempty states")
        if (
            type(self.inputs) is not tuple
            or not self.inputs
            or any(not isinstance(i, str) or not i for i in self.inputs)
            or len(set(self.inputs)) != len(self.inputs)
        ):
            raise ValueError("inputs must be a tuple of unique nonempty symbols")
        object.__setattr__(self, "memory_carrier", tuple(self.memory_carrier))
        object.__setattr__(self, "inputs", tuple(self.inputs))
        object.__setattr__(
            self, "update_map", tuple(tuple(x) for x in self.update_map)
        )
        object.__setattr__(
            self, "report_map", tuple(tuple(x) for x in self.report_map)
        )
        object.__setattr__(
            self, "comparison", tuple(tuple(x) for x in self.comparison)
        )
        mem_set = set(self.memory_carrier)
        inp_set = set(self.inputs)
        update_keys = []
        for tr in self.update_map:
            if (
                type(tr) is not tuple
                or len(tr) != 3
                or tr[0] not in mem_set
                or tr[1] not in inp_set
                or tr[2] not in mem_set
            ):
                raise ValueError("update transitions must map (M x I) -> M")
            update_keys.append((tr[0], tr[1]))
        if len(update_keys) != len(set(update_keys)):
            raise ValueError("update transitions must have unique (memory, input) source pairs")
        if set(update_keys) != {(m, i) for m in mem_set for i in inp_set}:
            raise ValueError("update transitions must cover all (memory, input) pairs deterministically")
        rep_keys = []
        for rep in self.report_map:
            if type(rep) is not tuple or len(rep) != 2 or rep[0] not in mem_set:
                raise ValueError("reports must map M -> O")
            rep_keys.append(rep[0])
        if len(rep_keys) != len(set(rep_keys)):
            raise ValueError("reports must have unique source states")
        if set(rep_keys) != mem_set:
            raise ValueError("reports must cover all memory carrier states")
        for comp in self.comparison:
            if type(comp) is not tuple or len(comp) != 2:
                raise ValueError("comparison must be pairs of report values")

    def step(self, state: str, input_symbol: str) -> Outcome[str]:
        for src, sym, dst in self.update_map:
            if src == state and sym == input_symbol:
                return Accepted(dst)
        return Refused(
            RefusalCode.INVALID_INPUT, f"no update defined for ({state}, {input_symbol})"
        )

    def report(self, state: str) -> Outcome[str]:
        for s, rep in self.report_map:
            if s == state:
                return Accepted(rep)
        return Refused(RefusalCode.INVALID_INPUT, f"no report for state {state}")

    def are_equivalent(self, o1: str, o2: str) -> bool:
        if o1 == o2:
            return True
        return (o1, o2) in self.comparison or (o2, o1) in self.comparison

    def is_observable(self) -> bool:
        """Checks if distinct memory states produce distinct reports."""
        rep_dict = dict(self.report_map)
        return len(set(rep_dict.values())) == len(self.memory_carrier)

    def is_reversible(self, input_symbol: str) -> bool:
        """Checks if update map under input_symbol is a well-defined permutation on memory_carrier."""
        if input_symbol not in set(self.inputs):
            return False
        step_dict: dict[str, str] = {}
        for src, sym, dst in self.update_map:
            if sym == input_symbol:
                if src in step_dict:
                    return False  # Non-functional (multiple destinations for same src)
                step_dict[src] = dst
        # Must be defined for all memory carrier states
        if set(step_dict.keys()) != set(self.memory_carrier):
            return False
        # Must be injective (hence bijective on finite carrier)
        return len(set(step_dict.values())) == len(self.memory_carrier)


def make_cm1_static_carrier() -> RetentionPacket:
    """CM1: Carrier non-triviality (|M| >= 2) with static update (u(m, i) = m)."""
    m = ("m0", "m1")
    inputs = ("tick",)
    u = (("m0", "tick", "m0"), ("m1", "tick", "m1"))
    r = (("m0", "r0"), ("m1", "r1"))
    approx = (("r0", "r0"), ("r1", "r1"))
    return RetentionPacket(m, inputs, u, r, approx)


def make_cm2_blind_readout() -> RetentionPacket:
    """CM2: Dynamic state update with blind/constant report (r(m) = o0)."""
    m = ("m0", "m1")
    inputs = ("toggle",)
    u = (("m0", "toggle", "m1"), ("m1", "toggle", "m0"))
    r = (("m0", "constant"), ("m1", "constant"))
    approx = (("constant", "constant"),)
    return RetentionPacket(m, inputs, u, r, approx)


def make_cm3_coarse_grained_report() -> RetentionPacket:
    """CM3: Invertible update dynamics with non-injective report (ker(r) > id)."""
    m = ("m0", "m1", "m2")
    inputs = ("cycle",)
    u = (("m0", "cycle", "m1"), ("m1", "cycle", "m2"), ("m2", "cycle", "m0"))
    r = (("m0", "even"), ("m1", "odd"), ("m2", "even"))
    approx = (("even", "even"), ("odd", "odd"))
    return RetentionPacket(m, inputs, u, r, approx)


def make_cm4_nontrivial_tolerance() -> RetentionPacket:
    """CM4: Injective report with non-trivial tolerance relation where o0 ~ o1 despite o0 != o1."""
    m = ("m0", "m1")
    inputs = ("step",)
    u = (("m0", "step", "m1"), ("m1", "step", "m0"))
    r = (("m0", "val0"), ("m1", "val1"))
    approx = (("val0", "val0"), ("val1", "val1"), ("val0", "val1"))
    return RetentionPacket(m, inputs, u, r, approx)


def make_cm5_lossy_reset() -> RetentionPacket:
    """CM5: Injective report (r = id) with collapsing lossy update u(m, reset) = m0."""
    m = ("m0", "m1")
    inputs = ("reset", "keep")
    u = (
        ("m0", "reset", "m0"),
        ("m1", "reset", "m0"),
        ("m0", "keep", "m0"),
        ("m1", "keep", "m1"),
    )
    r = (("m0", "m0"), ("m1", "m1"))
    approx = (("m0", "m0"), ("m1", "m1"))
    return RetentionPacket(m, inputs, u, r, approx)


def tree_behavior_equivalent(
    p1: RetentionPacket,
    s1: str,
    p2: RetentionPacket,
    s2: str,
    depth: int,
) -> bool:
    """Branching observation equivalence over finite computation trees."""
    if set(p1.inputs) != set(p2.inputs):
        return False
    if depth < 0:
        return True
    rep1 = p1.report(s1)
    rep2 = p2.report(s2)
    if isinstance(rep1, Refused) or isinstance(rep2, Refused):
        return False
    if not p1.are_equivalent(rep1.value, rep2.value) or not p2.are_equivalent(rep2.value, rep1.value):
        return False
    if depth == 0:
        return True
    for sym in sorted(p1.inputs):
        next1 = p1.step(s1, sym)
        next2 = p2.step(s2, sym)
        if isinstance(next1, Refused) or isinstance(next2, Refused):
            return False
        if not tree_behavior_equivalent(p1, next1.value, p2, next2.value, depth - 1):
            return False
    return True


# Executable finite evidence; AuthorityEffect: None.

