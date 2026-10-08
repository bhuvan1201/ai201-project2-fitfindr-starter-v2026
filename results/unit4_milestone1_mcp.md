# Unit 4, Milestone 1 — MCP check

The environment check completed with 10 passed and 0 failed. Before changing the search call, the existing agent completed `vintage graphic tee under $30` with two model calls.

## Tool discovery

```text
$ .venv/bin/python mcp_client.py
Asking mcp_server.py what it offers…

  search_listings
    Search local clothing listings by description keywords, optional size, and an inclusive maximum price in dollars; None skips either optional filter.

Return listing dictionaries (id, title, description, category, style_tags,
size, condition, price, colors, brand, platform), ranked by keyword overlap
and limited to the configured result count, or [] when nothing matches.

    - description: string
    - size: string  (optional)
    - max_price: number  (optional)
```

## Compare full results with direct search

```bash
.venv/bin/python - <<'PY'
from mcp_client import call_tool
from tools import search_listings
cases = [
    {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0},
    {'description': 'track jacket', 'size': 'M', 'max_price': 45.0},
    {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0},
]
for args in cases:
    direct = search_listings(**args)
    remote = call_tool('search_listings', args)
    assert isinstance(remote, list)
    assert remote == direct
    print(f"PASS: {args!r} -> {len(remote)} results; MCP matches direct search exactly")
PY
```

Actual output:

```text
PASS: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0} -> 10 results; MCP matches direct search exactly
PASS: {'description': 'track jacket', 'size': 'M', 'max_price': 45.0} -> 2 results; MCP matches direct search exactly
PASS: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0} -> 0 results; MCP matches direct search exactly
```

## Full agent after the MCP move

Search runs through MCP. The two model-calling tools reuse cached responses from the pre-change run. This is a build check; it is not the five-try evaluation.

```text
$ .venv/bin/python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Y2K Streetwear**
*   **New item:** Y2K Baby Tee — Butterfly Print
*   **Wardrobe pieces:** Baggy straight-leg jeans, dark wash (w_001), Chunky white sneakers (w_007), Black crossbody bag (w_010)
*   **Why it works:** The fitted, cropped silhouette of the butterfly tee balances the volume of the high-waisted baggy jeans for an authentic Y2K streetwear proportion. The white sneakers tie into the white on the tee, and the crossbody bag keeps it functional. (You could add a claw clip to complete the look.)

**Outfit 2: Vintage Denim Layer**
*   **New item:** Y2K Baby Tee — Butterfly Print
*   **Wardrobe pieces:** Wide-leg khaki trousers (w_002), Vintage black denim jacket (w_006), Black combat boots (w_008)
*   **Why it works:** Pairing the feminine, graphic baby tee with structured khaki trousers creates a cool contrast. Throwing on the slightly cropped vintage black denim jacket and edge of the combat boots grounds the pink and purple butterfly tones with a touch of grunge. (You could add silver hoop earrings to accent the vintage vibe.)

  Fit card: I scored this Y2K Baby Tee with a butterfly print for $18.00 on Depop. Styled with baggy straight-leg jeans, chunky white sneakers, and a black crossbody bag, the look nails authentic Y2K streetwear proportions.

0 model calls this session, 2 served from cache
```
