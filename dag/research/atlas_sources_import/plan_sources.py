"""Prepare byte-custody plans for cited restored atlas files.

AuthorityEffect: None. Git parent-object bytes, restored bytes and existing twins
are compared exactly. Planning does not replay any archived proof or application.
All filesystem and Git failures refuse; nonmatching restored sources are explicit
row outcomes. Git is trusted, has a per-command deadline, and runs without hooks.
"""
from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from enum import Enum
import hashlib
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import os

# Explicit sibling module, including under the repository's required Python -I.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from import_sources import (Budget, FailureCode, ImportFailure, JSON, MAX_FILE,
                            encode, inside, mapping, normalise, parse, string)

COMMIT = '3379759468'
PREFIX = 'omega_engine_atlas/coda_atlas/F004_papers/'
FAMS = frozenset(('quantum_foundations', 'general_relativity', 'finite_quantum_mechanics',
                 'finite_to_continuum', 'fermion_sign_problem', 'majorana', 'mub6'))
LIVE = frozenset(('dag nodes/records/routes (derivation_dag.json)', 'dag fragments (sync inputs)',
    'code/**', 'papers/**', 'scripts/**', 'lean4/**', 'docs/**', 'problem_sets/**',
    'dag other (operads, research, pfp, tools)', 'other'))
MAX_TRACKED = 200000
TIMEOUT_SECONDS = 120


class Outcome(str, Enum):
    VERIFIED = 'verified'
    MISSING = 'missing_in_ana'
    NEWLINES = 'ana_newline_only_diff'
    DIFFERENT = 'ana_differs'


@dataclass(frozen=True)
class Configuration:
    repository: Path
    restored: Path
    sibling: Path
    removal_commit: str = COMMIT


@dataclass(frozen=True)
class Candidate:
    atlas_path: str
    family: str
    relative: str
    references: dict[str, JSON]


@dataclass(frozen=True)
class FileIndex:
    by_size: dict[int, tuple[str, ...]]
    by_name: dict[str, tuple[str, ...]]


def git(repository: Path, arguments: list[str], limit: int = MAX_FILE) -> bytes:
    """Bound returned data and execution time; close scratch output on all paths.

    Git object sizes are checked before requesting contents. The trusted Git
    process may temporarily spool its output to disk before the size check.
    """
    with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as errors:
        try:
            result = subprocess.run(['git', '-C', str(repository), *arguments], stdout=output,
                                    stderr=errors, timeout=TIMEOUT_SECONDS, check=False)
        except subprocess.TimeoutExpired as exc:
            raise ImportFailure(FailureCode.LIMIT, 'Git deadline exceeded') from exc
        errors.seek(0)
        diagnostic = errors.read(4096).decode('utf-8', 'replace')
        if result.returncode:
            raise ImportFailure(FailureCode.IO, f'Git exited {result.returncode}: {diagnostic}')
        output.seek(0)
        data = output.read(limit + 1)
        if len(data) > limit:
            raise ImportFailure(FailureCode.LIMIT, 'Git output exceeds limit')
        return data


def select(inventory: JSON) -> tuple[Candidate, ...]:
    paths = mapping(inventory).get('paths')
    if not isinstance(paths, list) or len(paths) > MAX_TRACKED:
        raise ImportFailure(FailureCode.INVALID_PLAN, 'inventory paths must be a bounded list')
    selected: dict[str, Candidate] = {}
    for value in paths:
        row = mapping(value)
        path = string(row, 'path')
        if not row.get('removed_in_commit') or row.get('removed_dir') or not path.startswith(PREFIX):
            continue
        tail = path[len(PREFIX):]
        family, separator, relative = tail.partition('/')
        if family not in FAMS:
            continue
        if not separator or not relative:
            raise ImportFailure(FailureCode.INVALID_PLAN, f'missing family-relative path: {path}')
        references = {k: v for k, v in mapping(row.get('referenced_from')).items() if k in LIVE}
        if references:
            if path in selected:
                raise ImportFailure(FailureCode.INVALID_PLAN, f'duplicate inventory source: {path}')
            selected[path] = Candidate(path, family, relative, references)
    if not selected:
        raise ImportFailure(FailureCode.INVALID_PLAN, 'no cited restored files selected')
    return tuple(selected[k] for k in sorted(selected))


def index_files(root: Path) -> FileIndex:
    raw = git(root, ['ls-files', '-z'])
    try:
        names = raw.decode('utf-8').split('\0')
    except UnicodeError as exc:
        raise ImportFailure(FailureCode.INVALID_PATH, 'tracked filenames must be UTF-8') from exc
    if len(names) > MAX_TRACKED:
        raise ImportFailure(FailureCode.LIMIT, 'too many tracked paths')
    by_name: dict[str, list[str]] = collections.defaultdict(list)
    by_size: dict[int, list[str]] = collections.defaultdict(list)
    for name in sorted(set(names)):
        if not name or name.startswith(('dag/results/', 'lean4/Imported/', 'sources/')):
            continue
        path = inside(root, name)
        if not path.is_file():
            raise ImportFailure(FailureCode.STALE_INPUT, f'tracked file unavailable: {name}')
        by_name[path.name].append(name)
        by_size[path.stat().st_size].append(name)
    return FileIndex({k: tuple(v) for k, v in by_size.items()}, {k: tuple(v) for k, v in by_name.items()})


def read_object(sibling: Path, parent: str, candidate: Candidate, budget: Budget) -> bytes:
    spec = f'{parent}:{candidate.atlas_path}'
    raw_size = git(sibling, ['cat-file', '-s', spec], 64).strip()
    if not raw_size.isdigit() or int(raw_size) > MAX_FILE:
        raise ImportFailure(FailureCode.LIMIT, f'Git object too large: {candidate.atlas_path}')
    data = git(sibling, ['show', spec])
    budget.charge(len(data))
    if len(data) != int(raw_size):
        raise ImportFailure(FailureCode.SOURCE_CHANGED, candidate.atlas_path)
    return data


def find_twin(root: Path, index: FileIndex, candidate: Candidate, data: bytes,
              budget: Budget) -> tuple[str, str] | None:
    for name in index.by_size.get(len(data), ()):
        if budget.read(inside(root, name)) == data:
            return 'identical', name
    for name in index.by_name.get(Path(candidate.relative).name, ()):
        if normalise(budget.read(inside(root, name))) == normalise(data):
            return 'newline_equivalent', name
    return None


def plan_row(config: Configuration, parent: str, index: FileIndex,
             candidate: Candidate, budget: Budget) -> dict[str, JSON]:
    restored = inside(config.restored, f'{candidate.family}/{candidate.relative}')
    data = read_object(config.sibling, parent, candidate, budget)
    row: dict[str, JSON] = {'atlas_path': candidate.atlas_path, 'family': candidate.family,
        'rel': candidate.relative, 'ana_path': str(restored), 'refs': candidate.references,
        'git_sha256': hashlib.sha256(data).hexdigest(), 'size': len(data), 'resolved_git_commit': parent}
    try:
        actual = budget.read(restored)
    except FileNotFoundError:
        row['status'] = Outcome.MISSING.value
        return row
    row['ana_sha256'] = hashlib.sha256(actual).hexdigest()
    if actual != data:
        row['status'] = Outcome.NEWLINES.value if normalise(actual) == normalise(data) else Outcome.DIFFERENT.value
        return row
    row['status'] = Outcome.VERIFIED.value
    twin = find_twin(config.repository, index, candidate, data, budget)
    if twin is not None:
        row['resolved_to_existing'] = {'match': twin[0], 'path': twin[1]}
    else:
        names = index.by_name.get(Path(candidate.relative).name, ())
        if names:
            row['in_repo_same_name_different_content'] = list(names)
    return row


def build_plan(config: Configuration, inventory: JSON) -> list[JSON]:
    if re.fullmatch('[0-9a-f]{7,40}', config.removal_commit) is None:
        raise ImportFailure(FailureCode.INVALID_PLAN, 'removal commit must be a hexadecimal Git id')
    config = Configuration(config.repository.resolve(strict=True), config.restored.resolve(strict=True),
                           config.sibling.resolve(strict=True), config.removal_commit)
    candidates = select(inventory)
    parent = git(config.sibling, ['rev-parse', '--verify', config.removal_commit + '^']).decode('ascii').strip()
    if re.fullmatch('[0-9a-f]{40}', parent) is None:
        raise ImportFailure(FailureCode.INVALID_PLAN, 'Git did not resolve an exact parent commit')
    index, budget = index_files(config.repository), Budget()
    return [plan_row(config, parent, index, candidate, budget) for candidate in candidates]


def write_plan(destination: Path, rows: list[JSON]) -> None:
    """Replace a plan atomically after complete validation and serialization."""
    data = encode(rows, 1)
    Budget().charge(len(data))
    with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.atlas-plan-', delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            stream.close()
            temporary.unlink()
            raise
    try:
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', type=Path)
    parser.add_argument('inventory', type=Path)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--ana', type=Path, default=Path('C:/.ana'))
    parser.add_argument('--sibling', type=Path, default=Path('C:/Users/a343o/source/repos/the_symbol_game'))
    args = parser.parse_args()
    try:
        rows = build_plan(Configuration(args.repo, args.ana, args.sibling), parse(Budget().read(args.inventory)))
        write_plan(args.plan, rows)
    except (ImportFailure, OSError, UnicodeError) as exc:
        parser.exit(1, f'refusing: {exc}\n')
    print(dict(collections.Counter(string(mapping(row), 'status') for row in rows)))


if __name__ == '__main__':
    main()
