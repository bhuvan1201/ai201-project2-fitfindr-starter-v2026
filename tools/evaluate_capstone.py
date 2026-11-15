#!/usr/bin/env python3
"""Collect and tally three capstone trials. Never edits the README or runs an LLM judge."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import socket
import ssl
import subprocess
import sys
import tempfile
import time

from measure_capstone import QUERY, application_records, completed, read_json, request_once, write_json

ROOT = Path(__file__).resolve().parents[1]
PAUSE = 10
RUNTIME = ('serve.py', 'config.py', 'run_log.py', 'agent.py', 'tools.py', 'generate.py',
           'mcp_client.py', 'mcp_server.py', 'utils/data_loader.py', 'data/listings.json',
           'data/wardrobe_schema.json', 'requirements.txt', 'requirements.lock',
           'pyproject.toml', 'vercel.json', '.python-version')
FROZEN = RUNTIME + ('criteria.md', 'notes/capstone_criteria_review.md',
                    'tools/measure_capstone.py', 'tools/evaluate_capstone.py')
NAMES = {1: 'Hosted completion', 2: 'Recoverable health logs', 3: 'Response within 45 seconds',
         4: 'Completed output and reported usage', 5: 'Visible logging failure'}
TARGETS = {1: (4, 5), 2: (5, 5), 3: (4, 5), 4: (5, 5), 5: (10, 10)}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    result = subprocess.run(['git', *args], cwd=ROOT, text=True, capture_output=True, timeout=60)
    if result.returncode:
        raise ValueError('Cannot verify committed test inputs. Commit the criteria and evaluation scripts first; '
                         'resolve any Git/iCloud error before making model calls. ' + result.stderr.strip())
    return result.stdout.strip()


def preflight(args):
    git('ls-files', '--error-unmatch', '--', *FROZEN)
    git('diff', '--exit-code', 'HEAD', '--', *FROZEN)
    plan = {'purpose': 'Formal capstone baseline evaluation', 'query': QUERY,
            'base_url': args.base_url.rstrip('/'), 'measured_requests_per_trial': 5,
            'warmups_per_trial': 1, 'health_requests_per_trial': 5,
            'local_fault_requests_per_trial': 10, 'pause_seconds': PAUSE,
            'hosted_ask_timeout_seconds': 310, 'health_timeout_seconds': 30,
            'file_sha256': {name: digest(ROOT / name) for name in FROZEN}}
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / 'evaluation_plan.json'
    if path.exists():
        if read_json(path) != plan:
            raise ValueError('Code, criteria, query or host differs from the frozen plan. Keep trials unchanged and preserve the existing evidence.')
    else:
        write_json(path, plan)
    return git('rev-parse', 'HEAD'), digest(ROOT / 'criteria.md')


def save_client(handle, args, kind, slot, url, payload, context, *, method='POST', timeout=310):
    row = request_once(url, payload, timeout, context, method=method)
    row.update(trial=args.trial, kind=kind, slot=slot)
    handle.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n')
    handle.flush()
    print(f'Trial {args.trial}: {kind} {slot}: HTTP {row["http_status"]}, '
          f'{row["client_elapsed_ms"]/1000:.3f}s, log={row["run_log"]}, '
          f'ID={row["request_id"]}', flush=True)
    return row


def fault_trial(args, folder, handle, context):
    """Ten real local health requests with an actually invalid append destination."""
    with tempfile.TemporaryDirectory(prefix='fitfindr-log-fault-') as temporary:
        temporary = Path(temporary)
        parent = temporary / 'regular_file_not_directory'
        parent.write_text('Controlled log-write fault; no personal data.\n')
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            port = probe.getsockname()[1]
        env = {**os.environ, 'PORT': str(port), 'AI201_CACHE': '0', 'AI201_DEBUG': '0',
               'FITFINDR_RUN_LOG': str(parent / 'runs.jsonl'), 'FITFINDR_LOG_STDOUT': '0',
               'PYTHONPYCACHEPREFIX': str(temporary / 'bytecode'), 'PYTHONUNBUFFERED': '1',
               'GEMINI_API_KEY': ''}
        setup = {'scope': 'Isolated local instance; public Vercel configuration unchanged',
                 'fault': 'Log destination has a regular file as its parent',
                 'command': [sys.executable, 'serve.py'], 'port': port,
                 'log_destination': str(parent / 'runs.jsonl'), 'ready': False}
        stdout_path, stderr_path = folder / 'fault_stdout.txt', folder / 'fault_stderr.txt'
        with stdout_path.open('x') as stdout, stderr_path.open('x') as stderr:
            child = subprocess.Popen([sys.executable, 'serve.py'], cwd=ROOT, env=env,
                                     stdout=stdout, stderr=stderr)
            try:
                deadline = time.monotonic() + 60
                while time.monotonic() < deadline:
                    if child.poll() is not None:
                        raise RuntimeError('The isolated server exited during startup; inspect fault_stderr.txt. No hosted model requests have been sent for this trial.')
                    try:
                        # TCP readiness only: do not add an eleventh health request.
                        with socket.create_connection(('127.0.0.1', port), timeout=.25):
                            break
                    except OSError:
                        time.sleep(.1)
                else:
                    raise RuntimeError('The isolated server did not start within 60 seconds; inspect fault_stderr.txt. No hosted model requests have been sent for this trial.')
                setup['ready'] = True
                write_json(folder / 'fault_setup.json', setup)
                for slot in range(1, 11):
                    save_client(handle, args, 'logging_failure', slot,
                                f'http://127.0.0.1:{port}/health', None, context,
                                method='GET', timeout=30)
            except Exception as exc:
                setup['setup_or_collection_error'] = f'{type(exc).__name__}: {exc}'
                write_json(folder / 'fault_setup.json', setup)
                raise
            finally:
                child.terminate()
                try:
                    child.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait(timeout=10)


def collect(args):
    import certifi
    if args.trial not in (1, 2, 3):
        raise ValueError('Trial must be 1, 2 or 3.')
    revision, criteria_hash = preflight(args)
    folder = args.out / f'trial{args.trial}'
    folder.mkdir(exist_ok=False)
    metadata = {'purpose': 'Formal capstone trial', 'trial': args.trial,
                'collector_checkout_revision': revision, 'criteria_sha256': criteria_hash,
                'started_at': dt.datetime.now(dt.timezone.utc).isoformat(),
                'finished': False, 'query': QUERY,
                'order': ['local_logging_failure', 'hosted_warmup', 'hosted_ask', 'hosted_health']}
    write_json(folder / 'metadata.json', metadata)
    context = ssl.create_default_context(cafile=certifi.where())
    print(f'Trial {args.trial}: local fault test first; then one hosted warm-up, five measured outfit requests and five health requests.', flush=True)
    print('Measured requests serve criteria 1, 3 and 4 together. No failed request is replaced.', flush=True)
    with (folder / 'client_requests.jsonl').open('x', encoding='utf-8') as handle:
        fault_trial(args, folder, handle, context)
        url = args.base_url.rstrip('/')
        save_client(handle, args, 'warmup', 1, url + '/ask', {'query': QUERY}, context)
        time.sleep(PAUSE)
        for slot in range(1, 6):
            save_client(handle, args, 'ask', slot, url + '/ask', {'query': QUERY}, context)
            if slot < 5:
                time.sleep(PAUSE)
        for slot in range(1, 6):
            save_client(handle, args, 'health', slot, url + '/health', None,
                        context, method='GET', timeout=30)
    metadata.update(finished=True, finished_at=dt.datetime.now(dt.timezone.utc).isoformat())
    write_json(folder / 'metadata.json', metadata)
    print(f'Saved {folder}. Export Vercel logs into {folder / "vercel_runtime.jsonl"} now using --since 30m.', flush=True)


def generated(row):
    body = row.get('response')
    return (row.get('http_status') == 200 and not row.get('transport_error')
            and isinstance(body, dict) and not body.get('error')
            and isinstance(body.get('outfit_suggestion'), str) and bool(body['outfit_suggestion'].strip())
            and isinstance(body.get('fit_card'), str) and bool(body['fit_card'].strip()))


def number(value):
    return type(value) in (int, float) and value >= 0


def matching_log(row, records):
    record = records.get(row['request_id'])
    if record is None:
        return None
    if record['input'] != row['input'] or record['status_code'] != row['http_status']:
        raise ValueError(f'Input/status mismatch for request {row["request_id"]}')
    if row['transport_error'] is None and record['output'] != row['response']:
        raise ValueError(f'Output mismatch for request {row["request_id"]}')
    return record


def score_trial(folder):
    metadata = read_json(folder / 'metadata.json')
    if not metadata.get('finished'):
        raise ValueError(f'{folder} is incomplete. Preserve the partial output and investigate before repeating any model requests.')
    rows = [json.loads(line) for line in (folder / 'client_requests.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    groups = {kind: [row for row in rows if row['kind'] == kind]
              for kind in ('warmup', 'ask', 'health', 'logging_failure')}
    expected = {'warmup': 1, 'ask': 5, 'health': 5, 'logging_failure': 10}
    if len(rows) != sum(expected.values()) or {key: len(value) for key, value in groups.items()} != expected:
        raise ValueError(f'{folder}: request counts differ from the fixed plan. No result can be silently replaced or omitted.')
    for kind, entries in groups.items():
        if [row['slot'] for row in entries] != list(range(1, expected[kind] + 1)):
            raise ValueError(f'{folder}: {kind} slots are duplicated or out of order.')
        if any(row['trial'] != metadata['trial'] for row in entries):
            raise ValueError(f'{folder}: responses belong to a different trial.')
    records = application_records(folder / 'vercel_runtime.jsonl')
    identifiers = [row['request_id'] for row in rows if row['request_id']]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError(f'{folder}: repeated application request IDs; cannot attribute records safely.')
    stderr = (folder / 'fault_stderr.txt').read_text(encoding='utf-8', errors='replace')
    details = {i: [] for i in NAMES}
    selected = {}
    missing = []
    for row in groups['ask']:
        log = matching_log(row, records)
        if log:
            selected[log['request_id']] = log
        else:
            missing.append({'kind': 'ask', 'slot': row['slot'], 'request_id': row['request_id']})
        c1 = completed(row) and generated(row) and isinstance(row['response'].get('selected_item'), dict)
        c3 = (generated(row) and log is not None and log.get('cache_enabled') is False
              and number(row['client_elapsed_ms']) and row['client_elapsed_ms'] <= 45000)
        usage = log.get('model_usage', {}) if log else {}
        c4 = (generated(row) and log is not None and log.get('cache_enabled') is False
              and type(usage.get('model_attempts')) is int and usage['model_attempts'] >= 2
              and type(usage.get('reported_total_tokens')) is int and usage['reported_total_tokens'] > 0)
        for criterion, passed in ((1, c1), (3, c3), (4, c4)):
            details[criterion].append({'slot': row['slot'], 'passed': bool(passed),
                                       'client_response': row, 'application_record': log})
    for row in groups['health']:
        log = matching_log(row, records)
        if log:
            selected[log['request_id']] = log
        else:
            missing.append({'kind': 'health', 'slot': row['slot'], 'request_id': row['request_id']})
        passed = (log is not None and {'timestamp', 'input', 'output', 'status_code', 'duration_ms'} <= log.keys()
                  and isinstance(log.get('timestamp'), str) and bool(log['timestamp'])
                  and number(log.get('duration_ms')))
        details[2].append({'slot': row['slot'], 'passed': passed,
                           'client_response': row, 'application_record': log})
    for row in groups['logging_failure']:
        error_lines = [line for line in stderr.splitlines()
                       if row['request_id'] and row['request_id'] in line and 'Could not save request' in line]
        passed = (row['http_status'] == 200 and row['run_log'] == 'failed'
                  and row['transport_error'] is None and bool(error_lines))
        details[5].append({'slot': row['slot'], 'passed': passed,
                           'client_response': row, 'stderr_lines': error_lines})
    scores = {str(i): {'criterion': NAMES[i], 'passed': sum(x['passed'] for x in details[i]),
                       'total': TARGETS[i][1], 'required': TARGETS[i][0]} for i in NAMES}
    for score in scores.values():
        score['verdict'] = 'MET' if score['passed'] >= score['required'] else 'MISSED'
    result = {'trial': metadata['trial'], 'criteria_sha256': metadata['criteria_sha256'],
              'warmup': {'client_response': groups['warmup'][0],
                         'application_record': matching_log(groups['warmup'][0], records)},
              'scores': scores, 'missing_hosted_records': missing,
              'scope': 'Criteria 1–4: public Vercel API. Criterion 5: isolated local HTTP instance.',
              'details': {str(i): details[i] for i in NAMES},
              'limitations': 'Counts test the stated observable fields, not outfit quality, token-accounting accuracy or an actual Vercel storage outage. A missing export record is observed missing evidence; its cause still needs diagnosis.'}
    write_json(folder / 'assessment.json', result)
    (folder / 'matched_application_records.jsonl').write_text(''.join(
        json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n' for row in selected.values()), encoding='utf-8')
    return result


def summarize(args):
    plan = read_json(args.out / 'evaluation_plan.json')
    if digest(ROOT / 'criteria.md') != plan['file_sha256']['criteria.md']:
        raise ValueError('The current criteria differ from the trial plan. Preserve the original targets and evidence.')
    trials = [score_trial(args.out / f'trial{i}') for i in (1, 2, 3)]
    if [trial['trial'] for trial in trials] != [1, 2, 3]:
        raise ValueError('Each trial folder must contain its own trial number, 1, 2 and 3.')
    ids = []
    for trial in trials:
        observed = [trial['warmup']['client_response']]
        observed += [entry['client_response'] for i in ('1', '2', '5') for entry in trial['details'][i]]
        ids.extend(row['request_id'] for row in observed if row['request_id'])
    if len(ids) != len(set(ids)):
        raise ValueError('Repeated request IDs across trials; cannot treat copied or reused responses as independent runs.')
    expected_hash = plan['file_sha256']['criteria.md']
    if any(trial['criteria_sha256'] != expected_hash for trial in trials):
        raise ValueError('Trials do not share the frozen criteria revision.')
    table = ['| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |',
             '|---|---|---|---|---|---|']
    verdicts = {}
    for i in NAMES:
        scores = [trial['scores'][str(i)] for trial in trials]
        verdict = 'MET' if all(score['verdict'] == 'MET' for score in scores) else 'MISSED'
        verdicts[str(i)] = verdict
        table.append(f'| {i}. {NAMES[i]} | {TARGETS[i][0]} of {TARGETS[i][1]} | '
                     + ' | '.join(f'{score["passed"]}/{score["total"]}' for score in scores)
                     + f' | {verdict} |')
    lines = ['### Run Log — Before', '',
             'Three formal trials with unchanged code and criteria. Criteria 1, 3 and 4 share each trial\'s five measured outfit requests; the one warm-up attempt is excluded. Criterion 2 uses five hosted health requests per trial. Criterion 5 uses ten health requests per trial in an isolated local instance with an invalid log destination.', '',
             *table, '', 'These counts check the stated response/log conditions; they do not judge outfit quality or establish accurate API billing.', '']
    producers = {1: 'agent.py::run_agent, returned over HTTP by serve.py::ask',
                 2: 'serve.py::finish_request_record and run_log.py::append_record, recovered from Vercel runtime logs',
                 3: 'tools/measure_capstone.py::request_once (monotonic client elapsed time)',
                 4: 'serve.py::model_usage_snapshot and serve.py::finish_request_record',
                 5: 'serve.py::finish_request_record (failure header and stderr error), triggered by tools/evaluate_capstone.py::fault_trial'}
    for i in NAMES:
        # Include a miss when one exists; otherwise show the first actual observation.
        examples = [entry for trial in trials for entry in trial['details'][str(i)]]
        example = next((entry for entry in examples if not entry['passed']), examples[0])
        lines += [f'**Criterion {i} — real output:** {producers[i]}.', '',
                  '```json', json.dumps(example, ensure_ascii=False, indent=2), '```', '']
    lines += ['All responses, logs, stderr captures and per-request assessments remain in the trial folders. This report is a draft artifact; the README has not been edited.', '']
    (args.out / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    write_json(args.out / 'summary.json', {'purpose': 'Formal three-trial baseline evaluation',
               'verdicts': verdicts, 'trials': [{'trial': t['trial'], 'scores': t['scores'],
                    'missing_hosted_records': t['missing_hosted_records']} for t in trials]})
    print('\n'.join(table))
    for trial in trials:
        if trial['missing_hosted_records']:
            print(f'Trial {trial["trial"]}: {len(trial["missing_hosted_records"])} hosted records were not recovered. Check export timing, pagination and the actual server behavior before diagnosing.')
    print(f'Saved {args.out / "summary.json"} and {args.out / "report.md"}. README unchanged; review the real results before adding them.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    command = commands.add_parser('collect', help='Run one formal trial, including the isolated local fault test.')
    command.add_argument('--out', type=Path, required=True)
    command.add_argument('--trial', type=int, choices=(1, 2, 3), required=True)
    command.add_argument('--base-url', default='https://fitfindr-capstone.vercel.app')
    command.set_defaults(action=collect)
    command = commands.add_parser('summarize', help='Tally all three trials after each runtime export is saved; never edit README.')
    command.add_argument('--out', type=Path, required=True)
    command.set_defaults(action=summarize)
    args = parser.parse_args()
    try:
        args.action(args)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        parser.exit(1, f'{type(exc).__name__}: {exc}\nPreserve the existing files. Do not repeat hosted model requests automatically.\n')


if __name__ == '__main__':
    main()
