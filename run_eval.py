#!/usr/bin/env python3
"""Five real trials per criterion. Review raw evidence manually to assign verdicts."""
import argparse
from copy import deepcopy
import datetime as dt
import json
from unittest.mock import patch
import traceback

import config
import scenarios as scenario_module


def run_once(scenario, use_trace=True):
    import agent
    import trace as trace_module
    from utils.data_loader import get_example_wardrobe, get_empty_wardrobe

    wardrobe = (get_empty_wardrobe() if scenario["wardrobe"] == "empty"
                else get_example_wardrobe())
    if scenario["wardrobe"] == "single":
        wardrobe["items"] = wardrobe["items"][:1]
    record = {"query": scenario["query"], "wardrobe": deepcopy(wardrobe),
              "session": None, "trace": "", "crashed": None, "calls": []}

    def recorder(name, function):
        def wrapped(*args, **kwargs):
            call = {"tool": name, "args": deepcopy(args), "kwargs": deepcopy(kwargs)}
            record["calls"].append(call)
            try:
                result = function(*args, **kwargs)
                call["returned"] = deepcopy(result)
                return result
            except Exception as exc:
                call["error"] = f"{type(exc).__name__}: {exc}"
                raise
        return wrapped

    # Record real inputs at call entry; delegate to the original tools.
    # These wrappers do not substitute tool results or change agent behavior.
    with patch.object(agent, "call_tool", recorder("search_listings (via MCP)", agent.call_tool)), \
         patch.object(agent, "suggest_outfit", recorder("suggest_outfit", agent.suggest_outfit)), \
         patch.object(agent, "create_fit_card", recorder("create_fit_card", agent.create_fit_card)):
        try:
            record["session"] = agent.run_agent(
                scenario["query"], wardrobe, enable_trace=use_trace)
        except Exception as exc:
            record["crashed"] = f"{type(exc).__name__}: {exc}"
            record["traceback"] = traceback.format_exc()
        finally:
            record["trace"] = trace_module.get_trace() if use_trace else ""
    return record


def write_report(rows, args, path):
    headers = " | ".join(f"Try {i}" for i in range(1, args.tries + 1))
    lines = [
        f"# Run log — {args.label or 'evaluation'}", "",
        "- Produced by: `run_eval.py::main` and `run_eval.py::run_once`",
        "- Agent: `agent.py::run_agent`; search: `mcp_client.call_tool` → `mcp_server.search_listings`",
        "- Model tools: `tools.py::suggest_outfit` and `tools.py::create_fit_card`",
        f"- Caching OFF; temperature: {config.TEMPERATURE}",
        f"- Planned tries per criterion: {args.tries}",
        "- Criterion 3: each try is three consecutive requests in this process.",
        "- Criteria 4 and 5 use five predefined input variants.",
        "- Inputs and returns are deep copies of actual calls, not simulated results.",
        "- Pending cells require manual review; a completed request is not necessarily a pass.",
        "", f"| Criterion | Target | {headers} | Verdict |",
        "|" + "|".join(["---"] * (args.tries + 3)) + "|",
    ]
    for row in rows:
        s = row["scenario"]
        pending = " | ".join(["Pending"] * args.tries)
        lines.append(f"| {s['criterion']}. {s['name']} | {s['target']} | {pending} | Pending |")
    lines += ["", "## Actual evidence", ""]
    for row in rows:
        s = row["scenario"]
        lines += [f"### Criterion {s['criterion']}: {s['name']}", ""]
        for i, trial in enumerate(row["tries"], 1):
            lines += [f"#### Try {i}", ""]
            for j, record in enumerate(trial, 1):
                lines += [f"Request {j}: `{record['query']}`", "",
                          "Trace:", "", "```text", record["trace"], "```", "",
                          "Full session, supplied wardrobe, and actual tool calls:", "",
                          "```json",
                          json.dumps({k: v for k, v in record.items() if k != "trace"},
                                     indent=2, ensure_ascii=False),
                          "```", ""]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path.with_suffix(".json").write_text(
        json.dumps({"cache_enabled": False, "temperature": config.TEMPERATURE,
                    "rows": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tries", "--trials", type=int, default=5, dest="tries")
    parser.add_argument("--label", default="")
    args = parser.parse_args()
    problems = scenario_module.validate()
    if args.tries != 5:
        problems.append("These criteria require exactly five trials, including five fixed variants.")
    if problems:
        parser.error("; ".join(problems))
    config.CACHE_ENABLED = False
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"
    rows = []
    print("Cache OFF. Results are saved after each trial.", flush=True)
    for scenario in scenario_module.SCENARIOS:
        row = {"scenario": scenario, "tries": []}
        rows.append(row)
        for attempt in range(1, args.tries + 1):
            print(f"Criterion {scenario['criterion']}, try {attempt}", flush=True)
            trial = [run_once(request) for request in
                     scenario_module.requests_for_try(scenario, attempt)]
            row["tries"].append(trial)
            write_report(rows, args, path)
    import generate
    print(f"Wrote {path.relative_to(config.ROOT)}", flush=True)
    print(generate.usage(), flush=True)
    print("Review the raw evidence manually before assigning PASS or FAIL.")


if __name__ == "__main__":
    main()
