"""Actual SQLite migrations, independent Fraction sums and custody boundaries.

Claim: urn:omega:fqm:quality:bounded-database-integrity:v1.
AuthorityEffect: None. Local finite database evidence, never physical proofs.
"""
from contextlib import closing
from fractions import Fraction
import hashlib
import io
from pathlib import Path
import random
import sqlite3
from unittest.mock import patch

import pytest

from src.databases.migrations import apply_migration, MigrationError, MigrationObservation


@pytest.fixture
def db():
    with closing(sqlite3.connect(':memory:')) as connection:
        connection.row_factory = sqlite3.Row
        yield connection


def stage(db, number=0):
    db.execute('INSERT INTO genesis_stages VALUES(?,?,?,?,?,?)', (number, 'finite', 'Q', None, 0, 'observed'))


def witness(db, **changes):
    fields = dict(witness_id='w', stage_id=0, x_locus='x', y_locus='y', demand_type='comparison',
                  qx_observation='0', qy_observation='1', reason='finite witness')
    fields.update(changes)
    db.execute('INSERT INTO survivor_witnesses (' + ','.join(fields) + ') VALUES (' + ','.join('?' for _ in fields) + ')', tuple(fields.values()))


def chain(db, **changes):
    fields = dict(chain_id='c', stage_id=0, dimension=1, simplex_label='s', boundary_representation='[]')
    fields.update(changes)
    db.execute('INSERT INTO simplicial_chains (' + ','.join(fields) + ') VALUES (' + ','.join('?' for _ in fields) + ')', tuple(fields.values()))


def objects(db):
    return tuple(db.execute("SELECT name,type,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY name"))


@pytest.mark.parametrize('name', ['ledger', 'signed_ensemble'])
def test_install_empty_rollback_reinstall(db, name):
    receipt = apply_migration(db, name)
    assert type(receipt) is MigrationObservation
    assert receipt.schema == name and receipt.direction == 'up'
    assert receipt.sqlite_version == sqlite3.sqlite_version
    assert len(receipt.source_sha256) == 64
    import src.databases.migrations as module
    assert receipt.source_sha256 == hashlib.sha256(module._source((name, 'up'))).hexdigest()
    with pytest.raises(AttributeError):
        receipt.schema = 'fake'
    assert db.execute('PRAGMA foreign_keys').fetchone()[0] == 1
    assert db.execute('PRAGMA busy_timeout').fetchone()[0] == 1000
    tables = [row for row in db.execute('PRAGMA table_list')
              if row['schema'] == 'main' and row['type'] == 'table'
              and not row['name'].startswith('sqlite_')]
    assert len(tables) == (5 if name == 'ledger' else 3)
    assert all(row['strict'] == 1 and row['wr'] == 1 for row in tables)
    first = objects(db)
    assert first and not db.in_transaction
    down = apply_migration(db, name, 'down')
    assert down.direction == 'down' and objects(db) == () and not db.in_transaction
    assert db.execute("SELECT COUNT(*) FROM sqlite_temp_master WHERE name LIKE '_finite_qm_%'").fetchone()[0] == 0
    assert apply_migration(db, name).source_sha256 == receipt.source_sha256
    assert objects(db) == first


@pytest.mark.parametrize('name', ['ledger', 'signed_ensemble'])
@pytest.mark.parametrize('autocommit', [True, sqlite3.LEGACY_TRANSACTION_CONTROL])
def test_failed_install_is_atomic_and_caller_work_survives(name, autocommit):
    with closing(sqlite3.connect(':memory:', autocommit=autocommit)) as c:
        conflict = 'genesis_stages' if name == 'ledger' else 'signed_ensembles'
        c.execute(f'CREATE TABLE {conflict}(old TEXT)')
        c.execute(f'INSERT INTO {conflict} VALUES (?)', ('untouched',))
        c.commit()
        before = objects(c)
        with pytest.raises(MigrationError, match='SQLite migration refused'):
            apply_migration(c, name)
        assert objects(c) == before and not c.in_transaction
        assert c.execute(f'SELECT * FROM {conflict}').fetchall() == [('untouched',)]
        c.execute('BEGIN')
        c.execute(f'INSERT INTO {conflict} VALUES (?)', ('pending',))
        with pytest.raises(MigrationError, match='idle exclusively owned'):
            apply_migration(c, name)
        assert c.in_transaction
        assert c.execute(f'SELECT COUNT(*) FROM {conflict}').fetchone()[0] == 2
        c.execute('ROLLBACK')
        assert c.execute(f'SELECT COUNT(*) FROM {conflict}').fetchone()[0] == 1


@pytest.mark.parametrize('name,kind', [('ledger','stage'),('ledger','receipt'),('ledger','witness'),('ledger','chain'),('signed_ensemble','ensemble'),('signed_ensemble','path')])
def test_down_refuses_stored_data_without_loss(db, name, kind):
    apply_migration(db, name)
    if kind in ('stage', 'witness', 'chain'):
        stage(db)
        if kind == 'witness':
            witness(db)
        elif kind == 'chain':
            chain(db)
    elif kind == 'receipt':
        db.execute('INSERT INTO ledger_receipts VALUES(?,?,?)', ('a'*64, 'local-reference', 'observation'))
    else:
        db.execute('INSERT INTO signed_ensembles VALUES(?,?)', ('e', 10))
        if kind == 'path':
            db.execute('INSERT INTO signed_configurations VALUES(?,?,?,?,?)', ('e', 1, 'o', 3, 1))
    db.commit()
    before = objects(db)
    data_before = tuple(db.iterdump())
    with pytest.raises(MigrationError):
        apply_migration(db, name, 'down')
    assert not db.in_transaction and objects(db) == before
    assert tuple(db.iterdump()) == data_before


def test_ledger_domains_and_reference_custody(db):
    apply_migration(db, 'ledger')
    stage(db)
    for key, values in {
        'witness_id': [None, '', 'bad id', 'w'*129, 'w\x00tail'],
        'stage_id': [None, -1, 9, 0.0, '0'],
        'x_locus': ['', ' ', 'x'*4097, 'x\x00tail'],
        'reason': ['', 'r'*4097],
        'is_retained': [None, -1, 2, 1.0, '1'],
        'created_at': ['bad', '2026-02-30 00:00:00'],
        'evidence_sha256': ['a'*64],
    }.items():
        for value in values:
            with pytest.raises(sqlite3.IntegrityError):
                witness(db, **{key:value})
    witness(db, x_locus='é'*4096)
    row = db.execute('SELECT * FROM survivor_witnesses').fetchone()
    assert row['is_retained'] == 1 and row['evidence_sha256'] is None
    for value in (None, 'f'*63, 'F'*64, 'g'*64, 'a'*64+'\x00tail'):
        with pytest.raises(sqlite3.IntegrityError):
            db.execute('INSERT INTO ledger_receipts VALUES(?,?,?)', (value, 'reference', 'observation'))
    db.execute('INSERT INTO ledger_receipts VALUES(?,?,?)', ('a'*64, 'local-reference', 'kernel_report'))
    with pytest.raises(sqlite3.IntegrityError):
        chain(db, stokes_verified=1)
    chain(db)
    assert db.execute('SELECT stokes_verified,evidence_sha256 FROM simplicial_chains').fetchone()[:] == (0, None)
    chain(db, chain_id='claimed', stokes_verified=1, evidence_sha256='a'*64)
    with pytest.raises(sqlite3.IntegrityError):
        db.execute('DELETE FROM genesis_stages WHERE stage_num=0')
    with pytest.raises(sqlite3.IntegrityError):
        db.execute('DELETE FROM ledger_receipts')
    for value in (-1,65,1.0,'1'):
        with pytest.raises(sqlite3.IntegrityError):
            chain(db, chain_id='bad', dimension=value)
    for number in (None,-1,1000001,1.0,'1'):
        with pytest.raises(sqlite3.IntegrityError):
            stage(db, number)
    plan = db.execute('EXPLAIN QUERY PLAN SELECT witness_id FROM survivor_witnesses WHERE stage_id=?',(0,)).fetchall()
    assert any('idx_survivor_stage' in row[3] and 'SEARCH' in row[3] for row in plan)


@pytest.mark.parametrize('table', ['genesis_stages','ledger_receipts','survivor_witnesses','simplicial_chains'])
def test_ledger_row_budgets(db, table):
    apply_migration(db, 'ledger')
    if table != 'genesis_stages':
        stage(db)
    if table == 'genesis_stages':
        query = 'INSERT INTO genesis_stages VALUES(?,?,?,?,?,?)'
        rows = [(j,'c','v',None,0,'observed') for j in range(4096)]
        extra = (4096,'c','v',None,0,'observed')
    elif table == 'ledger_receipts':
        query = 'INSERT INTO ledger_receipts VALUES(?,?,?)'
        rows = [(format(j,'064x'),'ref','assertion') for j in range(4096)]
        extra = (format(4096,'064x'),'ref','assertion')
    elif table == 'survivor_witnesses':
        query = 'INSERT INTO survivor_witnesses(witness_id,stage_id,x_locus,y_locus,demand_type,qx_observation,qy_observation,reason) VALUES(?,?,?,?,?,?,?,?)'
        rows = [(str(j),0,'x','y','d','','','r') for j in range(4096)]
        extra = ('4096',0,'x','y','d','','','r')
    else:
        query = 'INSERT INTO simplicial_chains(chain_id,stage_id,dimension,simplex_label,boundary_representation) VALUES(?,?,?,?,?)'
        rows = [(str(j),0,0,'s','') for j in range(4096)]
        extra = ('4096',0,0,'s','')
    db.executemany(query,rows)
    assert db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0] == 4096
    with pytest.raises(sqlite3.IntegrityError, match='row budget'):
        db.execute(query,extra)
    assert db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0] == 4096


def test_signed_sums_and_windows_against_fraction_oracle(db):
    apply_migration(db, 'signed_ensemble')
    rng = random.Random(81023)
    groups = {}
    for e, denominator in [('a',10),('b',17),('c',101)]:
        db.execute('INSERT INTO signed_ensembles VALUES(?,?)',(e,denominator))
        values = [('same',3,1),('same',1,-1),('zero',0,1)]
        values += [(str(rng.randrange(4)),rng.randrange(1000001),rng.choice([-1,1])) for _ in range(47)]
        db.executemany('INSERT INTO signed_configurations VALUES(?,?,?,?,?)',[(e,j,*row) for j,row in enumerate(values)])
        signed = sum((Fraction(m*s,denominator) for o,m,s in values), Fraction())
        mass = sum((Fraction(m,denominator) for o,m,s in values), Fraction())
        row = db.execute('SELECT * FROM SignedEnsembleAudit WHERE ensemble_id=?',(e,)).fetchone()
        assert Fraction(row['signed_numerator'],row['common_denominator']) == signed
        assert Fraction(row['unsigned_numerator'],row['common_denominator']) == mass
        assert Fraction(row['average_sign_num'],row['average_sign_den']) == signed/mass
        assert row['path_count'] == 50 and row['audit_status'] == 'FINITE_SUM'
        for orbit,m,s in values:
            groups.setdefault((e,orbit),[]).append((m,s))
    orbit_rows = db.execute('SELECT * FROM SignedOrbitAudit').fetchall()
    assert {(row['ensemble_id'],row['orbit_id']) for row in orbit_rows} == set(groups)
    for row in orbit_rows:
        values = groups[(row['ensemble_id'],row['orbit_id'])]
        total = sum(m for m,s in values)
        signed = sum(m*s for m,s in values)
        assert row['orbit_path_count'] == len(values)
        assert row['orbit_signed_numerator'] == signed and row['orbit_unsigned_numerator'] == total
        if total:
            assert Fraction(row['average_sign_num'],row['average_sign_den']) == Fraction(signed,total)
        else:
            assert row['average_sign_num'] is None and row['average_sign_den'] is None
    window_rows = db.execute('SELECT * FROM SignedPathWindowAudit').fetchall()
    assert len(window_rows) == 150
    for row in window_rows:
        values = groups[(row['ensemble_id'],row['orbit_id'])]
        assert row['orbit_unsigned_numerator'] == sum(m for m,s in values)
        assert row['orbit_signed_numerator'] == sum(m*s for m,s in values)
    same = db.execute("SELECT average_sign_num,average_sign_den FROM SignedOrbitAudit WHERE orbit_id='same'").fetchall()
    assert len(same) == 3 and all(Fraction(*row) == Fraction(1,2) for row in same)


def test_explicit_empty_zero_balanced_and_negative_cases(db):
    apply_migration(db, 'signed_ensemble')
    for label in ['empty','zero','balanced','negative']:
        db.execute('INSERT INTO signed_ensembles VALUES(?,?)',(label,1))
    db.executemany('INSERT INTO signed_configurations VALUES(?,?,?,?,?)',[
        ('zero',0,'o',0,1),('balanced',0,'o',3,1),('balanced',1,'o',3,-1),('negative',0,'o',3,-1)])
    rows = {r['ensemble_id']:r for r in db.execute('SELECT * FROM SignedEnsembleAudit')}
    assert rows['empty']['audit_status'] == 'EMPTY_ENSEMBLE' and rows['empty']['path_count'] == 0
    assert rows['zero']['audit_status'] == 'ZERO_UNSIGNED_MASS' and rows['zero']['path_count'] == 1
    for label in ['empty','zero']:
        assert rows[label]['average_sign_num'] is None and rows[label]['average_sign_den'] is None
    assert Fraction(rows['balanced']['average_sign_num'],rows['balanced']['average_sign_den']) == 0
    assert Fraction(rows['negative']['average_sign_num'],rows['negative']['average_sign_den']) == -1


def test_signed_domains_and_frozen_denominator(db):
    apply_migration(db, 'signed_ensemble')
    for value in [None,0,-1,1000000001,1.0,'1']:
        with pytest.raises(sqlite3.IntegrityError):
            db.execute('INSERT INTO signed_ensembles VALUES(?,?)',('bad',value))
    for value in [None,'','bad id','x'*129,'e\x00tail']:
        with pytest.raises(sqlite3.IntegrityError):
            db.execute('INSERT INTO signed_ensembles VALUES(?,?)',(value,1))
    db.execute('INSERT INTO signed_ensembles VALUES(?,?)',('e',10))
    db.execute('UPDATE signed_ensembles SET common_denominator=20')
    for index, bads in [(0,['missing']), (1,[None,-1,1000000001,1.0,'1']),
                         (2,[None,'','bad id','o\x00tail']), (3,[None,-1,1000001,0.5,1.0,'1']),
                         (4,[None,0,2,1.0,'1'])]:
        for value in bads:
            row = ['e',0,'o',3,1]
            row[index] = value
            with pytest.raises(sqlite3.IntegrityError):
                db.execute('INSERT INTO signed_configurations VALUES(?,?,?,?,?)',row)
    db.execute('INSERT INTO signed_configurations VALUES(?,?,?,?,?)',('e',0,'o',3,1))
    with pytest.raises(sqlite3.IntegrityError,match='denominator is frozen'):
        db.execute('UPDATE signed_ensembles SET common_denominator=10')
    db.execute('UPDATE signed_ensembles SET common_denominator=20')
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("DELETE FROM signed_ensembles WHERE ensemble_id='e'")
    plan = db.execute('EXPLAIN QUERY PLAN SELECT path_id FROM signed_configurations WHERE ensemble_id=? AND orbit_id=?',('e','o')).fetchall()
    assert any('idx_signed_orbit' in r[3] and 'SEARCH' in r[3] for r in plan)


def test_maximum_signed_sum_stays_integer_and_row_caps(db):
    apply_migration(db, 'signed_ensemble')
    db.executemany('INSERT INTO signed_ensembles VALUES(?,?)',[(str(j),1000000000) for j in range(128)])
    with pytest.raises(sqlite3.IntegrityError,match='ensemble row budget'):
        db.execute('INSERT INTO signed_ensembles VALUES(?,?)',('overflow',1))
    db.executemany('INSERT INTO signed_configurations VALUES(?,?,?,?,?)',[('0',j,'o',1000000,1) for j in range(4096)])
    with pytest.raises(sqlite3.IntegrityError,match='configuration row budget'):
        db.execute('INSERT INTO signed_configurations VALUES(?,?,?,?,?)',('0',4096,'o',1,1))
    row = db.execute("SELECT unsigned_numerator,typeof(unsigned_numerator),signed_numerator FROM SignedEnsembleAudit WHERE ensemble_id='0'").fetchone()
    assert tuple(row) == (4096000000,'integer',4096000000)


def test_migration_source_and_connection_admission(db, monkeypatch):
    import src.databases.migrations as module
    for schema,direction in [(None,'up'),('ledger',[]),('ledger','UP'),('x'*33,'up')]:
        with pytest.raises(MigrationError):
            apply_migration(db,schema,direction)
    with pytest.raises(MigrationError):
        apply_migration(object(),'ledger')
    closed = sqlite3.connect(':memory:');closed.close()
    with pytest.raises(MigrationError,match='SQLite migration refused'):
        apply_migration(closed,'ledger')
    with patch.object(Path,'open',side_effect=OSError('fixture unavailable')):
        with pytest.raises(MigrationError,match='source unavailable'):
            apply_migration(db,'ledger')
    with monkeypatch.context() as m:
        m.setattr(module,'MAX_SCRIPT_BYTES',1)
        with pytest.raises(MigrationError,match='byte budget'):
            apply_migration(db,'ledger')
    with monkeypatch.context() as m:
        m.setattr(module,'_source',lambda key:b'\xff')
        with pytest.raises(MigrationError,match='UTF-8'):
            apply_migration(db,'ledger')
    def broken_factory(cursor,row):
        raise AssertionError('caller row factory must not execute in migration preflight')
    db.row_factory = broken_factory
    assert apply_migration(db,'ledger').schema == 'ledger'


def test_source_streams_are_bounded_and_closed(db):
    import src.databases.migrations as module
    for raw, message in [(b'', 'source is empty'), (b'x'*(module.MAX_SCRIPT_BYTES+1), 'byte budget')]:
        stream = io.BytesIO(raw)
        with patch.object(Path,'open',return_value=stream):
            with pytest.raises(MigrationError,match=message):
                apply_migration(db,'ledger')
        assert stream.closed and not db.in_transaction


def test_closed_names_and_connection_classes(db):
    class StringAlias(str):
        pass
    class ConnectionAlias(sqlite3.Connection):
        pass
    with pytest.raises(MigrationError,match='built-in strings'):
        apply_migration(db,StringAlias('ledger'))
    with closing(sqlite3.connect(':memory:',factory=ConnectionAlias)) as alias:
        with pytest.raises(MigrationError,match='built-in SQLite connection'):
            apply_migration(alias,'ledger')


def test_foreign_key_enablement_is_verified(db):
    def ignore_enable(action,arg1,arg2,database,trigger):
        return sqlite3.SQLITE_IGNORE if action == sqlite3.SQLITE_PRAGMA and arg1 == 'foreign_keys' and arg2 is not None else sqlite3.SQLITE_OK
    db.set_authorizer(ignore_enable)
    try:
        with pytest.raises(MigrationError,match='foreign-key enforcement unavailable'):
            apply_migration(db,'ledger')
        assert not db.in_transaction and objects(db) == ()
    finally:
        db.set_authorizer(None)


def test_failed_open_transaction_and_interrupt_cleanup(db, monkeypatch):
    import src.databases.migrations as module
    with monkeypatch.context() as m:
        m.setattr(module,'_source',lambda key:b'BEGIN IMMEDIATE; CREATE TABLE partial(x);')
        with pytest.raises(MigrationError,match='did not complete'):
            apply_migration(db,'ledger')
    assert not db.in_transaction and objects(db) == ()
    def interrupted(connection):
        connection.execute('BEGIN IMMEDIATE')
        connection.execute('CREATE TABLE interrupted(x)')
        raise KeyboardInterrupt('controlled fixture')
    monkeypatch.setattr(module,'_prepare',interrupted)
    with pytest.raises(KeyboardInterrupt,match='controlled fixture'):
        apply_migration(db,'ledger')
    assert not db.in_transaction and objects(db) == ()


def test_rollback_failure_is_explicit_state_unknown(db, monkeypatch):
    import src.databases.migrations as module
    monkeypatch.setattr(module,'_source',lambda key:b'BEGIN IMMEDIATE; CREATE TABLE partial(x); SELECT * FROM missing; COMMIT;')
    def deny_rollback(action,arg1,arg2,database,trigger):
        return sqlite3.SQLITE_DENY if action == sqlite3.SQLITE_TRANSACTION and arg1 == 'ROLLBACK' else sqlite3.SQLITE_OK
    db.set_authorizer(deny_rollback)
    try:
        with pytest.raises(MigrationError,match='connection state is unverified'):
            apply_migration(db,'ledger')
        assert db.in_transaction
    finally:
        db.set_authorizer(None)
        if db.in_transaction:
            db.execute('ROLLBACK')


def test_busy_database_refusal_releases_no_caller_lock(tmp_path):
    path = tmp_path/'busy.sqlite'
    with closing(sqlite3.connect(path)) as owner, closing(sqlite3.connect(path)) as other:
        owner.execute('CREATE TABLE unrelated(x)');owner.commit()
        owner.execute('BEGIN IMMEDIATE')
        owner.execute('INSERT INTO unrelated VALUES(1)')
        with pytest.raises(MigrationError) as caught:
            apply_migration(other,'ledger')
        assert caught.value.code == 'SQLITE_BUSY' and not other.in_transaction
        assert owner.in_transaction
        owner.execute('ROLLBACK')
        assert apply_migration(other,'ledger').schema == 'ledger'
