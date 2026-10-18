"""Typed refusal carrier for the omega_terminalizers surface.

Law: a refusal is a valid terminal (gtla.md SVIII legality table, row
"malformed, ungrounded, or illegal route" -> ``Refused``). Every refusal
raised by this package carries a machine-readable ``token`` so callers and
tests can route on the refusal class instead of parsing prose.

AuthorityEffect: None. A refusal never mints, widens, or retires authority.
"""

from __future__ import annotations
class TerminalizerRefusal(ValueError):
    """Typed refusal raised by omega_terminalizers surfaces.

    Attributes:
        token: machine-readable refusal token (stable; tests bind to it).

    The rendered message is ``"<token>: <detail>"`` so existing
    ``pytest.raises(ValueError, match=...)`` callers keep working.
    """

    def __init__(self, token: str, detail: str = "") -> None:
        self.token = token
        super().__init__(f"{token}: {detail}" if detail else token)


__all__ = ["TerminalizerRefusal"]
