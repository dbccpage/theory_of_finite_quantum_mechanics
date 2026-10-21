"""Check that every reference in the pre-genesis to WDP fragment resolves.

For each record: every non-absent witness names an existing file whose text
declares the symbol (Lean, Rust or Python declaration forms; other files by
substring); every cited source names an existing file whose cited line range
contains the quoted text (whitespace-normalized); every coda atlas path exists.
A record whose paper or node status is PROVED_LEAN must cite a Lean declaration
that is not an axiom and whose body holds no sorry or admit.

Roots: local is this checkout; symbol_game is the sibling the_symbol_game
checkout (or TFQ_SYMBOL_GAME_ROOT); github19l is dbccpage/19L57G1 at the pinned
commit, fetched with `gh api` only when --network is given.
AuthorityEffect: None. Resolution is not a check that any statement is true.
Usage: python -B dag/verify_pregenesis_to_wdp_citations.py [--manifest PATH] [--network]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = HERE / 'fragments/pregenesis_to_wdp.json'
LEAN_DECL = (r'^[ \t]*(?:@\[[^\]\n]*\][ \t]*)?(?:(?:private|protected|noncomputable|partial|unsafe)[ \t]+)*'
             r'(theorem|lemma|def|abbrev|structure|inductive|class|instance|opaque|axiom)[ \t]+(?:[\w.]+\.)?')
LEAN_STOP = re.compile(r'^(theorem|lemma|def|abbrev|structure|inductive|class|instance|end|namespace|section|'
                       r'example|noncomputable|private|protected|open|@\[|/--|#)', re.M)


def symbol_game_root() -> Path | None:
    env = os.environ.get('TFQ_SYMBOL_GAME_ROOT')
    if env:
        return Path(env)
    for parent in ROOT.parents:
        candidate = parent / 'the_symbol_game'
        if (candidate / 'omega_engine_atlas').is_dir():
            return candidate
    return None


class Files:
    def __init__(self, network: bool, commit: str):
        self.network = network
        self.commit = commit
        self.sg = symbol_game_root()
        self.cache: dict[tuple[str, str], str | None] = {}

    def text(self, root: str, path: str) -> str | None:
        key = (root, path)
        if key in self.cache:
            return self.cache[key]
        value = None
        if root == 'local':
            p = ROOT / path
            value = p.read_text(encoding='utf-8', errors='replace') if p.is_file() else None
        elif root == 'symbol_game' and self.sg is not None:
            p = self.sg / path
            value = p.read_text(encoding='utf-8', errors='replace') if p.is_file() else None
        elif root == 'github19l' and self.network:
            run = subprocess.run(
                ['gh', 'api', '-H', 'Accept: application/vnd.github.raw',
                 f'repos/dbccpage/19L57G1/contents/{path}?ref={self.commit}'],
                capture_output=True)
            value = run.stdout.decode('utf-8', errors='replace') if run.returncode == 0 else None
        self.cache[key] = value
        return value

    def skipped(self, root: str) -> bool:
        return (root == 'github19l' and not self.network) or (root == 'symbol_game' and self.sg is None)


def declares(text: str, path: str, symbol: str) -> tuple[bool, str]:
    """Whether the file declares `symbol`; returns the Lean declaration body when it does."""
    leaf = symbol.split('::')[-1].split('.')[-1]
    if path.endswith('.lean'):
        m = re.search(LEAN_DECL + re.escape(leaf) + r"(?![\w'])", text, re.M)
        if not m:
            return False, ''
        stop = LEAN_STOP.search(text, m.end())
        return True, text[m.start(): stop.start() if stop else len(text)]
    if path.endswith('.rs'):
        return bool(re.search(r'\b(fn|struct|enum|trait|type|const|static|mod)\s+' + re.escape(leaf) + r'\b',
                              text)), ''
    if path.endswith('.py'):
        return bool(re.search(r'^\s*(def|class)\s+' + re.escape(leaf) + r'\b|^' + re.escape(leaf) + r'\s*=',
                              text, re.M)), ''
    return leaf in text, ''


def norm(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def check(manifest, files: Files) -> tuple[list[str], int]:
    errs: list[str] = []
    skipped = 0
    for r in manifest['records']:
        rid = r['id']
        proved = r['record_status'] == 'PROVED_LEAN' or (r.get('dag') or {}).get('status') == 'PROVED_LEAN'
        proved_lean_ok = False
        for tier in ('lean', 'rust', 'python'):
            for e in r['witnesses'].get(tier, []):
                if 'absent' in e:
                    continue
                if files.skipped(e['root']):
                    skipped += 1
                    continue
                text = files.text(e['root'], e['path'])
                if text is None:
                    errs.append(f'{rid}: {tier} file missing: {e["root"]}:{e["path"]}')
                    continue
                if not e.get('symbol'):
                    continue
                ok, body = declares(text, e['path'], e['symbol'])
                if not ok:
                    errs.append(f'{rid}: {tier} symbol {e["symbol"]} not declared in {e["path"]}')
                    continue
                if tier == 'lean' and e['path'].endswith('.lean') and e['root'] != 'github19l':
                    code = re.sub(r'/-.*?-/|--[^\n]*', '', body, flags=re.S)
                    bad = re.match(r'\s*(?:@\[[^\]]*\]\s*)?(?:\w+\s+)*axiom\b', code) or \
                        re.search(r'\b(sorry|admit)\b', code)
                    if bad:
                        errs.append(f'{rid}: lean {e["symbol"]} is an axiom or holds sorry/admit')
                    else:
                        proved_lean_ok = True
        if proved and not proved_lean_ok and not files.skipped('symbol_game'):
            errs.append(f'{rid}: PROVED_LEAN without a resolved, sorry-free Lean declaration')
        for s in r.get('sources', []):
            if files.skipped(s['root']):
                skipped += 1
                continue
            text = files.text(s['root'], s['path'])
            if text is None:
                errs.append(f'{rid}: source file missing: {s["root"]}:{s["path"]}')
                continue
            lines = text.splitlines()
            a, _, b = s['lines'].partition('-')
            lo, hi = int(a), int(b or a)
            if not 1 <= lo <= hi <= len(lines):
                errs.append(f'{rid}: source lines {s["lines"]} outside {s["path"]} ({len(lines)} lines)')
                continue
            if norm(s['quote']) not in norm('\n'.join(lines[lo - 1:hi])):
                errs.append(f'{rid}: quote not found in {s["path"]}:{s["lines"]}: {s["quote"][:70]!r}')
        for p in r.get('coda_atlas_paths', []):
            if files.sg is not None and not (files.sg / p).exists():
                errs.append(f'{rid}: coda atlas path missing: {p}')
    return errs, skipped


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=MANIFEST)
    parser.add_argument('--network', action='store_true', help='fetch github19l files with gh api')
    args = parser.parse_args(argv)
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    commit = json.loads(MANIFEST.read_text(encoding='utf-8'))['external_roots']['github19l']['commit']
    files = Files(args.network, commit)
    errs, skipped = check(manifest, files)
    for err in errs:
        print('FAIL', err)
    print(f'records={len(manifest["records"])} failures={len(errs)} skipped_refs={skipped} '
          f'symbol_game={"found" if files.sg else "absent"} network={args.network}')
    return int(bool(errs))


if __name__ == '__main__':
    sys.exit(main())
