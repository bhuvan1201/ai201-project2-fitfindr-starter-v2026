# Milestone 5 — focused search comparison

The five typed queries, allowed clothing IDs and required valid IDs were defined in `tools/check_search_types.py` before changing `tools.py`. The same test then ran through MCP before and after. These are supplementary diagnostics, not replacements for the original five criteria.

Commands:

```sh
python tools/check_search_types.py --label before
python tools/check_search_types.py --label after
```

A typed query passes if every returned listing belongs to its declared clothing family and every required valid listing is present. Jackets include bombers, windbreakers, blazers and shackets. Tees and sneakers have separate allowed sets. These expectations are based on the supplied listing titles. The sixth query is a control with no explicit clothing type.

| Query | Wrong-type results before → after | Missing required IDs before → after | Pass before → after |
|---|---|---|---|
| 90s track jacket size M | 2 → 0 | none → none | FAIL → PASS |
| vintage jacket under $50 | 7 → 0 | lst_018 → none | FAIL → PASS |
| vintage graphic tee under $30 | 7 → 0 | none → none | FAIL → PASS |
| platform sneakers under $60 | 1 → 0 | none → none | FAIL → PASS |
| denim jacket under $50 | 4 → 0 | none → none | FAIL → PASS |

Across these query results, wrong-type occurrences dropped from 21 to 0. All previously returned valid results were retained. The complete result dictionaries and ordering for the untyped `vintage` query were unchanged.

Actual returned IDs for the jacket query:

```text
before: ['lst_004', 'lst_022', 'lst_013', 'lst_032', 'lst_034']
after:  ['lst_004', 'lst_022', 'lst_032']
```

The removed items were the silk slip dress (lst_013) and bucket hat (lst_034). For the vintage-jacket query, filtering before the result limit also allowed the valid linen blazer (lst_018) into the returned list.

Evidence: [before JSON](search_type_before.json), [after JSON](search_type_after.json). Produced by `tools/check_search_types.py::main` using `mcp_client.call_tool` → `mcp_server.search_listings` → `tools.py::search_listings`. No model calls are needed for these checks.

## What this does not prove

This checks clothing families, not every word in a request. Other jackets can still appear for a denim-jacket query. The recognized families are jackets, tees and sneakers; unrecognized types keep the existing keyword behavior. Title-based detection can miss an unfamiliar name, and the helper does not interpret negations or distinguish a requested item from a companion item in a complex sentence. No claim of general search accuracy follows from these six queries.
