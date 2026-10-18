"""Outcome coproduct and fail-closed Python authority boundary."""

from typing import Any, Optional, Union

try:
    from omega_engine.crates.replay import DescentWitness
except ImportError:
    try:
        from omega_engine.crates.replay import DescentWitness
    except ImportError:
        class DescentWitness:
            pass

from .refusal import Refusal
from .terminal import AuthorityTerminal, Terminal, is_auth



class CertifiedAuthority:
    """Host-only authority record.

    The Python mirror has no authenticated human-promotion adapter, so its
    public constructor refuses every local certification attempt:
    :meth:`certify` always raises ``PermissionError`` after its guard checks
    pass and never returns an instance — no code path in this repo
    legitimately constructs a ``CertifiedAuthority``.

    Sealing: mirrors the sentinel-key pattern shared with
    ``omega_pipelines.gtlanf.GtlaNf`` and ``omega_replay.DescentWitness`` —
    the sentinel key is name-mangled (``__sealed_key``). A prior version of
    this file kept the key as a plain, unmangled class attribute
    (``_secret_key``), so ``CertifiedAuthority(CertifiedAuthority._secret_key,
    "FAKE_TERMINAL", "FAKE_WITNESS")`` constructed successfully — a live
    authority-forgery vector (a caller could mint an "always-refused" record
    directly, bypassing ``certify()``'s host law), not merely a
    documentation gap. ``CertifiedAuthority._secret_key`` no longer exists
    (``AttributeError``).

    The seal is BEST-EFFORT (Inspector M18 precedent, same honesty level as
    the other two seals): Python has no private fields, so a sufficiently
    determined caller can still reach the mangled name
    ``CertifiedAuthority._CertifiedAuthority__sealed_key``. It blocks
    casual/accidental construction and makes forgery loud in review; it is
    not a cryptographic unforgeability guarantee — the Rust owner's private
    fields are the enforced boundary.
    """

    __sealed_key: Any = object()  # name-mangled; best-effort seal (M18)

    def __init__(self, key: Any, terminal: AuthorityTerminal, witness: Any) -> None:
        if key is not CertifiedAuthority.__sealed_key:
            raise TypeError("CertifiedAuthority construction is sealed")
        self._terminal = terminal
        self._witness = witness

    @property
    def terminal(self) -> AuthorityTerminal:
        return self._terminal

    @property
    def witness(self) -> Any:
        return self._witness

    @classmethod
    def certify(
        cls,
        terminal: AuthorityTerminal,
        witness: Any,
        descent_state: Any = None,
    ) -> "CertifiedAuthority":
        if not isinstance(witness, DescentWitness):
            raise TypeError("CertifiedAuthority requires a DescentWitness")
        if witness.replay_hash != getattr(descent_state, "replay_hash", None):
            raise ValueError("descent state is not bound to the replay witness")
        if not is_auth(terminal, descent_state):
            raise ValueError("terminal does not satisfy the authority guards")
        raise PermissionError(
            "local Python certification is disabled; authenticated human "
            "promotion must be supplied by the host authority boundary"
        )


Outcome = Union[Terminal, Refusal]


def authority_from_outcome(
    outcome: Outcome,
    witness: Any,
    descent_state: Any = None,
) -> Optional[CertifiedAuthority]:
    if not isinstance(outcome, AuthorityTerminal):
        return None
    try:
        return CertifiedAuthority.certify(outcome, witness, descent_state)
    except (PermissionError, TypeError, ValueError):
        return None


__all__ = ["CertifiedAuthority", "Outcome", "authority_from_outcome"]


