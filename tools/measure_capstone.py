#!/usr/bin/env python3
"""Collect capstone Milestone 3 measurements; no acceptance verdicts are assigned."""
import argparse
import datetime as dt
import json
from pathlib import Path
import ssl
import statistics
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
QUERY = '90s track jacket in size M'
MARKER = '<!-- capstone-milestone3-measurements -->'


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def revision():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                       text=True, timeout=5).strip()
    except (OSError, subprocess.SubprocessError):
        return None


def request_once(url, payload, timeout, context):
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    request = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={'Content-Type': 'application/json'})
    tick = time.perf_counter()
    status, headers, output, error = None, {}, None, None
    try:
        try:
            response = urllib.request.urlopen(request, timeout=timeout, context=context)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            status = response.status
            headers = {'request_id': response.headers.get('X-Request-ID'),
                       'run_log': response.headers.get('X-Run-Log')}
            text = response.read().decode('utf-8', errors='replace')
            try:
                output = json.loads(text)
            except ValueError:
                output = {'raw': text}
    except (OSError, urllib.error.URLError) as exc:
        error = f'{type(exc).__name__}: {exc}'
    return {'timestamp': started, 'url': url, 'input': payload,
            'http_status': status, 'response': output,
            'client_elapsed_ms': round((time.perf_counter() - tick) * 1000, 3),
            'request_id': headers.get('request_id'), 'run_log': headers.get('run_log'),
            'transport_error': error}


def collect(args):
    import certifi
    parsed = urllib.parse.urlsplit(args.base_url)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError('Use a base HTTP(S) URL without a query or fragment.')
    args.out.mkdir(parents=True, exist_ok=False)
    context = ssl.create_default_context(cafile=certifi.where())
    write_json(args.out / 'collection.json', {
        'purpose': 'Milestone 3 operational measurement, not formal acceptance trials',
        'collector_checkout_revision': revision(), 'base_url': args.base_url.rstrip('/'),
        'query': args.query, 'count': args.count, 'pause_seconds': args.pause,
        'timeout_seconds': args.timeout,
        'warm_up': 'None; the first request is included. Host cold/warm state is not asserted.',
    })
    print(f'{args.count} matching requests plus one rejected-input request.', flush=True)
    print('This cost sample is separate from formal three-trial criterion testing.', flush=True)
    print('Each completed outfit normally uses two model calls; retries can add calls.', flush=True)
    with (args.out / 'client_requests.jsonl').open('x', encoding='utf-8') as handle:
        cases = [('measurement', {'query': args.query}) for _ in range(args.count)]
        cases.append(('rejected_input', {}))
        for index, (kind, payload) in enumerate(cases, 1):
            row = request_once(args.base_url.rstrip('/') + '/ask', payload, args.timeout, context)
            row.update(kind=kind, sequence=index)
            handle.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n')
            handle.flush()
            print(f'{index}/{len(cases)} {kind}: HTTP {row["http_status"]}, '
                  f'{row["client_elapsed_ms"]/1000:.3f}s, log={row["run_log"]}, '
                  f'ID={row["request_id"]}', flush=True)
            if kind == 'measurement' and index < args.count and args.pause:
                time.sleep(args.pause)
    print(f'Saved responses in {args.out}. Export Vercel runtime logs immediately using --since 30m.', flush=True)


def application_records(path):
    records = {}
    text = path.read_text(encoding='utf-8')
    if not text.strip():
        raise ValueError('Runtime export is empty. Check the Vercel export command; use --since 30m on Hobby. Recover logs before repeating any model requests.')
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        wrapper = json.loads(line)
        if isinstance(wrapper, dict) and wrapper.get('status') == 'error':
            raise ValueError(f'Runtime export contains a CLI error: {wrapper.get("message", wrapper.get("reason"))}. {wrapper.get("hint", "")}')
        candidates = [wrapper]
        if wrapper.get('type') == 'log':
            message = wrapper.get('data', {}).get('message', '')
            try:
                candidates = [json.loads(message)]
            except (ValueError, TypeError):
                candidates = []
                for part in message.splitlines():
                    try:
                        candidates.append(json.loads(part))
                    except ValueError:
                        pass
        for row in candidates:
            if not isinstance(row, dict) or not {'request_id', 'timestamp', 'status_code',
                                                   'input', 'output', 'duration_ms'} <= row.keys():
                continue
            key = row['request_id']
            if key in records and records[key] != row:
                raise ValueError(f'Conflicting application records for request {key}, line {number}')
            records[key] = row
    return records


def completed(row):
    body = row.get('response')
    return (row.get('http_status') == 200 and isinstance(body, dict)
            and not body.get('error') and bool(body.get('selected_item'))
            and bool(body.get('outfit_suggestion')) and bool(body.get('fit_card')))


def mean(values):
    return round(statistics.mean(values), 5) if values else None


def summarize(args):
    metadata = read_json(args.out / 'collection.json')
    clients = [json.loads(line) for line in (args.out / 'client_requests.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    measures = [row for row in clients if row['kind'] == 'measurement']
    failures = [row for row in clients if row['kind'] == 'rejected_input']
    logs = application_records(args.runtime)
    selected, missing, problems = [], [], []
    ids = [row['request_id'] for row in clients if row['request_id']]
    if len(ids) != len(set(ids)):
        problems.append('Client responses contain repeated application request IDs.')
    for client in clients:
        record = logs.get(client['request_id'])
        if record is None:
            missing.append({'sequence': client['sequence'], 'request_id': client['request_id'],
                            'http_status': client['http_status'], 'transport_error': client['transport_error']})
            continue
        if (record['input'] != client['input']
                or record['status_code'] != client['http_status']
                or (client['transport_error'] is None and record['output'] != client['response'])):
            raise ValueError(f'Client/log input, output or status mismatch: {client["request_id"]}')
        selected.append(record)
        if client['run_log'] != 'saved':
            problems.append(f'Request {client["sequence"]} did not report a saved log.')
    measured_logs = [logs[row['request_id']] for row in measures if row['request_id'] in logs]
    if len(measures) != metadata['count']:
        problems.append(f'Expected {metadata["count"]} measurements; found {len(measures)}.')
    if len(failures) != 1 or failures[0]['http_status'] != 400:
        problems.append('The rejected-input example did not produce the expected HTTP 400.')
    if missing:
        problems.append(f'{len(missing)} client responses lack recovered application records.')
    if any(row.get('cache_enabled') is not False for row in measured_logs):
        problems.append('Caching was not confirmed disabled on every recovered measurement.')
    usages = [row.get('model_usage', {}) for row in measured_logs]
    keys = ('model_attempts', 'reported_prompt_tokens', 'reported_output_tokens', 'reported_total_tokens')
    for usage in usages:
        if any(type(usage.get(key)) is not int or usage[key] < 0 for key in keys):
            problems.append('A recovered record lacks nonnegative integer model-usage counters.')
            break
    full_usage = len(measured_logs) == metadata['count'] and all(
        all(type(u.get(key)) is int and u[key] >= 0 for key in keys) for u in usages)
    totals = {key: sum(u[key] for u in usages) for key in keys} if full_usage else None
    summary = {
        'purpose': metadata['purpose'], 'collector_checkout_revision': metadata['collector_checkout_revision'],
        'expected_measurements': metadata['count'], 'recorded_measurements': len(measures),
        'completed_outfits': sum(completed(row) for row in measures),
        'incomplete_or_failed_outfits': sum(not completed(row) for row in measures),
        'recovered_application_records': len(selected), 'missing_records': missing,
        'mean_client_elapsed_seconds': mean([row['client_elapsed_ms'] / 1000 for row in measures]),
        'mean_server_elapsed_seconds': mean([row['duration_ms'] / 1000 for row in measured_logs]) if full_usage else None,
        'reported_usage_totals': totals,
        'mean_reported_total_tokens': round(totals['reported_total_tokens'] / metadata['count'], 5) if totals else None,
        'zero_reported_tokens_despite_model_attempts': sum(
            u.get('model_attempts', 0) > 0 and u.get('reported_total_tokens', 0) == 0 for u in usages),
        'measurement_issues': problems, 'complete_evidence': not problems,
        'method': 'Sequential uncached matching attempts; no warm-up excluded; all attempted runs, including failures, remain in the averages. The rejected-input example is excluded from the cost sample. Client duration is wall time, including network and waits, not CPU time. Pauses between requests are excluded; waits within a request are included. Tokens are provider-reported adapter counters, not verified billing or API dollars.',
    }
    write_json(args.out / 'summary.json', summary)
    (args.out / 'application_records.jsonl').write_text(''.join(
        json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n' for row in selected), encoding='utf-8')
    report = ['### Instrumentation', '',
              f'Milestone 3 operational sample: {len(measures)} matching attempts and one deliberately rejected input. This is not the formal three-trial criteria evaluation.', '',
              'Requests were sent and timed by `tools/measure_capstone.py::request_once`; server records were produced by `serve.py::finish_request_record` and saved by `run_log.py::append_record`. Runtime records were recovered by request ID. These are complete recovered application records in client-request order:', '',
              '```jsonl']
    report.extend(json.dumps(row, ensure_ascii=False, allow_nan=False) for row in selected)
    report += ['```', '', '### What It Costs', '',
               f'- Completed outfits: {summary["completed_outfits"]}/{len(measures)} attempts.',
               f'- Mean client elapsed time per attempted request: {summary["mean_client_elapsed_seconds"]} seconds.',
               f'- Mean server elapsed time per attempted request: {summary["mean_server_elapsed_seconds"]} seconds.',
               f'- Mean reported tokens per attempted request: {summary["mean_reported_total_tokens"]}.',
               f'- Reported model usage totals: `{json.dumps(totals, sort_keys=True)}`.', '',
               summary['method'], '',
               'Both elapsed-time figures measure wall time, not CPU consumption. A zero reported token count, including after a model attempt, does not establish zero token usage or zero spend. No dollar cost is inferred from a pricing page.', '',
               f'Usage records with model attempts but zero reported tokens: {summary["zero_reported_tokens_despite_model_attempts"]}.', '',
               f'Client responses, original runtime export, matched application records and the numeric summary are saved under `{args.out.as_posix()}`.', '']
    if problems:
        report += ['**Incomplete measurement evidence:**'] + [f'- {p}' for p in problems] + ['']
    (args.out / 'report.md').write_text('\n'.join(report), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f'Read {args.out / "report.md"}. No acceptance verdicts have been assigned.')
    if problems:
        raise SystemExit('Evidence is incomplete. Preserve it and investigate; do not silently rerun or count missing records as passes.')


def update_readme(args):
    summary = read_json(args.out / 'summary.json')
    if not summary['complete_evidence'] or summary['recorded_measurements'] != 10:
        raise ValueError('README insertion requires complete evidence for exactly ten measured attempts.')
    target = ROOT / 'README.md'
    text = target.read_text(encoding='utf-8')
    if MARKER in text:
        raise ValueError('A Milestone 3 measurement section already exists. Preserve its history and review any replacement manually.')
    if '## Capstone' not in text:
        raise ValueError('README has no Capstone section.')
    position = text.rfind('\n---\n\n📖')
    if position < text.index('## Capstone'):
        raise ValueError('Could not locate the footer after the Capstone section.')
    section = '\n' + MARKER + '\n\n' + (args.out / 'report.md').read_text(encoding='utf-8')
    text = text[:position] + section + text[position:]
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith('**Still needed for the run-path milestone:**'):
            lines[i] = '**Milestone 3 measurement evidence:** See Instrumentation and What It Costs below. Formal three-trial criteria evaluation remains separate.'
    target.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Inserted measured Instrumentation and What It Costs sections into README.md. Review the diff before committing.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    command = commands.add_parser('collect', help='Make actual hosted requests and save every response immediately.')
    command.add_argument('--base-url', default='https://fitfindr-capstone.vercel.app')
    command.add_argument('--query', default=QUERY)
    command.add_argument('--count', type=int, default=10)
    command.add_argument('--pause', type=float, default=10)
    command.add_argument('--timeout', type=float, default=310)
    command.add_argument('--out', type=Path, required=True)
    command.set_defaults(action=collect)
    command = commands.add_parser('summarize', help='Join actual client responses to exported runtime logs.')
    command.add_argument('--out', type=Path, required=True)
    command.add_argument('--runtime', type=Path, required=True)
    command.set_defaults(action=summarize)
    command = commands.add_parser('write-readme', help='Insert the saved complete measurement report once.')
    command.add_argument('--out', type=Path, required=True)
    command.set_defaults(action=update_readme)
    args = parser.parse_args()
    if args.command == 'collect' and (args.count < 1 or args.pause < 0 or args.timeout <= 0):
        parser.error('count and timeout must be positive; pause must be nonnegative.')
    try:
        args.action(args)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{type(exc).__name__}: {exc}\n')


if __name__ == '__main__':
    main()
