#!/usr/bin/env python3
"""
FitFindr over HTTP. ← UNIT 9

    python serve.py                       run it on your machine
    gunicorn serve:app                    run it the way a host runs it

Everything else in this repo exits after one command. A host has nothing to
keep running, so a command line cannot be deployed. This file is the smallest
thing that can: it starts a web server, waits, and hands each request to the
same `run_agent()` your CLI calls. **No new agent logic lives here.** If your
loop works from `python app.py ask`, it works from here; if it doesn't, fix it
there, not in this file.

Two routes:

    POST /ask       {"query": "vintage graphic tee under $30",
                     "wardrobe": {...}}     ← wardrobe is optional
    GET  /health    is it awake?

`/ask` returns the session dict from `run_agent()` as JSON, unchanged — the
same keys you print from the command line, including `error`. Read
`session["error"]` first, exactly as you do everywhere else.

It runs **one request at a time**, and one route is deliberately slower than a
web server has to be. The reason is worth reading before you deploy: see the
note above `_one_at_a_time` below — it also decides which gunicorn worker you
can use.

Capstone instrumentation records each completed HTTP request in JSON Lines,
including rejected requests and errors. Timing is server-side elapsed time,
including queueing; it is not CPU time or network round-trip latency.
"""

import datetime as dt
import json
import os
import sys
import threading
import time
import uuid

# config first, and before anything that talks to the model: it loads your .env
# and fixes the Windows console encoding for every module that imports it.
import config  # noqa: F401

from flask import Flask, g, got_request_exception, jsonify, request

import generate
import run_log

from agent import run_agent
from utils.data_loader import get_example_wardrobe

app = Flask(__name__)


# ── one request at a time ─────────────────────────────────────────────────────
# Here's why this exists.
#
# A web server will happily run two requests at once. Two things in this repo
# assume otherwise:
#
#   • If you moved a tool onto MCP in unit 4, `mcp_client.call_tool` starts
#     `mcp_server.py` as a separate process over stdio, one per call. Two
#     overlapping requests means two extra Python interpreters, and the free
#     tier you're deploying to has 512 MB for all of it. That is the reason
#     that would still be here even if everything else were perfect.
#   • `generate.py`'s pacing window and its call counter are plain module
#     globals — deliberately, because that file is teaching pacing and quota,
#     not locking. Two threads sharing them means the per-minute limiter is
#     counting something that isn't true.
#
# What the lock covers is exactly the agent run: the part that spawns
# processes and calls the model. Reading the request, rejecting a bad one, and
# turning the answer into JSON all happen outside it — so a request with a
# malformed body comes straight back with a 400 instead of queueing behind
# somebody else's agent.
#
# Serialising the runs costs you nothing here — this is one user asking one
# question — and it keeps the deployed behaviour identical to the CLI's. When
# that stops being an acceptable trade, the fix is a real queue, not a bigger
# lock.
#
# The same constraint decides your start command, and this is the part that
# bites in deployment rather than on your machine. `mcp_client.call_tool`
# wraps `asyncio.run()`, and `asyncio.run()` refuses to start when an event
# loop is already running. An async worker always has one running. So under
# `gunicorn -k gevent` (or `-k eventlet`, or `serve:app` wrapped for an ASGI
# server like uvicorn) EVERY MCP call fails with "asyncio.run() cannot be
# called from a running event loop" — not some of them under load, all of
# them, every time, in a place your laptop never showed you.
#
#     gunicorn serve:app              ← right: the DEFAULT sync worker
#     gunicorn -k gevent serve:app    ← breaks every MCP call you make

_one_at_a_time = threading.Lock()


def decode_record_json(text):
    """Keep non-standard JSON numbers as raw text, not invalid JSONL floats."""
    def reject_constant(value):
        raise ValueError(f"Non-standard JSON number: {value}")
    return json.loads(text, parse_constant=reject_constant)


@app.before_request
def begin_request_record():
    """Capture input before validation; retain malformed bodies as raw text."""
    g.run_started = time.perf_counter()
    g.run_timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")
    g.run_id = uuid.uuid4().hex
    g.queue_ms = 0.0
    g.agent_ms = 0.0
    g.run_exception = None
    g.model_usage = {"model_attempts": 0, "reported_prompt_tokens": 0,
                     "reported_output_tokens": 0, "reported_total_tokens": 0}
    raw = request.get_data(cache=True, as_text=True)
    if request.is_json:
        try:
            g.run_input = decode_record_json(raw)
            g.input_format = "json"
            return
        except (ValueError, TypeError):
            pass
    g.run_input = {"raw": raw} if raw else None
    g.input_format = "raw" if raw else "empty"


def note_unhandled_exception(sender, exception, **extra):
    """Observe framework errors without changing the existing error response."""
    g.run_exception = f"{type(exception).__name__}: {exception}"


got_request_exception.connect(note_unhandled_exception, app, weak=False)


@app.after_request
def finish_request_record(response):
    """Save one record for the HTTP response, including non-2xx responses.

    A log-storage failure is exposed in a header and stderr. It must not erase
    a result already produced by the agent or pretend the record was saved.
    """
    response_text = response.get_data(as_text=True)
    output = {"raw": response_text}
    output_format = "raw"
    if response.is_json:
        try:
            output = decode_record_json(response_text)
            output_format = "json"
        except (ValueError, TypeError):
            pass
    error = g.run_exception or (output.get("error") if isinstance(output, dict) else None)
    outcome = ("error" if response.status_code >= 500 else
               "rejected" if response.status_code >= 400 else
               "stopped" if error else "success")
    record = {
        "timestamp": g.run_timestamp,
        "request_id": g.run_id,
        "method": request.method,
        "path": request.path,
        "input_format": g.input_format,
        "input": g.run_input,
        "output_format": output_format,
        "output": output,
        "status_code": response.status_code,
        "outcome": outcome,
        "error": error,
        "duration_ms": round((time.perf_counter() - g.run_started) * 1000, 3),
        "queue_ms": g.queue_ms,
        "agent_ms": g.agent_ms,
        "configured_model": config.MODEL,
        "cache_enabled": config.CACHE_ENABLED,
        "model_usage": g.model_usage,
    }
    response.headers["X-Request-ID"] = g.run_id
    try:
        run_log.append_record(record)
    except (OSError, TypeError, ValueError) as exc:
        response.headers["X-Run-Log"] = "failed"
        app.logger.error("Could not save request %s: %s", g.run_id, exc)
    else:
        response.headers["X-Run-Log"] = "saved"
        if config.RUN_LOG_STDOUT:
            try:
                run_log.mirror_record(record)
            except OSError as exc:
                app.logger.error("Saved request %s but could not mirror it: %s", g.run_id, exc)
    return response


def model_usage_snapshot():
    """Cumulative adapter counters. Read before/after a run inside the lock.

    Attempts include retries, not just successful answers. Token counts are
    what the provider reported to the existing adapter; missing metadata is
    not proof that a request used zero tokens or incurred zero spend.
    """
    tokens = generate.token_counts()
    return {"model_attempts": generate.call_count(),
            "reported_prompt_tokens": tokens["prompt"],
            "reported_output_tokens": tokens["output"],
            "reported_total_tokens": tokens["total"]}


@app.get("/health")
def health():
    """Is the server awake? A host pings something like this to find out."""
    return jsonify({"status": "ok"})


@app.post("/ask")
def ask():
    """
    Run the agent on one query.

    In:   {"query": "...", "wardrobe": {...}}   wardrobe optional — leave it
                                                out and you get the same
                                                example wardrobe the CLI uses.
    Out:  the session dict from run_agent(), as JSON.
    """
    payload = request.get_json(silent=True) or {}
    query = (payload.get("query") or "").strip()
    if not query:
        # 400 rather than a stack trace: the caller can act on this one.
        return jsonify({"error": "Send JSON with a 'query' field, e.g. "
                                 '{"query": "vintage graphic tee under $30"}'}), 400

    wardrobe = payload.get("wardrobe")
    if not isinstance(wardrobe, dict):
        wardrobe = get_example_wardrobe()

    # A queued request should look like a queued request. Without this the
    # second caller just sits there, and "slow" and "waiting its turn" are
    # indistinguishable from the outside — which is how people conclude the
    # deployment is broken when it is behaving exactly as designed.
    #
    # This is NOT the logging you add in the follow-along. It prints nothing
    # on the normal path, carries no timing and counts nothing; it says only
    # that this request had to wait. `locked()` can be a moment out of date,
    # so the note is occasionally missed — which costs nothing, because
    # nothing depends on it.
    if _one_at_a_time.locked():
        print(
            "  [serve] another request is still running. This one is waiting "
            "its turn — serve.py handles one at a time, on purpose.",
            file=sys.stderr,
            flush=True,
        )

    failure = None
    session = None
    queued_at = time.perf_counter()
    with _one_at_a_time:
        acquired_at = time.perf_counter()
        g.queue_ms = round((acquired_at - queued_at) * 1000, 3)
        usage_before = model_usage_snapshot()
        try:
            session = run_agent(query, wardrobe)
        except Exception as exc:  # noqa: BLE001 — a 500 with a sentence beats a hang
            failure = f"{type(exc).__name__}: {exc}"
            g.run_exception = failure
        finally:
            usage_after = model_usage_snapshot()
            g.model_usage = {key: usage_after[key] - usage_before[key]
                             for key in usage_before}
            g.agent_ms = round((time.perf_counter() - acquired_at) * 1000, 3)

    # Outside the lock: building a response is not work the next caller should
    # be waiting on.
    if failure is not None:
        return jsonify({"error": failure}), 500

    return jsonify(session)


if __name__ == "__main__":
    # PORT and 0.0.0.0 are not decoration. A host tells you which port to
    # listen on through PORT, and it reaches your process from outside the
    # container — bind 127.0.0.1 and nothing but the container itself can
    # connect, which looks exactly like a broken app from the browser.
    port = int(os.getenv("PORT", "5000"))

    # Never on by default. Flask's debugger executes code typed into a browser,
    # and a deployed app with it on is a stranger's shell. Set AI201_DEBUG=1 in
    # your own terminal when you want the reloader.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"\nFitFindr is listening on http://localhost:{port}")
    print("It runs one request at a time — a second one waits for the first.")
    print("Ask it something (single quotes, as always):\n")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"query\": \"vintage graphic tee under $30\"}}'\n"
    )
    print(f"Request log: {config.RUN_LOG_PATH}")
    print("Ctrl-C to stop.\n")

    app.run(host="0.0.0.0", port=port, debug=debug)
