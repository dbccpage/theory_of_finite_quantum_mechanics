"""Plan the atlas-sources import: which cited files of the seven restored F004 families are already in the repo.

AuthorityEffect: None. Reads the inventory written by dag/research/lean_replay_campaign/atlas_inventory.py, the
restored families under --ana and the sibling git history. Reads nothing under --ana except the cited files.

    python -I -X utf8 plan_sources.py <repo> <inventory.json> <plan.json> [--ana C:\\.ana] [--sibling <the_symbol_game>]

For each file the repository cites in one of the families it checks, in this order:
  1. the --ana copy against `git show <commit>^:<path>` in the sibling repo (sha256);
  2. an identical file (sha256) elsewhere in this repository (not dag/results, lean4/Imported, sources/);
  3. a newline-equivalent file of the same name (sha256 of the LF-normalised bytes);
  4. otherwise the file has to be copied; a same-named file with different content is recorded as an edition
     difference and is not substituted.
"""
import argparse, collections, hashlib, json, os, subprocess

COMMIT = '3379759468'
PREFIX = 'omega_engine_atlas/coda_atlas/F004_papers/'
FAMS = ['003_quantum_foundations', '004_general_relativity', '006_finite_qm', '007_finite_to_continuum',
        '008_fsp', '009_ms_majorana', '010_mub6']
LIVE = ("dag nodes/records/routes (derivation_dag.json)", "dag fragments (sync inputs)", "code/**", "papers/**",
        "scripts/**", "lean4/**", "docs/**", "problem_sets/**", "dag other (operads, research, pfp, tools)", "other")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(b):
    return b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo')
    ap.add_argument('inventory')
    ap.add_argument('plan')
    ap.add_argument('--ana', default=r'C:\.ana')
    ap.add_argument('--sibling', default=r'C:\Users\a343o\source\repos\the_symbol_game')
    args = ap.parse_args()
    repo, ana_root, sg = args.repo, args.ana, args.sibling

    inv = json.load(open(args.inventory, encoding='utf-8'))
    cited = []
    for p in inv['paths']:
        if not p.get('removed_in_commit') or p.get('removed_dir') or not p['path'].startswith(PREFIX):
            continue
        fam = p['path'][len(PREFIX):].split('/')[0]
        live = {k: v for k, v in p['referenced_from'].items() if k in LIVE}
        if fam in FAMS and live:
            cited.append((p['path'], fam, live))

    tracked = subprocess.run(['git', '-C', repo, 'ls-files', '-z'], capture_output=True).stdout \
        .decode('utf-8', 'surrogateescape').split('\0')
    tracked = [t for t in tracked if t and not t.startswith(('dag/results/', 'lean4/Imported/', 'sources/'))]
    by_name = collections.defaultdict(list)
    by_size = collections.defaultdict(list)
    for t in tracked:
        by_name[os.path.basename(t)].append(t)
        try:
            by_size[os.path.getsize(os.path.join(repo, t))].append(t)
        except OSError:
            pass

    rows = []
    for path, fam, live in sorted(cited):
        rel = path[len(PREFIX) + len(fam) + 1:]
        row = {'atlas_path': path, 'family': fam, 'rel': rel, 'ana_path': os.path.join(ana_root, fam, *rel.split('/')),
               'refs': live}
        git = subprocess.run(['git', '-C', sg, '-c', 'core.quotepath=off', 'show', f'{COMMIT}^:{path}'],
                             capture_output=True)
        if git.returncode != 0:
            row['status'] = 'not_in_git'
            rows.append(row)
            continue
        gb = git.stdout
        row.update(git_sha256=sha(gb), size=len(gb))
        if not os.path.isfile(row['ana_path']):
            row['status'] = 'missing_in_ana'
            rows.append(row)
            continue
        ab = open(row['ana_path'], 'rb').read()
        row['ana_sha256'] = sha(ab)
        if sha(ab) != sha(gb):
            row['status'] = 'ana_newline_only_diff' if sha(norm(ab)) == sha(norm(gb)) else 'ana_differs'
            rows.append(row)
            continue
        row['status'] = 'verified'
        existing = None
        for t in by_size.get(len(gb), []):
            try:
                if sha(open(os.path.join(repo, t), 'rb').read()) == row['git_sha256']:
                    existing = ('identical', t)
                    break
            except OSError:
                pass
        if not existing:
            ng = sha(norm(gb))
            for t in by_name.get(os.path.basename(path), []):
                try:
                    if sha(norm(open(os.path.join(repo, t), 'rb').read())) == ng:
                        existing = ('newline_equivalent', t)
                        break
                except OSError:
                    pass
        if existing:
            row['resolved_to_existing'] = {'match': existing[0], 'path': existing[1]}
        elif by_name.get(os.path.basename(path)):
            row['in_repo_same_name_different_content'] = by_name[os.path.basename(path)]
        rows.append(row)
    json.dump(rows, open(args.plan, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(len(rows), 'cited files;', dict(collections.Counter(r['status'] for r in rows)))
    print('resolved to existing', sum(1 for r in rows if 'resolved_to_existing' in r))
    print('to copy', sum(1 for r in rows if r['status'] == 'verified' and 'resolved_to_existing' not in r))
    print('copied files with a same-named, different in-repo file',
          sum(1 for r in rows if r.get('in_repo_same_name_different_content')))


if __name__ == '__main__':
    main()
