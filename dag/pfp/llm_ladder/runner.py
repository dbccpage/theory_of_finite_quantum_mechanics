"""Ladder policy and orchestration for one node and one stage (P0).

AuthorityEffect: None.

Policy (see DESIGN.md "Ladder policy"):
  - tier 0 is the free models; tiers 1..5 are cheap OpenRouter, Haiku 5.5, Sonnet 5.5, Opus 5.5, Fable 5.1;
  - each attempt rotates to the next usable model of its tier, so an escalation is never decided by one
    model's bad day;
  - a host-classified failure is a SENT attempt whose answer the host rejected (schema violation, too few
    verified entries, or too high a refused-claim rate). N of them at a tier escalate to the next tier;
  - an infrastructure failure (rate limit, timeout, unavailable model, authentication) never counts as a
    host failure: the model rotates, a bounded number of times, then the tier is abandoned;
  - Fable 5.1 is used only with allow_fable (the final hard step), and any paid call is refused before
    dispatch when a weekly or run cap would be exceeded (budget.py);
  - every refused claim becomes a negative operad entry (memory.py) BEFORE the next attempt is compiled, so
    the next call is guided by it unless feedback is switched off (the control arm of the pilot).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from .budget import BudgetRefused, Ledger, cost_microusd as rate_cost, micro_to_usd
from .config import DEFAULT_POLICY, PRICES, STAGE_EFFORT
from .gateway import Gateway
from .llm_common import Redactor, sha256_text, utc_iso, utc_stamp
from .memory import HallucinationIndex, index_path
from .packets import CompiledPacket, compile_p0, estimate_tokens, staged_baseline_tokens
from .providers import CallRequest, ProviderError, extract_json
from .records import POLICY_NOTE, RunWriter, build_delta, host_check_record
from .verify import DeclIndex, Failure, LeanRunner, VerifyReport, Verifier


class LadderRunner:
    def __init__(self, root, *, ledger: Ledger, providers: dict, tiers: list, policy: dict | None = None,
                 redactor: Redactor | None = None, decl_index: DeclIndex | None = None, verifier: Verifier | None = None,
                 sleeper=time.sleep, clock=time.monotonic):
        self.root = Path(root)
        self.ledger, self.providers, self.tiers = ledger, providers, tiers
        self.policy = {**DEFAULT_POLICY, **(policy or {})}
        self.red = redactor or Redactor()
        self.index = decl_index or DeclIndex(self.root)
        self.verifier = verifier or Verifier(self.root, index=self.index, lean=LeanRunner(self.root))
        self.hall = HallucinationIndex(index_path(self.root))
        self._sleep, self._clock = sleeper, clock

    # ------------------------------------------------------------------ planning
    def effort_for(self, stage: str, model: str, override=None):
        if override:
            return override
        return STAGE_EFFORT.get(stage, {}).get(model)

    def plan(self, node_id, *, stage='P0', start_tier=0, max_tier=4, run_cap_microusd=0, feedback=True, allow_fable=False,
             effort_override=None) -> dict:
        packet = compile_p0(self.root, node_id, attempt_id='plan', policy=self.policy, index=self.index, feedback=feedback,
                            hallucinations=self.hall)
        tokens = packet.estimated_tokens()
        rows, worst_total = [], 0
        for tier in self.tiers:
            if not start_tier <= tier['id'] <= max_tier or (tier['id'] == 5 and not allow_fable):
                continue
            for cand in tier['candidates']:
                configured = cand['provider'] in self.providers and cand.get('enabled', True)
                price = PRICES.get((cand['provider'], cand['model']))
                worst = rate_cost(tokens, tier['max_tokens'], *price) if price and tier['family'] != 'free' else 0
                rows.append({'tier': tier['id'], 'name': tier['name'], 'family': tier['family'], 'provider': cand['provider'],
                             'model': cand['model'], 'configured': configured, 'effort': self.effort_for(stage, cand['model'], effort_override),
                             'max_tokens': tier['max_tokens'], 'attempts_before_escalation': tier['attempts_before_escalation'],
                             'worst_case_usd_per_call': round(micro_to_usd(worst), 6)})
            if tier['family'] != 'free' and tier['candidates']:
                price = PRICES.get((tier['candidates'][0]['provider'], tier['candidates'][0]['model']))
                if price:
                    worst_total += tier['attempts_before_escalation'] * rate_cost(tokens, tier['max_tokens'], *price)
        week = self.ledger.week_totals()
        return {'node_id': node_id, 'stage': stage, 'packet': packet, 'estimated_input_tokens': tokens,
                'staged_prompt_tokens_baseline': staged_baseline_tokens(self.root, node_id), 'tiers': rows,
                'worst_case_all_paid_tiers_usd': round(micro_to_usd(worst_total), 4),
                'run_cap_usd': micro_to_usd(run_cap_microusd), 'week': week, 'feedback': feedback,
                'note': 'Input tokens are a local byte estimate; the live run uses count_tokens for Anthropic. No call was made.'}

    # ------------------------------------------------------------------ one request
    def _request(self, packet: CompiledPacket, tier: dict, cand: dict, stage, effort_override) -> CallRequest:
        max_tokens = tier['max_tokens']
        return CallRequest(model=cand['model'], system=packet.system, user=packet.user, max_tokens=max_tokens,
                           schema=packet.schema, effort=self.effort_for(stage, cand['model'], effort_override),
                           stream=max_tokens > self.policy['stream_above_max_tokens'], body_extra=dict(cand.get('body_extra', {})))

    def _accept(self, report: VerifyReport) -> bool:
        return (report.parsed and report.verified_total() >= self.policy['min_verified']
                and report.failure_rate() <= self.policy['max_failure_rate'])

    # ------------------------------------------------------------------ the run
    def run(self, node_id, *, stage='P0', run_cap_microusd, start_tier=0, max_tier=4, feedback=True, allow_fable=False,
            effort_override=None, label=None, write=True, fixed_attempts=None) -> dict:
        """fixed_attempts=N is the MEASUREMENT mode used by the pilot: exactly N answered attempts at the start tier,
        no acceptance stop and no escalation, so that a control arm and a guided arm are paired."""
        if stage != 'P0':
            raise ValueError('only P0 is wired: P1+ need host-reviewed missions (dag/pfp/prepare_stage.py) first')
        stamp = utc_stamp()
        run_name = stamp + '_ladder'
        probe = self.root / 'dag' / 'results' / node_id / 'runs'
        bump = 0
        while (probe / run_name).exists():
            bump += 1
            run_name = '%s_ladder_%d' % (stamp, bump)
        run_id = '%s/%s' % (node_id, run_name)
        gateway = Gateway(self.providers, self.ledger, run_id=run_id, run_cap_microusd=run_cap_microusd, redactor=self.red)
        writer = RunWriter(self.root, node_id, run_name, self.red) if write else None
        attempts, texts = [], {}
        accepted = None
        stop_reason = 'ladder_exhausted'
        dead_providers, cooldown = set(), {}
        first_packet = None
        seq = 0
        for tier in self.tiers:
            if not start_tier <= tier['id'] <= max_tier or (tier['id'] == 5 and not allow_fable):
                continue
            usable_all = [c for c in tier['candidates'] if c['provider'] in self.providers and c.get('enabled', True)]
            if not usable_all:
                attempts.append({'attempt_id': 't%d-skip' % tier['id'], 'tier': tier['id'], 'status': 'tier_unconfigured'})
                continue
            host_failures = infra_failures = cursor = waits_done = answered = 0
            abstainers: set = set()
            limit = tier['attempts_before_escalation'] if fixed_attempts is None else fixed_attempts
            while (answered if fixed_attempts is not None else host_failures) < limit and infra_failures < tier['max_infra_failures']:
                now = self._clock()
                usable = [c for c in usable_all if c['provider'] not in dead_providers and cooldown.get(c['provider'], 0) <= now]
                if not usable:
                    waits = [cooldown[c['provider']] - now for c in usable_all if c['provider'] not in dead_providers]
                    if waits and min(waits) <= 90 and tier['family'] == 'free' and waits_done < 3:
                        waits_done += 1
                        attempts.append({'attempt_id': 't%d-wait' % tier['id'], 'tier': tier['id'], 'status': 'backoff_wait',
                                         'wait_s': round(min(waits), 1)})
                        self._sleep(min(waits) + 0.5)
                        continue
                    break
                cand = usable[cursor % len(usable)]
                cursor += 1
                seq += 1
                aid = 'a%d-%d' % (tier['id'], seq)
                packet = compile_p0(self.root, node_id, attempt_id=aid, policy=self.policy, index=self.index,
                                    feedback=feedback, hallucinations=self.hall)
                first_packet = first_packet or packet
                request = self._request(packet, tier, cand, stage, effort_override)
                row = {'attempt_id': aid, 'tier': tier['id'], 'provider': cand['provider'], 'model': cand['model'],
                       'effort': request.effort, 'guided': feedback, 'known_neg_injected': packet.meta['known_neg_injected'],
                       'known_pos_injected': packet.meta['known_pos_injected'], 'input_sha256': packet.input_sha256,
                       'injected_neg_ids': packet.meta['neg_entry_ids']}
                try:
                    result = gateway.call(cand['provider'], request, tier_id=tier['id'], family=tier['family'], attempt_id=aid)
                except BudgetRefused as refusal:
                    row.update(status='budget_refused', code=refusal.code, message=refusal.message)
                    attempts.append(row)
                    stop_reason = 'budget_refused:' + refusal.code
                    return self._finish(node_id, run_id, run_name, writer, attempts, texts, gateway, accepted, stop_reason,
                                        first_packet, run_cap_microusd, feedback)
                except ProviderError as error:
                    infra_failures += 1
                    row.update(status='infra_error', code=error.code, message=self.red.redact(error.message), backoff=error.backoff_events)
                    if error.code in ('auth', 'payment_required', 'provider_unconfigured'):
                        dead_providers.add(cand['provider'])
                    if error.code == 'rate_limited':
                        cooldown[cand['provider']] = self._clock() + min(error.retry_after or 30.0, 300.0)
                    if error.code == 'model_unavailable':
                        usable_all = [c for c in usable_all if c is not cand] or usable_all
                    attempts.append(row)
                    continue
                # the model answered
                report, response = self._check(result, packet)
                texts[aid] = (packet, result.text, response, report, cand, tier)
                accepted_now = self._accept(report)
                answered += 1
                abstained = report.parsed and not report.failures and report.verified_total() < self.policy['min_verified']
                row.update(status='accepted' if accepted_now else 'rejected', verified_total=report.verified_total(),
                           failures_total=report.failure_total(), failure_rate=round(report.failure_rate(), 4),
                           failures_by_class=report.by_class(), unverifiable=len(report.unverifiable),
                           input_tokens=result.input_tokens, output_tokens=result.output_tokens,
                           cost_microusd=result.cost_microusd, request_id=result.request_id, latency_s=result.latency_s,
                           stop_reason=result.stop_reason, served_model=result.model, structured_mode=result.structured_mode,
                           lean=report.lean.get('status'), abstained=abstained)
                row['negative_entries'] = [e['id'] for e in self.hall.add_failures(
                    report.failures, node_id=node_id, run_id=run_id, attempt_id=aid, model=result.model or cand['model'],
                    provider=cand['provider'], tier=tier['id'])]
                attempts.append(row)
                if accepted_now and fixed_attempts is not None:
                    accepted = accepted or aid
                    stop_reason = 'fixed_attempts_completed'
                elif accepted_now:
                    accepted = aid
                    stop_reason = 'accepted_at_tier_%d' % tier['id']
                    return self._finish(node_id, run_id, run_name, writer, attempts, texts, gateway, accepted, stop_reason,
                                        first_packet, run_cap_microusd, feedback)
                host_failures += 1
                if abstained:
                    abstainers.add(cand['model'])
                if self.policy.get('abstain_stop') and fixed_attempts is None and len(abstainers) >= self.policy['abstain_stop']:
                    stop_reason = 'blocked_abstained:%d_models_found_nothing_to_ground' % len(abstainers)
                    return self._finish(node_id, run_id, run_name, writer, attempts, texts, gateway, accepted, stop_reason,
                                        first_packet, run_cap_microusd, feedback)
            if fixed_attempts is not None:
                stop_reason = 'fixed_attempts_completed'
                break
        return self._finish(node_id, run_id, run_name, writer, attempts, texts, gateway, accepted, stop_reason, first_packet,
                            run_cap_microusd, feedback)

    def _check(self, result, packet: CompiledPacket):
        if result.refusal:
            report = VerifyReport()
            report.failures.append(Failure('model_refusal', 'reply', 'reply', 'model refused (stop_reason=refusal)',
                                           'category: %s' % (result.stop_category or 'unspecified')))
            return report, None
        response, error = extract_json(result.text)
        if response is None:
            report = VerifyReport()
            note = ' (truncated at max_tokens)' if result.truncated else ''
            report.failures.append(Failure('unparseable_reply', 'reply', 'reply', (result.text or '')[:120], (error or '') + note))
            return report, None
        return self.verifier.verify_p0(response, packet.schema, target_statement=packet.target_statement), response

    # ------------------------------------------------------------------ records
    def _finish(self, node_id, run_id, run_name, writer, attempts, texts, gateway, accepted, stop_reason, first_packet,
                run_cap_microusd, feedback):
        sent = [a for a in attempts if a.get('status') in ('accepted', 'rejected')]
        best = accepted
        if best is None and sent:
            best = max(sent, key=lambda a: (a['verified_total'] - a['failures_total'], -a['tier']))['attempt_id']
        summary = {'node_id': node_id, 'run_id': run_id, 'stage': 'P0', 'status': 'accepted' if accepted else
                   ('budget_refused' if stop_reason.startswith('budget_refused') else
                   ('blocked_abstained' if stop_reason.startswith('blocked_abstained') else 'not_accepted')), 'stop_reason': stop_reason,
                   'accepted_attempt': accepted, 'best_attempt': best, 'attempts': attempts,
                   'totals_by_tier': gateway.totals(), 'feedback': feedback}
        spend = sum(r.get('cost_microusd') or 0 for r in gateway.receipts)
        summary['spend_microusd'] = spend
        summary['spend_usd'] = micro_to_usd(spend)
        by_class: dict = {}
        by_model: dict = {}
        for a in sent:
            for cls, n in a['failures_by_class'].items():
                by_class[cls] = by_class.get(cls, 0) + n
                by_model.setdefault(a['model'], {})
                by_model[a['model']][cls] = by_model[a['model']].get(cls, 0) + n
        summary['hallucinations_by_class'] = dict(sorted(by_class.items()))
        summary['hallucinations_by_model'] = by_model
        if best and best in texts:
            packet, text, response, report, cand, tier = texts[best]
            summary['verified'] = {k: len(v) for k, v in report.verified.items()}
        if writer is not None and first_packet is not None:
            self._write(writer, summary, texts, gateway, best, accepted, first_packet, run_cap_microusd, run_id)
            summary['run_dir'] = writer.dir.relative_to(self.root).as_posix()
        return summary

    def _write(self, writer, summary, texts, gateway, best, accepted, first_packet, run_cap_microusd, run_id):
        ids = {}
        entries = self.hall.load()['entries']
        for entry in entries.values():
            ids[entry['claim_pattern']] = entry['id']
        deltas = {}
        for aid, (packet, text, response, report, cand, tier) in texts.items():
            model, provider = cand['model'], cand['provider']
            delta = build_delta(report, response, model=model, provider=provider, tier=tier['id'], node_id=summary['node_id'], entry_ids=ids)
            deltas[aid] = delta
            check = host_check_record(report, accepted=(aid == accepted), aid=aid, model=model)
            writer.attempt(packet, aid, raw_text=text, response=response, report=report, delta=delta, host_check=check)
        if best and best in texts:
            packet, text, response, report, cand, tier = texts[best]
            run_delta = dict(deltas[best])
            seen = {r['id'] for r in run_delta['failed_compositions'] + run_delta['counterexamples']}
            for aid, delta in deltas.items():
                if aid == best:
                    continue
                for key in ('failed_compositions', 'counterexamples'):
                    for row in delta[key]:
                        if row['id'] not in seen:
                            run_delta[key] = run_delta[key] + [row]
                            seen.add(row['id'])
            check = host_check_record(report, accepted=(best == accepted), aid=best, model=cand['model'])
            writer.best(packet, best, raw_text=text, response=response, delta=deltas[best], host_check=check, report=report,
                        run_delta=run_delta)
        else:
            writer._json('p0/request.json', first_packet.as_request_json())
        calls = self.red.redact_obj(gateway.receipts)
        sent = [r for r in gateway.receipts if r['status'] in ('ok', 'refused_by_model')]
        week = self.ledger.week_totals()
        receipt = {'schema_id': 'omega.pfp.llm-ladder.run-receipt.v1', 'authority_effect': 'None', 'node_id': summary['node_id'],
                   'stage': 'P0', 'run_id': run_id, 'finished_utc': utc_iso(), 'provider_calls_policy': POLICY_NOTE,
                   'external_provider_calls': len(sent), 'free_calls': sum(1 for r in sent if r['family'] == 'free'),
                   'paid_calls': sum(1 for r in sent if r['family'] != 'free'),
                   'policy': {k: self.policy[k] for k in ('min_verified', 'max_failure_rate', 'feedback')} | {'feedback_arm': summary['feedback']},
                   'tiers_configured': [{'id': t['id'], 'name': t['name'], 'attempts_before_escalation': t['attempts_before_escalation'],
                                         'models': [c['model'] for c in t['candidates']]} for t in self.tiers],
                   'run_cap_usd': micro_to_usd(run_cap_microusd), 'summary': summary, 'calls': calls,
                   'budget_week_after': {k: (micro_to_usd(v) if k.endswith('microusd') else v) for k, v in week.items()},
                   'redaction': 'Key values are redacted from every field; the scan test (test_ladder.py) re-checks the files.'}
        writer.receipt(receipt, calls)
