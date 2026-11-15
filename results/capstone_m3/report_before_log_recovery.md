### Instrumentation

Milestone 3 operational sample: 10 matching attempts and one deliberately rejected input. This is not the formal three-trial criteria evaluation.

Requests were sent and timed by `tools/measure_capstone.py::request_once`; server records were produced by `serve.py::finish_request_record` and saved by `run_log.py::append_record`. Runtime records were recovered by request ID. These are complete recovered application records in client-request order:

```jsonl
```

### What It Costs

- Completed outfits: 10/10 attempts.
- Mean client elapsed time per attempted request: 2.90604 seconds.
- Mean server elapsed time per attempted request: None seconds.
- Mean reported tokens per attempted request: None.
- Reported model usage totals: `null`.

Sequential uncached matching attempts; no warm-up excluded; all attempted runs, including failures, remain in the averages. The rejected-input example is excluded from the cost sample. Client duration is wall time, including network and waits, not CPU time. Pauses between requests are excluded; waits within a request are included. Tokens are provider-reported adapter counters, not verified billing or API dollars.

Both elapsed-time figures measure wall time, not CPU consumption. A zero reported token count, including after a model attempt, does not establish zero token usage or zero spend. No dollar cost is inferred from a pricing page.

Usage records with model attempts but zero reported tokens: 0.

Client responses, original runtime export, matched application records and the numeric summary are saved under `results/capstone_m3`.

**Incomplete measurement evidence:**
- 11 client responses lack recovered application records.
