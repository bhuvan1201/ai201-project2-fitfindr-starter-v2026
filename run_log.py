"""Append-only JSON Lines storage for the capstone's HTTP run records.

One synchronous server worker is supported. The thread lock keeps records
intact when health checks and agent responses finish on different threads.
The hosting filesystem may be ephemeral: commit extracts during measurement.
"""
import json
from pathlib import Path
import threading

_write_lock = threading.Lock()


def _path(path=None):
    if path is None:
        import config
        path = config.RUN_LOG_PATH
    return Path(path)


def append_record(record: dict, *, path=None) -> None:
    """Write one complete UTF-8 JSON object per line, including escaped newlines.

    Serialization and file errors propagate to the caller; a failed append is
    never reported as a saved record. No environment variables or headers are
    added here. The caller supplies the request/response fields to record.
    """
    line = json.dumps(record, ensure_ascii=False, allow_nan=False) + '\n'
    target = _path(path)
    with _write_lock:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('a', encoding='utf-8') as handle:
            handle.write(line)


def read_records(*, path=None) -> list[dict]:
    """Read saved records in order; malformed lines raise rather than disappear."""
    target = _path(path)
    if not target.exists():
        return []
    return [json.loads(line) for line in target.read_text(encoding='utf-8').splitlines()
            if line.strip()]
