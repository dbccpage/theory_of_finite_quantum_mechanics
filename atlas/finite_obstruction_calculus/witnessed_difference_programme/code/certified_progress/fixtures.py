"""Named finite examples for tests; no expected answers in models."""

from __future__ import annotations

from fractions import Fraction

from .model import graph_model as _table_model


def cheaper_route():
    return _table_model({"s": [("direct", "5", ["t"]), ("step", "1", ["u"])],
                         "u": [("finish", "1", ["t"])]})


def value_at(certificate, state):
    return next(Fraction(row["value"]) for row in certificate["values"] if row["belief"] == [state])
