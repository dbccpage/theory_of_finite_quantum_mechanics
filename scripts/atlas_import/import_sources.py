"""Bounded, byte-bound atlas import with prepare/apply separation.

AuthorityEffect: None. Only selected path fields are rewritten. Supplied plan
hashes are checked, not independently authenticated against sibling Git history.
Apply serializes cooperating importers, stages every output, and rolls back handled
I/O failures. It is not a multi-file crash-atomic transaction. Interrupted stages
retain originals and a journal for manual recovery; a retained lock blocks reuse.
The caller must keep the repository free of uncooperative concurrent writers.
"""
from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
import difflib
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile
from typing import TypeAlias

JSON: TypeAlias = None | bool | int | float | str | list['JSON'] | dict[str, 'JSON']
COMMIT_PARENT = '3379759468^'
REWRITE_KEYS = {'source', 'lean', 'lean4', 'rust', 'python', 'path', 'witnesses', 'sources'}
SKIP_KEYS = {'f004_refs', 'coda_atlas_paths', 'coda_atlas_ids'}
DEST = 'sources/atlas/papers'
MAX_FILE = 16 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_ROWS = 10000


class FailureCode(str, Enum):
    INVALID_PLAN = 'invalid_plan'
    INVALID_PATH = 'invalid_path'
    LIMIT = 'resource_limit'
    SOURCE_CHANGED = 'source_changed'
    STALE_INPUT = 'stale_input'
    BUSY = 'writer_busy'
    IO = 'io_failure'
    RECOVERY = 'manual_recovery_required'


class ImportFailure(Exception):
    def __init__(self, code: FailureCode, detail: str):
        self.code = code
        super().__init__(f'{code.value}: {detail}')


@dataclass(frozen=True)
class Snapshot:
    relative: str
    before: bytes | None
    after: bytes | None


@dataclass(frozen=True)
class PreparedImport:
    root: Path
    files: tuple[Snapshot, ...]
    copied: int
    resolved: int
    rewrites: int
    fragments: tuple[str, ...]


@dataclass
class Budget:
    used: int = 0

    def charge(self, size: int) -> None:
        if size > MAX_FILE or self.used + size > MAX_TOTAL:
            raise ImportFailure(FailureCode.LIMIT, 'file or aggregate byte limit exceeded')
        self.used += size

    def read(self, path: Path) -> bytes:
        with path.open('rb') as stream:
            data = stream.read(MAX_FILE + 1)
        self.charge(len(data))
        return data


def is_reparse(path: Path) -> bool:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def inside(root: Path, relative: str) -> Path:
    """Reject escaping, symlink and Windows junction paths, including ancestors."""
    rel = Path(relative)
    if not relative or ':' in relative or rel.is_absolute() or rel.root or rel.drive or '..' in rel.parts:
        raise ImportFailure(FailureCode.INVALID_PATH, repr(relative))
    target = root / rel
    cursor = target
    while cursor != root:
        if is_reparse(cursor):
            raise ImportFailure(FailureCode.INVALID_PATH, f'reparse point: {cursor}')
        cursor = cursor.parent
    if target == root or not target.resolve().is_relative_to(root):
        raise ImportFailure(FailureCode.INVALID_PATH, relative)
    return target


def mapping(value: JSON) -> dict[str, JSON]:
    if not isinstance(value, dict):
        raise ImportFailure(FailureCode.INVALID_PLAN, 'expected an object')
    return value


def string(row: dict[str, JSON], key: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value:
        raise ImportFailure(FailureCode.INVALID_PLAN, f'missing string: {key}')
    return value


def parse(data: bytes) -> JSON:
    try:
        result: JSON = json.loads(data)
        return result
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ImportFailure(FailureCode.INVALID_PLAN, f'invalid JSON: {exc}') from exc


def encode(value: JSON, indent: int = 2) -> bytes:
    try:
        return (json.dumps(value, indent=indent, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ImportFailure(FailureCode.INVALID_PLAN, f'unserializable JSON: {exc}') from exc


def rewrite(obj: JSON, pattern: re.Pattern[str], table: dict[str, str],
            counter: collections.Counter[str], ctx: str = '') -> JSON:
    if isinstance(obj, dict):
        out = {k: v if k in SKIP_KEYS else rewrite(v, pattern, table, counter, k) for k, v in obj.items()}
        if out.get('root') == 'symbol_game' and out.get('path') in list(table.values()):
            out['root'] = 'local'
            counter['root->local'] += 1
        return out
    if isinstance(obj, list):
        return [rewrite(v, pattern, table, counter, ctx) for v in obj]
    if isinstance(obj, str) and ctx in REWRITE_KEYS and not obj.startswith('absent'):
        def sub(match: re.Match[str]) -> str:
            counter[ctx] += 1
            return table[match.group(0)]
        return pattern.sub(sub, obj)
    return obj


def line_diff(a: bytes, b: bytes) -> dict[str, JSON]:
    left, right = a.decode('utf-8', 'replace').splitlines(), b.decode('utf-8', 'replace').splitlines()
    result: dict[str, JSON] = {'lines_atlas': len(left), 'lines_in_repo': len(right)}
    # Similarity is a bounded diagnostic, never a byte-identity certificate.
    if len(left) * len(right) <= 4_000_000:
        result['similarity'] = round(difflib.SequenceMatcher(None, left, right, autojunk=False).ratio(), 4)
    return result


def normalise(data: bytes) -> bytes:
    return data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')


def read_optional(path: Path, budget: Budget) -> bytes | None:
    try:
        return budget.read(path)
    except FileNotFoundError:
        return None


def add_snapshot(root: Path, files: dict[Path, Snapshot], relative: str,
                 after: bytes | None, budget: Budget, *, copy: bool = False) -> bytes | None:
    path = inside(root, relative)
    if path in files and after is None and files[path].before == files[path].after:
        return files[path].before
    if path in files:
        raise ImportFailure(FailureCode.INVALID_PLAN, f'colliding destination: {relative}')
    before = read_optional(path, budget)
    if copy and before is not None and before != after:
        raise ImportFailure(FailureCode.STALE_INPUT, f'existing copy differs: {relative}')
    if after is not None:
        budget.charge(len(after))
    files[path] = Snapshot(relative, before, after if after is not None else before)
    return before


def prepare_row(root: Path, row: dict[str, JSON], files: dict[Path, Snapshot],
                budget: Budget) -> tuple[str, str, dict[str, JSON]]:
    original, source = string(row, 'atlas_path'), string(row, 'ana_path')
    digest, size = string(row, 'git_sha256'), row.get('size')
    if row.get('status') != 'verified' or re.fullmatch('[0-9a-f]{64}', digest) is None:
        raise ImportFailure(FailureCode.INVALID_PLAN, f'unverified source: {original}')
    if type(size) is not int or size < 0:
        raise ImportFailure(FailureCode.INVALID_PLAN, f'invalid source size: {original}')
    data = budget.read(Path(source))
    if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
        raise ImportFailure(FailureCode.SOURCE_CHANGED, original)
    twin = row.get('resolved_to_existing')
    entry: dict[str, JSON] = {'original_atlas_path': original, 'ana_path': source,
        'sha256': digest, 'size_bytes': size, 'git_commit': COMMIT_PARENT + ' (the_symbol_game)'}
    if twin is not None:
        twin_row = mapping(twin)
        dest, match = string(twin_row, 'path'), string(twin_row, 'match')
        target = add_snapshot(root, files, dest, None, budget)
        if target is None or match not in ('identical', 'newline_equivalent'):
            raise ImportFailure(FailureCode.INVALID_PLAN, f'invalid twin: {original}')
        equal = data == target if match == 'identical' else normalise(data) == normalise(target)
        if not equal:
            raise ImportFailure(FailureCode.SOURCE_CHANGED, f'twin: {dest}')
        entry.update(outcome='resolved_to_existing', match=match)
    else:
        family = string(row, 'family')
        if re.fullmatch('[A-Za-z0-9_-]+', family) is None:
            raise ImportFailure(FailureCode.INVALID_PLAN, f'invalid family: {family}')
        rel = string(row, 'rel')
        inside(root, rel)
        dest = f'{DEST}/{family}/{rel}'
        add_snapshot(root, files, dest, data, budget, copy=True)
        target = data
        entry['outcome'] = 'copied'
        differences = edition_differences(root, row, data, budget)
        if differences:
            entry['edition_difference'] = differences
    entry.update(in_repo_path=dest, in_repo_sha256=hashlib.sha256(target).hexdigest())
    return original, dest, entry


def edition_differences(root: Path, row: dict[str, JSON], data: bytes, budget: Budget) -> dict[str, JSON]:
    twins = row.get('in_repo_same_name_different_content', [])
    if not isinstance(twins, list) or any(not isinstance(t, str) for t in twins):
        raise ImportFailure(FailureCode.INVALID_PLAN, 'invalid edition paths')
    if not twins:
        return {}
    diffs: dict[str, JSON] = {}
    for value in twins[:3]:
        if isinstance(value, str):
            diffs[value] = line_diff(data, budget.read(inside(root, value)))
    return {'same_named_in_repo_files': twins,
            'note': 'the in-repo file differs from the atlas file; references keep pointing at the atlas copy',
            'diffs': diffs}


def prepare(root: Path, rows: JSON) -> PreparedImport:
    """Read-only preparation: no output is published until all inputs validate."""
    root = root.resolve(strict=True)
    if not isinstance(rows, list) or not rows or len(rows) > MAX_ROWS:
        raise ImportFailure(FailureCode.INVALID_PLAN, 'plan must have 1..10000 rows')
    budget = Budget()
    files: dict[Path, Snapshot] = {}
    table: dict[str, str] = {}
    provenance: list[JSON] = []
    copied = resolved = 0
    for value in rows:
        row = mapping(value)
        original = string(row, 'atlas_path')
        if original in table:
            raise ImportFailure(FailureCode.INVALID_PLAN, f'duplicate source: {original}')
        original, dest, entry = prepare_row(root, row, files, budget)
        table[original] = dest
        provenance.append(entry)
        copied += int(entry['outcome'] == 'copied')
        resolved += int(entry['outcome'] == 'resolved_to_existing')
    document: dict[str, JSON] = {'schema_version': 'atlas_sources_provenance.v1', 'authority_effect': 'None',
        'source': 'the_symbol_game omega_engine_atlas/coda_atlas/F004_papers/{family}, deleted from the sibling working tree by commit 3379759468 and restored to --ana',
        'git_commit': COMMIT_PARENT, 'copied': copied, 'resolved_to_existing': resolved,
        'files': sorted(provenance, key=lambda e: string(mapping(e), 'original_atlas_path'))}
    add_snapshot(root, files, 'sources/atlas/PROVENANCE.json', encode(document, 1), budget)
    pattern = re.compile(r'(?<![\w/.\-])(?:' + '|'.join(re.escape(p) for p in sorted(table, key=len, reverse=True)) + r')(?![\w/])')
    paths = ['dag/derivation_dag.json'] + sorted(p.relative_to(root).as_posix() for p in (root / 'dag/fragments').glob('*.json'))
    if len(paths) > MAX_ROWS:
        raise ImportFailure(FailureCode.LIMIT, 'too many DAG fragments')
    counter: collections.Counter[str] = collections.Counter()
    for relative in paths:
        before = budget.read(inside(root, relative))
        try:
            new = rewrite(parse(before), pattern, table, counter)
        except RecursionError as exc:
            raise ImportFailure(FailureCode.LIMIT, 'JSON nesting exceeds rewrite stack') from exc
        after = encode(new) if new != parse(before) else before
        add_snapshot(root, files, relative, after, budget)
        if files[inside(root, relative)].before != before:
            raise ImportFailure(FailureCode.STALE_INPUT, relative)
    return PreparedImport(root, tuple(files.values()), copied, resolved, sum(counter.values()), tuple(paths[1:]))


def validate_current(plan: PreparedImport) -> None:
    fragments = tuple(sorted(p.relative_to(plan.root).as_posix() for p in (plan.root / 'dag/fragments').glob('*.json')))
    if fragments != plan.fragments:
        raise ImportFailure(FailureCode.STALE_INPUT, 'DAG fragment membership changed')
    budget = Budget()
    for item in plan.files:
        current = read_optional(inside(plan.root, item.relative), budget)
        if current != item.before:
            raise ImportFailure(FailureCode.STALE_INPUT, item.relative)


def stage_files(stage: Path, changes: tuple[Snapshot, ...]) -> None:
    journal: list[JSON] = []
    for index, item in enumerate(changes):
        if item.after is None:
            raise ImportFailure(FailureCode.INVALID_PLAN, 'deletion is not an import operation')
        (stage / f'{index}.new').write_bytes(item.after)
        if item.before is not None:
            (stage / f'{index}.old').write_bytes(item.before)
        journal.append({'path': item.relative, 'had_original': item.before is not None,
                        'new_sha256': hashlib.sha256(item.after).hexdigest(),
                        'old_sha256': hashlib.sha256(item.before).hexdigest() if item.before is not None else None})
    (stage / 'journal.json').write_bytes(encode({'schema': 'atlas_import_recovery.v1', 'files': journal}))


def rollback(root: Path, stage: Path, applied: list[tuple[int, Snapshot]], created: list[Path]) -> None:
    for index, item in reversed(applied):
        target = inside(root, item.relative)
        if read_optional(target, Budget()) != item.after:
            raise ImportFailure(FailureCode.RECOVERY, f'concurrent edit; originals retained at {stage}')
        if item.before is None:
            target.unlink()
        else:
            os.replace(stage / f'{index}.old', target)
    for directory in reversed(created):
        directory.rmdir()


def publish(plan: PreparedImport, stage: Path, changes: tuple[Snapshot, ...]) -> None:
    applied: list[tuple[int, Snapshot]] = []
    created: list[Path] = []
    try:
        for index, item in enumerate(changes):
            target = inside(plan.root, item.relative)
            if read_optional(target, Budget()) != item.before:
                raise ImportFailure(FailureCode.STALE_INPUT, item.relative)
            missing = []
            parent = target.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for directory in reversed(missing):
                directory.mkdir()
                created.append(directory)
            os.replace(stage / f'{index}.new', target)
            applied.append((index, item))
            if Budget().read(target) != item.after:
                raise OSError(f'published bytes differ: {item.relative}')
    except (OSError, ImportFailure) as exc:
        try:
            rollback(plan.root, stage, applied, created)
        except (OSError, ImportFailure) as recovery:
            raise ImportFailure(FailureCode.RECOVERY, f'{stage}; publish: {exc}; rollback: {recovery}') from recovery
        raise


def apply(plan: PreparedImport) -> None:
    """Apply a prepared snapshot. The lease and recovery stage survive interruption."""
    lock = plan.root / '.atlas-import.lock'
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise ImportFailure(FailureCode.BUSY, str(lock)) from exc
    stage: Path | None = None
    retain = False
    try:
        validate_current(plan)
        changes = tuple(item for item in plan.files if item.before != item.after)
        stage = Path(tempfile.mkdtemp(prefix='.atlas-import-stage-', dir=plan.root))
        stage_files(stage, changes)
        publish(plan, stage, changes)
    except ImportFailure as exc:
        retain = exc.code == FailureCode.RECOVERY
        raise
    except OSError as exc:
        raise ImportFailure(FailureCode.IO, str(exc)) from exc
    except BaseException:
        retain = True
        raise
    finally:
        if not retain:
            try:
                if stage is not None:
                    shutil.rmtree(stage)
                lock.rmdir()
            except OSError as exc:
                raise ImportFailure(FailureCode.RECOVERY, f'cleanup failed; inspect {lock} and {stage}: {exc}') from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', type=Path)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    try:
        plan = prepare(args.repo, parse(Budget().read(args.plan)))
        if args.write:
            apply(plan)
    except (ImportFailure, OSError) as exc:
        parser.exit(1, f'refusing: {exc}\n')
    print(json.dumps({'copied': plan.copied, 'resolved_to_existing': plan.resolved,
                      'references_rewritten': plan.rewrites, 'written': args.write}, sort_keys=True))


if __name__ == '__main__':
    main()
