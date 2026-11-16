# Running FitFindr

See **Capstone — Vercel** below for current deployment instructions. The course commands remain useful for running the existing agent.

---

## Before your first class

Setup happens **before class**. The [environment setup page](../pages/ide_setup)
has the per-operating-system commands and the exact versions.

**Same API key you set up in unit 1.** Nothing new to sign up for. There is one
new package — the MCP SDK, for unit 4 — and it installs with everything else.

From inside this repo after you've forked and cloned it:

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then paste your key into .env
python test.py
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env         # then paste your key into .env
python test.py
```

**You're ready when `python test.py` passes.**

If it doesn't and you've made one honest attempt at the error, post the
**whole** output in the help channel.

> Activate the virtual environment every time you open a new terminal. You
> should see `(.venv)` at the start of your prompt.

---

## Your first five minutes

Start with the data. Your tools will only be as good as your understanding of
what they're reading, and ten minutes here saves an hour of confused debugging.

```bash
python app.py fields                    # what a listing and a wardrobe item hold
python app.py listings --full -n 6      # read six listings all the way through
python app.py examples                  # queries worth trying
python app.py ask 'vintage graphic tee under $30'
```

> **Quote your queries with single quotes**, on every operating system. In
> PowerShell, `"vintage graphic tee under $30"` in double quotes silently
> becomes `vintage graphic tee under ` — PowerShell reads `$30` as a variable
> and substitutes nothing. You get results with no price ceiling and no error
> saying so. Single quotes are literal in PowerShell, bash and zsh alike.

That last command now runs the implemented agent. The original starter had stubs; Units 3 and 4 supplied the tools, planning loop and MCP search.

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment. Run it whenever something feels off |
| `python app.py fields` | The fields a listing and a wardrobe item have — **Milestone 1** |
| `python app.py listings` | Browse the data. `--full` for whole records, `-n` for how many |
| `python app.py examples` | Queries worth trying, including one that matches nothing |
| `python app.py ask '...'` | Run the agent on one query — **single quotes** |
| `python app.py ask` | Keep asking until you press Enter on an empty line |
| `python agent.py` | Runs both example paths — one that matches, one that can't |
| `python mcp_server.py` | Starts your MCP server — **unit 4** |
| `python mcp_client.py` | Asks the server what it offers — **unit 4** |
| `python run_eval.py --label before` | Runs every scenario five times and writes the run log — **unit 4** |
| `python serve.py` | Serves the agent over HTTP instead of exiting — **unit 9** |

Useful flags on `ask`:

| Flag | What it does |
|---|---|
| `--trace` | Print the loop step by step, once you've added the trace calls |
| `--empty-wardrobe` | Run as a user with nothing saved — one of unit 4's failure modes |

---

## Which command goes with which milestone

### Unit 3 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Read the data, run the starter | `app.py fields`, `app.py listings --full`, `app.py ask` |
| 2 | Spec your three tools | README, **Tool Inventory** |
| 3 | Write your acceptance criteria | `criteria.md` |
| 4 | Build the three tools | `tools.py`, tested one at a time from a terminal |
| 5 | Wire the loop and the state | `agent.py::run_agent` |
| 6 | Write it up | README |

### Unit 4 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Move one tool onto MCP | `mcp_server.py`, then `mcp_client.call_tool` in `run_agent` |
| 2 | Break it on purpose, then trace it | `trace.py`, `app.py ask --trace` |
| 3 | Run your test | `scenarios.py`, then `run_eval.py --label before` |
| 4 | Call each criterion, diagnose the misses | README |
| 5 | Fix one thing and re-run | `run_eval.py --label after` |
| 6 | Say what's still broken | README |

---

## Capstone — Vercel (Shape A, Path A)

**Public API:** https://fitfindr-capstone.vercel.app. Verified without Vercel authentication: `/health` returns 200; MCP empty search returns guidance; missing query returns 400. Request records were recovered from runtime logs. Clean local-checkout verification passed at `994e563` using a new Python 3.13 environment; its record is in `results/capstone_clean_checkout_check.json`. The ten-run hosted measurement is now recorded in `results/capstone_m3/summary.json`: 10/10 completed outfits, 11 recovered records including the rejected-input example, and 20 model attempts. Formal before and after evaluations have now run three trials per criterion; see `results/capstone_before/summary.json`, `results/capstone_after/summary.json` and the Capstone comparison in the README. Push the new capstone commits before following the GitHub clone command below; they were not yet on the remote when checked.

### Environment and installation

Use Python **3.13** (local verification environment: **3.13.15**). The host reads `.python-version`. There is no local model download: FitFindr calls the Gemini API and reads the small JSON files in `data/`. MCP starts another Python interpreter. `mcp_client.py::_server_parameters` passes the parent import paths explicitly so that the child can find Vercel-vendored packages, uses the source directory as its working directory, and disables bytecode writes. It does not pass the API key to the search subprocess. `requirements.txt` keeps the course version bounds; `requirements.lock` constrains all 48 application dependencies to the versions used for this build. Vercel prioritizes `pyproject.toml`, so its deployment dependency list mirrors those same 48 pins. Update both lists together.

From a fresh terminal, outside another repository:

```bash
git clone https://github.com/bhuvan1201/ai201-project2-fitfindr-starter-v2026.git
cd ai201-project2-fitfindr-starter-v2026
python3.13 -m venv "$HOME/.venvs/fitfindr-capstone-py313"
source "$HOME/.venvs/fitfindr-capstone-py313/bin/activate"
python -m pip install -r requirements.txt
cp .env.example .env
```

Enter your own `GEMINI_API_KEY` in `.env`. Keep this file private. If the repository is in iCloud, keeping the virtual environment outside the synced folder avoids offloaded package files interrupting Python.

With that environment active, this single command starts the HTTP service locally:

```bash
AI201_CACHE=0 FITFINDR_LOG_STDOUT=1 python serve.py
```

In a second terminal:

```bash
curl -i http://127.0.0.1:5000/health
curl -i http://127.0.0.1:5000/ask \
  -H 'Content-Type: application/json' \
  -d '{"query":"90s track jacket in size M"}'
```

The second request uses the real model and can consume API quota. The existing `app.py` command-line interface still works.

### Deploy to Vercel

The Flask app is exported as `serve:app` in `pyproject.toml`, so Vercel does not mistake the existing CLI `app.py` for the web entrypoint. Vercel runs the WSGI app itself; no Gunicorn start-command override is needed. `vercel.json` selects Flask and a 300-second maximum function duration; that limit is configuration, not a measured response-time promise.

Deployment currently uses the CLI; GitHub auto-deploy is not configured. Use the checked CLI version, then select your own account and the FitFindr project:

```bash
npx --yes vercel@65.16.0 login
npx --yes vercel@65.16.0 link
npx --yes vercel@65.16.0 env add GEMINI_API_KEY --environment production --sensitive
npx --yes vercel@65.16.0 deploy --prod
```

Paste the key only into Vercel's private environment-variable prompt. Do not put it in a command argument or a committed file. If you also deploy previews, add the key to the preview environment separately. `.vercelignore` excludes `.env`, local environments, old results and logs from uploads. `.vercel/` and downloaded local environment files are Git-ignored.

The committed configuration sets these non-secret runtime values:

| Setting | Value and purpose |
|---|---|
| `FITFINDR_RUN_LOG` | `/tmp/fitfindr/capstone_runs.jsonl` — Vercel's application directory is read-only |
| `FITFINDR_LOG_STDOUT` | `1` — also send each saved JSON record to runtime logs |
| `AI201_CACHE` | `0` — no writes to the repository cache and no cached model answers in measurements |
| `AI201_DEBUG` | `0` — normal model-adapter logging |

### Preserve the run record

Request records contain UTC time, input, output, status, elapsed milliseconds, queue and agent time, and per-request reported model usage. `X-Request-ID` connects the HTTP response to its record; check `X-Run-Log: saved` too. Details are under README → Capstone → Build.

Vercel's `/tmp` file is temporary and belongs to one function instance. It is not a complete shared history across instances or deployments. Capture the mirrored records from the project's **Logs** page, or use the linked CLI project:

```bash
mkdir -p results
npx --yes vercel@65.16.0 logs --environment production --since 30m --json > results/capstone_vercel_runtime_logs.jsonl
```

Vercel Hobby retains runtime logs for one hour. Export immediately with `--since 30m`; requesting a two-hour window is rejected. A failed CLI export can leave an empty redirected file. Check its exit status and recover logs before repeating model requests.

Keep the raw export, extract the actual application JSON records, and commit the evidence in the same session. Paste at least ten real request records into the README, including a failure. Do not use development fixtures as evidence.

Run measurements sequentially. The agent lock, pacing and usage counters are per process, not global across Vercel instances. `duration_ms` measures server-side wall time from the Flask request hook, including that lock's queue; it excludes network time, platform queueing, initialization before the hook and log writing. `agent_ms` includes API waits and retries. Record cold versus warm requests explicitly. A platform hard timeout can terminate the function before a final record is written, so also retain client responses and Vercel errors.

For the required cost number, measure ten real runs and report their mean elapsed seconds and reported token totals. Missing usage metadata is not evidence of zero API spend. Do not describe elapsed wall time as CPU time. Acceptance criteria must be written and committed before formal evaluation runs.

[Vercel Flask entrypoint guide](https://vercel.com/docs/frameworks/backend/flask), [Python runtime](https://vercel.com/docs/functions/runtimes/python), [runtime filesystem](https://vercel.com/docs/functions/runtimes), [CLI runtime logs](https://vercel.com/docs/cli/logs).

---


### Formal after trials and verified log export

The Milestone 6 change is in the local evidence-capture workflow. The hosted agent, prompts, application logging and criteria are unchanged, so this change does not require redeploying the API. Commit the updated evaluation tool before collecting; its preflight checks enforce committed inputs and a frozen plan across the three trials.

With the documented Python environment active, repeat these two commands for trials 1, 2 and 3:

```bash
python tools/evaluate_capstone.py collect --label after --trial 1 --out results/capstone_after
python tools/evaluate_capstone.py export-logs --trial 1 --out results/capstone_after
```

The second command checks the five measured request IDs and five health request IDs against recovered application records. It uses the existing Vercel account with CLI 65.16.0 and a 30-minute window. It retries only log retrieval, with a limit of six attempts per invocation and a five-second delay. Raw snapshots, stderr and `log_export_audit.json` record the attempts and completeness. The three warm-ups across the trials stay outside the acceptance scores.

If capture fails, preserve its audit and investigate. Additional log-export attempts do not resend model requests. Each new explicit invocation is recorded; do not rerun the outfit collection to replace missing logs or failed responses.

After all three trials and their exports:

```bash
python tools/evaluate_capstone.py summarize --out results/capstone_after
```

This writes an After report and summary with the original scoring rules plus capture-completeness statistics. It does not change the README. The committed `results/capstone_before/` files are the comparison baseline and must be preserved.

---

## Where everything lives

| File | What it does |
|---|---|
| `config.py` | Every setting worth changing — **TEMPERATURE and the cache are at the top** |
| `tools.py` | The three implemented FitFindr tools |
| `agent.py` | The implemented planning loop and session |
| `generate.py` | The only thing that calls out to a service. Handles pacing and quota |
| `trace.py` | The trace helper, and the loop's stop condition |
| `app.py` | The command line |
| `serve.py` | The same agent over HTTP, for deploying — **unit 9** |
| `mcp_server.py` | Your MCP server — **unit 4, you register the tool** |
| `mcp_client.py` | Calling an MCP tool from your agent. Given to you |
| `scenarios.py` | What your test runs. **You fill this in** |
| `run_eval.py` | Runs the scenarios repeatedly and writes the run log |
| `criteria.md` | Your five acceptance criteria. **You fill this in** |
| `data/` | 40 listings and the wardrobe schema |
| `utils/data_loader.py` | Loading the data. Use this rather than reading the files yourself |
| `results/` | Run logs. **Commit these** — they're your evidence |

---

## The two settings people go looking for

Both are at the top of `config.py`, and the brief points at them by name.

If your fit cards come out **word-for-word identical** every time, it is one of:

- **`CACHE_ENABLED`** — while you build, identical prompts reuse the answer
  already received. That's deliberate; it makes debugging free. `run_eval.py`
  turns it off automatically.
- **`TEMPERATURE`** — at `0.0` the model gives you the same words every time.
  It ships at `0.9`.

---

## About rate limits

**This is the heaviest pair in the course for call volume.** Two of your three
tools call the model, so one agent run is several requests, and a few runs back
to back while debugging can cross the per-minute limit.

`generate.py` handles it:

- **It paces itself** and says when it's waiting. **A pause is the starter
  doing its job, not a bug.**
- **It reuses answers** to prompts already sent, while you build.
- **It stops** if a session makes an unreasonable number of calls, rather than
  draining your day's allowance. For an agent, that usually means a loop isn't
  ending — look for that before raising the number.
- **It counts your calls** and prints the total when you exit.

`config.MAX_ITERATIONS` is the loop's own stop condition. Your loop this unit
is short enough that you may never hit it. Keep it — a missing stop condition
is the most common architectural failure in production agents.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `The planning loop isn't built yet` | Correct, at the start. That's the TODO in `agent.py` |
| `No GEMINI_API_KEY found` | No `.env`, or the key wasn't pasted in. On Windows check it didn't save as `.env.txt` |
| A message saying the model couldn't be reached | Usually a bad key. This is also **exactly what unit 4 Milestone 2 asks you to trigger on purpose** |
| `[rate limit] ... Waiting 34s` | Working as intended. Leave it |
| `[serve] another request is still running` | Also working as intended. `serve.py` answers one request at a time; yours is queued behind one that's mid-run |
| `QuotaGuard: This session has made 300 requests` | A loop isn't ending. Find it before raising the budget |
| `The loop ran 11 times, past MAX_ITERATIONS` | Same thing, caught earlier |
| `The server doesn't offer a tool called '...'` | Nothing registered in `mcp_server.py` yet, or the name doesn't match |
| MCP returns a string where you expected a list | You're not going through `mcp_client.call_tool`, which unwraps it |
| Fit cards identical every run | `CACHE_ENABLED` or `TEMPERATURE`. See above |
| `--trace` prints nothing | You haven't added `trace.step()` calls yet — unit 4, Milestone 2 |
| `IncompleteFieldDefinitionWarning: Field 'lifespan'` | Harmless noise from the MCP library's dependencies. Not your code, not an error. Ignore it |
| A price ceiling you typed is being ignored | You used double quotes in PowerShell. `$30` vanished. Use single quotes |
| `UnicodeEncodeError: 'charmap' codec can't encode` | Shouldn't happen — `config.py` sets the console to UTF-8. If you see it, you're running a file that doesn't import `config` |

Still stuck after one honest attempt? Post in the help channel with the full
error, what you ran, and what you expected.

---

## A note on committing

At least four new commits in unit 3, at least four more in unit 4. Your commit
history is what shows your criteria existed before your results did.

**Do not delete and recreate this repository.** You submit the same URL both
units.

`results/` is deliberately **not** in `.gitignore`.
