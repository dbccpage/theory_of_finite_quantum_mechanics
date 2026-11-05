# -*- coding: utf-8 -*-
"""
External authority grants (Paper 004 role separation, Paper 005 authority gap).

Authorization is a verified grant, never a caller-supplied boolean:

* ``ExternalAuthority`` holds a secret key and signs an ``AuthorityGrant`` bound to one
  problem digest, one evidence digest, one licensee and one nonce (HMAC-SHA256).
* ``AuthorityKeyring`` is deployment configuration: the verification keys of the
  authorities a CODA instance recognises. It checks the MAC and spends each nonce once.
* The firewall mints an ``AuthorityToken`` only through ``_mint_token`` and only for a
  grant the keyring accepted (MAC verified, nonce spent) against evidence it verified.
  ``_mint_token`` rechecks both, so calling it with a fabricated grant raises. Proposers supply data; they
  do not hold authority keys, so they cannot produce a grant that verifies.

A symmetric key means the keyring can also sign; keep keyrings with the operator, not
with proposers. AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import threading
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

from coda_application.domain._seal import canonical_bytes, seal
from coda_application.domain.entities import AuthorityToken, _token_body

_MIN_KEY_BYTES = 16


def _identifier(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or not value.isascii() or value != value.strip():
        raise ValueError(f"{name} must be a non-blank ASCII string without surrounding whitespace")
    return value


@dataclass(frozen=True)
class AuthorityGrant:
    """A signed grant from one external authority for one evaluated problem."""

    authority_id: str
    licensee: str
    problem_digest: str
    evidence_digest: str
    nonce: str
    mac: str

    def body(self) -> bytes:
        return canonical_bytes(
            {
                "authority_id": self.authority_id,
                "licensee": self.licensee,
                "problem_digest": self.problem_digest,
                "evidence_digest": self.evidence_digest,
                "nonce": self.nonce,
            }
        )


class ExternalAuthority:
    """The declared granter (a human or a policy outside the proposer). Holds the signing key."""

    def __init__(self, authority_id: str, key: bytes) -> None:
        self.authority_id = _identifier(authority_id, "authority_id")
        if not isinstance(key, bytes) or len(key) < _MIN_KEY_BYTES:
            raise ValueError(f"authority key must be at least {_MIN_KEY_BYTES} bytes")
        self.__key = key

    def grant(self, evaluation: Any, licensee: str, nonce: Optional[str] = None) -> AuthorityGrant:
        """Sign a grant for ``licensee`` bound to this evaluation's problem and evidence digests."""
        problem_digest = getattr(evaluation, "problem_digest", "")
        evidence_digest = getattr(evaluation, "evidence_digest", "")
        if not problem_digest or not evidence_digest:
            raise ValueError("a grant binds computed evidence: the evaluation has no problem/evidence digest")
        unsigned = AuthorityGrant(
            authority_id=self.authority_id,
            licensee=_identifier(licensee, "licensee"),
            problem_digest=problem_digest,
            evidence_digest=evidence_digest,
            nonce=_identifier(nonce or secrets.token_hex(16), "nonce"),
            mac="",
        )
        mac = hmac.new(self.__key, unsigned.body(), hashlib.sha256).hexdigest()
        return AuthorityGrant(**{**unsigned.__dict__, "mac": mac})

    def keyring(self) -> AuthorityKeyring:
        return AuthorityKeyring({self.authority_id: self.__key})


class AuthorityKeyring:
    """Verification keys of the authorities this deployment recognises; nonces are single-use."""

    def __init__(self, keys: Mapping[str, bytes]) -> None:
        checked: Dict[str, bytes] = {}
        for authority_id, key in dict(keys).items():
            if not isinstance(key, bytes) or len(key) < _MIN_KEY_BYTES:
                raise ValueError(f"authority key for {authority_id!r} must be at least {_MIN_KEY_BYTES} bytes")
            checked[_identifier(authority_id, "authority_id")] = key
        self.__keys = checked
        self.__spent: set = set()
        self.__lock = threading.Lock()

    def verify(self, grant: Any) -> bool:
        """True iff ``grant`` is an AuthorityGrant signed by a recognised authority."""
        if type(grant) is not AuthorityGrant:
            return False
        fields = (grant.authority_id, grant.licensee, grant.problem_digest, grant.evidence_digest, grant.nonce, grant.mac)
        if not all(isinstance(f, str) and f.isascii() for f in fields):
            return False
        key = self.__keys.get(grant.authority_id)
        if key is None:
            return False
        expected = hmac.new(key, grant.body(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, grant.mac)

    def is_spent(self, grant: AuthorityGrant) -> bool:
        with self.__lock:
            return (grant.authority_id, grant.nonce) in self.__spent

    def spend(self, grant: AuthorityGrant) -> bool:
        """Verify and consume the grant's nonce; False if invalid or already spent."""
        if not self.verify(grant):
            return False
        with self.__lock:
            key = (grant.authority_id, grant.nonce)
            if key in self.__spent:
                return False
            self.__spent.add(key)
            return True


def _mint_token(grant: AuthorityGrant, keyring: AuthorityKeyring) -> AuthorityToken:
    """Firewall-only: mint the token for a grant ``keyring`` has verified and spent.

    The recheck means a grant that was never signed by a recognised authority, or whose
    nonce the firewall has not consumed, cannot be turned into a sealed token here.
    """
    if type(keyring) is not AuthorityKeyring or not keyring.verify(grant) or not keyring.is_spent(grant):
        raise PermissionError("a token is minted only for a verified grant whose nonce the firewall spent")
    fields = {
        "token_id": f"AUTH-{secrets.token_hex(16)}",
        "licensee": grant.licensee,
        "authority_id": grant.authority_id,
        "binding": grant.evidence_digest,
        "granted_externally": True,
        "halt_guards_satisfied": True,
    }
    return AuthorityToken(**fields, seal=seal("authority-token", _token_body(_Fields(fields))))


class _Fields:
    def __init__(self, fields: Dict[str, Any]) -> None:
        self.__dict__.update(fields)
