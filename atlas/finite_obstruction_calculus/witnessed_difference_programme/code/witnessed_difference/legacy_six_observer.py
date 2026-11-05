"""Source-bound finite (C,p,~,W,V,tau) education presentation.

This source is known; identity with the unrecovered archival tuple is not proven.
The verifier table is a selected finite domain, not all of the rational space.
"""
from dataclasses import dataclass

from .obstruction import verify_matrix_certificate
from .outcomes import Accepted
from .semantic_legacy_observers import SourceCustody


@dataclass(frozen=True)
class SixObserver:
    custody: SourceCustody
    carrier: tuple
    terms: tuple
    receipts: tuple
    pair_receipts: tuple
    relation: tuple
    terminal_labels: tuple
    terminalizer: tuple

    def __post_init__(self):
        if not isinstance(self.custody, SourceCustody):
            raise ValueError("source binding required")
        for field in ("carrier", "terms", "receipts", "terminal_labels", "terminalizer"):
            object.__setattr__(self, field, tuple(getattr(self, field)))
        for field in ("pair_receipts", "relation"):
            object.__setattr__(self, field, tuple(tuple(row) for row in getattr(self, field)))
        n = len(self.terms)
        if (not n or len(set(self.terms)) != n or len(set(self.carrier)) != len(self.carrier)
                or len(self.receipts) != n or len(self.pair_receipts) != n or len(self.relation) != n
                or any(len(r) != n for r in self.pair_receipts) or any(len(r) != n for r in self.relation)
                or any(type(v) is not bool for row in self.relation for v in row)
                or len(self.terminalizer) != n or not self.terminal_labels
                or any(type(v) is not int or not 0 <= v < len(self.terminal_labels) for v in self.terminalizer)):
            raise ValueError("incomplete six-field domain")
        first = self.receipts[0]
        if len(first.delta) != len(self.carrier):
            raise ValueError("carrier/cochain mismatch")
        for c in (*self.receipts, *(c for row in self.pair_receipts for c in row)):
            if (not isinstance(verify_matrix_certificate(c), Accepted)
                    or (c.matrix, c.columns, c.weights) != (first.matrix, first.columns, first.weights)):
                raise ValueError("actual common repair/gauge certificate required")
        for i in range(n):
            for j in range(n):
                c = self.pair_receipts[i][j]
                if (c.delta != tuple(a-b for a, b in zip(self.receipts[i].delta, self.receipts[j].delta))
                        or self.relation[i][j] != (c.value == 0)):
                    raise ValueError("declared relation must be exactly image(d0) comparison")
                if self.receipts[i] == self.receipts[j] and self.terminalizer[i] != self.terminalizer[j]:
                    raise ValueError("terminalizer must be a function of its receipt")

    def terminal(self, term):
        if type(term) is not int or not 0 <= term < len(self.terms):
            raise ValueError("terminal requires a declared term index")
        return self.terminal_labels[self.terminalizer[term]]
