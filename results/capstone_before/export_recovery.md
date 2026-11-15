# Formal-trial runtime export recovery

The first tally found six records missing from each immediate export for trials 2 and 3: the last measured outfit request and all five health requests. Their client responses had matching request IDs and `X-Run-Log: saved`.

A later read-only Vercel export using the same project, environment and `--since 30m` recovered the original hosted records. Inputs, outputs and HTTP statuses were checked against the original client files. This is consistent with delayed availability of the latest log entries; no exact platform mechanism is asserted. No requests, warm-ups or trials were repeated, and no code, criteria or original client responses were changed.

Each trial's immediate export is preserved as `vercel_runtime_initial.jsonl`, and its first assessment as `assessment_initial_export.json`. The root initial summary/report are retained with `_initial_export` names. The shared later export is `vercel_runtime_recovery.jsonl`. Each active `vercel_runtime.jsonl` combines its original export with that later export; the unchanged parser deduplicates identical application records by request ID.

The initial tally is an incomplete-export diagnostic, not an independent trial or a before/after system improvement. The final baseline assessment uses the recovered records for the same original requests.
