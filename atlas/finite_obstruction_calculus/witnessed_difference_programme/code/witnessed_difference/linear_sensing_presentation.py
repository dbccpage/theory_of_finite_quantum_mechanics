"""Exact rational linear sensing; repair invariance is a separate checked strengthening."""

from dataclasses import dataclass
from fractions import Fraction


def _q(value):
    if type(value) is not int and not isinstance(value, Fraction):
        raise ValueError("exact rational input required")
    return Fraction(value)


@dataclass(frozen=True)
class RepairBlindspotWitness:
    parameters: tuple[Fraction, ...]
    repair_defect: tuple[Fraction, ...]
    sensed_report: tuple[Fraction, ...]
    is_blindspot: bool
    is_nontrivial: bool


@dataclass(frozen=True)
class LinearSensingPresentation:
    report_rows: tuple[tuple[Fraction, ...], ...]
    repair_rows: tuple[tuple[Fraction, ...], ...]
    repair_columns: int

    def __post_init__(self):
        if type(self.repair_columns) is not int or self.repair_columns < 0:
            raise ValueError("invalid repair dimension")
        reports = tuple(tuple(_q(v) for v in row) for row in self.report_rows)
        repairs = tuple(tuple(_q(v) for v in row) for row in self.repair_rows)
        if any(len(row) != len(repairs) for row in reports) or any(
            len(row) != self.repair_columns for row in repairs
        ):
            raise ValueError("linear sensing shape mismatch")
        object.__setattr__(self, "report_rows", reports)
        object.__setattr__(self, "repair_rows", repairs)

    @staticmethod
    def _apply(rows, values, dimension):
        values = tuple(_q(v) for v in values)
        if len(values) != dimension:
            raise ValueError("linear input shape mismatch")
        return tuple(sum((a * x for a, x in zip(row, values)), Fraction(0)) for row in rows)

    def report(self, defect):
        return self._apply(self.report_rows, defect, len(self.repair_rows))

    def try_quotient(self):
        for row in self.report_rows:
            for j in range(self.repair_columns):
                if sum((row[i] * self.repair_rows[i][j] for i in range(len(row))), Fraction(0)):
                    raise ValueError("report sees admissible repairs: R d0 != 0")
        return LinearSensingQuotient(self)

    def check_repair_blindspot(self, parameters):
        parameters = tuple(_q(v) for v in parameters)
        defect = self._apply(self.repair_rows, parameters, self.repair_columns)
        report = self.report(defect)
        return RepairBlindspotWitness(parameters, defect, report, not any(report), any(defect))

    def verify_blindspot_witness(self, witness):
        if (
            not isinstance(witness, RepairBlindspotWitness)
            or self.check_repair_blindspot(witness.parameters) != witness
        ):
            raise ValueError("blindspot witness differs from actual maps")


@dataclass(frozen=True)
class LinearSensingQuotient:
    sensing: LinearSensingPresentation

    def __post_init__(self):
        # Check directly: construction itself cannot bypass the invariance law.
        s = self.sensing
        if not isinstance(s, LinearSensingPresentation):
            raise ValueError("checked sensing required")
        for j in range(s.repair_columns):
            if any(s.report(tuple(row[j] for row in s.repair_rows))):
                raise ValueError("report sees admissible repairs: R d0 != 0")

    def report(self, defect):
        return self.sensing.report(defect)
