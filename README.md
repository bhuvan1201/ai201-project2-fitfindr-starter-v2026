# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr helps a user search a local set of secondhand clothing listings using a description, size, and maximum price. When it finds a match, it selects the highest-ranked listing and suggests outfits using clothes from the user's wardrobe. It then creates a short fit-card caption that includes the selected item, price, platform, and overall style. If no listing matches, it stops before the model tools and tells the user which parts of the search they could change.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the local listings by description keywords, with optional size and price filters. It does not call the model.
- **Inputs:** `description` (str), `size` (str or None, default None), and `max_price` (float or None, default None). None skips that filter; the price limit is inclusive.
- **Returns:** A list of matching listing dictionaries, highest keyword score first, up to `config.SEARCH_RESULT_LIMIT` results (currently 10). Each dictionary contains `id` (str), `title` (str), `description` (str), `category` (str), `style_tags` (list of strings), `size` (str), `condition` (str), `price` (float), `colors` (list of strings), `brand` (str or None), and `platform` (str).
- **When it has nothing:** Returns `[]` when no listing passes the filters and matches at least one description keyword. An empty or whitespace-only description also returns `[]`.

Search uses keyword overlap, an inclusive price limit, and the `_size_matches` helper.

### `suggest_outfit`

- **What it does:** Calls the model through `generate()` to suggest one or two outfits combining the selected listing with pieces from the user's wardrobe.
- **Inputs:** `new_item` (dict containing a listing returned by `search_listings`) and `wardrobe` (dict with an `items` key containing a list of wardrobe item dictionaries). Each wardrobe item has `id`, `name`, `category`, `colors`, `style_tags`, and `notes`.
- **Returns:** A non-empty string describing one or two outfit ideas, naming the selected item and the wardrobe pieces used, with an explanation of how to style them. It must not claim the user owns items absent from the supplied wardrobe.
- **When it has nothing:** When `wardrobe["items"]` is empty, returns a non-empty string of general styling advice for the selected item. Suggested pieces are described as options, not items the user already owns. A valid selected listing is required; the loop stops before calling this tool if search found nothing.

### `create_fit_card`

- **What it does:** Calls the model through `generate()` to turn an outfit suggestion and a selected listing into a short caption someone could post.
- **Inputs:** `outfit` (str returned by `suggest_outfit`) and `new_item` (dict containing the same selected listing).
- **Returns:** A string containing a two-to-four-sentence caption. It mentions the selected item, its price, and its platform once each, and describes the outfit's style using the supplied information. It does not invent missing details such as a brand when `brand` is None.
- **When it has nothing:** If `outfit` is empty or contains only whitespace, returns `"I couldn't create a fit card because no outfit suggestion was provided."` without calling the model. A valid selected listing is required.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->



**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` suggesting the user change the description, size, or budget, and stop without calling `suggest_outfit` or `create_fit_card`. Otherwise, store the first result in `session["selected_item"]` and call `suggest_outfit` using that saved item and `session["wardrobe"]`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** `agent.py::parse_query` uses regular expressions. It removes a dollar amount such as `$30` and stores it as `max_price=30.0`, reads a size such as `M`, `S/M`, `W30 L30`, or `US 8`, and keeps the remaining words as the description. A bare number after `size` (for example, `size 8`) is treated as a US shoe size. Prices written as words, such as “thirty dollars,” are not understood.

**What moves through the session:** `agent.py::new_session` stores the query and wardrobe. `run_agent` then saves the parsed search inputs in `parsed` and the matching listings in `search_results`. If there is a match, it puts the first result in `selected_item`, passes that saved item and `wardrobe` to `suggest_outfit`, saves its text in `outfit_suggestion`, then passes the saved suggestion and item to `create_fit_card` and saves the caption in `fit_card`. If search returns `[]`, it saves a useful message in `error` and leaves the later fields as `None`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```text
$ .venv/bin/python app.py ask '90s track jacket in size M'

  Found:    90s Track Jacket — Navy/White Stripe — $45.0 on poshmark

  Outfit:   **Outfit 1: Casual Streetwear**
*   **Pieces:** 90s Track Jacket, White ribbed tank top (w_003), Baggy straight-leg jeans (w_001), Chunky white sneakers (w_007).
*   **Why it works:** The fitted white tank balances the relaxed, baggy fit of the dark wash jeans, while the white stripes on the jacket tie into the sneakers for a cohesive, sporty 90s look. *(Suggested addition: vintage baseball cap).*

**Outfit 2: High-Low Contrast**
*   **Pieces:** 90s Track Jacket, White ribbed tank top (w_003), Wide-leg khaki trousers (w_002), Chunky white sneakers (w_007).
*   **Why it works:** Pairing the athletic track jacket with tailored khaki trousers creates a stylish high-low mix, and the white tank and sneakers keep the palette crisp and coordinated. *(Suggested addition: minimalist silver hoops).*

  Fit card: Scored this authentic Champion 90s track jacket on Poshmark for $45.00! I styled it into a casual streetwear fit with a ribbed tank, baggy jeans, and chunky sneakers. It gives off a sporty, vintage vibe that is so easy to layer.

2 model calls this session, 1147 prompt + 273 output tokens
```

**The three tools, tested one at a time**

```text
$ .venv/bin/python -c 'from tools import search_listings; print([(x["id"], x["title"], x["size"], x["price"]) for x in search_listings("graphic tee", max_price=30)])'
[('lst_002', 'Y2K Baby Tee — Butterfly Print', 'S/M', 18.0), ('lst_006', 'Graphic Tee — 2003 Tour Bootleg Style', 'L', 24.0), ('lst_017', 'Mesh Long-Sleeve Top — Black', 'S/M', 15.0), ('lst_033', 'Vintage Band Tee — Faded Grey', 'L', 19.0), ('lst_011', 'Low-Rise Cargo Pants — Khaki', 'W29', 27.0), ('lst_015', 'Vintage Graphic Hoodie — Faded Black', 'L', 26.0)]
```

```text
$ .venv/bin/python -c 'from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, get_empty_wardrobe, load_listings; item = load_listings()[0]; print("EXAMPLE WARDROBE:"); print(suggest_outfit(item, get_example_wardrobe())); print("EMPTY WARDROBE:"); print(suggest_outfit(item, get_empty_wardrobe()))'
EXAMPLE WARDROBE:
Here are two outfits featuring your new Vintage Levi's 501 Jeans:

**Outfit 1: Casual Streetwear**
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   *Why it works:* The fitted white tank balances the straight-leg cut of the Levi's, while the slightly cropped black jacket and chunky sneakers lean into the vintage streetwear vibe.

**Outfit 2: Cozy & Relaxed**
*   **Top:** Oversized grey crewneck sweatshirt
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt, Black crossbody bag
*   *Why it works:* Tucking the front of the oversized crewneck into the 501s creates an effortless, balanced silhouette. The combat boots add an edge that complements the faded denim wash. *(Consider adding a simple silver chain necklace to complete the look).*
EMPTY WARDROBE:
Here are two ways to style the Vintage Levi's 501 Jeans:

1. **Casual Streetwear:** Pair the jeans with a tucked-in graphic t-shirt, a leather belt, and classic white leather sneakers. Add a black leather jacket for an extra layer.
2. **Classic Smart-Casual:** Combine the medium wash denim with a crisp, oversized white button-down shirt and brown leather loafers. Accessorize with a minimalist gold watch.
```

```text
$ AI201_CACHE=0 .venv/bin/python -c 'from tools import create_fit_card; from utils.data_loader import load_listings; item = load_listings()[0]; outfit = "Pair these jeans with a white ribbed tank, black denim jacket, and chunky white sneakers."; [print(f"RUN {i}: {create_fit_card(outfit, item)}") for i in range(1, 4)]'
RUN 1: Scored these vintage Levi's 501 jeans for just $38.00 on depop. Styled them with a white ribbed tank, black denim jacket, and chunky white sneakers for the ultimate classic streetwear look.
RUN 2: Scored these classic Levi's 501 Jeans for just $38.0 on depop! I styled them with a white ribbed tank, black denim jacket, and chunky white sneakers for the ultimate vintage streetwear look.
RUN 3: Scored these classic Levi's 501 Jeans for just $38.0 on depop! Paired with a white ribbed tank, black denim jacket, and chunky white sneakers, the look gives off an effortless vintage streetwear vibe.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Codex to explain how a tool specification should describe inputs, outputs, and empty cases, and then used it to review my Tool Inventory for gaps.
- *What came back:* The review pointed out that saying a tool “returns a list” was not specific enough. It also explained why `search_listings` should return `[]` when nothing matches, since the planning loop uses that value to choose whether to continue or stop.
- *What I changed:* I documented the input types and exact return values for all three tools. I also made the empty cases explicit and learned how a tool's return value becomes part of the control flow of an agent.

**Moment 2**

- *What I asked for:* I asked Codex to help me check whether my planning loop was actually carrying state between tools and stopping correctly after an empty search.
- *What came back:* It suggested checking the item received by `suggest_outfit` against `session["selected_item"]`, and replacing the later tools with functions that raise an error during the empty-search test. Those checks also revealed that the query parser ignored `size 8` and that the loop was trying the unfinished MCP path from Unit 4.
- *What I changed:* I updated the size parser so `size 8` becomes `US 8`, kept the Unit 3 search call local, and ran both the successful and empty-search paths myself. This helped me understand how session state makes each intermediate value visible and how a branch can be tested beyond checking only the final response.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

Baseline command: `python run_eval.py --label before`. The run made 50 model calls with caching off (26,962 prompt tokens and 6,532 output tokens). There were 25 criterion trials containing 35 agent requests, because each trial for criterion 3 contains three requests.

The scenarios were set before this run. Criterion 1 repeats the tee query and criterion 2 repeats the impossible query. Criterion 3 repeats tee → empty → jacket in the same process. Criterion 4 uses five different listings. Criterion 5 uses two full wardrobes, two containing only `w_001`, and one empty wardrobe.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops with guidance | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Each request keeps its own selected item | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card reports listing details correctly | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Outfit advice does not invent ownership | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

These scores come from reviewing the recorded evidence against `criteria.md`, not from a phrase scorer. Complete sessions, actual tool inputs and returns, and traces are saved in [the generated report](results/run_2026-10-08_004633_before.md) and its [JSON evidence](results/run_2026-10-08_004633_before.json). The generated report leaves scoring cells pending by design; the completed review is the table above. [The assessment notes](results/unit4_before_assessment.md) explain what was checked for each try.

**Real output from one try**

**Criterion 1, try 1:** `agent.py::run_agent`, printed by `trace.py::step` and captured by `run_eval.py::run_once`. All three tools appear:

```text
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
      in:  {'new_item_id': 'lst_002', 'wardrobe_ids': ['w_001', 'w_002', 'w_003', 'w_004', 'w_005', 'w_006', 'w_007', 'w_008', 'w_009', 'w_010']}
      out: **Outfit 1: Y2K Streetwear** *   **Top:** Y2K Baby Tee — Butterfly Print *   **Bottoms:** Baggy straight-leg jeans, dark wash (w_001) *   **Shoes:** Chunky whit…
[6] create_fit_card
      in:  {'new_item_id': 'lst_002', 'outfit': '**Outfit 1: Y2K Streetwear**\n*   **Top:** Y2K Baby Tee — Butterfly Print\n*   **Bottoms:** Baggy straight-leg jeans, dark…
      out: I scored this Y2K Baby Tee — Butterfly Print on depop for just $18.0! I styled it with baggy dark-wash jeans, chunky white sneakers, and a black crossbody bag f…
```

**Criterion 2, try 1:** `agent.py::_nothing_found_message`, returned in the session by `agent.py::run_agent`. The recorded calls contain only the MCP search:

```text
Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.
```

**Criterion 3, try 1:** This is the empty request's actual session-field excerpt captured by `run_eval.py::run_once`:

```json
{
  "selected_item": null,
  "outfit_suggestion": null,
  "fit_card": null
}
```

The complete trial selected `lst_002`, then nothing, then `lst_004`. The full captured item dictionaries passed to both later tools matched each request's selected item and first search result. This comparison passed in all five sequences; the empty requests called neither later tool.

**Criterion 4, try 1:** `tools.py::create_fit_card`. The selected listing was the Y2K Baby Tee — Butterfly Print, priced at $18 on depop:

```text
Scored this Y2K Baby Tee — Butterfly Print for just $18.00 on depop! Paired with baggy straight-leg jeans, chunky white sneakers, and a black crossbody bag, this look gives off a classic Y2K streetwear vibe.
```

**Criterion 5, try 3:** `tools.py::suggest_outfit`. The supplied wardrobe contained only the dark-wash baggy jeans (`w_001`). Sneakers are explicitly presented as an addition:

```text
**Outfit Idea:**

*   **Top:** 90s Track Jacket — Navy/White Stripe
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Suggested Addition:** Crisp white sneakers

**Why it works:**
The dark wash baggy jeans match the streetwear and 90s vintage vibe of the track jacket. Pairing the navy-and-white jacket with the indigo denim creates a cohesive, relaxed, retro-athletic look. Adding white sneakers would tie in the white stripe detail on the sleeves.
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5) | All five runs recorded the MCP search, outfit call and fit-card call returning successfully, with a non-empty fit card. |
| 2 | Impossible query stops with guidance | 5 of 5 | MET (5/5) | Every run returned an empty search, called neither later tool, and suggested changing the words, size or budget. |
| 3 | Each request keeps its own selected item | 5 of 5 | MET (5/5) | In every tee → empty → jacket sequence, the full item dictionaries passed to both later tools matched that request's selected item and first result. The empty request kept all three result fields empty and called neither later tool. |
| 4 | Fit card reports listing details correctly | 4 of 5 | MET (5/5) | All five captions identified the selected clothing item and gave the correct price and platform. Other item details mentioned in the captions agreed with the listings. |
| 5 | Outfit advice does not invent ownership | 5 of 5 | MET (5/5) | Across the two full, two single-item and one empty wardrobe tests, the advice was non-empty. Owned pieces matched the supplied wardrobe; extra pieces were suggestions, not claims of ownership. |

**Diagnoses**

None of the five criteria was missed in this baseline, so there is no failed criterion to assign to a tool, branch, session or model output. The [assessment notes](results/unit4_before_assessment.md) contain the checks behind these verdicts. Different wording and price formats such as `$18.00` instead of `$18` are allowed by the original criteria, so those differences are not failures.

The test coverage was narrow in some places. Criterion 1 repeated the same matching query, and criterion 2 repeated the same impossible query. Criterion 3 checked state carefully, but used the same three requests each time. Criteria 4 and 5 covered different listings and wardrobe sizes, but five successful tries still cannot show how the model will handle every input. The weakest standard is criterion 1: it checks whether the loop finishes, without requiring the selected item to satisfy the user's full request.

There is a search-quality limitation visible in the saved evidence. For `90s track jacket size M`, criterion 3, try 1 returned:

```text
lst_004: 90s Track Jacket — Navy/White Stripe
lst_022: 90s Leather Bomber — Black
lst_013: 90s Silk Slip Dress — Floral, Midi Length
lst_032: Shacket — Olive Canvas
lst_034: Bucket Hat — Reversible, Brown Plaid
```

The place responsible is the search tool, `tools.py::search_listings`. After filtering size and price, it accepts any listing with at least one shared keyword from its title, description or style tags. It does not require the requested clothing type to match. That lets loosely related items into the results. The loop then selects the first result without another match check. In this recorded run the correct jacket was first, so this limitation did not cause a criterion to fail or a wrong selected item.

For a future stronger test, I would tighten criterion 1 to: **For five queries with the expected clothing type, size and maximum price written down before testing, the selected listing must satisfy all three requirements and the agent must return a fit card in 5 of 5 tries.** This would check whether the completed run actually meets the request. I would require five because returning an item that breaks an explicit requirement is not a successful recommendation. This is a proposed future standard, not a revision used to rescore this baseline. The original criteria and targets stay as they were.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

Command: `AI201_CACHE=0 python app.py ask '90s track jacket in size M' --trace`

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
```

**Empty search**

Command: `python app.py ask 'designer ballgown size XXS under $5' --trace`

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

The happy path has six steps, while the empty search stops after three. The selected listing ID, `lst_004`, also appears in the inputs to both later tools. The trace abbreviates long values and shows wardrobe item IDs; the full printed outfit and caption are in [the saved check output](results/unit4_milestone2_checks.md).

**Failure checks — Milestone 2**

| Case | What happened |
|---|---|
| Empty search | Stopped before either model tool, made zero model calls, and suggested broader words, a different size, or a higher budget. |
| Empty wardrobe | Returned general styling suggestions with two model calls. The outfit advice suggested combinations without saying those items were already owned. |
| Model unavailable | A temporary invalid API key caused the outfit call to fail. The agent kept the search results, stopped before the fit card, and displayed a message asking me to check the key and try again. |

The model checks ran with caching disabled. The invalid key only applied to that command; the saved `.env` was unchanged. These checks exercise the existing handlers, while the code change adds the trace. The repeated criteria evaluation comes next.

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

I registered `search_listings` in `mcp_server.py` with the same inputs as my Tool Inventory. In `agent.py::run_agent`, search now goes through `mcp_client.call_tool`, and its returned list is stored in `session["search_results"]`. The server calls the existing search function, so the filtering and ranking stay the same. The agent does not silently fall back to direct search.

For Milestone 1, I compared the complete MCP and direct-search results for a matching query, a size-and-price-filtered query, and an impossible query. All three matched exactly, including list order. The full agent also returned an outfit and fit card through the MCP search path. That repeat run reused two cached model responses, so it checks the connection and data flow, not repeated model reliability. Commands and actual output are saved in [the MCP check](results/unit4_milestone1_mcp.md). The later evaluation will disable caching.

---

## The Improvement

**What changed:** `tools.py::search_listings` now checks clothing type before ranking results. When the query names a jacket, tee or sneaker, the listing title must identify an item in that family. Jacket aliases include bombers, windbreakers, blazers and shackets. The existing size filter, price filter and keyword ranking remain in place. Queries without a recognized type keep their previous behavior.

**Which problem it was meant to fix:** The baseline jacket search returned a dress and a hat because they shared other keywords. The original five criteria all passed, but they did not measure this problem. A separate test was defined before the change, with five typed queries and a broad `vintage` query as a control. Each typed query had a fixed set of allowed item IDs and required valid results, so an empty result could not count as success.

The focused test ran through MCP before and after:

```sh
python tools/check_search_types.py --label before
python tools/check_search_types.py --label after
```

| Focused check | Before | After |
|---|---|---|
| Queries returning only the right clothing family and all required items | 0/5 | 5/5 |
| Wrong-type result occurrences across the five queries | 21 | 0 |
| Previously returned valid items preserved | Reference results | All preserved |
| Broad `vintage` query | Reference results | Same complete results and order |

Actual returned IDs for `90s track jacket size M`, recorded by `tools/check_search_types.py::main` through MCP:

```text
before: ['lst_004', 'lst_022', 'lst_013', 'lst_032', 'lst_034']
after:  ['lst_004', 'lst_022', 'lst_032']
```

The dress (`lst_013`) and hat (`lst_034`) are gone. The [focused comparison](results/search_type_comparison.md) links the complete before and after search output.

### Run Log — After

Command: `python run_eval.py --label after`. The run used the same scenarios, wardrobes, targets and temperature as the baseline, with caching off. It completed 35 agent requests and 50 model calls (27,271 prompt tokens and 6,815 output tokens). The selected item for every request was also unchanged.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops with guidance | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Each request keeps its own selected item | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card reports listing details correctly | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Outfit advice does not invent ownership | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

The [full after report](results/run_2026-10-10_151811_after.md) and [JSON evidence](results/run_2026-10-10_151811_after.json) contain actual sessions, tool inputs, outputs and traces from `run_eval.py::run_once`. The generated report leaves scoring cells blank for review; the table here contains the reviewed verdicts. The [after assessment](results/unit4_after_assessment.md) records the checks for each criterion.

**Did it help, and how do I know:** The focused search checks improved from 0/5 to 5/5, with wrong-type results dropping from 21 to zero and no previously returned valid items lost. The original criteria stayed at 5/5 each, so those results show no regression on the tested cases. They do not show an increase in the original pass rate, which was already perfect.

This is still a limited filter. It recognizes three clothing families from words in titles, not every possible clothing name. A denim-jacket query can still return other kinds of jackets, and a sentence mentioning sneakers as a companion item could be misread as requesting sneakers. Type aliases only affect filtering; keyword scoring is still literal. These limits remain for later work rather than adding another change to this experiment.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
