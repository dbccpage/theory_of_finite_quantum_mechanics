"""Incorporate the reviewed PFP result folders into derivation_dag.json and the TFQ JSONL.

Every folder dag/results/<NODE-ID>/reviews/*/ holds the review of one DAG node. The curated
decisions in dag/fragments/pfp_review_decisions.json say, for each reviewed node, which review file
is the latest, what the review does to the node (scope_effect) and any status, statement or
bottleneck override. This script owns three things:

- a pfp_review object on each reviewed node of derivation_dag.json: the review path and sha256,
  the verdict, narrowest_claim, does_not_support, next_test, the scope_effect, the prior status,
  statement and bottleneck, and the later runs that supersede the review;
- the decision overrides, applied idempotently from the prior values kept in that object. A status is
  never raised. A route into a lowered node is lowered with it (the old route status is kept);
- pfp_review_refs on every base row of theory_of_finite_qm.jsonl that names a reviewed node.

A next_test that is one of the boilerplate strings of the decisions file is replaced by the node's own
does_not_support obligation. Review text copied into the DAG replaces the words universal, proves and
impossible, which the DAG file forbids; the review files themselves are never changed.

Run order: this script, then sync_unified_dag.py, sync_application_branches.py and
sync_pregenesis_to_wdp.py; --check on all four is then clean. --check detects stale generated data
without writing; --report lists the decisions.
AuthorityEffect: None. Synchronization does not establish a mathematical claim, and no status is raised.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DECISIONS = 'dag/fragments/pfp_review_decisions.json'
GENERATED_SLICES = ('unified_dag', 'pregenesis_to_wdp', 'application_branches')
SCOPE_EFFECTS = ('consistent', 'caveat_added', 'statement_narrowed', 'status_lowered')
# Weakest to strongest. A decision may keep or lower a status, never raise it.
STATUS_RANK = {
    'OPEN': 0, 'SOURCE_RECORD': 0, 'IMPORTED_ASSUMPTION': 1, 'ADMITTED_PRIMITIVE': 1, 'CONDITIONAL': 2,
    'DEFINITION': 2, 'COMPUTATIONALLY_CHECKED': 3, 'PROVED_PROSE': 4, 'PROVED_LEAN': 5,
}
ROUTE_RANK = {'GAP_NO_DERIVATION': 0, 'RECORD_PARENT': 0, 'CONDITIONAL_ON_IMPORT': 1, 'COMPUTED': 2,
              'DERIVED_PROSE': 3, 'DERIVED_LEAN': 4}
ROUTE_FOR_STATUS = {'OPEN': 'GAP_NO_DERIVATION', 'CONDITIONAL': 'CONDITIONAL_ON_IMPORT',
                    'COMPUTATIONALLY_CHECKED': 'COMPUTED', 'PROVED_PROSE': 'DERIVED_PROSE',
                    'PROVED_LEAN': 'DERIVED_LEAN'}
OBJECT_KEYS = ('review', 'review_sha256', 'review_refs', 'verdict', 'narrowest_claim', 'does_not_support',
               'next_test', 'scope_effect', 'reason', 'prior_status', 'prior_statement', 'prior_bottleneck',
               'superseded_by')
WORDS = [(r'\buniversal\b', 'general'), (r'\buniversally\b', 'generally'), (r'\bproves\b', 'establishes'),
         (r'\bimpossible\b', 'not possible')]


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def record_line(record, newline):
    return json.dumps(record, ensure_ascii=False, sort_keys=True) + newline


def sanitize(text: str) -> str:
    for pattern, replacement in WORDS:
        text = re.sub(pattern, replacement, text, flags=re.I)
    return text


def review_sha256(data: bytes) -> str:
    """Newline-normalized, so that a CRLF checkout hashes like the committed bytes."""
    return hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest()


def find_text(obj, key):
    """The first string stored under key, at any depth (claim_boundary is sometimes nested)."""
    if isinstance(obj, dict):
        if isinstance(obj.get(key), str):
            return obj[key]
        for value in obj.values():
            found = find_text(value, key)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_text(value, key)
            if found is not None:
                return found
    return None


def load_decisions(root: Path = ROOT):
    return json.loads((root / DECISIONS).read_text(encoding='utf-8'))


def review_digest(root: Path, entry: dict, boilerplate: list[str]) -> dict:
    """The fields of one review that the DAG carries."""
    path = root / entry['review']
    data = path.read_bytes()
    review = json.loads(data.decode('utf-8'))
    given = entry.get('review_digest', {})
    narrowest = given.get('narrowest_claim') or find_text(review, 'narrowest_claim')
    unsupported = given.get('does_not_support') or find_text(review, 'does_not_support')
    if not narrowest or not unsupported:
        raise ValueError(f'{entry["node_id"]}: review has no narrowest_claim/does_not_support; add review_digest')
    next_test = given.get('next_test') or find_text(review, 'next_test')
    if not next_test or next_test in boilerplate:
        next_test = unsupported
    verdict = given.get('verdict') or review.get('status') or 'reviewed'
    refs = list(entry.get('extra_reviews', [])) + [entry['review']]
    return {
        'review': entry['review'], 'review_sha256': review_sha256(data), 'review_refs': refs,
        'verdict': sanitize(verdict), 'narrowest_claim': sanitize(narrowest),
        'does_not_support': sanitize(unsupported), 'next_test': sanitize(next_test),
    }


def decision_errors(decisions: dict, nodes: dict) -> list[str]:
    errors = []
    seen = set()
    for entry in decisions['decisions']:
        nid = entry['node_id']
        if nid in seen:
            errors.append(f'{nid}: duplicate decision')
        seen.add(nid)
        if nid not in nodes:
            errors.append(f'{nid}: not a DAG node')
        if entry['scope_effect'] not in SCOPE_EFFECTS:
            errors.append(f'{nid}: bad scope_effect {entry["scope_effect"]}')
        if entry['scope_effect'] == 'status_lowered' and 'status' not in entry:
            errors.append(f'{nid}: status_lowered without a status')
        if entry['scope_effect'] != 'status_lowered' and 'status' in entry:
            errors.append(f'{nid}: status override but scope_effect {entry["scope_effect"]}')
        if entry['scope_effect'] == 'statement_narrowed' and 'statement' not in entry:
            errors.append(f'{nid}: statement_narrowed without a statement')
    return errors


def apply_decisions(root: Path, dag: dict, decisions: dict) -> list[str]:
    """Write pfp_review objects and overrides onto the nodes and lower the routes of lowered nodes."""
    nodes = {n['id']: n for n in dag['nodes']}
    errors = decision_errors(decisions, nodes)
    if errors:
        return errors
    incoming: dict[str, list[dict]] = {}
    for route in dag['routes']:
        incoming.setdefault(route['output'], []).append(route)
    boilerplate = decisions['boilerplate_next_test']
    for entry in decisions['decisions']:
        node = nodes[entry['node_id']]
        old = node.get('pfp_review') or {}
        obj = review_digest(root, entry, boilerplate)
        obj['scope_effect'] = entry['scope_effect']
        obj['reason'] = sanitize(entry['reason'])
        # Prior values: kept from the first application where this decision overrides the field.
        prior = {}
        for field, key in (('status', 'prior_status'), ('statement', 'prior_statement'),
                           ('bottleneck', 'prior_bottleneck')):
            prior[field] = old[key] if field in entry and key in old else node[field]
        obj['prior_status'], obj['prior_statement'], obj['prior_bottleneck'] = (
            prior['status'], prior['statement'], prior['bottleneck'])
        obj['superseded_by'] = list(entry.get('superseded_by', []))
        new_status = entry.get('status', prior['status'])
        if STATUS_RANK[new_status] > STATUS_RANK[prior['status']]:
            return [f'{entry["node_id"]}: decision raises {prior["status"]} to {new_status}']
        for field in ('status', 'statement', 'bottleneck'):
            if field in entry:
                node[field] = entry[field]
        route_prior = dict(old.get('prior_route_status', {}))
        if new_status != prior['status']:
            target = ROUTE_FOR_STATUS[new_status]
            for route in incoming.get(node['id'], []):
                base = route_prior.get(route['id'], route['status'])
                if ROUTE_RANK[base] > ROUTE_RANK[target]:
                    route_prior[route['id']] = base
                    route['status'] = target
        if route_prior:
            obj['prior_route_status'] = dict(sorted(route_prior.items()))
        node.pop('pfp_review', None)
        node['pfp_review'] = obj
    return []


def reviewed_refs(dag: dict) -> dict[str, list[str]]:
    return {n['id']: n['pfp_review']['review_refs'] for n in dag['nodes'] if 'pfp_review' in n}


def generated_files(root: Path = ROOT):
    folder = root / 'dag'
    decisions = load_decisions(root)
    dag = json.loads((folder / 'derivation_dag.json').read_text(encoding='utf-8'))
    errors = apply_decisions(root, dag, decisions)
    if errors:
        raise ValueError('pfp review decisions invalid:\n  ' + '\n  '.join(errors))
    refs_of = reviewed_refs(dag)
    aliases = json.loads((folder / 'fragments/unified_dag.json').read_text(encoding='utf-8'))['row_aliases']
    lines = (folder / 'theory_of_finite_qm.jsonl').read_bytes().decode('utf-8').splitlines(keepends=True)
    newline = '\r\n' if lines and lines[0].endswith('\r\n') else '\n'
    out = []
    for line in lines:
        record = json.loads(line)
        if record.get('source_slice') not in GENERATED_SLICES:
            ids = set(record['existing_derivation_dag_ids']) | set(aliases.get(record['id'], []))
            refs = sorted({ref for i in ids for ref in refs_of.get(i, [])})
            if refs:
                record = dict(record, pfp_review_refs=refs)
            else:
                record = {k: v for k, v in record.items() if k != 'pfp_review_refs'}
            if record != json.loads(line):
                line = record_line(record, newline)
        out.append(line)
    return {folder / 'derivation_dag.json': json_text(dag).encode('utf-8'),
            folder / 'theory_of_finite_qm.jsonl': ''.join(out).encode('utf-8')}


def report(root: Path = ROOT) -> str:
    decisions = load_decisions(root)
    dag = json.loads((root / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    nodes = {n['id']: n for n in dag['nodes']}
    counts: dict[str, int] = {}
    rows = []
    for entry in decisions['decisions']:
        counts[entry['scope_effect']] = counts.get(entry['scope_effect'], 0) + 1
        if entry['scope_effect'] in ('status_lowered', 'statement_narrowed'):
            prior = nodes[entry['node_id']].get('pfp_review', {}).get('prior_status', nodes[entry['node_id']]['status'])
            rows.append(f'{entry["scope_effect"]}: {entry["node_id"]} {prior} -> {entry.get("status", prior)}: {entry["reason"]}')
    return '\n'.join([f'{k}={v}' for k, v in sorted(counts.items())] + rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--report', action='store_true', help='list the decisions; write nothing')
    args = parser.parse_args()
    if args.report:
        print(report(ROOT))
        return 0
    differences = []
    for path, expected in generated_files(ROOT).items():
        if not path.exists() or path.read_bytes() != expected:
            differences.append(path.relative_to(ROOT).as_posix())
            if not args.check:
                path.write_bytes(expected)
    print('stale=' + ','.join(differences) if differences else 'pfp results synchronized')
    return int(bool(differences) and args.check)


if __name__ == '__main__':
    raise SystemExit(main())
