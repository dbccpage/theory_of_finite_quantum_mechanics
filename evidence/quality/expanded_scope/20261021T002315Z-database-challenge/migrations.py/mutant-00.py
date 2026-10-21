"""Owned transactions for the two bounded local SQLite migrations.

Claim: urn:omega:fqm:sql:owned-bounded-migration-lifecycle:v1
Origin: local databases/schema.sql and fermion_sign_problem.sql migrations.
AuthorityEffect: None. An observation receipt is not verification of data truth.
"""
from __future__ import annotations

import hashlib
from contextlib import closing
from pathlib import Path
import sqlite3
from typing import NamedTuple

MAX_SCRIPT_BYTES = 65536
BUSY_TIMEOUT_MS = 1000
_MIGRATIONS = {
    ('ledger', 'up'): 'schema.sql',
    ('ledger', 'down'): 'schema.down.sql',
    ('signed_ensemble', 'up'): 'fermion_sign_problem.sql',
    ('signed_ensemble', 'down'): 'fermion_sign_problem.down.sql',
}


class MigrationError(ValueError):
    """Expected admission, source, ownership or SQLite migration refusal."""

    def __init__(self, invariant: str, code: str | None = None):
        self.invariant, self.code = invariant, code
        super().__init__(invariant if code is None else invariant + ' (' + code + ')')


class MigrationObservation(NamedTuple):
    """Immutable metadata of bytes executed at this call; not an admitted proof."""
    schema: str
    direction: str
    source_sha256: str
    sqlite_version: str


def _key(schema: object, direction: object) -> tuple[str, str]:
    if not isinstance(schema, str) or not isinstance(direction, str):
        raise MigrationError('migration names must be built-in strings')
    if len(schema) > 32 or len(direction) > 8 or (schema, direction) not in _MIGRATIONS:
        raise MigrationError('unknown migration name or direction')
    return schema, direction


def _source(key: tuple[str, str]) -> bytes:
    path = Path(__file__).resolve().with_name(_MIGRATIONS[key])
    try:
        with path.open('rb') as stream:
            raw = stream.read(MAX_SCRIPT_BYTES + 1)
    except OSError as error:
        raise MigrationError('migration source unavailable') from error
    if not raw:
        raise MigrationError('migration source is empty')
    if len(raw) > MAX_SCRIPT_BYTES:
        raise MigrationError('migration source byte budget exceeded')
    return raw


def _idle(connection: object) -> sqlite3.Connection:
    if type(connection) is not sqlite3.Connection:
        raise MigrationError('migration requires a built-in SQLite connection')
    if connection.in_transaction:
        raise MigrationError('migration requires an idle exclusively owned connection')
    return connection


def _prepare(connection: sqlite3.Connection) -> None:
    with closing(connection.cursor()) as cursor:
        cursor.row_factory = None
        cursor.execute('PRAGMA foreign_keys=ON')
        if cursor.execute('PRAGMA foreign_keys').fetchone()[0] != 1:
            raise MigrationError('SQLite foreign-key enforcement unavailable')
        cursor.execute('PRAGMA busy_timeout=' + str(BUSY_TIMEOUT_MS))


def _rollback(connection: sqlite3.Connection) -> None:
    try:
        if connection.in_transaction:
            with closing(connection.cursor()) as cursor:
                cursor.execute('ROLLBACK')
    except sqlite3.Error as error:
        raise MigrationError('rollback failed; connection state is unverified', getattr(error, 'sqlite_errorname', None)) from error


def apply_migration(connection: object, schema: object, direction: object = 'up') -> MigrationObservation:
    """Run a fixed source on an idle caller-owned connection; never close it.

    The caller must own exclusive access and retain foreign_keys=ON afterward.
    This enables FK enforcement and a 1000-ms busy timeout as connection policy.
    Busy waiting is bounded; filesystem stalls and arbitrary caller callbacks
    are not hard-deadline guarantees. Source files are trusted local package
    inputs; their executed digest is observed, not compared with an authority.
    """
    key = _key(schema, direction)
    raw = _source(key)
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as error:
        raise MigrationError('migration source is not UTF-8') from error
    admitted = None
    try:
        admitted = _idle(connection)
        _prepare(admitted)
        with closing(admitted.cursor()) as cursor:
            cursor.executescript(text)
        if admitted.in_transaction:
            raise MigrationError('migration did not complete its transaction')
    except BaseException as error:
        # If admission refused an existing transaction, admitted stays None:
        # rolling that back would destroy caller-owned work.
        if admitted is not None:
            _rollback(admitted)
        if type(error) is MigrationError:
            raise
        if isinstance(error, sqlite3.Error):
            raise MigrationError('SQLite migration refused', getattr(error, 'sqlite_errorname', None)) from error
        raise
    return MigrationObservation(key[0], key[1], hashlib.sha256(raw).hexdigest(), sqlite3.sqlite_version)
