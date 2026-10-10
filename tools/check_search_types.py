"""Fixed search-quality checks defined before the Milestone 5 tool change."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent import parse_query
from mcp_client import call_tool

JACKETS = ["lst_004", "lst_007", "lst_010", "lst_018", "lst_022", "lst_032", "lst_036"]
TEES = ["lst_002", "lst_006", "lst_033"]
SNEAKERS = ["lst_019", "lst_035"]
CASES = [
    ("90s track jacket size M", JACKETS, ["lst_004", "lst_022", "lst_032"]),
    ("vintage jacket under $50", JACKETS, ["lst_004", "lst_007", "lst_010", "lst_018"]),
    ("vintage graphic tee under $30", TEES, TEES),
    ("platform sneakers under $60", SNEAKERS, SNEAKERS),
    ("denim jacket under $50", JACKETS, ["lst_007"]),
    ("vintage", None, []),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", choices=["before", "after"], required=True)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parents[1] / "results"
    path = directory / f"search_type_{args.label}.json"
    if path.exists():
        parser.error(f"Evidence already exists: {path}; do not overwrite it.")
    records = []
    for query, allowed, required in CASES:
        results = call_tool("search_listings", parse_query(query))
        ids = [item["id"] for item in results]
        wrong = [item for item in ids if allowed is not None and item not in allowed]
        missing = [item for item in required if item not in ids]
        records.append({"query": query, "allowed_ids": allowed, "required_ids": required,
                        "results": results, "wrong_type_ids": wrong,
                        "missing_required_ids": missing,
                        "pass": not wrong and not missing if allowed else None})
        print(query, "=>", ids, "wrong type:", wrong, "missing:", missing)
    evidence = {"purpose": "Supplementary search-type test; original five criteria unchanged.",
                "producer": "tools/check_search_types.py::main via mcp_client.call_tool",
                "cases": records}
    if args.label == "after":
        before = json.loads((directory / "search_type_before.json").read_text())
        evidence["untyped_query_unchanged"] = records[-1]["results"] == before["cases"][-1]["results"]
        evidence["previous_valid_results_preserved"] = all(
            {x["id"] for x in old["results"] if x["id"] in old["allowed_ids"]}
            <= {x["id"] for x in new["results"]}
            for old, new in zip(before["cases"][:-1], records[:-1]))
        print("Untyped query unchanged:", evidence["untyped_query_unchanged"])
        print("Previous valid results preserved:", evidence["previous_valid_results_preserved"])
    path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")
    print("Saved", path)


if __name__ == "__main__":
    main()
