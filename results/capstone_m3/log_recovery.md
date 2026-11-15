# Runtime log export recovery

The original export used `--since 2h`. Vercel rejected the requested window as outside this Hobby account's runtime-log retention, leaving an empty export. The initial incomplete summary and report are preserved as `summary_before_log_recovery.json` and `report_before_log_recovery.md`.

The existing logs were recovered with the same project, scope, environment and limit, changing the window to `--since 30m`. No matching queries or model calls were repeated. Client responses and the original collection metadata were not changed. The nullable collector checkout revision remains as originally recorded; it was not filled in after the fact.
