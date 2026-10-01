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

- **What it does:** Searches the local listings by description keywords, with optional size and price filters. It does not call the model. Matching and ranking follow the rules below.
- **Inputs:** `description` (str), `size` (str or None, default None), and `max_price` (float or None, default None). None skips that filter; the price limit is inclusive.
- **Returns:** A list of matching listing dictionaries, highest keyword score first, up to `config.SEARCH_RESULT_LIMIT` results (currently 10). Each dictionary contains `id` (str), `title` (str), `description` (str), `category` (str), `style_tags` (list of strings), `size` (str), `condition` (str), `price` (float), `colors` (list of strings), `brand` (str or None), and `platform` (str).
- **When it has nothing:** Returns `[]` when no listing passes the filters and matches at least one description keyword. An empty or whitespace-only description also returns `[]`.

**Search matching rules:**

- Use the instructor's `_keywords` helper on the description and on the listing's `title`, `description`, and `style_tags`. It lowercases text, extracts sequences of letters a–z, digits, and apostrophes, and removes single-character tokens and these stopwords: `a`, `an`, `and`, `the`, `for`, `with`, `under`, `over`, `in`, `of`. Score each listing by the number of distinct shared keywords. A keyword counts once even if it appears in several fields. Require a score above zero, and keep the original file order when scores tie. This allows partial keyword matches; a description with no remaining keywords returns `[]`.
- Keep only listings whose price is at or below `max_price`, when provided.
- Use the instructor's `_size_matches` helper. None or an empty string skips size filtering. Otherwise, remove parenthetical fit notes, split both sizes on `/`, trim surrounding whitespace, and compare the resulting labels without regard to capitalization. Any shared label is a match: `M` matches `S/M`, and a request for `S/M` can match either `S` or `M`. `L` does not match `XL`.
- A listing with a size label starting with `ONE SIZE` passes any requested size filter, including adjustable and oversized variants. This is the helper's matching rule, not a guarantee of physical fit.
- Other numeric size labels must match exactly after that normalization. `8` does not match `US 8`, and `W30` does not match `W30 L30`. The helper does not convert shoe-size formats or split waist and length measurements.

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

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```
$ python -c "from tools import suggest_outfit; ..."

```

```
$ python -c "from tools import create_fit_card; ..."

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

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
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



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

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



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
