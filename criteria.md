# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->
Completing the full path requires search to find an item and two model calls to return an outfit suggestion and a fit card. I expect this to work in at least four of five tries, allowing one failure because the model-dependent steps may not always complete successfully.
---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
Checking whether search returned an empty list is a decision made by my code, without asking the model. I expect all five tries to stop before the next tool and tell the user what they can change, because continuing with no selected item would leave the next tool without its required input.
---

## 3. Each request uses its own selected item without carrying over old state

In all five trials, each consisting of three consecutive requests in the same Python process—a matching tee search, an empty search, and a matching jacket search—the item passed to both `suggest_outfit` and `create_fit_card` must contain exactly the same keys and values as that request's `session["selected_item"]` and first search result. The empty request must leave `selected_item`, `outfit_suggestion`, and `fit_card` as None and call neither later tool. Any mismatch or carried-over result fails the whole trial.

**How I will check:** Use queries verified against the listings so the tee and jacket searches select different item IDs and the middle search has no match. Record copies of the actual tool inputs when each call starts, and compare them with that request's returned session and search results. Run the three-request sequence five times; each complete sequence counts as one trial.

**Why this target:**

Checking one request alone could miss an old item or fit card being reused on the next request. I want the tee, empty search, and jacket requests to stay separate. The code controls this state, so I expect all five sequences to pass even though the generated wording may change.

---

## 4. The fit card reports the listing details correctly

In at least four of five tries, the generated fit card identifies the selected item and states its price and platform correctly when compared with the selected listing. A missing or incorrect detail counts as a failure.

**How I will check:** Use five different selected listings with non-empty outfit suggestions. The caption may shorten or reword the title, but it must identify the same clothing type and must not change any item details it mentions, such as color, brand, or size. The price must have the same numeric value and the platform must name the same service; capitalization and equivalent price formatting are allowed. A missing caption also fails.

**Why this target:**

These details help the user understand what the agent found and where it is listed. The model can change the wording, but the facts should stay the same. I chose four of five because I expect consistent factual output while allowing one generation failure.

---

## 5. Outfit suggestions do not invent clothes the user owns

In all five tries, `suggest_outfit` must return non-empty styling advice for the selected item without describing any other item as already owned unless that item is present in the supplied `wardrobe["items"]`. Test two tries with the example wardrobe, two with a wardrobe containing only one item, and one with an empty wardrobe. Any invented ownership claim or empty response fails that try.

**How I will check:** Compare every reference to an owned wardrobe piece with the supplied item names and details. For example, "your white sneakers" fails if no white sneakers were provided. Additional pieces are allowed only when clearly presented as suggestions, such as "you could add white sneakers." With an empty wardrobe, the response must provide general styling advice without claiming any suggested pieces are already owned. The selected new item is provided separately and is not treated as an invented wardrobe item.

**Why this target:**

An outfit suggestion should use the wardrobe information I supplied. A small or empty wardrobe makes it tempting for the model to fill in missing pieces, but it should describe those as suggestions rather than possessions. I chose five of five because inventing what the user owns defeats the purpose of supplying a wardrobe, even if the outfit sounds convincing.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
