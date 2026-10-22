"""Tests of scripts/build_status.py with an in-memory history.

AuthorityEffect: None. No test touches the network or the real history, except one that asks git whether any generated
status file is tracked. The real build is checked by `python -I -X utf8 scripts/build_status.py --check`.
"""
from pathlib import Path
import datetime as dt
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import build_status as bs  # noqa: E402


def commit(sha, iso, subject):
    return bs.Commit(sha, dt.datetime.fromisoformat(iso).astimezone(dt.timezone.utc), subject)


def node(status, statement='s', stage='GENESIS'):
    return {'status': status, 'statement': statement, 'stage': stage}


class FakeSource:
    """Same methods as GitSource. `snapshots` maps a sha to its nodes; a sha missing from it has no DAG file."""

    def __init__(self, commits, snapshots, logs=None):
        self.commits, self.snapshots, self.logs = commits, snapshots, logs or {}

    def nodes(self, sha):
        return {} if sha is None else self.snapshots.get(sha, {})

    def dag_changed(self, sha, parent):
        return parent is None or self.snapshots.get(sha) != self.snapshots.get(parent)

    def log_lines(self, sha):
        return [] if sha is None else self.logs.get(sha, [])


DAY = dt.date(2026, 10, 22)


def digest(src, day=DAY):
    return bs.render_digest(day, src.commits, bs.partition_by_day(src.commits), src)


# ------------------------------------------------------------------ differences

def test_diff_nodes_reports_added_removed_status_and_statement():
    old = {'A': node('OPEN'), 'B': node('OPEN'), 'C': node('OPEN', 'x'), 'D': node('OPEN')}
    new = {'A': node('PROVED_LEAN'), 'C': node('OPEN', 'y'), 'D': node('OPEN'), 'E': node('DEFINITION')}
    assert bs.diff_nodes(old, new) == [
        ('A', 'status', 'OPEN', 'PROVED_LEAN'), ('B', 'removed', 'OPEN', ''),
        ('C', 'statement', 'OPEN', 'OPEN'), ('E', 'added', '', 'DEFINITION')]


def test_digest_lists_each_kind_of_change_under_its_commit():
    c0 = commit('b' * 40, '2026-10-22T12:00:00+00:00', 'change things')
    c1 = commit('a' * 40, '2026-10-21T12:00:00+00:00', 'base')
    before = {'A': node('OPEN'), 'B': node('OPEN'), 'C': node('OPEN', 'x')}
    after = {'A': node('PROVED_LEAN'), 'C': node('OPEN', 'y'), 'E': node('DEFINITION')}
    text, stats = digest(FakeSource([c0, c1], {c0.sha: after, c1.sha: before}))
    assert '1 added, 1 status, 1 statement, 1 removed' in text
    assert '| `A` | status | `OPEN` | `PROVED_LEAN` |' in text
    assert '| `B` | removed | `OPEN` |  |' in text
    assert '| `C` | statement |' in text and 'Added: `E`' in text
    assert stats == {'commits': 1, 'node_changes': 4}


def test_same_day_add_then_narrow_is_two_events_not_one_addition():
    base = commit('1' * 40, '2026-10-21T09:00:00+00:00', 'before')
    add = commit('2' * 40, '2026-10-22T09:00:00+00:00', 'add X')
    narrow = commit('3' * 40, '2026-10-22T10:00:00+00:00', 'narrow X')
    src = FakeSource([narrow, add, base], {
        base.sha: {},
        add.sha: {'X': node('PROVED_LEAN', 'broad statement')},
        narrow.sha: {'X': node('PROVED_LEAN', 'narrow statement')}})
    text, stats = digest(src)
    first, second = text.index('add X'), text.index('narrow X', text.index('add X') + 1)
    assert first < second                                           # chronological order within the day
    added_part, narrowed_part = text[first:second], text[second:]
    assert 'Added: `X`' in added_part and '| `X` |' not in added_part
    assert '| `X` | statement | `PROVED_LEAN` | `PROVED_LEAN` |' in narrowed_part and 'Added:' not in narrowed_part
    assert stats['node_changes'] == 2


def test_commits_are_partitioned_by_utc_day():
    late_local = commit('a' * 40, '2026-10-21T23:30:00-05:00', 'late in New York, early UTC')    # 22nd 04:30 UTC
    early_local = commit('b' * 40, '2026-10-22T01:00:00+02:00', 'early in Berlin, late UTC')     # 21st 23:00 UTC
    by_day = bs.partition_by_day([late_local, early_local])
    assert by_day[dt.date(2026, 10, 22)] == [0] and by_day[dt.date(2026, 10, 21)] == [1]


def test_a_day_without_commits_says_so():
    only = commit('a' * 40, '2026-10-20T12:00:00+00:00', 'old')
    text, stats = digest(FakeSource([only], {only.sha: {'A': node('OPEN')}}))
    assert 'No commits on this date.' in text and 'No commit of this day changed a node.' in text
    assert stats == {'commits': 0, 'node_changes': 0}


def test_new_campaign_log_lines_are_taken_against_the_parent():
    new = commit('b' * 40, '2026-10-22T12:00:00+00:00', 'log')
    old = commit('a' * 40, '2026-10-21T12:00:00+00:00', 'base')
    line_a, line_b = '2026-10-21 | A | Derived | url | x', '2026-10-22 | B | Narrowed | url | y'
    text, _ = digest(FakeSource([new, old], {new.sha: {}, old.sha: {}}, {new.sha: [line_a, line_b], old.sha: [line_a]}))
    assert '- ' + bs.esc(line_b) in text and bs.esc(line_a) not in text


# ------------------------------------------------------------------ git access

def scripted(handlers):
    """A git runner: `handlers` maps the first word(s) of the command to (code, stdout, stderr) or a function."""
    calls = []

    def run(args):
        calls.append(list(args))
        for key, answer in handlers.items():
            if list(args[:len(key)]) == list(key):
                return answer(args) if callable(answer) else answer
        return 1, '', 'unscripted: %s' % ' '.join(args)
    run.calls = calls
    return run


LOG = ('%s\x1f2026-10-22T12:00:00+00:00\x1fsubject\n%s\x1f2026-10-21T12:00:00+00:00\x1fbase\n' % ('b' * 40, 'a' * 40))
RAW_TOUCH = '\x01%s\n\n:100644 100644 %s %s M\tdag/derivation_dag.json\n' % ('b' * 40, '1' * 40, '2' * 40)


def git_source(extra):
    handlers = {('log', '--first-parent', '--format=%H%x1f%cI%x1f%s'): (0, LOG, ''),
                ('log', '--first-parent', '-m'): (0, RAW_TOUCH, '')}
    handlers.update(extra)
    return bs.GitSource('HEAD', scripted(handlers))


def test_shallow_clone_is_refused():
    src = git_source({('rev-parse', '--is-shallow-repository'): (0, 'true\n', '')})
    with pytest.raises(bs.GitError):
        src.require_full_history()
    src = git_source({('rev-parse', '--is-shallow-repository'): (0, 'false\n', '')})
    src.require_full_history()


def test_failed_cat_file_does_not_become_an_empty_dag():
    src = git_source({('cat-file', 'blob'): (128, '', 'fatal: bad object')})
    with pytest.raises(bs.GitError):
        src.nodes('b' * 40)      # the log says the DAG exists with blob 2222..., but reading it fails


def test_failed_git_show_does_not_turn_every_node_into_an_addition():
    """The old build treated a failed `git show` as an empty DAG, so every node looked added."""
    new, old = 'b' * 40, 'a' * 40
    src = git_source({('cat-file', 'blob'): (128, '', 'fatal: bad object')})
    with pytest.raises(bs.GitError):
        bs.commit_changes(src, src.commits, 0)
    assert src.commits[0].sha == new and src.commits[1].sha == old


def test_absent_path_is_an_empty_snapshot_only_when_git_confirms_it():
    # the oldest commit has no DAG file: no commit at or below it touches the path
    ok = git_source({('cat-file', '-e', 'a' * 40): (0, '', ''), ('cat-file', '-e', 'a' * 40 + ':' + bs.DAG_PATH): (128, '', 'absent')})
    assert ok.nodes('a' * 40) == {}
    missing_commit = git_source({('cat-file', '-e', 'a' * 40): (128, '', 'missing')})
    with pytest.raises(bs.GitError):
        missing_commit.nodes('a' * 40)
    path_exists = git_source({('cat-file', '-e', 'a' * 40): (0, '', ''), ('cat-file', '-e', 'a' * 40 + ':' + bs.DAG_PATH): (0, '', '')})
    with pytest.raises(bs.GitError):
        path_exists.nodes('a' * 40)


def test_a_failing_log_is_an_error():
    src = bs.GitSource('HEAD', scripted({('log',): (128, '', 'fatal: bad revision')}))
    with pytest.raises(bs.GitError):
        src.commits


def test_generated_status_files_are_not_tracked_in_this_repository():
    assert bs.tracked_generated_paths() == []
    out = subprocess.run(['git', 'check-ignore', 'docs/status/README.md', 'docs/status/daily/2026-10-22.md'],
                         cwd=ROOT, capture_output=True, text=True).stdout.split()
    assert out == ['docs/status/README.md', 'docs/status/daily/2026-10-22.md']


def test_tracked_generated_file_is_reported():
    runner = scripted({('ls-files',): (0, 'docs/status/README.md\n', '')})
    assert bs.tracked_generated_paths(runner) == ['docs/status/README.md']


# ------------------------------------------------------------------ pull requests

class Proc:
    def __init__(self, code, out=b'', err=b''):
        self.returncode, self.stdout, self.stderr = code, out, err


def test_prs_are_skipped_unless_requested_and_fail_loudly_when_requested():
    assert bs.prs_block(False) == bs.PRS_PLACEHOLDER
    with pytest.raises(bs.GitError):
        bs.prs_block(True, lambda cmd: Proc(1, b'', b'gh: not logged in'))
    def missing(cmd):
        raise FileNotFoundError('gh')
    with pytest.raises(bs.GitError):
        bs.prs_block(True, missing)
    with pytest.raises(bs.GitError):
        bs.prs_block(True, lambda cmd: Proc(0, b'not json'))
    assert bs.prs_block(True, lambda cmd: Proc(0, b'[]')) == 'There are no open pull requests.'
    row = b'[{"number": 7, "title": "T | x", "author": {"login": "a"}, "isDraft": false, "updatedAt": "2026-10-22T01:00:00Z", "url": "u"}]'
    assert '| [#7](u) | T \\| x | a | ready | 2026-10-22 |' in bs.prs_block(True, lambda cmd: Proc(0, row))


# ------------------------------------------------------------------ generation and drift

def small_source():
    c0 = commit('b' * 40, '2026-10-22T12:00:00+00:00', 'narrow')
    c1 = commit('a' * 40, '2026-10-21T12:00:00+00:00', 'base')
    return FakeSource([c0, c1], {c0.sha: {'A': node('PROVED_LEAN', 'new')}, c1.sha: {'A': node('PROVED_LEAN', 'old')}})


DOC = {'nodes': [{'id': 'A', 'stage': 'GENESIS', 'status': 'PROVED_LEAN', 'statement': 'new'}], 'routes': [], 'stages': ['GENESIS'],
       'status_legend': {'PROVED_LEAN': 'a named Lean declaration exists'}}


def test_generation_is_deterministic_and_has_no_clock_reading(tmp_path):
    first = bs.generate(small_source(), DOC, as_of=DAY, days=3, root=tmp_path)
    second = bs.generate(small_source(), DOC, as_of=DAY, days=3, root=tmp_path)
    assert first == second
    assert sorted(first) == ['docs/status/README.md', 'docs/status/daily/2026-10-20.md', 'docs/status/daily/2026-10-21.md',
                             'docs/status/daily/2026-10-22.md', 'docs/status/daily/index.md']
    assert 'Open pull requests are listed' in first['docs/status/README.md']


def test_check_compares_every_generated_file_byte_for_byte(tmp_path):
    files = bs.generate(small_source(), DOC, as_of=DAY, days=3, root=tmp_path)
    assert bs.drift(files, tmp_path, strict=True) == ['missing: ' + rel for rel in sorted(files)]
    assert bs.drift(files, tmp_path) == []                       # absent files are not drift unless strict
    bs.write_files(files, tmp_path)
    assert bs.drift(files, tmp_path, strict=True) == []
    digest_path = tmp_path / 'docs/status/daily/2026-10-22.md'
    digest_path.write_bytes(digest_path.read_bytes() + b'x')
    assert bs.drift(files, tmp_path) == ['stale: docs/status/daily/2026-10-22.md']
    bs.write_files(files, tmp_path)
    (tmp_path / 'docs/status/daily/2026-01-01.md').write_text('old', encoding='utf-8')
    assert bs.drift(files, tmp_path) == ['unexpected file: docs/status/daily/2026-01-01.md']
    bs.write_files(files, tmp_path)                              # writing removes files the build does not produce
    assert bs.drift(files, tmp_path, strict=True) == []


def test_only_the_pull_request_block_is_ignored(tmp_path):
    files = bs.generate(small_source(), DOC, as_of=DAY, days=2, root=tmp_path)
    bs.write_files(files, tmp_path)
    readme = tmp_path / 'docs/status/README.md'
    text = readme.read_text(encoding='utf-8')
    readme.write_text(text.replace(bs.PRS_PLACEHOLDER, '| PR | different |'), encoding='utf-8')
    assert bs.drift(files, tmp_path) == []
    readme.write_text(text.replace('Where the project stands', 'Where it stands'), encoding='utf-8')
    assert bs.drift(files, tmp_path) == ['stale: docs/status/README.md']
    readme.write_text(text.replace('\n', '\r\n'), encoding='utf-8', newline='')
    assert bs.drift(files, tmp_path) == []                       # line endings are normalised, nothing else is
