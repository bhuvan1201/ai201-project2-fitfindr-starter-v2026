# Unit 4 Milestone 2 — traces and failure checks

Run on 2026-10-07. These are smoke checks, not the five-trial criteria evaluation.

The existing failure handlers worked in these runs. This milestone adds tracing in `agent.py::run_agent` using `trace.py::step`; `app.py::_ask_one` prints the final results. Model errors come through `generate.py`.

Caching was disabled for the happy path, empty wardrobe, and invalid-key checks. The invalid key was a temporary command environment variable; the saved `.env` was not changed. There were five model request attempts in total, including the rejected-key attempt.

## Happy path

Command:

```sh
AI201_CACHE=0 .venv/bin/python app.py ask '90s track jacket in size M' --trace
```

Actual output:

```text
[1] parse_query
      in:  90s track jacket in size M
      out: {'description': '90s track jacket in', 'size': 'M', 'max_price': None}
[2] search_listings (via MCP)
      in:  {'description': '90s track jacket in', 'size': 'M', 'max_price': None}
      out: 5 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +2 more
[3] branch
      →    Search found matches: select the first result and continue.
[4] select_item
      out: lst_004: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
[5] suggest_outfit
      in:  {'new_item_id': 'lst_004', 'wardrobe_ids': ['w_001', 'w_002', 'w_003', 'w_004', 'w_005', 'w_006', 'w_007', 'w_008', 'w_009', 'w_010']}
      out: Here are two outfit suggestions using your new track jacket:  **Outfit 1: Casual Streetwear** *   **Top:** White ribbed tank top *   **Bottoms:** Baggy straight…
[6] create_fit_card
      in:  {'new_item_id': 'lst_004', 'outfit': 'Here are two outfit suggestions using your new track jacket:\n\n**Outfit 1: Casual Streetwear**\n*   **Top:** White ribbed…
      out: I scored this navy and white 90s Track Jacket for $45.0 on Poshmark! Paired with baggy jeans and chunky sneakers, it creates a cool and casual 90s athletic stre…

  Found:    90s Track Jacket — Navy/White Stripe — $45.0 on poshmark

  Outfit:   Here are two outfit suggestions using your new track jacket:

**Outfit 1: Casual Streetwear**
*   **Top:** White ribbed tank top
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Shoes:** Chunky white sneakers
*   **Why it works:** The fitted white tank balances the relaxed, baggy denim, and the white sneakers tie in the white stripe details on the track jacket for a cohesive 90s athletic look.

**Outfit 2: High-Low Contrast**
*   **Bottoms:** Wide-leg khaki trousers
*   **Shoes:** Black combat boots
*   **Suggested Addition:** A simple white t-shirt to layer underneath.
*   **Why it works:** Pairing the sporty, navy 90s track jacket with tailored khaki trousers creates a cool contrast between athletic and smart-casual styles, while the combat boots add an edgy streetwear finish.

  Fit card: I scored this navy and white 90s Track Jacket for $45.0 on Poshmark! Paired with baggy jeans and chunky sneakers, it creates a cool and casual 90s athletic streetwear vibe.

2 model calls this session, 1127 prompt + 241 output tokens
```

## Empty search

Command:

```sh
.venv/bin/python app.py ask 'designer ballgown size XXS under $5' --trace
```

Actual output:

```text
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
[3] branch
      →    Search returned []: stop before suggest_outfit and create_fit_card.

  Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.

0 model calls this session
```

## Empty wardrobe

Command:

```sh
AI201_CACHE=0 .venv/bin/python app.py ask 'vintage graphic tee under $30' --empty-wardrobe --trace
```

Actual output:

```text
(running with an empty wardrobe)
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] branch
      →    Search found matches: select the first result and continue.
[4] select_item
      out: lst_002: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[5] suggest_outfit
      in:  {'new_item_id': 'lst_002', 'wardrobe_ids': []}
      out: To style the Y2K Butterfly Baby Tee, consider these options:  1. **Y2K Streetwear:** Pair the tee with a pair of low-rise baggy cargo pants in khaki or light wa…
      →    Empty wardrobe: general styling advice.
[6] create_fit_card
      in:  {'new_item_id': 'lst_002', 'outfit': 'To style the Y2K Butterfly Baby Tee, consider these options:\n\n1. **Y2K Streetwear:** Pair the tee with a pair of low-ris…
      out: Scored this Y2K Baby Tee with a butterfly print for $18 on Depop! I styled it with a pleated denim mini skirt, knee-high white socks, and retro platform sandals…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   To style the Y2K Butterfly Baby Tee, consider these options:

1. **Y2K Streetwear:** Pair the tee with a pair of low-rise baggy cargo pants in khaki or light wash denim, and add chunky platform sneakers and a small shoulder bag.
2. **Casual Retro:** Layer the tee with a pleated denim mini skirt, knee-high white socks, and retro platform sandals.

  Fit card: Scored this Y2K Baby Tee with a butterfly print for $18 on Depop! I styled it with a pleated denim mini skirt, knee-high white socks, and retro platform sandals for the ultimate casual retro vibe.

2 model calls this session, 431 prompt + 130 output tokens
```

## Model unavailable

Command:

```sh
GEMINI_API_KEY=unit4-invalid-test-key AI201_CACHE=0 .venv/bin/python app.py ask 'navy athletic jacket size M under $46' --trace
```

Actual output:

```text
[1] parse_query
      in:  navy athletic jacket size M under $46
      out: {'description': 'navy athletic jacket', 'size': 'M', 'max_price': 46.0}
[2] search_listings (via MCP)
      in:  {'description': 'navy athletic jacket', 'size': 'M', 'max_price': 46.0}
      out: 2 items: 90s Track Jacket — Navy/White Stripe, Shacket — Olive Canvas
[3] branch
      →    Search found matches: select the first result and continue.
[4] select_item
      out: lst_004: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
[5] suggest_outfit
      in:  {'new_item_id': 'lst_004', 'wardrobe_ids': ['w_001', 'w_002', 'w_003', 'w_004', 'w_005', 'w_006', 'w_007', 'w_008', 'w_009', 'w_010']}
      →    The model couldn't be reached while creating the outfit suggestion. Search found 2 listing(s). Check GEMINI_API_KEY in your .env and try again. The service said: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.

  The model couldn't be reached while creating the outfit suggestion. Search found 2 listing(s). Check GEMINI_API_KEY in your .env and try again. The service said: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.

1 model calls this session
```

