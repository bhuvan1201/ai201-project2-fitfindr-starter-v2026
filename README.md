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

**Unit 3 — Moment 1**

- *What I asked for:* I asked Codex to explain how a tool specification should describe inputs, outputs, and empty cases, and then used it to review my Tool Inventory for gaps.
- *What came back:* The review pointed out that saying a tool “returns a list” was not specific enough. It also explained why `search_listings` should return `[]` when nothing matches, since the planning loop uses that value to choose whether to continue or stop.
- *What I changed:* I documented the input types and exact return values for all three tools. I also made the empty cases explicit and learned how a tool's return value becomes part of the control flow of an agent.

**Unit 3 — Moment 2**

- *What I asked for:* I asked Codex to help me check whether my planning loop was actually carrying state between tools and stopping correctly after an empty search.
- *What came back:* It suggested checking the item received by `suggest_outfit` against `session["selected_item"]`, and replacing the later tools with functions that raise an error during the empty-search test. Those checks also revealed that the query parser ignored `size 8` and that the loop was trying the unfinished MCP path from Unit 4.
- *What I changed:* I updated the size parser so `size 8` becomes `US 8`, kept the Unit 3 search call local, and ran both the successful and empty-search paths myself. This helped me understand how session state makes each intermediate value visible and how a branch can be tested beyond checking only the final response.

**Unit 4 — Turning criteria into tests**

- *What I asked:* I asked for help working through the testing milestones and explaining what each check showed.
- *What came back:* Codex implemented the MCP and trace changes. For the state criterion, each trial contained a tee search, an empty search and a jacket search in the same process. The later tool inputs were recorded so they could be compared with the session.
- *What this clarified:* Five successful requests are not automatically five passes. Each result has to be checked against the specific criterion. State checks need recorded inputs; caption and ownership checks need the generated text compared with the supplied data.

**Unit 4 — Measuring an improvement after all criteria passed**

- *What I asked:* I asked what could be improved next, then agreed to clothing-type filtering.
- *What came back:* Codex identified a gap in the original tests: a jacket search could return a dress and a hat without failing any criterion. It defined focused checks before changing the tool, then I implemented the filter, and ran the before-and-after comparison and original evaluation.
- *What changed and what this clarified:* The focused checks improved from 0/5 to 5/5, while the original criteria remained at 5/5 each. The conclusion is that the filter improved the measured search results, not that the whole system became perfect. The saved evidence and remaining limitations make that distinction explicit.

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

In Milestone 1, `search_listings` was registered in `mcp_server.py` with the same inputs as the Tool Inventory. In `agent.py::run_agent`, search now goes through `mcp_client.call_tool`, and its returned list is stored in `session["search_results"]`. The server calls the existing search function, so the MCP move itself did not change filtering or ranking. The separate Milestone 5 filter change is described below. The agent does not silently fall back to direct search.

The Milestone 1 comparison checked the complete MCP and direct-search results for a matching query, a size-and-price-filtered query, and an impossible query. All three matched exactly, including list order. The full agent also returned an outfit and fit card through the MCP search path. That repeat run reused two cached model responses, so it checks the connection and data flow, not repeated model reliability. Commands and actual output are saved in [the MCP check](results/unit4_milestone1_mcp.md). Both later evaluations ran with caching disabled.

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

None of the original five criteria is still missed: each scored 5/5 in the after-run. That only covers the recorded scenarios. It does not mean the agent handles every request correctly.

The clearest remaining gap is matching all parts of a request. The after-results for `denim jacket under $50` still include the track jacket and olive shacket. They pass the new jacket-family filter, but they are not denim jackets. A next step would be to separate required attributes, such as material, from optional style words and test those requirements with fixed expected results.

The type filter also has a small vocabulary. It only recognizes jacket, tee and sneaker families, and relies on words in listing titles. Other clothing types keep the old keyword behavior. More complex wording, such as asking for a jacket to wear with sneakers, could also confuse which type is being requested. Those cases have not been evaluated here; they would need their own tests before extending the filter.

The model checks are limited too. Five correct captions and five ownership checks are useful evidence, but they cannot establish that future model responses will always be accurate. Additional wardrobe combinations and repeated runs would give broader coverage.

The work stopped after one measured change so the before-and-after comparison stayed clear. Fixing attribute matching, expanding the type vocabulary and changing model prompts at the same time would make it harder to tell which change helped. The original criteria, baseline evidence and remaining limitations are kept as part of the result.


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

## Capstone

### The Shape

**System:** FitFindr — the existing system from Units 3 and 4, in this same repository.

**Shape:** A — deploy and instrument.

**Run path:** Path A — a hosted service with a public URL. Vercel — https://fitfindr-capstone.vercel.app. This is an HTTP API: use `GET /health` or `POST /ask`; there is no frontend.

I am extending FitFindr by adding an operational layer around the existing agent. The repo already has `serve.py`, which exposes the same `agent.py::run_agent` through `POST /ask` and provides `GET /health`. I will host that service and add structured JSON Lines records of requests, their outputs or failures, elapsed time, and model calls and tokens where available. I will document a reproducible run path in `RUNNING.md`, check it from a clean checkout, and measure the average cost of ten real runs using recorded time and API-reported usage.

**Out of scope:**

- Changing the search matching, clothing-type filter or ranking.
- Adding another tool, changing the outfit and fit-card prompts, or expanding the listings and wardrobe data.
- Building a frontend, accounts or a database.

**Scope check:** This is one operational extension around the existing HTTP wrapper. The build will focus on request instrumentation and deployment setup; it will reuse the agent, MCP search tool and model adapter. If deployment setup consumes the available build block, I will record the blocker and cut scope rather than rebuild the system. The brief permits switching to Path B if hosting remains blocked, but the selected path at this stage is Path A.

**Claim when finished:** A user can send a query to the hosted FitFindr service, receive its existing result, and inspect a saved run record showing what happened, how long it took and what model usage was reported.

### Build — operational instrumentation

The extension lives in `serve.py` and `run_log.py`. The existing agent, tools, search ranking and model adapter are unchanged. `POST /ask` still returns the agent's session dictionary, including its existing early-stop messages. `GET /health` keeps its original response.

Each completed HTTP request appends one JSON object to `logs/capstone_runs.jsonl`. `FITFINDR_RUN_LOG` can select another path. The record includes:

| Fields | What they record |
|---|---|
| `timestamp`, `request_id`, `method`, `path` | UTC start time, unique correlation ID and requested route |
| `input_format`, `input`, `output_format`, `output` | Parsed JSON or raw input, and the returned JSON or raw response text |
| `status_code`, `outcome`, `error` | HTTP status, success/rejected/stopped/error classification and any observed error |
| `duration_ms` | Server-side elapsed time from the request hook to response logging, including queueing; excludes log-writing time and network round-trip time |
| `queue_ms`, `agent_ms` | Time waiting for the existing lock, then elapsed agent-run time including MCP, API waits and retries |
| `configured_model`, `cache_enabled` | The model and cache configuration for interpreting the run |
| `model_usage` | Per-request model attempts and reported prompt/output/total tokens |

`serve.py::model_usage_snapshot` reads `generate.call_count()` and `generate.token_counts()` before and after the agent run, inside the existing lock. This prevents another request's model usage from being attributed to the wrong run. Attempts include retries, not just successful answers. Token fields are reported counters: missing provider metadata is not proof of zero tokens or zero API spend. Health checks and rejected requests do not inherit the process's cumulative counts.

Non-standard JSON values such as `NaN` or `Infinity` are retained as raw text in the record rather than allowed to invalidate a JSONL line. This changes capture only, not the endpoint's validation or response.

The response's `X-Request-ID` matches its saved record. `X-Run-Log: saved` confirms the file append; `failed` and an error on stderr expose a storage failure while retaining the original response. `FITFINDR_LOG_STDOUT=1` also mirrors saved JSON records to the hosting log stream for copying into the committed evidence; it does not replace the JSONL file. A mirror failure is reported on stderr and does not falsely imply that the successful file append failed. Request headers and environment credentials are not added to the records. Request bodies and outputs are recorded, so demonstration inputs should be chosen deliberately.

The logger supports the existing single-worker service. File persistence across a host restart is not assumed; measured extracts must be committed in the session that produces them. The selected host is Vercel. `RUNNING.md` documents its entrypoint, Python environment, temporary log storage and disabled response cache. Public health, MCP empty-search and rejected-input checks pass. Clean-checkout verification and the measured cost are tracked below.

**Development verification:** AI-assisted implementation checks used temporary logs and a temporary Python 3.13 environment with the same installed package versions because the original environment's files were offloaded to iCloud. Checks exercised the real MCP search and original empty-result branch, the matching agent pipeline with controlled generation, rejected and exceptional requests, storage failure, and per-request usage isolation under concurrent requests. No model API calls were made, synthetic counters were not treated as cost measurements, and these temporary records were not committed as capstone run evidence. These development checks preceded the committed capstone criteria. Later operational measurements are recorded below; formal three-trial evaluation remains separate.


### Hosted run path — deployment checks

I chose Vercel. The service is at **https://fitfindr-capstone.vercel.app**, with the health route at **https://fitfindr-capstone.vercel.app/health**. It was deployed through the Vercel CLI; GitHub push does not automatically deploy this project. `RUNNING.md` has the installation and deployment commands. The Gemini key is a private production secret; it is excluded from source uploads and Git.

Two setup problems showed up on the host. First, Vercel installed from `pyproject.toml` instead of `requirements.txt`, so the initial function could not import `dotenv`. The deployment manifest now includes the same 48 exact package pins as the local constraints file. Second, the MCP child interpreter could not import `mcp`, even though the Flask process could. `mcp_client.py::_server_parameters` now explicitly passes the parent's Python import paths to the child. This is a runtime setup change; the search rules and tool outputs are unchanged.

After those fixes, these unauthenticated requests to the production URL were checked:

| Check | Result | Log confirmation |
|---|---|---|
| `GET /health` | 200, `{"status":"ok"}` | `X-Run-Log: saved` |
| `POST /ask`, `designer ballgown size XXS under $5` | 200, empty results, actionable guidance, `fit_card: null` | `X-Run-Log: saved` |
| `POST /ask`, `{}` | 400, asks for a query | `X-Run-Log: saved` |

The actual client responses, request IDs and matching application records are in [deployment smoke evidence](results/capstone_deployment_smoke.json); the [raw Vercel runtime export](results/capstone_deployment_smoke_runtime.jsonl) also retains the observed setup errors. These are deployment checks, not the formal three-trial results. The saved application records report zero model attempts, and no Gemini-generated outfit was requested. The later Milestone 3 measurement below completed ten model-backed requests and records their measured time and reported usage.

**Clean-checkout verification:** passed at `994e563`. I cloned the committed local repository into a separate temporary folder, installed `requirements.txt` in a new Python 3.13 environment, and started `serve.py` outside the editor. HTTP health and a real MCP empty search passed, both records were saved, and the checkout stayed clean. These checks used a temporary port and log path with no Gemini key. [Verification record](results/capstone_clean_checkout_check.json). The revision has not yet been pushed, so a fresh GitHub clone will not contain this setup until it is pushed.

**Milestone 3 measurement evidence:** See Instrumentation and What It Costs below. Formal three-trial criteria evaluation remains separate.

### Acceptance Criteria

The five capstone criteria and their reasons are recorded in [criteria.md — Capstone](criteria.md#capstone--shape-a-deploy-and-instrument). The earlier Unit 3/4 criteria remain in their original section. The [testability review](notes/capstone_criteria_review.md) records the fixed query, warm-up, timing and sampling rules. Criteria 3 and 4 retain their original sentences with explicit clarifications underneath; their numerical targets are unchanged.

<!-- capstone-milestone3-measurements -->

### Instrumentation

Milestone 3 operational sample: 10 matching attempts and one deliberately rejected input. This is not the formal three-trial criteria evaluation.

Requests were sent and timed by `tools/measure_capstone.py::request_once`; server records were produced by `serve.py::finish_request_record` and saved by `run_log.py::append_record`. Runtime records were recovered by request ID. These are complete recovered application records in client-request order:

```jsonl
{"timestamp": "2026-11-14T23:43:31.173+00:00", "request_id": "1c075cf5c5b44e99a0e71f9687590baa", "method": "POST", "path": "/ask", "input_format": "json", "input": {"query": "90s track jacket in size M"}, "output_format": "json", "output": {"error": null, "fit_card": "I am obsessed with this 90s Track Jacket — Navy/White Stripe I found on Poshmark for $45.0$. Layering it over a white ribbed tank with baggy jeans gives off the ultimate athletic streetwear vibe. It is the easiest lightweight piece for styling effortless retro looks!", "outfit_suggestion": "**Outfit 1: 90s Streetwear**\n*   **New Item:** 90s Track Jacket — Navy/White Stripe\n*   **Wardrobe Pieces:** White ribbed tank top (w_003), Baggy straight-leg jeans, dark wash (w_001), Chunky white sneakers (w_007)\n*   **Why it works:** Layering the track jacket partially unzipped over the fitted white tank plays with proportions against the baggy jeans. The white sneakers tie into the jacket's white stripes for a cohesive, athletic streetwear look. \n*   *Optional addition:* A retro silver chain necklace.\n\n**Outfit 2: High-Low Contrast**\n*   **New Item:** 90s Track Jacket — Navy/White Stripe\n*   **Wardrobe Pieces:** Wide-leg khaki trousers (w_002), Chunky white sneakers (w_007), Black crossbody bag (w_010)\n*   **Why it works:** Pairing the sporty, vintage track jacket with tailored khaki trousers creates an effortless high-low mix. The white sneakers keep the casual energy flowing, and the black crossbody bag grounds the lighter earth tones.", "parsed": {"description": "90s track jacket in", "max_price": null, "size": "M"}, "query": "90s track jacket in size M", "search_results": [{"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, {"brand": null, "category": "outerwear", "colors": ["black"], "condition": "good", "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.", "id": "lst_022", "platform": "depop", "price": 75.0, "size": "M", "style_tags": ["90s", "vintage", "leather", "classic", "grunge"], "title": "90s Leather Bomber — Black"}, {"brand": null, "category": "outerwear", "colors": ["olive", "green"], "condition": "excellent", "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.", "id": "lst_032", "platform": "poshmark", "price": 33.0, "size": "M/L", "style_tags": ["earth tones", "classic", "layering", "minimal"], "title": "Shacket — Olive Canvas"}], "selected_item": {"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, "wardrobe": {"items": [{"category": "bottoms", "colors": ["dark blue", "indigo"], "id": "w_001", "name": "Baggy straight-leg jeans, dark wash", "notes": "High-waisted, sits above the hip", "style_tags": ["denim", "streetwear", "baggy"]}, {"category": "bottoms", "colors": ["khaki", "tan"], "id": "w_002", "name": "Wide-leg khaki trousers", "notes": null, "style_tags": ["earth tones", "minimal", "wide-leg"]}, {"category": "tops", "colors": ["white"], "id": "w_003", "name": "White ribbed tank top", "notes": "Goes with everything", "style_tags": ["basics", "minimal", "fitted"]}, {"category": "tops", "colors": ["grey", "charcoal"], "id": "w_004", "name": "Oversized grey crewneck sweatshirt", "notes": "Really oversized — drops below the hip", "style_tags": ["oversized", "basics", "cozy"]}, {"category": "tops", "colors": ["black"], "id": "w_005", "name": "Black cropped zip hoodie", "notes": null, "style_tags": ["athletic", "streetwear", "cropped"]}, {"category": "outerwear", "colors": ["black"], "id": "w_006", "name": "Vintage black denim jacket", "notes": "Slightly cropped", "style_tags": ["denim", "vintage", "classic"]}, {"category": "shoes", "colors": ["white"], "id": "w_007", "name": "Chunky white sneakers", "notes": null, "style_tags": ["sneakers", "chunky", "streetwear"]}, {"category": "shoes", "colors": ["black"], "id": "w_008", "name": "Black combat boots", "notes": "Lace-up, mid-ankle height", "style_tags": ["boots", "grunge", "classic"]}, {"category": "accessories", "colors": ["brown"], "id": "w_009", "name": "Brown leather belt", "notes": null, "style_tags": ["classic", "earth tones", "accessories"]}, {"category": "accessories", "colors": ["black"], "id": "w_010", "name": "Black crossbody bag", "notes": null, "style_tags": ["minimal", "accessories", "everyday"]}]}}, "status_code": 200, "outcome": "success", "error": null, "duration_ms": 4718.064, "queue_ms": 0.002, "agent_ms": 4716.154, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 2, "reported_prompt_tokens": 1187, "reported_output_tokens": 315, "reported_total_tokens": 1502}}
{"timestamp": "2026-11-14T23:43:46.124+00:00", "request_id": "e009e86447404d128aa0c95dac0a5f59", "method": "POST", "path": "/ask", "input_format": "json", "input": {"query": "90s track jacket in size M"}, "output_format": "json", "output": {"error": null, "fit_card": "Score! I just thrifted this authentic 90s track jacket for $45.00 on Poshmark. I paired it with a white ribbed tank top, baggy dark-wash jeans, and chunky white sneakers. The final look has a retro 90s streetwear vibe that is lightweight and great for layering.", "outfit_suggestion": "Here are two outfit suggestions using your new track jacket:\n\n**Outfit 1: Casual Streetwear**\n*   **New Item:** 90s Track Jacket — Navy/White Stripe\n*   **Wardrobe Pieces:** Baggy straight-leg jeans (dark wash), White ribbed tank top, Chunky white sneakers\n*   **Why it works:** The baggy dark-wash jeans and white tank lean into a 90s streetwear aesthetic that matches the retro vibe of the track jacket. The chunky white sneakers tie in with the white stripe details on the sleeves. \n*   *Suggested addition:* A silver chain necklace.\n\n**Outfit 2: High-Low Mix**\n*   **New Item:** 90s Track Jacket — Navy/White Stripe\n*   **Wardrobe Pieces:** Wide-leg khaki trousers, White ribbed tank top, Chunky white sneakers\n*   **Why it works:** Pairing the athletic track jacket with tailored khaki trousers creates a balanced high-low look. The white tank keeps the layers lightweight, and the white sneakers coordinate with the jacket's stripes to pull the outfit together.\n*   *Suggested addition:* A minimal canvas tote bag.", "parsed": {"description": "90s track jacket in", "max_price": null, "size": "M"}, "query": "90s track jacket in size M", "search_results": [{"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, {"brand": null, "category": "outerwear", "colors": ["black"], "condition": "good", "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.", "id": "lst_022", "platform": "depop", "price": 75.0, "size": "M", "style_tags": ["90s", "vintage", "leather", "classic", "grunge"], "title": "90s Leather Bomber — Black"}, {"brand": null, "category": "outerwear", "colors": ["olive", "green"], "condition": "excellent", "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.", "id": "lst_032", "platform": "poshmark", "price": 33.0, "size": "M/L", "style_tags": ["earth tones", "classic", "layering", "minimal"], "title": "Shacket — Olive Canvas"}], "selected_item": {"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, "wardrobe": {"items": [{"category": "bottoms", "colors": ["dark blue", "indigo"], "id": "w_001", "name": "Baggy straight-leg jeans, dark wash", "notes": "High-waisted, sits above the hip", "style_tags": ["denim", "streetwear", "baggy"]}, {"category": "bottoms", "colors": ["khaki", "tan"], "id": "w_002", "name": "Wide-leg khaki trousers", "notes": null, "style_tags": ["earth tones", "minimal", "wide-leg"]}, {"category": "tops", "colors": ["white"], "id": "w_003", "name": "White ribbed tank top", "notes": "Goes with everything", "style_tags": ["basics", "minimal", "fitted"]}, {"category": "tops", "colors": ["grey", "charcoal"], "id": "w_004", "name": "Oversized grey crewneck sweatshirt", "notes": "Really oversized — drops below the hip", "style_tags": ["oversized", "basics", "cozy"]}, {"category": "tops", "colors": ["black"], "id": "w_005", "name": "Black cropped zip hoodie", "notes": null, "style_tags": ["athletic", "streetwear", "cropped"]}, {"category": "outerwear", "colors": ["black"], "id": "w_006", "name": "Vintage black denim jacket", "notes": "Slightly cropped", "style_tags": ["denim", "vintage", "classic"]}, {"category": "shoes", "colors": ["white"], "id": "w_007", "name": "Chunky white sneakers", "notes": null, "style_tags": ["sneakers", "chunky", "streetwear"]}, {"category": "shoes", "colors": ["black"], "id": "w_008", "name": "Black combat boots", "notes": "Lace-up, mid-ankle height", "style_tags": ["boots", "grunge", "classic"]}, {"category": "accessories", "colors": ["brown"], "id": "w_009", "name": "Brown leather belt", "notes": null, "style_tags": ["classic", "earth tones", "accessories"]}, {"category": "accessories", "colors": ["black"], "id": "w_010", "name": "Black crossbody bag", "notes": null, "style_tags": ["minimal", "accessories", "everyday"]}]}}, "status_code": 200, "outcome": "success", "error": null, "duration_ms": 2512.768, "queue_ms": 0.001, "agent_ms": 2512.21, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 2, "reported_prompt_tokens": 1177, "reported_output_tokens": 312, "reported_total_tokens": 1489}}
{"timestamp": "2026-11-14T23:43:58.837+00:00", "request_id": "7facc54f28d248f295280658eb15e77a", "method": "POST", "path": "/ask", "input_format": "json", "input": {"query": "90s track jacket in size M"}, "output_format": "json", "output": {"error": null, "fit_card": "Scored this authentic 90s track jacket for $45.0 on Poshmark! It's lightweight and perfect for layering into a casual streetwear fit.", "outfit_suggestion": "Here are two outfit suggestions using your new track jacket and existing wardrobe pieces:\n\n**Outfit 1: Casual Streetwear**\n* **Pieces to wear:** 90s Track Jacket, White ribbed tank top, Baggy straight-leg jeans, Chunky white sneakers.\n* **Why it works:** The fitted white tank balances the relaxed fit of the baggy dark-wash jeans. Layering the navy and white track jacket on top matches the 90s streetwear vibe, while the chunky white sneakers tie the whole sporty look together. \n\n**Outfit 2: High-Low Mix**\n* **Pieces to wear:** 90s Track Jacket, Wide-leg khaki trousers, Chunky white sneakers.\n* **Why it works:** Pairing the athletic track jacket with tailored wide-leg khaki trousers creates a cool contrast between sporty and minimal styles. \n* *Suggested addition:* You could add a simple white t-shirt underneath to complete the base layer.", "parsed": {"description": "90s track jacket in", "max_price": null, "size": "M"}, "query": "90s track jacket in size M", "search_results": [{"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, {"brand": null, "category": "outerwear", "colors": ["black"], "condition": "good", "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.", "id": "lst_022", "platform": "depop", "price": 75.0, "size": "M", "style_tags": ["90s", "vintage", "leather", "classic", "grunge"], "title": "90s Leather Bomber — Black"}, {"brand": null, "category": "outerwear", "colors": ["olive", "green"], "condition": "excellent", "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.", "id": "lst_032", "platform": "poshmark", "price": 33.0, "size": "M/L", "style_tags": ["earth tones", "classic", "layering", "minimal"], "title": "Shacket — Olive Canvas"}], "selected_item": {"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, "wardrobe": {"items": [{"category": "bottoms", "colors": ["dark blue", "indigo"], "id": "w_001", "name": "Baggy straight-leg jeans, dark wash", "notes": "High-waisted, sits above the hip", "style_tags": ["denim", "streetwear", "baggy"]}, {"category": "bottoms", "colors": ["khaki", "tan"], "id": "w_002", "name": "Wide-leg khaki trousers", "notes": null, "style_tags": ["earth tones", "minimal", "wide-leg"]}, {"category": "tops", "colors": ["white"], "id": "w_003", "name": "White ribbed tank top", "notes": "Goes with everything", "style_tags": ["basics", "minimal", "fitted"]}, {"category": "tops", "colors": ["grey", "charcoal"], "id": "w_004", "name": "Oversized grey crewneck sweatshirt", "notes": "Really oversized — drops below the hip", "style_tags": ["oversized", "basics", "cozy"]}, {"category": "tops", "colors": ["black"], "id": "w_005", "name": "Black cropped zip hoodie", "notes": null, "style_tags": ["athletic", "streetwear", "cropped"]}, {"category": "outerwear", "colors": ["black"], "id": "w_006", "name": "Vintage black denim jacket", "notes": "Slightly cropped", "style_tags": ["denim", "vintage", "classic"]}, {"category": "shoes", "colors": ["white"], "id": "w_007", "name": "Chunky white sneakers", "notes": null, "style_tags": ["sneakers", "chunky", "streetwear"]}, {"category": "shoes", "colors": ["black"], "id": "w_008", "name": "Black combat boots", "notes": "Lace-up, mid-ankle height", "style_tags": ["boots", "grunge", "classic"]}, {"category": "accessories", "colors": ["brown"], "id": "w_009", "name": "Brown leather belt", "notes": null, "style_tags": ["classic", "earth tones", "accessories"]}, {"category": "accessories", "colors": ["black"], "id": "w_010", "name": "Black crossbody bag", "notes": null, "style_tags": ["minimal", "accessories", "everyday"]}]}}, "status_code": 200, "outcome": "success", "error": null, "duration_ms": 2445.484, "queue_ms": 0.0, "agent_ms": 2444.933, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 2, "reported_prompt_tokens": 1131, "reported_output_tokens": 234, "reported_total_tokens": 1365}}
{"timestamp": "2026-11-14T23:44:11.629+00:00", "request_id": "c617540a8e034364bcce782234c53fed", "method": "POST", "path": "/ask", "input_format": "json", "input": {"query": "90s track jacket in size M"}, "output_format": "json", "output": {"error": null, "fit_card": "I scored this navy and white 90s track jacket on Poshmark for $45.00! I styled it with a white ribbed tank, baggy dark-wash jeans, and chunky white sneakers for a cool, athletic streetwear look. It has a great lightweight feel that is perfect for layering.", "outfit_suggestion": "**Outfit 1: 90s Streetwear Casual**\n* **Pieces:** 90s Track Jacket — Navy/White Stripe, White ribbed tank top, Baggy straight-leg jeans, dark wash, Chunky white sneakers\n* **Why it works:** The white ribbed tank layers under the lightweight track jacket, while the baggy dark-wash jeans and chunky white sneakers lean completely into the jacket’s 90s athletic and streetwear aesthetic. \n* **Optional addition:** A classic silver chain necklace.\n\n**Outfit 2: High-Low Contrast**\n* **Pieces:** 90s Track Jacket — Navy/White Stripe, Wide-leg khaki trousers, Chunky white sneakers\n* **Why it works:** Pairing the sporty, navy-and-white track jacket with the neutral wide-leg khaki trousers creates a cool contrast between athletic streetwear and minimalist earth tones. \n* **Optional addition:** A simple minimalist watch or baseball cap.", "parsed": {"description": "90s track jacket in", "max_price": null, "size": "M"}, "query": "90s track jacket in size M", "search_results": [{"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, {"brand": null, "category": "outerwear", "colors": ["black"], "condition": "good", "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.", "id": "lst_022", "platform": "depop", "price": 75.0, "size": "M", "style_tags": ["90s", "vintage", "leather", "classic", "grunge"], "title": "90s Leather Bomber — Black"}, {"brand": null, "category": "outerwear", "colors": ["olive", "green"], "condition": "excellent", "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.", "id": "lst_032", "platform": "poshmark", "price": 33.0, "size": "M/L", "style_tags": ["earth tones", "classic", "layering", "minimal"], "title": "Shacket — Olive Canvas"}], "selected_item": {"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, "wardrobe": {"items": [{"category": "bottoms", "colors": ["dark blue", "indigo"], "id": "w_001", "name": "Baggy straight-leg jeans, dark wash", "notes": "High-waisted, sits above the hip", "style_tags": ["denim", "streetwear", "baggy"]}, {"category": "bottoms", "colors": ["khaki", "tan"], "id": "w_002", "name": "Wide-leg khaki trousers", "notes": null, "style_tags": ["earth tones", "minimal", "wide-leg"]}, {"category": "tops", "colors": ["white"], "id": "w_003", "name": "White ribbed tank top", "notes": "Goes with everything", "style_tags": ["basics", "minimal", "fitted"]}, {"category": "tops", "colors": ["grey", "charcoal"], "id": "w_004", "name": "Oversized grey crewneck sweatshirt", "notes": "Really oversized — drops below the hip", "style_tags": ["oversized", "basics", "cozy"]}, {"category": "tops", "colors": ["black"], "id": "w_005", "name": "Black cropped zip hoodie", "notes": null, "style_tags": ["athletic", "streetwear", "cropped"]}, {"category": "outerwear", "colors": ["black"], "id": "w_006", "name": "Vintage black denim jacket", "notes": "Slightly cropped", "style_tags": ["denim", "vintage", "classic"]}, {"category": "shoes", "colors": ["white"], "id": "w_007", "name": "Chunky white sneakers", "notes": null, "style_tags": ["sneakers", "chunky", "streetwear"]}, {"category": "shoes", "colors": ["black"], "id": "w_008", "name": "Black combat boots", "notes": "Lace-up, mid-ankle height", "style_tags": ["boots", "grunge", "classic"]}, {"category": "accessories", "colors": ["brown"], "id": "w_009", "name": "Brown leather belt", "notes": null, "style_tags": ["classic", "earth tones", "accessories"]}, {"category": "accessories", "colors": ["black"], "id": "w_010", "name": "Black crossbody bag", "notes": null, "style_tags": ["minimal", "accessories", "everyday"]}]}}, "status_code": 200, "outcome": "success", "error": null, "duration_ms": 2462.061, "queue_ms": 0.001, "agent_ms": 2461.457, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 2, "reported_prompt_tokens": 1130, "reported_output_tokens": 261, "reported_total_tokens": 1391}}
{"timestamp": "2026-11-14T23:44:24.357+00:00", "request_id": "84fc6d97ba764efab49cd16591f11596", "method": "POST", "path": "/ask", "input_format": "json", "input": {"query": "90s track jacket in size M"}, "output_format": "json", "output": {"error": null, "fit_card": "Scored this authentic Champion 90s Track Jacket for $45.0 on Poshmark! I paired the navy-and-white striped, full-zip layer with baggy dark wash jeans, a white ribbed tank top, and chunky sneakers for an effortless 90s athletic streetwear vibe.", "outfit_suggestion": "**Outfit 1: Casual Streetwear**\n*   **Pieces:** 90s Track Jacket, White ribbed tank top, Baggy straight-leg jeans (dark wash), Chunky white sneakers\n*   **Why it works:** Layering the track jacket over the white tank top leans into the 90s athletic aesthetic. The baggy dark wash jeans and chunky white sneakers match the streetwear vibe, while the white in the sneakers ties back to the jacket's stripe detail.\n*   *Suggested addition:* Silver hoop earrings or a simple chain necklace.\n\n**Outfit 2: High-Low Mix**\n*   **Pieces:** 90s Track Jacket, White ribbed tank top, Wide-leg khaki trousers, Black crossbody bag\n*   **Why it works:** Pairing the sporty, navy-and-white track jacket with wide-leg khaki trousers creates a smart-casual contrast. The fitted white tank top balances the voluminous trousers and the lightweight jacket. \n*   *Suggested addition:* Retro running shoes or minimalist leather loafers.", "parsed": {"description": "90s track jacket in", "max_price": null, "size": "M"}, "query": "90s track jacket in size M", "search_results": [{"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, {"brand": null, "category": "outerwear", "colors": ["black"], "condition": "good", "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.", "id": "lst_022", "platform": "depop", "price": 75.0, "size": "M", "style_tags": ["90s", "vintage", "leather", "classic", "grunge"], "title": "90s Leather Bomber — Black"}, {"brand": null, "category": "outerwear", "colors": ["olive", "green"], "condition": "excellent", "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.", "id": "lst_032", "platform": "poshmark", "price": 33.0, "size": "M/L", "style_tags": ["earth tones", "classic", "layering", "minimal"], "title": "Shacket — Olive Canvas"}], "selected_item": {"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, "wardrobe": {"items": [{"category": "bottoms", "colors": ["dark blue", "indigo"], "id": "w_001", "name": "Baggy straight-leg jeans, dark wash", "notes": "High-waisted, sits above the hip", "style_tags": ["denim", "streetwear", "baggy"]}, {"category": "bottoms", "colors": ["khaki", "tan"], "id": "w_002", "name": "Wide-leg khaki trousers", "notes": null, "style_tags": ["earth tones", "minimal", "wide-leg"]}, {"category": "tops", "colors": ["white"], "id": "w_003", "name": "White ribbed tank top", "notes": "Goes with everything", "style_tags": ["basics", "minimal", "fitted"]}, {"category": "tops", "colors": ["grey", "charcoal"], "id": "w_004", "name": "Oversized grey crewneck sweatshirt", "notes": "Really oversized — drops below the hip", "style_tags": ["oversized", "basics", "cozy"]}, {"category": "tops", "colors": ["black"], "id": "w_005", "name": "Black cropped zip hoodie", "notes": null, "style_tags": ["athletic", "streetwear", "cropped"]}, {"category": "outerwear", "colors": ["black"], "id": "w_006", "name": "Vintage black denim jacket", "notes": "Slightly cropped", "style_tags": ["denim", "vintage", "classic"]}, {"category": "shoes", "colors": ["white"], "id": "w_007", "name": "Chunky white sneakers", "notes": null, "style_tags": ["sneakers", "chunky", "streetwear"]}, {"category": "shoes", "colors": ["black"], "id": "w_008", "name": "Black combat boots", "notes": "Lace-up, mid-ankle height", "style_tags": ["boots", "grunge", "classic"]}, {"category": "accessories", "colors": ["brown"], "id": "w_009", "name": "Brown leather belt", "notes": null, "style_tags": ["classic", "earth tones", "accessories"]}, {"category": "accessories", "colors": ["black"], "id": "w_010", "name": "Black crossbody bag", "notes": null, "style_tags": ["minimal", "accessories", "everyday"]}]}}, "status_code": 200, "outcome": "success", "error": null, "duration_ms": 2449.678, "queue_ms": 0.001, "agent_ms": 2449.121, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 2, "reported_prompt_tokens": 1147, "reported_output_tokens": 277, "reported_total_tokens": 1424}}
{"timestamp": "2026-11-14T23:44:37.107+00:00", "request_id": "183a209bfa344e7fb2141d372a3066a3", "method": "POST", "path": "/ask", "input_format": "json", "input": {"query": "90s track jacket in size M"}, "output_format": "json", "output": {"error": null, "fit_card": "Scored this 90s Track Jacket for $45 on Poshmark. I styled it with a white ribbed tank top, baggy straight-leg jeans, and chunky white sneakers for an authentic 90s streetwear vibe.", "outfit_suggestion": "**Outfit 1: 90s Streetwear**\n*   **Pieces:** 90s Track Jacket, White ribbed tank top, Baggy straight-leg jeans, Chunky white sneakers.\n*   **Why it works:** The white tank pairs effortlessly with the white sleeve stripes, while the baggy dark wash jeans and chunky sneakers lean into the jacket's authentic 90s streetwear aesthetic. \n\n**Outfit 2: High-Low Contrast**\n*   **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, Chunky white sneakers.\n*   **Why it works:** Pairing the athletic, navy track jacket with tailored khaki trousers creates a sharp high-low contrast. The white sneakers tie the look together by picking up the jacket's white stripe details. *(Consider adding a simple white t-shirt underneath for layering).*", "parsed": {"description": "90s track jacket in", "max_price": null, "size": "M"}, "query": "90s track jacket in size M", "search_results": [{"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, {"brand": null, "category": "outerwear", "colors": ["black"], "condition": "good", "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.", "id": "lst_022", "platform": "depop", "price": 75.0, "size": "M", "style_tags": ["90s", "vintage", "leather", "classic", "grunge"], "title": "90s Leather Bomber — Black"}, {"brand": null, "category": "outerwear", "colors": ["olive", "green"], "condition": "excellent", "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.", "id": "lst_032", "platform": "poshmark", "price": 33.0, "size": "M/L", "style_tags": ["earth tones", "classic", "layering", "minimal"], "title": "Shacket — Olive Canvas"}], "selected_item": {"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, "wardrobe": {"items": [{"category": "bottoms", "colors": ["dark blue", "indigo"], "id": "w_001", "name": "Baggy straight-leg jeans, dark wash", "notes": "High-waisted, sits above the hip", "style_tags": ["denim", "streetwear", "baggy"]}, {"category": "bottoms", "colors": ["khaki", "tan"], "id": "w_002", "name": "Wide-leg khaki trousers", "notes": null, "style_tags": ["earth tones", "minimal", "wide-leg"]}, {"category": "tops", "colors": ["white"], "id": "w_003", "name": "White ribbed tank top", "notes": "Goes with everything", "style_tags": ["basics", "minimal", "fitted"]}, {"category": "tops", "colors": ["grey", "charcoal"], "id": "w_004", "name": "Oversized grey crewneck sweatshirt", "notes": "Really oversized — drops below the hip", "style_tags": ["oversized", "basics", "cozy"]}, {"category": "tops", "colors": ["black"], "id": "w_005", "name": "Black cropped zip hoodie", "notes": null, "style_tags": ["athletic", "streetwear", "cropped"]}, {"category": "outerwear", "colors": ["black"], "id": "w_006", "name": "Vintage black denim jacket", "notes": "Slightly cropped", "style_tags": ["denim", "vintage", "classic"]}, {"category": "shoes", "colors": ["white"], "id": "w_007", "name": "Chunky white sneakers", "notes": null, "style_tags": ["sneakers", "chunky", "streetwear"]}, {"category": "shoes", "colors": ["black"], "id": "w_008", "name": "Black combat boots", "notes": "Lace-up, mid-ankle height", "style_tags": ["boots", "grunge", "classic"]}, {"category": "accessories", "colors": ["brown"], "id": "w_009", "name": "Brown leather belt", "notes": null, "style_tags": ["classic", "earth tones", "accessories"]}, {"category": "accessories", "colors": ["black"], "id": "w_010", "name": "Black crossbody bag", "notes": null, "style_tags": ["minimal", "accessories", "everyday"]}]}}, "status_code": 200, "outcome": "success", "error": null, "duration_ms": 2377.478, "queue_ms": 0.001, "agent_ms": 2376.949, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 2, "reported_prompt_tokens": 1110, "reported_output_tokens": 226, "reported_total_tokens": 1336}}
{"timestamp": "2026-11-14T23:44:49.684+00:00", "request_id": "da349cb4b3fa47238be8a7a14b9a6d8d", "method": "POST", "path": "/ask", "input_format": "json", "input": {"query": "90s track jacket in size M"}, "output_format": "json", "output": {"error": null, "fit_card": "Scored this navy and white 90s Track Jacket for $45.0 on Poshmark! Paired with baggy dark wash jeans and chunky sneakers, it creates the ultimate casual streetwear vibe.", "outfit_suggestion": "**Outfit 1: Casual Streetwear**\n*   **Top:** White ribbed tank top\n*   **Bottoms:** Baggy straight-leg jeans, dark wash\n*   **Shoes:** Chunky white sneakers\n*   **Why it works:** The white ribbed tank highlights the athletic 90s aesthetic of the track jacket, while the dark wash baggy jeans and chunky white sneakers reinforce the retro streetwear vibe. \n\n**Outfit 2: High-Low Mix**\n*   **Bottoms:** Wide-leg khaki trousers\n*   **Shoes:** Chunky white sneakers\n*   **Suggested Addition:** A minimal silver chain necklace \n*   **Why it works:** Pairing the sporty navy and white track jacket with tailored wide-leg khaki trousers creates a balanced high-low look, anchored by the white sneakers to tie the colors together.", "parsed": {"description": "90s track jacket in", "max_price": null, "size": "M"}, "query": "90s track jacket in size M", "search_results": [{"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, {"brand": null, "category": "outerwear", "colors": ["black"], "condition": "good", "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.", "id": "lst_022", "platform": "depop", "price": 75.0, "size": "M", "style_tags": ["90s", "vintage", "leather", "classic", "grunge"], "title": "90s Leather Bomber — Black"}, {"brand": null, "category": "outerwear", "colors": ["olive", "green"], "condition": "excellent", "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.", "id": "lst_032", "platform": "poshmark", "price": 33.0, "size": "M/L", "style_tags": ["earth tones", "classic", "layering", "minimal"], "title": "Shacket — Olive Canvas"}], "selected_item": {"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, "wardrobe": {"items": [{"category": "bottoms", "colors": ["dark blue", "indigo"], "id": "w_001", "name": "Baggy straight-leg jeans, dark wash", "notes": "High-waisted, sits above the hip", "style_tags": ["denim", "streetwear", "baggy"]}, {"category": "bottoms", "colors": ["khaki", "tan"], "id": "w_002", "name": "Wide-leg khaki trousers", "notes": null, "style_tags": ["earth tones", "minimal", "wide-leg"]}, {"category": "tops", "colors": ["white"], "id": "w_003", "name": "White ribbed tank top", "notes": "Goes with everything", "style_tags": ["basics", "minimal", "fitted"]}, {"category": "tops", "colors": ["grey", "charcoal"], "id": "w_004", "name": "Oversized grey crewneck sweatshirt", "notes": "Really oversized — drops below the hip", "style_tags": ["oversized", "basics", "cozy"]}, {"category": "tops", "colors": ["black"], "id": "w_005", "name": "Black cropped zip hoodie", "notes": null, "style_tags": ["athletic", "streetwear", "cropped"]}, {"category": "outerwear", "colors": ["black"], "id": "w_006", "name": "Vintage black denim jacket", "notes": "Slightly cropped", "style_tags": ["denim", "vintage", "classic"]}, {"category": "shoes", "colors": ["white"], "id": "w_007", "name": "Chunky white sneakers", "notes": null, "style_tags": ["sneakers", "chunky", "streetwear"]}, {"category": "shoes", "colors": ["black"], "id": "w_008", "name": "Black combat boots", "notes": "Lace-up, mid-ankle height", "style_tags": ["boots", "grunge", "classic"]}, {"category": "accessories", "colors": ["brown"], "id": "w_009", "name": "Brown leather belt", "notes": null, "style_tags": ["classic", "earth tones", "accessories"]}, {"category": "accessories", "colors": ["black"], "id": "w_010", "name": "Black crossbody bag", "notes": null, "style_tags": ["minimal", "accessories", "everyday"]}]}}, "status_code": 200, "outcome": "success", "error": null, "duration_ms": 2317.371, "queue_ms": 0.001, "agent_ms": 2316.847, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 2, "reported_prompt_tokens": 1107, "reported_output_tokens": 217, "reported_total_tokens": 1324}}
{"timestamp": "2026-11-14T23:45:02.208+00:00", "request_id": "11ab596096c9420bb569f90482787d86", "method": "POST", "path": "/ask", "input_format": "json", "input": {"query": "90s track jacket in size M"}, "output_format": "json", "output": {"error": null, "fit_card": "I scored this vintage Champion 90s Track Jacket for just $45.00 on Poshmark! Paired with baggy jeans, a ribbed tank, and chunky sneakers, it creates the ultimate casual streetwear vibe.", "outfit_suggestion": "**Outfit 1: Casual Streetwear**\n*   **Pieces:** 90s Track Jacket, White ribbed tank top, Baggy straight-leg jeans, Chunky white sneakers.\n*   **Why it works:** The white ribbed tank top layers perfectly under the lightweight track jacket, while the baggy dark-wash jeans and chunky white sneakers lean into the jacket's authentic 90s and streetwear aesthetic.\n*   *Suggested addition:* A silver chain necklace to complete the retro look.\n\n**Outfit 2: High-Low Mix**\n*   **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, Chunky white sneakers.\n*   **Why it works:** Pairing the athletic, navy-and-white track jacket with tailored wide-leg khaki trousers creates a cool contrast between sporty and smart. The chunky white sneakers tie the relaxed silhouettes together. \n*   *Suggested addition:* A simple white t-shirt to wear underneath the unzipped jacket.", "parsed": {"description": "90s track jacket in", "max_price": null, "size": "M"}, "query": "90s track jacket in size M", "search_results": [{"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, {"brand": null, "category": "outerwear", "colors": ["black"], "condition": "good", "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.", "id": "lst_022", "platform": "depop", "price": 75.0, "size": "M", "style_tags": ["90s", "vintage", "leather", "classic", "grunge"], "title": "90s Leather Bomber — Black"}, {"brand": null, "category": "outerwear", "colors": ["olive", "green"], "condition": "excellent", "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.", "id": "lst_032", "platform": "poshmark", "price": 33.0, "size": "M/L", "style_tags": ["earth tones", "classic", "layering", "minimal"], "title": "Shacket — Olive Canvas"}], "selected_item": {"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, "wardrobe": {"items": [{"category": "bottoms", "colors": ["dark blue", "indigo"], "id": "w_001", "name": "Baggy straight-leg jeans, dark wash", "notes": "High-waisted, sits above the hip", "style_tags": ["denim", "streetwear", "baggy"]}, {"category": "bottoms", "colors": ["khaki", "tan"], "id": "w_002", "name": "Wide-leg khaki trousers", "notes": null, "style_tags": ["earth tones", "minimal", "wide-leg"]}, {"category": "tops", "colors": ["white"], "id": "w_003", "name": "White ribbed tank top", "notes": "Goes with everything", "style_tags": ["basics", "minimal", "fitted"]}, {"category": "tops", "colors": ["grey", "charcoal"], "id": "w_004", "name": "Oversized grey crewneck sweatshirt", "notes": "Really oversized — drops below the hip", "style_tags": ["oversized", "basics", "cozy"]}, {"category": "tops", "colors": ["black"], "id": "w_005", "name": "Black cropped zip hoodie", "notes": null, "style_tags": ["athletic", "streetwear", "cropped"]}, {"category": "outerwear", "colors": ["black"], "id": "w_006", "name": "Vintage black denim jacket", "notes": "Slightly cropped", "style_tags": ["denim", "vintage", "classic"]}, {"category": "shoes", "colors": ["white"], "id": "w_007", "name": "Chunky white sneakers", "notes": null, "style_tags": ["sneakers", "chunky", "streetwear"]}, {"category": "shoes", "colors": ["black"], "id": "w_008", "name": "Black combat boots", "notes": "Lace-up, mid-ankle height", "style_tags": ["boots", "grunge", "classic"]}, {"category": "accessories", "colors": ["brown"], "id": "w_009", "name": "Brown leather belt", "notes": null, "style_tags": ["classic", "earth tones", "accessories"]}, {"category": "accessories", "colors": ["black"], "id": "w_010", "name": "Black crossbody bag", "notes": null, "style_tags": ["minimal", "accessories", "everyday"]}]}}, "status_code": 200, "outcome": "success", "error": null, "duration_ms": 2542.3, "queue_ms": 0.001, "agent_ms": 2541.74, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 2, "reported_prompt_tokens": 1137, "reported_output_tokens": 251, "reported_total_tokens": 1388}}
{"timestamp": "2026-11-14T23:45:14.969+00:00", "request_id": "e5043aaeb92e4dc0ac49afee1e2b059a", "method": "POST", "path": "/ask", "input_format": "json", "input": {"query": "90s track jacket in size M"}, "output_format": "json", "output": {"error": null, "fit_card": "I am obsessed with this 90s Track Jacket I found on poshmark for $45.0! I styled it with a white ribbed tank, baggy straight-leg jeans, and chunky white sneakers for a cool, casual streetwear vibe.", "outfit_suggestion": "Here are two outfit suggestions using your new 90s track jacket:\n\n**Outfit 1: Casual Streetwear**\n*   **Pieces:** 90s Track Jacket, White ribbed tank top, Baggy straight-leg jeans, Chunky white sneakers\n*   **Why it works:** The fitted white tank balances the relaxed fit of the dark wash jeans, while the track jacket adds a sporty 90s layer. The white sneakers tie in the jacket's white stripe.\n*   **Optional addition:** Silver hoop earrings.\n\n**Outfit 2: High-Low Mix**\n*   **Pieces:** 90s Track Jacket, White ribbed tank top, Wide-leg khaki trousers, Black combat boots\n*   **Why it works:** Pairing the athletic navy-and-white track jacket with tailored khaki trousers creates a cool contrast between sporty and smart. The fitted white tank keeps the base clean, and the combat boots add a grounded edge.\n*   **Optional addition:** A minimalist silver chain necklace.", "parsed": {"description": "90s track jacket in", "max_price": null, "size": "M"}, "query": "90s track jacket in size M", "search_results": [{"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, {"brand": null, "category": "outerwear", "colors": ["black"], "condition": "good", "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.", "id": "lst_022", "platform": "depop", "price": 75.0, "size": "M", "style_tags": ["90s", "vintage", "leather", "classic", "grunge"], "title": "90s Leather Bomber — Black"}, {"brand": null, "category": "outerwear", "colors": ["olive", "green"], "condition": "excellent", "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.", "id": "lst_032", "platform": "poshmark", "price": 33.0, "size": "M/L", "style_tags": ["earth tones", "classic", "layering", "minimal"], "title": "Shacket — Olive Canvas"}], "selected_item": {"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, "wardrobe": {"items": [{"category": "bottoms", "colors": ["dark blue", "indigo"], "id": "w_001", "name": "Baggy straight-leg jeans, dark wash", "notes": "High-waisted, sits above the hip", "style_tags": ["denim", "streetwear", "baggy"]}, {"category": "bottoms", "colors": ["khaki", "tan"], "id": "w_002", "name": "Wide-leg khaki trousers", "notes": null, "style_tags": ["earth tones", "minimal", "wide-leg"]}, {"category": "tops", "colors": ["white"], "id": "w_003", "name": "White ribbed tank top", "notes": "Goes with everything", "style_tags": ["basics", "minimal", "fitted"]}, {"category": "tops", "colors": ["grey", "charcoal"], "id": "w_004", "name": "Oversized grey crewneck sweatshirt", "notes": "Really oversized — drops below the hip", "style_tags": ["oversized", "basics", "cozy"]}, {"category": "tops", "colors": ["black"], "id": "w_005", "name": "Black cropped zip hoodie", "notes": null, "style_tags": ["athletic", "streetwear", "cropped"]}, {"category": "outerwear", "colors": ["black"], "id": "w_006", "name": "Vintage black denim jacket", "notes": "Slightly cropped", "style_tags": ["denim", "vintage", "classic"]}, {"category": "shoes", "colors": ["white"], "id": "w_007", "name": "Chunky white sneakers", "notes": null, "style_tags": ["sneakers", "chunky", "streetwear"]}, {"category": "shoes", "colors": ["black"], "id": "w_008", "name": "Black combat boots", "notes": "Lace-up, mid-ankle height", "style_tags": ["boots", "grunge", "classic"]}, {"category": "accessories", "colors": ["brown"], "id": "w_009", "name": "Brown leather belt", "notes": null, "style_tags": ["classic", "earth tones", "accessories"]}, {"category": "accessories", "colors": ["black"], "id": "w_010", "name": "Black crossbody bag", "notes": null, "style_tags": ["minimal", "accessories", "everyday"]}]}}, "status_code": 200, "outcome": "success", "error": null, "duration_ms": 2452.776, "queue_ms": 0.001, "agent_ms": 2452.246, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 2, "reported_prompt_tokens": 1144, "reported_output_tokens": 262, "reported_total_tokens": 1406}}
{"timestamp": "2026-11-14T23:45:27.603+00:00", "request_id": "5b6b515e886f4f80b22aafc44c56eeba", "method": "POST", "path": "/ask", "input_format": "json", "input": {"query": "90s track jacket in size M"}, "output_format": "json", "output": {"error": null, "fit_card": "Scored this vintage 90s Track Jacket on Poshmark for $45.0! Paired with baggy jeans, a ribbed tank, and chunky sneakers, it creates the ultimate casual streetwear vibe.", "outfit_suggestion": "Here are two outfit options using your new track jacket:\n\n**Outfit 1: Casual Streetwear**\n* **Pieces:** 90s Track Jacket, Baggy straight-leg jeans, White ribbed tank top, Chunky white sneakers, Black crossbody bag.\n* **Why it works:** The fitted white tank balances the volume of the baggy dark wash jeans. Layering the lightweight track jacket unzipped over the tank leans into the 90s streetwear aesthetic, while the white sneakers tie in the jacket's stripe detail.\n\n**Outfit 2: High-Low Contrast**\n* **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, White ribbed tank top, Chunky white sneakers. \n* **Why it works:** Pairing the athletic navy-and-white jacket with tailored khaki trousers creates a stylish contrast between sportswear and smart-casual separates. Keep the jacket fully zipped for a streamlined top, and add a simple ball cap to complete the look.", "parsed": {"description": "90s track jacket in", "max_price": null, "size": "M"}, "query": "90s track jacket in size M", "search_results": [{"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, {"brand": null, "category": "outerwear", "colors": ["black"], "condition": "good", "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.", "id": "lst_022", "platform": "depop", "price": 75.0, "size": "M", "style_tags": ["90s", "vintage", "leather", "classic", "grunge"], "title": "90s Leather Bomber — Black"}, {"brand": null, "category": "outerwear", "colors": ["olive", "green"], "condition": "excellent", "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.", "id": "lst_032", "platform": "poshmark", "price": 33.0, "size": "M/L", "style_tags": ["earth tones", "classic", "layering", "minimal"], "title": "Shacket — Olive Canvas"}], "selected_item": {"brand": "Champion", "category": "outerwear", "colors": ["navy", "white"], "condition": "excellent", "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.", "id": "lst_004", "platform": "poshmark", "price": 45.0, "size": "M", "style_tags": ["90s", "vintage", "athletic", "streetwear"], "title": "90s Track Jacket — Navy/White Stripe"}, "wardrobe": {"items": [{"category": "bottoms", "colors": ["dark blue", "indigo"], "id": "w_001", "name": "Baggy straight-leg jeans, dark wash", "notes": "High-waisted, sits above the hip", "style_tags": ["denim", "streetwear", "baggy"]}, {"category": "bottoms", "colors": ["khaki", "tan"], "id": "w_002", "name": "Wide-leg khaki trousers", "notes": null, "style_tags": ["earth tones", "minimal", "wide-leg"]}, {"category": "tops", "colors": ["white"], "id": "w_003", "name": "White ribbed tank top", "notes": "Goes with everything", "style_tags": ["basics", "minimal", "fitted"]}, {"category": "tops", "colors": ["grey", "charcoal"], "id": "w_004", "name": "Oversized grey crewneck sweatshirt", "notes": "Really oversized — drops below the hip", "style_tags": ["oversized", "basics", "cozy"]}, {"category": "tops", "colors": ["black"], "id": "w_005", "name": "Black cropped zip hoodie", "notes": null, "style_tags": ["athletic", "streetwear", "cropped"]}, {"category": "outerwear", "colors": ["black"], "id": "w_006", "name": "Vintage black denim jacket", "notes": "Slightly cropped", "style_tags": ["denim", "vintage", "classic"]}, {"category": "shoes", "colors": ["white"], "id": "w_007", "name": "Chunky white sneakers", "notes": null, "style_tags": ["sneakers", "chunky", "streetwear"]}, {"category": "shoes", "colors": ["black"], "id": "w_008", "name": "Black combat boots", "notes": "Lace-up, mid-ankle height", "style_tags": ["boots", "grunge", "classic"]}, {"category": "accessories", "colors": ["brown"], "id": "w_009", "name": "Brown leather belt", "notes": null, "style_tags": ["classic", "earth tones", "accessories"]}, {"category": "accessories", "colors": ["black"], "id": "w_010", "name": "Black crossbody bag", "notes": null, "style_tags": ["minimal", "accessories", "everyday"]}]}}, "status_code": 200, "outcome": "success", "error": null, "duration_ms": 2481.267, "queue_ms": 0.0, "agent_ms": 2480.718, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 2, "reported_prompt_tokens": 1134, "reported_output_tokens": 245, "reported_total_tokens": 1379}}
{"timestamp": "2026-11-14T23:45:30.259+00:00", "request_id": "4c903db4923d4cf29b41f38249c4a91a", "method": "POST", "path": "/ask", "input_format": "json", "input": {}, "output_format": "json", "output": {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}, "status_code": 400, "outcome": "rejected", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_ms": 0.308, "queue_ms": 0.0, "agent_ms": 0.0, "configured_model": "gemini-3.5-flash-lite", "cache_enabled": false, "model_usage": {"model_attempts": 0, "reported_prompt_tokens": 0, "reported_output_tokens": 0, "reported_total_tokens": 0}}
```

The first runtime export requested `--since 2h` and was rejected by Vercel's Hobby retention limit, leaving an empty file. Changing the window to `--since 30m` recovered all eleven matching records without repeating any model calls. The initial incomplete report and summary are preserved alongside the recovered evidence; see `results/capstone_m3/log_recovery.md`.

### What It Costs

- Completed outfits: 10/10 attempts.
- Mean client elapsed time per attempted request: 2.90604 seconds.
- Mean server elapsed time per attempted request: 2.67592 seconds.
- Mean reported tokens per attempted request: 1400.4.
- Reported model usage totals: `{"model_attempts": 20, "reported_output_tokens": 2600, "reported_prompt_tokens": 11404, "reported_total_tokens": 14004}`.

Sequential uncached matching attempts; no warm-up excluded; all attempted runs, including failures, remain in the averages. The rejected-input example is excluded from the cost sample. Client duration is wall time, including network and waits, not CPU time. Pauses between requests are excluded; waits within a request are included. Tokens are provider-reported adapter counters, not verified billing or API dollars.

Both elapsed-time figures measure wall time, not CPU consumption. A zero reported token count, including after a model attempt, does not establish zero token usage or zero spend. No dollar cost is inferred from a pricing page.

Usage records with model attempts but zero reported tokens: 0.

Client responses, original runtime export, matched application records and the numeric summary are saved under `results/capstone_m3`.

**For 100 people a day:** Assuming each person makes one matching request, with usage like this ten-run sample, the daily total would be `100 × 1400.4 = 140,040` reported tokens and `100 × 2 = 200` model attempts. The measured token average comes from `14,004 ÷ 10 = 1400.4` tokens per request. More requests per person would multiply those totals again; these are usage projections, not an API bill.

At the same measured averages, 100 sequential requests would add up to `100 × 2.90604 = 290.604` seconds of client waiting and `100 × 2.67592 = 267.592` seconds of server wall time. These totals exclude pauses between requests and the separate log-export step. They do not measure CPU use or show that the service can handle 100 simultaneous users. The cost sample uses one query, so different queries, output lengths and retries could change it. [Ten-run measurement](results/capstone_m3/summary.json).

<!-- capstone-formal-baseline -->

### Run Log — Before

I ran all five criteria three times with the same committed code and criteria. Each trial used one hosted warm-up followed by five measured track-jacket requests. Those five requests supplied criteria 1, 3 and 4; the warm-up was excluded from their scores. Criterion 2 used five hosted health requests per trial. Criterion 5 used ten health requests per trial in a separate local instance with an invalid log destination, leaving the public service unchanged.

All three trial records identify collector revision `8bbd9eb` and the same criteria hash. The frozen file hashes and test settings are in [the evaluation plan](results/capstone_before/evaluation_plan.json).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Hosted completion | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Recoverable health logs | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Response within 45 seconds | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Completed output and reported usage | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Visible logging failure | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

All five targets were met in all three trials. This checks completion, recoverable records, the stated time limit, reported usage and the controlled logging-failure behavior. It does not establish outfit quality, accurate API billing or resilience to a real Vercel storage outage.

**Log recovery:** The immediate exports for trials 2 and 3 omitted their last outfit record and five health records. A later read-only export recovered those same records, with inputs, outputs and statuses matching the original responses. No requests were repeated and no code or targets changed. The [recovery note](results/capstone_before/export_recovery.md) explains the original exports and initial incomplete tallies retained alongside the final baseline.

**Repeated-run check:** The 15 measured requests have distinct request IDs and 15 different outfit/fit-card output pairs. Their records all show caching disabled, two model attempts each and positive reported token usage. The identical pass counts therefore do not come from reusing saved responses. These checks exclude the three warm-ups; see [the repetition check](results/capstone_before/repetition_check.json).

**Observed response times:** Trial 1: 17.623–21.377 seconds; Trial 2: 2.491–2.720 seconds; Trial 3: 2.513–5.904 seconds. These ranges exclude warm-ups and the 10-second pauses between requests. Trial 1 was slower than the later trials, while all measured requests remained below 45 seconds. These observations alone do not establish the cause of the difference.

The excerpts below select existing fields from the saved responses and application records. Values and generated text are unchanged. Full responses, stderr files, runtime exports and per-request assessments remain in [the baseline evidence](results/capstone_before/).

**Criterion 1 — completed hosted response, trial 1, request 2.** Produced by `agent.py::run_agent`, returned by `serve.py::ask`, and captured by `tools/measure_capstone.py::request_once`. Source: [client responses](results/capstone_before/trial1/client_requests.jsonl).

```json
{
  "trial": 1,
  "slot": 2,
  "http_status": 200,
  "request_id": "b460aa161a9a4a61ac92390d6685f9db",
  "response": {
    "selected_item": {
      "brand": "Champion",
      "category": "outerwear",
      "colors": [
        "navy",
        "white"
      ],
      "condition": "excellent",
      "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
      "id": "lst_004",
      "platform": "poshmark",
      "price": 45.0,
      "size": "M",
      "style_tags": [
        "90s",
        "vintage",
        "athletic",
        "streetwear"
      ],
      "title": "90s Track Jacket — Navy/White Stripe"
    },
    "outfit_suggestion": "**Outfit 1: 90s Streetwear**\n*   **Pieces:** 90s Track Jacket, White ribbed tank top, Baggy straight-leg jeans, Chunky white sneakers.\n*   **Why it works:** The white ribbed tank layers perfectly under the lightweight track jacket. Pairing it with baggy dark-wash jeans and chunky white sneakers leans into a cohesive 90s streetwear aesthetic, with the white sneakers tying in the jacket's white stripes.\n*   *Suggested addition:* Silver hoop earrings.\n\n**Outfit 2: High-Low Casual**\n*   **Pieces:** 90s Track Jacket, White ribbed tank top, Wide-leg khaki trousers, Chunky white sneakers.\n*   **Why it works:** The sporty navy-and-white track jacket contrasts sharply with clean khaki trousers for an effortless high-low mix. The fitted white tank balances the wide-leg silhouette. \n*   *Suggested addition:* A minimalist baseball cap.",
    "fit_card": "Scored this authentic 90s track jacket for $45.0 on Poshmark! Paired with a white ribbed tank, baggy jeans, and chunky sneakers, it creates a cohesive 90s streetwear aesthetic.",
    "error": null
  }
}
```

**Criterion 2 — recovered hosted health record, trial 1.** Produced by `serve.py::finish_request_record` and `run_log.py::append_record`, mirrored to Vercel by `run_log.py::mirror_record`. Source: [matched application records](results/capstone_before/trial1/matched_application_records.jsonl).

```json
{
  "timestamp": "2026-11-15T06:16:12.752+00:00",
  "request_id": "7160680289284d9390fe2b14c0ad0a98",
  "method": "GET",
  "path": "/health",
  "input_format": "empty",
  "input": null,
  "output_format": "json",
  "output": {
    "status": "ok"
  },
  "status_code": 200,
  "outcome": "success",
  "error": null,
  "duration_ms": 0.232,
  "queue_ms": 0.0,
  "agent_ms": 0.0,
  "configured_model": "gemini-3.5-flash-lite",
  "cache_enabled": false,
  "model_usage": {
    "model_attempts": 0,
    "reported_prompt_tokens": 0,
    "reported_output_tokens": 0,
    "reported_total_tokens": 0
  }
}
```

**Criterion 3 — slowest measured client response, trial 1, request 2.** Produced by `tools/measure_capstone.py::request_once`. This is the same request as the completed response shown for criterion 1, so its generated outputs are shown there. Source: [client responses](results/capstone_before/trial1/client_requests.jsonl).

```json
{
  "trial": 1,
  "slot": 2,
  "timestamp": "2026-11-15T06:14:19.840254+00:00",
  "url": "https://fitfindr-capstone.vercel.app/ask",
  "http_status": 200,
  "request_id": "b460aa161a9a4a61ac92390d6685f9db",
  "client_elapsed_ms": 21377.034,
  "transport_error": null
}
```

**Criterion 4 — recorded usage for the same completed request.** Produced by `serve.py::model_usage_snapshot` and `serve.py::finish_request_record`. Source: [matched application records](results/capstone_before/trial1/matched_application_records.jsonl).

```json
{
  "timestamp": "2026-11-15T06:14:19.989+00:00",
  "request_id": "b460aa161a9a4a61ac92390d6685f9db",
  "status_code": 200,
  "outcome": "success",
  "cache_enabled": false,
  "model_usage": {
    "model_attempts": 2,
    "reported_prompt_tokens": 1136,
    "reported_output_tokens": 251,
    "reported_total_tokens": 1387
  }
}
```

**Criterion 5 — isolated local logging failure, trial 1.** `tools/evaluate_capstone.py::fault_trial` configured a log path whose parent was a regular file. `serve.py::finish_request_record` retained HTTP 200, set the failure header and emitted the matching stderr error. Sources: [client responses](results/capstone_before/trial1/client_requests.jsonl), [fault setup](results/capstone_before/trial1/fault_setup.json), and [stderr](results/capstone_before/trial1/fault_stderr.txt).

```json
{
  "trial": 1,
  "slot": 1,
  "method": "GET",
  "url": "http://127.0.0.1:57069/health",
  "http_status": 200,
  "request_id": "6089d619feb94d2abef3c1400ef4c19b",
  "run_log": "failed",
  "response": {
    "status": "ok"
  },
  "transport_error": null
}
```

Matching original stderr line:

```text
[2026-11-14 22:13:20,224] ERROR in serve: Could not save request 6089d619feb94d2abef3c1400ef4c19b: [Errno 17] File exists: '/var/folders/9g/v18s588943g4v58_2hbz9vyc0000gn/T/fitfindr-log-fault-uzbchkhd/regular_file_not_directory'
```

The [machine-readable summary](results/capstone_before/summary.json) and [generated report](results/capstone_before/report.md) retain the complete counts and assessments. The original Milestone 3 ten-run cost measurement remains separate from this formal baseline.

<!-- capstone-milestone6 -->

### Verdicts and diagnosis

All five criteria were MET in all three baseline trials, as shown in Run Log — Before. There is no missed criterion to assign to a failing stage.

My targets were basic in some places. Criterion 1 checks whether the workflow finishes, without checking the quality of the outfit. Criterion 4 checks that usage is reported, without checking its billing accuracy. Criterion 5 checks one controlled local log-path fault. Passing these checks does not cover every failure the hosted service could have.

The clearest target I would tighten in a future version is criterion 3: from at least 4 of 5 responses within 45 seconds to at least 4 of 5 within 10 seconds. The first trial took 17.623–21.377 seconds per measured request, which the current target accepts even though that wait would be noticeable to a user. This is a proposed future standard; the actual criterion stays at 45 seconds for the before-and-after comparison.

One operational weakness did show up while collecting evidence. The first log export recovered 10/10 required records in trial 1, then only 4/10 in trial 2 and 4/10 in trial 3: 18/30 altogether. The missing records belonged to the last outfit request and the health requests. Their responses reported saved logs, and a later export recovered the matching records without repeating any requests.

The stage was the export and verification step. Its mechanism was a one-shot fetch that accepted a successful CLI exit without checking whether all expected request IDs were actually present. The observed records became available to a later fetch; these results do not establish the precise internal platform cause. Manual recovery completed the final baseline, so the initial incomplete exports are not being counted as failed application trials. The preserved files and [recovery note](results/capstone_before/export_recovery.md) show that history.

### The Improvement — verified log capture

I changed one part of the operational layer: the log-export step. `tools/evaluate_capstone.py export-logs` now compares recovered records with the ten required request IDs for that trial: five measured outfit requests and five health requests. It checks their inputs, outputs and HTTP statuses too. Warm-up records are retained when available but excluded from that ten-record target.

If records are missing, the command fetches existing logs again, up to six attempts with five seconds between attempts. It never repeats an outfit request. Each raw export, CLI stderr and attempt count is saved, and the command only reports completion after the matching records are written to the evidence file. If it reaches the limit, it returns an error and preserves the partial capture.

The intended benefit was to reduce manual recovery after an immediate export. I compared record coverage when the configured capture step finished, plus export attempts and manual reinvocation. This additional capture measure does not replace or change the five acceptance criteria; the actual results are below.

The tradeoff is extra log queries and waiting when records are not available immediately. This happens after the application requests, outside their measured response times. This change is not expected to make outfit generation faster, and a faster after-run would not by itself prove that the exporter caused it.

### Run Log — After

I reran the full set three times with the original criteria, query, request counts and cache settings. The application, data and shared request helper hashes match the before plan; only the evaluation/export tool changed. Criteria 1–4 ran against the public API. Criterion 5 again used a separate local instance with an invalid log destination.

Trial 1 was kept when a local Git preflight timed out before trial 2 started. Downloading the offloaded iCloud files restored the check, and every frozen source hash still matched. I resumed trials 2 and 3 without repeating trial 1 or changing the application. That setup delay is outside the timed HTTP requests.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Hosted completion | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Recoverable health logs | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Response within 45 seconds | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Completed output and reported usage | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Visible logging failure | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

All five criteria remained MET. The [side-by-side result artifact](results/capstone_after/comparison.md) contains both complete sets of trial counts. The [after summary](results/capstone_after/summary.json) and per-trial assessment files retain the individual observations.

### Before/after comparison

| Measure | Before | After |
|---|---|---|
| Criteria meeting their targets in all three trials | 5/5 | 5/5 |
| Required records visible in the first fetch | 18/30 | 18/30 |
| Required records captured when the configured capture command finished | 18/30 | 30/30 |
| Trials needing manual log recovery after export | 2/3 | 0/3 |

The before criterion scores already include the manual recovery, so this is not an increase in the acceptance pass rate. The improvement removed that manual step in these after runs. The five acceptance targets were not changed.

| After trial | First fetch | Verified capture | CLI queries | Capture elapsed time |
|---|---|---|---|---|
| 1 | 10/10 | 10/10 | 1 | 13.639s |
| 2 | 4/10 | 10/10 | 2 | 14.555s |
| 3 | 4/10 | 10/10 | 2 | 11.402s |

Trials 2 and 3 reproduced the same missing-record pattern: their first fetch had 4/10 required records. The second fetch found all ten, and each trial completed in one export-command invocation. The exporter repeated zero application requests. Raw snapshots, stderr and each attempt's coverage are saved in the trial folders and `log_export_audit.json` files.

**Did it help?** Yes, for the observed capture problem. The configured step now checks completeness and obtained 30/30 required records without manual recovery. It used five CLI queries across three trials, including two automatic retries, with five seconds of retry waiting in each of trials 2 and 3. This extra work happens after the application responses, outside the latency criterion. The measured capture-command times are shown above; the before CLI command duration was not measured, so I am not claiming an export-speed improvement.

The generation code was unchanged. These runs do not establish that the export change caused faster generation; export waiting was outside the timed requests. The retry limit, log-retention window and service outages can still prevent capture; three successful after trials do not establish that every future export will succeed.

The after evidence uses fresh requests and output rather than the saved baseline. See [the repetition check](results/capstone_after/repetition_check.json) and [the measured comparison](results/capstone_after/comparison.json). The excerpts below select unchanged fields from the actual after responses and records. Full data remains in `results/capstone_after/`.

**Criterion 1 — actual after response, trial 3, request 3.** Produced by `agent.py::run_agent` and `serve.py::ask`, captured by `tools/measure_capstone.py::request_once`. [Source client responses](results/capstone_after/trial3/client_requests.jsonl).

```json
{
  "trial": 3,
  "slot": 3,
  "http_status": 200,
  "request_id": "107e765542224d8383472b5831ed64d8",
  "response": {
    "selected_item": {
      "brand": "Champion",
      "category": "outerwear",
      "colors": [
        "navy",
        "white"
      ],
      "condition": "excellent",
      "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
      "id": "lst_004",
      "platform": "poshmark",
      "price": 45.0,
      "size": "M",
      "style_tags": [
        "90s",
        "vintage",
        "athletic",
        "streetwear"
      ],
      "title": "90s Track Jacket — Navy/White Stripe"
    },
    "outfit_suggestion": "**Outfit 1: Casual Streetwear**\n*   **Top:** White ribbed tank top\n*   **Bottoms:** Baggy straight-leg jeans, dark wash\n*   **Shoes:** Chunky white sneakers\n*   **Why it works:** The white tank pairs with the white stripe on the track jacket, while the baggy jeans and chunky sneakers lean into the jacket's 90s athletic aesthetic. *(Optional addition: Silver hoop earrings to complete the retro look.)*\n\n**Outfit 2: High-Low Contrast**\n*   **Bottoms:** Wide-leg khaki trousers\n*   **Shoes:** Chunky white sneakers\n*   **Why it works:** Pairing the sporty navy track jacket with tailored khaki trousers creates a stylish contrast between athletic and minimal streetwear, unified by the white sneakers. *(Optional addition: A simple white t-shirt layered underneath.)*",
    "fit_card": "Scored this authentic 90s track jacket on Poshmark for just $45.00! I styled the navy and white zip-up over a white ribbed tank with baggy dark wash jeans and chunky sneakers. It gives off a totally effortless, retro streetwear vibe.",
    "error": null
  }
}
```

**Criterion 2 — actual recovered health record, after trial 1.** Produced by `serve.py::finish_request_record`, saved by `run_log.py::append_record` and recovered by `tools/evaluate_capstone.py::export_logs`. [Source application records](results/capstone_after/trial1/matched_application_records.jsonl).

```json
{
  "timestamp": "2026-11-15T20:42:10.654+00:00",
  "request_id": "e1e94c0a0bc144d393f37d233d07ccb4",
  "method": "GET",
  "path": "/health",
  "input_format": "empty",
  "input": null,
  "output_format": "json",
  "output": {
    "status": "ok"
  },
  "status_code": 200,
  "outcome": "success",
  "error": null,
  "duration_ms": 0.262,
  "queue_ms": 0.0,
  "agent_ms": 0.0,
  "configured_model": "gemini-3.5-flash-lite",
  "cache_enabled": false,
  "model_usage": {
    "model_attempts": 0,
    "reported_prompt_tokens": 0,
    "reported_output_tokens": 0,
    "reported_total_tokens": 0
  }
}
```

**Criterion 3 — slowest measured after response.** Produced by `tools/measure_capstone.py::request_once`. Its completed generated outputs are shown for the same request ID under criterion 1 above. [Source client responses](results/capstone_after/trial3/client_requests.jsonl).

```json
{
  "trial": 3,
  "slot": 3,
  "timestamp": "2026-11-16T00:42:06.979853+00:00",
  "url": "https://fitfindr-capstone.vercel.app/ask",
  "http_status": 200,
  "request_id": "107e765542224d8383472b5831ed64d8",
  "client_elapsed_ms": 4234.31,
  "transport_error": null
}
```

**Criterion 4 — actual usage record for that completed request.** Produced by `serve.py::model_usage_snapshot` and `serve.py::finish_request_record`. [Source application records](results/capstone_after/trial3/matched_application_records.jsonl).

```json
{
  "timestamp": "2026-11-16T00:42:07.245+00:00",
  "request_id": "107e765542224d8383472b5831ed64d8",
  "status_code": 200,
  "outcome": "success",
  "cache_enabled": false,
  "model_usage": {
    "model_attempts": 2,
    "reported_prompt_tokens": 1113,
    "reported_output_tokens": 238,
    "reported_total_tokens": 1351
  }
}
```

**Criterion 5 — actual local logging-failure response and stderr, after trial 1.** Triggered by `tools/evaluate_capstone.py::fault_trial`; the header and error come from `serve.py::finish_request_record`. [Client responses](results/capstone_after/trial1/client_requests.jsonl), [fault setup](results/capstone_after/trial1/fault_setup.json) and [stderr](results/capstone_after/trial1/fault_stderr.txt).

```json
{
  "trial": 1,
  "slot": 1,
  "method": "GET",
  "url": "http://127.0.0.1:64873/health",
  "http_status": 200,
  "request_id": "54791f214f2647ea8a92f6ab48e895a8",
  "run_log": "failed",
  "response": {
    "status": "ok"
  },
  "transport_error": null
}
```

```text
[2026-11-15 12:41:00,438] ERROR in serve: Could not save request 54791f214f2647ea8a92f6ab48e895a8: [Errno 17] File exists: '/var/folders/9g/v18s588943g4v58_2hbz9vyc0000gn/T/fitfindr-log-fault-y7wc1iuw/regular_file_not_directory'
```


<!-- capstone-milestone7 -->

### What's Still Broken

All five capstone criteria were MET in all three before and after trials. I would still tighten criterion 3 from at least 4 of 5 responses within 45 seconds to at least 4 of 5 within 10 seconds in a future test. The first before trial took 17.623–21.377 seconds per measured request, so the current target accepts a wait I would want to reduce. The recorded 45-second criterion and its verdict stay unchanged.

Log capture still depends on exporting records while they are available. Vercel's temporary file is not a shared, permanent history, and the export command stops after six attempts. The improvement recovered 30/30 required records automatically in the after trials, but that does not guarantee recovery after a longer delay or an outage. I would address this with durable storage for the structured records. I stopped after the one measured exporter change so the comparison remained about that change.

The tests also used one matching query and sequential requests. They check completion, timing and reported usage, rather than whether every outfit is useful or every token counter matches billing. The logging-failure test used a controlled local instance; it does not demonstrate how a hosted platform timeout behaves. Broader query, load and failure coverage remains outside this capstone's tested scope.

### What I'd Do Next

If I had another unit, I would first send each structured request record to durable shared storage and test that it can be recovered after restarting the service. I would do that before adding another FitFindr feature because recovering evidence is still dependent on a timely export, and without that record I cannot reliably investigate a later failure.

### How I Used AI

**Moment 1 — Adding the hosted run path and measurements**

- *What I asked for:* Help wrapping the existing FitFindr agent with structured request logging, preparing the Vercel setup and measuring usage without changing the search or generation behavior.
- *What came back:* AI helped implement the request records and usage capture, prepare the deployment and measurement commands. It also helped investigate the missing dependencies in the hosted MCP subprocess.
- *What I did with it:* I chose Vercel, ran the hosted measurement commands and shared the actual terminal output. The write-up uses the ten recorded requests and their reported usage. It keeps model tokens separate from billing and wall time separate from CPU time.

**Moment 2 — Checking incomplete log exports**

- *What I asked for:* Help understanding why successful HTTP requests were missing from the immediate log export, and how to improve capture without repeating model requests.
- *What came back:* AI compared request IDs with the recovered records, helped implement bounded retries and completeness checks in the exporter.
- *What I did with it:* I ran the three after trials and log exports and provided the terminal results. The original trials and criteria were preserved. I kept the unchanged acceptance pass rate in the report and used the capture result—18/30 records at the end of the original export step versus 30/30 after verified capture—to explain what improved. The extra queries and waiting are reported too.

### Submission check

The capstone extends the existing FitFindr repository with Shape A and the hosted Path A. The public API and reproducible run instructions are in [RUNNING.md](RUNNING.md). The README includes ten real instrumentation records plus a rejected request, the measured cost and daily arithmetic, both three-trial result sets, all five verdicts, the diagnosis of incomplete exports and the measured improvement. The original criteria and earlier project sections are retained.


---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
