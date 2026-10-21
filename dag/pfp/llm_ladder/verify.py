"""Host verification of a model's P0 mining answer, and classification of every failed claim.

AuthorityEffect: None. A claim counts only after the host has checked it locally:
  - a cited Lean, Rust or Python declaration must exist at the cited path (scan below; the Lean pattern
    is the one used by dag/pfp/generate_prompts.py);
  - a stated arity must match the declaration where the host can read it;
  - a relation or lemma that restates a source must not change the source's numerals (statement drift);
  - exact numeric claims are recomputed with Fractions;
  - a Lean skeleton must elaborate (`lake env lean` in lean4/ when the toolchain matches; otherwise the
    check is skipped with a recorded reason, never silently passed);
  - a composition must type-match two verified generators and be licensed by a verified relation.
Verification confirms that a name exists and a statement is consistent with its source. It does NOT
confirm that a generator's semantic predicate is the intended mathematics; that stays a P0 host review.

Failure classes (the `cls` field; each becomes a NEGATIVE operad entry, see memory.py):
  nonexistent_declaration  wrong_source_location  wrong_signature  statement_drift  false_numeric_claim
  vacuous_proof  unjustified_generalisation  lean_elaboration_failure  composition_type_mismatch
  composition_unlicensed  schema_violation  unparseable_reply  model_refusal
"""
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

from .llm_common import sha256_text

# Counterexample-type failures contradict a claim with a concrete host fact; the rest are failed compositions.
COUNTEREXAMPLE_CLASSES = {'false_numeric_claim', 'statement_drift', 'wrong_signature'}
G_CODES = {'schema_violation': 'G1_SCHEMA', 'unparseable_reply': 'G1_SCHEMA', 'nonexistent_declaration': 'G3_WITNESS',
           'wrong_source_location': 'G3_WITNESS', 'wrong_signature': 'G3_WITNESS', 'false_numeric_claim': 'G3_WITNESS',
           'lean_elaboration_failure': 'G3_WITNESS', 'composition_type_mismatch': 'G3_WITNESS',
           'composition_unlicensed': 'G3_WITNESS', 'statement_drift': 'G5_SCOPE', 'vacuous_proof': 'G5_SCOPE',
           'unjustified_generalisation': 'G5_SCOPE', 'model_refusal': 'G1_SCHEMA'}

SKIP_DIRS = {'.git', '.lake', 'target', 'node_modules', '__pycache__', 'results', '.claude', 'evidence', 'papers',
             'docs', 'problem_sets', 'rules', 'b', '.venv', 'venv'}
LEAN_DECLARATION = re.compile(
    r'^(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|partial|unsafe)\s+)*'
    r'(theorem|lemma|def|structure|inductive|class|abbrev|instance|axiom|opaque)\s+([^\s:({\[]+)')
RUST_DECLARATION = re.compile(
    r'^\s*(?:pub(?:\([^)]*\))?\s+)?(?:async\s+|const\s+|unsafe\s+)*(fn|struct|enum|trait|type|const|static|mod)\s+(\w+)')
NUMERAL = re.compile(r"(?<![A-Za-z_\d.'])\d+(?:\.\d+)?(?![A-Za-z_\d'])")
BACKTICKED = re.compile(r'`([A-Za-z_][A-Za-z0-9_.:]*[A-Za-z0-9_])`')


# --------------------------------------------------------------------------- declaration index
class DeclIndex:
    """Index of declarations in lean4/, code/, dag/, scripts/ (never dag/results).

    Scanning every file takes tens of seconds, so a tables-only cache keyed by (path, size, mtime) may be
    kept outside the repository (cache_path). Source lines are read on demand, never cached on disk.
    """

    ROOTS = ('lean4', 'code', 'dag', 'scripts')

    def __init__(self, root, *, cache_path=None):
        self.root = Path(root)
        self.cache_path = Path(cache_path) if cache_path else None
        self._files: dict = {}
        self._lines: dict = {}
        self._by_short: dict | None = None
        self._paths: list | None = None

    # ---- scanning
    def _scan_lean(self, text: str):
        stack, table = [], []
        for number, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            namespace = re.match(r'namespace\s+(\S+)', stripped)
            section = re.match(r'section(?:\s+(\S+))?\s*$', stripped)
            end = re.match(r'end(?:\s+(\S+))?\s*$', stripped)
            if namespace:
                stack.append(('ns', namespace.group(1)))
            elif section:
                stack.append(('sec', section.group(1) or ''))
            elif end and stack:
                stack.pop()
            match = LEAN_DECLARATION.match(line)
            if match and line[:1] not in (' ', '\t', '-'):
                kind, name = match.groups()
                prefix = '.'.join(n for k, n in stack if k == 'ns')
                full = name[len('_root_.'):] if name.startswith('_root_.') else (prefix + '.' + name if prefix else name)
                table.append({'kind': kind, 'name': name, 'full': full, 'line': number})
        return table

    def _scan_rust(self, text: str):
        table = []
        for number, line in enumerate(text.splitlines(), 1):
            match = RUST_DECLARATION.match(line)
            if match:
                kind, name = match.groups()
                table.append({'kind': kind, 'name': name, 'full': name, 'line': number})
        return table

    def _scan_python(self, text: str):
        table = []
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError, RecursionError):
            return table
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                arity = None
                if not isinstance(node, ast.ClassDef):
                    args = [a for a in node.args.posonlyargs + node.args.args if a.arg not in ('self', 'cls')]
                    arity = len(args) + len(node.args.kwonlyargs)
                table.append({'kind': 'class' if isinstance(node, ast.ClassDef) else 'def', 'name': node.name,
                              'full': node.name, 'line': node.lineno, 'arity': arity})
        return table

    def lines(self, relpath: str) -> list:
        lines = self._lines.get(relpath)
        if lines is None:
            if len(self._lines) > 64:
                self._lines.clear()
            lines = (self.root / relpath).read_bytes().decode('utf-8', errors='replace').splitlines()
            self._lines[relpath] = lines
        return lines

    def file_entry(self, relpath: str):
        entry = self._files.get(relpath)
        if entry is not None:
            return entry
        path = self.root / relpath
        if not path.is_file():
            return None
        suffix = path.suffix
        if suffix not in ('.lean', '.rs', '.py'):
            return None
        text = path.read_bytes().decode('utf-8', errors='replace')
        if suffix == '.lean':
            lang, table = 'lean', self._scan_lean(text)
        elif suffix == '.rs':
            lang, table = 'rust', self._scan_rust(text)
        else:
            lang, table = 'python', self._scan_python(text)
        entry = {'lang': lang, 'table': table}
        self._files[relpath] = entry
        return entry

    def source_paths(self) -> list:
        if self._paths is None:
            found = []
            for top in self.ROOTS:
                base = self.root / top
                if not base.is_dir():
                    continue
                for folder, dirs, files in os.walk(base):
                    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                    for name in files:
                        if name.endswith(('.lean', '.rs', '.py')):
                            found.append(os.path.relpath(os.path.join(folder, name), self.root).replace(os.sep, '/'))
            self._paths = sorted(found)
        return self._paths

    def by_short(self) -> dict:
        """short name -> [(path, decl)] over every source file (cached on disk when cache_path is set)."""
        if self._by_short is None:
            cache = {}
            if self.cache_path and self.cache_path.is_file():
                try:
                    cache = json.loads(self.cache_path.read_bytes().decode('utf-8'))
                except (OSError, ValueError):
                    cache = {}
            fresh, changed = {}, False
            for rel in self.source_paths():
                stat = (self.root / rel).stat()
                hit = cache.get(rel)
                if hit and hit[0] == stat.st_size and hit[1] == stat.st_mtime_ns:
                    self._files.setdefault(rel, {'lang': hit[2], 'table': hit[3]})
                    fresh[rel] = hit
                    continue
                entry = self.file_entry(rel)
                if entry is not None:
                    fresh[rel] = [stat.st_size, stat.st_mtime_ns, entry['lang'], entry['table']]
                    changed = True
            if self.cache_path and (changed or len(fresh) != len(cache)):
                try:
                    self.cache_path.parent.mkdir(parents=True, exist_ok=True)
                    self.cache_path.write_bytes(json.dumps(fresh).encode('utf-8'))
                except OSError:
                    pass
            index: dict = {}
            for rel, hit in fresh.items():
                for decl in hit[3]:
                    index.setdefault(decl['full'].split('.')[-1], []).append((rel, decl))
            self._by_short = index
        return self._by_short

    # ---- queries
    @staticmethod
    def match_in_table(table, name: str):
        tail = re.split(r'::|\.', name)
        hits = [d for d in table if d['full'] == name]
        if not hits:
            hits = [d for d in table if d['full'].split('.')[-len(tail):] == tail]
        if not hits:
            hits = [d for d in table if d['name'] == name or d['name'].split('.')[-1] == tail[-1]]
        return hits

    def find_anywhere(self, name: str) -> list:
        short = re.split(r'::|\.', name)[-1]
        return [(p, d) for p, d in self.by_short().get(short, [])]

    def window(self, relpath: str, decl: dict, span: int = 80) -> str:
        """Source text of one declaration: from its line to the next top-level declaration (max `span` lines)."""
        entry = self.file_entry(relpath)
        lines = self.lines(relpath)
        start = decl['line'] - 1
        later = [d['line'] - 1 for d in entry['table'] if d['line'] - 1 > start]
        stop = min([start + span] + later[:1])
        return '\n'.join(lines[start:stop])

    def statement(self, relpath: str, decl: dict) -> str:
        """The declaration's header: up to the first ':=' or ' where' (Lean) or the signature (Rust/Python)."""
        text = self.window(relpath, decl, span=14)
        for marker in (':=', ' where', '{'):
            if marker in text:
                text = text.split(marker, 1)[0]
                break
        return text.strip()


def default_cache_path(root) -> Path:
    """Outside the repository: the OS temp directory, one file per checkout."""
    return Path(tempfile.gettempdir()) / ('pfp_ladder_declindex_%s.json' % sha256_text(str(Path(root).resolve()))[:10])


KIND_WORDS = re.compile(r'^(?:theorem|lemma|def|abbrev|structure|inductive|class|instance|axiom|opaque|fn|struct|enum|trait|const)\s+')


def normalise_ref_fields(path, decl):
    """Format tolerance only: a model that copies a whole `path::decl` into one field, or a leading kind word, is
    read as it plainly meant (the leading identifier of the declaration field). The normalised citation is still checked
    in full: path, declaration and arity."""
    path = str(path or '').strip()
    decl = KIND_WORDS.sub('', str(decl or '').strip())
    if '::' in path:
        head, _, tail = path.partition('::')
        path, decl = head.strip(), (decl or KIND_WORDS.sub('', tail.strip()))
    if '::' in decl and re.search(r'\.(?:lean|rs|py)$', decl.split('::', 1)[0].strip()):
        head, _, tail = decl.partition('::')
        path, decl = path or head.strip(), tail.strip()
    lead = re.match(r"[A-Za-z_][\w.']*", decl)
    return path, (lead.group(0) if lead else decl)


def normalise_path(path: str):
    """Repository-relative POSIX path, or None for an absolute path or one that climbs out of the tree."""
    if not isinstance(path, str) or not path.strip():
        return None
    cleaned = path.strip().replace('\\', '/')
    while cleaned.startswith('./'):
        cleaned = cleaned[2:]
    if cleaned.startswith('/') or re.match(r'^[A-Za-z]:', cleaned) or '..' in cleaned.split('/'):
        return None
    return cleaned


# --------------------------------------------------------------------------- arity
def _split_top_level(text: str):
    """Yield (char, depth) for each char of text, tracking ()[]{}⟨⟩ depth."""
    depth = 0
    for index, ch in enumerate(text):
        if ch in '([{⟨':
            yield index, ch, depth
            depth += 1
        elif ch in ')]}⟩':
            depth = max(0, depth - 1)
            yield index, ch, depth
        else:
            yield index, ch, depth


def lean_arity_candidates(header: str):
    """Explicit-binder count, and that plus the top-level arrows of the conclusion. Heuristic."""
    binders, conclusion_start = 0, None
    for index, ch, depth in _split_top_level(header):
        if ch == '(' and depth == 0:
            close = header.find(')', index)
            group = header[index + 1: close if close > 0 else len(header)]
            if ':' in group:
                names = group.split(':', 1)[0].split()
                binders += len([n for n in names if n and n != '_'] or [''])
        elif ch == ':' and depth == 0 and conclusion_start is None:
            conclusion_start = index + 1
    arrows = 0
    if conclusion_start is not None:
        tail = header[conclusion_start:]
        for index, ch, depth in _split_top_level(tail):
            if depth == 0 and (ch == '→' or tail[index: index + 2] == '->'):
                arrows += 1
    return binders, binders + arrows


def rust_arity(header: str):
    match = re.search(r'\(([^)]*)\)', header, re.S)
    if not match:
        return None
    params = [p.strip() for p in re.split(r',(?![^<]*>)', match.group(1)) if p.strip()]
    return len([p for p in params if not re.match(r'^&?(?:mut\s+)?self\b', p)])


def check_arity(index: DeclIndex, relpath: str, decl: dict, claimed):
    """None when consistent or unknowable, else an evidence string."""
    if not isinstance(claimed, int) or isinstance(claimed, bool):
        return None
    entry = index.file_entry(relpath)
    if entry['lang'] == 'python':
        if decl.get('arity') is not None and decl['arity'] != claimed:
            return 'python def %s takes %d parameters; the claim says %d' % (decl['name'], decl['arity'], claimed)
        return None
    header = index.statement(relpath, decl)
    if entry['lang'] == 'rust' and decl['kind'] == 'fn':
        actual = rust_arity(header)
        if actual is not None and actual != claimed:
            return 'rust fn %s takes %d parameters; the claim says %d' % (decl['name'], actual, claimed)
        return None
    if entry['lang'] == 'lean' and decl['kind'] in ('theorem', 'lemma', 'def', 'abbrev'):
        low, high = lean_arity_candidates(header)
        if claimed not in (low, high):
            return ('lean %s %s has %d explicit binders (%d with conclusion arrows); the claim says %d '
                    '(heuristic count)' % (decl['kind'], decl['name'], low, high, claimed))
    return None


# --------------------------------------------------------------------------- numerals and statements
def numerals(text: str) -> set:
    return set(NUMERAL.findall(text or ''))


def statement_drift(claim: str, *sources: str):
    """None, or an evidence string naming the numerals the claim introduces that no source contains."""
    allowed = {'0', '1'}
    for source in sources:
        allowed |= numerals(source)
    foreign = sorted(n for n in numerals(claim) if n not in allowed)
    if foreign:
        return 'numerals %s appear in the claim but in none of the checked sources (heuristic)' % ', '.join(foreign)
    return None


def normalise_pattern(text: str) -> str:
    text = re.sub(r'\d+(?:\.\d+)?', '#', (text or '').lower())
    text = re.sub(r'[^a-z#_/ ]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()[:160]


_ALLOWED_BINOPS = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
                   ast.Div: lambda a, b: a / b}


def safe_fraction(expr: str) -> Fraction:
    """Exact value of an arithmetic expression over integers, decimals, + - * / and integer powers."""
    text = (expr or '').strip().replace('^', '**').replace('×', '*').replace('−', '-').replace('÷', '/')
    text = text.replace('·', '*')
    if len(text) > 200:
        raise ValueError('expression too long')

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return Fraction(repr(node.value)) if isinstance(node.value, float) else Fraction(node.value)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            value = walk(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
            return _ALLOWED_BINOPS[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            base, exponent = walk(node.left), walk(node.right)
            if exponent.denominator != 1 or abs(exponent) > 64 or abs(base) > 10 ** 6:
                raise ValueError('power out of range')
            return base ** int(exponent)
        raise ValueError('unsupported syntax in numeric claim')

    return walk(ast.parse(text, mode='eval'))


def parse_value(value: str) -> Fraction:
    return safe_fraction(str(value))


# --------------------------------------------------------------------------- Lean
class LeanRunner:
    """Elaborate a snippet with `lake env lean` in lean4/. Skips, with a recorded reason, when it cannot."""

    ENV_PROBLEMS = re.compile(r'unknown package|unknown module prefix|object file .* does not exist|'
                              r'no such file or directory|failed to (?:read|load) (?:file|olean)|could not resolve', re.I)

    def __init__(self, root, *, run=None, which=shutil.which, timeout=240):
        self.root, self.timeout, self._run, self._which = Path(root), timeout, run, which
        self._status = None

    def availability(self):
        """(bool, reason). Requires `lean --version` to name the version in lean4/lean-toolchain."""
        if self._status is not None:
            return self._status
        toolchain = self.root / 'lean4' / 'lean-toolchain'
        lean, lake = self._which('lean'), self._which('lake')
        if not lean or not lake:
            home = Path.home() / '.elan' / 'bin'
            lean = lean or (str(home / 'lean') if (home / 'lean').exists() or (home / 'lean.exe').exists() else None)
            lake = lake or (str(home / 'lake') if (home / 'lake').exists() or (home / 'lake.exe').exists() else None)
        if not toolchain.is_file():
            self._status = (False, 'lean4/lean-toolchain missing')
        elif not lean or not lake:
            self._status = (False, 'lean or lake not found on PATH or in ~/.elan/bin')
        else:
            wanted = re.search(r'v?(\d+\.\d+\.\d+(?:-rc\d+)?)', toolchain.read_text(encoding='utf-8'))
            try:
                proc = (self._run or subprocess.run)([lean, '--version'], capture_output=True, text=True, timeout=60)
                reported = proc.stdout + proc.stderr
            except (OSError, subprocess.TimeoutExpired) as error:
                self._status = (False, 'lean --version failed: ' + type(error).__name__)
                return self._status
            if wanted and wanted.group(1) in reported:
                self._status = (True, 'lean %s matches lean4/lean-toolchain' % wanted.group(1))
                self._lean, self._lake = lean, lake
            else:
                found = re.search(r'version\s+(\S+)', reported)
                self._status = (False, 'installed lean %s does not match lean4/lean-toolchain %s (toolchain check)' % (
                    found.group(1).rstrip(',') if found else '?', wanted.group(1) if wanted else '?'))
        return self._status

    def elaborate(self, snippet: str) -> dict:
        ok, reason = self.availability()
        if not ok:
            return {'status': 'skipped', 'reason': reason}
        scratch = Path(tempfile.mkdtemp(prefix='ladder-lean-'))
        try:
            source = scratch / 'Snippet.lean'
            source.write_bytes(snippet.replace('\r\n', '\n').encode('utf-8'))
            try:
                proc = (self._run or subprocess.run)([self._lake, 'env', self._lean, str(source)], cwd=str(self.root / 'lean4'),
                                                      capture_output=True, text=True, timeout=self.timeout)
            except subprocess.TimeoutExpired:
                return {'status': 'skipped', 'reason': 'lean timed out after %ds' % self.timeout}
            except OSError as error:
                return {'status': 'skipped', 'reason': 'lean could not start: ' + type(error).__name__}
            output = (proc.stdout or '') + (proc.stderr or '')
            errors = [l for l in output.splitlines() if re.search(r'\berror\b', l)]
            if errors and any(self.ENV_PROBLEMS.search(l) for l in errors):
                return {'status': 'skipped', 'reason': 'lean environment incomplete: ' + errors[0][:160]}
            return {'status': 'ok' if proc.returncode == 0 and not errors else 'failed', 'errors': errors[:6],
                    'sorry': 'sorry' in output, 'returncode': proc.returncode}
        finally:
            shutil.rmtree(scratch, ignore_errors=True)


# --------------------------------------------------------------------------- report objects
@dataclass
class Failure:
    cls: str
    claim_id: str
    claim_kind: str
    claim: str
    evidence: str
    decl_key: str | None = None
    confidence: str = 'exact'

    @property
    def entry_type(self) -> str:
        return 'counterexample' if self.cls in COUNTEREXAMPLE_CLASSES else 'failed_composition'

    @property
    def pattern(self) -> str:
        base = self.decl_key if self.decl_key and self.cls in ('nonexistent_declaration', 'wrong_source_location') \
            else normalise_pattern(self.claim)
        return self.cls + ':' + base


@dataclass
class VerifyReport:
    parsed: bool = False
    schema_errors: list = field(default_factory=list)
    verified: dict = field(default_factory=lambda: {'generators': [], 'relations': [], 'compositions': [],
                                                    'lemmas': [], 'numeric': []})
    failures: list = field(default_factory=list)
    unverifiable: list = field(default_factory=list)
    lean: dict = field(default_factory=lambda: {'status': 'not_needed', 'reason': 'no Lean skeleton in the reply'})
    claims: int = 0

    def verified_total(self) -> int:
        return sum(len(v) for v in self.verified.values())

    def failure_total(self) -> int:
        return len(self.failures)

    def failure_rate(self) -> float:
        denominator = self.verified_total() + self.failure_total()
        return self.failure_total() / denominator if denominator else 1.0

    def by_class(self) -> dict:
        counts: dict = {}
        for failure in self.failures:
            counts[failure.cls] = counts.get(failure.cls, 0) + 1
        return dict(sorted(counts.items()))


# --------------------------------------------------------------------------- schema subset validator
def validate_schema(value, schema, path='$'):
    """Errors for the JSON-schema subset the ladder uses (type, enum, required, properties, items)."""
    errors = []
    kind = schema.get('type')
    checks = {'object': dict, 'array': list, 'string': str, 'integer': int, 'boolean': bool}
    if kind in checks:
        wrong = not isinstance(value, checks[kind]) or (kind == 'integer' and isinstance(value, bool))
        if wrong:
            return ['%s: expected %s' % (path, kind)]
    if 'enum' in schema and value not in schema['enum']:
        errors.append('%s: %r not in enum' % (path, value if not isinstance(value, str) else value[:40]))
    if kind == 'object':
        for key in schema.get('required', []):
            if key not in value:
                errors.append('%s: missing %s' % (path, key))
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            for key in value:
                if key not in props:
                    errors.append('%s: unexpected %s' % (path, key))
        for key, sub in props.items():
            if key in value:
                errors += validate_schema(value[key], sub, path + '.' + key)
    elif kind == 'array':
        for position, item in enumerate(value):
            errors += validate_schema(item, schema.get('items', {}), '%s[%d]' % (path, position))
    return errors


# --------------------------------------------------------------------------- the verifier
class Verifier:
    def __init__(self, root, *, index: DeclIndex | None = None, lean: LeanRunner | None = None, run_lean=True):
        self.root = Path(root)
        self.index = index or DeclIndex(root)
        self.lean = lean or LeanRunner(root)
        self.run_lean = run_lean

    # ---- reference check ------------------------------------------------
    def check_ref(self, ref, claimed_arity=None):
        """('ok', info) | ('unchecked', reason) | ('fail', cls, evidence, decl_key)."""
        if not isinstance(ref, dict) or ref.get('status') in (None, 'none', 'proposed_new'):
            return 'unchecked', 'no existing declaration cited'
        path_text, decl_name = normalise_ref_fields(ref.get('path'), ref.get('decl'))
        if not decl_name:
            return 'unchecked', 'no declaration name'
        key = decl_name
        relpath = normalise_path(path_text)
        if relpath is None:
            elsewhere = self.index.find_anywhere(decl_name)
            if elsewhere:
                return 'fail', 'wrong_source_location', 'path %r is not a repository-relative path; %s exists at %s' % (
                    str(ref.get('path'))[:80], decl_name, elsewhere[0][0]), key
            return 'fail', 'nonexistent_declaration', 'path %r is not a repository-relative path and no declaration %s was found' % (
                str(ref.get('path'))[:80], decl_name), key
        entry = self.index.file_entry(relpath)
        if entry is None:
            elsewhere = self.index.find_anywhere(decl_name)
            if elsewhere:
                return 'fail', 'wrong_source_location', 'no file %s; declaration %s exists at %s' % (relpath, decl_name, elsewhere[0][0]), key
            return 'fail', 'nonexistent_declaration', 'no file %s and no indexed declaration named %s' % (relpath, decl_name), key
        hits = self.index.match_in_table(entry['table'], decl_name)
        if not hits:
            elsewhere = self.index.find_anywhere(decl_name)
            if elsewhere:
                return 'fail', 'wrong_source_location', '%s has no declaration %s; it exists at %s' % (relpath, decl_name, elsewhere[0][0]), key
            return 'fail', 'nonexistent_declaration', '%s has no declaration %s and none exists in the indexed sources' % (relpath, decl_name), key
        decl = hits[0]
        problem = check_arity(self.index, relpath, decl, claimed_arity)
        if problem:
            return 'fail', 'wrong_signature', problem, key
        return 'ok', {'path': relpath, 'decl': decl['full'], 'kind': decl['kind'], 'line': decl['line'],
                      'lang': entry['lang'], 'window': self.index.window(relpath, decl)}

    # ---- helpers --------------------------------------------------------
    def _prose_names(self, text, known_text):
        """Backticked identifiers in prose that exist nowhere: (name, evidence) pairs (heuristic)."""
        bad = []
        for name in set(BACKTICKED.findall(text or '')):
            looks_like_decl = ('_' in name or '.' in name or '::' in name or re.search(r'[a-z][A-Z]', name)) and len(name) > 4
            if not looks_like_decl or name in (known_text or '') or '.' in name and name.endswith(('.lean', '.rs', '.py')):
                continue
            if not self.index.find_anywhere(name):
                bad.append(name)
        return bad

    # ---- main entry -----------------------------------------------------
    def verify_p0(self, response, schema, *, target_statement='') -> VerifyReport:
        report = VerifyReport()
        if not isinstance(response, dict):
            report.failures.append(Failure('unparseable_reply', 'reply', 'reply', 'reply is not a JSON object', 'no object'))
            return report
        report.parsed = True
        errors = validate_schema(response, schema)
        report.schema_errors = errors[:20]
        known = target_statement
        valid_ids = {'generators': {}, 'relations': {}}
        item_schemas = {k: schema['properties'][k]['items'] for k in
                        ('generators', 'relations', 'compositions', 'lemmas', 'near_misses', 'numeric_claims')}

        def items(key):
            raw = response.get(key)
            if not isinstance(raw, list):
                if key in response or key in schema.get('required', []):
                    report.failures.append(Failure('schema_violation', key, key, '%s is not an array' % key, 'expected array'))
                return []
            good = []
            for position, item in enumerate(raw):
                problems = validate_schema(item, item_schemas[key], '%s[%d]' % (key, position))
                if problems:
                    claim_id = item.get('id') if isinstance(item, dict) and isinstance(item.get('id'), str) else '%s[%d]' % (key, position)
                    report.failures.append(Failure('schema_violation', claim_id, key, str(item)[:160], '; '.join(problems[:3])))
                else:
                    good.append(item)
            report.claims += len(raw)
            return good

        # generators
        for gen in items('generators'):
            status, *rest = self.check_ref(gen['ref'], gen.get('arity'))
            claim = '%s: (%s) -> %s [%s]' % (gen['id'], ', '.join(gen['inputs']), gen['output'], gen['ref'].get('decl', ''))
            if status == 'fail':
                cls, evidence, key = rest
                report.failures.append(Failure(cls, gen['id'], 'generator', claim, evidence, key))
            elif status == 'unchecked':
                report.unverifiable.append({'id': gen['id'], 'kind': 'generator', 'reason': rest[0]})
            else:
                info = rest[0]
                known += '\n' + info['window']
                valid_ids['generators'][gen['id']] = gen
                report.verified['generators'].append({**gen, 'host_evidence': {k: info[k] for k in ('path', 'decl', 'kind', 'line', 'lang')},
                                                      'evidence_status': 'declaration_exists_semantics_unreviewed'})
        # relations
        for rel in items('relations'):
            status, *rest = self.check_ref(rel['ref'])
            claim = '%s: %s [%s]' % (rel['id'], rel['statement'], rel['ref'].get('decl', ''))
            if status == 'fail':
                cls, evidence, key = rest
                report.failures.append(Failure(cls, rel['id'], 'relation', claim, evidence, key))
                continue
            if status == 'unchecked':
                report.unverifiable.append({'id': rel['id'], 'kind': 'relation', 'reason': rest[0]})
                continue
            info = rest[0]
            drift = statement_drift(rel['statement'], info['window'], target_statement)
            names = self._prose_names(rel['statement'], info['window'] + target_statement)
            if drift:
                report.failures.append(Failure('statement_drift', rel['id'], 'relation', claim, drift, rel['ref'].get('decl'), 'heuristic'))
            elif names:
                report.failures.append(Failure('nonexistent_declaration', rel['id'], 'relation', claim,
                                               'statement cites %s, which exists nowhere in the indexed sources (heuristic)' % ', '.join(sorted(names)),
                                               sorted(names)[0], 'heuristic'))
            else:
                valid_ids['relations'][rel['id']] = rel
                report.verified['relations'].append({**rel, 'host_evidence': {k: info[k] for k in ('path', 'decl', 'kind', 'line', 'lang')},
                                                     'evidence_status': 'declaration_exists_statement_consistent_semantics_unreviewed'})
        # compositions
        for comp in items('compositions'):
            claim = '%s . slot %d <- %s via %s' % (comp['outer'], comp['slot'], comp['inner'], comp['licensing_relation'])
            outer, inner = valid_ids['generators'].get(comp['outer']), valid_ids['generators'].get(comp['inner'])
            if outer is None or inner is None:
                missing = [n for n, g in (('outer', outer), ('inner', inner)) if g is None]
                report.failures.append(Failure('composition_type_mismatch', claim, 'composition', claim,
                                               'the %s generator%s not a verified generator of this reply' % (' and '.join(missing), ' is' if len(missing) == 1 else 's are')))
                continue
            slot = comp['slot']
            if not 0 <= slot < len(outer['inputs']) or _norm(outer['inputs'][slot]) != _norm(inner['output']):
                have = outer['inputs'][slot] if 0 <= slot < len(outer['inputs']) else 'no such slot'
                report.failures.append(Failure('composition_type_mismatch', claim, 'composition', claim,
                                               'output colour %r of %s does not match input colour %r (slot %d) of %s' % (
                                                   inner['output'], comp['inner'], have, slot, comp['outer'])))
                continue
            if comp['licensing_relation'] not in valid_ids['relations']:
                report.failures.append(Failure('composition_unlicensed', claim, 'composition', claim,
                                               'licensing relation %r is not a verified relation of this reply; matching colours alone is insufficient' % comp['licensing_relation']))
                continue
            report.verified['compositions'].append({**comp, 'evidence_status': 'colours_match_and_licensed_by_verified_relation'})
        # numeric claims
        for num in items('numeric_claims'):
            claim = '%s: %s = %s' % (num['id'], num['expr'], num['value'])
            try:
                computed, stated = safe_fraction(num['expr']), parse_value(num['value'])
            except (ValueError, SyntaxError, ZeroDivisionError, RecursionError):
                report.unverifiable.append({'id': num['id'], 'kind': 'numeric', 'reason': 'expression not exactly evaluable'})
                continue
            if computed != stated:
                report.failures.append(Failure('false_numeric_claim', num['id'], 'numeric', claim,
                                               'exact recomputation gives %s, not %s' % (computed, stated)))
            else:
                report.verified['numeric'].append({**num, 'host_evidence': {'recomputed': str(computed)}})
        # lemmas (statement checks; Lean last)
        pending_lean = []
        for lem in items('lemmas'):
            claim = '%s: %s' % (lem['id'], lem['statement'])
            ref = lem.get('ref') or {}
            relation = lem['relation_to_target']
            info = None
            if ref.get('status') == 'existing':
                status, *rest = self.check_ref(ref)
                if status == 'fail':
                    cls, evidence, key = rest
                    report.failures.append(Failure(cls, lem['id'], 'lemma', claim, evidence, key))
                    continue
                info = rest[0] if status == 'ok' else None  # 'unchecked' carries a reason string, not a declaration
            skeleton = lem.get('lean_skeleton', '') or ''
            vacuous = None
            if lem.get('claims_proved'):
                if not skeleton.strip():
                    vacuous = 'claims_proved is true but no Lean text is given'
                elif re.search(r'\b(sorry|admit)\b', skeleton):
                    vacuous = 'claims_proved is true but the Lean text contains sorry/admit'
                elif re.search(r'^\s*axiom\b', skeleton, re.M):
                    vacuous = 'the Lean text introduces an axiom instead of proving the statement'
            if not vacuous and (re.search(r':\s*True\b', skeleton)
                                or re.search(r'(?:theorem|lemma)\s+\S+[^:]*:\s*(\w+)\s*=\s*\1\s*:=', skeleton)):
                vacuous ='the Lean statement is a tautology (True or x = x), so it does not state the lemma'
            if vacuous:
                report.failures.append(Failure('vacuous_proof', lem['id'], 'lemma', claim, vacuous))
                continue
            if relation in ('restates', 'implies'):
                sources = [target_statement] + ([info['window']] if info else [])
                drift = statement_drift(lem['statement'], *sources)
                if drift:
                    report.failures.append(Failure('statement_drift', lem['id'], 'lemma', claim, drift, ref.get('decl') or None, 'heuristic'))
                    continue
            if relation in ('strengthens',) and not info:
                report.failures.append(Failure('unjustified_generalisation', lem['id'], 'lemma', claim,
                                               'the lemma strengthens the target but cites no verified existing declaration that justifies it'))
                continue
            names = self._prose_names(lem['statement'], target_statement + (info['window'] if info else ''))
            if names:
                report.failures.append(Failure('nonexistent_declaration', lem['id'], 'lemma', claim,
                                               'statement cites %s, which exists nowhere in the indexed sources (heuristic)' % ', '.join(sorted(names)),
                                               sorted(names)[0], 'heuristic'))
                continue
            if skeleton.strip():
                pending_lean.append((lem, claim, skeleton))
            else:
                report.unverifiable.append({'id': lem['id'], 'kind': 'lemma', 'reason': 'no Lean skeleton; statement consistent with sources but not elaborated'})
        if pending_lean and self.run_lean:
            available, reason = self.lean.availability()
            report.lean = {'status': 'ran' if available else 'skipped', 'reason': reason}
            for lem, claim, skeleton in pending_lean:
                if not available:
                    report.unverifiable.append({'id': lem['id'], 'kind': 'lemma', 'reason': 'Lean elaboration skipped: ' + reason})
                    continue
                outcome = self.lean.elaborate(skeleton)
                if outcome['status'] == 'skipped':
                    report.lean = {'status': 'skipped', 'reason': outcome['reason']}
                    report.unverifiable.append({'id': lem['id'], 'kind': 'lemma', 'reason': 'Lean elaboration skipped: ' + outcome['reason']})
                elif outcome['status'] == 'ok':
                    report.verified['lemmas'].append({**lem, 'host_evidence': {'lean': 'elaborates', 'sorry_in_output': outcome.get('sorry', False)},
                                                      'evidence_status': 'statement_elaborates_proof_not_claimed' if outcome.get('sorry') else 'lean_elaborates'})
                else:
                    unknown = re.search(r"unknown (?:identifier|constant) '([^']+)'", ' '.join(outcome['errors']))
                    if unknown:
                        report.failures.append(Failure('nonexistent_declaration', lem['id'], 'lemma', claim,
                                                       'Lean: ' + outcome['errors'][0][:200], unknown.group(1)))
                    else:
                        report.failures.append(Failure('lean_elaboration_failure', lem['id'], 'lemma', claim,
                                                       'Lean: ' + (outcome['errors'][0][:200] if outcome['errors'] else 'nonzero exit')))
        elif pending_lean:
            report.lean = {'status': 'skipped', 'reason': 'Lean elaboration disabled by the caller'}
            for lem, _, _ in pending_lean:
                report.unverifiable.append({'id': lem['id'], 'kind': 'lemma', 'reason': 'Lean elaboration disabled'})
        for miss in items('near_misses'):
            report.unverifiable.append({'id': miss['id'], 'kind': 'near_miss', 'reason': 'semantic near miss; P4 host check decides'})
        return report


def _norm(colour: str) -> str:
    return re.sub(r'\s+', '', str(colour)).lower()


def claim_fingerprint(failure: Failure) -> str:
    return sha256_text(failure.pattern)[:12]
