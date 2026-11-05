"""Source-declared partial observer adapters with actual maps and checks.

Authority tags and historical receipts are preserved as metadata, never treated
as semantics or new authority. Missing layers remain None. Source digest format
checking is not a claim of authentic custody; the inventory records blob checks.
"""
from dataclasses import dataclass, replace
from fractions import Fraction

from .context_reflection import ContextHom, ContextSystem
from .linear_sensing_presentation import LinearSensingPresentation
from .observer import OperationalObserverPacket, QuotientObserver, RetentionPacket
from .obstruction import MatrixQuotientCertificate, verify_matrix_certificate
from .outcomes import Accepted
from .quantum_measurement_replay import (
    FiniteInstrumentModel,
    FinitePositiveMixture,
    outcome_record,
)
from .quotient_observer import LinearQuotientObserver, make_linear_quotient_observer


@dataclass(frozen=True)
class SourceCustody:
    path: str
    recorded_sha256: str
    source_receipts: tuple[str, ...] = ()
    source_authority_tags: tuple[str, ...] = ()

    def __post_init__(self):
        if not isinstance(self.path, str) or not self.path or not isinstance(self.recorded_sha256, str):
            raise ValueError("source identity required")
        if len(self.recorded_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in self.recorded_sha256):
            raise ValueError("source digest must be a SHA256 spelling")
        object.__setattr__(self, "source_receipts", tuple(self.source_receipts))
        object.__setattr__(self, "source_authority_tags", tuple(self.source_authority_tags))


@dataclass(frozen=True)
class Presentation:
    states: tuple[str, ...]
    reports: tuple[str, ...]
    q: tuple[int, ...]
    contexts: ContextSystem | None = None

    def __post_init__(self):
        for field in ("states", "reports", "q"):
            object.__setattr__(self, field, tuple(getattr(self, field)))
        if not self.states or len(set(self.states)) != len(self.states) or not self.reports or len(set(self.reports)) != len(self.reports):
            raise ValueError("unique finite input and report carriers required")
        if len(self.q) != len(self.states) or any(type(x) is not int or not 0 <= x < len(self.reports) for x in self.q):
            raise ValueError("presentation must be a total typed map")
        if self.contexts is not None and len(self.contexts.profiles) != len(self.states):
            raise ValueError("context carrier disagrees")


@dataclass(frozen=True)
class Memory:
    packet: RetentionPacket
    store: tuple[str, ...] | None = None
    presentation_reports: tuple[str, ...] | None = None

    def __post_init__(self):
        packet = self.packet
        for state in packet.memory_carrier:
            for symbol in packet.inputs:
                entries = [target for source, label, target in packet.update_map if (source, label) == (state, symbol)]
                if len(entries) != 1:
                    raise ValueError("memory update must be total and functional")
            if not isinstance(packet.report(state), Accepted):
                raise ValueError("memory readout must be total")
        if (self.store is None) != (self.presentation_reports is None):
            raise ValueError("store and its report carrier must be supplied together")
        if self.store is not None:
            object.__setattr__(self, "store", tuple(self.store))
            object.__setattr__(self, "presentation_reports", tuple(self.presentation_reports))
            if len(self.store) != len(self.presentation_reports):
                raise ValueError("store domain disagrees")
            for state, report in zip(self.store, self.presentation_reports, strict=True):
                # The bridge transports the declared predicate itself.  The
                # historical packet convenience method closes it under
                # equality and symmetry; neither law is part of this adapter.
                if (state not in packet.memory_carrier
                        or (packet.report(state).value, report) not in packet.comparison):
                    raise ValueError("stored presentation does not reaccess under declared comparison")

    def reaccess(self, report_index):
        if self.store is None:
            raise ValueError("missing presentation-to-memory interface")
        if type(report_index) is not int or not 0 <= report_index < len(self.store):
            raise ValueError("report index outside presentation carrier")
        return self.packet.report(self.store[report_index]).value


@dataclass(frozen=True)
class FiniteEvaluator:
    contexts: ContextSystem
    certificates: tuple[MatrixQuotientCertificate, ...]
    transforms: tuple[tuple[int, ...], ...]
    tolerance: Fraction

    def __post_init__(self):
        object.__setattr__(self, "certificates", tuple(self.certificates))
        object.__setattr__(self, "transforms", tuple(tuple(t) for t in self.transforms))
        if type(self.tolerance) is not Fraction or self.tolerance < 0:
            raise TypeError("exact nonnegative tolerance required")
        if len(self.certificates) != len(self.contexts.profiles):
            raise ValueError("finite defect domain disagrees")
        for certificate in self.certificates:
            if not isinstance(verify_matrix_certificate(certificate), Accepted):
                raise ValueError("certificate failed independent replay")
        first = self.certificates[0]
        if any(c.matrix != first.matrix or c.weights != first.weights or c.columns != first.columns for c in self.certificates):
            raise ValueError("repair and gauge declarations must be common")
        for t in self.transforms:
            ContextHom(self.contexts, self.contexts, t)
            if sorted(t) != list(range(len(self.certificates))) or any(self.certificates[i].value != self.certificates[j].value for i, j in enumerate(t)):
                raise ValueError("transform must preserve the actual finite evaluations")

    def status(self, state):
        if type(state) is not int or not 0 <= state < len(self.certificates):
            raise ValueError("state outside evaluator domain")
        return "WithinTolerance" if self.certificates[state].value <= self.tolerance else "AboveTolerance"


@dataclass(frozen=True)
class AdaptedObserver:
    custody: SourceCustody
    presentation: Presentation | None = None
    memory: Memory | None = None
    operational: OperationalObserverPacket | None = None
    evaluator: FiniteEvaluator | None = None
    policy: tuple[str, str] | None = None
    linear: LinearQuotientObserver | None = None
    quantum: tuple | None = None
    linear_sensing: LinearSensingPresentation | None = None


def adapt_quotient(source, custody):
    if not isinstance(source, QuotientObserver):
        raise ValueError("checked quotient source required")
    q = tuple(next(i for i, block in enumerate(source.equivalence_classes) if state in block) for state in source.carrier)
    return AdaptedObserver(custody, Presentation(source.carrier, tuple(f"class:{i}" for i in range(len(source.equivalence_classes))), q))


def adapt_report_context(presentation, custody):
    if not isinstance(presentation, Presentation) or presentation.contexts is None:
        raise ValueError("explicit context semantics required")
    return AdaptedObserver(custody, presentation)


def adapt_operational(source, custody):
    if not isinstance(source, OperationalObserverPacket):
        raise ValueError("typed operational source required")
    states = source.states
    table = {(s, a): target for s, a, target in source.transitions}
    if len(table) != len(source.transitions) or set(table) != {(s, a) for s in states for a in source.alphabet}:
        raise ValueError("operational action must be complete and functional")
    report_table, profile_table = dict(source.reports), dict(source.profiles)
    if set(report_table) != set(states) or set(profile_table) != set(states):
        raise ValueError("report/profile domains must be exact")
    report_labels = tuple(sorted(set(report_table.values())))
    profile_labels = tuple(sorted(set(profile_table.values())))
    contexts = ContextSystem(tuple(profile_labels.index(profile_table[s]) for s in states),
                             tuple(tuple(states.index(table[s, a]) for a in source.alphabet) for s in states), len(source.alphabet))
    presentation = Presentation(states, report_labels, tuple(report_labels.index(report_table[s]) for s in states), contexts)
    return AdaptedObserver(custody, presentation, operational=source)


def attach_memory(adapted, memory):
    if adapted.presentation is None or memory.store is None or memory.presentation_reports != adapted.presentation.reports:
        raise ValueError("explicit report-to-memory bridge required")
    return replace(adapted, memory=memory)


def attach_evaluator(adapted, evaluator, policy=None):
    if adapted.presentation is None or adapted.presentation.contexts != evaluator.contexts:
        raise ValueError("evaluator domain must match explicit presentation contexts")
    if policy is not None:
        policy = tuple(policy)
        if len(policy) != 2 or any(action not in {"Store", "Emit", "RequestData", "Refuse"} for action in policy):
            raise ValueError("policy must define both exact status actions")
    return replace(adapted, evaluator=evaluator, policy=policy)


def adapt_linear(source, custody):
    if not isinstance(source, LinearQuotientObserver) or not isinstance(make_linear_quotient_observer(source.complex_, source.report_rows), Accepted):
        raise ValueError("linear quotient must independently satisfy R d0=0")
    return AdaptedObserver(custody, linear=source)


def adapt_quantum(instrument, mixture, custody):
    if not isinstance(instrument, FiniteInstrumentModel) or not isinstance(mixture, FinitePositiveMixture):
        raise ValueError("exact instrument and positive mixture required")
    # Retain the full quantum carrier and all outcome records, not only labels.
    records = tuple(outcome_record(instrument, mixture, i) for i in range(len(instrument.groups)))
    return AdaptedObserver(custody, quantum=(instrument, mixture, mixture.density(instrument.dimension), records))


def self_report(adapted, target_custody, state, memory_state, decoder):
    if (target_custody.path, target_custody.recorded_sha256) != (adapted.custody.path, adapted.custody.recorded_sha256):
        raise ValueError("self target belongs to another declared source")
    if adapted.presentation is None or adapted.memory is None:
        raise ValueError("self-target presentation and reaccess semantics required")
    if type(state) is not int or not 0 <= state < len(adapted.presentation.q):
        raise ValueError("self target outside presentation")
    if memory_state not in adapted.memory.packet.memory_carrier:
        raise ValueError("reaccess state outside memory")
    report = adapted.memory.packet.report(memory_state).value
    if report not in decoder or decoder[report] != adapted.presentation.q[state]:
        raise ValueError("reaccessed payload does not decode the targeted component")
    return (state, report, adapted.presentation.q[state])



def adapt_linear_sensing(source, custody):
    """General sensing is a report, not automatically a repair-quotient report."""
    if not isinstance(source, LinearSensingPresentation):
        raise ValueError("checked exact linear sensing source required")
    # Reconstruct shape/coefficient validation independently; do not assume Rd0=0.
    checked = LinearSensingPresentation(source.report_rows, source.repair_rows, source.repair_columns)
    return AdaptedObserver(custody, linear_sensing=checked)
