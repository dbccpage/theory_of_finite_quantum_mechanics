"""Replay all current C250 machine predictions and receipt links.

AuthorityEffect: None. Prediction scoring is not mathematical verification.
Judged prose clauses remain outside this machine report.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from omega_engine_projects.ms_majorana.code.tests.support.finite_qm.entrypoints.c250_score_block import score_bet_file, validate_block_result


def replay(app: Path) -> dict:
    custody = json.loads((app / 'evidence/c250_review_custody_20260907.json').read_text(encoding='utf-8'))
    original = {entry['path']: entry['sha256'] for entry in custody['files']}
    blocks = []
    totals = Counter()
    for block in range(1, 11):
        root = app / f'block_{block:02d}'
        path = root / 'result.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        notes = validate_block_result(data, block, app)
        bets = sorted((root / 'bets').glob('BET-*.txt'))
        if len(bets) != 3:
            raise ValueError(f'Expected three predictions for block {block}, found {len(bets)}')
        scores = []
        for bet in bets:
            rel = bet.relative_to(app).as_posix()
            digest = hashlib.sha256(bet.read_bytes()).hexdigest()
            if digest != original.get(rel):
                raise ValueError(f'Original prediction changed: {rel}')
            scored = score_bet_file(bet, data)
            scored.update(path=rel, sha256=digest, judged_clauses='UNSCORED')
            scores.append(scored)
            totals.update(c['status'] for c in scored['clauses'])
        blocks.append({'block': block, 'result_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'receipt_validation': notes, 'predictions': scores})
    return {'authority_effect': 'None', 'scope': '30 original prediction files; all machine clauses, including those labelled FORCED. HIT compares the scoped recorded value and does not prove the predicate. Missing or narrower evidence remains OPEN. Judged prose is unscored.',
            'original_head': custody['original_head'], 'totals_all_machine_clauses': dict(sorted(totals.items())),
            'standing_bets_fully_scored': False, 'terminal_claim_verified': False, 'blocks': blocks}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Write the current report; default verifies it')
    args = parser.parse_args()
    app = (Path(__file__).resolve().parents[4] / "apps/finite_qm")
    result = replay(app)
    target = app / 'evidence/c250_machine_review_20260907.json'
    if args.write:
        target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    elif json.loads(target.read_text(encoding='utf-8')) != result:
        raise ValueError('Stale machine review; inspect inputs before regenerating')
    print(json.dumps(result['totals_all_machine_clauses'], sort_keys=True))
    print('30 immutable predictions, 10 result records and all linked receipts verified; judged clauses remain unscored')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

__all__ = ['main', 'replay']
